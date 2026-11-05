from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
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
        self.sweep(load("extra"))
        self.beyond(e)
        self.hill(e)
        self.tails(load("extra"))
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
                why(r"far tails fall like a power of the loss, not like $e^{-x^2/2}$: the tail exponent $\zeta$ is what "
                    r"matters, and it is estimable")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"The tails. <bookmark mark='a'/> Daily American returns since nineteen twenty-six have an excess kurtosis of "
            f"{e['kurt']:.0f}, where a normal has zero. <bookmark mark='b'/> The worst day lost {100 * e['worst']:.1f} "
            "percent. <bookmark mark='c'/> Far tails fall like a power of the loss, not like the normal's exponential of "
            "a square, and the power, the tail exponent, can be estimated."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def pbdh(self):
        st = VGroup(MathTex(r"P(L - u \le y \mid L > u) \;\to\; G_{\xi,\beta(u)}(y) = 1 - \Bigl(1 + \frac{\xi y}{\beta}\Bigr)^{-1/\xi}",
                            font_size=32),
                    wrapped_label(r"for almost any distribution used in finance, the excesses over a high threshold are "
                                  r"approximately generalised Pareto; $\xi > 0$ is a power tail with exponent $1/\xi$, "
                                  r"$\xi = 0$ exponential, $\xi < 0$ a finite end point", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Pickands--Balkema--de Haan (1974--75)", st, r"the theorem behind peaks over threshold",
                            width=11.8, font_size=22)
        with self.voiceover(
            "The theorem that makes this possible. <bookmark mark='a'/> For almost any distribution, the excesses over a "
            "high threshold are approximately generalised Pareto, with shape xi and scale beta. <bookmark mark='b'/> A "
            "positive xi is a power tail with exponent one over xi; zero, an exponential tail; negative, a tail that ends. "
            "It plays for extremes the role the central limit theorem plays for sums."
        ) as vo:
            vo.wait_until("a")
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
                why(r"a tail exponent of about five: the fifth moment is infinite, the fourth barely finite"),
                why(r"quantiles beyond the data from the fitted tail; ES is $(\text{VaR} + \beta - \xi u)/(1 - \xi)$")]
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
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def survival(self, e):
        s = e["surv"]
        x = 100 * np.asarray(s["x"], float)
        emp = np.log10(np.asarray(s["emp"], float))
        fit = np.log10(np.asarray(s["fit"], float))
        g = axes([np.log10(1.5), np.log10(20)], [-3.4, 0], x_length=7.0, y_length=4.2, xlabel=r"daily loss, \% (log scale)",
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

    def sweep(self, x):
        hx = [-3.6, -0.8, 1.8, 4.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"threshold, loss percentile", r"threshold",
                                                                         r"exceedances", r"$\hat\xi$")])
        tab = VGroup(head)
        for r in x["sweep"]:
            tab.add(VGroup(MathTex(rf"{100 * r['q']:g}\%", font_size=26), MathTex(rf"{100 * r['u']:.2f}\%", font_size=26),
                           MathTex(f"{r['n_u']:,}".replace(",", "{,}"), font_size=26),
                           MathTex(f"{r['xi']:.3f}", font_size=26, color=TAIL_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        lo = min(r["xi"] for r in x["sweep"])
        hi = max(r["xi"] for r in x["sweep"])
        with self.voiceover(
            "Does the answer depend on the threshold? <bookmark mark='a'/> Move it from the ninetieth to the ninety-ninth "
            "percentile, and the number of exceedances falls from about two and a half thousand to two hundred and "
            f"fifty. <bookmark mark='b'/> The fitted shape stays between {lo:.2f} and {hi:.2f}. When the estimate is "
            "stable across thresholds, the generalised Pareto has found the tail, not the threshold."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r_[3] for r_ in tab[1:]]), color=TAIL_C))
        self.wait(0.4)
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
            "Beyond the data. <bookmark mark='a'/> At ninety-nine percent, EVT and history agree, "
            f"{100 * r99['evt'][0]:.1f} and {100 * r99['hs'][0]:.1f} percent, while the normal says "
            f"{100 * r99['normal'][0]:.1f}. <bookmark mark='b'/> At ninety-nine point nine nine, a day in forty years, "
            f"history has only two or three points; EVT extrapolates {100 * r9999['evt'][0]:.1f} percent with a shortfall "
            f"of {100 * r9999['evt'][1]:.1f}; the normal still says {100 * r9999['normal'][0]:.1f}. The normal's error "
            "grows without limit as the confidence rises."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def hill(self, e):
        ks = np.asarray(e["hill_k"], float)
        h = np.asarray(e["hill"], float)
        g = axes([np.log10(20), np.log10(2000)], [1.5, 5], x_length=7.0, y_length=4.0, xlabel=r"largest losses used, $k$",
                 ylabel=r"Hill's tail exponent", xticks=[np.log10(25), np.log10(100), np.log10(400), np.log10(1600)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[2, 3, 4, 5], font_size=16).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, np.log10(ks), h, TAIL_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), b), radius=0.07, color=TAIL_C) for a, b in zip(ks, h)])
        ref = DashedLine(ax.c2p(np.log10(20), 1 / e["xi"]), ax.c2p(np.log10(2000), 1 / e["xi"]), color=GREY_B)
        with self.voiceover(
            "A second estimate, Bruce Hill's. <bookmark mark='a'/> From the k largest losses, the tail exponent is one "
            "over the mean log ratio of each to the k-th. <bookmark mark='b'/> With the hundred largest it says about "
            f"{h[2]:.1f}; with sixteen hundred, {h[-1]:.1f}. The estimate drifts with k, the bias against variance "
            "trade-off of every tail estimator. Somewhere between three and five, the classic answer for stocks: fat, "
            "but with a finite variance."
        ) as vo:
            self.play(FadeIn(g), Create(ref))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots))
            vo.wait_until("b")
            self.play(Indicate(dots[2], color=HURDLE))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, x):
        t = x["tails"]
        hx = [-3.4, -0.4, 2.2, 4.6]
        head = VGroup(*[label(s_, font_size=16, color=GREY_B) for s_ in (r"tail", r"days", r"GPD $\hat\xi$",
                                                                           r"Hill, $k = 5\%$ of days")])
        tab = VGroup(head)
        for key, nm in (("us_left", r"US market, losses"), ("us_right", r"US market, gains"),
                        ("btc_left", r"Bitcoin 2017--20, losses"), ("btc_right", r"Bitcoin 2017--20, gains")):
            v = t[key]
            tab.add(VGroup(label(nm, font_size=18), MathTex(f"{v['n']:,}".replace(",", "{,}"), font_size=24),
                           MathTex(f"{v['xi']:+.2f}", font_size=26, color=TAIL_C), MathTex(f"{v['hill100']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        ul, ur = t["us_left"], t["us_right"]
        bl, br = t["btc_left"], t["btc_right"]
        with self.voiceover(
            "Other tails. <bookmark mark='a'/> The American market's gains are as fat-tailed as its losses, fatter by the "
            f"fitted shape, {ur['xi']:.2f} against {ul['xi']:.2f}: its biggest up days came inside its crises, in the "
            "nineteen thirties and in twenty oh eight. <bookmark mark='b'/> Bitcoin's losses from twenty seventeen to "
            f"twenty twenty have a shape of {bl['xi']:.2f}, while its gains' estimate, {br['xi']:+.2f}, comes from only "
            "sixty-two days: a reminder that a tail estimate from four years is mostly noise."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def mcneil(self):
        rows = [cmath(r"r_t", r"=", r"\mu_t + \sigma_t z_t", font_size=44),
                cmath(r"\sigma_t", r":", r"\text{GJR-GARCH, fitted}", font_size=40, colors={r"\sigma_t": MODEL_C}),
                cmath(r"z_t", r":", r"\text{generalised Pareto beyond the 90th percentile}", font_size=36,
                      colors={r"z_t": TAIL_C}),
                cmath(r"\text{VaR}_t", r"=", r"\mu_t + \sigma_t\,\text{VaR}(z)", font_size=40, colors={r"\text{VaR}_t": VAR_C})]
        whys = [why(r"McNeil and Frey (2000): returns are a volatility times an iid shock"),
                why(r"so model the volatility, Part 7's GARCH, to make the shocks nearly independent"),
                why(r"then fit the tail of the shocks, where EVT's assumptions hold far better than for raw returns"),
                why(r"Chapter 3's sixth forecaster: its exceptions did not cluster, but it was too cautious at 99\%")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "EVT for a forecast, after Alexander McNeil and Rüdiger Frey. <bookmark mark='a'/> A return is a volatility "
            "times an independent shock. <bookmark mark='b'/> Model the volatility with GARCH, so the shocks are nearly "
            "independent, <bookmark mark='c'/> and fit the shocks' tail with the generalised Pareto, where the theory's "
            "assumptions hold. <bookmark mark='d'/> That was Chapter three's sixth forecaster: its exceptions did not "
            "cluster, but at ninety-nine percent it was too cautious."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def cautions(self):
        cards = VGroup(
            desk_question(r"the threshold is a choice", r"too low and the Pareto is wrong; too high and it is noise: fits "
                          r"and Hill plots across thresholds are part of the answer", width=12.4, font_size=19),
            desk_question(r"dependence breaks the theory", r"raw returns cluster; the theorem is for independent draws, "
                          r"which is why McNeil and Frey filter first", width=12.4, font_size=19),
            desk_question(r"extrapolation is a model", r"EVT gives the best guess beyond the data, not knowledge of it; its "
                          r"confidence intervals at 99.99\% are wide", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> The threshold is a choice: too low and the Pareto does not apply, too "
            "high and there is too little data. <bookmark mark='b'/> Dependence breaks the theory, which is why McNeil "
            "and Frey filter first. <bookmark mark='c'/> And extrapolation is still a model: the best guess beyond the "
            "data, with wide uncertainty, not knowledge of it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
