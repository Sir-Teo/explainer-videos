from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

GO = "#3DDC84"
LEFT_COLOR = "#5DADEC"


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.simple()
        self.choice()
        self.reveal()
        self.puzzle()

    def card(self):
        card = chapter_card(1, r"How fast are you?", r"Before any history, an experiment. You are the subject.",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter one. Before any history, an experiment, and you are the subject."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def counter(self, stage, i, n):
        t = label(rf"trial {i} of {n}", font_size=24, color=GREY_B)
        return t.move_to(stage.box.get_corner(UR) + LEFT * 1.3 + DOWN * 0.4)

    def simple(self):
        stage = demo_stage(9.6, 4.3).shift(UP * 0.55)
        c = stage.box.get_center()
        lamp = Circle(radius=0.8, stroke_color=GREY_B, stroke_width=3, fill_color=GREY_D, fill_opacity=1).move_to(c)
        go = Circle(radius=0.8, stroke_color=WHITE, stroke_width=3, fill_color=GO, fill_opacity=1).move_to(c)
        cap = label(r"when the circle turns green: \ tap", font_size=32, color=GREY_A).next_to(stage, DOWN, buff=0.45)
        with self.voiceover(
            "Put one finger on the desk in front of you. <bookmark mark='a'/> In this frame there's a grey "
            "circle. At some moment it will turn green. When it does, tap, as fast as you can. Three tries. "
            "Ready."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(lamp), FadeIn(cap))
        n = 3
        for i, fore in enumerate((2.3, 1.4, 2.9), 1):
            cnt = self.counter(stage, i, n)
            self.add(cnt)
            self.wait(fore)
            self.remove(lamp)
            self.add(go)
            self.wait(0.9)
            self.remove(go, cnt)
            self.add(lamp)
            self.wait(0.5)
        self.stage, self.lamp, self.cap = stage, lamp, cap

    def choice(self):
        stage, c = self.stage, self.stage.box.get_center()
        cross = MathTex(r"+", font_size=70, color=GREY_B).move_to(c)
        right = Circle(radius=0.8, stroke_color=WHITE, stroke_width=3, fill_color=GO, fill_opacity=1)
        left = Square(side_length=1.5, stroke_color=WHITE, stroke_width=3, fill_color=LEFT_COLOR, fill_opacity=1)
        right.move_to(c)
        left.move_to(c)
        key_l = VGroup(left.copy().scale(0.28), label(r"blue square: \ left hand", font_size=28, color=LEFT_COLOR))
        key_r = VGroup(right.copy().scale(0.28), label(r"green circle: \ right hand", font_size=28, color=GO))
        for k in (key_l, key_r):
            k.arrange(RIGHT, buff=0.25)
        key = VGroup(key_l, key_r).arrange(RIGHT, buff=1.2).next_to(stage, DOWN, buff=0.45)
        with self.voiceover(
            "Now a choice. <bookmark mark='a'/> If a green circle appears, tap with your right hand. If a blue "
            "square appears, tap with your left. You won't know which is coming. Four tries."
        ) as vo:
            self.play(FadeOut(self.lamp), FadeOut(self.cap))
            vo.wait_until("a")
            self.play(FadeIn(key), FadeIn(cross))
        n = 4
        for i, (fore, stim) in enumerate(((1.8, right), (2.5, left), (1.3, left), (2.1, right)), 1):
            cnt = self.counter(stage, i, n)
            self.add(cnt)
            self.wait(fore)
            self.remove(cross)
            self.add(stim)
            self.wait(1.0)
            self.remove(stim, cnt)
            self.add(cross)
            self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        d = load("rt_shape")
        w = d["woods"]
        t = np.asarray(d["t"])
        ticks = [100, 200, 300, 400, 500, 600, 700, 800]
        top = rt_axes([100, 800], 0.019, x_length=10.6, y_length=1.7, center=[0.2, 1.55, 0], xlabel="")
        bot = rt_axes([100, 800], 0.0058, x_length=10.6, y_length=2.5, center=[0.2, -1.55, 0], xticks=ticks)
        ax1, ax2 = top.ax, bot.ax
        simple = curve(ax1, t, d["pdf_simple"], P.PSYCHE, 4)
        published = DashedLine(ax1.c2p(w["mean_corrected_ms"], 0), ax1.c2p(w["mean_corrected_ms"], 0.0185),
                               color=P.HUMAN, stroke_width=3)
        pub_lab = label(rf"{fmt_int(w['n'])} adults: \ mean {w['mean_corrected_ms']:.0f} ms", font_size=26,
                        color=P.HUMAN).next_to(ax1.c2p(250, 0.014), RIGHT, buff=0.1)
        s_lab = label(r"a simple reaction", font_size=30, color=P.PSYCHE).move_to(ax1.c2p(640, 0.011))
        bars = hist(ax2, d["edges"], d["hist_choice"], P.PSYCHE, 0.4)
        ex = curve(ax2, t, d["exgauss_pdf"], P.PSYCHE, 4)
        normal = curve(ax2, t, d["normal_pdf"], GREY_A, 3)
        c_lab = label(r"a choice", font_size=30, color=P.PSYCHE).move_to(ax2.c2p(165, 0.0035))
        n_lab = label(r"a bell curve with the same mean and spread", font_size=24, color=GREY_A)
        n_lab.next_to(ax2.c2p(430, 0.0052), RIGHT, buff=0.1)
        n_arrow = Arrow(n_lab.get_left() + LEFT * 0.05, ax2.c2p(395, 0.0046), buff=0.05, color=GREY_A,
                        stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        tail = label(r"the long tail of slow responses", font_size=26, color=P.ACCENT)
        tail.move_to(ax2.c2p(655, 0.0031))
        tail_line = Line(ax2.c2p(520, 0.0022), ax2.c2p(790, 0.0022), color=P.ACCENT, stroke_width=3)
        head = heading(r"What people get")
        tag = psyche_tag(r"curves: Psyche (a model; \ its choice stages are illustrative)")
        src = published_tag(archive.WOODS_2015.cite)
        with self.voiceover(
            "You can't see your own numbers yet. On this part's page of the course site, the same experiment "
            "runs in your browser and shows them to you. Here is what people get. <bookmark mark='a'/> A simple "
            "reaction to a light takes about a fifth of a second. In a study of "
            f"{w['n']:,} adults, the average was {w['mean_corrected_ms']:.0f} milliseconds. "
            "<bookmark mark='b'/> A choice takes longer. And notice the shape. The times don't pile up evenly "
            "around their average. <bookmark mark='c'/> A bell curve with the same average and spread misses: "
            "it's too low at the peak, and it gives out too early on the right. <bookmark mark='d'/> Reaction "
            "times lean. There's a hump, and then a long tail of slow responses. That tail is a clue about what "
            "deciding is, and all of Part 25 is spent on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(bot), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(simple), FadeIn(s_lab))
            self.play(Create(published), FadeIn(pub_lab))
            vo.wait_until("b")
            self.play(FadeIn(bars, lag_ratio=0.05), FadeIn(c_lab), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(normal), FadeIn(n_lab), GrowArrow(n_arrow))
            vo.wait_until("d")
            self.play(Create(ex), Create(tail_line), FadeIn(tail))
        self.clear_scene()

    def puzzle(self):
        d = load("rt_shape")
        unit = 0.026
        simple = stage_bar([(r"simple", d["mean_simple"], METHOD["a"])], unit=unit, height=0.9, font_size=32)
        choice = stage_bar([(r"choice", d["mean_choice"], METHOD["b"])], unit=unit, height=0.9, font_size=32)
        simple.names[0].next_to(simple.cells[0], LEFT, buff=0.3)
        choice.names[0].next_to(choice.cells[0], LEFT, buff=0.3)
        choice.shift(DOWN * 1.7 + RIGHT * (simple.cells[0].get_left()[0] - choice.cells[0].get_left()[0]))
        g = VGroup(simple, choice).move_to([0.4, 0.3, 0])
        extra = Line([simple.cells[0].get_right()[0], choice.cells[0].get_bottom()[1], 0],
                     choice.cells[0].get_corner(DR))
        br = brace_note(extra, rf"{d['mean_choice'] - d['mean_simple']:.0f} ms more: \ doing what?", DOWN, P.ACCENT,
                        font_size=30)
        q = label(r"The same eyes. \ The same finger.", font_size=44).to_edge(UP, buff=0.8)
        tag = psyche_tag(r"bars: Psyche (a model)")
        with self.voiceover(
            "So here is the first puzzle of the series. Your choice took longer than your simple reaction. "
            "<bookmark mark='a'/> The same eyes, and the same finger. <bookmark mark='b'/> What were you doing "
            "with the extra time, and can it be measured? <bookmark mark='c'/> Before anyone could ask that, "
            "somebody had to show that a nervous system takes any time at all."
        ) as vo:
            self.play(FadeIn(simple), FadeIn(choice), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(br))
        self.clear_scene()
