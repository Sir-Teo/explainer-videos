from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Groups(VoiceoverScene):
    def construct(self):
        self.card()
        self.overlap()
        self.invariance()
        self.fields()
        self.threat()

    def card(self):
        card = chapter_card(10, r"Group differences, \ with care", r"What can a difference between averages show?",
                            lit={1970: r"Lewontin", 2004: r"Wicherts et al.", 2018: r"Flore et al."}, part=PART,
                            scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter ten. Group differences, with care."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def overlap(self):
        d = load("groups")
        head = heading(r"What a difference between averages means")
        x = np.linspace(-4, 4.5, 300)
        panels = VGroup()
        for i, (dd, ov, ab) in enumerate(zip(d["d"], d["overlap"], d["above"])):
            A = axes([-4, 4.5], [0, 0.45], x_length=3.6, y_length=2.0, xticks=None, yticks=None,
                     center=[-4.4 + 4.4 * i, 0.9, 0], font_size=14)
            y1 = np.exp(-0.5 * x ** 2) / np.sqrt(2 * np.pi)
            y2 = np.exp(-0.5 * (x - dd) ** 2) / np.sqrt(2 * np.pi)
            c1, c2 = curve(A.ax, x, y1, VERB, stroke_width=3), curve(A.ax, x, y2, SPEED, stroke_width=3)
            t = VGroup(label(rf"$d = {dd:g}$", font_size=22),
                       label(rf"overlap {pct(ov)}", font_size=18, color=GOOD),
                       label(rf"{pct(ab)} of the lower group above the higher group's mean", font_size=15,
                             color=GREY_A)).arrange(DOWN, buff=0.12).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, c1, c2, t))
        rows = rows_of([
            (r"a difference between two groups' averages, \ in standard deviations, \ says little about any member "
             r"of either group", WHITE),
            (r"and nothing, \ on its own, \ about why it exists: \ the cause is a separate question, \ needing a "
             r"separate design", YOU),
        ], 12.4, 23, 0.34).move_to([0, -2.6, 0])
        tag = psyche_tag(r"\texttt{traits.overlap}")
        with self.voiceover(
            "This is the most misused topic in psychology, so begin with what a difference means. "
            "<bookmark mark='a'/> Two groups whose averages differ by a fifth of a standard deviation overlap by "
            f"{spct(d['overlap'][0])}. At half a standard deviation they overlap by {spct(d['overlap'][1])}, and at "
            f"a full one by {spct(d['overlap'][2])}, with {spct(d['above'][2])} of the lower group still above the "
            "higher group's average. A difference between averages says little about any member of either group. "
            "<bookmark mark='b'/> And on its own it says nothing about why it exists. The cause is a separate "
            "question, and it needs a separate design."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.4),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def invariance(self):
        d = load("groups")
        head = heading(r"Is the test measuring the same thing in both groups?")
        A = axes([-0.6, 5.6], [-0.1, 0.7], x_length=6.0, y_length=3.6, xticks=list(range(6)),
                 yticks=[0, 0.2, 0.4, 0.6], xfmt=lambda v: f"test {int(v) + 1}", yfmt=lambda v: f"{v:g}",
                 ylabel=r"difference between groups (SD)", center=[-2.9, -0.4, 0], font_size=14)
        bl = bars(A.ax, np.arange(6) - 0.18, d["latent_tests"], G, width=0.34)
        bb = bars(A.ax, np.arange(6) + 0.18, d["bias_tests"], LOST, width=0.34)
        key = legend([(G, r"a real difference in the ability"), (LOST, r"one test biased, \ no real difference")],
                     font_size=16).next_to(A, UP, buff=0.1)
        rows = rows_of([
            (r"if two groups differ in the ability a test measures, \ every test moves, \ in proportion to how much "
             r"of the ability it carries", G),
            (r"if one test is biased, \ by unfamiliar words or a skill one group was never taught, \ only that "
             r"test moves", LOST),
            (rf"the totals cannot tell them apart: \ {d['latent_total']:.2f} SD from a real difference, \ "
             rf"{d['bias_total']:.2f} from one biased test", WHITE),
            (r"measurement invariance: \ fit the factor model in both groups, \ and test whether loadings and "
             r"intercepts are equal; \ only then compare the groups' factor means", MODEL),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{traits.invariance\_demo}")
        with self.voiceover(
            "The technical question comes first: is the test measuring the same thing in both groups? "
            "<bookmark mark='a'/> If two groups really differ in the ability a test measures, every test moves, in "
            "proportion to how much of the ability it carries. <bookmark mark='b'/> If one test is biased, because "
            "of unfamiliar words or a skill one group was never taught, only that test moves. "
            "<bookmark mark='c'/> The total scores can't tell these apart. In Psyche's example a real difference "
            f"gives {d['latent_total']:.2f} of a standard deviation in the totals, and one biased test gives "
            f"{d['bias_total']:.2f}. <bookmark mark='d'/> The tool is measurement invariance: fit the factor model "
            "in both groups and test whether the loadings and the intercepts are equal. Only if they are can the "
            "groups' factor means be compared. Part 44 builds it. Wicherts showed the Flynn gains fail this test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bb), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fields(self):
        head = heading(r"Two fields, \ again")
        rows = rows_of([
            (r"Part 9's two fields: \ the same mix of seeds in rich soil and in poor soil", WHITE),
            (r"within each field, \ differences in height are almost entirely genetic: \ heritability near 100\%",
             G),
            (r"between the fields, \ the difference is entirely the soil", VERB),
            (r"so heritability within groups says nothing about the cause of a difference between them: \ Richard "
             r"Lewontin's point, \ 1970", YOU),
            (r"the cause of a group difference has to be studied directly, \ and for intelligence the data that "
             r"could settle it by design largely do not exist", LOST),
        ], 12.4, 22, 0.3).move_to([0, -1.85, 0])
        rng = np.random.default_rng(1970)
        seeds = rng.normal(size=12)
        fields = VGroup()
        for cx, base, soil, name in ((-3.3, 1.25, "#6B4F2A", r"rich soil"), (3.3, 0.55, "#C9B48A", r"poor soil")):
            ground = Rectangle(width=4.8, height=0.28, stroke_width=0, fill_color=soil, fill_opacity=1.0)
            ground.move_to([cx, 0.25, 0])
            top = ground.get_top()[1]
            plants = VGroup(*[Line([cx - 2.1 + 4.2 * k / 11, top, 0], [cx - 2.1 + 4.2 * k / 11, top + base + 0.28 * g, 0],
                                   color=GOOD, stroke_width=5) for k, g in enumerate(seeds)])
            mean = DashedLine([cx - 2.35, top + base, 0], [cx + 2.35, top + base, 0], color=VERB, stroke_width=2)
            fields.add(VGroup(ground, label(name, font_size=18, color=GREY_A).next_to(ground, DOWN, buff=0.1),
                              plants, mean))
        gap = DoubleArrow([0, 0.39 + 0.55, 0], [0, 0.39 + 1.25, 0], color=VERB, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.2)
        gap_l = label(r"the soil", font_size=17, color=VERB).next_to(gap, RIGHT, buff=0.1)
        with self.voiceover(
            "Now the most common logical error. <bookmark mark='a'/> Remember Part 9's two fields, the same mix of "
            "seeds sown in rich soil and in poor soil. <bookmark mark='b'/> Within each field, differences in "
            "height are almost entirely genetic, a heritability near a hundred percent. <bookmark mark='c'/> Between "
            "the fields, the difference is entirely the soil. <bookmark mark='d'/> So heritability within groups "
            "says nothing about the cause of a difference between them. That was Richard Lewontin's point, in 1970. "
            "<bookmark mark='e'/> The cause of a group difference has to be studied directly, and for intelligence "
            "the data that could settle it by design largely don't exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(f[0]) for f in fields], *[FadeIn(f[1]) for f in fields], FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[LaggedStart(*[Create(p_) for p_ in f[2]], lag_ratio=0.1) for f in fields], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[Create(f[3]) for f in fields], GrowFromCenter(gap), FadeIn(gap_l), FadeIn(rows[2]))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def threat(self):
        head = heading(r"Stereotype threat: \ the record")
        rows = rows_of([
            (r"the claim: \ reminding people of a negative stereotype about their group lowers their test scores", WHITE),
            (r"Paulette Flore and Jelte Wicherts, \ 2015: \ a meta-analysis of studies with schoolgirls in "
             r"mathematics and science: \ signs of publication bias", G),
            (r"Flore, \ Mulder and Wicherts, \ 2018: \ a registered report with more than 2{,}000 Dutch "
             r"secondary-school students: \ no stereotype-threat effect on mathematics", LOST),
            (r"the full record, \ and what remains of the idea, \ is Part 36's", YOU),
        ], 12.4, 24, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Flore \& Wicherts (2015); \ Flore et al.\ (2018)")
        with self.voiceover(
            "One proposed cause of group differences in test scores has its own replication record. "
            "<bookmark mark='a'/> The claim is that reminding people of a negative stereotype about their group "
            "lowers their test scores. <bookmark mark='b'/> In 2015 Paulette Flore and Jelte Wicherts "
            "meta-analysed studies of schoolgirls in mathematics and science, and found signs of publication bias. "
            "<bookmark mark='c'/> In 2018 Flore, Mulder and Wicherts ran a registered report with more than two "
            "thousand Dutch secondary-school students, and found no stereotype-threat effect on mathematics. "
            "<bookmark mark='d'/> The full record, and what remains of the idea, is Part 36's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
