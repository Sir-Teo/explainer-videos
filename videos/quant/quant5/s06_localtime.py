from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause

K = 100.0


class LocalTime(VoiceoverScene):
    def construct(self):
        s = load("stoploss")
        tn = load("tanaka")
        self.card()
        self.kink(tn)
        self.sandpile(tn)
        self.tanaka()
        self.scatter(s)

    def card(self):
        c = chapter_card(11, r"Local time and Tanaka: the paradox resolved", r"Where did the money go?",
                         part=PART)
        with self.voiceover("Chapter eleven. Local time, Tanaka's formula, and the paradox resolved."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kink(self, tn):
        g = axes([-1, 1], [0, 1.05], x_length=5.4, y_length=3.0, xlabel=r"$x$", xticks=[-1, 0, 1], yticks=[0, 1],
                 font_size=16)
        g2 = axes([-1, 1], [0, 12], x_length=5.4, y_length=2.2, xlabel=r"$x$", ylabel=r"$f_\varepsilon''$",
                  xticks=[-1, 0, 1], yticks=[0, 10], font_size=16)
        VGroup(g, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        ax, a2 = g.ax, g2.ax
        absx = curve(ax, np.array([-1, 0, 1]), np.array([1, 0, 1]), GREY_B, stroke_width=2)
        ek = ValueTracker(0.5)
        xs = np.linspace(-1, 1, 201)

        def fe():
            e = ek.get_value()
            y = np.where(np.abs(xs) >= e, np.abs(xs), e / 2 + xs ** 2 / (2 * e))
            return curve(ax, xs, y, ITO, stroke_width=3)

        def box():
            e = ek.get_value()
            hgt = min(1 / e, 12)
            return Rectangle(width=a2.c2p(2 * e, 0)[0] - a2.c2p(0, 0)[0], height=a2.c2p(0, hgt)[1] - a2.c2p(0, 0)[1],
                             stroke_width=0, fill_color=JUMP, fill_opacity=0.7).move_to(a2.c2p(0, 0), aligned_edge=DOWN)
        lf, lb = always_redraw(fe), always_redraw(box)
        el = always_redraw(lambda: MathTex(rf"\varepsilon = {ek.get_value():.2f}", font_size=28, color=ITO)
                           .next_to(g, UP, buff=0.1).align_to(g, LEFT))
        rows = [cmath(r"f_\varepsilon(x)", r"=", r"|x| \text{ for } |x| \ge \varepsilon,\quad \tfrac{\varepsilon}{2} + "
                      r"\tfrac{x^2}{2\varepsilon} \text{ inside}", font_size=28),
                cmath(r"f_\varepsilon(W_t)", r"=", r"f_\varepsilon(0) + \int_0^t f_\varepsilon'(W)\,dW + \frac{1}{2\varepsilon}"
                      r"\int_0^t \mathbf{1}_{\{|W_s| < \varepsilon\}}\,ds", font_size=28),
                cmath(r"|W_t|", r"=", r"\int_0^t \operatorname{sgn}(W_s)\,dW_s + L^0_t", font_size=32,
                      colors={r"L^0_t": JUMP}),
                cmath(r"\int_0^t g(W_s)\,ds", r"=", r"\int_{\mathbb{R}} g(a)\,L^a_t\,da", font_size=30)]
        whys = [why(r"round the kink off with a parabola; $f_\varepsilon'' = 1/\varepsilon$ on the band", 18),
                why(r"It\^o's lemma ($C^1$ and piecewise $C^2$ is enough)", 18),
                why(r"$\varepsilon \to 0$: $f_\varepsilon' \to \operatorname{sgn}$; the last term converges: "
                    r"Tanaka (1963)", 18),
                why(r"the same limit at every level $a$: local time is an occupation density", 18)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=2.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "Itô's lemma needs two derivatives, and the absolute value has a kink at zero. Hiroshi Tanaka's idea, in "
            "1963, was to round it off. <bookmark mark='a'/> Inside a band of half-width epsilon, replace the kink by "
            "a parabola. Its second derivative is one over epsilon on the band: the red box, whose area is always "
            "two. <bookmark mark='b'/> Apply the lemma: the second-order term is one over two epsilon times the time "
            "spent in the band. <bookmark mark='c'/> Shrink epsilon. The band thins, the box grows taller, and the "
            "term converges: the local time at zero. The absolute value of W is the integral of its sign, plus local "
            "time. <bookmark mark='d'/> The same limit at every level gives an occupation density."
        ) as vo:
            self.add(lf, lb, el)
            self.play(FadeIn(g), FadeIn(g2), Create(absx))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(ek.animate.set_value(0.09), run_time=3)
            step(2)
            vo.wait_until("d")
            step(3)
        for m in (lf, lb, el):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def sandpile(self, tn):
        w = np.asarray(tn["path"])
        Lr = np.asarray(tn["L_run"])
        t = np.linspace(0, 1, len(w))
        lo, hi = w.min() - 0.1, w.max() + 0.1
        g = axes([0, 1], [lo, hi], x_length=6.4, y_length=4.2, xlabel=r"time", ylabel=r"$W_t$", xticks=[0, 1],
                 yticks=[0], font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0)
        path = tracing(ax, t, w, tk, BM, stroke_width=2)
        x0 = ax.get_right()[0] + 0.15
        bins = np.linspace(lo, hi, 41)
        bw = bins[1] - bins[0]

        def pile():
            n = int(np.clip(tk.get_value(), 1, len(w) - 1))
            h, _ = np.histogram(w[:n], bins)
            dens = h / (len(w) - 1) / bw
            return VGroup(*[Rectangle(width=max(0.9 * d, 0.001), height=ax.c2p(0, bw)[1] - ax.c2p(0, 0)[1] - 0.004,
                                      stroke_width=0, fill_color=STRAT, fill_opacity=0.75)
                            .move_to([x0 + 0.45 * d, ax.c2p(0, b0 + bw / 2)[1], 0]) for b0, d in zip(bins[:-1], dens)
                            if d > 0])
        sp = always_redraw(pile)
        zl = DashedLine(ax.c2p(0, 0), [x0 + 2.2, ax.c2p(0, 0)[1], 0], color=JUMP, stroke_width=2)
        lt = always_redraw(lambda: MathTex(rf"L^0_t \approx {Lr[int(np.clip(tk.get_value(), 0, len(Lr) - 1))]:.3f}",
                                           font_size=30, color=JUMP).next_to(zl, UP, buff=0.12).align_to(zl, RIGHT))
        eps = VGroup(*[MathTex(rf"\varepsilon = {r['eps']}:\ \ {r['L']:.3f}", font_size=22, color=GREY_A)
                       for r in tn["eps_rows"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        eps.add(MathTex(rf"\text{{Tanaka: }} {tn['tan_one']:.3f}", font_size=24, color=JUMP))
        el = label(r"time-in-band, one path of 200{,}000 steps:", font_size=18, color=GREY_B)
        # the title is the widest line: stack it with the rows and place the block as one, inside the frame
        VGroup(el, eps.arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(
            UR, buff=0.35)
        pc, ans = pause(r"The expected local time at 0 of Brownian motion by $t = 1$?",
                        rf"$\mathbb{{E}}|W_1| = \sqrt{{2/\pi}} = {tn['theory']:.3f}$ (Tanaka, in expectation). Measured: "
                        rf"{tn['mean_occ']:.3f} by occupation, {tn['mean_tan']:.3f} by Tanaka.", width=4.8, font_size=19)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Watch it on one path. As it runs, the purple sandpile records the time spent at each level, growing "
            "sideways; local time at zero is the pile's height at the dashed line. <bookmark mark='a'/> It grows only "
            "while the path is near zero. <bookmark mark='b'/> On a fine path, the time-in-band estimates settle "
            f"toward Tanaka's value, {tn['tan_one']:.3f}, as epsilon shrinks. <bookmark mark='c'/> A pause: what is "
            "the expected local time at zero by time one? <bookmark mark='d'/> Take expectations in Tanaka's formula: "
            f"the expected absolute value of W, about {tn['theory']:.2f}; twenty thousand paths agree. And Lévy showed "
            "that local time has the law of the running maximum."
        ) as vo:
            self.add(path, sp, lt)
            self.play(FadeIn(g), Create(zl))
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(w) - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(el), LaggedStart(*[FadeIn(r) for r in eps], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        for m in (path, sp, lt):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def tanaka(self):
        rows = [cmath(r"(S_T - K)^+", r"=", r"(S_0 - K)^+", r"+", r"\int_0^T \mathbf{1}_{\{S_t > K\}}\,dS_t", r"+",
                      r"\tfrac12 L_T^K", font_size=40,
                      colors={r"\int_0^T \mathbf{1}_{\{S_t > K\}}\,dS_t": DRIFT, r"\tfrac12 L_T^K": JUMP}),
                cmath(r"L_T^K", r"=", r"\lim_{\varepsilon \to 0} \frac{1}{2\varepsilon} \int_0^T \mathbf{1}_{\{|S_t - K| < \varepsilon\}}"
                      r"\,d\langle S\rangle_t", font_size=40, colors={r"L_T^K": JUMP}),
                cmath(r"\mathbb{E}_Q\big[\tfrac12 L_T^K\big]", r"=", r"C_0 - (S_0 - K)^+", font_size=40,
                      colors={r"\mathbb{E}_Q\big[\tfrac12 L_T^K\big]": JUMP})]
        whys = [why(r"Tanaka (1963): It\^o's lemma for the kink $x \mapsto (x - K)^+$; the stop-loss hedge earns the green "
                    r"term"),
                why(r"local time: how long the path lingered at $K$, measured in quadratic variation"),
                why(r"take expectations: the missing term is worth exactly the option's time value (Carr and Jarrow 1990)")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.0, buff=1.0, edge=6.9)
        with self.voiceover(
            "Back to the opening puzzle. A call's payoff has the same kink, at the strike, and Tanaka's formula, "
            "applied to the price, says what happens there. The payoff equals its starting value, plus the gains from "
            "holding one share whenever the stock is above the strike, which is exactly the stop-loss hedge, plus one "
            "more term. <bookmark mark='a'/> That term is half the local time at the strike: how long the path spent "
            "within a hair of K, measured in quadratic variation, and rescaled by the hair's width. For a smooth path "
            "it would be zero. A Brownian path that touches K touches it infinitely often, and the local time is "
            "positive. <bookmark mark='b'/> Take expectations under the pricing measure. The gains term has mean "
            "zero, so the missing term is worth the call's price minus its intrinsic value: its time value. Peter "
            "Carr and Robert Jarrow published this resolution in 1990. The hedge is free only on paths that never "
            "come near the strike."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def scatter(self, s):
        sc = s["scatter"]
        e, L = np.asarray(sc["err"]), np.asarray(sc["half_L"])
        hi = float(np.percentile(np.concatenate([e, L]), 99))
        g = axes([0, hi], [0, hi], x_length=5.4, y_length=5.0, xlabel=r"$\tfrac12 L_T^K$ on the path",
                 ylabel=r"the stop-loss hedge's shortfall", xticks=[0, 10, 20], yticks=[0, 10, 20], font_size=18)
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.1)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(a, hi), min(b, hi)), radius=0.03, color=JUMP, fill_opacity=0.6) for a, b in zip(L, e)])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(hi, hi), color=GREY_B, stroke_width=2)
        rows = s["rows"]
        tab = VGroup(*[MathTex(rf"{r['n']:,}\text{{ trades: }} {r['mean_err']:.2f} \pm {r['sd_err']:.2f}".replace(",", "{,}"),
                               font_size=26, color=GREY_A) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(
            label(r"average shortfall, by rebalancing frequency:", font_size=22, color=GREY_A), tab,
            MathTex(rf"\text{{the call's time value: }} {s['call']:.2f}", font_size=30, color=WHITE),
            MathTex(rf"\text{{correlation, path by path: }} {sc['corr']:.2f}", font_size=30, color=JUMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Now all four thousand paths: the hedge's shortfall against half the local time at the strike. "
            f"<bookmark mark='a'/> They line up, with a correlation of {sc['corr']:.2f}. Paths that never came near "
            "the strike cost nothing; paths that lingered there cost a lot. <bookmark mark='b'/> On average the "
            f"shortfall is the call's whole time value, about {s['call']:.0f} dollars, at every frequency. Local time "
            "is real money: it is why options near the strike close to expiry are the hardest to hedge, and Dupire's "
            "local volatility, in Part twelve, uses the same term."
            " Local time is what a continuous path costs a hedger. Real prices also jump. Next."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
