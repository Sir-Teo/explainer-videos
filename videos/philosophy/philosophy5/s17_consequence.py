from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Consequence(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"What makes it logical?", r"What is it for a conclusion to follow?",
                            lit=(1936, 1990), part=PART)
        with self.voiceover("Chapter sixteen. What makes it logical?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tarski()
        self.etchemendy()
        self.invariance()
        self.tonk()

    def tarski(self):
        hcs = VGroup(history_card(1837, r"Bernard Bolzano", r"\textit{Wissenschaftslehre}: \ vary the ideas, \ keep "
                                  r"the truth", width=5.6, color=HIST),
                     history_card(1936, r"Alfred Tarski", r"`On the concept of logical consequence'", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        arg = VGroup(label(r"all whales are mammals; \ Moby is a whale; \ so Moby is a mammal", font_size=26),
                     label(r"all $P$ are $Q$; \ $a$ is $P$; \ so $a$ is $Q$", font_size=26, color=GOAL),
                     label(r"no reinterpretation of $P$, $Q$, $a$ makes the premises true and the conclusion false",
                           font_size=24, color=OK)).arrange(DOWN, buff=0.3).move_to([0, -0.2, 0])
        split = label(r"but which words may be reinterpreted? \ `all', `is', `so' must be held fixed: \ the "
                      r"\textit{logical constants}", font_size=24, color=BAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Every logic in this part disagrees with classical logic about what follows from what. So what does "
            "'follows' mean? <bookmark mark='a'/>Bernard Bolzano in 1837, and Alfred Tarski in 1936, gave the "
            "answer that Part 3 used. <bookmark mark='b'/>An argument is logically valid when its form guarantees "
            "the conclusion. All whales are mammals, Moby is a whale, so Moby is a mammal. "
            "<bookmark mark='c'/>Replace whale, mammal and Moby by anything you like: no reinterpretation makes the "
            "premises true and the conclusion false. <bookmark mark='d'/>But this needs a division of the "
            "vocabulary. 'All', 'is' and 'so' must be held fixed. Which words are the logical constants, and why?"
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(arg[0]))
            vo.wait_until("c")
            self.play(FadeIn(arg[1]), FadeIn(arg[2]))
            vo.wait_until("d")
            self.play(FadeIn(split))
        self.clear_scene()

    def etchemendy(self):
        hc = history_card(1990, r"John Etchemendy", r"\textit{The Concept of Logical Consequence}", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"Tarski checks \textit{reinterpretations} within the world there is", font_size=26),
                      label(r"if there were only three things in all, \ `there are at most three things' would come "
                            r"out logically true", font_size=26),
                      label(r"but logic should not depend on how many things exist", font_size=26, color=BAD),
                      label(r"the reply: \ quantify over all set-sized models, \ not just the actual world "
                            r"\ (as in Part 3)", font_size=24, color=GREY_A),
                      label(r"the question remains: \ \textit{why} is truth in all models the mark of following?",
                            font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(hc, DOWN,
                                                                                                    buff=0.5)
        rows.set_x(0)
        with self.voiceover(
            "In 1990 John Etchemendy argued that Tarski's definition gets the right answers by luck. "
            "<bookmark mark='a'/>It tests an argument by reinterpreting its words, within the world as it is. "
            "<bookmark mark='b'/>So suppose there were only three things in existence. Then no reinterpretation "
            "could make 'there are at least four things' true, and 'there are at most three things' would count as "
            "a truth of logic. <bookmark mark='c'/>But whether there are four things is not a matter of logic. "
            "<bookmark mark='d'/>The standard reply varies the domain as well, over all models, as Part 3 did. "
            "<bookmark mark='e'/>Etchemendy's deeper point survives: the definition tells us which arguments pass "
            "a test, not why passing it is what following consists in."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def invariance(self):
        d = load("invariance")
        hc = history_card(1966, r"Tarski, \ `What are logical notions?'", r"the logical notions are those no "
                          r"permutation of the world can change", width=7.0, color=HIST).to_corner(UL, buff=0.3)
        rel = VGroup()
        for r in d["relations"]:
            pts = [np.array([np.cos(PI / 2 + TAU * i / 3), np.sin(PI / 2 + TAU * i / 3), 0]) * 0.55 for i in range(3)]
            dots = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in pts])
            arcs = VGroup()
            if r["name"] in ("identity", "everything"):
                arcs.add(*[Circle(radius=0.14, color=CONN, stroke_width=2).move_to(p * 1.35) for p in pts])
            if r["name"] in ("distinctness", "everything"):
                for i in range(3):
                    for j in range(3):
                        if i != j:
                            arcs.add(Line(pts[i], pts[j], color=CONN, stroke_width=1.6, buff=0.1))
            rel.add(VGroup(VGroup(dots, arcs), label(r["name"], font_size=22, color=GOAL)).arrange(DOWN, buff=0.25))
        rel.arrange(RIGHT, buff=0.9).move_to([-2.6, 0.2, 0])
        rl = label(rf"of the 512 binary relations on 3 things, \ exactly {len(d['relations'])} are invariant",
                   font_size=24, color=OK).next_to(rel, DOWN, buff=0.4)
        hd = [label(r"things", font_size=22, color=P.CLAIM), label(r"quantifiers", font_size=22, color=P.CLAIM),
              label(r"invariant", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(str(q["n"]), font_size=26), MathTex(f"{q['all']:,}".replace(",", "{,}"), font_size=26),
                 MathTex(str(q["invariant"]), font_size=26, color=OK)] for q in d["quantifiers"]]
        grid = ValueGrid(hd, rows, col_w=[1.2, 2.0, 1.6], cell_h=0.55, font_size=26).move_to([4.6, 0.3, 0])
        ql = label(r"exactly the quantifiers that only count: \ $2^{n+1}$ \ ($\forall$, $\exists$, `at least two', "
                   r"`an even number', ...)", font_size=22, color=GOAL).to_edge(DOWN, buff=0.85)
        crit = label(r"Sher (1991): \ this is the mark of logic; \ Feferman (1999): \ then `uncountably many' is "
                     r"logical too", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        assert all(q["invariant"] == q["by_cardinality"] for q in d["quantifiers"])
        with self.voiceover(
            "Tarski's own answer came in a lecture of 1966. <bookmark mark='a'/>A notion is logical if no "
            "permutation of the world can change it: shuffle all the objects, and a logical notion stays the same. "
            "'Red' changes, since a shuffle can move red things to where blue things were. <bookmark mark='b'/>The "
            "Reasoner tries every binary relation on three things, all five hundred and twelve. Exactly four "
            "survive every shuffle: the empty relation, identity, distinctness, and the relation that holds "
            "between everything. <bookmark mark='c'/>And of the quantifiers, the sets of subsets, the invariant "
            "ones are exactly those that only count: for all, there exists, at least two, an even number of. Two "
            "to the n plus one of them, out of two to the two to the n. <bookmark mark='d'/>Gila Sher made this the "
            "criterion of logic in 1991. Solomon Feferman objected that it is too generous: 'uncountably many' "
            "passes the test, and so the logic inherits the hard questions of set theory."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rel[0]))
            vo.wait_until("b")
            self.play(FadeIn(rel[1:]), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(grid), FadeIn(ql))
            vo.wait_until("d")
            self.play(FadeIn(crit))
        self.clear_scene()

    def tonk(self):
        hc = history_card(1960, r"Arthur Prior", r"`The runabout inference-ticket'", width=5.8, color=HIST).to_corner(
            UL, buff=0.35)
        rules = VGroup(VGroup(label(r"tonk-introduction", font_size=24, color=GOAL),
                              MathTex(r"\frac{A}{A \ \mathrm{tonk}\ B}", font_size=42)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"tonk-elimination", font_size=24, color=GOAL),
                              MathTex(r"\frac{A \ \mathrm{tonk}\ B}{B}", font_size=42)).arrange(DOWN, buff=0.2)
                       ).arrange(RIGHT, buff=1.6).move_to([0, 0.9, 0])
        boom = MathTex(r"A \ \Rightarrow\ A \ \mathrm{tonk}\ B \ \Rightarrow\ B \qquad \text{for any } A, B",
                       font_size=36, color=BAD).next_to(rules, DOWN, buff=0.6)
        ans = VGroup(label(r"Belnap (1962): \ new rules must be \textit{conservative}: \ prove nothing new in the old "
                           r"language", font_size=24),
                     label(r"Prawitz, Dummett: \ \textit{harmony}: \ elimination takes out no more than introduction "
                           r"puts in", font_size=24),
                     label(r"so the logical constants may be those whose rules are in harmony", font_size=24,
                           color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(boom, DOWN, buff=0.5)
        ans.set_x(0)
        with self.voiceover(
            "There is a second tradition, which looks at proofs instead of models. Gentzen suggested that a "
            "connective's meaning is fixed by its introduction rule. <bookmark mark='a'/>In 1960 Arthur Prior "
            "replied with a joke connective, tonk. From A, infer A tonk B, as with 'or'. From A tonk B, infer B, as "
            "with 'and'. <bookmark mark='b'/>Then anything follows from anything. <bookmark mark='c'/>Nuel Belnap "
            "answered that a new connective must be conservative: it must prove nothing new in the old language. "
            "Dag Prawitz and Michael Dummett proposed harmony: an elimination rule may take out no more than the "
            "introduction rule puts in. Tonk fails both. On this view, the logical constants are those whose rules "
            "are in harmony, and that criterion favours intuitionistic logic, as Part 9 will explain."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rules))
            vo.wait_until("b")
            self.play(Write(boom))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a) for a in ans], lag_ratio=0.5), run_time=3)
        self.clear_scene()
