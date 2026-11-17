from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403
from videos.psychology.psych35.s07_impressions import face


class Introspection(VoiceoverScene):
    def construct(self):
        self.card()
        self.stockings()
        self.blindness()
        self.turned()

    def card(self):
        card = chapter_card(11, r"Knowing ourselves", r"Do we read our own minds the way we read others'?",
                            lit={1967: r"Bem", 1977: r"Nisbett \& Wilson", 2005: r"Johansson et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter eleven. Knowing ourselves."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stockings(self):
        head = heading(r"Four identical pairs")
        pairs = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.0, height=2.0, stroke_color=GREY_A,
                                          fill_color="#2A2F38", fill_opacity=1) for _ in range(4)])
        pairs.arrange(RIGHT, buff=0.35).move_to([-3.6, 0.7, 0])
        pos = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(p_, DOWN, buff=0.15)
                       for t, p_ in zip((r"left", "", "", r"right"), pairs)])
        rows = rows_of([
            (r"Nisbett and Wilson, \ 1977: \ shoppers chose the best of four pairs of stockings; \ the pairs were "
             r"identical", WHITE),
            (r"the rightmost pair was chosen far more often than the leftmost", PERSON),
            (r"asked why, \ people cited the knit, \ the sheerness, \ the feel; \ nobody mentioned the position", AUTH),
            (r"Nisbett and Wilson's conclusion: \ we often explain our own behaviour with plausible theories, \ not "
             r"by looking inward", YOU),
        ], 6.0, 21, 0.38).move_to([3.3, -0.3, 0])
        tag = historical_tag(r"Nisbett \& Wilson (1977)")
        with self.voiceover(
            "The part ends by turning the question round. We read other minds by inference. Do we read our own "
            "any differently? <bookmark mark='a'/> In 1977 Richard Nisbett and Timothy Wilson had shoppers choose "
            "the best of four pairs of stockings. The pairs were identical. <bookmark mark='b'/> The rightmost "
            "pair was chosen far more often than the leftmost. <bookmark mark='c'/> Asked why, people cited the "
            "knit, the sheerness, the feel. Nobody mentioned the position. <bookmark mark='d'/> Nisbett and "
            "Wilson concluded that we often explain our own behaviour with plausible theories, not by looking "
            "inward."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pairs), FadeIn(pos))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(pairs[3].animate.set_stroke(PERSON, width=5), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def blindness(self):
        head = heading(r"Choice blindness")
        f1 = RoundedRectangle(corner_radius=0.1, width=1.5, height=2.0, stroke_color=PERSON, fill_color="#2A2F38",
                              fill_opacity=1).move_to([-4.6, 0.8, 0])
        f2 = RoundedRectangle(corner_radius=0.1, width=1.5, height=2.0, stroke_color=CROWD, fill_color="#2A2F38",
                              fill_opacity=1).move_to([-2.6, 0.8, 0])
        g1 = face(PERSON, 0.3).scale(0.8).move_to(f1)
        g2 = face(CROWD, -0.1).scale(0.8).move_to(f2)
        g2[0].stretch(0.85, 0)
        f1.add(g1)
        f2.add(g2)
        l1 = label(r"chosen", font_size=16, color=PERSON).next_to(f1, DOWN, buff=0.15)
        l2 = label(r"handed back", font_size=16, color=CROWD).next_to(f2, DOWN, buff=0.15)
        swap = CurvedArrow(f1.get_top() + UP * 0.1, f2.get_top() + UP * 0.1, angle=-1.2, color=AUTH)
        rows = rows_of([
            (r"Johansson, \ Hall, \ Sikstr\"om and Olsson, \ 2005: \ people chose the more attractive of two faces "
             r"on cards, \ 15 times; \ on some trials the experimenter secretly handed back the other card", WHITE),
            (r"fewer than one switch in ten was noticed at once", AUTH),
            (r"asked why they had chosen it, \ people gave reasons for the face they had turned down", CROWD),
            (r"a reason can be built after the choice, \ for whatever choice we are shown", YOU),
        ], 6.0, 21, 0.38).move_to([3.3, -0.3, 0])
        tag = published_tag(r"Johansson et al.\ (2005)")
        with self.voiceover(
            "A sharper version came in 2005. <bookmark mark='a'/> Johansson, Hall and colleagues had "
            "people choose the more attractive of two faces on cards, fifteen times. On some trials the "
            "experimenter, by sleight of hand, gave back the card they had not chosen. <bookmark mark='b'/> Fewer "
            "than one switch in ten was noticed at once. <bookmark mark='c'/> Asked why they had chosen it, people "
            "gave reasons for the face they had turned down. <bookmark mark='d'/> A reason can be built after the "
            "choice, for whatever choice we're shown."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(f1), FadeIn(f2), FadeIn(l1))
            vo.wait_until("a")
            self.play(Create(swap), FadeIn(l2), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def turned(self):
        head = heading(r"The observer inside")
        left = VGroup(word_chip(r"reading others", color=CROWD, font_size=24, width=5.2),
                      wrapped_label(r"watch what they do and the situation; \ infer the attitude, \ the goal, \ the "
                                    r"belief that best explains it", 5.2, 20, WHITE)).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"reading ourselves", color=PERSON, font_size=24, width=5.2),
                       wrapped_label(r"often the same inference, \ with more data: \ Bem's self-perception, \ the "
                                     r"stockings, \ the swapped faces", 5.2, 20, WHITE)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.7, 0])
        foot = rows_of([
            (r"not always: \ people do know their own feelings and plans in ways no observer can, \ and Part 3 "
             r"showed when self-reports are good measurements", GOOD),
            (r"but for the causes of our own behaviour, \ we are often in the observer's seat", YOU),
        ], 11.6, 21, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Put it together with chapter three. <bookmark mark='a'/> To read others, we watch what they do and "
            "the situation, and infer the attitude, goal or belief that best explains it. <bookmark mark='b'/> To "
            "read ourselves we often run the same inference, with more data. That was Bem's self-perception, and "
            "it's the stockings and the swapped faces. <bookmark mark='c'/> Not always. People know their own "
            "feelings and plans in ways no observer can, and Part 3 showed when self-reports are good measurements. "
            "<bookmark mark='d'/> But for the causes of our own behaviour, we're often in the observer's seat."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
