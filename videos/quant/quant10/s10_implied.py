from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import IMP, OPT, PART, REA, SPOT, load

# the Surface's future rows (videos/quant/SYLLABUS.md, "The Surface"), with the part that adds each
FUTURE_ROWS = [(r"SVI, SSVI; a surface VAE; local volatility", 12), (r"Heston, SABR, Bates, variance gamma", 13),
               (r"rough Bergomi, quadratic rough Heston, path-dependent vol", 14),
               (r"neural calibrator; neural SDE", 17)]


class Implied(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("implied")
        self.card()
        self.smiles(d)
        self.surface3d(d)
        self.scoreboard(d)

    def card(self):
        c = chapter_card(12, r"The first smile, and the Surface's first row", r"Is the market's world the formula's?",
                         lit=(1987,), part=PART)
        with self.voiceover("Chapter twelve. The first smile, and the Surface's first row."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def smiles(self, d):
        q = d["q0"]
        exp = np.array(q["expiry"])
        k, iv, T = np.asarray(q["k"], float), np.asarray(q["iv"], float), np.asarray(q["T"], float)
        show = ["2025-12-19", "2026-01-30", "2026-03-27", "2026-06-26"]
        cols = [interpolate_color(ManimColor(IMP), ManimColor(WHITE), a) for a in (0.0, 0.25, 0.5, 0.75)]
        g = axes([-0.8, 0.8], [0.3, 0.9], x_length=8.6, y_length=4.6, xlabel=r"log-moneyness $\ln(K/F)$",
                 ylabel=r"implied volatility", xticks=[-0.6, -0.3, 0, 0.3, 0.6], yticks=[0.4, 0.6, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        groups = VGroup()
        flats = VGroup()
        labels_ = VGroup()
        for e, c in zip(show, cols):
            m = (exp == e) & (np.abs(k) <= 0.8)
            o = np.argsort(k[m])
            kk, vv = k[m][o], iv[m][o]
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=c) for a, b in zip(kk, vv)])
            line = curve(ax, kk, vv, c, stroke_width=2.5)
            groups.add(VGroup(line, dots))
            flat = d["flat_fit"][e]
            flats.add(DashedLine(ax.c2p(-0.8, flat), ax.c2p(0.8, flat), color=c, stroke_width=1.5))
            days = int(round(T[exp == e][0] * 365))
            labels_.add(label(rf"{days} days", font_size=22, color=c))
        labels_.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        bs_note = wrapped_label(r"If Black--Scholes were the truth, every curve would be flat: one volatility "
                                r"per underlying.", 3.8, 24, GREY_A).next_to(labels_, DOWN, buff=0.6).align_to(labels_,
                                                                                                         LEFT)
        src = note(rf"Deribit BTC options, {d['q0']['ref_time'].replace('T', ' ').replace('Z', ' UTC')}; "
                   rf"{len(k)} out-of-the-money quotes from {d['q0']['n_trades']:,} trades".replace(",", "{,}", 1),
                   font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            f"""Reconstruct IVs from the mark prices attached to trades, using the parity-fitted forward ratio; take each instrument's median and retain out-of-the-money instruments. The Surface contains {len(k)} instrument quotes across {len(d['flat_fit'])} expiries. Here we show {len(show)} selected expiries with absolute log strike over forward at most point eight. <bookmark mark='a'/> A constant-volatility model gives a flat smile at each maturity. The observed curves bend and lean, pricing tail payoffs differently. They concern risk-neutral valuation, not identified physical crash probabilities. Carry conventions also matter, as the next chapter shows. <bookmark mark='b'/> Dashed lines are the vega-weighted flat-IV fits."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            for grp, lb in zip(groups, labels_):
                self.play(Create(grp[0]), LaggedStart(*[FadeIn(x) for x in grp[1]], lag_ratio=0.03), FadeIn(lb),
                          run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(bs_note))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(f) for f in flats], lag_ratio=0.3, run_time=2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface3d(self, d):
        q = d["q0"]
        k, iv, T = np.asarray(q["k"], float), np.asarray(q["iv"], float), np.asarray(q["T"], float)
        keep = (np.abs(k) <= 0.8) & (T >= 2 / 365)
        ax = ThreeDAxes(x_range=[-0.8, 0.8, 0.4], y_range=[0, 0.8, 0.2], z_range=[0.3, 1.1, 0.2], x_length=8.0,
                        y_length=5.4, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 1.1)  # the short-dated wing rises high: keep it under the title
        pts = smile_points3d(ax, k[keep], T[keep], iv[keep], color=IMP, radius=0.045)
        exp = np.array(q["expiry"])[keep]
        lines = VGroup()
        planes = VGroup()
        for e in sorted(set(exp)):
            m = exp == e
            o = np.argsort(k[keep][m])
            kk, tt, vv = k[keep][m][o], T[keep][m][o], iv[keep][m][o]
            if len(kk) >= 2:
                lines.add(VMobject(stroke_color=IMP, stroke_width=2, stroke_opacity=0.7).set_points_as_corners(
                    [ax.c2p(a, b, c) for a, b, c in zip(kk, tt, vv)]))
                f = d["flat_fit"][e]
                planes.add(Line(ax.c2p(-0.8, tt[0], f), ax.c2p(0.8, tt[0], f), color=GREY_B, stroke_width=1.5))
        hint = VGroup(label(r"log-moneyness", font_size=24, color=GREY_A),
                      label(r"time to expiry (to 0.8 years)", font_size=24, color=GREY_A),
                      label(r"implied volatility", font_size=24, color=IMP)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.1).to_corner(UR, buff=0.4)
        title = label(r"the Surface: Deribit BTC, 10 December 2025", font_size=28).to_corner(UL, buff=0.4)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.82)
        self.add_fixed_in_frame_mobjects(hint, title)
        self.remove(hint, title)
        with self.voiceover(
            "Put every expiry together and you have the series' Surface: two hundred and fifty-odd implied "
            "volatilities over strike and maturity, frozen on one morning. Every pricing model in this series will "
            "be calibrated to it and scored on it. The short-dated smiles, in front, are steep and high: it was "
            "the morning of a Federal Reserve decision. <bookmark mark='a'/> The grey lines are Black-Scholes' "
            "best effort, one flat volatility per expiry: the level of each expiry right, and nothing else."
        ) as vo:
            self.play(FadeIn(title), FadeIn(hint), Create(ax), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.004, run_time=3))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1, run_time=2))
            self.move_camera(theta=-40 * DEGREES, run_time=max(vo.until("a") - 0.5, 1.0))
            self.play(LaggedStart(*[Create(p_) for p_ in planes], lag_ratio=0.1, run_time=2))
            self.move_camera(theta=-30 * DEGREES, phi=72 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, pts, lines, planes)),
                                                                  FadeOut(hint), FadeOut(title)], run_time=0.5)
        self.clear_scene(run_time=0.1)

    # ------------------------------------------------------------------
    def scoreboard(self, d):
        row = d["surface_row"]
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in
                        (r"model", r"part", r"in sample", r"next day", r"arbitrage", r"parameters")])
        xs = [-6.6, -1.0, 0.5, 2.1, 3.7, 5.3]
        for h, x in zip(head, xs):
            h.move_to([x, 0, 0], aligned_edge=LEFT if x == xs[0] else ORIGIN)
        rows = VGroup(head)
        first = VGroup(label(r"Black--Scholes, one vol per expiry", font_size=24),
                       MathTex(r"10", font_size=26),
                       MathTex(rf"{row['rmse_in']:.2f}", font_size=30, color=IMP),
                       MathTex(rf"{row['rmse_out']:.2f}", font_size=30, color=IMP),
                       MathTex(rf"{row['arbitrage']}", font_size=30),
                       MathTex(rf"{row['params']}", font_size=30))
        for m, x in zip(first, xs):
            m.move_to([x, 0, 0], aligned_edge=LEFT if x == xs[0] else ORIGIN)
        rows.add(first)
        for name, part in FUTURE_ROWS:
            r = VGroup(label(name, font_size=22, color=GREY_C), MathTex(str(part), font_size=24, color=GREY_C),
                       *[MathTex(r"?", font_size=26, color=GREY_D) for _ in range(4)])
            for m, x in zip(r, xs):
                m.move_to([x, 0, 0], aligned_edge=LEFT if x == xs[0] else ORIGIN)
            rows.add(r)
        for i, r in enumerate(rows):
            r.shift(DOWN * i * 0.62)
        for r in rows[1:]:
            if r[0].width > 5.0:
                r[0].scale_to_fit_width(5.0)
            r[0].move_to([xs[0], r[0].get_y(), 0], aligned_edge=LEFT)
        rows.set_y(-0.3)
        title = label(r"The Surface: the series' pricing scoreboard", font_size=36).to_edge(UP, buff=0.5)
        unit = note(r"vega-weighted RMSE of implied volatility, in vol points; next day: 11 December, parameters "
                    r"held; arbitrage: calendar violations", font_size=20).to_edge(DOWN, buff=0.4)
        hl = SurroundingRectangle(first, color=IMP, buff=0.12, corner_radius=0.08, stroke_width=2)
        dv = note(rf"DVOL that morning: {100 * d['dvol_ref']:.1f}\%; the Surface's 30-day at-the-money volatility: "
                  rf"{100 * d['atm30']:.1f}\%", font_size=20).next_to(unit, UP, buff=0.15)
        with self.voiceover(
            f"""The first Surface row: one volatility per expiry has vega-weighted IV RMSE {row['rmse_in']:.2f} points in sample and {row['rmse_out']:.2f} the following morning with the parameters held. These are weighted averages, not worst-quote errors. At the eleven sampled maturities, fitted total variance does not decrease; that sampled normalized check is not a general arbitrage certificate for interpolation, carry or execution. <bookmark mark='a'/> Later models use the same frozen quotes. DVOL is {100 * d['dvol_ref']:.1f} percent, against interpolated ATM thirty-day IV of {100 * d['atm30']:.1f}. The index includes option wings and uses a different construction; their difference is not a constant correction across dates."""
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            self.play(FadeIn(rows[1], shift=UP * 0.2), Create(hl))
            self.play(FadeIn(unit))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.25, run_time=2))
            self.play(FadeIn(dv))
        self.wait(0.4)
        self.clear_scene()
