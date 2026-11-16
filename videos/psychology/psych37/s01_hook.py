from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


def coins(n: int, color, r: float = 0.13) -> VGroup:
    return VGroup(*[Circle(radius=r, color=color, fill_opacity=0.8, stroke_width=2) for _ in range(n)]).arrange(
        RIGHT, buff=0.08)


class Hook(VoiceoverScene):
    def construct(self):
        self.offer()
        self.result()
        self.question()
        self.objectives()

    def offer(self):
        head = heading(r"Take it, \ or leave it")
        pie = coins(10, PERSON).move_to([-3.4, 1.6, 0])
        prop = little_person(1.1, color=CROWD).move_to([-5.3, 0.0, 0])
        resp = little_person(1.1, color=MODEL).move_to([-1.5, 0.0, 0])
        lp = label(r"proposer", font_size=16, color=CROWD).next_to(prop, DOWN, buff=0.1)
        lr = label(r"responder", font_size=16, color=MODEL).next_to(resp, DOWN, buff=0.1)
        keep = coins(8, CROWD).scale(0.8).move_to([-4.3, -1.6, 0])
        give = coins(2, MODEL).scale(0.8).move_to([-2.3, -1.6, 0])
        rows = rows_of([
            (r"the ultimatum game: \ one person proposes how to split a sum; \ the other accepts, \ and both are "
             r"paid, \ or rejects, \ and both get nothing", WHITE),
            (r"a responder who wants only money should accept any positive offer; \ a proposer who knows that "
             r"should offer the smallest amount", AUTH),
            (r"so the textbook prediction for ten coins: \ offer one, \ and it is accepted", CROWD),
        ], 6.0, 21, 0.4).move_to([3.3, -0.1, 0])
        with self.voiceover(
            "Here is a game you can play with ten coins. <bookmark mark='a'/> One person proposes how to split "
            "them. The other either accepts, and both are paid, or rejects, and both get nothing. "
            "<bookmark mark='b'/> A responder who cares only about money should accept any offer above zero, "
            "because something beats nothing. A proposer who knows that should offer as little as possible. "
            "<bookmark mark='c'/> So the textbook prediction is: offer one coin, and it's accepted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pie), FadeIn(prop), FadeIn(resp), FadeIn(lp), FadeIn(lr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(keep), FadeIn(give))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Transform(keep, coins(9, CROWD).scale(0.8).move_to([-4.3, -1.6, 0])),
                      Transform(give, coins(1, MODEL).scale(0.8).move_to([-2.0, -1.6, 0])))
        self.clear_scene()

    def result(self):
        head = heading(r"What people do")
        A = axes([-0.6, 1.6], [0, 50], x_length=4.4, y_length=3.4, xticks=None, yticks=[0, 25, 50],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"average offer, \ share of the sum", center=[-3.9, -0.3, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [36.7, 40], [CROWD, PERSON], width=0.6)
        names = VGroup(wrapped_label(r"the first study, \ 1982", 1.8, 15, CROWD).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                       buff=0.15),
                       wrapped_label(r"37 papers, \ 2004", 1.8, 15, PERSON).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"37\%", font_size=18, color=CROWD).next_to(A.ax.c2p(0, 36.7), UP, buff=0.1),
                      label(r"40\%", font_size=18, color=PERSON).next_to(A.ax.c2p(1, 40), UP, buff=0.1))
        rows = rows_of([
            (r"G\"uth, \ Schmittberger and Schwarze, \ 1982: \ the first ultimatum experiments; \ proposers offered "
             r"on average about 37\% of the sum", WHITE),
            (r"Oosterbeek, \ Sloof and van de Kuilen, \ 2004: \ 37 papers: \ the average offer was 40\%", PERSON),
            (r"and low offers are often rejected: \ people pay to refuse a split they see as unfair", AUTH),
            (r"proposers seem to know it: \ they offer far more than the textbook minimum", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"G\"uth, \ Schmittberger \& Schwarze (1982); \ Oosterbeek et al.\ (2004)")
        with self.voiceover(
            "That isn't what happens. <bookmark mark='a'/> In 1982 Werner Güth and colleagues ran the first "
            "ultimatum experiments. Proposers offered on average about thirty-seven percent of the sum. "
            "<bookmark mark='b'/> In 2004 a meta-analysis of thirty-seven papers found an average offer of forty "
            "percent. <bookmark mark='c'/> And low offers are often rejected. People pay, out of their own pocket, "
            "to refuse a split they see as unfair. <bookmark mark='d'/> Proposers seem to know it, and offer far "
            "more than the textbook minimum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(tops[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(tops[1]), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ why cooperate with strangers?")
        rows = rows_of([
            (r"the games economists use as experiments, \ and what ``rational'' predicts in each", CROWD),
            (r"why cooperation evolves, \ why it decays, \ and what punishment does", PERSON),
            (r"the same games in fifteen small societies", MODEL),
            (r"and the closest bargains of all: \ attraction, \ relationships, \ and how little can be predicted "
             r"about a particular couple", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks why people cooperate with strangers. <bookmark mark='a'/> It sets out the games "
            "economists use as experiments, and what rational play predicts in each. <bookmark mark='b'/> It asks "
            "why cooperation evolves, why it decays, and what punishment does. <bookmark mark='c'/> It takes the "
            "same games to fifteen small societies. <bookmark mark='d'/> And it turns to the closest bargains of "
            "all: attraction, relationships, and how little can be predicted about a particular couple."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 37", font_size=34, color=GREY_B), label(r"Bonds and Bargains", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"five games as experiments, \ and the gap between rational and real",
            r"kin, \ reciprocity, \ reputation and punishment; \ a tournament of strategies",
            r"inequity aversion as a utility function, \ and the same games in fifteen societies",
            r"attraction: \ proximity, \ exposure, \ similarity, \ and what people say they want",
            r"predicting relationships, \ and why in-sample accuracy misleads",
            r"mate preferences across cultures, \ and loneliness and health",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 37 of Psychology, Built: bonds and bargains, the fourth part of Act Nine. "
            "<bookmark mark='a'/> We'll set out five games as experiments, and the gap between rational and real "
            "play. We'll meet kin, reciprocity, reputation and punishment, and run a tournament of strategies. "
            "We'll write inequity aversion as a utility function, and take the games to fifteen societies. We'll "
            "look at attraction, and at what people say they want. We'll try to predict relationships, and see why "
            "in-sample accuracy misleads. And we'll end with mate preferences across cultures, and loneliness and "
            "health."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
