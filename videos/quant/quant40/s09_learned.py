from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import (
    DATA_C,
    GOOD,
    MODEL_C,
    PART,
    TAIL_C,
    VAR_C,
    load,
)

SHOW = {"caviar": r"CAViaR (SAV)", "network": r"quantile network", "gjr_fhs": r"filtered HS (GJR-GARCH)",
        "hs": r"historical simulation"}


class Learned(VoiceoverScene):
    def construct(self):
        L = load("learned")
        self.card(L)
        self.pinball()
        self.caviar(L)
        self.network()
        self.results(L)
        self.path(L)
        self.dm(L)
        self.why_not()
        self.better()
        self.question()

    def card(self, L):
        m = L["models"]
        c = chapter_card(8, r"Learned risk", r"Can a model trained on the quantile beat one built from volatility?", part=PART)
        with self.voiceover(
            "Chapter eight, and the answer to the pause: no. On the thirty years after nineteen ninety, the network's "
            f"pinball loss was {m['network']['pinball']:.2f} against the GARCH-filtered forecast's "
            f"{m['gjr_fhs']['pinball']:.2f}, and it was exceeded on {100 * m['network']['rate']:.2f} percent of days, "
            "which Kupiec's test rejects. A learned model of the quantile had to rediscover volatility clustering, and "
            "did so less well than the model built on it."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pinball(self):
        rows = [cmath(r"\ell_\tau(q, r)", r"=", r"(\mathbf 1\{r < q\} - \tau)(q - r)", font_size=42, colors={r"\ell_\tau(q, r)": VAR_C}),
                cmath(r"\arg\min_q \mathbb E\,\ell_\tau(q, R)", r"=", r"F_R^{-1}(\tau)", font_size=40),
                cmath(r"\tau = 1\%", r":", r"\text{VaR}_{99\%} = -q", font_size=40)]
        whys = [why(r"the pinball, or check, loss: a penalty that tilts against being on the wrong side"),
                why(r"its expected value is minimised by the true quantile (proved in the research chapter)"),
                why(r"so any model of the return quantile can be trained, and compared, by its average pinball loss")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "How to train a quantile. <bookmark mark='a'/> The pinball loss penalises a forecast tau on one side and one "
            "minus tau on the other. <bookmark mark='b'/> Its expected value is minimised by the true quantile, as the "
            "research chapter proves. <bookmark mark='c'/> So any model of tomorrow's one percent quantile can be fitted, "
            "and compared with others, by its average pinball loss."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def caviar(self, L):
        b = L["beta"]
        rows = [cmath(r"q_t", r"=", r"\beta_0 + \beta_1 q_{t-1} + \beta_2 |r_{t-1}|", font_size=44, colors={r"q_t": MODEL_C}),
                cmath(r"\hat\beta_1,\ \hat\beta_2", r"=", rf"{b[1]:.3f},\ {b[2]:.3f}", font_size=40),
                cmath(r"\text{fit}", r":", r"\min_\beta \textstyle\sum_t \ell_{0.01}(q_t, r_t)", font_size=40)]
        whys = [why(r"Engle and Manganelli's CAViaR (2004): the quantile itself follows an autoregression, here the "
                    r"symmetric absolute value form"),
                why(r"fitted to 1926--1990: today's quantile keeps 86\% of yesterday's and moves 0.43 for each unit of "
                    r"yesterday's absolute return"),
                why(r"no distribution assumed at all: the model is fitted straight to the quantile")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Robert Engle and Simone Manganelli's CAViaR. <bookmark mark='a'/> The quantile itself follows an "
            "autoregression on yesterday's quantile and yesterday's absolute return. <bookmark mark='b'/> Fitted to "
            f"nineteen twenty-six to ninety, it keeps {100 * b[1]:.0f} percent of yesterday's quantile. "
            "<bookmark mark='c'/> No distribution is assumed: it is fitted straight to the pinball loss."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def network(self):
        rows = [cmath(r"x_t", r"=", r"(\sigma^{\text{EWMA}}_t,\ |r_{t-1}|,\ \overline{|r|}_5,\ \overline{|r|}_{22},\ r^-_{t-1})",
                      font_size=34),
                cmath(r"q_t", r"=", r"w_2^\top \tanh(W_1 x_t + b_1) + b_2", font_size=38, colors={r"q_t": TAIL_C}),
                cmath(r"\text{train}", r":", r"\text{Adam on the pinball loss, 1926--1990}", font_size=36)]
        whys = [why(r"five features known the evening before: volatility, yesterday's move, short and longer averages "
                    r"of absolute returns, and yesterday's loss"),
                why(r"sixteen hidden units: small, because a 1\% quantile sees only about 160 tail days a decade"),
                why(r"then frozen and tested on 1991--2020, with GJR-filtered HS refitted as it would have been")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And a quantile network. <bookmark mark='a'/> Five features known the evening before: volatility, "
            "yesterday's move, short and long averages of absolute returns, and yesterday's loss. <bookmark mark='b'/> "
            "Sixteen hidden units, kept small, because a one percent quantile sees only a few hundred tail days a "
            "decade. <bookmark mark='c'/> Trained on the pinball loss to nineteen ninety, then frozen, and tested on the "
            "thirty years after."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def results(self, L):
        hx = [-3.8, -0.8, 1.4, 3.4, 5.4]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"1991--2020, 1\% quantile", r"pinball, bp",
                                                                         r"exceeded", r"Kupiec $p$", r"indep.\ $p$")])
        tab = VGroup(head)
        best = min(L["models"], key=lambda k: L["models"][k]["pinball"])
        for k in ("gjr_fhs", "caviar", "network", "hs"):
            x = L["models"][k]
            tab.add(VGroup(label(SHOW[k], font_size=18, color=GOOD if k == best else WHITE),
                           MathTex(f"{x['pinball']:.2f}", font_size=26, color=GOOD if k == best else WHITE),
                           MathTex(rf"{100 * x['rate']:.2f}\%", font_size=24), MathTex(f"{x['kupiec_p']:.3f}", font_size=24),
                           MathTex(f"{x['ind_p']:.3f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        m = L["models"]
        with self.voiceover(
            "The test. <bookmark mark='a'/> The GARCH-filtered forecast has the lowest pinball loss, "
            f"{m['gjr_fhs']['pinball']:.2f}, with exceptions on {100 * m['gjr_fhs']['rate']:.2f} percent of days. "
            f"<bookmark mark='b'/> CAViaR comes close, {m['caviar']['pinball']:.2f}, and passes both backtests. "
            f"<bookmark mark='c'/> The network is worse, {m['network']['pinball']:.2f}, exceeded too often; and plain "
            f"historical simulation, {m['hs']['pinball']:.2f}, is far behind them all."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def path(self, L):
        y = L["y2008"]
        dd = np.asarray(y["d"], int)
        t = (dd // 10000 - 2008) + ((dd // 100) % 100 - 1) / 12 + (dd % 100) / 365
        r = 100 * np.asarray(y["r"], float)
        g = axes([2008, 2010], [-12, 12], x_length=8.2, y_length=4.2, xlabel=r"2008--2009, daily", ylabel=r"return and "
                 r"1\% quantile forecasts, \%", xticks=[2008, 2009, 2010], yticks=[-10, -5, 0, 5, 10], font_size=14)
        g.move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, max(min(v, 12), -12)), stroke_width=1.5, color=DATA_C,
                             stroke_opacity=0.5) for x, v in zip(t, r)])
        cs = [curve(ax, t, np.clip(100 * np.asarray(y[k], float), -12, 12), c, stroke_width=2.5)
              for k, c in (("gjr", VAR_C), ("caviar", MODEL_C), ("network", TAIL_C))]
        leg = legend([(VAR_C, r"filtered HS (GJR)"), (MODEL_C, r"CAViaR"), (TAIL_C, r"network")], font_size=16)
        leg.to_corner(DR, buff=0.5)
        with self.voiceover(
            "Through the crisis. <bookmark mark='a'/> All three forecasts fall with the returns as volatility rises in "
            "September twenty oh eight. <bookmark mark='b'/> The network reacts most slowly and recovers too fast: it "
            "learned the average speed of volatility from the past, while GARCH's filter reacts to each day as it comes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cs[0]), Create(cs[1]))
            vo.wait_until("b")
            self.play(Create(cs[2]))
        self.wait(0.4)
        self.clear_scene()

    def dm(self, L):
        a, b = L["dm_net_vs_gjr"], L["dm_cav_vs_gjr"]
        rows = [cmath(r"\text{network} - \text{GJR}", r":", rf"t = {a['t']:.2f},\ p = {a['p']:.3f}", font_size=38, colors={r"\text{network} - \text{GJR}": TAIL_C}),
                cmath(r"\text{CAViaR} - \text{GJR}", r":", rf"t = {b['t']:.2f},\ p = {b['p']:.3f}", font_size=38, colors={r"\text{CAViaR} - \text{GJR}": MODEL_C})]
        whys = [why(r"Diebold and Mariano's test on the daily pinball losses (Part 7), with autocorrelation-robust errors"),
                why(r"both learned models lose, but neither by enough to be rejected at 5\%: thirty years of 1\% "
                    r"quantiles barely separate good models")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Is the difference real? <bookmark mark='a'/> Diebold and Mariano's test on the daily pinball losses: the "
            f"network against GARCH, a t of {a['t']:.1f}; CAViaR, {b['t']:.1f}. <bookmark mark='b'/> Both lose, but "
            "neither is rejected at five percent. Thirty years of one percent quantiles are barely enough to tell good "
            "models apart, which is itself the lesson of this chapter and of Chapter three."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def why_not(self):
        cards = VGroup(
            desk_question(r"the structure is already known", r"daily risk is mostly volatility clustering and leverage, "
                          r"which GJR-GARCH builds in with three parameters", width=12.4, font_size=19),
            desk_question(r"tail data are scarce", r"a 1\% quantile is informed by about 650 tail days in 65 years of "
                          r"training: few enough to overfit even a small network", width=12.4, font_size=19),
            desk_question(r"the world shifted", r"the features' relation to the tail changed after 1990; a filter that "
                          r"re-estimates adapts, a frozen network does not", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it lost. <bookmark mark='a'/> The structure is already known: daily risk is mostly volatility clustering "
            "and asymmetry, which GJR-GARCH builds in with a handful of parameters. <bookmark mark='b'/> Tail data are "
            "scarce: about six hundred and fifty tail days in sixty-five years of training. <bookmark mark='c'/> And the "
            "world shifted after nineteen ninety; a filter that re-estimates adapts, a frozen network does not."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def better(self):
        cards = VGroup(
            desk_question(r"better inputs", r"implied volatility (Part 12's VIX, from 1990) and intraday realised "
                          r"measures (Part 7's HAR) carry information daily returns do not", width=12.4, font_size=19),
            desk_question(r"learn the residual", r"let a network adjust a GARCH forecast, rather than replace it: the "
                          r"structure kept, the remainder learned", width=12.4, font_size=19),
            desk_question(r"score the pair", r"train VaR and ES together with the joint score of the research chapter, "
                          r"so the tail beyond the quantile is learned too", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What would do better. <bookmark mark='a'/> Better inputs: implied volatility and intraday realised measures "
            "carry information daily returns do not. <bookmark mark='b'/> Learning the residual: let a network adjust a "
            "GARCH forecast rather than replace it. <bookmark mark='c'/> And scoring VaR and ES together, with the joint "
            "score the research chapter derives."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a 10-day 97.5\% ES of \$11m is computed for a large-cap equity book. Under FRTB a credit-spread "
                       r"book with the same 10-day ES must be held for 40 days. What capital does the rule imply for it?")
        with self.voiceover(
            "Pause and predict. A ten-day ninety-seven and a half percent expected shortfall of eleven million dollars is "
            "computed for a large-cap equity book. Under Basel's FRTB, a credit-spread book with the same ten-day "
            "shortfall is assumed to take forty days to exit. What does the rule imply for it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
