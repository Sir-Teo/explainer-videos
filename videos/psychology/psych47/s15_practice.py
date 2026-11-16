from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()

    def card(self):
        card = chapter_card(14, r"In practice: \ users, \ patients and dashboards", r"Whose behaviour does the number "
                            r"describe?", lit=(), part=PART, scale=("person", "group"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: users, patients and dashboards."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"The same question, \ everywhere")
        data = (
            (r"product metrics", r"users who use a feature more are more engaged; \ does using it make a user more "
                                 r"engaged? \ only within-user data, \ or an experiment, \ can say", MODEL),
            (r"experiments", r"randomize users, \ but analyse at the level randomized; \ sessions from one user are not "
                             r"independent, \ and many tests treat them as if they were", AUTH),
            (r"personalized health", r"wearables record one person for months: \ enough for that person's own "
                                     r"model, \ if the question is about them", GOOD),
            (r"learning and coaching", r"advice read off a cross-section (``people who sleep more score higher'') is "
                                       r"advice about people, \ not about you", PERSON),
            (r"items and prompts", r"any test of a few hand-picked stimuli, \ prompts or scenarios is a sample of "
                                   r"them: \ include them as random, \ or narrow the claim", SYMP),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=16, width=3.4), wrapped_label(how, 9.0, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "The question of this part runs through practice. <bookmark mark='a'/> Product metrics: users who use a "
            "feature more are more engaged. Does using it make a user more engaged? Only within-user data, or an "
            "experiment, can say. <bookmark mark='b'/> Experiments: randomize users, and analyse at the level "
            "randomized. Sessions from one user aren't independent, and many tests treat them as if they were. "
            "<bookmark mark='c'/> Personalized health: a wearable records one person for months, enough for that "
            "person's own model, if the question is about them. <bookmark mark='d'/> Learning and coaching: advice "
            "read off a cross-section is advice about people, not about you. <bookmark mark='e'/> And items and "
            "prompts: any test with a few hand-picked stimuli, prompts or scenarios is a sample of them. Include them "
            "as random, or narrow the claim."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
