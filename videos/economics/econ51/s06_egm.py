from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Egm(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The endogenous grid method", r"Can the Euler equation be solved without searching?",
             "Chapter five. The endogenous grid method.", lit={2006: r"Carroll"}, scale=("household",),
             horizon=("a lifetime",))
        self.problem()
        self.trick()
        self.rules()
        self.race()

    def problem(self):
        eqs = VGroup(
            MathTex(r"a' = R\,a + y - c \;\ge\; 0", font_size=40, color=WHITE),
            MathTex(r"u'(c) \;=\; \beta R\, \mathbb{E}\big[\,u'(c')\,\big] \quad\text{unless the limit binds}",
                    font_size=40, color=THEORY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 1.6)
        H = TRUTH["household"]
        notes = VGroup(
            label(rf"the household of Part 22: \ income follows a persistent chain \ ($\rho = {H['rho']}$), \ "
                  rf"no borrowing, \ $\beta = {H['beta']}$, \ $R = {H['R']}$", font_size=20, color=GREY_A),
            label(r"the usual way: \ at every asset level, \ every round, \ search for the $c$ that solves the "
                  r"equation", font_size=21, color=VFI),
            label(r"a root to find at each of 1,000 points, \ hundreds of rounds over".replace(",", "{,}"),
                  font_size=21, color=ERR),
        ).arrange(DOWN, buff=0.35).next_to(eqs, DOWN, buff=0.6)
        with self.voiceover(
            "The household of Part twenty-two: it earns an income that moves persistently up and down, saves at "
            "a fixed return, and cannot borrow. <bookmark mark='a'/> Its assets next year are this year's, with "
            "interest, plus income, minus consumption, and must not fall below zero. <bookmark mark='b'/> Its rule "
            "is the Euler equation: the marginal utility of consuming today equals beta times R times the expected "
            "marginal utility tomorrow, unless the borrowing limit binds. <bookmark mark='c'/> The usual way to "
            "solve it: at every level of assets, search for the consumption that makes the equation hold, <bookmark "
            "mark='d'/> a root to find at every grid point, in every one of hundreds of rounds."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def trick(self):
        chain = flow_chain([(r"choose $a'$ \\ on the grid", GRID), (r"$\beta R\,\mathbb{E}[u'(c')]$ \\ is known",
                                                                    VALUE),
                            (r"$c = (\beta R\,\mathbb{E}u')^{-1/\gamma}$", EGM), (r"$a = (c + a' - y)/R$", POLICY),
                            (r"interpolate \\ back to the grid", WHITE)],
                           box_w=2.25, box_h=1.1, buff=0.4, font_size=19,
                           notes=[r"the grid is for \\ next year's assets", r"from last \\ round's rule",
                                  r"invert $u'$: \\ no search", r"the budget says \\ where it came from",
                                  r"below the first \\ point, \ eat it all"], note_size=15)
        chain.move_to(UP * 0.6)
        foot = label(r"the grid of today's assets is found, \ not chosen: \ endogenous", font_size=23,
                     color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Carroll, \ Economics Letters (2006)", corner=DR, font_size=12)
        with self.voiceover(
            "Christopher Carroll's trick, published in 2006, turns the problem around. <bookmark mark='a'/> Put "
            "the grid on next year's assets instead of this year's. <bookmark mark='b'/> Then the right-hand side "
            "of the Euler equation, which depends only on next year, is known from last round's consumption rule. "
            "<bookmark mark='c'/> Inverting marginal utility gives today's consumption directly: no search, just a "
            "power. <bookmark mark='d'/> The budget then says what assets today lead to that choice: a equals c "
            "plus a prime minus y, over R. <bookmark mark='e'/> Those assets fall wherever they fall, so the rule "
            "is interpolated back onto the grid; below the first of them the borrowing limit binds, and the "
            "household consumes everything it has. <bookmark mark='f'/> Today's grid is found, not chosen, which "
            "is where the name comes from."
        ) as vo:
            self.play(FadeIn(tag))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                if i == 0:
                    self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
                else:
                    self.play(GrowArrow(chain.arrows[i - 1]), FadeIn(chain.boxes[i]), FadeIn(chain.notes[i]),
                              run_time=0.9)
            vo.wait_until("f")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def rules(self):
        Hh = load("household")
        a = np.array(Hh["a"])
        c = np.array(Hh["egm_c"])
        y = Hh["y"]
        ax = plane([0, 10], [0, 2.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                   xlabel=r"assets at the start of the year \ (mean income = 1)", ylabel=r"consumption",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        idx = (0, len(y) // 2, len(y) - 1)
        cols = (ERR, EGM, POLICY)
        curves = VGroup(*[path(ax, a, c[:, s], col, 2.8) for s, col in zip(idx, cols)])
        eat = path(ax, a, a * TRUTH["household"]["R"] + y[0], GREY_B, 1.4, yr=(0, 2.5))
        eat = DashedVMobject(eat, num_dashes=30)
        names = VGroup(*[label(t, font_size=17, color=col) for t, col in zip(
            (rf"lowest income \ ({y[0]:.2f})", r"middle income \ (1.00)", rf"highest income \ ({y[-1]:.2f})"),
            cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        side = VGroup(
            label(r"dashed: \ eat everything \\ (the lowest income)", font_size=17, color=GREY_B),
            label(r"near zero assets \\ the limit binds: \\ the rule follows \\ the dashed line, \\ then bends away",
                  font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        with self.voiceover(
            "Here are the rules it finds, for the lowest, middle and highest of five income levels. <bookmark "
            "mark='a'/> With the lowest income and little wealth, the household consumes everything it has: the "
            "rule lies on the dashed line, because the borrowing limit binds. <bookmark mark='b'/> With more "
            "wealth it starts to save, and the rule bends away. <bookmark mark='c'/> Higher income lifts the whole "
            "rule, by less than the income, because some of a good year is saved for bad ones."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(names[0]), Create(eat), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(curves[0], color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(names[1:]), run_time=1.8)
        self.clear_scene()

    def race(self):
        Hh = load("household")
        rows = Hh["vfi"]
        ax = plane([-2.2, 0.6], [-3.5, 0], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[-2, -1, 0], yticks=[-3, -2, -1, 0], xlabel=r"seconds, \ $\log_{10}$",
                   ylabel=r"worst Euler error, \ $\log_{10}$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        xs = [np.log10(r["seconds"]) for r in rows]
        ys = [r["ee"] for r in rows]
        line = path(ax, xs, ys, VFI, 2.4, smooth=False)
        vd = VGroup(*[VGroup(dot(ax, x, yv, VFI, 0.08),
                             label(rf"{r['n']}", font_size=14, color=VFI).next_to(ax.ax.c2p(x, yv), UR, buff=0.08))
                      for x, yv, r in zip(xs, ys, rows)])
        ex, ey = np.log10(Hh["egm_seconds"]), Hh["egm_ee"]
        ed = dot(ax, ex, ey, EGM, 0.12)
        el = label(r"endogenous grid, \ 200 points", font_size=16, color=EGM).next_to(ed, RIGHT, buff=0.15)
        last = rows[-1]
        side = VGroup(
            label(r"blue: \ value iteration \\ on grids of 100 to 800", font_size=18, color=VFI),
            label(rf"{last['n']} points: \ {last['seconds'] / Hh['egm_seconds']:.0f} times as long, \\ and "
                  rf"{10 ** (last['ee'] - Hh['egm_ee']):.0f} times less accurate", font_size=18, color=WHITE),
            label(r"lower and further left \\ is better", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "How much faster is it? Plot each method by the time it takes and the worst error it leaves, both on "
            "log scales, so lower and further left is better. <bookmark mark='a'/> Value iteration on grids of a "
            "hundred to eight hundred points: each doubling of the grid costs four times the time and buys only a "
            "little accuracy. <bookmark mark='b'/> The endogenous grid method, with two hundred points, sits far "
            f"below and to the left. <bookmark mark='c'/> Against value iteration with {last['n']} points it is "
            f"{last['seconds'] / Hh['egm_seconds']:.0f} times as fast and "
            f"{10 ** (last['ee'] - Hh['egm_ee']):.0f} times as accurate. Extending the blue line, value iteration "
            "would need a grid more than a hundred times finer to match it, and more memory than a laptop has."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in vd], lag_ratio=0.3), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ed, scale=1.5), FadeIn(el))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), Indicate(ed, color=WHITE, scale_factor=1.6))
        self.clear_scene()
