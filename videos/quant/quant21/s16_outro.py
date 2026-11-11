from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, COLL, CVA_C, DVA_C, EXPO, FVA_C, IM_C, PART, load

DESK = [
    (r"Why does a bank's DVA increase as its credit gets worse, and is that profit real?",
     'DVA is the value of not paying what the bank owes if it defaults; a worse credit makes default likelier, so the liability is worth less. Own-credit fair-value recognition is not freely spendable income; realization and prudential adjustments depend on the instrument and applicable rules'),
    (r"Two offsetting swaps with one counterparty: exposure with and without netting?",
     r"with netting, nothing: they cancel in every state. Without, the sum of each one's positive part, which is "
     r"large: the counterparty's administrator collects what it is owed and pays what it owes as an unsecured claim"),
    (r"A counterparty posts daily cash margin with a zero threshold. How can you still lose?",
     r"gap risk over the margin period (the move between its last payment and your close-out), and the cost of "
     r"replacing the hedges in a market that moved; plus disputes, and collateral that is itself correlated with the "
     r"default (wrong-way)"),
    (r"Why does margin rise exactly when cash is scarce?",
     r"margin models scale with recent volatility, and volatility rises in crises; every margined position is called "
     r"at once, and the cash is raised by selling, which raises volatility again. Floors, buffers and longer windows "
     r"dampen the loop at the cost of more margin in calm times"),
    (r"What does a backward pass get wrong at $\max(V, 0)$ or at a jump in a payoff?",
     'At a continuous kink, pathwise differentiation needs regularity and a justified derivative-expectation exchange; atoms at the kink need care. Jumps can add boundary contributions missed by naive pathwise differentiation. Smoothing adds bias; likelihood-ratio or conditional methods have their own assumptions'),
    (r"A client posts 20\% margin on a single-stock swap. What do you most want to know?",
     r"the size of its position against the stock's daily volume, at every dealer combined: that sets the time to "
     r"liquidate, and with it the margin. It is not visible because swaps leave the shares in the dealers' names"),
]

