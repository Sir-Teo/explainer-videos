from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, tag_box

BIND = r"\mathbin{>\!\!>\!\!=}"
KL = r"\mathbin{>\!\!=\!\!>}"


def sem(e: str) -> str:
    """The meaning brackets (TeX)."""
    return r"[\![\," + e + r"\,]\!]"


def fit(m, w):
    """Scale a mobject down to width w if it is wider."""
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def keep_in(m, x0=-6.85, x1=6.85):
    """Shift a mobject sideways so that it lies inside [x0, x1]."""
    if m.get_right()[0] > x1:
        m.shift(LEFT * (m.get_right()[0] - x1))
    if m.get_left()[0] < x0:
        m.shift(RIGHT * (x0 - m.get_left()[0]))
    return m


def pipe(names, gap=0.42, size=16, stub=0.3, color=GREY_A):
    """A program drawn as a pipeline: one box per stage, thick links between them, and a yellow joint (bind) on
    every link.  ``names`` are strings (monospace) or ready mobjects."""
    boxes = VGroup()
    for n in names:
        if isinstance(n, str):
            boxes.add(tag_box(n, color=color, size=size))
        else:
            r = RoundedRectangle(width=n.width + 0.35, height=max(0.5, n.height + 0.25), corner_radius=0.08,
                                 stroke_color=color, stroke_width=1.6, fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(r, n.move_to(r)))
    boxes.arrange(RIGHT, buff=gap)
    links, joints = VGroup(), VGroup()
    for a, b in zip(boxes, boxes[1:]):
        ln = Line(a.get_right(), b.get_left(), color=GREY_D, stroke_width=9)
        links.add(ln)
        joints.add(Dot(ln.get_center(), radius=0.09, color=HEAD))
    inlet = Line(boxes[0].get_left() + LEFT * stub, boxes[0].get_left(), color=GREY_D, stroke_width=9)
    outlet = Line(boxes[-1].get_right(), boxes[-1].get_right() + RIGHT * stub, color=GREY_D, stroke_width=9)
    g = VGroup(inlet, links, outlet, boxes, joints)
    g.boxes, g.joints, g.inlet, g.outlet, g.links = boxes, joints, inlet, outlet, links
    return g


