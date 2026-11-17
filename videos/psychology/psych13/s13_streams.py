from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Streams(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.df()

    def card(self):
        card = chapter_card(12, r"Two streams", r"Is seeing one thing, \ or two?",
                            lit={1982: r"Ungerleider and Mishkin", 1992: r"Goodale and Milner"}, part=PART,
                            scale=("brain", "mind"), marr=("what",))
        with self.voiceover("Chapter twelve. Two streams."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two(self):
        head = heading(r"Beyond the first stage")
        brain = head_outline(height=4.2).move_to([-3.6, -0.4, 0])
        # the head faces right: V1 at the back (left), both streams running forward
        v1 = Dot(brain.get_center() + np.array([-1.35, -0.35, 0]), radius=0.16, color=CELL)
        v1l = label(r"V1", font_size=22, color=CELL).next_to(v1, DOWN, buff=0.08)
        top = CurvedArrow(v1.get_center(), brain.get_center() + np.array([0.4, 1.15, 0]), angle=-PI / 4, color=SURROUND)
        bot = CurvedArrow(v1.get_center(), brain.get_center() + np.array([0.7, -0.85, 0]), angle=PI / 6, color=CENTRE)
        tl = label(r"dorsal: \ where, \ or how", font_size=22, color=SURROUND).next_to(top.get_end(), UP, buff=0.1)
        bl = label(r"ventral: \ what", font_size=22, color=CENTRE).next_to(bot.get_end(), DOWN, buff=0.1)
        rows = rows_of([
            (r"from V1, \ two broad routes through the cortex", WHITE),
            (r"Ungerleider and Mishkin, \ 1982, \ from lesions in monkeys: \ a lower stream for what an object is, \ "
             r"an upper one for where it is", CENTRE),
            (r"Goodale and Milner, \ 1992: \ the upper stream is less about where than about how: \ vision for guiding "
             r"action", SURROUND),
        ], 6.4, 27, 0.36).move_to([3.0, -0.2, 0])
        keep_in_frame(rows)
        with self.voiceover(
            "Everything so far happens in the first few stages of vision. <bookmark mark='a'/> From the primary "
            "visual cortex, V1, signals travel along two broad routes. <bookmark mark='b'/> In 1982 Leslie "
            "Ungerleider and Mortimer Mishkin, working from lesions in monkeys, proposed that a lower route, "
            "through the temporal lobe, works out what an object is, and an upper route, through the parietal lobe, "
            "works out where it is. <bookmark mark='c'/> Ten years later Melvyn Goodale and David Milner proposed a "
            "twist. The upper stream isn't so much about where things are as about how to act on them: vision for "
            "reaching and grasping. Their evidence was largely one woman."
        ) as vo:
            self.play(FadeIn(head), FadeIn(brain), FadeIn(v1), FadeIn(v1l))
            vo.wait_until("a")
            self.play(Create(top), Create(bot), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tl), FadeIn(rows[2]))
        self.clear_scene()

    def _polar(self, angles, color, center, title):
        circ = Circle(radius=1.5, color=GREY_D, stroke_width=2).move_to(center)
        ref = Line(center + LEFT * 1.5, center + RIGHT * 1.5, color=GREY_D, stroke_width=1.5)
        lines = VGroup(*[Line(center, center + 1.4 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0]),
                              color=color, stroke_width=2.5, stroke_opacity=0.8) for a in angles])
        t = label(title, font_size=24, color=color).next_to(circ, UP, buff=0.2)
        return VGroup(circ, ref, lines, t)

    def df(self):
        d = load("streams")
        head = heading(r"D.F.: \ posting without perceiving")
        # errors drawn relative to the slot: the slot always horizontal
        err_m = (np.asarray(d["matched"]) - np.asarray(d["slot"]) + 90) % 180 - 90
        err_p = (np.asarray(d["posted"]) - np.asarray(d["slot"]) + 90) % 180 - 90
        pm = self._polar(err_m, CENTRE, np.array([-4.4, 0.3, 0]), r"matching the slot's angle")
        pp = self._polar(err_p, SURROUND, np.array([-0.4, 0.3, 0]), r"posting a card into it")
        rows = rows_of([
            (r"1988: \ carbon monoxide poisoning damaged her lower stream; \ she could no longer say what shape or "
             r"angle she saw", WHITE),
            (r"asked to turn a card to match a slot's angle: \ near chance", CENTRE),
            (r"asked to post the card through the slot: \ her hand turned correctly as it moved", SURROUND),
            (r"vision guiding action without vision for knowing; \ how separate the streams are is now argued, \ and "
             r"they talk to each other", GREY_A),
            (r"seeing without knowing returns in Part 27, \ with blindsight", YOU),
        ], 4.6, 24, 0.28).move_to([4.5, -0.2, 0])
        keep_in_frame(rows)
        cap = label(r"each line: \ one trial's error from the slot (horizontal)", font_size=22, color=GREY_B)
        cap.next_to(VGroup(pm, pp), DOWN, buff=0.3)
        tags = VGroup(historical_tag(archive.MILNER_1991.cite), simulated_tag(r"schematic: \ simulated trials with "
                                                                               r"the published pattern"))
        with self.voiceover(
            "She's known in the literature as D.F. <bookmark mark='a'/> In 1988 carbon monoxide poisoning damaged the "
            "lower, ventral stream of her brain. She could still see colours and textures, but could no longer tell "
            "shapes apart, or say which way a line was tilted. <bookmark mark='b'/> In a now famous test, she was "
            "shown a slot in a disc, at different angles, and asked to turn a card in her hand to match it. Her "
            "settings were close to random: each line here is one trial's error. <bookmark mark='c'/> Then she was "
            "asked to post the card through the slot, as you'd post a letter. Her hand turned the card to the right "
            "angle as it moved. <bookmark mark='d'/> Vision guided her action, though it gave her no knowledge of "
            "the angle. Today the streams are thought to be less separate than the first accounts suggested, and to "
            "talk to each other constantly. <bookmark mark='e'/> But seeing without knowing is real, and it comes "
            "back in Part 27, with blindsight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pm), FadeIn(rows[1]), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(pp), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
