from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.hearing()
        self.eyes_codecs()
        self.triangle()

    def card(self):
        card = chapter_card(13, r"In practice: \ hearing tests, \ eye charts and codecs",
                            r"Where is psychophysics used every day?", lit=(), part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: hearing tests, eye charts and codecs."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hearing(self):
        d = load("audio")
        head = heading(r"A hearing test is a staircase")
        lv, h = d["levels"], d["heard"]
        A = axes([0, len(lv) + 1], [10, 45], x_length=6.6, y_length=4.2, xticks=list(range(1, len(lv) + 1)), yticks=[10, 20, 30, 40],
                 xlabel=r"presentation", ylabel=r"tone level, \ dB", center=[-3.0, -0.35, 0])
        ax = A.ax
        line = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(i + 1, v) for i, v in enumerate(lv)])
        dots = VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.1, color=MODEL if x else BAD) for i, (v, x) in enumerate(zip(lv, h))])
        thr = DashedLine(ax.c2p(0, d["threshold"]), ax.c2p(len(lv) + 1, d["threshold"]), color=THRESH, stroke_width=3)
        tl = label(rf"the threshold: \ {d['threshold']:.0f} dB", font_size=26, color=THRESH).next_to(ax.c2p(len(lv) + 1, d["threshold"]),
                                                                                                    UP, buff=0.08).shift(LEFT * 1.4)
        rows = rows_of([
            (r"press the button when you hear the tone", WHITE),
            (r"heard: \ 10 dB softer; \ not heard: \ 5 dB louder (green: heard, \ red: not)", WHITE),
            (r"the threshold: \ the lowest level heard on 2 of 3 rising presentations", THRESH),
            (r"a staircase aimed at the 50\% point of a yes-no curve: \ the 1940s rule still in the audiometer", MODEL),
            (r"and the audiogram's decibels are a logarithmic scale: \ every 10 dB, \ ten times the power", GREY_A),
        ], 5.0, 28, 0.28).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: a listener whose 50\% point is 25 dB")
        with self.voiceover(
            "If you've had your hearing tested, you've been in a psychophysics experiment. "
            "<bookmark mark='a'/> A tone, and you press the button when you hear it. "
            "<bookmark mark='b'/> The rule most audiometers follow dates from the nineteen-forties: when "
            "you hear the tone, the next one is ten decibels softer; when you don't, five decibels louder. "
            "<bookmark mark='c'/> The threshold is the lowest level you hear on two of three rising "
            "presentations. <bookmark mark='d'/> It's a staircase, aimed at the halfway point of a yes-no "
            "curve. And the answer here sits a little above the listener's true halfway point, as the "
            "rule's large steps make it do. <bookmark mark='e'/> The scale itself is Fechner's legacy. A "
            "decibel is a logarithm: every ten decibels is ten times the power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots, lag_ratio=0.3), FadeIn(rows[1]), run_time=4.0)
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(tl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def eyes_codecs(self):
        head = heading(r"Eye charts, \ and what a codec throws away")
        chart = VGroup()
        letters = ["E", "F P", "T O Z", "L P E D", "P E C F D"]
        for i, row in enumerate(letters):
            chart.add(Text(row, font="DejaVu Sans", font_size=int(60 * 0.72 ** i), color=WHITE))
        chart.arrange(DOWN, buff=0.18).move_to([-4.6, 0.6, 0])
        frame = SurroundingRectangle(chart, color=GREY_D, buff=0.3, corner_radius=0.08)
        eye = rows_of([
            (r"an eye chart is the method of limits, \ descending: \ the letters shrink until you fail", WHITE),
            (r"a forced choice among letters, \ so the guess rate is small", GREY_A),
        ], 4.2, 27, 0.25).next_to(frame, DOWN, buff=0.35)
        codec = rows_of([
            (r"an image or a sound file carries far more detail than you can notice", WHITE),
            (r"a codec measures what it keeps in units of just noticeable difference, \ and discards changes smaller than one",
             WEBERC),
            (r"your phone's photos and music are psychophysics, \ compressed", THRESH),
            (r"and designers ask the same question of prices and packages: \ will anyone notice?", GREY_A),
        ], 6.2, 29, 0.32).move_to([3.4, 0.0, 0])
        keep_in_frame(codec)
        tag = note(r"an illustration").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Two more everyday uses. <bookmark mark='a'/> An eye chart is the method of limits, "
            "descending: the letters shrink, row by row, until you fail. Naming a letter is a forced "
            "choice among many, so the chance of guessing right is small. <bookmark mark='b'/> And every "
            "photograph on your phone, and every song you stream, has been through psychophysics. The file "
            "began with far more detail than you can notice. A codec measures detail in units of just "
            "noticeable difference, and throws away the changes smaller than one. <bookmark mark='c'/> "
            "The same question, will anyone notice, is asked of prices and packages by people who'd "
            "rather you didn't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(frame), FadeIn(chart[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in chart[1:]], lag_ratio=0.5), FadeIn(eye), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in codec[:3]], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("c")
            self.play(FadeIn(codec[3]))
        self.clear_scene()

    def triangle(self):
        d = load("triangle")
        head = heading(r"Can anyone taste the difference? \ The triangle test")
        cups = VGroup()
        for name, col in (("A", STD), ("B", YOU), ("A", STD)):
            body = Polygon([-0.42, 0.5, 0], [0.42, 0.5, 0], [0.32, -0.5, 0], [-0.32, -0.5, 0], color=col,
                           stroke_width=3, fill_opacity=0.18)
            cups.add(VGroup(body, label(name, font_size=30, color=col).move_to(body)))
        cups.arrange(RIGHT, buff=0.45).move_to([-4.6, 1.75, 0])
        odd = SurroundingRectangle(cups[1], color=YOU, buff=0.12, corner_radius=0.1)
        A = axes([0, 0.6], [0, 1.05], x_length=5.0, y_length=3.0, xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 0.5, 0.8, 1],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:g}",
                 xlabel=r"share of tasters who can really tell", ylabel=r"chance the panel finds it",
                 center=[-3.4, -1.55, 0])
        ax = A.ax
        cols = {12: GREY_B, 30: YOU, 60: MODEL, 120: WEBERC}
        lines = VGroup(*[curve(ax, d["d"], d[f"power_{n}"], c, stroke_width=4 if n == 30 else 3) for n, c in cols.items()])
        eighty = DashedLine(ax.c2p(0, 0.8), ax.c2p(0.6, 0.8), color=GREY_B, stroke_width=2)
        lg = legend([(c, rf"{n} tasters") for n, c in cols.items()], font_size=22).next_to(A, RIGHT, buff=0.1).shift(UP * 0.9)
        rows = rows_of([
            (r"a company changes a recipe. \ Three samples, \ two the same: \ which one is odd?", WHITE),
            (r"guessing is right a third of the time: \ the curve of chapter 4 with a floor of $\tfrac13$, \ not "
             r"$\tfrac12$", THRESH),
            (rf"with 30 tasters, \ {d['crit_30']} or more right is a difference at 5\%", YOU),
            (rf"if 30\% of people can really tell, \ 30 tasters find it {100 * d['power_30_at_30']:.0f}\% of the "
             rf"time; \ {d['need_30pct']} tasters find it 80\% of the time", MODEL),
            (rf"finding nothing is not showing nothing: \ to catch a difference one taster in ten can tell takes "
             rf"{d['need_10pct']} tasters", BAD),
        ], 5.2, 27, 0.24).move_to([4.15, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ exact binomial tests")
        with self.voiceover(
            "Food and drink companies run psychophysics every week. <bookmark mark='a'/> A manufacturer "
            "wants to change a recipe, a cheaper ingredient, less sugar, and needs to know whether "
            "customers will notice. The standard method is the triangle test. Each taster gets three "
            "samples, two the same and one different, and must pick the odd one out. "
            "<bookmark mark='b'/> Guessing is right a third of the time, so this is the psychometric "
            "curve of chapter four with a floor of one third instead of one half. "
            "<bookmark mark='c'/> With thirty tasters, "
            f"{d['crit_30']} or more right answers is a difference at the five percent level. "
            "<bookmark mark='d'/> Now the power. Suppose thirty percent of people can really taste the "
            "change and the rest guess. Thirty tasters find it "
            f"{100 * d['power_30_at_30']:.0f} percent of the time; it takes {d['need_30pct']} tasters to find "
            "it eighty percent of the time. <bookmark mark='e'/> And here's the trap. The company usually "
            "hopes for no difference, and a panel that finds nothing hasn't shown there is nothing. To "
            "catch a change that one taster in ten can tell, it needs "
            f"{d['need_10pct']} tasters. That's Part 4's lesson about power, in a bottle of juice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cups], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(odd), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(eighty), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), FadeIn(lg), FadeIn(rows[3]),
                      run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

