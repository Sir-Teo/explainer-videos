from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Ageing(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_kinds()
        self.speed()
        self.selectivity()

    def card(self):
        card = chapter_card(10, r"Adulthood and ageing", r"What declines, \ what holds, \ and what improves?",
                            lit={1963: r"Horn \& Cattell", 1996: r"Salthouse", 2003: r"Charles et al."}, part=PART,
                            scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter ten. Adulthood and ageing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_kinds(self):
        d = load("ageing")
        head = heading(r"Fluid and crystallized")
        A = axes([20, 90], [-1.6, 1.3], x_length=6.4, y_length=4.4, xticks=[20, 40, 60, 80], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"age",
                 ylabel=r"SD, \ relative to age 25", center=[-2.9, -0.4, 0], font_size=16)
        sp = curve(A.ax, d["age"], d["speed"], LOST, stroke_width=5)
        fl = curve(A.ax, d["age"], d["fluid"], PERIOD, stroke_width=5)
        vo_ = curve(A.ax, d["age"], d["vocab"], GOOD, stroke_width=5)
        key = legend([(LOST, r"processing speed"), (PERIOD, r"reasoning with new problems"),
                      (GOOD, r"vocabulary and knowledge")], font_size=17).move_to(A.ax.c2p(40, -1.2))
        sh = label(r"illustrative curves, \ drawn to the typical shapes", font_size=16, color=GREY_B)
        sh.next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"Raymond Cattell, \ 1943, \ and John Horn: \ fluid intelligence, \ reasoning with what is new, \ "
             r"and crystallized intelligence, \ what has been learned", WHITE),
            (r"fluid abilities and speed decline through adulthood, \ more steeply later", PERIOD),
            (r"knowledge and vocabulary rise into the sixties, \ and decline only late", GOOD),
            (r"in Salthouse's 2009 sample, \ vocabulary was still rising at 60 while reasoning had fallen since "
             r"the late twenties", AGE),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.fluid\_crystallized}: \ illustrative")
        with self.voiceover(
            "Ageing isn't one decline. <bookmark mark='a'/> Raymond Cattell, from 1943, and later John Horn, split "
            "intelligence in two: fluid intelligence, reasoning with what is new, and crystallized intelligence, "
            "what has been learned. <bookmark mark='b'/> Fluid abilities and processing speed decline through "
            "adulthood, more steeply later. <bookmark mark='c'/> Knowledge and vocabulary rise into the sixties and "
            "decline only late. The curves are drawn to those typical shapes. <bookmark mark='d'/> In Salthouse's "
            "sample, vocabulary was still rising at sixty, while reasoning had been falling since the late twenties."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(sh))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(key))
            vo.wait_until("b")
            self.play(Create(sp), Create(fl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(vo_), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def speed(self):
        head = heading(r"Speed as the common cause?")
        chain = VGroup(*[word_chip(t, color=c, font_size=22, width=3.0) for t, c in (
            (r"slower processing", LOST), (r"steps run out of time", PERIOD), (r"early results lost", AGE),
            (r"worse reasoning and memory", COHORT))]).arrange(RIGHT, buff=0.35).move_to([0, 1.7, 0])
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.05, color=GREY_B)
                          for i in range(3)])
        rows = rows_of([
            (r"Timothy Salthouse, \ 1996: \ the processing-speed theory: \ a slower mind runs out of time for later "
             r"steps, \ and loses earlier results before it can combine them", WHITE),
            (r"the evidence: \ once simple speed is controlled, \ much of the age difference in many abilities "
             r"shrinks", AGE),
            (r"the limit: \ shared variance is not a cause; \ speed and the rest may both reflect one ageing brain "
             r"\ (Part 44's latent variables)", LOST),
            (r"and ageing is not only loss: \ older adults use knowledge and strategies to compensate, \ often "
             r"well, \ in everyday tasks", GOOD),
        ], 12.4, 24, 0.38).move_to([0, -1.2, 0])
        tag = published_tag(r"Salthouse (1996)")
        with self.voiceover(
            "Why would so many abilities decline together? <bookmark mark='a'/> In 1996 Timothy Salthouse proposed "
            "the processing-speed theory. A slower mind runs out of time for the later steps of a task, and loses "
            "its earlier results before it can combine them. <bookmark mark='b'/> The evidence is that once simple "
            "speed is controlled, much of the age difference in many abilities shrinks. <bookmark mark='c'/> The "
            "limit is that shared variance isn't a cause. Speed and the rest may both reflect one ageing brain, a "
            "question for the latent-variable models of Part 44. <bookmark mark='d'/> And ageing isn't only loss. "
            "Older adults use knowledge and strategies to compensate, often well, in everyday tasks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def selectivity(self):
        head = heading(r"Less time, \ better feelings?")
        rows = rows_of([
            (r"Laura Carstensen's socioemotional selectivity theory: \ when the future feels long, \ people seek "
             r"information and new contacts; \ when it feels short, \ they seek emotional meaning", WHITE),
            (r"Susan Charles, \ Mara Mather and Carstensen, \ 2003: \ 144 people aged 18 to 80 saw positive, \ "
             r"negative and neutral pictures; \ the oldest recalled fewer negative ones, \ and the bias grew with "
             r"each older group", OLD),
            (r"Andrew Reed, \ Larry Chan and Joseph Mikels, \ 2014: \ a meta-analysis of 100 studies, \ 7{,}129 "
             r"people: \ the positivity effect is reliable, \ larger when people are free to attend as they like",
             GOOD),
            (r"on average, \ emotional well-being holds or improves into old age, \ even as speed declines", YOU),
        ], 12.4, 24, 0.38).move_to([0, -0.3, 0])
        tag = published_tag(r"Charles et al.\ (2003); \ Reed et al.\ (2014)")
        with self.voiceover(
            "Something improves with age, too. <bookmark mark='a'/> Laura Carstensen's socioemotional selectivity "
            "theory says that when the future feels long, people seek information and new contacts, and when it "
            "feels short, they seek emotional meaning. <bookmark mark='b'/> In 2003, Susan Charles, Mara Mather and "
            "Carstensen showed a hundred and forty-four people aged eighteen to eighty positive, negative and "
            "neutral pictures. The oldest group recalled fewer of the negative ones, and the bias grew with each "
            "older group. <bookmark mark='c'/> In 2014, Andrew Reed, Larry Chan and Joseph Mikels pooled a hundred "
            "studies and over seven thousand people: this positivity effect is reliable, and larger when people are "
            "free to attend as they like. <bookmark mark='d'/> On average, emotional well-being holds or improves "
            "into old age, even as speed declines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
