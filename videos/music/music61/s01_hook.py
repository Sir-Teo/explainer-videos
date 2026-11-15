from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.answer_keys()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune with its chords, \ twice, \ on the same piano. \ One is a performance; \ the other is a machine's "
                           r"transcription of it, \ played back. \ Which is the original?", width=10.0)
        with self.voiceover(
            "A question for your ears. The Tune with its chords, twice, on the same piano. One is a performance; the other is "
            "a machine's transcription of that performance, played back. Which is the original?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"original or copy?", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        s = d["scores"]
        res = label(rf"the second: \ the copy has {s['hits']} of the {s['ref']} notes right, \ and {s['est'] - s['hits']} the performance did not play", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The second was the original. The machine's copy got {say(s['hits'])} of its {say(s['ref'])} notes right, and added "
            f"{say(s['est'] - s['hits'])} that were never played. Close, and not the same: this part is about that gap."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"Rome, \ 1770: \ the fourteen-year-old Mozart hears Allegri's Miserere in the Sistine Chapel", WHITE),
            (r"a nine-voice setting the Chapel kept to itself; \ that evening, \ his father wrote, \ Wolfgang wrote it out", WHITE),
            (r"to hear music and write down its notes: \ transcription, \ the oldest skill of the trained ear", WHITE),
            (r"for machines it has been called the holy grail of music computing", TUNE),
        ]
        rows_scene(self, r"the holy grail", items,
                   "The task is old. <bookmark mark='b'/> In Rome, in 1770, the fourteen-year-old Mozart heard Allegri's Miserere "
                   "in the Sistine Chapel, <bookmark mark='c'/> a nine-voice setting the Chapel kept to itself. That evening, his "
                   "father wrote home, Wolfgang wrote it out from memory. <bookmark mark='d'/> To hear music and write down its "
                   "notes is transcription, the oldest skill of the trained ear. <bookmark mark='e'/> For machines it has been "
                   "called the holy grail of music computing.", marks="bcde")

    # ------------------------------------------------------------------
    def answer_keys(self):
        items = [
            (r"Act XI turns the series' chain around: \ sound in, \ notes, \ beats, \ names and sources out", WHITE),
            (r"a listening machine needs an answer key: \ the notes that were really played", WHITE),
            (r"for recordings, \ answer keys are rare, \ slow to make, \ and argued over", WHITE),
            (r"Monochord makes its own sound, \ so every answer is exact, \ and unlimited", TUNE),
        ]
        rows_scene(self, r"Act XI: \ listening machines", items,
                   "This is the first part of Act Eleven, which turns the series' chain around: sound in, and notes, beats, "
                   "names and sources out. <bookmark mark='b'/> A listening machine is only as good as its answer key, the notes "
                   "that were really played. <bookmark mark='c'/> For recordings, answer keys are rare, slow to make, and argued "
                   "over. <bookmark mark='d'/> Monochord makes its own sound, so every answer is exact, and there is no limit to "
                   "how many.", marks="bcd")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"one voice's pitch: \ YIN, \ and what noise does to it",
            r"many notes at once: \ salience, \ and the hidden octave",
            r"where notes begin: \ spectral flux",
            r"taking a spectrogram apart: \ NMF; \ a network that listens",
            r"timbres never heard; \ keeping score",
            r"from notes to a score; \ fifty years of transcription",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. One voice's pitch, by YIN, and what noise does to it. <bookmark mark='b'/> Many notes at once, "
            "and the octave that hides. <bookmark mark='c'/> Where notes begin. <bookmark mark='d'/> Taking a spectrogram apart "
            "into notes, and a network that learns to listen. <bookmark mark='e'/> What happens on a timbre neither has heard, "
            "and how to keep score. <bookmark mark='f'/> And from notes to a score, and fifty years of the field."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
