from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.committee()
        self.addition()
        self.numbers()
        self.objectives()

    def committee(self):
        d = archive.STEVENS_1946.data
        head = heading(rf"{d['appointed']}: \ a committee of the British Association")
        crowd = people_row(d["members"], P.HUMAN, height=0.72, buff=0.22, per_row=7).move_to([-3.6, 0.75, 0])
        who = label(rf"{d['members']} members, from physics and from psychology", font_size=28, color=GREY_A)
        who.next_to(crowd, DOWN, buff=0.3)
        q = VGroup(label(r"their question", font_size=26, color=GREY_B),
                   label(r"Can a sensation be measured?", font_size=46, color=P.ACCENT)).arrange(DOWN, buff=0.15)
        q.move_to([3.45, 1.75, 0])
        # the test case: two tones, one meant to sound twice as loud as the other
        def tone(k, color):
            arcs = VGroup(*[Arc(radius=0.3 + 0.26 * i, start_angle=-0.7, angle=1.4, color=color, stroke_width=6)
                            for i in range(k)])
            return VGroup(Dot(radius=0.13, color=color), arcs)

        one, two = tone(2, GREY_A), tone(4, P.ACCENT)
        sone = VGroup(VGroup(one, label(r"1 sone", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.2),
                      VGroup(two, label(r"2 sones: \ twice as loud?", font_size=30, color=P.ACCENT)).arrange(DOWN, buff=0.2))
        sone.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to([3.45, -0.35, 0])
        years = VGroup(
            label(rf"{d['interim_report']} \ \ interim report: \ no agreement", font_size=38, color=GREY_A),
            label(rf"{d['final_report']} \ \ final report: \ no agreement", font_size=38, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -2.55, 0])
        src = historical_tag(archive.STEVENS_1946.cite)
        with self.voiceover(
            "In 1932 the British Association for the Advancement of Science appoints a committee. "
            f"<bookmark mark='a'/> It has {d['members']} members, physicists and psychologists, and one question to "
            "settle: is it possible to measure a human sensation? <bookmark mark='b'/> They have a test case in "
            "front of them. A laboratory at Harvard has published a scale of loudness, in units called sones, built "
            "so that a tone of two sones should sound twice as loud as a tone of one. Is that a measurement, in "
            "the sense in which a length is measured? <bookmark mark='c'/> The committee argues for six years and "
            "produces an interim report, in which one member complains that his colleagues came out by the same "
            "door they went in. They ask for more time. <bookmark mark='d'/> In 1940 comes the final report. It "
            "doesn't reach a conclusion. It prints the members' separate opinions, and they run from yes to never."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in crowd], lag_ratio=0.08), FadeIn(who), run_time=2.5)
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sone[0]), run_time=0.8)
            self.play(FadeIn(sone[1]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(years[0], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(years[1], shift=RIGHT * 0.2))
        self.clear_scene()

    def addition(self):
        head = heading(r"The physicists' objection: \ no addition, no measurement")
        unit = 1.1
        x0, y0 = -6.2, 1.3

        def rod(n, color):
            return Rectangle(width=n * unit, height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.95)

        ruler = VGroup(Line([x0, y0 - 0.55, 0], [x0 + 5 * unit, y0 - 0.55, 0], color=GREY_B, stroke_width=2))
        for i in range(6):
            ruler.add(Line([x0 + i * unit, y0 - 0.55, 0], [x0 + i * unit, y0 - 0.42, 0], color=GREY_B, stroke_width=2))
            ruler.add(label(rf"{i}", font_size=24, color=GREY_B).move_to([x0 + i * unit, y0 - 0.82, 0]))
        a = rod(2, GROUP_A).move_to([x0 + 1 * unit, y0 + 0.75, 0])
        b = rod(3, GROUP_B).move_to([x0 + 1.5 * unit, y0 + 1.3, 0])
        rule = label(r"lay them end to end: \ $2 + 3 = 5$", font_size=36, color=WHITE).move_to([3.5, 1.75, 0])
        note1 = wrapped_label(r"lengths can be added, by something you can do with the rods; \ that is why a "
                              r"length of 5 means five of the unit", 5.9, 28, GREY_A).next_to(rule, DOWN, buff=0.25)
        loud = VGroup(label(r"loudness, pain, brightness, liking", font_size=34, color=P.ACCENT),
                      label(r"what would it mean to lay two of them end to end?", font_size=30, color=GREY_A))
        loud.arrange(DOWN, buff=0.15).move_to([0, -0.4, 0])
        quote = quote_card(r"``Any law purporting to express a quantitative relation between sensation intensity and "
                           r"stimulus intensity is not merely false but is in fact meaningless unless and until a "
                           r"meaning can be given to the concept of addition as applied to sensation.''",
                           r"a member of the committee, final report (1940), as quoted by Stevens (1946)",
                           width=12.2, font_size=27, color=KANT).move_to([0, -2.1, 0])
        src = historical_tag(archive.STEVENS_1946.cite)
        with self.voiceover(
            "The deepest objection came from the physicists, and it rested on an account of measurement that one "
            "of the members, Norman Campbell, had worked out for physics. <bookmark mark='a'/> Why is length "
            "measurable? Because lengths add. Take a rod of two units and a rod of three, <bookmark mark='b'/> lay "
            "them end to end, and you get a rod of five. The arithmetic of the numbers copies something you can "
            "do with the objects. That's what gives the number five its meaning. <bookmark mark='c'/> Now try it "
            "with loudness. Or pain, or brightness, or how much you like something. There's nothing you can do "
            "with two sensations that corresponds to laying them end to end. <bookmark mark='d'/> So one member "
            "wrote that any law relating the intensity of a sensation to the intensity of its stimulus is not "
            "merely false, but meaningless, until someone says what addition means for sensations. Notice what "
            "he's claiming. He isn't saying that Fechner's law, from Part 1, has the wrong shape. He's saying it "
            "doesn't say anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(ruler), FadeIn(a), FadeIn(b))
            vo.wait_until("b")
            self.play(a.animate.move_to([x0 + 1 * unit, y0 - 0.2, 0]), b.animate.move_to([x0 + 3.5 * unit, y0 - 0.2, 0]),
                      run_time=1.6)
            self.play(FadeIn(rule), FadeIn(note1))
            vo.wait_until("c")
            self.play(FadeIn(loud, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()

    def numbers(self):
        board = wager_board((
            (r"a division, a subtraction, a logarithm, a forgetting curve", STATUS_COLOR["replicated"]),
            (r"minds can be compared fairly: \ a control, a shuffle, a balanced order", STATUS_COLOR["replicated"]),
            (r"the observer can be designed out, with a blind, \ where a blind can be kept", P.ACCENT),
        ), font_size=30)
        board.to_edge(UP, buff=0.3)
        mark = label(r"numbers, yes. \ But measurements?", font_size=28, color=P.ERR)
        mark.next_to(board.rows[0].reply, DOWN, buff=0.08).align_to(board.rows[0].reply, LEFT)
        for r in board.rows[1:]:  # make room under the first reply
            r.shift(DOWN * 0.3)
        qs = VGroup(
            label(r"1 \ \ What does the number mean?", font_size=36, color=SCALE["interval"]),
            label(r"2 \ \ How much of it is error?", font_size=36, color=ERRC),
            label(r"3 \ \ Does it measure what its name says?", font_size=36, color=TRUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This matters for everything we've done so far. <bookmark mark='a'/> Kant's first objection was that "
            "mathematics can't be applied to the mind, and Part 1 answered it with numbers: a reaction time, a "
            "threshold, a forgetting curve. <bookmark mark='b'/> The committee's point is sharper than Kant's. "
            "Having a number is not the same as having measured something. A reaction time in milliseconds, a "
            "rating of four out of five, a score on a test of intelligence: these are all numbers, and they are "
            "not all numbers in the same sense. <bookmark mark='c'/> So today we ask three things of a number "
            "attached to a mind. What does it mean: which statements about it say something? <bookmark mark='d'/> "
            "How much of it is error? <bookmark mark='e'/> And does it measure what its name says it measures? "
            "Every number in the rest of this series is worth as much as the answers to those three."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            vo.wait_until("a")
            self.play(*[FadeIn(r.reply) for r in board.rows])
            vo.wait_until("b")
            self.play(FadeIn(mark, shift=UP * 0.1))
            for m, q in zip("cde", qs):
                vo.wait_until(m)
                self.play(FadeIn(q, shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 3", font_size=34, color=GREY_B), label(r"The Measure", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"what a number survives: \ four kinds of scale, and the quarrel over averaging ratings",
            r"a reading of your character, on you; \ and why feeling accurate proves nothing",
            r"true score and error: \ reliability, Spearman's correction, and why longer tests are better",
            r"validity: \ does a test measure what its name says?",
            r"two names for one thing, \ and what a construct is",
            r"what people can report about themselves; \ and the reliability paradox",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part three: the measure. <bookmark mark='a'/> We start with the reply that a Harvard psychologist "
            "made to the committee: ask what you may do to a number without destroying what it records. That "
            "gives four kinds of scale, and settles an old quarrel about averaging ratings. <bookmark mark='b'/> "
            "Then a reading of your character, which you'll rate for accuracy, and what your rating is worth. "
            "<bookmark mark='c'/> The second question, error: a score is a true score plus noise, and from that "
            "one line come reliability, Spearman's correction, and the reason longer tests are better tests. "
            "<bookmark mark='d'/> The third and hardest: validity. <bookmark mark='e'/> Then what happens when "
            "one thing gets two names, and what kind of thing a psychological attribute is supposed to be. "
            "<bookmark mark='f'/> And last, two warnings: what people can and can't tell you about themselves, "
            "and why the best experiments make the worst tests."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
