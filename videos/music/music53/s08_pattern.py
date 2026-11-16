from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Pattern(SoundScene):
    def construct(self):
        chapter(self, 7, r"A pattern language and live coding", r"Can music be typed while it plays?")
        self.rules()
        self.expand()
        self.tree()
        self.heard()
        self.live()

    # ------------------------------------------------------------------
    def rules(self):
        rows = VGroup(
            VGroup(Text("c4 e4 g4", font="DejaVu Sans Mono", font_size=24, color=TUNE), label(r"spaces split one cycle into equal steps", font_size=18, color=WHITE)),
            VGroup(Text("c4 [e4 g4]", font="DejaVu Sans Mono", font_size=24, color=TUNE), label(r"brackets split a step again", font_size=18, color=WHITE)),
            VGroup(Text("c4 ~ e4", font="DejaVu Sans Mono", font_size=24, color=TUNE), label(r"a tilde is a rest", font_size=18, color=WHITE)),
            VGroup(Text("bd*2", font="DejaVu Sans Mono", font_size=24, color=TUNE), label(r"a star repeats inside the step", font_size=18, color=WHITE)),
            VGroup(Text("<a4 c5>", font="DejaVu Sans Mono", font_size=24, color=TUNE), label(r"angle brackets take one item per cycle, \ in turn", font_size=18, color=WHITE)),
        )
        for r in rows:
            r[0].move_to([-3.2, 0, 0], aligned_edge=RIGHT)
            r[1].move_to([-2.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.45)
        for r in rows:
            r[0].set_x(-3.2 - r[0].width / 2)
            r[1].set_x(-2.6 + r[1].width / 2)
        rows.move_to(DOWN * 0.2)
        cred = label(r"after the mini-notation of Alex McLean's TidalCycles \ (2009)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"five rules", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Our pattern language has five rules, after the mini-notation of Alex McLean's TidalCycles. <bookmark mark='a'/> "
            "Spaces split one cycle into equal steps. <bookmark mark='b'/> Square brackets split a step again. "
            "<bookmark mark='c'/> A tilde is a rest. <bookmark mark='d'/> A star repeats something inside its step. "
            "<bookmark mark='e'/> And angle brackets take one item per cycle, in turn, so a pattern can change from one cycle "
            "to the next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cred), FadeIn(ghost(rows, 0.25)))
            for mark, r in zip("abcde", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def expand(self):
        d = load("pattern")
        cyc = d["cycle"]
        me = d["mel_events"]
        W_ = 11.0
        x0 = -W_ / 2
        total = 4 * cyc
        bars = VGroup()
        for a, du, s in me:
            b = Rectangle(width=W_ * du / total - 0.04, height=0.32, stroke_width=0, fill_color=TUNE, fill_opacity=0.8)
            b.move_to([x0 + W_ * a / total + b.width / 2 + 0.02, 0.6, 0])
            bars.add(VGroup(b, label(s, font_size=12, color=WHITE).move_to(b)))
        de = d["drum_events"]
        dots = VGroup()
        ycol = {"bd": (-0.6, EAR), "sn": (-1.0, BLUE), "hh": (-1.4, GREY_A), "cp": (-1.0, GOLD)}
        for a, du, s in de:
            y, col = ycol[s]
            dots.add(Dot([x0 + W_ * a / total + 0.08, y, 0], radius=0.08, color=col))
        cyl = VGroup(*[DashedLine([x0 + W_ * c / 4, 1.1, 0], [x0 + W_ * c / 4, -1.7, 0], color=GREY_D, stroke_width=1) for c in range(5)])
        src = VGroup(Text(d["mel"], font="DejaVu Sans Mono", font_size=22, color=TUNE), Text(d["drums"], font="DejaVu Sans Mono", font_size=22, color=EAR)).arrange(DOWN, buff=0.15).to_edge(UP, buff=1.0)
        lab = VGroup(label(r"kick", font_size=13, color=EAR).move_to([x0 - 0.45, -0.6, 0]), label(r"snare", font_size=13, color=BLUE).move_to([x0 - 0.45, -1.0, 0]),
                     label(r"hat", font_size=13, color=GREY_A).move_to([x0 - 0.45, -1.4, 0]))
        head = label(r"two lines, \ four cycles", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Two lines of it, expanded over four cycles of two seconds. <bookmark mark='a'/> The melody: C, E, two Gs in the "
            "time of one, and then, from the angle brackets, A in the first cycle, C in the second, B in the third, E in the "
            "fourth. <bookmark mark='b'/> The drums: a kick, a half-step rest and a kick, a snare, then a kick and a hat "
            "sharing a step. The parser turns each line into a list of timed events, which the engine of the next chapter plays."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(cyl), FadeIn(lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.05), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pattern")
        c = clip("pattern.one")
        src = VGroup(Text(d["mel"], font="DejaVu Sans Mono", font_size=28, color=TUNE), Text(d["drums"], font="DejaVu Sans Mono", font_size=28, color=EAR)).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        head = label(r"the two lines, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("And heard: four cycles of the two lines, the melody on the engine's sawtooth voice, the drums from Part 51's circuits."):
            self.play(FadeIn(head), FadeIn(src))
        with self.listen(c) as snd:
            window(snd, r"a pattern", kind="synthesized", detail=r"two lines of text", corner=DL, tag_corner=DR)
            pulse(snd, src, 0.0, c.duration, buff=0.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def live(self):
        items = [
            (r"live coding: \ the musician edits the code while it plays, \ and the screen is shown to the audience", WHITE),
            (r"SuperCollider \ (1996), \ ChucK \ (Ge Wang, \ 2003), \ TidalCycles \ (2009), \ Sonic Pi \ (Sam Aaron, \ 2012)", WHITE),
            (r"algoraves \ (from 2012): \ dance nights where the instrument is a text editor", WHITE),
            (r"the change must take effect on the next cycle, \ without a glitch: \ the engine never stops", TUNE),
            (r"which is the engine's hardest rule", GREY_A),
        ]
        rows_scene(self, r"live coding", items,
                   "Text can be performed. <bookmark mark='b'/> In live coding the musician edits the code while it plays, and the screen is shown to the audience. <bookmark mark='c'/> SuperCollider in 1996, ChucK from Ge Wang in 2003, TidalCycles in 2009 and Sonic Pi from Sam Aaron in 2012 made it possible, <bookmark mark='d'/> and since 2012 algoraves have been dance nights where the instrument is a text editor. <bookmark mark='e'/> Changes must be scheduled safely; when they take effect depends on the environment and performer: the engine never stops. <bookmark mark='f'/> That is the engine's hardest rule.", marks="bcdef")

    # ------------------------------------------------------------------
    def tree(self):
        root = VGroup(RoundedRectangle(width=2.6, height=0.6, corner_radius=0.12, stroke_color=WHITE), label(r"one cycle: \ 2 s", font_size=16, color=WHITE)).arrange(ORIGIN).move_to(UP * 1.8)
        kids_t = [r"c4", r"e4", r"[\ g4 \ g4 \ ]", r"$\langle$ a4 c5 b4 e5 $\rangle$"]
        kids = VGroup(*[VGroup(RoundedRectangle(width=2.5, height=0.6, corner_radius=0.12, stroke_color=TUNE), label(t, font_size=16, color=TUNE)).arrange(ORIGIN) for t in kids_t]).arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        e1 = [Line(root.get_bottom(), k.get_top(), color=GREY_B, stroke_width=2) for k in kids]
        dur = VGroup(*[label(r"0.5 s", font_size=14, color=GREY_A).next_to(k, DOWN, buff=0.1) for k in kids])
        g = VGroup(*[VGroup(RoundedRectangle(width=1.1, height=0.5, corner_radius=0.1, stroke_color=BLUE), label(r"g4", font_size=14, color=BLUE)).arrange(ORIGIN) for _ in range(2)]).arrange(RIGHT, buff=0.15).next_to(kids[2], DOWN, buff=0.75)
        gl = VGroup(*[label(r"0.25 s", font_size=13, color=GREY_A).next_to(x, DOWN, buff=0.08) for x in g])
        e2 = [Line(kids[2].get_bottom(), x.get_top(), color=GREY_B, stroke_width=2) for x in g]
        alt = VGroup(*[label(rf"cycle {i + 1}: \ {t}", font_size=14, color=EAR) for i, t in enumerate(("a4", "c5", "b4", "e5"))]).arrange(DOWN, buff=0.1).next_to(kids[3], DOWN, buff=0.7)
        e3 = Line(kids[3].get_bottom(), alt.get_top(), color=GREY_B, stroke_width=2)
        diagram = VGroup(root, kids, *e1, dur, g, gl, *e2, alt, e3)
        diagram.scale(min(1.0, 12.6 / diagram.width)).move_to(UP * 0.1)
        note = label(r"the parser builds this tree once; \ playing a cycle walks it, \ dividing time at every level", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"how the pattern is read", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How is a pattern read? <bookmark mark='a'/> The parser builds a tree. The cycle, two seconds, is the root; its four "
            "steps are its children, half a second each. <bookmark mark='b'/> A bracket is a subtree that divides its half "
            "second again, two Gs of a quarter second each. <bookmark mark='c'/> An angle bracket is a node that picks one child "
            "per cycle, in turn. <bookmark mark='d'/> Playing a cycle walks the tree, dividing time at every level: a recursive "
            "program of a few dozen lines, which is why such languages are easy to extend."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root))
            vo.wait_until("a")
            self.play(FadeIn(kids), *[Create(e) for e in e1], FadeIn(dur))
            vo.wait_until("b")
            self.play(FadeIn(g), *[Create(e) for e in e2], FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeIn(alt), Create(e3))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
