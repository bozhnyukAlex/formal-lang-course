import sys

import pytest

from project.graph_query_language.parser import parse


@pytest.mark.parametrize(
    "text, accept",
    [
        (
            """
g = LOAD GRAPH "go";
g = SET START OF (SET FINAL OF g TO (GET VERTICES FROM g)) TO {1..100};
l1 = "l1" | "l2";
q1 = ("type" | l1)*;
q2 = "subclass_of" . q;
res1 = g & q1;
res2 = g & q2;
s = GET START VERTICES FROM g;
vertices1 = FILTER (LAMBDA v: v IN s) (MAP (LAMBDA ((u_g,u_q1),l,(v_g,v_q1)): u_g) (GET EDGES FROM res1));
vertices2 = FILTER (LAMBDA v: v IN s) (MAP (LAMBDA ((u_g,u_q2),l,(v_g,v_q1)): u_g) (GET EDGES FROM res2));
vertices3 = vertices1 & vertices2;
PRINT vertices3;
""",
            True,
        ),
        ('g = LOAD GRAPH "go"', False),
    ],
)
def test_parse_prog(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.prog()
    act = parser.getNumberOfSyntaxErrors() == 0
    print("errors: " + str(parser.getNumberOfSyntaxErrors()))
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("PRINT g2", True),
        ("print g2", False),
        ("PRINT {1..100}", True),
        ("PRINT", False),
        ('g1 = LOAD GRAPH "wine" ', True),
        ("g1 = LOAD GRAPH", False),
        ("g1 = {1..100}", True),
    ],
)
def test_parse_statement(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.stmt()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("g1 & g2", True),
        ("g1", True),
        ("{2..100} & {1}", True),
        ("", False),
        ("(GET EDGES FROM g) & {(1, 2)}", True),
        ("(GET FROM g) & {(1, 2)}", False),
        ("l1 . l2 . l3 | l4", True),
        ("l1 . l2 . l3 & l4", True),
        ('"label1" . "label2" | "label3"', True),
        ("FILTER (LAMBDA x: x IN s) g", True),
    ],
)
def test_parse_expr(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.expr()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("_a", True),
        ("graph1", True),
        ("213", False),
        ("неверный ввод", False),
    ],
)
def test_parse_variable(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.var()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("LAMBDA x, y, z : x", True),
        ("LAMBDA v: v IN s", True),
        ("LAMBDA ((u_g,u_q2),l,(v_g,v_q1)) : u_g", True),
        ("LAMBDA {x, y, z} : 1", False),
        ("LAMBDA 1, 2, 3: 1", False),
        ("LAMBDA x,y,z-> x", False),
    ],
)
def test_parse_lambda(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.anfunc()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("MAP (LAMBDA x : x) g", True),
        ("MAP (LAMBDA ((u_g,u_q1),l,(v_g,v_q1)): u_g) (GET EDGES FROM res1)", True),
        (" MAP (LAMBDA 1 : 1) 1", False),
        ("MAP p p", False),
    ],
)
def test_parse_map(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.mapping()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("FILTER (LAMBDA x: x) g", True),
        (
            "FILTER (LAMBDA ((u_g,u_q1),l,(v_g,v_q1)): u_g) (GET EDGES FROM res1)",
            True,
        ),
        (" FILTER (LAMBDA 1: 1) 1", False),
        ("FILTER p p", False),
    ],
)
def test_parse_filter(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.filtering()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("TRUE", True),
        ("FALSE", True),
        ("True", False),
        ("False", False),
        ("{1..100}", True),
        ("(1..100)", False),
        ("{1, 2, 3}", True),
        ("{1, 2, 3)", False),
        (
            '''"""
    S -> A S B S
    A -> a
    B -> b
    """
    ''',
            True,
        ),
        ('(1, "l", 2)', True),
        ('("l", "k", "m")', False),
        ("{(1, 2), (3, 4), (5, 6)}", True),
        ("{(1, 2), ('l', 4), (5, 6)}", False),
        ('"label"', True),
        ("label", False),
        ('{"l1", "l2"}', True),
        ('{"l1", l2}', False),
        ("0", True),
        ("_0", False),
        ("SET START OF g TO {1..100}", True),
        ("SET START OF g TO {1,,100}", False),
        ("SET FINAL OF g TO {1..100}", True),
        ("ADD START OF g TO {1, 2, 3}", True),
        ("ADD FINAL OF g TO labels1", True),
        ("GET VERTICES FROM g", True),
        ("GET START VERTICES FROM g", True),
        ("GET REACHABLE VERTICES FROM g", True),
        ("GET FROM g", False),
        ("GET LABELS FROM g", True),
        ("GET EDGES FROM g", True),
        ("GET EDGES FROM 1", False),
        ("GET START FROM 1", False),
    ],
)
def test_parse_val(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.val()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept
