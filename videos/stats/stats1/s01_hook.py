from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.bills()
        self.reasoning()
        self.life_table()
        self.question()
        self.objectives()

    # ------------------------------------------------------------------
    def bill_card(self):
        lines = [r"A General Bill of Mortality", r"Christened in all the Parishes", r"Buried",
                 r"Whereof of the Plague", r"Ague and Fever", r"Consumption", r"Convulsion", r"Teeth"]
        body = VGroup(*[Text(t, font="DejaVu Serif", font_size=22 if i else 26, color="#E9DFC8")
                        for i, t in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        body[0].set_x(0)
        box = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.7, corner_radius=0.1,
                               stroke_color="#8C7A55", stroke_width=2, fill_color="#2A2418", fill_opacity=1)
        body.move_to(box)
        tag = note(r"illustrative: the headings of a weekly Bill").next_to(box, DOWN, buff=0.15)
        return VGroup(box, body, tag)

    def bills(self):
        g = load("graunt")
        years, chr_, bur, plg = (np.asarray(g[k]) for k in ("years", "christenings", "burials", "plague"))
        card = self.bill_card().scale(1.25).move_to([-3.3, 0.2, 0])
        hc = history_card(1662, r"John Graunt, haberdasher of London",
                          r"\emph{Natural and Political Observations Made upon the Bills of Mortality}",
                          color=S.MUSEUM, width=5.4, font_size=26).move_to([3.6, 0.6, 0])
        A = axes([1625, 1712], [0, 100_000], x_length=10.6, y_length=4.6, xlabel=r"year",
                 xticks=[1630, 1650, 1670, 1690, 1710], yticks=[0, 25_000, 50_000, 75_000, 100_000],
                 yfmt=lambda v: fmt_int(v), center=[0.4, -0.3, 0])
        ax = A.ax
        cb = curve(ax, years, chr_, BIRTHS, 3)
        cd = curve(ax, years, bur, DEATHS, 3)
        lb = label(r"christenings", font_size=26, color=BIRTHS).next_to(ax.c2p(1700, chr_[-10]), DOWN, buff=0.25)
        ld = label(r"burials", font_size=26, color=DEATHS).next_to(ax.c2p(1690, 26_000), UP, buff=0.1)
        i65 = int(np.flatnonzero(years == 1665)[0])
        spike = Dot(ax.c2p(1665, bur[i65]), color=DEATHS, radius=0.08)
        ann = label(rf"1665: \ {fmt_int(g['burials_1665'])} buried, \ {fmt_int(g['plague_1665'])} of plague",
                    font_size=24, color=DEATHS).next_to(spike, RIGHT, buff=0.2)
        src = historical_tag(r"the London Bills, 1629--1710 (Arbuthnot 1710; Creighton)")
        with self.voiceover(
            "In 1662 a London haberdasher named John Graunt published a short book about lists of the dead. "
            "<bookmark mark='a'/> Every week, the parish clerks of London printed a Bill of Mortality: how many people "
            "were buried, and of what, and how many children were christened. Readers used them especially as "
            "warnings of when the plague was coming. <bookmark mark='b'/> Here are those numbers, year by year, "
            "from 1629 to 1710. Christenings in blue, burials in red. <bookmark mark='c'/> And here is 1665, the "
            f"Great Plague: {money(g['burials_1665'])} burials in one year, {money(g['plague_1665'])} of them from "
            "plague, three years after Graunt's book. Graunt had read decades of these lists, and he asked a "
            "question nobody had asked of them: what do the dead tell us about the living?"
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(card), FadeOut(hc))
            self.play(FadeIn(A), FadeIn(src))
            self.play(Create(cb), Create(cd), run_time=3.0)
            self.play(FadeIn(lb), FadeIn(ld))
            vo.wait_until("c")
            self.play(GrowFromCenter(spike), FadeIn(ann, shift=RIGHT * 0.2))
        self.A, self.cb, self.cd, self.lb, self.ld, self.src = A, cb, cd, lb, ld, src
        self.ann, self.spike = ann, spike

    def reasoning(self):
        g = load("graunt")
        ax = self.A.ax
        years, chr_, bur = (np.asarray(g[k]) for k in ("years", "christenings", "burials"))
        w = years <= g["graunt_last"]
        gap = band(ax, years[w], chr_[w], bur[w], DEATHS, opacity=0.25)
        excess = label(rf"buried $-$ christened: \ about {fmt_int(round(g['excess_window'], -1))} a year",
                       font_size=26, color=DEATHS).move_to(ax.c2p(1688, 62_000))
        excess.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.08)
        # the boys and the girls
        B = axes([1625, 1712], [1.0, 1.2], x_length=10.6, y_length=3.2, xlabel=r"year",
                 xticks=[1630, 1650, 1670, 1690, 1710], yticks=[1.0, 1.1, 1.2], ylabel=r"boys per girl christened",
                 yfmt=lambda v: f"{v:.1f}", center=[0.4, -0.6, 0])
        bx = B.ax
        one = DashedLine(bx.c2p(1625, 1.0), bx.c2p(1712, 1.0), color=GREY_B, stroke_width=2)
        dots = VGroup(*[Dot(bx.c2p(y, r), radius=0.045, color=S.MUSEUM) for y, r in zip(years, g["ratio"])])
        graunt = label(rf"Graunt: \ ``fourteen males to thirteen females'' $= {14 / 13:.3f}$", font_size=26)
        bills = label(rf"the Bills, 1629--1660: \ ${g['ratio_window']:.3f}$", font_size=26, color=S.MUSEUM)
        txt = VGroup(graunt, bills).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Nobody had ever counted London. There was no census, and there wouldn't be one for another hundred and "
            "forty years. But Graunt reasoned from the Bills. <bookmark mark='a'/> In almost every year, more people "
            f"were buried than were christened: in the years he could read, about {money(round(g['excess_window'], -1))} "
            "more each year. <bookmark mark='b'/> And yet London was growing, visibly, street by street. So people "
            "must have been arriving from the countryside, year after year, faster than the city's own deaths "
            "could thin it. A fact about the living, read from a list of the dead. <bookmark mark='c'/> He noticed "
            "something else. In every one of these eighty-two years, more boys were christened than girls. Graunt put "
            "it as fourteen boys for every thirteen girls, a ratio of one point oh seven seven. "
            f"<bookmark mark='d'/> The Bills of his years give {g['ratio_window']:.3f}. <bookmark mark='e'/> "
            "Forty-eight years later John Arbuthnot asked whether a fair coin could produce eighty-two years like that. "
            "His answer was the first significance test, and we'll run it ourselves in Part 10."
        ) as vo:
            self.play(FadeOut(self.ann), FadeOut(self.spike))
            vo.wait_until("a")
            self.play(FadeIn(gap), FadeIn(excess))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(self.A, self.cb, self.cd, self.lb, self.ld, gap, excess)))
            self.play(FadeIn(B), Create(one))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03), run_time=2.5)
            self.play(FadeIn(graunt))
            vo.wait_until("d")
            self.play(FadeIn(bills))
            vo.wait_until("e")
            self.play(Indicate(dots, color=S.ACCENT, scale_factor=1.3))
        self.play(FadeOut(VGroup(B, one, dots, txt, self.src)))

    def life_table(self):
        g = load("graunt")
        ages, alive = g["life_ages"], g["life_alive"]
        grid = VGroup(*[Dot(radius=0.11, color=S.MUSEUM) for _ in range(100)]).arrange_in_grid(10, 10, buff=0.22)
        grid.move_to([-3.6, -0.2, 0])
        title = label(r"Of a hundred conceived \dots", font_size=32).next_to(grid, UP, buff=0.4)
        counter = VGroup(label(r"age", font_size=30, color=GREY_A), MathTex("0", font_size=44),
                         label(r"alive", font_size=30, color=GREY_A), MathTex("100", font_size=44, color=S.MUSEUM))
        counter.arrange(RIGHT, buff=0.25).next_to(grid, DOWN, buff=0.4)
        A = axes([0, 90], [0, 100], x_length=5.4, y_length=4.0, xlabel=r"age", ylabel=r"alive (of 100)",
                 xticks=[0, 16, 36, 56, 76], yticks=[0, 50, 100], center=[3.4, -0.3, 0])
        ax = A.ax
        order = np.random.Generator(np.random.PCG64(3)).permutation(100)
        pts = [ax.c2p(a, n) for a, n in zip(ages, alive)]
        stairs = VMobject(color=S.MUSEUM, stroke_width=4)
        stair_pts = [pts[0]]
        for p0, p1 in zip(pts[:-1], pts[1:]):
            stair_pts += [np.array([p1[0], p0[1], 0]), p1]
        stairs.set_points_as_corners(stair_pts)
        src = historical_tag(r"Graunt (1662), ch.~11")
        with self.voiceover(
            "Graunt went further. He wanted to know how long Londoners lived, and the Bills didn't record ages at "
            "all. So he estimated. <bookmark mark='a'/> The Bills did record deaths from the diseases of infancy: "
            "thrush, convulsions, teeth, rickets. From those he estimated that of every hundred children conceived, "
            "thirty-six died before the age of six. <bookmark mark='b'/> For the rest of life he assumed a steady "
            "loss, decade after decade: sixty-four alive at six, forty at sixteen, twenty-five at twenty-six, sixteen "
            "at thirty-six, and on down to one at seventy-six. <bookmark mark='c'/> It's rough, and the second half "
            "is an assumption, not a measurement. But it's a pioneering life table: an ancestor of every survival "
            "curve in medicine and every insurance premium. Its modern descendant, the Kaplan–Meier curve, "
            "arrives in Part 40."
        ) as vo:
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(title), FadeIn(counter), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(A))
            vo.wait_until("b")
            for k in range(1, len(ages)):
                gone = order[alive[k]:alive[k - 1]]
                new_age = MathTex(str(ages[k]), font_size=44).move_to(counter[1])
                new_alive = MathTex(str(alive[k]), font_size=44, color=S.MUSEUM).move_to(counter[3])
                seg = VMobject(color=S.MUSEUM, stroke_width=4).set_points_as_corners(
                    [pts[k - 1], np.array([pts[k][0], pts[k - 1][1], 0]), pts[k]])
                self.play(*[grid[i].animate.set_color(GREY_D).scale(0.6) for i in gone],
                          Transform(counter[1], new_age), Transform(counter[3], new_alive), Create(seg),
                          run_time=0.9 if k < 4 else 0.6)
            vo.wait_until("c")
            self.play(Indicate(A, color=S.MUSEUM, scale_factor=1.03))
        self.clear_scene()

    def question(self):
        q1 = label(r"What can we know about what we cannot see,", font_size=44)
        q2 = label(r"from what we can?", font_size=44)
        q3 = label(r"And how often will we be wrong?", font_size=44, color=S.ACCENT)
        qs = VGroup(q1, q2, q3).arrange(DOWN, buff=0.35)
        smap = series_map(current=1, done=0, font_size=17)
        with self.voiceover(
            "That leap, from what was written down to what was never counted, is the whole subject. "
            "<bookmark mark='a'/> What can we know about what we cannot see, from what we can? "
            "<bookmark mark='b'/> And the half that turns it into a science: how often will we be wrong? "
            "<bookmark mark='c'/> This series is an education in that question, from a first course to a PhD, in "
            "sixty-five parts. <bookmark mark='d'/> The first two stages are a bachelor's degree: data, probability, "
            "estimation, testing, and the everyday methods, from regression to surveys. <bookmark mark='e'/> The "
            "third is a master's: the modern toolkit, from mixed models and Bayesian computation to causal "
            "inference. <bookmark mark='f'/> The fourth is the theory a PhD student is examined on, and the fifth "
            "is research, ending with a dissertation. <bookmark mark='g'/> We start where Graunt started: with data, "
            "and the shapes it makes."
        ) as vo:
            self.play(FadeIn(q1, shift=UP * 0.2), FadeIn(q2, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q1, color=WHITE, scale_factor=1.05), Indicate(q2, color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(q3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(qs), FadeIn(smap))
            for mark, cols in (("d", (0, 1)), ("e", (2,)), ("f", (3, 4))):
                vo.wait_until(mark)
                self.play(*[Indicate(smap.cols[c].head, color=S.ACCENT, scale_factor=1.15) for c in cols])
            vo.wait_until("g")
            self.play(Indicate(smap.part[1], color=S.ACCENT, scale_factor=1.4))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 1", font_size=34, color=GREY_B), label(r"The Shape of Data", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"populations and samples; \ the World, a population whose truth we know",
            r"histograms, \ and the centre and spread of data as answers to optimization problems",
            r"quantiles and box plots; \ skew, heavy tails and power laws; \ QQ plots and transformations",
            r"correlation as the cosine of an angle",
            r"how the same summaries hide different pictures, \ and how aggregation reverses conclusions",
            r"honest graphics; \ and the discovery that every summary is itself random",
        ], color=S.ACCENT, font_size=26)
        with self.voiceover(
            "Part one: the shape of data. <bookmark mark='a'/> In this part: what a population and a sample are, "
            "and a world we'll build so that we always know the truth. Histograms, and the centre and spread of "
            "data, which turn out to be answers to optimization problems. Quantiles and box plots; skew, heavy "
            "tails and power laws; QQ plots and transformations. Correlation, seen as an angle. How the same "
            "summary statistics can hide completely different pictures, and how combining groups can reverse a "
            "conclusion. Honest graphics. And at the end, the discovery that makes the rest of the series "
            "necessary: every summary we compute is itself random."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2))
        self.clear_scene()
