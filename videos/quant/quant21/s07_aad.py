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
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.12, run_time=3), FadeIn(side[0]))
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
        q = ask(r"AAD gives the CVA's derivative with respect to 10,000 inputs for the cost of a few valuations. What "
                r"is the catch?")
        with self.voiceover("Adjoint differentiation gives ten thousand derivatives for the cost of a few valuations. "
                            "What is the catch?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
