from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Option(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The option to wait", r"Why might a firm not build a project that pays for itself?",
             "Chapter three. The option to wait.", lit={1986: r"McDonald and Siegel", 1994: r"Dixit and Pindyck",
                                                         2009: r"Bloom"}, scale=("firm",), horizon=("years",))
        self.irreversible()
        self.threshold()
        self.uncertainty()

    def irreversible(self):
        rows = VGroup(
            label(r"the textbook rule: \ build if the project is worth more than it costs", font_size=25,
                  color=GREY_A),
            label(r"but most investment cannot be undone: \ a mine, \ a factory, \ a pipeline is sunk", font_size=24,
                  color=FIRM),
            label(r"and most can be delayed: \ next year you will know more", font_size=24, color=STOCK),
            label(r"building now kills an option to wait, \ and that option has value", font_size=26, color=E.ACCENT),
            label(r"Robert McDonald and Daniel Siegel, \ 1986; \ Avinash Dixit and Robert Pindyck, \ 1994", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"McDonald and Siegel, QJE 101(4) (1986); \ Dixit and Pindyck, \emph{Investment under "
                            r"Uncertainty} (1994)", corner=DR, font_size=12)
        with self.voiceover(
            "The user cost assumed a firm could sell a machine as easily as buy one. <bookmark mark='a'/> The "
            "textbook rule says build if the project is worth more than it costs. <bookmark mark='b'/> But most "
            "investment cannot be undone. A mine, a factory or a pipeline is sunk the day it is built. "
            "<bookmark mark='c'/> And most investment can be put off: next year you will know more about prices and "
            "demand. <bookmark mark='d'/> Building now kills the option to wait, and that option is worth something. "
            "<bookmark mark='e'/> Robert McDonald and Daniel Siegel priced it in 1986, and Avinash Dixit and Robert "
            "Pindyck made it a theory of investment."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def threshold(self):
        o = load("option")
        ax = plane([0, 0.5], [1, 4.5], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[1, 2, 3, 4],
                   xlabel=r"volatility of the project's value, \ a year", ylabel=r"build when value exceeds cost by",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: rf"{v:g}\times", font_size=16)
        npv = seg(ax, 0, 1, 0.5, 1, color=GREY_B, width=2, dashed=True)
        curve = path(ax, o["sigma"], o["multiple"], color=FIRM, width=4, yr=(1, 4.5))
        dots = VGroup(*[dot(ax, r["sigma"], r["multiple"], color=STOCK) for r in o["rows"]])
        side = VGroup(
            MathTex(r"dV = \mu V\,dt + \sigma V\,dW", font_size=32, color=WHITE),
            label(rf"interest {pc(o['r'], 0)}, \ no drift", font_size=19, color=GREY_A),
            label(r"the rule: \ build when $V \ge \frac{\beta}{\beta - 1} I$", font_size=21, color=FIRM),
            *[label(rf"volatility {100 * r['sigma']:.0f}\%: \ {r['multiple']:.2f} times the cost", font_size=19,
                    color=STOCK) for r in o["rows"]],
            label(r"NPV rule: \ 1 times", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Make it concrete. A project's value wanders up and down at random, with a given volatility. Building "
            "costs a fixed sum, once. <bookmark mark='a'/> The net present value rule says build as soon as the value "
            "passes the cost: the dashed line at one. <bookmark mark='b'/> The optimal rule is to wait until value "
            "exceeds cost by a margin that grows with uncertainty. <bookmark mark='c'/> With interest at four "
            f"percent and a volatility of {100 * o['rows'][0]['sigma']:.0f} percent a year, build at "
            f"{o['rows'][0]['multiple']:.2f} times the cost. At twenty percent, at twice the cost. At forty, at "
            f"{o['rows'][-1]['multiple']:.2f} times. <bookmark mark='d'/> Waiting is not timidity. It is the price "
            "of an option that building would destroy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(npv), FadeIn(side[-1]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(r) for r in side[3:-1]], lag_ratio=0.3), run_time=3)
            vo.wait_until("d")
            self.play(Indicate(curve, color=WHITE))
        self.clear_scene()

    def uncertainty(self):
        rows = VGroup(
            label(r"Nicholas Bloom, \ 2009: \ the impact of uncertainty shocks", font_size=26, color=E.ACCENT),
            label(r"when uncertainty jumps, \ the threshold jumps: \ firms pause hiring and investment", font_size=23,
                  color=RISK),
            label(r"then, \ as uncertainty fades, \ pent-up projects go ahead: \ a drop and a rebound", font_size=23,
                  color=FIRM),
            label(r"so policy that is itself uncertain has a cost, \ even before it is decided", font_size=23,
                  color=GREY_A),
            label(r"and investment is lumpy: \ long waits, \ then bursts \ (Part 52)", font_size=23, color=STOCK),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Bloom, Econometrica 77(3) (2009): \ 623--685", corner=DR, font_size=12)
        with self.voiceover(
            "This matters for business cycles. <bookmark mark='a'/> In 2009 Nicholas Bloom modelled firms with "
            "such options facing shocks to uncertainty itself. <bookmark mark='b'/> When uncertainty jumps, the "
            "threshold jumps with it, and firms pause hiring and investment all at once. <bookmark mark='c'/> As "
            "uncertainty fades, the projects that waited go ahead: a sharp drop and a rebound. "
            "<bookmark mark='d'/> So uncertainty about policy has a cost even before anything is decided. "
            "<bookmark mark='e'/> And investment in individual plants is lumpy, long waits and then bursts; whether "
            "that lumpiness survives in the aggregate is a question for Part fifty-two."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
