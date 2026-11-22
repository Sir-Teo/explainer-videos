from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import BG, DATA, HEAD, NO, PART, YES, chapter, load, mono

SHORT = {"insertion sort": "sort", "sieve": "sieve", "threshold, random": "threshold (random)",
         "threshold, sorted": "threshold (sorted)", "Fibonacci (recursive)": "Fibonacci",
         "correlated branches": "correlated", "the Job, chapter 1": "the Job"}


def acc_table(pred, names, font_size=22, cw=1.7, rh=0.5):
    tab = pred["table"]
    g, cells = VGroup(), VGroup()
    x0 = -4.4
    for j, n in enumerate(names):
        g.add(label(n, font_size=font_size - 2, color=GREY_B).move_to([x0 + 2.1 + j * cw, 0.55, 0]))
    for i, p in enumerate(tab):
        y = -i * rh
        g.add(label(SHORT[p], font_size=font_size, color=GREY_A).move_to([x0, y, 0], aligned_edge=RIGHT))
        for j, n in enumerate(names):
            a = tab[p]["rows"][n]["accuracy"]
            c = interpolate_color(ManimColor(NO), ManimColor(YES), max(0.0, min(1.0, (a - 0.5) / 0.5)))
            cell = VGroup(RoundedRectangle(width=cw * 0.92, height=rh * 0.86, corner_radius=0.06, stroke_width=0,
                                           fill_color=c, fill_opacity=0.4),
                          Text(f"{100 * a:.1f}", font="DejaVu Sans Mono", font_size=font_size - 2, color=WHITE))
            cell[1].move_to(cell[0])
            cell.move_to([x0 + 2.1 + j * cw, y, 0])
            cells.add(cell)
    return g, cells


