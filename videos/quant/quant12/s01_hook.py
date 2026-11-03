from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from explainer.quant.viz import smile_points3d
from explainer.quant.house import volsurface as V
from videos.quant.quant12.common import IV, LV, PART, SPOT, fixed, load, real_data


class Hook(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("surface")
        self.title_card()
        self.tour(s)
        self.history(s)
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
        ax.x_axis.set_color(SPOT); ax.y_axis.set_color(GREY_A); ax.z_axis.set_color(IV)  # the key reads off the axes
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

    def history(self, s):
        events = [(1973, r"one $\sigma$: Black--Scholes", QC.IDEA), (1987, r"the crash: the skew is born", QC.CRISIS),
                  (1993, r"the VIX, on S\&P 100 options", QC.FIRM), (1994, r"Dupire; Derman--Kani; Rubinstein", QC.IDEA),
                  (1999, r"variance swaps (Goldman's DDKZ)", QC.IDEA), (2003, r"the VIX becomes a strip of options", QC.FIRM),
                  (2004, r"VIX futures; SVI", QC.IDEA), (2009, r"the variance premium measured", QC.IDEA),
                  (2014, r"SSVI", QC.IDEA), (2018, r"Volmageddon", QC.CRISIS), (2021, r"Deribit's DVOL", QC.FIRM),
                  (2023, r"VIX1D; same-day options boom", QC.FIRM), (2024, r"options on bitcoin ETFs", QC.FIRM)]
        x0, x1 = -6.4, 6.4
        X = lambda y: x0 + (x1 - x0) * (y - 1970) / (2026 - 1970)  # noqa: E731
        line = Line([x0, 0, 0], [x1, 0, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[Text(str(y), font_size=14, color=GREY_D).next_to([X(y), 0, 0], DOWN, buff=0.12)
                         for y in (1970, 1980, 1990, 2000, 2010, 2020)])
        dots, labels = VGroup(), VGroup()
        for i, (y, name, col) in enumerate(events):
            d = Dot([X(y), 0, 0], radius=0.07, color=col)
            t = label(rf"{y}\; {name}", font_size=17, color=col)
            lvl = (i % 3) + 1
            t.move_to([X(y), (0.55 * lvl + 0.1) * (1 if i % 2 == 0 else -1), 0])
            keep_in_frame(t, margin=0.2)
            lead = Line(d.get_center(), t.get_bottom() if i % 2 == 0 else t.get_top(), color=GREY_C, stroke_width=1,
                        stroke_opacity=0.5)
            dots.add(VGroup(d, lead))
            labels.add(t)
        head = label(r"How we got here", font_size=34, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How did the market come to quote a surface? In 1973 Black and Scholes priced every option with one "
            "volatility, and for fourteen years the market more or less agreed. <bookmark mark='a'/> Then on the "
            "nineteenth of October 1987 the S&P 500 fell by a fifth in a day, and from then on index puts far below the "
            "money traded at much higher implied volatilities than calls: the skew was born. <bookmark mark='b'/> In "
            "1993 Cboe began publishing the VIX. In 1994 Dupire, Derman and Kani, and Rubinstein each showed how to fit "
            "the whole smile with one model. Goldman's quants explained how to trade variance itself, and in 2003 the "
            "VIX became exactly that: a strip of options. <bookmark mark='c'/> Then futures, arbitrage-free fits, and a "
            "decade of selling volatility that ended on the fifth of February 2018. <bookmark mark='d'/> And the newest "
            "chapters are Bitcoin's: Deribit's volatility index, same-day options, options on Bitcoin funds."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks))
            self.play(FadeIn(dots[0]), FadeIn(labels[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labels[1]), Flash(dots[1][0], color=QC.CRISIS))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(dots[i], labels[i])) for i in range(2, 6)], lag_ratio=0.5, run_time=4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(dots[i], labels[i])) for i in range(6, 10)], lag_ratio=0.5, run_time=3))
            self.play(Flash(dots[9][0], color=QC.CRISIS))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(dots[i], labels[i])) for i in range(10, 13)], lag_ratio=0.5, run_time=2.5))
        self.wait(0.3)
        self.clear_scene()
        self.bend(s)

    def bend(self, s):
        fit = s["ssvi"]
        ax = ThreeDAxes(x_range=[-0.4, 0.4, 0.2], y_range=[0, 0.5, 0.1], z_range=[0.3, 0.8, 0.1], x_length=7.6,
                        y_length=5.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)
        atm = float(np.sqrt(V.ssvi_surface_w(fit, 0.0, 30 / 365) / (30 / 365)))

        def f(k, T):
            return float(np.sqrt(V.ssvi_surface_w(fit, k, T) / T))

        def mk(g):
            sf = Surface(lambda u, v: ax.c2p(u, v, float(np.clip(g(u, v), 0.3, 0.8))), u_range=[-0.4, 0.4],
                         v_range=[0.03, 0.5], resolution=(24, 16), fill_opacity=0.8, stroke_width=0.3, stroke_color=GREY_D)
            sf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0.35), (IV, 0.55), (QC.LOSS, 0.75)], axis=2)
            return sf
        flat = mk(lambda k, T: atm)
        bent = mk(f)
        t1 = label(rf"Black--Scholes: one volatility, {100 * atm:.0f}\% everywhere", font_size=24, color=GREY_A).to_corner(UL, buff=0.4)
        t2 = label(r"the market: a different volatility at every strike and expiry", font_size=24, color=IV).to_corner(UL, buff=0.4)
        q = label(r"pause and predict: which corner is highest, and why?", font_size=22, color=QC.HOUSE).to_corner(DL, buff=0.3)
        fixed(self, t1, t2, q)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.9)
        with self.voiceover(
            "Here is that history as one picture. Before 1987 the surface was, near enough, flat: a single number. "
            "Pause and predict: when it bends, which corner rises highest? <bookmark mark='a'/> The short-dated "
            "downside. Options that pay if the price collapses soon are the ones everybody wants and nobody wants to "
            "sell: crash insurance. The flat plane bends into the Surface of December 2025. Black and Scholes still "
            "gives the language, implied volatility; but the object we trade is this whole curved sheet."
        ) as vo:
            self.play(Create(ax), FadeIn(flat), FadeIn(t1), FadeIn(q))
            vo.wait_until("a")
            self.play(Transform(flat, bent), FadeOut(t1), FadeIn(t2), FadeOut(q), run_time=4)
            self.move_camera(theta=-35 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, flat)), FadeOut(t2)], run_time=1.2)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The smile read as a distribution; the term structure; quoting by delta",
            r"How surfaces move: sticky strike, sticky delta, and the principal components of moves",
            r"Static arbitrage: Gatheral's $g$, calendars, Lee's moment formula",
            r"SVI and SSVI, fitted live; Dupire's local volatility and an implied tree",
            r"Gy\"ongy's theorem checked by simulation; local volatility's forward smile",
            r"Variance swaps replicated on real bitcoin; the VIX rebuilt; our index against DVOL",
            r"The variance risk premium on bitcoin and the S\&P 500; SVIX and risk-neutral moments",
            r"VIX futures, short-volatility notes and Volmageddon; dealer gamma and same-day options",
            r"Learning surfaces: an autoencoder and an arbitrage-free network; who builds surfaces; the frontier",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan. Reading the smile as a distribution; how surfaces move, and which shapes are impossible. "
            "Fitting: SVI, SSVI and Dupire's local volatility. Volatility as an asset: variance swaps on real Bitcoin, "
            "the VIX rebuilt, and the premium the market pays for variance. The products that blew up in 2018, and "
            "dealer hedging. And networks that learn surfaces, the firms that build them, and the frontier."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, this part builds the surface builder. <bookmark mark='a'/> Every price the volatility desk "
            "quotes from now on is read off a surface it fits, and that surface passes Part nine's arbitrage checker "
            "first. The trial counter will not move in this part: everything we measure here is a price or a "
            "description, not a strategy being tested."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
