from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import predict, ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, load, real_data

ALPHA, LAM, GAM_G = 0.88, 2.25, 0.61  # Tversky and Kahneman (1992)


def v(x):
    x = np.asarray(x, float)
    return np.where(x >= 0, np.abs(x) ** ALPHA, -LAM * np.abs(x) ** ALPHA)


def w(p, g=GAM_G):
    p = np.asarray(p, float)
    return p ** g / (p ** g + (1 - p) ** g) ** (1 / g)


class Behaviour(VoiceoverScene):
    def construct(self):
        self.card()
        self.allais()
        self.prospect()
        self.myopic(load("myopic_loss"))
        self.ambiguity()
        self.robust(load("robust_fraction"))

    def card(self):
        c = chapter_card(13, r"How people decide: prospect theory and ambiguity", r"What do real decisions look like?",
                         part=PART)
        with self.voiceover("Chapter thirteen. How people really decide: prospect theory, and ambiguity."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def allais(self):
        a = VGroup(label(r"Choice 1:\quad A: \$1 million for sure \quad or \quad B: 10\%: \$5m, 89\%: \$1m, 1\%: nothing",
                         font_size=22),
                   label(r"Choice 2:\quad C: 11\%: \$1m \quad or \quad D: 10\%: \$5m", font_size=22),
                   label(r"a commonly observed pattern: A and D", font_size=26, color=KELLY),
                   wrapped_label(r"C and D come from A and B by replacing a common 89\% chance of \$1m with zero; "
                                 r"independence says the order cannot flip (Allais 1953)", 12.0, 22, OVER),
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "Does anyone actually choose by expected utility? In 1953 Maurice Allais offered two choices. A sure million, "
            "or ten percent of five million, eighty-nine of one million, one of nothing: most take the sure million. Eleven "
            "percent of a million, or ten percent of five: most take the five. <bookmark mark='a'/> But the second pair is "
            "A and B with their common eighty-nine percent chance of a million replaced by zero in both. Independence says the order cannot flip; "
            "people flip it."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in a[:3]], lag_ratio=0.6, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(a[3]))
        self.wait(0.4)
        self.clear_scene()

    def prospect(self):
        g1 = axes([-100, 100], [-150, 70], x_length=5.4, y_length=3.3, xlabel=r"gain or loss from the reference point",
                  ylabel=r"value", xticks=[-100, 0, 100], yticks=[], font_size=16)
        g2 = axes([0, 1], [0, 1], x_length=3.3, y_length=3.3, xlabel=r"probability", ylabel=r"decision weight",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.6)  # short enough to leave the formulas room
        x = np.linspace(-100, 100, 201)
        lv = curve(g1.ax, x, v(x), VALUE, stroke_width=4)
        ref = DashedLine(g1.ax.c2p(0, -150), g1.ax.c2p(0, 70), color=GREY_C, stroke_width=1.5)
        p = np.linspace(0.001, 0.999, 200)
        diag = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        lw = curve(g2.ax, p, w(p), KELLY, stroke_width=4)
        notes = VGroup(
            MathTex(r"v(x) = x^{0.88}\ (x \ge 0),\quad -2.25\,(-x)^{0.88}\ (x < 0);\quad "
                    r"w(p) = \frac{p^{\delta}}{\big(p^{\delta} + (1-p)^{\delta}\big)^{1/\delta}}", font_size=26,
                    color=VALUE),
            wrapped_label(r"cumulative prospect theory (Tversky and Kahneman 1992; $\delta = 0.61$ for gains, $0.69$ "
                          r"for losses): weights apply to cumulative probabilities, ranked from the extremes, so the "
                          r"tails are overweighted, not every small chance", 11.6, 20, GREY_A),
            wrapped_label(r"in markets: selling winners and holding losers (Shefrin and Statman 1985); lottery-like "
                          r"stocks overpriced (Barberis and Huang 2008)", 11.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Kahneman and Tversky's prospect theory, 1979, and its cumulative form, 1992, makes three changes. "
            "<bookmark mark='a'/> Value is measured from a reference point, concave for gains, convex for losses, with a "
            "kink: the illustrative parameter makes the loss side two and a quarter times as steep in magnitude. These are fitted example parameters, not universal constants. <bookmark mark='b'/> "
            "Probabilities are weighted, so the extremes count for more, ranked from the tails inward. "
            "<bookmark mark='c'/> Related models study holding losers, selling winners and demand for lottery-like payoffs; those interpretations do not by themselves establish market causation."
        ) as vo:
            self.play(FadeIn(g1), Create(ref))
            vo.wait_until("a")
            self.play(Create(lv), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(diag), Create(lw), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def myopic(self, m):
        H = np.asarray(m["h"])
        vs, vb = np.asarray(m["stocks"]), np.asarray(m["bills"])
        r1, r24 = np.asarray(m["ret1"]), np.asarray(m["ret24"])
        # left: the S-curve with the monthly return histogram under it; right: CPT value against the evaluation period
        g1 = axes([-0.9, 1.6], [-1.2, 1.0], x_length=5.4, y_length=4.0, xlabel=r"return over the evaluation period",
                  ylabel=r"prospect value", xticks=[-0.5, 0, 0.5, 1], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[],
                  font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g1.ax
        xs = np.linspace(-0.9, 1.6, 301)
        vv = v(xs)
        inn = (vv >= -1.2) & (vv <= 1.0)  # the curve only inside the axes: no flat runs along the edges
        sc = curve(ax, xs[inn], vv[inn], VALUE, stroke_width=3)
        bins = np.linspace(-0.9, 1.6, 46)

        def hist(r_, col):
            h, _ = np.histogram(r_, bins=bins)
            h = h / len(r_) * 3.0
            grp = VGroup()
            for i, hh in enumerate(h):
                if hh <= 0:
                    continue
                a, b = ax.c2p(bins[i], -1.2), ax.c2p(bins[i + 1], -1.2 + hh)
                grp.add(Rectangle(width=b[0] - a[0] - 0.005, height=b[1] - a[1], stroke_width=0, fill_color=col,
                                  fill_opacity=0.5).move_to((a + b) / 2))
            return grp

        h1, h24 = hist(r1, OVER), hist(r24, GOOD)
        hl = label(r"one month", font_size=20, color=OVER).next_to(g1, UP, buff=0.05).align_to(g1, RIGHT)
        hl2 = label(r"two years", font_size=20, color=GOOD).next_to(g1, UP, buff=0.05).align_to(g1, RIGHT)
        g2 = axes([0, 36], [-0.05, 0.3], x_length=5.6, y_length=4.0, xlabel=r"evaluation period (months)",
                  ylabel=r"prospect-theory value", xticks=[1, 12, 24, 36], yticks=[0, 0.1, 0.2, 0.3], font_size=16)
        g2.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        a2 = g2.ax
        ls = curve(a2, H, vs, KELLY, stroke_width=4)
        lb = curve(a2, H, vb, GREY_B, stroke_width=4)
        cross = m["crossover"]
        cl = DashedLine(a2.c2p(cross, -0.05), a2.c2p(cross, 0.3), color=GOOD, stroke_width=2)
        cll = label(rf"{cross} months", font_size=18, color=GOOD).next_to(a2.c2p(cross, 0.3), DOWN, buff=0.1).shift(
            RIGHT * 0.7)
        leg = legend([(KELLY, r"US stocks"), (GREY_B, r"T-bills")], font_size=18).next_to(g2, UP, buff=0.05).align_to(
            g2, LEFT)
        q = predict(r"If you looked at your portfolio every five years instead of every month, would a loss-averse "
                       r"investor hold more stocks or fewer?", width=6.4, font_size=20).to_edge(UP, buff=0.3)
        src = real_data(r"French 1926--2020, overlapping nominal returns; reference zero, illustrative TK parameters; displayed histogram window, shared frequency scale")
        with self.voiceover(
            "Benartzi and Thaler proposed in 1995 that stocks are shunned because people check them too often. Pause and "
            "predict: looking every five years instead of every month, would a loss-averse investor hold more stocks, or "
            "fewer? <bookmark mark='a'/> The House's registered test, on ninety-four years of US returns. Over a month, half "
            "the returns sit on the steep loss side of the curve; over two years, the distribution slides into gains. "
            "<bookmark mark='b'/> Score stocks and bills every h months: bills win for short periods, and the curves cross "
            f"at {cross} months. Benartzi and Thaler found about a year, against bonds. <bookmark mark='c'/> This pure-stock versus bill comparison does not solve the optimal mixed allocation or the uncomputed five-year case. How "
            "often you look is itself a decision."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), FadeIn(g1), Create(sc), FadeIn(src))
            self.play(FadeIn(h1), FadeIn(hl))
            self.play(ReplacementTransform(h1, h24), ReplacementTransform(hl, hl2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(leg), Create(lb), Create(ls), run_time=2.5)
            self.play(Create(cl), FadeIn(cll))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def ambiguity(self):
        urn = VGroup(
            label(r"Ellsberg (1961): an urn of 90 balls, 30 red, 60 black or yellow in unknown proportion", font_size=24,
                  color=GREY_A),
            wrapped_label(r"most people prefer to bet on red rather than black, and on black-or-yellow rather than "
                          r"red-or-yellow: no single probability makes both choices consistent", 12.0, 22, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.5)
        rows = [cmath(r"0", r"=", r"V_t + \sup_{\pi}\inf_{h}\Big\{\big(r + \pi(\mu - r) + \pi\sigma h\big)xV_x + "
                      r"\tfrac12\pi^2\sigma^2x^2V_{xx} + \frac{h^2}{2\Psi}\Big\}", font_size=28),
                cmath(r"h^*", r"=", r"-\Psi\,\pi\sigma\,xV_x", font_size=30, colors={r"h^*": OVER}),
                cmath(r"\Psi", r"=", r"\frac{\theta}{(1-\gamma)V}\ \Rightarrow\ h^* = -\theta\pi\sigma", font_size=30),
                cmath(r"\pi^*", r"=", r"\frac{\mu - r}{(\gamma + \theta)\,\sigma^2}", font_size=34,
                      colors={r"\pi^*": KELLY})]
        whys = [why(r"robust control (Hansen and Sargent 2001; Anderson, Hansen and Sargent 2003): nature shifts the "
                    r"drift by $\pi\sigma h$, paying an entropy cost", font_size=20),
                why(r"the inner minimum: a parabola in $h$", font_size=20),
                why(r"Maenhout's scaling keeps the problem homothetic: nature lowers the stock's drift by "
                    r"$\theta\pi\sigma^2$", font_size=20),
                why(r"the outer maximum (Maenhout 2004): doubt about the mean acts exactly like extra risk aversion",
                    font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=1.6, x=-0.8, buff=0.55, edge=6.9)
        with self.voiceover(
            "Second, people dislike unknown odds apart from risk: Ellsberg's urn, 1961, and Gilboa and Schmeidler's theory, 1989: choose the action whose worst plausible model is best. <bookmark mark='a'/> Applied to Merton by Pascal Maenhout in 2004, after Hansen and Sargent: nature may lower the stock's drift, paying an entropy cost. <bookmark mark='b'/> The inner minimum is a parabola. <bookmark mark='c'/> With Maenhout's scaling, the bigger your stake, the more pessimistic the worst case. <bookmark mark='d'/> The result is Merton with gamma plus theta: doubt acts like extra risk aversion. The gamma-plus-theta result uses this particular homothetic entropy penalty. Theta here measures ambiguity; it is not the Sharpe-ratio symbol used elsewhere."
        ) as vo:
            self.play(FadeIn(urn))
            vo.wait_until("a")
            step(0, run_time=0.15)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def robust(self, rf):
        ex, s, gam = rf["excess"], rf["sigma"], rf["gamma"]
        row = [r_ for r_ in rf["rows"] if abs(r_["p"] - 0.2) < 1e-9][0]
        th = row["theta"]
        g = axes([0, 1.0], [-0.02, 0.10], x_length=6.2, y_length=4.2, xlabel=r"fraction in stocks $\pi$",
                 ylabel=r"expected excess return believed", xticks=[0, 0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[0, 0.04, 0.08], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        pis = np.linspace(0, 1.0, 101)
        fan = VGroup(*[DashedLine(ax.c2p(0, ex + d), ax.c2p(1.0, ex + d), color=GREY_D, stroke_width=1.2)
                       for d in np.linspace(-0.06, 0.02, 9)])
        nature = curve(ax, pis, ex - th * pis * s ** 2, OVER, stroke_width=4)
        best = curve(ax, pis, gam * s ** 2 * pis, UNDER,
                     stroke_width=4)
        pt = Dot(ax.c2p(row["pi"], ex - th * row["pi"] * s ** 2), color=KELLY, radius=0.1)
        leg = legend([(OVER, r"nature's worst case, given $\pi$"), (UNDER, r"the investor's Merton response, given "
                                                                          r"the drift")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        head = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"detection error", r"$\theta$",
                                                                       r"robust $\pi$")])
        cells = [head] + [VGroup(MathTex(f"{100 * r_['p']:.0f}\\%", font_size=26), MathTex(f"{r_['theta']:.1f}",
                                                                                           font_size=26),
                                 MathTex(f"{100 * r_['pi']:.0f}\\%", font_size=26, color=KELLY)) for r_ in rf["rows"]]
        tab = VGroup(*[x for r_ in cells for x in r_]).arrange_in_grid(rows=len(cells), cols=3, buff=(0.6, 0.15))
        side = VGroup(
            wrapped_label(r"how much doubt is reasonable? Choose $\theta$ so that the worst-case model could not be "
                          r"told apart from the estimate with 94 years of data, at a given error rate (Anderson, "
                          r"Hansen and Sargent 2003)", 4.6, 18, GREY_A),
            tab,
            MathTex(rf"\text{{no doubt: }}{100 * rf['pi_plain']:.0f}\%", font_size=26, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"The game on US numbers, gamma three: in red, nature's worst drift for each position; in blue, the investor's Merton response to each drift. <bookmark mark='a'/> They cross at {100 * row['pi']:.0f} percent, against {100 * rf['pi_plain']:.0f} with no doubt. <bookmark mark='b'/> How much doubt? Choose a calibration convention: choose theta so the worst case would be mistaken for the estimate twenty percent of the time in ninety-four years of data. Then theta is {th:.1f}. Next: the equations behind robust preferences and the American put alike: backward SDEs. Detection error is an equal-prior normal likelihood-test error for constant drifts and known volatility: Phi of minus the absolute drift difference times square-root years over twice sigma. Twenty percent is a chosen calibration, not an empirically established plausibility boundary."
        ) as vo:
            self.play(FadeIn(g), FadeIn(fan), FadeIn(leg))
            self.play(Create(nature), Create(best), run_time=2)
            vo.wait_until("a")
            self.play(GrowFromCenter(pt), Flash(pt, color=KELLY))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.25),
                      FadeIn(side[2]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()
