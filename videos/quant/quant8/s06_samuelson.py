from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Samuelson(VoiceoverScene):
    def construct(self):
        self.card()
        self.objection(load("samuelson"))
        self.derive()
        self.ergodic(load("ergodic"), load("ergodic_live"))

    def card(self):
        c = chapter_card(10, r"Samuelson's objection, and ergodicity", r"Should everyone maximize growth?",
                         part=PART)
        with self.voiceover("Chapter ten. Samuelson's objection, and ergodicity."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def objection(self, s):
        T = np.asarray(s["T"])
        p = np.asarray(s["p_kelly_richer"])
        g = axes([0, np.log10(200)], [0.5, 1.0], x_length=6.2, y_length=3.8, xlabel=r"years",
                 ylabel=r"chance Kelly ends richer", xticks=[0, 1, 2], xfmt=lambda u: f"{10 ** u:.0f}",
                 yticks=[0.5, 0.75, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7)
        g.shift(UP * 0.4)
        ax = g.ax
        line = curve(ax, np.log10(T), p, KELLY, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(np.log10(t), q), radius=0.05, color=KELLY) for t, q in zip(T, p)])
        title = wrapped_label(r"``Why we should not make mean log of wealth big though years to act are long'' "
                              r"(Samuelson 1979): the paper is written in words of one syllable, save its last word",
                              6.4, 19, GREY_B).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"\text{{Kelly: }} {100 * s['f_kelly']:.0f}\% \qquad \gamma = 3\text{{: }} {100 * s['f_merton']:.0f}\%",
                    font_size=28),
            label(r"the $\gamma = 3$ investor's certainty equivalent, a year:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{Kelly: }} {100 * s['ce_rate_kelly']:+.1f}\%", font_size=30, color=OVER),
            MathTex(rf"\text{{Merton: }} {100 * s['ce_rate_merton']:+.1f}\%", font_size=30, color=UNDER),
            wrapped_label(r"Kelly almost surely ends richer, and the $\gamma = 3$ investor rightly refuses it: Kelly's "
                          r"rare bad paths are worse than its common good ones are good, measured in that investor's "
                          r"utility", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"$\mu - r = 6\%$, $\sigma = 18\%$, $r = 2\%$; closed forms, checked by simulation")
        with self.voiceover(
            "Kelly's admirers in the 1960s and 70s argued that everyone with a long horizon should maximize growth, "
            "whatever their risk aversion: in the long run, Kelly beats any other strategy with near certainty. Paul "
            "Samuelson thought this was a fallacy, and in 1979 wrote a reply in words of one syllable, all but the "
            "last, so that no one could misread it. <bookmark mark='a'/> Compare Kelly with the Merton fraction of an "
            f"investor with gamma three: {100 * s['f_kelly']:.0f} percent in stocks against "
            f"{100 * s['f_merton']:.0f}. The chance that Kelly ends richer does rise toward one with the horizon: "
            f"{100 * p[list(T).index(10)]:.0f} percent after ten years, {100 * p[list(T).index(100)]:.0f} after a "
            "hundred. <bookmark mark='b'/> But measured in that investor's own utility, Kelly is worse at every "
            f"horizon: its certainty equivalent shrinks at {100 * abs(s['ce_rate_kelly']):.1f} percent a year, while "
            f"Merton's grows at {100 * s['ce_rate_merton']:.1f}. Both statements are true. Maximizing the probability "
            "of being ahead is not maximizing expected utility."
        ) as vo:
            self.play(FadeIn(g), FadeIn(title), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(side[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side[1:]], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\log W_T", r"\sim", r"N\big(mT,\ s^2T\big),\quad m = r + f(\mu - r) - \tfrac12 f^2\sigma^2,\ "
                      r"s = f\sigma", font_size=30),
                cmath(r"\mathrm{CE}", r"=", r"\big(\mathbb{E}\,W_T^{1-\gamma}\big)^{\frac{1}{1-\gamma}} = "
                      r"W_0\,e^{\left(m + \frac12(1-\gamma)s^2\right)T}", font_size=30, colors={r"\mathrm{CE}": VALUE}),
                cmath(r"\tfrac1T\log\frac{\mathrm{CE}}{W_0}", r"=", r"r + f(\mu - r) - \tfrac12\,\gamma f^2\sigma^2",
                      font_size=30),
                cmath(r"\arg\max_f", r"=", r"\frac{\mu - r}{\gamma\sigma^2}\ \ne\ \frac{\mu - r}{\sigma^2}\quad"
                      r"(\gamma \ne 1)", font_size=30, colors={r"\arg\max_f": KELLY})]
        whys = [why(r"constant-fraction wealth is log-normal (Part 5)", font_size=21),
                why(r"the certainty equivalent, from the normal moment generating function", font_size=21),
                why(r"simplify: the CE growth rate, at every horizon $T$", font_size=21),
                why(r"so the investor's best fraction is Merton's at every horizon; Kelly only at $\gamma = 1$",
                    font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "The algebra behind the objection takes four lines. With a constant fraction, log wealth is normal, "
            "with a mean and a variance that both grow linearly in time. <bookmark mark='a'/> The certainty "
            "equivalent for power utility is the expected wealth to the power one minus gamma, undone; the normal "
            "moment generating function computes it exactly. <bookmark mark='b'/> Its growth rate does not depend "
            "on the horizon at all: the cash rate, plus f times the excess return, minus gamma over two times f "
            "squared sigma squared. <bookmark mark='c'/> That parabola peaks at Merton's fraction for gamma, at "
            "every horizon. A long horizon does not turn anyone into a Kelly investor, unless gamma is one."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def ergodic(self, e, L):
        bins = np.asarray(L["bins"])
        H = np.asarray(L["hist"])
        g = axes([-6, 6], [0, 0.32], x_length=7.4, y_length=3.8, xlabel=r"wealth after $t$ flips (log scale)",
                 ylabel=r"share of 100{,}000 players", xticks=[-4, -2, 0, 2, 4], xfmt=lambda u: f"10^{{{int(u)}}}",
                 yticks=[0, 0.1, 0.2, 0.3], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0)
        width = bins[1] - bins[0]

        def hist():
            k = int(tk.get_value())
            grp = VGroup()
            for i, h in enumerate(H[k]):
                if h <= 0:
                    continue
                a, b = ax.c2p(bins[i], 0), ax.c2p(bins[i] + width, min(h, 0.32))
                grp.add(Rectangle(width=b[0] - a[0] - 0.01, height=max(b[1] - a[1], 0.005), stroke_width=0,
                                  fill_color=VALUE, fill_opacity=0.75).move_to((a + b) / 2))
            return grp

        hg = always_redraw(hist)
        mean_l = always_redraw(lambda: DashedLine(ax.c2p(L["log_mean"][int(tk.get_value())], 0),
                                                  ax.c2p(L["log_mean"][int(tk.get_value())], 0.32), color=KELLY,
                                                  stroke_width=3))
        med_l = always_redraw(lambda: DashedLine(ax.c2p(L["log_median"][int(tk.get_value())], 0),
                                                 ax.c2p(L["log_median"][int(tk.get_value())], 0.32), color=OVER,
                                                 stroke_width=3))
        tn = Integer(0, font_size=30, color=GREY_A)
        tn.add_updater(lambda m: m.set_value(int(tk.get_value())))
        tl = VGroup(label(r"flip", font_size=24, color=GREY_A), tn).arrange(RIGHT, buff=0.15).next_to(g, UP, buff=0.1)
        tl.align_to(g, RIGHT)
        leg = legend([(KELLY, r"the average player: $\times 1.05$ a flip"),
                      (OVER, r"the typical (median) player: $\times\sqrt{1.5 \times 0.6} \approx 0.95$")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            label(r"heads: $+50\%$, tails: $-40\%$", font_size=24),
            label(rf"after 60 flips, {100 * e['share_below_1']:.0f}\% have lost money", font_size=21, color=OVER),
            label(rf"the richest 1\% hold {100 * e['share_of_wealth_top1pct']:.0f}\% of the wealth", font_size=21,
                  color=GREY_A),
            wrapped_label(r"Peters (2019): wealth is not ergodic; its time average is the log growth: Kelly. Meder et "
                          r"al.\ (2021): subjects' risk taking shifted toward the time-optimal one when the dynamics "
                          r"were multiplicative", 4.4, 18, VALUE),
            wrapped_label(r"replies: Doctor, Wakker and Wang (2020): log utility under another name; Toda (2023): a "
                          r"sharp critique of ``ergodicity economics''", 4.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        q = pause_card(r"What fraction of your wealth should you stake on this coin each flip?", width=4.4,
                       font_size=20).to_edge(RIGHT, buff=0.35).to_edge(DOWN, buff=0.3)
        src = illustration(r"simulation: 100{,}000 players, 60 flips")
        with self.voiceover(
            "The argument has a modern form. Toss a coin: heads, your wealth rises fifty percent; tails, it falls "
            "forty. The average outcome is a gain of five percent per toss. Give the coin to a hundred thousand "
            "players and watch the distribution of their wealth, on a log scale. <bookmark mark='a'/> The average, "
            "in gold, runs off to the right, carried by a lucky few. The median player, in red, drifts left: a head "
            "and a tail together multiply wealth by point nine. After sixty flips, "
            f"{100 * e['share_below_1']:.0f} percent of players have lost money, and the richest one percent hold "
            f"{100 * e['share_of_wealth_top1pct']:.0f} percent of all the wealth. <bookmark mark='b'/> The physicist "
            "Ole Peters argues this is what expected value misses: the average over parallel worlds is not the "
            "average over one life, and the time average is the log growth rate, Kelly's criterion. An experiment by "
            "Meder and colleagues in 2021 found people's risk taking moved toward the time-optimal one when the "
            "gambles were multiplicative. Economists reply that this is log utility under another name, and "
            "Alexis Akira Toda's 2023 critique is sharper still. The debate is open. <bookmark mark='c'/> Pause "
            "and predict: what fraction should you stake on this coin? <bookmark mark='d'/> Kelly says "
            f"{100 * L['kelly_stake']:.0f} percent, which grows wealth about {100 * L['kelly_growth']:.1f} percent a "
            "flip: staking part of your wealth turns a losing game into a winning one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(src), FadeIn(leg), FadeIn(tl))
            self.add(hg, mean_l, med_l)
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(H) - 1), run_time=max(min(vo.remaining(10.0) - 2, 12), 7),
                      rate_func=linear)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
        for m in (hg, mean_l, med_l, tn):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
