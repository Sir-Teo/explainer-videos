from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BITS, FILEC, HEAD, KERN, LAM, META, NO, PART, YES, grid_table, load, num)


def row_of(c, mode, **kw):
    for r in c["rows"]:
        if r["mode"] == mode and all(r.get(k) == v for k, v in kw.items()) and (kw or "barriers" not in r):
            return r
    raise KeyError(mode)


class Crash(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariants()
        self.checker()
        self.careful()
        self.fsck()

    def card(self):
        card = chapter_card(7, r"Crash consistency", r"What must be true after a crash at any moment?",
                            lit=(1994,), extra=((1994, r"Ganger and Patt: \ soft updates"),), part=PART)
        with self.voiceover("Chapter seven. Crash consistency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def invariants(self):
        head = label(r"What \texttt{fsck} checks", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(*[VGroup(label(a, font_size=25, color=c), label(b, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07) for a, b, c in (
            (r"every block a file uses is marked used", r"else: \ the next allocation hands it out twice", NO),
            (r"every block marked used belongs to someone", r"else: \ a \textbf{leak}, \ space lost but nothing "
                                                            r"damaged", HEAD),
            (r"no block belongs to two files", r"else: \ writing one corrupts the other", NO),
            (r"every directory entry names a live inode", r"else: \ a name that leads to garbage", NO),
            (r"an inode's link count equals its names", r"else: \ freed too early, \ or never", KERN),
            (r"a file's size is covered by its blocks", r"else: \ a hole where data should be", LAM),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        side = label(r"what fsck \textbf{cannot} see: \\ a file whose blocks hold \\ the wrong bytes", font_size=24,
                     color=NO).move_to([4.5, -1.2, 0])
        with self.voiceover(
            "What does it mean for a file system to survive a crash? Its structures must agree with each other. The "
            "Unix tool fsck, the file system check, tests exactly these. <bookmark mark='a'/> Every block in use is "
            "marked used. <bookmark mark='b'/> Every block marked used belongs to some file; if not, it has leaked, "
            "which wastes space but harms nothing. <bookmark mark='c'/> No block belongs to two files. <bookmark "
            "mark='d'/> Every directory entry names a live inode. <bookmark mark='e'/> Link counts match the names. "
            "<bookmark mark='f'/> And sizes are covered by blocks. Our fsck checks all six, and can repair them. "
            "<bookmark mark='g'/> What no checker can see is a file that is perfectly consistent but full of the wrong "
            "bytes, as in the hook."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    def checker(self):
        c = load("crash")
        head = label(r"Crash every write: \ the checker", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(*[label(t, font_size=21, color=col) for t, col in (
            (r"1. \ record every block write and every flush of an operation", WHITE),
            (r"2. \ writes before the last flush are on the disk; \ of those after it, \ \textbf{any subset} may be "
             r"\ (the disk reorders)", HEAD),
            (r"3. \ for each such disk: \ mount it \ (replaying a journal, \ if there is one), \ run fsck, \ and read "
             r"the files", WHITE),
            (r"4. \ four operations: \ append to a file, \ create and write one, \ unlink, \ rename", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.5)
        none = row_of(c, "none")
        ops = none["ops"]
        rows = [[nm, str(ops[nm]["writes"]), str(ops[nm]["states"]), str(ops[nm]["corrupt"]), str(ops[nm]["bad_data"])]
                for nm in ("append", "create", "unlink", "rename")]
        rows.append([r"all four", str(none["writes"]), str(none["states"]), str(none["corrupt"]),
                     str(none["bad_data"])])
        tab = grid_table([r"no ordering at all", r"writes", r"crash points", r"corrupt", r"wrong bytes"], rows,
                         widths=[3.2, 1.6, 2.2, 1.8, 2.2], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(steps, DOWN, buff=0.45)
        for r in range(1, 6):
            tab.cells[r][3].set_color(NO)
            tab.cells[r][4].set_color(NO)
        foot = label(r"\texttt{crash\_states} and \texttt{fsck} in \texttt{explainer/cs/store/fs.py}", font_size=17,
                     color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "To study this honestly we need every crash, not a few lucky ones. So the file system records every "
            "block write and every flush it makes. <bookmark mark='a'/> A flush is a barrier: writes before it are "
            "safely on the disk. Of the writes after the last flush, the disk may have done any subset, in any "
            "order. <bookmark mark='b'/> For every possible disk, the checker mounts it, runs fsck, and reads the "
            "files back. <bookmark mark='c'/> Four everyday operations: appending, creating, unlinking, renaming. "
            "<bookmark mark='d'/> Written with no care at all, as the hook did, they give 126 crash points. 34 leave "
            "the file system corrupt, and 22 more show the wrong bytes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def careful(self):
        c = load("crash")
        none, care = row_of(c, "none"), row_of(c, "careful")
        head = label(r"Order the writes: \ never point at something unwritten", font_size=34).to_edge(UP, buff=0.3)
        chain = VGroup(*[flow for flow in (
            VGroup(label(r"data", font_size=20, color=FILEC)), VGroup(label(r"bitmap", font_size=20, color=BITS)),
            VGroup(label(r"indirect", font_size=20, color=KERN)), VGroup(label(r"inode", font_size=20, color=META)),
            VGroup(label(r"directory", font_size=20, color=YES)))])
        boxes = VGroup()
        for t in chain:
            r = RoundedRectangle(width=1.9, height=0.6, corner_radius=0.08, stroke_color=t[0].get_color(),
                                 stroke_width=1.8)
            boxes.add(VGroup(r, t.move_to(r)))
        boxes.arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.6)
        bars = VGroup(*[DashedLine(UP * 0.4, DOWN * 0.4, color=GREY_B).move_to(
            (boxes[i].get_right() + boxes[i + 1].get_left()) / 2) for i in range(4)])
        al = label(r"allocating: \ left to right, \ a flush between groups", font_size=19, color=GREY_A).next_to(
            boxes, DOWN, buff=0.15)
        fl = label(r"freeing: \ right to left \ (clear the pointer before freeing the block)", font_size=19,
                   color=GREY_A).next_to(al, DOWN, buff=0.08)
        rows = [[r"no ordering", str(none["flushes"]), str(none["states"]), str(none["corrupt"]),
                 str(none["bad_data"]), str(none["leak_only"])],
                [r"careful ordering", str(care["flushes"]), str(care["states"]), str(care["corrupt"]),
                 str(care["bad_data"]), str(care["leak_only"])]]
        tab = grid_table([r"", r"flushes", r"crash points", r"corrupt", r"wrong bytes", r"only a leak"], rows,
                         widths=[2.8, 1.5, 2.0, 1.5, 1.9, 1.9], row_h=0.45, font_size=20, mono_cols=())
        tab.next_to(fl, DOWN, buff=0.5)
        tab.cells[1][3].set_color(NO)
        tab.cells[1][4].set_color(NO)
        tab.cells[2][3].set_color(YES)
        tab.cells[2][4].set_color(YES)
        tab.cells[2][5].set_color(HEAD)
        lines = VGroup(
            label(r"a crash can now only lose space, \ never damage: \ fsck can run later, \ in the background",
                  font_size=20, color=YES),
            label(rf"the price: \ {care['flushes']} waits for the disk instead of {none['flushes']}; \ \textbf{{soft "
                  rf"updates}} \ (Ganger and Patt, 1994) \ keep the order without waiting", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first defence is order. Most of the damage comes from a pointer reaching the disk before the thing it "
            "points to. <bookmark mark='a'/> So when allocating, write the data first, then the bitmap, then any "
            "indirect block, then the inode, then the directory entry, and flush between them. <bookmark mark='b'/> "
            "When freeing, go the other way: clear the pointer before freeing what it pointed to. <bookmark "
            "mark='c'/> The checker confirms it. With careful ordering, no crash point is corrupt, and no file shows "
            "the wrong bytes. The worst a crash can do is leak a block or an inode, which fsck can reclaim at leisure. "
            "<bookmark mark='d'/> The price is waiting: thirteen flushes instead of five. Ganger and Patt's soft "
            "updates keep the same order without the waits, by tracking which buffered blocks depend on which, and "
            "FreeBSD has used them for decades."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.25), FadeIn(bars), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def fsck(self):
        c = load("crash")
        head = label(r"The trouble with fsck", font_size=36).to_edge(UP, buff=0.3)
        sc = c["scan"]
        W = 6.0
        mx = max(s["fsck_reads"] for s in sc)
        bars = VGroup()
        for k, s in enumerate(sc):
            w = max(0.05, W * s["fsck_reads"] / mx)
            r = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=NO, fill_opacity=0.85)
            bars.add(VGroup(label(rf"{num(s['blocks'])} blocks", font_size=19, color=GREY_A), r,
                            label(rf"{num(s['fsck_reads'])} blocks read", font_size=19, color=WHITE)))
        jr = sc[0]["journal_blocks"]
        tx = sum(1 for s in load("journal")["steps"] if s["kind"] in ("descriptor", "copy", "commit"))
        r = Rectangle(width=max(0.05, W * tx / mx), height=0.45, stroke_width=0, fill_color=YES, fill_opacity=0.85)
        bars.add(VGroup(label(r"replaying a journal", font_size=19, color=YES), r,
                        label(rf"{tx} blocks for one append; \ never more than {jr + 2}, \ whatever the disk",
                              font_size=19, color=WHITE)))
        for k, b in enumerate(bars):
            b[0].move_to([-4.4, 1.6 - 0.75 * k, 0], aligned_edge=RIGHT).shift(RIGHT * 1.0)
            b[1].next_to(b[0], RIGHT, buff=0.25)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        lines = VGroup(
            label(r"fsck reads every inode and every directory: \ its cost grows with the disk, \ not with the damage",
                  font_size=21, color=NO),
            label(r"on a multi-terabyte disk, \ hours of downtime after every crash", font_size=21, color=NO),
            label(r"and it repairs consistency, \ not correctness: \ it cannot know which bytes a file should hold",
                  font_size=21, color=HEAD),
            label(r"next: \ write down what you are about to do, \ \textit{before} doing it", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Fsck itself has two problems. <bookmark mark='a'/> It must read every inode and every directory, whatever "
            "went wrong, so its cost grows with the disk: four times the disk, about four times the reads. <bookmark "
            "mark='b'/> On a disk of many terabytes that meant hours with the machine down, after every power cut. "
            "<bookmark mark='c'/> And it restores consistency, not correctness: it can make the structures agree, but "
            "it has no idea what any file should contain. <bookmark mark='d'/> What if, instead, the file system wrote "
            "down what it was about to do before doing it? Then recovery would only have to read that note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:3]], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[3]), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
