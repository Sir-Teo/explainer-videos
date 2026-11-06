from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"completeness and transitivity; \ a money pump, \ 15 cents in 15 trades",
            r"St Petersburg: \ a million games; \ Bernoulli's log; \ Menger",
            r"von Neumann--Morgenstern; \ parallel lines in the triangle",
            r"Allais and Ellsberg: \ no utility, \ no probability fits \ (the Wall)",
            r"risk-weighted utility; \ prospect theory's fourfold pattern",
            r"Kelly: \ $f^* = 2p - 1$; \ 1000 fortunes; \ Pasadena's rearranged sums",
            r"Newcomb at any accuracy; \ the Price List; \ lesion, \ button, \ Damascus",
            r"policies; \ Ulysses and hyperbolic selves; \ Good's theorem; \ two envelopes",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Completeness and transitivity, and a money pump that "
            "took fifteen cents in fifteen trades. <bookmark mark='b'/>The St Petersburg game, played a million "
            "times; Bernoulli's logarithm, and Menger's reply. <bookmark mark='c'/>The von Neumann–Morgenstern "
            "theorem, and its parallel lines in the triangle. <bookmark mark='d'/>Allais's choices, which no "
            "utility fits, and Ellsberg's, which no probability fits: half of this part's brick in the Wall. "
            "<bookmark mark='e'/>Risk-weighted expected utility, and prospect theory's fourfold pattern. "
            "<bookmark mark='f'/>The Kelly fraction, a thousand simulated fortunes, and the Pasadena game's sum "
            "that depends on the order of adding. <bookmark mark='g'/>Newcomb's problem at every accuracy, its "
            "Price List, and the cases that split evidential from causal decision theory: the other half of the "
            "brick. <bookmark mark='h'/>Choosing policies, Ulysses and our hyperbolic selves, Good's theorem drawn "
            "and checked, and the two envelopes."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{decision.money\_pump, st\_petersburg}", r"cycles exploited; \ infinite expectations"),
                (r"\texttt{decision.eu, reu, triangle\_lines}", r"expected and risk-weighted utility"),
                (r"\texttt{decision.allais, ellsberg, prospect}", r"every utility and urn, \ checked"),
                (r"\texttt{decision.kelly, pasadena}", r"growth against ruin; \ rearranged sums"),
                (r"\texttt{decision.newcomb, smoking\_lesion}", r"a predictor; \ evidence against cause"),
                (r"\texttt{decision.damascus, psychopath\_button}", r"instability, \ both ways"),
                (r"\texttt{decision.hitchhiker, ulysses, discounting}", r"policies and selves over time"),
                (r"\texttt{decision.good\_theorem, two\_envelopes}", r"information; \ improper priors")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.48
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_decision.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=33, current=33).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, decision. <bookmark mark='a'/>It computes expected and risk-weighted "
            "utility, draws the Machina triangle, checks Allais and Ellsberg against every utility and every urn, "
            "evaluates prospects, simulates Kelly bettors and Newcomb players, compares evidential and causal "
            "expected utility on small causal models, evaluates policies over time, and checks the value of "
            "information. <bookmark mark='b'/>And the Wall has its thirty third brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[33], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that the money pump needs only strict cyclic preference, \ not completeness.",
            r"Prove that $g(f) = p\log(1+f) + (1-p)\log(1-f)$ is concave, \ and find where it crosses zero.",
            r"For which $u(\$1\text{M})$ does REU with $r(p) = p^2$ give the Allais pattern?",
            r"At what accuracy does a two-boxer's average equal a one-boxer's, \ in the simulation?",
            r"Draw Good's envelope for two acts, \ and find a test with value exactly zero.",
            r"Show that no proper prior makes every amount equally likely to be the smaller envelope.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>The money pump without "
            "completeness; the shape of the Kelly growth curve; the utilities for which risk-weighted utility gives "
            "Allais's pattern; Newcomb's break-even accuracy; a test worth exactly nothing; and why no proper prior "
            "can rescue the two-envelope argument. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"many choosers: \ games, \ backward induction, \ the social contract", [34]),
            (r"Harsanyi's theorem: \ expected utility for a whole society", [35]),
            (r"tiny chances of vast stakes: \ fanaticism and the far future", [36]),
            (r"aggregating preferences: \ Arrow's theorem", [39]),
            (r"agents that predict and are predicted; \ the off-switch", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 34, \textit{Games and the Social Contract}", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Many choosers at once: games, backward induction and the "
            "social contract, in Part 34. Harsanyi's theorem, expected utility for a whole society, in Part 35. "
            "Tiny chances of vast stakes, fanaticism and the far future, in Part 36. Aggregating preferences, and "
            "Arrow's theorem, in Part 39. And agents that predict and are predicted, and the off-switch, in Part "
            "42. <bookmark mark='b'/>Next, Part 34: games and the social contract."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Peterson, \textit{An Introduction to Decision Theory} (2nd ed., 2017)",
             r"Joyce, \textit{The Foundations of Causal Decision Theory} (1999)",
             r"Buchak, \textit{Risk and Rationality} (2013)",
             r"Ahmed, \textit{Evidence, Decision and Causality} (2014)"],
            [r"Bernoulli 1738; Menger 1934; von Neumann and Morgenstern 1944; Allais 1953; Savage 1954",
             r"Kelly 1956; Strotz 1956; Ellsberg 1961; Jeffrey 1965; Good 1967; Nozick 1969",
             r"Gibbard and Harper 1978; Kahneman and Tversky 1979; Lewis 1981; Quiggin 1982; Machina 1982",
             r"Eells 1982; Parfit 1984; Hammond 1988; Gilboa and Schmeidler 1989; McClennen 1990",
             r"Tversky and Kahneman 1992; Broome 1995; Nover and H\'ajek 2004; Colyvan 2006; Egan 2007",
             r"Easwaran 2008; Arntzenius 2008; Hadfield-Menell et al. 2017; Yudkowsky and Soares 2017"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
