from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import (HIST, I_COLOR, J_COLOR, MONO, VA, VB, arrow, barcode, chapter, load, plane)


class Vectors(VoiceoverScene):
    def construct(self):
        chapter(self, 1, r"Vectors and the inner product", r"How alike are two vectors?",
                "Chapter one. Vectors, and how alike two of them are.")
        self.arrows()
        self.two_moves()
        self.law_of_cosines()
        self.cauchy_schwarz()
        self.words()
        self.logits()

    # ------------------------------------------------------------------
    def arrows(self):
        pl = plane()
        v = np.array([3.0, 2.0, 0])
        a = arrow(v, color=C.BITS)
        dx = DashedLine(ORIGIN, [3, 0, 0], color=I_COLOR, stroke_width=4)
        dy = DashedLine([3, 0, 0], v, color=J_COLOR, stroke_width=4)
        col = Matrix([["3"], ["2"]], bracket_h_buff=0.12).scale(0.9).next_to(v, UR, buff=0.15)
        col.get_entries()[0].set_color(I_COLOR)
        col.get_entries()[1].set_color(J_COLOR)
        bg = BackgroundRectangle(col, color=BACKGROUND, fill_opacity=0.85, buff=0.1)
        three = Matrix([["3"], ["2"], ["1"]], bracket_h_buff=0.12).scale(0.9).move_to(col)
        g = load("gpt2")
        bar = np.asarray(g["barcodes"])[0][:12]
        many = MathTex(r"\begin{bmatrix}" + r" \\ ".join(f"{x:+.2f}" for x in bar[:5]) + r" \\ \vdots \\ "
                       + f"{bar[-1]:+.2f}" + r"\end{bmatrix}", font_size=30).move_to(col)
        if many.get_top()[1] > 3.7:  # keep the tall column on screen
            many.shift(DOWN * (many.get_top()[1] - 3.7))
        n768 = label(r"$768$ numbers: \ GPT-2's \texttt{dog}", font_size=26, color=GREY_A).next_to(many, DOWN, buff=0.15)
        hist = history_card(1844, r"Hermann Grassmann, \textit{Die lineale Ausdehnungslehre}",
                            r"quantities with direction that add and stretch, in any number of dimensions; "
                            r"ignored for decades, until Gibbs and Heaviside made vectors the language of physics "
                            r"in the 1880s", color=HIST, width=5.4).to_corner(DL, buff=0.3)
        with self.voiceover(
            "A vector is an arrow from the origin, <bookmark mark='a'/> or, just as well, a list of numbers: how far "
            "to go along each axis. <bookmark mark='b'/> Two numbers in the plane, three in space, and 768 for a word "
            "in GPT-2. <bookmark mark='c'/> Grassmann saw in 1844 that nothing about the algebra cares how many "
            "numbers there are. Almost nobody read him; forty years later Gibbs and Heaviside turned his ideas into "
            "the vector calculus physicists still use."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), run_time=1.5)
            self.play(GrowArrow(a))
            vo.wait_until("a")
            self.play(Create(dx), Create(dy))
            self.play(FadeIn(bg), Write(col))
            vo.wait_until("b")
            self.play(ReplacementTransform(col, three))
            self.play(ReplacementTransform(three, many), FadeIn(n768), bg.animate.stretch_to_fit_height(4.2).move_to(many))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.play(FadeOut(VGroup(dx, dy, many, n768, bg, a, hist)))
        self.pl = pl

    # ------------------------------------------------------------------
    def two_moves(self):
        u, w = np.array([2.0, 1.0, 0]), np.array([-1.0, 2.0, 0])
        au, aw = arrow(u, color=I_COLOR), arrow(w, color=J_COLOR)
        lu = MathTex(r"\mathbf{u}", font_size=40, color=I_COLOR).next_to(u, DOWN + RIGHT, buff=0.1)
        lw = MathTex(r"\mathbf{v}", font_size=40, color=J_COLOR).next_to(w, LEFT, buff=0.15)
        aw2 = arrow(u + w, start=u, color=J_COLOR)
        s = arrow(u + w, color=C.BITS)
        ls = MathTex(r"\mathbf{u} + \mathbf{v}", font_size=40, color=C.BITS).next_to(u + w, UP, buff=0.15)
        para = Polygon(ORIGIN, u, u + w, w, stroke_width=0, fill_color=C.BITS, fill_opacity=0.12)
        a, b = ValueTracker(1.0), ValueTracker(1.0)
        comb = always_redraw(lambda: arrow(a.get_value() * u + b.get_value() * w, color=C.BITS))
        trail = TracedPath(lambda: a.get_value() * u + b.get_value() * w, stroke_color=C.BITS, stroke_width=2,
                           stroke_opacity=0.6)
        read = always_redraw(lambda: MathTex(rf"{a.get_value():+.1f}\,\mathbf{{u}} {b.get_value():+.1f}\,\mathbf{{v}}",
                                             font_size=36, color=C.BITS).to_corner(UL, buff=0.5)
                             .add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1))
        basis = label(r"a \textit{basis}: \ every vector is $a\,\mathbf{u} + b\,\mathbf{v}$ \ in exactly one way",
                      font_size=30).to_edge(DOWN, buff=0.4).add_background_rectangle(color=BACKGROUND, opacity=0.85,
                                                                                    buff=0.1)
        with self.voiceover(
            "Two moves make all of linear algebra. <bookmark mark='a'/> Add two vectors: walk along one, then along "
            "the other. <bookmark mark='b'/> And scale them: stretch, shrink or flip. Mix the two moves, a times u "
            "plus b times v, <bookmark mark='c'/> and as a and b vary the tip sweeps out the whole plane. Then u and v "
            "are a basis: every vector has exactly one pair of coordinates in it."
        ) as vo:
            self.play(GrowArrow(au), GrowArrow(aw), FadeIn(lu), FadeIn(lw))
            vo.wait_until("a")
            self.play(TransformFromCopy(aw, aw2), run_time=1.0)
            self.play(GrowArrow(s), FadeIn(ls), FadeIn(para))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(aw2, s, ls, para)))
            self.add(trail, comb, read)
            vo.wait_until("c")
            for va, vb in ((2.0, -1.0), (-1.5, -1.5), (-2.0, 1.5), (1.5, 1.8)):
                self.play(a.animate.set_value(va), b.animate.set_value(vb), run_time=0.9)
            self.play(FadeIn(basis))
        for m in (comb, read):
            m.clear_updaters()
        trail.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law_of_cosines(self):
        A, B = np.array([3.2, 0.6, 0]), np.array([1.2, 2.2, 0])
        o = np.array([-4.6, -2.3, 0])
        aa, ab = arrow(o + A, start=o, color=VA), arrow(o + B, start=o, color=VB)
        amb = Line(o + B, o + A, color=GREY_A, stroke_width=4)
        la = MathTex(r"\mathbf{a}", font_size=40, color=VA).next_to(o + A, DOWN, buff=0.15)
        lb = MathTex(r"\mathbf{b}", font_size=40, color=VB).next_to(o + B, LEFT, buff=0.15)
        lab = MathTex(r"\mathbf{a}-\mathbf{b}", font_size=34, color=GREY_A).move_to(o + (A + B) / 2 + np.array([0.75, 0.45, 0]))
        ang = Angle(Line(o, o + A), Line(o, o + B), radius=0.7, color=WHITE)
        th = MathTex(r"\theta", font_size=34).move_to(Angle(Line(o, o + A), Line(o, o + B), radius=1.0).point_from_proportion(0.5))
        pic = VGroup(aa, ab, amb, la, lb, lab, ang, th)
        dfn = definition_card(r"the dot product (inner product)",
                              MathTex(r"\mathbf{a}\cdot\mathbf{b} = a_1 b_1 + a_2 b_2 + \dots + a_d b_d", font_size=34),
                              width=6.2).to_corner(UL, buff=0.3)
        props = label(r"symmetric, \ linear in each slot, \ $\mathbf{a}\cdot\mathbf{a} = |\mathbf{a}|^2 > 0$",
                      font_size=24, color=GREY_A).next_to(dfn, DOWN, buff=0.15).align_to(dfn, LEFT)
        colors = {r"\mathbf{a}": VA, r"\mathbf{b}": VB, r"|\mathbf{a}|^2": VA, r"|\mathbf{b}|^2": VB,
                  r"|\mathbf{a}|": VA, r"|\mathbf{b}|": VB}
        rows = [
            cmath(r"|\mathbf{a}-\mathbf{b}|^2", "=", r"(\mathbf{a}-\mathbf{b})\cdot(\mathbf{a}-\mathbf{b})",
                  font_size=36, colors=colors),
            cmath(r"|\mathbf{a}-\mathbf{b}|^2", "=", r"|\mathbf{a}|^2", "+", r"|\mathbf{b}|^2", r"- 2\,\mathbf{a}\cdot\mathbf{b}",
                  font_size=36, colors=colors),
            cmath(r"|\mathbf{a}-\mathbf{b}|^2", "=", r"|\mathbf{a}|^2", "+", r"|\mathbf{b}|^2",
                  r"- 2\,|\mathbf{a}|\,|\mathbf{b}|\cos\theta", font_size=36, colors=colors),
            cmath(r"\mathbf{a}\cdot\mathbf{b}", "=", r"|\mathbf{a}|\,|\mathbf{b}|\cos\theta", font_size=40, colors=colors),
        ]
        whys = [why(r"a length squared is a dot product"), why(r"expand: \ linear, symmetric"),
                why(r"the law of cosines, \ Euclid II.12--13"), why(r"compare the two lines")]
        for w in whys:
            w.scale(0.9)
        step = ladder(self, rows, whys, keep=4, top=0.9, x=1.3, buff=0.32, edge=6.9)
        with self.voiceover(
            "How alike are two vectors? <bookmark mark='a'/> Multiply them coordinate by coordinate and add: the dot "
            "product, also called the inner product. It is symmetric, it is linear in each slot, and a vector dotted "
            "with itself is its length squared. <bookmark mark='b'/> Now draw the triangle with sides a, b and a minus "
            "b. Its third side squared is a dot product. <bookmark mark='c'/> Expand it. <bookmark mark='d'/> The law "
            "of cosines, from Euclid, says the same side squared is this. <bookmark mark='e'/> Compare: the dot "
            "product is the two lengths times the cosine of the angle between them. Lists of numbers carry "
            "geometry."
        ) as vo:
            self.play(FadeIn(dfn, shift=DOWN * 0.2))
            self.play(FadeIn(props))
            vo.wait_until("a")
            self.play(GrowArrow(aa), GrowArrow(ab), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(Create(amb), FadeIn(lab), Create(ang), FadeIn(th))
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            self.play(Circumscribe(rows[3], color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cauchy_schwarz(self):
        colors = {r"\mathbf{a}": VA, r"\mathbf{b}": VB, r"|\mathbf{a}|^2": VA, r"|\mathbf{b}|^2": VB,
                  r"|\mathbf{a}|": VA, r"|\mathbf{b}|": VB}
        rows = [
            cmath(r"0", r"\le", r"|\mathbf{a} - t\,\mathbf{b}|^2", font_size=36, colors=colors),
            cmath(r"0", r"\le", r"|\mathbf{a}|^2 - 2t\,(\mathbf{a}\cdot\mathbf{b}) + t^2\,|\mathbf{b}|^2", font_size=36,
                  colors=colors),
            cmath(r"4(\mathbf{a}\cdot\mathbf{b})^2 - 4|\mathbf{a}|^2|\mathbf{b}|^2", r"\le", r"0", font_size=36,
                  colors=colors),
            cmath(r"|\mathbf{a}\cdot\mathbf{b}|", r"\le", r"|\mathbf{a}|\,|\mathbf{b}|", font_size=42, colors=colors),
        ]
        whys = [why(r"a length squared, \ for every number $t$"), why(r"expand"),
                why(r"a parabola that never dips below $0$: \\ at most one root, \ discriminant $\le 0$"),
                why(r"equality only when $\mathbf{a} = t\,\mathbf{b}$")]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-1.2, buff=0.3, edge=6.9)
        ax = Axes(x_range=[-0.5, 3.5, 1], y_range=[0, 9, 3], x_length=4.6, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -2.4, 0])
        tl = MathTex(r"t", font_size=26, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        fl = MathTex(r"|\mathbf{a}-t\mathbf{b}|^2", font_size=24, color=GREY_B).next_to(ax.y_axis, UP, buff=0.08)
        th = ValueTracker(1.1)
        a_ = np.array([2.4, 0.0])

        def b_():
            return 1.3 * np.array([math.cos(th.get_value()), math.sin(th.get_value())])

        par = always_redraw(lambda: ax.plot(lambda t: float(np.sum((a_ - t * b_()) ** 2)), x_range=[-0.5, 3.5],
                                            color=C.BITS, stroke_width=4).set_stroke(opacity=1))
        o = np.array([1.6, -2.6, 0])
        va = arrow(o + np.array([*a_, 0]) * 0.75, start=o, color=VA, stroke_width=5)
        vb = always_redraw(lambda: arrow(o + np.array([*b_(), 0]) * 0.75, start=o, color=VB, stroke_width=5))
        cs = always_redraw(lambda: MathTex(rf"\cos\theta = {math.cos(th.get_value()):+.2f}", font_size=30)
                           .next_to(o, RIGHT, buff=2.2).shift(UP * 0.3))
        hist = note(r"Cauchy (1821, \ sums); \ Bunyakovsky (1859) and Schwarz (1888, \ integrals)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Is the cosine always between minus one and one, even in 768 dimensions? That's the Cauchy-Schwarz "
            "inequality, and its proof is short. <bookmark mark='a'/> For any number t, the length of a minus t b, "
            "squared, can't be negative. <bookmark mark='b'/> Expand it: a parabola in t. <bookmark mark='c'/> A "
            "parabola that never dips below zero touches zero at most once, so its discriminant can't be positive. "
            "<bookmark mark='d'/> Rearranged: the dot product is at most the product of the lengths. "
            "<bookmark mark='e'/> Turn b, and watch the parabola: its lowest point reaches zero only when b lines up "
            "with a. So the cosine is honest in any number of dimensions, and an angle between two words makes "
            "sense."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            self.play(Create(ax), FadeIn(tl), FadeIn(fl), FadeIn(va))
            self.add(par, vb, cs)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(hist))
            vo.wait_until("e")
            self.play(th.animate.set_value(0.0), run_time=2.5)
            self.play(th.animate.set_value(PI), run_time=2.5)
            self.play(th.animate.set_value(1.1), run_time=1.5)
        for m in (par, vb, cs):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def words(self):
        g = load("gpt2")
        V = np.asarray(g["barcodes"])
        cos = np.asarray(g["barcode_cos"])
        names = list(g["barcode_words"])
        assert names == ["dog", "puppy", "tobacco", "cat"]
        head = label(r"cosine similarity $= \dfrac{\mathbf{a} \cdot \mathbf{b}}{|\mathbf{a}|\,|\mathbf{b}|}$", font_size=38)
        head.to_edge(UP, buff=0.4)
        pairs = [(1, C.TRUE_P), (3, C.TRUE_P), (2, GREY_B)]
        rows = VGroup()
        for j, col in pairs:
            name = data_text(f"dog · {names[j]}", font=MONO, font_size=28, color=WHITE)
            w = 6.5 * max(cos[0, j], 0.02)
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9)
            val = MathTex(f"{cos[0, j]:.2f}", font_size=34, color=col)
            rows.add(VGroup(name, bar, val))
        for k, r in enumerate(rows):
            r[0].move_to([-4.3, 1.6 - 0.75 * k, 0], aligned_edge=RIGHT).shift(RIGHT * 1.4)
            r[1].move_to([-2.6, 1.6 - 0.75 * k, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        vmax = float(np.abs(V[:2]).max())
        prod = V[0] * V[1]
        b1 = barcode(V[0], width=9.0, height=0.7, vmax=vmax).move_to([0.2, -1.0, 0])
        b2 = barcode(V[1], width=9.0, height=0.7, vmax=vmax).move_to([0.2, -1.9, 0])
        b3 = barcode(prod, width=9.0, height=0.7, pos=C.REWARD, neg=C.PENALTY).move_to([0.2, -2.95, 0])
        n1 = data_text("dog", font=MONO, font_size=24).next_to(b1, LEFT, buff=0.25)
        n2 = data_text("puppy", font=MONO, font_size=24).next_to(b2, LEFT, buff=0.25)
        n3 = MathTex(r"\times", font_size=34).next_to(b3, LEFT, buff=0.35)
        tot = MathTex(rf"\textstyle\sum = {float(prod.sum()):.1f}", font_size=34, color=C.REWARD).next_to(b3, RIGHT, buff=0.2)
        c = cos[0]
        with self.voiceover(
            "Divide by the two lengths and you get the cosine similarity, which runs from minus one to one. "
            f"<bookmark mark='a'/> For GPT-2's words: dog and puppy, {c[1]:.2f}. Dog and cat, {c[3]:.2f}. Dog and "
            f"tobacco, {c[2]:.2f}. <bookmark mark='b'/> In 768 dimensions you can't draw the angle, but you can "
            "compute it: multiply the two lists number by number, and add."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in rows:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(n1), FadeIn(b1), FadeIn(n2), FadeIn(b2))
            self.play(TransformFromCopy(b1, b3), Indicate(b2, color=WHITE, scale_factor=1.02), FadeIn(n3), run_time=1.5)
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logits(self):
        g = load("gpt2")
        toks = [t.strip() for t in g["top_tokens"]]
        logit = np.asarray(g["top_logits"])
        prob = np.asarray(g["top_probs"])
        prompt = data_text(g["prompt"] + " …", font=MONO, font_size=28).to_edge(UP, buff=0.5)
        n = len(toks)
        xs = np.linspace(-4.6, 4.6, n)
        rel = logit - logit[0]
        bars_s, bars_p, labs = VGroup(), VGroup(), VGroup()
        for k in range(n):
            hs = 1.6 * (rel[k] + 1.5) / 1.5  # the score drawn as a height above a floor 1.5 below the best
            bars_s.add(Rectangle(width=0.9, height=max(hs, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                 fill_opacity=0.9).move_to([xs[k], -1.6 + max(hs, 0.02) / 2, 0]))
            hp = 1.8 * prob[k] / prob[0]
            bars_p.add(Rectangle(width=0.9, height=hp, stroke_width=0, fill_color=C.PROB, fill_opacity=0.9)
                       .move_to([xs[k], -1.6 + hp / 2, 0]))
            labs.add(data_text(toks[k], font=MONO, font_size=24, color=C.TOKEN).move_to([xs[k], -2.0, 0]))
        sv = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=C.MODEL_Q).next_to(b, UP, buff=0.08)
                      for v, b in zip(logit, bars_s)])
        pv = VGroup(*[MathTex(f"{v:.3f}", font_size=24, color=C.PROB).next_to(b, UP, buff=0.08)
                      for v, b in zip(prob, bars_p)])
        f = cmath(r"z_k", "=", r"\mathbf{h}", r"\cdot", r"\mathbf{e}_k", colors={r"z_k": C.MODEL_Q, r"\mathbf{h}": C.BITS,
                                                                           r"\mathbf{e}_k": C.TRUE_P}, font_size=46)
        f.next_to(prompt, DOWN, buff=0.45)
        soft_f = cmath(r"q_k", "=", r"\frac{e^{z_k}}{\sum_j e^{z_j}}", colors={r"q_k": C.PROB}, font_size=46).move_to(f)
        recall = label(r"Part 1: \ scores $z_k$, \ then the softmax", font_size=26, color=GREY_A).next_to(soft_f, DOWN, buff=0.25)
        fh = label(r"$\mathbf{h}$: the model's final state; \ $\mathbf{e}_k$: token $k$'s own vector", font_size=26,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        tie = label(rf"the same ${g['vocab']:,}$ vectors the tokens start as".replace(",", "{,}"), font_size=26,
                    color=C.TRUE_P).next_to(fh, DOWN, buff=0.12)
        soft = label(r"softmax: \ the probabilities", font_size=26, color=C.PROB).next_to(fh, DOWN, buff=0.12)
        floor = Line([-5.4, -1.6, 0], [5.4, -1.6, 0], color=GREY_D, stroke_width=1.5)
        order = ", then ".join(toks[:3])
        with self.voiceover(
            "Here is why this matters. In Part 1, a network ended with a score for every possible next token, and the "
            "softmax turned the scores into probabilities. <bookmark mark='a'/> In GPT-2, every one of those scores "
            "is a dot product: the model's final state, dotted with each token's vector, the very same vectors the "
            "tokens started out as. <bookmark mark='b'/> After the Eiffel Tower is located in the city of, the "
            f"biggest dot products belong to {order}. <bookmark mark='c'/> Only the differences matter: the softmax "
            f"gives {toks[0]} {100 * prob[0]:.1f} percent."
        ) as vo:
            self.play(FadeIn(prompt))
            self.play(Write(soft_f), FadeIn(recall))
            vo.wait_until("a")
            self.play(ReplacementTransform(soft_f, f), FadeOut(recall), FadeIn(fh))
            self.play(FadeIn(tie))
            vo.wait_until("b")
            self.play(Create(floor), FadeIn(labs), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_s], lag_ratio=0.15),
                      FadeIn(sv), run_time=1.6)
            vo.wait_until("c")
            self.play(ReplacementTransform(bars_s, bars_p), ReplacementTransform(sv, pv), ReplacementTransform(tie, soft),
                      run_time=1.6)
            self.play(Indicate(pv[0], color=WHITE, scale_factor=1.4))
        self.wait(0.5)
        self.clear_scene()
