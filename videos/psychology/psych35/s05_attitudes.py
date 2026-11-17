from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Attitudes(VoiceoverScene):
    def construct(self):
        self.card()
        self.lapiere()
        self.when()

    def card(self):
        card = chapter_card(4, r"Attitudes and behaviour", r"Does what people say predict what they do?",
                            lit={1934: r"LaPiere", 1991: r"Ajzen", 2006: r"Glasman \& Albarrac\'in"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. Attitudes and behaviour."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lapiere(self):
        head = heading(r"A road trip, \ and a letter")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.6, y_length=3.6, xticks=None, yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"refused, \ or said they would", center=[-3.8, -0.3, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [100 / 251, 92], [GOOD, AUTH], width=0.6)
        names = VGroup(wrapped_label(r"in person: \ 251 places", 1.8, 15, GOOD).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"by letter: \ 128 replies", 1.8, 15, AUTH).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                         buff=0.15))
        tops = VGroup(label(r"1 refusal", font_size=16, color=GOOD).next_to(A.ax.c2p(0, 1), UP, buff=0.1),
                      label(r"92\% no", font_size=18, color=AUTH).next_to(A.ax.c2p(1, 92), UP, buff=0.1))
        rows = rows_of([
            (r"LaPiere, \ 1934: \ travelling across the United States with a young Chinese couple, \ he recorded how "
             r"251 hotels and restaurants treated them", WHITE),
            (r"they were refused once", GOOD),
            (r"about six months later he wrote to the same places, \ asking whether they would accept Chinese "
             r"guests; \ of the 128 that replied, \ 92\% said they would not", AUTH),
            (r"a classic of the gap between saying and doing; \ though the people who served the couple were not "
             r"necessarily the ones who answered the letter", YOU),
        ], 6.4, 20, 0.34).move_to([3.0, -0.3, 0])
        tag = historical_tag(r"LaPiere (1934)")
        with self.voiceover(
            "The idea that attitudes drive behaviour had an early warning. <bookmark mark='a'/> In the early 1930s "
            "the sociologist LaPiere travelled across the United States with a young Chinese couple, at a "
            "time of open prejudice, and recorded how two hundred and fifty-one hotels and restaurants treated "
            "them. <bookmark mark='b'/> They were refused once. <bookmark mark='c'/> About six months later he wrote "
            "to the same places, asking whether they would accept Chinese guests. Of the hundred and twenty-eight "
            "that replied, ninety-two percent said they would not. <bookmark mark='d'/> It became the classic "
            "example of the gap between saying and doing, though the people who served the couple were not "
            "necessarily the ones who answered the letter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(tops[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(tops[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def when(self):
        head = heading(r"When attitudes predict")
        nodes = VGroup(*[word_chip(t, color=c, font_size=20, width=3.6) for t, c in (
            (r"attitude toward the act", PERSON), (r"what others expect", CROWD), (r"control over the act", GOOD))])
        nodes.arrange(DOWN, buff=0.45).move_to([-4.2, 0.6, 0])
        inten = word_chip(r"intention", color=MODEL, font_size=22, width=2.4).move_to([-0.9, 0.6, 0])
        act = word_chip(r"behaviour", color=WHITE, font_size=22, width=2.4).move_to([2.0, 0.6, 0])
        arrows = VGroup(*[Arrow(n.get_right(), inten.get_left(), buff=0.1, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.15) for n in nodes],
                        Arrow(inten.get_right(), act.get_left(), buff=0.1, color=GREY_B, stroke_width=3))
        rows = rows_of([
            (r"Ajzen's theory of planned behaviour, \ 1991: \ attitudes toward the specific act, \ others' "
             r"expectations and perceived control shape an intention, \ which predicts the act", WHITE),
            (r"Glasman and Albarrac\'in, \ 2006: \ attitudes predict later behaviour better when they are easy to "
             r"call to mind, \ stable, \ formed by direct experience and held with confidence", CROWD),
            (r"LaPiere asked about a whole category, \ ``members of the Chinese race''; \ the innkeepers faced two "
             r"particular guests: \ the attitude and the act did not match in kind", YOU),
        ], 12.4, 20, 0.28).move_to([0, -2.1, 0])
        tag = historical_tag(r"Ajzen (1991); \ Glasman \& Albarrac\'in (2006)")
        with self.voiceover(
            "So when do attitudes predict? <bookmark mark='a'/> In 1991 Ajzen's theory of planned behaviour "
            "put three things before an act: the attitude toward that specific act, what others expect, and how "
            "much control a person feels they have. Together they shape an intention, which predicts the act. "
            "<bookmark mark='b'/> In 2006 Glasman and Albarracín pooled studies of attitudes and later behaviour. "
            "Attitudes predicted better when they were easy to call to mind, stable, formed by direct experience, "
            "and held with confidence. <bookmark mark='c'/> And the attitude has to match the act. LaPiere asked "
            "about a whole category of people. The innkeepers faced two particular guests at their door."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(nodes), FadeIn(inten), FadeIn(act), Create(arrows))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
