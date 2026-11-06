from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"states and the Born rule, \ sampled; \ interference; \ uncertainty; \ entanglement",
            r"the measurement problem as Maudlin's three claims: \ Bohm, \ GRW, \ Everett",
            r"EPR; \ CHSH derived, \ all 16 local strategies, \ $2\sqrt2$ and Tsirelson; \ Mermin's device",
            r"the CHSH game: \ $\tfrac34$ against 0.854 \ (the Wall); \ the PR box; \ fifty years of experiments",
            r"GHZ: \ 0 of 64; \ Peres--Mermin: \ 0 of 512; \ 18 vectors: \ 0 of $2^{18}$; \ contextuality",
            r"PBR's measurement table; \ Everett, \ decoherence, \ and branches counted against weighed",
            r"Bohm's trajectories through two slits; \ GRW's hit, \ simulated, \ and its tests",
            r"QBism, \ relational views, \ Frauchiger--Renner; \ the free will theorem; \ Bell at work",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The formalism: the Born rule sampled, interference, "
            "and uncertainty. "
            "<bookmark mark='b'/>The measurement problem as three claims, and the three great theories that each "
            "give one up. <bookmark mark='c'/>EPR, and Bell's inequality, derived and checked on every local "
            "strategy, and Mermin's device. <bookmark mark='d'/>The CHSH game, this part's brick in the Wall; the "
            "PR box; and the experiments. <bookmark mark='e'/>GHZ, the magic square and the eighteen-vector proof, "
            "checked by brute force. <bookmark mark='f'/>The PBR theorem, many worlds, decoherence, and counting "
            "branches. <bookmark mark='g'/>Bohmian trajectories and spontaneous "
            "collapse, simulated. <bookmark mark='h'/>And the perspectival views, Wigner's friend, and what the "
            "theorems buy us."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{quantum.born, interferometer}", r"the Born rule; \ fringes"),
                (r"\texttt{quantum.chsh, chsh\_game}", r"Bell, \ CHSH, \ Tsirelson"),
                (r"\texttt{quantum.mermin\_device, pr\_box}", r"instructions; \ the ladder"),
                (r"\texttt{quantum.ghz, peres\_mermin, cabello18}", r"no-go by brute force"),
                (r"\texttt{quantum.pbr}", r"the wavefunction is real"),
                (r"\texttt{quantum.decoherence}", r"branches stop interfering"),
                (r"\texttt{quantum.bohm}", r"guidance-equation trajectories"),
                (r"\texttt{quantum.grw}", r"spontaneous collapse"),
                (r"\texttt{spacetime.*}, \ \texttt{physlaws.*}, \ \texttt{theism.*}, \ \dots", r"Parts 1--25")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_quantum.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=26, current=26).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, quantum: a small Hilbert-space simulator. <bookmark mark='a'/>It samples "
            "the Born rule, runs an interferometer, enumerates every local strategy for CHSH and plays the game, "
            "checks GHZ, the Peres--Mermin square and Cabello's eighteen vectors by brute force, builds the PBR "
            "measurement, computes decoherence, integrates Bohmian trajectories, and simulates a GRW collapse. "
            "<bookmark mark='b'/>And the Wall has its "
            "twenty-sixth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[26], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $\langle \Psi^- | \sigma_a \otimes \sigma_b | \Psi^- \rangle = -\cos(a - b)$.",
            r"Find CHSH settings giving $|S| = 2.5$. \ What is the classical model nearest to them?",
            r"Prove that shared randomness cannot raise the CHSH game above $\tfrac34$.",
            r"Write the four-particle GHZ argument. \ How many local assignments must fail?",
            r"In the Peres--Mermin square, \ which single constraint can always be met last? \ Why five, \ not six?",
            r"GRW: \ how many particles must a superposition involve to collapse within a microsecond?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Derive the singlet "
            "correlation; tune the CHSH angles; prove that shared randomness does not help classically; extend GHZ "
            "to four particles; understand why the magic square fails by exactly one constraint; and find how big a "
            "superposition GRW collapses within a microsecond. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what a theory refers to: \ sense, \ reference and models", [27]),
            (r"minds, \ machines and observers", [30, 31]),
            (r"free will after Kochen and Specker", [32]),
            (r"deciding in a branching world", [33]),
            (r"fairness and trust in machines", [41]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 27, \textit{Sense and Reference}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                     buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>What a theory's terms refer to, in Part 27. Minds, machines "
            "and observers, in Parts 30 and 31. Free will after Kochen and Specker, in Part 32. Deciding in a "
            "branching world, in Part 33. And trust in machines we cannot inspect, in Part 41. "
            "<bookmark mark='b'/>Next, Part 27, and the start of a new act: sense and reference."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Maudlin, \textit{Philosophy of Physics: Quantum Theory} (2019); \ Albert, \textit{Quantum Mechanics "
             r"and Experience} (1992)",
             r"Bell, \textit{Speakable and Unspeakable in Quantum Mechanics} (1987); \ Wallace, \textit{The Emergent "
             r"Multiverse} (2012)",
             r"Dürr, Goldstein and Zanghì, \textit{Quantum Physics without Quantum Philosophy} (2013)",
             r"Myrvold, `Philosophical Issues in Quantum Theory', \textit{Stanford Encyclopedia}"],
            [r"Born 1926; von Neumann 1932; EPR 1935; Schrödinger 1935; Bohm 1952; Everett 1957; Wigner 1961",
             r"Bell 1964; Kochen and Specker 1967; CHSH 1969; Aspect 1982; GRW 1986; GHZ 1989; Mermin 1990",
             r"Ekert 1991; Maudlin 1995; Rovelli 1996; Deutsch 1999; Conway and Kochen 2006; PBR 2012",
             r"Hensen et al., Giustina et al., Shalm et al. 2015; Frauchiger and Renner 2018; Donadi et al. 2021"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
