from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load


class American(VoiceoverScene):
    def construct(self):
        a = load("american")
        self.card()
        self.lsm()
        self.bounds(a)

    def card(self):
        c = chapter_card(4, r"American options by simulation", r"How do you decide when to exercise with only paths?",
                         part=PART)
        with self.voiceover("Chapter four. American options by simulation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lsm(self):
        g = np.random.default_rng(5)
        S = 100 * np.exp(np.cumsum(0.2 * np.sqrt(1 / 25) * g.standard_normal((300, 1)), axis=0)[:, 0][:1])
        xs = 100 * np.exp(0.2 * np.sqrt(0.5) * g.standard_normal(300))
        cont = np.maximum(100 - xs, 0) * 0.55 + 4 + 0.6 * g.standard_normal(300) * 3
        cont = np.maximum(cont, 0)
        ax = axes([60, 140], [0, 40], x_length=6.2, y_length=4.0, xlabel=r"stock price at an exercise date",
                  ylabel=r"discounted value of continuing", xticks=[70, 100, 130], yticks=[0, 20, 40], font_size=15)
        ax.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        a = ax.ax
        itm = xs < 100
        dots = VGroup(*[Dot(a.c2p(x, min(y, 40)), radius=0.035, color=SPOT if i else GREY_D)
                        for x, y, i in zip(xs, cont, itm)])
        xx = np.linspace(60, 100, 50)
        coef = np.polyfit(xs[itm], cont[itm], 2)
        fit = curve(a, xx, np.clip(np.polyval(coef, xx), 0, 40), OPT, stroke_width=3)
        pay = curve(a, np.linspace(60, 140, 50), np.maximum(100 - np.linspace(60, 140, 50), 0), BAD, stroke_width=3)
        leg = legend([(SPOT, r"each in-the-money path: its realized future"), (OPT, r"regression: the expected future"),
                      (BAD, r"exercise now: $K - S$")], font_size=16).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        side = wrapped_label(r"Longstaff and Schwartz (2001): work backwards from expiry; at each date, regress the paths' "
                             r"realized discounted futures on simple functions of today's price, and exercise where the "
                             r"payoff beats the fitted continuation. The fitted rule is a real strategy, so its value is a "
                             r"lower bound", 4.6, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"schematic: one exercise date of an American put")
        with self.voiceover(
            "Monte Carlo runs forward in time, but exercise decisions are made backward: to decide today you need the "
            "value of waiting. Francis Longstaff and Eduardo Schwartz solved it in 2001 with a regression. At each "
            "exercise date, take the paths where the option is in the money, and record what each one actually earned "
            "by continuing. <bookmark mark='a'/> Regress those futures on simple functions of today's price: the "
            "fitted curve estimates the value of continuing. Exercise wherever the payoff beats it. Because that rule "
            "is a real strategy, the price it produces can only be a lower bound."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003, run_time=2),
                      FadeIn(leg[0]), Create(pay), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, a):
        ab = a["ab"]
        lo, hi = a["lsm"] - 0.08, max(r["upper"] + 2 * r["se"] for r in ab) + 0.04
        g = axes([0, len(ab) + 1], [lo, hi], x_length=7.4, y_length=4.2, ylabel=r"price of the American put",
                 xticks=list(range(1, len(ab) + 1)), xfmt=lambda u: f"{ab[int(round(u)) - 1]['inner']}",
                 yticks=[round(v, 2) for v in np.linspace(lo + 0.03, hi - 0.03, 4)], font_size=15,
                 xlabel=r"inner paths per point (the upper bound)")
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lsm = DashedLine(ax.c2p(0, a["lsm"]), ax.c2p(len(ab) + 1, a["lsm"]), stroke_color=GOOD, stroke_width=2.5)
        tree = DashedLine(ax.c2p(0, a["tree2000"]), ax.c2p(len(ab) + 1, a["tree2000"]), stroke_color=WHITE,
                          stroke_width=1.5)
        ups = VGroup()
        for i, r in enumerate(ab, 1):
            ups.add(VGroup(Dot(ax.c2p(i, r["upper"]), radius=0.07, color=BAD),
                           Line(ax.c2p(i, r["upper"] - 2 * r["se"]), ax.c2p(i, r["upper"] + 2 * r["se"]), stroke_color=BAD,
                                stroke_width=2)))
        leg = legend([(GOOD, rf"Longstaff--Schwartz: {a['lsm']:.3f} (lower)"),
                      (BAD, r"Andersen--Broadie (upper), $\pm 2$ s.e."),
                      (WHITE, rf"exercise at any time (2{{,}}000-step tree): {a['tree2000']:.3f}")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        last = ab[-1]
        side = VGroup(
            wrapped_label(r"the dual (Rogers 2002; Haugh and Kogan 2004): for any martingale $M$, $\mathbb{E}[\max_t (h_t - "
                          r"M_t)]$ is an upper bound; the closer $M$ is to the true value's martingale part, the tighter",
                          4.2, 18, GREY_A),
            wrapped_label(r"Andersen and Broadie (2004) build $M$ from the regression policy by nested simulation; noisy "
                          r"inner estimates inflate the bound, so it tightens as the inner paths grow", 4.2, 18, GREY_A),
            MathTex(rf"[{a['lsm']:.3f},\ {last['upper']:.3f}]", font_size=34, color=OPT),
            label(rf"25 exercise dates; with any date, tree {a['tree2000']:.3f}, PDE {a['fd']:.3f}", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        src = illustration(r"put struck at the money, one year, 20\% volatility, 5\% rates, 25 exercise dates")
        with self.voiceover(
            f"On an American put with twenty-five exercise dates, Longstaff–Schwartz gives {a['lsm']:.3f}. How far "
            "below the truth is it? A lower bound alone cannot say. <bookmark mark='a'/> Duality gives the other side. "
            "For any martingale, the expected maximum of the payoff minus the martingale is an upper bound, and Leif "
            "Andersen and Mark Broadie built a good martingale from the regression's own policy, by simulating inside "
            "the simulation. <bookmark mark='b'/> With few inner paths the noise inflates the bound; with "
            f"{last['inner']}, the price is pinned between {a['lsm']:.3f} and {last['upper']:.3f}. Allowed to exercise "
            f"at any moment rather than on twenty-five dates, the put is worth a little more, {a['tree2000']:.3f} on a "
            "fine tree, as it should be. A desk reports both bounds, not just the price."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lsm), FadeIn(leg[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in ups], lag_ratio=0.3, run_time=2.5), FadeIn(leg[1]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(tree), FadeIn(leg[2]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
