from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BAD, BUY_C, GOOD, IMPACT_C, KERNEL_C, PART, SELL_C, load)


class NoArb(VoiceoverScene):
    def construct(self):
        k = load("kernels")
        self.card()
        self.cost_formula()
        self.permanent()
        self.hs_example()
        self.box(k)
        self.gatheral()
        self.convex()
        self.gauss(k)
        self.refine(k)
        self.btc_passes(load("propagator"))
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(4, r"No dynamic arbitrage", r"Which models of impact are allowed?", part=PART)
        with self.voiceover("Chapter four. A box-shaped decay kernel can give a suitably timed multi-leg round trip negative expected model cost. A simple buy, wait, sell pair is not enough for a nonincreasing kernel; the counterexample needs the interactions of several legs. The requirement is to examine the whole quadratic cost functional under the model's trading and self-impact conventions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cost_formula(self):
        rows = [cmath(r"p_t", r"=", r"p_0 + \int_0^t G(t - s)\,dX_s + \text{noise}", font_size=38,
                      colors={r"G(t - s)": KERNEL_C}),
                cmath(r"\mathcal C[X]", r"=", r"\tfrac12 \iint G(|t - s|)\,dX_s\,dX_t", font_size=40,
                      colors={r"\mathcal C[X]": IMPACT_C}),
                cmath(r"\text{round trip}", r":", r"\textstyle\int dX = 0", font_size=36)]
        whys = [why(r"linear transient impact: each unit traded pushes the price by a kernel that decays"),
                why(r"the expected cost of a trading programme $X$: every trade pays the impact of the trades before it, "
                    r"and half its own"),
                why(r"a programme that ends flat; with no information, it should never have negative expected cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setting is deterministic signed finite-variation trading against linear transient impact and a martingale unaffected price. <bookmark mark='a'/> The causal price contains earlier trades. <bookmark mark='b'/> Expected impact cost uses the symmetric double integral, including half the self-impact of a block. Spread, fees, risk and any predictive drift are omitted. <bookmark mark='c'/> A zero-total round trip should have nonnegative expected cost. This is a model consistency condition, distinct from an executable risk-free arbitrage in a market with frictions."
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

    def permanent(self):
        rows = [cmath(r"\text{permanent}", r":", r"p \mathrel{+}= f(v)\,dt", font_size=38),
                cmath(r"\text{no round-trip profit}", r"\Rightarrow", r"f(v) = \kappa\,v", font_size=36,
                      colors={r"f(v) = \kappa\,v": GOOD}),
                cmath(r"\text{cost}", r"=", r"\tfrac12\,\kappa\,X^2\ \text{whatever the schedule}", font_size=34)]
        whys = [why(r"impact that never decays, as a function of the trading rate"),
                why(r"Huberman and Stanzl (2004): if permanent impact were nonlinear, buying fast and selling slowly, or the "
                    r"reverse, would make money; only a linear function forbids it"),
                why(r"so permanent impact cannot be optimised away; only the transient part depends on how one trades")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "First, permanent impact. <bookmark mark='a'/> Suppose trading at rate v moves the price permanently by f "
            "of v. <bookmark mark='b'/> Gur Huberman and Werner Stanzl showed that unless f is linear, buying fast and "
            "selling slowly, or the reverse, makes money. <bookmark mark='c'/> And with linear permanent impact the "
            "cost is one half kappa X squared whatever the schedule: it cannot be optimised away. Only the transient "
            "part depends on how one trades."
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

    def hs_example(self):
        rows = [cmath(r"f(v)", r"=", r"v\,|v|", font_size=40),
                cmath(r"\text{buy 1 in time 1}", r":", r"\Delta p = \int f(1)\,dt = 1", font_size=34, colors={r"\text{buy 1 in time 1}": BUY_C}),
                cmath(r"\text{sell 1 in time 10}", r":", r"\Delta p = -\int f(0.1)\,dt = -0.1", font_size=34,
                      colors={r"\text{sell 1 in time 10}": SELL_C}),
                cmath(r"\text{net}", r":", '\\text{cash profit 0.45; price ends } 0.9 \\text{ higher, holding nothing}', font_size=32,
                      colors={r"\text{net}": BAD})]
        whys = [why(r"suppose permanent impact grew like the square of the trading rate"),
                why(r"buying one unit fast pushes the price up by one"),
                why(r"selling it back slowly pushes it down by only a tenth"),
                why(r"so the selling happened at prices above the buying's average: repeat, and the trader is a money "
                    r"machine; a linear $f$ makes the two moves cancel exactly")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "An odd nonlinear permanent-rate illustration, f of v equals v times absolute v. <bookmark mark='a'/> Buys and sells therefore move prices in opposite directions. <bookmark mark='b'/> Buy one unit at rate one for time one: displacement rises from zero to one and average purchase displacement is one half. <bookmark mark='c'/> Sell it back at rate minus one tenth for time ten: displacement falls to point nine and average sale displacement is point nine five. <bookmark mark='d'/> With no spread, fees or noise, expected sale proceeds exceed purchase cost by point four five. Merely ending flat at a higher price would not have established profit; comparing the integrated cash flows does."
        ) as vo:
            step(0)
            for k_, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def box(self, k):
        b = k["kernels"]["box"]
        t = np.asarray(k["t"], float)
        v = np.asarray(b["round_trip"], float)
        top = float(np.abs(v).max()) * 1.15
        g = axes([0, 1], [-top, top], x_length=8.4, y_length=3.8, xlabel=r"time", ylabel=r"trades", xticks=[0, 0.5, 1],
                 yticks=[0], font_size=15).move_to(DOWN * 0.4)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.06, height=max(1e-3, abs(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=BUY_C if x > 0 else SELL_C, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(a, x / 2)) for a, x in zip(t, v)])
        st = label(rf"expected cost of this round trip: ${b['rt_cost']:.3f}$ per unit traded", font_size=20, color=BAD)
        st.to_edge(UP, buff=0.7)
        with self.voiceover(
            f"""A box kernel lasting three-tenths of the horizon. <bookmark mark='a'/> The unchanged code takes its most negative eigenvector, removes the mean so the trades sum to zero, and normalizes total absolute turnover to one. This constructs a candidate; it does not solve the exact constrained cheapest-round-trip problem. <bookmark mark='b'/> The candidate cost is {b['rt_cost']:.2f} per unit absolute turnover, negative in this frictionless linear model. Spread and other costs are omitted, but the kernel has failed this model consistency check."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def gatheral(self):
        rows = [cmath(r"\mathcal C[X] \ge 0", r"\ \forall\, X", r"\iff G\ \text{positive definite}", font_size=36),
                cmath(r"\text{spectral measure}", r"\ge", r"0", font_size=40, colors={r"0": GOOD}),
                cmath(r"\text{box kernel}", r":", r"\hat G = \text{sinc} < 0\ \text{somewhere}", font_size=36,
                      colors={r"\text{box kernel}": BAD})]
        whys = [why('all signed measures: positive definiteness; zero-total round trips alone test conditional positivity'),
                why('Bochner: a continuous even kernel is represented by a nonnegative spectral measure; a density needs extra conditions'),
                why(r"the box's transform is a sinc, negative in places, which is why the money machine exists; decaying "
                    r"exponentials and power laws pass")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Positive definiteness and round trips require a distinction. <bookmark mark='a'/> A nonnegative quadratic cost for every signed trading measure is the positive-definite condition. It is sufficient for nonnegative costs of zero-total round trips; the latter alone is conditional positive definiteness on the zero-mass subspace. <bookmark mark='b'/> For a continuous even kernel, Bochner's theorem represents positive definiteness by a nonnegative spectral measure. An ordinary Fourier density requires additional integrability or an appropriate generalized interpretation. <bookmark mark='c'/> The box transform changes sign, and our explicit zero-total candidate has negative cost. Decaying exponentials and shifted power laws with positive parameters provide useful positive-definite families."
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
        rows = [cmath(r"G\ \text{convex, decreasing}", r"\Rightarrow", r"\text{optimal } dX \ge 0", font_size=34,
                      colors={r"\text{optimal } dX \ge 0": GOOD}),
                cmath(r"G\ \text{p.d. but not convex}", r"\not\Rightarrow", r"\text{no intermediate sales}", font_size=34,
                      colors={r"\text{buy--sell oscillations}": BAD}),
                cmath(r"\text{e.g.}", r":", r"G(t) = e^{-t^2}", font_size=38)]
        whys = [why(r"Alfonsi, Schied and Slynko (2012): with a convex decreasing kernel the optimal way to buy never "
                    r"sells"),
                why(r"positive definiteness is not enough: some allowed kernels make the best purchase include sales, "
                    r"transaction-triggered price manipulation"),
                why(r"the Gaussian kernel is positive definite (its transform is Gaussian) but concave near zero")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A stronger schedule property. <bookmark mark='a'/> Under the relevant nonnegative, decreasing, convex-kernel hypotheses and well-posed trading problem, purchase optima can be chosen without intermediate sales. <bookmark mark='b'/> Positive definiteness alone does not guarantee this property. Some positive-definite kernels permit lower-cost purchases that include sales, called transaction-triggered manipulation. This differs from a negative-cost round trip. <bookmark mark='c'/> A Gaussian kernel is positive definite but concave near zero and illustrates the distinction on a finite grid; nonconvexity alone does not force every optimum to oscillate."
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

    def gauss(self, k):
        gg = [x for x in k["gauss"] if x["n"] == 11][0]
        t = np.asarray(gg["t"], float)
        v = np.asarray(gg["v"], float)
        top = float(np.abs(v).max()) * 1.15
        g = axes([-0.05, 1.05], [-top, top], x_length=8.4, y_length=3.8, xlabel=r"time", ylabel=r"trades",
                 xticks=[0, 0.5, 1], yticks=[0], font_size=15).move_to(DOWN * 0.4)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.25, height=max(1e-3, abs(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=BUY_C if x > 0 else SELL_C, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(a, x / 2)) for a, x in zip(t, v)])
        st = label(rf"to buy 1: buy {1 + gg['sell']:.2f}, sell {gg['sell']:.2f}; cost {gg['cost']:.3f} against TWAP's "
                   rf"{gg['twap']:.3f}", font_size=20, color=BAD).to_edge(UP, buff=0.7)
        with self.voiceover(
            f"""The Gaussian kernel on eleven grid dates. <bookmark mark='a'/> The unconstrained numerical optimizer buys {1+gg['sell']:.2f} units and sells {gg['sell']:.2f} back, net one. <bookmark mark='b'/> Its model cost is {gg['cost']:.3f} versus the equal-slice cost {gg['twap']:.3f}. Intermediate sales show transaction-triggered manipulation in this model, not a negative round-trip cost. A desk that requires monotone execution needs suitable kernel assumptions or an explicit no-sales constraint."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def refine(self, k):
        hx = [-3.6, -0.6, 2.2, 4.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"trading dates", r"largest trade",
                                                                         r"total sold", r"cost")])
        tab = VGroup(head)
        for r in k["gauss"]:
            tab.add(VGroup(MathTex(str(r["n"]), font_size=26), MathTex(f"{r['max']:,.2f}".replace(",", "{,}"),
                                                                        font_size=26),
                           MathTex(f"{r['sell']:,.2f}".replace(",", "{,}"), font_size=26, color=BAD),
                           MathTex(f"{r['cost']:.3f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label('Gaussian finite grids: large cancelling trades and severe conditioning; these solves do not prove a continuum existence result', 11.0, 16, GREY_A).to_edge(DOWN,
                                                                                                    buff=0.7)
        last = k["gauss"][-1]
        with self.voiceover(
            f"""Refining the Gaussian grid produces increasingly large cancelling trades. <bookmark mark='a'/> At twenty-one dates the largest computed trade is about {last['max']:,.0f} units for net quantity one. But fine Gaussian matrices are severely ill-conditioned: these floating-point solves are numerical illustrations, not a proof of the continuum infimum or nonexistence. Strict positivity on each distinct finite grid does not guarantee coercivity or attainment over all signed finite measures. Keep analytical existence results separate from this table."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def btc_passes(self, p):
        rows = [cmath(r"G(\ell)", r"=", rf"(1 + \ell/{p['G_peak_lag']})^{{-{p['beta']:.2f}}}", font_size=40,
                      colors={r"G(\ell)": KERNEL_C}),
                cmath(r"\text{decreasing, convex}", r":", r"\text{yes}", font_size=38, colors={r"\text{yes}": GOOD}),
                cmath(r"\text{positive definite}", r":", r"\text{yes (Pólya)}", font_size=38, colors={r"\text{yes (Pólya)}": GOOD})]
        whys = [why('a shifted-power-law surrogate using fitted parameters; not the raw empirical kernel'),
                why(r"its derivative is negative and its second derivative positive"),
                why('the chosen positive-parameter family meets sufficient model conditions; this does not validate the raw fit or observed market')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Now a chosen positive-parameter surrogate, not the unrestricted measured kernel. <bookmark mark='a'/> Use one plus lag over the fitted peak scale, raised to minus the positive fitted exponent {p['beta']:.2f}. This removes the initial rising section and imposes a functional family. <bookmark mark='b'/> That family is decreasing and convex for positive scale and exponent. <bookmark mark='c'/> Its even extension satisfies Polya's positive-definite criterion and appropriate no-intermediate-sale results. This validates properties of the chosen model, not a proof that the observed market or raw fitted kernel is free of manipulation."""
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

    def lessons(self):
        cards = VGroup(
            desk_question(r"test the model, not only the data", r"before an impact model drives a trading algorithm, check "
                          r"it is positive definite and, ideally, convex and decreasing", width=12.4, font_size=19),
            desk_question(r"exponential and power laws pass", r"Obizhaeva--Wang's exponential and Bouchaud's power-law "
                          r"propagator are both convex and decreasing", width=12.4, font_size=19),
            desk_question(r"nonlinear transient impact", r"with a power of the rate inside a decaying kernel, Gatheral "
                          r"showed exponential decay forces linearity, and a power-law decay must satisfy an "
                          r"inequality linking its exponent to the impact's; free choices are rare", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Lessons for model use. <bookmark mark='a'/> Check the quadratic cost functional and distinguish round-trip positivity, strict convexity, existence and monotone execution. <bookmark mark='b'/> Positive-parameter exponential and shifted-power-law families satisfy useful sufficient conditions; that does not validate their empirical calibration. <bookmark mark='c'/> With nonlinear instantaneous impact inside a transient kernel, Gatheral's no-manipulation restrictions require explicit rate, decay and admissibility assumptions. They are not a license to combine arbitrary concave impact and exponential decay."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('4. A four-leg round trip', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$G(t)=1$ for $0\\le t<\\tau$, then zero; trades $(+1,-1,+1,-1)$ spaced $0.7\\tau$.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Compute net quantity, total absolute turnover and $\\frac12 v^T\\Gamma v$.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause four. A box kernel equals one for lags below tau and zero afterwards, with unit self-impact. Trade plus one, minus one, plus one, minus one, spaced point seven tau apart. Compute net quantity, absolute turnover and the quadratic cost. Ignore spread and fees.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
