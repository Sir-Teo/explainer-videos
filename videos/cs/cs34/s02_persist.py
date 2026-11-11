from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (DATA, FILEC, HEAD, KERN, LAM, NO, PART, YES, blk, load, mono, num)


class Persist(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder()
        self.volatile()
        self.blocks()

    def card(self):
        card = chapter_card(1, r"Persistence", r"Where does data go when the power does?", lit=(1956,),
                            extra=((1956, r"IBM 350: \ the first disk"),), part=PART)
        with self.voiceover("Chapter one. Persistence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ladder(self):
        d = load("disk")
        head = label(r"The bottom of the hierarchy \ (Part 9)", font_size=36).to_edge(UP, buff=0.3)
        rungs = [(r"a register", 0.3e-9, GREY_B), (r"the L1 cache", 1e-9, DATA), (r"main memory", 100e-9, HEAD),
                 (r"flash: \ a random 4 KiB read", d["ssd_read_us"] * 1e-6, YES),
                 (r"disk: \ a random 4 KiB read", d["random_4k_ms"] * 1e-3, NO)]
        x0, x1 = -4.6, 4.6
        lo, hi = -10, -1

        def X(t):
            return x0 + (x1 - x0) * (math.log10(t) - lo) / (hi - lo)
        axis = Line([x0, -0.2, 0], [x1, -0.2, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup()
        for k, txt in ((-9, r"1 ns"), (-6, r"1 $\mu$s"), (-3, r"1 ms"), (-1, r"0.1 s")):
            ticks.add(VGroup(Line([X(10 ** k), -0.28, 0], [X(10 ** k), -0.12, 0], color=GREY_D),
                             label(txt, font_size=17, color=GREY_B).move_to([X(10 ** k), -0.55, 0])))
        dots = VGroup()
        for i, (nm, t, c) in enumerate(rungs):
            y = 0.35 + 0.55 * i
            dot = Dot([X(t), -0.2, 0], radius=0.09, color=c)
            stem = DashedLine([X(t), -0.2, 0], [X(t), y, 0], color=c, stroke_width=1.5)
            lab = label(nm, font_size=19, color=c).next_to([X(t), y, 0], RIGHT if i < 3 else LEFT, buff=0.1)
            dots.add(VGroup(dot, stem, lab))
        ratio = d["random_4k_ms"] * 1e-3 / 100e-9
        days = ratio / 86400
        lines = VGroup(
            label(rf"a disk read is ${num(ratio)}\times$ a memory read: \ if memory took a second, \ the disk would "
                  rf"take {days:.1f} days", font_size=21, color=NO),
            label(r"flash is a hundred times faster than the disk, \ and still a thousand times slower than memory",
                  font_size=21, color=YES),
            label(r"\textit{model} numbers: \ a 7200 rpm disk and an NVMe drive \ (chapters 2 and 3)", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 9 drew the memory hierarchy, and stopped at main memory. Below it is storage. <bookmark mark='a'/> "
            "On a scale of time, a register answers in a third of a nanosecond, the first cache in about one, main "
            "memory in about a hundred. <bookmark mark='b'/> Then a gap. A flash drive reads a random page in about "
            "eighty microseconds. <bookmark mark='c'/> A spinning disk takes about thirteen milliseconds. If a memory "
            "read took one second, a disk read would take a day and a half. <bookmark mark='d'/> Flash closed most of "
            "that gap, but storage is still a thousand times slower than memory, and everything in this part is "
            "shaped by that."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dots[i]) for i in range(3)], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(dots[3]))
            vo.wait_until("c")
            self.play(FadeIn(dots[4]), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def volatile(self):
        head = label(r"Memory forgets; \ storage remembers", font_size=36).to_edge(UP, buff=0.3)
        cols = VGroup()
        for title, color, items in (
            (r"main memory \ (DRAM)", HEAD, [r"a bit is charge on a tiny capacitor", r"it leaks: \ refreshed every "
                                             r"64 ms \ (Part 5)", r"power off: \ it fades away within minutes",
                                             r"any byte, \ in 100 ns"]),
            (r"storage", YES, [r"a bit is a magnetized patch, \ or charge \\ trapped behind an insulator",
                               r"no power needed: \ years", r"but read and written in \textbf{blocks}",
                               r"and slow, \ by the ladder before"])):
            rows = VGroup(*[label(t, font_size=21, color=WHITE) for t in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.22)
            cols.add(VGroup(label(title, font_size=26, color=color), rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3))
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(head, DOWN, buff=0.6)
        hist = VGroup(
            label(r"1956: \ IBM's 350 disk: \ 5 million characters on fifty 24-inch platters, \ 1{,}200 rpm",
                  font_size=20, color=GREY_A),
            label(r"today: \ about twenty terabytes in a box that fits in your hand; \ the same idea", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why have storage at all? <bookmark mark='a'/> Because memory forgets. A bit of main memory is a little "
            "charge on a capacitor, and it leaks away; Part 5's DRAM is refreshed every sixty-four milliseconds, and "
            "when the power goes, its contents fade within minutes. <bookmark mark='b'/> Storage keeps a bit without power: "
            "as a magnetized patch on a spinning platter, or as charge trapped behind an insulator in flash. It "
            "lasts for years. The price is that storage is read and written in whole blocks, and slowly. <bookmark "
            "mark='c'/> IBM's first disk, in 1956, held five million characters on fifty platters two feet across. "
            "A modern drive holds four million times as much in the palm of a hand, by the same principle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    def blocks(self):
        head = label(r"What the operating system sees: \ an array of blocks", font_size=34).to_edge(UP, buff=0.3)
        row = VGroup(*[blk(str(i), FILEC if i not in (3, 4) else KERN, w=0.72, h=0.72, font=17, fill=0.12)
                       for i in range(12)]).arrange(RIGHT, buff=0.06)
        dots = label(r"\ldots", font_size=30, color=GREY_B).next_to(row, RIGHT, buff=0.2)
        row = VGroup(row, dots).move_to(UP * 1.4)
        api = VGroup(mono("read(n)  -> block n", 22, DATA), mono("write(n, data)", 22, HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(row, DOWN, buff=0.5)
        facts = VGroup(
            label(r"a block: \ 512 bytes or 4 KiB on the device; \ our file system uses 1 KiB", font_size=21,
                  color=WHITE),
            label(r"\textbf{one} block write is atomic: \ all of it reaches the disk, \ or none", font_size=21,
                  color=YES),
            label(r"\textbf{two} block writes are not: \ a crash can land between them, \ and the disk may reorder "
                  r"them", font_size=21, color=NO),
            label(r"everything above \ (file systems, \ databases) \ is built from these two facts", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.18).next_to(api, DOWN, buff=0.5)
        with self.voiceover(
            "Underneath all the variety, the operating system sees one simple thing: a numbered array of blocks. "
            "<bookmark mark='a'/> It can read block n, or write block n; nothing smaller. Devices use blocks of 512 "
            "bytes or 4 kilobytes; our file system will use one kilobyte. <bookmark mark='b'/> Two facts about this "
            "interface carry the whole part. A single block write is atomic: after a crash, the block holds either "
            "the old contents or the new ones. <bookmark mark='c'/> But two block writes are not. A crash can come "
            "between them, and the disk may even have done the second one first. <bookmark mark='d'/> File systems "
            "and databases are, in the end, ways of building big atomic changes out of small ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(api), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()
