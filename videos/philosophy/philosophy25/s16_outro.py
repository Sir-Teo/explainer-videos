from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Newton's bucket, \ computed; \ Leibniz's shifts, \ checked: \ relations cannot see rotation",
            r"Kant's hands: \ orientation by signed area; \ the Möbius strip that swaps them",
            r"the Poincaré disk: \ geodesics, \ angle sums and areas; \ Gauss's 15 arcseconds",
            r"Poincaré's disk world: \ geometry plus physics; \ spacetime structures, \ Newton to Galileo",
            r"relativity: \ tilting simultaneity, \ the invariant interval; \ Reichenbach and Malament",
            r"McTaggart; \ four pictures of time; \ the Rietdijk--Putnam boost, \ computed",
            r"the hole argument \ (the Wall) \ and its Price List; \ best matching, \ built",
            r"Gödel's universe, \ Lewis's grandfather, \ Deutsch's fixed points; \ emergent spacetime",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Newton's bucket and Leibniz's shifts, which showed that "
            "relations cannot see rotation. <bookmark mark='b'/>Kant's hands, and the strip that swaps them. "
            "<bookmark mark='c'/>Hyperbolic geometry in the Poincaré disk. <bookmark mark='d'/>Poincaré's "
            "conventionalism, and the ladder of spacetime structures. <bookmark mark='e'/>Relativity's tilting "
            "simultaneity, and whether simultaneity is a convention. <bookmark mark='f'/>McTaggart, the theories of "
            "time, and the argument from relativity to the block. <bookmark mark='g'/>The hole argument, this part's "
            "brick in the Wall, and the relationalist's best matching. <bookmark mark='h'/>And time travel, with its "
            "paradoxes computed, and a glimpse of spacetime as something emergent."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{spacetime.bucket, shifts}", r"Newton and Leibniz"),
                (r"\texttt{spacetime.incongruent}", r"Kant's hands; \ the Möbius strip"),
                (r"\texttt{spacetime.hyp\_triangle, geodesic}", r"the Poincaré disk"),
                (r"\texttt{spacetime.disk\_world, gauss\_triangle}", r"conventions and measurements"),
                (r"\texttt{spacetime.lorentz, simultaneity, rietdijk\_putnam}", r"relativity"),
                (r"\texttt{spacetime.hole, best\_matching}", r"the hole; \ Barbour"),
                (r"\texttt{spacetime.ctc}", r"Deutsch's time travel"),
                (r"\texttt{physlaws.*}, \ \texttt{theism.*}, \ \texttt{worlds.*}, \ \dots", r"Parts 1--24")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_spacetime.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=25, current=25).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, spacetime. <bookmark mark='a'/>It computes the bucket's paraboloid, "
            "checks the shifts, measures orientation and transports a frame round a Möbius strip, draws geodesics "
            "and triangles in the Poincaré disk, applies Lorentz transformations, builds the hole diffeomorphism, "
            "best-matches configurations, and solves Deutsch's consistency condition for time travel. "
            "<bookmark mark='b'/>And the Wall has its twenty-fifth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[25], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"How fast must a 15 cm bucket spin for the water to rise 10 cm at the wall?",
            r"Show that a rotation of the plane keeps the sign of a polygon's signed area.",
            r"A hyperbolic triangle has angles $30^\circ$, $45^\circ$, $60^\circ$. \ What is its area?",
            r"Find the boost that makes the event $(t, x) = (0.3, 0.5)$ simultaneous with the origin.",
            r"State the hole argument for Newtonian gravity in Galilean spacetime. \ Does it go through?",
            r"Grandfather circuit with a CNOT instead of a NOT: \ find Deutsch's fixed points.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Spin a bucket; prove that "
            "rotations keep orientation; find a hyperbolic triangle's area from its angles; find the boost that "
            "makes an event simultaneous with you; try the hole argument in Newton's world; and solve a new "
            "time-travel circuit. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"quantum theory: \ the fixed stage, \ and what measurement does to it", [26]),
            (r"the lived present: \ Husserl's time-consciousness", [29]),
            (r"free will in a block universe", [32]),
            (r"the long future, \ and its value", [36, 42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 26, \textit{The Quantum Puzzle}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                    buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Quantum theory, its fixed stage, and what measurement does, "
            "in Part 26. The lived present, and Husserl's analysis of time-consciousness, in Part 29. Free will in a "
            "block universe, in Part 32. And the long future and its value, in Parts 36 and 42. <bookmark mark='b'/>Next, Part 26: the quantum puzzle."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Maudlin, \textit{Philosophy of Physics: Space and Time} (2012); \ Earman, \textit{World Enough and "
             r"Space-Time} (1989)",
             r"Huggett (ed.), \textit{Space from Zeno to Einstein} (1999); \ Dainton, \textit{Time and Space} (2nd "
             r"ed., 2010)",
             r"Norton, `The Hole Argument', \textit{Stanford Encyclopedia}; \ Arntzenius, \textit{Space, Time, and "
             r"Stuff} (2012)",
             r"Barbour, \textit{The End of Time} (1999); \ Huggett and Wüthrich, `Emergent Spacetime and Empirical "
             r"(In)coherence' (2013)"],
            [r"Newton 1687; Leibniz and Clarke 1715--16; Kant 1768; Lobachevsky 1829; Bolyai 1832; Riemann 1854",
             r"Poincaré 1902; Einstein 1905, 1915; Minkowski 1908; McTaggart 1908; Reichenbach 1928; Gödel 1949",
             r"Rietdijk 1966; Putnam 1967; Stein 1968; Lewis 1976; Malament 1977; Barbour and Bertotti 1982",
             r"Earman and Norton 1987; Deutsch 1991; Maldacena 1997; Van Raamsdonk 2010; Maldacena and Susskind "
             r"2013"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
