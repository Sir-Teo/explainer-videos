from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data


class Bergomi(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("bergomi")
        bs = load("bergomi_sim")
        self.card()
        self.curve_(b)
        self.model(bs)
        self.ribbon(bs)
        self.volvol(bs, load("facts"))
        self.ssr(load("ssr"))

    def card(self):
        c = chapter_card(13, r"Bergomi: forward variance as the state", r"What if the model's state were a whole curve?",
                         part=PART)
        with self.voiceover("Chapter thirteen. Bergomi's models: forward variance as the state."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curve_(self, b):
        e = np.asarray(b["edges"]) * 365
        fv = np.sqrt(np.asarray(b["market_fwd_var"]))
        g = axes([0, 300], [0.2, 0.7], x_length=7.2, y_length=4.0, xlabel=r"days ahead",
                 ylabel=r"forward volatility $\sqrt{\xi_0(T)}$", xticks=[0, 50, 100, 150, 200, 250, 300],
                 yticks=[0.3, 0.4, 0.5, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        steps = VGroup(*[Line(ax.c2p(a, v), ax.c2p(c_, v), stroke_color=IV, stroke_width=4) for a, c_, v in
                         zip(e[:-1], e[1:], fv)])
        risers = VGroup(*[DashedLine(ax.c2p(e[i + 1], fv[i]), ax.c2p(e[i + 1], fv[i + 1]), stroke_color=IV,
                                     stroke_width=1.5, dash_length=0.05) for i in range(len(fv) - 1)])
        hT = np.asarray(b["heston_T"]) * 365
        hes = curve(ax, hT, np.sqrt(np.asarray(b["heston_fwd_var"])), MODEL_COL["Heston"], stroke_width=3)
        leg = legend([(IV, r"the Surface: from variance-swap strikes, expiry to expiry"),
                      (MODEL_COL["Heston"], r"Heston's: one exponential, $\theta + (v_0 - \theta)e^{-\kappa T}$")],
                     font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        sat = int(np.argmin(fv))
        arrow = Arrow(ax.c2p(e[sat] + 60, fv[sat] - 0.04), ax.c2p((e[sat] + e[sat + 1]) / 2 + 1, fv[sat]), buff=0.05,
                      stroke_width=3, color=GREY_A, max_tip_length_to_length_ratio=0.15)
        sat_l = label(rf"Saturday 13 to Sunday 14 December: {100 * fv[sat]:.0f}\%", font_size=18, color=GREY_A).next_to(
            arrow.get_start(), RIGHT, buff=0.1)
        side = VGroup(
            MathTex(r"\xi_0(T) = \frac{d}{dT}\Big(T\,K_{\text{var}}(T)\Big)", font_size=32, color=IV),
            wrapped_label(r"the variance the market prices for each future instant, read from Part 12's variance swaps; "
                          r"between two expiries it is constant", 4.2, 19, GREY_A),
            wrapped_label(rf"bitcoin trades all weekend, yet Saturdays are calm: realized {100 * b['by_dow'][5]:.0f}\% "
                          rf"against {100 * np.mean(b['by_dow'][:5]):.0f}\% on weekdays (2024--2025, hourly); the "
                          r"market prices it in", 4.2, 19, GREY_A),
            wrapped_label(r"Heston's whole curve is pinned by three numbers; it cannot dip for a weekend, or rise for a "
                          r"known event", 4.2, 19, MODEL_COL["Heston"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = real_data(r"the Surface, 10 December 2025: SSVI, variance-swap strip at each expiry")
        with self.voiceover(
            (
            "A variance swap's strike times its maturity is the total variance priced to that date; its slope is the "
            "forward variance, constant between expiries. <bookmark mark='a'/> Notice the dip: the expiries on "
            "Saturday the thirteenth and Sunday the fourteenth bracket one weekend day, priced at "
            f"{100 * fv[sat]:.0f} percent against about fifty either side. Bitcoin's Saturdays realized "
            f"{100 * b['by_dow'][5]:.0f} percent over two years, weekdays {100 * np.mean(b['by_dow'][:5]):.0f}. "
            "<bookmark mark='b'/> Heston's curve is one exponential: it cannot dip for a weekend."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), FadeIn(side[0]), FadeIn(side[1]),
                      LaggedStart(*[Create(s_) for s_ in steps], lag_ratio=0.15, run_time=2.5), FadeIn(risers))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(sat_l), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(hes), FadeIn(leg[1]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def model(self, bs):
        p = bs["params"]
        rows = [cmath(r"\xi_t(T)", r"=", r"\mathbb{E}^Q_t\big[v_T\big]", font_size=38, colors={r"\xi_t(T)": IV}),
                cmath(r"\frac{d\xi_t(T)}{\xi_t(T)}", r"=", r"\omega\,\alpha_\theta\Big((1 - \theta)\,e^{-k_1(T - t)}\,dW^1_t + "
                      r"\theta\,e^{-k_2(T - t)}\,dW^2_t\Big)", font_size=34, colors={r"\frac{d\xi_t(T)}{\xi_t(T)}": VAR}),
                cmath(r"\xi_t(T)", r"=", r"\xi_0(T)\,\exp\Big(\omega\,x^T_t - \tfrac{\omega^2}{2}\operatorname{Var}x^T_t\Big),"
                      r"\quad x^T_t = \alpha_\theta\big[(1 - \theta)e^{-k_1(T-t)}X^1_t + \theta e^{-k_2(T-t)}X^2_t\big]",
                      font_size=28, colors={r"\xi_t(T)": IV}),
                cmath(r"\text{vol}\big(\xi_t(t+\tau)\big)", r"=", r"\omega\,\alpha_\theta\sqrt{(1 - \theta)^2e^{-2k_1\tau} + "
                      r"\theta^2e^{-2k_2\tau} + 2\rho_{12}\theta(1 - \theta)e^{-(k_1 + k_2)\tau}}", font_size=30,
                      colors={r"\text{vol}\big(\xi_t(t+\tau)\big)": VAR}),
                cmath(r"\text{Heston:}\ \ d\xi_t(T)", r"=", r"e^{-\kappa(T - t)}\,\xi\sqrt{v_t}\,dW^2_t", font_size=34,
                      colors={r"\text{Heston:}\ \ d\xi_t(T)": MODEL_COL["Heston"]})]
        whys = [why(r"the forward variance for date $T$: by the tower property a $Q$-martingale in $t$, the rate of a "
                    r"forward-starting variance swap", 20),
                why(r"Bergomi (2005): every point of the curve moves lognormally, driven by a fast and a slow "
                    r"Ornstein--Uhlenbeck factor ($dX^i = -k_iX^i\,dt + dW^i$) whose effect fades with the distance to $T$; "
                    r"$\alpha_\theta$ normalises so that $\omega$ is the vol of the shortest variance", 20),
                why(r"integrate: a lognormal martingale started from today's curve, which is an input, matched exactly", 20),
                why(r"It\^o: the term structure of vol of vol, set by $k_1, k_2, \theta$, independently of today's curve", 20),
                why(r"differentiate $\theta + (v - \theta)e^{-\kappa(T - t)}$: one exponential, and the same $\kappa$ also shapes "
                    r"today's curve", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            (
            "Lorenzo Bergomi turned this around: make the whole curve the state, and take today's curve from the "
            "market. Each point is the expected variance at its date, so a martingale: a forward variance swap's "
            "rate. <bookmark mark='a'/> In his two-factor model each point moves lognormally, driven by a fast and a "
            "slow Ornstein–Uhlenbeck factor that fade with distance. <bookmark mark='b'/> Integrated: today's curve "
            "times a lognormal martingale. <bookmark mark='c'/> By Itô, each point's volatility depends only on its "
            "distance tau: a vol-of-vol term structure, separate from today's curve. <bookmark mark='d'/> Heston's "
            "points all move by one shock times e to the minus kappa tau, with the same kappa that shapes today's "
            "curve: one number, two jobs."
        )
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

    def ribbon(self, bs):
        Tg = np.asarray(bs["Tg"]) * 365
        t = np.asarray(bs["t"]) * 365
        R = np.sqrt(np.clip(np.asarray(bs["ribbon"]), 0, None))
        H = np.sqrt(np.clip(np.asarray(bs["heston_ribbon"]), 0, None))
        ax = ThreeDAxes(x_range=[0, 300, 100], y_range=[0, 120, 30], z_range=[0.0, 1.0, 0.25], x_length=6.6, y_length=5.4,
                        z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)

        def lines(M, col):
            return VGroup(*[VMobject(stroke_color=col, stroke_width=2).set_points_as_corners(
                [ax.c2p(x, tt, float(np.clip(z, 0, 1.0))) for x, z in zip(Tg, row)]) for tt, row in zip(t, M)])

        LB, LH = lines(R, IV), lines(H, MODEL_COL["Heston"])
        hint = VGroup(label(r"one simulated path of the whole curve: forward vol $\sqrt{\xi_t(t + \tau)}$ over $\tau$ = 0 to "
                            r"300 days ahead (across) and the calendar date $t$ = 0 to 120 days (into the screen)",
                            font_size=19, color=GREY_A)).to_corner(UL, buff=0.3)
        hint[0].set(width=min(hint[0].width, 12.0))
        tag_b = label(r"Bergomi, two factors", font_size=24, color=IV).to_corner(UR, buff=0.4)
        tag_h = label(r"Heston", font_size=24, color=MODEL_COL["Heston"]).to_corner(UR, buff=0.4)
        mart = bs["mean_at"]["120"]
        dev = float(np.max(np.abs(np.asarray(mart["mean"]) / np.asarray(mart["xi0"]) - 1)))
        txt = wrapped_label(rf"average over 2{{,}}000 paths, 120 days on: within {100 * dev:.1f}\% of today's curve at every "
                            r"date (a martingale)", 4.6, 18, GREY_A).to_corner(DR, buff=0.35)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-125 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, tag_b, tag_h, txt)
        self.remove(hint, tag_b, tag_h, txt)
        with self.voiceover(
            (
            "Let it move. From the Surface's curve, simulate Bergomi's model day by day for four months; each day adds "
            "a slice out to three hundred days. <bookmark mark='a'/> The front whips, the far end barely moves, the "
            "weekend dip drifts in and passes. Omega is set so the model's thirty-day index moves like DVOL. "
            f"<bookmark mark='b'/> Averaged over two thousand paths, the curve stays within {100 * dev:.1f} percent of "
            "where it began: a martingale. <bookmark mark='c'/> Heston's curve moves as one exponential, and with "
            "kappa near fifteen, beyond a few weeks it never moves at all."
        )
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(tag_b), run_time=1.2)
            self.play(LaggedStart(*[Create(l_) for l_ in LB], lag_ratio=0.15), run_time=max(vo.until("b") - 1.5, 3))
            vo.wait_until("b")
            self.play(FadeIn(txt))
            vo.wait_until("c")
            self.move_camera(theta=-80 * DEGREES, run_time=1.2)
            self.play(FadeOut(LB), FadeOut(tag_b), FadeIn(tag_h), LaggedStart(*[Create(l_) for l_ in LH], lag_ratio=0.1),
                      run_time=3)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, LH)), FadeOut(hint), FadeOut(tag_h),
                                                                  FadeOut(txt)], run_time=1.5)
        self.clear_scene()

    def volvol(self, bs, f):
        tau = np.asarray(bs["tau"]) * 365
        g = axes([0, 365], [0, 3.0], x_length=6.4, y_length=4.0, xlabel=r"distance to the variance's date, $\tau$ (days)",
                 ylabel=r"vol of the forward variance $\xi_t(t + \tau)$", xticks=[0, 90, 180, 270, 365],
                 yticks=[0, 1, 2, 3], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.7)
        lb = curve(g.ax, tau, np.clip(np.asarray(bs["volvol_bergomi"]), 0, 3), IV, stroke_width=3.5)
        lh = curve(g.ax, tau, np.clip(np.asarray(bs["volvol_heston"]), 0, 3), MODEL_COL["Heston"], stroke_width=3.5)
        leg = legend([(IV, r"Bergomi: a fast and a slow factor"), (MODEL_COL["Heston"], r"Heston: one exponential, $e^{-\kappa\tau}$")],
                     font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        p = bs["params"]
        i90 = int(np.argmin(np.abs(tau - 90)))
        side = VGroup(
            MathTex(rf"k_1 = {p['k1']:g},\ k_2 = {p['k2']:g},\ \theta = {p['theta']:g},\ \omega = {bs['omega']:.2f}",
                    font_size=26, color=IV),
            wrapped_label(rf"illustrative speeds; $\omega$ set so that the model's 30-day vol index has DVOL's vol of vol, "
                          rf"{100 * f['volvol']:.0f}\%", 4.4, 18, GREY_A),
            MathTex(rf"\tau = 90\text{{d}}:\ \ {100 * bs['volvol_bergomi'][i90]:.0f}\%\ \text{{vs}}\ "
                    rf"{100 * bs['volvol_heston'][i90]:.0f}\%", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        pp = pause(r"A one-year variance swap and a one-week one: whose rate is more volatile?", width=4.6).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            (
            "One plot says it: the volatility of each point of the curve, against its distance. "
            "<bookmark mark='a'/> Bergomi's falls over weeks, then levels off: three months out, "
            f"{100 * bs['volvol_bergomi'][i90]:.0f} percent. <bookmark mark='b'/> Heston's starts far higher and dies "
            f"within weeks: {100 * bs['volvol_heston'][i90]:.0f} percent at three months. Bergomi's first Smile "
            "Dynamics paper made exactly this point: in Heston one kappa fixes the term structure of vol of vol, the "
            "forward skew and the spot–vol correlation together, so they cannot be set separately. Cliquets bet on "
            "this curve. <bookmark mark='c'/> Pause: a one-year variance swap or a one-week one, whose rate is more "
            "volatile? The one-week."
        )
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lh), FadeIn(leg[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def ssr(self, ss):
        rows_ = ss["rows"]
        rows = [cmath(r"R", r"=", r"\frac{d\sigma_{\text{ATM}}/d\ln S}{\partial_k\sigma\big|_0}", font_size=38, colors={r"R": VAR}),
                cmath(r"\mathbb{E}\big[dv \mid d\ln S\big]", r"=", r"\rho\,\xi\ d\ln S", font_size=36,
                      colors={r"\mathbb{E}\big[dv \mid d\ln S\big]": VAR}),
                cmath(r"d\sigma_{\text{ATM}}", r"\approx", r"\frac{dv}{2\sqrt v} = \frac{\rho\xi}{2\sqrt v}\,d\ln S", font_size=36,
                      colors={r"d\sigma_{\text{ATM}}": VAR}),
                cmath(r"R", r"\to", r"\frac{\rho\xi/(2\sqrt v)}{\rho\xi/(4\sqrt v)} = 2", font_size=38, colors={r"R": VAR})]
        whys = [why(r"the skew-stickiness ratio: how far the at-the-money vol moves per unit of log price, in units of the "
                    r"skew (Bergomi, ch.\ 9). Sticky strike is $R = 1$, sticky delta $R = 0$", 20),
                why(r"regress the variance's move on the price's: the two Brownian increments are correlated by $\rho$", 20),
                why(r"at short maturity the at-the-money vol is $\sqrt v$", 20),
                why(r"with chapter 4's short-maturity skew: $R = 2$, the same as local volatility (Part 12)", 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.55, edge=6.9)
        tab = VGroup(*[MathTex(rf"{r['days']}\ \text{{d}}:\ R = {r['R']:.2f}", font_size=26,
                               color=VAR) for r in rows_]).arrange_in_grid(rows=2, buff=(0.6, 0.2)).to_edge(DOWN, buff=0.45)
        r2, r365 = rows_[0], rows_[-1]
        with self.voiceover(
            (
            "One more dynamic: the skew-stickiness ratio, how far at-the-money volatility moves per unit of log price, "
            "in units of the skew. <bookmark mark='a'/> In Heston, the variance's expected move is rho xi per unit of "
            "log price; <bookmark mark='b'/> at-the-money vol is root v, so it moves rho xi over two root v. "
            "<bookmark mark='c'/> Divide by chapter four's skew: R equals two, like local volatility. "
            f"<bookmark mark='d'/> Exactly on our fit: {r2['R']:.2f} at two days, falling to {r365['R']:.2f} at a year. "
            "Short-dated, SV and local vol agree on how the smile moves; further out, they part."
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.15, run_time=2))
        self.wait(0.4)
        self.clear_scene()
