from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403


class VLA(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.chunks()

    def card(self):
        card = chapter_card(4, r"Acting in the physical world", r"How does a language model move a robot arm?", part=18)
        with self.voiceover("Chapter four. Acting in the physical world."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pipeline(self):
        cam = VGroup(*[Square(0.3, stroke_color=C.BITS, stroke_width=1.2, fill_color=C.BITS, fill_opacity=0.25) for _ in range(9)])
        cam.arrange_in_grid(rows=3, cols=3, buff=0.04).move_to([-5.2, 1.0, 0])
        cl = label(r"camera images", font_size=20, color=C.BITS).next_to(cam, DOWN, buff=0.12)
        txt = VGroup(*[Square(0.3, stroke_color=C.TRUE_P, stroke_width=1.2, fill_color=C.TRUE_P, fill_opacity=0.25) for _ in range(5)])
        txt.arrange(RIGHT, buff=0.04).move_to([-5.0, -1.0, 0])
        tl = label(r"``fold the towel''", font_size=20, color=C.TRUE_P).next_to(txt, DOWN, buff=0.12)
        vlm = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.2, stroke_color=WHITE, stroke_width=2.5).move_to([-0.8, 0, 0])
        vl = label(r"a vision-language model \\ (pretrained on the web)", font_size=22, color=WHITE).move_to(vlm)
        act = RoundedRectangle(width=2.4, height=1.4, corner_radius=0.2, stroke_color=C.INTERVAL, stroke_width=2.5).move_to([3.0, 0, 0])
        al = label(r"an action expert: \\ flow matching \\ (Part 14)", font_size=22, color=C.INTERVAL).move_to(act)
        arm = VGroup(Line([5.0, -1.2, 0], [5.4, 0.2, 0], color=GREY_A, stroke_width=6), Line([5.4, 0.2, 0], [6.2, 0.6, 0], color=GREY_A,
                                                                                                  stroke_width=6),
                     Dot([5.4, 0.2, 0], radius=0.08, color=GREY_B), Dot([6.2, 0.6, 0], radius=0.1, color=C.INTERVAL))
        arrows = VGroup(Arrow(cam.get_right(), vlm.get_left() + UP * 0.5, buff=0.1, color=GREY_B),
                        Arrow(txt.get_right(), vlm.get_left() + DOWN * 0.5, buff=0.1, color=GREY_B),
                        Arrow(vlm.get_right(), act.get_left(), buff=0.1, color=GREY_B),
                        Arrow(act.get_right(), arm[0].get_start() + UP * 0.6 + LEFT * 0.2, buff=0.1, color=GREY_B))
        cite_ = cite(r"A.~Brohan et al., \textit{RT-2} (2023); \ K.~Black et al., \textit{$\pi_0$} (2024)", corner=DR)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Robots are where agents meet physics. A vision-language-action model starts from a model that already "
            "reads images and text, trained on the web. <bookmark mark='a'/> Give it camera images and an "
            "instruction, and add a way to output motion. RT-2, in 2023, wrote actions as tokens, like words. "
            "<bookmark mark='b'/> Pi-zero, in 2024, added an action expert that generates smooth motions by flow "
            "matching, part fourteen's machinery, now drawing trajectories instead of pictures."
        ) as vo:
            self.play(FadeIn(cam), FadeIn(cl), FadeIn(txt), FadeIn(tl), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), Create(vlm), FadeIn(vl))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[2]), Create(act), FadeIn(al))
            self.play(GrowArrow(arrows[3]), FadeIn(arm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chunks(self):
        ax = Axes(x_range=[0, 50, 10], y_range=[-1.2, 1.2, 1], x_length=10.0, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 2.0)

        def f(t):
            return 0.8 * np.sin(t / 7) * np.cos(t / 13)

        segs = VGroup(*[VMobject(color=C.INTERVAL, stroke_width=4).set_points_smoothly(
            [ax.c2p(t, f(t)) for t in np.linspace(10 * i, 10 * (i + 1), 60)]) for i in range(5)])
        bands = VGroup(*[Rectangle(width=10.0 / 5 * 0.98, height=2.2, stroke_color=GREY_D, stroke_width=1, fill_color=C.INTERVAL,
                                   fill_opacity=0.05).move_to(ax.c2p(5 + 10 * i, 0)) for i in range(5)])
        bl = VGroup(*[label(rf"chunk {i + 1}", font_size=20, color=GREY_B).next_to(b, UP, buff=0.08) for i, b in enumerate(bands)])
        head = label(r"action chunks: \ the model plans a short stretch of motion at once, \\ then looks again", font_size=26)
        head.to_edge(UP, buff=0.3)
        xn = label(r"time $\to$ \ (the elbow's angle)", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        tag = note(r"illustrative trajectory").to_corner(DR, buff=0.3)
        # a two-link arm whose elbow follows the planned trajectory
        tt = ValueTracker(0.0)
        base = np.array([-0.8, -0.2, 0])

        def arm():
            t = tt.get_value()
            a1 = 1.15 + 0.35 * f(t)
            a2 = a1 - 1.1 + 1.1 * f(t)
            p1 = base + 1.5 * np.array([np.cos(a1), np.sin(a1), 0])
            p2 = p1 + 1.3 * np.array([np.cos(a2), np.sin(a2), 0])
            return VGroup(Line(base, p1, color=GREY_A, stroke_width=8), Line(p1, p2, color=GREY_A, stroke_width=7),
                          Dot(base, radius=0.1, color=GREY_B), Dot(p1, radius=0.08, color=C.INTERVAL), Dot(p2, radius=0.11, color=WHITE))

        plinth = Rectangle(width=1.2, height=0.2, stroke_width=0, fill_color=GREY_D, fill_opacity=1).next_to(base, DOWN, buff=0.08)
        live = always_redraw(arm)
        cursor = always_redraw(lambda: Line(ax.c2p(tt.get_value(), -1.2), ax.c2p(tt.get_value(), 1.2), color=WHITE, stroke_width=2))
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), f(tt.get_value())), radius=0.07, color=WHITE))
        look = label(r"look", font_size=24, color=C.BITS).move_to([3.2, 0.6, 0])
        plan = label(r"plan a chunk", font_size=24, color=C.INTERVAL).move_to([3.2, 0.6, 0])
        act = label(r"act", font_size=24, color=WHITE).move_to([3.2, 0.6, 0])

        def chunk(i):
            self.play(FadeIn(look, scale=1.2), bands[i].animate.set_fill(opacity=0.18), run_time=0.3)
            self.play(FadeOut(look), FadeIn(plan), Create(segs[i]), run_time=0.5)
            self.play(FadeOut(plan), FadeIn(act), tt.animate.set_value(10 * (i + 1)), run_time=1.0, rate_func=linear)
            self.play(FadeOut(act), bands[i].animate.set_fill(opacity=0.05), run_time=0.2)

        with self.voiceover(
            "And it doesn't act one tiny step at a time. It plans a chunk of motion, a second or so, then looks at "
            "the world again and plans the next: <bookmark mark='a'/> the belief and the world model of the earlier "
            "chapters, folded into one network that sees, thinks and moves."
        ) as vo:
            still = arm()  # fade in a still copy; the live arm (rebuilt every frame) can't be faded in
            self.play(FadeIn(head), Create(ax), FadeIn(xn), FadeIn(tag), FadeIn(bands), FadeIn(bl), FadeIn(plinth), FadeIn(still))
            self.remove(still)
            self.add(live, cursor, dot)
            for i in range(3):
                chunk(i)
            vo.wait_until("a")
            for i in range(3, 5):
                chunk(i)
        live.clear_updaters()
        cursor.clear_updaters()
        dot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
