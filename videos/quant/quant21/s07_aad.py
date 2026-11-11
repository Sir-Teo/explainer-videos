from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import xva as XV
from videos.quant.quant21.common import BAD, CVA_C, GOOD, PART, ask, fit_right, house_lab, illustration, load


class AAD(VoiceoverScene):
    def construct(self):
        a = load("aad")
        self.card()
        self.why()
        self.tape()
        self.grads(a)
        self.lab()

    def card(self):
        c = chapter_card(6, r"Sensitivities by AAD", r"How does CVA move with every input, at once?", part=PART)
        with self.voiceover("Chapter six. Every sensitivity of CVA, from one backward pass."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why(self):
        rows = [cmath(r"\frac{\partial\,\text{CVA}}{\partial\theta_k}", r"\approx", r"\frac{\text{CVA}(\theta + h e_k) - "
                      r"\text{CVA}(\theta)}{h},\quad k = 1, \dots, n", font_size=34, colors={r"\frac{\partial\,\text{CVA}}{\partial\theta_k}": BAD}),
                cmath(r"\bar\theta", r"=", r"\Big(\frac{\partial\,\text{CVA}}{\partial\theta}\Big)^{\!\top}\ \text{in one "
                      r"reverse sweep}", font_size=36, colors={r"\bar\theta": GOOD})]
        whys = [why(r"bumping: one full revaluation, every path and date, for each of the $n$ inputs: curve nodes, "
                    r"hazard rates, volatilities. A real book has thousands"),
                why(r"adjoint differentiation (Part 16): record the computation once, run the chain rule backwards, and "
                    r"every derivative arrives at a small constant multiple of the cost of one valuation")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "An XVA desk hedges its CVA, and for that it needs the sensitivity to every input: each point of the yield "
            "curve, each point of each counterparty's credit curve. By bumping, that is one full simulation per "
            "input, and a real book has thousands of them. <bookmark mark='a'/> Part sixteen's adjoint method gives "
            "them all at once: run the valuation forwards, then the chain rule backwards, and every derivative "
            "comes out for a few times the cost of one valuation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def tape(self):
        lam, t, ee, D, R = 0.02, 5.0, 4.0, 0.82, 0.4
        S = np.exp(-lam * t)
        PD = 1 - S
        cva = (1 - R) * ee * PD * D
        b_pd = (1 - R) * ee * D
        b_s = -b_pd
        b_lam = b_s * (-t * S)
        b_ee = (1 - R) * PD * D

        def node(tex, val, pos, col=WHITE):
            box = RoundedRectangle(corner_radius=0.12, width=2.5, height=1.05, stroke_color=col, stroke_width=2,
                                   fill_opacity=0).move_to(pos)
            top = MathTex(tex, font_size=28, color=col).move_to(box.get_center() + UP * 0.2)
            v = MathTex(val, font_size=24, color=GREY_A).move_to(box.get_center() + DOWN * 0.25)
            return VGroup(box, top, v)
        n_lam = node(r"\lambda", f"{lam:.2f}", [-5.2, 1.0, 0], BAD)
        n_ee = node(r"\text{EE}", f"{ee:.1f}", [-5.2, -1.4, 0], BAD)
        n_s = node(r"S = e^{-\lambda t}", f"{S:.3f}", [-1.9, 1.0, 0])
        n_pd = node(r"\text{PD} = 1 - S", f"{PD:.3f}", [1.3, 1.0, 0])
        n_c = node(r"\text{CVA}", f"{cva:.3f}", [4.6, -0.2, 0], QC.LOSS)
        nodes = [n_lam, n_ee, n_s, n_pd, n_c]
        edges = [(n_lam, n_s), (n_s, n_pd), (n_pd, n_c), (n_ee, n_c)]
        arrows = VGroup(*[Arrow(a_.get_right(), b_.get_left(), buff=0.08, color=GREY_B, stroke_width=3) for a_, b_ in edges])
        adj = [(n_c, r"\bar{c} = 1"), (n_pd, rf"\bar{{\text{{PD}}}} = (1-R)\,\text{{EE}}\,D = {b_pd:.2f}"),
               (n_s, rf"\bar S = -\bar{{\text{{PD}}}} = {b_s:.2f}"),
               (n_lam, rf"\bar\lambda = \bar S\cdot(-t S) = {b_lam:.1f}"),
               (n_ee, rf"\bar{{\text{{EE}}}} = (1-R)\,\text{{PD}}\,D = {b_ee:.3f}")]
        adjs = VGroup(*[MathTex(tx, font_size=22, color=GOOD).next_to(n_, DOWN if n_ is not n_ee else UP, buff=0.15)
                        for n_, tx in adj])
        adjs[0].next_to(n_c, DOWN, buff=0.15)
        adjs[4].next_to(n_ee, DOWN, buff=0.15)
        title = label(r"One default bucket: forward values, then adjoints backwards", font_size=26).to_edge(UP, buff=0.4)
        foot = wrapped_label(rf"$t$ = {t:g} years, discount $D$ = {D}, recovery {int(100 * R)}\%. Check: "
                             rf"$\partial\,\text{{CVA}}/\partial\lambda = (1-R)\,\text{{EE}}\,D\,t\,e^{{-\lambda t}}$ = "
                             rf"{(1 - R) * ee * D * t * S:.1f}. Every node is visited once each way, whatever the "
                             r"number of inputs", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How does one backward pass give every derivative? Take a single bucket of the CVA sum. "
            "<bookmark mark='a'/> Going forward, each step is computed and written down: the survival from the "
            "hazard rate, the default probability, and the CVA from that and the expected exposure. "
            "<bookmark mark='b'/> Now go backwards. Start with the derivative of the CVA with respect to itself, "
            "one. Each node passes back its own adjoint times its local derivative: the default probability's "
            f"adjoint is {b_pd:.2f}; the survival's is minus that; <bookmark mark='c'/> and the hazard rate's is "
            f"that times minus t times the survival, {b_lam:.1f}. The exposure gets its adjoint in the same sweep. "
            "<bookmark mark='d'/> Each node is visited once forwards and once backwards, however many inputs feed "
            "it. That is why the cost does not grow with the number of sensitivities, and why the memory does: "
            "every intermediate value of the forward pass must be kept for the way back."
        ) as vo:
            self.play(FadeIn(title), FadeIn(n_lam), FadeIn(n_ee))
            vo.wait_until("a")
            self.play(LaggedStart(GrowArrow(arrows[0]), FadeIn(n_s), GrowArrow(arrows[1]),
                                  FadeIn(n_pd), GrowArrow(arrows[2]), GrowArrow(arrows[3]), FadeIn(n_c),
                                  lag_ratio=0.35, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(adjs[0]), Indicate(n_c, color=GOOD))
            self.play(FadeIn(adjs[1]), Indicate(n_pd, color=GOOD))
            self.play(FadeIn(adjs[2]), Indicate(n_s, color=GOOD))
            vo.wait_until("c")
            self.play(FadeIn(adjs[3]), Indicate(n_lam, color=GOOD))
            self.play(FadeIn(adjs[4]), Indicate(n_ee, color=GOOD))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def grads(self, a):
        zt, gz, bz = np.asarray(a["zt"]), np.asarray(a["grad_zero"]) * 1e-4 * 1e3, np.asarray(a["bump_zero"]) * 1e-4 * 1e3
        gh, bh = np.asarray(a["grad_hazard"]) * 1e-4 * 1e3, np.asarray(a["bump_hazard"]) * 1e-4 * 1e3
        names = [f"{t:g}y" for t in zt] + [f"h{int(k)}y" for k in a["hazard_t"]]
        vals_a, vals_b = np.r_[gz, gh], np.r_[bz, bh]
        hx = [-4.6, -1.6, 1.4]
        head = VGroup(label(r"input", font_size=18, color=GREY_A), label(r"AAD, \$k per bp", font_size=18, color=GOOD),
                      label(r"bump, \$k per bp", font_size=18, color=BAD))
        for h_, x in zip(head, hx):
            h_.move_to([x, 2.6, 0])
        rows = VGroup()
        sel = [i for i in range(len(names)) if abs(vals_b[i]) > 1e-6]
        for r_i, i in enumerate(sel):
            y = 2.05 - 0.42 * r_i
            rows.add(VGroup(label(rf"zero {names[i]}" if i < len(zt) else rf"hazard to {names[i][1:]}", font_size=17
                                  ).move_to([hx[0], y, 0]),
                            MathTex(f"{vals_a[i]:+.3f}", font_size=24, color=GOOD).move_to([hx[1], y, 0]),
                            MathTex(f"{vals_b[i]:+.3f}", font_size=24, color=BAD).move_to([hx[2], y, 0])))
        side = VGroup(
            MathTex(rf"\text{{CVA}} = \${1e3 * a['cva']:.0f}\text{{k}}", font_size=28, color=CVA_C),
            MathTex(rf"\text{{AAD: }} {a['t_aad']:.1f}\,\text{{s}}\quad \text{{bumping: }} {a['t_bump']:.1f}\,\text{{s}}",
                    font_size=26),
            wrapped_label(rf"{a['n_inputs']} inputs here; the bumps cost one revaluation each, AAD one backward pass. "
                          r"Same random numbers in every run, so the two agree to the digits shown", 3.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The netting set's CVA, written in torch, with its derivative with respect to every zero-rate node and "
            "every hazard rate. <bookmark mark='a'/> Each derivative from the backward pass, beside the same "
            "derivative by bumping that input by a basis point. They agree. <bookmark mark='b'/> The backward pass "
            f"took {a['t_aad']:.1f} seconds; the bumps, {a['t_bump']:.0f}, for only {a['n_inputs']} inputs. For a "
            "bank's book, with thousands, that difference decides whether risk is known overnight or not at all."
        ) as vo:
            self.play(FadeIn(head),
                      LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.12, run_time=3), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=GOOD))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"CVA in torch: one backward pass", XV.cva_torch, "EE = torch.clamp", 6, width=7.8)
        card.to_edge(UP, buff=0.5)
        with self.voiceover(
            "The end of the House's implementation: expected exposure from the simulated values, survival from the "
            "hazards, the CVA as a sum, and one call to backward. Everything above that line is ordinary pricing "
            "code; the derivatives come with it."
        ):
            self.play(FadeIn(card))
        q = ask(r"exposure is $\max(V, 0)$, and a digital option's payoff jumps. What does a backward pass get wrong "
                r"at a kink or a jump, and how would you fix it?")
        with self.voiceover("Exposure takes the positive part of the value, and some payoffs jump. What does a backward "
                            "pass get wrong at a kink or a jump, and how would you fix it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
