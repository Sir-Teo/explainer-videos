from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Honest(VoiceoverScene):
    def construct(self):
        self.card()
        self.stopping()
        self.harking()

    def card(self):
        card = chapter_card(6, r"Honest people, wrong results", r"Why is good faith not enough?",
                            lit={1998: r"Kerr names HARKing"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter six. Honest people, wrong results."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stopping(self):
        d = load("stopping")
        head = heading(r"``Let's run a few more and look again''")
        n, typ, lucky = np.asarray(d["path_n"]), np.asarray(d["path_typical"]), np.asarray(d["path_lucky"])
        A = axes([0, 105], [0, 1.0], x_length=6.6, y_length=3.7, xticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"people in each group so far", ylabel=r"p-value",
                 center=[-3.1, -0.45, 0])
        ax = A.ax
        thr = DashedLine(ax.c2p(0, 0.05), ax.c2p(105, 0.05), color=SIG, stroke_width=3)
        thr_l = label(r".05", font_size=22, color=SIG).next_to(ax.c2p(105, 0.05), RIGHT, buff=0.08)
        p1 = curve(ax, n, typ, NULLC, stroke_width=3)
        first = int(np.argmax(lucky < 0.05))
        p2 = curve(ax, n[: first + 1], lucky[: first + 1], BAD, stroke_width=4)
        rest = DashedVMobject(curve(ax, n[first:], lucky[first:], BAD, stroke_width=2), num_dashes=40)
        stop = Dot(ax.c2p(n[first], lucky[first]), radius=0.11, color=BAD)
        stop_l = label(rf"stopped at {int(n[first])} a group: \ $p = {p_text(lucky[first])}$", font_size=26, color=BAD)
        stop_l.move_to(ax.c2p(66, 0.9))
        habit = VGroup(
            label(r"run 20 people a group", font_size=28, color=WHITE),
            label(r"$p$ is close, but above .05", font_size=28, color=NULLC),
            label(r"run 10 more, and look again", font_size=28, color=BAD),
        ).arrange(DOWN, buff=0.55).move_to([4.6, 0.3, 0])
        arrows = VGroup(*[Arrow(habit[i].get_bottom(), habit[i + 1].get_top(), buff=0.08, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(2)])
        loop = CurvedArrow(habit[2].get_right() + RIGHT * 0.1, habit[1].get_right() + RIGHT * 0.1, angle=PI / 1.6,
                           color=BAD, stroke_width=3)
        looks, rates = d["looks"], d["rates"]
        unit = 9.5
        bars = VGroup()
        for i, (k, r) in enumerate(zip(looks, rates)):
            y = 1.9 - 0.58 * i
            bar = Rectangle(width=unit * r, height=0.36, stroke_width=0, fill_color=(NULLC if k == 1 else BAD),
                            fill_opacity=0.9).move_to([3.0 + unit * r / 2, y, 0])
            nm = label(rf"{k} look" + ("" if k == 1 else "s"), font_size=24, color=WHITE).next_to([3.0, y, 0], LEFT,
                                                                                               buff=0.15)
            val = label(pct(r), font_size=24, color=(NULLC if k == 1 else BAD)).next_to(bar, RIGHT, buff=0.12)
            bars.add(VGroup(nm, bar, val))
        cap = wrapped_label(r"studies of nothing that reach $p < .05$ at some look", 4.6, 24, GREY_A)
        cap.next_to(bars, DOWN, buff=0.3).align_to(bars, LEFT)
        tag = note(r"simulated: a treatment with no effect, tested after every 10 people a group").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The forking paths needed a little ingenuity. This one needs none. You run twenty people a group. "
            "The result is nearly significant. So you run ten more and look again. Everyone has done it, and it "
            "feels like diligence. <bookmark mark='a'/> Here's a study of nothing, tested after every ten people. "
            "The p-value wanders, as it must, since there's nothing to find. <bookmark mark='b'/> Here's "
            "another. It wanders too, and at one point it dips under the line. If you stop there, you have a "
            "finding. If you'd kept going, it would have wandered back out. <bookmark mark='c'/> A p-value is "
            "only honest if you decided in advance when to look. Look once, and you're wrong five per cent of "
            f"the time. <bookmark mark='d'/> Look ten times, stopping at the first success, and it's "
            f"{100 * d['rate_10']:.0f} per cent. Keep looking for long enough and you will always get there. The "
            "data haven't changed. The rule for stopping was allowed to depend on the result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(thr), FadeIn(thr_l), FadeIn(tag))
            self.play(LaggedStart(FadeIn(habit[0]), GrowArrow(arrows[0]), FadeIn(habit[1]), GrowArrow(arrows[1]),
                                  FadeIn(habit[2]), Create(loop), lag_ratio=0.7), run_time=8.0)
            vo.wait_until("a")
            self.play(Create(p1), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(p2), run_time=3.0)
            self.play(FadeIn(stop, scale=1.5), FadeIn(stop_l))
            self.play(Create(rest), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(habit, arrows, loop)), run_time=0.6)
            self.play(FadeIn(bars[0]), FadeIn(cap))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[1:]], lag_ratio=0.4), run_time=4.0)
        self.clear_scene()

    def harking(self):
        head = heading(r"The target painted round the arrow")
        wall = panel(5.2, 4.2, center=[-3.9, -0.3, 0], color=GREY_D)
        rng_ = np.random.default_rng(12)
        pts = rng_.uniform([-6.1, -2.0], [-1.7, 1.4], (14, 2))
        cluster = np.array([[-3.1, 0.55], [-2.85, 0.35], [-3.3, 0.3], [-2.95, 0.75]])
        holes = VGroup(*[Dot([x, y, 0], radius=0.06, color=GREY_A) for x, y in np.vstack([pts, cluster])])
        c = cluster.mean(axis=0)
        target = VGroup(*[Circle(radius=r, color=BAD, stroke_width=4).move_to([c[0], c[1], 0]) for r in (0.25, 0.55, 0.85)])
        steps = VGroup(
            VGroup(label(r"HARKing", font_size=34, color=BAD),
                   wrapped_label(r"Hypothesizing After the Results are Known: \ the paper says the pattern was "
                                 r"predicted.", 6.2, 27, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"The garden of forking paths", font_size=34, color=SIG),
                   wrapped_label(r"Only one analysis was run. \ But it was chosen after seeing the data, and other "
                                 r"data would have led to another.", 6.2, 27, WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.1),
            VGroup(label(r"Why honesty is not enough", font_size=34, color=P.ACCENT),
                   wrapped_label(r"None of this feels like cheating from the inside. \ The remedy has to be in the "
                                 r"procedure, as the blind was.", 6.2, 27, WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([3.3, -0.2, 0])
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "There's an old joke about a Texan who fires his rifle at the side of a barn, <bookmark mark='a'/> "
            "walks over, finds where the holes are thickest, <bookmark mark='b'/> and paints a target round them. "
            "<bookmark mark='c'/> In research this has a name: hypothesizing after the results are known. You "
            "collect data, something unexpected turns up, and the paper is written as though that had been the "
            "prediction all along. The p-value in that paper is the sharpshooter's score. "
            "<bookmark mark='d'/> And here's the subtle part, pointed out by the statisticians Andrew Gelman and "
            "Eric Loken. You don't have to try sixteen analyses to have this problem. You may run only one. But "
            "if you chose it after looking, and would have chosen differently had the data come out differently, "
            "then the other fifteen were in play all the same. The paths fork whether or not you walk them. "
            "<bookmark mark='e'/> That's why this chapter has the title it has. None of these habits feels like "
            "cheating. Each feels like judgement. People doing them were sincere, and many were careful. So "
            "exhortation doesn't fix it. What fixed the experimenter's influence in Part 2 was a procedure, the "
            "blind. This needs a procedure too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(wall), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, scale=2.0) for h in holes], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in target], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(steps[1], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(steps[2], shift=UP * 0.15))
        self.clear_scene()
