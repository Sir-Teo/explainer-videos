from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Goals(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Goals", r"Does ``do your best'' get people's best?")
        self.older()
        self.theory()
        self.limits()

    def older(self):
        head = heading(r"Two older theories of work motivation")
        left = theory_card(r"Two factors", r"Frederick Herzberg, \ 1959",
                           r"pay, \ conditions and supervision can only remove dissatisfaction; \ achievement, \ "
                           r"recognition and the work itself motivate", r"the split came from the method", "failed",
                           width=6.1, font_size=19, color=PERSON)
        right = theory_card(r"Expectancy", r"Victor Vroom, \ 1964",
                            r"effort follows expectancy, \ times instrumentality, \ times valence: \ can I do it, \ "
                            r"will it pay, \ do I want what it pays", r"modest correlations; \ the product adds little",
                            "replicated, smaller", width=6.1, font_size=19, color=MODEL)
        VGroup(left, right).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to([0, 0.3, 0])
        eq = MathTex(r"F = E \times \sum (I \times V)", font_size=34, color=MODEL).next_to(right, DOWN, buff=0.3)
        tag = published_tag(r"Herzberg, \ Mausner \& Snyderman (1959); \ Vroom (1964); \ Van Eerde \& Thierry (1996)")
        with self.voiceover(
            "Most textbooks still teach two older theories first. <bookmark mark='a'/> In 1959 Frederick Herzberg "
            "and colleagues asked engineers and accountants to describe times they had felt especially good or "
            "especially bad about their jobs. The good times were about achievement, recognition and the work "
            "itself; the bad times about pay, supervision and conditions. So, Herzberg concluded, the two are "
            "separate: hygiene factors can only remove dissatisfaction, and only motivators motivate. "
            "<bookmark mark='b'/> The split did not survive other methods. Asked the same way, people credit "
            "themselves for good events and their circumstances for bad ones, the self-serving bias of Part 35, "
            "and with other measures the two lists overlap. <bookmark mark='c'/> In 1964 Victor Vroom wrote "
            "motivation as a product: effort follows the expectancy that trying leads to performing, times the "
            "chance that performing pays, times how much the pay is wanted. <bookmark mark='d'/> When Wendelien Van "
            "Eerde and Henk Thierry pooled the tests in 1996, each part correlated modestly with effort and "
            "performance, and multiplying them added little. Goal setting, which follows, has the stronger record."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left.box), FadeIn(left.name), FadeIn(left.claim))
            vo.wait_until("b")
            self.play(FadeIn(left.verdict), FadeIn(left.status))
            vo.wait_until("c")
            self.play(FadeIn(right.box), FadeIn(right.name), FadeIn(right.claim), Write(eq))
            vo.wait_until("d")
            self.play(FadeIn(right.verdict), FadeIn(right.status))
        self.clear_scene()

    def theory(self):
        rows_section(self, r"Goal-setting theory", [
            (r"Edwin Locke and Gary Latham, \ from the 1960s: \ specific, \ difficult goals lead to higher performance "
             r"than ``do your best''", WHITE),
            (r"hundreds of studies, \ in laboratories and workplaces, \ found the effect: \ one of the most replicated "
             r"in work psychology", GOOD),
            (r"how it works: \ a goal directs attention, \ raises effort, \ sustains persistence and prompts "
             r"strategies (Part 28's motivation)", MODEL),
            (r"it needs commitment and feedback: \ a goal no one accepts, \ or progress no one can see, \ does "
             r"little", PERSON),
        ], "Does do your best get people's best? <bookmark mark='a'/> From the nineteen sixties, Edwin Locke and Gary "
           "Latham found that specific, difficult goals lead to higher performance than do your best. "
           "<bookmark mark='b'/> Hundreds of studies, in laboratories and workplaces, found the effect. It's one of "
           "the most replicated results in work psychology. <bookmark mark='c'/> A goal directs attention, raises "
           "effort, sustains persistence, and prompts people to look for strategies: Part 28's motivation, at work. "
           "<bookmark mark='d'/> But it needs commitment and feedback. A goal no one accepts, or progress no one can "
           "see, does little.", tag=published_tag(r"Locke \& Latham (2002)"))

    def limits(self):
        chips_section(self, r"When goals go wrong", [
            (r"complex tasks", r"a hard performance goal on a task people have not yet learned can hurt: \ set "
                               r"learning goals first", AUTH),
            (r"narrow targets", r"what is counted improves; \ what is not counted can be neglected or gamed "
                                r"(Goodhart's law)", PERSON),
            (r"cheating", r"people just short of a goal are more likely to misreport (Schweitzer and colleagues)", MODEL),
            (r"the design", r"several goals, \ including quality, \ with honest measurement and room to learn", GOOD),
        ], "Goals can also go wrong. <bookmark mark='a'/> A hard performance goal on a task people haven't learned "
           "yet can hurt. Set learning goals first. <bookmark mark='b'/> What's counted improves, and what isn't "
           "counted can be neglected or gamed. That's Goodhart's law. <bookmark mark='c'/> People just short of a "
           "goal are more likely to misreport, as Maurice Schweitzer and colleagues found. <bookmark mark='d'/> So "
           "design several goals, including quality, with honest measurement and room to learn.")
