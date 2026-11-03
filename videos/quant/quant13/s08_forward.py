from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause

ORDER = ("LV", "Heston", "Bates", "VG", "SLV")
NAMES = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma", "SLV": r"SLV"}


class Forward(VoiceoverScene):
    def construct(self):
        e = load("exotics")
        fs = load("fwd_semi")
        self.card()
        self.accumulate(fs)
        self.smiles(e)
        self.derive(fs)
        self.coupons(fs)
        self.exotics(e)

    def card(self):
        c = chapter_card(14, r"Forward smiles and cliquets", r"Same vanillas, same exotic price?", part=PART)
        with self.voiceover("Chapter fourteen. Forward smiles, and cliquets."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def accumulate(self, fs):
        k = np.asarray(fs["k"])
        g = axes([-0.27, 0.27], [0.36, 0.7], x_length=6.8, y_length=4.2, xlabel=r"log-moneyness of a 30-day option, "
                 r"struck in 60 days", ylabel=r"Heston's forward smile", xticks=[-0.2, -0.1, 0, 0.1, 0.2],
                 yticks=[0.4, 0.5, 0.6, 0.7], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.7)
        ax = g.ax
        semi = curve(ax, k, np.asarray(fs["semi_iv"]), WHITE, stroke_width=3)
        ns = sorted(int(n) for n in fs["acc"])

        def pts(n):
            iv = np.clip(np.asarray(fs["acc"][str(n)], float), 0.36, 0.7)
            return VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=MODEL_COL["Heston"]) for a, b in zip(k, iv) if np.isfinite(b)])

        cur = pts(ns[0])
        cnt = MathTex(rf"{ns[0]:,}".replace(",", "{,}") + r"\ \text{paths}", font_size=30, color=MODEL_COL["Heston"])
        cnt.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        mc = np.array([np.asarray(v, float) for v in fs["mc"].values()])
        bandm = seed_band(ax, k, mc, MODEL_COL["Heston"], stroke_width=0)
        dev = float(np.max(np.abs(mc.mean(0) - np.asarray(fs["semi_iv"]))) * 100)
        spread = float(np.max(mc.max(0) - mc.min(0)) * 100)
        side = VGroup(
            wrapped_label(r"white: the forward smile by a one-dimensional integral over the law of $v$ at 60 days, Heston's "
                          r"price inside (exact up to quadrature)", 4.4, 18, GREY_A),
            wrapped_label(r"dots: Monte Carlo, as paths accumulate; band: three seeds of 40{,}000 paths", 4.4, 18,
                          MODEL_COL["Heston"]),
            MathTex(rf"\max |\text{{MC mean}} - \text{{integral}}| = {dev:.2f}\ \text{{pts}}", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        verdict = (f"The three seeds average to within {dev:.1f} of a vol point of the integral at every strike, inside "
                   f"their own spread of {spread:.1f}: the simulation and the formula agree." if dev <= max(spread, 0.3) else
                   f"The seeds' average misses the integral by up to {dev:.1f} points, more than their spread of "
                   f"{spread:.1f}: a discretisation bias in the simulation.")
        with self.voiceover(
            (
            "A forward smile is the smile a model predicts for a future date: here, the thirty-day smile sixty days "
            "out. No market quotes it; forward starts and cliquets pay on it. For Heston it can be computed two ways. "
            "White: a one-dimensional integral, derived shortly. <bookmark mark='a'/> Dots: Monte Carlo, the last "
            "month's return of ninety-day paths. With five hundred paths they scatter; as paths accumulate they "
            f"settle. <bookmark mark='b'/> {verdict}"
        )
        ) as vo:
            self.play(FadeIn(g), Create(semi), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(cnt), FadeIn(side[1]))
            per = max((vo.until("b") - 0.5) / (len(ns) - 1), 0.5)
            for n in ns[1:]:
                new_c = MathTex(rf"{n:,}".replace(",", "{,}") + r"\ \text{paths}", font_size=30,
                                color=MODEL_COL["Heston"]).move_to(cnt, aligned_edge=RIGHT)
                self.play(Transform(cur, pts(n)), Transform(cnt, new_c), run_time=per)
            vo.wait_until("b")
            self.play(FadeIn(bandm), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, fs):
        rows = [cmath(r"\Big(\frac{S_{T_2}}{S_{T_1}} - e^k\Big)^+", r"\Rightarrow", r"V_{T_1} = C\big(1,\ e^k,\ \tau;\ "
                      r"\text{state}_{T_1}\big)", font_size=34, colors={r"\Big(\frac{S_{T_2}}{S_{T_1}} - e^k\Big)^+": OPT}),
                cmath(r"\text{L\'evy:}\ \ V_0", r"=", r"C\big(1,\ e^k,\ \tau\big)\ \ \text{(today's smile)}", font_size=34,
                      colors={r"\text{L\'evy:}\ \ V_0": MODEL_COL["VG"]}),
                cmath(r"\text{Heston:}\ \ V_0", r"=", r"\int_0^\infty C_H\big(1,\ e^k,\ \tau;\ v\big)\ p_{T_1}(v)\,dv,"
                      r"\quad v_{T_1} \sim c\,\chi'^2_d(\lambda)", font_size=32,
                      colors={r"\text{Heston:}\ \ V_0": MODEL_COL["Heston"]}),
                cmath(r"\sum_i \min\big(\max(r_i, f), c\big)", r"=", r"\sum_i \Big[f + (r_i - f)^+ - (r_i - c)^+\Big]",
                      font_size=34, colors={r"\sum_i \min\big(\max(r_i, f), c\big)": OPT})]
        whys = [why(r"the payoff is homogeneous of degree 0 in the price at $T_1$: at $T_1$ it is an ordinary option with "
                    r"spot 1, worth the model's price given its state then", 20),
                why(r"independent stationary increments: the state is irrelevant, so the forward smile is today's "
                    r"$\tau$-smile (README problem 3)", 20),
                why(r"tower property: average Heston's price over the law of $v_{T_1}$, chapter 5's scaled non-central "
                    r"$\chi^2$; with COS inside, this is the white curve", 20),
                why(r"a cliquet coupon is floored at $f$ and capped at $c$: each period is a forward-start call spread, so "
                    r"a cliquet is priced off forward smiles, which no vanilla pins down", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.8, buff=0.6, edge=6.9)
        pp = pause(r"In which models is a forward-start option worth exactly today's option?", width=4.6).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            (
            "Why. A forward-start payoff ignores the price level at the first date, so then it is an ordinary option "
            "on a spot of one, worth the model's price given its state. <bookmark mark='a'/> In a Lévy model the "
            "state is irrelevant: the forward smile is today's. <bookmark mark='b'/> In Heston the state is the "
            "variance: average Heston's price over its chi-squared law at the first date, the white curve. A high "
            "variance then means a high and flatter forward smile, a low one a low and steeper smile; the average "
            "over that spread is why Heston's forward smile keeps its curvature. <bookmark mark='c'/> A cliquet is a "
            "strip of these: each coupon is a floor plus a forward-start call spread. <bookmark mark='d'/> Pause: "
            "where is a forward start worth exactly today's option? In every exponential Lévy model."
        )        )        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def coupons(self, fs):
        R = np.asarray(fs["monthly"])  # (4 months, 3 paths)
        cap, flo = 0.10, 0.0
        g = axes([0.3, 12.7], [-0.25, 0.3], x_length=10.0, y_length=4.0, ylabel=r"monthly return, three simulated paths",
                 xticks=[], yticks=[-0.2, -0.1, 0, 0.1, 0.2], yfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0",
                 font_size=15).to_edge(UP, buff=0.8)
        ax = g.ax
        capl = DashedLine(ax.c2p(0.3, cap), ax.c2p(12.7, cap), stroke_color=BAD, stroke_width=2)
        flol = DashedLine(ax.c2p(0.3, flo), ax.c2p(12.7, flo), stroke_color=GREY_B, stroke_width=2)
        lab = VGroup(label(r"cap 10\%", font_size=16, color=BAD).next_to(ax.c2p(12.7, cap), RIGHT, buff=0.08),
                     label(r"floor 0", font_size=16, color=GREY_B).next_to(ax.c2p(12.7, flo), RIGHT, buff=0.08))
        raw, clip, sums = VGroup(), VGroup(), VGroup()
        for p in range(3):
            for m in range(4):
                x = 1 + p * 4.2 + m * 0.8
                r = float(R[m, p])
                c_ = min(max(r, flo), cap)
                raw.add(Rectangle(width=0.5, height=max(abs(ax.c2p(0, np.clip(r, -0.25, 0.3))[1] - ax.c2p(0, 0)[1]), 1e-3),
                                  stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0).move_to(ax.c2p(x, np.clip(r, -0.25, 0.3) / 2)))
                clip.add(Rectangle(width=0.5, height=max(abs(ax.c2p(0, c_)[1] - ax.c2p(0, 0)[1]), 1e-3), stroke_width=0,
                                   fill_color=OPT, fill_opacity=0.85).move_to(ax.c2p(x, c_ / 2)))
            tot = float(np.clip(R[:, p], flo, cap).sum())
            sums.add(MathTex(rf"\text{{payoff}}\ {100 * tot:.1f}\%", font_size=26, color=OPT).next_to(ax.c2p(1 + p * 4.2 + 1.2, -0.25),
                                                                                                    DOWN, buff=0.15))
        foot = wrapped_label(r"each path: four monthly returns (grey outlines), each floored at 0 and capped at 10\% "
                             r"(pink); the payoff is their sum: big months are cut, bad months are forgiven", 12.0, 19, GREY_A)
        foot.to_edge(DOWN, buff=0.4)
        src = illustration(r"three paths of the fitted Heston")
        with self.voiceover(
            (
            "The cliquet on three simulated paths: each grey outline is a month's return. <bookmark mark='a'/> Each "
            "is floored at zero and capped at ten percent, and the payoff is the sum. <bookmark mark='b'/> So its "
            "value depends on each future month's volatility and skew: the forward smiles. Today's vanillas fix only "
            "the total return to each date, not how it is shared among months."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(raw), Create(flol))
            vo.wait_until("a")
            self.play(Create(capl), FadeIn(lab), LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(raw, clip)],
                                                              lag_ratio=0.08), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(sums), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def smiles(self, e):
        k = np.asarray(e["k"])
        g = axes([-0.25, 0.25], [0.38, 0.66], x_length=6.6, y_length=4.2, xlabel=r"log-moneyness of a 30-day option",
                 ylabel=r"implied volatility", xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=[0.4, 0.5, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        today = DashedVMobject(curve(ax, k, np.asarray(e["today"]), WHITE, stroke_width=3), num_dashes=40)
        lines = {m: curve(ax, k, np.clip(np.asarray(e["models"][m]["fwd_iv"]), 0.38, 0.66), MODEL_COL[m], stroke_width=2.8)
                 for m in ORDER}
        leg = legend([(WHITE, r"today's 30-day smile")] + [(MODEL_COL[m], NAMES[m]) for m in ORDER], font_size=17)
        leg.next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        sk = VGroup(label(r"skew of the forward smile (90\% minus 110\%)", font_size=19, color=GREY_A),
                    MathTex(rf"\text{{today}}\ \ {100 * e['today_skew']:.1f}", font_size=26),
                    *[MathTex(rf"\text{{{NAMES[m]}}}\ \ {100 * e['models'][m]['fwd_skew']:.1f}", font_size=26,
                              color=MODEL_COL[m]) for m in ORDER]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        sk.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"each model fitted to the Surface; the 30-day smile starting in 60 days, 40{,}000 paths")
        lv, he, vg = (e["models"][m] for m in ("LV", "Heston", "VG"))
        with self.voiceover(
            (
            (
            "Ask every fitted model the same question. <bookmark mark='a'/> Local volatility, as Part twelve showed, "
            f"flattens the forward smile: a skew of {100 * lv['fwd_skew']:.1f} points against "
            f"{100 * e['today_skew']:.1f} today. Its local volatility at the future date is a function of the price "
            "alone, and the far-out local skew is flat. <bookmark mark='b'/> Heston keeps "
            f"{100 * he['fwd_skew']:.1f} points and Bates {100 * e['models']['Bates']['fwd_skew']:.1f}: their variance "
            "is random whenever you start. Variance gamma repeats today's smile, "
            f"{100 * vg['fwd_skew']:.1f}, and SLV sits where its dial puts it, "
            f"{100 * e['models']['SLV']['fwd_skew']:.1f}. One set of vanillas, five futures."
        )
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(today), FadeIn(leg[0]), FadeIn(sk[:2]))
            vo.wait_until("a")
            self.play(Create(lines["LV"]), FadeIn(leg[1]), FadeIn(sk[2]))
            vo.wait_until("b")
            self.play(*[Create(lines[m]) for m in ORDER[1:]], FadeIn(leg[2:]), FadeIn(sk[3:]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def exotics(self, e):
        cl = {m: e["models"][m]["cliquet"] for m in ORDER}
        fs = {m: e["models"][m]["forward_start"] for m in ORDER}

        def bars(vals, title, fmt, lo, hi, ticks):
            g = axes([-0.6, len(ORDER) - 0.4], [lo, hi], x_length=5.2, y_length=3.4, xticks=list(range(len(ORDER))),
                     xfmt=lambda u: NAMES[ORDER[int(round(u))]], yticks=ticks, yfmt=fmt, font_size=14)
            ax = g.ax
            bs_ = VGroup(*[Rectangle(width=0.55, height=abs(ax.c2p(0, vals[m])[1] - ax.c2p(0, lo)[1]), stroke_width=0,
                                     fill_color=MODEL_COL[m], fill_opacity=0.85).move_to(ax.c2p(i, (vals[m] + lo) / 2))
                           for i, m in enumerate(ORDER)])
            t = label(title, font_size=20).next_to(g, UP, buff=0.15)
            v = np.array(list(vals.values()))
            spread = MathTex(rf"\text{{spread}}\ {100 * (v.max() - v.min()) / v.mean():.0f}\%", font_size=28,
                             color=BAD).next_to(g, DOWN, buff=0.25)
            return VGroup(g, t, bs_, spread)

        p1 = bars(cl, r"a cliquet: four monthly returns, each floored at 0 and capped at 10\%",
                  lambda u: f"{100 * u:.0f}\\%", 0.12, 0.145, [0.12, 0.13, 0.14])
        p2 = bars(fs, r"a forward-start at-the-money call: 30 days, starting in 60",
                  lambda u: f"{100 * u:.1f}\\%", 0.045, 0.057, [0.045, 0.05, 0.055])
        VGroup(p1, p2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.8)
        foot = wrapped_label(r"prices per unit of notional; the vanilla options all models were fitted to are the same. "
                             r"Model risk is this spread, and a desk reports it: the House prices every exotic under at "
                             r"least two models fitted to the same surface", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.4)
        v1, v2 = np.array(list(cl.values())), np.array(list(fs.values()))
        with self.voiceover(
            (
            "Price two such exotics. The cliquet costs between "
            f"{100 * v1.min():.1f} and {100 * v1.max():.1f} percent of notional across the five models: "
            f"{100 * (v1.max() - v1.min()) / v1.mean():.0f} percent apart. <bookmark mark='a'/> A forward-start "
            f"option, struck at the money in sixty days: {100 * (v2.max() - v2.min()) / v2.mean():.0f} percent apart, "
            "local volatility dearest. <bookmark mark='b'/> No vanilla can settle this. The spread is model risk, and "
            "an honest desk reports it."
            " Next: the hardest joint test, the SPX/VIX puzzle, measured on Bitcoin."
        )
        ) as vo:
            self.play(FadeIn(p1[:2]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p1[2]], lag_ratio=0.15), FadeIn(p1[3]))
            vo.wait_until("a")
            self.play(FadeIn(p2[:2]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p2[2]], lag_ratio=0.15), FadeIn(p2[3]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
