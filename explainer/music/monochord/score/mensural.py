"""Mensural notation: the first marks whose shapes say how long (Part 10).

``L`` is a long, ``B`` a breve, ``S`` a semibreve.  Under *imperfect* time a breve is two semibreves, always.  Under
*perfect* time it is three, unless its neighbours change it, by the rules Franco of Cologne wrote down in the
thirteenth century (stated here for breves and semibreves, as the next century used them):

    one semibreve between two breves        it is counted with the breve before it, which loses a third (imperfection)
    two semibreves between two breves       the second is doubled (alteration), so that the two fill a perfection
    three                                   a perfection of their own
    more than three                         the first imperfects the breve before; the rest go in threes (the rule as
                                            Apel's handbook summarizes it; the film uses only the first three cases)

A dot (``.``) after a note marks the end of a perfection and switches the first rule off.
"""

from __future__ import annotations


def read(symbols: str, perfect: bool = True) -> list[int]:
    """The length of every breve and semibreve of ``symbols``, in semibreves."""
    notes = []                                         # (symbol, dotted)
    for c in symbols:
        if c == "." and notes:
            notes[-1] = (notes[-1][0], True)
        elif c in "BS":
            notes.append((c, False))
    if not perfect:
        return [2 if c == "B" else 1 for c, _ in notes]
    out, i = [], 0
    while i < len(notes):
        if notes[i][0] == "B":
            out.append(3)
            i += 1
            continue
        j = i
        while j < len(notes) and notes[j][0] == "S":   # a run of semibreves
            j += 1
        n = rest = j - i
        after = i > 0 and notes[i - 1] == ("B", False)  # an undotted breve stands before the run
        before = j < len(notes)                        # and a breve after it
        if after and (n % 3 == 1 or (n > 3 and n % 3 == 2)):
            out[-1] = 2                                # the first semibreve imperfects the breve before
            rest = n - 1
        out.extend([1] * n)
        i = j
        if before and rest % 3 == 2:
            out[-1] = 2                                # alteration: the last semibreve before the breve is doubled
        elif before and rest % 3 == 1:
            out.append(2)                              # one left over: it imperfects the breve after, from the front
            i = j + 1
    return out


def perfections(lengths) -> bool:
    """Do the lengths fill whole groups of three?"""
    return sum(lengths) % 3 == 0
