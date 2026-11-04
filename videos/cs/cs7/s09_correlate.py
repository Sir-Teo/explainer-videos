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
            "A branch's own past is not the only clue. <bookmark mark='a'/> Branches in a program are often related. "
            "If the first two branches here go one way, the third is already decided. A predictor that watches only "
            "the third branch will never see that. <bookmark mark='b'/> So keep a record of the last few outcomes of "
            "every branch, in order: a global history register, which is simply Part 5's shift register, shifting in a "
            "one for each taken branch and a zero for each not taken. <bookmark mark='c'/> Tse-Yu Yeh and Yale Patt "
            "showed in 1991 that tables indexed by this history predict far better: two-level adaptive prediction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
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
            label(r"tournament: \ a local predictor and gshare side by side, \\ and a chooser, \ itself 2-bit counters, "
                  r"\ learning which to trust for each branch \ (the Alpha 21264, \ 1998)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Scott McFarling turned this into two designs that dominated the 1990s. <bookmark mark='a'/> gshare mixes "
            "the branch's address with the global history by an exclusive-or, and uses the result to pick a two-bit "
            "counter. The same branch, reached by different paths through the program, gets different counters, each "
            "learning what the branch does in that context. <bookmark mark='b'/> And since some branches are best "
            "predicted by their own history and others by the global one, a tournament predictor runs both and a third "
            "table of counters learns, branch by branch, which predictor to believe. Digital's Alpha 21264 shipped one "
            "in 1998."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
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
            label(r"its descendants have won most branch prediction championships since, \ and run in most high-end cores",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How long a history should a predictor use? Short ones learn quickly; long ones capture distant "
            "correlations but need far more table entries. <bookmark mark='a'/> André Seznec and Pierre Michaud's TAGE "
            "uses all of them. A plain table of counters is the base, and beside it sit tagged tables indexed with "
            "histories of geometrically growing length: four, eight, sixteen, thirty-two, sixty-four outcomes. "
            "<bookmark mark='b'/> The prediction comes from the longest history whose tag matches, and a table entry is "
            "only allocated for a branch that a shorter history got wrong. Each branch ends up using exactly as much "
            "history as it needs. <bookmark mark='c'/> TAGE and its descendants have won the branch prediction "
            "championships since 2006, and some form of it predicts the branches in most high-performance processors "
            "today. Pebble's library has a small one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
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
            "In 2001 Daniel Jiménez and Calvin Lin asked whether a branch predictor could simply learn, the way a "
            "neural network does. <bookmark mark='a'/> Their predictor is a perceptron, the oldest neural network, the "
            "one AI, Built began with. Its inputs are the last h branch outcomes, written as plus one for taken and "
            "minus one for not, and each branch has its own weights. <bookmark mark='b'/> The output y is the weighted "
            "sum, and the prediction is taken when y is not negative. <bookmark mark='c'/> Training is Rosenblatt's "
            "rule: when the prediction was wrong, or right but not confidently, add the outcome times each input to its "
            "weight. A history position that agrees with the branch gains weight; one that does not, loses it. "
            "<bookmark mark='d'/> Because the weights grow linearly with h, a perceptron can use histories of thirty or "
            "sixty branches where a table would need astronomically many entries. AMD's Zen processors use a perceptron "
            "in their branch prediction. There is a neural network in the processor you are watching this on, and it "
            "is learning your programs' branches."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
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
            vo.wait_until("a")
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
            "Here are the learning predictors side by side. <bookmark mark='a'/> Global history transforms Fibonacci, "
            "whose branches depend on the depth of the recursion, and the correlated benchmark, where the perceptron "
            "and TAGE come close to the best possible, since four of its six branches are genuinely random. "
            "<bookmark mark='b'/> On the Job, TAGE is best, cutting the mispredictions per thousand instructions by a "
            "third compared with two-bit counters. No predictor can do much with a branch that depends on random data, "
            "as the threshold loop shows, and that is the subject of chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()
