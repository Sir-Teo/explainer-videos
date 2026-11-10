from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

BW, BH = 0.42, 0.3


def bins_row(nb, x0, y0, color):
    g = VGroup()
    for b in range(nb):
        g.add(VGroup(Line([x0 + b * (BW + 0.08), y0, 0], [x0 + b * (BW + 0.08) + BW, y0, 0], color=color),
                     mono(str(b), 12, GREY_B).move_to([x0 + b * (BW + 0.08) + BW / 2, y0 - 0.18, 0])))
    return g


class Bins(VoiceoverScene):
    def construct(self):
        self.card()
        self.fill()
        self.table()
        self.why()

    def card(self):
        card = chapter_card(7, r"Balls into bins, \ and the power of two choices", r"How uneven does chance make "
                            r"things?", lit=(1994,), extra=((1994, r"two choices"),), part=PART)
        with self.voiceover((
            'Chapter seven. Balls into bins, and the power of two choices.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fill(self):
        d = load("bins")
        picks = d["small"]
        nb = 12
        head = label(r"24 balls, \ 12 bins", font_size=34).to_edge(UP, buff=0.35)
        x1, x2, y0 = -6.4, 0.6, -2.2
        row1 = bins_row(nb, x1, y0, DATA)
        row2 = bins_row(nb, x2, y0, YES)
        t1 = label(r"one random bin each", font_size=22, color=DATA).next_to(row1, UP, buff=3.3)
        t2 = label(r"the emptier of two random bins", font_size=22, color=YES).next_to(row2, UP, buff=3.3)
        load1, load2 = [0] * nb, [0] * nb
        with self.voiceover(
            (
            'Throw balls into bins at random. How full does the fullest bin get? This question decides how well a '
            "hash table's chains, Part 17, or a server farm's queues are balanced. <bookmark mark='a'/> On the left,"
            ' each of twenty-four balls goes into one random bin of twelve. On the right, each ball looks at two '
            "random bins and goes into the emptier one. <bookmark mark='b'/> The same random numbers drive both "
            "sides: the left uses the first choice, the right uses both. <bookmark mark='c'/> One choice leaves some"
            ' bins empty and piles others high. Two choices are strikingly even.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(row1), FadeIn(row2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            for a, b in picks:
                b2 = a if load2[a] <= load2[b] else b
                ball1 = Circle(radius=0.13, color=DATA, fill_opacity=0.85, stroke_width=0).move_to(
                    [x1 + a * (BW + 0.08) + BW / 2, y0 + 0.16 + load1[a] * BH, 0])
                ball2 = Circle(radius=0.13, color=YES, fill_opacity=0.85, stroke_width=0).move_to(
                    [x2 + b2 * (BW + 0.08) + BW / 2, y0 + 0.16 + load2[b2] * BH, 0])
                hl = VGroup(*[SurroundingRectangle(row2[c][0], color=HEAD, buff=0.06, stroke_width=1.5)
                              for c in (a, b)])
                load1[a] += 1
                load2[b2] += 1
                self.play(FadeIn(ball1, shift=DOWN * 0.3), FadeIn(hl), FadeIn(ball2, shift=DOWN * 0.3),
                          run_time=0.35)
                self.remove(hl)
            vo.wait_until("b")
            vo.wait_until("c")
            m1 = label(rf"fullest: \ {max(load1)}; \ empty: \ {load1.count(0)}", font_size=22, color=DATA
                       ).next_to(row1, DOWN, buff=0.45)
            m2 = label(rf"fullest: \ {max(load2)}; \ empty: \ {load2.count(0)}", font_size=22, color=YES
                       ).next_to(row2, DOWN, buff=0.45)
            self.play(FadeIn(m1), FadeIn(m2))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("bins")
        head = label(r"$n$ balls into $n$ bins: \ the fullest bin", font_size=34).to_edge(UP, buff=0.35)
        rows = [[words(r["n"]), str(r["one"]), f"{r['theory_one']:.1f}", str(r["two"]), f"{r['theory_two']:.1f}"]
                for r in d["rows"]]
        tab = grid_table([r"$n$", r"one choice", r"$\ln n / \ln\ln n$", r"two choices", r"$\log_2 \ln n$"], rows,
                         widths=[2.0, 2.0, 2.6, 2.2, 2.4], row_h=0.44, font_size=21, mono_cols=(),
                         colors=[[GREY_A, DATA, DATA, YES, YES]] * len(rows)).next_to(head, DOWN, buff=0.4)
        h1, h2 = d["hist_one"], d["hist_two"]
        top = max(max(h1), max(h2))
        bars = VGroup()
        for k in range(max(len(h1), len(h2))):
            for j, (h, c) in enumerate(((h1, DATA), (h2, YES))):
                v = h[k] if k < len(h) else 0
                hh = 2.0 * v / top
                bars.add(Rectangle(width=0.26, height=max(hh, 0.015), stroke_width=0, fill_color=c, fill_opacity=0.85
                                   ).move_to([-5.6 + k * 0.72 + j * 0.28, -3.1 + hh / 2, 0]))
        names = VGroup(*[mono(str(k), 14, GREY_A).move_to([-5.6 + k * 0.72 + 0.14, -3.3, 0]) for k in range(9)])
        cap = label(r"$n = 10^6$: \ how many bins hold $0, 1, 2, \dots$ balls", font_size=18, color=GREY_A
                    ).next_to(bars, UP, buff=0.15).align_to(bars, LEFT)
        side = VGroup(
            label('one choice: \\ Poisson(1) approximation, \\ fraction $\\approx e^{-1}/k!$ at load $k$', font_size=20, color=DATA),
            label(rf"{d['hist_one'][-1]} bins hold {len(d['hist_one']) - 1}", font_size=20, color=DATA),
            label(rf"two choices: \ none above {len(d['hist_two']) - 1}; \ only {d['hist_two'][-1]} reach it",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.6 + DOWN * 2.4)
        protocol = label("table maxima: 5 one-choice trials; 3 two-choice trials, except 1 at a million", font_size=17, color=GREY_A).next_to(tab, DOWN, buff=0.16)
        with self.voiceover(
            (
            (
            f"Now with n balls and n bins, for n from a thousand to a million. <bookmark mark='a'/> With one choice "
            f'the fullest bin holds about log n over log log n balls; the column beside it is that formula, which is '
            f'right only up to a factor that tends to one very slowly, so the measured loads are higher. <bookmark '
            f"mark='b'/> With two choices the fullest bin holds about log log n over log two, plus a constant. For a "
            f"million balls: ten against four. <bookmark mark='c'/> At a million, the one-choice loads approximately "
            f'follow a Poisson law, a fraction e to the minus one over k factorial of the bins holding k, with '
            f"{d['hist_one'][-1]}"
            f' unlucky bins holding '
            f"{len(d['hist_one']) - 1}"
            f'. With two choices nothing went above '
            f"{len(d['hist_two']) - 1}"
            f'. A tiny change in the rule, an exponential change in the result. This is the power of two choices, '
            f'from Azar, Broder, Karlin and Upfal in 1994.'
        )
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(protocol))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(*[Indicate(tab.cells[r][1], color=DATA) for r in range(1, len(rows) + 1)])
            vo.wait_until("b")
            self.play(*[Indicate(tab.cells[r][3], color=YES) for r in range(1, len(rows) + 1)])
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(names),
                      FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    def why(self):
        head = label(r"Why two choices square the tail", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"$\beta_i$: \ the number of bins holding at least $i$ balls", font_size=22, color=WHITE),
            label(r"a ball lands at height $i + 1$ only if \textbf{both} its bins already hold $\ge i$:", font_size=22,
                  color=WHITE),
            MathTex(r"\Pr \approx \left(\frac{\beta_i}{n}\right)^{2} \quad\Longrightarrow\quad "
                    r"\frac{\beta_{i+1}}{n} \lesssim \left(\frac{\beta_i}{n}\right)^{2}", font_size=36, color=YES),
            label(r"start from $\beta_4 / n \le \tfrac14$: \ $\tfrac{1}{4},\ \tfrac{1}{16},\ \tfrac{1}{256},\ "
                  r"\tfrac{1}{65536}, \dots$ \ below $1/n$ after $\log_2 \log_2 n$ steps", font_size=22, color=LAM),
            label(r"with one choice the tail falls like $1/k!$: \ only a little faster than exponentially",
                  font_size=22, color=DATA),
            label(r"$d$ choices: \ $\ln\ln n / \ln d$ \ (most of the gain is in the second choice)", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        foot = label(r"in practice: \ load balancers pick the less busy of two servers; \ cuckoo hashing "
                     r"(Part 17) gives each key two homes", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Why? <bookmark mark='a'/> Let beta i be the number of bins holding at least i balls. <bookmark "
            "mark='b'/> A ball lands at height i plus one only if both its bins already hold at least i, <bookmark "
            "mark='c'/> with probability about beta i over n, squared. So each height's fraction is about the square"
            " of the one below. <bookmark mark='d'/> Squaring collapses fast: a quarter, a sixteenth, one in two "
            'hundred and fifty-six, one in sixty-five thousand, below one over n after about log log n steps. '
            "<bookmark mark='e'/> With one choice there is no squaring, only one over k factorial. <bookmark "
            "mark='f'/> With d choices the load is log log n over log d, so most of the gain is in the second "
            "choice. <bookmark mark='g'/> Load balancers use exactly this rule, and cuckoo hashing gives every key "
            'two homes.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
