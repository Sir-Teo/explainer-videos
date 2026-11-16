from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Priming(VoiceoverScene):
    def construct(self):
        self.card()
        self.hallway()
        self.doyen()
        self.solid()

    def card(self):
        card = chapter_card(7, r"Priming and its collapse", r"Can a word make you walk more slowly?",
                            lit={1996: r"Bargh et al.", 2012: r"Doyen et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter seven. Priming and its collapse."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hallway(self):
        head = heading(r"The walk to the elevator")
        hall = VGroup(Line([-6.0, -0.4, 0], [0.0, -0.4, 0], color=GREY_B, stroke_width=3),
                      Line([-6.0, 0.6, 0], [0.0, 0.6, 0], color=GREY_B, stroke_width=3))
        walker = Dot([-5.6, 0.1, 0], radius=0.16, color=PERSON)
        words = VGroup(*[label(w, font_size=20, color=CROWD) for w in (r"Florida", r"grey", r"wrinkle", r"bingo")])
        words.arrange(RIGHT, buff=0.4).move_to([-3.0, 1.8, 0])
        rows = rows_of([
            (r"Bargh, \ Chen and Burrows, \ 1996: \ students unscrambled sentences; \ for some, \ the words "
             r"evoked old age", WHITE),
            (r"leaving, \ those students walked down the hallway more slowly, \ timed by an experimenter with a stopwatch", PERSON),
            (r"it became the most famous example of behavioural priming: \ a concept, \ activated without your "
             r"knowing, \ steering what you do", CROWD),
        ], 5.4, 20, 0.36).move_to([3.6, -0.2, 0])
        tag = historical_tag(r"Bargh, \ Chen \& Burrows (1996)")
        with self.voiceover(
            "The most famous claims of social cognition in the 1990s were about priming. <bookmark mark='a'/> In "
            "1996 Bargh, Chen and Burrows had students unscramble sentences. For some of them, the words evoked "
            "old age. <bookmark mark='b'/> When they left, those students walked down the hallway more slowly, "
            "timed by an experimenter with a stopwatch. <bookmark mark='c'/> "
            "It became the most famous example of behavioural priming: a concept, activated without your knowing, "
            "steering what you do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hall), FadeIn(walker))
            vo.wait_until("a")
            self.play(FadeIn(words), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(walker.animate.move_to([-0.4, 0.1, 0]), FadeIn(rows[1]), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def doyen(self):
        head = heading(r"Infrared beams, \ and expectations")
        A = axes([-0.6, 1.6], [0, 1.0], x_length=5.0, y_length=3.4, xticks=None, yticks=None,
                 ylabel=r"how much slower the primed group walked", center=[-3.6, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [0.03, 0.6], [GREY_B, AUTH], width=0.6)
        names = VGroup(*[wrapped_label(t, 2.0, 14, c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15) for k, (t, c) in
                         enumerate(((r"infrared sensors, \ blind experimenters", GREY_B),
                                    (r"experimenters expecting slowness", AUTH)))])
        note = label(r"the pattern reported, \ drawn schematically", font_size=15, color=GREY_B).next_to(A, UP, buff=0.1)
        rows = rows_of([
            (r"Doyen, \ Klein, \ Pichon and Cleeremans, \ 2012: \ the same study with walking speed timed by "
             r"infrared sensors: \ no effect", WHITE),
            (r"a slowing appeared only when the experimenters had been led to expect it", AUTH),
            (r"the likely source of the original effect: \ the people doing the measuring", MODEL),
            (r"later that year Daniel Kahneman wrote to priming researchers that he saw ``a train wreck looming'', "
             r"\ and asked them to replicate their own findings", YOU),
        ], 5.8, 19, 0.34).move_to([3.4, -0.3, 0])
        tag = published_tag(r"Doyen et al.\ (2012)")
        with self.voiceover(
            "Then people tried to repeat it. <bookmark mark='a'/> In 2012 Doyen and colleagues ran the "
            "same study, but timed walking speed with infrared sensors. There was no effect. "
            "<bookmark mark='b'/> A slowing appeared only when the experimenters had been led "
            "to expect it. <bookmark mark='c'/> The likely source of the original effect was the people doing the "
            "measuring. <bookmark mark='d'/> Later that year Daniel Kahneman, who had featured priming in his "
            "best-selling book, wrote to priming researchers that he saw a train wreck looming, and asked them to "
            "replicate their own findings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(note))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def solid(self):
        head = heading(r"What kind of priming is solid?")
        left = VGroup(word_chip(r"solid", color=GOOD, font_size=24, width=5.0),
                      wrapped_label(r"semantic priming: \ ``doctor'' speeds the recognition of ``nurse'' by tens of "
                                    r"milliseconds, \ measured by computer, \ in Part 22", 5.0, 20, WHITE),
                      wrapped_label(r"repetition priming: \ a word seen once is read faster the next time", 5.0, 20,
                                    WHITE)).arrange(DOWN, buff=0.3).move_to([-3.4, 0.3, 0])
        right = VGroup(word_chip(r"failed or unproven", color=AUTH, font_size=24, width=5.0),
                       wrapped_label(r"behavioural priming: \ words about old age slowing walking, \ money making "
                                     r"people selfish, \ a professor making them smarter", 5.0, 20, WHITE),
                       wrapped_label(r"the effects were large, \ the samples small, \ and the measures loose", 5.0, 20,
                                     WHITE)).arrange(DOWN, buff=0.3).move_to([3.4, 0.3, 0])
        foot = wrapped_label(r"the line is not ``priming exists'' against ``priming does not'': \ it is fast, \ "
                             r"measured effects inside a task against large effects on distant behaviour", 12.0, 21,
                             YOU).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So what's left? <bookmark mark='a'/> Semantic priming is solid. The word doctor speeds the "
            "recognition of nurse by tens of milliseconds, measured by computer, as in Part 22. So is repetition "
            "priming. <bookmark mark='b'/> What failed, or was never shown, is behavioural priming of the dramatic "
            "kind: words about old age slowing walking, money making people selfish, thinking of a professor "
            "making them smarter. The effects were large, the samples small and the measures loose. "
            "<bookmark mark='c'/> The line isn't between priming existing and not existing. It's between fast, "
            "measured effects inside a task, and large effects on distant behaviour."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