class Predict(WatchScene):
    def construct(self):
        chapter(self, 7, r"Predicting branches", r"Can the past predict a branch?", lit=(1981,),
                extra=((1981, r"Smith's branch predictors"),))
        self.static()
        self.counters()
        self.fsm()
        self.table()

    # ------------------------------------------------------------------
    def static(self):
        pr = load("predictors")["table"]
        sort_bt = pr["insertion sort"]["rows"]["backward taken"]["accuracy"]
        job_bt = pr["the Job, chapter 1"]["rows"]["backward taken"]["accuracy"]
        # a loop closes backwards; an if jumps forwards
        code = VGroup(mono("loop:", 28, GREY_B), mono("    ...", 28), mono("    beq  t0, t1, skip", 28),
                      mono("    ...", 28), mono("skip:", 28, GREY_B), mono("    bne  a0, zero, loop", 28)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16).move_to(LEFT * 2.2)
        back = CurvedArrow(code[5].get_left() + LEFT * 0.15, code[0].get_left() + LEFT * 0.15, angle=-1.4,
                           color=YES, stroke_width=5)
        fwd = CurvedArrow(code[2].get_right() + RIGHT * 0.15, code[4].get_right() + RIGHT * 0.15, angle=-1.3,
                          color=NO, stroke_width=5)
        col = code.get_right()[0] + 1.7
        bl = label(r"backwards: \ a loop. \ Guess taken.", font_size=30, color=YES)
        bl.move_to([col + bl.width / 2, code[5].get_center()[1], 0])
        fl = label(r"forwards: \ an \texttt{if}. \ Guess not taken.", font_size=30, color=NO)
        fl.move_to([col + fl.width / 2, code[2].get_center()[1] + 0.2, 0])
        with self.voiceover(
            "The cheapest guess is a fixed rule. Early machines used this one. <bookmark mark='a'/> A branch that "
            "jumps backwards is probably closing a loop: guess taken. <bookmark mark='b'/> A branch that jumps "
            f"forwards is probably an if: guess not taken. On the insertion sort, that rule is right "
            f"{100 * sort_bt:.0f} percent of the time."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in code], lag_ratio=0.12), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(back), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(fwd), FadeIn(fl))
        grp = VGroup(code, back, fwd, bl, fl)
        card = self.predict(r"Backward-taken on the Job's branches: \ how often right?",
                            [rf"about {100 * sort_bt:.0f}\%, \ like the sort", rf"about {100 * job_bt:.0f}\%",
                             r"about 10\%"],
                            narration="And on the Job? Is it right about as often, near "
                                      f"{100 * job_bt:.0f} percent, or almost never?", room=grp)
        self.reveal(card, 1, narration=(
            f"{100 * job_bt:.0f} percent: barely better than a coin. The Job's busiest branches jump forwards, and "
            "which way they go depends on the text. To do better, a predictor has to watch each branch."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def counters(self):
        bits = [1, 0, 1, 1, 0, 1, 1, 0]
        tab = VGroup()
        for b in bits:
            r = Rectangle(width=1.1, height=0.48, stroke_color=GREY_C, stroke_width=1.4)
            t = Text(str(b), font="DejaVu Sans Mono", font_size=26, color=YES if b else NO).move_to(r)
            tab.add(VGroup(r, t))
        tab.arrange(DOWN, buff=0.0).move_to(RIGHT * 3.0)
        tl = label(r"one bit per branch, \\ indexed by its address", font_size=24, color=GREY_A).next_to(tab, UP,
                                                                                                   buff=0.2)
        pc = mono("pc = 0x0074", 28, DATA).move_to(LEFT * 3.8 + UP * 0.8)
        idx = MathTex(r"(\texttt{pc} \gg 2) \bmod 8 = 5", font_size=34, color=GREY_A).next_to(pc, DOWN, buff=0.35)
        arr = Arrow(idx.get_right(), tab[5].get_left(), buff=0.15, color=HEAD, stroke_width=4)
        guess = label(r"guess: \ taken", font_size=30, color=YES).next_to(idx, DOWN, buff=0.6)
        with self.voiceover(
            "In 1981 James Smith measured the obvious learning rule. <bookmark mark='a'/> Keep a small table of bits, "
            "indexed by the low bits of the branch's address. <bookmark mark='b'/> To predict, look the branch up: a "
            "one means it was taken last time, so guess taken again. <bookmark mark='c'/> When it resolves, write down "
            "what it actually did."
        ) as vo:
            self.play(LaggedStart(*[GrowFromEdge(c, LEFT) for c in tab], lag_ratio=0.08), FadeIn(tl), run_time=1.3)
            vo.wait_until("a")
            self.play(Write(pc))
            vo.wait_until("b")
            self.play(FadeIn(idx, shift=DOWN * 0.1), GrowArrow(arr))
            self.play(Indicate(tab[5], color=HEAD), FadeIn(guess, shift=UP * 0.1))
            vo.wait_until("c")
            new = Text("0", font="DejaVu Sans Mono", font_size=26, color=NO).move_to(tab[5][1])
            nl = label(r"it wasn't: \ write 0", font_size=30, color=NO).move_to(guess)
            self.play(Transform(tab[5][1], new), Transform(guess, nl), Flash(tab[5], color=NO))
        self.clear_scene()

    # ------------------------------------------------------------------
    def fsm(self):
        f = load("predictors")
        pat = [bool(x) for x in f["pattern"]]
        p1, p2 = f["fsm"]["1-bit"]["predictions"], f["fsm"]["2-bit"]["predictions"]
        s2 = f["fsm"]["2-bit"]["states"]
        names = [r"strongly\\not", r"weakly\\not", r"weakly\\taken", r"strongly\\taken"]
        states = VGroup()
        for k, n in enumerate(names):
            c = Circle(radius=0.62, color=NO if k < 2 else YES, stroke_width=3, fill_color=BG, fill_opacity=1)
            t = label(n, font_size=20, color=NO if k < 2 else YES).move_to(c)
            states.add(VGroup(c, t))
        states.arrange(RIGHT, buff=1.0).move_to(UP * 1.9 + LEFT * 1.3)
        arrows = VGroup()
        for k in range(3):
            arrows.add(CurvedArrow(states[k].get_top() + RIGHT * 0.25, states[k + 1].get_top() + LEFT * 0.25,
                                   angle=-0.8, color=YES, stroke_width=2.5))
            arrows.add(CurvedArrow(states[k + 1].get_bottom() + LEFT * 0.25, states[k].get_bottom() + RIGHT * 0.25,
                                   angle=-0.8, color=NO, stroke_width=2.5))
        rows = [[(YES if t else NO, None) for t in pat],
                [((NO, "x") if a != t else (GREY_E, None)) for a, t in zip(p1, pat)],
                [((NO, "x") if a != t else (GREY_E, None)) for a, t in zip(p2, pat)]]
        strip = EventStrip(rows, names=[r"outcome", r"1-bit", r"2-bit"], window=len(pat), cell=0.27, gap=0.04)
        strip.move_to(DOWN * 1.4 + RIGHT * 0.5)
        m1 = np.concatenate([[0], np.cumsum([a != t for a, t in zip(p1, pat)])])
        m2 = np.concatenate([[0], np.cumsum([a != t for a, t in zip(p2, pat)])])
        meters = VGroup(Meter(r"1-bit misses", strip.t, values=m1, fmt="{:.0f}", color=NO, font_size=26),
                        Meter(r"2-bit misses", strip.t, values=m2, fmt="{:.0f}", color=YES, font_size=26)).arrange(
            RIGHT, buff=1.2).to_edge(DOWN, buff=0.35)
        token = always_redraw(lambda: Dot(states[s2[min(len(s2) - 1, max(0, int(strip.t.get_value()) - 1))]][0]
                                          .get_top() + DOWN * 0.18, color=HEAD, radius=0.09))
        with self.voiceover(
            "A loop that runs ten times shows the flaw. <bookmark mark='a'/> Its branch is taken nine times, then not. "
            "A one-bit table flips on the exit, so it misses the exit, and then misses again when the loop restarts."
        ) as vo:
            self.play(FadeIn(strip.labels), FadeIn(meters))
            self.add(strip)
            vo.wait_until("a")
            strip.advance(self, 11, per_step=0.3)
        card = self.predict(r"Four trips round a ten-iteration loop. \\ Which predictor misses less?",
                            [r"one bit", r"two bits", r"they tie"],
                            narration="Smith's fix was a second bit: a counter that needs two surprises in a row to "
                                      "change its mind. Over four trips round the loop, which misses less?",
                            where="right")
        self.park(card)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in states], lag_ratio=0.2), Create(arrows), run_time=1.4)
        self.add(token)
        with self.voiceover(
            "Watch the yellow dot. It sits at strongly taken. The exit nudges it to weakly taken, not across, so the "
            "restart is still guessed right."
        ):
            strip.advance(self, 12, per_step=0.25)
        strip.advance(self, len(pat) - 23, per_step=0.16)
        self.reveal(card, 1, narration=(
            f"Two bits: {int(m2[-1])} misses against {int(m1[-1])}, startup included. It misses the exits, and only "
            "the exits."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        pr = load("predictors")
        names = ["always taken", "backward taken", "1-bit", "2-bit"]
        g, cells = acc_table(pr, names)
        VGroup(g, cells).move_to(DOWN * 0.1 + RIGHT * 0.6)
        src = tag("simulated", r"online, over each program's full trace").to_corner(DR, buff=0.3)
        hard = [k for k in range(len(cells)) if k % 4 == 3]
        with self.voiceover(
            "Here are all seven programs, percent predicted correctly. <bookmark mark='a'/> Two bits are a big step "
            "up from fixed rules. <bookmark mark='b'/> But look at the threshold loop on random data and the "
            "Fibonacci recursion: a counter per branch remembers only which way it usually goes. To do better, it "
            "has to know what happened just before."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(cells[k], color=YES, scale_factor=1.05) for k in hard], run_time=1.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(cells[2 * 4 + 3], cells[4 * 4 + 3]), color=NO, scale_factor=1.15), run_time=1.2)
        self.clear_scene()
