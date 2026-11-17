from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.question()

    def card(self):
        card = chapter_card(14, r"In practice: \ surveys, \ tests and people analytics",
                            r"Where do latent variables earn their keep?", lit=(), part=PART,
                            scale=("person", "group", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: surveys, tests and people analytics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where the models work")
        data = (
            (r"test validation", r"a new questionnaire's factor structure confirmed in a fresh sample, \ with its "
                                 r"reliability from the loadings", MODEL),
            (r"surveys across countries", r"invariance tested before an engagement or wellbeing score is ranked "
                                          r"across countries, \ languages or groups", SYMP),
            (r"people analytics", r"engagement, \ burnout and intention to leave as latent variables, \ with "
                                  r"measurement error modelled, \ not ignored", PERSON),
            (r"marketing", r"satisfaction, \ trust and loyalty models of customers; \ attitude models in "
                           r"advertising", GOOD),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=4.0), wrapped_label(how, 7.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Where these models earn their keep. <bookmark mark='a'/> Test validation: a new questionnaire's factor "
            "structure confirmed in a fresh sample, with its reliability from the loadings. <bookmark mark='b'/> "
            "Surveys across countries: invariance tested before an engagement or wellbeing score is ranked across "
            "countries, languages or groups. <bookmark mark='c'/> People analytics: engagement, burnout and intention "
            "to leave as latent variables, with measurement error modelled rather than ignored. "
            "<bookmark mark='d'/> And marketing: models of customer satisfaction, trust and loyalty, and of attitudes "
            "in advertising."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"The question to ask")
        q = wrapped_label(r"What other diagram fits these data equally well, \ and what would tell them apart?", 11.0,
                          32, YOU).move_to([0, 1.2, 0])
        rows = rows_of([
            (r"a dashboard that says engagement ``drives'' retention has drawn one arrow of several that fit", AUTH),
            (r"a score compared across teams or countries needs scalar invariance first", MODEL),
            (r"the cheapest answer is often an experiment: \ change one thing for some teams, \ and watch", GOOD),
        ], 12.0, 22, 0.42).move_to([0, -1.3, 0])
        with self.voiceover(
            "In every one of these settings, one question does the most work. <bookmark mark='a'/> What other diagram "
            "fits these data equally well, and what would tell them apart? <bookmark mark='b'/> A dashboard that says "
            "engagement drives retention has drawn one arrow of several that fit. <bookmark mark='c'/> A score "
            "compared across teams or countries needs scalar invariance first. <bookmark mark='d'/> And the cheapest "
            "answer is often an experiment: change one thing for some teams, and watch."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
