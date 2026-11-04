from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
                                  load, mono)

VICTIM = ["victim: lw   t2, 0(s1)       # array1_size",
          "        bgeu a0, t2, out     # the bounds check: x < size?",
          "        add  t3, s0, a0",
          "        lbu  t3, 0(t3)       # array1[x]",
          "        slli t3, t3, 6",
          "        add  t3, t3, s2",
          "        lbu  t3, 0(t3)       # probe[array1[x] * 64]",
          "out:    ret"]


class Spectre(VoiceoverScene):
    def construct(self):
        self.card()
        self.channel()
        self.gadget()
        self.attack()
        self.probe()
        self.mitigate()
        self.world()

    def card(self):
        card = chapter_card(9, r"Spectre", r"Can a guess that never happened leak a secret?", lit=(2014, 2018),
                            extra=((2014, r"Flush+Reload"), (2018, r"Spectre and Meltdown")), part=PART)
        with self.voiceover("Chapter nine. Spectre."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def channel(self):
        head = label(r"A cache remembers what was touched", font_size=36).to_edge(UP, buff=0.35)
        n = 16
        lines = VGroup(*[Rectangle(width=0.6, height=0.6, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n)])
        lines.arrange(RIGHT, buff=0.08).move_to(UP * 1.0)
        idx = VGroup(*[label(str(k), font_size=16, color=GREY_B).next_to(l, DOWN, buff=0.08) for k, l in
                       enumerate(lines)])
        cap = note(r"a probe array: \ 256 cache lines, \ one per possible byte \ (16 shown)", font_size=20).next_to(
            lines, UP, buff=0.2)
        hot = lines[11].copy().set_fill(YES, opacity=0.8).set_stroke(YES)
        times = VGroup()
        for k, l in enumerate(lines):
            t = 2 if k == 11 else 60
            times.add(label(str(t), font_size=18, color=YES if k == 11 else NO).next_to(idx[k], DOWN, buff=0.25))
        tl = note(r"cycles to read each line", font_size=20).next_to(times, DOWN, buff=0.15)
        facts = VGroup(
            label(r"1. \ flush every line \quad 2. \ let the victim run \quad 3. \ time a read of every line",
                  font_size=24, color=GREY_A),
            label(r"the fast one is the line the victim touched: \ Flush+Reload \ (Yarom and Falkner, 2014)",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Before the attack, the channel it uses. Part 9 will build caches properly; for now, one fact. A read "
            "that finds its data in the cache takes two cycles on our core; one that must go to memory takes sixty. "
            "<bookmark mark='a'/> Lay out a probe array: two hundred fifty-six cache lines, one for each possible "
            "value of a byte. Flush them all from the cache. <bookmark mark='b'/> Now let some other code run, and "
            "suppose it reads line eleven. <bookmark mark='c'/> Afterwards, time a read of every line. Two hundred "
            "fifty-five of them take sixty cycles. One takes two. <bookmark mark='d'/> The timing reveals which line "
            "was touched, and so which byte value the other code used, though nobody told us. This is Flush plus "
            "Reload, described by Yuval Yarom and Katrina Falkner in 2014. Timing attacks on caches go back further: "
            "in 2005 they were used to steal encryption keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.05), FadeIn(idx))
            vo.wait_until("b")
            self.play(FadeIn(hot))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in times], lag_ratio=0.05), FadeIn(tl))
            vo.wait_until("d")
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gadget(self):
        head = label(r"The victim: \ a bounds check", font_size=36).to_edge(UP, buff=0.3)
        c = VGroup(mono("if (x < array1_size)", 24), mono("    y = probe[array1[x] * 64];", 24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 2.0)
        code = VGroup(*[mono(s, 19) for s in VICTIM]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(c, DOWN,
                                                                                                    buff=0.45)
        mem = VGroup()
        cells = ["0"] * 4 + ["…"] + ["0"] * 2 + ["P", "E", "B", "B", "L", "E"]
        for k, t in enumerate(cells):
            r = Rectangle(width=0.5, height=0.5, stroke_color=INF if k < 7 else NO, stroke_width=1.5)
            mem.add(VGroup(r, Text(t, font="DejaVu Sans Mono", font_size=16, color=GREY_A if k < 7 else NO).move_to(r)))
        mem.arrange(RIGHT, buff=0.03).to_edge(DOWN, buff=0.9)
        b1 = Brace(mem[:7], DOWN, color=INF)
        l1 = label(r"array1: \ 16 bytes", font_size=20, color=INF).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(mem[7:], DOWN, color=NO)
        l2 = label(r"a secret, \ just past the end", font_size=20, color=NO).next_to(b2, DOWN, buff=0.08)
        with self.voiceover(
            "Now the victim. It is the most ordinary code in the world: a bounds check. <bookmark mark='a'/> If x is "
            "less than the size of array one, read array one at x, and use the byte to index another array. "
            "<bookmark mark='b'/> In Pebble's instructions: load the size, compare, and only if x is in bounds, load "
            "the byte and then the probe line it selects. <bookmark mark='c'/> Just past the end of array one, in "
            "the same address space, sits a secret: here, six letters. The bounds check is exactly what stops anyone "
            "calling this code from reading them. Architecturally, it is perfect: run it on the emulator with any x, "
            "and it never touches the secret."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in code], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(mem), FadeIn(b1), FadeIn(l1), FadeIn(b2), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attack(self):
        head = label(r"The attack, \ on our core", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ \textit{train}: \ call the victim six times with x in bounds", font_size=24, color=DATA),
            label(r"2. \ \textit{flush} the probe lines, \ and \texttt{array1\_size} itself", font_size=24,
                  color=INF),
            label(r"3. \ call it with x = 16, \ 17, \ \dots: \ past the end", font_size=24, color=NO),
            label(r"4. \ time the probe lines", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UL, buff=0.45).shift(DOWN * 0.5)
        # a schematic of step 3, from the core's behaviour
        x0, y0, cw = -2.2, -1.2, 0.075
        bars = VGroup()
        rows = [(r"\texttt{lw t2, size}", 0, 60, INF, r"a miss: \ 60 cycles"),
                (r"\texttt{bgeu}: \ guessed \textit{in bounds}", 60, 61, NO, r""),
                (r"\texttt{lbu}: \ array1[16] = `P'", 3, 5, CTRL, r""),
                (r"\texttt{lbu}: \ probe[`P' $\times$ 64]", 7, 67, CTRL, r"fills a cache line"),
                (r"check resolves: \ squash", 61, 62, NO, r"")]
        for k, (nm, a, b, col, side) in enumerate(rows):
            y = y0 - k * 0.48
            lab = label(nm, font_size=19, color=GREY_A).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=(b - a) * cw, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.8)
            bar.move_to([x0 + a * cw + (b - a) * cw / 2, y, 0])
            s = label(side, font_size=17, color=col).next_to(bar, UP, buff=0.04).align_to(bar, RIGHT) if side else \
                VectorizedPoint()
            bars.add(VGroup(lab, bar, s))
        bars.shift(RIGHT * 2.2)
        squash = DashedLine([x0 + 2.2 + 61 * cw, y0 + 0.4, 0], [x0 + 2.2 + 61 * cw, y0 - 2.3, 0], color=NO)
        after = label(r"the registers are restored; \ the program never read the secret. \ But the line stays cached.",
                      font_size=22, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the attack, as it runs on our out-of-order core. <bookmark mark='a'/> First, train the branch "
            "predictor: call the victim six times with x in bounds, so the bounds check learns to expect in bounds. "
            "<bookmark mark='b'/> Then flush the probe lines from the cache, and flush array one's size as well. "
            "Our core has a model instruction for that, like x86's flush instruction. <bookmark mark='c'/> Now call "
            "the victim with x equal to sixteen, past the end. The load of the size misses: sixty cycles before the "
            "comparison can run. The predictor guesses in bounds, as it was trained to. So for sixty cycles the core "
            "runs ahead, speculatively: it loads array one at sixteen, which is the secret letter P, shifts it, and "
            "loads the probe line P times sixty-four. That load misses too, and brings the line into the cache. "
            "<bookmark mark='d'/> Then the size arrives, the comparison fails, and the core squashes everything "
            "after the branch. Registers go back to how they were. As far as the program can tell, the secret was "
            "never read. But the probe line is still in the cache."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("ab", steps[:2]):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            self.play(FadeIn(bars[0]))
            self.play(FadeIn(bars[2]), FadeIn(bars[3]))
            vo.wait_until("d")
            self.play(FadeIn(bars[1]), FadeIn(bars[4]), Create(squash))
            self.play(FadeIn(after), FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def probe(self):
        d = load("spectre")
        head = label(r"Step 4: \ time all 255 lines", font_size=36).to_edge(UP, buff=0.3)
        r = d["rounds"][0]
        ax = Axes(x_range=[0, 256, 32], y_range=[0, 70, 20], x_length=11.5, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(UP * 0.2)
        ax.y_axis.add_numbers([0, 20, 40, 60], font_size=16, num_decimal_places=0)
        bars = VMobject(color=NO, stroke_width=2.5).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(r)])
        k = int(np.argmin(r)) + 1
        dip = Dot(ax.c2p(k, min(r)), radius=0.1, color=YES)
        tag = label(rf"line {k} \ = \ `{chr(k)}': \ {min(r)} cycles", font_size=24, color=YES).next_to(
            ax.c2p(k, 30), RIGHT, buff=0.2)
        xl = note(r"probe line \ (a byte value)", font_size=20).next_to(ax, DOWN, buff=0.15)
        yl = note(r"cycles to read it", font_size=20).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        out = d["leaked"]
        letters = VGroup(*[Text(ch, font="DejaVu Sans Mono", font_size=40, color=NO) for ch in out]).arrange(
            RIGHT, buff=0.25).to_edge(DOWN, buff=0.6)
        cap = label(rf"six rounds, \ {d['cycles']:,} cycles: \ the console prints", font_size=24,
                    color=GREY_A).next_to(letters, UP, buff=0.25)
        with self.voiceover(
            "Now the attacker times a read of every probe line, using the cycle counter. <bookmark mark='a'/> Here "
            "are the times our core measured in the first round. Two hundred fifty-four lines take sixty-three "
            "cycles: memory. <bookmark mark='b'/> One takes five: line eighty, which is the code of the letter P. "
            "<bookmark mark='c'/> Repeat with x equal to seventeen, eighteen, and so on, one round per byte. In a "
            "hundred nine thousand cycles, the attack prints the secret, letter by letter. A program that the bounds "
            "check should have stopped has read memory it was never allowed to read, through instructions that, "
            "architecturally, never ran."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(bars), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dip, scale=2), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(l, scale=1.4) for l in letters], lag_ratio=0.35), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mitigate(self):
        d = load("spectre")
        m = d["mitigations"]
        v = d["victim_cost"]
        head = label(r"Two fixes, \ and what they cost", font_size=36).to_edge(UP, buff=0.3)
        fence = VGroup(mono("bgeu a0, t2, out", 17), mono("lw   t3, 8(a5)    # barrier", 17,
                                                          color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        mask = VGroup(mono("bgeu a0, t2, out", 17), mono("sltu t3, a0, t2   # 1 if in bounds", 17, color=HEAD),
                      mono("sub  t3, zero, t3  # all ones, or 0", 17, color=HEAD),
                      mono("and  a0, a0, t3    # x, or 0", 17, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        t1 = label(r"a speculation barrier \ (x86 \texttt{lfence})", font_size=22, color=DATA)
        t2 = label(r"an index mask \ (Linux \texttt{array\_index\_nospec})", font_size=22, color=YES)
        col1 = VGroup(t1, fence).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        col2 = VGroup(t2, mask).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(UP * 1.2)
        if cols.width > 13.0:
            cols.scale_to_fit_width(13.0)
        res = VGroup(
            label(rf"leaked: \ none \ (the probe shows no fast line)", font_size=22, color=GREY_A),
            label(rf"cost per call of the victim: \ {v['None']['per_call']:.1f} \ $\to$ \ "
                  rf"{v['fence']['per_call']:.1f} cycles \ (barrier), \ {v['mask']['per_call']:.1f} \ (mask)",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 1.3)
        why = label(r"the mask stops only the dangerous value; \ the barrier stops everything", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There are two classic fixes, and our core can measure both. <bookmark mark='a'/> The first is a "
            "speculation barrier after the check: an instruction that nothing younger may pass until it commits. On "
            "x86 it is l-fence; on our core, a read of the cycle counter. <bookmark mark='b'/> The second is cleverer. "
            "Compute, without any branch, a mask that is all ones if x is in bounds and zero if not, and and it into "
            "x. On a wrong path the index becomes zero, which reads nothing secret. Linux does exactly this, in a "
            "macro called array index no spec. <bookmark mark='c'/> Both stop the leak: the probe shows no fast "
            "line. <bookmark mark='d'/> But look at the price. Called in a loop, the victim costs four cycles a call. "
            "With the barrier, twelve: the barrier stops all overlap, not only the dangerous kind. With the mask, "
            "five. <bookmark mark='e'/> The mask blocks only the value that could leak, so it is what kernels use "
            "where they can, and it must be written by hand, at every bounds check that matters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(col1))
            vo.wait_until("b")
            self.play(FadeIn(col2))
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            vo.wait_until("d")
            self.play(FadeIn(res[1]))
            vo.wait_until("e")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def world(self):
        head = label(r"January 2018", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"Spectre \ (Kocher et al.; \ Horn, \ Google Project Zero): \ this attack, \ and one through "
                  r"indirect branches", font_size=22, color=NO),
            label(r"Meltdown \ (Lipp et al.): \ on many Intel cores, \ a load from kernel memory passed its value on "
                  r"\\ before the permission check took effect", font_size=22, color=NO),
            label(r"the fixes: \ separate kernel page tables, \ retpolines, \ coarser timers and site isolation in "
                  r"browsers, \ new hardware", font_size=22, color=YES),
            label(r"out-of-order cores from Intel, \ AMD, \ Arm and IBM \ were all affected by Spectre", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "This is the attack published in January 2018 as Spectre, found independently by Paul Kocher and "
            "colleagues and by Jann Horn of Google's Project Zero, together with a second variant that mistrains "
            "indirect branches instead. <bookmark mark='a'/> Published with it was Meltdown, by Moritz Lipp and "
            "others: on many Intel cores a load from kernel memory, which should have faulted, passed its value to "
            "the instructions after it before the fault took effect, so any program could read the kernel. "
            "<bookmark mark='b'/> The fixes came at every level. Operating systems gave the kernel its own page "
            "tables. Compilers learned new ways to make indirect calls. Browsers made their timers coarser and put "
            "each site in its own process. Chips were redesigned. <bookmark mark='c'/> Meltdown was a bug in some "
            "designs. Spectre is not a bug at all: it is what speculation does, and out-of-order cores from Intel, "
            "AMD, Arm and IBM were all affected. Part 55 returns to it. The Frontier chapter asks whether speculation can be "
            "made safe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items[0]))
            for mk, it in zip("abc", items[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
