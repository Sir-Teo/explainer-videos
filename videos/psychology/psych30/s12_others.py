from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Others(VoiceoverScene):
    def construct(self):
        self.card()
        self.temperament()
        self.vygotsky()
        self.overimitation()

    def card(self):
        card = chapter_card(11, r"Temperament and learning from others", r"How do children shape, \ and get shaped "
                            r"by, \ the people around them?", lit={1934: r"Vygotsky", 1977: r"Thomas \& Chess",
                                                                   2005: r"Horner \& Whiten", 2009: r"Csibra \& Gergely"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter eleven. Temperament and learning from others."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def temperament(self):
        head = heading(r"Babies differ from the start")
        A = axes([-0.5, 3.5], [0, 50], x_length=5.0, y_length=3.2, xticks=None, yticks=[0, 10, 20, 30, 40],
                 yfmt=lambda v: f"{v:g}\\%", ylabel=r"share of children", center=[-3.4, -0.2, 0], font_size=16)
        vals = [(r"easy", 40, GOOD), (r"difficult", 10, LOST), (r"slow to warm up", 15, LOOK), (r"mixed", 35, GREY_B)]
        bs = VGroup()
        for i, (t, v, c) in enumerate(vals):
            b = bars(A.ax, [i], [v], c, width=0.6)
            bs.add(VGroup(b, label(rf"{v}\%", font_size=16, color=c).next_to(b, UP, buff=0.06),
                          wrapped_label(t, 1.1, 15, c).next_to(A.ax.c2p(i, 0), DOWN, buff=0.15)))
        rows = rows_of([
            (r"Alexander Thomas and Stella Chess's New York Longitudinal Study, \ from 1956: \ parents' reports of "
             r"activity, \ regularity, \ mood and reaction to new things", WHITE),
            (r"about 40\% of children were easy, \ 10\% difficult, \ 15\% slow to warm up, \ and the rest a mix", CARE),
            (r"temperament is partly heritable, \ moderately stable, \ and only one input: \ goodness of fit with "
             r"the family matters", LOOK),
            (r"children also shape their own environments: \ a fussy baby evokes different care \ (Part 9's "
             r"gene--environment correlation)", MIND),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Thomas \& Chess (1977)")
        with self.voiceover(
            "Babies differ from the start. <bookmark mark='a'/> From 1956 Alexander Thomas and Stella Chess "
            "followed children in the New York Longitudinal Study, using parents' reports of activity, regularity, "
            "mood and reaction to new things. <bookmark mark='b'/> About forty percent of the children were easy, "
            "ten percent difficult, fifteen percent slow to warm up, and the rest a mix. <bookmark mark='c'/> "
            "Temperament is partly heritable and moderately stable, and it's only one input. What matters is how "
            "well it fits the family around the child. <bookmark mark='d'/> And children shape their own "
            "environments: a fussy baby evokes different care from a calm one, Part 9's gene-environment "
            "correlation in action."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def vygotsky(self):
        head = heading(r"The zone of proximal development")
        rings = VGroup(Circle(radius=0.8, color=GOOD, fill_opacity=0.25),
                       Annulus(inner_radius=0.8, outer_radius=1.6, color=LOOK, fill_opacity=0.25),
                       Circle(radius=2.2, color=GREY_B)).move_to([-3.6, -0.2, 0])
        rl = VGroup(label(r"alone", font_size=17, color=GOOD).move_to([-3.6, -0.2, 0]),
                    label(r"with help", font_size=17, color=LOOK).move_to([-3.6, 0.95, 0]),
                    label(r"not yet", font_size=17, color=GREY_B).move_to([-3.6, 1.75, 0]))
        rows = rows_of([
            (r"Lev Vygotsky, \ 1930s: \ what a child can do with help today, \ it can do alone tomorrow", WHITE),
            (r"the zone of proximal development: \ between what a child can do alone and what it can do with a "
             r"more skilled partner", LOOK),
            (r"teaching works best in that zone; \ a Goldilocks rule again, \ for learning from others", GOOD),
            (r"Gergely Csibra and Gy\"orgy Gergely: \ natural pedagogy; \ infants treat eye contact, \ their name "
             r"and infant-directed speech as signals that something worth learning is coming", MIND),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Vygotsky (1934); \ Csibra \& Gergely (2009)")
        with self.voiceover(
            "Much of what children learn comes from other people. <bookmark mark='a'/> In the 1930s Lev Vygotsky "
            "wrote that what a child can do with help today, it can do alone tomorrow. <bookmark mark='b'/> He "
            "called the space between what a child can do alone and what it can do with a more skilled partner the "
            "zone of proximal development. <bookmark mark='c'/> Teaching works best in that zone: the Goldilocks "
            "rule again, now for learning from others. <bookmark mark='d'/> Gergely Csibra and György Gergely "
            "proposed that infants are built for this. They treat eye contact, their own name and infant-directed "
            "speech as signals that something worth learning is coming, which may be why ManyBabies found the "
            "preference it did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rings), FadeIn(rl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def overimitation(self):
        head = heading(r"Copying too much")
        rows = rows_of([
            (r"Victoria Horner and Andrew Whiten, \ 2005: \ a person opens a puzzle box with some steps that are "
             r"needed and some that are not", WHITE),
            (r"with an opaque box, \ young chimpanzees and 3- to 4-year-old children copied everything", GREY_A),
            (r"with a transparent box, \ where the useless steps were visibly useless, \ chimpanzees skipped them; "
             r"\ children still copied them", MIND),
            (r"overimitation: \ children copy the method, \ not just the goal; \ it looks irrational, \ and it may "
             r"be how cultures pass on ways of doing things whose reasons nobody can see \ (Part 38)", GOOD),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Horner \& Whiten (2005); \ Lyons, \ Young \& Keil (2007)")
        with self.voiceover(
            "Children learn from others more faithfully than they need to. <bookmark mark='a'/> In 2005 Victoria "
            "Horner and Andrew Whiten showed young chimpanzees and three- to four-year-old children a person "
            "opening a puzzle box, with some steps that were needed and some that were not. <bookmark mark='b'/> "
            "With an opaque box, both chimpanzees and children copied everything. <bookmark mark='c'/> With a "
            "transparent box, where the useless steps were visibly useless, chimpanzees skipped them. Children still "
            "copied them. <bookmark mark='d'/> It's called overimitation. Children copy the method, not just the "
            "goal. It looks irrational, and it may be how cultures pass on ways of doing things whose reasons nobody "
            "can see, a theme of Part 38."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
