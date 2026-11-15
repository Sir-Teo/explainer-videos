from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class Diffusion(SoundScene):
    def construct(self):
        chapter(self, 6, r"Diffusion", r"Can a model draw by removing noise?")
        self.idea()
        self.steps()
        self.heard()
        self.profiles()
        self.latent()

    # ------------------------------------------------------------------
    def idea(self):
        lines = VGroup(
            label(r"forward: \ add a little noise, \ a hundred times, \ until nothing is left but noise", font_size=20, color=WHITE),
            MathTex(r"x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \varepsilon", font_size=38, color=TUNE),
            label(r"learn: \ a network that, \ shown $x_t$ and $t$, \ guesses the noise $\varepsilon$ that was added", font_size=20, color=WHITE),
            label(r"generate: \ start from pure noise and remove the guessed noise, \ step by step, \ back to $t = 0$", font_size=20, color=WHITE),
            label(r"Sohl-Dickstein et al. \ (2015); \ Ho, \ Jain and Abbeel \ (2020); \ the method behind most image generators", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"diffusion", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The third idea draws by removing noise. <bookmark mark='a'/> Take a real example and add a little noise, a hundred "
            "times over, until nothing is left but noise. <bookmark mark='b'/> At every step the example is a known mixture of "
            "the original and noise. <bookmark mark='c'/> Train a network that, shown a noisy example and how noisy it is, "
            "guesses the noise. <bookmark mark='d'/> Then generate: start from pure noise, and remove the guessed noise step by "
            "step back to the beginning. <bookmark mark='e'/> Jascha Sohl-Dickstein and colleagues proposed it in 2015, and "
            "Jonathan Ho and colleagues made it work in 2020; most image generators now run this way."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        d = load("diffusion")
        snaps = d["snapshots"]
        order = ["99", "75", "50", "25", "0"]
        panels = VGroup()
        for i, t in enumerate(order):
            v = np.array(snaps[t])[1]                      # the A4 tone
            ax = frame_axes(width=2.2, height=1.8, xlo=0, xhi=24, ylo=-80, yhi=10, center=[-5.0 + 2.5 * i, -0.4, 0])
            bars = VGroup(*[Line(ax.to(k + 0.5, -80), ax.to(k + 0.5, float(np.clip(v[k], -80, 10))), color=TUNE, stroke_width=3) for k in range(24)])
            panels.add(VGroup(ax, bars, label(rf"step {t}", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.12)))
        note = label(r"the levels of a tone's 24 harmonics \ (dB, \ the strongest at 0), \ as the noise is removed", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"a tone, \ drawn from noise", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's diffusion model draws something small: the profile of a bowed tone, the levels of its twenty-four "
            f"harmonics, given only the pitch. It learnt from {say(d['n_train'])} notes of the bowed-string model. "
            "<bookmark mark='a'/> Here is one profile being drawn, for the A above middle C: at step ninety-nine pure noise, "
            "then less and less, until at step nought a profile that falls away with the harmonics, as a string's does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.4), run_time=3.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("diffusion")
        c = clip("diffusion.six")
        boxes = choice_boxes([r"measured: \ A3, \ A4, \ G5", r"drawn by diffusion: \ A3, \ A4, \ G5"], width=4.6, height=0.9, buff=0.7, size=18).move_to(UP * 0.6)
        near = d["nearest_db"]
        res = label(rf"each drawn profile differs from its nearest training profile by {min(near):.1f} to {max(near):.1f} dB a harmonic: \ new, \ and in range", font_size=17, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"three tones, \ twice", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear steady tones at three pitches, first with profiles measured from the string model, then with profiles the diffusion model drew."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"measured, \ then drawn", kind="synthesized", detail=r"harmonic profiles", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["real0"], st["gen0"] - 0.3, buff=0.06)
            pulse(snd, boxes[1], st["gen0"], c.duration, buff=0.06)
        with self.voiceover(
            "The drawn tones are new, not copies: each differs from its nearest training profile by "
            f"{say(min(near), 1)} to {say(max(near), 1)} decibels a harmonic on average. They are bright or dark as the string's "
            "are at those pitches. A steady profile is not an instrument, but the method that drew it scales."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def latent(self):
        items = [
            (r"for music, \ diffusion runs in a latent space: \ a compressed code of the sound learnt by an autoencoder", WHITE),
            (r"Stable Audio \ (2023, \ 2024): \ latent diffusion conditioned on text and on timing, \ minutes long", WHITE),
            (r"every step refines the whole piece at once: \ no left-to-right commitment, \ unlike a language model", WHITE),
            (r"flow matching \ (2022): \ learn a straight path from noise to data; \ fewer steps", WHITE),
            (r"the diffusion model of Part 66 \ (a profile) \ and of Stable Audio \ (a song) \ differ in size, \ not in kind", TUNE),
        ]
        rows_scene(self, r"diffusion for music", items,
                   "For music, diffusion runs in a latent space, a compressed code of the sound learnt by an autoencoder. "
                   "<bookmark mark='b'/> Stable Audio, from 2023, is latent diffusion conditioned on text and on timing, and makes "
                   "minutes of audio. <bookmark mark='c'/> Every step refines the whole piece at once, with no left-to-right "
                   "commitment, unlike a language model. <bookmark mark='d'/> Flow matching, from 2022, learns a straighter path "
                   "from noise to data, and needs fewer steps. <bookmark mark='e'/> This chapter's model, which draws a profile, "
                   "and Stable Audio, which draws a song, differ in size, not in kind.", marks="bcde")

    # ------------------------------------------------------------------
    def profiles(self):
        d = load("diffusion")
        R, Gn = np.array(d["real"]), np.array(d["generated"])
        names = [r"A3", r"A4", r"G5"]
        panels = VGroup()
        for i in range(3):
            ax = frame_axes(width=3.6, height=2.6, xlo=1, xhi=24, ylo=-80, yhi=5, center=[-4.2 + 4.2 * i, -0.4, 0])
            k = np.arange(1, 25)
            panels.add(VGroup(ax, curve(k, np.clip(R[i], -80, 5), ax.to, color=GREY_B, width=2.5), curve(k, np.clip(Gn[i], -80, 5), ax.to, color=TUNE, width=2.5),
                              label(names[i], font_size=17, color=WHITE).next_to(ax, UP, buff=0.1)))
        key = VGroup(label(r"measured from the string model", font_size=15, color=GREY_B), label(r"drawn by diffusion", font_size=15, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.45)
        xl = label(r"harmonic 1 to 24 across; \ level in dB up", font_size=14, color=GREY_A).next_to(key, UP, buff=0.2)
        head = label(r"the profiles, \ drawn", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the profiles themselves, measured and drawn, at the three pitches. <bookmark mark='a'/> The drawn "
            "ones follow the measured ones' fall with the harmonic number, and their ups and downs, which come from where the "
            "bow touches the string, without copying any one of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.3), run_time=1.8)
        self.wait(0.6)
        self.clear_scene()
