from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Mincer(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Human capital and Mincer's equation", r"What is a year of school worth in the market?",
             "Chapter nine. Human capital and Mincer's equation.", lit={1964: r"Becker", 1974: r"Mincer"},
             scale=("person",), horizon=("a decade", "a century"))
        self.schooling()
        self.equation()
        self.fact()

    def schooling(self):
        Mi = load("mincer")
        ys = np.array(Mi["years"], float)
        ms = np.array([np.nan if v is None else v for v in Mi["means"]])
        ok = np.isfinite(ms)
        ax = plane([7.5, 18.5], [5.8, 6.7], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=list(range(8, 19, 2)), yticks=[5.9, 6.1, 6.3, 6.5, 6.7], xlabel=r"years of schooling",
                   ylabel=r"average log hourly wage, \ 1976", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.05 + 0.08 * np.sqrt(c / max(Mi["counts"])), color=SCHOOL)
                       for x, y, c in zip(ys[ok], ms[ok], np.array(Mi["counts"])[ok])])
        fit = seg(ax, 8, Mi["card_icpt"] + 8 * Mi["card_slope"], 18, Mi["card_icpt"] + 18 * Mi["card_slope"],
                  WHITE, 2.4, dashed=True)
        side = VGroup(
            label(rf"{Mi['n_card']:,} young men \\ (Card's sample, \ 1976)", font_size=18, color=GREY_A),
            label(r"dot size: \ how many", font_size=16, color=GREY_A),
            label(rf"roughly a straight line: \\ about {100 * Mi['card_slope']:.0f}\% a year \\ before any "
                  r"controls", font_size=18, color=SCHOOL),
            label(r"a bump at 12 and 16: \\ diplomas pay", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Card (1995), \ via Wooldridge's data", corner=DR, font_size=12)
        with self.voiceover(
            "Wages differ for reasons beyond supply and demand in one market: people differ in what they can do. In "
            "1964 Gary Becker called the skills people invest in human capital: like a machine, schooling costs "
            "something now, in fees and forgone earnings, and pays later. <bookmark mark='a'/> Here are 3,010 young "
            "American men in 1976, from a survey David Card later used: their average log wage by years of school. "
            f"<bookmark mark='b'/> The points lie roughly on a straight line, about {100 * Mi['card_slope']:.0f} "
            "percent more per year of school, before anything else is taken into account. <bookmark mark='c'/> There "
            "are bumps at twelve and sixteen years, a high-school and a college degree: diplomas themselves seem to "
            "pay."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts, lag_ratio=0.1), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(pts, color=WHITE, scale_factor=1.1))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def equation(self):
        Mi = load("mincer")
        b, se = Mi["b"], Mi["se"]
        eq = MathTex(r"\ln w = \alpha + \rho\,S + \beta_1 X + \beta_2 X^2 + \varepsilon", font_size=44).move_to(
            UP * 2.3)
        x = np.linspace(0, 45, 90)
        prof = b[2] * x + b[3] * x ** 2
        ax = plane([0, 45], [0, 0.7], center=LEFT * 2.6 + DOWN * 1.0, x_length=6.4, y_length=3.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"years of experience",
                   ylabel=r"log wage above a new entrant", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        ln = path(ax, x, prof, WAGE, 3.4)
        pk = dot(ax, Mi["peak_exper"], b[2] * Mi["peak_exper"] + b[3] * Mi["peak_exper"] ** 2, E.ACCENT, 0.08)
        side = VGroup(
            label(rf"$\rho$ = {b[1]:.3f} \ (s.e.\ {se[1]:.3f}): \\ {100 * b[1]:.1f}\% more per year of school",
                  font_size=20, color=SCHOOL),
            label(rf"experience: \ +{100 * b[2]:.1f}\% a year at first, \\ flattening to a peak \\ after "
                  rf"{Mi['peak_exper']:.0f} years", font_size=18, color=WAGE),
            label(rf"{Mi['n']} workers, \ the 1976 CPS; \\ $R^2$ = {Mi['r2']:.2f}", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.4 + DOWN * 0.9)
        tag = data_tag(r"the 1976 Current Population Survey, \ via Wooldridge's data", corner=DR, font_size=12)
        book = VGroup(label(r"1974", font_size=30, color=E.ACCENT),
                      label(r"Jacob Mincer, \ \emph{Schooling, Experience, and Earnings}", font_size=30),
                      label(r"schooling as an investment, \ \ experience as training on the job", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.3).move_to(UP * 0.3)
        terms = label(r"$S$: \ years of school; \ \ $X$: \ years of work since school", font_size=20,
                      color=GREY_A).next_to(eq, DOWN, buff=0.3)
        with self.voiceover(
            "In 1974 Jacob Mincer turned the investment idea into one of the most estimated equations in economics. "
            "<bookmark mark='a'/> The log wage is linear in years of school, and rises with years of experience at a "
            f"diminishing rate. <bookmark mark='b'/> Fitted to {Mi['n']} workers in the 1976 Current Population "
            f"Survey, a year of school is worth {100 * b[1]:.1f} percent, with a standard error under one point. "
            f"<bookmark mark='c'/> Experience adds about {100 * b[2]:.0f} percent a year at first, flattening as "
            f"skills stop growing, to a peak after about {Mi['peak_exper']:.0f} years. <bookmark mark='d'/> The "
            f"equation explains only {100 * Mi['r2']:.0f} percent of the differences in wages: people with the same "
            "schooling and experience earn very different amounts."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(book, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(book), run_time=0.5)
            self.play(Write(eq), FadeIn(terms), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(ax), Create(ln), FadeIn(pk), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def fact(self):
        Mi = load("mincer")
        f = next(x for x in facts.FACTS if x.key == "mincer")
        data_m = label(rf"the 1976 CPS: \\ {100 * Mi['b'][1]:.1f}\% a year; \\ Card's young men: \\ close to a line",
                       font_size=18, color=WHITE)
        theory_m = label(r"human capital: \\ a year of school \\ is an investment \\ repaid in wages", font_size=18,
                         color=SCHOOL)
        agora_m = label(r"least squares on \\ the same data \\ (but is it causal?)", font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, SCHOOL, None)).move_to(UP * 0.3)
        tag = published_tag(r"Becker (1964); \ Mincer (1974); \ Card (1995)", corner=DR, font_size=12)
        with self.voiceover(
            "That makes the shape one of the series' facts. <bookmark mark='a'/> In the data, log wages rise close to "
            "a straight line with schooling. <bookmark mark='b'/> The theory: schooling is an investment repaid in "
            "wages. <bookmark mark='c'/> But a regression cannot tell us whether school makes people more productive, "
            "or whether the more able stay in school longer. The next chapter tries to find out."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()
