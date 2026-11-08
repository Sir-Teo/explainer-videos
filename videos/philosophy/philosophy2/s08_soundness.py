from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403

RULE_TEX = {"andI": r"\land\mathrm{I}", "andE": r"\land\mathrm{E}", "orI": r"\lor\mathrm{I}", "impE": r"\to\mathrm{E}",
            "notE": r"\lnot\mathrm{E}", "botE": r"\bot\mathrm{E}", "dne": r"\lnot\lnot\mathrm{E}",
            "impI": r"\to\mathrm{I}", "notI": r"\lnot\mathrm{I}", "orE": r"\lor\mathrm{E}"}


def bridge(left_sym, right_sym, lw, rw):
    L = VGroup(MathTex(left_sym, font_size=90, color=CONN), label(lw, font_size=26, color=GREY_A)).arrange(
        DOWN, buff=0.2)
    R = VGroup(MathTex(right_sym, font_size=90, color=OK), label(rw, font_size=26, color=GREY_A)).arrange(
        DOWN, buff=0.2)
    L.move_to([-3.6, 0.6, 0])
    R.move_to([3.6, 0.6, 0])
    top = CurvedArrow(L[0].get_top() + UP * 0.1, R[0].get_top() + UP * 0.1, angle=-PI / 3, color=OK,
                      stroke_width=4)
    bot = CurvedArrow(R[0].get_bottom() + DOWN * 0.9, L[0].get_bottom() + DOWN * 0.9, angle=-PI / 3, color=GREY_C,
                      stroke_width=4)
    tl = label(r"soundness", font_size=30, color=OK).next_to(top, UP, buff=0.1)
    bl = label(r"completeness", font_size=30, color=GREY_C).next_to(bot, DOWN, buff=0.1)
    return L, R, top, bot, tl, bl


