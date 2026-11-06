from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, COST, DATA, HEAD, LAM, NO, PART, YES, load, mono)


class Segments(VoiceoverScene):
    def construct(self):
        self.card()
        self.base_bounds()
        self.fragmentation()

    def card(self):
        card = chapter_card(2, r"Base and bounds, \ and segments", r"What is the simplest translation that works?",
                            lit=(1961, 1978), extra=((1961, r"B5000: \ segments"), (1978, r"8086: \ segment registers")),
                            part=PART)
        with self.voiceover("Chapter two. Base and bounds, and segments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def base_bounds(self):
        head = label(r"The simplest translation: \ add a base", font_size=34).to_edge(UP, buff=0.3)
        va = mono("virtual 0x1234", 24, DATA)
        chk = VGroup(Rectangle(width=2.7, height=0.8, stroke_color=NO, fill_color=BG, fill_opacity=1),
                     mono("< bounds ?", 22, NO))
        add = VGroup(Circle(radius=0.38, stroke_color=YES, fill_color=BG, fill_opacity=1), MathTex("+", font_size=40,
                                                                                                    color=YES))
        pa = mono("physical 0x101234", 24, YES)
        for g in (chk, add):
            g[1].move_to(g[0])
        row = VGroup(va, chk, add, pa).arrange(RIGHT, buff=0.7).move_to([0, 1.5, 0])
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=2.2)
                        for a, b in zip(row[:-1], row[1:])])
        base = mono("base 0x100000", 20, YES).next_to(add, UP, buff=0.45)
        bar = Arrow(base.get_bottom(), add.get_top(), buff=0.05, color=YES, stroke_width=2)
        fault = label(r"no: \ a fault", font_size=19, color=NO).next_to(chk, DOWN, buff=0.25)
        segs = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=0.65, corner_radius=0.1, stroke_color=c,
                                                fill_color=c, fill_opacity=0.15), label(t, font_size=20, color=c))
                        for t, c in ((r"code", DATA), (r"data", HEAD), (r"heap", LAM), (r"stack", YES))])
        for s in segs:
            s[1].move_to(s[0])
        segs.arrange(RIGHT, buff=0.3).move_to([0, -0.6, 0])
        sl = label(r"\textbf{segments}: \ one base and bounds pair each; \ the address says which", font_size=21,
                   color=WHITE).next_to(segs, DOWN, buff=0.3)
        lines = VGroup(
            label(r"two registers, \ one add, \ one compare: \ relocation and protection at once", font_size=21,
                  color=YES),
            label(r"Burroughs B5000 \ (1961) \ and the 8086 \ (1978) \ had segments; \ x86-64 has all but abandoned them",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The simplest translation adds a base. <bookmark mark='a'/> The process uses addresses from zero. The "
            "hardware first checks each one against a bound, and faults if it is too big. <bookmark mark='b'/> Then it "
            "adds the base, the physical address where the kernel put this process. <bookmark mark='c'/> Two registers, "
            "one addition and one comparison, and the process can be loaded anywhere, and cannot touch anything outside "
            "its range. Part 31 had the bounds; adding the base gives relocation too. <bookmark mark='d'/> Segments "
            "generalise it: a separate base and bound for the code, the data, the heap and the stack, so each can grow "
            "on its own, and code can be shared. <bookmark mark='e'/> The Burroughs B5000 had segments in 1961, and "
            "Intel's 8086 in 1978. Modern x86 processors have all but abandoned them, for a reason the next picture "
            "shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(va))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[0]), FadeIn(chk), FadeIn(fault))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[1]), FadeIn(add), FadeIn(base), GrowArrow(bar), GrowArrow(arrs[2]), FadeIn(pa))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s) for s in segs], lag_ratio=0.2), FadeIn(sl))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def fragmentation(self):
        d = load("segments")
        head = label(r"External fragmentation", font_size=36).to_edge(UP, buff=0.3)
        M = d["M"]
        W = 12.0
        bar = VGroup()
        palette = [DATA, HEAD, LAM, YES, COST]
        for k, (a, n) in enumerate(d["live"]):
            r = Rectangle(width=W * n / M, height=0.8, stroke_color=BG, stroke_width=0.8,
                          fill_color=palette[k % len(palette)], fill_opacity=0.75)
            r.move_to([-W / 2 + W * (a + n / 2) / M, 1.2, 0])
            bar.add(r)
        holes = VGroup()
        for a, n in d["holes"]:
            r = Rectangle(width=W * n / M, height=0.8, stroke_color=NO, stroke_width=3.5, fill_color=NO, fill_opacity=0.12)
            r.move_to([-W / 2 + W * (a + n / 2) / M, 1.2, 0])
            holes.add(r)
        outline = Rectangle(width=W, height=0.8, stroke_color=GREY_B, stroke_width=1.5).move_to([0, 1.2, 0])
        bl = label(rf"memory of {M} units after 4{{,}}000 random requests under first fit: \ segments in colour, "
                   r"\ holes outlined in red", font_size=18, color=GREY_B).next_to(outline, DOWN, buff=0.15)
        ff = d["first_fail"]
        lines = VGroup(
            label(rf"the first refusal: \ a request for {ff['want']} units, \ with {ff['free']} free, \ but in "
                  rf"{ff['holes']} holes, \ the largest {ff['largest']}", font_size=22, color=NO),
            label(rf"in all, \ {d['fails']} requests refused; \ at the end, \ {d['free']} units free and the largest "
                  rf"hole {d['largest']}", font_size=22, color=NO),
            label(r"variable-sized pieces leave variable-sized gaps: \ the problem of \texttt{malloc} \ (Part 11), "
                  r"\ in the kernel", font_size=22, color=WHITE),
            label(r"compaction can move segments together, \ but stops every process while it copies", font_size=22,
                  color=GREY_A),
            label(r"so: \ make every piece the \textbf{same} size: \ a \textbf{page}", font_size=24, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(bl, DOWN, buff=0.5)
        with self.voiceover(
            "The trouble with segments is that they come in every size. <bookmark mark='a'/> We simulated a thousand "
            "and twenty-four units of memory, with segments of random sizes arriving and leaving, each placed in the "
            "first hole big enough. Here is the memory at the end: live segments in colour, holes outlined in red. "
            "<bookmark mark='b'/> The first refusal came early: a request for ninety units, when a hundred and "
            "thirty-eight were free, but split among eight holes, the largest sixty-three. <bookmark mark='c'/> Over "
            "the whole run, two hundred and forty-seven requests were refused. <bookmark mark='d'/> This is the problem "
            "of malloc from Part 11, now inside the kernel. <bookmark mark='e'/> Memory can be compacted by moving "
            "segments together, but every process must stop while it is copied. <bookmark mark='f'/> The way out is to "
            "make every piece the same size. Then any free piece fits any request. That piece is a page."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(outline), LaggedStart(*[FadeIn(r) for r in bar], lag_ratio=0.03), FadeIn(holes),
                      FadeIn(bl), run_time=2.5)
            for mk, ln in zip("bcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

