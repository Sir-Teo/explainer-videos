from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, NO, PART, T0C, T1C, YES, load, mono, num)


class Hook(VoiceoverScene):
    def construct(self):
        self.measured()
        self.lost()
        self.plan()

    def measured(self):
        d = load("racec")
        rows = {(r["mode"], r["threads"]): r for r in d["rows"]}
        head = label(r"Four threads, \ one counter", font_size=36).to_edge(UP, buff=0.3)
        src = VGroup(mono("long count = 0;", 22, GREY_A), mono("// in each of 4 threads:", 22, GREY_B),
                     mono("for (i = 0; i < 10000000; i++)", 22, WHITE), mono("    count = count + 1;", 22, WHITE)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(head, DOWN, buff=0.45)
        p4 = rows[("plain", 4)]
        W = 9.0
        bars = VGroup()
        for t, v, c in ((r"expected", p4["expected"], GREY_B), (r"what this machine printed", p4["value"], NO)):
            r = Rectangle(width=W * v / p4["expected"], height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bars.add(VGroup(label(t, font_size=20, color=c), r, label(num(v), font_size=22, color=WHITE)))
        for b in bars:
            b[1].move_to([-4.5, 0, 0], aligned_edge=LEFT)
            b[0].next_to(b[1], UP, buff=0.08).align_to(b[1], LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.15)
        bars[0].shift(DOWN * 0.6)
        bars[1].shift(DOWN * 1.8)
        lost = 1 - p4["value"] / p4["expected"]
        lines = VGroup(
            label(rf"{lost * 100:.0f}\% of the additions vanished, \ and the number changes from run to run",
                  font_size=22, color=NO),
            label(rf"with one thread: \ {num(rows[('plain', 1)]['value'])}, \ exactly right", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Four threads on this machine share one counter, and each adds one to it ten million times. <bookmark "
            "mark='a'/> The answer should be forty million. <bookmark mark='b'/> The machine printed ten and a half "
            "million. <bookmark mark='c'/> Nearly three quarters of the additions vanished, and running it again gives "
            "a different number. <bookmark mark='d'/> With one thread, the answer is exactly right. Nothing is wrong "
            "with the processor. The program is wrong, in a way that no test of one thread can find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def lost(self):
        head = label(r"Where an addition goes", font_size=36).to_edge(UP, buff=0.3)
        steps = [("A", "load r, count", "r = 0"), ("B", "load r, count", "r = 0"), ("A", "add r, r, 1", "r = 1"),
                 ("A", "store count, r", "count = 1"), ("B", "add r, r, 1", "r = 1"),
                 ("B", "store count, r", "count = 1")]
        cells = VGroup()
        for k, (t, ins, eff) in enumerate(steps):
            c = T0C if t == "A" else T1C
            x = -2.6 if t == "A" else 2.6
            r = RoundedRectangle(width=4.2, height=0.55, corner_radius=0.08, stroke_color=c, stroke_width=1.6,
                                 fill_color=c, fill_opacity=0.15).move_to([x, 1.9 - 0.68 * k, 0])
            cells.add(VGroup(r, mono(ins, 18, WHITE).move_to(r).shift(LEFT * 0.6),
                             mono(eff, 16, c).move_to(r).shift(RIGHT * 1.35)))
        ha = label(r"thread A", font_size=24, color=T0C).move_to([-2.6, 2.65, 0])
        hb = label(r"thread B", font_size=24, color=T1C).move_to([2.6, 2.65, 0])
        tl = Arrow([-5.8, 2.3, 0], [-5.8, -1.9, 0], buff=0, color=GREY_D, stroke_width=2)
        tll = label(r"time", font_size=18, color=GREY_B).next_to(tl, LEFT, buff=0.1)
        cnt = VGroup(label(r"count:", font_size=26, color=GREY_A), MathTex("0", font_size=40, color=WHITE)).arrange(
            RIGHT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 2.2)
        lines = VGroup(
            label(r"\texttt{count = count + 1} is three instructions: \ load, \ add, \ store", font_size=22,
                  color=WHITE),
            label(r"both threads loaded 0 before either stored: \ two additions, \ one result", font_size=22,
                  color=NO),
            label(r"the scheduler, \ or two cores at once, \ may interleave them anywhere", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is where an addition goes. <bookmark mark='a'/> In the machine, count equals count plus one is three "
            "instructions: load the count into a register, add one, store it back. <bookmark mark='b'/> Thread A "
            "loads zero. Before it stores, thread B loads zero too. <bookmark mark='c'/> A adds one and stores one. "
            "<bookmark mark='d'/> B adds one to its own stale zero, and stores one again. Two additions, and the count "
            "went up by one. <bookmark mark='e'/> A timer interrupt can switch threads between any two instructions, "
            "and on a multicore machine both threads run at once, so this happens all the time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ha), FadeIn(hb), GrowArrow(tl), FadeIn(tll), FadeIn(cnt))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[0]))
            self.play(FadeIn(cells[1]))
            vo.wait_until("c")
            self.play(FadeIn(cells[2]))
            self.play(FadeIn(cells[3]), cnt[1].animate.become(MathTex("1", font_size=40, color=WHITE).move_to(cnt[1])))
            vo.wait_until("d")
            self.play(FadeIn(cells[4]))
            self.play(FadeIn(cells[5]), cnt[1].animate.become(MathTex("1", font_size=40, color=NO).move_to(cnt[1])),
                      FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Concurrency", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the race, \ found by a model checker that tries every interleaving",
            r"locks from plain reads and writes \ (Peterson, \ proved), \ and how the hardware breaks them",
            r"real locks, \ semaphores, \ monitors, \ and deadlock",
            r"memory models, \ linearizability, \ and lock-free data structures",
            r"consensus numbers: \ why compare-and-swap can build anything",
            r"PebbleOS gains threads and an atomic instruction",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 33 of Computer Science, Built: Concurrency. <bookmark mark='a'/> In this part: the race, and a model "
            "checker of our own that tries every interleaving; locks built from nothing but reads and writes, proved "
            "correct, and then broken by the hardware; real locks, semaphores, monitors and deadlock; memory models, "
            "linearizability, and data structures without locks; the hierarchy that ranks synchronization by power, "
            "and why compare-and-swap can build anything; and PebbleOS gains threads and an atomic instruction."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
