from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Isolation(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.definitions()

    def card(self):
        card = chapter_card(12, r"Isolation levels", r"What exactly do the weaker levels give up?",
                            lit=(1992, 1995, 1999), extra=((1995, r"Berenson et al.: \ a critique of ANSI levels"),
                                                           (1999, r"Adya: \ levels as graph conditions")), part=PART)
        with self.voiceover("Chapter twelve. Isolation levels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def table(self):
        iso = load("isolation")
        head = label(r"Six levels, \ five anomalies, \ each one run", font_size=36).to_edge(UP, buff=0.3)
        an = iso["anomalies"]
        rows, colors = [], []
        for lv in iso["levels"]:
            r = iso["table"][lv]
            rows.append([lv] + [r"\checkmark" if r[a] == "prevented" else r"$\times$" for a in an])
            colors.append([WHITE] + [YES if r[a] == "prevented" else NO for a in an])
        tab = grid_table([r"level"] + [a.replace("non-repeatable", r"non-repeat-\\able") for a in an], rows,
                         widths=[3.0] + [1.9] * len(an), row_h=0.48, font_size=19, colors=colors, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        for c in tab.cells[0][1:]:
            if c.width > 1.8:
                c.width = 1.8
        ex = VGroup(
            label(r"\textbf{dirty read}: \ see a write that is later rolled back", font_size=18, color=GREY_A),
            label(r"\textbf{non-repeatable read}: \ read $x$ twice, \ get two values", font_size=18, color=GREY_A),
            label(r"\textbf{lost update}: \ two read-modify-writes, \ one vanishes", font_size=18, color=GREY_A),
            label(r"\textbf{phantom}: \ count the rows twice, \ a new one appears", font_size=18, color=GREY_A),
            label(r"\textbf{write skew}: \ the doctors", font_size=18, color=GREY_A),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.12), col_alignments="ll").next_to(tab, DOWN, buff=0.4)
        ex.set_x(0)
        with self.voiceover(
            "SQL lets each transaction choose how much isolation it gets. <bookmark mark='a'/> Our database "
            "implements six levels, and we ran each of five classic anomalies against each, as a little program and "
            "an interleaving, and recorded whether the anomaly happened. <bookmark mark='b'/> A dirty read sees a "
            "write that is later rolled back. A non-repeatable read reads the same item twice and gets two values. "
            "A lost update we have seen. A phantom is a row that appears between two counts. Write skew is the "
            "doctors. <bookmark mark='c'/> Read uncommitted permits everything. Read committed, the default in "
            "PostgreSQL, Oracle and SQL Server, stops only dirty reads. Repeatable read, with locks on what was read, "
            "stops all but phantoms. Snapshot isolation stops phantoms but not write skew: the two weaker-than-"
            "serializable levels fail in different places, so neither is stronger than the other. "
            "<bookmark mark='d'/> And only the serializable levels, by locking or by SSI, stop all five."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.rule), *[FadeIn(r[0]) for r in tab.cells[1:]],
                      *[FadeIn(c) for c in tab.cells[0][1:]])
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            for r in tab.cells[1:5]:
                self.play(*[FadeIn(c) for c in r[1:]], run_time=0.5)
            vo.wait_until("d")
            for r in tab.cells[5:]:
                self.play(*[FadeIn(c) for c in r[1:]], run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    def definitions(self):
        head = label(r"What should a level \textit{mean}?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"ANSI SQL-92 defined the levels by the phenomena each forbids, \ in English", font_size=21,
                  color=WHITE),
            label(r"Berenson, \ Bernstein, \ Gray et al. \ (1995): \ the wording is ambiguous, \ and missing "
                  r"anomalies; \ snapshot isolation fits nowhere", font_size=21, color=NO),
            label(r"Adya \ (1999): \ define levels as forbidden \textbf{cycles} in a graph of read, \ write and "
                  r"anti-dependencies among \textit{committed} transactions", font_size=21, color=HEAD),
            label(r"\ \ G0: \ a cycle of write edges; \ G1: \ dirty and intermediate reads; \ G2: \ any cycle with "
                  r"an anti-dependency \ (write skew)", font_size=19, color=GREY_A),
            label(r"independent of locks or versions: \ a level is a property of the history, \ checkable after the "
                  r"fact", font_size=21, color=YES),
            label(r"Kingsbury and Alvaro's Elle \ (2020) \ checks real histories this way, \ and has found violations "
                  r"of the promised level in many production databases", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The standard's definitions turned out to be a problem. <bookmark mark='a'/> SQL-92 defined each level "
            "by the phenomena it forbids, described in English. <bookmark mark='b'/> In 1995 Hal Berenson, Phil "
            "Bernstein, Jim Gray and colleagues showed that the wording was ambiguous, that it missed anomalies such "
            "as lost updates and write skew, and that snapshot isolation, already shipping, fitted none of the levels. "
            "<bookmark mark='c'/> Atul Adya's thesis of 1999 put it right. Draw a graph whose nodes are committed "
            "transactions and whose edges are the dependencies between them: who read whose write, who overwrote "
            "whose, who overwrote what someone else had read. <bookmark mark='d'/> Each level forbids a kind of "
            "cycle. Serializable forbids them all; snapshot isolation allows a cycle with two consecutive "
            "anti-dependencies, which is write skew. <bookmark mark='e'/> These definitions do not mention locks or "
            "versions, so they apply to any implementation, and can be checked after the fact on what actually "
            "happened. <bookmark mark='f'/> That is exactly what the tool Elle does, and testing real databases with "
            "it has found many that do not deliver the level they promise."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, KERN, LAM)
