from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Bentham's ledger; \ Sidgwick; \ two levels: \ when rules beat calculation",
            r"theories of welfare; \ the experience machine, \ 77\% would not enter",
            r"Harsanyi's theorem; \ two egalitarian rules, \ each broken",
            r"sum, \ priority, \ maximin; \ levelling down; \ the monster; \ Singer's pond",
            r"Kant; \ the universal lie collapses; \ five maxims; \ the murderer at the door",
            r"Ross; \ doing and allowing; \ the paradox of deontology \ (the Wall)",
            r"trolleys and double effect; \ the Price List; \ the Moral Machine",
            r"Taurek; \ aggregation; \ particularism; \ care; \ uncertainty and its value",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Bentham's ledger, Sidgwick's dualism, and two levels "
            "of moral thinking, with the noise at which calculation loses to rules. <bookmark mark='b'/>Theories of welfare, and the experience machine, which seventy "
            "seven percent of philosophers would not enter. <bookmark mark='c'/>Harsanyi's theorem, with two "
            "egalitarian rules broken in exactly the ways it predicts. <bookmark mark='d'/>Sums, priority, maximin and "
            "inequality measures, levelling down, the utility monster, and what Singer's argument asks of the rich. "
            "<bookmark mark='e'/>Kant, a world in which the universal lie collapses, the "
            "humanity formula as a consent test, five maxims tested, and the murderer at the door. <bookmark mark='f'/>Ross's duties, doing and allowing, and the paradox of "
            "deontology, this part's brick in the Wall. <bookmark mark='g'/>The trolley problem, double effect and its Price List. "
            "<bookmark mark='h'/>Taurek's numbers, Scanlon and partial aggregation, virtue, the holism of reasons "
            "against weighted rules, care, moral uncertainty, and the value of finding out which theory is true."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{ethics.felicific, two\_level}", r"Bentham's ledger; \ rules against acts"),
                (r"\texttt{ethics.harsanyi}", r"welfare functions, \ checked"),
                (r"\texttt{ethics.distributions, utility\_monster, pond}", r"distributions; \ the monster; \ the pond"),
                (r"\texttt{ethics.promise\_world, maxims, humanity\_test}", r"Kant's tests, \ run"),
                (r"\texttt{ethics.deontology\_paradox}", r"agent-relative rankings"),
                (r"\texttt{ethics.trolley, taurek, transmitter}", r"double effect; \ the numbers; \ aggregation"),
                (r"\texttt{ethics.particularism}", r"fixed weights against defeaters"),
                (r"\texttt{ethics.moral\_uncertainty, moral\_information}", r"choiceworthiness; \ moral VOI"),
                (r"\texttt{games.*}, \ \texttt{decision.*}, \ \dots", r"Parts 1--34")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_ethics.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=35, current=35).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, ethics. <bookmark mark='a'/>It keeps Bentham's ledger, checks social "
            "welfare functions against Harsanyi's axioms, pits a noisy calculator against a rule, scores "
            "distributions five ways and feeds a utility monster, prices Singer's argument, runs a world of promises "
            "and tests maxims for universalizability and consent, ranks outcomes agent-relatively, sorts trolley cases by double "
            "effect, runs Taurek's lotteries, aggregates claims partially, searches every weighting of reasons, and "
            "computes expected choiceworthiness under moral uncertainty and the value of moral information. "
            "<bookmark mark='b'/>And the Wall has its thirty fifth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[35], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $W = \min(\mathbb{E}u_1, \mathbb{E}u_2)$ violates the vNM independence axiom.",
            r"Find a distribution that maximin ranks above another although both totals and priority sums are lower.",
            r"In the promise world, \ find the largest share of liars for which lending never stops.",
            r"Write a maxim that the universal law test forbids though it is harmless, \ and explain why.",
            r"For what agent-relative weight $k$ does the constraint against killing one to save $n$ hold?",
            r"Show that range normalization can reverse a verdict of variance normalization.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>The ex-ante egalitarian and "
            "the independence axiom; when maximin disagrees with sums and priority; the largest share of liars a "
            "world of promises survives; a harmless maxim the test forbids; the weight that reproduces a constraint; "
            "and two normalizations that disagree. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"lives that may or may not exist; \ fanaticism; \ the far future", [36]),
            (r"what moral claims mean, \ and whether they can be true", [37]),
            (r"justice as fairness; \ the difference principle", [38]),
            (r"aggregating votes as Harsanyi aggregated utilities", [39]),
            (r"fairness criteria for algorithms; \ machines that weigh lives", [41]),
            (r"whose values to align a reasoner with, \ under moral uncertainty", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 36, \textit{Weighing Lives}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Lives that may or may not exist, fanaticism and the far "
            "future, in Part 36. What moral claims mean, and whether they can be true, in Part 37. Justice as "
            "fairness and the difference principle, in Part 38. Aggregating votes as Harsanyi aggregated "
            "utilities, in Part 39. Fairness criteria for algorithms, in Part 41. And whose values to align a "
            "reasoner with, under moral uncertainty, in Part 42. <bookmark mark='b'/>Next, Part 36: weighing lives."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kagan, \textit{Normative Ethics} (1998)",
             r"Kant, \textit{Groundwork} (1785); \ Parfit, \textit{On What Matters} (2011)",
             r"Scanlon, \textit{What We Owe to Each Other} (1998); \ Hursthouse, \textit{On Virtue Ethics} (1999)",
             r"MacAskill, Bykvist and Ord, \textit{Moral Uncertainty} (2020); \ Van Norden (2011)"],
            [r"Aristotle; Mencius; Bentham 1789; Constant and Kant 1797; Mill 1863; Sidgwick 1874; Ross 1930",
             r"Harsanyi 1955; Anscombe 1958; Diamond 1967; Foot 1967; Atkinson 1970; Sen 1973; Darley and Batson 1973",
             r"Nozick 1974; Thomson 1976, 1985, 2008; Gilligan 1982; Scheffler 1982; Noddings 1984; Korsgaard 1985, 1986",
             r"Singer 1972; Smart and Williams 1973; Rachels 1975; Taurek 1977; Hare 1981; Kagan 1988; Quinn 1989",
             r"Parfit 1984, 1991; Dreier 1993; Herman 1993; Harman 1999; Hooker 2000; Murphy 2000; Doris 2002",
             r"Williams 1976; Wolf 1982; Elster 1983; Railton 1984; Nussbaum 2000; Dancy 2004; Timmermann 2004",
             r"O'Neill 1985; Held 2006; McKeever and Ridge 2006; Korsgaard 2018",
             r"Bostrom 2009; Greene et al. 2009; De Brigard 2010; Portmore 2011; Voorhoeve 2014",
             r"Awad et al. 2018; Newberry and Ord 2021; Bourget and Chalmers 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
