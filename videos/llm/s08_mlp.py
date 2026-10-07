from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    PROMPT, Plot, data, label, load_arrays, random_values, show_chapter_card, token_row, vector_strip,
)

MLP_LAYER = 10


def gelu(x):
    x = np.asarray(x, dtype=float)
    return 0.5 * x * (1 + np.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x**3)))


def strip(seed, color, n=6, cell=0.17):
    return vector_strip(random_values(n, seed=seed), color=color, cell=cell, gap=0.03)


class MLP(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 7, "The MLP: where knowledge lives")
        self.d = data()
        self.arrays = load_arrays("gpt2_small")
        self.per_position()
        self.structure()
        self.neuron_view()
        self.facts()
        self.real_neurons()
        self.superposition()

    # ------------------------------------------------------------------
    def per_position(self):
        pieces = self.d["tokenize"][PROMPT + " Paris."]["pieces"][:-2][-6:]
        row = token_row(pieces, font_size=28, buff=0.45).to_edge(DOWN, buff=0.4)
        xs = [t.get_x() for t in row]
        below = VGroup(*[strip(i, C.EMBED).move_to([x, -1.9, 0]) for i, x in enumerate(xs)])
        boxes = VGroup(*[RoundedRectangle(width=0.75, height=0.75, corner_radius=0.1, stroke_color=C.MLP, stroke_width=2.5,
                                          fill_color=C.MLP, fill_opacity=0.2).move_to([x, -0.2, 0]) for x in xs])
        above = VGroup(*[strip(20 + i, C.EMBED).move_to([x, 1.5, 0]) for i, x in enumerate(xs)])
        same = label(r"the same MLP at every position", font_size=32, color=C.MLP).next_to(boxes, RIGHT, buff=0.4)
        if same.get_right()[0] > 6.9:
            VGroup(row, below, boxes, above).shift(LEFT * (same.get_right()[0] - 6.9))
            same.next_to(boxes, RIGHT, buff=0.4)
        note = label(r"no talking between positions here", font_size=28, color=GREY_A).next_to(same, DOWN, buff=0.2)
        note.align_to(same, LEFT)
        with self.voiceover(
            "After attention comes the second kind of step in every layer: a multilayer perceptron, or MLP. "
            "<bookmark mark='p'/> Unlike attention, it works on each position separately. The vectors don't talk to each "
            "other here. <bookmark mark='s'/> And every position goes through the very same MLP, with the same weights."
        ) as vo:
            self.play(FadeIn(row), FadeIn(below))
            vo.wait_until("p")
            self.play(FadeIn(boxes, lag_ratio=0.1))
            self.play(*[TransformFromCopy(b, a) for b, a in zip(below, above)], run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(same), FadeIn(note))
        self.clear_scene()

    # ------------------------------------------------------------------
    def structure(self):
        def column(n, x, color, radius=0.13, spread=5.4):
            ys = np.linspace(spread / 2, -spread / 2, n)
            return VGroup(*[Circle(radius, color=color, stroke_width=2.5).set_fill(color, 0.15).move_to([x, y, 0]) for y in ys])

        inp = column(8, -4.2, C.EMBED, spread=3.6)
        hid = column(16, 0.0, C.MLP, radius=0.12, spread=5.2)
        out = column(8, 4.2, C.EMBED, spread=3.6)
        for c in (inp, hid, out):
            c.shift(DOWN * 0.3)
        e1 = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.8, color=GREY_D).set_opacity(0.6)
                      for a in inp for b in hid])
        e2 = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.8, color=GREY_D).set_opacity(0.6)
                      for a in hid for b in out])
        l_in = label(r"768", font_size=32, color=C.EMBED).next_to(inp, DOWN, buff=0.25)
        l_hid = label(r"3072 neurons", font_size=32, color=C.MLP).next_to(hid, DOWN, buff=0.2)
        l_out = label(r"768", font_size=32, color=C.EMBED).next_to(out, DOWN, buff=0.25)
        w1 = MathTex(r"W_{\text{up}}", font_size=40, color=C.MLP).move_to(LEFT * 2.1 + UP * 3.1)
        w2 = MathTex(r"W_{\text{down}}", font_size=40, color=C.MLP).move_to(RIGHT * 2.1 + UP * 3.1)
        g = MathTex(r"\text{GELU}", font_size=34, color=C.MLP).next_to(hid, UP, buff=0.15)
        plus = label(r"added to the\\residual stream", font_size=28, color=GREY_A).next_to(out, RIGHT, buff=0.3)
        with self.voiceover(
            "An MLP does three things. <bookmark mark='u'/> First, it multiplies the vector by a big matrix, expanding it "
            "from 768 numbers to 3,072. <bookmark mark='g'/> Then it applies a simple nonlinear function to each of those "
            "numbers. <bookmark mark='d'/> Then a second matrix brings it back down to 768 numbers, <bookmark mark='a'/> and "
            "the result is added to the residual stream."
        ) as vo:
            self.play(FadeIn(inp), FadeIn(l_in))
            vo.wait_until("u")
            self.play(Create(e1, lag_ratio=0.002), FadeIn(hid), FadeIn(l_hid), FadeIn(w1), run_time=1.5)
            vo.wait_until("g")
            self.play(FadeIn(g), hid.animate.set_fill(C.MLP, 0.5))
            vo.wait_until("d")
            self.play(Create(e2, lag_ratio=0.002), FadeIn(out), FadeIn(l_out), FadeIn(w2), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(plus))
        self.net = VGroup(inp, hid, out, e1, e2, l_in, l_hid, l_out, w1, w2, g, plus)

    # ------------------------------------------------------------------
    def neuron_view(self):
        inp, hid, out, e1, e2 = self.net[:5]
        k = 6
        neuron = hid[k]
        PX = 3.9
        net = VGroup(inp, hid, out, e1, e2, self.net[5], self.net[6], self.net[7], self.net[10])
        q = MathTex(r"\vec r_i \cdot \vec x + b_i", font_size=40, color=C.MLP)
        q_note = label(r"``how much does $\vec x$ point along $\vec r_i$?''", font_size=28, color=GREY_A)
        qg = VGroup(q, q_note).arrange(DOWN, buff=0.15).move_to(RIGHT * PX + UP * 2.9)
        with self.voiceover(
            "Here's a useful way to read it. Look at a single neuron. <bookmark mark='r'/> Its incoming weights, one row of "
            "the first matrix, form a direction in the space. <bookmark mark='q'/> Taking the dot product with it asks a "
            "question: how much does this token's vector point that way? Add a bias, and that's the neuron's input."
        ) as vo:
            self.play(FadeOut(VGroup(self.net[8], self.net[9], self.net[11])), e1.animate.set_opacity(0.12),
                      e2.animate.set_opacity(0.12))
            self.play(net.animate.scale(0.82).to_edge(LEFT, buff=0.5))
            in_lines = VGroup(*[Line(a.get_center(), neuron.get_center(), stroke_width=2.5, color=C.MLP) for a in inp])
            vo.wait_until("r")
            self.play(Create(in_lines), neuron.animate.set_fill(C.MLP, 1.0).scale(1.4))
            vo.wait_until("q")
            self.play(FadeIn(qg, shift=DOWN * 0.2))

        pl = Plot((-3, 3), (-0.5, 3), width=3.4, height=2.0, x_ticks=[-2, 0, 2], y_ticks=[0, 2], font_size=22)
        pl.move_to(RIGHT * PX + UP * 0.45)
        curve = pl.line(np.linspace(-3, 3, 80), gelu(np.linspace(-3, 3, 80)), C.MLP, 4)
        relu = DashedVMobject(pl.line(np.linspace(-3, 3, 40), np.maximum(0, np.linspace(-3, 3, 40)), GREY_B, 2), num_dashes=30)
        gl = label(r"GELU", font_size=30, color=C.MLP).next_to(pl, LEFT, buff=0.3).shift(UP * 0.5)
        xv = ValueTracker(-2.2)
        pdot = always_redraw(lambda: Dot(pl.c2p(xv.get_value(), float(gelu(xv.get_value()))), color=YELLOW, radius=0.08))
        with self.voiceover(
            "The nonlinearity, called GELU, <bookmark mark='g'/> squashes negative inputs to nearly zero, and passes "
            "positive ones through. <bookmark mark='f'/> So each neuron is either quiet, or firing."
        ) as vo:
            vo.wait_until("g")
            self.play(Create(pl), Create(curve), Create(relu), FadeIn(gl))
            self.add(pdot)
            self.play(xv.animate.set_value(-0.3), run_time=1.2)
            vo.wait_until("f")
            self.play(xv.animate.set_value(2.4), run_time=1.5)

        out_lines = VGroup(*[Line(neuron.get_center(), b.get_center(), stroke_width=2.5, color=YELLOW) for b in out])
        out_l = MathTex(r"\vec c_i", font_size=40, color=YELLOW)
        out_note = label(r"= column $i$ of $W_{\text{down}}$, added to the vector", font_size=28, color=GREY_A)
        og = VGroup(out_l, out_note).arrange(RIGHT, buff=0.2).move_to(RIGHT * PX + DOWN * 1.35)
        total = MathTex(r"\text{MLP}(\vec x)", "=", r"\sum_i", r"\text{GELU}(\vec r_i \cdot \vec x + b_i)", r"\,\vec c_i",
                        font_size=38).move_to(RIGHT * PX + DOWN * 2.85)
        total[3].set_color(C.MLP)
        total[4].set_color(YELLOW)
        if total.get_right()[0] > 6.9:
            total.shift(LEFT * (total.get_right()[0] - 6.9))
        with self.voiceover(
            "And when neuron i fires, <bookmark mark='c'/> its outgoing weights, one column of the second matrix, are added "
            "to the vector, scaled by how strongly it fired. <bookmark mark='s'/> So the whole MLP is a sum: a long list of "
            "directions, each one switched on by its own question."
        ) as vo:
            vo.wait_until("c")
            self.play(Create(out_lines), FadeIn(og))
            vo.wait_until("s")
            self.play(Write(total))
        self.clear_scene()

    # ------------------------------------------------------------------
    def facts(self):
        x = strip(3, C.EMBED, n=8, cell=0.22).move_to(LEFT * 5.0 + DOWN * 0.3)
        xl = label(r"vector at ``of''\\after attention", font_size=28, color=C.EMBED).next_to(x, DOWN, buff=0.25)
        tags = VGroup(*[label(t, font_size=28, color=GREY_A) for t in
                        [r"\ldots mentions the Eiffel Tower", r"\ldots wants a city name next"]])
        tags.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(x, UP, buff=0.3).shift(RIGHT * 0.8)
        neuron = Circle(0.45, color=C.MLP, stroke_width=3).set_fill(C.MLP, 0.2).move_to(LEFT * 0.6 + DOWN * 0.3)
        nq = label(r"``Eiffel Tower\\and a city?''", font_size=28, color=C.MLP).next_to(neuron, UP, buff=0.25)
        a1 = Arrow(x.get_right(), neuron.get_left(), buff=0.15, color=GREY_B)
        out = strip(9, YELLOW, n=8, cell=0.22).move_to(RIGHT * 3.2 + DOWN * 0.3)
        ol = label(r"a direction\\meaning ``Paris''", font_size=28, color=YELLOW).next_to(out, DOWN, buff=0.25)
        a2 = Arrow(neuron.get_right(), out.get_left(), buff=0.15, color=YELLOW)
        tag = label(r"(cartoon: in real models, facts are spread across many neurons)", font_size=26, color=GREY_B)
        tag.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So, in a cartoon version: by the time our prompt reaches some layer, the vector at the word 'of' might "
            "encode <bookmark mark='a'/> that the text mentions the Eiffel Tower, <bookmark mark='b'/> and that a city "
            "name should come next. <bookmark mark='n'/> A neuron whose question matches that combination fires, "
            "<bookmark mark='p'/> and writes a direction meaning Paris into the vector."
        ) as vo:
            self.play(FadeIn(x), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tags[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(tags[1], shift=RIGHT * 0.2))
            vo.wait_until("n")
            self.play(GrowArrow(a1), FadeIn(neuron), FadeIn(nq))
            self.play(neuron.animate.set_fill(C.MLP, 0.9), Flash(neuron, color=C.MLP))
            vo.wait_until("p")
            self.play(GrowArrow(a2), FadeIn(out), FadeIn(ol))

        with self.voiceover(
            "Real models are messier: each fact seems to be spread across many neurons, and each neuron takes part in many "
            "different things. But experiments that edit or switch off parts of these layers suggest that the MLPs store "
            "much of what a model knows."
        ) as vo:
            self.play(Indicate(tag, color=WHITE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_neurons(self):
        acts = self.arrays["mlp_acts"][MLP_LAYER]
        frac = float((acts > 0.5).mean())
        assert abs(frac - self.d["mlp_frac_active"][MLP_LAYER]) < 1e-6 and 0.02 < frac < 0.05
        rows, cols = 48, 64
        cell = 0.088
        grid = VGroup()
        vmax = np.percentile(acts, 99.5)
        for v in acts[: rows * cols]:
            a = float(np.clip(v / vmax, 0, 1))
            grid.add(Square(cell * 0.86, stroke_width=0, fill_color=C.MLP if v > 0 else GREY_D,
                            fill_opacity=0.08 + 0.92 * a if v > 0 else 0.25))
        grid.arrange_in_grid(rows, cols, buff=cell * 0.14).move_to(LEFT * 2.2 + DOWN * 0.3)
        frame = SurroundingRectangle(grid, color=GREY_B, buff=0.06, stroke_width=1.5)
        title = label(rf"the 3072 neurons of GPT-2's layer {MLP_LAYER + 1} MLP, at the last token of our prompt (real)",
                      font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        n_on = int((acts > 0.5).sum())
        stat = VGroup(MathTex(rf"{n_on}", font_size=56, color=C.MLP), label(r"of 3072 fire strongly\\(about 1 in 30)",
                                                                            font_size=32)).arrange(DOWN, buff=0.2)
        stat.move_to(RIGHT * 4.6 + UP * 0.4)
        assert 25 < 3072 / n_on < 40
        with self.voiceover(
            "Here are the real neurons of one of GPT-2's MLP layers, <bookmark mark='g'/> at the last token of our prompt. "
            "<bookmark mark='s'/> Out of 3,072, only about one in thirty fires strongly. The rest stay close to zero."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("g")
            self.play(FadeIn(grid, lag_ratio=0.0005), Create(frame), run_time=2)
            vo.wait_until("s")
            self.play(FadeIn(stat, shift=UP * 0.2))

        pp = self.d["params"]
        share = pp["mlp_per_layer"] / pp["per_layer"]
        assert 0.6 < share < 0.7
        params = MathTex(r"2 \times 768 \times 3072 \approx 4.7 \text{ million parameters per layer}", font_size=36)
        params2 = label(r"two thirds of every block; in large models, most of all the weights", font_size=30,
                        color=GREY_A)
        VGroup(params, params2).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The two matrices hold about 4.7 million parameters per layer: twice as many as attention. In large models, "
            "that makes the MLPs home to most of all the weights."
        ) as vo:
            self.play(VGroup(grid, frame).animate.scale(0.85).shift(UP * 0.3), Write(params))
            self.play(FadeIn(params2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def superposition(self):
        rng = np.random.default_rng(0)
        dims = [3, 30, 768]
        hists, spread = [], {}
        bins = np.linspace(0, 180, 61)
        for dd in dims:
            v = rng.normal(size=(400, dd))
            v /= np.linalg.norm(v, axis=1, keepdims=True)
            ang = np.degrees(np.arccos(np.clip(v @ v.T, -1, 1)[np.triu_indices(400, 1)]))
            h, _ = np.histogram(ang, bins=bins)
            hists.append(h / h.max())
            spread[dd] = float(ang.std())
        assert 1.5 < spread[768] < 2.6  # "within a few degrees of perpendicular"

        pl = Plot((0, 180), (0, 1.05), width=9.0, height=3.6, x_ticks=[0, 45, 90, 135, 180],
                  x_fmt=lambda v: f"{v}^\\circ", y_ticks=[]).move_to(DOWN * 0.9)
        xl = label(r"angle between two random directions", font_size=28, color=GREY_A).next_to(pl, DOWN, buff=0.55)

        def bars(h):
            g = VGroup()
            w = 9.0 / 60
            for i, v in enumerate(h):
                r = Rectangle(width=w * 0.85, height=max(0.01, 3.6 * v), stroke_width=0, fill_color=C.EMBED, fill_opacity=0.85)
                r.move_to(pl.c2p((bins[i] + bins[i + 1]) / 2, 0), aligned_edge=DOWN)
                g.add(r)
            return g

        bs = [bars(h) for h in hists]
        dlab = [label(rf"in {dd} dimensions", font_size=36, color=YELLOW).move_to(pl.c2p(30, 0.9)) for dd in dims]
        puzzle = label(r"768 dimensions $\Rightarrow$ only 768 exactly perpendicular directions", font_size=32)
        puzzle2 = label(r"\ldots but far more than 768 things to represent?", font_size=32, color=GREY_A)
        VGroup(puzzle, puzzle2).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here's a puzzle. A space with 768 dimensions has room for only 768 directions that are exactly perpendicular "
            "to each other. <bookmark mark='b'/> Yet a model seems to know about far more than 768 different things."
        ) as vo:
            self.play(FadeIn(puzzle))
            vo.wait_until("b")
            self.play(FadeIn(puzzle2))

        with self.voiceover(
            "Part of the answer is a strange fact about high-dimensional space. <bookmark mark='a'/> Pick random directions "
            "in three dimensions, and the angles between them are all over the place. <bookmark mark='b'/> In 30 "
            "dimensions, they bunch up around ninety degrees. <bookmark mark='c'/> In 768 dimensions, almost every pair is "
            "within a few degrees of perpendicular."
        ) as vo:
            self.play(Create(pl), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bs[0]], lag_ratio=0.01), FadeIn(dlab[0]))
            vo.wait_until("b")
            self.play(Transform(bs[0], bs[1]), Transform(dlab[0], dlab[1]))
            vo.wait_until("c")
            self.play(Transform(bs[0], bs[2]), Transform(dlab[0], dlab[2]))

        sp = label(r"\emph{superposition}: many more features than dimensions,\\each in its own nearly perpendicular direction",
                   font_size=32, color=YELLOW).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In fact, the number of directions you can fit that are all nearly perpendicular grows exponentially with the "
            "dimension. Models appear to take advantage of this, <bookmark mark='s'/> packing many more features than they "
            "have dimensions into the same space, each in its own nearly perpendicular direction. Researchers call this "
            "superposition, and it's one reason the insides of these models are so hard to read."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeOut(VGroup(puzzle, puzzle2)), FadeIn(sp))
        self.clear_scene()
