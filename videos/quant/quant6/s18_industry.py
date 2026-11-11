from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card


class Industry(VoiceoverScene):
    def construct(self):
        la = load("lookahead")
        self.card()
        self.fsquared(la)
        self.regulator()
        self.firms()
        self.defences()

    def card(self):
        c = chapter_card(17, r"How research desks avoid fooling themselves", r"What do firms and regulators actually do?",
                         part=PART)
        with self.voiceover("Chapter seventeen. How research desks avoid fooling themselves."):
            show_card(self, c)
        self.play(FadeOut(c))

    def fsquared(self, la):
        cc = crisis_card(r"22 December 2014", r"F-Squared Investments", (
            r"The SEC's press release: F-Squared advertised its AlphaSector strategy's track record as ``not "
            r"backtested'', for years before the algorithm existed; an analyst had applied the buy and sell signals "
            r"to ``the week preceding'' the price changes they were based on, which ``inflated the results by "
            r"approximately 350 percent''. F-Squared admitted wrongdoing and agreed to pay \$35 million. Its "
            r"co-founder was charged separately; those charges were allegations."),
            stats=[(r"\$35\text{m}", r"\$30m disgorgement, \$5m penalty"), (r"\approx 350\%", r"inflation of the "
                                                                                         r"results, per the SEC")],
            width=6.4, font_size=21).to_corner(UL, buff=0.3)
        H, E, B = np.asarray(la["honest"]), np.asarray(la["early"]), np.asarray(la["hold"])
        n = len(H)
        g = axes([0, n], [0, np.log10(max(E.max(), 2)) + 0.1], x_length=5.6, y_length=3.6, xlabel=r"weeks, 2001--2008",
                 ylabel=r"growth of \$1 (log scale)", xticks=[0, n], yticks=[0, np.log10(2), 1],
                 yfmt=lambda u: f"{10 ** u:.0f}", font_size=14).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.6)
        ax = g.ax
        k = ValueTracker(2)
        lines = always_redraw(lambda: VGroup(
            curve(ax, np.arange(int(k.get_value())), np.log10(B[:int(k.get_value())]), GREY_B, stroke_width=2),
            curve(ax, np.arange(int(k.get_value())), np.log10(H[:int(k.get_value())]), GOOD, stroke_width=3),
            curve(ax, np.arange(int(k.get_value())), np.log10(E[:int(k.get_value())]), BAD, stroke_width=3)))
        leg = legend([(GOOD, rf"honest: {100 * la['ann_honest']:.0f}\% a year"),
                      (BAD, rf"signal one week early: {100 * la['ann_early']:.0f}\%"),
                      (GREY_B, rf"hold all ten: {100 * la['ann_hold']:.0f}\%")], font_size=17).next_to(g, UP, buff=0.15)
        tag = label(r"illustrative: a toy rotation on French's daily size deciles, not F-Squared's rule", font_size=16,
                    color=GREY_C).next_to(g, DOWN, buff=0.12)
        with self.voiceover(
            "This part's crisis file is a backtest. On the twenty-second of December 2014 the SEC announced that "
            "F-Squared Investments had advertised its AlphaSector track record as not backtested, for years before the "
            "algorithm existed; and, in the SEC's words, an analyst applied the signals to the week preceding the price "
            "changes they were based on, which inflated the results by approximately three hundred and fifty percent. "
            "F-Squared admitted wrongdoing and agreed to pay thirty-five million dollars; its co-founder was charged "
            "separately, allegations at the time. <bookmark mark='a'/> What can one week of look-ahead do? A toy on "
            "French's daily size portfolios, 2001 to 2008: each week, hold those that rose over the past four weeks. "
            f"Honestly, {100 * la['ann_honest']:.0f} percent a year. With the signal one week early, including the very "
            f"week it trades, {100 * la['ann_early']:.0f} percent. <bookmark mark='b'/> It harvests the move the signal was "
            "built from."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(leg), FadeIn(tag))
            self.add(lines)
            self.play(k.animate.set_value(n), run_time=vo.until("b"), rate_func=linear)
        lines.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def regulator(self):
        rule = firm_card(r"The SEC's Marketing Rule", (
            r"Rule 206(4)-1, adopted in December 2020: an adviser that shows hypothetical performance must have "
            r"policies and procedures making it relevant to the audience. On 11 September 2023 the SEC charged nine "
            r"advisers who ``advertised hypothetical performance to mass audiences on their websites without having "
            r"the required policies and procedures''; without admitting or denying the findings, they settled."),
            numbers=[(r"9", r"advisers"), (r"\$850{,}000", r"combined penalties")],
            source=r"SEC press release 2023-173", width=11.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "The regulator's answer: the SEC's Marketing Rule, adopted in December 2020, requires policies and "
            "procedures before an adviser shows hypothetical performance. <bookmark mark='a'/> In September 2023 nine "
            "advisers were charged with advertising it to mass audiences on their websites without them; without "
            "admitting or denying the findings, they settled, for eight hundred and fifty thousand dollars combined."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.play(Indicate(rule, color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        man = firm_card(r"Man Group", (
            r"publishes Campbell Harvey and Yan Liu's ``Backtesting'' (\textit{JPM} 2015): the common rule of halving "
            r"a backtested Sharpe ratio is a mistake; the haircut should come from a multiple-testing adjustment, and "
            r"it is nonlinear, mild for the best and severe for the marginal."), source=r"man.com/insights/backtesting",
            width=6.2, font_size=19)
        aqr = firm_card(r"AQR", (
            r"Jensen, Kelly and Pedersen (\textit{JF} 2023; Kelly and Pedersen at AQR): 153 factors in 93 countries; "
            r"82\% have significant CAPM alphas (Hou, Xue and Zhang: 35\%), 76\% after a multiple-testing correction, "
            r"and a Bayesian hierarchical model shrinks them together. Ilmanen et al.\ (2021): a century of factor "
            r"data, the premia hold out of sample, timing them mostly does not survive costs."),
            source=r"JF 78(5); JIM 19(4)", width=6.2, font_size=19)
        ra = firm_card(r"Research Affiliates", (
            r"Arnott, Harvey and Markowitz, ``A Backtesting Protocol in the Era of Machine Learning'' (\textit{JFDS} "
            r"2019): state the hypothesis first, report every trial, keep the data honest, reward research rather "
            r"than results."), width=6.2, font_size=19)
        prof = firm_card(r"The profession's own audit", (
            r"Menkveld et al.\ (\textit{JF} 2024): 164 teams, the same data and questions; their answers spread far "
            r"more than their standard errors implied (``non-standard errors''). P\'erignon et al.\ "
            r"(\textit{RFS} 2024): re-running 168 teams' own code on their own data reproduced the exact results "
            r"52\% of the time."), width=6.2, font_size=19)
        grid = VGroup(VGroup(man, aqr).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(ra, prof).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.6:
            grid.scale_to_fit_height(7.6)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "What do the firms say, on the record? Man Group publishes Campbell Harvey and Yan Liu's backtesting paper: "
            "halving a backtested Sharpe ratio is a mistake; the haircut should come from the number of trials, mild for "
            "the best, severe for the marginal. <bookmark mark='a'/> At AQR, Bryan Kelly and Lasse Pedersen, with Theis "
            "Jensen, found that eighty-two percent of a hundred and fifty-three factors have significant CAPM alphas, "
            "seventy-six after a multiple-testing correction, against an earlier thirty-five percent replication rate; "
            "their Bayesian model is chapter twelve at industrial scale. Antti Ilmanen and colleagues found factor "
            "premia held over a century of data, while timing them mostly did not survive costs. <bookmark mark='b'/> "
            "Research Affiliates' Robert Arnott, with Harvey and Harry Markowitz, wrote a backtesting protocol: "
            "hypothesis first, every trial reported. <bookmark mark='c'/> And the profession audited itself: in 2024 a "
            "hundred and sixty-four teams given the same data disagreed far more than their standard errors implied, "
            "and re-running a hundred and sixty-eight teams' own code reproduced their exact results fifty-two percent "
            "of the time."
        ) as vo:
            self.play(FadeIn(man))
            vo.wait_until("a")
            self.play(FadeIn(aqr))
            vo.wait_until("b")
            self.play(FadeIn(ra))
            vo.wait_until("c")
            self.play(FadeIn(prof))
        self.wait(0.4)
        self.clear_scene()

    def defences(self):
        chart = house_chart(PART, lit=("data",)).scale(0.55).to_edge(UP, buff=0.2)
        rows = [
            (r"a hypothesis written before the data are opened", r"the registry: code hash and parameters"),
            (r"every trial counted, haircuts from the count", r"the trial counter"),
            (r"a hold-out nobody may look at", r"the sealed envelope"),
            (r"standard errors that respect the sampling", r"HAC, clustering, bootstraps by default"),
            (r"results that rerun from one command", r"checksummed data, seeded compute"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=21, color=GREY_A), MathTex(r"\longrightarrow", color=GREY_C),
                              label(b, font_size=21, color=QC.HOUSE)).arrange(RIGHT, buff=0.3) for a, b in rows])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r_ in tab:
            r_[1].set_x(0.6)
            r_[0].next_to(r_[1], LEFT, buff=0.3)
            r_[2].next_to(r_[1], RIGHT, buff=0.3)
        tab.next_to(chart, DOWN, buff=0.4)
        q = predict(r"A one-week look-ahead on a weekly rotation: does it add a little or a lot?", width=9.0).to_edge(
            DOWN, buff=0.15)
        with self.voiceover(
            "Each practice maps onto the House. A hypothesis written down first: the registry, with the code's hash. "
            "Every trial counted: the trial counter, whose count sets the haircut. An untouched hold-out: the sealed "
            "envelope. Honest standard errors, respecting how the data were sampled: this part's module, by default. "
            "Results that rerun from one command: checksummed data and seeded computations. <bookmark mark='a'/> And "
            "this chapter's question: a week of look-ahead adds a lot."
            " Last, the frontier."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.5, run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()
