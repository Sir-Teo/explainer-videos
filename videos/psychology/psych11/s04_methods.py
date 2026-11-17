from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Methods(VoiceoverScene):
    def construct(self):
        self.card()
        self.limits()
        self.adjustment()
        self.constant()
        self.criterion()

    def card(self):
        card = chapter_card(3, r"Three classical methods", r"How do you find a step you can only just notice?",
                            lit={1860: r"Fechner's \emph{Elements}"}, part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter three. Three classical methods."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def limits(self):
        d = load("methods")
        head = heading(r"1. \ The method of limits")
        A = axes([0, 4], [0, 42], x_length=6.6, y_length=4.4, xticks=[], yticks=[0, 10, 20, 30, 40],
                 xlabel=r"four series, \ alternately down and up", ylabel=r"the increment over a standard of 100",
                 center=[-3.0, -0.35, 0])
        ax = A.ax
        series = VGroup()
        for j in range(4):
            lv, ans = d[f"series_{j}_levels"], d[f"series_{j}_answers"]
            x0 = j + 0.5
            g = VGroup()
            for k_, (v, a) in enumerate(zip(lv, ans)):
                col = MODEL if a else BAD
                g.add(Dot(ax.c2p(x0, v), radius=0.07, color=col))
            last = lv[len(ans) - 1]
            g.add(Line(ax.c2p(x0 - 0.35, last), ax.c2p(x0 + 0.35, last), color=THRESH, stroke_width=4))
            g.add(label(r"down" if j % 2 == 0 else r"up", font_size=24, color=GREY_A).next_to(ax.c2p(x0, 0), DOWN, buff=0.15))
            series.add(g)
        lg = VGroup(label(r"green: \ ``yes, it's more''", font_size=25, color=MODEL),
                    label(r"red: \ ``no''", font_size=25, color=BAD)).arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.1)
        rows = rows_of([
            (r"step the comparison down until the answer changes from yes to no; \ then up, \ until it changes back", WHITE),
            (r"the threshold: \ the average of the changeovers", THRESH),
            (rf"Psyche, \ eight series: \ ${d['limits_threshold']:.1f}$. \ Descending series stop late "
             rf"(${d['limits_down']:.1f}$), \ ascending ones early (${d['limits_up']:.1f}$)", WEBERC),
        ], 5.2, 28, 0.3).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's observer, \ steps of 2.5")
        with self.voiceover(
            "The first is the method of limits. A standard of 100, and a comparison that starts well "
            "above it. <bookmark mark='a'/> Step the comparison down, a little at a time, and ask each "
            "time: is it more? Stop when the answer changes from yes to no. Then start below and step "
            "up, until it changes back. <bookmark mark='b'/> The threshold is the average of the "
            "changeovers. <bookmark mark='c'/> On Psyche, eight series give "
            f"{d['limits_threshold']:.1f}. And look at the two directions. Descending series stop late, "
            f"around {d['limits_down']:.0f}, because one noisy no ends the series. Ascending ones stop "
            f"early, around {d['limits_up']:.0f}, because one noisy yes ends it. The method's answer "
            "depends on its own stopping rule. Fechner knew, and averaged the two directions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lg), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g, lag_ratio=0.1) for g in series], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def adjustment(self):
        d = load("methods")
        head = heading(r"2. \ The method of adjustment")
        s = d["adj_settings"]
        A = axes([70, 130], [0, 21], x_length=7.2, y_length=3.6, xticks=[70, 80, 90, 100, 110, 120, 130], yticks=[],
                 xlabel=r"where the comparison was set", ylabel=r"", center=[-2.6, -0.2, 0])
        ax = A.ax
        std = DashedLine(ax.c2p(100, 0), ax.c2p(100, 21), color=STD, stroke_width=3)
        sl = label(r"the standard", font_size=25, color=STD).next_to(ax.c2p(100, 21), UP, buff=0.08)
        dots = VGroup(*[Dot(ax.c2p(v, 1.0 + j), radius=0.09, color=YOU) for j, v in enumerate(s)])
        pse = Line(ax.c2p(d["adj_pse"], 0), ax.c2p(d["adj_pse"], 21), color=MODEL, stroke_width=4)
        knob = VGroup(Circle(radius=0.45, color=GREY_B, stroke_width=4), Line(ORIGIN, UP * 0.4, color=GREY_B, stroke_width=4))
        knob.move_to([-5.9, 3.35, 0])
        rows = rows_of([
            (r"the observer turns a knob until the two look the same", WHITE),
            (rf"the average setting: \ the point of subjective equality, \ ${d['adj_pse']:.1f}$", MODEL),
            (rf"their spread: \ a standard deviation of ${d['adj_sd']:.1f}$, \ which converts to a just noticeable "
             rf"difference of ${d['adj_jnd']:.1f}$ \ (the true one: ${d['jnd']:.1f}$)", WEBERC),
            (r"quick, \ natural, \ and the observer controls the stimulus: \ which makes it hard to check", GREY_A),
        ], 5.0, 28, 0.28).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's observer, \ 20 settings")
        with self.voiceover(
            "The second is the method of adjustment, which Fechner called the method of average error. "
            "<bookmark mark='a'/> The observer turns a knob until the comparison looks the same as the "
            "standard. Twenty times. <bookmark mark='b'/> The average setting is the point of subjective "
            f"equality: here {d['adj_pse']:.1f}, close to the standard. <bookmark mark='c'/> And the "
            "spread of the settings measures the threshold. A noisier observer misses by more. Here the "
            f"settings have a standard deviation of {d['adj_sd']:.1f}, which converts to a just noticeable "
            f"difference of {d['adj_jnd']:.1f}. The observer's true one is {d['jnd']:.1f}. "
            "<bookmark mark='d'/> It's quick and natural. But the observer controls the stimulus, so "
            "nothing stops them using a strategy, and nothing checks the settings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(std), FadeIn(sl), FadeIn(knob))
            vo.wait_until("a")
            self.play(Rotate(knob, angle=-PI / 2), FadeIn(rows[0]), FadeIn(dots, lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(pse), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def constant(self):
        d = load("methods")
        head = heading(r"3. \ The method of constant stimuli")
        A = axes([0, 25], [0.4, 1.02], x_length=7.0, y_length=4.2, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"the increment over a standard of 100",
                 ylabel=r"share of trials right", center=[-2.8, -0.35, 0])
        ax = A.ax
        chance = DashedLine(ax.c2p(0, 0.5), ax.c2p(25, 0.5), color=GREY_C, stroke_width=2)
        cl = label(r"guessing", font_size=24, color=GREY_A).next_to(ax.c2p(25, 0.5), UP, buff=0.05).shift(LEFT * 0.6)
        p = d["cs_k"] / d["cs_n"]
        bars = VGroup(*[Dot(ax.c2p(x, y), radius=0.1, color=YOU) for x, y in zip(d["cs_delta"], p)])
        nums = VGroup(*[label(rf"{int(k)}/{int(n)}", font_size=22, color=GREY_A).next_to(ax.c2p(x, y), UP, buff=0.12)
                        for x, y, k, n in zip(d["cs_delta"], p, d["cs_k"], d["cs_n"])])
        rows = rows_of([
            (r"fix eight increments in advance; \ show each 40 times, \ in random order", WHITE),
            (r"two intervals, \ one with the increment: \ which was more?", WHITE),
            (r"Fechner's ``right and wrong cases'': \ count the right answers at each level", THRESH),
            (r"slow, \ but each trial is independent, \ and the counts can be fitted", MODEL),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: Psyche's observer, \ 320 trials")
        with self.voiceover(
            "The third is the method of constant stimuli, Fechner's method of right and wrong cases. "
            "<bookmark mark='a'/> Fix eight increments in advance, and show each one forty times, in "
            "random order. <bookmark mark='b'/> On each trial there are two intervals, one with the "
            "standard and one with the standard plus the increment, and the question is which was more. "
            "<bookmark mark='c'/> Count the right answers at each level. At the smallest increments it's "
            "near half, which is guessing. At the largest it's near all. <bookmark mark='d'/> It's slow: "
            "three hundred and twenty trials here. But the trials are independent and the order is "
            "random, so nothing the observer expects can steer it, and the counts can be fitted, which "
            "is chapter six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(chance), FadeIn(cl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars, lag_ratio=0.2), FadeIn(nums, lag_ratio=0.2), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def criterion(self):
        d = load("methods")
        head = heading(r"The trouble with asking ``yes or no?''")
        crits = [(0.5, r"says yes easily"), (1.0, r"in between"), (1.5, r"says yes reluctantly")]
        bars = VGroup()
        for i, (c, name) in enumerate(crits):
            v = d[f"crit_{c}"]
            y = 1.6 - 1.2 * i
            bar = Rectangle(width=v * 0.3, height=0.55, stroke_width=0, fill_color=WEBERC, fill_opacity=0.85)
            bar.move_to([-3.2, y, 0], aligned_edge=LEFT)
            nm = label(name, font_size=29, color=WHITE).next_to(bar, LEFT, buff=0.3)
            nm.align_to(np.array([-6.6, 0, 0]), LEFT)
            val = label(rf"${v:.1f}$", font_size=30, color=WEBERC).next_to(bar, RIGHT, buff=0.2)
            bars.add(VGroup(nm, bar, val))
        cap = label(r"the method of limits' threshold, \ same eyes, \ three observers' habits", font_size=27,
                    color=GREY_A).next_to(bars, UP, buff=0.3)
        rows = rows_of([
            (r"the three observers have the same noise: \ the same sensitivity", WHITE),
            (r"they differ only in how sure they want to be before they say yes", THRESH),
            (r"a yes-no threshold mixes the two together", BAD),
            (r"two intervals, \ ``which was more?'': \ there is no yes to be cautious about. \ The fix, \ and Part 12's "
             r"subject", MODEL),
        ], 12.4, 30, 0.22).to_edge(DOWN, buff=0.55)
        tag = psyche_tag(r"computed: medians of 200 runs each")
        with self.voiceover(
            "The method of limits has a deeper problem than its stopping rule. Run it on three versions "
            "of Psyche with exactly the same noise in the head: the same sensitivity. "
            "<bookmark mark='a'/> One says yes easily. One is in between. One wants to be sure before it "
            f"says yes. Their thresholds: {d['crit_0.5']:.1f}, {d['crit_1.0']:.1f} and "
            f"{d['crit_1.5']:.1f}. <bookmark mark='b'/> Same eyes, different answers, because a yes-or-no "
            "question measures two things at once: how well you can see the difference, and how sure you "
            "want to be before you say so. <bookmark mark='c'/> The fix is in the third method's design. "
            "Show two intervals and ask which was more. There is no yes to be cautious about. Separating "
            "what you can see from what you're willing to say is the whole of Part 12."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cap), *[FadeIn(b[0]) for b in bars])
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in bars], lag_ratio=0.5),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
