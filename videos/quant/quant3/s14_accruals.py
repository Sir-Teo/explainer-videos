from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART, VALUE, load, real_data

IS_C, CF_C, ACC_C = VALUE, CASH, QC.LOSS


class Accruals(VoiceoverScene, ThreeDScene):
    def construct(self):
        a = load("accruals")
        self.card()
        self.define()
        self.derive(a)
        self.planes(a)
        self.real(a)

    def card(self):
        c = chapter_card(4, r"Accruals: where earnings and cash part", r"Which part of earnings lasts?", lit=(1996,),
                         part=PART)
        with self.voiceover("Chapter four. Accruals: where earnings and cash part."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def define(self):
        eq = cmath(r"\text{earnings}", r"=", r"\text{cash flow}", r"+", r"\text{accruals}", font_size=46,
                   colors={r"\text{earnings}": IS_C, r"\text{cash flow}": CF_C, r"\text{accruals}": ACC_C})
        eq.to_edge(UP, buff=0.7)
        d = definition_card(r"Accruals", r"The part of earnings not yet received or paid in cash: $NI - CFO$. From two "
                            r"balance sheets, Sloan's version: $(\Delta CA - \Delta\text{Cash}) - (\Delta CL - "
                            r"\Delta STD - \Delta TP) - \text{Dep}$: the growth in working capital, less "
                            r"depreciation.", width=7.6, color=ACC_C, font_size=22).next_to(eq, DOWN, buff=0.5)
        d.to_edge(LEFT, buff=0.5)
        judg = VGroup(
            label(r"accruals are judgments:", font_size=24, color=GREY_A),
            label(r"when a sale counts as made", font_size=22, color=GREY_A),
            label(r"how fast a machine wears out", font_size=22, color=GREY_A),
            label(r"what an unpaid bill will fetch", font_size=22, color=GREY_A),
            label(r"how big a provision should be", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(d, RIGHT, buff=0.5).align_to(d, UP)
        with self.voiceover(
            "Earnings and cash are different numbers, and the difference has a name: accruals. The toy firm's first year earned "
            "two hundred, of which a hundred arrived as cash. <bookmark mark='a'/> In a filing, accruals are net income minus "
            "operating cash flow, or, as Richard Sloan measured them in 1996, the growth in working capital less depreciation. "
            "<bookmark mark='b'/> They are where accounting needs judgment: when a sale counts as made, how fast a machine wears "
            "out, what an unpaid bill will fetch, how large a provision should be. Cash is harder to bend."
        ) as vo:
            self.play(Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(j) for j in judg], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, a):
        rows = [
            cmath(r"E_{t+1}", r"=", r"\alpha + \gamma\, E_t + \varepsilon", font_size=40, colors={r"E_{t+1}": IS_C}),
            cmath(r"E_{t+1}", r"=", r"\alpha + \gamma_1\, CFO_t + \gamma_2\, ACC_t + \varepsilon", font_size=40,
                  colors={r"E_{t+1}": IS_C}),
            cmath(r"\gamma_2", r"<", r"\gamma_1", font_size=44, colors={r"\gamma_2": ACC_C, r"\gamma_1": CF_C}),
        ]
        whys = [why(r"earnings persist: next year's (over assets) regressed on this year's"),
                why(r"split this year's earnings into cash and accruals, and let each have its own persistence"),
                why(r"a receivable either becomes cash or is written off; an error in an accrual reverses next year")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.75, edge=6.9)
        tab = VGroup(
            label(r"Sloan (1996), pooled, 1962--1991:", font_size=24, color=GREY_A),
            MathTex(rf"\gamma = {a['sloan']['all']:.3f}\qquad \gamma_1^{{\,cash}} = {a['sloan']['cfo']:.3f}\qquad "
                    rf"\gamma_2^{{\,accruals}} = {a['sloan']['acc']:.3f}", font_size=34),
            wrapped_label(r"and prices behaved as if the two were equally persistent: firms with high accruals then "
                          r"earned lower returns", 11.0, 22, QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Sloan's test is a regression. Earnings persist: this year's earnings, over assets, predict next year's with a slope "
            "below one, as profits drift back to normal. <bookmark mark='a'/> Now split this year's earnings into its cash part "
            "and its accrual part, and give each its own slope. <bookmark mark='b'/> The prediction: the accrual slope is smaller. "
            "A receivable either turns into cash or is written off, and an over-optimistic estimate this year must be reversed next "
            "year, so the accrual part of earnings carries noise that does not last. <bookmark mark='c'/> Sloan found exactly that, "
            f"on three decades of American firms: {a['sloan']['cfo']:.3f} for cash, {a['sloan']['acc']:.3f} for accruals. And the "
            "market priced both parts alike, so the firms with the most accruals went on to disappoint."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(tab[:2]))
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def planes(self, a):
        P = np.asarray(a["sim_points"])[:260]
        b0, b1, b2 = a["sim_beta"]
        ax = ThreeDAxes(x_range=[-0.05, 0.18, 0.05], y_range=[-0.05, 0.08, 0.05], z_range=[-0.08, 0.2, 0.05],
                        x_length=6.4, y_length=4.4, z_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        dots = VGroup(*[Dot3D(ax.c2p(x, y, z), radius=0.035, color=QC.SPOT, resolution=(4, 4)) for x, y, z in P])
        plane = Surface(lambda u, v: ax.c2p(u, v, b0 + b1 * u + b2 * v), u_range=[-0.05, 0.18], v_range=[-0.05, 0.08],
                        resolution=(10, 6), fill_opacity=0.45, stroke_width=0.6, stroke_color=GREY_B,
                        checkerboard_colors=[VALUE, VALUE])
        hint = VGroup(label(r"$x$: cash flow / assets", font_size=22, color=CF_C),
                      label(r"$y$: accruals / assets", font_size=22, color=ACC_C),
                      label(r"$z$: next year's earnings / assets", font_size=22, color=IS_C),
                      label(r"simulated: 2{,}000 firms, 10 years; profit persists 0.8; each accrual carries a booked "
                            r"error that reverses next year", font_size=17, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                  buff=0.1)
        hint.to_corner(UL, buff=0.35)
        res = VGroup(MathTex(rf"\gamma_1 = {b1:.2f} \pm {1.96 * a['sim_se'][1]:.2f}", font_size=32, color=CF_C),
                     MathTex(rf"\gamma_2 = {b2:.2f} \pm {1.96 * a['sim_se'][2]:.2f}", font_size=32, color=ACC_C),
                     label(rf"{a['sim_n']:,} firm-years; errors clustered by firm".replace(",", "{,}"), font_size=18,
                           color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, res)
        self.remove(hint, res)
        with self.voiceover(
            "Here is the mechanism in a simulated market whose truth we know. Each dot is a firm-year: cash flow on one axis, "
            "accruals on the other, next year's earnings as the height. Profits persist with point eight, and every accrual "
            "carries a small booked error that reverses next year. <bookmark mark='a'/> Fit Sloan's regression: a plane. "
            "<bookmark mark='b'/> Look along the accrual axis: it climbs steeply with cash flow. <bookmark mark='c'/> Look along "
            f"the cash axis: less steeply with accruals, {b2:.2f} against {b1:.2f}. Sloan's finding, produced by bookkeeping alone."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=3))
            vo.wait_until("a")
            self.play(Create(plane), FadeIn(res[2]), run_time=2)
            vo.wait_until("b")
            self.move_camera(phi=88 * DEGREES, theta=-90 * DEGREES, run_time=3, added_anims=[FadeIn(res[0])])
            vo.wait_until("c")
            self.move_camera(phi=88 * DEGREES, theta=0 * DEGREES, run_time=3, added_anims=[FadeIn(res[1])])
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, dots, plane)), FadeOut(hint),
                                                                  FadeOut(res)], run_time=1.5)
        self.clear_scene()

    def real(self, a):
        R = np.asarray(a["real_points"])
        b, se = np.asarray(a["real_beta"]), np.asarray(a["real_se"])
        gap = b[1] - b[2]
        sure = gap > 1.96 * np.hypot(se[1], se[2])
        g = axes([-0.12, 0.44], [-0.2, 0.7], x_length=5.6, y_length=4.2, xlabel=r"this year's earnings / assets",
                 ylabel=r"next year's earnings / assets", xticks=[0, 0.2, 0.4], yticks=[-0.2, 0, 0.2, 0.4, 0.6],
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        E = R[:, 1] + R[:, 2]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=QC.SPOT, fill_opacity=0.8) for x, y in zip(E, R[:, 0])
                        if -0.12 <= x <= 0.44 and -0.2 <= y <= 0.7])
        side = VGroup(
            label(rf"{a['real_firms']} large non-financial firms, {a['real_n']} firm-years, FY2009--2019 $\to$ next year",
                  font_size=20, color=GREY_A),
            MathTex(rf"\gamma_1^{{\,cash}} = {b[1]:.2f}\ (\pm {1.96 * se[1]:.2f})", font_size=32, color=CF_C),
            MathTex(rf"\gamma_2^{{\,accruals}} = {b[2]:.2f}\ (\pm {1.96 * se[2]:.2f})", font_size=32, color=ACC_C),
            wrapped_label((r"the gap has Sloan's sign and is clear of the noise" if sure and gap > 0 else
                           (r"the gap has Sloan's sign, but seven firms cannot separate it from noise"
                            if gap > 0 else r"seven firms show no gap at all: far too few to test Sloan")), 4.8, 22,
                          QC.GAIN if sure else GREY_A),
            MathTex(rf"\text{{accrual long-short, 1963--2020: }}{a['osap_mean']:.2f}\%\text{{ a month}},\ t = "
                    rf"{a['osap_t']:.1f}", font_size=26, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        src = real_data(r"SEC EDGAR company facts (10-K, as last reported); Chen--Zimmermann Accruals portfolio")
        if sure and gap > 0:
            gap_line = "The gap has Sloan's sign and is larger than the noise. "
        elif gap > 0:
            gap_line = "The gap has Sloan's sign, but the error bands are wide: seven firms cannot separate it from noise. "
        else:
            gap_line = "There is no gap here at all, and seven firms are far too few to say anything. "
        pp = desk_question(r"Pause and predict: two firms each earn 10\% of assets. One collected it in cash, one "
                           r"booked it as receivables. Whose earnings will be higher next year?", width=11.6,
                           font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now real filings. The House's fundamentals store holds the full XBRL histories of a handful of large companies; seven "
            f"of them are not banks, which gives {a['real_n']} firm-years with a following year. <bookmark mark='a'/> The same "
            f"regression: cash persists with {b[1]:.2f}, accruals with {b[2]:.2f}. {gap_line}Sloan used tens of thousands of "
            "firm-years; the full panel needs the SEC's bulk data, and the notes say how to load it. <bookmark mark='b'/> The market "
            "evidence is larger: the open-source replication of Sloan's portfolio, long low accruals and short high, earned "
            f"{a['osap_mean']:.2f} percent a month from 1963 to 2020, with a t-statistic of {a['osap_t']:.1f}. Chapter fourteen asks "
            "how much survived publication. <bookmark mark='c'/> Pause and predict: two firms each earn ten percent of assets, one "
            "in cash, one in receivables. Whose earnings will be higher next year? The cash earner's, on average."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
            vo.wait_until("c")
            self.play(FadeIn(pp, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
