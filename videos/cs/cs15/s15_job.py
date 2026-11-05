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
                          r"in the collector"], rows, widths=[2.4, 2.4, 3.2, 2.2, 2.6], row_h=0.46, font_size=19,
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
            "Now the Job, in the lambda core, on our own runtime, on our own machine. <bookmark mark='a'/> We ran "
            "the Pebble VM on the same six passages that priced rows three and five, and checked every output. "
            "A passage of twenty-four hundred bytes takes one point two million bytecodes, and sixty million Pebble "
            "instructions. <bookmark mark='b'/> How much of that is the garbage collector? We ran everything again "
            "with a heap so large that it never fills, and compared. The collector accounts for between one and "
            "five percent. <bookmark mark='c'/> Finally, the VM's own code ran on Part 8's out-of-order core, at "
            "about two instructions per cycle, which turns instructions into time."
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
        head = label(r"Ledger row 6", font_size=38).to_edge(UP, buff=0.35)
        rows = led + [{"part": p_, "label": t} for p_, t in ((16, r"sort, then count"), (17, r"a hash table"))]
        tab = ledger_table(rows, shown=7, highlight=(6,), font_size=21, row_h=0.42, label_width=4.8).move_to(
            DOWN * 0.3)
        r6, r5 = led[6], led[5]
        res = VGroup(
            label(rf"the $\lambda$-core on the Pebble VM: \ {human_time(r6['seconds'])} \ against "
                  rf"{human_time(r5['seconds'])} compiled", font_size=23, color=COST),
            label(rf"{r6['ratio_to_row5']:.0f}$\times$ slower; \ the garbage collector's part of it: \ "
                  rf"{100 * r6['gc_share']:.1f}\%", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger gets its seventh row, row six. <bookmark mark='a'/> The Job in the lambda core, "
            "interpreted by our VM and collected by Cheney's algorithm, would take about two and a half hours on "
            "the thirty novels, against fifty-eight seconds for the same algorithm compiled from the Pebble "
            "language. A hundred and fifty times slower. <bookmark mark='b'/> And the garbage collector, which "
            "this half of the part has been about, is under four percent of it. Collection is not the expense."
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
        head = label(r"Where the time goes", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"for every byte of text", r"hand-written \ (row 3)", r"the $\lambda$-core VM \ (row 6)"], [
            [r"Pebble instructions", f"{hand:.0f}", words(round(bc * d["per_bytecode"]))],
            [r"bytecodes", r"---", f"{bc:.0f}"],
            [r"Pebble instructions per bytecode", r"---", f"{d['per_bytecode']:.0f}"],
            [r"heap words allocated", "0", f"{wd:.0f}"],
        ], widths=[5.0, 3.2, 3.8], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, YES, NO], [WHITE, GREY_B, WHITE], [WHITE, GREY_B, NO], [WHITE, YES, COST]]).next_to(
            head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"\textbf{dispatch}: \ 48 instructions to run one bytecode, \ most of them deciding which: \ a "
                  r"JIT removes it \ (chapter 11)", font_size=20, color=GREY_A),
            label(r"\textbf{representation}: \ every character is a 3-word list cell, \ every count a boxed pair: \ "
                  r"arrays and unboxed integers remove it", font_size=20, color=GREY_A),
            label(r"\textbf{collection}: \ under 4\%, \ because almost everything dies young", font_size=20,
                  color=YES),
            label(r"the runtime is not the bottleneck forever: \ Part 16 changes the \textit{algorithm}",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where does a factor of a hundred and fifty come from? Per byte of text, the hand-written Job of Part 6 "
            "runs a hundred and thirty-nine instructions. <bookmark mark='a'/> The lambda core runs four hundred "
            "and fifty-nine bytecodes, and each costs forty-eight Pebble instructions, most of them spent deciding "
            "which instruction it is. That is dispatch, and it is what a just-in-time compiler eliminates. "
            "<bookmark mark='b'/> The rest is representation. Every character of the text becomes a three-word "
            "list cell, and every count a pair on the heap: sixty-two words allocated for every byte read. Arrays "
            "and unboxed integers remove that. <bookmark mark='c'/> The collector itself costs under four percent, "
            "because almost everything it would have to copy has already died. <bookmark mark='d'/> And all of "
            "this still uses the same slow algorithm, a list searched from the front for every word. Part 16 stops "
            "tuning the machine and changes the algorithm."
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
