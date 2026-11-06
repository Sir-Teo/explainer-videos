from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats43.common import *  # noqa: F403


def sci(v: float) -> str:
    """A small distance as TeX: four decimals, or m x 10^e below a thousandth."""
    if v >= 1e-3:
        return f"{v:.4f}"
    e = int(np.floor(np.log10(v)))
    return rf"${v / 10 ** e:.1f} \times 10^{{{e}}}$"


class Extremes(VoiceoverScene):
    def construct(self):
        self.card()
        self.maxstable()
        self.proof()
        self.domains()
        self.table()
        self.portpirie()

    def card(self):
        card = chapter_card(13, r"Extremes", r"What can a maximum converge to?", lit=(1928, 1943), part=PART)
        with self.voiceover("Chapter thirteen. Extremes: what a maximum can converge to."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def maxstable(self):
        rows = [
            cmath(r"M_n", r"=", r"\max(X_1, \ldots, X_n), \ \ P(M_n \le x) = F(x)^n", font_size=34),
            cmath(r"\frac{M_n - b_n}{a_n}", r"\Rightarrow", r"G \ \text{non-degenerate}", font_size=34),
            cmath(r"\text{max-stable}", r":", r"G(x)^k = G(\alpha_k x + \beta_k) \ \ \text{for every } k", font_size=32),
            cmath(r"\text{FTG}", r":", r"G(x) = \exp\big(-(1 + \xi x)^{-1/\xi}\big)", font_size=34),
        ]
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"independence"), why(r"normalized maxima"), why(r"the limit's own property"), why(r"Gumbel $\xi = 0$; \ Fr\'echet $\xi > 0$; \ Weibull $\xi < 0$")]
        with self.voiceover(
            "<bookmark mark='a'/> Part six previewed the extreme-value families. The maximum of n independent copies has CDF F "
            "to the n. <bookmark mark='b'/> Suppose that, after centring by b n and scaling by a n, it converges to a "
            "non-degenerate limit G. <bookmark mark='c'/> The maximum of k n variables is the maximum of k blocks of n, so "
            "the limit must satisfy G to the k equals G of an affine change of x, for every k: it must be max-stable. "
            "<bookmark mark='d'/> Ronald Fisher and Leonard Tippett in 1928, and Boris Gnedenko rigorously in 1943, solved "
            "that equation: the only solutions form one family, the generalized extreme value laws, Gumbel when xi is zero, "
            "Fréchet when xi is positive, reversed Weibull when it is negative."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"-\log G(x)", r"=", r"\psi(x): \ \ k\, \psi(x) = \psi(\alpha_k x + \beta_k)", font_size=32),
            cmath(r"\text{extend}", r":", r"k \to s > 0 \text{ real}: \ s\, \psi(x) = \psi(\alpha(s) x + \beta(s))", font_size=32),
            cmath(r"\alpha(st)", r"=", r"\alpha(s)\alpha(t) \ \Rightarrow \ \alpha(s) = s^{-\xi}", font_size=32),
            cmath(r"\xi = 0", r":", r"\beta(s) = -\log s \Rightarrow \psi(x) = e^{-x}; \ \ \xi \ne 0: \ \psi(x) = (1 + \xi x)^{-1/\xi}", font_size=28),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"take logs"), why(r"monotone, \ so rationals then reals"), why(r"Cauchy's equation"), why(r"solve, \ up to affine change")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof in outline. Write psi for minus the log of G; max-stability says k times psi of x "
            "is psi of an affine function of x. <bookmark mark='b'/> Because psi is monotone, the relation extends from whole "
            "numbers k to rationals and then to every positive real s. <bookmark mark='c'/> Composing two such changes shows "
            "that the scale factor is multiplicative, alpha of s t equals alpha of s times alpha of t, so it is a power of "
            "s, s to the minus xi. <bookmark mark='d'/> When xi is zero the shift is minus log s and psi is e to the minus x, "
            "the Gumbel law; otherwise psi is one plus xi x to the minus one over xi. Three families, one equation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def domains(self):
        d = load("extremes")
        g = np.asarray(d["g"])
        A = axes([-3, 6], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$P((M_n - b_n)/a_n \le x)$",
                 xticks=[-2, 0, 2, 4, 6], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        gum = curve(ax, g, d["gumbel"], LIMC, 4)
        e10 = curve(ax, g, d["curves"]["exponential_10"], LAWC, 3)
        n10 = curve(ax, g, d["curves"]["normal_10"], BADC, 3)
        n1k = curve(ax, g, d["curves"]["normal_1000"], S.PRIOR, 3)
        side = fit_rows(VGroup(
            label(r"gold: \ the Gumbel limit", font_size=22, color=LIMC),
            label(r"exponential maxima, \ $n = 10$: \ already close", font_size=22, color=LAWC),
            label(r"normal maxima, \ $n = 10$ and $1{,}000$: \ still visibly off", font_size=22, color=BADC),
            label(r"exponential, \ Pareto, \ uniform: \ $F^n = (1 - t/n)^n$ vs $e^{-t}$", font_size=22, color=GREY_A),
            label(r"normal: \ the error falls like $1/\log n$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which laws go where? The exponential and the normal both lie in the Gumbel domain, Pareto "
            "tails in the Fréchet domain, bounded laws like the uniform in the reversed Weibull domain. <bookmark mark='b'/> "
            "But the speed differs enormously. Normalized exponential maxima are close to the Gumbel law already at ten. "
            "<bookmark mark='c'/> Normal maxima, at ten and even at a thousand, are still visibly off. <bookmark mark='d'/> "
            "For the exponential, the Pareto and the uniform, after normalizing, the CDF of the maximum is exactly one minus "
            "t over n, to the n, against its limit e to the minus t, so all three converge at the same rate, about one over "
            "n. <bookmark mark='e'/> For the normal, the error falls only like one over log n: a hundred thousand "
            "observations are not enough for a good Gumbel fit to normal maxima."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: $F(a_n x + b_n)^n$")))
            vo.wait_until("a")
            self.play(Create(gum), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(e10), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(n10), Create(n1k), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("extremes")
        ns = [10, 100, 1000, 10_000, 100_000]
        rows = [[r"$n$"] + [f"{n:,}" for n in ns]]
        for k, nm in [("exponential", r"exponential"), ("pareto", r"Pareto(2)"), ("uniform", r"uniform"), ("normal", r"normal")]:
            rows.append([nm] + [sci(r["d"]) for r in d["rows"][k]])
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.22, colors=[GREY_A, None, None, None, BADC]).move_to([0, 0.6, 0])
        msg = fit_rows(VGroup(
            label(r"exact Kolmogorov distances of the normalized maximum from its limit", font_size=24, color=GREY_A),
            label(r"three identical rows: \ the same function of $t$; \ the normal's barely halves in $10^4\times$ the data", font_size=24, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The exact distances. The exponential, Pareto and uniform rows are identical, not by "
            "accident but because each normalized maximum is the same function of a transformed variable. <bookmark "
            "mark='b'/> They fall tenfold for every tenfold increase in n. The normal row falls from point oh six four at ten to "
            "point oh three five at a hundred thousand: barely halved in ten thousand times the data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(msg[0]))
            vo.wait_until("b")
            self.play(FadeIn(msg[1]))
        self.clear_scene()

    def portpirie(self):
        d = load("extremes")
        yrs, pp = np.asarray(d["pp_years"]), np.asarray(d["pp"])
        A = axes([1920, 1990], [3.5, 4.8], x_length=5.6, y_length=3.4, xlabel=r"year", ylabel=r"annual maximum sea level, \ m",
                 xticks=[1930, 1950, 1970, 1990], yticks=[3.5, 4.0, 4.5], center=[-3.4, 0.8, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=LAWC) for a, b in zip(yrs, pp)])
        rl = DashedLine(ax.c2p(1920, d["rl100"]), ax.c2p(1990, d["rl100"]), color=S.ACCENT, stroke_width=2.5)
        B = axes([3.5, 4.8], [0, 1], x_length=4.2, y_length=3.4, xlabel=r"level, \ m", ylabel=r"CDF", xticks=[3.6, 4.0, 4.4, 4.8],
                 yticks=[0, 0.5, 1], center=[3.6, 0.8, 0])
        bx = B.ax
        xs = np.linspace(3.5, 4.8, 200)
        c = -d["xi"]
        fit = curve(bx, xs, stats.genextreme.cdf(xs, c, d["loc"], d["scale"]), LIMC, 3.5)
        srt = np.sort(pp)
        ecdf = VGroup(*[Dot(bx.c2p(v, (i + 0.5) / len(srt)), radius=0.04, color=LAWC) for i, v in enumerate(srt)])
        side = fit_rows(VGroup(
            label(rf"Port Pirie, \ South Australia: \ {len(pp)} annual maxima, \ 1923--1987", font_size=22),
            label(rf"GEV fit: \ $\hat\xi = {d['xi']:.3f}$, \ $\hat\mu = {d['loc']:.2f}$, \ $\hat\sigma = {d['scale']:.3f}$: \ close to Gumbel", font_size=22, color=LIMC),
            label(rf"the 100-year level: \ {d['rl100']:.2f} m \ (Gumbel {d['rl100_gumbel']:.2f} m); \ the record: \ {d['pp_max']:.2f} m", font_size=22, color=S.ACCENT),
        ), 12.4, 0.28, [0, -2.45, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Real maxima. Stuart Coles's standard example: the highest sea level each year at Port Pirie, "
            f"in South Australia, sixty-five years from 1923. <bookmark mark='b'/> Each point is already a maximum over a "
            f"year of tides, so the theorem says a generalized extreme value law should fit, and it does. The fitted shape xi "
            f"is {say(d['xi'], 2)}, close to the Gumbel case. <bookmark mark='c'/> The level exceeded on average once a "
            f"century, the hundred-year return level that engineers design sea walls for, is {say(d['rl100'], 2)} metres "
            f"under the fitted law, and {say(d['rl100_gumbel'], 2)} under a pure Gumbel. The record, in 1934, was "
            f"{say(d['pp_max'], 2)}. Part six's Dutch dikes were designed this way, with the theorem behind them."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(museum_tag(r"Port Pirie: \ Coles (2001)")))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ecdf), Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rl), FadeIn(side[2]))
        self.clear_scene()
