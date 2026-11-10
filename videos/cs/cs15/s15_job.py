from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.measure()
        self.ledger()
        self.where()

    def card(self):
        card = chapter_card(14, r"The Job, \ collected", r"What does a runtime cost?", lit=(1995,),
                            extra=((1995, r"Java: \ bytecode and a collector for everyone"),), part=PART)
        with self.voiceover("Chapter fourteen. The Job, collected."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def measure(self):
        d = load("job")
        head = label(r"The Job on the Pebble VM, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["bytes"]), words(r["bytecodes"]), words(r["steps"]), str(r["gcs"]),
                 f"{100 * (1 - r['steps_nogc'] / r['steps']):.1f}\\%"] for r in d["rows"]]
        tab = grid_table([r"passage, \ bytes", r"bytecodes", r"Pebble instructions", r"collections",
                          'GC instruction share'], rows, widths=[2.4, 2.4, 3.2, 2.2, 2.6], row_h=0.46, font_size=19,
                         colors=[[WHITE, WHITE, COST, WHITE, YES]] * len(rows)).next_to(head, DOWN, buff=0.45)
        pts = VGroup(
            label(r"the same six passages as rows 3 and 5; \ every output checked against the reference",
                  font_size=20, color=GREY_B),
            label(r"the collector's share: \ rerun with a heap too big ever to fill, \ and compare", font_size=20,
                  color=GREY_A),
            label(rf"on Part 8's out-of-order core the VM runs at {d['ipc']:.2f} instructions per cycle \ "
                  rf"({words(d['ipc_sample']['instructions'])} instructions measured)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.13).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            (
            "Now price the complete Job on the Pebble VM. <bookmark mark='a'/> Each row is an actual passage "
            "executed by the emulator, with output checked against the reference. Instructions, allocations and "
            "copied words are exact for these executions. <bookmark mark='b'/> The no-collection comparison uses "
            "a large enough heap for the same passage. Subtracting instruction counts estimates collector "
            "instruction overhead, not the same fraction of elapsed time or out-of-order cycles. <bookmark "
            "mark='c'/> Cycles for larger projections use IPC from a smaller core sample. Keep measured emulator "
            "counts, sampled IPC and projected whole-corpus time distinct; none is a direct timing of thirty "
            "complete novels."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]], FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:4])) for r in tab.cells[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(*[FadeIn(r[4]) for r in tab.cells[1:]], FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        head = label('Ledger row 6: projection', font_size=38).to_edge(UP, buff=0.35)
        rows = led + [{"part": p_, "label": t} for p_, t in ((16, r"sort, then count"), (17, r"a hash table"))]
        tab = ledger_table(rows, shown=7, highlight=(6,), font_size=21, row_h=0.42, label_width=4.8).move_to(
            DOWN * 0.3)
        r6, r5 = led[6], led[5]
        res = VGroup(
            label(rf"the $\lambda$-core on the Pebble VM: \ {human_time(r6['seconds'])} \ against "
                  rf"{human_time(r5['seconds'])} compiled", font_size=23, color=COST),
            label(rf"projected runtime ratio: {r6['ratio_to_row5']:.0f}$\times$; \ GC instruction share: \ "
                  rf"{100 * r6['gc_share']:.1f}\%", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Row six adds a collected language runtime to our ledger. <bookmark mark='a'/> The hours and ratios "
            "are projections from the sampled passages and the stated core-pricing method. They are not a "
            "stopwatch measurement of the full corpus. <bookmark mark='b'/> The gap combines interpreter "
            "dispatch, data representation, algorithm choice and collection. It is a useful explanation target, "
            "but it cannot be attributed entirely to one mechanism or promised away by a JIT."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), Indicate(tab.rows[6], color=COST))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    def where(self):
        d = load("job")
        tot_b = sum(r["bytes"] for r in d["rows"])
        bc = sum(r["bytecodes"] for r in d["rows"]) / tot_b
        wd = sum(r["words"] for r in d["rows"]) / tot_b
        hand = sum(r["hand_instr"] for r in d["rows"]) / tot_b
        head = label('Where the model counts go', font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"for every byte of text", r"hand-written \ (row 3)", r"the $\lambda$-core VM \ (row 6)"], [
            [r"Pebble instructions", f"{hand:.0f}", words(round(bc * d["per_bytecode"]))],
            [r"bytecodes", r"---", f"{bc:.0f}"],
            [r"Pebble instructions per bytecode", r"---", f"{d['per_bytecode']:.0f}"],
            [r"heap words allocated", "0", f"{wd:.0f}"],
        ], widths=[5.0, 3.2, 3.8], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, YES, NO], [WHITE, GREY_B, WHITE], [WHITE, GREY_B, NO], [WHITE, YES, COST]]).next_to(
            head, DOWN, buff=0.5)
        pts = VGroup(
            label('dispatch: about 48 Pebble instructions per bytecode in this sample', font_size=20, color=GREY_A),
            label('representation: linked characters and association entries add heap work', font_size=20, color=GREY_A),
            label('collection: instruction-count delta, not elapsed-time share', font_size=20,
                  color=YES),
            label(r"the runtime is not the bottleneck forever: \ Part 16 changes the \textit{algorithm}",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Where does the VM's extra work go? <bookmark mark='a'/> Dispatch interprets each bytecode using "
            "several Pebble instructions, and tagged heap structures add representation work. <bookmark "
            "mark='b'/> The underlying word-counting algorithm still scans an association list; the runtime has "
            "not removed its quadratic growth. <bookmark mark='c'/> The collector's displayed share is an "
            "instruction-count difference against a no-collection run. It is not automatically its fraction of "
            "cycles or elapsed time. <bookmark mark='d'/> A faster collector can save only the work attributable "
            "to collection under that model. Part sixteen changes the algorithm itself, a different source of "
            "improvement."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
