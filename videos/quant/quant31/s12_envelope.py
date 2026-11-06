from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, GOOD, GP_C, HURDLE, MYO_C, OOS_C, PART, comma, fit_right, load


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.opened(e)
        self.versus(e)
        self.table(e)
        self.diagnose(e)
        self.why_it_failed()
        self.rules()
        self.question()

    def card(self):
        c = chapter_card(11, r"The aim portfolio on the coins, registered and opened", r"Did trading toward the aim "
                         r"survive five sealed years?", part=PART)
        with self.voiceover("Chapter eleven. Chapter five's trader, registered before the envelope is opened, and judged "
                            "once on 2021 to 2025."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"One rule, registered", r"the calm and the three-day reversal signals on every eligible Binance "
                         r"coin, combined in Garleanu and Pedersen's aim portfolio and traded toward it at their rate, with "
                         r"$\gamma = 1$ and $\lambda = 8$; signal speeds and coefficients fixed on 2018--2020; the quadratic "
                         r"cost charged inside the P\&L",
                         numbers=((rf"{e['n_trials']}", r"trials: every cost level and trader compared in Chapter 5"),
                                  (r"\lambda = 8", r"chosen as a cost level the myopic trader could not survive")),
                         kind=r"Registered", width=10.6, font_size=22).move_to(UP * 0.4)
        n_now = int(e["trials"])
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(n_now - e['n_trials'])}\ \to\ {comma(n_now)}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The registration. <bookmark mark='a'/> Both signals of Chapter five, on every eligible coin, combined in the "
            "aim portfolio and traded toward it at Garleanu and Pedersen's rate, at the cost level where the myopic "
            "trader had already failed. Every parameter was fixed on the research years, and the cost is charged inside "
            f"the profit and loss. <bookmark mark='b'/> It is charged with {e['n_trials']} trials, every cost level and "
            f"trader compared to choose it. The counter moves to {n_now:,}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        d = np.asarray(e["res"]["hold_dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        y = 100 * np.asarray(e["res"]["gp"]["cum_hold"], float)
        lo = float(np.floor(y.min() / 100) * 100)
        g = axes([x[0], x[-1]], [lo, 100], x_length=7.4, y_length=4.4, xlabel=r"2021--2025, sealed until now",
                 ylabel=r"cumulative return at 10\% research volatility, \%", xticks=[2021, 2023, 2025],
                 yticks=[lo, lo / 2, 0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_C, stroke_width=1.5)
        line = curve(ax, x, y, GP_C, stroke_width=3)
        gp, my = e["res"]["gp"], e["res"]["myopic"]
        st = VGroup(label(rf"Sharpe, 2018--20: {gp['sr_res']:.2f}", font_size=17, color=GP_C),
                    label(rf"Sharpe, 2021--25: {gp['sr_hold']:.2f}", font_size=17, color=BAD),
                    label(rf"myopic, same years: {my['sr_hold']:.2f}", font_size=17, color=MYO_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        fit_right(st)
        with self.voiceover(
            "The envelope. <bookmark mark='a'/> On the research years, a Sharpe ratio of "
            f"{gp['sr_res']:.2f} after costs. <bookmark mark='b'/> On the sealed years, a disaster: {gp['sr_hold']:.2f}, "
            f"with losses many times the volatility it was scaled to. The myopic trader, run on the same years, did as "
            f"badly, {my['sr_hold']:.2f}. Something other than the trading rule broke."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(st[0]))
            vo.wait_until("b")
            self.play(Create(line), run_time=2.5)
            self.play(FadeIn(st[1:]))
        self.wait(0.4)
        self.clear_scene()

    def versus(self, e):
        gp, my = e["res"]["gp"], e["res"]["myopic"]
        hx = [-3.0, 0.8, 3.8]
        head = VGroup(label(r"trader, $\lambda = 8$", font_size=18, color=GREY_B), label(r"2018--2020", font_size=18,
                                                                                         color=GREY_B),
                      label(r"2021--2025", font_size=18, color=OOS_C))
        tab = VGroup(head,
                     VGroup(label(r"Garleanu--Pedersen", font_size=20, color=GP_C), MathTex(f"{gp['sr_res']:.2f}", font_size=26),
                            MathTex(f"{gp['sr_hold']:.2f}", font_size=26, color=BAD)),
                     VGroup(label(r"myopic", font_size=20, color=MYO_C), MathTex(f"{my['sr_res']:.2f}", font_size=26),
                            MathTex(f"{my['sr_hold']:.2f}", font_size=26, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.8 * j, 0])
        foot = wrapped_label(r"daily Sharpe ratios, annualised, net of the quadratic cost; the myopic trader is shown for "
                             r"comparison and is not a registered strategy", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Did the dynamic trader at least beat the myopic one? <bookmark mark='a'/> On the research years, by far: "
            f"{gp['sr_res']:.2f} against {my['sr_res']:.2f}, at the same cost. <bookmark mark='b'/> On the sealed years both "
            "collapsed. Whatever broke, it broke the signals and the risk model they share, not the way they were "
            "traded."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(tab[1][:2], tab[2][:2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(tab[1][2], tab[2][2])))
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        row = e["res"]["row"]
        r, h = row["research"], row["holdout"]
        hx = [-3.2, 0.6, 3.8]
        head = VGroup(label(r"monthly, in the Track Record", font_size=18, color=GREY_B),
                      label(r"2018--2020", font_size=18, color=GREY_B), label(r"2021--2025", font_size=18, color=OOS_C))
        lines = [(r"Sharpe ratio", rf"{r['sharpe']:.2f} \pm {r['sharpe_se']:.2f}", rf"{h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}"),
                 (r"volatility", rf"{100 * r['vol']:.0f}\%", rf"{100 * h['vol']:.0f}\%"),
                 (r"worst drawdown", rf"{100 * r['maxdd']:.0f}\%", rf"{100 * h['maxdd']:.0f}\%"),
                 (r"months", rf"{r['n']}", rf"{h['n']}")]
        tab = VGroup(head)
        for nm, a, b in lines:
            tab.add(VGroup(label(nm, font_size=20), MathTex(a, font_size=26), MathTex(b, font_size=26, color=BAD)))
        for j, rr in enumerate(tab):
            for i, cell in enumerate(rr):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label(r"monthly sums of the daily net P\&L, scaled so research volatility is 10\% a year; the research "
                             r"months begin after the model's 120-day burn-in", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The Track Record's row, in months. <bookmark mark='a'/> Research: a Sharpe ratio of "
            f"{r['sharpe']:.2f}, with a standard error of {r['sharpe_se']:.2f} over {r['n']} months. Sealed years: "
            f"{h['sharpe']:.2f}, with a volatility of {100 * h['vol']:.0f} percent a year where ten was intended. The "
            "row is recorded as it is."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def diagnose(self, e):
        dg = e["diag"]
        names = [n.replace("USDT", "") for n in dg["low_vol_coins"]]
        s = dg["var_share_low"]
        bar_w = 9.0
        low = Rectangle(width=bar_w * s, height=0.8, fill_color=BAD, fill_opacity=0.8, stroke_width=0)
        rest = Rectangle(width=bar_w * (1 - s), height=0.8, fill_color=GREY_B, fill_opacity=0.8, stroke_width=0)
        bar = VGroup(low, rest).arrange(RIGHT, buff=0).move_to(UP * 0.8)
        l1 = label(rf"{100 * s:.0f}\% of the variance: {', '.join(names)}", font_size=20, color=BAD).next_to(bar, UP, buff=0.2)
        l1.align_to(bar, LEFT)
        txt = wrapped_label(rf"positions in coins whose 60-day volatility had fallen below 0.5\% a day, on "
                            rf"{dg['days_affected']} of {comma(dg['n_days'])} days; the rest of the book: a Sharpe ratio of "
                            rf"{dg['sr_rest']:.2f} (a diagnosis, not a new strategy: the holdout has been seen)", 11.0, 19,
                            GREY_A).next_to(bar, DOWN, buff=0.7)
        head = label(r"The diagnosis, on the registered rule exactly as it was", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The diagnosis, run on the registered rule exactly as it was. <bookmark mark='a'/> Split each day's profit "
            "and loss by coin. On "
            f"{dg['days_affected']} days out of {dg['n_days']:,}, the book held coins whose recent volatility had "
            "fallen almost to zero. Almost all of them were the last two months of 2025, when USDe, a dollar-pegged "
            "stablecoin, traded enough to enter the universe; CVC and FTT each had a single near-frozen day. Those "
            f"positions carried {100 * s:.0f} percent of the variance. "
            f"<bookmark mark='b'/> The rest of the book earned a Sharpe ratio of {dg['sr_rest']:.2f}. That number is a "
            "diagnosis, not a result: the sealed years have now been seen, and a repaired rule would be a new trial, on "
            "data that is no longer sealed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(low, LEFT), FadeIn(l1))
            self.play(GrowFromEdge(rest, LEFT))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def why_it_failed(self):
        rows = [cmath(r"x_i", r"=", r"\frac{\alpha_i}{\gamma\,\sigma_i^2}", font_size=42, colors={r"\sigma_i^2": BAD}),
                cmath(r"\sigma_i", r"\to", r"0\quad\Rightarrow\quad x_i \to \infty", font_size=38, colors={r"\infty": BAD}),
                cmath(r"r_i", r":", r"\text{one de-peg, delisting or unfreeze}", font_size=32)]
        whys = [why(r"the Markowitz position for a diagonal risk model, which the aim portfolio scales"),
                why(r"a coin that stops trading, or a stablecoin, has a forecast variance near zero, and the rule takes a "
                    r"position without limit"),
                why(r"the variance is near zero only until it is not: the loss arrives in one day, in a position the risk "
                    r"model said was riskless")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why. <bookmark mark='a'/> The rule divides each forecast by the asset's forecast variance. "
            "<bookmark mark='b'/> A stablecoin, or a coin that has stopped trading, has a variance near zero, and the "
            "rule takes a position with no limit. In the research years not one eligible coin was that calm, so the "
            "flaw could not show. <bookmark mark='c'/> And the variance is near zero only until it is not. "
            "This is the quant quake in miniature: the risk model said the position was riskless."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def rules(self):
        cards = VGroup(
            desk_question(r"a floor under every variance", r"no asset's forecast risk below a minimum, set from the "
                          r"asset class, never from the asset's own recent history alone", width=12.4, font_size=19),
            desk_question(r"limits that do not depend on the model", r"position caps as a share of the book and of "
                          r"daily volume, so a model error cannot become a position without bound", width=12.4, font_size=19),
            desk_question(r"a universe that knows what assets are", r"stablecoins, pegged and halted instruments "
                          r"excluded by rule, before any signal sees them", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What the House changes for every future rule (no trial: not a strategy)", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What the House changes, for every future rule, and charges as no trial because it is not a strategy. "
            "<bookmark mark='a'/> A floor under every forecast variance, set from the asset class. "
            "<bookmark mark='b'/> Position limits that do not depend on the model at all, as a share of the book and of "
            "daily volume. <bookmark mark='c'/> And a universe that knows what its assets are: pegged and halted "
            "instruments removed before any signal sees them."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"after seeing this result, the desk adds a variance floor and re-runs 2021--25. Its Sharpe is 0.4. "
                       r"What may the Track Record say about that number?")
        with self.voiceover(
            "Pause and predict. After seeing this result, a desk adds a variance floor and re-runs 2021 to 2025. The "
            "Sharpe ratio is point four. What may the Track Record say about that number?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
