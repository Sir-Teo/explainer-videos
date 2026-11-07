from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.rates()
        self.kde()
        self.question()
        self.game()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1972, 1980)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"Part 29: \ a kernel density estimate's error $\asymp n^{-4/5}$, \ for twice-differentiable densities", font_size=26),
            label(r"could a cleverer method do better? \ $n^{-1}$, \ like a parametric model?", font_size=26, color=GREY_A),
            label(r"1972: \ Farrell: \ no: \ at a point, \ no estimator beats $n^{-2s/(2s+1)}$ uniformly", font_size=26, color=LOWC),
            label(r"1980: \ Stone: \ for $s$ derivatives in $d$ dimensions, \ the rate is $n^{-2s/(2s+d)}$, \ for every method", font_size=26, color=LOWC),
            label(r"a speed limit, \ and the curse of dimensionality, \ as theorems", font_size=26, color=HYPC),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In Part twenty-nine a kernel density estimate's squared error shrank like n to the minus four fifths for a density with two derivatives, slower than the one over n of a parametric model. <bookmark mark='b'/> The natural question is whether a cleverer method could do better. <bookmark mark='c'/> In 1972 Roger Farrell proved that it cannot: at a single point, no estimator, of any kind, beats that rate uniformly over the smoothness class. <bookmark mark='d'/> In 1980 Charles Stone found the general law: with s derivatives in d dimensions, over the specified bounded smoothness class, the minimax squared-error rate is n to the minus two s over two s plus d, for every method whatsoever. <bookmark mark='e'/> It is a speed limit, and it turns the curse of dimensionality from a slogan into a theorem. It also changed what statisticians try to prove about their methods: not just that an estimator converges, but that it converges as fast as anything possibly could."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rates(self):
        d = load("hook")
        ln = np.log10(d["ns"])
        A = axes([2, 6], [-6.2, 0], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ of the minimax risk",
                 xticks=[2, 3, 4, 5, 6], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-6, -4, -2, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"2_1": UPC, "2_2": S.ALT, "2_4": HYPC, "2_8": LOWC, "4_8": LINC}
        cs = {k: polyline(ax, ln, np.log10(d["curves"][k]), c, 4) for k, c in cols.items()}
        par = DashedLine(ax.c2p(2, -2), ax.c2p(6, -6), color=TRUTHC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"white dashed: \ parametric, \ $n^{-1}$", font_size=22, color=TRUTHC),
            label(r"blue: \ $s = 2$, \ $d = 1$: \ $n^{-4/5}$", font_size=22, color=UPC),
            label(r"teal, \ gold, \ red: \ $d = 2, 4, 8$", font_size=22, color=HYPC),
            label(r"$d = 8$: \ $n^{-1/3}$: \ a million points act like a hundred", font_size=22, color=LOWC),
            label(r"purple: \ $s = 4$, \ $d = 8$: \ smoothness buys some back", font_size=22, color=LINC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are Stone's rates. The dashed line is the parametric one over n. <bookmark mark='b'/> "
            "With two derivatives in one dimension the rate is n to the minus four fifths, a little slower. <bookmark "
            "mark='c'/> In two, four and eight dimensions it gets steadily worse. <bookmark mark='d'/> In eight dimensions "
            "it is n to the minus a third: a million observations are worth about what a hundred are in a parametric "
            "problem. <bookmark mark='e'/> More smoothness helps: with four derivatives in eight dimensions the rate is back "
            "to n to the minus a half. The only ways around the curse are more smoothness or more structure."
        ) as vo:
            self.play(FadeIn(A), Create(par), FadeIn(exact_tag(r"exact: \ the rates")))
            for k, (m_, key) in enumerate(zip("abcde", [None, "2_1", None, "2_8", "4_8"])):
                vo.wait_until(m_)
                anims = [FadeIn(side[k])]
                if key == "2_1":
                    anims.insert(0, Create(cs["2_1"]))
                if m_ == "c":
                    anims = [Create(cs["2_2"]), Create(cs["2_4"]), Create(cs["2_8"]), FadeIn(side[k])]
                if key == "4_8":
                    anims.insert(0, Create(cs["4_8"]))
                self.play(*anims)
        self.clear_scene()

    def kde(self):
        d = load("hook")
        ln = np.log10([r["n"] for r in d["sim"]])
        mse = np.log10([r["mse"] for r in d["sim"]])
        A = axes([1.8, 4.0], [-5.4, -2.6], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ MSE of $\hat f(0)$",
                 xticks=[2, 3, 4], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-5, -4, -3], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = VGroup(polyline(ax, ln, mse, UPC, 4), *[Dot(ax.c2p(a, b), radius=0.09, color=UPC) for a, b in zip(ln, mse)])
        u = np.linspace(1.9, 3.9, 50)
        ref = DashedLine(ax.c2p(u[0], mse[0] - 0.8 * (u[0] - ln[0])), ax.c2p(u[-1], mse[0] - 0.8 * (u[-1] - ln[0])), color=LOWC, stroke_width=2.5)
        slope = (mse[-1] - mse[0]) / (ln[-1] - ln[0])
        side = fit_rows(VGroup(
            label(r"$N(0,1)$ data: \ a kernel estimate of $f(0)$", font_size=22),
            label(r"blue: \ its simulated MSE, \ bandwidth $1.06\,n^{-1/5}$", font_size=22, color=UPC),
            label(rf"slope {slope:.2f}", font_size=22, color=UPC),
            label(r"red dashed: \ slope $-4/5$, \ Farrell's limit", font_size=22, color=LOWC),
            label(r"approaching $-4/5$: \ one-density illustration; \ uniform bound in chapter 3", font_size=22, color=ADAPTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A pointwise illustration of the rate, rather than a uniform upper-bound proof. A kernel estimate of a normal density at zero, <bookmark mark='b'/> with its simulated mean squared error from a hundred to six thousand four hundred observations. <bookmark mark='c'/> On log scales the slope is {say(slope, 2)}, close to minus four fifths and steepening towards it as n grows: <bookmark mark='d'/> this normal-density example has the same asymptotic exponent as the class-wide minimax rate. A result at one density does not establish a uniform upper bound; chapter three supplies a genuine class-wide KDE bound. <bookmark mark='e'/> When the two meet, the rate is settled. This part builds the tools for the lower half, which is the hard one."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ref), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"the minimax risk: \ $\inf_{\hat\theta} \sup_{\theta \in \Theta} E_\theta\, \ell(\hat\theta, \theta)$", font_size=30),
            label(r"upper bound: \ exhibit one method and bound its worst case", font_size=26, color=UPC),
            label(r"lower bound: \ show that \emph{every} method has a bad case: \ reduce estimation to testing", font_size=26, color=LOWC),
            label(r"the tools: \ Le Cam's two points, \ Fano's many, \ Assouad's hypercube", font_size=26, color=HYPC),
            label(r"and the surprises: \ exact constants, \ adaptation, \ and rates no fast algorithm can reach", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The quantity of this part is the minimax risk: the best, over all estimators, of the worst "
            "risk over the parameter set. <bookmark mark='b'/> To bound it above, exhibit one method and control its worst "
            "case: that is what most of statistics does. <bookmark mark='c'/> To bound it below, show that every method has "
            "a bad case. The trick is to reduce estimation to testing: if two parameter values far apart produce nearly the "
            "same data, no estimator can tell which is true. <bookmark mark='d'/> The tools are Le Cam's method with two "
            "hypotheses, Fano's with many, and Assouad's with a hypercube of them. <bookmark mark='e'/> And there are "
            "surprises: exact constants, estimators that adapt to unknown smoothness, and rates that are possible in "
            "principle but seem out of reach for any efficient algorithm."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def game(self):
        rows = [
            cmath(r"\text{the statistician}", r":", r"\text{chooses } \hat\theta; \ \ \text{nature chooses } \theta \in \Theta", font_size=34),
            cmath(r"\inf_{\hat\theta} \sup_\theta R(\hat\theta, \theta)", r"\ge", r"\sup_\pi \inf_{\hat\theta} \textstyle\int R(\hat\theta, \theta)\, d\pi(\theta): \ \text{minimax} \ge \text{Bayes}", font_size=30),
            cmath(r"\text{a lower bound}", r":", r"\text{any prior's Bayes risk; \ the best is the least favourable}", font_size=32),
            cmath(r"\text{this part}", r":", r"\text{priors on two points, \ on packings, \ on cubes, \ Gaussian priors}", font_size=32),
        ]
        rows[1][-1].set_color(LOWC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"Wald's game, \ Part 45"), why(r"weak duality"), why(r"Part 45's least favourable prior"), why(r"every lower bound here")]
        heading = label('A supported prior turns a worst-case risk into a lower bound', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Minimax theory is Part forty-five's decision theory taken to infinite dimensions. The statistician picks an estimator; nature picks the parameter. <bookmark mark='b'/> For any prior on the parameter set, the worst-case risk of an estimator is at least its average risk under that prior, and so the minimax risk is at least the prior's Bayes risk. <bookmark mark='c'/> The lower-bound methods use prior-average testing or estimation risks for carefully chosen supported priors, and the best possible one comes from the least favourable prior. <bookmark mark='d'/> Le Cam's method puts the prior on two points, Fano's on a packing, Assouad's on the vertices of a cube, and the asymptotic Pinsker proof uses a Gaussian prior with slack and controlled truncation into the ellipsoid. The art is in the choice of prior."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(29, r"bandwidths, \ and the rate $n^{-4/5}$", r"that no smoother could do better",
                         r"chapters 3--5: \ Le Cam, \ Fano, \ Assouad: \ the rate is optimal"),
            upgrade_card(47, r"Hájek's local minimax theorem at root-$n$", r"a regular, \ root-$n$ problem",
                         r"chapter 2: \ Pinsker's exact constant, \ for nonparametric rates"),
            upgrade_card(49, r"the efficient bound for smooth functionals", r"that root-$n$ is achievable",
                         r"chapters 3, \ 6: \ when it is not, \ the rate itself"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are due. Part twenty-nine chose bandwidths and found the rate n to the "
            "minus four fifths, but took on trust that no smoother could do better; chapters three to five prove it. "
            "<bookmark mark='b'/> Part forty-seven's local minimax theorem lives at the root n scale; chapter two finds an "
            "exact minimax constant at nonparametric rates. <bookmark mark='c'/> And Part forty-nine's efficiency bound "
            "assumed root n was achievable; when it is not, this part finds the rate itself."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 50", font_size=34, color=GREY_B), label(r"Minimax Theory", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the Gaussian sequence model, \ and its connections to regular regression and density models",
            r"Pinsker's exact minimax risk; \ Le Cam's, \ Fano's and Assouad's lower bounds",
            r"upper bounds that match: \ blockwise James--Stein, \ thresholding; \ Lepski's adaptation",
            r"minimax testing and higher criticism; \ statistical--computational gaps",
        ], color=HYPC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 29, \ 45, \ 47").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.gsm}, \ the lower-bound workbench").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty: minimax theory, the limits of estimation. <bookmark mark='b'/> We'll meet the Gaussian sequence model and see why it stands for regression and density estimation; find Pinsker's exact linear minimax risk and asymptotic unrestricted constant; build lower bounds by Le Cam's, Fano's and Assouad's methods on a workbench of packed hypotheses; match them with blockwise James–Stein and thresholding; adapt to unknown smoothness with Lepski's method; test for sparse signals with higher criticism; and end at the frontier where statistics meets computational complexity."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
