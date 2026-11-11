from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Matching(VoiceoverScene):
    def construct(self):
        self.card()
        self.asflow()
        self.stable()
        self.measured()

    def card(self):
        card = chapter_card(12, r"Matching", r"Who goes with whom, \ and will they stay?", lit=(1962,),
                            extra=((1935, r"Hall's theorem"), (1962, r"Gale and Shapley")), part=PART)
        with self.voiceover("Chapter twelve. Matching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def asflow(self):
        head = label(r"Bipartite matching is a flow", font_size=34).to_edge(UP, buff=0.3)
        L = [Dot([-4.3, 1.5 - 1.0 * i, 0], radius=0.12, color=DATA) for i in range(4)]
        R = [Dot([-2.2, 1.5 - 1.0 * i, 0], radius=0.12, color=LAM) for i in range(4)]
        s = Dot([-6.0, 0.0, 0], radius=0.12, color=WHITE)
        t = Dot([-0.5, 0.0, 0], radius=0.12, color=WHITE)
        pairs = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2), (3, 2), (3, 3)]
        mid = VGroup(*[Line(L[a].get_center(), R[b].get_center(), color=GREY_B, stroke_width=1.6) for a, b in pairs])
        src = VGroup(*[Line(s.get_center(), x.get_center(), color=GREY_D, stroke_width=1.2) for x in L])
        snk = VGroup(*[Line(x.get_center(), t.get_center(), color=GREY_D, stroke_width=1.2) for x in R])
        chosen = VGroup(*[Line(L[a].get_center(), R[b].get_center(), color=YES, stroke_width=5) for a, b in
                          ((0, 1), (1, 0), (2, 2), (3, 3))])
        sl, tl = mono("s", 20, WHITE).next_to(s, LEFT, buff=0.1), mono("t", 20, WHITE).next_to(t, RIGHT, buff=0.1)
        pts = VGroup(
            label(r"workers on the left, \ jobs on the right, \\ an edge when a worker can do a job", font_size=21,
                  color=GREY_A),
            label(r"capacity 1 everywhere: \\ an integer max flow \textbf{is} a maximum matching", font_size=21,
                  color=YES),
            label(r"\textbf{Hall} \ (1935): \ everyone can be matched \ $\iff$ \\ every group of $k$ workers can do at "
                  r"least $k$ jobs", font_size=20, color=HEAD),
            label(r"K\H{o}nig \ (1931): \ max matching $=$ min vertex cover: \\ the min cut, \ in disguise", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if pts.width > 6.2:
            pts.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Flows solve matching. <bookmark mark='a'/> Put workers on the left and jobs on the right, with an edge "
            "whenever a worker can do a job, and ask for as many worker–job pairs as possible, no one used twice. "
            "<bookmark mark='b'/> Add a source feeding every worker and a sink fed by every job, give every pipe "
            "capacity one, and a maximum integer flow is exactly a maximum matching. <bookmark mark='c'/> The "
            "min-cut side says when everyone can be matched: Philip Hall's theorem, that every group of k workers "
            "must between them be able to do at least k jobs. <bookmark mark='d'/> And Dénes Kőnig's theorem, that "
            "the largest matching equals the smallest set of vertices touching every edge, is the max-flow "
            "min-cut theorem again."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(x) for x in L + R], Create(mid))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(s), FadeIn(t), FadeIn(sl), FadeIn(tl), Create(src), Create(snk), FadeIn(pts[1]))
            self.play(Create(chosen))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def stable(self):
        d = load("matching")
        head = label(r"Stable matching \ (Gale and Shapley, \ 1962)", font_size=34).to_edge(UP, buff=0.3)
        n = 4
        P, R = d["P"], d["R"]
        Pl = VGroup(*[VGroup(mono(f"P{i}", 20, DATA), mono(" ".join(f"R{j}" for j in P[i]), 15, GREY_B)).arrange(
            RIGHT, buff=0.3) for i in range(n)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.6)
        Rl = VGroup(*[VGroup(mono(f"R{i}", 20, LAM), mono(" ".join(f"P{j}" for j in R[i]), 15, GREY_B)).arrange(
            RIGHT, buff=0.3) for i in range(n)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(Pl, RIGHT,
                                                                                                  buff=1.5)
        cap = VGroup(label(r"proposers, \ with their preferences", font_size=17, color=GREY_B).next_to(Pl, UP, buff=0.2),
                     label(r"receivers, \ with theirs", font_size=17, color=GREY_B).next_to(Rl, UP, buff=0.2))
        lines = VGroup()
        for p, r in d["match"].items():
            lines.add(Line(Pl[int(p)].get_right() + RIGHT * 0.1, Rl[r][0].get_left() + LEFT * 0.1, color=YES,
                           stroke_width=3))
        steps = VGroup(
            label(r"each free proposer proposes \\ to the best receiver not yet tried", font_size=20, color=GREY_A),
            label(r"each receiver keeps the best offer so far, \\ and drops the rest", font_size=20, color=GREY_A),
            label(rf"here: \ {d['proposals']} proposals, \\ and no pair would both rather be together: \ "
                  r"\textbf{stable}", font_size=20, color=YES),
            label(r"always stable, \\ and the best stable matching for every proposer", font_size=20, color=HEAD),
            label(r"the US residency match \ (Roth and Peranson, \ 1999); \\ Nobel prize in economics, \ 2012",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if steps.width > 5.4:
            steps.scale_to_fit_width(5.4).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Stable matching is a preference problem, not minimum-cost assignment. Assume equally sized "
            "sides with strict, complete preference lists. <bookmark mark='a'/> Each free proposer tries "
            "the best receiver not yet approached. <bookmark mark='b'/> Receivers keep their best offer "
            "so far and reject the rest. <bookmark mark='c'/> At termination everyone is matched and no "
            "pair prefers each other to their current partners. The example's proposal count is computed "
            "from these lists. <bookmark mark='d'/> A proposer who prefers another receiver must already "
            "have tried that receiver and been rejected; that receiver's held partner only improves. This"
            " rules out a blocking pair. The resulting stable matching is optimal for proposers among "
            "stable matchings, not among every conceivable assignment. <bookmark mark='e'/> Deferred "
            "acceptance influenced residency-market design, but actual residency systems add capacities, "
            "couples and other rules beyond this simple model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(Pl), FadeIn(Rl), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(Create(lines), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("matching")
        head = label(r"How many proposals?", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['proposals']:,.0f}", f"{r['nHn']:,.0f}", words(r["worst"])] for r in d["rows"]]
        tab = grid_table([r"$n$ each side", r"proposals, \ random preferences", r"$n H_n \approx n \ln n$",
                          r"worst case $n^2$"], rows, widths=[2.4, 4.0, 3.0, 2.6], row_h=0.5, font_size=20,
                         colors=[[WHITE, YES, HEAD, NO]] * len(rows)).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label("five independent seeds per size; \\ $nH_n$ is a scale reference, \\ not an exact finite expectation",
                  font_size=21, color=GREY_A),
            label(rf"the \textbf{{assignment problem}}, \ with costs: \ the Hungarian algorithm \ (Kuhn, \ 1955), \ "
                  rf"$O(n^3)$: \\ {d['hungarian_n']} $\times$ {d['hungarian_n']} in "
                  rf"{1000 * d['hungarian_s']:.0f} ms (one observed solve), \\ total {d['hungarian_total']} against greedy's "
                  rf"{d['greedy_total']}", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Count proposals before drawing conclusions. <bookmark mark='a'/> We generate independent "
            "uniform complete preference permutations on both sides, use five fixed seeds per size and "
            "verify stability even at size one thousand. The table reports the sample mean. The n times "
            "harmonic-number column is an order n log n scale reference, not an exact finite expectation "
            "for this experiment. <bookmark mark='b'/> Minimum-cost assignment is different. On our fixed"
            " sixty-by-sixty cost matrix, the Hungarian algorithm returns a checked permutation and "
            "total, compared with a row-wise greedy assignment. Cubic complexity describes growth; this "
            "one matrix does not establish a universal timing or quality ratio."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()
