from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import CLS_A, CLS_B, load, region_image


class Hook(VoiceoverScene):
    def construct(self):
        self.spiral()
        self.plan()

    # ------------------------------------------------------------------
    def spiral(self):
        s = load("spiral")
        X, y, keep = np.asarray(s["X"]), np.asarray(s["y"]), list(s["keep"])
        S = 6.4  # the picture's side
        span = 6.8  # data units across it (-3.4 .. 3.4)
        c = np.array([-2.3, -0.2, 0])

        def P(p):
            return c + np.array([p[0] * S / span, p[1] * S / span, 0])

        dots = VGroup(*[Dot(P(p), radius=0.035, color=CLS_A if v == 0 else CLS_B) for p, v in zip(X, y)])
        imgs = [region_image(s[f"prob{k}"], s[f"regions{k}"], s["xs"], S, S).move_to(c) for k in keep]
        frame_ = Square(S, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
        sv = Integer(0, font_size=34, color=C.BITS)
        sl = VGroup(label(r"training step", font_size=28, color=GREY_A), sv).arrange(RIGHT, buff=0.15)
        sl.move_to([0, 2.2, 0]).align_to([1.5, 0, 0], LEFT)
        nreg = Integer(s[f"nreg{keep[0]}"], font_size=34, color=WHITE)
        nl = VGroup(nreg, label(r"flat pieces", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.15).next_to(sl, DOWN, buff=0.3)
        nl.align_to(sl, LEFT)
        net = label(r"$2 \to 32 \to 32 \to 32 \to 2$, \ ReLU", font_size=26, color=WHITE).next_to(nl, DOWN, buff=0.5)
        net.align_to(sl, LEFT)
        note_ = label(r"each piece: \ the network is \\ exactly a linear function there", font_size=24, color=GREY_A)
        note_.next_to(net, DOWN, buff=0.4).align_to(sl, LEFT)
        acc = float(np.asarray(s["curve"])[-1, 2])
        res = label(rf"${100 * acc:.0f}\%$ of the points on the right side", font_size=26, color=C.BITS)
        res.next_to(note_, DOWN, buff=0.4).align_to(sl, LEFT)
        with self.voiceover(
            "Two spirals, wound around each other. No straight line can separate them, and no classical method in "
            "part six would find this easy. <bookmark mark='a'/> Here's a small neural network, three layers of "
            "thirty-two simple units, before any training. The thin lines cut the plane into the pieces on which "
            "the network is exactly linear. <bookmark mark='b'/> Now train it."
        ) as vo:
            self.play(Create(frame_), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]), FadeIn(sl), FadeIn(nl), FadeIn(net), FadeIn(note_))
            self.bring_to_front(dots)
            vo.wait_until("b")
        with self.voiceover(
            "The pieces swing around, and the boundary between the colours bends to follow the spirals, until "
            "nearly every point is on the right side. <bookmark mark='a'/> A network is just this: many flat pieces, "
            "glued together, placed by gradient descent. This part is about why that works, and what it takes to "
            "make it work."
        ) as vo:
            cur = imgs[0]
            for k, img in zip(keep[1:], imgs[1:]):
                self.play(FadeOut(cur), FadeIn(img), ChangeDecimalToValue(sv, k), ChangeDecimalToValue(nreg, s[f"nreg{k}"]),
                          run_time=1.4)
                self.bring_to_front(dots)
                cur = img
            self.play(FadeIn(res))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 9: \ Networks", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"approximation, \ depth, \ signals, \ residuals, \ a neural language model", font_size=30,
                    color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=9, done=8).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "We'll see why one layer of these units can approximate anything, what depth adds, how to keep signals "
            "alive through fifty layers, and the one trick that lets networks get really deep. <bookmark mark='a'/> "
            "And at the end, the first neural language model takes its place on the scoreboard."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
