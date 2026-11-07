from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

COLS = [YES, DATA, LAM]          # the three colours of the small example


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def id_node(v, color=GREY_B, r=0.3, size=20):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    return VGroup(c, label(str(v), font_size=size, color=WHITE).move_to(c))


def f_example(a, b):
    """The illustrative 3-colouring of B_2 on ids 1..5: the highest bit where a - 1 and b - 1 differ."""
    return ((a - 1) ^ (b - 1)).bit_length() - 1


class Linial(VoiceoverScene):
    def construct(self):
        self.card()
        self.windows()
        self.base()
        self.speedup()
        self.example()
        self.tower()
        self.elimination()

    def card(self):
        card = chapter_card(3, r"Linial's lower bound", r"Could a ring be coloured in constant time?",
                            lit=(1987, 2019), extra=((1987, r"Linial: \ locality in distributed graph algorithms"),
                                                     (1992, r"the journal version, \ SIAM J.\ Computing"),
                                                     (2019, r"Brandt: \ automatic round elimination")), part=PART)
        with self.voiceover("Chapter three. Linial's lower bound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def windows(self):
        head = label(r"An algorithm is a function of windows", font_size=36).to_edge(UP, buff=0.3)
        ids = [7, 3, 9, 1, 5, 8, 2, 6, 4]
        nodes = VGroup(*[id_node(v) for v in ids]).arrange(RIGHT, buff=0.45).move_to([0, 1.75, 0])
        arrs = VGroup(*[Arrow(nodes[k].get_right(), nodes[k + 1].get_left(), buff=0.04, stroke_width=2,
                              color=GREY_C, max_tip_length_to_length_ratio=0.35) for k in range(len(ids) - 1)])
        dots = VGroup(label(r"$\cdots$", font_size=28, color=GREY_B).next_to(nodes, LEFT, buff=0.25),
                      label(r"$\cdots$", font_size=28, color=GREY_B).next_to(nodes, RIGHT, buff=0.25))
        nodes[4][0].set_stroke(DATA, width=3)
        nodes[5][0].set_stroke(LAM, width=3)
        bv = Brace(nodes[3:6], DOWN, buff=0.1, color=DATA)
        bvl = label(r"what $v$ sees after $t = 1$ round", font_size=18, color=DATA).next_to(bv, DOWN, buff=0.08)
        bw = Brace(nodes[4:7], UP, buff=0.1, color=LAM)
        bwl = label(r"what its successor sees", font_size=18, color=LAM).next_to(bw, UP, buff=0.06)
        ill = note(r"ids illustrative", font_size=16).next_to(nodes, RIGHT, buff=0.2).shift(DOWN * 0.55)
        fs = 30
        rows = [MathTex(r"c(v)", r"=", r"f(", r"x_{-t}, \dots, x_t", r")", font_size=fs),
                MathTex(r"c(\mathrm{succ}\,v)", r"=", r"f(", r"x_{-t+1}, \dots, x_{t+1}", r")", font_size=fs),
                MathTex(r"f(", r"x_1, \dots, x_{2t+1}", r")", r"\neq", r"f(", r"x_2, \dots, x_{2t+2}", r")",
                        font_size=fs)]
        rows[0][0].set_color(DATA)
        rows[1][0].set_color(LAM)
        rows[2][3].set_color(HEAD)
        whys = [label(r"a $t$-round algorithm: \ a function $f$ of the $2t + 1$ ids around a node", font_size=18,
                      color=GREY_B),
                label(r"its successor sees the same window, \ shifted by one", font_size=18, color=GREY_B),
                label(r"neighbours differ, \ for any $2t + 2$ distinct ids \ (each such row occurs on some ring)",
                      font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.25).move_to([-1.9, -1.1, 0])
        box = wrapped_label(r"so $f$ properly colours the \textbf{neighbourhood graph} $\mathcal N_{2t+1}$: \ its "
                            r"vertices are windows of $2t + 1$ distinct ids, \ and each window is joined to its "
                            r"shifts", 3.9, font_size=19, color=HEAD)
        frame = SurroundingRectangle(box, color=HEAD, buff=0.2, corner_radius=0.1, stroke_width=1.8)
        VGroup(frame, box).move_to([4.6, -1.1, 0])
        with self.voiceover(
            "Nathan Linial proved in 1987, in a paper published in full in 1992, that log star cannot be beaten. "
            "<bookmark mark='a'/> On an oriented ring, after t rounds a node knows the two t plus one identifiers "
            "centred on it, and nothing more. <bookmark mark='b'/> So any t-round algorithm is a function f from "
            "such windows to colours, and its successor's colour is f of the same window shifted one place. "
            "<bookmark mark='c'/> For a proper colouring, f must give every window and its shift different "
            "colours, since any row of distinct identifiers appears on some ring. <bookmark mark='d'/> So f "
            "properly colours a graph whose vertices are windows, the neighbourhood graph, which must therefore "
            "have chromatic number at most three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(arrs), FadeIn(dots), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowFromCenter(bv), FadeIn(bvl))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            self.play(GrowFromCenter(bw), FadeIn(bwl))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(col[2]))
            vo.wait_until("d")
            self.play(Create(frame), FadeIn(box))
        self.wait(0.4)
        self.clear_scene()

    def base(self):
        head = label(r"Keep only increasing windows", font_size=36).to_edge(UP, buff=0.3)
        n = 5
        c0 = np.array([-4.0, -0.2, 0])
        P = [c0 + 1.8 * np.array([np.cos(PI / 2 - k * TAU / n), np.sin(PI / 2 - k * TAU / n), 0]) for k in range(n)]
        cols = [YES, DATA, HEAD, NO, LAM]
        nodes = VGroup(*[id_node(k + 1).move_to(P[k]) for k in range(n)])
        edges = VGroup(*[Line(P[a], P[b], color=GREY_D, stroke_width=2) for a in range(n) for b in range(a + 1, n)])
        edges.set_z_index(-1)
        cap = label(r"$B_1$ for $n = 5$: \ every pair joined", font_size=19, color=GREY_A).next_to(nodes, DOWN,
                                                                                                   buff=0.3)
        fs = 30
        rows = [MathTex(r"B_k", r":\ ", r"x_1 < x_2 < \dots < x_k", r",\quad", r"(x_1, \dots, x_k)", r"\sim",
                        r"(x_2, \dots, x_{k+1})", font_size=fs),
                MathTex(r"\chi(B_{2t+1})", r"\le", r"\chi(\mathcal N_{2t+1})", r"\le", r"3", font_size=fs),
                MathTex(r"B_1", r":\ ", r"(x_1)", r"\sim", r"(x_2)", r"\ \text{for all } x_1 < x_2", font_size=fs),
                MathTex(r"\chi(B_1)", r"=", r"n", font_size=fs)]
        rows[3][2].set_color(NO)
        whys = [label(r"windows whose ids increase, \ joined to their increasing shifts", font_size=18, color=GREY_B),
                label(r"a subgraph never needs more colours", font_size=18, color=GREY_B),
                label(r"one id per window: \ every two ids are joined", font_size=18, color=GREY_B),
                label(r"the complete graph on $n$ ids needs $n$ colours", font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.28).move_to([2.25, 0.1, 0])
        plan = wrapped_label(r"the plan: \ walk from $B_{2t+1}$ down to $B_1$, \ one id at a time, \ and watch how "
                             r"many colours are needed", 12.4, font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The neighbourhood graph is enormous, so the argument studies a piece of it. <bookmark mark='a'/> Keep "
            "only windows whose identifiers increase, joined to their increasing shifts; call this graph B k, for "
            "windows of length k. <bookmark mark='b'/> A subgraph never needs more colours, so a t-round "
            "three-colouring of the ring three-colours B two t plus one. <bookmark mark='c'/> Now the smallest "
            "case, windows of length one. Any two identifiers form an increasing pair, so B one is the complete "
            "graph on n vertices, <bookmark mark='d'/> and it needs n colours. <bookmark mark='e'/> The proof "
            "walks from long windows down to short ones, one identifier at a time, counting how fast the colours "
            "may grow."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(FadeIn(col[1]))
            vo.wait_until("c")
            self.play(FadeIn(nodes), Create(edges), FadeIn(cap))
            self.play(FadeIn(col[2]))
            vo.wait_until("d")
            self.play(*[nd[0].animate.set_fill(c, opacity=0.6) for nd, c in zip(nodes, cols)])
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(plan))
        self.wait(0.4)
        self.clear_scene()

    def speedup(self):
        head = label(r"One id shorter, \ exponentially more colours", font_size=36).to_edge(UP, buff=0.3)
        stmt = MathTex(r"\chi(B_k) \le c", r"\;\Longrightarrow\;", r"\chi(B_{k-1}) \le 2^c", font_size=36,
                       color=HEAD).next_to(head, DOWN, buff=0.35)
        fs = 28
        rows = [
            MathTex(r"g(x_1, \dots, x_{k-1})", r"=", r"\{\, f(x_1, \dots, x_{k-1}, y) : y > x_{k-1} \,\}",
                    font_size=fs),
            MathTex(r"g(x_1, \dots, x_{k-1})", r"=", r"g(x_2, \dots, x_k)", r"\ \ni\ ", r"a = f(x_1, \dots, x_k)",
                    font_size=fs),
            MathTex(r"a", r"=", r"f(x_2, \dots, x_k, y)", r"\ \text{for some } y > x_k", font_size=fs),
            MathTex(r"f(x_1, \dots, x_k)", r"=", r"f(x_2, \dots, x_k, y)", r"\quad", r"\text{on an edge of } B_k",
                    font_size=fs),
        ]
        rows[0][2].set_color(DATA)
        rows[3][4].set_color(NO)
        whys = [label(r"label a short window by the \textit{set} of colours its extensions receive", font_size=18,
                      color=GREY_B),
                label(r"suppose two neighbours in $B_{k-1}$ got the same set; \ it contains $a$, \ taking $y = x_k$",
                      font_size=18, color=GREY_B),
                label(r"so $a$ is also the colour of some extension of the second window", font_size=18,
                      color=GREY_B),
                label(r"two neighbours in $B_k$ with one colour: \ impossible, \ so $g$ is proper", font_size=18,
                      color=GREY_B)]
        col = stacked(rows, whys, buff=0.2).next_to(stmt, DOWN, buff=0.35)
        concl = label(r"$g$ takes subsets of $c$ colours as values: \ at most $2^c$ of them", font_size=21,
                      color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the heart of the proof. <bookmark mark='a'/> If windows of length k can be properly coloured "
            "with c colours, windows of length k minus one can be coloured with two to the c. <bookmark mark='b'/> "
            "Colour each short window by a set: the colours f gives to all its increasing extensions by one more "
            "identifier y. <bookmark mark='c'/> Suppose two neighbouring short windows got the same set. The first "
            "set contains a, the colour of the first window extended by x k. <bookmark mark='d'/> So a is in the "
            "second set too: some extension of the second window by a larger y also has colour a. <bookmark "
            "mark='e'/> But those two long windows are neighbours in B k with the same colour, which is "
            "impossible. So the set colouring is proper, <bookmark mark='f'/> and its values are subsets of c "
            "colours: at most two to the c of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(stmt))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()

    def example(self):
        head = label(r"The lemma on five ids", font_size=36).to_edge(UP, buff=0.3)
        n = 5
        pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        X = {i: np.array([-5.9 + (i - 1) * 1.3, -0.3, 0]) for i in range(1, n + 1)}
        base_ = Line(X[1] + LEFT * 0.4, X[n] + RIGHT * 0.4, color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Dot(X[i], radius=0.07, color=GREY_A),
                                label(str(i), font_size=20, color=WHITE).next_to(X[i], DOWN, buff=0.15))
                         for i in X])
        boxes = {}
        for p in pairs:
            boxes[p] = ArcBetweenPoints(X[p[0]], X[p[1]], angle=-0.62 * PI, color=GREY_B, stroke_width=3)
        gv = VGroup(*boxes.values())
        cap = wrapped_label(r"$B_2$: \ each arc is a vertex, \ a pair $a < b$; \ arc $ab$ and arc $bc$ are "
                            r"neighbours", 5.6, font_size=18, color=GREY_A).next_to(ticks, DOWN, buff=0.25)
        cap.set_x(X[3][0])
        rule = note(r"illustrative $f$: \ the highest bit where $a - 1$ and $b - 1$ differ", font_size=16).next_to(
            cap, DOWN, buff=0.1)
        edges = VGroup(base_, ticks)
        sets = {}
        rowsg = VGroup()
        for x in range(1, n + 1):
            s = sorted({f_example(x, y) for y in range(x + 1, n + 1)})
            sets[x] = s
            body = VGroup(*[Dot(radius=0.11, color=COLS[k]) for k in s]).arrange(RIGHT, buff=0.12) if s else \
                MathTex(r"\varnothing", font_size=26, color=GREY_B)
            rowsg.add(VGroup(MathTex(rf"g({x})", r"=", font_size=28), body).arrange(RIGHT, buff=0.2))
        for r in rowsg:
            r[1].next_to(r[0], RIGHT, buff=0.2)
        rowsg.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([1.6, 0.9, 0])
        k5 = label(rf"{len(set(map(tuple, sets.values())))} different sets: \ a proper colouring of $B_1$, "
                   r"\ the complete graph", font_size=19, color=YES).next_to(rowsg, DOWN, buff=0.35)
        bound = label(r"3 colours on $B_2$, \ so at most $2^3 = 8$ sets on $B_1$; \ here 5 are needed", font_size=19,
                      color=HEAD).next_to(k5, DOWN, buff=0.2)
        VGroup(k5, bound).align_to(rowsg, LEFT)
        with self.voiceover(
            "Let us run the lemma on five identifiers. <bookmark mark='a'/> These are the windows of length two, "
            "increasing pairs, with a b joined to b c. <bookmark mark='b'/> Three colours suffice here; one way is "
            "to colour a b by the highest bit where a minus one and b minus one differ. <bookmark mark='c'/> Now "
            "give each identifier the set of colours on the pairs that start with it. One gets all three; five, "
            "which starts no pair, gets the empty set. <bookmark mark='d'/> All five sets differ, so they properly "
            "colour the complete graph on five vertices, as the lemma promised: at most eight sets were allowed, "
            "and five were needed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(edges), Create(gv), FadeIn(cap))
            vo.wait_until("b")
            self.play(*[boxes[p].animate.set_color(COLS[f_example(*p)]) for p in pairs], FadeIn(rule))
            vo.wait_until("c")
            for x, r in zip(range(1, n + 1), rowsg):
                starts = [boxes[(x, y)] for y in range(x + 1, n + 1)]
                anims = [Indicate(b, color=WHITE, scale_factor=1.05) for b in starts]
                self.play(FadeIn(r), *anims, run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(k5))
            self.play(FadeIn(bound))
        self.wait(0.4)
        self.clear_scene()

    def tower(self):
        c = load("cv")
        head = label(r"Iterate: \ a tower of exponentials", font_size=36).to_edge(UP, buff=0.3)
        chain_vals = [(r"2t + 1", r"3"), (r"2t", r"8"), (r"2t - 1", r"256"), (r"2t - 2", r"2^{256}"),
                      (r"\cdots", r"\cdots"), (r"1", r"n")]
        chain = VGroup()
        for w, v in chain_vals:
            fr = RoundedRectangle(width=1.65, height=0.95, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5,
                                  fill_color=BG, fill_opacity=1)
            t = VGroup(MathTex(rf"k = {w}", font_size=20, color=GREY_A), MathTex(v, font_size=28, color=HEAD)).arrange(
                DOWN, buff=0.1).move_to(fr)
            chain.add(VGroup(fr, t))
        chain.arrange(RIGHT, buff=0.42).next_to(head, DOWN, buff=0.35)
        chain[-1][1][1].set_color(NO)
        ca = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.04, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.4) for k in range(len(chain) - 1)])
        cl = label(r"colours a proper colouring of $B_k$ may need, \ at most", font_size=17, color=GREY_B).next_to(
            chain, DOWN, buff=0.12)
        fs = 30
        rows = [
            MathTex(r"n", r"=", r"\chi(B_1)", r"\le", r"\underbrace{2^{2^{\cdot^{\cdot^{2^{3}}}}}}_{2t\ \text{twos}}",
                    font_size=fs),
            MathTex(r"\log^* n", r"\le", r"2t + \log^* 3", r"=", r"2t + 2", font_size=fs),
            MathTex(r"t", r"\ge", r"\tfrac12 \log^* n - 1", font_size=fs),
        ]
        rows[2].set_color(YES)
        whys = [label(r"apply the lemma $2t$ times, \ from $\chi(B_{2t+1}) \le 3$", font_size=18, color=GREY_B),
                label(r"each 2 in the tower is undone by one logarithm; \ $\log^* 3 = 2$", font_size=18,
                      color=GREY_B),
                label(r"any 3-colouring of an $n$-node ring needs this many rounds", font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.25).move_to([-2.9, -0.75, 0])
        lb = math.ceil(c["log_star"] / 2 - 1)
        nn = f"{c['n']:,}".replace(",", "{,}")
        side = VGroup(
            wrapped_label(rf"$n = {nn}$: \ $\log^* n = {c['log_star']}$, \ so any algorithm needs at least "
                          rf"{lb} rounds; \ Cole and Vishkin used {c['rounds']}", 4.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"the constants differ, \ the growth does not: \ three-colouring a ring takes "
                          r"$\Theta(\log^* n)$ rounds", 4.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, -0.75, 0])
        with self.voiceover(
            "Now apply the lemma again and again. <bookmark mark='a'/> A t-round algorithm three-colours windows "
            "of length two t plus one. One identifier shorter, at most eight colours; then two hundred and "
            "fifty-six; then two to the two hundred and fifty-six; and so on, down to windows of length one, which "
            "need n. <bookmark mark='b'/> So n is at most a tower of two t twos with a three on top. <bookmark "
            "mark='c'/> Each logarithm peels off one level, so log star of n is at most two t plus two, <bookmark "
            "mark='d'/> and t is at least half of log star of n, minus one. <bookmark mark='e'/> For our "
            "million-node ring log star is five, so every algorithm needs at least two rounds; Cole and Vishkin's "
            "used seven. The constants differ, the growth does not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cl))
            for k, box in enumerate(chain):
                anims = [FadeIn(box, shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(ca[k - 1]))
                self.play(*anims, run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            vo.wait_until("c")
            self.play(FadeIn(col[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def elimination(self):
        head = label(r"Round elimination", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"$\Pi_0$ in $t$ rounds", DATA), (r"$\Pi_1$ in $t - 1$", DATA), (r"$\Pi_2$ in $t - 2$", DATA),
                 (r"$\cdots$", GREY_B), (r"$\Pi_t$ in 0 rounds", NO)]
        boxes = VGroup()
        for t, col in steps:
            lab_ = label(t, font_size=20, color=col)
            fr = RoundedRectangle(width=max(1.3, lab_.width + 0.4), height=0.7, corner_radius=0.1, stroke_color=col,
                                  stroke_width=1.8, fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(fr, lab_.move_to(fr)))
        boxes.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.6)
        if boxes.width > 12.4:
            boxes.scale_to_fit_width(12.4)
        arr = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, stroke_width=2, color=GREY_B,
                             max_tip_length_to_length_ratio=0.4) for k in range(len(boxes) - 1)])
        bl = label(r"each step: \ a faster algorithm for a derived problem", font_size=18, color=GREY_B).next_to(
            boxes, DOWN, buff=0.2)
        lines = VGroup(
            wrapped_label(r"Linial's lemma is one such step: \ removing one id from the window \ (half a round) \ "
                          r"turns $c$ colours into $2^c$; \ if the derived problem is still impossible in zero "
                          r"rounds, \ so was the original in $t$", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"Brandt \ (2019): \ for a wide class of problems on graphs that look locally like trees, "
                          r"\ the derived problem can be computed mechanically, \ so lower bounds can be found by a "
                          r"program", 12.4, font_size=21, color=YES),
            wrapped_label(r"the same paper of Linial's also gives the upper bound for any graph: \ $O(\Delta^2)$ "
                          r"colours in $O(\log^* n)$ rounds, \ for maximum degree $\Delta$", 12.4, font_size=21,
                          color=HEAD),
            wrapped_label(r"Chapter 11 returns to the map of which local problems take which time", 12.4,
                          font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bl, DOWN, buff=0.5)
        with self.voiceover(
            "Look at the shape of that proof. <bookmark mark='a'/> A t-round algorithm for one problem became a "
            "faster algorithm for a derived problem, and again, until a zero-round algorithm had to exist for a "
            "problem that plainly has none. <bookmark mark='b'/> Linial's lemma is one such step, trading one "
            "identifier of view for exponentially more colours. <bookmark mark='c'/> In 2019 Sebastian Brandt "
            "showed that for a wide class of problems on graphs that look locally like trees, the derived problem "
            "can be computed mechanically, so lower bounds can be searched for by a program: round elimination. "
            "<bookmark mark='d'/> Linial's paper also went the other way, colouring any graph of maximum degree "
            "delta with order delta squared colours in log star rounds. <bookmark mark='e'/> Chapter eleven "
            "returns to this map."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for k, b in enumerate(boxes):
                anims = [FadeIn(b, shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(arr[k - 1]))
                self.play(*anims, run_time=0.5)
            self.play(FadeIn(bl))
            for mk, ln in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
