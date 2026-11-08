from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Geach(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The Frege--Geach problem", r"Can attitudes stand in logical relations?",
                            lit=(1965, 1990, 2008), part=PART)
        with self.voiceover("Chapter six. The Frege-Geach problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.higher()
        self.pairs()
        self.wishful()
        self.negation()

    def problem(self):
        head = label(r"Geach \ (1965): \ the embedding problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        lines = VGroup(label(r"1. \ Lying is wrong.", font_size=26, color=OUGHT),
                       label(r"2. \ If lying is wrong, \ then getting your little brother to lie is wrong.",
                             font_size=26, color=OUGHT),
                       label(r"3. \ So getting your little brother to lie is wrong.", font_size=26, color=GOAL)
                       ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 1.1, 0])
        side = stack([(r"in 1, \ `lying is wrong' is asserted: \ an attitude is expressed", EXPR),
                      (r"in 2, \ the same words are not asserted: \ no disapproval of lying is expressed", BAD),
                      (r"so the words mean something different in the two premises, \ and the argument equivocates", BAD),
                      (r"yet it is plainly valid: \ meaning must be the same embedded and unembedded \ (Frege)", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=11.6, buff=0.22).move_to([0, -1.7, 0])
        with self.voiceover(
            "Peter Geach, developing a point of Frege's, set the expressivist a problem in 1965. "
            "<bookmark mark='a'/>Lying is wrong. If lying is wrong, then getting your little brother to lie is wrong. "
            "So getting your little brother to lie is wrong. <bookmark mark='b'/>In the first premise, lying is wrong is "
            "asserted, and on the expressivist view it expresses disapproval of lying. <bookmark mark='c'/>In the "
            "second, the same words appear inside a conditional, unasserted: someone who says the conditional need "
            "not disapprove of lying at all. <bookmark mark='d'/>So if meaning is the attitude expressed, the words "
            "mean different things in the two premises, and the argument equivocates. <bookmark mark='e'/>Yet it is "
            "plainly valid. Whatever lying is wrong means, it must mean the same embedded and unembedded, and the "
            "expressivist owes a semantics in which this argument comes out valid."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in lines], lag_ratio=0.4))
            for mk, r in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def higher(self):
        head = label(r"A first answer, \ and its flaw", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Blackburn \ (1984)", r"the conditional expresses a higher-order attitude: \ disapproval of approving of lying while not disapproving of getting your brother to lie", EXPR),
                (r"the inference", r"someone with both premises and not the conclusion has a clash of attitudes", EXPR),
                (r"Hale \ (1986)", r"but a clash of attitudes is a fractured sensibility, \ not a logical error: \ it is not the incoherence of believing p and not p", BAD),
                (r"what is needed", r"a semantics on which the clash is inconsistency itself: \ Gibbard's, \ next", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Blackburn's first answer, in 1984, was to give the conditional an attitude of its own. <bookmark "
            "mark='a'/>If lying is wrong, then getting your brother to lie is wrong, expresses a higher-order "
            "attitude: disapproval of the combination of disapproving of lying while not disapproving of getting your "
            "brother to lie. <bookmark mark='b'/>Someone who accepts both premises and rejects the conclusion has a "
            "clash of attitudes. <bookmark mark='c'/>Bob Hale objected in 1986 that a clash of attitudes is a "
            "fractured sensibility, a moral failing perhaps, but not a logical error like believing p and not p. "
            "<bookmark mark='d'/>What is needed is a semantics on which the clash simply is inconsistency, and that "
            "is what Gibbard supplied."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pairs(self):
        d = load("gibbard")
        head = label(r"Norm-world pairs \ (Gibbard, \ 1990; \ 2003)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["valid"] and (d["n_pairs"], d["n_left"]) == (8, 2)
        assert d["left"] == [["gullible", ["G", "L"]], ["not gullible", ["G", "L"]]]
        pairs = [tuple([w, tuple(n)]) for w, n in d["pairs"]]
        P1 = {tuple([w, tuple(n)]) for w, n in d["P1"]}
        P2 = {tuple([w, tuple(n)]) for w, n in d["P2"]}
        C = {tuple([w, tuple(n)]) for w, n in d["C"]}
        norms = [(), ("L",), ("G",), ("G", "L")]
        nlab = {(): r"forbids nothing", ("L",): r"forbids lying", ("G",): r"forbids G only",
                ("G", "L"): r"forbids both"}
        cells = {}
        grid = VGroup()
        for i, n in enumerate(norms):
            for j, w in enumerate(["gullible", "not gullible"]):
                sq = RoundedRectangle(width=1.6, height=0.7, corner_radius=0.08, stroke_color=EXPR, stroke_width=2,
                                      fill_color=EXPR, fill_opacity=0.25).move_to([-4.6 + 1.9 * j, 1.4 - 0.9 * i, 0])
                cells[(w, n)] = sq
                grid.add(sq)
        rl = VGroup(*[label(nlab[n], font_size=16, color=OUGHT).next_to(cells[("gullible", n)], LEFT, buff=0.2)
                      for n in norms])
        cl = VGroup(label(r"brother gullible", font_size=15, color=IS).next_to(cells[("gullible", ())], UP, buff=0.12),
                    label(r"not", font_size=15, color=IS).next_to(cells[("not gullible", ())], UP, buff=0.12))
        crosses1 = VGroup(*[Cross(cells[p], stroke_color=BAD, stroke_width=3, scale_factor=0.6) for p in pairs
                            if p not in P1])
        crosses2 = VGroup(*[Cross(cells[p], stroke_color=BAD, stroke_width=3, scale_factor=0.6) for p in pairs
                            if p in P1 and p not in P2])
        keep = VGroup(*[SurroundingRectangle(cells[p], buff=0.05, color=GOAL, stroke_width=3) for p in pairs
                        if p in P1 and p in P2])
        side = stack([(r"a judgment: \ the set of pairs (factual world, \ system of norms) it leaves open", EXPR),
                      (r"P1, \ lying is wrong: \ rules out the systems that permit lying", OUGHT),
                      (r"P2, \ the conditional: \ rules out `forbids lying but not G'", OUGHT),
                      (r"left: \ 2 of 8 pairs, \ and in both, \ getting your brother to lie is forbidden: \ C", GOAL),
                      (r"valid: \ whatever survives the premises satisfies the conclusion", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=5.6, buff=0.28).move_to([3.5, -0.1, 0])
        with self.voiceover(
            "Allan Gibbard's answer, in Wise Choices, Apt Feelings, of 1990, and Thinking How to Live, of 2003, gives "
            "moral judgments a content that logic can work on. <bookmark mark='a'/>Pair each way the world might be "
            "with each system of norms one might adopt. A judgment is identified with the set of pairs it leaves "
            "open. Here the norms concern two acts: lying, and getting your brother to lie; and the facts concern "
            "whether your brother is gullible, which happens not to matter. Eight pairs. <bookmark mark='b'/>The "
            "first premise, lying is wrong, rules out every pair whose norms permit lying. <bookmark mark='c'/>The "
            "conditional rules out the pairs whose norms forbid lying but permit getting your brother to lie. "
            "<bookmark mark='d'/>Two of the eight pairs are left, and in both, getting your brother to lie is "
            "forbidden: the conclusion. <bookmark mark='e'/>Validity is the same as for facts: whatever survives the "
            "premises satisfies the conclusion. Accepting the premises and rejecting the conclusion would be a "
            "plan that cannot be carried out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(rl), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in crosses1], lag_ratio=0.15), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in crosses2], lag_ratio=0.15), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(keep), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def wishful(self):
        head = label(r"Wishful thinking \ (Dorr, \ 2002)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        lines = VGroup(label(r"1. \ If lying is wrong, \ then the soul survives death.", font_size=25, color=IS),
                       label(r"2. \ Lying is wrong.", font_size=25, color=OUGHT),
                       label(r"3. \ So the soul survives death.", font_size=25, color=GOAL)
                       ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 1.2, 0])
        foot = stack([(r"valid, \ and an expressivist semantics must make it so", GREY_A),
                      (r"premise 1 may be a factual belief; \ premise 2, \ on the view, \ is an attitude", EXPR),
                      (r"so an attitude, \ together with a belief, \ licenses a new factual belief: \ "
                       r"believing something because of how one feels about lying", BAD),
                      (r"Dorr: \ that looks like wishful thinking, \ which is irrational; \ replies: \ the belief in 1 "
                       r"was already a disposition to such inferences", GOAL)],
                     font_size=19, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Even with norm-world pairs, the expressivist faces a further puzzle, set by Cian Dorr in 2002. "
            "<bookmark mark='a'/>If lying is wrong, then the soul survives death. Lying is wrong. So the soul "
            "survives death. <bookmark mark='b'/>The argument is valid, and the expressivist's semantics, like "
            "Gibbard's, makes it so. <bookmark mark='c'/>But premise one could be an ordinary factual belief, while "
            "premise two, on the expressivist view, is an attitude toward lying. <bookmark mark='d'/>So an attitude, "
            "combined with a belief, would license a new belief about a matter of fact: believing the soul survives "
            "because of how one feels about lying. <bookmark mark='e'/>Dorr argued that this is wishful thinking, "
            "which is irrational. Expressivists reply that whoever accepts the first premise is already disposed to "
            "make the inference, so the rationality of the conclusion is inherited, not created by a feeling."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in lines], lag_ratio=0.4))
            for mk, r in zip("bcde", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def negation(self):
        head = label(r"The negation problem \ (Unwin, \ 1999; \ Schroeder, \ 2008)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        hd = [r"\text{sentence}", r"\text{simple expressivism}"]
        rows = [(r"Jon thinks murdering is wrong", r"Jon disapproves of murdering", EXPR),
                (r"Jon thinks not murdering is wrong", r"Jon disapproves of not murdering", EXPR),
                (r"Jon does not think murdering is wrong", r"Jon does not disapprove of murdering", EXPR),
                (r"Jon thinks murdering is not wrong", r"?? \ \ no place left for the negation", BAD)]
        cells = [[label(a, font_size=19), label(b, font_size=19, color=c)] for a, b, c in rows]
        grid = ValueGrid(hd, cells, col_w=[5.4, 5.6], cell_h=0.6, font_size=18).move_to([0, 0.6, 0])
        foot = stack([(r"a single attitude, \ disapproval, \ has only two places for `not': \ three sentences need "
                       r"three", BAD),
                      (r"Schroeder, \ \textit{Being For} \ (2008): \ one attitude, \ `being for', \ with structured "
                       r"content, \ solves it, \ at a price", EXPR),
                      (r"Gibbard's hyperplans give judgments propositional structure from the start", GOAL)],
                     font_size=19, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Mark Schroeder showed in Being For, of 2008, that a sharper version of the problem remains, which Nicholas "
            "Unwin had found in 1999. <bookmark mark='a'/>Jon thinks murdering is wrong: on the simple view, Jon "
            "disapproves of murdering. <bookmark mark='b'/>Jon thinks not murdering is wrong: he disapproves of not "
            "murdering. <bookmark mark='c'/>Jon does not think murdering is wrong: he does not disapprove of it. "
            "<bookmark mark='d'/>But Jon thinks murdering is not wrong is a fourth thing, and there is no place left "
            "to put the negation: one attitude has only two places for not, and the sentences need three. "
            "<bookmark mark='e'/>Schroeder's own repair posits a single attitude, being for, whose contents have "
            "enough structure; Gibbard's hyperplans have that structure from the start. The price, Schroeder argued, "
            "is that expressivism ends up rebuilding the whole of truth-conditional semantics inside the mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[k]])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
