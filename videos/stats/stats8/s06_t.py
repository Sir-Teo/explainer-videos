from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403

T_COLS = {"1": S.RESID, "3": S.POST, "10": S.LIK, "30": SIM}


class StudentT(VoiceoverScene):
    def construct(self):
        self.card()
        self.density()
        self.family()
        self.multipliers()
        self.sleep()
        self.unpaired()

    def card(self):
        card = chapter_card(5, r"Student's $t$", r"A normal, divided by its own estimated scale", lit=(1908,), part=PART)
        with self.voiceover("Chapter five. Student's t."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def density(self):
        rows = [
            cmath(r"T", r"=", r"\frac{Z}{\sqrt{V/k}}", r",\quad Z \sim N(0,1) \perp V \sim \chi^2_k", font_size=34),
            cmath(r"f_T(t)", r"=", r"\int_0^\infty \phi\big(t\sqrt{v/k}\big)\sqrt{v/k}\ f_V(v)\,dv", font_size=32),
            cmath(r"f_T(t)", r"=", r"\frac{\Gamma\big(\tfrac{k+1}{2}\big)}{\sqrt{k\pi}\,\Gamma\big(\tfrac k2\big)}\Big(1 + \frac{t^2}{k}\Big)^{-(k+1)/2}",
                  font_size=32),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"chapter 3: \ the mean's coordinate over the deviations' length"),
                why(r"given $V = v$, \ $T$ is normal with scale $\sqrt{k/v}$: \ average over $v$ (Part 5's mixture)"),
                why(r"the integral is a gamma integral (Part 3)")]
        foot = label(r"a scale mixture of normals: \ the uncertainty in $s$ fattens the tails", font_size=26, color=S.ACCENT)
        foot.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Now the derivation. <bookmark mark='a'/> The t statistic is a standard normal divided by the square root "
            "of an independent chi-squared over its degrees of freedom: the mean's coordinate, over the deviations' "
            "length. <bookmark mark='b'/> Given the chi-squared, T is just a normal with a scale set by it. So the "
            "density of T is a mixture: average the normal density over the distribution of the scale, Part 5's "
            "latent-variable formula. <bookmark mark='c'/> The integral is a gamma integral, and out comes Student's "
            "density: a power of one plus t squared over k. <bookmark mark='d'/> It's a scale mixture of normals. "
            "Uncertainty about the scale is what fattens the tails."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def family(self):
        d = load("tdist")
        xs = np.asarray(d["xs"])
        A = axes([-5, 5], [0, 0.42], x_length=7.6, y_length=4.4, xlabel=r"$t$", xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4],
                 center=[-2.0, -0.4, 0])
        ax = A.ax
        nrm = curve(ax, xs, np.asarray(d["normal"]), EXACT, 4)
        cvs = VGroup(*[curve(ax, xs, np.asarray(d["pdf"][k]), c, 2.5) for k, c in T_COLS.items()])
        leg = legend([(c, rf"$t_{{{k}}}$: \ $P(|T| > 2) = {d['tail2'][k]:.3f}$") for k, c in T_COLS.items()] +
                     [(EXACT, r"normal: \ $0.046$")], font_size=22).move_to([4.6, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"$k = 1$: \ the Cauchy (Part 6's failed average)", font_size=22, color=S.RESID),
            label(r"$k \to \infty$: \ the normal \ ($s \to \sigma$, \ Slutsky)", font_size=22, color=EXACT),
        ), 5.0, 0.22, [4.6, -1.8, 0])
        with self.voiceover(
            "Here's the family. <bookmark mark='a'/> With one degree of freedom, it's the Cauchy, Part 6's distribution "
            "whose average never settles: the chance of exceeding two is thirty percent. <bookmark mark='b'/> With "
            "three, ten and thirty degrees of freedom the tails thin out, <bookmark mark='c'/> and in the limit the t "
            "distribution becomes the normal, because s converges to sigma, which is Part 6's Slutsky argument. By "
            "thirty degrees of freedom the two are hard to tell apart in the middle, though not far out in the tails."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cvs[0]), FadeIn(leg[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs[1:]], lag_ratio=0.4), FadeIn(leg[1:4]))
            vo.wait_until("c")
            self.play(Create(nrm), FadeIn(leg[4]), FadeIn(rows[1]))
        self.clear_scene()

    def multipliers(self):
        d = load("tdist")
        q = d["q975"]
        ks = [1, 2, 3, 4, 5, 9, 20, 60, 120]
        A = axes([0, np.log10(150)], [1.8, 4.6], x_length=7.4, y_length=4.2, xlabel=r"degrees of freedom $k$ (log scale)",
                 ylabel=r"$t_{k,\,0.975}$", xticks=[0, 1, 2], yticks=[2, 3, 4], xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, -0.4, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(np.log10(k), min(q[str(k)], 4.6)), radius=0.08, color=EXACT) for k in ks])
        labs = VGroup(*[MathTex(f"{q[str(k)]:.2f}", font_size=20, color=GREY_A).next_to(ax.c2p(np.log10(k), min(q[str(k)], 4.6)), UR, buff=0.05)
                        for k in ks if k in (2, 3, 4, 9, 30, 120) or k == 120])
        z = DashedLine(ax.c2p(0, 1.96), ax.c2p(np.log10(150), 1.96), color=GREY_B, stroke_width=2)
        zl = MathTex(r"1.96", font_size=24, color=GREY_B).next_to(ax.c2p(np.log10(150), 1.96), RIGHT, buff=0.1)
        rows = fit_rows(VGroup(
            label(r"the 95\% multiplier for $\bar x \pm t\, s/\sqrt n$", font_size=24),
            MathTex(r"k = 1:\ 12.71", font_size=26, color=S.RESID),
            label(r"$n = 4$ ($k = 3$): \ 3.18, \ not 1.96", font_size=24, color=EXACT),
            label(r"the price of not knowing $\sigma$: \ wider intervals", font_size=24, color=GREY_A),
        ), 4.8, 0.3, [4.6, 0.6, 0])
        with self.voiceover(
            "What does it mean in practice? <bookmark mark='a'/> The interval for a mean becomes the sample mean plus "
            "or minus a t multiplier times the standard error. <bookmark mark='b'/> With two observations, one degree "
            "of freedom, the multiplier is twelve point seven. With four observations it's three point one eight, "
            "the multiplier Gosset needed. <bookmark mark='c'/> It falls quickly toward one point nine six: two point "
            "two six at nine degrees of freedom, about two at sixty. That gap is the price of not knowing sigma, paid "
            "in width, and t makes it exactly the right price when the data are normal."
        ) as vo:
            self.play(FadeIn(A), Create(z), FadeIn(zl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.15), FadeIn(rows[1:3]), FadeIn(labs))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sleep(self):
        d = load("tdist")["sleep"]
        dd = np.asarray(d["d"])
        A = axes([-0.5, 5.0], [0, 11], x_length=6.0, y_length=3.6, xlabel=r"extra hours of sleep, \ drug 2 minus drug 1",
                 xticks=[0, 1, 2, 3, 4, 5], center=[-3.4, 0.4, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        order = np.argsort(dd)
        dots = VGroup(*[Dot(ax.c2p(v, 1 + i), radius=0.09, color=DATA) for i, v in enumerate(dd[order])])
        mean_l = DashedLine(ax.c2p(d["mean"], 0), ax.c2p(d["mean"], 11), color=SIM, stroke_width=2.5)
        ci = Line(ax.c2p(d["ci"][0], 0.3), ax.c2p(d["ci"][1], 0.3), color=EXACT, stroke_width=6)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 11), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            MathTex(rf"\bar d = {d['mean']:.2f},\ \ s = {d['sd']:.2f},\ \ n = 10", font_size=28),
            MathTex(rf"t = \frac{{{d['mean']:.2f}}}{{{d['sd']:.2f}/\sqrt{{10}}}} = {d['t']:.2f}", font_size=30, color=SIM),
            MathTex(rf"95\%:\ {d['mean']:.2f} \pm 2.26 \times {d['sd'] / np.sqrt(10):.2f} = [{d['ci'][0]:.2f},\ {d['ci'][1]:.2f}]",
                    font_size=26, color=EXACT),
            MathTex(rf"P(|t_9| \ge {d['t']:.2f}) = {d['p_t']:.4f}\quad \text{{vs normal }} {d['p_z']:.5f}", font_size=24, color=GREY_A),
            label(r"pairing: \ each patient is his own control (Part 13)", font_size=22, color=GREY_A),
        ), 5.6, 0.3, [3.6, 0.2, 0])
        src = historical_tag(r"Cushny \& Peebles (1905), \ in Student (1908)", corner=DL)
        with self.voiceover(
            "Student's paper ended with real data. <bookmark mark='a'/> Two sleeping drugs had been given to ten "
            "patients each, and the extra hours of sleep recorded. Student took, for each patient, the difference "
            "between the two drugs. <bookmark mark='b'/> The average difference is one point five eight hours, with a "
            "standard deviation of one point two three. <bookmark mark='c'/> The t statistic is four point oh six on "
            "nine degrees of freedom, and the ninety-five percent interval runs from point seven to two point four six "
            "hours. <bookmark mark='d'/> Treating t as normal would have overstated the evidence: a tail probability of "
            "five in a hundred thousand, where the right answer is about three in a thousand. Comparing each patient "
            "with himself, a paired design, is an idea Part 13 develops."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(mean_l), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(ci), FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def unpaired(self):
        e = load("extras")["unpaired"]
        rows = fit_rows(VGroup(
            label(r"the same 20 numbers, \ analysed as two separate groups of 10:", font_size=26),
            MathTex(r"t = \frac{\bar x_2 - \bar x_1}{s_p\sqrt{2/10}} = " + f"{e['t']:.2f}" + r",\quad 18\ df,\quad p = " + f"{e['p']:.3f}",
                    font_size=30, color=RESID),
            MathTex(r"\text{paired: } t = 4.06,\quad 9\ df,\quad p = 0.003", font_size=30, color=SIM),
            MathTex(rf"\operatorname{{corr}}(\text{{drug 1}}, \text{{drug 2}}) = {e['r']:.2f}", font_size=28),
            label(r"patients differ a lot from each other; \ pairing subtracts that variation out", font_size=24, color=S.ACCENT),
            label(r"the design decides the analysis: \ Part 10 (two-sample tests), \ Part 13 (blocking)", font_size=22, color=GREY_A),
        ), 12.6, 0.35, [0, 0.2, 0])
        with self.voiceover(
            "What if Student had ignored the pairing? <bookmark mark='a'/> Treat the same twenty numbers as two "
            "independent groups of ten. <bookmark mark='b'/> The two-sample t statistic is only one point eight six, "
            "and the p-value is point oh eight: no clear evidence at all. <bookmark mark='c'/> Paired, it was four point "
            "oh six, with p point oh oh three. <bookmark mark='d'/> The difference is the correlation between a "
            "patient's two results, point eight. Some patients sleep much more than others on either drug; pairing "
            "subtracts that variation out. <bookmark mark='e'/> The way the data were collected decides the right "
            "analysis, a theme of Parts 10 and 13."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k] if k < 4 else rows[4:], shift=RIGHT * 0.2))
        self.clear_scene()
