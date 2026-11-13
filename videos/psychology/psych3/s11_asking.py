from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


def face(kind: int, height: float = 1.5) -> VGroup:
    """A photograph of a face, as a card with a simple drawing on it; ``kind`` 0 or 1 gives two different faces."""
    cardw = height * 0.78
    back = RoundedRectangle(width=cardw, height=height, corner_radius=0.08, stroke_color=WHITE, stroke_width=2,
                            fill_color="#222A38", fill_opacity=1)
    skin = Ellipse(width=cardw * 0.58, height=height * 0.6, stroke_width=0, fill_color=P.HUMAN, fill_opacity=0.9)
    skin.shift(DOWN * height * 0.03)
    eyes = VGroup(Dot(radius=0.035, color=BLACK), Dot(radius=0.035, color=BLACK)).arrange(RIGHT, buff=cardw * 0.2)
    eyes.move_to(skin.get_center() + UP * height * 0.07)
    if kind == 0:
        hair = Arc(radius=cardw * 0.33, start_angle=0.15, angle=PI - 0.3, color="#8A5A2B", stroke_width=9)
        mouth = Arc(radius=0.14, start_angle=PI + 0.5, angle=PI - 1.0, color=BLACK, stroke_width=3)
    else:
        hair = Arc(radius=cardw * 0.33, start_angle=-0.35, angle=PI + 0.7, color="#3A3A3A", stroke_width=7)
        mouth = Line(LEFT * 0.12, RIGHT * 0.12, color=BLACK, stroke_width=3)
    hair.move_to(skin.get_top() + DOWN * height * 0.03)
    mouth.move_to(skin.get_center() + DOWN * height * 0.15)
    return VGroup(back, skin, hair, eyes, mouth)


