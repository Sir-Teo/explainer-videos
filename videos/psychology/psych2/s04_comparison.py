from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Comparison(VoiceoverScene):
    def construct(self):
        self.card()
        self.claim()
        self.one_group()
        self.control()

    def card(self):
        card = chapter_card(3, r"Compared with what?", r"A game is said to sharpen your reactions. \ How would you "
                            r"find out?", lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter three. Compared with what?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def claim(self):
        ad = VGroup(label(r"``Play ten minutes a day.", font_size=40, color=WHITE),
                    label(r"React faster in a week.''", font_size=40, color=WHITE)).arrange(DOWN, buff=0.15)
        box = RoundedRectangle(width=ad.width + 1.2, height=ad.height + 0.9, corner_radius=0.2, stroke_color=TREAT,
                               stroke_width=3, fill_color=CARD_FILL, fill_opacity=1)
        ad.move_to(box)
        claim = VGroup(box, ad).to_edge(UP, buff=0.5)
        tag = note(r"an invented advertisement").next_to(claim, RIGHT, buff=0.3)
        rows = VGroup()
        for name, text, color in (
            (r"independent variable", r"what the experimenter changes: \ the game, or no game", TREAT),
            (r"dependent variable", r"what is measured afterwards: \ reaction time", P.RESP),
            (r"operational definition", r"``reaction time'' = the mean of 20 simple reactions, in ms, on Battery "
                                        r"task 1", P.ACCENT),
        ):
            rows.add(VGroup(label(name, font_size=32, color=color), wrapped_label(text, 12.0, 30, WHITE))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(claim, DOWN, buff=0.6)
        with self.voiceover(
            "Here's a claim of a kind you meet every week. A game: play ten minutes a day, and react faster in a "
            "week. How would you find out whether it's true? <bookmark mark='a'/> Start by saying what the claim "
            "is about. Something is changed: you play the game, or you don't. That's the independent variable. "
            "<bookmark mark='b'/> And something is supposed to change as a result: how fast you react. The "
            "dependent variable. <bookmark mark='c'/> But react faster is not yet a measurement. So we say "
            "exactly what we'll do to get the number: twenty simple reactions on the task from Part 1, averaged, "
            "in milliseconds. That's an operational definition. It turns a phrase into a procedure anyone can "
            "repeat. Whether the procedure measures what the phrase meant is a separate question, and it's the "
            "whole of the next part."
        ) as vo:
            self.play(FadeIn(claim, shift=UP * 0.2), FadeIn(tag))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def one_group(self):
        d = load("one_group")
        al = d["alone"]
        head = heading(rf"Study 1: \ {d['n']} people, tested before and after a week of the game")
        pre, post = np.asarray(d["pre_sample"]), np.asarray(d["post_sample"])
        lo, hi = 160.0, 290.0
        A = axes([0, 3], [lo, hi], x_length=4.6, y_length=4.4, ylabel=r"mean reaction time (ms)",
                 yticks=[180, 220, 260], center=[-3.6, -0.55, 0])
        ax = A.ax
        xl = VGroup(label(r"before", font_size=26).next_to(ax.c2p(1, lo), DOWN, buff=0.2),
                    label(r"after", font_size=26).next_to(ax.c2p(2, lo), DOWN, buff=0.2))
        lines = VGroup(*[Line(ax.c2p(1, a), ax.c2p(2, b), color=P.POOL, stroke_width=1.2).set_opacity(0.45)
                         for a, b in zip(pre, post)])
        m0, m1 = Dot(ax.c2p(1, d["pre_mean"]), radius=0.12, color=WHITE), Dot(ax.c2p(2, d["post_mean"]), radius=0.12,
                                                                               color=WHITE)
        mline = Line(m0.get_center(), m1.get_center(), color=WHITE, stroke_width=5)
        res = VGroup(
            MathTex(rf"{d['pre_mean']:.0f}\ \text{{ms}}", r"\ \longrightarrow\ ", rf"{d['post_mean']:.0f}\ \text{{ms}}",
                    font_size=52),
            label(rf"${al['effect']:.1f}$ ms, \ 95\% interval ${al['lo']:.1f}$ to ${al['hi']:.1f}$", font_size=34,
                  color=TREAT),
            label(r"``The game works.''", font_size=40, color=TREAT),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.3, 0.6, 0])
        truth = VGroup(label(r"In the Pool we wrote the truth:", font_size=30, color=P.POOL),
                       label(r"the game does nothing.", font_size=40, color=TRUTH)).arrange(DOWN, buff=0.12,
                                                                                            aligned_edge=LEFT)
        truth.next_to(res, DOWN, buff=0.55).align_to(res, LEFT)
        tag = simulated_tag()
        with self.voiceover(
            f"So run the obvious study. Take {d['n']} people from the Pool. Measure their reaction time. Have "
            "them play the game for a week. Measure again. <bookmark mark='a'/> Each line is one person, and "
            f"most of them slope down. On average, {d['pre_mean']:.0f} milliseconds before, and "
            f"{d['post_mean']:.0f} after. <bookmark mark='b'/> An improvement of {abs(al['effect']):.1f} "
            "milliseconds, with an interval that's nowhere near zero. <bookmark mark='c'/> The game works. "
            "<bookmark mark='d'/> Except that this is the Pool, where we wrote the truth, and what we wrote is "
            "that the game does nothing at all. Every one of those people would have got faster without it. "
            "Why? Because the second time you take a test, you've taken it before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.03), run_time=3.0)
            self.play(FadeIn(m0), FadeIn(m1), Create(mline), FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(res[2], scale=1.1))
            vo.wait_until("d")
            self.play(res[2].animate.set_color(GREY_C), FadeIn(truth, shift=UP * 0.15))
        self.clear_scene()

    def control(self):
        d = load("one_group")
        m, wc = d["means"], d["with_control"]
        head = heading(r"Study 2: \ the same test, with a group that never saw the game")
        lo, hi = 198.0, 230.0
        A = axes([0, 3], [lo, hi], x_length=5.0, y_length=4.2, ylabel=r"mean reaction time (ms)",
                 yticks=[200, 210, 220, 230], center=[-3.5, -0.6, 0])
        ax = A.ax
        xl = VGroup(label(r"before", font_size=26).next_to(ax.c2p(1, lo), DOWN, buff=0.2),
                    label(r"after", font_size=26).next_to(ax.c2p(2, lo), DOWN, buff=0.2))

        def group(key, color):
            a, b = ax.c2p(1, m[key]["pre"]), ax.c2p(2, m[key]["post"])
            return VGroup(Line(a, b, color=color, stroke_width=6), Dot(a, radius=0.11, color=color),
                          Dot(b, radius=0.11, color=color))

        treated, ctrl = group("treated", TREAT), group("control", CTRL)
        leg = legend([(TREAT, r"played the game"), (CTRL, r"did not")], font_size=24)
        leg.next_to(ax.c2p(3, hi), DL, buff=0.1)
        gain = lambda k: m[k]["post"] - m[k]["pre"]  # noqa: E731
        rows = VGroup(
            label(rf"played: \ ${gain('treated'):+.1f}$ ms", font_size=36, color=TREAT),
            label(rf"did not: \ ${gain('control'):+.1f}$ ms", font_size=36, color=CTRL),
            label(rf"difference: \ ${wc['effect']:+.1f}$ ms, \ interval ${wc['lo']:.1f}$ to ${wc['hi']:+.1f}$",
                  font_size=36, color=TRUTH),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, 0.9, 0])
        idea = VGroup(
            label(r"The control group answers the question", font_size=30, color=GREY_A),
            label(r"``what would have happened anyway?''", font_size=38, color=P.ACCENT),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
        tag = simulated_tag()
        with self.voiceover(
            "The cure is to ask: compared with what? <bookmark mark='a'/> Run it again, and this time split the "
            "people in two. Half play the game. <bookmark mark='b'/> The other half don't, and otherwise go "
            "through exactly the same week: the same test before, the same test after. <bookmark mark='c'/> The "
            f"players improve by {abs(gain('treated')):.1f} milliseconds. The others improve by "
            f"{abs(gain('control')):.1f}. <bookmark mark='d'/> The difference between the two groups is the "
            f"game's effect, and it comes out at {wc['effect']:.1f}, give or take three: nothing, which is the "
            "truth. <bookmark mark='e'/> That second group is called a control group, and what it gives you is "
            "the answer to a question you can never ask of one person: what would have happened anyway? An "
            "experiment is a comparison, and a single group compared with its own past is the most common way "
            "to get the comparison wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(treated[1]), Create(treated[0]), FadeIn(treated[2]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(ctrl[1]), Create(ctrl[0]), FadeIn(ctrl[2]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0], shift=LEFT * 0.15))
            self.play(FadeIn(rows[1], shift=LEFT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=LEFT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(idea, shift=UP * 0.15))
        self.clear_scene()
