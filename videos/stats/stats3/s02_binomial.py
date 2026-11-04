from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Binomial(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.paths()
        self.formula()
        self.moments()
        self.poll()
        self.tree_voiceover("So the first arrow of the family tree: <bookmark mark='t'/> add up n independent "
                            "Bernoulli trials, and you get a binomial.", 1)

    def card(self):
        card = chapter_card(1, r"Bernoulli to binomial", r"Count the successes in $n$ independent trials",
                            lit=(1713,), part=PART)
        with self.voiceover("Chapter one. Bernoulli to binomial."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def paths(self):
        d = load("binomial")
        n, p = d["n"], d["p"]
        steps = np.asarray(d["paths"])
        dx, dy = 0.68, 0.48
        origin = np.array([-6.3, -3.0, 0])

        def pt(i, k):
            return origin + np.array([i * dx, k * dy, 0])

        lattice = VGroup()
        for i in range(n + 1):
            for k in range(i + 1):
                lattice.add(Dot(pt(i, k), radius=0.025, color=GREY_D))
        paths = VGroup()
        for s in steps[:24]:
            k = np.concatenate([[0], np.cumsum(s)])
            paths.add(VMobject(stroke_color=SIM, stroke_width=2, stroke_opacity=0.5).set_points_as_corners(
                [pt(i, kk) for i, kk in enumerate(k)]))
        xlab = label(r"trial", font_size=22, color=GREY_B).next_to(pt(n, 0), DOWN, buff=0.25).shift(LEFT * 2.5)
        ylab = label(r"successes so far", font_size=22, color=GREY_B).rotate(PI / 2).next_to(lattice, LEFT, buff=0.2)
        ends = np.asarray(d["ends"])
        cnt = np.bincount(ends, minlength=n + 1)
        stacks = VGroup()
        for k in range(n + 1):
            for j in range(cnt[k]):
                stacks.add(Dot(pt(n, k) + RIGHT * (0.35 + 0.16 * j), radius=0.055, color=SIM))
        dfn = definition_card(r"Bernoulli trial", r"one trial, success with probability $p$: \ $X \in \{0, 1\}$; \ "
                              r"named for Jacob Bernoulli, \emph{Ars Conjectandi} (1713)", color=DISC, width=5.6,
                              font_size=23).move_to([3.6, 2.4, 0])
        with self.voiceover(
            "The simplest random variable is a single trial that succeeds or fails: one if it succeeds, with "
            "probability p, zero if not. <bookmark mark='a'/> It's named for Jacob Bernoulli, whose book on "
            "probability appeared in 1713. <bookmark mark='b'/> Now repeat it, n times, independently, and count the "
            "successes. Draw each repetition as a path: one step right per trial, and one step up for each success. "
            f"Here n is ten and p is {p}. <bookmark mark='c'/> Each path ends at its number of successes, "
            "<bookmark mark='d'/> and piling up the endpoints of many paths builds the distribution of the count."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(FadeIn(lattice), FadeIn(xlab), FadeIn(ylab))
            self.play(Create(paths[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(pp) for pp in paths[1:]], lag_ratio=0.1), run_time=4.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in stacks], lag_ratio=0.03), run_time=2.0)
        self.clear_scene()

    def formula(self):
        d = load("binomial")
        n, p = d["n"], d["p"]
        rows = [
            cmath(r"P(\text{one given path with } k \text{ ups})", r"=", r"p^k (1-p)^{n-k}", font_size=34),
            cmath(r"P(X = k)", r"=", r"\binom{n}{k} p^k (1-p)^{n-k}", font_size=40),
        ]
        rows[1][0].set_color(DISC)
        whys = [why(r"independent trials multiply"), why(r"$\binom nk$ paths end at $k$: \ Part 2's counting")]
        A = axes([-0.6, 10.6], [0, 0.3], x_length=6.0, y_length=3.0, xlabel=r"$k$", xticks=list(range(0, 11)),
                 yticks=[0, 0.1, 0.2, 0.3], center=[-1.8, -2.0, 0])
        bars = pmf_bars(A.ax, range(n + 1), d["pmf"], DISC, width=0.6)
        eng = code_block(["coin(0.3).iid_sum(10).P(3)   # exact"], font_size=20).next_to(A, RIGHT, buff=0.6)
        with self.voiceover(
            "The formula is two ideas from Part 2. <bookmark mark='a'/> Any one path with k up-steps has "
            "probability p to the k times one minus p to the n minus k, because the trials are independent. "
            "<bookmark mark='b'/> And the number of such paths is n choose k: choose which of the n trials succeed. "
            "Multiply, and you have the binomial distribution. <bookmark mark='c'/> For ten trials with p equal to "
            "zero point three, it peaks at three, and the engine computes it exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.6, x=0.6, buff=0.55)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(eng))
        self.clear_scene()

    def moments(self):
        d = load("binomial")
        rows = [
            cmath(r"X", r"=", r"X_1 + X_2 + \cdots + X_n", font_size=38),
            cmath(r"E X", r"=", r"n\, E X_1", r"=", r"np", font_size=40),
            cmath(r"\mathrm{Var}\, X", r"=", r"n\, \mathrm{Var}\, X_1", r"=", r"np(1-p)", font_size=40),
        ]
        whys = [why(r"indicators of success"), why(r"linearity: \ $E X_1 = p$"),
                why(r"independence: \ $\mathrm{Var}\, X_1 = p - p^2$")]
        chk = MathTex(rf"n = 10,\ p = 0.3:\quad np = {d['E']:.1f},\ \ np(1-p) = {d['Var']:.1f}", font_size=30,
                      color=EXACT).to_edge(DOWN, buff=1.2)
        sim = MathTex(rf"\text{{simulated, 20{{,}}000 runs:}}\ \ {d['sim_mean']:.3f},\ \ {d['sim_var']:.3f}",
                      font_size=28, color=SIM).next_to(chk, DOWN, buff=0.2)
        with self.voiceover(
            "The mean and variance need no sums over the formula at all. <bookmark mark='a'/> Write the count as a "
            "sum of the n trials' indicators. <bookmark mark='b'/> By linearity, the expectation is n times p. "
            "<bookmark mark='c'/> By independence, the variances add, and each trial has variance p minus p "
            "squared, so the variance is n p times one minus p. <bookmark mark='d'/> For our example, three and two "
            "point one, and twenty thousand simulated runs agree."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.55)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(chk), FadeIn(sim))
        self.clear_scene()

    def poll(self):
        d = load("binomial")
        k = np.asarray(d["poll_k"])
        A = axes([-0.6, 35.6], [0, 0.14], x_length=8.2, y_length=4.2, xlabel=r"adults over 180 cm, \ in a poll of 100",
                 xticks=[0, 5, 10, 15, 20, 25, 30, 35], yticks=[0, 0.05, 0.1], center=[-1.8, -0.5, 0])
        ax = A.ax
        bars = pmf_bars(ax, k[:36], np.asarray(d["poll_emp"])[:36], SIM, width=0.65)
        dots = pmf_dots(ax, k[:36], np.asarray(d["poll_pmf"])[:36], EXACT, radius=0.06)
        p = d["p180"]
        info = VGroup(MathTex(rf"p = P(\text{{height}} > 180) = {p:.4f}", font_size=28, color=S.TRUTH),
                      MathTex(rf"\text{{binomial}}(100, p):\ \ np = {100 * p:.2f},\ \ np(1-p) = {100 * p * (1 - p):.2f}",
                              font_size=24, color=EXACT),
                      MathTex(rf"\text{{2{{,}}000 polls: mean }} {d['poll_mean']:.2f},\ \text{{variance }} {d['poll_var']:.2f}",
                              font_size=24, color=SIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        info.move_to([3.6, 2.6, 0])
        wr = label(r"sampled without replacement from $741{,}311$: \ chapter 4 explains why it is still binomial",
                   font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        tag = simulated_tag(corner=UL)
        with self.voiceover(
            "Binomials are everywhere in statistics because every yes-or-no question asked of a random sample is one. "
            "<bookmark mark='a'/> In the World, the share of adults taller than a hundred and eighty centimetres is "
            f"a parameter: {p:.4f}. <bookmark mark='b'/> Poll a hundred adults at random and count the tall ones. "
            "<bookmark mark='c'/> Two thousand polls, blue, against the binomial with n a hundred and that p, gold. "
            f"They agree, mean about {100 * p:.1f} and variance about {100 * p * (1 - p):.1f}. "
            "<bookmark mark='d'/> Strictly, a poll samples without replacement, so the count isn't exactly binomial; "
            "chapter four shows why, from a population this large, the difference vanishes. The spread of this "
            "count is the margin of error of every opinion poll, and Part 8 builds it into an interval."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(info[0]))
            vo.wait_until("b")
            self.play(FadeIn(A))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(dots), FadeIn(info[1:]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(wr))
        self.clear_scene()
