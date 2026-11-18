from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono, region)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.employment()
        self.superopt()
        self.egraph()
        self.open()

    def card(self):
        self.chapter(15, r"Frontier: \ searching for the best program", r"Can a machine find the optimal "
                            r"code?", lit=(1987, 2009), extra=((1987, r"Massalin's superoptimizer"),
                                                               (2009, r"equality saturation")), part=PART, said="Chapter fifteen. Frontier: searching for the best program.")

    def employment(self):
        self.wrong_idea(r"An optimizing compiler produces \\ the best possible code",
                        r"It applies rules that usually help. \\ The best program is undecidable in general",
                        narration="It's easy to believe that an optimizing compiler produces the best possible code.",
                        right_narration="It doesn't, and in general it can't: finding the best equivalent program is undecidable. "
                                        "It applies rules that usually help.")
        self.clear_scene()
        head = label(r"``Optimizing'' compilers do not optimize", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"they apply rules that usually help; \ nothing says the result is the best", font_size=22,
                  color=GREY_A),
            label("exact semantic questions can be undecidable in an unbounded language", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.5)
        loop = VGroup(code(["simulate M silently;", "print(1);"], size=22, color=DATA),
                      MathTex(r"\stackrel{?}{\equiv}", font_size=36, color=HEAD),
                      code(["loop:  j loop"], size=22, color=YES)).arrange(
                          RIGHT, buff=0.65).next_to(pts, DOWN, buff=0.45)
        why = VGroup(
            label(r"unbounded semantics: the left program prints if and only if $M$ halts", font_size=21, color=GREY_A),
            label(r"equivalent to the silent loop if and only if $M$ never halts", font_size=21, color=GREY_A),
            label(r"an exact equivalence decider would decide halting (Part 25)", font_size=22, color=NO),
            label(r"``the full employment theorem for compiler writers''", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(loop, DOWN, buff=0.4)
        with self.voiceover("An optimizing compiler usually improves a program according to selected costs; it does not promise the best equivalent program. <bookmark mark='a'/> Even deciding whether a particular replacement is legal can be impossible in a general language with unbounded computation. <bookmark mark='b'/> Consider a program that simulates an arbitrary machine M and prints a character if M halts. A silent infinite loop has the same observable behavior precisely when M never halts. <bookmark mark='c'/> An always-correct decision procedure for that equivalence would decide halting. This argument needs the unbounded semantic model; a fixed finite-memory Pebble machine has a finite state space, even if exhaustive analysis is impractical. It also does not assume an optimizer chooses one canonical spelling among equally short programs. <bookmark mark='d'/> Appel's full-employment theme is that compiler improvement keeps confronting such limits. For small restricted instruction fragments, however, candidate search and proof can still be useful.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[1]), FadeIn(loop), FadeIn(why[0]))
            vo.wait_until('c')
            self.play(FadeIn(why[1:3]))
            vo.wait_until('d')
            self.play(FadeIn(why[3]))
        self.wait(0.3)
        self.clear_scene()

    def superopt(self):
        self.ask(r"The shortest program for a small function: \\ can a computer find it?", [r"no",
                 r"yes, for very short ones"], 1,
                 say="Can a computer find the shortest program that computes a small function?",
                 reveal="Yes, for very short ones, by searching; the cost explodes with the length.")
        so = load("superopt")
        head = label("Superoptimization: search candidates, then prove them", font_size=32).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ enumerate Pebble sequences of length 1, 2, 3, ...", font_size=20, color=GREY_A),
            label("2. \\ filter on a fixed finite test set; observation pruning is incomplete", font_size=20,
                  color=GREY_A),
            label(r"3. \ prove the survivors with z3, \ for all $2^{32}$ inputs", font_size=20, color=GREY_A),
            label(r"Massalin, \ 1987: \ found tricks no human had", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        rows, cols = [], []
        for t in so["targets"]:
            rows.append([t["name"], str(t["length"]), "; ".join(" ".join(x.split()) for x in t["program"]),
                         f"{t['seconds']:.2f} s"])
            cols.append([WHITE, YES, WHITE, GREY_B])
        tab = grid_table([r"target", r"length", "found Pebble candidate (SMT-proved)", r"search + SMT"], rows,
                         widths=[2.3, 1.1, 7.4, 1.4], row_h=0.42, font_size=17, colors=cols,
                         mono_cols=(0, 2)).next_to(steps, DOWN, buff=0.35).set_x(0)
        absrow = [k for k, t in enumerate(so["targets"]) if t["name"] == "|x|"][0]
        explain = label("$|x|$: \\ $(x+(x\\gg31))\\oplus(x\\gg31)$; \\ wraps at $x=-2^{31}$", font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover("Massalin's 1987 superoptimizer searched small instruction sequences. Our demonstration borrows that idea, with an important limit. <bookmark mark='a'/> It searches increasing candidate lengths over selected register operations, immediate forms and available values. Finite test inputs reject many candidates quickly. <bookmark mark='b'/> A separate z3 check asks whether each survivor equals its specification for every encoded thirty-two-bit input. That proof concerns the arithmetic fragment and specified output, not memory, calling conventions or an entire compiler. <bookmark mark='c'/> The table shows short sequences whose equivalence checks succeeded. Our pruning merges prefixes that agree only on finite tests, so the search can miss useful alternatives. The first found length is not a certificate of global shortestness, even though an accepted equivalence proof is meaningful. <bookmark mark='d'/> The absolute-value sequence uses arithmetic sign shift, addition and exclusive-or. At the most negative signed word, the mathematical positive answer is unrepresentable; the specification returns the wrapped word. Signed division by two instead needs rounding toward zero. The min sequence is checked against signed comparison, including extreme inputs.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(steps[:2]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(steps[2:]))
            vo.wait_until('c')
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            for r in tab.cells[1:5]:
                self.play(*[FadeIn(c) for c in r], run_time=0.5)
            vo.wait_until('d')
            for r in tab.cells[5:]:
                self.play(*[FadeIn(c) for c in r], run_time=0.5)
            self.play(Indicate(VGroup(*tab.cells[absrow + 1]), color=HEAD), FadeIn(explain))
        self.wait(0.3)
        self.clear_scene()



    def eclass(self, items, color, title=None):
        t = VGroup(*[mono(s, 17, WHITE) for s in items]).arrange(DOWN, buff=0.14)
        box = DashedVMobject(RoundedRectangle(width=t.width + 0.5, height=t.height + 0.4, corner_radius=0.15,
                                              stroke_color=color, stroke_width=2), num_dashes=40)
        box.move_to(t)
        g = VGroup(box, t)
        if title:
            g.add(mono(title, 15, color).next_to(box, UP, buff=0.05).align_to(box, LEFT))
        g.items = t
        return g

    def egraph(self):
        head = label("Equality saturation: retain equivalent alternatives", font_size=32).to_edge(UP, buff=0.3)
        start = mono("(a * 2) * 2", 24, CODE).next_to(head, DOWN, buff=0.35)
        rules = VGroup(*[mono(r, 15, GREY_A) for r in ("x * 2  →  x << 1", "(x * y) * z  →  x * (y * z)",
                                                       "2 * 2  →  4", "x * 4  →  x << 2")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        rl = label(r"rewrite rules \ (all true mod $2^{32}$)", font_size=16, color=GREY_B).next_to(rules, UP,
                                                                                               buff=0.08)
        greedy = VGroup(label(r"one rule at a time:", font_size=19, color=NO),
                        mono("(a << 1) * 2  →  (a << 1) << 1", 16, NO),
                        label(r"two shifts, \ and associativity no longer applies", font_size=17, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(LEFT, buff=0.5).shift(UP * 1.0)
        c1 = self.eclass(["a * 2", "a << 1"], CTRL, "c1")
        c4 = self.eclass(["2 * 2", "4"], CTRL, "c4")
        root = self.eclass(["c1 * 2", "c1 << 1", "a * c4", "a << 2"], YES, "root")
        root.move_to(UP * 0.0 + RIGHT * 0.6)
        c1.move_to(DOWN * 2.3 + LEFT * 1.4)
        c4.move_to(DOWN * 2.3 + RIGHT * 2.6)
        ar = VGroup(
            Arrow(root.items[0].get_left(), c1[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6, tip_length=0.12),
            Arrow(root.items[1].get_left(), c1[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6, tip_length=0.12),
            Arrow(root.items[2].get_right(), c4[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6,
                  tip_length=0.12),
        )
        best = SurroundingRectangle(root.items[3], color=HEAD, buff=0.06)
        notes = VGroup(
            label(r"an \textbf{e-graph}: \ each dashed class holds expressions known to be equal", font_size=19,
                  color=GREY_A),
            label("apply sound rules subject to resource limits; extract under a stated cost model",
                  font_size=19, color=GREY_A),
            label("retained alternatives reduce commitment to an early rewrite order", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.2).to_edge(RIGHT, buff=0.3)
        for n in notes:
            if n.width > 6.0:
                n.width = 6.0
        with self.voiceover(
            (
            "Equality saturation keeps alternatives instead of committing to the first rewrite. <bookmark "
            "mark='a'/> In this example, a times two times two uses rules valid for our wrapping thirty-two-bit "
            "words. Other integer and floating-point semantics require their own rules. <bookmark mark='b'/> A "
            "one-way pass might turn the inner multiply into a shift before a multiplication-combining rule sees "
            "it. That illustrates a phase-ordering choice. <bookmark mark='c'/> An e-graph stores equivalence "
            "classes and shared expression structure. It can retain a times two and a shifted left by one as "
            "alternatives in one class. <bookmark mark='d'/> Rewriting expands and merges these classes. Our "
            "small example reaches the displayed alternatives, but general saturation need not terminate or stay "
            "small. Practical systems stop at time, size or iteration limits. <bookmark mark='e'/> Extraction "
            "chooses a represented expression under a specified cost model; here a single shift by two wins. "
            "Optimal tree-cost extraction is different from optimizing shared programs or proving global "
            "machine-code optimality. Tate and colleagues introduced equality saturation, and egg made it "
            "practical for many applications with domain-specific rewrite rules."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(start))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(rules))
            vo.wait_until("b")
            self.play(FadeIn(greedy))
            vo.wait_until("c")
            self.play(FadeOut(greedy), FadeIn(c1), FadeIn(c4), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(root), Create(ar), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Create(best), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()


    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label("spilling research: distinguish fixed/input register counts, holes and cost models", font_size=21, color=GREY_A),
            label(r"extracting the cheapest program from an e-graph is NP-hard when costs are shared: \ which "
                  r"cost models are tractable?", font_size=21, color=GREY_A),
            label("verified optimization: compare supported features, targets and measured workloads",
                  font_size=21, color=GREY_A),
            label("loop synthesis adds state, memory, invariants and termination questions",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover("These directions require carefully stated problems. <bookmark mark='a'/> Strict SSA makes uniform-register graph coloring tractable. Spill selection and copy coalescing add different optimization problems. For spill-everywhere without holes, a fixed number of registers already has known polynomial algorithms; allowing that number as input can make the chordal-graph problem hard. The notes separate these cases. <bookmark mark='b'/> E-graph extraction depends on whether costs count expression occurrences or shared computations. Some formulations admit simple dynamic programming; sharing and extra constraints can create harder problems. <bookmark mark='c'/> Verified optimization also faces an engineering frontier: supported language features, target coverage, proof effort, compilation time and generated-code performance. CompCert's published speed comparisons name particular targets and compiler versions. They are not a universal ranking against current optimization levels. <bookmark mark='d'/> Extending synthesis and validation to loops adds state, memory, invariants and termination questions. No five-instruction cutoff defines that entire field. <bookmark mark='e'/> Our starred exercise starts by reproducing a known restricted spilling result, then asks for a precisely scoped research investigation.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, q in zip('abcd', qs):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
