"""Psyche speaks and reads (Part 23 of *Psychology, Built*): the statistics of words, recognizing a word, finding
words in a stream, learning the past tense, and the cost of a surprising word.

Word statistics: Zipf's law fitted to a corpus, and the frequency of word types.  Recognizing a word: the
interactive activation model of McClelland and Rumelhart (1981), with a 14-segment font in the manner of Rumelhart
and Siple (1974), letter units in four positions and a lexicon of four-letter words; it reproduces the word
superiority effect of Reicher (1969) and Wheeler (1970).  Finding words: a learner that tracks transitional
probabilities between syllables (Saffran, Aslin and Newport 1996) and segments at their dips.  The past tense: a
two-route classifier, stem identity and stem endings, trained on a vocabulary that grows, in the manner of
Rumelhart and McClelland (1986), and the U-shaped curve of over-regularization it produces.  Surprisal: an
interpolated Kneser-Ney trigram language model, and reading times regressed on surprisal (Hale 2001; Levy 2008;
Smith and Levy 2013).
"""

from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np


# ============================================================================================== word statistics
def zipf_fit(counts, top: int | None = None) -> dict:
    """Zipf's law, frequency ~ C rank^-s: least squares on log frequency against log rank (over the ``top`` most
    frequent types, or all).  Returns the exponent s, the constant, R^2, and the ranks and frequencies."""
    f = np.sort(np.asarray(list(counts.values()) if isinstance(counts, dict) else counts, float))[::-1]
    if top:
        f = f[:top]
    r = np.arange(1, len(f) + 1, dtype=float)
    X = np.c_[np.ones(len(f)), np.log(r)]
    b, *_ = np.linalg.lstsq(X, np.log(f), rcond=None)
    res = np.log(f) - X @ b
    r2 = 1 - res.var() / np.log(f).var()
    return {"s": float(-b[1]), "logC": float(b[0]), "r2": float(r2), "rank": r, "freq": f}


# ============================================================================================== interactive activation
# A 14-segment font in the manner of Rumelhart and Siple (1974).  Segments: 0 top, 1 upper left, 2 upper right,
# 3 lower left, 4 lower right, 5 bottom, 6 middle left, 7 middle right, 8 upper centre, 9 lower centre, 10 upper-left
# diagonal, 11 upper-right diagonal, 12 lower-left diagonal, 13 lower-right diagonal.
SEGMENTS = {
    "A": (0, 1, 2, 3, 4, 6, 7), "B": (0, 2, 4, 5, 7, 8, 9), "C": (0, 1, 3, 5), "D": (0, 2, 4, 5, 8, 9),
    "E": (0, 1, 3, 5, 6), "F": (0, 1, 3, 6), "G": (0, 1, 3, 4, 5, 7), "H": (1, 2, 3, 4, 6, 7), "I": (0, 5, 8, 9),
    "J": (2, 3, 4, 5), "K": (1, 3, 6, 11, 13), "L": (1, 3, 5), "M": (1, 2, 3, 4, 10, 11), "N": (1, 2, 3, 4, 10, 13),
    "O": (0, 1, 2, 3, 4, 5), "P": (0, 1, 2, 3, 6, 7), "Q": (0, 1, 2, 3, 4, 5, 13), "R": (0, 1, 2, 3, 6, 7, 13),
    "S": (0, 1, 4, 5, 6, 7), "T": (0, 8, 9), "U": (1, 2, 3, 4, 5), "V": (1, 3, 11, 12), "W": (1, 2, 3, 4, 12, 13),
    "X": (10, 11, 12, 13), "Y": (9, 10, 11), "Z": (0, 5, 11, 12),
}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
IA_PARAMS = dict(fl_exc=0.005, fl_inh=0.15, lw_exc=0.07, lw_inh=0.04, ww_inh=0.21, wl_exc=0.30, decay=0.07,
                 a_max=1.0, a_min=-0.2)


def letter_features(ch: str | None) -> np.ndarray:
    """The 28 feature detectors of one position: 14 'segment present' then 14 'segment absent'.  None (a blank
    position) excites no detector; '#' is the mask, every segment present."""
    v = np.zeros(28)
    if ch is None:
        return v
    on = set(range(14)) if ch == "#" else set(SEGMENTS[ch])
    for s in range(14):
        v[s if s in on else 14 + s] = 1.0
    return v


