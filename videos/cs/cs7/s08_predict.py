from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, PipeChart,
                                  box, fmt, load, mono)

SHORT = {"insertion sort": "sort", "sieve": "sieve", "threshold, random": "threshold (random)",
         "threshold, sorted": "threshold (sorted)", "Fibonacci (recursive)": "Fibonacci",
         "correlated branches": "correlated", "the Job, chapter 1": "the Job"}


def acc_table(pred, names, font_size=20, cw=1.45, rh=0.42, highlight=None):
    tab = pred["table"]
    progs = list(tab)
    g = VGroup()
    x0 = -4.6
    for j, n in enumerate(names):
        g.add(label(n, font_size=font_size - 2, color=GREY_B).move_to([x0 + 2.0 + j * cw, 0.45, 0]))
    for i, p in enumerate(progs):
        y = -i * rh
        g.add(label(SHORT[p], font_size=font_size, color=GREY_A).move_to([x0, y, 0], aligned_edge=RIGHT))
        for j, n in enumerate(names):
            a = tab[p]["rows"][n]["accuracy"]
            c = interpolate_color(ManimColor(NO), ManimColor(YES), max(0.0, min(1.0, (a - 0.5) / 0.5)))
            cell = VGroup(Rectangle(width=cw * 0.92, height=rh * 0.85, stroke_width=0, fill_color=c, fill_opacity=0.35),
                          label(rf"{100 * a:.1f}", font_size=font_size, color=WHITE))
            cell[1].move_to(cell[0])
            cell.move_to([x0 + 2.0 + j * cw, y, 0])
            g.add(cell)
    return g


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.static()
        self.counters()
        self.fsm()
        self.table()

    def card(self):
        card = chapter_card(7, r"Predicting branches", r"Can the past predict a branch?", lit=(1981,), extra=((1981, r"Smith's branch predictors"),), part=PART)
        with self.voiceover("Chapter seven. Predicting branches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def static(self):
        pr = load("predictors")["table"]
        head = label(r"Guesses that never learn", font_size=38).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"always not taken: \ what the pipeline did so far", font_size=26, color=GREY_A),
            label(r"always taken: \ right for loops", font_size=26, color=GREY_A),
            label(r"backward taken, \ forward not: \ loops close backwards, \ \texttt{if}s jump forwards", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 1.2)
        res = VGroup(
            label(rf"sort: \ backward-taken is right {100 * pr['insertion sort']['rows']['backward taken']['accuracy']:.0f}\% "
                  r"of the time", font_size=24, color=YES),
            label(rf"the Job: \ only {100 * pr['the Job, chapter 1']['rows']['backward taken']['accuracy']:.0f}\%: \ its "
                  r"hot branches are forward, \ and data-dependent", font_size=24, color=NO),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The simplest guesses are fixed rules. <bookmark mark='a'/> Predict not taken, which is what our pipeline "
            "has done so far. Predict always taken, which suits loops, since a loop's closing branch is taken every time "
            "but the last. Or the compromise many early machines used: a branch that jumps backwards is probably a loop, "
            "so predict taken; a branch that jumps forwards is probably an if, so predict not taken. "
            "<bookmark mark='b'/> On the insertion sort, backward-taken is right ninety-nine percent of the time. On the "
            "Job it is right only fifty-seven percent: its busiest branches jump forwards, and whether they are taken "
            "depends on the text. To do better, a predictor has to watch what each branch actually does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counters(self):
        head = label(r"Remember what each branch did \ (Smith, 1981)", font_size=34).to_edge(UP, buff=0.35)
        tab = VGroup()
        for k in range(8):
            r = Rectangle(width=1.0, height=0.42, stroke_color=GREY_C, stroke_width=1.2)
            t = MathTex(["1", "0", "1", "1", "0", "1", "1", "0"][k], font_size=24, color=YES)
            tab.add(VGroup(r, t.move_to(r)))
        tab.arrange(DOWN, buff=0.0).move_to(RIGHT * 2.8)
        tl = label(r"a table of bits, \\ indexed by low bits of \texttt{pc}", font_size=20, color=GREY_A).next_to(tab, UP,
                                                                                                         buff=0.15)
        pc = mono("pc = 0x0074", 22, DATA).move_to(LEFT * 3.6 + UP * 0.6)
        idx = MathTex(r"(\texttt{pc} \gg 2) \bmod 1024", font_size=28, color=GREY_A).next_to(pc, DOWN, buff=0.3)
        arr = Arrow(idx.get_right(), tab[5].get_left(), buff=0.15, color=HEAD)
        pred = label(r"predict: \ taken if the bit is 1; \\ when the branch resolves, \ write what it did", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In 1981 James Smith measured the obvious learning rule. <bookmark mark='a'/> Keep a small table of bits, "
            "indexed by the low bits of the branch's address. <bookmark mark='b'/> To predict, look up the branch's "
            "bit: one means it was taken last time, so predict taken again. When the branch resolves, write down what "
            "it actually did. The table is tiny and fast enough to consult in the fetch stage, alongside the "
            "instruction memory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(pc), FadeIn(idx), GrowArrow(arr), Indicate(tab[5], color=HEAD))
            self.play(FadeIn(pred))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fsm(self):
        f = load("predictors")
        pat = f["pattern"]
        head = label(r"A loop of ten: \ one bit against two", font_size=36).to_edge(UP, buff=0.3)
        names = [r"\text{strongly}\\\text{not}", r"\text{weakly}\\\text{not}", r"\text{weakly}\\\text{taken}",
                 r"\text{strongly}\\\text{taken}"]
        states = VGroup()
        for k, n in enumerate(names):
            c = Circle(radius=0.55, color=NO if k < 2 else YES, stroke_width=3, fill_color=BG, fill_opacity=1)
            parts = n.split(r"\\")
            t = VGroup(*[MathTex(p_, font_size=18, color=NO if k < 2 else YES) for p_ in parts]).arrange(DOWN, buff=0.04)
            t.move_to(c)
            states.add(VGroup(c, t))
        states.arrange(RIGHT, buff=0.9).move_to(UP * 1.4)
        arrows = VGroup()
        for k in range(3):
            arrows.add(CurvedArrow(states[k].get_top() + RIGHT * 0.2, states[k + 1].get_top() + LEFT * 0.2, angle=-0.8,
                                   color=YES, stroke_width=2))
            arrows.add(CurvedArrow(states[k + 1].get_bottom() + LEFT * 0.2, states[k].get_bottom() + RIGHT * 0.2,
                                   angle=-0.8, color=NO, stroke_width=2))
        tl = VGroup(label(r"taken", font_size=18, color=YES).next_to(arrows[2], UP, buff=0.05),
                    label(r"not taken", font_size=18, color=NO).next_to(arrows[3], DOWN, buff=0.05))
        fl = label(r"a saturating counter: \ Part 5's state machine, \ two flip-flops per branch", font_size=22,
                   color=GREY_B).next_to(states, DOWN, buff=0.9)
        # the run: outcomes and the two predictors' mistakes
        x0 = -5.6
        dx = 0.28
        row_o = VGroup(*[Square(0.22, stroke_width=0, fill_color=YES if t else NO, fill_opacity=0.8).move_to(
            [x0 + k * dx, -1.0, 0]) for k, t in enumerate(pat)])
        rows = {}
        for j, name in enumerate(("1-bit", "2-bit")):
            preds = f["fsm"][name]["predictions"]
            rows[name] = VGroup(*[Text("x", font_size=16, color=NO).move_to([x0 + k * dx, -1.55 - 0.5 * j, 0])
                                  if p_ != t else Dot([x0 + k * dx, -1.55 - 0.5 * j, 0], radius=0.03, color=GREY_D)
                                  for k, (p_, t) in enumerate(zip(preds, pat))])
        labs = VGroup(label(r"outcome", font_size=18, color=GREY_B).next_to(row_o, LEFT, buff=0.2),
                      label(r"1-bit", font_size=18, color=GREY_B).next_to(rows["1-bit"], LEFT, buff=0.2),
                      label(r"2-bit", font_size=18, color=GREY_B).next_to(rows["2-bit"], LEFT, buff=0.2))
        m1 = sum(p_ != t for p_, t in zip(f["fsm"]["1-bit"]["predictions"], pat))
        m2 = sum(p_ != t for p_, t in zip(f["fsm"]["2-bit"]["predictions"], pat))
        res = label(rf"wrong: \ 1-bit {m1} times, \ 2-bit {m2} \ in four trips round the loop", font_size=24,
                    color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "One bit has a flaw that shows up in every loop. <bookmark mark='a'/> Watch a loop that runs ten times: its "
            "branch is taken nine times, then not taken once, again and again. The one-bit predictor gets the last trip "
            "wrong, as anything would. But then it remembers not taken, so it also gets the first trip of the next "
            "loop wrong: two mistakes per loop. <bookmark mark='b'/> The fix is hysteresis. Give each branch a two-bit "
            "saturating counter, a four-state machine of the kind Part 5 built: taken moves it right, not taken moves "
            "it left, and it predicts taken in the right-hand two states. A single surprise only moves it from "
            "strongly to weakly taken, so the prediction does not change. <bookmark mark='c'/> On the loop, the two-bit "
            "counter makes one mistake per loop instead of two. Two bits per branch became the standard for a decade."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(labs), LaggedStart(*[FadeIn(r) for r in row_o], lag_ratio=0.02), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(r) for r in rows["1-bit"]], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(states), Create(arrows), FadeIn(tl), FadeIn(fl), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows["2-bit"]], lag_ratio=0.02), run_time=1.5)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        pr = load("predictors")
        head = label(r"Percent predicted correctly", font_size=36).to_edge(UP, buff=0.35)
        tab = acc_table(pr, ["always taken", "backward taken", "1-bit", "2-bit"], font_size=20, cw=1.9).move_to(
            DOWN * 0.1 + RIGHT * 0.6)
        notes = label(r"learning wins on loops and on sorted data; \ on the Job, \ Fibonacci \ and the correlated "
                      r"benchmark \\ a branch's own history is not enough", font_size=22, color=HEAD).to_edge(DOWN,
                                                                                                buff=0.35)
        with self.voiceover(
            "Here are these four predictors on the benchmarks, each trained as it goes over the program's real branch "
            "trace. <bookmark mark='a'/> Counters beat fixed rules almost everywhere, and the two-bit counter is never "
            "much worse than the one-bit one. The threshold loop is the interesting pair: the same code, right "
            "seventy-five percent of the time on random data and almost always on sorted data, a puzzle chapter "
            "fourteen returns to. <bookmark mark='b'/> But on the Job, on Fibonacci and on the correlated benchmark, a "
            "counter per branch stalls between fifty and ninety-one percent. For those branches, the branch's own past "
            "says little. The next chapter looks at the past of the other branches."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()
