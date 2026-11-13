"""Lab 12: match (a+)+b two ways, by backtracking and by sets of states, and count what determinism costs."""

from videos.coursekit import labs

import re

import numpy as np

from explainer.cs.lang import automata as A
from explainer.cs.lang import regex as R

TITLE = "A regex that doubles, and an automaton that does not"
GOAL = ("Run the part's naive backtracking matcher and its Thompson simulation on (a+)+b against strings of a's with "
        "no b, and count their steps. Then determinize 'the n-th symbol from the end is 1' and compare the DFA's "
        "size with 2^n, and check every engine against Python's re on random strings.")
TASKS = [
    "Try the pattern (a|aa)+b and then a+b on the same failing inputs. Which one still blows up, and how fast?",
    "Build the DFA for 'the n-th symbol from the START is 1' ('(0|1)' * (n - 1) + '1(0|1)*'). How many states now, and why?",
    "Count the steps of R.backtrack(R.parse('.*.*=.*'), 'x' * n, anchored=False) for n = 20, 40, 80. What power of n is it?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    node = R.parse("(a+)+b")
    nfa = R.thompson(node)
    ns = list(range(2, 17, 2))
    back, sets = [], []
    for n in ns:
        matched_b, steps = R.backtrack(node, "a" * n)
        matched_n, work, _ = nfa.run("a" * n)
        assert not matched_b and not matched_n
        assert steps == 7 * 2 ** n - 2, "the naive backtracker tries every way to cut the a's into groups"
        assert work == 13 * n - 4, "the set of active states does linear work"
        back.append(steps)
        sets.append(work)
    lab.row("(a+)+b on 16 a's: backtracking steps", f"{back[-1]:,}   (7 x 2^16 - 2 = {7 * 2 ** 16 - 2:,})")
    lab.row("(a+)+b on 16 a's: state-set work", f"{sets[-1]}   (13 x 16 - 4 = {13 * 16 - 4}; the NFA has {nfa.n} states)")
    lab.row("each two more a's multiply the backtracker by", f"{back[-1] / back[-2]:.2f}   (the film: about four)")

    sizes = []
    for n in range(1, 11):
        dfa = A.from_regex(A.nth_from_end(n), alphabet="01")
        sizes.append((R.compile(A.nth_from_end(n)).n, dfa.n, A.minimize(dfa).n))
        assert sizes[-1][2] == 2 ** n and dfa.n == 2 ** n + 1, "the smallest DFA needs 2^n states"
    lab.row("n-th symbol from the end, n = 10", f"NFA {sizes[-1][0]} states   subset DFA {sizes[-1][1]:,}   minimal DFA {sizes[-1][2]:,} = 2^10")

    pattern = "(a|b)*abb"
    engines = R.thompson(R.parse(pattern)), A.from_regex(pattern), A.minimize(A.from_regex(pattern))
    agree = 0
    for _ in range(400):
        text = "".join(rng.choice(list("ab"), int(rng.integers(0, 12))))
        want = re.fullmatch(pattern, text) is not None
        got = [engines[0].run(text)[0], engines[1].run(text), engines[2].run(text), R.backtrack(R.parse(pattern), text)[0]]
        assert got == [want] * 4, text
        agree += 1
    lab.row(f"{pattern}: NFA, DFA, minimal DFA", f"{engines[0].n}, {engines[1].n} and {engines[2].n} states; "
                                                 f"all agree with Python's re on {agree} random strings")
    assert (engines[0].n, engines[1].n, engines[2].n) == (14, 5, 4), "the film's three machines"
    lab.note = ("Backtracking pays for every way of splitting the a's, 2^(n-1) of them; following all states at once "
                "merges them. A DFA never backtracks either, but it can need exponentially many states: here "
                "exactly 2^n.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(ns, back, "o-", color=labs.RED, label="backtracking: 7 x 2^n - 2 steps")
    ax[0].plot(ns, sets, "o-", color=labs.GREEN, label="sets of states: 13 n - 4")
    ax[0].set(yscale="log", title="(a+)+b against n a's and no b", xlabel="number of a's, n", ylabel="steps (log scale)")
    ax[0].legend()
    n_axis = np.arange(1, 11)
    ax[1].plot(n_axis, [s[0] for s in sizes], "o-", color=labs.BLUE, label="Thompson NFA")
    ax[1].plot(n_axis, [s[2] for s in sizes], "o-", color=labs.GOLD, label="minimal DFA")
    ax[1].plot(n_axis, 2.0 ** n_axis, ls=":", color=labs.MUTED, label="2^n")
    ax[1].set(yscale="log", title="The n-th symbol from the end is 1", xlabel="n", ylabel="states (log scale)")
    ax[1].legend()
    lab.fig = fig
    return lab
