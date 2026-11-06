from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

LEARN_C = {"nearest neighbour": OK, "majority": BLUEC, "always 0": GREY_B, "anti-majority": BAD}


def bit_cell(v, size=0.42, color=None) -> VGroup:
    sq = Square(side_length=size, stroke_color=GREY_C, stroke_width=1.2,
                fill_color=color or (FUT if v else "#1B2230"), fill_opacity=0.85 if v else 0.6)
    return VGroup(sq, MathTex(str(v), font_size=20, color=BLACK if v else GREY_B).move_to(sq))


class Lunch(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"No free lunch", r"Is any learner better than another?", lit=(1996,), part=PART)
        with self.voiceover("Chapter fourteen. No free lunch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.proof()
        self.average()
        self.pac()
        self.brick()
        self.bets()

    def proof(self):
        d = load("lunch")["slice"]
        head = label(r"Every world, \ weighed equally", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        setup = label(r"inputs: \ 3 bits, \ 8 of them; \ a `world' is any labelling: \ $2^8 = 256$ worlds",
                      font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        # training inputs and their labels
        tr = VGroup()
        for x, y in zip(d["train"], d["labels"]):
            tr.add(VGroup(MathTex(x, font_size=22, color=PAST), bit_cell(y)).arrange(DOWN, buff=0.1))
        tr.arrange(RIGHT, buff=0.25)
        trl = label(r"seen", font_size=20, color=PAST).next_to(tr, UP, buff=0.12)
        trg = VGroup(trl, tr).move_to([-4.6, 0.9, 0])
        # the test inputs and all 16 completions
        comps = VGroup()
        for c in d["completions"]:
            comps.add(VGroup(*[bit_cell(v, 0.3) for v in c]).arrange(RIGHT, buff=0.18))
        halves = [VGroup(*comps[:8]).arrange(DOWN, buff=0.06), VGroup(*comps[8:]).arrange(DOWN, buff=0.06)]
        VGroup(*halves).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        heads = VGroup()
        for hb in halves:
            cols = VGroup(*[MathTex(x, font_size=20, color=FUT) for x in d["test"]])
            for j, cm in enumerate(cols):
                cm.move_to([hb[0][j].get_x(), hb.get_top()[1] + 0.22, 0])
            heads.add(cols)
        cl = label(r"unseen: \ the 16 worlds that agree with what was seen", font_size=19, color=FUT).next_to(
            heads, UP, buff=0.12)
        block = VGroup(cl, heads, comps).move_to([1.9, -0.3, 0])
        pl = label(r"nearest neighbour predicts", font_size=19, color=OK).move_to([-4.0, -1.4, 0])
        pred_row = VGroup(*[bit_cell(v, 0.34) for v in d["pred"]]).arrange(RIGHT, buff=0.18).next_to(pl, DOWN,
                                                                                                    buff=0.15)
        counts = label(r"right, \ column by column: \ " + r", \ ".join(f"{k}/16" for k in d["correct"]),
                       font_size=20, color=GOAL).next_to(comps, DOWN, buff=0.15)
        foot = label(r"each unseen input: \ half the worlds say 1, \ half say 0: \ any guess is right half the time",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "David Wolpert's no free lunch theorem of 1996 is Hume's problem turned into a theorem. "
            "<bookmark mark='a'/>Take inputs of three bits: eight of them. A world is any way of labelling them, "
            "so there are two hundred and fifty six worlds. <bookmark mark='b'/>A learner sees the labels of four "
            "inputs. <bookmark mark='c'/>Which worlds agree with what it saw? Every way of labelling the other "
            "four: sixteen worlds. <bookmark mark='d'/>Now let the learner predict the unseen labels; here, nearest "
            "neighbour copies the label of the closest seen input. <bookmark mark='e'/>Look down any column. In "
            "exactly eight of the sixteen worlds the prediction is right. That is forced: half the consistent "
            "worlds say one there, and half say zero. <bookmark mark='f'/>So averaged over all worlds, any "
            "prediction on unseen inputs, by any learner, is right exactly half the time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(FadeIn(trg))
            vo.wait_until("c")
            self.play(FadeIn(cl), FadeIn(heads), LaggedStart(*[FadeIn(r) for r in comps], lag_ratio=0.08),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(pl), FadeIn(pred_row))
            vo.wait_until("e")
            anims = []
            for r, row in enumerate(comps):
                for j, cell in enumerate(row):
                    if d["completions"][r][j] == d["pred"][j]:
                        anims.append(cell[0].animate.set_stroke(OK, width=3))
                    else:
                        anims.append(cell.animate.set_opacity(0.3))
            self.play(*anims, run_time=1.5)
            self.play(FadeIn(counts))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def average(self):
        d = load("lunch")
        head = label(r"Four learners, \ two universes", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def panel(acc, title, x):
            base_y = -2.2
            g = VGroup()
            names = list(LEARN_C)
            for i, nm in enumerate(names):
                h = acc[nm] * 3.2
                b = Rectangle(width=0.7, height=max(h, 0.03), stroke_width=0, fill_color=LEARN_C[nm],
                              fill_opacity=0.85)
                b.move_to([x - 1.65 + i * 1.1, base_y + h / 2, 0])
                v = MathTex(f"{acc[nm]:.2f}", font_size=22, color=LEARN_C[nm]).next_to(b, UP, buff=0.08)
                g.add(VGroup(b, v))
            half = DashedLine([x - 2.3, base_y + 1.6, 0], [x + 2.3, base_y + 1.6, 0], color=GREY_B, stroke_width=1.5)
            t = label(title, font_size=21, color=WHITE).move_to([x, 1.75, 0])
            return g, half, t
        ga, ha, ta = panel(d["all"]["accuracy"], r"all 256 worlds", -3.4)
        gb, hb, tb = panel(d["smooth"]["accuracy"], r"a smooth universe: \ labels depend on the first bit", 3.4)
        leg = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                              label(n, font_size=18, color=c)).arrange(RIGHT, buff=0.1) for n, c in
                       LEARN_C.items()]).arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.25)
        foot = label(r"off the training set, \ a learner is only as good as its fit to the world it is in",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner checks the theorem by brute force. <bookmark mark='a'/>Four learners: nearest neighbour, "
            "majority vote, always say zero, and a perverse one that predicts the opposite of the majority. "
            "<bookmark mark='b'/>Over all two hundred and fifty six worlds, their accuracy on unseen inputs is "
            "exactly the same: one half, for every one of them, even the perverse one. <bookmark mark='c'/>Now "
            "restrict to a smooth universe, in which the label depends only on the first bit. "
            "<bookmark mark='d'/>Nearest neighbour is perfect, majority gets three quarters, always zero gets "
            "half, and the perverse learner a quarter. <bookmark mark='e'/>Off the training set, a learner is "
            "exactly as good as the match between its bias and the world it happens to be in."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(leg))
            vo.wait_until("b")
            self.play(FadeIn(ta), Create(ha), LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in ga], lag_ratio=0.2))
            self.play(*[FadeIn(g[1]) for g in ga])
            vo.wait_until("c")
            self.play(FadeIn(tb), Create(hb))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in gb], lag_ratio=0.2))
            self.play(*[FadeIn(g[1]) for g in gb])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def pac(self):
        d = load("lunch")["vc"]
        head = label(r"The other side: \ restrict the worlds, \ and get a guarantee", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        hc = label(r"Vapnik and Chervonenkis \ (1971); \ Valiant \ (1984): \ PAC learning", font_size=21,
                   color=HIST).next_to(head, DOWN, buff=0.2)

        def line_pts(labels, x0, y0, interval=None):
            g = VGroup(Line([x0 - 0.3, y0, 0], [x0 + 0.6 * len(labels) - 0.3, y0, 0], color=GREY_C,
                            stroke_width=2))
            for i, v in enumerate(labels):
                g.add(Dot([x0 + 0.6 * i, y0, 0], radius=0.09, color=OK if v == "1" else BAD))
            if interval is not None:
                a, b = interval
                g.add(Line([x0 + 0.6 * a - 0.2, y0 + 0.22, 0], [x0 + 0.6 * b + 0.2, y0 + 0.22, 0], color=FUT,
                           stroke_width=5))
            return g
        two = VGroup(line_pts("00", 0, 0), line_pts("10", 0, 0, (0, 0)), line_pts("01", 0, 0, (1, 1)),
                     line_pts("11", 0, 0, (0, 1))).arrange(RIGHT, buff=0.35).scale(1.15).move_to([-2.9, 0.7, 0])
        tl = label(r"intervals: \ 2 points, \ all 4 labellings", font_size=19, color=OK).next_to(two, UP, buff=0.12)
        three = line_pts("101", 0, 0).scale(1.35).move_to([3.6, 0.7, 0])
        x3 = label(r"3 points: \ `$+\,-\,+$' is impossible", font_size=19, color=BAD).next_to(three, UP, buff=0.12)
        hd = [r"\text{class}"] + [rf"k = {r['k']}" for r in d["intervals"]["rows"]] + [r"\text{VC dim}"]
        rows = []
        for nm in ("thresholds", "intervals"):
            rr = d[nm]["rows"]
            rows.append([label(nm, font_size=20, color=FUT)] +
                        [MathTex(rf"{r['made']}/{r['all']}", font_size=22, color=OK if r["made"] == r["all"] else
                                 BAD) for r in rr] + [MathTex(str(d[nm]["vc"]), font_size=24, color=GOAL)])
        grid = ValueGrid(hd, rows, col_w=[2.4, 1.2, 1.2, 1.2, 1.2, 1.6], cell_h=0.55, font_size=22).move_to(
            [0, -1.0, 0])
        thm = MathTex(r"\text{learnable} \iff \text{VC dim } d < \infty, \qquad m(\varepsilon, \delta) \approx "
                      r"\frac{d + \ln(1/\delta)}{\varepsilon}", font_size=30, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "No free lunch has a positive side. Restrict the worlds, and guarantees appear. This is the theory of "
            "Vladimir Vapnik and Alexey Chervonenkis, and Leslie Valiant's probably approximately correct learning. "
            "<bookmark mark='a'/>A class of hypotheses shatters a set of points if it can produce every labelling "
            "of them. Intervals on a line can produce all four labellings of two points. "
            "<bookmark mark='b'/>But not of three: no interval contains the outer two points and misses the middle "
            "one. <bookmark mark='c'/>The Reasoner counts, by brute force, the labellings each class can make. "
            "Thresholds shatter one point, intervals two: those are their VC dimensions. "
            "<bookmark mark='d'/>The fundamental theorem of statistical learning: a class can be learned, to "
            "accuracy epsilon with confidence one minus delta, from finitely many examples exactly when its VC "
            "dimension is finite, and the number of examples needed grows with that dimension. The guarantee holds "
            "in every world the class contains, and says nothing about the rest. That is the free lunch's price, "
            "paid in advance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t) for t in two], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(three), FadeIn(x3))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("d")
            self.play(Write(thm))
        self.clear_scene()

    def brick(self):
        w = wall(upto=15, current=15).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(15, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the fifteenth brick in the Wall. <bookmark mark='a'/>The dream: a justification of induction "
            "that needs no assumptions about the world. <bookmark mark='b'/>The wall: Hume's argument, Goodman's "
            "riddle, Gold's theorem, and now Wolpert's, which makes the point exact. Averaged over every possible "
            "world, no learner does better than any other off the data it has seen. <bookmark mark='c'/>What it "
            "forces: every learner, human or machine, bets on a kind of world. The bet can be good, and science is "
            "the history of good bets, but it is a bet, and the data alone cannot place it."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[15], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()

    def bets(self):
        head = label(r"What each learner bets on", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"nearest neighbour", r"nearby inputs have nearby labels \ (smoothness)", OK),
            (r"linear models", r"effects add up", BLUEC),
            (r"convolutional nets", r"local patterns, \ the same everywhere in the image", PAST),
            (r"Ockham, \ MDL, \ Solomonoff", r"the world is compressible", FUT),
            (r"Bayesians", r"the world is drawn from the prior", A_C),
            (r"science", r"laws: \ the same regularities here, \ there, \ and tomorrow", GOAL),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=23, color=c)
            y = label(b, font_size=21)
            x.move_to([-6.2 + x.width / 2, 1.7 - i * 0.78, 0])
            y.move_to([-1.6 + y.width / 2, 1.7 - i * 0.78, 0])
            g.add(VGroup(x, y))
        foot = label(r"no free lunch does not say learning fails: \ it says which bet you are making",
                     font_size=23, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So every learner bets on a world. <bookmark mark='a'/>Nearest neighbour bets on smoothness: nearby "
            "inputs have nearby labels. <bookmark mark='b'/>Linear models bet that effects add up. "
            "<bookmark mark='c'/>Convolutional networks bet on local patterns that look the same anywhere in an "
            "image. <bookmark mark='d'/>Ockham, MDL and Solomonoff bet that the world is compressible. "
            "<bookmark mark='e'/>A Bayesian bets the world was drawn from her prior. <bookmark mark='f'/>And science "
            "bets on laws: the same regularities here, there, and tomorrow. <bookmark mark='g'/>No free lunch does "
            "not say that learning fails. It says that every success is the success of a bet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
