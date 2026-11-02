from __future__ import annotations

import numpy as np

from explainer.ai.autodiff import Tensor, topological_order
from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, OPT, PART, SPOT, illustration, load, polyline, predict

OPS = {"+": "+", "neg": r"-", "*": r"\times", "exp": r"\exp", "relu": r"(\cdot)^+", "**": r"\surd", "pow": r"\surd",
       "input": r"\text{in}"}


def one_path_tape(z=0.5):
    """A one-path call price on the series' autodiff: its tape, every node's value, and every node's adjoint."""
    S0, sig, r, T, K = (Tensor(np.array(v), requires_grad=True) for v in (100.0, 0.2, 0.05, 1.0, 100.0))
    drift = (r - sig * sig * 0.5) * T
    vol = sig * (T ** 0.5)
    ST = S0 * (drift + vol * z).exp()
    V = (r * T * -1.0).exp() * (ST - K).relu()
    order = topological_order(V)
    adj = {id(V): np.ones_like(V.data)}
    for t in reversed(order):
        g = adj.get(id(t))
        if g is None:
            continue
        for p, f in t.parents:
            adj[id(p)] = adj.get(id(p), 0) + f(g)
    names = {id(S0): r"S_0", id(sig): r"\sigma", id(r): r"r", id(T): r"T", id(K): r"K"}
    rows = [{"op": names.get(id(t), r"\surd" if (t.op or "").startswith("**") else OPS.get(t.op or "input", t.op)), "val": float(t.data), "adj": float(adj.get(id(t), 0.0)),
             "leaf": id(t) in names} for t in order]
    return rows


