from __future__ import annotations

from videos.stats.stats26.common import *  # noqa: F403


class Argument(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.coherence()
        self.likelihood_principle()
        self.objections()
        self.calibrated()
        self.schools_differ()

    def card(self):
        card = chapter_card(12, r"The argument, \ honestly", r"Two hundred years of disagreement", lit=(1763, 1990), part=PART)
        with self.voiceover("Chapter twelve. The argument, honestly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        items = [
            (r"1763--1812: \ Bayes and Laplace; \ inverse probability is simply probability", PATH),
            (r"1920s--30s: \ Fisher calls it `founded upon an error'; \ Neyman and Pearson build frequentism", RES),
            (r"1939--54: \ Jeffreys keeps it alive; \ de Finetti and Savage ground it in coherence", PRIOR),
            (r"1960s--80s: \ a minority view; \ hard integrals limit it to conjugate models", GREY_A),
            (r"1990: \ Gelfand \& Smith bring the Gibbs sampler: \ any model can be fitted", SHRUNK),
            (r"today: \ both schools in daily use, \ often by the same people", HIT),
        ]
        rows = fit_rows(VGroup(*[label(t, font_size=24, color=c) for t, c in items]), 12.6, 0.45, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A short history, as Sharon McGrayne tells it in The Theory That Would Not Die. For Bayes "
            "and Laplace, reasoning from data to causes was simply probability. <bookmark mark='b'/> In the 1920s Fisher "
            "dismissed inverse probability as founded upon an error, and Neyman and Pearson built a theory of tests and "
            "intervals that needed no prior. <bookmark mark='c'/> Harold Jeffreys kept the Bayesian approach alive, and "
            "Bruno de Finetti and Leonard Savage rebuilt it on coherence. <bookmark mark='d'/> For decades it remained a "
            "minority view, partly for a practical reason: outside conjugate models, nobody could compute the integrals. "
            "<bookmark mark='e'/> In 1990 Alan Gelfand and Adrian Smith showed that the Gibbs sampler could fit almost any "
            "model, Part 27's story, and Bayesian methods spread fast. <bookmark mark='f'/> Today both schools are in daily "
            "use, often by the same people."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def coherence(self):
        rows = [
            cmath(r"\text{Dutch book}", r":", r"\text{incoherent odds } \Rightarrow \text{ a sure loss}", font_size=30),
            cmath(r"\text{Cox (1946)}", r":", r"\text{consistent plausibility } \Rightarrow \text{ the probability rules}", font_size=28),
            cmath(r"\text{Savage (1954)}", r":", r"\text{coherent preferences } \Rightarrow \text{ utility} \times \text{probability}", font_size=28),
            cmath(r"\text{conclusion}", r":", r"\text{update by Bayes's rule, \ or be exploitable}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"de Finetti (1937)"), why(r"plausible reasoning, \ axiomatized"), why(r"chapter nine"),
                why(r"the Bayesian's strongest card")]
        with self.voiceover(
            "<bookmark mark='a'/> The Bayesian case rests on coherence. De Finetti showed that if your betting odds break "
            "the rules of probability, someone can arrange bets you'll accept that lose whatever happens, a Dutch book. "
            "<bookmark mark='b'/> Richard Cox showed in 1946 that any consistent way of grading plausibility must obey the "
            "rules of probability. <bookmark mark='c'/> Savage showed coherent preferences imply a utility and a "
            "probability. <bookmark mark='d'/> So if your beliefs are to be coherent, they must be updated by Bayes's rule."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def objections(self):
        rows = fit_rows(VGroup(
            label(r"whose prior? \ two analysts, \ two posteriors", font_size=24, color=RES),
            label(r"coherence is about one person's beliefs, \ not about being right", font_size=24, color=RES),
            label(r"a model that is wrong is updated coherently to wrong answers", font_size=24, color=RES),
            label(r"replies: \ priors in the open, \ sensitivity, \ checking, \ chapters 3, \ 10, \ 11", font_size=24, color=SHRUNK),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The objections are serious too. Whose prior? Two analysts with different priors reach "
            "different conclusions from the same data. <bookmark mark='b'/> Coherence guarantees consistency within one "
            "person's beliefs; it doesn't make them right. <bookmark mark='c'/> And a wrong model is updated, perfectly "
            "coherently, towards wrong answers: the Poisson model for doctor visits was coherent. <bookmark mark='d'/> The "
            "modern replies are this part's practical chapters: priors stated openly, sensitivity analysis, and model "
            "checking, which steps outside pure coherence."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def calibrated(self):
        rows = [
            cmath(r"\text{Rubin (1984)}", r":", r"\text{Bayesianly justifiable, \ frequency calculations}", font_size=28),
            cmath(r"\text{Box (1980)}", r":", r"\text{Bayes to estimate, \ frequency to criticize}", font_size=28),
            cmath(r"\text{Little (2006)}", r":", r"\text{calibrated Bayes}", font_size=30),
            cmath(r"\text{the Board}", r":", r"\text{judges credible intervals by coverage too}", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"models built Bayesianly, \ judged by repeated use"), why(r"posterior inside, \ checks outside"),
                why(r"a working compromise"), why(r"chapter eleven's rows")]
        with self.voiceover(
            "<bookmark mark='a'/> A working compromise has grown up. Donald Rubin argued in 1984 for Bayesian answers whose "
            "behaviour in repeated use is checked by frequency calculations. <bookmark mark='b'/> George Box put it as "
            "Bayes for estimation within a model, frequentist reasoning for criticizing the model. <bookmark mark='c'/> "
            "Roderick Little calls it calibrated Bayes. <bookmark mark='d'/> It is what this series' Coverage Board does when "
            "it holds credible intervals to the standard of coverage."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def schools_differ(self):
        hdr = [r"", r"\textbf{frequentist}", r"\textbf{Bayesian}"]
        body = [[r"probability is", r"long-run frequency", r"degree of belief"],
                [r"parameters are", r"fixed, \ unknown", r"uncertain: \ given distributions"],
                [r"the answer", r"a procedure with guarantees", r"a posterior for this data set"],
                [r"strongest when", r"guarantees matter: \ trials, \ regulation", r"structure, \ few data, \ decisions"],
                [r"weakest when", r"many related parameters, \ no repetition", r"priors contested, \ models wrong"]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.9, row_buff=0.32, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[0].set_color(GREY_A)
            r[1].set_color(RAW)
            r[2].set_color(SHRUNK)
        tb.move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Where the schools differ, side by side. To a frequentist, probability is long-run "
            "frequency and parameters are fixed; to a Bayesian, probability is a degree of belief and parameters are "
            "uncertain. <bookmark mark='b'/> The frequentist delivers a procedure with guarantees over repetitions; the "
            "Bayesian, a posterior for the data in hand. <bookmark mark='c'/> Each is strongest where the other is weak: "
            "guarantees matter in regulated trials, while structure, small data and decisions favour Bayes. This series "
            "uses both, and the Board keeps both honest."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(tb[2]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3]))
            vo.wait_until("c")
            self.play(FadeIn(tb[4]), FadeIn(tb[5]))
        self.wait(1.0)
        self.clear_scene()

    def likelihood_principle(self):
        rows = [
            cmath(r"\text{data}", r":", r"9 \text{ heads, } 3 \text{ tails; \ } H_0: p = \tfrac12 \text{ vs } p > \tfrac12", font_size=30),
            cmath(r"\text{planned 12 tosses}", r":", r"P(\ge 9 \text{ heads}) = 0.073", font_size=30),
            cmath(r"\text{planned: \ stop at the 3rd tail}", r":", r"P(\ge 9 \text{ heads first}) = 0.033", font_size=30),
            cmath(r"\text{likelihood}", r":", r"p^9(1 - p)^3 \text{ both ways: \ the same posterior}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Lindley \& Phillips (1976)"), why(r"binomial: \ not significant at 5\%"),
                why(r"negative binomial: \ significant"), why(r"Birnbaum (1962): \ the likelihood principle")]
        with self.voiceover(
            "<bookmark mark='a'/> A sharp difference between the schools, from Dennis Lindley and Lawrence Phillips. A coin "
            "gives nine heads and three tails. Is it biased towards heads? <bookmark mark='b'/> If the plan was to toss "
            "twelve times, the p-value is point oh seven three: not significant. <bookmark mark='c'/> If the plan was to toss "
            "until the third tail, the same tosses give point oh three three: significant. The p-value depends on what the "
            "experimenter would have done with data that didn't happen. <bookmark mark='d'/> The likelihood is p to the ninth "
            "times one minus p cubed either way, so the Bayesian posterior is identical. Bayesians obey Allan Birnbaum's "
            "likelihood principle; frequentists, by design, do not, and stopping rules are where it shows."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
