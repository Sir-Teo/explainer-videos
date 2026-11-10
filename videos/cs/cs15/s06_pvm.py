from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.runtime import pvm as PV
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, words)


def _excerpt():
    src = PV.source().splitlines()
    k = next(i for i, l in enumerate(src) if l.strip().startswith("while 1 {") and "op = opv" in src[i + 1])
    body = src[k:k + 16]
    cons = next(i for i, l in enumerate(src) if l.rstrip().endswith("// CONS"))
    return [l[4:] for l in body], [l[4:] for l in src[cons:cons + 4]]


class PebbleVM(VoiceoverScene):
    def construct(self):
        self.card()
        self.source()
        self.cosim()
        self.dispatch()

    def card(self):
        card = chapter_card(5, r"The VM, \ on Pebble", r"Can our machine run our language?", lit=(1957,),
                            extra=((1957, r"FORTRAN"),), part=PART)
        with self.voiceover("Chapter five. The VM, on Pebble."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def source(self):
        loop, cons = _excerpt()
        head = label(r"A virtual machine, \ in the Pebble language", font_size=34).to_edge(UP, buff=0.3)
        c1 = code(loop, size=14, color=CODE)
        c2 = code(cons, size=14, color=DATA)
        l1 = label(r"the dispatch loop: \ fetch, \ then a chain of tests", font_size=19, color=GREY_B)
        l2 = label(r"\texttt{CONS}: \ collect if the heap is full, \ then build a cell", font_size=19,
                   color=GREY_B)
        blk = VGroup(l1, c1, l2, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(LEFT, buff=0.4).shift(
            DOWN * 0.15)
        if blk.height > 6.3:
            blk.scale_to_fit_height(6.3)
        pts = VGroup(
            label(r"compiled by Part 13's compiler, \ \texttt{-O2}", font_size=20, color=GREY_A),
            label(r"the loader reads the bytecode with \texttt{getc}, \ then the VM reads the text", font_size=20,
                  color=GREY_A),
            label(r"a stack, \ two semispaces of heap, \ and Cheney's collector: \ all in Pebble's 1 MiB",
                  font_size=20, color=YES),
            label(r"the Pebble language has no \texttt{switch} and no shifts: \ tags come apart with \texttt{/} and "
                  r"\texttt{\%}", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        if pts.width > 6.2:
            pts.scale_to_fit_width(6.2)
        with self.voiceover("A virtual machine is just a program, and we have a machine and a compiler of our own. So we wrote the virtual machine in the Pebble language of Part 13, compiled it, and ran it on Pebble. <bookmark mark='a'/> Its heart is this loop. Fetch the opcode and its argument, then test the opcode against each instruction in turn, and run the matching handler. <bookmark mark='b'/> Here is the handler for CONS: if the heap is full, collect; then write a header and two fields, and push a pointer. <bookmark mark='c'/> A loader at the start reads the compiled Job, byte by byte, and then the VM reads the text. The stack, a heap of two halves, and the collector all fit in Pebble's one megabyte of memory. <bookmark mark='d'/> The Pebble language has no switch statement and no bit shifts, so dispatch is a chain of ifs, and a tag is taken apart with division and remainder. Both turn out to matter.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(l1), FadeIn(c1), FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(l2), FadeIn(c2))
            vo.wait_until('c')
            self.play(FadeIn(pts[1:3]))
            vo.wait_until('d')
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def cosim(self):
        d = load("vm")
        r = d["orders"][0]
        head = label(r"Two machines, \ one behaviour", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"the Job on a passage", r"Python VM", r"Pebble VM, \ on the emulator"], [
            [r"output", r"the 20 words", r"the same 20 words"],
            [r"bytecodes executed", words(d["ops"]), words(d["ops"])],
            [r"collections", str(r["gcs"]), str(r["gcs"])],
            [r"words copied by the collector", words(r["copied"]), words(r["copied"])],
            [r"deepest stack, words", words(r["maxsp"]), words(r["maxsp"])],
            [r"Pebble instructions", r"---", words(r["steps"])],
        ], widths=[4.6, 3.0, 4.2], row_h=0.52, font_size=21, mono_cols=(),
            colors=[[WHITE, YES, YES]] * 5 + [[WHITE, GREY_B, COST]]).next_to(head, DOWN, buff=0.5)
        res = VGroup(
            label(rf"{r['per_bytecode']:.0f} Pebble instructions per bytecode", font_size=26, color=COST),
            label('finite in-range cosimulation: checked output and counters, not a universal proof',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Two implementations give us an opportunity to cross-check. <bookmark mark='a'/> Run the same "
            "in-range Job passage on the Python reference VM and the Pebble implementation. Their output, "
            "bytecode work, collection counts, copied words and deepest stack are checked as shown. <bookmark "
            "mark='b'/> This is finite cosimulation evidence for these programs and heap settings. It is not a "
            "proof of equivalence for every possible program, especially values beyond Pebble's tagged integer "
            "range. A mismatch would still be valuable: it would identify a concrete counterexample to "
            "investigate."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:6]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[6])), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def dispatch(self):
        d = load("vm")
        head = label(r"The price of dispatch", font_size=34).to_edge(UP, buff=0.3)
        rows = [[o["order"], words(o["steps"]), f"{o['per_bytecode']:.0f}"] for o in d["orders"]]
        tab = grid_table([r"the chain of \texttt{if}s, \ tested", r"Pebble instructions", r"per bytecode"], rows,
                         widths=[4.6, 3.4, 2.4], row_h=0.52, font_size=21, mono_cols=(),
                         colors=[[YES, WHITE, YES], [WHITE, WHITE, WHITE], [NO, WHITE, NO]]).next_to(
            head, DOWN, buff=0.5)
        cd = d["c_dispatch"]
        ns_s, ns_t = 1e9 * cd["switch"] / cd["bytecodes"], 1e9 * cd["threaded"] / cd["bytecodes"]
        c = VGroup(
            label(r"in C, \ on this machine: \ a tiny VM, \ 300 million bytecodes", font_size=21, color=GREY_B),
            label(rf"\texttt{{switch}}: \ {ns_s:.2f} ns per bytecode; \ \textbf{{threaded code}} \ "
                  rf"(\texttt{{goto *label[op]}}): \ {ns_t:.2f} ns", font_size=22, color=DATA),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.5)
        pts = VGroup(
            label(r"threaded code gives every handler its own indirect jump, \ and the branch predictor its own "
                  r"history \ (Bell, \ 1973; \ Ertl and Gregg, \ 2003)", font_size=19, color=GREY_A),
            label(r"modern predictors have narrowed the gap \ (Rohou et al., \ 2015): \ measure, \ do not trust "
                  r"folklore", font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Dispatch order changes the work of our Pebble interpreter. <bookmark mark='a'/> With its chain of "
            "tests, the same passage executes about forty-seven instructions per bytecode when frequent opcodes "
            "come first, sixty in opcode order, and a hundred in the reversed frequency order. These are "
            "instruction counts, not measured elapsed-time ratios. <bookmark mark='b'/> Our separate C experiment "
            "compares a switch with computed-goto threading. Its current timings are displayed; they belong to "
            "this tiny loop, compiler and host. <bookmark mark='c'/> A per-handler indirect branch can expose "
            "different prediction history, but modern predictors, compiler transformations and workload structure "
            "affect the result. Measure the generated implementation before applying an old performance rule."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c_) for c_ in tab.cells[0]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(c))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
