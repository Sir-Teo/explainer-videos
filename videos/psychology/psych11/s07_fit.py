from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Fit(VoiceoverScene):
    def construct(self):
        self.card()
        self.likelihood()
        self.surface()
        self.interval()
        self.goodness()
        self.lapse()

    def card(self):
        card = chapter_card(6, r"Fitting the curve", r"Which curve made these counts most likely, \ and how sure can we be?",
                            lit={2001: r"Wichmann and Hill"}, part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter six. Fitting the curve."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center):
        return axes([0, 25], [0.4, 1.02], x_length=6.6, y_length=4.0, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0.5, 0.75, 1.0],
                    yfmt=lambda v: f"{v:g}", xlabel=r"the increment", ylabel=r"share right", center=center)

    def likelihood(self):
        d = load("fit")
        head = heading(r"How likely are these counts, \ under one curve?")
        A = axes([0, 25], [0.4, 1.02], x_length=5.6, y_length=4.0, xticks=[0, 8, 16, 24], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"the increment", ylabel=r"share right", center=[-3.8, -0.35, 0])
        ax = A.ax
        p = d["k"] / d["n"]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.1, color=YOU) for x, y in zip(d["delta"], p)])
        x = np.linspace(0, 25, 200)
        bad_curve = curve(ax, x, psychometric_curve(x, 16.0, 2.0), BAD, stroke_width=4)
        good_curve = curve(ax, x, psychometric_curve(x, d["alpha"], d["beta"], d["lam"]), MODEL, stroke_width=5)
        lines = VGroup(
            MathTex(r"P(k \text{ of } n \mid x) = \binom{n}{k}\,\psi(x)^{k}\,\bigl(1-\psi(x)\bigr)^{n-k}", font_size=34),
            MathTex(r"\ln L(\alpha, \beta, \lambda) = \sum_{x} \bigl[k \ln \psi(x) + (n-k)\ln(1-\psi(x))\bigr] + c", font_size=32,
                    color=THRESH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows = rows_of([
            (r"each level: \ $k$ right out of $n$, \ a binomial count", WHITE),
            (r"a curve that passes far from the points makes these counts unlikely", BAD),
            (r"maximum likelihood: \ the curve that makes them most likely", MODEL),
        ], 5.6, 28, 0.25)
        lines.width = min(lines.width, 6.4)
        side = VGroup(lines, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.15, -0.3, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"simulated: one study of $8 \times 40$ trials, \ the middle one of 101")
        with self.voiceover(
            "Here's a study of 320 trials, picked by rule: of a hundred and one such studies on Psyche, "
            "the one with the middle threshold. <bookmark mark='a'/> At each level, k right out of n is "
            "a binomial count. So for any proposed curve, we can compute how likely these exact counts "
            "were. <bookmark mark='b'/> A curve that passes far from the points makes them very "
            "unlikely. <bookmark mark='c'/> Add up the logarithms of those probabilities over the levels, "
            "and you have the log-likelihood of the curve. The fit is the curve that makes it largest: "
            "maximum likelihood, the method of Part 9's twin models, here in its simplest form."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(dots, lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(bad_curve), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), Create(good_curve), bad_curve.animate.set_stroke(opacity=0.3), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def surface(self):
        d = load("fit")
        head = heading(r"The likelihood, \ over every curve at once")
        al, be, ll = d["grid_alpha"], d["grid_beta"], d["loglik"]
        A = axes([al[0], al[-1]], [be[0], be[-1]], x_length=6.4, y_length=4.4, xticks=[2, 6, 10, 14], yticks=[2, 6, 10],
                 xlabel=r"threshold parameter, $\alpha$", ylabel=r"spread, $\beta$", center=[-3.0, -0.35, 0])
        ax = A.ax
        top = ll.max()
        cells = VGroup()
        dx = abs(ax.c2p(al[1], 0)[0] - ax.c2p(al[0], 0)[0])
        dy = abs(ax.c2p(0, be[1])[1] - ax.c2p(0, be[0])[1])
        for r in range(0, len(be), 1):
            for c in range(0, len(al), 1):
                v = np.clip((ll[r, c] - top + 12) / 12, 0, 1)
                if v <= 0:
                    continue
                cells.add(Rectangle(width=dx * 1.02, height=dy * 1.02, stroke_width=0, fill_color=MODEL, fill_opacity=0.08 + 0.8 * v ** 2)
                          .move_to(ax.c2p(al[c], be[r])))
        best = Dot(ax.c2p(d["alpha"], d["beta"]), radius=0.11, color=WHITE)
        bl = label(r"the maximum", font_size=26, color=WHITE).next_to(best, UR, buff=0.08)
        rows = rows_of([
            (r"brighter: \ more likely; \ the bright ridge runs on a slant", WHITE),
            (rf"the maximum: \ $\alpha = {d['alpha']:.1f}$, \ $\beta = {d['beta']:.1f}$, \ with a lapse rate of "
             rf"${d['lam']:.2f}$", MODEL),
            (rf"the 75\% threshold: \ ${d['threshold']:.1f}$. \ The observer's true one: \ ${d['true75']:.1f}$", THRESH),
            (r"the ridge means a higher threshold with a shallower slope fits almost as well", GREY_A),
        ], 5.2, 28, 0.3).move_to([4.2, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: the log-likelihood on a grid")
        with self.voiceover(
            "We can draw the likelihood of every curve at once. Each point here is a curve, with its "
            "threshold across and its spread up, coloured by how likely it makes the counts. "
            "<bookmark mark='a'/> The bright region is where the good curves are. "
            f"<bookmark mark='b'/> The maximum is at alpha {d['alpha']:.1f} and beta {d['beta']:.1f}, "
            f"with a lapse rate of {d['lam']:.2f}. <bookmark mark='c'/> On that curve the seventy-five "
            f"percent threshold is {d['threshold']:.1f}. Psyche's true one is {d['true75']:.1f}. "
            "<bookmark mark='d'/> Notice the shape of the bright region. It's a ridge on a slant: a "
            "higher threshold with a shallower slope fits almost as well. The data pin down some "
            "combinations of the numbers much better than others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(cells), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(best, scale=1.5), FadeIn(bl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def interval(self):
        d = load("fit")
        head = heading(r"How sure? \ Refit a thousand imaginary repeats")
        lo, hi = d["ci"]
        edges = np.linspace(4, 13, 37)
        dens, _ = np.histogram(d["boot"], bins=edges, density=True)
        A = axes([4, 13], [0, float(dens.max()) * 1.45], x_length=6.6, y_length=3.6, xticks=[4, 6, 8, 10, 12], yticks=[],
                 xlabel=r"the 75\% threshold", ylabel=r"", center=[-3.0, -0.2, 0])
        ax = A.ax
        h = hist(ax, edges, dens, MODEL)
        ci = VGroup(Line(ax.c2p(lo, float(dens.max()) * 1.08), ax.c2p(hi, float(dens.max()) * 1.08), color=THRESH, stroke_width=6),
                    *[Line(ax.c2p(v, float(dens.max()) * 1.02), ax.c2p(v, float(dens.max()) * 1.14), color=THRESH, stroke_width=4)
                      for v in (lo, hi)])
        true = DashedLine(ax.c2p(d["true75"], 0), ax.c2p(d["true75"], float(dens.max()) * 1.3), color=WHITE, stroke_width=3)
        tl = label(r"the truth", font_size=25, color=WHITE).next_to(true.get_top(), UP, buff=0.08)
        rows = rows_of([
            (r"the parametric bootstrap: \ treat the fitted curve as the truth, \ draw new counts from it, \ refit", WHITE),
            (rf"1{{,}}000 refits: \ 95\% of the thresholds lie between ${lo:.1f}$ and ${hi:.1f}$", THRESH),
            (r"320 trials pin a threshold down to within about $\pm 30\%$", MODEL),
            (r"Wichmann and Hill (2001) made this the standard way", GREY_A),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        src = published_tag(archive.WICHMANN_HILL_2001.cite)
        tag = psyche_tag(r"computed: 1{,}000 bootstrap refits")
        with self.voiceover(
            "How sure can we be of that threshold? We can't run the study a thousand times. But we can "
            "imagine it. <bookmark mark='a'/> Treat the fitted curve as if it were the truth, draw new "
            "counts from it, the same number of trials at each level, and refit. That's the parametric "
            "bootstrap. <bookmark mark='b'/> A thousand refits, and ninety-five percent of their "
            f"thresholds lie between {lo:.1f} and {hi:.1f}. <bookmark mark='c'/> So three hundred and "
            "twenty trials pin a threshold down to within about thirty percent either way. That's the "
            "honest precision of a whole afternoon in the laboratory. <bookmark mark='d'/> Fitting by "
            "maximum likelihood and putting a bootstrap interval round the result became the standard "
            "way after two papers by Felix Wichmann and Jeremy Hill, in 2001."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ci), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(true), FadeIn(tl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def _devs(self, center, dev, boot, color, title):
        hi = float(max(np.percentile(boot, 99.5), dev * 1.15, 12.0))
        edges = np.linspace(0, hi, 31)
        dens, _ = np.histogram(np.clip(boot, 0, hi - 1e-9), bins=edges, density=True)
        top = float(dens.max()) * 1.35
        A = axes([0, hi], [0, top], x_length=5.2, y_length=2.2, xticks=[0, 5, 10, 15, 20, 25, 30][: int(hi // 5) + 1],
                 yticks=[], xlabel=r"deviance", ylabel=r"", center=center)
        h = hist(A.ax, edges, dens, color)
        mark = Line(A.ax.c2p(dev, 0), A.ax.c2p(dev, top * 0.9), color=THRESH, stroke_width=5)
        ml = label(r"the data", font_size=24, color=THRESH).next_to(mark, UP, buff=0.06)
        t = label(title, font_size=27, color=color).next_to(A, UP, buff=0.25)
        return A, h, VGroup(mark, ml), t

    def goodness(self):
        d, g, w = load("fit"), load("goodfit"), load("wander")
        head = heading(r"Does the curve fit? \ And what a fit cannot see")
        A, ha, ma, ta = self._devs([-3.4, 0.85, 0], d["deviance"], d["boot_dev"], MODEL, r"Psyche's observer")
        B, hb, mb, tb = self._devs([3.4, 0.85, 0], g["deviance"], g["boot_dev"], FECHC, r"an observer whose threshold drifts")
        rows = rows_of([
            (r"the deviance: \ how much worse the curve does than a model that fits every level exactly; \ the bars: "
             r"\ its value in repeats drawn from the fitted curve itself", WHITE),
            (rf"Psyche: \ {100 * d['p_fit']:.0f}\% of repeats fit worse than the data. \ Nothing is wrong", MODEL),
            (rf"a threshold that drifts between blocks of ten trials, \ typically by a factor of 1.8: \ "
             rf"{100 * g['p_fit']:.0f}\% fit worse. \ It passes too, \ and across 41 such studies the test flagged "
             rf"{100 * g['share_rejected']:.0f}\%, \ its rate by chance alone", FECHC),
            (rf"and the fitted threshold barely moves \ (medians of 101: \ {w['wander_th']:.1f} against "
             rf"{w['steady_th']:.1f}): \ a fit reports the session's average. \ Drift has to be looked for in the "
             rf"trials, \ in order", THRESH),
        ], 12.6, 26, 0.16).to_edge(DOWN, buff=0.78)
        tag = psyche_tag(r"computed: \ 1{,}000 and 300 refits; \ the second study the median of 41")
        with self.voiceover(
            "One more question before trusting any of this: does the curve fit at all? Maximum "
            "likelihood always finds the best curve of the family you gave it, even when no member of "
            "the family describes the data. <bookmark mark='a'/> The usual check is the deviance: how much "
            "worse the fitted curve does than a model that matches every level exactly. On its own the "
            "number means little, so use the bootstrap again. Draw studies from the fitted curve, refit "
            "each one, and see how large the deviance is when the curve really is the truth. "
            "<bookmark mark='b'/> For Psyche's study, "
            f"{100 * d['p_fit']:.0f} percent of the repeats fit worse than the real data did. Nothing is "
            "wrong. <bookmark mark='c'/> Now a harder case. Run the same design on an observer whose "
            "threshold drifts: in every block of ten trials, attention is better or worse, typically by a "
            f"factor of one point eight. {100 * g['p_fit']:.0f} percent of the repeats fit worse. It passes. "
            "Across forty-one such studies the test flagged "
            f"{100 * g['share_rejected']:.0f} percent, which is the rate it flags when nothing at all is "
            "wrong. <bookmark mark='d'/> And the fitted threshold barely moves: a median of "
            f"{w['wander_th']:.1f} against {w['steady_th']:.1f} for the steady observer. A fit reports "
            "the session's average, and with forty trials a level a drift inside the session is "
            "invisible to it. So a passing test is weak evidence. To see drift, you have to look at the "
            "trials in the order they happened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ta))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ha, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ma[0]), FadeIn(ma[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(tb), FadeIn(hb, lag_ratio=0.05), run_time=1.5)
            self.play(Create(mb[0]), FadeIn(mb[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lapse(self):
        d = load("fit")
        head = heading(r"One slip, \ and a fit with no room for slips")
        A = self._axes([-3.1, -0.35, 0])
        ax = A.ax
        p = d["k_lapse"] / d["n"]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.1, color=YOU) for x, y in zip(d["delta"], p)])
        ring = Circle(radius=0.28, color=BAD, stroke_width=4).move_to(dots[-1])
        x = np.linspace(0, 25, 200)
        nol = curve(ax, x, psychometric_curve(x, *_from_threshold(d["th_no_lapse"], d["beta_no_lapse"], 0.0)), BAD, stroke_width=4)
        wl = curve(ax, x, psychometric_curve(x, *_from_threshold(d["th_with_lapse"], d["beta_with_lapse"], d["lam_with_lapse"])),
                   MODEL, stroke_width=5)
        rows = rows_of([
            (r"the same study, \ with one more wrong answer at the easiest level", WHITE),
            (rf"forced to reach 100\%, \ the fit flattens: \ threshold ${d['th_no_lapse']:.1f}$", BAD),
            (rf"allowed a lapse rate, \ it shrugs: \ threshold ${d['th_with_lapse']:.1f}$ \ (the truth: "
             rf"${d['true75']:.1f}$)", MODEL),
            (r"so the fourth parameter is not decoration: \ leave it out, \ and one blink moves the answer", THRESH),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: the fit with and without $\lambda$")
        with self.voiceover(
            "Now the lapse rate. Take the same study, and add one more wrong answer at the easiest level, "
            "where any attentive observer is right. A blink. <bookmark mark='a'/> Fit a curve that must "
            "reach a hundred percent, and that one slip drags it flat. The threshold moves to "
            f"{d['th_no_lapse']:.1f}. <bookmark mark='b'/> Fit a curve that's allowed a lapse rate, and "
            f"it simply absorbs the slip. The threshold stays at {d['th_with_lapse']:.1f}, near the "
            f"truth of {d['true75']:.1f}. <bookmark mark='c'/> So lambda isn't decoration. Leave it out, "
            "and one blink at the top of the curve moves the answer by a quarter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(dots), FadeIn(rows[0]), Create(ring))
            vo.wait_until("a")
            self.play(Create(nol), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(wl), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()


def psychometric_curve(x, alpha, beta, lam=0.0):
    from explainer.psychology.psyche.psychophysics import psychometric
    return psychometric(x, alpha, beta, 0.5, lam, "gauss")


def _from_threshold(th75, beta, lam):
    """The alpha that puts the 75% point of a Gaussian curve with guess 0.5 and lapse ``lam`` at ``th75``."""
    from scipy import stats
    q = (0.75 - 0.5) / (1 - 0.5 - lam)
    return th75 - beta * stats.norm.ppf(q), beta, lam