PROBLEMS = [
    r"For a forward contract with value $V(t) = \sigma W_t$, show that $\text{EE}(t) = \sigma\sqrt{t/(2\pi)}$ and "
    r"$\text{PFE}_{95}(t) = 1.645\,\sigma\sqrt t$.",
    r"A swap's EE is roughly $\sigma\sqrt t\,(T - t)\,c$. At what $t$ is it largest? Compare with chapter 1's hump.",
    r"With a flat hazard $\lambda$ and constant EE, show that $\text{CVA} \approx (1 - R)\,\lambda\,\text{EE}\int_0^T "
    r"e^{-(r + \lambda)t}\,dt$, and hence that CVA as a running spread is about $(1 - R)\lambda \times \text{EPE}/N$.",
    r"Show that bilateral CVA with independent defaults is $(1 - R)\int \text{EE}(t) P(0,t) Q_b(t)\,(-dQ_c(t))$, and "
    r"explain why it is smaller than the unilateral CVA.",
    r"Collateral with zero threshold and margin period $m$: show that for $V(t) = \sigma W_t$ the collateralised EE is "
    r"about $\sigma\sqrt{m/(2\pi)}$, independent of $t$.",
    r"Compute SA-CCR's add-on for a single 10-year payer swap on \$100 million, unmargined ($S = 0$, $E = 10$).",
    r"A CCP's two largest members would lose 30 and 25 beyond their margin in a stress. What default fund does Cover 2 "
    r"require, and who pays if the third largest also defaults?",
    r"Why can AAD compute $n$ sensitivities for the cost of a few valuations, while bumping costs $n$? What does it "
    r"cost in memory?",
    r"With $N$ dealers and $K$ independent, equal asset classes, show that clearing one class lowers a dealer's expected "
    r"exposure if and only if $N > 1 + (\sqrt K + \sqrt{K - 1})^2$.",
    r"A trade needs capital $K(t) = K_0(1 - t/T)$ for $T$ years. With hurdle $h$ and no discounting, show that "
    r"$\text{KVA} = h K_0 T/2$.",    r"(qual) Write CVA over couplings of $N$ exposure paths and $M$ columns including survival as a transportation LP; show the "
    r"bounds are attained at vertices with at most $N + M - 1$ positive cells, and solve the two-path example by hand.",
    r"(qual) For $\theta > 0$, show that maximizing $\sum p_{ij}c_{ij} - \frac1\theta\mathrm{KL}(p\,\|\,p^\perp)$ over couplings gives "
    r"$p_{ij} = a_i b_j p^\perp_{ij}e^{\theta c_{ij}}$, and that Sinkhorn's alternating rescaling finds $a$, $b$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("exposure"), load("collateral"), load("cva"), load("wwr"), load("fva"), load("aad"),
                   load("deepxva"), load("im"), load("procyc"), load("ccp"), load("saccr"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, e, c, v, w, f, a, d, im, p, cc, s):
        rr = np.asarray(w["cva"])
        r = load("cvarisk")
        pages = [[
            (r"Archegos: more than \$10 billion of bank losses on one client's swaps", BAD),
            (rf"exposure: a hump from diffusion and run-off; netting, enforced by law, cut it by "
             rf"{100 * e['netting_benefit']:.0f}\%", EXPO),
            (rf"collateral leaves the margin period's moves: EPE {c['profiles']['none']['EPE']:.1f} to "
             rf"{c['profiles']['threshold 0']['EPE']:.1f}; haircuts and segregation protect what is held", COLL),
            (rf"CVA \${1e3 * v['cva']:.0f}k, a position with a CS01 of \${1e6 * r['cs01']:,.0f} a bp; DVA rises as the "
             r"bank weakens".replace(",", "{,}", 1), CVA_C),
            (r"price by increment: a trade that offsets the netting set earns a credit", CVA_C),
            (f"wrong-way risk: the same trade's CVA {rr[-1] / rr[2]:.1f} times larger when default and exposure move together within the flat-hazard illustration; regulatory alpha is a separate measure", BAD),
            ('Funding need not cancel even at equal spreads; KVA and MVA depend on a consistent cost policy',
             FVA_C),
            (rf"AAD: every sensitivity in one backward pass, {a['t_aad']:.0f} s against {a['t_bump']:.0f} s of bumps",
             DVA_C)],
            [('a fixed surrogate experiment: per-date cubic beats this network; high-dimensional bases need structure', EXPO),
             (f"initial margin \\${im['im']:.1f}m by a SIMM-style formula; it reduces modelled gap risk and incurs a funding cost", IM_C),
             (r"margin follows volatility: buffers and floors damp the jump and cost margin every calm day", IM_C),
             (r"clearing nets everyone, but one product cleared alone can raise total exposure", COLL),
             (r"Lehman's swaps closed out within a third of its margin; one power trader took two thirds of a fund",
              COLL),
             (r"the LME cancelled a day of nickel trades rather than let members default", BAD),
             (rf"capital: SA-CCR \${s['net']['EAD']:.1f}m netted, a CVA charge, and a leverage ratio that prices "
              r"balance sheet", FVA_C),
             (r"margin must follow the time it takes to sell; for Archegos's positions that was weeks", BAD)]]
        shown = []
        for k, items in enumerate(pages):
            rows = VGroup()
            for i, (t, col) in enumerate(items, 1 + 8 * k):
                rows.add(VGroup(MathTex(str(i), font_size=24, color=col), wrapped_label(t, 11.6, 22)).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            title = label(r"Part 21 in sixteen lines" + ("" if k == 0 else r", continued"), font_size=34).to_edge(UP, buff=0.35)
            if rows.width > 13.0:
                rows.scale_to_fit_width(13.0)
            if rows.height > 6.4:
                rows.scale_to_fit_height(6.4)
            rows.next_to(title, DOWN, buff=0.28)
            shown.append((title, rows))

        def show(k):
            title, rows = shown[k]
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        with self.voiceover(
            'The first half in eight lines. Reported Archegos losses motivate counterparty exposure, but the exposure model here is an illustrative floating-reset sketch. Netting requires enforceable agreements. Collateral leaves gap risk and contractual complications. CVA uses positive exposure, with the survival sign and discount convention specified; DVA is not freely spendable income. New trades change a whole netting set. Dependence can change loss even when default marginals are fixed, but our flat-hazard and piecewise-hazard examples have different marginals. Funding costs need not cancel at equal spreads, and combining adjustments requires a consistent policy. AAD differentiates one scalar computation with respect to many inputs.'
        ):
            show(0)
        self.wait(0.5)
        self.clear_scene()
        with self.voiceover(
            'The second half. Regression and neural networks approximate this fixed simulated model, with independent test paths and measured error. Initial margin reduces modelled gap risk and costs funding; the delta-only aggregation is not full SIMM. Buffers and floors trade higher calm-period margin for stability. Clearing changes netting and mutualizes some losses; its simulated waterfall frequencies are assumptions, not forecasts. Public episodes distinguish notional, collateral, losses and liquidity. Regulatory examples depend on jurisdiction and implementation date. Concentration and liquidation time matter, and no illustrative impact formula establishes a universally safe margin.'
        ):
            show(1)
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK[:4]]).arrange(DOWN, buff=0.25)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            'Four desk questions. Why does DVA rise as the bank\'s own credit worsens? It reflects own non-performance risk under the valuation convention; recognition does not create freely spendable income. <bookmark mark="a"/> Two offsetting swaps with one counterparty cancel under enforceable netting; without it, positive claims are considered separately. <bookmark mark="b"/> Daily collateral still leaves margin-period risk, disputes, settlement and collateral-value risk. <bookmark mark="c"/> Responsive margin can rise when liquidity is scarce. Buffers and floors trade calm-time cost for stability, but their performance must be tested under the actual policy.'
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        more = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK[4:]]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            'Two more. A continuous positive-part kink often permits pathwise differentiation under a continuous state law and suitable domination. Atoms and failure of derivative-expectation interchange need care. A discontinuous payoff can have a boundary contribution that naive differentiation misses. Smoothing introduces bias; likelihood-ratio and conditional methods require their own regularity checks. <bookmark mark="a"/> For a concentrated single-stock client, measure position size against available volume across dealers. It informs liquidation time and stress, but neither volume nor a fixed impact formula guarantees a safe margin.'
        ) as vo:
            self.play(FadeIn(more[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(more[1], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        def page(first, last, title, size):
            card = problem_set(PROBLEMS[first:last], font_size=size, title=title)
            for i, row in enumerate(card.rows, first + 1):
                row[0].become(label(str(i) + ".", font_size=size, color=QC.IDEA).move_to(row[0]))
            return card
        ps = page(0, 6, 'Problems 1--6', 22)
        with self.voiceover("Problems one to six. Derive expected exposure and the ninety-fifth percentile for the normal forward. Find the maximum of the diffusion-times-runoff swap profile. Turn constant-exposure CVA into a running spread, stating its reference notional and assumptions. Add the other party's survival to obtain a bilateral first-to-default expression. Derive gap exposure for a zero-threshold margin agreement under the stated lag. Then calculate the supervisory add-on for one swap. Keep pricing probabilities, discounting, time units and regulatory approximations explicit. The notes provide worked solutions; pause here to attempt the calculations."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.2, run_time=3))
        self.wait(2)
        self.clear_scene()
        ps = page(6, 10, 'Problems 7--10', 22)
        with self.voiceover("Problems seven to ten. Apply the exercise's chosen Cover Two requirement to two stressed excess losses, then explain what changes if a third member defaults. Compare the work and memory of reverse differentiation with bumping, and state the conditions needed at kinks or discontinuities. Derive the dealer-count threshold for clearing one class in the independent normal netting model. Finally integrate a linearly declining capital profile to obtain the undiscounted KVA in that exercise. Each result is conditional on its model and policy assumptions, rather than a general compliance or safety statement."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.2, run_time=3))
        self.wait(2)
        self.clear_scene()
        ps = page(10, 12, 'Qualifying problems 11--12', 24)
        with self.voiceover('The two qualifying problems. In the transport problem, let M count all columns, including survival. Prove that an optimum occurs at a vertex with at most N plus M minus one positive cells, allowing degeneracy, and solve the two-path example. For the entropy problem assume a positive theta and positive prescribed margins. Derive the exponentially tilted, row-and-column-scaled optimizer and explain Sinkhorn feasibility. Distinguish a regularization parameter from a pre-set KL budget, and state why a static coupling need not be adapted to market information. The English and Chinese notes contain the derivations.'):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.2, run_time=3))
        self.wait(2)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"balance sheet costs behind the cross-currency basis and the Treasury basis trade", [22]),
            (r"funding and capital as costs in every backtest", [26]),
            (r"market impact: what selling a concentrated position costs", [37]),
            (r"market makers and their counterparties", [38]),
            (r"the finale: the House's counterparties in a stress, with their collateral", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-two: balance-sheet costs behind the currency basis and the Treasury "
            "basis trade. Part twenty-six charges funding and capital in every backtest. Part thirty-seven measures "
            "what it costs to sell a concentrated position, Archegos's problem. Part thirty-eight turns to market "
            "makers. And the finale stresses the House's counterparties together with their collateral."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gregory, \textit{The xVA Challenge}; Green, \textit{XVA: Credit, Funding and Capital Valuation "
             r"Adjustments}; Brigo, Morini and Pallavicini, \textit{Counterparty Credit Risk, Collateral and Funding}; "
             r"Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 24"],
            [r"Brigo and Masetti (2005); Pykhtin and Zhu (2007); Piterbarg (2010); Burgard and Kjaer (2011); Duffie and "
             r"Zhu (2011); Hull and White (2012); Green, Kenyon and Dennis (2014); Cont (2015); Andersen, Duffie and Song "
             r"(2019); Gnoatto, Picarelli and Reisinger (2023); Giles and Glasserman (2006)",
             r"Basel Committee, SA-CCR (2014) and the CVA framework (2020); CPMI--IOSCO, \textit{Principles for "
             r"Financial Market Infrastructures} (2012); ISDA SIMM; Paul, Weiss report on Archegos (2021); LME notices "
             r"(March 2022) and the High Court's judgment (2023)"])
        with self.voiceover(
            "The textbooks this part follows, and the papers, standards and public records it draws on, from Brigo "
            "and Masetti's CVA to deep solvers for the adjustments. Every number on screen was computed by the "
            "House's code on the Fed's curve, with illustrative credit and margin parameters labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("credit",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 22, FX, Commodities and the Basis", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That completes the credit desk: default, and the price of every counterparty's promise. "
            "<bookmark mark='a'/> Next, Part twenty-two: currencies, commodities, and the bases that open when balance "
            "sheets are expensive. The House's macro desk opens."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
