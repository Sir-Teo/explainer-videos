from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Chain(SoundScene):
    def construct(self):
        chapter(self, 1, r"The chain, \ once more", r"What path does a piece of music travel, and which part built each link?")
        self.whole()
        self.acts()
        self.experiment()
        self.measures()

    # ------------------------------------------------------------------
    def whole(self):
        ch = chain(lit=tuple(CHAIN_COLOR), width=11.6, font_size=19, detour=True).move_to(UP * 0.6)
        back = VGroup(
            label(r"and the way back, \ added in Act XI: \ sound $\longrightarrow$ machine $\longrightarrow$ score", font_size=21, color=EAR),
        ).next_to(ch, DOWN, buff=0.7)
        head = label(r"the Chain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every chapter card of this series has carried the same drawing: the Chain, the path a piece of music travels. "
            "<bookmark mark='a'/> A mind makes a score; hands play it on an instrument; the sound crosses the air to an ear, "
            "and so to another mind. <bookmark mark='b'/> From Act Nine on, the detour lit up: a microphone, a mix, a master, "
            "a codec, a stream, a loudspeaker. <bookmark mark='c'/> And Act Eleven added the way back, from sound to a machine "
            "to a score. Every link is now lit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(ch.link[k]) for k, _ in CHAIN], lag_ratio=0.2), FadeIn(ch[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*ch[2:])), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(back))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def acts(self):
        items = [
            (r"Acts I and II, \ Sound and Notes: \ the instrument, \ the air, \ the ear; \ the score", WHITE),
            (r"Acts III to VII: \ voices, \ eras, \ the world's musics, \ the craft: \ what minds put in scores, \ and how hands play them", WHITE),
            (r"Act VIII, \ The Mind: \ the listener at the end of the chain", WHITE),
            (r"Acts IX and X, \ Electric Sound and the Studio: \ microphone, \ mix, \ master, \ codec, \ stream", WHITE),
            (r"Act XI, \ Listening Machines: \ the way back, \ from sound to a score", EAR),
            (r"Act XII: \ how the field knows what it knows, \ and now the whole chain at once", TUNE),
        ]
        rows_scene(self, r"which act built which link", items,
                   "Which act built which link? <bookmark mark='b'/> Acts One and Two built the instrument, the air and the ear, "
                   "and then the score. <bookmark mark='c'/> Acts Three to Seven filled the score and the hands: voices, a "
                   "thousand years of style, the world's other musics, and the craft of orchestrating, composing and performing. "
                   "<bookmark mark='d'/> Act Eight was the listener at the far end. <bookmark mark='e'/> Acts Nine and Ten built the "
                   "studio: microphones, mixing, mastering, codecs. <bookmark mark='f'/> Act Eleven built the way back, machines "
                   "that listen. <bookmark mark='g'/> And this act asked how the field knows what it knows, and now runs the whole "
                   "chain at once.", font_size=22, marks="bcdefg")

    # ------------------------------------------------------------------
    def experiment(self):
        steps = [(r"score", r"the whole Tune, \ 42 notes, \ at 120 beats a minute", 61),
                 (r"performed", r"a tempo that breathes, \ held phrase ends, \ dynamics that swell", 43),
                 (r"instrument", r"the simulated piano: \ hammer, \ stiff strings, \ soundboard", 38),
                 (r"room", r"a reverberant tail of 1.4 seconds", 55),
                 (r"microphone", r"its band, \ 60 Hz to 15 kHz, \ and a noise floor 50 dB down", 54),
                 (r"master", r"a soft limiter", 57),
                 (r"codec", r"the perceptual coder at 128, \ 64, \ 32 and 16 kbit/s", 58),
                 (r"and back", r"onsets and pitch, \ quantized with a drifting tempo, \ a key; \ a fingerprint", 61)]
        rows_ = VGroup()
        for name, what, part in steps:
            rows_.add(VGroup(label(name, font_size=19, color=TUNE), label(what, font_size=17, color=WHITE),
                             label(rf"Part {part}", font_size=16, color=GREY_B)))
        for r in rows_:
            r[0].move_to([-5.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.3, 0, 0], aligned_edge=LEFT)
            r[2].move_to([5.0, 0, 0], aligned_edge=LEFT)
        rows_.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.25)
        for r in rows_:
            r[0].set_x(-5.6 + r[0].width / 2)
            r[1].set_x(-3.3 + r[1].width / 2)
            r[2].set_x(5.0 + r[2].width / 2)
        head = label(r"the experiment: \ one tune, \ every link", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        marks = "abcdefgh"
        with self.voiceover(
            "So here is the experiment, one tune through every link. <bookmark mark='a'/> The score: the whole Tune, forty-two "
            "notes at a hundred and twenty beats a minute. <bookmark mark='b'/> A performance, as Part 43 modelled one: a tempo "
            "that breathes, phrase ends held, dynamics that swell to the middle of each phrase. <bookmark mark='c'/> The "
            "instrument: Part 38's simulated piano. <bookmark mark='d'/> A room, with a reverberant tail of one point four "
            "seconds. <bookmark mark='e'/> A microphone's band and its noise. <bookmark mark='f'/> A master's limiter. "
            "<bookmark mark='g'/> Part 58's coder, at four bit rates. <bookmark mark='h'/> And then the way back: onsets and "
            "pitch, a score with a drifting tempo, a key, a fingerprint. Each link is a model a part built and checked; none "
            "is new here."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip(marks, rows_):
                vo.wait_until(m)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        items = [
            (r"each stage is measured by what it changes: \ timing, \ dynamics, \ space, \ noise, \ peaks, \ bandwidth", WHITE),
            (r"what comes back is scored against what was written: \ notes found, \ wrong keys, \ wrong note values", WHITE),
            (r"wrong keys are counted by edit distance: \ the fewest insertions, \ deletions and substitutions \ that turn one line into the other", WHITE),
            (r"the transcriber's settings were chosen on four other tunes sent down the same chain, \ never on the Tune", TUNE),
        ]
        rows_scene(self, r"what is measured", items,
                   "What is measured? <bookmark mark='b'/> Each stage on the way down is measured by what it changes: timing, "
                   "dynamics, space, noise, peaks and bandwidth. <bookmark mark='c'/> What comes back is scored against what was "
                   "written: the notes found, the keys that are wrong, the note values that are wrong. <bookmark mark='d'/> Wrong "
                   "keys are counted by edit distance, the fewest insertions, deletions and substitutions that turn one line into "
                   "the other, so one missed note costs one, not every note after it. <bookmark mark='e'/> And the transcriber's "
                   "settings were chosen on four other tunes sent down the same chain, never on the Tune, so that the Tune is a "
                   "fair test.", marks="bcde")
