from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, PART, REF, axes, data_range, load

N_COL = {"5": BAD, "10": QC.THETA, "20": QC.IMPLIED, "40": GOOD}


class Research(VoiceoverScene):
    def construct(self):
        t = load("aposteriori")
        self.card()
        self.identity()
        self.euler()
        self.theorem()
        self.curves(t)
        self.floors(t)
        self.nonlinear(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"From population loss to a price-error bound",
                          r"What does the theorem say, and what did the training log measure?", part=PART)
        with self.voiceover(
            "For the researcher: distinguish a theorem about population loss from a moving average of training batches. The continuous-time identity, the Euler scheme and a nonlinear error estimate answer different questions."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def identity(self):
        rows = [
            cmath(r"dY_t", r"=", r"RY_t\,dt+Z_t\cdot dW_t,\quad Y_0=y_0", font_size=32),
            cmath(r"g(X_T)", r"=", r"e^{RT}u_0+\int_0^T e^{R(T-t)}Z_t^*\cdot dW_t", font_size=30),
            cmath(r"L_{\rm pop}", r"=", r"e^{2RT}(y_0-u_0)^2+\mathbb E\!\int_0^T e^{2R(T-t)}|Z_t-Z_t^*|^2dt", font_size=27),
            cmath(r"|y_0-u_0|", r"\le", r"e^{-RT}\sqrt{L_{\rm pop}}", font_size=34, colors={r"\le": GOOD}),
        ]
        whys = [why(r"linear continuous-time process; fixed deterministic $y_0$ and a predictable square-integrable $Z$"),
                why(r"$u_0=e^{-RT}\mathbb E[g(X_T)]$; martingale representation in the Brownian filtration, with square-integrable payoff"),
                why(r"$L_{\rm pop}=\mathbb E|Y_T-g(X_T)|^2$: subtract and apply It\^o isometry; the stochastic integral has mean zero"),
                why(r"a price-only population bound for a fixed candidate process; empirical loss and changing training iterates require separate statistical control")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.1, buff=0.5, edge=6.8)
        with self.voiceover(
            "Take the linear continuous-time equation, a fixed starting value and a predictable square-integrable candidate exposure. <bookmark mark='a'/> The discounted square-integrable payoff has a Brownian martingale representation. <bookmark mark='b'/> Subtract the two terminal values. The deterministic price error is orthogonal to the mean-zero stochastic integral, giving this population squared-loss identity. <bookmark mark='c'/> Dropping the nonnegative exposure-error term bounds the starting-price error. This is an expectation for a fixed candidate process. A measured batch loss, or an average over changing network weights, is a different quantity."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.clear_scene()

    def euler(self):
        body = VGroup(
            MathTex(r"Y_{k+1}=aY_k+Z_k\cdot\Delta W_k,\qquad a=1+Rh>0,\quad Nh=T", font_size=30),
            MathTex(r"\mathbb E[Y_N-g]=a^N y_0-e^{RT}u_0", font_size=32),
            MathTex(r"\left|e^{-RT}a^Ny_0-u_0\right|\le e^{-RT}\sqrt{L_{\rm pop}^{\rm Euler}}", font_size=32, color=GOOD),
        ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Euler changes the centre", body,
                            who=r"fixed predictable exposures; $L_{\rm pop}^{\rm Euler}=\mathbb E|Y_N-g|^2$", width=12.3)
        with self.voiceover(
            "The saved solver uses Euler drift steps. With a equal to one plus R h, its expected terminal value is a to the N times the starting value. Jensen's inequality therefore bounds the error of the reweighted starting value shown here. It does not give the identical continuous-time bound around the unadjusted starting value. A finite grid changes the centre even before exposure approximation. The batch losses in the next plots are moving training diagnostics, not known population losses for fixed weights."
        ):
            self.play(FadeIn(card))
        self.clear_scene()

    def theorem(self):
        body = VGroup(
            MathTex(r"\begin{aligned}\sup_t\mathbb E|Y_t-\hat Y_t|^2+\mathbb E\!\int_0^T|Z_t-\hat Z_t|^2dt"
                    r"\ &\le C\big[h+L_{\rm pop}^{\pi}\big]\end{aligned}", font_size=28),
            wrapped_label(r"Square-integrable data, Lipschitz/growth and time-regularity assumptions; sufficient weak coupling or monotonicity, and a sufficiently small time step. The full theorem also controls the forward process.", 10.7, 21, GREY_A),
        ).arrange(DOWN, buff=0.35)
        thm = theorem_card(r"A conditional a posteriori estimate", body,
                           who=r"Han--Long (2020), Theorem 1$'$; DOI 10.1186/s41546-020-00047-w", width=12.3)
        with self.voiceover(
            "Han and Long prove a population error estimate under their regularity, integrability and sufficient weak-coupling or monotonicity conditions, for sufficiently small time steps. <bookmark mark='a'/> The constant and the time-step term matter. This is not a theorem that every Lipschitz model and every numerical grid share a usable constant. <bookmark mark='b'/> Turning it into a numerical certificate needs justified constants and statistical control of a fixed model's population loss. The continuous linear price-only coefficient is not the constant for the whole-solution norm."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Indicate(body[0], scale_factor=1.03))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def curves(self, t):
        yr = data_range(*[np.log10(t["runs"][N][k]) for N in N_COL for k in ("err", "bound")])
        g = axes([0, 3000], yr, x_length=8.0, y_length=4.2, xlabel=r"training iteration",
                 ylabel=r"$\log_{10}$: reference gap / batch-loss scale", xticks=[0, 1000, 2000, 3000],
                 yticks=list(range(int(np.ceil(yr[0])), int(np.floor(yr[1]))+1)), font_size=14).move_to(LEFT*1.5+DOWN*0.2)
        lines = VGroup()
        for N, col in N_COL.items():
            r = t["runs"][N]
            lines.add(VGroup(curve(g.ax, r["iter"], np.log10(r["err"]), col, stroke_width=2.5),
                             DashedVMobject(curve(g.ax, r["iter"], np.log10(r["bound"]), col, stroke_width=2.5), num_dashes=40)))
        side = VGroup(legend([(col, rf"$N={N}$, one seed") for N, col in N_COL.items()], font_size=16),
                      wrapped_label(rf"{t['d']} assets; reference {t['reference']:.3f}, MC SE {t['reference_se']:.3f}. Solid: absolute reference gap. Dashed: discounted square root of a trailing average of 20 logged batch losses. These are diagnostics, not certified bounds.", 3.6, 17, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.25)
        with self.voiceover(
            "The saved ten-dimensional experiment uses four grids and a different training seed for each. The reference is a two-million-path Monte Carlo estimate with its own standard error. <bookmark mark='a'/> Solid curves show absolute gaps to that estimate. Dashed curves reuse the discounted square root of twenty logged batch losses, averaged across changing iterates. They omit the Euler centre correction and statistical uncertainty. <bookmark mark='b'/> A dashed curve lying above a solid one in these runs does not validate a certificate. The observed separation illustrates why population exposure-error bounds may be loose for price, while leaving the empirical and discretization questions open."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(v) for v in lines], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[Indicate(v[1], scale_factor=1.02) for v in lines])
        self.clear_scene()

    def floors(self, t):
        headings = [r"steps $N$", r"batch loss avg", r"discounted $\sqrt{\rm avg}$", r"mean ref. gap", r"seconds"]
        rows = [VGroup(*[label(v, font_size=18, color=GREY_A) for v in headings])]
        for N in N_COL:
            r = t["runs"][N]
            rows.append(VGroup(MathTex(N, font_size=28), MathTex(f"{r['floor']:.1f}", font_size=28),
                               MathTex(f"{t['disc']*np.sqrt(r['floor']):.2f}", font_size=28),
                               MathTex(f"{r['final_err']:.3f}", font_size=28, color=GOOD),
                               MathTex(f"{r['seconds']:.0f}", font_size=28)))
        for j, row in enumerate(rows):
            for x, cell in zip([-4.8, -2.2, 0.5, 3.0, 5.2], row):
                cell.move_to([x, 1.7-0.72*j, 0])
        foot = wrapped_label(r"Loss average: last 40 logged training batches. Reference gap: last 20 logged starting values. Different grids also use different seeds and update costs. Neither column is a confidence interval or an isolated discretization-error estimate.", 12.3, 20, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Read the summaries literally. <bookmark mark='a'/> The loss column averages forty logged training batches; the reference-gap column averages twenty logged starting values. Neither describes one frozen candidate evaluated with unlimited fresh samples. Changing the grid also changes the seed and the work per update. <bookmark mark='b'/> A small reference gap can coexist with a much larger loss scale. The continuous identity explains one possible source of that separation, but these moving batch averages do not isolate exposure error, time-step error or optimization error."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(*row[:3], row[4])) for row in rows[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(row[3]) for row in rows[1:]])
        self.clear_scene()

    def nonlinear(self, t):
        n = t["nonlinear"]
        it, u, L = (np.asarray(n[k], float) for k in ("iter", "u0", "loss"))
        k = 10
        sm = np.convolve(L, np.ones(k), mode="full")[:len(L)]/np.minimum(np.arange(1, len(L)+1), k)
        up, dn = u+np.sqrt(sm), u-np.sqrt(sm)
        yr = data_range(up, dn, u, [n["reference"]])
        g = axes([0, it.max()], yr, x_length=8.0, y_length=4.2, xlabel=r"training iteration",
                 ylabel=r"100-asset default-risk starting value", xticks=[0, 500, 1000, 1500, 2000],
                 yticks=[round(v) for v in np.linspace(*yr, 4)[1:-1]], font_size=14).move_to(LEFT*1.5+DOWN*0.2)
        band = Polygon(*[g.ax.c2p(a,b) for a,b in zip(it,up)], *[g.ax.c2p(a,b) for a,b in zip(it[::-1],dn[::-1])],
                       stroke_width=0, fill_color=NET, fill_opacity=0.18)
        line = curve(g.ax, it, u, NET, stroke_width=3)
        ref = DashedLine(g.ax.c2p(0,n["reference"]),g.ax.c2p(it.max(),n["reference"]),color=REF,stroke_width=2)
        side = wrapped_label(r"Seed 1. Full, unclipped $y_0\pm\sqrt{\text{trailing batch-loss average}}$. Unit coefficient chosen for illustration; no confidence level; omits the theorem's constant and time-step term. Published reference is approximate.", 3.6, 18, GREY_A).to_edge(RIGHT,buff=0.25)
        with self.voiceover(
            "For the nonlinear hundred-dimensional run, retain the full shaded range. <bookmark mark='a'/> The line is the trained starting value and the white line is the published approximate reference. <bookmark mark='b'/> The shading uses plus or minus square root of a trailing ten-log batch-loss average with an arbitrary unit coefficient. It supplies neither a confidence level nor the theorem's constant or time-step correction. Inclusion of the reference in such an illustrative band would not establish coverage or certify the solver."
        ) as vo:
            self.play(FadeIn(g),Create(ref),FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line))
            vo.wait_until("b")
            self.play(FadeIn(band))
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"Sharper validation", r"Can price and exposure errors be separated, with justified constants and fresh-sample uncertainty?",width=12.3,font_size=21),
            desk_question(r"Optimization and refinement", r"How do architecture, grid and optimization interact at the accuracy and cost needed for a product?",width=12.3,font_size=21),
            desk_question(r"Auditable evidence", r"Can a fixed model's loss and numerical assumptions be checked well enough to support a practical bound?",width=12.3,font_size=21),
        ).arrange(DOWN,buff=0.25)
        with self.voiceover(
            "Three research directions, rather than claims that no theory exists. <bookmark mark='a'/> Separate price and exposure errors while controlling constants and fresh-sample uncertainty. <bookmark mark='b'/> Understand the interaction of optimization, architecture and time refinement at a useful cost. <bookmark mark='c'/> Build auditable bounds for fixed models and specific products. A theorem, a training diagnostic and a production validation decision each require their own evidence."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for i,m in enumerate(("a","b","c")):
                vo.wait_until(m)
                self.play(Indicate(cards[i], scale_factor=1.02) if i == 0 else FadeIn(cards[i]))
        self.clear_scene()

    def question(self):
        q = desk_question(r"Pause and predict", r"A fixed continuous-time linear candidate has known population loss $9$, $R=2\%$ and $T=1$. What price-only bound follows? What if $Z=Z^*$?",width=12.0,font_size=23).move_to(UP*1.35)
        answer = theorem_card(r"Worked answer: population, continuous time", VGroup(
            MathTex(r"|y_0-u_0|\le 3e^{-0.02}\approx2.9406",font_size=32,color=GOOD),
            MathTex(r"Z=Z^*\quad\Rightarrow\quad L_{\rm pop}=e^{0.04}(y_0-u_0)^2",font_size=30),
            wrapped_label(r"An empirical batch loss of 9 alone gives no such numerical certificate.",10.5,21,GREY_A),
        ).arrange(DOWN,buff=0.25),width=12.0).next_to(q,DOWN,buff=0.45)
        with self.voiceover(
            "Pause and predict. A fixed continuous-time linear candidate has known population squared loss nine, at two percent over one year. What price-only bound follows? If the true continuous-time exposure were used, what would the loss become?"
        ):
            self.play(FadeIn(q))
        self.wait(2.5)
        with self.voiceover(
            "The price error is at most three times e to minus zero point zero two, about two point nine four zero six. With the true continuous-time exposure, the exposure-error integral vanishes, leaving e to zero point zero four times the squared price error. These statements require the stated population quantity and continuous-time process. A sampled training loss of nine alone does not provide that certificate."
        ):
            self.play(FadeIn(answer))
        self.wait(6)
