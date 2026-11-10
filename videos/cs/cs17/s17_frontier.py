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
        head = label(r"Nearly full hashing: \ experiment and theorem have different models", font_size=31).to_edge(UP, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[0, 2.15, 0.5], y_range=[0, 2.15, 0.5], x_length=5.5, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.05)
        xs = [np.log10(1 / r["delta"]) for r in rows]
        def line(key, col, dashed=False):
            pts = [ax.c2p(x, np.log10(r[key])) for x, r in zip(xs, rows)]
            curve = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
            return DashedVMobject(curve, num_dashes=24).set_color(col) if dashed else VGroup(curve, *[Dot(p, radius=0.05, color=col) for p in pts])
        measured = line("measured", DATA)
        expected = line("finite_expectation", HEAD, True)
        xt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v, t in ((0.30103, r"$1/2$"), (1, r"$1/10$"), (2, r"$1/100$"))])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "1"), (1, "10"), (2, "100"))])
        xl = label(r"free fraction $\delta$ \ (log scale)", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.12)
        yl = label(r"probes to first empty slot \ (log scale)", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        experiment = VGroup(
            label(r"fixed occupancy; \ fresh uniform permutation per trial", font_size=19, color=DATA),
            MathTex(r"\mathbb E[P]=\frac{m+1}{f+1},\quad f=m\delta", font_size=29, color=HEAD),
            label(r"8,192 slots; \ 5,000 independent trials per point", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(xl, DOWN, buff=0.22)
        theorem = VGroup(
            label(r"2025: \ no reordering, \ per-key random probe sequences", font_size=20, color=LAM),
            label(r"funnel: \ $O(\log^2(1/\delta))$ worst-case expected query/insert", font_size=19, color=YES),
            label(r"elastic: \ $O(1)$ amortized expected positive-query probes", font_size=19, color=YES),
            label(r"$O(\log(1/\delta))$ worst-case expected query/insert", font_size=19, color=YES),
            label(r"load-range and random-probing assumptions apply", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.19).move_to([3.6, 1.3, 0])
        if theorem.width > 6.1: theorem.scale_to_fit_width(6.1)
        recent = VGroup(
            label(r"2026 preprints: \ model choices matter", font_size=21, color=HEAD),
            label(r"full occupancy: \ non-oblivious hashing under hash assumptions", font_size=18, color=GREY_A),
            label(r"incremental insertion: \ constant expected bounds with reordering", font_size=18, color=GREY_A),
            label(r"braided cuckoo: \ $1-\varepsilon$ load, \ logarithmic in $1/\varepsilon$ with high probability", font_size=18, color=GREY_A),
            label(r"selected abstracts checked 10 Nov 2026; \ no implementations benchmarked", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -1.15, 0])
        if recent.width > 6.1: recent.scale_to_fit_width(6.1)
        note = label(r"query probes count sequence position; \ "
                     r"bounds are not benchmark curves", font_size=17, color=GREY_B).move_to([3.6, -2.9, 0])
        if note.width > 6.1: note.scale_to_fit_width(6.1)
        with self.voiceover(
            "Nearly full hashing needs careful model choices. <bookmark mark='a'/> First, a finite "
            "experiment: hold occupancy fixed and probe a fresh uniform permutation until the first empty"
            " slot. With m slots and f free, the exact expected count is m plus one over f plus one. "
            "<bookmark mark='b'/> Five thousand independent trials per point follow that expectation. We "
            "do not average insertions taken at different loads, and double hashing is not this "
            "uniform-permutation model. <bookmark mark='c'/> The 2025 funnel and elastic hashing results "
            "use per-key random probe sequences without moving existing keys. Funnel achieves squared "
            "logarithmic worst-case expected query and insertion bounds. <bookmark mark='d'/> Elastic "
            "hashing gives constant amortized expected positive-query probes, plus logarithmic worst-case"
            " expected query and insertion bounds. These are expectation statements with load-range "
            "assumptions, not deterministic per-operation caps. <bookmark mark='e'/> Selected 2026 "
            "preprints explore full occupancy, reordering, and braided cuckoo hashing under other models."
            " We checked their stated claims, not every proof, and implemented none of those new schemes."
            " Their bounds belong on theorem cards, not as constant-free timing curves beside this "
            "experiment."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(experiment))
            vo.wait_until("a"); self.play(Create(expected))
            vo.wait_until("b"); self.play(Create(measured))
            vo.wait_until("c"); self.play(FadeIn(theorem[:2]))
            vo.wait_until("d"); self.play(FadeIn(theorem[2:]), FadeIn(note))
            vo.wait_until("e"); self.play(FadeIn(recent))
        self.wait(0.3)
        self.clear_scene()

    def optimality(self):
        head = label(r"Is there a best binary search tree?", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{dynamic optimality} \ (Sleator and Tarjan, \ 1985): \ splay trees are within $O(1)$ of "
                  r"the best BST algorithm, \ on every sequence", font_size=21, color=HEAD),
            label(r"proved locality theorems: \ working-set, \ "
                  r"static-finger and sequential-access theorems", font_size=21, color=GREY_A),
            label(r"Tango trees \ (Demaine, \ Harmon, \ Iacono and P\u{a}tra\c{s}cu, \ 2004): \ $O(\log \log n)$-"
                  r"competitive, \ a historical general-BST benchmark", font_size=21, color=YES),
            label(r"a geometric view \ (2009): \ BST executions correspond to arborally satisfied point sets; \ "
                  r"\textsc{Greedy} may be optimal too", font_size=21, color=LAM),
            label(r"2026 preprints: \ Splay $O(\log\log n\,(\log\log\log n)^2)$; \ Greedy $2^{O(\sqrt{\log\log n})}$ competitive", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Dynamic optimality remains a demanding sequence question. <bookmark mark='a'/> Can an online"
            " binary-search-tree algorithm stay within a constant factor of the best offline execution, "
            "under the same model and initialization convention? Splay and Greedy are central candidates."
            " <bookmark mark='b'/> Splay already has strong locality theorems; those do not establish "
            "constant competitiveness on every sequence. <bookmark mark='c'/> Tango's log-log competitive"
            " ratio is a historical benchmark for general trees. Selected 2026 preprints state improved "
            "sublogarithmic competitive bounds specifically for Splay and Greedy. We identify their "
            "preprint status and checked scope in the notes. <bookmark mark='d'/> The geometric view asks"
            " for arborally satisfied point sets, a precise rectangle condition, rather than saying every"
            " rectangle is nonempty. <bookmark mark='e'/> None of these selected statements resolves the "
            "constant-factor conjecture. This is a dated snapshot, not an exhaustive literature survey."
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
            label(r"dynamic partial sums: \ word-size-dependent update/query trade-offs (P\u{a}tra\c{s}cu and "
                  r"Demaine, \ 2004)", font_size=21, color=GREY_A),
            label(r"\textbf{learned indexes} \ (Kraska et al., \ 2018): \ a model of the keys' distribution "
                  r"predicts where a key is", font_size=21, color=YES),
            label(r"a B-tree is a model too, \ of a step function; \ fitting the real distribution can be smaller "
                  r"and faster", font_size=21, color=YES),
            label(r"which correction/update/distribution assumptions make learned indexes useful?", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Two directions sharpen the design questions. <bookmark mark='a'/> Cell-probe predecessor "
            "bounds depend on key universe, word size, available space and query model. <bookmark "
            "mark='b'/> Dynamic partial-sums lower bounds likewise relate update and query costs with "
            "explicit word-size and amortization assumptions. A bare logarithm per operation hides those "
            "trade-offs. <bookmark mark='c'/> Learned indexes predict a position from a model of the key "
            "distribution. <bookmark mark='d'/> A useful implementation also verifies or corrects that "
            "prediction, handles updates, and accounts for memory. Some data sets benefit; distribution "
            "shift and adversarial inputs can change the outcome. <bookmark mark='e'/> The research "
            "question is which complete guarantees a particular structure provides under a particular "
            "model, not whether learned structures have any guarantees at all."
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
            label(r"which pairing-heap variant and operation model?", font_size=24, color=GREY_A),
            label(r"high-load hashing: \ reordering, \ deletions, \ adaptivity, \ hash assumptions?", font_size=24,
                  color=GREY_A),
            label(r"which complete learned-index guarantees survive updates and distribution shift?", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Ask each open question with its model attached. <bookmark mark='a'/> Can Splay, Greedy, or "
            "any online BST achieve constant competitiveness? <bookmark mark='b'/> Which pairing-heap "
            "variant, operation set and pointer model are we analyzing? Bounds for different variants "
            "cannot be combined into one generic claim. <bookmark mark='c'/> For high-load hashing, does "
            "the model permit reordering, deletions, adaptive probes or special hash assumptions? Recent "
            "constant expected bounds make a blanket impossibility claim inappropriate. <bookmark "
            "mark='d'/> For learned indexes, what correction, update and distribution assumptions make "
            "the guarantees useful? <bookmark mark='e'/> The research exercise is an investigation plan. "
            "The notes do not contain a solution to dynamic optimality."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs[0]))
            vo.wait_until("a")
            self.play(Indicate(qs[0], color=HEAD, scale_factor=1.02), run_time=0.7)
            for mk, q in zip("bcd", qs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
