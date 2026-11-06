from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


def bind_arc(q, v, color=QUANT, height=0.5):
    """An arc from a quantifier's variable down to an occurrence it binds."""
    a, b = q.get_top() + UP * 0.08, v.get_top() + UP * 0.08
    return ArcBetweenPoints(a, b, angle=-PI * 0.55 if b[0] > a[0] else PI * 0.55, color=color, stroke_width=3)


class Syntax(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Variables, quantifiers and capture", r"What does a variable do?", lit=(1879,),
                            part=PART)
        with self.voiceover("Chapter two. Variables, quantifiers, and capture."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grammar()
        self.binding()
        self.ambiguity()
        self.capture()
        self.unsound()

    def grammar(self):
        head = label(r"The grammar of first-order logic", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        terms = VGroup(label(r"terms \ (name objects)", font_size=26, color=OBJ),
                       MathTex(r"t \;::=\; x \;\mid\; c \;\mid\; f(t_1, \dots, t_n)", font_size=38)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        forms = VGroup(label(r"formulas \ (say things)", font_size=26, color=GOAL),
                       MathTex(r"\varphi \;::=\; R(t_1, \dots, t_n) \;\mid\; t_1 = t_2 \;\mid\; \lnot \varphi \;\mid\; "
                               r"(\varphi \land \psi) \;\mid\; \dots \;\mid\; \forall x\, \varphi \;\mid\; "
                               r"\exists x\, \varphi", font_size=38)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g = VGroup(terms, forms).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.5)
        ex = VGroup(
            VGroup(MathTex(r"\mathrm{father}(\mathrm{father}(x))", font_size=34, color=OBJ),
                   label(r"a term: \ $x$'s paternal grandfather", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(MathTex(r"\mathrm{Older}(\mathrm{socrates}, \mathrm{plato})", font_size=34, color=REL),
                   label(r"an atomic formula", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(MathTex(r"\forall x\, \exists y\ \mathrm{L}(x, y)", font_size=34, color=QUANT),
                   label(r"a sentence", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(
            RIGHT, buff=0.9).to_edge(DOWN, buff=0.7)
        fo = label(r"`first-order': \ the variables range over objects, never over properties", font_size=24,
                   color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "First the grammar, which is short. <bookmark mark='a'/>There are two kinds of expression. Terms name "
            "objects: a variable like x, a constant like Socrates, or a function applied to terms, like the father of "
            "the father of x, which names x's paternal grandfather. <bookmark mark='b'/>Formulas say things: a "
            "relation applied to terms, an identity between two terms, and then the connectives of Part 2, and two "
            "new operators, for every x, and there exists an x. <bookmark mark='c'/>So 'Socrates is older than "
            "Plato' is an atomic formula, and 'for every x there is a y such that x loves y' is a sentence. "
            "<bookmark mark='d'/>The logic is called first-order because its variables range over objects only. "
            "There is no variable for 'every property'. That restriction looks arbitrary, and Chapter thirteen will "
            "show that it is exactly what makes this logic behave so well."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(terms[0]), Write(terms[1]))
            self.play(FadeIn(ex[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(forms[0]), Write(forms[1]))
            vo.wait_until("c")
            self.play(FadeIn(ex[1], shift=UP * 0.2), FadeIn(ex[2], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(fo))
        self.clear_scene()

    def binding(self):
        parts = [r"\forall", r"x", r"\,(\mathrm{P}(", r"x", r") \to \exists", r"y", r"\, \mathrm{R}(", r"x", r",",
                 r"y", r")", r"\lor", r"\mathrm{Q}(", r"z", r"))"]
        f = MathTex(*parts, font_size=50).move_to([0, 1.0, 0])
        for i in (1, 3, 7):
            f[i].set_color(VAR)
        for i in (5, 9):
            f[i].set_color(QUANT)
        f[13].set_color(BAD)
        arcs_x = VGroup(*[bind_arc(f[1], f[i], color=VAR) for i in (3, 7)])
        arcs_y = VGroup(bind_arc(f[5], f[9], color=QUANT))
        scope = BraceBetweenPoints(f[2].get_corner(DL) + DOWN * 0.1, f[14].get_corner(DR) + DOWN * 0.1, DOWN,
                                   color=GREY_B)
        sl = label(r"the scope of $\forall x$", font_size=24, color=GREY_A).next_to(scope, DOWN, buff=0.12)
        free = label(r"$z$ is free: \ nothing binds it", font_size=26, color=BAD).next_to(f[13], UP, buff=0.6)
        defs = VGroup(
            label(r"an occurrence of $x$ is \textit{bound} if it lies in the scope of a $\forall x$ or $\exists x$; "
                  r"otherwise \textit{free}", font_size=24),
            label(r"a \textit{sentence} has no free variables: \ only sentences are true or false outright",
                  font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A quantifier binds the variable it names, throughout its scope. <bookmark mark='a'/>In this formula, the "
            "'for all x' at the front binds every x that follows, here and here. <bookmark mark='b'/>Its scope is "
            "everything in the brackets after it. <bookmark mark='c'/>The 'there exists a y' binds the y inside "
            "its own, smaller scope. <bookmark mark='d'/>But z is bound by nothing. It is free: like a pronoun with no "
            "antecedent, it waits for someone to say what it refers to. <bookmark mark='e'/>A formula with no free "
            "variables is a sentence, and only sentences are true or false outright. 'x is older than Plato' is "
            "neither until we know who x is."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arcs_x], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(GrowFromCenter(scope), FadeIn(sl))
            vo.wait_until("c")
            self.play(Create(arcs_y[0]))
            vo.wait_until("d")
            self.play(FadeIn(free), Indicate(f[13], color=BAD))
            vo.wait_until("e")
            self.play(FadeIn(defs, shift=UP * 0.2))
        self.clear_scene()

    def ambiguity(self):
        s = label(r"`Every student read some book.'", font_size=36).to_edge(UP, buff=0.6)
        r1 = VGroup(MathTex(r"\forall x\, (\mathrm{S}(x) \to \exists y\, (\mathrm{B}(y) \land \mathrm{Read}(x, y)))",
                            font_size=36, color=P.CLAIM),
                    label(r"each read a book, perhaps different ones", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        r2 = VGroup(MathTex(r"\exists y\, (\mathrm{B}(y) \land \forall x\, (\mathrm{S}(x) \to \mathrm{Read}(x, y)))",
                            font_size=36, color=P.AGENT),
                    label(r"one book that every student read", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        rr = VGroup(r1, r2).arrange(DOWN, buff=0.6).move_to([0, 0.2, 0])
        imp = label(r"the second entails the first, \ not conversely \ (Chapter 5 proves both halves)", font_size=26,
                    color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "English hides scope, and logic exposes it. <bookmark mark='a'/>'Every student read some book.' Does it "
            "say that each student read a book, perhaps a different one each? <bookmark mark='b'/>Or that there is "
            "one book that every student read? <bookmark mark='c'/>The two readings differ only in the order of the "
            "quantifiers. The second entails the first, but not the other way round, and in Chapter five the "
            "Reasoner will prove one direction and refute the other. Linguists call this a scope ambiguity, and "
            "translating English into logic means choosing a reading."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            self.play(Write(r1[0]), FadeIn(r1[1]))
            vo.wait_until("b")
            self.play(Write(r2[0]), FadeIn(r2[1]))
            vo.wait_until("c")
            self.play(FadeIn(imp))
        self.clear_scene()

    def capture(self):
        d = load("capture")
        head = label(r"Substitution: \ replace a free variable by a term", font_size=32, color=CONN).to_edge(UP,
                                                                                                         buff=0.4)
        base = VGroup(MathTex(r"\exists y\ \mathrm{L}(x, y)", font_size=38),
                      label(r"`$x$ loves somebody'", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.6)
        good = VGroup(MathTex(r"\exists y\ \mathrm{L}(a, y)", font_size=38, color=OK),
                      label(r"`$a$ loves somebody' \ $\checkmark$", font_size=24, color=OK)).arrange(RIGHT, buff=0.6)
        bad = VGroup(MathTex(r"\exists y\ \mathrm{L}(y, y)", font_size=38, color=BAD),
                     label(r"`somebody loves themselves' \ $\times$", font_size=24, color=BAD)).arrange(RIGHT, buff=0.6)
        fix = VGroup(MathTex(r"\exists z\ \mathrm{L}(y, z)", font_size=38, color=OK),
                     label(r"rename first: \ `$y$ loves somebody' \ $\checkmark$", font_size=24, color=OK)).arrange(
            RIGHT, buff=0.6)
        lab = VGroup(label(r"$x := a$", font_size=28, color=VAR), label(r"$x := y$, naively", font_size=28,
                                                                       color=VAR),
                     label(r"$x := y$, correctly", font_size=28, color=VAR))
        rows = VGroup(base, good, bad, fix).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([1.2, 0.1, 0])
        for l_, r_ in zip(lab, rows[1:]):
            l_.next_to(r_, LEFT, buff=0.6)
        assert d["captured"] == "∃y L(y, y)" and d["renamed"] == "∃z L(y, z)"
        rule = label(r"a term $t$ is \textit{free for} $x$ when no variable of $t$ gets captured; \ "
                     r"bound variables can always be renamed", font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now the most important operation in logic, and the most error-prone: substitution. "
            "<bookmark mark='a'/>Take the formula 'there is a y such that x loves y', which says that x loves "
            "somebody. <bookmark mark='b'/>Replace the free x by the constant a, and you get 'a loves somebody'. "
            "Fine. <bookmark mark='c'/>Now replace x by the variable y, naively. You get 'there is a y such that y "
            "loves y': somebody loves themselves. The y we put in has been captured by the quantifier, and the "
            "meaning has changed completely. <bookmark mark='d'/>The cure is to rename the bound variable first. "
            "Bound variables are placeholders, and their names do not matter: 'there is a z such that x loves z' says "
            "exactly the same thing. Now substitute, and you get 'y loves somebody', as intended. "
            "<bookmark mark='e'/>The official rule: a term is free for x when substituting it captures nothing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(base[0]), FadeIn(base[1]))
            vo.wait_until("b")
            self.play(FadeIn(lab[0]), Write(good[0]), FadeIn(good[1]))
            vo.wait_until("c")
            self.play(FadeIn(lab[1]), Write(bad[0]), FadeIn(bad[1]))
            self.play(Indicate(bad[0], color=BAD))
            vo.wait_until("d")
            self.play(FadeIn(lab[2]), Write(fix[0]), FadeIn(fix[1]))
            vo.wait_until("e")
            self.play(FadeIn(rule))
        self.clear_scene()

    def unsound(self):
        prem = fol.parse("forall x exists y ~x = y")
        bad = fol.parse("exists y ~y = y")
        two = fol.Structure(range(2), {})
        ok_any = all(fol.holds(prem, fol.Structure(range(n), {})) for n in (2, 3, 4))
        assert ok_any and not fol.holds(prem, fol.Structure(range(1), {}))
        assert not any(fol.holds(bad, fol.Structure(range(n), {})) for n in (1, 2, 3, 4)) and fol.holds(prem, two)
        p = VGroup(MathTex(r"\forall x\, \exists y\ \lnot\, x = y", font_size=44, color=OK),
                   label(r"`for everything there is something else': \ true in any world with two things", font_size=24,
                         color=GREY_A)).arrange(DOWN, buff=0.2).move_to([0, 1.7, 0])
        arrow = MathTex(r"\Downarrow \ \ \text{instantiate } x := y", font_size=34, color=GREY_B).move_to([0, 0.4, 0])
        c = VGroup(MathTex(r"\exists y\ \lnot\, y = y", font_size=44, color=BAD),
                   label(r"`something is not itself': \ false in every world", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.2).move_to([0, -0.9, 0])
        ind = VGroup(label(r"the same bug, in software:", font_size=24, color=CONN),
                     label(r"compilers, proof assistants, and the $\lambda$-calculus avoid it with de Bruijn's "
                           r"nameless variables (1972)", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why care? Because the basic rule for 'all', that what holds of everything holds of any particular term, "
            "is only sound when the term is free for the variable. <bookmark mark='a'/>For everything, there is "
            "something different from it: true in every world with at least two things. <bookmark mark='b'/>"
            "Instantiate x with the variable y, carelessly, and the y is captured. <bookmark mark='c'/>You have "
            "derived 'something is not identical to itself', which is false in every world. A true premise, a false "
            "conclusion, one careless step. <bookmark mark='d'/>The same bug haunts software. Compilers and proof "
            "assistants either rename very carefully, or do away with variable names altogether, using the numbered "
            "placeholders Nicolaas de Bruijn introduced in 1972 for his proof checker Automath."
        ) as vo:
            self.play(Write(p[0]))
            vo.wait_until("a")
            self.play(FadeIn(p[1]))
            vo.wait_until("b")
            self.play(FadeIn(arrow))
            vo.wait_until("c")
            self.play(Write(c[0]), FadeIn(c[1]))
            vo.wait_until("d")
            self.play(FadeIn(ind))
        self.clear_scene()
