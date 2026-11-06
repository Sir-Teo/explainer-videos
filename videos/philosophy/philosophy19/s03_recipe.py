from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Recipe(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The recipe for selection", r"What does natural selection need?", lit=(1970, 1984),
                            part=PART)
        with self.voiceover("Chapter two. The recipe for selection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lewontin()
        self.breeder()
        self.sieve()
        self.drift()
        self.drift_debate()

    def lewontin(self):
        hc = history_card(1970, r"Richard Lewontin", r"`The Units of Selection'", width=5.2, color=HIST).to_corner(
            UL, buff=0.35)
        items = [(r"1. \ variation", r"individuals differ in a trait", ORG),
                 (r"2. \ heredity", r"offspring resemble their parents in it", GENE),
                 (r"3. \ differential fitness", r"the trait affects survival or reproduction", ALT)]
        boxes = VGroup()
        for t, s, c in items:
            b = RoundedRectangle(width=3.8, height=1.3, corner_radius=0.15, color=c, stroke_width=2.5)
            tx = VGroup(label(t, font_size=22, color=c), label(s, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.12)
            boxes.add(VGroup(b, tx.move_to(b)))
        boxes.arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
        out = label(r"then the trait's distribution changes: \ evolution by natural selection, \ for \textit{any} "
                    r"entities that meet the three", font_size=21, color=GOAL).next_to(boxes, DOWN, buff=0.5)
        more = label(r"genes, \ cells, \ organisms, \ groups, \ species, \ computer programs", font_size=20,
                     color=GREY_A).next_to(out, DOWN, buff=0.25)
        with self.voiceover(
            "Richard Lewontin distilled natural selection into a recipe with three ingredients. "
            "<bookmark mark='a'/>Variation: individuals differ in some trait. <bookmark mark='b'/>Heredity: offspring "
            "resemble their parents in that trait. <bookmark mark='c'/>Differential fitness: the trait makes a "
            "difference to survival or reproduction. <bookmark mark='d'/>Whenever all three hold, the distribution of "
            "the trait changes from generation to generation. <bookmark mark='e'/>Nothing in the recipe mentions "
            "organisms. It applies to anything that meets the three conditions: genes, cells, groups, species, and "
            "even computer programs, a point that returns when we ask at what level selection acts."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, b in zip("abc", boxes):
                vo.wait_until(mk)
                self.play(FadeIn(b))
            vo.wait_until("d")
            self.play(FadeIn(out))
            vo.wait_until("e")
            self.play(FadeIn(more))
        self.clear_scene()

    def breeder(self):
        d = load("breeder")
        head = label(r"Selection without heredity does nothing", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        keys = sorted(d, key=lambda k: d[k]["h2"])
        gens = len(d[keys[0]]["means"])
        top = max(max(d[k]["means"]) for k in keys)
        ax = Axes(x_range=[0, gens - 1, 1], y_range=[-0.5, top + 0.5, 2], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.6, -0.3, 0])
        cols = [SELF, ORG, GENE]
        curves = VGroup(*[series_plot(ax, d[k]["means"], c, width=4) for k, c in zip(keys, cols)])
        labs = VGroup(*[label(r"$h^2 = " + f"{d[k]['h2']:.1f}" + r"$", font_size=18, color=c).next_to(
            ax.c2p(gens - 1, d[k]["means"][-1]), RIGHT, buff=0.1) for k, c in zip(keys, cols)])
        xl = label(r"generation", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"mean trait \ (in standard deviations)", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        eq = MathTex(r"R = h^2 S", font_size=40, color=GOAL).move_to([3.8, 1.6, 0])
        side = stack([(r"keep the top 30\% each generation", WHITE),
                      (r"$h^2$: \ the share of variation that is inherited", GREY_A),
                      (r"$S$: \ selection differential; \ \ $R$: \ response", GREY_A)] +
                     [(r"$h^2 = " + f"{d[k]['h2']:.1f}" + r"$: \ response " + f"{d[k]['response']:.2f}" +
                       r" per generation \ (predicted " + f"{d[k]['predicted']:.2f}" + r")", c)
                      for k, c in zip(keys, cols)], font_size=19, aligned_edge=LEFT, width=5.4).next_to(eq, DOWN,
                                                                                                       buff=0.4)
        with self.voiceover(
            "The Reasoner shows why heredity matters. <bookmark mark='a'/>Four thousand individuals with a trait "
            "that is part genetic, part environmental. Each generation, only the top thirty percent breed. "
            "<bookmark mark='b'/>If none of the variation is inherited, selection is as strong as ever, and nothing "
            "changes: the offspring regress all the way back to the mean. <bookmark mark='c'/>If half of it is "
            "inherited, the mean climbs steadily; if nine tenths, faster still. <bookmark mark='d'/>The breeder's "
            "equation predicts the response: heritability times the selection differential. The simulation agrees "
            "with it closely. Selection is a sieve; heredity is what lets the sieve's results accumulate."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(labs[0]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(labs[1]), FadeIn(labs[2]), FadeIn(side[4]),
                      FadeIn(side[5]), run_time=2)
            vo.wait_until("d")
            self.play(Write(eq))
        self.clear_scene()

    def sieve(self):
        hc = history_card(1984, r"Elliott Sober", r"\textit{The Nature of Selection}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        box = Rectangle(width=4.4, height=1.6, color=GREY_B).move_to([-3.4, 0.8, 0])
        grid = VGroup(*[Line([-5.4 + 0.5 * i, -0.4, 0], [-5.4 + 0.5 * i, -0.2, 0], color=GREY_B) for i in range(9)],
                      Line([-5.6, -0.3, 0], [-1.2, -0.3, 0], color=GREY_B, stroke_width=4))
        rng = np.random.default_rng(3)
        balls = VGroup()
        for i in range(12):
            small = i % 2 == 0
            col = ALT if small else ORG
            r = 0.12 if small else 0.24
            balls.add(Dot([-5.2 + 0.36 * i, 0.4 + 0.5 * rng.random(), 0], radius=r, color=col))
        rows = stack([(r"a toy: \ balls of different sizes and colours shaken through a sieve", WHITE),
                      (r"all small balls are pink, \ all large ones orange", GREY_A),
                      (r"pink balls pass: \ there is selection \textit{of} pink balls", ALT),
                      (r"but selection \textit{for} small size: \ size is what causes passing", GENE),
                      (r"fitness correlations do not reveal what is selected for: \ a causal question \ (Part 17)", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.6).move_to([3.2, -0.4, 0])
        with self.voiceover(
            "Elliott Sober's toy separates two ideas. <bookmark mark='a'/>A box of balls of different sizes and "
            "colours is shaken over a sieve. <bookmark mark='b'/>As it happens, all the small balls are pink and "
            "all the large ones orange. <bookmark mark='c'/>Only small balls fall through, so every ball that "
            "passes is pink. There is selection of pink balls. <bookmark mark='d'/>But there is selection for small "
            "size, not for colour: size is what causes a ball to pass. <bookmark mark='e'/>Correlations between "
            "traits and fitness cannot tell us which trait is selected for. That is a causal question, of exactly "
            "the kind Part 17 learned to ask."
        ) as vo:
            self.play(FadeIn(hc), Create(box), FadeIn(balls), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(grid))
            vo.wait_until("c")
            self.play(*[b.animate.shift(DOWN * 1.6) for b in balls if b.radius < 0.2], FadeIn(rows[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def drift(self):
        d = load("drift")
        head = label(r"The rival of selection: \ drift", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 120, 40], y_range=[0, 1, 0.5], x_length=5.6, y_length=3.0,
                  axis_config={"color": GREY_B, "font_size": 14}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([-3.4, 0.2, 0])
        al = label(r"allele frequency, \ neutral, \ $N = " + f"{d['path_N']}" + r"$, \ 24 populations", font_size=16,
                   color=GREY_A).next_to(ax, UP, buff=0.1)
        gl = label(r"generations", font_size=14, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        paths = VGroup(*[series_plot(ax, t, interpolate_color(ManimColor(GENE), ManimColor(ALT), i / 23), width=1.6)
                         for i, t in enumerate(d["paths"])])
        tally = label(f"{d['lost']}" + r" lost, \ " + f"{d['fixed']}" + r" fixed, \ " +
                      f"{24 - d['lost'] - d['fixed']}" + r" still drifting, \ with no selection at all", font_size=17,
                      color=WHITE).next_to(gl, DOWN, buff=0.15)
        formula = MathTex(r"u(s) = \frac{1 - e^{-2s}}{1 - e^{-2Ns}}", r"\quad\xrightarrow{\;s \to 0\;}\quad",
                          r"\frac{1}{N}", font_size=32).move_to([3.4, 1.9, 0])
        formula[0].set_color(GOAL)
        fx = d["fix"]
        hd = [r"s", r"\text{simulated}", r"\text{Kimura}"]
        rows = []
        for k in ("+0.00", "+0.01", "+0.05", "-0.01"):
            v = fx[k]
            rows.append([MathTex(f"{v['s']:+.2f}", font_size=24, color=OK if v["s"] > 0 else (BAD if v["s"] < 0 else
                                                                                               GREY_A)),
                         MathTex(f"{v['sim']:.4f}", font_size=24), MathTex(f"{v['kimura']:.4f}", font_size=24,
                                                                        color=GOAL)])
        grid = ValueGrid(hd, rows, col_w=[1.3, 1.9, 1.9], cell_h=0.48, font_size=20).move_to([3.4, -0.4, 0])
        cap = label(r"one new mutant, \ $N = " + f"{d['N']}" + r"$, \ " + f"{d['runs']:,}".replace(",", "{,}") +
                    r" runs each", font_size=16, color=GREY_A).next_to(grid, DOWN, buff=0.15)
        lesson = label(r"a 1\% advantage only doubles the odds: \ most beneficial mutations are lost by chance",
                       font_size=19, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Selection has a rival. <bookmark mark='a'/>In a finite population, which individuals happen to "
            "reproduce is partly a matter of chance, so allele frequencies wander even when no variant is fitter. "
            "The Reasoner runs twenty-four populations of fifty, each starting at one half, with no selection at "
            "all. <bookmark mark='b'/>After a hundred and twenty generations, twelve have lost the allele, ten have "
            "fixed it, and two are still drifting. This is random genetic drift. <bookmark mark='c'/>Now a single "
            "new mutant, in a population of a hundred. Motoo Kimura's diffusion theory gives its chance of taking "
            "over: one over N if it is neutral. <bookmark mark='d'/>The Reasoner checks the formula with forty "
            "thousand runs for each case. A neutral mutant fixes about one time in a hundred; a one percent "
            "advantage raises that to about one in forty-four; a five percent advantage to about one in eleven. A "
            "harmful mutant still sometimes wins. <bookmark mark='e'/>So even a beneficial mutation is usually lost "
            "by chance. Fitness raises the odds; it does not guarantee the outcome."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(al), FadeIn(gl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.05), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(tally))
            vo.wait_until("c")
            self.play(Write(formula))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                        lag_ratio=0.3), FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def drift_debate(self):
        head = label(r"Is drift a cause?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Kimura \ (1968)", r"the neutral theory: \ most molecular change is drift, \ not selection", GENE),
            (r"Beatty \ (1984)", r"selection is \textit{discriminate} sampling by fitness differences; \ drift is "
                                 r"\textit{indiscriminate} sampling", ORG),
            (r"the problem", r"any outcome is consistent with both: \ a fitter type can lose by drift", BAD),
            (r"statisticalists", r"Walsh, \ Lewens and Ariew; \ Matthen and Ariew \ (2002): \ selection and drift are "
                                 r"statistical summaries, \ not forces", GROUP),
            (r"causalists", r"Millstein \ (2002); \ Reisman and Forber \ (2005): \ shrink a population and drift "
                            r"increases: \ an intervention", ALT),
            (r"Part 17", r"the dispute is about what counts as a cause, \ and interventions decide it", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.6, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Drift raises a philosophical question. <bookmark mark='a'/>Motoo Kimura's neutral theory proposed "
            "that most evolutionary change at the molecular level is drift, not selection. "
            "<bookmark mark='b'/>John Beatty distinguished them as kinds of sampling: selection samples organisms "
            "discriminately, by their differences in fitness; drift samples them indiscriminately. "
            "<bookmark mark='c'/>The trouble is that any particular outcome could result from either, since a "
            "fitter type can lose by chance. <bookmark mark='d'/>Statisticalists, such as Denis Walsh, Tim Lewens "
            "and André Ariew, and Mohan Matthen with Ariew, conclude that selection and drift are not forces at all, "
            "but statistical summaries of what individual organisms do. <bookmark mark='e'/>Causalists, such as "
            "Roberta Millstein, reply that drift can be manipulated: shrink the population and drift grows "
            "stronger, which is just what makes something a cause. <bookmark mark='f'/>The dispute turns on what "
            "counts as a cause, and Part 17's interventions are the natural test."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
