from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403

NAMES = {"deworming": r"deworming", "cash": r"cash transfers", "nets": r"bed nets", "tutoring": r"remedial tutoring",
         "credit": r"microcredit", "graduation": r"graduation"}
COLS = {"deworming": HEALTH, "cash": CASH, "nets": POOR, "tutoring": SCHOOL, "credit": CREDIT, "graduation": TRAP}


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ spend the aid budget", r"Where should ten million dollars go?",
             "Chapter two. Play it: spend the aid budget.", lit={2025: r"GiveWell"}, scale=("nation",),
             horizon=("a year",))
        self.menu()
        self.ask()
        self.reveal()
        self.rule()

    def menu(self):
        A = load("aid")
        ax = plane([0, 6], [0, 12], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.8,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 4, 8, 12], xlabel=r"millions of dollars spent",
                   ylabel=r"thousands of healthy years", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        curves, names = VGroup(), VGroup()
        ends = {}
        for k in A["programmes"]:
            ys = A["curves"][k]
            curves.add(path(ax, A["xs"], ys, COLS[k], 3.0))
            ends[k] = ax.ax.c2p(6, ys[-1])[1]
        # spread the end labels so that none overlap (at least 0.27 apart), keeping their order
        order = sorted(ends, key=lambda k: ends[k])
        ypos, last = {}, -1e9
        for k in order:
            ypos[k] = max(ends[k], last + 0.27)
            last = ypos[k]
        for k in A["programmes"]:
            names.add(label(NAMES[k], font_size=15, color=COLS[k]).move_to(
                np.array([ax.ax.c2p(6, 0)[0] + 0.15, ypos[k], 0]), aligned_edge=LEFT))
        side = VGroup(
            label(r"the Island's six \\ programmes, \ measured \\ in one unit", font_size=19, color=WHITE),
            label(r"the slope at zero: \\ what the first \\ million buys", font_size=19, color=GREY_A),
            label(r"each curve flattens: \\ the easiest cases \\ are reached first", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. You run the Island's aid agency, with ten million dollars to spend this year, and six "
            "programmes to spend it on. <bookmark mark='a'/> Each curve shows what a programme achieves as you "
            "spend more on it, measured in one common unit, thousands of years of healthy life. Deworming, cash "
            "transfers, bed nets, remedial tutoring, microcredit, and a graduation programme for the poorest. "
            "<bookmark mark='b'/> The steepness at the start is what the first million buys. Bed nets are the "
            "steepest. <bookmark mark='c'/> But every curve flattens. The first nets go to the villages with the "
            "most malaria; the next million reaches places where it does less good."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(n)) for c, n in zip(curves, names)],
                                  lag_ratio=0.4), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(names[2], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def ask(self):
        head = label(r"Your turn: \ ten million dollars", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        plans = VGroup(
            label(r"A. \ all of it on the best programme: \ bed nets", font_size=26, color=POOR),
            label(r"B. \ an equal share to each: \ \$1.67 million apiece", font_size=26, color=GREY_A),
            label(r"C. \ your own split", font_size=26, color=YOU),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 0.4)
        ring = countdown().scale(0.6).next_to(plans, DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Three plans. <bookmark mark='a'/> Plan A: put all ten million into the best programme, bed nets. "
            "<bookmark mark='b'/> Plan B: spread it evenly, one and two-thirds million to each. "
            "<bookmark mark='c'/> Plan C: your own split. Pause, and decide where your money goes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(plans[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(plans[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(plans[2], shift=RIGHT * 0.2), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        A = load("aid")
        rows = [(r"A. \ all on nets", A["all_first"], POOR), (r"B. \ equal shares", A["even"], GREY_B),
                (r"the best split", A["best"], GAIN)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            y = 2.2 - 0.95 * i
            w = v / 20 * 7.5
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-3.4 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=col).next_to(np.array([-3.6, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{v:.1f}", font_size=22, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        alloc = VGroup()
        x0 = -3.4
        for k in A["programmes"]:
            m = A["alloc"][k]
            if m <= 0:
                continue
            w = m / 10 * 7.5
            r = Rectangle(width=w, height=0.55, stroke_color=BLACK, stroke_width=1.5, fill_color=COLS[k],
                          fill_opacity=0.85).move_to(np.array([x0 + w / 2, -1.6, 0]))
            alloc.add(VGroup(r, label(rf"{NAMES[k]} \\ \${m:.1f}m", font_size=13, color=WHITE).next_to(r, DOWN,
                                                                                                    buff=0.1)))
            x0 += w
        ah = label(r"the best split of the ten million", font_size=19, color=GAIN).move_to(np.array([0.35, -0.95, 0]))
        none = label(r"microcredit: \ \$0", font_size=16, color=CREDIT).next_to(alloc, RIGHT, buff=0.3)
        head = label(r"thousands of healthy years bought", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here is what each plan buys. <bookmark mark='a'/> Plan A, everything on nets: {A['all_first']:.1f} "
            "thousand healthy years. The nets run out of good places to go long before the money runs out. "
            f"<bookmark mark='b'/> Plan B, equal shares: {A['even']:.1f}. Spreading the money does far better. "
            f"<bookmark mark='c'/> The best split buys {A['best']:.1f}. <bookmark mark='d'/> It funds five "
            "programmes, in different amounts, and gives nothing to microcredit, whose first million buys less "
            "than the last million spent anywhere else. How close did your own split come?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b[0]) for b in bars])
            for mk, b in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(ah), LaggedStart(*[FadeIn(a, shift=UP * 0.1) for a in alloc], lag_ratio=0.3),
                      FadeIn(none), run_time=2.5)
        self.clear_scene()

    def rule(self):
        A = load("aid")
        eq = MathTex(r"\frac{\partial B_{\text{nets}}}{\partial \$} = \frac{\partial B_{\text{cash}}}{\partial \$} = "
                     r"\cdots = \lambda", font_size=44, color=THEORY).move_to(UP * 1.9)
        rows = VGroup()
        for i, k in enumerate(A["programmes"]):
            m = A["marginal_at_best"][k]
            txt = (rf"{NAMES[k]}: \ its first million buys {m:.2f}, \ so it gets nothing" if A["alloc"][k] == 0
                   else rf"{NAMES[k]}: \ the last million buys {m:.2f}")
            rows.add(label(txt, font_size=21, color=COLS[k]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(eq, DOWN, buff=0.55)
        foot = label(r"cost-effectiveness at the margin, \ not on average: \ GiveWell calls it \emph{room for more "
                     r"funding}", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The rule behind the best split is Part five's, applied to a budget. <bookmark mark='a'/> Keep moving "
            "money to whichever programme buys the most with its next dollar, until the next dollar buys the same "
            "everywhere it is spent. <bookmark mark='b'/> At the best split, the last million spent on each funded "
            f"programme buys about {A['marginal_at_best']['nets']:.2f} thousand years. Microcredit's very first "
            f"million buys only {A['marginal_at_best']['credit']:.2f}, so it gets nothing. <bookmark mark='c'/> "
            "The lesson is that cost-effectiveness is a number at the margin, not an average. The charity evaluator "
            "GiveWell asks not only how much good a charity does per dollar, but how much more money it could use "
            "as well: its room for more funding. The rest of this part is about what goes into curves like these, "
            "and how anyone could measure them."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(eq, color=WHITE), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows],
                                                             lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Indicate(r_, color=WHITE, scale_factor=1.03) for r_ in rows])
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
