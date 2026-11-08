from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Design or selection?", r"What explains the fit of organisms to their lives?",
                            lit=(1802, 1859), part=PART)
        with self.voiceover("Chapter one. Design or selection?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paley()
        self.darwin()
        self.eye()
        self.likelihood()

    def paley(self):
        hc = history_card(1802, r"William Paley", r"\textit{Natural Theology}", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        watch = VGroup(Circle(radius=1.1, color=GOAL, stroke_width=4),
                       *[Line(ORIGIN, 0.95 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_B, stroke_width=2)
                         .scale(0.15, about_point=0.95 * np.array([np.cos(a), np.sin(a), 0]))
                         for a in np.linspace(0, TAU, 12, endpoint=False)],
                       Line(ORIGIN, UP * 0.75, color=WHITE, stroke_width=4),
                       Line(ORIGIN, RIGHT * 0.55, color=WHITE, stroke_width=4)).move_to([-4.2, -0.6, 0])
        rows = stack([(r"a stone on a heath: \ it may have lain there forever", GREY_A),
                      (r"a watch: \ its parts are framed and put together for a purpose", GOAL),
                      (r"`the inference, \ we think, \ is inevitable, \ that the watch must have had a maker'", WHITE),
                      (r"the eye is a better instrument than the telescope: \ so it too had a maker", ORG),
                      (r"Hume \ (1779): \ the analogy is weak, \ and a designer needs explaining too", BAD)],
                     font_size=20, aligned_edge=LEFT, width=7.2).move_to([2.6, -0.6, 0])
        with self.voiceover(
            "William Paley's Natural Theology begins on a heath. <bookmark mark='a'/>If I strike my foot against a "
            "stone, I might suppose it had lain there forever. <bookmark mark='b'/>But if I find a watch, I notice "
            "that its parts are framed and put together for a purpose: to measure the hours. "
            "<bookmark mark='c'/>The inference, Paley wrote, is inevitable, that the watch must have had a maker. "
            "<bookmark mark='d'/>The eye is a far more intricate instrument than a telescope, so it too must have "
            "had a maker. <bookmark mark='e'/>David Hume had already objected, in Dialogues published in 1779, that "
            "the analogy between organisms and machines is weak, and that a designer would itself need explaining."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(watch))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def darwin(self):
        hc = history_card(1859, r"Charles Darwin", r"\textit{On the Origin of Species}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"one long argument", r"Darwin's own description: \ a single explanation for many classes of fact", GENE),
            (r"the facts", r"homology, \ embryology, \ rudimentary organs, \ biogeography, \ the fossil order", WHITE),
            (r"the explanation", r"descent with modification, \ driven by natural selection", OK),
            (r"its logical form", r"inference to the best explanation: \ the consilience of inductions \ (Whewell)",
             GOAL),
            (r"the gap", r"no mechanism of heredity until Mendel was rediscovered \ (1900) \ and the modern synthesis",
             BAD),
        ]
        g = rows_table(rows, top=1.4, gap=0.45, width=8.4, x_text=-2.6)
        with self.voiceover(
            "Darwin called the Origin one long argument. <bookmark mark='a'/>It offered a single explanation for "
            "many classes of fact. <bookmark mark='b'/>The same bones in a bat's wing, a whale's flipper and a "
            "human hand; similar embryos in different animals; rudimentary organs with no use; the distribution of "
            "species on islands; and the order of fossils in the rocks. <bookmark mark='c'/>All are explained by "
            "descent with modification, driven by natural selection. <bookmark mark='d'/>The form of the argument is "
            "inference to the best explanation, or what William Whewell called the consilience of inductions: many "
            "independent lines of evidence converging on one hypothesis. <bookmark mark='e'/>Its gap was heredity. "
            "Darwin had no workable theory of inheritance until Mendel's work was rediscovered in 1900 and fused with "
            "selection in the modern synthesis."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def eye(self):
        d = load("eye")
        head = label(r"Organs of extreme perfection", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        stages = VGroup()
        for i, ang in enumerate((0.0, 0.9, 1.8, 2.7, 3.6, 4.4)):
            c = np.array([-2.75 + i * 1.1, 0.95, 0])
            if ang == 0:
                shape = Line(c + LEFT * 0.4, c + RIGHT * 0.4, color=GENE, stroke_width=5)
            else:
                shape = Arc(radius=0.42, start_angle=-PI / 2 - ang / 2, angle=ang, arc_center=c, color=GENE,
                            stroke_width=5)
            g = VGroup(shape)
            if i == 5:
                g.add(Ellipse(width=0.28, height=0.4, color=ORG, fill_opacity=0.5).move_to(c + UP * 0.38))
            stages.add(g)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.06, color=GREY_C,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(5)])
        names = VGroup(*[label(n, font_size=14, color=GREY_A).move_to([stages[i].get_x(), 0.2, 0])
                         for i, n in enumerate((r"patch", r"cup", r"deeper", r"deeper still", r"pinhole", r"lens"))])
        quote = label(r"`absurd in the highest possible degree' \ \ \ yet each step is useful \ (Darwin, \ 1859)",
                      font_size=20, color=ORG).next_to(head, DOWN, buff=0.3)
        f1 = MathTex(r"n_{\text{steps}} = \frac{\ln F}{\ln 1.01} = \frac{\ln(8.0 \times 10^{7})}{\ln 1.01} = "
                     + f"{d['steps']:.0f}", font_size=32, color=GENE).move_to([0, -0.55, 0])
        f2 = MathTex(r"R = h^2 \, i \, \mathrm{CV} = 0.5 \times 0.01 \times 0.01 = " + f"{100 * d['per_gen']:.3f}"
                     + r"\%", font_size=32, color=ORG).next_to(f1, DOWN, buff=0.22)
        f3 = MathTex(r"\text{generations} = \frac{\ln F}{\ln(1 + R)} \approx " + f"{d['generations']:,.0f}".replace(
            ",", "{,}"), font_size=34, color=OK).next_to(f2, DOWN, buff=0.22)
        rows = stack([(r"Nilsson and Pelger \ (1994): \ every quantity changes by 1\% at a time, \ and every step "
                       r"improves the image", WHITE),
                      (r"with one generation a year: \ well under half a million years, \ a geological instant", GOAL)],
                     font_size=19, width=11.0).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Paley's favourite example was the eye. <bookmark mark='a'/>Darwin admitted that to suppose the eye "
            "could be formed by natural selection seems absurd in the highest possible degree. But, he argued, if a "
            "series of gradations exists from a simple patch to a perfect eye, each one useful to its owner, the "
            "difficulty disappears. <bookmark mark='b'/>In 1994 Dan-Eric Nilsson and Susanne Pelger put numbers on "
            "the series: a flat patch of light-sensitive cells, a cup, a deeper cup, a pinhole, and a lens, each "
            "step sharpening the image. <bookmark mark='c'/>Measured in steps of one percent, the whole change "
            "amounts to a factor of about eighty million: eighteen hundred and twenty-nine steps. "
            "<bookmark mark='d'/>They then assumed modest values for heritability, the strength of selection and "
            "variation, which give a change of only five thousandths of a percent per generation. "
            "<bookmark mark='e'/>The Reasoner divides: about three hundred and sixty-four thousand generations. "
            "<bookmark mark='f'/>For small animals with one generation a year, that is less than half a million "
            "years, an instant in geological time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stages], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(names), FadeIn(rows[0]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(Write(f1))
            vo.wait_until("d")
            self.play(Write(f2))
            vo.wait_until("e")
            self.play(Write(f3))
            vo.wait_until("f")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def likelihood(self):
        d = load("paley")
        head = label(r"Design against selection, \ as likelihoods \ (Sober)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        eq = MathTex(r"\frac{P(O \mid \text{selection})}{P(O \mid \text{design})}", font_size=36,
                     color=GOAL).next_to(head, DOWN, buff=0.35)
        hd = [r"\text{observation } O", r"P(O \mid \text{design})", r"P(O \mid \text{selection})", r"\text{ratio}"]
        rows = [[label(r["obs"], font_size=18), MathTex(f"{r['p_design']:.2f}", font_size=22, color=ORG),
                 MathTex(f"{r['p_selection']:.1f}", font_size=22, color=GENE),
                 MathTex(f"{r['ratio']:.0f}", font_size=22, color=OK)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[5.4, 2.4, 2.6, 1.4], cell_h=0.55, font_size=19).next_to(eq, DOWN, buff=0.4)
        note = stack([(r"illustrative probabilities: \ the point is the structure, \ not the numbers", GREY_A),
                      (r"imperfections and historical traces favour descent: \ an optimal designer would not make them",
                       OK),
                      (r"the catch: \ `design' predicts nothing until we specify the designer's goals and abilities", BAD),
                      (r"and if we may specify anything, \ it can fit every observation \ (Sober, \ 2008)", GOAL)],
                     font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Elliott Sober reframed the debate with Part 15's likelihoods. <bookmark mark='a'/>For each observation, "
            "ask how probable it is on the hypothesis of selection, and on the hypothesis of design. "
            "<bookmark mark='b'/>The vertebrate retina is wired backwards, with a blind spot where the nerve passes "
            "through it. The recurrent laryngeal nerve of a giraffe runs four and a half metres down and back up "
            "the neck to reach a larynx a few centimetres from its origin. Humans and chimpanzees share the same "
            "broken gene for making vitamin C. <bookmark mark='c'/>The probabilities here are illustrative; the "
            "structure is the point. Such historical traces are expected on descent with modification, and "
            "surprising on optimal design. <bookmark mark='d'/>The catch: design predicts nothing until we specify "
            "what the designer wanted and could do. <bookmark mark='e'/>And if we may specify anything at all, the "
            "design hypothesis fits every observation, and so is supported by none."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                        lag_ratio=0.3))
            for mk, r in zip("cde", [VGroup(note[0], note[1]), note[2], note[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
