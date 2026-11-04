from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403

DEPTS = "ABCDEF"


class Simpson(VoiceoverScene):
    def construct(self):
        self.card()
        self.by_department()
        self.where_applied()
        self.mosaics()
        self.weights()
        self.meaning()

    def card(self):
        card = chapter_card(8, r"Simpson's paradox", r"Every part one way, \ the whole the other", lit=(1975,), part=PART)
        with self.voiceover("Chapter eight. Simpson's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def by_department(self):
        d = load("tables")["depts"]
        A = axes([-0.6, 5.6], [0, 1], x_length=8.4, y_length=4.2, xlabel=r"department", ylabel=r"admitted", xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1],
                 center=[-1.8, 0.4, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        w = ax.c2p(0.34, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        names = VGroup()
        for k, dep in enumerate(DEPTS):
            for off, key, col in ((-0.19, "men", MEN), (0.19, "women", WOMEN)):
                v = d[dep][key]
                bars.add(Rectangle(width=w, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to(ax.c2p(k + off, 0), aligned_edge=DOWN))
            names.add(label(dep, font_size=24, color=GREY_B).move_to(ax.c2p(k, 0) + DOWN * 0.3))
        key = VGroup(label(r"men", font_size=24, color=MEN), label(r"women", font_size=24, color=WOMEN)).arrange(RIGHT, buff=0.5).next_to(A, UP, buff=0.1)
        rows = fit_rows(VGroup(
            label(r"department by department", font_size=24),
            label(r"A: \ women 82\%, \ men 62\%", font_size=24, color=WOMEN),
            label(r"women ahead in 4 of 6", font_size=24, color=OBS),
            label(r"the gaps in C and E are small", font_size=22, color=GREY_A),
        ), 3.8, 0.36, [5.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Admissions at Berkeley were decided by each department, so break the table down by "
            "department. <bookmark mark='b'/> In department A, eighty-two percent of women were admitted and sixty-two percent of "
            "men. <bookmark mark='c'/> In B, D and F, women also did as well as or better than men. <bookmark mark='d'/> In C and "
            "E, men were slightly ahead, by a few points. Department by department, there's no sign of the fourteen-point gap "
            "against women. If anything, it points the other way."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def where_applied(self):
        d = load("tables")["depts"]
        tm = sum(d[k]["n_men"] for k in DEPTS)
        tw = sum(d[k]["n_women"] for k in DEPTS)
        A = axes([-0.6, 5.6], [0, 0.4], x_length=8.4, y_length=3.8, xlabel=r"department \ (sorted by admission rate)", ylabel=r"share of applicants",
                 xticks=[], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-1.8, 0.4, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        w = ax.c2p(0.34, 0)[0] - ax.c2p(0, 0)[0]
        bars, names = VGroup(), VGroup()
        for k, dep in enumerate(DEPTS):
            for off, key, tot, col in ((-0.19, "n_men", tm, MEN), (0.19, "n_women", tw, WOMEN)):
                v = d[dep][key] / tot
                bars.add(Rectangle(width=w, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to(ax.c2p(k + off, 0), aligned_edge=DOWN))
            rate = (d[dep]["men"] * d[dep]["n_men"] + d[dep]["women"] * d[dep]["n_women"]) / (d[dep]["n_men"] + d[dep]["n_women"])
            names.add(label(rf"{dep}: \ {100 * rate:.0f}\%", font_size=20, color=GREY_B).move_to(ax.c2p(k, 0) + DOWN * 0.3))
        rows = fit_rows(VGroup(
            label(r"where did each sex apply?", font_size=24),
            label(r"men: \ mostly A and B, \ easy to enter", font_size=24, color=MEN),
            label(r"women: \ mostly C to F, \ hard to enter", font_size=24, color=WOMEN),
            label(r"F admitted 6\% of everyone", font_size=22, color=GREY_A),
        ), 3.8, 0.36, [5.0, 0.4, 0])
        with self.voiceover(
            "So where does the gap come from? <bookmark mark='a'/> Look at where each sex applied, with the departments "
            "ordered by their overall admission rate. <bookmark mark='b'/> More than half of the men applied to A and B, which "
            "admitted most of their applicants. <bookmark mark='c'/> Most women applied to C, D, E and F, which admitted few "
            "of anyone. <bookmark mark='d'/> Department F admitted six percent of its applicants, men and women alike. Women "
            "were concentrated in the departments that were hardest to enter."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def mosaics(self):
        B = museum.BERKELEY
        men = [(v[0], v[1]) for v in B.values()]
        wom = [(v[2], v[3]) for v in B.values()]
        m1 = mosaic(men, [-3.4, 0.3, 0], width=5.6, height=3.6, colors=(MEN, "#1B2733"), labels=list(DEPTS))
        m2 = mosaic(wom, [3.4, 0.3, 0], width=5.6, height=3.6, colors=(WOMEN, "#1B2733"), labels=list(DEPTS))
        h1 = label(r"men's applications", font_size=24, color=MEN).next_to(m1, UP, buff=0.2)
        h2 = label(r"women's applications", font_size=24, color=WOMEN).next_to(m2, UP, buff=0.2)
        foot = fit_rows(VGroup(
            label(r"column width: \ how many applied; \ coloured height: \ the share admitted", font_size=22, color=GREY_A),
            label(r"the same heights, \ department by department; \ different widths", font_size=24, color=OBS),
        ), 12.4, 0.22, [0, -2.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A mosaic plot shows it all at once. Each column is a department; its width is the number of "
            "applications, and the coloured part is the share admitted. Men on the left, women on the right. "
            "<bookmark mark='b'/> The coloured heights match closely, department by department: admission didn't depend much "
            "on sex. What differs is the widths. The men's picture is dominated by the wide, mostly coloured columns A and B; the "
            "women's by the wide, mostly dark columns C to F."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(m1, lag_ratio=0.1), FadeIn(h1), run_time=2.0)
            self.play(FadeIn(m2, lag_ratio=0.1), FadeIn(h2), FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def weights(self):
        d = load("tables")
        rows = [
            cmath(r"p_{\text{men}}", r"=", r"\sum_k w^{\text{men}}_k\, p^{\text{men}}_k", font_size=34),
            cmath(r"p_{\text{women}}", r"=", r"\sum_k w^{\text{women}}_k\, p^{\text{women}}_k", font_size=34),
            cmath(r"w^{\text{men}}", r"\ne", r"w^{\text{women}}", font_size=34),
            cmath(r"\text{so}", r":", rf"{100 * d['men_rate']:.1f}\%\ \text{{vs}}\ {100 * d['women_rate']:.1f}\%\ \text{{while}}\ p^{{\text{{women}}}}_k \gtrsim p^{{\text{{men}}}}_k", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"a weighted average of the department rates"), why(r"the same, \ with women's weights"),
                why(r"the weights are where each sex applied"), why(r"Simpson (1951); \ Yule (1903)")]
        with self.voiceover(
            "The arithmetic is simple. <bookmark mark='a'/> The men's overall admission rate is a weighted average of the "
            "department rates, weighted by where the men applied. <bookmark mark='b'/> The women's is a weighted average of "
            "theirs, weighted by where the women applied. <bookmark mark='c'/> The weights differ. <bookmark mark='d'/> So the "
            "averages can differ by fourteen points in one direction while the rates, department by department, lean the other "
            "way. Edward Simpson described the reversal in 1951; George Udny Yule had noticed it in 1903. Part 1 met it in the "
            "World's clinic, and Part 12 as omitted-variable bias."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"Bickel, \ Hammel \& O'Connell: \ the admissions committees showed no bias against women", font_size=24),
            label(r"the gap came from where women applied: \ crowded fields with few places", font_size=24, color=WOMEN),
            label(r"which raises its own questions, \ about earlier choices and funding", font_size=24, color=GREY_A),
            label(r"the right comparison depends on the question: \ the department is part of the story", font_size=24, color=OBS),
            label(r"causal diagrams decide which table to read \ (Parts 35--36)", font_size=22, color=GREY_A),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bickel, Hammel and O'Connell concluded that the admissions committees, taken together, showed "
            "no bias against women; if anything, a small bias in their favour. <bookmark mark='b'/> The aggregate gap arose "
            "because women applied in larger numbers to departments that were crowded and had few places. <bookmark mark='c'/> "
            "That raises its own questions, about the earlier choices and the funding that shaped those applications, but they "
            "aren't questions about the committees. <bookmark mark='d'/> Which table is right depends on the question being "
            "asked. <bookmark mark='e'/> Deciding which variables to condition on is a causal question, and Parts 35 and 36 "
            "give the tools, diagrams among them, for answering it."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
