from __future__ import annotations

from videos.psychology.psych15.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.aids()
        self.implants()
        self.codecs()
        self.haptics()

    def card(self):
        card = chapter_card(14, r"In practice: \ hearing aids, \ codecs and haptics",
                            r"Where does the science of the senses earn its keep?", lit={1993: r"MPEG Layer III"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: hearing aids, codecs and haptics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def aids(self):
        head = heading(r"Why a hearing aid is not an amplifier")
        rows = rows_of([
            (r"most hearing loss is lost outer hair cells: \ the cochlear amplifier of chapter two", WHITE),
            (r"quiet sounds vanish, \ but loud ones are as loud as ever: \ loudness grows abnormally fast", BAD),
            (r"so turning everything up makes loud sounds painful", PAIN),
            (r"modern aids compress: \ more gain for quiet sounds, \ little for loud, \ separately in each frequency band", TIMING),
            (r"and the filters are broader: \ amplified speech in noise stays hard to follow", GREY_A),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "Start with the commonest sensory disability. <bookmark mark='a'/> Most hearing loss is the loss of outer "
            "hair cells, the cochlear amplifier of chapter two. <bookmark mark='b'/> Without it, quiet sounds vanish, "
            "but loud sounds are nearly as loud as ever, so loudness grows abnormally fast between the two. "
            "<bookmark mark='c'/> That's why simply turning everything up fails: by the time speech is audible, loud "
            "sounds hurt. <bookmark mark='d'/> Modern hearing aids compress instead, giving a lot of gain to quiet "
            "sounds and little to loud ones, separately in each band of frequencies: an electronic stand-in for the "
            "lost amplifier. <bookmark mark='e'/> What they can't restore is the sharp tuning. The ear's filters stay "
            "broad, and a voice in a noisy room stays hard to separate, which is the complaint hearing-aid users make "
            "most."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def implants(self):
        head = heading(r"Cochlear implants: \ Greenwood's map, \ wired")
        rows = rows_of([
            (r"when the hair cells are gone, \ electrodes threaded into the cochlea stimulate the nerve directly", WHITE),
            (r"each of a dozen to two dozen contacts drives one place: \ the place-frequency map, \ in hardware", PLACE),
            (r"hundreds of thousands of users worldwide: \ about 740{,}000 devices registered by 2019", TIMING),
            (r"speech is often understood well; \ music and pitch are poor: \ few channels, \ little timing", BAD),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "When the hair cells are gone entirely, there's another way in. <bookmark mark='a'/> A cochlear implant "
            "threads a row of electrodes into the cochlea and stimulates the auditory nerve directly. "
            "<bookmark mark='b'/> Each of a dozen to two dozen contacts drives the nerve fibres at one place, carrying "
            "the sound's energy in one band of frequencies: Greenwood's place map, built in hardware. "
            "<bookmark mark='c'/> The American National Institutes of Health counted about seven hundred and forty "
            "thousand implants registered worldwide by 2019. <bookmark mark='d'/> Many users understand speech well, "
            "even on the phone. Music is harder: with so few channels, and little of the fine timing that chapter four "
            "showed pitch depends on, melodies are often hard to follow."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def codecs(self):
        head = heading(r"Codecs: \ throwing away what you cannot hear")
        rows = rows_of([
            (r"a CD sends 1{,}411 kilobits a second; \ a good MP3, \ about 128 to 256: \ a tenth of the data", WHITE),
            (r"the encoder runs a model of hearing: \ the threshold in quiet of chapter one, \ the masking of chapter three", SOUND),
            (r"in each short slice of time and each band, \ anything below the masked threshold is dropped or coarsened", PLACE),
            (r"perceptual coding: \ MP3 in the 1990s, \ AAC and Opus after it; \ almost all music and calls today", TIMING),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Psychoacoustics is also the reason your music fits on your phone. <bookmark mark='a'/> A compact disc "
            "sends about fourteen hundred kilobits of data a second. A good MP3 uses around a tenth of that. "
            "<bookmark mark='b'/> The encoder contains a model of hearing: the threshold in quiet, the formula from "
            "chapter one, and the masking of chapter three. <bookmark mark='c'/> In every few milliseconds of sound and "
            "every band of frequencies, it works out what a listener could not hear under the louder sounds nearby, and "
            "spends almost no bits on it. <bookmark mark='d'/> This is perceptual coding. It made the MP3 in the "
            "nineteen-nineties, and its descendants carry nearly all the music people stream and the calls they make."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def haptics(self):
        head = heading(r"Touch, \ engineered")
        rows = rows_of([
            (r"phones buzz near 150 to 250 Hz: \ where the Pacinian endings are most sensitive", SOUND),
            (r"Braille cells and touch displays are designed around the fingertip's 2 to 3 mm", TOUCH),
            (r"pain clinics use the gate and the brain's control of it: \ TENS, \ movement, \ and treatments for expectation and fear", PAIN),
            (r"and headsets add vibration and sound, \ to keep the senses in agreement", PRIOR),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Last, the skin. <bookmark mark='a'/> The vibration motor in your phone buzzes at around one hundred and "
            "fifty to two hundred and fifty hertz, close to where the Pacinian endings are most sensitive. "
            "<bookmark mark='b'/> Braille cells and touch displays are designed around the fingertip's resolution of a "
            "few millimetres. <bookmark mark='c'/> Pain clinics use the gate and the brain's control over it: "
            "electrical stimulation of the large fibres, graded movement, and psychological treatments aimed at the "
            "fear and expectation that hold the gate open. <bookmark mark='d'/> And virtual-reality systems add "
            "vibration and sound to keep the senses agreeing, because, as chapter twelve showed, disagreement makes "
            "people sick."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
