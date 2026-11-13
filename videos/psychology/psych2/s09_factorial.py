from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403

QUICK, SLOW = "#7EC8F5", "#F2A65A"


class Factorial(VoiceoverScene):
    def construct(self):
        self.card()
        self.patterns()
        self.scale()

    def card(self):
        card = chapter_card(8, r"It depends", r"Does the game help everyone equally, and how would you tell?",
                            lit=(), part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter eight. It depends."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mini(self, ys, title, verdict, color) -> VGroup:
        """A small 2 by 2 plot: two lines over 'no game' and 'game'."""
        A = axes([0.5, 2.5], [0, 4], x_length=3.0, y_length=2.4, center=ORIGIN)
        ax = A.ax
        g = VGroup(A)
        for (a, b), c in zip(ys, (QUICK, SLOW)):
            g.add(Line(ax.c2p(1, a), ax.c2p(2, b), color=c, stroke_width=5), Dot(ax.c2p(1, a), radius=0.07, color=c),
                  Dot(ax.c2p(2, b), radius=0.07, color=c))
        xl = VGroup(label(r"no game", font_size=20, color=GREY_A).next_to(ax.c2p(1, 0), DOWN, buff=0.12),
                    label(r"game", font_size=20, color=GREY_A).next_to(ax.c2p(2, 0), DOWN, buff=0.12))
        t = label(title, font_size=28, color=WHITE).next_to(A, UP, buff=0.25)
        v = wrapped_label(verdict, 3.6, 24, color).next_to(xl, DOWN, buff=0.25)
        g.add(xl, t, v)
        return g

    def patterns(self):
        head = heading(r"Two factors at once: \ who you are, and whether you played")
        a = self.mini(((1.4, 0.9), (3.1, 2.6)), r"parallel", r"the game takes off the same amount for everyone: "
                      r"\ two effects that add", TRUTH)
        b = self.mini(((1.4, 1.1), (3.1, 2.0)), r"fanning", r"it helps the slow more: \ an interaction", P.ACCENT)
        c = self.mini(((1.4, 2.4), (3.1, 2.0)), r"crossing", r"it helps one group and hurts the other: \ the "
                      r"average effect hides both", BIAS)
        g = VGroup(a, b, c).arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to([0, -0.35, 0])
        leg = legend([(QUICK, r"quick people"), (SLOW, r"slow people")], font_size=24)
        leg.arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.3)
        sch = schematic_tag(UR)
        with self.voiceover(
            "So far the question has been whether the game works. A better question is: for whom? To ask it, "
            "cross two factors in one experiment. Whether you played, and whether you're one of the quick people "
            "or one of the slow. Four cells, and three kinds of answer. <bookmark mark='a'/> The lines can be "
            "parallel. The game takes the same amount off everybody. Two effects that simply add. "
            "<bookmark mark='b'/> They can fan. The game helps slow people more than quick ones. That's called "
            "an interaction: the effect of one factor depends on the level of the other. <bookmark mark='c'/> Or "
            "they can cross. It helps one group and hurts the other, and the average effect, which might be "
            "zero, describes nobody. <bookmark mark='d'/> You met this picture in Part 1, where parallel lines "
            "meant two factors acting on different stages of a reaction. It depends is not a failure to find a "
            "law. Very often it is the law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(sch))
            for mark, m in zip("abc", (a, b, c)):
                vo.wait_until(mark)
                self.play(FadeIn(m, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Indicate(a[-2], color=TRUTH, scale_factor=1.15))
        self.clear_scene()

    def scale(self):
        d = load("factorial")
        ms, logs = np.asarray(d["ms"]), np.asarray(d["log"])
        head = heading(r"A game that takes a tenth off every reaction time")

        def plot(vals, center, ylabel, yr, yticks, yfmt=None):
            A = axes([0.5, 2.5], yr, x_length=3.6, y_length=3.4, ylabel=ylabel, yticks=yticks, yfmt=yfmt,
                     center=center)
            ax = A.ax
            g = VGroup(A)
            for row, c in zip(vals, (QUICK, SLOW)):
                g.add(Line(ax.c2p(1, row[0]), ax.c2p(2, row[1]), color=c, stroke_width=5),
                      Dot(ax.c2p(1, row[0]), radius=0.08, color=c), Dot(ax.c2p(2, row[1]), radius=0.08, color=c))
            g.add(label(r"no game", font_size=22, color=GREY_A).next_to(ax.c2p(1, yr[0]), DOWN, buff=0.15),
                  label(r"game", font_size=22, color=GREY_A).next_to(ax.c2p(2, yr[0]), DOWN, buff=0.15))
            return g

        left = plot(ms, [-4.3, -0.35, 0], r"milliseconds", [170, 245], [180, 200, 220, 240])
        right = plot(logs, [1.0, -0.35, 0], r"logarithm of milliseconds", [5.15, 5.5], [5.2, 5.3, 5.4, 5.5],
                     yfmt=lambda v: rf"{v:.1f}")
        gains = VGroup(label(rf"quick: \ ${d['gain_ms'][0]:.0f}$ ms", font_size=26, color=QUICK),
                       label(rf"slow: \ ${d['gain_ms'][1]:.0f}$ ms", font_size=26, color=SLOW),
                       label(rf"interaction: \ ${d['interaction_ms']:.1f}$ ms", font_size=26, color=P.ACCENT))
        gains.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(left, DOWN, buff=0.25)
        pct = VGroup(label(rf"quick: \ ${d['percent'][0]:.0f}\%$", font_size=26, color=QUICK),
                     label(rf"slow: \ ${d['percent'][1]:.0f}\%$", font_size=26, color=SLOW),
                     label(r"interaction: \ none", font_size=26, color=TRUTH))
        pct.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(right, DOWN, buff=0.25)
        moral = VGroup(
            wrapped_label(r"The same data. \ Whether there is an interaction depends on the scale.", 3.9, 28, WHITE),
            wrapped_label(r"Lines that cross survive any scale. \ Lines that only fan may not.", 3.9, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.05, 0.3, 0])
        tag = simulated_tag(rf"simulated: the Pool, {fmt_int(d['n'])} people")
        with self.voiceover(
            "One warning about interactions, and it's computed, so you can check it. Suppose the game takes a "
            "tenth off anybody's reaction time. That's a single, simple effect, the same for everyone. "
            f"<bookmark mark='a'/> Plot the four cell means in milliseconds. The quick people gain "
            f"{abs(d['gain_ms'][0]):.0f} milliseconds, the slow gain {abs(d['gain_ms'][1]):.0f}, because a tenth of "
            "a bigger number is bigger. The lines fan, and a statistical test finds an interaction. You could "
            "write a paper: the game helps slow people more. <bookmark mark='b'/> Now plot the same data on a "
            "logarithmic scale, where equal ratios are equal distances. Both groups drop by ten per cent. "
            "Parallel. No interaction. <bookmark mark='c'/> Nothing about the people changed between those two "
            "pictures. So when an interaction is the kind where the lines only fan, ask what scale it was "
            "measured on, and whether the claim would survive another one. Lines that cross do survive. This "
            "matters all through the series, wherever one group starts higher than another."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.15))
            self.play(FadeIn(gains, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.15))
            self.play(FadeIn(pct, lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(moral, shift=LEFT * 0.15))
        self.clear_scene()
