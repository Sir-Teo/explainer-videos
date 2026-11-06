from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Emergence(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Emergence", r"Can the whole do what no part does?", lit=(1925, 1970), part=PART)
        with self.voiceover("Chapter nine. Emergence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.broad()
        self.life()
        self.law()
        self.weak()

    def broad(self):
        head = label(r"British emergentism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Mill \ (1843)", r"`heteropathic' laws: \ chemical compounds have properties not predictable from their "
                               r"elements'", HIST),
            (r"Broad \ (1925)", r"\textit{The Mind and Its Place in Nature}: \ emergent properties obey trans-ordinal "
                                r"laws, \ not deducible even in principle", MIND),
            (r"the eclipse", r"quantum mechanics explained chemical bonding: \ chemistry's flagship example of "
                             r"emergence was reduced", BAD),
            (r"the survivor", r"the mind: \ Broad thought consciousness the likeliest case", FEEL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Perhaps minds are emergent: features of wholes that no part has. <bookmark mark='a'/>John Stuart Mill, "
            "in 1843, noted that chemical compounds have properties not predictable from those of their elements. "
            "<bookmark mark='b'/>C. D. Broad, in 1925, made it a theory: emergent properties obey trans-ordinal laws, "
            "linking one level to the next, that could not be deduced even in principle from complete knowledge of "
            "the lower level. <bookmark mark='c'/>Within a decade quantum mechanics had explained the chemical bond, "
            "and chemistry, emergentism's flagship example, had been reduced. <bookmark mark='d'/>The case that "
            "survived was the mind. To see what emergence could still mean, consider a world whose laws we know "
            "completely."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def life(self):
        d = load("life")
        head = label(r"Conway's Life: \ a glider gun firing", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["gens"] == 150 and d["frames_every"] == 3 and d["glider_c4"] and d["gliders_out"] == 4
        W, Hh = d["w"], d["h"]
        cs = 0.105
        ox, oy = -6.2 + cs / 2, 2.6

        def P(x, y):
            return np.array([ox + x * cs, oy - y * cs, 0])

        board = Rectangle(width=W * cs, height=Hh * cs, color=GREY_D, stroke_width=1).move_to(
            P((W - 1) / 2, (Hh - 1) / 2))

        def cells(frame):
            return VGroup(*[Square(side_length=cs * 0.92, stroke_width=0, fill_color=FUNC, fill_opacity=0.95).move_to(
                P(x, y)) for x, y in frame])

        rules = stack([(r"a dead cell with exactly 3 live neighbours is born", OK),
                       (r"a live cell with 2 or 3 survives; \ all others die", BAD),
                       (r"Gosper's gun \ (1970): \ a new glider every 30 generations", FUNC),
                       (r"a glider moves one cell diagonally every 4 generations", SYM),
                       (r"after 150 generations: \ 4 gliders in flight", GOAL)], font_size=19, aligned_edge=LEFT,
                      width=4.4, buff=0.3).move_to([4.6, 0.2, 0])
        gen = label(r"generation 0", font_size=18, color=GREY_A).next_to(board, DOWN, buff=0.15)
        frames = d["frames"]
        with self.voiceover(
            "In 1970 John Conway invented a universe with two rules, published by Martin Gardner in Scientific "
            "American. <bookmark mark='a'/>Space is a grid of cells, each alive or dead, and time goes in steps. A "
            "dead cell with exactly three live neighbours comes alive. <bookmark mark='b'/>A live cell with two or "
            "three live neighbours survives; every other cell dies. That is the whole physics. "
            "<bookmark mark='c'/>Here is a pattern found by Bill Gosper the same year. Watch it run. "
            "<bookmark mark='d'/>Every thirty generations it emits a small shape, a glider, that travels away across "
            "the grid, one cell diagonally every four generations, keeping its shape. "
            "<bookmark mark='e'/>After a hundred and fifty generations, four gliders are in flight. Nothing in the "
            "rules mentions guns, gliders or motion. They are only cells being born and dying."
        ) as vo:
            self.play(FadeIn(head), Create(board))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            cur = cells(frames[0])
            self.play(FadeIn(cur), FadeIn(gen))
            for k, fr in enumerate(frames[1:], start=1):
                nxt = cells(fr)
                ng = label(rf"generation {k * d['frames_every']}", font_size=18, color=GREY_A).move_to(gen)
                self.remove(cur, gen)
                self.add(nxt, ng)
                cur, gen = nxt, ng
                self.wait(0.3)
                if k == 15:
                    self.play(FadeIn(rules[2]), run_time=0.4)
                if k == 25:
                    self.play(FadeIn(rules[3]), run_time=0.4)
            vo.wait_until("e")
            self.play(FadeIn(rules[4]))
        self.clear_scene()

    def law(self):
        d = load("law")
        head = label(r"A law about gliders, \ found by running the rules", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert d["gens"] == 600 and d["holds"] == d["points"] == 21
        assert d["rows"][-1]["pop"] == 136 and d["rows"][-1]["outside"] == 95
        ax = Axes(x_range=[0, 600, 100], y_range=[0, 160, 40], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to([-2.5, -0.4, 0])
        xl = label(r"generation", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"live cells", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.15)
        curve = VMobject(color=FUNC, stroke_width=2).set_points_as_corners(
            [ax.c2p(t, p) for t, p in enumerate(d["pop"])])
        line = DashedLine(ax.c2p(0, 36), ax.c2p(600, 136), color=SYM)
        dots = VGroup(*[Dot(ax.c2p(r["gen"], r["pop"]), radius=0.06, color=SYM) for r in d["rows"]])
        law = MathTex(r"N(30k) \;=\; 36 + 5k", font_size=36, color=SYM).move_to([4.4, 1.4, 0])
        ll = label(r"exact at all 21 checks, \ $k = 0, \dots, 20$", font_size=19, color=OK).next_to(law, DOWN,
                                                                                                     buff=0.2)
        side = stack([(r"a law about guns and gliders, \ which the two rules never mention", GOAL),
                      (r"entailed by the rules, \ but found by running them", FUNC)], font_size=19,
                     width=4.4, buff=0.3).move_to([4.4, -1.0, 0])
        with self.voiceover(
            "The gun obeys a law of its own. <bookmark mark='a'/>The Reasoner runs it for six hundred "
            "generations, on a board large enough for every glider to fly free, and counts the live cells at each "
            "one. The count wobbles through every thirty-generation cycle. <bookmark mark='b'/>But at every "
            "thirtieth generation it lands on a straight line: thirty six cells, plus five for each glider fired. "
            "<bookmark mark='c'/>At generation six hundred there are one hundred and thirty six live cells, ninety "
            "five of them in the nineteen gliders already clear of the gun. The law holds at all twenty one checks. "
            "<bookmark mark='d'/>It is a law about guns and gliders, as exact as any law of chemistry, about things "
            "the two rules never mention. <bookmark mark='e'/>And the rules entail it, but nothing in the rules, "
            "inspected, says thirty: the Reasoner found it by running them. The next idea gives that a name."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=4)
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.05))
            self.play(FadeIn(law))
            vo.wait_until("c")
            self.play(FadeIn(ll))
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            vo.wait_until("e")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def weak(self):
        head = label(r"Weak and strong emergence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"weak \ (Bedau, \ 1997)", r"a macro-property derivable from the micro-dynamics, \ but only by "
                                        r"simulation: \ the glider", FUNC),
            (r"undecidable", r"Life can run any computation: \ whether a pattern ever dies out cannot in general be "
                             r"decided", SYM),
            (r"strong", r"not derivable from the low-level facts even in principle \ (Chalmers, \ 2006): \ "
                        r"consciousness, \ if anything", FEEL),
            (r"for the mind", r"weak emergence is compatible with physicalism; \ strong emergence is a new kind of "
                              r"law, \ and meets the exclusion problem head on", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Mark Bedau, in 1997, used worlds like this to define weak emergence. <bookmark mark='a'/>A macro-property "
            "is weakly emergent if it is derivable from the micro-dynamics, but only by simulation: there is no "
            "shortcut, you have to run it. The glider is a perfect example. <bookmark mark='b'/>In Life the lack of "
            "shortcuts is a theorem. Life can carry out any computation, so whether a pattern will ever die out is, "
            "in general, undecidable. <bookmark mark='c'/>Strong emergence is more: a property not derivable from the "
            "low-level facts even in principle. David Chalmers has argued that consciousness is the only clear "
            "candidate. <bookmark mark='d'/>Weak emergence sits comfortably with physicalism. Strong emergence would "
            "be a new kind of law, and it runs straight into the exclusion problem of chapter eight."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
