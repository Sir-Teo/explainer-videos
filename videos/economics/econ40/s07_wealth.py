from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Wealth(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Wealth, \ and $r$ against $g$", r"Who owns what, \ and why does wealth concentrate?",
             "Chapter six. Wealth, and r against g.", lit={2006: r"Klass et al.", 2014: r"Piketty",
                                                           2015: r"Rognlie; \ Krusell and Smith"},
             scale=("household", "nation"), horizon=("a decade", "a century"))
        self.shares()
        self.alpha()
        self.rg()
        self.replies()

    def shares(self):
        W = load("wealth")
        t = np.array(W["t"])
        ax = plane([1989, 2027], [0, 45], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 10, 20, 30, 40],
                   ylabel=r"share of household net worth", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%",
                   font_size=14)
        keys = (("top1", r"top 1\%", WEALTH), ("next9", r"the next 9\%", TOP), ("next40", r"the next 40\%", MIDDLE),
                ("bottom50", r"the bottom 50\%", BOTTOM))
        lines = VGroup(*[path(ax, t, W[k], c, 3.0, smooth=False) for k, _, c in keys])
        f, l_ = W["first"], W["last"]
        side = VGroup(*[label(rf"{nm}: \ {f[k]:.1f}\% $\to$ {l_[k]:.1f}\%", font_size=18, color=c)
                        for k, nm, c in keys]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve, \ Distributional Financial Accounts, \ via FRED", corner=DR, font_size=11)
        with self.voiceover(
            "Wealth is far more concentrated than income. The Federal Reserve now splits all American household "
            f"wealth, every quarter since 1989. <bookmark mark='a'/> The richest one percent held {f['top1']:.1f} "
            f"percent in 1989, and {l_['top1']:.1f} percent in 2026. <bookmark mark='b'/> The next nine percent "
            f"held between {min(W['next9']):.0f} and {max(W['next9']):.0f} percent throughout. "
            "<bookmark mark='c'/> The middle forty percent, the "
            f"homeowners, fell from {f['next40']:.0f} to {l_['next40']:.0f} percent. <bookmark mark='d'/> And the "
            f"bottom half of American households together own {l_['bottom50']:.1f} percent of the wealth: less "
            "than a tenth of what the top one percent own."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(lines[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(lines[0], color=WHITE, scale_factor=1.0))
            for mk, k in zip("bcd", range(1, 4)):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(side[k]), run_time=1.5)
        self.clear_scene()

    def alpha(self):
        W = load("wealth")
        t = np.array(W["t"])
        ax = plane([1989, 2027], [1.3, 1.9], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
                   ylabel=r"Pareto exponent of wealth, \ from the top 1\% and top 10\% shares",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, t, W["alpha"], WEALTH, 3.2, smooth=False)
        forbes = seg(ax, 1989, W["forbes"], 2004, W["forbes"], TOP, 3.0)
        side = VGroup(
            label(rf"{W['first']['date'][:4]}: \ {W['first']['alpha']:.2f}", font_size=19, color=WEALTH),
            label(rf"{W['last']['date'][:4]}: \ {W['last']['alpha']:.2f}", font_size=19, color=WEALTH),
            label(rf"the Forbes 400, \\ 1988--2003: \ {W['forbes']:.2f}", font_size=19, color=TOP),
            label(r"income's exponent \\ in 2022: \ about 1.6", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"computed from the DFA shares; \ " + tables.FORBES_400.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Wealth has a Pareto tail too. From the shares of the top one and top ten percent, the exponent follows. "
            f"<bookmark mark='a'/> It was {W['first']['alpha']:.2f} in 1989, <bookmark mark='b'/> and "
            f"{W['last']['alpha']:.2f} in 2026: fatter, and fatter than the tail of incomes. <bookmark mark='c'/> "
            "Physicists who fitted the Forbes 400 lists of the richest Americans from 1988 to 2003 found "
            f"{W['forbes']:.2f}, close to what the top shares imply now. Why is wealth's tail so fat?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                if k == 2:
                    self.play(Create(forbes), FadeIn(side[2]), FadeIn(side[3]))
                else:
                    self.play(FadeIn(side[k]))
        self.clear_scene()

    def rg(self):
        W = load("wealth")
        rg, z = np.array(W["rg"]), np.array(W["zeta"])
        ax = plane([-0.01, 0.045], [0.5, 4.5], center=LEFT * 2.0 + DOWN * 0.6, x_length=7.6, y_length=4.4,
                   xticks=[0, 0.01, 0.02, 0.03, 0.04], yticks=[1, 2, 3, 4],
                   xlabel=r"$r - g$: \ the return on wealth less the growth of the economy",
                   ylabel=r"the tail exponent of wealth", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        m = (z <= 4.5) & (z >= 0.5)
        ln = path(ax, rg[m], z[m], WEALTH, 3.4)
        one = seg(ax, -0.01, 1.0, 0.045, 1.0, LOSS, 1.5, dashed=True)
        marks = VGroup(*[dot(ax, float(k), v, TOP, 0.08) for k, v in W["marks"].items() if 0.5 <= v <= 4.5])
        eq = MathTex(r"d \ln w = (r - g - c)\, dt + \sigma\, dW, \quad \zeta = "
                     r"\frac{-(r-g-c) + \sqrt{(r-g-c)^2 + 2\sigma^2\delta}}{\sigma^2}", font_size=28).to_edge(
            UP, buff=0.3)
        mk = W["marks"]
        side = VGroup(
            label(rf"$r - g$ = 0: \ $\zeta$ = {mk['0.0']:.1f}", font_size=19, color=TOP),
            label(rf"$r - g$ = 2\%: \ $\zeta$ = {mk['0.02']:.1f}", font_size=19, color=TOP),
            label(rf"$r - g$ = 3\%: \ $\zeta$ = {mk['0.03']:.1f}", font_size=19, color=TOP),
            label(r"below 1 (red): \\ no stationary mean; \\ wealth would keep \\ concentrating", font_size=17,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
        tag = island_tag(corner=DR, font_size=14)
        hc = history_card(2014, r"Thomas Piketty", r"\emph{Capital in the Twenty-First Century}: \ when the "
                          r"return on wealth, \ $r$, \ exceeds the growth of the economy, \ $g$, \ inherited wealth "
                          r"outgrows earned income", color=WEALTH, width=10.4, font_size=24)
        with self.voiceover(
            "In 2014 Thomas Piketty's Capital in the Twenty-First Century put one inequality at the centre: r "
            "greater than g. When the return on wealth exceeds the growth rate of the economy, inherited wealth "
            "grows faster than incomes, unless it is consumed or taxed. <bookmark mark='p'/> Random growth makes the "
            "argument precise. A "
            "dynasty's wealth, relative to the economy, grows at r minus g minus what it consumes, with luck in its "
            "returns, and dynasties end or split. <bookmark mark='a'/> The tail exponent of wealth then depends on r "
            f"minus g. With r equal to g, zeta is {mk['0.0']:.1f} on the Island. <bookmark mark='b'/> At two points, "
            f"{mk['0.02']:.1f}; <bookmark mark='c'/> at three, {mk['0.03']:.1f}. <bookmark mark='d'/> A point or two "
            "of r minus g turns a thin tail into a very fat one; past a threshold, wealth has no stable distribution "
            "at all."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("p")
            self.play(FadeOut(hc), run_time=0.6)
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk_, k in zip("abc", (0, 2, 3)):
                vo.wait_until(mk_)
                self.play(FadeIn(marks[k], scale=1.5), FadeIn(side[(0, 1, 2)[("abc").index(mk_)]]))
            vo.wait_until("d")
            self.play(Create(one), FadeIn(side[3]))
        self.clear_scene()

    def replies(self):
        cards = point_cards([
            (r"housing", r"most of the rise in \\ the net capital share \\ is housing \ (Rognlie)", BOTTOM),
            (r"depreciation", r"with net, \ not gross, \\ saving, \ wealth does \\ not explode as growth \\ slows "
                              r"(Krusell and Smith)", MIDDLE),
            (r"substitution", r"a rising capital share \\ needs an elasticity of \\ substitution above one; \\ most "
                              r"estimates are below", TOP),
            (r"what remains", r"returns differ by wealth, \\ and the very top \\ earns the most: \ the \\ tail "
                              r"depends on $r$ there", WEALTH),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"the replies to $r > g$", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CAPITAL_2014.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The book drew sharp replies. <bookmark mark='a'/> Matthew Rognlie found that most of the rise in the "
            "net share of income going to capital is housing, not factories or shares. <bookmark mark='b'/> Per "
            "Krusell and Anthony Smith showed that, once capital wears out, the ratio of wealth to income does not "
            "explode as growth slows. <bookmark mark='c'/> And a rising capital share as capital piles up requires "
            "capital and labour to be easy substitutes, with an elasticity above one, while most estimates are "
            "below it. <bookmark mark='d'/> What survives is the mechanism: what matters for the tail is the return "
            "earned by the very top, and how it compares with the growth of everyone else's income."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
