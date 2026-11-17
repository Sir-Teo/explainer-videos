from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Thurstone(VoiceoverScene):
    def construct(self):
        self.law()
        self.vegetables()
        self.judges()

    def law(self):
        card = chapter_card(2, r"The law of comparative judgment", r"How do inconsistent choices give a scale?",
                            lit={1927: r"Thurstone"}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter two. The law of comparative judgment."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()
        head = heading(r"Two fluctuating impressions")
        A = axes([-3, 4], [0, 0.45], x_length=5.6, y_length=2.6, xticks=[-2, 0, 2, 4], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"impression", center=[-3.3, 0.9, 0], font_size=13)
        x = np.linspace(-3, 4, 300)
        from scipy import stats
        ci = curve(A.ax, x, stats.norm.pdf(x, 0.0, 1), SYMP, stroke_width=3)
        cj = curve(A.ax, x, stats.norm.pdf(x, 1.0, 1), PERSON, stroke_width=3)
        eqs = VGroup(
            MathTex(r"P(j \succ i) = \Phi\!\left(\frac{s_j - s_i}{\sigma\sqrt{2}}\right)", font_size=36, color=MODEL),
            MathTex(r"s_j - s_i = \sigma\sqrt{2}\;\Phi^{-1}\big(P(j \succ i)\big)", font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.35).move_to([-3.3, -1.8, 0])
        rows = rows_of([
            (r"each option evokes an impression that varies from moment to moment: \ normal, \ with mean $s$", WHITE),
            (r"the choice goes to the larger impression; \ the difference of two normals is normal, \ with variance "
             r"$2\sigma^2$ (Case V: \ equal spreads, \ no correlation)", MODEL),
            (r"invert: \ each proportion gives a distance on the scale; \ it is Part 12's signal detection, \ between "
             r"two stimuli", GOOD),
            (r"a proportion of 50\% means no distance; \ 84\% means $\sigma\sqrt 2$; \ 100\% means the scale cannot "
             r"say how far", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Thurstone's idea. <bookmark mark='a'/> Each option evokes an impression that varies from moment to "
            "moment: a normal distribution, with a mean s. <bookmark mark='b'/> The choice goes to the larger "
            "impression. The difference of two independent normals is normal, with twice the variance. That's his "
            "Case Five: equal spreads, no correlation. <bookmark mark='c'/> Invert the normal curve, and each "
            "proportion gives a distance on the scale. It's Part 12's signal detection, between two stimuli. "
            "<bookmark mark='d'/> Fifty percent means no distance. Eighty-four percent means one unit. And a hundred "
            "percent means the scale can't say how far."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(ci), Create(cj))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(eqs[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def vegetables(self):
        d = load("veg")
        head = heading(r"Nine vegetables")
        P = d["P"]
        cell = 0.36
        grid = VGroup()
        for i in range(9):
            for j in range(9):
                v = P[i, j]
                col = interpolate_color(ManimColor(AUTH), ManimColor(GOOD), float(v))
                grid.add(Square(cell, stroke_width=0.5, stroke_color=BLACK, fill_color=col, fill_opacity=0.9 if i != j
                                else 0.2).move_to([-5.2 + j * cell, 2.2 - i * cell, 0]))
        lab = VGroup(*[label(n, font_size=11, color=GREY_A).next_to(grid[9 * i], LEFT, buff=0.08)
                       for i, n in enumerate(d["names"])])
        A = axes([-1.1, 0.8], [0, 1], x_length=6.0, y_length=0.6, xticks=[-1, -0.5, 0, 0.5], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"scale value (Case V)", center=[-3.2, -2.3, 0], font_size=12)
        dots = VGroup(*[Dot(A.ax.c2p(s, 0.5), radius=0.07, color=PERSON) for s in d["thurstone"]])
        names = VGroup(*[label(n, font_size=11, color=GREY_A).next_to(A.ax.c2p(s, 0.5), UP if k % 2 else DOWN,
                                                                         buff=0.12)
                         for k, (n, s) in enumerate(zip(d["names"], d["thurstone"]))])
        rows = rows_of([
            (r"Guilford's students compared every pair of nine vegetables; \ each square is the share preferring the "
             r"row to the column (green: \ most)", WHITE),
            (r"Case V turns the 36 proportions into 9 numbers: \ turnips at the bottom, \ corn at the top", PERSON),
            (rf"the 9 numbers reproduce the 72 proportions to within {100 * d['err_thurstone']:.1f} points on "
             rf"average: \ one dimension is nearly enough", MODEL),
            (r"the scale has an arbitrary zero and unit: \ an interval scale, \ as Part 3 called it", GOOD),
        ], 5.6, 18, 0.36).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.thurstone\_scale}; \ Guilford (1954), \ via psychTools")
        with self.voiceover(
            "Here is the method on real preferences. <bookmark mark='a'/> J. P. Guilford's students compared every "
            "pair of nine vegetables. Each square is the share who preferred the row to the column. "
            "<bookmark mark='b'/> Case Five turns the thirty-six proportions into nine numbers: turnips at the bottom, "
            "corn at the top. <bookmark mark='c'/> And those nine numbers reproduce all the proportions to within "
            "about three and a half points on average. One dimension is nearly enough. <bookmark mark='d'/> The scale "
            "has an arbitrary zero and unit. It's an interval scale, in Part 3's terms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15),
                      FadeIn(names), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def judges(self):
        d = load("judges")
        head = heading(r"How many judges?")
        A = axes([0, 420], [0, 0.4], x_length=5.6, y_length=3.0, xticks=[5, 50, 100, 200, 400], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"judges, \ each judging every pair once",
                 ylabel=r"error in the scale (in $\sigma$)", center=[-3.3, 0.3, 0], font_size=13)
        c = curve(A.ax, d["n"], d["rmse"], MODEL, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(n, e), radius=0.07, color=MODEL) for n, e in zip(d["n"], d["rmse"])])
        rows = rows_of([
            (r"nine stimuli spread evenly over 2.4 discriminal SDs; \ panels of judges simulated by Case V", WHITE),
            (rf"5 judges: \ each scale value off by {d['rmse'][0]:.2f} SD on average; \ 25 judges: \ "
             rf"{d['rmse'][2]:.2f}; \ 100: \ {d['rmse'][4]:.2f}", MODEL),
            (r"the error halves each time the panel quadruples: \ the square-root law, \ as for any average", PERSON),
            (r"so a small panel can order stimuli that are far apart, \ but not ones a tenth of an SD apart", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.simulate\_pairs}, \ \texttt{thurstone\_scale}, \ 100 panels each")
        with self.voiceover(
            "How many judges does a scale need? <bookmark mark='a'/> Take nine stimuli spread evenly, and simulate "
            "panels of judges under Case Five. <bookmark mark='b'/> With five judges, each scale value is off by about "
            "a third of a standard deviation. With twenty-five, about an eighth. With a hundred, a sixteenth. "
            "<bookmark mark='c'/> The error halves each time the panel quadruples: the square-root law, as for any "
            "average. <bookmark mark='d'/> So a small panel can order stimuli that are far apart, but not ones a "
            "tenth of a standard deviation apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
