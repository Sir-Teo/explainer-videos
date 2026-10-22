from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import CLS_A, CLS_B, HIST, PART, PLAIN, load, region_image

T0, T1, XL, XR = 1938, 2016, -6.5, 6.5


def year_x(y):
    return XL + (XR - XL) * (y - T0) / (T1 - T0)


class Hook(VoiceoverScene):
    def construct(self):
        self.era()
        self.spiral()
        self.plan()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: seventy years of neural networks on one strip, with the two winters shaded."""
        y0 = -0.35
        axis = Line([XL, y0, 0], [XR, y0, 0], color=GREY_C, stroke_width=2.5)
        ticks = VGroup()
        for yr in range(1940, 2020, 10):
            ticks.add(Line([year_x(yr), y0 - 0.07, 0], [year_x(yr), y0 + 0.07, 0], color=GREY_C, stroke_width=2))
            ticks.add(Text(str(yr), font_size=18, color=GREY_B).next_to([year_x(yr), y0, 0], DOWN, buff=0.14))
        winters = VGroup()
        for a, b, name in ((1969, 1982, r"the first winter"), (1995, 2006, r"the second winter")):
            r = Rectangle(width=year_x(b) - year_x(a), height=5.4, stroke_width=0, fill_color=GREY_D, fill_opacity=0.28)
            r.move_to([(year_x(a) + year_x(b)) / 2, y0 + 0.2, 0])
            t = label(name, font_size=20, color=GREY_B).move_to([(year_x(a) + year_x(b)) / 2, -3.05, 0])
            winters.add(VGroup(r, t))
        events = [  # year, text, above?
            (1943, r"McCulloch \& Pitts: \\ a neuron in logic", True),
            (1958, r"Rosenblatt: \\ a perceptron that learns", False),
            (1969, r"Minsky \& Papert: \\ \textit{Perceptrons}", True),
            (1986, r"Rumelhart, Hinton \\ \& Williams: backprop", False),
            (1989, r"LeCun: \\ reading zip codes", True),
            (2006, r"Hinton et al.: \\ deep belief nets", False),
            (2012, r"AlexNet wins \\ ImageNet", True),
        ]
        marks = []
        for yr, txt, up in events:
            x = year_x(yr)
            stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=HIST, stroke_width=2)
            dot = Dot([x, y0, 0], radius=0.07, color=HIST)
            yl = label(rf"{yr}", font_size=24, color=HIST)
            t = label(txt, font_size=20, color=WHITE)
            words_ = VGroup(yl, t).arrange(DOWN, buff=0.06) if up else VGroup(yl, t).arrange(DOWN, buff=0.06)
            words_.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
            keep_in_frame(words_, margin=0.15)
            marks.append(VGroup(stem, dot, words_))
        head = label(r"How we got here", font_size=36).to_edge(UP, buff=0.35)
        tag = note(r"winters: \ approximate, \ schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 1943, a neurophysiologist and a young logician wrote down the first artificial neuron: a unit that "
            "adds up its inputs and fires if the total is big enough. <bookmark mark='a'/> Fifteen years later, Frank "
            "Rosenblatt built one that learned from examples, and the New York Times reported the Navy's hope that it "
            "would one day walk and talk. <bookmark mark='b'/> In 1969 a book proved what a single layer of such units cannot do, and for a "
            "decade few worked on them. <bookmark mark='c'/> In 1986 backpropagation trained the hidden "
            "layers in between, <bookmark mark='d'/> and networks learned to read handwritten zip codes. "
            "<bookmark mark='e'/> But by the late nineties they were out of fashion again. <bookmark mark='f'/> In "
            "2006 a way to train deep ones was found, and in 2012 a deep network won the ImageNet competition by a "
            "wide margin. The field has not looked back."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(marks[1], shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(marks[2], shift=UP * 0.2), FadeIn(winters[0]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(marks[3], shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(marks[4], shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(winters[1]))
            vo.wait_until("f")
            self.play(FadeIn(marks[5], shift=DOWN * 0.2))
            self.play(FadeIn(marks[6], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spiral(self):
        s = load("spiral")
        X, y, keep = np.asarray(s["X"]), np.asarray(s["y"]), [int(k) for k in s["keep"]]
        cv = np.asarray(s["curve"])
        S = 6.4  # the picture's side
        span = 6.8  # data units across it (-3.4 .. 3.4)
        c = np.array([-3.0, -0.2, 0])

        def P(p):
            return c + np.array([p[0] * S / span, p[1] * S / span, 0])

        dots = VGroup(*[Dot(P(p), radius=0.035, color=CLS_A if v == 0 else CLS_B) for p, v in zip(X, y)])
        imgs = [region_image(s[f"prob{k}"], s[f"regions{k}"], s["xs"], S, S).move_to(c) for k in keep]
        frame_ = Square(S, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
        sv = Integer(0, font_size=32, color=C.BITS)
        sl = VGroup(label(r"training step", font_size=26, color=GREY_A), sv).arrange(RIGHT, buff=0.15)
        sl.move_to([0, 2.9, 0]).align_to([0.7, 0, 0], LEFT)
        nreg = Integer(s[f"nreg{keep[0]}"], font_size=32, color=WHITE)
        nl = VGroup(nreg, label(r"flat pieces", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.15)
        nl.next_to(sl, DOWN, buff=0.25).align_to(sl, LEFT)
        net = label(r"$2 \to 32 \to 32 \to 32 \to 2$, \ ReLU", font_size=24, color=WHITE).next_to(nl, DOWN, buff=0.3)
        net.align_to(sl, LEFT)
        note_ = label(r"each piece: \ the network is \\ exactly a linear function there", font_size=22, color=GREY_A)
        note_.next_to(net, DOWN, buff=0.25).align_to(sl, LEFT)
        # the learning curve, scrubbed with the picture
        g = axes([0, keep[-1]], [0.4, 1.0], x_length=4.6, y_length=2.0, xlabel=r"step",
                 ylabel=r"points on the right side", xticks=[0, keep[-1]], yticks=[0.5, 1.0],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.75, -2.15, 0], font_size=18)

        def acc_line():
            t = sv.get_value()
            n_ = max(2, int(np.searchsorted(cv[:, 0], t, side="right")))
            pts = [g.ax.c2p(a_, float(np.clip(b_, 0.4, 1.0))) for a_, b_ in cv[:n_, [0, 2]]]
            return VMobject(color=C.BITS, stroke_width=3).set_points_as_corners(pts)

        live = always_redraw(acc_line)
        marker = always_redraw(lambda: glow_dot(g.ax.c2p(sv.get_value(), float(np.clip(np.interp(
            sv.get_value(), cv[:, 0], cv[:, 2]), 0.4, 1.0))), color=C.BITS, radius=0.06))
        acc = float(cv[-1, 2])
        tag = note(r"computed: \ trained on this computer").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is what a network does, in one picture. Two spirals, wound around each other. No straight line can "
            "separate them. <bookmark mark='a'/> Here's a small neural network, three layers of thirty-two simple "
            "units, before any training. The thin lines cut the plane into the pieces on which the network is "
            "exactly linear. <bookmark mark='b'/> Now train it."
        ) as vo:
            self.play(Create(frame_), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]), FadeIn(sl), FadeIn(nl), FadeIn(net), FadeIn(note_), FadeIn(tag))
            self.bring_to_front(dots)
            vo.wait_until("b")
            self.play(FadeIn(g))
        verdict = (f"until {100 * acc:.0f} percent of the points are on the right side."
                   if acc > 0.97 else f"and {100 * acc:.0f} percent of the points end up on the right side.")
        with self.voiceover(
            "The pieces swing around, and the boundary between the colours bends to follow the spirals, " + verdict +
            " <bookmark mark='a'/> A network is just this: many flat pieces, glued together, placed by gradient "
            "descent. This part is about why that works, who found it out, and what it takes to make it work."
        ) as vo:
            cur = imgs[0]
            self.add(live, marker)
            prev = 0
            for k, img in zip(keep[1:], imgs[1:]):
                self.play(FadeOut(cur), FadeIn(img), ChangeDecimalToValue(sv, k), ChangeDecimalToValue(nreg, s[f"nreg{k}"]),
                          run_time=0.5 + 0.9 * min((k - prev) / 500, 1.0))
                self.bring_to_front(dots)
                cur, prev = img, k
            marker.clear_updaters()
            live.clear_updaters()
            vo.wait_until("a")
            self.play(Indicate(cur, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Networks", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"the first neurons, \ the perceptron and its convergence proof, \ and what one layer cannot do",
            r"backpropagation, \ derived, \ and its history",
            r"what networks can represent: \ universal approximation, \ Barron's rate, \ what depth adds",
            r"why deep networks were hard to train: \ initialization, \ the edge of chaos, \ residual streams, \ "
            r"normalization",
            r"the modern block: \ GELU, \ SwiGLU, \ pre-norm, \ RMSNorm; \ and Kolmogorov--Arnold networks",
            r"the first neural language model, \ on the scoreboard",
        ], font_size=25).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 9 of AI, Built, in the second act: learning from data. <bookmark mark='a'/> In it: the first neurons, the perceptron, and the proof that it learns; "
            "backpropagation, derived; what networks can represent, with one layer and with many; why deep networks "
            "were so hard to train, and the fixes, from initialization to the residual stream and normalization; the "
            "block inside today's language models; and the first neural language model, on our scoreboard."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
