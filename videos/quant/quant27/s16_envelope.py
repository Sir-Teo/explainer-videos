from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant27.common import BAD, COIN, COMPLEX, GOOD, HURDLE, MKT, NET, PART, ask, comma, fit_right, load


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.network(e["nn3"])
        self.robust(e["nn3"])
        self.deflate(e["nn3"], e["trials"])
        self.timer(e["kmz"])
        self.rows(e)
        self.question()

    def card(self):
        c = chapter_card(15, r"The machine-learned strategies, registered and opened", r"What do the models do on five "
                         r"years nobody has looked at?", part=PART)
        with self.voiceover("Chapter fifteen. Two of this part's models, registered with every trial counted, and "
                            "opened once on the sealed years 2021 to 2025."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        cards = VGroup(
            firm_card(r"NN3 on coins", r"the paper's best architecture, chosen before any research result: a 32--16--8 "
                      r"network, five seeds; trained to mid-2020, early-stopped on its second half; a weekly "
                      r"value-weighted quintile long-short", numbers=((r"25", r"trials: the zoo, plus the ENet, PCR and "
                                                                        r"PLS grids"),), width=6.2, font_size=19,
                      kind=r"Registered"),
            firm_card(r"The complexity timer", r"Chapter 4's random-feature ridge on the Welch--Goyal predictors: "
                      r"$P = 12{,}000$, $z = 0.1$, twelve months of training, ten seeds; scaled to 10\% volatility in "
                      r"research", numbers=((r"84", r"trials: the grid of complexities and penalties"),), width=6.2,
                      font_size=19, kind=r"Registered"),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.4)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        ctr = MathTex(rf"\text{{the counter}}:\ 10{{,}}346\ \to\ {comma(e['trials'])}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two registrations. <bookmark mark='a'/> The three-layer network ensemble on coins: Gu, Kelly and Xiu's "
            "best architecture, chosen before any research result came in, which matters, because in research it "
            "came last. Trained to the middle of 2020, stopped early on the second half, and traded as a weekly "
            "value-weighted long-short. It counts twenty-five trials: the zoo and the tuning grids. <bookmark "
            "mark='b'/> And Chapter 4's complexity timer, with its twelve thousand random features, counting the "
            "eighty-four complexities and penalties of its grid. <bookmark mark='c'/> The counter goes from ten "
            "thousand three hundred and forty-six to ten thousand four hundred and fifty-five."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def network(self, n):
        cum = np.asarray(n["cum_vw"])
        T = len(cum)
        g = axes([0, T - 1], [min(cum.min(), 0) - 0.2, cum.max() * 1.1], x_length=8.6, y_length=4.0,
                 xlabel=r"week, 2021--2025", ylabel=r"cumulative log return, long-short", xticks=[], yticks=[0, 1, 2, 3, 4],
                 font_size=13).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(0)
        line = always_redraw(lambda: curve(ax, np.arange(int(tr.get_value()) + 1), cum[:int(tr.get_value()) + 1], NET,
                                           stroke_width=3))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(T - 1, 0), color=GREY_B, stroke_width=1.5)
        h, r = n["row"]["holdout"], n["row"]["research"]
        side = VGroup(
            MathTex(rf"SR = {h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=26, color=NET),
            MathTex(rf"\text{{net of 10 bp}}:\ {h['sharpe_net']:.2f}", font_size=24),
            MathTex(rf"R^2_{{\text{{oos}}}} = {100 * n['r2']:+.1f}\%", font_size=24, color=GOOD),
            MathTex(rf"\text{{equal weights}}:\ {n['sr_ew']:.2f}", font_size=24, color=BAD),
            MathTex(rf"\text{{research (2019--20)}}:\ {r['sharpe']:.2f}", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        fit_right(side)
        foot = note(r"monthly returns, compounded from weekly; Sharpe ratios annualised, with Lo's standard error", font_size=15,
                    color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The envelope opens on the network. <bookmark mark='a'/> Five years, two hundred and sixty-one weeks, "
            "around three hundred coins a week. <bookmark mark='b'/> The value-weighted long-short earns a Sharpe ratio "
            "of one point three, plus or minus a third; one point one after Binance's fee. The out-of-sample R squared "
            "is positive, three tenths of a percent, Gu, Kelly and Xiu's order of magnitude. <bookmark mark='c'/> But "
            "with equal weights the same forecasts lose, minus point four. And in research this model was the zoo's "
            "worst, at minus point seven. On two years of forty coins nothing could be learned about it; on five "
            "years of three hundred, something could."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            self.add(line)
            vo.wait_until("a")
            self.play(tr.animate.set_value(T - 1), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3:]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def robust(self, n):
        w = np.asarray(n["weeks"])
        r = np.expm1(np.diff(np.r_[0.0, np.asarray(n["cum_vw"])]))
        sr = lambda x: float(x.mean() / x.std() * math.sqrt(52))  # noqa: E731
        years = list(range(2021, 2026))
        by = [sr(r[(w // 10000) == y]) for y in years]
        k = np.argsort(-r)
        no5, no10 = sr(np.delete(r, k[:5])), sr(np.delete(r, k[:10]))
        g = axes([2020.4, 2025.6], [0, 3], x_length=6.4, y_length=3.6, xlabel=r"year", ylabel=r"Sharpe ratio, weekly",
                 xticks=years, yticks=[0, 1, 2, 3], font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]),
                                  height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0, fill_color=NET,
                                  fill_opacity=0.85).move_to([ax.c2p(y, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0])
                        for y, v in zip(years, by)])
        cost50 = (n["row"]["holdout"]["mean"] - 5 * n["cost"]) / n["row"]["holdout"]["vol"]
        side = VGroup(
            MathTex(rf"\text{{weeks up}}:\ {100 * (r > 0).mean():.0f}\%,\ \ \text{{median}}\ {100 * np.median(r):+.1f}\%",
                    font_size=24),
            MathTex(rf"\text{{without its best 5 weeks}}:\ {no5:.2f}", font_size=24),
            MathTex(rf"\text{{without its best 10}}:\ {no10:.2f}", font_size=24),
            MathTex(rf"\text{{at 50 bp a trade}}:\ {cost50:.2f}", font_size=24, color=BAD),
            wrapped_label(r"looked at after opening, for the record only: nothing here changes the registered strategy", 4.6,
                          15, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Is it one lucky event? <bookmark mark='a'/> No: it made money in every one of the five years, with "
            "Sharpe ratios from about three quarters to nearly two and a half. <bookmark mark='b'/> Half the weeks "
            "are up, a little more; the median week makes nine tenths of a percent. Remove its five best weeks and "
            "the Sharpe ratio is still about one point one; remove ten and it is about point seven. <bookmark "
            "mark='c'/> The weak point is cost. At fifty basis points a trade, more realistic for the smaller coins it "
            "holds, the Sharpe ratio falls to about a half."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(side[:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3:]))
        self.wait(0.4)
        self.clear_scene()

    def deflate(self, n, trials):
        h = n["row"]["holdout"]
        T = h["n"]
        s = h["sharpe"] / math.sqrt(12)
        rows = []
        for N, lab, col in ((25, r"this strategy's own 25 trials", NET), (84 + 25, r"this part's 109", HURDLE),
                            (trials, rf"the series' {comma(trials)}", BAD)):
            d = BT.deflated_sharpe(s, T, N, 1 / T)
            rows.append(VGroup(label(lab, font_size=20, color=col),
                               MathTex(rf"\text{{hurdle}}\ {d['sr0'] * math.sqrt(12):.2f},\ \ \text{{DSR}}\ {d['dsr']:.2f}",
                                       font_size=26)))
        # arrange() re-centres a group on the origin, so the rows are laid out before the table
        w = max(r_[0].width for r_ in rows)
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.5 + w - r_[0].width)
        tab = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.3)
        head = MathTex(rf"\widehat{{SR}} = {h['sharpe']:.2f}\ \text{{over}}\ {T}\ \text{{months}}", font_size=30,
                       color=NET).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"Part 26's deflated Sharpe ratio: the probability that the true Sharpe ratio beats the "
                             r"expected best of $N$ trials of noise with the same five-year standard error. A hold-out "
                             r"is one look, so its own $N$ is one; the counter says how much the series has searched to "
                             r"get here", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now Part 26's question: is it better than the best of the noise we tried? <bookmark mark='a'/> Against "
            "its own twenty-five trials, the hurdle is about point nine, and the deflated Sharpe ratio is point eight. "
            "<bookmark mark='b'/> Against the whole series' ten thousand four hundred and fifty-five, the hurdle is "
            "one point seven, and the probability falls below a fifth. A hold-out is a single look, so the strict "
            "number of trials for it is one. But the counter is the honest reminder of how much searching went into "
            "having this strategy to look at. The finale will deflate every row of the Track Record by it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def timer(self, k):
        cum = np.asarray(k["cum"])
        T = len(cum)
        g = axes([0, T - 1], [min(cum.min(), 0) - 0.03, max(cum.max(), 0) + 0.05], x_length=8.6, y_length=3.8,
                 xlabel=r"month, 2021--2025", ylabel=r"cumulative return, timer", xticks=[], yticks=[], font_size=13).move_to(
            LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        line = curve(ax, np.arange(T), cum, COMPLEX, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(T - 1, 0), color=GREY_B, stroke_width=1.5)
        r, h = k["row"]["research"], k["row"]["holdout"]
        side = VGroup(
            MathTex(rf"\text{{research}}:\ {r['sharpe']:.2f} \pm {r['sharpe_se']:.2f}", font_size=24, color=GREY_B),
            MathTex(rf"\text{{hold-out}}:\ {h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=24, color=COMPLEX),
            MathTex(rf"\text{{the market}}:\ {k['sr_mkt_hold']:.2f}", font_size=24, color=MKT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        fit_right(side)
        with self.voiceover(
            "The complexity timer. <bookmark mark='a'/> In research, ninety years of it, a Sharpe ratio of a third, "
            "measured to a tenth. <bookmark mark='b'/> On the five sealed years it lost a little, minus point one "
            "seven, while simply holding the market earned point seven. Five years cannot rule out a modest true edge; "
            "the standard error is nearly half. But Chapter 5's reading, that the timer is a volatility-scaled "
            "momentum, gave no reason to expect more, and in five years of a strong market, momentum in the index "
            "had little to add."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def rows(self, e):
        cols = [r"strategy", r"research", r"hold-out", r"net"]
        data = [(r"NN3 coins, long-short", e["nn3"]["row"]), (r"complexity timer", e["kmz"]["row"])]
        hx = [-3.8, 0.6, 2.9, 5.0]
        tab = VGroup(VGroup(*[label(c_, font_size=20, color=GREY_B).move_to([hx[i], 1.6, 0]) for i, c_ in
                              enumerate(cols)]))
        for j, (nm, row) in enumerate(data):
            y = 0.8 - 0.8 * j
            tab.add(VGroup(label(nm, font_size=20, color=QC.HOUSE).move_to([hx[0], y, 0]),
                           MathTex(rf"{row['research']['sharpe']:.2f}", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(rf"{row['holdout']['sharpe']:.2f} \pm {row['holdout']['sharpe_se']:.2f}",
                                   font_size=26).move_to([hx[2], y, 0]),
                           MathTex(rf"{row['holdout']['sharpe_net']:.2f}", font_size=26).move_to([hx[3], y, 0])))
        title = label(r"The Track Record, Part 27's rows", font_size=28).to_edge(UP, buff=0.5)
        foot = note(r"annualised Sharpe ratios of monthly returns; the net column charges the strategy's own turnover",
                    font_size=16, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And the two rows enter the Track Record: the coin network, from minus point seven in research to one "
            "point three on the sealed years, one point one net; and the timer, from a third to a small loss."
        ):
            self.play(FadeIn(title), FadeIn(tab), FadeIn(foot))
            self.wait(1.0)
        self.clear_scene()

    def question(self):
        q = ask(r"the coin network's research Sharpe ratio was $-0.7$ and its hold-out $1.3$. Would you have funded "
                r"it in January 2021? What would a capital ramp (Part 26) have done with it?")
        with self.voiceover(
            "Pause and predict. The coin network's research Sharpe ratio was minus point seven, and its hold-out one "
            "point three. Would you have funded it in January 2021? And what would Part 26's capital ramp have done "
            "with it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
