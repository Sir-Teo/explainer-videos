from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, TCOL, YES, grid_table, load, num)


def log_cell(r, w=0.92):
    kind = r["kind"]
    c = TCOL.get(r["txn"], GREY_B)
    txt = {"update": f"T{r['txn']} p{r['page']}", "commit": f"T{r['txn']} C", "end": f"T{r['txn']} end",
           "clr": f"CLR p{r['page']}"}[kind]
    rect = Rectangle(width=w, height=0.62, stroke_color=c, stroke_width=1.6,
                     fill_color=c if kind != "update" else BLACK, fill_opacity=0.25 if kind != "update" else 0)
    lsn = Text(str(r["lsn"]), font="DejaVu Sans Mono", font_size=12, color=GREY_B)
    t = Text(txt, font="DejaVu Sans Mono", font_size=13, color=c)
    g = VGroup(rect, VGroup(lsn, t).arrange(DOWN, buff=0.05).move_to(rect))
    return g


class Aries(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.example()
        self.passes()
        self.tested()

    def card(self):
        card = chapter_card(13, r"Recovery: \ ARIES", r"How does a database survive a crash at any instant?",
                            lit=(1992,), extra=((1992, r"Mohan et al.: \ ARIES"),), part=PART)
        with self.voiceover("Chapter thirteen. Recovery."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rules(self):
        head = label(r"Pages, \ a buffer, \ and a log", font_size=36).to_edge(UP, buff=0.3)
        mem = VGroup(*[Square(0.6, stroke_color=HEAD, stroke_width=1.8) for _ in range(4)]).arrange(RIGHT, buff=0.15)
        disk = VGroup(*[Square(0.6, stroke_color=DATA, stroke_width=1.8) for _ in range(6)]).arrange(RIGHT, buff=0.15)
        logs = VGroup(*[Rectangle(width=0.45, height=0.6, stroke_color=KERN, stroke_width=1.5) for _ in range(12)]).arrange(
            RIGHT, buff=0.04)
        mem.move_to([-3.2, 1.6, 0])
        disk.move_to([-3.2, -0.2, 0])
        logs.move_to([3.4, -0.2, 0])
        ml = label(r"buffer pool \ (memory)", font_size=18, color=HEAD).next_to(mem, UP, buff=0.12)
        dl = label(r"data pages \ (disk)", font_size=18, color=DATA).next_to(disk, DOWN, buff=0.12)
        ll = label(r"the log \ (disk, \ append only)", font_size=18, color=KERN).next_to(logs, DOWN, buff=0.12)
        lines = VGroup(
            label(r"\textbf{steal}: \ a dirty page of an uncommitted transaction may be written to disk \ (to free "
                  r"memory): \ so recovery must \textit{undo}", font_size=19, color=NO),
            label(r"\textbf{no-force}: \ commit does not write the data pages \ (too slow): \ so recovery must "
                  r"\textit{redo}", font_size=19, color=HEAD),
            label(r"\textbf{write-ahead logging}: \ a page reaches disk only after the log records describing it; "
                  r"\ commit = the commit record is on disk", font_size=19, color=YES),
            label(r"each record: \ LSN, \ transaction, \ page, \ before and after values, \ the transaction's "
                  r"previous LSN; \ each page remembers the last LSN applied to it", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Part 34 made a file system survive crashes with a journal. A database faces the same problem with "
            "stricter demands, and the standard answer is ARIES, by C. Mohan and colleagues at IBM, from 1992. "
            "<bookmark mark='a'/> Pages are changed in a buffer in memory, and the buffer writes them back when it "
            "likes. ARIES allows it to steal: to write a page that an uncommitted transaction has changed. So after a "
            "crash, the disk may hold changes that must be undone. <bookmark mark='b'/> And it allows no-force: a "
            "commit does not wait for the data pages to be written. So the disk may lack committed changes, which "
            "must be redone. <bookmark mark='c'/> Both are safe because of one rule, write-ahead logging: every change "
            "is first described in an append-only log, and a page may go to disk only after its log records have. A "
            "transaction has committed when its commit record is on disk. <bookmark mark='d'/> Each log record holds "
            "its sequence number, its transaction, the page, the values before and after, and a pointer to the "
            "transaction's previous record. And each page records the sequence number of the last change applied to "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mem), FadeIn(ml), FadeIn(disk), FadeIn(dl))
            vo.wait_until("a")
            self.play(mem[1].animate.set_fill(NO, 0.5), FadeIn(lines[0]))
            self.play(mem[1].copy().animate.move_to(disk[2]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(logs), FadeIn(ll), FadeIn(lines[2]))
            self.play(LaggedStart(*[lg.animate.set_fill(KERN, 0.5) for lg in logs[:7]], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def example(self):
        a = load("aries")
        head = label(r"A crash", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup(*[log_cell(r) for r in a["log"]]).arrange(RIGHT, buff=0.06).next_to(head, DOWN, buff=0.5)
        detail = VGroup(*[Text(f"{r['before']}→{r['after']}" if r["kind"] == "update" else "", font="DejaVu Sans Mono",
                               font_size=12, color=GREY_A).next_to(c, DOWN, buff=0.08)
                          for r, c in zip(a["log"], cells)])
        crash = VGroup(Line(UP * 0.5, DOWN * 0.5, color=NO, stroke_width=5),
                       label(r"crash", font_size=18, color=NO)).arrange(DOWN, buff=0.08).next_to(cells, RIGHT, buff=0.2)
        rows = []
        for p in sorted(a["disk_at_crash"], key=int):
            v, plsn = a["disk_at_crash"][p]
            rows.append([f"page {p}", str(v), str(plsn), str(a["expect"][p])])
        tab = grid_table([r"at the crash", r"value on disk", r"page LSN", r"should be"], rows,
                         widths=[1.9, 2.0, 1.7, 1.7], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(detail, DOWN, buff=0.5).set_x(-3.2)
        for r in range(1, 5):
            tab.cells[r][3].set_color(YES)
        notes = VGroup(
            label(r"$T_3$ committed and ended; \ $T_2$ committed; \\ $T_1$ was still running: \ a \textbf{loser}",
                  font_size=20, color=WHITE),
            label(r"page 0 has lost $T_3$'s last two changes \\ (no-force)", font_size=20, color=HEAD),
            label(r"page 3 holds $T_1$'s first change \\ (steal)", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        with self.voiceover(
            "Here is a crash, from our implementation. <bookmark mark='a'/> Three transactions updated four pages. "
            "The log that reached the disk has twelve records: T3 made three updates to page 0, committed, and "
            "ended; T2 updated page 1 three times and committed; T1 updated pages 3 and 2 and 3 again, and had not "
            "committed. <bookmark mark='b'/> Then the power failed. The buffer pool is gone; the disk has whatever "
            "pages happened to be written. <bookmark mark='c'/> Page 0 has the value 72, from T3's first update: its "
            "last two updates never reached the disk, though T3 committed. <bookmark mark='d'/> And page 3 holds T1's "
            "first change, though T1 never committed. The right state is on the right: every committed change, and "
            "none of T1's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08), FadeIn(detail))
            vo.wait_until("b")
            self.play(FadeIn(crash), FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(tab.cells[1][1], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), Indicate(tab.cells[4][1], color=NO))
        self.wait(0.3)
        self.clear_scene()

    def passes(self):
        a = load("aries")
        P = a["passes"]
        head = label(r"Three passes: \ analysis, \ redo, \ undo", font_size=36).to_edge(UP, buff=0.3)
        allrec = a["log"] + [{"lsn": x["lsn"], "kind": x["kind"], "txn": x["txn"], "page": x["page"]}
                             for x in a["appended"]]
        cells = VGroup(*[log_cell(r, w=0.7) for r in allrec]).arrange(RIGHT, buff=0.05).next_to(head, DOWN, buff=0.5)
        if cells.width > 13.2:
            cells.width = 13.2
        cells.set_x(0)
        n0 = len(a["log"])
        an = a["analysis"]
        lines = VGroup(
            label(rf"\textbf{{analysis}}, \ forward: \ which transactions were running \ (loser: \ "
                  rf"$T_{an['losers'][0]}$), \ which pages may be dirty, \ and where redo must start \ "
                  rf"(LSN {P['redo_from']})", font_size=19, color=HEAD),
            label(rf"\textbf{{redo}}, \ forward: \ \textit{{repeat history}}: \ reapply every update, \ the loser's "
                  rf"too, \ unless the page LSN shows it is there: \ {P['redone']} redone, \ {P['skipped']} skipped",
                  font_size=19, color=YES),
            label(r"\textbf{undo}, \ backward: \ roll the losers back along their prev pointers: \ LSN "
                  + r", \ ".join(str(u) for u in P["undo_order"]) + r"; \ each undo logs a \textbf{CLR}", font_size=19,
                  color=NO),
            label(r"a CLR says what was undone and where undo resumes: \ crash during recovery, \ and the second "
                  r"recovery never undoes an undo", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cells, DOWN, buff=0.6).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        res = label(r"after recovery: \ page 0 = 18, \ page 1 = 3, \ page 2 = 0, \ page 3 = 0: \ exactly the "
                    r"committed state", font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        idx = {r["lsn"]: k for k, r in enumerate(allrec)}
        redone = [5, 7, 8, 11]
        with self.voiceover(
            "Recovery runs in three passes. <bookmark mark='a'/> Analysis reads the log forward and rebuilds what "
            "memory held: which transactions were active, here only T1, the loser, and which pages may have been "
            "dirty, which tells redo where to start. <bookmark mark='b'/> Redo reads forward again and repeats "
            "history: it reapplies every logged update, including the loser's, except where the page's own sequence "
            "number shows the change already reached the disk. Four updates are redone and five skipped. Now the "
            "pages are exactly as they were at the instant of the crash. <bookmark mark='c'/> Undo then walks the "
            "loser's records backward through their pointers, 11, then 5, then 1, restoring the before values. "
            "<bookmark mark='d'/> Each undo is itself logged, as a compensation record, which says where undoing "
            "should resume. If the machine crashes during recovery, the next recovery redoes these records and never "
            "undoes the same change twice. <bookmark mark='e'/> The result is exactly the committed state."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[:n0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), LaggedStart(*[Indicate(c, color=HEAD, scale_factor=1.05) for c in cells[:n0]],
                                                    lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            self.play(LaggedStart(*[Indicate(cells[idx[k]], color=YES, scale_factor=1.15) for k in redone],
                                  lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            for k in P["undo_order"]:
                self.play(Indicate(cells[idx[k]], color=NO, scale_factor=1.15), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]), LaggedStart(*[FadeIn(c) for c in cells[n0:]], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def tested(self):
        a = load("aries")
        R = a["random"]
        head = label(r"Crashing it on purpose", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"crash at a random moment, \ recover", f"{R['ok']} / {R['runs']}"],
                [r"\ \ and crash again in the middle of undo, \ recover again", f"{R['ok_undo_crash']} / {R['runs']}"]]
        tab = grid_table([r"500 random workloads \ (strict 2PL, \ steal, \ no-force)", r"committed state exact"], rows,
                         widths=[7.6, 3.2], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for r in (1, 2):
            tab.cells[r][1].set_color(YES)
        lines = VGroup(
            label(rf"over all runs: \ {num(R['redone'])} updates redone, \ {num(R['skipped'])} skipped by page LSN, \ "
                  rf"{num(R['undone'])} undone", font_size=20, color=WHITE),
            label(r"\textbf{checkpoints} bound the work: \ write the active-transaction and dirty-page tables \\ to "
                  r"the log, \ and analysis starts there", font_size=20, color=HEAD),
            label(r"the same three ideas \ (WAL, \ repeating history, \ logged undo) \ are in DB2, \ SQL Server and "
                  r"many others; \\ PostgreSQL redoes and never undoes, \ because its old versions stay in the table",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "One example proves little, so we crash it on purpose. <bookmark mark='a'/> Five hundred random "
            "workloads, each cut off by a crash at a random moment, then recovered: every one ends in exactly the "
            "committed state. <bookmark mark='b'/> Then the same five hundred, crashed again partway through undo, and "
            "recovered a second time: all five hundred correct. <bookmark mark='c'/> In real systems, checkpoints "
            "bound the work: from time to time the tables that analysis rebuilds are written to the log, and "
            "analysis begins there instead of at the start of time. <bookmark mark='d'/> ARIES's ideas, write-ahead "
            "logging, repeating history, logged undo, are in DB2 and SQL Server and many others. PostgreSQL gets by "
            "with redo alone, because its old row versions stay in the table, and a version written by a transaction "
            "that never committed is simply invisible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.rule), FadeIn(tab.cells[1][0]),
                      FadeIn(tab.cells[1][1]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[2][0]), FadeIn(tab.cells[2][1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA)
