from __future__ import annotations

from videos.psychology.psych15.common import *  # noqa: F403


class Balance(VoiceoverScene):
    def construct(self):
        self.card()
        self.vestibular()
        self.sickness()

    def card(self):
        card = chapter_card(12, r"Balance, \ and the senses together", r"What happens when the senses disagree?",
                            lit={1975: r"Reason \& Brand"}, part=PART, scale=("circuit", "mind"), marr=("what",))
        with self.voiceover("Chapter twelve. Balance, and the senses together."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def vestibular(self):
        head = heading(r"The vestibular sense")
        rows = rows_of([
            (r"beside each cochlea: \ three semicircular canals for turning, \ two otolith organs for tilt and acceleration", WHITE),
            (r"hair cells again, \ the same kind that hear, \ bent by fluid and tiny crystals", SOUND),
            (r"its fastest job: \ keep the eyes still as the head moves, \ a reflex of about 10 ms", TIMING),
            (r"shake your head while reading this line: \ the words stay readable; \ shake the screen instead, \ and they blur", YOU),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "There's a sense organ next to each cochlea that you've probably never thought about. "
            "<bookmark mark='a'/> Three semicircular canals, at right angles to each other, sense the head turning; "
            "two otolith organs sense tilt and acceleration. <bookmark mark='b'/> They use hair cells again, the same "
            "kind that hear, bent by moving fluid or by tiny crystals of calcium carbonate. <bookmark mark='c'/> Their "
            "fastest job is to keep your eyes still in space as your head moves, with a reflex that takes about ten "
            "milliseconds, among the quickest in the body. <bookmark mark='d'/> Try it. Shake your head gently while "
            "reading this line: the words stay readable. Now keep your head still and imagine the screen shaking at "
            "the same speed: the words would blur, because the reflex only knows about your head."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sickness(self):
        head = heading(r"When the senses disagree")
        rows = rows_of([
            (r"reading in a car: \ the inner ear says moving, \ the eyes say still", SOUND),
            (r"a headset's game: \ the eyes say moving, \ the inner ear says still", VISION),
            (r"sensory conflict theory \ (Reason and Brand, \ 1975): \ the mismatch, \ not the motion, \ makes you sick", BAD),
            (r"usually the senses agree, \ and are combined by reliability: \ Part 14's rule, \ as in the McGurk effect", PRIOR),
            (r"why nausea? \ one guess: \ conflicting senses can mean poison; \ it is a guess", GREY_A),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Balance is where conflicts between the senses are felt most. <bookmark mark='a'/> Reading in a moving "
            "car, your inner ear says you're moving and your eyes, fixed on the page, say you're still. "
            "<bookmark mark='b'/> In a virtual-reality game it's the reverse: the eyes say you're flying, the inner "
            "ear says you're sitting down. <bookmark mark='c'/> James Reason and Joseph Brand argued in 1975 that it's "
            "the mismatch, not motion as such, that makes people sick. <bookmark mark='d'/> Most of the time the "
            "senses agree, and the brain combines them by reliability, as in the ventriloquist, the rubber hand and the "
            "McGurk effect. Conflict that can't be resolved is felt as something wrong. <bookmark mark='e'/> Why it's "
            "felt as nausea is not known. One old suggestion is that, in our evolutionary past, senses that suddenly "
            "disagreed often meant poison, and vomiting was the safe response. It's a guess, and hard to test."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
