from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403

ROWS = [
    ("correspondence_bias",
     "Eight new rows today. The first: observers infer a person's attitude from what they say, even when the "
     "situation forced it. <bookmark mark='a'/> The original: Jones and Harris's Castro essays, in 1967. "
     "<bookmark mark='b'/> The record: Gilbert and Malone's review, a replication in the Philippines in 2017, and "
     "Walker, Smith and Vul's rational observer. <bookmark mark='c'/> The effect reproduces; whether it's an error "
     "depends on how sure the observer can be about the situation. <bookmark mark='d'/> Replicated."),
    ("induced_compliance",
     "The second: freely choosing to argue against your own view moves your attitude toward what you argued. "
     "<bookmark mark='a'/> The original: Festinger and Carlsmith's one dollar and twenty dollars, in 1959. "
     "<bookmark mark='b'/> The record: the replication of 2024, in thirty-nine laboratories and nearly five "
     "thousand people, which found no difference between high and low choice. <bookmark mark='c'/> Writing the "
     "essay shifted attitudes; choosing to write it did not add to that. <bookmark mark='d'/> Failed."),
    ("false_consensus",
     "The third: people overestimate how many others share their choices. <bookmark mark='a'/> The original: Ross, "
     "Greene and House's sandwich board, in 1977. <bookmark mark='b'/> The record: Mullen and colleagues' "
     "meta-analysis of a hundred and fifteen tests. <bookmark mark='c'/> Reliable and moderate, and partly "
     "reasonable inference from a sample of one. <bookmark mark='d'/> Replicated."),
    ("dunning_kruger",
     "The fourth: the least skilled overestimate themselves most, because they lack the skill to see their errors. "
     "<bookmark mark='a'/> The original: Kruger and Dunning, 1999. <bookmark mark='b'/> The record: Nuhfer and "
     "colleagues' random numbers, and McIntosh and colleagues' reanalysis. <bookmark mark='c'/> The graph "
     "replicates easily; how much of it is a deficit of insight, rather than regression and a flattering shift, is "
     "argued. <bookmark mark='d'/> Contested."),
    ("better_than_average",
     "The fifth: most people rate themselves above the median. <bookmark mark='a'/> The original: Svenson's "
     "drivers, in 1981. <bookmark mark='b'/> The record: a preregistered replication with twelve hundred people, in "
     "2023. <bookmark mark='c'/> Robust, though vague traits let each person define them in their own favour. "
     "<bookmark mark='d'/> Replicated."),
    ("elderly_priming",
     "The sixth: reading words about old age makes people walk more slowly. <bookmark mark='a'/> The original: "
     "Bargh, Chen and Burrows, 1996. <bookmark mark='b'/> The record: Doyen and colleagues' infrared sensors, in "
     "2012. <bookmark mark='c'/> The likely source of the original effect is the experimenters. "
     "<bookmark mark='d'/> Failed."),
    ("power_posing",
     "The seventh: two minutes of an expansive pose change hormones and risk-taking. <bookmark mark='a'/> The "
     "original: Carney, Cuddy and Yap, 2010. <bookmark mark='b'/> The record: Ranehill and colleagues' two hundred "
     "people, and the first author's own statement. <bookmark mark='c'/> A small effect on how powerful people say "
     "they feel remains. <bookmark mark='d'/> Failed."),
    ("inverse_planning",
     "And the eighth: people infer goals from movement as a Bayesian observer of a rational planner would. "
     "<bookmark mark='a'/> The original: Baker, Saxe and Tenenbaum, 2009. <bookmark mark='b'/> The record: the food "
     "trucks of 2017. <bookmark mark='c'/> Replicated within the programme that built it, and extended; independent "
     "tests are fewer. <bookmark mark='d'/> Replicated."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def row(self, key, text):
        card = ledger_card(self._get(key), width=12.8, font_size=21)
        with self.voiceover(text) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 35 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 4, "failed": 3, "contested": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ reading attitudes into forced acts, \ seeing ourselves in others, \ rating ourselves "
             r"above average, \ and reading goals from movement", GOOD),
            (r"what failed: \ the choice effect in dissonance, \ the elderly walk and power posing's hormones", AUTH),
            (r"what is argued: \ why the unskilled misjudge themselves", YOU),
            (r"the failures share a shape: \ small samples, \ large effects on distant behaviour, \ and loose "
             r"measures", MODEL),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: reading attitudes into forced acts, seeing ourselves in "
            "others, rating ourselves above average, and reading goals from movement. <bookmark mark='b'/> What "
            "failed: the choice effect in dissonance, the elderly walk, and power posing's hormones. "
            "<bookmark mark='c'/> What's argued: why the unskilled misjudge themselves. <bookmark mark='d'/> The "
            "failures share a shape. Small samples, large effects on distant behaviour, and loose measures. The "
            "findings that held were about judgments people make, measured as judgments."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
