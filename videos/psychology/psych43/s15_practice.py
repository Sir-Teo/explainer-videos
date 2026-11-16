from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.same()
        self.abtest()

    def card(self):
        card = chapter_card(14, r"In practice: \ decide before the data", r"Where else does this workflow apply?",
                            lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: decide before the data."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def same(self):
        head = heading(r"The same workflow, \ everywhere")
        data = (
            (r"product experiments", r"an A/B test names its metric, \ its minimum effect worth shipping and its "
                                     r"sample size before launch; \ peeking and metric-shopping are the forking paths",
             SYMP),
            (r"clinical trials", r"registration before the first patient, \ a statistical analysis plan, \ and "
                                 r"outcomes that cannot be switched afterwards", GOOD),
            (r"policy evaluation", r"pre-analysis plans for field experiments in economics and government", PERSON),
            (r"your own work", r"write the plan as code, \ run it on simulated data, \ freeze it, \ then look", YOU),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "This workflow isn't only for replications. <bookmark mark='a'/> A product experiment, an A/B test, names "
            "its metric, the smallest effect worth shipping, and its sample size before launch. Peeking at results and "
            "shopping among metrics are its forking paths. <bookmark mark='b'/> Clinical trials are registered before "
            "the first patient, with a statistical analysis plan and outcomes that can't be switched afterwards. "
            "<bookmark mark='c'/> Field experiments in economics and government use pre-analysis plans. "
            "<bookmark mark='d'/> And your own work: write the plan as code, run it on simulated data, freeze it, and "
            "only then look."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def abtest(self):
        a = load("abtest")
        head = heading(r"A product test, \ planned")
        eq = MathTex(r"n = \frac{(z_{0.975} + z_{0.8})^2\,\big(p_0(1 - p_0) + p_1(1 - p_1)\big)}{(p_1 - p_0)^2}",
                     font_size=34, color=MODEL).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"a shop converts 5\% of visitors; \ a new checkout is worth shipping only if it adds at least half a "
             r"percentage point", WHITE),
            (rf"two-sided 5\%, \ 80\% power: \ {num(a['n'])} visitors per arm, \ fixed before launch", MODEL),
            (rf"half the effect needs four times the people ({num(a['n_half'])}); \ double it, \ a quarter "
             rf"({num(a['n_double'])})", PERSON),
            (r"peeking daily and stopping at the first significant day is Part 4's optional stopping: \ plan the "
             r"looks, \ or use a sequential test built for them", AUTH),
            (r"the same plan as the replication: \ metric, \ smallest effect, \ sample size, \ analysis, \ then data",
             YOU),
        ], 12.4, 21, 0.36).move_to([0, -0.9, 0])
        tag = psyche_tag(r"two proportions, \ normal approximation")
        with self.voiceover(
            "Here's the same workflow in a product team. <bookmark mark='a'/> A shop converts five percent of its "
            "visitors. A new checkout is worth shipping only if it adds at least half a percentage point. "
            "<bookmark mark='b'/> At the usual error rates, that's about thirty-one thousand visitors per arm, fixed "
            "before launch. <bookmark mark='c'/> Half the effect needs four times the people. Double it, a quarter. "
            "<bookmark mark='d'/> Peeking every day and stopping at the first significant one is Part 4's optional "
            "stopping. Plan the looks, or use a sequential test built for them. <bookmark mark='e'/> It's the same "
            "plan as the replication: metric, smallest effect, sample size and analysis, and only then the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
