from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (FAIL, FCOL, GCOST, HEUR, HIST, HOT, LEARN, PART, PATH, SYMBOL, frontier_rgb,
                                  image_from_rgb, load, node_box, rgb, tour_mob)


def tile_frame(caption, color, TW=3.0, TH=2.0):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color="#121722", fill_opacity=1)
    return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        tm = load("tm")
        b5 = np.asarray(tm["bb5_img"])
        b5 = b5 / max(b5.max(), 1e-9)
        z, o = rgb("#1B2130"), rgb(FCOL)
        out.append((image_from_rgb(z * (1 - b5[..., None]) + o * b5[..., None], width=2.2, height=1.9, smooth=True),
                    r"a $5$-state machine halts", FCOL))
        g = load("grid")
        free = np.asarray(g["free"]).astype(bool)
        a = image_from_rgb(frontier_rgb(free, np.asarray(g["dijkstra_order"]), 1e9, band=1e9), width=1.5)
        b = image_from_rgb(frontier_rgb(free, np.asarray(g["astar_order"]), 1e9, band=1e9), width=1.5)
        out.append((Group(a, b).arrange(RIGHT, buff=0.1), r"Dijkstra's circle, \ A*'s ellipse", GCOST))
        p8 = load("puzzle8")
        ax = Axes(x_range=[0, 26, 5], y_range=[0, 5.5, 1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        D = np.asarray(p8["depths"])
        out.append((VGroup(ax, *[curve(ax, D, np.log10(np.asarray(p8[k])), c, 3) for k, c in
                                 (("astar_h0", GCOST), ("astar_h1", FCOL), ("astar_h2", HEUR))]),
                    r"better guesses, \ less search", HEUR))
        t = load("tsp")
        ax2 = Axes(x_range=[0, 1800, 300], y_range=[0, 1200, 300], x_length=TW * 0.85, y_length=TH * 0.85,
                   tips=False, axis_config={"stroke_opacity": 0})
        xy = np.asarray(t["xy"], float)
        out.append((VGroup(ax2, tour_mob(ax2, xy, t["sa_best_tour"], color=HOT, width=2),
                           *[Dot(ax2.c2p(*p), radius=0.025, color=WHITE) for p in xy]), r"annealing finds the tour", HOT))
        ab = load("alphabeta")
        ax3 = Axes(x_range=[0, 10, 2], y_range=[0, 8, 2], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax3, curve(ax3, ab["depths"], np.log10(np.asarray(ab["minimax"])), GREY_B, 3),
                           curve(ax3, np.arange(1, len(ab["ab_perfect"]) + 1), np.log10(np.asarray(ab["ab_perfect"])),
                                 PATH, 3)), r"alpha--beta: \ $b^{d/2}$", PATH))
        s3 = load("sat3")
        A = np.asarray(s3["alphas"], float)
        ax4 = Axes(x_range=[A[0], A[-1], 1], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        sat_tile = VGroup(ax4, *[curve(ax4, A, s3[f"psat_{n}"], c, 3) for n, c in
                                zip(s3["ns"], [GREY_B, HEUR, FCOL, PATH])])
        censored = any(s3[f"censored_{n}"] for n in s3["ns"])
        if censored:
            sat_tile.add(*[DashedVMobject(curve(ax4, A, s3[f"psat_upper_{n}"], c, 2))
                           for n, c in zip(s3["ns"], [GREY_B, HEUR, FCOL, PATH])])
        out.append((sat_tile, r"SAT fraction bounds" if censored else r"SAT's phase transition", SYMBOL))
        cd = load("cdcl")
        ax5 = Axes(x_range=[2, 12, 2], y_range=[0, 8, 2], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax5, curve(ax5, cd["adder_widths"], np.log10(np.asarray(cd["adder_dpll"], float)), GCOST, 3),
                           curve(ax5, cd["adder_widths"], np.log10(np.asarray(cd["adder_cdcl"], float)), LEARN, 3)),
                    r"clause learning pays", LEARN))
        tl = load("tail")
        ax6 = Axes(x_range=[0, 5, 1], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax6, curve(ax6, np.log10(np.asarray(tl["coverage_k"], float)), np.asarray(tl["coverage"]),
                                      FAIL, 3)), r"the long tail", FAIL))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Turing defined what machines can compute, and what they cannot. Search finds solutions by "
            "trying things; A star, with an admissible heuristic, finds the cheapest and can greatly reduce the search, "
            "and effective heuristics often come from relaxed problems. Annealing's controlled randomness escapes local optima. "
            "With excellent move ordering, alpha-beta can search roughly twice as deep for the same work. Logic reduces to "
            "resolution and satisfiability, whose hard "
            "problems live at a phase transition, and clause learning makes solvers fast. And knowledge written by hand runs "
            "into the long tail, which is why the field turned to learning."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"from hand-written rules to learned weights", [9]),
            (r"search guided by a learned evaluation", [26]),
            (r"search over chains of thought; \ checkable answers", [28]),
            (r"planning, \ tools and agents", [29]),
            (r"proofs, \ verification, \ and checking the checker", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Learned weights replace hand-written rules with the perceptron and backpropagation, in "
            "Part 9. Search guided by a learned evaluation is AlphaZero, in Part 26. Search over chains of thought, rewarded by "
            "checkable answers, makes the reasoning models of Part 28. Planning and tools return in the agents of Part 29. And "
            "verification, proof, and who checks the checker close the series in Part 31."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the Manhattan distance of the 8-puzzle is consistent: \ every move changes it by exactly one.",
            r"Prove that a consistent heuristic is admissible. \ Give an admissible heuristic that is not consistent.",
            r"With perfect move ordering, show that alpha--beta on a uniform tree evaluates exactly "
            r"$b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves.",
            r"Show that the Metropolis rule satisfies detailed balance for $\pi(s) \propto e^{-E(s)/T}$, \ and that "
            r"as $T \to 0$, $\pi$ concentrates on the global minima.",
            r"Show that a resolvent is entailed by its parents. \ Refute $\{P \lor Q,\ \lnot P \lor Q,\ P \lor \lnot Q,"
            r"\ \lnot P \lor \lnot Q\}$ by resolution.",
            r"For random 3-SAT with $m = \alpha n$ clauses, show that the expected number of satisfying assignments is "
            r"$2^n (7/8)^{\alpha n}$, \ and deduce that the threshold is at most $\ln 2 / \ln(8/7) \approx 5.19$.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from consistent heuristics to the satisfiability threshold. Pause here, and "
            "work through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 3, \ Vectors That Mean Things", font_size=40).to_edge(UP, buff=0.5)
        sym = VGroup(node_box(r"\textit{cat}", SYMBOL, font_size=28), node_box(r"\textit{dog}", SYMBOL, font_size=28),
                     node_box(r"\textit{car}", SYMBOL, font_size=28)).arrange(DOWN, buff=0.35).move_to([-4.0, -0.4, 0])
        sl = label(r"symbols: \ equal or not", font_size=24, color=SYMBOL).next_to(sym, UP, buff=0.3)
        ax = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=5.0, y_length=3.4,
                         background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5})
        ax.move_to([3.2, -0.4, 0])
        pts = {"cat": (1.2, 1.0), "dog": (1.7, 0.6), "car": (-1.8, -1.2)}
        vecs = VGroup(*[Arrow(ax.c2p(0, 0), ax.c2p(*v), buff=0, color=LEARN, stroke_width=4) for v in pts.values()])
        names = VGroup(*[label(rf"\textit{{{k}}}", font_size=24, color=LEARN).next_to(ax.c2p(*v), UR, buff=0.05)
                         for k, v in pts.items()])
        vl = label(r"vectors: \ near or far", font_size=24, color=LEARN).next_to(ax, UP, buff=0.2)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Next time: meaning as geometry. To a symbol, cat is as far from dog as from car. Part 3 turns words into vectors, "
            "where nearness means similarity, and builds the linear algebra every model in this course runs on: inner products, "
            "eigenvalues, the singular value decomposition."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sym), FadeIn(sl), FadeIn(tag))
            self.play(Create(ax), FadeIn(vl), LaggedStart(*[GrowArrow(v) for v in vecs], lag_ratio=0.3),
                      FadeIn(names), run_time=max(2.0, vo.duration - 3.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~Russell \& P.~Norvig, \textit{Artificial Intelligence: A Modern Approach}, 4th ed.\ (2020)",
             r"N.~J.~Nilsson, \textit{The Quest for Artificial Intelligence} (2009); \ J.~Pearl, \textit{Heuristics} "
             r"(1984)",
             r"A.~Biere et al., \textit{Handbook of Satisfiability}, 2nd ed.\ (2021); \ D.~E.~Knuth, \textit{TAOCP} "
             r"vol.\ 4B (2022)"],
            [r"Turing (1936, 1950); \ McCarthy, Minsky, Rochester \& Shannon (1955); \ Newell, Shaw \& Simon (1957); "
             r"\ Newell \& Simon (1976); \ Rad\'o (1962)",
             r"Moore (1959); \ Dijkstra (1959); \ Hart, Nilsson \& Raphael (1968); \ Korf (1985, 1997); \ Culberson "
             r"\& Schaeffer (1998); \ Korf \& Felner (2002); \ Agostinelli et al.\ (2019)",
             r"Metropolis et al.\ (1953); \ Kirkpatrick, Gelatt \& Vecchi (1983); \ Holland (1975); \ Romera-Paredes "
             r"et al.\ (2023); \ Novikov et al.\ (2025)",
             r"von Neumann (1928); \ Shannon (1950); \ Samuel (1959); \ Knuth \& Moore (1975); \ Campbell, Hoane \& "
             r"Hsu (2002); \ Schaeffer et al.\ (2007)",
             r"Robinson (1965); \ Wos, Robinson \& Carson (1965); \ Davis \& Putnam (1960); \ Davis, Logemann \& "
             r"Loveland (1962); \ Cook (1971); \ Mitchell, Selman \& Levesque (1992); \ M\'ezard, Parisi \& Zecchina "
             r"(2002); \ Marques-Silva \& Sakallah (1999); \ Moskewicz et al.\ (2001)",
             r"Waltz (1975); \ Mackworth (1977); \ McCarthy \& Hayes (1969); \ Fikes \& Nilsson (1971); \ Sussman "
             r"(1975); \ Blum \& Furst (1997); \ Hoffmann \& Nebel (2001)",
             r"Quillian (1968); \ Minsky (1974); \ Shortliffe (1976); \ Yu et al.\ (1979); \ McDermott (1982); \ "
             r"Lenat (1995); \ Weizenbaum (1966, 1976); \ Lighthill (1973); \ Moravec (1988)",
             r"Jones \& Bergen (2025); \ Trinh et al.\ (2024); \ Hubert et al.\ (2025); \ Valmeekam et al.\ (2024); "
             r"\ Liu et al.\ (2023); \ Shrager (2026)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Russell and Norvig's textbook is the place to go deeper: everything in this part is in it. For the "
            "history, Nils Nilsson's The Quest for Artificial Intelligence. Thanks for watching, and see you in Part 3."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