class InteractiveActivation:
    """McClelland and Rumelhart's (1981) model: feature, letter and word levels in four positions, excitation
    between consistent units, inhibition between inconsistent ones and within the word level, and feedback from
    words to letters.  ``lexicon`` is a list of four-letter words; ``freq`` gives each word's resting level
    (from -0.92 for the rarest to 0 for the commonest, by log frequency)."""

    def __init__(self, lexicon, freq=None, **params):
        self.p = {**IA_PARAMS, **params}
        self.words = [w.upper() for w in lexicon]
        W = len(self.words)
        f = np.ones(W) if freq is None else np.asarray(freq, float)
        lf = np.log(f + 1)
        self.word_rest = -0.92 + 0.92 * (lf - lf.min()) / max(np.ptp(lf), 1e-9)
        # letter consistency with features: (26, 28)
        C = np.zeros((26, 28))
        for i, L in enumerate(LETTERS):
            C[i] = letter_features(L)
        self.consistent = C
        # word-letter membership: (W, 4, 26)
        M = np.zeros((W, 4, 26))
        for w, word in enumerate(self.words):
            for p_, ch in enumerate(word):
                M[w, p_, LETTERS.index(ch)] = 1.0
        self.M = M

    def _update(self, a, net, rest):
        p = self.p
        eff = np.where(net > 0, net * (p["a_max"] - a), net * (a - p["a_min"]))
        a = a + eff - p["decay"] * (a - rest)
        return np.clip(a, p["a_min"], p["a_max"])

    def run(self, display, cycles: int = 40, mask_at: int | None = None, record=None):
        """Run the network on a display (four characters, None for blank) for ``cycles`` cycles, replacing it by
        the mask '####' at cycle ``mask_at``.  Returns letter activations (cycles, 4, 26) and word activations
        (cycles, W)."""
        p = self.p
        W = len(self.words)
        L = np.zeros((4, 26))
        Wa = self.word_rest.copy()
        letters_t, words_t = [], []
        for t in range(cycles):
            shown = ["#"] * 4 if (mask_at is not None and t >= mask_at) else display
            F = np.stack([letter_features(c) for c in shown])  # (4, 28)
            # features -> letters: excitation from consistent detectors, inhibition from inconsistent ones
            on = F @ self.consistent.T                   # consistent detectors active
            off = F.sum(1, keepdims=True) - on            # inconsistent detectors active
            net_L = p["fl_exc"] * on - p["fl_inh"] * off
            Lp = np.clip(L, 0, None)
            Wp = np.clip(Wa, 0, None)
            # words -> letters (feedback)
            net_L = net_L + p["wl_exc"] * np.einsum("w,wpl->pl", Wp, self.M)
            # letters -> words: excitation from letters in the word, inhibition from letters not in it
            in_word = np.einsum("pl,wpl->w", Lp, self.M)
            not_in = Lp.sum() - in_word
            net_W = p["lw_exc"] * in_word - p["lw_inh"] * not_in - p["ww_inh"] * (Wp.sum() - Wp)
            L = self._update(L, net_L, 0.0)
            Wa = self._update(Wa, net_W, self.word_rest)
            letters_t.append(L.copy())
            words_t.append(Wa.copy())
        return np.array(letters_t), np.array(words_t)

    def forced_choice(self, display, position: int, target: str, foil: str, cycles: int = 40, mask_at: int = 12,
                      rate: float = 0.1, mu: float = 10.0) -> float:
        """Reicher's two-alternative test, read out as McClelland and Rumelhart did: a running average of each
        letter's activation at ``position`` (rate ``rate``), turned into the probability of reading each of the 26
        letters by Luce's rule with scale ``mu``; a letter that is read decides the choice, otherwise the subject
        guesses between target and foil.  The best accuracy over the trial is returned."""
        Lt, _ = self.run(display, cycles, mask_at)
        i, j = LETTERS.index(target), LETTERS.index(foil)
        o = np.zeros(26)
        best = 0.0
        for t in range(cycles):
            o = o + rate * (Lt[t, position] - o)
            s = np.exp(mu * o)
            pr = s / s.sum()
            best = max(best, pr[i] + 0.5 * (1 - pr[i] - pr[j]))
        return float(best)


# ============================================================================================== finding words
SAFFRAN_WORDS = ("tupiro", "golabu", "bidaku", "padoti")  # Saffran, Aslin and Newport (1996), Experiment 1


def syllables(word: str) -> list:
    return [word[i:i + 2] for i in range(0, len(word), 2)]


