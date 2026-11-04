from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, SHRINK_C, TRUE_C, fit_right, load


def _ym(d: int) -> str:
    import calendar
    return f"{calendar.month_name[d % 100]} {d // 100}"


class Views(VoiceoverScene):
    def construct(self):
        v = load("views")
        self.card()
        self.math()
        self.reweight(v)
        self.consequences(v)
        self.question()

    def card(self):
        c = chapter_card(10, r"Entropy pooling", r"How do you impose a view on a whole distribution, not just on a mean?",
                         part=PART)
        with self.voiceover("Chapter ten. Black-Litterman blends views into expected returns, under normality. Attilio "
                            "Meucci generalised it in 2008: impose any view on a whole distribution of scenarios, and "
                            "change it as little as possible."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def math(self):
        rows = [cmath(r"\min_q", r"\ ", r"\textstyle\sum_j q_j\log\frac{q_j}{p_j}\quad \text{s.t.}\ Aq = b,\ 1^\top q = 1",
                      font_size=32, colors={r"\min_q": SHRINK_C}),
                cmath(r"q_j", r"\propto", r"p_j\,e^{\lambda^\top a_j}", font_size=36, colors={r"q_j": SHRINK_C}),
                cmath(r"\lambda", r"=", r"\arg\min_\lambda\ \log\textstyle\sum_j p_j e^{\lambda^\top a_j} - \lambda^\top b",
                      font_size=32, colors={r"\lambda": HURDLE})]
        whys = [why(r"keep the scenarios, change their probabilities: the closest distribution to the prior in relative "
                    r"entropy that satisfies the views (each a linear statement about $q$)"),
                why(r"the solution tilts the prior exponentially, one multiplier per view"),
                why(r"the multipliers solve a smooth convex problem with as many unknowns as views, not scenarios")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The idea. <bookmark mark='a'/> Keep the historical scenarios, and change only their probabilities: find the "
            "distribution closest to the prior in relative entropy that satisfies the views. <bookmark mark='b'/> The "
            "answer tilts each scenario's probability exponentially, by how much that scenario agrees with the views. "
            "<bookmark mark='c'/> The tilt has one multiplier per view, found by a small convex problem, however many "
            "scenarios there are."
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

    def reweight(self, v):
        q = np.asarray(v["q"], float)
        d = np.asarray(v["dates"], float)
        x = d // 100 + ((d % 100) - 0.5) / 12
        J = v["J"]
        top = float(np.ceil(q.max() * J))
        g = axes([x[0], x[-1]], [0, top], x_length=9.6, y_length=4.0, xlabel=r"",
                 ylabel=r"posterior probability $\times J$ (1 = the prior)", xticks=[1970, 1990, 2010, 2020],
                 yticks=[0, 1, top], xfmt=lambda v_: f"{v_:.0f}", font_size=15).move_to(LEFT * 0.4 + DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, qq * J), color=BAD if qq * J > 1 else GREY_C, stroke_width=1.6)
                        for a, qq in zip(x, q)])
        one = DashedLine(ax.c2p(x[0], 1), ax.c2p(x[-1], 1), color=GREY_B, stroke_width=1.2)
        tops = [_ym(int(t)) for t in v["top_dates"][:3]]
        view = 100 * v["view"][1]
        eq = label(rf"view: banks' expected excess return is ${view:.0f}\%$ a month", font_size=22, color=HURDLE
                   ).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"A stress view on the industries' {J} monthly scenarios since 1970: banks will lose "
            f"{abs(view):.0f} percent a month on average. <bookmark mark='a'/> Each line is one month's new probability, "
            "relative to the prior's one in "
            f"{J}. The months that agree with the view are weighted up: the most, {tops[0]}, {tops[1]} and {tops[2]}. "
            "Entropy pooling chose crises on its own, because those are the months in which the view was true. "
            f"<bookmark mark='b'/> Its effective number of scenarios is {v['ens']:.0f}: the view moved the distribution "
            "with a light touch."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.002, run_time=3))
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def consequences(self, v):
        cols = v["columns"]
        pr, po = np.asarray(v["prior"]), np.asarray(v["post"])
        dlt = po - pr
        order = np.argsort(dlt)
        i_b = cols.index("Banks")
        worst = [k for k in order if k != i_b][:2]
        best = int(order[-1])
        cards = VGroup(
            desk_question(r"the view spreads", rf"banks fall to {100 * po[i_b]:.0f}\% a year, as asked; and through the "
                          rf"months that made it true, {cols[worst[0]]} falls by {100 * abs(dlt[worst[0]]):.0f} points and "
                          rf"{cols[worst[1]]} by {100 * abs(dlt[worst[1]]):.0f}, while {cols[best]} moves least",
                          width=12.4, font_size=19),
            desk_question(r"the whole distribution moves", r"volatilities, correlations and tails are reweighted together "
                          r"with the means: the crisis months bring their own correlations", width=12.4, font_size=19),
            desk_question(r"no normality needed", r"any view that is linear in the probabilities: means, volatilities, "
                          r"correlations, quantiles, even a ranking", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the view did. <bookmark mark='a'/> Banks fall to the stated level; and because the view was answered "
            f"with real crisis months, other industries fall with them: {cols[worst[0]]} and {cols[worst[1]]} the most. "
            "<bookmark mark='b'/> Volatilities, correlations and tails move together with the means. "
            "<bookmark mark='c'/> And nothing here needs normality: any view that is linear in the probabilities can be "
            "imposed, including views on volatility, correlation or a ranking."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a view that the prior already satisfies is imposed. What are the posterior probabilities?")
        with self.voiceover(
            "Pause and predict. You impose a view that the prior already satisfies. What are the posterior "
            "probabilities?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
