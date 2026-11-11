from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, VT_C
from videos.quant.quant32.illustrations import volatility_cases


class VolTarget(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.cases(volatility_cases())
        self.shock()
        self.optimizer()
        self.capital_structure()
        self.financing()
        self.literature()
        self.crowding()
        self.question()

    def card(self):
        c = chapter_card(3, r"Volatility targeting", r"When does a forecast risk budget become realised risk?", part=PART)
        with self.voiceover(
            "Chapter three. A volatility target specifies desired forecast risk, not a guaranteed realised "
            "outcome. We can derive exactly what the rule does under chosen forecasts, then ask what "
            "evidence is needed to assess its risk, return and trading consequences."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rule(self):
        rows = [
            cmath(r"x_t", r"=", r"\min\!\left(c,\frac{\sigma^*}{\hat\sigma_{t-1}}\right)", font_size=40),
            cmath(r"\operatorname{Var}_{t-1}(x_t r_t)", r"=", r"x_t^2\operatorname{Var}_{t-1}(r_t)", font_size=34),
            cmath(r"\sigma_{\rm scaled,t}", r"=", r"x_t\,\sigma_{\rm true,t}", font_size=38),
        ]
        whys = [
            why(r"exposure is known before the return; chosen target and cap, with a positive available forecast"),
            why(r"conditional on prior information, exposure is fixed; return units and forecast horizon must agree"),
            why(r"the target is reached only if the forecast is correct and the exposure cap does not bind"),
        ]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.25, buff=0.65, edge=6.8)
        with self.voiceover(
            "Hold the target divided by an available forecast, with a leverage cap. The forecast must be "
            "positive and known before the return being scaled. "
            "<bookmark mark='a'/> Conditional on that earlier information, exposure is fixed, so variance "
            "is multiplied by its square. Forecast and return horizons must use consistent units. "
            "<bookmark mark='b'/> Resulting conditional volatility is exposure times true conditional "
            "volatility. It equals the target only if the forecast is correct and the cap does not bind. "
            "A conventional annualised risk unit also differs from a guarantee about a whole year's "
            "realised path, especially when dependence, costs or financing change the account."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def cases(self, data):
        head = label(r"Chosen annualised risk cases: target 10\%, cap 3", font_size=29).to_edge(UP, buff=0.5)
        rows = VGroup(*[
            label(rf"forecast {100 * v['forecast']:.0f}\%, true {100 * v['realised']:.0f}\%: "
                  rf"exposure {v['exposure']:.1f}, scaled risk {100 * v['conditional_risk']:.0f}\%",
                  font_size=25, color=VT_C if i < 2 else BAD)
            for i, v in enumerate(data["cases"])
        ]).arrange(DOWN, buff=0.5)
        foot = wrapped_label(r"stipulated conditional SDs, not estimates or observed investment results",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Choose a ten percent target and a cap of three. A correct twenty percent forecast gives "
            "exposure one half and ten percent scaled risk. "
            "<bookmark mark='a'/> A correct ten percent forecast gives exposure one and the same risk. "
            "<bookmark mark='b'/> A correct two percent forecast would call for five times exposure, but "
            "the cap restricts it to three. Scaled risk is six percent, below the target. "
            "<bookmark mark='c'/> Finally let the forecast be ten percent while true risk is twenty. "
            "Exposure remains one, giving twenty percent risk. The target did not fail algebraically; "
            "the forecast was wrong. These stipulated cases distinguish a control rule, a binding limit "
            "and a forecasting error without attributing an outcome to a historical asset."
        ) as vo:
            for i, mark in enumerate(("a", "b", "c"), 1):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i]))
        self.clear_scene()

    def shock(self):
        lam, before, shock = 60 / 61, 0.10, -0.04
        after = math.sqrt(lam * before ** 2 + (1 - lam) * 252 * shock ** 2)
        next_x = 0.10 / after
        daily_units = r"\text{每日}" if zh() else r"{\rm daily}"
        rows = VGroup(
            MathTex(r"\hat v_t=\frac{60}{61}\hat v_{t-1}+\frac1{61}r_t^2", font_size=38),
            MathTex(r"\hat\sigma_{t-1}=10\%,\qquad r_t=-4\%\ " + daily_units, font_size=34),
            MathTex(rf"\hat\sigma_t={100 * after:.2f}\%,\qquad x_t=1,\quad x_{{t+1}}={next_x:.3f}", font_size=34),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen available prior forecast; daily second moments annualised by 252; "
                             r"the current shock changes the next exposure", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Forecast timing matters. The House EWMA uses a sixty-day centre of mass, so the decay "
            "coefficient is sixty over sixty-one. It accumulates squared returns: an uncentred second "
            "moment, which differs from variance when the conditional mean is material. "
            "<bookmark mark='a'/> Choose an available ten percent annual forecast and a daily "
            "shock of minus four percent. Today's exposure remains one; the shock has already happened. "
            f"<bookmark mark='b'/> After updating, the annualised forecast is {100 * after:.2f} percent "
            f"and the next exposure is {next_x:.3f}. A positive four percent shock gives the same "
            "squared-return update. This estimator alone is not a model of asymmetric price-volatility "
            "causality, and deleveraging afterward does not erase the initial loss."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def optimizer(self):
        rows = VGroup(
            MathTex(r"x_{\rm MV}=\frac{\mu_t}{\gamma\sigma_t^2}", font_size=40),
            MathTex(r"x_{\rm target}=\frac{\sigma^*}{\sigma_t}", font_size=40),
            MathTex(r"\mu_t=k\sigma_t^2\ \Longrightarrow\ x_{\rm MV}=\frac{k}{\gamma}", font_size=36),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"costless one-period conditional mean-variance reference; positive risk aversion "
                             r"and variance, no exposure constraints", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Risk targeting and utility optimisation answer different questions. In a costless one-period "
            "mean-variance model, optimal exposure is conditional expected excess return divided by "
            "risk aversion times conditional variance. "
            "<bookmark mark='a'/> Volatility targeting instead scales by inverse standard deviation. "
            "Even with constant expected return, inverse variance and inverse standard deviation differ. "
            "<bookmark mark='b'/> If expected excess return rises exactly in proportion to variance, "
            "the mean-variance optimum is constant. The volatility target would still vary. No universal "
            "Sharpe improvement follows from the scaling formula alone. We need a joint model or "
            "evidence about expected returns, risk forecasts, dependence and implementation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def capital_structure(self):
        rows = VGroup(
            MathTex(r"E=A-D,\qquad \sigma_E\approx\frac{A}{E}\sigma_A", font_size=38),
            MathTex(r"A=100,\ D=50,\ \sigma_A=10\%:\quad \sigma_E\approx20\%", font_size=32),
            MathTex(r"A=80,\ D=50,\ \sigma_A=10\%:\quad \sigma_E\approx26.67\%", font_size=32),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen local approximation with fixed locally riskless debt; omits default, "
                             r"option convexity and changes in asset risk", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "One proposed price-volatility mechanism is balance-sheet leverage. In a local approximation "
            "with fixed riskless debt, equity is assets minus debt and percentage volatility is "
            "asset volatility times assets over equity. "
            "<bookmark mark='a'/> Choose assets one hundred, debt fifty and asset volatility ten percent: "
            "equity volatility is about twenty percent. "
            "<bookmark mark='b'/> Let assets fall to eighty with debt and asset risk fixed. Equity "
            "is thirty, giving about twenty-six point six seven percent volatility. This is a conditional "
            "mechanism. Default risk, option convexity, changing asset volatility and news can also "
            "matter; it does not identify the sole cause of an empirical volatility spike."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def financing(self):
        rows = VGroup(
            MathTex(r"\text{cash weight}=1-x", font_size=38),
            MathTex(r"\text{extra funding spread cost}=s\,\max(x-1,0)", font_size=34),
            MathTex(r"x=3,\quad s=1\%:\quad \text{cost}=2\%\ {\rm of\ initial\ capital}", font_size=31),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen one-period excess-return convention; borrowing above the cash benchmark "
                             r"pays an additional spread; other trading and collateral costs omitted",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Low forecast volatility can call for borrowing. With risky exposure x, the cash weight "
            "is one minus x. A negative cash weight represents borrowing under this convention. "
            "<bookmark mark='a'/> When risky returns are already excess of a cash benchmark, an additional "
            "borrowing spread is charged to the amount above one. "
            "<bookmark mark='b'/> Choose exposure three and a one percent spread. The extra cost is "
            "two percent of starting capital for the period, separate from the benchmark already "
            "removed from excess returns. Actual margin, collateral remuneration, trading costs and "
            "funding limits can differ; a risk cap does not make those cash flows disappear."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def literature(self):
        cards = VGroup(
            desk_question(r"Moreira and Muir", r"volatility-managed factor evidence uses an inverse-variance "
                          r"construction, different from this inverse-SD EWMA rule", width=12.2, font_size=20),
            desk_question(r"Cederburg and coauthors", r"implementation and out-of-sample evaluation affect "
                          r"whether historical management gains are attainable", width=12.2, font_size=20),
            desk_question(r"Harvey and coauthors", r"results depend on assets and implementation; risk-asset "
                          r"findings are not a universal improvement", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "The literature asks empirical versions of these questions. Moreira and Muir study "
            "volatility-managed factors with an inverse-variance construction, different from our "
            "inverse-standard-deviation rule. "
            "<bookmark mark='a'/> Cederburg and coauthors examine implementation and out-of-sample "
            "performance: historical comparisons cannot automatically be treated as allocations "
            "an investor could have formed. "
            "<bookmark mark='b'/> Harvey and coauthors study targeting across asset groups. Their "
            "findings also require the stated assets, sample and implementation. Different designs "
            "need not agree, and a model identity cannot settle which net-return comparison will "
            "survive a properly specified independent evaluation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def crowding(self):
        rows = VGroup(
            MathTex(r"\hat\sigma:20\%\to40\%,\qquad x:0.5\to0.25", font_size=38),
            wrapped_label(r"shared risk signals can imply common desired reductions; actual net trades "
                          r"and market impact need additional evidence", 11.8, 25, HURDLE),
            wrapped_label(r"smoothing and turnover limits change both adjustment speed and retained "
                          r"risk; none is a free guarantee", 11.8, 24, GREY_A),
        ).arrange(DOWN, buff=0.7)
        self.play(FadeIn(rows[0]))
        with self.voiceover(
            "Common forecasts can produce common desired trades. With a ten percent target, a forecast "
            "rising from twenty to forty percent cuts desired exposure from one half to one quarter. "
            "<bookmark mark='a'/> Investors sharing the rule and similar assets can want to reduce "
            "together. Whether actual net selling moves prices depends on flows, offsetting orders, "
            "liquidity and other participants. The formula alone does not identify a cause of a named crash. "
            "<bookmark mark='b'/> Smoothing, slower rebalancing and turnover limits can moderate "
            "adjustment but also retain risk longer. Those choices need their own specification "
            "and evaluation, alongside liquidity reserves and financing constraints."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('\\sigma^\\star=10\\%,\\quad\\widehat\\sigma=10\\%,\\quad\\sigma_{\\rm true}=20\\%,\\quad c=3', font_size=34),
            MathTex('x=\\min(\\sigma^\\star/\\widehat\\sigma,c)', font_size=34),
            MathTex('\\sigma_{\\rm scaled}=|x|\\sigma_{\\rm true}', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Target 10\%, prior forecast 10\%, true conditional SD 20\%, cap 3. "
                       r"What exposure and conditional scaled risk follow?")
        with self.voiceover(
            "Pause and predict. The target is ten percent, the available forecast ten percent, "
            "true conditional standard deviation twenty percent, and the exposure cap three. "
            "What exposure is chosen, what conditional risk results, and which assumption "
            "would have been needed to reach the target?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
