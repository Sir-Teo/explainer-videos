from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (boxed, density, gauss_pdf, hist_shape, label, load, mtex, note, num, pdf_curve,
                                      polyline)
from videos.stochastic.compute import COIN_DOWN, COIN_UP, GBM_MU, GBM_SIGMA

LN10 = math.log(10)


class LogAxes(Axes):
    """Time on x, natural-log wealth on y, labeled in powers of ten.  The labels and grid are built on first access,
    after the axes have been positioned."""

    def __init__(self, T, y_lo, y_hi, powers, **kwargs):
        super().__init__(x_range=[0, T, T / 4], y_range=[y_lo, y_hi, 1], tips=False,
                         axis_config={"stroke_color": GREY_B, "include_ticks": False}, **kwargs)
        self._T, self._lo, self._hi, self._powers = T, y_lo, y_hi, [k for k in powers if y_lo <= k * LN10 <= y_hi]
        self._deco = None

    def _build(self):
        if self._deco is None:
            T, lo = self._T, self._lo
            yl = VGroup(*[MathTex(r"\times" + ("1" if k == 0 else rf"10^{{{k}}}"), font_size=24, color=GREY_A)
                          .next_to(self.c2p(0, k * LN10), LEFT, buff=0.12) for k in self._powers])
            grid = VGroup(*[DashedLine(self.c2p(0, k * LN10), self.c2p(T, k * LN10), color=GREY_D, stroke_width=1,
                                       dash_length=0.06) for k in self._powers])
            xl = VGroup(MathTex("0", font_size=24).next_to(self.c2p(0, lo), DOWN, buff=0.12),
                        MathTex(f"{T:g}", font_size=24).next_to(self.c2p(T, lo), DOWN, buff=0.12))
            self._deco = (yl, grid, xl)
        return self._deco

    @property
    def y_labels(self):
        return self._build()[0]

    @property
    def grid(self):
        return self._build()[1]

    @property
    def x_labels(self):
        return self._build()[2]


def log_axes(T, y_lo, y_hi, x_length=9.0, y_length=5.2, powers=None) -> LogAxes:
    return LogAxes(T, y_lo, y_hi, powers or [], x_length=x_length, y_length=y_length)


def column(group: Mobject, left=1.7, right=6.9, top=3.5) -> Mobject:
    """Left-align ``group`` at x = left, shrink it to end before x = right, and hang it from y = top."""
    if group.width > right - left:
        group.scale_to_fit_width(right - left)
    group.align_to([left, 0, 0], LEFT)
    group.align_to([0, top, 0], UP)
    return group


