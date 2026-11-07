from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono

FIX = "(fix fact n -> (if (n = 0) then 1 else (n * (fact (n - 1)))))"


def short(s: str) -> str:
    """A trace term with the recursive function written as its name."""
    return s.replace(FIX, "fact")


def term(s: str, size=22, color=GREY_A, hi=None, hi_color=HEAD):
    """A term in monospace, with the characters hi = (i, j) of the string coloured."""
    t = Text(s, font="DejaVu Sans Mono", font_size=size, color=color)
    if hi:
        a = len(s[:hi[0]].replace(" ", ""))
        b = len(s[:hi[1]].replace(" ", ""))
        if b > a:
            t[a:b].set_color(hi_color)
    return t


def changed(old: str, new: str):
    """The span of ``new`` that differs from ``old``: common prefix and suffix removed."""
    p = 0
    while p < min(len(old), len(new)) and old[p] == new[p]:
        p += 1
    s = 0
    while s < min(len(old), len(new)) - p and old[-1 - s] == new[-1 - s]:
        s += 1
    return p, len(new) - s


def rule(prems, concl, name=None, color=GREY_B, name_color=GREY_B, buff=0.5, bar=True, fs=20):
    """An inference rule (or a node of a derivation tree): premises above a line, the conclusion below, the rule's
    name to the right of the line.  Premises may themselves be rules."""
    p = VGroup(*prems).arrange(RIGHT, buff=buff, aligned_edge=DOWN) if prems else VGroup()
    w = max(p.width if prems else 0.0, concl.width) + 0.25
    line = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=2, color=color)
    if not bar:
        line.set_opacity(0)
    concl.next_to(line, DOWN, buff=0.12)
    if prems:
        p.next_to(line, UP, buff=0.12)
    anchor = line if bar else concl
    nm = label(name, font_size=fs, color=name_color).next_to(anchor, RIGHT, buff=0.12) if name else VectorizedPoint(
        line.get_right())
    g = VGroup(p, line, concl, nm)
    g.prem, g.line, g.concl, g.name = p, line, concl, nm
    return g


def levels(t, d=0, out=None):
    """The parts of a derivation tree by depth, the conclusion first, for growing it upward."""
    out = {} if out is None else out
    out.setdefault(d, []).extend([t.concl, t.line, t.name])
    for q in t.prem:
        if hasattr(q, "line"):
            levels(q, d + 1, out)
        else:
            out.setdefault(d + 1, []).append(q)
    return [VGroup(*out[k]) for k in sorted(out)]


def M(s, fs=28, color=WHITE):
    return MathTex(s, font_size=fs, color=color)


