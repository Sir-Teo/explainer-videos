from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono, module_box

SHORT = {"assume": r"\mathrm{hyp}", "imp_intro": r"{\Rightarrow}I", "imp_elim": r"{\Rightarrow}E",
         "and_intro": r"{\wedge}I", "and_elim_left": r"{\wedge}E_1", "and_elim_right": r"{\wedge}E_2",
         "or_intro_left": r"{\vee}I_1", "or_intro_right": r"{\vee}I_2", "or_elim": r"{\vee}E",
         "bot_elim": r"{\bot}E", "dne": r"\neg\neg E"}

RULE_TEX = {
    "assume": r"\frac{}{A \vdash A}",
    "imp_intro": r"\frac{\Gamma \vdash B}{\Gamma \setminus A \vdash A \Rightarrow B}",
    "imp_elim": r"\frac{\Gamma \vdash A \Rightarrow B \quad \Delta \vdash A}{\Gamma, \Delta \vdash B}",
    "and_intro": r"\frac{\Gamma \vdash A \quad \Delta \vdash B}{\Gamma, \Delta \vdash A \wedge B}",
    "and_elim_left": r"\frac{\Gamma \vdash A \wedge B}{\Gamma \vdash A}",
    "and_elim_right": r"\frac{\Gamma \vdash A \wedge B}{\Gamma \vdash B}",
    "or_intro_left": r"\frac{\Gamma \vdash A}{\Gamma \vdash A \vee B}",
    "or_intro_right": r"\frac{\Gamma \vdash B}{\Gamma \vdash A \vee B}",
    "or_elim": r"\frac{\Gamma \vdash A \vee B \quad \Delta_1 \vdash C \quad \Delta_2 \vdash C}"
               r"{\Gamma, \Delta_1 \setminus A, \Delta_2 \setminus B \vdash C}",
    "bot_elim": r"\frac{\Gamma \vdash \bot}{\Gamma \vdash A}",
    "dne": r"\frac{\Gamma \vdash \neg\neg A}{\Gamma \vdash A}",
}


def seq_tex(s: str) -> str:
    """A sequent from the kernel's log (unicode) as LaTeX."""
    for a, b in (("⊢", r"\vdash "), ("∧", r"\wedge "), ("∨", r"\vee "), ("⇒", r"\Rightarrow "), ("¬", r"\neg "),
                 ("⊥", r"\bot ")):
        s = s.replace(a, b)
    return s


def gentzen(node, fs=28, gap=1.0, depth=0, out=None):
    """A proof tree drawn Gentzen's way: premises above a bar, the conclusion below, the rule at the bar's right.
    ``out`` collects (depth, parts) so the tree can be revealed from the leaves down."""
    out = [] if out is None else out
    seq = MathTex(seq_tex(node["sequent"]), font_size=fs)
    kids = [gentzen(c, fs, gap, depth + 1, out)[0] for c in node["above"]]
    parts = VGroup()
    if kids:
        row = VGroup(*kids).arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        left, right = row[0][-1].get_left()[0], row[-1][-1].get_right()[0]
        w = max(right - left, seq.width) + 0.2
        bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=1.6, color=GREY_B)
        mid = (left + right) / 2
        bar.move_to([mid, row.get_bottom()[1] - 0.1, 0])
        g = VGroup(row)
    else:
        w = seq.width + 0.2
        bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=1.6, color=GREY_B)
        g = VGroup()
    seq.next_to(bar, DOWN, buff=0.1)
    name = MathTex(SHORT[node["rule"]], font_size=fs - 6, color=HEAD).next_to(bar, RIGHT, buff=0.1)
    parts.add(bar, name, seq)
    out.append((depth, parts))
    g.add(bar, name, seq)
    return g, out


