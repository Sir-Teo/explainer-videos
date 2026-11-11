from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def sem(e: str) -> str:
    """The relational reading of a type (TeX)."""
    return r"[\![\," + e + r"\,]\!]"


def pct(x: float) -> str:
    return f"{100 * x:.0f}" + r"\%"


def cells(values, color=WHITE, w=0.62, h=0.42, fs=22, bad=()):
    """A list drawn as a row of boxes; entries at positions in ``bad`` in red."""
    g = VGroup()
    for i, v in enumerate(values):
        c = NO if i in bad else color
        r = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.4, fill_color=BG, fill_opacity=1)
        t = MathTex(str(v), font_size=fs, color=c)
        if t.width > w - 0.08:
            t.scale_to_fit_width(w - 0.08)
        g.add(VGroup(r, t.move_to(r)))
    return g.arrange(RIGHT, buff=0.05)


def derive(self, rows, whys, marks, vo, run_time=1.3):
    """Write the first row, then grow each next row out of a copy of the previous one at its bookmark."""
    self.play(Write(rows[0]), FadeIn(whys[0]))
    for k, mk in enumerate(marks, start=1):
        vo.wait_until(mk)
        self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=run_time)


class Parametricity(VoiceoverScene):
    def construct(self):
        self.card()
        self.abstraction()
        self.relations()
        self.free_r()
        self.checked()
        self.sort()
        self.limits()

    def card(self):
        card = chapter_card(6, r"Theorems for free", r"What does a type promise about every program of that type?",
                            lit=(1983, 1989),
                            extra=((1983, r"Reynolds: \ types, \ abstraction and parametric polymorphism"),
                                   (1989, r"Wadler: \ Theorems for free!")), part=PART)
        with self.voiceover("Chapter six. Theorems for free. What does a type promise about every program of that "
                            "type?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ Reynolds: abstraction as a relation
    def abstraction(self):
        head = label(r"Reynolds: \ two representations, \ one behaviour", font_size=36).to_edge(UP, buff=0.3)
        impls = VGroup(
            VGroup(label(r"counter $A$", font_size=22, color=DATA),
                   mono("start = 0", size=18, color=WHITE), mono("inc n  = n + 1", size=18, color=WHITE),
                   mono("read n = n", size=18, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"counter $B$", font_size=22, color=LAM),
                   mono("start = 0", size=18, color=WHITE), mono("inc m  = m - 1", size=18, color=WHITE),
                   mono("read m = -m", size=18, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        xa, xb = impls[0].get_x(), impls[1].get_x()
        ys = [-0.15, -1.05, -1.95, -2.85]
        sa = VGroup(*[MathTex(str(k), font_size=28, color=DATA).move_to([xa, y, 0]) for k, y in enumerate(ys)])
        sb = VGroup(*[MathTex(str(-k), font_size=28, color=LAM).move_to([xb, y, 0]) for k, y in enumerate(ys)])
        inca = VGroup(*[Arrow(sa[k].get_bottom(), sa[k + 1].get_top(), buff=0.08, color=GREY_B, stroke_width=2,
                              max_tip_length_to_length_ratio=0.25) for k in range(3)])
        incb = VGroup(*[Arrow(sb[k].get_bottom(), sb[k + 1].get_top(), buff=0.08, color=GREY_B, stroke_width=2,
                              max_tip_length_to_length_ratio=0.25) for k in range(3)])
        il = label(r"\textsf{inc}", font_size=18, color=GREY_B).next_to(inca[0], LEFT, buff=0.12)
        rel = VGroup(*[DashedLine(sa[k].get_right(), sb[k].get_left(), buff=0.15, color=KERN, stroke_width=2,
                                  dash_length=0.1) for k in range(4)])
        rl = MathTex(r"n \mathrel{R} m \iff m = -n", font_size=26, color=KERN).next_to(rel[0], UP, buff=0.12)
        side = VGroup(
            wrapped_label(r"a client sees the hidden state only through \textsf{start}, \ \textsf{inc} and "
                          r"\textsf{read}", 5.6, font_size=22, color=WHITE),
            wrapped_label(r"$R$ is respected: \ \textsf{start} relates to \textsf{start}, \ \textsf{inc} keeps "
                          r"related states related, \ \textsf{read} gives equal numbers", 5.6, font_size=21,
                          color=KERN),
            wrapped_label(r"so no client polymorphic in the state's type can tell $A$ from $B$", 5.6,
                          font_size=21, color=YES),
            wrapped_label(r"``Type structure is a syntactic discipline for enforcing levels of abstraction.'' \ "
                          r"--- Reynolds, \ 1983", 5.6, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -0.5, 0])
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        ill = note(r"illustrative counters", font_size=16).to_corner(DL, buff=0.2)
        with self.voiceover(
            "John Reynolds asked what it means for a type to hide something. <bookmark mark='a'/> Here are two "
            "counters. One counts up from zero; the other counts down, and reads its state negated. <bookmark "
            "mark='b'/> A client sees the state only through start, increment and read. <bookmark mark='c'/> Relate "
            "n in the first to minus n in the second. The starts are related, increment keeps related states "
            "related, and read gives equal numbers. <bookmark mark='d'/> Reynolds' abstraction theorem, of nineteen "
            "eighty-three, says that then no client that is polymorphic in the hidden type can tell the two apart. "
            "<bookmark mark='e'/> In his words, type structure is a syntactic discipline for enforcing levels of "
            "abstraction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(impls), FadeIn(ill))
            self.play(FadeIn(sa[0]), FadeIn(sb[0]))
            for k in range(3):
                self.play(GrowArrow(inca[k]), GrowArrow(incb[k]), FadeIn(sa[k + 1]), FadeIn(sb[k + 1]),
                          *([FadeIn(il)] if k == 0 else []), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(r) for r in rel], lag_ratio=0.3), FadeIn(rl), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ every type as a relation
    def relations(self):
        head = label(r"Every type, \ read as a relation", font_size=36).to_edge(UP, buff=0.3)
        xl, xr = -6.3, -4.3
        ys = [-2.4, -1.05, 0.3, 1.75]
        cols = [DATA, HEAD, LAM, YES]
        rails = VGroup(Line([xl, -2.9, 0], [xl, 2.5, 0], color=GREY_C, stroke_width=3),
                       Line([xr, -2.9, 0], [xr, 2.5, 0], color=GREY_C, stroke_width=3))
        rungs = VGroup(*[Line([xl, y, 0], [xr, y, 0], color=c, stroke_width=5) for y, c in zip(ys, cols)])
        tnames = VGroup(*[MathTex(s, font_size=24, color=c).next_to(r, UP, buff=0.08) for s, r, c in zip(
            (r"\mathsf{Int}", r"A \to B", r"[A]", r"\forall \alpha.\ A"), rungs, cols)])
        fs = 28
        defs = VGroup(
            MathTex(r"x \;" + sem(r"\mathsf{Int}") + r"\; y", r"\iff", r"x = y", font_size=fs, color=DATA),
            MathTex(r"f \;" + sem(r"A \to B") + r"\; g", r"\iff", r"x \;" + sem("A") + r"\; y \implies f\,x \;"
                    + sem("B") + r"\; g\,y", font_size=fs, color=HEAD),
            MathTex(r"xs \;" + sem("[A]") + r"\; ys", r"\iff", r"\text{same length, related element by element}",
                    font_size=fs, color=LAM),
            MathTex(r"t \;" + sem(r"\forall \alpha.\ A") + r"\; t'", r"\iff", r"\text{for every relation } R:\ "
                    r"t_X \;" + sem(r"A") + r"_{\alpha \mapsto R} \; t'_{X'}", font_size=fs, color=YES),
        )
        for d, y in zip(defs, ys):
            d.move_to([0, y + 0.25, 0]).align_to(np.array([-3.8, 0, 0]), LEFT)
            if d.get_right()[0] > 6.85:
                d.scale_to_fit_width(6.85 + 3.8).align_to(np.array([-3.8, 0, 0]), LEFT)
        rx = label(r"$R$ any relation between types $X$ and $X'$", font_size=19, color=GREY_A).next_to(
            defs[3], DOWN, buff=0.12).align_to(defs[3], LEFT)
        thm = VGroup(
            label(r"the abstraction theorem \ (Reynolds, \ 1983):", font_size=22, color=YES),
            MathTex(r"\vdash t : T", r"\implies", r"t \;" + sem("T") + r"\; t", font_size=34, color=YES),
        ).arrange(RIGHT, buff=0.4).next_to(defs[3], UP, buff=0.45)
        thm.set_x(1.5)
        if thm.get_top()[1] > 3.1:
            thm.shift(DOWN * (thm.get_top()[1] - 3.1))
        with self.voiceover(
            "The idea behind the theorem is chapter five's ladder again, with one new rung. Read every type as a "
            "relation. <bookmark mark='a'/> Integers are related when they are equal. <bookmark mark='b'/> "
            "Functions are related when they send related arguments to related results. <bookmark mark='c'/> Lists "
            "are related when they have the same length and are related element by element. <bookmark mark='d'/> "
            "And the new rung: a polymorphic value is related to another if, for every pair of types and every "
            "relation between them, its two instances are related. <bookmark mark='e'/> The abstraction theorem: "
            "every well-typed term is related to itself, at its own type. A polymorphic function cannot inspect its "
            "argument, so it must respect every relation at once."
        ) as vo:
            self.play(FadeIn(head), Create(rails))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [Create(rungs[k]), FadeIn(tnames[k]), FadeIn(defs[k])]
                if k == 3:
                    anims.append(FadeIn(rx))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(thm))
            self.play(Circumscribe(thm[1], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the free theorem for r, derived
    def free_r(self):
        head = label(r"Deriving the free theorem for \ $r : \forall a.\ [a] \to [a]$", font_size=36).to_edge(
            UP, buff=0.3)
        fs = 36
        rows = VGroup(
            MathTex(r"r", r"\;" + sem(r"\forall a.\ [a] \to [a]") + r"\;", r"r", font_size=fs),
            MathTex(r"r_A", r"\;" + sem(r"[R] \to [R]") + r"\;", r"r_B", font_size=fs),
            MathTex(r"xs \mathrel{[R]} ys", r"\implies", r"r\,xs \mathrel{[R]} r\,ys", font_size=fs),
            MathTex(r"\mathit{map}\,f\,xs = ys", r"\implies", r"\mathit{map}\,f\,(r\,xs) = r\,ys", font_size=fs),
            MathTex(r"\mathit{map}\,f\,(r\,xs) = r\,(\mathit{map}\,f\,xs)", font_size=fs),
            MathTex(r"\mathit{map}\,f \circ r = r \circ \mathit{map}\,f", font_size=fs + 4, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        whys = VGroup(
            label(r"the abstraction theorem", font_size=22, color=GREY_B),
            label(r"the $\forall$ rung: \ any $R$ between any $A$ and $B$", font_size=22, color=GREY_B),
            label(r"the $\to$ rung", font_size=22, color=GREY_B),
            label(r"choose $R$ to be $f$'s graph: \ $a \mathrel{R} b \iff f\,a = b$", font_size=22, color=HEAD),
            label(r"take $ys = \mathit{map}\,f\,xs$", font_size=22, color=GREY_B),
            label(r"for every $f$, \ and every $r$ of this type", font_size=22, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.6
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        if whys.get_right()[0] > 6.85:
            whys.shift(LEFT * (whys.get_right()[0] - 6.85))
        lift = label(r"for $R$ a graph, \ $xs \mathrel{[R]} ys$ \ means \ $\mathit{map}\,f\,xs = ys$", font_size=20,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now read off a theorem. <bookmark mark='a'/> Take any function r from lists of a to lists of a. By the "
            "abstraction theorem, r is related to itself at its type. <bookmark mark='b'/> By the for-all rung, "
            "for any types A and B and any relation R between them, the instances of r are related at lists of R to"
            " lists of R. <bookmark mark='c'/> By the function rung: related lists go to related lists. <bookmark "
            "mark='d'/> Now the one creative step: choose R to be the graph of a function f. Lists are related "
            "exactly when mapping f over the first gives the second. <bookmark mark='e'/> Take ys to be map f of "
            "xs. <bookmark mark='f'/> And there it is: map f after r equals r after map f, for every f, and every "
            "r of this type, without reading a line of r's code."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            derive(self, rows, whys, "bcdef", vo)
            self.play(FadeIn(lift))
            self.play(Circumscribe(rows[-1], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ checked by property tests
    def checked(self):
        fr = load("free")
        head = label(r"The square commutes", font_size=36).to_edge(UP, buff=0.3)
        xs, f = [1, 2, 3], (lambda x: x * x)
        tl, tr_ = cells(xs, DATA), cells(xs[::-1], DATA)
        bl, br = cells([f(x) for x in xs], YES), cells([f(x) for x in xs][::-1], YES)
        tl.move_to([-5.2, 1.6, 0])
        tr_.move_to([-1.9, 1.6, 0])
        bl.move_to([-5.2, -1.0, 0])
        br.move_to([-1.9, -1.0, 0])
        a_top = Arrow(tl.get_right(), tr_.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5)
        a_bot = Arrow(bl.get_right(), br.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5)
        a_l = Arrow(tl.get_bottom(), bl.get_top(), buff=0.15, color=HEAD, stroke_width=2.5)
        a_r = Arrow(tr_.get_bottom(), br.get_top(), buff=0.15, color=HEAD, stroke_width=2.5)
        l_top = label(r"$r$ = reverse", font_size=20, color=GREY_B).next_to(a_top, UP, buff=0.1)
        l_bot = label(r"$r$", font_size=20, color=GREY_B).next_to(a_bot, DOWN, buff=0.1)
        l_l = MathTex(r"\mathit{map}\,f", font_size=24, color=HEAD).next_to(a_l, LEFT, buff=0.1)
        l_r = MathTex(r"\mathit{map}\,f", font_size=24, color=HEAD).next_to(a_r, RIGHT, buff=0.1)
        fl = MathTex(r"f(x) = x^2", font_size=26, color=HEAD).next_to(VGroup(bl, br), DOWN, buff=0.55)
        ill = note(r"illustrative square", font_size=16).next_to(fl, DOWN, buff=0.15)
        sq = VGroup(tl, tr_, bl, br, a_top, a_bot, a_l, a_r, l_top, l_bot, l_l, l_r)
        if sq.get_left()[0] < -6.7:
            VGroup(sq, fl, ill).shift(RIGHT * (-6.7 - sq.get_left()[0]))
        names = list(fr["rearrangements"])
        bw = 2.4
        bars = VGroup()
        for n in names:
            v = fr["rearrangements"][n]
            nm = label(rf"\textsf{{{n}}}", font_size=21, color=WHITE)
            frame = Rectangle(width=bw, height=0.34, stroke_color=GREY_D, stroke_width=1.2)
            fill = Rectangle(width=max(0.02, bw * v), height=0.34, stroke_width=0, fill_color=YES,
                             fill_opacity=0.85).align_to(frame, LEFT)
            val = label(pct(v), font_size=20, color=YES)
            bars.add(VGroup(nm, VGroup(frame, fill), val))
        for b in bars:
            b[0].move_to([1.6, 0, 0])
            b[1].move_to([3.6 + bw / 2 - 0.9, 0, 0])
            b[2].next_to(b[1], RIGHT, buff=0.2)
        bars.arrange(DOWN, buff=0.3)
        for b in bars:
            b[0].align_to(np.array([0.6, 0, 0]), LEFT)
            b[1].align_to(np.array([2.6, 0, 0]), LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        bh = label(r"$\mathit{map}\,f \circ r = r \circ \mathit{map}\,f$ \ held on", font_size=22, color=WHITE)
        btab = VGroup(bh, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.0, 0])
        if btab.get_right()[0] > 6.85:
            btab.shift(LEFT * (btab.get_right()[0] - 6.85))
        bnote = wrapped_label(r"random lists, \ random $f(x) = ax^2 + b$: \ neither monotone nor one-to-one. \ "
                              r"The theorem asks nothing of $f$ \ (Part 14 used only linear $f$)", 6.0, font_size=19,
                              color=GREY_A).next_to(btab, DOWN, buff=0.35).align_to(btab, LEFT)
        with self.voiceover(
            "Draw the theorem as a square. <bookmark mark='a'/> Start with a list, reverse it, then square every "
            "element; or square first and reverse after. <bookmark mark='b'/> Both paths meet. <bookmark mark='c'/> "
            "Our property test tries four rearrangements, reverse, take three, every other element and rotate, on "
            "random lists, with random quadratic functions f. <bookmark mark='d'/> The law held every time. In Part "
            "fourteen we tested linear functions only; the derivation shows why that was never needed. The theorem "
            "asks nothing of f at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(fl), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowArrow(a_top), FadeIn(l_top), FadeIn(tr_))
            self.play(GrowArrow(a_l), FadeIn(l_l), FadeIn(bl))
            vo.wait_until("b")
            self.play(GrowArrow(a_r), FadeIn(l_r), GrowArrow(a_bot), FadeIn(l_bot), FadeIn(br))
            self.play(Indicate(br, color=YES))
            vo.wait_until("c")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(VGroup(b[0], b[1][0])) for b in bars], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(*[GrowFromEdge(b[1][1], LEFT) for b in bars], *[FadeIn(b[2]) for b in bars], run_time=1.5)
            self.play(FadeIn(bnote))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ sort
    def sort(self):
        fr = load("free")
        ce = fr["sort_counterexample"]
        head = label(r"The free theorem for \ \textsf{sort}", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        rows = VGroup(
            MathTex(r"\mathit{sort} : \forall a.\ (a \to a \to \mathsf{Bool}) \to [a] \to [a]", font_size=fs),
            MathTex(r"c \;" + sem(r"R \to R \to \mathsf{Bool}") + r"\; c'", r"\implies",
                    r"\mathit{sort}\,c \;" + sem(r"[R] \to [R]") + r"\; \mathit{sort}\,c'", font_size=fs),
            MathTex(r"c\,x\,y = c'\,(f\,x)\,(f\,y)", r"\implies",
                    r"\mathit{map}\,f\,(\mathit{sort}\,c\,xs) = \mathit{sort}\,c'\,(\mathit{map}\,f\,xs)",
                    font_size=fs),
            MathTex(r"x \le y \iff f\,x \le f\,y", r"\implies",
                    r"\mathit{map}\,f \circ \mathit{sort} = \mathit{sort} \circ \mathit{map}\,f", font_size=fs,
                    color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        whys = VGroup(
            label(r"the type", font_size=19, color=GREY_B),
            label(r"the $\forall$ and $\to$ rungs", font_size=19, color=GREY_B),
            label(r"$R$ = $f$'s graph", font_size=19, color=HEAD),
            label(r"$c = c' = {\le}$", font_size=19, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.4
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        if whys.get_right()[0] > 6.85:
            VGroup(rows, whys).scale_to_fit_width(13.4).to_edge(LEFT, buff=0.4)
        srt = sorted(ce["xs"])
        bad = {i for i, (a, b) in enumerate(zip(ce["sort_then_map"], ce["map_then_sort"])) if a != b}
        lists = VGroup(
            VGroup(MathTex(r"xs", font_size=26, color=DATA), cells(ce["xs"], DATA)),
            VGroup(MathTex(r"\mathit{sort}\,xs", font_size=26, color=DATA), cells(srt, DATA)),
            VGroup(MathTex(r"\mathit{map}\,g\,(\mathit{sort}\,xs)", font_size=26, color=WHITE),
                   cells(ce["sort_then_map"], WHITE, bad=bad)),
            VGroup(MathTex(r"\mathit{sort}\,(\mathit{map}\,g\,xs)", font_size=26, color=WHITE),
                   cells(ce["map_then_sort"], WHITE, bad=bad)),
        )
        for L in lists:
            L[1].move_to([-0.4, 0, 0]).align_to(np.array([-2.4, 0, 0]), LEFT)
            L[0].next_to(L[1], LEFT, buff=0.3)
        lists.arrange(DOWN, buff=0.18, aligned_edge=RIGHT)
        lists.next_to(rows, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        a, b = ce["xs"][1], ce["xs"][0]
        gl = MathTex(rf"g(x) = x^2:\ \ {a} < {b}\ \text{{ but }}\ g({a}) = {a * a} > {b * b} = g({b})",
                     font_size=24, color=NO)
        okl = label(rf"$f(x) = 2x + 1$ \ (order-preserving): \ held on {pct(fr['sort_monotone'])} of random lists",
                    font_size=20, color=YES)
        side = VGroup(gl, okl).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(lists, DOWN, buff=0.3).align_to(
            lists, LEFT)
        if side.get_bottom()[1] < -3.75:
            VGroup(lists, side).shift(UP * (-3.75 - side.get_bottom()[1]))
        with self.voiceover(
            "Wadler's paper of nineteen eighty-nine turned this into a method: write down a type, and read off its "
            "theorem. Take sort, which is given a comparison. <bookmark mark='a'/> Its type says that related "
            "comparisons give related sorts. <bookmark mark='b'/> With R the graph of f, the comparisons are related "
            "when comparing x and y gives the same answer as comparing f of x and f of y. <bookmark mark='c'/> So "
            "for an f that preserves and reflects the order, mapping and sorting commute. <bookmark mark='d'/> The "
            "condition matters. Our test found this list for squaring, which is not monotone: minus fifteen is "
            "below minus six, but its square is larger. <bookmark mark='e'/> Sort, then square, and the list is "
            "out of order; square, then sort, and it is sorted. For two x plus one, the law held on every list."
        ) as vo:
            self.play(FadeIn(head))
            derive(self, rows, whys, "abc", vo)
            vo.wait_until("d")
            self.play(FadeIn(lists[0]), FadeIn(lists[1]))
            self.play(FadeIn(gl))
            vo.wait_until("e")
            self.play(FadeIn(lists[2]))
            self.play(FadeIn(lists[3]))
            self.play(FadeIn(okl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ where it bends, and where it pays
    def limits(self):
        head = label(r"Where the theorem bends, \ and where it pays", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(*[mono(s, size=21, color=c) for s, c in (
            ("static <T> T id(T x) {", WHITE),
            ("  if (x instanceof String)", NO),
            ("    return (T) \"surprise\";", NO),
            ("  return x;", WHITE),
            ("}", WHITE))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        box = SurroundingRectangle(code, buff=0.25, corner_radius=0.1, color=GREY_D, stroke_width=1.5)
        cg = VGroup(box, code)
        ct = label(r"Java: \ the type says $\forall T.\ T \to T$", font_size=20, color=GREY_A).next_to(cg, UP,
                                                                                                      buff=0.15)
        cn = wrapped_label(r"a runtime type test looks inside the type variable: \ the free theorem \ "
                           r"(\textit{id} is the identity) \ fails", 5.6, font_size=21, color=NO).next_to(cg, DOWN,
                                                                                                         buff=0.2)
        left = VGroup(ct, cg, cn).move_to([-3.6, 0.5, 0])
        if left.get_left()[0] < -6.8:
            left.shift(RIGHT * (-6.8 - left.get_left()[0]))
        ill = note(r"illustrative code", font_size=16).next_to(cn, DOWN, buff=0.12).align_to(cn, LEFT)
        bends = VGroup(
            label(r"bends", font_size=26, color=NO),
            wrapped_label(r"general recursion: \ every type contains $\bot$, \ so the theorems need $f$ strict \ "
                          r"(Wadler, \ 1989)", 5.8, font_size=21, color=WHITE),
            wrapped_label(r"\texttt{seq} in Haskell, \ type tests, \ reflection", 5.8, font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        pays = VGroup(
            label(r"pays", font_size=26, color=YES),
            wrapped_label(r"fusion in GHC: \ \textit{foldr/build}, \ justified by parametricity \ (Gill, "
                          r"\ Launchbury and Peyton Jones, \ 1993)", 5.8, font_size=21, color=WHITE),
            wrapped_label(r"representation independence: \ swap a module's hidden implementation safely", 5.6,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        right = VGroup(bends, pays).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.7, 0.2, 0])
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        with self.voiceover(
            "Free theorems hold only while the language keeps its side of the bargain. <bookmark mark='a'/> This "
            "Java method has the type of the identity, but it tests the type of its argument at run time and "
            "returns something else for strings. The free theorem says it must be the identity, and it is not. "
            "<bookmark mark='b'/> General recursion bends the theorems too: every type now contains bottom, and "
            "Wadler showed they then need f to be strict. Haskell's seq, which can tell bottom from a function, "
            "bends them further. <bookmark mark='c'/> Where the bargain holds, it pays. GHC fuses list pipelines "
            "with a rewrite rule, foldr of build, whose correctness is a free theorem, and modules can swap their "
            "hidden representations safely, as Reynolds' counters did."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ct), FadeIn(cg), FadeIn(ill))
            self.play(FadeIn(cn))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in bends], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in pays], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()


_ = (LAM,)
