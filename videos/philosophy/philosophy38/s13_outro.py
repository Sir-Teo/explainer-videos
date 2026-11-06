from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Thrasymachus and Gyges; \ Plato's city and soul; \ Popper's charge",
            r"Hobbes, \ Locke, \ Rousseau; \ Hume against tacit consent",
            r"the original position; \ the difference principle: \ (8, \ 6) over (5, \ 5) and (12.5, \ 3.75)",
            r"200 societies: \ the average picks 140, \ maximin 173, \ moderate risk aversion 128",
            r"Wilt: \ a Gini of 0.01 from free exchange; \ the Price List; \ the proviso",
            r"Dworkin's auction: \ prices 1.11, \ 0.89, \ 1, \ envy-free; \ Anderson; \ Sen and Nussbaum",
            r"Sen's paradox in all 6 assignments \ (the Wall); \ Berlin, \ MacCallum, \ Pettit",
            r"Selfridge--Conway; \ rent at \$165 or more; \ stable matching, \ 3 of 24; \ Sandel to Pogge",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Thrasymachus and the ring of Gyges, Plato's city and "
            "soul, and Popper's charge against them. <bookmark mark='b'/>The social contract from Hobbes to Rousseau, "
            "and Hume's objection. <bookmark mark='c'/>The original position, and the difference principle, which "
            "prefers eight and six to five and five, and to twelve and a half and three and three quarters. <bookmark "
            "mark='d'/>Two hundred societies chosen behind the veil: the average picks one, maximin another, and "
            "moderate risk aversion a third. <bookmark mark='e'/>Wilt Chamberlain's fortune from free exchange, the "
            "Price List, and the proviso. <bookmark mark='f'/>Dworkin's auction, built and envy-free, and the debate "
            "over equality of what. <bookmark mark='g'/>Sen's paradox, forced in every assignment of rights: this "
            "part's brick in the Wall; and three ideas of liberty. <bookmark mark='h'/>Fair division from cake to "
            "rent, stable matching for schools, and the critics and extenders of the whole tradition, from Sandel to Pogge."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{justice.veil}", r"choosing a society, \ under any attitude to risk"),
                (r"\texttt{justice.ceei}", r"equilibrium from equal incomes"),
                (r"\texttt{justice.liberal\_paradox}", r"Sen's theorem, \ by exhaustive search"),
                (r"\texttt{justice.selfridge\_conway, \ rent\_division}", r"envy-free division"),
                (r"\texttt{justice.stable\_matching}", r"deferred acceptance, \ every matching checked"),
                (r"\texttt{justice.gini, \ wilt, \ three\_societies}", r"inequality"),
                (r"\texttt{prop.mus\_mcs}", r"the Price List"),
                (r"\texttt{metaethics.*}, \ \texttt{population.*}, \ \dots", r"Parts 1--37")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_justice.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=38, current=38).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, justice. <bookmark mark='a'/>It chooses societies behind a veil under any "
            "attitude to risk, finds competitive equilibria from equal incomes, searches every assignment of rights "
            "for Sen's cycle, divides cakes and rents without envy, matches students to schools stably, and measures inequality. <bookmark mark='b'/>And "
            "the Wall has its thirty eighth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[38], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that if only one person has rights, \ over any number of pairs, \ rights and Pareto never force a "
            r"cycle.",
            r"Compute the Gini coefficient of the incomes $(0, 0, 0, 1)$, \ and explain why it is not 1.",
            r"With societies $(1, 9)$ and $(4, 4)$, \ for which $\eta$ does the CRRA chooser prefer the second?",
            r"Show that Ana, \ the first cutter, \ never envies whoever took the trimmed piece in Selfridge--Conway.",
            r"Check that rents $(1400, 900, 700)$ are also envy-free, \ and find the least surplus.",
            r"State the Wilt Chamberlain argument as an inconsistent set, \ and say which claim you would deny.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Why Sen's theorem needs two "
            "people with rights; the Gini coefficient of a society where one person has everything; the risk aversion "
            "at which a chooser switches to the equal society; why the first cutter in Selfridge and Conway's "
            "procedure never envies the trimmed piece; another envy-free rent, and its least surplus; and Nozick's "
            "argument as a Price List. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"aggregating preferences: \ Arrow, \ Gibbard--Satterthwaite, \ the discursive dilemma", [39]),
            (r"fairness for classifiers: \ which equality, \ and can they all hold?", [41]),
            (r"envy-free and maximin allocation, \ by machines", [41]),
            (r"the veil of ignorance as a method for aligning AI", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 39, \textit{The Arithmetic of Democracy}", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Sen's paradox is a cousin of Arrow's theorem, which Part 39 "
            "proves, along with the impossibility of a voting rule that cannot be gamed. Part 41 asks which equality "
            "a classifier should have, finds that the natural measures cannot all hold together, and uses envy-free "
            "and maximin allocation. And Part 42 asks whether the veil of ignorance can guide the alignment of an AI "
            "system. <bookmark mark='b'/>Next, Part 39: the arithmetic of democracy."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kymlicka, \textit{Contemporary Political Philosophy} (2nd ed., 2002); \ Rawls, \textit{A Theory of "
             r"Justice} (1971)",
             r"Nozick, \textit{Anarchy, State, and Utopia} (1974); \ Sen, \textit{Collective Choice and Social Welfare} "
             r"(1970; 2017)",
             r"Brams and Taylor, \textit{Fair Division} (1996); \ Moulin, \textit{Fair Division and Collective Welfare} "
             r"(2003)",
             r"Procaccia, `Cake Cutting Algorithms', \textit{Handbook of Computational Social Choice} (2016)"],
            [r"Plato, \textit{Republic}; Hobbes 1651; Locke 1689; Hume 1748; Rousseau 1762; Constant 1819; Mill 1859",
             r"Popper 1945; Steinhaus 1948; Harsanyi 1953, 1975; Berlin 1958; Dubins and Spanier 1961; MacCallum 1967",
             r"Foley 1967; Sen 1970, 1979, 2009; Rawls 1971, 1993, 1999; Gibbard 1974; Varian 1974; Beitz 1979",
             r"Taylor 1979; Dworkin 1981; MacIntyre 1981; Sandel 1982, 2012; Walzer 1983; Carens 1987; Harel and Nitzan 1987",
             r"Pateman 1988; Okin 1989; Arneson 1989; Cohen 1989, 1995, 2008; Young 1990; Gaertner, Pattanaik and Suzumura 1992",
             r"Shue 1993; Brams and Taylor 1995; Pettit 1997; Mills 1997; Anderson 1999; Nussbaum 2000; Blake 2001",
             r"Murphy and Nagel 2002; Pogge 2002; Lipton et al. 2004; Nagel 2005; Cohen and Sabel 2006; Wellman 2008",
             r"Procaccia 2009; Budish 2011; Gardiner 2011; Chan 2014; Bell 2015; Milanović 2015; Aziz and Mackenzie 2016",
             r"Caragiannis et al. 2016; Gal, Mash, Procaccia and Zick 2016; Bai 2019; Gabriel 2020; Weidinger et al. 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
