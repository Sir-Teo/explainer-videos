from __future__ import annotations

from videos.psychology.psych15.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.hidden()
        self.chronic()
        self.predict()

    def card(self):
        card = chapter_card(15, r"Frontier: \ hidden losses and learned pain", r"What can a hearing test not see?",
                            lit={2009: r"Kujawa \& Liberman"}, part=PART, scale=("circuit", "mind"), marr=("how",))
        with self.voiceover("Chapter fifteen. The frontier: hidden losses, and learned pain."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", MODEL),
            (r"the cochlea as a bank of tuned filters, \ with an active amplifier", WHITE),
            (r"masking and critical bands, \ precise enough to build codecs on", WHITE),
            (r"timing differences between the ears, \ read to about 10 $\mu$s", WHITE),
            (r"pain is gated, \ and controlled from the brain", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", BAD),
            (r"how pitch is computed: \ place, \ timing, \ or both", WHITE),
            (r"how mammals read interaural time", WHITE),
            (r"how much of the rubber hand is expectation", WHITE),
            (r"how many smells there are", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.voiceover(
            "Here's where things stand. <bookmark mark='a'/> Solid: the cochlea is a bank of tuned filters with an "
            "active amplifier; masking and critical bands are understood well enough to build every audio codec on; "
            "the ears' timing differences are read to about ten microseconds; and pain is gated in the spinal cord and "
            "controlled from the brain. <bookmark mark='b'/> Argued: exactly how pitch is computed; how mammals read "
            "the timing between the ears; how much of the rubber hand is expectation; and how many smells there are. "
            "Three more questions are at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=5.0)
        self.clear_scene()

    def hidden(self):
        head = heading(r"Hidden hearing loss")
        rows = rows_of([
            (r"2009: \ Kujawa and Liberman expose mice to two hours of loud noise", WHITE),
            (r"their thresholds recover completely: \ a normal audiogram", TIMING),
            (r"but up to half the synapses between hair cells and nerve fibres are gone for good", BAD),
            (r"a loss the standard test cannot see: \ perhaps why some people struggle in noisy rooms with normal audiograms", PLACE),
            (r"in people the evidence is still mixed: \ the synapses cannot be counted in a living ear", GREY_A),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.KUJAWA_LIBERMAN_2009.cite)
        with self.voiceover(
            "The first is a kind of hearing loss that a hearing test can't see. <bookmark mark='a'/> In 2009, Sharon "
            "Kujawa and Charles Liberman exposed mice to two hours of loud noise, the kind of level a concert can "
            "reach. <bookmark mark='b'/> Their hearing thresholds recovered completely within days: by the audiogram, "
            "nothing was wrong. <bookmark mark='c'/> But many of the synapses between the inner hair cells and the "
            "nerve fibres, up to about half in later studies, were gone for good. <bookmark mark='d'/> If the same "
            "happens in people, it could explain why many adults with normal audiograms struggle to follow speech in "
            "a noisy restaurant. <bookmark mark='e'/> In people the evidence is still mixed, partly because the "
            "synapses can't be counted in a living ear. It's a live question for anyone who goes to loud concerts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def chronic(self):
        head = heading(r"Pain that has been learned")
        rows = rows_of([
            (r"most acute pain fades as the injury heals; \ for some people, \ it does not", WHITE),
            (r"chronic pain is common, \ and often outlasts any damage that can be found", PAIN),
            (r"the nervous system can become sensitized: \ the gate held open, \ the signal amplified", PLACE),
            (r"a growing view: \ chronic pain as learning, \ in the brain's systems for prediction and value", PRIOR),
            (r"conditioning and prediction errors are Parts 16 and 17; \ treatments, \ Part 57", GREY_A),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "The second concerns pain that doesn't go away. <bookmark mark='a'/> Most pain fades as an injury heals. "
            "For some people it doesn't. <bookmark mark='b'/> Chronic pain is common, and it often outlasts any "
            "damage a doctor can find. <bookmark mark='c'/> One mechanism is sensitization: after injury, the spinal "
            "cord and brain can turn up their own gain, holding the gate open. <bookmark mark='d'/> A growing view, "
            "still argued over, treats chronic pain partly as something learned, in the brain's systems for "
            "prediction and value, the same systems that learn which places are dangerous. <bookmark mark='e'/> "
            "Learning and prediction errors are Parts 16 and 17. Treatments, and the evidence for them, are Part 57."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def predict(self):
        head = heading(r"The ear that predicts")
        rows = rows_of([
            (r"play a regular sequence of tones, \ then an odd one: \ the brain responds to the surprise", WHITE),
            (r"the mismatch negativity, \ about 150 ms after the odd tone, \ even when attention is elsewhere", TIMING),
            (r"the auditory cortex seems to predict the next sound, \ and to signal when it is wrong", PRIOR),
            (r"perception as prediction: \ Part 14's priors, \ running in time; \ Part 58", PLACE),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "The last is about expectation. <bookmark mark='a'/> Play a regular sequence of identical tones, then an "
            "odd one. <bookmark mark='b'/> Even when the listener is reading a book and ignoring the sounds, the brain's "
            "electrical response to the odd tone differs, about a hundred to two hundred milliseconds after it. Risto "
            "Näätänen and colleagues named it the mismatch negativity in 1978. <bookmark mark='c'/> One reading is that "
            "the auditory cortex is constantly predicting the next sound, and signals when the prediction fails. "
            "<bookmark mark='d'/> That's Part 14's priors, running forward in time. Whether the whole brain works this "
            "way is the question of Part 58."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
