from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CODE, COST, CTRL, DATA, HEAD, HIST, NO, PART, YES, live_int, load


class Jug(VGroup):
    def __init__(self, cap: int, unit=0.55, width=1.2, color=DATA):
        super().__init__()
        self.cap, self.unit = cap, unit
        self.glass = RoundedRectangle(width=width, height=cap * unit, corner_radius=0.08, stroke_color=GREY_A,
                                      stroke_width=3, fill_opacity=0)
        self.ticks = VGroup(*[Line(LEFT * 0.12, RIGHT * 0.12, color=GREY_D, stroke_width=1.5).move_to(
            self.glass.get_corner(DL) + UP * k * unit + RIGHT * 0.12) for k in range(1, cap)])
        self.level = ValueTracker(0)
        self.water = always_redraw(lambda: Rectangle(
            width=width - 0.1, height=max(self.level.get_value() * unit, 0.001), stroke_width=0, fill_color=color,
            fill_opacity=0.75).move_to(self.glass.get_bottom() + UP * (self.level.get_value() * unit / 2 + 0.03)))
        self.num = always_redraw(lambda: Integer(round(self.level.get_value()), font_size=36, color=WHITE).next_to(
            self.glass, UP, buff=0.15))
        self.cap_label = MathTex(rf"{cap}\ \text{{gal}}", font_size=28, color=GREY_B)
        self.cap_label.next_to(self.glass, DOWN, buff=0.15)
        self.add(self.water, self.glass, self.ticks, self.num, self.cap_label)


