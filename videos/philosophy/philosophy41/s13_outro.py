from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"COMPAS: \ 45\% against 23\% false positives; \ 63\% against 59\% precision",
            r"independence, \ separation, \ sufficiency; \ one threshold, \ unequal error rates",
            r"Chouldechova's identity checked; \ balance 0.44 against 0.60 \ (the Wall); \ the Price List",
            r"equal false positives: \ precision 0.55 against 0.74; \ the cost of fairness",
            r"Hedden's coins; \ Hellman; \ Long; \ Binns",
            r"Dwork's Lipschitz condition; \ counterfactual fairness, \ a 1.0 shift removed",
            r"$e^{\varepsilon}$ checked; \ randomized response 0.34; \ 64 bits rebuilt",
            r"Shapley 0.45, \ 0.20, \ $-0.60$; \ three counterfactuals; \ responsibility gaps",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The COMPAS dispute, in which both sides' numbers were "
            "right. <bookmark mark='b'/>Three criteria of fairness, and a single threshold that leaves error rates "
            "unequal. <bookmark mark='c'/>Chouldechova's identity and Kleinberg's balance, this part's brick in the "
            "Wall, and its Price List. <bookmark mark='d'/>Separate thresholds, which trade one equality for another. "
            "<bookmark mark='e'/>Hedden's coins and the philosophers' replies. <bookmark mark='f'/>Individual and "
            "counterfactual fairness. <bookmark mark='g'/>Differential privacy's guarantee checked, a survey that "
            "protects every answer, and a database rebuilt from accurate sums. <bookmark mark='h'/>Shapley values, "
            "counterfactual explanations that are not unique, and the gaps in responsibility."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{fairness.population, criteria, sweep}", r"group criteria and the identity"),
                (r"\texttt{fairness.group\_thresholds}", r"the trade-off, \ group by group"),
                (r"\texttt{fairness.counterfactual}", r"a structural causal model"),
                (r"\texttt{fairness.laplace, randomized\_response}", r"differential privacy"),
                (r"\texttt{fairness.composition, reconstruction}", r"the privacy budget, \ and an attack"),
                (r"\texttt{fairness.explain}", r"Shapley values and counterfactuals"),
                (r"\texttt{aesthetics.*}, \ \texttt{vote.*}, \ \dots", r"Parts 1--40")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_fairness.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=41, current=41).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, fairness. <bookmark mark='a'/>It builds populations and measures every "
            "group criterion, checks the impossibility, searches thresholds, reasons with a causal model, adds "
            "calibrated noise, attacks noisy data, and explains a model's decisions. <bookmark mark='b'/>And the Wall "
            "has its forty first brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[41], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive Chouldechova's identity from the four cells of the confusion table.",
            r"Show that a perfect predictor satisfies calibration and both balance conditions.",
            r"Why does a classifier that labels everyone high risk satisfy demographic parity?",
            r"Compute $\varepsilon$ for randomized response with a coin that shows heads with probability $3/4$.",
            r"Two queries with $\varepsilon = 0.5$ each: \ what is the total by basic composition?",
            r"Find the Shapley values of $f = x_1 x_2$ at $(1, 1)$ with baseline $(0, 0)$.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>The identity from scratch; "
            "why perfect prediction escapes the theorem; a trivially fair but useless classifier; the privacy of a "
            "biased coin; adding up a privacy budget; and the Shapley values of a product. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"whose values a reasoner should have: \ fairness as one of them", [42]),
            (r"optimizing a proxy, \ and what goes wrong: \ Goodhart's law", [42]),
            (r"responsibility for systems that act on their own", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 42, \textit{Aligning Reasoners}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Part 42, the finale, asks whose values a reasoner should "
            "have, of which fairness is one; what goes wrong when a system optimizes a measurable proxy, as the "
            "health algorithm optimized cost; and who is responsible for systems that act on their own. <bookmark "
            "mark='b'/>Next, Part 42: aligning reasoners."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Barocas, Hardt and Narayanan, \textit{Fairness and Machine Learning} (2023)",
             r"Dwork and Roth, \textit{The Algorithmic Foundations of Differential Privacy} (2014)",
             r"Hellman, `Measuring Algorithmic Fairness' (2020); \ Nissenbaum, \textit{Privacy in Context} (2010)",
             r"Kleinberg, Mullainathan and Raghavan (2016); \ Chouldechova (2017)"],
            [r"Warren and Brandeis 1890; Warner 1965; \textit{Griggs v. Duke Power} 1971; Phelps 1972; Arrow 1973",
             r"Rachels 1975; Thompson 1980; Nissenbaum 1996; Sweeney 2000; Dinur and Nissim 2003; Matthias 2004",
             r"Dwork, McSherry, Nissim and Smith 2006; Hellman 2008; Narayanan and Shmatikov 2008; Solove 2008",
             r"Dwork et al. 2012; Lippert-Rasmussen 2014; Eidelson 2015; Angwin et al. 2016; Burrell 2016",
             r"Hardt, Price and Srebro 2016; Corbett-Davies et al. 2017; Kusner et al. 2017; Lundberg and Lee 2017",
             r"Wachter, Mittelstadt and Russell 2017; Zafar et al. 2017; Binns 2018; Buolamwini and Gebru 2018",
             r"Dressel and Farid 2018; Durán and Formanek 2018; Hébert-Johnson et al. 2018; Kohler-Hausmann 2019",
             r"Mitchell et al. 2019; Obermeyer et al. 2019; Rudin 2019; Zuboff 2019; Slack et al. 2020; Hedden 2021",
             r"Gebru et al. 2021; Long 2021; Santoni de Sio and Mecacci 2021; EU AI Act 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