class Operational(VoiceoverScene):
    def construct(self):
        self.card()
        self.language()
        self.rules()
        self.one_step()
        self.run()
        self.big_step()
        self.cek()

    def card(self):
        card = chapter_card(1, r"Meaning as steps", r"What does a machine do with a program?", lit=(1981, 1987),
                            extra=((1981, r"Plotkin: \ structural operational semantics"),
                                   (1986, r"Felleisen and Friedman: \ the CEK machine"),
                                   (1987, r"Kahn: \ natural semantics")), part=PART)
        with self.voiceover("Chapter one. Meaning as steps. What does a machine do with a program?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def language(self):
        head = label(r"A small language with recursion", font_size=36).to_edge(UP, buff=0.3)
        g = VGroup(
            M(r"e \;::=\; n \;\mid\; b \;\mid\; x", 40),
            M(r"\mid\; \mathsf{fun}\ x \to e \;\mid\; e_1\ e_2", 40),
            M(r"\mid\; \mathsf{if}\ e_0\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2 \;\mid\; e_1 \oplus e_2"
              r"\quad (\oplus \in \{+,\,-,\,\times,\,<,\,=\})", 40),
            M(r"\mid\; \mathsf{fix}\ f\ x \to e", 40, HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for r in g[1:]:
            r.shift(RIGHT * 0.75)
        fixnote = label(r"a function named $f$, \ of argument $x$, \ whose body may call $f$", font_size=23,
                        color=HEAD)
        vals = M(r"v \;::=\; n \;\mid\; b \;\mid\; \mathsf{fun}\ x \to e \;\mid\; \mathsf{fix}\ f\ x \to e", 40, YES)
        valnote = label(r"values: \ the finished terms, \ what a program is trying to become", font_size=23,
                        color=YES)
        block = VGroup(g, fixnote, vals, valnote).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        fixnote.shift(RIGHT * 0.75)
        valnote.shift(RIGHT * 0.75)
        block.next_to(head, DOWN, buff=0.45)
        prog = VGroup(
            label(r"factorial, \ the program this part follows", font_size=20, color=GREY_B),
            mono("fix fact n -> if n = 0 then 1 else n * fact (n - 1)", size=22, color=WHITE),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        frame = SurroundingRectangle(prog, buff=0.18, corner_radius=0.1, color=GREY_D, stroke_width=1.5)
        with self.voiceover(
            "We need a language small enough to reason about and large enough to be interesting. "
            "<bookmark mark='a'/> Its terms are integers and booleans, variables, functions and their applications, "
            "conditionals and arithmetic, <bookmark mark='b'/> and one construct for recursion: fix f x arrow e is "
            "a function named f, of argument x, whose body may call f itself. <bookmark mark='c'/> Some terms are "
            "finished: numbers, booleans and functions. These are the values, and a program's whole job is to "
            "become one. <bookmark mark='d'/> Here is factorial, written with fix. We follow it through this whole "
            "part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in g[:3]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(g[3]), FadeIn(fixnote))
            vo.wait_until("c")
            self.play(FadeIn(vals), FadeIn(valnote))
            vo.wait_until("d")
            self.play(FadeIn(prog), Create(frame))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        head = label(r"Small steps: \ $e \to e'$ \ \ (Plotkin, \ 1981)", font_size=36).to_edge(UP, buff=0.3)
        fs = 31
        search = VGroup(
            rule([M(r"e_1 \to e_1'", fs)], M(r"e_1 \oplus e_2 \to e_1' \oplus e_2", fs), r"\textsc{Op-L}"),
            rule([M(r"e_2 \to e_2'", fs)], M(r"v_1 \oplus e_2 \to v_1 \oplus e_2'", fs), r"\textsc{Op-R}"),
            rule([M(r"e_1 \to e_1'", fs)], M(r"e_1\ e_2 \to e_1'\ e_2", fs), r"\textsc{App-L}"),
            rule([M(r"e_2 \to e_2'", fs)], M(r"v_1\ e_2 \to v_1\ e_2'", fs), r"\textsc{App-R}"),
        ).arrange(RIGHT, buff=0.5)
        for r in search:
            r.line.set_color(KERN)
        st = label(r"search rules: \ where to look", font_size=24, color=KERN)
        red = VGroup(
            rule([], M(r"n_1 \oplus n_2 \to n \quad (n = n_1 \oplus n_2)", fs), r"\textsc{Op}", bar=False),
            rule([], M(r"\mathsf{if}\ \mathsf{true}\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2 \to e_1", fs),
                 r"\textsc{If-T}", bar=False),
            rule([], M(r"\mathsf{if}\ \mathsf{false}\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2 \to e_2", fs),
                 r"\textsc{If-F}", bar=False),
            rule([], M(r"(\mathsf{fun}\ x \to e)\ v \to e[v/x]", fs), r"\textsc{Beta}", bar=False),
            rule([], M(r"(\mathsf{fix}\ f\ x \to e)\ v \to e[\,\mathsf{fix}\ f\ x \to e\,/\,f,\ \ v/x\,]", fs,
                       HEAD), r"\textsc{Fix}", bar=False),
        )
        left = VGroup(*red[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(*red[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        redg = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        rt = label(r"reduction rules: \ what to do", font_size=24, color=HEAD)
        for grp in (search, redg):
            if grp.width > 13.4:
                grp.scale_to_fit_width(13.4)
        top = VGroup(st, search).arrange(DOWN, buff=0.35)
        bot = VGroup(rt, redg).arrange(DOWN, buff=0.35)
        VGroup(top, bot).arrange(DOWN, buff=0.75).next_to(head, DOWN, buff=0.5)
        foot = note(r"call by value, \ left to right; \ one more search rule steps the condition of an \ "
                    r"\textsf{if}", font_size=18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Gordon Plotkin's structural operational semantics, from his Aarhus lecture notes of nineteen eighty-one,"
            " defines one step of computation by rules: above the line, what must hold; below it, what follows. "
            "<bookmark mark='a'/> Search rules say where to look. To step an arithmetic term, step its left side; "
            "once that is a value, step the right. That is call by value, left to right, made explicit. <bookmark "
            "mark='b'/> Reduction rules say what to do when the search finds something ready. Two numbers become "
            "their sum or product; a conditional on true becomes its first branch; a function applied to a value "
            "becomes its body, with the value substituted for the parameter. <bookmark mark='c'/> And fix unrolls "
            "itself: the body receives the value for x, and the whole function for f."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(st), LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in search], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(r) for r in red[:4]], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(red[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def one_step(self):
        f = load("fact")
        tr = [short(s) for s in f["trace"]]
        a, b = tr[3], tr[4]
        head = label(r"One step is a theorem", font_size=36).to_edge(UP, buff=0.3)
        i = a.index("(3 - 1)")
        before = term(a, size=22, color=WHITE, hi=(i, i + 7))
        p, q = changed(a, b)
        after = term(b, size=22, color=WHITE, hi=(p, q))
        arrow = MathTex(r"\to", font_size=34)
        pair = VGroup(before, arrow, after).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.4)
        src = note(r"terms 4 and 5 of our interpreter's trace of \ \texttt{fact 3} \ (\texttt{fact} abbreviates the "
                   r"\texttt{fix})", font_size=17).next_to(pair, DOWN, buff=0.15)
        fs = 36
        leaf = rule([], M(r"3 - 1 \to 2", fs, HEAD), r"\textsc{Op}")
        mid = rule([leaf], M(r"\mathit{fact}\ (3 - 1) \to \mathit{fact}\ 2", fs), r"\textsc{App-R}")
        root = rule([mid], M(r"3 \times \mathit{fact}\ (3 - 1) \to 3 \times \mathit{fact}\ 2", fs), r"\textsc{Op-R}")
        side = VGroup(
            label(r"$\mathit{fact}$ is a value, \ so \textsc{App-R} may step the argument", font_size=21,
                  color=GREY_A),
            label(r"$3$ is a value, \ so \textsc{Op-R} may step the right side", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(root, side).arrange(RIGHT, buff=0.7).next_to(src, DOWN, buff=0.7)
        thm = VGroup(
            label(r"\textbf{Determinism}", font_size=24, color=YES),
            MathTex(r"e \to e_1", r"\ \text{ and }\ ", r"e \to e_2", r"\ \implies\ ", r"e_1 = e_2", font_size=32,
                    color=YES),
        ).arrange(RIGHT, buff=0.4)
        pf = wrapped_label(r"proof: \ induction on the derivation of $e \to e_1$. \ Values never step, \ and every "
                           r"search rule needs everything to its left to be a value, \ so at most one rule fits any "
                           r"term.", 12.4, font_size=19, color=GREY_A)
        VGroup(thm, pf).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        mid_y = (src.get_bottom()[1] + thm.get_top()[1]) / 2
        VGroup(root, side).set_y(mid_y)
        lv = levels(root)
        with self.voiceover(
            "Each step is a small theorem, with a proof tree. <bookmark mark='a'/> Here is the step our interpreter "
            "takes from the fourth term of factorial's trace to the fifth: three times fact of three minus one "
            "becomes three times fact of two. <bookmark mark='b'/> Read the tree from the bottom. Three is a value, "
            "so the product may step its right side. Fact is a value, so the application may step its argument. And "
            "three minus one steps to two, by arithmetic. <bookmark mark='c'/> A first theorem: if a term steps to e "
            "one and to e two, then they are equal. The language is deterministic. The proof is an induction on the "
            "derivation: values never step, and every search rule needs everything to its left to be a value, so at "
            "most one rule ever fits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(before), FadeIn(src))
            self.play(FadeIn(arrow), FadeIn(after, shift=RIGHT * 0.2))
            vo.wait_until("b")
            for k, part in enumerate(lv):
                self.play(FadeIn(part, shift=UP * 0.15), *([FadeIn(side[1])] if k == 0 else
                                                          [FadeIn(side[0])] if k == 1 else []), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(thm), FadeIn(pf))
        self.wait(0.4)
        self.clear_scene()

    def run(self):
        f = load("fact")
        tr = [short(s) for s in f["trace"]]
        head = label(r"A run: \ \texttt{fact 3}, \ step by step", font_size=36).to_edge(UP, buff=0.3)
        W = 12.8

        def show(k):
            hi = changed(tr[k - 1], tr[k]) if k else None
            t = term(tr[k], size=24, color=WHITE, hi=hi)
            if t.width > W:
                t.scale_to_fit_width(W)
            return t.move_to([0, 2.05, 0])

        counter = [label(rf"step {k} of {f['steps']}", font_size=22, color=HEAD).move_to([0, 1.3, 0])
                   for k in range(len(tr))]
        lens = [len(s) for s in tr]
        n = len(tr)
        bw, gap, H = 0.42, 0.18, 2.9
        x0 = -(n * (bw + gap) - gap) / 2 + bw / 2
        base_y = -2.55
        bars = VGroup()
        for k, L in enumerate(lens):
            h = H * L / max(lens)
            r = Rectangle(width=bw, height=h, stroke_width=0, fill_color=DATA if k < n - 1 else YES,
                          fill_opacity=0.85)
            r.move_to([x0 + k * (bw + gap), base_y + h / 2, 0])
            bars.add(r)
        axis = Line([x0 - 0.4, base_y, 0], [-x0 + 0.4, base_y, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[label(f"{k}", font_size=16, color=GREY_B).next_to(bars[k], DOWN, buff=0.12).set_y(
            base_y - 0.2) for k in range(0, n, 3)])
        cap = note(r"length of the printed term at each step \ (characters, \ \texttt{fact} abbreviated): \ the "
                   r"pending multiplications pile up, \ then collapse", font_size=17).to_edge(DOWN, buff=0.3)
        cur = show(0)
        cnt = counter[0]
        with self.voiceover(
            "<bookmark mark='a'/> Here is factorial of three, from our "
            "small-step interpreter, one step at a time, with each step's new piece in yellow. "
            "<bookmark mark='b'/> Watch the length of the term. It grows as multiplications pile up, each waiting "
            "for its right-hand side: three times, two times, one times. Those pending operations are the call "
            "stack of Part 11, written into the term itself. <bookmark mark='c'/> At the base case the term "
            f"collapses, and after {f['steps']} steps it is the value {f['value']}. Because the language is "
            "deterministic, a run is a line, not a tree, and the value at its end, if there is one, is what the "
            "program means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cur), FadeIn(cnt), Create(axis), FadeIn(ticks), FadeIn(cap))
            self.play(GrowFromEdge(bars[0], DOWN))
            vo.wait_until("a")
            for k in range(1, n):
                if k == 6:
                    vo.wait_until("b")
                if k == 13:
                    vo.wait_until("c")
                nxt = show(k)
                self.play(ReplacementTransform(cur, nxt), ReplacementTransform(cnt, counter[k]),
                          GrowFromEdge(bars[k], DOWN), run_time=0.6)
                cur, cnt = nxt, counter[k]
            self.play(Indicate(cur, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def big_step(self):
        a = load("agree")
        head = label(r"Big steps: \ $e \Downarrow v$ \ \ (Kahn, \ 1987)", font_size=36).to_edge(UP, buff=0.3)
        fs = 29
        rs = VGroup(
            rule([], M(r"v \Downarrow v", fs), r"\textsc{Val}"),
            rule([M(r"e_1 \Downarrow n_1", fs), M(r"e_2 \Downarrow n_2", fs)],
                 M(r"e_1 \oplus e_2 \Downarrow n_1 \oplus n_2", fs), r"\textsc{Op}", buff=0.35),
            rule([M(r"e_1 \Downarrow \mathsf{fun}\ x \to e", fs), M(r"e_2 \Downarrow v_2", fs),
                  M(r"e[v_2/x] \Downarrow v", fs)], M(r"e_1\ e_2 \Downarrow v", fs), r"\textsc{App}", buff=0.35),
        ).arrange(RIGHT, buff=0.7, aligned_edge=DOWN).next_to(head, DOWN, buff=0.45)
        fs2 = 29
        sq = r"(\mathsf{fun}\ x \to x \times x)"
        t1 = rule([], M(r"\mathsf{fun}\ x \to x \times x \Downarrow \mathsf{fun}\ x \to x \times x", fs2),
                  r"\textsc{Val}")
        t2 = rule([rule([], M(r"1 \Downarrow 1", fs2)), rule([], M(r"2 \Downarrow 2", fs2))],
                  M(r"1 + 2 \Downarrow 3", fs2, DATA), r"\textsc{Op}", buff=0.3)
        t3 = rule([rule([], M(r"3 \Downarrow 3", fs2)), rule([], M(r"3 \Downarrow 3", fs2))],
                  M(r"3 \times 3 \Downarrow 9", fs2), r"\textsc{Op}", buff=0.3)
        tree = rule([t1, t2, t3], M(sq + r"\ (1 + 2) \Downarrow 9", 34, YES), r"\textsc{App}", buff=0.45)
        if tree.width > 12.4:
            tree.scale_to_fit_width(12.4)
        tree.next_to(rs, DOWN, buff=0.8)
        ill = note(r"illustrative program", font_size=16).next_to(tree, DOWN, buff=0.12).align_to(tree, RIGHT)
        thm = VGroup(
            MathTex(r"e \Downarrow v", r"\iff", r"e \to^{*} v", font_size=34, color=WHITE),
            label(rf"our big-step evaluator \ (environments in place of substitution) \ and small-step interpreter "
                  rf"agree on {a['agree']} of {a['n']} random programs", font_size=19, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        lv = levels(tree)
        with self.voiceover(
            "Small steps answer the question: what happens next? Sometimes we only want the answer. <bookmark "
            "mark='a'/> Gilles Kahn's natural semantics, from nineteen eighty-seven, relates a term directly to its "
            "value: e evaluates to v. A value evaluates to itself; an arithmetic term evaluates both sides and "
            "combines them; an application evaluates the function, then the argument, then the body with the argument"
            " substituted. <bookmark mark='b'/> Now the proof tree is the whole computation. Squaring, applied to one"
            " plus two: the function is a value, the argument evaluates to three, and the body, three times three, to"
            " nine. <bookmark mark='c'/> The two semantics agree: e evaluates to v exactly when e reaches v in small "
            "steps. Our big-step evaluator uses environments instead of substitution, and it agrees with the small-"
            f"step interpreter on all {a['n']} random programs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in rs], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            for part in lv:
                self.play(FadeIn(part, shift=UP * 0.15), run_time=0.9)
            self.play(FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.wait(0.4)
        self.clear_scene()

    def cek(self):
        a = load("agree")
        head = label(r"The CEK machine \ (Felleisen and Friedman, \ 1986)", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            ["(fun x -> x + 1) 2", "{}", "[]"],
            ["fun x -> x + 1", "{}", "[arg 2]"],
            ["<closure x>", "{}", "[arg 2]"],
            ["2", "{}", "[call <closure>]"],
            ["2", "{}", "[call <closure>]"],
            ["x + 1", "{x: 2}", "[]"],
            ["x", "{x: 2}", "[_ + 1]"],
            ["2", "{x: 2}", "[_ + 1]"],
            ["1", "{x: 2}", "[2 + _]"],
            ["1", "{x: 2}", "[2 + _]"],
            ["3", "{x: 2}", "[]"],
        ]
        is_val = [False, False, True, False, True, False, False, True, False, True, True]
        tab = grid_table([r"C \ (control)", r"E \ (environment)", r"K \ (continuation)"], rows,
                         widths=[2.9, 2.0, 2.6], row_h=0.37, font_size=19, mono_cols=(0, 1, 2))
        for r, v in enumerate(is_val, start=1):
            tab.cells[r][0].set_color(YES if v else WHITE)
            tab.cells[r][2].set_color(KERN)
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.45)
        ill = note(r"an illustrative run; \ green: \ a value in the control register", font_size=16).next_to(
            tab, DOWN, buff=0.15).align_to(tab, LEFT)
        regs = VGroup(
            wrapped_label(r"\textbf{C}: \ the term being worked on, \ or the value just found", 4.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"\textbf{E}: \ the environment, \ variables to values", 4.6, font_size=19, color=DATA),
            wrapped_label(r"\textbf{K}: \ the continuation, \ a stack of frames saying what to do with the next "
                          r"value \ (the call stack of Part 15)", 4.6, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        regs.next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        ms, mc = a["mean_small_steps"], a["mean_cek_steps"]
        L = 2.9
        b1 = Rectangle(width=L * ms / mc, height=0.32, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
        b2 = Rectangle(width=L, height=0.32, stroke_width=0, fill_color=KERN, fill_opacity=0.85)
        n1 = label(r"small steps", font_size=18, color=GREY_A)
        n2 = label(r"CEK transitions", font_size=18, color=GREY_A)
        v1 = label(f"{ms:.1f}", font_size=18, color=DATA)
        v2 = label(f"{mc:.1f}", font_size=18, color=KERN)
        n2.next_to(n1, DOWN, buff=0.22, aligned_edge=LEFT)
        bx = max(n1.get_right()[0], n2.get_right()[0]) + 0.2
        for nm, b, v in ((n1, b1, v1), (n2, b2, v2)):
            b.move_to([bx + b.width / 2, nm.get_y(), 0])
            v.next_to(b, RIGHT, buff=0.12)
        r1, r2 = VGroup(n1, b1, v1), VGroup(n2, b2, v2)
        chart = VGroup(label(rf"mean per program, \ {a['n']} random programs", font_size=18, color=GREY_B),
                       VGroup(r1, r2)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        chart.next_to(regs, DOWN, buff=0.45).align_to(regs, LEFT)
        why = wrapped_label(r"each transition does constant work; \ a small step searches and copies the whole term",
                            4.6, font_size=19, color=GREY_A).next_to(chart, DOWN, buff=0.25).align_to(regs, LEFT)
        right = VGroup(regs, chart, why)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        with self.voiceover(
            "Neither semantics is how a real interpreter runs. <bookmark mark='a'/> Matthias Felleisen and Daniel "
            "Friedman's CEK machine, from nineteen eighty-six, keeps three registers: a control term, an environment "
            "for the variables, and a continuation, a stack of frames saying what to do with the next value. "
            "<bookmark mark='b'/> Here it runs a function applied to two. It remembers the argument in a frame, "
            "evaluates the function to a closure, then the argument, binds x to two, and works through x plus one "
            "with two more frames. <bookmark mark='c'/> Each transition does constant work, so it takes more of them:"
            " about two hundred and ninety-four per program on average, against seventy-three small steps. But each "
            "small step searches and copies the whole term. <bookmark mark='d'/> This is the interpreter loop of Part"
            " 15, derived from the rules."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0], tab.rule)), LaggedStart(*[FadeIn(r) for r in regs],
                                                                          lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.35), FadeIn(ill),
                      run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(chart[0]), FadeIn(n1), FadeIn(n2), GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT),
                      FadeIn(v1), FadeIn(v2))
            self.play(FadeIn(why))
            vo.wait_until("d")
            self.play(Indicate(tab.cells[-1][0], color=YES))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO)
