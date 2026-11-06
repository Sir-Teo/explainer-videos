from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (DATA, FILEC, HEAD, KERN, NO, PART, YES, code, grid_table, load)


class Fsync(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.patterns()
        self.studies()

    def card(self):
        card = chapter_card(13, r"fsync, \ and what applications must do", r"When is data really on the disk?",
                            lit=(2009, 2018), extra=((2009, r"ext4's empty files"), (2018, r"``fsyncgate''")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Fsync, and what applications must do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def layers(self):
        head = label(r"Where a write waits", font_size=36).to_edge(UP, buff=0.3)
        stages = [(r"the program's buffer", DATA, r"\texttt{fwrite}: \ not even the kernel has it"),
                  (r"the page cache", HEAD, r"\texttt{write} returns here; \ written back within about 30 s"),
                  (r"the drive's cache", KERN, r"volatile memory inside the disk: \ lost with the power"),
                  (r"the platter, \ or the flash", FILEC, r"durable")]
        boxes = VGroup()
        for t, c, note in stages:
            r = RoundedRectangle(width=3.6, height=0.7, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.12)
            boxes.add(VGroup(r, label(t, font_size=21, color=WHITE).move_to(r),
                             label(note, font_size=18, color=GREY_A).next_to(r, RIGHT, buff=0.4)))
        boxes.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        arrows = VGroup(*[Arrow(boxes[i][0].get_bottom(), boxes[i + 1][0].get_top(), buff=0.05, color=GREY_B,
                                stroke_width=2) for i in range(3)])
        lines = VGroup(
            label(r"\texttt{fsync(fd)}: \ write the file's dirty pages and its metadata, \ then tell the drive to "
                  r"\textbf{flush} its cache", font_size=20, color=YES),
            label(r"for a new or renamed file, \ fsync the \textbf{directory} too: \ the name is in the directory's "
                  r"blocks", font_size=20, color=HEAD),
            label(r"a drive that acknowledges a flush it has not done makes all of this, \ and every journal, \ a "
                  r"fiction", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When a program writes, where do the bytes go? <bookmark mark='a'/> With buffered input and output, first "
            "into the program's own buffer, which not even the kernel can see. <bookmark mark='b'/> Then into the "
            "kernel's page cache. The write call returns here, and the kernel writes the page back to the disk at "
            "its convenience, within about thirty seconds. <bookmark mark='c'/> Even then, the drive may hold it in "
            "its own volatile cache. <bookmark mark='d'/> Only then is it durable. <bookmark mark='e'/> Fsync is the "
            "call that pushes a file through every stage: its pages, its metadata, and a flush command to the drive. "
            "<bookmark mark='f'/> A new file's name lives in its directory, so the directory needs an fsync too. "
            "<bookmark mark='g'/> And all of it, journals included, rests on drives honouring flushes, which some "
            "cheap ones have not."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[i]), *([GrowArrow(arrows[i - 1])] if i else []))
            for mk, ln in zip("efg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def patterns(self):
        d = load("apps")
        head = label(r"Replacing a file's contents, \ crashed at every point", font_size=34).to_edge(UP, buff=0.3)
        src = code([
            "write(fd, new, n)                  // 1. in place",
            "",
            "write(tmp, new, n); rename(tmp, f) // 2. by rename",
            "",
            "write(tmp, new, n); fsync(tmp);    // 3. the safe way",
            "rename(tmp, f); fsync(dir)",
        ], size=18).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.7)
        R = {(r["pattern"], r["delayed"]): r for r in d["rows"]}

        def cell(r):
            bad = r["states"] - r["ok"]
            if not bad:
                return rf"all {r['states']} intact"
            kind = {"torn": r"half old, \ half new", "empty": r"an \textbf{empty} file"}[r["kinds"][0]]
            return rf"{bad} of {r['states']}: \ {kind}"
        rows = [[p, cell(R[(p, False)]), cell(R[(p, True)])] for p in ("in place", "write, rename",
                                                                        "write, fsync, rename")]
        tab = grid_table([r"", r"blocks allocated at once", r"delayed allocation"], rows, widths=[3.2, 3.5, 3.9],
                         row_h=0.5, font_size=19, mono_cols=())
        tab.next_to(src, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        cols = {(1, 1): NO, (1, 2): NO, (2, 1): YES, (2, 2): NO, (3, 1): YES, (3, 2): YES}
        for (r, c), col in cols.items():
            tab.cells[r][c].set_color(col)
        lines = VGroup(
            label(r"in place is never safe: \ a crash between two block writes tears the file", font_size=20,
                  color=NO),
            label(r"rename is atomic, \ but with delayed allocation the new file's \textit{data} may not exist yet: "
                  r"\ ext4, \ 2009", font_size=20, color=NO),
            label(r"fsync before rename: \ every crash point leaves the old file or the new one", font_size=20,
                  color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the application's side. A program wants to replace a small file, a configuration or a saved game, "
            "and our checker crashes each way of doing it at every point, on ordered PebbleFS. <bookmark mark='a'/> "
            "Overwriting it in place tears it: a crash between the block writes leaves half old and half new. "
            "Journaling metadata does not protect data written in place. <bookmark mark='b'/> Writing a new file and "
            "renaming it over the old one is the classic idiom, because rename is atomic. With blocks allocated at "
            "once, it survives. But with delayed allocation, the rename can reach the disk before the new file's data "
            "even has blocks. A crash then leaves an empty file. This is exactly what happened when ext4 arrived in "
            "2009, and users lost their settings. <bookmark mark='c'/> The safe way: write the new file, fsync it, then "
            "rename, then fsync the directory. Every crash point leaves either the old file or the new one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(src[0]), *[FadeIn(m) for m in tab.cells[1]], FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(src[2]), *[FadeIn(m) for m in tab.cells[2]], FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(src[4]), FadeIn(src[5]), *[FadeIn(m) for m in tab.cells[3]], FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def studies(self):
        head = label(r"What the studies found", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(a, font_size=22, color=c), label(b, font_size=18, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07) for a, b, c in (
            (r"Pillai et al., \ \textit{All File Systems Are Not Created Equal} \ (2014)",
             r"a tool that explores crash states of real programs: \ 60 vulnerabilities in 11 applications, \ "
             r"including databases and version control", HEAD),
            (r"each file system persists in its own order",
             r"code that survives crashes on one may lose data on another; \ POSIX promises very little", KERN),
            (r"``fsyncgate'' \ (PostgreSQL, \ 2018)",
             r"after a failed write-back, \ Linux reported the error once and marked the pages clean; \ PostgreSQL "
             r"retried fsync, \ which succeeded, \ and the data was gone", NO),
            (r"the lesson", r"a failed fsync means the data is lost: \ do not retry, \ recover from your own log; \ "
                            r"PostgreSQL now stops and replays its journal", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        with self.voiceover(
            "Real programs get this wrong all the time. <bookmark mark='a'/> In 2014 Pillai and colleagues built a "
            "tool that records a program's system calls and explores the crash states a file system allows. Across "
            "eleven widely used applications, databases and version control among them, it found sixty places where "
            "a crash could lose or corrupt data. <bookmark mark='b'/> Part of the trouble is that each file system "
            "persists operations in its own order, and the standard promises very little, so code that is safe on "
            "one can fail on another. <bookmark mark='c'/> And in 2018 the PostgreSQL developers discovered that when "
            "Linux failed to write a page back, it reported the error once, then marked the page clean. PostgreSQL "
            "retried the fsync, the retry succeeded, and the write was silently lost. <bookmark mark='d'/> The lesson: "
            "a failed fsync means the data is gone. Do not retry. PostgreSQL now stops, and recovers from its own "
            "write-ahead log, which is where Part 35 picks up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
