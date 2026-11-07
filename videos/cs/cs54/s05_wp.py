from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, grid_table, load,
                                   mono)


def tx(s: str) -> str:
    """One of the instrument's assertions (unicode or ASCII) as LaTeX."""
    s = s.replace("&&", "∧").replace("||", "∨").replace("==>", "⇒").replace("<=", "≤").replace(">=", "≥")
    s = s.replace("==", "=")
    s = re.sub(r"\b([A-Za-z]+)'(\d+)", r"\1'_{\2}", s)
    s = re.sub(r"\b([A-Za-z]{2,})\b", r"\\mathit{\1}", s)
    for a, b in ((">>>", r" \mathbin{>\!\!>\!\!>} "), (">>", r" \mathbin{>\!\!>} "), ("≥", r" \ge "),
                 ("≤", r" \le "), ("∧", r" \,\wedge\, "), ("∨", r" \,\vee\, "), ("¬", r" \neg "),
                 ("⇒", r" \Rightarrow "), ("≠", r" \ne "), ("*", r" \cdot ")):
        s = s.replace(a, b)
    return s


def listing_lines(rows) -> list[str]:
    return ["    " * r["depth"] + r["code"] for r in rows]


SHORT = (("established", r"established on entry"), ("preserved", r"preserved by the body"),
         ("exit", r"exit gives the postcondition"), ("non-negative", r"variant $\ge 0$"),
         ("decreases", r"variant decreases"))

NAMES = {"max": r"max$(a, b)$", "swap": r"swap without a temporary", "gauss": r"Gauss's summation loop",
         "binsearch": r"binary search, \ fixed midpoint", "binsearch_buggy": r"binary search, \ textbook midpoint"}


def short_name(name: str) -> str:
    return next(s for k, s in SHORT if k in name)


