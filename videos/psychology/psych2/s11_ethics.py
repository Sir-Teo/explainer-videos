from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403

RESPECT, BENEFIT, JUSTICE = "#7EC8F5", "#7BD88F", "#F2C14E"


class Ethics(VoiceoverScene):
    def construct(self):
        self.card()
        self.deceived()
        self.tuskegee()
        self.belmont()
        self.series_rule()

    def card(self):
        card = chapter_card(10, r"The subject is a person", r"What may an experimenter do to find something out?",
                            lit={1963: r"Milgram's obedience study", 1972: r"Tuskegee exposed",
                                 1979: r"the Belmont Report"}, part=PART, scale=("person", "culture"),
                            marr=("what",))
        with self.voiceover(
            "Chapter ten. The subject is a person."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def deceived(self):
        head = heading(r"Every design so far kept something from someone")
        rows = VGroup()
        for who, what in ((r"the students with the rats", r"were told a false story about their animals"),
                          (r"the teachers", r"were given a list that meant nothing"),
                          (r"the dog handlers", r"were told where a scent was that did not exist")):
            rows.add(VGroup(label(who, font_size=30, color=P.ACCENT), label(what, font_size=30, color=WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5)
        n, went = 40, 26
        cols = [BIAS] * went + [GREY_B] * (n - went)
        crowd = people_row(n, cols, height=0.5, buff=0.12, per_row=20).move_to([0, -1.25, 0])
        m_head = label(r"Milgram, 1963: \ ``a study of memory''. \ 40 men are told to give another man electric "
                       r"shocks.", font_size=28, color=WHITE).next_to(crowd, UP, buff=0.3)
        m_res = VGroup(label(rf"{went} of {n}", font_size=44, color=BIAS),
                       label(r"went to the last switch. \ There were no shocks; \ they did not know that.",
                             font_size=28, color=WHITE)).arrange(RIGHT, buff=0.35).next_to(crowd, DOWN, buff=0.3)
        with self.voiceover(
            "Look back over this part, and something should bother you. <bookmark mark='a'/> The students with "
            "the rats were lied to. So were the teachers, and the dog handlers. A blind is a way of keeping "
            "someone in the dark, and with a horse that costs nothing. With a person it does. "
            "<bookmark mark='b'/> The case everyone knows is Stanley Milgram's, at Yale, in 1963. Forty men "
            "came for what they were told was a study of memory, and were instructed to give stronger and "
            "stronger electric shocks to another man each time he made a mistake. <bookmark mark='c'/> "
            f"{went} of the {n} went on to the last switch on the board. There were no shocks. The other man was "
            "an actor. But the forty didn't know that, and many of them were visibly shaken. Part 34 tells what "
            "the study did and didn't show. Here the question is the other one: was it all right to do it? "
            "The argument over that began within a year, and it has not stopped."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            grey = crowd.copy()
            for p_ in grey:
                p_.set_color(P.HUMAN)
            self.play(FadeIn(m_head), FadeIn(grey, lag_ratio=0.02))
            vo.wait_until("c")
            self.play(ReplacementTransform(grey, crowd), FadeIn(m_res, shift=UP * 0.15))
        self.clear_scene()

    def tuskegee(self):
        head = heading(r"Tuskegee, Alabama, 1932 to 1972")
        line = NumberLine(x_range=[1930, 1975, 5], length=11.0, include_ticks=True, color=GREY_B, stroke_width=3)
        line.move_to([0, 0.4, 0])
        yrs = VGroup(*[label(str(y), font_size=22, color=GREY_A).next_to(line.n2p(y), DOWN, buff=0.2)
                       for y in (1930, 1940, 1950, 1960, 1970)])
        span = Line(line.n2p(1932), line.n2p(1972), color=BIAS, stroke_width=10)
        s_lab = label(r"399 Black men with syphilis are observed, and not treated", font_size=28, color=BIAS)
        s_lab.next_to(span, UP, buff=0.25)
        pen = VGroup(Line(line.n2p(1947) + UP * 0.25, line.n2p(1947) + DOWN * 0.9, color=TRUTH, stroke_width=3),
                     label(r"penicillin is the standard cure", font_size=24, color=TRUTH))
        pen[1].next_to(pen[0], DOWN, buff=0.08)
        end = VGroup(Line(line.n2p(1972) + UP * 0.25, line.n2p(1972) + DOWN * 1.6, color=WHITE, stroke_width=3),
                     label(r"a newspaper report ends it", font_size=24, color=WHITE))
        end[1].next_to(end[0], DOWN, buff=0.08)
        if end[1].get_right()[0] > 6.9:
            end[1].shift(LEFT * (end[1].get_right()[0] - 6.9))
        text = wrapped_label(r"They were told they were being treated for ``bad blood''. \ They were never asked, "
                             r"and never told.", 12.2, 30, WHITE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "And there are cases with no argument at all. From 1932, the United States Public Health Service "
            "followed about four hundred Black men with syphilis in Tuskegee, Alabama, to record what the "
            "disease does when it isn't treated. <bookmark mark='a'/> The men were told they were being "
            "treated. <bookmark mark='b'/> By the late nineteen-forties penicillin was the standard cure. They "
            "weren't given it. <bookmark mark='c'/> The study ran for forty years, and it stopped in 1972 "
            "because a newspaper reported it. <bookmark mark='d'/> This is the history behind every consent "
            "form you'll ever sign. The rules that follow weren't worked out from first principles. Each was "
            "written after somebody was harmed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(line), FadeIn(yrs))
            vo.wait_until("a")
            self.play(Create(span), FadeIn(s_lab), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pen, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(text, shift=UP * 0.15))
        self.clear_scene()

    def belmont(self):
        head = heading(r"The Belmont Report, 1979: \ three principles")
        cards = VGroup()
        for name, means, practice, color in (
            (r"Respect for persons", r"people decide for themselves", r"informed consent; \ the right to leave "
                                                                     r"at any moment, without giving a reason",
             RESPECT),
            (r"Beneficence", r"do no harm, and weigh what is left", r"risks set against benefits, by someone other "
                                                                    r"than the researcher: \ an ethics board",
             BENEFIT),
            (r"Justice", r"who bears the burden, and who gets the benefit?", r"no group is studied because it is "
                                                                             r"convenient or powerless", JUSTICE),
        ):
            t = VGroup(label(name, font_size=34, color=color), label(means, font_size=26, color=WHITE),
                       wrapped_label(practice, 3.6, 23, GREY_A)).arrange(DOWN, buff=0.2)
            box = RoundedRectangle(width=4.2, height=3.3, corner_radius=0.15, stroke_color=color, stroke_width=2.5,
                                   fill_color=CARD_FILL, fill_opacity=0.95)
            t.move_to(box)
            if t.width > 3.9:
                t.scale_to_fit_width(3.9)
            cards.add(VGroup(box, t))
        cards.arrange(RIGHT, buff=0.3).move_to([0, 0.35, 0])
        dec = wrapped_label(r"Deception: \ only when the question cannot be asked without it, never about the "
                            r"risks, and always followed by a full account (debriefing).", 12.6, 28, P.ACCENT)
        dec.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 1979 a national commission in the United States, set up after Tuskegee, put the rules on three "
            "principles, and most of the world's research ethics still follows them. <bookmark mark='a'/> "
            "Respect for persons. People decide for themselves whether to take part, knowing what's involved, "
            "and they can leave whenever they like. <bookmark mark='b'/> Beneficence. Don't harm, and where "
            "some risk remains, weigh it against the benefit. And don't let the researcher be the one who does "
            "the weighing. That's what an ethics board is for. <bookmark mark='c'/> And justice. Ask who "
            "carries the burden of the research, and who gets the benefit. In Tuskegee, those were different "
            "people. <bookmark mark='d'/> Where does that leave the blind? Deception is still allowed, under "
            "conditions. Only when the question can't be asked honestly. Never about the risks. And followed by "
            "a debriefing, in which the subject is told everything. Notice that these are design constraints, "
            "like counterbalancing. A good design is one that answers the question and that you'd be willing to "
            "explain to the people in it."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abc", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(dec, shift=UP * 0.15))
        self.clear_scene()

    def series_rule(self):
        stage = demo_stage(width=11.0, height=3.6, center=[0, 0.2, 0])
        c = stage.box.get_center()
        rules = VGroup(
            label(r"You are told what each experiment is before you do it.", font_size=32),
            label(r"Any surprise is explained straight afterwards.", font_size=32),
            label(r"Nothing you do is stored, or leaves your screen.", font_size=32),
            label(r"You can skip any of them.", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(c)
        with self.voiceover(
            "This series runs experiments on you, so here are its rules. <bookmark mark='a'/> You're told what "
            "each one is before you do it. <bookmark mark='b'/> Where an experiment needs a surprise to work, "
            "the surprise is explained as soon as it's over. <bookmark mark='c'/> Nothing you do is recorded. "
            "On the course site the experiments run in your own browser, and your data never leave it. "
            "<bookmark mark='d'/> And you can skip any of them. The films still make sense."
        ) as vo:
            self.play(FadeIn(stage))
            for mark, r in zip("abcd", rules):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
