from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Identity(VoiceoverScene):
    def construct(self):
        self.card()
        self.theory()
        self.cooperation()
        self.camp()
        self.lost_boys()

    def card(self):
        card = chapter_card(2, r"Identity and competition", r"Why would a label be enough?",
                            lit={1954: r"Sherif et al.", 1979: r"Tajfel \& Turner", 2014: r"Balliet et al.",
                                 2018: r"Perry"}, part=PART, scale=("group",), marr=("what",))
        with self.voiceover("Chapter two. Identity and competition."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def theory(self):
        head = heading(r"Social identity")
        me = Circle(radius=0.5, color=PERSON, fill_opacity=0.25).move_to([-4.4, 0.6, 0])
        ml = label(r"me", font_size=20, color=PERSON).move_to(me)
        groups = VGroup(*[word_chip(t, color=c, font_size=18, width=2.4) for t, c in (
            (r"Klee fans", IN), (r"my school", CROWD), (r"my team", GOOD))]).arrange(DOWN, buff=0.35)
        groups.move_to([-1.9, 0.6, 0])
        links = VGroup(*[Line(me.get_right(), g.get_left(), color=GREY_B, stroke_width=2) for g in groups])
        rows = rows_of([
            (r"Tajfel and Turner, \ 1979: \ part of who we are comes from the groups we belong to", WHITE),
            (r"we want our groups to compare well with others: \ positive distinctiveness", IN),
            (r"so a label is enough to start a comparison, \ and favouritism keeps the comparison favourable", PERSON),
            (r"self-categorization theory (Turner and colleagues, \ 1987): \ which identity is switched on depends "
             r"on the situation", YOU),
        ], 6.2, 20, 0.36).move_to([3.2, -0.2, 0])
        tag = historical_tag(r"Tajfel \& Turner (1979); \ Turner et al.\ (1987)")
        with self.voiceover(
            "Why would a label be enough? <bookmark mark='a'/> In 1979 Tajfel and John Turner proposed that part "
            "of who we are comes from the groups we belong to. <bookmark mark='b'/> And we want those groups to "
            "compare well with others. <bookmark mark='c'/> So a label is enough to start a comparison, and "
            "favouritism keeps the comparison favourable. <bookmark mark='d'/> Turner's self-categorization theory "
            "added that which identity is switched on depends on the situation: a fan at the match, a scientist "
            "at work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(me), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(groups), Create(links), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def cooperation(self):
        head = heading(r"How big is favouritism?")
        A = axes([-0.6, 1.6], [0, 0.5], x_length=4.4, y_length=3.4, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"ingroup favouritism, \ $d$", center=[-3.9, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [0.19, 0.42], [IN, GOOD], width=0.6)
        names = VGroup(wrapped_label(r"a label only", 1.8, 15, IN).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"outcomes depend on each other", 1.8, 15, GOOD).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                            buff=0.15))
        tops = VGroup(label(r"0.19", font_size=18, color=IN).next_to(A.ax.c2p(0, 0.19), UP, buff=0.1),
                      label(r"0.42", font_size=18, color=GOOD).next_to(A.ax.c2p(1, 0.42), UP, buff=0.1))
        rows = rows_of([
            (r"Balliet, \ Wu and De Dreu, \ 2014: \ 212 studies of whether people cooperate more with their own "
             r"group", WHITE),
            (r"where groups were only labels, \ as in dictator games, \ the favouritism was slight", IN),
            (r"where people's outcomes depended on each other, \ as in social dilemmas, \ it was about twice as "
             r"large", GOOD),
            (r"and the other group was treated much like strangers: \ more warmth for us, \ not hostility to them",
             YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Balliet, \ Wu \& De Dreu (2014)")
        with self.voiceover(
            "How big is the effect, across many studies? <bookmark mark='a'/> In 2014 Balliet, Wu and De Dreu "
            "pooled two hundred and twelve studies of whether people cooperate more with their own group. "
            "<bookmark mark='b'/> Where groups were only labels, as in a game where one person splits money, the "
            "favouritism was slight, an effect of about point two. <bookmark mark='c'/> Where people's outcomes "
            "depended on each other, it was about twice as large. <bookmark mark='d'/> And the other group was "
            "treated much like strangers. Favouritism was mostly more warmth for us, not hostility to them."
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

    def camp(self):
        head = heading(r"Robbers Cave, \ 1954")
        eagles = VGroup(*[Dot(radius=0.11, color=IN) for _ in range(11)]).arrange_in_grid(3, 4, buff=0.18)
        rattlers = VGroup(*[Dot(radius=0.11, color=OUTG) for _ in range(11)]).arrange_in_grid(3, 4, buff=0.18)
        eagles.move_to([-4.7, 0.9, 0])
        rattlers.move_to([-2.3, 0.9, 0])
        le = label(r"Eagles", font_size=18, color=IN).next_to(eagles, UP, buff=0.15)
        lr = label(r"Rattlers", font_size=18, color=OUTG).next_to(rattlers, UP, buff=0.15)
        stages = VGroup(*[word_chip(t, color=c, font_size=17, width=1.6) for t, c in (
            (r"bonding", GOOD), (r"contests", AUTH), (r"shared goals", MODEL))]).arrange(RIGHT, buff=0.2)
        stages.move_to([-3.5, -1.0, 0])
        arrows = VGroup(*[Arrow(stages[k].get_right(), stages[k + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        rows = rows_of([
            (r"Sherif and colleagues: \ 22 boys of about eleven at a summer camp in Oklahoma, \ in two groups that "
             r"did not know the other existed", WHITE),
            (r"each group bonded and named itself; \ then a tournament with prizes for the winners turned them into "
             r"enemies: \ raids, \ name-calling, \ a burnt flag", AUTH),
            (r"contact alone did not help; \ goals that needed both groups did, \ gradually: \ fixing the water "
             r"supply, \ pulling a stuck truck", MODEL),
            (r"realistic conflict theory: \ competition for real stakes creates hostility, \ and shared goals can "
             r"undo it", YOU),
        ], 6.4, 20, 0.34).move_to([3.0, -0.2, 0])
        tag = historical_tag(r"Sherif et al.\ (1954, \ 1961)")
        with self.voiceover(
            "The most famous study of group conflict came earlier, from Muzafer Sherif, whose light opened Part "
            "34. <bookmark mark='a'/> In 1954 he and his colleagues took twenty-two boys of about eleven to a "
            "summer camp in Oklahoma, in two groups that didn't know the other existed. <bookmark mark='b'/> Each "
            "group bonded and named itself, the Eagles and the Rattlers. Then a tournament, with prizes for the "
            "winners, turned them into enemies: raids, name-calling, a flag burnt. <bookmark mark='c'/> Simply "
            "bringing them together didn't help. Goals that needed both groups did, gradually: fixing the camp's "
            "water supply, pulling a stuck truck. <bookmark mark='d'/> It became the founding study of realistic "
            "conflict theory: competition for real stakes creates hostility, and shared goals can undo it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eagles), FadeIn(rattlers), FadeIn(le), FadeIn(lr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(stages[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowArrow(arrows[0]), FadeIn(stages[1]),
                      eagles.animate.shift(LEFT * 0.3), rattlers.animate.shift(RIGHT * 0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), GrowArrow(arrows[1]), FadeIn(stages[2]),
                      eagles.animate.shift(RIGHT * 0.3), rattlers.animate.shift(LEFT * 0.3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lost_boys(self):
        head = heading(r"As run, \ and as staged")
        rows = rows_of([
            (r"the year before, \ 1953, \ Sherif tried the same design at Middle Grove, \ New York; \ it was not "
             r"part of the famous report", WHITE),
            (r"Gina Perry's book \emph{The Lost Boys}, \ 2018, \ from Sherif's archives: \ at Middle Grove, \ the "
             r"boys would not turn on each other, \ and the study was abandoned", AUTH),
            (r"the boys did not know they were in a study; \ in Perry's account, \ staff provoked some of the conflict", CROWD),
            (r"so the textbook result is one run of a design that had already failed once: \ a demonstration, \ "
             r"with the conditions arranged, \ not an estimate of how often camps turn hostile", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        tag = historical_tag(r"Perry (2018)")
        with self.voiceover(
            "Like the prison study in Part 34, Robbers Cave has an archive. <bookmark mark='a'/> The year before, "
            "in 1953, Sherif tried the same design at Middle Grove, in New York State. It wasn't part of the famous "
            "report. <bookmark mark='b'/> In 2018 Gina Perry's book The Lost Boys, written from Sherif's archives, "
            "described how at Middle Grove the boys would not turn on each other, and the study was abandoned. "
            "<bookmark mark='c'/> The boys didn't know they were in a study, and in Perry's account, staff "
            "provoked some of the conflict. <bookmark mark='d'/> So the textbook result is one run of a design that had already "
            "failed once. It's a demonstration, with the conditions arranged, not an estimate of how often groups "
            "turn hostile."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
