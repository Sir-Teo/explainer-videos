from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class World(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The world's distribution", r"Has the world become more or less unequal?",
             "Chapter eleven. The world's distribution.", lit={2016: r"Lakner and Milanovic"},
             scale=("world",), horizon=("a decade", "a century"))
        self.between()
        self.elephant()
        self.top()

    def between(self):
        W = load("world")
        ys = W["years"]
        ax = plane([1978, 2025], [0.4, 0.7], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0.4, 0.5, 0.6, 0.7],
                   ylabel=r"Gini of countries' GDP per person, \ weighted by population", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        la = path(ax, ys, W["all"], TOP, 3.4, smooth=False)
        lc = path(ax, ys, W["no_china"], LOSS, 2.8, smooth=False)
        li = path(ax, ys, W["no_china_india"], GREY_B, 2.8, smooth=False)
        C, I_ = W["CHN"], W["IND"]
        side = VGroup(
            label(rf"gold: \ {W['n']} countries, \\ {100 * W['pop_share']:.0f}\% of the people: \\ "
                  rf"{W['all'][0]:.2f} $\to$ {W['all'][-1]:.2f}", font_size=18, color=TOP),
            label(rf"red: \ without China: \\ {W['no_china'][0]:.2f} $\to$ {W['no_china'][-1]:.2f}", font_size=18,
                  color=LOSS),
            label(rf"grey: \ without China \\ and India: \ {W['no_china_india'][0]:.2f} $\to$ "
                  rf"{W['no_china_india'][-1]:.2f}", font_size=18, color=GREY_B),
            label(rf"China: \ GDP per person \\ $\times${C['y2023'] / C['y1980']:.0f} since 1980; \\ India "
                  rf"$\times${I_['y2023'] / I_['y1980']:.0f}", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Penn World Table 11.0; \ computed", corner=DR, font_size=12)
        with self.voiceover(
            "Step back to the whole world. The largest part of global inequality is between countries: where you "
            "are born. <bookmark mark='a'/> Treat everyone as earning their country's average, and compute a Gini "
            f"across the world's people. It was {W['all'][0]:.2f} in 1980, and {W['all'][-1]:.2f} in 2023: a large "
            "fall. <bookmark mark='b'/> Take China out, and most of the fall disappears. <bookmark mark='c'/> Take "
            "out India as well, and inequality between the remaining countries did not fall at all. "
            f"<bookmark mark='d'/> Since 1980 China's output per person has grown about "
            f"{C['y2023'] / C['y1980']:.0f}-fold, India's {I_['y2023'] / I_['y1980']:.0f}-fold. Two countries with "
            "a third of humanity moved from the bottom of the world's distribution towards its middle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(li), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def elephant(self):
        G = tables.GLOBAL.data
        cards = point_cards([
            (r"around the global median", r"the largest gains: \\ mostly the new \\ middle classes of Asia", GAIN),
            (rf"the {G['stagnant_lo']}th to {G['stagnant_hi']}th percentiles", r"essentially no gain: \\ largely the "
             r"lower middle \\ classes of rich countries", LOSS),
            (r"the top 1\%", r"large gains: \\ the global rich", TOP),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.3)
        head = label(rf"real income growth by global percentile, \ {G['first']}--{G['last']}: \ the elephant curve",
                     font_size=26, color=E.ACCENT).to_edge(UP, buff=0.5)
        sub = label(r"each person ranked in one world distribution, \ household surveys from most of the world",
                    font_size=18, color=GREY_A).next_to(head, DOWN, buff=0.2)
        foot = label(r"not the same people at each percentile in both years: \ a comparison of positions",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.GLOBAL.tag, corner=DR, font_size=11)
        steps = flow_chain([(r"household \\ surveys", BOTTOM), (r"one world \\ ranking", MIDDLE),
                            (r"growth at each \\ percentile", TOP)],
                           notes=[r"about 1988 \\ and 2008", r"everyone, \\ in dollars of \\ equal buying power",
                                  r"the growth \\ incidence curve"], box_w=2.8, font_size=20,
                           note_size=15).move_to(DOWN * 0.3)
        with self.voiceover(
            "Inside the world distribution, Christoph Lakner and Branko Milanovic ranked everyone on one scale and "
            f"asked how much real income grew at each percentile between {G['first']} and {G['last']}. Plotted, the "
            "curve looks like an elephant raising its trunk. <bookmark mark='a'/> The largest gains were around the "
            "global median, mostly the new middle classes of China and the rest of Asia. <bookmark mark='b'/> Around "
            f"the {G['stagnant_lo']}th to {G['stagnant_hi']}th percentiles, largely the lower middle classes of rich "
            "countries, there was essentially no gain. <bookmark mark='c'/> And the global top one percent gained a "
            "great deal. <bookmark mark='d'/> The curve compares positions, not people: the person at a percentile "
            "in 2008 is not the one who was there in 1988. Still, it tells the political story of the period, and "
            "Part thirty-six's China shock is one of its chapters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("a")
            self.play(FadeOut(steps), run_time=0.6)
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def top(self):
        W = load("world")
        T = W["world_top1"]
        ax = plane([1815, 2030], [10, 28], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1850, 1900, 1950, 2000], yticks=[10, 15, 20, 25], ylabel=r"the world's top 1\% share",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        ln = path(ax, T["year"], T["value"], TOP, 3.4, smooth=False)
        pts = VGroup(*[dot(ax, y, v, TOP, 0.05) for y, v in zip(T["year"], T["value"]) if y < 1980])
        val = dict(zip(T["year"], T["value"]))
        side = VGroup(
            label(rf"1910: \ {val[1910]:.0f}\%", font_size=19, color=WHITE),
            label(rf"1970: \ {val[1970]:.0f}\%", font_size=19, color=WHITE),
            label(rf"{T['year'][-1]}: \ {T['value'][-1]:.0f}\%", font_size=19, color=WHITE),
            label(r"between countries: \ falling; \\ within them: \ rising", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"World Inequality Database, \ via Our World in Data; \ sparse before 1980", corner=DR,
                       font_size=11)
        with self.voiceover(
            "The World Inequality Database estimates the share of the world's top one percent, from scattered "
            f"points in the nineteenth century to yearly figures since 1980. <bookmark mark='a'/> About "
            f"{val[1910]:.0f} percent in 1910; <bookmark mark='b'/> {val[1970]:.0f} percent in 1970; "
            f"<bookmark mark='c'/> {T['value'][-1]:.0f} percent in {T['year'][-1]}. <bookmark mark='d'/> Two forces "
            "pull in opposite directions: poorer countries catching up shrinks the gaps between nations, while "
            "rising inequality inside many of them pulls the top away."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts), Create(ln), run_time=2.0)
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()
