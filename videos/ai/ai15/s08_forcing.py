from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import PATCH, gray_image, load

TEACH, FORCE = C.SURPRISE, C.INTERVAL
CLEAN, NOISY = GREY_A, C.TRUE_P


def strip(frames, size, buff=0.03) -> Group:
    return Group(*[gray_image(f_, size) for f_ in frames]).arrange(RIGHT, buff=buff)


class Forcing(VoiceoverScene):
    def construct(self):
        self.card()
        self.recipes()
        self.rollouts()
        self.frontier()

    def card(self):
        card = chapter_card(8, r"Rolling forward", r"How do you make a video longer than you trained on?", lit=(2024, 2025), part=15)
        with self.voiceover("Chapter eight. Rolling forward."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def recipes(self):
        c = load("clips")
        T = int(c["T"])

        def row(levels, color_lo, y, title, tcol):
            g = VGroup()
            for k, t in enumerate(levels):
                sq = Square(0.62, stroke_color=GREY_C, stroke_width=1.5, fill_color=interpolate_color(ManimColor(NOISY), ManimColor(CLEAN), t),
                            fill_opacity=0.25 + 0.6 * t)
                g.add(VGroup(sq, MathTex(f"{t:.1f}" if 0 < t < 1 else f"{int(t)}", font_size=20, color=WHITE).move_to(sq)))
            g.arrange(RIGHT, buff=0.1).move_to([0.9, y, 0])
            tl = label(title, font_size=22, color=tcol).next_to(g, LEFT, buff=0.35)
            return VGroup(g, tl)

        g = np.random.default_rng(5)
        teach = row([1.0] * 5 + [round(float(g.uniform(0.1, 0.9)), 1)] + [0.0] * (T - 6), CLEAN, 1.4, r"teacher forcing", TEACH)
        force = row([round(float(x), 1) for x in g.uniform(0.05, 0.95, T)], CLEAN, -0.6, r"diffusion forcing", FORCE)
        # in teacher forcing, the future frames aren't in the input at all
        for k in range(6, T):
            teach[0][k].set_opacity(0.08)
        fl = label(r"each frame's noise level $t$: \ $1$ clean, \ $0$ pure noise", font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        lt = label(r"the past clean, \ one frame noised, \ learn that frame", font_size=20, color=TEACH).next_to(teach, DOWN, buff=0.15)
        lf = label(r"every frame its own noise level, \ learn them all", font_size=20, color=FORCE).next_to(force, DOWN, buff=0.15)
        eq = MathTex(r"\mathcal{L} = \mathbb{E}\sum_{f} \big\| v_\theta\big(x_1^{t_1}, \ldots, x_T^{t_T}\big)_f - (x_f - \varepsilon_f)\big\|^2",
                     font_size=32, color=FORCE).to_edge(DOWN, buff=0.9)
        el = label(r"with causal attention: \ frame $f$ sees frames $1 \ldots f$", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        cite_ = cite(r"B.~Chen et al., \textit{Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion} (2024)", corner=DR)
        with self.voiceover(
            f"A whole-clip model makes exactly {T} frames. For longer videos, and for worlds you can walk around in, "
            "a model has to write frame after frame, like a language model writes tokens. <bookmark mark='a'/> The "
            "obvious way to train that is teacher forcing: give the model the real past frames, clean, and teach it "
            "to denoise the next one. <bookmark mark='b'/> But at generation time, the past is the model's own work, "
            "slightly wrong, and it was never trained on that. <bookmark mark='c'/> Diffusion forcing, from Boyuan "
            "Chen and colleagues, gives every frame its own noise level during training, so the model learns to "
            "work from a past that's anywhere from clean to pure noise. <bookmark mark='d'/> The loss is plain flow "
            "matching, summed over frames, with attention that only looks back."
        ) as vo:
            self.play(FadeIn(fl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(teach), FadeIn(lt))
            vo.wait_until("b")
            self.play(Indicate(teach[0][:5], color=TEACH))
            vo.wait_until("c")
            self.play(FadeIn(force), FadeIn(lf))
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(el))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rollouts(self):
        c = load("clips")
        T, Lg = int(c["T"]), int(c["long"])
        tr, fr = np.asarray(c["teacher_rollout"]), np.asarray(c["forcing_rollout"])
        S = 0.37
        cols = list(range(0, Lg, 2))  # every other frame, to fit
        rt = Group(*[strip(e[cols], S) for e in tr[:2]]).arrange(DOWN, buff=0.08)
        rf = Group(*[strip(e[cols], S) for e in fr[:2]]).arrange(DOWN, buff=0.08)
        Group(rt, rf).arrange(DOWN, buff=0.75).move_to([0.6, 1.1, 0])
        lt = label(r"teacher forcing", font_size=22, color=TEACH).next_to(rt, LEFT, buff=0.3)
        lf = label(r"diffusion forcing", font_size=22, color=FORCE).next_to(rf, LEFT, buff=0.3)
        edge = (T / 2) * (S + 0.03)
        marks = VGroup(*[DashedLine(r_.get_corner(UL) + RIGHT * edge + UP * 0.1, r_.get_corner(DL) + RIGHT * edge + DOWN * 0.1,
                                    dash_length=0.05, stroke_width=2, color=C.BITS) for r_ in (rt, rf)])
        ml = label(rf"trained on ${T}$ frames", font_size=18, color=C.BITS).next_to(marks[0], UP, buff=0.05)
        # how often the letter is still recognized, frame by frame
        tf, ff = np.asarray(c["teacher_frame_right"], float), np.asarray(c["forcing_frame_right"], float)
        ax = CornerAxes(x_range=[0, Lg, 8], y_range=[0, 1, 0.5], x_length=7.0, y_length=2.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0.6, -2.3, 0])
        xs = np.arange(1, Lg + 1)
        ct = VMobject(color=TEACH, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, tf)])
        cf = VMobject(color=FORCE, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ff)])
        vt = DashedLine(ax.c2p(T, 0), ax.c2p(T, 1), dash_length=0.05, stroke_width=1.5, color=C.BITS)
        yt = VGroup(*[MathTex(rf"{int(100 * y)}\%", font_size=18, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.08) for y in (0, 1)])
        xt = VGroup(*[MathTex(str(x), font_size=18, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.06) for x in (1, T, Lg)])
        yn = label(r"letter still recognized, \ by frame", font_size=18, color=GREY_A).next_to(ax, LEFT, buff=0.6).shift(UP * 0.3)
        early_t, late_t = float(tf[:T].mean()), float(tf[-T:].mean())
        early_f, late_f = float(ff[:T].mean()), float(ff[-T:].mean())
        holds = late_f > late_t + 0.05
        with self.voiceover(
            f"We trained both on {T}-frame clips, with the same network and the same number of steps, then asked "
            f"each for {Lg} frames, one at a time, looking back at most {T - 1}. <bookmark mark='a'/> Teacher "
            f"forcing: in its first {T} frames the judge recognizes the letter {100 * early_t:.0f} percent of the "
            f"time; in the last {T}, {100 * late_t:.0f}. <bookmark mark='b'/> Diffusion forcing: {100 * early_f:.0f} "
            f"percent, then {100 * late_f:.0f}. "
            + ("Small errors feed on themselves when a model has only ever seen a perfect past; training on noisy "
               "pasts makes it robust to its own mistakes." if holds else
               "On clips this simple, both hold up about as well; the difference grows with longer, richer videos, "
               "where small errors have more room to feed on themselves.")
        ) as vo:
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(r_) for r_ in rt], lag_ratio=0.3), Create(marks[0]), FadeIn(ml),
                      Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yn), Create(vt))
            vo.wait_until("a")
            self.play(Create(ct), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lf), LaggedStart(*[FadeIn(r_) for r_ in rf], lag_ratio=0.3), Create(marks[1]))
            self.play(Create(cf), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        rows = VGroup(
            VGroup(label(r"Self Forcing \ (2025)", font_size=24, color=FORCE),
                   label(r"train on the model's own rollouts, \\ judged as whole videos", font_size=20, color=GREY_A)),
            VGroup(label(r"world models \ (Genie 3, 2025)", font_size=24, color=PATCH),
                   label(r"every frame also conditioned on an action: \\ a world you can walk around in, \ in real time", font_size=20,
                         color=GREY_A)),
            VGroup(label(r"one model, \ two jobs", font_size=24, color=C.TRUE_P),
                   label(r"the same transformer predicts text tokens \\ and denoises image patches \ (Transfusion, BAGEL)",
                         font_size=20, color=GREY_A)),
        )
        for r_ in rows:
            r_.arrange(RIGHT, buff=0.6, aligned_edge=UP)
            r_[1].move_to([1.4, r_[1].get_y(), 0], aligned_edge=LEFT)
            r_[0].move_to([-6.2, r_[0].get_y(), 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0, 0])
        for r_ in rows:
            r_[0].set_x(-6.2 + r_[0].width / 2)
            r_[1].set_x(0.4 + r_[1].width / 2)
        note_ = note(r"as published; \ not reproduced here").to_corner(DR, buff=0.3)
        cite_ = cite(r"X.~Huang et al., \textit{Self Forcing} (2025); \ Google DeepMind, \textit{Genie 3} (2025); \ C.~Zhou et al., "
                     r"\textit{Transfusion} (2024)", corner=UL)
        with self.voiceover(
            "This is where video generation is heading. <bookmark mark='a'/> Self Forcing, in 2025, trains the "
            "model on its own rollouts, videos it generates itself, frame after frame, scoring whole generated "
            "videos, to close the gap between training and use "
            "entirely. <bookmark mark='b'/> Condition each frame on an action as well, and you have a world model: "
            "DeepMind's Genie 3 generates a world you can move through, frame by frame, in real time. "
            "<bookmark mark='c'/> And some models now do text and pictures in one transformer, predicting tokens "
            "for one and denoising patches for the other."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(note_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()
