from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause, real_data


class MarketMaker(VoiceoverScene):
    def construct(self):
        fl = load("flow")
        self.card()
        self.game()
        self.gm()
        self.derive()
        self.rain(fl)
        self.markout(fl)

    def card(self):
        c = chapter_card(8, r"Making a market: the spread", r"Who are you trading with?", lit=(1985,), part=PART)
        with self.voiceover("Chapter eight. Making a market: the spread, and who you trade with."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def game(self):
        q = desk_question(r"Make me a market on the roll of a die. \ldots Now I tell you the roll is even. Make me a new "
                          r"market.", width=10.6, font_size=28).to_edge(UP, buff=0.6)
        rows = [cmath(r"\mathbb{E}[X]", r"=", r"3.5\quad\Rightarrow\quad 3.3\ \text{bid},\ 3.7\ \text{ask}", font_size=36,
                      colors={r"\mathbb{E}[X]": OPT}),
                cmath(r"\mathbb{E}[X \mid \text{even}]", r"=", r"4\quad\Rightarrow\quad 3.8\ /\ 4.2", font_size=36,
                      colors={r"\mathbb{E}[X \mid \text{even}]": ALT})]
        whys = [why(r"quote around fair value, wide enough to be paid for the risk: the spread is the market maker's "
                    r"income and its insurance"),
                why(r"new information moves the fair value; and the person asking may know more than you, so after a "
                    r"trade, fair value moves against you: adverse selection (Glosten and Milgrom 1985)")]
        step = ladder(self, rows, whys, keep=2, top=0.9, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "The classic market-making interview game. Make me a market on the roll of a die. The expected roll is "
            "three and a half, so you quote around it: buy at three point three, sell at three point seven. The "
            "spread is your income, and your protection. <bookmark mark='a'/> Then the interviewer says: the roll is "
            "even. Your fair value jumps to four, and your market with it. The lesson is the one that rules every "
            "options desk: the person trading with you may know something, so after each trade the fair value tends "
            "to move against you. Lawrence Glosten and Paul Milgrom called it adverse selection in 1985."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gm(self):
        mu, n = 0.3, 24
        g = np.random.default_rng(118)
        trades = []
        for _ in range(n):  # the true value is high: informed traders buy; the rest buy or sell at random
            trades.append(1 if g.random() < mu else (1 if g.random() < 0.5 else -1))
        pi, path = 0.5, []
        for tr_ in trades:
            pb = pi * (mu + (1 - mu) / 2) + (1 - pi) * (1 - mu) / 2
            ask = pi * (mu + (1 - mu) / 2) / pb
            ps = pi * (1 - mu) / 2 + (1 - pi) * (mu + (1 - mu) / 2)
            bid = pi * (1 - mu) / 2 / ps
            path.append((pi, bid, ask))
            pi = ask if tr_ > 0 else bid
        path.append((pi, path[-1][1], path[-1][2]))
        gp = axes([0, n], [0, 1], x_length=7.0, y_length=3.8, xlabel=r"trades", ylabel=r"value: low 0, high 1",
                  xticks=[0, 8, 16, 24], yticks=[0, 0.5, 1], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = gp.ax
        tr = ValueTracker(0.0)
        xs = np.arange(n + 1)
        bid_l = tracing(ax, xs, [p_[1] for p_ in path], tr, QC.GAIN, stroke_width=3)
        ask_l = tracing(ax, xs, [p_[2] for p_ in path], tr, QC.LOSS, stroke_width=3)
        bel = always_redraw(lambda: VGroup(
            Rectangle(width=0.7, height=3.0 * at_index(np.array([p_[0] for p_ in path]), tr), stroke_width=0,
                      fill_color=QC.GAIN, fill_opacity=0.8).move_to([4.2, -1.9, 0], aligned_edge=DOWN),
            Rectangle(width=0.7, height=3.0 * (1 - at_index(np.array([p_[0] for p_ in path]), tr)), stroke_width=0,
                      fill_color=QC.LOSS, fill_opacity=0.8).move_to([5.3, -1.9, 0], aligned_edge=DOWN)))
        bl = VGroup(label(r"P(high)", font_size=20, color=QC.GAIN).move_to([4.2, -2.25, 0]),
                    label(r"P(low)", font_size=20, color=QC.LOSS).move_to([5.3, -2.25, 0]),
                    label(r"the market maker's belief", font_size=21, color=GREY_A).move_to([4.75, 1.6, 0]))

        def marks():
            k = int(tr.get_value())
            return VGroup(*[Triangle(fill_opacity=1, stroke_width=0, color=QC.GAIN if trades[i] > 0 else QC.LOSS)
                            .scale(0.07).rotate(0 if trades[i] > 0 else PI).move_to(ax.c2p(i + 0.5, 0.04))
                            for i in range(min(k, n))])
        mk = always_redraw(marks)
        leg = legend([(QC.LOSS, r"ask $= \mathbb{E}[V \mid \text{a buy}]$"), (QC.GAIN, r"bid $= \mathbb{E}[V \mid "
                      r"\text{a sell}]$")], font_size=18).next_to(gp, UP, buff=0.05).align_to(gp, LEFT)
        src = illustration(rf"illustration: {int(100 * mu)}\% of traders informed, the value is high")
        with self.voiceover(
            "Glosten and Milgrom's model, running. An asset is worth either nothing or one; only some traders know "
            "which. Here it is truly worth one, and thirty percent of the traders know it, so they always buy; the "
            "rest buy or sell at random. The market maker cannot tell them apart. <bookmark mark='a'/> So it quotes "
            "an ask equal to the value expected given that someone buys, and a bid equal to the value expected given "
            "a sell. Every trade is evidence: a buy pushes its belief up, a sell pushes it down. "
            "<bookmark mark='b'/> Trade by trade the belief climbs toward the truth, the quotes rise with it, and the "
            "spread narrows: once the market maker knows the value, there is nothing left to fear, and no spread. "
            "The spread is the price of not knowing who is on the other side."
        ) as vo:
            self.play(FadeIn(gp), FadeIn(bl), FadeIn(src), FadeIn(leg))
            self.add(bel)
            vo.wait_until("a")
            self.add(bid_l, ask_l, mk)
            self.play(tr.animate.set_value(n * 0.4), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(n), run_time=max(vo.remaining(1.0) - 0.3, 1.0), rate_func=linear)
        for m in (bel, bid_l, ask_l, mk):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\text{ask}", r"=", r"\mathbb{E}[V \mid \text{buy}] = \frac{\pi\,\big(\mu + \tfrac{1-\mu}{2}\big)\,V_H + "
                  r"(1-\pi)\,\tfrac{1-\mu}{2}\,V_L}{\Pr(\text{buy})}", font_size=32, colors={r"\text{ask}": QC.LOSS}),
            cmath(r"\text{ask} - \text{bid}", r"=", r"\mu\,(V_H - V_L)\qquad (\pi = \tfrac12)", font_size=36),
            cmath(r"\text{edge}", r"=", r"s\,(p - m_t),\qquad \text{markout}_h = s\,(p - m_{t+h}) + \Delta\,(I_{t+h} - "
                  r"I_t)", font_size=32),
            cmath(r"\text{adverse selection}", r"=", r"\text{edge} - \text{markout}", font_size=36),
        ]
        whys = [why(r"Bayes: a buy comes from every informed trader when the value is high, and from half the others"),
                why(r"substitute $\pi = \tfrac12$: the spread is the informed share times the uncertainty"),
                why(r"in the data: the maker's edge against the mark at the trade, and what is left $h$ later, the "
                    r"option marked again and the delta hedge counted"),
                why(r"what the informed took back (Huang and Stoll's decomposition of the spread)")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.6, buff=0.5, edge=6.9)
        with self.voiceover(
            "The algebra of it. The ask is the expected value given a buy, by Bayes' rule: buys come from all the "
            "informed traders when the value is high, and from half of the others either way. "
            "<bookmark mark='a'/> At even odds: the spread is the informed share times the uncertainty. <bookmark mark='b'/> To measure it on real "
            "trades, split it. The maker's edge is what it charged against fair value at the moment of the trade. "
            "The markout is what is left some time later, once the option is marked again and the delta hedge is "
            "counted. <bookmark mark='c'/> The difference is adverse selection."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rain(self, fl):
        r = np.asarray(fl["rain"])
        g = axes([-0.4, 0.4], [0, 1.0], x_length=7.2, y_length=4.6, xlabel=r"log-moneyness $\ln K/S$",
                 ylabel=r"years to expiry", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0, 0.25, 0.5, 0.75, 1],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        m = (np.abs(r[:, 0]) < 0.4) & (r[:, 1] < 365)
        r = r[m]
        dots = VGroup(*[Dot(ax.c2p(a, min(b / 365, 1.0)), radius=0.012 + 0.01 * min(np.sqrt(c_), 3),
                            color=YELLOW if s_ > 0 else QC.SPOT, fill_opacity=0.55) for a, b, s_, c_, _ in r])
        leg = legend([(YELLOW, r"taker buys"), (QC.SPOT, r"taker sells")], font_size=18).next_to(g, UP, buff=0.05).align_to(
            g, RIGHT)
        side = VGroup(
            label(rf"{fl['n']:,} trades on {fl['days']} Wednesdays".replace(",", "{,}"), font_size=22, color=GREY_A),
            label(rf"OTM calls: {100 * fl['otm call bought']:.0f}\% bought, {100 * fl['otm call sold']:.0f}\% sold",
                  font_size=20, color=YELLOW),
            label(rf"OTM puts: {100 * fl['otm put bought']:.0f}\% bought, {100 * fl['otm put sold']:.0f}\% sold",
                  font_size=20, color=QC.SPOT),
            wrapped_label(r"shares of all traded vega; the rest is in the money", 4.2, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        src = real_data(r"Deribit BTC option trades, 00:00--12:00 UTC; the dots: 4 June 2025")
        with self.voiceover(
            "Now real flow. Every Bitcoin option trade on Deribit during one Wednesday morning, falling into place on "
            "a plane of strike against expiry: gold when the taker bought, blue when the taker sold, larger for larger "
            "trades. <bookmark mark='a'/> Over "
            f"{fl['days']} Wednesdays of 2024 and 2025 that is {fl['n']:,} trades. By vega, takers bought and sold "
            "out-of-the-money calls in about equal measure, and the same for puts: the market maker's book is not "
            "one-sided."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.play(ShowIncreasingSubsets(dots), run_time=max(vo.until("a") - 0.3, 2.0), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3, run_time=2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def markout(self, fl):
        hz = [0, 5, 30, 60]
        c, cb = np.asarray(fl["curve"]), np.asarray(fl["curve_big"])
        top = max(c.max(), cb.max()) * 1.25
        g = axes([0, 60], [0, top], x_length=5.6, y_length=3.6, xlabel=r"minutes after the trade",
                 ylabel=r"maker's gain, vol points", xticks=[0, 5, 30, 60], yticks=[0, round(top / 2, 2)],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        la = curve(ax, hz, c, GAMMA, stroke_width=3.5)
        lb = curve(ax, hz, cb, ALT, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=GAMMA) for x, y in zip(hz, c)])
        leg = legend([(GAMMA, r"all trades"), (ALT, r"the largest 5\%")], font_size=17).next_to(g, UP, buff=0.05).align_to(
            g, RIGHT)
        kept = fl["kept_1h"]
        card = lab_card(r"markouts, in volatility points", [
            "def markouts(ts, sign, price, mark, index, delta, vega, horizons):",
            "    edge = sign * (price - mark) * index / vega",
            "    out = {'edge': edge}",
            "    for h in horizons:",
            "        k = np.searchsorted(ts, ts + h)",
            "        kk = np.minimum(k, len(ts) - 1)",
            "        dv = mark[kk] * index[kk] - price * index",
            "        dh = delta * (index[kk] - index)",
            "        out[h] = np.where(k < len(ts), -sign * (dv - dh) / vega, np.nan)",
            "    return out",
        ], source="explainer/quant/house/quoting.py", width=6.6, font_size=17).to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.3)
        lab = fl["lab"]
        cov = fl["coverage"]
        verdict = (rf"an hour later the maker keeps {100 * kept:.0f}\% of its edge: the rest went to traders who knew "
                   r"something")
        note_ = wrapped_label(rf"{verdict}; measured against Deribit's own mark price, on the {100 * cov[-1]:.0f}\% of "
                              r"trades with a later print", 5.8, 18, GREY_A).next_to(g, DOWN, buff=0.25).align_to(g, LEFT)
        pc = pause(r"Your quote is hit, and then the market moves against you. Was your spread too narrow, or too "
                   r"wide?", width=4.6, font_size=19, corner=DL)
        ksay = (f"An hour later it keeps about {100 * kept:.0f} percent of that: the rest went back to traders who knew "
                "where the price was going." if kept < 0.9 else
                f"An hour later it keeps {100 * kept:.0f} percent: adverse selection here is small.")
        with self.voiceover(
            "And the spread's split. Here is the House's markout function: the edge at the trade, then each later "
            "mark, with the delta hedge counted, in volatility points. <bookmark mark='a'/> Run on one day, then on "
            f"all of them. Against Deribit's own mark, the maker's average edge at the trade is {c[0]:.2f} volatility "
            f"points. <bookmark mark='b'/> Five minutes later, {c[1]:.2f}; half an hour, {c[2]:.2f}; an hour, "
            f"{c[3]:.2f}. {ksay} The largest trades pay a wider edge, {cb[0]:.2f}, and more of it goes back: an hour "
            f"later {cb[3]:.2f}. The market maker is right to charge them more. "
            "<bookmark mark='c'/> So, pause and predict: your quote is hit, and the market moves against you. Too "
            "narrow, or too wide? Narrow, if it happens every time: that is adverse selection, priced too cheaply."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"markouts(...)  # 4 June 2025: {lab['n']} trades",
                                 f"edge {lab['edge']:.2f}   5m {lab['300']:.2f}   30m {lab['1800']:.2f}   1h {lab['3600']:.2f}"],
                    font_size=17)
            self.play(FadeIn(g), FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(Create(la), FadeIn(dots[1:]), Create(lb), FadeIn(leg), run_time=2)
            self.play(FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()
