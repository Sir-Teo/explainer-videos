from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Uses(SoundScene):
    def construct(self):
        chapter(self, 10, r"What separation is for", r"Who needs a mix un-mixed?")
        self.uses()
        self.remix()
        self.rights()
        self.listeners()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"restoration: \ a voice lifted from a demo cassette; \ old mono recordings remixed in stereo", WHITE),
            (r"karaoke and practice: \ the voice removed, \ or the drums, \ so you can play along", WHITE),
            (r"remixing and sampling: \ a single stem from a finished record \ (Part 60's licences still apply)", WHITE),
            (r"upmixing: \ stereo spread to surround and Part 55's immersive formats", WHITE),
            (r"analysis: \ cleaner input for Part 61's transcribers and Part 62's chord recognizers", TUNE),
        ]
        rows_scene(self, r"uses", items,
                   "Who needs a mix un-mixed? <bookmark mark='b'/> Restorers: a voice lifted from a demo cassette, old mono "
                   "recordings remixed in stereo. <bookmark mark='c'/> Karaoke and practice: the voice removed, or the drums, so "
                   "you can play along. <bookmark mark='d'/> Remixers and samplers, taking a single stem from a finished record, "
                   "though Part 60's licences still apply. <bookmark mark='e'/> Upmixing: stereo spread to surround and to Part "
                   "55's immersive formats. <bookmark mark='f'/> And analysis: cleaner input for Part 61's transcribers and Part "
                   "62's chord recognizers.", marks="bcdef")

    # ------------------------------------------------------------------
    def rights(self):
        items = [
            (r"a separated stem is still a copy of the recording: \ the master's rights travel with it", WHITE),
            (r"the vocal of a famous singer, \ separated, \ is the raw material of voice cloning \ (Part 66)", WHITE),
            (r"services now separate on the phone, \ in real time: \ some recordings can now yield useful approximate stems", WHITE),
            (r"what used to be impossible is now a button, \ and rights and permitted uses still depend on jurisdiction and agreements \ (dated)", TUNE),
        ]
        rows_scene(self, r"rights", items,
                   "Separation also raises questions. <bookmark mark='b'/> A separated stem is still a copy of the recording, and "
                   "the master's rights travel with it. <bookmark mark='c'/> The separated vocal of a famous singer is the raw "
                   "material of voice cloning, the subject of Part 66. <bookmark mark='d'/> Apps now separate on a phone, in real "
                   "time: some recordings can now yield useful approximate stems. <bookmark mark='e'/> What used to be impossible is now a button, "
                   "and rights and permitted uses still depend on jurisdiction and agreements.", marks="bcde")

    # ------------------------------------------------------------------
    def listeners(self):
        items = [
            (r"the cocktail-party problem: \ Cherry \ (1953) \ asked how people follow one voice among many", WHITE),
            (r"people do not separate signals; \ they attend to streams \ (Bregman, \ 1990: \ auditory scene analysis)", WHITE),
            (r"cues: \ a common onset, \ harmonicity, \ a common location, \ continuity", WHITE),
            (r"the methods of this part borrow each cue: \ panning, \ harmonic templates, \ continuity in time", TUNE),
        ]
        rows_scene(self, r"how listeners do it", items,
                   "And how do listeners do it? <bookmark mark='b'/> Colin Cherry named the cocktail-party problem in 1953: how do "
                   "people follow one voice among many? <bookmark mark='c'/> People attend to perceptual streams rather than necessarily reconstructing isolated waveforms, "
                   "as Albert Bregman's auditory scene analysis of 1990 described. <bookmark mark='d'/> Their cues: a common onset, "
                   "harmonicity, a common location, continuity. <bookmark mark='e'/> The methods of this part borrow each cue: "
                   "panning, harmonic templates, continuity in time.", marks="bcde")

    # ------------------------------------------------------------------
    def remix(self):
        d = load("remix")
        c = clip("remix.three")
        card = listen_card(r"The session as mixed, \ then two remixes: \ vocals 6 dB up, \ drums 6 dB down. \ One was made from separated stems, \ one from the true stems. \ Which was separated?", width=9.6)
        with self.voiceover("Your turn. A remix needs less than you might think. Hear the session as mixed, then two remixes with the vocals six decibels up and the drums six down. One was made from the network's vocals and the median filter's drums; the other from the true stems. Which was separated?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"as mixed", r"first remix", r"second remix"], width=3.6, height=0.9, buff=0.35, size=17).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        res = label(rf"the first: \ {d['sdr_remix']:.1f} dB from the true remix; \ the original mix, \ {d['sdr_mix']:.1f} dB",
                    font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        why = label(r"in a remix the stems are added back, \ so most of each stem's errors cancel", font_size=16, color=GREY_A).next_to(res, DOWN, buff=0.3)
        st = d["starts"]
        ks = ["mix", "separated", "true"]
        with self.listen(c) as snd:
            window(snd, r"a remix, \ two ways", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"The first remix was the separated one. The two are close: {say(d['sdr_remix'], 1)} decibels apart by SDR, much closer than either is to the "
            "original mix. A remix adds the stems back together, so whatever one stem wrongly took from another is mostly "
            "returned. Turning a voice up or down is far easier than lifting it out alone: a separator can be good enough for "
            "a remix long before it is good enough for an a cappella."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res), FadeIn(why))
        self.wait(0.4)
        self.clear_scene()
