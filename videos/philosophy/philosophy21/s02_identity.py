from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Identity(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Identity and Leibniz's law", r"What does `the same' mean?", lit=(1686, 1892),
                            part=PART)
        with self.voiceover("Chapter one. Identity and Leibniz's law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kinds()
        self.logic()
        self.converse()
        self.necessity()
        self.computing()

    def kinds(self):
        head = label(r"Numerical and qualitative identity", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(Circle(radius=0.6, color=WHOLE, fill_opacity=0.4), label(r"ball 1", font_size=16)).move_to(
            [-4.4, 1.5, 0])
        b = VGroup(Circle(radius=0.6, color=WHOLE, fill_opacity=0.4), label(r"ball 2", font_size=16)).move_to(
            [-2.8, 1.5, 0])
        for g in (a, b):
            g[1].move_to(g[0])
        la = label(r"qualitatively identical: \ exactly alike", font_size=19, color=WHOLE).next_to(VGroup(a, b), DOWN,
                                                                                               buff=0.3)
        hesp = label(r"Hesperus \ = \ Phosphorus", font_size=26, color=NOM).move_to([3.4, 1.6, 0])
        lh = label(r"numerically identical: \ one thing, \ two names", font_size=19, color=NOM).next_to(hesp, DOWN,
                                                                                                  buff=0.2)
        rows = stack([(r"qualitative: \ sharing properties \ (two balls from one mould)", WHOLE),
                      (r"numerical: \ being one and the same thing \ (the evening star is the morning star)", NOM),
                      (r"identity in the numerical sense is what philosophers mean by `=': \ a relation each thing "
                       r"bears to itself and to nothing else", GOAL),
                      (r"Frege \ (1892): \ `Hesperus = Phosphorus' is informative, \ `Hesperus = Hesperus' is not "
                       r"\ (Part 27)", GREY_A)], font_size=21, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Same has two meanings. <bookmark mark='a'/>Two balls from one mould are qualitatively identical: exactly "
            "alike, yet two. <bookmark mark='b'/>The evening star and the morning star are numerically identical: one "
            "planet, Venus, under two names. <bookmark mark='c'/>Philosophers' identity, written with the equals sign, "
            "is numerical: the relation that each thing bears to itself and to nothing else. <bookmark mark='d'/>Even "
            "so, Frege noticed, Hesperus is Phosphorus tells us something that Hesperus is Hesperus does not, a puzzle "
            "for Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hesp), FadeIn(lh), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def logic(self):
        head = label(r"The logic of identity: \ two axioms", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax1 = MathTex(r"\text{(Ref)} \quad a = a", font_size=34, color=OK)
        ax2 = MathTex(r"\text{(LL)} \quad a = b \to (\varphi(a) \to \varphi(b))", font_size=34, color=UNIV)
        axs = VGroup(ax1, ax2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.0, 1.6, 0])
        sym = VGroup(MathTex(r"\text{symmetry: take } \varphi(x) := x = a", font_size=26, color=GREY_A),
                     MathTex(r"a = b \to (a = a \to b = a)", font_size=28),
                     MathTex(r"\text{with (Ref): } a = b \to b = a", font_size=28, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.6, -0.6, 0])
        tra = VGroup(MathTex(r"\text{transitivity: take } \varphi(x) := x = c", font_size=26, color=GREY_A),
                     MathTex(r"b = a \to (b = c \to a = c)", font_size=28),
                     MathTex(r"\text{so } a = b \land b = c \to a = c", font_size=28, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.6, 0])
        note = label(r"identity is the smallest reflexive relation obeying Leibniz's law: \ an equivalence relation, "
                     r"and more", font_size=19, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Logic needs only two axioms for identity. <bookmark mark='a'/>Reflexivity: everything is identical to "
            "itself. <bookmark mark='b'/>And Leibniz's law, the indiscernibility of identicals: if a is b, whatever is "
            "true of a is true of b. <bookmark mark='c'/>Symmetry follows. Let the property be being identical to a. "
            "If a is b, and a is identical to a, then b is identical to a. <bookmark mark='d'/>So does transitivity. "
            "Let the property be being identical to c. <bookmark mark='e'/>Identity is the smallest reflexive "
            "relation that obeys Leibniz's law: an equivalence relation, and more. Every puzzle in this part tests one "
            "of these two axioms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(ax1))
            vo.wait_until("b")
            self.play(Write(ax2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in sym], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m) for m in tra], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def converse(self):
        hc = history_card(1686, r"G. W. Leibniz", r"\textit{Discourse on Metaphysics}, \ \S 9", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        f1 = MathTex(r"a = b \;\to\; \forall F\,(Fa \leftrightarrow Fb)", font_size=34, color=UNIV)
        f2 = MathTex(r"\forall F\,(Fa \leftrightarrow Fb) \;\to\; a = b", font_size=34, color=GOAL)
        l1 = label(r"the indiscernibility of identicals: \ uncontroversial", font_size=17, color=UNIV)
        l2 = label(r"the identity of indiscernibles \ (PII): \ contested", font_size=17, color=GOAL)
        g = VGroup(VGroup(f1, l1).arrange(DOWN, buff=0.15), VGroup(f2, l2).arrange(DOWN, buff=0.15)).arrange(
            DOWN, buff=0.5).move_to([2.2, 1.0, 0])
        rows = stack([(r"`no two substances are entirely alike': \ Leibniz looked for two identical leaves, \ and "
                       r"found none", WHITE),
                      (r"if `$F$' may be `is identical to $a$', \ PII is trivial", BAD),
                      (r"so: \ which properties count? \ qualitative ones only", GREY_A)], font_size=20,
                     aligned_edge=LEFT, width=8.6).move_to([1.2, -1.9, 0])
        with self.voiceover(
            "Leibniz's name is also attached to a much bolder principle, the converse. <bookmark mark='a'/>If a is b, "
            "a and b share every property: no one doubts that. <bookmark mark='b'/>But if a and b share every "
            "property, are they one? That is the identity of indiscernibles, and it is contested. "
            "<bookmark mark='c'/>Leibniz held that no two substances are entirely alike; the story is that he sent a "
            "courtier into the garden to find two identical leaves, and none were found. <bookmark mark='d'/>The "
            "principle is trivial if being identical to a counts as a property. <bookmark mark='e'/>So the real "
            "question is whether things alike in every qualitative respect must be one. The next chapter tests it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(l1))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(l2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def necessity(self):
        hc = history_card(1971, r"Saul Kripke", r"`Identity and Necessity'", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        steps = VGroup(
            MathTex(r"(1)\quad \Box\,(a = a)", font_size=32),
            MathTex(r"(2)\quad a = b \to (\Box(a = a) \to \Box(a = b))", font_size=32),
            MathTex(r"(3)\quad a = b \to \Box(a = b)", font_size=34, color=OK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.3).move_to([-2.0, 0.6, 0])
        why = VGroup(label(r"necessity of reflexivity", font_size=19, color=GREY_A),
                     label(r"Leibniz's law, \ with $\varphi(x) := \Box(a = x)$", font_size=19, color=GREY_A),
                     label(r"from (1) and (2)", font_size=19, color=GREY_A))
        for w_, st in zip(why, steps):
            w_.next_to(st, RIGHT, buff=0.4)
        rows = stack([(r"Barcan \ (1947) \ and Kripke: \ true identities are necessary", ABS),
                      (r"`Hesperus = Phosphorus' is necessary, \ yet was discovered: \ necessary \textit{a posteriori} "
                       r"\ (Part 22)", GOAL),
                      (r"the statue and the lump \ (chapter 3): \ if identical, \ necessarily so; \ but they could "
                       r"come apart", BAD),
                      (r"so contingent identity \ (Gibbard) \ needs a different logic of names \ (Lewis's "
                       r"counterparts)", UNIV)], font_size=19, aligned_edge=LEFT, width=11.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The two axioms have a surprising consequence in modal logic. <bookmark mark='a'/>Necessarily, a is a. "
            "<bookmark mark='b'/>Apply Leibniz's law to the property of being necessarily identical to a. If a is b, "
            "and a has that property, so does b. <bookmark mark='c'/>So if a is b, then necessarily a is b. Ruth "
            "Barcan Marcus proved this in 1947, and Saul Kripke defended it: true identities are necessary. "
            "<bookmark mark='d'/>Hesperus is Phosphorus is then necessary, though astronomers had to discover it: a "
            "necessary truth known a posteriori, a theme of Part 22. <bookmark mark='e'/>And the statue and the lump, "
            "which could have come apart, cannot be identical even now. Allan Gibbard's contingent identity requires "
            "giving up the simple logic of names, for something like Lewis's counterparts."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, st, w_ in zip("abc", steps, why):
                vo.wait_until(mk)
                self.play(Write(st), FadeIn(w_))
            self.play(FadeIn(rows[0]))
            for mk, r in zip("de", rows[1:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def computing(self):
        d = load("pyid")
        head = label(r"Identity in practice: \ programs and records", font_size=30, color=CONN).to_edge(UP,
                                                                                                buff=0.3)
        code = VGroup(*[label(r"\texttt{" + t + "}", font_size=20, color=c) for t, c in (
            (r"a = [1, 2]", WHITE), (r"b = a", WHITE), (r"c = [1, 2]", WHITE),
            (r"a is b \ \ $\to$ \ " + str(d["before"]["a is b"]), OK),
            (r"a is c \ \ $\to$ \ " + str(d["before"]["a is c"]), BAD),
            (r"a == c \ \ $\to$ \ " + str(d["before"]["a == c"]), OK),
            (r"a.append(3)", GOAL),
            (r"b \ \ $\to$ \ [1, 2, 3]; \ \ c \ \ $\to$ \ [1, 2]", UNIV))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.18).move_to([-4.5, -0.2, 0])
        box = SurroundingRectangle(code, buff=0.25, color=GREY_D, corner_radius=0.1)
        rows = stack([(r"\texttt{is}: \ numerical identity, \ one object under two names", OK),
                      (r"\texttt{==}: \ qualitative equality, \ the same value", WHOLE),
                      (r"change $a$ and $b$ changes: \ Leibniz's law, \ for aliases", UNIV),
                      (r"databases: \ a primary key is a criterion of identity", GOAL),
                      (r"record linkage \ (Fellegi and Sunter, \ 1969): \ are two records one person?", NOM)],
                     font_size=20, aligned_edge=LEFT, width=7.6).move_to([2.75, -0.2, 0])
        with self.voiceover(
            "Programmers live with the distinction between numerical and qualitative identity every day. "
            "<bookmark mark='a'/>In Python, let a be a list, let b be a, and let c be a new list with the same "
            "contents. The operator is tests numerical identity: a is b, but a is not c. The operator equals-equals "
            "tests qualitative equality: a and c are equal. <bookmark mark='b'/>Now append to a. Through b, the "
            "change shows up, because a and b are one object: Leibniz's law for aliases. Through c, it does not. "
            "<bookmark mark='c'/>Databases assign primary keys, which are criteria of identity by decree. "
            "<bookmark mark='d'/>And record linkage, made rigorous by Ivan Fellegi and Alan Sunter in 1969, asks of two "
            "records whether they describe one person: a question of personal identity, settled by probabilities."
        ) as vo:
            self.play(FadeIn(head), Create(box))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in code[:6]], lag_ratio=0.3), FadeIn(rows[0]), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(code[6]), FadeIn(code[7]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
