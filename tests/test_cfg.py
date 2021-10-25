import pytest
from pyformlang.cfg import Production, Variable, Terminal, Epsilon

from project.cfg_utils import (
    get_cnf_from_file,
    get_wcnf_from_file,
    is_wcnf,
    get_original_cfg_from_file,
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
            "example_3.txt",
            "S",
            {
                Production(Variable("a#CNF#"), [Terminal("a")]),
                Production(Variable("S"), [Variable("a#CNF#"), Variable("b#CNF#")]),
                Production(Variable("S"), []),
                Production(Variable("b#CNF#"), [Terminal("b")]),
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

    csg_old = get_original_cfg_from_file(path, axiom)
    cnf = get_cnf_from_file(path, axiom)

    assert is_wcnf(cnf, csg_old)