def syllable_stream(words=SAFFRAN_WORDS, n: int = 180, rng=None) -> list:
    """A continuous stream of ``n`` words, each a run of two-letter syllables, in random order with no word
    repeated twice in a row and no pauses: the stimulus of Saffran et al. (1996), as syllables."""
    rng = rng or np.random.default_rng(0)
    out, prev = [], None
    for _ in range(n):
        w = prev
        while w == prev:
            w = words[rng.integers(len(words))]
        out += syllables(w)
        prev = w
    return out


def transitional_probabilities(stream) -> dict:
    """P(next syllable | this syllable), counted over the stream."""
    pair = Counter(zip(stream[:-1], stream[1:]))
    first = Counter(stream[:-1])
    return {(a, b): c / first[a] for (a, b), c in pair.items()}


def segment(stream, tp: dict | None = None) -> list:
    """Cut the stream wherever the transitional probability dips below both its neighbours (a local minimum)."""
    tp = tp or transitional_probabilities(stream)
    p = np.array([tp[(a, b)] for a, b in zip(stream[:-1], stream[1:])])
    words, cur = [], [stream[0]]
    for k in range(len(p)):
        left = p[k - 1] if k > 0 else np.inf
        right = p[k + 1] if k + 1 < len(p) else np.inf
        if p[k] < left and p[k] < right:
            words.append("".join(cur))
            cur = []
        cur.append(stream[k + 1])
    words.append("".join(cur))
    return words


def word_score(item: str, tp: dict) -> float:
    """The mean transitional probability inside a candidate word: high for words, lower for part-words that
    straddle a boundary."""
    s = syllables(item)
    return float(np.mean([tp.get((a, b), 0.0) for a, b in zip(s[:-1], s[1:])]))


# ============================================================================================== the past tense
IRREGULAR = {
    "go": "went", "be": "was", "have": "had", "do": "did", "say": "said", "make": "made", "take": "took",
    "come": "came", "see": "saw", "know": "knew", "get": "got", "give": "gave", "find": "found", "think": "thought",
    "tell": "told", "become": "became", "leave": "left", "feel": "felt", "bring": "brought", "begin": "began",
    "keep": "kept", "hold": "held", "write": "wrote", "stand": "stood", "hear": "heard", "let": "let", "mean": "meant",
    "set": "set", "meet": "met", "run": "ran", "pay": "paid", "sit": "sat", "speak": "spoke", "lie": "lay",
    "lead": "led", "read": "read", "grow": "grew", "lose": "lost", "fall": "fell", "send": "sent", "build": "built",
    "understand": "understood", "draw": "drew", "break": "broke", "spend": "spent", "cut": "cut", "rise": "rose",
    "drive": "drove", "buy": "bought", "wear": "wore", "choose": "chose", "eat": "ate", "sing": "sang",
    "drink": "drank", "swim": "swam", "ring": "rang", "fly": "flew", "throw": "threw", "catch": "caught",
    "teach": "taught", "sleep": "slept", "forget": "forgot", "win": "won", "hide": "hid", "ride": "rode",
}
REGULAR = (
    "walk", "talk", "look", "want", "ask", "seem", "turn", "start", "show", "call", "try", "need", "help", "play",
    "move", "live", "believe", "happen", "include", "continue", "change", "watch", "follow", "stop", "create",
    "open", "learn", "add", "allow", "appear", "offer", "remember", "love", "consider", "wait", "serve", "die",
    "expect", "stay", "reach", "kill", "remain", "suggest", "raise", "pass", "report", "decide", "pull", "return",
    "explain", "hope", "develop", "carry", "receive", "agree", "support", "hit", "produce", "cover", "describe",
    "fill", "jump", "kick", "laugh", "listen", "smile", "cook", "clean", "dance", "rain", "push", "touch", "climb",
    "dream", "wash", "paint", "plant", "visit", "answer", "cry", "enjoy", "hurry", "marry", "worry", "study",
    "fix", "miss", "kiss", "pick", "pack", "lock", "knock", "shout", "point", "count", "hunt", "end", "mend",
    "bake", "shake", "share", "stare", "care", "save", "wave", "close", "use", "smell", "spell", "yell", "fail",
    "sail", "mail", "nail", "pour", "roar", "fear", "clear", "join", "rest", "test", "trust", "dust", "beg", "hug",
)


