from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Views(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Total, average, and between", r"How do we compare different numbers of people?",
                            lit=(1984,), part=PART)
        with self.voiceover("Chapter one. Total, average, and between."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.formulas()
        self.scored()

    def question(self):
        hc = history_card(1984, r"Derek Parfit", r"\textit{Reasons and Persons}, \ Part Four", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        a = parfit_bars([(10, 10)], -4.6, -2.2, unit_w=0.16, unit_h=0.24, color=WELL)
        b = parfit_bars([(20, 6)], 0.6, -2.2, unit_w=0.16, unit_h=0.24, color=POP)
        la = label(r"A: \ 10 people at 10", font_size=20, color=WELL).next_to(a, DOWN, buff=0.2)
        lb = label(r"B: \ 20 people at 6", font_size=20, color=POP).next_to(b, DOWN, buff=0.2)
        cap = label(r"width: \ how many people; \ height: \ how well each life goes", font_size=18,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        q = label(r"which is better?", font_size=26, color=GOAL).move_to([0.3, 1.5, 0])
        side = stack([(r"same-number choices: \ Part 35's theories apply", GREY_A),
                      (r"different-number choices: \ who exists depends on what we do", FUT)],
                     font_size=19, aligned_edge=LEFT, width=5.4, buff=0.25).move_to([3.3, 2.4, 0])
        with self.voiceover(
            "Most of ethics compares outcomes for a fixed set of people. Derek Parfit's Reasons and Persons, in its "
            "fourth part, asked what happens when the number itself is in play. <bookmark mark='a'/>Parfit drew "
            "outcomes as blocks: the width is how many people exist, the height how well each life goes. "
            "<bookmark mark='b'/>In A, ten people live at level ten. In B, twenty people live at level six. "
            "<bookmark mark='c'/>B contains more good in total, and less per person. Which is better? "
            "<bookmark mark='d'/>For choices among outcomes with the same people, the theories of Part 35 apply. For "
            "choices that change who exists, which every policy on families, health and climate does, we need "
            "something new."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(GrowFromEdge(a, DOWN), FadeIn(la))
            self.play(GrowFromEdge(b, DOWN), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def formulas(self):
        head = label(r"Four axiologies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        fs = VGroup(MathTex(r"\text{total: } \; V = \sum_i w_i", font_size=32, color=WELL),
                    MathTex(r"\text{average: } \; V = \frac{1}{N}\sum_i w_i", font_size=32, color=POP),
                    MathTex(r"\text{critical level: } \; V = \sum_i (w_i - c)", font_size=32, color=RISK),
                    MathTex(r"\text{variable value: } \; V = g(N)\,\bar w, \;\; g \text{ increasing, bounded}",
                            font_size=32, color=FUT)).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-2.4, 0.1, 0])
        side = stack([(r"Sidgwick \ (1874): \ more happy lives are better, \ other things equal", WELL),
                      (r"only how well lives go on average matters, \ not how many there are", POP),
                      (r"Blackorby, \ Bossert and Donaldson: \ a life below $c$ makes things worse, \ though worth "
                       r"living", RISK),
                      (r"Hurka \ (1983); \ Ng \ (1989): \ numbers matter, \ but less and less", FUT)],
                     font_size=18, aligned_edge=LEFT, width=4.8, buff=0.5).move_to([4.3, 0.1, 0])
        for f, t in zip(fs, side):
            t.match_y(f)
        foot = label(r"$w_i$: \ the welfare of person $i$; \ $N$: \ how many exist; \ 0: \ a life just worth living",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here are the main answers, each a formula. Let w sub i be the welfare of person i, with zero the level "
            "of a life just worth living, and N the number of people. <bookmark mark='a'/>The total view adds up "
            "welfare. Henry Sidgwick saw in 1874 that it implies more happy lives are better, other things equal. "
            "<bookmark mark='b'/>The average view divides by N: only how well lives go on average matters, not how "
            "many there are. <bookmark mark='c'/>Critical-level views, developed by Charles Blackorby, Walter Bossert "
            "and David Donaldson, subtract a positive level c from each life, so that adding a life worth living, "
            "but below c, makes things worse. <bookmark mark='d'/>And variable-value views, proposed by Thomas Hurka "
            "in 1983 and Yew-Kwang Ng in 1989, multiply the average by a function of numbers that grows but is "
            "bounded: more people add value, but less and less."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, f, s in zip("abcd", fs, side):
                vo.wait_until(mk)
                self.play(FadeIn(f), FadeIn(s))
        self.clear_scene()

    def scored(self):
        d = load("sequence")
        rows = d["rows"]
        head = label(r"Parfit's sequence, \ scored", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["best"] == {"total": "Z", "average": "A", "critical level": "D", "variable value": "E",
                             "prioritarian": "Z"} and d["growth"] == 1.1
        assert (rows[-1]["n"], rows[-1]["w"]) == (1024, 0.2533)
        show = [r for r in rows if r["name"] in "ABCDEFG"] + [rows[-1]]
        hd = [r"\text{world}", r"\text{people}", r"\text{each}", r"\text{total}", r"\text{average}",
              r"\text{critical, } c = 2", r"\text{variable value}"]
        keys = ["total", "average", "critical level", "variable value"]
        cols = {"total": WELL, "average": POP, "critical level": RISK, "variable value": FUT}
        cells = []
        for r in show:
            row = [label(r["name"], font_size=17, color=GOAL), label(f"{r['n']}", font_size=17, color=GREY_A),
                   label(f"{r['w']:.2f}", font_size=17, color=GREY_A)]
            for k in keys:
                row.append(label(f"{r[k]:.1f}", font_size=17, color=cols[k] if d["best"][k] == r["name"] else WHITE))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[1.3, 1.4, 1.3, 1.6, 1.6, 2.2, 2.3], cell_h=0.44, font_size=16).move_to(
            [0, -0.15, 0])
        boxes = VGroup()
        for k, j in zip(keys, range(3, 7)):
            i = [r["name"] for r in show].index(d["best"][k])
            boxes.add(SurroundingRectangle(grid.cell[i][j], buff=0.07, color=cols[k], stroke_width=2))
        foot = label(r"each step: \ twice the people, \ 55\% of the welfare, \ 10\% more in total", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner scores Parfit's famous sequence. <bookmark mark='a'/>World A has one unit of population, "
            "say ten billion people, each at welfare one hundred. Each next world has twice the people, each at "
            "fifty five percent of the welfare, so the total rises ten percent a step. After ten steps comes Z: a "
            "thousand and twenty four times the people, each at a quarter of a point, lives barely worth living. "
            "<bookmark mark='b'/>The total view counts every step an improvement, and ranks Z best of all. "
            "<bookmark mark='c'/>The average view ranks A best, and every step a loss. <bookmark mark='d'/>A critical "
            "level of two ranks D best: from there on, more lives below two make things worse. "
            "<bookmark mark='e'/>And variable value, whose weight on numbers grows but is bounded, peaks at E. Four "
            "views, four different best worlds, from the same data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][:3])) for i in range(len(show))], lag_ratio=0.15),
                      FadeIn(foot))
            for mk, j, b in zip("bcde", range(3, 7), boxes):
                vo.wait_until(mk)
                self.play(*[FadeIn(grid.cell[i][j]) for i in range(len(show))])
                self.play(Create(b))
        self.clear_scene()
