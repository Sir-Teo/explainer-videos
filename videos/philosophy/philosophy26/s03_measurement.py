from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Measurement(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The measurement problem", r"What happens when we look?", lit=(1935, 1995),
                            part=PART)
        with self.voiceover("Chapter two. The measurement problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.linearity()
        self.cat()
        self.mixtures()
        self.price()

    def linearity(self):
        head = label(r"Apply the theory to the measuring device", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f1 = MathTex(r"|0\rangle|\text{ready}\rangle \;\to\; |0\rangle|\text{reads } 0\rangle", font_size=32,
                     color=CLASS).move_to([0, 1.6, 0])
        f2 = MathTex(r"|1\rangle|\text{ready}\rangle \;\to\; |1\rangle|\text{reads } 1\rangle", font_size=32,
                     color=CLASS).next_to(f1, DOWN, buff=0.3)
        f3 = MathTex(r"\big(a|0\rangle + b|1\rangle\big)|\text{ready}\rangle \;\to\; a\,|0\rangle|\text{reads } "
                     r"0\rangle + b\,|1\rangle|\text{reads } 1\rangle", font_size=32, color=BAD).next_to(f2, DOWN,
                                                                                               buff=0.5)
        rows = stack([(r"a good measuring device: \ its pointer ends up showing the value", WHITE),
                      (r"Schrödinger's equation is linear: \ superpositions in, \ superpositions out", ABS),
                      (r"so the pointer ends in a superposition of both readings", BAD),
                      (r"but every measurement we have ever made showed one reading", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.26).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now treat the measuring device as a quantum system too, as it surely is: it is made of atoms. "
            "<bookmark mark='a'/>A good device starts ready, and if the qubit is zero, its pointer ends up reading "
            "zero; <bookmark mark='b'/>if the qubit is one, it reads one. <bookmark mark='c'/>But Schrödinger's "
            "equation is linear. Feed in a superposition of zero and one, and out comes a superposition of the pointer "
            "reading zero and the pointer reading one. <bookmark mark='d'/>Every measurement anyone has ever made "
            "showed a single reading. Either the theory is incomplete, or its equation is not the whole story, or "
            "there is more to the world than one reading."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(Write(f3), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cat(self):
        hc = history_card(1935, r"Erwin Schrödinger", r"`The Present Situation in Quantum Mechanics'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        box = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.2, color=GREY_B).move_to([-3.0, -0.8, 0])
        atom = Dot([-4.6, -0.3, 0], radius=0.12, color=WAVE)
        al = label(r"atom", font_size=17, color=WAVE).next_to(atom, DOWN, buff=0.1)
        cat_alive = label(r"cat: \ alive", font_size=20, color=OK).move_to([-2.2, -0.3, 0])
        cat_dead = label(r"cat: \ dead", font_size=20, color=BAD).move_to([-2.2, -1.3, 0])
        plus = MathTex(r"\tfrac{1}{\sqrt2}\big(|\text{decayed}\rangle|\text{dead}\rangle + |\text{intact}\rangle"
                       r"|\text{alive}\rangle\big)", font_size=30, color=WAVE).move_to([3.0, 1.0, 0])
        rows = stack([(r"a radioactive atom, \ a Geiger counter, \ a vial of poison, \ a cat", WHITE),
                      (r"after an hour, \ the atom is half decayed, \ half intact", WAVE),
                      (r"by linearity, \ the cat is too", BAD),
                      (r"Schrödinger's point: \ this is absurd, \ so the theory, \ read literally, \ is incomplete",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=5.6, buff=0.3).move_to([3.4, -1.1, 0])
        with self.voiceover(
            "Schrödinger made the point vivid in 1935. <bookmark mark='a'/>Seal a cat in a box with a radioactive "
            "atom, a Geiger counter and a vial of poison that breaks if the counter fires. <bookmark mark='b'/>After "
            "an hour, the atom is in a superposition of decayed and intact. <bookmark mark='c'/>By the linearity we "
            "just saw, so is the counter, the vial, and the cat: dead and alive. <bookmark mark='d'/>Schrödinger did "
            "not think the cat was both. He meant the example as a reductio: read literally and applied to "
            "everything, the theory gives absurd results, so it cannot be the whole story."
        ) as vo:
            self.play(FadeIn(hc), Create(box), FadeIn(atom), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(atom, color=WAVE))
            vo.wait_until("c")
            self.play(FadeIn(cat_alive), FadeIn(cat_dead), Write(plus), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mixtures(self):
        d = load("mixtures")
        head = label(r"Can density matrices dissolve it?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["all_equal_half_I"] and d["reduced"] == [[0.5, 0.0], [0.0, 0.5]]
        eqs = VGroup(MathTex(r"\rho_A = \mathrm{Tr}_B\, |\Psi^-\rangle\langle\Psi^-| = \begin{pmatrix} \tfrac12 & 0 "
                             r"\\ 0 & \tfrac12 \end{pmatrix}", font_size=32, color=WAVE),
                     MathTex(r"= \tfrac12 |0\rangle\langle 0| + \tfrac12 |1\rangle\langle 1|", font_size=32,
                             color=ALICE),
                     MathTex(r"= \tfrac12 |{+}\rangle\langle {+}| + \tfrac12 |{-}\rangle\langle {-}|", font_size=32,
                             color=ALICE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-2.6, 1.2, 0])
        note = label(r"no measurement on $A$ alone can tell these apart", font_size=21, color=GREY_A).next_to(
            eqs, RIGHT, buff=0.5)
        if note.width > 4.2:
            note = wrapped_label(r"no measurement on $A$ alone can tell these apart", 4.2, 21, GREY_A).next_to(
                eqs, RIGHT, buff=0.5)
        pu, te = d["purity"], d["singlet_test"]
        assert pu == {"entangled": 1.0, "mixture": 0.5} and te == {"entangled": 1.0, "mixture": 0.5}
        hd = [r"\text{the pair}", r"\text{purity } \mathrm{Tr}\,\rho^2", r"P(\text{passes the } \Psi^- \text{ test})"]
        rows = [[label(r"entangled, \ $|\Psi^-\rangle$", font_size=22, color=WAVE),
                 MathTex(f"{pu['entangled']:.1f}", font_size=26), MathTex(f"{te['entangled']:.1f}", font_size=26)],
                [label(r"coin-flip mixture of $|01\rangle$, $|10\rangle$", font_size=22, color=ALICE),
                 MathTex(f"{pu['mixture']:.1f}", font_size=26), MathTex(f"{te['mixture']:.1f}", font_size=26)]]
        grid = ValueGrid(hd, rows, col_w=[5.0, 2.8, 3.6], cell_h=0.55, font_size=22).move_to([0, -1.5, 0])
        foot = stack([(r"d'Espagnat: \ an \textit{improper} mixture is not ignorance of a fact", GOAL),
                      (r"Bell \ (1990): \ such answers hold `FAPP', \ for all practical purposes", HIST)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A tempting escape uses density matrices. <bookmark mark='a'/>Take half of an entangled pair and ask for "
            "its state alone. The Reasoner traces out the other half: one half times the identity. "
            "<bookmark mark='b'/>That is exactly the matrix of a coin flip, a particle that is either zero or one, we "
            "know not which. It is also the matrix of a coin flip between plus and minus. <bookmark mark='c'/>No "
            "measurement on that half can tell these apart. So, the thought goes, after a measurement the pointer is "
            "simply in one state or the other, and we are ignorant which. <bookmark mark='d'/>But look at the whole "
            "pair. The entangled pair is pure, with purity one; the coin-flip mixture has purity one half. A joint "
            "test for the entangled state passes every time on the pair, and half the time on the mixture. "
            "<bookmark mark='e'/>Bernard d'Espagnat called the first kind an improper mixture: it is not ignorance "
            "of a fact. John Bell's name for answers like this, in 1990, was FAPP: good for all practical purposes, "
            "and no more."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            self.play(Write(eqs[2]))
            vo.wait_until("c")
            self.play(FadeIn(note))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def price(self):
        d = load("triad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["C"], ["D"], ["L"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the measurement problem")
        positions = [(("C",), r"Bohm \ (1952)", r"add particles with positions: \ the wavefunction is not the "
                                                r"whole story"),
                     (("L",), r"GRW \ (1986)", r"add random collapses to the equation"),
                     (("D",), r"Everett \ (1957)", r"every outcome happens, \ on its own branch")]
        with self.voiceover(
            "Tim Maudlin put the problem as three claims that cannot all be true. <bookmark mark='a'/>The "
            "wavefunction of a system is complete: it says everything there is to say about it. The wavefunction "
            "always evolves by the linear Schrödinger equation. And measurements always have single, definite "
            "outcomes. <bookmark mark='b'/>The cat shows that the three are inconsistent. <bookmark mark='c'/>Each "
            "of the great interpretations gives up exactly one. David Bohm gives up the first: there are particles "
            "with definite positions, and the wavefunction guides them. <bookmark mark='d'/>Ghirardi, Rimini and "
            "Weber give up the second: the wavefunction occasionally collapses by itself, at random. "
            "<bookmark mark='e'/>Hugh Everett gives up the third: every outcome happens, each in its own branch of "
            "a universal wavefunction. The rest of this part prices the three, after the theorems that close off "
            "the easy fourth option: hidden values that were there all along."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.2)
                self.play(*anims)
        self.clear_scene()
