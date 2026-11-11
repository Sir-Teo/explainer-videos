from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (HEAD, KERN, LAM, NO, PART, YES, code, fit_right, grid_table, load)

HANDLER = [
    "pfault: csrr s0, tval        # the faulting address",
    "        lw   t1, LO(t0)",
    "        bltu s0, t1, segv",
    "        lw   t1, HI(t0)",
    "        bgeu s0, t1, segv    # outside its memory",
    "        ...                  # find its L2 entry",
    "        bnez t2, segv        # mapped: a protection fault",
    "        lw   s2, nextframe(zero)",
    "        ...                  # take a frame",
    "pz:     sw   zero, 0(t2)     # zero it",
    "        ...",
    "        sw   t2, 0(s1)       # map it",
    "        j    resume          # run the instruction again",
]


class PebbleVM(VoiceoverScene):
    def construct(self):
        self.card()
        self.kernel()
        self.space()
        self.four()
        self.pipeline()

    def card(self):
        card = chapter_card(14, r"PebbleOS gains virtual memory", r"What did our kernel need?", lit=(),
                            extra=(), part=PART)
        with self.voiceover("Chapter fourteen. PebbleOS gains virtual memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kernel(self):
        d = load("pebblevm")
        head = label(r"What changed in the kernel", font_size=36).to_edge(UP, buff=0.3)
        src = code(HANDLER, size=14)
        box = SurroundingRectangle(src, color=GREY_D, buff=0.18, corner_radius=0.08)
        sg = VGroup(box, src).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        items = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"the MMU \ (\texttt{mmu.py}): \ a two-level walk, \\ a 16-entry TLB, \ faults 12, 13, 15", LAM),
            (r"the boot loader builds a table per process: \\ the kernel's superpage, \ code R+X, \ data R+W", WHITE),
            (r"a switch loads and writes \texttt{ptbr}: \\ two instructions, \ and the TLB is flushed", HEAD),
            (r"a fault inside the process's range: \\ a zeroed frame, \ mapped, \ retried", YES),
            (r"anything else: \ killed, \ exactly as in Part 31", NO),
            (rf"kernel: \ {d['kernel']} instructions \ $\rightarrow$ \ {d['kernel_vm']}", KERN),
        )]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(sg, RIGHT, buff=0.4).align_to(sg, UP)
        fit_right(items)
        with self.voiceover(
            "Our own machine has had all of this since chapter three. Here is what it took. <bookmark mark='a'/> The "
            "hardware: a memory-management unit for Pebble, with the two-level walk, a sixteen-entry TLB, and three "
            "new kinds of fault. <bookmark mark='b'/> The boot loader builds one page table per process, with the "
            "kernel's superpage in entry zero, the code pages readable and executable, and the data pages readable "
            "and writable. <bookmark mark='c'/> The context switch gains two instructions, to load and write the page-table "
            "base register, which also flushes the TLB. <bookmark mark='d'/> And the trap handler gains this: a page "
            "fault at an address inside the process's range, on a page not yet mapped, gets a fresh frame, zeroed, "
            "mapped, and the instruction runs again. <bookmark mark='e'/> Any other fault kills the process, as it "
            "did in Part 31. <bookmark mark='f'/> In all, forty-six instructions: the kernel grew from two hundred and "
            "eighty-four to three hundred and thirty."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                if mk == "d":
                    self.play(Create(box), FadeIn(src), FadeIn(it), run_time=1.2)
                else:
                    self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def space(self):
        d = load("sameva")
        w = d["walks"][0]
        head = label(r"One process's address space, \ page by page", font_size=34).to_edge(UP, buff=0.3)
        what = {0x400000: r"library code: \ \texttt{\_start}, \ \texttt{getc}, \ \texttt{putc}",
                0x401000: r"the input buffer", 0x402000: r"input's end; \ the output buffer begins",
                0x403000: r"the rest of the output buffer",
                0x404000: r"the program's code", 0x405000: r"its data: \ \texttt{cell}",
                0x4ff000: r"the top of the stack"}

        def flags(f):
            return " ".join(n for n, b in (("R", 2), ("W", 4), ("X", 8), ("U", 16), ("A", 64), ("D", 128)) if f & b)
        rows = []
        prev = None
        for va, pa, f in w["maps"]:
            if prev is not None and va - prev > 0x1000:
                rows.append([r"\textit{...}", r"--", r"--", rf"{(va - prev) // 0x1000 - 1} pages never mapped"])
            rows.append([rf"\texttt{{{va:#x}}}", rf"\texttt{{{pa:#x}}}", rf"\texttt{{{flags(f)}}}", what.get(va, "")])
            prev = va
        tab = grid_table([r"virtual page", r"frame", r"bits", r"what it holds"], rows,
                         widths=[2.4, 2.2, 2.6, 5.4], row_h=0.44, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        gap = next(i for i, r in enumerate(rows) if "never" in r[3]) + 1
        for c in tab.cells[gap]:
            c.set_color(GREY_B)
        n = len(w["maps"])
        lines = VGroup(
            label(r"code: \ R X, \ never W; \ data: \ R W, \ never X; \ all U; \ A and D set by the hardware as it ran",
                  font_size=21, color=WHITE),
            label(rf"{n} of 256 pages mapped: \ {4 * n} KiB of frames for a 1 MiB address space", font_size=21,
                  color=YES),
            label(r"the stack sits at the top, \ 1 MiB away, \ and the gap costs nothing: \ room to grow", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the whole page table of the hook's first process, read out of our machine. <bookmark mark='a'/> "
            "The library's code, then three pages of buffers for input and output, then the program's own code, and "
            "its data page, holding the cell from the hook. <bookmark mark='b'/> Then two hundred and forty-nine "
            "pages that were never mapped, and at the very top, the stack. <bookmark mark='c'/> The bits tell the "
            "story. Code is readable and executable, never writable; data is writable, never executable; every page "
            "is marked for user mode; and the hardware has set accessed and dirty as the program ran. The output "
            "buffer is dirty because the program printed. <bookmark mark='d'/> Seven pages of the two hundred and "
            "fifty-six are mapped: twenty-eight kibibytes of memory for a one-mebibyte address space. <bookmark "
            "mark='e'/> And the stack sits a whole mebibyte above the code, with nothing in between to pay for: room "
            "for both to grow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:gap]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[gap:]], lag_ratio=0.4))
            for mk, ln in zip("cde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def four(self):
        p = load("protect")
        head = label(r"Four processes, \ one machine", font_size=36).to_edge(UP, buff=0.3)
        pr = {q["name"]: q for q in p["procs"]}
        what = {"good": r"prints eight A's", "codewrite": r"stores to its own code",
                "wild": r"loads from \texttt{0x600000}", "grower": r"touches 16 new heap pages, \ prints G"}
        res = {"good": r"exit 0", "codewrite": rf"killed: \ cause 15, \ exit {pr['codewrite']['exit']}",
               "wild": rf"killed: \ cause 13, \ exit {pr['wild']['exit']}",
               "grower": rf"exit 0, \ after {p['page_faults']} page faults"}
        cols = {"good": YES, "codewrite": NO, "wild": NO, "grower": HEAD}
        tab = grid_table([r"process", r"what it does", r"what happened"],
                         [[rf"\texttt{{{n}}}", what[n], res[n]] for n in ("good", "codewrite", "wild", "grower")],
                         widths=[2.6, 4.8, 4.8], row_h=0.58, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for i, n in enumerate(("good", "codewrite", "wild", "grower")):
            tab.cells[i + 1][2].set_color(cols[n])
        out = label(rf"the console: \ \texttt{{{p['output'].strip()}}}", font_size=24, color=YES).next_to(tab, DOWN,
                                                                                                          buff=0.45)
        lines = VGroup(
            label(r"a write to code: \ mapped, \ but not writable; \ a wild load: \ outside the process altogether",
                  font_size=20, color=WHITE),
            label(r"each death is the kernel's decision: \ the hardware only reports, \ and the others never notice",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now four processes on one machine. <bookmark mark='a'/> One prints eight letters A. <bookmark mark='b'/> "
            "One stores a zero over its own first instruction. Its code page is mapped, but not writable: a store "
            "fault, cause fifteen, and the kernel kills it. <bookmark mark='c'/> One loads from an address beyond its "
            "memory: a load fault, cause thirteen, killed. <bookmark mark='d'/> And one walks up its heap, touching "
            "sixteen new pages. It takes sixteen page faults, each served with a zeroed frame, and prints a G. "
            "<bookmark mark='e'/> The console shows only the survivors' output. <bookmark mark='f'/> A write to code "
            "is a protection fault; a wild load is outside the process altogether. <bookmark mark='g'/> In both cases "
            "the hardware only reports, the kernel decides, and the other processes never notice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("e")
            self.play(FadeIn(out))
            for mk, ln in zip("fg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def pipeline(self):
        d = load("pebblevm")
        head = label(r"The Job's pipeline, \ paged", font_size=36).to_edge(UP, buff=0.3)
        L, E = d["lazy"], d["eager"]
        f = lambda v: f"{v:,}".replace(",", "{,}")
        tab = grid_table([r"", r"instructions", r"page faults", r"frames used"], [
            [r"Part 31: \ no paging", f(d["native_steps"]), r"--", r"--"],
            [r"paged, \ everything mapped at boot", f(E["steps"]), f(E["page_faults"]), f(E["frames"])],
            [r"paged, \ zero pages on demand", f(L["steps"]), f(L["page_faults"]), f(L["frames"])],
        ], widths=[5.2, 2.4, 2.2, 2.2], row_h=0.58, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        extra = E["steps"] - d["native_steps"]
        per = (L["steps"] - E["steps"]) / max(1, L["page_faults"])
        lines = VGroup(
            label(rf"the output: \ byte for byte the same, \ {f(d['bytes'])} bytes of text in", font_size=21,
                  color=YES),
            label(rf"translation itself costs \textbf{{{extra}}} instructions: \ \texttt{{ptbr}} loaded and written at "
                  rf"each switch; \ the TLB hides the rest", font_size=21, color=WHITE),
            label(rf"each demand fault costs about {per:,.0f} instructions, \ nearly all zeroing 4 KiB".replace(
                ",", "{,}"), font_size=21, color=HEAD),
            label(rf"but the Job's 1 MiB of address space needs {L['frames']} frames, \ not {E['frames']}: \ most of "
                  rf"its table is never touched", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Finally, the pipeline that has run through this series: the tokenizer feeding the Job, as two processes, "
            "now each in its own address space. <bookmark mark='a'/> Without paging, Part 31's kernel ran it in five "
            "hundred and fifty-eight thousand instructions. <bookmark mark='b'/> Paged, with every page mapped at "
            "boot, it takes just twelve more. <bookmark mark='c'/> Paged with zero pages on demand, it takes seven "
            "page faults and twenty-two thousand more instructions. <bookmark mark='d'/> The output is identical, "
            "byte for byte. <bookmark mark='e'/> So translation itself is almost free: two instructions for the table "
            "register at each switch, and the TLB hides the rest. <bookmark mark='f'/> A demand fault costs about three "
            "thousand instructions, nearly all of them zeroing. <bookmark mark='g'/> What demand paging buys is "
            "memory: the two processes need twenty-four frames instead of a hundred and forty-six, because most of "
            "the Job's hash table is never touched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abc", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            for mk, ln in zip("defg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
