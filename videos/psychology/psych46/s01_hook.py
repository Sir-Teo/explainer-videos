from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.crimes()
        self.idea()
        self.question()
        self.objectives()

    def crimes(self):
        head = heading(r"Which is worse?")
        pairs = (
            (r"arson", r"burglary"), (r"forgery", r"smuggling"), (r"vagrancy", r"bootlegging"),
        )
        cards = VGroup()
        for a, b in pairs:
            cards.add(VGroup(word_chip(a, color=PERSON, font_size=20, width=2.8), label(r"or", font_size=18, color=GREY_B),
                             word_chip(b, color=SYMP, font_size=20, width=2.8)).arrange(RIGHT, buff=0.3))
        cards.arrange(DOWN, buff=0.35).move_to([-3.3, 0.4, 0])
        rows = rows_of([
            (r"1927: \ Louis Thurstone asks students, \ for every pair of offences, \ which is the more serious", WHITE),
            (r"no one can say how serious arson is on a scale; \ everyone can say which of two is worse", PERSON),
            (r"people disagree, \ and the same person may disagree with themselves: \ the inconsistency is the "
             r"information", MODEL),
            (r"from the proportions who choose each side, \ Thurstone derives a scale of seriousness", GOOD),
        ], 6.0, 20, 0.4).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Thurstone (1927)")
        with self.voiceover(
            "In 1927 Louis Thurstone, in Chicago, gave students a list of offences. <bookmark mark='a'/> For every "
            "pair, which is the more serious? <bookmark mark='b'/> No one can say how serious arson is on a scale. But "
            "everyone can say which of two offences is worse. <bookmark mark='c'/> People disagree, and the same "
            "person may not answer the same way twice. Thurstone saw that the inconsistency is the information. "
            "<bookmark mark='d'/> From the proportions who choose each side, he derived a scale of seriousness: a "
            "number for something that has no units."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.3), run_time=2.0)
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def idea(self):
        head = heading(r"From a choice to a number")
        steps = VGroup()
        for yr, txt, c in (
                (r"1927", r"Thurstone: \ each option evokes a fluctuating impression; \ choices follow the larger", PERSON),
                (r"1959", r"Luce: \ one axiom about choice, \ and a ratio scale follows", MODEL),
                (r"1974", r"McFadden: \ the same model predicts how people will travel, \ and later wins a Nobel "
                          r"Prize in economics", GOOD),
                (r"1982", r"a decoy no one picks changes what people pick: \ the axiom fails, \ and preferences bend "
                          r"with the menu", AUTH)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=18, width=1.6), wrapped_label(txt, 10.0, 21, WHITE))
                      .arrange(RIGHT, buff=0.4))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "From those comparisons grew a whole science of choice. <bookmark mark='a'/> Thurstone: each option "
            "evokes a fluctuating impression, and the choice follows the larger. <bookmark mark='b'/> In 1959 Duncan "
            "Luce replaced the impressions with a single axiom about choice. <bookmark mark='c'/> In 1974 Daniel "
            "McFadden used the same model to predict how people would travel, work that later won a Nobel Prize in "
            "economics. <bookmark mark='d'/> And in 1982 a decoy that no one picks was shown to change what people "
            "do pick. The axiom fails, and preferences bend with the menu."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how do you turn a preference into a number?")
        rows = rows_of([
            (r"paired comparisons, \ Thurstone's law and Luce's axiom", SYMP),
            (r"random utility, \ the logit, \ and where it fails", MODEL),
            (r"decoys, \ compromises and conjoint analysis", PERSON),
            (r"what happens between a survey question and its answer", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how to turn I prefer this one into a number, and what happens between a question and "
            "its answer. <bookmark mark='a'/> Paired comparisons, Thurstone's law and Luce's axiom. "
            "<bookmark mark='b'/> Random utility, the logit, and where it fails. <bookmark mark='c'/> Decoys, "
            "compromises, and the conjoint studies that price products. <bookmark mark='d'/> And what happens "
            "between a survey question and its answer."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 46", font_size=34, color=GREY_B), label(r"Scaling, \ Surveys and Choice", font_size=52))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Thurstone's Case V, \ derived and fitted",
            r"Luce's axiom and Bradley-Terry, \ by the MM algorithm",
            r"random utility: \ Gumbel noise gives the logit",
            r"the decoy and compromise effects, \ and a model of both",
            r"conjoint analysis: \ part-worths and willingness to pay",
            r"the survey response process, \ response styles and the NPS",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 46 of Psychology, Built: scaling, surveys and choice. <bookmark mark='a'/> We'll derive "
            "Thurstone's law and fit it to real preferences. We'll fit Luce's model by a simple algorithm that always "
            "climbs. We'll show that random utility with the right noise gives the logit. We'll build the decoy and "
            "compromise effects from one model. We'll run a conjoint study and price its attributes. And we'll follow "
            "a survey question to its answer, through response styles and the net promoter score."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
