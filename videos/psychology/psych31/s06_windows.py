from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Windows(VoiceoverScene):
    def construct(self):
        self.card()
        self.kittens()
        self.language()
        self.care()
        self.closing()

    def card(self):
        card = chapter_card(5, r"Windows", r"What has to happen early, \ and what can happen any time?",
                            lit={1963: r"Wiesel \& Hubel", 1989: r"Johnson \& Newport", 2017: r"ERA study"},
                            part=PART, scale=("cell", "person"), marr=("how",))
        with self.voiceover("Chapter five. Windows."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kittens(self):
        d = load("windows")
        head = heading(r"One eye, \ closed in a kitten")
        A = axes([0, 20], [0, 1.15], x_length=6.0, y_length=3.8, xticks=[0, 4, 8, 12, 16, 20], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age \ (weeks)", ylabel=r"effect of closing one eye",
                 center=[-3.0, -0.6, 0], font_size=16)
        win = curve(A.ax, d["weeks"], d["early"], AGE, stroke_width=5)
        rows = rows_of([
            (r"Torsten Wiesel and David Hubel, \ 1963: \ close one eye of a young kitten, \ and most cells in "
             r"the visual cortex stop responding to it; \ in an adult cat, \ the same closure does little", WHITE),
            (r"Hubel and Wiesel, \ 1970: \ the susceptible period runs from about the fourth week to three or four "
             r"months, \ most intense in weeks four and five", AGE),
            (r"a sensitive period: \ the same experience, \ with very different effects at different ages", YOU),
            (r"why a child's lazy eye is treated early", GOOD),
        ], 5.6, 21, 0.34).move_to([3.6, -0.3, 0])
        tag = historical_tag(r"Wiesel \& Hubel (1963); \ Hubel \& Wiesel (1970)")
        shape = label(r"illustrative shape", font_size=16, color=GREY_B).next_to(A, DOWN, buff=0.1)
        with self.voiceover(
            "The clearest window is in vision, and Part 7 met it. <bookmark mark='a'/> In 1963, Torsten Wiesel and "
            "David Hubel closed one eye of young kittens. Afterwards, most cells in the visual cortex no longer "
            "responded to that eye. In adult cats, the same closure did little. <bookmark mark='b'/> In 1970 they "
            "mapped the window: it runs from about the fourth week to three or four months, most intense in weeks "
            "four and five. The curve here is drawn to that shape. <bookmark mark='c'/> That's a sensitive period: "
            "the same experience, with very different effects at different ages. <bookmark mark='d'/> And it's why "
            "a child's lazy eye is treated early."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(shape))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(win), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def language(self):
        d = load("windows")
        head = heading(r"A window for grammar?")
        A = axes([0, 40], [0, 1.1], x_length=6.0, y_length=3.8, xticks=[0, 10, 20, 30, 40], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age when learning began", ylabel=r"eventual grammar",
                 center=[-3.0, -0.6, 0], font_size=16)
        win = curve(A.ax, d["t_lang"], d["lang"], COHORT, stroke_width=5)
        rows = rows_of([
            (r"Jacqueline Johnson and Elissa Newport, \ 1989: \ 46 Chinese and Korean speakers in the US; \ the "
             r"later they arrived, \ the worse their English grammar", WHITE),
            (r"Kenji Hakuta and colleagues, \ 2003, \ from census data on millions of immigrants: \ a steady "
             r"decline with age of arrival, \ no break at puberty", PERIOD),
            (r"Joshua Hartshorne, \ Joshua Tenenbaum and Steven Pinker, \ 2018: \ 669{,}498 people online; \ "
             r"ability to learn grammar near its peak until about 17, \ then declining", COHORT),
            (r"a decline with age is clear; \ how sharp, \ when, \ and why, \ are argued \ (Part 23's Ledger)", YOU),
        ], 5.6, 21, 0.32).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Johnson \& Newport (1989); \ Hartshorne et al.\ (2018)")
        shape = label(r"illustrative shape", font_size=16, color=GREY_B).next_to(A, DOWN, buff=0.1)
        with self.voiceover(
            "Language has a window too, but a blurrier one. <bookmark mark='a'/> In 1989 Jacqueline Johnson and "
            "Elissa Newport tested forty-six Chinese and Korean speakers living in the United States: the later "
            "they had arrived, the worse their English grammar. <bookmark mark='b'/> Kenji Hakuta and colleagues, "
            "using census data on millions of immigrants, found a steady decline with age of arrival, with no break "
            "at puberty. <bookmark mark='c'/> And in 2018 Joshua Hartshorne, Joshua Tenenbaum and Steven Pinker "
            "analysed six hundred and sixty-nine thousand people who took an online grammar quiz. Separating age, age "
            "of starting and years of experience, they estimated that the ability to learn grammar stays near its "
            "peak until about seventeen, then declines. <bookmark mark='d'/> A decline with age is clear. How sharp "
            "it is, when it starts and why are argued, as Part 23's Ledger recorded."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(shape))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(win), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def care(self):
        head = heading(r"A window for care?")
        bar_l = VGroup(Rectangle(width=4.2, height=0.5, color=GOOD, fill_color=GOOD, fill_opacity=0.6),
                       label(r"under 6 months in an institution", font_size=20)).arrange(DOWN, buff=0.15)
        bar_r = VGroup(Rectangle(width=4.2, height=0.5, color=LOST, fill_color=LOST, fill_opacity=0.6),
                       label(r"more than 6 months", font_size=20)).arrange(DOWN, buff=0.15)
        VGroup(bar_l, bar_r).arrange(RIGHT, buff=1.0).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"the English and Romanian Adoptees study: \ children adopted into British families from Romanian "
             r"institutions after 1989, \ followed to ages 22 to 25", WHITE),
            (r"under six months in an institution: \ as few problems as British adoptees", GOOD),
            (r"more than six months: \ autistic features, \ inattention and overactivity persisted into adulthood, "
             r"\ and three to four times the rate of emotional problems", LOST),
            (r"IQ, \ low in childhood, \ recovered by early adulthood; \ and a fifth of the long-stay group had no "
             r"problems at any age", AGE),
            (r"not a lottery: \ the age of adoption was not randomized; \ Bucharest's trial is the randomized check",
             YOU),
        ], 12.4, 23, 0.34).move_to([0, -1.0, 0])
        tag = published_tag(r"Sonuga-Barke et al.\ (2017)")
        with self.voiceover(
            "Is there a window for care? <bookmark mark='a'/> After 1989, British families adopted children from "
            "Romanian institutions, and the English and Romanian Adoptees study followed them to ages twenty-two to "
            "twenty-five. <bookmark mark='b'/> Those who had spent less than six months in an institution had as few "
            "problems as British adoptees. <bookmark mark='c'/> Those who had spent more had autistic features, "
            "inattention and overactivity that persisted into adulthood, and three to four times the rate of "
            "emotional problems. <bookmark mark='d'/> Their IQ, low in childhood, recovered by early adulthood, and "
            "a fifth of the long-stay group had no problems at any age. <bookmark mark='e'/> The age of adoption "
            "wasn't randomized, so this is a correlation. Bucharest's lottery is the randomized check, and it "
            "points the same way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bar_l), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bar_r), FadeIn(rows[2]))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def closing(self):
        head = heading(r"What closes a window")
        rows = rows_of([
            (r"experience-expectant: \ the brain counts on input every member of the species gets, \ light and "
             r"patterned sight, \ voices, \ a caregiver, \ at a time it can be counted on", AGE),
            (r"experience-dependent: \ learning what is particular to one life, \ which stays open for a lifetime "
             r"\ (Part 7's London taxi drivers)", COHORT),
            (r"in animals, \ windows can be moved: \ changing the brain's inhibitory signalling can open or close "
             r"the visual one early or late", MODEL),
            (r"so early is not destiny: \ some windows close, \ most learning does not; \ the question is always "
             r"which", YOU),
        ], 12.4, 25, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "So what makes a window? A useful distinction was made by William Greenough and colleagues. "
            "<bookmark mark='a'/> Some development is experience-expectant: the brain counts on input that every "
            "member of the species gets, light and patterned sight, voices, a caregiver, and it counts on getting it "
            "at a predictable time. Those windows close. <bookmark mark='b'/> Other development is "
            "experience-dependent: learning what is particular to one life, which stays open for a lifetime, like "
            "the London taxi drivers of Part 7. <bookmark mark='c'/> In animals, windows can be moved: changing the "
            "brain's inhibitory signalling can open or close the visual one early or late, which suggests a window "
            "is a state of a circuit, not just a date. <bookmark mark='d'/> So early isn't destiny. Some windows "
            "close; most learning doesn't. The question is always which."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
