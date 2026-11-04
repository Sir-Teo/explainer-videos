from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import credit as CR
from videos.quant.quant20.common import (ASSET, BAD, DEBT, EQUITY, PART, RISKY, ask, fit_right, grid_fn, house_lab,
                                         illustration, load, surf3d_axes)


class Merton(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("merton")
        self.card()
        self.payoffs()
        self.derive()
        self.surface(m)
        self.term(m)
        self.puzzle(load("spreads"))
        self.lab()

    def card(self):
        c = chapter_card(2, r"Merton: debt as an option", r"What does a company's equity say about its debt?", lit=(1974,),
                         part=PART)
        with self.voiceover("Chapter two. Robert Merton's insight: a company's shares are an option on its assets."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def payoffs(self):
        g = axes([0, 200], [0, 200], x_length=6.0, y_length=4.2, xlabel=r"assets at maturity $V_T$",
                 ylabel=r"payoff", xticks=[0, 100, 200], yticks=[0, 100, 200], font_size=14).shift(LEFT * 2.6 + DOWN * 0.3)
        ax = g.ax
        D = 100
        eq = VMobject().set_points_as_corners([ax.c2p(0, 0), ax.c2p(D, 0), ax.c2p(200, 200 - D)]).set_stroke(EQUITY, 4)
        de = VMobject().set_points_as_corners([ax.c2p(0, 0), ax.c2p(D, D), ax.c2p(200, D)]).set_stroke(DEBT, 4)
        kink = DashedLine(ax.c2p(D, 0), ax.c2p(D, 200), color=GREY_B, stroke_width=1.5)
        rows = VGroup(
            MathTex(r"E_T = \max(V_T - D,\ 0)", font_size=34, color=EQUITY),
            MathTex(r"B_T = \min(V_T,\ D) = D - \max(D - V_T,\ 0)", font_size=30, color=DEBT),
            wrapped_label(r"shareholders own a call on the firm's assets with strike the face of the debt; bondholders "
                          r"own a safe bond and have sold the shareholders a put. Default is the put being exercised",
                          4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        fit_right(rows)
        with self.voiceover(
            "A company owes a single debt, D, due at T. When it comes due, if the assets are worth more than D, the "
            "shareholders pay it and keep the rest. <bookmark mark='a'/> If not, they walk away, and the bondholders "
            "take the assets. So the shares pay like a call option on the assets, struck at the debt. "
            "<bookmark mark='b'/> And the bonds pay like a safe bond minus a put. Default is simply the put being "
            "exercised. Merton saw in 1974 that Black and Scholes had already priced both."
        ) as vo:
            self.play(FadeIn(g), Create(kink))
            vo.wait_until("a")
            self.play(Create(eq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(de), FadeIn(rows[1]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"dV_t", r"=", r"\mu V_t\,dt + \sigma_V V_t\,dW_t", font_size=40, colors={r"dV_t": ASSET}),
                cmath(r"E_0", r"=", r"V_0 N(d_1) - D e^{-rT} N(d_2),\quad d_{1,2} = \frac{\ln(V_0/D) + (r \pm "
                      r"\frac12\sigma_V^2)T}{\sigma_V\sqrt T}", font_size=32, colors={r"E_0": EQUITY}),
                cmath(r"s", r"=", r"-\frac{1}{T}\ln\Big(N(d_2) + \frac{V_0 e^{rT}}{D}\,N(-d_1)\Big)", font_size=36,
                      colors={r"s": RISKY}),
                cmath(r"\mathbb{P}(V_T < D)", r"=", r"N(-DD),\quad DD = \frac{\ln(V_0/D) + (\mu - \frac12\sigma_V^2)T}"
                      r"{\sigma_V\sqrt T}", font_size=34, colors={r"\mathbb{P}(V_T < D)": BAD})]
        whys = [why(r"the firm's assets follow geometric Brownian motion (Part 5), traded or replicable"),
                why(r"equity is Black--Scholes (Part 10) with the assets as the underlying and the debt as the strike"),
                why(r"debt is worth $V_0 - E_0$; its yield over $r$ is the credit spread, a function of leverage "
                    r"$De^{-rT}/V_0$, asset volatility and maturity only"),
                why(r"under the real-world drift $\mu$, the chance the assets end below the debt: the distance to "
                    r"default $DD$ counts standard deviations of cushion")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.5, edge=6.9)
        with self.voiceover(
            "Write the assets as a geometric Brownian motion, as in Part five. <bookmark mark='a'/> Then the equity is "
            "Black and Scholes, with the firm's assets as the underlying and the debt as the strike. "
            "<bookmark mark='b'/> The debt is whatever is left, and its yield over the safe rate is the credit "
            "spread. It depends on three things only: leverage, the volatility of the assets, and maturity. "
            "<bookmark mark='c'/> And with the assets' real-world drift, the probability of ending below the debt is "
            "one minus a normal distribution at the distance to default: how many standard deviations of cushion the "
            "firm has."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def surface(self, m):
        lev, vol, Z = np.asarray(m["lev"]), np.asarray(m["vol"]), np.minimum(np.asarray(m["spread_bp"]), 1500)
        f = grid_fn(lev, vol, Z)
        ax = surf3d_axes([0.1, 0.9, 0.2], [0.1, 0.6, 0.1], [0, 1500, 500], x_length=6.0, y_length=4.8, z_length=3.2)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, w: ax.c2p(u, w, f(u, w)), u_range=(0.1, 0.9), v_range=(0.1, 0.6), resolution=(24, 20),
                       fill_opacity=0.85, stroke_width=0.4, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.GAIN, 0), (QC.IMPLIED, 300), (QC.LOSS, 1500)], axis=2)
        key = label(r"leverage $De^{-rT}/V$ (across), asset volatility (back), 5-year spread in bp (up, capped at "
                    r"1{,}500)", font_size=19, color=GREY_A).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "Merton's five-year spread over every combination of leverage and asset volatility. "
            "<bookmark mark='a'/> A firm with little debt pays almost nothing, whatever its volatility. As leverage "
            "rises the spread climbs, and volatility makes it climb faster: shareholders with nothing left to lose "
            "gain from risk, and bondholders pay for it. <bookmark mark='b'/> This is the asset-substitution problem "
            "Jensen and Meckling wrote about in 1976, drawn as a surface."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-125 * DEGREES, run_time=5)
            vo.wait_until("b")
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)

    def term(self, m):
        Ts = np.asarray(m["Ts"])
        cols = {"safe": QC.GAIN, "middling": QC.IMPLIED, "distressed": QC.LOSS}
        g = axes([0, 20], [0, 800], x_length=7.4, y_length=4.4, xlabel=r"maturity, years", ylabel=r"Merton spread, bp",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 200, 400, 600, 800], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, Ts, np.clip(np.asarray(m["term"][k]), 0, 800), c_, stroke_width=3.5)
                         for k, c_ in cols.items()])
        side = VGroup(
            legend([(QC.GAIN, r"leverage 0.3, vol 20\%"), (QC.IMPLIED, r"leverage 0.6, vol 25\%"),
                    (QC.LOSS, r"leverage 1.05, vol 30\% (already under water)")], font_size=16),
            wrapped_label(r"the failure: a healthy firm's short-dated spread goes to zero, because a diffusion cannot "
                          r"reach the default point in a week. Real one-year spreads are not zero; jumps, unseen "
                          r"assets (Duffie and Lando, 2001) and the next chapter's random clock fix it", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "And by maturity. <bookmark mark='a'/> A healthy firm's spread starts at zero and rises with time. "
            "<bookmark mark='b'/> A middling one rises and then falls, once surviving the early years makes the "
            "future safer. <bookmark mark='c'/> A firm already under water has huge short spreads that fall with "
            "maturity, because it has time to recover. The first shape is the model's failure: real bonds that mature "
            "in a few months still pay a spread. Assets that move continuously cannot reach the default point that "
            "fast; jumps, or assets the market cannot see exactly, are needed, and the next chapters drop the "
            "assets altogether."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(lines[i]), run_time=1.5)
            self.play(FadeIn(side[1]))
        self.add(illustration(r"Merton (1974); r = 4\%; leverage here is the face of the debt over the assets, $D/V$"))
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self, s):
        cases = [(0.4, 0.25, r"Baa-like: leverage 40\%, asset vol 25\%"), (0.5, 0.3, r"leverage 50\%, vol 30\%"),
                 (0.6, 0.25, r"leverage 60\%, vol 25\%")]
        vals = [float(CR.merton_spread(1.0, sv, L * np.exp(0.04 * 5), 0.04, 5.0) * 1e4) for L, sv, _ in cases]
        g = axes([0.4, 4.6], [0, 220], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"5-year spread, bp",
                 xticks=[], yticks=[0, 50, 100, 150, 200], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (v_, (_, _, l_)) in enumerate(zip(vals + [100 * s["mean_baa"]], cases + [(0, 0, r"Moody's Baa, average since 1953")])):
            b_ = Rectangle(width=0.7, height=max(ax.c2p(0, v_)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                           fill_color=EQUITY if i < 3 else RISKY, fill_opacity=0.8).move_to(
                [ax.c2p(i + 1, 0)[0], (ax.c2p(0, v_)[1] + ax.c2p(0, 0)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(f"{v_:.0f}", font_size=24).next_to(b_, UP, buff=0.1),
                            wrapped_label(l_, 1.5, 14, GREY_A).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.15)))
        side = wrapped_label(r"the credit spread puzzle, in numbers: calibrated to a typical medium-grade firm, Merton "
                             r"explains a fraction of the Baa spread. The rest is chapter 1's premium for bad times and "
                             r"illiquidity, which a risk-neutral model with no jumps leaves out", 3.8, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now the puzzle of chapter one, in numbers. Give Merton a typical medium-grade company: debt at forty "
            "percent of its assets, asset volatility of twenty-five percent. <bookmark mark='a'/> Its five-year spread "
            f"comes out at {vals[0]:.0f} basis points. Baa bonds have paid {100 * s['mean_baa']:.0f} on average. "
            "Even much riskier firms in the model barely reach it. The model prices the expected loss; the market "
            "also charges for when the loss arrives and for how hard the bond is to sell."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Merton backwards: assets from equity", CR.merton_solve, "def f(z):", 5, width=7.6)
        card.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.5)
        V, s, D, r, T = 120.0, 0.25, 100.0, 0.03, 1.0
        E, dl = CR.merton_equity(V, s, D, r, T)
        sE = float(dl * s * V / E)
        v2, s2 = CR.merton_solve(float(E), sE, D, r, T)
        out = [f"equity {float(E):.3f}, equity vol {sE:.4f}, debt face {D:.0f}",
               f"solved:  assets {v2:.4f}  asset vol {s2:.4f}",
               f"truth:   assets {V:.4f}  asset vol {s:.4f}"]
        with self.voiceover(
            "In practice the assets cannot be seen; the equity can. Two equations tie them: the equity is the call's "
            "value, and the equity's volatility is the call's delta times the assets' volatility, scaled. "
            "<bookmark mark='a'/> The House solves the pair in logarithms, and recovers a known firm exactly."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        q = ask(r"a firm's shares rise 10\% on news that its assets became riskier, with no change in their value. "
                r"What happened to its bonds?")
        with self.voiceover("A company's shares rise ten percent on news that its assets became riskier, at the same "
                            "value. What happened to its bonds?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
