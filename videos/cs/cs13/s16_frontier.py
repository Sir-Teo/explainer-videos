from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono, region)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.employment()
        self.superopt()
        self.cost()
        self.stochastic()
        self.egraph()
        self.learned()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ searching for the best program", r"Can a machine find the optimal "
                            r"code?", lit=(1987, 2009), extra=((1987, r"Massalin's superoptimizer"),
                                                               (2009, r"equality saturation")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: searching for the best program."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def employment(self):
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

    def cost(self):
        so = load("superopt")
        head = label(r"Candidate-search cost on this host", font_size=34).to_edge(UP, buff=0.3)
        best = {}
        for t in so["targets"]:
            best[t["length"]] = max(best.get(t["length"], 0), t["seconds"])
        ks = sorted(best)
        ch = VGroup()
        import math
        assert all(value > 0 for value in best.values())
        y_max = max(6, math.ceil(max(3 + math.log10(value) for value in best.values()) + 0.75))
        ax = Axes(x_range=[0.5, 4.5, 1], y_range=[0, y_max, 1], x_length=5.5, y_length=4.0,
                  axis_config={"color": GREY_D, "include_ticks": True},
                  y_axis_config={"include_numbers": False}).move_to(LEFT * 2.6 + DOWN * 0.3)
        ylab = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0.5, y), LEFT, buff=0.1)
                        for y, t in ((1, r"10 ms"), (3, r"1 s"), (5, r"100 s"))])
        xlab = VGroup(*[label(str(k), font_size=16, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                        for k in ks])
        xt = label(r"found body length (different target functions)", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        import math
        dots = VGroup(*[Dot(ax.c2p(k, 3 + math.log10(best[k])), color=NO, radius=0.08) for k in ks])
        line = VMobject(color=NO, stroke_width=2).set_points_as_corners([d.get_center() for d in dots])
        vals = VGroup(*[label(f"{best[k]:.3f} s" if best[k] < 1 else f"{best[k]:.0f} s", font_size=15,
                              color=NO).next_to(dots[i], UP + LEFT * 0.3, buff=0.1) for i, k in enumerate(ks)])
        side = VGroup(
            label("11 register operations + selected immediate forms; restricted search vocabulary", font_size=19,
                  color=GREY_A),
            label("more available operands increase the branching of the candidate search", font_size=19, color=GREY_A),
            label(r"pruning helps: \ skip any value already computed \ (observational equivalence)", font_size=19,
                  color=GREY_A),
            label("this run searches through length 4; no universal five-instruction cutoff", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover("Search has a measurable cost. <bookmark mark='a'/> This plot groups the recorded runs by their reported candidate length and takes the longest elapsed time in each group. The vertical axis is logarithmic. These are host measurements for these target functions and this implementation, including the work performed by its proof checks. They are not universal times for all programs of a given length. <bookmark mark='b'/> Each extra candidate instruction introduces choices of operation, operands and selected immediate constants. The search grows rapidly, while finite-test pruning reduces work at the price of completeness. We stop at the configured length bound. Neither four observed lengths nor that chosen limit proves a universal five-instruction barrier.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), FadeIn(xt), run_time=0.6)
            vo.wait_until('a')
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.4), Create(line), FadeIn(vals), run_time=2.5)
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.6), run_time=5)
        self.wait(0.3)
        self.clear_scene()

    def stochastic(self):
        head = label(r"Smarter search", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"STOKE", font_size=24, color=YES),
                   label(r"Schkufza, Sharma, Aiken, \ 2013", font_size=18, color=GREY_B),
                   label(r"a random walk over x86 programs (Markov chain Monte Carlo), \ cost $=$ wrongness on "
                         r"tests $+$ estimated time;", font_size=19, color=GREY_A),
                   label("reported gains on selected kernels, compilers and evaluation machines", font_size=19,
                         color=GREY_A)),
            VGroup(label(r"Souper", font_size=24, color=CTRL),
                   label(r"Sasnauskas, Regehr et al., \ 2017", font_size=18, color=GREY_B),
                   label(r"synthesizes small replacements for pieces of LLVM IR with an SMT solver;",
                         font_size=19, color=GREY_A),
                   label(r"its finds are reported as missing optimizations, \ and many were added to LLVM",
                         font_size=19, color=GREY_A)),
            VGroup(label(r"AlphaDev", font_size=24, color=FUNC),
                   label(r"Mankowitz et al., \ 2023", font_size=18, color=GREY_B),
                   label(r"reinforcement learning over assembly for sorting 3 to 5 numbers;", font_size=19,
                         color=GREY_A),
                   label("particular routines improved; derived code entered LLVM libc++", font_size=19, color=GREY_A)),
        )
        for r in rows:
            r[0].move_to([-5.4, 0, 0], aligned_edge=LEFT)
            top = VGroup(r[1], r[2], r[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            top.move_to([-3.2, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[0].set_x(-5.4 + r[0].width / 2)
            VGroup(r[1], r[2], r[3]).set_x(-3.2 + VGroup(r[1], r[2], r[3]).width / 2)
        with self.voiceover(
            (
            "Search can use stronger guidance than plain enumeration. <bookmark mark='a'/> STOKE, introduced in "
            "2013, explores x86 program fragments stochastically, using test errors and a performance objective "
            "to guide proposals. Its reported gains belong to selected kernels, comparison compilers and "
            "evaluation machines. Testing and the applicable validation method remain essential. <bookmark "
            "mark='b'/> Souper uses solver-guided synthesis to find replacements for fragments of LLVM "
            "intermediate code. Such findings can expose missed optimizations; neither search method promises the "
            "best program for every function. <bookmark mark='c'/> AlphaDev's 2023 study searched assembly "
            "routines for small sorting tasks. It improved particular three- and five-element instruction "
            "sequences and matched the comparison length for four elements. Derived C++ routines entered LLVM's "
            "libc++ sorting implementation. The measured latency and library gains depend on the study's routines "
            "and workloads; this does not prove universal shortest sorting or a speedup for every input and "
            "machine."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
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

    def learned(self):
        head = label(r"Learning the heuristics", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"a compiler is full of guesses: \ inline this call? \ spill which value? \ unroll how far?",
                  font_size=21, color=GREY_A),
            label(r"\textbf{MLGO} \ (Trofin et al., \ Google, \ 2021): \ a learned inlining policy in LLVM, \ "
                  r"trained by reinforcement learning", font_size=20, color=GREY_A),
            label("documented MLGO objectives: inlining for size; register eviction for performance",
                  font_size=20, color=YES),
            label(r"the hard part: \ the guess must be cheap, \ and stay good when the code changes", font_size=20,
                  color=NO),
            label(r"how such policies are trained: \ \textit{AI, Built}", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "Another direction is to learn selected optimization choices. <bookmark mark='a'/> Compilers contain "
            "heuristics for inlining, register eviction and loop transformations. A learned policy can replace "
            "one of those choices while the compiler still enforces its correctness constraints. <bookmark "
            "mark='b'/> Google's MLGO project introduced learned inlining decisions aimed at smaller code. LLVM's "
            "current documentation also describes a learned greedy register-allocation eviction policy aimed at "
            "performance. Those are different objectives. <bookmark mark='c'/> Reported code-size savings concern "
            "particular trained models, software corpora and deployments; they are not a promise for every "
            "program or for the register policy. <bookmark mark='d'/> The practical challenge is to make each "
            "decision cheap, measure the result on the target workload, and keep the policy useful as code and "
            "compilers change. <bookmark mark='e'/> Our companion series, AI, Built, develops the learning "
            "methods behind such policies."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
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
