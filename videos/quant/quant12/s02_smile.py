from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import smile as SM
from explainer.quant.house import volsurface as V
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


class Smile(VoiceoverScene):
    def construct(self):
        s = load("surface")
        self.card()
        self.shapes(s)
        self.quoting(s)
        self.arbitrage(s)

    def card(self):
        c = chapter_card(1, r"Smile, skew, term structure", r"Why does every strike have its own volatility?", part=PART)
        with self.voiceover("Chapter one. Smile, skew, and term structure."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shapes(self, s):
        per = [p for p in s["per"] if p["n"] >= 10]
        pick = [per[1], per[len(per) // 2], per[-1]]
        g = axes([-0.5, 0.5], [0.3, 0.9], x_length=6.6, y_length=4.2, xlabel=r"log-moneyness $\ln K/F$",
                 ylabel=r"implied volatility", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.4, 0.6, 0.8],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = [BAD, IV, LV]
        lines, dots, leg_items = VGroup(), VGroup(), []
        for p, c in zip(pick, cols):
            kk = np.linspace(-0.5, 0.5, 101)
            iv = SM.svi_iv(p["svi"], kk, p["T"])
            lines.add(curve(ax, kk, np.clip(iv, 0.3, 0.9), c, stroke_width=3))
            k, v = np.asarray(p["k"]), np.asarray(p["iv"])
            m = (np.abs(k) <= 0.5) & (v <= 0.9) & (v >= 0.3)
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=c) for a, b in zip(k[m], v[m])]))
            leg_items.append((c, rf"{p['expiry']}: {p['T'] * 365:.0f} days"))
        leg = legend(leg_items, font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"skew: puts dearer than calls the same distance away; the crash insurance premium", 4.2, 20,
                          BAD),
            wrapped_label(r"smile: both wings above the middle; returns have fat tails (Part 1), so far strikes are hit "
                          r"more often than a normal distribution says", 4.2, 20, IV),
            wrapped_label(r"term structure: short expiries swing most; long ones are anchored near the long-run level", 4.2,
                          20, LV),
            wrapped_label(r"in equity indices the skew is steep and one-sided (since 1987); in bitcoin it is milder and can "
                          r"flip toward calls in rallies", 4.2, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface, three of its expiries; dots: quotes; lines: SVI fits")
        with self.voiceover(
            "Here are three slices of the Surface: a short, a middle and a long expiry. <bookmark mark='a'/> Each "
            "is a smile: both wings sit above the middle, because returns have fat tails and far strikes are reached "
            "more often than a normal distribution allows. And the left wing is higher than the right: the skew, the "
            "premium paid for protection against a crash. <bookmark mark='b'/> The short expiry swings the most; "
            "the long ones are anchored. In stock indices, the skew has been steep and one-sided since the crash "
            "of 1987. In Bitcoin it is milder, and in strong rallies it can even tilt toward calls."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(dots))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def quoting(self, s):
        rm = s["sticky_rmse"]
        rows = [cmath(r"\Delta_{25}", r"\to", r"\text{the strike whose call has a delta of } 0.25", font_size=34,
                      colors={r"\Delta_{25}": IV}),
                cmath(r"\text{RR}_{25} = \sigma_{25C} - \sigma_{25P}", r",", r"\ \text{BF}_{25} = \tfrac12(\sigma_{25C} + "
                      r"\sigma_{25P}) - \sigma_{ATM}", font_size=32, colors={r"\text{RR}_{25} = \sigma_{25C} - \sigma_{25P}": BAD})]
        whys = [why(r"dealers quote by delta, not strike: a 25-delta option means the same thing whatever the spot"),
                why(r"the risk reversal measures the skew, the butterfly the smile's curvature: the vanna and volga trades "
                    r"of Part 11")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-0.6, buff=0.8, edge=6.9)
        test = VGroup(
            label(r"when spot moves, does the smile stay at each strike, or move with it?", font_size=23, color=GREY_A),
            MathTex(rf"\text{{sticky strike: }} {rm['sticky strike']:.1f}\ \text{{vol pts}}\qquad \text{{sticky moneyness: }}"
                    rf" {rm['sticky moneyness']:.1f}\ \text{{vol pts}}", font_size=30, color=OPT),
            wrapped_label(rf"error predicting 11 December's quotes from 10 December's surface, as bitcoin moved from "
                          rf"{s['S']:,.0f} to {s['S_next']:,.0f}".replace(",", "{,}"), 11.0, 20, GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Traders do not quote options by strike. They quote by delta: a twenty-five-delta call is the call whose "
            "delta is a quarter, whatever the spot price. Two numbers then summarize a smile. <bookmark mark='a'/> "
            "The risk reversal, the call's volatility minus the put's, measures the skew; the butterfly, their "
            "average above the at-the-money volatility, measures the curvature. <bookmark mark='b'/> And when the "
            "spot moves, does the smile stay put at each strike, or move with the spot? A test on the Surface: "
            "predict the next day's quotes from this day's surface, both ways. Moving with the spot, sticky "
            f"moneyness, misses by {rm['sticky moneyness']:.1f} volatility points; staying at each strike, by "
            f"{rm['sticky strike']:.1f}. On this day, the smile moved with the spot."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(test))
        self.wait(0.4)
        self.clear_scene()

    def arbitrage(self, s):
        c = chapter_card(2, r"Static arbitrage, and SSVI", r"Which smiles are possible?", part=PART)
        with self.voiceover("Chapter two. Static arbitrage, and SSVI."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))
        fit = s["ssvi"]
        rows = [cmath(r"g(k)", r"=", r"\Big(1 - \frac{k\,w'}{2w}\Big)^2 - \frac{w'^2}{4}\Big(\frac1w + \frac14\Big) + "
                      r"\frac{w''}{2} \;\ge\; 0", font_size=32, colors={r"g(k)": BAD}),
                cmath(r"\partial_T w(k, T)", r"\ge", r"0,\qquad \limsup_{|k|\to\infty} \frac{w(k)}{|k|} \le 2", font_size=32,
                      colors={r"\partial_T w(k, T)": LV}),
                cmath(r"w", r"=", r"\frac{\theta_T}{2}\Big(1 + \rho\varphi k + \sqrt{(\varphi k + \rho)^2 + 1 - \rho^2}\Big)",
                      font_size=32, colors={r"w": IV})]
        whys = [why(r"butterflies: the density hidden in the smile (Part 9) must be positive; in total variance "
                    r"$w = \sigma^2 T$ that is Gatheral's $g \ge 0$"),
                why(r"calendars: total variance must not fall with maturity; wings: no steeper than Lee's moment bound "
                    r"(2004)"),
                why(rf"SSVI (Gatheral and Jacquier 2014): one formula for the whole surface, provably arbitrage-free; on the "
                    rf"Surface, $\rho = {fit['rho']:.2f}$, fitted to {s['rmse_ssvi']:.2f} vol points")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.75, edge=6.9)
        foot = wrapped_label(rf"Part 9's checker passes every expiry: the smallest $g$ is {min(p['g_min'] for p in s['per']):.2f} "
                             rf"for the per-expiry SVI fits and {s['g_ssvi_min']:.2f} for SSVI", 11.0, 21, GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Not every smile is possible. Part nine showed that the curvature of call prices is a probability "
            "density, so it must be positive. Jim Gatheral wrote that condition in terms of total variance: a "
            "function g of the smile that must never go negative. <bookmark mark='a'/> Across expiries, total "
            "variance must not fall, or a calendar spread is free money; and Roger Lee showed in 2004 that the "
            "wings can grow no faster than linearly. <bookmark mark='b'/> Gatheral and Antoine Jacquier's SSVI, from "
            "2014, is one formula for the whole surface that satisfies all of them by construction. Fitted to the "
            f"Surface, it misses the quotes by {s['rmse_ssvi']:.2f} volatility points, and every expiry passes the "
            "checker."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
