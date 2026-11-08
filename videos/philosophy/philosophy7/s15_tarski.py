from __future__ import annotations

import re

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Tarski(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Tarski: \ truth is not definable", r"Can arithmetic say what is true in "
                            r"arithmetic?", lit=(1933,), part=PART)
        with self.voiceover("Chapter fourteen. Tarski's theorem: truth is not definable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.partial()
        self.contrast()

    def theorem(self):
        hc = history_card(1933, r"Alfred Tarski", r"`The concept of truth in formalized languages'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        want = VGroup(label(r"suppose some formula $\mathrm{True}(x)$ of arithmetic satisfied, \ for every sentence "
                            r"$A$:", font_size=26),
                      MathTex(r"\mathrm{True}(\ulcorner A \urcorner) \ \leftrightarrow\ A", font_size=44,
                              color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, 1.1, 0])
        tl = label(r"Tarski's Convention T, \ from Part 3", font_size=22, color=GREY_B).next_to(want, DOWN, buff=0.2)
        diag = VGroup(label(r"the diagonal lemma, \ with $\varphi(x) := \lnot\,\mathrm{True}(x)$:", font_size=26),
                      MathTex(r"L \ \leftrightarrow\ \lnot\,\mathrm{True}(\ulcorner L \urcorner)", font_size=44,
                              color=SELF),
                      label(r"with Convention T: \ $L \leftrightarrow \lnot L$", font_size=30, color=BAD)).arrange(
            DOWN, buff=0.25).next_to(tl, DOWN, buff=0.5)
        thm = label(r"so no formula of arithmetic defines arithmetical truth", font_size=28, color=OK).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "In 1933 Alfred Tarski proved a theorem that is shorter than Gödel's, and in a sense deeper. "
            "<bookmark mark='a'/>Suppose arithmetic had a formula, True of x, that is true of exactly the codes of "
            "the true sentences: for every sentence A, True of A's code if and only if A. That is Tarski's "
            "Convention T, from Part 3. <bookmark mark='b'/>Apply the diagonal lemma to not True. It gives a sentence L equivalent to "
            "'L is not true'. That is the liar, now as a sentence of arithmetic. <bookmark mark='c'/>With "
            "Convention T, L holds if and only if L does not. <bookmark mark='d'/>So there is no such formula. "
            "Arithmetical truth cannot be defined in arithmetic."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(want), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(diag[0]), Write(diag[1]))
            vo.wait_until("c")
            self.play(FadeIn(diag[2]))
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.clear_scene()

    def partial(self):
        d = load("delta0")
        head = label(r"But partial truth \textit{is} definable", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        sub = label(r"the Reasoner's truth predicate for \textit{bounded} sentences: \ every quantifier "
                    r"$\forall x < t$, $\exists x < t$", font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.25)
        rows = VGroup()
        for i, ex in enumerate(d["examples"]):
            y = 1.3 - 0.78 * i
            tex = re.sub(r"([∀∃])(\w)<(\w+)\s*", lambda m_: ("\\forall " if m_.group(1) == "∀" else "\\exists ")
                         + m_.group(2) + "{<}" + m_.group(3) + "\\;", ex["s"])
            tex = (tex.replace("¬", r"\lnot ").replace("∧", r"\wedge ").replace("∨", r"\vee ")
                   .replace("×", r"\times "))
            m = MathTex(tex, font_size=30)
            m.move_to([-6.3 + m.width / 2, y + 0.12, 0])
            g = label(ex["gloss"], font_size=20, color=GREY_B).move_to([-6.3, y - 0.26, 0], aligned_edge=LEFT)
            v = label(r"true" if ex["value"] else r"false", font_size=26, color=OK if ex["value"] else BAD).move_to(
                [5.6, y + 0.05, 0])
            rows.add(VGroup(m, g, v))
        ladder = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"$\Delta_0$ truth: \ computable \ (finite search)", OK),
            (r"$\Sigma_1$ truth: \ definable by a $\Sigma_1$ formula \ (`a witness exists')", PROV),
            (r"$\Sigma_n$ truth: \ definable, \ for each fixed $n$", PROV),
            (r"truth for all sentences at once: \ \textit{not} definable \ (Tarski)", BAD))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        assert [ex["value"] for ex in d["examples"]] == [True, False, True, True]
        with self.voiceover(
            "Tarski's theorem forbids a truth predicate for the whole language. It allows partial ones. "
            "<bookmark mark='a'/>Here is the Reasoner's truth predicate for bounded sentences, where every "
            "quantifier is limited: for all x below ten, there is a y below ten. Such a quantifier is only a long "
            "'and', or a long 'or', so a finite search decides it. <bookmark mark='b'/>Every number below ten has a "
            "partner summing to nine: true. Two has a whole square root: false. Every number below thirty is even "
            "or odd: true. There is a prime between ninety and a hundred: true, it is ninety-seven. "
            "<bookmark mark='c'/>Truth for bounded sentences is computable, and arithmetic can define it. So can "
            "it define truth for sigma one sentences, 'a witness exists', and for sigma two, and for each fixed "
            "level. What it cannot do is define truth for every level at once. The hierarchy of partial truth "
            "predicates has no top."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[VGroup(r[0], r[1]) for r in rows])))
            vo.wait_until("b")
            for r in rows:
                self.play(FadeIn(r[2], scale=0.6), run_time=0.6)
                self.wait(1.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in ladder], lag_ratio=0.5), run_time=4)
        self.clear_scene()

    def contrast(self):
        head = label(r"Truth and proof come apart", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(label(r"provability", font_size=30, color=PROV),
                      label(r"definable: \ $\mathrm{Prov}(x)$ is a $\Sigma_1$ formula", font_size=24),
                      label(r"the liar for it is $G$: \ not a paradox, \ a theorem", font_size=24, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(label(r"truth", font_size=30, color=GOAL),
                       label(r"not definable in arithmetic", font_size=24),
                       label(r"the liar for it is a contradiction", font_size=24, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.9, 0])
        div = Line(cols.get_top() + UP * 0.1, cols.get_bottom() + DOWN * 0.1, color=GREY_D).move_to(
            [(left.get_right()[0] + right.get_left()[0]) / 2, cols.get_center()[1], 0])
        concl = VGroup(label(r"so provability is not truth: \ a second proof of incompleteness", font_size=28,
                             color=GOAL),
                       label(r"truth for a language can be defined, \ but only in a richer metalanguage", font_size=24,
                             color=GREY_A),
                       label(r"a hierarchy of languages; \ or a language that holds its own truth, \ at a price: "
                             r"\ Part 8", font_size=24, color=SELF)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Put the two theorems side by side. <bookmark mark='a'/>Provability is definable in arithmetic, and "
            "the liar built from it is Gödel's sentence: not a paradox, but a theorem about what can be proved. "
            "<bookmark mark='b'/>Truth is not definable, and the liar built from it is a contradiction. "
            "<bookmark mark='c'/>So provability and truth must differ, which is a second proof of incompleteness, "
            "and the cleanest. <bookmark mark='d'/>Tarski's way out was a hierarchy: truth for one language can be "
            "defined, but only in a richer metalanguage. Whether a language can after all hold its own truth "
            "predicate, and at what price, is the subject of Part 8."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(Create(div), FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(concl[0]))
            vo.wait_until("d")
            self.play(FadeIn(concl[1]), FadeIn(concl[2]))
        self.clear_scene()
