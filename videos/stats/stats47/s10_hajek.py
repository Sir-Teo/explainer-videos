from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Hajek(VoiceoverScene):
    def construct(self):
        self.card()
        self.regular()
        self.hodges()
        self.lam()
        self.chart()
        self.table()
        self.meaning()

    def card(self):
        card = chapter_card(9, r"The convolution and LAM theorems", r"In what sense the MLE is best", lit=(1970, 1972), part=PART)
        with self.voiceover("Chapter nine. Hájek's convolution and local asymptotic minimax theorems: in what sense the MLE is best."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def regular(self):
        rows = [
            cmath(r"T_n \text{ regular at } \theta", r":", r"\sqrt n\big(T_n - (\theta + h/\sqrt n)\big) \overset{\theta + h/\sqrt n}\Rightarrow L \ \ \text{the same } L \ \forall h", font_size=28),
            cmath(r"\text{convolution theorem}", r":", r"L = N(0, I_\theta^{-1}) * M \ \ \text{for some law } M", font_size=32),
            cmath(r"\text{so}", r":", r"\mathrm{Var}\, L \ge I_\theta^{-1}, \ \ P(L \in C) \le N(0, I^{-1})(C)", font_size=32),
            cmath(r"\text{the MLE}", r":", r"\text{regular, \ with } L = N(0, I^{-1}): \ M = \delta_0", font_size=32),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"its limit does not depend on $h$"), why(r"Hájek (1970)"), why(r"Anderson's lemma: \ any symmetric convex $C$"), why(r"efficient")]
        with self.voiceover(
            "<bookmark mark='a'/> Hájek's first theorem, of 1970, is about regular estimators: those whose limiting "
            "error distribution, at the scale one over root n, is the same under every local alternative. <bookmark "
            "mark='b'/> In a nonsingular regular LAN model, for an estimator regular under every fixed local shift, "
            "the limit law is the normal with the inverse information, convolved with some other law M: the best "
            "possible normal plus independent extra noise. <bookmark mark='c'/> When the convolution limit has finite"
            " covariance, its covariance is at least the inverse information, and by Anderson's lemma it puts no more"
            " probability than that normal into any symmetric convex set. <bookmark mark='d'/> A suitably consistent,"
            " asymptotically efficient regular MLE has M a point mass at zero: nothing added. It is efficient among "
            "regular estimators, with no unbiasedness required."
        ) as vo:
            heading=label('A regular LAN estimator has Gaussian noise plus independent noise',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hodges(self):
        rows = [
            cmath(r"\text{Hodges at } \theta = 0", r":", r"\text{under } \theta_n = h/\sqrt n, \ |\bar x| < n^{-1/4} \ \text{w.p.} \to 1", font_size=30),
            cmath(r"T_n = 0", r"\Rightarrow", r"\sqrt n(T_n - \theta_n) = -h", font_size=34),
            cmath(r"\text{the limit}", r":", r"\delta_{-h}: \ \text{a different law for each } h", font_size=34),
            cmath(r"\text{not regular}", r":", r"\text{so the convolution theorem says nothing about it}", font_size=32),
        ]
        rows[2][-1].set_color(HODC)
        rows[3][-1].set_color(HODC)
        whys = [why(r"inside the zone"), why(r"exactly"), why(r"it depends on $h$"), why(r"superefficiency's loophole")]
        with self.voiceover(
            "<bookmark mark='a'/> Hodges's estimator at zero fails this test. Under the local alternative h over root n, "
            "the sample mean is within n to the minus one quarter of zero with probability tending to one, <bookmark "
            "mark='b'/> so the estimator reports zero, and its scaled error is exactly minus h. <bookmark mark='c'/> The "
            "limit is a point mass at minus h: a different law for every h. <bookmark mark='d'/> It is not regular, so the "
            "convolution theorem does not apply. Superefficiency lives in exactly this loophole."
        ) as vo:
            heading=label('Hodges has a local error limit that depends on the shift',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lam(self):
        rows = [
            cmath(r"\text{any } T_n", r":", r"\lim_{c \to \infty} \liminf_n \sup_{|h| \le c} E_{\theta + h/\sqrt n}\, \ell\big(\sqrt n(T_n - \theta - h/\sqrt n)\big)", font_size=28),
            cmath(r"\phantom{X}", r"\ge", r"E\, \ell(Z), \ \ Z \sim N(0, I_\theta^{-1})", font_size=34),
            cmath(r"\ell \text{ bowl-shaped}", r":", r"\text{symmetric, \ quasi-convex: \ e.g.\ squared error}", font_size=32),
            cmath(r"\text{the MLE}", r":", r"\text{attains with efficient regularity and uniform local risk convergence}", font_size=34),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"no estimator regularity; \ model remains LAN"), why(r"Hájek (1972)"), why(r"the loss"), why(r"the final answer")]
        with self.voiceover(
            "<bookmark mark='a'/> The second theorem, of 1972, drops regularity of the estimator, while retaining the"
            " regular LAN model and appropriate measurability and loss assumptions. For any estimator whatever, take "
            "its worst risk over a neighbourhood of size c over root n around theta, <bookmark mark='b'/> let n grow "
            "and then c: the result is at least the risk of the normal with the inverse information. <bookmark "
            "mark='c'/> For a nonnegative lower-semicontinuous bowl-shaped loss, the lower bound follows first for "
            "bounded truncations and then by a limit. Squared error is an example. <bookmark mark='d'/> An efficient "
            "regular estimator attains the Gaussian bound when its local risks also converge uniformly as required. "
            "For unbounded squared loss that needs moment control; a distributional normal limit alone does not prove"
            " risk convergence. It is locally asymptotically minimax: the sense in which it is best. Hodges can win "
            "at a point and even over a fixed small local radius. It cannot improve the bound when n grows first and "
            "the local radius then grows without bound."
        ) as vo:
            heading=label('Local minimax takes sample size first and local radius second',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("hajek")
        h = np.asarray(d["h"])
        A = axes([-12, 12], [0, 40], x_length=7.4, y_length=4.4, xlabel=r"local parameter $h$", ylabel=r"$n\,E(T_n - h/\sqrt n)^2$",
                 xticks=[-10, -5, 0, 5, 10], yticks=[0, 1, 10, 20, 30, 40], center=[-2.5, 0.2, 0])
        rb = RiskBump(A.ax)
        bd = rb.bound(1.0, MLEC)
        cols = {"100": ALTC, "10000": S.ACCENT, "1000000": HODC, "100000000": S.PRIOR}
        cs = {n: rb.curve(h, d[f"n{n}"], c, 3.5, ymax=40) for n, c in cols.items()}
        par = rb.curve(h, h ** 2, LIMC, 2.5, ymax=40)
        side = fit_rows(VGroup(
            VGroup(label(r"Hodges, \ $n = $", font_size=22), label(r"$10^2$", font_size=22, color=ALTC), label(r"$10^4$", font_size=22, color=S.ACCENT),
                   label(r"$10^6$", font_size=22, color=HODC), label(r"$10^8$", font_size=22, color=S.PRIOR)).arrange(RIGHT, buff=0.15),
            label(r"blue dashed: \ the MLE, \ 1 at every $h$", font_size=22, color=MLEC),
            label(r"white: \ the limit $h^2$: \ the point mass at $-h$", font_size=22, color=LIMC),
            label(r"limiting risk $h^2$ is below 1 for $|h|<1$", font_size=22, color=GOODC),
            label(r"over $|h|\le c$: \ worst risk $\to c^2$; \ then $c\to\infty$", font_size=22, color=HODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The risk-bump explorer shows both theorems at once. Here is Hodges's scaled risk as a "
            "function of the local parameter, for a hundred up to a hundred million observations. <bookmark mark='b'/> The "
            "MLE's is one, everywhere. <bookmark mark='c'/> As n grows, Hodges's local risk converges to h squared, the "
            "squared error of always saying zero, <bookmark mark='d'/> which is below one only for h between minus one and "
            "one. <bookmark mark='e'/> So the worst risk over any neighbourhood of radius c tends to c squared: below one for "
            "small c, unbounded for large c. In the limit of large neighbourhoods, it loses."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ normal integrals")))
            vo.wait_until("a")
            self.play(*[Create(cs[n]) for n in cols], FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(bd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(par), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("hajek")
        cs = d["cs"]
        rows = [[r"$n$"] + [rf"$\sup_{{|h| \le {c}}}$" for c in cs]]
        for n in ("100", "10000", "1000000", "100000000"):
            rows.append([rf"$10^{{{len(n) - 1}}}$"] + [f"{v:.2f}" for v in d["sup"][n]])
        rows.append([r"MLE"] + ["1.00"] * len(cs))
        tab = table_rows(rows, font_size=30, col_buff=1.0, row_buff=0.3, colors=[GREY_A, None, None, None, None, MLEC]).move_to([0, 0.6, 0])
        note_ = label(r"Hodges's worst local scaled risk: \ it tends to $c^2$, \ this Hodges example's $\liminf$ is at least 1 once $c \ge 1$", font_size=24, color=S.ACCENT).move_to([0, -2.4, 0])
        if note_.width > 12.6:
            note_.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> In numbers: the worst scaled risk of Hodges's estimator over neighbourhoods of "
            "radius one, two, four and eight. <bookmark mark='b'/> For large n the entries approach one, four, "
            "sixteen and sixty-four: c squared. <bookmark mark='c'/> The MLE's worst risk is one in every "
            "neighbourhood. The local asymptotic minimax lower bound is one after taking the large-sample lower limit"
            " and then allowing c to grow; it is not a universal lower bound for every fixed small c."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:5]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tab[5]), FadeIn(note_))
        self.clear_scene()

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"Le Cam (1953): \ superefficiency is possible only on a set of Lebesgue measure zero", font_size=26),
            label(r"Hájek: \ and even there, \ it costs worst-case risk nearby", font_size=26, color=HODC),
            label(r"modern echoes: \ shrinkage and sparse estimators \ (the lasso, \ thresholding)", font_size=26, color=S.ACCENT),
            label(r"can be superefficient at zero with suitable threshold tuning; \ risk rises near the threshold \ (Leeb \& Pötscher 2005)", font_size=26, color=GREY_A),
            label(r"the Bayesian counterpart: \ Bernstein--von Mises, \ Part 53", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Le Cam proved in 1953 that superefficiency can only happen on a set of parameter "
            "values of Lebesgue measure zero. <bookmark mark='b'/> Hájek's theorems add that even there it is paid "
            "for in worst-case risk nearby. <bookmark mark='c'/> The lesson is not academic. Thresholding and "
            "lasso-type estimators, Part thirty-two's sparse methods, <bookmark mark='d'/> with sufficiently "
            "aggressive threshold tuning can be superefficient at zero: excellent when the truth is sparse, and with "
            "bumps of risk near the edge of detectability, as Hannes Leeb and Benedikt Pötscher showed. <bookmark "
            "mark='e'/> The Bayesian counterpart, the Bernstein–von Mises theorem, is Part fifty-three."       ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
