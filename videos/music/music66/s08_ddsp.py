from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class Ddsp(SoundScene):
    def construct(self):
        chapter(self, 7, r"Differentiable DSP", r"Can a network learn to play a synthesizer?")
        self.idea()
        self.training()
        self.heard()
        self.inside()
        self.vibrato()
        self.transfer()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"DDSP \ (Engel, \ Hantrakul, \ Gu and Roberts, \ 2020): \ keep the synthesizer, \ learn only its controls", WHITE),
            (r"the synthesizer: \ 40 harmonics of the pitch, \ each with its own level, \ plus noise in 16 bands \ (Parts 3 and 51)", WHITE),
            (r"the network: \ from pitch and loudness, \ 250 times a second, \ to the harmonics' levels and the noise's", WHITE),
            (r"the loss: \ compare the synthesized and the real spectra at five resolutions; \ the synthesizer is differentiable, \ so the error flows back", WHITE),
            (r"tiny, \ fast, \ and controllable: \ any pitch curve and loudness curve can drive it", TUNE),
        ]
        rows_scene(self, r"the fourth idea", items,
                   "The fourth idea keeps the synthesizer. <bookmark mark='b'/> DDSP, from Jesse Engel and colleagues at Google in "
                   "2020, learns only the synthesizer's controls. <bookmark mark='c'/> The synthesizer is the additive one of Parts 3 and "
                   "51: forty harmonics of the pitch, each with its own level, plus noise in sixteen bands. <bookmark mark='d'/> A "
                   "network turns pitch and loudness, two hundred and fifty times a second, into those levels. "
                   "<bookmark mark='e'/> It learns by comparing the synthesized and the real spectra at five resolutions; because "
                   "every step of the synthesizer is differentiable, the error flows back to the network. <bookmark mark='f'/> The "
                   "result is tiny, fast and controllable: any pitch curve and loudness curve can drive it.", marks="bcdef")

    # ------------------------------------------------------------------
    def training(self):
        d = load("ddsp")
        L = np.array(d["losses"])
        ax = frame_axes(width=7.5, height=3.0, xlo=0, xhi=len(L) - 1, ylo=0, yhi=L.max() * 1.05, center=DOWN * 0.5 + LEFT * 1.0)
        cv = curve(np.arange(len(L)), L, ax.to, color=TUNE, width=3)
        xl = label(r"training", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"spectral loss, \ five resolutions", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c = load("corpus")
        side = VGroup(label(rf"{d['params']:,} weights", font_size=16, color=WHITE),
                      label(rf"{c['string_seconds']:.0f} s of the bowed-string model's notes", font_size=16, color=WHITE),
                      label(r"one-second chunks, \ chosen at random", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"learning a string", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Monochord's DDSP has {say(d['params'])} weights, and learns from {say(round(c['string_seconds']))} seconds of the "
            "bowed-string model's notes, a second at a time. <bookmark mark='a'/> The spectral loss falls steeply, then levels: "
            "most of a string's sound is a harmonic profile that depends on pitch and loudness, and that is just what the "
            "network can express."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.6)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ddsp")
        c = clip("ddsp.two")
        boxes = choice_boxes([r"the string model", r"DDSP, \ from its pitch and loudness"], width=4.2, height=0.9, buff=0.8, size=18).move_to(UP * 0.6)
        res = label(rf"{d['dist']:.1f} dB from the string by spectrum \ (white noise of the same loudness: \ {d['dist_noise']:.0f} dB)", font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"a phrase it never heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the Tune's opening on the string model, which the network never heard, then the network's resynthesis from that phrase's pitch and loudness alone."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"model, \ then DDSP", kind="synthesized", detail=r"Part 9's string; \ DDSP", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["model"], st["ddsp"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["ddsp"], c.duration, buff=0.08)
        with self.voiceover(
            f"By spectrum the resynthesis is {say(d['dist'], 1)} decibels from the original, where noise of the same loudness "
            f"would be {say(round(d['dist_noise']))}. What it misses, if you listen for it, is in the attacks and in the bow's "
            "noise, which a few noise bands describe only roughly."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        d = load("ddsp")
        A = np.array(d["amps"]).T
        pic = heat_image(A[::-1], A.max() - 3, A.max(), width=10.0, height=2.6).move_to(DOWN * 0.1)
        f0 = np.array(d["f0"])
        lab = label(r"the network's controls over the phrase: \ the level of each of 40 harmonics \ (harmonic 1 at the bottom), \ log scale", font_size=16, color=GREY_A).next_to(pic, DOWN, buff=0.25)
        head = label(r"what the network sets", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what the network does over that phrase: the level of each of its forty harmonics, moment by moment. "
            "<bookmark mark='a'/> Each note starts bright, as the bow catches the string, and darkens as it settles: the "
            "brightness falls as the loudness grows, a correlation of minus nought point seven. Across pitches the profile "
            "changes little. These are the controls of a synthesizer, and they can be read, edited and driven by anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pic))
            vo.wait_until("a")
            self.play(FadeIn(lab))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transfer(self):
        items = [
            (r"timbre transfer: \ take a singer's pitch and loudness, \ drive the string with them", WHITE),
            (r"the result keeps the singer's phrasing, \ vibrato and dynamics, \ in the string's sound \ (the Variation, \ at the end)", WHITE),
            (r"real DDSP models learn violins, \ flutes and voices from minutes of recordings", WHITE),
            (r"the same controls drive voice conversion: \ the next chapter's subject, \ and its problem", TUNE),
        ]
        rows_scene(self, r"timbre transfer", items,
                   "Drive it with anything, and it becomes an effect. <bookmark mark='b'/> Take a singer's pitch and loudness and "
                   "drive the string with them: timbre transfer. <bookmark mark='c'/> The result keeps the singer's phrasing, "
                   "vibrato and dynamics in the string's sound, as this part's Variation will let you hear. <bookmark mark='d'/> "
                   "Real DDSP models learn violins, flutes and voices from minutes of recordings. <bookmark mark='e'/> And the same "
                   "idea, controls taken from one performer and given to another's sound, is voice conversion: the next chapter's "
                   "subject, and its problem.", marks="bcde")

    # ------------------------------------------------------------------
    def vibrato(self):
        d = load("vibrato")
        c = clip("vibrato.two")
        boxes = choice_boxes([r"a swell with a semitone-wide vibrato", r"a glide over an octave"], width=4.6, height=0.9, buff=0.6, size=18).move_to(UP * 0.6)
        note = label(r"neither was in the training notes: \ each was a fixed pitch at a fixed bow", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"controls it never saw", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Because the network only sets a synthesizer's controls, it can be driven by curves it never saw. Hear it with a slow swell and a vibrato a semitone wide, then with a glide over an octave."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"vibrato, \ then a glide", kind="synthesized", detail=r"the DDSP string", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["vibrato"], st["glide"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["glide"], c.duration, buff=0.08)
        with self.voiceover("Neither gesture was in its training notes, each of which held one pitch at one bow. The synthesizer's harmonics follow the pitch exactly, which is why such models generalize where sample-by-sample ones do not."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
