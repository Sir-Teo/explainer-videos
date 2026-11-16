from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Dopamine(VoiceoverScene):
    def construct(self):
        self.card()
        self.discovery()
        self.binding()
        self.revised()

    def card(self):
        card = chapter_card(3, r"Dopamine", r"What do antipsychotics act on?",
                            lit={1952: r"chlorpromazine", 1976: r"Seeman; \ Creese", 2009: r"Howes \& Kapur"},
                            part=PART, scale=("molecule", "circuit"), marr=("how",))
        with self.voiceover("Chapter three. Dopamine."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def discovery(self):
        head = heading(r"A drug from surgery")
        steps = VGroup()
        for yr, txt, c in ((r"1950s", r"Laborit, \ a French surgeon, \ looks for a drug to calm patients before "
                                     r"operations, \ and tries chlorpromazine", GREY_A),
                           (r"1952", r"Delay and Deniker in Paris give it to agitated psychotic patients: \ "
                                     r"hallucinations and delusions recede", GOOD),
                           (r"1955", r"in a few years it is used around the world; \ asylum populations begin to "
                                     r"fall", SYMP)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=20, width=1.8), wrapped_label(txt, 9.6, 21, WHITE))
                      .arrange(RIGHT, buff=0.35))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.4, 0])
        foot = wrapped_label(r"like the antidepressants of Part 40, \ the first antipsychotic was found by chance, "
                             r"\ and explained afterwards", 12.0, 21, YOU).move_to([0, -2.4, 0])
        tag = historical_tag(r"Delay \& Deniker (1952)")
        with self.voiceover(
            "The first treatment came from surgery. <bookmark mark='a'/> In the early nineteen-fifties a French "
            "surgeon, Henri Laborit, was looking for a drug to calm patients before operations, and tried a new "
            "compound, chlorpromazine. <bookmark mark='b'/> In 1952 the psychiatrists Jean Delay and Pierre Deniker "
            "gave it to agitated psychotic patients in Paris. Hallucinations and delusions receded. "
            "<bookmark mark='c'/> Within a few years it was used around the world, and asylum populations began to "
            "fall. <bookmark mark='d'/> Like the antidepressants of Part 40, the first antipsychotic was found by "
            "chance, and explained afterwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, s in zip("abc", steps):
                vo.wait_until(m)
                self.play(FadeIn(s, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def binding(self):
        head = heading(r"The dose follows the receptor")
        A = axes([-0.5, 3.5], [-0.5, 3.5], x_length=4.6, y_length=4.0, xticks=None, yticks=None,
                 xlabel=r"strength of binding to D2 receptors", ylabel=r"typical clinical dose (log)",
                 center=[-3.4, 0.0, 0], font_size=13)
        rng = np.random.default_rng(3)
        x = np.linspace(0, 3, 14)
        y = 3 - x + rng.normal(0, 0.22, len(x))
        dots = scatter(A.ax, x, y, PERSON, radius=0.07)
        line = curve(A.ax, np.array([0, 3.0]), np.array([3.0, 0.0]), MODEL, stroke_width=3)
        lm = label(r"schematic: \ each dot a drug", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Seeman and colleagues, \ and Creese, \ Burt and Snyder, \ 1976: \ the more tightly a drug binds "
             r"dopamine D2 receptors, \ the smaller the dose that treats psychosis", WHITE),
            (r"and amphetamine, \ which releases dopamine, \ can cause psychosis in high doses", AUTH),
            (r"the dopamine hypothesis: \ psychosis is too much dopamine signalling", MODEL),
            (r"but blockade is immediate, \ and improvement takes days to weeks; \ and negative and cognitive "
             r"symptoms barely change", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Seeman et al.\ (1976); \ Creese, \ Burt \& Snyder (1976)")
        with self.voiceover(
            "Why did it work? <bookmark mark='a'/> In 1976 two groups, Philip Seeman's and Ian Creese's with Solomon "
            "Snyder, found that the more tightly a drug binds dopamine D2 receptors, the smaller the dose that "
            "treats psychosis. Across drugs, the dose follows the receptor. <bookmark mark='b'/> And amphetamine, "
            "which releases dopamine, can cause psychosis in high doses. <bookmark mark='c'/> Hence the dopamine "
            "hypothesis: psychosis is too much dopamine signalling. <bookmark mark='d'/> But blockade is immediate, "
            "while improvement takes days to weeks. And the negative and cognitive symptoms barely change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots), Create(line))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def revised(self):
        head = heading(r"Version three")
        chain = VGroup()
        for t, c in ((r"genes, \ stress, \ drugs, \ adversity", GREY_A), (r"raised dopamine synthesis in the "
                                                                          r"striatum", AUTH),
                     (r"aberrant salience", SYMP), (r"psychosis", PERSON)):
            chain.add(word_chip(t, color=c, font_size=19, width=3.0))
        chain.arrange(RIGHT, buff=0.45).move_to([0, 1.1, 0])
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.06, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.25) for i in range(3)])
        rows = rows_of([
            (r"Howes and Kapur, \ 2009: \ many routes converge on raised presynaptic dopamine synthesis in the "
             r"striatum, \ seen in brain imaging", WHITE),
            (r"dopamine is a final common pathway to psychosis, \ not to schizophrenia as a whole", MODEL),
            (r"antipsychotics act at the end of the chain: \ they reduce the positive symptoms and the risk of "
             r"relapse, \ at a cost in side effects", GOOD),
        ], 12.4, 22, 0.42).move_to([0, -1.6, 0])
        tag = published_tag(r"Howes \& Kapur (2009)")
        with self.voiceover(
            "The theory has been revised. <bookmark mark='a'/> In 2009 Oliver Howes and Shitij Kapur proposed a "
            "third version. Many routes, genes, stress, drugs, adversity, converge on raised dopamine synthesis in "
            "the striatum, which brain imaging can see. <bookmark mark='b'/> Dopamine becomes a final common pathway "
            "to psychosis, not an explanation of schizophrenia as a whole. <bookmark mark='c'/> Antipsychotics act "
            "at the end of the chain. They reduce the positive symptoms and the risk of relapse, at a cost in side "
            "effects that people weigh differently."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.3), Create(arrows), FadeIn(rows[0]))
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
