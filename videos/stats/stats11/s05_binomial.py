from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Binomial(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.wilson()
        self.panels()
        self.wilson_saw()
        self.widths()
        self.world_case()
        self.advice()

    def card(self):
        card = chapter_card(4, r"The binomial family", r"Six intervals for a proportion", lit=(1927,), part=PART)
        with self.voiceover("Chapter four. The binomial family."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        cards = VGroup(
            history_card(1927, r"E. B. Wilson, \ \emph{JASA} 22", r"invert the score test: \ ``probable inference, \ the law of succession''",
                         color=METHOD_COL["wilson"], width=4.0, font_size=20),
            history_card(1934, r"C. Clopper \& E. S. Pearson", r"invert exact tests: \ never below 95\%", color=METHOD_COL["clopper_pearson"],
                         width=4.0, font_size=20),
            history_card(1998, r"A. Agresti \& B. Coull", r"``Approximate is better than `exact''': \ add two successes and two failures",
                         color=METHOD_COL["agresti_coull"], width=4.0, font_size=20),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.9, 0])
        foot = label(r"and Jeffreys' Bayesian interval, \ which Brown, Cai \& DasGupta (2001) found behaves like a good confidence interval",
                     font_size=24, color=METHOD_COL["jeffreys"]).to_edge(DOWN, buff=1.0)
        if foot.width > 12.6:
            foot.width = 12.6
        intro = label('A century of alternatives to the Wald interval', font_size=36)
        with self.voiceover(
            "The better intervals have been available for almost a century. <bookmark mark='a'/> In 1927 Edwin Bidwell "
            "Wilson, a mathematician and physicist who had been Gibbs's student, inverted the score test. "
            "<bookmark mark='b'/> In 1934 Charles Clopper and Egon Pearson inverted exact tests, and got an interval whose "
            "coverage never falls below ninety-five percent. <bookmark mark='c'/> In 1998 Alan Agresti and Brent Coull, "
            "in a paper with the provocative title 'Approximate is better than exact', proposed adding two successes and "
            "two failures and then using the Wald formula. <bookmark mark='d'/> And Brown, Cai and DasGupta found that "
            "the Bayesian interval from Jeffreys' prior also behaves like a good confidence interval."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def wilson(self):
        rows = [
            cmath(r"\frac{|\hat p - p_0|}{\sqrt{p_0(1 - p_0)/n}}", r"\le", r"z", r"\quad\text{the score test accepts } p_0", font_size=32),
            cmath(r"(\hat p - p_0)^2", r"\le", r"z^2\,\frac{p_0(1 - p_0)}{n}", r"\quad\text{a quadratic in } p_0", font_size=32),
            cmath(r"\text{centre}", r"=", r"\frac{\hat p + z^2/(2n)}{1 + z^2/n} = \frac{x + z^2/2}{n + z^2}", font_size=32),
            cmath(r"x + 2,\ n + 4", r"\Rightarrow", r"\text{Agresti--Coull: Wald around Wilson's centre}", font_size=30),
        ]
        rows[2][2].set_color(METHOD_COL["wilson"])
        rows[3][2].set_color(METHOD_COL["agresti_coull"])
        whys = [why(r"the null's own SE, \ not $\hat p$'s"), why(r"square: \ solve for the two roots"),
                why(r"pulled toward $\tfrac12$: \ never a zero-width interval"), why(r"$z^2/2 \approx 2$: \ ``add two successes and two failures''")]
        with self.voiceover(
            "Here's why Wilson's interval works. <bookmark mark='a'/> The score test divides by the standard error the "
            "null value implies, root p-nought times one minus p-nought over n, not by the estimated one. "
            "<bookmark mark='b'/> Squaring, the accepted values of p-nought satisfy a quadratic inequality, and its two "
            "roots are the interval's ends. <bookmark mark='c'/> The interval's centre isn't p-hat: it's pulled toward a "
            "half, as if z squared over two extra successes and failures had been added. Even with zero successes, the "
            "interval has positive width. <bookmark mark='d'/> Agresti and Coull's idea: z squared over two is almost "
            "two, so add two successes and two failures, and use the plain Wald formula around that centre."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.7, x=-0.2, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def panels(self):
        d = load("binom")
        ps = np.asarray(d["ps"])
        order = ["wald", "wilson", "agresti_coull", "clopper_pearson", "jeffreys", "lr"]
        panels = VGroup()
        for i, k in enumerate(order):
            r, c = divmod(i, 3)
            A = axes([0, 1], [0.8, 1], x_length=3.6, y_length=1.8, xticks=[0, 0.5, 1], yticks=[0.8, 0.95, 1], yfmt=lambda v: f"{v:.2f}",
                     center=[-4.3 + 4.3 * c, 1.6 - 3.3 * r, 0], font_size=16)
            ax = A.ax
            cov = np.asarray(d["cov"][k])
            cv = polyline(ax, ps, cov, METHOD_COL[k], 1.6)
            nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=EXACT, stroke_width=1.5)
            ttl = label(METHOD_TEX[k], font_size=22, color=METHOD_COL[k]).next_to(A, UP, buff=0.08)
            num = MathTex(rf"\text{{grid mean }} {100 * d['mean'][k]:.1f}\%,\ \text{{grid min }} {100 * d['min'][k]:.1f}\%", font_size=20,
                          color=METHOD_COL[k]).next_to(A, DOWN, buff=0.1)
            panels.add(VGroup(A, nom, cv, ttl, num))
        tag = note(r"exact coverage, \ $n = 50$, \ clipped at 80\%").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now the comparison, with exact coverage curves for fifty trials. All averages and minima here refer to the displayed parameter grid. <bookmark mark='a'/> Wald: mean ninety "
            "point seven, and a minimum off the bottom of the chart, twenty-two percent near the edges. "
            "<bookmark mark='b'/> Wilson: mean ninety-five point two, close to the promise, with dips to ninety-one near "
            "the edges. <bookmark mark='c'/> Agresti–Coull: slightly conservative, ninety-five point eight on average, "
            "and no sampled grid value below ninety-three and a half. <bookmark mark='d'/> Clopper–Pearson: always at or above "
            "ninety-five, as guaranteed, but at the price of averaging ninety-seven: it promises ninety-five and delivers "
            "more, by being wide. <bookmark mark='e'/> Jeffreys: mean ninety-five point oh, with deep dips near zero "
            "and one. <bookmark mark='f'/> And the likelihood ratio interval: mean ninety-four point eight, also dipping "
            "at the edges. All of them sawtooth, because the data are discrete. None is perfect; the Wald interval is "
            "simply the worst."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[1]) for p in panels], *[FadeIn(p[3]) for p in panels])
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(Create(panels[k][2]), FadeIn(panels[k][4]), run_time=1.2)
        self.clear_scene()

    def widths(self):
        d = load("binom")
        order = ["wald", "wilson", "agresti_coull", "clopper_pearson", "jeffreys", "lr"]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"interval", r"grid mean coverage", r"width at $p = 0.05$", r"width at $p = 0.5$")])
        xs = [-4.4, -1.2, 1.6, 4.4]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.4, 0])
        cells = VGroup()
        for i, k in enumerate(order):
            y = 1.7 - 0.55 * i
            cells.add(VGroup(label(METHOD_TEX[k], font_size=26, color=METHOD_COL[k]).move_to([xs[0], y, 0]),
                             MathTex(rf"{100 * d['mean'][k]:.1f}\%", font_size=28).move_to([xs[1], y, 0]),
                             MathTex(rf"{d['width05'][k]:.3f}", font_size=28).move_to([xs[2], y, 0]),
                             MathTex(rf"{d['width5'][k]:.3f}", font_size=28).move_to([xs[3], y, 0])))
        foot = label(r"Wald is narrowest near the edge \ because it is wrong there; \ coverage must be compared before width", font_size=24,
                     color=OBS).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "What do the better intervals cost? <bookmark mark='a'/> Width. At p equals a half, they're all about the same, "
            "around point two seven. <bookmark mark='b'/> At p equals point zero five, the Wald interval is the narrowest, "
            "point one zero, and Agresti–Coull and Clopper–Pearson the widest, near point one four. "
            "<bookmark mark='c'/> But the Wald interval is narrow there precisely because it's wrong there. A short "
            "interval that misses isn't a bargain. Coverage has to be checked before width means anything."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"Brown, Cai \& DasGupta's advice", font_size=32, color=OBS),
            label(r"never use the Wald interval for a proportion", font_size=26, color=METHOD_COL["wald"]),
            label(r"small $n$: \ Wilson or Jeffreys; \ $n \ge 40$: \ Agresti--Coull too", font_size=26),
            label(r"Clopper--Pearson when the 95\% must be guaranteed, \ at every $p$, \ and width is the price", font_size=24, color=GREY_A),
            label(r"all of them: \ \texttt{statkit.intervals.BINOMIAL}, \ with exact coverage by \texttt{binom\_coverage}", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Brown, Cai and DasGupta's advice has become standard. <bookmark mark='b'/> Never use the "
            "Wald interval for a proportion. <bookmark mark='c'/> For small samples, Wilson or Jeffreys; for forty or "
            "more, Agresti–Coull is fine too, and it's easy to teach. <bookmark mark='d'/> Use Clopper–Pearson when the "
            "ninety-five percent must be guaranteed for every p, as in a regulatory setting, and accept the extra width. "
            "<bookmark mark='e'/> All six are in statkit's intervals module, with a function that computes any interval's "
            "exact coverage, so you can check them yourself."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wilson_saw(self):
        from explainer.stats.kit import intervals as I
        ns = np.arange(10, 101)
        A = axes([10, 100], [0.8, 1.0], x_length=9.6, y_length=4.2, xlabel=r"sample size $n$", ylabel=r"exact coverage at $p = 0.2$",
                 xticks=[10, 25, 50, 75, 100], yticks=[0.8, 0.9, 0.95, 1.0], yfmt=lambda v: f"{v:.2f}", center=[0, 0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(10, 0.95), ax.c2p(100, 0.95), color=EXACT, stroke_width=2)
        curves = VGroup()
        for k in ("wald", "wilson", "agresti_coull"):
            cov = [float(I.binom_coverage(I.BINOMIAL[k], int(n), [0.2])[0]) for n in ns]
            curves.add(polyline(ax, ns, cov, METHOD_COL[k], 2.2))
        leg = legend([(METHOD_COL[k], METHOD_TEX[k]) for k in ("wald", "wilson", "agresti_coull")], font_size=22).to_edge(UP, buff=0.3).shift(RIGHT * 4)
        foot = label(r"better approximations still oscillate above and below 95\%; \ no uniform guarantee", font_size=26, color=OBS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Back to the hook's picture, with the better intervals added. <bookmark mark='a'/> The Wald interval's coverage "
            "at p equals point two, as n grows. <bookmark mark='b'/> Wilson's: still a sawtooth, from ninety-two and a half "
            "to ninety-eight, but straddling the promise instead of sitting below it. <bookmark mark='c'/> Agresti–Coull, "
            "similar and a little higher. <bookmark mark='d'/> Discreteness never goes away; what changes is whether the "
            "teeth point up or down."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(leg[k]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def world_case(self):
        from explainer.stats.kit import intervals as I
        from explainer.stats.world import World

        W = World()
        sick = W.screening["sick"]
        truth = float(sick[W.adult].mean())
        idx = W.sample(300, among=W.adult, seed=11)
        x = int(sick[idx].sum())
        A = axes([0, 0.04], [0, 4], x_length=7.0, y_length=3.4, xlabel=r"prevalence of the World's silent condition", xticks=[0, 0.01, 0.02, 0.03, 0.04],
                 xfmt=lambda v: f"{v:g}", center=[0.4, 0.4, 0])
        ax = A.ax
        tr = DashedLine(ax.c2p(truth, 0), ax.c2p(truth, 4), color=EXACT, stroke_width=2.5)
        lines = VGroup()
        for i, k in enumerate(("wald", "wilson", "clopper_pearson")):
            lo, hi = I.BINOMIAL[k](x, 300)
            y = 3.2 - i
            lines.add(VGroup(Line(ax.c2p(lo, y), ax.c2p(hi, y), color=METHOD_COL[k], stroke_width=6),
                             label(METHOD_TEX[k], font_size=22, color=METHOD_COL[k]).next_to(ax.c2p(0, y), LEFT, buff=0.2),
                             MathTex(rf"[{lo:.4f}, {hi:.4f}]", font_size=22, color=METHOD_COL[k]).next_to(ax.c2p(hi, y), RIGHT, buff=0.15)))
        rows = fit_rows(VGroup(
            label(rf"a survey of 300 adults finds {x} cases; \ the World's true prevalence is {100 * truth:.2f}\%", font_size=24),
            label(r"Wald's lower end, \ 0.0004, \ is a prevalence of 1 in 2,800: \ an artefact of symmetry", font_size=24, color=MISS),
        ), 12.6, 0.3, [0, -2.4, 0])
        tag = simulated_tag(r"the World: \ screening", corner=UR)
        with self.voiceover(
            "A realistic case from the World, which has a silent condition affecting just under one percent of adults. Binomial calculations approximate this survey without replacement; the sampling fraction is small. "
            "<bookmark mark='a'/> A survey of three hundred adults finds four cases. <bookmark mark='b'/> The Wald interval "
            "runs from point zero zero zero four to point zero two six; Wilson's and Clopper–Pearson's from about point "
            "zero zero four to point zero three four. <bookmark mark='c'/> All three happen to contain the truth this "
            "time. But Wald's lower end, one in twenty-eight hundred, is an artefact of forcing a symmetric interval onto "
            "a skewed problem, and its upper end is too low: exactly the pattern that makes it miss so often near zero."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.15) for l_ in lines], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