class Effects(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.unit_bind()
        self.three()
        self.laws()
        self.kleisli()
        self.handlers()

    def card(self):
        card = chapter_card(8, r"Effects and monads", r"How can a mathematical meaning describe a program that does "
                            r"things?", lit=(1991, 2009),
                            extra=((1991, r"Moggi: \ notions of computation and monads"),
                                   (2009, r"Plotkin and Pretnar: \ effect handlers")), part=PART)
        with self.voiceover("Chapter eight. Effects and monads. How can a mathematical meaning describe a program "
                            "that does things?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ values are not computations
    def problem(self):
        head = label(r"A number, \ or a computation of one?", font_size=36).to_edge(UP, buff=0.3)
        naive = MathTex(sem(r"e : \mathsf{int}"), r"\in", r"\mathbb{Z}", font_size=40).next_to(head, DOWN,
                                                                                               buff=0.4)
        moggi = MathTex(sem(r"e : \mathsf{int}"), r"\in", r"T\,", r"\mathbb{Z}", font_size=40).move_to(naive)
        moggi[2].set_color(HEAD)
        cross = Cross(naive[2], stroke_color=NO, stroke_width=5, scale_factor=1.4)
        spec = [("12 / b", r"may fail, \ when $b = 0$", r"\mathbb{Z} + \{\mathsf{err}\}", r"exceptions", NO),
                ("tick(); tick(); 10 * count", r"reads and changes a counter", r"S \to \mathbb{Z} \times S",
                 r"state", KERN),
                ("12 / choose [1, 2, 3, 4]", r"has several answers", r"\mathsf{List}\,\mathbb{Z}",
                 r"nondeterminism", LAM)]
        rows, doms, news = VGroup(), [], []
        for k, (code, what, dom, name, col) in enumerate(spec):
            y = 0.95 - 1.3 * k
            c = mono(code, size=20, color=WHITE)
            c.move_to([0, y + 0.15, 0]).align_to(np.array([-6.4, 0, 0]), LEFT)
            w = label(what, font_size=19, color=GREY_B).next_to(c, DOWN, buff=0.12, aligned_edge=LEFT)
            ar = Arrow([-0.9, y, 0], [0.2, y, 0], buff=0, color=GREY_B, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.2)
            d = MathTex(dom, font_size=32, color=col).next_to(ar, RIGHT, buff=0.3)
            n = MathTex(r"T\,\mathbb{Z}", r"=", dom, font_size=32, color=col)
            n[0].set_color(HEAD)
            n.next_to(ar, RIGHT, buff=0.3)
            nm = label(name, font_size=22, color=col).move_to([0, y, 0]).align_to(np.array([4.6, 0, 0]), LEFT)
            rows.add(VGroup(c, w, ar, d, nm))
            doms.append(d)
            news.append(n)
        cap = wrapped_label(r"Moggi: \ a \textit{value} of type $A$ is not a \textit{computation} of type $A$; \ give "
                            r"computations the meaning $T\,A$, \ for a \textbf{monad} $T$ \ --- \ one $T$ per effect",
                            12.6, font_size=22, color=YES).to_edge(DOWN, buff=0.35)
        ill = note(r"illustrative programs", font_size=16).to_corner(DR, buff=0.2).shift(UP * 0.75)
        with self.voiceover(
            "Every meaning so far was pure: an integer expression denoted an integer. <bookmark mark='a'/> Real "
            "programs do more. Twelve divided by b may fail. <bookmark mark='b'/> A counter may be read and changed. "
            "<bookmark mark='c'/> A choice may give several answers. <bookmark mark='d'/> None of these denotes one "
            "number. Failure needs an extra value; state needs a function from the old counter to a result and a new "
            "one; choice needs a list. <bookmark mark='e'/> Eugenio Moggi, in nineteen eighty-nine and nineteen "
            "ninety-one, said this uniformly: tell values apart from computations, and let a computation of an "
            "integer mean an element of T of the integers, for a structure T called a monad. Each effect is a choice "
            "of T."
        ) as vo:
            self.play(FadeIn(head), Write(naive))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k][0], shift=RIGHT * 0.2), FadeIn(rows[k][1]), *([FadeIn(ill)] if k == 0
                                                                                       else []))
            vo.wait_until("d")
            self.play(Create(cross))
            for r in rows:
                self.play(GrowArrow(r[2]), FadeIn(r[3]), FadeIn(r[4]), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeOut(cross), TransformMatchingTex(naive, moggi), run_time=1.2)
            self.play(*[TransformMatchingTex(d, n) for d, n in zip(doms, news)], FadeIn(cap), run_time=1.4)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ return and bind, as plumbing
    def unit_bind(self):
        head = label(r"Return and bind: \ the plumbing", font_size=36).to_edge(UP, buff=0.3)
        fs = 34
        types = VGroup(
            MathTex(r"\mathsf{return}", r":", r"A \to T\,A", font_size=fs),
            MathTex(BIND, r":", r"T\,A \to (A \to T\,B) \to T\,B", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.4)
        types[0][0].set_color(YES)
        types[1][0].set_color(HEAD)
        tw = VGroup(label(r"a value as a computation that does nothing else", font_size=19, color=GREY_B),
                    label(r"run one computation, \ feed its value to the next", font_size=19, color=GREY_B))
        for t, r in zip(tw, types):
            t.next_to(r, RIGHT, buff=0.5)
        VGroup(types, tw).set_x(0)
        stages = [MathTex(r"f : A \to T\,B", font_size=26), MathTex(r"g : B \to T\,C", font_size=26),
                  MathTex(r"h : C \to T\,D", font_size=26)]
        p = pipe(stages, gap=1.0, stub=0.6).move_to([0, -0.35, 0])
        jl = VGroup(*[MathTex(BIND, font_size=26, color=HEAD).next_to(j, UP, buff=0.2) for j in p.joints])
        dot = Dot(p.inlet.get_start(), radius=0.11, color=DATA).set_z_index(5)
        cap = label(r"each stage takes a plain value; \ the effect lives in the joints", font_size=21,
                    color=HEAD).next_to(p, DOWN, buff=0.35)
        d0 = MathTex(r"\mathsf{do}\ \{\,", r"q", r"\leftarrow", r"12 \div b", r";\ ", r"\mathsf{return}\,(q+1)",
                     r"\,\}", font_size=32)
        d1 = MathTex(r"12 \div b", BIND, r"\lambda", r"q", r".\ ", r"\mathsf{return}\,(q+1)", font_size=32)
        d1[1].set_color(HEAD)
        der = VGroup(d0, MathTex(r"=", font_size=32), d1).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.75)
        dl = label(r"after Wadler \ (1992), \ Haskell's \textsf{do} block is bind, \ written sideways", font_size=19,
                   color=GREY_B).next_to(der, DOWN, buff=0.15)
        with self.voiceover(
            "A monad is three things. <bookmark mark='a'/> A type constructor T, and return, which turns a value "
            "into a computation that does nothing else. <bookmark mark='b'/> And bind, which runs a computation of "
            "an A and feeds its value to a function that produces a computation of a B. <bookmark mark='c'/> Think "
            "of a program as a pipeline of stages, each taking a plain value and producing a computation. <bookmark "
            "mark='d'/> Bind is the joint between stages: it unpacks what one stage produced and feeds the next, and "
            "the effect lives entirely in the joints. <bookmark mark='e'/> Philip Wadler's papers of nineteen "
            "ninety-two carried this into programming. A do block in Haskell is bind, written sideways."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(types[0]), FadeIn(tw[0]))
            vo.wait_until("b")
            self.play(Write(types[1]), FadeIn(tw[1]))
            vo.wait_until("c")
            self.play(FadeIn(p.inlet), FadeIn(p.outlet), FadeIn(p.links), FadeIn(p.boxes))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(j) for j in p.joints], lag_ratio=0.3), FadeIn(jl))
            self.add(dot)
            for j in p.joints:
                self.play(dot.animate.move_to(j), run_time=0.7)
                self.play(Flash(j, color=HEAD, flash_radius=0.3), run_time=0.4)
            self.play(dot.animate.move_to(p.outlet.get_end()), run_time=0.6)
            self.play(FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeOut(dot), Write(d0))
            self.play(FadeIn(der[1]), TransformMatchingTex(d0.copy(), d1), FadeIn(dl), run_time=1.4)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ one program, three monads
    def three(self):
        m = load("monads")
        head = label(r"Three monads, \ one shape of program", font_size=36).to_edge(UP, buff=0.3)
        xs = [-4.55, 0.0, 4.55]
        W = 4.2
        cols = [DATA, KERN, LAM]
        titles = [r"exceptions: \ \textsf{Maybe}", r"state: \ \textsf{State}", r"nondeterminism: \ \textsf{List}"]
        tdefs = [r"T\,A = A + \{\mathsf{Nothing}\}", r"T\,A = S \to A \times S", r"T\,A = [A]"]
        binds = [[r"\mathsf{Nothing}" + BIND + r"k = \mathsf{Nothing}", r"\mathsf{Just}\,a" + BIND + r"k = k\,a"],
                 [r"m" + BIND + r"k = \lambda s.\ \mathbf{let}\ (a, s') = m\,s", r"\mathbf{in}\ k\,a\,s'"],
                 [r"m" + BIND + r"k = \mathsf{concat}\,(\mathsf{map}\,k\,m)"]]
        progs = [["12 / b", "+ 1"], ["tick", "tick", "10 * count"], ["choose b", "12 / b"]]
        tops, pipes = [], []
        for x, c, t, d, bl, pr in zip(xs, cols, titles, tdefs, binds, progs):
            g = VGroup(label(t, font_size=23, color=c), MathTex(d, font_size=27, color=WHITE))
            bb = VGroup(*[MathTex(s, font_size=23, color=GREY_A) for s in bl]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
            g.add(bb)
            g.arrange(DOWN, buff=0.2)
            fit(g, W).move_to([x, 0, 0]).align_to(np.array([0, 2.75, 0]), UP)
            tops.append(g)
            p = fit(pipe(pr, color=c), W - 0.1).move_to([x, -0.45, 0])
            pipes.append(p)
        seps = VGroup(*[DashedLine([x, 2.7, 0], [x, -2.8, 0], color=GREY_D, stroke_width=1.5, dash_length=0.1)
                        for x in (-2.27, 2.27)])
        # Maybe: three inputs
        mb = m["maybe"]
        res_m = VGroup()
        for b in ("0", "3", "4"):
            v = mb[b]
            res_m.add(MathTex(rf"b = {b}:\ \ " + (r"\mathsf{Nothing}" if v is None else rf"\mathsf{{Just}}\,{v}"),
                              font_size=26, color=NO if v is None else YES))
        res_m.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(pipes[0], DOWN, buff=0.45)
        # State: the counter wire below the pipe
        ps = pipes[1]
        wire_y = ps.get_bottom()[1] - 0.3
        wire = Line([ps.get_left()[0], wire_y, 0], [ps.get_right()[0], wire_y, 0], color=KERN, stroke_width=2.5)
        marks = [ps.inlet.get_start(), *[j.get_center() for j in ps.joints], ps.outlet.get_end()]
        svals = [0, 1, 2, m["state"]["final_state"]]
        slabs = VGroup(*[MathTex(rf"s={v}" if i == 0 else str(v), font_size=22, color=KERN).move_to(
            [pt[0], wire_y - 0.25, 0]) for i, (pt, v) in enumerate(zip(marks, svals))])
        slabs[0].shift(RIGHT * 0.15)
        res_s = VGroup(MathTex(rf"({m['state']['result']},\ {m['state']['final_state']})", font_size=30, color=YES),
                       label(r"result, \ final counter", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.1)
        res_s.next_to(slabs, DOWN, buff=0.3).set_x(xs[1])
        # List: four branches
        pl = pipes[2]
        res_l = VGroup(MathTex(r"[" + r",\ ".join(str(v) for v in m["list"]) + r"]", font_size=30, color=YES),
                       label(r"$b \in \{1, 2, 3, 4\}$", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.1)
        res_l.next_to(pl, DOWN, buff=0.45).set_x(xs[2])
        foot = wrapped_label(r"the program text is the same; \ only the joint changed \ \ (values computed by our "
                             r"instrument)", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Three monads, one shape of program. <bookmark mark='a'/> For exceptions, T of A is an A or Nothing, and "
            "bind skips the rest once a stage has failed. <bookmark mark='b'/> Twelve divided by zero gives Nothing; "
            "by three, five after adding one; by four, four. <bookmark mark='c'/> For state, T of A is a function "
            "from the counter to a result and a new counter, and bind threads the counter through. <bookmark "
            "mark='d'/> Tick twice from zero, then return ten times the counter: twenty, with the counter left at "
            "two. <bookmark mark='e'/> For nondeterminism, T of A is a list, and bind runs the rest once for each "
            "possibility. <bookmark mark='f'/> Choosing b from one to four gives twelve, six, four and three. "
            "<bookmark mark='g'/> Only the joint changed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seps))
            vo.wait_until("a")
            self.play(FadeIn(tops[0]), FadeIn(pipes[0]))
            vo.wait_until("b")
            p = pipes[0]
            for k, b in enumerate(("0", "3", "4")):
                d = Dot(p.inlet.get_start(), radius=0.1, color=DATA).set_z_index(5)
                self.add(d)
                self.play(d.animate.move_to(p.joints[0]), run_time=0.5)
                if mb[b] is None:
                    self.play(d.animate.set_color(NO).move_to(res_m[k].get_left() + LEFT * 0.2), run_time=0.6)
                else:
                    self.play(d.animate.move_to(p.outlet.get_end()), run_time=0.5)
                self.play(FadeOut(d), FadeIn(res_m[k]), run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(tops[1]), FadeIn(pipes[1]), Create(wire))
            vo.wait_until("d")
            d = Dot(ps.inlet.get_start(), radius=0.1, color=DATA).set_z_index(5)
            self.add(d)
            self.play(FadeIn(slabs[0]), run_time=0.4)
            for k, pt in enumerate(marks[1:], start=1):
                self.play(d.animate.move_to(pt), run_time=0.5)
                self.play(FadeIn(slabs[k]), run_time=0.3)
            self.play(FadeOut(d), FadeIn(res_s))
            vo.wait_until("e")
            self.play(FadeIn(tops[2]), FadeIn(pipes[2]))
            vo.wait_until("f")
            d = Dot(pl.inlet.get_start(), radius=0.1, color=DATA).set_z_index(5)
            self.add(d)
            self.play(d.animate.move_to(pl.joints[0]), run_time=0.5)
            ds = VGroup(*[Dot(pl.joints[0].get_center(), radius=0.08, color=DATA).set_z_index(5) for _ in range(4)])
            self.remove(d)
            self.add(ds)
            end = pl.outlet.get_end()
            self.play(*[dd.animate.move_to(end + UP * (0.27 * (1.5 - i))) for i, dd in enumerate(ds)], run_time=0.8)
            self.play(FadeOut(ds), FadeIn(res_l))
            vo.wait_until("g")
            self.play(FadeIn(foot), *[Indicate(j, color=HEAD) for pp in pipes for j in pp.joints])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the three laws, one checked by algebra
    def laws(self):
        head = label(r"The monad laws, \ checked by algebra", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        L = VGroup(
            MathTex(r"\mathsf{return}\,a", BIND, r"k", r"=", r"k\,a", font_size=fs),
            MathTex(r"m", BIND, r"\mathsf{return}", r"=", r"m", font_size=fs),
            MathTex(r"(m", BIND, r"k)", BIND, r"h", r"=", r"m", BIND, r"(\lambda x.\ k\,x", BIND, r"h)",
                    font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        names = VGroup(*[label(t, font_size=20, color=HEAD) for t in (r"left unit", r"right unit",
                                                                      r"associativity")])
        lx = L.get_right()[0] + 0.6
        for n, r in zip(names, L):
            n.move_to([lx + n.width / 2, r.get_y(), 0])
        rule = Line([-6.4, 0, 0], [6.4, 0, 0], color=GREY_D, stroke_width=1.5).next_to(L, DOWN, buff=0.28)
        rule.set_x(0)
        sub = label(r"check the left unit for \textsf{State}:", font_size=21, color=KERN).next_to(rule, DOWN,
                                                                                                 buff=0.2)
        sub.align_to(L, LEFT)
        rows = VGroup(
            MathTex(r"\mathsf{return}\,a", BIND, r"k", font_size=fs),
            MathTex(r"=", r"\lambda s.\ ", r"\mathbf{let}\ (x, s') =", r"(\mathsf{return}\,a)\,s",
                    r"\ \mathbf{in}\ k\,x\,s'", font_size=fs),
            MathTex(r"=", r"\lambda s.\ ", r"\mathbf{let}\ (x, s') =", r"(a, s)", r"\ \mathbf{in}\ k\,x\,s'",
                    font_size=fs),
            MathTex(r"=", r"\lambda s.\ ", r"k\,a\,s", font_size=fs),
            MathTex(r"=", r"k\,a", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(sub, DOWN, buff=0.25).align_to(L, LEFT)
        for r in rows[1:]:
            r.shift(RIGHT * 0.5)
        rows[4][1].set_color(YES)
        whys = VGroup(
            label(r"the law's left side", font_size=20, color=GREY_B),
            label(r"unfold bind for state", font_size=20, color=GREY_B),
            label(r"return for state: \ $\lambda s.\ (a, s)$", font_size=20, color=GREY_B),
            label(r"match: \ $x = a$, \ $s' = s$", font_size=20, color=GREY_B),
            label(r"$\lambda s.\ f\,s = f$: \ the law holds", font_size=20, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.6
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        keep_in(whys)
        with self.voiceover(
            "A monad must obey three laws, which make sequencing behave. <bookmark mark='a'/> Left unit: returning a "
            "value and binding it is just applying the next stage. <bookmark mark='b'/> Right unit: binding to "
            "return changes nothing. <bookmark mark='c'/> Associativity: how you group a pipeline does not matter. "
            "<bookmark mark='d'/> Check the first law for state, by algebra, as in chapter two. <bookmark mark='e'/> "
            "Unfold bind: a function of the counter that runs return a, and passes its result and new counter to k. "
            "<bookmark mark='f'/> Return a, given s, is the pair a and s. <bookmark mark='g'/> So x is a, and s "
            "prime is s. <bookmark mark='h'/> And a function that applies k a to its argument is k a itself. The law "
            "holds; the other two are checked the same way."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Write(L[k]), FadeIn(names[k]))
            vo.wait_until("d")
            self.play(Create(rule), FadeIn(sub), Write(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("efgh", start=1):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=1.3)
            self.play(Circumscribe(rows[4], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Kleisli composition
    def kleisli(self):
        head = label(r"Kleisli composition: \ a category of effectful functions", font_size=36).to_edge(UP, buff=0.3)
        pts = {"A": [-6.0, 1.2, 0], "B": [-4.4, 1.2, 0], "C": [-2.8, 1.2, 0]}
        objs = {k: VGroup(Dot(p, radius=0.07, color=WHITE), MathTex(k, font_size=30).next_to(p, UP, buff=0.15))
                for k, p in pts.items()}
        fa = Arrow(pts["A"], pts["B"], buff=0.15, color=DATA, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        ga = Arrow(pts["B"], pts["C"], buff=0.15, color=LAM, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        fl = MathTex("f", font_size=26, color=DATA).next_to(fa, DOWN, buff=0.08)
        gl = MathTex("g", font_size=26, color=LAM).next_to(ga, DOWN, buff=0.08)
        comp = CurvedArrow(np.array(pts["A"]) + DOWN * 0.2, np.array(pts["C"]) + DOWN * 0.2, angle=PI / 2.4,
                           color=HEAD, stroke_width=3, tip_length=0.18)
        cl = MathTex(r"f", KL, r"g", font_size=28, color=HEAD).next_to(comp, DOWN, buff=0.1)
        tys = VGroup(MathTex(r"f : A \to T\,B", font_size=26, color=DATA),
                     MathTex(r"g : B \to T\,C", font_size=26, color=LAM)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.12)
        tys.next_to(cl, DOWN, buff=0.35).set_x(pts["B"][0])
        fs = 30
        defn = MathTex(r"(f", KL, r"g)", r"\,x", r"=", r"f\,x", BIND, r"g", font_size=fs, color=HEAD)
        a0 = MathTex(r"\mathsf{return}\,a", BIND, r"f", r"=", r"f\,a", font_size=fs)
        a1 = MathTex(r"(\mathsf{return}", KL, r"f)", r"\,a", r"=", r"f\,a", font_size=fs)
        a2 = MathTex(r"\mathsf{return}", KL, r"f", r"=", r"f", font_size=fs, color=YES)
        b2 = MathTex(r"f", KL, r"\mathsf{return}", r"=", r"f", font_size=fs, color=YES)
        c2 = MathTex(r"(f", KL, r"g)", KL, r"h", r"=", r"f", KL, r"(g", KL, r"h)", font_size=fs, color=YES)
        right = VGroup(defn, a0, a1, a2, b2, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        right.next_to(head, DOWN, buff=0.45).align_to(np.array([-1.2, 0, 0]), LEFT)
        rwhy = VGroup(label(r"definition", font_size=19, color=GREY_B),
                      label(r"the left unit law", font_size=19, color=GREY_B),
                      label(rf"rewritten with ${KL}$", font_size=19, color=GREY_B),
                      label(r"drop the $a$", font_size=19, color=YES),
                      label(r"right unit", font_size=19, color=YES),
                      label(r"associativity", font_size=19, color=YES))
        wx = max(r.get_right()[0] for r in right) + 0.5
        for w, r in zip(rwhy, right):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        keep_in(rwhy)
        cat = label(r"identity and associativity: \ the \textbf{Kleisli category} of $T$", font_size=22,
                    color=YES).next_to(right, DOWN, buff=0.3).align_to(right, LEFT)
        mog = MathTex(sem(r"\mathbf{let}\ x = e_1\ \mathbf{in}\ e_2") + r"\rho", r"=", sem("e_1") + r"\rho", BIND,
                      r"\lambda v.\ " + sem("e_2") + r"\rho[x \mapsto v]", font_size=32)
        mog[3].set_color(HEAD)
        mcap = label(r"Moggi: \ a term with a free $x : A$ and a result of type $B$ denotes a Kleisli arrow $A \to "
                     r"T\,B$", font_size=20, color=GREY_A)
        VGroup(mog, mcap).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is a tidier way to state the laws. <bookmark mark='a'/> Compose two effectful functions, f from A "
            "to computations of B and g from B to computations of C, by running f and binding its result to g. This "
            "is Kleisli composition, after Heinrich Kleisli. <bookmark mark='b'/> Take the left unit law, <bookmark "
            "mark='c'/> rewrite it with the new composition, <bookmark mark='d'/> and drop the a: return composed "
            "with f is f. <bookmark mark='e'/> Likewise f composed with return is f, and composition is associative. "
            "<bookmark mark='f'/> Effectful functions form a category, with return as its identity. <bookmark "
            "mark='g'/> And this is Moggi's semantics: a program with a free variable of type A and a result of type "
            "B denotes a Kleisli arrow, and let is bind."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(o) for o in objs.values()], GrowArrow(fa), GrowArrow(ga), FadeIn(fl), FadeIn(gl),
                      FadeIn(tys))
            self.play(Create(comp), FadeIn(cl), Write(defn), FadeIn(rwhy[0]))
            vo.wait_until("b")
            self.play(FadeIn(a0), FadeIn(rwhy[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(a0.copy(), a1), FadeIn(rwhy[2]), run_time=1.3)
            vo.wait_until("d")
            self.play(TransformMatchingTex(a1.copy(), a2), FadeIn(rwhy[3]), run_time=1.3)
            vo.wait_until("e")
            self.play(FadeIn(b2), FadeIn(rwhy[4]))
            self.play(FadeIn(c2), FadeIn(rwhy[5]))
            vo.wait_until("f")
            self.play(FadeIn(cat), Circumscribe(VGroup(a2, b2, c2), color=YES))
            vo.wait_until("g")
            self.play(Write(mog), FadeIn(mcap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ algebraic effects and handlers
    def handlers(self):
        head = label(r"Algebraic effects, \ and handlers", font_size=36).to_edge(UP, buff=0.3)
        prog = VGroup(mono("if choose () then 6", size=18, color=WHITE),
                      mono("else if choose () then 4", size=18, color=WHITE),
                      mono("else fail ()", size=18, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        prog.next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        pos = {"r": [-4.3, 1.0, 0], "l1": [-5.7, -0.55, 0], "n2": [-2.9, -0.55, 0], "l2": [-4.0, -2.1, 0],
               "l3": [-1.8, -2.1, 0]}
        txt = {"r": "choose", "l1": "return 6", "n2": "choose", "l2": "return 4", "l3": "fail"}
        colr = {"r": KERN, "n2": KERN, "l1": WHITE, "l2": WHITE, "l3": NO}
        nodes = {k: tag_box(txt[k], color=colr[k], size=17).move_to(p) for k, p in pos.items()}
        tree_e = VGroup()
        elab = VGroup()
        for a, b, t in (("r", "l1", "true"), ("r", "n2", "false"), ("n2", "l2", "true"), ("n2", "l3", "false")):
            ln = Line(nodes[a].get_bottom(), nodes[b].get_top(), color=GREY_B, stroke_width=2)
            tree_e.add(ln)
            lt = label(rf"\textsf{{{t}}}", font_size=17, color=GREY_B)
            side = LEFT if nodes[b].get_x() < nodes[a].get_x() else RIGHT
            lt.next_to(ln.get_center(), side, buff=0.12)
            elab.add(lt)
        ops = VGroup(MathTex(r"\mathsf{choose} : 1 \to \mathsf{bool}", r"\qquad", r"\mathsf{fail} : 1 \to 0",
                             font_size=28, color=KERN),
                     label(r"Plotkin and Power \ (2001): \ an effect is given by its operations", font_size=19,
                           color=GREY_B)).arrange(DOWN, buff=0.12)
        ops.move_to([3.0, 2.45, 0])

        def hbox(title, lines, col):
            t = label(title, font_size=21, color=col)
            ls = VGroup(*[MathTex(s, font_size=24, color=WHITE) for s in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.1)
            body = VGroup(t, ls).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            fit(body, 6.9)
            fr = RoundedRectangle(width=7.3, height=body.height + 0.3, corner_radius=0.12, stroke_color=col,
                                  stroke_width=1.8, fill_color=BG, fill_opacity=1)
            body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
            return VGroup(fr, body)

        h1 = hbox(r"handler 1: \ collect every result",
                  [r"\mathsf{return}\,v \mapsto [v]", r"\mathsf{choose}\,k \mapsto k\,\mathsf{true} \mathbin{+\!\!+} "
                   r"k\,\mathsf{false}", r"\mathsf{fail}\,k \mapsto [\,]"], YES)
        h2 = hbox(r"handler 2: \ backtrack",
                  [r"\mathsf{return}\,v \mapsto \mathsf{Just}\,v", r"\mathsf{choose}\,k \mapsto k\,\mathsf{true}, \ "
                   r"\text{or } k\,\mathsf{false} \text{ if that is } \mathsf{Nothing}",
                   r"\mathsf{fail}\,k \mapsto \mathsf{Nothing}"], DATA)
        hs = VGroup(h1, h2).arrange(DOWN, buff=0.25).next_to(ops, DOWN, buff=0.3)
        hs.align_to(np.array([-0.55, 0, 0]), LEFT)
        kn = label(r"$k$: \ the rest of the program, \ a continuation \ (Part 15)", font_size=18,
                   color=GREY_B).next_to(hs, DOWN, buff=0.15).align_to(hs, LEFT)

        def vals(vs, col):
            g = VGroup()
            for key, v in vs.items():
                t = MathTex(v, font_size=24, color=col)
                if key.startswith("l"):
                    t.next_to(nodes[key], DOWN, buff=0.12)
                else:
                    t.next_to(nodes[key], RIGHT, buff=0.15)
                g.add(t)
            return g

        v1 = vals({"l1": r"[6]", "l2": r"[4]", "l3": r"[\,]", "n2": r"[4]", "r": r"[6,\ 4]"}, YES)
        v2 = vals({"l1": r"\mathsf{Just}\,6", "l2": r"\mathsf{Just}\,4", "l3": r"\mathsf{Nothing}",
                   "n2": r"\mathsf{Just}\,4", "r": r"\mathsf{Just}\,6"}, DATA)
        foot = wrapped_label(r"one program, \ two meanings; \ OCaml 5, \ Koka and Eff build effects this way: \ "
                             r"exceptions, \ generators and async code can be written as handlers", 7.4, font_size=19,
                             color=WHITE).next_to(kn, DOWN, buff=0.2).align_to(hs, LEFT)
        ill = note(r"illustrative program", font_size=16).to_corner(DL, buff=0.2)
        with self.voiceover(
            "Gordon Plotkin and John Power, in two thousand and one, started from the other end: an effect is given "
            "by its operations. <bookmark mark='a'/> Here, choose, which returns a boolean, and fail, which never "
            "returns. <bookmark mark='b'/> A program using them is a tree: a node per operation, a branch per "
            "answer, values at the leaves. <bookmark mark='c'/> Matija Pretnar and Plotkin added handlers in two "
            "thousand and nine. A handler says what each operation does, given the rest of the program as a "
            "continuation, and running the program folds the tree. <bookmark mark='d'/> One handler collects every "
            "result: six and four. <bookmark mark='e'/> Another backtracks: try true, and only if that fails, try "
            "false. Same tree: six. <bookmark mark='f'/> The program never changed, only its handler. OCaml five "
            "builds its effects this way; exceptions, generators and async code can all be written as handlers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(ops))
            vo.wait_until("b")
            self.play(FadeIn(nodes["r"]))
            self.play(Create(tree_e[0]), Create(tree_e[1]), FadeIn(elab[:2]), FadeIn(nodes["l1"]),
                      FadeIn(nodes["n2"]))
            self.play(Create(tree_e[2]), Create(tree_e[3]), FadeIn(elab[2:]), FadeIn(nodes["l2"]),
                      FadeIn(nodes["l3"]))
            vo.wait_until("c")
            self.play(FadeIn(h1), FadeIn(kn))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in v1[:3]], lag_ratio=0.3))
            self.play(FadeIn(v1[3], shift=UP * 0.1))
            self.play(FadeIn(v1[4], shift=UP * 0.1))
            self.play(Circumscribe(v1[4], color=YES))
            vo.wait_until("e")
            self.play(FadeIn(h2))
            self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(v1[:3], v2[:3])], lag_ratio=0.3))
            self.play(ReplacementTransform(v1[3], v2[3]))
            self.play(ReplacementTransform(v1[4], v2[4]))
            vo.wait_until("f")
            self.play(FadeIn(foot), Circumscribe(v2[4], color=DATA))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
