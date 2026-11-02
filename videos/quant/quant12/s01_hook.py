from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from explainer.quant.viz import smile_points3d
from explainer.quant.house import volsurface as V
from videos.quant.quant12.common import IV, LV, PART, SPOT, load, real_data


class Hook(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("surface")
        self.title_card()
        self.tour(s)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The shape of fear")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twelve. The volatility surface. Black and Scholes assumed one volatility. The market quotes a "
            "different one for every strike and every expiry, and the shape it draws is the market's map of fear."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def tour(self, s):
        fit = s["ssvi"]
        ax = ThreeDAxes(x_range=[-0.4, 0.4, 0.2], y_range=[0, 0.5, 0.1], z_range=[0.3, 0.8, 0.1], x_length=7.6,
                        y_length=5.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)

        def f(k, T):
            th = V.theta_at(fit, T)
            return float(np.sqrt(V.ssvi_w(k, th, fit["rho"], fit["eta"], fit["gamma"]) / T))

        surf = Surface(lambda u, v: ax.c2p(u, v, np.clip(f(u, v), 0.3, 0.8)), u_range=[-0.4, 0.4], v_range=[0.03, 0.5],
                       resolution=(32, 24), fill_opacity=0.8, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0.35), (IV, 0.55), (QC.LOSS, 0.75)], axis=2)
        k, T, iv = (np.asarray(s[x]) for x in ("k", "T", "iv"))
        m = (np.abs(k) <= 0.4) & (T <= 0.5) & (T >= 0.03) & (iv >= 0.3) & (iv <= 0.8)
        dots = smile_points3d(ax, k[m], T[m], iv[m], color=WHITE, radius=0.03)
        hint = VGroup(label(r"log-moneyness $\ln K/F$", font_size=24, color=SPOT), label(r"years to expiry", font_size=24,
                                                                                    color=GREY_A),
                      label(r"implied volatility", font_size=24, color=IV)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        hint.to_corner(UR, buff=0.4)
        params = note(rf"dots: {int(m.sum())} quotes; surface: SSVI fit, {s['rmse_ssvi']:.2f} vol points (vega-weighted)",
                      font_size=19).to_corner(DR, buff=0.3)
        src = real_data(r"the Surface: Deribit BTC options, 10 December 2025, 08:00 UTC", corner=DL)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, params, src)
        self.remove(hint, params, src)
        with self.voiceover(
            "Here is the Surface, the frozen day of Bitcoin options this series prices against. Each white dot is a "
            "quote: an implied volatility at one strike and one expiry. <bookmark mark='a'/> Through them, a smooth "
            "surface with no arbitrage in it, fitted to within a fraction of a volatility point. <bookmark mark='b'/> "
            "Read its shape. Along the strikes it curves up at both ends, and higher on the downside: the smile and "
            "its skew, the price of crash insurance. Along the expiries it changes too: the term structure. This part "
            "is about reading that shape, fitting it without arbitrage, and trading it."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), FadeIn(dots), run_time=2)
            vo.wait_until("a")
            self.play(Create(surf), FadeIn(params), run_time=3)
            vo.wait_until("b")
            self.move_camera(theta=-30 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, dots)), FadeOut(hint),
                                                                  FadeOut(params), FadeOut(src)], run_time=1.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Smile, skew and term structure; quoting by delta; sticky strike against sticky delta",
            r"Static arbitrage: butterflies, calendars, Lee's moment formula; SSVI fitted to the Surface",
            r"Dupire's local volatility, and the forward smile it gets wrong",
            r"Variance swaps and the VIX, rebuilt from options; our index against DVOL",
            r"The variance risk premium, measured on two years of weekly surfaces",
            r"Volmageddon, 5 February 2018; dealer gamma and same-day options",
            r"Learning surfaces: a variational autoencoder over two years of bitcoin smiles",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. The smile's shape and how traders quote it. The conditions that keep a surface free of "
            "arbitrage, and a fit that obeys them. Local volatility, and what it gets wrong. Variance swaps and the "
            "VIX, rebuilt from option prices. The variance risk premium, measured. The day the short-volatility "
            "trade blew up. And a neural network that learns what Bitcoin's surfaces look like."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, this part builds the surface builder. <bookmark mark='a'/> Every price the volatility desk "
            "quotes from now on is read off a surface it fits, and that surface passes Part nine's arbitrage checker "
            "first."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
