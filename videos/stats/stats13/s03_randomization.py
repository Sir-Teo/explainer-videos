from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Randomization(VoiceoverScene):
    def construct(self):
        self.card()
        self.sharp_null()
        self.trial()
        self.exact()
        self.balance()
        self.doctor()
        self.why_t()

    def card(self):
        card = chapter_card(2, r"Randomization as inference", r"The coin that made the layout is the probability model",
                            lit=(1935,), part=PART)
        with self.voiceover("Chapter two. Randomization as inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sharp_null(self):
        rows = [
            cmath(r"y_i(A),\ y_i(B)", r":", r"\text{plot } i\text{'s yield under each variety}", font_size=32),
            cmath(r"\text{we see}", r":", r"y_i = y_i(B)\ \text{if } i \text{ got B, else } y_i(A)", font_size=32),
            cmath(r"H_0", r":", r"y_i(A) = y_i(B)\ \text{ for every plot } i", font_size=34),
            cmath(r"\text{under } H_0", r":", r"\text{the 20 yields are fixed; \ only the labels were random}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"two potential yields: \ Neyman (1923)"), why(r"one of them, \ chosen by the randomization"),
                why(r"Fisher's sharp null: \ the variety does nothing, \ anywhere"),
                why(r"so every other labelling was equally likely to have happened")]
        with self.voiceover(
            "Fisher's argument needs no model of the soil at all. <bookmark mark='a'/> Each plot has two potential yields: what "
            "it would give with variety A, and what it would give with B. Jerzy Neyman wrote experiments this way in 1923. "
            "<bookmark mark='b'/> We see only one of the two, the one the randomization chose. <bookmark mark='c'/> Now "
            "suppose the variety does nothing whatever, on any plot: each plot's two potential yields are equal. That's "
            "Fisher's sharp null hypothesis, sharper than a statement about averages. <bookmark mark='d'/> If it's true, the "
            "twenty yields we harvested would have been exactly the same under any other labelling. The yields are fixed "
            "numbers; the only randomness is in which labels went where, and we chose those labels ourselves, by lot."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trial(self):
        d = load("randinf")
        y = np.asarray(d["y"])
        alloc = np.asarray(d["alloc"])
        fp = field_from(y, cell=0.75, center=[-3.6, 0.3, 0], lo=y.min() - 1, hi=y.max() + 1)
        letters = VGroup()
        for r in range(4):
            for c in range(5):
                k = int(alloc[r, c])
                t = VGroup(label("AB"[k], font_size=22, color=[S.CTRL, S.TREAT][k]),
                           label(rf"{y[r, c]:.1f}", font_size=17, color=WHITE)).arrange(DOWN, buff=0.04)
                letters.add(t.move_to(fp.cells[r][c]))
        ya, yb = y[alloc == 0], y[alloc == 1]
        rows = fit_rows(VGroup(
            label(r"a small trial: \ 20 plots, \ 10 of each variety, \ by lot", font_size=24),
            MathTex(rf"\bar y_B = {yb.mean():.2f},\quad \bar y_A = {ya.mean():.2f}", font_size=30),
            MathTex(rf"\text{{observed difference}}\ = {d['obs']:.2f}", font_size=32, color=OBS),
            label(r"could a meaningless labelling have produced a difference this large?", font_size=24),
            label(r"count the labellings", font_size=26, color=OBS),
        ), 5.4, 0.34, [3.6, 0.2, 0])
        with self.voiceover(
            "A small trial. <bookmark mark='a'/> Twenty plots on a corner of the field, ten given variety B by lot, ten given "
            "A. <bookmark mark='b'/> B's plots average fifty-three point five, A's fifty point eight: <bookmark mark='c'/> "
            "an observed difference of two point seven one bushels. <bookmark mark='d'/> If the variety did nothing, these same "
            "twenty numbers, split by some other labelling, could have shown any of a range of differences. How unusual is "
            "ours among them? <bookmark mark='e'/> We don't need a formula. We can count."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.02))
            vo.wait_until("a")
            self.play(FadeIn(letters, lag_ratio=0.03), FadeIn(rows[0]), run_time=1.5)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.clear_scene()

    def exact(self):
        d = load("randinf")
        y = np.asarray(d["y"]).ravel()
        treat = np.asarray(d["alloc"]).ravel() == 1
        pm = PermutationMachine(y, treat, colors=(S.TREAT, S.CTRL), center=[0, 2.55, 0], width=11.0, radius=0.24, font_size=15,
                                fmt="{:.1f}", row_gap=0.75)
        A = axes([-5, 5], [0, 9000], x_length=8.4, y_length=3.2, xlabel=r"difference under a random relabelling",
                 ylabel=r"labellings", xticks=[-4, -2, 0, 2, 4], yticks=[0, 4000, 8000], center=[-0.6, -1.4, 0],
                 yfmt=lambda v: f"{int(v):,}")
        ax = A.ax
        edges = np.asarray(d["edges"])
        hist = np.asarray(d["hist"])
        keep = (edges[:-1] >= -5) & (edges[1:] <= 5)
        e2 = edges[:-1][keep]
        w = edges[1] - edges[0]
        bars = VGroup()
        for e, h in zip(e2, hist[keep]):
            c = OBS if abs(e + w / 2) >= abs(d["obs"]) else NULLC
            bars.add(*hist_bars(ax, [e, e + w], [h], color=c, opacity=0.85))
        mk = pm.mark(ax, d["obs"], color=OBS, height=8600)
        mk2 = pm.mark(ax, -d["obs"], color=OBS, height=8600)
        rows = fit_rows(VGroup(
            MathTex(rf"\binom{{20}}{{10}} = {d['n_alloc']:,}\ \text{{labellings, all equally likely}}", font_size=26),
            MathTex(rf"{d['count']:,}\ \text{{of them as extreme:}}\ \ p = {d['p_exact']:.3f}", font_size=28, color=OBS),
            MathTex(rf"\text{{Student's }} t = {d['t']:.2f}:\ \ p = {d['p_t']:.3f}", font_size=26, color=S.LIK),
        ), 3.8, 0.3, [5.1, -1.0, 0])
        g = np.random.Generator(np.random.PCG64(5))
        with self.voiceover(
            "<bookmark mark='a'/> Here are the twenty yields as tokens, B's on top. Shuffle the labels, and recompute the "
            "difference. <bookmark mark='b'/> Shuffle again, and again. Each shuffle is a labelling the randomization could "
            "just as well have produced. <bookmark mark='c'/> There are twenty choose ten, a hundred and eighty-four thousand "
            "seven hundred and fifty-six, ways to choose ten plots out of twenty, all equally likely. A computer can try every "
            "one. Here's the exact distribution of the difference under the sharp null: the randomization distribution. "
            "<bookmark mark='d'/> Six thousand three hundred and twenty-two labellings give a difference at least as large as "
            "ours, in either direction: a p-value of point zero three four, exact, with no assumption about the soil, normal "
            "or otherwise. <bookmark mark='e'/> Student's t-test, which assumes normal errors, gives point zero three one. "
            "Fisher noticed this agreement in 1935, and argued that the t-test is best thought of as an approximation to the "
            "randomization test, whose validity comes from the coin."
        ) as vo:
            self.play(FadeIn(pm), FadeIn(A))
            vo.wait_until("a")
            for _ in range(2):
                self.play(pm.shuffle(g.permutation(20), run_time=0.9))
            vo.wait_until("b")
            for _ in range(3):
                self.play(pm.shuffle(g.permutation(20), run_time=0.6))
            self.play(pm.reset(run_time=0.6))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(mk), Create(mk2), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def balance(self):
        d = load("balance")
        dh = np.asarray(d["dh"])
        di = np.asarray(d["di"]) / 1000
        A1 = axes([-5, 5], [0, 260], x_length=5.4, y_length=3.0, xlabel=r"difference in mean height, \ cm", ylabel=r"",
                  xticks=[-4, -2, 0, 2, 4], yticks=[0, 100, 200], center=[-3.4, 0.2, 0])
        A2 = axes([-15, 15], [0, 260], x_length=5.4, y_length=3.0, xlabel=r"difference in mean income, \ thousands", ylabel=r"",
                  xticks=[-10, 0, 10], yticks=[0, 100, 200], center=[3.4, 0.2, 0])
        e1 = np.linspace(-5, 5, 41)
        e2 = np.linspace(-15, 15, 41)
        b1 = hist_bars(A1.ax, e1, np.histogram(dh, e1)[0], color=S.WORLD, opacity=0.8)
        b2 = hist_bars(A2.ax, e2, np.histogram(di, e2)[0], color=S.WORLD, opacity=0.8)
        rows = fit_rows(VGroup(
            label(r"200 of the World's adults, \ split 100 / 100 by lot, \ 5,000 times", font_size=24),
            MathTex(rf"\text{{SD of the height gap}}\ {d['sd_h']:.2f}\ \text{{cm;\ \ income gap}}\ {d['sd_i'] / 1000:.1f}\ \text{{thousand}}", font_size=26),
            label(rf"beyond two SDs: \ {100 * d['big_h']:.1f}\% of splits, \ as chance says", font_size=24, color=OBS),
            label(r"nobody measured these: \ randomization balances every variable at once, \ on average", font_size=24, color=OBS),
        ), 12.4, 0.26, [0, -2.55, 0])
        tag = simulated_tag(r"the World: \ 200 adults", corner=UR)
        with self.voiceover(
            "Randomization's other gift is balance, on variables nobody measured. <bookmark mark='a'/> Take two hundred of the "
            "World's adults, and split them a hundred and a hundred by lot, five thousand times, as if for a trial. "
            "<bookmark mark='b'/> The two groups' mean heights differ by a centimetre or so, with a standard deviation of one "
            "point three; their mean incomes differ by a few thousand. <bookmark mark='c'/> Splits more than two standard "
            "deviations apart occur four point eight percent of the time: exactly the rate chance predicts, so the test's "
            "p-value already accounts for them. <bookmark mark='d'/> We never told the randomizer about height or income. "
            "It balances them anyway, along with blood pressure, diet, genes and everything else, not perfectly in any one "
            "split, but in a way whose imperfection is known."
        ) as vo:
            self.play(FadeIn(A1), FadeIn(A2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.02), FadeIn(rows[1]), run_time=2.5)
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def doctor(self):
        d = load("balance")
        h = np.asarray(d["h"])
        srt = np.sort(h)
        A = axes([140, 205], [0, 1], x_length=10.0, y_length=1.2, xlabel=r"height, \ cm", ylabel=r"", xticks=[150, 160, 170, 180, 190, 200],
                 yticks=[], center=[0, 0.6, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(3))
        jit = g.uniform(0.15, 0.85, len(h))
        dots = VGroup(*[Dot(ax.c2p(v, j), radius=0.05, color=S.TREAT if v >= srt[100] else S.CTRL) for v, j in zip(h, jit)])
        rows = fit_rows(VGroup(
            label(r"now let a well-meaning doctor choose: \ the treatment to the 100 tallest, \ ``who look strongest''", font_size=24),
            MathTex(rf"\text{{height gap}}\ = {d['chosen_h']:.1f}\ \text{{cm}} \ =\ {d['chosen_h'] / d['sd_h']:.0f}\ \text{{SDs of the random gap}}", font_size=28, color=RES),
            label(r"anything related to height, \ or to the doctor's judgement, \ now rides along with the treatment", font_size=24),
            label(r"the selection need not be conscious: \ only a coin is guaranteed to know nothing", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "Compare a human allocator. <bookmark mark='a'/> Suppose a well-meaning doctor gives the treatment to the hundred "
            "patients who look strongest, and suppose that means the tallest. <bookmark mark='b'/> The groups now differ in "
            "height by sixteen centimetres, twelve standard deviations of the random gap. <bookmark mark='c'/> Anything related "
            "to height, or to whatever the doctor was judging, now travels with the treatment, and the trial will credit the "
            "treatment for it. <bookmark mark='d'/> The selection needn't be conscious, or even about anything the doctor could "
            "name. Only a random device is guaranteed to know nothing about the patients."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots, lag_ratio=0.003), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.clear_scene()

    def why_t(self):
        rows = [
            cmath(r"p_{\text{rand}}", r"=", r"\frac{\#\{\text{labellings with } |\Delta| \ge |\Delta_{\text{obs}}|\}}{\binom{n}{n/2}}", font_size=34),
            cmath(r"\text{large } n", r":", r"\text{the randomization distribution of } t \approx t_{n-2}", font_size=32),
            cmath(r"\text{so}", r":", r"p_t \approx p_{\text{rand}}\ \text{ without normal errors}", font_size=32),
            cmath(r"\text{too many labellings}", r":", r"\text{sample 10{,}000 of them (Part 10)}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"exact: \ the only probability is the experimenter's coin"),
                why(r"Eden \& Yates (1933), \ Pitman (1937), \ Welch (1937)"), why(r"the design justifies the familiar test"),
                why(r"a Monte Carlo $p$-value, \ with its own small error")]
        with self.voiceover(
            "So the logic of a randomized experiment is self-contained. <bookmark mark='a'/> The p-value is a count: the "
            "share of possible labellings that give a difference at least as extreme as the one observed. The only "
            "probability in it is the experimenter's own coin. <bookmark mark='b'/> In the 1930s Eden and Yates checked it "
            "on real wheat data, and Pitman and Welch proved it: for moderate samples, the randomization distribution of "
            "the t statistic is close to Student's t distribution. <bookmark mark='c'/> So the familiar t-test and F-test "
            "are justified by the design, even when the errors aren't normal. <bookmark mark='d'/> When the labellings are "
            "too many to count, sample ten thousand of them at random, as in Part 10. On the Coverage Board, a randomization "
            "test on skewed data keeps its five percent promise, as we'll see at the end of this part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
