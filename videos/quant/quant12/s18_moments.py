from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


def _t(s):
    d = date.fromisoformat(s)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class Moments(VoiceoverScene):
    def construct(self):
        m = load("rn_moments")
        self.card()
        self.strips(m)
        self.derive()
        self.series(m)
        self.svix(m)

    def card(self):
        c = chapter_card(13, r"What option prices say about the future", r"Can a strip of options forecast a return?",
                         part=PART)
        with self.voiceover("Chapter thirteen. What option prices say about the future."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def strips(self, m):
        K = np.asarray(m["K"])
        S = m["strips"]
        names = [("logvar", r"log variance: weight $2/K^2$ (the VIX)", IV),
                 ("svix", r"SVIX: weight $2/F^2$, flat (Martin)", LV),
                 ("cubic", r"skewness: weight $(6x - 3x^2)/K^2$ (Bakshi, Kapadia, Madan)", BAD)]
        gs = VGroup()
        for key, title, col in names:
            y = np.asarray(S[key])
            g = axes([K.min(), K.max()], [-1.05, 1.05] if key == "cubic" else [0, 1.05], x_length=3.9, y_length=2.6,
                     xlabel=r"$K/F$", xticks=[0.5, 1.0, 1.5, 2.0], yticks=[], font_size=14)
            bars = VGroup(*[Line(g.ax.c2p(a, 0), g.ax.c2p(a, b), color=col, stroke_width=2) for a, b in zip(K[::8], y[::8])])
            t = wrapped_label(title, 3.9, 17, col).next_to(g, UP, buff=0.1)
            gs.add(VGroup(g, bars, t))
        gs.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.8)
        foot = wrapped_label(r"each bar: weight $\times$ the out-of-the-money option price at that strike, scaled to its "
                             r"largest; the sum is the moment", 12, 19, GREY_B).to_edge(DOWN, buff=0.8)
        mo = m["surface_mom"]
        nums = MathTex(rf"\text{{the Surface, 30 days: }}\ \sigma_Q = {100 * np.sqrt(mo['var']):.1f}\%,\ \ "
                       rf"\text{{skew}}_Q = {mo['skew']:.2f},\ \ \text{{kurt}}_Q = {mo['kurt']:.1f}", font_size=30,
                       color=WHITE).next_to(foot, UP, buff=0.35)
        src = real_data(r"the Surface's SSVI fit, 30-day strip")
        sq, sk, ku = 100 * np.sqrt(mo["var"]), mo["skew"], mo["kurt"]
        with self.voiceover(
            "Chapter nine bought variance with a strip weighted by one over K squared. Change the weights, and the "
            "same options price other things. <bookmark mark='a'/> Weight them equally and you get Ian Martin's SVIX, "
            "the risk-neutral variance of the return itself. <bookmark mark='b'/> Weight them by a cubic in log-"
            "moneyness, negative for puts and positive for calls, and the strip prices the third moment: Gurdip Bakshi, "
            "Nikunj Kapadia and Dilip Madan's risk-neutral skewness, from 2003. <bookmark mark='c'/> On the Surface at "
            f"thirty days: a risk-neutral volatility of {sq:.1f} percent, a skewness of {sk:.2f}, and a kurtosis of "
            f"{ku:.1f}, more than twice a normal distribution's three."
        ) as vo:
            self.play(FadeIn(gs[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(gs[1]))
            vo.wait_until("b")
            self.play(FadeIn(gs[2]), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(nums))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\text{var}^Q(R)", r"=", r"\frac{2}{F^2}\int_0^\infty \text{OTM}(K)\,dK", font_size=38,
                      colors={r"\text{var}^Q(R)": LV}),
                cmath(r"\mathbb{E}[R] - R_f", r"=", r"\frac{\text{var}^Q(R)}{R_f} - \text{cov}(mR, R)", font_size=38,
                      colors={r"\mathbb{E}[R] - R_f": OPT}),
                cmath(r"\text{cov}(mR, R) \le 0", r"\Rightarrow", r"\mathbb{E}[R] - R_f \ge R_f\,\text{SVIX}^2", font_size=38),
                cmath(r"V, W, X", r"=", r"\mathbb{E}^Q[r^2], \mathbb{E}^Q[r^3], \mathbb{E}^Q[r^4],\quad r = \ln S_T/F", font_size=34),
                cmath(r"\text{skew}_Q", r"=", r"\frac{W - 3\mu V + 2\mu^3}{(V - \mu^2)^{3/2}}", font_size=38,
                      colors={r"\text{skew}_Q": BAD})]
        whys = [why(r"Carr--Madan with $f(S) = S^2$: $f'' = 2$, a flat weight; $R = S_T/S_0$, zero rates"),
                why(r"Martin (2017): from $\mathbb{E}^Q X = R_f\,\mathbb{E}[mX]$ and $\mathbb{E}[mR] = 1$, expand "
                    r"$\text{var}^Q(R)$"),
                why(r"his negative-correlation condition: holds if the market's return is bad news for whoever "
                    r"holds it (Problem 5)"),
                why(r"Carr--Madan with $f = r^n$: each moment is its own strip (Bakshi, Kapadia and Madan 2003)"),
                why(r"centre and scale as usual, with $\mu = \mathbb{E}^Q r$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.72, edge=6.9)
        with self.voiceover(
            "Carr and Madan's identity again. For the payoff S squared the second derivative is constant: the "
            "risk-neutral variance is a flat strip. <bookmark mark='a'/> Martin: weight by the discount factor, and "
            "the expected excess return is that variance minus a covariance. <bookmark mark='b'/> If the covariance is "
            "not positive, as Martin argues for the market, the variance is a lower bound on the expected excess return, "
            "read straight from option prices. <bookmark mark='c'/> Powers of the log return give each moment its own "
            "strip; <bookmark mark='d'/> centre and scale for skewness and kurtosis, model free."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def series(self, m):
        t = np.array([_t(d) for d in m["days"]])
        sk, ku = np.asarray(m["skew"]), np.asarray(m["kurt"])
        g1 = axes([2021.2, 2026], [-2.0, 1.0], x_length=8.4, y_length=2.4, ylabel=r"risk-neutral skewness, 30 days",
                  xticks=[], yticks=[-2, -1, 0, 1], font_size=15).to_edge(UP, buff=0.5)
        zero = DashedLine(g1.ax.c2p(2021.2, 0), g1.ax.c2p(2026, 0), color=GREY_C)
        bars = VGroup(*[Line(g1.ax.c2p(a, 0), g1.ax.c2p(a, float(np.clip(b, -2, 1))), color=QC.HOUSE if b > 0 else BAD,
                             stroke_width=2) for a, b in zip(t, sk)])
        g2 = axes([2021.2, 2026], [2, 14], x_length=8.4, y_length=2.0, ylabel=r"risk-neutral kurtosis",
                  xticks=[2022, 2023, 2024, 2025], xfmt=lambda u: f"{u:.0f}", yticks=[3, 8, 13], font_size=15
                  ).next_to(g1, DOWN, buff=0.4)
        three = DashedLine(g2.ax.c2p(2021.2, 3), g2.ax.c2p(2026, 3), color=GREY_C)
        kl = curve(g2.ax, t, np.clip(ku, 2, 14), LV, stroke_width=2)
        ps = m["share_pos_skew"]
        side = label(rf"skewness positive in {100 * ps:.0f}\% of weeks (mean {m['mean_skew']:.2f}); kurtosis "
                     rf"{m['mean_kurt']:.1f} on average; corr(skew, next 30 days' return) = {m['corr_ret']:.2f}",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        src = real_data(r"weekly Deribit surfaces, 2021--2025", corner=UR)
        tsk = load("termskew")
        cs = 100 * tsk["call_skew"]
        pp = 100 * ps
        cr = m["corr_ret"]
        with self.voiceover(
            "Here are both, every Wednesday since 2021. Skewness on top, gold when positive. <bookmark mark='a'/> "
            f"Chapter one found the smile call-skewed in {cs:.0f} percent of weeks; the full risk-neutral skewness "
            f"is positive in only {pp:.0f} percent. They measure different things: the risk reversal compares two "
            "strikes near the money, the skewness weighs the whole distribution, and Bitcoin's far left tail is priced "
            "dearly even in weeks when near-the-money calls are bid. <bookmark mark='b'/> Kurtosis, below, stays far "
            "above three. And the correlation between this week's skewness and the next month's return is "
            f"{cr:.2f}: a description, not a strategy."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(zero), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.004,
                                                                          run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(three), Create(kl), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def svix(self, m):
        h = load("history")
        notes = VGroup(
            wrapped_label(r"Martin (2017): for the S\&P 500 the bound averaged about 5\% a year, and rose above 20\% at "
                          r"the height of the 2008 crisis: expected returns are highest when options are dearest", 11.0, 22,
                          GREY_A),
            wrapped_label(rf"for bitcoin, from the same weekly strips: {100 * m['svix_mean']:.0f}\% a year on average since "
                          rf"2021, {100 * m['svix_late']:.0f}\% in 2024--2025", 11.0, 22, IV),
            wrapped_label(r"it holds only if bitcoin's falls coincide with bad times for its marginal holder: an "
                          r"assumption, not a measurement. Martin and Wagner (2019) extend the bound to single stocks", 11.0,
                          22, GREY_B),
            wrapped_label(r"pause and predict: the bound says at least 30\% a year. Why not simply buy?", 11.0, 22, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN)
        a, b = 100 * m["svix_mean"], 100 * m["svix_late"]
        with self.voiceover(
            "What does the bound say? For the S&P 500, Martin found it averaged about five percent a year, close to "
            "the historical equity premium, and rose above twenty percent at the height of the 2008 crisis. "
            f"<bookmark mark='a'/> For Bitcoin, the same strips give {a:.0f} percent a year on average since 2021, and "
            f"{b:.0f} in the last two years. <bookmark mark='b'/> Pause and predict: if options say Bitcoin's expected "
            "return is at least thirty percent a year, why not simply buy? Because the bound is only as good as its "
            "condition. It assumes the asset's falls arrive in bad times for whoever holds it at the margin. For the "
            "stock market that is plausible; for Bitcoin it is an assumption nobody has tested, and a lower bound "
            "under an assumption is not a forecast."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()
