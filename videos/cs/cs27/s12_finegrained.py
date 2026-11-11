from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, words)


class FineGrained(VoiceoverScene):
    def construct(self):
        self.card()
        self.hypotheses()
        self.williams()
        self.measured()

    def card(self):
        card = chapter_card(11, r"Fine-grained complexity", r"Why can't we beat quadratic time?", lit=(1995, 2015),
                            extra=((1995, r"3SUM-hardness"), (2005, r"Williams: OV"), (2015, r"edit distance")),
                            part=PART)
        with self.voiceover("Chapter eleven. Fine-grained complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hypotheses(self):
        head = label(r"Three conjectures, \ and what they explain", font_size=32).to_edge(UP, buff=0.3)
        rows = [[r"\textbf{SETH}: \ $k$-SAT needs $2^{(1 - o(1))n}$ as $k \to \infty$", r"orthogonal vectors, \ edit "
                 r"distance, \ LCS \ (Part 21), \ graph diameter"],
                [r"\textbf{3SUM}: \ no $n^{2 - \varepsilon}$ algorithm", r"collinear points \ (Part 22), \ triangle "
                 r"listing, \ polygon covering"],
                [r"\textbf{APSP}: \ no $n^{3 - \varepsilon}$ all-pairs shortest paths", r"negative triangle, \ "
                 r"radius, \ betweenness \ (Part 18)"]]
        tab = grid_table([r"hypothesis", r"conditionally optimal, \ given it"], rows, widths=[6.4, 6.4], row_h=0.62,
                         font_size=20, mono_cols=(), colors=[[HEAD, WHITE], [DATA, WHITE], [LAM, WHITE]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"Williams \ (2005): \ split the $n$ variables in two; \ list the $2^{n/2}$ half-assignments as "
                  r"vectors, \ one coordinate per clause", font_size=21, color=WHITE),
            label(r"two vectors are orthogonal $\iff$ together they satisfy every clause", font_size=21, color=DATA),
            label(r"so OV in $N^{2 - \varepsilon}$ would solve SAT in $2^{(1 - \varepsilon/2)n}$: \ refuting SETH",
                  font_size=21, color=NO),
            label(r"these are not P vs NP questions: \ they ask for the \textbf{exponent}", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "NP-hardness alone does not prove an exponential lower bound. Fine-grained hypotheses ask more specific questions about achievable exponents. <bookmark mark='a'/> SETH says that for every fixed positive epsilon, some fixed clause width rules out a two-to-the-one-minus-epsilon-times-n SAT algorithm in the specified deterministic model. <bookmark mark='b'/> The 3SUM and APSP hypotheses concern fixed exponent improvements over quadratic and cubic time, with input and machine models stated. Logarithmic speedups do not refute them. <bookmark mark='c'/> Split a sparse bounded-width SAT instance’s variables into two halves. Each partial assignment becomes a vector whose coordinates identify clauses it fails to satisfy. <bookmark mark='d'/> Two vectors are orthogonal exactly when their combined assignment satisfies every clause. Under the dimensional and polynomial-overhead conditions, a fixed exponent improvement for the relevant OV family would refute SETH. <bookmark mark='e'/> The three hypotheses are distinct conditional assumptions. Their reductions and precise variants must be stated rather than treating all fast-problem lower bounds as one conjecture."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), run_time=4.0)
            for mk, ln in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def williams(self):
        w = load("williams")
        N = w["N"]
        head = label(r"SAT as orthogonal vectors, \ run", font_size=34).to_edge(UP, buff=0.3)
        rows = [[str(r["seed"]), r"satisfiable" if r["sat"] else r"unsatisfiable",
                 r"orthogonal pair" if r["ov"] else r"none", f"{r['ov_s'] * 1000:.0f} ms"] for r in w["rows"]]
        tab = grid_table([r"formula", r"our CDCL solver", r"OV search", r"OV time"], rows,
                         widths=[1.8, 3.2, 3.2, 2.0], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[GREY_A, YES if r["sat"] else NO, YES if r["ov"] else NO, DATA] for r in w["rows"]])
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        tl = label(rf"random 3-SAT, \ $n = {w['n']}$ variables, \ {w['m']} clauses", font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(rf"each half: \ $2^{{{w['n'] // 2}}}$ = {words(N)} vectors with {w['m']} coordinates", font_size=21,
                  color=WHITE),
            label(r"the two answers agree on every formula", font_size=21, color=YES),
            label(rf"$N^2$ = {words(N * N)} pairs \ = $2^{{{w['n']}}}$: \ exactly the number of assignments",
                  font_size=21, color=HEAD),
            label(r"so beating $N^2$ by any polynomial factor beats $2^n$ for SAT: \ unsatisfiable formulas, "
                  r"\ which check every pair, \ are the slow rows", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.22).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "We execute the SAT-to-orthogonal-vectors reduction on six complete finite inputs. <bookmark mark='a'/> Each formula has twenty-four variables and a hundred and one clauses. Every one of the two halves’ four thousand and ninety-six vectors is retained and independently reconstructed. <bookmark mark='b'/> Orthogonal-vector search is checked with a separate native implementation. Positive pairs decode to satisfying assignments; SAT statuses are also cross-checked with native Glucose. Native UNSAT agreement is implementation evidence rather than a retained refutation proof. <bookmark mark='c'/> Each pair of half assignments corresponds to one full assignment, so the full cross-product has two to the twenty-fourth pairs. <bookmark mark='d'/> Search may stop early on positive instances. The measured times describe these specific inputs and implementations, not an exponential lower bound or an asymptotic theorem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.5)
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        f = load("finegrained")
        head = label(r"Quadratic, \ measured", font_size=34).to_edge(UP, buff=0.35)
        rows = [[words(o["n"]), f"{o['seconds'] * 1000:.0f} ms", f"{t['seconds'] * 1000:.0f} ms"]
                for o, t in zip(f["ov"], f["three_sum"])]
        tab = grid_table([r"$n$", r"orthogonal vectors \ (64-bit)", r"3SUM \ (sort + two pointers)"], rows,
                         widths=[1.8, 4.0, 4.4], row_h=0.45, font_size=20, mono_cols=(),
                         colors=[[WHITE, DATA, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"no-instances, \ so both algorithms do all their work", font_size=21, color=GREY_A),
            label(r"each doubling of $n$ costs about $4\times$: \ quadratic, \ as the conjectures say it must be",
                  font_size=21, color=WHITE),
            label(r"3SUM's conjecture was refined: \ $n^2 / \mathrm{polylog}$ algorithms exist \ (Gr\o nlund and "
                  r"Pettie, 2014), \ $n^{2 - \varepsilon}$ is still open", font_size=21, color=NO),
            label(r"in practice: \ a conditional lower bound says \textbf{stop optimizing the exponent}; \ attack "
                  r"constants, \ or approximate", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The timing table uses finite negative instances with explicit certificates. <bookmark mark='a'/> Every vector in the OV fixtures shares bit sixty-three, so no orthogonal pair exists. Every integer in the 3SUM fixtures is odd, so three of them cannot sum to zero. Full inputs are retained. <bookmark mark='b'/> We report the median of thirty teaching-call intervals per size; serialization and independent checking occur outside those timers. <bookmark mark='c'/> These loops show roughly quadratic growth over the measured sizes. Fixed sixty-four-bit vectors are an implementation benchmark, distinct from growing-dimension OV hardness assumptions. <bookmark mark='d'/> Known logarithmic 3SUM improvements and future algorithmic changes must be distinguished from a fixed polynomial-exponent improvement. Conditional lower bounds are useful only within their stated models and assumptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
