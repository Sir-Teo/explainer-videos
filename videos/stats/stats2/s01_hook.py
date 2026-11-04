from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


def coin_pile(n=64, cols=8, r=0.13, center=ORIGIN) -> VGroup:
    g = VGroup(*[Circle(radius=r, stroke_color="#9C7A2E", stroke_width=1.5, fill_color="#E8C872", fill_opacity=1)
                 for _ in range(n)])
    g.arrange_in_grid(int(np.ceil(n / cols)), cols, buff=0.05)
    return g.move_to(center)


def tally(name: str, color, won: int, of=3, r=0.2) -> VGroup:
    dots = VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color,
                           fill_opacity=0.9 if k < won else 0.0) for k in range(of)]).arrange(RIGHT, buff=0.18)
    nm = label(name, font_size=34, color=color)
    g = VGroup(nm, dots).arrange(RIGHT, buff=0.35)
    g.dots = dots
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.letters()
        self.game()
        self.pacioli()
        self.fermat()
        self.pascal()
        self.check()
        self.objectives()

    # ------------------------------------------------------------------
    def letters(self):
        paris = VGroup(label(r"Blaise Pascal", font_size=36, color=PA), label(r"Paris, \ aged 31", font_size=24,
                                                                                 color=GREY_A)).arrange(DOWN, buff=0.15)
        toulouse = VGroup(label(r"Pierre de Fermat", font_size=36, color=PB),
                          label(r"Toulouse, \ a magistrate", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        paris.move_to([-4.3, 1.6, 0])
        toulouse.move_to([4.3, 1.6, 0])
        env = VGroup(Rectangle(width=0.9, height=0.56, stroke_color="#E9DFC8", stroke_width=2, fill_color="#2A2418",
                               fill_opacity=1),
                     Polygon([-0.45, 0.28, 0], [0, -0.05, 0], [0.45, 0.28, 0], stroke_color="#E9DFC8", stroke_width=2))
        env.move_to(paris.get_bottom() + DOWN * 0.7)
        hc = history_card(1654, r"letters between Paris and Toulouse, \ summer and autumn",
                          r"most of the letters survive; \ in them, probability is invented to settle a "
                          r"gambler's question", color=S.MUSEUM, width=6.0, font_size=24).move_to([0, -1.9, 0])
        tl = timeline(lit=(1654,)).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In the summer of 1654, two Frenchmen began exchanging letters about a gambling problem. "
            "<bookmark mark='a'/> One was Blaise Pascal, in Paris: thirty-one years old, already famous for a "
            "calculating machine and for experiments on the vacuum. <bookmark mark='b'/> The other was Pierre de "
            "Fermat, a magistrate in Toulouse, who did mathematics in the evenings and rarely published any of it. "
            "<bookmark mark='c'/> The problem had reached Pascal, by most accounts, from a gambler and writer, the "
            "Chevalier de Méré. It was already two hundred years old, and nobody had solved it. "
            "<bookmark mark='d'/> In a few letters, they did, and in solving it they invented the mathematics of "
            "chance."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(paris, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(toulouse, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(env))
            for _ in range(2):
                self.play(env.animate.move_to(toulouse.get_bottom() + DOWN * 0.7), path_arc=-0.6, run_time=1.2)
                self.play(env.animate.move_to(paris.get_bottom() + DOWN * 0.7), path_arc=-0.6, run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def game(self):
        a = tally(r"A", PA, 0).move_to([-3.6, 1.7, 0])
        b = tally(r"B", PB, 0).move_to([3.6, 1.7, 0])
        pile = coin_pile(center=[0, -1.0, 0])
        stake = label(r"the stake: \ $2 \times 32 = 64$ pistoles", font_size=28, color="#E8C872").next_to(pile, DOWN,
                                                                                                        buff=0.3)
        rule = label(r"first to \textbf{three} points takes all; \ each point is a fair toss", font_size=30)
        rule.to_edge(UP, buff=0.4)
        a2, b1 = tally(r"A", PA, 2).move_to(a), tally(r"B", PB, 1).move_to(b)
        stop = label(r"interrupted at $2$ to $1$", font_size=40, color=S.ACCENT).move_to([0, 0.6, 0])
        ask = label(r"How should the $64$ pistoles be divided?", font_size=36).move_to([0, -3.35, 0])
        with self.voiceover(
            "Here's the problem, in the form Pascal wrote it down. <bookmark mark='a'/> Two players, call them A and "
            "B, each put thirty-two pistoles into the pot. They play a game of rounds, each round a fair toss: "
            "whoever wins a round scores a point, and the first to three points takes all sixty-four. "
            "<bookmark mark='b'/> They play. A wins a round, then B, then A. <bookmark mark='c'/> The score is two "
            "to one, and the game is interrupted: there's no more time, or the lights go out, or someone knocks at "
            "the door. <bookmark mark='d'/> The game will never be finished. How should they divide the pot? Not "
            "fifty-fifty: A is ahead. Not all to A: A hasn't won yet. Then what's fair?"
        ) as vo:
            self.play(FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(rule), LaggedStart(*[FadeIn(c, scale=0.6) for c in pile], lag_ratio=0.02), run_time=2.0)
            self.play(FadeIn(stake))
            vo.wait_until("b")
            self.play(a.dots[0].animate.set_fill(PA, opacity=0.9), run_time=0.6)
            self.play(b.dots[0].animate.set_fill(PB, opacity=0.9), run_time=0.6)
            self.play(a.dots[1].animate.set_fill(PA, opacity=0.9), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(stop, scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.a, self.b, self.pile, self.stake, self.rule = a, b, pile, stake, rule
        self.play(FadeOut(stop), FadeOut(ask))

    def pacioli(self):
        hc = history_card(1494, r"Luca Pacioli, \ \emph{Summa de arithmetica}",
                          r"divide in proportion to the points won: \ $2 : 1$", color=GREY_B, width=5.6,
                          font_size=24).move_to([-3.7, -1.2, 0])
        split = MathTex(r"64 \times \tfrac23 = 42\tfrac23", r"\qquad", r"64 \times \tfrac13 = 21\tfrac13",
                        font_size=34).move_to([0, 0.5, 0])
        split[0].set_color(PA)
        split[2].set_color(PB)
        tc = history_card(1556, r"Niccol\`o Tartaglia", r"at $1$ to $0$, \ Pacioli gives A \emph{everything}. "
                          r"\ Absurd: \ after one round the game has barely begun.", color=S.RESID, width=5.6,
                          font_size=24).move_to([3.7, -1.2, 0])
        key = label(r"the split must depend on what \emph{could still happen}, \ not on what did", font_size=32,
                    color=S.ACCENT).move_to([0, -3.4, 0])
        with self.voiceover(
            "People had tried. <bookmark mark='a'/> In 1494 the Franciscan friar Luca Pacioli, Leonardo's friend and "
            "the father of double-entry bookkeeping, proposed dividing the pot in proportion to the points won: two "
            "to one. <bookmark mark='b'/> Forty-two and two-thirds pistoles to A, twenty-one and a third to B. "
            "<bookmark mark='c'/> Sixty years later Tartaglia pointed out the flaw. If the game stopped at one to "
            "nothing, Pacioli's rule would give A the entire pot, after a single round of a game to three. That "
            "can't be fair. <bookmark mark='d'/> The fault is deeper than the arithmetic. Pacioli divides by the "
            "past, by what has already happened. A fair division should depend on the future: on what could still "
            "happen, if the game went on."
        ) as vo:
            self.play(FadeOut(self.stake), self.pile.animate.scale(0.55).move_to([0, 2.95, 0]),
                      self.a.animate.scale(0.8).move_to([-4.8, 2.6, 0]), self.b.animate.scale(0.8).move_to([4.8, 2.6, 0]),
                      FadeOut(self.rule))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(Write(split))
            vo.wait_until("c")
            self.play(FadeIn(tc, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(key, shift=UP * 0.2))
        self.play(FadeOut(VGroup(hc, split, tc, key)))

    def fermat(self):
        d = load("points")
        rows = VGroup()
        for word, a_wins in d["fermat"]:
            cells = VGroup(*[VGroup(Circle(radius=0.34, stroke_width=0, fill_color=PA if ch == "A" else PB,
                                           fill_opacity=0.9), label(ch, font_size=30, color=BLACK))
                             for ch in word])
            for c in cells:
                c[1].move_to(c[0])
            cells.arrange(RIGHT, buff=0.25)
            verdict = label(r"A wins" if a_wins else r"B wins", font_size=30, color=PA if a_wins else PB)
            rows.add(VGroup(cells, verdict).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([-2.6, -1.05, 0])
        head = label(r"Fermat: \ play two more rounds, \ whatever happens", font_size=30, color=PB)
        head.next_to(rows, UP, buff=0.35)
        frac_ = MathTex(r"P(\text{A wins})", r"=", r"\tfrac34", font_size=44).move_to([3.6, 0.2, 0])
        frac_[0].set_color(PA)
        frac_[2].set_color(EXACT)
        share = MathTex(r"\tfrac34 \times 64 = 48", r"\qquad", r"\tfrac14 \times 64 = 16", font_size=34)
        share.next_to(frac_, DOWN, buff=0.5)
        share[0].set_color(PA)
        share[2].set_color(PB)
        obj = label(r"``but if A wins the first round, the second is never played''", font_size=26, color=GREY_A)
        obj.move_to([0, -3.45, 0])
        pile = self.pile
        left = VGroup(*pile[:48])
        right = VGroup(*pile[48:])
        with self.voiceover(
            "Fermat's answer is a trick of the imagination. <bookmark mark='a'/> A needs one more point; B needs "
            "two. So at most two more rounds would settle it. Imagine those two rounds are played, whatever "
            "happens. <bookmark mark='b'/> There are four ways they could go, each equally likely: A A, A B, B A, "
            "B B. <bookmark mark='c'/> In three of the four, A gets the point first. Only if B wins both does B "
            "take the game. <bookmark mark='d'/> So A should have three quarters of the pot, forty-eight pistoles, "
            "and B one quarter, sixteen. <bookmark mark='e'/> A colleague of Pascal's, Gilles de Roberval, objected: if A wins the "
            "next round, the second is never played, so why count it? Fermat's reply is the heart of the method: playing a "
            "round that can't change the winner changes nothing, so you may imagine it played. Complete the "
            "future, then count. <bookmark mark='f'/> Sixty-four pistoles, split forty-eight to sixteen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.3), run_time=1.6)
            self.play(*[Indicate(r, color=PA, scale_factor=1.05) for r, (_, w) in zip(rows, d["fermat"]) if w])
            vo.wait_until("d")
            self.play(Write(frac_))
            self.play(FadeIn(share, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(obj))
            vo.wait_until("f")
            self.play(FadeOut(VGroup(rows, head, obj, frac_, share)))
            self.play(left.animate.arrange_in_grid(6, 8, buff=0.05).scale(1.25).move_to([-3.3, -0.4, 0]),
                      right.animate.arrange_in_grid(2, 8, buff=0.05).scale(1.25).move_to([3.3, -0.4, 0]),
                      self.a.animate.scale(1.25).move_to([-3.3, 2.0, 0]), self.b.animate.scale(1.25).move_to([3.3, 2.0, 0]),
                      run_time=2.0)
            self.play(FadeIn(MathTex(r"48", font_size=48, color=PA).move_to([-3.3, -2.6, 0])),
                      FadeIn(MathTex(r"16", font_size=48, color=PB).move_to([3.3, -2.6, 0])))
        self.clear_scene()

    def pascal(self):
        d = load("points")
        stake = d["stake"]
        # the backward recursion as a tree, then the whole table
        tree = VGroup()
        root = MathTex(r"(2,1)", font_size=40).move_to([-4.6, 0.8, 0])
        up = MathTex(r"(3,1)", font_size=40, color=PA).move_to([-1.6, 2.2, 0])
        dn = MathTex(r"(2,2)", font_size=40).move_to([-1.6, -0.6, 0])
        e1 = Line(root.get_right(), up.get_left(), color=GREY_B)
        e2 = Line(root.get_right(), dn.get_left(), color=GREY_B)
        p1 = MathTex(r"\tfrac12", font_size=28, color=GREY_A).next_to(e1.get_center(), UP, buff=0.15)
        p2 = MathTex(r"\tfrac12", font_size=28, color=GREY_A).next_to(e2.get_center(), DOWN, buff=0.15)
        v_up = MathTex(r"64", font_size=36, color=PA).next_to(up, RIGHT, buff=0.3)
        v_dn = MathTex(r"32", font_size=36, color=GREY_A).next_to(dn, RIGHT, buff=0.3)
        why_dn = label(r"a tie: \ by symmetry, half", font_size=22, color=GREY_B).next_to(v_dn, RIGHT, buff=0.25)
        v_root = MathTex(r"\tfrac12 \cdot 64 + \tfrac12 \cdot 32", r"=", r"48", font_size=36).move_to([-3.9, -1.9, 0])
        v_root[2].set_color(EXACT)
        tree.add(root, up, dn, e1, e2, p1, p2, v_up, v_dn, why_dn, v_root)
        title = label(r"Pascal: \ value each score by its two futures, \ backwards from the end", font_size=30,
                      color=PA).to_edge(UP, buff=0.35)
        # the table, score (A's points, B's points), game to three
        cell = 1.0
        grid = VGroup()
        cells = {}
        origin = np.array([2.0, -2.2, 0])
        for a in range(4):
            for b in range(4):
                if a == 3 and b == 3:
                    continue
                if a == 3:
                    v, col = stake, PA
                elif b == 3:
                    v, col = 0, PB
                else:
                    v, col = d["pascal"][a][b], WHITE
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1.2, fill_color=CELL, fill_opacity=1)
                sq.move_to(origin + np.array([b * cell, a * cell, 0]))
                t = MathTex(f"{v:g}", font_size=30, color=col).move_to(sq)
                cells[(a, b)] = VGroup(sq, t)
                grid.add(cells[(a, b)])
        xl = label(r"B's points", font_size=22, color=PB).next_to(grid, DOWN, buff=0.15)
        yl = label(r"A's points", font_size=22, color=PA).rotate(PI / 2).next_to(grid, LEFT, buff=0.15)
        bt = VGroup(*[MathTex(str(b), font_size=22, color=GREY_B).move_to(origin + np.array([b * cell, -0.68, 0]))
                      for b in range(4)])
        at = VGroup(*[MathTex(str(a), font_size=22, color=GREY_B).move_to(origin + np.array([-0.68, a * cell, 0]))
                      for a in range(4)])
        xl.next_to(bt, DOWN, buff=0.08)
        yl.next_to(at, LEFT, buff=0.1)
        rule = MathTex(r"V(a, b)", r"=", r"\tfrac12\, V(a{+}1, b) + \tfrac12\, V(a, b{+}1)", font_size=32)
        rule.move_to([-3.4, -2.6, 0])
        name = label(r"the expected value: \ Huygens, 1657", font_size=24, color=S.ACCENT).next_to(rule, DOWN, buff=0.25)
        with self.voiceover(
            "Pascal solved it differently, and his way would turn out to be even more powerful. "
            "<bookmark mark='a'/> Start from the score, two to one, and look one round ahead. <bookmark mark='b'/> "
            "If A wins it, A has three points and takes all sixty-four. <bookmark mark='c'/> If B wins it, the score "
            "is two all; then the game is symmetric, and each deserves half, thirty-two. <bookmark mark='d'/> Each "
            "happens with probability one half, so A deserves the average of sixty-four and thirty-two: forty-eight. "
            "The same answer as Fermat's, by a different road. <bookmark mark='e'/> And the road goes everywhere. "
            "Write the value to A of every score in a table: sixty-four where A has won, zero where B has, "
            "<bookmark mark='f'/> and fill in the rest backwards, each cell the average of the cell above it and "
            "the cell to its right. <bookmark mark='g'/> That one rule, the value now is the average of the values "
            "next, is what Christiaan Huygens would call, three years later, the value of a chance. We call it "
            "expectation. Working backwards from the end is what we now call dynamic programming."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(root))
            vo.wait_until("b")
            self.play(Create(e1), FadeIn(p1), FadeIn(up), FadeIn(v_up))
            vo.wait_until("c")
            self.play(Create(e2), FadeIn(p2), FadeIn(dn), FadeIn(v_dn), FadeIn(why_dn))
            vo.wait_until("d")
            self.play(Write(v_root))
            vo.wait_until("e")
            self.play(tree.animate.scale(0.75).move_to([-3.6, 0.9, 0]))
            self.play(FadeIn(bt), FadeIn(at), FadeIn(xl), FadeIn(yl),
                      *[FadeIn(cells[k]) for k in cells if k[0] == 3 or k[1] == 3])
            vo.wait_until("f")
            for total in (4, 3, 2, 1, 0):
                ks = [(a, total - a) for a in range(3) if 0 <= total - a < 3]
                self.play(*[FadeIn(cells[k], scale=1.15) for k in ks], run_time=0.8)
            self.play(Indicate(cells[(2, 1)], color=EXACT, scale_factor=1.2))
            vo.wait_until("g")
            self.play(Write(rule), FadeIn(name))
        self.clear_scene()

    def check(self):
        d = load("points")
        running = np.asarray(d["running"])
        n = d["sim_n"]
        A = axes([0, n], [0.6, 0.9], x_length=9.0, y_length=4.2, xlabel=r"simulated finishes from $2$ to $1$",
                 ylabel=r"fraction won by A", xticks=[0, 2500, 5000, 7500, 10000], yticks=[0.6, 0.7, 0.75, 0.8, 0.9],
                 xfmt=lambda v: fmt_int(v), center=[-1.0, -0.3, 0])
        ax = A.ax
        xs = np.arange(len(running)) * 50 + 1
        path = curve(ax, xs[2:], np.clip(running[2:], 0.6, 0.9), SIM, 3)
        gold = DashedLine(ax.c2p(0, 0.75), ax.c2p(n, 0.75), color=EXACT, stroke_width=3)
        box = exact_sim(r"\tfrac34", 0.75, d["sim_p"], n).move_to([4.6, 2.2, 0])
        tag = note(r"computed: fair tosses, seeded").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Throughout this part we'll check every exact answer against simulation. <bookmark mark='a'/> Here are "
            f"{fmt_int(n)} games, each restarted from two to one and actually played out with simulated fair tosses. "
            f"<bookmark mark='b'/> The fraction that A wins wanders, then settles: {d['sim_p']:.4f}, against "
            "Fermat's three quarters. The exact answer is gold, the simulated one blue, and the gap between them is "
            "the noise of a finite experiment, a gap the rest of this series will learn to measure."
        ) as vo:
            self.play(FadeIn(A), Create(gold), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(path), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(box, shift=LEFT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 2", font_size=34, color=GREY_B), label(r"Chance, Counted", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"classical probability: \ Cardano, Galileo, de M\'er\'e; \ counting with permutations, combinations, "
            r"stars and bars",
            r"Bertrand's paradox, \ and Kolmogorov's axioms with their consequences: \ inclusion--exclusion, the union "
            r"bound, $1/e$",
            r"conditioning, \ Bayes' theorem in odds form, \ the prosecutor's fallacy, \ Monty Hall's protocols",
            r"independence, \ pairwise and mutual; \ conditional independence",
            r"random variables and distribution functions; \ expectation, indicators, variance; \ St.\ Petersburg; "
            r"\ generating functions",
            r"what probability means: \ frequency, logic, belief, \ and the Dutch book",
        ], color=S.ACCENT, font_size=25)
        prereq = note(r"prerequisites: \ Part 1; \ high-school algebra").to_corner(DL, buff=0.3)
        code = code_block([
            "die = Dist.uniform(range(1, 7))",
            "(die ** 3).map(sum).P(10)        # 27/216, exactly",
            "(die ** 4).P(lambda r: 6 in r)   # 671/1296",
        ], font_size=24)
        built = label(r"Built in this part: \ an exact probability engine, \ checked against simulation",
                      font_size=30, color=S.ACCENT)
        bb = VGroup(built, code).arrange(DOWN, buff=0.45)
        with self.voiceover(
            "So this part asks: how do we reason exactly about what might happen? Part two: chance, counted. "
            "<bookmark mark='a'/> In this part: classical probability, from Cardano and "
            "Galileo to the Chevalier de Méré, and the counting it needs. Bertrand's paradox, and Kolmogorov's "
            "axioms with what follows from them. Conditioning; Bayes' theorem; a miscarriage of justice; and the "
            "Monty Hall problem, done properly. Independence. Random variables, expectation and variance, and "
            "generating functions. And the old argument about what probability means. <bookmark mark='b'/> Along "
            "the way we'll build an engine that computes probabilities on finite spaces exactly, as fractions, with "
            "no rounding at all, and we'll check every answer it gives against simulation."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("b")
            self.play(FadeOut(obj), FadeOut(prereq), FadeIn(bb, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
