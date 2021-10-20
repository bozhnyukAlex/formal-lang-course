import pytest
from pyformlang.cfg import Production, Variable, Terminal, Epsilon

from project.cfg_utils import (
    get_cnf_from_file,
    get_wcnf_from_file,
    is_wcnf,
    get_original_csg_from_file,
)


def test_wrong_file():
    path_not_exists = "tests/data/cfgs/emp"
    path_not_txt = "tests/data/cfgs/empty"
    path_to_empty = "tests/data/cfgs/empty.txt"

    with pytest.raises(OSError):
        get_cnf_from_file(path_not_exists)
    with pytest.raises(OSError):
        get_cnf_from_file(path_not_txt)
    with pytest.raises(OSError):
        get_cnf_from_file(path_to_empty)


def test_wrong_text():
    with pytest.raises(ValueError):
        get_cnf_from_file("tests/data/cfgs/exception.txt")


@pytest.mark.parametrize(
    "filename, axiom",
    [
        ("epsilon_cfg.txt", "E"),
        ("example_1.txt", "S"),
        ("random.txt", "NP"),
        ("example_2.txt", "S"),
        ("example_3.txt", "S"),
        ("example_4.txt", "S"),
        ("math.txt", "Expr"),
    ],
)
def test_cnf_from_file_start_symbol(filename, axiom):
    path = "tests/data/cfgs/" + filename

    wcnf = get_wcnf_from_file(path, axiom)

    assert wcnf.start_symbol == Variable(axiom)


@pytest.mark.parametrize(
    "filename, axiom, productions",
    [
        ("epsilon_cfg.txt", "E", {Production(Variable("E"), [Epsilon()])}),
        (
            "example_1.txt",
            "S",
            {
                Production(Variable("C#CNF#1"), [Variable("S"), Variable("b#CNF#")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("S"), [Variable("S"), Variable("S")]),
                Production(Variable("b#CNF#"), [Terminal("b")]),
                Production(Variable("S"), []),
                Production(Variable("a#CNF#"), [Terminal("a")]),
            },
        ),
        (
            "random.txt",
            "NP",
            {
                Production(Variable("CN"), [Terminal("boy")]),
                Production(Variable("Det"), [Terminal("the")]),
                Production(Variable("Wh"), [Terminal("whom")]),
                Production(Variable("S/NP"), [Variable("NP"), Variable("VP/NP")]),
                Production(Variable("VTrans"), [Terminal("hates")]),
                Production(Variable("NP"), [Variable("Det"), Variable("CN")]),
                Production(Variable("VP/NP"), [Variable("VTrans"), Variable("NP")]),
                Production(Variable("NP"), [Terminal("mark")]),
                Production(Variable("C#CNF#1"), [Variable("Wh"), Variable("S/NP")]),
                Production(Variable("CN"), [Variable("CN"), Variable("C#CNF#1")]),
            },
        ),
        (
            "math.txt",
            "Expr",
            {
                Production(Variable("MulOp"), [Terminal("div")]),
                Production(Variable("Factor"), [Terminal("variable")]),
                Production(Variable("Factor"), [Terminal("number")]),
                Production(Variable("Term"), [Terminal("number")]),
                Production(Variable("Term"), [Terminal("variable")]),
                Production(Variable("Expr"), [Terminal("variable")]),
                Production(Variable("Expr"), [Terminal("number")]),
                Production(Variable("MulOp"), [Terminal("mul")]),
                Production(Variable("Primary"), [Terminal("variable")]),
                Production(Variable("AddOp"), [Terminal("sub")]),
                Production(Variable("AddOp"), [Terminal("add")]),
                Production(Variable("Primary"), [Terminal("number")]),
                Production(Variable("Expr"), [Variable("Expr"), Variable("C#CNF#3")]),
                Production(
                    Variable("C#CNF#2"), [Variable("pow#CNF#"), Variable("Primary")]
                ),
                Production(
                    Variable("Factor"), [Variable("Factor"), Variable("C#CNF#2")]
                ),
                Production(
                    Variable("C#CNF#1"), [Variable("MulOp"), Variable("Factor")]
                ),
                Production(Variable("Term"), [Variable("Term"), Variable("C#CNF#1")]),
                Production(Variable("Expr"), [Variable("AddOp"), Variable("Term")]),
                Production(Variable("C#CNF#3"), [Variable("AddOp"), Variable("Term")]),
                Production(Variable("pow#CNF#"), [Terminal("pow")]),
                Production(Variable("Term"), [Variable("Factor"), Variable("C#CNF#2")]),
                Production(Variable("Expr"), [Variable("Term"), Variable("C#CNF#1")]),
                Production(Variable("Expr"), [Variable("Factor"), Variable("C#CNF#2")]),
            },
        ),
        (
            "example_2.txt",
            "S",
            {
                Production(Variable("C#CNF#2"), [Variable("c#CNF#"), Variable("B")]),
                Production(Variable("A"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
                Production(Variable("C#CNF#1"), [Variable("B"), Variable("C#CNF#2")]),
                Production(Variable("B"), [Variable("d#CNF#"), Variable("C#CNF#3")]),
                Production(
                    Variable("C#CNF#3"), [Variable("e#CNF#"), Variable("f#CNF#")]
                ),
                Production(Variable("f#CNF#"), [Terminal("f")]),
                Production(Variable("S"), [Variable("A"), Variable("B")]),
                Production(Variable("c#CNF#"), [Terminal("c")]),
                Production(Variable("d#CNF#"), [Terminal("d")]),
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("e#CNF#"), [Terminal("e")]),
            },
        ),
    ],
)
def test_cnf_from_file_productions(filename, axiom, productions):
    path = "tests/data/cfgs/" + filename
    wcnf = get_wcnf_from_file(path, axiom)
    assert set(wcnf.productions) == set(productions)


@pytest.mark.parametrize(
    "filename, axiom",
    [
        ("epsilon_cfg.txt", "E"),
        ("random.txt", "NP"),
        ("example_2.txt", "S"),
        ("example_4.txt", "S"),
        ("math.txt", "Expr"),
    ],
)
def test_get_wcnf_from_file(filename, axiom):
    path = "tests/data/cfgs/" + filename

    csg_old = get_original_csg_from_file(path, axiom)
    cnf = get_cnf_from_file(path, axiom)

    assert is_wcnf(cnf, csg_old)
