from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.cohorts()
        self.causes()
        self.ageing()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ cohorts, \ causes and ageing", r"What is open?",
                            lit={2013: r"epigenetic clocks", 2016: r"target trials", 2018: r"ABCD"}, part=PART,
                            scale=("brain", "person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: cohorts, causes and ageing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cohorts(self):
        head = heading(r"Following ten thousand children")
        rows = rows_of([
            (r"the Adolescent Brain Cognitive Development study: \ 11{,}880 children aged 9 and 10 invited at 21 "
             r"sites in the United States, \ followed into adulthood with repeated brain scans, \ tests and "
             r"interviews", WHITE),
            (r"its data are shared with researchers, \ and its size answers Part 8's warning: \ links between brain "
             r"and behaviour are small, \ and need thousands of people", AGE),
            (r"but a cohort is still a cohort: \ every finding is about children born around 2007, \ growing up in "
             r"their period", COHORT),
            (r"and it is observational: \ a correlation in ten thousand children is precise, \ not causal", LOST),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Casey et al.\ (2018)")
        with self.voiceover(
            "Three frontiers. The first is scale. <bookmark mark='a'/> The Adolescent Brain Cognitive Development "
            "study invited eleven thousand eight hundred and eighty children aged nine and ten at twenty-one sites "
            "across the United States, and follows them into adulthood with repeated brain scans, tests and "
            "interviews. <bookmark mark='b'/> Its data are shared with researchers, and its size answers Part 8's "
            "warning that links between brain and behaviour are small and need thousands of people. "
            "<bookmark mark='c'/> But a cohort is still a cohort. Every finding is about children born around 2007, "
            "growing up in their period. <bookmark mark='d'/> And it's observational. A correlation in ten "
            "thousand children is precise, not causal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def causes(self):
        head = heading(r"Causes from cohorts")
        items = [
            (r"within families", r"compare siblings: \ genes and home held partly fixed \ (birth order, \ the "
             r"Flynn reversal)", COHORT),
            (r"natural experiments", r"a rule that assigns as if at random: \ a school-entry cutoff, \ a "
             r"lottery for foster care", PERIOD),
            (r"target trials", r"write down the trial you would run, \ then emulate it with cohort data, \ "
             r"its assumptions stated", AGE),
        ]
        rows = VGroup()
        for name, txt, col in items:
            rows.add(VGroup(word_chip(name, color=col, font_size=22, width=3.6),
                            wrapped_label(txt, 8.2, 22, WHITE)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.2, 0])
        foot = wrapped_label(r"each trades the lottery's guarantee for an assumption that can be argued; \ Part 47 "
                             r"takes up people over time", 12.0, 22, YOU).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second frontier is getting causes out of cohorts, since lotteries are rare. "
            "<bookmark mark='a'/> Within-family designs compare siblings, holding genes and home partly fixed, as "
            "in the birth-order and Flynn-reversal studies. <bookmark mark='b'/> Natural experiments find a rule "
            "that assigns people as if at random: a school-entry cutoff, or a lottery for foster care. "
            "<bookmark mark='c'/> And target trial emulation writes down the randomized trial you would run, then "
            "imitates it with cohort data, with its assumptions stated. <bookmark mark='d'/> Each trades the "
            "lottery's guarantee for an assumption that can be argued. Part 47 takes up people over time."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def ageing(self):
        head = heading(r"Measuring, \ and changing, \ ageing")
        rows = rows_of([
            (r"ageing clocks: \ patterns of chemical marks on DNA, \ first shown by Steve Horvath in 2013, \ "
             r"predict chronological age closely; \ the gap between the two is studied as biological ageing", AGE),
            (r"the open question: \ does a clock measure ageing, \ or only correlate with it? \ Part 3's validity "
             r"question, \ in a new instrument", LOST),
            (r"multidomain trials like FINGER are now run in many countries with a shared design, \ so that their "
             r"results can be pooled", GOOD),
            (r"the outcome that matters, \ dementia, \ takes many years to observe: \ trials must use earlier "
             r"measures, \ and those must be validated against it", YOU),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "The third frontier is ageing itself. <bookmark mark='a'/> Ageing clocks use patterns of chemical marks "
            "on DNA. First shown by Steve Horvath in 2013, they predict chronological age closely, and the gap "
            "between the two is studied as biological ageing. <bookmark mark='b'/> The open question is whether a "
            "clock measures ageing or only correlates with it: Part 3's validity question, in a new instrument. "
            "<bookmark mark='c'/> Multidomain trials like FINGER are now run in many countries with a shared design, "
            "so that their results can be pooled. <bookmark mark='d'/> And the outcome that matters, dementia, takes "
            "many years to observe, so trials use earlier measures, which must themselves be validated against it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"which early experiences open or close windows in people, \ and which only seem to because of who "
             r"receives them?", CHILD),
            (r"can the effects of early programmes be predicted from what changes first, \ or only seen decades "
             r"later?", CARE),
            (r"how much of cognitive ageing is the passage of time, \ and how much the diseases that come with "
             r"it?", OLD),
            (r"what is the Flynn effect made of, \ and what is reversing it?", COHORT),
        ], 12.4, 26, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four open questions. <bookmark mark='a'/> Which early experiences open or close windows in people, and "
            "which only seem to, because of who receives them? <bookmark mark='b'/> Can the effects of early "
            "programmes be predicted from what changes first, or only seen decades later? <bookmark mark='c'/> How "
            "much of cognitive ageing is the passage of time, and how much the diseases that come with it? "
            "<bookmark mark='d'/> And what is the Flynn effect made of, and what is reversing it?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
