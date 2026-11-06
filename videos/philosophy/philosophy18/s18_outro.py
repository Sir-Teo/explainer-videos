from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"the Vienna Circle and Church's trivialization; \ Hempel, \ the flagpole, \ statistical relevance",
            r"Newton's moon test; \ unification and mechanism",
            r"Kuhn's revolutions \ (a cascade); \ Lakatos's Neptune and Vulcan; \ Feyerabend and Laudan",
            r"underdetermination: \ two Newtonian worlds; \ the Duhem problem at OPERA; \ Quine's web",
            r"no miracles and its base rate; \ Laudan's list; \ the realism trilemma \ (the Wall)",
            r"structural realism and Fresnel's equations; \ constructive empiricism; \ Hacking",
            r"reduction and multiple realizability; \ the Ising model renormalized; \ universality",
            r"idealization; \ demarcation; \ inductive risk; \ BACON and AI scientists",
        ]
        card = objectives_card(items, title=r"What we built", font_size=23)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Verificationism and its collapse under Church's "
            "argument; Hempel's laws and the counterexamples to them. <bookmark mark='b'/>Unification, with "
            "Newton's moon test, and mechanisms. <bookmark mark='c'/>Kuhn's revolutions, with a toy cascade, and "
            "the methodologies of his critics. <bookmark mark='d'/>Underdetermination, from Newton's absolute space "
            "to a loose cable at OPERA. <bookmark mark='e'/>The no-miracles argument, its base rate, and the "
            "history of failed theories: this part's brick in the Wall. <bookmark mark='f'/>Structural realism and "
            "constructive empiricism. <bookmark mark='g'/>Reduction and emergence, with the Ising model "
            "renormalized. <bookmark mark='h'/>And models, demarcation, values, and machines that discover."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{science.church\_ayer, flagpole, moon\_test}", r"meaning; \ explanation"),
                (r"\texttt{science.kuhn\_toy, galilean\_twins}", r"revolutions; \ equivalence"),
                (r"\texttt{science.no\_miracles, meta\_induction, fresnel}", r"realism"),
                (r"\texttt{science.ising\_sw, block\_spin, rg\_flow, onsager\_m}", r"emergence"),
                (r"\texttt{science.kinetic\_temperature, pendulum\_idealization}", r"reduction; \ models"),
                (r"\texttt{science.inductive\_risk, bacon}", r"values; \ discovery"),
                (r"\texttt{causal.*}, \ \texttt{stats.*}, \ \dots", r"Parts 1--17")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_science.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=18, current=18).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, science. <bookmark mark='a'/>It checks Church's entailments, derives "
            "flagpoles and moons, runs the toy revolution and two Newtonian worlds, computes no-miracles posteriors "
            "and Fresnel's equations, samples and coarse-grains the Ising model against Onsager's exact answer, "
            "recovers temperature from molecules, measures how false the pendulum is, sets thresholds under "
            "inductive risk, and rediscovers Kepler's law. <bookmark mark='b'/>And the Wall has its eighteenth "
            "brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[18], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that Church's $D$ is not entailed by $O_1, O_2, O_3$ alone, \ so it is not itself an observation.",
            r"State the flagpole as a Woodward intervention. \ Which variable can be set, \ and which follows?",
            r"With $P(S \mid T) = 0.9$ and $P(S \mid \lnot T) = 0.1$, \ what base rate makes $P(T \mid S) = 1/2$?",
            r"Show that a Galilean boost leaves Newton's equations for two bodies unchanged.",
            r"Coarse-grain a $9 \times 9$ checkerboard by $3 \times 3$ majority. \ What do you get, \ and why?",
            r"In the inductive-risk model, \ find the threshold when the two costs are equal and $P(\text{toxic}) = 1/2$.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Church's sentence; the "
            "flagpole as an intervention; the base rate that makes success a coin flip; Galilean invariance; a "
            "checkerboard coarse-grained; and a threshold under inductive risk. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"mechanisms and explanation in biology", [19]),
            (r"laws of nature and objective chance", [24]),
            (r"absolute space; \ symmetry and equivalence", [25]),
            (r"realism about the wavefunction; \ indistinguishable particles", [26]),
            (r"multiple realizability; \ minds and machines", [30]),
            (r"inductive risk and fair algorithms", [41]),
            (r"AI scientists; \ evaluating what machines know", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 19, \textit{Life}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Mechanisms and explanation in biology, in Part 19. Laws of "
            "nature and chance, in Part 24. Absolute space and symmetry, in Part 25. Realism about quantum theory, "
            "in Part 26. Multiple realizability, in Part 30. Inductive risk and fair algorithms, in Part 41. And "
            "machines that do science, in the finale. <bookmark mark='b'/>Next, Part 19: life."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Godfrey-Smith, \textit{Theory and Reality} (2003, 2021); \ Salmon, \textit{Four Decades of Scientific "
             r"Explanation} (1989)",
             r"Kuhn, \textit{The Structure of Scientific Revolutions} (1962); \ van Fraassen, \textit{The Scientific "
             r"Image} (1980)",
             r"Psillos, \textit{Scientific Realism} (1999); \ Batterman, \textit{The Devil in the Details} (2002)",
             r"Douglas, \textit{Science, Policy, and the Value-Free Ideal} (2009); \ Weisberg, \textit{Simulation and "
             r"Similarity} (2013)"],
            [r"Hempel and Oppenheim 1948; Church 1949; Quine 1951; Rudner 1953; Nagel 1961; Putnam 1967, 1975",
             r"Lakatos 1970; Friedman 1974; Laudan 1977, 1981, 1983; Kitcher 1981; Hacking 1983; Worrall 1989",
             r"Ladyman 1998; Machamer, Darden and Craver 2000; Magnus and Callender 2004; Stanford 2006",
             r"Langley 1978; Pigliucci and Boudry 2013; Fahrbach 2011; Sullivan 2022"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
