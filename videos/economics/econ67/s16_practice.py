from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ reading a paper, \ a forecast, \ an op-ed", r"What should a careful reader "
             r"ask of each?", "Chapter fourteen. In practice: reading a paper, a forecast, an op-ed.",
             scale=("world",), horizon=("a day",))
        self.paper()
        self.prior()
        self.forecast_oped()

    def paper(self):
        cards = point_cards([
            (r"the design", r"what variation identifies the effect, \ and could it have been chosen after seeing "
             r"results?", TRUE),
            (r"the evidence", r"how far past 1.96? \ how many outcomes and specifications? \ was there a plan?",
             PUB),
            (r"the size", r"is the effect plausible, \ or the size only a lucky estimate could have? \ what do "
             r"other studies find?", FAIL),
            (r"the record", r"are the data and code public, \ and has anyone reproduced or replicated it?", FIRST),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"reading a paper", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Four questions for any empirical paper. <bookmark mark='a'/> The design: what variation identifies the "
            "effect, and could it have been chosen after seeing the results? <bookmark mark='b'/> The evidence: how "
            "far past the line is the key test, how many outcomes and specifications were tried, and was there a "
            "plan? <bookmark mark='c'/> The size: is the effect plausible, or is it the size that only a lucky "
            "estimate could produce, given the study's power? And what do other studies find? <bookmark mark='d'/> "
            "And the record: are the data and code public, and has anyone reproduced or replicated it?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def prior(self):
        P = load("playit")
        B = P["by_z"]
        rows = VGroup(
            label(r"a new result: \ an instrumental-variables estimate, \ $p = 0.04$", font_size=24, color=WHITE),
            label(rf"in the simulated field, \ results like it replicate {100 * B[0]['rate']:.0f}\% of the time",
                  font_size=22, color=PUB),
            label(rf"and their true effect is about {100 * B[0]['true_over_orig']:.0f}\% of the published one",
                  font_size=22, color=FIRST),
            label(r"a reader's best guess: \ shrink the estimate, \ and wait for the replication", font_size=22,
                  color=E.ACCENT),
            label(r"a pre-registered trial with $p < 0.001$ deserves a very different reading", font_size=22,
                  color=TRUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.2)
        tag = island_tag(r"the simulated field's own odds \ (chapter one)", corner=DL, font_size=12)
        with self.voiceover(
            "Put numbers on it. <bookmark mark='a'/> A new paper reports an instrumental-variables estimate with a "
            "p-value of four in a hundred. <bookmark mark='b'/> In the simulated field, results like it replicate "
            f"about {100 * B[0]['rate']:.0f} percent of the time. <bookmark mark='c'/> And their true effects are, "
            f"on average, about {100 * B[0]['true_over_orig']:.0f} percent of what was published. <bookmark "
            "mark='d'/> So a reader's best guess is a smaller effect than the paper's, held with less confidence, "
            "until someone replicates it. <bookmark mark='e'/> A pre-registered trial with a p-value below one in a "
            "thousand deserves a very different reading. The p-value is the same kind of number; what it means "
            "depends on the process that produced it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def forecast_oped(self):
        cards = point_cards([
            (r"a forecast", r"a number with an interval, \ a date and a record: \ how did this forecaster do "
             r"before? \ (Part 57)", FIRST),
            (r"a model's claim", r"what is assumed, \ what is estimated, \ and would the claim survive a "
             r"different, \ reasonable assumption?", STATE),
            (r"an op-ed", r"separate the is from the ought: \ which sentences are evidence, \ which are values?",
             PUB),
            (r"a consensus", r"read the Dial, \ not the loudest estimate: \ is it settled, \ does it depend on the "
             r"setting, \ or is it contested?", TRUE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"reading a forecast, \ a model, \ an op-ed", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.5)
        with self.voiceover(
            "The same habits for everything else economists say in public. <bookmark mark='a'/> A forecast should "
            "come with an interval, a date and a record: how has this forecaster done before? Part fifty-seven "
            "scored the professionals. <bookmark mark='b'/> A model's claim rests on assumptions: which are "
            "estimated, which assumed, and would the claim survive a different, reasonable one? <bookmark "
            "mark='c'/> An op-ed mixes evidence with values; this series' is-and-ought card separates the two. "
            "<bookmark mark='d'/> And when someone tells you what economists know, read the Dial rather than the "
            "loudest estimate: settled within a range, depending on the setting, or contested."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
