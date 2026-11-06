from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Fitness(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Fitness and the Price equation", r"Is `survival of the fittest' a tautology?",
                            lit=(1970, 1979), part=PART)
        with self.voiceover("Chapter three. Fitness and the Price equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tautology()
        self.price()
        self.check()
        self.fisher()

    def tautology(self):
        head = label(r"Survival of the fittest", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the objection", r"who are the fittest? \ those who survive. \ So `the survivors survive': \ empty", BAD),
            (r"Popper \ (1974)", r"Darwinism is `a metaphysical research programme'; \ he withdrew the charge in 1978",
             GREY_A),
            (r"the propensity view", r"Mills and Beatty \ (1979): \ fitness is a \textit{disposition} to survive and "
                                     r"reproduce, \ like fragility", OK),
            (r"its point", r"the fitter twin can die first: \ actual success is evidence of fitness, \ not its "
                           r"definition", GENE),
            (r"the residue", r"expected offspring is not enough: \ variance and timing matter too \ (Gillespie; \ "
                             r"Beatty and Finsen)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.4)
        with self.voiceover(
            "Herbert Spencer's phrase, survival of the fittest, invites an objection. <bookmark mark='a'/>Who are the "
            "fittest? Those who survive. Then the principle says only that the survivors survive, which is empty. "
            "<bookmark mark='b'/>Karl Popper called Darwinism a metaphysical research programme on these grounds, "
            "and later withdrew the charge. <bookmark mark='c'/>The standard answer, from Susan Mills and John "
            "Beatty, is the propensity interpretation: fitness is a disposition to survive and reproduce, as "
            "fragility is a disposition to break. <bookmark mark='d'/>A fragile glass may survive and a sturdy one "
            "shatter; the fitter of two identical twins can be struck by lightning first. Actual success is evidence "
            "of fitness, not its definition. <bookmark mark='e'/>And the expected number of offspring is not the "
            "whole story: variance in offspring number, and timing, change which type spreads."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        hc = history_card(1970, r"George Price", r"`Selection and Covariance', \ \textit{Nature}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        eq = MathTex(r"\bar w\, \Delta \bar z", r"\;=\;", r"\mathrm{cov}(w_i, z_i)", r"\;+\;",
                     r"\mathrm{E}\big(w_i\, \Delta z_i\big)", font_size=42).next_to(hc, DOWN, buff=0.7).set_x(0)
        eq[0].set_color(WHITE)
        eq[2].set_color(ORG)
        eq[4].set_color(GENE)
        b1 = Brace(eq[2], DOWN, color=ORG)
        t1 = label(r"selection: \ traits that covary with fitness spread", font_size=19, color=ORG).next_to(b1, DOWN)
        b2 = Brace(eq[4], DOWN, color=GENE)
        t2 = label(r"transmission: \ offspring differ from parents", font_size=19, color=GENE).next_to(b2, DOWN)
        t2.shift(DOWN * 0.6)
        rows = stack([(r"$z_i$: \ parent $i$'s trait; \ \ $w_i$: \ its number of offspring; \ \ $\Delta z_i$: \ "
                       r"offspring mean minus parent", GREY_A),
                      (r"an identity: \ true of any population that reproduces, \ whatever the biology", GOAL),
                      (r"it holds at every level at once: \ the Wall's brick is built from it \ (Chapter 6)", GROUP)],
                     font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1970 George Price, an American chemist who taught himself genetics in London, published an "
            "equation that captures all of selection in one line. <bookmark mark='a'/>On the left, the change in "
            "a trait's population average from one generation to the next, scaled by mean fitness. "
            "<bookmark mark='b'/>The first term on the right is the covariance between parents' fitness and their "
            "trait: if fitter individuals have more of the trait, the trait spreads. This is selection. "
            "<bookmark mark='c'/>The second term is the fitness-weighted average change from parent to offspring: "
            "transmission, including mutation and imperfect inheritance. <bookmark mark='d'/>The equation is an "
            "identity. It holds for any population that reproduces, with no assumptions about the biology. "
            "<bookmark mark='e'/>Because it can be applied to individuals within groups and to groups within a "
            "population at once, it will become the tool for the levels-of-selection debate."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq[0]), Write(eq[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq[2]), GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("c")
            self.play(Write(eq[3]), Write(eq[4]), GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def check(self):
        d = load("price")
        head = label(r"The identity, \ checked on 500 birds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pts = d["points"]
        zs = [p[0] for p in pts]
        ws = [p[1] for p in pts]
        ax = Axes(x_range=[min(zs) - 0.2, max(zs) + 0.2, 1], y_range=[-0.5, max(ws) + 1, 2], x_length=6.0,
                  y_length=4.0, axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to(
            [-3.0, -0.4, 0])
        rng = np.random.default_rng(0)
        dots = VGroup(*[Dot(ax.c2p(z, w + rng.uniform(-0.25, 0.25)), radius=0.035, color=ORG, fill_opacity=0.7)
                        for z, w in pts])
        zm = float(np.mean(zs))
        wm = float(np.mean(ws))
        x0, x1 = min(zs), max(zs)
        line = Line(ax.c2p(x0, wm + d["slope"] * (x0 - zm)), ax.c2p(x1, wm + d["slope"] * (x1 - zm)), color=GOAL,
                    stroke_width=4)
        xl = label(r"wing length $z$", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"offspring $w$", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).shift(LEFT * 2.3)
        hd = [r"\text{term}", r"\text{value}"]
        rows = [[MathTex(r"\Delta \bar z", font_size=24), MathTex(f"{d['delta']:+.3f}", font_size=24)],
                [MathTex(r"\mathrm{cov}(w, z)/\bar w", font_size=24, color=ORG),
                 MathTex(f"{d['selection']:+.3f}", font_size=24, color=ORG)],
                [MathTex(r"\mathrm{E}(w \Delta z)/\bar w", font_size=24, color=GENE),
                 MathTex(f"{d['transmission']:+.3f}", font_size=24, color=GENE)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 1.8], cell_h=0.6, font_size=20).move_to([3.6, 0.8, 0])
        note = stack([(r"the two sides agree to $10^{-15}$", OK),
                      (r"the tilted cloud \textit{is} the covariance", GOAL),
                      (r"offspring are a little shorter: \ transmission pulls back", GENE)], font_size=19,
                     aligned_edge=LEFT, width=5.2).next_to(grid, DOWN, buff=0.4)
        assert d["identity_error"] < 1e-9
        with self.voiceover(
            "The Reasoner checks the identity on a simulated population. <bookmark mark='a'/>Five hundred birds, "
            "each with a wing length and a number of offspring; longer wings mean more offspring on average. "
            "<bookmark mark='b'/>The tilt of this cloud is the covariance between trait and fitness: selection "
            "pushes the average up by about point four five. <bookmark mark='c'/>But offspring wings are a little "
            "shorter than their parents', so transmission pulls back by about point one. <bookmark mark='d'/>The "
            "observed change in the average is the sum of the two, to fifteen decimal places, as it must be."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.005), run_time=2)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[1])),
                      FadeIn(note[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[2])), FadeIn(note[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[0])), FadeIn(note[0]))
        self.clear_scene()

    def fisher(self):
        d = load("fisher")
        head = label(r"Fisher's fundamental theorem", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        l1 = MathTex(r"\bar w \, \Delta \bar z = \mathrm{Cov}(w, z) + \mathrm{E}(w \, \Delta z)", font_size=34)
        l2 = MathTex(r"z = w: \quad \bar w \, \Delta \bar w = \mathrm{Var}(w) + \mathrm{E}(w \, \Delta w)",
                     font_size=34, color=ORG)
        l3 = MathTex(r"\Delta \bar w = \frac{\mathrm{Var}(w)}{\bar w} \ \ge \ 0", font_size=38, color=OK)
        eqs = VGroup(l1, l2, l3).arrange(DOWN, buff=0.28).move_to([-3.2, 1.0, 0])
        note3 = label(r"faithful transmission: \ $\Delta w = 0$", font_size=16, color=GREY_A).next_to(l3, RIGHT,
                                                                                                   buff=0.3)
        G = len(d["mean"])
        ax1 = Axes(x_range=[0, G, 10], y_range=[1.1, 1.55, 0.1], x_length=4.2, y_length=1.7,
                   axis_config={"color": GREY_B, "font_size": 14}, x_axis_config={"include_numbers": True},
                   y_axis_config={"include_numbers": True}).move_to([3.6, 1.45, 0])
        ax2 = Axes(x_range=[0, G, 10], y_range=[0, 0.05, 0.025], x_length=4.2, y_length=1.7,
                   axis_config={"color": GREY_B, "font_size": 14}, x_axis_config={"include_numbers": True},
                   y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 3}}).move_to(
            [3.6, -0.85, 0])
        c1 = series_plot(ax1, d["mean"], OK, width=3)
        c2 = series_plot(ax2, d["var"], ORG, width=3)
        t1 = label(r"mean fitness $\bar w$", font_size=16, color=OK).next_to(ax1, UP, buff=0.05)
        t2 = label(r"variance in fitness", font_size=16, color=ORG).next_to(ax2, UP, buff=0.05)
        ws = ", ".join(f"{x:g}" for x in d["w"])
        rows = stack([(r"three asexual types, \ fitness " + ws + r": \ the identity holds to $10^{-15}$", GREY_A),
                      (r"selection uses up the variance it feeds on", ORG),
                      (r"Price \ (1972), \ Ewens \ (1989): \ the theorem is about the \textit{partial} change; \ the "
                       r"environment deteriorates as others evolve", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=12.4).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "The Price equation contains a famous theorem as a special case. <bookmark mark='a'/>Take the trait to "
            "be fitness itself. <bookmark mark='b'/>Then the covariance becomes the variance in fitness. "
            "<bookmark mark='c'/>If offspring inherit their parents' fitness faithfully, the change in mean fitness "
            "is the variance divided by the mean, and a variance is never negative. This is Ronald Fisher's "
            "fundamental theorem of natural selection, from 1930: the rate of increase in fitness equals the "
            "genetic variance in fitness. <bookmark mark='d'/>The Reasoner iterates three asexual types. Mean "
            "fitness climbs towards that of the best type, <bookmark mark='e'/>while the variance first rises, as "
            "the best type becomes common, and then collapses: selection uses up the very variation it feeds on. "
            "<bookmark mark='f'/>Fisher's own statement was long misread as saying that mean fitness always "
            "increases. George Price, and later Warren Ewens, showed that it concerns only the partial change due "
            "to selection: the rest of the world, including other evolving species, keeps making the environment "
            "worse."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(l1))
            vo.wait_until("b")
            self.play(Write(l2))
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(note3))
            vo.wait_until("d")
            self.play(Create(ax1), FadeIn(t1), Create(c1), FadeIn(rows[0]), run_time=2)
            vo.wait_until("e")
            self.play(Create(ax2), FadeIn(t2), Create(c2), FadeIn(rows[1]), run_time=2)
            vo.wait_until("f")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
