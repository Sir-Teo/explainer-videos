from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403

# the thirteen signatures of the report of 12 September 1904, by what the report says of each (Pfungst, Suppl. II)
SIGNERS = [
    r"circus manager", r"count", r"school board", r"teacher", r"zoo director", r"zoologist", r"Dr.\ Kandt",
    r"major", r"major-general", r"veterinarian", r"physiologist", r"psychologist", r"H.\ Suermondt",
]


class Hook(VoiceoverScene):
    def construct(self):
        self.hans()
        self.commission()
        self.wager()
        self.objectives()

    def tap(self, hans, counter, n, run_time=0.42, start=0):
        """Tap ``n`` times, counting on screen."""
        pivot = hans.pivot.get_center()
        for k in range(start + 1, start + n + 1):
            self.play(Rotate(hans.leg, -0.38, about_point=pivot), run_time=run_time / 2, rate_func=rush_into)
            counter.become(label(rf"{k}", font_size=72, color=HORSE).move_to(counter))
            self.play(Rotate(hans.leg, 0.38, about_point=pivot), run_time=run_time / 2, rate_func=rush_from)

    def hans(self):
        place = VGroup(label(r"1904", font_size=64, color=KANT),
                       label(r"Berlin: \ a courtyard in the north of the city", font_size=34, color=WHITE))
        place.arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        hans = horse(3.5).move_to([-3.7, -0.75, 0])
        name = label(r"Hans", font_size=40, color=HORSE).next_to(hans, DOWN, buff=0.25)
        owner = questioner(2.7).move_to([1.0, -0.95, 0])
        who = VGroup(label(r"Wilhelm von Osten", font_size=30), label(r"a retired teacher of mathematics",
                                                                      font_size=24, color=GREY_A))
        who.arrange(DOWN, buff=0.08).next_to(owner, DOWN, buff=0.25)
        board = RoundedRectangle(width=3.6, height=1.5, corner_radius=0.1, stroke_color=GREY_A, stroke_width=2,
                                 fill_color="#1B2230", fill_opacity=1).move_to([4.6, 0.6, 0])
        q = MathTex(r"3 + 4 = \ ?", font_size=60).move_to(board)
        counter = label(r"0", font_size=72, color=HORSE).move_to([-0.9, 0.9, 0])
        feats = VGroup(*[label(t, font_size=30, color=GREY_A) for t in (
            r"adds, subtracts, multiplies", r"works with fractions", r"tells the time", r"spells out words")])
        feats.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, -1.7, 0])
        src = historical_tag(archive.PFUNGST_1907.cite)
        with self.voiceover(
            "Berlin, 1904. In a courtyard in the north of the city, a retired teacher of mathematics named "
            "Wilhelm von Osten is showing visitors his horse. <bookmark mark='a'/> The horse is called Hans, and "
            "von Osten has been teaching him for four years, the way you would teach a child: with a blackboard, "
            "and patience, and carrots. <bookmark mark='b'/> He asks a question. Three plus four. "
            "<bookmark mark='c'/> And Hans answers with his right forefoot. <bookmark mark='d'/> Seven. "
            "He can subtract, and multiply. He can work with fractions, tell the time, and spell out words, a tap "
            "at a time. <bookmark mark='e'/> And he answers strangers as well as his master, which is what makes "
            "it hard to dismiss. The newspapers call him Clever Hans, and the question in Berlin that summer is "
            "whether a horse can think."
        ) as vo:
            self.play(FadeIn(place, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(hans, shift=RIGHT * 0.3), FadeIn(name), FadeIn(owner), FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(board), Write(q))
            vo.wait_until("c")
            self.play(FadeIn(counter))
            self.tap(hans, counter, 7)
            vo.wait_until("d")
            self.play(Circumscribe(counter, color=HORSE, buff=0.12),
                      LaggedStart(*[FadeIn(f, shift=LEFT * 0.15) for f in feats], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("e")
            self.play(Indicate(name, color=HORSE, scale_factor=1.15))
        self.clear_scene()

    def commission(self):
        d = load("hans")
        head = heading(r"12 September 1904: \ a commission of thirteen", color=KANT)
        people = VGroup()
        for role in SIGNERS:
            fig = little_person(0.85, color=P.HUMAN)
            t = label(role, font_size=23, color=GREY_A)
            people.add(VGroup(fig, t).arrange(DOWN, buff=0.12))
        people.arrange_in_grid(rows=2, cols=7, buff=(0.42, 0.35)).next_to(head, DOWN, buff=0.4)
        if people.width > 13.4:
            people.width = 13.4
        star = SurroundingRectangle(people[11], color=P.ACCENT, buff=0.08, corner_radius=0.08, stroke_width=2)
        stumpf = label(r"Carl Stumpf, \ director of Berlin's Psychological Institute", font_size=26, color=P.ACCENT)
        stumpf.next_to(people, DOWN, buff=0.25)
        verdict = quote_card(r"Tricks are out of the question. \ldots\ Unintentional signs of the kind which are at "
                             r"present familiar are likewise excluded. \ldots\ This is a case worthy of a serious "
                             r"and incisive investigation.", r"report of the commission, 12 September 1904, signed "
                             r"by all thirteen (abridged)", width=12.2, font_size=30, color=KANT)
        verdict.to_edge(DOWN, buff=0.75)
        src = historical_tag(archive.PFUNGST_1907.cite + r", Supplement II")
        assert d["commission_members"] == len(SIGNERS)
        with self.voiceover(
            "So a commission is formed to settle it. <bookmark mark='a'/> Thirteen people. A circus manager, who "
            "knows every trick by which animals are made to look clever. The director of the zoo. A veterinarian. "
            "Two retired officers. A physiologist of the senses. <bookmark mark='b'/> And the director of Berlin's "
            "Psychological Institute, Carl Stumpf. They watch Hans work. They watch von Osten for signals. They "
            "have Hans questioned while von Osten is out of the yard. <bookmark mark='c'/> And on the twelfth of "
            "September they sign a report. Tricks are out of the question. Unintentional signs, of the kind they "
            "know about, are excluded too. Thirteen experts looked for the trick, and found none. "
            "<bookmark mark='d'/> They were right about one thing. Nobody was cheating. And the report's last "
            "line asks for a serious investigation, which is where this part begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.15) for p_ in people], lag_ratio=0.18), run_time=7.0)
            vo.wait_until("b")
            self.play(Create(star), FadeIn(stumpf))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(verdict.src, color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def wager(self):
        board = wager_board((
            (r"a division, a subtraction, a logarithm, a forgetting curve", STATUS_COLOR["replicated"]),
            (r"tasks can be taken apart; \ whether the mind's stages can is settled case by case",
             STATUS_COLOR["contested"]),
            None,
        ), font_size=30)
        board.move_to([0, 0.6, 0])
        q = label(r"How do you ask a mind a question without telling it the answer?", font_size=40,
                  color=P.ACCENT).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Remember where Part 1 left Kant's wager. <bookmark mark='a'/> On his first objection, that numbers "
            "can't be applied to the mind, he had lost. On the second, about experiment, he had half a point. "
            "<bookmark mark='b'/> And the third was untouched: the observer disturbs what is observed. Kant meant "
            "watching your own mind. But the horse shows it is worse than that. <bookmark mark='c'/> Thirteen "
            "careful observers, a mind they wanted to understand, and something passed between the two that none "
            "of them could see. <bookmark mark='d'/> So here is the question for today. How do you ask a mind a "
            "question without telling it the answer? Every rule of experimental design in psychology is an answer "
            "to that, and most of them are in the story of this horse."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            vo.wait_until("a")
            self.play(FadeIn(board.rows[0].reply), FadeIn(board.rows[1].reply))
            vo.wait_until("b")
            self.play(FadeIn(board.rows[2].reply), Indicate(board.rows[2].objection, color=KANT, scale_factor=1.08))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 2", font_size=34, color=GREY_B), label(r"The Experiment", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"how one student found what thirteen experts missed, \ and the blind he invented",
            r"compared with what? \ the control group, and six designs that fool their authors",
            r"why assignment is left to a shuffled deck, \ and what the shuffle buys",
            r"each person as their own control: \ what pairing buys, and what it costs",
            r"the experimenter and the subject as sources of the result; \ interactions; \ validity",
            r"the subject is a person: \ the rules that came from getting it wrong",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part two: the experiment. <bookmark mark='a'/> We'll see how one student found what thirteen experts "
            "had missed, and the remedy he invented on the spot. <bookmark mark='b'/> Then the first question to "
            "ask of any study, compared with what, and six tempting designs that fool the people who run them. "
            "<bookmark mark='c'/> Why deciding who gets what is left to a shuffled deck of cards, a trick "
            "psychologists were the first to use. <bookmark mark='d'/> How using each person as their own "
            "control buys a great deal, and what it costs. <bookmark mark='e'/> How the experimenter and the "
            "subject each bend the result, what an interaction is, and four different ways a study can be wrong. "
            "<bookmark mark='f'/> And last, the rules for treating the subject as a person, each of which was "
            "written after somebody failed to."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
