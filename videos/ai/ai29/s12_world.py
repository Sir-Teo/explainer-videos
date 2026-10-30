from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, HIST, MODEL, PART, load, node_box


def gray(a, size, color=None) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    tint = np.array(ManimColor(color or WHITE).to_rgb())
    rgb = np.concatenate([a[..., None] * tint[None, None], np.ones(a.shape + (1,))], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


class World(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.model()
        self.learning()
        self.imagine()

    def card(self):
        card = chapter_card(11, r"World models", r"Can an agent imagine what happens next?", part=PART)
        with self.voiceover("Chapter eleven. World models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        V = node_box(r"V: \ a VAE squeezes \ each frame", C.TRUE_P, 22, height=1.0)
        M = node_box(r"M: \ a recurrent network \ predicts what comes next", MODEL, 22, height=1.0)
        Cc = node_box(r"C: \ a tiny linear \ controller", AGENT, 22, height=1.0)
        row = VGroup(V, M, Cc).arrange(RIGHT, buff=0.7).move_to([0, 1.7, 0])
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B) for a, b in zip(row, row[1:])])
        cards = VGroup(
            history_card(1990, r"Dyna \ (Sutton); \ Schmidhuber's recurrent world models", r"learn a model of the "
                         r"world, \ and practise in it between real steps", width=4.2, color=HIST, font_size=18),
            history_card(2018, r"World Models \ (Ha \& Schmidhuber)", r"car racing from pixels, \ score $906$: \ the first "
                         r"to pass $900$; \ and a VizDoom agent trained entirely inside its own dream", width=4.2,
                         color=HIST, font_size=18),
            history_card(2019, r"MuZero \ (Part 26)", r"a model of only what planning needs: \ value, \ policy, \ "
                         r"reward, \ never the pixels", width=4.2, color=HIST, font_size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "An agent that can predict the results of its actions can try things out in its head before doing "
            "them. <bookmark mark='a'/> The idea is old. Around 1990 Richard Sutton's Dyna learned a model of the "
            "world and practised in it between real steps, and Jürgen Schmidhuber built recurrent networks that "
            "modelled their world. <bookmark mark='b'/> In 2018 David Ha and Schmidhuber made it vivid. A "
            "variational autoencoder squeezes each frame of a game, <bookmark mark='c'/> a recurrent network "
            "learns to predict the next squeezed frame, <bookmark mark='d'/> and a tiny controller acts on both. It "
            "was the first to score over nine hundred at a car-racing game from pixels, and in VizDoom it was "
            "trained entirely inside its own dream. <bookmark mark='e'/> MuZero, in Part 26, went the other way: a "
            "model of only what planning needs, never the pixels."
        ) as vo:
            self.play(FadeIn(row[0]), FadeIn(row[1]), FadeIn(row[2]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15), Indicate(V, color=C.TRUE_P))
            vo.wait_until("c")
            self.play(GrowArrow(arr[0]), Indicate(M, color=MODEL))
            vo.wait_until("d")
            self.play(GrowArrow(arr[1]), Indicate(Cc, color=AGENT))
            vo.wait_until("e")
            self.play(FadeIn(cards[2], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        w = load("world")
        first = np.asarray(w["first"])
        S, Z = int(w["S"]), int(w["Z"])
        f1, f2 = gray(first[0], 1.4).move_to([-5.2, 0.6, 0]), gray(first[1], 1.4).move_to([-3.6, 0.6, 0])
        enc = Polygon([-1.0, 0.8, 0], [0.8, 0.3, 0], [0.8, -0.3, 0], [-1.0, -0.8, 0], stroke_color=C.TRUE_P, stroke_width=2.5,
                      fill_color=C.TRUE_P, fill_opacity=0.12).move_to([-1.6, 0.6, 0])
        zc = VGroup(*[Square(0.2, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.EMBED, fill_opacity=0.7) for _ in range(Z)])
        zc.arrange(DOWN, buff=0).move_to([0.2, 0.6, 0])
        dyn = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.12, stroke_color=C.BITS, stroke_width=2.5).move_to([2.2, 0.6, 0])
        dl = label(r"what comes \\ next?", font_size=22, color=C.BITS).move_to(dyn)
        zn = zc.copy().move_to([4.0, 0.6, 0])
        dec = Polygon([-0.8, 0.3, 0], [1.0, 0.8, 0], [1.0, -0.8, 0], [-0.8, -0.3, 0], stroke_color=C.TRUE_P, stroke_width=2.5,
                      fill_color=C.TRUE_P, fill_opacity=0.12).move_to([5.4, 0.6, 0])
        arrows = VGroup(Arrow(f2.get_right(), enc.get_left(), buff=0.1, color=GREY_B), Arrow(enc.get_right(), zc.get_left(), buff=0.1, color=GREY_B),
                        Arrow(zc.get_right(), dyn.get_left(), buff=0.1, color=GREY_B), Arrow(dyn.get_right(), zn.get_left(), buff=0.1, color=GREY_B),
                        Arrow(zn.get_right(), dec.get_left(), buff=0.1, color=GREY_B))
        labs = VGroup(label(rf"two frames, \ ${S}\times{S}$", font_size=20, color=GREY_A).next_to(Group(f1, f2), DOWN, buff=0.15),
                      label(rf"${Z}$ numbers", font_size=20, color=C.EMBED).next_to(zc, DOWN, buff=0.15),
                      label(r"the next frame's \\ numbers", font_size=20, color=C.EMBED).next_to(zn, DOWN, buff=0.15))
        foot = label(r"a small world model, \ trained here on bouncing balls", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        cite_ = cite(r"D.~Ha \& J.~Schmidhuber, \textit{World Models} (2018); \ D.~Hafner et al., \textit{Dreamer} (2020--2025)", corner=DR)
        with self.voiceover(
            "To plan, an agent needs to predict what its actions will do. A world model learns that from experience. "
            "<bookmark mark='a'/> Ours watches a ball bouncing in a box. It squeezes each frame into eight numbers, "
            "learns how those numbers change from one frame to the next, and can turn numbers back into a picture."
        ) as vo:
            self.play(FadeIn(f1), FadeIn(f2), FadeIn(labs[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.25), FadeIn(enc), FadeIn(zc), FadeIn(dyn),
                      FadeIn(dl), FadeIn(zn), FadeIn(dec), FadeIn(labs[1:]), run_time=3.0)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def imagine(self):
        w = load("world")
        real, imag = np.asarray(w["real"]), np.asarray(w["imag"])
        pe = np.asarray(w["pos_err"])
        S = 1.25
        r_img = gray(real[0], S, C.TRUE_P).move_to([-4.6, 1.3, 0])
        i_img = gray(imag[0], S, C.BITS).move_to([-4.6, -0.6, 0])
        rl = label(r"real", font_size=24, color=C.TRUE_P).next_to(r_img, LEFT, buff=0.2)
        il = label(r"imagined", font_size=24, color=C.BITS).next_to(i_img, LEFT, buff=0.2)
        overlay = Group(gray(real[0], 2.6, C.TRUE_P), gray(imag[0], 2.6, C.BITS).set_opacity(0.6)).move_to([-1.2, 0.35, 0])
        ol = label(r"both, overlaid", font_size=22, color=GREY_A).next_to(overlay, UP, buff=0.12)
        ax = Axes(x_range=[0, len(pe), 10], y_range=[0, max(4.0, float(pe.max()) * 1.1), 1], x_length=4.4, y_length=3.0,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([4.2, 0.0, 0])
        c = VMobject(color=C.SURPRISE, stroke_width=3.5).set_points_as_corners([ax.c2p(i + 1, v) for i, v in enumerate(pe)])
        xn = label(r"steps imagined ahead", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yn = label(r"how far off the ball is \ (pixels)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        counter = VGroup(label(r"step", font_size=24, color=GREY_A), Integer(1, font_size=28, color=C.BITS)).arrange(RIGHT, buff=0.15)
        counter.next_to(overlay, DOWN, buff=0.3)
        tail = label(r"Genie, \ Dreamer, \ video world models: \\ the same idea, \ at scale", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now let it imagine. Give it two real frames and let it run on its own predictions, step after step, "
            "<bookmark mark='a'/> while the real ball keeps going. For a while, imagination and reality move "
            f"together: one step ahead it's {pe[0]:.1f} pixels off. <bookmark mark='b'/> Then small errors compound, "
            f"like the long tasks of the last chapter: {pe[19]:.1f} pixels off after twenty steps. <bookmark mark='c'/> "
            "Agents like Dreamer learn by practising inside such imagined worlds, and Genie generates whole playable "
            "worlds from video."
        ) as vo:
            self.play(FadeIn(r_img), FadeIn(i_img), FadeIn(rl), FadeIn(il), FadeIn(overlay), FadeIn(ol), FadeIn(counter),
                      Create(ax), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            for t in range(1, len(real)):
                new_o = Group(gray(real[t], 2.6, C.TRUE_P), gray(imag[t], 2.6, C.BITS).set_opacity(0.6)).move_to(overlay)
                self.play(Transform(r_img, gray(real[t], S, C.TRUE_P).move_to(r_img)),
                          Transform(i_img, gray(imag[t], S, C.BITS).move_to(i_img)),
                          Transform(overlay, new_o), counter[1].animate.set_value(t + 1), run_time=0.25, rate_func=linear)
            self.play(Create(c), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How a world model learns: its imagined continuation of one clip, at checkpoints during training."""
        w = load("world")
        checks = [int(c) for c in w["checks"]]
        dreams = np.asarray(w["dreams"])
        real = np.asarray(w["probe_real"])
        n = dreams.shape[1]
        S = 0.72
        rows = Group()
        for k in range(len(checks)):
            rows.add(Group(*[gray(f_, S, C.INTERVAL) for f_ in dreams[k]]).arrange(RIGHT, buff=0.04))
        rr = Group(*[gray(f_, S, GREY_A) for f_ in real]).arrange(RIGHT, buff=0.04)
        Group(rr, *rows).arrange(DOWN, buff=0.12).move_to([0.8, -0.3, 0])
        ll = VGroup(label(r"what really happens", font_size=18, color=GREY_A).next_to(rr, LEFT, buff=0.25),
                    *[MathTex(rf"\text{{step }}{c:,}".replace(",", "{,}"), font_size=22, color=C.INTERVAL).next_to(r_, LEFT, buff=0.25)
                      for c, r_ in zip(checks, rows)])
        head = label(rf"from the same two frames, \ the next ${n}$ imagined \ (each feeding the next)", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.4)
        def centre(f):
            f = np.clip(np.asarray(f, float), 0, None)
            ys_, xs_ = np.indices(f.shape)
            return np.array([(f * ys_).sum(), (f * xs_).sum()]) / max(f.sum(), 1e-9)

        miss = float(np.linalg.norm(centre(dreams[-1, -1]) - centre(real[-1])))  # the last checkpoint's last frame
        peak = [float(np.asarray(dd).max()) for dd in dreams]  # the brightest pixel of each checkpoint's dream
        held = [sum(1 for f_, r_ in zip(dd, real) if np.asarray(f_).max() > 0.35
                    and np.linalg.norm(centre(f_) - centre(r_)) < 2.0) for dd in dreams]
        early = (f"After {checks[1]} steps its brightest pixel is only {peak[1]:.2f}: it has learned the safest guess, "
                 "a nearly empty frame, the average of all frames." if peak[1] < 0.35 else
                 f"After {checks[1]} steps a faint ball appears, and it keeps it near the real one for {held[1]} of the "
                 f"{n} frames.")
        mid = (f"By step {checks[2]} it keeps the ball within two pixels of the real one for {held[2]} of the {n} "
               "frames, then loses it, as each guess builds on the last one's blur." if held[2] < n else
               f"By step {checks[2]} it already carries the ball through all {n} frames.")
        with self.voiceover(
            "How does a world model learn to dream? Here it is at checkpoints during training, each time given the "
            "same two opening frames and left to imagine the next twelve, every frame built on its own last guess. "
            f"<bookmark mark='a'/> Untrained, its brightest pixel is {peak[0]:.2f}: a haze, nothing like a ball. "
            f"<bookmark mark='b'/> {early} <bookmark mark='c'/> {mid} <bookmark mark='d'/> The final model "
            f"carries the ball through {held[-1]} of the {n} frames, though small errors still add up: after twelve "
            f"imagined frames, its ball is {miss:.1f} pixels from the real one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rr), FadeIn(ll[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ll[1]))
            for mk, k in (("b", 1), ("c", 2)):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=DOWN * 0.1), FadeIn(ll[k + 1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_, shift=DOWN * 0.1), FadeIn(l_)) for r_, l_ in zip(rows[3:], ll[4:])],
                                  lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