class GeometricBM(VoiceoverScene):
    def construct(self):
        self.coin_game()
        self.naive()
        self.solve()
        self.verify()
        self.drag()

    # ------------------------------------------------------------------
    def coin_game(self):
        d = load("coin")
        T = d["paths"].shape[1] - 1
        ts = np.arange(T + 1)
        ax = log_axes(T, -14, 8, x_length=6.6, y_length=5.6, powers=[-6, -4, -2, 0, 2, 3]).to_edge(LEFT, buff=1.2)
        ax.shift(DOWN * 0.3)
        xl = label(r"round", font_size=24, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
        rules = VGroup(
            label(r"heads: wealth $\times 1.5$", font_size=30),
            label(r"tails: wealth $\times 0.6$", font_size=30),
            MathTex(r"\text{average multiplier: } \tfrac12(1.5 + 0.6) = 1.05", font_size=32, color=C.MEAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        column(rules, top=3.5)
        one = polyline(ax, ts, d["paths"][0], color=C.BROWNIAN, stroke_width=2.5)
        fan = VGroup(*[polyline(ax, ts, p, color=C.BROWNIAN, stroke_width=1.1).set_stroke(opacity=0.28)
                       for p in d["paths"][1:]])
        pct = d["pct"]
        band = Polygon(*[ax.c2p(t, y) for t, y in zip(ts, pct[1])], *[ax.c2p(t, y) for t, y in zip(ts[::-1], pct[3][::-1])],
                       stroke_width=0, fill_color=C.MEDIAN, fill_opacity=0.18)
        med = polyline(ax, ts, d["theory_median"], color=C.MEDIAN, stroke_width=4)
        mean = DashedLine(ax.c2p(0, 0), ax.c2p(T, d["theory_mean"][-1]), color=C.MEAN, stroke_width=3.5, dash_length=0.12)
        smean = polyline(ax, ts, d["sample_mean"], color=C.MEAN, stroke_width=2.5).set_stroke(opacity=0.7)
        mean_l = MathTex(r"1.05^{n}", font_size=28, color=C.MEAN).next_to(ax.c2p(T, d["theory_mean"][-1]), UP, buff=0.12)
        med_l = MathTex(r"0.9^{n/2}", font_size=28, color=C.MEDIAN).next_to(ax.c2p(T, d["theory_median"][-1]), RIGHT, buff=0.12)
        lost, lost_exact = (float(x) for x in d["lost"])
        e_end = math.exp(d["theory_mean"][-1])
        m_end = math.exp(d["theory_median"][-1])
        s_end = math.exp(d["sample_mean"][-1])
        assert round(e_end, 1) == 131.5 and round(100 * m_end, 1) == 0.5 and round(100 * lost) == 87 and round(s_end) == 52
        stats = VGroup(
            MathTex(rf"\text{{expected after 100: }}\times{e_end:.1f}", font_size=28, color=C.MEAN),
            MathTex(rf"\text{{median after 100: }}\times{m_end:.4f}", font_size=28, color=C.MEDIAN),
            MathTex(rf"\text{{players who lost money: }}{100 * lost:.0f}\%", font_size=28),
            MathTex(rf"\text{{average of our 10{{,}}000: }}\times{s_end:.0f}", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        column(stats, top=rules.get_bottom()[1] - 0.5)
        sim = note(r"10{,}000 simulated players; 80 shown").to_corner(DR, buff=0.3)

        with self.voiceover(
            "Itô's lemma has consequences you can feel in your wallet. Here's a game. <bookmark mark='h'/> You start with "
            "a hundred dollars and flip a coin. Heads, your wealth grows by fifty percent. Tails, it shrinks by forty "
            "percent. <bookmark mark='m'/> On average, each round multiplies your money by 1.05: an expected gain of five "
            "percent per round. Should you play?"
        ) as vo:
            vo.wait_until("h")
            self.play(FadeIn(rules[:2]))
            vo.wait_until("m")
            self.play(Write(rules[2]))
        with self.voiceover(
            "Here's one player over a hundred rounds, on a logarithmic scale. <bookmark mark='f'/> And here are eighty "
            "more, out of ten thousand we simulated. <bookmark mark='e'/> The expected wealth really does grow by five "
            "percent a round, to 131 and a half times the stake after a hundred rounds. <bookmark mark='d'/> But the typical player "
            "goes down, and down, and down. After a hundred rounds, the median player has half a percent of their money "
            "left, and 87 percent of the players lost money."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.y_labels), FadeIn(ax.grid), FadeIn(ax.x_labels), FadeIn(xl))
            self.play(Create(one), run_time=2)
            vo.wait_until("f")
            self.play(LaggedStart(*[Create(p) for p in fan], lag_ratio=0.02), FadeIn(sim), run_time=2.5)
            vo.wait_until("e")
            self.play(Create(mean), FadeIn(mean_l), FadeIn(stats[0]))
            vo.wait_until("d")
            self.play(FadeIn(band), Create(med), FadeIn(med_l), FadeIn(stats[1]))
            self.play(FadeIn(stats[2]))
        with self.voiceover(
            "The average is held up by a handful of spectacularly lucky players, so rare that even the average of our "
            "ten thousand <bookmark mark='s'/> only reaches 52 times the stake, not 131. <bookmark mark='w'/> The reason "
            "is simple: one heads and one tails multiply your wealth by 1.5 times 0.6, which is 0.9. You lose ten percent "
            "every two rounds. For a typical path, what matters is the average of the logarithm, not the logarithm of "
            "the average."
        ) as vo:
            vo.wait_until("s")
            self.play(Create(smean), FadeIn(stats[3]))
            vo.wait_until("w")
            pair = MathTex(r"1.5 \times 0.6 = 0.9", font_size=36, color=C.MEDIAN).next_to(stats, DOWN, buff=0.35)
            pair.align_to(stats, LEFT)
            self.play(Write(pair))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def naive(self):
        sde = MathTex(r"dS", r"=", r"\mu S\,dt", r"+", r"\sigma S\,dW", font_size=48).to_edge(UP, buff=0.5)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        gbm = label(r"geometric Brownian motion: returns are noisy, not prices", font_size=28, color=GREY_A)
        gbm.next_to(sde, DOWN, buff=0.15)
        params = MathTex(rf"\mu = {GBM_MU:g} \;(5\%), \qquad \sigma = {GBM_SIGMA:g} \;(45\%)", font_size=32)
        params.next_to(gbm, DOWN, buff=0.25)
        coin_note = note(r"the coin game's mean return and its standard deviation per round").next_to(params, DOWN, buff=0.1)
        g1 = MathTex(r"S_t", r"\overset{?}{=}", r"S_0\, e^{\mu t + \sigma W_t}", font_size=44).move_to(DOWN * 0.3)
        chk = MathTex(r"d\big(S_0 e^{\mu t + \sigma W_t}\big)", r"=", r"S\,\big(\mu\,dt", r"+", r"\sigma\,dW",
                      r"+", r"\tfrac12\sigma^2\,dt\big)", font_size=40).next_to(g1, DOWN, buff=0.5)
        chk[2].set_color(C.DRIFT)
        chk[4].set_color(C.BROWNIAN)
        chk[6].set_color(C.QV)
        why = label(r"It\^o: $f_t = \mu f$, \ $f_w = \sigma f$, \ $f_{ww} = \sigma^2 f$", font_size=26, color=GREY_B)
        why.next_to(chk, DOWN, buff=0.25)
        wrong = label(r"an extra $\tfrac12\sigma^2 S\,dt$: \ not our equation", font_size=30, color=C.RIGHT_PT)
        wrong.next_to(why, DOWN, buff=0.3)
        with self.voiceover(
            "Now the continuous version. <bookmark mark='s'/> Let a price S have returns made of a drift, mu d t, plus "
            "noise, sigma d W. That's geometric Brownian motion, the standard model of a stock price. "
            "<bookmark mark='p'/> To match the coin game, take mu equal to five percent and sigma equal to forty-five "
            "percent per round: the game's average return and its standard deviation."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(sde), FadeIn(gbm))
            vo.wait_until("p")
            self.play(FadeIn(params), FadeIn(coin_note))
        with self.voiceover(
            "Ordinary calculus suggests a solution: <bookmark mark='g'/> S equals S zero times e to the mu t plus sigma W. "
            "<bookmark mark='c'/> But check it with Itô's lemma. The function e to the mu t plus sigma w has time "
            "derivative mu f, slope sigma f, and curvature sigma squared f. So its change is S times mu d t, plus sigma d "
            "W, <bookmark mark='x'/> plus one half sigma squared d t. That extra term means the guess solves a different "
            "equation."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(g1))
            vo.wait_until("c")
            self.play(Write(chk[:5]), FadeIn(why))
            vo.wait_until("x")
            self.play(Write(chk[5:]))
            self.play(FadeIn(wrong))
        self.wait(0.4)
        self.play(FadeOut(VGroup(g1, chk, why, wrong, params, coin_note, gbm)), sde.animate.to_corner(UL, buff=0.45))
        self.sde = sde

    # ------------------------------------------------------------------
    def solve(self):
        l1 = MathTex(r"d(\ln S)", r"=", r"\frac{1}{S}\,dS", r"-", r"\frac{1}{2}\frac{1}{S^2}\,(dS)^2", font_size=42)
        l1[4].set_color(C.QV)
        l2 = MathTex(r"d(\ln S)", r"=", r"\big(\mu\,dt + \sigma\,dW\big)", r"-", r"\tfrac12\sigma^2\,dt", font_size=42)
        l2[4].set_color(C.QV)
        l3 = MathTex(r"\ln S_t", r"=", r"\ln S_0", r"+", r"\big(\mu - \tfrac12\sigma^2\big)\,t", r"+", r"\sigma W_t",
                     font_size=42)
        l3[4].set_color(C.DRIFT)
        l3[6].set_color(C.BROWNIAN)
        col = VGroup(l1, l2, l3).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        for m in (l2, l3):
            m.shift((l1[1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        ito_note = label(r"It\^o with $f(s) = \ln s$: \ $f' = 1/s$, \ $f'' = -1/s^2$", font_size=26, color=GREY_B)
        ito_note.to_corner(UR, buff=0.45)
        dsq = label(r"$(dS)^2 = \sigma^2 S^2\,dt$", font_size=26, color=C.QV).next_to(ito_note, DOWN, buff=0.15).align_to(ito_note, LEFT)
        sol = MathTex(r"S_t", r"=", r"S_0\,\exp\!\Big(\big(\mu - \tfrac12\sigma^2\big)\,t", r"+", r"\sigma W_t\Big)",
                      font_size=48)
        sol[2].set_color(C.DRIFT)
        sol[4].set_color(C.BROWNIAN)
        sb = boxed(sol, color=C.QV, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The way to solve it is to look at the logarithm. <bookmark mark='a'/> Apply Itô's lemma to log S: one over "
            "S, times d S, minus one half, one over S squared, times d S squared. <bookmark mark='b'/> d S squared is sigma "
            "squared S squared d t, by the multiplication table. <bookmark mark='c'/> So the change in log S is mu d t plus "
            "sigma d W, minus one half sigma squared d t. Constant coefficients: we can integrate directly."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(ito_note))
            vo.wait_until("b")
            self.play(FadeIn(dsq))
            vo.wait_until("c")
            self.play(Write(l2))
        with self.voiceover(
            "Log S grows at the rate mu minus one half sigma squared, plus sigma times W. <bookmark mark='s'/> And the "
            "price is S zero, times e to the mu minus one half sigma squared, t, plus sigma W. The one half sigma squared "
            "is Itô's correction, and it's exactly what the naive guess was missing."
        ) as vo:
            self.play(Write(l3))
            vo.wait_until("s")
            self.play(Write(sol), Create(sb[0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verify(self):
        d = load("gbm")
        t, em, ito, naive = d["one_t"], d["one_em"], d["one_ito"], d["one_naive"]
        T = float(t[-1])
        ax = log_axes(T, -9, 9, x_length=10.0, y_length=5.0, powers=[-3, -2, -1, 0, 1, 2, 3]).move_to(DOWN * 0.5 + RIGHT * 0.3)
        c_em = polyline(ax, t, em, color=WHITE, stroke_width=7).set_stroke(opacity=0.35)
        c_ito = polyline(ax, t, ito, color=C.QV, stroke_width=2.5)
        c_naive = polyline(ax, t, naive, color=C.RIGHT_PT, stroke_width=2.5)
        leg = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=WHITE, stroke_width=7).set_stroke(opacity=0.35),
                   label(r"simulate $dS = \mu S\,dt + \sigma S\,dW$ directly (1{,}000{,}000 Euler steps)", font_size=26)),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.RIGHT_PT, stroke_width=3),
                   MathTex(r"S_0 e^{\mu t + \sigma W_t}", r"\quad\text{(naive)}", font_size=30, color=C.RIGHT_PT)),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.QV, stroke_width=3),
                   MathTex(r"S_0 e^{(\mu - \sigma^2/2) t + \sigma W_t}", r"\quad\text{(It\^o)}", font_size=30, color=C.QV)),
        )
        for g in leg:
            g.arrange(RIGHT, buff=0.2)
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4)
        factor = math.exp(naive[-1] - em[-1])
        assert 20_000 < factor < 30_000, factor
        with self.voiceover(
            "Let's check that numerically. <bookmark mark='e'/> Simulate the equation directly, one small step at a time, a "
            "million steps, with one fixed sequence of random kicks. <bookmark mark='n'/> The naive formula, driven by the "
            "same kicks, flies off: after a hundred rounds it's too big by a factor of about twenty-five thousand. "
            "<bookmark mark='i'/> Itô's formula sits right on top of the simulation."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.y_labels), FadeIn(ax.grid), FadeIn(ax.x_labels))
            vo.wait_until("e")
            self.play(Create(c_em), FadeIn(leg[0]), run_time=2)
            vo.wait_until("n")
            self.play(Create(c_naive), FadeIn(leg[1]), run_time=2)
            vo.wait_until("i")
            self.play(Create(c_ito), FadeIn(leg[2]), run_time=2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drag(self):
        d = load("gbm")
        tt, logS, pct = d["tt"], d["paths"], d["pct"]
        T = float(tt[-1])
        mu, sig = GBM_MU, GBM_SIGMA
        g = mu - 0.5 * sig**2
        ax = log_axes(T, -14, 10, x_length=6.2, y_length=5.6, powers=[-6, -4, -2, 0, 2, 4]).to_edge(LEFT, buff=1.1)
        ax.shift(DOWN * 0.3)
        fan = VGroup(*[polyline(ax, tt, p, color=C.BROWNIAN, stroke_width=1.0).set_stroke(opacity=0.25) for p in logS[:80]])
        band = Polygon(*[ax.c2p(t, y) for t, y in zip(tt, pct[1])], *[ax.c2p(t, y) for t, y in zip(tt[::-1], pct[3][::-1])],
                       stroke_width=0, fill_color=C.MEDIAN, fill_opacity=0.18)
        med = Line(ax.c2p(0, 0), ax.c2p(T, g * T), color=C.MEDIAN, stroke_width=4)
        mean = DashedLine(ax.c2p(0, 0), ax.c2p(T, mu * T), color=C.MEAN, stroke_width=3.5, dash_length=0.12)
        hax = Axes(x_range=[0, 0.12, 0.05], y_range=[-14, 10, 1], x_length=1.4, y_length=5.6, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).next_to(ax, RIGHT, buff=0.1)
        hax.x_axis.set_opacity(0)
        edges = np.linspace(-14, 10, 49)
        hist = hist_shape(hax, edges, density(d["final"], edges), sideways=True, color=C.PDF)
        ys = np.linspace(-14, 10, 200)
        curve = pdf_curve(hax, ys, gauss_pdf(ys, g * T, sig**2 * T), sideways=True, color=WHITE, stroke_width=2)
        formulas = VGroup(
            MathTex(r"\mathbb E[S_t]", r"=", r"S_0\, e^{\mu t}", font_size=36),
            MathTex(r"\text{median}(S_t)", r"=", r"S_0\, e^{(\mu - \frac12\sigma^2)\, t}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        formulas[0].set_color(C.MEAN)
        formulas[1].set_color(C.MEDIAN)
        why_mean = label(r"because $\mathbb E\big[e^{\sigma W_t}\big] = e^{\frac12\sigma^2 t}$: \ the lucky tail",
                         font_size=24, color=GREY_B).next_to(formulas, DOWN, buff=0.2).align_to(formulas, LEFT)
        rate = MathTex(r"\mu - \tfrac12\sigma^2", r"=", rf"{mu:g} - \tfrac12({sig:g})^2", r"=", rf"{100 * g:.1f}\%",
                       font_size=32, color=C.MEDIAN).next_to(why_mean, DOWN, buff=0.4).align_to(formulas, LEFT)
        coin_rate = 0.5 * math.log(COIN_UP * COIN_DOWN)
        cr = label(rf"the coin game: $\tfrac12 \ln 0.9 = {100 * coin_rate:.1f}\%$ per round", font_size=26,
                   color=GREY_A).next_to(rate, DOWN, buff=0.2).align_to(formulas, LEFT)
        below, below_exact = (float(x) for x in d["below"])
        bl = label(rf"below the start at $t = 100$:\\{100 * below:.1f}\% \ (exact: {100 * below_exact:.1f}\%)",
                   font_size=26, tex_environment="flushleft").next_to(cr, DOWN, buff=0.3).align_to(formulas, LEFT)
        column(VGroup(formulas, why_mean, rate, cr, bl), left=hax.get_right()[0] + 0.3, top=3.4)
        drag = label(r"volatility drag: noise lowers the typical growth rate by $\tfrac12\sigma^2$", font_size=30,
                     color=C.QV).to_edge(DOWN, buff=0.25)
        sim = note(r"4{,}000 simulated paths; 80 shown").to_corner(DR, buff=0.3)
        assert round(100 * g, 1) == -5.1 and round(100 * coin_rate, 1) == -5.3

        with self.voiceover(
            "Now we can see the coin game's paradox in the formula. <bookmark mark='f'/> Here are geometric Brownian "
            "paths with the game's parameters. <bookmark mark='m'/> The expected price grows like e to the mu t, because "
            "the exponential of a bell curve is pulled up by its lucky tail. <bookmark mark='d'/> But the typical path, the "
            "median, grows at the rate mu minus one half sigma squared. With mu at five percent and sigma at forty-five "
            "percent, that's minus five point one percent per round, <bookmark mark='c'/> almost exactly the coin game's "
            "minus five point three."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.y_labels), FadeIn(ax.grid), FadeIn(ax.x_labels))
            vo.wait_until("f")
            self.play(LaggedStart(*[Create(p) for p in fan], lag_ratio=0.02), FadeIn(sim), run_time=2.5)
            vo.wait_until("m")
            self.play(Create(mean), FadeIn(formulas[0]), FadeIn(why_mean))
            vo.wait_until("d")
            self.play(FadeIn(band), Create(med), FadeIn(formulas[1]), FadeIn(rate))
            vo.wait_until("c")
            self.play(FadeIn(cr))
        with self.voiceover(
            "On the log scale, the final prices form a bell curve: the price itself is log-normal. "
            "<bookmark mark='b'/> Eighty-seven percent of paths end below where they started, even though the expected "
            "price has grown a hundred and fifty times. <bookmark mark='v'/> This is volatility drag, and it's Itô's "
            "correction term at work: noise doesn't just add uncertainty, it lowers the long-run growth rate, by exactly "
            "one half sigma squared."
        ) as vo:
            self.play(FadeIn(hist), Create(curve))
            vo.wait_until("b")
            self.play(FadeIn(bl))
            vo.wait_until("v")
            self.play(FadeIn(drag, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
