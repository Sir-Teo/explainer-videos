from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Tarski(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Tarski's analysis", r"What exactly goes wrong?", lit=(1933,), part=PART)
        with self.voiceover("Chapter two. Tarski's analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.derivation()
        self.satisfaction()
        self.hierarchy()
        self.nixon()

    def derivation(self):
        d = load("tschema")
        head = label(r"Three ingredients, \ three lines", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"1.", r"T(\ulcorner A \urcorner) \leftrightarrow A \quad \text{for every sentence } A",
                 r"the T-schema \ (Convention T, Part 3)"),
                (r"2.", r"L \;=\; \lnot T(\ulcorner L \urcorner)", r"self-reference \ (the diagonal lemma, Part 7)"),
                (r"3.", r"T(\ulcorner L \urcorner) \leftrightarrow \lnot T(\ulcorner L \urcorner)",
                 r"from 1 and 2, \ by classical logic")]
        tab = VGroup()
        for i, (n, f, why) in enumerate(rows):
            y = 1.5 - 1.0 * i
            tab.add(VGroup(label(n, font_size=26, color=GREY_B).move_to([-5.9, y, 0]),
                           MathTex(f, font_size=36, color=SELF if i == 2 else WHITE).move_to([-5.4, y, 0],
                                                                                              aligned_edge=LEFT),
                           label(why, font_size=22, color=GREY_A).move_to([1.6, y - 0.45, 0], aligned_edge=LEFT)))
        sat = label(r"the Reasoner: \ $l \leftrightarrow \lnot l$ \ is unsatisfiable \ (Part 2's SAT solver)",
                    font_size=26, color=BAD).to_edge(DOWN, buff=1.0)
        assert not d["sat"]
        with self.voiceover(
            "Alfred Tarski, in 1933, isolated exactly what the argument uses. <bookmark mark='a'/>First, the "
            "T-schema: for every sentence A, 'A' is true if and only if A. It seems to define what truth means. "
            "<bookmark mark='b'/>Second, self-reference: there is a sentence L that says of itself that it is not "
            "true. Part 7's diagonal lemma guarantees one in any language that can talk about its own sentences. "
            "<bookmark mark='c'/>Third, classical logic, which takes the instance of the schema for L and delivers "
            "'L is true if and only if L is not true'. <bookmark mark='d'/>As propositional logic, l if and only "
            "if not l. Part 2's SAT solver confirms that nothing satisfies it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(sat))
        self.clear_scene()


    def satisfaction(self):
        d = load("tarskidef")
        head = label(r"Tarski's positive result: \ truth \textit{defined}, \ for a language without it", font_size=30,
                     color=CONN).to_edge(UP, buff=0.4)
        model = VGroup(label(r"a model: \ snow, grass, coal; \ White, Green, Black", font_size=24, color=GREY_A))
        model.next_to(head, DOWN, buff=0.3)
        clauses = VGroup(
            MathTex(r"g \text{ satisfies } \mathrm{White}(x) \iff g(x) \in \{\text{snow}\}", font_size=30),
            MathTex(r"g \text{ satisfies } \lnot A \iff g \text{ does not satisfy } A", font_size=30),
            MathTex(r"g \text{ satisfies } A \wedge B \iff \text{it satisfies both}", font_size=30),
            MathTex(r"g \text{ satisfies } \exists x\, A \iff \text{some } g' \text{ differing at most at } x "
                    r"\text{ satisfies } A", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(
            [-0.8, 0.5, 0])
        why = label(r"satisfaction, \ not truth, \ is the recursive notion: \ $\exists x\,\mathrm{White}(x)$ is made "
                    r"of the open formula $\mathrm{White}(x)$", font_size=22, color=GOAL).next_to(clauses, DOWN,
                                                                                         buff=0.35)
        ex = VGroup(*[label(rf"${t}$: \ {'true' if v else 'false'}".replace("∃", r"\exists ").replace("∀", r"\forall ")
                            .replace("¬", r"\lnot "), font_size=22, color=OK if v else BAD) for t, v in d["examples"]])
        ex.arrange(RIGHT, buff=0.45).move_to([0, -2.55, 0])
        chk = label(rf"the Reasoner: \ all {d['count']} sentences to depth 2, \ each true or false, \ Convention T met",
                    font_size=22, color=OK).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Tarski's paper did more than diagnose. It showed how to define truth properly for a language that "
            "does not contain its own truth predicate. <bookmark mark='a'/>Take a little model: snow, grass and "
            "coal, with the predicates white, green and black. <bookmark mark='b'/>The trick is that truth is not "
            "the notion to define step by step. 'Something is white' is built from 'x is white', which is neither "
            "true nor false until x is given a value. So Tarski defined satisfaction: when an assignment of objects "
            "to variables satisfies a formula. An atomic formula by checking the object; a negation by not "
            "satisfying; a conjunction by satisfying both; and 'there is an x' by some assignment that differs at "
            "most at x. <bookmark mark='c'/>A sentence is true when it is satisfied. The Reasoner implements the "
            "clauses and checks every sentence up to depth two: each comes out true or false, and the definition "
            "meets Convention T. The definition lives in the metalanguage, as the hierarchy requires."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(model))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in clauses], lag_ratio=0.6), run_time=6)
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.2), FadeIn(chk))
        self.clear_scene()

    def hierarchy(self):
        head = label(r"Tarski's way out: \ a hierarchy of languages", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        levels = VGroup()
        for k, (t, c) in enumerate(((r"$\mathcal{L}_0$: \ snow, grass, numbers; \ no truth predicate", GREY_A),
                                    (r"$\mathcal{L}_1$: \ adds $T_0$, \ true for sentences of $\mathcal{L}_0$", OK),
                                    (r"$\mathcal{L}_2$: \ adds $T_1$, \ true for sentences of $\mathcal{L}_1$", GOAL),
                                    (r"$\mathcal{L}_3$: \ adds $T_2$ \dots", GLUT))):
            box = Rectangle(width=6.0 + 1.2 * k, height=0.75, stroke_color=c, stroke_width=2, fill_color=c,
                            fill_opacity=0.08).move_to([0, -2.4 + 1.0 * k, 0])
            levels.add(VGroup(box, label(t, font_size=24, color=c).move_to(box)))
        liar = label(r"`this sentence is not true$_n$' \ would need $T_n$ inside $\mathcal{L}_n$: \ it cannot be "
                     r"written", font_size=24, color=SELF).next_to(head, DOWN, buff=0.4)
        cost = label(r"the price: \ no single word `true'; \ and English seems to have one", font_size=24,
                     color=BAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Tarski's response was to give up the second ingredient for any single language. "
            "<bookmark mark='a'/>Start with a language with no truth predicate at all. Truth for its sentences is "
            "defined in a second language, the metalanguage, with a predicate true sub zero. Truth for that "
            "language needs a third, and so on up. <bookmark mark='b'/>Now the liar cannot be written: a sentence "
            "saying 'I am not true at level n' would have to contain the truth predicate for its own level, and "
            "none does. <bookmark mark='c'/>The price is that there is no single word 'true'. Tarski thought "
            "natural languages, which seem to have one, are simply inconsistent; for formal languages, the "
            "hierarchy was his answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in levels], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(liar))
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.clear_scene()

    def nixon(self):
        hc = history_card(1975, r"Saul Kripke", r"`Outline of a theory of truth'", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        dean = VGroup(label(r"Jones:", font_size=28, color=GOAL),
                      label(r"`most of Nixon's assertions about Watergate are false'", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        nixon = VGroup(label(r"Nixon:", font_size=28, color=GOAL),
                       label(r"`everything Jones says about Watergate is true'", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        both = VGroup(dean, nixon).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.5, 0])
        lv = label(r"each must be one level above the other: \ no levels work", font_size=26, color=BAD).next_to(
            both, DOWN, buff=0.5)
        risk = label(r"whether a sentence is paradoxical can depend on the facts: \ the liar is a \textit{risk}, "
                     r"not a grammar error", font_size=26, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Saul Kripke pointed out in 1975 why the hierarchy does not fit how we talk. "
            "<bookmark mark='a'/>Suppose Jones says that most of Nixon's assertions about Watergate are false, "
            "and Nixon says that everything Jones says about Watergate is true. <bookmark mark='b'/>On Tarski's "
            "view, each remark must sit at a level above the other, which is impossible. Yet usually there is no "
            "problem at all: if Nixon has said plenty of plainly false things, Jones is simply right. Only if "
            "Nixon's other assertions are exactly balanced, half true and half false, does the pair become a liar. "
            "<bookmark mark='c'/>Whether a sentence is paradoxical depends on the facts. Speakers cannot check "
            "levels in advance. The liar is a risk that any ordinary use of 'true' runs. Kripke's own theory, two "
            "chapters on, is built around that."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(both))
            vo.wait_until("b")
            self.play(FadeIn(lv))
            vo.wait_until("c")
            self.play(FadeIn(risk))
        self.clear_scene()
