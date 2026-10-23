from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import FWD, HIST, NEURON, PART, WEIGHT, unit_circle


class Neurons(VoiceoverScene):
    def construct(self):
        self.card()
        self.mcp()
        self.hebb()
        self.rosenblatt()
        self.widrow()

    def card(self):
        card = chapter_card(1, r"The first neurons", r"Can a network of switches compute, and can it learn?",
                            lit=(1943, 1949, 1958, 1960), part=PART)
        with self.voiceover("Chapter one. The first neurons."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mcp(self):
        ins = VGroup(*[Circle(radius=0.44, color=GREY_B, stroke_width=3, fill_color="#121722", fill_opacity=1)
                       .move_to([-5.7, 1.3 - 2.6 * k, 0]) for k in range(2)])
        names = VGroup(*[MathTex(rf"x_{k + 1}", font_size=34, color=GREY_A).next_to(ins[k], LEFT, buff=0.15)
                         for k in range(2)])
        body = unit_circle(r"\ge \theta", radius=0.78, font_size=36).move_to([-2.9, 0, 0])
        edges = VGroup(*[Arrow(ins[k].get_right(), body.get_left() + UP * (0.25 - 0.5 * k), buff=0.05, color=GREY_C,
                               stroke_width=3) for k in range(2)])
        wl = VGroup(*[MathTex(rf"w_{k + 1}", font_size=34, color=WEIGHT).move_to(edges[k].get_center() + UP * 0.35)
                      for k in range(2)])
        outc = Circle(radius=0.44, color=GREY_B, stroke_width=3, fill_color="#121722", fill_opacity=1).move_to([-0.5, 0, 0])
        oarr = Arrow(body.get_right(), outc.get_left(), buff=0.05, color=NEURON, stroke_width=4)
        yl = MathTex(r"y", font_size=34, color=GREY_A).next_to(outc, UP, buff=0.12)
        digits_in = VGroup(*[MathTex("0", font_size=40).move_to(c) for c in ins])
        digit_out = MathTex("0", font_size=40).move_to(outc)
        rule = cmath(r"y", r"=", r"\begin{cases} 1 & \text{if } w_1 x_1 + w_2 x_2 \ge \theta \\ 0 & \text{otherwise}"
                     r"\end{cases}", font_size=38).move_to([3.5, 2.6, 0])
        defc = definition_card(r"A McCulloch--Pitts unit",
                               r"inputs and output are $0$ or $1$; \ it fires when the weighted sum of its inputs "
                               r"reaches a threshold $\theta$", color=NEURON, width=6.4).move_to([3.4, 2.4, 0])
        # the truth table, filled in as the inputs are switched
        rows = [(0, 0), (0, 1), (1, 0), (1, 1)]
        head = VGroup(*[MathTex(t, font_size=36, color=c) for t, c in ((r"x_1", GREY_A), (r"x_2", GREY_A),
                                                                     (r"\text{AND}", FWD), (r"\text{OR}", FWD))])
        xs_ = [1.3, 2.5, 4.0, 5.6]
        for t, x in zip(head, xs_):
            t.move_to([x, 0.75, 0])
        hline = Line([0.7, 0.35, 0], [6.4, 0.35, 0], color=GREY_C, stroke_width=1.5)
        cells = {}
        for i, (a, b) in enumerate(rows):
            yy = -0.1 - 0.62 * i
            cells[(i, 0)] = MathTex(str(a), font_size=36).move_to([xs_[0], yy, 0])
            cells[(i, 1)] = MathTex(str(b), font_size=36).move_to([xs_[1], yy, 0])
            cells[(i, 2)] = MathTex(str(int(a + b >= 2)), font_size=36, color=FWD).move_to([xs_[2], yy, 0])
            cells[(i, 3)] = MathTex(str(int(a + b >= 1)), font_size=36, color=FWD).move_to([xs_[3], yy, 0])
        settings = {"and": (r"w_1 = w_2 = 1,\ \ \theta = 2", FWD), "or": (r"w_1 = w_2 = 1,\ \ \theta = 1", FWD)}
        setl = MathTex(settings["and"][0], font_size=34, color=WEIGHT).move_to([-3.3, -2.75, 0])
        setl2 = MathTex(settings["or"][0], font_size=34, color=WEIGHT).move_to(setl)
        notl = label(r"NOT: \ one input, \ $w = -1$, \ $\theta = 0$", font_size=30, color=WEIGHT).move_to([3.5, -2.85, 0])
        cite_ = cite(r"W.~S.~McCulloch \& W.~Pitts, \textit{A Logical Calculus of the Ideas Immanent in Nervous "
                     r"Activity} (1943)", corner=DL)

        def fire(i, col):
            a, b = rows[i]
            out = int(a + b >= (2 if col == 2 else 1))
            anims = [Transform(digits_in[0], MathTex(str(a), font_size=40).move_to(ins[0])),
                     Transform(digits_in[1], MathTex(str(b), font_size=40).move_to(ins[1])),
                     ins[0].animate.set_fill(FWD if a else "#121722", opacity=0.5 if a else 1),
                     ins[1].animate.set_fill(FWD if b else "#121722", opacity=0.5 if b else 1),
                     Transform(digit_out, MathTex(str(out), font_size=40).move_to(outc)),
                     outc.animate.set_fill(FWD if out else "#121722", opacity=0.5 if out else 1)]
            return anims

        with self.voiceover(
            "In 1943, Warren McCulloch, a neurophysiologist, and Walter Pitts, a young logician, published a "
            "logical calculus of the ideas immanent in nervous activity. Their neuron is a switch. "
            "<bookmark mark='a'/> Its inputs are zero or one, and each comes in with a weight. "
            "<bookmark mark='b'/> The unit fires, it outputs a one, when the weighted sum reaches a threshold. "
            "<bookmark mark='c'/> With both weights one and a threshold of two, it fires only when both inputs are on: "
            "that's AND. <bookmark mark='d'/> Lower the threshold to one, and it fires when either is on: OR. "
            "<bookmark mark='e'/> One input with weight minus one and threshold zero gives NOT. From AND, OR and NOT "
            "you can build any logical formula, so a network of these units can compute anything a logic circuit can. "
            "But every weight was set by hand. Nothing learned."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(names), FadeIn(digits_in), FadeIn(cite_), FadeIn(defc))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.2), FadeIn(wl), FadeIn(body))
            vo.wait_until("b")
            self.play(GrowArrow(oarr), FadeIn(outc), FadeIn(yl), FadeIn(digit_out), FadeOut(defc), Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(head), Create(hline), FadeIn(setl))
            for i in range(4):
                self.play(*fire(i, 2), run_time=0.45)
                self.play(FadeIn(cells[(i, 0)]), FadeIn(cells[(i, 1)]), FadeIn(cells[(i, 2)]), run_time=0.35)
            vo.wait_until("d")
            self.play(Transform(setl, setl2))
            for i in range(4):
                self.play(*fire(i, 3), FadeIn(cells[(i, 3)]), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(notl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hebb(self):
        a = Circle(radius=0.7, color=NEURON, stroke_width=4).move_to([-5.2, 0.5, 0])
        b = Circle(radius=0.7, color=NEURON, stroke_width=4).move_to([-1.5, 0.5, 0])
        al, bl = (label(t, font_size=30, color=GREY_A).next_to(c, DOWN, buff=0.2) for t, c in
                  ((r"cell A", a), (r"cell B", b)))
        syn = Line(a.get_right(), b.get_left(), color=WEIGHT, stroke_width=2)
        w = ValueTracker(2.0)
        syn.add_updater(lambda m: m.set_stroke(width=w.get_value()))
        quote = wrapped_label(r"``When an axon of cell A is near enough to excite a cell B and repeatedly or "
                              r"persistently takes part in firing it, some growth process or metabolic change takes "
                              r"place in one or both cells such that A's efficiency, as one of the cells firing B, is "
                              r"increased.''", 6.4, 28, WHITE)
        src = label(r"D.~O.~Hebb, \textit{The Organization of Behavior} (1949), p.~62", font_size=22, color=GREY_B)
        qc = VGroup(quote, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, 0.5, 0])
        head = label(r"1949: \ Donald Hebb, \ a psychologist, \ asks where learning comes from", font_size=32,
                     color=HIST).to_edge(UP, buff=0.55)
        rule = cmath(r"\Delta w_{AB}", r"=", r"\eta", r"\, x_A", r"\, x_B", font_size=50,
                     colors={r"\Delta w_{AB}": WEIGHT}).move_to([-3.35, -2.2, 0])
        rl = label(r"strengthen a connection by the activity at both ends", font_size=24, color=GREY_A)
        rl.next_to(rule, DOWN, buff=0.25)
        later = label(r"later summarized: \\ ``cells that fire together wire together''", font_size=26, color=GREY_B)
        later.move_to([3.3, -2.45, 0])

        def spikes():
            ds = [glow_dot(a.get_center(), color=FWD, radius=0.12), glow_dot(b.get_center(), color=FWD, radius=0.12)]
            return Succession(AnimationGroup(FadeIn(ds[0], scale=2), FadeIn(ds[1], scale=2)),
                              AnimationGroup(FadeOut(ds[0]), FadeOut(ds[1])), run_time=0.6)

        with self.voiceover(
            "Where would learning come from? In 1949 the psychologist Donald Hebb proposed an answer, for real "
            "neurons. <bookmark mark='a'/> When an axon of cell A is near enough to excite a cell B, and repeatedly "
            "or persistently takes part in firing it, some growth process or metabolic change takes place in one or "
            "both cells, such that A's efficiency, as one of the cells firing B, is increased. <bookmark mark='b'/> "
            "In symbols: strengthen a connection in proportion to the activity at both of its ends. Decades later it "
            "was summed up as: cells that fire together, wire together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), FadeIn(al), FadeIn(bl), Create(syn))
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.2))
            for k in range(4):
                self.play(spikes(), w.animate.set_value(2.0 + 2.5 * (k + 1)), run_time=0.8)
            vo.wait_until("b")
            self.play(Write(rule), FadeIn(rl))
            self.play(FadeIn(later))
        syn.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rosenblatt(self):
        g = np.random.default_rng(1958)  # the random wiring of the drawing
        n, s = 20, 0.155
        retina = VGroup(*[Square(s, stroke_width=0.6, stroke_color=GREY_D, fill_color=GREY_E, fill_opacity=1)
                          .move_to([-5.0 + (j - n / 2 + 0.5) * s, 0.35 + (n / 2 - i - 0.5) * s, 0])
                          for i in range(n) for j in range(n)])
        letter = [(i, j) for i in range(4, 16) for j in range(5, 8)] + [(i, j) for i in range(4, 7) for j in range(8, 15)]
        for i, j in letter:  # a T on the camera
            retina[i * n + j].set_fill(WHITE, opacity=0.9)
        A = VGroup(*[Circle(radius=0.115, color=NEURON, stroke_width=2).move_to([-2.1, 2.35 - 0.27 * k, 0])
                     for k in range(16)])
        R = VGroup(*[Circle(radius=0.15, color=FWD, stroke_width=2.5).move_to([-0.35, 1.5 - 0.45 * k, 0]) for k in range(8)])
        wires = VGroup()
        for k in range(16):
            for c in g.choice(n * n, 5, replace=False):
                wires.add(Line(retina[c].get_center(), A[k].get_left(), stroke_width=0.5, color=GREY_C, stroke_opacity=0.6))
        out_w = VGroup(*[Line(a_.get_right(), r_.get_left(), stroke_width=0.7, color=WEIGHT, stroke_opacity=0.7)
                         for a_ in A for r_ in R])
        cap = VGroup(label(r"$20 \times 20 = 400$ photocells", font_size=24, color=GREY_A).next_to(retina, DOWN, buff=0.25),
                     label(r"$512$ association \\ units ($16$ drawn)", font_size=24, color=NEURON).next_to(A, DOWN, buff=0.25),
                     label(r"$8$ response \\ units", font_size=24, color=FWD).next_to(R, DOWN, buff=0.25))
        cap[2].shift(RIGHT * 0.2)
        tag = note(r"schematic").next_to(VGroup(retina, R), UP, buff=0.35).align_to(retina, LEFT)
        c1 = history_card(1958, r"Frank Rosenblatt, \ Cornell Aeronautical Laboratory: \ the perceptron",
                          r"simulated on an IBM 704: \ after $50$ trials it told cards marked on the left from cards "
                          r"marked on the right", width=6.0, color=HIST).move_to([3.75, 1.6, 0])
        c2 = history_card(r"8 July 1958", r"\textit{The New York Times}: \ ``New Navy Device Learns by Doing''",
                          r"the Navy expects it ``will be able to walk, talk, see, write, reproduce itself and be "
                          r"conscious of its existence''", width=6.0, color=C.SURPRISE).move_to([3.75, -1.3, 0])
        c3 = history_card(1960, r"The Mark I Perceptron, \ shown in June 1960",
                          r"$400$ photocells, \ $512$ association units, \ $8$ response units; \ the weights were "
                          r"potentiometers turned by electric motors", width=6.0, color=HIST).move_to([3.75, -1.3, 0])
        with self.voiceover(
            "In 1958 Frank Rosenblatt, a psychologist at the Cornell Aeronautical Laboratory, put the two ideas "
            "together: a McCulloch and Pitts unit whose weights are learned from examples. He called it the "
            "perceptron. <bookmark mark='a'/> That July he showed it, simulated on an IBM 704 computer: after fifty "
            "trials, it had taught itself to tell cards marked on the left from cards marked on the right. "
            "<bookmark mark='b'/> The New York Times reported that the Navy expected the machine to walk, talk, see, "
            "write, reproduce itself, and be conscious of its existence. <bookmark mark='c'/> Then he built it. The "
            "Mark I Perceptron, shown in 1960, had a camera of four hundred photocells, twenty by twenty, wired at "
            "random to five hundred and twelve association units, which fed eight response units. <bookmark mark='d'/> "
            "Its weights were potentiometers, turned by electric motors as it learned."
        ) as vo:
            self.play(FadeIn(retina), FadeIn(cap[0]), FadeIn(tag), FadeIn(c1, shift=UP * 0.2))
            self.play(Create(wires), FadeIn(A), FadeIn(cap[1]), run_time=1.5)
            vo.wait_until("a")
            self.play(Circumscribe(c1, color=HIST))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(c2), FadeIn(c3, shift=UP * 0.2), Create(out_w), FadeIn(R), FadeIn(cap[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[Indicate(r_, color=FWD) for r_ in R], lag_ratio=0.1),
                      out_w.animate.set_stroke(width=1.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def widrow(self):
        colors = {r"w": WEIGHT, r"\eta": GREY_A}
        perc = cmath(r"w \leftarrow w + y\, x", font_size=48).move_to([-3.6, 2.3, 0])
        pl = label(r"Rosenblatt: \ only after a mistake, \\ by the whole input", font_size=28, color=GREY_A)
        pl.next_to(perc, DOWN, buff=0.25)
        rows = [cmath(r"L(w)", r"=", r"\tfrac12\,(y - w \cdot x)^2", colors=colors, font_size=42),
                cmath(r"\nabla_w L", r"=", r"-(y - w \cdot x)\, x", colors=colors, font_size=42),
                cmath(r"w", r"\leftarrow", r"w + \eta\,(y - w \cdot x)\, x", colors=colors, font_size=42)]
        whys = [why(r"the squared error on one example"), why(r"chain rule"), why(r"a small step downhill")]
        step = ladder(self, rows, whys, keep=3, top=0.7, x=1.2, buff=0.6, edge=6.9)
        hc = history_card(1960, r"Bernard Widrow \& Ted Hoff, \ Stanford: \ ADALINE",
                          r"an adaptive linear neuron, \ trained by least mean squares", width=5.6,
                          color=HIST).move_to([3.6, 2.4, 0])
        sgd = label(r"every example, \ in proportion to the error: \\ stochastic gradient descent \ (Part 11)",
                    font_size=30, color=C.BITS).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Two years later, at Stanford, Bernard Widrow and his student Ted Hoff built ADALINE, an adaptive linear "
            "neuron, with a different rule. <bookmark mark='a'/> The perceptron changes its weights only after a "
            "mistake, and then by the whole input. <bookmark mark='b'/> Widrow and Hoff instead wrote down the "
            "squared error on one example, before the threshold, <bookmark mark='c'/> took its gradient, "
            "<bookmark mark='d'/> and stepped a little way downhill, on every example, in proportion to the error. "
            "<bookmark mark='e'/> That's the least mean squares rule, and it is stochastic gradient descent: the "
            "update that trains every network in this series, and the subject of Part 11."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), Write(perc))
            vo.wait_until("a")
            self.play(FadeIn(pl), Circumscribe(perc, color=GREY_A))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            self.play(Create(SurroundingRectangle(rows[2], color=C.BITS, buff=0.12, corner_radius=0.08)))
            vo.wait_until("e")
            self.play(FadeIn(sgd))
        self.wait(0.3)
        self.clear_scene()
