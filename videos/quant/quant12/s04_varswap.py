from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


class VarSwap(VoiceoverScene):
    def construct(self):
        w = load("varswap")
        t = load("trunc")
        self.card()
        self.payoffs()
        self.replicate()
        self.strip(w, t)
        self.jumps(t)

    def card(self):
        c = chapter_card(9, r"Variance swaps: buying volatility itself", r"How do you buy volatility itself?", part=PART)
        with self.voiceover("Chapter nine. Variance swaps: buying volatility itself."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def payoffs(self):
        g = axes([0.4, 1.8], [-0.1, 1.2], x_length=7.2, y_length=4.4, xlabel=r"$S_T / F$", ylabel=r"payoff",
                 xticks=[0.5, 1.0, 1.5], yticks=[0, 0.5, 1.0], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        x = np.linspace(0.4, 1.8, 281)
        target = 2 * (x - 1 - np.log(x))  # the log contract plus a forward: -2 ln x + 2(x - 1)
        tl = curve(ax, x, np.clip(target, -0.1, 1.2), OPT, stroke_width=5)
        Ks = np.concatenate([np.arange(0.95, 0.39, -0.05), np.arange(1.05, 1.81, 0.05)])
        order = np.argsort(np.abs(np.log(Ks)))
        Ks = Ks[order]
        n = ValueTracker(0)

        def strip_sum(m):
            tot = np.zeros_like(x)
            for K in Ks[:m]:
                q = 2 * 0.05 / K ** 2
                tot += q * (np.maximum(K - x, 0) if K < 1 else np.maximum(x - K, 0))
            return tot
        approx = always_redraw(lambda: curve(ax, x, np.clip(strip_sum(int(n.get_value())), -0.1, 1.2), IV, stroke_width=3))
        resid = always_redraw(lambda: band(ax, x, np.clip(strip_sum(int(n.get_value())), -0.1, 1.2),
                                           np.clip(target, -0.1, 1.2), BAD, 0.25))
        cnt = always_redraw(lambda: MathTex(rf"\text{{options in the strip: }} {int(n.get_value())}", font_size=28,
                                            color=IV).next_to(g, UP, buff=0.1))
        side = VGroup(
            label(r"target: $2\big(S/F - 1 - \ln S/F\big)$", font_size=22, color=OPT),
            wrapped_label(r"each option bought in amount $2\,\Delta K / K^2$: puts below the forward, calls above", 4.4,
                          20, IV),
            wrapped_label(r"red: what the strip still misses; the far wings, where few strikes are listed", 4.4, 20, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"strikes every 5\% of the forward")
        with self.voiceover(
            "A variance swap pays, at expiry, the variance the price actually realized, minus a fixed strike agreed "
            "today. To hedge it you need the purple curve: a logarithm, measured from the forward. No exchange lists "
            "that payoff. <bookmark mark='a'/> But you can build it. Take the option struck nearest the forward, "
            "bought in an amount two times the strike spacing over the strike squared. Then the next one out, a put "
            "below, a call above, each with the same weighting. <bookmark mark='b'/> The sum of hockey sticks bends "
            "toward the log curve, and the red residual shrinks to the far wings, where the strikes run out."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(tl), FadeIn(side[0]))
            self.add(resid, approx, cnt)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            self.play(n.animate.set_value(6), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(n.animate.set_value(len(Ks)), run_time=4, rate_func=linear)
            self.play(FadeIn(side[2]))
        for m_ in (approx, resid, cnt):
            m_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def replicate(self):
        rows = [cmath(r"\int_0^T \sigma_t^2\,dt", r"=", r"2\int_0^T \frac{dS_t}{S_t} - 2\ln\frac{S_T}{S_0}", font_size=34,
                      colors={r"\int_0^T \sigma_t^2\,dt": RV}),
                cmath(r"f(S)", r"=", r"f(F) + f'(F)(S - F) + \int_0^F f''(K)(K - S)^+dK + \int_F^\infty f''(K)(S - K)^+dK",
                      font_size=30, colors={r"f(S)": OPT}),
                cmath(r"K_{\text{var}}", r"=", r"\frac{2}{T}\int_0^\infty \frac{\text{OTM}(K)}{K^2}\,dK", font_size=38,
                      colors={r"K_{\text{var}}": IV}),
                cmath(r"\mathbb{E}^Q\!\int_0^T \Big(\frac{dS}{S}\Big)^2", r"=", r"K_{\text{var}}\,T\quad \text{for any continuous }"
                      r"S", font_size=32),
                cmath(r"2(e^J - 1 - J) - J^2", r"=", r"\tfrac13 J^3 + O(J^4)", font_size=36,
                      colors={r"2(e^J - 1 - J) - J^2": BAD})]
        whys = [why(r"It\^o (Part 5): $d\ln S = dS/S - \tfrac12\sigma^2 dt$; realized variance is a delta-hedging gain "
                    r"minus a log contract"),
                why(r"Taylor's theorem with integral remainder about $F$ (Carr and Madan 1998): any payoff is a bond, a "
                    r"forward and a strip of options"),
                why(r"take $f = -\ln$, so $f'' = 1/K^2$, and Q-expectations: the hedge is free (Neuberger 1994; Demeterfi, "
                    r"Derman, Kamal and Zou 1999)"),
                why(r"model-free implied variance (Britten-Jones and Neuberger 2000): no volatility model was assumed"),
                why(r"with a jump $J$ the log contract pays $2(e^J - 1 - J)$, realized variance $J^2$: down-jumps leave the "
                    r"replication short by about $|J|^3/3$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.72, edge=6.9)
        with self.voiceover(
            "Why the log? Itô's formula. The log of the price drifts down by half the variance, so realized variance "
            "is twice the gains of holding one over S of the asset, minus twice the log return. The first term is a "
            "trading strategy; the second is the log contract. <bookmark mark='a'/> Peter Carr and Dilip Madan's "
            "identity writes any smooth payoff as a bond, a forward, and a strip of options weighted by its second "
            "derivative. <bookmark mark='b'/> For the log, the second derivative is one over K squared, so the fair "
            "variance strike is two over T times the integral of out-of-the-money option prices over K squared. "
            "Anthony Neuberger proposed the log contract in 1994; Goldman's Demeterfi, Derman, Kamal and Zou wrote the "
            "desk's version in 1999. <bookmark mark='c'/> Mark Britten-Jones and Neuberger showed it needs no model at "
            "all, as long as the price moves continuously. <bookmark mark='d'/> And if it jumps, the identity breaks by "
            "a cubic term: a down-jump leaves the replication short."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def strip(self, w, t):
        K, otm = np.asarray(w["K"]), np.asarray(w["otm"])
        F = w["F"]
        m = (K > 0.4 * F) & (K < 1.8 * F)
        contrib = otm / K ** 2
        contrib = contrib / contrib[m].max()
        g = axes([0.4 * F, 1.8 * F], [0, 1.05], x_length=7.0, y_length=3.8, xlabel=r"strike (\$)",
                 ylabel=r"each option's share of the variance strike", xticks=[50000, 100000, 150000],
                 xfmt=lambda u: f"{u / 1000:.0f}k", yticks=[0, 0.5, 1], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        Km, cm = K[m][::10], contrib[m][::10]
        rows = np.asarray(t["rows"])
        xs, vs = rows[:, 0], rows[:, 1]
        tr = ValueTracker(0.05)

        def bars():
            x = tr.get_value()
            keep = np.abs(np.log(Km / F)) <= x
            return VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, b), color=(IV if a > F else BAD) if k_ else GREY_D,
                                 stroke_width=3) for a, b, k_ in zip(Km, cm, keep)])
        bb = always_redraw(bars)
        ro = readout(r"\sqrt{K_{\text{var}}} =", lambda: 100 * float(np.interp(tr.get_value(), xs, vs)), digits=1,
                     font_size=32, color=IV, unit=r"\%")
        ro2 = readout(r"\text{strikes within } \pm", lambda: 100 * tr.get_value(), digits=0, font_size=28, color=GREY_A,
                      unit=r"\%\ \text{(in log)}")
        side = VGroup(ro2, ro,
                      MathTex(rf"\text{{full strip: }} {100 * w['kvar']:.1f}\%\quad \text{{ATM: }} {100 * w['atm']:.1f}\%",
                              font_size=28, color=OPT),
                      wrapped_label(rf"{100 * t['share_beyond_20']:.0f}\% of the variance lives beyond $\pm 20\%$ of the "
                                    r"forward", 4.4, 20, BAD),
                      wrapped_label(r"pause and predict: why is the variance strike above at-the-money volatility?", 4.4,
                                    19, QC.HOUSE)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"30-day strip from the SSVI fit to the Surface")
        x20 = 100 * float(np.interp(0.2, xs, vs))
        kv, atm, sh = 100 * w["kvar"], 100 * w["atm"], 100 * t["share_beyond_20"]
        with self.voiceover(
            "Now the real strip: thirty-day Bitcoin options on the Surface, each bar its share of the variance strike. "
            "The puts, in red, carry the most weight: one over K squared is largest at low strikes, and the downside "
            "is where the smile is dearest. <bookmark mark='a'/> Keep only the strikes near the forward and widen the "
            f"window. Within twenty percent, the strike reads {x20:.1f} percent; the whole strip, {kv:.1f}. "
            f"{sh:.0f} percent of the variance sits in options more than twenty percent away, which is why an index "
            "that stops where the quotes stop reads low. <bookmark mark='b'/> Pause and predict: why is the variance "
            f"strike, {kv:.1f}, above at-the-money volatility, {atm:.1f}? Because the strip owns the whole smile, and the "
            "wings are dearer than the middle."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            self.add(bb)
            vo.wait_until("a")
            self.play(tr.animate.set_value(0.2), run_time=2.5)
            self.play(tr.animate.set_value(1.2), run_time=3.5)
            bb.clear_updaters()
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        for x in (ro, ro2):
            x.num.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def jumps(self, t):
        J = np.asarray(t["J"])
        gap = np.asarray(t["jump_gap"])
        g = axes([-0.4, 0.4], [0, 0.18], x_length=6.6, y_length=4.0, xlabel=r"a single jump $J$ in $\ln S$",
                 ylabel=r"variance paid", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0, 0.08, 0.16], font_size=16
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        rv = curve(g.ax, J, J ** 2, RV, stroke_width=3)
        lc = curve(g.ax, J, np.clip(2 * (np.exp(J) - 1 - J), 0, 0.18), OPT, stroke_width=3)
        sl = band(g.ax, J, np.minimum(J ** 2, 2 * (np.exp(J) - 1 - J)), np.maximum(J ** 2, np.clip(2 * (np.exp(J) - 1 - J), 0, 0.18)),
                  BAD, 0.35)
        leg = legend([(RV, r"realized variance: $J^2$"), (OPT, r"the log contract: $2(e^J - 1 - J)$")], font_size=17
                     ).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        j20 = float(np.interp(-0.2, J, gap))
        side = VGroup(
            MathTex(rf"J = -20\%:\ \ \text{{gap}} = {j20:.4f}", font_size=30, color=BAD),
            wrapped_label(rf"{100 * abs(j20) / 0.04:.0f}\% of that jump's variance is not paid by the hedge: the variance "
                          r"seller who hedges is short the crash", 4.4, 20, GREY_A),
            wrapped_label(r"real contracts cap the payout (often at 2.5 times the strike in volatility) for this reason",
                          4.4, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"one jump, no diffusion")
        pct = 100 * abs(j20) / 0.04
        with self.voiceover(
            "Jumps are where the replication leaks. Suppose the price jumps once, by J in logs. A variance swap pays J "
            "squared, the teal curve. The hedged strip pays two times e to the J minus one minus J, the purple one. "
            "<bookmark mark='a'/> For a rise they nearly agree. For a fall they part: a fall of twenty percent in log terms leaves the "
            f"hedge short by about {pct:.0f} percent of that jump's variance. Whoever sold variance and hedged with "
            "options is short the crash; and that is one reason variance swaps on single stocks carry caps."
            " Next: that replication, run on real Bitcoin."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(rv), Create(lc), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(sl), FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
