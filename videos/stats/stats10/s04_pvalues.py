from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class PValues(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.uniform_proof()
        self.histograms()
        self.discrete()
        self.surprise()

    def card(self):
        card = chapter_card(3, r"The $p$-value", r"What is its distribution?", part=PART)
        with self.voiceover("Chapter three. The p-value."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        dc = definition_card(r"$p$-value", r"For a statistic $T$ with null distribution function $F_0$, \ the $p$-value of data $x$ is \ "
                             r"$p(x) = P_{H_0}\big(T \ge T(x)\big) = 1 - F_0\big(T(x)^-\big)$. \ "
                             r"Before the data are seen, \ $p(X)$ is a random variable.", color=OBS, width=10.0, font_size=26).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            label(r"a function of the data, \ like any statistic: \ it has a sampling distribution", font_size=26),
            label(r"its distribution under $H_0$ is what makes ``$p < 0.05$'' mean ``1 in 20''", font_size=26, color=OBS),
        ), 12.6, 0.34, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Formally, the p-value is the probability, under the null, of a statistic at least as "
            "large as the one observed. As a function of the data, it's a statistic like any other. Before the data "
            "are collected, it's a random variable. <bookmark mark='b'/> So it has a sampling distribution, and we can "
            "ask what it is. <bookmark mark='c'/> That distribution is what gives the phrase p less than point zero "
            "five its meaning."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def uniform_proof(self):
        rows = [
            cmath(r"P_{H_0}\big(p(X) \le u\big)", r"=", r"P_{H_0}\big(1 - F_0(T) \le u\big)", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"P_{H_0}\big(F_0(T) \ge 1 - u\big)", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"1 - (1 - u) = u", font_size=34),
            cmath(r"p(X)", r"\sim", r"\mathrm{Uniform}(0, 1) \text{ under } H_0", font_size=36),
        ]
        rows[0][0].set_color(OBS)
        rows[3][2].set_color(OBS)
        whys = [why(r"continuous $T$"), why(r"rearrange"), why(r"$F_0(T) \sim$ Uniform: \ the probability integral transform (Parts 3, 7)"),
                why(r"so $P(p \le 0.05) = 0.05$: \ the size of the test")]
        with self.voiceover(
            "Here's the key fact. <bookmark mark='a'/> If the null is true and the statistic is continuous, the "
            "chance that the p-value is at most u is the chance that one minus F of T is at most u, <bookmark mark='b'/> "
            "that is, that F of T is at least one minus u. <bookmark mark='c'/> But F of T, a continuous random variable "
            "pushed through its own distribution function, is uniform: the probability integral transform, from Part 3, "
            "which Part 7 used to generate random numbers. So the chance is u. <bookmark mark='d'/> Under the null, the "
            "p-value is uniformly distributed between zero and one. Every value is equally likely. That's why rejecting "
            "when p is below point zero five makes a mistake exactly five percent of the time when the null is true."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def histograms(self):
        d = load("pvalues")
        ed = np.asarray(d["edges"])
        panels = VGroup()
        specs = (("0.0", r"$H_0$ true: \ $\delta = 0$", NULLC), ("0.3", r"$\delta = 0.3\sigma$", ALTC), ("0.8", r"$\delta = 0.8\sigma$", ALTC))
        for j, (k, t, c) in enumerate(specs):
            ymax = 6.0 if k != "0.0" else 1.6
            A = axes([0, 1], [0, ymax], x_length=3.6, y_length=3.0, xlabel=r"$p$", xticks=[0, 0.5, 1], center=[-4.4 + 4.4 * j, 0.6, 0],
                     font_size=18)
            ax = A.ax
            h = np.minimum(np.asarray(d[k]["hist"]), ymax)
            bars = hist_bars(ax, ed, h, color=c, opacity=0.7)
            ttl = label(t, font_size=24, color=c).next_to(A, UP, buff=0.15)
            num = MathTex(rf"P(p < 0.05) = {d[k]['below05']:.3f}", font_size=26, color=OBS).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, bars, ttl, num))
        foot = fit_rows(VGroup(
            label(r"one-sample $t$-tests, \ $n = 15$, \ 20,000 each", font_size=22, color=GREY_A),
            label(r"under $H_0$, \ flat; \ under an alternative, \ piled toward 0: \ the pile below 0.05 is the \emph{power}", font_size=26,
                  color=OBS),
        ), 12.6, 0.3, [0, -2.7, 0])
        tag = simulated_tag(r"simulated", corner=UR)
        with self.voiceover(
            "Let's see it. <bookmark mark='a'/> Twenty thousand t-tests on samples of fifteen, with the null true. The "
            "p-values are flat across zero to one, and four point nine percent of them fall below point zero five. "
            "<bookmark mark='b'/> Now let the true mean be point three standard deviations away from the null. The "
            "p-values pile up toward zero, but only about one in five falls below point zero five. "
            "<bookmark mark='c'/> At point eight standard deviations, the pile is a spike near zero, and eighty-two "
            "percent fall below point zero five. <bookmark mark='d'/> The share of p-values below the line is the "
            "test's power: its chance of detecting a real effect. Under the null, the p-value is a uniform random number; "
            "under an alternative, it's a random number that tends to be small. Either way, it's random, which will "
            "matter a great deal in chapter eleven."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(p[0]) for p in panels])
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(panels[k][1], lag_ratio=0.03), FadeIn(panels[k][2]), FadeIn(panels[k][3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def discrete(self):
        ps = [1 / 70, 17 / 70, 53 / 70, 69 / 70, 1.0]
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xlabel=r"$u$", ylabel=r"$P_{H_0}(p \le u)$", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 0.5, 1], center=[-3.0, -0.2, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        probs = [1 / 70, 16 / 70, 36 / 70, 16 / 70, 1 / 70]
        cum = np.cumsum(probs)
        pts = [ax.c2p(0, 0)]
        prev = 0.0
        for pv, c in zip(ps, cum):
            pts += [ax.c2p(pv, prev), ax.c2p(pv, c)]
            prev = c
        pts.append(ax.c2p(1, 1))
        stair = VMobject(stroke_color=OBS, stroke_width=4).set_points_as_corners(pts)
        rows = fit_rows(VGroup(
            label(r"the tea: \ only five $p$-values are possible", font_size=26),
            MathTex(r"\tfrac1{70},\ \tfrac{17}{70},\ \tfrac{53}{70},\ \tfrac{69}{70},\ 1", font_size=32, color=OBS),
            MathTex(r"P_{H_0}(p \le u) \le u", font_size=32),
            label(r"a discrete $p$-value is \emph{super-uniform}: \ a test at $\alpha = 0.05$ really has size $\tfrac1{70}$", font_size=24,
                  color=GREY_A),
            label(r"valid, \ but conservative: \ it rejects less often than promised", font_size=24, color=GREY_A),
        ), 6.4, 0.34, [3.3, -0.2, 0])
        with self.voiceover(
            "With a discrete statistic, the story changes slightly. <bookmark mark='a'/> In the tea test, only five "
            "p-values are possible: one in seventy, seventeen in seventy, fifty-three in seventy, sixty-nine in "
            "seventy, and one. <bookmark mark='b'/> Their distribution function is a staircase, and it never rises above "
            "the diagonal. The chance of a p-value at most u is at most u. Such p-values are called super-uniform. "
            "<bookmark mark='c'/> So a test that rejects when p is below point zero five really rejects only one time "
            "in seventy under the null. It's valid, since it never rejects more often than promised, but conservative. "
            "Part 11 will meet the same effect in intervals for proportions."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(stair), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def surprise(self):
        d = load("arbuthnot")
        items = [(r"$p = 0.5$", 1.0), (r"$p = 0.05$", -np.log2(0.05)), (r"the tea, \ $p = 1/70$", np.log2(70)),
                 (r"Darwin, \ $p = 0.053$", -np.log2(0.0527)), (r"$p = 0.005$", -np.log2(0.005))]
        rows = VGroup()
        for t, s_ in items:
            coins = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=OBS, fill_opacity=0.9) for _ in range(int(round(s_)))]).arrange(RIGHT, buff=0.06)
            rows.add(VGroup(label(t, font_size=26), MathTex(rf"{s_:.1f}", font_size=30, color=OBS), coins))
        for r in rows:
            r[0].move_to([-4.6, 0, 0])
            r[1].move_to([-1.6, 0, 0])
            r[2].next_to([-0.9, 0, 0], RIGHT, buff=0)
        rows.arrange(DOWN, buff=0.38).move_to([0, 0.3, 0])
        for r in rows:
            r[0].set_x(-4.6)
            r[1].set_x(-1.6)
            r[2].align_to([-0.9, 0, 0], LEFT)
        head = VGroup(MathTex(r"s = -\log_2 p", font_size=36, color=OBS),
                      label(r"the surprise in bits: \ as surprising as $s$ fair coins all landing heads", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        foot = label(r"Arbuthnot: \ $s = 82$ \ \ (Greenland 2019 calls it the $S$-value)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How surprising is a given p-value? A helpful translation, popularized by Sander Greenland, turns it into "
            "coin flips. <bookmark mark='a'/> Minus the log, base two, of p, measures the surprise in bits: a p-value "
            "of p is as surprising as that many fair coins all landing heads. <bookmark mark='b'/> A p-value of one "
            "half is one coin. Point zero five is four point three coins: about as surprising as four heads in a row, "
            "which is not very. The perfect tea score is six coins; Darwin's maize, a little over four. Point zero zero "
            "five is seven and a half. <bookmark mark='c'/> And Arbuthnot's eighty-two years are, of course, eighty-two "
            "coins. Thinking in coins is a useful antidote to treating point zero five as proof."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.4), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
