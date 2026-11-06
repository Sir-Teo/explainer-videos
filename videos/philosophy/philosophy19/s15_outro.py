from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Paley's watch and Darwin's argument, \ as likelihoods; \ the eye in 364{,}000 generations",
            r"Lewontin's recipe and the breeder's equation; \ drift against Kimura's formula",
            r"the Price equation, \ derived and checked on 500 birds; \ Fisher's fundamental theorem",
            r"hawks and doves on the simplex; \ ESS; \ rock, \ paper, \ scissors; \ signals that learn to mean",
            r"Hamilton's rule; \ haplodiploidy; \ multilevel selection and Simpson's reversal \ (the Wall)",
            r"genes and vehicles; \ spandrels; \ three adaptationisms; \ functions and Swampman \ (a Price List)",
            r"species, \ kinds and cladistic parsimony; \ the genetic code counted; \ parity in bits",
            r"Axelrod and the shadow of the future; \ entropy budgets; \ definitions of life; \ Conway and Lenia",
        ]
        card = objectives_card(items, title=r"What we built", font_size=23)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Paley's design argument and Darwin's reply, weighed as "
            "likelihoods, and the eye's clock. <bookmark mark='b'/>Lewontin's three conditions, the breeder's equation, "
            "and drift. <bookmark mark='c'/>The Price equation, derived and checked, with Fisher's theorem inside it. "
            "<bookmark mark='d'/>Evolutionary game theory on the simplex, and signals that come to mean something. "
            "<bookmark mark='e'/>Hamilton's rule, relatedness counted gene by gene, and the levels of selection: this "
            "part's brick in the Wall. <bookmark mark='f'/>Genes and organisms, spandrels and adaptationism, and "
            "functions, with Swampman's Price List. <bookmark mark='g'/>Species and kinds, trees, the genetic code, and "
            "parity in bits. <bookmark mark='h'/>Cooperation and the shadow of the future, the thermodynamics of life, "
            "the failure of its definitions, and artificial life, from von Neumann to a creature the Reasoner found for "
            "itself."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{evo.paley\_likelihoods, eye\_generations, breeder}", r"design; \ heredity"),
                (r"\texttt{evo.wright\_fisher, kimura\_fix}", r"drift"),
                (r"\texttt{evo.price\_check, fisher\_theorem}", r"the Price equation"),
                (r"\texttt{evo.replicator, hawk\_dove, rps, lewis\_signalling}", r"games; \ signals"),
                (r"\texttt{evo.hamilton\_sim, relatedness, multilevel}", r"kin; \ levels"),
                (r"\texttt{evo.code\_information, parity\_demo, fitch\_score}", r"code; \ trees"),
                (r"\texttt{evo.axelrod\_mini, shadow, entropy\_budget, life\_definitions}", r"cooperation; \ life"),
                (r"\texttt{evo.conway\_glider, lenia\_glider}", r"artificial life"),
                (r"\texttt{science.*}, \ \texttt{causal.*}, \ \dots", r"Parts 1--18")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.5
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_evo.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=19, current=19).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, evo. <bookmark mark='a'/>It weighs design against selection, times the "
            "eye, breeds with and without heredity, checks drift against Kimura, verifies the Price equation and "
            "Fisher's theorem, runs replicator dynamics and signalling games, counts relatedness and applies Hamilton's "
            "rule, splits selection into levels, counts the genetic code and its information, scores trees by "
            "parsimony, plays the repeated prisoner's dilemma in and out of the shadow of the future, balances entropy "
            "budgets, tests definitions of life, and runs Conway's Life and Lenia. <bookmark mark='b'/>And the Wall has "
            "its nineteenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[19], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive the Price equation $\bar w \, \Delta \bar z = \mathrm{Cov}(w, z) + \mathrm{E}(w \, \Delta z)$ "
            r"for two types with no mutation.",
            r"In hawk--dove with $V = 4$, $C = 6$, \ find the mixed ESS, \ and show that it resists invasion by "
            r"pure hawks.",
            r"Show that with $r = 1/8$ and $c = 1$, \ altruism spreads only if $b > 8$. \ Which relative has "
            r"$r = 1/8$?",
            r"Give two groups in which altruists lose within each group yet rise overall. \ Which Price term "
            r"is positive?",
            r"A codon mutates at one letter. \ Why are third-position changes most often silent?",
            r"Check by hand that the glider returns to its shape after four steps, \ shifted by $(1, 1)$.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Derive the Price "
            "equation; find a mixed evolutionarily stable strategy; apply Hamilton's rule to cousins; build a "
            "Simpson reversal; explain silent mutations; and step the glider by hand. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"natural kinds and species as individuals", [20]),
            (r"persistence: \ the glider, \ Theseus's ship, \ and you", [21]),
            (r"design arguments, \ fine-tuning and likelihoods", [23]),
            (r"organization and realization: \ minds and machines", [30]),
            (r"evolutionary games and the social contract", [34]),
            (r"evolutionary debunking of moral realism", [37]),
            (r"open-endedness and what we want from artificial agents", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Act V, \ \textit{The World}: \ Part 20, \textit{What There Is}", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Natural kinds, and species as individuals, in Part 20. "
            "Persistence, with gliders and ships, in Part 21. Design arguments and fine-tuning, in Part 23. "
            "Organization and minds, in Part 30. Evolutionary games and the social contract, in Part 34. "
            "Evolutionary debunking of morality, in Part 37. And open-endedness in artificial agents, in the "
            "finale. <bookmark mark='b'/>Next, Act Five begins, with the oldest question of all: what there is."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Sober, \textit{The Nature of Selection} (1984) and \textit{Philosophy of Biology} (1993, 2000)",
             r"Okasha, \textit{Evolution and the Levels of Selection} (2006); \ Godfrey-Smith, \textit{Darwinian "
             r"Populations and Natural Selection} (2009)",
             r"Sterelny and Griffiths, \textit{Sex and Death} (1999); \ Maynard Smith, \textit{Evolution and the "
             r"Theory of Games} (1982)",
             r"Schrödinger, \textit{What Is Life?} (1944); \ Bedau and Cleland (eds.), \textit{The Nature of Life} "
             r"(2010)"],
            [r"Lewontin 1970; Price 1970, 1972; Hamilton 1964; Maynard Smith and Price 1973; Mills and Beatty 1979",
             r"Wright 1973; Cummins 1975; Millikan 1984; Gould and Lewontin 1979; Hull 1980; Ghiselin 1974",
             r"Axelrod and Hamilton 1981; Nowak 2006; Nowak, Tarnita and Wilson 2010; Maynard Smith 2000",
             r"von Neumann 1966; Langton 1989; Ray 1991; Lenski et al. 2003; Chan 2019; Cleland 2012"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
