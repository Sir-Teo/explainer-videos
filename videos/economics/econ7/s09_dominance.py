from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

NET_COLOR = {"old": LATER, "better": SAFE, "spread": RISKY}
NET_NAME = {"old": r"the old net", "better": r"the better net", "spread": r"the wide net"}


def bars(ax, x, p, color, dx=0.0, width=0.5):
    a = ax.ax
    g = VGroup()
    for xi, pi in zip(x, p):
        h = a.c2p(0, pi)[1] - a.c2p(0, 0)[1]
        g.add(Rectangle(width=width, height=max(h, 1e-3), stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
            a.c2p(xi, 0) + RIGHT * dx, aligned_edge=DOWN))
    return g


class Dominance(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Stochastic dominance", r"When is one gamble better than another for everyone who likes more, "
             r"or everyone who dislikes risk?", "Chapter seven. Stochastic dominance.", lit={1970: r"Rothschild and "
                                                                                                r"Stiglitz"})
        self.first_order()
        self.second_order()

    def nets(self, keys, center=LEFT * 3.6 + UP * 1.45):
        d = load("dominance")
        ax = plane([-1, 13], [0, 0.6], center=center, x_length=5.6, y_length=2.2, xticks=[0, 2, 4, 6, 8, 10, 12],
                   yticks=[0, 0.25, 0.5], xlabel=r"fish a day", ylabel=r"chance", font_size=15)
        offs = {1: [0.0], 2: [-0.17, 0.17]}[len(keys)]
        g = VGroup(*[bars(ax, d[k]["x"], d[k]["p"], NET_COLOR[k], dx=o, width=0.32) for k, o in zip(keys, offs)])
        return d, ax, g

    def cdf_axes(self, ylab, top=1.0, center=LEFT * 3.6 + DOWN * 1.9, yticks=(0, 0.5, 1.0)):
        return plane([-1, 13], [0, top], center=center, x_length=5.6, y_length=2.6, xticks=[0, 2, 4, 6, 8, 10, 12],
                     yticks=list(yticks), xlabel=r"fish", ylabel=ylab, font_size=15)

    def first_order(self):
        d, ax, g = self.nets(["old", "better"])
        cx = self.cdf_axes(r"chance of no more than this")
        grid = np.array(d["grid"])
        F0 = path(cx, grid, np.array(d["old"]["F"]), color=NET_COLOR["old"], width=3, smooth=False)
        F1 = path(cx, grid, np.array(d["better"]["F"]), color=NET_COLOR["better"], width=3, smooth=False)
        legend = VGroup(*[label(rf"{NET_NAME[k]}: \ " + r", ".join(f"{x}" for x in d[k]["x"]) + r" fish",
                                font_size=20, color=NET_COLOR[k]) for k in ("old", "better")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(13.0, 0.62), aligned_edge=UR)
        side = VGroup(
            label(r"first-order dominance:", font_size=27, color=SAFE),
            label(r"the better net's CDF is nowhere above the old one's: \\ for every catch $c$, \ it is at least "
                  r"as likely \\ to bring more than $c$", font_size=23),
            MathTex(r"F_{\text{better}}(c) \;\le\; F_{\text{old}}(c) \quad \text{for all } c", font_size=34,
                    color=SAFE),
            label(r"then everyone who prefers more fish to fewer \\ prefers the better net, \ whatever their "
                  r"utility", font_size=23, color=E.ACCENT),
            label(r"not the same as a higher mean: \\ a higher mean is necessary, \ not enough", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Sometimes we don't need to know anyone's utility function to say which gamble is better. "
            "<bookmark mark='a'/> Ana's old net brings two, six or ten fish a day, with chances a quarter, a half and "
            "a quarter. A better net turns the worst days into four. <bookmark mark='b'/> Draw each net's cumulative "
            "distribution: the chance of catching no more than each number. The better net's curve is never above "
            "the old one's. <bookmark mark='c'/> That's first-order stochastic dominance: for every catch, the better "
            "net is at least as likely to beat it. <bookmark mark='d'/> And then everyone who prefers more fish to "
            "fewer, risk lover or risk hater, prefers the better net. Expected utility with any increasing utility "
            "function agrees. <bookmark mark='e'/> A higher mean is necessary for this, but not enough: one gamble "
            "can have the higher mean and still have a worse bad tail."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(legend[0]))
            self.play(FadeIn(g[1]), FadeIn(legend[1]))
            vo.wait_until("b")
            self.play(FadeIn(cx), Create(F0), Create(F1), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def second_order(self):
        d, ax, g = self.nets(["old", "spread"])
        grid = np.array(d["grid"])
        cx = self.cdf_axes(r"$\int F$: \ area under the CDF", top=7.0, yticks=(0, 2, 4, 6))
        I0 = path(cx, grid, np.array(d["old"]["IF"]), color=NET_COLOR["old"], width=3)
        I1 = path(cx, grid, np.array(d["spread"]["IF"]), color=NET_COLOR["spread"], width=3)
        legend = VGroup(*[label(rf"{NET_NAME[k]}: \ " + r", ".join(f"{x}" for x in d[k]["x"]) + r" fish",
                                font_size=20, color=NET_COLOR[k]) for k in ("old", "spread")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(13.0, 0.62), aligned_edge=UR)
        ce = d["ce"]
        side = VGroup(
            label(r"the wide net: \ the same mean, 6 fish, \\ spread further: \ 0 or 12 on the edges", font_size=23,
                  color=RISKY),
            label(r"a mean-preserving spread \ (Rothschild and Stiglitz, 1970)", font_size=23, color=GREY_A),
            label(r"second-order dominance: \ the area under \\ the old net's CDF is nowhere larger", font_size=24,
                  color=LATER),
            label(r"then everyone who dislikes risk prefers the old net", font_size=23, color=E.ACCENT),
            label(rf"certainty equivalents, \ $\gamma$ = 0.5, 2, 5: \\ old {ce['old']['0.5']:.2f}, "
                  rf"{ce['old']['2']:.2f}, {ce['old']['5']:.2f}; \ wide {ce['spread']['0.5']:.2f}, "
                  rf"{ce['spread']['2']:.2f}, {ce['spread']['5']:.2f}", font_size=21),
            label(r"``riskier'' made precise: \ the same mean, \\ and every risk averter likes it less", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now a harder comparison. <bookmark mark='a'/> A wide net catches the same six fish on average, but its "
            "bad days bring nothing and its good days twelve. <bookmark mark='b'/> It's the old net with its outcomes "
            "pushed apart, keeping the mean: what Michael Rothschild and Joseph Stiglitz, in 1970, called a "
            "mean-preserving spread. Neither net dominates the other in the first-order sense: the wide net has the "
            "better best day and the worse worst day. <bookmark mark='c'/> But compare the areas under their "
            "cumulative distributions, built up from the left. The old net's area is never larger. That's "
            "second-order dominance, <bookmark mark='d'/> and it means everyone who dislikes risk, every concave "
            "utility function, prefers the old net. <bookmark mark='e'/> The certainty equivalents agree, at every "
            "level of risk aversion: the gap widens as gamma grows. <bookmark mark='f'/> This is what riskier means, "
            "made precise: a spread around the same mean that every risk-averse person dislikes. It will matter when "
            "we price assets and design insurance."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(g[0]), FadeIn(legend[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]), FadeIn(legend[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cx), Create(I0), Create(I1), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
