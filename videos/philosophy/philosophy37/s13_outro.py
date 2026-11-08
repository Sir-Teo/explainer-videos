from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Hume's law; \ Prior's tea; \ Schurz's pattern on 175,616 models \ (the Wall)",
            r"Moore's open question; \ the naturalistic fallacy; \ water and H$_2$O",
            r"realism, \ natural and not; \ supervenience; \ moral twin earth",
            r"Mackie's error theory; \ companions in guilt; \ the Price List, \ 62\% realist",
            r"Ayer, \ Stevenson, \ Blackburn; \ Frege--Geach; \ norm-world pairs, \ 2 of 8 left",
            r"relativism and its disagreement problem; \ Rawls, \ Korsgaard, \ Street",
            r"Street's dilemma as an analogy: \ 0.83, \ $-0.02$, \ 0.68; \ Haidt; \ Greene",
            r"Mencius and Xunzi; \ reflective equilibrium as MaxSAT, \ and how it moves",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Hume's law, Prior's tea, and Schurz's pattern checked on "
            "a hundred and seventy five thousand models: this part's brick in the Wall. <bookmark mark='b'/>Moore's "
            "open question, the naturalistic fallacy, and water as H two O. <bookmark mark='c'/>Realism, natural and "
            "non-natural, the supervenience challenge, and moral twin earth. <bookmark mark='d'/>Mackie's error "
            "theory, the companions in guilt, and the Price List, with sixty two percent of philosophers realists. "
            "<bookmark mark='e'/>Ayer, Stevenson and Blackburn, the Frege-Geach problem, and Gibbard's norm-world "
            "pairs, two of eight left by the premises. <bookmark mark='f'/>Relativism and its problem of "
            "disagreement, and the constructivists. <bookmark mark='g'/>Street's dilemma as an analogy, with its "
            "three correlations, and the psychology of Haidt and Greene. <bookmark mark='h'/>Mencius and Xunzi, and "
            "reflective equilibrium as an optimization, and how it moves when the weights do."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{metaethics.analyse, schurz\_table}", r"a deontic logic on every small model"),
                (r"\texttt{metaethics.norm\_world\_pairs}", r"Gibbard's semantics"),
                (r"\texttt{metaethics.reflective\_equilibrium}", r"weighted MaxSAT"),
                (r"\texttt{metaethics.debunking}", r"Street's dilemma, \ as an analogy"),
                (r"\texttt{prop.mus\_mcs}", r"the Price List"),
                (r"\texttt{population.*}, \ \texttt{ethics.*}, \ \dots", r"Parts 1--36")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_metaethics.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=37, current=37).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, metaethics. <bookmark mark='a'/>It checks inferences in a logic of ought "
            "on every small model and asks whether their normative parts do any work, builds Gibbard's norm-world "
            "pairs, finds reflective equilibria by weighted MaxSAT, and runs Street's dilemma as an analogy. "
            "<bookmark mark='b'/>And the Wall has its thirty seventh brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[37], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $p \vdash p \vee Oq$ is valid in KD, \ and that $Oq$ can be replaced by any formula.",
            r"Find a countermodel to $Op \vdash p$ with two worlds.",
            r"Show that $Op \to Pp$ is valid in KD but not in K, \ where a world may have no ideal world.",
            r"In the norm-world semantics, \ show that `lying is wrong' and `lying is not wrong' leave no pair in "
            r"common.",
            r"Give weights for which reflective equilibrium keeps D, \ F and H.",
            r"State Mackie's argument from queerness as a valid argument, \ and say which premise you would deny.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Prior's tea in KD; a "
            "countermodel to is from ought; ought implies may, and why it needs the D axiom; contradiction in norm-world "
            "semantics; weights that make the absolutist principle win; and Mackie's queerness as a valid argument. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"justice as a construction: \ the original position", [38]),
            (r"aggregating attitudes: \ voting and Arrow's theorem", [39]),
            (r"aesthetic judgment: \ realism, \ expressivism, \ again", [40]),
            (r"fairness criteria: \ whose values, \ and are they facts?", [41]),
            (r"aligning a reasoner with values it may not share", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 38, \textit{Justice}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Justice as a construction, from the original position, in Part "
            "38. Aggregating attitudes by voting, and Arrow's theorem, in Part 39. Whether judgments of beauty state "
            "facts or express attitudes, in Part 40. Whose values fairness criteria encode, in Part 41. And how to "
            "align a reasoner with values it may not share, in Part 42. <bookmark mark='b'/>Next, Part 38: justice."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Miller, \textit{An Introduction to Contemporary Metaethics} (2013)",
             r"Gibbard, \textit{Thinking How to Live} (2003); \ Schroeder, \textit{Being For} (2008)",
             r"Mackie, \textit{Ethics: Inventing Right and Wrong} (1977); \ Schurz, \textit{The Is-Ought Problem} (1997)",
             r"Street (2006); \ Ivanhoe and Van Norden, \textit{Readings in Classical Chinese Philosophy}"],
            [r"Mencius; Xunzi; Herodotus; Hume 1739; Moore 1903; Ayer 1936; Frankena 1939; Langford 1942",
             r"Stevenson 1944; Goodman 1955; Prior 1960; Geach 1965; Blackburn 1971, 1984, 1993; Harman 1975, 1977",
             r"Daniels 1979; Rawls 1971, 1980; Sturgeon 1985; Boyd 1988; Brink 1989; Gibbard 1990; Horgan and Timmons 1991",
             r"Korsgaard 1996; Unwin 1999; Haidt 2001; Joyce 2001, 2006; Greene et al. 2001; Shafer-Landau 2003",
             r"Dreier 2004; Wong 2006; Cuneo 2007; Copp 2008; Berker 2009; Graham, Haidt and Nosek 2009",
             r"McGuire et al. 2009; Enoch 2010, 2011; Kelly and McGrath 2010; Street 2010; Wielenberg 2010",
             r"Parfit 2011; Greene 2013; MacFarlane 2014; Olson 2014; Streumer 2017; Bourget and Chalmers 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