class Asking(VoiceoverScene):
    def construct(self):
        self.card()
        self.thesis()
        self.faces()
        self.limits()

    def card(self):
        card = chapter_card(10, r"Asking people", r"What can a person report about their own mind?",
                            lit={1977: r"Nisbett \& Wilson", 2005: r"choice blindness"}, part=PART,
                            scale=("mind", "person"), marr=("what",))
        with self.voiceover(
            "Chapter ten. Asking people."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def thesis(self):
        hc = history_card(1977, r"Richard Nisbett and Timothy Wilson", r"``Telling more than we can know: \ verbal "
                          r"reports on mental processes''", color=P.ARCHIVE, width=7.6, font_size=26)
        hc.to_edge(UP, buff=0.4)

        def box(text, color, w=3.0):
            t = wrapped_label(text, w - 0.4, 26, WHITE)
            return VGroup(panel(w, 1.3, color=color), t)

        cause = box(r"something moves the person", ERRC).move_to([-4.6, 0.35, 0])
        act = box(r"they act", GREY_B, 2.2).move_to([-0.9, 0.35, 0])
        ask = box(r"``Why did you do that?''", P.ACCENT, 3.4).move_to([2.9, 0.35, 0])
        a1 = Arrow(cause.get_right(), act.get_left(), color=GREY_B, stroke_width=4, buff=0.1)
        a2 = Arrow(act.get_right(), ask.get_left(), color=GREY_B, stroke_width=4, buff=0.1)
        theory = box(r"a theory of why people do such things", GROUP_A, 4.2).move_to([2.9, -1.9, 0])
        a3 = Arrow(theory.get_top(), ask.get_bottom(), color=GROUP_A, stroke_width=4, buff=0.1)
        cross = DashedLine(cause.get_bottom() + DOWN * 0.1, theory.get_left() + LEFT * 0.1, color=ERRC, stroke_width=3)
        cross_l = label(r"not consulted", font_size=24, color=ERRC).next_to(cross.get_center(), DL, buff=0.1)
        obs = wrapped_label(r"an onlooker, asked to guess, gives the same answer", 4.0, 26, GROUP_A)
        obs.next_to(theory, LEFT, buff=0.4).shift(DOWN * 0.9 + RIGHT * 0.3)
        tag = note(r"schematic").to_corner(UR, buff=0.2)
        with self.voiceover(
            "The cheapest instrument in psychology is the question. Most of what's known about personality, "
            "attitudes, mood and wellbeing comes from asking. So what can a person report about their own mind? "
            "In 1977 Richard Nisbett and Timothy Wilson reviewed the experiments and reached an uncomfortable "
            "answer. <bookmark mark='a'/> Take any study in which the experimenter knows what moved people, "
            "because the experimenter moved it. <bookmark mark='b'/> Then ask the people why they did what they "
            "did. <bookmark mark='c'/> They answer at once, and with confidence. But the answers often leave "
            "out the thing that moved them, and name things that didn't. <bookmark mark='d'/> Where do the "
            "answers come from, then? Nisbett and Wilson's proposal: from the person's theory of why people in "
            "general do such things. And the evidence for that is neat. <bookmark mark='e'/> Ask onlookers, who "
            "weren't in the experiment, to guess why someone would act that way, and they give the same "
            "answers. The person isn't reading off an inner record. They're explaining themselves the way they'd "
            "explain a stranger."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cause), GrowArrow(a1), FadeIn(act))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(ask))
            vo.wait_until("d")
            self.play(FadeIn(theory), GrowArrow(a3), Create(cross), FadeIn(cross_l))
            vo.wait_until("e")
            self.play(FadeIn(obs, shift=UP * 0.1))
        self.clear_scene()

    def faces(self):
        d = archive.JOHANSSON_2005.data
        head = heading(r"Choice blindness")
        fa, fb = face(0, 2.1).move_to([-5.3, 1.2, 0]), face(1, 2.1).move_to([-3.0, 1.2, 0])
        hand = Arrow([-5.3, -0.95, 0], [-5.3, 0.05, 0], color=P.ACCENT, stroke_width=6, buff=0)
        step = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"1. \ choose the more attractive face", WHITE),
            (r"2. \ the photographs are secretly exchanged", ERRC),
            (r"3. \ ``Why did you choose this one?''", P.ACCENT))])
        step.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.7, -2.0, 0])
        detected = round(100 * d["detected_at_most"])
        grid = VGroup(*[Square(0.27, stroke_width=0, fill_color=(P.ACCENT if i < detected else "#3A4150"), fill_opacity=1)
                        for i in range(100)]).arrange_in_grid(rows=5, cols=20, buff=0.06).move_to([3.4, 1.55, 0])
        g_cap = VGroup(label(rf"of every 100 exchanges, at most {detected} were noticed", font_size=28, color=P.ACCENT),
                       label(rf"{d['n']} people, {d['trials']} choices each, {d['manipulated']} of them exchanged",
                             font_size=22, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(grid, DOWN, buff=0.25)
        more = VGroup(
            wrapped_label(r"For the rest, people gave reasons for a choice they had not made, as readily as for "
                          r"the ones they had.", 6.2, 26, WHITE),
            wrapped_label(rf"Of those who noticed nothing, {100 * d['would_have_noticed']:.0f}\% said they would "
                          r"have noticed such a trick.", 6.2, 26, ERRC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g_cap, DOWN, buff=0.4)
        src = published_tag(archive.JOHANSSON_2005.cite)
        with self.voiceover(
            "For nearly thirty years that claim was hard to test head on, because you'd need to know what a person's "
            "real reasons were. Then in 2005 a group in Sweden found a way, with a conjuring trick. "
            "<bookmark mark='a'/> You're shown two photographs of faces and asked which is more attractive. You "
            "point. <bookmark mark='b'/> The experimenter hands you the one you chose, and asks why you chose "
            "it. Except that on some trials, by sleight of hand, <bookmark mark='c'/> you're handed the other "
            f"one: the face you rejected. <bookmark mark='d'/> Counting every sign of suspicion, no more than "
            f"{detected} per cent of those exchanges were noticed. <bookmark mark='e'/> The rest of the time "
            "people looked at the face they hadn't chosen, and explained why they'd chosen it. Something like: "
            "I liked her smile. And those explanations were hard to tell apart from the ones for real choices. "
            f"<bookmark mark='f'/> Afterwards, {100 * d['would_have_noticed']:.0f} per cent of the people who had "
            "noticed nothing said they'd certainly have noticed a trick like that. The same result has since "
            "been found with the taste of jam and the smell of tea, at a supermarket stall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(fa), FadeIn(fb), FadeIn(step[0]))
            self.play(GrowArrow(hand))
            vo.wait_until("c")
            self.play(fa.animate.move_to(fb.get_center()), fb.animate.move_to(fa.get_center()), FadeIn(step[1]),
                      run_time=1.2)
            self.play(FadeIn(step[2]))
            vo.wait_until("d")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(g_cap), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(more[0]))
            vo.wait_until("f")
            self.play(FadeIn(more[1]))
        self.clear_scene()

    def limits(self):
        head = heading(r"So what is a self-report worth?")
        rows = VGroup()
        for q, a, color in (
                (r"what I see, feel or intend, now", r"reportable; \ a measurement like any other, with its error",
                 TRUE),
                (r"how I usually behave", r"a summary of memory and self-image; \ useful, and coloured by both",
                 SCALE["interval"]),
                (r"why I did what I did", r"a theory, held by the person it is about", ERRC)):
            ql = label(q, font_size=38, color=color)
            al = label(a, font_size=28, color=GREY_A)
            rows.add(VGroup(ql, al).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.75, 0])
        end = VGroup(
            label(r"Treat an answer as a measurement, with a reliability and a validity argument of its own.",
                  font_size=28, color=P.ACCENT),
            label(r"Where you can, measure the behaviour as well: \ a second method.", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "It would be easy to take the wrong lesson from this, which is that asking people is worthless. "
            "It isn't, and the finding has limits that matter. <bookmark mark='a'/> People can tell you a good "
            "deal about what they see, feel and intend at this moment. That's a measurement, with error, like "
            "any other, and Part 11 is built on it. <bookmark mark='b'/> They can tell you how they usually "
            "behave, which is what a personality questionnaire asks. That's a summary of memory and of "
            "self-image, and it's coloured by both, but as we'll see it predicts real outcomes. "
            "<bookmark mark='c'/> What they can't reliably give you is the cause of their own behaviour. That's "
            "a theory, and its author has no special access. <bookmark mark='d'/> So the practical rule is the "
            "one this whole part has been building. An answer to a question is a measurement, not a window. "
            "Ask what it's reliable across, and what the evidence is that it measures what you hoped. "
            "<bookmark mark='e'/> And where you can, measure the behaviour too. That gives you a second method, "
            "and you know from chapter seven why you want one."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(end[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(end[1]))
        self.clear_scene()
