from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, ask, comma, fit_right, illustration, load


class Toolkit(VoiceoverScene):
    def construct(self):
        t = load("toolkit")
        self.card()
        self.bars(t)
        self.fracdiff(t["fracdiff"])
        self.barrier()
        self.meta(t["meta"])
        self.unique(t["uniqueness"])
        self.question()

    def card(self):
        c = chapter_card(12, r"The practitioner's toolkit", r"Which of the tricks pay for themselves?", lit=(2018,),
                         part=PART)
        with self.voiceover("Chapter twelve. Marcos Lopez de Prado's toolkit for machine learning in finance, each tool "
                            "tested against the simple thing it replaces."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bars(self, t):
        e = np.linspace(-6, 6, 61)
        c = (e[:-1] + e[1:]) / 2
        panels = VGroup()
        for k, title, col in (("time", r"daily bars", LINEAR), ("dollar", r"dollar bars", TREE)):
            h = np.asarray(t[k]["hist"], float)
            h = h / h.sum() / (e[1] - e[0])
            top = 0.6
            g = axes([-6, 6], [0, top], x_length=5.4, y_length=3.0, xlabel=r"standardised return", ylabel=r"density",
                     xticks=[-6, -3, 0, 3, 6], yticks=[], font_size=12)
            ax = g.ax
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, min(v, top))[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=0.75).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, min(v, top))[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
            xs = np.linspace(-6, 6, 200)
            nrm = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), WHITE, stroke_width=2)
            cap = VGroup(label(title, font_size=20, color=col),
                         MathTex(rf"\text{{excess kurtosis}}\ {t[k]['kurt']:.1f}", font_size=22)).arrange(RIGHT, buff=0.3)
            panels.add(VGroup(cap, VGroup(g, bars, nrm)).arrange(DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        foot = wrapped_label(rf"Bitcoin, 2018--2020: {comma(t['time']['n'])} daily closes against the same number of dollar "
                             rf"bars, each closing once an average day's traded value has changed hands (from 0 to "
                             rf"{t['bars_per_day']['max']} bars a day). White: the normal. Squared returns still cluster "
                             rf"(autocorrelation {t['dollar']['ac_sq']:.2f} against {t['time']['ac_sq']:.2f}): sampling by "
                             r"activity tames the tails, not the volatility clustering", 12.4, 16, GREY_A).to_edge(DOWN, buff=0.35)
        foot2 = None
        head = label(r"Tool 1: the clock", font_size=30).to_edge(UP, buff=0.45)
        with self.voiceover(
            "First, the clock. Prices are usually sampled at fixed times, a close every day. But markets do not do "
            "business at a fixed rate. <bookmark mark='a'/> Lopez de Prado's information-driven bars close each time a "
            "fixed amount of money has traded instead, so a busy day has many bars and a quiet one none. "
            "<bookmark mark='b'/> On Bitcoin from 2018 to 2020, with as many dollar bars as there were days, the "
            "returns are much closer to normal: an excess kurtosis of eight instead of twenty-two. The extreme days are spread over "
            "several bars. But the squared returns still cluster, more than before. Sampling by activity tames the "
            "tails; it does not remove volatility clustering, and the next model still has to handle it."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.add(illustration(r"Binance BTCUSDT hourly; the House's \texttt{ml.dollar\_bars}", corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def fracdiff(self, f):
        ds, adf, cor = np.asarray(f["d"]), np.asarray(f["adf"]), np.asarray(f["corr"])
        g = axes([0, 1], [-24, 1], x_length=6.0, y_length=4.0, xlabel=r"differencing order $d$",
                 ylabel=r"ADF statistic", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[-20, -10, 0], font_size=13).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        la = curve(ax, ds, adf, NET, stroke_width=3)
        crit = DashedLine(ax.c2p(0, f["crit"]), ax.c2p(1, f["crit"]), color=HURDLE, stroke_width=2)
        g2 = axes([0, 1], [0, 1.05], x_length=4.8, y_length=4.0, xlabel=r"differencing order $d$",
                  ylabel=r"correlation with the price", xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0], font_size=13).to_edge(
            RIGHT, buff=0.6).shift(DOWN * 0.3)
        lc = curve(g2.ax, ds, cor, COIN, stroke_width=3)
        k = int(np.flatnonzero(adf < f["crit"])[0])
        dot1 = Dot(ax.c2p(ds[k], adf[k]), color=GOOD, radius=0.08)
        dot2 = Dot(g2.ax.c2p(ds[k], cor[k]), color=GOOD, radius=0.08)
        rows = [cmath(r"(1 - L)^d x_t", r"=", r"\textstyle\sum_{k \ge 0} w_k\, x_{t-k},\quad w_k = -w_{k-1}\frac{d - k + 1}{k}",
                      font_size=32, colors={r"(1 - L)^d x_t": NET})]
        rows[0].to_edge(UP, buff=0.4)
        foot = wrapped_label(rf"Bitcoin's log price, daily, 2018--2020. At $d = {ds[k]:.1f}$ the series passes the "
                             rf"Dickey--Fuller test (gold: the 5\% critical value) and still has a correlation of "
                             rf"{cor[k]:.2f} with the price; the ordinary return ($d = 1$) keeps {cor[-1]:.2f}",
                             12.0, 17, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Second, memory. A price is not stationary, so models are usually fed returns, which are, but which forget "
            "the level entirely. <bookmark mark='a'/> Fractional differencing takes a fractional power of the difference "
            "operator: an infinite weighted sum of past prices whose weights die away. Zero is the price, one is the "
            "return, and in between lie series that are stationary but remember where the price has been. "
            "<bookmark mark='b'/> On Bitcoin's log price, the Dickey-Fuller test already rejects a unit root at d of "
            "three tenths, where the series still has a correlation of point nine two with the price. The daily return "
            "keeps point zero nine. Whether a model can use that memory is an empirical question each time; the tool "
            "only makes it available."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(g), FadeIn(g2), Create(crit))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(la), Create(lc), run_time=2)
            self.play(FadeIn(dot1), FadeIn(dot2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def barrier(self):
        rng = np.random.default_rng(4)
        P = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.02, 40)))
        g = axes([0, 39], [P.min() * 0.95, P.max() * 1.08], x_length=8.0, y_length=4.0, xlabel=r"days",
                 ylabel=r"price", xticks=[], yticks=[], font_size=14).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        line = curve(ax, np.arange(40), P, COIN, stroke_width=3)
        i0, h = 8, 20
        up, dn = P[i0] * 1.08, P[i0] * 0.92
        box = VGroup(Line(ax.c2p(i0, up), ax.c2p(i0 + h, up), color=GOOD, stroke_width=2.5),
                     Line(ax.c2p(i0, dn), ax.c2p(i0 + h, dn), color=BAD, stroke_width=2.5),
                     Line(ax.c2p(i0 + h, dn), ax.c2p(i0 + h, up), color=HURDLE, stroke_width=2.5))
        hit = int(np.flatnonzero((P[i0 + 1:i0 + h + 1] >= up) | (P[i0 + 1:i0 + h + 1] <= dn))[0]) + i0 + 1 if \
            np.any((P[i0 + 1:i0 + h + 1] >= up) | (P[i0 + 1:i0 + h + 1] <= dn)) else i0 + h
        dot = Dot(ax.c2p(hit, P[hit]), color=GOOD if P[hit] >= up else (BAD if P[hit] <= dn else HURDLE), radius=0.09)
        side = VGroup(label(r"upper: take profit $(+1)$", font_size=18, color=GOOD),
                      label(r"lower: stop loss $(-1)$", font_size=18, color=BAD),
                      label(r"vertical: time's up (the sign then)", font_size=18, color=HURDLE),
                      wrapped_label(r"barriers set in units of recent volatility, so a label means the same in calm and "
                                    r"wild markets. Lopez de Prado (2018), ch. 3", 3.4, 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Third, labels. A model is only as good as the question it is trained to answer, and 'was the return over "
            "the next ten days positive?' is not the question a trader faces. <bookmark mark='a'/> The triple-barrier "
            "label asks instead which of three things happens first: the price rises far enough to take profit, falls "
            "far enough to stop out, or time runs out. The barriers are set in units of recent volatility, so a label "
            "means the same thing in a calm market and a wild one, and it matches how positions are actually managed."
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(side), run_time=1.5)
            self.play(FadeIn(dot, scale=1.5))
        self.add(illustration(r"illustration: a simulated path"))
        self.wait(0.4)
        self.clear_scene()

    def meta(self, m):
        rows = VGroup(
            MathTex(r"\text{primary: the side}\ \ s_t = \operatorname{sign}(P_t / P_{t-20} - 1)", font_size=30, color=MOM),
            MathTex(r"\text{secondary: }\ \Pr(\text{the bet hits its profit barrier} \mid \text{features}) > \tfrac12 ?",
                    font_size=30, color=TREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.6)
        hx = [-3.6, 1.0, 4.4]
        head = VGroup(label(r"Bitcoin, held-out period", font_size=18, color=GREY_B), label(r"every bet", font_size=18, color=MOM),
                      label(r"meta-labelled", font_size=18, color=TREE))
        data = [(r"bets taken", r"100\%", rf"{100 * m['taken']:.0f}\%"),
                (r"precision (barrier hit in the bet's favour)", rf"{100 * m['precision_primary']:.0f}\%",
                 rf"{100 * m['precision_meta']:.0f}\%"),
                (r"mean per opportunity, \%", rf"{100 * m['mean_primary']:.1f}", rf"{100 * m['mean_meta']:.1f}"),
                (r"its standard deviation, \%", rf"{100 * m['sd_primary']:.1f}", rf"{100 * m['sd_meta']:.1f}"),
                (r"mean / sd", rf"{m['mean_primary'] / m['sd_primary']:.2f}", rf"{m['mean_meta'] / m['sd_meta']:.2f}")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(a, font_size=18, color=GREY_A), MathTex(b, font_size=24),
                                                 MathTex(c, font_size=24)) for a, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.0 - 0.6 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.0, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(r"Bitcoin daily, the last third of 2018--2020 held out; secondary model: the House's boosted "
                             r"trees on volatility, the last day's return and the side. Meta-labelling raised precision and cut "
                             r"risk; the reward per unit of risk barely moved", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Fourth, meta-labelling: separate deciding the side of a bet from deciding its size. <bookmark mark='a'/> "
            "A primary model picks the side, here simply twenty-day momentum. A secondary model, trained on the "
            "triple-barrier outcomes, decides only whether to take each bet. <bookmark mark='b'/> On Bitcoin's last "
            "year of research data, the secondary model skipped about a third of the bets, and the precision of those "
            "it kept rose from sixty-one to sixty-six percent. The risk fell with it. But the reward per unit of risk "
            "hardly moved. Meta-labelling made a smaller, more accurate strategy here, not a better one, which is the "
            "usual result for a tool sold as an improvement: measure it."
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def unique(self, u):
        cards = VGroup(
            desk_question(r"overlapping labels are not independent", rf"each day's ten-day label shares most of its days "
                          rf"with its neighbours: {comma(u['n'])} labels carry the information of about "
                          rf"{u['effective']:.0f} independent ones (average uniqueness {u['mean']:.2f})", width=12.2,
                          font_size=20),
            desk_question(r"so weight them, and say so", r"weighting each label by its uniqueness keeps a model from "
                          r"treating a ten-day move as ten separate lessons; the effective count is the honest sample "
                          r"size for every standard error", width=12.2, font_size=20),
            desk_question(r"the rule for every tool here", r"adopt it when, tested against the simple version on data "
                          r"it has not seen, it pays for its complexity", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Last, the sample size itself. <bookmark mark='a'/> Each day's ten-day label shares most of its days with its "
            "neighbours: a thousand and eighty-six labels carry about as much information as a hundred and twenty-five "
            "independent ones. <bookmark mark='b'/> Weighting each label by its uniqueness keeps a model from treating "
            "one ten-day move as ten separate lessons, and the effective count is the honest sample size for every "
            "standard error. <bookmark mark='c'/> And the rule for every tool in this chapter: adopt it when, against "
            "the simple version, on data it has not seen, it pays for its complexity."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a secondary model doubles the precision of your bets but takes only one bet in ten. When is that "
                r"better than taking every bet, and how would you decide before trading?")
        with self.voiceover(
            "Pause and predict. A secondary model doubles the precision of your bets, but takes only one bet in ten. "
            "When is that better than taking every bet, and how would you decide before trading?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
