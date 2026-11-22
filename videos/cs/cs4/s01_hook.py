from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, DATA, FUNC, HEAD, NO, PART, YES, bit_cells, fmt, load


class Hook(WatchScene):
    def construct(self):
        self.counter()
        self.tenth()
        self.story()
        self.title(PART)

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
        cap = label(r"illustrative signed 32-bit view counter", font_size=28, color=GREY_A).to_edge(
            DOWN, buff=1.3)
        lim = MathTex(r"2^{31} - 1 = " + fmt(mx), font_size=36, color=COST).next_to(cap, DOWN, buff=0.25)
        with self.voiceover(
            "In December 2014, YouTube announced that one music video had been watched more times than its view "
            "counter was ever designed to hold. <bookmark mark='a'/> The count had been kept in a signed "
            "thirty-two-bit integer, and the largest number that fits is two to the thirty-one, minus one: two "
            "billion, one hundred and forty-seven million and some. <bookmark mark='b'/> One more than that, and such "
            "a counter does not grow. It wraps around, to minus two billion. This animation models a signed two's-complement counter. YouTube had already "
            "upgraded to sixty-four bits before the milestone, which will last a while."
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
    def tenth(self):
        d = load("clock")
        prompt = VGroup(Text(">>> 0.1 + 0.2", font="DejaVu Sans Mono", font_size=40, color=CODE),
                        Text(d["point_three"], font="DejaVu Sans Mono", font_size=40, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.8)
        q = label(r"Python and JavaScript: binary64 arithmetic", font_size=28, color=GREY_A).next_to(prompt, DOWN,
                                                                                                    buff=0.8)
        with self.voiceover(
            "In Python or JavaScript, ask for zero point one plus zero point two. <bookmark mark='a'/> The answer "
            "is not zero point three. It is zero point three, then fifteen zeros, then a four. Python says so, "
            "JavaScript says so: these expressions use binary64 floating point. Other formats can round differently. None of them is broken."
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
            self.play(FadeIn(head), FadeIn(VGroup(ring, ticks)))
            vo.wait_until("a")
            self.play(Indicate(ring, scale_factor=1.03), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[Create(t) for t in dots], lag_ratio=0.05), FadeIn(rl), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

