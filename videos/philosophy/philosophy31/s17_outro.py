from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Nagel's bat; \ Block's access and phenomenal consciousness",
            r"the hard problem \ (the Wall); \ Chalmers's map of responses",
            r"Mary's room: \ 3 possibilities, \ 1 left; \ abilities, \ acquaintance, \ concepts",
            r"zombies: \ the 2D matrix for water and pain; \ the Price List",
            r"the explanatory gap; \ phenomenal concepts; \ illusionism; \ 12 bits seen, \ 3.46 said",
            r"Russellian monism and the combination problem",
            r"a workspace that ignites: \ a masking curve; \ blindsight at 77\% with chance confidence",
            r"$\Phi$ by cuts; \ an adder at 0; \ unfolding; \ a T-maze agent; \ Cogitate; \ animals; \ machines",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Nagel's bat, and Block's two kinds of consciousness. "
            "<bookmark mark='b'/>The hard problem, this part's brick in the Wall, and the map of responses to it. "
            "<bookmark mark='c'/>Mary's room, as three possibilities reduced to one, and three ways to deny that "
            "she learns a fact. <bookmark mark='d'/>Zombies, with the two-dimensional matrices for water and for "
            "pain, and the Price List. <bookmark mark='e'/>The explanatory gap, phenomenal concepts, illusionism, "
            "and a self-model that sees twelve bits and can say three and a half. <bookmark mark='f'/>Russell's "
            "intrinsic natures, and the combination problem. <bookmark mark='g'/>A workspace that ignites and "
            "draws a masking curve, and blindsight: seventy seven percent correct, with confidence at chance. "
            "<bookmark mark='h'/>Phi, computed by cutting; an adder with none and lattices with more; the unfolding "
            "argument; an agent that looks before it leaps; the great test of the theories; and the questions of "
            "animals and machines."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{consciousness.two\_d, mary}", r"two dimensions; \ what Mary rules out"),
                (r"\texttt{consciousness.introspection}", r"a self-model's capacity"),
                (r"\texttt{consciousness.workspace}", r"ignition and masking"),
                (r"\texttt{consciousness.metacognition}", r"confidence, \ and blindsight"),
                (r"\texttt{consciousness.phi\_simple}", r"a simplified $\Phi$, \ by cuts"),
                (r"\texttt{consciousness.aaronson, unfolding}", r"two objections, \ computed"),
                (r"\texttt{consciousness.tmaze}", r"active inference"),
                (r"\texttt{consciousness.indicators}", r"fourteen indicators, \ applied"),
                (r"\texttt{mind.*}, \ \texttt{phenomenology.*}, \ \dots", r"Parts 1--30")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_consciousness.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=31, current=31).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, consciousness. <bookmark mark='a'/>It evaluates two-dimensional "
            "matrices and what Mary can rule out, measures a self-model's capacity, runs a workspace that ignites "
            "and an observer with and without a monitor, computes a simplified phi by cutting, checks two "
            "objections to it, and runs an agent that minimizes expected free energy. <bookmark mark='b'/>And the "
            "Wall has its thirty first brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[31], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Extend the 2D matrix to `heat is molecular motion'; \ where do its primary and secondary intensions "
            r"differ?",
            r"In Mary's model, \ what must be true of the possibilities for the ability hypothesis to be right?",
            r"Find the delay at which the workspace ignites on half the trials, \ as a function of the noise.",
            r"Show that a feedforward network has $\Phi = 0$ under the simplified measure, \ for any state.",
            r"Compute $\Phi$ for a 3-by-3 torus of XOR gates in two different states. \ Does it depend on the state?",
            r"Give the T-maze agent an unreliable cue \ (60\%). \ When does it stop looking before it leaps?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A third sentence for the "
            "two-dimensional matrix; what the ability hypothesis needs of Mary's possibilities; the workspace's "
            "half-way delay as the noise changes; a proof that feedforward networks have no phi; phi for a "
            "lattice in two states; and a T-maze agent with a poor cue. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"agents, \ causes and free will", [32]),
            (r"minds that choose under uncertainty", [33]),
            (r"whose welfare counts, \ and how much", [35, 36]),
            (r"machines that decide about people", [41]),
            (r"aligned reasoners, \ and their moral status", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 32, \textit{Free Will}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Agents, causes and free will, in Part 32. Minds that choose "
            "under uncertainty, in Part 33. Whose welfare counts, and how much, in Parts 35 and 36. Machines that "
            "decide about people, in Part 41. And aligned reasoners, and whether they matter morally, in Part 42. "
            "<bookmark mark='b'/>Next, Part 32: free will."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Chalmers, \textit{The Conscious Mind} (1996); \ \textit{The Character of Consciousness} (2010)",
             r"Dennett, \textit{Consciousness Explained} (1991); \ Seth, \textit{Being You} (2021)",
             r"Dehaene, \textit{Consciousness and the Brain} (2014); \ Albantakis et al., `IIT 4.0' (2023)",
             r"Butlin, Long et al., `Consciousness in Artificial Intelligence' (2023); \ Frankish, `Illusionism' "
             r"(2016)"],
            [r"Helmholtz 1867; James 1890; Russell 1927; Nagel 1974; Kirk 1974; Jackson 1982; Levine 1983",
             r"Rosenthal 1986; Weiskrantz 1986; Baars 1988; Lewis 1988; Loar 1990; Block 1995; Chalmers 1995",
             r"Dehaene, Kerszberg and Changeux 1998; Papineau 2002; Tononi 2004; Del Cul et al. 2007",
             r"Balduzzi and Tononi 2008; Friston 2010; Lau and Rosenthal 2011; Graziano 2013; Aaronson 2014; Friston et al. 2015",
             r"Chalmers 2018; Doerig et al. 2019; Birch et al. 2021; Long, Sebo et al. 2024; Cogitate 2025"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
