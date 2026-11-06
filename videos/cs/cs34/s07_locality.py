from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BITS, FILEC, HEAD, META, NO, PART, YES, LAM, load, ms)


class Locality(VoiceoverScene):
    def construct(self):
        self.card()
        self.ffs()
        self.measured()
        self.extents()

    def card(self):
        card = chapter_card(6, r"Locality", r"Where should the blocks of a file go?", lit=(1984,),
                            extra=((1984, r"McKusick et al.: \ FFS"),), part=PART)
        with self.voiceover("Chapter six. Locality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ffs(self):
        head = label(r"The fast file system, \ 1984", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        ring = VGroup()
        for k in range(n):
            a0 = PI / 2 - k * TAU / n
            sec = AnnularSector(inner_radius=1.0, outer_radius=2.0, angle=-TAU / n + 0.04, start_angle=a0,
                                color=[META, FILEC, BITS, YES, META, FILEC, BITS, YES][k], fill_opacity=0.22,
                                stroke_width=1.5, stroke_color=GREY_B)
            ring.add(sec)
        ring.move_to([-3.6, -0.3, 0])
        cg = label(r"cylinder groups", font_size=18, color=GREY_A).next_to(ring, DOWN, buff=0.15)
        inside = VGroup(*[label(t, font_size=17, color=c) for t, c in (
            (r"each group: \ a copy of the superblock,", GREY_A), (r"its own bitmaps,", BITS),
            (r"its own inodes,", META), (r"and its data blocks", FILEC))]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        inside.next_to(ring, UP, buff=0.3).align_to(ring, LEFT).shift(LEFT * 0.4)
        rules = VGroup(
            label(r"the old Unix file system: \ free blocks handed out in whatever order they were freed", font_size=20,
                  color=NO),
            label(r"after some use, \ a file's blocks were scattered: \ about 2\% of the disk's bandwidth", font_size=20,
                  color=NO),
            label(r"FFS: \ a file's inode in its directory's group, \ its blocks near its inode", font_size=20,
                  color=YES),
            label(r"a large file moves to a new group now and then, \ so one file cannot fill a group", font_size=20,
                  color=HEAD),
            label(r"bigger blocks \ (4 KiB, \ with fragments for small files)", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.8, -0.2, 0])
        with self.voiceover(
            "The first Unix file system put blocks wherever a free one happened to be. Free blocks were kept on a "
            "list in the order they were freed, so after a while a file's blocks lay all over the disk. <bookmark "
            "mark='a'/> Measured at Berkeley, it delivered about two percent of what the disk could do. <bookmark "
            "mark='b'/> McKusick and his colleagues' fast file system of 1984 divided the disk into cylinder groups, "
            "each a little file system of its own, with its bitmaps, its inodes and its data close together. "
            "<bookmark mark='c'/> A file's inode goes in the same group as its directory, and its blocks near its "
            "inode, so a directory listing and a file read stay in one place. <bookmark mark='d'/> A very large file "
            "is moved to a fresh group every so often, so that it cannot crowd out its neighbours. <bookmark "
            "mark='e'/> And blocks grew to four kilobytes. Together these made the file system many times faster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(ring), FadeIn(cg), FadeIn(inside))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]))
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
            vo.wait_until("e")
            self.play(FadeIn(rules[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("locality")
        head = label(r"One 4 MiB file, \ three ways", font_size=36).to_edge(UP, buff=0.3)
        names = {"contiguous": (r"written alone", YES), "interleaved": (r"beside another file", HEAD),
                 "aged": (r"on an aged disk", NO)}
        rows = VGroup()
        for k, nm in enumerate(("contiguous", "interleaved", "aged")):
            r = d[nm]
            t, c = names[nm]
            first = r["first"]
            base = min(first)
            span = max(max(first) - base, 24)
            strip = VGroup(Line(LEFT * 2.6, RIGHT * 2.6, color=GREY_D, stroke_width=1.5))
            for i, b in enumerate(first[:16]):
                x = -2.6 + 5.2 * (b - base) / span if nm == "aged" else -2.6 + 5.2 * (b - base) / 48
                strip.add(Rectangle(width=0.09, height=0.32, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to(
                    [x, 0, 0]))
            info = VGroup(label(t, font_size=20, color=c),
                          label(rf"{r['extents']:,} runs".replace(",", "{,}"), font_size=17, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)
            times = VGroup(label(rf"disk: \ {ms(r['hdd_ms'])}", font_size=20, color=WHITE),
                           label(rf"flash: \ {ms(r['ssd_ms'])}", font_size=17, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)
            row = VGroup(info, strip, times)
            info.move_to([-4.8, 0, 0], aligned_edge=LEFT)
            strip.move_to([0.4, 0, 0])
            times.move_to([4.0, 0, 0], aligned_edge=LEFT)
            row.shift(UP * (1.6 - 1.25 * k))
            rows.add(row)
        cap = label(r"the file's first 16 blocks, \ by position on the disk", font_size=17, color=GREY_B).next_to(
            rows[0][1], UP, buff=0.2)
        lim = d["seq_limit_ms"]
        lines = VGroup(
            label(rf"alone: \ close to the disk's limit of {ms(lim)}", font_size=20, color=YES),
            label(r"two files growing together take turns: \ every other block belongs to the other one", font_size=20,
                  color=HEAD),
            label(rf"scattered: \ a seek for every block, \ ${d['aged']['hdd_ms'] / d['contiguous']['hdd_ms']:.0f}"
                  r"\times$ slower; \ even flash suffers, \ one small request at a time", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "We can measure this with PebbleFS and the disk model. One four-megabyte file, laid out three ways, then "
            "read in full. <bookmark mark='a'/> Written alone, its blocks are handed out in a row, and reading it "
            "takes 41 milliseconds, close to the 28 it takes the platter to pass that much data under the head. "
            "<bookmark mark='b'/> Written while another file grows beside it, the two files take turns: every other "
            "block is the neighbour's. In the model the head just waits for the gaps to pass, so this costs less "
            "than twice as much; but each run is now one block long. <bookmark mark='c'/> On an aged disk, where "
            "free blocks are scattered, every block costs a seek. Seventeen seconds: four hundred times slower. Even "
            "flash, with no arm, is two hundred times slower, because it serves four thousand tiny requests instead "
            "of a few large ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i]), FadeIn(lines[i]))
        self.wait(0.3)
        self.clear_scene()

    def extents(self):
        head = label(r"Extents, \ and deciding late", font_size=36).to_edge(UP, buff=0.3)
        ptr = VGroup(*[Rectangle(width=0.32, height=0.42, stroke_color=FILEC, fill_color=FILEC, fill_opacity=0.3)
                       for _ in range(24)]).arrange(RIGHT, buff=0.03)
        pl = label(r"block pointers: \ one per block", font_size=19, color=FILEC).next_to(ptr, UP, buff=0.1)
        ext = VGroup(*[Rectangle(width=w, height=0.42, stroke_color=YES, fill_color=YES, fill_opacity=0.3)
                       for w in (4.0, 2.5, 1.2)]).arrange(RIGHT, buff=0.08)
        el = label(r"extents: \ (first block, \ length)", font_size=19, color=YES).next_to(ext, UP, buff=0.1)
        top = VGroup(VGroup(pl, ptr), VGroup(el, ext)).arrange(DOWN, buff=0.5).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"\textbf{extents} \ (XFS 1994, \ ext4 2008): \ one record maps a run of up to 128 MiB", font_size=21,
                  color=YES),
            label(r"\textbf{delayed allocation}: \ choose blocks only when the data is written out, \ when the size is "
                  r"known", font_size=21, color=HEAD),
            label(r"\textbf{preallocation}: \ \texttt{fallocate} reserves a contiguous run before writing",
                  font_size=21, color=LAM),
            label(r"on flash the drive remaps everything anyway; \ but big requests still win \ (chapter 3)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(top, DOWN, buff=0.5)
        with self.voiceover(
            "Modern file systems push the idea further. <bookmark mark='a'/> Instead of one pointer per block, they "
            "record extents: a first block and a length. One ext4 extent maps a run of up to 128 megabytes, so a big "
            "contiguous file is described in a few records rather than thousands of pointers. <bookmark mark='b'/> "
            "Delayed allocation decides where the blocks go only when the data is finally written out, by which time "
            "the file system knows how big the file is, and two files growing together no longer interleave. "
            "<bookmark mark='c'/> And a program that knows its size can reserve a run in advance. <bookmark "
            "mark='d'/> On flash, the drive remaps blocks under the file system anyway, but large sequential "
            "requests still beat small scattered ones. Delayed allocation has a price, though, and chapter 13 will "
            "make us pay it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top[0]))
            vo.wait_until("a")
            self.play(FadeIn(top[1]), FadeIn(lines[0]))
            for mk, i in zip("bcd", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i]))
        self.wait(0.3)
        self.clear_scene()
