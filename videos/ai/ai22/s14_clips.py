from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (LAT_C, LETTERS, PART, PATCH, VID_C, VID_NAME, fmt_int, glyph_sheet, load, mean_band,
                                   spread_bars, take_away)

JOINT_C, INDEP_C = VID_C["clip"], C.SURPRISE


def strip(frames, size=0.62, gap=0.06):
    return glyph_sheet(np.asarray(frames), 1, len(frames), size=size, gap=gap)


class Clips(VoiceoverScene):
    def construct(self):
        self.card()
        self.intro()
        self.training()
        self.agree()

    def card(self):
        card = chapter_card(13, r"Frames that agree", r"Why denoise a whole clip at once?", part=PART)
        with self.voiceover("Chapter thirteen. Frames that agree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def intro(self):
        d = load("clips")
        ex, rx = np.asarray(d["examples"]), np.asarray(d["rec_examples"])
        T = int(d["T"])
        r1 = strip(ex[0]).move_to([0.6, 2.3, 0])
        r2 = strip(rx[0]).next_to(r1, DOWN, buff=0.2)
        l1 = label(r"a real clip \ (held-out font)", font_size=18, color=GREY_A).next_to(r1, LEFT, buff=0.3)
        l2 = label(r"each frame rebuilt from \\ $5 \times 5 \times 4 = 100$ numbers", font_size=18, color=LAT_C).next_to(r2, LEFT, buff=0.3)
        toks = VGroup(*[RoundedRectangle(width=0.62, height=0.42, corner_radius=0.06, stroke_color=LAT_C, stroke_width=2,
                                         fill_color=LAT_C, fill_opacity=0.15) for _ in range(T)]).arrange(RIGHT, buff=0.06)
        toks.move_to([0.6, -0.4, 0])
        tl = label(r"one token per frame: \ its $100$ latent numbers", font_size=18, color=LAT_C).next_to(toks, DOWN, buff=0.12)
        bl = label(r"a transformer over the frames \ (adaLN-Zero from each frame's noise level)", font_size=18,
                   color=GREY_A)
        blk = RoundedRectangle(width=max(toks.width, bl.width) + 0.5, height=0.8, corner_radius=0.12, stroke_color=GREY_B,
                               stroke_width=2)
        blk.next_to(toks, UP, buff=0.15)
        bl.move_to(blk)
        given = SurroundingRectangle(toks[0], color=WHITE, buff=0.05, stroke_width=2.5)
        gl = label(r"given: \ the first frame", font_size=18, color=WHITE).next_to(given, DOWN, buff=0.55).shift(LEFT * 0.4)
        stats = label(rf"rebuild error ${float(d['ae_rmse']):.3f}$; \ the judge reads the letter in "
                      rf"${100 * float(d['real_right']):.0f}\%$ of real frames, \ ${100 * float(d['rec_right']):.0f}\%$ of "
                      r"rebuilt ones", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now let's make video ourselves. The clips are a letter moving one pixel a frame and bouncing off the "
            "walls. <bookmark mark='a'/> As real video models do, we work in an autoencoder's latent space: each "
            "frame squeezed to a hundred numbers. <bookmark mark='b'/> A small transformer sees one token per frame, "
            "and each frame's noise level reaches it through adaLN-Zero, as in chapter 6. <bookmark mark='c'/> The "
            "task: given the first frame, from a font the model never saw, draw the next seven. The first model "
            "denoises the whole clip at once: every frame at the same noise level, every frame attending to every "
            "other. That's full-sequence diffusion, the way Sora works."
        ) as vo:
            self.play(FadeIn(r1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(r2), FadeIn(l2), FadeIn(stats))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in toks], lag_ratio=0.1), FadeIn(tl), FadeIn(blk), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(given), FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("clips")
        modes = ["clip", "teacher", "forcing"]
        cv = {m: np.asarray(d[f"{m}_curve"]) for m in modes}  # (seeds, points, [step, loss])
        st = cv["clip"][0, :, 0]
        top = float(max(np.percentile(cv[m][:, :, 1], 98) for m in modes)) * 1.1
        ax = axes([0, st[-1]], [0, top], x_length=6.4, y_length=3.4, xlabel=r"training step \ ($64$ clips each)",
                  ylabel=r"flow-matching loss \ (each model on its own frames)", xticks=[0, st[-1]],
                  yticks=[0, round(top / 2, 2)], center=[-2.4, 0.0, 0], font_size=18, xfmt=lambda x: fmt_int(x))
        lines = VGroup(*[mean_band(ax.ax, st, cv[m][:, :, 1], VID_C[m]) for m in modes])
        leg = legend([(VID_C[m], VID_NAME[m]) for m in modes], font_size=20).move_to([4.6, 0.6, 0])
        card = pause_card(r"Drawn together, \ or frame by frame from the same model: \ which clips keep one letter, "
                          r"moving one way?", width=4.6, font_size=22).move_to([4.7, -1.5, 0])
        hd = note(rf"three models of ${fmt_int(d['params'])}$ weights, \ three seeds each \ (bands: \ min to max)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We trained three models of this size, three seeds each: the whole-clip model, and two that write frame "
            "by frame, which the next chapter needs. <bookmark mark='a'/> Here they are learning. Their losses aren't "
            "comparable with each other, since each is asked something different, but all three settle. "
            "<bookmark mark='b'/> Now, pause and predict. Take the whole-clip model, and draw a clip's frames either "
            "together, or each from a separate run of the same model. Which clips keep one letter, moving one way?"
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(hd))
            vo.wait_until("a")
            self.play(*[FadeIn(l_[0]) for l_ in lines], *[Create(l_[1]) for l_ in lines], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def agree(self):
        d = load("clips")
        J, I_ = np.asarray(d["joint_clips"]), np.asarray(d["indep_clips"])
        labs = [int(x) for x in d["given_labels"]]
        rows = Group()
        for k in range(3):
            rows.add(Group(strip(J[k], size=0.56), strip(I_[k], size=0.56)).arrange(DOWN, buff=0.08))
        rows.arrange(DOWN, buff=0.3).move_to([-2.6, -0.1, 0])
        tags = VGroup(*[VGroup(label(r"together", font_size=16, color=JOINT_C).next_to(r_[0], LEFT, buff=0.2),
                               label(r"separately", font_size=16, color=INDEP_C).next_to(r_[1], LEFT, buff=0.2)) for r_ in rows])
        hd = label(r"the first frame is given; \ the other $7$ drawn", font_size=20, color=GREY_A).next_to(rows, UP, buff=0.25)
        jr, ir = np.asarray(d["joint_all_right"], float), np.asarray(d["indep_all_right"], float)
        jj, ij = np.asarray(d["joint_jerk"], float), np.asarray(d["indep_jerk"], float)
        b1 = spread_bars([[jr, ir]], [JOINT_C, INDEP_C], None, height=2.0, bar_w=0.6, gap=0.25, vmax=1.0,
                         fmt=lambda v: rf"{100 * v:.0f}\%", font_size=18).move_to([3.3, 1.2, 0])
        b2 = spread_bars([[jj, ij]], [JOINT_C, INDEP_C], None, height=2.0, bar_w=0.6, gap=0.25,
                         fmt=lambda v: f"{v:.2f}", font_size=18).move_to([5.6, 1.2, 0])
        t1 = label(r"every frame \\ the right letter", font_size=16, color=GREY_A).next_to(b1, DOWN, buff=0.15)
        t2 = label(r"wobble: \ jumps in \\ the letter's path (px)", font_size=16, color=GREY_A).next_to(b2, DOWN, buff=0.15)
        leg = legend([(JOINT_C, r"drawn together"), (INDEP_C, r"from separate samples")], font_size=18).move_to([4.4, -1.6, 0])
        hdn = note(rf"$64$ clips, \ three seeds; \ real clips' wobble: \ ${float(d['real_jerk']):.2f}$ px").to_edge(DOWN, buff=0.3)
        if jj.mean() < ij.mean() and jr.mean() >= ir.mean():
            verdict = (f"Drawn together, the frames agree: {100 * jr.mean():.0f} percent of clips keep the right letter "
                       f"in every frame, against {100 * ir.mean():.0f}, and the letter's path wobbles {jj.mean():.2f} "
                       f"pixels a frame, against {ij.mean():.2f} when each frame is drawn on its own.")
        elif jj.mean() < ij.mean():
            verdict = (f"Drawn together, the motion is steadier: the letter's path wobbles {jj.mean():.2f} pixels a "
                       f"frame, against {ij.mean():.2f} when each frame is drawn on its own; the letter itself survives "
                       f"in {100 * jr.mean():.0f} percent of clips against {100 * ir.mean():.0f}.")
        else:
            verdict = (f"Surprisingly, drawing the frames together doesn't steady the motion here: {jj.mean():.2f} "
                       f"pixels of wobble against {ij.mean():.2f}.")
        if jj.mean() < ij.mean():
            close = "Denoising the whole clip at once makes the frames agree."
        else:
            close = "At this size, denoising the whole clip at once doesn't buy agreement."
        tk = take_away(r"one noise level, \ full attention: \ frames that agree, \ but a clip of fixed length")
        with self.voiceover(
            "Here's the catch with one frame: it doesn't say which way the letter is moving. The model has to "
            "choose, and every frame has to make the same choice. <bookmark mark='a'/> In each pair, the top row is "
            "a clip drawn together. The bottom row takes each frame from a different sample of the same model, as if "
            "the frames had been drawn one by one, independently. <bookmark mark='b'/> " + verdict
            + " <bookmark mark='c'/> " + close + " And the clip's length is fixed when the model is trained."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(hdn))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_), FadeIn(t_)) for r_, t_ in zip(rows, tags)], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(t_[0], color=JOINT_C) for t_ in tags], run_time=1.0)
            self.play(*[Indicate(t_[1], color=INDEP_C) for t_ in tags], run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(b1.base), FadeIn(b2.base), FadeIn(b1.bars), FadeIn(b2.bars), FadeIn(t1), FadeIn(t2), FadeIn(leg))
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
