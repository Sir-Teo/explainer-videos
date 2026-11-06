from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Plato's three answers; \ the tether; \ justified true belief",
            r"Gettier's cases as models; \ Dharmottara's mirage; \ the lucky arrow",
            r"no false lemmas, \ no defeaters, \ and Zagzebski's recipe",
            r"reliability and its generality problem; \ sensitivity; \ safety; \ the archer",
            r"knowledge first: \ anti-luminosity \ (the Wall), \ and the failure of KK",
            r"the vat, \ closure, \ and four answers; \ the butterfly and the sponge",
            r"foundations, \ coherence, \ infinite chains; \ inside or outside; \ the web; \ asking people",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Plato's three answers, and the definition the "
            "twentieth century took from them. <bookmark mark='b'/>Gettier's cases, as models the Reasoner checks, "
            "and their older cousins. <bookmark mark='c'/>The repairs, and the recipe that defeats them. "
            "<bookmark mark='d'/>Four theories, each a checker on the same cases. <bookmark mark='e'/>Knowledge "
            "first, and two theorems about margins. <bookmark mark='f'/>The skeptic, and the ways to answer her or "
            "live with her. <bookmark mark='g'/>And the shape of justification, the web, and what ordinary people "
            "say."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{knowledge.gettier}", r"Gettier's cases: \ a valid proof, \ a false lemma, \ a near miss"),
                (r"\texttt{knowledge.sensitive, safe}", r"Nozick's and Sosa's conditions over spheres of worlds"),
                (r"\texttt{knowledge.zagzebski}", r"the recipe, \ run"),
                (r"\texttt{knowledge.generality}", r"one look, \ five process types, \ five reliabilities"),
                (r"\texttt{knowledge.luminosity\_series, iterate\_k}", r"margins for error; \ K without KK"),
                (r"\texttt{knowledge.coherence\_flip, revisions}", r"coherence vs.\ truth; \ Quine's web"),
                (r"\texttt{modern.*}, \ \texttt{types.*}, \ \dots", r"Parts 1--10")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 6.0:
                b.width = 6.0
            b.move_to([0.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_knowledge.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=11, current=11).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a module for knowledge. <bookmark mark='a'/>It builds Gettier's cases as first-order "
            "models and checks the proofs inside them; evaluates sensitivity and safety over spheres of worlds; "
            "runs Zagzebski's recipe; computes the reliability of every process type a belief belongs to; applies "
            "margins for error, to a cold morning and an unmarked clock; pits coherence against truth; and finds "
            "every minimal revision of Quine's web. <bookmark mark='b'/>And the Wall has its eleventh brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[11], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"In Gettier's Case II, \ which of Smith's beliefs is the false lemma? \ Build a variant with no false "
            r"lemma that is still not knowledge.",
            r"Apply Zagzebski's recipe to `X = the belief comes from a process that is 99\% reliable'.",
            r"Kripke's barns: \ is `there is a red barn' \textit{safe}? \ Is `there is a barn' safe, \ if believed by "
            r"deduction from it?",
            r"On the unmarked clock with a margin of 2 marks, \ for $p$ = `at most 20', \ where do $Kp$ and $KKp$ end?",
            r"Show that if KK held in a margin model, \ $p$ = `at most 20' could be known nowhere.",
            r"(Essay) Moore, \ Dretske, \ or the contextualist: \ which answer to the skeptic, \ and at what price?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Gettier's lemma; "
            "Zagzebski's recipe; Kripke's barns under safety; the clock with a wider margin; why KK and margins "
            "cannot live together; and an essay on the skeptic. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"epistemic logic, \ common knowledge, \ testimony", [12]),
            (r"degrees of belief, \ the lottery, \ coherence", [13]),
            (r"revising beliefs, \ conditionals", [14]),
            (r"induction, \ and the web in science", [15, 18]),
            (r"reference, \ and Putnam's externalism", [27]),
            (r"what a machine could know", [30]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 12, \textit{Knowledge Among Many}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                       buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Knowledge in groups, common knowledge and testimony, in Part "
            "12. Degrees of belief, and the lottery, in Part 13. Revising beliefs, in Part 14. Induction and Quine's "
            "web in science, in Parts 15 and 18. Reference, and Putnam's externalism, in Part 27. And what it would "
            "mean for a machine to know, in Part 30. <bookmark mark='b'/>Next, Part 12: knowledge among many."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Plato, \textit{Theaetetus}, \textit{Meno}; \ Pritchard, \textit{What Is This Thing Called Knowledge?}",
             r"Williamson, \textit{Knowledge and Its Limits} (2000); \ Nozick, \textit{Philosophical Explanations} "
             r"(1981), ch.\ 3",
             r"Sosa, \textit{A Virtue Epistemology} (2007); \ DeRose, \textit{The Case for Contextualism} (2009)",
             r"Olsson, \textit{Against Coherence} (2005); \ Nagel, \textit{Knowledge: A Very Short Introduction} "
             r"(2014)"],
            [r"Gettier 1963; Clark 1963; Lehrer and Paxson 1969; Dretske 1970; Goldman 1976, 1979; BonJour 1980",
             r"Lehrer and Cohen 1983; Lehrer 1990; DeRose 1992; Zagzebski 1994; Lewis 1996; Conee and Feldman 1998",
             r"Sosa 1999; Weinberg, Nichols and Stich 2001; Bovens and Hartmann 2003; Pritchard 2012; Greco 2010",
             r"Moore 1939; Quine 1951; Putnam 1968, 1981; Nagel et al.\ 2013; Machery et al.\ 2017; Cova et al.\ 2021"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
