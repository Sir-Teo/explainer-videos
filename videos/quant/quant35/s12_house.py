from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import micro as M
from videos.quant.quant35.common import BAD, DEALER_C, FLOW_C, GOOD, INF_C, PART, PRICE_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("dealer"), load("gm"), load("kyle"), load("flow"), None, load("vpin"),
                   load("discovery"))
        self.footprint(load("flow"))
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(11, r"Rule 35: know who is on the other side", r"What must the House know about a market "
                         r"before it trades there?", part=PART)
        self.add(c)
        with self.voiceover("Chapter eleven. The House's thirty-fifth rule is about the counterparty. Before any desk "
                            "trades in a market, it must know who it is likely to be trading with, and what its own "
                            "orders will tell them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, dl, g, k, f, m, v, d):
        rows = [(r"dealer inventory sd, without and with shading", rf"{dl['0.0']['inv_sd']:.0f},\ "
                 rf"{dl['0.05']['inv_sd']:.1f}", DEALER_C),
                ('GM, $\\mu=0.3$: capped pretrade crossing index', rf"{g['0.3']['to99']:.0f}", PRICE_C),
                (r"Kyle, continuous: insider's profit, simulated", rf"{k['bridge_profit']:.3f}", INF_C),
                (r"Bitcoin: $\lambda$ per \$1m, $R^2$ at 1 min and 1 hour", rf"{f['full']['lambda']:.2f};\ "
                 rf"{f['agg']['1']['r2']:.2f},\ {f['agg']['60']['r2']:.2f}", FLOW_C),
                (r"ETF comparison: frozen SPY input rejected", r"\text{unavailable}", BAD),
                ('VPIN: volatility / aggregate taker-window correlations', rf"{v['corr_rv']:.2f},\ {v['corr_true']:.2f}",
                 INF_C),
                (r"perpetual vs spot: return correlation; IS bound width", rf"{d['corr0']:.3f};\ {d['width']:.2f}", GOOD)]
        hx = [-2.4, 4.6]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.65 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The microstructure desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label('nine verified ordinary outputs: stipulated models and public Binance research; ETF original failed frozen SPY validation. No sealed strategy access, refresh or replacement backtest', 12.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.25)
        self.add(title, tab[0], foot)
        with self.voiceover(
            "The sheet records nine verified ordinary outputs and an explicit missing comparison. <bookmark mark='a'/> Inventory shading is a stipulated simulation; GM's crossing index is conditional and capped; continuous Kyle is approximated on a finite grid. Bitcoin flow slopes and fit statistics are descriptive. The ETF comparison is unavailable after frozen SPY validation failed. VPIN's two correlations compare different imbalance constructions, and information shares are model-dependent attribution ranges. This sheet neither identifies counterparties' private information nor approves a live trading system."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def footprint(self, f):
        lam = f["full"]["lambda"]
        rows = [cmath(r"\text{same-bar fitted change}", r"=", rf"10\hat\lambda={10*lam:.1f}\ \text{{bp}}", font_size=32),
                cmath(r"\text{separate permanent-linear model}", r":", r"p(q)-p_0=\lambda q", font_size=30),
                cmath(r"\text{mean execution shortfall}", r"=", r"\frac1Q\int_0^Q\lambda q\,dq=\frac{\lambda Q}{2}", font_size=30)]
        whys = [why(r"multiply a regression coefficient by chosen net flow for a fitted return, without causal interpretation"),
                why(r"this additional stipulated execution path is not estimated by the same-minute bins; ignore spread, fees, decay and outside flow"),
                why(r"the average price paid differs from the terminal price change. Neither number supplies an optimal real execution schedule")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(f"Separate a fit from an execution model. <bookmark mark='a'/> Ten million dollars times the saved regression slope gives {10*lam:.1f} basis points of fitted same-bar return. It is not an estimate of an added order's causal cost. <bookmark mark='b'/> Separately stipulate permanent linear impact as quantity accumulates, with no spread, fees, outside flow or decay. <bookmark mark='c'/> Integrating that assumed price path gives average shortfall lambda Q over two, half its terminal change. A concave minute-bin plot does not calibrate this path, prove cheaper slicing or determine the House's footprint.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Glosten--Milgrom quotes", M.gm_quotes, "pb_hi, pb_lo", 4, width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            "Chapter two's quotes in four lines. The probability of a buy when the value is high, and when it is low; "
            "Bayes' rule for the value given a buy, and given a sell; and the quotes are the expected values. Nothing in "
            "it knows about profit: zero profit is built into the definition."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Kyle's lambda from data", M.kyle_lambda, "r = np.asarray(ret, float)", 11, width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            'The exact regression source drops nonfinite paired observations, includes an intercept and computes a classical iid residual-based t-statistic and same-sample R squared. Dropping observations does not restore missing calendar minutes. This routine estimates an association; it supplies no robust standard errors, causal identification, parent-order cost or public-information variance decomposition.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"Hasbrouck's information shares", M.hasbrouck_is, "a_perp = np.array", 3,
                         extra=((M.hasbrouck_is, "for order in ((0, 1), (1, 0)):", 7),), width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            'The exact information-share code uses the complement of the fitted adjustment loadings and two Cholesky orderings of residual covariance. These give attribution bounds within a specified stable two-market cointegration model. The range is not a confidence interval, and a true causal share is not guaranteed to lie inside it when the statistical or structural assumptions fail.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"Kyle in continuous time, simulated", M.kyle_continuous, "for k in range(n):", 7, width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            'The unchanged Euler source approximates the bridge. Each step applies remaining-gap drift plus fresh independent noise. At the final step the old gap cancels but the new noise remains. Thus the last price differs from value by lambda sigma u square root of the time step times a standard Normal draw. The continuous theorem has exact endpoint learning; this finite-step helper does not. The code and financial algorithm are preserved, and the presentation states its numerical limit.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("compliance", "data")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{inventory\_dealer}, \texttt{gm\_quotes}, \texttt{gm\_simulate}", r"dealers"),
            (r"\texttt{kyle\_one}, \texttt{kyle\_multi}, \texttt{kyle\_continuous}", r"Kyle"),
            (r"\texttt{roll\_spread}, \texttt{amihud}, \texttt{kyle\_lambda}", r"liquidity"),
            (r"\texttt{bvc\_vpin}, \texttt{hasbrouck\_is}", r"toxicity, discovery"),
            (r"\texttt{data.binance\_klines}: \texttt{taker\_buy}", r"signed flow"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=20, color=QC.HOUSE), label(b_, font_size=20, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label('Proposed Rule 35: document counterparties and observations, separate flow association from identified execution cost, validate matching measurements and review order conduct in context. These requirements do not establish a deployed surveillance or execution system.', 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        self.add(chart, tab[0])
        with self.voiceover(
            "The library provides research tools. <bookmark mark='a'/> Dealer and Kyle models, liquidity proxies, bulk classification and information-share estimators have different assumptions. Public taker volume records trade side, not informed identity. <bookmark mark='b'/> Proposed Rule thirty-five asks a desk to document those distinctions, identify execution costs with suitable evidence and review its orders in context. The lesson does not establish deployed surveillance, counterparty identification or a trading approval. Failed input validation remains visible rather than being filled by an unverified result."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the research paper with Roll spreads", 'check the Roll assumptions against aligned quote evidence; a minimum tick does not establish the effective spread', width=12.0, font_size=25),
            desk_question(r"the vendor selling a toxicity signal", 'compare identical bucket definitions with inputs available at the decision time; associations do not identify informed probability', width=12.0, font_size=25),
            desk_question(r"the desk that must buy \$50m today", 'require identified costs, fees, fills and constraints; a descriptive regression slope alone cannot prescribe slicing', width=12.0, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Three review questions. <bookmark mark='a'/> For a daily spread paper, inspect identification assumptions and seek actual aligned quotes, rather than equating a tick with an effective spread. <bookmark mark='b'/> For a toxicity vendor, compare like-for-like bucket statistics and test inputs available at the decision time; correlation with volatility does not measure informed probability. <bookmark mark='c'/> For a large proposed order, require a causal cost model, fills, fees, participation constraints and information risk. A regression slope and a concave plot alone do not prescribe slicing."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
