from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


class Variance(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.sums()
        self.petersburg()
        self.running()
        self.utility()

    def card(self):
        card = chapter_card(12, r"Variance, and a game worth infinity", r"How far from its expectation does a "
                            r"variable stray?", lit=(1738,), part=PART)
        with self.voiceover("Chapter twelve. Variance, and a game worth infinity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        d = load("variance")
        rows = [
            cmath(r"\mathrm{Var}\, X", r"=", r"E\big[(X - \mu)^2\big]", font_size=40),
            cmath(r"\mathrm{Var}\, X", r"=", r"E X^2 - 2\mu\, E X + \mu^2", font_size=40),
            cmath(r"\mathrm{Var}\, X", r"=", r"E X^2 - \mu^2", font_size=40),
            cmath(r"\mathrm{Var}(\text{die})", r"=", rf"\tfrac{{91}}{{6}} - \left(\tfrac72\right)^2", r"=",
                  rf"{frac(d['Var'])}", font_size=40),
        ]
        rows[3][4].set_color(EXACT)
        whys = [why(r"$\mu = E X$: \ the mean squared deviation"), why(r"expand; \ linearity"),
                why(r"$E X = \mu$"), why(r"$E X^2 = \tfrac16(1 + 4 + \dots + 36)$")]
        title = label(r"Variance: \ Part 1's spread, \ for a random variable", font_size=34).to_edge(UP, buff=0.4)
        sd = label(r"standard deviation: \ $\sqrt{\mathrm{Var}\, X}$, \ in the units of $X$", font_size=26,
                   color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Expectation is the centre. With a finite second moment, variance measures the spread around it, as "
            "it did for data in Part 1. "
            "<bookmark mark='a'/> The variance of X is the expected squared distance from its mean, mu. "
            "<bookmark mark='b'/> Expand the square and use linearity: expected X squared, minus two mu times the "
            "expectation of X, plus mu squared. <bookmark mark='c'/> The expectation of X is mu, so this collapses "
            "to the shortcut: the mean of the square minus the square of the mean. <bookmark mark='d'/> For one die "
            "the mean of the square is ninety-one sixths and the mean is seven halves, so the variance is thirty-five "
            "twelfths. <bookmark mark='e'/> Its square root, the standard deviation, about one point seven, is in the "
            "same units as the die."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=4, top=2.4, x=-0.8, buff=0.5)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k in (1, 2))
            vo.wait_until("e")
            self.play(FadeIn(sd))
        self.clear_scene()

    def sums(self):
        d = load("variance")
        rows = [
            cmath(r"\mathrm{Var}(X + Y)", r"=", r"\mathrm{Var}\, X + \mathrm{Var}\, Y + 2\,\mathrm{Cov}(X, Y)",
                  font_size=36),
            cmath(r"\mathrm{Var}(X_1 + \cdots + X_n)", r"=", r"n\, \mathrm{Var}\, X_1", font_size=36),
            cmath(r"\mathrm{Var}(\text{ten dice})", r"=", rf"10 \cdot \tfrac{{35}}{{12}} = {frac(d['var_ten'])}",
                  font_size=36),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"$\mathrm{Cov}(X, Y) = E[(X - EX)(Y - EY)]$"), why(r"iid, finite variance: \ covariances $0$, same variance"),
                why(r"the engine: \ \texttt{die.iid\_sum(10).var()}")]
        sd = label(r"so the SD of a sum of $n$ grows like $\sqrt n$, \ and the SD of an \emph{average} shrinks like "
                   r"$1/\sqrt n$", font_size=26, color=S.ACCENT).to_edge(DOWN, buff=0.9)
        back = label(r"Part 1's $\sigma/\sqrt{n}$, \ explained: \ Part 6 makes it a law", font_size=24, color=GREY_B)
        back.next_to(sd, DOWN, buff=0.2)
        intro = label("Variances of independent sums", font_size=36)
        with self.voiceover(
            "Variances of sums are where independence earns its keep. <bookmark mark='a'/> In general the variance "
            "of a sum is the sum of the variances plus twice the covariance, which measures how X and Y move "
            "together. <bookmark mark='b'/> For independent variables every covariance is zero, so variances simply "
            "add: n independent copies have n times the variance. <bookmark mark='c'/> Ten dice: ten times "
            "thirty-five twelfths, as the engine confirms by convolving ten dice exactly. <bookmark mark='d'/> So "
            "the standard deviation of a sum grows only like root n, and the standard deviation of an average "
            "shrinks like one over root n. That's the sigma over root n we met at the end of Part 1, now derived; "
            "Part 6 turns it into the law of large numbers."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.2, buff=0.6)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(sd), FadeIn(back))
        self.clear_scene()

    def petersburg(self):
        d = load("variance")
        hc = history_card(1738, r"Daniel Bernoulli, \ St.\ Petersburg Academy", r"the problem: \ his cousin "
                          r"Nicolaus Bernoulli, \ 1713", color=S.MUSEUM, width=5.2, font_size=22).to_corner(UL, buff=0.35)
        coins = VGroup()
        for k in range(1, 6):
            seq = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=GREY_B if j < k - 1 else S.ACCENT,
                                  fill_opacity=0.9) for j in range(k)]).arrange(RIGHT, buff=0.08)
            labs = VGroup(*[label(r"T" if j < k - 1 else r"H", font_size=18, color=BLACK).move_to(c)
                            for j, c in enumerate(seq)])
            pay = MathTex(rf"2^{k} = {2 ** k}", font_size=28, color=S.ACCENT)
            pr = MathTex(rf"\tfrac{{1}}{{{2 ** k}}}", font_size=28, color=GREY_A)
            coins.add(VGroup(VGroup(seq, labs), pr, pay))
        for c in coins:
            c[0].move_to([-3.6, 0, 0], aligned_edge=LEFT)
            c[1].move_to([-0.4, 0, 0])
            c[2].move_to([1.4, 0, 0], aligned_edge=LEFT)
        coins.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-1.2, -0.6, 0])
        heads = VGroup(label(r"tosses", font_size=24, color=GREY_B), label(r"chance", font_size=24, color=GREY_B),
                       label(r"you win", font_size=24, color=GREY_B))
        for h_, x in zip(heads, (coins[0][0].get_x(), coins[0][1].get_x(), coins[0][2].get_x())):
            h_.move_to([x, coins.get_top()[1] + 0.35, 0])
        ev = MathTex(r"E(\text{prize})", r"=", r"\tfrac12 \cdot 2 + \tfrac14 \cdot 4 + \tfrac18 \cdot 8 + \cdots",
                     r"=", r"1 + 1 + 1 + \cdots", r"=", r"\infty", font_size=34).to_edge(DOWN, buff=0.5)
        ev[6].set_color(S.RESID)
        q = label(r"how much would you pay to play?", font_size=30, color=S.ACCENT).move_to([4.3, 2.3, 0])
        with self.voiceover(
            "Now a game that broke the theory of expectation, or seemed to. <bookmark mark='a'/> It was posed by "
            "Nicolaus Bernoulli in 1713, and his cousin Daniel published the most famous analysis of it in 1738, "
            "in the journal of the academy at St. Petersburg. <bookmark mark='b'/> Toss a fair coin until it lands "
            "heads. If the first head comes on toss k, you win two to the k ducats: two if it's the first toss, "
            "four if the second, eight if the third, doubling each time. <bookmark mark='c'/> How much would you "
            "pay to play? Pascal and Huygens would say: the expected prize. <bookmark mark='d'/> Each term of the "
            "expectation is a probability of one over two to the k times a prize of two to the k: one ducat. "
            "Infinitely many terms of one. The expected prize is infinite. Yet almost nobody would pay even twenty "
            "ducats."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(heads), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in coins], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(Write(ev))
        self.clear_scene()

    def running(self):
        d = load("variance")
        ns, run, lg = np.asarray(d["ns"]), np.asarray(d["running"]), np.asarray(d["log2"])
        A = axes([0, 20.5], [0, 32], x_length=9.4, y_length=4.6, xlabel=r"games played (log scale)",
                 ylabel=r"average prize so far (ducats)", xticks=[0, 5, 10, 15, 20], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: rf"2^{{{int(v)}}}", center=[-1.0, -0.3, 0])
        ax = A.ax
        cv = curve(ax, lg, run, SIM, 2.5)
        guide = curve(ax, lg, lg, EXACT, 2.5)
        gl = MathTex(r"\log_2 n", font_size=30, color=EXACT).next_to(ax.c2p(20, 20), UR, buff=0.1)
        tag = note(rf"simulated: $2^{{20}} = {fmt_int(d['n_games'])}$ games; \ largest prize "
                   rf"{fmt_int(int(d['max_pay']))} ducats").to_corner(DR, buff=0.3)
        feller = label(r"$S_n/(n\log_2 n) \to 1$ in probability \ (Feller, 1945)", font_size=24,
                       color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What actually happens if you play, again and again? <bookmark mark='a'/> Here are a million simulated "
            "games, and the average prize so far, with the number of games on a doubling scale. <bookmark mark='b'/> "
            "The average never settles. It drifts upward, jumping whenever a long run of tails pays out a huge prize, "
            f"and the biggest of the million paid {money(d['max_pay'])} ducats. <bookmark mark='c'/> William Feller "
            "showed that the average of n games, divided by the base-two logarithm of n, converges to one in "
            "probability. That describes typical growth, with occasional much larger excursions; it is not a "
            "promise that every running path hugs this line. An infinite expectation doesn't mean infinite winnings. It means "
            "there's no average for the averages to settle down to, and the law of averages in Part 6 will need a "
            "finite mean."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(cv, color=S.ACCENT, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(guide), FadeIn(gl), FadeIn(feller))
        self.clear_scene()

    def utility(self):
        d = load("variance")
        rows = [
            cmath(r"E \log_2(\text{prize})", r"=", r"\sum_{k \ge 1} \frac{k}{2^k}", r"=", r"2", font_size=38),
            cmath(r"\text{certainty equivalent of prize}", r"=", r"2^{E \log_2(\text{prize})}", r"=", r"4 \text{ ducats}", font_size=32),
        ]
        rows[0][4].set_color(EXACT)
        rows[1][4].set_color(EXACT)
        whys = [why(r"Bernoulli: \ value money by its logarithm"), why(r"the sure amount with the same expected log")]
        A = axes([0, 34], [-1, 5.5], x_length=4.6, y_length=2.8, xlabel=r"wealth", ylabel=r"$\log_2$",
                 xticks=[0, 8, 16, 32], yticks=[-1, 0, 5], center=[-3.8, -1.6, 0])
        xs = np.linspace(0.5, 34, 200)
        lc = curve(A.ax, xs, np.log2(xs), S.LIK, 3)
        lab = label(r"each doubling adds the same utility", font_size=22, color=S.LIK).next_to(A, UP, buff=0.15)
        take = VGroup(label(r"expectation of money is not the value of money", font_size=26, color=S.ACCENT),
                      label(r"expected utility: \ von Neumann \& Morgenstern, 1944; \ Kelly betting, 1956",
                            font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if take.width > 7.4:
            take.width = 7.4
        take.move_to([2.7, -1.8, 0])
        intro = label('Valuing a random prize', font_size=36)
        with self.voiceover(
            "Daniel Bernoulli's own answer changed economics. <bookmark mark='a'/> A ducat means less to a rich man "
            "than to a poor one, he argued, so we should value money by its logarithm: each doubling of wealth adds "
            "the same amount of satisfaction. <bookmark mark='b'/> The expected logarithm of the prize is the sum of "
            "k over two to the k, which is exactly two. <bookmark mark='c'/> So the game is worth the sure amount "
            "whose logarithm is two: four ducats. This is the certainty equivalent of the prize alone, not an "
            "entry fee. A player's willingness to pay depends on initial wealth: compare the expected log of "
            "wealth minus the fee plus the prize with the log of starting wealth. <bookmark mark='d'/> The "
            "expectation of money is not the value of money. Two centuries later the idea became expected utility "
            "theory, and the logarithm became Kelly's rule for sizing bets."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), Create(lc), FadeIn(lab))
            step = ladder(self, rows, whys, keep=2, top=2.6, x=0.8, buff=0.7)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(take, shift=UP * 0.2))
        _ = d
        self.clear_scene()
