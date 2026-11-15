from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"A voice and a piano recorded together on one track. \ Then the voice twice: \ once as it was recorded alone, \ "
                           r"once separated from the mix by a machine. \ Which is the separated one?", width=10.0)
        with self.voiceover(
            "A question for your ears. A voice and a piano recorded together on one track. Then the voice twice: once as it "
            "was recorded on its own, once separated from the mix by a machine. Which is the separated one?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"the mix", r"first", r"second"], width=2.8, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"mix, \ then two voices", kind="physical model", detail=r"Part 8's voice, \ Part 38's piano", corner=DL, tag_corner=DR)
            ks = ["mix", "first", "second"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = label(rf"the first was separated: \ a faint ghost of the piano, \ a little smearing \ ({d['sdr']:.0f} dB SDR); \ the second was the voice alone", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first was separated: listen for a faint ghost of the piano and a little smearing. The second was the voice "
            f"as recorded alone. By the measure of Chapter 9, the separation is {say(d['sdr'])} decibels from the truth."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1977 or so: \ John Lennon records a song at home on cassette, \ voice and piano on one track", WHITE),
            (r"in the 1990s the surviving Beatles try to finish it, \ and give up: \ the piano and the hum could not be removed", WHITE),
            (r"2023: \ software built for a documentary separates the voice, \ and `Now and Then' is released", WHITE),
            (r"separation is un-baking a cake: \ the mix adds everything together, \ and addition forgets", WHITE),
            (r"Monochord owns the ingredients, \ so this part can say exactly how well each method does", TUNE),
        ]
        rows_scene(self, r"un-baking a cake", items,
                   "The question has a famous answer. <bookmark mark='b'/> Around 1977 John Lennon recorded a song at home on "
                   "cassette, voice and piano on one track. <bookmark mark='c'/> In the 1990s the surviving Beatles tried to finish "
                   "it and gave up: the piano and the hum could not be taken away from the voice. <bookmark mark='d'/> In 2023, "
                   "software built for a documentary separated the voice, and the song, Now and Then, was released. "
                   "<bookmark mark='e'/> Separation is un-baking a cake: the mix adds everything together, and addition forgets. "
                   "<bookmark mark='f'/> Monochord owns the ingredients of its cakes, so this part can say exactly how well each "
                   "method does.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the mixing model, \ and what it takes to undo it",
            r"panning and independent components",
            r"harmonic against percussive; \ factorization again",
            r"masks, \ and the best a mask can do",
            r"the phase problem; \ networks that separate",
            r"measuring separation, \ and what it is for",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The mixing model, and what it takes to undo it. <bookmark mark='b'/> Separating by where sounds "
            "are panned, and by independence. <bookmark mark='c'/> Harmonic against percussive, and factorization again. "
            "<bookmark mark='d'/> Masks, and the best any mask can do. <bookmark mark='e'/> The phase problem, and networks "
            "that separate. <bookmark mark='f'/> And how separation is measured, and what it is for."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
