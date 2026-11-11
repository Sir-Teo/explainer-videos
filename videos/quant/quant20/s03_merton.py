from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

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
        self.feedback()

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
            "Assume continuously diffusing, traded or replicable assets, constant volatility and interest rates, and a single zero-coupon debt with no earlier default or payout. The asset process has physical drift mu. <bookmark mark='a'/> Pricing uses a risk-neutral measure with drift r, producing the Black-Scholes equity value. <bookmark mark='b'/> Debt is assets minus equity. For this model, its spread is determined by leverage, asset volatility and maturity, with the leverage convention and rate held explicit. <bookmark mark='c'/> To calculate an actual terminal-default probability instead of a price, use physical drift mu and the assumed lognormal asset distribution. Distance to default is a standardized distance, not a probability. Its negative normal tail is a model probability only under those assumptions; estimating mu and calibrating real event frequencies remain separate tasks."
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
        raw = {k: np.asarray(m["term"][k], dtype=float) for k in cols}
        assert all(np.isfinite(v).all() and (v >= -1e-7).all() for v in raw.values())
        ymax = np.ceil(np.log10(1 + max(v.max() for v in raw.values())) / 0.5) * 0.5
        ticks = np.log10(1 + np.asarray([0, 1, 10, 100, 1000, 10000]))
        g = axes([0, 20], [0, ymax], x_length=7.4, y_length=4.4, xlabel=r"maturity, years", ylabel=r"Merton spread, bp (log $1+s$ scale)",
                 xticks=[0, 5, 10, 15, 20], yticks=ticks, yfmt=lambda v: f"{10 ** v - 1:,.0f}".replace(",", "{,}"), font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, Ts, np.log10(1 + np.maximum(raw[k], 0)), c_, stroke_width=3.5)
                         for k, c_ in cols.items()])
        side = VGroup(
            legend([(QC.GAIN, r"leverage 0.3, vol 20\%"), (QC.IMPLIED, r"leverage 0.6, vol 25\%"),
                    (QC.LOSS, r"leverage 1.05, vol 30\% (already under water)")], font_size=16),
            wrapped_label('all saved curves shown without top-coding, on a $\\log_{10}(1+s_{\\rm bp})$ axis labeled in bp. A solvent diffusion has a tiny positive short-horizon default tail; jumps, uncertainty and other frictions are possible extensions', 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "These are different hypothetical zero-coupon debts priced at different maturities using the displayed Merton inputs. <bookmark mark='a'/> For the solvent parameter case, very short spreads approach zero; the plotted curve rises over this range. <bookmark mark='b'/> Another parameter case has a hump. This is a term structure across alternative contracts, not evidence that a single Merton firm survives earlier default dates: its default event is only at the chosen maturity. <bookmark mark='c'/> For assets already below the promised face amount, the short spread can be very large and decline with maturity as recovery becomes possible. At a fixed positive distance from the boundary, a continuous diffusion has a positive but extremely small short-horizon tail probability; it is incorrect to say it cannot cross quickly. Jumps, uncertainty, early-default rules and noncredit frictions offer possible explanations for larger observed short spreads."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(lines[i]), run_time=1.5)
            self.play(FadeIn(side[1]))
        self.add(illustration(r"Merton (1974); r = 4\%; leverage $D/V$; residuals below $10^{-7}$ bp treated as zero"))
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self, s):
        cases = [(0.4, 0.25, r"illustration: leverage 40\%, asset vol 25\%"), (0.5, 0.3, r"leverage 50\%, vol 30\%"),
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
        side = wrapped_label(r"Illustrative model parameters versus a broad historical yield gap. Instruments, "
                             r"duration, composition and dates are unmatched; the difference is not a measured "
                             r"liquidity premium or a calibrated residual.", 3.8, 21, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"This is an illustrative parameter comparison, not a calibrated medium-grade issuer study. Assume the displayed leverage and asset volatilities for hypothetical five-year zero-coupon debts. <bookmark mark='a'/> The first model spread is {vals[0]:.0f} basis points. The broad historical Baa-minus-Treasury average shown beside it is {100 * s['mean_baa']:.0f} basis points, from different instruments, durations and dates. The difference cannot be assigned uniquely to liquidity or a missing premium. Merton's pricing measure already embeds a price of asset risk through the measure change; it does not price only physical expected loss. The credit-spread puzzle literature uses more careful matching and calibration. This chart motivates that question rather than replicating its empirical estimates."
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
            "Equity value and equity volatility provide two model equations for latent assets and asset volatility. The diffusion relation uses call delta and leverage, under the stated Merton assumptions. <bookmark mark='a'/> The House solves in logarithms and recovers this deliberately constructed example within numerical tolerance. One successful inversion is not a uniqueness or calibration guarantee for noisy market inputs; inspect convergence, residuals, parameter sensitivity and the model assumptions."
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

    def feedback(self):
        title = wrapped_label('Answer: value transfers under the stated Merton assumptions', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('At fixed total asset value, $E+B=V$. A gain of $0.1E$ in equity means a loss of $0.1E$ in debt, not a 10\\% fall in debt.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Hold total asset value and the other Merton inputs fixed. Debt plus equity equals asset value. If equity gains ten percent of its previous value because asset volatility rises, debt loses that same dollar amount. Its percentage loss is ten percent times the equity-to-debt value ratio, not automatically ten percent. Real financing changes can violate the fixed-input comparison.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
