from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, LEAN, PART, POLICY, PRM_C, RIGHT_C, SEARCH, WRONG_C, node_box


class Formal(VoiceoverScene):
    def construct(self):
        self.card()
        self.lean()
        self.alphaproof()
        self.imo()
        self.spectrum()

    def card(self):
        card = chapter_card(13, r"Proofs a machine can check", r"What if the checker could check everything?",
                            lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter thirteen. Proofs a machine can check."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lean(self):
        code = code_block([
            "theorem two_mul_le (a b : Nat) (h : a <= b) :",
            "    2 * a <= 2 * b := by",
            "  omega",
        ], font_size=22, color=WHITE)
        box = SurroundingRectangle(code, color=LEAN, buff=0.3, corner_radius=0.12, stroke_width=2)
        g = VGroup(box, code).move_to([-1.3, 1.4, 0])
        gl = label(r"Lean 4: \ a statement, \ and a proof the kernel checks", font_size=22, color=LEAN)
        gl.next_to(g, UP, buff=0.2)
        ok = VGroup(MathTex(r"\checkmark", font_size=48, color=RIGHT_C), label(r"accepted", font_size=26, color=RIGHT_C))
        ok.arrange(RIGHT, buff=0.2).next_to(g, RIGHT, buff=0.6)
        sch = note(r"illustrative").next_to(g, DOWN, buff=0.15).align_to(g, LEFT)
        pts = VGroup(
            label(r"every step checked by a small trusted kernel: \ no lucky guesses, \ no hand-waving", font_size=24,
                  color=GREY_A),
            label(r"a reward that cannot be hacked \ (if the statement says what was meant)", font_size=24,
                  color=RIGHT_C),
            label(r"Mathlib: \ a library of formalized mathematics, \ written by a community since 2017",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.6, 0])
        head = label(r"a checker that cannot be fooled?", font_size=34, color=LEAN).to_edge(UP, buff=0.35)
        gl.next_to(g, UP, buff=0.2)
        # the limit of an answer checker: a right number at the end of a broken argument (schematic)
        chips = VGroup(*[node_box(t, c, font_size=24) for t, c in (
            (r"step 1", RIGHT_C), (r"step 2", WRONG_C), (r"step 3", RIGHT_C), (r"answer: \ right", RIGHT_C))])
        chips.arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        crr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(chips, chips[1:])])
        broken = VGroup(chips, crr, label(r"a right number \ at the end of a broken argument", font_size=26,
                                          color=GREY_A).next_to(chips, DOWN, buff=0.45),
                        note(r"schematic").next_to(chips, UP, buff=0.3))
        with self.voiceover(
            "Everything in this part has leaned on a checker, and checkers have limits: a right number can sit at the "
            "end of a broken argument. Mathematics has a way out. <bookmark mark='a'/> In a proof assistant such as "
            "Lean, a theorem and its proof are written as code, and a small trusted kernel checks every single "
            "inference. <bookmark mark='b'/> No lucky guesses, no hand-waving: a proof is accepted, or it isn't. "
            "<bookmark mark='c'/> For reinforcement learning, that is the perfect reward, one that cannot be hacked, "
            "as long as the formal statement says what was meant. <bookmark mark='d'/> And since 2017 a community "
            "has been formalizing mathematics in Lean's library, Mathlib, which gives such systems something to "
            "build on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(broken))
            vo.wait_until("a")
            self.play(FadeOut(broken))
            self.play(FadeIn(g), FadeIn(gl), FadeIn(sch))
            vo.wait_until("b")
            self.play(FadeIn(ok, scale=1.3), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphaproof(self):
        steps = [(r"$\sim 1$ million problems \\ in words", GREY_B), (r"a Gemini model \\ translates to Lean", POLICY),
                 (r"$\sim 80$ million \\ formal statements", LEAN), (r"AlphaZero-style search \\ for proofs", SEARCH),
                 (r"checked proofs \\ train the network", RIGHT_C)]
        boxes = VGroup(*[node_box(t, c, font_size=28, height=1.0) for t, c in steps])
        boxes[:3].arrange(RIGHT, buff=0.9).move_to([0, 2.0, 0])
        boxes[3].move_to([boxes[2].get_x(), 0.1, 0])
        boxes[4].move_to([boxes[0].get_x() + 0.5, 0.1, 0])
        arrows = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
            Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
            Arrow(boxes[2].get_bottom(), boxes[3].get_top(), buff=0.08, color=GREY_B, stroke_width=3),
            Arrow(boxes[3].get_left(), boxes[4].get_right(), buff=0.08, color=GREY_B, stroke_width=3))
        back = CurvedArrow(boxes[4].get_bottom() + RIGHT * 0.3, boxes[3].get_bottom() + LEFT * 0.3, angle=0.9,
                           color=RIGHT_C, stroke_width=3, tip_length=0.18)
        ttrl = label(r"at test time: \ prove variants of the hard problem, \ and learn from them", font_size=26,
                     color=SEARCH).move_to(DOWN * 1.45)
        hc = history_card(2024, r"IMO 2024: \ AlphaProof and AlphaGeometry 2, \ Google DeepMind",
                          r"$28$ of $42$ points, \ one short of gold; \ four of six problems, \ including the hardest, "
                          r"\ which five contestants solved. \ Some took up to three days", width=8.4,
                          color=LEAN).to_edge(DOWN, buff=0.35)
        cite_ = cite(r"T.~Hubert et al., \textit{Nature} (2025); \ Google DeepMind (2024)", corner=UR)
        with self.voiceover(
            "Google DeepMind's AlphaProof put this to work. <bookmark mark='a'/> A Gemini model translated about a "
            "million maths problems from words into Lean, some eighty million formal statements. Then Part 26's "
            "AlphaZero went to work on them: search for proofs, keep the ones Lean accepts, and train the network on "
            "them, round after round. <bookmark mark='b'/> On the hardest problems it went further: at test time it "
            "generated variants of the problem, proved those, and learned from them, reinforcement learning during "
            "the exam. <bookmark mark='c'/> At the 2024 International Mathematical Olympiad, with AlphaGeometry 2 for "
            "the geometry, it scored 28 of 42, one point short of gold, solving four of the six problems, including "
            "the hardest, which only five contestants solved. Some proofs took it three days."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[i - 1]), FadeIn(b, shift=RIGHT * 0.1))
                                    for i, b in enumerate(boxes) if i], lag_ratio=0.5), run_time=4.0)
            self.play(Create(back))
            vo.wait_until("b")
            self.play(FadeIn(ttrl))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def imo(self):
        rows = [
            (r"2024 \ AlphaProof + AlphaGeometry 2 \ (Lean, days)", 28, LEAN),
            (r"2025 \ Gemini Deep Think \ (words, $4\tfrac12$ hours)", 35, POLICY),
            (r"2025 \ OpenAI experimental model \ (words)", 35, POLICY),
        ]
        W = 6.0
        g = VGroup()
        for i, (t, v, c) in enumerate(rows):
            y = 1.6 - i * 1.0
            name = label(t, font_size=21, color=GREY_A).move_to([-1.4, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=W * v / 42, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bar.move_to([-1.2 + W * v / 84, y, 0])
            val = label(rf"${v}$", font_size=24, color=c).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(name, bar, val))
        x0 = -1.2
        golds = VGroup(
            DashedLine([x0 + W * 29 / 42, 2.2, 0], [x0 + W * 29 / 42, 1.25, 0], color=C.BITS, dash_length=0.06),
            DashedLine([x0 + W * 35 / 42, 1.25, 0], [x0 + W * 35 / 42, -0.75, 0], color=C.BITS, dash_length=0.06))
        gl = VGroup(label(r"gold: $29$", font_size=18, color=C.BITS).next_to(golds[0], UP, buff=0.05),
                    label(r"gold: $35$", font_size=18, color=C.BITS).next_to(golds[1], DOWN, buff=0.05))
        head = label(r"points of $42$ at the International Mathematical Olympiad", font_size=24, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        notes = VGroup(
            label(r"Deep Think: \ graded and certified by the IMO's coordinators; \ OpenAI's: \ graded by former "
                  r"medallists", font_size=20, color=GREY_B),
            label(r"formal provers in 2025: \ Harmonic's Aristotle \ and ByteDance's Seed-Prover \ proved five of six "
                  r"in Lean", font_size=20, color=LEAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.95)
        cite_ = cite(r"Google DeepMind (July 2025); \ Harmonic (2025); \ ByteDance Seed (2025)", corner=DR)
        with self.voiceover(
            "A year later the picture changed. <bookmark mark='a'/> At the 2025 Olympiad, a version of Google's Gemini "
            "with Deep Think, which explores many lines of thought in parallel, solved five of the six problems, 35 "
            "points, exactly the gold-medal line, writing in plain English, within the four and a half hours; the "
            "Olympiad's own coordinators graded it. <bookmark mark='b'/> OpenAI announced the same score for an "
            "experimental reasoning model, graded by former medallists. <bookmark mark='c'/> And formal provers "
            "caught up too: Harmonic's Aristotle and ByteDance's Seed-Prover each proved five of the six in Lean, "
            "every step checked. A year earlier, the best systems had needed days, and people to translate the problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(g[0]), Create(golds[0]), FadeIn(gl[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]), Create(golds[1]), FadeIn(gl[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        line = Arrow([-6.2, 0.4, 0], [6.2, 0.4, 0], buff=0, color=GREY_B, stroke_width=3)
        head = label(r"the checkers reasoning learns from", font_size=34).to_edge(UP, buff=0.5)
        exs = [r"the kernel: \\ yes or no", r"AIME, \\ GSM8K", r"unit tests", r"chapter three", r"essays, \\ advice"]
        items = [(-5.2, r"a proof \\ in Lean", LEAN), (-2.8, r"a number \\ to match", RIGHT_C),
                 (-0.5, r"code \\ and its tests", CHAIN), (1.9, r"a process \\ grader", PRM_C),
                 (4.5, r"a model \\ as judge", WRONG_C)]
        marks = VGroup()
        for (x, t, c), e in zip(items, exs):
            marks.add(VGroup(Dot([x, 0.4, 0], radius=0.09, color=c), label(t, font_size=24, color=c).next_to([x, 0.4, 0],
                                                                                                        UP, buff=0.3),
                             label(e, font_size=19, color=GREY_B).next_to([x, 0.4, 0], DOWN, buff=0.3)))
        ends = VGroup(label(r"exact, \ unhackable", font_size=24, color=RIGHT_C).move_to([-4.6, 2.0, 0]),
                      label(r"learned, \ hackable", font_size=24, color=WRONG_C).move_to([4.6, 2.0, 0]))
        take = label(r"reinforcement learning advances fastest \ where the checker is exact", font_size=28, color=SEARCH)
        take.to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "So here is the spectrum every reasoning method lives on. <bookmark mark='a'/> At one end, checkers that "
            "cannot be fooled: a proof in Lean, a number to match, code that must pass its tests. <bookmark mark='b'/> "
            "At the other, learned graders, a process reward model, or another model acting as judge, which a strong "
            "enough optimizer will find ways around. <bookmark mark='c'/> Reasoning has advanced fastest exactly where "
            "the checker is exact: mathematics and code. Stretching it to everything else, essays, advice, research, "
            "is where the hard problems are."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks[:3]], lag_ratio=0.4), FadeIn(ends[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks[3:]], lag_ratio=0.4), FadeIn(ends[1]))
            vo.wait_until("c")
            self.play(FadeIn(take))
        self.wait(0.3)
        self.clear_scene()
