import pytest
from pyformlang.cfg import CFG

from project import cyk, get_original_cfg_from_file


@pytest.mark.parametrize(
    "cfg, words",
    [
        (
            """
                    S -> epsilon
                    """,
            [""],
        ),
        (
            """
                    S -> a S b S
                    S -> epsilon
                    """,
            ["", "aabbababaaabbb", "ab", "aaaabbbb"],
        ),
    ],
)
def test_cyk_accept(cfg, words):
    cfg = CFG.from_text(cfg)
    assert all(cyk(cfg, word) for word in words)


@pytest.mark.parametrize(
    "cfg, words",
    [
        (
            """
                    S -> epsilon
                    """,
            ["epsilon", "abab"],
        ),
        (
            """""",
            ["", "epsilon"],
        ),
        (
            """
                    S -> a S b S
                    S -> epsilon
                    """,
            ["aba", "abcd"],
        ),
    ],
)
def test_cyk_not_accept(cfg, words):
    cfg = CFG.from_text(cfg)
    assert all(not cyk(cfg, word) for word in words)


@pytest.mark.parametrize(
    "grammar_file, words_file",
    [
        (
            "epsilon.txt",
            "epsilon_words_accept.txt",
        ),
        (
            "grammar.txt",
            "grammar_words_accept.txt",
        ),
    ],
)
def test_cyk_from_file_accept(grammar_file, words_file):
    grammar_path = "tests/data/cyk/" + grammar_file
    words_path = "tests/data/cyk/" + words_file
    words_file = open(words_path, "r")
    words = words_file.readlines()
    words = list(map(lambda s: s.rstrip("\n"), words))
    words_file.close()
    cfg = get_original_cfg_from_file(grammar_path)
    assert all(cyk(cfg, word) for word in words)


@pytest.mark.parametrize(
    "grammar_file, words_file",
    [
        (
            "epsilon.txt",
            "epsilon_words_not_accept.txt",
        ),
        (
            "empty_grammar.txt",
            "empty_words.txt",
        ),
        (
            "grammar.txt",
            "grammar_words_not_accept.txt",
        ),
    ],
)
def test_cyk_from_file_not_accept(grammar_file, words_file):
    grammar_path = "tests/data/cyk/" + grammar_file
    words_path = "tests/data/cyk/" + words_file
    grammar_file = open(grammar_path, "r")
    words_file = open(words_path, "r")
    words = words_file.readlines()
    words = list(map(lambda s: s.rstrip("\n"), words))
    words_file.close()
    grammar = grammar_file.readlines()
    grammar_file.close()
    cfg = CFG.from_text("\n".join(grammar))
    assert all(not cyk(cfg, word) for word in words)
