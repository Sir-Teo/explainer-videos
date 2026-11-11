from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, JRN, META, NO, PART, YES, blk, grid_table, load)
from videos.cs.cs34.s08_crash import row_of

KIND = {"data": (r"data", FILEC), "descriptor": (r"descriptor", JRN), "copy": (r"copy", JRN),
        "commit": (r"commit", YES), "checkpoint": (r"home", META), "clear": (r"clear", GREY_B)}


class Journal(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.recovery()
        self.modes()
        self.barriers()

    def card(self):
        card = chapter_card(8, r"Journaling", r"Can several block writes be made atomic?", lit=(1987, 2001),
                            extra=((1987, r"Hagmann: \ Cedar's log"), (2001, r"ext3")), part=PART)
        with self.voiceover("Chapter eight. Journaling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def protocol(self):
        j = load("journal")
        head = label(r"One append, \ in ordered mode", font_size=36).to_edge(UP, buff=0.3)
        steps = j["steps"]
        cells = VGroup()
        for s in steps:
            if s["kind"] == "flush":
                cells.add(VGroup(DashedLine(UP * 0.55, DOWN * 0.55, color=NO, stroke_width=2.5),
                                 label(r"flush", font_size=16, color=NO).shift(DOWN * 0.75)))
                continue
            nm, c = KIND[s["kind"]]
            what = s["what"].replace("data bitmap", "bitmap").replace("inode table", "inode")
            b = blk(nm, c, w=1.35, h=0.75, font=18, fill=0.3)
            sub = label(what if s["kind"] in ("copy", "checkpoint") else (r"\#" + str(s["block"])), font_size=13,
                        color=GREY_A).scale(1.25).next_to(b, DOWN, buff=0.08)
            cells.add(VGroup(b, sub))
        cells.arrange(RIGHT, buff=0.1).next_to(head, DOWN, buff=0.7)
        if cells.width > 13.2:
            cells.width = 13.2
        notes = VGroup(
            label(r"1. \ the new data, \ in place; \ flush", font_size=22, color=FILEC),
            label(r"2. \ into the journal: \ a \textbf{descriptor} naming the home blocks, \ then copies of the "
                  r"new bitmap and inode; \ flush", font_size=20, color=JRN),
            label(r"3. \ the \textbf{commit} block: \ one block write, \ the atomic moment; \ flush", font_size=20,
                  color=YES),
            label(r"4. \ \textbf{checkpoint}: \ the same blocks to their homes; \ flush; \ then clear the journal",
                  font_size=20, color=META),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(cells, DOWN, buff=0.6)
        groups = [[0, 1], [2, 3, 4, 5], [6, 7], list(range(8, len(cells)))]
        with self.voiceover(
            "A journal, or write-ahead log, is a reserved area of the disk where the file system writes down what it "
            "is about to do. Here is one append, every block write in order. <bookmark mark='a'/> First, in ordered "
            "mode, the new data goes straight to its block, and the disk is flushed. Nothing points at it yet, so this "
            "is harmless. <bookmark mark='b'/> Then, into the journal: a descriptor saying which home blocks this "
            "transaction changes, here the bitmap and the inode, followed by copies of their new contents. Flush. "
            "<bookmark mark='c'/> Then one more block: the commit. A single block write is atomic, so this is the "
            "moment the whole transaction happens. Flush. <bookmark mark='d'/> Only now are the bitmap and the inode "
            "written to their real places, the checkpoint, and then the journal is cleared for the next transaction."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g, n in zip("abcd", groups, notes):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(cells[i]) for i in g], lag_ratio=0.25), FadeIn(n))
        self.wait(0.3)
        self.clear_scene()

    def recovery(self):
        j = load("journal")
        head = label(r"Crash after any write, \ then mount", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for a in j["after"]:
            rows.append([str(a["writes"]), a["recovery"], "clean" if not a["fsck"] else str(a["fsck"]),
                         "the old file" if a["content"] == "old" else "the new file"])
        tab = grid_table([r"crash after write", r"the journal", r"fsck", r"the file"], rows,
                         widths=[2.6, 2.6, 1.6, 2.6], row_h=0.42, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        for r, a in enumerate(j["after"], start=1):
            tab.cells[r][1].set_color({"clean": GREY_A, "discarded": HEAD, "replayed": YES}[a["recovery"]])
            tab.cells[r][3].set_color(GREY_A if a["content"] == "old" else YES)
        lines = VGroup(
            label(r"no commit block: \ the transaction never happened; \ recovery \textbf{discards} it", font_size=21,
                  color=HEAD),
            label(r"a commit block: \ recovery \textbf{replays} the copies to their homes; \ doing it twice is "
                  r"harmless", font_size=21, color=YES),
            label(r"recovery reads the journal, \ not the disk: \ a few blocks, \ however large the disk", font_size=21,
                  color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now crash after each of those writes, and mount the disk. <bookmark mark='a'/> Before the commit block, "
            "the journal holds an unfinished transaction. Recovery sees no commit and throws it away: the old file, "
            "intact. <bookmark mark='b'/> After the commit, recovery copies the journaled blocks to their homes, "
            "whether or not the checkpoint got there first. Replaying twice gives the same result, so a crash during "
            "recovery is harmless too. The new file, intact. <bookmark mark='c'/> And recovery reads only the journal: "
            "a handful of blocks, on a disk of any size. That is why journaling replaced the long fsck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def modes(self):
        c = load("crash")
        head = label(r"What to journal", font_size=36).to_edge(UP, buff=0.3)
        rows, cfg = [], []
        for mode, name in (("writeback", r"metadata only; \ data whenever"), ("ordered", r"data first, \ then "
                                                                                        r"metadata"),
                           ("data", r"data and metadata")):
            r = row_of(c, mode)
            cfg.append(r)
            rows.append([mode, name, str(r["writes"]), str(r["states"]), str(r["corrupt"]), str(r["bad_data"])])
        tab = grid_table([r"mode", r"what goes through the journal", r"writes", r"crash points", r"corrupt",
                          r"wrong bytes"], rows, widths=[1.8, 4.4, 1.3, 1.9, 1.4, 1.9], row_h=0.5, font_size=20,
                         mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.5)
        tab.cells[1][5].set_color(NO)
        for r in (1, 2, 3):
            tab.cells[r][4].set_color(YES)
        tab.cells[2][5].set_color(YES)
        tab.cells[3][5].set_color(YES)
        lines = VGroup(
            label(r"\textbf{writeback}: \ the structures always survive, \ but a file may end in stale bytes",
                  font_size=21, color=NO),
            label(r"\textbf{ordered} \ (ext3 and ext4's default): \ data reaches its home before the metadata that "
                  r"points to it commits", font_size=21, color=YES),
            label(r"\textbf{data}: \ the strongest, \ but every data block is written twice", font_size=21,
                  color=HEAD),
            label(r"real journals batch many operations into one transaction: \ ext4 commits every 5 seconds",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a choice about what goes through the journal. <bookmark mark='a'/> Journal only the metadata, "
            "and let data blocks reach the disk whenever they like, and the structures always survive. But 90 of "
            "the crash points leave a file ending in someone else's old bytes. <bookmark mark='b'/> Ordered mode, the "
            "default in ext3 and ext4, writes the data to its home before the metadata that points to it commits, "
            "which is what we traced. Every crash point comes back intact. <bookmark mark='c'/> Journaling the data "
            "too is just as safe but writes every data block twice. <bookmark mark='d'/> Real journals also batch: "
            "ext4 gathers the changes of many operations into one transaction, committed every five seconds by "
            "default."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def barriers(self):
        c = load("crash")
        nb = row_of(c, "ordered", barriers=False)
        cs = row_of(c, "ordered", barriers=False, jcsum=True)
        head = label(r"Leave out one flush", font_size=36).to_edge(UP, buff=0.3)
        seq = VGroup(blk(r"descriptor", JRN, w=1.6, h=0.6, font=16), blk(r"copies", JRN, w=1.6, h=0.6, font=16),
                     blk(r"commit", YES, w=1.6, h=0.6, font=16)).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.7)
        gone = Cross(DashedLine(UP * 0.4, DOWN * 0.4).move_to((seq[1].get_right() + seq[2].get_left()) / 2),
                     stroke_color=NO, stroke_width=3, scale_factor=0.5)
        q = label(r"the commit may reach the disk before the copies", font_size=20, color=NO).next_to(seq, DOWN,
                                                                                                     buff=0.3)
        od = row_of(c, "ordered")
        rows = [[r"ordered, \ with every flush", str(od["corrupt"]), str(od["bad_data"])],
                [r"ordered, \ no flush before the commit", str(nb["corrupt"]), str(nb["bad_data"])],
                [r"\ldots{} and a checksum of the copies in the commit", str(cs["corrupt"]), str(cs["bad_data"])]]
        tab = grid_table([r"", r"corrupt", r"wrong bytes"], rows, widths=[6.4, 1.6, 2.0], row_h=0.5, font_size=20,
                         mono_cols=())
        tab.next_to(q, DOWN, buff=0.5)
        tab.cells[2][1].set_color(NO)
        tab.cells[3][1].set_color(YES)
        lines = VGroup(
            label(rf"{nb['corrupt']} of {nb['states']} crash points: \ recovery replays the old contents of the journal "
                  r"area, \ left by an earlier transaction", font_size=20, color=NO),
            label(r"a checksum lets recovery tell a whole transaction from a torn one: \ ext4's "
                  r"\texttt{journal\_checksum}", font_size=20, color=YES),
            label(r"so one flush can be saved, \ safely; \ the file system must still trust that a flush is a flush "
                  r"\ (chapter 13)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Each flush makes the file system wait for the disk, so it is tempting to drop one. <bookmark mark='a'/> "
            "Remove the flush between the journal copies and the commit block, and the disk may write the commit "
            "first. <bookmark mark='b'/> The checker finds 25 crash points where recovery sees a commit, replays the "
            "journal, and copies in blocks that were never written for this transaction: stale contents from an "
            "earlier one. Corruption, created by the recovery itself. <bookmark mark='c'/> The fix is a checksum of "
            "the copies, stored in the commit block. Recovery replays only a transaction whose copies match, and every "
            "crash point comes back intact. ext4 does exactly this. <bookmark mark='d'/> It all still rests on the "
            "disk telling the truth about its flushes, which we will question in chapter 13."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seq))
            vo.wait_until("a")
            self.play(Create(gone), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
