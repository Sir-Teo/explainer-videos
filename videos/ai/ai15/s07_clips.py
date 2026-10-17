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
        jl = label(r"one sample of the whole clip", font_size=22, color=JOINT).next_to(jr, UP, buff=0.15).align_to(jr, LEFT)
        il = label(r"each frame from a different sample", font_size=22, color=INDEP).next_to(ir, UP, buff=0.15).align_to(ir, LEFT)
        want = [LETTERS[k % 26] for k in range(3)]
        asked = VGroup(*[Text(w_, font="DejaVu Sans Mono", font_size=22, color=C.BITS).next_to(r_, LEFT, buff=0.2)
                         for w_, r_ in zip(want, jr)])
        asked2 = VGroup(*[Text(w_, font="DejaVu Sans Mono", font_size=22, color=C.BITS).next_to(r_, LEFT, buff=0.2)
                          for w_, r_ in zip(want, ir)])
        ja, ia, ra = float(c["joint_all_right"]), float(c["indep_all_right"]), float(c["real_all_right"])
        jj, ij, rj = float(c["joint_jerk"]), float(c["indep_jerk"]), float(c["real_jerk"])
        tab = VGroup(
            VGroup(Dot(radius=0.01, fill_opacity=0), label(r"every frame \\ the right letter", font_size=20, color=GREY_A),
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
        jn = label(r"jerkiness: \ how much the letter's centre \\ changes speed, frame to frame", font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.4)
        f = MathTex(r"p(x_1, \ldots, x_T) \;\neq\; \prod_f p(x_f)", font_size=34).to_edge(UP, buff=0.35)
        smoother = jj < ij - 0.05
        with self.voiceover(
            f"We trained a small diffusion transformer on whole clips, all {T} frames denoised together, attention "
            "running across frames as well as within them. <bookmark mark='a'/> Asked for a letter, it draws a whole "
            "clip at once. <bookmark mark='b'/> Now take the same model, but build each clip from frames of different "
            "samples: frame one from one sample, frame two from another, as if each frame were drawn on its own. "
            "<bookmark mark='c'/> Each frame alone looks fine. Together, "
            + (f"the motion falls apart: jerkiness {ij:.2f} pixels against {jj:.2f} for whole clips, and {rj:.2f} for "
               "real ones. " if smoother else
               f"the numbers are close here, {ij:.2f} against {jj:.2f} pixels of jerkiness, but the letter jumps from "
               "place to place. ")
            + "<bookmark mark='d'/> A video is a joint distribution: the frames have to be drawn together, or "
            "conditioned on each other. That's the whole difficulty, and the rest of this part is about it."
        ) as vo:
            self.play(FadeIn(jl), FadeIn(asked))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in jr], lag_ratio=0.25), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(il), FadeIn(asked2), LaggedStart(*[FadeIn(r_) for r_ in ir], lag_ratio=0.25), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(jn))
            vo.wait_until("d")
            self.play(Write(f))
        self.wait(0.3)
        self.clear_scene()
