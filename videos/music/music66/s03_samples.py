from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class Samples(SoundScene):
    def construct(self):
        chapter(self, 2, r"One sample at a time", r"What does a network write when it writes every sample?")
        self.wavenet()
        self.ours()
        self.heard()
        self.lessons()

    # ------------------------------------------------------------------
    def wavenet(self):
        items = [
            (r"WaveNet \ (van den Oord et al., \ 2016): \ predict each sample from all the samples before it", WHITE),
            (r"dilated convolutions: \ layers that look 1, \ 2, \ 4, \ 8 \dots \ samples back, \ so a stack of 30 sees thousands", WHITE),
            (r"conditioned on what to say: \ text, \ or a speaker; \ unconditioned on music, \ it noodles", WHITE),
            (r"generation is serial: \ every sample waits for the last; \ the first versions took minutes for a second", WHITE),
            (r"its lasting use was as a vocoder: \ turning a spectrogram into sound \ (Chapter 3)", TUNE),
        ]
        rows_scene(self, r"WaveNet", items,
                   "WaveNet, from Aäron van den Oord and colleagues in 2016, predicts each sample from all the samples before it. "
                   "<bookmark mark='b'/> Its trick for looking far back cheaply is the dilated convolution: layers that look one, "
                   "two, four, eight samples back, so that a stack of thirty sees thousands. <bookmark mark='c'/> Told what to say, "
                   "a text or a speaker, it spoke astonishingly well; left to itself on music, it noodled. <bookmark mark='d'/> "
                   "And generation is serial: every sample waits for the one before, and the first versions took minutes for a "
                   "second of sound. <bookmark mark='e'/> Its lasting use was as a vocoder, turning a spectrogram into sound, as "
                   "the next chapter explains.", marks="bcde")

    # ------------------------------------------------------------------
    def ours(self):
        d = load("ar")
        cv_ = np.array(d["bits_train_curve"])
        ax = frame_axes(width=7.0, height=2.8, xlo=0, xhi=len(cv_) - 1, ylo=0, yhi=8.5, center=DOWN * 0.6 + LEFT * 1.4)
        cv = curve(np.arange(len(cv_)), cv_, ax.to, color=TUNE, width=3)
        ref = DashedLine(ax.to(0, 8), ax.to(len(cv_) - 1, 8), color=GREY_B, stroke_width=1.5)
        test = DashedLine(ax.to(0, d["bits_test"]), ax.to(len(cv_) - 1, d["bits_test"]), color=EAR, stroke_width=2)
        xl = label(r"training", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"bits per sample \ (8: \ a blind guess among 256)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(rf"reads the last {d['context']} samples", font_size=16, color=WHITE),
                      label(r"two hidden layers; \ 256 outputs", font_size=16, color=WHITE),
                      label(r"on the training notes \ (gold)", font_size=16, color=TUNE),
                      label(rf"on a phrase it never heard: \ {d['bits_test']:.1f} bits \ (red)", font_size=16, color=EAR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"Monochord's sample-by-sample network", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Monochord's version is far smaller: a network that reads the last {say(d['context'])} samples and outputs a "
            "probability for each of the 256 levels of the next, trained on a minute of the bowed-string model's notes. "
            "<bookmark mark='a'/> On its training notes it learns quickly to beat a blind guess of eight bits a sample. "
            f"<bookmark mark='b'/> On a phrase it never heard, {say(d['bits_test'], 1)} bits"
            + (", worse than the blind guess: it has learnt its training notes' waveforms by heart, not how a string behaves. "
               if d["bits_test"] > 8 else ". ")
            + "And two hundred and fifty-six samples is a sixtieth of a second, a few cycles of the lowest notes, nothing like "
            "a phrase."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(ref), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(test), FadeIn(side[3]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ar")
        c = clip("ar.two")
        boxes = choice_boxes([r"half a second of the string", r"the same, \ then the network's next second"], width=4.6, height=0.9, buff=0.6, size=18).move_to(UP * 0.6)
        res = label(rf"16,000 decisions for one second; \ {d['seconds_to_sample_1s']:.0f} s of computing on this machine", font_size=19, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"one sample at a time, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear half a second of a bowed phrase, then the same half second with the network's next second after it."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"prime, \ then continued", kind="synthesized", detail=r"Part 9's string; \ a sample-level network", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["prime"], st["continued"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["continued"], c.duration, buff=0.08)
        with self.voiceover(
            "After the string, it writes whatever a sixtieth of a second of memory, learnt by heart, allows. Sixteen thousand "
            f"decisions took about {say(round(d['seconds_to_sample_1s']))} seconds of computing here. Bigger networks, trained "
            "for weeks on far more audio, made such continuations sound like instruments; they still could not plan a phrase."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lessons(self):
        items = [
            (r"samples carry fine detail the ear needs, \ and almost none of the structure the music has", WHITE),
            (r"so: \ split the job \ \ \ structure in a compact representation, \ detail filled in by another model", WHITE),
            (r"the rest of this part is that split: \ spectrograms, \ codec tokens, \ latents, \ synthesizer controls", TUNE),
        ]
        rows_scene(self, r"the lesson", items,
                   "The lesson was clear by 2017. <bookmark mark='b'/> Samples carry the fine detail the ear needs, and almost "
                   "none of the structure the music has. <bookmark mark='c'/> So split the job: plan the structure in a compact "
                   "representation, and let another model fill in the detail. <bookmark mark='d'/> The rest of this part is that "
                   "split, four ways: spectrograms, codec tokens, latents, and the controls of a synthesizer.", marks="bcd")
