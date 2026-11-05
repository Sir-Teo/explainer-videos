from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class Confluence(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph_small()
        self.diamond()
        self.bigger()
        self.debruijn()

    def card(self):
        card = chapter_card(6, r"Church--Rosser, \ and de Bruijn", r"Can two orders give two answers?",
                            lit=(1936,), extra=((1936, r"Church and Rosser; \ Turing"),), part=PART)
        with self.voiceover("Chapter six. Church Rosser, and de Bruijn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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
            label(r"every path ends at the same normal form", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Strategies can disagree about whether we finish. Can they disagree about the answer? <bookmark "
            "mark='a'/> Here is every possible reduction of one small term, computed by our reducer: lambda x, x "
            "x, applied to lambda y, y, applied to z. It has two redexes, so two first steps. Reducing the outer "
            "one copies the inner, giving two copies to reduce, in either order. <bookmark mark='b'/> Six terms, "
            "seven single steps, and every path, however it wanders, ends at the same place: z z."
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
            label(r"so a normal form, \ if any, \ is \textbf{unique}", font_size=22, color=YES),
            label(r"strategies change \textit{whether} and \textit{how fast}, \ never \textit{what}", font_size=22,
                  color=YES),
            label(r"the proof: \ one step does not form a diamond \ (a copied redex needs two steps);", font_size=19,
                  color=GREY_A),
            label(r"\textit{parallel} reduction, \ every chosen redex at once, \ does \ (Tait, \ Martin-L\"of)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
        diamond = VGroup(M, A, B, P, arr, da, stars).shift(LEFT * 3.2)
        with self.voiceover(
            "That was no accident. <bookmark mark='a'/> Church and Rosser proved in 1936 that if a term M reduces, "
            "in any number of steps, to N one and to N two, then there is some term P that both can reach. Draw "
            "it as a diamond: whatever two directions you take, the paths can be brought back together. <bookmark "
            "mark='b'/> So a normal form, if one exists, is unique, because a normal form cannot reduce any "
            "further, and two different ones could never meet. Strategies change whether we arrive and how fast, "
            "never what we arrive at. <bookmark mark='c'/> The proof has a pleasing trick. Single steps do not "
            "close into diamonds, because a step can copy a redex, which then takes two steps to finish. But "
            "parallel reduction, which reduces any chosen set of redexes at once, does close in one step, and "
            "diamonds of parallel steps tile together into the theorem."
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

    def bigger(self):
        c = load("confluence")
        head = label(r"A bigger graph", font_size=34).to_edge(UP, buff=0.3)
        b = c["big"]
        src = mono(b["source"].replace("\\", "λ"), 20, CODE).next_to(head, DOWN, buff=0.4)
        depth = b["depth"]
        levels = {}
        for k, d in enumerate(depth):
            levels.setdefault(d, []).append(k)
        maxd = max(levels)
        pts = {}
        for d, ks in levels.items():
            for r, k in enumerate(ks):
                pts[k] = np.array([(r - (len(ks) - 1) / 2) * min(1.3, 11.0 / max(len(ks), 1)),
                                   1.7 - 4.2 * d / max(maxd, 1), 0])
        nf = set(b["normal_index"])
        dots = VGroup(*[Dot(pts[k], radius=0.09 if k in nf else 0.07, color=YES if k in nf else CODE)
                        for k in range(len(depth))])
        lines = VGroup(*[Line(pts[i], pts[j], color=GREY_D, stroke_width=1.0) for i, j in b["edge_list"]])
        fact = VGroup(
            label(rf"{b['nodes']} terms, \ {b['edges']} single steps, \ {b['normal']} normal form", font_size=24,
                  color=YES),
            label(r"confluent: \ every pair of reducts has a common reduct \ (checked on the whole graph)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A slightly bigger term already has a large graph of possible reductions. <bookmark mark='a'/> This one "
            "has thirty terms connected by ninety-three single steps. <bookmark mark='b'/> Our reducer checks every "
            "pair of terms in the graph: each pair has a common reduct, and there is exactly one normal form. The "
            "theorem, confirmed on a small example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(fact))
        self.wait(0.3)
        self.clear_scene()

    def debruijn(self):
        c = load("confluence")
        head = label(r"Names, \ removed: \ de Bruijn indices", font_size=34).to_edge(UP, buff=0.3)
        rows = [[k.replace("\\", "λ"), v] for k, v in c["debruijn"].items()]
        tab = grid_table([r"with names", r"de Bruijn \ (1972)"], rows, widths=[5.6, 4.6], row_h=0.55, font_size=22,
                         mono_cols=(0, 1)).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"a variable becomes a number: \ how many $\lambda$s up its binder is", font_size=22,
                  color=GREY_A),
            label(r"$\alpha$-equivalent terms become \textit{identical}; \ no capture can happen", font_size=22,
                  color=YES),
            label(r"compilers and proof assistants use them inside; \ environments replace substitution \ "
                  r"(Part 15)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Names cause trouble: alpha equivalence, and the capture trap of chapter one. Nicolaas de Bruijn, "
            "building one of the first proof checkers in 1972, removed them. <bookmark mark='a'/> Replace each "
            "variable by a number: how many lambdas you must pass, going up the tree, to reach the one that binds "
            "it. Lambda x, x is lambda, zero. Two, lambda f x, f of f of x, becomes lambda lambda, one applied to "
            "one applied to zero. <bookmark mark='b'/> Now alpha-equivalent terms are literally identical, and "
            "capture cannot happen. <bookmark mark='c'/> Compilers and proof assistants use this representation "
            "inside, and Part 15 replaces substitution altogether with environments, which is how real "
            "interpreters run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
