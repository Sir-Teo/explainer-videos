from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def cell(text: str | None, w=0.66, h=0.46, color=YES, fs=24):
    """One entry of a partial function's table: its value, or bottom when undefined."""
    r = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.5, fill_color=BG, fill_opacity=1)
    t = MathTex(r"\bot" if text is None else text, font_size=fs, color=GREY_C if text is None else color)
    if t.width > w - 0.08:
        t.scale_to_fit_width(w - 0.08)
    t.move_to(r)
    return VGroup(r, t)


def strip(values, w=0.66, h=0.46, color=YES, fs=24):
    return VGroup(*[cell(v, w, h, color, fs) for v in values]).arrange(RIGHT, buff=0.06)


class Domains(VoiceoverScene):
    def construct(self):
        self.card()
        self.order()
        self.cpo()
        self.continuity()
        self.kleene()
        self.chain()
        self.dinf()

    def card(self):
        card = chapter_card(3, r"Domains and fixed points", r"Why does every recursive definition have a meaning?",
                            lit=(1969, 1970), extra=((1969, r"Scott: \ a model of the untyped $\lambda$-calculus"),
                                                     (1970, r"Scott: \ outline of a mathematical theory of "
                                                            r"computation")), part=PART)
        with self.voiceover("Chapter three. Domains and fixed points. Why does every recursive definition have a "
                            "meaning?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def order(self):
        head = label(r"Ordered by information: \ $x \sqsubseteq y$", font_size=36).to_edge(UP, buff=0.3)
        bot = MathTex(r"\bot", font_size=40, color=GREY_B).move_to([-3.6, -1.3, 0])
        nums = VGroup(*[MathTex(s, font_size=34, color=DATA) for s in (r"\cdots", "-1", "0", "1", "2", "3",
                                                                        r"\cdots")]).arrange(RIGHT, buff=0.5)
        nums.move_to([-3.6, 0.9, 0])
        lines = VGroup(*[Line(bot.get_top(), n.get_bottom(), buff=0.1, color=GREY_C, stroke_width=1.6)
                         for n in nums[1:-1]])
        zl = label(r"$\mathbb{Z}_\bot$: \ the integers, \ with $\bot$ below", font_size=22, color=GREY_A).next_to(
            nums, UP, buff=0.45)
        zn = wrapped_label(r"numbers side by side: \ knowing ``3'' is not more or less than knowing ``4''", 5.6,
                           font_size=20, color=GREY_A).next_to(bot, DOWN, buff=0.4)
        f = strip(["1", None, "2", None])
        g = strip(["1", "5", "2", None])
        h = strip(["1", "5", "3", None])
        names = [MathTex(s, font_size=30, color=c) for s, c in (("f", WHITE), ("g", YES), ("h", NO))]
        rows = VGroup(*[VGroup(n, s).arrange(RIGHT, buff=0.3) for n, s in zip(names, (f, g, h))]).arrange(
            DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.6, 0.3, 0])
        idx = VGroup(*[MathTex(str(i), font_size=20, color=GREY_B).next_to(c, UP, buff=0.1) for i, c in
                       enumerate(f)])
        r1 = MathTex(r"f \sqsubseteq g", font_size=30, color=YES).next_to(rows[1], RIGHT, buff=0.35)
        r2 = MathTex(r"f \not\sqsubseteq h", font_size=30, color=NO).next_to(rows[2], RIGHT, buff=0.35)
        g[1][0].set_stroke(HEAD, width=2.5)
        h[2][0].set_stroke(NO, width=2.5)
        fl = wrapped_label(r"functions, \ pointwise: \ $f \sqsubseteq g$ \ if wherever $f$ is defined, \ $g$ is "
                           r"defined and agrees", 5.8, font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.45)
        right = VGroup(rows, idx, r1, r2, fl)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.35)
        with self.voiceover(
            "To choose the least solution we need an order, and Dana Scott's insight was to order meanings by "
            "information. <bookmark mark='a'/> In the integers with bottom, the undefined result sits below every "
            "number, and the numbers sit side by side: knowing that a result is three is neither more nor less than "
            "knowing that it is four. <bookmark mark='b'/> Functions are ordered pointwise: one is below another if, "
            "wherever the first is defined, the second is defined too, and agrees. <bookmark mark='c'/> Filling in "
            "answers moves up the order. Changing an answer does not: h has more answers than f, but it is not above "
            "f."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bot), FadeIn(nums), Create(lines), FadeIn(zl))
            self.play(FadeIn(zn))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(idx), FadeIn(fl))
            self.play(FadeIn(rows[1]), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(r2), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    def cpo(self):
        head = label(r"Complete partial orders", font_size=36).to_edge(UP, buff=0.3)
        xs = [-4.6, -4.2, -4.7, -4.3, -4.5]
        ys = [-3.0, -2.1, -1.2, -0.3, 0.6]
        dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=DATA) for x, y in zip(xs, ys)])
        dl = VGroup(*[MathTex(rf"d_{k}", font_size=28, color=DATA).next_to(d, LEFT, buff=0.18)
                      for k, d in enumerate(dots)])
        segs = VGroup(*[Line(dots[k].get_center(), dots[k + 1].get_center(), color=GREY_C, stroke_width=2)
                        for k in range(4)])
        vd = MathTex(r"\vdots", font_size=30, color=GREY_B).move_to([-4.45, 1.2, 0])
        lub = Dot([-4.45, 1.95, 0], radius=0.11, color=YES)
        lubl = MathTex(r"\bigsqcup_n d_n", font_size=30, color=YES).next_to(lub, RIGHT, buff=0.2)
        ubs = VGroup(Dot([-3.2, 2.65, 0], radius=0.08, color=GREY_B), Dot([-5.5, 2.6, 0], radius=0.08, color=GREY_B))
        ubl = label(r"other upper bounds", font_size=18, color=GREY_B).next_to(ubs[0], RIGHT, buff=0.15)
        ubln = VGroup(*[Line(lub.get_center(), u.get_center(), color=GREY_D, stroke_width=1.5) for u in ubs])
        defs = VGroup(
            wrapped_label(r"a \textbf{cpo}: \ a partial order $\sqsubseteq$ \ with", 6.6, font_size=24, color=WHITE),
            wrapped_label(r"1. \ a least element $\bot$: \ no information at all", 6.6, font_size=22, color=GREY_A),
            wrapped_label(r"2. \ a least upper bound $\bigsqcup_n d_n$ for every chain \ "
                          r"$d_0 \sqsubseteq d_1 \sqsubseteq d_2 \sqsubseteq \cdots$", 6.6, font_size=22,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 1.3, 0])
        ex = VGroup(
            wrapped_label(r"in $\mathbb{Z}_\bot$ a chain climbs at most one step", 6.6, font_size=21, color=GREY_A),
            wrapped_label(r"among partial functions a chain can climb forever; \ its least upper bound collects "
                          r"all their answers", 6.6, font_size=21, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(defs, DOWN, buff=0.6).align_to(defs, LEFT)
        strips = VGroup(*[strip(v, w=0.52, h=0.42, fs=22) for v in (["1", None, None], ["1", "1", None],
                                                                    ["1", "1", "2"])]).arrange(
            RIGHT, buff=0.35).next_to(ex, DOWN, buff=0.35).align_to(ex, LEFT)
        lt = VGroup(*[MathTex(r"\sqsubseteq", font_size=28, color=GREY_B).move_to(
            (strips[k].get_right() + strips[k + 1].get_left()) / 2) for k in range(2)])
        cd = MathTex(r"\sqsubseteq \cdots", font_size=28, color=GREY_B).next_to(strips, RIGHT, buff=0.15)
        with self.voiceover(
            "Domains are partial orders with two extra properties. <bookmark mark='a'/> There is a least element, "
            "bottom: no information at all. <bookmark mark='b'/> And every chain, each element at least as defined as"
            " the one before, has a least upper bound: above them all, and below every other bound. This is a "
            "complete partial order, a cpo. <bookmark mark='c'/> In the integers, chains climb at most one step. But "
            "among partial functions a chain can climb forever, and its least upper bound collects all of their "
            "answers. That is how an infinite object, like factorial on all the naturals, is reached from finite "
            "pieces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defs[0]))
            vo.wait_until("a")
            self.play(FadeIn(defs[1]), FadeIn(dots[0]), FadeIn(dl[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]))
            for k in range(1, 5):
                self.play(Create(segs[k - 1]), FadeIn(dots[k]), FadeIn(dl[k]), run_time=0.6)
            self.play(FadeIn(vd), FadeIn(lub, scale=1.5), FadeIn(lubl))
            self.play(Create(ubln), FadeIn(ubs), FadeIn(ubl))
            vo.wait_until("c")
            self.play(FadeIn(ex[0]))
            self.play(FadeIn(ex[1]), FadeIn(strips), FadeIn(lt), FadeIn(cd))
        self.wait(0.4)
        self.clear_scene()

    def continuity(self):
        head = label(r"Continuity", font_size=36).to_edge(UP, buff=0.3)
        fs = 34
        mono_ = VGroup(label(r"monotone", font_size=24, color=GREY_A),
                       MathTex(r"d \sqsubseteq e", r"\implies", r"F(d) \sqsubseteq F(e)", font_size=fs))
        cont = VGroup(label(r"continuous", font_size=24, color=YES),
                      MathTex(r"F\Big(\bigsqcup_n d_n\Big)", r"=", r"\bigsqcup_n F(d_n)", font_size=fs, color=YES))
        for g in (mono_, cont):
            g.arrange(RIGHT, buff=0.5)
        defs = VGroup(mono_, cont).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.45)
        intu = wrapped_label(r"any finite part of the output depends on only a finite part of the input", 12.4,
                             font_size=22, color=WHITE).next_to(defs, DOWN, buff=0.35)
        hdef = MathTex(r"H(g) = \begin{cases} 1 & g \text{ total} \\ \bot & \text{otherwise} \end{cases}",
                       font_size=32, color=NO)
        hnote = label(r"monotone, \ but not continuous", font_size=20, color=NO)
        hg = VGroup(hdef, hnote).arrange(DOWN, buff=0.2).move_to([-4.0, -1.75, 0])
        chain = VGroup(*[MathTex(rf"H(g_{k}) = \bot", font_size=28, color=GREY_A) for k in range(3)],
                       MathTex(r"\cdots", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.45)
        l1 = MathTex(r"\bigsqcup_k H(g_k)", r"=", r"\bot", font_size=32, color=GREY_A)
        l2 = MathTex(r"H\Big(\bigsqcup_k g_k\Big)", r"=", r"H(\mathit{fact}_{\mathbb{N}})", r"=", r"1",
                     font_size=32, color=NO)
        right = VGroup(chain, l1, l2).arrange(DOWN, buff=0.3).move_to([2.6, -1.6, 0])
        cap = label(r"$g_k$: \ factorial on $0, \ldots, k-1$; \ each partial, \ their limit total", font_size=19,
                    color=GREY_B).next_to(right, UP, buff=0.3)
        foot = note(r"$H$ would decide totality: \ a cousin of the halting problem \ (Part 25)", font_size=18
                    ).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Kleene's theorem needs two properties of F. <bookmark mark='a'/> It must be monotone: more information "
            "in gives at least as much out. <bookmark mark='b'/> And it must be continuous, in Scott's sense: F of "
            "the limit of a chain is the limit of F along the chain. Any finite part of the output depends on only a "
            "finite part of the input. <bookmark mark='c'/> Here is a monotone function that is not continuous. H "
            "returns one if its argument is a total function, and bottom otherwise. <bookmark mark='d'/> Along the "
            "chain of partial factorials every answer is bottom, so the limit is bottom; but H of the limit is one. "
            "<bookmark mark='e'/> No program computes H: it would decide whether a function halts everywhere, a "
            "cousin of Part 25's halting problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mono_))
            vo.wait_until("b")
            self.play(FadeIn(cont[0]), Write(cont[1]))
            self.play(FadeIn(intu))
            vo.wait_until("c")
            self.play(FadeIn(hg))
            vo.wait_until("d")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(l1))
            self.play(FadeIn(l2))
            self.play(Circumscribe(VGroup(l1[2], l2[4]), color=NO))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def kleene(self):
        head = label(r"Kleene's fixed-point theorem", font_size=36).to_edge(UP, buff=0.3)
        stmt = VGroup(
            label(r"If $D$ is a cpo and $F : D \to D$ is continuous, \ then", font_size=24, color=WHITE),
            MathTex(r"\mathrm{fix}\,F \;=\; \bigsqcup_{n \ge 0} F^n(\bot)", font_size=38, color=YES),
            label(r"is the least fixed point of $F$.", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.4)
        if stmt.width > 13.2:
            stmt.scale_to_fit_width(13.2)
        fs = 32
        t1 = label(r"a chain", font_size=22, color=KERN)
        e1 = MathTex(r"\bot \sqsubseteq F(\bot)", r"\implies", r"F^n(\bot) \sqsubseteq F^{n+1}(\bot)", font_size=fs)
        w1 = label(r"$\bot$ is least; \ apply the monotone $F$ \ $n$ times", font_size=19, color=GREY_B)
        t2 = label(r"a fixed point", font_size=22, color=HEAD)
        lhs = MathTex(r"F\Big(\bigsqcup_n F^n(\bot)\Big)", r"=", font_size=fs)
        v1 = MathTex(r"\bigsqcup_n", r"F\big(", r"F^n(\bot)", r"\big)", font_size=fs)
        v2 = MathTex(r"\bigsqcup_n", r"F^{n+1}(\bot)", font_size=fs)
        v3 = MathTex(r"\bigsqcup_n", r"F^{n}(\bot)", font_size=fs, color=HEAD)
        w2s = [label(s, font_size=19, color=GREY_B) for s in
               (r"continuity", r"the same as $F^{n+1}$", r"the same chain with $\bot$ in front: \ the same limit")]
        t3 = label(r"the least", font_size=22, color=YES)
        e3 = MathTex(r"F(d) = d", r"\implies", r"F^n(\bot) \sqsubseteq F^n(d) = d", r"\implies",
                     r"\bigsqcup_n F^n(\bot) \sqsubseteq d", font_size=fs)
        w3 = label(r"induction on $n$; \ a least upper bound is below every upper bound", font_size=19,
                   color=GREY_B)
        rows = VGroup(VGroup(t1, e1), VGroup(t2, lhs), VGroup(t3, e3))
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.85).next_to(stmt, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
            r[1].set_x(-3.3 + r[1].width / 2)
        for t in (t1, t2, t3):
            t.set_x(-6.3 + t.width / 2)
        for v in (v1, v2, v3):
            v.next_to(lhs, RIGHT, buff=0.2)
        w1.next_to(e1, DOWN, buff=0.15).align_to(e1, LEFT)
        for w in w2s:
            w.next_to(lhs, DOWN, buff=0.15).align_to(lhs, LEFT)
        w3.next_to(e3, DOWN, buff=0.15).align_to(e3, LEFT)
        foot = note(r"Part 13's liveness analysis climbed the same way, \ in a finite lattice where the climb "
                    r"stops", font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the theorem, usually credited to Stephen Kleene. <bookmark mark='a'/> If D is a cpo and F is "
            "continuous, then the limit of bottom, F of bottom, F of F of bottom, and so on, is the least fixed point"
            " of F. <bookmark mark='b'/> First, a chain: bottom is below F of bottom, since bottom is below "
            "everything; apply the monotone F n times. <bookmark mark='c'/> Second, a fixed point. Apply F to the "
            "limit. By continuity, F passes inside. <bookmark mark='d'/> F of F to the n is F to the n plus one: "
            "<bookmark mark='e'/> the same chain with bottom missing from the front, so the same limit. <bookmark "
            "mark='f'/> Third, the least: by induction, every element of the chain is below any fixed point d, so "
            "their least upper bound is too. <bookmark mark='g'/> It is the climb of Part 13's liveness analysis; "
            "here it may go on forever, and continuity carries us to the limit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt[0]), Write(stmt[1]), FadeIn(stmt[2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(t1), Write(e1), FadeIn(w1))
            vo.wait_until("c")
            self.play(FadeIn(t2), Write(lhs))
            self.play(FadeIn(v1), FadeIn(w2s[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(v1, v2), ReplacementTransform(w2s[0], w2s[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(v2, v3), ReplacementTransform(w2s[1], w2s[2]))
            vo.wait_until("f")
            self.play(FadeIn(t3), Write(e3), FadeIn(w3), run_time=2)
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def chain(self):
        rows = load("kleene")["rows"]
        head = label(r"The Kleene chain of factorial", font_size=36).to_edge(UP, buff=0.3)
        y0, dy = -2.75, 0.58
        cw, x0 = 0.72, -3.7
        ncol = len(rows[0]["table"])
        dots, names, strips_, arrows = VGroup(), VGroup(), [], VGroup()
        for r in rows:
            k = r["k"]
            y = y0 + k * dy
            d = Dot([-6.3, y, 0], radius=0.08, color=DATA)
            nm = MathTex(r"\bot" if k == 0 else (r"F(\bot)" if k == 1 else rf"F^{{{k}}}(\bot)"), font_size=26,
                         color=DATA).next_to(d, RIGHT, buff=0.2)
            s = strip([None if v is None else str(v) for v in r["table"]], w=cw - 0.06, h=0.46, fs=24)
            s.move_to([x0 + s.width / 2, y, 0])
            dots.add(d)
            names.add(nm)
            strips_.append(s)
        for k in range(len(rows) - 1):
            arrows.add(Line(dots[k].get_center(), dots[k + 1].get_center(), color=GREY_C, stroke_width=2))
        hdr = VGroup(*[MathTex(str(n), font_size=20, color=GREY_B).move_to([strips_[0][n].get_x(), y0 - 0.45, 0])
                       for n in range(ncol)])
        nlab = MathTex(r"n", font_size=22, color=GREY_B).next_to(hdr, LEFT, buff=0.3)
        top = rows[-1]["table"]
        lub_vals = [str(v) for v in top[:-1]] + [r"\cdots"]
        ytop = y0 + len(rows) * dy + 0.35
        lub_s = strip(lub_vals, w=cw - 0.06, h=0.46, fs=24, color=YES)
        lub_s.move_to([x0 + lub_s.width / 2, ytop, 0])
        for c in lub_s:
            c[0].set_stroke(YES, width=2)
        lub_d = Dot([-6.3, ytop, 0], radius=0.11, color=YES)
        lub_n = MathTex(r"\bigsqcup_k F^k(\bot)", font_size=24, color=YES).next_to(lub_d, RIGHT, buff=0.15)
        vd = MathTex(r"\vdots", font_size=26, color=GREY_B).move_to([-6.3, (ytop + y0 + (len(rows) - 1) * dy) / 2, 0])
        notes = VGroup(
            wrapped_label(r"$F(h)(n) = 1$ if $n = 0$, \ else $n \cdot h(n-1)$: \ each application adds one answer",
                          4.3, font_size=20, color=WHITE),
            wrapped_label(r"$F^k(\bot)$ is factorial unrolled $k$ times: \ defined on inputs that need fewer than $k$ "
                          r"recursive calls", 4.3, font_size=20, color=DATA),
            wrapped_label(r"the limit: \ factorial on all of $\mathbb{N}$, \ undefined on negative numbers", 4.3,
                          font_size=20, color=YES),
            VGroup(MathTex(r"[\![\,\mathsf{while}\ b\ \mathsf{do}\ c\,]\!] = \bigsqcup_k W^k(\bot)", font_size=26,
                           color=KERN),
                   wrapped_label(r"$W^k(\bot)$: \ the loop run at most $k$ times, \ $\bot$ if it needs more", 4.3,
                                 font_size=20, color=KERN)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        notes.move_to([4.55, -0.2, 0])
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        src = note(r"computed: \ our Kleene iteration of the factorial functional", font_size=16).next_to(
            notes, DOWN, buff=0.3).align_to(notes, LEFT)
        with self.voiceover(
            "Here is the theorem at work, computed by our instrument. <bookmark mark='a'/> Start with bottom, the "
            "function that knows nothing. <bookmark mark='b'/> Apply factorial's F once, and it knows that factorial "
            "of zero is one. Again, and it knows zero and one. Each application adds one answer. <bookmark mark='c'/>"
            " So the k-th function is factorial unrolled k times: it answers every input that needs fewer than k "
            "recursive calls. <bookmark mark='d'/> The chain never stops, but its least upper bound is the whole of "
            "factorial, the least fixed point that chapter two was looking for, still undefined on negative numbers. "
            "<bookmark mark='e'/> A while loop works the same way: its meaning is the least fixed point of one "
            "unrolling, and the k-th approximation runs the loop at most k times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(nlab))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(names[0]), FadeIn(strips_[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            for k in range(1, len(rows)):
                if k == 4:
                    vo.wait_until("c")
                    self.play(FadeIn(notes[1]))
                new = strips_[k][k - 1]
                self.play(Create(arrows[k - 1]), FadeIn(dots[k]), FadeIn(names[k]),
                          ReplacementTransform(strips_[k - 1].copy(), strips_[k]), run_time=0.8)
                self.play(Indicate(new, color=HEAD, scale_factor=1.15), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(vd), FadeIn(lub_d, scale=1.5), FadeIn(lub_n), FadeIn(lub_s), FadeIn(notes[2]),
                      FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def dinf(self):
        head = label(r"Scott's $D_\infty$: \ a model of the untyped $\lambda$-calculus", font_size=36).to_edge(
            UP, buff=0.3)
        need = MathTex(r"D", r"\;\cong\;", r"[D \to D]", font_size=48, color=WHITE).next_to(head, DOWN, buff=0.5)
        needl = label(r"every term is a function, \ and can be applied to any term, \ itself included \ (Part 14)",
                      font_size=21, color=GREY_A).next_to(need, DOWN, buff=0.2)
        cantor = VGroup(MathTex(r"|D \to D| \;\ge\; |2^D| \;>\; |D|", font_size=34, color=NO),
                        label(r"for all set functions, \ once $D$ has two elements \ (Cantor)", font_size=20,
                              color=NO)).arrange(DOWN, buff=0.15)
        cantor.move_to([-3.8, -0.5, 0])
        boxes = VGroup()
        for k in range(4):
            r = RoundedRectangle(width=1.0 + 1.3 * k, height=0.7 + 0.55 * k, corner_radius=0.15,
                                 stroke_color=[DATA, LAM, KERN, YES][k], stroke_width=2)
            boxes.add(r)
        for r in boxes:
            r.move_to([3.6, -0.75, 0], aligned_edge=DOWN)
            r.shift(DOWN * 0.0)
        bl = VGroup(*[MathTex(s, font_size=24, color=c).next_to(boxes[k].get_top(), DOWN, buff=0.08)
                      for k, (s, c) in enumerate(((r"D_0", DATA), (r"D_1 = [D_0 \to D_0]", LAM),
                                                   (r"D_2 = [D_1 \to D_1]", KERN), (r"\cdots", YES)))])
        bl[0].move_to(boxes[0])
        for k in (1, 2, 3):
            bl[k].next_to(boxes[k].get_top(), DOWN, buff=0.08)
        stack = VGroup(boxes, bl)
        stack.move_to([3.6, -0.6, 0])
        sl = label(r"continuous functions only, \ each domain inside the next", font_size=20, color=GREY_A).next_to(
            stack, DOWN, buff=0.2)
        lim = VGroup(MathTex(r"D_\infty", r"\;\cong\;", r"[D_\infty \to D_\infty]", font_size=44, color=YES),
                     label(r"the limit: \ Dana Scott, \ 1969", font_size=21, color=YES)).arrange(RIGHT, buff=0.5)
        lim.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The same ideas answered an old question about Church's lambda calculus, from Part 14: does the untyped "
            "calculus have a mathematical model at all? <bookmark mark='a'/> There, every term is a function that can"
            " be applied to any term, even itself, so a model needs a space D that is the same as the functions from "
            "D to D. <bookmark mark='b'/> For ordinary functions that is impossible: by Cantor's diagonal argument, "
            "there are always more functions from D to D than elements of D. <bookmark mark='c'/> Dana Scott's "
            "answer, in nineteen sixty-nine, was to use only continuous functions, and to build D as a limit: a "
            "domain, its space of continuous functions, that space's, and so on, each inside the next. <bookmark "
            "mark='d'/> The limit, D infinity, is isomorphic to its own space of continuous functions: the first "
            "mathematical model of the untyped lambda calculus."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(need), FadeIn(needl))
            vo.wait_until("b")
            self.play(FadeIn(cantor))
            vo.wait_until("c")
            for k in range(4):
                self.play(Create(boxes[k]), FadeIn(bl[k]), run_time=0.7)
            self.play(FadeIn(sl))
            vo.wait_until("d")
            self.play(FadeIn(lim))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, LAM, NO)