class Invariants(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.jugs()
        self.gcd()
        self.robot()
        self.termination()
        self.hoare()

    def card(self):
        card = chapter_card(5, r"Invariants", r"How do you prove that a process can never do the wrong thing?",
                            part=PART)
        with self.voiceover("Chapter five. Invariants."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def method(self):
        head = label(r"The state-machine method", font_size=38).to_edge(UP, buff=0.4)
        pts = [np.array([x, y, 0]) for x, y in ((-5, 0.6), (-3.4, 1.6), (-3.2, -0.4), (-1.6, 0.8), (-1.2, -1.4),
                                                (0.4, 1.4), (0.6, -0.2), (2.2, 0.8), (2.4, -1.4), (4.0, 0.4))]
        good = VGroup(*[Dot(p, radius=0.13, color=YES) for p in pts])
        edges = VGroup()
        for a, b in ((0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (3, 6), (4, 6), (5, 7), (6, 7), (6, 8), (7, 9),
                     (8, 9)):
            edges.add(Arrow(pts[a], pts[b], buff=0.16, stroke_width=2.5, color=GREY_C, max_tip_length_to_length_ratio=0.12))
        bad = VGroup(*[Dot(p, radius=0.13, color=NO) for p in (np.array([1.6, -2.6, 0]), np.array([4.4, -2.2, 0]))])
        region = RoundedRectangle(width=10.6, height=4.0, corner_radius=0.4, stroke_color=YES, stroke_width=2,
                                  fill_color=YES, fill_opacity=0.05).move_to(DOWN * 0.0 + RIGHT * -0.4)
        rl = label(r"the invariant holds", font_size=24, color=YES).next_to(region, UP, buff=0.1).align_to(region, LEFT)
        bl = label(r"bad states", font_size=24, color=NO).next_to(bad, DOWN, buff=0.15)
        start = label(r"start", font_size=24, color=HEAD).next_to(good[0], LEFT, buff=0.15)
        rules = VGroup(label(r"1. \ it holds at the start", font_size=28, color=GREY_A),
                       label(r"2. \ every move from a state where it holds \\ leads to a state where it holds",
                             font_size=28, color=GREY_A),
                       label(r"$\Rightarrow$ \ it holds in every reachable state: \ no path out", font_size=28,
                             color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).to_edge(
            LEFT, buff=0.6)
        with self.voiceover(
            "The hook's proof is an example of the most useful method in this whole series. <bookmark mark='a'/> Model "
            "a process as a state machine: states, and the moves allowed between them. The puzzle's states are "
            "arrangements, a program's are the values of its variables, a network protocol's are the messages in "
            "flight. <bookmark mark='b'/> Some states are bad: a crash, two trains on one track, a lost bank transfer. "
            "We want to prove they can never be reached. <bookmark mark='c'/> Find a property that holds at the start, "
            "and that every move preserves. Then, by induction on the number of moves, it holds in every reachable "
            "state. If the bad states break it, there is no path to them. You never have to explore the states; you "
            "only have to check one move."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(good), LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.05), FadeIn(start),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bad), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(region), FadeIn(rl), FadeIn(rules, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jugs(self):
        d = load("jugs")
        A, B = Jug(3, color=DATA), Jug(5, color=CTRL)
        VGroup(A, B).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(LEFT * 3.2 + DOWN * 0.4)
        head = label(r"Exactly 4 gallons, \ from a 3 and a 5", font_size=38).to_edge(UP, buff=0.35)
        moves = VGroup()
        for k, st in enumerate(d["path"][1:], 1):
            moves.add(label(rf"{k}. \ {st['move']} \ \ $\to$ \ $({st['state'][0]}, {st['state'][1]})$", font_size=28,
                            color=GREY_A))
        moves.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.2 + DOWN * 0.2)
        rules = note(r"allowed: \ fill a jug, \ empty a jug, \ pour one into the other until one is full or empty",
                     font_size=22).to_edge(DOWN, buff=0.3)
        src = note(r"\textit{Die Hard with a Vengeance} (1995)", font_size=20).next_to(head, DOWN, buff=0.1)
        with self.voiceover(
            "A puzzle from a film. Two jugs, three gallons and five gallons, no markings, a fountain. Measure out exactly "
            "four gallons, or the bomb goes off. <bookmark mark='a'/> You may fill a jug, empty it, or pour one into "
            "the other until one is full or the other is empty. <bookmark mark='b'/> Breadth-first search over the "
            f"states finds a shortest solution, {len(d['path']) - 1} moves. Fill the five. Pour it into the three, "
            "leaving two. Empty the three. Pour the two across. Fill the five again. Top up the three, which takes one "
            "gallon, and four are left."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rules))
            vo.wait_until("b")
            for k, st in enumerate(d["path"][1:]):
                a_, b_ = st["state"]
                self.play(FadeIn(moves[k], shift=RIGHT * 0.1), A.level.animate.set_value(a_),
                          B.level.animate.set_value(b_), run_time=1.0)
            self.play(Indicate(B.num, color=YES, scale_factor=1.6), moves[-1].animate.set_color(YES))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gcd(self):
        d = load("jugs")
        head = label(r"Which amounts can ever appear?", font_size=38).to_edge(UP, buff=0.4)
        inv = label(r"invariant: \ every amount in either jug is a multiple of $\gcd(A, B)$", font_size=30,
                    color=YES).next_to(head, DOWN, buff=0.4)
        why = label(r"fill: $A$ or $B$; \ empty: $0$; \ pour: \ a difference or a sum of multiples", font_size=26,
                    color=GREY_A).next_to(inv, DOWN, buff=0.25)
        rows = VGroup()
        for c in d["caps"]:
            rows.add(VGroup(MathTex(rf"A = {c['A']},\ B = {c['B']}", font_size=32, color=DATA),
                            MathTex(rf"\gcd = {c['gcd']}", font_size=32, color=CTRL),
                            MathTex(r"\{" + r",\,".join(str(x) for x in c["amounts"]) + r"\}", font_size=32,
                                    color=YES if 4 in c["amounts"] else NO)))
        for r in rows:
            r[0].move_to(LEFT * 4.2, aligned_edge=LEFT)
            r[1].move_to(LEFT * 0.6, aligned_edge=LEFT)
            r[2].move_to(RIGHT * 1.6, aligned_edge=LEFT)
        for i, r in enumerate(rows):
            r.shift(DOWN * (0.2 + 0.62 * i))
        hdr = VGroup(note(r"jugs", font_size=22).move_to(LEFT * 4.2, aligned_edge=LEFT),
                     note(r"invariant", font_size=22).move_to(LEFT * 0.6, aligned_edge=LEFT),
                     note(r"every amount reachable \ (computed)", font_size=22).move_to(RIGHT * 1.6, aligned_edge=LEFT)
                     ).shift(UP * 0.35)
        bez = label(r"and every multiple appears: \ Bezout, \ chapter 12", font_size=26, color=HEAD).to_edge(DOWN,
                                                                                                         buff=0.4)
        with self.voiceover(
            "Now the question an invariant answers: which amounts are possible at all? <bookmark mark='a'/> The "
            "invariant: every amount in either jug is a multiple of the greatest common divisor of the two sizes. "
            "<bookmark mark='b'/> It holds at the start, when both are empty. Filling gives A or B; emptying gives zero; "
            "pouring moves an amount that is a difference of multiples. Every move preserves it. "
            "<bookmark mark='c'/> With three and five, the gcd is one, and every amount is possible. With six and nine "
            "it is three: you can search for ever and never get four gallons, and the invariant tells you so before you "
            "start. <bookmark mark='d'/> The search finds the converse too: every multiple of the gcd up to the bigger "
            "jug does appear. That is Bézout's identity, and Euclid's algorithm again, in chapter twelve."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(inv))
            vo.wait_until("b")
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.25),
                      run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(bez))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def robot(self):
        head = label(r"A robot that moves diagonally", font_size=38).to_edge(UP, buff=0.4)
        N, s = 9, 0.58
        o = np.array([-3.0, -0.4, 0])
        dots = VGroup()
        for x in range(-4, 5):
            for y in range(-4, 5):
                ok = (x + y) % 2 == 0
                dots.add(Dot(o + np.array([x * s, y * s, 0]), radius=0.07, color=YES if ok else GREY_D))
        robot = Square(0.3, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(o)
        target = Circle(0.17, color=NO, stroke_width=3).move_to(o + np.array([s, 0, 0]))
        tl = label(r"$(1, 0)$?", font_size=26, color=NO).next_to(target, UP, buff=0.12)
        tl.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.04)
        rng = np.random.default_rng(4)
        path = [np.zeros(2, int)]
        for _ in range(14):
            step = np.array([rng.choice([-1, 1]), rng.choice([-1, 1])])
            nxt = path[-1] + step
            if np.abs(nxt).max() <= 4:
                path.append(nxt)
        txt = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"moves: \ $(x, y) \to (x \pm 1, \ y \pm 1)$", GREY_A),
            (r"invariant: \ $x + y$ is even", YES),
            (r"each move changes $x + y$ by $-2$, $0$ or $+2$", CTRL),
            (r"$(1, 0)$: \ $1 + 0$ is odd. \ Never.", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.4)
        with self.voiceover(
            "One more, to see how little an invariant needs. A robot on a grid moves one step diagonally at a time. "
            "Can it reach the square just to its right? <bookmark mark='a'/> Watch it wander. <bookmark mark='b'/> "
            "The invariant: x plus y is even. Each move changes x and y by one each, so their sum changes by minus two, "
            "zero or two. Every square it can ever visit is green. <bookmark mark='c'/> The target has x plus y equal to "
            "one, odd. The robot can wander for ever and it will never get there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(robot), Create(target), FadeIn(tl), FadeIn(txt[0]))
            vo.wait_until("a")
            for p in path[1:]:
                self.play(robot.animate.move_to(o + np.array([p[0] * s, p[1] * s, 0])), run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
            vo.wait_until("c")
            self.play(FadeIn(txt[3]), Indicate(target, color=NO))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def termination(self):
        head = label(r"Termination: \ a quantity that must shrink", font_size=38).to_edge(UP, buff=0.4)
        arr = [5, 2, 7, 1, 6, 3, 4]
        w = 0.62

        def bars(a):
            g = VGroup()
            for i, v in enumerate(a):
                b = Rectangle(width=w * 0.8, height=v * 0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
                b.move_to([(i - 3) * w - 2.6, -2.2 + v * 0.225, 0])
                g.add(b)
            return g

        def inv(a):
            return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])

        g = bars(arr)
        cnt = live_int(inv(arr), 44, COST)
        cl = VGroup(label(r"pairs out of order:", font_size=30, color=GREY_A), cnt).arrange(RIGHT, buff=0.3)
        cl.move_to(RIGHT * 0.5 + UP * 1.0, aligned_edge=LEFT)
        cnt.add_updater(lambda m: m.next_to(cl[0], RIGHT, buff=0.3))
        rule = label(r"rule: \ swap any adjacent pair that is out of order", font_size=28, color=CTRL).next_to(
            head, DOWN, buff=0.35)
        argm = VGroup(*[label(t, font_size=25, color=c) for t, c in (
            (r"each swap fixes exactly one pair", GREY_A),
            (r"a natural number that drops by $1$ each step: \\ at most $\binom{n}{2}$ swaps, \ then it stops", YES),
            (r"and when it stops, \ nothing is out of order: \ sorted", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cl, DOWN, buff=0.5).align_to(cl, LEFT)
        with self.voiceover(
            "Invariants prove that nothing bad happens. A second tool proves that something good eventually does: the "
            "process stops. <bookmark mark='a'/> Here is a sorting rule: find two neighbours in the wrong order, and "
            "swap them. Repeat. Does it always stop? <bookmark mark='b'/> Count the pairs that are out of order, "
            "anywhere in the list. Each swap of neighbours fixes exactly that one pair and changes no other. "
            "<bookmark mark='c'/> So the count drops by one at every step, and a natural number cannot drop for ever. "
            "At most n choose two swaps. And when no swap is possible, the count is zero, so the list is sorted. That "
            "quantity is called a variant, or a ranking function. Euclid's remainders in Part 1 were one; Part 16 uses "
            "this very count to analyse sorting algorithms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            a = list(arr)
            changed = True
            while changed:
                changed = False
                for i in range(len(a) - 1):
                    if a[i] > a[i + 1]:
                        pi, pj = g[i].get_x(), g[i + 1].get_x()
                        a[i], a[i + 1] = a[i + 1], a[i]
                        self.play(g[i].animate.set_x(pj), g[i + 1].animate.set_x(pi),
                                  cnt.tracker.animate.set_value(inv(a)), run_time=0.45)
                        g.submobjects[i], g.submobjects[i + 1] = g.submobjects[i + 1], g.submobjects[i]
                        changed = True
            vo.wait_until("c")
            self.play(FadeIn(argm, lag_ratio=0.3), g.animate.set_color(YES))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hoare(self):
        head = label(r"Invariants inside programs", font_size=38).to_edge(UP, buff=0.4)
        code = code_block([
            "s = 0",
            "i = 0",
            "while i < n:",
            "    # invariant: s == 0 + 1 + ... + (i - 1)",
            "    s = s + i",
            "    i = i + 1",
            "# here: i == n, so s == 0 + 1 + ... + (n - 1)",
        ], font_size=26).move_to(LEFT * 1.4 + UP * 0.3)
        code[3].set_color(YES)
        code[6].set_color(HEAD)
        notes = VGroup(note(r"holds before the loop: \ the empty sum is $0$", font_size=24),
                       note(r"each pass keeps it: \ add $i$, \ then move $i$ on", font_size=24),
                       note(r"at exit: \ invariant $+$ the loop's condition failing $=$ the answer", font_size=24)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(code, DOWN, buff=0.5).align_to(code, LEFT)
        hc = history_card(1969, r"Robert Floyd (1967), \ Tony Hoare (1969)", r"proofs about programs, \ built from loop "
                          r"invariants: \ Part 54 checks them by machine", width=4.6, font_size=21).to_corner(DR, buff=0.35)
        with self.voiceover(
            "In programs, the same idea has a name you will see in code reviews: the loop invariant. "
            "<bookmark mark='a'/> This loop adds up the numbers below n. The comment states what is true at the top of "
            "every pass: s is the sum of everything below i. <bookmark mark='b'/> It holds before the first pass, when "
            "both are zero. Each pass adds i and moves i on, so it still holds. And when the loop ends, the invariant "
            "plus the fact that i is no longer less than n gives exactly the answer we wanted. <bookmark mark='c'/> "
            "Robert Floyd and Tony Hoare turned this into a logic of programs in the late 1960s, and in Part 54 a "
            "machine checks such proofs for us."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(notes, lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()
