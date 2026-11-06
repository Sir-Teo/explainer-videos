from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.corps()
        self.table()
        self.fit()
        self.question()
        self.objectives()

    def corps(self):
        d = load("horsekick")
        tl = timeline(lit=(1898,)).to_edge(UP, buff=0.35)
        hc = history_card(1898, r"Ladislaus von Bortkiewicz, \ \emph{Das Gesetz der kleinen Zahlen}",
                          r"The Law of Small Numbers: \ rare events, counted, follow a law", color=S.MUSEUM, width=6.4,
                          font_size=24).move_to([-3.2, 0.6, 0])
        grid = VGroup()
        for c in range(10):
            row = VGroup(*[Square(side_length=0.24, stroke_color=GREY_D, stroke_width=1, fill_color="#121722",
                                  fill_opacity=1) for _ in range(20)]).arrange(RIGHT, buff=0.04)
            grid.add(row)
        grid.arrange(DOWN, buff=0.06).move_to([3.4, -0.4, 0])
        cl = label(r"10 cavalry corps", font_size=22, color=GREY_A).rotate(PI / 2).next_to(grid, LEFT, buff=0.15)
        yl = label(r"20 years, 1875--1894", font_size=22, color=GREY_A).next_to(grid, UP, buff=0.15)
        g = np.random.Generator(np.random.PCG64(7))
        counts = np.repeat(d["k"], d["n"])
        g.shuffle(counts)
        nums = VGroup()
        for i, c in enumerate(counts):
            r, col = divmod(i, 20)
            if c:
                nums.add(MathTex(str(c), font_size=18, color=S.RESID).move_to(grid[r][col]))
        tag = historical_tag(r"Bortkiewicz (1898), 200 corps-years; \ placement in the grid illustrative")
        with self.voiceover(
            "In 1898 a Russian-born statistician working in Germany, Ladislaus von Bortkiewicz, published a small "
            "book with a strange subject. <bookmark mark='a'/> For twenty years, 1875 to 1894, the Prussian army had "
            "recorded every cavalryman killed by the kick of a horse, corps by corps and year by year. "
            "<bookmark mark='b'/> Take ten of the corps: two hundred corps-years. <bookmark mark='c'/> In most of "
            f"them, nobody died. In some, one man. Rarely two, or three. Once, four. {d['deaths']} deaths in all, an "
            f"average of {d['lam']:.2f} per corps per year. Random misfortunes, as unpredictable as anything could "
            "be. And yet Bortkiewicz showed they follow a formula."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(cl), FadeIn(yl), FadeIn(tag), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n_, scale=1.5) for n_ in nums], lag_ratio=0.03), run_time=4.0)
        self.clear_scene()

    def table(self):
        d = load("horsekick")
        k, n = d["k"], d["n"]
        A = axes([-0.6, 4.6], [0, 120], x_length=7.4, y_length=4.6, xlabel=r"deaths in a corps-year",
                 ylabel=r"number of corps-years", xticks=[0, 1, 2, 3, 4], yticks=[0, 50, 100], center=[-1.8, -0.3, 0])
        ax = A.ax
        bars = pmf_bars(ax, k, n, DATA, width=0.6)
        vals = VGroup(*[MathTex(str(v), font_size=28, color=DATA).next_to(b, UP, buff=0.1) for v, b in zip(n, bars)])
        tag = historical_tag(r"Bortkiewicz (1898); \ Quine \& Seneta (1987)")
        with self.voiceover(
            "Here is his count. <bookmark mark='a'/> A hundred and nine corps-years with no deaths, sixty-five with "
            "one, twenty-two with two, three with three, and one with four. <bookmark mark='b'/> If deaths were "
            "rare and independent, each soldier on each day carrying a tiny chance, what shape should this be?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(vals))
        self.A, self.bars, self.vals, self.tag = A, bars, vals, tag

    def fit(self):
        d = load("horsekick")
        ax = self.A.ax
        k, exp_ = d["k"], d["expected"]
        dots = VGroup(*[Dot(ax.c2p(kk, e), radius=0.09, color=EXACT) for kk, e in zip(k, exp_)])
        f = MathTex(r"200 \times \frac{\lambda^k e^{-\lambda}}{k!}", r",\quad \lambda = 0.61", font_size=36,
                    color=EXACT).move_to([4.4, 2.2, 0])
        rows = VGroup()
        for kk, obs, e in zip(k, d["n"], exp_):
            lab = rf"{kk}" if kk < 4 else r"4+"
            rows.add(MathTex(rf"{lab}:\ \ {obs}\ \ \text{{vs}}\ \ {e:.1f}", font_size=28))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, -0.4, 0])
        hdr = label(r"observed \ vs \ Poisson", font_size=22, color=GREY_B).next_to(rows, UP, buff=0.2)
        vm = MathTex(rf"\text{{mean }} {d['lam']:.2f},\ \ \text{{variance }} {d['var']:.2f}", font_size=26,
                     color=GREY_A).next_to(rows, DOWN, buff=0.35)
        with self.voiceover(
            "Bortkiewicz's answer was a formula Siméon Denis Poisson had derived in 1837. <bookmark mark='a'/> The "
            "chance of k events is lambda to the k, times e to the minus lambda, over k factorial, with lambda the "
            "average rate, here zero point six one. <bookmark mark='b'/> Multiply by two hundred, and the formula "
            "predicts a hundred and eight point seven corps-years with no deaths, sixty-six point three with one, "
            "twenty point two with two, four point one with three, under one with four or more. "
            "<bookmark mark='c'/> Gold dots, the formula; the historical counts, the bars. They agree closely. The observed mean and sample variance both round to zero point six one. Equality of mean and variance is a property of a Poisson population, not a requirement that every finite sample matches exactly. A law, hidden inside two hundred tragedies."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.25), FadeIn(hdr),
                      LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(vm), Indicate(dots, color=EXACT, scale_factor=1.3))
        self.clear_scene()

    def question(self):
        ft = FamilyTree().scale(0.92)
        q = label(r"Why do the same few shapes keep appearing?", font_size=40, color=S.ACCENT).to_edge(UP, buff=0.3)
        intro = label('Why do these shapes recur?', font_size=36)
        with self.voiceover(
            "Bortkiewicz's horse kicks raise the question of this part. <bookmark mark='a'/> Why do the same few "
            "shapes keep appearing: the Poisson for rare events, the bell curve for measurements, the exponential "
            "for waiting times? <bookmark mark='b'/> The answer is that the distributions of probability are not a "
            "zoo but a family, and every member is related to the others by an operation: a sum, a limit, a "
            "transformation, a mixture. <bookmark mark='c'/> Here is the family tree, still dark. Each arrow is a "
            "derivation. By the end of this part, we'll have derived every one of them, and lit the whole tree."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(ft, lag_ratio=0.02), run_time=2.5)
            vo.wait_until("c")
            self.play(*ft.light_nodes(*FAMILY_NODES.keys()), run_time=2.0)
            self.play(*[n.animate.set_opacity(0.35) for n in ft.nodes.values()], run_time=1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 3", font_size=34, color=GREY_B), label(r"The Family of Distributions", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Bernoulli, binomial, \ and the law of rare events that makes the Poisson",
            r"waiting: \ geometric, negative binomial, exponential, gamma; \ the Poisson process and the inspection "
            r"paradox",
            r"sampling without replacement: \ the hypergeometric, \ and counting the fish in the World's lake",
            r"the normal, derived three ways; \ transformations and Jacobians; \ $\chi^2$, $t$, $F$ and Cauchy",
            r"order statistics, \ heavy tails, \ moment generating functions, \ mixtures, \ exponential families",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Part 2; \ calculus").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Part three: the family of distributions. <bookmark mark='a'/> In this part: the binomial and the law of "
            "rare events. Waiting times, and a paradox about buses. Sampling without replacement, and an estimate of "
            "the number of fish in the World's lake. The normal distribution, derived three different ways; "
            "transformations; the distributions that statistics itself creates, chi-squared, t and F; order "
            "statistics; heavy tails; generating functions; mixtures; and the exponential families that hold most "
            "of them together."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
        self.wait(1.0)
        self.clear_scene()
