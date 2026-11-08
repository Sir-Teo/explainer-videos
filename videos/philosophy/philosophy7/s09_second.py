from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Second(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The second incompleteness theorem", r"Can arithmetic prove itself consistent?",
                            lit=(1931,), part=PART)
        with self.voiceover("Chapter eight. The second incompleteness theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.statement()
        self.conditions()
        self.modal()
        self.brick()

    def statement(self):
        con = MathTex(r"\mathrm{Con}(\mathrm{PA}) \ := \ \lnot\,\mathrm{Prov}(\ulcorner 0 = 1 \urcorner)",
                      font_size=46, color=PROV).move_to([0, 2.2, 0])
        steps = VGroup(
            label(r"the first half of Chapter 7 was an argument: \ if PA is consistent, \ $G$ is not provable",
                  font_size=26),
            label(r"that argument can be carried out \textit{inside} PA:", font_size=26),
            MathTex(r"\mathrm{PA} \vdash \mathrm{Con}(\mathrm{PA}) \to \lnot\,\mathrm{Prov}(\ulcorner G \urcorner)"
                    r"\quad \text{that is,} \quad \mathrm{PA} \vdash \mathrm{Con}(\mathrm{PA}) \to G", font_size=34,
                    color=GOAL),
            label(r"so if PA proved $\mathrm{Con}(\mathrm{PA})$, \ it would prove $G$: \ impossible", font_size=28,
                  color=BAD)).arrange(DOWN, buff=0.35).next_to(con, DOWN, buff=0.6)
        thm = theorem_card(r"Gödel II", r"a consistent theory containing PA cannot prove its own consistency",
                           width=10.0, font_size=26).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The second theorem comes almost for free. <bookmark mark='a'/>Write Con of PA for the sentence that "
            "zero equals one is not provable: PA is consistent. <bookmark mark='b'/>The first half of the last "
            "chapter was an argument: if PA is consistent, then G is not provable. <bookmark mark='c'/>That "
            "argument is itself elementary arithmetic, so PA can carry it out. PA proves: if PA is consistent, then "
            "G is not provable, which is to say, then G. <bookmark mark='d'/>So if PA proved its own consistency, it "
            "would prove G, which it cannot. <bookmark mark='e'/>A consistent theory containing PA cannot prove its "
            "own consistency. And since Hilbert's finitary methods can all be formalized in PA, a "
            "finitary proof that PA is consistent is impossible."
        ) as vo:
            self.play(Write(con))
            vo.wait_until("a")
            for mk, st in zip("bcd", (steps[0], VGroup(steps[1], steps[2]), steps[3])):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=DOWN * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(thm))
        self.clear_scene()

    def conditions(self):
        hc = history_card(1939, r"Hilbert \& Bernays; \ Löb (1955)", r"what `provable' must satisfy for the second "
                          r"theorem", width=6.4, color=HIST).to_corner(UL, buff=0.35)
        rows = [(r"D1", r"\text{if } \mathrm{PA} \vdash A \text{, then } \mathrm{PA} \vdash \mathrm{Prov}(\ulcorner A \urcorner)",
                 r"provable things are provably provable"),
                (r"D2", r"\mathrm{Prov}(\ulcorner A \to B \urcorner) \to (\mathrm{Prov}(\ulcorner A \urcorner) \to "
                        r"\mathrm{Prov}(\ulcorner B \urcorner))", r"provability is closed under modus ponens"),
                (r"D3", r"\mathrm{Prov}(\ulcorner A \urcorner) \to \mathrm{Prov}(\ulcorner \mathrm{Prov}(\ulcorner A "
                        r"\urcorner) \urcorner)", r"PA knows D1 holds")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 0.9 - 1.05 * i
            la = label(a, font_size=26, color=NUM).move_to([-6.0, y, 0])
            lb = MathTex(b, font_size=32).move_to([-5.4, y + 0.12, 0], aligned_edge=LEFT)
            lc = label(c, font_size=22, color=GREY_B).move_to([-5.4, y - 0.36, 0], aligned_edge=LEFT)
            tab.add(VGroup(la, lb, lc))
        note = label(r"any provability predicate with these three properties obeys the second theorem",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What exactly must provability satisfy for this to go through? <bookmark mark='a'/>David Hilbert and "
            "Paul Bernays isolated the conditions in 1939, and Martin Löb simplified them in 1955. First: whatever "
            "PA proves, it proves to be provable. <bookmark mark='b'/>Second: provability is closed under modus "
            "ponens. <bookmark mark='c'/>Third: PA can prove the first condition about itself. "
            "<bookmark mark='d'/>Any notion of provability with these three properties falls under the second "
            "theorem. And they should look familiar."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def modal(self):
        d = load("gl")
        head = label(r"Read $\Box$ as `PA proves': \ the logic GL of Part 4", font_size=32, color=CONN).to_edge(
            UP, buff=0.45)
        rows = [(r"D1", r"\text{from } A \text{ infer } \Box A", r"necessitation"),
                (r"D2", r"\Box(A \to B) \to (\Box A \to \Box B)", r"K"),
                (r"D3", r"\Box A \to \Box\Box A", r"4"),
                (r"Löb", r"\Box(\Box A \to A) \to \Box A", r"L")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.6 - 0.62 * i
            tab.add(VGroup(label(a, font_size=24, color=NUM).move_to([-5.6, y, 0]),
                           MathTex(b, font_size=32).move_to([-4.8, y, 0], aligned_edge=LEFT),
                           label(c, font_size=24, color=GREY_B).move_to([0.6, y, 0], aligned_edge=LEFT)))
        g2 = MathTex(r"\lnot\Box\bot \ \to\ \lnot\Box\lnot\Box\bot", font_size=44, color=GOAL).move_to([0, -1.1, 0])
        g2l = label(r"Gödel II: \ `if consistent, then consistency is unprovable'", font_size=24,
                    color=GOAL).next_to(g2, DOWN, buff=0.2)
        chk = label(rf"the Reasoner: \ true at every world of all {d['second']['frames']} finite GL frames with up "
                    rf"to four worlds \ $\checkmark$", font_size=22, color=OK).to_edge(DOWN, buff=0.5)
        assert d["second"]["valid"]
        with self.voiceover(
            "Read the box of modal logic as 'PA proves'. <bookmark mark='a'/>The first condition is the rule of "
            "necessitation; the second is axiom K; the third is axiom four. <bookmark mark='b'/>Add Löb's axiom, "
            "which we met in Part 4 and will prove in Chapter 15, and you have the logic GL, which Robert Solovay "
            "showed in 1976 is exactly the logic of provability in PA. <bookmark mark='c'/>The second "
            "incompleteness theorem becomes a modal formula: if not box falsum, then not box not box falsum. If PA "
            "is consistent, it does not prove that it is. <bookmark mark='d'/>The Reasoner checks it on every "
            "finite GL frame, every irreflexive transitive relation, with up to four worlds: two hundred and "
            "forty-two frames, and it holds at every world."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(Write(g2), FadeIn(g2l))
            vo.wait_until("d")
            self.play(FadeIn(chk))
        self.clear_scene()

    def brick(self):
        w = wall(upto=7, current=7).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(7, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "This is the seventh brick in the Wall. <bookmark mark='a'/>The dream: a complete, consistent theory of "
            "arithmetic that proves its own consistency. The wall: Gödel's two theorems, joined in this part by "
            "Turing's halting problem, Tarski's theorem on truth and Löb's theorem, which share one diagonal "
            "argument. What it forces: truth outruns proof, and certainty about our foundations cannot come from "
            "the foundations alone."
        ) as vo:
            self.play(FadeIn(w))
            self.play(Indicate(w.brick[7], color=P.CONCL, scale_factor=1.08))
            vo.wait_until("a")
            self.play(FadeIn(wc))
        self.wait(1)
        self.clear_scene()
