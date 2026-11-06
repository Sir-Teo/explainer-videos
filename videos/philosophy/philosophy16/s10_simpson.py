from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403

MEN, WOMEN = "#6FB7FF", "#F28EC2"


def node(t, c, pos):
    circ = Circle(radius=0.42, color=c, stroke_width=3).move_to(pos)
    return VGroup(circ, label(t, font_size=19, color=c).move_to(pos))


def arrow(a, b, c=GREY_B):
    return Arrow(a[0].get_center(), b[0].get_center(), buff=0.45, color=c, stroke_width=3,
                 max_tip_length_to_length_ratio=0.15)


class Simpson(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Simpson's paradox", r"Can every part reverse the whole?", lit=(1951,), part=PART)
        with self.voiceover("Chapter nine. Simpson's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.aggregate()
        self.departments()
        self.covid()
        self.causal()

    def aggregate(self):
        d = load("simpson")
        head = label(r"Berkeley graduate admissions, \ fall 1973", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        sub = label(r"the six largest departments \ (Bickel, \ Hammel and O'Connell, \ 1975)", font_size=21,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        base = Line([-3.0, -2.5, 0], [3.0, -2.5, 0], color=GREY_C, stroke_width=2)
        bars = VGroup()
        for i, (who, rate, n, c) in enumerate(((r"men", d["men_rate"], d["men"], MEN),
                                               (r"women", d["women_rate"], d["women"], WOMEN))):
            b = Rectangle(width=1.8, height=rate * 8, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-1.4 + 2.8 * i, -2.5 + b.height / 2, 0])
            v = label(rf"{100 * rate:.0f}\% \ admitted", font_size=24, color=c).next_to(b, UP, buff=0.12)
            t = label(who + r" \ (" + f"{n:,}".replace(",", "{,}") + r" applicants)", font_size=20,
                      color=GREY_A).next_to(b, DOWN, buff=0.15)
            bars.add(VGroup(b, v, t))
        foot = label(r"a lawsuit seemed likely", font_size=22, color=BAD).to_edge(DOWN, buff=0.25).shift(RIGHT * 4)
        with self.voiceover(
            "In 1973 the graduate division of the University of California at Berkeley looked at its admissions. "
            "<bookmark mark='a'/>In its six largest departments, forty-five percent of men who applied were "
            "admitted. <bookmark mark='b'/>Only thirty percent of women were. <bookmark mark='c'/>The gap was large, "
            "the numbers were thousands, and a lawsuit seemed likely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(base))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def departments(self):
        d = load("simpson")
        head = label(r"Department by department", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        g = VGroup()
        for i, r in enumerate(rows):
            y = 1.9 - i * 0.78
            dl = label(r["dept"], font_size=24, color=WHITE).move_to([-6.2, y, 0])
            bm = Rectangle(width=r["men_rate"] * 5, height=0.22, stroke_width=0, fill_color=MEN,
                           fill_opacity=0.85).move_to([-5.7 + r["men_rate"] * 2.5, y + 0.14, 0])
            bw = Rectangle(width=r["women_rate"] * 5, height=0.22, stroke_width=0, fill_color=WOMEN,
                           fill_opacity=0.85).move_to([-5.7 + r["women_rate"] * 2.5, y - 0.14, 0])
            tm = label(rf"{100 * r['men_rate']:.0f}\%", font_size=16, color=MEN).next_to(bm, RIGHT, buff=0.08)
            tw = label(rf"{100 * r['women_rate']:.0f}\%", font_size=16, color=WOMEN).next_to(bw, RIGHT, buff=0.08)
            share_w = r["women"] / (r["men"] + r["women"])
            app = label(r"applicants: \ " + str(r["men"]) + r" men, \ " + str(r["women"]) + r" women", font_size=17,
                        color=GREY_B).move_to([2.0, y, 0])
            mk = label(r"women higher" if r["women_higher"] else r"men higher", font_size=17,
                       color=OK if r["women_higher"] else GREY_B).move_to([5.2, y, 0])
            g.add(VGroup(dl, bm, bw, tm, tw, app, mk))
            g[-1].share = share_w
        foot = stack([(r"women did better in " + str(d["depts_women_higher"]) + r" of 6 departments", OK),
                      (r"they applied more to the departments that admitted few of anyone", GOAL)], font_size=22).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Peter Bickel, Eugene Hammel and William O'Connell looked department by department. "
            "<bookmark mark='a'/>In department A, women were admitted at eighty-two percent, men at sixty-two. "
            "<bookmark mark='b'/>In B, C, D, E and F the rates were close, and women came out ahead in three of them. "
            "<bookmark mark='c'/>Women did better in four of the six departments. <bookmark mark='d'/>The reversal "
            "comes from where people applied. More than half the men applied to A and B, which admitted most "
            "applicants. Almost all the women applied to C through F, which admitted few applicants of either sex. "
            "Aggregating mixes the "
            "departments in different proportions for the two groups. This is Simpson's paradox, described by "
            "Edward Simpson in 1951, and earlier by Yule and Pearson."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[1:]], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(*[Indicate(r[5], color=WOMEN, scale_factor=1.05) for r in g if r.share > 0.5], FadeIn(foot[1]))
        self.clear_scene()

    def covid(self):
        head = label(r"The same pattern, \ in a pandemic", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"early 2020", r"a larger share of confirmed cases died in Italy than in China", BAD),
            (r"by age", r"in every age group, \ a \textit{smaller} share died in Italy", OK),
            (r"why", r"Italy's confirmed cases were much older: \ age drives both who is a case and who dies", GOAL),
            (r"source", r"von Kügelgen, \ Gresele and Schölkopf \ (2021), \ from the national reports", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.6, width=8.6, x_text=-2.6, label_size=23, text_size=22)
        foot = label(r"a reversal needs only unequal mixing: \ it is arithmetic, \ not a curiosity", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The pattern is not a curiosity of one university. <bookmark mark='a'/>Early in the COVID-19 pandemic, "
            "a larger share of confirmed cases died in Italy than in China. <bookmark mark='b'/>Yet within every age "
            "group, a smaller share died in Italy. <bookmark mark='c'/>Italy's confirmed cases were much older, and "
            "age drives both who becomes a confirmed case and who dies. <bookmark mark='d'/>Julius von Kügelgen, "
            "Luigi Gresele and Bernhard Schölkopf documented the reversal from the national reports. "
            "<bookmark mark='e'/>A reversal needs nothing more than groups mixed in unequal proportions. It is "
            "arithmetic, and it is everywhere."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def causal(self):
        head = label(r"Which table is the right one? \ The data cannot say", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        lpos = [np.array([-5.4, 0.6, 0]), np.array([-3.4, 1.8, 0]), np.array([-1.4, 0.6, 0])]
        g1, d1, a1 = node(r"sex", WOMEN, lpos[0]), node(r"dept", FISH, lpos[1]), node(r"admit", OK, lpos[2])
        left = VGroup(g1, d1, a1, arrow(g1, d1), arrow(d1, a1), arrow(g1, a1, BAD))
        lt = label(r"department is a \textit{mediator}:", font_size=20, color=FISH).next_to(left, DOWN, buff=0.3)
        ll = label(r"for discrimination \textit{by departments}, \ condition on it", font_size=19,
                   color=GREY_A).next_to(lt, DOWN, buff=0.1)
        rpos = [np.array([1.8, 0.6, 0]), np.array([3.8, 1.8, 0]), np.array([5.8, 0.6, 0])]
        t2, b2, r2 = node(r"drug", ALTC, rpos[0]), node(r"BP", FISH, rpos[1]), node(r"recover", OK, rpos[2])
        right = VGroup(t2, b2, r2, arrow(t2, b2), arrow(b2, r2), arrow(t2, r2))
        rt = label(r"a drug works \textit{through} blood pressure:", font_size=20, color=FISH).next_to(right, DOWN,
                                                                                                    buff=0.3)
        rl = label(r"for the drug's total effect, \ do \textit{not} condition", font_size=19,
                   color=GREY_A).next_to(rt, DOWN, buff=0.1)
        foot = stack([(r"the same numbers, \ two causal stories, \ two right answers", GOAL),
                      (r"`no causes in, \ no causes out' \ (Cartwright); \ Pearl's graphs decide: \ Part 17", WHITE)],
                     font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So which table answers the question, the aggregate or the departments? Judea Pearl's answer is that "
            "the numbers alone cannot say. <bookmark mark='a'/>At Berkeley, sex influences which department one "
            "applies to, and the department influences admission. To ask whether departments discriminate, "
            "condition on the department, as Bickel did. <bookmark mark='b'/>Now take numbers with exactly the "
            "same pattern, about a drug that works by lowering blood pressure. Blood pressure is on the causal path. "
            "To ask whether the drug helps, you must not condition on it, and the aggregate table is the right one. "
            "<bookmark mark='c'/>The same numbers, two causal stories, two different right answers. As Nancy "
            "Cartwright put it, no causes in, no causes out. Part 17 builds the graphs that decide."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(lt), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rt), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()
