from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


class Expectation(VoiceoverScene):
    def construct(self):
        self.card()
        self.balance()
        self.layers()
        self.linearity()
        self.matches()
        self.birthdays()
        self.coupons()

    def card(self):
        card = chapter_card(11, r"Expectation", r"Pascal's averages, and the most useful trick in probability",
                            lit=(1654,), part=PART)
        with self.voiceover("Chapter eleven. Expectation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def balance(self):
        d = load("variables")
        pmf = np.asarray(d["pmf"])
        A = axes([1, 13], [0, 0.2], x_length=7.0, y_length=3.6, xticks=list(range(2, 13)), center=[-2.9, 0.2, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.42, height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=SIM,
                                  fill_opacity=0.85).move_to(ax.c2p(s, p / 2)) for s, p in zip(range(2, 13), pmf)])
        fulcrum = Triangle(color=EXACT, fill_color=EXACT, fill_opacity=1).scale(0.22).move_to(ax.c2p(7, 0) + DOWN * 0.55)
        fl = MathTex(r"E X = 7", font_size=34, color=EXACT).next_to(fulcrum, DOWN, buff=0.15)
        dfn = definition_card(r"Expectation", r"$E X = \sum_x x\, P(X = x) = \sum_\omega X(\omega)\, P(\omega)$: \ the "
                              r"balance point of the distribution", color=EXACT, width=5.4, font_size=23)
        dfn.move_to([4.3, 2.4, 0])
        lotus = definition_card(r"LOTUS", r"$E\, g(X) = \sum_x g(x)\, P(X = x)$: \ no need to find the distribution "
                                r"of $g(X)$ first", color=GREY_B, width=5.4, font_size=22, kind=r"the law of the "
                                r"unconscious statistician")
        lotus.move_to([4.3, -1.6, 0])
        with self.voiceover(
            "Pascal valued the interrupted game by averaging over its futures, and Huygens called it the value of a "
            "chance. Today it's called expectation. <bookmark mark='a'/> The expectation of a random variable is the "
            "sum of its values, each weighted by its probability. <bookmark mark='b'/> In pictures, it's the balance "
            "point of the distribution: put the probability bars on a seesaw, and the fulcrum that balances them "
            "is the expectation. For the sum of two dice it's seven. <bookmark mark='c'/> To find the expectation of "
            "a function of X, say X squared, you don't need the distribution of X squared. Weight g of each value by "
            "that value's probability. It's called the law of the unconscious statistician, because people use it "
            "without noticing that it needs a proof; on a finite space the proof is just regrouping a sum."
        ) as vo:
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(fulcrum, shift=UP * 0.2), FadeIn(fl))
            self.play(Rotate(VGroup(A, bars), angle=0.05, about_point=ax.c2p(7, 0)), run_time=0.6)
            self.play(Rotate(VGroup(A, bars), angle=-0.05, about_point=ax.c2p(7, 0)), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(lotus, shift=LEFT * 0.2))
        self.clear_scene()

    def layers(self):
        A = axes([0, 7], [0, 6.6], x_length=6.6, y_length=4.4, xlabel=r"value of a die", xticks=list(range(1, 7)),
                 center=[-3.3, -0.3, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        cols = [S.EST, S.LIK, S.ACCENT, S.POST, S.PRIOR, S.TREAT]
        # one column per face, height = face value; layers k = 1..6 run across faces >= k
        cells = VGroup()
        layer_of = []
        for v in range(1, 7):
            for k in range(1, v + 1):
                sq = Rectangle(width=0.86, height=0.62, stroke_color=BACKGROUND, stroke_width=2, fill_color=GREY_C,
                               fill_opacity=0.8).move_to(ax.c2p(v, k - 0.5))
                cells.add(sq)
                layer_of.append(k)
        cap = label(r"$E X = \tfrac16 (1 + 2 + \dots + 6) = \tfrac{21}{6}$", font_size=30).move_to([3.6, 2.4, 0])
        rows = VGroup(*[MathTex(rf"P(X \ge {k}) = \tfrac{{{7 - k}}}{{6}}", font_size=28, color=cols[k - 1])
                        for k in range(1, 7)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -0.2, 0])
        tot = MathTex(r"E X = \sum_{k \ge 1} P(X \ge k)", r"=", r"\tfrac{21}{6} = 3.5", font_size=32).move_to([3.5, -2.6, 0])
        tot[2].set_color(EXACT)
        gen = label(r"for $X \ge 0$: \ $E X = \int_0^\infty P(X > t)\, dt$", font_size=24, color=GREY_B)
        gen.next_to(tot, DOWN, buff=0.2)
        with self.voiceover(
            "There's a second way to compute an expectation, and it's often easier. <bookmark mark='a'/> Draw a die's "
            "six values as columns of blocks, the column for face v v blocks tall; the expectation is the average "
            "column height, twenty-one sixths. <bookmark mark='b'/> Now count the blocks by layer instead of by "
            "column. The bottom layer runs across every face: X is at least one with probability one. The second "
            "layer misses face one: X is at least two with probability five sixths. And so on up. "
            "<bookmark mark='c'/> Adding by layers gives the same total: the expectation of a variable with values "
            "one, two, three and so on is the sum of the chances that it's at least k. For a continuous variable "
            "the sum becomes an integral of the tail probability. It's called the layer-cake formula, and we'll use "
            "it again and again."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells], lag_ratio=0.03), FadeIn(cap))
            vo.wait_until("b")
            for k in range(1, 7):
                self.play(*[c.animate.set_fill(cols[k - 1], opacity=0.85) for c, l in zip(cells, layer_of) if l == k],
                          FadeIn(rows[k - 1], shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("c")
            self.play(Write(tot), FadeIn(gen))
        self.clear_scene()

    def linearity(self):
        rows = [
            cmath(r"E(X + Y)", r"=", r"\sum_\omega \big(X(\omega) + Y(\omega)\big) P(\omega)", font_size=36),
            cmath(r"E(X + Y)", r"=", r"\sum_\omega X(\omega) P(\omega) + \sum_\omega Y(\omega) P(\omega)", font_size=36),
            cmath(r"E(X + Y)", r"=", r"E X + E Y", font_size=40),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"the definition, \ on $\Omega$"), why(r"split the sum"), why(r"\emph{no independence needed}")]
        ind = definition_card(r"Indicator", r"$\mathbf 1_A = 1$ if $A$ happens, \ $0$ if not; \quad "
                              r"$E\, \mathbf 1_A = P(A)$", color=S.ACCENT, width=6.2, font_size=24).to_edge(DOWN, buff=0.4)
        title = label(r"Linearity: finite expectations", font_size=38).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The most useful fact about expectation is the simplest. <bookmark mark='a'/> The expectation of a sum "
            "is a sum over outcomes, <bookmark mark='b'/> and a sum over outcomes splits in two. "
            "<bookmark mark='c'/> So the expectation of X plus Y is the expectation of X plus the expectation of Y. "
            "Here the expectations are finite, so there is no undefined infinity minus infinity. X and Y can be "
            "as dependent as you like. <bookmark mark='d'/> Combine that with indicators, "
            "variables that are one when an event happens and zero when it doesn't, whose expectation is the "
            "event's probability, and you can compute averages of things whose distributions are hopeless."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=3, top=2.3, x=-1.2, buff=0.55)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(ind, shift=UP * 0.2))
        self.clear_scene()

    def matches(self):
        d = load("expectation")
        rows = [
            cmath(r"M", r"=", r"\sum_{i=1}^{n} \mathbf 1\{\text{card } i \text{ in place } i\}", font_size=34),
            cmath(r"E M", r"=", r"n \cdot \tfrac1n", r"=", r"1", font_size=38),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"count the matches with indicators"), why(r"each card is in its place w.p.\ $\tfrac1n$; \ "
                                                             r"linearity")]
        tbl = VGroup(*[MathTex(rf"n = {f['n']}:\ E M = {frac(f['E'])},\ \mathrm{{Var}}\, M = {frac(f['Var'])}",
                               font_size=22, color=EXACT) for f in d["fixed"][1:]]).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.1)
        tbl.move_to([-4.6, -1.6, 0])
        tcap = label(r"the engine, every order", font_size=20, color=GREY_B).next_to(tbl, UP, buff=0.15)
        counts = np.asarray(d["deck_counts"])
        pois = np.asarray(d["poisson"])
        A = axes([-0.6, 6.6], [0, 0.42], x_length=5.6, y_length=2.7, xlabel=r"matches in a shuffled deck of $52$",
                 xticks=list(range(0, 7)), yticks=[0, 0.2, 0.4], center=[2.8, -2.0, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.5, height=max(ax.c2p(0, c)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=SIM, fill_opacity=0.85).move_to(ax.c2p(k, c / 2))
                        for k, c in enumerate(counts[:7])])
        pts = VGroup(*[Dot(ax.c2p(k, p), radius=0.07, color=EXACT) for k, p in enumerate(pois[:7])])
        leg = legend([(SIM, rf"{fmt_int(10_000)} shuffles, \ mean {d['deck_mean']:.3f}"),
                      (EXACT, r"$e^{-1}/k!$: \ Part 3's Poisson")], font_size=20).next_to(A, UP, buff=0.15)
        intro = label('Matches in a shuffled deck', font_size=36)
        with self.voiceover(
            "Here's linearity working a miracle. <bookmark mark='a'/> Shuffle a deck, and count how many cards end "
            "up in their original position. Write that count as a sum of indicators, one per card. "
            "<bookmark mark='b'/> Each card lands in its own place with probability one over n, so the expected "
            "number of matches is n times one over n: one. For every n. The indicators are dependent, since if "
            "fifty-one cards are in place the fifty-second must be too, and it doesn't matter. "
            "<bookmark mark='c'/> The engine confirms it exactly for decks of two to eight cards, by listing every "
            "order; the variance turns out to be one as well. <bookmark mark='d'/> And ten thousand shuffles of a "
            "real deck average one match, with a distribution that's almost exactly e to the minus one over k "
            "factorial, a shape Part 3 will name: the Poisson."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=3.0, x=-0.4, buff=0.45)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(tcap), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in tbl], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1))
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.1), FadeIn(leg))
        self.clear_scene()

    def birthdays(self):
        d = load("expectation")
        pm = np.asarray(d["p_match"])
        A = axes([0, 70], [0, 1.0], x_length=7.6, y_length=4.4, xlabel=r"people in the room, $n$",
                 ylabel=r"P(two share a birthday)", xticks=[0, 10, 23, 40, 50, 70], yticks=[0, 0.5, 1],
                 center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = curve(ax, np.arange(len(pm)), pm, EXACT, 3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(70, 0.5), color=GREY_C, stroke_width=1.5)
        at23 = DashedLine(ax.c2p(23, 0), ax.c2p(23, pm[23]), color=S.ACCENT, stroke_width=2)
        dot = Dot(ax.c2p(23, pm[23]), radius=0.08, color=S.ACCENT)
        f1 = MathTex(r"1 - \frac{365 \cdot 364 \cdots (365 - n + 1)}{365^n}", font_size=30, color=EXACT).move_to([4.4, 2.6, 0])
        box = exact_sim(r"P_{23}", d["p23"], d["sim23"], 20_000, font_size=26, digits=3).move_to([4.4, 1.2, 0])
        pairs = MathTex(rf"E(\text{{shared pairs}}) = \binom{{23}}{{2}} \tfrac{{1}}{{365}} = {d['e_pairs23']:.3f}",
                        font_size=28, color=S.ACCENT).move_to([4.2, -0.4, 0])
        pw = label(r"$253$ pairs, \ each sharing with chance $\tfrac1{365}$: \ indicators again", font_size=22,
                   color=GREY_B).next_to(pairs, DOWN, buff=0.2)
        if pw.width > 5.6:
            pw.width = 5.6
        intro = label('The birthday problem', font_size=36)
        with self.voiceover(
            "Two more classics. <bookmark mark='a'/> How many people must be in a room for it to be more likely than "
            "not that two share a birthday? Ignoring leap years and assuming birthdays are equally likely, the "
            "chance that n people all differ is three sixty-five, times three sixty-four, and so on down, over three "
            "sixty-five to the n. <bookmark mark='b'/> The chance of a match crosses one half at just twenty-three "
            "people, <bookmark mark='c'/> and twenty thousand simulated rooms agree. <bookmark mark='d'/> Why so "
            "few? Because a match can happen between any pair, and twenty-three people make two hundred and "
            "fifty-three pairs. By indicators and linearity, the expected number of shared pairs is two hundred and "
            "fifty-three over three sixty-five, about seven tenths."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), Write(f1))
            vo.wait_until("b")
            self.play(Create(cv), Create(half), run_time=2.0)
            self.play(Create(at23), FadeIn(dot, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(box))
            vo.wait_until("d")
            self.play(FadeIn(pairs), FadeIn(pw))
        self.clear_scene()

    def coupons(self):
        d = load("expectation")
        k = d["k"]
        waits = [k / (k - i) for i in range(k)]
        A = axes([0, k + 1], [0, 52], x_length=6.0, y_length=3.4, xlabel=r"the $i$-th new sticker",
                 ylabel=r"expected packs to wait", xticks=[1, 10, 20, 30, 40, 50], yticks=[0, 25, 50],
                 center=[-3.4, 0.9, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.08, height=max(ax.c2p(0, w)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=S.ACCENT, fill_opacity=0.85).move_to(ax.c2p(i + 1, w / 2))
                        for i, w in enumerate(waits)])
        rows = [
            cmath(r"T", r"=", r"T_1 + T_2 + \cdots + T_{n}", font_size=32),
            cmath(r"E T", r"=", r"\frac{n}{n} + \frac{n}{n-1} + \cdots + \frac{n}{1}", r"=", r"n H_n", font_size=32),
            cmath(r"E T", r"=", rf"50 \cdot {d['H']:.3f}", r"=", rf"{d['mean_t']:.1f}", font_size=34),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"$T_i$: packs until the $i$-th new kind"), why(r"a wait for chance $p$ averages $1/p$"), None]
        times = np.asarray(d["times"])
        B = axes([50, 500], [0, 0.009], x_length=5.4, y_length=2.6, xlabel=r"packs to complete the album",
                 xticks=[100, 225, 300, 400, 500], center=[3.6, -1.75, 0])
        B.ax.y_axis.set_opacity(0)
        edges = np.linspace(50, 500, 46)
        hb = hist_bars(B.ax, edges, np.histogram(times, edges)[0] / (len(times) * np.diff(edges)), color=SIM)
        ml = Line(B.ax.c2p(d["mean_t"], 0), B.ax.c2p(d["mean_t"], 0.009), color=EXACT, stroke_width=3)
        hl = label(rf"$2{{,}}000$ albums: \ mean {d['sim_mean_t']:.1f}", font_size=22, color=SIM).next_to(B, UP, buff=0.1)
        intro = label('The coupon collector', font_size=36)
        with self.voiceover(
            "Last, the coupon collector. <bookmark mark='a'/> An album has fifty different stickers, and each pack "
            "contains one, chosen at random. How many packs do you expect to buy to fill the album? "
            "<bookmark mark='b'/> Split the wait into stages: T one packs until your first new sticker, T two until "
            "the second new kind, and so on. The total is their sum. <bookmark mark='c'/> When you have i minus one "
            "kinds, a pack is new with probability n minus i plus one over n, and a wait for an event of chance p "
            "averages one over p. <bookmark mark='d'/> Early on, almost every pack is new. At the end you wait fifty "
            "packs, on average, for the last sticker. <bookmark mark='e'/> Add the expectations, linearity again, "
            "and you get n times the harmonic number H n, which grows like n log n. <bookmark mark='f'/> For fifty "
            f"stickers, {d['mean_t']:.0f} packs. <bookmark mark='g'/> Two thousand simulated albums average "
            f"{d['sim_mean_t']:.0f}, with a long right tail: some collectors need four hundred."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A))
            vo.wait_until("b")
            step = ladder(self, rows, whys, keep=3, top=3.3, x=3.3, buff=0.45, edge=6.9)
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("f")
            step(2)
            vo.wait_until("g")
            self.play(FadeIn(B), FadeIn(hb), Create(ml), FadeIn(hl))
        self.clear_scene()
