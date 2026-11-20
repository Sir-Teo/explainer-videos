from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Value(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Present value and the Gordon formula", r"What is a stream of dividends worth, \ and how much "
             r"does the discount rate matter?", "Chapter one. Present value and the Gordon formula.",
             lit={1938: r"Williams", 1956: r"Gordon and Shapiro"}, scale=("firm", "market"), horizon=("decades",))
        self.pv()
        self.gordon()
        self.history()

    def pv(self):
        rows = VGroup(
            label(r"a dollar a year from now is worth $\frac{1}{1+r}$ today; \ in $t$ years, \ $\frac{1}{(1+r)^t}$",
                  font_size=25, color=BILL),
            MathTex(r"P_0 \;=\; \sum_{t=1}^{\infty} \frac{D_t}{(1+r)^t}", font_size=50, color=WHITE),
            label(r"an asset is worth the present value of what it will pay", font_size=24, color=GREY_A),
            MathTex(r"D_t = D_1 (1+g)^{t-1}, \;\; r > g \quad\Longrightarrow\quad P_0 = \frac{D_1}{r - g}",
                    font_size=46, color=STOCK),
            label(r"the Gordon formula \ (Williams, \ 1938; \ Gordon and Shapiro, \ 1956)", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Start with the arithmetic every asset price rests on. <bookmark mark='a'/> A dollar a year from now is "
            "worth one over one plus r today, where r is the rate at which you could grow a dollar instead. "
            "<bookmark mark='b'/> So an asset that pays dividends D one, D two, and so on, is worth the sum of their "
            "present values. <bookmark mark='c'/> That is the whole of the theory of value, if you know the "
            "dividends and the right rate. Both are the hard part. <bookmark mark='d'/> If dividends grow at a "
            "steady rate g, below r, the sum collapses to a famous formula: the first dividend over r minus g. "
            "<bookmark mark='e'/> John Burr Williams wrote down the idea in 1938; Myron Gordon made the formula a "
            "tool in the 1950s."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def gordon(self):
        g = load("gordon")
        ax = plane([0.035, 0.12], [0, 260], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=[0.04, 0.06, 0.08, 0.10, 0.12], yticks=[0, 50, 100, 150, 200, 250],
                   xlabel=r"discount rate $r$", ylabel=r"price, \ $D_1 / (r - g)$", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        rs = np.linspace(0.0355, 0.12, 200)
        curve = path(ax, rs, g["D1"] / (rs - g["g"]), color=STOCK, width=4, yr=(0, 260))
        p0 = dot(ax, g["r"], g["price"], color=WHITE)
        p1 = dot(ax, g["r"] + 0.01, g["price_up"], color=RISK)
        side = VGroup(
            label(rf"dividend next year: \ {g['D1']:g}; \ growth {pc(g['g'], 0)}", font_size=21, color=GREY_A),
            label(rf"at $r = {pc(g['r'], 0)}$: \ price {g['price']:.0f}", font_size=23, color=WHITE),
            label(rf"at $r = {pc(g['r'] + 0.01, 0)}$: \ price {g['price_up']:.0f}", font_size=23, color=RISK),
            label(rf"one point on the discount rate: \\ $-{100 * g['fall_per_point']:.0f}\%$ on the price", font_size=22,
                  color=HOLD),
            label(rf"a long-lived asset's duration, \\ $1/(r-g)$: \ {g['duration']:.0f} years", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Take a share that will pay a dividend of {g['D1']:g} next year, growing {100 * g['g']:.0f} percent a "
            "year for ever. <bookmark mark='a'/> At a discount rate of seven percent it is worth four over four "
            f"hundredths: {g['price']:.0f}. <bookmark mark='b'/> Raise the discount rate by a single point, to eight, "
            f"and it is worth {g['price_up']:.0f}. <bookmark mark='c'/> One point on the rate, a fifth off the price. "
            "<bookmark mark='d'/> Long-lived assets, whose value lies mostly in the distant future, are extremely "
            "sensitive to the rate at which that future is discounted. That is why so much of what moves stock "
            "prices and house prices is not news about dividends or rents, but news about discount rates."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(curve), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(p0), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def history(self):
        g = load("gordon")
        ax = plane([1870, 2015], [0, 50], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[1880, 1920, 1960, 2000], yticks=[0, 10, 20, 30, 40, 50],
                   ylabel=r"real price $\div$ real dividends, \ S\&P composite", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        line_ = path(ax, g["pd_years"], g["pd"], color=STOCK, width=3, smooth=False)
        mean = seg(ax, 1870, g["pd_mean"], 2015, g["pd_mean"], color=GREY_B, width=2, dashed=True)
        side = VGroup(
            label(rf"{g['pd_years'][0]}: \ {g['pd_first']:.0f} \ times dividends", font_size=20, color=STOCK),
            label(rf"average: \ {g['pd_mean']:.0f}", font_size=20, color=GREY_B),
            label(rf"{g['pd_years'][-1]}: \ {g['pd_last']:.0f}", font_size=20, color=STOCK),
            label(rf"real dividends grew \\ {pc(g['div_growth'])} a year", font_size=20, color=GREY_A),
            label(r"a price that wanders \\ this far is a puzzle \\ for chapter 10", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Shiller, \emph{Market Volatility} (1989), \ ch.\ 26 data, \ updated", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the ratio in the record. Robert Shiller's data for the S and P composite index of American "
            "stocks, from 1871, the price divided by a year of dividends. <bookmark mark='a'/> In "
            f"{g['pd_years'][0]} the market sold for about {g['pd_first']:.0f} times its dividends. "
            f"<bookmark mark='b'/> On average, about {g['pd_mean']:.0f}. <bookmark mark='c'/> By "
            f"{g['pd_years'][-1]}, about {g['pd_last']:.0f}. <bookmark mark='d'/> Real dividends grew only about "
            f"{100 * g['div_growth']:.1f} percent a year. <bookmark mark='e'/> If the Gordon formula holds, a "
            "ratio that wanders this far means that either expected growth or the discount rate moved a lot. "
            "Chapter ten asks which."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), FadeIn(mean), run_time=2.5)
            for mk, r_ in zip("abcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
