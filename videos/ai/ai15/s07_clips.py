from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load

JOINT, INDEP = C.INTERVAL, C.SURPRISE


def strip(frames, size, buff=0.05) -> Group:
    return Group(*[gray_image(f_, size) for f_ in frames]).arrange(RIGHT, buff=buff)


class Clips(VoiceoverScene):
    def construct(self):
        self.card()
        self.data()
        self.together()

    def card(self):
        card = chapter_card(7, r"Frames that agree", r"Why not draw a video one picture at a time?", part=15)
        with self.voiceover("Chapter seven. Frames that agree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def data(self):
        c = load("clips")
        ex = np.asarray(c["examples"])
        T = int(c["T"])
        rows = Group(*[strip(e, 1.05) for e in ex[:4]]).arrange(DOWN, buff=0.25).move_to(DOWN * 0.2)
        head = label(rf"our videos: \ a letter bouncing around, \ ${T}$ frames each", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        tl = MathTex(r"\text{time} \rightarrow", font_size=28, color=GREY_B).next_to(rows, DOWN, buff=0.25)
        with self.voiceover(
            "To see what video adds, we need videos we can check. Ours are tiny: a letter from part fourteen's fonts, "
            f"bouncing around a twenty by twenty frame, {T} frames long. <bookmark mark='a'/> A good video model has to "
            "get two things right that a picture model never faces: the letter must stay the same letter, and it "
            "must move smoothly."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.2), FadeIn(tl), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def together(self):
        c = load("clips")
        J, I = np.asarray(c["joint_clips"]), np.asarray(c["indep_clips"])
        T = int(c["T"])
        S = 0.78
        jr = Group(*[strip(e, S, 0.04) for e in J[:3]]).arrange(DOWN, buff=0.12)
        ir = Group(*[strip(e, S, 0.04) for e in I[:3]]).arrange(DOWN, buff=0.12)
        Group(jr, ir).arrange(DOWN, buff=0.9).move_to([-1.6, -0.5, 0])
        jl = label(r"one sample: \ the rest drawn together", font_size=22, color=JOINT).next_to(jr, UP, buff=0.15).align_to(jr, LEFT)
        il = label(r"each later frame from a different sample", font_size=22, color=INDEP).next_to(ir, UP, buff=0.15).align_to(ir, LEFT)
        # the given first frame of every clip, outlined: it is real, not generated
        given = VGroup(*[SurroundingRectangle(r_[0], buff=0.03, color=C.BITS, stroke_width=2.5) for r_ in (*jr, *ir)])
        gl = label(r"outlined: \ the given first frame, \ real", font_size=18, color=C.BITS).next_to(jl, RIGHT, buff=0.4)
        want = [LETTERS[int(k)] for k in np.asarray(c["given_labels"])[:3]]
        asked = VGroup(*[Text(w_, font="DejaVu Sans Mono", font_size=22, color=C.BITS).next_to(r_, LEFT, buff=0.2)
                         for w_, r_ in zip(want, jr)])
        asked2 = VGroup(*[Text(w_, font="DejaVu Sans Mono", font_size=22, color=C.BITS).next_to(r_, LEFT, buff=0.2)
                          for w_, r_ in zip(want, ir)])
        # scored on the generated frames only (the given first frame left out); the real clips on the same frames
        ja, ia, ra = (float(c[f"{k}_frames_right"]) for k in ("joint", "indep", "real"))
        jj, ij, rj = float(c["joint_jerk"]), float(c["indep_jerk"]), float(c["real_jerk"])
        tab = VGroup(
            VGroup(Dot(radius=0.01, fill_opacity=0), label(r"frames showing \\ the right letter", font_size=20, color=GREY_A),
                   label(r"jerkiness, \\ pixels", font_size=20, color=GREY_A)),
            VGroup(label(r"real clips", font_size=20, color=GREY_B), MathTex(rf"{100 * ra:.0f}\%", font_size=28, color=GREY_B),
                   MathTex(rf"{rj:.2f}", font_size=28, color=GREY_B)),
            VGroup(label(r"whole clip", font_size=20, color=JOINT), MathTex(rf"{100 * ja:.0f}\%", font_size=28, color=JOINT),
                   MathTex(rf"{jj:.2f}", font_size=28, color=JOINT)),
            VGroup(label(r"frame by frame", font_size=20, color=INDEP), MathTex(rf"{100 * ia:.0f}\%", font_size=28, color=INDEP),
                   MathTex(rf"{ij:.2f}", font_size=28, color=INDEP)),
        )
        for r_ in tab:
            for k, m_ in enumerate(r_):
                m_.move_to([3.5 + k * 1.55, 0, 0])
        tab.arrange(DOWN, buff=0.35).move_to([5.1, 0.4, 0])
        for k in range(3):
            x = tab[1][k].get_x()
            for r_ in tab:
                r_[k].set_x(x)
        tn = label(rf"frames $2$ to ${T}$ only: \ the given frame left out", font_size=18, color=GREY_B).next_to(tab, UP, buff=0.3)
        jn = label(r"jerkiness: \ how much the letter's centre \\ changes speed, frame to frame", font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.4)
        f = MathTex(r"p(x_2, \ldots, x_T \mid x_1) \;\neq\; \prod_{f \geq 2} p(x_f \mid x_1)", font_size=34).to_edge(UP, buff=0.35)
        smoother = jj < ij - 0.05
        # the letter: does each version keep it about as well as real clips do?
        keeps_j, keeps_i = ja >= ra - 0.15, ia >= ra - 0.15
        if keeps_j and keeps_i:
            letter = (f"Each frame alone looks fine: the judge reads the right letter in {100 * ja:.0f} percent of the "
                      f"drawn frames of whole clips, and {100 * ia:.0f} percent of the mixed ones, against "
                      f"{100 * ra:.0f} for real clips. ")
        elif ja < 0.5 and ia < 0.5:
            letter = (f"Even frame by frame, this small model struggles: the judge reads the right letter in only "
                      f"{100 * ja:.0f} percent of the drawn frames of whole clips, and {100 * ia:.0f} percent of the "
                      f"mixed ones, against {100 * ra:.0f} for real clips. ")
        else:
            letter = (f"The judge reads the right letter in {100 * ja:.0f} percent of the drawn frames of whole clips, "
                      f"and {100 * ia:.0f} percent of the mixed ones, against {100 * ra:.0f} for real clips. ")
        with self.voiceover(
            "We trained a small diffusion transformer to continue a clip. It's given the first frame of a real clip, "
            f"in a font it never saw, and the letter's name, and it denoises the other {T - 1} frames together, "
            "attention running across frames as well as within them. That's image-to-video: how real video models "
            "bring a still picture to life. <bookmark mark='a'/> Here are three of its clips; the outlined frame is "
            "the given one. <bookmark mark='b'/> Now take the same model, but build each clip from frames of "
            "different samples: frame two from one sample, frame three from another, each continuing the same first "
            "frame, as if each frame were drawn on its own. <bookmark mark='c'/> "
            + letter
            + (f"But together, the motion falls apart. Jerkiness, how much the letter's centre changes speed from "
               f"frame to frame, is {ij:.2f} pixels for the mixed clips, against {jj:.2f} for whole clips and "
               f"{rj:.2f} for real ones. The first frame doesn't say which way the letter is heading, so each sample "
               "picks its own direction. " if smoother else
               f"And the motion is no smoother for drawing the frames together: jerkiness, how much the letter's "
               f"centre changes speed from frame to frame, is {jj:.2f} pixels for whole clips and {ij:.2f} for the "
               f"mixed ones, against {rj:.2f} for real clips. ")
            + "<bookmark mark='d'/> A video is a joint distribution: the probability of the whole clip at once, "
            "where each frame depends on the others. The frames have to be drawn together, or conditioned on each "
            "other. That's the whole difficulty, and the rest of this part is about it."
        ) as vo:
            self.play(FadeIn(jl), FadeIn(asked))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in jr], lag_ratio=0.25), run_time=1.5)
            self.play(Create(given[:3]), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(il), FadeIn(asked2), LaggedStart(*[FadeIn(r_) for r_ in ir], lag_ratio=0.25), Create(given[3:]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tn), FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(jn))
            vo.wait_until("d")
            self.play(Write(f))
        self.wait(0.3)
        self.clear_scene()
