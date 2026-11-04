from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403

CHI_COLS = {"1": "#9FB4C7", "2": "#7BD88F", "3": "#F2C14E", "5": "#FF9F5A"}


class Sampling(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.chisq()
        self.student()
        self.fisher()
        self.lighthouse()
        self.tree_voiceover("Six arrows for the sampling family: <bookmark mark='t'/> squares of normals give chi-squared, "
                            "a special gamma; a normal over the root of a chi-squared gives Student's t; a ratio of "
                            "chi-squareds gives F; t with one degree of freedom is Cauchy, and with infinitely many, "
                            "the normal.", 8)

    def card(self):
        card = chapter_card(8, r"The sampling family", r"The distributions that statistics itself creates",
                            lit=(1908,), part=PART)
        with self.voiceover("Chapter eight. The sampling family."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def chisq(self):
        d = load("sampling")
        xs = np.asarray(d["xs"])
        A = axes([0, 12], [0, 0.6], x_length=7.4, y_length=4.2, xlabel=r"$x$", xticks=[0, 2, 4, 6, 8, 10, 12],
                 yticks=[0, 0.25, 0.5], center=[-2.4, -0.4, 0])
        ax = A.ax
        curves = VGroup(*[curve(ax, xs, np.clip(np.asarray(d["chi"][k]), 0, 0.6), CHI_COLS[k], 3) for k in ("1", "2", "3", "5")])
        labs = VGroup(*[label(rf"$k = {k}$", font_size=22, color=CHI_COLS[k]) for k in ("1", "2", "3", "5")])
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(10.5, 0.45))
        s3 = np.asarray(d["s3"])
        ed = np.linspace(0, 12, 49)
        h = hist_bars(ax, ed, np.histogram(s3, ed)[0] / (len(s3) * np.diff(ed)), color=SIM, opacity=0.4)
        dfn = definition_card(r"Chi-squared, $k$ degrees of freedom", r"$\chi^2_k = Z_1^2 + \cdots + Z_k^2$, \ "
                              r"independent standard normals; \ mean $k$, variance $2k$", color=CONT, width=5.4,
                              font_size=22).move_to([4.3, 2.4, 0])
        hc = label(r"Helmert (1876): \ the law of the sample variance; \ Pearson (1900): \ the $\chi^2$ test", font_size=22,
                   color=GREY_B).move_to([4.3, 0.9, 0])
        if hc.width > 5.4:
            hc.width = 5.4
        chk = MathTex(rf"k = 3:\ \ \text{{simulated mean }} {d['s3_mean']:.2f},\ \text{{variance }} {d['s3_var']:.2f}",
                      font_size=24, color=SIM).move_to([4.3, 0.1, 0])
        gam = MathTex(r"\chi^2_k", r"=", r"\text{gamma}\left(\tfrac k2,\ 2\right)", font_size=32, color=EXACT)
        gam.move_to([4.3, -1.0, 0])
        with self.voiceover(
            "Some distributions are created by statistics itself, as the laws of the quantities we compute from "
            "normal data. <bookmark mark='a'/> The first is the sum of k squared independent standard normals: "
            "chi-squared with k degrees of freedom. Its mean is k, since each square has mean one, and its "
            "variance two k. <bookmark mark='b'/> Here it is for one, two, three and five degrees of freedom. "
            "<bookmark mark='c'/> Twenty thousand sums of three simulated squares fall right on the curve for k "
            "equals three. <bookmark mark='d'/> Friedrich Helmert found it in 1876 as the law of the sample "
            "variance, and Karl Pearson in 1900 made it the basis of his famous test. <bookmark mark='e'/> And it's "
            "a relative we already know: chi-squared is a gamma, with shape k over two and scale two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(labs), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(h), FadeIn(chk))
            vo.wait_until("d")
            self.play(FadeIn(hc))
            vo.wait_until("e")
            self.play(Write(gam))
        self.clear_scene()

    def student(self):
        d = load("sampling")
        ts = np.asarray(d["ts"])
        A = axes([-5, 5], [0, 0.42], x_length=7.4, y_length=4.2, xlabel=r"$t$", xticks=[-4, -2, 0, 2, 4],
                 yticks=[0, 0.2, 0.4], center=[-2.4, -0.4, 0])
        ax = A.ax
        cols = {"1": S.RESID, "3": S.ACCENT, "30": S.LIK}
        nc = curve(ax, ts, np.asarray(d["normal"]), GREY_A, 4)
        tc = {k: curve(ax, ts, np.asarray(d["tden"][k]), c, 3) for k, c in cols.items()}
        leg = legend([(GREY_A, r"normal"), (cols["30"], r"$\nu = 30$"), (cols["3"], r"$\nu = 3$"),
                      (cols["1"], r"$\nu = 1$")], font_size=22).move_to(ax.c2p(3.6, 0.33))
        hc = history_card(1908, r"W. S. Gosset (``Student''), \ Guinness brewery, Dublin",
                          r"small samples of barley and yeast: \ the mean over its \emph{estimated} standard error",
                          color=S.MUSEUM, width=5.4, font_size=22).move_to([4.3, 2.3, 0])
        f = MathTex(r"T = \frac{Z}{\sqrt{V/\nu}}", r",\quad V \sim \chi^2_\nu", font_size=32, color=EXACT).move_to([4.3, 0.4, 0])
        notes = VGroup(label(r"heavier tails: \ uncertainty about $\sigma$", font_size=22, color=GREY_A),
                       label(r"$\nu \to \infty$: \ the normal", font_size=22, color=cols["30"]),
                       label(r"$\nu = 1$: \ the Cauchy", font_size=22, color=cols["1"])).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.15)
        notes.move_to([4.3, -1.2, 0])
        with self.voiceover(
            "The second was found in a brewery. <bookmark mark='a'/> William Sealy Gosset worked for Guinness in "
            "Dublin, testing barley and yeast in small samples. Guinness let him publish only under a pseudonym, "
            "Student, and in 1908 Student worked out the law of the sample mean divided by its estimated standard "
            "error. <bookmark mark='b'/> In modern form: a standard normal, divided by the square root of an "
            "independent chi-squared over its degrees of freedom. <bookmark mark='c'/> Compared with the normal, "
            "grey, its tails are heavier, because the estimated spread is itself uncertain. <bookmark mark='d'/> "
            "As the degrees of freedom grow the estimate firms up and t becomes the normal. With one degree of "
            "freedom its tails are so heavy that it has no mean at all: that's the Cauchy. Part 8 puts t to work."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(nc), Create(tc["3"]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(Create(tc["30"]), Create(tc["1"]), FadeIn(leg), FadeIn(notes[1:]))
        self.clear_scene()

    def fisher(self):
        d = load("sampling")
        fx, fd = np.asarray(d["fx"]), np.asarray(d["fden"])
        A = axes([0, 5], [0, 0.8], x_length=6.0, y_length=3.6, xlabel=r"$x$", xticks=[0, 1, 2, 3, 4, 5],
                 yticks=[0, 0.4, 0.8], center=[-3.0, -0.6, 0])
        cv = curve(A.ax, fx, fd, EXACT, 3)
        f = MathTex(r"F = \frac{V_1 / d_1}{V_2 / d_2}", r",\quad V_i \sim \chi^2_{d_i}", font_size=34, color=EXACT)
        f.move_to([3.6, 1.4, 0])
        cap = label(r"$F_{5,\,10}$", font_size=24, color=EXACT).next_to(A, UP, buff=0.15)
        hc = label(r"R. A. Fisher (1924); \ named $F$ in his honour by George Snedecor (1934)", font_size=24,
                   color=GREY_B).move_to([3.6, 0.0, 0])
        if hc.width > 6.0:
            hc.width = 6.0
        use = label(r"comparing two variances: \ the analysis of variance, \ Parts 12--13", font_size=24,
                    color=GREY_A).move_to([3.6, -1.0, 0])
        if use.width > 6.0:
            use.width = 6.0
        with self.voiceover(
            "The third is a ratio. <bookmark mark='a'/> Divide one chi-squared by its degrees of freedom, and "
            "another, independent one by its own, and take the ratio. <bookmark mark='b'/> Ronald Fisher studied it "
            "in 1924, and George Snedecor named it F in his honour. <bookmark mark='c'/> It's the law of a ratio of "
            "two estimated variances, and it powers the analysis of variance in Parts 12 and 13."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f), FadeIn(A), Create(cv), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(use))
        self.clear_scene()

    def lighthouse(self):
        d = load("sampling")
        ang, pos = np.asarray(d["ang"])[:40], np.asarray(d["pos"])[:40]
        lh = np.array([-3.0, 2.2, 0])
        shore_y = 0.7
        shore = Line([-6.8, shore_y, 0], [0.8, shore_y, 0], color=S.MUSEUM, stroke_width=3)
        sl = label(r"the shore", font_size=22, color=S.MUSEUM).next_to(shore, DOWN, buff=0.1).shift(RIGHT * 2.5)
        house = VGroup(Triangle(color=S.ACCENT, fill_color=S.ACCENT, fill_opacity=1).scale(0.18).move_to(lh),
                       label(r"lighthouse, 1 km out", font_size=20, color=S.ACCENT).next_to(lh, UP, buff=0.2))
        scale = 1.5
        beams = VGroup()
        hits = VGroup()
        for a, p in zip(ang, pos):
            x = lh[0] + scale * p
            if abs(x - lh[0]) < 3.6:
                beams.add(Line(lh, [x, shore_y, 0], color=S.ACCENT, stroke_width=1, stroke_opacity=0.4))
                hits.add(Dot([x, shore_y, 0], radius=0.05, color=SIM))
        run_c, run_n = np.asarray(d["run_c"]), np.asarray(d["run_n"])
        A = axes([0, 20000], [-3, 3], x_length=5.6, y_length=2.8, xlabel=r"flashes recorded", xticks=[0, 10000, 20000],
                 xfmt=lambda v: fmt_int(v), yticks=[-2, 0, 2], center=[3.9, -1.25, 0])
        ax = A.ax
        idx = np.unique(np.geomspace(5, 20000, 300).astype(int)) - 1
        cc = curve(ax, idx + 1, np.clip(run_c[idx], -3, 3), S.RESID, 2.5)
        cn = curve(ax, idx + 1, np.clip(run_n[idx], -3, 3), S.LIK, 2.5)
        leg = legend([(S.RESID, r"running mean: lighthouse"), (S.LIK, r"running mean: normal")], font_size=20)
        leg.next_to(A, UP, buff=0.15)
        f = MathTex(r"X = \tan\Theta,\ \ \Theta \sim U\!\left(-\tfrac\pi2, \tfrac\pi2\right)", r"\ \Rightarrow\ ",
                    r"f(x) = \frac{1}{\pi(1 + x^2)}", font_size=28).move_to([-3.0, -1.4, 0])
        f[2].set_color(EXACT)
        take = label(r"the average of Cauchy draws is Cauchy again: \ no law of averages without a mean", font_size=22,
                     color=S.ACCENT).move_to([-3.0, -2.6, 0])
        if take.width > 6.6:
            take.width = 6.6
        tag = note(r"simulated: 20,000 flashes").to_corner(UR, buff=0.3)
        with self.voiceover(
            "The Cauchy has a vivid story. <bookmark mark='a'/> A lighthouse stands a kilometre off a straight "
            "shore. Its lamp spins, and flashes at a random moment, so in a random direction. <bookmark mark='b'/> "
            "Record where each flash hits the shore. The position is the tangent of a uniform angle, and the CDF "
            "method gives its density: one over pi times one plus x squared, the Cauchy. "
            "<bookmark mark='c'/> Now average the recorded positions. For normal data, green, the running mean "
            "settles down. For the lighthouse, red, it never does: every so often a flash at a shallow angle lands "
            "kilometres down the coast and drags the average away. <bookmark mark='d'/> The Cauchy has no mean, "
            "and the average of Cauchy draws is just another Cauchy, no more concentrated than one draw. The laws "
            "of averages in Part 6 will need a condition, and this is why."
        ) as vo:
            self.play(Create(shore), FadeIn(sl), FadeIn(house), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in beams], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h_, scale=1.5) for h_ in hits], lag_ratio=0.05), Write(f))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(leg), Create(cn), Create(cc), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()
