from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Two bowed-string phrases. \ One is Monochord's physical model of a string, \ from Part 9. \ "
                           r"The other is a small network, \ given only the first's pitch and loudness. \ Which is the network?", width=10.0)
        with self.voiceover(
            "In 2016 a network wrote sound one sample at a time, sixteen thousand decisions a second. Listen first. Two phrases on a bowed string. One is Monochord's physical model of a string, from "
            "Part 9. The other was made by a small network that was given only the first one's pitch and loudness. Which is "
            "the network?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"model, \ or network?", kind="synthesized", detail=r"Part 9's string; \ a DDSP network", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the first: \ a network driving a synthesizer, \ {d['dist']:.1f} dB from the string by spectrum", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first was the network. It does not write sound sample by sample: it sets the controls of a synthesizer, "
            "forty harmonics and some noise, many times a second, and Chapter 7 builds it. That is one of three ideas this "
            "part follows from noodling to finished songs."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"2016: \ WaveNet writes sound one sample at a time, \ sixteen thousand decisions a second; \ its piano noodles nowhere", WHITE),
            (r"2020: \ Jukebox writes minutes of songs with singing, \ from tokens of compressed audio; \ hours to make a minute", WHITE),
            (r"2023: \ MusicLM and MusicGen turn a sentence into music, \ from tokens of a neural codec", WHITE),
            (r"2024: \ services return a finished song with a singer; \ the major labels sue two of them \ (dated)", WHITE),
            (r"what closed the gap: \ better representations, \ language models over them, \ diffusion, \ and data", TUNE),
        ]
        rows_scene(self, r"from noodling to songs", items,
                   "In 2016 DeepMind's WaveNet wrote sound one sample at a time, sixteen thousand decisions a second. Its speech was "
                   "startling; its piano, learnt from recordings, noodled nowhere. <bookmark mark='c'/> In 2020 OpenAI's Jukebox "
                   "wrote minutes of songs with singing, from tokens of compressed audio, taking hours to make a minute. "
                   "<bookmark mark='d'/> In 2023 MusicLM, from Google, and MusicGen, from Meta, turned a sentence into music. "
                   "<bookmark mark='e'/> By 2024 services returned a finished song with a singer, and the major record labels "
                   "sued two of them. <bookmark mark='f'/> What closed the gap? Better ways to represent sound, language models "
                   "over them, diffusion, and data: whose, is the last chapter's question.", marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"why raw audio is hard, \ and a network that writes one sample at a time",
            r"spectrograms and vocoders: \ sound from a picture of sound",
            r"tokens from a codec, \ and a language model over them",
            r"diffusion: \ drawing by removing noise",
            r"differentiable DSP: \ a network that plays a synthesizer",
            r"cloned voices, \ judging, \ watermarks, \ and whose data",
        ], title=r"The plan", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan, and for each idea Monochord builds the smallest honest version. <bookmark mark='a'/> Why raw "
            "audio is hard, and a network that writes it one sample at a time. <bookmark mark='b'/> Spectrograms and vocoders. "
            "<bookmark mark='c'/> Tokens from a codec, and a language model over them. <bookmark mark='d'/> Diffusion. "
            "<bookmark mark='e'/> A network that plays a synthesizer. <bookmark mark='f'/> And cloned voices, how to judge "
            "generated sound, how to mark it, and whose music it learnt from. The results are reported as they are."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
