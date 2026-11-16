from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Ica(SoundScene):
    def construct(self):
        chapter(self, 3, r"Independent components", r"Can a machine separate two sources without knowing what they are?")
        self.idea()
        self.picture_()
        self.session()
        self.kurtosis()
        self.heard()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"two microphones, \ two sources, \ each microphone a different mix: \ $\mathbf{x} = A\,\mathbf{s}$", WHITE),
            (r"if the sources are independent, \ find the unmixing $W$ that makes the outputs as independent as possible", WHITE),
            (r"the central limit theorem: \ a mix of independent signals is more Gaussian than either; \ so un-mix toward non-Gaussian", WHITE),
            (r"FastICA \ (Hyvärinen, \ 1999): \ whiten, \ then rotate until each output is as non-Gaussian as it can be", WHITE),
            (r"no model of the sources at all: \ `blind' source separation", TUNE),
        ]
        rows_scene(self, r"blind separation", items,
                   "With two channels there is a purely statistical trick. <bookmark mark='b'/> Two microphones and two sources, each microphone hearing a different mix. <bookmark mark='c'/> If the sources are independent, look for the un-mixing that makes the outputs as independent as possible. <bookmark mark='d'/> Under identifiable instantaneous mixing and independence assumptions, non-Gaussian contrasts can help recover sources; the central limit theorem motivates this, without making every two-source sum more Gaussian in every metric. <bookmark mark='e'/> Aapo Hyvärinen's FastICA whitens the data, then rotates it until each output is as non-Gaussian as it can be. <bookmark mark='f'/> No source templates, but strong independence and mixing assumptions: blind source separation.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def picture_(self):
        rng = np.random.default_rng(1)
        n = 400
        s = np.c_[rng.laplace(size=n), rng.uniform(-1.7, 1.7, n)]
        A = np.array([[0.9, 0.35], [0.4, 0.85]])
        x = s @ A.T
        def scatter(P, col, center):
            P = P / np.abs(P).max() * 1.4
            return VGroup(*[Dot([center[0] + p[0], center[1] + p[1], 0], radius=0.02, color=col) for p in P])
        a = scatter(s, GREY_B, (-4.0, -0.3))
        b = scatter(x, EAR, (0.0, -0.3))
        c = scatter(s, TUNE, (4.0, -0.3))
        la = label(r"two sources", font_size=17, color=GREY_B).next_to(a, UP, buff=0.3)
        lb = label(r"two microphones: \ mixed", font_size=17, color=EAR).next_to(b, UP, buff=0.3)
        lc = label(r"un-mixed by ICA", font_size=17, color=TUNE).next_to(c, UP, buff=0.3)
        head = label(r"what ICA sees", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what it sees, sample by sample. <bookmark mark='a'/> Two independent sources: a scatter aligned with the axes. <bookmark mark='b'/> Mixed, the scatter is sheared and rotated. <bookmark mark='c'/> ICA finds the transformation that squares it up again; it cannot know the sources' order or loudness, but it can recover their shapes under those assumptions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(c), FadeIn(lc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ica")
        c = clip("ica.two")
        boxes = choice_boxes([r"a dry mix", r"the same in a room"], width=3.4, height=0.9, buff=1.0, size=20).move_to(UP * 0.5)
        res = VGroup(label(rf"dry: \ the voice recovered, \ correlation {d['dry']['vocals']:.4f}", font_size=18, color=TUNE),
                     label(rf"in a room: \ {d['room']['vocals']:.2f}: \ each source now reaches each microphone smeared in time, \ and one un-mixing matrix cannot undo that", font_size=17, color=EAR)).arrange(DOWN, buff=0.3).next_to(boxes, DOWN, buff=0.6)
        head = label(r"ICA, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the voice as ICA recovers it from a dry two-channel mix of voice and piano, then from the same mix played in a room."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"dry, \ then a room", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["dry"], st["room"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["room"], c.duration, buff=0.08)
        with self.voiceover(
            "Dry, it is essentially perfect. In this simulated room the instantaneous method performs poorly: each source reaches each microphone through "
            "echoes, a convolution, and a single un-mixing matrix cannot undo that. Convolutive ICA works frequency by "
            "frequency, and must then decide which piece belongs to which source."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def session(self):
        d = load("icascatter")
        M = np.array(d["mixed"])[:900]
        U = np.array(d["unmixed"])[:900]
        def scatter(P, col, center, r=1.5):
            return VGroup(*[Dot([center[0] + r * p[0], center[1] + r * p[1], 0], radius=0.018, color=col, fill_opacity=0.7) for p in P])
        a = scatter(M, EAR, (-3.0, -0.4))
        b = scatter(U, TUNE, (3.0, -0.4))
        axes_ = VGroup(*[VGroup(Line([c - 1.7, -0.4, 0], [c + 1.7, -0.4, 0], color=GREY_D, stroke_width=1), Line([c, -2.1, 0], [c, 1.3, 0], color=GREY_D, stroke_width=1)) for c in (-3.0, 3.0)])
        la = label(r"the two microphones, \ sample against sample", font_size=17, color=EAR).next_to(a, UP, buff=0.35)
        lb = label(r"ICA's two outputs: \ voice across, \ piano and guitar up", font_size=17, color=TUNE).next_to(b, UP, buff=0.35)
        head = label(r"the session's voice and band, \ as a cloud", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now real music: the session's voice and its piano and guitar, mixed into two channels. <bookmark mark='a'/> Each "
            "dot is one sample, the left microphone across and the right one up: a slanted, star-shaped cloud, because music "
            "is mostly quiet with occasional loud moments. <bookmark mark='b'/> ICA's outputs turn the star square to the axes: "
            "where one source is loud, the other is usually near zero, so its arms lie along the axes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes_))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), run_time=1.2)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kurtosis(self):
        d = load("icascatter")
        ang = np.array(d["angles"])
        k = np.array(d["kurtosis"])
        ax = frame_axes(width=8.0, height=3.0, xlo=0, xhi=180, ylo=0, yhi=max(k) * 1.15, center=DOWN * 0.6 + LEFT * 1.2)
        cv = curve(ang, k, ax.to, color=TUNE, width=3)
        i = int(np.argmax(k))
        top = Dot(ax.to(ang[i], k[i]), radius=0.08, color=TUNE)
        xl = label(r"direction in the whitened cloud \ (degrees)", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"excess kurtosis: \ 0 for a Gaussian", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        ks, km = d["kurt_sources"], d["kurt_mixes"]
        side = VGroup(label(r"excess kurtosis", font_size=17, color=GREY_A),
                      label(rf"the voice: \ {ks['vocals']:.2f}", font_size=17, color=TUNE),
                      label(rf"piano and guitar: \ {ks['other']:.2f}", font_size=17, color=TUNE),
                      label(rf"the microphones: \ {km[0]:.2f} \ and \ {km[1]:.2f}", font_size=17, color=EAR),
                      label(rf"Gaussian noise: \ {d['kurt_gauss']:.2f}", font_size=17, color=GREY_B)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        head = label(r"climbing away from the Gaussian", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why does this work? Measure how far a signal is from Gaussian by its excess kurtosis: nought for Gaussian noise, "
            "large for a signal that is mostly quiet with loud peaks. <bookmark mark='a'/> The voice scores "
            f"{say(ks['vocals'], 2)}, the piano and guitar {say(ks['other'], 2)}; the two microphones, being mixtures, score less, "
            f"{say(km[0], 2)} and {say(km[1], 2)}: the central limit theorem at work. <bookmark mark='b'/> After whitening, try "
            "every direction through the cloud. <bookmark mark='c'/> The most non-Gaussian direction is the voice itself; that "
            "is the direction FastICA climbs to."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in side], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(cv), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(top, scale=1.5))
        self.wait(0.6)
        self.clear_scene()
