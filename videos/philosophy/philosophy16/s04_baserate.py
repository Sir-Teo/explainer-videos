from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403

PW_C = {"0.2": BAD, "0.5": FISH, "0.8": ALTC}


class BaseRate(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Base rates", r"How often is a `positive' result true?", lit=(2005,), part=PART)
        with self.voiceover("Chapter three. Base rates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grid()
        self.prosecutor()
        self.collins()
        self.science()
        self.why()

    def grid(self):
        d = load("baserate")
        head = label(r"A screening test, \ 1{,}000 people", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        spec = label(r"prevalence 1\%; \ sensitivity 90\%; \ false-positive rate 9\%", font_size=22,
                     color=GREY_A).next_to(head, DOWN, buff=0.2)
        cols, rows_ = 40, 25
        size = 0.15
        cells = VGroup()
        for i in range(d["population"]):
            r, c = divmod(i, cols)
            cells.add(Square(side_length=size, stroke_width=0, fill_color=WELL, fill_opacity=1).move_to(
                [-6.3 + c * (size + 0.03), 1.75 - r * (size + 0.03), 0]))
        rng = np.random.default_rng(7)
        spread = sorted(rng.choice(d["population"], d["sick"], replace=False).tolist())
        rest = [i for i in range(d["population"]) if i not in spread]
        fp = sorted(rng.choice(rest, d["fp"], replace=False).tolist())
        sick_cells = [cells[i] for i in spread]
        fp_cells = [cells[i] for i in fp]
        tp_cells = sick_cells[:d["tp"]]
        right = stack([
            (str(d["sick"]) + r" have the disease; \ " + str(d["tp"]) + r" test positive", SICK),
            (str(d["healthy"]) + r" do not; \ " + str(d["fp"]) + r" test positive anyway", FISH),
            (r"positive and sick: \ $\dfrac{" + str(d["tp"]) + r"}{" + str(d["tp"]) + " + " + str(d["fp"]) + r"} = "
             + f"{100 * d['ppv']:.0f}" + r"\%$", GOAL),
            (r"160 gynaecologists, \ 2007: \ most said about 90\%", BAD),
            (r"natural frequencies \ (Gigerenzer and Hoffrage, \ 1995) \ make it easy", GREY_A),
        ], font_size=21, aligned_edge=LEFT, buff=0.35, width=5.6).move_to([4.25, -0.4, 0])
        with self.voiceover(
            "Before asking what significance means for science, consider a medical test. <bookmark mark='a'/>A "
            "disease affects one percent of people. The test catches ninety percent of cases, and gives a false "
            "alarm for nine percent of healthy people. <bookmark mark='b'/>Picture a thousand people. "
            "<bookmark mark='c'/>Ten have the disease, and nine of them test positive. <bookmark mark='d'/>Nine "
            "hundred and ninety do not, but eighty-nine of them test positive anyway. <bookmark mark='e'/>So of "
            "the ninety-eight positives, only nine are sick: about nine percent. <bookmark mark='f'/>When Gerd "
            "Gigerenzer put this question to a hundred and sixty gynaecologists in 2007, most answered around "
            "ninety percent. <bookmark mark='g'/>Stated as natural frequencies, as here, the answer becomes easy. "
            "Stated as conditional probabilities, it defeats experts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(spec))
            vo.wait_until("b")
            self.play(FadeIn(cells, lag_ratio=0.001), run_time=1.5)
            vo.wait_until("c")
            self.play(*[c.animate.set_fill(SICK) for c in sick_cells], FadeIn(right[0]))
            self.play(*[c.animate.set_stroke(WHITE, width=2) for c in tp_cells])
            vo.wait_until("d")
            self.play(*[c.animate.set_fill(FISH) for c in fp_cells], FadeIn(right[1]))
            vo.wait_until("e")
            self.play(FadeIn(right[2]))
            vo.wait_until("f")
            self.play(FadeIn(right[3]))
            vo.wait_until("g")
            self.play(FadeIn(right[4]))
        self.clear_scene()

    def prosecutor(self):
        hc = history_card(1999, r"R v.\ Sally Clark", r"two infant deaths, \ one expert, \ one number", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        claim = MathTex(r"P(\text{two cot deaths}) = \Big(\frac{1}{8{,}543}\Big)^2 \approx \frac{1}{73\ \text{million}}",
                        font_size=34, color=BAD).next_to(hc, DOWN, buff=0.4).set_x(0)
        rows = [
            (r"error 1", r"squaring assumes the two deaths are independent; \ genes and environment are shared", FISH),
            (r"error 2", r"$P(\text{evidence} \mid \text{innocent})$ was heard as $P(\text{innocent} \mid "
                         r"\text{evidence})$: \ the prosecutor's fallacy", BAD),
            (r"the comparison", r"double murder of infants is rarer still: \ the odds favoured natural causes \ "
                                r"(Hill, \ 2004)", OK),
            (r"the outcome", r"convicted 1999; \ the Royal Statistical Society protested; \ freed on appeal, \ 2003",
             GREY_A),
        ]
        g = rows_table(rows, top=claim.get_bottom()[1] - 0.4, gap=0.4, width=8.6, x_text=-3.2)
        with self.voiceover(
            "Base rates decide lives as well as diagnoses. <bookmark mark='a'/>In 1999 Sally Clark was convicted in "
            "England of murdering her two baby sons. An expert witness told the jury that the chance of two cot "
            "deaths in such a family was one in eight thousand five hundred, squared: one in seventy-three million. "
            "<bookmark mark='b'/>The first error was squaring: it assumes the two deaths are independent, when "
            "genes and household are shared. <bookmark mark='c'/>The second error was worse. The number was the "
            "probability of the evidence if she were innocent, and it was heard as the probability that she was "
            "innocent, given the evidence. That is the prosecutor's fallacy, the base-rate fallacy in a courtroom. "
            "<bookmark mark='d'/>The relevant comparison is with the alternative explanation, double murder of "
            "infants, which is rarer still. The mathematician Ray Hill estimated that the odds favoured natural "
            "causes. <bookmark mark='e'/>The Royal Statistical Society protested, and Sally Clark was freed on "
            "appeal in 2003."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(claim))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def collins(self):
        d = load("collins")
        hc = history_card(1968, r"People v.\ Collins", r"the Supreme Court of California", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        tr = VGroup(*[label(f"{name}: \\ $1/{den:,}$".replace(",", "{,}"), font_size=19, color=GREY_A)
                      for name, den in d["traits"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        prod = MathTex(r"\text{product} = \frac{1}{" + f"{d['denominator']:,}".replace(",", "{,}") + r"}",
                       font_size=30, color=BAD)
        left = VGroup(tr, prod).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hc, DOWN, buff=0.35).to_edge(
            LEFT, buff=0.5)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.0,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([3.0, 0.2, 0])
        xl = label(r"couples in the area \ (millions)", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"$P(\text{another match} \mid \text{one match})$", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.15)
        curve = series_plot(ax, [y for _, y in d["curve"]], FISH, xs=[x for x, _ in d["curve"]])
        n = d["N"] / 1e6
        dot = Dot(ax.c2p(n, d["another"]), color=BAD, radius=0.07)
        dl = label(f"{n:.0f}" + r" million: \ " + f"{d['another']:.2f}", font_size=19, color=BAD).next_to(
            dot, RIGHT, buff=0.15).shift(DOWN * 0.15)
        foot = stack([(r"the traits were not independent, \ and the numbers were guesses", WHITE),
                      (r"the court reversed, \ with a mathematical appendix: \ the base rate is the number of "
                       r"couples", OK)], font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "An older case shows the same mistake with an extra twist. <bookmark mark='a'/>In 1964 a woman was "
            "robbed in Los Angeles, and witnesses described a couple fleeing in a partly yellow car. At trial, a "
            "mathematics instructor multiplied six frequencies: a man with a moustache, a woman with a ponytail, "
            "blond hair, a beard, and so on. <bookmark mark='b'/>The product was one in twelve million, and the "
            "jury convicted. <bookmark mark='c'/>The traits were not independent, and the numbers were guesses. "
            "But grant them. In 1968 California's Supreme Court asked the right question: given that one couple in "
            "the area fits, how likely is it that another does too? <bookmark mark='d'/>With twelve million "
            "couples in the area, the Reasoner computes it exactly: forty-two percent. <bookmark mark='e'/>One in "
            "twelve million was never the probability of innocence. The court reversed the conviction, and "
            "attached a mathematical appendix."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tr], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(Write(prod))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(Create(curve), run_time=1.5)
            self.play(FadeIn(dot), FadeIn(dl))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def science(self):
        d = load("ppv")
        head = label(r"Science as a screening test", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"\text{PPV} = \frac{(1 - \beta)\, R}{(1 - \beta)\, R + \alpha}", font_size=36,
                     color=GOAL).next_to(head, DOWN, buff=0.3)
        key = label(r"$R$: \ odds that a tested hypothesis is true; \ $1 - \beta$: \ power; \ $\alpha = 0.05$",
                    font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        ax = Axes(x_range=[-3, 1, 1], y_range=[0, 1, 0.25], x_length=6.2, y_length=3.4, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": False}).move_to([-3.0, -1.5, 0])
        yt = VGroup(*[label(f"{v:.2f}", font_size=15, color=GREY_B).next_to(ax.c2p(-3, v), LEFT, buff=0.1)
                      for v in (0, 0.25, 0.5, 0.75, 1)])
        xt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k, t in zip(range(-3, 2), (r"1:1000", r"1:100", r"1:10", r"1:1", r"10:1"))])
        xl = label(r"prior odds $R$", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.12)
        curves = VGroup()
        leg = VGroup()
        for pw, pts in d["curve"].items():
            curves.add(series_plot(ax, [y for _, y in pts], PW_C[pw], xs=[math.log10(r) for r, _ in pts]))
            leg.add(VGroup(Line(ORIGIN, RIGHT * 0.35, color=PW_C[pw], stroke_width=4),
                           label(rf"power {pw}", font_size=18, color=PW_C[pw])).arrange(RIGHT, buff=0.1))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.05).align_to(ax, LEFT).shift(
            RIGHT * 0.4)
        hd = [r"\text{study}", r"\text{PPV}"]
        tab = d["table"]
        pick = [0, 2, 3, 6, 7]
        names = [r"powered RCT, \ 1:1 odds", r"meta-analysis of small studies", r"underpowered phase I/II RCT",
                 r"underpowered epidemiology", r"discovery-oriented, \ massive testing"]
        rows = [[label(n, font_size=17), MathTex(f"{tab[i]['ppv']:.2f}" if tab[i]["ppv"] >= 0.01 else
                                                 f"{tab[i]['ppv']:.3f}", font_size=22,
                                                 color=OK if tab[i]["ppv"] > 0.5 else BAD)]
                for n, i in zip(names, pick)]
        grid = ValueGrid(hd, rows, col_w=[4.4, 1.2], cell_h=0.48, font_size=20).move_to([3.9, -1.4, 0])
        tl = label(r"Ioannidis \ (2005), \ recomputed \ (with his bias terms)", font_size=18,
                   color=HIST).next_to(grid, UP, buff=0.15)
        with self.voiceover(
            "John Ioannidis saw that science itself is a screening test. <bookmark mark='a'/>Of all the hypotheses "
            "a field tests, some fraction are true: call the odds R. A significant result is a positive. The share "
            "of positives that are true is the positive predictive value: power times R, over power times R plus "
            "alpha. <bookmark mark='b'/>Plot it against the prior odds. With high power and even odds, most "
            "significant results are true. With low power, or long odds, most are false. "
            "<bookmark mark='c'/>Ioannidis's own examples, recomputed with his allowance for bias: a well-powered "
            "trial, point eight five. A meta-analysis of small studies, point four one. An underpowered early trial, "
            "point two three. Underpowered epidemiology, point one two. And discovery research testing thousands of "
            "hypotheses, one in a thousand. <bookmark mark='d'/>Hence the title of his paper: why most published "
            "research findings are false."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(leg),
                      LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tl), FadeIn(grid.head), Create(grid.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(Indicate(grid.cell[4][1], color=BAD, scale_factor=1.3))
        self.clear_scene()

    def why(self):
        hc = history_card(2005, r"John Ioannidis", r"`Why Most Published Research Findings Are False'", width=7.0,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"a finding is less likely true when \ldots", WHITE),
            (r"the studies are smaller, \ and the effects smaller", GREY_A),
            (r"more relationships are tested, \ with less pre-selection", GREY_A),
            (r"designs, \ definitions and analyses are more flexible \ (next chapter)", FISH),
            (r"there are financial interests, \ or a hot field with many teams racing", GREY_A),
            (r"and only the significant results get published: \ the file drawer \ (Rosenthal, \ 1979)", BAD),
        ], font_size=22, aligned_edge=LEFT, buff=0.32).next_to(hc, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Ioannidis drew corollaries from the formula. <bookmark mark='a'/>A claimed finding is less likely to "
            "be true <bookmark mark='b'/>when the studies are smaller, and the effects smaller; "
            "<bookmark mark='c'/>when more relationships are tested, with less pre-selection; "
            "<bookmark mark='d'/>when designs, definitions and analyses are more flexible; <bookmark mark='e'/>when "
            "there are financial interests, or many teams racing in a hot field. <bookmark mark='f'/>And all of it "
            "is made worse when only significant results are published, and the rest go into what Robert Rosenthal "
            "called the file drawer."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
