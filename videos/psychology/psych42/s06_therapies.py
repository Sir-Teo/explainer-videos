from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Therapies(VoiceoverScene):
    def construct(self):
        self.card()
        self.families()
        self.dbt()

    def card(self):
        card = chapter_card(5, r"The therapies", r"What do therapists actually do?",
                            lit={1967: r"Beck", 1991: r"Linehan et al."}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter five. The therapies."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def families(self):
        head = heading(r"Four families")
        data = (
            (r"behavioural", r"change what is done: \ exposure, \ activation, \ reinforcement (Parts 16 and 40)", GOOD),
            (r"cognitive", r"Beck's cognitive therapy: \ notice, \ test and revise the thoughts that keep distress "
                           r"going", SYMP),
            (r"third wave", r"acceptance and commitment therapy, \ mindfulness-based cognitive therapy: \ change one's "
                            r"relation to thoughts, \ not their content", MODEL),
            (r"psychodynamic", r"patterns from the past repeated in relationships, \ worked through in the "
                               r"relationship with the therapist; \ fewer trials, \ some of them positive", PERSON),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.4), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.1, 0])
        foot = wrapped_label(r"most trials test cognitive behavioural therapy, \ so its evidence is the largest: \ "
                             r"more evidence is not the same as more effect", 12.0, 20, YOU).move_to([0, -2.7, 0])
        with self.voiceover(
            "The therapies come in four families. <bookmark mark='a'/> Behavioural therapies change what's done: "
            "exposure, activation, reinforcement, from Parts 16 and 40. <bookmark mark='b'/> Cognitive therapy, "
            "Aaron Beck's, has people notice, test and revise the thoughts that keep distress going. "
            "<bookmark mark='c'/> The third wave, acceptance and commitment therapy and mindfulness-based cognitive "
            "therapy, changes a person's relation to their thoughts, not their content. <bookmark mark='d'/> And "
            "psychodynamic therapy works on patterns from the past repeated in relationships, including the one with "
            "the therapist. It has fewer trials, some of them positive. <bookmark mark='e'/> Most trials test "
            "cognitive behavioural therapy, so its evidence is the largest. More evidence isn't the same as more "
            "effect."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def dbt(self):
        head = heading(r"A therapy built for self-harm")
        rows = rows_of([
            (r"Linehan, \ 1991: \ dialectical behaviour therapy for women with borderline personality disorder and "
             r"repeated self-harm: \ acceptance and change, \ skills groups, \ and phone coaching", WHITE),
            (r"against treatment as usual for a year, \ fewer and less severe acts of self-harm, \ and fewer days in "
             r"hospital", GOOD),
            (r"Linehan and colleagues, \ 2006: \ against treatment by community experts, \ about half the rate of "
             r"suicide attempts", SYMP),
            (r"later meta-analyses find smaller effects; \ the Ledger marks it replicated", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Linehan et al.\ (1991); \ Linehan et al.\ (2006)")
        with self.voiceover(
            "One therapy was built for a problem other therapies struggled with. <bookmark mark='a'/> In 1991 Marsha "
            "Linehan described dialectical behaviour therapy, for women with borderline personality disorder and "
            "repeated self-harm. It combines acceptance with change, skills groups, and coaching between sessions. "
            "<bookmark mark='b'/> Against treatment as usual for a year, it brought fewer and less severe acts of "
            "self-harm, and fewer days in hospital. <bookmark mark='c'/> In 2006, against treatment by experienced "
            "community therapists, the rate of suicide attempts was about halved. <bookmark mark='d'/> Later "
            "meta-analyses find smaller effects, and the Ledger marks it replicated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
