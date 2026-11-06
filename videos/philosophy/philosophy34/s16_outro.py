from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Nash equilibrium by support enumeration; \ best responses crossing",
            r"the dilemma; \ the commons, \ 1 to 100 herders; \ Ostrom's sanctions",
            r"the stag hunt: \ basins and stochastic stability",
            r"the centipede: \ backward induction, \ noisy players \ (the Wall)",
            r"correlated equilibrium: \ 5.25 each, \ by linear programming",
            r"the shadow of the future; \ the folk theorem, \ 156 plans; \ Axelrod with noise; \ extortion",
            r"evolution with rare mutations; \ fair division on the simplex, \ 72\%",
            r"Nash, \ Kalai--Smorodinsky, \ Rubinstein; \ Shapley and SHAP; \ auctions and matching",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Nash equilibrium, found by support enumeration, and "
            "best responses crossing. <bookmark mark='b'/>The prisoner's dilemma, the commons with up to a hundred "
            "herders, and Ostrom's sanctions. <bookmark mark='c'/>The stag hunt, its basins, and the stochastic "
            "stability of hare. <bookmark mark='d'/>The centipede, backward induction and noisy players: this part's "
            "brick in the Wall. <bookmark mark='e'/>Correlated equilibrium by linear programming, five and a quarter "
            "each. <bookmark mark='f'/>The shadow of the future, the folk theorem with "
            "the patience a hundred and fifty-six plans need, Axelrod's tournaments with noise, the population river, "
            "and extortion checked two thousand times. <bookmark mark='g'/>Evolution with rare mutations, and fair division from "
            "seventy two percent of the simplex. <bookmark mark='h'/>Bargaining, the Shapley value and SHAP, "
            "auctions, sponsored search and matching."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{games.nash\_equilibria, best\_responses}", r"support enumeration; \ crossings"),
                (r"\texttt{games.commons, public\_goods}", r"dilemmas with many players"),
                (r"\texttt{games.stag\_hunt, centipede}", r"selection; \ backward induction"),
                (r"\texttt{games.correlated\_chicken}", r"a linear program"),
                (r"\texttt{games.shadow, folk\_theorem}", r"repetition and patience"),
                (r"\texttt{games.tournament, ecological}", r"the strategy zoo, \ with noise"),
                (r"\texttt{games.zero\_determinant, evolution\_rare\_mutation}", r"Markov chains of play"),
                (r"\texttt{games.nash\_demand, bargaining, shapley}", r"fair division three ways"),
                (r"\texttt{games.auctions, gsp\_vcg, gale\_shapley}", r"mechanisms, \ checked"),
                (r"\texttt{decision.*}, \ \texttt{freewill.*}, \ \dots", r"Parts 1--33")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.46
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_games.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=34, current=34).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, games. <bookmark mark='a'/>It finds Nash equilibria, solves the commons "
            "and the stag hunt, runs the centipede backward with noisy players, finds correlated equilibria by "
            "linear programming, measures the patience a repeated game needs, plays tournaments with noise, turns "
            "memory-one strategies into Markov chains, "
            "evolves populations with rare mutations, computes basins of fair division, bargaining solutions and "
            "Shapley values, and checks auctions and matchings for truthfulness and stability. "
            "<bookmark mark='b'/>And the Wall has its thirty fourth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[34], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Find every Nash equilibrium of rock--paper--scissors, \ and prove there are no others.",
            r"In the commons, \ show that total grazing tends to $a - c$ as $n \to \infty$.",
            r"For what discount factor does grim trigger sustain cooperation in the repeated dilemma?",
            r"Derive the extortionate strategy for $\chi = 2$ with $(T, R, P, S) = (5, 3, 1, 0)$.",
            r"Show that the Shapley value of a unanimity game on $T$ gives $1/|T|$ to each member.",
            r"Prove that no student can gain by misreporting in deferred acceptance with two schools.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>The equilibria of rock "
            "paper scissors; the commons in the limit; the discount factor that sustains cooperation; an extortioner "
            "with a different ratio; the Shapley value of a unanimity game; and honesty in deferred acceptance. Pause "
            "here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"aggregating welfare: \ Harsanyi, \ utilitarianism, \ contractualism", [35]),
            (r"fairness across generations", [36]),
            (r"norms that evolve, \ and whether they bind", [37]),
            (r"the original position; \ justice as fairness", [38]),
            (r"voting as a mechanism: \ Arrow, \ Gibbard--Satterthwaite", [39]),
            (r"Shapley values in explanation; \ incentives in machines", [41, 42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 35, \textit{The Right and the Good}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Aggregating welfare, with Harsanyi and the utilitarians and "
            "their contractualist critics, in Part 35. Fairness across generations, in Part 36. Norms that evolve, "
            "and whether they bind, in Part 37. The original position and justice as fairness, in Part 38. Voting "
            "as a mechanism, with Arrow and the Gibbard–Satterthwaite theorem, in Part 39. And Shapley values in "
            "explanation, and incentives in machines, in Parts 41 and 42. <bookmark mark='b'/>Next, Part 35: the "
            "right and the good."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Osborne and Rubinstein, \textit{A Course in Game Theory} (1994)",
             r"Binmore, \textit{Game Theory and the Social Contract} (1994, 1998)",
             r"Skyrms, \textit{Evolution of the Social Contract} (1996); \textit{The Stag Hunt} (2004)",
             r"Nisan, Roughgarden, Tardos and Vazirani, \textit{Algorithmic Game Theory} (2007)"],
            [r"Hobbes 1651; Hume 1739; Rousseau 1755; Nash 1950, 1951; Shapley 1953; Vickrey 1961",
             r"Gale and Shapley 1962; Hardin 1968; Friedman 1971; Aumann 1974; Axelrod 1980, 1984; Rosenthal 1981",
             r"Myerson 1981; Rubinstein 1982; Roth 1982; Fudenberg and Maskin 1986; Gauthier 1986; Ostrom 1990",
             r"Harsanyi and Selten 1988; Kandori, Mailath and Rob 1993; Nowak and Sigmund 1993; Aumann 1995",
             r"Fehr and Schmidt 1999; Imhof, Fudenberg and Nowak 2005; Daskalakis et al. 2006; Roth 2007",
             r"Edelman et al. 2007; Press and Dyson 2012; Stewart and Plotkin 2013; Lundberg and Lee 2017",
             r"Kumar et al. 2020"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
