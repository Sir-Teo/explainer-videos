from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.idea()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"The Tune's first phrase, \ sung alone, \ three times: \ once as recorded, \ twice through a codec that "
                           r"throws most of the data away. \ Which was the original?", width=10.0)
        with self.voiceover(
            "In the 1980s Karlheinz Brandenburg, at Erlangen in Germany, was coding music for digital telephone lines. Begin with a voice. The Tune's first phrase, sung alone, three times: once as recorded, and twice through a "
            "codec that throws most of the data away. Which was the original?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one voice, \ three files", kind="physical model", detail=r"Part 8's voice, \ Monochord's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], st["third"] - 0.4, buff=0.08)
            pulse(snd, boxes[2], st["third"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        rows = VGroup(VGroup(label(r"version", font_size=17, color=GREY_A), label(r"estimated rate", font_size=17, color=GREY_A), label(r"rate ratio", font_size=17, color=GREY_A),
                             label(r"its noise against the mask", font_size=17, color=GREY_A)))
        data = [(r"first: \ our coder", f"{d['c64']['kbps']:.0f} kbit/s", rf"1/{d['pcm_kbps'] / d['c64']['kbps']:.0f}", rf"{d['c64']['margin']:.0f} dB below it", TUNE),
                (r"second: \ the original", f"{d['pcm_kbps']:.0f} kbit/s", r"1", r"none", WHITE),
                (r"third: \ our coder", f"{d['c16']['kbps']:.0f} kbit/s", rf"1/{d['pcm_kbps'] / d['c16']['kbps']:.0f}", rf"{-d['c16']['margin']:.0f} dB above it", EAR)]
        for a, b_, c_, e, col in data:
            rows.add(VGroup(label(a, font_size=19, color=col), label(b_, font_size=19, color=WHITE), label(c_, font_size=19, color=WHITE), label(e, font_size=19, color=col)))
        rows.arrange(DOWN, buff=0.4)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.0 * i)
        rows.move_to(UP * 0.2)
        note = label(r"estimated coding budgets; \ this demonstration does not establish transparency", font_size=19, color=TUNE).to_edge(DOWN, buff=0.6)
        head = label(r"the second was the original", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second. <bookmark mark='a'/> The original is sixteen-bit samples at forty-eight kilohertz: seven hundred and "
            "sixty-eight kilobits a second. The third was our codec at sixteen kilobits, an estimated coding budget one forty-eighth of the PCM rate, and you "
            "could hear it: its noise rises above what the voice can hide. <bookmark mark='b'/> But the first was the same "
            f"codec targeting sixty-four; its estimated rate here is about {say(d['c64']['kbps'])} kilobits a second. If you could not tell it from the original, that is the whole "
            "idea of this part: substantial data reduction can be perceptually subtle under suitable conditions; this demonstration does not prove transparency. Our perceptual coder estimates coded lengths rather than serializing a complete bitstream."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1980s: \ at Erlangen, \ Karlheinz Brandenburg works on coding music for ISDN telephone lines", WHITE),
            (r"the codec copes with orchestras and rock, \ and fails on one recording: \ Suzanne Vega's `Tom's Diner', \ a voice alone", WHITE),
            (r"a voice alone has nothing to hide the noise behind; \ he listened to it, \ he has said, \ over and over while tuning", WHITE),
            (r"1991 to 1993: \ MPEG-1 Audio Layer III; \ 1995: \ the file extension .mp3", WHITE),
            (r"1999: \ Napster. \ A file a tenth the size of a CD's broke the record industry's business", TUNE),
        ]
        rows_scene(self, r"Tom's Diner", items,
                   "The question has a famous history. <bookmark mark='b'/> In the 1980s, at Erlangen in Germany, Karlheinz "
                   "Brandenburg was working on coding music for digital telephone lines. <bookmark mark='c'/> His codec coped with "
                   "orchestras and rock, and failed on one recording: Suzanne Vega's Tom's Diner, a voice alone. "
                   "<bookmark mark='d'/> A voice alone has nothing to hide the coding noise behind, and he has said he listened to "
                   "it over and over while tuning the coder. <bookmark mark='e'/> The result became MPEG-1 Audio Layer Three, "
                   "standardized between 1991 and 1993, and from 1995 its files ended in dot m p three. <bookmark mark='f'/> In "
                   "1999 came Napster: small files and peer-to-peer distribution disrupted the record industry alongside other economic and technological changes.", marks="bcdef")

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"lossless coding removes redundancy: \ what can be predicted need not be sent \ (about half the size)", WHITE),
            (r"perceptual coding removes irrelevance: \ what cannot be heard need not be sent \ (a tenth, \ or less)", WHITE),
            (r"the second needs a model of hearing: \ Part 4's masking, \ band by band, \ frame by frame", WHITE),
            (r"and a transform in which to spend bits where they are audible: \ the MDCT", TUNE),
        ]
        rows_scene(self, r"two kinds of compression", items,
                   "There are two kinds of compression. <bookmark mark='b'/> Lossless coding removes redundancy: what can be "
                   "predicted need not be sent, and music usually halves. <bookmark mark='c'/> Perceptual coding removes "
                   "irrelevance: what cannot be heard need not be sent, and music shrinks to a tenth or less. "
                   "<bookmark mark='d'/> The second needs a model of hearing, Part 4's masking, applied band by band and frame by "
                   "frame, <bookmark mark='e'/> and a transform in which to spend the bits where they will be heard.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"entropy, \ prediction and a bit-exact lossless coder",
            r"masking thresholds, \ computed frame by frame",
            r"the MDCT, \ and why its aliases cancel",
            r"a perceptual coder: \ bit allocation, \ rate control, \ pre-echo, \ stereo",
            r"MP3, \ AAC and Opus; \ listening tests and their statistics",
            r"transcoding, \ vector quantization and neural codecs",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Entropy, prediction, and a lossless coder that rebuilds every bit. <bookmark mark='b'/> "
            "Masking thresholds, computed frame by frame. <bookmark mark='c'/> The modified discrete cosine transform, and why "
            "its aliases cancel. <bookmark mark='d'/> A perceptual coder of our own: bit allocation, rate control, pre-echo and "
            "stereo. <bookmark mark='e'/> MP3, AAC and Opus, and listening tests with their statistics. "
            "<bookmark mark='f'/> And transcoding, vector quantization, and the neural codecs at the frontier."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
