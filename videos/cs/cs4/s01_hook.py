from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, DATA, FUNC, HEAD, NO, PART, YES, bit_cells, fmt, load


class Hook(VoiceoverScene):
    def construct(self):
        self.counter()
        self.boeing()
        self.tenth()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def counter(self):
        d = load("clock")
        mx = d["int32_max"]
        head = label(r"December 2014", font_size=40, color=GREY_A).to_edge(UP, buff=0.5)
        val = ValueTracker(mx - 6)

        def odometer():
            v = int(round(val.get_value()))
            s = v if v <= mx else v - 2 ** 32
            bits = format(v & 0xFFFF_FFFF, "032b")
            cells = bit_cells(bits, cell=0.32, font_size=20,
                              colors=[NO if (i == 0 and bits[0] == "1") else (DATA if b == "1" else GREY_B)
                                      for i, b in enumerate(bits)])
            num = MathTex(fmt(s), font_size=72, color=NO if s < 0 else WHITE)
            return VGroup(num, cells).arrange(DOWN, buff=0.45).move_to(UP * 0.3)

        od = always_redraw(odometer)
        cap = label(r"views of one video, \ kept in a signed 32-bit integer", font_size=28, color=GREY_A).to_edge(
            DOWN, buff=1.3)
        lim = MathTex(r"2^{31} - 1 = " + fmt(mx), font_size=36, color=COST).next_to(cap, DOWN, buff=0.25)
        with self.voiceover(
            "In December 2014, YouTube announced that one music video had been watched more times than its view "
            "counter was ever designed to hold. <bookmark mark='a'/> The count had been kept in a signed "
            "thirty-two-bit integer, and the largest number that fits is two to the thirty-one, minus one: two "
            "billion, one hundred and forty-seven million and some. <bookmark mark='b'/> One more than that, and such "
            "a counter does not grow. It wraps around, to minus two billion. YouTube had switched to sixty-four bits "
            "just in time, which will last a while."
        ) as vo:
            self.play(FadeIn(head), FadeIn(od))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(lim))
            self.play(val.animate.set_value(mx), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(val.animate.set_value(mx + 3), run_time=1.8, rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boeing(self):
        d = load("clock")
        days = d["days_2_31_cs"]
        head = label(r"May 2015", font_size=40, color=GREY_A).to_edge(UP, buff=0.5)
        ax = NumberLine(x_range=[0, 260, 50], length=10.5, include_numbers=True, color=GREY_C,
                        font_size=22).move_to(DOWN * 0.4)
        axl = note(r"days of continuous power", font_size=22).next_to(ax, DOWN, buff=0.5)
        t = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(width=max(ax.n2p(t.get_value())[0] - ax.n2p(0)[0], 0.001), height=0.4,
                                              stroke_width=0, fill_color=HEAD if t.get_value() < days else NO,
                                              fill_opacity=0.85).move_to(ax.n2p(0), aligned_edge=LEFT).shift(UP * 0.6))
        mark = DashedLine(ax.n2p(days) + UP * 1.4, ax.n2p(days) + DOWN * 0.1, color=NO)
        mtxt = MathTex(r"\frac{2^{31}\ \text{centiseconds}}{8{,}640{,}000\ \text{per day}} = " + f"{days:.2f}"
                       + r"\ \text{days}", font_size=34, color=NO).next_to(mark, UP, buff=0.2).shift(LEFT * 2.6)
        what = label(r"a Boeing 787's generator controllers \ would all shut down at once", font_size=28,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In May 2015 the Federal Aviation Administration told airlines to switch their Boeing 787s off and on "
            "again, regularly. <bookmark mark='a'/> Each of the plane's electrical generators was run "
            "by a controller that counted time in hundredths of a second, in a signed thirty-two-bit integer. "
            "<bookmark mark='b'/> After two to the thirty-one hundredths of a second, which is two hundred and "
            "forty-eight days, that counter overflows, and the controllers, all powered up together, would all fail "
            "together, in flight."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(axl))
            vo.wait_until("a")
            self.add(bar)
            self.play(t.animate.set_value(days - 0.01), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(mtxt), t.animate.set_value(days + 0.5), run_time=1.0)
            self.play(FadeIn(what))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tenth(self):
        d = load("clock")
        prompt = VGroup(Text(">>> 0.1 + 0.2", font="DejaVu Sans Mono", font_size=40, color=CODE),
                        Text(d["point_three"], font="DejaVu Sans Mono", font_size=40, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.8)
        q = label(r"and every language with floating point agrees", font_size=28, color=GREY_A).next_to(prompt, DOWN,
                                                                                                    buff=0.8)
        with self.voiceover(
            "And on any computer you own, ask for zero point one plus zero point two. <bookmark mark='a'/> The answer "
            "is not zero point three. It is zero point three, then fifteen zeros, then a four. Python says so, "
            "JavaScript says so, and so does the chip underneath them. None of them is broken."
        ) as vo:
            self.play(FadeIn(prompt[0]))
            vo.wait_until("a")
            self.play(FadeIn(prompt[1]))
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        head = label(r"Finitely many bits", font_size=40).to_edge(UP, buff=0.4)
        # the integers on a clock
        ring = Circle(1.7, color=GREY_C, stroke_width=2).move_to(LEFT * 3.6 + DOWN * 0.3)
        n = 16
        ticks = VGroup()
        for k in range(n):
            ang = PI / 2 - 2 * PI * k / n
            p = ring.get_center() + 1.7 * np.array([np.cos(ang), np.sin(ang), 0])
            s = k if k < 8 else k - 16
            ticks.add(MathTex(str(s), font_size=24, color=NO if s < 0 else DATA).move_to(
                ring.get_center() + 2.1 * np.array([np.cos(ang), np.sin(ang), 0])))
            ticks.add(Dot(p, radius=0.04, color=GREY_B))
        cl = label(r"integers live on a clock", font_size=28, color=DATA).next_to(ring, DOWN, buff=0.75)
        # the reals on an uneven ruler
        line = NumberLine(x_range=[0, 8, 1], length=5.6, color=GREY_C, include_numbers=True, font_size=20).move_to(
            RIGHT * 3.3 + DOWN * 0.3)
        vals = [m / 4 * 2 ** e for e in range(-2, 3) for m in range(4, 8)]
        dots = VGroup(*[Line(line.n2p(v) + DOWN * 0.15, line.n2p(v) + UP * 0.15, color=FUNC, stroke_width=3)
                        for v in vals if v <= 8])
        rl = label(r"reals become a sparse, \ uneven ruler", font_size=28, color=FUNC).next_to(line, DOWN, buff=0.85)
        with self.voiceover(
            "All three stories have one cause. A machine has only finitely many bits. <bookmark mark='a'/> So its "
            "integers do not go on forever: they live on a clock, and going past the top brings you round to the "
            "bottom. <bookmark mark='b'/> And its real numbers are not a continuum. They are a sparse ruler, finely "
            "marked near zero and coarsely marked far away, and every answer is rounded to the nearest mark. "
            "<bookmark mark='c'/> This part builds the arithmetic of Pebble on top of those facts: the circuits that "
            "add, multiply and divide, as fast as gates allow, and the number formats that every calculation in the "
            "rest of the series runs on, with the ways they can bite."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ring), FadeIn(ticks), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[Create(t) for t in dots], lag_ratio=0.05), FadeIn(rl), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Arithmetic", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"binary and two's complement: \ one adder for signed and unsigned numbers",
            r"the ripple-carry adder, \ and carries as a parallel prefix: \ addition in $\log n$ time",
            r"multipliers as trees of adders; \ division, \ SRT, \ and the Pentium's bug",
            r"Pebble's ALU, \ built and verified",
            r"IEEE 754 floating point: \ the uneven ruler, \ rounding, \ and its error analysis",
            r"Wilkinson's polynomial, \ new number formats for AI, \ and how sin and exp are computed",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 4 of Computer Science, Built. Part 3 gave us gates; this part teaches them arithmetic. "
            "<bookmark mark='a'/> In this part: binary and two's complement, the trick that lets one adder serve both "
            "signed and unsigned numbers. The ripple-carry adder, and the beautiful idea that makes addition "
            "logarithmic: carries as a parallel prefix. Multipliers as trees of adders, division, and the most "
            "expensive table in the history of chips. Pebble's arithmetic logic unit, built and verified. Then "
            "floating point: the uneven ruler, rounding, and how errors grow, with a polynomial whose roots fly apart, "
            "the new formats that machine learning runs on, and how a chip computes a sine."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
