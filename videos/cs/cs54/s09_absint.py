from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono


def iv(b) -> str:
    """An interval bound from the analyser's JSON ('-inf', '+inf' or an integer) as LaTeX."""
    return {"-inf": r"-\infty", "+inf": r"+\infty"}.get(b, str(b)) if isinstance(b, str) else f"{b}"


def ivl(pair) -> str:
    return rf"[{iv(pair[0])}, {iv(pair[1])}]"


def plane(i_max=12, j_max=24, w=4.6, h=4.2):
    """Axes for the (i, j) plane of the two-counter loop, with a few tick labels."""
    ax = Axes(x_range=[0, i_max, 2], y_range=[0, j_max, 4], x_length=w, y_length=h,
              axis_config={"color": GREY_C, "include_ticks": True, "tip_length": 0.15})
    lx = MathTex("i", font_size=26, color=GREY_A).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
    ly = MathTex("j", font_size=26, color=GREY_A).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
    ticks = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                     for v in range(0, i_max + 1, 4)],
                   *[MathTex(str(v), font_size=18, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                     for v in range(4, j_max + 1, 4)])
    g = VGroup(ax, lx, ly, ticks)
    g.ax = ax
    return g


def box(ax, i0, i1, j0, j1, color, opacity=0.15, width=2.5):
    lo, hi = ax.c2p(i0, j0), ax.c2p(i1, j1)
    r = Rectangle(width=max(hi[0] - lo[0], 0.02), height=max(hi[1] - lo[1], 0.02), stroke_color=color,
                  stroke_width=width, fill_color=color, fill_opacity=opacity)
    return r.move_to((lo + hi) / 2)


