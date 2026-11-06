from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Plato's ladder; \ Republic X; \ Aristotle's mimesis and catharsis; \ Burke",
            r"the comma: \ 531441/524288, \ 23.46 cents; \ equal thirds 14 to 16 cents off",
            r"the dissonance curve: \ dips at 6:5, \ 5:4, \ 4:3, \ 3:2, \ 5:3, \ 2:1; \ they move with timbre",
            r"17 wallpaper groups built, \ 17 names found",
            r"rule 30: \ incompressible to zlib, \ fully learnable; \ interest as progress",
            r"$\varphi$ in 70\% of random buildings; \ Fechner, \ Markowsky",
            r"true judges 0.998; \ prejudice stuck at 0.62 \ (the Wall); \ Kant; \ the sublime",
            r"Brillo boxes; \ van Meegeren; \ \textit{Thaler v. Perlmutter}; \ Hardy; \ Xie He; \ Cook Ding",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Plato's ladder and his case against art, Aristotle's "
            "reply, and Burke's sublime. <bookmark mark='b'/>The Pythagorean comma, twenty three and a half cents, "
            "and equal temperament's thirds, fourteen to sixteen cents off. <bookmark mark='c'/>The dissonance curve, "
            "with the consonances as its dips, moving when the timbre changes. <bookmark mark='d'/>All seventeen "
            "wallpaper groups, built and named. <bookmark mark='e'/>A pattern that a compressor cannot shrink but a "
            "learner masters, and interest as compression progress. <bookmark mark='f'/>The golden ratio found in "
            "seventy percent of random buildings. <bookmark mark='g'/>Hume's true judges converging, prejudice that "
            "does not average out, this part's brick in the Wall, and Kant. <bookmark mark='h'/>Brillo boxes, "
            "forgeries, AI art before the courts, and beauty in proofs, poems and skill."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{aesthetics.tuning}", r"the comma and equal temperament"),
                (r"\texttt{aesthetics.dissonance\_curve}", r"roughness, \ in Sethares's form"),
                (r"\texttt{aesthetics.wallpaper, classify}", r"the 17 plane groups"),
                (r"\texttt{aesthetics.compressibility, compression\_progress}", r"order and interest"),
                (r"\texttt{aesthetics.golden, critics}", r"two tests, \ one an analogy"),
                (r"\texttt{prop.mus\_mcs}", r"the Price List"),
                (r"\texttt{vote.*}, \ \texttt{justice.*}, \ \dots", r"Parts 1--39")]
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
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_aesthetics.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=40, current=40).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, aesthetics. <bookmark mark='a'/>It tunes scales, computes roughness, "
            "generates and classifies the wallpaper groups, measures compression and the progress of a learner, tests "
            "the golden ratio, and simulates a panel of critics. <bookmark mark='b'/>And the Wall has its fortieth "
            "brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[40], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that no power of $3/2$ equals a power of $2$.",
            r"How many cents is the syntonic comma $81/80$?",
            r"Explain why two harmonic tones at ratio 3:2 share every second partial of the lower tone.",
            r"Which wallpaper groups have no mirrors and no glides?",
            r"Why does averaging remove a critic's noise but not a shared prejudice?",
            r"State the paradox of taste as an inconsistent triad, \ and say which claim Kant denies.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Why the circle of fifths "
            "cannot close; the size of another comma; why a fifth sounds smooth; the groups with no reflections at "
            "all; why averaging cannot cure prejudice; and the paradox of taste as a Price List. Pause here, and try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"machines that judge: \ whose standard, \ and can it be fair?", [41]),
            (r"aligning a reasoner with human taste and values", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 41, \textit{Fair Machines}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Machines now judge images, essays and applicants, and Part 41 "
            "asks by whose standard, and whether they can be fair. Part 42 asks how a reasoner can be aligned with "
            "human taste and values that, as Hume saw, no rule captures. <bookmark mark='b'/>Next, Part 41: fair "
            "machines."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Gaut and Lopes (eds), \textit{The Routledge Companion to Aesthetics}; \ Kant, \textit{Critique of the Power "
             r"of Judgment} (1790)",
             r"Hume, `Of the Standard of Taste' (1757); \ Sethares, \textit{Tuning, Timbre, Spectrum, Scale}",
             r"Conway, Burgiel and Goodman-Strauss, \textit{The Symmetries of Things} (2008)",
             r"Danto, \textit{The Transfiguration of the Commonplace} (1981); \ Li Zehou, \textit{The Path of Beauty} (1981)"],
            [r"Plato, \textit{Symposium}, \textit{Republic}, \textit{Hippias Major}; Aristotle, \textit{Poetics}; Plotinus; "
             r"Aquinas; Xie He; \textit{Zhuangzi}",
             r"Zhu Zaiyu 1584; Kepler 1619; Hutcheson 1725; Burke 1757; Helmholtz 1863; Fechner 1876; Fedorov 1891; "
             r"Tolstoy 1897",
             r"Wang Guowei 1908; Bell 1914; Duchamp 1917; Pólya 1924; Birkhoff 1933; Collingwood 1938; Hardy 1940; "
             r"Eysenck 1941",
             r"Weyl 1952; Weitz 1956; Sibley 1959; Danto 1964; Plomp and Levelt 1965; Goodman 1968; Walton 1970; "
             r"Berlyne 1971",
             r"Dickie 1974; Dutton 1979; Levinson 1979; McManus 1980; Csíkszentmihályi 1990; Markowsky 1992; "
             r"Sethares 1993",
             r"Green 1995; Gaut 2000; Zangwill 2001; Grünbaum 2006; Schmidhuber 2009; McDermott et al. 2010, 2016",
             r"Newman and Bloom 2012; Zeki et al. 2014; US Copyright Office 2023; \textit{Thaler v. Perlmutter} 2023, "
             r"2025"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
