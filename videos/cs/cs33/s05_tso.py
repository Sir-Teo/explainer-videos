from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, HEAD, LAM, NO, PART, T0C, T1C, YES, grid_table, load, mono, num)


def core_box(name, color, pos):
    r = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1).move_to(pos)
    return VGroup(r, label(name, font_size=20, color=color).move_to(r))


class Tso(VoiceoverScene):
    def construct(self):
        self.card()
        self.buffer()
        self.trace()
        self.table()

    def card(self):
        card = chapter_card(4, r"Peterson meets the store buffer", r"Does the hardware keep your program's order?",
                            lit=(1979, 2010), extra=((1979, r"Lamport: \ sequential consistency"),
                                                     (2010, r"Sewell et al.: \ x86-TSO")), part=PART)
        with self.voiceover("Chapter four. Peterson meets the store buffer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def buffer(self):
        d = load("litmus")
        mach = d["machine"]
        head = label(r"Every core has a store buffer \ (Part 10)", font_size=34).to_edge(UP, buff=0.3)
        c0 = core_box(r"core 0", T0C, [-3.2, 1.6, 0])
        c1 = core_box(r"core 1", T1C, [3.2, 1.6, 0])
        b0 = VGroup(*[Rectangle(width=0.7, height=0.45, stroke_color=T0C, stroke_width=1.4) for _ in range(3)]).arrange(
            RIGHT, buff=0).next_to(c0, DOWN, buff=0.35)
        b1 = VGroup(*[Rectangle(width=0.7, height=0.45, stroke_color=T1C, stroke_width=1.4) for _ in range(3)]).arrange(
            RIGHT, buff=0).next_to(c1, DOWN, buff=0.35)
        bl0 = label(r"store buffer", font_size=16, color=GREY_B).next_to(b0, LEFT, buff=0.15)
        bl1 = label(r"store buffer", font_size=16, color=GREY_B).next_to(b1, RIGHT, buff=0.15)
        memb = RoundedRectangle(width=9.0, height=0.8, corner_radius=0.1, stroke_color=GREY_B, fill_color=BG,
                                fill_opacity=1).move_to([0, -1.0, 0])
        mlab = mono("memory:  x = 0   y = 0", 20, WHITE).move_to(memb)
        e0 = mono("x=1", 16, T0C).move_to(b0[0])
        e1 = mono("y=1", 16, T1C).move_to(b1[0])
        a0 = Arrow(b0.get_bottom(), memb.get_top() + LEFT * 3.2, buff=0.08, color=T0C, stroke_width=2)
        a1 = Arrow(b1.get_bottom(), memb.get_top() + RIGHT * 3.2, buff=0.08, color=T1C, stroke_width=2)
        r0 = mono("r1 = y  -> 0", 18, NO).next_to(c0, UP, buff=0.15)
        r1 = mono("r2 = x  -> 0", 18, NO).next_to(c1, UP, buff=0.15)
        trials = num(mach["trials"])
        lines = VGroup(
            label(r"a store waits in the buffer; \ the core's next load goes straight to memory", font_size=21,
                  color=WHITE),
            label(r"\texttt{x = 1; r1 = y} \ $\|$ \ \texttt{y = 1; r2 = x}: \ both loads can read 0, \ impossible if "
                  r"steps simply interleave", font_size=21, color=NO),
            label(rf"Part 10 ran it on this machine: \ both 0 in {num(mach['plain']['r0=0, r1=0'])} of {trials} "
                  rf"runs; \ with a fence, \ {num(mach['mfence']['r0=0, r1=0'])}", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The proof assumed that each thread's writes and reads happen in program order. Real processors do not "
            "promise that. <bookmark mark='a'/> Each core puts its stores into a small store buffer, and lets them "
            "drain to memory later, so that a store never makes the core wait. <bookmark mark='b'/> The next load "
            "does not wait for the buffer: it reads memory directly. So core zero writes x, then reads y; core one "
            "writes y, then reads x. <bookmark mark='c'/> Both writes are still in the buffers, so both reads find "
            "zero. If instructions simply interleaved, one of the stores would have to come first, and at least one "
            "load would see a one. <bookmark mark='d'/> Part 10 ran exactly this test on this machine. Both loads "
            "read zero in most of a million runs, and never once with a fence between the store and the load."
        ) as vo:
            self.play(FadeIn(head), FadeIn(c0), FadeIn(c1), FadeIn(memb), FadeIn(mlab))
            vo.wait_until("a")
            self.play(FadeIn(b0), FadeIn(b1), FadeIn(bl0), FadeIn(bl1), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(e0), FadeIn(e1))
            vo.wait_until("c")
            self.play(FadeIn(r0), FadeIn(r1), FadeIn(lines[1]))
            self.play(GrowArrow(a0), GrowArrow(a1))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def trace(self):
        d = load("tso")
        row = next(r for r in d["rows"] if r["alg"] == "Peterson" and r["model"] == "tso" and r["fence"] == "False")
        head = label(r"The checker breaks Peterson under TSO", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup()
        for t in row["trace"]:
            c = T0C if t.startswith("P0") else T1C
            steps.add(mono(t, 18, c))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.07).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.2)
        notes = VGroup(
            label(r"P0's stores sit in its buffer: \\ P1 reads \texttt{flag0 = 0} from memory", font_size=21,
                  color=NO),
            label(r"P1's stores sit in its buffer too: \\ P0 had read \texttt{flag1 = 0}", font_size=21, color=NO),
            label(r"both enter: \ \textbf{10 steps}", font_size=23, color=NO),
            label(r"the fix: \ a \textbf{fence} after the two stores \\ (\texttt{mfence}: \ wait for the buffer to "
                  r"drain)", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(steps, RIGHT, buff=1.0).align_to(steps, UP)
        with self.voiceover(
            "Now give our checker the same store buffers. Under this model, called total store order, which is what "
            "x86 processors do, a store goes into a first-in, first-out buffer, and draining it is a separate step. "
            "<bookmark mark='a'/> The checker finds a schedule in ten steps. Thread zero raises its flag and sets turn, "
            "but both stores are still in its buffer. It reads flag one: zero, so it enters. <bookmark mark='b'/> "
            "Thread one does the same. Its own stores are buffered too, and it reads flag zero from memory, where it "
            "is still zero. <bookmark mark='c'/> Both are inside. The proof was right; its assumption was false. "
            "<bookmark mark='d'/> The fix is a fence after the two stores: an instruction that waits until the buffer "
            "has drained. On x86 that is m-fence, or any locked instruction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in steps[:5]], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in steps[5:]], lag_ratio=0.2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("tso")
        lt = load("litmus")
        head = label(r"Three memory models, \ checked", font_size=36).to_edge(UP, buff=0.3)
        fn = {"False": r"none", "True": r"before the loads", "both": r"also between the stores"}
        rows = []
        for r in d["rows"]:
            if r["alg"] != "Peterson":
                continue
            rows.append([r["model"].upper(), fn[r["fence"]], num(r["states"]), r"safe" if r["ok"] else r"broken"])
        tab = grid_table([r"model", r"Peterson's fences", r"states", r"mutual exclusion"], rows,
                         widths=[1.6, 4.0, 1.8, 2.8], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        for i, r in enumerate(rows):
            tab.cells[i + 1][3].set_color(YES if r[3] == "safe" else NO)
        mp = lt["models"]
        notes = VGroup(
            label(r"\textbf{SC}: \ steps interleave \\ (Lamport 1979)", font_size=19, color=WHITE),
            label(r"\textbf{TSO}: \ one FIFO buffer per core \\ (x86; \ Sewell et al. 2010)", font_size=19,
                  color=HEAD),
            label(r"\textbf{PSO}: \ stores to different \\ addresses drain in any order \\ (SPARC; \ Arm is weaker "
                  r"still)", font_size=19, color=LAM),
            label(rf"message passing, \ \texttt{{data = 42; flag = 1}}: \\ under PSO the reader can see the flag "
                  rf"\\ and stale data: \ {mp['pso']['mp']}", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        if notes.get_right()[0] > 6.9:
            notes.width = 6.9 - notes.get_left()[0]
        with self.voiceover(
            "Here is the whole picture. <bookmark mark='a'/> Under sequential consistency, Lamport's name for simple "
            "interleaving, Peterson is safe with no fences. <bookmark mark='b'/> Under total store order it breaks, "
            "and one fence before the loads repairs it. <bookmark mark='c'/> A weaker model, partial store order, "
            "lets stores to different addresses drain in either order. Now thread one's turn can reach memory before "
            "its flag, and Peterson breaks even with that fence. It needs a second fence, between the two stores. "
            "<bookmark mark='d'/> The same weakness breaks the most common pattern of all, message passing: write the "
            "data, then raise a flag. Under partial store order, a reader can see the flag and still read the old "
            "data. Arm and Power processors are weaker still, which is why every language now needs a memory model, "
            "the subject of chapter nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            groups = [tab.cells[1:4], tab.cells[4:7], tab.cells[7:10]]
            for mk, g, n_ in zip("abc", groups, notes[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*[c for r in g for c in r])), FadeIn(n_))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
