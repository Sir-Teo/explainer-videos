from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.markets()
        self.dating()

    def card(self):
        card = chapter_card(13, r"In practice: \ markets, \ teams and dating apps", r"Who uses these findings, \ and how?",
                            lit=(), part=PART, scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: markets, teams and dating apps."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def markets(self):
        head = heading(r"Designing for cooperation")
        items = [
            (r"reputation systems", r"marketplaces between strangers run on ratings: \ reputation, \ chapter three's "
             r"third route, \ made visible", PERSON),
            (r"repeat play", r"cooperation is easier when people expect to meet again: \ long relationships with "
             r"suppliers, \ stable teams", CROWD),
            (r"sanctions", r"punishment sustains contributions only if it is trusted to hit free riders, \ not "
             r"whoever is unpopular \ (chapter four)", AUTH),
            (r"fair splits", r"offers people see as unfair are refused even at a cost: \ in pay, \ pricing and "
             r"negotiation, \ perceived fairness is part of the deal", GOOD),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.6), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, -0.2, 0])
        with self.voiceover(
            "The games are tools for design. <bookmark mark='a'/> Marketplaces between strangers run on ratings. "
            "That's reputation, chapter three's third route, made visible. <bookmark mark='b'/> Cooperation is "
            "easier when people expect to meet again, which favours long relationships with suppliers, and stable "
            "teams. <bookmark mark='c'/> Sanctions sustain contributions only if they're trusted to hit free riders, "
            "not whoever is unpopular. <bookmark mark='d'/> And offers people see as unfair get refused, even at a "
            "cost. In pay, pricing and negotiation, perceived fairness is part of the deal."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dating(self):
        head = heading(r"What a matching algorithm can know")
        rows = rows_of([
            (r"dating products often claim to find compatible partners from questionnaires", WHITE),
            (r"chapter eight: \ questionnaires predict how choosy a person is and how desired, \ not the chemistry "
             r"of a particular pair", AUTH),
            (r"what such a service can do is put people in front of others likely to be interested at all, \ and "
             r"let them meet: \ proximity and exposure, \ chapter seven", GOOD),
            (r"and couple therapy, \ like any treatment, \ should be judged by randomized trials, \ not by how well a "
             r"theory fits the couples it was built on", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "And then there are the dating products. <bookmark mark='a'/> Many claim to find compatible partners "
            "from questionnaires. <bookmark mark='b'/> But chapter eight showed that questionnaires predict how "
            "choosy a person is, and how desired, not the chemistry of a particular pair. "
            "<bookmark mark='c'/> What such a service can do is put people in front of others likely to be "
            "interested at all, and let them meet. That's proximity and exposure, chapter seven. "
            "<bookmark mark='d'/> And couple therapy, like any treatment, should be judged by randomized trials, "
            "not by how well a theory fits the couples it was built on."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
