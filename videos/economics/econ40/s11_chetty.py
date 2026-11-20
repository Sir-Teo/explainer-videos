from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Chetty(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Forty million tax records", r"How likely is a child to rise, \ and is it getting harder?",
             "Chapter nine. Forty million tax records.", lit={2014: r"Chetty, \ Hendren, \ Kline and Saez",
                                                              2017: r"Chetty et al."},
             scale=("household", "nation"), horizon=("a century",))
        self.rankrank()
        self.matrix()
        self.absolute()
        self.why()

    def rankrank(self):
        C = load("chetty")
        r = np.array(C["rank"])
        ax = plane([0, 100], [20, 75], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[20, 30, 40, 50, 60, 70],
                   xlabel=r"parents' income rank", ylabel=r"children's mean income rank, \ at 31--32",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[dot(ax, k + 0.5, 100 * v, CHILD, 0.05) for k, v in enumerate(r)])
        fit = seg(ax, 0, 100 * C["intercept"], 100, 100 * (C["intercept"] + C["slope"]), WHITE, 3)
        flat = seg(ax, 0, 50, 100, 50, GREY_D, 1.5, dashed=True)
        side = VGroup(
            label(r"children born 1980--82, \\ ranked among their \\ own generation", font_size=17, color=GREY_A),
            label(rf"slope: \ {C['slope']:.3f}", font_size=22, color=WHITE),
            label(r"10 percentiles richer \\ parents: \ the child is \\ 3.4 percentiles higher", font_size=18,
                  color=CHILD),
            label(r"grey: \ if parents \\ did not matter", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(tables.CHETTY_2014.tag + r"; \ Opportunity Insights", corner=DR, font_size=10)
        with self.voiceover(
            "In 2014 Raj Chetty, Nathaniel Hendren, Patrick Kline and Emmanuel Saez linked the tax records of more "
            "than forty million American children to their parents'. Instead of logs, they used ranks: each child's "
            "place in the income distribution of their own generation, against the parents' place in theirs. "
            "<bookmark mark='a'/> Here are children born from 1980 to 1982, grouped by their parents' percentile. "
            "<bookmark mark='b'/> The relation is a straight line, with a slope of "
            f"{C['slope']:.3f}: <bookmark mark='c'/> ten percentiles richer parents, three and a half percentiles "
            "higher children. <bookmark mark='d'/> If parents did not matter, the line would be flat at fifty. Ranks "
            "do not suffer from zero incomes, or from the very top, the way logs do, which is why the rank slope is "
            "now the standard measure."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(pts, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(pts, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(flat), FadeIn(side[3]))
        self.clear_scene()

    def matrix(self):
        C = load("chetty")
        Q = np.array(C["quint"])
        cells = VGroup()
        size = 1.05
        x0, y0 = -3.6, 1.9
        for i in range(5):
            for j in range(5):
                v = Q[i, j]
                col = interpolate_color(ManimColor("#141821"), ManimColor(CHILD), min(v / 0.4, 1.0))
                sq = Square(side_length=size, stroke_color=GREY_D, stroke_width=1, fill_color=col,
                            fill_opacity=1).move_to(np.array([x0 + j * size, y0 - i * size, 0]))
                t = label(f"{100 * v:.1f}", font_size=19, color=WHITE).move_to(sq)
                cells.add(VGroup(sq, t))
        rows = VGroup(*[label(nm, font_size=17, color=PARENT).next_to(cells[5 * i][0], LEFT, buff=0.15)
                        for i, nm in enumerate((r"bottom", r"second", r"middle", r"fourth", r"top"))])
        cols = VGroup(*[label(nm, font_size=17, color=CHILD).next_to(cells[j][0], UP, buff=0.12)
                        for j, nm in enumerate((r"bottom", r"2nd", r"middle", r"4th", r"top"))])
        hr = label(r"parents' fifth", font_size=18, color=PARENT).next_to(rows, LEFT, buff=0.2).rotate(PI / 2)
        hc = label(r"the child's fifth, \ as an adult \ (percent of each row)", font_size=18,
                   color=CHILD).next_to(cols, UP, buff=0.15)
        q51 = SurroundingRectangle(cells[4], color=E.ACCENT, buff=0.02, stroke_width=4)
        side = VGroup(
            label(rf"bottom to top: \ {100 * C['q5q1']:.1f}\%", font_size=20, color=E.ACCENT),
            label(rf"stay at the bottom: \ {100 * C['q1q1']:.1f}\%", font_size=20, color=PARENT),
            label(rf"stay at the top: \ {100 * C['q5q5']:.1f}\%", font_size=20, color=CHILD),
            label(r"with no link, \\ every cell would be 20", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = data_tag(r"Opportunity Insights: \ the 100 $\times$ 100 transition matrix, \ summed by fifths",
                       corner=DR, font_size=11)
        with self.voiceover(
            "Summing their transition matrix by fifths gives the chances behind the line. Each row is a group of "
            "parents; each cell, the percent of their children who end up in each fifth. <bookmark mark='a'/> A "
            f"child born to the bottom fifth reaches the top fifth with probability {100 * C['q5q1']:.1f} percent: "
            "the third answer of the game. <bookmark mark='b'/> A third of those children stay in the bottom fifth. "
            f"<bookmark mark='c'/> And {100 * C['q5q5']:.0f} percent of the children of the top fifth stay there. "
            "<bookmark mark='d'/> If parents' incomes did not matter, every cell would read twenty."
        ) as vo:
            self.play(FadeIn(cells, lag_ratio=0.03), FadeIn(rows), FadeIn(cols), FadeIn(hr), FadeIn(hc),
                      FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(q51), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Indicate(cells[0], color=WHITE), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(cells[24], color=WHITE), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def absolute(self):
        C = load("chetty")
        ax = plane([1938, 1986], [0.4, 1.0], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[1940, 1950, 1960, 1970, 1980], yticks=[0.4, 0.6, 0.8, 1.0],
                   xlabel=r"the child's birth year", ylabel=r"share earning more than their parents",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        ln = path(ax, C["cohorts"], C["absmob"], MIDDLE, 3.4, smooth=False)
        bx = plane([0, 100], [0, 1.0], center=RIGHT * 3.2 + DOWN * 0.3, x_length=5.4, y_length=4.4,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"parents' income percentile", ylabel=r"", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        pk = np.arange(1, 101)
        l40 = path(bx, pk, C["by1940"], TOP, 3.0)
        l84 = path(bx, pk, C["by1984"], LOSS, 3.0)
        keys = VGroup(label(r"born 1940", font_size=17, color=TOP), label(r"born 1984", font_size=17, color=LOSS)
                      ).arrange(RIGHT, buff=0.4).next_to(bx, UP, buff=0.15)
        ends = VGroup(label(rf"{100 * C['absmob'][0]:.0f}\%", font_size=19, color=MIDDLE).next_to(
            ax.ax.c2p(C["cohorts"][0], C["absmob"][0]), UP, buff=0.12),
            label(rf"{100 * C['absmob'][-1]:.0f}\%", font_size=19, color=MIDDLE).next_to(
            ax.ax.c2p(C["cohorts"][-1], C["absmob"][-1]), DOWN, buff=0.12))
        tag = data_tag(tables.CHETTY_2017.tag + r"; \ Opportunity Insights", corner=DR, font_size=11)
        with self.voiceover(
            "Relative mobility asks who climbs past whom. Absolute mobility asks something plainer: do children "
            "earn more than their parents did at the same age, after inflation? <bookmark mark='a'/> In 2017 "
            "Chetty and five coauthors traced it by birth year. For children born in 1940, "
            f"{100 * C['absmob'][0]:.0f} percent out-earned their parents. <bookmark mark='b'/> For those born in "
            f"1984, {100 * C['absmob'][-1]:.0f} percent: a coin toss. <bookmark mark='c'/> By parents' percentile: "
            f"over ninety percent of the 1940 cohort out-earned their parents at almost every level, and "
            f"{100 * C['by1940'][89]:.0f} percent even at the ninetieth percentile. <bookmark mark='d'/> For the 1984 "
            "cohort the line has fallen everywhere, and further the richer the parents."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(ends[0], scale=1.3))
            vo.wait_until("b")
            self.play(FadeIn(ends[1]))
            vo.wait_until("c")
            self.play(FadeIn(bx), FadeIn(keys[0]), Create(l40), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(keys[1]), Create(l84), run_time=1.5)
        self.clear_scene()

    def why(self):
        D_ = tables.CHETTY_2017.data
        C = load("chetty")
        rows = [(r"children born in 1980: \ actual", 100 * C["absmob"][C["cohorts"].index(1980)], GREY_B),
                (r"with the growth of the 1940s and 50s, \\ shared as it is now", D_["growth_only"], TOP),
                (r"with today's growth, \\ shared as it was for the 1940 cohort", D_["sharing_only"], GAIN),
                (r"children born in 1940: \ actual", 100 * C["absmob"][0], GREY_B)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.6 - 1.15 * k
            r = Rectangle(width=v * 0.06, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([0.3 + v * 0.03, y, 0]))
            bars.add(VGroup(label(nm, font_size=18, color=WHITE).next_to(np.array([0.15, y, 0]), LEFT, buff=0.15),
                            r, label(f"{v:.0f}\\%", font_size=20, color=col).next_to(r, RIGHT, buff=0.15)))
        head = label(r"why the fall? \ Not mainly slower growth", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.CHETTY_2017.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Why the fall? Two things changed: the economy grew more slowly, and its growth went increasingly to "
            "the top. The authors separate them. <bookmark mark='a'/> For children born in 1980, absolute mobility "
            f"was {rows[0][1]:.0f} percent. <bookmark mark='b'/> Restore the faster growth of the 1940s and 1950s, "
            f"but share it as it is shared now, and it rises only to {D_['growth_only']} percent. "
            "<bookmark mark='c'/> Keep today's slower growth, but share it as it was shared for the 1940 cohort, and "
            f"it rises to {D_['sharing_only']} percent. <bookmark mark='d'/> Most of the fading American dream is the "
            "distribution of growth, not its rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bars[3]))
            for mk, b_ in zip("abc", bars[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(Indicate(bars[2], color=WHITE, scale_factor=1.02))
        self.clear_scene()
