from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, axes3, fixed, load, real_data


def _yr(d):
    d = int(d)
    x = date(d // 10000, (d // 100) % 100, d % 100)
    return x.year + (x.timetuple().tm_yday - 1) / 365


class ETP(VoiceoverScene, ThreeDScene):
    def construct(self):
        v = load("vx_etp")
        self.card()
        self.ribbon(v)
        self.derive()
        self.lab(v)
        self.rebuild(v)

    def card(self):
        c = chapter_card(14, r"VIX futures, the roll and short-volatility notes", r"How do you sell volatility to the public?",
                         part=PART)
        with self.voiceover("Chapter fourteen. VIX futures, the roll, and short-volatility notes."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ribbon(self, v):
        t = np.array([_yr(d) for d in v["days"]])
        curves = v["curve"]
        ax = axes3([2017.4, 2018.25, 0.2], [0, 220, 50], [10, 35, 5], x_length=7.6, y_length=4.4, z_length=3.0)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        lines = VGroup()
        i5 = v["i_feb5"]
        for i in list(range(0, len(t), 3)) + [i5 - 1, i5]:
            c = np.asarray(curves[i])
            col = BAD if i == i5 else (interpolate_color(ManimColor(QC.SPOT), ManimColor(IV), i / len(t)))
            pts = [ax.c2p(t[i], a, float(np.clip(b, 10, 35))) for a, b in c]
            if len(pts) > 1:
                lines.add(VMobject(color=col, stroke_width=5 if i == i5 else 2).set_points_as_corners(pts))
        vix = [x for x in v["vix"]]
        spot = VGroup(*[Dot3D(ax.c2p(t[i], 0, float(np.clip(x, 10, 35))), radius=0.03, color=WHITE, resolution=(3, 3))
                        for i, x in enumerate(vix) if x is not None and i % 2 == 0])
        hint = VGroup(label(r"across: date (June 2017 -- March 2018)", font_size=18, color=GREY_B),
                      label(r"depth: days to the future's expiry", font_size=18, color=GREY_B),
                      label(r"up: settlement price (VIX points); white: the VIX itself", font_size=18, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        red = label(r"red: 5 February 2018", font_size=20, color=BAD).to_corner(UR, buff=0.4)
        src = real_data(r"Cboe Futures Exchange: VX daily settlements")
        fixed(self, hint, red, src)
        cg, ms = 100 * v["contango"], 100 * v["median_slope"]
        f0, f1 = v["front"]
        with self.voiceover(
            "A VIX future settles, at expiry, on the VIX of that morning. Here is the whole futures curve, every day "
            "from June 2017 to March 2018, as a ribbon: date across, days to expiry going back, price up, and the VIX "
            "itself as white dots at the front. <bookmark mark='a'/> Almost every day the curve slopes up: futures above "
            f"the spot index, further-out futures higher still. The second month sat above the first on {cg:.0f} "
            f"percent of these days, by {ms:.1f} percent at the median. <bookmark mark='b'/> Then the red line. On the "
            f"fifth of February 2018 the front future went from {f0:.2f} to {f1:.2f}, and the curve folded over: "
            "backwardation, the near future above the far."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(src))
            self.play(LaggedStart(*[Create(x) for x in lines[:-2]], lag_ratio=0.02, run_time=4), FadeIn(spot))
            vo.wait_until("a")
            self.move_camera(theta=-25 * DEGREES, run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lines[-1]), FadeIn(red))
            self.move_camera(theta=-70 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, lines, spot)), FadeOut(hint),
                                                                  FadeOut(red), FadeOut(src)], run_time=1)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"F^{VX}_t(T)", r"=", r"\mathbb{E}^Q_t[\text{VIX}_T] \;\le\; \sqrt{\mathbb{E}^Q_t[\text{VIX}_T^2]}",
                      font_size=38, colors={r"F^{VX}_t(T)": IV}),
                cmath(r"w_1", r"=", r"\frac{d_r}{d_t},\quad w_2 = 1 - w_1,\quad r_t = \frac{w_1F_1' + w_2F_2'}{w_1F_1 + w_2F_2} - 1",
                      font_size=34, colors={r"w_1": LV}),
                cmath(r"\text{roll yield}", r"\approx", r"\frac{F_2 - F_1}{F_1}\ \text{per month, to the short}", font_size=36),
                cmath(r"N_{t+1}", r"=", r"N_t(1 + L\,r),\qquad \text{trade} = (L^2 - L)\,r\,N_t", font_size=38,
                      colors={r"N_{t+1}": OPT})]
        whys = [why(r"a future on the index, not on variance: Jensen puts it below the forward variance strike, so it is "
                    r"not replicated by options"),
                why(r"the short-term futures index: hold the first and second months, shifting weight daily ($d_r$ days "
                    r"left in the roll period of $d_t$)"),
                why(r"in contango each future drifts down toward spot as it ages: the seller of the index earns the slope"),
                why(r"a daily-reset note with leverage $L$; to restore exposure $L N_{t+1}$ the issuer trades $(L^2 - L) r N_t$: "
                    r"for $L = -1$ and $L = 2$ alike, $+2rN_t$, buying after a rise (Cheng and Madhavan 2009)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.65, edge=6.9)
        with self.voiceover(
            "Four lines. A VIX future is the expected VIX at expiry; the VIX is a square root of variance, so by "
            "Jensen the future sits below the root of the forward variance: no strip of options replicates it. "
            "<bookmark mark='a'/> The short-term index holds the first and second months, shifting weight a little "
            "every day. <bookmark mark='b'/> In contango each future drifts down toward spot: the short collects the "
            "roll. <bookmark mark='c'/> And a note promising L times each day's return must, after a rise of r, trade L "
            "squared minus L, times r, times its value. For L of minus one that is plus two r N: buy after a rise, as "
            "Cheng and Madhavan showed in 2009; the same for a doubly leveraged long note."
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

    def lab(self, v):
        card = lab_card(r"a futures index and a -1x note", [
            "def vx_index(days, settle, expiries):",
            "    for p, d in zip(days, days[1:]):",
            "        e1, e2, w1 = weights(p)           # roll from e1 to e2",
            "        num = w1 * settle[e1][d] + (1 - w1) * settle[e2][d]",
            "        den = w1 * settle[e1][p] + (1 - w1) * settle[e2][p]",
            "        ret.append(num / den - 1)",
            "",
            "def inverse_note(ret, L=-1.0, floor=0.0):",
            "    for r in ret:",
            "        n = max(n * (1 + L * r), floor)",
            "",
            "def rebalance_flow(L, r, N): return (L * L - L) * r * N",
        ], source="explainer/quant/house/volsurface.py (abridged)", width=8.0).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        r5 = v["feb5_ret"]
        out = [f"index return, 5 Feb 2018: {100 * r5:+.1f}%",
               f"-1x note, 5 Feb 2018:    {100 * v['note_feb5']:+.1f}%",
               f"note, June to December 2017: {100 * v['note_jun_dec']:+.0f}%",
               f"hedge purchase at the close: {v['flow_feb5']:.2f} x the note's value"]
        with self.voiceover(
            "In the House, the index is a loop over days, weights moving from the first month to the second, and the "
            "note is a running product of one minus each day's return, floored at zero. <bookmark mark='a'/> Feed it "
            "Cboe's settlement prices. On the fifth of February 2018 the rebuilt index rose "
            f"{100 * r5:.1f} percent, so the inverse note lost the same: almost everything."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.6)
        self.clear_scene()

    def rebuild(self, v):
        t = np.array([_yr(d) for d in v["days"]])
        lvl, note = np.asarray(v["level"]), np.asarray(v["note"])
        flow = np.asarray(v["flow"])
        g = axes([2017.4, 2018.25], [0, 2.0], x_length=7.6, y_length=3.0, ylabel=r"value, 1 June 2017 = 1",
                 xticks=[], yticks=[0, 1, 2], font_size=15).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        tr = ValueTracker(2)

        def upto(y, col, sw=3):
            i = int(max(tr.get_value(), 2))
            return curve(g.ax, t[:i], np.clip(y[:i], 0, 2.0), col, stroke_width=sw)
        ci = always_redraw(lambda: upto(lvl / 100, LV, 2))
        cn = always_redraw(lambda: upto(note, OPT, 4))
        leg = legend([(LV, r"short-term VIX futures index (rebuilt)"), (OPT, r"$-1\times$ daily note")], font_size=17
                     ).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        g2 = axes([2017.4, 2018.25], [-0.4, 2.0], x_length=7.6, y_length=2.2, ylabel=r"close-of-day purchase, "
                  r"$\times$ the note's value", xticks=[2017.5, 2017.75, 2018.0, 2018.25],
                  xfmt=lambda u: {2017.5: "Jul 17", 2017.75: "Oct 17", 2018.0: "Jan 18", 2018.25: "Apr 18"}[round(u * 4) / 4],
                  yticks=[0, 1, 2], font_size=15).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        rel = flow / np.maximum(note[:-1], 1e-9)
        bars = VGroup(*[Line(g2.ax.c2p(a, 0), g2.ax.c2p(a, float(np.clip(b, -0.4, 2.0))), color=BAD if b > 0 else RV,
                             stroke_width=2) for a, b in zip(t[1:], rel)])
        side = VGroup(
            label(rf"the note: {100 * v['note_jun_dec']:+.0f}\% June--December 2017", font_size=19, color=OPT),
            label(rf"5 February: index {100 * v['feb5_ret']:+.1f}\%, note {100 * v['note_feb5']:+.1f}\%", font_size=19,
                  color=BAD),
            wrapped_label(r"pause and predict: a \$1bn inverse note, its index up 10\%. How much must the hedge buy?", 4.4,
                          18, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        src = real_data(r"rebuilt from Cboe settlements by the index's published roll rule; not the issuer's figures")
        g17, f5 = 100 * v["note_jun_dec"], 100 * v["note_feb5"]
        with self.voiceover(
            "Now run the year. The index, in green, sags all through 2017: the roll eats it. The inverse note, in "
            f"purple, climbs: {g17:+.0f} percent from June to December, a smooth, steady climb. "
            "<bookmark mark='a'/> Then the fifth of February. Below, the futures the note's hedger had to buy at each "
            "day's close, as a multiple of the note's value: small every day, until one bar of nearly twice the note "
            f"itself. The note lost {abs(f5):.1f} percent in a day. Pause and predict: a billion-dollar inverse note, its "
            "index up ten percent. How much must the hedge buy? Two hundred million dollars of futures, in the last "
            "minutes of trading, whatever the price."
            " Next: the day those mechanics broke."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(g2))
            self.add(ci, cn)
            self.play(tr.animate.set_value(v["i_feb5"]), run_time=7, rate_func=linear)
            self.play(LaggedStart(*[Create(b) for b in bars[:v["i_feb5"] - 1]], lag_ratio=0.005, run_time=1.5),
                      FadeIn(side[0]))
            vo.wait_until("a")
            self.play(tr.animate.set_value(len(t)), run_time=2)
            self.play(LaggedStart(*[Create(b) for b in bars[v["i_feb5"] - 1:]], lag_ratio=0.01, run_time=1.5),
                      FadeIn(side[1]))
            self.play(FadeIn(side[2]))
        ci.clear_updaters()
        cn.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