def regular_past(stem: str) -> str:
    if stem.endswith("e"):
        return stem + "d"
    if stem.endswith("y") and stem[-2] not in "aeiou":
        return stem[:-1] + "ied"
    return stem + "ed"


def _endings(stem: str) -> list:
    return [f"end:{stem[-k:]}" for k in (1, 2, 3) if len(stem) >= k] + [f"len:{min(len(stem), 6)}"]


def past_tense_learner(schedule, epochs_per_stage: int = 30, lr: float = 0.5, rng=None, l2: float = 1e-4,
                       track=None) -> dict:
    """A small network that learns the past tense from a vocabulary that grows.  Each verb is represented by two
    kinds of input unit: one for the stem itself (it can only learn that verb) and units for its last one, two and
    three letters (shared with every verb that ends the same way).  The output chooses among 'add -ed' and each
    irregular past form, by softmax, trained by gradient descent on the verbs in the current vocabulary, each seen
    in proportion to its token frequency.  ``schedule`` is a list of vocabularies (lists of stems), one per stage.
    Returns, after every epoch, the share of the irregular verbs known so far that are over-regularized (given
    'add -ed') and the share that are right."""
    rng = rng or np.random.default_rng(0)
    stems = sorted({v for voc in schedule for v in voc})
    feats = sorted({f for v in stems for f in [f"stem:{v}"] + _endings(v)})
    fi = {f: i for i, f in enumerate(feats)}
    outs = ["+ed"] + sorted({IRREGULAR[v] for v in stems if v in IRREGULAR})
    oi = {o: i for i, o in enumerate(outs)}
    X = np.zeros((len(stems), len(feats)))
    for k, v in enumerate(stems):
        for f in [f"stem:{v}"] + _endings(v):
            X[k, fi[f]] = 1.0
    y = np.array([oi[IRREGULAR[v]] if v in IRREGULAR else 0 for v in stems])
    sidx = {v: k for k, v in enumerate(stems)}
    W = np.zeros((len(feats), len(outs)))
    over, right, stage_of = [], [], []
    for s_, voc in enumerate(schedule):
        rows = np.array([sidx[v] for v in voc])
        weights = np.array([3.0 if v in IRREGULAR else 1.0 for v in voc])
        weights = weights / weights.sum()
        for _ in range(epochs_per_stage):
            for _ in range(len(rows)):
                k = rows[rng.choice(len(rows), p=weights)]
                z = X[k] @ W
                p = np.exp(z - z.max())
                p /= p.sum()
                p[y[k]] -= 1.0
                W -= lr * (np.outer(X[k], p) + l2 * W)
            irr = [sidx[v] for v in (track or schedule[0]) if v in IRREGULAR]
            if irr:
                Z = X[irr] @ W
                P = np.exp(Z - Z.max(1, keepdims=True))
                P /= P.sum(1, keepdims=True)
                over.append(float(P[:, 0].mean()))  # the probability given to 'add -ed'
                right.append(float(P[np.arange(len(irr)), y[irr]].mean()))
            else:
                over.append(np.nan)
                right.append(np.nan)
            stage_of.append(s_)
    return {"over": np.array(over), "right": np.array(right), "stage": np.array(stage_of), "outputs": outs}


# ============================================================================================== surprisal
WORD_RE = r"[a-z]+(?:'[a-z]+)?"


def tokenize(text: str) -> list:
    import re

    return re.findall(WORD_RE, text.lower())


