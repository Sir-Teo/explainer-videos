from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BAD, BUY_C, GOOD, HURDLE, IMPACT_C, KERNEL_C, PART, SCHED_C, TWAP_C, fit_right,
                                         load)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        o = load("ow")
        self.card()
        self.setup_()
        self.convex()
        self.first_order()
        self.verify()
        self.solve()
        self.why_measures()
        self.theorem()
        self.intuition()
        self.limits()
        self.grid(o)
        self.saving(r)
        self.power_case()
        self.btc(r)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The optimal schedule under transient impact", r"Why blocks at the ends, and is the answer "
                          r"unique?", part=PART)
        with self.voiceover('For the researcher. We first prove uniqueness and a necessary-and-sufficient variational condition, conditional on a solution for a general kernel. Strict positivity alone does not prove existence over all finite signed measures. Then we construct the exponential-kernel candidate explicitly, verify it and thereby prove both existence and uniqueness for positive rho, depth and horizon. Numerical grids and fitted-parameter surrogate examples remain separate illustrations.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"\mathcal A", r"=", r"\{\text{signed measures } dX \text{ on } [0, T],\ \textstyle\int dX = X\}",
                      font_size=34),
                cmath(r"\mathcal C[X]", r"=", r"\tfrac12 \iint G(|t - s|)\,dX_s\,dX_t", font_size=40,
                      colors={r"\mathcal C[X]": IMPACT_C}),
                cmath(r"G", r":", '\\text{continuous; integrally strictly positive definite}', font_size=36,
                      colors={r"G": KERNEL_C})]
        whys = [why(r"strategies: any mixture of blocks and continuous trading, buys and sells, adding up to the order"),
                why(r"the expected cost under linear transient impact (Chapter 4), the noise averaged out"),
                why(r"Gatheral's condition, strict: $\mathcal C[\mu] > 0$ for every non-zero measure, so round trips "
                    r"cost money")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setting. <bookmark mark='a'/> Admissible strategies are finite signed Borel measures on a compact interval with fixed total mass. Their total variation is finite but not uniformly bounded over the admissible set. <bookmark mark='b'/> A continuous symmetric kernel makes each such measure's quadratic energy finite. <bookmark mark='c'/> Require integral strict positive definiteness on nonzero finite signed measures, or at least strict positivity on nonzero zero-mass directions for uniqueness. Strict positivity of every finite matrix on distinct points is not, by itself, the required measure-level existence or coercivity condition."
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

    def convex(self):
        rows = [cmath(r"\mathcal C[X + \varepsilon\mu]", r"=", r"\mathcal C[X] + \varepsilon\,B(X, \mu) + "
                      r"\varepsilon^2\,\mathcal C[\mu]", font_size=34),
                cmath(r"\mathcal C[\mu]", r">", r"0\quad (\mu \ne 0)", font_size=40, colors={r"0\quad (\mu \ne 0)": GOOD}),
                cmath(r"\Rightarrow", r"\ ", r"\text{at most one minimiser}", font_size=38)]
        whys = [why(r"a quadratic form: expand along any direction $\mu$; $B(X, \mu) = \iint G(|t - s|)\,dX_s\,d\mu_t$"),
                why(r"strict positive definiteness makes the second-order term positive"),
                why(r"so the cost is strictly convex on $\mathcal A$, which is convex: two minimisers would have a cheaper "
                    r"midpoint")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, uniqueness. <bookmark mark='a'/> The cost is a quadratic form: move along any direction mu, and "
            "it changes by a linear term and a quadratic one. <bookmark mark='b'/> Strict positive definiteness makes "
            "the quadratic term positive. <bookmark mark='c'/> So the cost is strictly convex on a convex set, and two "
            "minimisers would have a cheaper midpoint: there is at most one."
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

    def first_order(self):
        rows = [cmath(r"\mu", r"=", r"\delta_a - \delta_b", font_size=40),
                cmath(r"B(X^*, \mu)", r"=", r"f(a) - f(b) = 0,\quad f(t) = \int G(|t - s|)\,dX^*_s", font_size=32),
                cmath(r"f(t)", r"\equiv", r"\lambda\ \ \text{on } [0, T]", font_size=40, colors={r"f(t)": SCHED_C}),
                cmath(r"\mathcal C[X^*]", r"=", r"\tfrac12\,\lambda X", font_size=40)]
        whys = [why(r"an admissible perturbation: buy one more unit at $a$, one less at $b$; the total is unchanged"),
                why(r"at a minimum the first-order term vanishes in every admissible direction"),
                why('the full symmetric marginal-cost potential, including future trades, is constant: a Fredholm first-kind equation; a fixed-mass candidate solves optimality, while existence is separate'),
                why(r"integrate $f$ against $dX^*$: the minimal cost")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Lemma two, conditional characterization. <bookmark mark='a'/> At an existing minimizer, perturb by a point mass at a minus a point mass at b. Both signs of this perturbation remain admissible. <bookmark mark='b'/> The derivative vanishes, giving equality of f at a and b. Here f integrates the symmetric kernel over the entire trading interval, including future trades: it is a marginal-cost potential, not the causal displacement left by past trades. <bookmark mark='c'/> Thus f is constant everywhere. Conversely a candidate of the required total mass with constant f minimizes cost by quadratic positivity. <bookmark mark='d'/> Integrating the potential against that candidate gives cost one half lambda X."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def verify(self):
        rows = [cmath(r"dX^*", r"=", r"a\,\delta_0 + b\,dt + a\,\delta_T", font_size=40, colors={r"dX^*": SCHED_C}),
                cmath(r"f(t)", r"=", r"a\,(e^{-\rho t} + e^{-\rho(T - t)}) + \frac{b}{\rho}(2 - e^{-\rho t} - e^{-\rho(T - t)})",
                      font_size=28),
                cmath(r"f\ \text{constant}", r"\iff", r"a = b/\rho", font_size=40, colors={r"a = b/\rho": GOOD})]
        whys = [why(r"guess the shape: equal blocks at the ends and a constant rate between, for $G(t) = e^{-\rho t}$ "
                    r"(unit depth)"),
                why(r"integrate the kernel against it: the blocks contribute exponentials from each end, the flow their "
                    r"complements"),
                why(r"the exponentials cancel exactly when the block equals the rate times the recovery time $1/\rho$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma three, the exponential kernel. <bookmark mark='a'/> Guess the shape: equal blocks at the ends, a "
            "constant rate between. <bookmark mark='b'/> Integrate the kernel against it: each block contributes an "
            "exponential decaying from its end, and the steady flow contributes the complements. "
            "<bookmark mark='c'/> The exponentials cancel, and f is constant, exactly when each block equals the rate "
            "times the recovery time."
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

    def solve(self):
        rows = [cmath(r"2a + bT", r"=", r"X", font_size=40),
                cmath(r"a", r"=", r"\frac{X}{2 + \rho T},\quad b = \frac{\rho X}{2 + \rho T}", font_size=38,
                      colors={r"a": BUY_C}),
                cmath(r"\lambda", r"=", r"\frac{2b}{\rho} = \frac{2X}{2 + \rho T}", font_size=38),
                cmath(r"\mathcal C^*", r"=", r"\frac{X^2}{2 + \rho T}", font_size=42, colors={r"\mathcal C^*": IMPACT_C})]
        whys = [why(r"the order must be filled"),
                why(r"with $a = b/\rho$: the blocks and the rate"),
                why(r"the constant value of $f$"),
                why(r"and the cost, $\frac12 \lambda X$; with depth $q$, divide by $q$; Obizhaeva and Wang (2013)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Solve. <bookmark mark='a'/> The order must be filled: two blocks plus the rate times T is X. "
            "<bookmark mark='b'/> With the block equal to the rate over rho, each block is X over two plus rho T. "
            "<bookmark mark='c'/> The constant impact is twice the block. <bookmark mark='d'/> And the cost, half of "
            "lambda times X, is X squared over two plus rho T."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def why_measures(self):
        rows = [cmath(r"\mathcal A_{\text{rate}}", r"=", r"\{dX = v(t)\,dt\}", font_size=38),
                cmath(r"\inf_{\mathcal A_{\text{rate}}} \mathcal C", r"=", r"\mathcal C^*\ \text{but not attained}",
                      font_size=36, colors={r"\mathcal C^*\ \text{but not attained}": BAD}),
                cmath(r"v_\varepsilon", r"=", r"\frac{a}{\varepsilon}\mathbb 1_{[0,\varepsilon]} + b + "
                      r"\frac{a}{\varepsilon}\mathbb 1_{[T - \varepsilon, T]}", font_size=34)]
        whys = [why(r"restrict to strategies with a trading rate, no blocks"),
                why(r"the cost can be brought arbitrarily close to the optimum, but no rate reaches it"),
                why('for this explicit exponential candidate, bounded-variation bursts converge in energy; rate-only attainment fails')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "For the positive-rho exponential kernel, the verified optimum has nonzero endpoint atoms. <bookmark mark='a'/> Restricting to integrable trading rates excludes that unique measure. <bookmark mark='b'/> The minimum is therefore not attained in the rate-only class. <bookmark mark='c'/> The displayed narrow bursts preserve total mass and approximate the atoms weakly; continuity of the kernel on the compact square and bounded total variation give convergence of their energies. This proves the same infimum for this explicit exponential case. It is not a general existence theorem for arbitrary continuous strictly positive-definite kernels."
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

    def theorem(self):
        st = VGroup(MathTex(r"\min_{\mathcal A} \mathcal C\ \text{has at most one solution, characterised by } \int_0^T "
                            r"G(|t - s|)\,dX^*_s = \lambda\ \ \forall t \in [0, T]", font_size=28),
                    MathTex(r"G = \tfrac1q e^{-\rho t}:\quad dX^* = \tfrac{X}{2 + \rho T}\big(\delta_0 + \rho\,dt + "
                            r"\delta_T\big),\quad \mathcal C^* = \frac{X^2}{q\,(2 + \rho T)}", font_size=28),
                    wrapped_label(r"for positive $q,\rho,T$, this verified optimum has no sales; at $\rho=0$, uniqueness fails and cost is "
                                  r"permanent $X^2/2q$ for every schedule, and as $\rho T \to \infty$ to $X^2/(q\rho T)$, "
                                  r"Almgren--Chriss's temporary cost with $\eta = 1/(q\rho)$", 9.6, 20)).arrange(DOWN,
                                                                                                         buff=0.35)
        card = theorem_card(r"Transient impact (Obizhaeva--Wang 2013; Gatheral, Schied and Slynko 2012)", st,
                            r"this part's proof", width=11.8, font_size=22)
        self.add(card)
        with self.voiceover(
            "The theorem, with its quantifiers. <bookmark mark='a'/> For a continuous kernel with integral strict positivity, there is at most one finite signed minimizer. A fixed-mass candidate is optimal exactly when its full symmetric marginal-cost potential is constant. Existence still requires a candidate or an additional theorem. <bookmark mark='b'/> For positive rho, q and T, the endpoint blocks plus constant rate are that verified candidate, so existence and uniqueness follow, with cost X squared over q times two plus rho T. At rho zero the cost becomes schedule-independent and uniqueness fails. The fast-recovery temporary-cost connection also requires matching eta equal to one over q rho."
        ) as vo:
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def intuition(self):
        cards = VGroup(
            desk_question(r"why a block at the start", r"the book is undisturbed: the first units are the cheapest the "
                          r"order will ever buy, and their impact has the whole horizon to heal", width=12.4, font_size=19),
            desk_question(r"why a block at the end", r"the last trade's impact harms no later trade; only its own "
                          r"half-cost remains, so it is worth buying a lump", width=12.4, font_size=19),
            desk_question(r"why a constant rate between", 'the full symmetric marginal-cost potential includes effects on future trades; it is not the causal displacement', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why the exponential shape is plausible. <bookmark mark='a'/> An initial block can exploit undisturbed depth and allow its causal displacement to decay. <bookmark mark='b'/> The final block has no later trades to affect. <bookmark mark='c'/> Between them a steady rate balances exponential decay. The optimality test, however, equalizes the full symmetric marginal cost including effects on future trades. That potential is twice the constant interior causal displacement for this solution; confusing the two would misread the Fredholm condition."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        rows = [cmath(r"\rho \to 0", r":", r"\mathcal C^* \to \tfrac{X^2}{2q}\ \text{for every schedule}", font_size=36),
                cmath(r"\rho T \to \infty", r":", r"\mathcal C^* \approx \frac{X^2}{q\rho T} = \eta\,\frac{X^2}{T}",
                      font_size=36),
                cmath(r"\eta", r"=", r"\frac{1}{q\rho}", font_size=40, colors={r"\eta": HURDLE})]
        whys = [why(r"no resilience: impact is permanent and linear, Huberman and Stanzl's case; the schedule does not "
                    r"matter"),
                why(r"fast resilience: the blocks vanish, the rate is $X/T$, and the cost is TWAP's under Almgren--Chriss "
                    r"temporary impact"),
                why(r"so Almgren--Chriss's temporary impact is a thin book that heals fast: depth times resilience is the "
                    r"liquidity it measures")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The limits. <bookmark mark='a'/> At rho zero, cost is X squared over two q for every schedule with total X, and there is no unique optimum. The two-block limit is one choice. <bookmark mark='b'/> For large rho T, optimal cost is asymptotic to X squared over q rho T and endpoint shares vanish. <bookmark mark='c'/> This matches a risk-neutral temporary-cost model with eta equal to one over q rho. Keeping a nonzero eta in a fast-recovery limit requires joint rescaling of depth; with fixed q the modeled cost tends to zero. This does not generate a risk-aversion term by itself."
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

    def grid(self, o):
        hx = [-3.8, -1.0, 1.8, 4.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"grid dates", r"cost", r"first block",
                                                                         r"smallest trade")])
        tab = VGroup(head)
        for r in o["rows"]:
            tab.add(VGroup(MathTex(str(r["n"]), font_size=24), MathTex(f"{r['cost']:.5f}", font_size=24),
                           MathTex(f"{r['block']:.4f}", font_size=24), MathTex(f"{r['min']:.4f}", font_size=24)))
        tab.add(VGroup(label(r"formula", font_size=18, color=HURDLE),
                       MathTex(f"{o['closed']['cost']:.5f}", font_size=24, color=HURDLE),
                       MathTex(f"{o['closed']['block']:.4f}", font_size=24, color=HURDLE), MathTex(r"> 0", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.9 - 0.58 * j, 0])
        with self.voiceover(
            "Check one: the grid. Solve the discrete problem exactly, with rho T of ten, on finer and finer grids. "
            "<bookmark mark='a'/> The cost converges to the formula's "
            f"{o['closed']['cost']:.4f}, the first block to {o['closed']['block']:.4f}, and every trade is a purchase. "
            "The block shrinks toward the limit from above, because on a coarse grid the first date also carries part "
            "of the flow."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def saving(self, r):
        rows = r["rows"]
        x = np.log10([q["rhoT"] for q in rows])
        y = [100 * q["saving"] for q in rows]
        top = float(np.ceil(max(y) / 5) * 5)
        g = axes([-1, 2], [0, top], x_length=6.4, y_length=4.4, xlabel=r"resilience $\rho T$",
                 ylabel=r"saving of the optimum over TWAP, \%", xticks=[-1, 0, 1, 2], xfmt=lambda v: f"10^{{{v:.0f}}}",
                 yticks=[0, top / 2, top], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_ = VGroup(curve(ax, x, y, SCHED_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.07, color=SCHED_C)
                                                                for a, b in zip(x, y)])
        k = int(np.argmax(y))
        st = label(r"TWAP's cost: $\frac{1}{\rho T}\left(1 - \frac{1 - e^{-\rho T}}{\rho T}\right)$", font_size=18)
        st.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(st)
        with self.voiceover(
            "Check two: what the optimum is worth. TWAP's cost under the exponential kernel is a closed form too. "
            "<bookmark mark='a'/> The saving of the optimal schedule over TWAP is small when the book barely recovers, "
            "because then impact is nearly permanent, and small again when it recovers almost at once. In between it "
            f"peaks, at about {y[k]:.0f} percent when rho T is near {rows[k]['rhoT']:g}: a horizon a few recovery times "
            "long."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def power_case(self):
        rows = [cmath(r"G(t)", r"=", r"(1 + t/\ell_0)^{-\beta}", font_size=40, colors={r"G(t)": KERNEL_C}),
                cmath(r"\text{Fredholm}", r":", r"\int_0^T G(|t - s|)\,dX_s = \lambda", font_size=36),
                cmath(r"\text{solution}", r":", r"\text{blocks} + \text{a U-shaped rate}", font_size=36,
                      colors={r"\text{solution}": SCHED_C})]
        whys = [why('a chosen positive-parameter shifted-power-law surrogate using Chapter3 estimates'),
                why(r"the same characterisation, but no closed form: solve the integral equation numerically, as the "
                    r"House's \texttt{kernel\_optimal} does on a grid"),
                why('regularized shifted kernels and singular pure powers have different endpoint behavior; this graph is a finite-grid example')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Beyond the exponential, choose a shifted power-law family with positive scale and exponent. <bookmark mark='a'/> It is a regularized surrogate using fitted parameters, not the raw empirical propagator. <bookmark mark='b'/> Finite-grid linear algebra solves its discrete first-order equations; numerical residuals are finite-grid checks, not a continuum convergence proof. <bookmark mark='c'/> Its regularized endpoint blocks and U-shaped interior differ from an unshifted singular power-law kernel, whose endpoint density may diverge. Treat those kernel classes and their existence results separately."
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

    def btc(self, r):
        b = r["btc"]
        v = np.asarray(b["v"], float)
        n = len(v)
        rate = v * n
        top = float(np.ceil(rate[1:-1].max() * 1.6 * 10) / 10)
        g = axes([0, n - 1], [0, top], x_length=8.4, y_length=4.0, xlabel=r"decision, every 100 trades",
                 ylabel=r"trading rate (TWAP $= 1$)", xticks=[0, 100, 200], yticks=[0, 1], font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        mid = curve(ax, np.arange(1, n - 1), rate[1:-1], SCHED_C, stroke_width=3)
        tw = DashedLine(ax.c2p(0, 1), ax.c2p(n - 1, 1), color=TWAP_C, stroke_width=1.6)
        b0 = Arrow(ax.c2p(0, 0), ax.c2p(0, top * 0.95), buff=0, color=BUY_C, stroke_width=6)
        b1 = Arrow(ax.c2p(n - 1, 0), ax.c2p(n - 1, top * 0.95), buff=0, color=BUY_C, stroke_width=6)
        save = 100 * (1 - b["cost"] / b["twap"])
        with self.voiceover(
            f"""A fitted-parameter surrogate example. Use exponent {b['beta']:.2f}, scale {b['l0']} trades and a {b['trades']:,}-trade horizon, with one decision every hundred trades. <bookmark mark='a'/> The two hundred and one-date optimum has endpoint shares {100*b['block0']:.1f} percent and a nonnegative shallow interior U. These are discrete trades, not proof of continuum atom sizes. <bookmark mark='b'/> Its finite-grid model cost is {save:.1f} percent below equal grid slices. This comparison excludes spread, fees, risk, changing participation and informational drift; it is not an observed saving on actual orders."""
        ) as vo:
            self.play(FadeIn(g), Create(tw))
            vo.wait_until("a")
            self.play(GrowArrow(b0), GrowArrow(b1), Create(mid))
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Gatheral, Schied and Slynko (2012)", r"the Fredholm characterisation for general "
                          r"positive-definite kernels, and explicit solutions for several", width=12.4, font_size=18),
            desk_question(r"Alfonsi, Fruth and Schied (2010)", r"a book of general shape rather than a block: nonlinear "
                          r"impact, and optimal strategies that still open and close with blocks", width=12.4,
                          font_size=18),
            desk_question(r"Obizhaeva and Wang (2013)", r"the original model, with resilience as the speed at which new "
                          r"liquidity arrives, and its link to Almgren--Chriss", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Gatheral, Schied and Slynko gave the Fredholm characterisation for "
            "general kernels, and explicit solutions for several. <bookmark mark='b'/> Alfonsi, Antje Fruth and Schied "
            "let the book have any shape, which makes impact nonlinear, and found blocks at the ends still. "
            "<bookmark mark='c'/> And Obizhaeva and Wang's original paper read resilience as the speed of new liquidity."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: nonlinear and transient together", r"a model with square-root impact in size and a "
                          r"decaying kernel, free of dynamic arbitrage, whose optimal schedules are computable", width=12.4,
                          font_size=18),
            desk_question(r"open: impact with information", r"separating the part of impact that is information "
                          r"(permanent) from the part that is mechanical (transient), from public data", width=12.4,
                          font_size=18),
            desk_question(r"open: many executors", r"the equilibrium of many funds with transient impact and private "
                          r"signals, and whether it is stable", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> A model with square-root impact in size and a decaying kernel, "
            "free of dynamic arbitrage, whose optimal schedules can be computed. <bookmark mark='b'/> Separating, from "
            "public data, the part of impact that is information from the part that is mechanics. "
            "<bookmark mark='c'/> And the equilibrium of many funds with transient impact and private signals, and "
            "whether it is stable."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('7. Exponential resilience', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$X=1$, $T=1$, $q=1$, $\\rho=2$; allow finite signed measures and half-self-impact.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Find each endpoint block, the interior rate, optimum cost and TWAP cost.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause seven. Use an exponential kernel with quantity, horizon and depth all one, and rho equal to two. Finite signed measures and half-self-impact are allowed. Compute the endpoint blocks, interior rate, optimum cost and continuous TWAP cost. Give the saving with its correct denominator.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
