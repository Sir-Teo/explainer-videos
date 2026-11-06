from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Eubulides, \ the Mohists, \ Bradwardine and Buridan",
            r"Tarski: \ the T-schema, \ self-reference, \ classical logic; \ the hierarchy; \ Nixon and Jones",
            r"Grelling, \ Richard, \ Berry; \ Priest's inclosure schema",
            r"Kripke's fixed points, \ built; \ grounded, ungrounded, paradoxical; \ revenge \ (the Wall)",
            r"revision sequences; \ Curry; \ Yablo's staircase; \ gluts and LP",
            r"the Price List; \ TB, CT, KF, FS; \ correspondence and deflation",
            r"the surprise exam, \ the knower, \ Moore's paradox",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The liar's history, from Eubulides and the Mohists to "
            "the medieval schools. <bookmark mark='b'/>Tarski's three ingredients, and his hierarchy, and why it "
            "does not fit how we talk. <bookmark mark='c'/>The liar's family, and the pattern that unites it. "
            "<bookmark mark='d'/>Kripke's fixed points, built and run, and the revenge that stalks them. "
            "<bookmark mark='e'/>Revision, Curry, Yablo's staircase, and true contradictions. "
            "<bookmark mark='f'/>The Price List, the formal theories of truth, and what truth is. "
            "<bookmark mark='g'/>And the paradoxes of knowledge and belief."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{truth.value, jump}", r"strong Kleene truth, \ with a truth predicate"),
                (r"\texttt{truth.kripke\_stages, fixed\_points}", r"Kripke's construction; \ every fixed point"),
                (r"\texttt{truth.classify, intrinsic}", r"grounded, ungrounded, paradoxical"),
                (r"\texttt{truth.revision, revision\_verdicts}", r"revision sequences"),
                (r"\texttt{truth.yablo\_solutions, grelling}", r"Yablo; \ Grelling"),
                (r"\texttt{truth.moore}", r"Moore's paradox in KD4"),
                (r"\texttt{arith.*}, \ \texttt{sets.*}, \ \texttt{modal.*}, \ \dots", r"Parts 1--7")]
        lefts = [label(a, font_size=22, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=22, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([0.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_truth.py}", font_size=22, color=GREY_B).to_edge(
            DOWN, buff=0.4)
        w = wall(upto=8, current=8).scale(0.4).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has a module for truth. <bookmark mark='a'/>It evaluates sentences that talk about their "
            "own truth, runs Kripke's construction stage by stage, finds every fixed point and classifies each "
            "sentence, runs revision sequences from every starting guess, solves finite Yablo staircases, sorts "
            "Grelling's adjectives, and checks Moore's paradox in belief logic. <bookmark mark='b'/>And the Wall "
            "has its eighth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[8], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Find all fixed points of the world \ $A$: `$B$ is true', \ $B$: `$A$ is true'. \ Which are classical?",
            r"Show that `the liar is true or the liar is not true' has no value in any Kripke fixed point, \ but is "
            r"stably true in revision theory.",
            r"Give the four steps of the Grelling paradox, \ and say which of the Price List's claims each uses.",
            r"Prove that every finite Yablo sequence has exactly one consistent assignment.",
            r"Derive a contradiction from the knower: \ `this sentence is not known', \ with $K\varphi \to \varphi$ "
            r"known.",
            r"(Essay) Gap, glut, hierarchy or restriction? \ Defend one, \ and answer its revenge.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A pair of truth-tellers, "
            "a sentence that divides Kripke from revision theory, Grelling's paradox on the Price List, Yablo's "
            "finite staircases, the knower, and an essay on the four ways out. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"truth and proof in mathematics; \ what numbers are", [9]),
            (r"knowledge, belief and the knower", [12]),
            (r"vagueness and gaps, \ again", [5, 13]),
            (r"meaning without truth conditions?", [27, 28]),
            (r"agents that reason about their own reasoning", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 9, \textit{What Is Mathematics About?}", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Truth and proof in mathematics, and what numbers are, in "
            "Part 9. Knowledge, belief and the knower, in Part 12. Gaps and degrees, already met in vagueness, in "
            "Parts 5 and 13. Whether meaning needs truth conditions at all, in Parts 27 and 28. And agents that "
            "reason about their own reasoning, in Part 42. <bookmark mark='b'/>Next, Part 9: what is mathematics "
            "about?"
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kripke, `Outline of a theory of truth' (1975); \ Gupta \& Belnap, \textit{The Revision Theory of Truth} "
             r"(1993)",
             r"Field, \textit{Saving Truth from Paradox} (2008); \ Priest, \textit{In Contradiction} (1987, 2006)",
             r"Halbach, \textit{Axiomatic Theories of Truth} (2011); \ Beall, Glanzberg \& Ripley, \textit{Formal "
             r"Theories of Truth} (2018)",
             r"Sorensen, \textit{A Brief History of the Paradox} (2003); \ Cook, \textit{The Yablo Paradox} (2014)"],
            [r"Mohist canon B71; Bradwardine c.\ 1324; Buridan, \textit{Sophismata}; Russell 1908; Grelling \& Nelson "
             r"1908; Richard 1905",
             r"Tarski 1933, 1944; Curry 1942; Moore 1942; O'Connor 1948; Quine 1953; Kaplan \& Montague 1960",
             r"Hintikka 1962; Gupta 1982; Herzberger 1982; McGee 1985; Friedman \& Sheard 1987; Feferman 1991",
             r"Yablo 1993; Priest 1979, 1994, 1997; Shapiro 1998; Ketland 1999, 2005; Chow 1998; Maudlin 2004"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