class KneserNey:
    """An interpolated Kneser-Ney trigram model over words (Chen and Goodman 1999), with one absolute discount
    ``d``.  Words outside the ``vocab_size`` most frequent become '<unk>'.  ``surprisal(context, word)`` is
    -log2 P(word | the two words before)."""

    def __init__(self, tokens, d: float = 0.75, vocab_size: int = 30000):
        cnt = Counter(tokens)
        self.vocab = {w for w, _ in cnt.most_common(vocab_size)}
        toks = ["<s>", "<s>"] + [w if w in self.vocab else "<unk>" for w in tokens]
        self.d = d
        self.c3 = Counter(zip(toks, toks[1:], toks[2:]))
        self.c2 = Counter(zip(toks, toks[1:]))
        # continuation counts
        self.n1p_w = Counter(w for (_, w) in self.c2)            # N1+(. w)
        self.n1p_vw = Counter((v, w) for (_, v, w) in self.c3)    # N1+(. v w)
        self.n1p_v_dot_mid = Counter(v for (_, v, _) in self.c3)  # N1+(. v .)
        self.n1p_uv_dot = Counter((u, v) for (u, v, _) in self.c3)  # N1+(u v .)
        self.c2_ctx = Counter()
        for (u, v, _), c in self.c3.items():
            self.c2_ctx[(u, v)] += c
        self.n1p_v_dot = Counter(v for (v, _) in self.c2)          # N1+(v .)
        self.total_bigram_types = len(self.c2)

    def _p_uni(self, w):
        return (self.n1p_w.get(w, 0) + 1) / (self.total_bigram_types + len(self.vocab) + 1)

    def _p_bi(self, v, w):
        den = self.n1p_v_dot_mid.get(v, 0)
        if den == 0:
            return self._p_uni(w)
        num = max(self.n1p_vw.get((v, w), 0) - self.d, 0)
        lam = self.d * self.n1p_v_dot.get(v, 0) / den
        return num / den + lam * self._p_uni(w)

    def prob(self, u, v, w):
        u = u if u in self.vocab or u == "<s>" else "<unk>"
        v = v if v in self.vocab or v == "<s>" else "<unk>"
        w = w if w in self.vocab else "<unk>"
        den = self.c2_ctx.get((u, v), 0)
        if den == 0:
            return self._p_bi(v, w)
        num = max(self.c3.get((u, v, w), 0) - self.d, 0)
        lam = self.d * self.n1p_uv_dot.get((u, v), 0) / den
        return num / den + lam * self._p_bi(v, w)

    def surprisal(self, words) -> np.ndarray:
        """Surprisal in bits of each word of a sequence given the two before it."""
        seq = ["<s>", "<s>"] + list(words)
        return np.array([-np.log2(self.prob(seq[i - 2], seq[i - 1], seq[i])) for i in range(2, len(seq))])


def rt_regression(rt, surprisal, length, logfreq, prev_surprisal=None) -> dict:
    """Least squares of reading time on surprisal, word length and log frequency (and the previous word's
    surprisal, for spillover).  Returns the coefficients (ms per bit, per letter, per log unit), their standard
    errors and R^2."""
    cols = [np.ones(len(rt)), surprisal, length, logfreq]
    names = ["const", "surprisal", "length", "logfreq"]
    if prev_surprisal is not None:
        cols.append(prev_surprisal)
        names.append("prev_surprisal")
    X = np.c_[tuple(cols)]
    b, *_ = np.linalg.lstsq(X, rt, rcond=None)
    res = rt - X @ b
    s2 = res @ res / (len(rt) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return {"names": names, "coef": b, "se": se, "r2": float(1 - res.var() / np.var(rt))}


def random_typing(n_chars: int = 2_000_000, alphabet: str = "abcdefghijklmnopqrstuvwxyz", p_space: float = 0.18,
                  rng=None) -> Counter:
    """Miller's (1957) monkey: characters typed at random, a space with probability ``p_space``.  The 'words'
    between spaces follow a Zipf-like law with no meaning at all.  Returns their counts."""
    rng = rng or np.random.default_rng(0)
    probs = np.r_[np.full(len(alphabet), (1 - p_space) / len(alphabet)), p_space]
    chars = np.array(list(alphabet) + [" "])[rng.choice(len(probs), size=n_chars, p=probs)]
    return Counter(w for w in "".join(chars).split(" ") if w)


def cohort(word: str, lexicon) -> list:
    """Marslen-Wilson's cohort, letter by letter (letters standing in for speech sounds): the number of words in
    the lexicon that begin with the first k letters of ``word``, for k = 1..len(word).  The uniqueness point is
    the first k at which only one word is left."""
    lex = list(lexicon)
    return [sum(1 for w in lex if w.startswith(word[:k])) for k in range(1, len(word) + 1)]


def syllable_count(word: str) -> int:
    """A rough English syllable count: groups of vowels, less a silent final e (at least one)."""
    import re

    w = word.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def flesch(text: str) -> dict:
    """Flesch's (1948) reading ease, 206.835 - 1.015 (words per sentence) - 84.6 (syllables per word), with a rough
    syllable count.  Higher is easier; 60 to 70 is plain English."""
    import re

    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    syl = sum(syllable_count(w) for w in words)
    wps = len(words) / max(len(sentences), 1)
    spw = syl / max(len(words), 1)
    return {"score": 206.835 - 1.015 * wps - 84.6 * spw, "words_per_sentence": wps, "syllables_per_word": spw}
