from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Hyper(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Hyperinflation and the inflation tax", r"How high can inflation go, \ and why would a "
             r"government print that much?", "Chapter six. Hyperinflation and the inflation tax.",
             lit={1956: r"Cagan", 2012: r"Hanke and Krus"}, scale=("nation",), horizon=("a month",))
        self.records()
        self.demand()
        self.laffer()
        self.called()

    def records(self):
        L = load("laffer")
        rows = L["table"]
        ax = plane([-0.6, 3.6], [0, 18], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8, xticks=[],
                   yticks=[0, 4, 8, 12, 16], ylabel=r"highest monthly inflation, \ \% \ (log scale)",
                   yfmt=lambda v: rf"$10^{{{v:.0f}}}$", font_size=16)
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, r in enumerate(rows):
            lo, hi = ax.ax.c2p(k, 0), ax.ax.c2p(k, r["log10"])
            bars.add(Rectangle(width=0.9, height=hi[1] - lo[1], fill_color=PRICE, fill_opacity=0.75,
                               stroke_width=0).move_to((lo + hi) / 2))
            names.add(label(rf"{r['country']} \\ {r['month']}", font_size=16, color=WHITE).next_to(lo, DOWN, buff=0.12))
            d = r["doubling_days"]
            when = rf"{24 * d:.0f} hours" if d < 2 else rf"{d:.1f} days"
            vals.add(label(rf"prices double \\ every {when}", font_size=15, color=PRICE).next_to(bars[-1], UP,
                                                                                               buff=0.08))
        side = VGroup(
            label(r"Cagan's definition: \\ over 50\% a month", font_size=20, color=GREY_A),
            label(r"Germany, \ October 1923: \\ 29{,}500\% a month", font_size=20, color=PRICE),
            label(r"Hungary, \ July 1946: \\ $4.19 \times 10^{16}$\% a month", font_size=20, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Hanke and Krus, \ \"World Hyperinflations\", \ Cato WP 8 (2012)", corner=DR, font_size=12)
        with self.voiceover(
            "Phillip Cagan defined a hyperinflation in 1956 as prices rising more than fifty percent a month. "
            "Steve Hanke and Nicholas Krus later listed every one they could document. <bookmark mark='a'/> Here "
            "are four peaks, on a log scale. Germany, October 1923: prices rose twenty-nine thousand five hundred "
            "percent in a month, doubling every few days. <bookmark mark='b'/> Yugoslavia, January 1994, and Zimbabwe, "
            "November 2008: prices doubled every day or so. <bookmark mark='c'/> And the record, Hungary in July "
            "1946: forty-one quadrillion percent in a month, prices doubling about every fifteen hours."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(names), run_time=1)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]), GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(vals[3]), FadeIn(side[2]))
        self.clear_scene()

    def demand(self):
        rows = VGroup(
            label(r"Cagan's demand for real balances", font_size=27, color=E.ACCENT),
            MathTex(r"\ln \frac{M_t}{P_t} \;=\; -\alpha\,\pi^e_t \;+\; \gamma", font_size=48, color=MONEY),
            label(r"when people expect prices to rise fast, \ they hold less money: \ they spend wages the day they "
                  r"are paid", font_size=23, color=GREY_A),
            label(r"$\alpha$: \ the semi-elasticity, \ in months; \ about 5 for Germany in 1922--23", font_size=23,
                  color=MONEY),
            label(r"the inflation tax: \ printing money takes purchasing power from everyone who holds it",
                  font_size=23, color=PRICE),
            MathTex(r"\text{real seigniorage} \;=\; \pi \cdot \frac{M}{P} \;=\; \pi\,e^{-\alpha\pi + \gamma}",
                    font_size=42, color=PRICE),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Cagan, \ in Friedman (ed.), \emph{Studies in the Quantity Theory of Money} (1956): "
                            r"\ 25--117", corner=DR, font_size=12)
        with self.voiceover(
            "Cagan's insight was about demand. <bookmark mark='a'/> People choose how much purchasing power to keep "
            "in money. <bookmark mark='b'/> He wrote the log of real balances as falling in proportion to expected "
            "inflation. <bookmark mark='c'/> When prices are expected to rise fast, people hold as little money as "
            "they can: workers are paid daily and spend their wages within hours. <bookmark mark='d'/> The constant, "
            "alpha, measured in months, was about five in Germany. <bookmark mark='e'/> And a government that prints "
            "money collects a tax: every holder of money loses purchasing power, and the government gains it. "
            "<bookmark mark='f'/> The tax rate is inflation; the tax base is real balances. Raise the rate, and the "
            "base shrinks."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def laffer(self):
        L = load("laffer")
        ax = plane([0, 1.2], [0, 0.08], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], yticks=[0, 0.02, 0.04, 0.06, 0.08],
                   xlabel=r"inflation, \ a month", ylabel=r"seigniorage, \ a month \ (real balances at zero "
                   r"inflation $= 1$)", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.2f}", font_size=16)
        curve = path(ax, L["mu"], L["revenue"], color=PRICE, width=4)
        peak = dot(ax, L["best"], L["max"], color=E.ACCENT, r=0.1)
        drop = seg(ax, L["best"], 0, L["best"], L["max"], color=E.ACCENT, width=2, dashed=True)
        side = VGroup(
            label(r"the inflation tax's \\ Laffer curve", font_size=22, color=PRICE),
            label(rf"most revenue at \\ $\pi = 1/\alpha = {100 * L['best_exact']:.0f}\%$ a month", font_size=22,
                  color=E.ACCENT),
            label(rf"at most {100 * L['max_exact']:.1f}\% of real balances \\ a month", font_size=20, color=GREY_A),
            label(r"beyond it, \ printing faster \\ raises \emph{less}", font_size=21, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Plot the revenue against the rate. <bookmark mark='a'/> At low inflation the tax raises little. As "
            "inflation rises, revenue rises, until people's flight from money outruns the higher rate. "
            "<bookmark mark='b'/> With alpha equal to five, revenue is highest at one over alpha: twenty percent a "
            f"month. <bookmark mark='c'/> And even there it is only about {100 * L['max_exact']:.1f} percent of the "
            "real balances people would hold at zero inflation, each month. <bookmark mark='d'/> Beyond the peak, "
            "printing faster raises less. A government that wants revenue should stop at twenty percent a month. "
            "None did."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(curve), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(peak), Create(drop), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["cagan_ceiling"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=19).move_to(UP * 0.1)
        tag = published_tag(r"Cagan (1956), \ as summarized in later work on Cagan's paradox", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> The revenue theory says governments print money to pay their bills, and "
            "Cagan's estimates put the most they could raise at about twenty percent inflation a month. "
            "<bookmark mark='b'/> They went far beyond it. German prices rose three hundred and twenty-two percent a "
            "month on average from August 1922 to November 1923, and in most of Cagan's seven cases inflation ran "
            "above the rate that maximized revenue. Economists call it Cagan's paradox. The likeliest answers: "
            "expectations lag, so printing faster pays for a while before people catch up; and governments in "
            "collapse could not commit to stop. <bookmark mark='c'/> Wrong, as a forecast of what governments would "
            "do."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
