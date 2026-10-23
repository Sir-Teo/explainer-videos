from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, LEAN, PART, POLICY, SEARCH, WRONG_C

ARC_COLORS = ["#111111", "#1E93FF", "#F93C31", "#4FCC30", "#FFDC00", "#999999", "#E53AA3", "#FF851B", "#87D8F1",
              "#921231"]


def grid_mob(G, cell=0.28):
    G = np.asarray(G)
    g = VGroup()
    for r in range(G.shape[0]):
        for c in range(G.shape[1]):
            g.add(Square(cell, stroke_color="#333333", stroke_width=1, fill_color=ARC_COLORS[int(G[r, c])],
                         fill_opacity=1).move_to([c * cell, -r * cell, 0]))
    return g


def rays(G):
    """The illustrative rule: every coloured cell sends a line of its colour to the right edge."""
    G = np.array(G)
    out = G.copy()
    for r in range(G.shape[0]):
        for c in range(G.shape[1]):
            if G[r, c]:
                out[r, c:] = np.where(out[r, c:] == 0, G[r, c], out[r, c:])
    return out


class ARC(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.history()
        self.arc3()

    def card(self):
        card = chapter_card(14, r"Puzzles nobody has seen", r"Can a model reason about something truly new?",
                            lit=(2024, 2026), part=PART)
        with self.voiceover("Chapter fourteen. Puzzles nobody has seen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def task(self):
        A = np.zeros((6, 6), int)
        A[1, 1], A[4, 2] = 2, 1
        B = np.zeros((6, 6), int)
        B[0, 3], B[2, 0], B[5, 4] = 3, 4, 2
        T = np.zeros((6, 6), int)
        T[1, 2], T[3, 0], T[4, 3] = 6, 1, 7
        pairs = VGroup()
        for X in (A, B):
            pairs.add(VGroup(grid_mob(X), MathTex(r"\to", font_size=34, color=GREY_B), grid_mob(rays(X))).arrange(RIGHT, buff=0.3))
        test = VGroup(grid_mob(T), MathTex(r"\to", font_size=34, color=GREY_B),
                      label(r"?", font_size=60, color=SEARCH)).arrange(RIGHT, buff=0.3)
        ans = grid_mob(rays(T)).move_to(test[2])
        VGroup(pairs, test).arrange(RIGHT, buff=0.8).move_to(UP * 0.7)
        pairs.arrange(DOWN, buff=0.4).move_to([-3.3, 0.6, 0])
        test.move_to([3.4, 0.6, 0])
        ans.move_to(test[2])
        pl = label(r"a few examples", font_size=22, color=GREY_A).next_to(pairs, UP, buff=0.2)
        tl = label(r"a new input: \ what comes out?", font_size=22, color=SEARCH).next_to(test, UP, buff=0.2)
        sch = note(r"illustrative: \ not an ARC task").to_corner(UR, buff=0.3)
        hc = history_card(2019, r"F.~Chollet, \ \textit{On the Measure of Intelligence}",
                          r"intelligence is the efficiency of acquiring new skills; \ grids up to $30 \times 30$, \ ten "
                          r"colours, \ a handful of examples, \ every task different", width=8.4,
                          color=SEARCH).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every benchmark so far rewards knowing things. In 2019 François Chollet, who wrote the Keras library, "
            "argued that intelligence is something else: how efficiently you acquire a new skill. He built a test of "
            "it, the Abstraction and Reasoning Corpus, now called ARC-AGI. <bookmark mark='a'/> Each task gives a "
            "few pairs of coloured grids, an input and an output. <bookmark mark='b'/> Then a new input. What comes "
            "out? <bookmark mark='c'/> People find most tasks easy. Every task is different, so nothing can be "
            "memorized: the rule must be found, on the spot."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(sch), FadeIn(pl), LaggedStart(*[FadeIn(p_[0]) for p_ in pairs],
                                                                                         lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_[1:]) for p_ in pairs], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(test), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeOut(test[2]), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        # reported scores: (year as a decimal, score), each benchmark's own sets and costs
        v1 = [(2020.5, 20.0, r"Kaggle, \ program search"), (2024.9, 53.5, r"test-time training"),
              (2024.97, 75.7, r"o3, \ \$26 a task"), (2024.99, 87.5, r"o3, \ $172\times$ the compute")]
        v2 = [(2025.23, 4.0, r"at launch"), (2025.93, 24.0, r"NVARC, \ Kaggle"), (2025.93, 37.6, r"Claude Opus 4.5"),
              (2025.93, 54.0, r"Poetiq on Gemini 3 Pro"), (2026.78, 91.3, r"Gemini 4 Argon")]
        g = axes([2019, 2027], [0, 100], x_length=10.4, y_length=4.6, xlabel=r"year",
                 ylabel=r"best reported scores, \ percent \ (sets and costs differ)", xticks=list(range(2019, 2028)),
                 xfmt=lambda v: f"{int(v)}", yticks=[0, 50, 100], center=[-0.6, -0.5, 0])
        ax = g.ax

        def series(pts, col):
            line = VMobject(stroke_color=col, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y, _ in pts])
            dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=col) for x, y, _ in pts])
            return VGroup(line, dots)

        s1, s2 = series(v1, CHAIN), series(v2, POLICY)
        l1 = label(r"ARC-AGI-1", font_size=22, color=CHAIN).next_to(ax.c2p(2020.5, 20.0), UP, buff=0.2)
        l2 = label(r"ARC-AGI-2", font_size=22, color=POLICY).next_to(ax.c2p(2025.23, 4.0), RIGHT, buff=0.25)
        notes1 = VGroup(*[label(t, font_size=17, color=CHAIN).next_to(ax.c2p(x, y), LEFT, buff=0.12)
                          for x, y, t in v1[1:]])
        notes1[0].shift(UP * 0.2)
        notes1[2].shift(UP * 0.12)
        notes1[1].shift(DOWN * 0.1)
        notes2 = VGroup(*[label(t, font_size=17, color=POLICY).next_to(ax.c2p(x, y), RIGHT, buff=0.12)
                          for x, y, t in v2[1:]])
        hl = label(r"ARC-AGI-2: \\ a person, \\ on average, \\ $60\%$", font_size=17, color=GREY_B)
        hx = max(ax.c2p(2027, 60)[0], notes2[2].get_right()[0]) + 0.2  # clear of the point labels
        hl.move_to([hx + hl.width / 2, ax.c2p(2027, 60)[1], 0])
        hum = DashedLine(ax.c2p(2025.2, 60), [hx - 0.1, ax.c2p(2027, 60)[1], 0], color=GREY_B, dash_length=0.08)
        cite_ = cite(r"ARC Prize Foundation: \ results pages and reports, 2020--2026", corner=DR)
        with self.voiceover(
            "ARC-AGI-1 resisted for five years. <bookmark mark='a'/> The 2020 Kaggle contest was won with about 20 "
            "percent, by searching over hand-written programs. In 2024, training on each task's own examples at test "
            "time reached 53.5. <bookmark mark='b'/> Then in December 2024, OpenAI's o3 scored 75.7 percent at about "
            "twenty-six dollars a task, and 87.5 with 172 times the compute. <bookmark mark='c'/> So in March 2025 a "
            "harder version, ARC-AGI-2, launched, and the best systems fell back to a few percent, while a person "
            "solves 60 percent on average. <bookmark mark='d'/> By December, a four-billion-parameter model trained "
            "on synthetic tasks won the Kaggle contest with 24 percent; Claude Opus 4.5 reached 37.6; and a "
            "refinement loop wrapped around Gemini 3 Pro, 54. ARC Prize named the year's theme: refinement loops, "
            "propose, check, improve. <bookmark mark='e'/> And in October 2026, ARC Prize verified Google's Gemini 4 "
            "Argon at 91 percent. In nineteen months, the harder test was all but solved."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(s1[1][0]), FadeIn(l1), Create(VMobject().set_points_as_corners([ax.c2p(*v1[0][:2]), ax.c2p(*v1[1][:2])])
                                                          .set_stroke(CHAIN, 3)), FadeIn(s1[1][1]), FadeIn(notes1[0]))
            vo.wait_until("b")
            self.play(Create(s1[0]), FadeIn(s1[1][2:]), FadeIn(notes1[1:]))
            vo.wait_until("c")
            self.play(FadeIn(s2[1][0]), FadeIn(l2), Create(hum), FadeIn(hl))
            vo.wait_until("d")
            self.play(FadeIn(s2[1][1:4]), FadeIn(notes2[:3]))
            vo.wait_until("e")
            self.play(Create(s2[0]), FadeIn(s2[1][4]), FadeIn(notes2[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arc3(self):
        hc = history_card(2026, r"ARC-AGI-3 \ (March)", r"interactive games with no instructions: \ explore, \ work out "
                          r"the goal, \ plan. \ Scored by how efficiently the goal is reached, \ against people",
                          width=5.4, color=WRONG_C).move_to([-4.0, 0.0, 0])
        rows = [(r"people", 100.0, GREY_A), (r"Claude Opus 4.6, \ March", 0.5, WRONG_C),
                (r"Gemini 3.1 Pro, \ March", 0.4, WRONG_C), (r"GPT-5.4, \ March", 0.2, WRONG_C),
                (r"GPT-6 Astra, \ September", 62.7, POLICY)]
        W = 3.2
        bars = VGroup()
        for i, (t, v, c) in enumerate(rows):
            y = 1.7 - i * 0.85
            name = label(t, font_size=26, color=GREY_A).move_to([2.4, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(W * v / 100, 0.02), height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.9)
            bar.move_to([2.6 + max(W * v / 100, 0.02) / 2, y, 0])
            val = label(rf"${v:g}\%$", font_size=26, color=c).next_to(bar, RIGHT, buff=0.1)
            bars.add(VGroup(name, bar, val))
        bh = label(r"ARC-AGI-3, \ ARC Prize's standard harness", font_size=24, color=GREY_B).next_to(bars, UP, buff=0.3)
        lesson = VGroup(label(r"each new test falls faster than the last", font_size=26, color=GREY_A),
                        label(r"what is learned: \ propose, \ check, \ refine \ (a loop, \ like every chapter here)",
                              font_size=24, color=SEARCH)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        cite_ = cite(r"ARC Prize Foundation, \textit{ARC-AGI-3} technical report (April 2026); \\ ARC Prize, "
                     r"\textit{GPT-6 Astra on ARC-AGI-3} (September 2026)", corner=UL)
        with self.voiceover(
            "So in March 2026 came ARC-AGI-3: interactive games, with no instructions. The player must explore, work "
            "out what the goal is, and plan, and is scored by how efficiently it gets there, against people. "
            "<bookmark mark='a'/> People could solve every game. At launch, every frontier model scored below one "
            "percent. <bookmark mark='b'/> In September, ARC Prize measured OpenAI's GPT-6 Astra at 62.7 percent with "
            "their standard harness. <bookmark mark='c'/> Each new test has fallen faster than the last. And what "
            "solves them looks like every chapter of this part: propose, check, refine, in a loop."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(cite_), FadeIn(bh))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                    for b in bars[:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(bars[4][0]), GrowFromEdge(bars[4][1], LEFT), FadeIn(bars[4][2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lesson], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
