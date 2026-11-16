from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.hiring()
        self.testing()
        self.algorithms()

    def card(self):
        card = chapter_card(13, r"In practice: \ audits and structure", r"What should an organization actually do?",
                            lit=(), part=PART, scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: audits and structure."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hiring(self):
        head = heading(r"What to buy instead of a training")
        items = [
            (r"measure outcomes", r"audit your own process: \ callbacks, \ offers and promotions by group, \ "
             r"the way chapter six measured the market", GOOD),
            (r"structure decisions", r"the same questions and scoring for every candidate \ (Part 53); \ "
             r"criteria fixed before names are seen", IN),
            (r"remove the cue", r"where the name or photograph carries no information, \ hide it", PERSON),
            (r"evaluate the fix", r"a training, \ a policy or a nudge is a treatment: \ randomize it, \ and "
             r"measure behaviour, \ not just attitudes", MODEL),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.6), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, -0.2, 0])
        with self.voiceover(
            "What should an organization actually do? <bookmark mark='a'/> Measure outcomes. Audit your own process, "
            "callbacks, offers and promotions by group, the way chapter six measured the market. "
            "<bookmark mark='b'/> Structure decisions: the same questions and scoring for every candidate, as in "
            "Part 53, with criteria fixed before names are seen. <bookmark mark='c'/> Where a name or a photograph "
            "carries no information about the job, hide it. <bookmark mark='d'/> And treat every fix, a training, "
            "a policy or a nudge, as a treatment. Randomize it, and measure behaviour, not just attitudes."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def testing(self):
        head = heading(r"Paired testing")
        a = little_person(1.2, color=IN).move_to([-5.0, 0.8, 0])
        b = little_person(1.2, color=OUTG).move_to([-3.6, 0.8, 0])
        house = VGroup(Polygon([-4.9, -0.4, 0], [-3.7, -0.4, 0], [-4.3, 0.2, 0], color=GREY_B),
                       Rectangle(width=1.0, height=0.8, color=GREY_B).move_to([-4.3, -0.8, 0])).shift(DOWN * 0.6)
        rows = rows_of([
            (r"the audit idea is older than r\'esum\'es: \ pairs of testers matched on everything but group ask about "
             r"the same flat, \ the same loan, \ the same job", WHITE),
            (r"governments and fair-housing groups use paired tests to detect and document discrimination", CROWD),
            (r"what they measure is a difference in treatment, \ with the person held fixed by design", GOOD),
            (r"the limit: \ one pair is an anecdote; \ chapter six's power calculation says how many pairs a "
             r"conclusion needs", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        with self.voiceover(
            "The same logic runs outside hiring. <bookmark mark='a'/> Pairs of testers, matched on everything but "
            "their group, ask about the same flat, the same loan, the same job. <bookmark mark='b'/> Governments "
            "and fair-housing organizations use paired tests to detect and document discrimination. "
            "<bookmark mark='c'/> What they measure is a difference in treatment, with the person held fixed by "
            "design. <bookmark mark='d'/> The limit is the one from chapter six. One pair is an anecdote, and the "
            "power calculation says how many pairs a conclusion needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), FadeIn(house))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def algorithms(self):
        head = heading(r"Auditing an algorithm")
        rows = rows_of([
            (r"a model trained on past decisions learns their patterns, \ biased ones included: \ chapter eleven's "
             r"ladder, \ automated", WHITE),
            (r"an algorithm can be audited like an employer: \ send it matched inputs that differ only in group, \ "
             r"and compare the outputs", CROWD),
            (r"unlike a person, \ it can be tested on millions of matched cases, \ and changed by changing a rule", GOOD),
            (r"which definition of fairness to hold it to is a choice, \ and they conflict: \ the statistics series "
             r"takes that up", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "And the newest employer is software. <bookmark mark='a'/> A model trained on past decisions learns "
            "their patterns, biased ones included. It's chapter eleven's ladder, automated. "
            "<bookmark mark='b'/> But an algorithm can be audited like an employer: send it matched inputs that "
            "differ only in group, and compare the outputs. <bookmark mark='c'/> Unlike a person, it can be tested "
            "on millions of matched cases, and changed by changing a rule. <bookmark mark='d'/> Which definition "
            "of fairness to hold it to is a choice, and the definitions conflict. The statistics series takes that "
            "up."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
