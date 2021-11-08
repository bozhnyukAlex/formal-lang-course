from pyformlang.cfg import CFG

__all__ = ["cyk"]


def cyk(cfg: CFG, word: str) -> bool:
    """
    Determines whether the given string can be generated in the given context-free grammar

    Parameters
    ----------
    cfg: CFG
        input grammar
    word: str
        word for checking

    Returns
    -------
    bool
        true if word can be generated in the given cfg
        false otherwise

    """
    word_len = len(word)

    if not word_len:
        return cfg.generate_epsilon()

    cnf = cfg.to_normal_form()

    term_productions = [p for p in cnf.productions if len(p.body) == 1]
    var_productions = [p for p in cnf.productions if len(p.body) == 2]

    dp_matrix = [[set() for _ in range(word_len)] for _ in range(word_len)]

    for i in range(word_len):
        dp_matrix[i][i].update(
            production.head.value
            for production in term_productions
            if word[i] == production.body[0].value
        )

    for step in range(1, word_len):
        for i in range(word_len - step):
            j = i + step
            for k in range(i, j):
                dp_matrix[i][j].update(
                    production.head.value
                    for production in var_productions
                    if production.body[0].value in dp_matrix[i][k]
                    and production.body[1].value in dp_matrix[k + 1][j]
                )
    return cnf.start_symbol.value in dp_matrix[0][word_len - 1]
