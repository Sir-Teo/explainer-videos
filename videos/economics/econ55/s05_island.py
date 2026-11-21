from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


def pair(yr=(-0.9, 0.4), pr=(-0.6, 0.2), h=16, top=0.0):
    axy = plane([0, h], list(yr), center=LEFT * 3.4 + DOWN * (0.45 - top), x_length=5.4, y_length=4.0,
                xticks=[0, 4, 8, 12, 16], yticks=[-0.8, -0.4, 0, 0.4], xlabel=r"quarters",
                ylabel=r"output, \ \% per point of the rate", xfmt=lambda v: f"{v:.0f}",
                yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=12)
    axp = plane([0, h], list(pr), center=RIGHT * 2.0 + DOWN * (0.45 - top), x_length=5.4, y_length=4.0,
                xticks=[0, 4, 8, 12, 16], yticks=[-0.6, -0.4, -0.2, 0, 0.2], xlabel=r"quarters",
                ylabel=r"inflation, \ points", xfmt=lambda v: f"{v:.0f}",
                yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=12)
    zs = VGroup(DashedLine(axy.ax.c2p(0, 0), axy.ax.c2p(h, 0), color=GREY_D, stroke_width=1),
                DashedLine(axp.ax.c2p(0, 0), axp.ax.c2p(h, 0), color=GREY_D, stroke_width=1))
    return axy, axp, zs


class Island(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The five, \ on the Island's history", r"Which assumptions recover the truth?",
             "Chapter four. The five, on the Island's history.", lit={2018: r"Stock and Watson"}, scale=("nation",),
             horizon=("a decade",))
        self.one()
        self.many()

    def one(self):
        S = load("schemes")
        tr = S["truth"]["monetary"]
        h = np.arange(len(tr["y"]))
        axy, axp, zs = pair()
        truth = VGroup(path(axy, h, tr["y"], TRUTHC, 3.0), path(axp, h, tr["pi"], TRUTHC, 3.0))
        sg = S["sign"]
        sband = VGroup(band(axy, h, sg["y"]["lo"], sg["y"]["hi"], METHOD["sign"], 0.22),
                       band(axp, h, sg["pi"]["lo"], sg["pi"]["hi"], METHOD["sign"], 0.22))
        lines = {}
        for m in ("recursive", "proxy", "hetero"):
            lines[m] = VGroup(path(axy, h, S[m]["y"], METHOD[m], 2.4, yr=(-0.9, 0.4)),
                              path(axp, h, S[m]["pi"], METHOD[m], 2.4, yr=(-0.6, 0.2)))
        side = VGroup(
            label(r"white: \ the truth", font_size=18, color=TRUTHC),
            label(r"grey: \ timing", font_size=18, color=METHOD["recursive"]),
            label(r"blue: \ signs \ (the middle \\ two thirds of the set)", font_size=18, color=METHOD["sign"]),
            label(r"gold: \ the instrument", font_size=18, color=METHOD["proxy"]),
            label(r"purple: \ the variance", font_size=18, color=METHOD["hetero"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.25)
        tag = island_tag(rf"simulated: \ one history of {S['T']} quarters", corner=DR, font_size=13)
        with self.voiceover(
            f"On the Island we know the truth, so take one history of {S['T']} quarters and try each scheme. "
            "<bookmark mark='a'/> In white, what a one-point rise in the rate truly does: output dips and recovers; "
            "inflation drops at once and fades. <bookmark mark='b'/> Timing gets it wrong. It forces the "
            "first-quarter effects to zero, which the Island's bank violates, so inflation barely moves and "
            "output falls less than it should. <bookmark mark='c'/> Signs give a band. For inflation it contains "
            "the truth for a year and a half; for output its middle runs well below it. The set of mixing matrices "
            "that obey the signs is wide, and how the band looks depends on how the candidates were drawn, as "
            "Christiane Baumeister and James Hamilton warned. <bookmark mark='d'/> The outside instrument lands "
            "near the truth, <bookmark mark='e'/> and so does the change in variance. One history is noisy, "
            "though; the instrument's output path wanders after two years."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), FadeIn(zs), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["recursive"]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(sband), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["proxy"]), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(lines["hetero"]), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def many(self):
        M = load("schemes_mc")
        tr = M["truth"]["monetary"]
        h = np.arange(len(tr["y"]))
        axy, axp, zs = pair()
        truth = VGroup(path(axy, h, tr["y"], TRUTHC, 3.0), path(axp, h, tr["pi"], TRUTHC, 3.0))
        groups = {}
        for m in ("recursive", "proxy", "hetero"):
            d = M["methods"][m]
            groups[m] = VGroup(band(axy, h, d["y"]["lo"], d["y"]["hi"], METHOD[m], 0.14),
                               band(axp, h, d["pi"]["lo"], d["pi"]["hi"], METHOD[m], 0.14),
                               path(axy, h, d["y"]["mean"], METHOD[m], 2.6, yr=(-0.9, 0.4)),
                               path(axp, h, d["pi"]["mean"], METHOD[m], 2.6, yr=(-0.6, 0.2)))
        rec, prx = M["methods"]["recursive"], M["methods"]["proxy"]
        lr = M["methods"]["long_run"]["y"]["mean"]
        side = VGroup(
            label(rf"{M['reps']} histories: \\ the average, \ and 90\% \\ of the histories", font_size=18,
                  color=WHITE),
            label(r"timing: \ wrong on average", font_size=18, color=METHOD["recursive"]),
            label(r"instrument and variance: \\ right on average", font_size=18, color=METHOD["proxy"]),
            label(rf"the long run finds supply: \\ output $+{lr[-1]:.2f}$ for ever \\ (truth "
                  rf"$+{M['truth']['supply']['y'][-1]:.2f}$)", font_size=18, color=METHOD["long_run"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.25)
        tag = island_tag(rf"simulated: \ {M['reps']} histories", corner=DR, font_size=13)
        with self.voiceover(
            f"So run each scheme on {M['reps']} histories and average. <bookmark mark='a'/> Timing is wrong on "
            f"average, not by bad luck: inflation's first-quarter fall is "
            f"{say_num(tr['pi'][0], 2)} points, and timing says zero, by assumption, every time. <bookmark "
            "mark='b'/> The instrument and the change in variance are right on average, the variance a little "
            "noisier. <bookmark mark='c'/> And the long-run restriction answers a different question. It cannot "
            "separate demand from money, since neither moves output for ever, but it finds the supply shock: "
            f"output up {lr[-1]:.2f} percent for good, against {M['truth']['supply']['y'][-1]:.2f} in truth. "
            "<bookmark mark='d'/> Each scheme is only as good as its assumption, and on the Island, unlike in the "
            "world, we can check."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), FadeIn(zs), Create(truth), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(groups["recursive"]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(groups["proxy"]), FadeIn(groups["hetero"]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(truth, color=WHITE, scale_factor=1.0))
        del rec, prx
        self.clear_scene()
