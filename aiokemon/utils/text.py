def levenshtein_osa(a: str, b: str) -> int:
    """A slightly-modified version of the traditional Levenshtein algorithm
    that considers an adjacent character swap as one operation rather than
    two.
    """
    a_len = len(a)
    b_len = len(b)
    D = [list(range(i, b_len + 1 + i)) for i in range(a_len + 1)]

    for i in range(1, a_len + 1):
        for j in range(1, b_len + 1):
            cost = (a[i - 1] != b[j - 1])
            D[i][j] = min(D[i - 1][j] + 1,          # deletion
                          D[i][j - 1] + 1,          # insertion
                          D[i - 1][j - 1] + cost)   # substitution
            if (
                    (i > 1 and j > 1)
                and (a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1])
            ):
                D[i][j] = min(
                    D[i][j], D[i - 2][j - 2] + 1    # adjacent transposition
                )

    return D[a_len][b_len]
