from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import predict, ALT, KELLY, OVER, PART, UNDER, VALUE, illustration, load

MU, R, SIG, GAM, FLOOR = 0.08, 0.02, 0.18, 3.0, 0.6


class HJB(VoiceoverScene):
    def construct(self):
        h = load("hjb_fd")
        self.card()
        self.derive()
        self.parabola(h)
        self.verify()
        self.solve(h)

    def card(self):
        c = chapter_card(3, r"The HJB equation and the verification theorem", r"What does Bellman's recursion become "
                         r"in continuous time?", lit=(1969,), part=PART)
        with self.voiceover("Chapter three. The Hamilton-Jacobi-Bellman equation, and the verification theorem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"V(t, x)", r"=", r"\sup_{\pi}\ \mathbb{E}\big[V(t + h, X_{t+h})\big]", font_size=32,
                      colors={r"V(t, x)": VALUE}),
                cmath(r"V(t + h, X_{t+h})", r"=", r"V + \int_t^{t+h}\big(V_s + \mathcal{L}^{\pi} V\big)\,ds + "
                      r"\int_t^{t+h} V_x\,\pi\sigma X\,dW", font_size=30),
                cmath(r"0", r"=", r"\sup_{\pi}\ \mathbb{E}\Big[\tfrac1h\int_t^{t+h}\big(V_s + \mathcal{L}^{\pi} V\big)\,ds"
                      r"\Big]", font_size=30),
                cmath(r"0", r"=", r"V_t + \sup_{\pi}\Big\{\big(r + \pi(\mu - r)\big)\,x V_x + \tfrac12\pi^2\sigma^2 x^2 "
                      r"V_{xx}\Big\}", font_size=30),
                cmath(r"\pi^*", r"=", r"-\frac{(\mu - r)\,V_x}{\sigma^2\,x\,V_{xx}}", font_size=32,
                      colors={r"\pi^*": KELLY}),
                cmath(r"V", r"=", r"f(t)\,\frac{x^{1-\gamma}}{1-\gamma}\ \Rightarrow\ f' + (1-\gamma)\Big(r + "
                      r"\frac{\theta^2}{2\gamma}\Big) f = 0,\ \ \pi^* = \frac{\mu - r}{\gamma\sigma^2}", font_size=30,
                      colors={r"V": VALUE})]
        whys = [why(r"dynamic programming over a short interval $[t, t + h]$", font_size=21),
                why(r"It\^o's formula for $V(s, X_s)$, with $dX = X\big((r + \pi(\mu - r))\,dt + \pi\sigma\,dW\big)$",
                    font_size=21),
                why(r"the $dW$ integral has mean zero; subtract $V(t, x)$ and divide by $h$", font_size=21),
                why(r"let $h \to 0$: the Hamilton--Jacobi--Bellman equation, with $V(T, x) = u(x)$", font_size=21),
                why(r"first-order condition in $\pi$: the vertex of a parabola, a maximum when $V_{xx} < 0$",
                    font_size=21),
                why(r"ansatz: $xV_x = (1-\gamma)V$, $x^2V_{xx} = -\gamma(1-\gamma)V$; $\theta = (\mu - r)/\sigma$, "
                    r"the Sharpe ratio (Merton 1969)", font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.6, buff=0.95, edge=6.9)
        with self.voiceover(
            "Shrink Bellman's period to an instant. Over a short interval of length h, the value now is the best expected value at the end of the interval: the same principle. <bookmark mark='a'/> Expand that future value with Itô's formula from Part five. It is today's value, plus a drift integral, the time derivative plus the generator of wealth under the chosen fraction, plus a stochastic integral against the Brownian motion. <bookmark mark='b'/> The stochastic integral has mean zero. Subtract today's value from both sides and divide by h. <bookmark mark='c'/> Let h go to zero, and the average of the integrand becomes its value now: zero equals the time derivative plus the supremum, over the fraction, of the drift of wealth times V x plus half the variance times V x x. This is the Hamilton-Jacobi-Bellman equation, with utility as its terminal condition. <bookmark mark='d'/> The thing inside the supremum is a parabola in pi. When V is concave its vertex is the maximum, and the first-order condition gives the fraction. <bookmark mark='e'/> Now guess a power of wealth times a function of time. The x derivatives become multiples of V, the supremum becomes a number, and the equation collapses to an ordinary differential equation for f, equal to one at the end. The fraction is Merton's: the excess return over gamma times the variance. This formal derivation assumes smooth value, valid dynamic programming and admissible control processes over the interval. The stochastic integral needs localization and sufficient integrability to have zero expectation."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def parabola(self, h):
        # left: wealth with a moving dot; right: the Hamiltonian per unit of (1 - gamma) V, a parabola in pi
        gw = axes([0.5, 3.0], [0, 1], x_length=5.0, y_length=1.0, xlabel=r"wealth $x$", xticks=[0.6, 1, 2, 3],
                  font_size=17).to_edge(LEFT, buff=0.7).to_edge(UP, buff=1.4)
        gh = axes([0, 1.5], [-0.06, 0.05], x_length=6.2, y_length=4.0, xlabel=r"fraction $\pi$",
                  ylabel=r"$\big[\pi(\mu - r)\,xV_x + \tfrac12\pi^2\sigma^2x^2V_{xx}\big] \,/\, (1-\gamma)V$",
                  xticks=[0, 0.5, 1, 1.5], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[0], font_size=16)
        gh.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        ax = gh.ax
        x = ValueTracker(3.0)
        fl = ValueTracker(0.0)
        pis = np.linspace(0, 1.5, 151)
        F = FLOOR * np.exp(-R * 5.0)  # the floor's value five years before the deadline

        def ham(xv, on):
            k = xv / max(xv - on * F, 1e-6)
            return pis * (MU - R) * k - 0.5 * GAM * SIG ** 2 * pis ** 2 * k ** 2

        def vertex(xv, on):
            return (MU - R) / (GAM * SIG ** 2) * (xv - on * F) / xv

        def par_curve():
            v = ham(x.get_value(), fl.get_value())
            m = (v >= -0.06) & (v <= 0.05)  # only the part inside the axes: no flat line along the bottom
            return curve(ax, pis[m], v[m], VALUE, stroke_width=4)

        par = always_redraw(par_curve)
        top = always_redraw(lambda: DashedLine(ax.c2p(vertex(x.get_value(), fl.get_value()), -0.06),
                                               ax.c2p(vertex(x.get_value(), fl.get_value()), 0.05), color=KELLY,
                                               stroke_width=2.5))
        rv = DecimalNumber(61.7, num_decimal_places=1, unit=r"\%", font_size=34, color=KELLY)
        read = VGroup(MathTex(r"\pi^* =", font_size=34, color=KELLY), rv).arrange(RIGHT, buff=0.15)
        read.next_to(gh, UP, buff=0.15).align_to(gh, RIGHT)
        rv.add_updater(lambda m: m.set_value(100 * vertex(x.get_value(), fl.get_value())))
        dot = always_redraw(lambda: Dot(gw.ax.c2p(x.get_value(), 0.5), radius=0.1, color=UNDER))
        flr = DashedLine(gw.ax.c2p(F, 0), gw.ax.c2p(F, 1), color=OVER, stroke_width=3)
        fll = label(r"floor's present value", font_size=17, color=OVER).next_to(flr, UP, buff=0.08)
        fll.align_to(flr, LEFT).shift(LEFT * 0.05)  # reads rightward from the line, not off the frame
        txt = VGroup(label(r"no floor: the parabola keeps its vertex", font_size=22, color=GREY_A),
                     label(r"a floor: the vertex slides to 0 as wealth nears it", font_size=22, color=OVER)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(gw, DOWN, buff=1.0).align_to(gw, LEFT)
        q = predict(r"Double $\sigma$. What happens to the Merton fraction?", width=5.6, font_size=22).next_to(
            txt, DOWN, buff=0.5).align_to(gw, LEFT)
        with self.voiceover(
            "Here is the maximum as a picture: at every wealth, the bracket, divided by the positive number one minus "
            "gamma times V, is a parabola in the fraction, and the decision is its vertex. <bookmark mark='a'/> Move wealth. "
            f"Without a floor the vertex never moves: {100 * h['pi_merton']:.0f} percent everywhere. <bookmark mark='b'/> "
            "Switch on chapter two's floor: as wealth nears it the parabola narrows and the vertex slides to zero. "
            "<bookmark mark='c'/> Pause and predict: double the volatility, and the fraction? <bookmark mark='d'/> Falls "
            f"fourfold, to about {100 * h['pi_merton'] / 4:.0f} percent."
        ) as vo:
            self.play(FadeIn(gw), FadeIn(gh), FadeIn(dot), FadeIn(txt[0]))
            self.add(par, top, read)
            vo.wait_until("a")
            self.play(x.animate.set_value(0.7), run_time=3)
            self.play(x.animate.set_value(3.0), run_time=2)
            vo.wait_until("b")
            self.play(fl.animate.set_value(1.0), Create(flr), FadeIn(fll), FadeIn(txt[1]), run_time=1.5)
            self.play(x.animate.set_value(F + 0.04), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("d")
        for m in (par, top, rv, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def verify(self):
        card = theorem_card(r"Verification", VGroup(
            wrapped_label(r"If $w \in C^{1,2}$ solves the HJB equation with $w(T, \cdot) = u$, and for every admissible "
                          r"$\pi$ the stochastic integral $M$ below is a true martingale, then $w = V$, and the "
                          r"maximizer $\pi^*$ is optimal.", 11.0, 23, WHITE),
            MathTex(r"u(X^{\pi}_T) = w(t, x) + \int_t^T \big(w_s + \mathcal{L}^{\pi} w\big)\,ds + M_T \ \le\ w(t, x) + M_T",
                    font_size=32),
            wrapped_label(r"It\^o, then the HJB: the drift is at most zero for every $\pi$, and exactly zero for "
                          r"$\pi^*$. Take expectations: $\mathbb{E}\,u(X^\pi_T) \le w(t, x)$, with equality at $\pi^*$.",
                          11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25), who=r"Fleming and Rishel (1975); Pham ch.\ 3; Bj\"ork",
            width=12.2, color=VALUE).move_to(ORIGIN)
        with self.voiceover(
            """We guessed a smooth solution. Verification turns it into a value function under suitable growth and integrability conditions. Apply Itô along any admissible wealth process. <bookmark mark='a'/> HJB makes the drift nonpositive. If localization and uniform integrability justify expectations at the terminal time, expected utility is at most today's candidate value. An admissible, well-posed feedback attaining the supremum has zero drift and reaches that value. Thus it is optimal. <bookmark mark='b'/> Smoothness, the stochastic-integral condition, terminal limits and admissibility all matter; a martingale condition alone is not a general exclusion of doubling strategies. The next chapter handles nonsmooth value functions."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Circumscribe(card.body[1], color=VALUE), run_time=2)
            self.play(Indicate(card.body[2], color=KELLY, scale_factor=1.03))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()

    def solve(self, h):
        y, pi = np.asarray(h["y"]), np.asarray(h["pi"])
        g = axes([-2, 2], [min(0.55, float(pi.min()) - 0.01), max(0.68, float(pi.max()) + 0.01)], x_length=6.0, y_length=2.6, xlabel=r"log wealth",
                 ylabel=r"the solver's fraction at $t = 0$", xticks=[-2, -1, 0, 1, 2], yticks=[0.56, 0.6, 0.64, 0.68],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.7).to_edge(UP, buff=0.8)
        ax = g.ax
        ref = DashedLine(ax.c2p(-2, h["pi_merton"]), ax.c2p(2, h["pi_merton"]), color=KELLY, stroke_width=2)
        ln = curve(ax, y, pi, VALUE, stroke_width=4)
        pc = np.asarray(h["pass_counts"])
        bars = VGroup()
        bg = axes([0.5, len(pc) + 0.5], [0, max(pc) * 1.15], x_length=4.0, y_length=1.6,
                  xlabel=r"policy-iteration passes in a time step", xticks=list(range(1, len(pc))), xfmt=lambda u: f"{int(u)}",
                  yticks=[], font_size=15).next_to(g, DOWN, buff=0.7).align_to(g, LEFT)
        for k, cnt in enumerate(pc):
            if cnt:
                top = bg.ax.c2p(k, cnt)
                bot = bg.ax.c2p(k, 0)
                bars.add(Rectangle(width=0.4, height=top[1] - bot[1], fill_color=ALT, fill_opacity=0.85,
                                   stroke_width=0).move_to((top + bot) / 2))
                bars.add(MathTex(str(int(cnt)), font_size=20, color=GREY_A).next_to(top, UP, buff=0.05))
        conv = h["convergence"]
        tab = VGroup(*[MathTex(rf"{c['n_t']} \times {c['n_y']}:\ \ \text{{value error }} {100 * c['rel_err']:.2f}\%,\ "
                               rf"\ \pi \text{{ error }} {100 * c['pi_err']:.3f}\text{{ pp}}", font_size=24)
                       for c in conv]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side = VGroup(
            wrapped_label(r"implicit finite differences on (time, log wealth); at each step, policy iteration: solve "
                          r"for $V$ given $\pi$, update $\pi$ to the vertex, repeat", 5.2, 19, GREY_A),
            label(r"grid against the closed form $f(t)$:", font_size=21, color=GREY_B), tab,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"the House's \texttt{hjb\_fd\_merton}; $\gamma = 3$, ten years")
        with self.voiceover(
            "The equation can also be solved without guessing. The House's finite-difference solver, "
            f"{h['n_t']} time steps by {h['n_y']} wealth nodes, alternates at each step: solve for the value given the "
            "fraction, move the fraction to each vertex, repeat. <bookmark mark='a'/> Most steps took "
            f"{int(np.argmax(h['pass_counts']))} passes. <bookmark mark='b'/> Its fraction is Merton's to "
            f"{100 * h['pi_err']:.3f} points, its value within {100 * h['rel_err']:.2f} percent of the closed form, "
            "<bookmark mark='c'/> and the error falls as the grid is refined."
            " But value functions are not always smooth. Next: what to do when they have kinks."
        ) as vo:
            self.play(FadeIn(g), Create(ref), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bg), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(ln), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=2.5))
        self.wait(0.4)
        self.clear_scene()
