from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Voices(SoundScene):
    def construct(self):
        chapter(self, 8, r"Singing and cloned voices", r"Whose voice is it, \ when a machine sings?")
        self.synthesis()
        self.three()
        self.cloning()
        self.law()

    # ------------------------------------------------------------------
    def synthesis(self):
        items = [
            (r"singing synthesis began as rules: \ Part 8's voice is one \ (a source and formant filters)", WHITE),
            (r"concatenation: \ Vocaloid \ (2004) \ joins recorded syllables of one singer; \ Hatsune Miku \ (2007) \ became a star", WHITE),
            (r"then networks: \ a score and lyrics to a spectrogram, \ a vocoder to sound", WHITE),
            (r"Vocaloid's singers consented and were paid: \ the voice was licensed, \ like a sample library", TUNE),
        ]
        rows_scene(self, r"singing synthesis", items,
                   "Machines have sung for a long time. <bookmark mark='b'/> The first singing synthesizers were rules, as Part 8's "
                   "voice is: a source and formant filters. <bookmark mark='c'/> Then concatenation: Yamaha's Vocaloid, from 2004, "
                   "joins recorded syllables of one singer, and its voice Hatsune Miku, in 2007, became a star in her own right. "
                   "<bookmark mark='d'/> Then networks, from a score and lyrics to a spectrogram and through a vocoder to sound. "
                   "<bookmark mark='e'/> Vocaloid's singers consented and were paid: the voice was licensed, like a sample library.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def cloning(self):
        items = [
            (r"voice conversion: \ keep a performance's content and timing, \ give it another speaker's or singer's timbre", WHITE),
            (r"a few minutes of someone's recordings can now be enough \ (Part 64's separation supplies clean vocals)", WHITE),
            (r"2023: \ a song with imitated voices of two famous singers spreads widely before it is taken down \ (dated)", WHITE),
            (r"the singer did not consent, \ and the recordings it learnt from belong to someone", WHITE),
            (r"the technique is the same as timbre transfer; \ the difference is whose sound it is", TUNE),
        ]
        rows_scene(self, r"cloned voices", items,
                   "Voice conversion keeps a performance's content and timing and gives it another singer's timbre. "
                   "<bookmark mark='c'/> A few minutes of someone's recordings can now be enough, and Part 64's separation supplies "
                   "clean vocals from finished records. <bookmark mark='d'/> In 2023 a song with imitated voices of two famous "
                   "singers spread widely before it was taken down. <bookmark mark='e'/> The singers had not consented, and the "
                   "recordings the model learnt from belonged to someone. <bookmark mark='f'/> The technique is the same as the "
                   "last chapter's timbre transfer; the difference is whose sound it is.", marks="cdef")

    # ------------------------------------------------------------------
    def law(self):
        items = [
            (r"a voice is not a copyrighted work; \ protection comes from rights of publicity and personality, \ which vary by place", WHITE),
            (r"Tennessee's ELVIS Act \ (2024) \ added voice to the likeness a person controls \ (dated)", WHITE),
            (r"platforms label or remove imitations on request; \ some artists license their voices to such models", WHITE),
            (r"what is settled: \ consent and pay can be built in; \ what is not: \ the law across countries \ (verify the latest)", TUNE),
        ]
        rows_scene(self, r"the law, \ for now", items,
                   "What does the law say? <bookmark mark='b'/> A voice is not a copyrighted work; protection comes from rights of "
                   "publicity and personality, which vary by place. <bookmark mark='c'/> Tennessee's ELVIS Act of 2024 added a "
                   "person's voice to the likeness they control. <bookmark mark='d'/> Platforms label or remove imitations on "
                   "request, and some artists license their voices to such models. <bookmark mark='e'/> What is settled is that "
                   "consent and payment can be built in; what is not is the law across countries, which is changing as this is "
                   "made.", marks="bcde")

    # ------------------------------------------------------------------
    def three(self):
        d = load("voices")
        c = clip("voices.three")
        boxes = choice_boxes([r"soprano", r"alto", r"tenor"], width=3.0, height=0.9, buff=0.6, size=19).move_to(UP * 0.6)
        note = label(r"the same notes, \ timing and vibrato; \ a different source and vocal tract each time", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"one performance, \ three voices", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("What a voice converter keeps and what it changes can be heard with Part 8's voices. Here is one performance of the Tune's first phrase, the same notes, timing and vibrato, sung by a soprano, an alto and a tenor."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = ["soprano", "alto", "tenor"]
        with self.listen(c) as snd:
            window(snd, r"three voices", kind="synthesized", detail=r"Part 8's voices", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            "The performance stays; the source and the vocal tract change, and with them who seems to be singing. In Part 8 "
            "each voice was a set of numbers we chose. A voice converter learns those numbers from someone's recordings, and "
            "that is where the trouble starts."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
