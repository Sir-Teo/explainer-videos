from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403

SHORT = ["visual perception", "cubes", "paper form board", "flags", "general information", "paragraph comprehension",
         "sentence completion", "word classification", "word meaning", "addition", "code", "counting dots",
         "straight--curved capitals", "word recognition", "number recognition", "figure recognition", "object--number",
         "number--figure", "figure--word", "deduction", "numerical puzzles", "problem reasoning", "series completion",
         "arithmetic problems"]
FNAMES = [r"verbal", r"speed", r"spatial", r"memory"]


def heat(L, cell=0.2, x0=0.0, y0=0.0, color=None):
    color = color or FAC
    g = VGroup()
    for i in range(L.shape[0]):
        for j in range(L.shape[1]):
            v = float(np.clip(abs(L[i, j]), 0, 1))
            g.add(Square(cell * 0.92, stroke_width=0, fill_opacity=1,
                         fill_color=interpolate_color(ManimColor("#1b2030"), ManimColor(color), v)).move_to([x0 + j * cell * 3.2, y0 - i * cell, 0]))
    return g


class Factor(VoiceoverScene):
    def construct(self):
        self.card()
        self.spearman()
        self.model()
        self.indeterminacy()
        self.tests()
        self.how_many()
        self.rotate()
        self.scores()
        self.heywood()
        self.versus()

    def card(self):
        card = chapter_card(5, r"Factor analysis", r"Hidden causes of shared variation", lit=(1904,), part=PART)
        with self.voiceover("Chapter five. Factor analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def spearman(self):
        rows = fit_rows(VGroup(
            label(r"1904: \ Charles Spearman sees that school marks in every subject correlate positively", font_size=24),
            label(r"his model: \ one general factor $g$ plus a specific part for each test", font_size=24, color=FAC),
            label(r"Thurstone (1930s): \ several factors, \ and the idea of rotating them", font_size=24, color=FAC),
            label(r"what $g$ means has been contested for a century; \ the model only describes covariance", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1904 Charles Spearman noticed that children's marks in very different subjects, "
            "classics, French, music, all correlated positively. <bookmark mark='b'/> He proposed that each mark is one "
            "general factor, which he called g, plus a part specific to the test. <bookmark mark='c'/> In the 1930s Louis "
            "Thurstone allowed several factors, and introduced the idea of rotating them to make them interpretable. "
            "<bookmark mark='d'/> What g is, and whether it is anything at all, has been argued for a century, often "
            "bitterly. The statistics can settle less than either side has wished: a factor model describes a pattern of "
            "covariance, and does not by itself show that a factor is a real thing."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"x", r"=", r"\mu + L f + \varepsilon, \ \ f \sim N_k(0, I), \ \ \varepsilon \sim N_p(0, \Psi)", font_size=28),
            cmath(r"\Sigma", r"=", r"L L^\top + \Psi, \ \ \Psi \text{ diagonal}", font_size=32),
            cmath(r"\sigma_{jj}", r"=", r"\underbrace{\textstyle\sum_m l_{jm}^2}_{\text{communality}} + \underbrace{\psi_j}_{\text{uniqueness}}", font_size=28),
            cmath(r"\text{parameters}", r":", r"pk + p \ \ll \ p(p+1)/2", font_size=30),
        ]
        rows[1][-1].set_color(FAC)
        whys = [why(r"$k$ factors, \ $p$ tests"), why(r"all correlation runs through the factors"),
                why(r"shared and specific variance"), why(r"24 tests, \ 4 factors: \ 120 vs 300")]
        with self.voiceover(
            "<bookmark mark='a'/> The model: each of p observed scores is a mean, plus loadings times k unobserved factors, "
            "plus an error specific to that score. <bookmark mark='b'/> Then the covariance is L L transpose plus a "
            "diagonal: every correlation between two tests runs through the common factors. <bookmark mark='c'/> Each "
            "variance splits into a communality, the part shared with other tests, and a uniqueness. "
            "<bookmark mark='d'/> The model is economical: with twenty-four tests and four factors, a hundred and twenty "
            "parameters stand in for three hundred variances and covariances."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def indeterminacy(self):
        rows = [
            cmath(r"(L T)(L T)^\top", r"=", r"L L^\top \ \text{for any orthogonal } T", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the loadings are determined only up to rotation}", font_size=30),
            cmath(r"\text{ML}", r":", r"\min_\Psi \ \log|\Sigma| + \mathrm{tr}(\Sigma^{-1} R) - \log|R| - p", font_size=30),
            cmath(r"\text{test}", r":", r"(n - 1 - \tfrac{2p + 5}{6} - \tfrac{2k}{3}) \hat F \ \approx \ \chi^2_{((p - k)^2 - p - k)/2}", font_size=26),
        ]
        rows[2][-1].set_color(FAC)
        whys = [why(r"rotational indeterminacy"), why(r"choose $T$ for interpretability"),
                why(r"Lawley (1940), \ J\"oreskog (1967)"), why(r"Bartlett's corrected LR test")]
        with self.voiceover(
            "<bookmark mark='a'/> One fact shapes everything that follows. Rotate the loadings by any orthogonal matrix and "
            "the implied covariance does not change. <bookmark mark='b'/> So the data determine the loadings only up to "
            "rotation, and the analyst chooses a rotation to make them interpretable. <bookmark mark='c'/> Estimation is by "
            "maximum likelihood, Derrick Lawley's in 1940 and Karl Jöreskog's practical algorithm of 1967, minimizing this "
            "discrepancy between the model and the sample correlations over the uniquenesses. <bookmark mark='d'/> And "
            "Bartlett's corrected likelihood-ratio statistic tests whether k factors suffice."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tests(self):
        d = load("fa")
        R_names = SHORT
        cols = VGroup(VGroup(*[label(rf"{i + 1}.\ {R_names[i]}", font_size=19) for i in range(12)]).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
                      VGroup(*[label(rf"{i + 1}.\ {R_names[i]}", font_size=19) for i in range(12, 24)]).arrange(DOWN, aligned_edge=LEFT, buff=0.14))
        cols.arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([-2.2, -0.1, 0])
        rows = fit_rows(VGroup(
            label(rf"{d['n']} seventh- and eighth-graders, \ Chicago, \ 1937--38", font_size=22),
            label(r"24 tests: \ spatial, \ verbal, \ speed, \ memory, \ reasoning", font_size=22, color=FAC),
            label(r"every correlation positive: \ mean 0.30", font_size=22),
            label(rf"first eigenvalue {d['eig'][0]:.1f} of 24: \ Spearman's pattern", font_size=22, color=MAPC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic data: Karl Holzinger and Frances Swineford gave twenty-four tests to a hundred "
            "and forty-five schoolchildren in suburban Chicago in 1937 and 1938. <bookmark mark='b'/> Spatial tests like "
            "cubes and flags; verbal tests like paragraph comprehension; speeded tests like addition and counting dots; "
            "memory tests like word and number recognition. <bookmark mark='c'/> Every one of the two hundred and seventy-six "
            "correlations is positive, averaging point three. <bookmark mark='d'/> The first eigenvalue of the correlation "
            "matrix is eight point one, a third of the total: Spearman's pattern, a strong general factor."
        ) as vo:
            self.add(harman_tag())
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in [*cols[0], *cols[1]]], lag_ratio=0.08), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def how_many(self):
        d = load("fa")
        hdr = [r"\textbf{factors $k$}", r"\textbf{LR $\chi^2$}", r"\textbf{df}", r"\textbf{$p$-value}"]
        body = []
        for k in range(1, 6):
            f = d["fits"][str(k)]
            e = int(np.floor(np.log10(f["p"])))
            pv = f"{f['p']:.3f}" if f["p"] > 0.001 else rf"${f['p'] / 10 ** e:.1f} \times 10^{{{e}}}$"
            body.append([str(k), f"{f['chi2']:.1f}", f"{f['df']:.0f}", pv])
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.3,
                        colors=[GREY_A, RES, RES, RES, MAPC, FAC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"one factor is rejected overwhelmingly: \ $g$ alone is not enough", font_size=22, color=RES),
            label(r"four factors pass at 1\%; \ five at 5\%: \ the traditional answer is four", font_size=22, color=FAC),
            label(r"with large $n$ every model is eventually rejected: \ the test is a guide, \ not a verdict", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How many factors? Bartlett's test, for one to five. One factor is rejected with a p-value "
            "of ten to the minus thirty-three: a general factor alone does not explain these correlations. Two and three "
            "factors are rejected too. <bookmark mark='b'/> Four factors give a p-value of point oh two, five factors point "
            "one three. Harman's traditional answer, and Holzinger's, is four. <bookmark mark='c'/> But with a large enough "
            "sample, any parsimonious model will be rejected; the test is a guide to how much structure the data can "
            "support, not a verdict on the truth."
        ) as vo:
            self.add(harman_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:4]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[4:]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def rotate(self):
        d = load("fa")
        raw, rot = np.asarray(d["loadings_raw"]), np.asarray(d["loadings"])
        cell = 0.2
        h0 = heat(raw, cell, x0=-2.2, y0=2.35)
        h1 = heat(rot, cell, x0=-2.2, y0=2.35)
        names = VGroup(*[label(SHORT[i], font_size=15, color=GREY_B).next_to(h0[i * 4], LEFT, buff=0.15) for i in range(24)])
        heads0 = VGroup(*[label(rf"F{j + 1}", font_size=18, color=GREY_A).next_to(h0[j], UP, buff=0.12) for j in range(4)])
        heads1 = VGroup(*[label(FNAMES[j], font_size=17, color=FAC).next_to(h0[j], UP, buff=0.12) for j in range(4)])
        rows = fit_rows(VGroup(
            label(r"four-factor ML loadings: \ brighter = larger", font_size=22),
            label(r"unrotated: \ F1 loads on everything: \ $g$", font_size=22, color=GREY_A),
            label(r"varimax \ (Kaiser 1958): \ each test loads mostly on one factor", font_size=22, color=FAC),
            label(r"verbal 5--9; \ speed 10--13; \ spatial 1--4; \ memory 14--19", font_size=22, color=FAC),
            label(r"same fit, \ same $\Sigma$: \ only the description changed", font_size=22, color=RES),
        ), 4.4, 0.42, [4.4, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The four-factor loadings, as a heat map: twenty-four tests down, four factors across, "
            "brighter for a larger loading. <bookmark mark='b'/> As estimated, the first factor loads on every test, "
            "between a third and three quarters: that is Spearman's g. <bookmark mark='c'/> Now rotate by Henry Kaiser's "
            "varimax criterion of 1958, the rotation that makes the squared loadings in each column as spread out as "
            "possible. <bookmark mark='d'/> Each test now loads mostly on one factor, and the factors can be named: verbal, "
            "speed, spatial, memory. <bookmark mark='e'/> Nothing about the fit changed. The two pictures imply exactly the "
            "same covariance matrix. Whether these children have one general ability or four special ones is not a "
            "question these data can answer by themselves."
        ) as vo:
            self.add(harman_tag())
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(h0), FadeIn(heads0), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[h0[i * 4] for i in range(24)]), color=MAPC, scale_factor=1.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[c.animate.set_fill(h1[i].get_fill_color()) for i, c in enumerate(h0)], FadeOut(heads0), FadeIn(heads1),
                      FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def heywood(self):
        u = np.asarray(load("fa")["uniqueness"])
        rows = [
            cmath(r"\psi_j", r"\to", r"0: \ \text{communality reaches 1}", font_size=30),
            cmath(r"\psi_j", r"<", r"0: \ \text{a negative variance}", font_size=30),
            cmath(r"\text{causes}", r":", r"\text{too many factors, \ small } n, \ \text{a misspecified model}", font_size=28),
            cmath(r"\text{here}", r":", rf"\text{{none}}: \ \hat\psi_j \in [{u.min():.2f}, {u.max():.2f}]", font_size=30),
        ]
        rows[1][-1].set_color(RES)
        whys = [why(r"a boundary solution"), why(r"impossible: \ a Heywood case"), why(r"Heywood (1931)"),
                why(r"the four-factor fit is interior")]
        with self.voiceover(
            "<bookmark mark='a'/> A warning sign to watch for. Sometimes the likelihood pushes a uniqueness to zero, so that "
            "one test is explained entirely by the factors. <bookmark mark='b'/> Unconstrained algorithms can even return a "
            "negative variance. These are Heywood cases, after H. B. Heywood's paper of 1931. <bookmark mark='c'/> They "
            "signal too many factors, too small a sample, or a wrong model. <bookmark mark='d'/> The four-factor fit here has "
            "none: every uniqueness lies between a quarter and four fifths."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def versus(self):
        hdr = [r"", r"\textbf{principal components}", r"\textbf{factor analysis}"]
        body = [[r"is", r"a rotation of the data", r"a model for the data"],
                [r"explains", r"total variance", r"covariance, \ off the diagonal"],
                [r"specific variance", r"absorbed into components", r"set apart in $\Psi$"],
                [r"scores", r"exact linear combinations", r"estimated, \ not observed"],
                [r"units", r"change the answer", r"scale-invariant \ (ML)"]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.8, row_buff=0.3, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[1].set_color(PCC)
            r[2].set_color(FAC)
        tb.move_to([0, 0.5, 0])
        foot = label(r"they agree when uniquenesses are small and equal; \ they can differ a lot when not", font_size=22,
                     color=PATH).move_to([0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Factor analysis and principal components are often confused. Components are a rotation of "
            "the data; factors are a model. Components explain total variance; factors explain covariance, the off-diagonal "
            "part, and set each test's specific variance apart. <bookmark mark='b'/> Component scores are exact linear "
            "combinations of the data; factor scores must be estimated. And maximum likelihood factor analysis is "
            "unaffected by rescaling a variable, where components change. <bookmark mark='c'/> When the uniquenesses are "
            "small and similar the two give much the same answer; when they are not, they can differ a great deal."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:4]))
            vo.wait_until("b")
            self.play(FadeIn(tb[4:]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def scores(self):
        rows = [
            cmath(r"\hat f_{\text{Thomson}}", r"=", r"L^\top \Sigma^{-1} (x - \mu)", font_size=32),
            cmath(r"\hat f_{\text{Bartlett}}", r"=", r"(L^\top \Psi^{-1} L)^{-1} L^\top \Psi^{-1} (x - \mu)", font_size=30),
            cmath(r"\text{indeterminacy}", r":", r"f \text{ is never recovered exactly from } p \text{ tests}", font_size=28),
            cmath(r"\text{rotation}", r":", r"\text{oblique (promax, oblimin) lets factors correlate}", font_size=28),
        ]
        rows[1][-1].set_color(FAC)
        whys = [why(r"regression scores: \ $E(f \mid x)$"), why(r"weighted least squares: \ unbiased"), why(r"factor score indeterminacy"), why(r"Thurstone's `simple structure'")]
        with self.voiceover(
            "<bookmark mark='a'/> A child's factor scores must be estimated. Godfrey Thomson's regression scores are "
            "the conditional expectation of the factors given the tests. <bookmark mark='b'/> Bartlett's scores are a "
            "weighted least-squares fit of the loadings to the child's results, unbiased but noisier. <bookmark "
            "mark='c'/> Neither recovers the factors exactly; with finitely many tests there is always uncertainty "
            "left, an old and much argued point. <bookmark mark='d'/> And the rotation need not be orthogonal. Oblique "
            "rotations such as promax let the factors correlate with each other, which for abilities is usually more "
            "realistic; a second-order factor analysis of those correlations brings back a general factor."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
