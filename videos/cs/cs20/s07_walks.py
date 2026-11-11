from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, code, grid_table, load, mono,
                                   words)


class Walks(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_sat()
        self.ruin()
        self.schoening()

    def card(self):
        card = chapter_card(6, r"Random walks that solve SAT", r"Can a drunkard find a satisfying assignment?",
                            lit=(1991, 1999), extra=((1991, r"Papadimitriou's walk"), (1999, r"Sch\"oning's walk")),
                            part=PART)
        with self.voiceover((
            'Chapter six. Random walks that solve SAT.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_sat(self):
        head = label(r"A walk for 2-SAT", font_size=34).to_edge(UP, buff=0.35)
        cl = MathTex(r"(x_1 \lor \lnot x_2)", r"\land", r"(x_2 \lor x_3)", r"\land", r"(\lnot x_1 \lor \lnot x_3)",
                     r"\land", r"(x_2 \lor \lnot x_4)", r"\land \cdots", font_size=32).next_to(head, DOWN, buff=0.45)
        for i in (0, 2, 4, 6):
            cl[i].set_color(DATA)
        algo = code([
            "start from any assignment",
            "repeat:",
            "    if every clause holds: done",
            "    pick any clause that fails",
            "    flip one of its two variables, at random",
        ], size=22).next_to(cl, DOWN, buff=0.5)
        note_ = label(r"Part 18 solved 2-SAT exactly with strongly connected components; \ this walk uses no "
                      r"structure at all", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            'A 2-SAT formula is an and of clauses, each an or of two literals. Part 18 solved it exactly, with '
            "strongly connected components of the implication graph. <bookmark mark='a'/> Christos Papadimitriou "
            'analyzed a much dumber method in 1991. Start anywhere. While some clause fails, pick one, and flip one '
            "of its two variables, chosen by a coin. <bookmark mark='b'/> It uses no structure at all. Why should it"
            ' ever finish?'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(algo))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def ruin(self):
        head = label(r"Distance to a solution, \ as a walk on a line", font_size=34).to_edge(UP, buff=0.35)
        n = 12
        line = NumberLine(x_range=[0, n, 1], length=11.0, include_numbers=True, font_size=22, color=GREY_B)
        line.move_to(UP * 0.6)
        zero = label(r"solved", font_size=20, color=YES).next_to(line.n2p(0), DOWN, buff=0.55)
        wall = label(r"wall", font_size=20, color=GREY_A).next_to(line.n2p(n), DOWN, buff=0.55)
        facts = VGroup(
            label(r"fix a satisfying assignment $x^*$; \ $D$ = the number of variables where we differ from it",
                  font_size=21, color=WHITE),
            label(r"a failing clause has a literal where we differ from $x^*$; \ flipping it: $D - 1$", font_size=21,
                  color=WHITE),
            MathTex(r"\Pr[D \to D - 1] \ge \tfrac12", font_size=34, color=YES),
            label(r"gambler's ruin, \ with a wall at $n$: \ expected time to reach 0 from $D$ is $\le D(2n - D) \le "
                  r"n^2$", font_size=21, color=LAM),
            label(r"so: \ run $2n^2$ steps; \ by Markov, \ if satisfiable, \ we fail with probability $\le \tfrac12$",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        rng = random.Random(3)
        path = [8]
        while path[-1] > 0 and len(path) < 200:
            x = path[-1]
            step = -1 if (x == n or rng.random() < 0.5) else 1
            path.append(x + step)
        tok = Dot(line.n2p(path[0]), radius=0.15, color=HEAD)
        distance_path = VMobject().set_points_as_corners([line.n2p(x) for x in path])
        trace_curve = VMobject(color=LAM, stroke_width=2).set_points_as_corners(
            [[-5.5 + 11*i/(len(path)-1), -0.4 + 0.55*x/n, 0] for i,x in enumerate(path)])
        trace_base = Line([-5.5,-0.4,0],[5.5,-0.4,0],color=GREY_D,stroke_width=1)
        trace_note = label(rf"same {len(path)-1} flips; \ curve: distance versus flip number; \ compressed in time",
                           font_size=16,color=GREY_A).move_to(DOWN*0.68)
        with self.voiceover(
            (
            f'Fix one satisfying assignment, x star, and let D be the number of variables where our assignment '
            f"differs from it. <bookmark mark='a'/> A clause that fails has both its literals false, but x star makes"
            f' at least one of them true, so we disagree with x star on at least one of the two variables. <bookmark '
            f"mark='b'/> Flipping a random one of the two moves D one step closer to zero with probability at least a"
            f" half. <bookmark mark='c'/> So D does a random walk on the line from zero to n, pushed toward zero at "
            f"least as often as away. This is the gambler's ruin. From any start, the expected time to reach zero is "
            f"at most n squared. <bookmark mark='d'/> Here is one walk, starting eight steps away. It took "
            f'{len(path) - 1}'
            f" flips. We may even stop sooner, at some other solution. <bookmark mark='e'/> So run two n squared "
            f"steps. If the formula is satisfiable, Markov's inequality says we fail with probability at most a half,"
            f' and repetition does the rest. The bound is for the worst formula: on random satisfiable ones, with up '
            f'to three hundred and twenty variables, the walk needed only about two flips per variable.'
        )
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(zero), FadeIn(wall))
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]))
            vo.wait_until("d")
            self.play(FadeIn(tok), Create(trace_base), FadeIn(trace_note), run_time=0.4)
            cue_budget = max(0.2, vo.until("e", minimum=0) - 0.7)
            self.play(MoveAlongPath(tok, distance_path), Create(trace_curve),
                      run_time=min(7.0, cue_budget), rate_func=linear)
            self.play(Flash(tok, color=YES), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

    def schoening(self):
        d = load("walks")
        head = label(r"Sch\"oning's walk for 3-SAT", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"a failing 3-clause: \ the right flip is one of three, \ $\Pr[D \to D - 1] \ge \tfrac13$",
                  font_size=21, color=WHITE),
            label(r"the walk can drift \textbf{away}: \ restart from a fresh random point every $3n$ flips",
                  font_size=21, color=WHITE),
            MathTex(r"\Pr[\text{one restart succeeds}] \ge \frac{1}{\mathrm{poly}(n)} \left(\frac34\right)^n "
                    r"\quad\Longrightarrow\quad \mathrm{poly}(n)\left(\frac43\right)^n \text{ expected restarts}", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.35)
        if pts[2].width > 13.0:
            pts[2].scale_to_fit_width(13.0)
        rows = d["three"]
        ax = Axes(x_range=[7, 21, 2], y_range=[0, 6.5, 1], x_length=6.4, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 1.6)
        xl = VGroup(*[label(str(x), font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x in range(8, 21, 4)])
        yl = VGroup(*[label(rf"$10^{y}$", font_size=16, color=GREY_B).next_to(ax.c2p(7, y), LEFT, buff=0.1)
                      for y in range(0, 7, 2)])

        def series(key, color):
            pts_ = [ax.c2p(r["n"], math.log10(r[key])) for r in rows]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts_),
                          *[Dot(p, radius=0.05, color=color) for p in pts_])
        s_brute = series("brute", NO)
        s_bound = series("schoening", HEAD)
        s_meas = series("mean_restarts", YES)
        leg = VGroup(label(r"$2^n$: \ every assignment", font_size=19, color=NO),
                     label(r"$(4/3)^n$: \ exponential scale only", font_size=19, color=HEAD),
                     label(r"measured restarts", font_size=19, color=YES),
                     label(r"random 3-SAT at 4.26 clauses per variable, \\ with exactly one solution", font_size=17,
                           color=GREY_A),
                     label(r"selected later SAT algorithms: \ base around $1.3$; \ not a record survey", font_size=19, color=LAM),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.6)
        last = rows[-1]
        with self.voiceover(
            (
            (
            f"For 3-SAT the same walk works, but worse. <bookmark mark='a'/> A failing clause now has three "
            f'variables, and only one of them might be the right one to flip, so the chance that D falls can be as '
            f"low as one third. <bookmark mark='b'/> The walk can drift away from the solution, so Uwe Schöning, in "
            f"1999, restarts it from a fresh random assignment every three n flips. <bookmark mark='c'/> A careful "
            f'count shows each restart succeeds with probability at least three quarters to the n divided by a '
            f'polynomial factor, giving expected restarts of order four thirds to the n up to polynomial factors: '
            f"exponential, but far fewer than the two to the n assignments. <bookmark mark='d'/> We tested small "
            f'random formulas near the threshold, retaining those with exactly one satisfying assignment, checked by '
            f'brute force. This is a selected fixture family, not a proof of worst-case difficulty. <bookmark '
            f"mark='e'/> With "
            f"{last['n']}"
            f' variables, the walk needed about '
            f"{last['mean_restarts']:.0f}"
            f' restarts on average, compared with the displayed exponential scale; the omitted polynomial factors '
            f'mean that curve is not a finite upper bound. Brute force has about a million assignments to try here. '
            f"Selected later descendants of Paturi, Pudlák, Saks and Zane's algorithm achieve exponential bases "
            f'around one point three; this is not a current-record survey. Whether something much better exists is '
            f'the question behind the exponential time hypothesis of Part 27.'
        )
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(s_brute), FadeIn(leg[0]))
            self.play(Create(s_bound), FadeIn(leg[1]))
            vo.wait_until("e")
            self.play(Create(s_meas), FadeIn(leg[2]), FadeIn(leg[3]))
            self.play(FadeIn(leg[4]))
        self.wait(0.3)
        self.clear_scene()
