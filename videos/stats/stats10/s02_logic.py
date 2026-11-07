from __future__ import annotations

from math import comb

import numpy as np
from scipy import stats

from videos.stats.stats10.common import *  # noqa: F403


class Logic(VoiceoverScene):
    def construct(self):
        self.card()
        self.ingredients()
        self.sign_test()
        self.disjunction()
        self.which_null()
        self.bernoulli()
        self.five_percent()

    def card(self):
        card = chapter_card(1, r"Fisher's logic", r"A null, \ a statistic, \ a tail probability", lit=(1710,), part=PART)
        with self.voiceover("Chapter one. Fisher's logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ingredients(self):
        items = [
            (r"1.\ \ a \emph{null hypothesis} $H_0$: \ a specified statistical claim and its sampling assumptions", NULLC),
            (r"2.\ \ a \emph{test statistic} $T(X)$: \ a number that is large when the data disagree with $H_0$", WHITE),
            (r"3.\ \ the \emph{$p$-value}: \ $p = P_{H_0}\big(T(X) \ge T(x_{\mathrm{obs}})\big)$", OBS),
        ]
        rows = fit_rows(VGroup(*[label(t, font_size=28, color=c) for t, c in items]), 12.6, 0.55, [0, 0.8, 0])
        ex = fit_rows(VGroup(
            label(r"Arbuthnot: \ $H_0$: \ each year is a fair coin; \ $T$ = years with more boys; \ $p = P(T \ge 82) = 2^{-82}$",
                  font_size=24, color=GREY_A),
            label(r"the tea: \ $H_0$: \ she is guessing; \ $T$ = milk-first cups found; \ $p = P(T \ge 4) = 1/70$", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.0, 0])
        intro = label('A specified null, a statistic, and its null tail probability', font_size=36)
        with self.voiceover(
            "Arbuthnot's argument, and the tea, share a structure that Fisher made into a method. "
            "<bookmark mark='a'/> First, a null hypothesis: a specified claim and sampling model, here how the data would arise if nothing "
            "interesting were happening, if the years were coins or the lady were guessing. "
            "<bookmark mark='b'/> Second, a test statistic: a number computed from the data that tends to be large when "
            "the data disagree with the null. <bookmark mark='c'/> Third, the p-value: the probability, computed under "
            "the null, of a statistic at least as large as the one observed. <bookmark mark='d'/> For Arbuthnot, the "
            "statistic is the number of boys' years, and the p-value is two to the minus eighty-two. "
            "<bookmark mark='e'/> For the tea, the statistic is the number of milk-first cups correctly found, and the "
            "p-value is one in seventy. Notice what's absent: there's no alternative hypothesis anywhere. Fisher's test "
            "only asks how surprising the data are, if the null is true."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(ex[0]))
            vo.wait_until("e")
            self.play(FadeIn(ex[1]))
        self.clear_scene()

    def sign_test(self):
        n = 20
        ks = np.arange(n + 1)
        pmf = np.array([comb(n, k) for k in ks]) / 2 ** n
        A = axes([-0.5, 20.5], [0, 0.2], x_length=7.6, y_length=3.8, xlabel=r"boys' years, \ out of 20", ylabel=r"$P_{H_0}$",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2], center=[-2.2, -0.2, 0])
        ax = A.ax
        bars = bars_at(ax, ks, pmf, 0.8, NULLC, highlight=set(range(15, 21)), hcolor=OBS)
        tail = sum(pmf[15:])
        rows = fit_rows(VGroup(
            label(r"a smaller version: \ 20 years", font_size=24, color=GREY_A),
            MathTex(r"H_0:\ T \sim \mathrm{Binomial}\big(20, \tfrac12\big)", font_size=30),
            MathTex(rf"T_{{\mathrm{{obs}}}} = 15:\ \ p = P(T \ge 15) = {tail:.4f}", font_size=30, color=OBS),
            MathTex(r"T_{\mathrm{obs}} = 82 \text{ of } 82:\ \ p = 2^{-82}", font_size=30, color=OBS),
            label(r"the sign test: \ only the direction of each year counts", font_size=24, color=GREY_A),
        ), 5.2, 0.34, [4.3, -0.2, 0])
        with self.voiceover(
            "Here's the null distribution of a sign test, drawn for twenty years to keep it visible. "
            "<bookmark mark='a'/> If each year is a fair coin, the number of boys' years is binomial with twenty trials "
            "and probability one half: a symmetric hump around ten. <bookmark mark='b'/> Suppose boys had won fifteen "
            "years out of twenty. The p-value is the total height of the bars at fifteen and beyond: about two "
            "percent. <bookmark mark='c'/> Arbuthnot's case is the far end of a much longer row: eighty-two out of "
            "eighty-two, a single bar so small it's two to the minus eighty-two. <bookmark mark='d'/> The test throws "
            "away everything but the sign of each year, which is why it's called the sign test. It's the oldest "
            "significance test there is, and it still gets used, because it needs no model for the magnitudes. Its binomial calibration still needs independent signs with probability one half under the null, after ties are handled."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.05), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), *[Indicate(b, color=OBS) for b in bars[15:]])
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def disjunction(self):
        q = label(r"``Either an exceptionally rare chance has occurred, \ or the theory of random distribution is not true.''",
                  font_size=30).move_to([0, 1.2, 0])
        who = label(r"R. A. Fisher, \ \emph{Statistical Methods and Scientific Inference} (1956)", font_size=22,
                    color=GREY_A).next_to(q, DOWN, buff=0.3)
        rows = fit_rows(VGroup(
            label(r"a small $p$ is evidence against $H_0$, \ graded, \ not a verdict", font_size=26, color=OBS),
            label(r"a large $p$ is not evidence for $H_0$: \ the data may simply be too few to tell", font_size=26),
            label(r"``the null hypothesis is never proved or established, \ but is possibly disproved'' \ (\emph{Design}, 1935)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.36, [0, -1.6, 0])
        intro = label('Interpreting incompatibility with a null model', font_size=36)
        with self.voiceover(
            "What does a small p-value license us to say? <bookmark mark='a'/> Fisher put it as a disjunction: either "
            "an exceptionally rare chance has occurred, or the theory of random distribution is not true. "
            "<bookmark mark='b'/> So a small p-value is evidence against the null, and the smaller it is, the stronger "
            "the evidence. For Fisher it was graded, not a yes-or-no verdict. <bookmark mark='c'/> And a large p-value "
            "is not evidence for the null. It may only mean the experiment was too small to see anything. "
            "<bookmark mark='d'/> In The Design of Experiments he wrote that the null hypothesis is never proved or "
            "established, but is possibly disproved, in the course of experimentation."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(q), FadeIn(who))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def which_null(self):
        d = load("arbuthnot")
        n_year = (d["males"] + d["females"]) / d["n"]
        p = d["males"] / (d["males"] + d["females"])
        year_size = round(n_year)
        py = stats.binom.sf(year_size // 2, year_size, p)
        rows = [
            cmath(r"P(\text{a christening is a boy})", r"=", rf"p \approx {p:.3f}", r"\quad\text{(the 82-year share)}", font_size=32),
            cmath(r"P(\text{boys win a year of } \approx 11{,}400)", r"=", rf"P\{{\mathrm{{Binomial}}({year_size},p)>{year_size // 2}\}} \approx {py:.5f}",
                  font_size=30),
            cmath(r"P(\text{boys win all 82 years})", r"\approx", rf"{py:.5f}^{{82}} \approx {py ** 82:.2f}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"what the data say: \ about 107 boys for every 100 girls"), why(r"equal-year illustration, independent children and years"),
                why(r"with a 51.6\% coin, \ 82 straight wins are \emph{expected}")]
        foot = fit_rows(VGroup(
            label(r"rejecting $H_0$ does not prove your favourite alternative", font_size=28, color=OBS),
            label(r"Arbuthnot rejected ``a fair coin each year'', \ not ``chance'': \ a biased coin explains it all", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.3, 0])
        intro = label('Rejecting one chance model does not reject chance', font_size=36)
        with self.voiceover(
            "So did Arbuthnot prove Providence? <bookmark mark='a'/> His null was a fair coin each year. But across the "
            "eighty-two years, about fifty-one point six percent of christenings were boys. <bookmark mark='b'/> A "
            "year has about eleven thousand four hundred christenings, so in a simplified equal-year model with independent children, if each child is "
            "a boy with probability point five one six, boys win a given year with probability about point nine nine "
            "nine seven five, approximately. This illustration fixes every year at the average size; it does not fit the full pattern of historical annual counts. "
            "<bookmark mark='c'/> Over eighty-two years, that's a ninety-eight percent chance of a clean sweep. Under "
            "this chance model, what Arbuthnot saw was entirely expected. <bookmark mark='d'/> The lesson is the most "
            "important one in this part: rejecting a null hypothesis doesn't prove the alternative you had in mind. "
            "Arbuthnot rejected one particular chance model, a fair coin, not chance itself."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bernoulli(self):
        h1 = history_card(1712, r"Willem 's Gravesande", r"repeats the argument with a finer statistic, \ the number of boys each year, \ "
                          r"and again finds chance wanting", color=DATA, width=6.0, font_size=22).move_to([-3.3, 0.9, 0])
        h2 = history_card(1713, r"Nicolaus Bernoulli", r"replies that a die with 35 faces, \ 18 marked ``boy'', \ fits the yearly "
                          r"counts well: \ chance, \ with the right model", color=DATA, width=6.0, font_size=22).move_to([3.3, 0.9, 0])
        foot = label(r"the first argument over which null hypothesis to test", font_size=26, color=OBS).to_edge(DOWN, buff=1.0)
        intro = label('Which probability model should explain the births?', font_size=36)
        with self.voiceover(
            "The point was made at the time. <bookmark mark='a'/> In 1712 the Dutch mathematician Willem 's Gravesande "
            "redid the argument with a finer statistic, the number of boys in each year, and still found a fair coin "
            "wanting. <bookmark mark='b'/> But Nicolaus Bernoulli, nephew of Jacob, replied that the yearly counts fit "
            "very well if each birth is like the throw of a die with thirty-five faces, eighteen of them marked boy. "
            "A biased probability model can explain a persistent male excess without Providence; whether it fits the full data is a separate question. <bookmark mark='c'/> It was the first "
            "argument over which null hypothesis to test, and it has never stopped."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def five_percent(self):
        xs = np.linspace(-3.6, 3.6, 300)
        A = axes([-3.6, 3.6], [0, 0.42], x_length=7.6, y_length=3.6, xlabel=r"$z$", xticks=[-3, -1.96, 0, 1.96, 3],
                 center=[-2.0, -0.2, 0])
        ax = A.ax
        cv = curve(ax, xs, stats.norm.pdf(xs), NULLC, 3)
        lt = shade(ax, xs[xs <= -1.96], stats.norm.pdf(xs[xs <= -1.96]), REJ, 0.6)
        rt = shade(ax, xs[xs >= 1.96], stats.norm.pdf(xs[xs >= 1.96]), REJ, 0.6)
        rows = fit_rows(VGroup(
            label(r"Fisher (1925): \ $P = 0.05$, \ or 1 in 20, \ at $1.96$ or nearly 2", font_size=24),
            label(r"``it is convenient to take this point as a limit''", font_size=24, color=GREY_A),
            label(r"a convention for when to look harder, \ not a law", font_size=24, color=OBS),
            label(r"for higher odds, \ 1 in 50 or 1 in 100 (1926)", font_size=22, color=GREY_A),
        ), 5.0, 0.34, [4.4, -0.2, 0])
        with self.voiceover(
            "Where does the famous five percent come from? <bookmark mark='a'/> In his 1925 textbook, Statistical "
            "Methods for Research Workers, Fisher noted that a normal deviate beyond one point nine six, or nearly two "
            "standard deviations, occurs by chance about one time in twenty. <bookmark mark='b'/> It is convenient, he "
            "wrote, to take this point as a limit in judging whether a deviation is to be considered significant. "
            "<bookmark mark='c'/> A convenience, a line at which to start taking a result seriously, not a law of "
            "nature. <bookmark mark='d'/> A year later he added that anyone wanting higher odds could draw the line at one in "
            "fifty, or one in a hundred. How a convenience became a rule is part of the story of the next chapters."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(rt), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()
