from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAIN, GAUSS, LOSS, PART, REAL, hist_bars, load


class Efficient(VoiceoverScene):
    def construct(self):
        n = load("nagel")
        self.card()
        self.fama()
        self.paradox()
        self.noise()
        self.nagel(n)

    def card(self):
        c = chapter_card(9, r"Efficient markets", r"If prices are fair, who makes them fair?", lit=(1970, 1980, 1986),
                         part=PART)
        with self.voiceover("Chapter nine. Efficient markets."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def fama(self):
        d = definition_card(r"Efficient market (Fama, 1970)", r"A market in which prices always ``fully reflect'' "
                            r"available information.", width=8.2, color=REAL, font_size=26).to_edge(UP, buff=0.4)
        forms = VGroup()
        for name, what, test in (
                (r"weak", r"past prices", r"chapter 4: the variance ratio"),
                (r"semi-strong", r"all public information", r"event studies: earnings, mergers, splits"),
                (r"strong", r"all information, even private", r"insiders do earn more: it fails")):
            forms.add(VGroup(label(name, font_size=28, color=QC.IDEA), label(what, font_size=24),
                             label(test, font_size=21, color=GREY_B)).arrange(DOWN, buff=0.12))
        forms.arrange(RIGHT, buff=0.7).next_to(d, DOWN, buff=0.6)
        joint = theorem_card(r"The joint-hypothesis problem", r"Every test of efficiency is also a test of a model of "
                             r"what returns \emph{should} be. A strategy that beats the market may have found a "
                             r"mispricing, or may have found a risk that deserves its reward. The data cannot tell "
                             r"the two apart without the model.", width=11.0, font_size=23, kind=r"Fama").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1970 Eugene Fama gathered the evidence of the previous decades into one idea: an efficient market is "
            "one in which prices always fully reflect the available information. <bookmark mark='a'/> He sorted the "
            "evidence into three forms. Weak: past prices can't be used to beat the market; chapter four tested "
            "that. Semi-strong: no public information can, which is tested by watching prices react to news. "
            "Strong: not even private information can; that one fails, insiders do profit, which is why insider "
            "trading is illegal. <bookmark mark='b'/> And he named the catch that has run through the field ever "
            "since. Every test of efficiency is also a test of a model of what returns should be. If a strategy "
            "beats the market, it may have found a mispricing, or it may be taking a risk that deserves its "
            "reward. Without a model of risk, the data cannot tell those apart. Act four of this series is that "
            "argument."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in forms], lag_ratio=0.6, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(joint, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def paradox(self):
        steps = [r"prices reflect\\all information", r"no one is paid\\to find information",
                 r"no one finds it", r"prices stop\\reflecting it", r"finding it pays", r"traders find it"]
        nodes = VGroup()
        R = 2.6
        for i, s in enumerate(steps):
            ang = PI / 2 - i * TAU / len(steps)
            t = Tex(r"\begin{tabular}{c}" + s + r"\end{tabular}", font_size=26)
            box = RoundedRectangle(width=2.9, height=1.05, corner_radius=0.15, stroke_color=QC.IDEA, stroke_width=2)
            nodes.add(VGroup(box, t.move_to(box)).move_to(R * np.array([np.cos(ang) * 1.12, np.sin(ang), 0])))
        arrows = VGroup()
        for i in range(len(steps)):
            a, b = nodes[i], nodes[(i + 1) % len(steps)]
            arrows.add(CurvedArrow(a.get_center() + (b.get_center() - a.get_center()) * 0.33,
                                   a.get_center() + (b.get_center() - a.get_center()) * 0.67, angle=-0.4,
                                   color=GREY_B, stroke_width=3))
        cyc = VGroup(nodes, arrows).scale(0.9).shift(LEFT * 2.9 + DOWN * 0.2)
        card = history_card(1980, r"Sanford Grossman and Joseph Stiglitz, \textit{AER}",
                            r"``On the impossibility of informationally efficient markets'': if information is costly, "
                            r"prices can't fully reflect it, or no one would pay to gather it. In equilibrium the "
                            r"market is \emph{just inefficient enough} to pay those who make it efficient.",
                            width=4.8, font_size=21).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "There is a paradox at the heart of the idea. If prices already reflected all information, nobody "
            "would be paid for finding information. <bookmark mark='a'/> So nobody would look, and prices would "
            "stop reflecting it. Then finding information would pay again, and traders would find it, and prices "
            "would reflect it once more. <bookmark mark='b'/> In 1980 Sanford Grossman and Joseph Stiglitz turned "
            "the paradox into a theorem: when information costs money, a perfectly efficient market is impossible. "
            "In equilibrium the market is just inefficient enough to pay the people who make it efficient. That "
            "sentence is the business model of every firm in Part thirty-four."
        ) as vo:
            self.play(FadeIn(nodes[0]))
            self.play(Create(arrows[0]), FadeIn(nodes[1]))
            vo.wait_until("a")
            for i in range(2, len(steps)):
                self.play(Create(arrows[i - 1]), FadeIn(nodes[i]), run_time=0.8)
            self.play(Create(arrows[-1]))
            vo.wait_until("b")
            self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def noise(self):
        card = history_card(1986, r"Fischer Black, ``Noise'', \textit{Journal of Finance}",
                            r"Noise traders, who trade on what they think is information but isn't, make trading "
                            r"possible at all; they also make prices noisy. ``We might define an efficient market as "
                            r"one in which price is within a factor of 2 of value.''", width=9.6, font_size=25)
        card.move_to(UP * 0.6)
        tie = wrapped_label(r"Milgrom--Stokey (1982): from a Pareto-efficient allocation, common priors and "
                            r"common-knowledge rationality rule out trade based on private information alone",
                            10.0, 22, GREY_A).next_to(card, DOWN, buff=0.5)
        with self.voiceover(
            "Six years later Fischer Black, of Black and Scholes, gave the other half of the answer in his "
            "presidential address, called Noise. With a common prior and an efficient initial allocation, "
            "rational traders cannot create trade from private information alone. Risk sharing, liquidity needs "
            "and different beliefs also matter. Black emphasized noise: people who trade on things they believe "
            "are information but aren't. Noise makes "
            "markets liquid, and it also makes prices noisy. With characteristic dryness Black suggested we call a "
            "market efficient if the price is within a factor of two of value. <bookmark mark='a'/> Who that noise "
            "comes from, and who profits from it, is chapter eleven."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(tie))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nagel(self, n):
        setup = VGroup(
            label(r"A simulated market where prices are efficient by construction:", font_size=26),
            label(rf"{n['N']} stocks, each with {n['J']} characteristics; payoffs depend on them through "
                  r"weights $\theta$ nobody knows", font_size=23, color=GREY_A),
            label(r"investors learn $\theta$ from the payoffs they see, by Bayes' rule, and price every stock at its "
                  r"expected payoff", font_size=23, color=GREY_A),
            label(rf"afterwards, an econometrician regresses returns on the characteristics, {n['T']} periods, "
                  rf"{n['sims']} markets", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.35)
        if setup.width > 13.2:
            setup.scale_to_fit_width(13.2)
        p = np.asarray(n["p_in"])
        oos = np.asarray(n["r2_oos"])
        e1 = np.linspace(0, 1, 21)
        h1 = np.histogram(p, e1)[0] / len(p)
        g1 = axes([0, 1], [0, 0.7], x_length=5.4, y_length=3.2, xlabel=r"in-sample $p$-value",
                  ylabel=r"share of markets", xticks=[0, 0.25, 0.5, 0.75, 1], xfmt=lambda v: f"{v:g}", yticks=[0, 0.3, 0.6],
                  font_size=18)
        e2 = np.linspace(-0.12, 0.02, 15)
        h2 = np.histogram(np.clip(oos, -0.119, 0.019), e2)[0] / len(oos)
        g2 = axes([-0.12, 0.02], [0, 0.5], x_length=5.4, y_length=3.2, xlabel=r"out-of-sample $R^2$",
                  ylabel=r"share of markets", xticks=[-0.1, -0.05, 0], xfmt=lambda v: f"{100 * v:.0f}\\%",
                  yticks=[0, 0.25, 0.5], font_size=18)
        pair = VGroup(g1, g2).arrange(RIGHT, buff=1.0).next_to(setup, DOWN, buff=0.5)
        bb1 = hist_bars(g1.ax, e1, h1, LOSS)
        fl = DashedLine(g1.ax.c2p(0, 0.05), g1.ax.c2p(1, 0.05), color=GAUSS, stroke_width=2)
        fll = label(r"if there were nothing to find", font_size=18, color=GAUSS).next_to(g1.ax.c2p(1, 0.05), UP, buff=0.05)
        fll.align_to(g1.ax.c2p(1, 0), RIGHT)
        bb2 = hist_bars(g2.ax, e2, h2, REAL)
        zl = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(0, 0.5), color=GAIN, stroke_width=2.5)
        res = VGroup(
            MathTex(rf"\text{{rejects at the 5\% level in}}\ {100 * n['reject']:.0f}\%\ \text{{of markets}}",
                    font_size=30, color=LOSS),
            MathTex(rf"\text{{median out-of-sample}}\ R^2 = {100 * n['median_r2_oos']:.1f}\%;\ \text{{positive in}}\ "
                    rf"{100 * n['oos_positive']:.0f}\%", font_size=30, color=REAL),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)
        if res.width > 13.2:
            res.scale_to_fit_width(13.2)
        cite_ = note(r"after Martin and Nagel (2022), ``Market efficiency in the age of big data'', \textit{JFE}",
                     font_size=18).to_corner(UR, buff=0.15)
        with self.voiceover(
            "One more turn, from the frontier. In 2022 Ian Martin and Stefan Nagel asked what efficiency means when "
            "investors face thousands of possible predictors, as they do today. Here is their argument as a "
            f"simulation. {n['N']} stocks, each with {n['J']} characteristics. Payoffs depend on the "
            "characteristics through weights nobody knows. Investors learn the weights from what they see, by "
            "Bayes' rule, and price every stock at its expected payoff given everything known: efficient by "
            "construction. <bookmark mark='a'/> Afterwards an econometrician regresses the realized returns on the "
            "characteristics and tests whether they predicted anything. If markets are efficient, the test should "
            "reject one time in twenty. It rejects in "
            f"{100 * n['reject']:.0f} percent of these markets. <bookmark mark='b'/> The predictability is real in "
            "hindsight: it is the investors' learning, visible only after the fact. Now test properly, out of "
            "sample: at each date, use only what was known before it. The out-of-sample R squared is negative in "
            f"every one of {n['sims']} markets. <bookmark mark='c'/> In-sample predictability is not evidence of an "
            "inefficient market, and only out-of-sample tests keep their meaning. That is why the House will seal "
            "its data in an envelope, in chapter sixteen."
            " Next: the two worlds every price lives in."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(s) for s in setup], lag_ratio=0.6, run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(g1), Create(fl), FadeIn(fll))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb1], lag_ratio=0.05))
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(zl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb2], lag_ratio=0.05))
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()
