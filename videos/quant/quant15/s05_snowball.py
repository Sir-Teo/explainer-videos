from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, CASH, DELTA, GOOD, IV, OPT, PART, SPOT, VEGA, illustration, load


class Snowball(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("snowball")
        self.card()
        self.payoff(s)
        self.coupon(s)
        self.surface(s)
        self.greeks(s)

    def card(self):
        c = chapter_card(4, r"The snowball", r"What does a saver sell when she buys a 15\% coupon?", part=PART)
        with self.voiceover("Chapter four. The snowball."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def payoff(self, s):
        t = s["terms"]
        rows = VGroup(
            VGroup(label(r"every month after the third:", font_size=24, color=GREY_A),
                   label(rf"index $\ge$ {100 * t['ko']:.0f}\% of its start $\Rightarrow$ repaid, plus the coupon for the months "
                         r"held", font_size=24, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"every day:", font_size=24, color=GREY_A),
                   label(rf"index closes below {100 * t['ki']:.0f}\% $\Rightarrow$ knocked in", font_size=24, color=BAD))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(rf"after {t['months']} months, never knocked out:", font_size=24, color=GREY_A),
                   label(r"never knocked in $\Rightarrow$ the full coupon; knocked in $\Rightarrow$ the index's loss, "
                         r"one for one", font_size=24, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.6)
        eq = MathTex(r"\text{snowball} = \text{bond} + \text{coupon, while alive} - \text{down-and-in put}",
                     font_size=34, color=OPT).to_edge(DOWN, buff=1.2)
        note_ = wrapped_label(r"the name: the coupon accrues month by month, like a snowball rolling; the risk is the "
                              r"knock-in, which turns the note into the index itself", 11.0, 20, GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "The snowball, xueqiu in Chinese, was the best-selling structured product in China, linked mostly to "
            "the CSI 500 and CSI 1000 indices. Its terms fit on a card. Every month after the third, if the index "
            "is above its starting level, the note is repaid with its coupon for the months held. <bookmark mark='a'/> "
            "Every day, if the index closes below about three-quarters of its start, the note is knocked in. "
            "<bookmark mark='b'/> If it reaches maturity without being repaid, the buyer gets the full coupon if it "
            "never knocked in, and otherwise takes the index's loss, one for one. <bookmark mark='c'/> In option "
            "terms, the buyer owns a bond and a coupon, and has sold a down-and-in put. The coupon is the put's "
            "premium, paid in instalments."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def coupon(self, s):
        v = np.asarray(s["vols"])
        c = np.asarray(s["coupons"])
        g = axes([0.10, 0.34], [0, 0.30], x_length=6.4, y_length=4.2, xlabel=r"volatility of the index",
                 ylabel=r"fair coupon, a year", xticks=[0.12, 0.16, 0.20, 0.24, 0.28, 0.32], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda u: f"{100 * u:.0f}\\%", yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, v, c, OPT, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=OPT) for a, b in zip(v, c)])
        mk = Dot(ax.c2p(s["sigma"], s["coupon"]), radius=0.1, color=IV)
        mkl = label(rf"CSI 500, 2021--2023: {100 * s['sigma']:.0f}\% $\Rightarrow$ {100 * s['coupon']:.1f}\%", font_size=18,
                    color=IV).next_to(mk, RIGHT, buff=0.15)
        side = VGroup(
            wrapped_label(r"the coupon that makes the note worth exactly its price, by Monte Carlo under the risk-neutral "
                          r"measure (Part 4), rates 2\%", 4.4, 19, GREY_A),
            wrapped_label(r"the buyer is selling volatility: the more the index swings, the likelier the knock-in, the "
                          r"higher the fair coupon. A double-digit coupon is not a gift; it is the price of a crash",
                          4.4, 19, WHITE),
            wrapped_label(r"issuers sell below fair value and keep the difference: Henderson and Pearson (2011) found US "
                          r"retail notes priced about 8\% above their fair value; C\'el\'erier and Vall\'ee (2017) found "
                          r"European issuers raising headline rates through complexity", 4.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = illustration(r"24 months; knock-out 103\%, knock-in 75\%; 20{,}000 paths per point")
        with self.voiceover(
            "What coupon is fair? Price the note by simulation and solve for the coupon that makes it worth exactly "
            "what the buyer pays. <bookmark mark='a'/> It rises steeply with the index's volatility. At the CSI "
            f"500's volatility over 2021 to 2023, about {100 * s['sigma']:.0f} percent, the fair coupon is "
            f"{100 * s['coupon']:.1f} percent a year. The buyer is selling volatility, and a double-digit coupon is "
            "the price of a crash, not a gift. <bookmark mark='b'/> And issuers do not sell at fair value. Brian "
            "Henderson and Neil Pearson found US retail notes priced about eight percent above theirs; Claire "
            "Célérier and Boris Vallée found European issuers raising headline rates by making products more complex."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(mk), FadeIn(mkl), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, s):
        sp = np.asarray(s["spots"])
        mo = np.asarray(s["months"], float)
        Z = np.asarray(s["surface"])
        f = RegularGridInterpolator((mo, sp), Z, bounds_error=False, fill_value=None)
        ax = ThreeDAxes(x_range=[0.65, 1.10, 0.15], y_range=[0, 22, 6], z_range=[0.6, 1.3, 0.2], x_length=7.0,
                        y_length=5.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)
        surf = Surface(lambda u, w: ax.c2p(u, w, float(f((w, u)))), u_range=[0.65, 1.10], v_range=[0, 22],
                       resolution=(30, 22), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(BAD, 0.65), (IV, 0.9), (GOOD, 1.15)], axis=2)
        ki = VMobject(stroke_color=BARRIER, stroke_width=4).set_points_as_corners(
            [ax.c2p(0.75, w, float(f((w, 0.75))) + 0.02) for w in np.linspace(0, 22, 12)])
        hint = VGroup(label(r"index, relative to the note's start", font_size=22, color=SPOT),
                      label(r"months since issue", font_size=22, color=GREY_A),
                      label(r"value of the note, per 1 invested", font_size=22, color=OPT)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.1).to_corner(UL, buff=0.4)
        cliff = label(r"the knock-in line: below it, the note is the index", font_size=20, color=BARRIER).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, cliff)
        self.remove(hint, cliff)
        with self.voiceover(
            "Here is the note's value, not yet knocked in, over the index level and the months since issue. On the "
            "right, near the start, it is worth a little more than it cost: the coupon is accruing and repayment is "
            "near. <bookmark mark='a'/> On the left, the surface falls away toward the knock-in line. Cross it, and "
            "the note stops being a bond with a coupon and becomes a position in the index, a loss of a quarter or "
            "more on the day it happens. That edge is the cliff the whole product is built on."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(Create(ki), FadeIn(cliff))
            self.move_camera(theta=-60 * DEGREES, phi=66 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, ki)), FadeOut(hint),
                                                                  FadeOut(cliff)], run_time=1.5)
        self.clear_scene()

    def greeks(self, s):
        G = s["greeks"]
        S = np.array([r["S"] for r in G])
        dl = np.array([r["note_delta"] for r in G])
        vg = -np.array([r["note_vega"] for r in G])  # the dealer's: short the note
        g1 = axes([0.70, 1.05], [0, 2.0], x_length=5.6, y_length=3.4, xlabel=r"index, relative to start",
                  ylabel=r"dealer's hedge (index units per 1 of notes)", xticks=[0.75, 0.85, 0.95, 1.05], yticks=[0, 1, 2],
                  font_size=14)
        g2 = axes([0.70, 1.05], [-0.004, 0.012], x_length=5.6, y_length=3.4, xlabel=r"index, relative to start",
                  ylabel=r"dealer's vega (per vol point)", xticks=[0.75, 0.85, 0.95, 1.05], yticks=[0, 0.005, 0.01],
                  font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=1.0)
        above = S >= 0.75
        l1 = curve(g1.ax, S[above], dl[above], DELTA, stroke_width=3)
        l1b = curve(g1.ax, S[~above], dl[~above], DELTA, stroke_width=3)
        l2 = curve(g2.ax, S, vg, VEGA, stroke_width=3)
        z2 = DashedLine(g2.ax.c2p(0.70, 0), g2.ax.c2p(1.05, 0), stroke_color=GREY_C, stroke_width=1.2)
        bars = VGroup(*[DashedLine(g.ax.c2p(0.75, lo), g.ax.c2p(0.75, hi), stroke_color=BARRIER, stroke_width=2)
                        for g, lo, hi in ((g1, 0, 2.0), (g2, -0.004, 0.012))])
        i_hi = int(np.argmax(np.where(above, dl, -1)))
        d_hi, d_lo = dl[i_hi], dl[~above].mean()
        foot = wrapped_label(rf"the issuing broker sold the note and hedges by holding index futures: {d_hi:.1f} units per "
                             rf"unit of notes just above the knock-in, about {d_lo:.1f} once it is breached. The knock-in "
                             r"forces the hedger to sell into the fall it is part of; and above the barrier the dealer is "
                             r"long volatility, a supply it sells to the market (chapter 5)", 11.8, 19, GREY_A).to_edge(DOWN, buff=0.4)
        src = illustration(r"six months after issue, not yet knocked in (left of the line: knocked in); 30{,}000 paths, "
                           r"common random numbers", corner=UR)
        with self.voiceover(
            "Now the issuer's side. The broker that sold the note is short it, and hedges by holding index futures. "
            "Here is how many, six months in. As the index falls toward the knock-in, the hedge grows, to "
            f"{d_hi:.1f} times the notional just above the line. <bookmark mark='a'/> Then the barrier breaks, and "
            f"the hedge drops to about {d_lo:.1f}. On the day of the knock-in, the hedger must sell, into a falling "
            "market it is part of. <bookmark mark='b'/> And look at volatility. Above the barrier the dealer is long "
            "volatility, which it offsets by selling options in the market. Below it, that exposure collapses and "
            "even turns slightly short. Every snowball sold adds to both effects."
        ) as vo:
            self.play(FadeIn(g1), Create(l1), Create(bars[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l1b), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(z2), Create(l2), Create(bars[1]))
        self.wait(0.4)
        self.clear_scene()
