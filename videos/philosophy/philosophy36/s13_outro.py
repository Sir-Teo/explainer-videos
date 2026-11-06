from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"four axiologies, \ four best worlds on Parfit's sequence",
            r"the repugnant conclusion; \ the very repugnant, \ 601 times A",
            r"mere addition, \ step by step; \ its Price List",
            r"six conditions, \ five views, \ every row a cross: \ Arrhenius \ (the Wall)",
            r"the asymmetry; \ non-identity: \ harmed, \ 0",
            r"Ramsey derived; \ Stern against Nordhaus, \ 53 times; \ declining rates",
            r"a point of risk: \ 0.06 or 100 centuries; \ a chain of long shots",
            r"Basu--Mitra proved; \ QALYs, \ heavy tails, \ and a \$12 million life",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Four axiologies, with four different best worlds on "
            "Parfit's sequence. <bookmark mark='b'/>The repugnant conclusion, and the very repugnant one, at six "
            "hundred and one times A's population. <bookmark mark='c'/>The mere addition paradox, step by step, and "
            "its Price List. <bookmark mark='d'/>Six conditions and five views, with a cross in every row: "
            "Arrhenius's impossibility, this part's brick in the Wall. <bookmark mark='e'/>The asymmetry, and the "
            "non-identity problem, where the count of people harmed is zero. <bookmark mark='f'/>The Ramsey rule, "
            "derived, Stern against Nordhaus by a factor of fifty three, and Weitzman's declining rates. "
            "<bookmark mark='g'/>A point of extinction risk worth six hundredths of a century or a hundred centuries, "
            "and a chain of long shots that forces recklessness, timidity or intransitivity. "
            "<bookmark mark='h'/>Basu and Mitra's theorem, proved; QALYs and heavy tails; and a statistical life "
            "valued at twelve million dollars."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{population.total, average, critical\_level, variable\_value}", r"axiologies"),
                (r"\texttt{population.parfit\_sequence, mere\_addition}", r"A to Z; \ the staircase"),
                (r"\texttt{population.check, arrhenius\_table}", r"conditions, \ searched"),
                (r"\texttt{population.non\_identity}", r"who is harmed"),
                (r"\texttt{population.ramsey, existential}", r"discounting; \ the time of perils"),
                (r"\texttt{population.fanaticism, infinite}", r"long shots; \ streams"),
                (r"\texttt{population.cost\_effectiveness, vsl}", r"the tools of practice"),
                (r"\texttt{ethics.*}, \ \texttt{games.*}, \ \dots", r"Parts 1--35")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.48
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.4:
                b.width = 4.4
            b.move_to([1.8 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_population.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=36, current=36).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, population. <bookmark mark='a'/>It scores populations by four "
            "axiologies, runs Parfit's sequence and the mere addition staircase, searches small populations for "
            "violations of six conditions, counts who is harmed in a non-identity case, discounts by the Ramsey rule, "
            "values reductions in existential risk, climbs a chain of long shots, compares infinite streams, ranks "
            "interventions by cost per QALY, and derives a value of a statistical life. <bookmark mark='b'/>And the "
            "Wall has its thirty sixth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[36], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that the average view calls a mere addition worse exactly when the added lives are below the "
            r"average.",
            r"Show that every critical-level view with $c > 0$ implies the sadistic conclusion.",
            r"Derive the Ramsey rule for $u(c) = \log c$, \ and say what $\eta$ is.",
            r"With constant risk $r$ after this century, \ show that halving this century's risk $r$ is worth half a "
            r"century, \ whatever $r$.",
            r"Find two streams that the catching-up criterion leaves unranked.",
            r"A rule costs \$90 million and prevents 7 expected deaths: \ find its break-even VSL.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>When the average view calls a "
            "mere addition worse; why every positive critical level is sadistic; the Ramsey rule for logarithmic "
            "utility; what halving this century's risk is worth when the risk stays constant; two streams that "
            "catching up cannot rank; and a break-even value of a statistical life. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"whether intuitions about Z are evidence of anything", [37]),
            (r"justice between generations; \ Rawls's just savings", [38]),
            (r"Arrow's theorem, \ the model for Arrhenius's", [39]),
            (r"algorithms that allocate scarce care, \ and their fairness", [41]),
            (r"the long future of minds like ours, \ and machines", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 37, \textit{Is and Ought}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Whether our intuitions about Z are evidence of anything, in "
            "Part 37. Justice between generations, and Rawls's just savings principle, in Part 38. Arrow's theorem, "
            "the model for Arrhenius's, in Part 39. Algorithms that allocate scarce care, and their fairness, in "
            "Part 41. And the long future of minds like ours, and of machines, in Part 42. "
            "<bookmark mark='b'/>Next, Part 37: is and ought."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Parfit, \textit{Reasons and Persons} (1984), Part Four",
             r"Broome, \textit{Weighing Lives} (2004); \ Greaves, ``Population Axiology'' (2017)",
             r"Arrhenius, ``An Impossibility Theorem for Welfarist Axiologies'' (2000)",
             r"Stern, \textit{The Economics of Climate Change} (2006); \ Ord, \textit{The Precipice} (2020)"],
            [r"Sidgwick 1874; Ramsey 1928; Diamond 1965; Schelling 1968; Narveson 1973; Svensson 1980; McMahan 1981",
             r"Hurka 1983; Jonsen 1986; Parfit 1986, 2016; Ng 1989; Anderson 1993; Blackorby, Bossert and Donaldson 1995",
             r"Weitzman 1998, 2001; Rachels 1998; Tännsjö 2002; Bostrom 2002, 2009, 2011; Basu and Mitra 2003",
             r"Zame 2007; Huemer 2008; Nordhaus 2008; Temkin 2012; Ord 2013; MacAskill 2015; Singer 2015",
             r"Srinivasan 2015; Greaves 2016; Gabriel 2017; Askell 2018; Monton 2019; Greaves and MacAskill 2021",
             r"Zuber et al. 2021; Wilkinson 2022; Crary 2023; Tarsney 2023; Thorstad 2023; Beckstead and Thomas 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
