from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Condorcet's cycle; \ 1 in 18 with 3 voters, \ 8.77\% in the limit, \ 37\% with 7 candidates",
            r"five rules, \ five winners; \ instant runoff; \ every agenda a different winner",
            r"May's theorem: \ 59,049 rules, \ 1 survivor, \ simple majority",
            r"Arrow: \ the pivotal voter; \ Borda's D and E swap when C withdraws \ (the Wall)",
            r"Arrow by SAT: \ 108 variables, \ 992 clauses, \ 2 dictatorships; \ the Price List",
            r"manipulation found for 4 rules, \ none for 2; \ the median wins all 4,096 single-peaked profiles",
            r"quadratic voting; \ juries: \ 0.998, \ or 0.60 with a leader; \ diversity: \ 94 against 89",
            r"the discursive dilemma; \ Alabama's lost seat; \ Bradley--Terry is Borda",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Condorcet's cycle, and its probability: one in eighteen "
            "with three voters, eight point eight percent in the limit, and thirty seven percent with seven "
            "candidates. <bookmark mark='b'/>Five rules with five winners, and an agenda that decides the outcome. "
            "<bookmark mark='c'/>May's theorem: of fifty nine thousand rules, only simple majority survives. "
            "<bookmark mark='d'/>Arrow's theorem and the pivotal voter, this part's brick in the Wall, and the Borda "
            "count breaking independence. <bookmark mark='e'/>Arrow proved again by a SAT solver, with exactly two "
            "dictatorships left, and its Price List. <bookmark mark='f'/>Manipulations found for every reasonable "
            "rule, and the median voter winning every single-peaked profile. <bookmark mark='g'/>Quadratic voting, "
            "the jury theorem and its fragility, and diversity rebuilt. <bookmark mark='h'/>The discursive dilemma, "
            "Alabama's lost seat, and the discovery that reward models count like Borda."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{vote.plurality, borda, irv, kemeny, schulze, \dots}", r"nine rules"),
                (r"\texttt{vote.paradox\_exact, paradox\_simulated}", r"the chance of a cycle"),
                (r"\texttt{vote.may\_theorem, arrow\_cnf, arrow\_sat}", r"theorems by search and SAT"),
                (r"\texttt{vote.manipulation, black}", r"strategy and single peaks"),
                (r"\texttt{vote.jury, hong\_page, list\_pettit}", r"truth and judgment"),
                (r"\texttt{vote.hamilton, divisor, bradley\_terry}", r"seats and reward models"),
                (r"\texttt{justice.*}, \ \texttt{prop.*}, \ \dots", r"Parts 1--38")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_vote.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=39, current=39).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, vote. <bookmark mark='a'/>It counts ballots by nine rules, computes the "
            "chance of a cycle exactly and by simulation, proves May's and Arrow's theorems by search and by SAT, "
            "searches for manipulations, checks the median voter theorem, computes juries, rebuilds Hong and Page, "
            "checks List and Pettit, divides seats, and fits reward models. <bookmark mark='b'/>And the Wall has its "
            "thirty ninth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[39], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that with an odd number of voters, \ pairwise majority on two alternatives is never tied.",
            r"Find a profile of 3 voters on which the Borda winner is not the Condorcet winner.",
            r"Show that if preferences are single-peaked, \ the majority relation among 3 options has no cycle.",
            r"Show that a dictatorship is strategy-proof.",
            r"With $p = 0.6$, \ compute the probability that a majority of 3 independent voters is right.",
            r"Find quotas where Hamilton's method and Webster's method disagree.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Why an odd electorate never "
            "ties; a Borda winner who is not the Condorcet winner; why single peaks forbid cycles; why a dictator "
            "cannot be manipulated; the smallest jury theorem; and two seat methods that disagree. Pause here, and "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"judgments of taste, \ and whether they can be aggregated", [40]),
            (r"fairness criteria that cannot all hold: \ an impossibility like Arrow's", [41]),
            (r"aggregating human feedback, \ and whose values a machine should have", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 40, \textit{Beauty}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Part 40 asks whether judgments of beauty can be right or "
            "wrong, and whether a crowd of critics converges. Part 41 meets fairness criteria for machines that "
            "cannot all hold together, an impossibility in Arrow's style. And Part 42 asks how to aggregate human "
            "feedback, and whose values a machine should have. <bookmark mark='b'/>Next, Part 40: beauty."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Arrow, \textit{Social Choice and Individual Values} (1951); \ Sen, \textit{Collective Choice and Social "
             r"Welfare} (1970; 2017)",
             r"Brandt, Conitzer, Endriss, Lang and Procaccia (eds), \textit{Handbook of Computational Social Choice} "
             r"(2016)",
             r"List and Pettit, \textit{Group Agency} (2011); \ Saari, \textit{Chaotic Elections!} (2001)",
             r"Balinski and Young, \textit{Fair Representation} (1982); \ Gaertner, \textit{A Primer in Social Choice "
             r"Theory}"],
            [r"Llull 1299; Cusanus 1433; Borda 1770; Condorcet 1785; Dodgson 1876; Galton 1907; Hotelling 1929",
             r"Black 1948; May 1952; Guilbaud 1952; Downs 1957; Vickrey 1961; Plott 1967; Sen 1966, 1970, 1991",
             r"Gibbard 1973, 1977; Satterthwaite 1975; Young 1975, 1988; McKelvey 1976; d'Aspremont and Gevers 1977",
             r"Brams and Fishburn 1978; Moulin 1980; Riker 1982; Kornhauser and Sager 1986; Bartholdi, Tovey and Trick "
             r"1989",
             r"Ladha 1992; Habermas 1992; Pettit 2001; Ford 2002; List and Pettit 2002; G. Mackie 2003; Hong and Page "
             r"2004",
             r"Geanakoplos 2005; Conitzer, Sandholm and Lang 2007; Estlund 2008; Dasgupta and Maskin 2008; Friedgut, "
             r"Kalai and Nisan 2008",
             r"Tang and Lin 2009; Nipkow 2009; Faliszewski and Procaccia 2010; Balinski and Laraki 2011; Geist and "
             r"Endriss 2011",
             r"Landemore 2013; List et al. 2013; Dietrich and Spiekermann 2013; Thompson 2014; Brandt and Geist 2016; "
             r"Brennan 2016",
             r"Lalley and Weyl 2018; Kahng, Mackenzie and Procaccia 2018; Siththaranjan et al. 2023; Conitzer et al. "
             r"2024; Ge et al. 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
