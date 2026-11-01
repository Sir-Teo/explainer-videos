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
        self.invert(d)
        self.smiles(d)
        self.surface3d(d)
        self.scoreboard(d)

    def card(self):
        c = chapter_card(9, r"Implied volatility and the first smile", r"What volatility is the market charging?",
                         lit=(1987,), part=PART)
        with self.voiceover("Chapter nine. Implied volatility and the first smile."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def invert(self, d):
        F, K, T, target = d["solver_F"], d["solver_K"], d["solver_T"], d["solver_price"]
        sig = np.linspace(0.05, 1.2, 200)
        prices = bs.price(F, K, T, sig) / 1000
        g = axes([0, 1.2], [0, 16], x_length=6.6, y_length=4.2, xlabel=r"volatility $\sigma$",
                 ylabel=r"Black--Scholes price, thousands of dollars", xticks=[0.25, 0.5, 0.75, 1.0],
                 yticks=[0, 5, 10, 15], xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, sig, prices, OPT, stroke_width=4)
        tgt = DashedLine(ax.c2p(0, target / 1000), ax.c2p(1.2, target / 1000), color=GREY_B, stroke_width=1.5)
        tgt_lab = MathTex(rf"\text{{market price}}\ \${target:,.0f}".replace(",", "{,}"), font_size=26, color=GREY_A)
        tgt_lab.next_to(ax.c2p(1.2, target / 1000), UP, buff=0.1).shift(LEFT * 1.2)
        its = np.asarray(d["solver_iters"], float)
        dot = glow_dot(ax.c2p(its[-1], target / 1000), color=IMP, radius=0.07)
        drop = DashedLine(ax.c2p(its[-1], target / 1000), ax.c2p(its[-1], 0), color=IMP, stroke_width=2)
        quote = VGroup(
            label(r"one real quote, 10 December 2025, 08:00 UTC", font_size=24, color=GREY_A),
            label(rf"a BTC call, strike \${K:,.0f}, {T * 365:.0f} days".replace(",", "{,}"), font_size=26),
            label(rf"forward \${F:,.0f} (from put--call parity)".replace(",", "{,}"), font_size=24, color=SPOT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        rows = VGroup(*[MathTex(rf"\sigma_{{{i}}} = {100 * v:.10f}\%", font_size=28,
                                color=IMP if i == len(its) - 1 else GREY_A) for i, v in enumerate(its)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(quote, DOWN, buff=0.5).align_to(quote, LEFT)
        rows_lab = VGroup(label(r"initial guess: Corrado--Miller", font_size=20, color=GREY_B),
                          label(r"then Newton steps, kept inside a bisection bracket", font_size=20, color=GREY_B))
        rows_lab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        with self.voiceover(
            "The formula has five inputs. Four can be looked up: the price of the underlying, the strike, the time "
            "and the interest rate. The fifth, volatility, cannot. So traders turn the formula around: given the "
            "market's price, find the volatility that reproduces it. That number is the implied volatility. "
            "<bookmark mark='a'/> Here is one real quote from the House's data: a Bitcoin call on Deribit, the "
            "largest crypto options exchange, on the morning of the tenth of December 2025. The Black-Scholes price "
            "rises steadily with volatility, so exactly one volatility matches the market price. "
            "<bookmark mark='b'/> The House's solver starts from Corrado and Miller's approximation, which lands "
            "within a twentieth of a volatility point, and two Newton steps finish the job to twelve digits: "
            f"{100 * its[-1]:.2f} percent. Peter Jaeckel's method, which desks use, does it in two steps from "
            "anywhere. Traders stopped quoting prices and started quoting this number, because it puts options of "
            "every strike and maturity on one scale."
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(quote), Create(tgt), FadeIn(tgt_lab))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows_lab[0]))
            for r in rows[1:]:
                self.play(FadeIn(r), run_time=0.6)
            self.play(FadeIn(rows_lab[1]), FadeIn(dot, scale=1.5), Create(drop))
        self.wait(0.3)
        self.clear_scene()

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
            "Now do this for every option traded that morning. Plot the implied volatility of each against its "
            "strike, measured as the log of strike over forward, one curve per expiry. "
            "<bookmark mark='a'/> If the Black-Scholes world were the real one, each curve would be a flat line: "
            "the underlying has one volatility, whatever strike you ask about. Instead they smile, and lean. "
            "Out-of-the-money puts, to the left, are dearer than calls the same distance away, and both wings rise "
            "above the middle. The market is charging for something the formula does not have: big moves, mostly "
            "down, more often than a lognormal allows. Part one measured exactly those fat tails in the prices "
            "themselves; here they are, priced. <bookmark mark='b'/> The dashed lines are the best one can do with "
            "Black-Scholes as stated, one volatility per expiry."
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
        ax = ThreeDAxes(x_range=[-0.8, 0.8, 0.4], y_range=[0, 0.8, 0.2], z_range=[0.3, 1.0, 0.2], x_length=8.0,
                        y_length=5.4, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)
        pts = smile_points3d(ax, k[keep], np.minimum(T[keep], 0.8), iv[keep], color=IMP, radius=0.045)
        exp = np.array(q["expiry"])[keep]
        lines = VGroup()
        planes = VGroup()
        for e in sorted(set(exp)):
            m = exp == e
            o = np.argsort(k[keep][m])
            kk, tt, vv = k[keep][m][o], np.minimum(T[keep][m][o], 0.8), iv[keep][m][o]
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
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.95)
        self.add_fixed_in_frame_mobjects(hint, title)
        self.remove(hint, title)
        with self.voiceover(
            "Put every expiry together and you have the series' Surface: two hundred and fifty-odd implied "
            "volatilities over strike and maturity, frozen on one morning, from the trades of that day. Every "
            "pricing model in this series will be calibrated to it and scored on it. The short-dated smiles, in "
            "front, are steep and high: it was the morning of a Federal Reserve decision, and the market was "
            "paying for the next few days' moves. Further back, the surface flattens out. <bookmark mark='a'/> "
            "And the grey lines are Black-Scholes' best effort, one flat volatility per expiry. It gets the level "
            "of each expiry right and nothing else."
        ) as vo:
            self.play(FadeIn(title), FadeIn(hint), Create(ax), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.004, run_time=3))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1, run_time=2))
            self.move_camera(theta=-40 * DEGREES, run_time=max(vo.until("a") - 0.5, 1.0))
            self.play(LaggedStart(*[Create(p_) for p_ in planes], lag_ratio=0.1, run_time=2))
            self.move_camera(theta=-30 * DEGREES, phi=72 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, pts, lines, planes)),
                                                                  FadeOut(hint), FadeOut(title)], run_time=1.5)
        self.clear_scene()

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
            "So the Surface gets its first row. Black-Scholes with one volatility per expiry misses the market's "
            f"implied volatilities by {row['rmse_in']:.2f} volatility points, weighted by vega, on the day it was "
            f"fitted, and by {row['rmse_out']:.2f} the next morning with its parameters held. It has no calendar "
            "arbitrage, and eleven parameters, one per expiry. <bookmark mark='a'/> The rows below are empty: the "
            "smile models of Part twelve, stochastic volatility and jumps in thirteen, rough volatility in "
            "fourteen, neural networks in seventeen. Each will be fitted to the same quotes and judged by the "
            "same numbers. One more number for later: Deribit's own volatility index, DVOL, computed the way the "
            f"VIX is, stood at {100 * d['dvol_ref']:.1f} percent that morning, a little above the at-the-money "
            f"thirty-day volatility, {100 * d['atm30']:.1f}, because it includes the smile's wings."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            self.play(FadeIn(rows[1], shift=UP * 0.2), Create(hl))
            self.play(FadeIn(unit))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.25, run_time=2))
            self.play(FadeIn(dv))
        self.wait(0.4)
        self.clear_scene()
