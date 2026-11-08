from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Impossible(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The impossibility", r"Can a score be fair by every measure?", lit=(2016, 2017), part=PART)
        with self.voiceover("Chapter three. The impossibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.identity()
        self.balance()
        self.proof()
        self.price()
        self.wall_brick()

    def identity(self):
        c = load("criteria")
        r, idf = c["rates"], c["identity_fpr"]
        assert abs(idf["A"] - r["A"]["fpr"]) < 0.002 and abs(idf["B"] - r["B"]["fpr"]) < 0.002
        head = label(r"Chouldechova's identity \ (2017)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = MathTex(r"p = \frac{TP + FN}{N}, \quad \mathrm{PPV} = \frac{TP}{TP + FP}, \quad "
                       r"\mathrm{FNR} = \frac{FN}{TP + FN}, \quad \mathrm{FPR} = \frac{FP}{FP + TN}",
                       font_size=30).move_to([0, 2.2, 0])
        step = MathTex(r"FP = TP\,\frac{1 - \mathrm{PPV}}{\mathrm{PPV}}, \qquad TP = (1 - \mathrm{FNR})\, p N, "
                       r"\qquad FP + TN = (1 - p) N", font_size=30).move_to([0, 1.1, 0])
        ident = MathTex(r"\mathrm{FPR} \;=\; \frac{p}{1 - p}\cdot\frac{1 - \mathrm{PPV}}{\mathrm{PPV}}\cdot"
                        r"(1 - \mathrm{FNR})", font_size=40, color=EXPL).move_to([0, -0.1, 0])
        box = SurroundingRectangle(ident, color=EXPL, buff=0.15)
        hd = [r"\text{group}", r"p", r"\mathrm{PPV}", r"\mathrm{FNR}", r"\text{identity gives FPR}",
              r"\text{measured FPR}"]
        cells = [[label(g, font_size=20, color=GA if g == "A" else GB), label(f"{r[g]['base']:.3f}", font_size=19),
                  label(f"{r[g]['ppv']:.3f}", font_size=19), label(f"{r[g]['fnr']:.3f}", font_size=19),
                  label(f"{idf[g]:.4f}", font_size=19, color=EXPL), label(f"{r[g]['fpr']:.4f}", font_size=19)]
                 for g in "AB"]
        grid = ValueGrid(hd, cells, col_w=[1.4, 1.4, 1.4, 1.4, 3.4, 2.6], cell_h=0.5, font_size=18).move_to([0, -2.0, 0])
        foot = MathTex(r"\mathrm{PPV}_A=\mathrm{PPV}_B=q\in(0,1),\quad"
                       r"\mathrm{FNR}_A=\mathrm{FNR}_B<1,\quad p_A\ne p_B"
                       r"\ \Longrightarrow\ \mathrm{FPR}_A\ne\mathrm{FPR}_B",
                       font_size=23, color=BAD).to_edge(DOWN, buff=0.25)
        if foot.width > 13.3:
            foot.width = 13.3
        with self.voiceover(
            "Alexandra Chouldechova showed in 2017 why the two analyses had to disagree. It takes three lines of "
            "algebra. <bookmark mark='a'/>Start from the definitions: the base rate p, the precision, the "
            "false-negative rate and the false-positive rate, all ratios of the four cells of the confusion table. "
            "<bookmark mark='b'/>Rewrite the false positives in terms of the true positives and the precision, the "
            "true positives in terms of the base rate and the false-negative rate, and the people who do not reoffend "
            "as one minus p times N. <bookmark mark='c'/>Divide, and the false-positive rate equals p over one minus "
            "p, times one minus the precision over the precision, times one minus the false-negative rate. <bookmark "
            "mark='d'/>The Reasoner checks it on its population: the identity reproduces each group's false-positive "
            "rate. <bookmark mark='e'/>For base rates strictly between zero and one, equal precision strictly "
            "between zero and one, and a common false-negative rate below one, different base rates force different "
            "false-positive rates. Perfect precision is an exception: there are no false positives, even if some "
            "positives are missed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defs))
            vo.wait_until("b")
            self.play(Write(step))
            vo.wait_until("c")
            self.play(Write(ident), Create(box))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*rw)) for rw in grid.cell],
                                                                         lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def balance(self):
        c = load("criteria")
        bal, cal = c["balance"], c["calibration"]
        assert bal["A"]["pos"] == 0.4429 and bal["B"]["pos"] == 0.5998
        head = label(r"Calibrated, \ and unbalanced \ (Kleinberg, \ Mullainathan and Raghavan, \ 2016)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], x_length=4.6, y_length=4.6,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"numbers_to_include": [0.2, 0.4, 0.6, 0.8, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 1}},
                  y_axis_config={"numbers_to_include": [0.2, 0.4, 0.6, 0.8, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.6, -0.5, 0])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C)
        xl = label(r"score", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"share who reoffend", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        dots = VGroup()
        for g, col in (("A", GA), ("B", GB)):
            for k, v in enumerate(cal[g]):
                if v is not None:
                    dots.add(Dot(ax.c2p(0.05 + 0.1 * k, v), radius=0.07, color=col))
        side = stack([(r"calibration: \ in both groups, \ a score of $s$ means a share $s$ reoffend", FAIRC),
                      (rf"average score of those who reoffend: \ A {bal['A']['pos']:.2f}, \ B {bal['B']['pos']:.2f}", RESP),
                      (rf"average score of those who do not: \ A {bal['A']['neg']:.2f}, \ B {bal['B']['neg']:.2f}", RESP),
                      (r"the theorem: \ calibration and both balances together force equal base rates, \ or perfect "
                       r"prediction", GOAL)], font_size=20, buff=0.32, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 6.6:
                s0.width = 6.6
        side.move_to([3.2, -0.3, 0])
        with self.voiceover(
            "Jon Kleinberg, Sendhil Mullainathan and Manish Raghavan proved the same impossibility for scores, in "
            "2016. <bookmark mark='a'/>Calibration: in each group, a score of s means a share s reoffend. On the "
            "Reasoner's population, both groups' dots lie on the diagonal. <bookmark mark='b'/>Balance for the "
            "positive class: those who do reoffend should get the same average score in each group. Here they get "
            "point four four in group A and point six in group B. <bookmark mark='c'/>Balance for the negative class: "
            "those who do not reoffend should get the same average score. Here, point two four against point four. "
            "<bookmark mark='d'/>The theorem: all three conditions can hold together only if the groups have equal "
            "base rates, or the prediction is perfect. Neither is true of any real risk score."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(diag), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d0, scale=1.5) for d0 in dots], lag_ratio=0.05), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def price(self):
        d = load("trilemma")
        claims = [(c0["key"], c0["text"]) for c0 in d["claims"]]
        assert d["mus"] == [["BAL", "BASE", "CAL", "IMPERF"]] and len(d["mcs"]) == 4
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=3.6, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ fairness")
        positions = [(("BAL",), r"keep calibration", r"most deployed risk scores; \ Northpointe; \ Hedden \ (2021)"),
                     (("CAL",), r"equalize error rates", r"Hardt, \ Price and Srebro \ (2016): \ post-processing"),
                     (("BASE",), r"change the target", r"predict a less biased outcome, \ or intervene on the base "
                                                       r"rates themselves"),
                     (("IMPERF",), r"perfect prediction", r"never available")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>The score is calibrated in each group; its average "
            "is equal across groups within each outcome class, x A equals x B and y A equals y B; the base rates "
            "differ; and prediction is imperfect. <bookmark mark='b'/>Kleinberg's theorem forces one to go. "
            "<bookmark mark='c'/>Keeping calibrated scores, as Northpointe did, can leave these class averages "
            "unequal. <bookmark mark='d'/>For a binary decision, the two class averages are the true-positive and "
            "false-positive rates. Hardt, Price and Srebro's post-processing equalizes those rates; the resulting "
            "binary output loses calibration in this case. This differs from retaining a calibrated score "
            "alongside a separate adjusted decision. <bookmark mark='e'/>Some propose changing the target: predicting an outcome less "
            "shaped by biased measurement, or changing the conditions that make base rates differ. <bookmark "
            "mark='f'/>Perfect prediction is never on offer."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c0) for c0 in pl.cards], lag_ratio=0.35))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=41, current=41).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(41, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        assumptions = MathTex(r"0<p_A,p_B<1,\qquad\Pr(0<R<1)>0", font_size=20,
                              color=GREY_A).next_to(card, DOWN, buff=0.22)
        with self.voiceover(
            "This is the forty first brick in the Wall. <bookmark mark='a'/>The dream was a classifier fair by every "
            "measure: calibrated, with equal class-average scores, and treating each group alike. Kleinberg, "
            "Mullainathan and Raghavan proved that when base rates differ and prediction is imperfect, calibration "
            "and both class balances cannot all hold. Chouldechova's identity shows a related trade-off for "
            "classification. <bookmark mark='b'/>What it forces is a choice of which "
            "fairness to have, and that choice is moral, not technical."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), FadeIn(assumptions), Indicate(w.brick[41], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def proof(self):
        c = load("criteria")
        R, B = c["rates"], c["balance"]
        odds = {g: R[g]["base"] / (1 - R[g]["base"]) for g in "AB"}
        ratio = {g: B[g]["neg"] / (1 - B[g]["pos"]) for g in "AB"}
        assert all(abs(odds[g] - ratio[g]) < 0.03 for g in "AB")
        assert round(odds["A"], 2) == 0.42 and round(ratio["A"], 2) == 0.43
        assert round(odds["B"], 2) == 1.02 and round(ratio["B"], 2) == 0.99
        head = label(r"Why calibration and balance collide", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = label(r"in group $a$: \ base rate $p_a$; \ average score of those who reoffend $x_a$, \ of those who do "
                     r"not $y_a$", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.28)
        eqs = VGroup(
            MathTex(r"\text{calibration:}\quad \mathbb{E}[R \mid A = a] = \Pr(Y = 1 \mid A = a) = p_a", font_size=30),
            MathTex(r"p_a\, x_a + (1 - p_a)\, y_a = p_a", font_size=30),
            MathTex(r"\Longrightarrow\quad \frac{p_a}{1 - p_a} = \frac{y_a}{1 - x_a}", font_size=32, color=FAIRC),
            MathTex(r"\text{balance: } x_A = x_B,\ y_A = y_B \quad\Longrightarrow\quad \frac{p_A}{1 - p_A} = "
                    r"\frac{p_B}{1 - p_B}", font_size=30, color=RESP),
        ).arrange(DOWN, buff=0.28).next_to(defs, DOWN, buff=0.3)
        cells = [[label(g, font_size=20, color=GA if g == "A" else GB), label(f"{odds[g]:.2f}", font_size=20),
                  label(f"{ratio[g]:.2f}", font_size=20)] for g in "AB"]
        grid = ValueGrid([r"\text{group}", r"p/(1-p)", r"y/(1-x)"], cells, col_w=[1.6, 2.0, 2.0], cell_h=0.48,
                         font_size=20).to_corner(DR, buff=0.5).shift(DOWN * 0.1)
        foot = wrapped_label(r"unless $x = 1$ and $y = 0$: \ perfect prediction, \ where the equation holds for any "
                             r"base rate", 6.2, 20, GOAL).to_corner(DL, buff=0.55)
        with self.voiceover(
            "Why must this happen? The proof takes four lines. <bookmark mark='a'/>In group a, write p for the base "
            "rate, x for the average score of those who reoffend, and y for the average score of those who do not. "
            "Calibration means the average score in the group equals its base rate. <bookmark mark='b'/>But the "
            "average score is a mixture: a share p of the group averages x, and the rest averages y. So p x plus one "
            "minus p times y equals p. <bookmark mark='c'/>Rearranging, the odds of the base rate, p over one minus p, "
            "equal y over one minus x. <bookmark mark='d'/>Now balance says x and y are the same in both groups. "
            "Then the right-hand sides are equal, so the odds are equal, so the base rates are equal. <bookmark "
            "mark='e'/>The Reasoner checks its population. In group A, the odds are point four two, and y over one "
            "minus x is point four three; in group B, one point zero two against point nine nine, equal up to "
            "sampling noise. The identity holds in each group, so the two sides cannot both match across groups. "
            "<bookmark mark='f'/>The only escape is x equal to one and y equal to zero, which is perfect "
            "prediction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs), FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1], shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(TransformFromCopy(eqs[1], eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3], shift=DOWN * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c0) for rw in grid.cell for c0 in rw])
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
