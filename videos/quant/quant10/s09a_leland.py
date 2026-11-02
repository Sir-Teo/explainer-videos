from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAIN, GAM, IMP, LOSS, OPT, PART, SPOT, THE, computed, load

C_ = {r"\Gamma": GAM, r"\sigma_L^2": IMP, r"\sigma^2": IMP, r"\sigma": IMP, r"k": LOSS, r"\Delta t": THE,
      r"S": SPOT, r"S^2": SPOT}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class Leland(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.landscape(load("leland_grid"))
        self.derive()
        self.check(load("discrete"), load("leland_grid"))
        self.limit(load("kabanov"))

    def card(self):
        c = chapter_card(10, r"Paying for it: Leland's volatility", r"What does hedging cost?", lit=(1985,),
                         part=PART)
        with self.voiceover("Chapter ten. Paying for it: Leland's volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def landscape(self, lg):
        N = np.asarray(lg["N"], float)
        kb = np.asarray(lg["k"], float) * 1e4
        tot = np.asarray(lg["total"], float)
        lx = np.log10(N)
        zmax = 3.5
        ax = ThreeDAxes(x_range=[lx[0], lx[-1], 0.5], y_range=[0, 50, 10], z_range=[0, zmax, 1], x_length=7.4,
                        y_length=5.4, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)

        def height(a, b):
            col = np.array([np.interp(a, lx, tot[j]) for j in range(len(kb))])
            return float(min(np.interp(b, kb, col), zmax))

        surf = Surface(lambda u, v: ax.c2p(u, v, height(u, v)), u_range=[lx[0], lx[-1]], v_range=[0, 50],
                       resolution=(24, 20))
        surf.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0.3), (GAM, 1.5), (LOSS, zmax)], axis=2)
        surf.set_style(fill_opacity=0.6, stroke_width=0.3, stroke_color=GREY_D)
        best = np.array([np.log10(b) for b in lg["best"]])
        ridge = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_smoothly(
            [ax.c2p(a, b, height(a, b) + 0.03) for a, b in zip(best, kb)])
        balls = VGroup(*[Dot3D(ax.c2p(a, b, height(a, b) + 0.03), radius=0.07, color=YELLOW) for a, b in zip(best, kb)])
        hint = VGroup(label(r"hedges per quarter (log scale)", font_size=24, color=THE),
                      label(r"one-way cost, basis points", font_size=24, color=LOSS),
                      label(r"expected cost $+$ one sd of the hedging error", font_size=24, color=GAM)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        tab = VGroup(*[MathTex(rf"{k_:g}\,\text{{bp}}:\ N^* = {b}", font_size=26, color=YELLOW if k_ else GREY_A)
                       for k_, b in zip(kb, lg["best"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tab.to_corner(UR, buff=0.4)
        foot = note(r"short a 3-month at-the-money call, $\sigma = 20\%$; 10,000 paths per cell", font_size=20)
        foot.to_corner(DR, buff=0.3)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.88)
        for m in (hint, tab, foot):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        free_best = lg["best"][0]
        with self.voiceover(
            "Every rebalance pays a cost, a fraction k of the value traded. Here is what that does to the last "
            "chapter's short call: across, the hedges in the quarter; deep, the cost in basis points; up, the "
            "expected cost plus one standard deviation of the hedging error. <bookmark mark='a'/> At zero cost "
            f"more hedging always helps: the best in our grid is {free_best} hedges, the most we tried. As costs "
            "rise the far end lifts and a valley appears. <bookmark mark='b'/> The gold ridge traces its floor: at "
            f"a quarter of a percent the best is {lg['best'][4]} hedges, about {lg['best'][4] / 13:.0f} a week. "
            "Pause and predict: costs double. More often, or less? Less: the ridge moves left."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), FadeIn(foot), run_time=1.5)
            self.play(FadeIn(surf), run_time=2)
            vo.wait_until("a")
            self.move_camera(theta=-30 * DEGREES, phi=62 * DEGREES, run_time=2)
            vo.wait_until("b")
            self.play(Create(ridge), FadeIn(balls), FadeIn(tab), run_time=2)
            self.move_camera(theta=-45 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)]))], run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            row(r"|\delta\Delta|", r"\approx", r"\Gamma", r"\,|\delta S|", r"=", r"\Gamma", r"S", r"\sigma",
                r"\sqrt{\Delta t}", r"\,|Z|"),
            row(r"\mathbb E[\text{cost}]", r"=", r"\tfrac{k}{2}", r"S", r"\,\mathbb E|\delta\Delta|", r"=",
                r"\tfrac{k}{2}", r"\Gamma", r"S^2", r"\sigma", r"\sqrt{\Delta t}\sqrt{2/\pi}"),
            row(r"\frac{\mathbb E[\text{cost}]}{\Delta t}", r"=", r"\tfrac12", r"\Gamma", r"S^2", r"\cdot",
                r"\frac{\sigma\,k\sqrt{2/\pi}}{\sqrt{\Delta t}}"),
            row(r"\sigma_L^2", r"=", r"\sigma^2", r"\Big(1 + \sqrt{\tfrac{2}{\pi}}\,\frac{", r"k", r"}{",
                r"\sigma", r"\sqrt{\Delta t}}\Big)", fs=40),
        ]
        whys = [why(r"over one step delta moves by gamma times the stock's move"),
                why(r"$k$ the round-trip cost; $\mathbb E|Z| = \sqrt{2/\pi}$"),
                why(r"per unit of time: it looks like extra variance, times $\tfrac12\Gamma S^2$"),
                why(r"absorb it into the volatility: Leland (1985)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.75, edge=6.9)
        foot = note(r"error $\propto \sqrt{\Delta t}$ (chapter 9), cost $\propto 1/\sqrt{\Delta t}$: the valley",
                    font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Hayne Leland's insight, in 1985: the cost can be priced. Over one step, delta moves by gamma times "
            "the stock's move. <bookmark mark='a'/> Each trade costs half the round trip on its value, and a normal "
            "move's average size is root two over pi. <bookmark mark='b'/> Per unit of time the cost is half gamma "
            "S squared, chapter seven's factor, times something growing like one over root delta t. "
            "<bookmark mark='c'/> So absorb it into the volatility: sell and hedge at Leland's sigma L. Error "
            "shrinks like root delta t, cost grows like its inverse: the valley."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self, d, lg):
        card = lab_card(r"Leland's volatility", [
            "def leland_vol(sigma, k, dt):",
            "    return sigma * np.sqrt(1 + np.sqrt(2/np.pi)",
            "                           * k / (sigma * np.sqrt(dt)))",
            "",
            "sL = leland_vol(0.2, 2 * k, T / N)",
            "delta_hedge(t, S, K, T, sL, position=-1,",
            "            sigma_price=sL, cost=k, cost_ends=False)",
        ], source="explainer/quant/house/bs.py, hedge.py", width=7.0).to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.5)
        lab = lg["lab"]
        k = d["cost"]
        rows = VGroup(
            label(rf"weekly hedging, cost {100 * k:.2f}\% one way, 40,000 paths:", font_size=24, color=GREY_A),
            MathTex(rf"\text{{priced at }}20\%:\ \text{{mean}}\ {d['naive_mean']:+.2f}", font_size=30, color=LOSS),
            MathTex(rf"\text{{priced at }}\sigma_L = {100 * d['sigma_leland']:.1f}\%:\ \text{{mean}}\ "
                    rf"{d['leland_mean']:+.2f}", font_size=30, color=OPT),
            MathTex(rf"\text{{first hedge and unwind}}:\ {d['end_costs']:.2f}", font_size=28, color=GREY_B),
            MathTex(rf"\text{{without them}}:\ {d['leland_mid_mean']:+.2f}", font_size=30, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        with self.voiceover(
            "In the House it is three lines. <bookmark mark='a'/> Problem four: a round trip of point two percent "
            f"at twenty percent volatility needs {100 * lab['daily']:.1f} percent hedging daily, "
            f"{100 * lab['weekly']:.1f} weekly. <bookmark mark='b'/> The check, weekly, a quarter percent each way: "
            f"priced at twenty the seller loses {-d['naive_mean']:.2f}; at Leland's {100 * d['sigma_leland']:.1f}, "
            f"{-d['leland_mean']:.2f}, and the rest is the first hedge and the unwind, {d['end_costs']:.2f}, which "
            f"the formula leaves out. Without them: {d['leland_mid_mean']:+.2f}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"leland_vol(0.2, 0.002, 1/252)  ->  {lab['daily']:.4f}",
                                 f"leland_vol(0.2, 0.002, 1/52)   ->  {lab['weekly']:.4f}"])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self, kb):
        rows_ = kb["rows"]
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"hedges", r"$\sigma_L$", r"premium",
                                                                        r"mean P\&L", r"sd")])
        xs = [-4.2, -2.2, -0.2, 1.9, 3.9]
        for h_, x in zip(head, xs):
            h_.move_to([x, 0, 0])
        tab = VGroup(head)
        for i, r_ in enumerate(rows_):
            cells = VGroup(MathTex(f"{r_['N']:,}".replace(",", "{,}"), font_size=28),
                           MathTex(rf"{100 * r_['sigma_L']:.1f}\%", font_size=28, color=IMP),
                           MathTex(rf"{r_['premium']:.2f}", font_size=28, color=OPT),
                           MathTex(rf"{r_['mean']:+.2f}", font_size=28),
                           MathTex(rf"{r_['sd']:.2f}", font_size=28))
            for c_, x in zip(cells, xs):
                c_.move_to([x, -(i + 1) * 0.55, 0])
            tab.add(cells)
        tab.move_to(UP * 0.6)
        title = label(rf"Leland's strategy, cost {100 * kb['k']:.2f}\% one way, ever more often", font_size=28)
        title.to_edge(UP, buff=0.4)
        cap = wrapped_label(rf"a share costs {kb['share']:.0f}: the call can never be worth more. Soner, Shreve "
                            r"and Cvitani\'c (1995): with costs, the cheapest perfect hedge of a call is to buy the "
                            r"share. Kabanov and Safarian (1997): Leland's error does not vanish in the limit.",
                            12.0, 22, GREY_A).to_edge(DOWN, buff=0.4)
        sd_first, sd_last = rows_[0]["sd"], rows_[-1]["sd"]
        kab_line = (f"In our runs its spread is still shrinking, {sd_first:.2f} to {sd_last:.2f}: the failure is in "
                    "the limit, and in the price." if sd_last < sd_first else
                    f"In our runs its spread stops shrinking: {sd_first:.2f} to {sd_last:.2f}.")
        with self.voiceover(
            "Follow the recipe to its end and it breaks. Fix the cost, hedge ever more often: sigma L climbs from "
            f"{100 * rows_[0]['sigma_L']:.0f} percent to {100 * rows_[-1]['sigma_L']:.0f}, and the premium from "
            f"{rows_[0]['premium']:.2f} to {rows_[-1]['premium']:.2f}, without bound in the limit. <bookmark mark='a'/> Soner, Shreve and Cvitanic proved in 1995 that the "
            "cheapest sure cover for a call with costs is to buy the share; Kabanov and Safarian showed in 1997 "
            f"that with a constant cost Leland's error does not go to zero. {kab_line} The practical answer is a "
            "band where you do not trade: Parts eleven and seventeen."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3, run_time=3), FadeIn(computed()))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
