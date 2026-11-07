from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono

FIX = "(fix fact n -> (if (n = 0) then 1 else (n * (fact (n - 1)))))"


def sem(e: str) -> str:
    """The semantic brackets around a term (TeX)."""
    return r"[\![\," + e + r"\,]\!]"


def panel(title, body, color, w=5.6, h=3.4):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=color, stroke_width=2,
                             fill_color=BG, fill_opacity=1)
    t = label(title, font_size=24, color=color).next_to(frame.get_top(), DOWN, buff=0.2)
    if body.width > w - 0.4:
        body.scale_to_fit_width(w - 0.4)
    body.next_to(t, DOWN, buff=0.3)
    return VGroup(frame, t, body)


def mini(values, w=0.42, h=0.34, fs=18):
    """A partial function's table, small: values, or bottom where undefined."""
    cells = VGroup()
    for v in values:
        r = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.2, fill_color=BG, fill_opacity=1)
        t = MathTex(r"\bot" if v is None else str(v), font_size=fs, color=GREY_C if v is None else YES)
        if t.width > w - 0.06:
            t.scale_to_fit_width(w - 0.06)
        cells.add(VGroup(r, t.move_to(r)))
    return cells.arrange(RIGHT, buff=0.04)


class Adequacy(VoiceoverScene):
    def construct(self):
        self.card()
        self.bridge()
        self.soundness()
        self.ladder()
        self.proof()
        self.full_abstraction()
        self.games()

    def card(self):
        card = chapter_card(4, r"Adequacy and full abstraction", r"Do the steps and the mathematics agree?",
                            lit=(1977,), extra=((1977, r"Plotkin: \ LCF considered as a programming language"),),
                            part=PART)
        with self.voiceover("Chapter four. Adequacy and full abstraction. Do the steps and the mathematics agree?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bridge(self):
        f = load("fact")
        head = label(r"Two meanings, \ one program", font_size=36).to_edge(UP, buff=0.3)
        tail = [s.replace(FIX, "fact") for s in f["trace"][-4:]]
        steps = VGroup(*[mono(s, size=20, color=GREY_A) for s in tail]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        steps[-1].set_color(YES)
        left = panel(r"steps \ (chapter 1)", VGroup(mono("fact 3", size=22, color=WHITE),
                                                   MathTex(r"\to^{*}", font_size=30), steps).arrange(DOWN, buff=0.2),
                     HEAD)
        right = panel(r"mathematics \ (chapters 2 and 3)",
                      VGroup(MathTex(sem(r"\mathit{fact}\ 3") + r"=" + sem(r"\mathit{fact}") + r"(3)", font_size=32),
                             MathTex(r"= \Big(\bigsqcup_k F^k(\bot)\Big)(3) = " + str(f["value"]), font_size=32,
                                     color=YES)).arrange(DOWN, buff=0.3), DATA)
        VGroup(left, right).arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.4)
        a1 = Arrow(left.get_right() + UP * 0.6, right.get_left() + UP * 0.6, buff=0.1, color=YES, stroke_width=3)
        a2 = Arrow(right.get_left() + DOWN * 0.6, left.get_right() + DOWN * 0.6, buff=0.1, color=KERN,
                   stroke_width=3)
        l1 = label(r"soundness", font_size=20, color=YES).next_to(a1, UP, buff=0.1)
        l2 = label(r"adequacy", font_size=20, color=KERN).next_to(a2, DOWN, buff=0.1)
        thms = VGroup(
            MathTex(r"\text{soundness:}\quad", r"e \to^{*} v", r"\implies", sem("e") + "=" + sem("v"), font_size=36,
                    color=YES),
            MathTex(r"\text{adequacy:}\quad", sem("e") + r"= n", r"\implies", r"e \to^{*} n", font_size=36,
                    color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tnote = label(r"$e$ a closed program of type \textsf{int}; \ together: \ $e$ diverges exactly when "
                      r"$[\![\,e\,]\!] = \bot$", font_size=22, color=GREY_A)
        VGroup(thms, tnote).arrange(DOWN, buff=0.3).next_to(VGroup(left, right), DOWN, buff=0.7)
        with self.voiceover(
            "We now have two meanings for every program: the steps of chapter one, and the mathematics of chapters "
            "two and three. Do they agree? <bookmark mark='a'/> Soundness: if a program steps to a value, its "
            "denotation is the denotation of that value. Computing never changes meaning. <bookmark mark='b'/> "
            "Adequacy: if the denotation of a whole program of integer type is a number n, not bottom, then the "
            "machine really does reach n. <bookmark mark='c'/> Together, the mathematics predicts exactly what the "
            "machine does, including whether it stops. Gordon Plotkin proved this in nineteen seventy-seven for PCF, "
            "a typed lambda calculus with numbers, booleans and fix: essentially our language, with types."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(thms[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(thms[1]))
            vo.wait_until("c")
            self.play(FadeIn(tnote))
        self.wait(0.4)
        self.clear_scene()

    def soundness(self):
        head = label(r"Soundness: \ each step preserves meaning", font_size=36).to_edge(UP, buff=0.3)
        fs = 34
        rows = VGroup(
            MathTex(sem(r"(\mathsf{fun}\ x \to e)\ v") + r"\rho", font_size=fs),
            MathTex(r"=", r"\big(\lambda u.\ " + sem("e") + r"\rho[x \mapsto u]\big)", r"\big(", sem("v") + r"\rho",
                    r"\big)", font_size=fs),
            MathTex(r"=", sem("e") + r"\rho[x \mapsto", sem("v") + r"\rho", r"]", font_size=fs),
            MathTex(r"=", sem("e[v/x]") + r"\rho", font_size=fs, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        for r in rows[1:]:
            r.shift(RIGHT * 0.5)
        whys = VGroup(
            label(r"the \textsc{Beta} rule's left side", font_size=21, color=GREY_B),
            label(r"the application and function equations", font_size=21, color=GREY_B),
            label(r"apply the map", font_size=21, color=GREY_B),
            label(r"substitution lemma \ (induction on $e$)", font_size=21, color=YES),
        )
        wx = max(r.get_right()[0] for r in rows) + 0.6
        for w, r in zip(whys, rows):
            w.move_to([wx + w.width / 2, r.get_y(), 0])
        if whys.get_right()[0] > 6.85:
            whys.shift(LEFT * (whys.get_right()[0] - 6.85))
        rest = wrapped_label(r"\textsc{Fix}: \ the same, \ using $[\![\,\mathsf{fix}\ f\ x \to e\,]\!] = "
                             r"F([\![\,\mathsf{fix}\ f\ x \to e\,]\!])$; \ \ search rules: \ compositionality", 12.4,
                             font_size=21, color=WHITE).next_to(rows, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        hard = VGroup(
            label(r"adequacy by induction on $e$? \ \ the case $e_1\ e_2$:", font_size=22, color=KERN),
            MathTex(sem("e_1") + r"\ \text{is a function}\ \varphi", r"\qquad", r"e_1 \Downarrow\ ?", font_size=30,
                    color=WHITE),
            label(r"a hypothesis about \textsf{int} says nothing about $e_1 : \textsf{int} \to \textsf{int}$",
                  font_size=20, color=NO),
        ).arrange(DOWN, buff=0.18).next_to(rest, DOWN, buff=0.6).set_x(0)
        hard[1][2].set_color(NO)
        box = SurroundingRectangle(hard, buff=0.15, corner_radius=0.1, color=GREY_D, stroke_width=1.5)
        with self.voiceover(
            "Soundness is the easy direction: show that one step preserves meaning, then count the steps. <bookmark "
            "mark='a'/> Take the beta rule, a function applied to a value. <bookmark mark='b'/> By the equations, its"
            " meaning is the map, applied to the value's meaning. <bookmark mark='c'/> Applying the map binds x to "
            "that meaning. <bookmark mark='d'/> And by a substitution lemma, proved by induction on e, that is the "
            "meaning of the body with the value substituted. <bookmark mark='e'/> The fix rule works the same way, "
            "and it is exactly where we need fix to mean a fixed point. <bookmark mark='f'/> Adequacy is harder. Try "
            "induction on the program. At an application, all we know is that the function's meaning is some "
            "mathematical function, and a hypothesis about integers says nothing about the function program. We need "
            "a statement about every type at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            for k, mk in enumerate("bcd", start=1):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k - 1].copy(), rows[k]), FadeIn(whys[k]), run_time=1.4)
            vo.wait_until("e")
            self.play(FadeIn(rest))
            vo.wait_until("f")
            self.play(FadeIn(hard), Create(box))
        self.wait(0.4)
        self.clear_scene()

    def ladder(self):
        head = label(r"A logical relation: \ a ladder of types", font_size=36).to_edge(UP, buff=0.3)
        xl, xr = -6.2, -3.4
        ys = [-2.6, -0.9, 0.8, 2.3]
        rail_l = Line([xl, -3.1, 0], [xl, 2.75, 0], color=GREY_C, stroke_width=3)
        rail_r = Line([xr, -3.1, 0], [xr, 2.75, 0], color=GREY_C, stroke_width=3)
        cols = [DATA, HEAD, LAM, GREY_B]
        rungs = VGroup(*[Line([xl, y, 0], [xr, y, 0], color=c, stroke_width=5) for y, c in zip(ys, cols)])
        names = VGroup(*[MathTex(s, font_size=26, color=c).next_to(r, UP, buff=0.1) for s, r, c in
                         zip((r"\mathsf{int}", r"\mathsf{int} \to \mathsf{int}",
                              r"(\mathsf{int} \to \mathsf{int}) \to \mathsf{int}", r"\vdots"), rungs, cols)])
        ups = VGroup(*[Arrow([xr + 0.25, ys[k] + 0.05, 0], [xr + 0.25, ys[k + 1] - 0.05, 0], buff=0.05,
                             color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.12) for k in range(2)])
        d_int = VGroup(
            MathTex(r"d \;\triangleleft_{\mathsf{int}}\; e", r"\iff", r"d = \bot", r"\ \text{or}\ ",
                    r"e \Downarrow d", font_size=32, color=DATA),
            label(r"a number is related to a program that evaluates to it", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        d_fun = VGroup(
            MathTex(r"d \;\triangleleft_{\sigma \to \tau}\; e", r"\iff", r"d = \bot", r"\ \text{or}\ ",
                    r"e \Downarrow v \ \text{with}", font_size=32, color=HEAD),
            MathTex(r"a \;\triangleleft_\sigma\; e'", r"\implies", r"d(a) \;\triangleleft_\tau\; v\ e'",
                    r"\quad \text{for all } a,\ e'", font_size=32, color=HEAD),
            label(r"related arguments go to related results", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        d_fun[1].shift(RIGHT * 0.6)
        d_int.move_to([2.0, ys[0] + 0.3, 0])
        d_fun.move_to([2.0, ys[1] + 0.85, 0])
        for g in (d_int, d_fun):
            g.align_to(np.array([-2.6, 0, 0]), LEFT)
        wf = wrapped_label(r"each rung uses only smaller types: \ well defined because the language is typed", 9.0,
                           font_size=21, color=WHITE).move_to([2.0, ys[2] + 0.5, 0]).align_to(np.array([-2.6, 0, 0]),
                                                                                           LEFT)
        src = note(r"simplified, \ after Winskel's textbook proof for an eager language", font_size=16).to_corner(
            DR, buff=0.3)
        with self.voiceover(
            "That statement is a logical relation: one relation for each type, each built on smaller types, like the "
            "rungs of a ladder. <bookmark mark='a'/> On the bottom rung, the integers: a meaning d is related to a "
            "program e if d is bottom, or e evaluates to d. <bookmark mark='b'/> On the rung for functions from sigma"
            " to tau, d is related to e if d is bottom, or e evaluates to a function value v, and whenever a meaning "
            "a is related to an argument program, d of a is related to v applied to that program. <bookmark "
            "mark='c'/> Related arguments go to related results. <bookmark mark='d'/> Each rung uses only smaller "
            "types, so the definition is well founded; that is why the language must be typed."
        ) as vo:
            self.play(FadeIn(head), Create(rail_l), Create(rail_r))
            vo.wait_until("a")
            self.play(Create(rungs[0]), FadeIn(names[0]), FadeIn(d_int))
            vo.wait_until("b")
            self.play(GrowArrow(ups[0]), Create(rungs[1]), FadeIn(names[1]), FadeIn(d_fun[0]))
            self.play(FadeIn(d_fun[1]))
            vo.wait_until("c")
            self.play(FadeIn(d_fun[2]))
            vo.wait_until("d")
            self.play(GrowArrow(ups[1]), Create(rungs[2]), FadeIn(names[2]), Create(rungs[3]), FadeIn(names[3]),
                      FadeIn(wf), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = load("kleene")["rows"]
        head = label(r"The fundamental lemma", font_size=36).to_edge(UP, buff=0.3)
        lem = VGroup(MathTex(sem("e"), r"\;\triangleleft_\tau\;", "e", font_size=40, color=YES),
                     label(r"for every closed program $e : \tau$ \ \ (induction on $e$)", font_size=22,
                           color=GREY_A)).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.35)
        ks = range(4)
        ys = [-1.9 + 0.85 * k for k in ks]
        dots = VGroup(*[Dot([-5.6, y, 0], radius=0.09, color=DATA) for y in ys])
        segs = VGroup(*[Line(dots[k].get_center(), dots[k + 1].get_center(), color=GREY_C, stroke_width=2)
                        for k in range(3)])
        nms = VGroup(*[MathTex(r"\bot" if k == 0 else (r"F(\bot)" if k == 1 else rf"F^{{{k}}}(\bot)"), font_size=24,
                               color=DATA).next_to(dots[k], LEFT, buff=0.15) for k in ks])
        tabs = VGroup(*[mini(rows[k]["table"][:5]).next_to(dots[k], RIGHT, buff=0.3) for k in ks])
        vd = MathTex(r"\vdots", font_size=26, color=GREY_B).move_to([-5.6, ys[-1] + 0.6, 0])
        lub = Dot([-5.6, ys[-1] + 1.2, 0], radius=0.11, color=YES)
        lubn = MathTex(sem(r"\mathit{fact}") + r"= \bigsqcup_k F^k(\bot)", font_size=24, color=YES).next_to(
            lub, RIGHT, buff=0.2)
        prog = VGroup(mono("fact", size=24, color=WHITE))
        pbox = SurroundingRectangle(prog, buff=0.2, corner_radius=0.1, color=GREY_B)
        prog = VGroup(pbox, prog).move_to([0.4, ys[1] + 0.4, 0])
        links = VGroup(*[DashedLine(tabs[k].get_right(), pbox.get_left(), color=GREY_B, stroke_width=1.6,
                                    dash_length=0.08) for k in ks])
        lublink = DashedLine(lubn.get_right(), pbox.get_left(), color=YES, stroke_width=2.2, dash_length=0.08)
        rel = MathTex(r"\triangleleft", font_size=30, color=GREY_B).next_to(pbox, UP, buff=0.15)
        steps = VGroup(
            wrapped_label(r"1. \ $\bot \triangleleft e$: \ true on every rung, \ by definition", 5.2, font_size=20,
                          color=GREY_A),
            wrapped_label(r"2. \ if $F^k(\bot) \triangleleft \mathit{fact}$ then $F^{k+1}(\bot) \triangleleft "
                          r"\mathit{fact}$: \ one more unrolling matches one more use of \textsc{Fix}", 5.2,
                          font_size=20, color=DATA),
            wrapped_label(r"3. \ each relation is closed under limits of chains \ (\textit{admissible}): \ so the "
                          r"limit is related", 5.2, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.1, 0])
        if steps.get_right()[0] > 6.85:
            steps.shift(LEFT * (steps.get_right()[0] - 6.85))
        fs = 34
        a0 = MathTex(sem("e"), r"=", r"n", font_size=fs, color=WHITE)
        a1 = MathTex(r"n", r"\;\triangleleft_{\mathsf{int}}\;", r"e", font_size=fs, color=WHITE)
        a2 = MathTex(r"e", r"\Downarrow", r"n", font_size=fs, color=YES)
        tag = label(r"at type \textsf{int}: \ adequacy", font_size=22, color=YES)
        for a in (a0, a1, a2):
            a.move_to([0.0, -3.05, 0])
        tag.next_to(a0, LEFT, buff=0.8)
        tabsrc = note(r"tables: \ our Kleene chain of factorial, \ inputs 0 to 4", font_size=16).next_to(
            dots[0], DOWN, buff=0.3).align_to(nms[0], LEFT)
        with self.voiceover(
            "The fundamental lemma: every well-typed closed program is related to its own meaning. <bookmark "
            "mark='a'/> The hard case is fix, whose meaning is the limit of a Kleene chain, here factorial's. Bottom "
            "is related to anything, by definition. <bookmark mark='b'/> If one approximation is related to the "
            "program, so is the next, because one more unrolling of the meaning matches one more use of the fix rule."
            " <bookmark mark='c'/> And each relation is closed under limits of chains, a property called "
            "admissibility, so the limit, the meaning itself, is related. <bookmark mark='d'/> Now read the lemma at "
            "type int. If the meaning of e is a number n, <bookmark mark='e'/> then n is related to e, <bookmark "
            "mark='f'/> which, on the bottom rung, means that e evaluates to n. That is adequacy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lem))
            vo.wait_until("a")
            self.play(FadeIn(prog), FadeIn(dots[0]), FadeIn(nms[0]), FadeIn(tabs[0]), FadeIn(tabsrc))
            self.play(Create(links[0]), FadeIn(rel), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            for k in range(1, 4):
                self.play(Create(segs[k - 1]), FadeIn(dots[k]), FadeIn(nms[k]), FadeIn(tabs[k]),
                          Create(links[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(vd), FadeIn(lub, scale=1.5), FadeIn(lubn), FadeIn(steps[2]))
            self.play(Create(lublink))
            vo.wait_until("d")
            self.play(FadeIn(tag), Write(a0))
            vo.wait_until("e")
            self.play(TransformMatchingTex(a0, a1), run_time=1.3)
            vo.wait_until("f")
            self.play(TransformMatchingTex(a1, a2), run_time=1.3)
            self.play(Circumscribe(a2, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def full_abstraction(self):
        head = label(r"Full abstraction, \ and parallel-or", font_size=36).to_edge(UP, buff=0.3)
        ce = MathTex(r"e_1 \cong e_2", r"\iff", r"\text{for every context } C:\ \ C[e_1] \Downarrow n \iff "
                     r"C[e_2] \Downarrow n", font_size=30, color=WHITE).next_to(head, DOWN, buff=0.35)
        i1 = VGroup(MathTex(sem("e_1") + "=" + sem("e_2"), r"\implies", r"e_1 \cong e_2", font_size=30, color=YES),
                    label(r"compositionality, \ then adequacy", font_size=19, color=YES)).arrange(RIGHT, buff=0.4)
        i2 = VGroup(MathTex(r"e_1 \cong e_2", r"\implies", sem("e_1") + "=" + sem("e_2"), font_size=30, color=NO),
                    label(r"full abstraction: \ fails for PCF \ (Plotkin, \ 1977)", font_size=19, color=NO)).arrange(
            RIGHT, buff=0.4)
        imps = VGroup(i1, i2).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ce, DOWN, buff=0.3)
        tt, ff, bt = r"\mathsf{true}", r"\mathsf{false}", r"\bot"
        trows = [(r"x", r"y", r"\mathrm{por}(x, y)"), (tt, bt, tt), (bt, tt, tt), (ff, ff, ff)]
        table = VGroup()
        for i, r in enumerate(trows):
            row = VGroup(*[MathTex(c, font_size=28, color=GREY_B if i == 0 else (YES if j == 2 else WHITE))
                           for j, c in enumerate(r)])
            for j, m in enumerate(row):
                m.move_to([j * 1.5, -i * 0.5, 0])
            table.add(row)
        rule_ = Line(table[0].get_left() + DOWN * 0.25 + LEFT * 0.2, table[0].get_right() + DOWN * 0.25 + RIGHT * 0.2,
                     color=GREY_D, stroke_width=1.5)
        tab = VGroup(table, rule_)
        tl = wrapped_label(r"parallel-or: \ true if either argument is, \ even if the other never finishes; \ "
                           r"continuous, \ so in the model", 5.4, font_size=19, color=GREY_A)
        left = VGroup(tab, tl).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        tk = MathTex(r"T_k(f) = \begin{cases} k & f(\mathsf{true}, \bot) = f(\bot, \mathsf{true}) = \mathsf{true},"
                     r"\ f(\mathsf{false}, \mathsf{false}) = \mathsf{false} \\ \bot & \text{otherwise}"
                     r"\end{cases}", font_size=26, color=WHITE)
        tkl = wrapped_label(r"no PCF program can pass all three tests: \ a sequential $f$ must look at one argument "
                            r"first. \ So $T_0 \cong T_1$, \ yet $[\![\,T_0\,]\!](\mathrm{por}) = 0 \neq 1 = "
                            r"[\![\,T_1\,]\!](\mathrm{por})$", 6.3, font_size=19, color=GREY_A)
        right = VGroup(tk, tkl).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if tk.width > 6.6:
            tk.scale_to_fit_width(6.6)
        VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(imps, DOWN, buff=0.45)
        foot = label(r"Plotkin: \ add parallel-or to PCF, \ and Scott's model becomes fully abstract", font_size=21,
                     color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Two programs are contextually equivalent when no context can tell them apart. <bookmark mark='a'/> If "
            "two terms have the same meaning, then by compositionality every context gives them the same meaning, and"
            " by adequacy the same behaviour. <bookmark mark='b'/> Full abstraction is the converse: equivalent "
            "programs have equal meanings, so the model sees no distinction that programs cannot. Plotkin showed that"
            " Scott's model of PCF is not fully abstract. <bookmark mark='c'/> The culprit is parallel-or: true if "
            "either argument is true, even when the other runs forever. It is continuous, so it lives in the model, "
            "but no PCF program computes it. A sequential program must look at one argument first, and if that one "
            "loops, so does the program. <bookmark mark='d'/> So two tests that differ only on parallel-or are "
            "equivalent in PCF, though their meanings differ. <bookmark mark='e'/> And adding parallel-or to the "
            "language, Plotkin showed, makes the model fully abstract."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ce))
            vo.wait_until("a")
            self.play(FadeIn(i1))
            vo.wait_until("b")
            self.play(FadeIn(i2))
            vo.wait_until("c")
            self.play(FadeIn(table[0]), Create(rule_))
            self.play(LaggedStart(*[FadeIn(r) for r in table[1:]], lag_ratio=0.3), FadeIn(tl), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(tk))
            self.play(FadeIn(tkl))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def games(self):
        head = label(r"Games: \ sequentiality built in", font_size=36).to_edge(UP, buff=0.3)
        xo, xp = -4.6, -0.6
        to = label(r"Opponent \ (the environment)", font_size=21, color=DATA).move_to([xo, 2.4, 0])
        tp = label(r"Player \ (the program)", font_size=21, color=HEAD).move_to([xp, 2.4, 0])
        vo_l = DashedLine([xo, 2.1, 0], [xo, -2.7, 0], color=GREY_D, dash_length=0.1)
        vp_l = DashedLine([xp, 2.1, 0], [xp, -2.7, 0], color=GREY_D, dash_length=0.1)
        moves = [("O", r"result?", DATA), ("P", r"argument?", HEAD), ("O", r"true", DATA), ("P", r"false", HEAD)]
        ys = [1.5, 0.5, -0.5, -1.5]
        arrows, tags = VGroup(), VGroup()
        for (who, txt, c), y in zip(moves, ys):
            a, b = ([xo, y + 0.3, 0], [xp, y - 0.3, 0]) if who == "O" else ([xp, y + 0.3, 0], [xo, y - 0.3, 0])
            arr = Arrow(a, b, buff=0.1, color=c, stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
            t = label(txt, font_size=20, color=c).next_to(arr.get_center(), UP, buff=0.12)
            arrows.add(arr)
            tags.add(t)
        game = label(r"the game for $\mathsf{bool} \to \mathsf{bool}$: \ the strategy of \ \textsf{not}", font_size=19,
                     color=GREY_B).move_to([(xo + xp) / 2, -3.1, 0])
        notes = VGroup(
            wrapped_label(r"fully abstract models of PCF \ (1990s): \ Abramsky, \ Jagadeesan and Malacaria; \ Hyland "
                          r"and Ong; \ Nickau", 4.6, font_size=21, color=YES),
            wrapped_label(r"after identifying strategies that no test can tell apart", 4.6, font_size=18,
                          color=GREY_B),
            wrapped_label(r"a type is a game; \ a program is a strategy: \ a rule for its next move", 4.6,
                          font_size=21, color=WHITE),
            wrapped_label(r"one move at a time: \ parallel-or would have to ask both arguments at once, \ so it is "
                          r"not a strategy", 4.6, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, 0.0, 0])
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        with self.voiceover(
            "A fully abstract model of PCF itself was found in the nineteen nineties, in games: by Samson Abramsky, "
            "Radha Jagadeesan and Pasquale Malacaria, by Martin Hyland and Luke Ong, and independently by Hanno "
            "Nickau. <bookmark mark='a'/> A type becomes a game between the program and its environment, taking turns"
            " to ask and answer. <bookmark mark='b'/> A program is a strategy, a rule for its next move. Here the "
            "environment asks for a result; the program asks for its argument; told true, it answers false. <bookmark"
            " mark='c'/> A strategy makes one move at a time, so parallel-or, which must ask both of its arguments at"
            " once, is not a strategy: sequentiality is built in. <bookmark mark='d'/> Next, we ask directly when two"
            " programs are the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(to), FadeIn(tp), Create(vo_l), Create(vp_l), FadeIn(notes[0]),
                      FadeIn(notes[1]))
            vo.wait_until("a")
            self.play(FadeIn(notes[2]))
            vo.wait_until("b")
            for a, t in zip(arrows, tags):
                self.play(GrowArrow(a), FadeIn(t), run_time=0.8)
            self.play(FadeIn(game))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.6)
        self.clear_scene()


_ = (LAM,)
