from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CPUC, FLOPC, GPUC, PART, POWERC, load

TRANS_C, FREQ_C, PERF_C, CORES_C = WHITE, FLOPC, CPUC, C.PROB


class PowerWall(VoiceoverScene):
    def construct(self):
        self.card()
        self.moore()
        self.dennard()
        self.breakdown()
        self.wall()
        self.parallel()

    def card(self):
        card = chapter_card(1, r"The power wall", r"Why did clocks stop getting faster?", lit=(1965, 1974, 2005),
                            part=PART)
        with self.voiceover("Chapter one. The power wall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def moore(self):
        t = load("trends")
        tt, ty = np.asarray(t["transistors_t"]), np.asarray(t["transistors_y"]) * 1e3  # data in thousands
        g = axes([1970, 2023], [3, 11], x_length=7.6, y_length=4.6, xlabel=r"year",
                 ylabel=r"transistors on one microprocessor \ (log scale)", xticks=[1970, 1980, 1990, 2000, 2010, 2020],
                 yticks=[3, 5, 7, 9, 11], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.3, -0.3, 0])
        order = np.argsort(tt)
        dots = VGroup(*[Dot(g.ax.c2p(tt[i], math.log10(ty[i])), radius=0.045, color=TRANS_C) for i in order])
        k, b0 = np.polyfit(tt, np.log10(ty), 1)
        fit = DashedLine(g.ax.c2p(1971, k * 1971 + b0), g.ax.c2p(2022, k * 2022 + b0), color=GREY_B, dash_length=0.1)
        dbl = t["transistor_doubling"]
        fl = label(rf"fit: \ doubling every ${dbl:.1f}$ years", font_size=24, color=GREY_A)
        fl.next_to(g.ax.c2p(1988, k * 1988 + b0), UP, buff=1.1)
        hc = history_card(1965, r"Gordon Moore, \ Fairchild Semiconductor",
                          r"the number of components on a chip doubles every year; \ in 1975 he revised it to every two "
                          r"years", width=5.0, color=FLOPC).move_to([4.3, -1.3, 0])
        first, last = ty[order[0]], ty.max()
        src = cite(r"data: \ K.~Rupp, \textit{Microprocessor trend data} (CC BY 4.0)", corner=DR)
        ends = VGroup(label(rf"Intel 4004: \ ${first:,.0f}$".replace(",", "{,}"), font_size=20, color=GREY_A)
                      .next_to(dots[0], RIGHT, buff=0.5).shift(DOWN * 0.2),
                      label(rf"${last / 1e9:.0f}$ billion", font_size=20, color=GREY_A).next_to(dots[-1], RIGHT, buff=0.15))
        with self.voiceover(
            "In 1965 Gordon Moore, then at Fairchild Semiconductor, noticed that the number of components on a chip "
            "had been doubling every year, and guessed it would keep going. <bookmark mark='a'/> Here are fifty years "
            f"of microprocessors, on a log scale: from Intel's 4004 in 1971, with about {round(first, -2):,.0f} "
            f"transistors, to chips with {last / 1e9:.0f} billion. <bookmark mark='b'/> A straight line on a log "
            f"scale is exponential growth. The fit doubles every {dbl:.1f} years, the pace Moore settled on in 1975. "
            "For three decades, each doubling also made every program faster, for free."
        ) as vo:
            self.play(FadeIn(g), FadeIn(hc, shift=LEFT * 0.2), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(ends), Indicate(dots[0], scale_factor=2.0), Indicate(dots[-1], scale_factor=2.0))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shrink_picture(self, k: int, side=2.6, center=(-4.4, 0.4, 0)) -> VGroup:
        n = 2 * k
        cells = VGroup(*[Square(side / n * 0.72, stroke_width=1.2, stroke_color=FLOPC, fill_color=FLOPC,
                                fill_opacity=0.3) for _ in range(n * n)])
        cells.arrange_in_grid(rows=n, cols=n, buff=side / n * 0.28)
        frame = Square(side + 0.15, stroke_color=GREY_C, stroke_width=1.5)
        return VGroup(frame, cells.move_to(frame)).move_to(center)

    def dennard(self):
        colors = {r"\kappa": FLOPC, r"P": POWERC}
        rows = [
            cmath(r"L,\ V", r"\;\to\;", r"L/\kappa,\ V/\kappa", colors=colors, font_size=34),
            cmath(r"C", r"\;\to\;", r"C/\kappa", colors=colors, font_size=34),
            cmath(r"f", r"\;\to\;", r"\kappa f", colors=colors, font_size=34),
            cmath(r"P = C V^2 f", r"\;\to\;", r"\tfrac{C}{\kappa}\,\tfrac{V^2}{\kappa^2}\,\kappa f = P/\kappa^2",
                  colors=colors, font_size=34),
            cmath(r"\tfrac{P}{\text{area}}", r"\;\to\;", r"\kappa^2 \cdot P/\kappa^2 = \text{constant}", colors=colors,
                  font_size=34),
        ]
        whys = [why(r"shrink every length and the voltage"), why(r"capacitance $\propto$ area / thickness"),
                why(r"less charge to move, \ shorter wires"), why(r"switching power"),
                why(r"$\kappa^2$ more transistors per area")]
        step = ladder(self, rows, whys, keep=5, top=2.7, x=1.0, buff=0.42, edge=6.8)
        pic1 = self.shrink_picture(2)
        pic2 = self.shrink_picture(4)
        tag = schematic_tag(corner=DL)
        hc = history_card(1974, r"Robert Dennard and colleagues, \ IBM",
                          r"scale a transistor down by $\kappa$ and it gets faster \ while the power per area stays the "
                          r"same", width=6.4, color=FLOPC).to_edge(DOWN, buff=0.25).shift(RIGHT * 2.6)
        with self.voiceover(
            "Why did shrinking make computers faster? The answer came in 1974 from Robert Dennard and his colleagues at "
            "IBM, the engineer who had invented the one-transistor memory cell. <bookmark mark='a'/> Shrink every "
            "length of a transistor by a factor kappa, and lower the voltage by the same factor. <bookmark mark='b'/> "
            "The capacitance it has to charge falls by kappa, <bookmark mark='c'/> and it switches kappa times "
            "faster. <bookmark mark='d'/> The power to switch it is C V squared f, which falls by kappa squared. "
            "<bookmark mark='e'/> But kappa squared more transistors now fit in the same area. So the power per "
            "square millimetre stays the same, while the clock gets faster and the count goes up. That's Dennard "
            "scaling, and for thirty years it was the free lunch."
        ) as vo:
            self.play(FadeIn(pic1), FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            self.play(ReplacementTransform(pic1, pic2), run_time=1.2)
            for i, mk in enumerate("bcde", 1):
                vo.wait_until(mk)
                if i == 1:
                    self.play(FadeOut(hc))
                step(i)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def breakdown(self):
        colors = {r"\kappa": FLOPC, r"P": POWERC, r"V": C.SURPRISE}
        rows = VGroup(
            cmath(r"V", r"\;\to\;", r"V", colors=colors, font_size=36),
            cmath(r"P", r"\;\to\;", r"\tfrac{C}{\kappa}\,V^2\,\kappa f = P", colors=colors, font_size=36),
            cmath(r"\tfrac{P}{\text{area}}", r"\;\to\;", r"\kappa^2 \cdot \tfrac{P}{\text{area}}", colors=colors,
                  font_size=36),
        )
        whys = VGroup(why(r"leakage: \ the off-current falls at most $10\times$ per $60$ mV", font_size=22),
                      why(r"each transistor: \ the same power as before", font_size=22),
                      why(r"$\kappa^2$ more of them: \ the chip heats up", font_size=22))
        blocks = VGroup(*[VGroup(r_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.14) for r_, w_ in zip(rows, whys)])
        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_corner(UL, buff=0.6)
        cards = VGroup(
            history_card(2004, r"Intel cancels the Pentium 4's successor", r"and turns to two cores per chip",
                         width=5.6, color=POWERC),
            history_card(2005, r"Herb Sutter, \ \textit{The free lunch is over}", r"programs will only get faster if "
                         r"they run in parallel", width=5.6, color=POWERC),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        g = axes([0, 1.0], [-12, -3], x_length=4.4, y_length=2.6, xlabel=r"gate voltage", ylabel=r"current (log)",
                 center=[3.7, 1.1, 0])
        vs = np.linspace(0, 1.0, 120)
        curves = VGroup()
        for vt, col in ((0.45, GREY_B), (0.3, C.SURPRISE)):
            ii = -4 + np.minimum(vs - vt, 0.0) / 0.06  # one decade of current per 60 mV below threshold
            curves.add(curve(g.ax, vs, ii, col, 3))
        off = VGroup(*[Dot(g.ax.c2p(0, -4 - vt / 0.06), radius=0.06, color=col)
                       for vt, col in ((0.45, GREY_B), (0.3, C.SURPRISE))])
        ol = label(r"lower threshold: \\ more current when off", font_size=18, color=C.SURPRISE)
        ol.next_to(off[1], LEFT, buff=0.25)
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "Then, in the early two thousands, the voltage stopped falling. <bookmark mark='a'/> A transistor is a "
            "switch, and below a certain voltage it can't switch off cleanly: at room temperature the current falls "
            "at most tenfold for every sixty millivolts, so a lower voltage means leakage. <bookmark mark='b'/> With "
            "the voltage stuck, each smaller transistor uses as much power as the old one, <bookmark mark='c'/> and "
            "packing kappa squared more of them into the same area multiplies the heat by kappa squared. "
            "<bookmark mark='d'/> In 2004 Intel cancelled the successor to the Pentium 4 and turned to two cores per "
            "chip. A year later the programmer Herb Sutter wrote that the free lunch was over."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(whys[0]), Create(curves[0]))
            self.play(Create(curves[1]), FadeIn(off), FadeIn(ol))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        t = load("trends")
        series = [("frequency", FREQ_C, r"clock, MHz", 1.0), ("watts", POWERC, r"typical power, W", 1.0),
                  ("specint", PERF_C, r"single-thread speed (SPECint $\times 10^3$)", 1.0),
                  ("cores", CORES_C, r"cores", 1.0)]
        g = axes([1970, 2023], [-1, 6], x_length=8.2, y_length=4.8, xlabel=r"year", ylabel=r"log scale",
                 xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6],
                 yfmt=lambda v: rf"10^{{{int(v)}}}" if v > 1 else ("1" if v == 0 else "10"), center=[-2.0, -0.2, 0])
        groups = VGroup()
        for name, col, _, _ in series:
            x, y = np.asarray(t[f"{name}_t"]), np.asarray(t[f"{name}_y"])
            keep = (y > 0) & (np.log10(y) <= 6)
            groups.add(VGroup(*[Dot(g.ax.c2p(a, math.log10(b)), radius=0.04, color=col)
                                for a, b in zip(x[keep], y[keep])]))
        lg = legend([(col, txt) for _, col, txt, _ in series], font_size=20).move_to([4.6, 1.4, 0])
        wall_x = g.ax.c2p(2005, 0)[0]
        wall = DashedLine([wall_x, g.ax.c2p(0, -1)[1], 0], [wall_x, g.ax.c2p(0, 6)[1], 0], color=C.SURPRISE,
                          dash_length=0.1)
        wl = label(r"2005", font_size=22, color=C.SURPRISE).next_to(wall, UP, buff=0.08)
        e, late = t["freq_doubling_early"], t["freq_growth_late"]
        se, sl = t["specint_doubling_early"], t["specint_doubling_late"]
        rate = (f"and since 2006 it has drifted down by about {100 * (1 - late):.0f} percent a year" if late < 1 else
                f"and since 2006 it has crept up by only {100 * (late - 1):.0f} percent a year")
        f04 = t["freq_2004"] / 1000
        facts = VGroup(label(rf"clock: \ doubling every ${e:.1f}$ years, \ 1985--2003", font_size=20, color=FREQ_C),
                       label(rf"single-thread speed: \ every ${se:.1f}$ years, \ then ${sl:.1f}$", font_size=20,
                             color=PERF_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, -1.4, 0])
        src = cite(r"data: \ K.~Rupp, \textit{Microprocessor trend data} (CC BY 4.0)", corner=DR)
        with self.voiceover(
            "You can see the wall in the data. <bookmark mark='a'/> Clock speed doubled every "
            f"{e:.1f} years from 1985 to 2003, and stopped near {f04:.1f} gigahertz; " + rate + ". "
            "<bookmark mark='b'/> Power had been climbing with it, and it levelled off at what a fan and a heat sink "
            "can carry away, around a hundred watts. <bookmark mark='c'/> Single-thread speed, what one program "
            f"gets, doubled every {se:.1f} years until then; since 2010, every {sl:.1f}. <bookmark mark='d'/> What "
            "kept growing was the number of cores. The transistors kept coming; the only way left to use them was in "
            "parallel."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(d) for d in groups[0]], lag_ratio=0.02), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(wall), FadeIn(wl), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in groups[1]], lag_ratio=0.02), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in groups[2]], lag_ratio=0.02), FadeIn(lg[2]), FadeIn(facts[1]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in groups[3]], lag_ratio=0.02), FadeIn(lg[3]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallel(self):
        colors = {r"P": POWERC, r"f": FLOPC, r"V": C.SURPRISE}
        rows = [
            cmath(r"P", r"\propto", r"C\,V^2 f", colors=colors, font_size=38),
            cmath(r"P", r"\propto", r"f^3", colors=colors, font_size=38),
        ]
        whys = [why(r"switching power"), why(r"a faster clock needs a higher voltage: \ $V \propto f$, roughly")]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-2.5, buff=0.4, edge=6.8)
        bars = LiveBars([1, 1], max_value=8, height=3.0, bar_width=1.1, gap=1.6, colors=[POWERC, POWERC],
                        show_values=True, digits=0, value_font=28,
                        labels=[r"one core, \ clock $\times 2$", r"two cores, \ same clock"], label_font=22)
        bars.place(base_y=-2.9, x=-2.5)
        bl = label(r"power for twice the work \ (one core today $= 1$)", font_size=22, color=POWERC)
        bl.move_to([-2.5, 0.85, 0])
        amdahl = theorem_card(r"Amdahl's law", r"if a fraction $p$ of the work can be split $N$ ways, \ the speed-up is "
                              r"$\dfrac{1}{(1 - p) + p/N}$", who=r"Gene Amdahl, 1967", width=5.4, font_size=22,
                              kind=r"Law").move_to([3.9, -0.6, 0])
        gpu = label(r"a GPU: \ thousands of slow, simple lanes", font_size=24, color=GPUC).next_to(amdahl, DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            "Why does parallel win? <bookmark mark='a'/> Switching power is C V squared f, and to run a clock faster "
            "you have to raise the voltage roughly in proportion. So power grows like the cube of the clock. "
            "<bookmark mark='b'/> To do twice the work, one core at twice the clock burns about eight times the "
            "power. Two cores at the same clock burn twice the power. <bookmark mark='c'/> The catch is Amdahl's law, "
            "from 1967: the part of a program that can't be split limits the speed-up, however many cores you add. "
            "<bookmark mark='d'/> So the winning chip for a problem that splits into millions of identical pieces "
            "has thousands of slow, simple lanes. That chip already existed. It drew video games."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(bl))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(*bars.to([8, 2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(amdahl, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(gpu, shift=UP * 0.1))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
