from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, COST, CTRL, DATA, FILE_COLORS, FUNC, HEAD, NO, PART, YES, box, code, load,
                                   memory_strip, region)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        mem = memory_strip([(r"code", 0.2, DATA), (r"data", 0.15, CTRL), (r"heap $\uparrow$", 0.25, YES), (r"", 0.15, BG),
                            (r"stack $\downarrow$", 0.25, NO)], w=1.6, total_h=2.2)
        frames = VGroup(*[region(2.4, 0.4, t, c, font_size=16) for t, c in (("main", GREY_B), ("lookup", DATA),
                                                                           ("alloc", CTRL))]).arrange(DOWN, buff=0)
        h = load("heap")["rows"]
        bars = VGroup(*[Rectangle(width=0.4, height=1.2 * r["fragmentation"], stroke_width=0, fill_color=c,
                                  fill_opacity=0.8) for r, c in zip(h, (DATA, CTRL, YES, FUNC, NO))]).arrange(
            RIGHT, buff=0.15, aligned_edge=DOWN)
        objs = VGroup(*[region(1.4, 0.5, n, c, font_size=16) for n, c in zip(("main.o", "table.o", "alloc.o", "io.o"),
                                                                             FILE_COLORS)]).arrange_in_grid(2, 2,
                                                                                                           buff=0.1)
        asl = code([r[0] for r in load("aslr")["runs"]], size=16)
        smash = VGroup(region(2.6, 0.5, r"buffer", DATA, font_size=16), region(2.6, 0.4, r"\texttt{ra}", NO,
                                                                             font_size=16)).arrange(UP, buff=0)
        tiles = Group(
            tile(mem, r"the address space", DATA),
            tile(frames, r"frames and conventions", CTRL),
            tile(bars, r"five allocators, \ one trace", YES),
            tile(objs, r"object files, \ linked", FUNC),
            tile(asl, r"randomized layout", HEAD),
            tile(smash, r"the stack smash", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ The Running Program", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            "We followed a program from source to a process. The diagrams connected byte layout and pointer "
            "arithmetic to branches, frames and calling conventions. Five simulated allocators replayed one "
            "recorded Perl trace. Knuth's balance argument matched that workload approximately, while an "
            "adversarial trace illustrated the worst-case question without proving a general theorem. Pebble "
            "gained a linker and loader; compiled host examples exposed object sections, dynamic references and "
            "virtual mappings. Finally, a toy stack overwrite showed how distinct defenses interrupt different "
            "parts of an attack."
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the compiler that writes this code", [13]),
            (r"garbage collection and moving heaps", [15]),
            (r"exceptions, \ signals, \ system calls", [31]),
            (r"pages, \ \texttt{mmap}, \ the TLB", [32]),
            (r"proving programs correct", [54]),
            (r"return-oriented programming, \ trusting trust", [55]),
        ], font_size=25)
        with self.voiceover(
            (
            "These mechanisms return throughout the course. Part 13 builds a compiler that emits structured calls "
            "and references. Part 15 builds runtime reclamation, including moving collectors whose assumptions "
            "differ from nonmoving allocation. Part 31 adds exceptional control flow, signals and system calls, "
            "and Part 32 connects virtual addresses to pages. Part 54 studies program and compiler correctness "
            "under explicit semantics. Part 55 studies code-reuse attacks and the trust placed in our tools."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"debugging", r"gdb and lldb: \ backtraces are the stack's frames"),
            (r"memory errors", r"AddressSanitizer, \ Valgrind, \ UBSan"),
            (r"builds", r"undefined references, \ duplicate symbols, \ link order, \ \texttt{-fPIC}"),
            (r"performance", r"allocator choice: \ jemalloc, \ tcmalloc, \ mimalloc"),
            (r"security", r"stack protectors, \ NX, \ ASLR, \ PIE, \ CFI: \ inspect actual build coverage"),
        ])
        with self.voiceover(
            (
            "In practice, inspect a backtrace with the build's symbols and unwinding information. Use sanitizers "
            "and memory-checking tools to find exercised classes of errors, while recognizing their "
            "instrumentation and coverage limits. Read linker diagnostics separately from compiler diagnostics: "
            "undefined references, duplicate symbols and archive ordering are concrete clues. Benchmark allocator "
            "choices on representative workloads before claiming a speedup. Check which stack, page, "
            "randomization and control-flow defenses your platform and build actually enable; defaults and "
            "coverage vary."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"On x86-64, \ how big is \texttt{struct \{ char a; double b; short c; char d; \}}? \ Reorder its fields "
            r"to make it as small as possible.",
            r"Write the prologue and epilogue of a Pebble function that calls another function and uses \texttt{s0} "
            r"and \texttt{s1}. \ How big is its frame?",
            r"A first-fit heap holds 1,000 blocks, \ and 80\% of allocations split their hole. \ About how many "
            r"holes are there?",
            r"Pebble's linker resolves \texttt{la t0, sym} with \texttt{sym} at \texttt{0x12345}. \ What do the "
            r"\texttt{lui} and \texttt{ori} immediates become?",
            r"\textit{Build.} \ Write first-fit \texttt{malloc} and \texttt{free} with boundary tags in Pebble "
            r"assembly, \ replay Perl's first 10,000 events on the emulator, \ and compare with \texttt{heap.py}.",
            '$\\bigstar$ \\textit{Research.} \\ State a nonmoving-allocation model, compare known bounds for first fit and best fit, and test small adversarial cases. What would require a proof?',
        ], font_size=22)
        with self.voiceover(
            (
            "The notes give six exercises and worked guidance. The fifth implements an allocator in Pebble "
            "assembly and compares a trace replay under identical header, alignment and splitting rules. The "
            "research exercise asks you to state a precise nonmoving-allocation model, locate the relevant upper "
            "and lower bounds, and explore small adversarial cases. A simulation can reveal a counterexample or "
            "motivate a conjecture; it cannot establish a universal worst-case theorem by itself."
        )
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 12, \ Languages and Automata", font_size=42).to_edge(UP, buff=0.6)
        sm = StateDiagram({"q0": (-3, 0), "q1": (0, 0), "q2": (3, 0)},
                          [("q0", "q1", "a", 0), ("q1", "q2", "b", 0), ("q2", "q2", "a,b", UP),
                           ("q1", "q1", "a", UP)], radius=0.45, accept=("q2",)).shift(DOWN * 0.2)
        q = label(r"how does a program read a program?", font_size=30, color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. To build Part 13's compiler we first need the theory of reading text: regular expressions, "
            "finite automata and grammars, and the parsers built from them. Part 12, Languages and Automata."
        ):
            self.play(FadeIn(nxt), FadeIn(sm))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bryant and O'Hallaron, \textit{Computer Systems: A Programmer's Perspective}, 3rd ed., ch. 3, 7, 9",
             r"Levine, \textit{Linkers and Loaders} (2000)",
             r"Knuth, \textit{The Art of Computer Programming}, vol. 1, \S 2.5",
             r"the System V ABI, \ x86-64 and RISC-V supplements"],
            [r"Knowlton, ``A fast storage allocator'' (1965)",
             r"Robson, ``An estimate of the store size necessary for dynamic storage allocation'' (1971)",
             r"Robson, ``Bounds for some functions concerning dynamic storage allocation'' (1974)",
             r"Wilson, Johnstone, Neely and Boles, ``Dynamic storage allocation: a survey'' (1995)",
             r"Johnstone and Wilson, ``The memory fragmentation problem: solved?'' (1998)",
             r"Aleph One, ``Smashing the stack for fun and profit'', Phrack 49 (1996)",
             r"Leroy, ``Formal verification of a realistic compiler'' (2009)",
             r"Memarian et al., ``Into the depths of C: elaborating the de facto standards'' (2016)",
             r"Watson et al., ``CHERI: a hybrid capability-system architecture'' (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
