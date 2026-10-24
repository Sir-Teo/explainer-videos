from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, GNN_C, KIND_COLOR, KIND_NAME, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C, load,
                                   project, take_away, takeaway_anims, tiny_words)
from videos.ai.ai25.physics import rot_axis

PLUS, MINUS = "#F2A07B", "#8FB9EE"


def particles(X, q, center, scale=0.8, r=0.13):
    g = VGroup()
    for p, c in zip(X, q):
        pt = np.array([center[0] + scale * p[0], center[1] + scale * p[1], 0])
        g.add(Circle(radius=r, stroke_width=1.2, stroke_color=WHITE, fill_color=PLUS if c > 0 else MINUS,
                     fill_opacity=0.95).move_to(pt))
    return g


class Symmetry(VoiceoverScene):
    def construct(self):
        self.card()
        self.groups()
        self.diagram()
        self.averaging()
        self.check()

    def card(self):
        card = chapter_card(2, r"Invariance and equivariance", r"What does it mean for a function to respect a "
                            r"symmetry?", lit=(1998,), part=PART)
        with self.voiceover("Chapter two. Invariance and equivariance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def groups(self):
        sq = Square(2.0, color=SYM, stroke_width=4, fill_color=SYM, fill_opacity=0.08).move_to([-4.2, 0.6, 0])
        corner = Dot(sq.get_corner(UR), radius=0.13, color=PRED_C)
        shape = VGroup(sq, corner)
        rl = label(r"turn by $90^\circ$: \ four turns, \ and you are back", font_size=22, color=SYM)
        rl.next_to(sq, DOWN, buff=0.5)
        d = definition_card(r"group", r"a set $G$ of transformations that can be composed ($gh \in G$), with a "
                            r"do-nothing element $e$ and an undo $g^{-1}$ for every $g$ \ (composition associative)",
                            width=7.6, font_size=24).move_to([2.6, 1.7, 0])
        n16 = math.factorial(16)
        exs = VGroup(
            label(r"turns of a square: \ $4$ elements", font_size=23),
            label(rf"orderings of $16$ points: \ $16! = {n16:,}$".replace(",", "{,}"), font_size=23),
            label(r"turns of space, \ $SO(3)$: \ infinitely many", font_size=23),
            label(r"shifts of an image: \ one per offset", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(d, DOWN, buff=0.45).align_to(d, LEFT)
        with self.voiceover(
            "A symmetry is a transformation that leaves what matters unchanged. Turn a square by ninety degrees and "
            "you have the same square. <bookmark mark='a'/> Turn it four times and you are back where you "
            "started. <bookmark mark='b'/> The transformations of a problem form a group: you can do one after "
            "another, there is one that does nothing, and each one can be undone. <bookmark mark='c'/> The square "
            "has four turns. The orderings of sixteen points, a permutation group, have sixteen factorial elements, "
            f"about {n16 / 1e12:.0f} trillion. <bookmark mark='d'/> Turns of space form a continuous group, SO(3), "
            "with infinitely many; and an image has its shifts."
        ) as vo:
            self.play(FadeIn(shape))
            for _ in range(2):
                self.play(Rotate(shape, -PI / 2, about_point=sq.get_center()), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(rl))
            for _ in range(2):
                self.play(Rotate(shape, -PI / 2, about_point=sq.get_center()), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(d, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(exs[0]), FadeIn(exs[1]))
            vo.wait_until("d")
            self.play(FadeIn(exs[2]), FadeIn(exs[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagram(self):
        d = load("nbody_data")
        x = np.asarray(d["test_x0"])[0]
        xT = np.asarray(d["test_xT"])[0]
        q = np.asarray(d["test_q"])[0]
        R = rot_axis([0, 0, 1], 1.1)
        P0, _ = project(x - x.mean(0), 0.0, 0.0)
        PT, _ = project(xT - x.mean(0), 0.0, 0.0)
        Pr, _ = project((x - x.mean(0)) @ R.T, 0.0, 0.0)
        PTr, _ = project((xT - x.mean(0)) @ R.T, 0.0, 0.0)
        s = 0.45
        cA, cB, cC, cD = np.array([-3.6, 1.7, 0]), np.array([1.2, 1.7, 0]), np.array([-3.6, -1.5, 0]), \
            np.array([1.2, -1.5, 0])
        A = particles(P0, q, cA, s, 0.1)
        B = particles(Pr, q, cB, s, 0.1)
        # the lower row is drawn smaller, so that where the particles go stays on screen
        s2 = min(s, 1.15 / max(np.abs(np.r_[P0, PT]).max(), 1e-9))

        def arrows(P, Q, c):
            return VGroup(*[Arrow(c + s2 * np.r_[p, 0], c + s2 * np.r_[q_, 0], buff=0, color=PRED_C, stroke_width=3,
                                  max_tip_length_to_length_ratio=0.25) for p, q_ in zip(P, Q)])
        Cg = VGroup(particles(P0, q, cC, s2, 0.07).set_opacity(0.35), arrows(P0, PT, cC))
        Dg = VGroup(particles(Pr, q, cD, s2, 0.07).set_opacity(0.35), arrows(Pr, PTr, cD))
        top = Arrow(cA + RIGHT * 1.5, cB + LEFT * 1.5, color=SYM, buff=0.1, stroke_width=4)
        bot = Arrow(cC + RIGHT * 1.5, cD + LEFT * 1.5, color=SYM, buff=0.1, stroke_width=4)
        left = Arrow(cA + DOWN * 1.0, cC + UP * 1.0, color=STRUCT, buff=0.1, stroke_width=4)
        right = Arrow(cB + DOWN * 1.0, cD + UP * 1.0, color=STRUCT, buff=0.1, stroke_width=4)
        lt = MathTex(r"g", font_size=40, color=SYM).next_to(top, UP, buff=0.08)
        lb = MathTex(r"g", font_size=40, color=SYM).next_to(bot, UP, buff=0.08)
        ll = MathTex(r"f", font_size=40, color=STRUCT).next_to(left, LEFT, buff=0.1)
        lr = MathTex(r"f", font_size=40, color=STRUCT).next_to(right, RIGHT, buff=0.1)
        nA = MathTex(r"x", font_size=34).next_to(A, UP, buff=0.1)
        nB = MathTex(r"g \cdot x", font_size=34).next_to(B, UP, buff=0.1)
        nC = MathTex(r"f(x)", font_size=34, color=PRED_C).next_to(Cg, DOWN, buff=0.1)
        nD = MathTex(r"f(g\cdot x) = g \cdot f(x)", font_size=34, color=PRED_C).next_to(Dg, DOWN, buff=0.1)
        side = VGroup(
            cmath(r"\text{invariant:}", r"\quad f(g \cdot x) = f(x)", font_size=32),
            label(r"energy, \ a class, \ a yes or no", font_size=22, color=GREY_B),
            cmath(r"\text{equivariant:}", r"\quad f(g \cdot x) = g \cdot f(x)", font_size=32),
            label(r"forces, \ future positions, \ a segmentation", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.95, 0.0, 0])
        side[0][1].set_color(STRUCT)
        side[2][1].set_color(STRUCT)
        side.width = min(side.width, 3.6)
        side.move_to([5.0, 0.0, 0])
        tag = note(r"the five particles of the hook, \ where they go by $t = 1$ (computed)", font_size=20)
        tag.to_corner(UL, buff=0.25)
        with self.voiceover(
            "Now a function of the data, f: here, where each of our five particles will be one time unit later. "
            "<bookmark mark='a'/> Turn the input, apply f, <bookmark mark='b'/> or apply f and then turn the "
            "output. <bookmark mark='c'/> If the two paths always agree, f is equivariant: transforming the input "
            "transforms the output the same way. <bookmark mark='d'/> If the output doesn't change at all, f is "
            "invariant: the energy of the molecule, or the label of an image. <bookmark mark='e'/> Equivariance is "
            "what intermediate layers need, so that the information about how the input was turned is kept, not "
            "thrown away; invariance is what a final answer often needs."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nA), FadeIn(tag))
            self.play(GrowArrow(left), FadeIn(ll), FadeIn(Cg), FadeIn(nC))
            vo.wait_until("a")
            self.play(GrowArrow(top), FadeIn(lt), FadeIn(B), FadeIn(nB))
            vo.wait_until("b")
            self.play(GrowArrow(right), FadeIn(lr), GrowArrow(bot), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(Dg), Write(nD))
            vo.wait_until("d")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Indicate(side[2], color=STRUCT))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def averaging(self):
        cols = {r"g": SYM, r"h": SYM, r"g'": SYM}
        rows = [
            cmath(r"\bar f(x)", r"=", r"\frac{1}{|G|} \sum_{g \in G} g^{-1} f(g \cdot x)", font_size=36),
            cmath(r"\bar f(h \cdot x)", r"=", r"\frac{1}{|G|} \sum_{g \in G} g^{-1} f(g h \cdot x)", font_size=36),
            cmath(r"\bar f(h \cdot x)", r"=", r"\frac{1}{|G|} \sum_{g' \in G} (g' h^{-1})^{-1} f(g' \cdot x)",
                  font_size=36),
            cmath(r"\bar f(h \cdot x)", r"=", r"\frac{1}{|G|} \sum_{g' \in G} h \, g'^{-1} f(g' \cdot x)", font_size=36),
            cmath(r"\bar f(h \cdot x)", r"=", r"h \cdot \bar f(x)", font_size=36),
        ]
        whys = [why(r"average $f$ over the group"), why(r"put in a turned input"),
                why(r"$g' = gh$: \ as $g$ runs over $G$, \ so does $g'$"), why(r"$(ab)^{-1} = b^{-1} a^{-1}$"),
                why(r"$h$ is linear: \ out of the sum")]
        for r_ in rows:
            r_.scale(32 / 36)
        step = ladder(self, rows, whys, keep=5, top=3.4, x=-1.8, buff=0.24, edge=6.9)
        cost = VGroup(
            label(r"any $f$ becomes equivariant, \ at the price of $|G|$ evaluations", font_size=22, color=STRUCT),
            label(r"$|G| = 16!$ for sixteen points; \ infinite for turns of space", font_size=22, color=PLAIN),
            label(r"augmentation: \ a random $g$ in training, \ hoping $f$ learns the rest", font_size=22, color=AUG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is a way to make any function equivariant. Average it over the group: for every transformation "
            "g, transform the input, apply f, and undo g on the output. <bookmark mark='a'/> Feed this average a "
            "turned input, h of x. <bookmark mark='b'/> Rename g times h as g prime: as g runs through the whole "
            "group, so does g prime, so the sum is the same sum. <bookmark mark='c'/> The inverse of a product "
            "reverses its order, <bookmark mark='d'/> and h comes out of the sum. The average is equivariant, "
            "whatever f was. <bookmark mark='e'/> The catch is the price: one evaluation per group element, sixteen "
            "factorial for sixteen points, infinitely many for turns of space. <bookmark mark='f'/> Data "
            "augmentation is the cheap version: one random transformation per training example, and the hope that "
            "the network learns the rest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            self.play(FadeIn(cost[0]), FadeIn(cost[1]))
            vo.wait_until("f")
            self.play(FadeIn(cost[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        e = load("equivariance")
        kinds = ["egnn", "gnn", "mlp_aug", "mlp"]
        p = pause_card(r"Four networks predict where the particles will be. \ Turn the input: \ which of them "
                       r"turn their answer exactly?", width=8.4).move_to(UP * 2.3)
        hdr = [r"network", r"turned", r"shifted", r"reordered", r"its own error"]
        xs = [-4.6, -1.5, 0.6, 2.7, 5.0]
        y0 = 0.8
        head = VGroup(*[label(h, font_size=22, color=GREY_A).move_to([x, y0, 0]) for h, x in zip(hdr, xs)])

        def val(v, ref):
            s = sci(v, 1) if v < 0.01 else f"{v:.2f}"
            col = STRUCT if v < 1e-4 else (AUG if v < 0.5 * ref else PLAIN)
            return MathTex(s, font_size=28, color=col)

        table = VGroup()
        for k, kind in enumerate(kinds):
            r = e[f"dyn_{kind}"]
            y = y0 - 0.6 * (k + 1)
            row = VGroup(label(KIND_NAME[kind], font_size=24, color=KIND_COLOR[kind]).move_to([xs[0], y, 0]))
            for v, x in zip((r["err"], r["err_translate"], r["err_permute"]), xs[1:4]):
                row.add(val(v, r["test_rmse"]).move_to([x, y, 0]))
            row.add(MathTex(f"{r['test_rmse']:.2f}", font_size=28, color=GREY_A).move_to([xs[4], y, 0]))
            table.add(row)
        rule = Line([-6.4, y0 - 0.3, 0], [6.4, y0 - 0.3, 0], color=GREY_D, stroke_width=1.2)
        tag = note(rf"computed: \ ${int(e['n'])}$ test systems, \ random turns and shifts; \ distances in the units "
                   r"of the positions", font_size=20)
        tag.next_to(table, DOWN, buff=0.35).align_to(rule, RIGHT)
        eg, gn, ma, ml = (e[f"dyn_{k}"] for k in kinds)
        aug_frac = ma["err"] / max(ma["test_rmse"], 1e-9)
        aug_verdict = ("smaller than its own error, but not zero" if aug_frac < 1 else
                       "still as large as its own error")
        eg_tiny = tiny_words(max(eg["err"], eg["err_translate"]))
        tk = take_away(r"built in: \ exact, \ on every input; \ learned from copies: \ approximate, \ and only near "
                       r"the training data")
        with self.voiceover(
            "Here is the check, computed on our five-particle system, with four networks trained on the same data "
            "for the same number of steps. <bookmark mark='a'/> Pause and predict: which of them turns its answer "
            "exactly when the input is turned? <bookmark mark='b'/> The equivariant network, EGNN, which we'll build "
            f"in chapter seven: its turned and shifted answers are off by {eg_tiny} of a unit, rounding error. "
            "<bookmark mark='c'/> A message-passing network fed the raw coordinates handles a reordering exactly, "
            "because it sums over neighbours, but not a turn. <bookmark mark='d'/> The plain MLP gets none of them exactly, "
            f"and with turned copies in training its turning error is {ma['err']:.2f}, {aug_verdict}. <bookmark "
            "mark='e'/> That is the lesson of this chapter: a symmetry built into the layers holds exactly, on every "
            "input; a symmetry learned from examples holds only approximately, and only near the data it saw."
        ) as vo:
            self.play(FadeIn(p, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(head), Create(rule), *[FadeIn(r_[0]) for r_ in table])
            vo.wait_until("b")
            self.play(FadeIn(table[0][1:]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(table[1][1:]))
            vo.wait_until("d")
            self.play(FadeIn(table[2][1:]), FadeIn(table[3][1:]))
            vo.wait_until("e")
            self.play(FadeOut(p), FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
