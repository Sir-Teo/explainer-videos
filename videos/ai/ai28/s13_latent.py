from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, DIRECT, FILLER, PART, POLICY, RIGHT_C, WRONG_C, load, node_box

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
        h = VGroup(*[Rectangle(width=0.16, height=0.16 + 0.9 * abs(np.sin(1.7 * i)), stroke_width=0, fill_color=LATENT,
                               fill_opacity=0.85) for i in range(24)]).arrange(RIGHT, buff=0.03, aligned_edge=DOWN)
        h.move_to([-4.2, 1.3, 0])
        hl = label(r"the last hidden state: \\ thousands of numbers", font_size=22, color=LATENT).next_to(h, DOWN, buff=0.2)
        tok = node_box(r"one token", CHAIN, font_size=24).move_to([0.2, 1.3, 0])
        tl = label(r"about $17$ bits, \\ from a vocabulary of $100{,}000$", font_size=22, color=CHAIN).next_to(tok, DOWN, buff=0.2)
        h2 = h.copy().move_to([4.5, 1.3, 0])
        h2l = label(r"the next input", font_size=22, color=GREY_A).next_to(h2, DOWN, buff=0.2)
        a1 = Arrow(h.get_right(), tok.get_left(), buff=0.15, color=GREY_B)
        a2 = Arrow(tok.get_right(), h2.get_left(), buff=0.15, color=GREY_B)
        sq = label(r"squeeze", font_size=20, color=GREY_B).next_to(a1, UP, buff=0.05)
        sch = note(r"schematic").to_corner(DR, buff=0.3)
        rec = label(rf"chapter one, \ $16$ bits: \ dots ${100 * fd:.0f}\%$, \ at once ${100 * dd:.0f}\%$", font_size=24,
                    color=FILLER).move_to(DOWN * 1.4)
        q = label(r"what if the model passed its state on directly, \ without writing it down?", font_size=28,
                  color=LATENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A chain of thought is computation, but it has a narrow throat. <bookmark mark='a'/> Each step, the "
            "model's last hidden state, thousands of numbers, is squeezed into a single token: with a vocabulary of a "
            "hundred thousand, about seventeen bits. <bookmark mark='b'/> Then the token is turned back into numbers "
            "for the next step. Everything the model carries forward must fit through that throat. "
            f"<bookmark mark='c'/> {dots} <bookmark mark='d'/> So why not pass the state on directly?"
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(hl), GrowArrow(a1), FadeIn(sq), FadeIn(tok), FadeIn(tl))
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
        def col(x, kind):
            g = VGroup(*[RoundedRectangle(width=0.7, height=0.32, corner_radius=0.06, stroke_color=GREY_C,
                                          stroke_width=1.5, fill_color=GREY_D, fill_opacity=0.3) for _ in range(3)])
            g.arrange(UP, buff=0.12).move_to([x, 0, 0])
            return g

        top_y = 1.6
        cot, coc = VGroup(), VGroup()
        for row, (g_, y, kind) in enumerate(((cot, top_y, "token"), (coc, -1.4, "latent"))):
            xs = [-4.6 + 1.9 * i for i in range(5)]
            stacks = VGroup(*[col(x, kind).shift(UP * y) for x in xs])
            g_.add(stacks)
            links = VGroup()
            for i in range(4):
                a, b = stacks[i], stacks[i + 1]
                if kind == "token":
                    t = node_box(r"tok", CHAIN, font_size=16, height=0.36).move_to((a.get_top() + b.get_bottom()) / 2 +
                                                                                   UP * 0.35)
                    links.add(VGroup(Arrow(a.get_top(), t.get_left(), buff=0.05, stroke_width=2, color=CHAIN,
                                           max_tip_length_to_length_ratio=0.2),
                                     t, Arrow(t.get_right(), b.get_bottom(), buff=0.05, stroke_width=2, color=CHAIN,
                                              max_tip_length_to_length_ratio=0.2)))
                else:
                    links.add(CurvedArrow(a.get_top() + RIGHT * 0.1, b.get_bottom() + LEFT * 0.1, angle=-1.4,
                                          stroke_width=3, color=LATENT, tip_length=0.15))
            g_.add(links)
        l1 = label(r"chain of thought: \ state $\to$ token $\to$ state", font_size=24, color=CHAIN)
        l1.next_to(cot, LEFT, buff=0.3).shift(RIGHT * 0.2)
        l1.move_to([4.5, top_y + 1.1, 0])
        l2 = label(r"continuous thought: \ the state goes straight back in", font_size=24, color=LATENT)
        l2.move_to([4.5, -1.4 + 1.1, 0])
        hc = history_card(2024, r"S.~Hao et al., \ Meta: \ \textit{Coconut}", r"continuous thoughts can hold several "
                          r"possible next steps at once: \ a breadth-first search; \ better than a chain of thought on "
                          r"logic puzzles that need search", width=5.4, color=LATENT).to_corner(DR, buff=0.25)
        sch = note(r"schematic").to_corner(UL, buff=0.3)
        with self.voiceover(
            "That is Coconut, from Shibo Hao and colleagues at Meta, in December 2024. <bookmark mark='a'/> In a "
            "chain of thought, each step's state is turned into a token, and the token back into a state. "
            "<bookmark mark='b'/> In Coconut, for a stretch of reasoning, the last hidden state goes straight back in "
            "as the next input: a continuous thought. It is trained with a curriculum that replaces written steps "
            "with continuous ones, a few at a time. <bookmark mark='c'/> Something unexpected came out. A continuous "
            "thought need not commit to one next step: it can hold several at once, so the model searches "
            "breadth-first. On logic puzzles that need search, it beat a written chain of thought."
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(cot[0]), LaggedStart(*[FadeIn(l_) for l_ in cot[1]], lag_ratio=0.3), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(coc[0]), LaggedStart(*[Create(l_) for l_ in coc[1]], lag_ratio=0.3), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.15))
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
            tab.add(VGroup(label(t, font_size=22, color=GREY_A).move_to([-5.0, -0.2 - 0.55 * i, 0], aligned_edge=LEFT),
                           label(rf"${v:g}\%$", font_size=22, color=LATENT).move_to([-1.2, -0.2 - 0.55 * i, 0])))
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
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(th), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2))
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
                  r"Tiny Networks} (2025): \ first prize, \ ARC Prize 2025 papers", font_size=18).to_edge(UP, buff=0.25)
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
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(net), FadeIn(x), GrowArrow(a_xz), FadeIn(z), FadeIn(y))
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
        left = VGroup(label(r"written thought", font_size=28, color=CHAIN),
                      label(r"we can read it: \ catch a plan to cheat \\ before it happens", font_size=22, color=GREY_A))
        right = VGroup(label(r"latent thought", font_size=28, color=LATENT),
                       label(r"more efficient, \ possibly more capable, \\ but unreadable", font_size=22, color=GREY_A))
        for g_ in (left, right):
            g_.arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=2.0).move_to(UP * 0.8)
        vs = MathTex(r"\longleftrightarrow", font_size=48, color=GREY_C).move_to(UP * 0.8)
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
            self.play(FadeIn(left), FadeIn(vs), FadeIn(right))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(Indicate(right[0], color=LATENT))
        self.wait(0.3)
        self.clear_scene()
