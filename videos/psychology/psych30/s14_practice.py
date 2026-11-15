from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.screening()
        self.programmes()
        self.media()

    def card(self):
        card = chapter_card(13, r"In practice: \ screening, \ programmes and media",
                            r"Where does infancy research change what people do?",
                            lit={1962: r"Perry Preschool", 2010: r"DeLoache et al.", 2022: r"Durkin et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: screening, programmes and media."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def screening(self):
        head = heading(r"Developmental screening")
        times = VGroup(*[word_chip(t, color=c, font_size=20, width=2.6) for t, c in (
            (r"9 months", LOOK), (r"18 months", LOOK), (r"24 or 30 months", LOOK))]).arrange(RIGHT, buff=0.4)
        times.move_to([0, 1.7, 0])
        aut = label(r"autism-specific screening at 18 and 24 months", font_size=20, color=MIND).next_to(times, DOWN,
                                                                                                   buff=0.3)
        rows = rows_of([
            (r"the American Academy of Pediatrics recommends watching development at every visit, \ and a "
             r"standardized questionnaire at set ages", WHITE),
            (r"a screen is a test with a threshold: \ Part 12's hits, \ misses and false alarms apply, \ and a "
             r"positive screen leads to a full assessment, \ not a diagnosis", LOOK),
            (r"the milestones behind them are population norms: \ the spread between healthy children is wide, \ "
             r"so late on one milestone means little, \ late on many means more", NUM),
        ], 12.2, 24, 0.36).move_to([0, -1.6, 0])
        tag = published_tag(r"American Academy of Pediatrics guidance")
        with self.voiceover(
            "The first place infancy research meets practice is the doctor's office. <bookmark mark='a'/> The "
            "American Academy of Pediatrics recommends watching development at every visit, and a standardized "
            "questionnaire at set ages, around nine, eighteen, and twenty-four or thirty months, with an "
            "autism-specific screen at eighteen and twenty-four months. <bookmark mark='b'/> A screen is a test "
            "with a threshold, so Part 12's hits, misses and false alarms apply. A positive screen leads to a full "
            "assessment, not a diagnosis. <bookmark mark='c'/> And the milestones behind them are population norms. "
            "The spread between healthy children is wide, so being late on one milestone means little, and being "
            "late on many means more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in times], lag_ratio=0.3), FadeIn(aut), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def programmes(self):
        head = heading(r"Early childhood programmes")
        rows = rows_of([
            (r"the Perry Preschool Project, \ Michigan, \ from 1962: \ 123 children from poor families, \ "
             r"randomized; \ IQ gains faded within a few years, \ while gains in schooling and adult outcomes "
             r"persisted", GOOD),
            (r"the Head Start Impact Study, \ a national randomized trial: \ small early effects, \ largely gone by "
             r"third grade", LOST),
            (r"Tennessee's statewide pre-kindergarten, \ randomized: \ by sixth grade, \ the children who attended "
             r"were doing slightly worse than those who did not \ (Durkin and colleagues, \ 2022)", LOST),
            (r"small, \ intensive programmes and large public ones differ; \ fade-out of test scores is common, \ "
             r"and what lasts, \ if anything, \ is often not what was measured first", GREY_A),
        ], 12.2, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Schweinhart et al.\ (2005); \ Puma et al.\ (2012); \ Durkin et al.\ (2022)")
        with self.voiceover(
            "The second is early education, where the stakes and the claims are large. <bookmark mark='a'/> The "
            "Perry Preschool Project in Michigan began in 1962 with a hundred and twenty-three children from poor "
            "families, assigned at random. The gains in IQ faded within a few years, while gains in schooling and "
            "adult outcomes persisted. <bookmark mark='b'/> The Head Start Impact Study, a national randomized "
            "trial, found small early effects, largely gone by third grade. <bookmark mark='c'/> And a randomized "
            "study of Tennessee's statewide pre-kindergarten, reported by Kelley Durkin and colleagues in 2022, "
            "found that by sixth grade the children who attended were doing slightly worse than those who "
            "didn't. <bookmark mark='d'/> Small, intensive programmes and large public ones are different things. "
            "Fade-out of test scores is common, and what lasts, if anything, is often not what was measured first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def media(self):
        head = heading(r"Media for babies")
        rows = rows_of([
            (r"Judy DeLoache and colleagues, \ 2010: \ 12- to 18-month-olds watched a popular word-learning DVD "
             r"at home for four weeks", WHITE),
            (r"they learned no more of its words than children who never saw it; \ the most learning came when "
             r"parents taught the words in everyday activities", LOST),
            (r"parents who liked the DVD overestimated what their children had learned", GREY_A),
            (r"infants learn words from people who respond to them: \ natural pedagogy again, \ and the reason "
             r"designers of children's toys and media now test with children, \ not only with parents", GOOD),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"DeLoache et al.\ (2010)")
        with self.voiceover(
            "The third is a market: media for babies. <bookmark mark='a'/> In 2010 Judy DeLoache and colleagues gave "
            "families of twelve- to eighteen-month-olds a popular word-learning DVD to watch at home for four weeks. "
            "<bookmark mark='b'/> The children learned no more of its words than children who never saw it. The "
            "most learning came when parents taught the words during everyday activities. "
            "<bookmark mark='c'/> And parents who liked the DVD overestimated what their children had learned. "
            "<bookmark mark='d'/> Infants learn words from people who respond to them, natural pedagogy again, and "
            "it's one reason designers of children's toys and media now test with children, not only with parents."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
