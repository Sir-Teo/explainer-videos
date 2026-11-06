from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (COST, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, num)

ALGS = ("block nested loops", "index nested loops", "sort-merge", "grace hash")
ACOL = {"block nested loops": NO, "index nested loops": KERN, "sort-merge": LAM, "grace hash": YES}


def pages(n, color, w=0.32, h=0.42, cols=10):
    g = VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color,
                           fill_opacity=0.25) for _ in range(n)])
    g.arrange_in_grid(cols=cols, buff=0.06)
    return g


class Joins(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.algorithms()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Joins, \ page by page", r"Which way of matching two tables is cheapest?",
                            lit=(1983,), extra=((1983, r"Kitsuregawa: \ the Grace hash join"),), part=PART)
        with self.voiceover("Chapter five. Joins, page by page."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"The unit of cost is the page", font_size=36).to_edge(UP, buff=0.3)
        R = pages(20, DATA).move_to([-3.4, 1.6, 0])
        S = pages(10, HEAD).move_to([-3.4, -0.05, 0])
        rl = label(r"$R$: \ $M$ = 400 pages \ (20,000 rows)", font_size=19, color=DATA).next_to(R, UP, buff=0.15)
        sl = label(r"$S$: \ $N$ = 200 pages \ (10,000 rows)", font_size=19, color=HEAD).next_to(S, UP, buff=0.15)
        mem = VGroup(*[Square(0.5, stroke_color=GREY_B, stroke_width=1.5) for _ in range(5)]).arrange(RIGHT, buff=0.1)
        mem.move_to([3.2, 1.6, 0])
        ml = label(r"memory: \ $B$ buffer pages", font_size=19, color=GREY_A).next_to(mem, UP, buff=0.15)
        lines = VGroup(
            label(r"a disk reads or writes whole pages; \ in Part 34 a random page cost milliseconds, \ the CPU's "
                  r"work on it microseconds", font_size=21, color=WHITE),
            label(r"so a join's cost is counted in \textbf{page I/Os}, \ given $M$, \ $N$ \ and $B$", font_size=21,
                  color=COST),
            label(r"block nested loops: \ fill $B - 2$ buffers with $R$, \ scan all of $S$ against them, \ repeat",
                  font_size=21, color=NO),
            label(r"cost \ $M + \lceil M / (B-2) \rceil \cdot N$: \ with $B$ = 5, \ 400 + 134 $\times$ 200 = "
                  r"27{,}200 pages", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "To compare join algorithms, count what is expensive. <bookmark mark='a'/> A disk moves whole pages, and "
            "in Part 34 a random page cost milliseconds while the processor's work on it cost microseconds. "
            "<bookmark mark='b'/> So the cost of a join is the number of pages read and written, given the size of "
            "each table in pages, M and N, and the number of pages of memory, B. Here R has four hundred pages and S "
            "two hundred. <bookmark mark='c'/> The simplest join fills memory with a block of R, keeping two pages "
            "for input and output, and reads all of S to find the matches, then the next block, and again. "
            "<bookmark mark='d'/> With five pages of memory, that is a hundred and thirty-four blocks, each reading "
            "all of S: twenty-seven thousand page reads, to join tables that hold only six hundred."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(R), FadeIn(S), FadeIn(rl), FadeIn(sl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(mem), FadeIn(ml), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            for blk in range(3):
                chunk = R[blk * 3:blk * 3 + 3]
                self.play(*[p.animate.set_fill(DATA, 0.9) for p in chunk], run_time=0.3)
                self.play(LaggedStart(*[Indicate(p, color=HEAD, scale_factor=1.15) for p in S], lag_ratio=0.08),
                          run_time=1.0)
                self.play(*[p.animate.set_fill(DATA, 0.25) for p in chunk], run_time=0.2)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def algorithms(self):
        head = label(r"Four ways to join", font_size=36).to_edge(UP, buff=0.3)
        spec = [
            ("block nested loops", r"blocks of $R$ against all of $S$", r"$M + \lceil M/(B-2)\rceil N$",
             r"needs no index, \ no order; \ fine when one side fits"),
            ("index nested loops", r"for each row of $R$, \ probe an index on $S$", r"$M + |R|\,(1 + \text{match pages})$",
             r"wins when $R$ is small: \ a few probes, \ not a scan"),
            ("sort-merge", r"sort both by the key, \ then one merging pass", r"$2M p_R + 2N p_S + M + N$",
             r"$p$ passes of external sort; \ output arrives sorted"),
            ("grace hash", r"hash both into $B-1$ buckets on disk, \ join bucket by bucket", r"$3\,(M + N)$",
             r"each input read twice, \ written once, \ if buckets fit: \ $B \gtrsim \sqrt{M}$"),
        ]
        cards = VGroup()
        for name, idea, cost, note_ in spec:
            c = ACOL[name]
            g = VGroup(label(rf"\textbf{{{name}}}", font_size=22, color=c), label(idea, font_size=18, color=WHITE),
                       label(cost, font_size=22, color=c), label(note_, font_size=16, color=GREY_A)).arrange(
                DOWN, buff=0.13)
            frame = SurroundingRectangle(g, buff=0.2, color=c, stroke_width=1.5, corner_radius=0.08)
            frame.stretch_to_fit_width(6.2)
            frame.stretch_to_fit_height(2.3)
            frame.move_to(g)
            cards.add(VGroup(frame, g))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.3)).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "There are four classic ways to join. <bookmark mark='a'/> Block nested loops, which needs nothing: no "
            "index, no order. <bookmark mark='b'/> Index nested loops: for each row of R, look its key up in an index "
            "on S. Each lookup costs a page or two, so it wins when R is small. <bookmark mark='c'/> Sort-merge: sort "
            "both tables on the join key, with Part 16's external merge sort, then walk them together once. Its cost "
            "is the sorting passes, and its output comes out in order, which a later operator may want. "
            "<bookmark mark='d'/> And the hash join, in the form first built for the Grace database machine in Tokyo: "
            "hash both tables into buckets on disk, so that matching rows land in matching buckets, then join each "
            "pair of buckets in memory. Every page is read, written and read again: three times M plus N, as long as "
            "each bucket fits in memory."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        jr = load("joins")["rows"]
        head = label(r"Formula against measurement", font_size=36).to_edge(UP, buff=0.3)
        Bs = [r["B"] for r in jr]
        rows, colors = [], []
        for a in ALGS:
            rows.append([a] + [num(r["measured"][a]) for r in jr])
            colors.append([ACOL[a]] + [WHITE] * len(jr))
            rows.append([r"\ \ formula"] + [num(r["formula"][a]) for r in jr])
            colors.append([GREY_B] * (len(jr) + 1))
        tab = grid_table([r"pages read and written"] + [rf"$B$ = {b}" for b in Bs], rows,
                         widths=[3.6] + [1.45] * len(Bs), row_h=0.36, font_size=18, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        for r in range(2, len(rows) + 1, 2):
            for c in tab.cells[r]:
                c.scale(0.85)
        for k, r in enumerate(jr):
            if not r["buckets_fit"]:
                tab.cells[7][k + 1].set_color(NO)
                tab.cells[8][k + 1].set_color(NO)
        lines = VGroup(
            label(r"block nested loops and sort-merge: \ the counts equal the formulas exactly", font_size=19,
                  color=YES),
            label(r"index nested loops reads less: \ 13\% of keys of $R$ have no match in $S$, \ and their probe "
                  r"stops at the bucket", font_size=19, color=KERN),
            label(r"Grace hash: \ partly filled bucket pages add 1--9\%; \ in red, \ $B < 40$: \ a bucket of $R$ "
                  r"no longer fits, \ and it must be split again", font_size=19, color=NO),
            label(r"no algorithm always wins: \ with ample memory block nested loops is cheapest; \ with little, \ "
                  r"hashing, \ by fifteen times", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "Formulas like these fill database textbooks. Our joins count every page they touch, so we can check "
            "them, for five sizes of memory. <bookmark mark='a'/> Block nested loops and sort-merge match their "
            "formulas exactly, page for page. <bookmark mark='b'/> Index nested loops reads less than its formula, "
            "because the formula assumes every probe finds a match, and thirteen percent of R's keys have none. "
            "<bookmark mark='c'/> The hash join pays a little for buckets whose last page is half full, and with "
            "under forty pages of memory a bucket no longer fits, so a real system would partition it again. "
            "<bookmark mark='d'/> Most important, the winner changes. With eighty pages of memory the simplest join "
            "is the cheapest; with five, hashing is fifteen times cheaper. The right algorithm depends on the sizes, "
            "and only the database knows the sizes. That is why it, and not the programmer, should choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
