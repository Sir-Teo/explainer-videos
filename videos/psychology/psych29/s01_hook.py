from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


def bear(scale: float = 1.0, color="#8B5A2B") -> VGroup:
    """A bear's head: face, ears, snout, eyes, nose."""
    head = Circle(radius=0.9, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0)
    ears = VGroup(*[Circle(radius=0.32, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0).move_to(
        [dx, 0.75, 0]) for dx in (-0.65, 0.65)])
    inner = VGroup(*[Circle(radius=0.15, color="#D2A679", fill_opacity=0.9, stroke_width=0).move_to([dx, 0.75, 0])
                     for dx in (-0.65, 0.65)])
    snout = Ellipse(width=0.8, height=0.55, color="#D2A679", fill_opacity=0.95, stroke_width=0).move_to([0, -0.35, 0])
    nose = Ellipse(width=0.26, height=0.16, color=BLACK, fill_opacity=1, stroke_width=0).move_to([0, -0.22, 0])
    eyes = VGroup(*[Dot([dx, 0.15, 0], radius=0.07, color=BLACK) for dx in (-0.32, 0.32)])
    return VGroup(ears, inner, head, snout, nose, eyes).scale(scale)


class Hook(VoiceoverScene):
    def construct(self):
        self.woods()
        self.order()
        self.question()
        self.objectives()

    def woods(self):
        b = bear(1.0).move_to([-3.6, 0.3, 0])
        heart = label(r"heart racing", font_size=22, color=BODY).move_to([-3.6, -1.6, 0])
        run = Arrow([-2.2, -1.6, 0], [-0.4, -1.6, 0], color=BODY, buff=0)
        rows = rows_of([
            (r"1884: \ William James asks what an emotion is", WHITE),
            (r"common sense: \ we see the bear, \ are afraid, \ and run", COG),
            (r"James: \ we see the bear, \ the body reacts, \ and the feeling \emph{is} our perception of the "
             r"body's reaction", BODY),
            (r"``we feel sorry because we cry, \ angry because we strike, \ afraid because we tremble''", FEAR),
        ], 5.8, 24, 0.38).move_to([3.3, 0.0, 0])
        tag = historical_tag(r"James (1884)")
        with self.voiceover(
            "You are walking in the woods, and a bear steps onto the path. <bookmark mark='a'/> In 1884 William "
            "James asked what happens next, and what an emotion is. <bookmark mark='b'/> Common sense says: you see "
            "the bear, you are afraid, and so you run. <bookmark mark='c'/> James said the order is wrong. You see "
            "the bear, your body reacts, the heart racing, the legs moving, and the feeling of fear is your "
            "perception of those bodily changes. <bookmark mark='d'/> In his words, we feel sorry because we cry, "
            "angry because we strike, afraid because we tremble, and not the other way round."
        ) as vo:
            self.play(FadeIn(b, scale=0.8), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(heart), GrowArrow(run))
            self.play(Indicate(heart, color=BODY))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def order(self):
        head = heading(r"Two orders of events")
        def chain(items, y):
            g = VGroup(*[word_chip(t, color=c, font_size=22) for t, c in items]).arrange(RIGHT, buff=0.9)
            arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
                              for a, b in zip(g, g[1:])])
            return VGroup(g, arrows).move_to([0, y, 0])
        common = chain([(r"the bear", WHITE), (r"fear", FEAR), (r"the body reacts", BODY), (r"run", WHITE)], 1.4)
        james = chain([(r"the bear", WHITE), (r"the body reacts", BODY), (r"the felt fear", FEAR)], -0.6)
        cl = label(r"common sense", font_size=20, color=GREY_B).next_to(common, UP, buff=0.2)
        jl = label(r"James, \ and Lange in 1885", font_size=20, color=BODY).next_to(james, UP, buff=0.2)
        foot = wrapped_label(r"the argument about order has run ever since: \ body first, \ thought first, \ or "
                             r"a brain that builds both", 12.0, 24, COG).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here are the two orders. <bookmark mark='a'/> In common sense, the bear causes fear, and fear causes "
            "the body's reaction. <bookmark mark='b'/> In James's account, and in the Danish physician Carl Lange's "
            "a year later, the bear causes the body's reaction, and the felt emotion comes last: it is the body, "
            "perceived. <bookmark mark='c'/> Psychology has argued about the order ever since. Does the body come "
            "first, or a thought about the situation, or does the brain build both at once?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cl), FadeIn(common))
            vo.wait_until("b")
            self.play(FadeIn(jl), FadeIn(james))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what is an emotion?")
        rows = rows_of([
            (r"the body and the label: \ James, \ Cannon, \ adrenaline and a rickety bridge", BODY),
            (r"faces: \ six basic emotions, \ and what happens without a list to choose from", FACE),
            (r"a map of feelings recovered from 1962 data, \ and from you", PLEAS),
            (r"a pen in the teeth, \ seventeen laboratories, \ and 286 effect sizes", COG),
            (r"appraisal, \ fear circuits, \ forecasting, \ money, \ and a ratio that was withdrawn", FEAR),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So: what is an emotion, and where does it come from? <bookmark mark='a'/> We'll start with the body "
            "and the label: James, his critic Walter Cannon, an injection of adrenaline, and a rickety bridge. "
            "<bookmark mark='b'/> Then faces: the claim of six universal emotions, and what happens when people "
            "aren't given a list to choose from. <bookmark mark='c'/> Then a map of feelings, recovered from data "
            "collected in 1962, and then from you. <bookmark mark='d'/> Then a pen held in the teeth, seventeen "
            "laboratories, and two hundred and eighty-six effect sizes. <bookmark mark='e'/> And then appraisal, "
            "fear in the brain, how badly we forecast our own feelings, what money does for happiness, and a magic "
            "number that was withdrawn."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 29", font_size=34, color=GREY_B), label(r"Emotion", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"James--Lange, \ Cannon's objections, \ and two factors as inference",
            r"basic emotions and their critics, \ and the circumplex recovered by scaling",
            r"facial feedback: \ the original, \ the null, \ and the meta-analysis recomputed",
            r"appraisal computed, \ and the two roads to the amygdala",
            r"regulation, \ forecasting, \ and money and happiness reconciled",
            r"a famous ratio and how it was taken apart",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 29 of Psychology, Built: emotion. <bookmark mark='a'/> We'll weigh James and Lange against "
            "Cannon's objections, and write the two-factor theory as inference. We'll test the basic emotions "
            "against their critics, and recover the circumplex by multidimensional scaling. We'll follow facial "
            "feedback from the original study to its null replication and recompute its meta-analysis from the "
            "open data. We'll compute an appraisal model and LeDoux's two roads to the amygdala. We'll cover "
            "regulation, forecasting, and money and happiness, reconciled. And we'll end with a famous ratio, and "
            "how a graduate student and a physicist took it apart."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
