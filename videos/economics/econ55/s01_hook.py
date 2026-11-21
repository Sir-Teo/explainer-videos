from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.puzzle()
        self.question()
        self.title()
        self.objectives()

    def puzzle(self):
        P = load("puzzle")
        h = np.arange(P["h"] + 1)
        ax = plane([0, 48], [-1.4, 0.5], center=LEFT * 1.6 + DOWN * 0.45, x_length=7.8, y_length=4.8,
                   xticks=[0, 12, 24, 36, 48], yticks=[-1.0, -0.5, 0, 0.5], xlabel=r"months after the rise",
                   ylabel=r"consumer prices, \ \% change", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(48, 0), color=GREY_C, stroke_width=1.2)
        pl, cm = P["plain"]["cpi"], P["commod"]["cpi"]
        b1 = band(ax, h, pl["lo"], pl["hi"], INFL, 0.2)
        c1 = path(ax, h, pl["point"], INFL, 3.0)
        b2 = band(ax, h, cm["lo"], cm["hi"], THEORY, 0.2)
        c2 = path(ax, h, cm["point"], THEORY, 3.0)
        head = label(rf"American data, \ {P['first'][:4]}--{P['last'][:4]}: \ the Federal Reserve raises its rate one "
                     r"point", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.45)
        side = VGroup(
            label(r"a vector autoregression: \\ production, \ prices, \\ the funds rate, \ 12 months of lags",
                  font_size=18, color=GREY_A),
            label(rf"orange: \ prices rise, \\ for {P['months_above_zero']} months", font_size=19, color=INFL),
            label(r"the bank raised rates \\ when it saw inflation coming", font_size=19, color=E.ACCENT),
            label(r"green: \ add commodity prices, \\ a sign of what the bank saw", font_size=19, color=THEORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"FRED: \ industrial production, \ CPI, \ funds rate, \ PPI all commodities; \ this film's VARs",
                       corner=DR, font_size=12)
        with self.voiceover(
            "In 1992 Christopher Sims ran the most careful vector autoregressions of the day, for five countries, "
            "asking what happens after a central bank raises its rate. We can repeat his American exercise with "
            f"the data in our Data Room: industrial production, consumer prices and the federal funds rate, month by "
            f"month from {P['first'][:4]} to {P['last'][:4]}. <bookmark mark='a'/> Here is what consumer prices do "
            "after a one-point rise in the funds rate. They rise. For "
            f"{P['months_above_zero']} months the price level is higher than it would have been, by up to "
            f"{P['peak_rise']:.2f} percent, and the band around the estimate does not include a fall for more than "
            "a year. <bookmark mark='b'/> Raising rates to fight inflation, it seems, raises inflation. It came to "
            "be called the price puzzle. <bookmark mark='c'/> Sims's own diagnosis was that the Federal Reserve "
            "raised rates when it saw inflation coming, using information the model did not have, so the model "
            "mistook the bank's foresight for the effect of its policy. <bookmark mark='d'/> Give the model a "
            "piece of what the bank saw, commodity prices, which move before consumer prices do, and the puzzle "
            f"shrinks: after {P['commod_cross']} months prices are lower, and after four years "
            f"{abs(P['commod_48']):.1f} percent lower. The data had not changed. The assumption had."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), Create(zero), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(b1), Create(c1), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(c1, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(b2), Create(c2), FadeIn(side[3]), run_time=2.0)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what can a history of a few series say on its own?", font_size=26, color=DATA),
            label(r"what assumptions turn correlations into the effect of a policy?", font_size=26, color=EST),
            label(r"how are whole models of the economy estimated?", font_size=26, color=MODEL),
            label(r"and which answers survive, \ whatever the method?", font_size=26, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: with one history and no control group, how can anyone say what a policy did? <bookmark "
            "mark='a'/> What can a history of a few series say on its own? <bookmark mark='b'/> What assumptions "
            "turn its correlations into the effect of a policy? <bookmark mark='c'/> How are whole models of the "
            "economy estimated? <bookmark mark='d'/> And which answers survive, whatever the method?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["spread"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, RATE, 2.2, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 55 \ $\cdot$ \ Identifying Macro", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-five: identifying macro."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what a vector autoregression identifies, \ and what it cannot",
            r"five ways to identify a shock, \ tested where the truth is known",
            r"local projections, \ narrative and high-frequency instruments",
            r"a DSGE model estimated by the Kalman filter and Metropolis--Hastings",
            r"regions, \ matched impulse responses, \ and what macroeconomics knows",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "By the end of this part you will be able to say <bookmark mark='a'/> what a vector autoregression "
            "identifies on its own, and what it cannot; <bookmark mark='b'/> five ways of identifying a shock, "
            "each tested on the Island's history, where the true effect of policy is known; <bookmark mark='c'/> "
            "how local projections and narrative and high-frequency instruments work; <bookmark mark='d'/> how a "
            "whole model of the economy is estimated, with the Kalman filter and the Metropolis-Hastings "
            "algorithm, and what it cannot learn; <bookmark mark='e'/> and what regions, matched impulse "
            "responses and a few decades of argument have taught macroeconomics."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
