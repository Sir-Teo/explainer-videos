from __future__ import annotations

from math import comb

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class Likelihood(VoiceoverScene):
    def construct(self):
        self.card()
        self.fisher()
        self.flip()
        self.sharpen()
        self.score()
        self.horsekicks()
        self.tanks()
        self.invariance()

    def card(self):
        card = chapter_card(3, r"Maximum likelihood", r"Which parameter makes the data least surprising?", lit=(1922,), part=PART)
        with self.voiceover("Chapter three. Maximum likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fisher(self):
        h1 = history_card(1912, r"R. A. Fisher, \ a Cambridge undergraduate", r"``On an absolute criterion for fitting frequency "
                          r"curves'': \ choose the curve that makes the observed sample most probable", color=LIK, width=6.0,
                          font_size=22).move_to([-3.3, 1.0, 0])
        h2 = history_card(1922, r"R. A. Fisher, \ Rothamsted", r"``On the mathematical foundations of theoretical statistics'': \ "
                          r"names consistency, \ efficiency \ and sufficiency, \ and argues the method is the best possible",
                          color=LIK, width=6.0, font_size=22).move_to([3.3, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"forerunners: \ Daniel Bernoulli (1778), \ Lambert, \ and Gauss (1809), \ who derived the normal curve from it",
                  font_size=24, color=GREY_A),
            label(r"``likelihood'' (Fisher, 1921): \ not a probability of $\theta$, \ but of the data, \ read as a function of $\theta$",
                  font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1912, Ronald Fisher, then a Cambridge undergraduate, published a three-page paper "
            "proposing an absolute criterion for fitting curves: choose the curve that makes the sample you actually "
            "observed as probable as possible. <bookmark mark='b'/> Ten years later, working at the Rothamsted "
            "agricultural station, he wrote the paper that founded mathematical statistics as a subject, gave names to "
            "consistency, efficiency and sufficiency, and argued that his method was the best possible. "
            "<bookmark mark='c'/> He had forerunners: Daniel Bernoulli in 1778, Johann Lambert, and Gauss, who in 1809 "
            "derived the normal curve by asking which error law makes the average the most likely value. "
            "<bookmark mark='d'/> And Fisher was careful with words. He called the quantity the likelihood, to keep it "
            "distinct from a probability. It is the probability of the data, read as a function of the parameter. It is "
            "not the probability of the parameter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def flip(self):
        n, k = 10, 7
        ps = (0.3, 0.5, 0.7, 0.9)
        panels = VGroup()
        for j, p in enumerate(ps):
            A = axes([-0.5, 10.5], [0, 0.42], x_length=2.9, y_length=1.9, xticks=[0, 7, 10], center=[-4.8 + 3.2 * j, 1.5, 0],
                     font_size=18)
            ax = A.ax
            bars = VGroup()
            for x in range(n + 1):
                pr = comb(n, x) * p ** x * (1 - p) ** (n - x)
                b = Rectangle(width=ax.c2p(0.8, 0)[0] - ax.c2p(0, 0)[0], height=max(1e-3, ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]),
                              stroke_width=0, fill_color=S.ACCENT if x == k else GREY_C, fill_opacity=0.9 if x == k else 0.5)
                b.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
                bars.add(b)
            t = MathTex(rf"p = {p}", font_size=24).next_to(ax, UP, buff=0.12)
            v = MathTex(rf"{comb(n, k) * p ** k * (1 - p) ** (n - k):.3f}", font_size=24, color=S.ACCENT).next_to(ax, DOWN, buff=0.45)
            panels.add(VGroup(A, bars, t, v))
        ps_ = np.linspace(0.01, 0.99, 200)
        L = np.array([comb(n, k) * p ** k * (1 - p) ** (n - k) for p in ps_])
        B = axes([0, 1], [0, 0.3], x_length=7.0, y_length=2.1, xlabel=r"$p$", ylabel=r"$L(p) = P_p(7 \text{ heads in } 10)$",
                 xticks=[0, 0.3, 0.5, 0.7, 0.9, 1], center=[0, -2.2, 0], font_size=18)
        bx = B.ax
        Lc = curve(bx, ps_, L, LIK, 3.5)
        pts = VGroup(*[Dot(bx.c2p(p, comb(n, k) * p ** k * (1 - p) ** (n - k)), radius=0.07, color=S.ACCENT) for p in ps])
        with self.voiceover(
            "Here's what it means. A coin is tossed ten times and lands heads seven times. What is p? "
            "<bookmark mark='a'/> Each panel is a candidate value of p, and the bars are the probabilities of every "
            "possible number of heads. We only care about one bar: seven, the one we saw. <bookmark mark='b'/> Under p "
            "equals point three, seven heads is rare: point zero zero nine. Under a fair coin, point one one seven. "
            "Under point seven, point two six seven. Under point nine, point zero five seven. <bookmark mark='c'/> Now "
            "slide p continuously and track the height of that one bar. That's the likelihood function: the data held "
            "fixed, the parameter moving. <bookmark mark='d'/> Its peak is the maximum likelihood estimate: point "
            "seven, the observed proportion. Notice the curve isn't a density in p; its area isn't one. It only ranks "
            "parameter values by how well they predicted what happened."
        ) as vo:
            vo.wait_until("a")
            self.play(*[FadeIn(pn[0]) for pn in panels], *[FadeIn(pn[2]) for pn in panels])
            self.play(*[FadeIn(pn[1], lag_ratio=0.05) for pn in panels])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(pn[3]) for pn in panels], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(B), *[TransformFromCopy(pn[3], pt) for pn, pt in zip(panels, pts)])
            self.play(Create(Lc), run_time=2.0)
            vo.wait_until("d")
            peak = DashedLine(bx.c2p(0.7, 0), bx.c2p(0.7, 0.3), color=S.ACCENT, stroke_width=2)
            self.play(Create(peak), Indicate(pts[2], color=S.ACCENT))
        self.clear_scene()

    def sharpen(self):
        d = load("likelihood")
        ps = np.asarray(d["ps"])
        A = axes([0.3, 0.95], [-6, 0], x_length=6.8, y_length=4.4, xlabel=r"$p$", ylabel=r"$\ell(p) - \ell(\hat p)$",
                 xticks=[0.3, 0.5, 0.7, 0.9], yticks=[-6, -4, -2, 0], center=[-2.9, -0.3, 0])
        ax = A.ax
        cols = {"10": S.PRIOR, "100": S.POST, "1000": LIK}
        cs = VGroup(*[clip_curve(ax, ps, d[n], cols[n], 3.5, ymin=-6) for n in ("10", "100", "1000")])
        cut = DashedLine(ax.c2p(0.3, -1.92), ax.c2p(0.95, -1.92), color=GREY_B, stroke_width=1.8)
        cut_l = MathTex(r"-1.92", font_size=22, color=GREY_B).next_to(ax.c2p(0.95, -1.92), RIGHT, buff=0.1)
        leg = legend([(S.PRIOR, r"7 of 10"), (S.POST, r"70 of 100"), (LIK, r"700 of 1{,}000")], font_size=22).move_to([4.5, 2.0, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\ell(p) = k\log p + (n - k)\log(1 - p)", font_size=28),
            label(r"the same peak; \ ten times the data, \ ten times the curvature", font_size=24, color=S.ACCENT),
            label(r"the width where $\ell$ drops $1.92$: \ a 95\% interval (Wilks; \ Part 11)", font_size=24, color=GREY_A),
        ), 5.0, 0.34, [4.3, -0.8, 0])
        with self.voiceover(
            "In practice we work with the logarithm of the likelihood: products of probabilities become sums, and "
            "the peak doesn't move. <bookmark mark='a'/> Here's the log-likelihood for seven heads in ten, shifted so "
            "its peak is zero. It's broad: p could easily be anything from point four to point nine. "
            "<bookmark mark='b'/> Seventy heads in a hundred: the same peak, but the curve is ten times as sharply "
            "curved. <bookmark mark='c'/> Seven hundred in a thousand: a narrow spike. More data, sharper likelihood. "
            "<bookmark mark='d'/> That curvature is going to be the whole story of this part. The sharper the peak, "
            "the more precisely the data pin the parameter down. Draw a line one point nine two below the peak, and the "
            "values of p above it form an approximate ninety-five percent confidence interval, which Part 11 will "
            "explain and test."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(leg[k]), run_time=1.5)
                if k == 1:
                    self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(cut), FadeIn(cut_l), FadeIn(rows[2]))
        self.clear_scene()

    def score(self):
        rows = [
            cmath(r"L(\theta)", r"=", r"\prod_{i=1}^n p_\theta(x_i)", font_size=36),
            cmath(r"\ell(\theta)", r"=", r"\sum_{i=1}^n \log p_\theta(x_i)", font_size=36),
            cmath(r"U(\theta)", r"=", r"\ell'(\theta) = \sum_{i=1}^n \frac{\partial}{\partial\theta}\log p_\theta(x_i)", font_size=34),
            cmath(r"U(\hat\theta)", r"=", r"0", r"\quad\text{the likelihood equation}", font_size=36),
            cmath(r"\text{coin}:\ \frac{k}{p} - \frac{n - k}{1 - p}", r"=", r"0\ \Rightarrow\ \hat p = \frac kn", font_size=34),
        ]
        rows[3][2].set_color(LIK)
        rows[4][2].set_color(LIK)
        whys = [why(r"independent observations: \ multiply"), why(r"take logs: \ add"), why(r"the score: \ the slope of $\ell$"),
                why(r"at an interior peak the slope is zero"), why(r"the observed proportion, \ as it should be")]
        with self.voiceover(
            "The machinery. <bookmark mark='a'/> For independent observations, the likelihood is a product of "
            "densities, one per observation. <bookmark mark='b'/> Its logarithm is a sum. <bookmark mark='c'/> The "
            "derivative of the log-likelihood has a name: the score. It's a sum of independent pieces, one per "
            "observation, which means the law of large numbers and the central limit theorem apply to it, and that "
            "will be the key to everything in chapters five and nine. <bookmark mark='d'/> At a peak inside the "
            "parameter space, the score is zero. That's the likelihood equation. <bookmark mark='e'/> For the coin, the "
            "score is k over p minus n minus k over one minus p, and it vanishes at k over n. Maximum likelihood "
            "recovers the obvious answer, which is reassuring, and then goes on to give answers where nothing is obvious."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.95, x=-0.6, buff=0.45, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def horsekicks(self):
        d = load("likelihood")["hk"]
        lams = np.asarray(d["lams"])
        A = axes([0.4, 1.0], [-6, 0], x_length=5.6, y_length=3.6, xlabel=r"$\lambda$, \ deaths per corps-year",
                 ylabel=r"$\ell(\lambda) - \ell(\hat\lambda)$", xticks=[0.4, 0.6, 0.8, 1.0], yticks=[-6, -3, 0],
                 center=[-3.4, -0.4, 0])
        ax = A.ax
        cv = clip_curve(ax, lams, d["ll"], LIK, 3.5, ymin=-6)
        pk = DashedLine(ax.c2p(d["lam_hat"], -6), ax.c2p(d["lam_hat"], 0), color=S.ACCENT, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(r"\ell(\lambda) = \sum_i (x_i\log\lambda - \lambda - \log x_i!) = S\log\lambda - n\lambda + c", font_size=26),
            MathTex(rf"U(\lambda) = \frac{{S}}{{\lambda}} - n = 0\ \Rightarrow\ \hat\lambda = \bar x = \frac{{{d['S']}}}{{{d['n']}}} = {d['lam_hat']:.2f}",
                    font_size=28, color=LIK),
        ), 6.4, 0.3, [3.0, 2.2, 0])
        hdr = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (r"deaths", r"observed", r"expected")])
        xs = [1.0, 2.9, 4.9]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 0.7, 0])
        cells = VGroup()
        for i, (kk, o, e) in enumerate(zip(d["k"], d["count"], d["expected"])):
            y = 0.2 - 0.46 * i
            cells.add(VGroup(MathTex(str(kk), font_size=26).move_to([xs[0], y, 0]), MathTex(str(o), font_size=26, color=DATA).move_to([xs[1], y, 0]),
                             MathTex(f"{e:.1f}", font_size=26, color=LIK).move_to([xs[2], y, 0])))
        src = historical_tag(r"Bortkiewicz (1898): \ 10 corps $\times$ 20 years", corner=DR)
        with self.voiceover(
            "A real example, from Part 3's Museum. <bookmark mark='a'/> Ladislaus Bortkiewicz's two hundred "
            "corps-years of Prussian cavalry records, and the number of soldiers killed by horse kicks in each. If the "
            "counts are Poisson with rate lambda, the log-likelihood depends on the data only through their total, "
            "S. <bookmark mark='b'/> Set the score to zero: lambda hat is the sample mean, a hundred and twenty-two "
            "deaths over two hundred corps-years, point six one. <bookmark mark='c'/> Here's the curve, sharply peaked "
            "at point six one. <bookmark mark='d'/> And here's the check. With lambda equal to point six one, the "
            "Poisson model expects a hundred and nine corps-years with no deaths, and there were a hundred and nine; "
            "sixty-six with one, against sixty-five; twenty with two, against twenty-two. A one-parameter model, fitted "
            "by maximum likelihood, reproduces a century-old table almost exactly."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(cv), Create(pk))
            vo.wait_until("d")
            self.play(FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.3))
        self.clear_scene()

    def tanks(self):
        d = load("tanks")
        one, k = d["one"], len(d["one"])
        m = max(one)
        Ns = np.arange(150, 501)
        L = np.array([0.0 if N < m else float(np.exp(-np.sum(np.log(np.arange(N - k + 1, N + 1))))) for N in Ns])
        L = L / L.max()
        A = axes([150, 500], [0, 1.1], x_length=6.6, y_length=3.6, xlabel=r"$N$", ylabel=r"$L(N) \div L(214)$",
                 xticks=[150, 214, 300, 400, 500], yticks=[0, 0.5, 1], center=[-2.8, -0.6, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(N, 0), ax.c2p(N, v), color=LIK, stroke_width=1.6) for N, v in zip(Ns[::3], L[::3]) if v > 0])
        zero = Line(ax.c2p(150, 0), ax.c2p(m - 1, 0), color=S.RESID, stroke_width=5)
        rows = fit_rows(VGroup(
            MathTex(r"L(N) = P_N(\text{these 6 serials}) = \begin{cases} 0, & N < m \\[2pt] 1/\binom{N}{6}, & N \ge m \end{cases}",
                    font_size=28),
            label(r"zero below the largest serial; \ falling above it", font_size=24, color=GREY_A),
            MathTex(rf"\hat N_{{\mathrm{{MLE}}}} = m = {m}", font_size=32, color=MAX),
            label(r"the peak is at the jump: \ the score equation says nothing", font_size=24, color=S.ACCENT),
            label(r"and the MLE is biased low (ch.~1)", font_size=24, color=S.ACCENT),
        ), 4.9, 0.34, [4.2, -0.2, 0])
        with self.voiceover(
            "Now the tanks, by likelihood. <bookmark mark='a'/> Given N, every set of six serials from one to N is "
            "equally likely, so the probability of the six we saw is one over N choose six, provided N is at least "
            "the largest, and zero otherwise. <bookmark mark='b'/> As a function of N, the likelihood is zero up to two "
            "hundred and thirteen, jumps up at two hundred and fourteen, and then falls: every extra tank makes our "
            "particular six a little less probable. <bookmark mark='c'/> So the maximum likelihood estimate is the "
            "maximum itself. <bookmark mark='d'/> Two lessons. The peak is on the boundary, where the curve jumps, so "
            "setting a derivative to zero would never have found it. And the MLE here is the recipe we already saw was "
            "biased low: maximum likelihood is a principle, not a guarantee of quality in small samples."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(zero), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(bars[0], color=MAX))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def invariance(self):
        d = load("likelihood")["hk"]
        lh = d["lam_hat"]
        tc = theorem_card(r"Invariance of the MLE",
                          r"if $\hat\theta$ maximizes $L(\theta)$, \ then for any function $g$, \ the MLE of $g(\theta)$ is $g(\hat\theta)$",
                          who=r"Zehna (1966), \ via the induced likelihood", color=LIK, width=9.6, font_size=26).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"P(\text{{no deaths in a corps-year}}) = e^{{-\lambda}}\ \Rightarrow\ \widehat{{e^{{-\lambda}}}} = e^{{-{lh:.2f}}} = {np.exp(-lh):.3f}",
                    font_size=30, color=LIK),
            MathTex(r"\widehat{\sigma} = \sqrt{\widehat{\sigma^2}},\qquad \widehat{\log\text{odds}} = \log\frac{\hat p}{1 - \hat p}", font_size=30),
            label(r"unbiasedness has no such property: \ $E s^2 = \sigma^2$ but $E s < \sigma$ (Part 8)", font_size=24,
                  color=GREY_A),
            label(r"likelihood is about the data's fit, \ not the parameter's coordinates", font_size=26, color=S.ACCENT),
        ), 12.6, 0.36, [0, -1.4, 0])
        with self.voiceover(
            "One property makes maximum likelihood especially convenient. <bookmark mark='a'/> It's invariant. If theta "
            "hat maximizes the likelihood, then the maximum likelihood estimate of any function of theta is that "
            "function of theta hat. <bookmark mark='b'/> The probability that a corps-year passes without a death is e "
            "to the minus lambda, so its estimate is e to the minus point six one, point five four three. "
            "<bookmark mark='c'/> The MLE of a standard deviation is the square root of the MLE of the variance; of "
            "the log-odds, the log of the odds. <bookmark mark='d'/> Unbiasedness doesn't behave this way: s squared "
            "is unbiased for sigma squared, but s is biased for sigma, as Part 8 showed. <bookmark mark='e'/> The "
            "likelihood measures how well each distribution fits the data, and the same distribution fits equally well "
            "whatever coordinates we use to label it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
