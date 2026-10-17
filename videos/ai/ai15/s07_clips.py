from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load
from videos.ai.ai15.deep import centers

JOINT, INDEP = C.INTERVAL, C.SURPRISE


def strip(frames, size, buff=0.05) -> Group:
    return Group(*[gray_image(f_, size) for f_ in frames]).arrange(RIGHT, buff=buff)


def centre_paths(clips, names, colors, box=1.15) -> VGroup:
    """Where the letter's centre is in each frame of a clip, frame by frame, one box per clip: a smooth clip traces an
    even line, a jerky one zigzags. The first dot (the given frame) is outlined."""
    g = VGroup()
    cs = [centers(cl) for cl in clips]  # each (T, 2): row, column, in pixels
    win = max(float(np.ptp(c, 0).max()) for c in cs) + 2.0  # one zoom for all three, so their sizes compare
    for c, nm, col in zip(cs, names, colors):
        sq = Square(box, stroke_color=GREY_C, stroke_width=1.2)
        mid = (c.min(0) + c.max(0)) / 2
        pts = [sq.get_center() + RIGHT * box * (x - mid[1]) / win + DOWN * box * (y - mid[0]) / win for y, x in c]
        path = VMobject(color=col, stroke_width=2).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p_, radius=0.045, color=col) for p_ in pts])
        dots[0].set_stroke(C.BITS, width=2)
        g.add(VGroup(sq, path, dots, label(nm, font_size=16, color=col).next_to(sq, DOWN, buff=0.08)))
    return g.arrange(RIGHT, buff=0.35, aligned_edge=UP)


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
        Group(jr, ir).arrange(DOWN, buff=0.9).move_to([-1.6, -0.62, 0])
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
        tab.arrange(DOWN, buff=0.35).move_to([4.85, 0.3, 0])
        for k in range(3):
            x = tab[1][k].get_x()
            for r_ in tab:
                r_[k].set_x(x)
        tn = label(rf"frames $2$ to ${T}$ only: \ the given frame left out", font_size=18, color=GREY_B).next_to(tab, UP, buff=0.3)
        # jerkiness, pictured: the letter's centre in each frame of a real clip, the first whole clip, the first mixed one
        pic = centre_paths([np.asarray(c["examples"])[0], J[0], I[0]], [r"real", r"whole clip", r"frame by frame"],
                           [GREY_B, JOINT, INDEP])
        jn = gloss(r"jerkiness", r"how much the letter's centre \\ changes speed, frame to frame; \\ each dot: \ its centre "
                   r"in one frame, \ zoomed in", pic, width=4.4, color=GREY_A)
        if jn.width > 4.9:  # clear of the clips on the left
            jn.scale_to_fit_width(4.9)
        jn.next_to(tab, DOWN, buff=0.3).set_x(tab.get_x())
        if jn.get_left()[0] < 1.95:
            jn.shift(RIGHT * (1.95 - jn.get_left()[0]))
        keep_in_frame(jn)
        f = MathTex(r"p(x_2, \ldots, x_T \mid x_1) \;\neq\; \prod_{f \geq 2} p(x_f \mid x_1)", font_size=32).to_edge(UP, buff=0.2)
        smoother = jj < ij - 0.05
        # the letter: does each version keep it about as well as real clips do?
        keeps_j, keeps_i = ja >= ra - 0.15, ia >= ra - 0.15
        if keeps_j and keeps_i:
            letter = (f"Each frame alone looks fine: the judge, our letter-reading classifier, reads the right letter "
                      f"in {100 * ja:.0f} percent of the drawn frames of whole clips, and {100 * ia:.0f} percent of the "
                      f"mixed ones, against {100 * ra:.0f} for real clips. ")
        elif ja < 0.5 and ia < 0.5:
            letter = (f"Even frame by frame, this small model struggles: the judge, our letter-reading classifier, reads "
                      f"the right letter in only {100 * ja:.0f} percent of the drawn frames of whole clips, and "
                      f"{100 * ia:.0f} percent of the mixed ones, against {100 * ra:.0f} for real clips. ")
        else:
            letter = (f"The judge, our letter-reading classifier, reads the right letter in {100 * ja:.0f} percent of the "
                      f"drawn frames of whole clips, and {100 * ia:.0f} percent of the mixed ones, against "
                      f"{100 * ra:.0f} for real clips. ")
        with self.voiceover(
            "We trained a small diffusion transformer, with a little convolution at each end, to continue a clip. "
            "It's given the first frame of a real clip, in a font it never saw, and the letter's name, "
            f"<bookmark mark='g'/> and it denoises the other {T - 1} frames together, attention running across frames as well as within them. "
            "That's image-to-video: how real video models bring a still picture to life. <bookmark mark='a'/> Here are three of its clips; the outlined frame is "
            "the given one. <bookmark mark='b'/> Now take the same model, but build each clip from frames of "
            "different samples: frame two from one sample, frame three from another, each continuing the same first "
            "frame, as if each frame were drawn on its own. <bookmark mark='c'/> "
            + letter
            + (f"But together, the motion falls apart. <bookmark mark='j'/> Jerkiness, how much the letter's centre changes speed from "
               f"frame to frame, is {ij:.2f} pixels for the mixed clips, against {jj:.2f} for whole clips and "
               f"{rj:.2f} for real ones. The first frame doesn't say which way the letter is heading, so each sample "
               "picks its own direction. " if smoother else
               f"And the motion is no smoother for drawing the frames together. <bookmark mark='j'/> Jerkiness, how much the letter's "
               f"centre changes speed from frame to frame, is {jj:.2f} pixels for whole clips and {ij:.2f} for the "
               f"mixed ones, against {rj:.2f} for real clips. ")
            + "<bookmark mark='d'/> A video is a joint distribution: the probability of the whole clip at once, "
            "where each frame depends on the others. The frames have to be drawn together, or conditioned on each "
            "other. That's the whole difficulty, and the rest of this part is about it."
        ) as vo:
            # the given first frames from the start; the generated frames as the narration reaches them
            self.play(FadeIn(jl), FadeIn(asked), LaggedStart(*[FadeIn(r_[0]) for r_ in jr], lag_ratio=0.2))
            self.play(Create(given[:3]), FadeIn(gl))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.1) for k in range(1, T) for f_ in (r_[k] for r_ in jr)],
                                  lag_ratio=0.04), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(r_[1:], color=JOINT, scale_factor=1.03) for r_ in jr])
            vo.wait_until("b")
            self.play(FadeIn(il), FadeIn(asked2), LaggedStart(*[FadeIn(r_) for r_ in ir], lag_ratio=0.25), Create(given[3:]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tn), FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("j")
            jp = jn[1][2]
            self.play(FadeIn(jn[0]), FadeIn(jn[1][:2]), *[FadeIn(VGroup(b_[0], b_[3])) for b_ in jp])
            self.play(*[AnimationGroup(Create(b_[1]), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in b_[2]], lag_ratio=0.3))
                        for b_ in jp], run_time=2.0)
            vo.wait_until("d")
            self.play(Write(f))
        self.wait(0.3)
        self.clear_scene()
