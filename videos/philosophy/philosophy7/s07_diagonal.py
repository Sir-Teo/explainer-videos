from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Diagonal(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Self-reference without paradox", r"Can a sentence talk about itself?",
                            lit=(1938,), part=PART)
        with self.voiceover("Chapter six. Self-reference, without paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.regress()
        self.quine()
        self.quine_sentence()
        self.lemma()

    def regress(self):
        head = label(r"The naive way: \ a regress", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        boxes = VGroup()
        w, h = 11.0, 4.6
        for k in range(7):
            r = RoundedRectangle(width=w * 0.8 ** k, height=h * 0.8 ** k, corner_radius=0.1, stroke_color=interpolate_color(
                ManimColor(SELF), ManimColor(GREY_D), k / 6), stroke_width=2)
            boxes.add(r.move_to([0.0 + 0.35 * (1 - 0.8 ** k) * 4, -0.4, 0]))
        texts = VGroup()
        for k in range(4):
            t = label(r"this sentence, \ which is \dots", font_size=int(26 * 0.8 ** k), color=GREY_A)
            t.next_to(boxes[k].get_corner(UL), DR, buff=0.12 * 0.8 ** k)
            texts.add(t)
        cap = label(r"to name itself, \ a sentence would have to contain itself", font_size=28,
                    color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How can a sentence talk about itself? <bookmark mark='a'/>The naive way fails. To quote itself in "
            "full, a sentence would have to contain a copy of itself, which contains a copy of itself, and so on "
            "for ever, like a pair of facing mirrors. <bookmark mark='b'/>No finite sentence can do it. The trick "
            "that avoids the regress turns up first in a place you may not expect: in programs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25), LaggedStart(
                *[FadeIn(t) for t in texts], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.clear_scene()

    def quine(self):
        d = load("quine")
        head = label(r"A program that prints itself", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        src = code_tex(d["src"], font_size=34, color=TAPE)
        sbox = SurroundingRectangle(src, buff=0.3, corner_radius=0.1, stroke_color=TAPE, stroke_width=2,
                                    fill_color="#0F141C", fill_opacity=1)
        prog = VGroup(sbox, src).move_to([0, 1.5, 0])
        lab1 = label(r"the program", font_size=22, color=GREY_B).next_to(prog, UP, buff=0.12)
        out = code_tex(d["out"], font_size=34, color=GOAL)
        obox = SurroundingRectangle(out, buff=0.3, corner_radius=0.1, stroke_color=GOAL, stroke_width=2,
                                    fill_color="#0F141C", fill_opacity=1)
        outp = VGroup(obox, out).move_to([0, -0.6, 0])
        lab2 = label(r"what it prints", font_size=22, color=GREY_B).next_to(outp, UP, buff=0.12)
        eq = label(r"identical \ $\checkmark$ \ (the Reasoner ran it)", font_size=26, color=OK).next_to(outp, DOWN,
                                                                                                       buff=0.35)
        parts = VGroup(label(r"a template $s$, \ with a hole $\%r$", font_size=24, color=SELF),
                       label(r"and an instruction: \ print the template, \ with its own quotation in the hole",
                             font_size=24, color=SELF)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        assert d["ok"]
        with self.voiceover(
            "Here is a program in Python that prints its own source code. Programs like this are called quines. "
            "<bookmark mark='a'/>Run it, and it prints exactly itself; the Reasoner ran it, and compared. "
            "<bookmark mark='b'/>It has two halves. A template, s, with a hole in it. And an instruction: print the "
            "template, with the template's own quotation filled into the hole. The program never contains a copy of "
            "itself. It contains a description, and an instruction to apply the description to itself. That is "
            "the whole trick, and Stephen Kleene proved in 1938 that every programming language allows it: any "
            "program can be given access to its own code."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog), FadeIn(lab1))
            vo.wait_until("a")
            self.play(FadeIn(outp), FadeIn(lab2))
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(parts))
        self.clear_scene()

    def quine_sentence(self):
        d = load("quine")
        hc = history_card(1962, r"W. V. O. Quine", r"`The ways of paradox'", width=5.4, color=HIST).to_corner(
            UL, buff=0.35)
        phrase = A.QUINE_PHRASE
        s = VGroup(label(r"`" + phrase + r"'", font_size=28, color=SELF),
                   label(phrase, font_size=28, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(
            [0, 0.6, 0])
        br1 = Brace(s[0], LEFT, color=SELF)
        br1l = label(r"a quotation", font_size=22, color=SELF).next_to(br1, LEFT, buff=0.15)
        br2 = Brace(s[1], LEFT, color=GOAL)
        br2l = label(r"what is said of it", font_size=22, color=GOAL).next_to(br2, LEFT, buff=0.15)
        check = label(r"the phrase, \ preceded by its quotation, \ is this very sentence \ $\checkmark$",
                      font_size=26, color=OK).next_to(s, DOWN, buff=0.7)
        liar = label(r"so the sentence says: \ `I am false'; \ no `this', \ no indexical", font_size=26,
                     color=BAD).next_to(check, DOWN, buff=0.35)
        assert d["subject_ok"]
        with self.voiceover(
            "The philosopher W. V. O. Quine, after whom quines are named, made the same trick into a sentence in "
            "1962. <bookmark mark='a'/>Take the phrase: yields falsehood when preceded by its quotation. Now "
            "precede it by its quotation. <bookmark mark='b'/>What does the sentence say? That a certain phrase, "
            "when preceded by its quotation, yields a falsehood. But that phrase, preceded by its quotation, is "
            "this very sentence; the Reasoner checks that too. <bookmark mark='c'/>So the sentence says of itself "
            "that it is false: a liar, built without the word this."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s[1]), FadeIn(br2), FadeIn(br2l))
            self.play(FadeIn(s[0]), FadeIn(br1), FadeIn(br1l))
            vo.wait_until("b")
            self.play(FadeIn(check))
            vo.wait_until("c")
            self.play(FadeIn(liar))
        self.clear_scene()

    def lemma(self):
        d = load("quine")
        thm = theorem_card(r"the diagonal lemma \ (Gödel 1931; Carnap 1934)", r"for every formula $\varphi(x)$ "
                           r"there is a sentence $D$ with \ $Q \vdash D \leftrightarrow \varphi(\ulcorner D \urcorner)$",
                           width=10.2, font_size=26).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"$\mathrm{diag}(n)$: \ the code of the formula coded by $n$, \ with $\bar n$ put in for $x$ \ "
                  r"(computable, \ so representable)", font_size=24),
            label(r"let $\psi(x) := \varphi(\mathrm{diag}(x))$, \ with code $k$; \ and let $D := \psi(\bar k)$",
                  font_size=24),
            label(r"then $\mathrm{diag}(k) = \ulcorner \psi(\bar k) \urcorner = \ulcorner D \urcorner$, \ so \ "
                  r"$D = \varphi(\mathrm{diag}(\bar k))$ says $\varphi(\ulcorner D \urcorner)$", font_size=24,
                  color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.45)
        eng = VGroup(label(r"in English, with $\varphi$ = `is unprovable':", font_size=22, color=GREY_B),
                     label(r"`the diagonalization of \ `the diagonalization of $x$ is unprovable' \ is unprovable'",
                           font_size=24, color=SELF),
                     label(r"the Reasoner diagonalizes the quoted template \ and gets the sentence back \ "
                           r"$\checkmark$", font_size=22, color=OK)).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.18).next_to(steps, DOWN, buff=0.7).align_to(steps, LEFT)
        assert d["godel_ok"]
        with self.voiceover(
            "Inside arithmetic, the trick becomes the diagonal lemma, implicit in Gödel's paper and stated in "
            "general by Rudolf Carnap in 1934. <bookmark mark='a'/>For any property phi, there is a sentence D that "
            "Q proves equivalent to: phi holds of D's own code. <bookmark mark='b'/>The proof is the quine. Let diag "
            "of n be the code of the formula you get by putting n's own numeral into the formula coded by n. It is "
            "computable, so arithmetic can express it. <bookmark mark='c'/>Let psi of x say: phi holds of diag of "
            "x. Psi has some code, k. Put k into psi: that is D. <bookmark mark='d'/>Diag of k is the code of D "
            "itself, so D says that phi holds of D. No regress: D contains a description of itself, and arithmetic "
            "does the copying. <bookmark mark='e'/>In English, with phi as 'is unprovable', the sentence reads like "
            "this, and the Reasoner checks that diagonalizing the quoted template gives the sentence back."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Indicate(thm, color=GOAL, scale_factor=1.02))
            for mk, st in zip("bcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in eng], lag_ratio=0.4))
        self.clear_scene()
