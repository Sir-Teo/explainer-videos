from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.brewer()
        self.brewery()
        self.cards()
        self.result()
        self.objectives()

    def brewer(self):
        tl = timeline(lit=(1908,)).to_edge(UP, buff=0.35)
        hc = history_card(1908, r"``Student'' (William Sealy Gosset), \ ``The probable error of a mean''",
                          r"\emph{Biometrika} 6: \ a brewer at Arthur Guinness \& Son, Dublin, \ who could only afford small samples \ "
                          r"\textemdash{} and Guinness let him publish only under a pen name", color=S.MUSEUM, width=8.4,
                          font_size=24).move_to([0, 0.7, 0])
        rows = fit_rows(VGroup(
            label(r"the trouble: \ with 4 barley plots, \ $s$ is a poor stand-in for $\sigma$", font_size=26),
            MathTex(r"\bar x \pm 1.96\,\frac{s}{\sqrt n} \quad \text{is too narrow when } n \text{ is small}", font_size=30, color=RESID),
        ), 12.6, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "In 1899 the Guinness brewery in Dublin hired a young chemist, William Sealy Gosset, to make its beer "
            "more consistent. <bookmark mark='a'/> His experiments were small: four plots of barley, a handful of "
            "malting trials. And the statistics of the day were built for large samples, where the sample's standard "
            "deviation could simply stand in for the true one. <bookmark mark='b'/> With four observations it can't. "
            "The standard deviation of four numbers is itself wildly variable, so the usual interval, the mean plus "
            "or minus one point nine six standard errors, is too narrow. Guinness let him publish the answer in 1908, "
            "but only under a pen name: Student."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def cards(self):
        d = load("student")
        hts, cnt = np.asarray(d["heights"]), np.asarray(d["counts"])
        A = axes([140, 197], [0, 480], x_length=6.0, y_length=3.6, xlabel=r"height (cm; whole inches)", ylabel=r"men",
                 xticks=[145, 160, 175, 190], yticks=[0, 200, 400], center=[-3.4, 0.6, 0])
        bars_ = VGroup()
        for h, c in zip(hts, cnt):
            lo, hi = A.ax.c2p(h - 1.1, 0), A.ax.c2p(h + 1.1, c)
            bars_.add(Rectangle(width=hi[0] - lo[0], height=max(1e-3, hi[1] - lo[1]), stroke_width=0, fill_color=DATA,
                                fill_opacity=0.8).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
        src = historical_tag(r"Macdonell (1902): \ 3,000 criminals' heights", corner=DL)
        first = np.asarray(d["first"])
        cards = VGroup()
        for i in range(3):
            for j in range(4):
                c = VGroup(RoundedRectangle(width=1.05, height=0.62, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5,
                                            fill_color="#1b2130", fill_opacity=1),
                           MathTex(f"{first[i, j]:.1f}", font_size=22, color=DATA))
                c[1].move_to(c[0])
                c.move_to([1.0 + 1.12 * j, 2.2 - 1.0 * i, 0])
                cards.add(c)
        means = VGroup(*[MathTex(rf"\bar x = {first[i].mean():.1f}", font_size=24, color=SIM).move_to([5.9, 2.2 - 1.0 * i, 0])
                         for i in range(3)])
        dots = MathTex(r"\vdots \quad 750 \text{ samples of } 4", font_size=28, color=GREY_A).move_to([3.0, -0.9, 0])
        rows = fit_rows(VGroup(
            label(r"3,000 cards, \ one per man", font_size=24),
            label(r"shuffled, \ and dealt in fours", font_size=24),
            label(r"for each four: \ $t = (\bar x - \mu) \big/ (s/\sqrt 4)$", font_size=24, color=SIM),
        ), 6.0, 0.22, [-3.4, -2.75, 0])
        with self.voiceover(
            "How do you check a theory of small samples in 1908, with no computer? <bookmark mark='a'/> Gosset used "
            "a table published six years earlier by William Macdonell: the heights of three thousand men in English "
            "prisons, measured to the inch. <bookmark mark='b'/> He wrote each man's height on a piece of card, "
            "three thousand cards. Shuffled them thoroughly. <bookmark mark='c'/> And dealt them out in fours: seven "
            "hundred and fifty samples of four men. <bookmark mark='d'/> For each four he computed the mean, the "
            "standard deviation, and the ratio of the mean's error to its estimated standard error. It was the first "
            "Monte Carlo study of a statistical method, done by hand."
        ) as vo:
            self.play(FadeIn(A), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.04))
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.08))
            vo.wait_until("d")
            self.play(FadeIn(means), FadeIn(dots), FadeIn(rows[2]))
        self.clear_scene()

    def result(self):
        d = load("student")
        ed, hist = np.asarray(d["edges"]), np.asarray(d["hist"])
        t_ = load("tdist")
        xs = np.asarray(t_["xs"])
        A = axes([-6, 6], [0, 0.45], x_length=7.6, y_length=4.4, xlabel=r"$t = (\bar x - \mu)/(s/\sqrt 4)$",
                 xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[0, 0.2, 0.4], center=[-2.0, -0.4, 0])
        ax = A.ax
        h = hist_bars(ax, ed, np.clip(hist, 0, 0.45), color=DATA, opacity=0.65)
        nrm = curve(ax, xs, np.asarray(t_["normal"]), NORMAL, 3)
        t3 = curve(ax, xs, np.asarray(t_["pdf"]["3"]), EXACT, 3.5)
        leg = legend([(NORMAL, r"the normal curve"), (EXACT, r"Student's curve, \ $t_3$")], font_size=22).move_to([4.6, 2.1, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"\bar x \pm 1.96\,s/\sqrt 4:\ \ \text{{covers }} {100 * d['cover_z']:.1f}\%", font_size=28, color=RESID),
            MathTex(rf"\bar x \pm 3.18\,s/\sqrt 4:\ \ \text{{covers }} {100 * d['cover_t']:.1f}\%", font_size=28, color=EXACT),
            label(r"heavier tails: \ $s$ is sometimes far too small", font_size=24, color=GREY_A),
            MathTex(rf"\text{{World, 3{{,}}000 residents: }} {100 * d['world_cover_z']:.1f}\% \text{{ vs }} {100 * d['world_cover_t']:.1f}\%",
                    font_size=24, color=GREY_A),
        ), 5.2, 0.3, [4.3, -0.4, 0])
        tag = historical_tag(r"750 samples of 4 from Macdonell's men, \ one shuffle (seed 1908)", corner=DR)
        with self.voiceover(
            "Here is the result, redone with one seeded shuffle of the same three thousand heights. "
            "<bookmark mark='a'/> The histogram of the seven hundred and fifty ratios is not the normal curve: it's "
            "narrower in the middle and much heavier in the tails. <bookmark mark='b'/> The usual interval, with one "
            f"point nine six, covers the true mean only {100 * d['cover_z']:.0f} percent of the time, not ninety-five. "
            "<bookmark mark='c'/> Gosset found the right curve, partly by inspired guesswork that Fisher later made "
            "rigorous: Student's t distribution with three degrees of freedom, in gold, which follows the histogram. Its multiplier is three point one eight, and with it the "
            f"interval covers {100 * d['cover_t']:.0f} percent; slightly over, because the heights were rounded to "
            "whole inches. <bookmark mark='d'/> The same experiment on three thousand residents of the World tells the "
            "same story. The tails are heavy because, now and then, four men happen to be similar in height, s comes "
            "out far too small, and the ratio explodes."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.02), Create(nrm), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(t3), FadeIn(leg[1]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 8", font_size=34, color=GREY_B), label(r"From Sample to Population", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"sampling distributions and standard errors: \ the sampling machine",
            r"why $n - 1$; \ Fisher's geometry of the sample; \ $\chi^2$, \ $t$ and $F$ derived",
            r"bias, variance and mean squared error; \ consistency; \ plug-in estimators",
            r"standard errors for ratios: \ Laplace's census of France (1802); \ finite populations",
            r"the Coverage Board opens: \ which textbook intervals keep their promise?",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 4, 6 and 7").to_corner(DL, buff=0.3)
        built = label(r"Built in this part: \ the first rows of the Coverage Board", font_size=28, color=S.ACCENT)
        built.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part asks how much an estimate wobbles, and how a single sample can tell you. "
            "<bookmark mark='a'/> Part eight: from sample to population. <bookmark mark='b'/> We'll watch sampling "
            "distributions form; see why the variance divides by n minus one; follow Fisher into n dimensions, "
            "where chi-squared, t and F all fall out of one picture; weigh bias against variance; build standard "
            "errors for ratios, as Laplace did to count France; correct for small populations; and finally open the "
            "Coverage Board, where textbook intervals are tested against the truth. <bookmark mark='c'/> Some of them "
            "fail."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("c")
            self.play(obj.animate.shift(UP * 0.4), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def brewery(self):
        rows = fit_rows(VGroup(
            label(r"1904: \ Gosset's internal report, \ ``The application of the `law of error' to the work of the brewery''",
                  font_size=24, color=S.MUSEUM),
            label(r"barley varieties, \ hop resins, \ yeast counts: \ experiments of a few runs each", font_size=24),
            label(r"1906--07: \ a year in Karl Pearson's laboratory in London, \ learning the large-sample theory \ \ldots", font_size=24),
            label(r"\ldots{} \ and seeing that it did not fit a brewer's samples", font_size=24, color=RESID),
            label(r"1907: \ counting yeast cells with a haemocytometer \ \textemdash{} \ he rediscovered the Poisson law (Part 3)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.36, [0, 0.2, 0])
        with self.voiceover(
            "Gosset's problems were real ones. <bookmark mark='a'/> In a 1904 report to the Guinness board he set out "
            "to apply the law of error to the work of the brewery. <bookmark mark='b'/> His experiments compared barley "
            "varieties, hop resins, and yeast, each with only a few runs, because each run was a season's crop or a "
            "brew. <bookmark mark='c'/> In 1906 the company sent him to spend a year in Karl Pearson's laboratory in "
            "London, where he learned the theory of the day, <bookmark mark='d'/> and saw that it was built for samples "
            "of hundreds, not a brewer's handful. <bookmark mark='e'/> The same year he studied counts of yeast cells "
            "under a microscope, and rediscovered the Poisson distribution of Part 3."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
