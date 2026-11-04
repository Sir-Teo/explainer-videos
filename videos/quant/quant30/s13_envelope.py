from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EW_C, GOOD, HRP_C, HURDLE, OOS_C, PART, SHRINK_C, comma, fit_right, load

S_COL = {"lw_gmv_part30": SHRINK_C, "hrp_part30": HRP_C, "equal_weight_part30": EW_C}
S_NAME = {"lw_gmv_part30": r"shrunk minimum variance", "hrp_part30": r"HRP", "equal_weight_part30": r"1/N"}


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.opened(e)
        self.table(e)
        self.reading(e)
        self.question()

    def card(self):
        c = chapter_card(12, r"Minimum variance and HRP, registered and opened", r"Did the humble rules keep their "
                         r"promise on five sealed years?", part=PART)
        with self.voiceover("Chapter twelve. Two optimizers from this part, and the benchmark they must beat, registered "
                            "and opened once on 2021 to 2025."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"Three rules, registered", r"on the 49 industries, rebalanced monthly on the trailing 120 months: "
                         r"minimum variance with Ledoit--Wolf constant-correlation shrinkage; HRP on the sample "
                         r"covariance; and 1/N as the benchmark",
                         numbers=((rf"{e['n_trials']}", r"trials for each optimizer: every rule and window of Chapter 2's "
                                                         r"contest; 1 for 1/N"),
                                  (r"10\ \text{bp}", r"per dollar traded, on each rule's measured turnover")),
                         kind=r"Registered", width=10.6, font_size=22).move_to(UP * 0.4)
        n_now = int(e["trials"])
        n_before = n_now - 2 * int(e["n_trials"]) - 1
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(n_before)}\ \to\ {comma(n_now)}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The registration. <bookmark mark='a'/> Three rules on the forty-nine industries, each re-estimated monthly "
            "on the previous ten years: minimum variance with constant-correlation shrinkage, which led Chapter two's "
            "contest; hierarchical risk parity; and one over N, the benchmark. <bookmark mark='b'/> Each optimizer is "
            f"charged with the {e['n_trials']} rule-and-window combinations we compared to choose it. The counter moves to "
            f"{n_now:,}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        st = e["strats"]
        d = np.asarray(st["lw_gmv_part30"]["hold_dates"], float)
        x = d // 100 + ((d % 100) - 0.5) / 12
        ys = {k: 100 * np.asarray(v["cum_hold"], float) for k, v in st.items()}
        lo = float(np.floor(min(y.min() for y in ys.values()) / 10) * 10)
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 10) * 10)
        g = axes([x[0], x[-1]], [min(lo, 0), hi], x_length=7.4, y_length=4.4, xlabel=r"2021--2025, sealed until now",
                 ylabel=r"cumulative log return, \%", xticks=[2021, 2023, 2025], yticks=[min(lo, 0), 0, hi],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, x, ys[k], S_COL[k], stroke_width=3) for k in st])
        leg = legend([(S_COL[k], S_NAME[k]) for k in st], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        with self.voiceover(
            "The envelope. <bookmark mark='a'/> Five years: the boom of 2021, the bear market of 2022 as rates rose, and "
            "the recovery led by a handful of technology firms. <bookmark mark='b'/> All three rules made money, along "
            "different paths."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines], run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        st = e["strats"]
        hx = [-4.0, -1.0, 1.4, 3.6, 5.6]
        head = VGroup(label(r"rule", font_size=17, color=GREY_B), label(r"Sharpe, 1980--2020", font_size=17, color=GREY_B),
                      label(r"Sharpe, 2021--25", font_size=17, color=OOS_C), label(r"net", font_size=17, color=OOS_C),
                      label(r"volatility", font_size=17, color=OOS_C))
        tab = VGroup(head)
        for k, v in st.items():
            r, h = v["row"]["research"], v["row"]["holdout"]
            tab.add(VGroup(label(S_NAME[k], font_size=19, color=S_COL[k]), MathTex(f"{r['sharpe']:.2f}", font_size=24),
                           MathTex(rf"{h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=24),
                           MathTex(f"{h['sharpe_net']:.2f}", font_size=24), MathTex(rf"{100 * h['vol']:.1f}\%", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(r"monthly excess returns over T-bills; standard errors for 60 months; net: after 10 bp per "
                             r"dollar traded", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        lw, hp, ew = (st[k]["row"]["holdout"] for k in ("lw_gmv_part30", "hrp_part30", "equal_weight_part30"))
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> Over the research years, shrunk minimum variance and HRP both beat one "
            "over N. <bookmark mark='b'/> On the sealed years the order reversed: one over N earned a Sharpe ratio of "
            f"{ew['sharpe']:.2f}, HRP {hp['sharpe']:.2f}, minimum variance {lw['sharpe']:.2f}. Minimum variance still "
            f"had the least risk, {100 * lw['vol']:.1f} percent against {100 * ew['vol']:.1f}. And every difference is "
            f"smaller than one standard error, about {lw['sharpe_se']:.2f}: five years cannot rank these rules."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[2:])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, e):
        st = e["strats"]
        lw = st["lw_gmv_part30"]
        cards = VGroup(
            desk_question(r"what minimum variance promised", r"less risk, not more return; it delivered less risk, though "
                          rf"less of it than in research ({100 * lw['vol_res']:.1f}\% then, "
                          rf"{100 * lw['vol_hold']:.1f}\% now)", width=12.4, font_size=19),
            desk_question(r"why 1/N did well", rf"2021--25 rewarded the industries that had been volatile: across the 49, "
                          rf"the correlation of their 2021--25 return with their 2011--20 volatility is "
                          rf"{e['vol_return_corr']:.2f}; the leaders were {', '.join(e['top_hold'][:3])}", width=12.4,
                          font_size=19),
            desk_question(r"what the Track Record keeps", r"three rows, with standard errors larger than their differences; "
                          r"the finale combines them with the rest of the series' evidence", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How to read it. <bookmark mark='a'/> Minimum variance promises less risk, not more return, and it delivered "
            f"less risk, though less of an advantage than in research: {100 * lw['vol_res']:.1f} percent then, "
            f"{100 * lw['vol_hold']:.1f} now. <bookmark mark='b'/> These years rewarded the industries that had been most "
            f"volatile: the correlation between an industry's return in them and its volatility in the decade before was "
            f"{e['vol_return_corr']:.2f}. Those are exactly the industries a risk-based rule leans away from. <bookmark mark='c'/> The Track Record keeps "
            "three rows whose standard errors are larger than their differences, which is itself the honest finding."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two rules each have a Sharpe ratio standard error of 0.45 over five years, and their returns "
                       r"correlate 0.9. Is the standard error of their difference larger or smaller than 0.45?")
        with self.voiceover(
            "Pause and predict. Two rules each have a Sharpe ratio standard error of about point four five over five "
            "years, and their returns are ninety percent correlated. Is the standard error of their difference larger or "
            "smaller?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
