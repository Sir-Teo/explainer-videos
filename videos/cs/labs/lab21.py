"""Lab 21: find a pattern four ways in a synthetic text, invert its Burrows-Wheeler transform, and check Myers' diff."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.algo import strings as st

TITLE = "Four matchers, one transform, one diff"
GOAL = ("Count the character comparisons of naive search, Knuth-Morris-Pratt and Boyer-Moore on a text of random "
        "words, check the naive count against its exact prefix identity and its worst case, sort the suffixes, invert "
        "the Burrows-Wheeler transform, count by backward search, and check Myers' diff against the LCS.")
TASKS = [
    "Shrink the alphabet to 'ab' in make_text. Boyer-Moore's comparisons per character rise: which of its two shift rules is now doing the work?",
    "Search for a pattern that does not occur and print fm.steps: how many rank requests does backward search make before the interval is empty?",
    "Apply st.move_to_front to the text itself and to its transform, and compare their entropies with the two bars of the figure.",
]


def make_text(rng, words=2500):
    """Space-separated words drawn with Zipf-like frequencies from a vocabulary of 120 random lowercase words."""
    letters = np.array(list("etaoinshrdlucmfwyp"))
    vocab = ["".join(rng.choice(letters, int(rng.integers(2, 9)))) for _ in range(120)]
    p = 1 / np.arange(1, len(vocab) + 1)
    return " ".join(rng.choice(vocab, words, p=p / p.sum())).encode()


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    text = make_text(rng)
    n = len(text)

    # 1. three matchers, the same answers; the naive count is an exact sum over matching prefixes
    lengths, per_char = [2, 3, 4, 6, 8, 12, 16, 24, 32], {"naive": [], "KMP": [], "Boyer-Moore": []}
    for m in lengths:
        tot = {k: 0 for k in per_char}
        for _ in range(3):
            i = int(rng.integers(0, n - m))
            pat = text[i:i + m]
            (h1, c1), (h2, c2), (h3, c3, _) = st.naive(text, pat), st.kmp(text, pat), st.boyer_moore(text, pat)
            assert h1 == h2 == h3 and i in h1, "the three matchers find the same occurrences"
            t = np.frombuffer(text, dtype=np.uint8)
            A, alive, identity = n - m + 1, np.ones(n - m + 1, dtype=bool), 0
            for j in range(m):  # alignments whose first j characters match each cost one more comparison
                identity += int(alive.sum())
                alive &= t[j:j + A] == pat[j]
            assert c1 == identity, "naive comparisons = the number of matching proper prefixes, over all alignments"
            assert c2 <= 2 * n, "KMP never exceeds 2n"
            for k, c in zip(per_char, (c1, c2, c3)):
                tot[k] += c / (3 * n)
        for k, series in per_char.items():
            series.append(tot[k])
    i8, i32 = lengths.index(8), lengths.index(32)
    lab.row("comparisons per character, m = 8", "   ".join(f"{k} {per_char[k][i8]:.3f}" for k in per_char))
    lab.row("comparisons per character, m = 32", "   ".join(f"{k} {per_char[k][i32]:.3f}" for k in per_char))
    assert per_char["naive"][i8] < 1.3 and per_char["Boyer-Moore"][i8] < 0.4 and per_char["Boyer-Moore"][i32] < 0.2

    # 2. the worst case: a^n against a^(m-1) b
    wn, wm = 3000, 40
    wt, wp = b"a" * wn, b"a" * (wm - 1) + b"b"
    (_, cn), (_, ck) = st.naive(wt, wp), st.kmp(wt, wp)
    assert cn == (wn - wm + 1) * wm and ck <= 2 * wn
    lab.row("worst case, n = 3,000, m = 40", f"naive {cn:,} = (n - m + 1) m   KMP {ck:,} <= 2n = {2 * wn:,}")

    # 3. suffix array, the Burrows-Wheeler transform and backward search
    T = text + b"\0"
    sa = st.suffix_array(T)
    assert list(sa[:400]) == st.suffix_array_naive(T)[:400] and sorted(sa) == list(range(len(T)))
    L = st.bwt_from_sa(T, sa)
    assert st.inverse_bwt(L) == T, "the LF mapping walks the text back out"
    fm = st.FMIndex(T, sa)
    for m in (1, 2, 4, 7):
        i = int(rng.integers(0, n - m))
        pat = text[i:i + m]
        fm.steps = 0
        count, (lo, hi) = fm.count(pat)
        assert count == len(st.naive(text, pat)[0]) and fm.steps == 2 * m, "two rank requests per pattern character"
        assert sorted(fm.locate(r) for r in range(lo, hi)) == st.naive(text, pat)[0], "and the rows locate the hits"
    lab.row("backward search, 7 characters", f"{count} occurrences counted with 14 rank requests, against {st.naive(text, pat)[1]:,} comparisons for a scan")
    h_text, h_bwt = st.entropy(np.frombuffer(T, dtype=np.uint8)), st.entropy(np.frombuffer(L, dtype=np.uint8))
    mtf_text, mtf_bwt = st.entropy(st.move_to_front(T)), st.entropy(st.move_to_front(L))
    assert st.runs(L) < 0.6 * st.runs(T) and mtf_bwt < 0.7 * mtf_text, "sorting by context gathers equal characters"
    assert abs(h_text - h_bwt) < 0.01, "the transform is a permutation: its letter counts are unchanged"
    lab.row("runs of equal characters", f"text {st.runs(T):,}   transform {st.runs(L):,}   ({len(T):,} characters)")
    lab.row("entropy after move-to-front", f"text {mtf_text:.2f} bits   transform {mtf_bwt:.2f} bits   (letters alone: {h_text:.2f})")

    # 4. Myers' diff: D = n + m - 2 LCS
    for _ in range(20):
        a = [int(v) for v in rng.integers(0, 6, int(rng.integers(5, 40)))]
        b = [v for v in a if rng.random() > 0.2] + [int(v) for v in rng.integers(0, 6, int(rng.integers(0, 5)))]
        d = st.myers(a, b)[0]
        assert d == len(a) + len(b) - 2 * st.lcs_len(a, b), "Myers' D is the insert-delete distance"
    lab.row("Myers' diff", "D = n + m - 2 LCS on 20 random pairs of sequences")
    lab.note = ("The naive scan costs about one comparison per character on word-like text and (n - m + 1) m at worst; "
                "KMP's 2n holds on any text; Boyer-Moore reads less the longer the pattern; and the sorted transform "
                "can be both inverted and searched.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for (k, v), color in zip(per_char.items(), (labs.RED, labs.BLUE, labs.GREEN)):
        ax[0].loglog(lengths, v, "o-", color=color, label=k)
    ax[0].loglog(lengths, [1 / m for m in lengths], color=labs.MUTED, ls="--", label="1/m")
    ax[0].set(title="Comparisons per character of text", xlabel="pattern length m", ylabel="comparisons / n")
    ax[0].set_xticks(lengths, [str(m) for m in lengths])
    ax[0].minorticks_off()
    ax[0].legend()
    names = ["text,\nletters", "transform,\nletters", "text,\nmove-to-front", "transform,\nmove-to-front"]
    ax[1].bar(names, [h_text, h_bwt, mtf_text, mtf_bwt], color=[labs.BLUE, labs.GOLD, labs.BLUE, labs.GOLD], width=0.6)
    ax[1].set(title="Zero-order entropy before and after the transform", ylabel="bits per character")
    lab.fig = fig
    return lab
