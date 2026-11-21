from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Hard(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Why recessions are hard to forecast", r"Why does the best forecast almost never say "
             r"`recession'?", "Chapter eight. Why recessions are hard to forecast.",
             lit={1989: r"Hamilton", 1976: r"Lucas"}, scale=("nation",), horizon=("a year",))
        self.regimes()
        self.never()
        self.reflexive()

    def regimes(self):
        Rg = load("regimes")
        y, s, pr = np.array(Rg["y"]), np.array(Rg["s"]), np.array(Rg["prob"])
        t = np.arange(len(y))
        ax = plane([0, len(y)], [-9, 9], center=UP * 0.9 + LEFT * 1.4, x_length=10.2, y_length=3.2,
                   xticks=[], yticks=[-6, 0, 6], xlabel=r"", ylabel=r"growth, \ \% a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=12)
        spans, cur = [], None
        for k, v in enumerate(s):
            if v == 1 and cur is None:
                cur = k
            if v == 0 and cur is not None:
                spans.append((cur, k))
                cur = None
        if cur is not None:
            spans.append((cur, len(s)))
        rec = shade(ax, spans, -9, 9, RECESS, 0.6)
        line = path(ax, t, y, SPF, 2.0, smooth=False)
        axp = plane([0, len(y)], [0, 1], center=DOWN * 2.0 + LEFT * 1.4, x_length=10.2, y_length=1.6,
                    xticks=[0, 40, 80, 120, 160], yticks=[0, 0.5, 1], xlabel=r"quarters",
                    ylabel=r"inferred chance of recession", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                    font_size=12)
        rec2 = shade(axp, spans, 0, 1, RECESS, 0.6)
        lp = path(axp, t, pr, GB, 2.2, smooth=False)
        side = VGroup(
            MathTex(r"y_t = \mu_{s_t} + \sigma \varepsilon_t", font_size=28, color=SPF),
            label(rf"$\mu$: \ ${Rg['mu'][0]:+.0f}$ in expansion, \\ ${Rg['mu'][1]:+.0f}$ in recession", font_size=17,
                  color=GREY_A),
            label(rf"stay: \ {Rg['p_stay'][0]:.2f} and {Rg['p_stay'][1]:.2f} \\ a quarter", font_size=17,
                  color=GREY_A),
            label(rf"recessions found: \ {Rg['found']} of {Rg['starts']}, \\ "
                  rf"{Rg['mean_lag']:.1f} quarters late \ on average", font_size=17, color=GB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ Hamilton's two regimes", corner=DR, font_size=12)
        c_e = Circle(radius=0.55, color=SPF, stroke_width=3).move_to(ax.ax.c2p(len(y) * 0.3, 0))
        c_r = Circle(radius=0.55, color=ERR, stroke_width=3).move_to(ax.ax.c2p(len(y) * 0.7, 0))
        t_e = label(rf"expansion \\ ${Rg['mu'][0]:+.0f}$", font_size=17, color=SPF).move_to(c_e)
        t_r = label(rf"recession \\ ${Rg['mu'][1]:+.0f}$".replace("-", "{-}"), font_size=17, color=ERR).move_to(c_r)
        a1 = CurvedArrow(c_e.get_top() + RIGHT * 0.2, c_r.get_top() + LEFT * 0.2, angle=-PI / 4, color=GREY_B,
                         stroke_width=2)
        a2 = CurvedArrow(c_r.get_bottom() + LEFT * 0.2, c_e.get_bottom() + RIGHT * 0.2, angle=-PI / 4,
                         color=GREY_B, stroke_width=2)
        p1 = label(f"{1 - Rg['p_stay'][0]:.2f}", font_size=16, color=GREY_A).next_to(a1, UP, buff=0.05)
        p2 = label(f"{1 - Rg['p_stay'][1]:.2f}", font_size=16, color=GREY_A).next_to(a2, DOWN, buff=0.05)
        s1 = label(rf"stay {Rg['p_stay'][0]:.2f}", font_size=16, color=SPF).next_to(c_e, LEFT, buff=0.2)
        s2 = label(rf"stay {Rg['p_stay'][1]:.2f}", font_size=16, color=ERR).next_to(c_r, RIGHT, buff=0.2)
        chain2 = VGroup(c_e, c_r, t_e, t_r, a1, a2, p1, p2, s1, s2)
        with self.voiceover(
            "Why is it so hard? Start with James Hamilton's model of 1989. <bookmark mark='a'/> The economy is in "
            f"one of two states: expansion, with growth around {Rg['mu'][0]:.0f} percent a year, or recession, "
            f"around {say_num(Rg['mu'][1], 0)}. Expansions persist with probability {Rg['p_stay'][0]:.2f} a "
            f"quarter, recessions with {Rg['p_stay'][1]:.2f}. <bookmark mark='b'/> Here is a simulated history, "
            "recessions shaded. <bookmark mark='c'/> Hamilton's filter infers the state from growth alone. It finds "
            f"{Rg['found']} of the {Rg['starts']} recessions, but on average {Rg['mean_lag']:.1f} quarters after "
            "they began: recognizing, again, rather than forecasting."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(chain2))
            vo.wait_until("b")
            self.play(FadeOut(chain2), run_time=0.6)
            self.play(FadeIn(rec), Create(line), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(axp), FadeIn(rec2), Create(lp), FadeIn(side[3]), run_time=2.5)
        self.clear_scene()

    def never(self):
        Rg, S = load("regimes"), load("score")
        rows = Rg["rows"]
        h = np.array([r["h"] for r in rows])
        ax = plane([-0.3, 4.3], [-3.5, 3.5], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.4, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[-3, 0, 3], xlabel=r"quarters ahead",
                   ylabel=r"best forecast of growth, \ knowing today's state", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        z = DashedLine(ax.ax.c2p(-0.3, 0), ax.ax.c2p(4.3, 0), color=GREY_C, stroke_width=1.2)
        fe = path(ax, h, [r["f_exp"] for r in rows], SPF, 3.0, smooth=False)
        fr = path(ax, h, [r["f_rec"] for r in rows], ERR, 3.0, smooth=False)
        r4 = S["rows"][-1]
        side = VGroup(
            label(r"blue: \ from inside an expansion", font_size=18, color=SPF),
            label(r"red: \ from inside a recession", font_size=18, color=ERR),
            label(rf"quarters of falling growth: \ {100 * Rg['share_neg_growth']:.0f}\%", font_size=18,
                  color=GREY_A),
            label(rf"best forecasts a year ahead \\ below zero: \ {100 * rows[-1]['share_neg']:.0f}\%", font_size=18,
                  color=E.ACCENT),
            label(rf"the real forecasters, \ a year ahead: \\ below zero {100 * r4['share_neg_fc']:.0f}\% of the "
                  rf"time; \\ growth fell in {100 * r4['share_neg_act']:.0f}\% of quarters", font_size=18,
                  color=FIRST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Now suppose a forecaster knew the model exactly, and even knew today's state for certain. <bookmark "
            "mark='a'/> From inside an expansion, the best forecast is positive at every horizon. <bookmark "
            "mark='b'/> From inside a recession, it is negative for a couple of quarters, then positive, because "
            "recessions end. <bookmark mark='c'/> So the forecast that minimizes squared error is below zero a "
            "year ahead in none of the quarters, though growth is negative in "
            f"{100 * Rg['share_neg_growth']:.0f} percent of them. <bookmark mark='d'/> The real forecasters do the "
            f"same: their forecasts a year ahead were below zero {100 * r4['share_neg_fc']:.0f} percent of the time, "
            f"and growth was negative in {100 * r4['share_neg_act']:.0f} percent of quarters. This is not cowardice. "
            "When an event is rare and its timing random, the best guess of the average is never the event."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(z))
            vo.wait_until("a")
            self.play(Create(fe), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fr), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def reflexive(self):
        chain = flow_chain([(r"a forecast of recession", ERR), (r"the central bank cuts rates; \ firms delay "
                                                                  r"hiring", GB),
                            (r"the recession is milder, \ or never comes", LATEST),
                            (r"the forecast looks wrong", BENCH)], direction=RIGHT, box_w=2.9, box_h=1.2, buff=0.45,
                           font_size=19)
        chain.move_to(UP * 0.4)
        foot = label(r"a forecast that changes the outcome cannot be scored like a forecast of the weather",
                     font_size=22, color=E.ACCENT).next_to(chain, DOWN, buff=0.8)
        top = label(r"forecasts that change what they forecast", font_size=28, color=WHITE).to_edge(UP, buff=0.8)
        with self.voiceover(
            "And there is a second difficulty, which weather forecasters do not have. <bookmark mark='a'/> A "
            "forecast of recession, if believed, <bookmark mark='b'/> can lead a central bank to cut rates and "
            "firms to hold back, <bookmark mark='c'/> which can make the recession milder, or prevent it, "
            "<bookmark mark='d'/> and then the forecast looks wrong. Robert Lucas's critique, from Part twenty-eight, "
            "applies to forecasts too: when people act on a prediction, the pattern it was fitted to can change. "
            "<bookmark mark='e'/> Some of 2023's missing recession may be of this kind; no one can say how much."
        ) as vo:
            self.play(FadeIn(top))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=UP * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
