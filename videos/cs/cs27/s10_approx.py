from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load)


class Approx(VoiceoverScene):
    def construct(self):
        self.card()
        self.gap()
        self.maxsat()
        self.table()

    def card(self):
        card = chapter_card(9, r"Hardness of approximation", r"Why can't some approximations be improved?",
                            lit=(1991, 2001), extra=((1991, r"Feige--Goldwasser--Lov\'asz--Safra--Szegedy"),
                                                     (2001, r"H\aa stad")), part=PART)
        with self.voiceover("Chapter nine. Hardness of approximation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def gap(self):
        head = label(r"A PCP is a gap", font_size=34).to_edge(UP, buff=0.35)
        bar = Rectangle(width=10, height=0.5, stroke_color=GREY_B).next_to(head, DOWN, buff=1.0)
        yes = Rectangle(width=0.6, height=0.5, stroke_width=0, fill_color=YES, fill_opacity=0.8).align_to(bar, RIGHT
                                                                                                          ).align_to(
            bar, UP)
        no = Rectangle(width=5.0, height=0.5, stroke_width=0, fill_color=NO, fill_opacity=0.8).align_to(bar, LEFT
                                                                                                       ).align_to(
            bar, UP)
        lab = VGroup(label(r"fraction of clauses satisfiable", font_size=19, color=GREY_A).next_to(bar, UP, buff=0.12),
                     label(r"satisfiable: \ 100\%", font_size=19, color=YES).next_to(yes, DOWN, buff=0.12),
                     label(r"unsatisfiable: \ at most $1 - \varepsilon$", font_size=19, color=NO).next_to(no, DOWN,
                                                                                                    buff=0.12))
        lines = VGroup(
            label(r"read the verifier's tests as clauses: \ a proof is an assignment", font_size=22, color=WHITE),
            label(r"true statement: \ some assignment satisfies \textbf{all} of them", font_size=22, color=YES),
            label(r"false statement: \ every assignment fails a \textbf{constant fraction}", font_size=22, color=NO),
            label(r"so telling ``all'' from ``at most $1 - \varepsilon$'' is NP-hard: \ approximating within "
                  r"$1 - \varepsilon$ is too", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(lab, DOWN, buff=0.6)
        with self.voiceover(
            "PCPs imply hardness of approximation through a gap-preserving reduction. <bookmark mark='a'/> Encode each verifier acceptance test as a bounded-arity constraint, with proof bits serving as assignment variables. <bookmark mark='b'/> Perfect completeness gives an assignment satisfying every constraint in a yes-instance. <bookmark mark='c'/> Soundness bounds the fraction that any assignment can satisfy in a no-instance, leaving a constant gap. Conversion to a particular clause format may change that constant. <bookmark mark='d'/> An approximation strong enough to distinguish the two cases would solve the original NP-hard decision problem. The objective, reduction, completeness and soundness parameters determine the actual approximation threshold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(yes), FadeIn(lab[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(no), FadeIn(lab[2]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def maxsat(self):
        m = load("maxsat")
        head = label(r"MAX-3SAT: \ a coin is optimal", font_size=34).to_edge(UP, buff=0.35)
        rows = [[f"{r['ratio']:g}", f"{r['random'] * 100:.1f}\\%", f"{r['walksat'] * 100:.1f}\\%"] for r in m["rows"]]
        tab = grid_table([r"clauses per variable", r"random assignment", r"local search \ (WalkSAT)"], rows,
                         widths=[3.0, 3.0, 3.4], row_h=0.45, font_size=20, mono_cols=(),
                         colors=[[WHITE, HEAD, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        tl = label(r"random 3-SAT, \ $n = 100$, \ 5 formulas per row", font_size=18, color=GREY_A).next_to(
            tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"a random assignment satisfies each 3-clause with probability $\tfrac78$: \ 87.5\% on average",
                  font_size=21, color=HEAD),
            label(r"H\aa stad \ (2001): \ for every $\varepsilon > 0$, \ beating $\tfrac78 + \varepsilon$ on "
                  r"\textbf{satisfiable} formulas is NP-hard", font_size=21, color=NO),
            label('no deterministic fixed improvement in the worst case unless P = NP', font_size=21, color=WHITE),
            label(r"on random formulas local search does far better: \ worst case and typical case differ",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "Consider MAX-E3SAT with three distinct variables in each clause. <bookmark mark='a'/> A uniform random assignment satisfies each such clause with probability seven eighths, so linearity of expectation guarantees that fraction on average. Conditional expectation can derandomize this guarantee. <bookmark mark='b'/> Our finite random formulas and bounded WalkSAT runs are retained in full. Their better scores concern this sample distribution and do not improve a worst-case approximation guarantee. <bookmark mark='c'/> Håstad proved that for every fixed positive epsilon, distinguishing satisfiable instances from instances with optimum at most seven eighths plus epsilon is NP-hard. <bookmark mark='d'/> Consequently, a deterministic polynomial-time algorithm beating that threshold would imply P equals NP. Randomized algorithms require the corresponding randomized complexity qualification. Sampling success on easy instances does not establish such a uniform algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        head = label('Selected approximation bounds', font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"MAX-3SAT", r"$\tfrac78$ \ (random)", r"$\tfrac78 + \varepsilon$", r"H\aa stad \ (2001)"],
                [r"MAX-3LIN", r"$\tfrac12$ \ (random)", r"$\tfrac12 + \varepsilon$", r"H\aa stad \ (2001)"],
                [r"set cover", r"$\ln n$ \ (greedy)", r"$(1 - \varepsilon) \ln n$", r"Feige \ (1998); \ Dinur--Steurer "
                 r"(2014)"],
                [r"clique", r"$n$ \ (trivial)", r"$n^{1 - \varepsilon}$", r"H\aa stad \ (1999); \ Zuckerman \ (2007)"],
                [r"vertex cover", r"2 \ (matching, Part 23)", r"$\sqrt 2 - \varepsilon$", r"Khot, \ Minzer, \ Safra "
                 r"\ (2018)"],
                [r"MAX-CUT", r"0.878 \ (Goemans--Williamson)", r"$\tfrac{16}{17} + \varepsilon$", r"H\aa stad; \ "
                 r"Trevisan et al."]]
        tab = grid_table([r"problem", 'illustrative algorithm / guarantee', r"NP-hard to beat", r"by"], rows,
                         widths=[2.4, 3.6, 2.6, 4.6], row_h=0.5, font_size=19, mono_cols=(),
                         colors=[[WHITE, YES, NO, GREY_A]] * 4 + [[WHITE, YES, HEAD, GREY_A]] * 2)
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        note = label(r"the last two rows have a gap between what we can do and what we can rule out: \ chapter 10",
                     font_size=22, color=HEAD).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Compare approximation thresholds only for the stated optimization problems and models. <bookmark mark='a'/> MAX-E3SAT has the seven-eighths guarantee. The MAX-E3LIN result instead concerns distinguishing almost-satisfiable linear systems from systems whose optimum is near one half; exactly satisfiable linear systems are solved by elimination. <bookmark mark='b'/> Set-cover hardness has logarithmic dependence on the universe size. Clique hardness gives an n to the one-minus-epsilon barrier, while the trivial n approximation is merely a simple baseline, not the best known algorithm. <bookmark mark='c'/> Vertex cover and MAX-CUT retain gaps between unconditional algorithms and known hardness. The next chapter explains which sharper barriers would follow from the Unique Games Conjecture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:5]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[5])), FadeIn(VGroup(*tab.cells[6])))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
