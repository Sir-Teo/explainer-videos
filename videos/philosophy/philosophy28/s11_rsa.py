from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


def matrix(title, data, rows, cols, col, x, y, cw=1.25, ch=0.45, hi=None):
    t = label(title, font_size=20, color=col)
    grid = VGroup()
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            sq = Rectangle(width=cw, height=ch, stroke_width=1, stroke_color=GREY_D, fill_color=col,
                           fill_opacity=0.08 + 0.75 * float(v))
            sq.move_to([x + j * cw, y - i * ch, 0])
            num = MathTex(f"{v:.2f}", font_size=18).move_to(sq)
            grid.add(VGroup(sq, num))
    rl = VGroup(*[label(r_, font_size=15, color=GREY_A).next_to(grid[i * len(cols)], LEFT, buff=0.1)
                  for i, r_ in enumerate(rows)])
    cl = VGroup(*[label(c_, font_size=15, color=GREY_A).next_to(grid[j], UP, buff=0.1) for j, c_ in enumerate(cols)])
    t.next_to(cl, UP, buff=0.15).align_to(grid, LEFT)
    out = VGroup(t, grid, rl, cl)
    if hi is not None:
        i, j = hi
        out.add(SurroundingRectangle(grid[i * len(cols) + j], color=TRUTH, buff=0.02, stroke_width=3))
    return out


