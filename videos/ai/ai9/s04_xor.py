from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import (BWD, CLS_A, CLS_B, FWD, HIST, NEURON, PART, WEIGHT, load, network, panel,
                                  region_image)
from videos.ai.ai9.s03_perceptron import clip_line

XOR_PTS = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]


class XOR(VoiceoverScene):
    def construct(self):
        self.card()
        self.proof()
        self.book()
        self.hidden()

    def card(self):
        card = chapter_card(3, r"XOR, and the first winter", r"What can't a single layer do?", lit=(1969,), part=PART)
        with self.voiceover("Chapter three. XOR, and the first winter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def proof(self):
        d = load("perceptron")
        xe = [int(v) for v in d["xor_epochs"]]
        c, side = np.array([-4.6, 1.0, 0]), 3.2
        sq = Square(side, stroke_color=GREY_D, stroke_width=1.5).move_to(c)

        def P(x, y):
            return c + np.array([(x - 0.5) * side / 1.8, (y - 0.5) * side / 1.8, 0])

        pts = VGroup(*[Dot(P(*p), radius=0.13, color=CLS_B if v else CLS_A) for p, v in XOR_PTS])
        lab = VGroup(*[MathTex(rf"({p[0]},{p[1]}) \to {v}", font_size=24, color=CLS_B if v else CLS_A)
                       .next_to(P(*p), DOWN if p[1] == 0 else UP, buff=0.18) for p, v in XOR_PTS])
        head = label(r"XOR: \ fire when exactly one input is on", font_size=26, color=WHITE).next_to(sq, UP, buff=0.55)
        colors = {r"\theta": WEIGHT, r"w_1": WEIGHT, r"w_2": WEIGHT}
        rows = [cmath(r"0", r"<", r"\theta", font_size=34, colors=colors),
                cmath(r"w_1 \ge \theta,", r"\ \ ", r"w_2 \ge \theta", font_size=34, colors=colors),
                cmath(r"w_1 + w_2", r"<", r"\theta", font_size=34, colors=colors),
                cmath(r"w_1 + w_2", r"\ge", r"2\theta \ > \ \theta", font_size=34, colors=colors)]
        whys = [why(r"$(0,0)$ must not fire"), why(r"$(1,0)$ and $(0,1)$ must fire"), why(r"$(1,1)$ must not fire"),
                why(r"add the middle line; \ $\theta > 0$")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=1.2, buff=0.55, edge=6.9, align_index=None)
        cross = Cross(VGroup(rows[2], rows[3]), stroke_color=C.SURPRISE, stroke_width=5).scale(0.6)
        bad = label(r"contradiction: \ no line does it", font_size=28, color=C.SURPRISE).move_to([2.6, -1.1, 0])
        # the perceptron on XOR: mistakes in every pass, forever
        n = len(xe)
        bw = 0.12
        bars = VGroup(*[Rectangle(width=bw, height=0.32 * v, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.85)
                        .move_to([-6.2 + i * (bw + 0.05) + bw / 2, -3.0 + 0.16 * v, 0]) for i, v in enumerate(xe)])
        base = Line([-6.3, -3.0, 0], [-6.2 + n * (bw + 0.05) + 0.05, -3.0, 0], color=GREY_C, stroke_width=1.5)
        bl = label(rf"the perceptron on XOR: \ mistakes in each of ${n}$ passes", font_size=22, color=GREY_A)
        bl.next_to(base, UP, buff=1.55).align_to(base, LEFT)
        with self.voiceover(
            "Here is the simplest thing a single unit cannot do. XOR, exclusive or: fire when exactly one input is "
            "on. <bookmark mark='a'/> Suppose a threshold unit did it. The input zero, zero must not fire, so the "
            "threshold is positive. <bookmark mark='b'/> Each input alone must fire, so each weight is at least theta. "
            "<bookmark mark='c'/> Both together must not fire, so the two weights add up to less than theta. "
            "<bookmark mark='d'/> But adding the middle line, they add up to at least two theta, which is more than "
            "theta. A contradiction: no line puts the two blue points on one side and the two pink ones on the "
            f"other. <bookmark mark='e'/> Run the perceptron on it anyway, and it never settles: in every one of {n} "
            f"passes, it makes between {min(xe)} and {max(xe)} mistakes."
        ) as vo:
            self.play(Create(sq), FadeIn(pts, scale=1.5), FadeIn(lab), FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(Create(cross), FadeIn(bad))
            vo.wait_until("e")
            self.play(Create(base), FadeIn(bl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.04),
                      run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def book(self):
        hc = history_card(1969, r"Marvin Minsky \& Seymour Papert, \ MIT: \ \textit{Perceptrons}",
                          r"theorems on what a single layer of trainable weights can compute", width=6.0,
                          color=HIST).move_to([-3.4, 2.3, 0])
        # two figures on a retina: connected and not (schematic)
        def retina(cells, center):
            g = VGroup()
            n, s = 9, 0.26
            for i in range(n):
                for j in range(n):
                    on = (i, j) in cells
                    g.add(Square(s, stroke_width=0.6, stroke_color=GREY_D, fill_color=WHITE if on else GREY_E,
                                 fill_opacity=0.9 if on else 1).move_to(center + np.array([(j - 4) * s, (4 - i) * s, 0])))
            return g

        ring = {(i, j) for i in range(1, 8) for j in range(1, 8) if i in (1, 7) or j in (1, 7)}
        conn = ring | {(4, j) for j in range(1, 6)}
        disc = (ring - {(1, 4), (7, 4)}) | {(4, j) for j in range(2, 5)}
        r1, r2 = retina(conn, np.array([-5.0, -1.0, 0])), retina(disc, np.array([-1.8, -1.0, 0]))
        l1 = label(r"connected", font_size=22, color=FWD).next_to(r1, DOWN, buff=0.15)
        l2 = label(r"not connected", font_size=22, color=C.SURPRISE).next_to(r2, DOWN, buff=0.15)
        res = label(r"parity and connectedness: \ a single layer needs units \\ that see nearly the whole picture",
                    font_size=22, color=GREY_A).move_to([-3.4, -3.15, 0])
        tag = note(r"schematic").next_to(r2, RIGHT, buff=0.2).align_to(r2, DOWN)
        quote = wrapped_label(r"``we consider it to be an important research problem to elucidate (or reject) our "
                              r"intuitive judgment that the extension is sterile.''", 5.4, 24, WHITE)
        qsrc = label(r"Minsky \& Papert, \textit{Perceptrons} (1969), on networks of many layers", font_size=18,
                     color=GREY_B)
        qc = VGroup(quote, qsrc).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 1.9, 0])
        winter = VGroup(
            label(r"1971: \ Rosenblatt dies, \ aged $43$", font_size=24, color=GREY_A),
            label(r"the 1970s: \ money and students go to symbolic AI \ (Part 2)", font_size=24, color=GREY_A),
            label(r"1980: \ Fukushima's neocognitron, \ ancestor of the convnet \ (Part 10)", font_size=24,
                  color=NEURON),
            label(r"1982: \ Hopfield's network revives the field \ (Part 20)", font_size=24, color=NEURON),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -1.5, 0])
        with self.voiceover(
            "In 1969 Marvin Minsky and Seymour Papert of MIT published Perceptrons, a book of careful theorems about "
            "what these machines can compute. <bookmark mark='a'/> A single layer of trainable weights can't "
            "compute parity, and can't tell a connected figure from a disconnected one, unless some of its units see "
            "nearly the whole picture at once. <bookmark mark='b'/> Networks with more layers could do more, and they "
            "knew it, but nobody knew how to train them. Of such machines, the authors wrote that it was an "
            "important research problem to elucidate, or reject, their intuitive judgment that the extension is sterile. "
            "<bookmark mark='c'/> Rosenblatt died in a boating accident in 1971. Money and students went to the "
            "symbolic AI of Part 2. <bookmark mark='d'/> Through the seventies only a few kept going; Kunihiko "
            "Fukushima's neocognitron of 1980 is the ancestor of the convolutional networks of Part 10, and John "
            "Hopfield's network of 1982 brought physicists back to the subject."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(r2), FadeIn(l1), FadeIn(l2), FadeIn(tag), FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(qc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(winter[0]), FadeIn(winter[1]))
            vo.wait_until("d")
            self.play(FadeIn(winter[2]), FadeIn(winter[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hidden(self):
        d = load("xor")
        keep = [int(k) for k in d["keep"]]
        losses = np.asarray(d["losses"])
        side = 3.4
        cin, chid = np.array([-4.6, 0.8, 0]), np.array([-0.7, 0.8, 0])
        fin, fhid = panel(side + 0.2, side + 0.2, cin), panel(side + 0.2, side + 0.2, chid)
        tin = label(r"the input square", font_size=24, color=GREY_A).next_to(fin, UP, buff=0.12)
        thid = label(r"as the hidden layer sees it", font_size=24, color=GREY_A).next_to(fhid, UP, buff=0.12)

        def Pin(p):
            return cin + np.array([(p[0] - 0.5) * side / 2, (p[1] - 0.5) * side / 2, 0])

        def Phid(h):
            return chid + np.array([h[0] * side / 2.3, h[1] * side / 2.3, 0])

        imgs = {t: region_image(d[f"q{t}"], np.zeros_like(d[f"q{t}"]), d["xs"], side, side, boundary=False).move_to(cin)
                for t in keep}
        pin = VGroup(*[Dot(Pin(p), radius=0.11, color=CLS_B if v else CLS_A) for p, v in XOR_PTS])

        def hid_picture(t):
            G = np.asarray(d[f"grid{t}"])
            lines = VGroup(*[VMobject(stroke_width=1.6, color=GREY_B if i < 9 else GREY_C, stroke_opacity=0.8)
                             .set_points_as_corners([Phid(h) for h in L]) for i, L in enumerate(G)])
            H = np.asarray(d[f"h{t}"])
            dots = VGroup(*[Dot(Phid(h), radius=0.11, color=CLS_B if v else CLS_A) for h, (_, v) in zip(H, XOR_PTS)])
            w = np.asarray(d[f"w2_{t}"])
            seg = clip_line(w, L=1.15)
            sep = (Line(Phid(seg[0]), Phid(seg[1]), color=WEIGHT, stroke_width=3.5) if seg else VectorizedPoint(chid))
            return VGroup(lines, sep, dots)

        net = network([2, 2, 1], x0=-6.0, x1=-3.8, height=1.0, center=[-4.9, -2.6, 0], radius=0.16)
        netl = label(r"$2 \to 2 \to 1$, \ tanh, \ sigmoid output", font_size=20, color=GREY_A)
        netl.next_to(net, RIGHT, buff=0.3)
        g = axes([0, keep[-1]], [0, 0.8], x_length=4.0, y_length=2.4, xlabel=r"step", ylabel=r"loss \ (cross-entropy)",
                 xticks=[0, keep[-1]], yticks=[0, 0.4, 0.8], center=[4.6, 1.2, 0], font_size=18)
        t = ValueTracker(0)

        def lossline():
            n_ = max(2, int(t.get_value()) + 1)
            xs = np.arange(0, n_, 10)
            return VMobject(color=BWD, stroke_width=3).set_points_as_corners([g.ax.c2p(x, min(losses[x], 0.8)) for x in xs])

        live = always_redraw(lossline)
        dot = always_redraw(lambda: glow_dot(g.ax.c2p(t.get_value(), min(losses[int(t.get_value())], 0.8)), color=BWD,
                                             radius=0.06))
        sv = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28)
                           .move_to([4.6, -0.75, 0]))
        tag = note(r"computed: \ trained with the series' own autodiff \ (Part 4)").to_corner(DR, buff=0.2)
        l0, l1 = float(losses[0]), float(losses[-1])
        solved, starts = int(d["solved"]), int(d["starts"])
        cur_img, cur_h = imgs[keep[0]], hid_picture(keep[0])
        caveat = (f"One honest caveat: from {starts} random starts, {solved} found a solution like this. The others got "
                  "stuck with one point wrong, in a local minimum of the loss. This is one that didn't."
                  if solved < starts else f"All {starts} random starts found a solution like this one.")
        with self.voiceover(
            "What a single unit can't do, two layers can. Put two units in the middle, hidden between the input and "
            "the output, and train all the weights by gradient descent, with the series' own automatic "
            "differentiation from Part 4. <bookmark mark='a'/> On the left, the input square, tinted by what the "
            "network says about every point of it. <bookmark mark='b'/> On the right, the same square as the hidden "
            "layer sees it: every grid line, bent by the two tanh units, and the output unit's line, in yellow."
        ) as vo:
            self.play(FadeIn(net), FadeIn(netl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fin), FadeIn(tin), FadeIn(cur_img), FadeIn(pin))
            vo.wait_until("b")
            self.play(FadeIn(fhid), FadeIn(thid), FadeIn(cur_h), FadeIn(g))
            self.add(live, dot, sv)
        with self.voiceover(
            "Now train. <bookmark mark='a'/> The hidden layer bends and folds the square, until the two blue points "
            "sit on one side of a straight line and the two pink on the other. Then the output unit, which can only "
            f"draw a line, has an easy job. The loss falls from {l0:.2f} to {l1:.4f}. <bookmark mark='b'/> " + caveat
        ) as vo:
            vo.wait_until("a")
            for k in keep[1:]:
                nh = hid_picture(k)
                self.play(FadeOut(cur_img), FadeIn(imgs[k]), Transform(cur_h, nh), t.animate.set_value(k), run_time=0.9)
                cur_img = imgs[k]
                self.bring_to_front(pin)
            vo.wait_until("b")
            for m in (live, dot, sv):
                m.clear_updaters()
            self.play(Indicate(cur_h[2], color=WHITE))
        self.wait(0.3)
        self.clear_scene()
