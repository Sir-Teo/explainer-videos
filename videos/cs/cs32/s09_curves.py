from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, COST, DATA, HEAD, LAM, NO, PART, YES, curve, fit_right, grid_table, load,
                                   mono)

PC = {"opt": YES, "lru": DATA, "fifo": NO, "clock": GREY_B, "2q": COST, "arc": HEAD, "lirs": LAM, "random": GREY_D}


def faults_axes(xmax, ymin, ymax, xstep, xlabel):
    ax = Axes(x_range=[0, xmax, xstep], y_range=[ymin, ymax, 1], x_length=6.4, y_length=3.9,
              axis_config={"color": GREY_D, "include_numbers": False})
    xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, ymin), DOWN, buff=0.08)
                  for x in range(0, xmax + 1, xstep)])
    yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                  for k in range(ymin, ymax + 1)])
    xl = label(xlabel, font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
    return ax, VGroup(ax, xt, yt, xl)


class Curves(VoiceoverScene):
    def construct(self):
        self.card()
        self.job()
        self.stack()
        self.scans()
        self.wset()
        self.thrash()

    def card(self):
        card = chapter_card(8, r"Working sets and thrashing", r"How much memory does a program need?",
                            lit=(1968, 1970), extra=((1968, r"Denning: \ the working set"), (1970, r"Mattson's stack "
                                                                                                  r"algorithms")),
                            part=PART)
        with self.voiceover("Chapter eight. Working sets, and thrashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def job(self):
        d = load("curves")
        head = label(r"Every policy, \ on the Job's references", font_size=34).to_edge(UP, buff=0.3)
        sz = d["job_sizes"]
        ax, axes = faults_axes(40, 1, 5, 8, r"frames \ (1 KiB pages)")
        axes.to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        cvs = VGroup()
        for p in ("fifo", "random", "clock", "lru", "arc", "lirs", "opt"):
            cvs.add(curve(ax, sz, [math.log10(max(v, 1)) for v in d["job"][p]], PC[p], width=2.5))
        keys = VGroup(*[label(p.upper() if p != "random" else "random", font_size=17, color=PC[p])
                        for p in ("fifo", "random", "clock", "lru", "arc", "lirs", "opt")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to(ax.c2p(33, 4.2))
        refs = f"{d['job_refs']:,}".replace(",", "{,}")
        o, lr, ff = d["job"]["opt"], d["job"]["lru"], d["job"]["fifo"]
        i8 = sz.index(8)
        notes = VGroup(
            label(rf"the Job on {d['job_bytes']:,} bytes".replace(",", "{,}") + rf": \\ {refs} references to "
                  rf"{d['job_pages']} pages", font_size=20, color=WHITE),
            label(rf"with 8 frames: \ OPT {o[i8]:,}, \\ LRU {lr[i8]:,}, \ FIFO {ff[i8]:,}".replace(",", "{,}"),
                  font_size=20, color=GREY_A),
            label(r"LRU sits between OPT and FIFO; \\ CLOCK close behind LRU", font_size=20, color=DATA),
            label(r"LRU's whole curve from one pass: \\ stack distances \ (Mattson et al., 1970)", font_size=20,
                  color=YES),
            label(r"by 40 frames every page fits: \\ only the 39 first touches", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How do the policies compare on a real program? <bookmark mark='a'/> We recorded every memory reference of "
            "the Job on a sixteen-kilobyte passage, a hundred and twenty thousand of them, to thirty-nine pages of one "
            "kibibyte, and replayed them through each policy at every memory size. <bookmark mark='b'/> With eight "
            "frames, the optimum takes twelve thousand faults, LRU twenty-three thousand, and FIFO twenty-nine "
            "thousand. <bookmark mark='c'/> LRU sits between the optimum and FIFO, with CLOCK close behind it. "
            "<bookmark mark='d'/> And because LRU is a stack algorithm, its whole curve comes from a single pass over "
            "the trace, by recording how deep each page is in the recency stack when it is used again: Mattson and "
            "his colleagues' trick from 1970, which caches are still sized with. <bookmark mark='e'/> With forty "
            "frames everything fits, and only the first touches fault."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.2), FadeIn(keys), FadeIn(notes[0]),
                      run_time=3.0)
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def stack(self):
        string = list("abcbadca")
        head = label(r"Mattson's trick, \ by hand", font_size=36).to_edge(UP, buff=0.3)
        st, dist = [], []
        cols = VGroup()
        for p in string:
            dd = st.index(p) + 1 if p in st else None
            dist.append(dd)
            cells = VGroup()
            for i in range(4):
                v = st[i] if i < len(st) else ""
                hl = dd is not None and i == dd - 1
                r = Rectangle(width=0.62, height=0.46, stroke_color=HEAD if hl else GREY_D, stroke_width=2 if hl else 1,
                              fill_color=HEAD if hl else BG, fill_opacity=0.3 if hl else 1)
                cells.add(VGroup(r, mono(v, 18, WHITE if hl else GREY_A).move_to(r)))
            cells.arrange(DOWN, buff=0)
            top = mono(p, 22, WHITE)
            dl = MathTex(r"\infty" if dd is None else str(dd), font_size=28, color=NO if dd is None else HEAD)
            cols.add(VGroup(top, cells, dl).arrange(DOWN, buff=0.14))
            if p in st:
                st.remove(p)
            st.insert(0, p)
        cols.arrange(RIGHT, buff=0.22).next_to(head, DOWN, buff=0.5).shift(LEFT * 2.2)
        sl = label(r"the recency stack \\ before each reference \\ (most recent on top)", font_size=17,
                   color=GREY_A).next_to(cols, LEFT, buff=0.25)
        if sl.get_left()[0] < -6.9:
            VGroup(sl, cols).shift(RIGHT * (-6.9 - sl.get_left()[0]))
        dl_ = label(r"distance", font_size=17, color=HEAD).next_to(cols[0][2], LEFT, buff=0.25)
        n = len(string)
        miss = {k: sum(1 for d in dist if d is None or d > k) for k in range(1, 5)}
        tab = grid_table([r"frames $k$", r"misses $= \#\{d > k\}$"], [[str(k), str(v)] for k, v in miss.items()],
                         widths=[1.4, 2.6], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(cols, RIGHT, buff=0.6).align_to(cols, UP)
        lines = VGroup(
            label(r"a reference hits with $k$ frames exactly when its page is among the top $k$: \ distance $\le k$",
                  font_size=21, color=WHITE),
            label(rf"so one pass over {n} references gives LRU's misses for \textit{{every}} memory size at once",
                  font_size=21, color=YES),
            label(r"that is how chapter 8's whole LRU curve came from a single pass, \ and how caches are still sized",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is that trick worked by hand, on eight references. <bookmark mark='a'/> Keep the pages in a stack, "
            "most recently used on top. For each reference, find how deep its page is: that depth is its stack "
            "distance. A page never seen before has distance infinity. <bookmark mark='b'/> Then move it to the top. "
            "Page b is found at depth two, a at depth three, c at depth four. <bookmark mark='c'/> Now the key fact. "
            "LRU with k frames holds exactly the top k pages of this stack, so a reference hits precisely when its "
            "distance is at most k. <bookmark mark='d'/> Count the distances greater than k, and you have LRU's "
            "misses: eight with one frame, seven with two, five with three, four with four. <bookmark mark='e'/> One "
            "pass gives every memory size at once. That is how the whole LRU curve came from a single pass over the "
            "Job's trace, and how cache sizes are still chosen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(dl_), LaggedStart(*[FadeIn(c) for c in cols[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cols[3:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def scans(self):
        d = load("curves")
        head = label(r"A scan flushes LRU", font_size=34).to_edge(UP, buff=0.3)
        sz = d["scan_sizes"]
        ax, axes = faults_axes(80, 1, 5, 16, r"frames")
        axes.to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        cvs = VGroup()
        for p in ("lru", "clock", "2q", "arc", "lirs", "opt"):
            cvs.add(curve(ax, sz, [math.log10(max(v, 1)) for v in d["scan"][p]], PC[p], width=2.5))
        keys = VGroup(*[label(p.upper(), font_size=17, color=PC[p]) for p in ("lru", "clock", "2q", "arc", "lirs",
                                                                               "opt")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to(ax.c2p(14, 2.3))
        s = d["scan"]
        i32 = sz.index(32)
        notes = VGroup(
            label(r"a trace like a database's: \\ 20 hot pages, \ and a 60-page scan, \ repeated", font_size=20,
                  color=WHITE),
            label(rf"with 32 frames: \ LRU {s['lru'][i32]:,}, \ ARC {s['arc'][i32]:,}, \\ LIRS {s['lirs'][i32]:,}, "
                  rf"\ OPT {s['opt'][i32]:,}".replace(",", "{,}"), font_size=20, color=GREY_A),
            label(r"each scan pushes the hot pages out of LRU \\ before they are used again", font_size=20, color=NO),
            label(r"ARC \ (Megiddo and Modha, 2003) \\ balances recency against frequency; \\ LIRS \ (Jiang and Zhang, "
                  r"2002) \\ ranks pages by reuse distance", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "LRU has a famous weakness. <bookmark mark='a'/> Here is a trace like a database's: twenty hot pages used "
            "over and over, and then a scan through sixty pages, used once, again and again. <bookmark mark='b'/> With "
            "thirty-two frames, LRU faults on almost every reference, and so does CLOCK. <bookmark mark='c'/> Each "
            "scan pushes the hot pages out just before they are needed again, because the scanned pages are more "
            "recent. <bookmark mark='d'/> The adaptive replacement cache, ARC, keeps two lists, pages seen once and "
            "pages seen twice, and moves the boundary between them as it learns. LIRS ranks pages by the distance "
            "between their last two uses, so a page used once never displaces a page used often. Both do far better, "
            "and LIRS approaches the optimum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.2), FadeIn(keys), FadeIn(notes[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def wset(self):
        d = load("wset")
        head = label(r"The working set", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 610, 100], y_range=[0, 40, 10], x_length=10.0, y_length=3.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([0.3, 0.6, 0])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 10, 20, 30, 40)])
        xl = label(r"position in the Job's references \ (every 200th)", font_size=17, color=GREY_A).next_to(
            ax, DOWN, buff=0.15)
        cvs = VGroup()
        for tau, c in (("100", YES), ("1000", HEAD), ("10000", DATA)):
            v = d["ws"][tau]
            cvs.add(VMobject(color=c, stroke_width=2).set_points_as_corners([ax.c2p(i, y) for i, y in enumerate(v)]))
        keys = VGroup(*[label(t, font_size=17, color=c) for t, c in ((r"$\tau = 100$", YES), (r"$\tau = 1{,}000$", HEAD),
                                                                      (r"$\tau = 10{,}000$", DATA))]).arrange(
            RIGHT, buff=0.5).next_to(ax, UP, buff=0.15)
        lines = VGroup(
            label(r"Denning \ (1968): \ $W(t, \tau)$, \ the pages used in the last $\tau$ references", font_size=21,
                  color=WHITE),
            label(r"keep each process's working set in memory, \ or do not run it at all", font_size=21, color=YES),
            label(r"the Job's moves in phases: \ reading text, \ then the report", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Peter Denning gave the idea that ties this together. <bookmark mark='a'/> A program's working set at "
            "time t is the set of pages it used in the last tau references. <bookmark mark='b'/> Here it is along the "
            "Job's trace, for three windows: in any hundred references the Job uses about nine pages, over longer ones "
            "it reaches all thirty-nine. <bookmark mark='c'/> Denning's rule for a time-shared machine: keep each "
            "running process's working set in memory, and if they do not all fit, run fewer processes."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xl), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(Create(cvs[0]), FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cvs[1]), Create(cvs[2]), FadeIn(keys[1:]), FadeIn(lines[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def thrash(self):
        d = load("wset")
        head = label(r"Thrashing", font_size=36).to_edge(UP, buff=0.3)
        th = d["thrash"]
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 0.6, 0.1], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in range(0, 11, 2)])
        yt = VGroup(*[label(f"{int(y * 100)}\\%", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 0.2, 0.4, 0.6)])
        xl = label(r"processes sharing 64 frames", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"processor busy", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cv = curve(ax, [r["n"] for r in th], [r["util"] for r in th], NO)
        best = max(th, key=lambda r: r["util"])
        notes = VGroup(
            label(r"each process: \ a working set of 20 pages, \\ and some ordinary waits for I/O", font_size=20,
                  color=WHITE),
            label(rf"more processes overlap the waits: \\ {best['util'] * 100:.0f}\% busy at {best['n']}", font_size=20,
                  color=YES),
            label(r"past 64 / 20, \ the working sets no longer fit: \\ every process faults, \ and waits for the disk",
                  font_size=20, color=NO),
            label(r"at 8, \ the processor is idle: \\ the machine is all disk", font_size=20, color=NO),
            label(r"the cure: \ swap whole processes out, \\ or kill one \ (Linux's out-of-memory killer)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Break that rule and you get thrashing. <bookmark mark='a'/> We simulated processes sharing sixty-four "
            "frames, each with a working set of twenty pages, and each sometimes waiting for ordinary input or output. "
            "<bookmark mark='b'/> With more processes, the processor fills the waits with other work, up to half busy "
            "with three. <bookmark mark='c'/> But four working sets of twenty do not fit in sixty-four frames. Now "
            "every process faults, each fault waits for the one disk, and utilisation falls. <bookmark mark='d'/> At "
            "eight processes the processor is almost idle, and the disk never stops: the machine is all paging. "
            "<bookmark mark='e'/> Operating systems in the sixties learned to respond by taking whole processes out of "
            "memory; Linux, when memory is truly exhausted, kills one."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.0)
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
