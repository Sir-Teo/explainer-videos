from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BITS, FILEC, GREY_B, HEAD, JRN, KERN, META, PART, ROLEC, YES, blk, layout_bar,
                                   load, mono, num)


class SimpleFS(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.inode()
        self.lookup()

    def card(self):
        card = chapter_card(5, r"A simple file system", r"Where do the inodes and the blocks go?", lit=(1974,),
                            extra=((1974, r"the Unix file system"),), part=PART)
        with self.voiceover("Chapter five. A simple file system."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def layout(self):
        d = load("fs")
        sb = d["sb"]
        head = label(rf"PebbleFS on an 8 MiB disk: \ {num(sb['nblocks'])} blocks of 1 KiB", font_size=34).to_edge(
            UP, buff=0.3)
        parts = [(r"super", 1, GREY_B), (r"inode map", 1, BITS), (r"data map", sb["ndbmap"], BITS),
                 (r"inode table", sb["nitable"], META), (r"journal", sb["jlen"], JRN), (r"data", sb["ndata"], FILEC)]
        bar = layout_bar(parts, width=12.4, h=0.8, font=16).move_to(UP * 1.6)
        counts = VGroup(*[label(rf"{num(b)}", font_size=15, color=GREY_B).next_to(seg, DOWN, buff=0.08)
                          for seg, (_, b, _) in zip(bar, parts)])
        rows = VGroup(
            label(rf"\textbf{{superblock}} \ (block 0): \ where everything else is; \ read first, \ at mount",
                  font_size=20, color=GREY_A),
            label(rf"\textbf{{bitmaps}}: \ one bit per inode, \ one per data block: \ free or used", font_size=20,
                  color=BITS),
            label(rf"\textbf{{inode table}}: \ {num(sb['ninodes'])} inodes of 64 bytes, \ 16 to a block", font_size=20,
                  color=META),
            label(rf"\textbf{{journal}}: \ {sb['jlen']} blocks, \ for chapter 8", font_size=20, color=JRN),
            label(rf"\textbf{{data}}: \ {num(sb['ndata'])} blocks, \ {sb['ndata'] / sb['nblocks'] * 100:.0f}\% of the "
                  rf"disk", font_size=20, color=FILEC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(bar, DOWN, buff=0.7)
        foot = label(r"\texttt{explainer/cs/store/fs.py}: \ the same bytes PebbleOS's kernel will read \ "
                     r"(chapter 15)", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now we build one: PebbleFS, a small Unix file system in the style of the original, on a disk of eight "
            "thousand one-kilobyte blocks. <bookmark mark='a'/> Block zero is the superblock, which says where "
            "everything else is. <bookmark mark='b'/> Then two bitmaps, one bit per inode and one per data block, "
            "saying which are free. <bookmark mark='c'/> Then the inode table: 256 inodes of 64 bytes, sixteen to a "
            "block. <bookmark mark='d'/> A journal, which we will need in chapter 8. <bookmark mark='e'/> And the "
            "rest, almost all of the disk, for data. The bar is drawn on a square-root scale; otherwise the metadata "
            "would be invisible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(counts), FadeIn(foot))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def inode(self):
        d = load("fs")
        head = label(r"An inode, \ and the largest file", font_size=36).to_edge(UP, buff=0.3)
        fields = [("type", META), ("links", META), ("size", META)] + [(rf"d{i}", FILEC) for i in range(10)] + [
            ("ind", KERN), ("dind", KERN), ("", GREY_D)]
        cells = VGroup(*[blk(t, c, w=0.62, h=0.5, font=14, fill=0.2) for t, c in fields]).arrange(RIGHT, buff=0.03)
        cells.move_to(UP * 1.9)
        cap = label(r"64 bytes: \ sixteen 4-byte words", font_size=18, color=GREY_B).next_to(cells, UP, buff=0.12)
        datab = VGroup(*[blk("", FILEC, w=0.3, h=0.3, fill=0.4) for _ in range(10)]).arrange(RIGHT, buff=0.04)
        datab.next_to(cells[3:13], DOWN, buff=0.7)
        ind = blk(r"256 pointers", KERN, w=1.8, h=0.45, font=14).next_to(cells[13], DOWN, buff=0.7).shift(LEFT * 0.4)
        dind = blk(r"256 pointers", KERN, w=1.8, h=0.45, font=14).next_to(cells[14], DOWN, buff=1.6).shift(
            RIGHT * 1.0)
        mids = VGroup(*[blk(r"256", KERN, w=0.7, h=0.4, font=13) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        mids.next_to(dind, DOWN, buff=0.45)
        arrows = VGroup(
            *[Arrow(cells[3 + k].get_bottom(), datab[k].get_top(), buff=0.04, color=FILEC, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.15) for k in range(10)],
            Arrow(cells[13].get_bottom(), ind.get_top(), buff=0.04, color=KERN, stroke_width=1.8),
            Arrow(cells[14].get_bottom(), dind.get_top(), buff=0.04, color=KERN, stroke_width=1.8),
            *[Arrow(dind.get_bottom(), m.get_top(), buff=0.04, color=KERN, stroke_width=1.5) for m in mids])
        mx = d["maxfile"]
        sum_ = VGroup(
            label(r"10 direct blocks: \ 10 KiB", font_size=20, color=FILEC),
            label(r"single indirect: \ 256 more, \ 256 KiB", font_size=20, color=KERN),
            label(r"double indirect: \ $256^2 = 65{,}536$ more, \ 64 MiB", font_size=20, color=KERN),
            label(rf"the largest file: \ $(10 + 256 + 65{{,}}536) \times 1$ KiB $= {num(mx)}$ bytes", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.5)
        foot = label(r"small files need no indirect block at all; \ ext2 adds a triple-indirect pointer and 4 KiB "
                     r"blocks: \ terabytes", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is a PebbleFS inode: sixteen words. <bookmark mark='a'/> The type, the number of links, the size "
            "in bytes. <bookmark mark='b'/> Then ten direct pointers, each the number of one data block: enough for a "
            "file of ten kilobytes. <bookmark mark='c'/> For larger files, a single-indirect pointer names a block "
            "that holds 256 more pointers. <bookmark mark='d'/> And a double-indirect pointer names a block of 256 "
            "pointers to such blocks: sixty-five thousand more. <bookmark mark='e'/> So the largest file is just over "
            "64 megabytes. The tree is lopsided on purpose: most files are small, and they need no indirect block at "
            "all, while a big one pays one extra read per 256 blocks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(cells[:3]))
            vo.wait_until("a")
            self.play(Indicate(cells[:3], color=META))
            vo.wait_until("b")
            self.play(FadeIn(cells[3:13]), FadeIn(datab), *[GrowArrow(a) for a in arrows[:10]], FadeIn(sum_[0]))
            vo.wait_until("c")
            self.play(FadeIn(cells[13]), FadeIn(ind), GrowArrow(arrows[10]), FadeIn(sum_[1]))
            vo.wait_until("d")
            self.play(FadeIn(cells[14:]), FadeIn(dind), GrowArrow(arrows[11]), FadeIn(mids),
                      *[GrowArrow(a) for a in arrows[12:]], FadeIn(sum_[2]))
            vo.wait_until("e")
            self.play(FadeIn(sum_[3]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def lookup(self):
        d = load("fs")
        head = label(r"Opening \texttt{/novels/emma}: \ every block read", font_size=34).to_edge(UP, buff=0.3)
        reads = d["first_reads"][:8]
        why = {"superblock": r"the layout \ (at boot)", "inode table": r"inode 1, \ the root",
               "directory": r"a directory's entries", "file data": r"the file's first blocks"}
        rows = VGroup()
        seen_dir = 0
        for r in reads:
            role = r["role"]
            w = why[role]
            if role == "directory":
                w = r"the root's entries: \ \texttt{novels} is inode 2" if not seen_dir else \
                    r"\texttt{novels}'s entries: \ \texttt{emma} is inode 3"
                seen_dir += 1
            c = ROLEC.get(role, GREY_B)
            rows.add(VGroup(mono(f"block {r['block']:>4}", 18, c), label(role, font_size=19, color=c),
                            label(w, font_size=18, color=GREY_A)))
        for row in rows:
            row[1].next_to(row[0], RIGHT, buff=0.4)
            row[2].next_to(row[0], RIGHT, buff=2.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(head, DOWN, buff=0.5).set_x(0)
        note = VGroup(
            label(r"inodes 2 and 3 share inode 1's block: \ already in the kernel's buffer, \ no second read",
                  font_size=19, color=YES),
            label(rf"in all: \ {d['reads']} reads for {num(d['emma_bytes'])} bytes \ ({d['data_blocks']} data "
                  rf"blocks, \ {d['indirect_blocks']} indirect, \ and the four above)", font_size=20, color=WHITE),
            label(r"run by PebbleOS's kernel, \ in Pebble assembly, \ and checked against the Python file system",
                  font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Watch the disk while a program opens slash novels slash emma and reads it. This is PebbleOS's kernel "
            "doing it, the one chapter 15 builds, and every block is logged. <bookmark mark='a'/> At boot, the "
            "superblock. <bookmark mark='b'/> Then the root's inode, from the inode table. <bookmark mark='c'/> The "
            "root directory's block: the entry novels gives inode 2. Its inode is in the same table block, already in "
            "the kernel's buffer, so no read. <bookmark mark='d'/> Then the novels directory, where emma is inode 3. "
            "<bookmark mark='e'/> And then the file's own blocks, one after another. Two hundred kilobytes cost 201 "
            "reads: the data, one indirect block, and the four reads of the lookup."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i]))
                if i == 2:
                    self.play(FadeIn(note[0]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.3), FadeIn(note[1]))
            self.play(FadeIn(note[2]))
        self.wait(0.3)
        self.clear_scene()
