from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403

SIG_COLOR = {"0": CAP, "0.5": ATC, "1": OUT, "2": AVC, "inf": LAB}
SIG_NAME = {"0": r"$\sigma = 0$: \ Leontief", "0.5": r"$\sigma = \tfrac12$", "1": r"$\sigma = 1$: \ Cobb--Douglas",
            "2": r"$\sigma = 2$", "inf": r"$\sigma = \infty$: \ perfect substitutes"}


class CobbDouglas(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Cobb and Douglas, \ and the shape of technology", r"What did the 1928 regression find, "
             r"and how much should we believe it?", "Chapter two. Cobb and Douglas, and the shape of technology.",
             lit={1928: r"Cobb and Douglas"}, scale=("firm", "market"), horizon=("a decade",))
        self.refit()
        self.fragile()
        self.ces()
        self.shares()

    def refit(self):
        d = load("douglas")
        Y, L, K = (np.array(d[k], float) for k in ("Y", "L", "K"))
        x, y = np.log(K / L), np.log(Y / L)
        ax = plane([-0.05, 1.05], [-0.1, 0.45], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.0, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.1, 0.2, 0.3, 0.4], xlabel=r"$\log(K/L)$: "
                   r"capital per worker", ylabel=r"$\log(Y/L)$: \ output per worker", font_size=17)
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(xi, yi), radius=0.06, color=OUT) for xi, yi in zip(x, y)])
        yrs = list(d["years"])
        tags = VGroup(*[label(str(yr), font_size=14, color=GREY_B).next_to(dots[yrs.index(yr)], UR, buff=0.03)
                        for yr in (1899, 1908, 1921, 1922)])
        b, c0 = d["crs"]["capital"], d["crs"]["const"]
        line = Line(a.c2p(-0.02, c0 - 0.02 * b), a.c2p(1.02, c0 + 1.02 * b), color=WHITE, stroke_width=2.5)
        side = VGroup(
            label(r"Cobb and Douglas's regression, \ refitted:", font_size=24),
            MathTex(r"\log\frac{Y}{L} = \log A + \beta \log\frac{K}{L}", font_size=36),
            label(rf"slope $\beta$ = {b:.3f}: \ capital's exponent", font_size=24, color=CAP),
            label(rf"labour's: \ $1 - \beta$ = {1 - b:.3f}; \ $A$ = {d['A']:.3f}", font_size=24, color=LAB),
            label(r"constant returns imposed: \ the exponents \\ must add up to one", font_size=22, color=GREY_A),
            label(r"24 years, \ one regression, \ no standard errors \\ reported in 1928", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"data: Cobb and Douglas (1928) via Felipe and Adams (2005); fitted on screen",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Let's refit their regression on their own numbers. <bookmark mark='a'/> Each dot is a year: across, the "
            "log of capital per worker; up, the log of output per worker. <bookmark mark='b'/> With constant returns "
            "imposed, so that the two exponents add up to one, the slope of the line through these points is "
            "capital's exponent. <bookmark mark='c'/> It comes out at nought point two five four, which leaves "
            "nought point seven four six for labour, and a constant of one point oh one. That's the 1928 formula, "
            "recovered exactly. <bookmark mark='d'/> Twenty-four years, one regression, and in the original paper no "
            "standard errors at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.08), FadeIn(tags),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def fragile(self):
        d = load("douglas")
        rows = [(r"constant returns imposed", 1 - d["crs"]["capital"], d["crs"]["capital"], "", WHITE),
                (r"unrestricted", d["unrestricted"]["labour"], d["unrestricted"]["capital"], "", WHITE),
                (r"with a time trend", d["trend"]["labour"], d["trend"]["capital"],
                 rf"trend {100 * d['trend']['trend']:.1f}\% a year", HOLD),
                (r"in growth rates", d["growth"]["labour"], d["growth"]["capital"], "", HOLD),
                (r"1899--1920 only", d["early"]["labour"], d["early"]["capital"], "", HOLD)]
        head = VGroup(label(r"specification", font_size=24, color=GREY_B), label(r"labour", font_size=24, color=LAB),
                      label(r"capital", font_size=24, color=CAP), label(r"", font_size=24))
        xs = [-3.8, 0.2, 2.2, 4.6]
        grid = VGroup()
        for j, h in enumerate(head):
            h.move_to([xs[j], 2.7, 0])
        for i, (name, lab_, cap_, extra, col) in enumerate(rows):
            r_ = VGroup(label(name, font_size=26, color=col), label(f"{lab_:.2f}", font_size=28, color=LAB),
                        label(f"{cap_:+.2f}".replace("-", "$-$").replace("+", ""), font_size=28,
                              color=CAP if cap_ > 0 else HOLD),
                        label(extra, font_size=20, color=GREY_A))
            for j, c in enumerate(r_):
                c.move_to([xs[j], 2.0 - 0.62 * i, 0])
            grid.add(r_)
        rule = Line([-6.3, 2.35, 0], [6.3, 2.35, 0], color=GREY_C, stroke_width=1.5)
        q = quote_card(tables.COBB_DOUGLAS_1928.data["verdict"], r"Felipe and Adams, \emph{Eastern Economic "
                       r"Journal} (2005), p.\ 432", width=11.8, font_size=23, color=HOLD).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Felipe and Adams (2005), table 2, reproduced on screen", corner=DR, font_size=13)
        with self.voiceover(
            "How robust is it? <bookmark mark='a'/> Drop the restriction and estimate both exponents freely: labour "
            "nought point eight one, capital nought point two three, and the restriction isn't rejected. So far, so "
            "good. <bookmark mark='b'/> But output grew partly because technology improved, which the formula "
            "ignores. Add a time trend, as critics soon asked, and capital's exponent turns negative: minus nought "
            "point five three. <bookmark mark='c'/> Estimate in growth rates and it's minus one and a half. Leave "
            "out the last two years and it falls to nought point oh eight. <bookmark mark='d'/> Jesus Felipe and "
            "Gerard Adams, who ran these in 2005, concluded that if Cobb and Douglas had had computers, their "
            "results would have been dismissed. The famous function survived on its convenience, and on its "
            "remarkable agreement with income shares."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(tag), FadeIn(grid[0]))
            vo.wait_until("a")
            self.play(FadeIn(grid[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(grid[2], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(grid[3], shift=RIGHT * 0.1), FadeIn(grid[4], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def ces(self):
        t = load("techs")
        Ls = np.array(t["Ls"])
        ax = plane([0, 3.5], [0, 3.5], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.8, y_length=5.8,
                   xticks=[0, 1, 2, 3], yticks=[0, 1, 2, 3], xlabel=r"labour", ylabel=r"capital", font_size=18)
        curves = VGroup()
        for k in ("0", "0.5", "1", "2", "inf"):
            Ks = np.array(t["curves"][k])
            if k == "0":
                a = ax.ax
                curves.add(VMobject(stroke_color=SIG_COLOR[k], stroke_width=3).set_points_as_corners(
                    [a.c2p(1, 3.5), a.c2p(1, 1), a.c2p(3.5, 1)]))
            else:
                curves.add(path(ax, Ls, Ks, color=SIG_COLOR[k], width=3, xr=(0, 3.5), yr=(0, 3.5),
                                smooth=k != "inf"))
        names = VGroup(*[label(SIG_NAME[k], font_size=20, color=SIG_COLOR[k]) for k in ("0", "0.5", "1", "2",
                                                                                        "inf")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(
            MathTex(r"q = A\,\bigl[s K^{\rho} + (1-s) L^{\rho}\bigr]^{\nu/\rho}, \quad \sigma = \frac{1}{1-\rho}",
                    font_size=32),
            label(r"Arrow, Chenery, Minhas and Solow (1961): \ CES", font_size=21, color=GREY_B),
            label(r"$\sigma$, \ the elasticity of substitution: \\ the percent change in $K/L$ \\ per percent change "
                  r"in $w/r$", font_size=23, color=E.ACCENT),
            names,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Cobb and Douglas's function builds in one particular amount of substitution. To see which, compare "
            "isoquants, all passing through the same point. <bookmark mark='a'/> At one extreme, no substitution at "
            "all: inputs in fixed proportions, Leontief's right angle. At the other, perfect substitutes: a straight "
            "line. <bookmark mark='b'/> In between is the family Kenneth Arrow, Hollis Chenery, Bagicha Minhas and "
            "Robert Solow introduced in 1961: the constant elasticity of substitution, or CES. "
            "<bookmark mark='c'/> Its parameter sigma, the elasticity of substitution, is the percentage change in "
            "the ratio of capital to labour when the wage rises one percent relative to the rental of capital. "
            "<bookmark mark='d'/> Cobb–Douglas is the case sigma equals one. Below one, capital and labour are poor "
            "substitutes; above one, good ones. Whether the true value is above or below one turns out to matter a "
            "great deal."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(curves[0]), Create(curves[4]), FadeIn(names[0]), FadeIn(names[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), Create(curves[1]), Create(curves[3]), FadeIn(names[1]),
                      FadeIn(names[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(curves[2]), FadeIn(names[2]))
        self.clear_scene()

    def shares(self):
        rows = VGroup(
            label(r"with competitive markets, each input is paid its marginal product:", font_size=27),
            MathTex(r"\frac{w L}{p\,q} = \frac{L\,\partial q/\partial L}{q} = b, \qquad \frac{r K}{p\,q} = a",
                    font_size=42, color=OUT),
            label(r"so under Cobb--Douglas the income shares are the exponents, \\ whatever wages and rents do",
                  font_size=26, color=OUT),
            label(r"with $\sigma < 1$, \ cheaper capital raises labour's share; \ with $\sigma > 1$, \ it lowers it",
                  font_size=26, color=E.ACCENT),
            label(r"the falling labour share since 2000 is one reason the value of $\sigma$ is contested: \ "
                  r"chapter 13", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "Here's why it matters. <bookmark mark='a'/> If markets are competitive, each input is paid its marginal "
            "product. <bookmark mark='b'/> Then labour's share of income is the elasticity of output with respect to "
            "labour, which in Cobb–Douglas is just its exponent. <bookmark mark='c'/> So under Cobb–Douglas the "
            "shares are constant, whatever happens to wages and rents. That's why the constant shares of the "
            "twentieth century made it the workhorse. <bookmark mark='d'/> With CES the shares move. If sigma is below "
            "one, capital getting cheaper raises labour's share; if it's above one, it lowers it. "
            "<bookmark mark='e'/> So when labour's share began to fall, the value of sigma became a live question. "
            "Chapter thirteen has the estimates."
        ) as vo:
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
