from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono


def cell(text: str, color=GREY_B, w=0.62, h=0.5, size=20):
    """One heap word: a box with its contents in monospace."""
    box = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.8, fill_color=BG, fill_opacity=1)
    t = mono(text, size=size, color=WHITE).move_to(box)
    return VGroup(box, t)


def var_box(name: str, color=DATA):
    """A program variable: its name beside a small box that holds a pointer."""
    box = RoundedRectangle(width=0.5, height=0.42, corner_radius=0.06, stroke_color=color, stroke_width=1.8,
                           fill_color=BG, fill_opacity=1)
    t = mono(name, size=20, color=color).next_to(box, LEFT, buff=0.12)
    return VGroup(box, t)


def ptr(a, b, color=GREY_A, angle=0.0):
    """A pointer from point a to point b (straight, or curved by ``angle``)."""
    if angle:
        return CurvedArrow(a, b, angle=angle, color=color, stroke_width=2.2, tip_length=0.14)
    return Arrow(a, b, buff=0.02, color=color, stroke_width=2.2, max_tip_length_to_length_ratio=0.18,
                 max_stroke_width_to_length_ratio=10)


def node(val: str, color=DATA):
    """A list node of two words: its value and its next pointer."""
    v = cell(val, color=color)
    n = cell("", color=color)
    g = VGroup(v, n).arrange(RIGHT, buff=0)
    g.val, g.nxt = v, n
    return g


def tag(name: str, color, target, depth: float, dx: float = 0.0):
    """A variable's name below a node (or nil), with an arrow up to it; ``depth`` and ``dx`` keep i, j and k
    apart when two of them point at the same place."""
    t = mono(name, size=20, color=color)
    t.move_to(target.get_bottom() + DOWN * depth + RIGHT * dx)
    a = Arrow(t.get_top(), target.get_bottom() + RIGHT * dx, buff=0.06, color=color, stroke_width=2,
              max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=10)
    return VGroup(t, a)


