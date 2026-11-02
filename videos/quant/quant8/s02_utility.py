from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import control as C
from videos.quant.quant8.common import BAD, GOOD, KELLY, PART, VALUE, load


class Utility(VoiceoverScene):
    def construct(self):
        u = load("utility_check")
        self.card()
        self.axioms()
        self.curves(u)
        self.slider(u)
        self.pratt(u)
        self.check(u)

    def card(self):
        c = chapter_card(1, r"Utility and risk aversion", r"What is a gamble worth to you?", part=PART)
        with self.voiceover("Chapter one. Utility, and risk aversion."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def axioms(self):
        sp = history_card(1738, r"Daniel Bernoulli, St Petersburg",
                          r"A coin is tossed until it lands heads; the pot doubles each toss. Its expected payout is "
                          r"infinite, yet nobody pays much to play. Bernoulli: value it by the logarithm of wealth, "
                          r"and its value is a few ducats.", width=5.6)
        ax = definition_card(r"von Neumann and Morgenstern (1944)", VGroup(*[
            label(t, font_size=21, color=GREY_A) for t in (
                r"completeness: any two gambles can be ranked",
                r"transitivity: $A \succeq B$ and $B \succeq C$ give $A \succeq C$",
                r"continuity: no gamble is infinitely better or worse",
                r"independence: mixing both with a third keeps the order",
            )]).arrange(DOWN, aligned_edge=LEFT, buff=0.14), kind=r"Axioms", width=6.8, color=VALUE)
        thm = MathTex(r"\Longrightarrow\ \ A \succeq B \iff \mathbb{E}\,u(A) \ge \mathbb{E}\,u(B)", font_size=34,
                      color=VALUE)
        VGroup(sp, ax).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(UP, buff=0.5)
        thm.next_to(VGroup(sp, ax), DOWN, buff=0.5)
        with self.voiceover(
            "In 1738 Daniel Bernoulli looked at a game with an infinite expected payout, a pot that doubles until a coin "
            "lands heads, that nobody would pay much to play. His answer: value money by a utility, the logarithm of "
            "wealth. <bookmark mark='a'/> In 1944 von Neumann and Morgenstern made it a theorem. If your preferences among "
            "gambles are complete, transitive, continuous, and independent, meaning that mixing two gambles with the same "
            "third never reverses their order, <bookmark mark='b'/> then you prefer A to B exactly when A has the larger "
            "expected utility."
        ) as vo:
            self.play(FadeIn(sp, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(ax, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(thm))
        self.wait(0.4)
        self.clear_scene()

    def curves(self, u):
        g = axes([0, 200], [-1.6, 0.8], x_length=6.6, y_length=4.6, xlabel=r"wealth", ylabel=r"utility (log)",
                 xticks=[50, 100, 150, 200], yticks=[], font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = g.ax
        w = np.linspace(20, 200, 200)
        line = curve(ax, w, np.log(w / 100), VALUE, stroke_width=4)
        a, b = (50, np.log(0.5)), (150, np.log(1.5))
        # the gamble as two equal weights hung on the curve
        wa = VGroup(Line(ax.c2p(*a), ax.c2p(a[0], a[1] - 0.35), color=GREY_B, stroke_width=1.5),
                    Square(0.28, fill_color=GOOD, fill_opacity=0.9, stroke_width=0).move_to(ax.c2p(a[0], a[1] - 0.48)))
        wb = VGroup(Line(ax.c2p(*b), ax.c2p(b[0], b[1] - 0.35), color=GREY_B, stroke_width=1.5),
                    Square(0.28, fill_color=GOOD, fill_opacity=0.9, stroke_width=0).move_to(ax.c2p(b[0], b[1] - 0.48)))
        pa, pb = Dot(ax.c2p(*a), color=GOOD), Dot(ax.c2p(*b), color=GOOD)
        chord = Line(ax.c2p(*a), ax.c2p(*b), color=GREY_B, stroke_width=2)
        eu = 0.5 * (a[1] + b[1])
        mid = Dot(ax.c2p(100, eu), color=WHITE)
        ce = u["ce_g1"]
        cedot = Dot(ax.c2p(ce, eu), color=KELLY)
        hline = DashedLine(ax.c2p(ce, eu), ax.c2p(100, eu), color=KELLY, stroke_width=2)
        vline = DashedLine(ax.c2p(ce, eu), ax.c2p(ce, -1.6), color=KELLY, stroke_width=2)
        cel = MathTex(rf"CE = {ce:.1f}", font_size=26, color=KELLY).next_to(cedot, LEFT, buff=0.15).shift(UP * 0.25)
        side = VGroup(
            label(r"a coin flip: 50 or 150, from 100", font_size=24, color=GREY_A),
            MathTex(r"\mathbb{E}[u(W)] = \tfrac12 u(50) + \tfrac12 u(150)", font_size=30),
            MathTex(r"u(CE) = \mathbb{E}[u(W)]", font_size=30, color=KELLY),
            wrapped_label(r"the balance point of the two weights sits on the chord, below the curve: a concave $u$ "
                          r"values the gamble below its average", 4.6, 20, GREY_A),
            wrapped_label(r"the gap $100 - CE$ is the risk premium", 4.6, 22, VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Take a coin flip that leaves you with fifty or a hundred and fifty, from a hundred, and log utility. "
            "<bookmark mark='a'/> Hang the two outcomes on the curve as equal weights. Their balance point is the middle of "
            "the chord, and its height is the expected utility; because the curve bends, the chord lies below it. "
            "<bookmark mark='b'/> Slide left until you meet the curve: that sure wealth is worth as much as the gamble, the "
            f"certainty equivalent, {ce:.1f}. The gap of {100 - ce:.1f} is the risk premium, and the bend is risk aversion."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(wa, shift=DOWN * 0.2), FadeIn(wb, shift=DOWN * 0.2))
            self.play(Create(chord), FadeIn(mid), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(Create(hline), FadeIn(cedot), run_time=1.2)
            self.play(Create(vline), FadeIn(cel), FadeIn(side[2]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def slider(self, u):
        gam, ces = np.asarray(u["gammas"]), np.asarray(u["ce"])
        g = axes([30, 200], [-0.6, 1.4], x_length=7.2, y_length=4.8, xlabel=r"wealth",
                 ylabel=r"utility, scaled so $u(50) = 0$ and $u(150) = 1$", xticks=[50, 100, 150, 200], yticks=[0, 1],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lg = ValueTracker(np.log(0.5))
        w = np.linspace(30, 200, 300)

        def scaled(gm):
            f = lambda x: C.crra(x, gm)  # noqa: E731
            y = (f(w) - f(50.0)) / (f(150.0) - f(50.0))
            return np.where(y < -0.6, np.nan, np.minimum(y, 1.4))

        crv = always_redraw(lambda: curve(ax, w, scaled(float(np.exp(lg.get_value()))), VALUE, stroke_width=4))
        chord = Line(ax.c2p(50, 0), ax.c2p(150, 1), color=GREY_B, stroke_width=2)
        ends = VGroup(Dot(ax.c2p(50, 0), color=GOOD), Dot(ax.c2p(150, 1), color=GOOD))
        mid = Dot(ax.c2p(100, 0.5), color=WHITE)

        def ce_now():
            return float(np.interp(lg.get_value(), np.log(gam), ces))

        hl = always_redraw(lambda: DashedLine(ax.c2p(ce_now(), 0.5), ax.c2p(100, 0.5), color=KELLY, stroke_width=2))
        cd = always_redraw(lambda: Dot(ax.c2p(ce_now(), 0.5), color=KELLY, radius=0.09))
        vl = always_redraw(lambda: DashedLine(ax.c2p(ce_now(), 0.5), ax.c2p(ce_now(), -0.6), color=KELLY,
                                              stroke_width=2))
        read = VGroup(*[VGroup(MathTex(t, font_size=36, color=c_), DecimalNumber(0, num_decimal_places=1, font_size=36,
                                                                                    color=c_)).arrange(RIGHT, buff=0.15)
                        for t, c_ in ((r"\gamma =", VALUE), (r"CE =", KELLY), (r"\text{premium} =", GREY_A))])
        read.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=1.0).shift(UP * 1.2)
        read[0][1].set_value(0.5)
        read[1][1].set_value(ce_now())
        read[2][1].set_value(100 - ce_now())
        read[0][1].add_updater(lambda m: m.set_value(float(np.exp(lg.get_value()))))
        read[1][1].add_updater(lambda m: m.set_value(ce_now()))
        read[2][1].add_updater(lambda m: m.set_value(100 - ce_now()))
        rows = [cmath(r"u(W)", r"=", r"\frac{W^{1-\gamma}}{1-\gamma}", font_size=34, colors={r"u(W)": VALUE})]
        eq = rows[0].to_corner(DR, buff=0.6).shift(UP * 0.6)
        why_ = wrapped_label(r"constant relative risk aversion: the same gambles, in percent, at any wealth; "
                             r"$\gamma = 1$ is the log", 4.0, 19, GREY_B).next_to(eq, DOWN, buff=0.2).to_edge(RIGHT, buff=0.3)
        i3 = int(np.argmin(abs(gam - 3)))
        with self.voiceover(
            "Economists usually give the curve one dial: power utility, wealth to the power one minus gamma, over one minus "
            "gamma, with the logarithm at gamma one. Someone with this utility takes the same gambles, in percentages, rich or "
            "poor. Scale the curve so the two outcomes stay at zero and one: then the chord never moves, and only the bend "
            "changes. <bookmark mark='a'/> Turn the dial. As gamma rises the curve bends harder, and the certainty equivalent "
            f"slides left: {ces[i3]:.1f} at gamma three, and at thirty, {ces[-1]:.1f}, barely above the worst outcome. "
            "<bookmark mark='b'/> Surveys and laboratory choices put most people's gamma between one and ten."
        ) as vo:
            self.play(FadeIn(g), Create(chord), FadeIn(ends), FadeIn(mid), FadeIn(eq), FadeIn(why_))
            self.add(crv, hl, vl, cd, read)
            vo.wait_until("a")
            self.play(lg.animate.set_value(np.log(30)), run_time=max(min(vo.remaining(8.0) - 3, 14), 6),
                      rate_func=smooth)
            vo.wait_until("b")
        for m in (crv, hl, vl, cd, *[r_[1] for r_ in read]):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def pratt(self, u):
        rows = [cmath(r"\mathbb{E}\,u(W + \tilde\varepsilon)", r"=", r"u(W - \pi)", font_size=34),
                cmath(r"\mathbb{E}\,u(W + \tilde\varepsilon)", r"\approx", r"u(W) + \tfrac12\,\sigma^2 u''(W)",
                      font_size=34),
                cmath(r"u(W - \pi)", r"\approx", r"u(W) - \pi\, u'(W)", font_size=34),
                cmath(r"\pi", r"\approx", r"\tfrac12\,\sigma^2\Big(-\frac{u''(W)}{u'(W)}\Big) = \tfrac12\,\sigma^2 A(W)",
                      font_size=34, colors={r"\pi": KELLY}),
                cmath(r"\frac{\pi}{W}", r"\approx", r"\tfrac12\,\gamma\,\Big(\frac{\sigma}{W}\Big)^2,\qquad "
                      r"\gamma = -\frac{W u''(W)}{u'(W)}", font_size=34, colors={r"\frac{\pi}{W}": KELLY})]
        whys = [why(r"definition: the premium $\pi$ makes a fair gamble $\tilde\varepsilon$ ($\mathbb{E}\tilde\varepsilon"
                    r" = 0$, variance $\sigma^2$) as bad as a sure loss of $\pi$"),
                why(r"Taylor to second order; the first-order term vanishes because $\mathbb{E}\tilde\varepsilon = 0$"),
                why(r"Taylor to first order on the other side: $\pi$ is small"),
                why(r"equate the two: the premium is half the variance times absolute risk aversion $A$ (Pratt 1964; "
                    r"Arrow 1965)"),
                why(r"divide by $W$: relative risk aversion $\gamma$; for CRRA it is the constant $\gamma$")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.9, buff=0.6, edge=6.9)
        with self.voiceover(
            "What is the bend worth in money? Pratt in 1964 and Arrow in 1965: define the premium pi so that a fair gamble "
            "is as bad as losing pi for sure. <bookmark mark='a'/> Expand the left side to second order; the mean is zero, "
            "so half the variance times u double prime remains. <bookmark mark='b'/> Expand the right side to first order. "
            "<bookmark mark='c'/> Equate: the premium is half the variance times the absolute risk aversion. "
            "<bookmark mark='d'/> Divide by wealth, and relative risk aversion appears: for power utility, exactly gamma."
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

    def check(self, u):
        rows = u["premia"]
        head = VGroup(*[label(t, font_size=21, color=GREY_B) for t in (r"$\gamma$", r"gamble", r"exact premium",
                                                                       r"$\tfrac12\gamma\sigma^2/W$")])
        cells = [head]
        for r_ in rows:
            cells.append(VGroup(MathTex(f"{r_['gamma']:g}", font_size=28, color=VALUE),
                                MathTex(rf"100 \pm {r_['stake']:.0f}", font_size=28),
                                MathTex(f"{r_['exact']:.2f}", font_size=28, color=KELLY),
                                MathTex(f"{r_['approx']:.2f}", font_size=28, color=GREY_A)))
        tab = VGroup(*[m for r_ in cells for m in r_]).arrange_in_grid(rows=len(cells), cols=4, buff=(0.7, 0.2),
                                                                    col_alignments="cccc")
        tab.to_edge(UP, buff=0.7)
        g3 = [r_ for r_ in rows if r_["gamma"] == 3.0 and r_["stake"] == 50.0][0]
        g1 = [r_ for r_ in rows if r_["gamma"] == 1.0 and r_["stake"] == 50.0][0]
        q = pause_card(r"$\gamma = 3$, wealth 100, the 50-or-150 flip: would you pay more or less than 20 to avoid it?",
                       width=8.4, font_size=24).next_to(tab, DOWN, buff=0.5)
        ans = label(rf"more: the certainty equivalent is {u['ce_g3']:.1f}, so the premium is {100 - u['ce_g3']:.1f}",
                    font_size=24, color=KELLY).next_to(q, DOWN, buff=0.3)
        rabin = wrapped_label(r"Rabin (2000): if expected utility of wealth explains turning down a small fair-ish bet "
                              r"at every wealth, it implies absurd refusals of large ones. Small-stakes aversion needs "
                              r"another explanation: chapter 13.", 12.0, 20, GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Check it. For a ten-dollar gamble the approximation is nearly exact; for fifty dollars it drifts: "
            f"{g1['exact']:.1f} against {g1['approx']:.1f} at gamma one. <bookmark mark='a'/> Pause and predict: with gamma "
            "three, would you pay more or less than twenty to avoid the fifty-or-a-hundred-and-fifty flip? "
            f"<bookmark mark='b'/> More: {100 - u['ce_g3']:.1f}. <bookmark mark='c'/> One warning, from Matthew Rabin in "
            "2000: utility of wealth cannot explain refusing small favourable bets without absurd refusals of large ones. "
            "Chapter thirteen takes that up."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.25, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ans))
            vo.wait_until("c")
            self.play(FadeIn(rabin))
        self.wait(0.4)
        self.clear_scene()
