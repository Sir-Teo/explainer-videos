from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"the white horse: \ `is' as identity or inclusion; \ the Mohists' names; \ Mill",
            r"Frege: \ sense and reference; \ three descriptions of one point, \ computed",
            r"Russell's descriptions and their scopes; \ Strawson's gaps; \ Donnellan's two uses",
            r"Kripke: \ rigid names, \ Gödel and Schmidt, \ chains of use; \ Twin Earth; \ Burge",
            r"Kaplan's character and content; \ the two-dimensional matrix",
            r"Tarski, \ Davidson and Foster; \ Montague's types and $\lambda$; \ a parser, \ built",
            r"generalized quantifiers: \ 512 of 65\,536; \ `most' is not first-order",
            r"intensions; \ belief reports \ (the Wall); \ donkeys, \ dynamics, \ machines",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The white horse, and the two readings of is, with the "
            "Mohist and Millian theories of names. <bookmark mark='b'/>Frege's sense and reference, with his medians "
            "computed. <bookmark mark='c'/>Russell's descriptions and the scope of negation, Strawson's gaps and "
            "Donnellan's two uses. <bookmark mark='d'/>Kripke's rigid names and causal chains, Twin Earth, and "
            "Burge's arthritis. <bookmark mark='e'/>Kaplan's indexicals and the two-dimensional matrix. "
            "<bookmark mark='f'/>Truth-conditional semantics, from Tarski to Montague, ending in a working parser. "
            "<bookmark mark='g'/>Generalized quantifiers, conservativity counted, and a game that proves most is not "
            "first-order. <bookmark mark='h'/>And intensions, belief reports, this part's brick in the Wall, donkey "
            "sentences, and meaning in machines."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{semantics.medians, descriptions}", r"Frege's point; \ Russell's scopes"),
                (r"\texttt{semantics.rigidity, two\_d, kaplan}", r"names, \ worlds, \ contexts"),
                (r"\texttt{semantics.t\_theory, foster}", r"T-sentences, \ derived"),
                (r"\texttt{semantics.reduce, interpret}", r"$\lambda$-terms; \ the Heim--Kratzer parser"),
                (r"\texttt{semantics.quantifiers, ef\_most}", r"conservativity; \ the game"),
                (r"\texttt{semantics.dpl, donkeys}", r"dynamic predicate logic"),
                (r"\texttt{semantics.to\_sql, nli\_suite}", r"semantics, \ executed"),
                (r"\texttt{quantum.*}, \ \texttt{spacetime.*}, \ \texttt{fol.*}, \ \dots", r"Parts 1--26")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_semantics.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=27, current=27).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, semantics. <bookmark mark='a'/>It computes Frege's medians and Russell's "
            "scopes, rigid designation across worlds, Kaplan's contexts and two-dimensional matrices, derives "
            "T-sentences, reduces lambda terms, interprets trees by Heim and Kratzer's rules, checks conservativity, "
            "plays Ehrenfeucht–Fraïssé games, runs dynamic predicate logic, and compiles meanings to SQL. "
            "<bookmark mark='b'/>And the Wall has its twenty-seventh brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[27], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Give Russell's analysis of `the author of \textit{Waverley} is not Scott' in both scopes; \ find a model "
            r"separating them.",
            r"Draw the two-dimensional matrix for `I am here now', \ with contexts as rows.",
            r"Write a truth theory for `and', `or' and `not' that Foster's trick cannot fool. \ What did you add?",
            r"Interpret `no student read every book' in both scopes; \ build a model where they differ.",
            r"Prove that `at least half' is conservative \ and right-upward but neither way on the left.",
            r"Show by an Ehrenfeucht--Fraïssé game that `there is an even number of $P$' is not first-order.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Russell's scopes for a "
            "negated identity; the matrix for I am here now; a truth theory Foster cannot fool; a scope ambiguity "
            "with no and every; a conservativity proof; and an Ehrenfeucht–Fraïssé game for parity. Pause here, and "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"meaning as use; \ rule-following; \ speech acts", [28]),
            (r"content, \ externalism and the mind", [30, 31]),
            (r"belief, \ knowledge and their reports", [11, 12]),
            (r"language models and what they mean", [41, 42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 28, \textit{Meaning in Use}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Meaning as use, rule-following and speech acts, in Part 28. "
            "Externalism and the contents of the mind, in Parts 30 and 31. Belief and knowledge, which Parts 11 and "
            "12 built, now with their reports. And language models and what their words mean, in Parts 41 and 42. "
            "<bookmark mark='b'/>Next, Part 28: meaning in use."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Lycan, \textit{Philosophy of Language} (3rd ed., 2019); \ Kripke, \textit{Naming and Necessity} (1980)",
             r"Heim and Kratzer, \textit{Semantics in Generative Grammar} (1998); \ Gamut, \textit{Logic, Language, "
             r"and Meaning} (1991)",
             r"Peters and Westerståhl, \textit{Quantifiers in Language and Logic} (2006)",
             r"Speaks, `Theories of Meaning', \textit{Stanford Encyclopedia}"],
            [r"Mill 1843; Frege 1892; Russell 1905; Tarski 1933; Carnap 1947; Strawson 1950; Searle 1958",
             r"Geach 1962; Hintikka 1962; Donnellan 1966; Davidson 1967; Montague 1970; Evans 1973; Putnam 1975",
             r"Foster 1976; Kaplan 1977; Burge 1979; Kripke 1979; Barwise and Cooper 1981; Kamp 1981; Heim 1982",
             r"Keenan and Stavi 1986; Salmon 1986; Crimmins and Perry 1989; Groenendijk and Stokhof 1991",
             r"Schlenker 2003; Lake and Baroni 2018; Yu et al. 2018; Yanaka et al. 2019; Berglund et al. 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
