from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.two_men()
        self.third_fact()
        self.question()
        self.objectives()

    def two_men(self):
        head = heading(r"1904: \ two men, \ one number")
        left = VGroup(label(r"Charles Spearman", font_size=30, color=G),
                      label(r"England", font_size=20, color=GREY_B),
                      wrapped_label(r"schoolchildren's marks in Classics, \ French, \ English and Mathematics, \ and "
                                    r"their skill at telling two tones apart", 5.6, 22, WHITE),
                      wrapped_label(r"every ability correlated with every other: \ he proposed one general factor, "
                                    r"\ and invented factor analysis to measure it", 5.6, 22, G))
        left.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        right = VGroup(label(r"Alfred Binet", font_size=30, color=VERB),
                       label(r"Paris", font_size=20, color=GREY_B),
                       wrapped_label(r"asked by the Ministry of Public Instruction for a way to find children who "
                                     r"would need special help at school", 5.6, 22, WHITE),
                       wrapped_label(r"with Th\'eodore Simon, \ a scale of tasks of rising difficulty, \ published "
                                     r"in 1905; \ in 1909 he protested against the ``brutal pessimism'' of calling a "
                                     r"child's intelligence fixed", 5.6, 22, VERB))
        right.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, -0.1, 0])
        tag = historical_tag(r"Spearman (1904); \ Binet \& Simon (1905)")
        with self.voiceover(
            "In 1904 two men, working separately, put a number on the mind. <bookmark mark='a'/> In England, "
            "Charles Spearman collected schoolchildren's marks in Classics, French, English and Mathematics, and "
            "tested how finely they could tell two tones apart. Every ability correlated with every other. He "
            "proposed that one general factor ran through them all, and invented factor analysis to measure it. "
            "<bookmark mark='b'/> In Paris, the Ministry of Public Instruction asked Alfred Binet for a way to find "
            "the children who would need special help at school. With Theodore Simon he built a scale of tasks of "
            "rising difficulty, published in 1905. And in 1909 he protested against what he called the brutal "
            "pessimism of declaring a child's intelligence fixed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in left], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in right], lag_ratio=0.5), run_time=3.0)
        self.clear_scene()

    def third_fact(self):
        head = heading(r"Within twenty years")
        rows = rows_of([
            (r"the mathematics is beautiful: \ a correlation matrix explained by a single column of numbers", G),
            (r"the test predicts: \ school results, \ jobs and health, \ better than most measures psychology has", GOOD),
            (r"and within twenty years, \ in the United States, \ test scores were being used to justify sterilizing "
             r"people: \ in 1927 the Supreme Court upheld it, \ eight votes to one", HARM),
            (r"all three facts are in this part", YOU),
        ], 12.4, 26, 0.45).move_to([0, -0.2, 0])
        tag = historical_tag(r"\emph{Buck v. Bell} (1927)")
        with self.voiceover(
            "Three facts belong together in this part. <bookmark mark='a'/> The mathematics is beautiful: a whole "
            "matrix of correlations explained by a single column of numbers. <bookmark mark='b'/> The test predicts: "
            "school results, jobs and health, better than most measures psychology has. <bookmark mark='c'/> And "
            "within twenty years, in the United States, test scores were being used to justify sterilizing people. "
            "In 1927 the Supreme Court upheld it, eight votes to one. <bookmark mark='d'/> All three facts are true, "
            "and all three are in this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ is there one thing that ``intelligence'' measures?")
        rows = rows_of([
            (r"the positive manifold, \ in Spearman's table and in a real test battery, \ recomputed", G),
            (r"factor analysis derived, \ one factor or many, \ and three worlds that make the same correlations", MODEL),
            (r"the IQ scale, \ what it predicts, \ what it rests on, \ and how scores change", VERB),
            (r"group differences, \ the history of harm, \ and other ``intelligences''", HARM),
        ], 12.4, 27, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "So this part asks whether there is one thing that the word intelligence measures. "
            "<bookmark mark='a'/> We'll start with the positive manifold, in Spearman's own table and in a real test "
            "battery, recomputed. <bookmark mark='b'/> Then we'll derive factor analysis, ask whether there's one "
            "factor or many, and build three different worlds that produce the same correlations. "
            "<bookmark mark='c'/> Then the IQ scale itself, what it predicts, what it rests on, and how scores "
            "change. <bookmark mark='d'/> And then group differences, handled with care, the history of harm, and "
            "the other intelligences people have proposed."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 32", font_size=34, color=GREY_B), label(r"Intelligence", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the positive manifold, \ from Spearman's 1904 table and Holzinger and Swineford's 301 children",
            r"the factor model derived: \ loadings, \ tetrads, \ one factor against three, \ the hierarchy",
            r"common cause, \ sampling and mutualism: \ the same correlations from different worlds",
            r"the IQ scale, \ its error, \ its validity, \ and range restriction",
            r"heritability, \ schooling and the Flynn effect; \ group differences and measurement invariance",
            r"the history of harm, \ and the replication record of eight claims",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 32 of Psychology, Built: intelligence, and the first part of Act Eight, on how people "
            "differ. <bookmark mark='a'/> We'll recompute the positive manifold from Spearman's 1904 table and from "
            "Holzinger and Swineford's three hundred and one children. We'll derive the factor model, with loadings "
            "and tetrads, and test one factor against three. We'll build a common cause, a sampling world and a "
            "mutualism world that all make the same correlations. We'll take apart the IQ scale, its error, its "
            "validity, and the statistics of range restriction. We'll weigh heritability, schooling and the Flynn "
            "effect, and treat group differences through measurement invariance. And we'll face the history of "
            "harm, and enter the replication record of eight claims."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
