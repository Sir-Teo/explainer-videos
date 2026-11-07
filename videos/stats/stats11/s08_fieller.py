from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Fieller(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.derivation()
        self.shapes()
        self.g_rule()
        self.impossible()

    def card(self):
        card = chapter_card(7, r"Ratios: \ Fieller", r"When the denominator might be near zero", part=PART)
        with self.voiceover("Chapter seven. Ratios, and Fieller's interval."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"many targets are ratios of means, \ $\rho = \mu_y/\mu_x$", font_size=28),
            label(r"bioassay: \ the relative potency of two drugs; \ the dose that kills half (ED50)", font_size=24, color=GREY_A),
            label(r"economics: \ cost per life saved, \ an incremental cost-effectiveness ratio", font_size=24, color=GREY_A),
            label(r"Part 8's Laplace: \ people per birth", font_size=24, color=GREY_A),
            label(r"the delta method gives $\hat\rho \pm 1.96\,\mathrm{SE}$; \ it breaks when $\bar x$ might be near zero", font_size=26,
                  color=MISS),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Many quantities of interest are ratios of two means. <bookmark mark='b'/> In bioassay, "
            "the relative potency of two drugs, or the dose that kills half the subjects. <bookmark mark='c'/> In health "
            "economics, the extra cost per life saved. <bookmark mark='d'/> In Part 8, Laplace's people per birth. "
            "<bookmark mark='e'/> The delta method gives an estimate plus or minus one point nine six standard errors. "
            "That works when the denominator is far from zero compared with its uncertainty, and fails badly when it "
            "isn't."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def derivation(self):
        rows = [
            cmath(r"\bar y - \rho\,\bar x", r"\sim", r"N\big(0,\ v_y - 2\rho\,c_{xy} + \rho^2 v_x\big)", font_size=32),
            cmath(r"(\bar y - \rho\,\bar x)^2", r"\le", r"z^2\,\big(v_y - 2\rho\,c_{xy} + \rho^2 v_x\big)", font_size=32),
            cmath(r"(\bar x^2 - z^2 v_x)\,\rho^2 - 2(\bar x\bar y - z^2 c_{xy})\,\rho + (\bar y^2 - z^2 v_y)", r"\le", r"0", font_size=28),
        ]
        rows[2][0].set_color(OBS)
        whys = [why(r"at the true $\rho$: \ an exact pivot: \ jointly normal means, known covariance"), why(r"accept $\rho$ if the pivot is small"),
                why(r"a quadratic inequality in $\rho$: \ Fieller (1940, 1954)")]
        intro = label('Avoid dividing by an uncertain denominator', font_size=36)
        with self.voiceover(
            "Edgar Fieller's idea, in 1940, was to avoid dividing at all. <bookmark mark='a'/> At the true ratio rho, the "
            "combination y-bar minus rho x-bar has mean zero, and for jointly normal means with known covariance it's exactly normal, with a variance "
            "we can write down. <bookmark mark='b'/> So accept every rho for which this pivot is within z standard "
            "errors of zero. <bookmark mark='c'/> Squared out, that's a quadratic inequality in rho. Its solution set is "
            "Fieller's confidence set, and its coverage is exact under this known-covariance normal model. A common independent estimated variance scale uses a t cutoff instead. But a quadratic inequality doesn't always describe an "
            "interval."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def shapes(self):
        d = load("fieller")
        specs = [("clear", r"$\bar x = 10 \pm 1$"), ("weak", r"$\bar x = 2.2 \pm 1$"), ("rays", r"$\bar x = 1.7 \pm 1$"), ("none", r"$\bar x = 0.8 \pm 1$")]
        lines = VGroup()
        for i, (k, t) in enumerate(specs):
            c = d[k]
            y = 2.2 - 1.45 * i
            nl = NumberLine(x_range=[-6, 12, 2], length=8.4, include_numbers=i == 3, font_size=18, color=GREY_C).move_to([0.9, y, 0])
            g = VGroup(nl, label(t + r", \ $\bar y = " + f"{c['my']:g}" + r" \pm 1$", font_size=20, color=GREY_A).next_to(nl, LEFT, buff=0.2))
            clipx = lambda v: float(np.clip(v, -6, 12))  # noqa: E731
            if c["kind"] == "bounded":
                g.add(Line(nl.n2p(clipx(c["lo"])), nl.n2p(clipx(c["hi"])), color=OBS, stroke_width=8))
            elif c["kind"] == "complement":
                g.add(Line(nl.n2p(-6), nl.n2p(clipx(c["lo"])), color=OBS, stroke_width=8),
                      Line(nl.n2p(clipx(c["hi"])), nl.n2p(12), color=OBS, stroke_width=8))
                if c["lo"] < -6:
                    g.add(VGroup(Arrow(nl.n2p(-4.5), nl.n2p(-6.3), buff=0, color=OBS, stroke_width=4),
                                 MathTex(rf"\text{{and}}\ \le {c['lo']:.0f}", font_size=20, color=OBS).next_to(nl.n2p(-4.5), UP, buff=0.12)))
            else:
                g.add(Line(nl.n2p(-6), nl.n2p(12), color=OBS, stroke_width=8))
            dl, dh = c["delta"]
            g.add(Line(nl.n2p(clipx(dl)) + DOWN * 0.22, nl.n2p(clipx(dh)) + DOWN * 0.22, color=METHOD_COL["wald"], stroke_width=4))
            g.add(Dot(nl.n2p(clipx(c["ratio"])), radius=0.07, color=WHITE))
            desc = {"bounded": r"bounded", "complement": r"two rays", "all": r"the whole line"}[c["kind"]]
            g.add(label(desc, font_size=22, color=OBS).next_to(nl, RIGHT, buff=0.2))
            lines.add(g)
        leg = legend([(OBS, r"Fieller (exact)"), (METHOD_COL["wald"], r"delta method")], font_size=22).to_edge(UP, buff=0.25).shift(RIGHT * 3)
        with self.voiceover(
            "Four datasets, each mean measured with a standard error of one. <bookmark mark='a'/> When "
            "x-bar is ten, far from zero, Fieller's set is an ordinary interval, almost the same as the delta method's. "
            "<bookmark mark='b'/> When x-bar is two point two, Fieller's interval is bounded but strongly skewed, from "
            "one to twenty-one, while the delta method's is symmetric and stops at four and a half: it understates how "
            "large the ratio could be. <bookmark mark='c'/> At one point seven, the denominator might plausibly be zero, "
            "and the solution of the quadratic is two rays: everything above one point one seven, and everything below "
            "minus nineteen. The ratio could be huge, of either sign. <bookmark mark='d'/> And at point eight, the "
            "confidence set is the whole line. At this confidence level no finite ratio is excluded, and Fieller's method says so, where "
            "the delta method confidently reports a finite interval."
        ) as vo:
            self.play(FadeIn(leg))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(lines[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def impossible(self):
        tc = theorem_card(r"Gleser \& Hwang (1987)", r"In weakly identified ratio models satisfying their conditions, \ as a ratio does when "
                          r"$\mu_x = 0$, \ any confidence set with coverage $1 - \alpha > 0$ for every parameter value \ must be unbounded "
                          r"with positive probability.", color=OBS, width=10.4, font_size=26).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"Fieller's infinite sets are not a flaw: \ every honest procedure must sometimes give one", font_size=26, color=OBS),
            label(r"a method that always reports a finite interval for a ratio \ must fail its promise near $\mu_x = 0$", font_size=24),
            label(r"weak instruments in econometrics are the same problem: \ Part 37's Anderson--Rubin sets", font_size=24, color=GREY_A),
        ), 12.6, 0.34, [0, -1.7, 0])
        with self.voiceover(
            "Is the infinite answer a defect? <bookmark mark='a'/> No. Leon Gleser and Jiunn Tzon Hwang proved in 1987 that "
            "under appropriate weak-identification conditions, as a ratio does when the denominator's mean is zero, every "
            "confidence procedure that keeps its promise for every parameter value must sometimes return an unbounded "
            "set. <bookmark mark='b'/> Fieller's infinite answers are honesty, not failure. <bookmark mark='c'/> Any "
            "method that always reports a finite interval for a ratio must break its promise near a zero denominator. "
            "<bookmark mark='d'/> The same theorem governs weak instruments in econometrics, and Part 37's Anderson–Rubin "
            "intervals, which can also be infinite."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def g_rule(self):
        d = load("fieller")
        rows = [
            cmath(r"g", r"=", r"\frac{z^2\, v_x}{\bar x^2} = \Big(\frac{z}{\bar x/\mathrm{SE}(\bar x)}\Big)^2", font_size=34),
            cmath(r"g < 1", r"\iff", r"\bar x \text{ is significantly far from } 0 \iff \text{Fieller's set is bounded}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"Fieller's index: \ how uncertain the denominator is"), why(r"$g = 1$: \ the denominator's own interval just touches 0")]
        vals = VGroup(*[MathTex(rf"\bar x = {d[k]['mx']:g}:\ g = {1.96 ** 2 / d[k]['mx'] ** 2:.2f}", font_size=28,
                                color=OBS if 1.96 ** 2 / d[k]['mx'] ** 2 < 1 else MISS) for k in ("clear", "weak", "rays", "none")])
        vals.arrange(RIGHT, buff=0.6).move_to([0, -1.2, 0])
        if vals.width > 12.6:
            vals.width = 12.6
        foot = label(r"a common rule: \ use the delta method only when $g < 0.05$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        intro = label('Measure the uncertainty in the denominator', font_size=36)
        with self.voiceover(
            "There's a one-number summary of which case you're in. <bookmark mark='a'/> Fieller's index g is z squared "
            "times the denominator's variance over its squared estimate: one over the denominator's squared z-score, "
            "scaled. <bookmark mark='b'/> The set is bounded exactly when g is less than one, which is when the "
            "denominator is significantly different from zero. <bookmark mark='c'/> Our four cases have g of point zero "
            "four, point eight, one point three and six. <bookmark mark='d'/> A common rule in bioassay is to trust the "
            "delta method only when g is below about point zero five."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(vals))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
