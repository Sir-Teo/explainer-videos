from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.licenses()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ what a failure licenses", r"What does a failed replication show?",
                            lit={2016: r"Van Bavel et al.", 2020: r"Nosek \& Errington"}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter fifteen. Frontier: what a failure licenses."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def licenses(self):
        head = heading(r"What a failure licenses")
        rows = rows_of([
            (r"Nosek and Errington, \ 2020: \ a replication is a study whose outcome would count as evidence about "
             r"a claim; \ what it shows depends on the theory that says the two studies are the same", WHITE),
            (r"hidden moderators: \ a failure might mean the effect depends on a setting; \ Many Labs 2 found little "
             r"variation for most effects, \ so the burden is on whoever names the moderator", AUTH),
            (r"replication at scale: \ many small labs running one protocol, \ as here, \ give power no single lab "
             r"has", GOOD),
            (r"a failed replication licenses less confidence in a claim, \ not the claim's opposite", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Nosek \& Errington (2020); \ Van Bavel et al.\ (2016)")
        with self.voiceover(
            "What does a failed replication license? <bookmark mark='a'/> In 2020 Brian Nosek and Timothy Errington "
            "defined a replication as a study whose outcome would count as evidence about a claim. What it shows "
            "depends on the theory that says the two studies are the same. <bookmark mark='b'/> Hidden moderators: a "
            "failure might mean the effect depends on a setting. But Many Labs 2 found little variation across "
            "settings for most effects, so the burden is on whoever names the moderator. <bookmark mark='c'/> "
            "Replication at scale: many small labs running one protocol, as here, give power that no single lab has. "
            "<bookmark mark='d'/> And a failed replication licenses less confidence in a claim, not the claim's "
            "opposite."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"which findings deserve the cost of a multi-lab replication, \ and who decides?", SYMP),
            (r"when is a conceptual replication worth more than a direct one?", MODEL),
            (r"can theory say in advance which differences between two studies matter?", PERSON),
            (r"will registered reports change which questions get asked, \ or only how they are answered?", GOOD),
            (r"what would make a field's findings trustworthy without replicating each one?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. Which findings deserve the cost of a multi-lab replication, and who decides? "
            "<bookmark mark='b'/> When is a conceptual replication worth more than a direct one? <bookmark mark='c'/> "
            "Can theory say in advance which differences between two studies matter? <bookmark mark='d'/> Will "
            "registered reports change which questions get asked, or only how they're answered? <bookmark mark='e'/> "
            "And what would make a field's findings trustworthy without replicating each one?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
