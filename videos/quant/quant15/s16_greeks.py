from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, IV, OPT, PART, SPOT, VEGA, illustration, load


class Greeks(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("snowball")
        g = load("greeks3d")
        self.card()
        self.surface(s)
        self.delta3d(g)
        self.gamma3d(g)
        self.vega3d(g)
        self.derive()
        self.bumps(load("bump_curve"))

    def card(self):
        c = chapter_card(8, r"The issuer's Greeks, in three dimensions", r"What does the bank that sold the snowball "
                         r"have to trade, and when?", part=PART)
        with self.voiceover("Chapter eight. The issuer's Greeks, in three dimensions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def surface(self, s):
        sp = np.asarray(s["spots"])
        mo = np.asarray(s["months"], float)
        Z = np.asarray(s["surface"])
        Zk = np.asarray(s["surface_ki"])
        f = RegularGridInterpolator((mo, sp), Z, bounds_error=False, fill_value=None)
        fk = RegularGridInterpolator((mo, sp), Zk, bounds_error=False, fill_value=None)
        ax = ThreeDAxes(x_range=[0.65, 1.10, 0.15], y_range=[0, 22, 6], z_range=[0.6, 1.3, 0.2], x_length=7.0,
                        y_length=5.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)
        surf = Surface(lambda u, w: ax.c2p(u, w, float(f((w, u)))), u_range=[0.65, 1.10], v_range=[0, 22],
                       resolution=(30, 22), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(BAD, 0.65), (IV, 0.9), (GOOD, 1.15)], axis=2)
        sheet = Surface(lambda u, w: ax.c2p(u, w, float(fk((w, u)))), u_range=[0.65, 1.10], v_range=[0, 22],
                        resolution=(24, 16), fill_opacity=0.45, stroke_width=0.2, stroke_color=GREY_D)
        sheet.set_fill(BAD, opacity=0.4)
        ki = VMobject(stroke_color=BARRIER, stroke_width=4).set_points_as_corners(
            [ax.c2p(0.75, w, float(f((w, 0.75))) + 0.02) for w in np.linspace(0, 22, 12)])
        hint = VGroup(label(r"index, relative to the note's start", font_size=22, color=SPOT),
                      label(r"months since issue", font_size=22, color=GREY_A),
                      label(r"value of the note, per 1 invested", font_size=22, color=OPT)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.1).to_corner(UL, buff=0.4)
        cliff = label(r"the knock-in line: below it, the note is the index", font_size=20, color=BARRIER).to_corner(DR, buff=0.4)
        cliff2 = label(r"red sheet: the same note, already knocked in", font_size=20, color=BAD).next_to(cliff, UP, buff=0.15)
        cliff2.align_to(cliff, RIGHT)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, cliff, cliff2)
        self.remove(hint, cliff, cliff2)
        with self.voiceover(
            "Here is the note's value, not yet knocked in, over the index level and the months since issue. Near "
            "the start it is worth a little more than it cost. <bookmark mark='a'/> On the left, the surface falls away toward the knock-in line. Cross it, and "
            "the note stops being a bond with a coupon and becomes a position in the index, a loss of a quarter or "
            "more on the day it happens. <bookmark mark='b'/> Underneath, in red, the same note once it has knocked "
            "in: it has stepped off the upper surface onto a lower one, for good, even if the index recovers. The "
            "gap between the two sheets is the cliff the product is built on; every Greek we draw next is that cliff, "
            "differentiated."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(Create(ki), FadeIn(cliff))
            self.move_camera(theta=-60 * DEGREES, phi=66 * DEGREES, run_time=3)
            vo.wait_until("b")
            self.play(Create(sheet), FadeIn(cliff2), run_time=2)
            self.move_camera(theta=-160 * DEGREES, phi=78 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, ki, sheet)), FadeOut(hint),
                                                                  FadeOut(cliff), FadeOut(cliff2)], run_time=1.5)
        self.clear_scene()

    def greek3d(self, g, which):
        sp = np.asarray(g["spots"])
        mo = np.asarray(g["months"], float)
        if which == "gamma":  # the slope of the delta grid: steadier than second differences of noisy prices
            A = np.gradient(np.asarray(g["alive_delta"], float), sp, axis=1)
            K = np.gradient(np.asarray(g["ki_delta"], float), sp, axis=1)
        else:
            A = np.asarray(g[f"alive_{which}"], float)
            K = np.asarray(g[f"ki_{which}"], float)
        if which == "delta":  # show the hedge the issuer holds: minus its delta, in index units per 1 of notes
            A, K = -A, -K
        lo = float(np.nanpercentile(np.concatenate([A.ravel(), K.ravel()]), 2))
        hi = float(np.nanpercentile(np.concatenate([A.ravel(), K.ravel()]), 98))
        if lo > 0:
            lo = 0.0
        if hi < 0:
            hi = 0.0
        A, K = np.clip(A, lo, hi), np.clip(K, lo, hi)
        fa = RegularGridInterpolator((mo, sp), A, bounds_error=False, fill_value=None)
        fk = RegularGridInterpolator((mo, sp), K, bounds_error=False, fill_value=None)
        zl = 3.0
        sc = zl / (hi - lo)
        ax = ThreeDAxes(x_range=[0.66, 1.12, 0.1], y_range=[0, 23, 6], z_range=[0, zl, 1], x_length=7.0, y_length=5.0,
                        z_length=zl, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                              "stroke_width": 2}).shift(DOWN * 0.7)

        def z(v):
            return (v - lo) * sc

        col = {"delta": DELTA, "gamma": QC.GAMMA, "vega": VEGA}[which]
        up = Surface(lambda u, w: ax.c2p(u, w, z(float(fa((w, u))))), u_range=[0.755, 1.12], v_range=[0, 23],
                     resolution=(26, 20), fill_opacity=0.85, stroke_width=0.25, stroke_color=GREY_D)
        up.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0), (col, zl * 0.6), (WHITE, zl)], axis=2)
        dn = Surface(lambda u, w: ax.c2p(u, w, z(float(fk((w, u))))), u_range=[0.66, 1.12], v_range=[0, 23],
                     resolution=(22, 14), fill_opacity=0.4, stroke_width=0.2, stroke_color=GREY_D)
        dn.set_fill(BAD, opacity=0.4)
        zero = Polygon(ax.c2p(0.66, 0, z(0)), ax.c2p(1.12, 0, z(0)), ax.c2p(1.12, 23, z(0)), ax.c2p(0.66, 23, z(0)),
                       stroke_width=1, stroke_color=GREY_C, fill_color=GREY_D, fill_opacity=0.15)
        kil = Line(ax.c2p(0.75, 0, z(0)), ax.c2p(0.75, 23, z(0)), stroke_color=BARRIER, stroke_width=4)
        title = {"delta": r"the issuer's hedge: index futures held per 1 of notes",
                 "gamma": r"the issuer's gamma: how fast that hedge changes",
                 "vega": r"the issuer's vega, per vol point"}[which]
        hint = VGroup(label(title, font_size=22, color=col),
                      label(r"spot 0.66 to 1.12 of the start; months 0 to 23; red: knocked in", font_size=18,
                            color=GREY_A),
                      label(rf"range shown: {lo:.3g} to {hi:.3g}; grey plane: zero", font_size=18, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.35)
        return {"ax": ax, "up": up, "dn": dn, "zero": zero, "kil": kil, "hint": hint}

    def _g3play(self, vo, o):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-118 * DEGREES, zoom=0.82)
        self.add_fixed_in_frame_mobjects(o["hint"])
        self.remove(o["hint"])
        self.play(FadeIn(o["hint"]), Create(o["ax"]), FadeIn(o["zero"]), Create(o["kil"]), Create(o["up"]), run_time=3)
        vo.wait_until("a")
        self.play(Create(o["dn"]), run_time=2)
        self.move_camera(theta=-55 * DEGREES, phi=70 * DEGREES, run_time=3)
        vo.wait_until("b")
        self.move_camera(theta=-150 * DEGREES, phi=60 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))

    def _g3end(self, o):
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(o["ax"], o["up"], o["dn"], o["zero"],
                                                                                 o["kil"])), FadeOut(o["hint"])],
                         run_time=1.2)
        self.clear_scene()

    def delta3d(self, g):
        o = self.greek3d(g, "delta")
        sp, mo = np.asarray(g["spots"]), np.asarray(g["months"], float)
        A, K = np.asarray(g["alive_delta"], float), np.asarray(g["ki_delta"], float)
        j6 = int(np.argmin(np.abs(mo - 6)))
        above = sp > 0.755
        h_above = float(np.max(-A[j6][above]))
        s_above = float(sp[above][np.argmax(-A[j6][above])])
        h_ki = float(np.mean(-K[j6][sp < 0.75]))
        with self.voiceover(
            "Start with the hedge: how many index futures the issuer holds per unit of notes. Far above the "
            "barrier, near the knock-out, it is modest. As the index falls toward the knock-in it climbs into "
            f"a ridge: six months in, it peaks at {h_above:.2f} times the notional, at a spot of {s_above:.2f}. "
            "<bookmark mark='a'/> Then it falls off the cliff, onto the red sheet of knocked-in notes, where "
            f"the hedge is about {h_ki:.2f}: the note has become the index, and the issuer is short it. "
            "<bookmark mark='b'/> Seen along the barrier, the drop is the trade the issuer must make on the "
            "day of a knock-in. It sells the difference into a market that has just fallen."
        ) as vo:
            self._g3play(vo, o)
        self._g3end(o)

    def gamma3d(self, g):
        o = self.greek3d(g, "gamma")
        sp, mo = np.asarray(g["spots"]), np.asarray(g["months"], float)
        A = np.gradient(np.asarray(g["alive_delta"], float), sp, axis=1)
        j6 = int(np.argmin(np.abs(mo - 6)))
        m_above = float(np.max(np.abs(A[j6][sp > 0.755])))
        with self.voiceover(
            "Now the gamma: how fast that hedge must change as the index moves. Over most of the surface it is "
            "small. <bookmark mark='a'/> Along the knock-in line it spikes, because the hedge is steep there "
            f"and about to jump; six months in, its largest size above the barrier is {m_above:.1f} per unit "
            "of spot. And there are ripples at each monthly knock-out date, where a note can vanish. "
            "<bookmark mark='b'/> Gamma is a promise to trade: to buy as the index falls toward the barrier, in "
            "amounts that grow as it nears."
        ) as vo:
            self._g3play(vo, o)
        self._g3end(o)

    def vega3d(self, g):
        o = self.greek3d(g, "vega")
        sp, mo = np.asarray(g["spots"]), np.asarray(g["months"], float)
        A = np.asarray(g["alive_vega"], float)
        j6 = int(np.argmin(np.abs(mo - 6)))
        above = sp > 0.755
        v_pk = float(np.max(A[j6][above]))
        s_pk = float(sp[above][np.argmax(A[j6][above])])
        i_m, i_s = np.unravel_index(np.argmax(A[:, above]), A[:, above].shape)
        m_pk, s_pk2 = int(mo[i_m]), float(sp[above][i_s])
        with self.voiceover(
            "And the vega. Above the barrier the issuer is long volatility, a hill: it owns the down-and-in "
            "put the buyer sold, and more volatility makes a knock-in likelier. Six months in, the hill peaks "
            f"at {v_pk:.4f} per vol point, at a spot of {s_pk:.2f}, between the barrier and the start. "
            f"<bookmark mark='a'/> Over the whole grid, the peak is at month {m_pk} and spot {s_pk2:.2f}. That is "
            "what practitioners call peak vega: not at the barrier, where a knock-in is nearly certain, but on the way "
            "down to it. "
            "<bookmark mark='b'/> On the red sheet, once knocked in, the put is a deep vanilla put with little vega "
            "left, and the hill is gone."
        ) as vo:
            self._g3play(vo, o)
        self._g3end(o)

    def derive(self):
        rows = [
            cmath(r"\hat\Delta", r"=", r"\frac{V(S + h) - V(S - h)}{2h}", font_size=38, colors={r"\hat\Delta": DELTA}),
            cmath(r"\text{error}", r"=", r"O(h^2) + O\Big(\frac{\sigma_{MC}}{h\sqrt N}\Big)", font_size=36,
                  colors={r"\text{error}": BAD}),
            cmath(r"\operatorname{Var}\big[\hat\Delta_{\text{CRN}}\big]", r"=", r"O\Big(\frac{1}{hN}\Big)\ \text{near a "
                  r"barrier}", font_size=36, colors={r"\operatorname{Var}\big[\hat\Delta_{\text{CRN}}\big]": IV}),
            cmath(r"\mathcal V_{\text{issuer}}", r"=", r"-\mathcal V_{\text{note}} = \mathcal V_{DIP} - "
                  r"\mathcal V_{\text{coupon strip}}", font_size=36, colors={r"\mathcal V_{\text{issuer}}": VEGA}),
        ]
        whys = [why(r"a central difference: bump the spot both ways and reprice"),
                why(r"the Taylor remainder against the noise of a difference of two independent estimates: a small $h$ "
                    r"drowns in noise"),
                why(r"with common random numbers the noise cancels on smooth payoffs, but near a barrier a path flips "
                    r"between knocked in and not as $h$ crosses it: an indicator jumps on a set of measure $O(h)$"),
                why(r"the decomposition of chapter 1: the issuer owns the put and owes the coupons. The put's vega is "
                    r"largest near the barrier; once knocked in, it is a deep vanilla put with little vega")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.8, edge=6.9)
        pp = pause_card(r"Where is the issuer's vega largest: at the start, on the way down to the knock-in, or after it?",
                        width=6.0).to_corner(DR, buff=0.3)
        with self.voiceover(
            "How are these numbers made? By bumping the spot up and down by h and repricing. "
            "<bookmark mark='a'/> With independent simulations, the error is the Taylor remainder, h squared, plus "
            "noise divided by h, which explodes as h shrinks. <bookmark mark='b'/> Common random numbers cancel most "
            "of the noise, for smooth payoffs. Near a barrier, paths flip state as the bump crosses them, and the "
            "variance returns, of order one over h N. "
            "<bookmark mark='c'/> And the issuer's vega sign comes from chapter one: it owns the down-and-in put and "
            "owes the coupons. <bookmark mark='p'/> Where is it largest? On the way down to the knock-in, not at it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("p")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def bumps(self, b):
        h = np.asarray(b["h"])
        crn = np.asarray(b["crn"])
        ind = np.asarray(b["independent"])
        lh = np.log10(h)
        allv = np.concatenate([crn.ravel(), ind.ravel()])
        lo, hi = float(np.percentile(allv, 0)) - 0.1, float(np.percentile(allv, 100)) + 0.1
        g = axes([lh[0] - 0.1, lh[-1] + 0.1], [lo, hi], x_length=7.0, y_length=4.2, xlabel=r"bump size $h$ (log scale)",
                 ylabel=r"the issuer's delta at spot 0.77", xticks=list(lh),
                 xfmt=lambda u: f"{10 ** u:.4g}", yticks=[round(lo + 0.1, 1), round(hi - 0.1, 1)], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        b1 = seed_band(ax, lh, ind, BAD)
        b2 = seed_band(ax, lh, crn, GOOD)
        leg = legend([(BAD, r"independent paths for the up and down prices, 3 seeds"),
                      (GOOD, r"common random numbers, 3 seeds")], font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        spread_ind = float(np.mean(ind.max(0) - ind.min(0)))
        spread_crn = float(np.mean(crn.max(0) - crn.min(0)))
        sp_small = float(crn[:, 0].max() - crn[:, 0].min())
        sp_big = float(crn[:, -1].max() - crn[:, -1].min())
        side = VGroup(
            wrapped_label(rf"mean spread across seeds: {spread_ind:.2f} with independent paths, {spread_crn:.2f} with "
                          r"common ones", 4.6, 19, WHITE),
            wrapped_label(rf"with common numbers the seeds disagree by {sp_small:.2f} at the smallest bump and "
                          rf"{sp_big:.2f} at the largest: near the barrier, a small bump is noisy even with the same "
                          r"paths, and a large one is biased. Chapter 18 shows the fix", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"six months in, not knocked in, spot 0.77 (the barrier is 0.75); 30{,}000 paths per price")
        with self.voiceover(
            "Watch the trade-off happen. The issuer's delta at a spot of 0.77, two points above the barrier, "
            "computed with five bump sizes and three seeds each. <bookmark mark='a'/> In red, independent paths for "
            f"the up and the down price: the seeds disagree by {spread_ind:.2f} on average, and worst at the "
            f"smallest bump. <bookmark mark='b'/> In green, common random numbers: the spread falls to "
            f"{spread_crn:.2f}, but the smallest bump still wobbles, by {sp_small:.2f}, as paths flip across the "
            "barrier, and the largest straddles it and is biased. There is no free bump size near a cliff."
            " Next: what happened when those Greeks met a falling market."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(b1[0]), Create(b1[1]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2[0]), Create(b2[1]), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