class Assistants(VoiceoverScene):
    def construct(self):
        self.card()
        self.lcf()
        self.rules()
        self.proof()
        self.refused()
        self.systems()
        self.mathematics()

    def card(self):
        card = chapter_card(10, r"Proof assistants", r"Who checks the checker?", lit=(1972, 2014),
                            extra=((1972, r"Milner's LCF"), (2014, r"Flyspeck: \ Kepler, \ checked")), part=PART)
        with self.voiceover("Chapter ten. Proof assistants."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lcf(self):
        size = load("lcf")["size"]
        head = label(r"Milner's idea: \ only the kernel makes theorems", font_size=36).to_edge(UP, buff=0.3)
        outer = RoundedRectangle(width=6.4, height=5.2, corner_radius=0.2, stroke_color=GREY_C, stroke_width=2,
                                 fill_color=GREY_E, fill_opacity=0.25).move_to([-3.4, -0.5, 0])
        ol = label(r"untrusted: \ may be huge, \ clever, \ or wrong", font_size=19, color=GREY_A).next_to(
            outer.get_top(), DOWN, buff=0.2)
        users = VGroup(*[module_box(t, c, font=19) for t, c in ((r"tactics", DATA), (r"proof search", LAM),
                                                       (r"scripts", DATA), (r"you", HEAD))])
        users.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.4)).next_to(ol, DOWN, buff=0.35)
        kern = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.12, stroke_color=KERN, stroke_width=3,
                                fill_color=KERN, fill_opacity=0.2).move_to([-3.4, -2.2, 0])
        kl = VGroup(label(r"kernel", font_size=24, color=KERN),
                    label(rf"{size['kernel_lines']} lines, \ {len(size['rules'])} rules", font_size=18,
                          color=WHITE)).arrange(DOWN, buff=0.08).move_to(kern)
        calls = VGroup(*[Arrow(u.get_bottom(), kern.get_top(), buff=0.08, color=GREY_B, stroke_width=2,
                               max_tip_length_to_length_ratio=0.12) for u in users[2:]])
        thm = MathTex(r"\mathsf{thm}", font_size=34, color=YES).next_to(outer, RIGHT, buff=0.3).set_y(kern.get_y())
        out = Arrow(kern.get_right(), thm.get_left(), buff=0.08, color=YES, stroke_width=3)
        src = code_block([
            "def imp_elim(th1, th2):",
            "    if (not isinstance(th1.concl, Imp)",
            "            or th1.concl.a != th2.concl):",
            "        raise KernelError(\"imp_elim: ...\")",
            "    return Thm(th1.hyps | th2.hyps,",
            "               th1.concl.b, _KEY)",
        ], size=17).move_to([3.6, 1.1, 0])
        sl = label(r"one rule of our kernel \ (modus ponens)", font_size=18, color=GREY_A).next_to(src, UP, buff=0.2)
        ml = wrapped_label(r"Edinburgh LCF's language for writing tactics, \ designed by Milner's group, \ became "
                           r"\textbf{ML}, \ the ancestor of Standard ML and OCaml", 5.2, font_size=19,
                           color=LAM).next_to(src, DOWN, buff=0.6).align_to(src, LEFT)
        with self.voiceover(
            "In 1972 Robin Milner built LCF, a program for checking proofs that could be trusted without trusting "
            "most of it. <bookmark mark='a'/> A theorem is a value of an abstract type, and only the inference rules,"
            " gathered in a small kernel, can make one. <bookmark mark='b'/> Everything else, tactics, proof search, "
            "scripts, the user, can call the rules but cannot forge a result. <bookmark mark='c'/> Here is one rule "
            "of our own kernel: modus ponens checks that the second premise is the antecedent of the first, or "
            "refuses. Our kernel has sixty-nine lines and eleven rules. <bookmark mark='d'/> For Edinburgh LCF, "
            "Milner's group designed a language for writing tactics: ML, the ancestor of Standard ML and OCaml."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(kern), FadeIn(kl))
            self.play(GrowArrow(out), FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(outer), FadeIn(ol), LaggedStart(*[FadeIn(u) for u in users], lag_ratio=0.2))
            self.play(LaggedStart(*[GrowArrow(c) for c in calls], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(sl), FadeIn(src))
            self.play(Indicate(kl[1], color=KERN))
            vo.wait_until("d")
            self.play(FadeIn(ml))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        names = load("lcf")["size"]["rules"]
        head = label(r"Natural deduction: \ the kernel's eleven rules", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup()
        for nm in names:
            f = MathTex(RULE_TEX[nm], font_size=26, color=LAM if nm == "dne" else WHITE)
            t = mono(nm, size=16, color=LAM if nm == "dne" else HEAD)
            cells.add(VGroup(f, t).arrange(DOWN, buff=0.15))
        order = ["assume", "imp_intro", "imp_elim", "and_intro", "and_elim_left", "and_elim_right", "or_intro_left",
                 "or_intro_right", "bot_elim", "dne", "or_elim"]
        assert sorted(order) == sorted(names)
        idx = {nm: k for k, nm in enumerate(names)}
        grid = VGroup(*[cells[idx[nm]] for nm in order[:10]]).arrange_in_grid(rows=3, cols=4, buff=(0.45, 0.4))
        grid.next_to(head, DOWN, buff=0.4)
        last = cells[idx["or_elim"]]
        last.move_to(grid[-1]).shift(RIGHT * 0.2)
        # the eleventh cell takes the two empty slots at the end of the last row
        row3 = VGroup(grid[8], grid[9])
        last.next_to(row3, RIGHT, buff=0.6).align_to(row3, DOWN)
        allg = VGroup(grid, last)
        if allg.width > 13.4:
            allg.scale_to_fit_width(13.4)
        allg.set_x(0)
        seqn = MathTex(r"\Gamma \vdash A", font_size=32, color=YES)
        seql = label(r"a sequent: \ from the hypotheses $\Gamma$, \ the conclusion $A$", font_size=19, color=YES)
        sg = VGroup(seqn, seql).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        groups = {"a": ["assume"], "b": ["imp_intro", "imp_elim"],
                  "c": ["and_intro", "and_elim_left", "and_elim_right", "or_intro_left", "or_intro_right", "or_elim",
                        "bot_elim"], "d": ["dne"]}
        with self.voiceover(
            "The kernel's logic is natural deduction, Gerhard Gentzen's system from the 1930s. A sequent says: from "
            "these hypotheses, this conclusion. <bookmark mark='a'/> Assumption starts every proof: A, from A. "
            "<bookmark mark='b'/> Each connective has a rule to introduce it and one to use it. Implication is "
            "introduced by discharging a hypothesis, and used by modus ponens. <bookmark mark='c'/> Then conjunction,"
            " disjunction, and falsehood, from which anything follows. <bookmark mark='d'/> The eleventh rule, double"
            " negation, is the only classical one; without it the logic is intuitionistic, the logic of Part 14's "
            "programs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sg))
            for mk, nms in groups.items():
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(cells[idx[n]], shift=UP * 0.1) for n in nms], lag_ratio=0.2),
                          run_time=max(1.0, 0.4 * len(nms)))
            self.play(Indicate(cells[idx["dne"]], color=LAM))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        pf = load("lcf")["proofs"]["and_comm"]
        assert pf["closed"] and pf["tautology"]
        head = label(r"A proof, \ built by the kernel", font_size=36).to_edge(UP, buff=0.3)
        tree, parts = gentzen(pf["tree"], fs=28, gap=0.9)
        tree.move_to([-2.9, 0.1, 0])
        if tree.get_left()[0] < -6.8:
            tree.shift(RIGHT * (-6.8 - tree.get_left()[0]))
        by_depth = {}
        for d, p in parts:
            by_depth.setdefault(d, VGroup()).add(p)
        depth = max(by_depth)
        steps = label(rf"{len(pf['steps'])} kernel calls; \ no hypotheses left; \ truth tables agree", font_size=19,
                      color=YES).next_to(tree, DOWN, buff=0.45)
        lean = code_block(["theorem swap (A B : Prop)", "    (h : A ∧ B) : B ∧ A :=", "  And.intro h.2 h.1"],
                          size=19).move_to([4.2, 0.6, 0])
        ll = label(r"the same theorem in Lean 4", font_size=19, color=DATA).next_to(lean, UP, buff=0.25)
        ll.align_to(lean, LEFT)
        lnote = wrapped_label(r"Lean's kernel checks this line as a typed program: \ propositions as types \ "
                              r"(Part 14)", 4.4, font_size=18, color=GREY_A).next_to(lean, DOWN, buff=0.35)
        lnote.align_to(lean, LEFT)
        with self.voiceover(
            "Here is a proof our kernel made: A and B implies B and A. <bookmark mark='a'/> It starts from one "
            "assumption, A and B, used twice. <bookmark mark='b'/> The elimination rules take it apart, into B and "
            "into A. <bookmark mark='c'/> Introduction puts them together the other way round. <bookmark mark='d'/> "
            "Discharging the assumption leaves the theorem with no hypotheses, after five kernel calls, and a truth "
            "table agrees. <bookmark mark='e'/> In Lean the proof is one line, which Lean's kernel checks as a typed "
            "program: Part 14's propositions as types."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in by_depth[depth - k]], lag_ratio=0.3))
            self.play(FadeIn(steps), Indicate(by_depth[0][0][2], color=YES))
            vo.wait_until("e")
            self.play(FadeIn(ll), FadeIn(lean))
            self.play(FadeIn(lnote))
        self.wait(0.4)
        self.clear_scene()

    def refused(self):
        bad = load("lcf")["illegal"]
        assert all(b["refused"] for b in bad)
        head = label(r"What the kernel refuses", font_size=36).to_edge(UP, buff=0.3)
        wall = Rectangle(width=0.35, height=4.4, stroke_color=KERN, stroke_width=2, fill_color=KERN,
                         fill_opacity=0.35).move_to([-1.5, 0.15, 0])
        wl = label(r"kernel", font_size=20, color=KERN).next_to(wall, UP, buff=0.1)
        rows = VGroup()
        ys = np.linspace(1.9, -1.6, len(bad))
        for b, y in zip(bad, ys):
            a = label(b["attempt"].replace("_", r"\_"), font_size=20, color=WHITE)
            if a.width > 4.4:
                a.scale_to_fit_width(4.4)
            a.move_to([-4.5, y, 0])
            arr = Arrow([-1.0 - 0.0, y, 0], [-0.8, y, 0], buff=0, color=GREY_B, stroke_width=2)
            arr.put_start_and_end_on([a.get_right()[0] + 0.15, y, 0], [wall.get_left()[0] - 0.05, y, 0])
            x = Cross(stroke_color=NO, stroke_width=4).scale(0.13).move_to([wall.get_x(), y, 0])
            msg = mono(b["message"], size=16, color=NO).next_to(wall, RIGHT, buff=0.3).set_y(y)
            if msg.get_right()[0] > 6.85:
                msg.scale_to_fit_width(6.85 - msg.get_left()[0])
                msg.next_to(wall, RIGHT, buff=0.3).set_y(y)
            rows.add(VGroup(a, arr, x, msg))
        caveat = wrapped_label(r"Python cannot seal a type as ML does: \ our guard stops honest mistakes, \ not a "
                               r"determined forger. \ The \textbf{de Bruijn criterion}: \ proofs that a small, \ "
                               r"independent checker can recheck", 12.6, font_size=19,
                               color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Every illegal step is refused. <bookmark mark='a'/> Making a theorem directly, without a rule. "
            "<bookmark mark='b'/> Modus ponens, with the wrong antecedent. <bookmark mark='c'/> Taking apart a "
            "conjunction that is really an implication. <bookmark mark='d'/> Double negation, applied to a single "
            "negation. <bookmark mark='e'/> And editing the conclusion of a finished theorem. Each stops at the "
            "kernel with a message. <bookmark mark='f'/> One caution: Python cannot seal a type the way ML can, so "
            "our guard stops honest mistakes, not a determined forger. Serious systems also meet what is called the "
            "de Bruijn criterion: their proofs can be rechecked by a small, independent program."
        ) as vo:
            self.play(FadeIn(head), FadeIn(wall), FadeIn(wl))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), GrowArrow(r[1]))
                self.play(Create(r[2]), FadeIn(r[3]), run_time=0.8)
            vo.wait_until("f")
            self.play(FadeIn(caveat))
        self.wait(0.4)
        self.clear_scene()

    def systems(self):
        head = label(r"Two ways to trust a prover", font_size=36).to_edge(UP, buff=0.3)

        def lane(title, steps, color, who, y):
            t = label(title, font_size=24, color=color)
            boxes = VGroup(*[module_box(s, c, w=2.7, font=19) for s, c in steps]).arrange(RIGHT, buff=0.75)
            arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.06, color=GREY_B,
                                    stroke_width=2, max_tip_length_to_length_ratio=0.15)
                              for k in range(len(boxes) - 1)])
            w = label(who, font_size=19, color=GREY_A)
            g = VGroup(t, VGroup(boxes, arrows), w).arrange(DOWN, buff=0.25)
            g.move_to([0, y, 0])
            return g, boxes, arrows
        l1, b1, a1 = lane(r"LCF style: \ a theorem is an abstract value",
                          [(r"tactic", DATA), (r"kernel rules", KERN), (r"thm", YES)], DATA,
                          r"HOL, \ HOL Light, \ Isabelle", 1.55)
        l2, b2, a2 = lane(r"proof terms: \ a proof is a program",
                          [(r"tactic", DATA), (r"proof term", LAM), (r"type-checking kernel", KERN), (r"thm", YES)],
                          LAM, r"Rocq \ (called Coq until 2025), \ Lean, \ Agda", -1.15)
        foot = wrapped_label(r"either way, \ what sits above the kernel can be enormous, \ automated and wrong: \ "
                             r"the result is still trusted", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Proof assistants trust their kernels in one of two ways. <bookmark mark='a'/> In the LCF style, as in "
            "HOL Light and Isabelle, a theorem is an abstract value that only the kernel's rules can make; HOL "
            "Light's kernel is a few hundred lines. <bookmark mark='b'/> In the other, as in Rocq, called Coq until "
            "2025, and in Lean, a tactic builds a proof term, which is a program, and a small kernel type-checks it. "
            "<bookmark mark='c'/> Either way, what sits above the kernel can be enormous, automated and wrong, and "
            "the result can still be trusted, which is why the frontier chapter can let language models write proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(l1[0]), FadeIn(b1[0]))
            self.play(GrowArrow(a1[0]), FadeIn(b1[1]), GrowArrow(a1[1]), FadeIn(b1[2]), FadeIn(l1[2]))
            vo.wait_until("b")
            self.play(FadeIn(l2[0]), FadeIn(b2[0]))
            for k in range(3):
                self.play(GrowArrow(a2[k]), FadeIn(b2[k + 1]), run_time=0.7)
            self.play(FadeIn(l2[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot), Indicate(b1[1], color=KERN), Indicate(b2[2], color=KERN))
        self.wait(0.4)
        self.clear_scene()

    def mathematics(self):
        head = label(r"Mathematics, \ checked", font_size=36).to_edge(UP, buff=0.3)
        y0 = 0.2
        nl = NumberLine(x_range=[1970, 2025, 5], length=12.4, color=GREY_C, include_numbers=False).move_to([0, y0, 0])
        yrs = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.12)
                       for v in range(1970, 2026, 10)])
        ev = [(1976, r"four colours: \\ Appel and Haken, \\ by computer", HEAD, 1),
              (1998, r"Kepler: \ Hales, \\ heavy computation", HEAD, 1),
              (2005, r"four colours, \\ formal in Coq \\ (Gonthier, \ Werner)", YES, -1),
              (2012, r"odd order \\ theorem, \ Coq", YES, 1),
              (2014, r"Flyspeck: \ Kepler, \\ HOL Light \\ and Isabelle", YES, -1),
              (2022, r"Liquid Tensor \\ Experiment, \\ Lean", YES, 1)]
        items = []
        for yr, txt, col, side in ev:
            d = Dot(nl.n2p(yr), radius=0.08, color=col)
            t = VGroup(label(str(yr), font_size=19, color=col),
                       Tex(r"\begin{tabular}{@{}c@{}}" + txt + r"\end{tabular}", font_size=18, color=GREY_A)
                       ).arrange(DOWN, buff=0.06)
            if side > 0:
                t.next_to(d, UP, buff=0.55)
            else:
                t.next_to(d, DOWN, buff=0.55)
            tick = Line(d.get_center(), t.get_bottom() if side > 0 else t.get_top(), color=col, stroke_width=1.2,
                        stroke_opacity=0.6)
            items.append(VGroup(tick, d, t))
        for k in range(1, len(items)):
            a, b = items[k - 1][2], items[k][2]
            if np.sign(ev[k][3]) == np.sign(ev[k - 1][3]) and b.get_left()[0] < a.get_right()[0] + 0.15:
                b.shift(RIGHT * (a.get_right()[0] + 0.15 - b.get_left()[0]))
        arcs = VGroup(
            CurvedArrow(nl.n2p(1976) + DOWN * 0.15, nl.n2p(2005) + DOWN * 0.15, angle=TAU / 14, color=GREY_B,
                        stroke_width=1.6, tip_length=0.15),
            CurvedArrow(nl.n2p(1998) + DOWN * 0.15, nl.n2p(2014) + DOWN * 0.15, angle=TAU / 14, color=GREY_B,
                        stroke_width=1.6, tip_length=0.15))
        legend = VGroup(label(r"computer-assisted proof", font_size=18, color=HEAD),
                        label(r"checked by a proof assistant", font_size=18, color=YES)).arrange(RIGHT, buff=0.8)
        legend.to_edge(DOWN, buff=0.35)
        ml = label(r"Lean's \textbf{mathlib}: \ a community library of formal mathematics \ (\textit{AI, \ Built}, \ "
                   r"Part 25)", font_size=19, color=DATA).next_to(legend, UP, buff=0.25)
        with self.voiceover(
            "Proof assistants now check real mathematics. <bookmark mark='a'/> In 1976 Kenneth Appel and Wolfgang "
            "Haken proved the four colour theorem with a computer checking many cases, and many mathematicians were "
            "uneasy. <bookmark mark='b'/> In 2005 Georges Gonthier, with Benjamin Werner, completed a proof checked "
            "end to end in Coq. <bookmark mark='c'/> Thomas Hales's 1998 proof of the Kepler conjecture also leaned "
            "on computation; his Flyspeck project finished a formal proof in HOL Light and Isabelle in 2014. "
            "<bookmark mark='d'/> In 2012 Gonthier's team checked the odd order theorem, and in 2022 Lean's users "
            "finished the Liquid Tensor Experiment, Peter Scholze's challenge, on top of mathlib, which AI, Built met"
            " in Part 25."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(yrs), FadeIn(legend))
            vo.wait_until("a")
            self.play(FadeIn(items[0]))
            vo.wait_until("b")
            self.play(FadeIn(items[2]), Create(arcs[0]))
            vo.wait_until("c")
            self.play(FadeIn(items[1]))
            self.play(FadeIn(items[4]), Create(arcs[1]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
            self.play(FadeIn(items[5]), FadeIn(ml))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, LAM, NO, YES)
