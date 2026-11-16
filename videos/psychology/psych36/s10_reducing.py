from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Reducing(VoiceoverScene):
    def construct(self):
        self.card()
        self.reviews()
        self.radio()
        self.training()

    def card(self):
        card = chapter_card(9, r"Reducing prejudice", r"What has been shown to work?",
                            lit={2009: r"Paluck", 2019: r"Chang et al.", 2021: r"Paluck et al."}, part=PART,
                            scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter nine. Reducing prejudice."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def reviews(self):
        head = heading(r"Hundreds of experiments, \ few answers")
        rows = rows_of([
            (r"Paluck, \ Porat, \ Clark and Green, \ 2021: \ 418 experiments on reducing prejudice, \ reported in "
             r"309 papers from 2007 to 2019", WHITE),
            (r"many were brief, \ light-touch studies that measured attitudes soon afterwards", AUTH),
            (r"few measured behaviour, \ few followed people for long, \ few were run where prejudice does its "
             r"damage", CROWD),
            (r"their verdict: \ much of the research is ill-suited to give actionable, \ evidence-based "
             r"recommendations", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Paluck, \ Porat, \ Clark \& Green (2021)")
        with self.voiceover(
            "What has been shown to reduce prejudice? <bookmark mark='a'/> In 2021 Paluck and colleagues reviewed "
            "four hundred and eighteen experiments, reported in three hundred and nine papers from 2007 to 2019. "
            "<bookmark mark='b'/> Many were brief, light-touch studies that measured attitudes soon afterwards."
            " <bookmark mark='c'/> Few measured behaviour, few followed people for long, and few were run "
            "where prejudice does its damage. <bookmark mark='d'/> Their verdict was that much of the research is "
            "ill-suited to give actionable, evidence-based recommendations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def radio(self):
        head = heading(r"A radio drama in Rwanda")
        radio = VGroup(RoundedRectangle(corner_radius=0.15, width=2.4, height=1.5, stroke_color=PERSON,
                                        fill_color="#1B2029", fill_opacity=1),
                       Circle(radius=0.42, color=PERSON).shift(LEFT * 0.5),
                       VGroup(*[Line(LEFT * 0.35, RIGHT * 0.35, color=GREY_B) for _ in range(3)]).arrange(
                           DOWN, buff=0.15).shift(RIGHT * 0.6),
                       Line([0.6, 0.75, 0], [1.1, 1.5, 0], color=GREY_B))
        radio.move_to([-4.2, 1.0, 0])
        A = axes([-0.6, 1.6], [0, 1.0], x_length=4.0, y_length=2.2, xticks=None, yticks=None,
                 center=[-4.0, -1.6, 0], font_size=14)
        b = bars(A.ax, [0, 1], [0.08, 0.6], [GREY_B, GOOD], width=0.6)
        names = VGroup(wrapped_label(r"personal beliefs", 1.8, 14, GREY_B).next_to(A.ax.c2p(0, 0), DOWN, buff=0.1),
                       wrapped_label(r"perceived norms, \ behaviour", 1.8, 14, GOOD).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                         buff=0.1))
        note = label(r"the pattern reported, \ drawn schematically", font_size=13, color=GREY_B).next_to(A, UP,
                                                                                                    buff=0.05)
        rows = rows_of([
            (r"Paluck, \ 2009: \ a year-long field experiment in Rwanda after the genocide; \ communities were "
             r"assigned at random to a radio soap opera about reconciliation, \ or one about health", WHITE),
            (r"listeners' personal beliefs barely moved", GREY_A),
            (r"what they thought others believed did, \ and so did behaviour: \ more willingness to speak up and "
             r"disagree, \ more cooperation", GOOD),
            (r"a lesson that recurs: \ norms, \ what people think others think, \ can move when private attitudes "
             r"do not, \ Part 34's crowds again", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = published_tag(r"Paluck (2009)")
        with self.voiceover(
            "One of the clearest field experiments came from Rwanda. <bookmark mark='a'/> In 2009 Elizabeth Levy "
            "Paluck reported a year-long field experiment after the genocide. Communities were assigned at random "
            "to listen to a radio soap opera about reconciliation, or to one about health. "
            "<bookmark mark='b'/> Listeners' personal beliefs barely moved. <bookmark mark='c'/> But what they "
            "thought other people believed did, and so did their behaviour: more willingness to speak up and "
            "disagree, more cooperation. <bookmark mark='d'/> It's a lesson that recurs. Norms, what people think "
            "others think, can move when private attitudes don't. Part 34's crowds again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(radio))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(names), FadeIn(note), GrowFromEdge(b[0], DOWN), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def training(self):
        head = heading(r"Diversity training")
        rows = rows_of([
            (r"diversity training is a large industry; \ few programmes are evaluated with control groups", WHITE),
            (r"Chang, \ Milkman and colleagues, \ 2019: \ an online diversity training randomized among 3{,}016 "
             r"employees of a global company", CROWD),
            (r"attitudes moved; \ behaviour changed little, \ and mainly among people who were already supportive",
             AUTH),
            (r"their conclusion: \ one-off trainings are not a remedy for bias at work; \ structure, \ such as the "
             r"structured interviews of Part 53, \ is the usual alternative", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Chang et al.\ (2019)")
        with self.voiceover(
            "And the most common intervention of all. <bookmark mark='a'/> Diversity training is a large industry, "
            "and few programmes are evaluated against a control group. <bookmark mark='b'/> In 2019 Edward Chang, "
            "Katherine Milkman and colleagues randomized an online diversity training among three thousand "
            "employees of a global company. <bookmark mark='c'/> Attitudes moved. Behaviour changed little, and "
            "mainly among people who were already supportive. <bookmark mark='d'/> Their conclusion was that "
            "one-off trainings are not a remedy for bias at work. Changing the structure of decisions, like the "
            "structured interviews of Part 53, is the usual alternative."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
