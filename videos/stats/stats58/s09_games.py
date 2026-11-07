from __future__ import annotations

from videos.stats.stats58.common import *  # noqa: F403


class Games(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Game-theoretic probability: Shafer and Vovk's foundation, in which probability "
                       "itself is defined by betting.", 8, r"Game-theoretic probability", r"Probability as a game", lit=(1939,))
        self.protocol()
        self.upper()
        self.lln()
        self.forecaster()
        self.forecaster_worked()
        self.evidence()
        self.scale()

    def protocol(self):
        heading = label('The forecasting game', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Glenn Shafer and Vladimir Vovk rebuilt probability as a game between three "
            "players. At each round, Forecaster announces prices for bets on the next outcome. <bookmark mark='b'/> "
            "Skeptic chooses a bet at those prices, and may not risk more than she has. <bookmark mark='c'/> "
            "Reality announces the outcome, and Skeptic's capital changes accordingly. <bookmark mark='d'/> No "
            'probability distribution is assumed anywhere: Reality may play however it likes, adversarially even. '
            'Probability is what Skeptic cannot profit from.'
        ),
            [(r"\text{Forecaster}", r":", r"\text{prices } p_t \text{ for bets on } Y_t", 38),
             (r"\text{Skeptic}", r":", r"\text{a bet } \lambda_t, \ \text{never risking more than } K_{t-1}", 38),
             (r"\text{Reality}", r":", r"Y_t; \ \ K_t = K_{t-1}\{1 + \lambda_t(Y_t - p_t)\}", 38),
             (r"\text{no model}", r":", r"\text{Reality may play adversarially}", 38)],
            [r"Shafer \& Vovk (2001, 2019)", r"the gambler", r"the world", r"probability without measure"],
            colors=[(2, WEALTHC)])

    def upper(self):
        heading = label('Upper probability in a complete protocol', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Upper probability is the least starting capital needed for a nonnegative strategy "
            "to cover an event indicator. <bookmark mark='b'/> In a complete finite-horizon binary forecasting "
            'game, backward replication makes this price equal to the probability from the announced conditional '
            'forecasts. More general infinite-horizon equalities require additional assumptions. <bookmark '
            "mark='c'/> A game-null event admits nonnegative strategies that become arbitrarily rich on it; a "
            "savings construction can turn repeated gains into unbounded banked capital. <bookmark mark='d'/> This "
            'gives a pathwise language for almost-sure laws. A frequentist probability guarantee still refers to a '
            'probability model for which the bets are conditionally fair.'
        ),
            [(r"\overline P(E)", r"=", r"\inf\{K_0: \text{a strategy ends with } K \ge 1_E, \ K \ge 0\}", 36),
             (r"\text{with a model}", r":", r"\overline P=P \text{ for complete finite binary protocols}", 38),
             (r"\overline P(E) = 0", r"\iff", r"\text{Skeptic gets infinitely rich on } E", 38),
             (r"\text{Ville (1939)}", r":", r"\text{laws of probability} = \text{no free lunch}", 38)],
            [r"a price, \ not a measure", r"consistency", r"null events", r"Ville's thesis"],
            colors=[(0, WEALTHC), (3, CSC)])

    def lln(self):
        heading = label('A countable mixture proves the strong law', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Suppose binary forecasts are always one-half, but the running frequency fails to "
            "converge to one-half. <bookmark mark='b'/> Divide capital among a countable collection of gamblers "
            'with fixed small positive and negative rational stakes, all chosen before the observations. <bookmark '
            "mark='c'/> The logarithm of each account is bounded below by its stake times the centered sum minus a "
            'quadratic stake cost. If a nonzero excess frequency recurs, one correctly signed small stake has '
            "arbitrarily large capital along that subsequence. <bookmark mark='d'/> A standard banking or savings "
            'strategy locks in these recurring gains. Thus a single combined nonnegative strategy can become rich '
            'whenever the strong law fails. An informal rule that simply bets on whichever side was recently '
            'winning is not the proof.'
        ),
            [(r"\text{suppose}", r":", r"\bar Y_t \not\to \tfrac12", 40),
             (r"\text{Skeptic}", r":", r"\text{mix fixed rational stakes } \lambda\in[-1,1]", 36),
             (r"\log K_t^\lambda", r"\ge", r"\lambda t(\bar Y_t-\tfrac12)-\lambda^2 t/4", 38),
             (r"\text{so}", r":", r"\bar Y_t \to \tfrac12 \text{, \ or Skeptic gets rich}", 38)],
            [r"a fair coin", r"Kelly, \ small", r"gain beats variance", r"Part 6's law, \ by betting"],
            colors=[(2, WEALTHC), (3, CSC)])

    def forecaster(self):
        heading = label('Conditional forecast validity', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> For a probabilistic test of a weather forecaster, state the null precisely: "
            'conditional on the full observed past, the next rain probability equals the announced forecast. '
            "Empirical calibration alone is weaker. <bookmark mark='b'/> Choose a nonnegative predictable betting "
            "factor using that forecast before rain is observed. <bookmark mark='c'/> Under this conditional "
            "forecasting null the capital is a test martingale. <bookmark mark='d'/> Ville then bounds the chance "
            'of ever reaching one hundred by one percent under that null. Capital can be computed for any weather '
            'sequence, but the probability statement depends on the conditional null being true.'
        ),
            [(r"\text{forecast}", r":", r"p_t=P(Y_t=1\mid\mathcal F_{t-1})", 38),
             (r"K_t", r"=", r"\prod_{s \le t}\{1 + \lambda_s(Y_s - p_s)\}", 38),
             (r"\text{if the forecasts are right}", r":", r"K_t \text{ is a test martingale}", 38),
             (r"K_t \ge 100", r":", r"P_0(\text{ever crosses }100)\le 1\%", 38)],
            [r"the forecaster's claim", r"Skeptic's wealth", r"the null", r"Ville, \ again"],
            colors=[(1, WEALTHC), (3, FIXEDC)])

    def forecaster_worked(self):
        heading = label('Log drift approximates the crossing time', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A forecaster always announces thirty percent. For a worked alternative, suppose "
            "rain is IID with probability forty percent. <bookmark mark='b'/> A stake of one-half multiplies "
            "capital by one point three five on rain, and point eight five otherwise. <bookmark mark='c'/> Expected "
            'log growth is point four log one point three five plus point six log point eight five, about point '
            "zero two two five per day. <bookmark mark='d'/> Dividing log one hundred by this drift gives about two "
            'hundred and four days. This is a drift approximation, not a guaranteed crossing time. Overshoot and '
            'random fluctuations matter: under this IID alternative the expected crossing time lies between roughly '
            'two hundred and four and two hundred and eighteen days.'
        ),
            [(r"p_t = 0.3, \ \text{truth } 0.4", r":", r"\lambda = \tfrac12", 38),
             (r"\text{rain}", r":", r"\times 1.35; \ \ \text{dry: } \times 0.85", 38),
             (r"\text{growth}", r"=", r"0.4\log 1.35 + 0.6\log 0.85 \approx 0.0225", 38),
             (r"K_t = 100", r":", r"t \approx \log 100 / 0.0225 \approx 205 \text{ days}", 38)],
            [r"miscalibrated", r"the two outcomes", r"Kelly's growth", r"drift approximation; random crossing time"],
            colors=[(2, WEALTHC), (3, CSC)])

    def evidence(self):
        heading = label('Evidence depends on conditional fairness', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> An e-value measures the payoff of a test bet, rather than the probability that a "
            "hypothesis is true. <bookmark mark='b'/> A sequentially valid betting construction can allow "
            'data-dependent stopping without a preplanned sample size. Its null-model or conditional-forecast '
            "assumptions remain essential. <bookmark mark='c'/> Evidence multiplies when the next factor has "
            'conditional null expectation at most one. Merely choosing a bet before seeing its outcome does not '
            "establish that fairness. <bookmark mark='d'/> Shafer advocates this betting interpretation as a useful "
            'way for scientists to communicate evidence. That philosophical interpretation is separate from the '
            'mathematical assumptions behind the guarantee.'
        ),
            [(r"\text{an e-value}", r":", r"\text{evidence, \ in units of money}", 38),
             (r"\text{not needed}", r":", r"\text{a planned } n; \ \text{conditional null assumptions still needed}", 36),
             (r"\text{it compounds}", r":", r"\text{the next study's bet multiplies in}", 38),
             (r"\text{Shafer}", r":", r"\text{closer to how scientists reason}", 38)],
            [r"a different currency", r"freedoms", r"chapter 4's product", r"a philosophical claim"],
            colors=[(0, WEALTHC)])

    def scale(self):
        heading = label('A descriptive evidence scale', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A rough scale, to read e-values. Below one: the bet lost, no evidence against the "
            "null. <bookmark mark='b'/> Around ten: worth noticing; a p-value of half a percent, calibrated, is "
            "worth about this. <bookmark mark='c'/> Around a hundred: strong, as CAST's evidence of harm was by the "
            "end. <bookmark mark='d'/> Beyond a thousand: very strong. This resembles Jeffreys's scale for Bayes "
            'factors in Part fifteen, and for simple hypotheses the likelihood ratio is both a Bayes factor and an '
            'e-value.'
        ),
            [(r"E < 1", r":", r"\text{the bet lost}", 40),
             (r"E \approx 10", r":", r"\text{worth noticing}", 40),
             (r"E \approx 100", r":", r"\text{strong}", 40),
             (r"E > 1{,}000", r":", r"\text{very strong}", 40)],
            [r"nothing against $H_0$", r"one descriptive scale; \ calibrator choice matters", r"CAST working label-model wealth: 333", r"Jeffreys's scale, \ Part 15"],
            colors=[(2, WEALTHC), (3, CSC)])
