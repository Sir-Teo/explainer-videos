from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403


class AB(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Tests in industry", r"What happens when everyone peeks?", lit=(1945,),
                            part=PART)
        with self.voiceover("Chapter eleven. Tests in industry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.abtest()
        self.peeking()
        self.boundaries()
        self.lessons()

    def abtest(self):
        head = label(r"The A/B test", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        users = VGroup(*[Dot(radius=0.07, color=GREY_B) for _ in range(60)]).arrange_in_grid(6, 10, buff=0.18).move_to(
            [-4.6, -0.4, 0])
        a_box = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=NEYP, stroke_width=2).move_to(
            [0.6, 0.6, 0])
        b_box = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=FISH, stroke_width=2).move_to(
            [0.6, -1.4, 0])
        at = label(r"A: \ the old page \ \ 10.0\%", font_size=21, color=NEYP).move_to(a_box)
        bt = label(r"B: \ the new button \ \ 10.6\%", font_size=21, color=FISH).move_to(b_box)
        arr = VGroup(Arrow([-3.0, -0.2, 0], a_box.get_left(), buff=0.1, color=GREY_B, stroke_width=3),
                     Arrow([-3.0, -0.6, 0], b_box.get_left(), buff=0.1, color=GREY_B, stroke_width=3))
        rl = label(r"randomize", font_size=19, color=GREY_B).next_to(arr, UP, buff=0.05)
        side = stack([(r"randomization: \ Fisher's idea \ (1935), \ at the scale of millions", WHITE),
                      (r"tens of thousands of experiments a year at the largest firms", GREY_A),
                      (r"`most ideas fail to improve the metric they were designed to improve'", BAD),
                      (r"Kohavi, \ Tang and Xu \ (2020)", HIST)], font_size=20, aligned_edge=LEFT, width=4.3).move_to(
            [4.7, -0.4, 0])
        with self.voiceover(
            "Fisher's randomized experiment now runs the internet. <bookmark mark='a'/>Visitors to a web site are "
            "randomly split. <bookmark mark='b'/>Half see the old page, half see a new button, and the company "
            "compares conversion rates: say ten percent against ten point six. <bookmark mark='c'/>The largest "
            "firms run tens of thousands of such experiments a year. <bookmark mark='d'/>And their experience, "
            "summarized by Ron Kohavi, Diane Tang and Ya Xu, is humbling: most ideas fail to improve the metric "
            "they were designed to improve. Telling small real effects from noise is the whole job."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(users, lag_ratio=0.02), GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(rl))
            vo.wait_until("b")
            self.play(Create(a_box), Create(b_box), FadeIn(at), FadeIn(bt))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def peeking(self):
        d = load("ab")
        head = label(r"The peeking problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        sub = label(f"{d['runs']:,}".replace(",", "{,}") + r" A/A tests: \ no real difference, \ " +
                    f"{d['visitors']:,}".replace(",", "{,}") + r" visitors per arm, \ a dashboard checked " +
                    str(d["looks"]) + r" times", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        base = Line([-3.6, -2.4, 0], [3.6, -2.4, 0], color=GREY_C, stroke_width=2)
        vals = [(r"look once", 0.05, NEYP), (r"stop at the first $p < 0.05$", d["peeking_fp"], BAD),
                (r"betting e-process", d["e_process_fp"], OK)]
        bars = VGroup()
        for i, (t, v, c) in enumerate(vals):
            b = Rectangle(width=1.5, height=max(v * 9, 0.03), stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-2.6 + 2.6 * i, -2.4 + b.height / 2, 0])
            pct = label(rf"{100 * v:.0f}\%", font_size=26, color=c).next_to(b, UP, buff=0.1)
            lab = label(t, font_size=18, color=GREY_A).next_to(b, DOWN, buff=0.15)
            bars.add(VGroup(b, pct, lab))
        foot = label(r"false `wins' among experiments that change nothing", font_size=21, color=GREY_B).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Chapter five's problem, at industrial scale. <bookmark mark='a'/>Run two thousand A/A tests, in which "
            "both arms are identical, with a dashboard that shows the p-value after every hundred visitors. "
            "<bookmark mark='b'/>A team that looks once, at the planned end, declares a false win five percent of "
            "the time. <bookmark mark='c'/>A team that stops as soon as the dashboard shows p below point zero five "
            "declares a false win in thirty-one percent of experiments that changed nothing. "
            "<bookmark mark='d'/>A team that instead tracks a betting e-process, which chapter twelve explains, and "
            "stops when it reaches twenty, is wrong four percent of the time, however often it looks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(base))
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[i][0], DOWN), FadeIn(bars[i][1]), FadeIn(bars[i][2]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def boundaries(self):
        head = label(r"Sequential tests: \ spend $\alpha$ as you go", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        K = 5
        ax = Axes(x_range=[0, K + 0.5, 1], y_range=[0, 5, 1], x_length=7.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.4, -0.9, 0])
        xl = label(r"look", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"$|z|$ needed to stop", font_size=18, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1).align_to(
            ax.y_axis, LEFT)
        naive = DashedLine(ax.c2p(0.5, 1.96), ax.c2p(K + 0.3, 1.96), color=BAD, stroke_width=2)
        nl = label(r"1.96 every time: \ invalid", font_size=17, color=BAD).next_to(naive, RIGHT, buff=0.05).shift(
            DOWN * 0.15)
        pocock = VGroup(*[Dot(ax.c2p(k, 2.413), radius=0.08, color=FISH) for k in range(1, K + 1)])
        obf = VGroup(*[Dot(ax.c2p(k, 2.040 * math.sqrt(K / k)), radius=0.08, color=ALTC) for k in range(1, K + 1)])
        obf_l = series_plot(ax, [2.040 * math.sqrt(K / k) for k in range(1, K + 1)], ALTC, xs=list(range(1, K + 1)),
                            width=2)
        side = stack([(r"Wald's sequential test \ (1945): \ wartime quality control", HIST),
                      (r"Pocock \ (1977): \ the same, \ higher bar at every look", FISH),
                      (r"O'Brien and Fleming \ (1979): \ strict early, \ near 1.96 at the end", ALTC),
                      (r"always-valid $p$-values \ (Johari et al., \ 2017)", OK)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -0.5, 0])
        with self.voiceover(
            "Statisticians have long known how to look repeatedly and stay honest. <bookmark mark='a'/>Abraham Wald "
            "invented the sequential probability ratio test during the Second World War, to inspect munitions with "
            "fewer samples. <bookmark mark='b'/>Comparing to one point nine six at every look is invalid. "
            "<bookmark mark='c'/>Stuart Pocock's design, for five planned looks, raises the bar to two point four "
            "one at each of them. <bookmark mark='d'/>Peter O'Brien and Thomas Fleming spend almost no error early, "
            "demanding a z of four and a half at the first look, and almost two at the last. "
            "<bookmark mark='e'/>And in 2017 Ramesh Johari and colleagues gave A/B platforms always-valid p-values, "
            "which may be watched continuously."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(naive), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(pocock), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(obf_l), FadeIn(obf), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lessons(self):
        head = label(r"Industrial epistemology", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Twyman's law", r"any figure that looks interesting or different is usually wrong", FISH),
            (r"guardrails", r"check the split itself: \ a sample-ratio mismatch voids the test", NEYP),
            (r"many metrics", r"fifty metrics, \ one will move: \ the garden, \ again", BAD),
            (r"the base rate", r"if 1 idea in 10 works, \ one `win' in five is false at power 0.8, \ one in three at "
                              r"power 0.5: \ Chapter 3", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Experimentation teams have rediscovered the philosophy of this part as rules of thumb. "
            "<bookmark mark='a'/>Twyman's law: any figure that looks interesting or different is usually wrong. "
            "<bookmark mark='b'/>Check the randomization itself before believing the result. "
            "<bookmark mark='c'/>Watch fifty metrics and one will move by chance: the garden of forking paths again. "
            "<bookmark mark='d'/>And because most ideas fail, the base rate is low. If one idea in ten really "
            "works, about one win in five is false when tests have power point eight, and one in three when power "
            "is point five, as Ioannidis's formula predicts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