class AAD(VoiceoverScene):
    def construct(self):
        g = load("greeks")
        s = load("aad_scale")
        self.card()
        self.tape()
        self.proof()
        self.lab(g)
        self.scaling(s)

    def card(self):
        c = chapter_card(11, r"Adjoint differentiation: every Greek for a few prices", r"Why is AAD's cost independent of "
                         r"the number of Greeks?", lit=(2006,), part=PART)
        with self.voiceover("Chapter eleven. Adjoint differentiation: every Greek for the price of a few."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tape(self):
        rows = one_path_tape()
        n = len(rows)
        w = min(0.78, 12.8 / n)
        cells = VGroup()
        for r in rows:
            box = Rectangle(width=w, height=1.9, stroke_color=GREY_C, stroke_width=1.2, fill_color="#0E141C",
                            fill_opacity=1)
            op = MathTex(r["op"], font_size=24, color=SPOT if r["leaf"] else GREY_A)
            val = MathTex(f"{r['val']:.3g}", font_size=17, color=WHITE)
            adj = MathTex(f"{r['adj']:.3g}", font_size=17, color=DELTA)
            cells.add(VGroup(box, op, val, adj))
        cells.arrange(RIGHT, buff=0.04).move_to(DOWN * 0.2)
        for c in cells:
            c[1].move_to(c[0].get_top() + DOWN * 0.35)
            c[2].move_to(c[0].get_center())
            c[3].move_to(c[0].get_bottom() + UP * 0.35)
            if c[2].width > w - 0.06:
                c[2].scale_to_fit_width(w - 0.06)
            if c[3].width > w - 0.06:
                c[3].scale_to_fit_width(w - 0.06)
        lab = VGroup(label(r"each cell: the operation (top), its forward value (middle),", font_size=18, color=GREY_B),
                     label(r"and its adjoint $\bar v = \partial V / \partial v$ (bottom)", font_size=18, color=DELTA)
                     ).arrange(RIGHT, buff=0.15).next_to(cells, DOWN, buff=0.55)
        head = label(r"the tape of one path's call price, $V = e^{-rT}\big(S_0 e^{(r - \sigma^2/2)T + \sigma\sqrt T z} - K\big)^+$, "
                     r"$z = 0.5$", font_size=22, color=GREY_A).to_edge(UP, buff=0.5)
        leaves = {r["op"]: r for r in rows if r["leaf"]}
        res = MathTex(rf"\bar S_0 = {leaves['S_0']['adj']:.4f},\ \ \bar\sigma = {leaves[chr(92) + 'sigma']['adj']:.2f},\ \ "
                      rf"\bar r = {leaves['r']['adj']:.2f},\ \ \bar T = {leaves['T']['adj']:.2f},\ \ \bar K = {leaves['K']['adj']:.4f}",
                      font_size=28, color=DELTA).to_edge(DOWN, buff=0.35)
        fwd = Arrow(cells[0].get_top() + UP * 0.25, cells[-1].get_top() + UP * 0.25, buff=0, stroke_width=3, color=SPOT)
        bwd = Arrow(cells[-1].get_bottom() + DOWN * 0.25, cells[0].get_bottom() + DOWN * 0.25, buff=0, stroke_width=3,
                    color=DELTA)
        with self.voiceover(
            "Bumping costs one extra pricing per input, and a real book has thousands of inputs. Adjoint "
            "differentiation removes that dependence. Here it is on the smallest possible case: one path of a call "
            "priced by the series' own autodiff. <bookmark mark='a'/> The forward pass computes the price and "
            "records every operation on a tape: the five inputs, then the multiplications, the exponential, the "
            "payoff's kink, the discount. <bookmark mark='b'/> Then the backward sweep. Seed the price's adjoint with "
            "one and walk the tape from right to left. Each node passes its adjoint to its inputs, multiplied by its "
            "local derivative: the chain rule, applied once per edge. <bookmark mark='c'/> When the sweep reaches the "
            "left end, all five sensitivities are there at once: delta, vega, rho, the time derivative and the strike "
            "sensitivity, for one backward pass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[c[0] for c in cells])), FadeIn(lab))
            vo.wait_until("a")
            self.play(GrowArrow(fwd))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[1]), FadeIn(c[2])) for c in cells], lag_ratio=0.25,
                                  run_time=4))
            vo.wait_until("b")
            self.play(GrowArrow(bwd))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[3]), Indicate(c[0], color=DELTA, scale_factor=1.04))
                                    for c in reversed(cells)], lag_ratio=0.25, run_time=5))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\nabla y^\top", r"=", r"\bar y\;J_f\,J_g\,J_h,\qquad y = f(g(h(x))),\ x \in \mathbb{R}^n", font_size=34,
                  colors={r"\nabla y^\top": DELTA}),
            cmath(r"\text{forward: } J_f\big(J_g(J_h\,\dot x)\big)", r"\quad", r"\text{reverse: } \big((\bar y J_f)J_g\big)J_h",
                  font_size=32),
            cmath(r"\bar v_i", r"=", r"\sum_{j:\,i \to j} \bar v_j\,\frac{\partial v_j}{\partial v_i}", font_size=36,
                  colors={r"\bar v_i": DELTA}),
            cmath(r"\text{cost}(\nabla f)", r"\le", r"\omega\cdot\text{cost}(f),\quad \omega \approx 3\text{--}5,\ "
                  r"\text{independent of } n", font_size=32, colors={r"\le": GOOD}),
        ]
        whys = [why(r"the chain rule as a product of Jacobians"),
                why(r"forward mode carries one input direction per pass ($n$ passes); reverse mode carries one row for "
                    r"the scalar output (one pass): associativity, nothing else"),
                why(r"the adjoint recursion: each node visited once, one multiply--add per edge of the tape"),
                why(r"Griewank's cheap gradient principle (Griewank and Walther, \textit{Evaluating Derivatives}, 2008); "
                    r"Giles and Glasserman's ``smoking adjoints'' (2006) applied it path by path to Monte Carlo; "
                    r"Capriotti (2011) generalised it to any pricing code")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
        q = predict(r"A swap book has 2{,}000 curve points. Bumping costs 4{,}000 prices. AAD costs about?", width=5.0,
                    font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Why it is cheap. The gradient of a composition is a product of Jacobians. <bookmark mark='a'/> Multiply "
            "from the right, and you carry one input direction per pass: n passes for n inputs, the forward mode. "
            "Multiply from the left, starting from the single output, and every product is a row: one pass for all "
            "inputs. That is the whole idea; matrix multiplication is associative. <bookmark mark='b'/> Node by node "
            "it is the adjoint recursion, one multiply-add per edge. <bookmark mark='c'/> So the gradient costs a "
            "small constant times the function, independent of the number of inputs: Griewank's cheap gradient "
            "principle. Giles and Glasserman brought it to Monte Carlo Greeks in 2006, path by path, and it needs the "
            "pathwise conditions of the last chapter: digitals need smoothing or the likelihood ratio. Pause and "
            "predict: a swap book with two thousand curve points. AAD costs a handful of prices."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def lab(self, g):
        a = g["aad"]
        card = lab_card(r"AAD on an Asian option", [
            "s0, k, t, v, rr = (Tensor(np.array(a, float), requires_grad=True)",
            "                   for a in (S0, K, T, sigma, r))",
            "d = t * (1.0 / n_steps); lx = s0.log(); acc = None",
            "drift = (rr - v * v * 0.5) * d; sdt = d ** 0.5",
            "for i in range(n_steps):",
            "    lx = lx + drift + v * sdt * Tensor(z[i])",
            "    e = lx.exp(); acc = e if acc is None else acc + e",
            "pay = (acc * (1.0 / n_steps) - k).relu()",
            "price = pay.mean() * (rr * t * -1.0).exp()",
            "price.backward()      # one sweep: s0.grad, v.grad, ...",
        ], source="explainer/quant/house/engine.py  aad_greeks", width=7.6).to_corner(UL, buff=0.35)
        names = [("delta", "dV/dS0"), ("vega", "dV/dsigma"), ("rho", "dV/dr"), ("theta_T", "dV/dT"), ("dK", "dV/dK")]
        out = ["            AAD        bump"] + [f"{nm:<10} {a['aad'][k]:>9.4f}  {a['bump'][k]:>9.4f}" for k, nm in names]
        out.append(f"cost: AAD {g['aad_ratio']:.1f} prices, bumping {g['bump_ratio']:.1f}")
        with self.voiceover(
            "The House prices an Asian option with fifty fixings and twenty thousand paths on the same autodiff: ten "
            "lines, and one call to backward. <bookmark mark='a'/> All five sensitivities agree with central bumps, "
            f"and the sweep cost {g['aad_ratio']:.1f} times one price, against {g['bump_ratio']:.1f} for bumping. With "
            "five inputs that is a modest saving. The point is what happens with more."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.5)
        self.clear_scene()

    def scaling(self, s):
        rows = s["rows"]
        x = np.log10([r["inputs"] for r in rows])
        aad = np.array([r["t_aad"] / r["t_price"] for r in rows])
        bump = np.array([r["t_bump"] / r["t_price"] for r in rows])
        prox_a = np.array([(r["fwd_ops"] + r["bwd_ops"]) / r["fwd_ops"] for r in rows])
        prox_b = np.array([2.0 * r["inputs"] for r in rows])
        g = axes([0.2, 2.2], [0, 3], x_length=6.6, y_length=4.2, xlabel=r"inputs differentiated (spots and vols)",
                 ylabel=r"cost in prices (log)", xticks=[np.log10(2), 1, 2], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[0, 1, 2, 3], yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        la = polyline(ax, x, np.clip(np.log10(aad), 0, 3), DELTA)
        lb = polyline(ax, x, np.clip(np.log10(bump), 0, 3), BAD)
        pa = DashedVMobject(polyline(ax, x, np.log10(prox_a), DELTA, dots=False)[0], num_dashes=20)
        pb = DashedVMobject(polyline(ax, x, np.clip(np.log10(prox_b), 0, 3), BAD, dots=False)[0], num_dashes=20)
        leg = legend([(DELTA, r"AAD, wall clock (best of several runs)"), (BAD, r"central bumps, wall clock"),
                      (GREY_B, r"dashed: operation counts (machine-free)")], font_size=16).next_to(g, UP, buff=0.1)
        leg.align_to(g, LEFT)
        big = rows[-1]
        side = VGroup(
            MathTex(rf"{big['inputs']}\ \text{{inputs: AAD}}\ {aad[-1]:.1f}\times,\ \ \text{{bumps}}\ {bump[-1]:.0f}\times",
                    font_size=28, color=GOOD),
            MathTex(rf"\text{{tape: }}{big['nodes']}\ \text{{nodes, backward/forward ops}} = {big['bwd_ops'] / big['fwd_ops']:.2f}",
                    font_size=24, color=GREY_A),
            MathTex(rf"\max|\Delta_{{\text{{AAD}}}} - \Delta_{{\text{{bump}}}}| = {big['max_delta_diff']:.1e}", font_size=24,
                    color=GREY_A),
            wrapped_label(r"memory: the tape stores every intermediate, steps $\times$ paths. Check-pointing stores every "
                          r"$k$-th state and recomputes the rest during the sweep, trading time for memory (Savine 2018, "
                          r"ch.\ 13); desks also differentiate path by path", 4.6, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        src = illustration(r"an Asian basket on $d$ assets, 4{,}000 paths, 12 steps; " + s["machine"].replace("%", r"\%"))
        with self.voiceover(
            "Now grow the problem: an Asian basket on more and more assets, differentiating with respect to every "
            "spot and every volatility. Cost in units of one price, on a log scale. <bookmark mark='a'/> Bumping is a "
            "line: two extra prices per input. Adjoints stay nearly flat, apart from timing noise at the smallest "
            "sizes, where one price takes a millisecond. With "
            f"{big['inputs']} inputs, AAD cost {aad[-1]:.1f} prices on this machine and bumping {bump[-1]:.0f}. "
            "<bookmark mark='b'/> Wall-clock time on a shared machine is noisy, so the dashed lines count operations "
            "instead: the backward sweep does about as much arithmetic as the forward pass, whatever the number of "
            "inputs. <bookmark mark='c'/> The price is memory: the tape remembers every intermediate, so long "
            "simulations store checkpoints and recompute between them."
            " In low dimensions there is a faster road than simulation. Next: finite differences."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lb), Create(la), FadeIn(leg[:2]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(pa), Create(pb), FadeIn(leg[2]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.5)
        self.clear_scene()
