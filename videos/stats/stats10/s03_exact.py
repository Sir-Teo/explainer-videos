from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class Exact(VoiceoverScene):
    def construct(self):
        self.card()
        self.tea_null()
        self.designs()
        self.table()
        self.darwin()
        self.flips()
        self.machine()
        self.why_random()

    def card(self):
        card = chapter_card(2, r"Exact tests by design", r"Randomization makes the null distribution", lit=(1935,), part=PART)
        with self.voiceover("Chapter two. Exact tests by design."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def tea_null(self):
        d = load("tea")["8"]
        pmf = np.asarray(d["pmf"])
        A = axes([-0.5, 4.5], [0, 0.6], x_length=6.4, y_length=3.8, xlabel=r"milk-first cups correctly chosen, \ of 4",
                 ylabel=r"$P_{H_0}$", xticks=[0, 1, 2, 3, 4], yticks=[0, 0.25, 0.5], center=[-2.8, -0.2, 0])
        ax = A.ax
        bars = bars_at(ax, range(5), pmf, 0.7, NULLC, highlight={4}, hcolor=OBS)
        labs = VGroup(*[MathTex(rf"\tfrac{{{c}}}{{70}}", font_size=26).next_to(bars[i], UP, buff=0.08) for i, c in enumerate((1, 16, 36, 16, 1))])
        rows = fit_rows(VGroup(
            MathTex(r"P(j \text{ right}) = \frac{\binom4j\binom4{4-j}}{\binom84}", font_size=32),
            label(r"the hypergeometric law (Part 3): \ $1, 16, 36, 16, 1$ out of 70", font_size=24, color=GREY_A),
            MathTex(r"p = P(4 \text{ right}) = \tfrac1{70} = 0.014", font_size=30, color=OBS),
            MathTex(r"P(\ge 3 \text{ right}) = \tfrac{17}{70} = 0.24", font_size=30),
            label(r"three right is not convincing: \ a guesser does it one time in four", font_size=24, color=GREY_A),
        ), 5.4, 0.32, [3.9, -0.2, 0])
        with self.voiceover(
            "Let's work out the tea test completely. <bookmark mark='a'/> If the lady is guessing, her four choices are "
            "a random four of the eight cups. The number of milk-first cups among them has a hypergeometric "
            "distribution, from Part 3: choose j of the four milk-first cups and four minus j of the others. "
            "<bookmark mark='b'/> The counts are one, sixteen, thirty-six, sixteen and one, out of seventy. "
            "<bookmark mark='c'/> All four right has probability one in seventy. That's the p-value if she gets them "
            "all. <bookmark mark='d'/> But three right, or better, has probability seventeen in seventy, about one in "
            "four. Fisher was explicit: with this design only a perfect score would count as evidence. One mistake, and it does not reject at five percent, though the result still contains information about her skill."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(labs), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(bars[4], color=OBS))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def designs(self):
        d = load("tea")
        hdr = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (r"cups", r"ways to choose", r"$p$ for a perfect score")])
        xs = [-4.0, -0.4, 3.6]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.4, 0])
        cells = VGroup()
        for i, cups in enumerate(("6", "8", "10", "12")):
            y = 1.7 - 0.6 * i
            r = d[cups]
            cells.add(VGroup(MathTex(cups, font_size=32).move_to([xs[0], y, 0]),
                             MathTex(f"{r['splits']}", font_size=32).move_to([xs[1], y, 0]),
                             MathTex(rf"\tfrac{{1}}{{{r['splits']}}} = {r['all']:.4f}", font_size=30, color=OBS).move_to([xs[2], y, 0])))
        pw = d["power"]
        rows = fit_rows(VGroup(
            label(r"and a lady with real but imperfect skill? \ independent binary perceptions correct with chance $q$; choose four, breaking ties randomly:", font_size=24),
            MathTex(rf"P(\text{{perfect score with 8 cups}}):\ \ q = 0.7:\ {pw['0.7']:.2f},\quad q = 0.8:\ {pw['0.8']:.2f},\quad q = 0.9:\ {pw['0.9']:.2f}",
                    font_size=28, color=ALTC),
            label(r"only a perfect observed score passes; even a skilled taster can fail: \ Fisher's design has little \emph{power} \ (ch.~4)", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -1.9, 0])
        tag = simulated_tag(r"simulated: \ 40,000 sessions per $q$", corner=DR)
        with self.voiceover(
            "The design decides how much evidence is possible. <bookmark mark='a'/> With six cups, three of each, a "
            "perfect score has probability one in twenty under guessing: not much. With eight, one in seventy. With ten, "
            "one in two hundred and fifty-two; with twelve, one in nine hundred and twenty-four. More cups, more "
            "possible evidence. <bookmark mark='b'/> But consider a lady with real, imperfect skill, right about each cup "
            "with probability q, before enforcing the choice of exactly four milk-first cups by random tie-breaking. These power numbers depend on that response model. <bookmark mark='c'/> Simulating her sessions: if she's right seventy percent of the time, "
            "she achieves a perfect score with eight cups only eleven percent of the time; at eighty percent, a quarter "
            "of the time; even at ninety percent, only half. <bookmark mark='d'/> The test controls the chance of being "
            "fooled by a guesser, but it often fails to detect a genuine skill. That second kind of failure is what "
            "Neyman and Pearson would build their theory on, in chapter four."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def table(self):
        cells = [[r"4", r"0"], [r"0", r"4"]]
        grid = VGroup()
        for i in range(2):
            for j in range(2):
                sq = Square(side_length=1.6, stroke_color=GREY_B, stroke_width=2)
                sq.move_to([-3.6 + 1.6 * j, 0.8 - 1.6 * i, 0])
                grid.add(VGroup(sq, MathTex(cells[i][j], font_size=40, color=OBS if i == j else WHITE).move_to(sq)))
        rl = VGroup(label(r"milk first", font_size=22, color=GREY_A).next_to(grid[0], LEFT, buff=0.25),
                    label(r"tea first", font_size=22, color=GREY_A).next_to(grid[2], LEFT, buff=0.25))
        cl = VGroup(label(r"she says milk", font_size=22, color=GREY_A).next_to(grid[0], UP, buff=0.2),
                    label(r"she says tea", font_size=22, color=GREY_A).next_to(grid[1], UP, buff=0.2))
        rows = fit_rows(VGroup(
            label(r"Fisher's exact test for any $2 \times 2$ table:", font_size=26),
            label(r"fix both margins; \ under independence the top-left count is hypergeometric", font_size=24, color=GREY_A),
            MathTex(r"P(a) = \frac{\binom{a + c}{a}\binom{b + d}{b}}{\binom{n}{a + b}}", font_size=34, color=OBS),
            label(r"exact at any sample size: \ no normal approximation", font_size=24, color=GREY_A),
            label(r"\texttt{statkit.tests.fisher\_exact}", font_size=22, color=GREY_A),
        ), 6.4, 0.34, [3.3, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Written as a table, the tea experiment is a two by two: the truth in the rows, her "
            "answers in the columns. A perfect score puts four on the diagonal and zero off it. <bookmark mark='b'/> "
            "Fisher's exact test works for any such table. Hold both sets of margins fixed: here, four of each kind of "
            "cup, and four of each answer. <bookmark mark='c'/> Then if rows and columns are independent, the top-left "
            "count has a hypergeometric distribution, and its tail probability is the p-value. "
            "<bookmark mark='d'/> No normal approximation is involved, so it's exact at any sample size, which is why "
            "it's still the standard test for small tables, in clinical trials and genetics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def darwin(self):
        d = load("darwin")
        diffs = np.asarray(d["d"])
        A = axes([0.5, 15.5], [-80, 80], x_length=7.0, y_length=4.2, ylabel=r"cross $-$ self, \ eighths of an inch",
                 yticks=[-80, -40, 0, 40, 80], center=[-2.6, -0.2, 0])
        ax = A.ax
        zero = Line(ax.c2p(0.5, 0), ax.c2p(15.5, 0), color=GREY_B, stroke_width=2)
        bars = VGroup()
        for i, v in enumerate(diffs):
            top, bot = ax.c2p(i + 1, max(v, 0)), ax.c2p(i + 1, min(v, 0))
            bars.add(Rectangle(width=0.32, height=max(abs(top[1] - bot[1]), 1e-3), stroke_width=0,
                               fill_color=DATA if v > 0 else REJ, fill_opacity=0.85).move_to((top + bot) / 2))
        hc = history_card(1876, r"Charles Darwin, \ \emph{Cross and Self Fertilisation}", r"15 pairs of maize plants, \ one cross- and "
                          r"one self-fertilized, \ grown in the same pots", color=DATA, width=4.8, font_size=20).move_to([4.6, 1.6, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"\textstyle\sum d_i = {d['sum']:.0f}", font_size=32, color=OBS),
            label(r"13 of 15 favour crossing", font_size=24),
            label(r"Galton looked at them for Darwin; \ Fisher returned to them in 1935", font_size=22, color=GREY_A),
        ), 4.6, 0.3, [4.6, -1.0, 0])
        src = historical_tag(r"Darwin (1876), \ via Fisher (1935)", corner=DR)
        with self.voiceover(
            "Fisher's other example in 1935 was an experiment of Charles Darwin's. <bookmark mark='a'/> Darwin grew "
            "fifteen pairs of maize plants, one cross-fertilized and one self-fertilized in each pair, side by side in the "
            "same pots, and measured their heights. <bookmark mark='b'/> Here are the fifteen differences, cross minus "
            "self, in eighths of an inch. Thirteen favour the crossed plant, two the self-fertilized one. "
            "<bookmark mark='c'/> Their sum is three hundred and fourteen. Darwin had asked his cousin Francis Galton for "
            "help with the numbers. Fisher returned to them with a new idea."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[2]))
        self.clear_scene()

    def flips(self):
        d = load("darwin")
        diffs = np.asarray(d["d"])
        A = axes([0.5, 15.5], [-80, 80], x_length=5.6, y_length=2.6, yticks=[-80, 0, 80], center=[-3.6, 1.6, 0], font_size=18)
        ax = A.ax
        zero = Line(ax.c2p(0.5, 0), ax.c2p(15.5, 0), color=GREY_B, stroke_width=2)

        def bar_set(vals):
            g = VGroup()
            for i, v in enumerate(vals):
                top, bot = ax.c2p(i + 1, max(v, 0)), ax.c2p(i + 1, min(v, 0))
                g.add(Rectangle(width=0.22, height=max(abs(top[1] - bot[1]), 1e-3), stroke_width=0,
                                fill_color=DATA if v > 0 else REJ, fill_opacity=0.85).move_to((top + bot) / 2))
            return g

        bars = bar_set(diffs)
        sum_t = MathTex(rf"\textstyle\sum = {diffs.sum():.0f}", font_size=30, color=OBS).next_to(A, DOWN, buff=0.2)
        ed = np.asarray(d["edges"])
        B = axes([-560, 560], [0, 1300], x_length=6.0, y_length=3.0, xlabel=r"$\sum \pm |d_i|$ \ over all $2^{15} = 32{,}768$ sign patterns",
                 xticks=[-500, -314, 0, 314, 500], center=[3.3, 0.9, 0], font_size=18)
        bx = B.ax
        h = np.asarray(d["hist"])
        hb = hist_bars(bx, ed, h, color=NULLC, opacity=0.6)
        hot = VGroup(*[hb[i] for i in range(len(h)) if ed[i] >= 314 - 10])
        mark = DashedLine(bx.c2p(314, 0), bx.c2p(314, 1300), color=OBS, stroke_width=2.5)
        g = np.random.Generator(np.random.PCG64(1935))
        rows = fit_rows(VGroup(
            label(r"under independent sign symmetry or a sharp null with randomized within-pair assignments: each sign can be flipped", font_size=24),
            MathTex(rf"\#\{{\text{{patterns with }} \textstyle\sum \ge 314\}} = {d['count']} \text{{ of }} {d['total']:,}".replace(",", "{,}"),
                    font_size=30, color=OBS),
            MathTex(rf"p_{{\text{{one-sided}}}} = {d['p_one']:.4f},\qquad p_{{\text{{two-sided}}}} = {d['p_two']:.4f}", font_size=30, color=OBS),
            MathTex(rf"\text{{Student's }} t = {d['t']:.2f}:\ \ p = {d['t_p']:.4f}", font_size=28, color=GREY_A),
            label(r"Fisher: \ the $t$-test is a good approximation to the test the randomization justifies", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.26, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's calculation uses sign-exchangeability under the null: for example, independent symmetric differences, or a sharp no-effect null with randomized assignments within pairs. Then within each pair, which "
            "plant ended up taller has nothing to do with how it was fertilized, and each difference was equally likely "
            "to come out positive or negative. So flip the signs. <bookmark mark='b'/> Here's one random flip; the sum "
            "changes. Here's another, and another. <bookmark mark='c'/> There are two to the fifteen, thirty-two "
            "thousand seven hundred and sixty-eight, sign patterns, all equally likely under the null. Compute the sum "
            "for every one of them, and that's the exact null distribution. <bookmark mark='d'/> The observed sum, three "
            "hundred and fourteen, is beaten or equalled by eight hundred and sixty-three of them: a one-sided p-value of "
            "two point six percent, and two-sided, five point three. Fisher counted them without a computer. "
            "<bookmark mark='e'/> Student's t-test, which assumes normality, gives point zero four nine seven, almost the "
            "same. Fisher's conclusion was that the t-test is justified as an approximation to the randomization test, "
            "in this dataset. Exact design-based validity needs the actual random assignment mechanism and a sharp null; a t approximation is not universally accurate for every data shape."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(bars), FadeIn(sum_t), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            for _ in range(3):
                sg = np.where(g.random(15) < 0.5, 1, -1)
                nv = sg * np.abs(diffs)
                self.play(Transform(bars, bar_set(nv)),
                          Transform(sum_t, MathTex(rf"\textstyle\sum = {nv.sum():.0f}", font_size=30, color=NULLC).move_to(sum_t)),
                          run_time=0.9)
                self.wait(0.4)
            vo.wait_until("c")
            self.play(FadeIn(hb, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("d")
            self.play(Transform(bars, bar_set(diffs)), Transform(sum_t, MathTex(rf"\textstyle\sum = 314", font_size=30, color=OBS).move_to(sum_t)),
                      Create(mark), hot.animate.set_fill(OBS, opacity=0.9))
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def machine(self):
        d = load("permute")
        vals = list(d["a"]) + list(d["b"])
        in_a = [True] * 7 + [False] * 7
        m = PermutationMachine(vals, in_a, colors=(S.TREAT, S.CTRL), center=[-3.0, 1.4, 0], width=5.4, radius=0.27, font_size=20)
        ga = label(r"region A", font_size=22, color=S.TREAT).next_to(m.slots_a[0], LEFT, buff=0.45)
        gb = label(r"region B", font_size=22, color=S.CTRL).next_to(m.slots_b[0], LEFT, buff=0.45)
        st = MathTex(rf"\bar x_A - \bar x_B = {d['obs']:.2f}", font_size=30, color=OBS).move_to([-3.0, -0.1, 0])
        ed = np.asarray(d["edges"])
        B = axes([-12.5, 12.5], [0, 0.11], x_length=5.8, y_length=3.0, xlabel=r"$\bar x_A - \bar x_B$ (cm) \ over all 3{,}432 splits",
                 xticks=[-10, -5, 0, 5, 10], center=[3.6, 1.1, 0], font_size=18)
        bx = B.ax
        hist = np.asarray(d["hist"]) / d["n_splits"]
        hb = hist_bars(bx, ed, hist, color=NULLC, opacity=0.55)
        obs_l = m.mark(bx, d["obs"], color=OBS)
        neg_l = m.mark(bx, -d["obs"], color=OBS)
        rows = fit_rows(VGroup(
            label(r"7 men from each of two of the World's regions: \ do their heights differ?", font_size=24),
            MathTex(rf"p = \frac{{{d['extreme']:,}}}{{3{{,}}432}} = {d['p']:.3f}".replace(",", "{,}", 1), font_size=30, color=OBS),
            label(rf"source-pool means: {d['truth']['a']:.1f} and {d['truth']['b']:.1f} cm; matching means do not establish exchangeability", font_size=24,
                  color=EXACT),
            label(r"Built: \ the permutation machine; \ \texttt{statkit.tests.permutation\_test}", font_size=22, color=GREY_A),
        ), 12.6, 0.28, [0, -2.3, 0])
        tag = simulated_tag(r"the World: \ heights in cm", corner=UR)
        with self.voiceover(
            "The same idea works for two separate groups, and here it is as a machine. <bookmark mark='a'/> Seven men "
            "from each of two of the World's regions, their heights rounded to the centimetre. Region A's average is two "
            "point seven centimetres below region B's. Is that a real difference? <bookmark mark='b'/> If the region "
            "makes no difference, the labels are arbitrary: any seven of these fourteen men could have been called A. "
            "So shuffle the labels. Deal the tokens into new seats, and recompute the difference. Again. And again. "
            "Each shuffle drops one dot onto the null distribution. <bookmark mark='c'/> There are three thousand four "
            "hundred and thirty-two ways to split fourteen into two sevens, so we can do them all. "
            "<bookmark mark='d'/> Our observed difference sits in the middle of the pile: more than half the splits are "
            "at least as extreme, so the p-value is point five six. No evidence of a difference. "
            "<bookmark mark='e'/> And the World knows the truth: the two regions' men average the same, to a tenth of a "
            "centimetre. Similar means do not establish identical distributions or prove the permutation null. This result fails to reject exchangeability; it does not establish it."
        ) as vo:
            self.play(FadeIn(m), FadeIn(ga), FadeIn(gb), FadeIn(st), FadeIn(B), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            dots = VGroup()
            for perm in d["shuffles"]:
                self.play(m.shuffle(perm, run_time=0.9))
                a, b = m.groups()
                s_ = float(a.mean() - b.mean())
                dot = m.drop(bx, s_, 1.0, radius=0.06, color=S.ALT)
                self.play(Transform(st, MathTex(rf"\bar x_A - \bar x_B = {s_:.2f}", font_size=30, color=S.ALT).move_to(st)), FadeIn(dot),
                          run_time=0.5)
                dots.add(dot)
            vo.wait_until("c")
            self.play(m.reset(), FadeOut(dots), FadeIn(hb, lag_ratio=0.02),
                      Transform(st, MathTex(rf"\bar x_A - \bar x_B = {d['obs']:.2f}", font_size=30, color=OBS).move_to(st)), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(obs_l), Create(neg_l), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def why_random(self):
        rows = fit_rows(VGroup(
            label(r"where the null distribution comes from", font_size=32, color=OBS),
            label(r"in a properly randomized experiment: the sharp no-effect null supplies the randomization distribution",
                  font_size=24),
            label(r"no normality model needed; the assignment mechanism, sharp null and no-interference assumptions still matter",
                  font_size=24),
            label(r"in the World's regions, \ nobody randomized: \ exchangeability under $H_0$ is an assumption", font_size=24,
                  color=GREY_A),
            label(r"randomization inference: \ Parts 13 and 35; \ permutation tests and ranks: \ Part 16", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        intro = label('Randomization and exchangeability are different justifications', font_size=36)
        with self.voiceover(
            "There's a deep point here about where null distributions come from. <bookmark mark='a'/> <bookmark mark='b'/> "
            "In the tea test and in a properly designed experiment, the experimenter randomized: for example, the order of the tea cups. For Darwin's historical data, do not assume an undocumented random assignment mechanism; the sign-flip calculation can instead be read under a symmetry model. Then the null distribution isn't a model at all. It's the "
            "randomization itself, which we know exactly because we did it. <bookmark mark='c'/> No assumption of "
            "normality, no model for the data: the test is valid by design. That was Fisher's great insight, and it's "
            "why he insisted on randomization. <bookmark mark='d'/> In the World's regions, nobody randomized which man "
            "lives where, so treating the labels as exchangeable under the null is an assumption about the world. "
            "<bookmark mark='e'/> Randomization inference returns with designed experiments in Part 13 and causal "
            "inference in Part 35, and permutation and rank tests in Part 16."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
