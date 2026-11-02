from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, OPT, PART, SPOT, VEGA, illustration, load


class Greeks(VoiceoverScene):
    def construct(self):
        g = load("greeks")
        self.card()
        self.three(g)
        self.tape()
        self.cost(g)

    def card(self):
        c = chapter_card(5, r"Greeks, and adjoint differentiation", r"Why is AAD's cost independent of the number of Greeks?",
                         part=PART)
        with self.voiceover("Chapter five. Greeks, and adjoint differentiation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def three(self, g):
        ex = g["exact"]
        head = VGroup(label(r"", font_size=20), label(r"call: delta", font_size=21, color=GREY_A),
                      label(r"digital: delta", font_size=21, color=GREY_A))
        rows = [(r"bump and reprice", "bump", BAD), (r"pathwise", "pathwise", GOOD), (r"likelihood ratio", "likelihood ratio", OPT)]
        tab = VGroup(VGroup(VectorizedPoint(), head[1], head[2]))
        for name, key, col in rows:
            c = g["call"].get(key)
            d = g["digital"].get(key)
            cells = [label(name, font_size=22, color=col)]
            cells.append(MathTex(rf"{c['delta']:.4f} \pm {c['delta_se']:.4f}", font_size=26) if c else
                         MathTex(r"-", font_size=26))
            cells.append(MathTex(rf"{d['delta']:.4f} \pm {d['delta_se']:.4f}", font_size=26) if d else
                         label(r"fails: the payoff jumps", font_size=19, color=BAD))
            tab.add(VGroup(*cells))
        tab.add(VGroup(label(r"exact", font_size=22, color=GREY_A), MathTex(f"{ex['call']['delta']:.4f}", font_size=26, color=GREY_A),
                       MathTex(f"{ex['digital']['delta']:.4f}", font_size=26, color=GREY_A)))
        xs = [-4.2, 0.2, 4.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.3 - 0.75 * i, 0])
        foot = wrapped_label(r"bumping reprices with the input nudged (biased, and noisy for jumps); pathwise differentiates the "
                             r"payoff along each path (low noise, but needs a continuous payoff); the likelihood ratio "
                             r"differentiates the density instead (works for any payoff, noisier) (Broadie and Glasserman "
                             r"1996)", 11.6, 19, GREY_A).to_edge(DOWN, buff=0.5)
        src = illustration(r"200{,}000 paths, common random numbers", corner=UR)
        with self.voiceover(
            "A desk needs sensitivities as much as prices, and Monte Carlo offers three ways to get them. Bump an "
            "input and reprice, with the same random numbers. Differentiate the payoff along each path, the pathwise "
            "method. Or differentiate the probability density instead, the likelihood ratio. <bookmark mark='a'/> For "
            "a call all three agree; pathwise is the least noisy. <bookmark mark='b'/> For a digital, the payoff jumps, "
            "and the pathwise derivative is zero almost everywhere: it fails. The likelihood ratio does not care, "
            "because it never differentiates the payoff. Mark Broadie and Paul Glasserman laid this out in 1996."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def tape(self):
        names = [r"S_0", r"\sigma", r"r", r"T"]
        ins = VGroup(*[MathTex(n, font_size=34) for n in names]).arrange(DOWN, buff=0.7).to_edge(LEFT, buff=1.2)
        mids = VGroup(*[Circle(radius=0.32, stroke_color=GREY_B, stroke_width=2) for _ in range(5)])
        mids.arrange(DOWN, buff=0.45).move_to(LEFT * 1.0)
        mids2 = VGroup(*[Circle(radius=0.32, stroke_color=GREY_B, stroke_width=2) for _ in range(3)])
        mids2.arrange(DOWN, buff=0.7).move_to(RIGHT * 1.6)
        out = MathTex(r"V", font_size=40, color=OPT).move_to(RIGHT * 4.2)
        fwd = VGroup()
        for a in ins:
            for b in mids[::2] if a is ins[0] else mids[1::2]:
                fwd.add(Arrow(a.get_right(), b.get_left(), buff=0.1, stroke_width=2, color=SPOT, tip_length=0.12))
        for k_, a in enumerate(mids):
            fwd.add(Arrow(a.get_right(), mids2[k_ * 3 // 5].get_left(), buff=0.05, stroke_width=2, color=SPOT,
                          tip_length=0.12))
        for a in mids2:
            fwd.add(Arrow(a.get_right(), out.get_left(), buff=0.1, stroke_width=2, color=SPOT, tip_length=0.12))
        back = VGroup(*[Arrow(a.get_end(), a.get_start(), buff=0.0, stroke_width=3, color=DELTA, tip_length=0.14)
                        for a in fwd])
        grads = VGroup(*[MathTex(rf"\bar{{{n}}}", font_size=30, color=DELTA).next_to(i_, LEFT, buff=0.2)
                         for n, i_ in zip(names, ins)])
        cap = VGroup(label(r"forward: compute the price, record every operation on a tape", font_size=21, color=SPOT),
                     label(r"backward: one sweep sends $\partial V/\partial(\cdot)$ to every input at once", font_size=21,
                           color=DELTA)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bumping costs one extra pricing per input, and a real book has thousands of inputs. Adjoint "
            "differentiation, AAD, removes that dependence. Run the pricing forward once, and record every operation on "
            "a tape. <bookmark mark='a'/> Then sweep the tape backwards, from the price to the inputs, applying the "
            "chain rule at each step. One backward sweep delivers the derivative with respect to every input at once. "
            "Mike Giles and Paul Glasserman brought it to Monte Carlo in 2006 as smoking adjoints. It is the same "
            "reverse-mode differentiation that trains every neural network, and the House runs it with the series' "
            "own autodiff from the AI series."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(mids), FadeIn(mids2), FadeIn(out), LaggedStart(*[GrowArrow(a) for a in fwd],
                                                                                         lag_ratio=0.03, run_time=2.5),
                      FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(FadeOut(fwd), LaggedStart(*[GrowArrow(a) for a in reversed(back)], lag_ratio=0.03, run_time=2.5),
                      FadeIn(cap[1]))
            self.play(FadeIn(grads))
        self.wait(0.4)
        self.clear_scene()

    def cost(self, g):
        a = g["aad"]
        names = {"delta": r"\partial S_0", "vega": r"\partial\sigma", "rho": r"\partial r", "theta_T": r"\partial T",
                 "dK": r"\partial K"}
        tab = VGroup(VGroup(label(r"sensitivity", font_size=21, color=GREY_A), label(r"AAD (one sweep)", font_size=21, color=GREY_A),
                            label(r"bump and reprice", font_size=21, color=GREY_A)))
        for k, n in names.items():
            tab.add(VGroup(MathTex(n, font_size=28), MathTex(f"{a['aad'][k]:.4f}", font_size=28, color=DELTA),
                           MathTex(f"{a['bump'][k]:.4f}", font_size=28)))
        xs = [-4.4, -1.0, 2.4]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.4 - 0.62 * i, 0])
        n = g["n_greeks"]
        side = VGroup(
            MathTex(rf"\text{{AAD: all {n} for}}\ {g['aad_ratio']:.1f}\times\ \text{{a price}}", font_size=30, color=GOOD),
            MathTex(rf"\text{{bumping:}}\ {g['bump_ratio']:.0f}\times", font_size=30, color=BAD),
            wrapped_label(r"the AAD cost ratio stays a small constant however many inputs there are: a whole yield curve, "
                          r"a whole surface. Bumping grows with each one", 4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"an arithmetic Asian call, 50 fixings, 20{,}000 paths; the series' autodiff, pure numpy")
        with self.voiceover(
            "Here it is on an Asian option priced by twenty thousand paths. All five sensitivities from one backward "
            "sweep, matching the bumped values. <bookmark mark='a'/> The sweep cost "
            f"{g['aad_ratio']:.1f} times one price; bumping all five cost {g['bump_ratio']:.0f} times. With five inputs "
            "the saving is modest. With a yield curve of fifty points, or a volatility surface of five hundred, AAD's "
            "ratio stays the same and bumping grows with every input. That is why banks rebuilt their risk systems "
            "around it."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
