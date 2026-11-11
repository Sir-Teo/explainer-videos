from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, EXPO, GOOD, PART, ZERO, load

WORST, BEST, INDEP, ENT = BAD, GOOD, WHITE, QC.IDEA


class Research(VoiceoverScene):
    def construct(self):
        t = load("wwr_bounds")
        self.card()
        self.transport()
        self.lp(t)
        self.conditional(t)
        self.entropic()
        self.frontier(t)
        self.models(t)
        self.open_problems()
        self.question()
        self.answer()

    def card(self):
        c = research_card(r"Bounding wrong-way risk", r"If nobody knows how default depends on exposure, how large can CVA "
                          r"be?", part=PART)
        with self.voiceover("For the researcher: Chapter 4 modelled wrong-way risk with a copula and with Hull and "
                            "White's hazard link, and got different answers. Both are guesses about a dependence nobody "
                            "observes. Here is the question without the guess: given what we do know, how large and how "
                            "small can CVA be?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def transport(self):
        rows = [cmath(r"\mathrm{CVA}", r"=", r"(1 - R)\sum_j D(t_j)\,\mathbb E\big[V(t_j)^+\,\mathbf 1\{\tau \in (t_{j-1}, t_j]\}\big]",
                      font_size=30, colors={r"\mathrm{CVA}": CVA_C}),
                cmath(r"\mathrm{CVA}(p)", r"=", r"\sum_{i, j} p_{ij}\,c_{ij},\qquad c_{ij} = (1 - R)D(t_j)V_i(t_j)^+", font_size=30,
                      colors={r"\mathrm{CVA}(p)": CVA_C}),
                cmath(r"\sum_j p_{ij} = \tfrac1N,\ \ \sum_i p_{ij}", r"=", r"q_j = \Pr(\tau \in (t_{j-1}, t_j])", font_size=30,
                      colors={r"q_j = \Pr(\tau \in (t_{j-1}, t_j])": ZERO})]
        whys = [why('Bucketed loss with deterministic discounts; stochastic discounts belong inside the joint expectation'),
                why(r"on $N$ simulated exposure paths and $M$ default buckets (plus survival), the unknown is the joint "
                    r"probability $p_{ij}$ that path $i$ goes with default in bucket $j$"),
                why(r"its margins are known: each path has weight $1/N$, each bucket the probability from the CDS curve. "
                    r"Maximizing or minimizing a linear cost over couplings with fixed margins is a transportation problem")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Wrong-way risk bounds", wrapped_label(
            'Finite empirical bounds for these fixed path and default-bucket margins and deterministic discounts. Static couplings need not be adapted or economically realizable. Entropy constraints add model structure; the chosen budget is an assumption', 10.6, 20, GREY_A),
            who=r"Glasserman and Yang (2018), \textit{Management Science} 64", width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Write CVA before assuming anything. <bookmark mark='a'/> It is the expected discounted exposure at the "
            "moment of default. <bookmark mark='b'/> On simulated exposure paths and default buckets, the unknown is a "
            "table: the probability that path i goes with default in bucket j. <bookmark mark='c'/> Its margins are "
            "known: every path has weight one over N, and every bucket has the probability the CDS curve gives it. "
            "Optimizing a linear cost over tables with fixed margins is a transportation problem. "
            "<bookmark mark='d'/> Paul Glasserman and Linan Yang set it up this way in 2018."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.clear_scene()
            thm.move_to(ORIGIN)
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def lp(self, t):
        vals = [("best", r"best case (right-way), linear program", t["best"], BEST),
                ("indep", r"independence, Chapter 3's assumption", t["indep"], INDEP),
                ("worst", r"worst case (wrong-way), linear program", t["worst"], WORST)]
        g = axes([0, 2.0], [-0.5, 2.5], x_length=7.6, y_length=3.6, xlabel=r"CVA, millions", ylabel=r"",
                 xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[], font_size=15).move_to(LEFT * 1.2 + UP * 0.2)
        ax = g.ax
        bars = VGroup()
        for k, (_, name, v, col) in enumerate(vals):
            p0, p1 = ax.c2p(0, k - 0.3), ax.c2p(max(v, 0.005), k + 0.3)
            bars.add(VGroup(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to((p0 + p1) / 2),
                            label(rf"{name}: {v:.2f}", font_size=17, color=col).next_to(ax.c2p(max(v, 0.005), k), RIGHT,
                                                                                     buff=0.12)))
        for b_ in bars:
            fit_right(b_[1], 6.9)
        side = wrapped_label(rf"Chapter 1's netting set (three swaps, 200m notional) against a BBB-like counterparty: "
                             rf"{100 * t['default_prob']:.0f}\% chance of default in ten years, recovery {100 * t['R']:.0f}\%; "
                             rf"{t['N']:,} exposure paths by {t['M']} monthly buckets; the worst case puts "
                             rf"{100 * t['worst_top_decile_share']:.0f}\% of the default probability on the tenth of "
                             r"paths with the largest exposure", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Solve both programs for Chapter 1's netting set and a counterparty with a one in four chance of default "
            f"over ten years. <bookmark mark='a'/> Independence, the standard assumption, gives {t['indep']:.2f} "
            f"million. <bookmark mark='b'/> The worst case: {t['worst']:.2f} million, four and a half times as much, by "
            f"putting the defaults on the paths where the bank is owed most. <bookmark mark='c'/> And the best: "
            f"{t['best']:.2f}. With a quarter chance of default and exposure often zero, defaults can be hidden entirely "
            "where nothing is owed. The data alone say almost nothing about wrong-way risk."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[0]))
        self.wait(0.4)
        self.clear_scene()

    def conditional(self, t):
        tm = np.asarray(t["times"], float)
        cnd = t["cond"]
        top = max(float(np.max(v)) for v in cnd.values()) + 1e-9
        g = axes([0, 10], [0, 1.1 * top], x_length=8.0, y_length=4.2, xlabel=r"default date, years",
                 ylabel=r"expected exposure given default, millions", xticks=[0, 2, 4, 6, 8, 10],
                 yticks=list(np.round(np.linspace(0, top, 4), 0)), font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(curve(ax, tm, cnd["indep"], INDEP, stroke_width=3), curve(ax, tm, cnd["worst"], WORST, stroke_width=3),
                       curve(ax, tm, cnd["best"], BEST, stroke_width=3))
        leg = legend([(INDEP, r"independence: the expected exposure"), (WORST, r"worst case"), (BEST, r"best case")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label("in each bucket, the exposure averaged over the paths the coupling assigns to default there. Independence gives this subset's mean profile. Extreme couplings jointly allocate finite path masses across all default buckets; these curves are not pointwise exposure bounds", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            'Inspect default-conditioned exposure for each optimized coupling. <bookmark mark="a"/> Independence gives the mean positive exposure of this fixed empirical subset. <bookmark mark="b"/> The loss-maximizing coupling allocates default mass across dates and paths subject to both sets of margins. It does not independently select the highest path at each date. <bookmark mark="c"/> The loss-minimizing coupling here places defaults on zero exposure. These are profiles under three particular couplings, not pointwise envelopes for every feasible model. The LP bounds the integrated discounted loss, and the distinction matters when a model changes the timing of exposure.'
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(leg[k]), run_time=1.3)
        self.wait(0.4)
        self.clear_scene()

    def entropic(self):
        rows = [cmath(r"\max_p\ \mathrm{CVA}(p)", r"\ \text{s.t.}\ ", r"\mathrm{KL}\big(p\,\|\,p^{\perp}\big) \le \eta,\quad "
                      r"\text{margins fixed}", font_size=30, colors={r"\max_p\ \mathrm{CVA}(p)": ENT}),
                cmath(r"p_{ij}(\theta)", r"\propto", 'p^{\\perp}_{ij}\\,e^{\\theta c_{ij}/c_{\\max}}\\quad\\text{rescaled to fixed margins}',
                      font_size=30, colors={r"p_{ij}(\theta)": ENT})]
        whys = [why(r"the worst case is extreme: it couples default with the very worst paths. Budget instead how far the "
                    r"joint law may move from independence $p^{\perp} = \frac1N q_j$, in relative entropy"),
                why(r"the Lagrangian's solution is an exponential tilt towards high-exposure cells, $\theta > 0$ for "
                    r"wrong-way, $\theta < 0$ for right-way; alternating rescalings restore the margins")]
        step = ladder(self, rows, whys, keep=2, top=2.3, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The extremes are extreme. <bookmark mark='a'/> So budget the departure from independence: allow the joint "
            "law to differ from it by at most a given relative entropy. <bookmark mark='b'/> The solution is an "
            "exponential tilt of the independent table towards high-exposure cells for wrong-way risk, or away from them "
            "for right-way, rescaled row by row and column by column until the margins hold again: the Sinkhorn "
            "iteration of entropic optimal transport, which Part 9 met."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def frontier(self, t):
        e = t["entropic"]
        kl = np.array([x["kl"] for x in e])
        cv = np.array([x["cva"] for x in e])
        th = np.array([x["theta"] for x in e])
        up, lo = th >= 0, th <= 0
        g = axes([0, 0.2], [0, 1.9], x_length=8.0, y_length=4.2, xlabel=r"relative-entropy budget $\eta$",
                 ylabel='CVA of tilted couplings, millions', xticks=[0, 0.05, 0.1, 0.15, 0.2], yticks=[0, 0.5, 1.0, 1.5],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        m_up = kl[up] <= 0.2
        m_lo = kl[lo] <= 0.2
        cu = curve(ax, kl[up][m_up], cv[up][m_up], WORST, stroke_width=3)
        cl = curve(ax, kl[lo][m_lo][::-1], cv[lo][m_lo][::-1], BEST, stroke_width=3)
        ind = DashedLine(ax.c2p(0, t["indep"]), ax.c2p(0.2, t["indep"]), color=INDEP, stroke_width=1.8)
        wl = DashedLine(ax.c2p(0, t["worst"]), ax.c2p(0.2, t["worst"]), color=WORST, stroke_width=1.2)
        leg = legend([(WORST, r"upper bound (wrong-way)"), (BEST, r"lower bound (right-way)"), (INDEP, r"independence"),
                      (WORST, r"unconstrained worst case")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        j = int(np.argmin(np.abs(kl - 0.02) + 10 * (th < 0)))
        side = wrapped_label(f'each point uses its achieved KL, not a pre-set budget. Nearby sampled values: {cv[lo][np.argmin(np.abs(kl[lo] - 0.02))]:.2f} to {cv[j]:.2f}', 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            'Plot each numerically rescaled coupling at its achieved relative entropy. <bookmark mark="a"/> At zero tilt the coupling is independent. <bookmark mark="b"/> Positive and negative tilts favor larger and smaller loss cells. The plotted points are a sampled regularization path, not exact solutions at every labeled entropy budget. Units matter: the implementation divides cost by its maximum, so theta is dimensionless. A KL-constrained optimum corresponds to a suitable Lagrange multiplier when feasibility, convergence and duality conditions hold; choosing a penalty and choosing a budget are distinct operations.'
        ) as vo:
            self.play(FadeIn(g), Create(ind), Create(wl), FadeIn(leg[2]), FadeIn(leg[3]), FadeIn(side))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(cu), Create(cl), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def models(self, t):
        cards = VGroup(
            desk_question(r"Match the default law", r"Gaussian example: flat mean hazard. LP: original piecewise CDS survival. These are different margins.", width=12.0, font_size=22),
            desk_question(r"Match the empirical path law", r"Chapter 4: 20{,}000 paths. LP: one fixed subset of 1{,}500. Match weights, buckets, costs and discounting before applying a bound.", width=12.0, font_size=22),
            desk_question(r"Check feasibility and economic structure", r"Numerical inclusion alone is not a theorem. Static couplings can use future information; adapted or causal restrictions define a different problem.", width=12.0, font_size=22),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.5: cards.scale_to_fit_height(6.5)
        with self.voiceover('The chapter four calculations cannot automatically be tested against this single finite bound problem. <bookmark mark="a"/> The Gaussian example uses a flat mean hazard, while this LP uses a piecewise default curve. Both chapter four models use twenty thousand paths, while the LP uses a fixed fifteen hundred-path subset. <bookmark mark="b"/> A number falling between these extrema proves no containment theorem. To compare a model with these bounds, first match the path weights, default-bucket margins, costs and discount convention. Then verify that its coupling is feasible. Static transport bounds also allow dependencies that need not define an adapted trading model.') as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: which budget is plausible", r"the entropy budget must be set by judgement; linking it to "
                          r"observable quantities (CDS spread moves against exposure drivers) is open", width=12.4,
                          font_size=18),
            desk_question(r"open: bounds with more structure", r"requiring the coupling to respect time (default cannot "
                          r"depend on future exposure) or monotonicity tightens the bounds; such constrained transport "
                          r"problems are larger and less studied", width=12.4, font_size=18),
            desk_question(r"open: capital and accounting", r"regulators use a fixed multiplier ($\alpha = 1.4$) partly for "
                          r"wrong-way risk; whether bounds like these should replace it is unsettled", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The entropy budget is set by judgement; linking it to observable "
            "quantities, such as how CDS spreads move with the exposure's drivers, is open. <bookmark mark='b'/> "
            "Requiring the coupling to respect time, since default cannot depend on future exposure, tightens the "
            "bounds; such constrained transport problems are larger and less studied. <bookmark mark='c'/> And "
            "regulators use a fixed multiplier of one point four, partly for wrong-way risk; whether bounds like these "
            "should replace it is unsettled."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k: self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two exposure paths, equally likely, worth 0 and 10 at one date; default there has probability "
                       r"0.2. With zero rates and no recovery, what are the independent, worst and best CVA?")
        with self.voiceover(
            "Pause and predict. Two equally likely exposure paths, worth zero and ten at one date, and a default "
            "probability of a fifth at that date. With zero rates and no recovery, what are the independent, the worst "
            "and the best CVA?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def answer(self):
        head = label(r"Answer: check the joint probability mass", font_size=32).to_edge(UP, buff=0.6)
        rows = VGroup(MathTex(r"L_{ind}=10(0.5)(0.2)=1", font_size=42), MathTex(r"L_{max}=10(0.2)=2", font_size=42), MathTex(r"L_{min}=0(0.2)=0", font_size=42)).arrange(DOWN, buff=0.65)
        with self.voiceover('The independent joint mass on the ten-unit exposure and default is one half times one fifth: one tenth, so expected loss is one. <bookmark mark="a"/> Put all one fifth of default probability on the high-exposure path: loss is two. <bookmark mark="b"/> Put it all on the zero-exposure path: loss is zero. Both extremes are feasible because each path has probability one half. The bound concerns these fixed margins; it does not infer a default mechanism.') as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
