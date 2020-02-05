# -*- coding: utf-8 -*-
"""
    saltrewrite.testsuite.fix_asserts
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This rewrites unittest `self.assert*` into plain assertions

    The source for most of this code is:

        https://github.com/craigds/decrapify/blob/master/pytestify.py
"""
from functools import wraps

from bowler import Query
from bowler import TOKEN
from bowler.types import Leaf
from bowler.types import Node
from fissix.fixer_util import ArgList
from fissix.fixer_util import Attr
from fissix.fixer_util import Call
from fissix.fixer_util import Comma
from fissix.fixer_util import Dot
from fissix.fixer_util import KeywordArg
from fissix.fixer_util import touch_import
from fissix.pygram import python_symbols as syms
from saltrewrite.utils import keyword
from saltrewrite.utils import parenthesize_if_necessary

# NOTE: these don't take inversions into account.
# Hence why assertNotEqual is a synonym of assertEqual
SYNONYMS = {
    "assertEquals": "assertEqual",
    "failUnlessEqual": "assertEqual",
    "assertNotEqual": "assertEqual",
    "failIfEqual": "assertEqual",
    "assertIsNot": "assertIs",
    "assertNotIn": "assertIn",
    "failUnless": "assertTrue",
    "assert_": "assertTrue",
    "assertFalse": "assertTrue",
    "failIf": "assertTrue",
    "assertIsNotNone": "assertIsNone",
    "assertMultiLineEqual": "assertEqual",
    "assertSequenceEqual": "assertEqual",
    "assertListEqual": "assertEqual",
    "assertTupleEqual": "assertEqual",
    "assertSetEqual": "assertEqual",
    "assertDictEqual": "assertEqual",
    "assertNotIsInstance": "assertIsInstance",
    "assertNotAlmostEqual": "assertAlmostEqual",
}


ARGUMENTS = {
    "assertEqual": 2,
    "assertIs": 2,
    "assertIn": 2,
    "assertGreater": 2,
    "assertLess": 2,
    "assertGreaterEqual": 2,
    "assertLessEqual": 2,
    "assertIsInstance": 2,
    # TODO: assertRaises()
    "assertAlmostEqual": 2,
    "assertTrue": 1,
    "assertIsNone": 1,
}


OPERATORS = {
    "assertEqual": Leaf(TOKEN.EQEQUAL, "==", prefix=" "),
    "assertIs": Leaf(TOKEN.NAME, "is", prefix=" "),
    "assertIn": Leaf(TOKEN.NAME, "in", prefix=" "),
    "assertTrue": [],
    "assertIsNone": [Leaf(TOKEN.NAME, "is", prefix=" "), Leaf(TOKEN.NAME, "None", prefix=" "),],
    "assertGreater": Leaf(TOKEN.GREATER, ">", prefix=" "),
    "assertLess": Leaf(TOKEN.LESS, "<", prefix=" "),
    "assertGreaterEqual": Leaf(TOKEN.GREATEREQUAL, ">=", prefix=" "),
    "assertLessEqual": Leaf(TOKEN.LESSEQUAL, "<=", prefix=" "),
}


# Functions where we invert the operator, or add a 'not'
INVERT_FUNCTIONS = {
    "assertNotEqual",
    "failIfEqual",
    "assertIsNot",
    "assertNotIn",
    "assertFalse",
    "failIf",
    "assertIsNotNone",
    "assertNotIsInstance",
    "assertNotAlmostEqual",
}
BOOLEAN_VALUES = ("True", "False")


def rewrite(paths, interactive):
    (
        Query(paths)
        .select_class("TestCase")
        # NOTE: You can append as many .select().modify() bits as you want to one query.
        # Each .modify() acts only on the .select[_*]() immediately prior.
        .select_method("assertEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertEquals")
        .modify(callback=assertmethod_to_assert)
        .select_method("failUnlessEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertNotEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("failIfEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIs")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIsNot")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIn")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertNotIn")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertTrue")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertFalse")
        .modify(callback=assertmethod_to_assert)
        .select_method("assert_")
        .modify(callback=assertmethod_to_assert)
        .select_method("failUnless")
        .modify(callback=assertmethod_to_assert)
        .select_method("failIf")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIsNone")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIsNotNone")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertGreater")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertGreaterEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertLess")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertLessEqual")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertIsInstance")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertNotIsInstance")
        .modify(callback=assertmethod_to_assert)
        .select_method("assertAlmostEqual")
        .modify(callback=assertalmostequal_to_assert)
        .select_method("assertNotAlmostEqual")
        .modify(callback=assertalmostequal_to_assert)
        .select(
            """
            function_call=power<
                self_attr="self" raises_attr=trailer< "." "assertRaises" >
                trailer< '(' function_arguments=any* ')' >
            >
        """
        )
        .modify(callback=handle_assertraises)
        # Actually run all of the above.
        .write(interactive=interactive)
    )


