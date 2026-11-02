from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Samuelson(VoiceoverScene):
    def construct(self):
        self.card()
        self.objection(load("samuelson"))
        self.ergodic(load("ergodic"))

    def card(self):
        c = chapter_card(5, r"Samuelson's objection, and ergodicity", r"Should everyone maximize growth?",
                         part=PART)
        with self.voiceover("Chapter five. Samuelson's objection, and ergodicity."):
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
            f"Merton's grows at {100 * s['ce_rate_merton']:.1f}. Both statements are true. Kelly wins most of the "
            "time; when it loses, it loses so much that a cautious investor should not take the bet. Maximizing the "
            "probability of being ahead is not maximizing expected utility."
        ) as vo:
            self.play(FadeIn(g), FadeIn(title), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(side[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side[1:]], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def ergodic(self, e):
        t = np.asarray(e["t"])
        g = axes([0, 60], [-4, 3], x_length=7.0, y_length=4.4, xlabel=r"flips",
                 ylabel=r"wealth (log scale)", xticks=[0, 20, 40, 60], yticks=[-4, -2, 0, 2],
                 yfmt=lambda u: f"10^{{{int(u)}}}", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        paths = VGroup(*[curve(ax, t, np.clip(np.log10(np.asarray(p_)), -4, 3), GREY_B, stroke_width=1.2).set_stroke(
            opacity=0.5) for p_ in e["paths"]])
        ens = curve(ax, t, np.log10(np.asarray(e["ensemble"])), KELLY, stroke_width=4)
        med = curve(ax, t, np.log10(np.asarray(e["median"])), OVER, stroke_width=4)
        leg = legend([(KELLY, r"average over 100{,}000 players: $\times 1.05$ a flip"),
                      (OVER, r"the typical player: $\times\sqrt{1.5 \times 0.6} \approx 0.95$ a flip"),
                      (GREY_B, r"twelve players")], font_size=19).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            label(r"heads: $+50\%$, tails: $-40\%$", font_size=26),
            label(rf"after 60 flips, {100 * e['share_below_1']:.0f}\% of players have lost money", font_size=22,
                  color=OVER),
            label(rf"the richest 1\% hold {100 * e['share_of_wealth_top1pct']:.0f}\% of the wealth", font_size=22,
                  color=GREY_A),
            wrapped_label(r"Peters (2019): wealth is not ergodic; average it over time, not over parallel worlds, "
                          r"and the time average of a multiplicative gamble is its log growth: Kelly", 4.2, 20, VALUE),
            wrapped_label(r"the reply (Doctor, Wakker and Wang 2020): that is log utility under another name, and "
                          r"Samuelson's objection still applies", 4.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulation: 100{,}000 players, 60 flips")
        with self.voiceover(
            "The argument has a modern form. Toss a coin: heads, your wealth rises fifty percent; tails, it falls "
            "forty. The average outcome is a gain of five percent per toss, so the average over a hundred thousand "
            "players grows steadily. <bookmark mark='a'/> But follow any one player. Over time a head and a tail "
            "multiply wealth by one point five times zero point six, which is zero point nine: the typical player "
            f"shrinks. After sixty flips, {100 * e['share_below_1']:.0f} percent of players have lost money, and the "
            f"richest one percent hold {100 * e['share_of_wealth_top1pct']:.0f} percent of all the wealth. "
            "<bookmark mark='b'/> The physicist Ole Peters argues that this is what expected utility misses: "
            "wealth is not ergodic, its average over parallel worlds is not its average over one life, and the time "
            "average is the log growth rate, Kelly's criterion. Economists reply that this is log utility under "
            "another name, and that Samuelson's objection still stands. The debate is open. The House's position: "
            "size by growth, then cut it to a fraction for the uncertainty in the edge."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(src), Create(ens), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.05), Create(med), FadeIn(leg[1:]),
                      run_time=3)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
