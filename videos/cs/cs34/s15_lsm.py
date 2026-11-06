from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, JRN, LAM, NO, PART, YES, blk, grid_table, load)


def levels_fig(shape, unit=0.055, h=0.42, gap=0.12, color=FILEC, width=5.5):
    """Each level a row; each run a bar whose width is its number of entries."""
    g = VGroup()
    for li in range(4):
        runs = shape[li] if li < len(shape) else []
        row = VGroup(label(rf"L{li}", font_size=16, color=GREY_B))
        bars = VGroup(*[Rectangle(width=max(0.08, min(width, n * unit)), height=h, stroke_color=color,
                                  stroke_width=1.2, fill_color=color, fill_opacity=0.35) for n in runs])
        bars.arrange(RIGHT, buff=0.05)
        if len(runs) == 0:
            bars = VGroup(Rectangle(width=0.08, height=h, stroke_width=0, fill_opacity=0))
        bars.next_to(row[0], RIGHT, buff=0.2)
        row.add(bars)
        g.add(row)
    g.arrange(DOWN, aligned_edge=LEFT, buff=gap)
    return g


class Lsm(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.compaction()
        self.amplification()

    def card(self):
        card = chapter_card(14, r"LSM trees", r"How do you index data that arrives faster than a disk can seek?",
                            lit=(1996, 2006), extra=((1996, r"O'Neil et al.: \ the LSM tree"), (2006, r"Bigtable")),
                            part=PART)
        with self.voiceover("Chapter fourteen. LSM trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Buffer, \ sort, \ write once, \ merge later", font_size=36).to_edge(UP, buff=0.3)
        mem = blk(r"memtable: \ sorted, \ in memory", HEAD, w=4.2, h=0.7, font=19, fill=0.2).move_to([-3.2, 1.8, 0])
        wal = blk(r"log: \ every put, \ appended", JRN, w=3.4, h=0.6, font=17, fill=0.2).move_to([2.6, 1.8, 0])
        runs = VGroup(*[blk(t, FILEC, w=w, h=0.55, font=16, fill=0.3) for t, w in (
            (r"run 3 \ (newest)", 2.2), (r"run 2", 2.2), (r"run 1", 2.2))]).arrange(RIGHT, buff=0.25)
        runs.move_to([-1.4, 0.2, 0])
        blooms = VGroup(*[label(r"Bloom filter, \ index", font_size=14, color=LAM).next_to(r, DOWN, buff=0.08)
                          for r in runs])
        a1 = Arrow(mem.get_bottom(), runs[0].get_top(), buff=0.08, color=GREY_B, stroke_width=2)
        lines = VGroup(
            label(r"\textbf{put}: \ append to the log \ (for crashes), \ insert in the memtable: \ no disk seek",
                  font_size=20, color=WHITE),
            label(r"memtable full: \ write it out as one sorted, \ immutable \textbf{run} \ (an SSTable), \ "
                  r"sequentially", font_size=20, color=FILEC),
            label(r"\textbf{get}: \ the memtable, \ then each run from newest to oldest; \ a Bloom filter \ (Part 20) "
                  r"skips runs without the key", font_size=20, color=LAM),
            label(r"runs pile up, \ so they are \textbf{merged} in the background: \ \textbf{compaction}", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A B-tree updates its pages in place: each insert reads a page and writes it back, a random write. In "
            "1996 O'Neil and colleagues proposed the log-structured merge tree, which never does that. <bookmark "
            "mark='a'/> A put is appended to a log, for crash recovery, and inserted into a sorted table in memory, "
            "the memtable. No seek at all. <bookmark mark='b'/> When the memtable fills, it is written out in one "
            "sequential sweep as a sorted, immutable run, an SSTable. <bookmark mark='c'/> A lookup checks the "
            "memtable, then each run from newest to oldest. Each run carries a Bloom filter, Part 20's, so runs that "
            "cannot hold the key are skipped without reading them. <bookmark mark='d'/> Runs accumulate, so they are "
            "merged in the background. Google's Bigtable, LevelDB, RocksDB and Cassandra are all built this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mem), FadeIn(wal))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), LaggedStart(*[FadeIn(r) for r in runs], lag_ratio=0.3), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(blooms), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def compaction(self):
        d = load("lsm")
        head = label(r"Leveled against tiered compaction", font_size=36).to_edge(UP, buff=0.3)
        gl, gt = d["grow"]["leveled"]["shapes"], d["grow"]["tiered"]["shapes"]
        n = min(len(gl), len(gt), 12)
        L = levels_fig(gl[0], color=YES).move_to([-3.6, 0.3, 0])
        T = levels_fig(gt[0], color=HEAD).move_to([3.0, 0.3, 0])
        tl = VGroup(label(r"\textbf{leveled}: \ one run per level, \ $T = 3$ times the one above", font_size=19,
                          color=YES), label(r"a run arriving at a level is merged into it", font_size=17,
                                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tt = VGroup(label(r"\textbf{tiered}: \ up to $T$ runs per level", font_size=19, color=HEAD),
                    label(r"when $T$ collect, \ they merge into one run below", font_size=17,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        tl.move_to([-3.4, 2.4, 0])
        tt.move_to([3.2, 2.4, 0])
        cnt = label(r"memtable flushes: \ 1", font_size=19, color=GREY_B).to_edge(DOWN, buff=1.6)
        wl, wt = d["grow"]["leveled"], d["grow"]["tiered"]
        lines = VGroup(
            label(rf"over {wl['inserted'] // 4} flushes of this tiny tree: \ leveled wrote "
                  rf"{wl['written'] / wl['inserted']:.1f} entries per put, \ tiered "
                  rf"{wt['written'] / wt['inserted']:.1f}", font_size=19, color=WHITE),
            label(r"leveled rewrites each level often: \ more writing, \ but few runs to search; \ tiered: \ the "
                  r"opposite", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "There are two classic ways to merge. Here is a tiny tree, four entries per memtable, growing one flush "
            "at a time. <bookmark mark='a'/> On the left, leveled compaction, LevelDB's and RocksDB's default. Each "
            "level holds a single run, three times larger than the level above. When a run arrives at a level it is "
            "merged straight into that level's run, which is rewritten. <bookmark mark='b'/> On the right, tiered "
            "compaction, Cassandra's default. A level collects up to three runs, and only when it has three are they "
            "merged together into one run on the next level. <bookmark mark='c'/> Watch the difference. Leveled keeps "
            "few runs, so a lookup checks few places, but rewrites the same data again and again. Tiered writes each "
            "entry once per level, but leaves many runs to search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(tt), FadeIn(L), FadeIn(T), FadeIn(cnt))
            vo.wait_until("a")
            for k in range(1, n // 2):
                self.play(Transform(L, levels_fig(gl[k], color=YES).move_to(L, aligned_edge=UL)),
                          Transform(T, levels_fig(gt[k], color=HEAD).move_to(T, aligned_edge=UL)),
                          Transform(cnt, label(rf"memtable flushes: \ {k + 1}", font_size=19, color=GREY_B).move_to(
                              cnt)), run_time=0.7)
            vo.wait_until("b")
            for k in range(n // 2, n):
                self.play(Transform(L, levels_fig(gl[k], color=YES).move_to(L, aligned_edge=UL)),
                          Transform(T, levels_fig(gt[k], color=HEAD).move_to(T, aligned_edge=UL)),
                          Transform(cnt, label(rf"memtable flushes: \ {k + 1}", font_size=19, color=GREY_B).move_to(
                              cnt)), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def amplification(self):
        d = load("lsm")
        head = label(rf"Three amplifications, \ {d['n'] // 1000}{{,}}000 puts over {d['keys'] // 1000}{{,}}000 keys",
                     font_size=32).to_edge(UP, buff=0.3)
        R = {(r["policy"], r["bloom_bits"]): r for r in d["rows"]}
        rows = []
        for pol in ("leveled", "tiered"):
            for bits in (0, 10):
                r = R[(pol, bits)]
                rows.append([pol, r"none" if not bits else rf"{bits} bits a key", rf"{r['write_amp']:.1f}",
                             rf"{r['read_hit']:.2f}", rf"{r['read_miss']:.2f}", rf"{r['space_amp']:.2f}"])
        bt = d["btree"]
        tab = grid_table([r"compaction", r"Bloom filters", r"write", r"reads, \ found", r"reads, \ absent",
                          r"space"], rows, widths=[2.0, 2.3, 1.4, 1.9, 1.9, 1.4], row_h=0.46, font_size=19,
                         mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.45)
        btl = label(rf"a B-tree, \ 100-byte records in 4 KiB pages: \ {bt[0]['write_amp']:.0f} bytes written per "
                    rf"byte updated, \ {bt[-1]['write_amp']:.0f} with half its leaves cached", font_size=20,
                    color=NO).next_to(tab, DOWN, buff=0.35)
        lines = VGroup(
            label(r"leveled: \ about five times the writing of tiered, \ a tenth of its runs, \ almost no wasted "
                  r"space", font_size=20, color=YES),
            label(r"Bloom filters make a lookup for an absent key nearly free, \ for either policy", font_size=20,
                  color=LAM),
            label(r"the \textbf{RUM conjecture} \ (Athanassoulis et al., 2016): \ read, \ update and memory overheads "
                  r"cannot all be minimal", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(btl, DOWN, buff=0.6)
        with self.voiceover(
            "Now at scale: two hundred thousand puts over a hundred thousand keys, a memtable of a thousand, size ratio "
            "ten. <bookmark mark='a'/> Three costs. Write amplification: bytes written to disk per byte put. Read "
            "amplification: runs read per lookup. Space amplification: entries stored per live key. <bookmark "
            "mark='b'/> Leveled writes each entry about twelve times; tiered about twice. But tiered leaves nineteen "
            "runs, and without filters a lookup for a missing key reads all of them. <bookmark mark='c'/> Ten bits of "
            "Bloom filter per key bring that down to almost nothing for both. <bookmark mark='d'/> And a B-tree, for "
            "comparison, writes a whole four-kilobyte page to change a hundred-byte record: forty times "
            "amplification, falling only when much of the tree fits in memory. <bookmark mark='e'/> No design wins "
            "on all three costs. Athanassoulis and colleagues called this the RUM conjecture, and tuning an LSM tree "
            "is choosing a point in that triangle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.cells[0][2]), FadeIn(tab.cells[0][3]), FadeIn(tab.cells[0][4]),
                      FadeIn(tab.cells[0][5]), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(m) for r in (1, 3) for m in tab.cells[r]], FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(m) for r in (2, 4) for m in tab.cells[r]], FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(btl))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
