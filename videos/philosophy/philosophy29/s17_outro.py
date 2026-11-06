from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Brentano's intentionality; \ Twardowski, \ Meinong; \ Husserl's reduction and noema",
            r"a cube from 4000 viewpoints; \ free variation of 5000 triangles \ (an analogy)",
            r"the living present: \ Husserl's diagram; \ 120 melodies, \ three presents",
            r"Heidegger: \ being-in-the-world, \ the hammer, \ care; \ Dreyfus and the limits of rules",
            r"the frame problem: \ axioms counted, \ Dennett's robots planned \ (the Wall; \ a Price List)",
            r"Merleau-Ponty; \ 4E cognition; \ Braitenberg's vehicles; \ Sartre, \ Beauvoir, \ Fanon",
            r"Kierkegaard, \ Nietzsche: \ a reversible world returns; \ Simmel's wheels do not",
            r"Gadamer's circle; \ Saussure's vectors rotated; \ Derrida; \ Foucault, \ Habermas, \ Kyoto",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Brentano's thesis that the mental is the intentional, "
            "its critics, and Husserl's method. <bookmark mark='b'/>A cube never seen whole, and free variation, "
            "computed as an analogy. <bookmark mark='c'/>The living present, with Husserl's diagram and three models "
            "of the present tested on every five-note melody. <bookmark mark='d'/>Heidegger's being-in-the-world, "
            "and Dreyfus's critique of rules. <bookmark mark='e'/>The frame problem, with its axioms counted and "
            "Dennett's robots planned, this part's brick in the Wall and its Price List. "
            "<bookmark mark='f'/>The lived body, embodied cognition and Braitenberg's vehicles; and the "
            "existentialists. <bookmark mark='g'/>Kierkegaard and Nietzsche, and the eternal return tested on a "
            "reversible world and on Simmel's wheels. <bookmark mark='h'/>And interpretation, structure and "
            "difference with word vectors rotated, power, communication, and the Kyoto school."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{phenomenology.adumbrations, eidetic}", r"profiles; \ variation"),
                (r"\texttt{phenomenology.retention, husserl\_diagram}", r"the living present"),
                (r"\texttt{phenomenology.axiom\_counts, robots}", r"the frame problem"),
                (r"\texttt{phenomenology.braitenberg}", r"bodies in a world"),
                (r"\texttt{phenomenology.recurrence}", r"the eternal return"),
                (r"\texttt{phenomenology.hermeneutic, procrustes}", r"circle; \ structure"),
                (r"\texttt{phenomenology.gaming, dictionary}", r"norms; \ deferral"),
                (r"\texttt{pragmatics.*}, \ \texttt{semantics.*}, \ \texttt{fol.*}, \ \dots", r"Parts 1--28")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_phenomenology.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=29, current=29).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, phenomenology. <bookmark mark='a'/>It computes a cube's profiles, "
            "free variation and a retentional present; counts frame axioms and plans for Dennett's robots; drives "
            "Braitenberg's vehicles; runs a reversible world to its return; iterates the hermeneutic circle; "
            "rotates and realigns word vectors; games a threshold; and finds the words a dictionary cannot define "
            "without leaving itself. <bookmark mark='b'/>And the Wall has its twenty-ninth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[29], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that no viewpoint outside a convex polyhedron shows all its faces at once; \ find one that "
            r"shows all but one.",
            r"With decay $\lambda = \tfrac12$, \ show that the retentional present always determines the order of "
            r"distinct notes. \ What if $\lambda = 1$?",
            r"Write successor-state axioms for Dennett's room, \ including the ramification `things on the wagon "
            r"move with it'.",
            r"Show that a second-order cellular automaton $x_{t+1} = f(x_t) \oplus x_{t-1}$ is invertible for every "
            r"$f$.",
            r"In the hermeneutic toy, \ prove that a text of only ambiguous words leaves every prejudice fixed.",
            r"Find the minimum grounding set of a dictionary of your own design; \ when is it a single word?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Faces of a polyhedron seen "
            "at once; why a fading present determines order, and when it does not; successor-state axioms for "
            "Dennett's room; why Fredkin's automata are reversible; a fixed point of the hermeneutic circle; and a "
            "dictionary of your own. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"intentionality naturalized; \ the Chinese room", [30]),
            (r"the first person, \ qualia and the hard problem", [31]),
            (r"freedom, \ after Sartre", [32]),
            (r"deliberation and democracy, \ after Habermas", [39]),
            (r"normalization, \ gaming and fairness", [41]),
            (r"relevance, \ background and aligned machines", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 30, \textit{Mind and Machine}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Brentano's problem, how a physical thing can be about "
            "anything, and the Chinese room, in Part 30. The first person, qualia and the hard problem, in Part 31. "
            "Freedom, in Part 32. Deliberation and democracy, in Part 39. Normalization, gaming and fairness, in "
            "Part 41. And relevance and the background, for machines we want to align, in Part 42. "
            "<bookmark mark='b'/>Next, Part 30: mind and machine."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Moran, \textit{Introduction to Phenomenology} (2000); \ Zahavi, \textit{Husserl's Phenomenology} (2003)",
             r"Dreyfus, \textit{Being-in-the-World} (1991); \textit{What Computers Still Can't Do} (1992)",
             r"Gallagher and Zahavi, \textit{The Phenomenological Mind} (2008); \ Varela, Thompson and Rosch (1991)",
             r"Shanahan, `The Frame Problem', \textit{Stanford Encyclopedia}; \ Heisig, \textit{Philosophers of "
             r"Nothingness} (2001)"],
            [r"D\=ogen 1240; Bentham 1791; Kierkegaard 1843, 1844; Brentano 1874; Nietzsche 1882, 1887; James 1890",
             r"Twardowski 1894; Husserl 1900, 1905, 1913; Simmel 1907; Nishida 1911, 1926; Saussure 1916",
             r"Heidegger 1927, 1929; Carnap 1932; Sartre 1943; Merleau-Ponty 1945; Beauvoir 1947, 1949; Fanon 1952",
             r"Gadamer 1960; Derrida 1967; McCarthy and Hayes 1969; Dreyfus 1972; Foucault 1975; Habermas 1981",
             r"Fodor 1983; Dennett 1984; Braitenberg 1984; Reiter 1991; Clark and Chalmers 1998; Grush 2006"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
