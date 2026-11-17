from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.drawer()

    def card(self):
        card = chapter_card(14, r"In practice: \ reviews, \ vendors and file drawers", r"Where is a literature weighed "
                            r"for a decision?", lit=(), part=PART, scale=("society",), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: reviews, vendors and file drawers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where a literature is weighed")
        items = [
            (r"evidence reviews", r"medicine and policy pool trials by protocol: \ search everything, \ including "
                                  r"registries and unpublished data, \ grade the certainty, \ and say why", SYMP),
            (r"due diligence", r"a vendor's ``proven by science'' claim: \ which studies, \ how many were run, \ who "
                               r"paid, \ and what the prediction interval says about your setting", AUTH),
            (r"guidelines", r"a recommendation should change when the pooled estimate shrinks; \ many lag a decade "
                            r"behind their evidence", MODEL),
            (r"journalism", r"one new study is one study: \ report where it sits in the funnel", PERSON),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=3.6), wrapped_label(what, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Where is a literature weighed for a decision? <bookmark mark='a'/> In evidence reviews, medicine and "
            "policy pool trials by protocol: search everything, including registries and unpublished data, grade the "
            "certainty, and say why. <bookmark mark='b'/> In due diligence on a vendor's claim that something is "
            "proven by science: which studies, how many were run, who paid, and what the prediction interval says "
            "about your own setting. <bookmark mark='c'/> In guidelines, which should change when the pooled estimate "
            "shrinks, and often lag years behind their evidence. <bookmark mark='d'/> And in journalism, where one new "
            "study is one study, and the story is where it sits in the funnel."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def drawer(self):
        head = heading(r"Your own file drawer")
        rows = rows_of([
            (r"a company runs hundreds of experiments a year; \ the ones that win are presented, \ the rest forgotten",
             WHITE),
            (r"the archive of winners is a filtered literature: \ its average lift is inflated, \ exactly as in "
             r"chapter one", AUTH),
            (r"keep every experiment, \ with its pre-stated metric and its result, \ in one searchable register", GOOD),
            (r"then pool them, \ shrink the winners toward the base rate (Part 48's hierarchy), \ and re-test the "
             r"biggest before building on them", MODEL),
            (r"the denominator is the cure here too", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Every organization has its own file drawer. <bookmark mark='a'/> A company runs hundreds of experiments "
            "a year. The ones that win are presented, and the rest are forgotten. <bookmark mark='b'/> That archive "
            "of winners is a filtered literature. Its average lift is inflated, exactly as in the opening. "
            "<bookmark mark='c'/> So keep every experiment, with its pre-stated metric and its result, in one "
            "searchable register. <bookmark mark='d'/> Then pool them, shrink the winners toward the base rate with "
            "Part 48's hierarchy, and test the biggest again before building on them. <bookmark mark='e'/> The "
            "denominator is the cure here too."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
