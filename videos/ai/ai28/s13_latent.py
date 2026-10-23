from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, FILLER, PART, POLICY, RIGHT_C, WRONG_C, load, node_box

LATENT = C.LATENT if hasattr(C, "LATENT") else GREEN_B


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.bottleneck()
        self.coconut()
        self.tiny()
        self.trm()
        self.monitor()

    def card(self):
        card = chapter_card(12, r"Thinking without words", r"Must a model think in tokens?", lit=(2024, 2025),
                            part=PART)
        with self.voiceover("Chapter twelve. Thinking without words."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bottleneck(self):
        p = load("parity")
        fd = float(np.mean(p["accs_filler16"]))
        dd = float(np.mean(p["accs_direct16"]))
        if fd < dd + 0.1:
            dots = ("In chapter one, giving our model meaningless dots instead of words didn't help: positions are not "
                    "the point; carrying state forward is.")
        else:
            dots = (f"In chapter one, meaningless dots helped our model a little, {100 * fd:.0f} percent against "
                    f"{100 * dd:.0f}, but nowhere near a written chain: carrying state forward is the point.")
        # a hidden state (many numbers) squeezed into one token, and back
        h = VGroup(*[Rectangle(width=0.2, height=0.2 + 1.6 * abs(np.sin(1.7 * i)), stroke_width=0, fill_color=LATENT,
                               fill_opacity=0.85) for i in range(20)]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
        h.move_to([-4.3, 1.0, 0])
        hl = label(r"the last hidden state: \\ thousands of numbers", font_size=24, color=LATENT).next_to(h, DOWN, buff=0.25)
        tok = node_box(r"one token", CHAIN, font_size=30).move_to([0.0, 1.0, 0])
        tl = label(r"about $17$ bits, \\ from a vocabulary of $100{,}000$", font_size=24, color=CHAIN).next_to(tok, DOWN, buff=0.25)
        h2 = h.copy().move_to([4.4, 1.0, 0])
        bits = label(r"for example, \ $4096$ numbers of $16$ bits each: \ $65{,}536$ bits \ $\to$ \ $17$ bits",
                     font_size=26, color=GREY_A).move_to(DOWN * 1.05)
        h2l = label(r"the next input", font_size=24, color=GREY_A).next_to(h2, DOWN, buff=0.25)
        a1 = Arrow(h.get_right(), tok.get_left(), buff=0.15, color=GREY_B)
        a2 = Arrow(tok.get_right(), h2.get_left(), buff=0.15, color=GREY_B)
        sq = label(r"squeeze", font_size=22, color=GREY_B).next_to(a1, UP, buff=0.05)
        head = label(r"a chain of thought has a narrow throat", font_size=34).to_edge(UP, buff=0.5)
        sch = note(r"schematic").to_corner(DR, buff=0.3)
        rec = label(rf"chapter one, \ $16$ bits: \ dots ${100 * fd:.0f}\%$, \ at once ${100 * dd:.0f}\%$", font_size=26,
                    color=FILLER).move_to(DOWN * 2.0)
        q = label(r"what if the model passed its state on directly, \ without writing it down?", font_size=28,
                  color=LATENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A chain of thought is computation, but it has a narrow throat. <bookmark mark='a'/> Each step, the "
            "model's last hidden state, thousands of numbers, is squeezed into a single token: with a vocabulary of a "
            "hundred thousand, about seventeen bits. <bookmark mark='b'/> Then the token is turned back into numbers "
            "for the next step. Everything the model carries forward must fit through that throat. "
            f"<bookmark mark='c'/> {dots} <bookmark mark='d'/> So why not pass the state on directly?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(sch), FadeIn(h), FadeIn(hl))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(sq), FadeIn(tok), FadeIn(tl))
            self.play(FadeIn(bits))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(h2), FadeIn(h2l))
            vo.wait_until("c")
            self.play(FadeIn(rec))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coconut(self):
        def col(x, y):
            g = VGroup(*[RoundedRectangle(width=1.0, height=0.4, corner_radius=0.07, stroke_color=GREY_C,
                                          stroke_width=1.8, fill_color=GREY_D, fill_opacity=0.3) for _ in range(3)])
            return g.arrange(UP, buff=0.14).move_to([x, y, 0])

        xs = [-5.2 + 2.6 * i for i in range(5)]
        rows = {}
        for kind, y in (("token", 1.55), ("latent", -1.1)):
            stacks = VGroup(*[col(x, y) for x in xs])
            links = VGroup()
            for i in range(4):
                a, b = stacks[i], stacks[i + 1]
                if kind == "token":
                    t = node_box(r"tok", CHAIN, font_size=20, height=0.42).move_to([(xs[i] + xs[i + 1]) / 2, y, 0])
                    links.add(VGroup(Arrow(a[2].get_right(), t.get_top(), buff=0.06, stroke_width=3, color=CHAIN,
                                           max_tip_length_to_length_ratio=0.15),
                                     t, Arrow(t.get_bottom(), b[0].get_left(), buff=0.06, stroke_width=3, color=CHAIN,
                                              max_tip_length_to_length_ratio=0.15)))
                else:
                    links.add(CurvedArrow(a[2].get_right(), b[0].get_left(), angle=-1.6, stroke_width=4, color=LATENT,
                                          tip_length=0.18))
            rows[kind] = VGroup(stacks, links)
        l1 = label(r"chain of thought: \ state $\to$ token $\to$ state", font_size=26, color=CHAIN)
        l1.next_to(rows["token"], UP, buff=0.25).align_to(rows["token"], LEFT)
        l2 = label(r"continuous thought: \ the state goes straight back in", font_size=26, color=LATENT)
        l2.next_to(rows["latent"], UP, buff=0.25).align_to(rows["latent"], LEFT)
        hc = history_card(2024, r"S.~Hao et al., \ Meta: \ \textit{Coconut}", r"continuous thoughts can hold several "
                          r"possible next steps at once: \ a breadth-first search; \ better than a chain of thought on "
                          r"logic puzzles that need search", width=9.0, color=LATENT).to_edge(DOWN, buff=0.2)
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "That is Coconut, from Shibo Hao and colleagues at Meta, in December 2024. <bookmark mark='a'/> In a "
            "chain of thought, each step's state is turned into a token, and the token back into a state. "
            "<bookmark mark='b'/> In Coconut, for a stretch of reasoning, the last hidden state goes straight back in "
            "as the next input: a continuous thought. It is trained with a curriculum that replaces written steps "
            "with continuous ones, a few at a time. <bookmark mark='c'/> Something unexpected came out. A continuous "
            "thought need not commit to one next step: it can hold several at once, so the model searches "
            "breadth-first. On logic puzzles that need search, it beat a written chain of thought."
        ) as vo:
            self.play(FadeIn(sch), FadeIn(rows["token"][0]), FadeIn(rows["latent"][0]), FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in rows["token"][1]], lag_ratio=0.3), FadeIn(l1))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in rows["latent"][1]], lag_ratio=0.3), FadeIn(l2))
            vo.wait_until("c")
            self.play(Indicate(hc, color=LATENT, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiny(self):
        hc = history_card(2025, r"G.~Wang et al., \ Sapient: \ \textit{Hierarchical Reasoning Model}",
                          r"$27$ million parameters, \ about $1{,}000$ training examples, \ no pretraining: \ a slow module "
                          r"and a fast one, \ recurring", width=6.6, color=LATENT).move_to([-3.25, 2.0, 0])
        rows = [(r"Sudoku-Extreme", 55.0), (r"Maze-Hard", 74.5), (r"ARC-AGI-1", 40.3), (r"ARC-AGI-2", 5.0)]
        tab = VGroup()
        for i, (t, v) in enumerate(rows):
            tab.add(VGroup(label(t, font_size=26, color=GREY_A).move_to([-5.6, -0.2 - 0.7 * i, 0], aligned_edge=LEFT),
                           label(rf"${v:g}\%$", font_size=26, color=LATENT).move_to([-1.2, -0.2 - 0.7 * i, 0])))
        th = label(r"as reported", font_size=20, color=GREY_B).next_to(tab, UP, buff=0.2).align_to(tab, LEFT)
        ap = history_card(2025, r"ARC Prize's analysis \ (August)", r"reproduced: \ $32\%$ on ARC-AGI-1, \ $2\%$ on "
                          r"ARC-AGI-2. \ The two-level hierarchy barely mattered \ (a same-size transformer came within "
                          r"about $5$ points); \ the outer loop of refinement did", width=6.2,
                          color=C.SURPRISE).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "A second line of work drops the language model altogether. <bookmark mark='a'/> In June 2025, Sapient "
            "Intelligence's Hierarchical Reasoning Model, only twenty-seven million parameters, trained from scratch on "
            "about a thousand examples per task, scored 55 percent on extreme Sudoku and 74 percent on hard mazes, and "
            "reported 40 percent on ARC-AGI-1, puzzles we'll meet in chapter fourteen. Its idea: two recurrent modules, a slow one that plans and a fast "
            "one that computes, iterating many times before answering. <bookmark mark='b'/> The ARC Prize team "
            "checked. They reproduced most of the result, 32 percent on their held-out set, but found the hierarchy "
            "barely mattered: a transformer of the same size came within about five points. What mattered was an "
            "outer loop: the model's answer fed back in and refined, again and again."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(th), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(ap, shift=LEFT * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trm(self):
        net = node_box(r"one $2$-layer network", POLICY, font_size=24).move_to([0, 0.3, 0])
        x = node_box(r"$x$: \ the puzzle", GREY_B, font_size=22).move_to([-4.6, 0.3, 0])
        z = node_box(r"$z$: \ a latent scratchpad", LATENT, font_size=22).move_to([0, 2.3, 0])
        y = node_box(r"$y$: \ the current answer", RIGHT_C, font_size=22).move_to([4.4, 0.3, 0])
        a_xz = Arrow(x.get_right(), net.get_left(), buff=0.1, color=GREY_B)
        loop_z = CurvedArrow(net.get_top() + LEFT * 0.4, z.get_bottom() + LEFT * 0.4, angle=-0.9, color=LATENT,
                             stroke_width=3, tip_length=0.15)
        back_z = CurvedArrow(z.get_bottom() + RIGHT * 0.4, net.get_top() + RIGHT * 0.4, angle=-0.9, color=LATENT,
                             stroke_width=3, tip_length=0.15)
        nz = label(r"update $z$, \ $6$ times", font_size=20, color=LATENT).next_to(z, RIGHT, buff=0.3)
        a_y = Arrow(net.get_right(), y.get_left(), buff=0.1, color=RIGHT_C)
        ny = label(r"then improve $y$", font_size=20, color=RIGHT_C).next_to(a_y, DOWN, buff=0.1)
        outer = CurvedArrow(y.get_bottom() + DOWN * 0.05, net.get_bottom() + DOWN * 0.05, angle=-1.2, color=GREY_A,
                            stroke_width=2.5, tip_length=0.15)
        no = label(r"repeat; \ checked after each round, \ up to $16$ rounds \ (deep supervision)", font_size=20,
                   color=GREY_A).move_to([0.6, -1.6, 0])
        res = VGroup(label(r"$7$ million parameters", font_size=24, color=POLICY),
                     label(r"Sudoku-Extreme $87.4\%$, \ Maze-Hard $85.3\%$", font_size=22, color=GREY_A),
                     label(r"ARC-AGI-1 $44.6\%$, \ ARC-AGI-2 $7.8\%$", font_size=22, color=GREY_A))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3).shift(LEFT * 3.2)
        hc = note(r"A.~Jolicoeur-Martineau, \ Samsung SAIL Montr\'eal, \textit{Less is More: Recursive Reasoning with "
                  r"Tiny Networks} (2025) \\ first prize, \ ARC Prize 2025 papers", font_size=20).to_edge(UP, buff=0.25)
        with self.voiceover(
            "In October 2025, Alexia Jolicoeur-Martineau at Samsung's lab in Montreal stripped the idea to its core. "
            "<bookmark mark='a'/> One tiny network, two layers. It reads the puzzle, x, and keeps two things: a latent "
            "scratchpad z, and its current answer y. <bookmark mark='b'/> It updates the scratchpad six times, then "
            "uses it to improve the answer. <bookmark mark='c'/> Then it does it all again, and its answer is checked "
            "after every round, up to sixteen of them. <bookmark mark='d'/> With seven million parameters, it beat the "
            "Hierarchical Reasoning Model on every task: 87 percent on extreme Sudoku against 55, and 45 percent on "
            "ARC-AGI-1, ahead of many large language models. It won the first prize for papers in the 2025 ARC Prize. "
            "Depth through recurrence, instead of through tokens."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(net))
            vo.wait_until("a")
            self.play(FadeIn(x), GrowArrow(a_xz), FadeIn(z), FadeIn(y))
            vo.wait_until("b")
            self.play(Create(loop_z), Create(back_z), FadeIn(nz))
            self.play(GrowArrow(a_y), FadeIn(ny))
            vo.wait_until("c")
            self.play(Create(outer), FadeIn(no))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monitor(self):
        def toks():
            return VGroup(*[node_box(r"tok", CHAIN, font_size=22, height=0.45) for _ in range(4)]).arrange(RIGHT, buff=0.15)

        def vecs():
            return VGroup(*[VGroup(*[Rectangle(width=0.09, height=0.1 + 0.5 * abs(np.sin(2.3 * i + 1.1 * j)),
                                               stroke_width=0, fill_color=LATENT, fill_opacity=0.85) for i in range(6)])
                            .arrange(RIGHT, buff=0.03, aligned_edge=DOWN) for j in range(4)]).arrange(RIGHT, buff=0.25)

        left = VGroup(toks(), label(r"written thought", font_size=32, color=CHAIN),
                      label(r"we can read it: \ catch a plan to cheat \\ before it happens", font_size=26, color=GREY_A))
        right = VGroup(vecs(), label(r"latent thought", font_size=32, color=LATENT),
                       label(r"more efficient, \ possibly more capable, \\ but unreadable", font_size=26, color=GREY_A))
        for g_ in (left, right):
            g_.arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.8).move_to(UP * 0.7)
        vs = MathTex(r"\longleftrightarrow", font_size=56, color=GREY_C).move_to([0, left[1].get_y(), 0])
        head = label(r"the price of thinking without words", font_size=34).to_edge(UP, buff=0.5)
        hc = history_card(2025, r"T.~Korbak et al., \ from OpenAI, Google DeepMind, Anthropic and others",
                          r"\textit{Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety}",
                          width=8.6, color=WRONG_C).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There's a price. A chain written in words can be read. <bookmark mark='a'/> In 2025, researchers from "
            "many labs together called this a new and fragile opportunity for safety: if a model plans to cheat, its "
            "written chain of thought may say so before it acts. <bookmark mark='b'/> Thinking in vectors may be more "
            "efficient, but nobody can read it. Whether we can trust what a chain of thought says is a question for "
            "Parts 30 and 31."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(vs), FadeIn(right))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(Indicate(right[0], color=LATENT))
        self.wait(0.3)
        self.clear_scene()
