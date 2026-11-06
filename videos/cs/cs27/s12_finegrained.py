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
            "NP-hardness separates polynomial from exponential. Many practical questions are finer: is quadratic "
            "time really necessary? <bookmark mark='a'/> Fine-grained complexity answers with a few conjectures. "
            "The strong exponential time hypothesis says satisfiability with long clauses cannot be solved much faster "
            "than two to the n. Part 21 used it for edit distance. The 3SUM conjecture, that finding three numbers "
            "summing to zero needs quadratic time, explains why many geometry problems from Part 22 resist faster "
            "algorithms. And the all-pairs shortest paths conjecture covers a family of cubic graph problems. "
            "<bookmark mark='b'/> The link from SAT to quadratic problems is a beautiful trick of Ryan Williams. "
            "Split the variables into two halves, and turn each half-assignment into a vector with one coordinate per "
            "clause, zero if that half already satisfies the clause. <bookmark mark='c'/> Two vectors are orthogonal "
            "exactly when together they satisfy every clause. <bookmark mark='d'/> So a truly subquadratic algorithm "
            "for orthogonal vectors would break the strong exponential time hypothesis. <bookmark mark='e'/> These "
            "questions are not about P versus NP. They are about exponents."
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
            "We ran the reduction. <bookmark mark='a'/> Six random formulas, each with twenty-four variables and a "
            "hundred and one clauses. Each half of the variables gives four thousand and ninety-six vectors, one "
            "coordinate per clause. <bookmark mark='b'/> On every formula, searching for an orthogonal pair gives "
            "the same answer as our SAT solver. <bookmark mark='c'/> And the number of pairs is four thousand and "
            "ninety-six squared, which is two to the twenty-four: exactly the number of assignments. Brute-force "
            "orthogonal vectors is brute-force SAT. <bookmark mark='d'/> So any algorithm that beats N squared by a "
            "polynomial factor would beat two to the n for satisfiability. The slow rows are the unsatisfiable "
            "formulas, where every pair has to be checked."
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
            "Here are the two baselines on this machine. <bookmark mark='a'/> We fed both algorithms instances "
            "with no solution, so they had to do all their work. <bookmark mark='b'/> Each doubling of n costs about "
            "four times as much: quadratic. Four thousand vectors take six tenths of a second; four thousand numbers, "
            "three quarters. <bookmark mark='c'/> The conjectures are delicate: Allan Grønlund and Seth Pettie shaved "
            "logarithmic factors off 3SUM in 2014, so the conjecture now asks only that no polynomial improvement "
            "exists. <bookmark mark='d'/> For an engineer, a conditional lower bound is a stopping rule: stop looking "
            "for a better exponent, and work on constants, parallelism or approximation instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
