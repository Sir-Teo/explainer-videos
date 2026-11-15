from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403

STAGES = [
    (r"1.\ \ avoid punishment", r"preconventional", AGE),
    (r"2.\ \ serve your own interest", r"preconventional", AGE),
    (r"3.\ \ be a good person to those you know", r"conventional", PERIOD),
    (r"4.\ \ keep the law and the social order", r"conventional", PERIOD),
    (r"5.\ \ the social contract and individual rights", r"postconventional", COHORT),
    (r"6.\ \ universal ethical principles", r"postconventional", COHORT),
]


class Moral(VoiceoverScene):
    def construct(self):
        self.card()
        self.heinz()
        self.stages()
        self.voice()
        self.erikson()

    def card(self):
        card = chapter_card(9, r"Moral development and identity", r"How does a child's sense of right grow?",
                            lit={1958: r"Kohlberg", 1982: r"Gilligan", 2000: r"Jaffee \& Hyde"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter nine. Moral development and identity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def heinz(self):
        head = heading(r"Heinz and the druggist")
        stage = demo_stage(12.4, 3.0, center=[0, 1.0, 0])
        story = wrapped_label(r"A woman is dying of a cancer that one drug might cure. \ The druggist who "
                              r"discovered it charges ten times what it costs him to make. \ Her husband, \ Heinz, "
                              r"\ can raise only half. \ The druggist refuses to sell it cheaper or let him pay "
                              r"later. \ Heinz breaks in and steals the drug. \ Should he have done that? \ Why?",
                              11.6, 24, WHITE).move_to(stage)
        rows = rows_of([
            (r"Lawrence Kohlberg, \ from his 1958 dissertation: \ dilemmas like this, \ put to children and "
             r"adults in long interviews", AGE),
            (r"what is scored is the reasoning, \ not the answer: \ ``yes'' and ``no'' can come from any stage", YOU),
        ], 12.4, 24, 0.36).move_to([0, -1.9, 0])
        with self.voiceover(
            "Here's a dilemma. <bookmark mark='a'/> A woman is dying of a cancer that one drug might cure. The "
            "druggist who discovered it charges ten times what it costs him to make. Her husband, Heinz, can raise "
            "only half. The druggist refuses to sell it cheaper or let him pay later. Heinz breaks in and steals the "
            "drug. Should he have done that, and why? <bookmark mark='b'/> Lawrence Kohlberg, starting from his "
            "1958 dissertation, put dilemmas like this to children and adults in long interviews. "
            "<bookmark mark='c'/> What he scored was the reasoning, not the answer: yes and no can come from any "
            "stage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(story), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def stages(self):
        head = heading(r"Kohlberg's six stages")
        steps = VGroup()
        for i, (txt, lvl, col) in enumerate(STAGES):
            box = Rectangle(width=4.6, height=0.62, color=col, fill_color=col, fill_opacity=0.15, stroke_width=2)
            box.move_to([-2.5 + 0.25 * i, -2.4 + 0.75 * i, 0])
            t = label(txt, font_size=18, color=col)
            if t.width > 4.4:
                t.width = 4.4
            steps.add(VGroup(box, t.move_to(box)))
        lv = VGroup(label(r"preconventional", font_size=20, color=AGE).next_to(steps[0], LEFT, buff=0.2),
                    label(r"conventional", font_size=20, color=PERIOD).next_to(steps[2], LEFT, buff=0.2),
                    label(r"postconventional", font_size=20, color=COHORT).next_to(steps[4], LEFT, buff=0.2))
        for l_ in lv:
            keep_in_frame(l_)
        rows = rows_of([
            (r"a sequence, \ claimed the same in every culture, \ each stage built on the one before", WHITE),
            (r"Anne Colby, \ Kohlberg and colleagues, \ 1983: \ 58 boys aged 10, \ 13 and 16, \ followed for "
             r"twenty years: \ the main test of the order", AGE),
            (r"most adults reason at stages 3 and 4; \ stage 6 was so rare it was later dropped from scoring", PERIOD),
        ], 5.2, 21, 0.36).move_to([4.0, 0.6, 0])
        tag = published_tag(r"Colby et al.\ (1983)")
        with self.voiceover(
            "Kohlberg found six stages, in three levels. <bookmark mark='a'/> At the preconventional level, right "
            "is what avoids punishment, then what serves your own interest. At the conventional level, it's being a "
            "good person to those you know, then keeping the law and the social order. At the postconventional "
            "level, it's the social contract and individual rights, then universal ethical principles. "
            "<bookmark mark='b'/> He claimed the stages were a sequence, the same in every culture, each built on "
            "the one before. <bookmark mark='c'/> The main test was longitudinal: Anne Colby, Kohlberg and colleagues "
            "followed fifty-eight boys, first interviewed at ten, thirteen and sixteen, for twenty years. "
            "<bookmark mark='d'/> Most adults reason at stages three and four, and stage six was so rare that it was "
            "later dropped from the scoring."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in steps], lag_ratio=0.6), FadeIn(lv),
                      run_time=6.0)
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def voice(self):
        head = heading(r"A different voice?")
        A = axes([-0.6, 1.6], [0, 0.35], x_length=4.0, y_length=3.4, xticks=None, yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: f"{v:g}", ylabel=r"Cohen's $d$", center=[-4.0, -0.5, 0], font_size=15)
        b = bars(A.ax, [0, 1], [0.28, 0.19], [CARE, AGE], width=0.6)
        nm = VGroup(label(r"care: \ women", font_size=17, color=CARE).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                    label(r"justice: \ men", font_size=17, color=AGE).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        rows = rows_of([
            (r"Carol Gilligan, \ 1982, \ \emph{In a Different Voice}: \ Kohlberg's first subjects were boys; \ his "
             r"scale rewards an ethic of justice and rights, \ and would score an ethic of care, \ which she heard "
             r"more in women, \ as lower", WHITE),
            (r"Lawrence Walker, \ 1984: \ a review of 108 studies; \ sex differences in Kohlberg's stages were "
             r"rare", COHORT),
            (r"Sara Jaffee and Janet Hyde, \ 2000, \ a meta-analysis: \ women used care reasoning a little more, \ "
             r"$d = 0.28$; \ men justice reasoning a little more, \ $d = 0.19$", AGE),
            (r"both orientations are used by both sexes, \ depending more on the dilemma than on the person", YOU),
        ], 7.6, 21, 0.34).move_to([2.4, -0.3, 0])
        tag = published_tag(r"Walker (1984); \ Jaffee \& Hyde (2000)")
        with self.voiceover(
            "The sharpest critique came from Kohlberg's colleague Carol Gilligan. <bookmark mark='a'/> In 1982, in "
            "In a Different Voice, she pointed out that his first subjects were all boys, and that his scale rewards "
            "an ethic of justice and rights. An ethic of care and responsibility, which she heard more often in "
            "women, would be scored as lower. <bookmark mark='b'/> The claim that the scale scored women lower was "
            "then tested. In 1984 Lawrence Walker reviewed a hundred and eight studies and found sex differences in "
            "Kohlberg's stages were rare. <bookmark mark='c'/> And in 2000 Sara Jaffee and Janet Hyde's "
            "meta-analysis found women used care reasoning a little more, a d of 0.28, and men justice reasoning a "
            "little more, a d of 0.19. <bookmark mark='d'/> Both orientations are used by both sexes, and which one "
            "appears depends more on the dilemma than on the person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(nm), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def erikson(self):
        head = heading(r"Identity across the lifespan")
        ages = [r"infancy", r"early childhood", r"play age", r"school age", r"adolescence", r"young adulthood",
                r"adulthood", r"old age"]
        crises = [r"trust \ vs \ mistrust", r"autonomy \ vs \ shame", r"initiative \ vs \ guilt",
                  r"industry \ vs \ inferiority", r"identity \ vs \ role confusion", r"intimacy \ vs \ isolation",
                  r"generativity \ vs \ stagnation", r"integrity \ vs \ despair"]
        col = VGroup()
        for i, (a, c) in enumerate(zip(ages, crises)):
            colr = CHILD if i < 4 else (AGE if i < 6 else OLD)
            col.add(VGroup(label(a, font_size=19, color=colr), label(c, font_size=19))
                    .arrange(RIGHT, buff=0.3))
        for r in col:
            r[0].set_width(min(r[0].width, 2.6))
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.2, -0.4, 0])
        rows = rows_of([
            (r"Erik Erikson, \ 1950: \ eight stages from birth to old age, \ each organized around a tension", WHITE),
            (r"adolescence's task: \ an identity, \ a sense of who one is across roles and over time", AGE),
            (r"influential as a map, \ hard to test as a theory: \ the stages are descriptions, \ and their "
             r"order is not a measured result", LOST),
            (r"its lasting idea: \ development does not stop at adulthood", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Kohlberg's stages ended in adulthood. Erik Erikson's didn't. <bookmark mark='a'/> In 1950 he described "
            "eight stages from birth to old age, each organized around a tension: trust against mistrust in infancy, "
            "through to integrity against despair in old age. <bookmark mark='b'/> Adolescence's task is an "
            "identity, a sense of who one is across roles and over time. <bookmark mark='c'/> Erikson's scheme was "
            "influential as a map and hard to test as a theory: the stages are descriptions, and their order isn't a "
            "measured result. <bookmark mark='d'/> But its lasting idea runs through the rest of this part: "
            "development doesn't stop at adulthood."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in col], lag_ratio=0.4), FadeIn(rows[0]),
                      run_time=4.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
