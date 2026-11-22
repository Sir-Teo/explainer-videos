from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class Confluence(WatchScene):
    def construct(self):
        self.card()
        self.graph_small()
        self.diamond()

    def card(self):
        self.chapter(6, r"Church--Rosser, \ and de Bruijn", r"Can two orders give two answers?", lit=(1936,), extra=((1936, r"Church and Rosser; \ Turing"),), part=PART, said="Chapter six. Church Rosser, and de Bruijn.")

    def graph_small(self):
        c = load("confluence")["small"]
        head = label(r"Every way to reduce one term", font_size=34).to_edge(UP, buff=0.3)
        pos = [(0, 2.3), (-3.0, 0.9), (3.0, 0.9), (-4.4, -0.6), (-1.6, -0.6), (0, -2.1)]
        nodes = []
        for (x, y), s in zip(pos, c["nodes"]):
            t = mono(s.replace("\\", "λ"), 17, YES if s == c["nodes"][c["normal"][0]] else CODE)
            r = SurroundingRectangle(t, buff=0.12, corner_radius=0.08, color=GREY_D, stroke_width=1.2)
            nodes.append(VGroup(r, t).move_to([x, y, 0]))
        edges = VGroup(*[Arrow(nodes[i][0].get_bottom(), nodes[j][0].get_top(), buff=0.05, color=GREY_B,
                               stroke_width=2, tip_length=0.13) for i, j in c["edges"]])
        cap = VGroup(
            label(rf"{len(c['nodes'])} terms, \ {len(c['edges'])} single steps, \ computed by our reducer",
                  font_size=20, color=GREY_A),
            label("this finite graph: every maximal reduction reaches the same normal form", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            (
            "Compare all reductions of this precisely parenthesized term. <bookmark mark='a'/> Lambda x, x x is "
            "applied to the whole argument consisting of the identity applied to z. There are two redexes "
            "initially. Reducing the outer one copies the argument; reducing the inner one first avoids that "
            "duplication. The computed graph identifies terms up to renaming bound variables. <bookmark "
            "mark='b'/> It has six nodes and seven reduction edges. This finite graph is fully explored, and "
            "every maximal reduction path reaches z z. That exact example illustrates confluence. The general "
            "theorem also covers terms with infinite paths; it does not say that every path in every lambda term "
            "terminates."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes[0]))
            vo.wait_until("a")
            shown, anims = {0}, []
            for k, (i, j) in enumerate(c["edges"]):
                grp = [GrowArrow(edges[k])]
                if j not in shown:
                    shown.add(j)
                    grp.append(FadeIn(nodes[j]))
                anims.append(AnimationGroup(*grp))
            self.play(LaggedStart(*anims, lag_ratio=0.4), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(cap), nodes[5][0].animate.set_stroke(YES, 3))
        self.wait(0.3)
        self.clear_scene()

    def diamond(self):
        self.ask(r"Two reduction orders both reach normal forms. \\ Can the normal forms differ?", [r"yes", r"no"], 1,
                 say="Two different reduction orders both reach a normal form. Can they reach different ones?",
                 reveal="No. Church and Rosser proved normal forms are unique.")
        head = label(r"The Church--Rosser theorem \ (1936)", font_size=34).to_edge(UP, buff=0.3)
        M = MathTex("M", font_size=40).move_to(UP * 1.6)
        A = MathTex("N_1", font_size=40).move_to(LEFT * 2 + UP * 0.0)
        B = MathTex("N_2", font_size=40).move_to(RIGHT * 2 + UP * 0.0)
        P = MathTex("P", font_size=40, color=YES).move_to(DOWN * 1.6)
        arr = VGroup(Arrow(M.get_bottom(), A.get_top(), buff=0.15, color=GREY_B),
                     Arrow(M.get_bottom(), B.get_top(), buff=0.15, color=GREY_B))
        da = VGroup(DashedLine(A.get_bottom(), P.get_top(), buff=0.15, color=YES),
                    DashedLine(B.get_bottom(), P.get_top(), buff=0.15, color=YES))
        stars = VGroup(MathTex("*", font_size=26).next_to(arr[0].get_center(), LEFT, buff=0.1),
                       MathTex("*", font_size=26).next_to(arr[1].get_center(), RIGHT, buff=0.1))
        thm = label(r"if $M$ reduces to $N_1$ and to $N_2$, \ some $P$ is reachable from both", font_size=23,
                    color=HEAD).next_to(head, DOWN, buff=0.3)
        side = VGroup(
            label("a full $\\beta$-normal form, if it exists, is unique up to $\\alpha$-equivalence", font_size=22, color=YES),
            label("confluence does not imply termination; weak-head stopping is a different criterion", font_size=22,
                  color=YES),
            label(r"the proof: \ one step does not form a diamond \ (a copied redex needs two steps);", font_size=19,
                  color=GREY_A),
            label(r"\textit{parallel} reduction, \ every chosen redex at once, \ does \ (Tait, \ Martin-L\"of)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
        diamond = VGroup(M, A, B, P, arr, da, stars).shift(LEFT * 3.2)
        with self.voiceover(
            (
            "Church and Rosser's theorem concerns beta reduction in the pure calculus. <bookmark mark='a'/> If M "
            "reduces by zero or more steps to N one and N two, some P is reachable from both. The four sides of "
            "this diamond are reduction sequences, not necessarily single steps. <bookmark mark='b'/> Thus a beta "
            "normal form, if one exists, is unique up to renaming bound variables. Effects or additional rewrite rules need their own confluence argument. <bookmark "
            "mark='c'/> Ordinary one-step beta reduction lacks the diamond property because a contracted redex "
            "can copy another redex. The formal parallel-reduction relation permits coordinated contraction with "
            "substitution; it has the joining property used to establish confluence. It is a proof device, not a "
            "claim that arbitrary overlapping edits can be performed independently."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(M), GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(A), FadeIn(B), FadeIn(stars))
            self.play(Create(da), FadeIn(P))
            vo.wait_until("b")
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2:]))
        self.wait(0.3)
        self.clear_scene()


