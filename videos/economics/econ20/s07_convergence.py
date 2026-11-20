from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403

XT = [500, 1000, 3000, 10000, 30000]


def scatter(c, xs, ys, center, title, color=OUTPUT, x_length=6.0, y_length=4.4, yr=(-0.03, 0.08)):
    ax = plane([np.log(300), np.log(60000)], list(yr), center=center, x_length=x_length, y_length=y_length,
               xticks=[np.log(v) for v in XT], yticks=[-0.02, 0, 0.02, 0.04, 0.06, 0.08][:6],
               xlabel=r"GDP per head at the start \ (2021 dollars, \ log)", ylabel=title,
               xfmt=lambda v: commas(np.exp(v)), yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
    dots = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.045, color=color).set_opacity(0.85)
                    for x, y in zip(xs, ys) if yr[0] <= y <= yr[1]])
    return ax, dots


def fit_line(ax, xs, ys, color=E.ACCENT):
    b, a = np.polyfit(xs, ys, 1)
    x0, x1 = min(xs), max(xs)
    return Line(ax.ax.c2p(x0, a + b * x0), ax.ax.c2p(x1, a + b * x1), color=color, stroke_width=4)


class Convergence(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Do poor countries catch up?", r"Do countries that start poorer grow faster, \ as the Solow "
             r"model says they should?", "Chapter six. Do poor countries catch up?",
             lit={1991: r"Barro", 1992: r"MRW", 1995: r"Islam", 1997: r"Pritchett"}, scale=("world",),
             horizon=("decades",))
        self.absolute()
        self.conditional()
        self.mrw()
        self.panels()
        self.fact()

    def absolute(self):
        c = load("convergence")
        d = c["1960-1990"]
        ax, dots = scatter(c, d["ly0"], d["growth"], DOWN * 0.45 + LEFT * 1.5, r"growth of GDP per head a year, "
                           r"1960--1990", x_length=8.4, y_length=5.0)
        line = fit_line(ax, d["ly0"], d["growth"])
        ab = d["absolute"]
        side = VGroup(
            label(rf"{d['n']} countries \\ of a million people or more", font_size=20, color=GREY_A),
            label(rf"slope: \ ${ab['slope']:+.4f}$ \\ (s.e. {ab['se']:.4f})".replace("+", "{+}"), font_size=21,
                  color=E.ACCENT),
            label(r"poorer countries \\ did \emph{not} grow faster", font_size=22, color=HOLD),
            label(r"Pritchett, \ 1997: \\ ``Divergence, big time''", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        src = data_tag(r"Penn World Table 11.0 \ (rgdpna, pop)", corner=DR, font_size=12)
        with self.voiceover(
            "If every country had the same steady state, the Solow model would make a sharp prediction: the further "
            "below it a country starts, the faster it grows. Poor countries would catch up. <bookmark mark='a'/> "
            f"Here are {d['n']} countries with a million people or more, each placed by its income per head in 1960 "
            "and its growth over the next thirty years. <bookmark mark='b'/> If anything, the line slopes up: "
            "richer countries grew a little faster. <bookmark mark='c'/> Over those decades the poor did not catch "
            "up, they fell further behind. <bookmark mark='d'/> Lant Pritchett summed up two centuries of it in the "
            "title of a 1997 paper: divergence, big time."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.02), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def conditional(self):
        c = load("convergence")
        d = c["1960-2019"]
        left, ldots = scatter(c, d["ly0"], d["growth"], LEFT * 3.5 + DOWN * 0.5, r"growth a year, \ 1960--2019",
                              x_length=5.6, y_length=4.2, yr=(-0.03, 0.07))
        lline = fit_line(left, d["ly0"], d["growth"])
        right, rdots = scatter(c, d["partial_ly0"], d["partial_growth"], RIGHT * 3.4 + DOWN * 0.5,
                               r"growth a year, \ net of the controls", color=CAPITAL, x_length=5.6, y_length=4.2,
                               yr=(-0.03, 0.07))
        rline = fit_line(right, d["partial_ly0"], d["partial_growth"])
        ab, co = d["absolute"], d["conditional"]
        tl = label(rf"no controls: \ slope ${ab['slope']:+.4f}$ \ ({ab['se']:.4f})".replace("+", "{+}"),
                   font_size=18, color=OUTPUT).next_to(left, UP, buff=0.2)
        tr = label(rf"holding investment, \ population growth \ and schooling fixed: \ ${co['slope']:+.4f}$ \ "
                   rf"({co['se']:.4f})".replace("+", "{+}"), font_size=18, color=CAPITAL).next_to(right, UP, buff=0.2)
        if tr.width > 6.6:
            tr.width = 6.6
        res = label(rf"implied speed: \ $\lambda = {pc(co['lambda'])}$ a year \ $\cdot$ \ half-life about "
                    rf"{np.log(2) / co['lambda']:.0f} years", font_size=23, color=E.ACCENT).to_edge(DOWN, buff=0.25)
        tag = published_tag(r"Barro, QJE 106(2) (1991): \ 98 countries, \ 1960--1985", corner=UR, font_size=12)
        barro = label(r"Barro, \ 1991: \ compare countries with the same saving, \ population growth and schooling",
                      font_size=20, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "But the model does not say all countries have the same steady state. A country that saves little, "
            "whose population grows fast, or whose people have little schooling, should be heading for a lower one. "
            "<bookmark mark='a'/> Robert Barro's answer, in 1991, was to compare countries holding those things "
            "fixed. <bookmark mark='b'/> On the left, sixty years of the newest data with no controls: "
            "<bookmark mark='c'/> almost no slope. Rich and poor grew at about the same rate on average. "
            "<bookmark mark='d'/> On the right, the same growth and the same starting incomes, each net of the "
            "country's investment rate, population growth and schooling in 1960. <bookmark mark='e'/> Now the line "
            "slopes down clearly. Among countries with similar saving, population growth and schooling, the poorer "
            "grew faster. <bookmark mark='f'/> The slope implies that each country closed about "
            f"{100 * co['lambda']:.1f} percent of the gap to its own steady state each year: a half-life of about "
            f"{np.log(2) / co['lambda']:.0f} years. That is conditional convergence."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(FadeIn(barro))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dt) for dt in ldots], lag_ratio=0.02), run_time=2)
            vo.wait_until("c")
            self.play(Create(lline), FadeIn(tl))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(dt) for dt in rdots], lag_ratio=0.02), run_time=2)
            vo.wait_until("e")
            self.play(Create(rline), FadeIn(tr))
            vo.wait_until("f")
            self.play(FadeOut(barro), FadeIn(res, shift=UP * 0.1))
        self.clear_scene()

    def mrw(self):
        lit = load("convergence")["lit"]
        left = VGroup(
            label(r"Mankiw, \ Romer \ and Weil, \ 1992", font_size=27, color=E.ACCENT),
            MathTex(r"\ln y^\ast = \text{const} + \frac{\alpha}{1-\alpha}\ln s - \frac{\alpha}{1-\alpha}"
                    r"\ln(n+g+\delta)", font_size=34),
            label(rf"98 non-oil countries, \ 1985: \ $R^2 = {lit['mrw_r2_textbook']:.2f}$, \ but the slopes imply "
                  rf"$\alpha \approx {lit['mrw_alpha_textbook']:.2f}$", font_size=21, color=OUTPUT),
            label(r"add human capital, \ $Y = K^\alpha H^\beta (AL)^{1-\alpha-\beta}$, \ schooling as its saving "
                  r"rate:", font_size=21, color=GREY_A),
            label(rf"$\alpha = {lit['mrw_alpha']:.2f}$, \ $\beta = {lit['mrw_beta']:.2f}$, \ "
                  rf"$R^2 = {lit['mrw_r2_aug']:.2f}$", font_size=24, color=HUMAN),
            label(rf"and the speed of convergence: \ {pc(lit['mrw_lambda_nonoil'], 2)} a year \ (OECD: "
                  rf"{pc(lit['mrw_lambda_oecd'], 2)})", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"Mankiw, Romer and Weil, QJE 107(2) (1992): \ 407--437, \ tables I, II and V",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The most famous test came a year later. <bookmark mark='a'/> Gregory Mankiw, David Romer and David "
            "Weil took the steady state itself to the data: log income should rise with the log of the saving rate "
            "and fall with the log of population growth plus g plus delta, with matching coefficients alpha over one "
            "minus alpha. <bookmark mark='b'/> Across ninety-eight countries, saving and population growth alone "
            f"explained {100 * lit['mrw_r2_textbook']:.0f} percent of the differences in income. But the "
            f"coefficients implied a capital share of about {lit['mrw_alpha_textbook']:.2f}, twice the national "
            "accounts' third. <bookmark mark='c'/> So they added human capital, accumulated like physical capital, "
            "with the share of the working-age population in secondary school as its saving rate. "
            f"<bookmark mark='d'/> Now physical capital's share came out at {lit['mrw_alpha']:.2f}, human capital's "
            f"at {lit['mrw_beta']:.2f}, and the model explained {100 * lit['mrw_r2_aug']:.0f} percent of the "
            "variation. Broad capital, the two together, has a share near three fifths. <bookmark mark='e'/> And "
            f"countries converged at about {100 * lit['mrw_lambda_nonoil']:.1f} percent a year: slower than the "
            "textbook, as a large broad share says it should be."
        ) as vo:
            self.play(FadeIn(left[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left[1]))
            vo.wait_until("b")
            self.play(FadeIn(left[2]))
            vo.wait_until("c")
            self.play(FadeIn(left[3]))
            vo.wait_until("d")
            self.play(FadeIn(left[4]))
            vo.wait_until("e")
            self.play(FadeIn(left[5]))
        self.clear_scene()

    def panels(self):
        lit = load("convergence")["lit"]
        rows = VGroup(
            label(r"but each country may have its own steady state, \ for reasons no regression measures", font_size=24,
                  color=GREY_A),
            label(rf"Nazrul Islam, \ 1995: \ five-year panels with a constant for each country \ $\Rightarrow$ \ "
                  rf"$\lambda \approx {pc(lit['islam_lambda_nonoil'], 1)}$", font_size=23, color=E.ACCENT),
            label(r"faster, \ because now each country converges to its \emph{own} level, \ wherever that is",
                  font_size=23, color=GREY_A),
            label(r"but with short panels a constant for each country pushes the estimated speed up \ (Nickell, "
                  r"1981)", font_size=20, color=HOLD),
            label(r"Quah, \ 1996: \ perhaps no single path at all, \ but clubs: \ twin peaks of rich and poor",
                  font_size=23, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Islam, QJE 110(4) (1995), \ table IV; \ Nickell, Econometrica 49(6) (1981); \ "
                            r"Quah, EJ 106(437) (1996)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The controls are only what can be measured. <bookmark mark='a'/> Each country may have its own steady "
            "state, set by its institutions, geography or culture. <bookmark mark='b'/> In 1995 Nazrul Islam cut the "
            "same data into five-year panels and gave every country its own constant. The speed of convergence "
            f"jumped to about {100 * lit['islam_lambda_nonoil']:.0f} percent a year, close to the textbook's. "
            "<bookmark mark='c'/> That is not a contradiction: now each country is converging to its own level, "
            "not to one predicted from its saving and schooling. <bookmark mark='d'/> Panels this short have a bias "
            "of their own: with a constant for every country, the estimated speed is pushed upward, as Stephen "
            "Nickell showed in 1981, so the truth may lie between. <bookmark mark='e'/> And Danny Quah argued that the world "
            "is not converging to one distribution but splitting into clubs: twin peaks of the rich and the poor. "
            "Conditional convergence is a fact. Whether the poor catch up is another question."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.12))
        self.clear_scene()

    def fact(self):
        co = load("convergence")["1960-2019"]["conditional"]
        f = next(x for x in facts.FACTS if x.key == "conditional_convergence")
        data_m = label(rf"holding saving, \ population growth \\ and schooling fixed: \\ about {pc(co['lambda'])} a "
                       rf"year; \\ with no controls, \ none", font_size=19, color=WHITE)
        agora_m = label(r"a Solow economy below \\ its own steady state \\ grows faster, \ the further \\ below it is",
                        font_size=19, color=E.AGORA)
        guess_m = label(r"did you expect \\ the poor to catch up?", font_size=19, color=E.ACCENT)
        fc = fact_card(tex_safe(f.statement), columns=((r"your guess", guess_m), (r"the data", data_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22)
        fc.move_to(UP * 0.1)
        with self.voiceover(
            "That goes on the list of facts. <bookmark mark='a'/> Poor countries grow faster than rich ones once "
            "saving and schooling are held fixed, and not otherwise. <bookmark mark='b'/> The data column: about "
            f"{100 * co['lambda']:.1f} percent a year with the controls, nothing without them. "
            "<bookmark mark='c'/> And Agora's column is filled by the model of this part: an economy below its own "
            "steady state grows faster the further below it starts."
        ) as vo:
            self.play(FadeIn(fc))
            vo.wait_until("c")
            self.play(Indicate(agora_m, color=WHITE))
        self.clear_scene()
