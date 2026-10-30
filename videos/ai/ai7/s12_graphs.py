from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import HIDDEN, PART, SEEN, card_in, load

MSG = C.BITS  # messages
EXACT = C.TRUE_P


def node(tex, pos, hidden=True, r=0.36):
    c = Circle(radius=r, color=HIDDEN if hidden else SEEN, stroke_width=3,
               fill_color=BACKGROUND if hidden else SEEN, fill_opacity=1 if hidden else 0.35).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=30).move_to(pos))


def word_node(text, pos, observed=False, r=0.5, color=None):
    col = color or (SEEN if observed else HIDDEN)
    c = Circle(radius=r, color=col, stroke_width=3, fill_color=col if observed else BACKGROUND,
               fill_opacity=0.35 if observed else 1).move_to(pos)
    return VGroup(c, label(text, font_size=20).move_to(pos))


def edge(a, b, color=GREY_B):
    d = b[0].get_center() - a[0].get_center()
    d = d / np.linalg.norm(d)
    return Arrow(a[0].get_center() + d * a[0].width / 2, b[0].get_center() - d * b[0].width / 2, buff=0.04,
                 color=color, stroke_width=3, max_tip_length_to_length_ratio=0.25)


class Graphs(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Models as pictures", r"What depends on what?", lit=(1988,), part=PART)
        with self.voiceover("Chapter eleven. Models as pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pictures()
        self.dsep()
        self.bp()

    def pictures(self):
        # the mixture: a hidden source, then a page (a plate of n pages)
        z = node(r"z", [-4.6, 1.6, 0])
        x = node(r"x", [-4.6, -0.2, 0], hidden=False)
        plate = SurroundingRectangle(VGroup(z, x), color=GREY_C, buff=0.35, corner_radius=0.12)
        pn = MathTex(r"n", font_size=28, color=GREY_B).next_to(plate.get_corner(DR), UL, buff=0.1)
        mix = VGroup(z, x, edge(z, x), plate, pn)
        mix_l = label(r"a mixture: \\ hidden source $\to$ page", font_size=24, color=GREY_A).next_to(plate, DOWN, buff=0.25)
        # the hidden Markov model
        zs = [node(rf"z_{k}", [-1.6 + 1.5 * k, 1.6, 0]) for k in range(1, 5)]
        xs = [node(rf"x_{k}", [-1.6 + 1.5 * k, -0.2, 0], hidden=False) for k in range(1, 5)]
        hmm = VGroup(*zs, *xs, *[edge(zs[k], zs[k + 1]) for k in range(3)], *[edge(zs[k], xs[k]) for k in range(4)])
        hmm_l = label(r"a hidden Markov model: \\ a chain of hidden states, \ each emitting a letter", font_size=24,
                      color=GREY_A).next_to(VGroup(*xs), DOWN, buff=0.6)
        key = VGroup(VGroup(Circle(radius=0.14, color=HIDDEN, stroke_width=3), label(r"hidden", font_size=22, color=HIDDEN)).arrange(RIGHT, buff=0.12),
                     VGroup(Circle(radius=0.14, color=SEEN, stroke_width=3, fill_color=SEEN, fill_opacity=0.35),
                            label(r"observed", font_size=22, color=SEEN)).arrange(RIGHT, buff=0.12))
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.35)
        colors = {r"\mathrm{parents}(v)": HIDDEN}
        f = cmath(r"p(\text{everything})", "=", r"\prod_{v}", r"\,p\big(v \mid", r"\mathrm{parents}(v)", r"\big)",
                  colors=colors, font_size=40).to_edge(DOWN, buff=1.15)
        fn = label(r"$\prod$: \ multiply one probability per circle, \ each given the circles that point into it",
                   font_size=24, color=GREY_A)
        fn.next_to(f, DOWN, buff=0.15)
        cite_ = cite(r"J.~Pearl, \textit{Probabilistic Reasoning in Intelligent Systems} (1988)", corner=DR)
        # a language model: every earlier letter points at every later one
        lm = [node(rf"x_{k}", [-1.6 + 1.5 * k, 0.6, 0], hidden=False) for k in range(1, 5)]
        lm_e = VGroup(*[CurvedArrow(lm[a][0].get_top() + UP * 0.02, lm[b][0].get_top() + UP * 0.02, angle=-0.6 - 0.25 * (b - a),
                                    color=GREY_B, stroke_width=2.5, tip_length=0.14)
                        for a in range(4) for b in range(a + 1, 4)])
        lm_l = label(r"a language model: \ every earlier letter points at every later one", font_size=24,
                     color=GREY_A).next_to(VGroup(*lm), DOWN, buff=0.5)
        # the drawing rules, built big as they're named, then shrunk into the mixture's own z -> x
        dz, dx = node(r"z", [0, 1.5, 0], r=0.62), node(r"x", [0, -1.2, 0], r=0.62)
        for d_ in (dz, dx):
            d_[0].set_stroke(GREY_B).set_fill(BACKGROUND, opacity=1)
            d_[1].scale(1.5)
        dzh = node(r"z", [0, 1.5, 0], r=0.62)
        dzh[1].scale(1.5)
        dxo = node(r"x", [0, -1.2, 0], hidden=False, r=0.62)
        dxo[1].scale(1.5)
        d_e = edge(dz, dx)
        tq = label(r"one circle per quantity", font_size=28, color=GREY_A).next_to(VGroup(dz, dx), LEFT, buff=0.8)
        to = label(r"shaded: \ observed", font_size=28, color=SEEN).next_to(dx, RIGHT, buff=0.6)
        th = label(r"empty: \ hidden", font_size=28, color=HIDDEN).next_to(dz, RIGHT, buff=0.6)
        ta = label(r"arrow: \ depends directly on", font_size=28, color=GREY_B).next_to(d_e, LEFT, buff=0.5)
        with self.voiceover(
            "Every model in this part can be drawn the same way: <bookmark mark='q'/> a circle for each quantity, "
            "<bookmark mark='o'/> shaded if we observe it, <bookmark mark='h'/> empty if it's hidden, "
            "<bookmark mark='r'/> and an arrow wherever one depends directly on another. "
            "<bookmark mark='a'/> The mixture: a hidden choice of source, then a page, repeated for every page. "
            "<bookmark mark='b'/> The hidden Markov model: a chain of hidden states, each emitting a letter. "
            "<bookmark mark='c'/> The picture is a formula. The probability of everything is a product, the big "
            "pi: multiply one probability per circle, each given only the circles that point into it, its parents. "
            "That's a Bayesian network, Judea "
            "Pearl's language for reasoning under uncertainty."
        ) as vo:
            vo.wait_until("q")
            self.play(Create(dz[0]), Create(dx[0]), FadeIn(dz[1]), FadeIn(dx[1]), FadeIn(tq))
            vo.wait_until("o")
            self.play(Transform(dx, dxo), FadeIn(to))
            vo.wait_until("h")
            self.play(Transform(dz, dzh), FadeIn(th))
            vo.wait_until("r")
            self.play(GrowArrow(d_e), FadeOut(tq), FadeIn(ta))
            vo.wait_until("a")
            self.play(FadeOut(VGroup(to, th, ta)), ReplacementTransform(dz, mix[0]), ReplacementTransform(dx, mix[1]),
                      ReplacementTransform(d_e, mix[2]), FadeIn(key), run_time=1.2)
            self.play(FadeIn(mix[3:]), FadeIn(mix_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in hmm], lag_ratio=0.05), FadeIn(hmm_l), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fn), FadeIn(cite_))
        self.wait(0.3)
        self.play(FadeOut(VGroup(mix, mix_l, hmm, hmm_l)))
        with self.voiceover(
            "Part one's language models fit the same picture, with an arrow from every earlier letter to every later "
            "one. <bookmark mark='a'/> Nothing is hidden, but nothing is simplified either: each factor is a "
            "prediction from the whole past. Counting can't fill in factors like that. A network, from part nine "
            "on, can."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m) for m in lm], lag_ratio=0.1), FadeIn(lm_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in lm_e], lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dsep(self):
        d = load("dsep")
        fk, co = d["fork"], d["collider"]
        P = [np.array([-4.6, 0, 0]), np.array([0, 0, 0]), np.array([4.6, 0, 0])]

        def panel(cx, kind):
            if kind == "chain":
                a, m, b = (word_node(t, [cx + dx, 0.6, 0]) for t, dx in ((r"cloudy", -1.5), (r"rain", 0), (r"wet", 1.5)))
                arrs = VGroup(edge(a, m), edge(m, b))
            elif kind == "fork":
                m = word_node(r"cloudy", [cx, 1.6, 0])
                a, b = word_node(r"rain", [cx - 1.2, -0.1, 0]), word_node(r"sprinkler", [cx + 1.2, -0.1, 0], r=0.62)
                arrs = VGroup(edge(m, a), edge(m, b))
            else:
                a, b = word_node(r"rain", [cx - 1.2, 1.6, 0]), word_node(r"sprinkler", [cx + 1.2, 1.6, 0], r=0.62)
                m = word_node(r"wet", [cx, -0.1, 0])
                arrs = VGroup(edge(a, m), edge(b, m))
            return VGroup(a, m, b, arrs)

        pans = VGroup(panel(P[0][0], "chain"), panel(P[1][0], "fork"), panel(P[2][0], "collider"))
        names = VGroup(*[label(t, font_size=26, color=GREY_A).move_to([p_[0], 2.85, 0])
                         for t, p_ in zip((r"a chain", r"a fork", r"a collider"), P)])
        rules = VGroup(label(r"observe the middle: \ blocked", font_size=22, color=GREY_B),
                       label(r"observe the middle: \ blocked", font_size=22, color=GREY_B),
                       label(r"observe the middle: \ \emph{opened}", font_size=22, color=C.SURPRISE))
        for r_, p_ in zip(rules, P):
            r_.move_to([p_[0], -1.25, 0])
        fnum = VGroup(label(rf"$p(\text{{sprinkler}} \mid \text{{rain}}) = {fk['p_s_r']:.2f}$, \ "
                            rf"$\mid$ no rain: ${fk['p_s_nr']:.2f}$", font_size=20),
                      label(rf"given cloudy: \ ${fk['p_s_rc']:.3f}$ \ vs \ ${fk['p_s_nrc']:.3f}$", font_size=20,
                            color=SEEN)).arrange(DOWN, buff=0.1).move_to([0, -2.35, 0])
        cnum = VGroup(label(rf"$p(\text{{rain}}) = {co['p_r']:.2f}$; \ given wet: ${co['p_r_w']:.2f}$", font_size=20),
                      label(rf"wet and sprinkler on: \ ${co['p_r_ws']:.2f}$", font_size=20, color=C.SURPRISE))
        cnum.arrange(DOWN, buff=0.1).move_to([4.6, -2.35, 0])
        cnum2 = label(r"(simulated, $400{,}000$ days)", font_size=18, color=GREY_B).to_corner(DR, buff=0.2)
        dfn = label(r"$d$-separation: \ $X$ and $Y$ are independent given $Z$ when every path between them is blocked",
                    font_size=22, color=C.BITS).to_edge(DOWN, buff=0.15)
        explained = co["p_r_w"] > co["p_r"] + 0.05 and abs(co["p_r_ws"] - co["p_r"]) < 0.05
        verdict = (f"Simulate it: rain alone has a {100 * co['p_r']:.0f} percent chance. Wet grass raises it to "
                   f"{100 * co['p_r_w']:.0f} percent. But wet grass with the sprinkler on brings it back to "
                   f"{100 * co['p_r_ws']:.0f}: the sprinkler explains the wetness away."
                   if explained else
                   f"Simulate it: rain alone {100 * co['p_r']:.0f} percent; given wet grass {100 * co['p_r_w']:.0f}; "
                   f"given wet grass and the sprinkler {100 * co['p_r_ws']:.0f}.")
        with self.voiceover(
            "A graph also tells you, without any numbers, which things are independent. Information flows along "
            "paths, and there are only three kinds of junction. <bookmark mark='a'/> In a chain, cloudy leads to "
            "rain leads to wet grass. Once you know it rained, the clouds tell you nothing more about the grass: "
            "observing the middle blocks the path. <bookmark mark='b'/> In a fork, clouds cause both rain and, less "
            f"often, the sprinkler. The two look related: the sprinkler is on {100 * fk['p_s_r']:.0f} percent of "
            f"rainy days and {100 * fk['p_s_nr']:.0f} percent of dry ones. Given the clouds, the link disappears. "
            "<bookmark mark='c'/> The collider is the strange one. Rain and the sprinkler are independent, but both "
            "wet the grass, and observing the wet grass connects them. " + verdict + " <bookmark mark='d'/> Pearl and "
            "his students turned these three cases into a rule, d-separation, that reads every independence off the "
            "picture."
        ) as vo:
            self.play(FadeIn(names), FadeIn(pans))
            vo.wait_until("a")
            self.play(pans[0][1][0].animate.set_fill(SEEN, opacity=0.35).set_stroke(SEEN), FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(Circumscribe(pans[1], color=WHITE))
            self.play(FadeIn(fnum[0]))
            self.play(pans[1][1][0].animate.set_fill(SEEN, opacity=0.35).set_stroke(SEEN), FadeIn(rules[1]), FadeIn(fnum[1]))
            vo.wait_until("c")
            self.play(Circumscribe(pans[2], color=WHITE))
            self.play(pans[2][1][0].animate.set_fill(SEEN, opacity=0.35).set_stroke(SEEN), FadeIn(rules[2]),
                      FadeIn(cnum[0]), FadeIn(cnum2))
            self.play(FadeIn(cnum[1]))
            vo.wait_until("d")
            self.play(FadeIn(dfn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bp(self):
        d = load("bp")
        n = int(d["n"])
        edges = [tuple(e) for e in d["edges"]]
        exact, belief = np.asarray(d["exact"]), np.asarray(d["belief"])
        order = [tuple(o) for o in d["order"]]
        pos = {0: [-3.2, 2.3, 0], 1: [-4.9, 0.6, 0], 2: [-1.5, 0.6, 0], 3: [-5.8, -1.2, 0], 4: [-4.0, -1.2, 0],
               5: [-2.4, -1.2, 0], 6: [-0.6, -1.2, 0]}
        vs = {i: VGroup(Circle(radius=0.3, color=HIDDEN, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1).move_to(pos[i]),
                        MathTex(rf"x_{i + 1}", font_size=26).move_to(pos[i])) for i in range(n)}
        fac = {}
        lines = VGroup()
        for a, b in edges:
            mid = (np.array(pos[a]) + np.array(pos[b])) / 2
            fac[(a, b)] = Square(0.22, color=GREY_A, fill_color=GREY_A, fill_opacity=0.8).move_to(mid)
            lines.add(Line(pos[a], pos[b], color=GREY_C, stroke_width=2.5))
        unary = VGroup(*[Square(0.18, color=GREY_B, fill_color=GREY_B, fill_opacity=0.6).move_to(np.array(pos[i]) + UP * 0.45 + RIGHT * 0.35)
                         for i in range(n)])
        graph = VGroup(lines, *fac.values(), unary, *vs.values())
        colors = {r"m_{i \to j}(x_j)": MSG, r"m_{k \to i}(x_i)": MSG}
        eq = cmath(r"m_{i \to j}(x_j)", r"=", r"\sum_{x_i} \phi_i(x_i)\, \psi_{ij}(x_i, x_j)", r"\prod_{k \ne j}",
                   r"m_{k \to i}(x_i)", colors=colors, font_size=32).move_to([3.4, 2.9, 0])
        bq = cmath(r"p(x_i)", r"\propto", r"\phi_i(x_i)", r"\prod_k", r"m_{k \to i}(x_i)", colors=colors, font_size=32)
        bq.next_to(eq, DOWN, buff=0.25)
        fl = label(r"squares: \ factors \ (each a table of numbers, \ random here)", font_size=20, color=GREY_A)
        fl.next_to(graph, DOWN, buff=0.25)
        dots = VGroup()
        for a, b in order:
            dots.add(Dot(pos[a], radius=0.09, color=MSG))
        bx = 1.4
        bars_ = VGroup()
        for i in range(n):
            y = 1.05 - 0.5 * i
            bars_.add(VGroup(MathTex(rf"x_{i + 1}", font_size=24).move_to([bx - 0.5, y, 0]),
                             Rectangle(width=max(3.2 * exact[i], 0.02), height=0.17, stroke_width=0, fill_color=EXACT,
                                       fill_opacity=0.9).move_to([bx + 1.6 * exact[i], y + 0.1, 0]),
                             Rectangle(width=max(3.2 * belief[i], 0.02), height=0.17, stroke_width=0, fill_color=MSG,
                                       fill_opacity=0.9).move_to([bx + 1.6 * belief[i], y - 0.1, 0])))
        bl = legend([(EXACT, rf"exact: \ all $2^{n} = {2 ** n}$ states summed"), (MSG, rf"belief propagation: \ "
                                                                                     rf"${len(order)}$ messages")],
                    font_size=20).move_to([3.4, -2.6, 0])
        err = float(np.abs(exact - belief).max())
        bh = label(r"the probability that each $x_i = 1$", font_size=22, color=GREY_A).next_to(bars_, UP, buff=0.2)
        bh.align_to(bars_, LEFT)
        loopy = d["loopy_final"]
        exact_say = (f"it agrees with summing all {2 ** n} states to the last digits." if err < 1e-9 else
                     f"it differs from summing all {2 ** n} states by {err:.4f}.")
        with self.voiceover(
            "Pictures also tell us how to compute. Redraw the model as a factor graph: circles for the variables, and "
            "a small square for each factor of the product, each a table of numbers. <bookmark mark='a'/> To find "
            "the probability of one variable, we'd have to sum over all the others, every combination. Judea Pearl's "
            "belief propagation, from 1982, sends messages instead. <bookmark mark='b'/> Each circle tells its "
            "neighbour what it believes, given everything on its own side. Leaves first, up to the root, <bookmark "
            "mark='c'/> then back down. <bookmark mark='d'/> Multiply the messages arriving at a circle, and you have "
            f"its exact probability. On a tree it is exact: " + exact_say + " <bookmark mark='e'/> Add one factor "
            f"that closes a loop, and the same messages, passed round and round, are only approximate, off by about "
            f"{loopy:.4f} here. Yet loopy belief "
            "propagation decodes the error-correcting codes in phones and satellite links, and its messages are the "
            "message passing of part twenty-five's graph neural networks."
        ) as vo:
            self.play(FadeIn(graph), FadeIn(fl), FadeIn(eq), FadeIn(bh), FadeIn(VGroup(*[b_[0] for b_ in bars_])))
            vo.wait_until("a")
            self.play(Indicate(eq, color=MSG, scale_factor=1.03))
            vo.wait_until("b")
            for k in range(6):
                a, b = order[k]
                self.play(dots[k].animate.move_to(pos[b]), run_time=0.45)
                self.play(FadeOut(dots[k]), Indicate(vs[b][0], color=MSG, scale_factor=1.15), run_time=0.3)
            vo.wait_until("c")
            for k in range(6, len(order)):
                a, b = order[k]
                self.play(dots[k].animate.move_to(pos[b]), run_time=0.4)
                self.play(FadeOut(dots[k]), run_time=0.2)
            vo.wait_until("d")
            self.play(Write(bq), FadeIn(bl), LaggedStart(*[FadeIn(b_[1:]) for b_ in bars_], lag_ratio=0.1))
            vo.wait_until("e")
            loop = Line(pos[3], pos[4], buff=0.32, color=C.SURPRISE, stroke_width=4)
            lsq = Square(0.22, color=C.SURPRISE, fill_color=C.SURPRISE, fill_opacity=0.8).move_to(
                (np.array(pos[3]) + np.array(pos[4])) / 2)
            self.play(Create(loop), FadeIn(lsq))
        self.wait(0.3)
        self.clear_scene()
