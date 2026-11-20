from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Bunching(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Bunching at kinks", r"Can a histogram reveal an elasticity?",
             "Chapter nine. Bunching at kinks.", lit={2010: r"Saez", 2013: r"Kleven and Waseem"},
             scale=("person",), horizon=("a year",))
        self.spike()
        self.estimate()
        self.findings()

    def _hist(self, ax, mid, h, col, bw):
        g = VGroup()
        for x, v in zip(mid, h):
            p0, p1 = ax.ax.c2p(x - bw / 2 + 0.02, 0), ax.ax.c2p(x + bw / 2 - 0.02, v)
            g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0, fill_color=col,
                            fill_opacity=0.8).move_to((p0 + p1) / 2))
        return g

    def spike(self):
        B = load("bunching")
        mid, h = np.array(B["mid"]), np.array(B["h"])
        ymax = float(h.max()) * 1.08
        ax = plane([25, 75], [0, ymax], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[30, 40, 50, 60, 70], yticks=[0, round(ymax / 2, -2), round(ymax, -2)],
                   xlabel=r"taxable income, \ thousands", ylabel=r"taxpayers", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:,.0f}", font_size=14)
        bars = self._hist(ax, mid, h, WORKER, B["bin_w"])
        kink = vline(ax, B["z_star"], 0, ymax, RATE)
        kl = label(rf"the rate rises from {100 * B['t0']:.0f}\% to {100 * B['t1']:.0f}\%", font_size=17,
                   color=RATE).next_to(ax.ax.c2p(B["z_star"], ymax), UP, buff=0.05)
        side = VGroup(
            label(rf"{B['n']:,} taxpayers \\ on the Island", font_size=18, color=WHITE),
            label(r"just above the kink, \\ each extra dollar \\ is taxed more: \\ some stop at it", font_size=18,
                  color=RATE),
            label(rf"{100 * B['share_bunched']:.1f}\% of taxpayers \\ choose to sit at the kink", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A cleaner way to see the elasticity uses the schedule's own corners. <bookmark mark='a'/> Here are "
            f"{B['n']:,} of the Island's taxpayers by taxable income. <bookmark mark='b'/> At fifty thousand the "
            f"marginal rate rises from {100 * B['t0']:.0f} to {100 * B['t1']:.0f} percent. Someone who would have "
            "earned a little more than fifty thousand now keeps less of each extra dollar above it, and some decide "
            "to stop exactly at the corner. <bookmark mark='c'/> They pile up: a spike in the histogram, made of "
            f"{100 * B['share_bunched']:.1f} percent of all taxpayers. The more responsive people are, the more of "
            "them bunch, so the size of the spike measures the elasticity."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(kink), FadeIn(kl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(bars[int(np.argmin(np.abs(mid - B["z_star"])))], color=WHITE, scale_factor=1.2),
                      FadeIn(side[2]))
        self.clear_scene()

    def estimate(self):
        B = load("bunching")
        mid, h, cf = np.array(B["mid"]), np.array(B["h"]), np.array(B["cf"])
        ymax = float(h.max()) * 1.08
        ax = plane([25, 75], [0, ymax], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[30, 40, 50, 60, 70], yticks=[0, round(ymax / 2, -2), round(ymax, -2)],
                   xlabel=r"taxable income, \ thousands", ylabel=r"taxpayers", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:,.0f}", font_size=14)
        bars = self._hist(ax, mid, h, WORKER, B["bin_w"])
        cfl = path(ax, mid, cf, TOP, 3.0)
        w = B["window"]
        win = Rectangle(width=ax.ax.c2p(B["z_star"] + w, 0)[0] - ax.ax.c2p(B["z_star"] - w, 0)[0],
                        height=ax.ax.c2p(0, ymax)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=GREY_D,
                        fill_opacity=0.35).move_to(ax.ax.c2p(B["z_star"], ymax / 2))
        eq = MathTex(r"\hat e = \frac{b}{z^{*} \, \ln\!\big(\frac{1 - t_0}{1 - t_1}\big)}", font_size=34).to_edge(
            UP, buff=0.3)
        side = VGroup(
            label(r"grey: \ a window \\ around the kink", font_size=17, color=GREY_A),
            label(r"gold: \ a polynomial \\ fitted outside it: \\ what the histogram \\ would be with no kink",
                  font_size=17, color=TOP),
            label(rf"excess mass $b$: \\ {B['b']:.2f} thousand of income \\ at the kink's density", font_size=17,
                  color=WHITE),
            label(rf"estimate: \ {B['e_hat']:.2f}; \\ planted: \ {B['e']:.2f}", font_size=20, color=E.ACCENT),
            label(rf"with larger frictions: \\ {B['noisy_e_hat']:.2f}", font_size=17, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 2010 Emmanuel Saez turned the spike into an estimator. <bookmark mark='a'/> Mark a window around the "
            "kink. <bookmark mark='b'/> Fit a smooth curve to the histogram outside it: an estimate of what the "
            "distribution would look like without the kink. <bookmark mark='c'/> The excess of taxpayers inside "
            "the window over that curve, measured in income at the curve's height, is the bunching. "
            "<bookmark mark='d'/> Divide by the kink's location times the log change in the share kept, and out "
            f"comes the elasticity: {B['e_hat']:.2f}, against the {B['e']:.2f} planted on the Island. "
            "<bookmark mark='e'/> But people cannot always fine-tune their incomes. With larger frictions the spike "
            f"spreads out, and the same estimator gives {B['noisy_e_hat']:.2f}: frictions make people look less "
            "responsive than they would be if adjusting were free."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(bars), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(win), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cfl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def findings(self):
        cards = point_cards([
            (r"the EITC's first kink", r"clear bunching, \\ but only among \\ the self-employed", TOP),
            (r"why them", r"their income is \\ self-reported: \\ easy to adjust \\ on paper", RATE),
            (r"wage earners", r"almost no bunching: \\ hours are hard \\ to fine-tune", WORKER),
            (r"notches", r"where the average rate \\ jumps, \ a hole above: \\ how many fail \\ to respond (Pakistan)",
             GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what the bunching studies found", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.BUNCHING.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Applied to American tax returns, the method gave a striking answer. <bookmark mark='a'/> There is clear "
            "bunching at the first kink of the Earned Income Tax Credit, <bookmark mark='b'/> but only among the "
            "self-employed, whose income is reported by themselves and easy to adjust on paper. "
            "<bookmark mark='c'/> Wage earners, whose employers report their pay, barely bunch at all. "
            "<bookmark mark='d'/> Henrik Kleven and Mazhar Waseem used notches, where the average rate jumps, in "
            "Pakistan: the hole left just above a notch reveals how many people fail to respond, and so separates "
            "frictions from preferences."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
