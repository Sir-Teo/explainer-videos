from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.trials()
        self.answers()

    def card(self):
        card = chapter_card(5, r"On you: \ a threshold of your own", r"Where does your guessing begin?", lit=(), part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter five. On you: a threshold of your own."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def trials(self):
        d = load("onyou")
        stage = demo_stage(13.0, 6.4, r"On you: \ eight trials", center=[0, -0.2, 0])
        c = stage.box.get_center()
        note_ = label(r"For each trial, \ say or write: \ left or right?", font_size=30, color=P.ACCENT)
        note_.move_to(stage.box.get_top() + DOWN * 0.75)
        with self.voiceover(
            "Your turn. Eight trials. On each, two grey patches: say, or write down, which is brighter, "
            "left or right. Guess when you're not sure. That's the rule of a forced choice: never pass. "
            "Number one."
        ):
            self.play(FadeIn(stage), FadeIn(note_))
        for i, (inc, side) in enumerate(zip(d["increments"], d["brighter"])):
            left, right = (100.0, 100.0 + inc) if side == 1 else (100.0 + inc, 100.0)
            pair = patch_pair(left, right, size=2.2, gap=0.6).move_to(c + DOWN * 0.15)
            num = label(rf"{i + 1}", font_size=40, color=GREY_A).move_to(c + np.array([-5.6, 2.0, 0]))
            ring = countdown_ring(0.35).move_to(c + np.array([5.6, 2.0, 0]))
            self.play(FadeIn(pair), FadeIn(num), run_time=0.4)
            self.add(ring)
            self.play(ring.t.animate.set_value(0.0), run_time=3.2, rate_func=linear)
            self.remove(ring)
            self.play(FadeOut(pair), FadeOut(num), run_time=0.3)
        self.clear_scene()

    def answers(self):
        d = load("onyou")
        head = heading(r"The answers")
        order = np.argsort(d["increments"])[::-1]
        rows = VGroup()
        for r, i in enumerate(range(8)):
            inc, side, p = d["increments"][i], d["brighter"][i], d["p_clean"][i]
            y = 2.2 - 0.62 * r
            rows.add(VGroup(
                label(rf"{i + 1}", font_size=30, color=GREY_A).move_to([-5.9, y, 0]),
                label(r"right" if side else r"left", font_size=30, color=YOU).move_to([-4.6, y, 0]),
                label(rf"{inc:g}\%", font_size=30, color=WHITE).move_to([-2.9, y, 0]),
                Rectangle(width=4.0 * p, height=0.36, stroke_width=0, fill_color=MODEL, fill_opacity=0.85).move_to(
                    [-1.6, y, 0], aligned_edge=LEFT),
                label(rf"{100 * p:.0f}\%", font_size=28, color=MODEL).move_to([3.0, y, 0]),
            ))
        hdr = VGroup(label(r"trial", font_size=25, color=GREY_A).move_to([-5.9, 2.85, 0]),
                     label(r"brighter", font_size=25, color=YOU).move_to([-4.6, 2.85, 0]),
                     label(r"difference", font_size=25, color=GREY_A).move_to([-2.9, 2.85, 0]),
                     label(r"how often an observer with a 7.6\% threshold is right", font_size=25, color=MODEL).move_to([1.1, 2.85, 0]))
        half = VGroup(DashedLine([-1.6 + 2.0, -2.6, 0], [-1.6 + 2.0, 2.6, 0], color=GREY_C, stroke_width=2),
                      label(r"chance", font_size=24, color=GREY_A).move_to([-1.6 + 2.0, -2.85, 0]))
        rows_ = rows_of([
            (r"count your right answers at 12\% and above, \ and at 3\% and below", WHITE),
            (r"if you were sure of the first and unsure of the second, \ your threshold is somewhere between: \ you have "
             r"just walked up a psychometric function", THRESH),
        ], 3.2, 26, 0.3).move_to([5.25, -0.2, 0])
        keep_in_frame(rows_)
        tag = note(r"the course site measures it properly: \ a staircase on your own screen, \ and a fitted curve").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here are the answers, trial by trial, in the second column. Check them against your own. "
            "<bookmark mark='a'/> Next to each, the chance that an observer "
            f"with a just noticeable difference of {d['jnd']:.1f} percent gets it right. At twenty-four "
            "percent, nearly always. At one and a half percent, little better than a coin. "
            "<bookmark mark='b'/> Count your right answers on the big differences, twelve percent and "
            "above, and on the small ones, three percent and below. If you were sure of the first and "
            "unsure of the second, your threshold is somewhere between. You've just walked up a "
            "psychometric function. <bookmark mark='c'/> Eight trials can't say more than that. The "
            "course site has the real thing: a staircase run on your own screen, and your own curve, "
            "fitted the way the next chapter fits one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(half), *[FadeIn(VGroup(*r[:3])) for r in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[3], LEFT), FadeIn(r[4])) for r in rows], lag_ratio=0.3),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows_))
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.clear_scene()