class Wp(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.rules()
        self.vcgen()
        self.blast()
        self.table()
        self.scaling()

    def card(self):
        card = chapter_card(4, r"Weakest preconditions, \ checked by SAT", r"Can a machine do the bookkeeping?",
                            lit=(1975, 2008), extra=((1975, r"Dijkstra: \ guarded commands"),
                                                     (2008, r"de Moura and Bj{\o}rner: \ Z3")), part=PART)
        with self.voiceover("Chapter four. Weakest preconditions, checked by SAT."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def definition(self):
        head = label(r"The weakest precondition", font_size=36).to_edge(UP, buff=0.3)
        iff = MathTex(r"\{P\}\ c\ \{Q\}", r"\quad\iff\quad", r"P \Rightarrow \mathit{wp}(c, Q)", font_size=42)
        iff[0].set_color(DATA)
        iff[2].set_color(HEAD)
        iff.next_to(head, DOWN, buff=0.35)
        before = Rectangle(width=5.4, height=3.3, stroke_color=GREY_C, stroke_width=1.5).move_to([-3.3, -0.55, 0])
        after = Rectangle(width=3.4, height=3.3, stroke_color=GREY_C, stroke_width=1.5).move_to([3.6, -0.55, 0])
        lb = label(r"states before", font_size=17, color=GREY_B).next_to(before, DOWN, buff=0.1)
        la = label(r"states after", font_size=17, color=GREY_B).next_to(after, DOWN, buff=0.1)
        wpe = Ellipse(width=4.0, height=2.5, color=HEAD, fill_opacity=0.12).move_to([-3.0, -0.4, 0])
        wpl = MathTex(r"\mathit{wp}(c, Q)", font_size=30, color=HEAD).next_to(wpe.get_top(), DOWN, buff=0.2)
        p1 = Ellipse(width=1.3, height=0.8, color=DATA, fill_opacity=0.25).move_to([-3.9, -0.6, 0])
        p2 = Ellipse(width=1.3, height=0.8, color=DATA, fill_opacity=0.25).move_to([-2.2, -0.75, 0])
        p1l = MathTex(r"P", font_size=26, color=DATA).move_to(p1)
        p2l = MathTex(r"P'", font_size=26, color=DATA).move_to(p2)
        Q = Ellipse(width=2.4, height=1.8, color=YES, fill_opacity=0.15).move_to([3.6, -0.4, 0])
        Ql = MathTex(r"Q", font_size=30, color=YES).next_to(Q.get_top(), DOWN, buff=0.2)
        froms = [[-4.6, -0.2, 0], [-3.3, 0.05, 0], [-1.6, -0.25, 0]]
        tos = [[3.1, -0.6, 0], [3.7, -0.9, 0], [4.2, -0.4, 0]]
        runs = VGroup(*[VGroup(Dot(a, radius=0.06), Dot(b, radius=0.06),
                               Arrow(a, b, buff=0.08, color=HEAD, stroke_width=2,
                                     max_tip_length_to_length_ratio=0.04)) for a, b in zip(froms, tos)])
        oa, ob = [-5.6, -1.9, 0], [2.2, -1.95, 0]
        miss = VGroup(Dot(oa, radius=0.06, color=NO), Dot(ob, radius=0.06, color=NO),
                      DashedLine(oa, ob, buff=0.08, color=NO, stroke_width=1.5))
        missl = label(r"may miss $Q$, \ or never end", font_size=16, color=NO).move_to([3.9, -1.95, 0])
        notes = VGroup(
            wrapped_label(r"$\mathit{wp}(c, Q)$: \ every state from which $c$ is sure to finish in $Q$; \ any valid "
                          r"precondition lies inside it", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"Edsger Dijkstra \ (1975, \ with guarded commands): \ a calculus for deriving programs "
                          r"together with their proofs", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Hoare's rules check a proof; Dijkstra's weakest preconditions compute one. <bookmark mark='a'/> For "
            "a statement c and a postcondition Q, the weakest precondition is the set of all starting states from"
            " which c is sure to finish inside Q. <bookmark mark='b'/> Every valid precondition lies inside it, "
            "so a triple holds exactly when its precondition implies the weakest one. <bookmark mark='c'/> "
            "Dijkstra introduced the idea in 1975, with his guarded commands, as a calculus for deriving programs"
            " together with their proofs. Read as a function from postconditions to preconditions, it turns "
            "proving into calculating."
        ) as vo:
            self.play(FadeIn(head), Create(before), Create(after), FadeIn(lb), FadeIn(la), FadeIn(Q), FadeIn(Ql))
            vo.wait_until("a")
            self.play(FadeIn(wpe), FadeIn(wpl), FadeIn(notes[0]))
            self.play(LaggedStart(*[GrowFromPoint(r, r[0].get_center()) for r in runs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(p1l), FadeIn(p2), FadeIn(p2l), Write(iff))
            self.play(FadeIn(miss), FadeIn(missl))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        g = load("hoare")["programs"]["gauss"]
        fl = load("hoare")["flow"]["gauss"]
        head = label(r"Weakest preconditions, \ rule by rule", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\mathit{wp}(x := e,\ Q)", r"=", r"Q[e/x]", font_size=30),
            MathTex(r"\mathit{wp}(c_1 ;\, c_2,\ Q)", r"=", r"\mathit{wp}(c_1,\ \mathit{wp}(c_2,\ Q))", font_size=30),
            MathTex(r"\mathit{wp}(\mathbf{if}\ b\ \mathbf{then}\ c_1\ \mathbf{else}\ c_2,\ Q)", r"=",
                    r"(b \Rightarrow \mathit{wp}(c_1, Q)) \wedge (\neg b \Rightarrow \mathit{wp}(c_2, Q))",
                    font_size=30),
            MathTex(r"\mathit{wp}(\mathbf{assert}\ p,\ Q)", r"=", r"p \wedge Q", font_size=30),
            MathTex(r"\mathit{wp}(\mathbf{havoc}\ x,\ Q)", r"=", r"\forall x.\ Q", font_size=30),
        )
        for e in eqs:
            e[0].set_color(HEAD)
        eqs.arrange(DOWN, buff=0.2)
        for e in eqs:
            e.shift(RIGHT * (eqs[0][1].get_x() - e[1].get_x()))       # line up the equals signs
        eqs.next_to(head, DOWN, buff=0.35)
        wl = next(st for st in fl if st["code"].startswith("while"))
        s0 = next(st for st in fl if st["code"] == "s = 0")
        i0 = next(st for st in fl if st["code"] == "i = 0")
        vc0 = g["vcs"][0]
        tags = VGroup(label(r"the loop gives its invariant", font_size=18, color=YES),
                      label(r"up through \texttt{s = 0}", font_size=18, color=GREY_A),
                      label(r"up through \texttt{i = 0}", font_size=18, color=GREY_A),
                      label(r"from the precondition: \ VC 1", font_size=18, color=DATA))
        forms = VGroup(MathTex(tx(wl["before"]), font_size=30, color=YES),
                       MathTex(tx(s0["before"]), font_size=30),
                       MathTex(tx(i0["before"]), font_size=30),
                       MathTex(tx(vc0["unicode"]), font_size=30, color=DATA))
        rows = VGroup(*[VGroup(t, f) for t, f in zip(tags, forms)])
        for k, (t, f) in enumerate(zip(tags, forms)):
            t.move_to([-4.6, -0.95 - k * 0.68, 0], aligned_edge=RIGHT).set_x(-2.6, direction=RIGHT)
            f.next_to(t, RIGHT, buff=0.35)
        start = code_block(listing_lines(g["listing"][:3]), size=17).to_corner(DR, buff=0.4)
        with self.voiceover(
            "The rules become equations. <bookmark mark='a'/> Assignment is substitution. A sequence takes the "
            "second statement first, then the first. A conditional splits on its test. An assertion adds a "
            "conjunct, and havoc, an unknown value, means the condition must hold for every value. <bookmark "
            "mark='b'/> Here is our tool on the start of Gauss's loop. The loop contributes its invariant. "
            "<bookmark mark='c'/> Pushing it up through s gets zero writes zero for s; through i gets zero, zero "
            "for i. <bookmark mark='d'/> What remains must follow from the precondition, n at least zero. That "
            "implication is the first verification condition, and it is plainly true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.1) for e in eqs], lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(start), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Indicate(eqs[0], color=WHITE, scale_factor=1.03), FadeIn(tags[1]),
                      ReplacementTransform(forms[0].copy(), forms[1]))
            self.play(Indicate(eqs[1], color=WHITE, scale_factor=1.03), FadeIn(tags[2]),
                      ReplacementTransform(forms[1].copy(), forms[2]))
            vo.wait_until("d")
            self.play(FadeIn(tags[3]), ReplacementTransform(forms[2].copy(), forms[3]))
        self.wait(0.4)
        self.clear_scene()

    def vcgen(self):
        g = load("hoare")["programs"]["gauss"]
        head = label(r"Verification conditions", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(listing_lines(g["listing"]), size=18).next_to(head, DOWN, buff=0.35).to_edge(LEFT,
                                                                                                        buff=0.8)
        loop = next(r for r in g["listing"] if r["kind"] == "while")
        ann = VGroup(
            MathTex(r"\mathit{pre}:\ " + tx(g["pre"]), font_size=26, color=DATA),
            MathTex(r"I:\ " + tx(loop["invariant"]), font_size=26, color=YES),
            MathTex(r"V:\ " + tx(loop["variant"]), font_size=26, color=LAM),
            MathTex(r"\mathit{post}:\ " + tx(g["post"]), font_size=26, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(code, RIGHT, buff=1.0)
        gen = Arrow(ann.get_bottom() + DOWN * 0.05, ann.get_bottom() + DOWN * 0.55, buff=0, color=HEAD,
                    stroke_width=3, max_tip_length_to_length_ratio=0.3)
        forms = VGroup()
        for v in g["vcs"]:
            f = VGroup(MathTex(tx(v["unicode"]), font_size=24))
            if f.width > 9.8 and " ⇒ " in v["unicode"]:       # too long for one line: break at the implication
                hyp, concl = v["unicode"].split(" ⇒ ", 1)
                f = VGroup(MathTex(tx(hyp), font_size=24),
                           MathTex(r"\Rightarrow\ " + tx(concl), font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.1)
                f[1].shift(RIGHT * 0.4)
            if f.width > 9.8:
                f.width = 9.8
            forms.add(f)
        forms.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        forms.next_to(gen, DOWN, buff=0.3).set_x(-3.6, direction=LEFT)
        rows = VGroup()
        for v, f in zip(g["vcs"], forms):
            nm = label(short_name(v["name"]), font_size=18, color=HEAD)
            nm.next_to(f[0], LEFT, buff=0.3).set_x(-3.9, direction=RIGHT)
            rows.add(VGroup(nm, f))
        foot = wrapped_label(r"closed formulas about integers, \ free variables read as ``for all'': \ the program has "
                             r"disappeared; \ all valid means the program is correct, \ one invalid means the program "
                             r"or its annotation is wrong", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Loops are where the calculation needs help. <bookmark mark='a'/> We give the generator the loop's "
            "invariant and a variant. <bookmark mark='b'/> It turns the program into five closed formulas: the "
            "invariant is established on entry, preserved by the body, and together with the exit test gives the "
            "postcondition; the variant stays non-negative, and falls on every pass. <bookmark mark='c'/> Each "
            "formula speaks only about integers. The program has disappeared. If all of them are valid, the "
            "program is correct; if one fails, either the program or its annotation is wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(ann))
            vo.wait_until("b")
            self.play(GrowArrow(gen))
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.35), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def blast(self):
        sw = load("hoare")["programs"]["swap"]["vcs"][0]
        head = label(r"From a formula to clauses", font_size=36).to_edge(UP, buff=0.3)
        names = [r"VC $f$", r"negate: \ $\neg f$", r"bit-blast", r"CNF clauses", r"CDCL \ (Part 26)"]
        boxes = VGroup(*[RoundedRectangle(width=2.15, height=0.62, corner_radius=0.1, stroke_color=KERN if k == 4
                                          else GREY_B, stroke_width=1.8, fill_color=BG, fill_opacity=1)
                         for k in range(5)]).arrange(RIGHT, buff=0.42).next_to(head, DOWN, buff=0.4)
        btxt = VGroup(*[label(n, font_size=19, color=WHITE).move_to(b) for n, b in zip(names, boxes)])
        arrs = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.04, color=GREY_B,
                              stroke_width=2, max_tip_length_to_length_ratio=0.35) for k in range(4)])
        o_ok = label(r"UNSAT: \ $f$ is valid", font_size=19, color=YES)
        o_bad = label(r"SAT: \ a counterexample", font_size=19, color=NO)
        outs = VGroup(o_ok, o_bad).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(boxes[4], DOWN, buff=0.35)
        outs.align_to(boxes[4], RIGHT)
        oarr = Arrow(boxes[4].get_bottom(), outs.get_top(), buff=0.04, color=KERN, stroke_width=2,
                     max_tip_length_to_length_ratio=0.3)
        # a 16-bit adder: two words of Boolean variables and a chain of full adders passing carries
        W, cw, xr = 16, 0.36, -0.4
        xs = [xr - i * cw for i in range(W)]                 # bit i (least significant on the right)

        def bits(y, col):
            return VGroup(*[Square(side_length=cw * 0.75, stroke_color=col, stroke_width=1.2, fill_color=col,
                                   fill_opacity=0.25).move_to([x, y, 0]) for x in xs])
        bx, by = bits(0.55, DATA), bits(0.15, LAM)
        fas = VGroup(*[RoundedRectangle(width=cw * 0.6, height=0.42, corner_radius=0.05, stroke_color=KERN,
                                        stroke_width=1.4, fill_color=BG, fill_opacity=1).move_to([x, -0.45, 0])
                       for x in xs])
        carries = VGroup(*[Arrow(fas[i].get_left(), fas[i + 1].get_right(), buff=0.0, color=KERN, stroke_width=1.5,
                                 max_tip_length_to_length_ratio=0.5) for i in range(W - 1)])
        bs = bits(-1.05, YES)
        tags = VGroup(mono("x", size=18, color=DATA).next_to(bx, LEFT, buff=0.2),
                      mono("y", size=18, color=LAM).next_to(by, LEFT, buff=0.2),
                      label(r"$+$", font_size=20, color=KERN).next_to(fas, LEFT, buff=0.2),
                      mono("x+y", size=16, color=YES).next_to(bs, LEFT, buff=0.12))
        acap = label(r"each 16-bit integer: \ 16 Boolean variables; \ $+$: \ a chain of full adders \ (Part 4)",
                     font_size=18, color=GREY_A).next_to(bs, DOWN, buff=0.25).align_to(bs, LEFT)
        gate = VGroup(
            MathTex(r"v \leftrightarrow (a \wedge b)", font_size=34, color=KERN),
            MathTex(r"(\neg v \vee a)", r"\ \wedge\ ", r"(\neg v \vee b)", r"\ \wedge\ ",
                    r"(v \vee \neg a \vee \neg b)", font_size=28),
            label(r"Tseitin: \ one new variable and three clauses per and-gate", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to([3.8, -0.3, 0])
        stats = label(rf"the swap's VC: \ {sw['vars']:,} variables, \ {sw['clauses']:,} clauses, \ "
                      rf"{sw['conflicts']:,} conflicts, \ {sw['seconds']:.2f} s: \ UNSAT, \ so valid for every 16-bit "
                      rf"$x$, $y$", font_size=21, color=YES).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How does a SAT solver judge a statement about integers? <bookmark mark='a'/> A formula is valid "
            "exactly when its negation has no satisfying assignment. So we negate it, and translate. <bookmark "
            "mark='b'/> Each sixteen-bit integer becomes sixteen Boolean variables, and addition becomes a chain "
            "of full adders passing carries along, the circuit of Part 4. <bookmark mark='c'/> Every gate becomes"
            " a new variable and a few clauses; for an and gate, three. <bookmark mark='d'/> For the swap, the "
            "result is four hundred and twenty-five variables and one thousand two hundred and thirty-nine "
            "clauses. Our CDCL solver from Part 26 shows them unsatisfiable in about a quarter of a second, so "
            "the swap is right for every pair of sixteen-bit values."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]), FadeIn(btxt[0]))
            vo.wait_until("a")
            for k in range(1, 5):
                self.play(GrowArrow(arrs[k - 1]), FadeIn(boxes[k]), FadeIn(btxt[k]), run_time=0.5)
            self.play(GrowArrow(oarr), FadeIn(outs))
            vo.wait_until("b")
            self.play(FadeIn(bx), FadeIn(by), FadeIn(fas), FadeIn(tags), FadeIn(acap))
            self.play(LaggedStart(*[GrowArrow(c) for c in carries], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(gate[0]))
            self.play(FadeIn(gate[1]), FadeIn(gate[2]))
            vo.wait_until("d")
            self.play(FadeIn(stats), Indicate(o_ok, color=YES))
        assert 0.15 < sw["seconds"] < 0.35 and sw["status"] == "valid"   # "about a quarter of a second"
        self.wait(0.4)
        self.clear_scene()

    def table(self):
        progs = load("hoare")["programs"]
        head = label(r"Every program, \ every condition", font_size=36).to_edge(UP, buff=0.3)
        rows, colors = [], []
        for k, p in progs.items():
            nv = len(p["vcs"])
            ok = sum(v["status"] == "valid" for v in p["vcs"])
            rows.append([NAMES[k], f"{p['w']}", f"{nv}", f"{ok}", f"{sum(v['clauses'] for v in p['vcs']):,}",
                         f"{sum(v['seconds'] for v in p['vcs']):.2f} s", r"proved" if p["proved"] else r"refuted"])
            colors.append([WHITE, GREY_A, GREY_A, YES if ok == nv else NO, GREY_A, GREY_A,
                           YES if p["proved"] else NO])
        tab = grid_table([r"program", r"bits", r"VCs", r"valid", r"clauses", r"SAT time", r"verdict"], rows,
                         widths=[4.4, 0.9, 0.9, 0.9, 1.5, 1.5, 1.5], row_h=0.56, font_size=20, colors=colors,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        bad = progs["binsearch_buggy"]
        fails = [v for v in bad["vcs"] if v["status"] != "valid"]
        cex = VGroup(*[label(rf"{short_name(v['name'])}: \ " + ", \\ ".join(
            rf"${tx(k)} = {val:,}$".replace(",", "{,}") for k, val in v["counterexample"].items()),
            font_size=19, color=NO) for v in fails]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cex.next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        cex_l = label(r"the refuted conditions, \ with the solver's counterexamples \ ($c'$, $V'$: \ the unknown "
                      r"comparison and the variant's old value)", font_size=17, color=GREY_B).next_to(
            cex, DOWN, buff=0.2).align_to(cex, LEFT)
        recheck = wrapped_label(r"every counterexample is re-checked by evaluating the formula on it: \ a SAT answer "
                                r"is never taken on trust", 12.4, font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is every program of this part so far. <bookmark mark='a'/> The maximum, the swap and the binary"
            " search loop are proved at sixteen bits. Gauss's loop is proved at eight bits, for a reason we are "
            "about to see. <bookmark mark='b'/> The binary search with the textbook midpoint is refuted: two of "
            "its five conditions fail, each with concrete values from the solver. <bookmark mark='c'/> A "
            "counterexample is never taken on trust. The tool evaluates the formula on the solver's values and "
            "checks that it really is false."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0], tab.rule)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:5]], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[5])))
            self.play(FadeIn(cex), FadeIn(cex_l))
            vo.wait_until("c")
            self.play(FadeIn(recheck))
        self.wait(0.4)
        self.clear_scene()

    def scaling(self):
        sc = load("hoare")["gauss_scaling"]
        head = label(r"Multipliers are hard", font_size=36).to_edge(UP, buff=0.3)
        ms = [r["seconds"] * 1000 for r in sc]
        chart = bar_chart(ms, [rf"{r['w']} bits" for r in sc], [HEAD] * len(sc), height=3.6, bar_w=0.9, gap=0.55,
                          fmt_=lambda v: f"{v:,.0f} ms", font_size=20, log=True)
        chart.move_to([-3.6, -0.5, 0])
        cap = label(r"SAT time for Gauss's two product conditions \ (log scale)", font_size=18, color=GREY_A).next_to(
            chart, UP, buff=0.35)
        assert all(all(s == "valid" for s in r["status"]) for r in sc)
        notes = VGroup(
            wrapped_label(r"comparing two multipliers is the classic hard case for SAT: \ each two bits of word "
                          r"cost several times as long", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{SMT} solvers such as Z3 \ (de Moura and Bj{\o}rner, \ Microsoft Research, \ "
                          r"2008) \ pair a SAT search with decision procedures for arithmetic, \ arrays and "
                          r"bit-vectors; \ Dafny hands its conditions to Z3", 5.6, font_size=20, color=YES),
            wrapped_label(r"an UNSAT answer can come with a proof that a small independent checker verifies: \ "
                          r"Chapter 10's theme", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Multiplication is where this approach strains. <bookmark mark='a'/> Gauss's conditions compare two "
            "products, and multipliers are the classic hard case for SAT. Every two extra bits of word cost our "
            "solver several times as long: from five milliseconds at four bits to over two seconds at ten. "
            "<bookmark mark='b'/> Industrial verifiers hand their conditions to SMT solvers such as Z3, from "
            "Microsoft Research, which pair a SAT search with decision procedures for arithmetic, arrays and bit-"
            "vectors. Dafny, for one, works this way. <bookmark mark='c'/> And when a solver says unsatisfiable, "
            "it can also emit a proof that a small independent checker verifies, a theme that Chapter ten makes "
            "central."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n))
                                    for b, v, n in zip(chart.bars, chart.vals, chart.names)], lag_ratio=0.4),
                      FadeIn(chart[0]), run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (mono,)