class RSA(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Rational speech acts, \ built", r"Can conversation be computed?", lit=(2012,),
                            part=PART)
        with self.voiceover("Chapter ten. Rational speech acts, built."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.model()
        self.reference()
        self.scalar()
        self.levels()
        self.reach()

    def model(self):
        head = label(r"Listeners and speakers, \ reasoning about each other", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"L_0(s \mid u) \;\propto\; [\![u]\!](s)\, P(s)", font_size=34, color=WORD),
            MathTex(r"S_1(u \mid s) \;\propto\; \exp\!\big(\alpha\,(\log L_0(s \mid u) - C(u))\big)", font_size=34,
                    color=USE),
            MathTex(r"L_1(s \mid u) \;\propto\; S_1(u \mid s)\, P(s)", font_size=34, color=HEAR),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-1.6, 0.4, 0])
        notes = VGroup(label(r"a literal listener: \ the states where $u$ is true", font_size=19, color=GREY_A),
                       label(r"a speaker: \ chooses $u$ to make $L_0$ guess $s$", font_size=19, color=GREY_A),
                       label(r"a pragmatic listener: \ Bayes on the speaker", font_size=19, color=GREY_A))
        for n_, e in zip(notes, eqs):
            n_.next_to(e, RIGHT, buff=0.4)
        foot = label(r"Frank and Goodman \ (2012): \ Grice's reasoning as recursive Bayesian inference", font_size=22,
                     color=HIST).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 2012 Michael Frank and Noah Goodman turned Grice's reasoning into a model you can compute: the "
            "Rational Speech Acts model. <bookmark mark='a'/>Start with a literal listener. Hearing an utterance u, "
            "she spreads her belief over the states where u is literally true, in proportion to their prior "
            "probability. <bookmark mark='b'/>Then a speaker. Wanting to convey a state s, she chooses among "
            "utterances in proportion to how well each would lead the literal listener to s, sharpened by a "
            "rationality parameter alpha, and discounted by cost. <bookmark mark='c'/>Then a pragmatic listener, who "
            "reasons about that speaker by Bayes' rule: which state would have made her say this? "
            "<bookmark mark='d'/>Each level reasons about the one below. Grice's maxims become consequences of a "
            "speaker trying to be understood."
        ) as vo:
            self.play(FadeIn(head))
            for mk, e, n_ in zip("abc", eqs, notes):
                vo.wait_until(mk)
                self.play(Write(e), FadeIn(n_))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def reference(self):
        d = load("reference")
        head = label(r"A reference game", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        objs = VGroup(VGroup(Square(0.6, color=WORD, fill_opacity=0.8)), VGroup(Circle(0.32, color=WORD, fill_opacity=0.8)),
                      VGroup(Square(0.6, color=OK, fill_opacity=0.8))).arrange(RIGHT, buff=0.6).move_to([-4.6, 2.1, 0])
        words, objects = d["words"], d["objects"]
        short = [r"blue sq.", r"blue circ.", r"green sq."]
        L0 = matrix(r"$L_0$: \ literal listener", d["L0"], words, short, WORD, -5.75, 0.6, cw=1.1)
        S1T = [list(x) for x in zip(*d["S1"])]                      # utterances x states, for display
        S1 = matrix(r"$S_1$: \ speaker \ (columns sum to 1)", S1T, words, short, USE, -1.6, 0.6, cw=1.1)
        L1 = matrix(r"$L_1$: \ pragmatic listener", d["L1"], words, short, HEAR, 2.8, 0.6, cw=1.1, hi=(0, 0))
        assert d["L1"][0][0] == 0.6 and d["L1"][0][1] == 0.4 and d["L0"][0][0] == 0.5
        foot = stack([(r"`blue', \ literally: \ either blue object, \ 50/50", WORD),
                      (r"but a speaker meaning the blue circle had a better word, \ `circle'", USE),
                      (r"so the pragmatic listener hears `blue' as the blue square: \ 0.60 to 0.40", HEAR)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the model on Frank and Goodman's kind of game. <bookmark mark='a'/>Three objects: a blue square, "
            "a blue circle, a green square. A speaker may say one word: blue, green, square or circle. "
            "<bookmark mark='b'/>The literal listener hearing blue has no reason to prefer either blue object: fifty "
            "fifty. <bookmark mark='c'/>The speaker. Wanting the blue circle, she could say blue, or circle, which "
            "picks it out uniquely; she says circle twice as often. Wanting the blue square, blue and square are "
            "equally good. <bookmark mark='d'/>The pragmatic listener reasons backwards: if the speaker had meant the "
            "blue circle, she would more likely have said circle. So hearing blue, she favours the blue square, sixty "
            "to forty. The Reasoner's numbers, and the direction people's choices go in Frank and Goodman's "
            "experiments."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(objs))
            vo.wait_until("b")
            self.play(FadeIn(L0), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(S1), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(L1), FadeIn(foot[2]))
        self.clear_scene()

    def scalar(self):
        d, a = load("scalar"), load("alphas")
        head = label(r"`Some', \ derived", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        states = [str(s) for s in d["states"]]
        L0 = matrix(r"$L_0$: \ literal", d["L0"], d["words"], states, WORD, -6.0, 1.4, cw=0.95)
        L1 = matrix(rf"$L_1$: \ pragmatic \ ($\alpha = {d['alpha']:g}$)", d["L1"], d["words"], states, HEAR, -1.6, 1.4,
                    cw=0.95, hi=(1, 3))
        some = d["L1"][1]
        assert some[3] < 0.01 and abs(some[1] - 0.497) < 0.001
        tag = label(r"states: \ how many of 3 cookies were eaten", font_size=17, color=GREY_A).next_to(L0, DOWN,
                                                                                                     buff=0.2).align_to(L0, LEFT)
        hd = [r"\alpha", r"L_1(\text{all 3} \mid \text{`some'})"]
        cells = [[MathTex(f"{r['alpha']:g}", font_size=22), MathTex(f"{r['p_all_given_some']:.4f}", font_size=22,
                                                                     color=HEAR)] for r in a["rows"]]
        grid = ValueGrid(hd, cells, col_w=[1.2, 3.0], cell_h=0.42, font_size=19).move_to([4.6, 0.6, 0])
        foot = stack([(r"literally, \ `some' is true of 1, \ 2 or 3: \ each $\tfrac13$", WORD),
                      (r"pragmatically, \ 3 nearly vanishes: \ a speaker who saw all 3 would have said `all'", HEAR),
                      (r"the more rational the speaker is assumed to be, \ the stronger the implicature", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the scalar implicature. <bookmark mark='a'/>Someone ate some of three cookies; the states are how many: "
            "none, one, two or three. The words: none, some, all. <bookmark mark='b'/>Literally, some is true if one, "
            "two or three were eaten; the literal listener gives each a third. <bookmark mark='c'/>The pragmatic "
            "listener, with a fairly rational speaker, gives three almost nothing: about six in a thousand. A speaker "
            "who saw all three eaten would have said all. Some has come to mean some but not all, with no change in "
            "its literal meaning. <bookmark mark='d'/>And the strength of the inference depends on how rational the "
            "listener takes the speaker to be: as alpha grows from a half to eight, the chance of all, given some, "
            "falls from fifteen percent to almost zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(L0), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(L1), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row],
                      FadeIn(foot[2]))
        self.clear_scene()

    def levels(self):
        d = load("levels")
        head = label(r"How deep does the reasoning go?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bs, sa = d["blue_square"], d["some_all"]
        assert bs[:3] == [0.5, 0.6, 0.6364] and abs(bs[6] - 0.6649) < 1e-4
        assert sa[:3] == [0.3333, 0.1111, 0.0476] and sa[6] < 0.003
        eq = MathTex(r"S_k(u \mid s) \propto L_{k-1}(s \mid u)^{\alpha}", r"\qquad",
                     r"L_k(s \mid u) \propto S_k(u \mid s)\, P(s)", font_size=30).move_to([0, 2.3, 0])
        eq[0].set_color(USE)
        eq[2].set_color(HEAR)

        def plot(vals, col, x, title):
            ax = Axes(x_range=[0, 6, 1], y_range=[0, 1, 0.25], x_length=4.8, y_length=2.8, tips=False,
                      axis_config={"color": GREY_B, "font_size": 16},
                      y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}}
                      ).move_to([x, -0.5, 0])
            xs = VGroup(*[MathTex(str(k), font_size=16, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                          for k in range(7)])
            xl = label(r"level $k$", font_size=16, color=GREY_A).next_to(xs, DOWN, buff=0.1)
            t = label(title, font_size=19, color=col).next_to(ax, UP, buff=0.2)
            pts = [ax.c2p(k, v) for k, v in enumerate(vals)]
            curve = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
            dots = VGroup(*[Dot(p, radius=0.06, color=col) for p in pts])
            return VGroup(ax, xs, xl, t), curve, dots

        A, ca, da = plot(bs, WORD, -3.4, r"reference game: \ $L_k(\text{blue square} \mid \text{`blue'})$")
        B, cb, db = plot(sa, HEAR, 3.4, r"cookies, \ $\alpha = 1$: \ $L_k(\text{all 3} \mid \text{`some'})$")
        foot = stack([(r"each level adds less: \ 0.5, \ 0.6, \ 0.64, \ \dots, \ 0.66; \ and `all' roughly halves at "
                       r"each step", GOAL),
                      (r"people differ: \ some reason literally, \ others a level deep or more \ (Franke and Degen, \ "
                       r"2016)", HIST)], font_size=19, aligned_edge=LEFT, width=12.0,
                     buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How deep does the reasoning go? <bookmark mark='a'/>The model can be iterated: a speaker who reasons "
            "about the pragmatic listener, a listener who reasons about that speaker, and so on, level after level. "
            "<bookmark mark='b'/>In the reference game, the credence that blue means the blue square rises from a "
            "half to point six at the first level, then to point six four, and then creeps up, toward about two "
            "thirds. <bookmark mark='c'/>In the cookie game, with a speaker of ordinary rationality, the credence "
            "that some means all three falls from a third to a ninth, then to under a twentieth, roughly halving at "
            "each further level. <bookmark mark='d'/>Each level adds less than the one before. "
            "<bookmark mark='e'/>Which level do people use? Fitting the model to individual participants in reference "
            "games, Michael Franke and Judith Degen found in 2016 that people differ: some reason literally, others a "
            "level deep or more. In the model, at least, the first step of reasoning about the other does most of "
            "the work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(A))
            self.play(Create(ca), LaggedStart(*[FadeIn(x) for x in da], lag_ratio=0.2), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(B))
            self.play(Create(cb), LaggedStart(*[FadeIn(x) for x in db], lag_ratio=0.2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def reach(self):
        head = label(r"What the model reaches", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"reference", r"which object a speaker means, \ in games like this one, \ predicted closely", WORD),
            (r"hyperbole", r"`it cost a million dollars': \ Kao and colleagues \ (2014) \ add the speaker's attitude "
                           r"to what is meant", USE),
            (r"politeness", r"speakers trade informativeness against kindness", HEAR),
            (r"the limits", r"the alternatives a speaker considers must be given in advance: \ where do they come "
                            r"from?", BAD),
            (r"Goodman and Frank \ (2016)", r"a review of the programme: \ pragmatics as probabilistic inference", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "The model has been extended in many directions. <bookmark mark='a'/>It predicts which object a speaker "
            "means in reference games like this one. <bookmark mark='b'/>Justine Kao and colleagues extended it in "
            "2014 to hyperbole: it cost a million dollars, understood as it cost a lot, and I'm annoyed. "
            "<bookmark mark='c'/>Others added politeness, as speakers trade being informative against being kind. "
            "<bookmark mark='d'/>Its main limit is that the alternatives a speaker considers, the utterances she might "
            "have said instead, must be given in advance. Where they come from is one of the open questions. "
            "<bookmark mark='e'/>Noah Goodman and Michael Frank reviewed the programme in 2016: pragmatic language "
            "understanding as probabilistic inference."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