class Separation(VoiceoverScene):
    def construct(self):
        self.card()
        self.aliasing()
        self.assertions()
        self.frame()
        self.reversal()
        self.proof()
        self.infer()

    def card(self):
        card = chapter_card(5, r"Separation logic", r"How do we reason about pointers?", lit=(2002, 2015),
                            extra=((2002, r"Reynolds: \ separation logic"),
                                   (2015, r"Facebook's Infer, \ open source")), part=PART)
        with self.voiceover("Chapter five. Separation logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def aliasing(self):
        head = label(r"Pointers break the assignment axiom", font_size=36).to_edge(UP, buff=0.3)
        triple = MathTex(r"\{\, y.f = 2 \,\}", r"\quad x.f := 3 \quad", r"\{\, y.f = 2 \,\}", font_size=40)
        triple[0].set_color(DATA)
        triple[2].set_color(YES)
        triple.next_to(head, DOWN, buff=0.35)
        tl = label(r"the axiom says yes: \ the postcondition never mentions $x.f$", font_size=19,
                   color=GREY_A).next_to(triple, DOWN, buff=0.15)

        def panel(aliased: bool):
            x, y = var_box("x"), var_box("y", LAM)
            VGroup(x, y).arrange(DOWN, buff=0.55, aligned_edge=RIGHT)
            a, b = cell("1"), cell("2")
            VGroup(a, b).arrange(DOWN, buff=0.55).next_to(VGroup(x, y), RIGHT, buff=1.4)
            px = ptr(x[0].get_center(), a.get_left(), DATA)
            py = ptr(y[0].get_center(), (a.get_left() + DOWN * 0.12) if aliased else b.get_left(), LAM)
            dots = VGroup(Dot(x[0].get_center(), radius=0.05, color=DATA), Dot(y[0].get_center(), radius=0.05,
                                                                              color=LAM))
            cap = label(r"$x$ and $y$ apart" if not aliased else r"$x$ and $y$ aliased: \ the same cell",
                        font_size=19, color=GREY_B)
            g = VGroup(x, y, a, b, px, py, dots)
            cap.next_to(g, UP, buff=0.2)
            out = VGroup(cap, g)
            out.a, out.b = a, b
            return out
        p1, p2 = panel(False), panel(True)
        VGroup(p1, p2).arrange(RIGHT, buff=2.2).next_to(tl, DOWN, buff=0.35)
        r1 = label(r"$y.f = 2$: \ holds", font_size=20, color=YES).next_to(p1, DOWN, buff=0.15)
        r2 = label(r"$y.f = 3$: \ the triple is false", font_size=20, color=NO).next_to(p2, DOWN, buff=0.15)
        rows = VGroup(
            MathTex(r"\mathit{wp}", r"=", r"h[x \mapsto 3]\,[y] = 2", font_size=32),
            MathTex(r"\mathit{wp}", r"=", r"(\mathbf{if}\ y = x\ \mathbf{then}\ 3\ \mathbf{else}\ h[y]) = 2",
                    font_size=32),
            MathTex(r"\mathit{wp}", r"=", r"x \ne y \,\wedge\, h[y] = 2", font_size=32, color=DATA),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.35).set_x(-2.2)
        whys = VGroup(label(r"the heap as one big array $h$", font_size=18, color=GREY_A),
                      label(r"look up an updated array", font_size=18, color=GREY_A),
                      label(r"a case split on aliasing", font_size=18, color=DATA))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        for w in whys:
            w.align_to(whys[0], LEFT)
        whys.shift(RIGHT * (2.6 - whys.get_left()[0]))
        with self.voiceover(
            "Hoare's logic treats each variable as its own box, and pointers break that. <bookmark mark='a'/> Suppose"
            " y's field holds two, and we store three through x. The assignment axiom says y's field still holds two,"
            " since the postcondition never mentions x. <bookmark mark='b'/> If x and y point to different cells, "
            "that is right. <bookmark mark='c'/> If they point to the same cell, it is false. <bookmark mark='d'/> "
            "The classical repair treats the heap as one big array, and every read must then ask whether two pointers"
            " are equal. <bookmark mark='e'/> With n pointers, that is about n squared over two cases."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(triple), FadeIn(tl))
            self.play(FadeIn(p1), FadeIn(p2))
            vo.wait_until("b")
            n1 = cell("3").move_to(p1.a)
            self.play(Transform(p1.a, n1), FadeIn(r1))
            vo.wait_until("c")
            n2 = cell("3").move_to(p2.a)
            self.play(Transform(p2.a, n2), FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def assertions(self):
        head = label(r"Assertions that own memory", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            VGroup(MathTex(r"\mathsf{emp}", font_size=40, color=GREY_A),
                   label(r"the empty heap", font_size=18, color=GREY_B)),
            VGroup(MathTex(r"x \mapsto v", font_size=40, color=DATA),
                   label(r"exactly one cell, \ at $x$, \ holding $v$", font_size=18, color=GREY_B)),
            VGroup(MathTex(r"P \ast Q", font_size=40, color=HEAD),
                   label(r"the heap splits in two disjoint parts: \ $P$ of one, \ $Q$ of the other", font_size=18,
                         color=GREY_B)),
        )
        for d in defs:
            d.arrange(DOWN, buff=0.15)
        defs.arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.35)
        strip = VGroup(*[cell(s) for s in ("7", "3", "5", "0", "3", "9")]).arrange(RIGHT, buff=0).move_to(
            [-3.2, 0.55, 0])
        bp = Brace(VGroup(*strip[:3]), DOWN, color=DATA)
        bq = Brace(VGroup(*strip[3:]), DOWN, color=LAM)
        lp = MathTex(r"P", font_size=30, color=DATA).next_to(bp, DOWN, buff=0.08)
        lq = MathTex(r"Q", font_size=30, color=LAM).next_to(bq, DOWN, buff=0.08)
        tint_p = SurroundingRectangle(VGroup(*strip[:3]), buff=0.04, color=DATA, fill_color=DATA, fill_opacity=0.15,
                                      stroke_width=0)
        tint_q = SurroundingRectangle(VGroup(*strip[3:]), buff=0.04, color=LAM, fill_color=LAM, fill_opacity=0.15,
                                      stroke_width=0)
        ill = note(r"illustrative", font_size=16).next_to(strip, UP, buff=0.12).align_to(strip, LEFT)
        con = VGroup(
            MathTex(r"x \mapsto 3", r"\ast", r"y \mapsto 3", r"\;\Rightarrow\;", r"x \ne y", font_size=34),
            MathTex(r"x \mapsto 3", r"\wedge", r"y \mapsto 3", r"\;\Rightarrow\;", r"x = y", font_size=34),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.6, 0.45, 0])
        con[0][1].set_color(HEAD)
        con[0][4].set_color(YES)
        con[1][4].set_color(LAM)
        conl = label(r"two cells, \ so two addresses; \ but one cell cannot be two", font_size=18,
                     color=GREY_A).next_to(con, DOWN, buff=0.2)
        ldef = VGroup(
            MathTex(r"\mathit{list}(\epsilon, i)", r"\iff", r"\mathsf{emp} \wedge i = \mathit{nil}", font_size=32),
            MathTex(r"\mathit{list}(a{\cdot}\alpha, i)", r"\iff", r"\exists k.\ i \mapsto a, k", r"\;\ast\;",
                    r"\mathit{list}(\alpha, k)", font_size=32),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-2.9, -1.75, 0])
        for r in ldef:
            r.shift(RIGHT * (ldef[0][1].get_x() - r[1].get_x()))
        ldef[1][2].set_color(DATA)
        ldef[1][4].set_color(YES)
        nodes = VGroup(*[node(v) for v in ("a", "b", "c")]).arrange(RIGHT, buff=0.45).move_to([3.2, -1.75, 0])
        nil = mono("nil", size=18, color=GREY_B).next_to(nodes, RIGHT, buff=0.45)
        links = VGroup(*[ptr(nodes[q].nxt.get_center(), nodes[q + 1].get_left(), GREY_A) for q in range(2)],
                       ptr(nodes[2].nxt.get_center(), nil.get_left(), GREY_A))
        own = VGroup(*[SurroundingRectangle(nd, buff=0.07, color=c, stroke_width=1.6)
                       for nd, c in zip(nodes, (DATA, YES, YES))])
        own_l = label(r"the first node, \ $\ast$ \ the rest of the list", font_size=18, color=GREY_A).next_to(
            nodes, DOWN, buff=0.3)
        with self.voiceover(
            "Around two thousand and one, John Reynolds, Peter O'Hearn and Hongseok Yang made each assertion describe"
            " a piece of the heap. <bookmark mark='a'/> Emp holds of the empty heap; x points to v holds of exactly "
            "one cell. <bookmark mark='b'/> The separating conjunction, P star Q, says the heap splits into two "
            "disjoint parts, P holding of one and Q of the other. <bookmark mark='c'/> Two cells joined by the star "
            "are at different addresses; joined by an ordinary and, they must be the same cell. <bookmark mark='d'/> "
            "A list is either empty, or a first node separately joined to the rest of the list."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]), FadeIn(strip), FadeIn(ill))
            self.play(FadeIn(tint_p), FadeIn(tint_q), GrowFromCenter(bp), GrowFromCenter(bq), FadeIn(lp),
                      FadeIn(lq))
            vo.wait_until("c")
            self.play(FadeIn(con[0]))
            self.play(FadeIn(con[1]), FadeIn(conl))
            vo.wait_until("d")
            self.play(FadeIn(ldef), FadeIn(nodes), FadeIn(nil), Create(links))
            self.play(LaggedStart(*[Create(o) for o in own], lag_ratio=0.3), FadeIn(own_l))
        self.wait(0.4)
        self.clear_scene()

    def frame(self):
        head = label(r"Small axioms, \ and the frame rule", font_size=36).to_edge(UP, buff=0.3)
        ax = VGroup(
            MathTex(r"\{x \mapsto -\}\ \ [x] := v\ \ \{x \mapsto v\}", font_size=30),
            MathTex(r"\{x \mapsto v\}\ \ y := [x]\ \ \{x \mapsto v \wedge y = v\}", font_size=30),
            MathTex(r"\{\mathsf{emp}\}\ \ x := \mathbf{new}(v)\ \ \{x \mapsto v\}", font_size=30),
            MathTex(r"\{x \mapsto -\}\ \ \mathbf{free}(x)\ \ \{\mathsf{emp}\}", font_size=30),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.4, 1.35, 0])
        axl = label(r"$[x]$: \ the cell at address $x$; \ each axiom names only the cell it touches", font_size=18,
                    color=GREY_A).next_to(ax, DOWN, buff=0.2).align_to(ax, LEFT)
        rule = MathTex(r"\dfrac{\{P\}\ c\ \{Q\}}{\{P \ast R\}\ c\ \{Q \ast R\}}", font_size=40, color=HEAD).move_to(
            [3.6, 1.6, 0])
        side = label(r"$c$ changes no variable free in $R$", font_size=18, color=GREY_A).next_to(rule, DOWN,
                                                                                               buff=0.2)
        heap = VGroup(*[cell(v, w=0.8, h=0.62, size=24) for v in "1284"]).arrange(RIGHT, buff=0).move_to(
            [4.1, -0.25, 0])
        xs = mono("x", size=18, color=DATA).next_to(heap[0], UP, buff=0.12)
        ys = mono("y", size=18, color=LAM).next_to(heap[1], UP, buff=0.12)
        foot = SurroundingRectangle(heap[0], buff=0.05, color=HEAD, stroke_width=3)
        fr = SurroundingRectangle(VGroup(*heap[1:]), buff=0.05, color=GREY_C, fill_color=GREY_C, fill_opacity=0.25,
                                  stroke_width=1.5)
        fl = label(r"footprint", font_size=18, color=HEAD).next_to(foot, LEFT, buff=0.15)
        frl = label(r"frame $R$: \ untouched", font_size=18, color=GREY_B).next_to(fr, DOWN, buff=0.15)
        rows = VGroup(
            MathTex(r"\{x \mapsto 1\}", r"\ \ [x] := 3\ \ ", r"\{x \mapsto 3\}", font_size=34),
            MathTex(r"\{x \mapsto 1", r"\ast y \mapsto 2", r"\}", r"\ \ [x] := 3\ \ ", r"\{x \mapsto 3", r"\ast y \mapsto 2",
                    r"\}", font_size=34),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.0, -2.0, 0])
        rows[1][1].set_color(GREY_B)
        rows[1][5].set_color(GREY_B)
        whys = VGroup(label(r"the small axiom", font_size=18, color=GREY_A),
                      label(r"framed by $y \mapsto 2$: \ no case for $x = y$", font_size=18, color=YES))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        whys.align_to(whys[1], LEFT)
        whys[0].align_to(whys[1], LEFT)
        with self.voiceover(
            "The heap's rules are small. <bookmark mark='a'/> A store into the cell at x needs exactly that cell; "
            "reading, allocating and freeing are just as local. <bookmark mark='b'/> Everything else comes back "
            "through the frame rule: if c takes P to Q, it takes P star R to Q star R, provided c changes none of R's"
            " variables. <bookmark mark='c'/> What c touches is its footprint; the rest is the frame. <bookmark "
            "mark='d'/> Our store: the small axiom gives x points to three. <bookmark mark='e'/> Frame on y points to"
            " two. The star already excludes aliasing, so there is no case split. O'Hearn calls this local reasoning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.1) for a in ax], lag_ratio=0.3), FadeIn(axl),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Write(rule), FadeIn(side))
            vo.wait_until("c")
            self.play(FadeIn(heap), FadeIn(xs), FadeIn(ys))
            self.play(Create(foot), FadeIn(fl))
            self.play(FadeIn(fr), FadeIn(frl))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(Transform(heap[0], cell("3").move_to(heap[0])), Indicate(fr, color=GREY_A, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def reversal(self):
        head = label(r"Reversing a list in place", font_size=36).to_edge(UP, buff=0.3)
        lines = ["j = nil", "while i != nil:", "    k = i.next", "    i.next = j", "    j = i", "    i = k"]
        code = code_block(lines, size=22).move_to([-4.6, 0.6, 0])
        vals = ("a", "b", "c")
        nodes = VGroup(*[node(v) for v in vals]).arrange(RIGHT, buff=0.9).move_to([1.8, 0.9, 0])
        nil_l = mono("nil", size=18, color=GREY_B).next_to(nodes, LEFT, buff=0.7)
        nil_r = mono("nil", size=18, color=GREY_B).next_to(nodes, RIGHT, buff=0.7)
        targets = [nil_l, *nodes, nil_r]                   # index 0 is the left nil, 1..3 the nodes, 4 the right nil

        def fwd(q):                                        # node q's next pointer, pointing right
            dst = nodes[q + 1].get_left() if q < 2 else nil_r.get_left()
            return ptr(nodes[q].nxt.get_center(), dst, DATA)

        def back(q):                                       # node q's next pointer, reversed, over the top
            a = nodes[q].nxt.get_top()
            b = (nodes[q - 1].val.get_top() if q > 0 else nil_l.get_top()) + UP * 0.05
            return ptr(a, b, YES, angle=0.9)
        links = [fwd(q) for q in range(3)]
        depth = {"i": 0.55, "j": 1.15, "k": 0.85}
        dx = {"i": -0.2, "j": 0.0, "k": 0.2}
        cols = {"i": DATA, "j": YES, "k": HEAD}

        def put(name, idx):
            return tag(name, cols[name], targets[idx], depth[name], dx[name])
        ti, tj = put("i", 1), put("j", 0)
        tk = None
        marker = SurroundingRectangle(code[0], color=HEAD, buff=0.06, stroke_width=2)
        ill = note(r"illustrative values", font_size=16).next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
        notes = VGroup(
            wrapped_label(r"each pass moves one node from $i$'s list \ (blue) \ to the front of $j$'s \ (green), \ "
                          r"by turning one pointer round", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"no cell is allocated or freed: \ the proof must show that the two lists never share a "
                          r"cell, \ and never lose one", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Reynolds' showcase was reversing a linked list in place. <bookmark mark='a'/> The variable i walks down "
            "the old list, j collects the reversed part, and k remembers the way on. <bookmark mark='b'/> Each pass "
            "saves i's successor, turns i's next pointer round to j, and moves both one node on. <bookmark mark='c'/>"
            " One node at a time leaves i's list for the front of j's, until i is nil. <bookmark mark='d'/> Nothing "
            "is allocated or freed. Correctness means the two lists never share a cell and never lose one, which is "
            "exactly what the star can say."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(nodes), FadeIn(nil_l), FadeIn(nil_r), *[Create(lk) for lk in links], FadeIn(ill))
            self.play(Create(marker), FadeIn(tj), FadeIn(ti))
            vo.wait_until("b")
            for q in range(3):
                self.play(marker.animate.move_to(code[2]), run_time=0.3)
                nk = put("k", q + 2)
                if tk is None:
                    self.play(FadeIn(nk), run_time=0.5)
                    tk = nk
                else:
                    self.play(Transform(tk, nk), run_time=0.5)
                self.play(marker.animate.move_to(code[3]), run_time=0.3)
                nb = back(q)
                self.play(ReplacementTransform(links[q], nb), *[c[0].animate.set_stroke(color=YES) for c in nodes[q]],
                          run_time=0.7)
                links[q] = nb
                self.play(marker.animate.move_to(code[4]), Transform(tj, put("j", q + 1)), run_time=0.5)
                self.play(marker.animate.move_to(code[5]), Transform(ti, put("i", q + 2)), run_time=0.5)
                if q == 0:
                    vo.wait_until("c")
            self.play(marker.animate.move_to(code[1]), run_time=0.3)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        head = label(r"The proof: \ two lists, \ kept apart", font_size=36).to_edge(UP, buff=0.3)
        inv = MathTex(r"I:\quad \exists \alpha, \beta.\ \ \mathit{list}(\alpha, i)", r"\ast",
                      r"\mathit{list}(\beta, j)", r"\ \wedge\ \mathit{rev}(\alpha_0) = \mathit{rev}(\alpha) \cdot \beta",
                      font_size=34).next_to(head, DOWN, buff=0.3)
        inv.set_color(YES)
        inv[1].set_color(HEAD)
        rows = VGroup(
            MathTex(r"\mathit{list}(a{\cdot}\alpha', i)", r"\ast", r"\mathit{list}(\beta, j)", font_size=30),
            MathTex(r"i \mapsto a, k", r"\ast", r"\mathit{list}(\alpha', k)", r"\ast", r"\mathit{list}(\beta, j)",
                    font_size=30),
            MathTex(r"i \mapsto a, j", r"\ast", r"\mathit{list}(\alpha', k)", r"\ast", r"\mathit{list}(\beta, j)",
                    font_size=30),
            MathTex(r"\mathit{list}(\alpha', k)", r"\ast", r"\mathit{list}(a{\cdot}\beta, i)", font_size=30),
            MathTex(r"\mathit{list}(\alpha', i)", r"\ast", r"\mathit{list}(a{\cdot}\beta, j)", font_size=30,
                    color=YES),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.0, -0.35, 0])
        rows[2][0].set_color(HEAD)
        whys = VGroup(
            wrapped_label(r"$I$ and $i \ne \mathit{nil}$: \ the list has a first node $a$", 6.1, font_size=18,
                          color=GREY_A),
            wrapped_label(r"unfold it; \ \texttt{k = i.next} reads the node", 6.1, font_size=18, color=GREY_A),
            wrapped_label(r"\texttt{i.next = j}: \ the small axiom on one cell, \ the rest framed", 6.1,
                          font_size=18, color=HEAD),
            wrapped_label(r"fold: \ $i$ now heads the list $a{\cdot}\beta$", 6.1, font_size=18, color=GREY_A),
            wrapped_label(r"\texttt{j = i; i = k}: \ $I$ again, \ since $\mathit{rev}(a{\cdot}\alpha') \cdot "
                          r"\beta = \mathit{rev}(\alpha') \cdot a{\cdot}\beta$", 6.1, font_size=18, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        for w in whys:
            w.set_x(0.6, direction=LEFT)
        exit_ = MathTex(r"I \wedge i = \mathit{nil}", r"\;\Rightarrow\;", r"\alpha = \epsilon", r"\;\Rightarrow\;",
                        r"\mathit{list}(\mathit{rev}(\alpha_0), j)", font_size=32, color=DATA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One invariant does it. <bookmark mark='a'/> Two lists, alpha from i and beta from j, kept apart by the "
            "star; and the original list reversed equals alpha reversed followed by beta. <bookmark mark='b'/> Enter "
            "the body with i not nil: i's list has a first node, a. <bookmark mark='c'/> Unfold it; reading i dot "
            "next names the rest k. <bookmark mark='d'/> The store into i dot next touches one cell. The small axiom "
            "handles it, and the frame rule carries both other lists through. <bookmark mark='e'/> Fold: i now heads "
            "the list a followed by beta. <bookmark mark='f'/> Renaming restores the invariant. <bookmark mark='g'/> "
            "At the exit alpha is empty, and j holds the list reversed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(inv))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("cdef"):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k].copy(), rows[k + 1]), FadeIn(whys[k + 1]))
            vo.wait_until("g")
            self.play(FadeIn(exit_, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def infer(self):
        head = label(r"Separation logic at scale", font_size=36).to_edge(UP, buff=0.3)
        names = {"main": (0.0, 1.9), "parse": (-2.2, 0.75), "render": (2.2, 0.75), "push": (-3.4, -0.4),
                 "new_node": (-2.2, -1.55), "draw": (1.2, -0.4), "free_tree": (3.4, -0.4)}
        calls = [("main", "parse"), ("main", "render"), ("parse", "new_node"), ("parse", "push"),
                 ("render", "draw"), ("render", "free_tree"), ("push", "new_node")]
        boxes = {k: tag_box_(k).move_to([x - 2.4, y, 0]) for k, (x, y) in names.items()}
        edges = VGroup(*[Arrow(boxes[a].get_bottom(), boxes[b].get_top(), buff=0.05, color=GREY_C, stroke_width=1.8,
                               max_tip_length_to_length_ratio=0.12) for a, b in calls])
        order = ["new_node", "push", "draw", "free_tree", "parse", "render", "main"]
        specs = {k: SurroundingRectangle(boxes[k], color=YES, buff=0.06, stroke_width=2.5) for k in order}
        ill = note(r"an illustrative call graph", font_size=16).next_to(VGroup(*boxes.values()), DOWN, buff=0.3)
        bi = MathTex(r"H", r"\ast", r"\,?M", r"\;\vdash\;", r"P", r"\ast", r"\,?F", font_size=40).move_to(
            [-2.4, -2.75, 0])
        bi[2].set_color(HEAD)
        bi[6].set_color(LAM)
        bil = VGroup(label(r"$?M$: \ the missing heap, \ added to the caller's precondition", font_size=17,
                           color=HEAD),
                     label(r"$?F$: \ the frame, \ left untouched by the call", font_size=17, color=LAM)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bi, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"\textbf{bi-abduction} \ (Calcagno, \ Distefano, \ O'Hearn and Yang, \ 2009): \ infer each "
                          r"procedure's footprint from its body, \ callees first; \ each is analysed once, \ alone",
                          4.6, font_size=19, color=WHITE),
            wrapped_label(r"Facebook bought Monoidics, \ the start-up behind it, \ in 2013; \ \textbf{Infer}, \ "
                          r"open source since 2015, \ checks code changes for null dereferences and leaks before "
                          r"they are merged", 4.6, font_size=19, color=DATA),
            wrapped_label(r"concurrent separation logic \ (O'Hearn; \ Brookes): \ the 2016 G\"odel Prize; \ its "
                          r"descendant Iris is the logic of RustBelt's proofs about Rust \ (Part 55)", 4.6, font_size=19,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, -0.2, 0])
        with self.voiceover(
            "The frame rule also makes proofs compositional. <bookmark mark='a'/> A procedure's specification "
            "mentions only its footprint, so it is proved once, alone, and reused anywhere. <bookmark mark='b'/> In "
            "2009 Calcagno, Distefano, O'Hearn and Yang inferred such specifications by bi-abduction: at each call, "
            "find the heap the caller is missing, and the frame the call leaves alone. <bookmark mark='c'/> Facebook "
            "bought Monoidics, the start-up behind it, in 2013. Its analyser, Infer, open source since 2015, checks "
            "code changes for null dereferences and leaks. <bookmark mark='d'/> Concurrent separation logic won "
            "O'Hearn and Stephen Brookes the 2016 Gödel Prize, and its descendant, Iris, underlies the RustBelt "
            "proofs about Rust that Part 55 returns to."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in boxes.values()], Create(edges), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(specs["new_node"]))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            self.play(LaggedStart(*[Create(specs[k]) for k in order[1:]], lag_ratio=0.5), run_time=3)
            self.play(Write(bi), FadeIn(bil))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


def tag_box_(name: str):
    """A procedure in the call graph: its name in a rounded box."""
    t = mono(name, size=18, color=WHITE)
    box = RoundedRectangle(width=t.width + 0.35, height=0.5, corner_radius=0.08, stroke_color=GREY_B,
                           stroke_width=1.6, fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


_ = (KERN, load)
