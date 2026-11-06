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
            "In 2002 Subhash Khot proposed a conjecture about a simple kind of constraint problem. <bookmark "
            "mark='a'/> Give each vertex a label from zero to k minus one. Each edge demands that the label at one "
            "end equal the label at the other plus some constant, modulo k. A label on one end determines the other "
            "uniquely: hence unique games. <bookmark mark='b'/> If every constraint can be met, there is an easy "
            "algorithm: fix one label and propagate. <bookmark mark='c'/> Khot conjectured that telling apart games "
            "where nearly all constraints can be met from games where almost none can is NP-hard. <bookmark "
            "mark='d'/> Nearly satisfiable is exactly where propagation fails: a single violated edge sends the labels "
            "astray."
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
            "We can watch propagation fail. We planted a labelling on three thousand vertices and nine thousand "
            "edges, with seven labels, then corrupted a fraction epsilon of the constraints. <bookmark mark='a'/> "
            "With no corruption, propagation from any vertex satisfies every constraint. <bookmark mark='b'/> With "
            "five percent corrupted, the hidden labelling still satisfies ninety-five percent, but propagation gets "
            "only eighty-three: each bad edge in the search tree corrupts everything below it. <bookmark mark='c'/> "
            "At twenty percent, propagation falls to a half, and random labels get one seventh. <bookmark "
            "mark='d'/> A semidefinite program does much better, losing only about the square root of epsilon log "
            "k, as Moses Charikar and Konstantin and Yury Makarychev showed in 2006. <bookmark mark='e'/> The "
            "conjecture says that, up to constants, nothing efficient can do better."
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
            label(r"Raghavendra \ (2008): \ for \textbf{every} constraint problem, \ one semidefinite program is the "
                  r"best algorithm", font_size=22, color=HEAD),
            label(r"evidence against: \ unique games in time $\exp(n^{\varepsilon})$ \ (Arora, \ Barak, \ Steurer, "
                  r"2010)", font_size=22, color=NO),
            label(r"evidence for: \ the \textbf{2-to-2 theorem} \ (Khot, \ Minzer, \ Safra, 2018), \ a weaker form, "
                  r"\ proved", font_size=22, color=DATA),
            label(r"which already gives vertex cover hardness $\sqrt 2 - \varepsilon$", font_size=22, color=GREY_A),
            label(r"the conjecture itself: \ open", font_size=24, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part 23 met the conjecture's consequences; here is the whole picture. <bookmark mark='a'/> If it holds, "
            "the factor two for vertex cover is optimal, <bookmark mark='b'/> and so is Goemans and Williamson's "
            "point eight seven eight for MAX-CUT. <bookmark mark='c'/> Prasad Raghavendra showed in 2008 that it "
            "would make one semidefinite program the optimal approximation algorithm for every constraint "
            "satisfaction problem at once. <bookmark mark='d'/> There is evidence against it: Sanjeev Arora, Boaz "
            "Barak and David Steurer found an algorithm for unique games that is subexponential. <bookmark "
            "mark='e'/> And evidence for it: in 2018 Subhash Khot, Dor Minzer and Muli Safra proved the 2-to-2 "
            "theorem, a slightly weaker version, <bookmark mark='f'/> which already shows vertex cover is hard to "
            "approximate below the square root of two. <bookmark mark='g'/> The conjecture itself remains open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
