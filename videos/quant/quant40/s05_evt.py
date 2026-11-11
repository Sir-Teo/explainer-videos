from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import (
    BAD,
    DATA_C,
    HURDLE,
    MODEL_C,
    PART,
    TAIL_C,
    VAR_C,
    load,
)


class EVT(VoiceoverScene):
    def construct(self):
        e = load("evt")
        self.card(e)
        self.fat(e)
        self.pbdh()
        self.pot(e)
        self.survival(e)
        self.sweep()
        self.beyond(e)
        self.hill(e)
        self.tails()
        self.mcneil()
        self.cautions()
        self.question()

    def card(self, e):
        yrs = e["log10_p_worst"] * -1 - math.log10(252)
        c = chapter_card(4, r"Extreme value theory", r"How do we say anything about losses larger than any we have seen?",
                         part=PART)
        with self.voiceover(
            f"Chapter four, and the answer to the pause: the nineteenth of October nineteen eighty-seven was "
            f"{e['z_worst']:.0f} standard deviations. Under the normal, a day like that has a probability of about ten to "
            f"the minus {abs(e['log10_p_worst']):.0f}: once in ten to the {yrs:.0f} years, against a universe fourteen "
            "billion years old. The normal is not wrong in the tail; it is not even close."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fat(self, e):
        rows = [cmath(r"\text{excess kurtosis}", r"=", rf"{e['kurt']:.1f}", font_size=42, colors={rf"{e['kurt']:.1f}": BAD}),
                cmath(r"\text{worst day}", r"=", rf"{100 * e['worst']:.1f}\%\ (19\ \text{{Oct}}\ 1987)", font_size=40),
                cmath(r"P(L > x)", r"\sim", r"x^{-\zeta}", font_size=44, colors={r"P(L > x)": TAIL_C})]
        whys = [why(r"the US market's daily returns, 1926--2020: a normal has zero (Part 1's first stylised fact)"),
                why(r"the largest of 24,896 days, more than sixteen standard deviations"),
                why('a positive-shape regularly varying model has a power tail, not like $e^{-x^2/2}$: the tail exponent $\\zeta$ is what matters, and it is estimable')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"The data reject a simple Gaussian-tail description, without proving one universal tail law. <bookmark mark='a'/> Daily-market excess kurtosis is {e['kurt']:.1f}. <bookmark mark='b'/> The largest observed daily loss is {100*e['worst']:.1f} percent, far out under a fitted Gaussian benchmark. <bookmark mark='c'/> A positive-shape generalized Pareto model motivates power-tail extrapolation. Lognormal, mixtures and other non-Gaussian models can also have heavy-looking finite samples, so kurtosis or one crash alone does not establish regular variation. Threshold choice and uncertainty remain part of the answer."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def pbdh(self):
        st = VGroup(MathTex(r"P(L - u \le y \mid L > u) \;\to\; G_{\xi,\beta(u)}(y) = 1 - \Bigl(1 + \frac{\xi y}{\beta}\Bigr)^{-1/\xi}",
                            font_size=32),
                    wrapped_label('for a distribution in an appropriate maximum domain of attraction, as its threshold approaches the endpoint, the excesses over a high threshold are approximately generalised Pareto; $\\xi > 0$ is a power tail with exponent $1/\\xi$, $\\xi = 0$ exponential, $\\xi < 0$ a finite end point', 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Pickands--Balkema--de Haan (1974--75)", st, r"the theorem behind peaks over threshold",
                            width=11.8, font_size=22)
        with self.voiceover(
            "Peaks over threshold uses a limiting theorem. <bookmark mark='a'/> If the parent distribution lies in a generalized-extreme-value maximum domain of attraction, the conditional excess law approaches a generalized Pareto law with threshold-dependent scale as the threshold approaches the upper endpoint. The approximation is not guaranteed for every distribution or finite cutoff. <bookmark mark='b'/> Positive shape gives a regularly varying power tail, zero an exponential-type limit, negative a finite endpoint. Estimation with dependent observations needs additional mixing or clustering treatment; the marginal theorem itself is not a blanket iid requirement."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.02))
        self.wait(0.5)
        self.clear_scene()

    def pot(self, e):
        rows = [cmath(r"u", r"=", rf"{100 * e['u']:.2f}\%\ \text{{(the 95th percentile of losses)}}", font_size=36),
                cmath(r"\hat\xi,\ \hat\beta", r"=", rf"{e['xi']:.3f},\ {100 * e['beta']:.3f}\%", font_size=40,
                      colors={r"\hat\xi,\ \hat\beta": TAIL_C}),
                cmath(r"1/\hat\xi", r"=", rf"{1 / e['xi']:.1f}", font_size=42),
                cmath(r"\text{VaR}_\alpha", r"=", r"u + \frac\beta\xi\Bigl[\Bigl(\frac{n}{N_u}(1 - \alpha)\Bigr)^{-\xi} - 1\Bigr]",
                      font_size=34, colors={r"\text{VaR}_\alpha": VAR_C})]
        whys = [why(rf"peaks over threshold: keep the {e['n_u']:,} days whose loss exceeded the threshold"),
                why(r"the generalised Pareto fitted to their excesses by maximum likelihood"),
                why('under an extrapolated regularly varying model, moment p is finite for p below 1/xi and infinite above it; boundary cases need more information'),
                why('extrapolated quantiles; require xi < 1 for finite ES, which is $(\\text{VaR} + \\beta - \\xi u)/(1 - \\xi)$')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"Peaks over threshold, on the American market. <bookmark mark='a'/> Take the threshold at the ninety-fifth "
            f"percentile of daily losses, {100 * e['u']:.2f} percent, and keep the {e['n_u']:,} days beyond it. "
            f"<bookmark mark='b'/> Fit the generalised Pareto to their excesses: xi of {e['xi']:.2f}. "
            f"<bookmark mark='c'/> A tail exponent of about {1 / e['xi']:.0f}. <bookmark mark='d'/> And the fitted tail "
            "gives quantiles, and shortfalls, beyond any day in the data."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def survival(self, e):
        s = e["surv"]
        x = 100 * np.asarray(s["x"], float)
        emp = np.log10(np.asarray(s["emp"], float))
        fit = np.log10(np.asarray(s["fit"], float))
        g = axes([np.log10(1.5), np.log10(20)], [-3.6, 0], x_length=7.0, y_length=4.2, xlabel=r"daily loss, \% (log scale)",
                 ylabel=r"share of exceedances beyond it", xticks=[np.log10(2), np.log10(5), np.log10(10), np.log10(20)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}",
                 font_size=16).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        ok = (x > 1.5) & (x < 20)
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), b), radius=0.05, color=DATA_C) for a, b in zip(x[ok], emp[ok])])
        line = curve(ax, np.log10(x[ok]), fit[ok], TAIL_C, stroke_width=3)
        leg = legend([(DATA_C, rf"the {e['n_u']:,} worst days"), (TAIL_C, r"generalised Pareto fit")], font_size=18)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 2.0)
        with self.voiceover(
            "How well it fits. <bookmark mark='a'/> On logarithmic scales, the share of exceedances beyond each loss: the "
            "data fall along a slightly curving line. <bookmark mark='b'/> The fitted Pareto follows them out to the "
            "nineteen eighty-seven crash, the single point at the end."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(Create(line))
        self.wait(0.4)
        self.clear_scene()

    def sweep(self, unused=None):
        head=label('Threshold choice and uncertainty',font_size=29).to_edge(UP,buff=0.35)
        cards=VGroup(
            desk_question('lower cutoff','More excesses, potentially greater GPD approximation bias.',width=12.0,font_size=23),
            desk_question('higher cutoff','Fewer excesses, greater sampling variability; inspect dependence as well as fit.',width=12.0,font_size=23),
            desk_question('no successful sweep reported','The combined extra output is omitted. No retry or substitute historical fit; threshold stability would be a diagnostic, not proof.',width=12.0,font_size=23)
        ).arrange(DOWN,buff=0.28).next_to(head,DOWN,buff=0.35)
        with self.voiceover("Threshold choice trades data against approximation. A lower cutoff supplies more excesses and can add bias. <bookmark mark='a'/> A higher cutoff leaves fewer observations, so dependence and sampling variability matter. <bookmark mark='b'/> The combined extra original was blocked and returned no approved output. Its historical sweep is omitted, without retry or substitute fit. A future authorized analysis would inspect shape stability and uncertainty; apparent stability alone would not prove a tail law.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def beyond(self, e):
        hx = [-4.2, -1.4, 1.4, 4.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"confidence", r"normal VaR / ES",
                                                                         r"historical VaR / ES", r"EVT VaR / ES")])
        tab = VGroup(head)
        for r in e["rows"]:
            a = r["alpha"]
            tab.add(VGroup(MathTex(rf"{100 * a:g}\%", font_size=26),
                           MathTex(rf"{100 * r['normal'][0]:.1f} / {100 * r['normal'][1]:.1f}", font_size=24, color=MODEL_C),
                           MathTex(rf"{100 * r['hs'][0]:.1f} / {100 * r['hs'][1]:.1f}", font_size=24, color=DATA_C),
                           MathTex(rf"{100 * r['evt'][0]:.1f} / {100 * r['evt'][1]:.1f}", font_size=24, color=TAIL_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        r99, r9999 = e["rows"][0], e["rows"][-1]
        with self.voiceover(
            f"Model extrapolation beyond observed losses. <bookmark mark='a'/> At ninety-nine percent the fitted EVT VaR is {100*r99['evt'][0]:.1f} percent and the historical estimate {100*r99['hs'][0]:.1f}, compared with normal {100*r99['normal'][0]:.1f}. <bookmark mark='b'/> At ninety-nine point nine nine percent, the nominal exceedance rate is one in ten thousand trading days, about forty years at two hundred and fifty-two days a year. EVT gives {100*r9999['evt'][0]:.1f} percent VaR and {100*r9999['evt'][1]:.1f} percent ES. Only a few observations inform this region, and no confidence interval is computed here. Fitted positive-shape tails increasingly diverge from Gaussian extrapolation; the data do not prove either limiting model."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def hill(self, e):
        ks = np.asarray(e["hill_k"], float)
        h = np.asarray(e["hill"], float)
        g = axes([np.log10(20), np.log10(2000)], [1.5, 6], x_length=7.0, y_length=4.0, xlabel=r"largest losses used, $k$",
                 ylabel=r"Hill's tail exponent", xticks=[np.log10(25), np.log10(100), np.log10(400), np.log10(1600)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[2, 3, 4, 5], font_size=16).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, np.log10(ks), h, TAIL_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), b), radius=0.07, color=TAIL_C) for a, b in zip(ks, h)])
        ref = DashedLine(ax.c2p(np.log10(20), 1 / e["xi"]), ax.c2p(np.log10(2000), 1 / e["xi"]), color=GREY_B)
        with self.voiceover(
            f"Hill estimates a power-tail exponent using the k largest positive losses relative to the next order statistic, the k-plus-first cutoff in this implementation. <bookmark mark='a'/> That convention differs from dividing by the kth largest value. It presumes a positive regularly varying tail and suitable asymptotic threshold growth. <bookmark mark='b'/> The cached estimate is {h[2]:.1f} at one hundred observations and {h[-1]:.1f} at sixteen hundred. Drift across k signals threshold sensitivity and a bias-variance tradeoff. These estimates do not establish finite variance or other population moments from one sample."
        ) as vo:
            self.play(FadeIn(g), Create(ref))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots))
            vo.wait_until("b")
            self.play(Indicate(dots[2], color=HURDLE))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, unused=None):
        head=label('Comparing tail estimates',font_size=29).to_edge(UP,buff=0.35)
        cards=VGroup(
            desk_question('align definitions','Simple returns and log returns differ; sample periods, frequencies and thresholds must be stated.',width=12.0,font_size=23),
            desk_question('compare uncertainty','Finite tail samples and threshold choice can dominate a difference between estimated shapes.',width=12.0,font_size=23),
            desk_question('no cross-market ranking here','The combined extra output is unavailable; no Bitcoin tail result or new historical fit is presented.',width=12.0,font_size=23)
        ).arrange(DOWN,buff=0.28).next_to(head,DOWN,buff=0.35)
        with self.voiceover("Cross-market tail comparisons require aligned definitions. A simple daily US return and a Bitcoin log return use different transformations and sample spans. <bookmark mark='a'/> Differences in a fitted shape can reflect threshold and sampling uncertainty rather than an identified population ordering. <bookmark mark='b'/> The combined extra output is unavailable, so no Bitcoin tail table or substitute historical fit is presented. A successful finite fit would still not establish an exact asymptotic exponent or moment boundary.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def mcneil(self):
        rows = [cmath(r"r_t", r"=", r"\mu_t + \sigma_t z_t", font_size=44),
                cmath(r"\sigma_t", r":", r"\text{GJR-GARCH, fitted}", font_size=40, colors={r"\sigma_t": MODEL_C}),
                cmath(r"z_t", r":", r"\text{generalised Pareto beyond the 90th percentile}", font_size=36,
                      colors={r"z_t": TAIL_C}),
                cmath(r"\text{VaR}_t", r"=", r"-\mu_t + \sigma_t\,\text{VaR}_\alpha(-z)", font_size=40, colors={r"\text{VaR}_t": VAR_C})]
        whys = [why('McNeil and Frey (2000): location-scale return model; iid standardized shocks are an assumption to check'),
                why(r"so model the volatility, Part 7's GARCH, to make the shocks nearly independent"),
                why('fit the residual loss tail, checking remaining dependence and threshold uncertainty'),
                why(r"Chapter 3's sixth forecaster: its exceptions did not cluster, but it was too cautious at 99\%")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "McNeil and Frey's conditional tail approach assumes a return location plus volatility times a standardized shock. <bookmark mark='a'/> Volatility filtering aims to remove changing scale; it does not guarantee independent residuals. <bookmark mark='b'/> Fit a generalized Pareto model to high residual losses. <bookmark mark='c'/> In positive-loss convention the quantile is minus location plus volatility times the quantile of minus the shock, not plus the return mean. <bookmark mark='d'/> The cached implementation omits the time-varying location term in its final forecast, uses periodic fits and has the initialization limitation already stated; it is an illustrative implementation rather than a certified reproduction."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def cautions(self):
        cards = VGroup(
            desk_question(r"the threshold is a choice", r"too low and the Pareto is wrong; too high and it is noise: fits "
                          r"and Hill plots across thresholds are part of the answer", width=12.4, font_size=19),
            desk_question('dependence needs treatment', 'the marginal excess limit and dependent-sample inference are different questions; filtering does not guarantee iid shocks', width=12.4, font_size=19),
            desk_question(r"extrapolation is a model", r"EVT gives the best guess beyond the data, not knowledge of it; its "
                          r"confidence intervals at 99.99\% are wide", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> Threshold choice trades approximation bias against sampling noise. <bookmark mark='b'/> The marginal excess theorem differs from dependent-sample inference; residual clustering, mixing assumptions or declustering can matter even after filtering. <bookmark mark='c'/> Extrapolation remains a model assumption with uncertainty. No interval calculated in this lecture certifies a remote-tail probability or a universal moment boundary."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"bank stocks and insurance stocks have a daily correlation of about 0.8. A Gaussian model says that "
                       r"on banks' worst 1\% of days, insurers have their worst 1\% about 40\% of the time. What do the "
                       r"data say?")
        with self.voiceover(
            "Pause and predict. Bank stocks and insurance stocks have a daily correlation of about nought point eight. A "
            "Gaussian model says that on banks' worst one percent of days, insurers have their own worst one percent about "
            "forty percent of the time. What do the data say?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
