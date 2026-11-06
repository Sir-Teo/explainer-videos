from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Hume's circle; \ Laplace's rule; \ de Finetti's theorem; \ Carnap's $\lambda$",
            r"the Nyāya inference; \ Dignāga's wheel, \ checked; \ the Cārvāka challenge",
            r"the ravens \ (Price List); \ six measures; \ old evidence; \ grue, \ in a network",
            r"Popper; \ Duhem and Quine; \ Miller's flip; \ the best explanation, \ raced",
            r"merging of opinions; \ Gold; \ Putnam's diagonal; \ Kelly's hierarchy and razor",
            r"Solomonoff's universal prior; \ code lengths and MDL",
            r"no free lunch \ (the Wall); \ Reichenbach; \ meta-induction and its regret bound",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Hume's circle, and the first mathematical answers. "
            "<bookmark mark='b'/>The Indian logicians' wheel of reasons, and their own skeptic. "
            "<bookmark mark='c'/>Three paradoxes of confirmation, the third reproduced in a neural network. "
            "<bookmark mark='d'/>Popper, what happened to falsification and to closeness to the truth, and the "
            "race between explanation and conditionalization. "
            "<bookmark mark='e'/>The theory of learning in the limit, which justified Ockham's razor as the shortest "
            "path to the truth. <bookmark mark='f'/>The universal prior, and compression. <bookmark mark='g'/>And "
            "no free lunch, with the two best vindications of induction we have."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{induction.succession, sunrise, hetucakra}", r"Laplace; \ the wheel"),
                (r"\texttt{induction.ravens, measures, grue}", r"confirmation"),
                (r"\texttt{induction.miller\_tichy, explanationist}", r"Popper; \ IBE"),
                (r"\texttt{induction.merging, gold\_adversary, putnam\_diagonal}", r"learning in the limit"),
                (r"\texttt{induction.ockham, solomonoff, mdl\_degree}", r"simplicity"),
                (r"\texttt{induction.no\_free\_lunch, nfl\_slice, meta\_induction}", r"lunch and regret"),
                (r"\texttt{revision.*}, \ \texttt{credence.*}, \ \dots", r"Parts 1--14")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_induction.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=15, current=15).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has one new module, induction. <bookmark mark='a'/>It computes Laplace's rule and "
            "Dignāga's wheel, the Bayesian ravens and six confirmation measures, the Miller and Tichý theorem by "
            "exhaustive search, merging and Gold's adversary, Kelly's retraction game, a toy universal prior, MDL, "
            "the no free lunch average over every world, and the meta-inductor's regret. "
            "<bookmark mark='b'/>And the Wall has its fifteenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[15], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive $(s + 1)/(n + 2)$ from the uniform prior, \ using $\int_0^1 \theta^a (1-\theta)^b\, d\theta = "
            r"\frac{a!\, b!}{(a + b + 1)!}$.",
            r"In the ravens model, \ let $H'$ have 1{,}000 white ravens. \ Recompute both Bayes factors.",
            r"Find $E_1$, $E_2$ that the log likelihood ratio and Christensen's measure rank oppositely.",
            r"Place `all emeralds are grue' and `only finitely many emeralds are blue' in Kelly's hierarchy.",
            r"Prove: \ exponential weights has regret at most $\frac{\ln N}{\eta} + \frac{\eta T}{8}$; \ optimize "
            r"$\eta$.",
            r"No free lunch, \ again: \ if every world's labels depend only on the \textit{last} bit, \ how does "
            r"nearest neighbour do?",
        ], font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Laplace's rule from the "
            "Beta integral; the ravens with different numbers; a new disagreement between measures; grue in Kelly's "
            "hierarchy; the regret bound for exponential weights; and a world in which nearest neighbour meets its "
            "match. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"significance, \ likelihood \ and Bayes factors", [16]),
            (r"learning causes from data", [17]),
            (r"underdetermination \ and scientific realism", [18]),
            (r"laws and chance: \ what makes regularities hold", [24]),
            (r"inductive bias in learning machines", [41, 42]),
            (r"goal misgeneralization: \ grue, \ for agents", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 16, \textit{Evidence by Numbers}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Significance tests, likelihoods and Bayes factors, in Part "
            "16. Learning causes from data, in Part 17. Underdetermination and realism, in Part 18. Laws and "
            "chance, in Part 24. Inductive bias in learning machines, in Parts 41 and 42. And goal "
            "misgeneralization, an agent that learned grue when we meant green, in the finale. "
            "<bookmark mark='b'/>Next, Part 16: evidence by numbers."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Skyrms, \textit{Choice and Chance} (4th ed.\ 2000); \ Howson and Urbach, \textit{Scientific "
             r"Reasoning} (2006); \ Earman, \textit{Bayes or Bust?} (1992); \ Lipton, \textit{Inference to the Best "
             r"Explanation} (2004)",
             r"Kelly, \textit{The Logic of Reliable Inquiry} (1996); \ Schurz, \textit{Hume's Problem Solved} (2019)",
             r"Li and Vitányi, \textit{An Introduction to Kolmogorov Complexity} (4th ed.\ 2019); \ Grünwald, "
             r"\textit{The MDL Principle} (2007)",
             r"Shalev-Shwartz and Ben-David, \textit{Understanding Machine Learning} (2014); \ Matilal, "
             r"\textit{The Character of Logic in India} (1998)"],
            [r"Hume 1748; Laplace 1814; Reichenbach 1938; Hempel 1945; Carnap 1950, 1952; Goodman 1955; Popper 1959",
             r"Blackwell and Dubins 1962; Putnam 1963; Solomonoff 1964; Gold 1967; Good 1967; Miller 1974; Tichý 1974",
             r"Rissanen 1978; Glymour 1980; Salmon 1981; Wolpert 1996; Fitelson 1999; Kelly 2007; Schurz 2008",
             r"de Finetti 1937; Black 1958; Littlestone and Warmuth 1994; Greaves and Wallace 2006; Cesa-Bianchi and "
             r"Lugosi 2006; Douven 2013; Belot 2013; Sterkenburg 2016; Delétang et al.\ 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
