from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403
from explainer.philosophy.reasoner import matrix as mx

SET_COL = {"near": OK, "mid": HALF, "far": P.CLAIM, "slow": OK, "medium": HALF, "fast": BAD,
           "none": GREY_B, "light": OK, "firm": HALF, "hard": BAD}


def curve(G, xs, ys, color, width=3):
    ax = G.ax
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def heat(fn, n=16, size=2.6, color=OK) -> VGroup:
    g = VGroup()
    s = size / n
    for i in range(n):
        for j in range(n):
            a, b = (i + 0.5) / n, (j + 0.5) / n
            v = fn(a, b)
            g.add(Square(side_length=s, stroke_width=0, fill_color=interpolate_color(ManimColor("#0B0F17"),
                                                                                    ManimColor(color), v),
                         fill_opacity=1).move_to([i * s, j * s, 0]))
    frame = SurroundingRectangle(g, buff=0, color=GREY_C, stroke_width=1.5)
    xa = MathTex("a", font_size=24, color=GREY_A).next_to(frame, DOWN, buff=0.1)
    ya = MathTex("b", font_size=24, color=GREY_A).next_to(frame, LEFT, buff=0.1)
    return VGroup(g, frame, xa, ya)


class Fuzzy(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Degrees of truth", r"Can truth come in degrees, and can a machine use them?",
                            lit=(1965, 1987), part=PART)
        with self.voiceover("Chapter nine. Degrees of truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.zadeh()
        self.tnorms()
        self.controller()
        self.stop()

    def zadeh(self):
        hc = history_card(1965, r"Lotfi Zadeh", r"`Fuzzy sets', \textit{Information and Control}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        G = axes([150, 210], [0, 1.05], x_length=7.0, y_length=3.0, xticks=[150, 170, 190, 210], yticks=[0, 0.5, 1],
                 xlabel=r"height (cm)", ylabel=r"degree of `tall'", center=[0.6, -0.7, 0])
        xs = list(range(150, 211))
        ys = [min(1, max(0, (x - 165) / 25)) for x in xs]
        crisp = [1 if x >= 180 else 0 for x in xs]
        c1 = curve(G, xs, crisp, GREY_B, 2.5)
        c2 = curve(G, xs, ys, OK, 4)
        l1 = label(r"a classical set: \ in or out at 180", font_size=22, color=GREY_B).move_to([-5.0, -0.2, 0])
        l2 = label(r"a fuzzy set: \ membership in degrees", font_size=22, color=OK).move_to([-5.0, -0.8, 0])
        ops = label(r"Zadeh's operations: \ $\min$ for `and', \ $\max$ for `or', \ $1 - x$ for `not'", font_size=24,
                    color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The middle value of Łukasiewicz can be spread into a continuum. <bookmark mark='a'/>In 1965 Lotfi "
            "Zadeh, an engineer at Berkeley, defined fuzzy sets. <bookmark mark='b'/>A classical set of tall people "
            "draws a line, say at one hundred and eighty centimetres: in or out. <bookmark mark='c'/>A fuzzy set "
            "assigns each height a degree of membership between zero and one, rising gradually. "
            "<bookmark mark='d'/>For the connectives Zadeh took the minimum for 'and', the maximum for 'or', and "
            "one minus the degree for 'not': Łukasiewicz's tables, extended to every number in between."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(G))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(l1))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(ops))
        self.clear_scene()

    def tnorms(self):
        d = load("tnorms")
        head = label(r"Three ways to say `and' with degrees: \ t-norms", font_size=30, color=CONN).to_edge(UP,
                                                                                                       buff=0.4)
        specs = [(r"Gödel", r"\min(a, b)", lambda a, b: min(a, b)),
                 (r"product", r"a \cdot b", lambda a, b: a * b),
                 (r"Łukasiewicz", r"\max(0,\ a + b - 1)", lambda a, b: max(0.0, a + b - 1))]
        cols = VGroup()
        for name, f, fn in specs:
            hm = heat(fn, n=16, size=2.6)
            t = VGroup(label(name, font_size=26, color=GOAL), MathTex(f, font_size=30)).arrange(DOWN, buff=0.12)
            cols.add(VGroup(t, hm).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.45)
        res = MathTex(r"a \otimes c \le b \iff c \le (a \Rightarrow b)", font_size=34, color=GOAL).to_edge(DOWN,
                                                                                                    buff=0.9)
        rl = label(r"each t-norm has one residuum, \ its implication; \ the Reasoner checks the law on a grid "
                   r"$\checkmark$", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        hj = label(r"Hájek (1998): \ BL, the logic of all continuous t-norms", font_size=22, color=GREY_B).next_to(
            res, UP, buff=0.25)
        assert all(d["residuation"].values())
        with self.voiceover(
            "There is more than one way to say 'and' with degrees. <bookmark mark='a'/>Any operation that is "
            "associative, commutative, increasing, and has one as its unit will do. These are called t-norms. "
            "Here are the three basic ones, as maps: brighter means truer. The minimum, Gödel's. The product. And "
            "Łukasiewicz's, which is zero unless the two degrees together exceed one. <bookmark mark='b'/>Each "
            "comes with exactly one matching implication, its residuum, fixed by this law: c is below 'a implies "
            "b' exactly when 'a and c' is below b. The Reasoner checks the law for all three on a grid. "
            "<bookmark mark='c'/>In 1998 Petr Hájek gave the logic common to all continuous t-norms, which he "
            "called basic logic. Fuzzy logic, in this sense, is mathematical logic, with theorems and completeness "
            "proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(Write(res), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(hj))
        self.clear_scene()

    def controller(self):
        d = load("fuzzy")
        hc = history_card(1987, r"the Sendai subway", r"Hitachi's fuzzy train controller \ (Yasunobu and Miyamoto)",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        ex = d["example"]
        G1 = axes([0, 400], [0, 1.05], x_length=4.0, y_length=1.6, xticks=[0, 200, 400], yticks=[0, 1],
                  xlabel=r"distance to stop (m)", center=[-4.4, -0.9, 0])
        G2 = axes([0, 22], [0, 1.05], x_length=4.0, y_length=1.6, xticks=[0, 10, 20], yticks=[0, 1],
                  xlabel=r"speed (m/s)", center=[0.0, -0.9, 0])
        G3 = axes([0, 1], [0, 1.05], x_length=3.6, y_length=1.6, xticks=[0, 0.5, 1], yticks=[0, 1],
                  xlabel=r"brake", center=[4.6, -0.9, 0])
        c1 = VGroup(*[curve(G1, d["xs"]["dist"], ys, SET_COL[k]) for k, ys in d["sets"]["dist"].items()])
        c2 = VGroup(*[curve(G2, d["xs"]["speed"], ys, SET_COL[k]) for k, ys in d["sets"]["speed"].items()])
        c3 = VGroup(*[curve(G3, d["xs"]["brake"], ys, SET_COL[k], 2) for k, ys in d["sets"]["brake"].items()])
        n1 = VGroup(*[label(k, font_size=18, color=SET_COL[k]) for k in d["sets"]["dist"]]).arrange(RIGHT, buff=0.3
                                                                                                    ).next_to(G1, UP, buff=0.1)
        n2 = VGroup(*[label(k, font_size=18, color=SET_COL[k]) for k in d["sets"]["speed"]]).arrange(RIGHT, buff=0.3
                                                                                                     ).next_to(G2, UP, buff=0.1)
        n3 = VGroup(*[label(k, font_size=18, color=SET_COL[k]) for k in d["sets"]["brake"]]).arrange(RIGHT, buff=0.25
                                                                                                     ).next_to(G3, UP, buff=0.1)
        vl1 = DashedLine(G1.ax.c2p(ex["d"], 0), G1.ax.c2p(ex["d"], 1.05), color=GOAL)
        vl2 = DashedLine(G2.ax.c2p(ex["v"], 0), G2.ax.c2p(ex["v"], 1.05), color=GOAL)
        agg = G3.ax.plot_line_graph(d["xs"]["brake"], ex["agg"], add_vertex_dots=False, line_color=GOAL,
                                    stroke_width=4)
        area = Polygon(*[G3.ax.c2p(x, y) for x, y in zip(d["xs"]["brake"], ex["agg"])], G3.ax.c2p(1, 0),
                       G3.ax.c2p(0, 0), stroke_width=0, fill_color=GOAL, fill_opacity=0.25)
        cen = DashedLine(G3.ax.c2p(ex["brake"], 0), G3.ax.c2p(ex["brake"], 1.05), color=WHITE)
        fired = [(w, c, i) for i, (w, c) in enumerate(ex["fire"]) if w > 0]
        rule_txt = VGroup(*[label(rf"if {d['rules'][i][0]} and {d['rules'][i][1]}, \ brake {c}: \ fires at "
                                  rf"{w:.2f}", font_size=22, color=SET_COL[c]) for w, c, i in fired]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        ex_l = label(rf"now: \ {ex['d']:.0f} m to go, \ {ex['v']:.0f} m/s", font_size=24, color=GOAL).next_to(
            hc, DOWN, buff=0.3).align_to(hc, LEFT)
        out = label(rf"brake = centre of the shaded area = {ex['brake']:.2f}", font_size=24, color=WHITE).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Fuzzy logic's most famous success was a train. <bookmark mark='a'/>In 1987 the Sendai subway in Japan "
            "opened with a controller designed by Hitachi engineers, Seiji Yasunobu and Shoji Miyamoto, that "
            "braked by fuzzy rules. The Reasoner builds a small one. <bookmark mark='b'/>Distance to the stop is "
            "near, middling or far, each a fuzzy set. Speed is slow, medium or fast. <bookmark mark='c'/>The brake "
            "can be none, light, firm or hard. <bookmark mark='d'/>Nine rules link them, like 'if middling and "
            "fast, brake firm'. Now the train is one hundred and twenty metres out, at fifteen metres per second. "
            "<bookmark mark='e'/>Each rule fires to the degree that both its conditions hold, the minimum of the "
            "two. Two rules fire, partly. <bookmark mark='f'/>Each fired rule clips its brake set at its degree; "
            "the clipped sets are combined, and the brake applied is the centre of the shaded area."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(G1), FadeIn(G2), FadeIn(G3))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(n1), Create(c2), FadeIn(n2))
            vo.wait_until("c")
            self.play(Create(c3), FadeIn(n3))
            vo.wait_until("d")
            self.play(FadeIn(ex_l), Create(vl1), Create(vl2))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in rule_txt], lag_ratio=0.4))
            vo.wait_until("f")
            self.play(c3.animate.set_stroke(opacity=0.35), FadeIn(area), Create(agg))
            self.play(Create(cen), FadeIn(out))
        self.clear_scene()

    def stop(self):
        d = load("fuzzy")
        S = d["sims"]
        G = axes([0, 52], [0, 22], x_length=6.2, y_length=3.4, xticks=[0, 20, 40], yticks=[0, 10, 20],
                 xlabel=r"time (s)", ylabel=r"speed (m/s)", center=[-3.0, 0.45, 0])
        Ga = axes([0, 52], [-1.3, 0.1], x_length=6.2, y_length=1.4, xticks=[0, 20, 40], yticks=[-1.2, 0],
                  ylabel=r"braking (m/s$^2$)", center=[-3.0, -2.85, 0])
        fz = curve(G, S["fuzzy"]["t"], S["fuzzy"]["v"], OK, 4)
        bb = curve(G, S["bang"]["t"], S["bang"]["v"], BAD, 4)
        fa = curve(Ga, S["fuzzy"]["t"], S["fuzzy"]["a"], OK, 3)
        ba = curve(Ga, S["bang"]["t"], S["bang"]["a"], BAD, 3)
        leg = legend([(OK, r"fuzzy rules"), (BAD, r"two-valued rule: \ full brake at the last moment")],
                     font_size=22).move_to([3.6, 2.4, 0])
        hd = [label(r"", font_size=22), label(r"fuzzy", font_size=22, color=OK), label(r"two-valued", font_size=22,
                                                                                    color=BAD)]
        rows = [[label(r"stopping error", font_size=22), MathTex(rf"{S['fuzzy']['error']:+.1f}\ \text{{m}}",
                                                                  font_size=26),
                 MathTex(rf"{S['bang']['error']:+.1f}\ \text{{m}}", font_size=26)],
                [label(r"worst jerk", font_size=22), MathTex(rf"{S['fuzzy']['jerk']:.1f}\ \text{{m/s}}^3", font_size=26),
                 MathTex(rf"{S['bang']['jerk']:.1f}\ \text{{m/s}}^3", font_size=26)],
                [label(r"time to stop", font_size=22), MathTex(rf"{S['fuzzy']['time']:.0f}\ \text{{s}}", font_size=26),
                 MathTex(rf"{S['bang']['time']:.0f}\ \text{{s}}", font_size=26)]]
        grid = ValueGrid(hd, rows, col_w=[2.4, 1.6, 1.8], cell_h=0.6, font_size=24).move_to([3.5, 0.3, 0])
        moral = VGroup(label(r"the gain is comfort, \ not cleverness:", font_size=24, color=GOAL),
                       label(r"degrees let the brake change gradually", font_size=24, color=GOAL)).arrange(
            DOWN, buff=0.12).move_to([3.5, -1.9, 0])
        vag = label(r"is fuzzy logic a theory of vagueness? \ Chapter 11", font_size=22, color=GREY_B).move_to(
            [3.4, -2.8, 0])
        assert S["fuzzy"]["jerk"] < S["bang"]["jerk"]
        with self.voiceover(
            "Run the controller on a simulated train, six hundred metres from its stop at twenty metres per "
            "second. <bookmark mark='a'/>The fuzzy controller eases the brake on, then off. "
            "<bookmark mark='b'/>Compare a two-valued rule: no brake, then full brake at the last possible moment. "
            "<bookmark mark='c'/>Both stop near the mark. The two-valued rule is even a little faster. But its "
            "braking jumps from nothing to everything at once, and the jerk, the change in braking that "
            "passengers feel, is six times worse. <bookmark mark='d'/>So the gain is comfort, not cleverness: "
            "degrees let a decision change gradually. <bookmark mark='e'/>Whether degrees of truth also explain "
            "vagueness is a different question, and Chapter 11 takes it up."
        ) as vo:
            self.play(FadeIn(G), FadeIn(Ga), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(fz), Create(fa), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(bb), Create(ba), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(grid))
            vo.wait_until("d")
            self.play(FadeIn(moral))
            vo.wait_until("e")
            self.play(FadeIn(vag))
        self.clear_scene()
