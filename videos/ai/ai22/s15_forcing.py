from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, PART, PATCH, VID_C, VID_NAME, glyph_sheet, load, mean_band

MODES = ["teacher", "forcing", "forcing_noisy", "clip"]


def noise_rows() -> VGroup:
    """Training noise levels per frame: teacher forcing (clean context, one noisy frame) against diffusion forcing
    (every frame its own level). Bars: how noisy each frame is (schematic draws)."""
    rng = np.random.default_rng(5)
    out = VGroup()
    for kind, levels, col in (("teacher", [0, 0, 0, 0, 0.7, 1, 1, 1], VID_C["teacher"]),
                              ("forcing", [0] + list(rng.uniform(0, 1, 7)), VID_C["forcing"])):
        frames = VGroup()
        for k, s in enumerate(levels):
            box = Square(0.5, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_D, fill_opacity=0.15 + 0.6 * s)
            bar = Rectangle(width=0.12, height=max(0.02, 0.5 * s), stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.next_to(box, RIGHT, buff=0.04).align_to(box, DOWN)
            frames.add(VGroup(box, bar))
        frames.arrange(RIGHT, buff=0.18)
        if kind == "teacher":
            for k in range(5, 8):
                frames[k].set_opacity(0.25)
        nm = label(VID_NAME[kind], font_size=20, color=col).next_to(frames, LEFT, buff=0.3)
        out.add(VGroup(nm, frames))
    out.arrange(DOWN, buff=0.45, aligned_edge=RIGHT)
    return out


class Forcing(VoiceoverScene):
    def construct(self):
        self.card()
        self.forcing()
        self.rollouts()
        self.drift()
        self.realtime()

    def card(self):
        card = chapter_card(14, r"Rolling forward", r"How does a video go on past its training length?", part=PART)
        with self.voiceover("Chapter fourteen. Rolling forward."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forcing(self):
        rows = noise_rows().move_to([0.4, 0.6, 0])
        bl = label(r"bars: \ each frame's noise level in one training example \ (schematic)", font_size=18,
                   color=GREY_A).next_to(rows, DOWN, buff=0.3)
        tf = label(r"earlier frames clean, \ one frame noisy, \ later ones unseen", font_size=18, color=VID_C["teacher"])
        tf.next_to(rows[0], UP, buff=0.15)
        df = label(r"every frame at its own noise level", font_size=18, color=VID_C["forcing"]).next_to(rows[1], DOWN, buff=0.95)
        cite_ = cite(r"B.~Chen, D.~Mart\'i Mons\'o, Y.~Du, M.~Simchowitz, R.~Tedrake \& V.~Sitzmann, \textit{Diffusion "
                     r"Forcing} (2024)", corner=DL)
        with self.voiceover(
            "To go on past a fixed length, write the video frame by frame, like text: each frame from the ones "
            "before, with causal attention. <bookmark mark='a'/> The obvious way to train it is teacher forcing: "
            "give the model clean earlier frames, and teach it to denoise the next one. <bookmark mark='b'/> In July "
            "2024 Boyuan Chen, Vincent Sitzmann and colleagues proposed diffusion forcing: give every frame its own "
            "random noise level, so the model learns to work from any mix of clean and noisy context. At generation "
            "time it can then treat its own earlier frames as slightly noisy, never quite trusting them."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(tf))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(df), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rollouts(self):
        d = load("clips")
        truth = np.asarray(d["truth"])[0]
        L_, T = int(d["long"]), int(d["T"])
        pick = list(range(1, L_, 3))[:11]  # every third frame
        S = 0.5
        rows = Group(glyph_sheet(truth[pick], 1, len(pick), size=S, gap=0.05))
        names = [label(r"physics", font_size=18, color=GREY_A)]
        for m in MODES:
            rows.add(glyph_sheet(np.asarray(d[f"{m}_clips"])[0][pick], 1, len(pick), size=S, gap=0.05))
            names.append(label(VID_NAME[m], font_size=18, color=VID_C[m]))
        rows.arrange(DOWN, buff=0.15).move_to([1.2, -0.2, 0])
        for n_, r in zip(names, rows):
            n_.next_to(r, LEFT, buff=0.25)
        hd = label(rf"two frames given, \ then ${L_ - 2}$ drawn: \ $4\times$ the {T}-frame training clips \ (every third frame shown)",
                   font_size=20, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "We trained a teacher-forcing model and a diffusion-forcing model, the same size as the clip model, on "
            "the same eight-frame clips, three seeds each. Now give each model two real frames, which fix the "
            f"motion, and ask for {L_ - 2} more: four times the length any of them trained on. <bookmark mark='a'/> "
            "Here are the frames physics says should come, <bookmark mark='b'/> and each model's rollout: teacher "
            "forcing, diffusion forcing taking its own frames as clean, diffusion forcing taking them as slightly "
            "noisy, and the clip model, extended six frames at a time from the last two."
        ) as vo:
            self.play(FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_), FadeIn(n_)) for r_, n_ in zip(rows[1:], names[1:])],
                                  lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drift(self):
        d = load("clips")
        L_, T = int(d["long"]), int(d["T"])
        fr = np.arange(L_)
        keep = fr >= 2
        top = max(float(np.asarray(d[f"{m}_pos"])[:, keep].max()) for m in MODES) * 1.1
        ax = axes([0, L_], [0, top], x_length=5.2, y_length=3.2, xlabel=r"frame",
                  ylabel=r"distance from where physics puts the letter (px)", xticks=[0, T, 2 * T, L_],
                  yticks=[0, round(top / 2, 1)], center=[-3.4, 0.3, 0], font_size=17)
        bx = axes([0, L_], [0, 1], x_length=5.2, y_length=3.2, xlabel=r"frame", ylabel=r"the judge reads the right letter",
                  xticks=[0, T, 2 * T, L_], yticks=[0, 0.5, 1], center=[3.4, 0.3, 0], font_size=17)
        trained = VGroup(DashedLine(ax.ax.c2p(T, 0), ax.ax.c2p(T, top), color=GREY_C, stroke_width=1.5),
                         DashedLine(bx.ax.c2p(T, 0), bx.ax.c2p(T, 1), color=GREY_C, stroke_width=1.5))
        tl = label(r"trained length", font_size=16, color=GREY_C).next_to(trained[0], UP, buff=0.05)
        lines_p = VGroup(*[mean_band(ax.ax, fr[keep], np.asarray(d[f"{m}_pos"])[:, keep], VID_C[m]) for m in MODES])
        lines_r = VGroup(*[mean_band(bx.ax, fr[keep], np.asarray(d[f"{m}_right"])[:, keep], VID_C[m]) for m in MODES])
        leg = legend([(VID_C[m], VID_NAME[m]) for m in MODES], font_size=18).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        if leg.width > 13:
            leg.width = 13
        hd = note(r"median over $64$ clips of held-out fonts; \ bands: \ three seeds, \ min to max").to_edge(UP, buff=0.3)
        late = {m: float(np.asarray(d[f"{m}_pos"])[:, -T:].mean()) for m in MODES}
        early = {m: float(np.asarray(d[f"{m}_pos"])[:, 2:T].mean()) for m in MODES}
        lr = {m: float(np.asarray(d[f"{m}_right"])[:, -T:].mean()) for m in MODES}
        best = min(MODES, key=lambda m: late[m])
        names = {"teacher": "teacher forcing", "forcing": "diffusion forcing", "forcing_noisy":
                 "diffusion forcing with noisy context", "clip": "the clip model"}
        drift_tf = late["teacher"] - early["teacher"]
        if late["teacher"] > max(late["forcing"], late["forcing_noisy"]) + 0.3:
            verdict = (f"Teacher forcing drifts most: within the trained length its letter is {early['teacher']:.1f} "
                       f"pixels from where it should be; over the last eight frames, {late['teacher']:.1f}. Diffusion "
                       f"forcing ends at {late['forcing']:.1f}, and {late['forcing_noisy']:.1f} with noisy context.")
        elif drift_tf > 0.3:
            verdict = (f"Every frame-by-frame model drifts: teacher forcing from {early['teacher']:.1f} pixels off "
                       f"within the trained length to {late['teacher']:.1f} at the end, diffusion forcing to "
                       f"{late['forcing']:.1f}, and {late['forcing_noisy']:.1f} with noisy context.")
        else:
            verdict = (f"Our rollouts hardly drift: teacher forcing stays within {late['teacher']:.1f} pixels of the "
                       f"physics, diffusion forcing within {late['forcing']:.1f}. A bouncing letter is easy to "
                       "continue; the errors that compound in real video are richer.")
        ending = (f"Lowest at the end: {names[best]}, at {late[best]:.1f} pixels, with the right letter "
                  f"{100 * lr[best]:.0f} percent of the time over the last eight frames.")
        why_line = ("The errors compound because each model trained on real frames but now reads its own, slightly "
                    "wrong ones. That mismatch has a name: exposure bias." if drift_tf > 0.3 else
                    "In real video the errors do compound, because a model trained on real frames must read its own, "
                    "slightly wrong ones. That mismatch has a name: exposure bias.")
        with self.voiceover(
            "Measured over sixty-four clips and three seeds: how far the letter is from where physics puts it, frame "
            "by frame, and whether the judge still reads the right letter. <bookmark mark='a'/> " + verdict
            + " <bookmark mark='b'/> " + ending + " <bookmark mark='c'/> " + why_line
        ) as vo:
            self.play(FadeIn(hd), Create(ax), Create(bx), Create(trained), FadeIn(tl), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[FadeIn(l_[0]) for l_ in lines_p], *[Create(l_[1]) for l_ in lines_p], run_time=2.5)
            vo.wait_until("b")
            self.play(*[FadeIn(l_[0]) for l_ in lines_r], *[Create(l_[1]) for l_ in lines_r], run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def realtime(self):
        head = label(r"Training on its own frames, \ and video in real time", font_size=34).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(r"Dec 2024", r"CausVid \ (Yin et al.)", r"a slow two-way teacher distilled into a causal "
                         r"student: \ $4$ steps a frame, \ $9.4$ frames a second", color=HIST, width=4.3, font_size=23),
            history_card(r"Jun 2025", r"Self Forcing \ (Huang, Li, He, Zhou \& Shechtman)", r"train on its own rollouts, "
                         r"\ judge the whole video at once: \ $17$ frames a second, \ $0.45$ s to the first, \ one GPU",
                         color=HIST, width=4.3, font_size=23),
            history_card(r"Aug 2025", r"Genie 3 \ (Google DeepMind)", r"a world you steer as it is drawn, \ in real "
                         r"time: \ Part 29", color=HIST, width=4.3, font_size=23),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        if cards.width > 13.2:
            cards.width = 13.2
        loop = VGroup(node_box_(r"generate frames \ from its own past", VID_C["forcing"]),
                      node_box_(r"score the whole clip \ against a teacher", PATCH))
        loop.arrange(RIGHT, buff=1.4).to_edge(DOWN, buff=0.7)
        arr = VGroup(CurvedArrow(loop[0].get_top() + UP * 0.05, loop[1].get_top() + UP * 0.05, angle=-0.8, color=GREY_B),
                     CurvedArrow(loop[1].get_bottom() + DOWN * 0.05, loop[0].get_bottom() + DOWN * 0.05, angle=-0.8, color=GREY_B))
        with self.voiceover(
            "The cure for exposure bias is to train on what the model will actually see. <bookmark mark='a'/> In "
            "December 2024 CausVid distilled a slow model, whose frames attend both ways, into a causal one that "
            "needs four denoising steps a frame. <bookmark mark='b'/> In June 2025 Xun Huang and colleagues went "
            "further with Self Forcing: during training, the model rolls out a whole clip from its own frames, "
            "<bookmark mark='c'/> and the whole clip is scored at once against a teacher. It generates seventeen "
            "frames a second on one GPU, with the first frame in under half a second: video as fast as it plays. "
            "<bookmark mark='d'/> Make the frames respond to a player's actions, and you have an interactive world "
            "model, like Google DeepMind's Genie 3: that's Part 29."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1), FadeIn(loop[0]))
            vo.wait_until("c")
            self.play(FadeIn(loop[1]), Create(arr))
            vo.wait_until("d")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


def node_box_(text, color, font_size=20):
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.35, corner_radius=0.1, stroke_color=color,
                           stroke_width=2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))