# TODO : Add this to fissix.fixer_util
def Assert(test, message=None, **kwargs):
    """Build an assertion statement"""
    if not isinstance(test, list):
        test = [test]
    test[0].prefix = " "
    if message is not None:
        if not isinstance(message, list):
            message = [message]
        message.insert(0, Comma())
        message[1].prefix = " "

    node = Node(syms.assert_stmt, [Leaf(TOKEN.NAME, "assert")] + test + (message or []), **kwargs,)
    print(123, node)
    return node


def conversion(func):
    """
    Decorator. Handle some boilerplate
    """

    @wraps(func)
    def wrapper(node, capture, filename):
        if capture.get("function_def"):
            # Not interested in `def assertEqual`, leave that alone.
            # We only care about *calls*
            return node

        arguments_nodes = capture["function_arguments"]
        if not arguments_nodes:
            return node

        # This is wrapped in a list for some reason?
        arguments_node = arguments_nodes[0]

        if arguments_node.type == syms.arglist:
            # multiple arguments
            actual_arguments = [n for n in arguments_node.children if n.type != TOKEN.COMMA]
        else:
            # one argument
            actual_arguments = [arguments_node]

        # Un-multi-line, where a and b are on separate lines
        actual_arguments = [a.clone() for a in actual_arguments]
        for a in actual_arguments:
            a.prefix = " "

        # Avoid creating syntax errors for multi-line nodes
        # (this is overly restrictive, but better than overly lax)
        # https://github.com/facebookincubator/Bowler/issues/12
        actual_arguments = [parenthesize_if_necessary(a) for a in actual_arguments]

        assertion = func(node, capture, actual_arguments)

        if assertion is not None:
            node.parent.set_child(0, assertion)
            node.remove()

    return wrapper


@conversion
def assertmethod_to_assert(node, capture, arguments):
    """
    self.assertEqual(foo, bar, msg)
    --> assert foo == bar, msg

    self.assertTrue(foo, msg)
    --> assert foo, msg

    self.assertIsNotNone(foo, msg)
    --> assert foo is not None, msg

    .. etc
    """
    function_name = capture["function_name"].value
    invert = function_name in INVERT_FUNCTIONS
    function_name = SYNONYMS.get(function_name, function_name)
    num_arguments = ARGUMENTS[function_name]

    if len(arguments) not in (num_arguments, num_arguments + 1):
        # Not sure what this is. Leave it alone.
        return None

    if len(arguments) == num_arguments:
        message = None
    else:
        message = arguments.pop()
        if message.type == syms.argument:
            # keyword argument (e.g. `msg=abc`)
            message = message.children[2].clone()

    if function_name == "assertIsInstance":
        arguments[0].prefix = ""
        assert_test_nodes = [Call(keyword("isinstance"), [arguments[0], Comma(), arguments[1]])]
        if invert:
            assert_test_nodes.insert(0, keyword("not"))
    elif function_name == "assertAlmostEqual":
        arguments[1].prefix = ""
        # TODO: insert the `import pytest` at the top of the file
        if invert:
            op_token = Leaf(TOKEN.NOTEQUAL, "!=", prefix=" ")
        else:
            op_token = Leaf(TOKEN.EQEQUAL, "==", prefix=" ")
        assert_test_nodes = [
            Node(
                syms.comparison,
                [
                    arguments[0],
                    op_token,
                    Node(
                        syms.power,
                        Attr(keyword("pytest"), keyword("approx", prefix=""))
                        + [
                            ArgList(
                                [
                                    arguments[1],
                                    Comma(),
                                    KeywordArg(keyword("abs"), Leaf(TOKEN.NUMBER, "1e-7")),
                                ]
                            )
                        ],
                    ),
                ],
            )
        ]
        # Adds a 'import pytest' if there wasn't one already
        touch_import(None, "pytest", node)

    else:
        op_tokens = OPERATORS[function_name]
        if not isinstance(op_tokens, list):
            op_tokens = [op_tokens]
        op_tokens = [o.clone() for o in op_tokens]

        if invert:
            if not op_tokens:
                op_tokens.append(keyword("not"))
            elif op_tokens[0].type == TOKEN.NAME and op_tokens[0].value == "is":
                op_tokens[0] = Node(syms.comp_op, [keyword("is"), keyword("not")], prefix=" ")
            elif op_tokens[0].type == TOKEN.NAME and op_tokens[0].value == "in":
                op_tokens[0] = Node(syms.comp_op, [keyword("not"), keyword("in")], prefix=" ")
            elif op_tokens[0].type == TOKEN.EQEQUAL:
                op_tokens[0] = Leaf(TOKEN.NOTEQUAL, "!=", prefix=" ")

        if num_arguments == 2:
            # a != b, etc.
            assert_test_nodes = [arguments[0]] + op_tokens + [arguments[1]]
        elif function_name == "assertTrue":
            assert_test_nodes = op_tokens + [arguments[0]]
            # not a
        elif function_name == "assertIsNone":
            # a is not None
            assert_test_nodes = [arguments[0]] + op_tokens

    return Assert(assert_test_nodes, message.clone() if message else None, prefix=node.prefix)


