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
        self.lad_voiceover(
            "<bookmark mark='a'/> Glenn Shafer and Vladimir Vovk rebuilt probability as a game between three players. At each "
            "round, Forecaster announces prices for bets on the next outcome. <bookmark mark='b'/> Skeptic chooses a bet at "
            "those prices, and may not risk more than she has. <bookmark mark='c'/> Reality announces the outcome, and "
            "Skeptic's capital changes accordingly. <bookmark mark='d'/> No probability distribution is assumed anywhere: "
            "Reality may play however it likes, adversarially even. Probability is what Skeptic cannot profit from.",
            [(r"\text{Forecaster}", r":", r"\text{prices } p_t \text{ for bets on } Y_t", 38),
             (r"\text{Skeptic}", r":", r"\text{a bet } \lambda_t, \ \text{never risking more than } K_{t-1}", 38),
             (r"\text{Reality}", r":", r"Y_t; \ \ K_t = K_{t-1}\{1 + \lambda_t(Y_t - p_t)\}", 38),
             (r"\text{no model}", r":", r"\text{Reality may play adversarially}", 38)],
            [r"Shafer \& Vovk (2001, 2019)", r"the gambler", r"the world", r"probability without measure"],
            colors=[(2, WEALTHC)])

    def upper(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Then define the upper probability of an event as the smallest starting capital with which "
            "Skeptic can be sure to end with at least one if the event happens, and never go into debt. <bookmark mark='b'/> "
            "When Forecaster's prices come from a probability distribution, this agrees with ordinary probability for the "
            "events that matter. <bookmark mark='c'/> An event of upper probability zero is one on which Skeptic can become "
            "infinitely rich from a unit stake. <bookmark mark='d'/> That is Ville's idea from his 1939 thesis: almost-sure "
            "laws are statements that no betting strategy can make you rich, and Ville's inequality is the finite version.",
            [(r"\overline P(E)", r"=", r"\inf\{K_0: \text{a strategy ends with } K \ge 1_E, \ K \ge 0\}", 36),
             (r"\text{with a model}", r":", r"\overline P = P \text{ on the events that matter}", 38),
             (r"\overline P(E) = 0", r"\iff", r"\text{Skeptic gets infinitely rich on } E", 38),
             (r"\text{Ville (1939)}", r":", r"\text{laws of probability} = \text{no free lunch}", 38)],
            [r"a price, \ not a measure", r"consistency", r"null events", r"Ville's thesis"],
            colors=[(0, WEALTHC), (3, CSC)])

    def lln(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The law of large numbers, proved by betting. Suppose the forecasts are fair coins, and the "
            "running frequency of heads does not settle at a half. <bookmark mark='b'/> Then Skeptic, betting a small fixed "
            "fraction on whichever side has been winning, multiplies her capital without bound, <bookmark mark='c'/> because "
            "each bet earns about epsilon times the excess frequency and loses only epsilon squared in variance. <bookmark "
            "mark='d'/> So the frequency must converge, unless Reality is willing to let Skeptic get rich. The same game "
            "yields the law of the iterated logarithm and the central limit theorem.",
            [(r"\text{suppose}", r":", r"\bar Y_t \not\to \tfrac12", 40),
             (r"\text{Skeptic}", r":", r"\text{bets a fraction } \varepsilon \text{ on the side that has been winning}", 36),
             (r"\log K_t", r"\approx", r"\varepsilon\,t\,|\bar Y_t - \tfrac12| - \varepsilon^2 t/2 \to \infty", 38),
             (r"\text{so}", r":", r"\bar Y_t \to \tfrac12 \text{, \ or Skeptic gets rich}", 38)],
            [r"a fair coin", r"Kelly, \ small", r"gain beats variance", r"Part 6's law, \ by betting"],
            colors=[(2, WEALTHC), (3, CSC)])

    def forecaster(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The practical use: testing a forecaster with no model of the weather. Each day the "
            "forecaster says the chance of rain is p t. <bookmark mark='b'/> Skeptic bets lambda t on rain, at those odds: "
            "her capital is multiplied by one plus lambda t times rain minus p t. <bookmark mark='c'/> If the forecasts are "
            "calibrated in the strong sense, the forecaster's own probabilities, that capital is a test martingale. <bookmark "
            "mark='d'/> So if it reaches one hundred, the forecaster is discredited at level one percent, whatever the "
            "weather really does, and whenever Skeptic chose to look.",
            [(r"\text{forecast}", r":", r"p_t = P(\text{rain tomorrow})", 38),
             (r"K_t", r"=", r"\prod_{s \le t}\{1 + \lambda_s(Y_s - p_s)\}", 38),
             (r"\text{if the forecasts are right}", r":", r"K_t \text{ is a test martingale}", 38),
             (r"K_t \ge 100", r":", r"\text{discredited at } 1\%, \ \text{any weather}", 38)],
            [r"the forecaster's claim", r"Skeptic's wealth", r"the null", r"Ville, \ again"],
            colors=[(1, WEALTHC), (3, FIXEDC)])

    def forecaster_worked(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A worked case. A forecaster always says thirty percent; in truth it rains on forty percent "
            "of days. <bookmark mark='b'/> Skeptic bets lambda a half on rain each day. On a rainy day her capital is "
            "multiplied by one plus a half times point seven, one point three five; on a dry day by one minus a half times "
            "point three, point eight five. <bookmark mark='c'/> Her expected log growth per day is point four log one point "
            "three five plus point six log point eight five, about point zero two two five. <bookmark mark='d'/> So her "
            "capital reaches one hundred, log one hundred over that growth, after roughly two hundred days: a season "
            "discredits the forecaster.",
            [(r"p_t = 0.3, \ \text{truth } 0.4", r":", r"\lambda = \tfrac12", 38),
             (r"\text{rain}", r":", r"\times 1.35; \ \ \text{dry: } \times 0.85", 38),
             (r"\text{growth}", r"=", r"0.4\log 1.35 + 0.6\log 0.85 \approx 0.0225", 38),
             (r"K_t = 100", r":", r"t \approx \log 100 / 0.0225 \approx 205 \text{ days}", 38)],
            [r"miscalibrated", r"the two outcomes", r"Kelly's growth", r"a season"],
            colors=[(2, WEALTHC), (3, CSC)])

    def evidence(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In this view an e-value is not a probability but a measure of evidence with units: money. "
            "<bookmark mark='b'/> It does not need a sample size fixed in advance, or a model of how the data would have "
            "turned out otherwise, or a stopping rule. <bookmark mark='c'/> And it compounds: evidence from the next study "
            "multiplies in, as long as each bet is made before the data it is applied to. <bookmark mark='d'/> Shafer argues "
            "this is closer to how scientists actually reason than tail probabilities under hypothetical repetitions.",
            [(r"\text{an e-value}", r":", r"\text{evidence, \ in units of money}", 38),
             (r"\text{not needed}", r":", r"\text{a planned } n, \ \text{a stopping rule, \ counterfactual samples}", 36),
             (r"\text{it compounds}", r":", r"\text{the next study's bet multiplies in}", 38),
             (r"\text{Shafer}", r":", r"\text{closer to how scientists reason}", 38)],
            [r"a different currency", r"freedoms", r"chapter 4's product", r"a philosophical claim"],
            colors=[(0, WEALTHC)])

    def scale(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A rough scale, to read e-values. Below one: the bet lost, no evidence against the null. "
            "<bookmark mark='b'/> Around ten: worth noticing; a p-value of half a percent, calibrated, is worth about this. "
            "<bookmark mark='c'/> Around a hundred: strong, as CAST's evidence of harm was by the end. <bookmark mark='d'/> "
            "Beyond a thousand: very strong. This resembles Jeffreys's scale for Bayes factors in Part fifteen, and "
            "for simple hypotheses the likelihood ratio is both a Bayes factor and an e-value.",
            [(r"E < 1", r":", r"\text{the bet lost}", 40),
             (r"E \approx 10", r":", r"\text{worth noticing}", 40),
             (r"E \approx 100", r":", r"\text{strong}", 40),
             (r"E > 1{,}000", r":", r"\text{very strong}", 40)],
            [r"nothing against $H_0$", r"like $p \approx 0.005$, \ calibrated", r"CAST ended at 333", r"Jeffreys's scale, \ Part 15"],
            colors=[(2, WEALTHC), (3, CSC)])
