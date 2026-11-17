from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Glm(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_voxel()
        self.every_voxel()
        self.subtraction()

    def card(self):
        card = chapter_card(6, r"The linear model of an experiment", r"How does an experiment become a map?", lit=(),
                            part=PART, scale=("brain", "mind"), marr=("how",))
        with self.voiceover(
            "Chapter six. The linear model of an experiment."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_voxel(self):
        d = load("glm")
        head = heading(r"One voxel: \ how much of the prediction is in the data?")
        t = d["scans"]
        X = d["X"][:, 0]
        A = axes([0, 240], [-0.25, 1.15], x_length=11.4, y_length=1.05, xticks=[], yticks=[0, 1],
                 xlabel=r"", ylabel=r"", center=[-0.4, 2.1, 0])
        blocks = VGroup(*[Rectangle(width=np.linalg.norm(A.ax.c2p(20, 0) - A.ax.c2p(0, 0)), height=0.12, stroke_width=0,
                                    fill_color=SPIKE, fill_opacity=0.9).move_to(A.ax.c2p(float(o) + 10, -0.16))
                          for o in np.arange(20, 240, 40)])
        pred = curve(A.ax, t, X / X.max(), BLOOD, stroke_width=3.5)
        pl = label(r"task on (bars), \ and the predicted response", font_size=27, color=BLOOD).next_to(A, UP, buff=0.05)
        sb, st = round(d["silent_beta"], 2) + 0.0, round(d["silent_t"], 1) + 0.0  # no "minus zero" on screen
        B = axes([0, 240], [-3, 3], x_length=11.4, y_length=1.45, xticks=[], yticks=[-2, 0, 2],
                 xlabel=r"", ylabel=r"", center=[-0.4, 0.3, 0])
        ya = curve(B.ax, t, np.clip(d["active_y"], -3, 3), VOLT, stroke_width=1.8)
        fa = curve(B.ax, t, d["active_fit"], MODEL, stroke_width=4)
        bl = label(rf"a voxel in an active region: \ weight {d['active_beta']:.2f}, \ $t = {d['active_t']:.1f}$",
                   font_size=27, color=MODEL).next_to(B, UP, buff=0.05)
        C = axes([0, 240], [-3, 3], x_length=11.4, y_length=1.45, xticks=[0, 60, 120, 180, 240], yticks=[-2, 0, 2],
                 xlabel=r"time (s)", ylabel=r"", center=[-0.4, -2.05, 0])
        ys = curve(C.ax, t, np.clip(d["silent_y"], -3, 3), VOLT, stroke_width=1.8)
        fs = curve(C.ax, t, d["silent_fit"], NOISE, stroke_width=4)
        cl = label(rf"a voxel elsewhere: \ weight {sb:.2f}, \ $t = {st:.1f}$", font_size=27,
                   color=NOISE).next_to(C.ax.c2p(120, 3), UP, buff=0.12)
        tag = psyche_tag(r"simulated voxels (Psyche)")
        with self.voiceover(
            "Now an experiment. A person lies in the scanner and does a task for twenty seconds, rests for "
            "twenty, and so on, while an image is taken every two seconds. <bookmark mark='a'/> From the "
            "last chapter you can write down what a voxel that cares about the task should do: the on and "
            "off periods, convolved with the echo. That predicted curve is called a regressor. "
            "<bookmark mark='b'/> Here's the measured signal from one voxel. It's noisy, as always. Ask "
            "one question of it: what multiple of the prediction, added to a constant, fits this best? "
            f"Least squares answers: a weight of {d['active_beta']:.2f}. Divide the weight by its "
            f"uncertainty and you have a t statistic, here {d['active_t']:.1f}. <bookmark mark='c'/> And "
            f"here's a voxel somewhere else. Its best weight is {sb:.2f}, and its t is "
            f"{st:.1f}. Nothing. <bookmark mark='d'/> That's the whole analysis. It's the "
            "regression of Part 4, with a predictor built from the design of the experiment and the "
            "physiology of blood. The weight is how strongly this voxel followed the task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(blocks))
            vo.wait_until("a")
            self.play(Create(pred), FadeIn(pl), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(ya), run_time=2.0)
            self.play(Create(fa), FadeIn(bl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(C), Create(ys), run_time=1.5)
            self.play(Create(fs), FadeIn(cl), run_time=1.5)
            vo.wait_until("d")
        self.clear_scene()

    def every_voxel(self):
        d = load("tests")
        head = heading(r"The same fit in every voxel gives a map")
        truth = heat(d["truth"], 4.2, 0.0, float(d["truth"].max()) * 1.6, mask=d["mask"], center=[-4.8, -0.3, 0])
        tm = heat(np.clip(d["t"], 0, None), 4.2, 0.0, 8.0, mask=d["mask"], center=[-0.2, -0.3, 0])
        tl = label(r"where the task truly acts", font_size=28, color=MODEL).next_to(truth, UP, buff=0.12)
        ml = label(r"the map of $t$ values", font_size=28, color=THRESH).next_to(tm, UP, buff=0.12)
        blank = heat(np.zeros_like(d["truth"]), 4.2, 0.0, 1.0, mask=d["mask"], center=[-4.8, -0.3, 0])
        blank_l = label(r"a synthetic slice", font_size=28, color=GREY_A).next_to(blank, UP, buff=0.12)
        rows = rows_of([
            (rf"a slice of {fmt_int(d['voxels'])} voxels; \ {d['active']} of them respond to the task", WHITE),
            (r"one regression in each, \ one $t$ in each", WHITE),
            (r"no voxel knows about its neighbours: \ a map is thousands of separate tests", THRESH),
            (r"where do you draw the line between colour and no colour?", P.ACCENT),
        ], 4.3, 29, 0.32).move_to([4.75, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"a synthetic brain (Psyche)")
        with self.voiceover(
            "Do that in every voxel and you have a map. To see what such a map is worth, we need a brain "
            "where we know the answer, so here is a synthetic one. <bookmark mark='a'/> A slice of "
            f"{d['voxels']:,} voxels. In two patches, {d['active']} voxels in all, the signal "
            "really does follow the task, weakly. Everywhere else there's only noise, and the noise is "
            "smooth, so that neighbouring voxels resemble each other, as they do in a real scan. "
            "<bookmark mark='b'/> Run the regression in every voxel and colour each one by its t. The two "
            "patches show up. So do speckles where nothing is happening. <bookmark mark='c'/> Notice what "
            "the map is. It's not one finding. It's sixteen hundred separate tests laid side by side, and "
            "a real brain has a hundred times as many. <bookmark mark='d'/> The published picture comes "
            "from drawing a line: voxels above it get colour, voxels below it get none. Where to draw that "
            "line is the next chapter. It's where the salmon came from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(blank), FadeIn(blank_l))
            vo.wait_until("a")
            self.play(FadeOut(blank_l), FadeIn(truth), FadeIn(tl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tm), FadeIn(ml), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def subtraction(self):
        head = heading(r"What is the map a map of? \ Part 1's subtraction, again")
        a = VGroup(label(r"task A", font_size=38, color=THRESH),
                   wrapped_label(r"read a word aloud", 3.6, 33, WHITE)).arrange(DOWN, buff=0.12)
        b = VGroup(label(r"task B", font_size=38, color=NOISE),
                   wrapped_label(r"look at a word", 3.6, 33, WHITE)).arrange(DOWN, buff=0.12)
        minus = label(r"$-$", font_size=70)
        eq = label(r"$=$", font_size=70)
        c = VGroup(label(r"the map", font_size=38, color=MODEL),
                   wrapped_label(r"``the brain areas for speaking''?", 4.4, 33, WHITE)).arrange(DOWN, buff=0.12)
        line = VGroup(a, minus, b, eq, c).arrange(RIGHT, buff=0.5).move_to([0, 1.5, 0])
        if line.width > 13.2:
            line.width = 13.2
        rows = rows_of([
            (r"a map is always a contrast: \ one condition minus another", WHITE),
            (r"Donders, 1868: \ subtract two reaction times to time one mental step", DATA),
            (r"the same assumption: \ that adding a step leaves the other steps as they were (pure insertion)",
             THRESH),
            (r"So the map is only as good as the control task. \ ``Rest'' is not nothing: \ a resting brain is "
             r"busy.", P.ACCENT),
        ], 12.6, 30, 0.28).move_to([0, -1.6, 0])
        with self.voiceover(
            "Before that, one thing about what a map can mean. A voxel's signal has no natural zero, so "
            "nobody maps activity. They map a difference. <bookmark mark='a'/> The task, minus a control. "
            "Reading a word aloud, minus looking at a word. What's left is said to be the brain areas for "
            "speaking. <bookmark mark='b'/> You've seen this before. It's Donders, in Part 1, subtracting "
            "one reaction time from another to time a single step of thought. <bookmark mark='c'/> It "
            "carries the same assumption, pure insertion: that adding the step of speaking leaves "
            "everything else, the seeing and the reading, exactly as it was. Part 1 showed how that can "
            "fail. <bookmark mark='d'/> So a map is only as good as its control task. And the most common "
            "control of all, lying still and doing nothing, isn't nothing. A resting brain is busy, with "
            "the things minds do when left alone. Some regions are reliably more active at rest than in "
            "almost any task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in line], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
