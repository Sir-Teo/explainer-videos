from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Martingales(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.lr()
        self.doob()
        self.urn()

    def card(self):
        card = chapter_card(2, r"Martingales", r"A fair game, \ in symbols", part=PART)
        with self.voiceover("Chapter two. Martingales: a fair game, in symbols."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"M_n", r":", r"\mathcal F_n\text{-measurable}, \ E|M_n| < \infty, \ \ E[M_{n+1} \mid \mathcal F_n] = M_n", font_size=32),
            cmath(r"\text{sums}", r":", r"M_n = \textstyle\sum_{k \le n} X_k, \ E[X_k \mid \mathcal F_{k-1}] = 0: \ \text{dependent steps allowed}", font_size=28),
            cmath(r"\text{products}", r":", r"M_n = \textstyle\prod_{k \le n} Y_k, \ E[Y_k \mid \mathcal F_{k-1}] = 1", font_size=32),
            cmath(r"\text{Doob}", r":", r"M_n = E[Z \mid \mathcal F_n]: \ \text{what you would predict, \ as you learn}", font_size=30),
        ]
        rows[0][-1].set_color(MARTC)
        whys = [why(r"a fair game"), why(r"martingale differences"), why(r"wealth, \ likelihood ratios"), why(r"the Doob martingale")]
        with self.voiceover(
            "<bookmark mark='a'/> A martingale is a sequence adapted to a growing flow of information, integrable, "
            "whose conditional expectation tomorrow, given everything known today, is its value today: a fair game. "
            "<bookmark mark='b'/> Sums of steps whose conditional mean is zero are martingales, and the steps need "
            "not be independent; that is the whole point. <bookmark mark='c'/> For nonnegative factors, products with"
            " conditional mean one are martingales too. Signed products additionally need integrability: a gambler's "
            "wealth under fair bets, or a likelihood ratio. <bookmark mark='d'/> And the successive predictions of "
            "any fixed integrable random variable, as information arrives, form a martingale named after Joseph Doob,"
            " whose 1953 book made the theory."
        ) as vo:
            heading=label('Martingales have zero conditional drift',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lr(self):
        d = load("lr")
        n = np.log10(np.asarray(d["idx"], float))
        A = axes([0, 3], [-12, 6], x_length=7.4, y_length=4.4, xlabel=r"tosses $n$", ylabel=r"$\log L_n$, \ $L_n = \prod_k \frac{q(X_k)}{p(X_k)}$",
                 xticks=[0, 1, 2, 3], yticks=[-12, -6, 0, 6], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        p0 = VGroup(*[polyline(ax, n, row, NULLC, 1.4, 0.6) for row in d["log0"]])
        p1 = VGroup(*[polyline(ax, n, row, ALTC, 1.4, 0.7) for row in d["log1"]])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"testing a fair coin ($p$) against $q$: \ heads w.p.\ 0.6", font_size=22),
            label(r"under $p$: \ $E_p[q/p] = 1$, \ so $L_n$ is a martingale", font_size=22, color=NULLC),
            label(rf"yet $\log L_n$ drifts down at $\text{{KL}}(p \| q) = {d['kl_null']:.4f}$ per toss", font_size=22, color=NULLC),
            label(rf"mean 1, \ median about $10^{{{int(np.round(np.log10(d['median_final0'])))}}}$ after 1,000: \ $L_n \to 0$ a.s.", font_size=22, color=GREY_A),
            label(rf"under $q$: \ up at $\text{{KL}}(q \| p) = {d['kl_alt']:.4f}$ per toss", font_size=22, color=ALTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The statistician's martingale is the likelihood ratio. Test a fair coin against one that lands heads sixty percent of the time, and multiply, toss by toss, the ratio of the two probabilities of what happened. <bookmark mark='b'/> If the coin is fair, each factor has mean one, so the product is a martingale with mean one forever. <bookmark mark='c'/> Nevertheless the typical null path trends down over the long run, with local upward moves: the logarithm drifts at minus the Kullback–Leibler divergence, {say(d['kl_null'], 4)} per toss. <bookmark mark='d'/> After a thousand tosses the median ratio is about one in a billion, while the mean is still one, held up by rare enormous paths. A martingale can converge to zero almost surely while its mean stays fixed. <bookmark mark='e'/> If the coin is biased, the green paths climb instead, at the other divergence. This asymmetry is the engine of sequential testing."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), FadeIn(exact_tag(r"simulated: 40 null and 20 biased coins")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(p0), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(p1), FadeIn(side[4]), run_time=2.0)
        self.clear_scene()

    def doob(self):
        rows = [
            cmath(r"X_n", r"=", r"M_n + A_n, \ \ A_n = \textstyle\sum_{k \le n} E[X_k - X_{k-1} \mid \mathcal F_{k-1}]", font_size=32),
            cmath(r"A_n", r":", r"\text{predictable: \ known one step ahead}", font_size=32),
            cmath(r"X_n = S_n^2", r":", r"S_n^2 = (S_n^2 - n) + n \ \ \text{for a fair } \pm 1 \text{ walk}", font_size=32),
            cmath(r"\langle M \rangle_n", r"=", r"\textstyle\sum_k E[(M_k - M_{k-1})^2 \mid \mathcal F_{k-1}]: \ \text{the predictable variation}", font_size=28),
        ]
        rows[0][-1].set_color(MARTC)
        whys = [why(r"Doob's decomposition"), why(r"the drift"), why(r"an example"), why(r"chapters 7 and 13")]
        with self.voiceover(
            "<bookmark mark='a'/> Any adapted integrable sequence splits into a martingale plus a drift, which is the"
            " sum of the expected next steps. <bookmark mark='b'/> The drift is predictable: each term is known one "
            "step ahead. <bookmark mark='c'/> For the square of a fair random walk, the drift is just n, so S n "
            "squared minus n is a martingale. <bookmark mark='d'/> For a square-integrable martingale, applied to its"
            " square, the drift is the predictable variation, the sum of conditional variances of the steps: the "
            "quantity the martingale central limit theorem and the theory of counting processes are built on."
        ) as vo:
            heading=label('An adapted process splits into martingale and predictable drift',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def urn(self):
        d = load("urn")
        st = np.asarray(d["steps"], float)
        A = axes([0, 2000], [0, 1], x_length=5.4, y_length=3.2, xlabel=r"draws", ylabel=r"share of red", xticks=[0, 1000, 2000],
                 yticks=[0, 0.5, 1], center=[-3.5, 0.95, 0])
        B = axes([0, 1], [0, 2], x_length=4.2, y_length=3.2, xlabel=r"share after 600 draws", ylabel=r"density", xticks=[0, 0.5, 1], yticks=[0, 1, 2],
                 center=[3.6, 0.95, 0])
        cols = [CHAINC, MARTC, S.ALT, S.PRIOR, S.KEPT, S.RESID]
        paths = VGroup(*[polyline(A.ax, st, row, cols[i % 6], 1.8, 0.8) for i, row in enumerate(d["paths"])])
        e = np.asarray(d["edges"])
        hb = bars_at(B.ax, (e[:-1] + e[1:]) / 2, d["hist"], e[1] - e[0], MARTC, opacity=0.75)
        flat = DashedLine(B.ax.c2p(0, 1), B.ax.c2p(1, 1), color=LIMC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"P\'olya's urn: \ draw a ball, \ return it with another of its colour", font_size=22),
            label(r"the share of red is a martingale, \ bounded, \ so it converges", font_size=22, color=MARTC),
            label(r"limit: Uniform(0,1); plotted finite draws: 601-point uniform lattice", font_size=22, color=LIMC),
            label(rf"finite-law KS $D={d['ks_d']:.3f}$; Monte Carlo $p={d['ks_p']:.3f}$ (9,999 null runs)", font_size=22, color=GREY_A),
            label(r"the draws are exchangeable: \ de Finetti's mixture, \ seen (Part 5)", font_size=22, color=S.ACCENT),
        ), 12.4, 0.28, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> George Pólya's urn starts with one red ball and one blue. Draw a ball at random, "
            "and return it with another of the same colour. <bookmark mark='b'/> The share of red is a martingale, "
            "and it is bounded between zero and one; chapter five will show that such a martingale must converge. "
            "<bookmark mark='c'/> The theoretical limits have a uniform distribution. Here we simulate two thousand "
            "independent urns for six hundred draws, not all the way to their limits. Their terminal shares follow an"
            " exact uniform lattice on six hundred and one possible values; the displayed goodness-of-fit check is "
            "calibrated to that finite law by Monte Carlo. <bookmark mark='d'/> The colours drawn are exchangeable "
            "but not independent: given the limit, they are independent coins with that probability of red. That is "
            "de Finetti's theorem from Part five, whose reverse-martingale proof chapter five outlines."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(exact_tag(r"24 long paths; 2,000 terminal urns, 600 draws")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(paths), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(hb), Create(flat), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
