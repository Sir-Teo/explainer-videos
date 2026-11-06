from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"the \textit{Tractatus}: \ pictures, \ logical space, \ all 16 truth functions from N",
            r"the \textit{Investigations}: \ the builders, \ language games, \ family resemblance computed",
            r"plus and quus: \ the sceptical paradox and solution \ (the Wall); \ the beetle in the box",
            r"gavagai and proxy functions: \ 300 sentences, \ reference inscrutable; \ charity, \ computed",
            r"Austin's performatives; \ Searle's taxonomy; \ Grice's maxims and implicature",
            r"`some, \ not all': \ Horn scales, \ experiments, \ and the RSA model, \ built",
            r"Lewis signalling games learned by reinforcement; \ partial pooling; \ word vectors",
            r"the octopus and grounding \ (a Price List); \ two probes; \ pragmatics in machines",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The Tractatus, with every truth function made from one "
            "operation. <bookmark mark='b'/>The Investigations: the builders, language games, and family resemblance, "
            "computed. <bookmark mark='c'/>Plus and quus, the sceptical paradox, this part's brick in the Wall, and "
            "the private language argument. <bookmark mark='d'/>Quine's gavagai and proxy functions, and Davidson's "
            "charity, computed. <bookmark mark='e'/>Speech acts, and Grice's theory of implicature. "
            "<bookmark mark='f'/>Some, not all, derived by the Rational Speech Acts model. <bookmark mark='g'/>"
            "Conventions emerging in signalling games, and meaning as distribution. <bookmark mark='h'/>And the "
            "question whether language models mean, priced, probed and tested."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{pragmatics.operation\_n, family}", r"the \textit{Tractatus}; \ games"),
                (r"\texttt{pragmatics.plus\_quus}", r"the sceptical paradox"),
                (r"\texttt{pragmatics.proxy, gavagai, charity}", r"Quine and Davidson"),
                (r"\texttt{pragmatics.rsa, reference\_game, scalar}", r"rational speech acts"),
                (r"\texttt{pragmatics.signalling}", r"conventions from reinforcement"),
                (r"\texttt{pragmatics.vectors, probe}", r"distribution and its limits"),
                (r"\texttt{semantics.*}, \ \texttt{quantum.*}, \ \texttt{fol.*}, \ \dots", r"Parts 1--27")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_pragmatics.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=28, current=28).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, pragmatics. <bookmark mark='a'/>It generates truth functions by "
            "operation N, checks family resemblance, builds plus and quus, applies proxy functions, plays "
            "interpreter, runs the Rational Speech Acts model, plays signalling games, and builds and probes word "
            "vectors. <bookmark mark='b'/>And the Wall has its twenty-eighth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[28], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that `neither \dots\ nor' alone generates all 16 truth functions of two propositions.",
            r"Define a rival to `plus' that agrees with it on all sums below 1000. \ What fact rules it out?",
            r"Give a proxy function for a model of the natural numbers with `$<$'. \ What is preserved?",
            r"Compute the RSA listener for `some' with 4 cookies and $\alpha = 1$.",
            r"In a 3-state signalling game, \ why is partial pooling an equilibrium?",
            r"Design a corpus in which a probe \textit{can} recover fictionality. \ What did you add?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Generating every truth "
            "function from neither-nor; a rival to plus and what rules it out; a proxy function for the numbers; the "
            "RSA listener for four cookies; why partial pooling is an equilibrium; and a corpus that would let a probe "
            "recover fiction. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"meaning in a lived world: \ phenomenology", [29]),
            (r"minds, \ machines and the Chinese room", [30]),
            (r"qualia and the beetle", [31]),
            (r"games, \ conventions and the social contract", [34]),
            (r"aligning reasoners: \ what is meant, \ not just said", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 29, \textit{Being and Time-Consciousness}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Meaning in a lived world, in Part 29's phenomenology. Minds, "
            "machines and the Chinese room, in Part 30. Qualia and the beetle in the box, in Part 31. Games, "
            "conventions and the social contract, in Part 34. And aligning reasoners with what is meant, not just "
            "said, in Part 42. <bookmark mark='b'/>Next, Part 29: being and time-consciousness."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Wittgenstein, \textit{Tractatus} (1921); \textit{Philosophical Investigations} (1953)",
             r"Kripke, \textit{Wittgenstein on Rules and Private Language} (1982); \ Quine, \textit{Word and Object} "
             r"(1960)",
             r"Davidson, \textit{Inquiries into Truth and Interpretation} (1984); \ Grice, \textit{Studies in the Way "
             r"of Words} (1989)",
             r"Lewis, \textit{Convention} (1969); \ Skyrms, \textit{Signals} (2010)"],
            [r"Saussure 1916; Harris 1954; Austin 1955/1962; Firth 1957; Grice 1957, 1975; Searle 1969, 1975",
             r"Horn 1972; Davidson 1973, 1974; Lewis 1983; Harnad 1990; Brandom 1994; Noveck 2001",
             r"Bott and Noveck 2004; Frank and Goodman 2012; Kao et al. 2014; Goodman and Frank 2016",
             r"Andreas and Klein 2016; Cohn-Gordon et al. 2018; Bender and Koller 2020; Piantadosi and Hill 2022",
             r"Mollo and Millière 2023; Li et al. 2023; Ruis et al. 2023; Hu et al. 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