class Soundness(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Soundness: proofs never lie", r"Is everything we can prove true?", part=PART)
        with self.voiceover("Chapter seven. Soundness: proofs never lie."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.two()
        self.rules()
        self.unsound()
        self.tonk()

    def two(self):
        L, R, top, bot, tl, bl = bridge(r"\Gamma \vdash \varphi", r"\Gamma \models \varphi",
                                        r"there is a proof: \ rules, lines, boxes",
                                        r"truth preserved: \ every valuation")
        with self.voiceover(
            "We now have two ways of saying that a conclusion follows from premises. <bookmark mark='a'/>One is about "
            "proof: there is a derivation, written with a single turnstile. <bookmark mark='b'/>The other is about "
            "truth: every valuation that makes the premises true makes the conclusion true, the double turnstile. "
            "Proof is something we do, with marks on paper, and anyone can check it. Truth is about every way the "
            "world might be. <bookmark mark='c'/>Are the two the same? Two theorems answer, one for each direction. "
            "<bookmark mark='d'/>The first is soundness: whatever we can prove is valid. Proofs never lie."
        ) as vo:
            self.play(FadeIn(L[0]), FadeIn(R[0]))
            vo.wait_until("a")
            self.play(FadeIn(L[1], shift=UP * 0.1), Indicate(L[0], color=CONN))
            vo.wait_until("b")
            self.play(FadeIn(R[1], shift=UP * 0.1), Indicate(R[0], color=OK))
            vo.wait_until("c")
            self.play(Create(bot), FadeIn(bl), Create(top), FadeIn(tl))
            vo.wait_until("d")
            self.play(Indicate(tl, color=OK, scale_factor=1.2), top.animate.set_stroke(width=6))
        self.clear_scene()

    def rules(self):
        d = load("soundness")["rules"]
        thm = theorem_card(r"Soundness", r"if $\Gamma \vdash \varphi$ then $\Gamma \models \varphi$", width=5.4,
                           font_size=26).to_corner(UL, buff=0.4)
        idea = wrapped_label(r"by induction on the length of the proof: \ premises are true wherever $\Gamma$ is; "
                             r"each rule turns true lines into a true line", 5.6, 24, GREY_A)
        idea.next_to(thm, DOWN, buff=0.4).align_to(thm, LEFT)
        rows = []
        for r in d:
            chk = r["check"] if not r["premises"] else (", ".join(r["premises"]) + " ⊨ " + r["check"])
            if r["premises"]:
                left = r", ".join(ftex(x) for x in r["premises"]) + r" \models " + ftex(r["check"])
            else:
                left = ftex(r["check"])
            rows.append([MathTex(RULE_TEX[r["rule"]], font_size=28, color=CONN), MathTex(left, font_size=26),
                         MathTex(r"\checkmark", font_size=30, color=OK) if r["sound"] else MathTex(r"\times",
                                                                                                    color=BAD)])
        grid = ValueGrid([r"\text{rule}", r"\text{its condition}", r"\text{checked}"], rows, cell_h=0.5,
                         font_size=26)
        grid.scale_to_fit_height(6.0)
        if grid.width > 7.6:
            grid.width = 7.6
        grid.to_edge(RIGHT, buff=0.35).set_y(-0.1)
        k = next(i for i, r in enumerate(d) if r["rule"] == "impI")
        box = grid.row_box(k, color=GOAL)
        gloss_ = wrapped_label(r"$G$ stands for the premises: \ if $G$ with $A$ gives $B$, \ $G$ alone gives "
                               r"$A \to B$", 5.6, 24, GOAL).next_to(idea, DOWN, buff=0.4).align_to(idea, LEFT)
        with self.voiceover(
            "The proof follows the shape of proofs: induction on their length. <bookmark mark='a'/>A premise is true "
            "in every valuation that makes the premises true, trivially. Then show that every rule, applied to lines "
            "that are true in a valuation, produces a line that is true in it. <bookmark mark='b'/>Each rule's "
            "condition is a small entailment or tautology of its own, so the Reasoner checks them all, one by one. "
            f"<bookmark mark='c'/>All {len(d)} pass."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(idea))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[i][:2])) for i in range(len(rows))], lag_ratio=0.12),
                      run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[i][2], scale=1.4) for i in range(len(rows))], lag_ratio=0.1))
        with self.voiceover(
            "The rules that close boxes need a little more care, because the premises change inside a box. "
            "<bookmark mark='a'/>Arrow introduction says: if the premises together with A lead to B, then the premises "
            "alone lead to 'if A then B'. Its condition is this formula, with G standing for the premises: and it is a "
            "tautology, so the step is safe whatever G says."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(box), FadeIn(gloss_))
        self.clear_scene()

    def unsound(self):
        u = load("soundness")["unsound"]
        am = ArgumentMap(["A -> B", "B"], "A", width=4.4, font_size=40, center=[-3.2, 0.8, 0])
        v = am.verdict(font_size=28).next_to(am, DOWN, buff=0.4).align_to(am, LEFT)
        tag = label(r"a rule we must not add", font_size=28, color=BAD).next_to(am, UP, buff=0.4)
        cm = u["countermodel"]
        assert not u["sound"] and cm == {"A": False, "B": True}
        cor = theorem_card(r"Consistency", r"nothing proves $\bot$ from no premises: \ no valuation makes $\bot$ "
                           r"true, so by soundness no proof can reach it", kind=r"Corollary", width=6.0,
                           font_size=24).move_to([3.4, 0.6, 0])
        phil = wrapped_label(r"what we can check (proofs) never outruns what is so (truth)", 11.0, 30, GOAL)
        phil.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Compare a rule we must not add: from 'if A then B' and B, infer A, affirming the consequent as a rule. "
            "<bookmark mark='a'/>The Reasoner finds its countermodel at once: A false, B true. A system with that rule "
            "would prove false conclusions from true premises. <bookmark mark='b'/>Soundness has a corollary. No "
            "valuation makes the false constant true, so no proof from no premises can ever reach it: the system is "
            "consistent. <bookmark mark='c'/>What we can check never outruns what is so."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(am))
            vo.wait_until("a")
            self.play(FadeIn(v, scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(cor, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(Write(phil))
        self.clear_scene()

    def tonk(self):
        t = load("tonk")
        rules = VGroup(VGroup(MathTex(r"\dfrac{A}{A \ \mathrm{tonk}\ B}", font_size=48),
                              label(r"like `or'", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15),
                       VGroup(MathTex(r"\dfrac{A \ \mathrm{tonk}\ B}{B}", font_size=48),
                              label(r"like `and'", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(
            RIGHT, buff=1.0).to_corner(UL, buff=0.5)
        hc = history_card(1960, r"Arthur Prior", r"`The Runabout Inference-Ticket'", width=4.6, color=HIST)
        hc.to_corner(UR, buff=0.4)
        chain = MathTex(r"\text{it rains}", r"\ \vdash\ ", r"\text{it rains tonk the moon is cheese}", r"\ \vdash\ ",
                        r"\text{the moon is cheese}", font_size=30)
        chain[4].set_color(BAD)
        chain.move_to([0, 0.3, 0])
        sym = {"⊤": r"\top", "⊥": r"\bot", "→": r"\to", "←": r"\leftarrow", "∧": r"\land", "∨": r"\lor",
               "↔": r"\leftrightarrow", "⊕": r"\oplus", "↑": r"\uparrow", "↓": r"\downarrow", "¬p": r"\lnot p",
               "¬q": r"\lnot q", "p": "p", "q": "q", "↚": r"\not\leftarrow", "↛": r"\not\to"}
        io = MathTex(r"\text{sound introduction: }\ " + r",\ ".join(sym[x] for x in t["intro_only"]), font_size=32,
                     color=OK)
        eo = MathTex(r"\text{sound elimination: }\ " + r",\ ".join(sym[x] for x in t["elim_only"]), font_size=32,
                     color=OK)
        bo = MathTex(r"\text{both: }\ \varnothing", font_size=36, color=BAD)
        sets = VGroup(io, eo, bo).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.7, 0])
        bel = label(r"Belnap (1962): rules define a connective only if they prove nothing new about the old words",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Soundness also says something about what rules can and cannot do. <bookmark mark='a'/>In 1960 Arthur "
            "Prior invented a connective he called tonk, with an introduction rule like 'or': from A, infer A tonk "
            "B; and an elimination rule like 'and': from A tonk B, infer B. <bookmark mark='b'/>Two harmless-looking "
            "rules, and together they prove anything from anything. From 'it rains', infer 'it rains tonk the moon "
            "is cheese', and then 'the moon is cheese'."
        ) as vo:
            self.play(FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(FadeIn(hc), FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(Write(chain))
        with self.voiceover(
            "Could some truth table make tonk sound? Its introduction needs it true whenever A is true; its "
            "elimination needs B true whenever it is. <bookmark mark='a'/>The Reasoner checks all sixteen tables. "
            f"{len(t['intro_only'])} make the introduction sound, {len(t['elim_only'])} make the elimination "
            "sound, and none does both: in the row where A is true and B false, the demands collide. "
            "<bookmark mark='b'/>Nuel Belnap's reply, in 1962, was that rules can give a word its meaning only if "
            "they are in harmony with the rest of the language: adding them must prove nothing new about the old "
            "words. Our rules pass that test; tonk's do not. The question of how rules give meaning returns in "
            "Part 28."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(sets[0]), FadeIn(sets[1]))
            self.play(FadeIn(sets[2], scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(bel))
        self.clear_scene()
