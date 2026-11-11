from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


class Ugc(VoiceoverScene):
    def construct(self):
        self.card()
        self.games()
        self.propagation()
        self.consequences()

    def card(self):
        card = chapter_card(10, r"The Unique Games Conjecture", r"One conjecture that would close many gaps",
                            lit=(2002, 2018), extra=((2002, r"Khot"), (2018, r"the 2-to-2 theorem")), part=PART)
        with self.voiceover("Chapter ten. The Unique Games Conjecture."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def games(self):
        head = label(r"Unique games", font_size=34).to_edge(UP, buff=0.3)
        P = {0: (-5.4, 1.2), 1: (-3.6, 1.8), 2: (-2.2, 0.6), 3: (-4.4, -0.4), 4: (-2.8, -1.3)}
        E = [(0, 1, "+1"), (1, 2, "+2"), (0, 3, "+3"), (3, 4, "+1"), (2, 4, "+4"), (1, 3, "+0")]
        nodes = VGroup(*[VGroup(Circle(radius=0.28, color=DATA, stroke_width=2.5).set_fill(BG, 1).move_to([*P[k], 0]),
                                mono(f"x{k}", 16, WHITE).move_to([*P[k], 0])) for k in P])
        edges = VGroup()
        for a, b, t in E:
            ln = Line([*P[a], 0], [*P[b], 0], buff=0.3, color=GREY_B, stroke_width=2)
            edges.add(VGroup(ln, mono(t, 15, HEAD).move_to(ln.get_center() + UP * 0.18)))
        gl = label(r"labels in $\{0, \ldots, k-1\}$; \ each edge: \ $x_b = x_a + c \pmod k$", font_size=18,
                   color=GREY_A).next_to(VGroup(nodes, edges), DOWN, buff=0.3)
        lines = VGroup(
            label(r"each constraint is a \textbf{permutation}: \\ a label on one end fixes the other", font_size=21,
                  color=WHITE),
            label(r"if all constraints can be met, \\ propagation finds a solution: \ easy", font_size=21, color=YES),
            label(r"\textbf{UGC} \ (Khot, 2002): \ for every $\varepsilon$, \ for large $k$, \\ telling ``$1 - "
                  r"\varepsilon$ satisfiable'' from ``$\varepsilon$ satisfiable'' \\ is NP-hard", font_size=21,
                  color=HEAD),
            label(r"almost-satisfiable is where propagation breaks: \\ one bad edge sends labels astray", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(nodes, RIGHT, buff=1.4).align_to(nodes, UP)
        fit_right(lines)
        with self.voiceover(
            "A general unique game assigns labels from a finite alphabet, and each directed edge specifies a permutation relating its endpoint labels. <bookmark mark='a'/> Knowing one endpoint label uniquely determines the other. The drawing and experiment use the special case of cyclic shifts modulo k. <bookmark mark='b'/> For a satisfiable connected instance, choose a root label, propagate along a spanning tree, and check every remaining edge. General permutation games may require trying each possible root label. <bookmark mark='c'/> The Unique Games Conjecture says that for every positive completeness and soundness tolerance, some sufficiently large fixed alphabet makes distinguishing almost-satisfiable instances from instances with very small optimum NP-hard. <bookmark mark='d'/> The hard distinction is approximate satisfiability. It does not contradict the easy test for fully satisfiable games, and the planted shift instances are not a general hardness experiment."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(nodes), FadeIn(gl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def propagation(self):
        u = load("unique")
        head = label(r"Propagation, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[f"{r['eps'] * 100:g}\\%", f"{r['planted'] * 100:.0f}\\%", f"{r['propagate'] * 100:.1f}\\%",
                 f"{r['random'] * 100:.1f}\\%"] for r in u["rows"]]
        tab = grid_table([r"edges corrupted, \ $\varepsilon$", r"hidden labelling", r"propagation",
                          r"random labels"], rows, widths=[3.4, 3.0, 2.6, 2.6], row_h=0.42, font_size=20,
                         mono_cols=(), colors=[[WHITE, HEAD, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        tl = label(rf"{words(u['n'])} vertices, \ {words(u['m'])} random edges, \ $k = {u['k']}$; \ propagation "
                   r"from the best of 10 roots", font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.12)
        r5 = next(r for r in u["rows"] if r["eps"] == 0.05)
        r20 = next(r for r in u["rows"] if r["eps"] == 0.2)
        lines = VGroup(
            label(r"no corruption: \ propagation satisfies everything, \ as promised", font_size=21, color=YES),
            label(rf"5\% corrupted: \ the hidden labels still satisfy 95\%; \ propagation gets "
                  rf"{r5['propagate'] * 100:.0f}\%: \ a bad tree edge ruins its whole subtree", font_size=21,
                  color=NO),
            label(rf"20\%: \ {r20['propagate'] * 100:.0f}\% against 80\%; \ random labels get $1/k$", font_size=21,
                  color=NO),
            label(r"semidefinite programming does better: \ $1 - O(\sqrt{\varepsilon \log k})$ \ (Charikar, \ "
                  r"Makarychev, \ Makarychev, 2006)", font_size=21, color=HEAD),
            label(r"UGC says that is essentially the best any efficient algorithm can do", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.2).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "This finite experiment plants a labelling on a connected simple graph, then corrupts a specified number of edge shifts. <bookmark mark='a'/> We retain all three thousand vertices, nine thousand distinct edges and seven-symbol labels. Ten chosen roots supply the displayed best propagation score. <bookmark mark='b'/> With no corrupted edges, propagation satisfies every constraint. <bookmark mark='c'/> After corruption, a spanning-tree mistake can spread through a subtree. The planted labelling’s displayed score is a lower bound on the true optimum, not a computed optimum certificate. <bookmark mark='d'/> The random baseline now uses independent label draws from one seeded generator per trial. An earlier implementation reset the generator at every vertex and produced constant labels; that original data is preserved. <bookmark mark='e'/> These finite results compare two heuristics on one planted model. General unique-game approximation theorems and conjectured worst-case hardness use their own promises and alphabet parameters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.5)
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def consequences(self):
        head = label(r"If it is true", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"vertex cover: \ factor 2 is optimal \ (Khot and Regev, 2003)", font_size=22, color=YES),
            label(r"MAX-CUT: \ Goemans--Williamson's 0.878 is optimal \ (Khot, \ Kindler, \ Mossel, \ O'Donnell, "
                  r"2004)", font_size=22, color=YES),
            label('Raghavendra: each fixed finite-domain bounded-arity MAX-CSP; optimal SDP threshold under UGC', font_size=22, color=HEAD),
            label('near-satisfiable unique-game algorithms: subexponential, parameter-dependent (ABS, 2010)', font_size=22, color=NO),
            label('Grassmann / 2-to-2 results: related hardness with different completeness promises (2018)', font_size=22, color=DATA),
            label(r"which already gives vertex cover hardness $\sqrt 2 - \varepsilon$", font_size=22, color=GREY_A),
            label(r"the conjecture itself: \ open", font_size=24, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The consequences below are conditional on the Unique Games Conjecture, except where a separate theorem is explicitly stated. <bookmark mark='a'/> It would make improving vertex cover below factor two by any fixed positive constant NP-hard. <bookmark mark='b'/> It would make the Goemans–Williamson MAX-CUT approximation constant optimal up to arbitrarily small additive error in the appropriate worst-case sense. <bookmark mark='c'/> Raghavendra’s theorem concerns each fixed finite-domain, bounded-arity MAX-CSP: a canonical semidefinite relaxation and rounding achieve its optimal approximation threshold under the conjecture. It does not cover every optimization problem. <bookmark mark='d'/> Subexponential algorithms solve certain near-satisfiable unique-game promises with parameter-dependent runtimes. They neither refute the conjecture nor establish P equals NP. <bookmark mark='e'/> The Grassmann-graph and two-to-two games results establish related hardness theorems with different completeness promises. <bookmark mark='f'/> In particular, the known unique-game hardness regime with completeness near one half must not be confused with the conjecture’s near-one completeness requirement. <bookmark mark='g'/> These are precise conditional and partial results; our planted seven-label experiment decides none of the outstanding worst-case questions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
