from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Fisher, \ Neyman--Pearson, \ Jeffreys: \ evidence against, \ no decision, \ evidence for",
            r"the $p$-value's distribution; \ six misreadings; \ the ASA statement",
            r"base rates and PPV; \ the garden of forking paths; \ the replication record",
            r"optional stopping; \ the likelihood principle; \ Birnbaum's theorem \ (the Wall)",
            r"Lindley's paradox; \ the bound $e^{z^2/2}$; \ severity curves",
            r"Simpson's paradox at Berkeley; \ the reference class; \ A/B tests and peeking",
            r"testing by betting and Ville's inequality; \ AIC against BIC",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Three schools, and three verdicts from one coin. "
            "<bookmark mark='b'/>What a p-value is, and six things it is not. <bookmark mark='c'/>Base rates, why "
            "many findings are false, and a machine that manufactures discoveries from noise. "
            "<bookmark mark='d'/>Optional stopping, and Birnbaum's theorem, this part's brick in the Wall. "
            "<bookmark mark='e'/>Lindley's paradox, the limits of a significant result, and severity. "
            "<bookmark mark='f'/>Simpson's paradox, the reference class, and statistics in industry. "
            "<bookmark mark='g'/>And testing by betting, with the choice between truth and prediction in model "
            "selection."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{stats.three\_schools, p\_distribution, misreadings}", r"one coin; \ $p$"),
                (r"\texttt{stats.base\_rate, ppv, ioannidis\_table}", r"base rates"),
                (r"\texttt{stats.garden, garden\_paths, optional\_stopping}", r"forking paths; \ peeking"),
                (r"\texttt{stats.birnbaum, lindley, prior\_sensitivity}", r"likelihood; \ Bayes factors"),
                (r"\texttt{stats.severity, simpson, betting, ab\_peeking}", r"severity; \ betting"),
                (r"\texttt{stats.aic\_bic}, \ \texttt{stats.t\_two\_sided}", r"model choice"),
                (r"\texttt{induction.*}, \ \texttt{revision.*}, \ \dots", r"Parts 1--15")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_stats.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=16, current=16).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, stats. <bookmark mark='a'/>It runs the three schools on one coin, "
            "simulates p-values and their misreadings, computes base rates and Ioannidis's table, walks the garden "
            "of forking paths, peeks at data under the null, checks Birnbaum's example and Lindley's paradox, draws "
            "severity curves, reverses Berkeley, bets against a fair coin, and chooses polynomial degrees by AIC and "
            "BIC. <bookmark mark='b'/>And the Wall has its sixteenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[16], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prevalence 0.1\%, \ sensitivity 99\%, \ false positives 1\%: \ what share of positives are sick?",
            r"For Ann's and Bo's coins, \ show that the Bayes factor under a uniform prior is the same.",
            r"Prove that under $H_0$ the $p$-value of a continuous test statistic is uniform on $[0, 1]$.",
            r"If $E_1, E_2$ are independent e-values, \ is $E_1 E_2$ one? \ Is $(E_1 + E_2)/2$?",
            r"Compute Lindley's $B_{01}$ for $z = 3$, \ $n = 10^4$, \ $\tau = 1$. \ Which way does it point?",
            r"Reweight Berkeley's six departments by total applicants: \ who is admitted more?",
        ], font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A rare disease and a good "
            "test; Ann and Bo under Bayes; why p is uniform under the null; combining e-values; Lindley's paradox at "
            "three sigma; and Berkeley, reweighted. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Simpson's paradox, \ randomized trials, \ causal graphs", [17]),
            (r"underdetermination; \ truth or prediction", [18]),
            (r"frequencies, \ propensities, \ and chance", [24]),
            (r"tests as decisions; \ expected utility", [33]),
            (r"reference classes and fair risk scores", [41]),
            (r"evaluating machines: \ benchmarks, \ evals, \ significance", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 17, \textit{Cause}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Simpson's paradox, randomized trials and causal graphs, in "
            "Part 17. Underdetermination, and the choice between truth and prediction, in Part 18. Frequencies and "
            "propensities, in Part 24. Tests as decisions, in Part 33. Reference classes and fair risk scores, in "
            "Part 41. And the statistics of evaluating machines, in the finale. <bookmark mark='b'/>Next, Part 17: "
            "cause."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Royall, \textit{Statistical Evidence} (1997); \ Hacking, \textit{Logic of Statistical Inference} (1965)",
             r"Mayo, \textit{Statistical Inference as Severe Testing} (2018); \ Sober, \textit{Evidence and Evolution} "
             r"(2008), ch.\ 1",
             r"Berger and Wolpert, \textit{The Likelihood Principle} (1988); \ Shafer and Vovk, \textit{Game-Theoretic "
             r"Foundations} (2019)",
             r"Kohavi, Tang and Xu, \textit{Trustworthy Online Controlled Experiments} (2020)"],
            [r"Fisher 1925; Neyman and Pearson 1933; Jeffreys 1939; Ville 1939; Wald 1945; Lindley 1957; Birnbaum 1962",
             r"Edwards, Lindman and Savage 1963; Akaike 1973; Bickel et al.\ 1975; Schwarz 1978; Forster and Sober 1994",
             r"Sellke et al.\ 2001; Ioannidis 2005; Hájek 2007; Simmons et al.\ 2011; Gelman and Loken 2013; Mayo 2014",
             r"Open Science Collaboration 2015; Wasserstein and Lazar 2016; Johari et al.\ 2017; Benjamin et al.\ 2018; "
             r"Ramdas et al.\ 2023; Grünwald et al.\ 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
