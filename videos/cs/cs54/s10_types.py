from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono, tag_box


def run_tree(depth=4, top=(-3.8, 2.2), width=5.8, dy=1.15):
    """Every execution of a program drawn as a binary tree: nodes by level, and the edge into each node."""
    nodes, edges = {}, {}
    for d in range(depth + 1):
        n = 2 ** d
        for k in range(n):
            x = top[0] - width / 2 + width * (k + 0.5) / n
            nodes[(d, k)] = Dot([x, top[1] - d * dy, 0], radius=0.055, color=GREY_B)
            if d:
                p = nodes[(d - 1, k // 2)]
                edges[(d, k)] = Line(p.get_center(), nodes[(d, k)].get_center(), color=GREY_D, stroke_width=1.8)
    return nodes, edges


def path_edges(edges, depth, leaf):
    """The edges from the root to one leaf."""
    return [edges[(d, leaf >> (depth - d))] for d in range(1, depth + 1)]


class Types(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.abstract()
        self.refine()
        self.midpoint()
        self.liquid()
        self.spectrum()

    def card(self):
        card = chapter_card(9, r"Types as lightweight proofs", r"What does a type checker prove?",
                            lit=(1978, 2008), extra=((1978, r"Milner: \ well-typed programs cannot go wrong"),
                                                     (2008, r"liquid types")), part=PART)
        with self.voiceover("Chapter nine. Types as lightweight proofs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"A theorem about every run", font_size=36).to_edge(UP, buff=0.3)
        depth = 4
        nodes, edges = run_tree(depth)
        tree = VGroup(*edges.values(), *nodes.values())
        cap = label(r"every execution of one program \ (schematic)", font_size=18, color=GREY_B).next_to(
            tree, DOWN, buff=0.3)
        tests = [3, 9, 14]
        lit = VGroup(*[e.copy().set_color(DATA).set_stroke(width=3.5) for t in tests for e in path_edges(edges, depth, t)])
        tdots = VGroup(*[nodes[(depth, t)].copy().set_color(DATA).scale(1.6) for t in tests])
        tl = label(r"three tests: \ three paths", font_size=19, color=DATA).next_to(cap, DOWN, buff=0.15)
        allp = VGroup(*[e.copy().set_color(YES).set_stroke(width=2.6) for e in edges.values()])
        al = label(r"one type check: \ every path", font_size=19, color=YES).next_to(cap, DOWN, buff=0.15)
        rows = VGroup(
            MathTex(r"\vdash e : \tau", font_size=34, color=HEAD),
            MathTex(r"\vdash e : \tau", r"\;\Rightarrow\;", r"e \text{ is a value}", r"\;\vee\;",
                    r"\exists e'.\ e \to e'", font_size=30),
            MathTex(r"\vdash e : \tau", r"\;\wedge\;", r"e \to e'", r"\;\Rightarrow\;", r"\vdash e' : \tau",
                    font_size=30),
            MathTex(r"\vdash e : \tau", r"\;\wedge\;", r"e \to^{*} e'", r"\;\Rightarrow\;",
                    r"e' \text{ is not stuck}", font_size=30, color=YES),
        )
        whys = VGroup(label(r"the checker's verdict, \ once, \ before any run", font_size=18, color=GREY_A),
                      label(r"progress \ (Part 14)", font_size=18, color=GREY_A),
                      label(r"preservation \ (Part 14)", font_size=18, color=GREY_A),
                      label(r"by induction on the number of steps", font_size=18, color=YES))
        col = VGroup(*[VGroup(r, w).arrange(DOWN, buff=0.12, aligned_edge=LEFT) for r, w in zip(rows, whys)])
        col.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([3.3, 0.1, 0])
        with self.voiceover(
            "A type checker proves a theorem about every run of a program. <bookmark mark='a'/> Picture every "
            "execution as a branch of a tree. Tests walk a few branches. <bookmark mark='b'/> A type checker reads "
            "the code once and speaks for all of them. <bookmark mark='c'/> Part 14 proved what its verdict means. "
            "Progress: a well-typed term is a value, or it can take a step. <bookmark mark='d'/> Preservation: a step"
            " keeps the type. <bookmark mark='e'/> Chain the two by induction on the number of steps, and a well-"
            "typed program never gets stuck. That is Milner's slogan: well-typed programs cannot go wrong."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(VGroup(*edges.values())), FadeIn(VGroup(*nodes.values())), FadeIn(cap), run_time=1.5)
            self.play(Create(lit), FadeIn(tdots), FadeIn(tl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(tl), FadeIn(al), Create(allp), run_time=1.5)
            self.play(FadeIn(col[0]))
            vo.wait_until("c")
            self.play(FadeIn(col[1]))
            vo.wait_until("d")
            self.play(FadeIn(whys[2]), TransformMatchingTex(rows[0].copy(), rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(whys[3]), TransformMatchingTex(rows[2].copy(), rows[3]))
            self.play(Indicate(rows[3], color=YES, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def abstract(self):
        head = label(r"A type checker is an abstract interpreter", font_size=36).to_edge(UP, buff=0.3)
        pos = {"if": (-3.4, 1.7), "b": (-5.4, 0.3), "+": (-3.4, 0.3), "0": (-1.4, 0.3), "x": (-4.3, -1.1),
               "1": (-2.5, -1.1)}
        txt = {"if": "if", "b": "b", "+": "+", "0": "0", "x": "x", "1": "1"}
        boxes = {k: tag_box(txt[k], color=GREY_B, size=22, w=0.9, h=0.55).move_to([*pos[k], 0]) for k in pos}
        links = [("if", "b"), ("if", "+"), ("if", "0"), ("+", "x"), ("+", "1")]
        lines = VGroup(*[Line(boxes[a].get_bottom(), boxes[b].get_top(), buff=0.05, color=GREY_D, stroke_width=1.8)
                         for a, b in links])
        src = mono("if b then x + 1 else 0", size=22, color=WHITE).next_to(boxes["if"], UP, buff=0.35)
        ty = {"b": (r"\mathsf{bool}", LAM), "x": (r"\mathsf{int}", DATA), "1": (r"\mathsf{int}", DATA),
              "0": (r"\mathsf{int}", DATA), "+": (r"\mathsf{int}", DATA), "if": (r"\mathsf{int}", YES)}
        tys = {k: MathTex(t, font_size=26, color=c).next_to(boxes[k], RIGHT if k != "if" else LEFT, buff=0.12)
               for k, (t, c) in ty.items()}
        rule = MathTex(r"\frac{\ e_1 : \mathsf{bool} \quad e_2 : \tau \quad e_3 : \tau\ }"
                       r"{\ \mathtt{if}\ e_1\ \mathtt{then}\ e_2\ \mathtt{else}\ e_3 : \tau\ }", font_size=30)
        rl = label(r"the rule for \texttt{if}: \ both branches, \ one type", font_size=18, color=GREY_A)
        gam = VGroup(MathTex(r"\gamma(\mathsf{int}) = \{\dots, -1, 0, 1, \dots\}", font_size=28, color=DATA),
                     MathTex(r"\gamma(\mathsf{bool}) = \{\mathit{true}, \mathit{false}\}", font_size=28, color=LAM))
        gl = label(r"each type stands for a set of values, \ as an interval did", font_size=18, color=GREY_A)
        right = VGroup(rule, rl, gam.arrange(DOWN, buff=0.15, aligned_edge=LEFT), gl).arrange(
            DOWN, buff=0.22).move_to([3.5, 1.2, 0])
        rej = mono('(if true then 1 else "no") + 1', size=22, color=NO)
        rejl = wrapped_label(r"never goes wrong, \ yet rejected: \ the branches' types differ. \ Sound, \ so "
                             r"incomplete \ (Rice, \ Part 25)", 5.6, font_size=19, color=NO)
        rg = VGroup(rej, rejl).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(right, DOWN, buff=0.55)
        rg.align_to(right, LEFT)
        cite = note(r"Cousot, \ ``Types as abstract interpretations'' \ (1997)", font_size=17).to_edge(DOWN, buff=0.3)
        cite.to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "Why is checking so cheap? <bookmark mark='a'/> A type checker is an abstract interpreter, in the sense "
            "of chapter eight: it runs the program on types instead of values. <bookmark mark='b'/> Types flow up the"
            " tree. x plus one is an int; both branches of the if are ints; so the whole expression is an int. "
            "<bookmark mark='c'/> Patrick Cousot made the connection precise in 1997. <bookmark mark='d'/> And like "
            "intervals, the abstraction loses information. This expression never goes wrong, because its condition is"
            " always true, but its two branches have different types, so it is rejected. Sound, and therefore "
            "incomplete."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b) for b in boxes.values()], Create(lines))
            vo.wait_until("a")
            self.play(FadeIn(gam), FadeIn(gl))
            vo.wait_until("b")
            self.play(*[FadeIn(tys[k], shift=UP * 0.1) for k in ("b", "x", "1", "0")])
            self.play(FadeIn(tys["+"], shift=UP * 0.1))
            self.play(FadeIn(rule), FadeIn(rl))
            self.play(FadeIn(tys["if"], shift=UP * 0.1), Indicate(boxes["if"], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(cite))
            vo.wait_until("d")
            self.play(FadeIn(rej), FadeIn(rejl))
        self.wait(0.4)
        self.clear_scene()

    def refine(self):
        head = label(r"Refinement types: \ a type plus a predicate", font_size=36).to_edge(UP, buff=0.3)
        nl = NumberLine(x_range=[-4, 12, 1], length=8.8, color=GREY_C, include_numbers=False).move_to([-2.1, 1.3, 0])
        nums = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.1)
                        for v in range(-4, 13, 2)])
        n_val = 8

        def band(a, b, y, color, open_left=False, open_right=False):
            x0 = nl.n2p(a)[0] - (0.3 if open_left else 0.12)
            x1 = nl.n2p(b)[0] + (0.3 if open_right else 0.12)
            return Rectangle(width=x1 - x0, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.75).move_to(
                [(x0 + x1) / 2, y, 0])
        b_int = band(-4, 12, 0.2, GREY_B, True, True)
        b_nat = band(0, 12, -0.35, DATA, False, True)
        b_idx = band(0, n_val - 1, -0.9, YES)
        tx = [MathTex(r"\mathsf{int}", font_size=28, color=GREY_A),
              MathTex(r"\mathsf{nat} = \{\, v : \mathsf{int} \mid 0 \le v \,\}", font_size=28, color=DATA),
              MathTex(r"\mathsf{idx}(n) = \{\, v : \mathsf{int} \mid 0 \le v < n \,\}", font_size=28, color=YES)]
        for t, b in zip(tx, (b_int, b_nat, b_idx)):
            t.next_to(nl, RIGHT, buff=0.6).set_y(b.get_y())
            if t.get_right()[0] > 6.85:
                t.shift(LEFT * (t.get_right()[0] - 6.85))
        ex = label(rf"drawn with $n = {n_val}$ \ (illustrative)", font_size=17, color=GREY_B).next_to(b_idx, DOWN,
                                                                                                    buff=0.15)
        ex.align_to(b_idx, LEFT)
        rows = VGroup(
            MathTex(r"\{\, v \mid p \,\}", r"\;<:\;", r"\{\, v \mid q \,\}", font_size=34),
            MathTex(r"\forall v.\ ", r"p", r"\;\Rightarrow\;", r"q", font_size=34),
            MathTex(r"\forall v.\ ", r"0 \le v < n", r"\;\Rightarrow\;", r"0 \le v", font_size=34, color=YES),
        )
        whys = VGroup(label(r"a subtype \ldots", font_size=19, color=GREY_A),
                      label(r"\ldots is a subset: \ an implication", font_size=19, color=GREY_A),
                      label(r"so $\mathsf{idx}(n) <: \mathsf{nat}$: \ valid", font_size=19, color=YES))
        lines = VGroup(*[VGroup(r, w).arrange(RIGHT, buff=0.5) for r, w in zip(rows, whys)])
        lines.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(ex, DOWN, buff=0.45).set_x(0)
        for r in rows[1:]:
            r.shift(RIGHT * (rows[0][1].get_x() - r[2].get_x()))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5)
        cite = note(r"Freeman and Pfenning, \ ``Refinement types for ML'' \ (1991)", font_size=17).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Tim Freeman and Frank Pfenning introduced refinement types in 1991. <bookmark mark='a'/> A refinement "
            "type is a base type with a predicate. Int is every integer. <bookmark mark='b'/> The naturals are the "
            "integers v with v at least zero. <bookmark mark='c'/> The valid indices of an array of length n run from"
            " zero up to n, excluded. <bookmark mark='d'/> A subtype is a subset, which is an implication: whatever "
            "satisfies p satisfies q. <bookmark mark='e'/> So every index is a natural, because zero at most v below "
            "n implies zero at most v. Type checking has become logic, and the logic can go to a solver."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nl), FadeIn(nums), FadeIn(cite))
            vo.wait_until("a")
            self.play(GrowFromEdge(b_int, LEFT), FadeIn(tx[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b_nat, LEFT), FadeIn(tx[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b_idx, LEFT), FadeIn(tx[2]), FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def midpoint(self):
        m = load("hoare")["midpoints"]
        good = next(x for x in m if x["mid"] == "lo + ((hi - lo) >> 1)" and x["pre"].startswith("0 <= lo"))
        bad = m[0]
        assert good["status"] == "valid" and bad["status"] == "invalid"
        ce = bad["counterexample"]
        head = label(r"Bloch's bug as a type error", font_size=36).to_edge(UP, buff=0.3)
        sig = VGroup(
            MathTex(r"lo : \{\, v \mid 0 \le v \,\}", font_size=30, color=DATA),
            MathTex(r"hi : \{\, v \mid lo < v \,\}", font_size=30, color=DATA),
            MathTex(r"mid : \{\, v \mid lo \le v < hi \,\}", font_size=30, color=HEAD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        code = mono(f"mid = {good['mid']}", size=22)
        left = VGroup(sig, code).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.4)
        left.to_edge(LEFT, buff=0.6)
        rows = VGroup(
            MathTex(r"\{\, v \mid v = m \,\}", r"\;<:\;", r"\{\, v \mid lo \le v < hi \,\}", font_size=32),
            MathTex(r"0 \le lo \wedge lo < hi", r"\;\Rightarrow\;", r"lo \le m < hi", font_size=32),
            MathTex(r"0 \le lo \wedge lo < hi", r"\;\Rightarrow\;", r"lo \le lo + ((hi - lo) \gg 1) < hi",
                    font_size=32, color=YES),
        )
        whys = VGroup(label(r"the expression's exact type, \ against the declared one", font_size=18, color=GREY_A),
                      label(r"the facts in scope imply the predicate, \ with $m$ for $v$", font_size=18,
                            color=GREY_A),
                      label(r"$m$ written out: \ the verification condition of chapter 3", font_size=18,
                            color=YES))
        col = VGroup(*[VGroup(r, w).arrange(DOWN, buff=0.1, aligned_edge=LEFT) for r, w in zip(rows, whys)])
        col.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(left, RIGHT, buff=0.7).align_to(left, UP)
        if col.get_right()[0] > 6.85:
            col.shift(LEFT * (col.get_right()[0] - 6.85))
        ok = wrapped_label(rf"our SAT solver, \ 16-bit words: \ \textbf{{valid}} \ ({good['vars']:,} variables, \ "
                           rf"{good['clauses']:,} clauses, \ {good['seconds']:.2f} s): \ it type-checks", 6.2,
                           font_size=19, color=YES)
        badc = mono(f"mid = {bad['mid']}", size=22, color=NO)
        badl = wrapped_label(rf"\textbf{{invalid}}: \ $lo = {format(ce['lo'], ',').replace(',', '{,}')}$, \ $hi = {format(ce['hi'], ',').replace(',', '{,}')}$ \ "
                             r"overflows the sum: \ a \textbf{type error}, \ at compile time", 6.2, font_size=19,
                             color=NO)
        okg = VGroup(ok).next_to(col, DOWN, buff=0.4).align_to(col, LEFT)
        badg = VGroup(badc, badl).arrange(RIGHT, buff=0.45).next_to(okg, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "The hook's midpoint, as a type. <bookmark mark='a'/> Declare low a natural and high greater than low, "
            "and demand that mid lie from low up to high, excluded. <bookmark mark='b'/> The checker gives the "
            "expression its exact type, v equals m, and asks whether that is a subtype. <bookmark mark='c'/> Under "
            "the facts in scope, that is an implication, <bookmark mark='d'/> and written out it is exactly the "
            "verification condition our SAT solver handled in chapter three. <bookmark mark='e'/> For the repaired "
            "midpoint it is valid over sixteen-bit words, so the program type-checks. <bookmark mark='f'/> For "
            "Bloch's original line the solver's counterexample becomes a type error: the bug, rejected before the "
            "program runs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in sig], lag_ratio=0.3), FadeIn(code))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            vo.wait_until("c")
            self.play(FadeIn(whys[1]), TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(whys[2]), TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(okg))
            vo.wait_until("f")
            self.play(FadeIn(badg))
            self.play(Indicate(badc, color=NO))
        self.wait(0.4)
        self.clear_scene()

    def liquid(self):
        head = label(r"Inferring refinements: \ liquid types", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["# n : nat,  len(a) == n", "i = 0", "while i < n:      # i : {v | K}",
                           "    a[i] = 0      # needs 0 <= i < n", "    i = i + 1"], size=20)
        code.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        quals = [r"0 \le v", r"v = 0", r"v < n", r"v \le n"]
        chips = VGroup()
        for q in quals:
            t = MathTex(q, font_size=30, color=WHITE)
            box = RoundedRectangle(width=t.width + 0.4, height=0.55, corner_radius=0.08, stroke_color=HEAD,
                                   stroke_width=1.8, fill_color=BG, fill_opacity=1)
            t.move_to(box)
            chips.add(VGroup(box, t))
        chips.arrange(RIGHT, buff=0.3).next_to(code, RIGHT, buff=0.8).align_to(code, UP)
        ql = label(r"qualifiers: \ candidate facts for $K$", font_size=18, color=HEAD).next_to(chips, DOWN, buff=0.15)
        ql.align_to(chips, LEFT)
        checks = VGroup(
            MathTex(r"v = 0", r"\;\Rightarrow\;", r"q", font_size=30),
            MathTex(r"K[i] \wedge i < n \wedge v = i + 1", r"\;\Rightarrow\;", r"q", font_size=30),
            MathTex(r"K[i] \wedge i < n", r"\;\Rightarrow\;", r"0 \le i < n", font_size=30, color=YES),
        )
        cl = VGroup(label(r"on entry: \ $i = 0$; \ $0 < n$ may fail \ ($n = 0$)", font_size=18, color=GREY_A),
                    label(r"round the loop: \ $i + 1 = 0$ fails; \ a second round removes nothing", font_size=18,
                          color=GREY_A),
                    label(r"$K = 0 \le v \wedge v \le n$: \ the access is in bounds", font_size=18, color=YES))
        col = VGroup(*[VGroup(c, w).arrange(DOWN, buff=0.1, aligned_edge=LEFT) for c, w in zip(checks, cl)])
        col.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(ql, DOWN, buff=0.5).align_to(chips, LEFT)
        ill = note(r"illustrative, \ worked by hand over mathematical integers", font_size=17).next_to(code, DOWN,
                                                                                                    buff=0.35)
        ill.align_to(code, LEFT)
        cite = wrapped_label(r"Rondon, \ Kawaguchi and Jhala \ (2008): \ a fixpoint over conjunctions of "
                             r"qualifiers, \ predicate abstraction \ (chapter 8's iteration, \ with facts in place "
                             r"of intervals)", 5.4, font_size=18, color=GREY_B).next_to(ill, DOWN, buff=0.35)
        cite.align_to(code, LEFT)

        def strike(chip):
            return Line(chip.get_left(), chip.get_right(), color=NO, stroke_width=3)
        with self.voiceover(
            "Liquid types, from Patrick Rondon, Ming Kawaguchi and Ranjit Jhala in 2008, infer refinements. <bookmark"
            " mark='a'/> The loop counter's type is an unknown, K. The programmer supplies candidate facts, called "
            "qualifiers. <bookmark mark='b'/> Start by assuming all of them. On entry i is zero, which need not be "
            "less than n, so that one goes. <bookmark mark='c'/> Round the loop, i plus one is not zero, so that one "
            "goes too. Another round removes nothing: a fixpoint, as in chapter eight. <bookmark mark='d'/> So i lies"
            " from zero to n, and with the loop's test every access to a of i is in bounds, with no annotation on the"
            " loop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.25), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            s1 = strike(chips[2])
            self.play(Create(s1), chips[2].animate.set_opacity(0.35))
            vo.wait_until("c")
            self.play(FadeIn(col[1]))
            s2 = strike(chips[1])
            self.play(Create(s2), chips[1].animate.set_opacity(0.35))
            self.play(chips[0][0].animate.set_stroke(YES), chips[3][0].animate.set_stroke(YES))
            vo.wait_until("d")
            self.play(FadeIn(col[2]), FadeIn(cite))
        self.wait(0.4)
        self.clear_scene()

    def spectrum(self):
        head = label(r"How much a type can say", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=7.4, y_length=5.0,
                  axis_config={"color": GREY_C, "include_ticks": False, "tip_length": 0.15}).move_to([-2.4, -0.55, 0])
        xl = label(r"what the programmer must write", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = label(r"what is proved", font_size=18, color=GREY_A).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
        pts = [((1.2, 2.0), DATA, r"simple types", r"no stuck programs \ (Part 14)"),
               ((3.4, 4.2), KERN, r"ownership types", r"no use after free \ (Rust, \ Part 55)"),
               ((5.6, 6.4), HEAD, r"refinement types", r"bounds, \ invariants \ (LiquidHaskell, \ F$^*$)"),
               ((8.2, 8.8), YES, r"dependent types", r"full correctness \ (Rocq, \ Lean, \ Agda)")]
        dots, tags = VGroup(), VGroup()
        for (x, y), c, nm, what in pts:
            d = Dot(ax.c2p(x, y), radius=0.1, color=c)
            t = VGroup(label(nm, font_size=20, color=c), label(what, font_size=17, color=GREY_A)).arrange(
                DOWN, buff=0.06, aligned_edge=LEFT).next_to(d, RIGHT, buff=0.2)
            dots.add(d)
            tags.add(t)
        steps = VGroup(*[Line(dots[k].get_center(), dots[k + 1].get_center(), color=GREY_D, stroke_width=2)
                         for k in range(len(dots) - 1)])
        sch = note(r"schematic", font_size=17).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        side = wrapped_label(r"at the top, \ a type is a full specification \ and a program of that type is its "
                             r"proof: \ the type checker has become a proof checker", 3.2, font_size=19,
                             color=YES).move_to([5.2, -1.6, 0])
        for t in tags:
            if t.get_right()[0] > 6.85:
                t.shift(LEFT * (t.get_right()[0] - 6.85))
        with self.voiceover(
            "Types form a ladder. <bookmark mark='a'/> Simple types, like those of Part 14 and of our own compiler's "
            "checker, cost almost nothing and rule out stuck programs. <bookmark mark='b'/> Ownership types, Rust's, "
            "to which Part 55 returns, rule out use after free and data races in safe code. <bookmark mark='c'/> "
            "Refinement types, in LiquidHaskell and F star, prove bounds and invariants, with a solver doing the "
            "work. <bookmark mark='d'/> At the top, dependent types can state full functional correctness, and the "
            "programmer writes the proof. There a type checker is a proof checker, which is the next chapter's "
            "subject."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(dots[k], scale=0.5), FadeIn(tags[k])]
                if k:
                    anims.append(Create(steps[k - 1]))
                self.play(*anims)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
