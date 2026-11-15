from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_stimulation()
        self.row_overjustification()
        self.row_goals()
        self.row_depletion()
        self.row_delay()
        self.row_grit()
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until("a")
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until("b")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until("c")
        self.play(FadeIn(card.note))
        vo.wait_until("d")
        self.play(FadeIn(card.status, scale=1.3))

    def row_stimulation(self):
        card = ledger_card(self._get("brain_stimulation_reward"), width=12.8, font_size=23)
        with self.voiceover(
            "Six new rows today. The first: animals will work for electrical stimulation of certain brain sites, "
            "often in preference to food. <bookmark mark='a'/> The original: Olds and Milner, 1954. "
            "<bookmark mark='b'/> The record: Olds's map of reward sites in 1958, Routtenberg and Lindy's rats that "
            "chose stimulation over food in 1965, and a standard laboratory method ever since. "
            "<bookmark mark='c'/> One of the most reproduced findings in behavioural neuroscience. What changed is "
            "what it means: wanting, not pleasure. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_overjustification(self):
        card = ledger_card(self._get("overjustification"), width=12.8, font_size=22)
        with self.voiceover(
            "The second: an expected, tangible reward for something people already enjoy reduces how much they "
            "choose to do it later. <bookmark mark='a'/> The original: Lepper, Greene and Nisbett's markers, 1973. "
            "<bookmark mark='b'/> The record: Cameron and Pierce's meta-analysis finding little harm, Deci, Koestner and Ryan's hundred and twenty-eight experiments, and Cerasoli and colleagues' "
            "forty years of field data. <bookmark mark='c'/> Reliable in the laboratory under the conditions the "
            "meta-analyses specify; how much it matters outside is contested. <bookmark mark='d'/> Replicated, with "
            "its scope argued."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_goals(self):
        card = ledger_card(self._get("goal_setting"), width=12.8, font_size=22)
        with self.voiceover(
            "The third: specific, difficult goals lead to better performance than do your best. "
            "<bookmark mark='a'/> The original: Locke, 1968. <bookmark mark='b'/> The record: Mento, Steel and "
            "Karren's meta-analysis in 1987, Locke and Latham's review of hundreds of studies, Ordóñez and "
            "colleagues on the costs, and the meta-analysis of if-then plans. <bookmark mark='c'/> Robust in the "
            "laboratory and the field, smaller for complex new tasks, and with costs when goals are narrow. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_depletion(self):
        card = ledger_card(self._get("ego_depletion"), width=12.8, font_size=22)
        with self.voiceover(
            "The fourth: exerting self-control on one task impairs it on the next, as if a resource were used up. "
            "<bookmark mark='a'/> The original: Baumeister and colleagues' radishes, 1998. <bookmark mark='b'/> The "
            "record: a meta-analysis of a hundred and ninety-eight tests in 2010; bias corrections near zero in "
            "2015; twenty-three laboratories finding point oh four in 2016; and a second multisite test, with tasks "
            "the proponents chose, close to zero in 2021. <bookmark mark='c'/> Fatigue after effort is real. A "
            "limited resource is not supported. <bookmark mark='d'/> Failed, in its sequential-task form."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_delay(self):
        card = ledger_card(self._get("delay_of_gratification"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: how long a preschooler waits for a larger treat predicts achievement years later. "
            "<bookmark mark='a'/> The original: Shoda, Mischel and Peake, 1990. <bookmark mark='b'/> The record: "
            "Kidd and colleagues' reliable and unreliable adults, McGuire and Kable's rational giving up, and Watts, "
            "Duncan and Quan's nine hundred children. <bookmark mark='c'/> The association exists, but it's small, "
            "and largely shared with family background and early ability. <bookmark mark='d'/> Replicated, "
            "smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_grit(self):
        card = ledger_card(self._get("grit"), width=12.8, font_size=23)
        with self.voiceover(
            "And the sixth: grit predicts achievement beyond conscientiousness. <bookmark mark='a'/> The original: "
            "Duckworth and colleagues, 2007. <bookmark mark='b'/> The record: a twin study in 2016 finding that grit "
            "added little beyond the Big Five, and Credé's meta-analysis in 2017. <bookmark mark='c'/> Grit predicts "
            "modestly and is nearly conscientiousness. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 28 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "failed": 1, "replicated, smaller": 1, "contested": 1}
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=20, width=2.8)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 22, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-3.3, 0.2, 0])
        rows_ = rows_of([
            (r"the mechanisms replicate: \ brain-stimulation reward, \ undermining rewards, \ goals", GOOD),
            (r"the self-control stories shrink or fail: \ a resource that runs out, \ a test that predicts a "
             r"life, \ a trait with a new name", LOST),
            (r"the survivors are effects measured in experiments; \ the casualties were claims about people, \ "
             r"from small samples", WANT),
        ], 5.6, 23, 0.36).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> The mechanisms replicate: brain-stimulation reward, rewards that "
            "undermine interest, and goals that work. <bookmark mark='b'/> The self-control stories shrank or "
            "failed: a resource that runs out, a test at four that predicts a life, and a trait that turned out to "
            "be an old one with a new name. <bookmark mark='c'/> The survivors are effects measured inside "
            "experiments. The casualties were broad claims about people, built on small samples."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
