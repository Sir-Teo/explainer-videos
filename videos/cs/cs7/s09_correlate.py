from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)
from videos.cs.cs7.s08_predict import acc_table


class Correlate(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.gshare()
        self.tage()
        self.perceptron()
        self.heatmap()
        self.table()

    def card(self):
        card = chapter_card(8, r"Correlation, \ and a perceptron", r"Can other branches predict this one?",
                            lit=(1991, 1993, 2001, 2006), extra=((1991, r"two-level prediction"), (1993, r"gshare"), (2001, r"the perceptron predictor"), (2006, r"TAGE")), part=PART)
        with self.voiceover("Chapter eight. Correlation, and a perceptron."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"Branches talk to each other", font_size=38).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 21) for t in ("if (x == 0) a = 1;        // branch A",
                                              "if (y == 0) b = 1;        // branch B",
                                              "if (x == 0 && y == 0) ... // branch C: decided by A and B")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.4)
        ghr = VGroup(*[VGroup(Square(0.45, stroke_color=CLOCK, stroke_width=1.5),
                              MathTex(b, font_size=24, color=YES if b == "1" else NO))
                       for b in "1101001110"]).arrange(RIGHT, buff=0.04)
        for g in ghr:
            g[1].move_to(g[0])
        ghr.move_to(DOWN * 0.7)
        gl = label(r"the global history register: \ the last outcomes of \textit{all} branches, \ a shift register "
                   r"\ (Part 5)", font_size=22, color=CLOCK).next_to(ghr, DOWN, buff=0.25)
        ins = label(r"Yeh and Patt, \ 1991: \ two-level predictors, \ indexed by history", font_size=22,
                    color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A branch's own past is not the only clue. <bookmark mark='a'/> If the first two conditions here are "
            'known, the third is determined. A counter watching only the third branch does not directly observe that '
            "cross-branch information. <bookmark mark='b'/> Record recent outcomes in order in a global history shift "
            "register: one for taken, zero for not taken. <bookmark mark='c'/> Yeh and Patt's 1991 work demonstrated "
            'two-level adaptive prediction. Which information helps depends on the program, history representation, '
            'table sharing and training.'
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ghr), FadeIn(gl))
            new = VGroup(Square(0.45, stroke_color=CLOCK, stroke_width=1.5), MathTex("1", font_size=24, color=YES))
            new[1].move_to(new[0])
            new.next_to(ghr, LEFT, buff=0.04)
            self.play(FadeIn(new, shift=RIGHT * 0.3), ghr.animate.shift(RIGHT * 0.49), FadeOut(ghr[-1]))
            vo.wait_until("c")
            self.play(FadeIn(ins))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gshare(self):
        head = label(r"gshare and tournaments \ (McFarling, 1993)", font_size=34).to_edge(UP, buff=0.35)
        pc = mono("pc bits      0 1 1 0 1 0 0 1 1 0 1 1", 20, DATA)
        h = mono("history      1 1 0 1 0 0 1 1 1 0 0 1", 20, CLOCK)
        x = mono("xor  index   1 0 1 1 1 0 1 0 0 0 1 0", 20, HEAD)
        rows = VGroup(pc, h, x).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 1.5 + LEFT * 2.0)
        line = Line(rows[1].get_corner(DL) + DOWN * 0.05, rows[1].get_corner(DR) + DOWN * 0.05, color=GREY_C)
        tab = box(1.6, 2.2, r"\text{2-bit}\\\text{counters}", YES, 20).move_to(RIGHT * 3.6 + UP * 1.4)
        arr = Arrow(x.get_right(), tab.get_left(), buff=0.2, color=HEAD)
        tour = VGroup(
            label(r"gshare: \ one table of 2-bit counters, \ indexed by \texttt{pc} xor history: \\ one branch in "
                  r"different contexts gets different counters", font_size=22, color=GREY_A),
            label('our tournament: bimodal counters + gshare + chooser; \\\\ Alpha 21264 instead combined local-history and global-history predictors', font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Global history records recent branch outcomes. <bookmark mark='a'/> McFarling's gshare hashes that "
            "history with the branch address using exclusive-or, then selects a two-bit counter. Different contexts "
            "can select different counters; collisions can also make unrelated contexts share one. <bookmark "
            "mark='b'/> Our tournament chooses between a per-address bimodal counter table and gshare, using another "
            "table of counters. This illustrates adaptive choice. It is not a reproduction of Alpha 21264's historical "
            "local-history and global-history predictor: a per-address direction counter is simpler than a "
            "local-history predictor."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(Create(line), FadeIn(rows[2]))
            self.play(FadeIn(tab), GrowArrow(arr), FadeIn(tour[0]))
            vo.wait_until("b")
            self.play(FadeIn(tour[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tage(self):
        head = label(r"TAGE: \ geometric histories \ (Seznec and Michaud, 2006)", font_size=32).to_edge(UP, buff=0.35)
        lens = [0, 4, 8, 16, 32, 64]
        tabs = VGroup()
        for k, L in enumerate(lens):
            name = r"\text{base}" if L == 0 else rf"h = {L}"
            b = box(1.5, 1.2 + 0.18 * k, name, YES if L == 0 else FUNC, 22)
            tabs.add(b)
        tabs.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to(UP * 0.8)
        tags = label(r"each tagged table is indexed by the \texttt{pc} and a longer slice of history: \ 4, 8, 16, 32, 64 "
                     r"outcomes", font_size=22, color=GREY_A).next_to(tabs, DOWN, buff=0.4)
        rule = VGroup(
            label(r"the longest history whose tag matches makes the prediction", font_size=24, color=HEAD),
            label(r"on a mistake, \ allocate an entry with a longer history; \ useful bits decide what may be evicted",
                  font_size=22, color=GREY_A),
            label('TAGE is influential; our simplified implementation is not a commercial predictor',
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Different branches benefit from different history lengths. <bookmark mark='a'/> Seznec and Michaud's TAGE "
            "combines a base predictor with partially tagged components using geometrically spaced histories. Our "
            "simplified version uses four through sixty-four outcomes. <bookmark mark='b'/> It selects the longest "
            "matching tag and allocates longer-history entries after some misses. Partial tags can alias, capacity is "
            "finite, and allocation does not guarantee exactly the minimum history a branch needs. Full designs add "
            "confidence, alternate-provider and replacement policies. <bookmark mark='c'/> TAGE and its descendants "
            "are influential competition and processor designs. We will compare our small implementation, keeping its "
            "results distinct from commercial predictors and the full published algorithms."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tabs], lag_ratio=0.25), FadeIn(tags),
                      run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(rule[0]), Indicate(tabs[4], color=HEAD))
            self.play(FadeIn(rule[1]))
            vo.wait_until("c")
            self.play(FadeIn(rule[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def perceptron(self):
        head = label(r"A neural network inside the CPU \ (Jiménez and Lin, 2001)", font_size=32).to_edge(UP, buff=0.35)
        xs = VGroup(*[Circle(radius=0.22, color=CLOCK, stroke_width=2).move_to([-5.0, 1.7 - 0.55 * k, 0])
                      for k in range(7)])
        xl = VGroup(*[MathTex(t, font_size=22, color=CLOCK).move_to(c) for t, c in
                      zip([r"1", r"x_1", r"x_2", r"x_3", r"\vdots", r"x_{h-1}", r"x_h"], xs)])
        y = Circle(radius=0.45, color=HEAD, stroke_width=3).move_to(LEFT * 1.4 + DOWN * 0.0)
        yl = MathTex(r"\Sigma", font_size=40, color=HEAD).move_to(y)
        ws = VGroup(*[Line(c.get_right(), y.get_left(), color=FUNC, stroke_width=1.5 + 2 * abs(np.sin(k * 1.7)))
                      for k, c in enumerate(xs)])
        out = Arrow(y.get_right(), y.get_right() + RIGHT * 1.0, buff=0, color=HEAD)
        eqs = VGroup(
            MathTex(r"y = w_0 + \sum_{i=1}^{h} w_i\,x_i", font_size=36, color=CODE),
            MathTex(r"x_i = +1 \text{ if the } i\text{th last branch was taken, } -1 \text{ if not}", font_size=26,
                    color=GREY_A),
            MathTex(r"\text{predict taken} \iff y \ge 0", font_size=32, color=HEAD),
            MathTex(r"\text{wrong, or } |y| \le \theta: \quad w_i \leftarrow w_i + t\,x_i", font_size=30, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.3)
        note = label(r"\textit{AI, Built}'s first learning machine, \ Rosenblatt's perceptron (1958), \ in hardware: \\ "
                     r"one per table entry, \ a few hundred bytes of weights, \ answering in a cycle", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Jimenez and Lin proposed perceptron branch prediction in 2001. <bookmark mark='a'/> Represent each of the "
            "last h outcomes as plus one or minus one. A hash of the branch address selects a weight vector, so "
            "different branches can share and interfere with the same weights. <bookmark mark='b'/> Add a bias and the "
            "weighted inputs; a nonnegative sum predicts taken. <bookmark mark='c'/> When wrong or insufficiently "
            "confident, adjust weights toward the observed outcome. The heatmap next shows the weights this rule "
            "learns. <bookmark mark='d'/> Parameter count grows linearly with history length, unlike a fully "
            "enumerated context table. That comparison does not cover every table-based scheme. Perceptron-derived "
            "predictors have appeared in real products, as Jimenez's 2016 paper notes; the exact predictor in an "
            "unknown viewing device cannot be assumed."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(xs), FadeIn(xl))
            vo.wait_until("b")
            self.play(Create(ws), FadeIn(y), FadeIn(yl), GrowArrow(out), FadeIn(eqs[0]), FadeIn(eqs[1]))
            self.play(FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[3]))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heatmap(self):
        pc = load("perceptron")
        head = label(r"What the perceptron learned", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        order = ["correlated branches", "the Job, chapter 1", "insertion sort"]
        for k, name in enumerate(order):
            d = pc[name]
            w = np.array(d["weights"], float)
            m = max(1.0, np.abs(w).max())
            cells = VGroup()
            for i, v in enumerate(w):
                c = interpolate_color(ManimColor(BG), ManimColor(YES if v > 0 else NO), min(1.0, abs(v) / m))
                cells.add(Square(0.36, stroke_width=0.5, stroke_color=GREY_D, fill_color=c, fill_opacity=1))
            cells.arrange(RIGHT, buff=0.02)
            lab = VGroup(label(rf"\textit{{{name}}}", font_size=20, color=GREY_A),
                         Text(d["text"], font="DejaVu Sans Mono", font_size=14, color=CODE)).arrange(DOWN, buff=0.05,
                                                                                                    aligned_edge=RIGHT)
            acc = label(rf"perceptron {100 * d['perceptron']:.1f}\% \ $|$ \ 2-bit {100 * d['two_bit']:.1f}\%",
                        font_size=18, color=HEAD)
            row = VGroup(lab, cells, acc)
            lab.next_to(cells, LEFT, buff=0.3)
            acc.next_to(cells, RIGHT, buff=0.3)
            row.move_to(UP * (1.5 - 1.25 * k))
            rows.add(row)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.3)
        axis = VGroup(*[Text(str(i), font_size=12, color=GREY_C).next_to(rows[-1][1][i], DOWN, buff=0.08)
                        for i in range(0, len(rows[-1][1]), 4)])
        al = label(r"bias, \ then the 1st, 2nd, \ldots \ most recent branch", font_size=18, color=GREY_B).next_to(
            rows[-1][1], DOWN, buff=0.4)
        key = label(r"green: \ ``agrees with this branch''; \ red: \ ``disagrees''", font_size=20,
                    color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Because a perceptron's knowledge is a row of weights, we can look at what it learned. Each row here is one "
            "branch: the bias weight, then one weight for each of the last sixteen branch outcomes, most recent first. "
            "<bookmark mark='a'/> The correlated benchmark was built so that branch B repeats the outcome of branch A, "
            "four branches earlier, with three random branches in between. The perceptron found it: one bright weight "
            "at position four, almost nothing elsewhere, and B predicted almost perfectly, where a two-bit counter manages a coin "
            "toss. <bookmark mark='b'/> The Job's scan branch, the test for a table entry of the wrong length, has a "
            "messier pattern: its outcome depends on the lengths of words in the table, and some of that shows up in "
            "the recent history. <bookmark mark='c'/> The insertion sort's comparison alternates with its loop branch, "
            "and the weights alternate too."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rows[0]), FadeIn(axis), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(key))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        pr = load("predictors")
        head = label(r"All the predictors, \ every benchmark", font_size=36).to_edge(UP, buff=0.35)
        tab = acc_table(pr, ["2-bit", "gshare", "tournament", "TAGE", "perceptron"], font_size=19, cw=1.55).move_to(
            DOWN * 0.1 + RIGHT * 0.9)
        job = pr["table"]["the Job, chapter 1"]["rows"]
        notes = label(rf"the Job: \ {100 * job['2-bit']['accuracy']:.1f}\% $\to$ {100 * job['TAGE']['accuracy']:.1f}\%: "
                      rf"\ mispredictions per thousand instructions \ {job['2-bit']['mpki']:.0f} $\to$ "
                      rf"{job['TAGE']['mpki']:.0f}", font_size=22, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Compare the learning predictors on these traces. <bookmark mark='a'/> Global information helps Fibonacci "
            "and the correlated benchmark, but the latter uses fixed-seed pseudorandom data, not genuine independent "
            "coin flips. Its observed accuracy is not an information-theoretic ceiling. <bookmark mark='b'/> Our TAGE "
            "is best on the shown Job trace and reduces misses relative to the two-bit predictor. Different data and "
            "budgets can change that ranking. The irregular threshold stream is difficult for these online predictors; "
            "that does not prove that no predictor with other information could learn it."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(tab, lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()
