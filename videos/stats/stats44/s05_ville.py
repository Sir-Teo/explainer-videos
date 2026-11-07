from __future__ import annotations

import math

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Maximal(VoiceoverScene):
    def construct(self):
        self.card()
        self.doob()
        self.ville_card()
        self.ville()
        self.paths()
        self.pvalues()
        self.board()

    def card(self):
        card = chapter_card(4, r"Maximal inequalities and Ville", r"How high can a fair game climb?", lit=(1939,), part=PART)
        with self.voiceover("Chapter four. Maximal inequalities: how high can a fair game climb?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def doob(self):
        rows = [
            cmath(r"\text{Doob}", r":", r"P\big(\max_{0 \le k \le n} M_k \ge \lambda\big) \le E[M_n^+] / \lambda \ \ \text{(submartingale)}", font_size=30),
            cmath(r"\text{proof}", r":", r"\tau = \text{first time above } \lambda; \ \ \lambda P(\tau \le n) \le E[M_\tau 1_{\tau \le n}] \le E[M_n^+]", font_size=28),
            cmath(r"L^p", r":", r"E\big[\max_{0 \le k \le n} |M_k|^p\big] \le \big(\tfrac{p}{p - 1}\big)^p E|M_n|^p, \ \ p > 1", font_size=30),
            cmath(r"\text{so}", r":", r"\text{a martingale's whole path is controlled by its last value}", font_size=30),
        ]
        rows[0][-1].set_color(MARTC)
        whys = [why(r"Doob's maximal inequality"), why(r"optional stopping again"), why(r"Doob's $L^p$ inequality"), why(r"Kolmogorov's, \ generalized")]
        with self.voiceover(
            "<bookmark mark='a'/> Doob's maximal inequality generalizes Kolmogorov's from the last part: the chance that a "
            "submartingale ever climbs above lambda before time n is at most the expected positive part at time n, over "
            "lambda. <bookmark mark='b'/> The proof stops at the first time the path crosses lambda; optional stopping, with "
            "a bounded time, does the rest. <bookmark mark='c'/> Its L p version bounds the whole running maximum by a "
            "constant times the final value, for every p above one. <bookmark mark='d'/> A martingale cannot wander far "
            "without its final value showing it."
        ) as vo:
            heading=label('Stop at the first crossing to control the running maximum',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ville_card(self):
        hc = history_card(1939, r"Jean Ville, \ \emph{\'Etude critique de la notion de collectif}",
                          r"a thesis against Richard von Mises's definition of randomness; \ to state it, \ Ville named and "
                          r"studied the \emph{martingale}, \ the gambler's betting system, \ and proved its maximal inequality",
                          color=MARTC, width=11.4, font_size=23).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"a random sequence is one on which no betting system gets rich", font_size=26, color=GREY_A),
            label(r"the word comes from the doubling strategy of the casinos", font_size=24, color=GREY_B),
        ), 12.4, 0.4, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The infinite-horizon version is older, and statistically the most important. In 1939 Jean "
            "Ville, criticizing Richard von Mises's definition of a random sequence, took the casino word martingale for a "
            "betting system and made it mathematics. <bookmark mark='b'/> His idea: a sequence is random if no betting "
            "system, playing fair odds against it, can get rich. <bookmark mark='c'/> And he proved the inequality that "
            "makes that idea quantitative."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def ville(self):
        rows = [
            cmath(r"M_n \ge 0", r",", r"\ M_0 = 1, \ \text{a (super)martingale under } H_0", font_size=32),
            cmath(r"\text{Ville}", r":", r"P_0\big(\sup_{n \ge 0} M_n \ge 1/\alpha\big) \le \alpha", font_size=36),
            cmath(r"\text{proof}", r":", r"\tau=\inf\{k:M_k\ge1/\alpha\}:\ \ P(\tau\le n)/\alpha\le E M_{\tau\wedge n}\le1", font_size=30),
            cmath(r"\text{test}", r":", r"\text{reject } H_0 \text{ when your wealth reaches } 1/\alpha, \ \text{at any time you like}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a fair bet against $H_0$"), why(r"Ville's inequality (1939)"), why(r"the maximal inequality, \ forever"), why(r"anytime-valid: \ Part 58")]
        with self.voiceover(
            "<bookmark mark='a'/> Let M be a nonnegative martingale, or supermartingale, starting at one under the null "
            "hypothesis: the wealth of someone betting against the null at fair odds, a likelihood ratio for instance. "
            "<bookmark mark='b'/> Ville's inequality: the chance that it ever reaches one over alpha, at any time at all, is "
            "at most alpha. <bookmark mark='c'/> It is Doob's inequality for each n, with the limit taken over all n. "
            "<bookmark mark='d'/> Read as a test: bet against the null, watch your wealth, and reject when it reaches one "
            "over alpha. You may look after every observation and stop whenever you like, and the false alarm rate is still "
            "at most alpha. Part fifty-eight builds modern anytime-valid inference on this one line."
        ) as vo:
            heading=label('Nonnegative wealth gives an infinite-horizon crossing bound',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def paths(self):
        d = load("lr")
        n = np.log10(np.asarray(d["idx"], float))
        A = axes([0, 3], [-6, 3], x_length=7.4, y_length=4.4, xlabel=r"tosses $n$", ylabel=r"$\log_{10}$ wealth",
                 xticks=[0, 1, 2, 3], yticks=[-6, -3, 0, 1, 3], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        bp = BettingPaths(ax, n, [np.asarray(r) / math.log(10) for r in d["log0"]], ymin=-6, ymax=3)
        bp1 = BettingPaths(ax, n, [np.asarray(r) / math.log(10) for r in d["log1"]], ymin=-6, ymax=3)
        side = fit_rows(VGroup(
            label(r"a fair coin; \ the gambler bets on heads at 0.6", font_size=22),
            label(r"blue: \ 40 of 4,000 wealth paths under $H_0$", font_size=22, color=NULLC),
            label(rf"reached 10 within 1,000 tosses: \ {100 * d['cross10']:.1f}\% \ (Ville: \ $\le 10\%$)", font_size=22, color=BADC),
            label(r"green: \ a biased coin: \ wealth grows exponentially", font_size=22, color=ALTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the test, drawn with this part's betting-paths instrument. A gambler bets against a fair coin, putting her wealth on heads at the odds a sixty percent coin would deserve. <bookmark mark='b'/> Forty of four thousand wealth paths under the null, on a log scale: most sink towards zero. <bookmark mark='c'/> The red line is wealth ten, one over alpha for alpha a tenth. Of the four thousand paths, {100 * d['cross10']:.1f} percent ever touched it within a thousand tosses, inside Ville's ten percent; The theorem bounds the true infinite-horizon crossing probability by ten percent, not the exact fraction in every finite simulation. <bookmark mark='d'/> Against a coin that really is biased, wealth grows exponentially, and the line is crossed early. This long-run log-wealth growth helps explain power, although it is not itself a finite-sample power calculation: the Kullback–Leibler divergence again."       ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 4,000 fair coins, 1,000 tosses each")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bp.paths(NULLC)), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(bp.threshold(0.1)), FadeIn(bp.crossers(0.1)), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(bp1.paths(ALTC)), FadeIn(side[3]), run_time=2.0)
        self.clear_scene()

    def board(self):
        show_board(self, board_rows("betting", "z test"),
                   "<bookmark mark='a'/> On the Board, a fair coin watched for a thousand tosses. A betting test that hedges on "
                   "both sides and rejects at wealth ten raises a false alarm eight point nine percent of the time: within its "
                   "ten percent, kept. <bookmark mark='b'/> A z test at the ten percent level, checked after every tenth toss, "
                   "raises one sixty percent of the time: broken. Peeking breaks a fixed-sample test; it cannot break Ville's.",
                   [("a", [0]), ("b", [1])])

    def pvalues(self):
        rows = fit_rows(VGroup(
            label(r"an anytime-valid p-value: \ $p_n = 1 / \max_{0 \le k \le n} M_k$", font_size=26, color=MARTC),
            label(r"by Ville, \ $P_0(p_n \le \alpha \text{ for some } n) \le \alpha$: \ valid however you stop", font_size=26),
            label(r"an e-value: \ $M_\tau$ itself, \ with $E_0 M_\tau \le 1$ at finite stopping times (or a defined limit)", font_size=26, color=S.ACCENT),
            label(r"evidence that can be multiplied across studies \ and continued after a look", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Ville's inequality turns wealth into p-values. Include the initial wealth of one. "
            "One over the running maximum is then an anytime-valid p-value: <bookmark mark='b'/> under the null, the "
            "chance it ever falls below alpha is at most alpha, whatever stopping rule the analyst follows, even one "
            "chosen after looking. <bookmark mark='c'/> The wealth at a stopping time is itself an e-value: for "
            "finite stopping times its expectation is at most one. An infinite stopping time needs the nonnegative "
            "supermartingale limit and Fatou's lemma. <bookmark mark='d'/> Unlike p-values, e-values from independent"
            " studies can simply be multiplied, Conditional validity also allows sequential products. A study can "
            "continue after an interim look while following the same valid wealth process; choosing a new favorable "
            "bet after seeing its outcomes is not licensed. Part fifty-eight is built on them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
