from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, DIRECT, LEAN, MONO, PART, PASS, POLICY, VOTE, RIGHT_C


def hbars(rows, x0=-1.2, width=4.6, row_h=0.62, font_size=22, top=2.0, vmax=100.0):
    """Horizontal bars: (label, value in percent, colour).  Labels right-aligned at x0, values after the bars."""
    g = VGroup()
    for i, (txt, v, col) in enumerate(rows):
        y = top - i * row_h
        name = label(txt, font_size=font_size, color=GREY_A)
        name.move_to([x0 - 0.2 - name.width / 2, y, 0])
        w = max(width * v / vmax, 0.02)
        bar = Rectangle(width=w, height=row_h * 0.62, stroke_width=0, fill_color=col, fill_opacity=0.9)
        bar.move_to([x0 + w / 2, y, 0])
        val = label(rf"${v:g}\%$", font_size=font_size, color=col).next_to(bar, RIGHT, buff=0.12)
        g.add(VGroup(name, bar, val))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.prompting()
        self.rl_era()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def prompting(self):
        strip = timeline(lit=(2022, 2025)).to_edge(DOWN, buff=0.35)
        hc = history_card(2022, r"Wei et al., \ Google: \ \textit{Chain-of-thought prompting}",
                          r"eight worked examples in the prompt, \ the reasoning written out", width=6.4,
                          color=CHAIN).move_to([-3.3, 2.45, 0])
        hk = history_card(2022, r"Kojima et al., \ Tokyo and Google: \ \textit{Large language models are zero-shot "
                          r"reasoners}", r"one sentence: \ ``Let's think step by step.''", width=6.4,
                          color=CHAIN).move_to([3.4, 2.45, 0])
        b1 = hbars([(r"answer at once", 17.9, DIRECT), (r"chain of thought", 56.9, CHAIN)], x0=-4.3, width=3.0,
                   top=0.75, font_size=22, row_h=0.62)
        t1 = label(r"PaLM 540B, \ grade-school maths \ (GSM8K)", font_size=20, color=GREY_B).next_to(b1, UP, buff=0.15)
        b2 = hbars([(r"answer at once", 17.7, DIRECT), (r"``let's think step by step''", 78.7, CHAIN)], x0=2.9,
                   width=3.0, top=0.75, font_size=22, row_h=0.62)
        t2 = label(r"InstructGPT, \ arithmetic word problems \ (MultiArith)", font_size=20, color=GREY_B)
        t2.next_to(b2, UP, buff=0.15)
        ex_q = data_text("Q: Roger has 5 tennis balls. He buys 2 more cans of\ntennis balls. Each can has 3 tennis "
                         "balls. How many\ntennis balls does he have now?", font=MONO, font_size=14, color=GREY_A,
                         line_spacing=0.8)
        ex_a = data_text("A: Roger started with 5 balls. 2 cans of 3 tennis balls\neach is 6 tennis balls. 5 + 6 = 11. "
                         "The answer is 11.", font=MONO, font_size=14, color=CHAIN, line_spacing=0.8)
        ex = VGroup(ex_q, ex_a).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        exl = label(r"one of the eight examples \ (the paper's Figure 1)", font_size=18, color=GREY_B)
        exg = VGroup(exl, ex).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.3, -1.15, 0])
        zs = VGroup(data_text("Q: <any question>", font=MONO, font_size=17, color=GREY_A),
                    data_text("A: Let's think step by step.", font=MONO, font_size=17, color=CHAIN))
        zs.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        zl = label(r"no examples at all", font_size=18, color=GREY_B)
        zg = VGroup(zl, zs).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -1.15, 0])
        cite_ = cite(r"J.~Wei et al.\ (2022); \ T.~Kojima et al.\ (2022): \ share of problems solved", corner=DL)
        cite_.next_to(strip, UP, buff=0.12).to_edge(LEFT, buff=0.3)
        with self.voiceover(
            "In January 2022, a team at Google tried something simple. Instead of showing a large language model "
            "a few questions with their answers, they showed it eight questions with the working written out. "
            "<bookmark mark='a'/> On grade-school maths word problems, Google's 540-billion-parameter PaLM went "
            "from 18 percent right to 57: it wrote out its own working, and got far more right. "
            "<bookmark mark='b'/> Four months later, a team from Tokyo and Google found you didn't even need the "
            "examples. One sentence, let's think step by step, took one of OpenAI's models from 18 to 79 percent on "
            "arithmetic word problems. <bookmark mark='c'/> The ability was already in the model. It only had to be "
            "asked to write its reasoning down."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(hc, shift=UP * 0.2))
            self.play(FadeIn(exg, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                                for r_ in b1], lag_ratio=0.6), FadeIn(cite_), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hk, shift=UP * 0.2), FadeIn(zg, shift=UP * 0.1))
            self.play(FadeIn(t2), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                                for r_ in b2], lag_ratio=0.6), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(b1[1][1], color=CHAIN), Indicate(b2[1][1], color=CHAIN), Indicate(ex_a, color=CHAIN))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rl_era(self):
        rows = [
            (r"GPT-4o", 12, DIRECT),
            (r"o1, \ one try", 74, POLICY),
            (r"o1, \ a vote of $64$", 83, VOTE),
            (r"o1, \ best of $1{,}000$ by a learned scorer", 93, PASS),
            (r"R1-Zero, \ before RL", 15.6, DIRECT),
            (r"R1-Zero, \ after RL", 71.0, POLICY),
            (r"R1-Zero, \ a vote of $64$", 86.7, VOTE),
        ]
        bars = hbars(rows, x0=-1.9, width=3.3, row_h=0.56, font_size=20, top=1.9)
        head = label(r"AIME 2024: \ share of the problems solved", font_size=26).next_to(bars, UP, buff=0.3)
        head.align_to(bars, LEFT)
        sep = DashedLine(bars[3].get_corner(DL) + DOWN * 0.08 + LEFT * 3.6, bars[3].get_corner(DR) + DOWN * 0.08
                         + RIGHT * 0.7, color=GREY_D, dash_length=0.06)
        src = note(r"self-reported: \ OpenAI (Sept 2024); \ DeepSeek-AI (Jan 2025)").to_corner(DL, buff=0.3)
        o1 = history_card(2024, r"OpenAI o1 \ (September)", r"trained with reinforcement learning to think before it "
                          r"answers: \ a long chain of thought, \ hidden from the user", width=4.6,
                          color=POLICY).move_to([4.6, 1.2, 0])
        imo = history_card(2025, r"International Mathematical Olympiad",
                           r"Gemini Deep Think: \ $35$ of $42$ points, \ gold-medal level, \ in plain language, \ "
                           r"within the $4\tfrac12$ hours; \ graded by the IMO's coordinators. \ OpenAI reported the "
                           r"same score", width=4.6, color=LEAN).move_to([4.6, 1.2, 0])
        arc = history_card(2026, r"ARC-AGI-3 \ (March)", r"games no model has seen: \ people solve all of them, \ "
                           r"every frontier model at launch \ below $1\%$", width=4.6, color=C.SURPRISE)
        arc.next_to(imo, DOWN, buff=0.25)
        if arc.get_bottom()[1] < -3.7:
            VGroup(imo, arc).shift(UP * (-3.7 - arc.get_bottom()[1]))
        with self.voiceover(
            "For two years that was the method: ask for a chain of thought, sample a few, perhaps take a vote. Then, "
            "in September 2024, OpenAI released o1, trained with reinforcement learning to think before it answers. "
            "<bookmark mark='a'/> On the 2024 American Invitational Mathematics Examination, AIME, GPT-4o had solved "
            "12 percent of the problems. <bookmark mark='b'/> o1 solved 74 percent with one try, 83 with a vote "
            "over sixty-four, and 93 when a learned scorer picked from a thousand. <bookmark mark='c'/> In January "
            "2025, DeepSeek showed how. R1-Zero: reinforcement learning straight from a base model, rewarded only "
            "for right answers. It climbed from 16 percent to 71, and to 87 with a vote, and its weights were "
            "open. <bookmark mark='d'/> In July 2025, systems wrote gold-medal solutions at the International "
            "Mathematical Olympiad, in plain language, within the time limit. <bookmark mark='e'/> And yet when "
            "ARC-AGI-3, a set of games no model had seen, launched in March 2026, every frontier model scored "
            "below one percent, while people solved them all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(o1, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                    for r_ in bars[1:4]], lag_ratio=0.7), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(sep))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                    for r_ in bars[4:]], lag_ratio=0.7), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeOut(o1, shift=UP * 0.2), FadeIn(imo, shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(arc, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How does a model learn to think, \\ and what does thinking buy?", font_size=42).move_to(UP * 1.6)
        steps = [(r"a chain of thought", CHAIN), (r"many chains, \ one vote", VOTE), (r"checking the steps", C.NEURAL),
                 (r"learning from a checker", POLICY), (r"thinking longer", C.LENGTH), (r"search", PASS),
                 (r"proofs", LEAN)]
        path = VGroup()
        for i, (t, c) in enumerate(steps):
            if i:
                path.add(MathTex(r"\to", font_size=34, color=GREY_C))
            path.add(label(t, font_size=30, color=c))
        row1, row2 = VGroup(*path[:8]), VGroup(*path[7:])
        row1.arrange(RIGHT, buff=0.2)
        row2 = VGroup(*path[8:]).arrange(RIGHT, buff=0.2)
        VGroup(row1, row2).arrange(DOWN, buff=0.4).move_to(DOWN * 0.5)
        ours = label(r"and all of it tried here, \ on tiny models trained on this computer", font_size=28,
                     color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That is the question of this part: how does a model learn to think, and what does thinking buy? "
            "<bookmark mark='a'/> We'll follow the field's own path: why writing a chain of thought adds "
            "computation; sampling many chains and voting; checking the steps; reinforcement learning from a "
            "checker of answers, derived; what thinking longer buys; search; and proofs a machine can check. "
            "<bookmark mark='b'/> And we'll try each idea here, on tiny models trained on the computer making this "
            "video."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in path], lag_ratio=0.15), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Reasoning", font_size=48).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"why writing steps adds computation: \ depth, \ TC$^0$, \ chains of thought",
            r"many chains and a vote; \ checking answers or checking steps",
            r"reinforcement learning from a checker: \ GRPO derived, \ the KL estimators, \ Dr.~GRPO, DAPO, GSPO, CISPO",
            r"what that training does: \ entropy, \ length, \ and does it widen what a model can solve?",
            r"thinking at answer time: \ parallel or sequential, \ budgets, \ best-of-$N$, \ search",
            r"the frontier: \ thinking without words, \ tiny recursive models, \ formal proofs, \ ARC-AGI",
        ], font_size=25)
        with self.voiceover(
            "This is Part 28 of AI, Built, the third part of the act on agency. <bookmark mark='a'/> In this part: "
            "why writing steps adds computation; many chains and a vote, and checking steps instead of answers; "
            "reinforcement learning from a checker, with GRPO derived and its successors; what that training does "
            "to a model, to its uncertainty, to how long it thinks, and to what it can solve at all; how to spend "
            "computation at answer time; and the frontier: thinking without words, tiny recursive models, formal "
            "proofs, and puzzles no model has seen."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
