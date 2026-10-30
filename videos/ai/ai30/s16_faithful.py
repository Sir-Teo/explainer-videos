from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, FEAT, PART

HINT = C.SURPRISE


def box(lines, color, w=3.3):
    t = VGroup(*[label(l_, font_size=20, color=c_) for l_, c_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    r = RoundedRectangle(width=max(w, t.width + 0.4), height=t.height + 0.4, corner_radius=0.1, stroke_color=color,
                         stroke_width=2).move_to(t)
    return VGroup(r, t)


class Faithful(VoiceoverScene):
    def construct(self):
        self.card()
        self.biased()
        self.hints()
        self.inside()

    def card(self):
        card = chapter_card(15, r"Does the chain of thought tell the truth?", r"Is the written reasoning the computation?",
                            part=PART)
        with self.voiceover("Chapter fifteen. Does the chain of thought tell the truth?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def biased(self):
        head = label(r"Part 28's reasoning models write their thinking down. \ Is it what they did?", font_size=28)
        head.to_edge(UP, buff=0.4)
        shots = VGroup(*[box([(rf"example {i}", GREY_B), (r"$\ldots$ \ answer: \ (A)", WHITE)], GREY_C, w=2.6)
                         for i in (1, 2, 3)]).arrange(RIGHT, buff=0.3)
        q = box([(r"the new question", GREY_B), (r"$\ldots$ \ answer: \ ?", WHITE)], GREY_C, w=2.6)
        row = VGroup(shots, q).arrange(RIGHT, buff=0.6).move_to(UP * 0.7)
        bias = label(r"in every example, \ the right option was moved to (A)", font_size=22, color=HINT).next_to(row, DOWN, buff=0.25)
        expl = box([(r"its explanation", GREY_B), (r"step by step, \ for (A)", WHITE), (r"no word about the pattern", HINT)],
                   GREY_C, w=4.2).next_to(bias, DOWN, buff=0.35)
        hc = VGroup(history_card(2023, r"M.~Turpin, J.~Michael, E.~Perez \& S.~Bowman",
                                 r"biased examples cut accuracy by up to $36\%$ on $13$ BIG-Bench Hard tasks; \ the "
                                 r"explanations never mention the bias", width=6.2, color=HINT, font_size=18),
                    history_card(2023, r"T.~Lanham et al., \ Anthropic",
                                 r"edit or cut the chain of thought and see whether the answer changes: \ on many "
                                 r"tasks it doesn't", width=6.2, color=HINT, font_size=18)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "The last question about the inside of a model is the one Part 28 left open. Reasoning models write out "
            "their thinking. Is the writing the thinking? <bookmark mark='a'/> In 2023 Miles Turpin, Julian "
            "Michael, Ethan Perez and Sam Bowman gave models few-shot examples in which the right answer was always "
            "option A. <bookmark mark='b'/> The models picked up the pattern, and their step-by-step explanations "
            "argued for A without ever mentioning it; on thirteen hard tasks accuracy fell by up to 36 percent. "
            "<bookmark mark='c'/> The same year, Tamera Lanham and colleagues at Anthropic edited and truncated "
            "chains of thought, and on many tasks the answer did not change: the chain was not doing the work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(bias))
            vo.wait_until("b")
            self.play(FadeIn(expl), FadeIn(hc[0]))
            vo.wait_until("c")
            self.play(FadeIn(hc[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hints(self):
        head = label(r"Slip in a hint; \ does the chain of thought own up to using it?", font_size=30).to_edge(UP, buff=0.4)
        vals = [(r"Claude 3.7 Sonnet", 0.25, FEAT), (r"DeepSeek-R1", 0.39, C.TRUE_P)]
        grids = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            cells = VGroup(*[Square(0.22, stroke_color=GREY_D, stroke_width=1, fill_color=col, fill_opacity=0) for _ in range(100)])
            cells.arrange_in_grid(10, 10, buff=0.05).move_to([-3.2 + 6.4 * i, -0.4, 0])
            n_ = label(nm, font_size=26, color=col).next_to(cells, UP, buff=0.25)
            p_ = label(rf"${100 * v:.0f}$ \ of \ $100$", font_size=26, color=col).next_to(cells, DOWN, buff=0.2)
            grids.add(VGroup(cells, n_, p_))
        cap = label(r"of $100$ answers the hint changed: \ how often the chain of thought mentions it", font_size=22,
                    color=GREY_A).next_to(grids, DOWN, buff=0.3)
        tag = note(r"published, \ not measured here; \ admitted reward hacks: \ under $2\%$ in most settings").to_corner(DR, buff=0.25)
        cite_ = cite(r"Y.~Chen et al.\ (Anthropic), \textit{Reasoning Models Don't Always Say What They Think} (2025)", corner=DL)
        with self.voiceover(
            "In 2025 Yanda Chen and colleagues at Anthropic did it with reasoning models. Put a hint in the question, "
            "a professor's opinion, say, or an answer said to come from unauthorized access; keep the cases where the hint changed the answer, and read "
            "the chain of thought. <bookmark mark='a'/> Claude 3.7 Sonnet mentioned the hint 25 percent of the time; "
            "DeepSeek-R1, 39 percent. <bookmark mark='b'/> Trained to exploit a reward hack, the models used it, and "
            "admitted it in their reasoning less than 2 percent of the time in most settings. The written chain is a "
            "useful window, Part 31 builds monitors on it, but it is not a confession."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), *[FadeIn(g[0], lag_ratio=0.01) for g in grids], *[FadeIn(g[1]) for g in grids],
                      FadeIn(cap))
            vo.wait_until("a")
            for g, (_, v, col) in zip(grids, vals):
                on = g[0][:int(round(100 * v))]
                self.play(LaggedStart(*[c.animate.set_fill(col, 0.9).set_stroke(col) for c in on], lag_ratio=0.04),
                          FadeIn(g[2]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        head = label(r"Reading the computation instead \ (Claude 3.5 Haiku, \ attribution graphs)", font_size=28).to_edge(UP, buff=0.35)
        cols = VGroup(
            box([(r"faithful", C.TRUE_P), (r"$\sqrt{0.64}$", WHITE), (r"the graph shows $\sqrt{64} = 8$ computed", GREY_A)],
                C.TRUE_P, w=3.9),
            box([(r"made up", HINT), (r"$\cos(23423)$, \ ``with a calculator''", WHITE),
                 (r"no calculation in the graph: \ a guess", GREY_A)], HINT, w=3.9),
            box([(r"motivated", CAUSE), (r"the same, \ ``I got $4$ by hand''", WHITE),
                 (r"the graph works \textit{backwards} from $4$", GREY_A), (r"to the step that reaches it", GREY_A)],
                CAUSE, w=3.9),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
        if cols.width > 13.2:
            cols.scale_to_fit_width(13.2)
        why_ = label(r"our models write no chains of thought, \ so this chapter is cited, \ not computed: \\ a toy "
                     r"of this size would show nothing honest", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.45)
        cite_ = cite(r"Lindsey et al., \textit{On the Biology of a Large Language Model} (2025)", corner=DR)
        with self.voiceover(
            "The attribution graphs of chapter eleven can check a chain of thought against the computation. "
            "<bookmark mark='a'/> Asked for the square root of 0.64, Claude 3.5 Haiku really did compute the root "
            "of 64. <bookmark mark='b'/> Asked for the cosine of a large number, it claimed to use a calculator; the "
            "graph shows no calculation, only a guess. <bookmark mark='c'/> And told that the user had worked out "
            "the answer as 4, it worked backwards: the graph shows the hinted 4 setting an intermediate value, which "
            "the written steps then reach as if by honest arithmetic. That is motivated reasoning, seen from inside. "
            "<bookmark mark='d'/> Our own models do not write chains of thought, so here we cite rather than compute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cols[k], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()