class Absint(VoiceoverScene):
    def construct(self):
        self.card()
        self.approx()
        self.lattice()
        self.kleene()
        self.widening()
        self.relational()
        self.domains()

    def card(self):
        card = chapter_card(8, r"Abstract interpretation", r"Can a proof be computed by approximation?",
                            lit=(1977, 2003), extra=((1977, r"Cousot and Cousot"),
                                                     (2003, r"Astr\'ee: \ the Airbus A340")), part=PART)
        with self.voiceover("Chapter eight. Abstract interpretation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def approx(self):
        gap = load("absint")["gap"]
        pts = gap["reachable"]
        head = label(r"Sound approximation", font_size=36).to_edge(UP, buff=0.3)
        P = plane().move_to([-3.4, -0.35, 0])
        ax = P.ax
        dots = VGroup(*[Dot(ax.c2p(i, j), radius=0.06, color=WHITE) for i, j in pts])
        i0, i1 = min(p[0] for p in pts), max(p[0] for p in pts)
        j0, j1 = min(p[1] for p in pts), max(p[1] for p in pts)
        best = box(ax, i0, i1, j0, j1, HEAD)
        bad = Rectangle(width=ax.c2p(12, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 24)[1] - ax.c2p(0, j1 + 0.6)[1],
                        stroke_width=0, fill_color=NO, fill_opacity=0.22).move_to(
            (ax.c2p(0, j1 + 0.6) + ax.c2p(12, 24)) / 2)
        badl = label(rf"bad: \ $j > {j1}$", font_size=18, color=NO).move_to(ax.c2p(9.5, 22.5))
        coarse = box(ax, i0, i1, j0, 24, LAM, opacity=0.1)
        coarse_t = Triangle(color=LAM, fill_opacity=1).scale(0.1).move_to(ax.c2p((i0 + i1) / 2, 24) + UP * 0.08)
        notes = VGroup(
            wrapped_label(rf"the states at the loop's head: \ {len(pts)} points on a line \ (white)", 5.6,
                          font_size=20, color=WHITE),
            wrapped_label(rf"compute instead with a coarser kind of set, \ here a box: \ $i \in [{i0}, {i1}]$, "
                          rf"$j \in [{j0}, {j1}]$", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{sound}: \ the box contains every real state, \ so if the box misses the bad "
                          r"states, \ so does the program: \ proved", 5.6, font_size=20, color=YES),
            wrapped_label(r"a coarser box that touches them gives an \textbf{alarm}, \ which may be false: \ the "
                          r"price of always terminating \ (Rice, \ Part 25)", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The third way around Rice's theorem is to approximate soundly, a theory Patrick and Radhia Cousot set "
            "out in 1977. <bookmark mark='a'/> A loop with two counters reaches eleven states at its head, all on a "
            "line. <bookmark mark='b'/> Instead of exact sets, compute with simpler ones: here a box, one range per "
            "variable. <bookmark mark='c'/> The box contains every real state, so if it misses the bad states, so "
            "does the program: a proof. <bookmark mark='d'/> A coarser box may touch the bad region and raise an "
            "alarm, though no real state is bad. A sound analysis never misses a bug; the price is false alarms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(P))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(best), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(bad), FadeIn(badl), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Create(coarse), FadeIn(coarse_t), FadeIn(notes[3]))
            self.play(Indicate(bad, color=NO, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def lattice(self):
        head = label(r"The interval lattice", font_size=36).to_edge(UP, buff=0.3)
        pos = {"bot": (-3.6, -2.6), "00": (-5.2, -1.5), "11": (-3.6, -1.5), "22": (-2.0, -1.5), "01": (-4.4, -0.4),
               "12": (-2.8, -0.4), "02": (-3.6, 0.7), "top": (-3.6, 2.2)}
        tex = {"bot": r"\bot", "00": "[0, 0]", "11": "[1, 1]", "22": "[2, 2]", "01": "[0, 1]", "12": "[1, 2]",
               "02": "[0, 2]", "top": r"[-\infty, +\infty]"}
        nodes = {k: MathTex(t, font_size=28).move_to([*pos[k], 0]) for k, t in tex.items()}
        links = [("bot", "00"), ("bot", "11"), ("bot", "22"), ("00", "01"), ("11", "01"), ("11", "12"),
                 ("22", "12"), ("01", "02"), ("12", "02")]
        lines = VGroup(*[Line(nodes[a].get_top(), nodes[b].get_bottom(), buff=0.08, color=GREY_C, stroke_width=1.6)
                         for a, b in links])
        up = DashedLine(nodes["02"].get_top(), nodes["top"].get_bottom(), buff=0.12, color=GREY_C, stroke_width=1.6)
        upl = label(r"\dots \ infinitely many", font_size=17, color=GREY_B).next_to(up, RIGHT, buff=0.15)
        join = MathTex(r"[0, 0] \sqcup [2, 2] = [0, 2]", font_size=30, color=HEAD).to_corner(DL, buff=0.5)
        join.shift(RIGHT * 0.3)
        joinl = label(r"join: \ the hull, \ which also contains 1", font_size=18, color=HEAD).next_to(join, RIGHT,
                                                                                                    buff=0.3)
        gal = VGroup(
            MathTex(r"\alpha(S)", r"=", r"[\min S, \max S]", font_size=32),
            MathTex(r"\gamma([a, b])", r"=", r"\{x : a \le x \le b\}", font_size=32),
            MathTex(r"\alpha(S) \sqsubseteq I", r"\iff", r"S \subseteq \gamma(I)", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.3)
        for e in gal:
            e.shift(RIGHT * (gal[0][1].get_x() - e[1].get_x()))
        whys = VGroup(label(r"abstraction: \ the smallest interval holding $S$", font_size=17, color=GREY_A),
                      label(r"concretization: \ the numbers an interval means", font_size=17, color=GREY_A),
                      label(r"a \textbf{Galois connection}: \ $\alpha(S)$ is the best interval for $S$", font_size=17,
                            color=YES))
        for w, e in zip(whys, gal):
            w.next_to(e, DOWN, buff=0.06)
        right = VGroup(*[VGroup(e, w) for e, w in zip(gal, whys)]).arrange(DOWN, buff=0.22).move_to([3.4, 1.2, 0])
        ex = MathTex(r"S = \{1, 4, 6\}", r"\;\mapsto\;", r"[1, 6]", r"\;\mapsto\;", r"\{1, 2, \dots, 6\} \supseteq S",
                     font_size=30).next_to(right, DOWN, buff=0.35)
        exl = label(r"illustrative: \ sound, \ but 2, \ 3 and 5 came along", font_size=17, color=GREY_B).next_to(
            ex, DOWN, buff=0.1)
        chain = MathTex(r"[0, 0] \sqsubseteq [0, 1] \sqsubseteq [0, 2] \sqsubseteq \cdots", font_size=30,
                        color=NO).next_to(exl, DOWN, buff=0.35)
        chl = label(r"chains that climb for ever: \ iteration need not stop", font_size=17, color=NO).next_to(
            chain, DOWN, buff=0.1)
        with self.voiceover(
            "For one variable the simpler sets are intervals, and they form a lattice. <bookmark mark='a'/> At the "
            "bottom, the empty interval, for unreachable code; at the top, all integers; each interval sits below "
            "those that contain it. <bookmark mark='b'/> Where two branches meet, intervals are joined by taking "
            "their hull, which picks up values neither branch had. <bookmark mark='c'/> Abstraction maps a set to the"
            " smallest interval holding it; concretization maps an interval back to its numbers. Together they form a"
            " Galois connection: the abstraction is the best interval possible, yet it still gains numbers. <bookmark"
            " mark='d'/> And the lattice has chains that climb for ever."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes["bot"]), FadeIn(nodes["top"]))
            self.play(LaggedStart(*[FadeIn(nodes[k]) for k in ("00", "11", "22", "01", "12", "02")], lag_ratio=0.2),
                      Create(lines), Create(up), FadeIn(upl), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(nodes["00"], color=HEAD), Indicate(nodes["22"], color=HEAD))
            self.play(nodes["02"].animate.set_color(HEAD), FadeIn(join), FadeIn(joinl))
            vo.wait_until("c")
            for e, w in zip(gal, whys):
                self.play(FadeIn(e), FadeIn(w), run_time=0.8)
            self.play(FadeIn(ex), FadeIn(exl))
            vo.wait_until("d")
            self.play(FadeIn(chain), FadeIn(chl))
        self.wait(0.4)
        self.clear_scene()

    def kleene(self):
        ex = load("absint")["examples"]["counter_no_widen"]
        lp = ex["loops"][0]
        head = label(r"Iterating to an invariant", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["    " * (p["code"].startswith("x = x")) + p["code"] for p in ex["points"]], size=22)
        code.move_to([-4.6, 1.6, 0])
        eqs = VGroup(
            MathTex(r"X", r"=", r"[0, 0] \sqcup \big((X \sqcap [-\infty, 99]) + 1\big)", font_size=32),
            MathTex(r"X_{k+1}", r"=", r"[0, 0] \sqcup \big((X_k \sqcap [-\infty, 99]) + 1\big)", font_size=32),
            MathTex(r"X_0 = [0, 0],\ X_1 = [0, 1],\ X_2 = [0, 2],\ \dots", font_size=32),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([2.5, 1.65, 0])
        whys = VGroup(label(r"the loop head: \ entry, \ or one more pass of the body", font_size=17, color=GREY_A),
                      label(r"solve by iterating from the entry state", font_size=17, color=GREY_A),
                      label(r"each pass adds one", font_size=17, color=GREY_A))
        for w, e in zip(whys, eqs):
            w.next_to(e, RIGHT, buff=0.25)
            if w.get_right()[0] > 6.85:
                w.next_to(e, DOWN, buff=0.05).align_to(e, LEFT)
        rows = VGroup(*[VGroup(e, w) for e, w in zip(eqs, whys)]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        rows.move_to([2.4, 1.6, 0])
        x0, x1, y = -5.8, 5.8, -1.2
        nl = NumberLine(x_range=[0, 100, 10], length=x1 - x0, color=GREY_C, include_numbers=False).move_to(
            [(x0 + x1) / 2, y, 0])
        nums = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.12)
                        for v in range(0, 101, 20)])
        hi = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(width=max(nl.n2p(hi.get_value())[0] - nl.n2p(0)[0], 0.06), height=0.3,
                                              stroke_width=0, fill_color=HEAD, fill_opacity=0.8).move_to(
            nl.n2p(hi.get_value() / 2) + UP * 0.32))
        cnt = always_redraw(lambda: MathTex(rf"k = {int(round(hi.get_value()))}:\ \ X_k = [0, "
                                            rf"{int(round(hi.get_value()))}]", font_size=30, color=HEAD).move_to(
            [0, y + 1.05, 0]))
        done = label(rf"stable after {lp['ascending']} rounds: \ $X = {ivl(lp['head']['x'])}$", font_size=21,
                     color=YES).next_to(nl, DOWN, buff=0.6)
        exit_ = next(p for p in ex["points"] if p["code"].startswith("assert"))
        ok = ex["asserts"][0]["proved"]
        assert ok and lp["ascending"] == 101
        ex_t = MathTex(r"X \sqcap [100, +\infty]", r"=", ivl(exit_["state"]["x"]), font_size=32,
                       color=YES).next_to(done, DOWN, buff=0.3)
        ex_l = label(r"at the exit: \ the assertion is proved", font_size=19, color=YES).next_to(ex_t, RIGHT,
                                                                                                 buff=0.35)
        with self.voiceover(
            "What holds at a loop's head? <bookmark mark='a'/> Here x counts from zero to a hundred. At the head, x "
            "is zero on entry, or one more than a value that passed the test: an equation over intervals. <bookmark "
            "mark='b'/> Solve it by iterating from the entry state. <bookmark mark='c'/> Each round the interval "
            "grows by one: zero to zero, zero to one, zero to two. <bookmark mark='d'/> After one hundred and one "
            "rounds it stops changing. At the exit, the failed test leaves exactly a hundred, and the assertion is "
            "proved. A loop to two billion would take two billion rounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(whys[2]), FadeIn(nl), FadeIn(nums), FadeIn(bar), FadeIn(cnt))
            self.play(hi.animate.set_value(100), run_time=5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(done))
            self.play(FadeIn(ex_t), FadeIn(ex_l))
        self.wait(0.4)
        self.clear_scene()

    def widening(self):
        E = load("absint")["examples"]
        tr = E["counter_widen"]["trace"]
        head = label(r"Widening: \ jump, \ then narrow", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"[a, b] \,\nabla\, [c, d]", r"=", r"\big[\ c < a\ ?\ -\infty : a,\ \ d > b\ ?\ +\infty : "
                       r"b\ \big]", font_size=32).next_to(head, DOWN, buff=0.3)
        rl = label(r"a bound that moved is sent to infinity; \ a stable bound stays", font_size=18,
                   color=GREY_A).next_to(rule, DOWN, buff=0.1)
        x0, x1, y = -5.6, 4.6, 0.2
        nl = NumberLine(x_range=[0, 100, 10], length=x1 - x0, color=GREY_C, include_numbers=False).move_to(
            [(x0 + x1) / 2, y, 0])
        inf = VGroup(DashedLine(nl.n2p(100), nl.n2p(100) + RIGHT * 1.6, color=GREY_C, stroke_width=2),
                     MathTex(r"+\infty", font_size=26, color=GREY_B).next_to(nl.n2p(100) + RIGHT * 1.6, RIGHT,
                                                                           buff=0.1))
        nums = VGroup(*[MathTex(str(v), font_size=18, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.12)
                        for v in range(0, 101, 20)])

        def bar_to(xr, color):
            return Rectangle(width=max(xr - nl.n2p(0)[0], 0.06), height=0.3, stroke_width=0, fill_color=color,
                             fill_opacity=0.8).move_to([(nl.n2p(0)[0] + xr) / 2, y + 0.32, 0])

        def end_x(b):
            return nl.n2p(100)[0] + 1.6 if b == "+inf" else nl.n2p(b)[0]
        steps = [t for t in tr if t["phase"] != "entry"]
        bar = bar_to(end_x(0), HEAD)
        txt = MathTex(r"X_0 = [0, 0]", font_size=30, color=HEAD).move_to([0, y + 1.0, 0])
        assert [t["phase"] for t in steps] == ["ascending", "ascending", "narrowing", "narrowing"]
        captions = []
        for t in steps:
            k = t["iteration"]
            h = t["head"]["x"]
            if t["phase"] == "ascending":
                c = rf"X_{k} = X_{k - 1} \,\nabla\, {ivl(t['computed']['x'])} = {ivl(h)}"
            else:
                c = rf"X_{k} = X_{k - 1} \,\Delta\, F(X_{k - 1}) = {ivl(h)}"
            captions.append((MathTex(c, font_size=30, color=YES if t["phase"] == "narrowing" else HEAD).move_to(
                [0, y + 1.0, 0]), end_x(h[1]), YES if t["phase"] == "narrowing" else HEAD))
        rows, colors = [], []
        names = {"counter": r"$x$ counts to 100", "bounded": r"$i$ counts to an input $n \le 50$",
                 "two": r"$i$ counts to 10, \ $j$ goes up by 2"}
        for key, nm in names.items():
            a, b = E[f"{key}_no_widen"]["loops"][0], E[f"{key}_widen"]["loops"][0]
            plain = f"{a['ascending']}" if a["converged_without_widening"] else r"never stops"
            proved = E[f"{key}_widen"]["asserts"][0]["proved"]
            rows.append([nm, plain, f"{b['ascending']} + {b['narrowing']}", r"yes" if proved else r"no"])
            colors.append([WHITE, NO if not a["converged_without_widening"] else GREY_A, YES, YES if proved else NO])
        tab = grid_table([r"loop", r"plain rounds", r"widen + narrow", r"assertion proved"], rows,
                         widths=[4.6, 2.0, 2.2, 2.4], row_h=0.45, font_size=19, colors=colors, mono_cols=())
        tab.to_edge(DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Widening, also from the Cousots, forces the iteration to finish. <bookmark mark='a'/> A bound that has "
            "not moved stays; a bound that moved jumps straight to infinity. <bookmark mark='b'/> The first round "
            "moves x's upper bound from zero to one, so it jumps to infinity. <bookmark mark='c'/> The next round "
            "computes zero to a hundred, which fits inside: a fixpoint. <bookmark mark='d'/> That is too big, so "
            "narrowing runs the loop again, letting only the infinite bound come back down: zero to a hundred. "
            "<bookmark mark='e'/> Two rounds and two narrowing steps, instead of a hundred and one. On the "
            "two-counter loop, plain iteration never stops."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nl), FadeIn(nums), FadeIn(inf), FadeIn(bar), FadeIn(txt))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(rl))
            for k, (m, xr, col) in enumerate(captions):
                if k in (0, 1, 2):
                    vo.wait_until("bcd"[k])
                self.play(Transform(txt, m), Transform(bar, bar_to(xr, col)), run_time=1.2)
                self.wait(0.4)
            vo.wait_until("e")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def relational(self):
        gap = load("absint")["gap"]
        two = load("absint")["examples"]["two_widen"]
        pts = gap["reachable"]
        head = label(r"What intervals cannot see", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([("    " if p["code"].startswith(("i = i", "j = j")) else "") + p["code"]
                           for p in two["points"]], size=20).move_to([-4.6, 1.4, 0])
        P = plane(i_max=12, j_max=40, w=4.2, h=4.4).move_to([1.0, -0.4, 0])
        ax = P.ax
        dots = VGroup(*[Dot(ax.c2p(i, j), radius=0.055, color=WHITE) for i, j in pts])
        climb = gap["no_widen_climb"]
        jt = ValueTracker(0)
        it = ValueTracker(0)
        grow = always_redraw(lambda: box(ax, 0, min(it.get_value(), 12), 0, min(jt.get_value(), 40), HEAD,
                                         opacity=0.12))
        cnt = always_redraw(lambda: MathTex(rf"j \le {int(round(jt.get_value()))}", font_size=28, color=HEAD).next_to(
            ax.c2p(12, 40), RIGHT, buff=0.2).shift(DOWN * 0.3))
        last = climb[-1]
        assert last["i"] == [0, 10] and not gap["no_widen_converged"]
        clab = label(rf"plain iteration: \ round {last['iteration']}, \ $j \in {ivl(last['j'])}$, \ still climbing",
                     font_size=18, color=HEAD).next_to(P, DOWN, buff=0.25)
        wh = gap["widen_head"]
        wbox = box(ax, 0, 10, 0, 40, LAM, opacity=0.12)
        wl = MathTex(rf"i \in {ivl(wh['i'])},\ j \in {ivl(wh['j'])}", font_size=28, color=LAM).next_to(
            ax.c2p(12, 40), RIGHT, buff=0.2).shift(DOWN * 0.9)
        ba = gap["widen_before_assert"]
        alarm = wrapped_label(rf"at the assertion: \ $i \in {ivl(ba['i'])}$, \ $j \in {ivl(ba['j'])}$: \ "
                              r"\texttt{assert j == 20} is \textbf{not proved}, \ a false alarm", 3.7, font_size=19,
                              color=NO).next_to(code, DOWN, buff=0.5).align_to(code, LEFT)
        line = DashedLine(ax.c2p(0, 0), ax.c2p(12, 24), color=YES, stroke_width=3)
        ll = MathTex(r"j = 2i", font_size=28, color=YES).next_to(ax.c2p(12, 24), RIGHT, buff=0.15)
        rel = wrapped_label(r"the relation is what boxes lose; \ linear equalities \ (Karr, \ 1976) \ and "
                            r"polyhedra \ (Cousot and Halbwachs, \ 1978) \ keep $j = 2i$, \ and with $i = 10$ give "
                            r"$j = 20$", 3.7, font_size=19, color=YES).next_to(alarm, DOWN, buff=0.35).align_to(
            alarm, LEFT)
        assert not gap["assert_proved"]
        with self.voiceover(
            "Intervals have a blind spot. <bookmark mark='a'/> Here i counts to ten and j goes up by two, so j is "
            "always twice i, and ends at twenty. <bookmark mark='b'/> Plain iteration bounds i by the test, but "
            "nothing bounds j on its own, and its interval climbs by two every round, for ever. <bookmark mark='c'/> "
            "Widening sends j to infinity, and narrowing cannot bring it back. <bookmark mark='d'/> So the assertion "
            "that j is twenty is not proved: a false alarm, on a correct program. <bookmark mark='e'/> What was lost "
            "is the relation. Relational domains keep j equal to two i, and with i equal to ten, j is twenty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(P))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15))
            vo.wait_until("b")
            self.add(grow, cnt)
            self.play(it.animate.set_value(10), jt.animate.set_value(20), run_time=2, rate_func=linear)
            self.play(jt.animate.set_value(40), run_time=2, rate_func=linear)
            self.play(FadeIn(clab))
            vo.wait_until("c")
            self.remove(grow, cnt)
            self.play(FadeIn(wbox), FadeIn(wl))
            vo.wait_until("d")
            self.play(FadeIn(alarm))
            vo.wait_until("e")
            self.play(Create(line), FadeIn(ll), FadeIn(rel))
        self.wait(0.4)
        self.clear_scene()

    def domains(self):
        pts = load("absint")["gap"]["reachable"]
        head = label(r"A ladder of domains", font_size=36).to_edge(UP, buff=0.3)
        P = plane(i_max=12, j_max=24, w=4.4, h=4.4).move_to([-4.2, -0.2, 0])
        ax = P.ax
        dots = VGroup(*[Dot(ax.c2p(i, j), radius=0.055, color=WHITE) for i, j in pts])
        i0, i1 = min(p[0] for p in pts), max(p[0] for p in pts)
        j0, j1 = min(p[1] for p in pts), max(p[1] for p in pts)
        s1 = max(i + j for i, j in pts)
        d0, d1 = min(j - i for i, j in pts), max(j - i for i, j in pts)
        bx = box(ax, i0, i1, j0, j1, HEAD, opacity=0.08)
        # the octagon: the box cut by i + j and j - i bounds; its corners, in order round the boundary
        corners = []
        for (a, b) in ((i0, d0 + i0), (i0, min(j1, d1 + i0)), (min(i1, s1 - j1), j1), (i1, min(j1, s1 - i1)),
                       (i1, max(j0, d0 + i1)), (max(i0, j0 - d1), j0)):
            corners.append(ax.c2p(a, b))
        corners = [c for k, c in enumerate(corners) if k == 0 or not np.allclose(c, corners[k - 1])]
        corners = corners[:-1] if np.allclose(corners[0], corners[-1]) else corners
        assert len(corners) == 4                       # j = 2i: the octagon is a parallelogram here
        octo = Polygon(*corners, color=LAM, stroke_width=2.5, fill_color=LAM, fill_opacity=0.12)
        seg = Line(ax.c2p(i0, j0), ax.c2p(i1, j1), color=YES, stroke_width=5)
        rows = [[r"intervals", r"$a \le x \le b$", r"linear", r"Astr\'ee, \ compilers"],
                [r"octagons \ (Min\'e, \ 2006)", r"$\pm x \pm y \le c$", r"cubic", r"Astr\'ee"],
                [r"polyhedra \ (1978)", r"$\sum_k a_k x_k \le c$", r"exponential", r"research tools"]]
        tab = grid_table([r"domain", r"facts it keeps", r"cost", r"used in"], rows, widths=[2.5, 1.8, 1.4, 2.2],
                         row_h=0.6, font_size=19, colors=[[HEAD] * 4, [LAM] * 4, [YES] * 4], mono_cols=())
        tab.move_to([2.9, 1.3, 0])
        cap = label(rf"the same {len(pts)} points: \ box, \ octagon, \ and the exact segment", font_size=18,
                    color=GREY_A).next_to(P, DOWN, buff=0.2)
        ast = wrapped_label(r"\textbf{Astr\'ee} \ (Cousot's group, \ \'Ecole normale sup\'erieure): \ in 2003 it "
                            r"proved, \ fully automatically, \ that the primary flight-control software of the Airbus "
                            r"A340 can raise no run-time error \ (no overflow, \ no division by zero, \ no "
                            r"out-of-bounds access), \ and later the A380's", 6.6, font_size=19, color=WHITE)
        ast.next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Domains form a ladder of precision and cost. <bookmark mark='a'/> Intervals draw a box, at a cost linear"
            " in the number of variables. <bookmark mark='b'/> Antoine Miné's octagons also bound sums and "
            "differences of pairs, at cubic cost; here they cut the box to a parallelogram, but still cannot say that"
            " j is twice i. <bookmark mark='c'/> Convex polyhedra can: they shrink to the exact segment, but their "
            "operations can take exponential time. <bookmark mark='d'/> Real analysers mix domains. In 2003 Astrée, "
            "from the Cousots' group in Paris, proved automatically that the Airbus A340's flight-control software "
            "can raise no run-time error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(P), FadeIn(dots), FadeIn(cap))
            self.play(FadeIn(VGroup(*tab.cells[0], tab.rule)))
            vo.wait_until("a")
            self.play(Create(bx), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(Create(octo), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(Create(seg), FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(ast))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, mono)
