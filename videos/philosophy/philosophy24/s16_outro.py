from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"laws as regularities; \ uranium and gold; \ the best system built, \ in bits",
            r"Armstrong's necessitation and the inference problem; \ powers; \ primitivism",
            r"Humean chance: \ 75\% undermining futures; \ the big bad bug and the New Principle",
            r"determinism defined; \ Norton's dome, \ solved and animated",
            r"the Lorenz exponent, \ forecast horizons, \ and Poincaré's roulette wheel",
            r"Boltzmann's counting; \ the H-theorem; \ Loschmidt and Zermelo",
            r"the Kac ring: \ decay, \ recurrence, \ reversal, \ and a dip at now \ (the Wall)",
            r"the Past Hypothesis, \ Boltzmann brains, \ the Price List; \ Szilard, \ Landauer, \ Toffoli",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Laws as regularities, the two spheres, and Lewis's "
            "best system, built as a contest measured in bits. <bookmark mark='b'/>Laws as relations between "
            "universals, with the inference problem; laws as powers; laws as primitive. "
            "<bookmark mark='c'/>Humean chance, the undermining futures that carry three quarters of the "
            "probability in a small world, the big bad bug, and the New Principle that fixes it. "
            "<bookmark mark='d'/>Determinism, and Norton's dome. <bookmark mark='e'/>Chaos, with its Lyapunov "
            "exponent and forecast horizons, and the roulette wheel that turns determinism into chance. "
            "<bookmark mark='f'/>Boltzmann's entropy, his H-theorem, and the objections of Loschmidt and Zermelo. "
            "<bookmark mark='g'/>The Kac ring, which decays, recurs, reverses, and shows that a typical present is "
            "a dip in entropy: this part's brick in the Wall. <bookmark mark='h'/>And the special beginning, the "
            "Boltzmann brains, the Price List of the arrow, and the thermodynamics of information."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{physlaws.best\_system}", r"simplicity and strength, \ in bits"),
                (r"\texttt{physlaws.undermining, new\_principle}", r"Humean chance and its bug"),
                (r"\texttt{physlaws.norton\_dome}", r"Newton without determinism"),
                (r"\texttt{physlaws.lorenz, arbitrary\_functions}", r"chaos; \ deterministic chance"),
                (r"\texttt{physlaws.boltzmann, h\_theorem, free\_gas}", r"entropy and reversal"),
                (r"\texttt{physlaws.kac\_ring, kac\_both\_ways, recurrence}", r"the arrow in a toy"),
                (r"\texttt{physlaws.szilard, landauer}", r"the price of forgetting"),
                (r"\texttt{theism.*}, \ \texttt{worlds.*}, \ \texttt{persist.*}, \ \dots", r"Parts 1--23")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_physlaws.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=24, current=24).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, physlaws. <bookmark mark='a'/>It scores candidate laws by description "
            "length, computes undermining futures and the New Principle, solves Norton's dome, integrates the "
            "Lorenz system and spins Poincaré's wheel, counts microstates and runs a toy kinetic gas, builds the Kac "
            "ring, and prices Szilard's engine and Landauer's erasure. <bookmark mark='b'/>And the Wall has its "
            "twenty-fourth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[24], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Add a term $0.5\,t^3$ to the falling-body law. \ How many data points before the best system finds it?",
            r"Past: \ 50 heads in 100 tosses. \ What chance do the next 100 tosses give to undermining futures?",
            r"For a dome of height $\propto r^{a}$, \ for which exponents $a$ can the ball start to slide on its own?",
            r"With $\lambda = 0.9$, \ what initial precision forecasts the Lorenz system to time 50?",
            r"Show that a Kac ring with an even number of marks returns to its start after $N$ ticks.",
            r"Szilard's engine with the partition at $\tfrac13$: \ the expected work, \ and the cost of erasing the "
            r"record.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Find how much data the best "
            "system needs to detect a small cubic term; count undermining futures in a bigger world; find which "
            "domes break determinism; price a long Lorenz forecast; prove the Kac ring's early return; and balance "
            "the books of a lopsided Szilard engine. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"relativity, \ the block universe, \ and whether time passes", [25]),
            (r"quantum chance: \ collapse, \ GRW, \ and probability in many worlds", [26]),
            (r"information, \ computation and the mind", [30]),
            (r"determinism and free will: \ the consequence argument", [32]),
            (r"decisions, \ counterfactuals and chance", [33]),
            (r"the long-run future and its value", [36, 42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 25, \textit{Space and Time}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                  buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Relativity, the block universe, and whether time passes, in "
            "Part 25. Quantum chance, collapse and probability in a branching universe, in Part 26. Information and "
            "the mind, in Part 30. Determinism and free will, in Part 32. Decisions, counterfactuals and chance, in "
            "Part 33. And the value of the long-run future, in Parts 36 and 42. <bookmark mark='b'/>Next, Part 25: "
            "space and time."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Armstrong, \textit{What Is a Law of Nature?} (1983); \ Earman, \textit{A Primer on Determinism} (1986)",
             r"Albert, \textit{Time and Chance} (2000); \ Sklar, \textit{Physics and Chance} (1993); \ Price, "
             r"\textit{Time's Arrow and Archimedes' Point} (1996)",
             r"Bird, \textit{Nature's Metaphysics} (2007); \ Maudlin, \textit{The Metaphysics Within Physics} (2007); "
             r"\ Strevens, \textit{Bigger than Chaos} (2003)",
             r"Leff and Rex (eds.), \textit{Maxwell's Demon 2} (2003); \ Kac, \textit{Probability and Related Topics} "
             r"(1959)"],
            [r"Ramsey 1928; Lewis 1973, 1979, 1980, 1983, 1994; Dretske 1977; Tooley 1977; van Fraassen 1989",
             r"Hall 1994; Thau 1994; Loewer 2001; Norton 2003, 2008; Malament 2008; Lorenz 1963",
             r"Boltzmann 1872, 1877, 1895; Loschmidt 1876; Poincaré 1890; Zermelo 1896; Penrose 1979; Popper 1956",
             r"Maxwell 1867; Szilard 1929; Landauer 1961; Bennett 1973, 1982; Fredkin and Toffoli 1982; Bérut et al. "
             r"2012"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
