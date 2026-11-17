from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403

# Arnett (2008): six APA journals, 2003-2007; samples by origin, against the share of the world's population
SAMPLES = (68, 28, 4)
PEOPLE = (5, 7, 88)


def stack(values, colors, height: float = 4.2, width: float = 1.3) -> VGroup:
    """A 100% stacked bar, bottom to top."""
    out = VGroup()
    y = 0.0
    for v, c in zip(values, colors):
        h = height * v / 100
        out.add(Rectangle(width=width, height=max(h, 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85)
                .move_to([0, y + h / 2, 0]))
        y += h
    return out


class Hook(VoiceoverScene):
    def construct(self):
        self.count()
        self.weird()
        self.question()
        self.objectives()

    def count(self):
        head = heading(r"Who is in the experiments?")
        left = stack(SAMPLES, (PERSON, WEST, WORLD)).move_to([-4.8, -0.4, 0])
        right = stack(PEOPLE, (PERSON, WEST, WORLD)).move_to([-2.2, -0.4, 0])
        names = VGroup(wrapped_label(r"samples in six leading journals", 2.2, 15, GREY_A).next_to(left, DOWN, buff=0.2),
                       wrapped_label(r"the world's population", 2.2, 15, GREY_A).next_to(right, DOWN, buff=0.2))
        key = legend([(PERSON, r"United States"), (WEST, r"other Western, \ industrialized"),
                      (WORLD, r"the rest of the world")], font_size=15).next_to(right, RIGHT, buff=0.35)
        key.shift(UP * 1.2)
        n1 = label(r"68\%", font_size=20, color=BLACK).move_to(left[0])
        n2 = label(r"88\%", font_size=20, color=BLACK).move_to(right[2])
        rows = rows_of([
            (r"Arnett, \ 2008: \ the samples in six leading American Psychological Association journals, \ "
             r"2003 to 2007", WHITE),
            (r"68\% came from the United States, \ and 96\% from Western industrialized countries", PERSON),
            (r"those countries hold about 12\% of the world's population; \ the other 88\% supplied about 4\% of "
             r"the samples", WORLD),
        ], 5.0, 20, 0.4).move_to([4.3, -0.9, 0])
        tag = published_tag(r"Arnett (2008)")
        with self.voiceover(
            "Who is psychology about? <bookmark mark='a'/> In 2008 Jeffrey Arnett counted the people in six leading "
            "journals of the American Psychological Association, from 2003 to 2007. <bookmark mark='b'/> Sixty-eight "
            "percent of the samples came from the United States, and ninety-six percent from Western industrialized "
            "countries. <bookmark mark='c'/> Those countries hold about twelve percent of the world's population. "
            "The other eighty-eight percent of humanity supplied about four percent of the samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(b, DOWN) for b in left])
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(n1), Indicate(left[0], color=PERSON))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[GrowFromEdge(b, DOWN) for b in right], FadeIn(n2))
        self.clear_scene()

    def weird(self):
        head = heading(r"WEIRD")
        letters = VGroup()
        for ch, word in (("W", r"Western"), ("E", r"educated"), ("I", r"industrialized"), ("R", r"rich"),
                         ("D", r"democratic")):
            letters.add(VGroup(label(ch, font_size=44, color=WEST), label(word, font_size=24, color=GREY_A))
                        .arrange(RIGHT, buff=0.3, aligned_edge=DOWN))
        letters.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-4.0, -0.3, 0])
        rows = rows_of([
            (r"Henrich, \ Heine and Norenzayan, \ 2010: \ ``The weirdest people in the world?''", WHITE),
            (r"on visual illusions, \ fairness, \ cooperation, \ reasoning, \ the self, \ these samples are often at "
             r"one end of the human range", WORLD),
            (r"and American undergraduates are often at the end of that end", PERSON),
            (r"the claim is not that WEIRD people are wrong, \ but that a science of humans built on them may "
             r"describe a special case", YOU),
        ], 7.0, 21, 0.42).move_to([2.6, -0.3, 0])
        tag = published_tag(r"Henrich, \ Heine \& Norenzayan (2010)")
        with self.voiceover(
            "Two years later a paper gave the problem a name. <bookmark mark='a'/> Joseph Henrich, Steven Heine and "
            "Ara Norenzayan asked whether psychology's subjects were the weirdest people in the world: Western, "
            "educated, industrialized, rich and democratic. <bookmark mark='b'/> They went through the evidence on "
            "visual illusions, fairness, cooperation, reasoning and the self, and found these samples often sat at "
            "one end of the human range. <bookmark mark='c'/> And American undergraduates were often at the end of "
            "that end. <bookmark mark='d'/> The claim isn't that WEIRD people are wrong. It's that a science of "
            "humans built on them may be describing a special case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in letters],
                                                            lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ whose mind has psychology been describing?")
        rows = rows_of([
            (r"what varies across societies, \ from a visual illusion to the self, \ and what causes the variation",
             WORLD),
            (r"how to measure across cultures without fooling yourself", MODEL),
            (r"culture as a second inheritance, \ with its own mathematics", GOOD),
            (r"and morality as the test case: \ one trolley, \ millions of people, \ and a puppet show for babies",
             PERSON),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks whose mind psychology has been describing. <bookmark mark='a'/> It looks at what "
            "varies across societies, from a visual illusion to the self, and at what causes the variation. "
            "<bookmark mark='b'/> It asks how to measure across cultures without fooling yourself. "
            "<bookmark mark='c'/> It treats culture as a second inheritance, with its own mathematics. "
            "<bookmark mark='d'/> And it takes morality as the test case: one trolley, millions of people, and a "
            "puppet show for babies."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 38", font_size=34, color=GREY_B), label(r"Culture and Morals", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"who psychology's samples are, \ and an illusion that varies",
            r"independent and interdependent selves, \ and where cultural differences come from",
            r"measuring across cultures: \ the reference-group effect",
            r"cultural evolution: \ conformity, \ prestige, \ and population size",
            r"moral psychology: \ intuition, \ reasoning, \ and one trolley in 42 countries",
            r"infants and morality, \ and what does travel",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 38 of Psychology, Built: culture and morals, the last part of Act Nine. "
            "<bookmark mark='a'/> We'll see who psychology's samples are, and an illusion that varies. We'll meet "
            "independent and interdependent selves, and theories of where cultural differences come from. We'll "
            "see how a simple rating scale can hide a real difference. We'll write down the mathematics of "
            "conformity, prestige and population size. We'll turn to moral psychology, and to one trolley in forty-"
            "two countries. And we'll end with infants, and with what does travel."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
