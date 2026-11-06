from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, KERN, NO, PART, YES, blk, code, grid_table, load, mono, num)


class PebbleDisk(VoiceoverScene):
    def construct(self):
        self.card()
        self.device()
        self.novels()
        self.kv()
        self.ledger()

    def card(self):
        card = chapter_card(15, r"PebbleOS gets a disk", r"Can our machine read the novels from its own file system?",
                            part=PART)
        with self.voiceover("Chapter fifteen. PebbleOS gets a disk."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def device(self):
        d = load("fs")
        head = label(r"A disk on the I/O page, \ and a file system in the kernel", font_size=34).to_edge(UP, buff=0.3)
        regs = VGroup(*[blk(t, KERN, w=2.3, h=0.5, font=16, fill=0.2) for t in (
            r"block number", r"memory address", r"command: \ 1 = read")]).arrange(DOWN, buff=0.08)
        rl = label(r"three device registers \ (kernel only)", font_size=18, color=KERN).next_to(regs, UP, buff=0.12)
        dev = VGroup(rl, regs).move_to([-4.6, 1.2, 0])
        src = code([
            "bmap:   li   t1, 10           # block a0 of the file at s1",
            "        bge  a0, t1, bm1",
            "        slli t2, a0, 2          # direct: word 3 + a0",
            "        add  t2, s1, t2",
            "        lw   a3, 12(t2)",
            "        j    bmret",
            "bm1:    addi a0, a0, -10",
            "        lw   a3, 52(s1)         # single indirect",
            "        la   a4, indbuf",
            "        la   a5, indtag",
            "        call bread              # unless already buffered",
        ], size=15).move_to([1.9, 0.9, 0])
        parts = VGroup(
            label(rf"{d['kernel_fs_instructions']} instructions: \ read the superblock at boot; \ \texttt{{bread}} with "
                  r"a four-block buffer cache; \ \texttt{iget}; \ \texttt{bmap}", font_size=19, color=WHITE),
            label(r"\texttt{open(path)}: \ walk the path from the root, \ comparing 32-byte entries; \ "
                  r"\texttt{read} on descriptor 3, \ or on 0 when a shell redirects it", font_size=19, color=HEAD),
            label(rf"\texttt{{cat /novels/emma}}: \ {num(d['emma_bytes'])} bytes, \ byte for byte; \ "
                  rf"{d['reads']} block reads, \ in the order the Python model predicts", font_size=19, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now our own machine. PebbleOS gets a disk. <bookmark mark='a'/> The device is three registers on the I/O "
            "page that only the kernel can reach: a block number, a memory address, and a command. Store a one in "
            "the command, and the block is copied straight into memory: direct memory access. <bookmark mark='b'/> "
            "The kernel gains a file system that reads PebbleFS, two hundred and sixty instructions of Pebble "
            "assembly: read the superblock at boot, a buffer cache of four blocks, find an inode, and bmap, which "
            "follows the direct, indirect and double-indirect pointers. <bookmark mark='c'/> There is a new system "
            "call, open, that walks a path from the root, and read now works on an open file, or on standard input "
            "when a shell has redirected it from a file. <bookmark mark='d'/> Run cat on slash novels slash emma, and "
            "two hundred thousand bytes come out exactly, from 201 block reads, in the order the Python file system "
            "says they should come."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dev))
            vo.wait_until("b")
            self.play(FadeIn(src), FadeIn(parts[0]))
            vo.wait_until("c")
            self.play(FadeIn(parts[1]))
            vo.wait_until("d")
            self.play(FadeIn(parts[2]))
        self.wait(0.3)
        self.clear_scene()

    def novels(self):
        p = load("pebble")
        lay = p["layouts"]
        head = label(r"Thirty novels on PebbleFS", font_size=36).to_edge(UP, buff=0.3)
        names = VGroup(*[label(rf"\texttt{{{s['name']}}}", font_size=14, color=FILEC)
                         for s in lay["next"]["sizes"]])
        names.arrange_in_grid(rows=10, cols=3, buff=(0.25, 0.08), col_alignments="lll")
        if names.width > 5.6:
            names.width = 5.6
        names.move_to([-3.6, 0.2, 0])
        nl = label(r"\texttt{ls /novels}", font_size=18, color=GREY_B).next_to(names, UP, buff=0.15).align_to(names,
                                                                                                         LEFT)
        nx, rd = lay["next"], lay["random"]
        rows = [[r"laid out by our allocator", rf"{nx['hdd_s']:.2f} s", rf"{nx['ssd_s'] * 1000:.0f} ms"],
                [r"on an aged disk", rf"{rd['hdd_s']:.0f} s", rf"{rd['ssd_s']:.1f} s"]]
        tab = grid_table([r"", r"the model disk", r"the model flash"], rows, widths=[3.0, 1.9, 1.9], row_h=0.5,
                         font_size=19, mono_cols=())
        tab.move_to([3.55, 0.9, 0])
        tab.cells[1][1].set_color(YES)
        tab.cells[2][1].set_color(NO)
        info = VGroup(
            label(rf"{num(nx['bytes'])} bytes in {num(nx['reads'])} block reads; \ fsck: \ clean", font_size=19,
                  color=WHITE),
            label(rf"in order, \ only {nx['hdd_jumps']} jumps: \ the lookups and the indirect blocks", font_size=19,
                  color=YES),
            label(r"scattered, \ every block a seek", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.4).align_to(tab, LEFT)
        with self.voiceover(
            "Now the Job's own data. <bookmark mark='a'/> The thirty novels are written to a PebbleFS disk, one file "
            "each, twenty-five million bytes, and fsck finds nothing wrong. <bookmark mark='b'/> Reading all of them "
            "takes 24,640 block reads. Laid out as our allocator lays them, the model disk moves its arm only 76 "
            "times, for the lookups and indirect blocks, and the whole corpus streams off in half a second. <bookmark "
            "mark='c'/> On an aged disk, with every block somewhere else, it would take a hundred seconds. On flash, "
            "seventeen milliseconds, or two seconds if scattered."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nl), LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.03), FadeIn(info[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.rule),
                      *[FadeIn(m) for m in tab.cells[1]], FadeIn(info[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in tab.cells[2]], FadeIn(info[2]))
        self.wait(0.3)
        self.clear_scene()

    def kv(self):
        k = load("kv")
        head = label(r"A key-value store on top", font_size=36).to_edge(UP, buff=0.3)
        files = VGroup(*[VGroup(mono(f["name"], 18, FILEC), label(rf"{num(f['entries'])} entries, \ {num(f['bytes'])} bytes",
                                                         font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.4)
                         for f in k["files"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        files.next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)
        rows = [[t["word"], num(t["count"]), num(t["read"])] for t in k["top"]]
        tab = grid_table([r"word", r"counted", r"read back"], rows, widths=[1.8, 1.8, 1.8], row_h=0.42, font_size=19,
                         mono_cols=(0,))
        tab.next_to(files, RIGHT, buff=1.2).align_to(files, UP)
        lines = VGroup(
            label(rf"\textit{{{k['book']}}}: \ {num(k['words'])} words, \ {num(k['distinct'])} distinct, \ counted "
                  rf"into chapter 14's LSM tree", font_size=20, color=WHITE),
            label(r"each run of the tree is a file: \ sorted 8-byte entries, \ written once, \ never changed",
                  font_size=20, color=FILEC),
            label(r"lookups read the files back, \ newest first: \ every count correct; \ fsck: \ clean", font_size=20,
                  color=YES),
            label(r"a database is a layer like this one: \ Part 35", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And one layer more. <bookmark mark='a'/> We count the words of Pride and Prejudice into chapter 14's LSM "
            "tree. <bookmark mark='b'/> Each of its runs becomes a file on PebbleFS: sorted eight-byte entries, written "
            "once and never changed, which is exactly the kind of file a file system handles best. <bookmark "
            "mark='c'/> Looking words up reads those files back, newest first, and every count comes back right. "
            "<bookmark mark='d'/> That is what a storage engine is: a structure built from files, as files are built "
            "from blocks. Part 35 builds a database on that idea."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(files), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        p = load("pebble")
        led = p["ledger"]
        row = led[-1]
        head = label(r"Ledger row 12", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.31,
                           label_width=4.8).scale(0.92).move_to(UP * 0.95)
        notes = VGroup(
            label(rf"tok reads the novels from PebbleFS, \ piped to the job: \ {row['instructions'] / 1e9:.2f} billion "
                  rf"instructions, \ priced as row 11: \ {row['cpu_seconds']:.2f} s", font_size=19, color=WHITE),
            label(rf"the kernel's share: \ {p['per_byte']['kernel']:.1f} instructions a byte, \ against "
                  rf"{p['row11_kernel_per_byte']:.1f} from the tape: \ the copy loop is the same size", font_size=19,
                  color=GREY_A),
            label(rf"plus the disk: \ {row['disk_seconds']:.2f} s \ = \ {row['seconds']:.2f} s \ (flash: \ "
                  rf"{row['ssd_seconds'] * 1000:.0f} ms; \ an aged disk: \ {row['aged_disk_seconds']:.0f} s)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So the ledger gets row twelve. <bookmark mark='a'/> The tokenizer now reads the novels from the file "
            "system instead of the tape, and pipes words to the job, as in Part 31. We fit the instruction counts "
            "on thirty-two passages read through PebbleOS, check the fit on held-out ones, and project the corpus: "
            "2.65 billion instructions, priced exactly as row eleven. <bookmark mark='b'/> Reading through a real "
            "file system costs the kernel no more than the tape did, about twenty-two instructions a byte, because "
            "the work is the same byte-by-byte copy. <bookmark mark='c'/> What is new is the disk: half a second for "
            "the model disk to deliver twenty-five megabytes. Two point six six seconds in all. On flash the disk "
            "time all but vanishes; on an aged disk it would be a hundred seconds, nearly fifty times the computation. Where "
            "the blocks are matters more than the code that reads them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
