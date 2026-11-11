from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        tiles = Group(
            tile(MathTex(r"A(Br) \overset{?}{=} Cr", font_size=40, color=DATA), r"Freivalds; \ Schwartz--Zippel", DATA),
            tile(MathTex(r"\binom{n}{2}^{-1}", font_size=44, color=LAM), r"Karger's contraction", LAM),
            tile(MathTex(r"\le \tfrac14", font_size=44, color=YES), r"Miller--Rabin", YES),
            tile(MathTex(r"(1 - e^{-kn/m})^k", font_size=40, color=HEAD), r"Bloom filters", HEAD),
            tile(MathTex(r"\frac{eN}{w},\ e^{-d}", font_size=40, color=COST), r"Count-Min: \ ledger row 9", COST),
            tile(MathTex(r"\frac{1.04}{\sqrt{m}}", font_size=44, color=CTRL), r"HyperLogLog", CTRL),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Randomness as a Resource", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            "What we built in this part. Las Vegas and Monte Carlo, and amplification. Freivalds' check and the "
            "Schwartz–Zippel lemma, with perfect matchings and fingerprints. Karger's random contractions. "
            'Miller–Rabin. Random walks for satisfiability, balls in bins and the power of two choices. Bloom '
            'filters, reservoirs, Misra–Gries and Count-Min, and the Job in eighteen kilobytes. HyperLogLog, the AMS'
            ' sketch and MinHash. The probabilistic method, and the ways to remove the coins.'
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"fingerprints: \ Rabin--Karp string search", [21]),
            (r"LSH for nearest neighbours in high dimensions", [22]),
            (r"randomized rounding; \ MAX-CUT's 0.878", [23]),
            (r"BPP, \ hardness against randomness, \ streaming lower bounds", [27]),
            (r"pseudorandom generators; \ big primes", [29, 30]),
            (r"Bloom filters per run in LSM trees", [34]),
            (r"sketches in production; \ SimHash in a crawler", [46, 47]),
            (r"two choices in load balancers; \ expanders", [48, 56]),
        ], font_size=23)
        with self.voiceover(
            (
            "Where this comes back. Part 21 turns fingerprints into Rabin and Karp's string search, and Part 22 uses"
            ' locality-sensitive hashing for nearest neighbours. Part 23 rounds linear programs at random, including'
            " MAX-CUT's famous 0.878. Part 27 develops BPP, hardness against randomness and the lower bounds for "
            "streams. Part 29 builds cryptographic generators, and Part 30 needs the big primes. Part 34's storage "
            'engines keep a Bloom filter per file; Parts 46 and 47 run sketches and SimHash in production; and Part '
            "48's load balancers use two choices, while Part 56 builds the expanders."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"databases", r"Bloom filters in RocksDB, \ Cassandra and Bigtable; \ HyperLogLog in Redis and BigQuery"),
            (r"networks", r"Count-Min and heavy hitters in routers; \ two random choices in load balancers"),
            (r"caches", r"W-TinyLFU's Count-Min admission filter \ (Caffeine)"),
            (r"data", r"MinHash deduplication of web crawls and language-model training sets"),
            (r"security", r"probable-prime screening where needed; \ operating-system randomness; \ ChaCha20"),
        ])
        with self.voiceover(
            (
            'In practice, databases use Bloom filters and approximate count-distinct sketches. Routers estimate '
            'heavy hitters, load balancers sample choices, and caches use frequency summaries. MinHash helps propose'
            ' near-duplicate documents for verification. Security protocols require strong randomness, and some '
            'public-key systems generate large primes. Elliptic-curve handshakes show why not every secure '
            'connection starts with freshly generated primes. Each application must choose its own accuracy, '
            'confidence and threat model.'
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Exact-arithmetic Freivalds with $r$ uniform in $\{0, \dots, q - 1\}^n$: \ prove a wrong $C$ passes with probability "
            r"$\le 1/q$, \ and that this is tight.",
            r"For fixed $\alpha\ge1$, \ prove an $O_\alpha(n^{2\alpha})$ bound on cuts within factor $\alpha$ "
            r"of a positive minimum cut, \ using contraction.",
            r"A Bloom filter with false-positive rate $\varepsilon$: \ show the optimum needs $m = n \log_2(1/\varepsilon)"
            r"/ \ln 2 \approx 1.44\, n \log_2 (1/\varepsilon)$ bits.",
            r"Weighted sampling in one pass: \ keep the $k$ items with the largest $u_i^{1/w_i}$, \ $u_i$ uniform, \ "
            r"and prove ordered sampling without replacement, \ each next choice proportional to remaining weight.",
            r"\textit{Design.} \ Sketch 256-register HyperLogLog in Pebble using repeated halving; \ explain finite-hash "
            r"limits. \ The notes' pseudocode is unexecuted.",
            r"$\bigstar$ \textit{Research.} \ Give a deterministic polynomial-time algorithm that decides whether an "
            r"arithmetic circuit computes the zero polynomial.",
        ], font_size=22)
        with self.voiceover(
            (
            'Six problems, with worked arguments in the notes. The fifth is a design exercise: a Pebble HyperLogLog '
            'sketch using repeated halving, with finite-hash limitations. Its pseudocode has not been compiled or '
            'benchmarked as a finished program. The last is a research problem, marked with a star: general '
            'deterministic polynomial identity testing. Its solution is unknown, and the notes give a starting '
            'point.'
        )
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 21, \ Strings", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"searching text with automata built from patterns \ (KMP)", DATA),
            (r"indexes of every suffix", LAM),
            (r"a reversible transform that sorts a book into runs \ (Burrows--Wheeler)", YES),
            (r"searching the novels while they stay compressed", COST))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"every \texttt{git diff} is a shortest path on a grid", font_size=26, color=GREY_A
                  ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            (
            'Next time, the oldest data of all, text. Searching it efficiently leads to automata built from '
            'patterns, to indexes of every suffix, and to a reversible transform that sorts a book into compressible'
            ' runs, so that we can search the novels while they stay compressed. And every git diff turns out to be '
            'a shortest path on a grid. Part 21, Strings.'
        )
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Motwani and Raghavan, \textit{Randomized Algorithms}; \ Mitzenmacher and Upfal, \textit{Probability "
             r"and Computing}",
             r"Alon and Spencer, \textit{The Probabilistic Method}",
             r"Cormode and Yi, \textit{Small Summaries for Big Data}; \ Muthukrishnan, \textit{Data Streams}",
             r"Knuth, \textit{The Art of Computer Programming}, \ volume 2, \ chapter 3"],
            [r"Freivalds (1977); \ Schwartz (1980); \ Zippel (1979); \ Lov\'asz (1979); \ Karger (1993); \ Karger "
             r"and Stein (1996)",
             r"Miller (1976); \ Rabin (1980); \ Agrawal, Kayal and Saxena (2004); \ Sch\"oning (1999); \ Azar et al. "
             r"(1999)",
             r"Bloom (1970); \ Vitter (1985); \ Misra and Gries (1982); \ Cormode and Muthukrishnan (2005); \ Estan "
             r"and Varghese (2002)",
             r"Flajolet and Martin (1985); \ Flajolet et al. (2007); \ Alon, Matias and Szegedy (1996); \ Broder "
             r"(1997); \ Indyk and Motwani (1998)",
             r"Erd\H{o}s (1947); \ Moser and Tardos (2010); \ Impagliazzo and Wigderson (1997); \ Kabanets and "
             r"Impagliazzo (2004)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover((
            'The books and papers this part follows are on screen and in the notes. Thank you for watching.'
        )):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
