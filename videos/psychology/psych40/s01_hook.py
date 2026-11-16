from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


def shuttle_box(color=GREY_B) -> VGroup:
    """A two-compartment shuttle box with a low barrier."""
    floor = Line([-1.6, 0, 0], [1.6, 0, 0], color=color, stroke_width=4)
    walls = VGroup(Line([-1.6, 0, 0], [-1.6, 1.3, 0], color=color, stroke_width=3),
                   Line([1.6, 0, 0], [1.6, 1.3, 0], color=color, stroke_width=3),
                   Line([0, 0, 0], [0, 0.45, 0], color=color, stroke_width=4))
    grid = VGroup(*[Line([x, 0.02, 0], [x + 0.1, 0.02, 0], color=AUTH, stroke_width=2)
                    for x in np.arange(-1.5, -0.1, 0.2)])
    return VGroup(floor, walls, grid)


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.dogs()
        self.revision()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part is about anxiety and depression, and it touches on suicide. "
            "<bookmark mark='a'/> It's education, not diagnosis or treatment. If any of it touches your own life, "
            "talk to a doctor, a counsellor, or someone you trust. <bookmark mark='b'/> If you're in danger now, call "
            "your local emergency number. In the United States you can call or text nine eight eight. In the UK and "
            "Ireland, Samaritans are on one one six, one two three. And find a helpline dot com lists free, "
            "confidential lines in other countries."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.head))
            vo.wait_until("a")
            self.play(FadeIn(card.body))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.6), run_time=3.0)
        self.wait(1.5)
        self.clear_scene()

    def dogs(self):
        head = heading(r"Dogs that stopped trying")
        groups = VGroup()
        for name, c, note in ((r"escapable shock", GOOD, r"a panel turns it off"),
                              (r"inescapable shock", AUTH, r"yoked: \ same shocks, \ no control"),
                              (r"no shock", GREY_A, r"")):
            box = shuttle_box().scale(0.55)
            dog = little_person(0.5, color=c).move_to(box.get_bottom() + UP * 0.3 + LEFT * 0.45)
            groups.add(VGroup(box, dog, label(name, font_size=15, color=c).next_to(box, DOWN, buff=0.15),
                              label(note, font_size=12, color=GREY_B).next_to(box, DOWN, buff=0.45)))
        groups.arrange(DOWN, buff=0.35).move_to([-4.4, -0.3, 0])
        rows = rows_of([
            (r"Seligman and Maier, \ 1967: \ three groups of dogs; \ one could stop shocks by pressing a panel, \ one "
             r"received the same shocks with no control, \ one received none", WHITE),
            (r"a day later, \ in a shuttle box where jumping a low barrier ended the shock, \ most dogs from the "
             r"inescapable group lay down and took it", AUTH),
            (r"the dogs that had control, \ and those with no shock, \ learned to escape", GOOD),
            (r"the theory: \ they had learned that nothing they did mattered, \ learned helplessness, \ and it "
             r"became a model of depression", YOU),
        ], 7.4, 19, 0.36).move_to([2.6, -0.2, 0])
        tag = historical_tag(r"Seligman \& Maier (1967)")
        with self.voiceover(
            "In 1967 Martin Seligman and Steven Maier ran an experiment that became a theory of depression. "
            "<bookmark mark='a'/> Three groups of dogs. One could stop shocks by pressing a panel. One received "
            "exactly the same shocks, with no control. One received none. <bookmark mark='b'/> A day later they were "
            "put in a shuttle box, where jumping a low barrier ended the shock. Most of the dogs from the "
            "inescapable group lay down and took it. <bookmark mark='c'/> The dogs that had had control, and those "
            "with no shock, learned to escape. <bookmark mark='d'/> The theory: they had learned that nothing they "
            "did mattered. Learned helplessness became one of the founding models of depression."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(groups))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def revision(self):
        head = heading(r"Fifty years later")
        old = VGroup(word_chip(r"1967", color=GREY_A, font_size=20, width=2.0),
                     wrapped_label(r"animals learn that they have no control, \ and become passive", 4.6, 20, WHITE))
        new = VGroup(word_chip(r"2016", color=GOOD, font_size=20, width=2.0),
                     wrapped_label(r"passivity is the default response to prolonged threat; \ what is learned is "
                                   r"control, \ which switches the passivity off", 4.6, 20, GOOD))
        for g in (old, new):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(old, new).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.8, 0])
        rows = rows_of([
            (r"Maier and Seligman, \ 2016: \ the brain circuits of the effect, \ traced in rats, \ ran the other way "
             r"from the theory", WHITE),
            (r"the original authors reversed their own explanation; \ the finding, \ that control protects, \ "
             r"stands", YOU),
        ], 12.0, 21, 0.36).move_to([0, -2.2, 0])
        tag = published_tag(r"Maier \& Seligman (2016)")
        with self.voiceover(
            "Fifty years later its own authors turned it around. <bookmark mark='a'/> In 1967 the idea was that "
            "animals learn they have no control, and so become passive. <bookmark mark='b'/> In 2016, after decades "
            "of tracing the brain circuits in rats, Maier and Seligman concluded the opposite. Passivity is the "
            "default response to prolonged threat. What's learned is control, and control switches the passivity "
            "off. <bookmark mark='c'/> The circuits ran the other way from the theory. <bookmark mark='d'/> The "
            "authors reversed their own explanation. The finding, that control protects, still stands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(old))
            vo.wait_until("b")
            self.play(FadeIn(new))
            for m, r in zip("cd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what are anxiety and depression made of?")
        rows = rows_of([
            (r"anxiety built from conditioning: \ fear that avoidance keeps alive, \ and exposure that removes it", SYMP),
            (r"depression built from reward and control: \ helplessness, \ anhedonia, \ and a model of mood", MODEL),
            (r"what the drugs act on, \ and what the trials say they do", PERSON),
            (r"stress, \ genes and life events; \ bipolar disorder; \ and why suicide is so hard to predict", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks what anxiety and depression are made of, and what treatments act on. "
            "<bookmark mark='a'/> It builds anxiety from the conditioning of Part 16: fear that avoidance keeps "
            "alive, and exposure that removes it. <bookmark mark='b'/> It builds depression from reward and control: "
            "helplessness, anhedonia, and a model of mood. <bookmark mark='c'/> It asks what the drugs act on, and "
            "what the trials say they do. <bookmark mark='d'/> And it turns to stress, genes and life events, to "
            "bipolar disorder, and to why suicide is so hard to predict."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 40", font_size=34, color=GREY_B), label(r"Fear and Sadness", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"anxiety as learning: \ avoidance, \ exposure and the return of fear",
            r"the anxiety disorders in one frame, \ and attention to threat",
            r"depression: \ cognition, \ helplessness and control",
            r"reward, \ anhedonia and a model of momentary mood",
            r"serotonin, \ and what antidepressant trials show",
            r"stress and genes, \ lithium, \ and the limits of predicting suicide",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 40 of Psychology, Built: fear and sadness. <bookmark mark='a'/> We'll treat anxiety as "
            "learning: avoidance, exposure, and the return of fear. We'll put the anxiety disorders in one frame, "
            "and look at attention to threat. We'll take depression through cognition, helplessness and control, "
            "then through reward, with a model of momentary mood. We'll weigh the serotonin story and what "
            "antidepressant trials show. And we'll end with stress and genes, lithium, and the limits of predicting "
            "suicide."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
