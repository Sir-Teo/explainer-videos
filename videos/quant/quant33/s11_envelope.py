"""Evaluation protocol. No sealed cache, payload, score or registry operation."""
from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import PART, RES_C, COST_C, HURDLE


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.timing()
        self.accounting()
        self.constraint()
        self.costs()
        self.selection()
        self.precision()
        self.question()

    def panel(self, title, formula, explanation, narration):
        head = label(title, font_size=31).to_edge(UP, buff=0.45)
        eq = MathTex(formula, font_size=35, color=RES_C).move_to(UP * 0.8)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        text = wrapped_label(explanation, 11.7, 23).move_to(DOWN * 1.3)
        self.add(head, eq, text)
        with self.voiceover(narration):
            self.wait(0.3)
        self.clear_scene()

    def card(self):
        self.panel(
            r"10. An evaluation protocol", r"\text{research proxy}\ \longrightarrow\ \text{accounting}\ \longrightarrow\ \text{evaluation}",
            r"No sealed-year result is used here. The nine ordinary originals were verified once; their outputs do not certify an executable book.",
            "Chapter ten. What would turn a residual diagnostic into a credible strategy evaluation? The nine ordinary computations were each run once on their audited inputs. This chapter uses no sealed-year strategy output and makes no held-out performance claim. Instead, we specify what an evaluator would have to fix and measure: information timing, actual holdings, the cash account, execution costs and research selection. A frozen proxy can be reproducible and still answer a narrower question than an investable return series.")

    def timing(self):
        self.panel(
            r"Fix the information clock", r"\mathcal F_t\ \longrightarrow\ q_t\ \longrightarrow\ q_t^\top\Delta P_{t+1}",
            r"Specify the close or quote used, data release lags, fitting windows, rebalance time and the earliest executable order.",
            "Start with the information clock. A signal using today's close is observed after that close has formed; trading at that same close needs a justified order convention. The PCA fits use trailing information through the current close and apply their signal to the next return. That is a useful indexing convention, but not a complete execution model. The universe also uses complete histories over the research interval, so membership is retrospective. An independent evaluation would need a universe and decision rule available at each decision time.")

    def accounting(self):
        self.panel(
            r"Holdings and cash define wealth", r"V_t=q_t^\top P_t+B_t,\qquad \Delta V=q_t^\top\Delta P+\text{cash accrual}-\text{costs}",
            r"State shares, hedge holdings, dividends, borrow, financing and the gross-capital denominator. A fitted intercept is not an automatic cash flow.",
            "Next write the actual holdings and cash account. Wealth is shares times prices plus cash. Between rebalances it changes with price moves, distributions and financing; trading adds explicit execution charges. A fitted regression residual subtracts an intercept and factor returns, but only actual instruments produce cash flows. Normalize by the entire chosen capital convention, including the hedge. The stored residual proxy normalizes by active industry signals and subtracts a fitted intercept. Those conventions cannot be silently renamed full-book gross return.")

    def constraint(self):
        self.panel(
            r"Separate fitting constraints from prediction", r"\sum_{s=t-L+1}^{t}\hat u_s\simeq0\quad\text{when OLS includes an intercept}",
            r"A cumulative fitted residual ends near zero in each window. This finite-window bridge does not prove next-period profits.",
            "A particularly important diagnostic is the endpoint constraint. Least squares with an intercept makes the residuals sum to approximately zero over the fitting window. Their cumulative sum therefore ends near zero. An autoregression fitted to that path may see an appearance of mean reversion partly imposed by construction. The next residual can still contain useful information, but that is a separate empirical question. Evaluate returns from fixed information and actual holdings rather than treating the fitted bridge as proof of a trade.")

    def costs(self):
        self.panel(
            r"Reconstruct every trade", r"\mathrm{TC}_t=\sum_j c_{j,t}\,|\Delta q_{j,t}|\,P_{j,t}+\text{impact}_t",
            r"Net real hedge holdings; charge rescaling and final exits. The stored two-leg discrete-signal cost is a proxy with omissions.",
            "An execution audit reconstructs changes in every holding, including hedges. Netting can reduce separate hedge trades under linear costs, but it does not excuse missing transactions. In the stored algorithm, a changing number of active signals rescales continuing positions without including all those trades in turnover. A fully empty new book receives zero net profit, omitting its exit charge. Separate-hedge approximations can err the other way. The net effect is not known to be conservative. Keep the financial algorithm unchanged and state that limitation explicitly.")

    def selection(self):
        self.panel(
            r"Research choices remain research choices", r"\max_{i\le N}\hat S_i\quad\text{depends on }N\text{ and dependence across trials}",
            r"Nine configurations share data, features and costs. Counting choices documents search; it does not make correlated rules independent.",
            "Selection comes next. The eight threshold variants and the later mathematical-band configuration share the same research period and pipeline. Choosing a winner after comparing them spends information. A counter documents that search; it does not erase selection or make the rules independent. Any null maximum-Sharpe calculation must state its error model and dependence assumptions. This review adds no new market trial or registration. A future evaluation would require a fixed protocol and genuinely independent evidence appropriate to the question.")

    def precision(self):
        self.panel(
            r"Precision is conditional", r"\operatorname{se}(\hat S_{\rm annual})\approx T_{\rm years}^{-1/2},\qquad (2/0.3)^2\approx44.4",
            r"A low-Sharpe iid approximation needs decades. Serial dependence, nonnormality, selection and changing risk alter precision.",
            "Even an ideal clean return series can be imprecise. Under the simple independent-return approximation, the annual Sharpe standard error is roughly one over the square root of years. A Sharpe of point three is two such standard errors from zero only after about forty-four point four years. This is a planning calculation, not a universal sample-size guarantee. Serial correlation, skew, changing volatility and strategy selection alter it. The appropriate conclusion here is a documented research proxy and a clear evaluation specification, with no sealed-year verdict.")

    def question(self):
        self.panel(
            r"Pause and predict", r"g_{t-1}=4,\quad g_t=2,\quad h_{i,t-1}=h_{i,t}=1",
            r"The held signal is unchanged, but equal active-signal weights move from $1/4$ to $1/2$. Does discrete-signal turnover capture that trade?",
            "Pause and predict. Four active unit signals become two. A surviving unit signal has not changed, yet its normalized weight moves from one quarter to one half. Does a turnover measure using only changes in the discrete signal include that rebalance? It does not. That is why actual normalized holdings, and their hedge changes, must be reconstructed before interpreting the cost proxy as a net wealth result.")
