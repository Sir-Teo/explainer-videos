from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.yao()
        self.optimality()
        self.learned()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ how good can a data structure be?", r"Are the textbook bounds the "
                            r"truth?", lit=(2025,), extra=((1985, r"Yao: \ uniform hashing is optimal?"),
                                                           (2025, r"Farach-Colton, \ Krapivin and Kuszmaul")),
                            part=PART)
        with self.voiceover("Chapter sixteen. Frontier: how good can a data structure be?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def yao(self):
        d = load("frontier")
        head = label(r"A forty-year-old conjecture, \ refuted", font_size=34).to_edge(UP, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[0, 2.1, 0.5], y_range=[0, 2.1, 0.5], x_length=5.6, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.4)
        xs = [np.log10(1 / r["delta"]) for r in rows]

        def line(key, col, dash=False):
            pts = [ax.c2p(x, np.log10(max(r[key], 1))) for x, r in zip(xs, rows)]
            v = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
            return DashedVMobject(v, num_dashes=24).set_color(col) if dash else VGroup(
                v, *[Dot(p, radius=0.05, color=col) for p in pts])
        meas, yao_, funnel = line("measured", NO), line("yao", NO, dash=True), line("funnel", YES, dash=True)
        xt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v, t in ((0.3, r"$\tfrac12$"), (1, r"$\tfrac1{10}$"), (2, r"$\tfrac1{100}$"))])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "1"), (1, "10"), (2, "100"))])
        xl = label(r"free fraction $\delta$ of the table", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(r"probes for one more insert, \ log scale", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1
                                                                                                  ).align_to(ax, LEFT)
        side = VGroup(
            label(r"Yao \ (1985) \ conjectured that random probe sequences are optimal: \ about $1/\delta$",
                  font_size=20, color=NO),
            label(r"red: \ double hashing measured, \ $2^{13}$ slots \ (dashed: \ $1/\delta$)", font_size=19,
                  color=NO),
            label(r"2025: \ \textbf{funnel hashing} reaches $O(\log^2 \tfrac1\delta)$ \ (green, \ growth rate only), "
                  r"\ and that is optimal for its kind", font_size=20, color=YES),
            label(r"\textbf{elastic hashing}: \ $O(1)$ on average, \ $O(\log \tfrac1\delta)$ worst case; \ no "
                  r"element ever moves", font_size=20, color=YES),
            label(r"found by Andrew Krapivin, \ an undergraduate, \ while reading about tiny pointers", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Even hash tables still hold surprises. <bookmark mark='a'/> Suppose a table never moves a key once "
            "placed, and only a fraction delta of its slots is free. In 1985 Andrew Yao conjectured that the best "
            "one can do is to probe random slots, which costs about one over delta probes per insert. <bookmark "
            "mark='b'/> Our double-hashing table follows that curve as it fills. <bookmark mark='c'/> In 2025 "
            "Martín Farach-Colton, Andrew Krapivin and William Kuszmaul refuted the conjecture. Their funnel "
            "hashing needs only order log squared of one over delta probes, and they proved that optimal for its "
            "class. <bookmark mark='d'/> Their elastic hashing does even better: a constant on average, and log "
            "of one over delta in the worst case, still without moving any key. <bookmark mark='e'/> Krapivin "
            "found the idea as an undergraduate, while reading a paper on tiny pointers."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(meas), Create(yao_), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(funnel), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def optimality(self):
        head = label(r"Is there a best binary search tree?", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{dynamic optimality} \ (Sleator and Tarjan, \ 1985): \ splay trees are within $O(1)$ of "
                  r"the best BST algorithm, \ on every sequence", font_size=21, color=HEAD),
            label(r"proved: \ splay trees are $O(\log n)$-competitive \ (trivially) \ and satisfy the working-set, \ "
                  r"static-finger and sequential-access theorems", font_size=21, color=GREY_A),
            label(r"Tango trees \ (Demaine, \ Harmon, \ Iacono and P\u{a}tra\c{s}cu, \ 2004): \ $O(\log \log n)$-"
                  r"competitive, \ the best known", font_size=21, color=YES),
            label(r"a geometric view \ (2009): \ a BST execution is a set of points with no empty rectangles; \ "
                  r"\textsc{Greedy} may be optimal too", font_size=21, color=LAM),
            label(r"the conjecture has resisted forty years of attack", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The splay tree's conjecture is the other great open question of this part. <bookmark mark='a'/> "
            "Dynamic optimality says that on every access sequence, a splay tree is within a constant factor of "
            "the best possible binary search tree algorithm, even one that knows the whole sequence in advance. "
            "<bookmark mark='b'/> Many consequences are proved: the working-set theorem, the static-finger "
            "theorem, sequential access in linear time. <bookmark mark='c'/> The best competitive ratio known for "
            "any tree is log log n, from Erik Demaine, Dion Harmon, John Iacono and Mihai Pătraşcu's tango trees. "
            "<bookmark mark='d'/> A geometric reformulation turns every execution into a set of points in which no "
            "rectangle is empty, and suggests a simple greedy algorithm that may be optimal as well. <bookmark "
            "mark='e'/> The conjecture itself has resisted forty years of attack."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def learned(self):
        head = label(r"Lower bounds, \ and learning the data", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{cell-probe lower bounds}: \ the exact time--space trade-off for predecessor search \ "
                  r"(P\u{a}tra\c{s}cu and Thorup, \ 2006)", font_size=21, color=GREY_A),
            label(r"dynamic problems: \ $\Omega(\log n)$ per operation for partial sums \ (P\u{a}tra\c{s}cu and "
                  r"Demaine, \ 2004)", font_size=21, color=GREY_A),
            label(r"\textbf{learned indexes} \ (Kraska et al., \ 2018): \ a model of the keys' distribution "
                  r"predicts where a key is", font_size=21, color=YES),
            label(r"a B-tree is a model too, \ of a step function; \ fitting the real distribution can be smaller "
                  r"and faster", font_size=21, color=YES),
            label(r"open: \ guarantees for learned structures, \ and which distributions they help", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Two more directions are active. <bookmark mark='a'/> Lower bounds. In the cell-probe model of Part "
            "16, Mihai Pătraşcu and Mikkel Thorup pinned down exactly how fast predecessor search can be in a given "
            "amount of space, <bookmark mark='b'/> and Pătraşcu and Erik Demaine proved that maintaining partial "
            "sums under updates needs logarithmic time per operation, the first such bound for a dynamic problem. "
            "<bookmark mark='c'/> And learning. Tim Kraska and colleagues observed in 2018 that an index is a "
            "model: given a key, it predicts a position. <bookmark mark='d'/> A B-tree models the keys as a step "
            "function; a model fitted to the real distribution of keys can be smaller and faster. <bookmark "
            "mark='e'/> What such learned structures can guarantee, and for which data, is open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"is the splay tree dynamically optimal? \ is any BST $O(1)$-competitive?", font_size=24,
                  color=GREY_A),
            label(r"what is the exact cost of decrease-key in a pairing heap?", font_size=24, color=GREY_A),
            label(r"how few probes can a hash table use when nearly full, \ if elements may move?", font_size=24,
                  color=GREY_A),
            label(r"which learned data structures come with worst-case guarantees?", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> Is the splay tree dynamically optimal, and is "
            "any binary search tree? <bookmark mark='b'/> What exactly does decrease-key cost in a pairing heap? The "
            "answer is known to lie between log log n and something slightly larger. <bookmark mark='c'/> How few "
            "probes can a nearly full hash table use if it may move keys? <bookmark mark='d'/> And which learned "
            "structures can promise anything in the worst case? <bookmark mark='e'/> This part's research problem "
            "takes up the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
