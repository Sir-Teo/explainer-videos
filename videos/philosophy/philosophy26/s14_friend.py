from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Friend(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Perspectives and Wigner's friend", r"Is a quantum state relative to an observer?",
                            lit=(1996, 2018), part=PART)
        with self.voiceover("Chapter thirteen. Perspectives, and Wigner's friend."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.views()
        self.friend()
        self.test()
        self.fr()

    def views(self):
        head = label(r"Quantum states as perspectives", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"QBism", r"Fuchs, \ Schack, \ Caves: \ a quantum state is an agent's degrees of belief about her future "
                       r"experiences; \ the Born rule is a coherence constraint, \ like Part 13's Dutch books", WAVE),
            (r"relational", r"Rovelli \ (1996): \ states and values are relative to other systems; \ there is no "
                            r"view from nowhere", ALICE),
            (r"Copenhagen", r"Bohr: \ the theory is a tool for describing experiments, \ in classical terms", HIST),
            (r"what they share", r"no measurement problem, \ because no claim that $\psi$ describes the world from "
                                 r"outside", OK),
            (r"what they owe", r"an account of what the world is like, \ if not like $\psi$ says", BAD),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=20)
        with self.voiceover(
            "A fourth family of views makes quantum states perspectival. <bookmark mark='a'/>QBism, developed by "
            "Christopher Fuchs, Rüdiger Schack and Carlton Caves: a quantum state is an agent's degrees of belief "
            "about her own future experiences, and the Born rule is a coherence constraint on those beliefs, like the "
            "Dutch book arguments of Part 13. <bookmark mark='b'/>Carlo Rovelli's relational quantum mechanics: "
            "states and values are relative to other systems, and there is no view from nowhere. "
            "<bookmark mark='c'/>And Bohr's Copenhagen view, on which the theory is a tool for describing "
            "experiments in classical terms. <bookmark mark='d'/>What they share: no measurement problem, because "
            "none of them claims that the wavefunction describes the world from outside. <bookmark mark='e'/>What "
            "they owe: an account of what the world is like, if it is not as the wavefunction says."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def friend(self):
        hc = history_card(1961, r"Eugene Wigner", r"`Remarks on the Mind-Body Question'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        lab = RoundedRectangle(width=4.0, height=2.6, corner_radius=0.2, color=ALICE).move_to([-2.6, -0.8, 0])
        ll = label(r"the friend's sealed lab", font_size=18, color=ALICE).next_to(lab, UP, buff=0.1)
        fr_ = Dot([-3.4, -0.8, 0], radius=0.18, color=ALICE)
        fl = label(r"friend", font_size=17, color=ALICE).next_to(fr_, DOWN, buff=0.1)
        q = Dot([-1.8, -0.8, 0], radius=0.1, color=WAVE)
        ql = label(r"qubit", font_size=17, color=WAVE).next_to(q, DOWN, buff=0.1)
        w = Dot([2.6, -0.8, 0], radius=0.2, color=BOB)
        wl = label(r"Wigner, \ outside", font_size=18, color=BOB).next_to(w, DOWN, buff=0.1)
        rows = stack([(r"the friend measures the qubit, \ and sees a result", ALICE),
                      (r"Wigner, \ outside, \ describes the whole lab by Schrödinger's equation: \ a superposition",
                       BOB),
                      (r"whose description is right? \ both, \ relative to each? \ neither?", BAD)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Eugene Wigner sharpened the issue in 1961. <bookmark mark='a'/>His friend sits in a sealed lab and "
            "measures a qubit. She sees a definite result. <bookmark mark='b'/>Wigner, outside, treats the whole lab, "
            "friend included, as a quantum system obeying Schrödinger's equation, and assigns it a superposition of "
            "the friend seeing zero and the friend seeing one. <bookmark mark='c'/>Whose description is right? "
            "Both, each relative to its holder? Or neither?"
        ) as vo:
            self.play(FadeIn(hc), Create(lab), FadeIn(ll), FadeIn(fr_), FadeIn(fl), FadeIn(q), FadeIn(ql), FadeIn(w),
                      FadeIn(wl))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def test(self):
        d = load("friend")
        head = label(r"Wigner's test", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["p_unitary"] == 1.0 and d["p_collapse"] == 0.5
        eqs = VGroup(MathTex(r"|{+}\rangle\,|\text{ready}\rangle \;\longrightarrow\; \tfrac{1}{\sqrt2}\big(|0\rangle|"
                             r"\text{saw } 0\rangle + |1\rangle|\text{saw } 1\rangle\big)", font_size=32, color=WAVE),
                     MathTex(r"\text{Wigner asks: \ is the pair in } \tfrac{1}{\sqrt2}\big(|0\rangle|\text{saw } 0"
                             r"\rangle + |1\rangle|\text{saw } 1\rangle\big)\text{?}", font_size=30, color=ABS)
                     ).arrange(DOWN, buff=0.4).move_to([0, 1.5, 0])
        hd = [r"\text{if the friend's measurement}", r"P(\text{yes})", r"\text{in %d runs}" % d["shots"]]
        rows = [[label(r"was unitary \ (no collapse)", font_size=22, color=WAVE),
                 MathTex(f"{d['p_unitary']:.1f}", font_size=26), MathTex(f"{d['freq_unitary']:.3f}", font_size=26,
                                                                       color=PART_C)],
                [label(r"collapsed to a definite result", font_size=22, color=ALICE),
                 MathTex(f"{d['p_collapse']:.1f}", font_size=26), MathTex(f"{d['freq_collapse']:.3f}", font_size=26,
                                                                        color=PART_C)]]
        grid = ValueGrid(hd, rows, col_w=[5.0, 1.8, 2.4], cell_h=0.55, font_size=21).move_to([0, -0.6, 0])
        side = stack([(r"the catch: \ Wigner needs control of every atom of the friend", BAD),
                      (r"Proietti et al. \ (2019): \ six photons, \ with photons as the friends", HIST),
                      (r"whether a real observer can be treated this way is what collapse theories deny", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=11.0, buff=0.24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In principle Wigner can test which story is right. <bookmark mark='a'/>Let the friend measure a qubit "
            "prepared in plus. If the friend obeys the Schrödinger equation, the qubit and the friend's memory end up "
            "entangled: saw zero with zero, plus saw one with one. <bookmark mark='b'/>Wigner measures the pair in a "
            "basis that contains exactly that entangled state. <bookmark mark='c'/>If the friend's measurement was "
            "unitary, Wigner gets yes every time. If it collapsed the state, so that the friend saw a definite "
            "result, Wigner gets yes only half the time. The Reasoner simulates two thousand runs of each. "
            "<bookmark mark='d'/>The catch is the friend. To do this to a person, Wigner would need control over "
            "every one of its atoms. An experiment in 2019, by Massimiliano Proietti and colleagues in Edinburgh, "
            "used single photons as the friends. <bookmark mark='e'/>Whether anything large enough to be an observer "
            "can be treated this way is exactly what collapse theories deny."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def fr(self):
        d = load("fr")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["C"], ["Q"], ["S"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ Frauchiger--Renner \ (2018)")
        positions = [(("S",), r"many worlds", r"the friend's outcome is one of several"),
                     (("C",), r"QBism; \ relational", r"agents' conclusions cannot simply be pooled"),
                     (("Q",), r"collapse theories", r"quantum theory fails for labs, \ and friends")]
        with self.voiceover(
            "In 2018 Daniela Frauchiger and Renato Renner built an extended Wigner's friend scenario, with two friends "
            "and two Wigners reasoning about one another, and proved a no-go theorem. <bookmark mark='a'/>Its three "
            "assumptions: quantum theory applies to everything, agents and labs included; an agent may rely on what "
            "another agent, reasoning correctly by the theory, has concluded; and each measurement has a single "
            "outcome for whoever made it. <bookmark mark='b'/>Together they lead to a contradiction. "
            "<bookmark mark='c'/>Many worlds gives up single outcomes. <bookmark mark='d'/>QBists and relationalists "
            "give up the pooling of conclusions: one agent's facts need not be another's. <bookmark mark='e'/>And "
            "collapse theories give up the universal validity of the theory: a lab with a friend in it is big enough "
            "to collapse."
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
