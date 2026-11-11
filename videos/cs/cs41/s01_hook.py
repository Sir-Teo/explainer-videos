from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono)


class Hook(VoiceoverScene):
    def construct(self):
        self.history()
        self.same()
        self.plan()

    def history(self):
        head = label(r"April 2005", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[label(t, font_size=24, color=c) for t, c in (
            (r"1972: \ SCCS \ --- \ 1982: \ RCS: \ one file at a time, \ locks", GREY_A),
            (r"1990: \ CVS: \ many files, \ a central server", GREY_A),
            (r"2000: \ Subversion: \ atomic commits, \ still central", GREY_A),
            (r"2002--2005: \ the Linux kernel on BitKeeper, \ a proprietary distributed system", HEAD),
            (r"April 2005: \ the free licence is withdrawn", NO),
            (r"days later: \ Linus Torvalds starts git; \ it manages its own source within days, \ and the kernel's "
             r"within weeks", YES))]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Version control is older than most of computing's habits. <bookmark mark='a'/> In the seventies and "
            "eighties, SCCS and RCS tracked one file at a time, and you locked a file to change it. CVS, in 1990, "
            "tracked whole projects on a central server; Subversion, in 2000, made commits atomic. "
            "<bookmark mark='b'/> From 2002 the Linux kernel used BitKeeper, a proprietary distributed system, "
            "under a free licence. <bookmark mark='c'/> In April 2005 that licence was withdrawn. "
            "<bookmark mark='d'/> Linus Torvalds started writing a replacement. Within days it could manage its own "
            "source code, and within a few weeks the kernel's. He called it git."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    def same(self):
        o = load("objects")
        head = label(r"Our git, \ and the real one", font_size=36).to_edge(UP, buff=0.3)
        names = [r"\texttt{README.md}", r"\texttt{src/job.py}", r"\texttt{src/util/io.py}", r"root tree", r"commit"]
        ours = [o["ours"]["blobs"]["README.md"], o["ours"]["blobs"]["src/job.py"], o["ours"]["blobs"]["src/util/io.py"],
                o["ours"]["tree"], o["ours"]["commit"]]
        real = [o["git"]["blobs"]["README.md"], o["git"]["blobs"]["src/job.py"], o["git"]["blobs"]["src/util/io.py"],
                o["git"]["tree"], o["git"]["commit"]]
        grid = VGroup()
        hdr = VGroup(label(r"object", font_size=20, color=GREY_B), label(r"our store", font_size=20, color=GREY_B),
                     label(r"git 2.43", font_size=20, color=GREY_B))
        grid.add(hdr)
        for n, a, b in zip(names, ours, real):
            grid.add(VGroup(label(n, font_size=20, color=WHITE), mono(a[:20] + "...", size=17,
                                                                     color=YES if a == b else NO),
                            mono(b[:20] + "...", size=17, color=GREY_A)))
        for row in grid:
            row[0].move_to([-5.0, 0, 0])
            row[1].move_to([-0.6, 0, 0])
            row[2].move_to([4.0, 0, 0])
        for i, row in enumerate(grid):
            row.shift(UP * (1.9 - i * 0.6))
        foot = wrapped_label(r"every object is named by the SHA-1 of its content \ (Part 29): \ write the same files "
                             r"with the same author and date, \ and any git anywhere computes the same names", 12.4,
                             font_size=22, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Git is simpler inside than its commands suggest, simple enough to rebuild. <bookmark mark='a'/> We wrote "
            "a small object store, a few dozen lines, and asked it and the real git to record the same three files "
            "with the same author and time. <bookmark mark='b'/> Every name is identical: the three files, the "
            "directory tree, and the commit. Each object's name is the hash of its contents, Part 29's SHA-1, so "
            "any copy of git anywhere computes the same names for the same history. This part opens up the three "
            "machines every change passes through: version control, the build, and the package manager."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[2])) for r in grid[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in grid[1:]], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Version Control, \ Builds and Dependencies", font_size=36).to_edge(UP,
                                                                                                    buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"git as a content-addressed Merkle graph",
            r"merge bases, \ three-way merge, \ bisect",
            r"packfiles and deltas; \ monorepos",
            r"build systems as incremental computation",
            r"version resolution is NP-complete",
            r"merge queues and canaries: \ shipping safely",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 41 of Computer Science, Built. <bookmark mark='a'/> We will see that git is secretly a "
            "Merkle graph of hashes; that merging is a three-way comparison and bisecting is binary search; that a "
            "build system is an incremental computation over a graph, and that choosing package versions is as hard "
            "as satisfiability. And we will follow a change through a merge queue and a canary release to the "
            "people who use it. Along the way we will measure this repository's own history, its forty versions of "
            "one file, its seventeen thousand objects and the tests each of its modules can reach, because the "
            "tools that built this series are themselves the best specimen of what this part is about."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (DATA, KERN, LAM)
