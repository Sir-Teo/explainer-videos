from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Canvassing(VoiceoverScene):
    def construct(self):
        self.card()
        self.fake()
        self.real()

    def card(self):
        card = chapter_card(10, r"Deep canvassing", r"Can one conversation change a mind for months?",
                            lit={2014: r"LaCour \& Green", 2016: r"Broockman \& Kalla"}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter ten. Deep canvassing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fake(self):
        head = heading(r"A study too good to be true")
        rows = rows_of([
            (r"LaCour and Green, \ 2014, \ \emph{Science}: \ a single conversation at the door with a canvasser "
             r"was reported to change attitudes to same-sex marriage, \ lastingly", WHITE),
            (r"David Broockman and Joshua Kalla, \ then graduate students, \ tried to extend it, \ and could not "
             r"reproduce how the survey had been run", CROWD),
            (r"with Peter Aronow they found irregularities in the data; \ the survey firm said it had done no such "
             r"work", AUTH),
            (r"the co-author, \ Donald Green, \ asked for a retraction, \ and \emph{Science} retracted the paper in "
             r"2015", PERSON),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = historical_tag(r"LaCour \& Green (2014), \ retracted")
        with self.voiceover(
            "The last chapter on reducing prejudice is a story of fraud, and of what came after. "
            "<bookmark mark='a'/> In 2014 a paper in Science by Michael LaCour and Donald Green reported that a "
            "single conversation at the door with a canvasser changed attitudes to same-sex marriage, lastingly. "
            "<bookmark mark='b'/> David Broockman and Joshua Kalla, then graduate students, tried to extend it, and "
            "couldn't reproduce how the survey had been run. <bookmark mark='c'/> With Peter Aronow they found "
            "irregularities in the data, and the survey firm said it had done no such work. "
            "<bookmark mark='d'/> Green asked for a retraction, and Science retracted the paper in 2015."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def real(self):
        head = heading(r"Then they ran the real experiment")
        door = VGroup(Rectangle(width=1.2, height=2.2, stroke_color=GREY_B, fill_color="#1B2029", fill_opacity=1),
                      Dot([0.38, 0, 0], radius=0.06, color=GREY_B)).move_to([-5.2, 0.8, 0])
        canvasser = little_person(1.2, color=CROWD).move_to([-3.9, 0.6, 0])
        voter = little_person(1.2, color=PERSON).move_to([-5.2, 0.6, 0])
        clock = label(r"about 10 minutes", font_size=16, color=GREY_A).next_to(VGroup(door, canvasser), DOWN,
                                                                               buff=0.3)
        A = axes([-0.6, 1.6], [0, 12], x_length=3.6, y_length=1.9, xticks=None, yticks=[0, 10],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"change in warmth", center=[-4.4, -2.0, 0], font_size=13)
        b = bars(A.ax, [0, 1], [0.4, 10], [GREY_B, GOOD], width=0.6)
        names = VGroup(label(r"control", font_size=13, color=GREY_B).next_to(A.ax.c2p(0, 0), DOWN, buff=0.08),
                       label(r"canvassed", font_size=13, color=GOOD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.08))
        rows = rows_of([
            (r"Broockman and Kalla, \ 2016, \ \emph{Science}: \ in Miami-Dade, \ voters were assigned at random to a "
             r"conversation of about ten minutes about transgender people, \ or about recycling", WHITE),
            (r"the canvassers asked voters to recall a time they had been judged for being different, \ and to "
             r"take the other's perspective", CROWD),
            (r"warmth toward transgender people rose about ten points on a feeling thermometer, \ and the change "
             r"lasted for months", GOOD),
            (r"canvassers who were not transgender had effects too; \ the fake study promised it, \ and the "
             r"people who exposed it delivered it", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = published_tag(r"Broockman \& Kalla (2016)")
        with self.voiceover(
            "Then the two students ran the experiment for real. <bookmark mark='a'/> In 2016 Broockman and Kalla "
            "published in Science a randomized experiment in Miami-Dade. Voters were assigned at random to a "
            "conversation of about ten minutes about transgender people, or to one about recycling. "
            "<bookmark mark='b'/> The canvassers asked voters to recall a time they had been judged for being "
            "different, and to take the other person's perspective. <bookmark mark='c'/> Warmth toward transgender "
            "people rose about ten points on a feeling thermometer, and the change lasted for months. "
            "<bookmark mark='d'/> Canvassers who weren't transgender had effects too. The fake study promised "
            "something; the people who exposed it delivered it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(door), FadeIn(voter), FadeIn(canvasser), FadeIn(clock))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(names), GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
