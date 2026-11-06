from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.koenigsberg()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Wir müssen wissen. \ Wir werden wissen. \ (We must know. \ We will know.)",
                       r"David Hilbert", r"radio address, Königsberg, 8 September 1930", width=10.0,
                       font_size=28).next_to(t, DOWN, buff=0.7)
        with self.voiceover(
            "Part 7 is about the limits of proof. <bookmark mark='a'/>On the eighth of September 1930, in "
            "Königsberg, David Hilbert ended a radio address with six words that are now on his gravestone: we "
            "must know, we will know. <bookmark mark='b'/>For the mathematician, he said, there is no ignorabimus: "
            "no question that must stay unanswered for ever."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.02))
        self.clear_scene()

    def koenigsberg(self):
        day1 = history_card(1930, r"7 September, \ a round table in Königsberg",
                            r"Kurt Gödel, aged 24: \ arithmetic has true sentences it cannot prove", width=6.4,
                            color=HIST)
        day2 = history_card(1930, r"8 September, \ the same city",
                            r"Hilbert: \ `we must know, \ we will know'", width=6.4, color=HIST)
        cards = VGroup(day1, day2).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.6)
        vn = label(r"in the room: \ John von Neumann, \ who saw at once what it meant", font_size=26,
                   color=GREY_A).next_to(cards, DOWN, buff=0.7)
        g = MathTex(r"G \ \leftrightarrow\ \lnot\,\mathrm{Prov}(\ulcorner G \urcorner)", font_size=60,
                    color=SELF).move_to([0, -1.4, 0])
        cap = label(r"a sentence that says of itself: \ `I am not provable'", font_size=28, color=GOAL).next_to(
            g, DOWN, buff=0.4)
        with self.voiceover(
            "The day before, at a round table in the same city, a twenty-four-year-old Kurt Gödel had quietly "
            "announced a theorem. <bookmark mark='a'/>Any consistent formal system strong enough for arithmetic "
            "contains true sentences that it cannot prove. <bookmark mark='b'/>Almost nobody reacted. John von "
            "Neumann did: he spoke with Gödel after the session, and within two months had found a second consequence "
            "himself, only to learn that Gödel had it already. <bookmark mark='c'/>At the heart of the proof is a sentence "
            "that says of itself: I am not provable."
        ) as vo:
            self.play(FadeIn(day1))
            vo.wait_until("a")
            self.play(FadeIn(day2))
            vo.wait_until("b")
            self.play(FadeIn(vn))
            vo.wait_until("c")
            self.play(Write(g), FadeIn(cap))
        self.clear_scene()

    def preview(self):
        goals = VGroup(*[label(t, font_size=28) for t in
                         (r"complete: \ every true sentence is provable",
                          r"consistent, \ and provably so, \ by finite means",
                          r"decidable: \ a procedure settles every question")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45).move_to([-1.2, 0.8, 0])
        head = label(r"Hilbert's three wishes for mathematics", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        who = [r"Gödel I \ (1931)", r"Gödel II \ (1931)", r"Church, \ Turing \ (1936)"]
        crosses = VGroup()
        for gl, w in zip(goals, who):
            c = Cross(scale_factor=0.18, stroke_color=BAD).next_to(gl, LEFT, buff=0.35)
            t = label(w, font_size=24, color=BAD).next_to(gl, RIGHT, buff=0.6)
            crosses.add(VGroup(c, t))
        bricks = label(r"this part's brick in the Wall: \ incompleteness, \ undecidability, \ undefinability, "
                       r"\ Löb", font_size=26, color=P.WALL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Hilbert wanted three things. <bookmark mark='a'/>A formal system for mathematics that is complete, "
            "proving every truth; consistent, and provably so, by methods anyone would accept; and decidable, with "
            "a mechanical procedure that settles every question. <bookmark mark='b'/>Within six years, all three "
            "were gone. Gödel's first theorem took completeness; his second took the proof of consistency; and "
            "Alonzo Church and Alan Turing took decidability. <bookmark mark='c'/>This part builds all of it, "
            "with the Reasoner doing the coding, and lays a brick in the Wall: incompleteness, undecidability, "
            "the undefinability of truth, and Löb's theorem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(gl, shift=RIGHT * 0.15) for gl in goals], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in crosses], lag_ratio=0.6), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(bricks))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Hilbert's program; \ a formal system you can play: \ MIU",
            r"arithmetic, axiom by axiom; \ recursive functions; \ the Chinese remainder theorem",
            r"Gödel numbering, \ live; \ quines and the diagonal lemma",
            r"the first and second incompleteness theorems; \ Rosser; \ provability logic",
            r"Turing machines and busy beavers; \ the Church--Turing thesis; \ Rice",
            r"natural independence; \ Berry and Chaitin; \ Tarski; \ Löb",
            r"minds and machines; \ Gentzen's answer: \ consistency by $\varepsilon_0$",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first Hilbert's program, and a formal system you can play by hand. "
            "<bookmark mark='b'/>Then arithmetic, axiom by axiom, the recursive functions it can express, and an "
            "ancient Chinese theorem that Gödel needed. <bookmark mark='c'/>Then the coding of formulas as numbers, "
            "programs that print themselves, and the diagonal lemma. <bookmark mark='d'/>Then the two "
            "incompleteness theorems, with their logic. <bookmark mark='e'/>Then Turing machines, and the "
            "busy beavers that mark the edge of the knowable. <bookmark mark='f'/>Then independence in ordinary "
            "mathematics, the Berry paradox made exact, Tarski's theorem on truth, and Löb's. "
            "<bookmark mark='g'/>And at the end, what the theorems do and do not say about minds, and the answer "
            "of Gerhard Gentzen."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
