from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.war()
        self.table()
        self.factory()
        self.objectives()

    def war(self):
        tl = timeline(lit=(1943,)).to_edge(UP, buff=0.35)
        hc = history_card(1943, r"the Economic Warfare Division, \ US Embassy, London", r"how many tanks is Germany building? \ "
                          r"spies and prisoners gave one answer; \ the serial numbers stamped on captured tanks gave another",
                          color=S.MUSEUM, width=8.4, font_size=24).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"gearboxes, \ chassis, \ engines, \ and the moulds of the road wheels carried numbers", font_size=24),
            label(r"numbered in sequence: \ the largest number seen says something about how many exist", font_size=24, color=S.ACCENT),
            label(r"R. Ruggles \& H. Brodie, \ \emph{JASA} (1947), \ told the story after the war", font_size=22, color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "In the Second World War, Allied planners needed a number: how many tanks was Germany building each month? "
            "<bookmark mark='a'/> Conventional intelligence, from spies, aerial photographs and prisoners, gave one "
            "answer. A small group of economists and statisticians in London found another, in the serial numbers "
            "stamped on the parts of captured and destroyed tanks. <bookmark mark='b'/> Gearboxes, chassis and engines "
            "were numbered, and so were the moulds that cast the road wheels. <bookmark mark='c'/> Numbers issued in "
            "sequence carry information: the largest one you've seen tells you something about how many exist. "
            "<bookmark mark='d'/> Richard Ruggles and Henry Brodie described the work after the war, in 1947."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        rows_ = museum.TANKS
        hdr = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (r"month", r"statistical", r"intelligence", r"German records")])
        xs = [-4.6, -1.4, 1.6, 4.6]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.0, 0])
        line = Line([-6.2, 1.6, 0], [6.2, 1.6, 0], color=GREY_D)
        cells = VGroup()
        for i, (mo, st, it, gr) in enumerate(rows_):
            y = 1.0 - 0.75 * i
            cells.add(VGroup(label(mo, font_size=26).move_to([xs[0], y, 0]),
                             MathTex(str(st), font_size=32, color=SIM).move_to([xs[1], y, 0]),
                             MathTex(f"{it:,}".replace(",", "{,}"), font_size=32, color=S.RESID).move_to([xs[2], y, 0]),
                             MathTex(str(gr), font_size=32, color=EXACT).move_to([xs[3], y, 0])))
        take = label(r"the serial numbers came close, \ and closer each year; \ intelligence was four to eight times too high", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.9)
        src = historical_tag(r"Ruggles \& Brodie (1947), \ monthly production", corner=DR)
        with self.voiceover(
            "Here are three months from their table. <bookmark mark='a'/> June 1940: the statistical estimate, from "
            "serial numbers, was a hundred and sixty-nine tanks. Intelligence said a thousand. When the German records "
            "were captured after the war, the true figure was a hundred and twenty-two. <bookmark mark='b'/> June 1941: "
            "two hundred and forty-four from the statistics, fifteen hundred and fifty from intelligence, two hundred "
            "and seventy-one in fact. <bookmark mark='c'/> August 1942: three hundred and twenty-seven, fifteen hundred "
            "and fifty, and three hundred and forty-two. <bookmark mark='d'/> The serial numbers were usually close; "
            "intelligence was five to ten times too high. How do you turn a handful of serial numbers into a count?"
        ) as vo:
            self.play(FadeIn(hdr), Create(line), FadeIn(src))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cells[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def factory(self):
        d = load("tanks")
        one = d["one"]
        f = TankFactory(d["N"], one, cols=30, cell=0.22, center=[0, 0.9, 0])
        f.tanks.set_fill(opacity=0.0)
        q = MathTex(r"N = \ ?", font_size=44, color=GREY_A).move_to([0, 3.0, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\text{captured serials: }" + ",\\ ".join(str(s_) for s_ in one), font_size=30, color=S.ACCENT),
            MathTex(rf"\text{{largest: }} m = {max(one)}", font_size=30),
            MathTex(rf"2\bar x - 1 = {d['one_est']['mom']:.0f},\qquad m\big(1 + \tfrac16\big) - 1 = {d['one_est']['umvue']:.0f}", font_size=30,
                    color=SIM),
        ), 12.6, 0.28, [0, -1.8, 0])
        ans = MathTex(rf"N = {d['N']}", font_size=40, color=EXACT).move_to(q)
        game = label(r"Built in this part: \ the tank factory game, \ which grades any estimator on 10,000 factories", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here's the problem in miniature, and we'll play it all part long. <bookmark mark='a'/> A factory has built "
            "some number of tanks, N, numbered one to N. We can't see them. <bookmark mark='b'/> We capture six, at "
            "random, and read their serial numbers. <bookmark mark='c'/> The largest is two hundred and fourteen. N is at "
            "least that. But how much bigger? <bookmark mark='d'/> Two recipes: double the average and subtract one, "
            "which gives two hundred and five, less than a serial number we've actually seen; or scale up the largest "
            "a little, which gives two hundred and forty-nine. <bookmark mark='e'/> The truth: three hundred. Neither "
            "is right this time; no estimator is right every time. The question is which recipe is best on average, and "
            "how good any recipe could possibly be. That's what estimation theory answers."
        ) as vo:
            self.add(f.tanks)
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(f.tanks.animate.set_fill(opacity=0.12))
            vo.wait_until("b")
            self.play(f.capture_anims(lag=0.25))
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(f.reveal(0.8), Transform(q, ans), FadeIn(game))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 9", font_size=34, color=GREY_B), label(r"Estimation", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"estimators as recipes, \ judged by their sampling distributions",
            r"the method of moments; \ maximum likelihood, \ its curvature and its standard error",
            r"sufficiency: \ what in the data matters; \ Rao--Blackwell: \ conditioning never hurts",
            r"the best unbiased estimator; \ Fisher information; \ the Cram\'er--Rao bound, \ and how the tanks beat it",
            r"comparing estimators, \ and what happens when the model is wrong",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Part 8").to_corner(DL, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part nine: estimation. <bookmark mark='b'/> We'll treat estimators as recipes and judge "
            "them by their sampling distributions; build them by the method of moments and by maximum likelihood, the "
            "most important idea in statistical inference; find out which parts of the data matter, with sufficiency; "
            "improve any estimator by conditioning, with the Rao–Blackwell theorem; find the best unbiased estimator; "
            "and meet the Cramér–Rao bound, the speed limit for unbiased estimation, which the tanks manage to break."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
        self.wait(1.0)
        self.clear_scene()