@conversion
def assertalmostequal_to_assert(node, capture, arguments):
    function_name = capture["function_name"].value
    invert = function_name in INVERT_FUNCTIONS
    function_name = SYNONYMS.get(function_name, function_name)

    nargs = len(arguments)
    if nargs < 2 or nargs > 5:
        return None

    def get_kwarg_value(index, name):
        i = 0
        for a in arguments:
            if a.type == syms.argument:
                if a.children[0].value == name:
                    return a.children[2].clone()
            else:
                if i == index:
                    return a.clone()
                i += 1
        return None

    first = get_kwarg_value(0, "first")
    second = get_kwarg_value(1, "second")

    if first is None or second is None:
        # Not sure what this is, leave it alone
        return

    places = get_kwarg_value(2, "places")
    msg = get_kwarg_value(3, "msg")
    delta = get_kwarg_value(4, "delta")

    if delta is not None:
        try:
            abs_delta = float(delta.value)
        except ValueError:
            # this should be a number, give up.
            return
    else:
        if places is None:
            places = 7
        else:
            try:
                places = int(places.value)
            except (ValueError, AttributeError):
                # this should be an int, give up.
                return
        abs_delta = "1e-%d" % places

    arguments[1].prefix = ""
    if invert:
        op_token = Leaf(TOKEN.NOTEQUAL, "!=", prefix=" ")
    else:
        op_token = Leaf(TOKEN.EQEQUAL, "==", prefix=" ")
    assert_test_nodes = [
        Node(
            syms.comparison,
            [
                arguments[0],
                op_token,
                Node(
                    syms.power,
                    Attr(keyword("pytest"), keyword("approx", prefix=""))
                    + [
                        ArgList(
                            [
                                arguments[1],
                                Comma(),
                                KeywordArg(keyword("abs"), Leaf(TOKEN.NUMBER, abs_delta)),
                            ]
                        )
                    ],
                ),
            ],
        )
    ]
    # Adds a 'import pytest' if there wasn't one already
    touch_import(None, "pytest", node)

    return Assert(assert_test_nodes, msg.clone() if msg else None, prefix=node.prefix)


@conversion
def handle_assertraises(node, capture, arguments):
    """
    with self.assertRaises(x):

        --> with pytest.raises(x):

    self.assertRaises(ValueError, func, arg1)

        --> pytest.raises(ValueError, func, arg1)
    """
    capture["self_attr"].replace(keyword("pytest", prefix=capture["self_attr"].prefix))
    capture["raises_attr"].replace(Node(syms.trailer, [Dot(), keyword("raises", prefix="")]))
    # Let's remove the msg= keyword argument if found
    for child in node.children:
        if child.type != syms.trailer:
            continue
        for tchild in child.children:
            if tchild.type != syms.arglist:
                continue
            previous_argument = None
            for argument in tchild.children:
                if isinstance(argument, Leaf):
                    previous_argument = argument
                    continue
                if isinstance(argument, Node):
                    if argument.type != syms.argument:
                        previous_argument = argument
                        continue
                    for leaf in argument.leaves():
                        if leaf.value == "msg":
                            argument.remove()
                            if previous_argument.value == ",":
                                # previous_argument is a comma, remove it.
                                previous_argument.remove()

    # Adds a 'import pytest' if there wasn't one already
    touch_import(None, "pytest", node)
