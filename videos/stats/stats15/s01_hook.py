from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.essay()
        self.table()
        self.posterior()
        self.laplace()
        self.sunrise()
        self.objectives()

    def essay(self):
        tl = timeline(lit=(1763,)).to_edge(UP, buff=0.35)
        hc = history_card(1763, r"Thomas Bayes \ (d.~1761), \ communicated by Richard Price",
                          r"``An Essay towards solving a Problem in the Doctrine of Chances'', \ \emph{Philosophical Transactions}: \ "
                          r"given how often an event has happened and failed, \ the chance that its probability lies between any two "
                          r"limits", color=PRIOR, width=10.4, font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a Presbyterian minister in Tunbridge Wells, \ and an amateur mathematician", font_size=24),
            label(r"the essay was found among his papers, \ and published two years after his death", font_size=24, color=GREY_A),
            label(r"the problem is the reverse of Part 2's: \ from the data back to the probability", font_size=26, color=POST),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1763 the Royal Society published an essay by Thomas Bayes, a Presbyterian minister in "
            "Tunbridge Wells who had died two years earlier. His friend Richard Price had found it among his papers. Its "
            "problem: given the number of times an unknown event has happened and failed, find the chance that its probability "
            "lies between any two limits. <bookmark mark='b'/> Bayes was an amateur mathematician, a Fellow of the Royal "
            "Society, who published almost nothing in his lifetime. <bookmark mark='c'/> His question runs the other way from "
            "everything in Part 2. There we knew the probability and asked about the data. Here we have the data, and ask what "
            "to believe about the probability."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("billiard")
        t = BilliardTable(width=6.4, height=4.2, center=[-2.8, 0.2, 0])
        u0 = d["u0"]
        w, wa = t.roll(u0, 0.62, color=S.TRUTH, radius=0.12)
        line = t.line(u0)
        balls = np.asarray(d["balls"])
        left = np.asarray(d["left"], bool)
        rolls = [t.roll(u, v, color=S.LIK if l_ else GREY_B) for (u, v), l_ in zip(balls, left)]
        rows = fit_rows(VGroup(
            label(r"uniform prior on W; \ one illustrative hidden position", font_size=26, color=S.TRUTH),
            label(r"its position $p$ is hidden", font_size=26),
            label(r"12 more balls: \ left or right of W?", font_size=26),
            label(rf"left of W: \ {int(left.sum())} of 12", font_size=26, color=S.LIK),
            label(r"where is W?", font_size=26, color=POST),
        ), 4.8, 0.36, [4.4, 0.2, 0])
        with self.voiceover(
            "Bayes made the problem concrete with a table. <bookmark mark='a'/> Model a ball W as equally likely to stop anywhere on the table. The drawing uses one fixed illustrative hidden position. <bookmark mark='b'/> Its position from the left edge, as a fraction of the "
            "table's width, is p, and we aren't allowed to see it. <bookmark mark='c'/> Now roll twelve more balls, and for each "
            "one we're told only whether it stopped to the left or the right of W. Each ball lands left with probability p. "
            "<bookmark mark='d'/> Eight of the twelve land to the left. <bookmark mark='e'/> What should we believe about where "
            "W is?"
        ) as vo:
            self.play(FadeIn(t))
            vo.wait_until("a")
            self.add(w)
            self.play(wa, FadeIn(rows[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]))
            self.play(w.animate.set_opacity(0.25), line.animate.set_opacity(0.25))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            for ball, anim in rolls:
                self.add(ball)
                self.play(anim, run_time=0.45)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def posterior(self):
        d = load("billiard")
        a, b = d["post"][-1]
        A = axes([0, 1], [0, 3.6], x_length=7.4, y_length=4.2, xlabel=r"W's position $p$", ylabel=r"belief (density)", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 1, 2, 3], center=[-2.2, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0, 1, 301)
        flat = density(ax, xs, np.ones_like(xs), PRIOR)
        post = density(ax, xs, stats.beta(a, b).pdf(xs), POST)
        truth = DashedLine(ax.c2p(d["u0"], 0), ax.c2p(d["u0"], 3.4), color=S.TRUTH, stroke_width=3)
        lo, hi = d["ci"]
        rows = fit_rows(VGroup(
            label(r"before: \ every position equally likely", font_size=24, color=PRIOR),
            MathTex(r"\text{after: }\ \pi(p \mid 8 \text{ of } 12) \propto p^{8}(1 - p)^{4}", font_size=28, color=POST),
            MathTex(rf"\text{{Beta}}({a}, {b}):\ \text{{mean}}\ {d['mean']:.2f}", font_size=28, color=POST),
            MathTex(rf"95\%:\ [{lo:.2f},\ {hi:.2f}]", font_size=28, color=POST),
            label(rf"the hidden ball was at {d['u0']:.2f}", font_size=24, color=S.TRUTH),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Before the twelve balls, every position for W was equally likely: a flat line. "
            "<bookmark mark='b'/> Bayes showed that afterwards our belief should be proportional to p to the eighth times one "
            "minus p to the fourth: the chance of exactly what we saw, if W were at p. <bookmark mark='c'/> Normalized, it's a "
            "beta distribution, Part 3's, with parameters nine and five, centred near point six four. <bookmark mark='d'/> It "
            "puts ninety-five percent of its weight between point three nine and point eight six. <bookmark mark='e'/> The "
            "hidden ball was at point six two. That curve illustrates Bayes's early posterior calculation."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(flat), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(flat, post), FadeIn(rows[1]), run_time=2.0)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                if k == 2:
                    self.play(Create(truth))
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def laplace(self):
        d = load("laplace")
        pb = museum.PARIS_BIRTHS
        hc = history_card(1774, r"Pierre-Simon Laplace", r"discovers the same idea independently, \ and makes it a tool: \ "
                          r"``the probability of causes from events''", color=S.ALT, width=9.6, font_size=22).move_to([0, 2.1, 0])
        rows = [
            cmath(r"\text{Paris, 1745--1770}", r":", rf"{pb['boys']:,}\ \text{{boys}},\ \ {pb['girls']:,}\ \text{{girls}}", font_size=30),
            cmath(r"\pi(p \mid \text{data})", r"=", rf"\text{{Beta}}({d['a']:,},\ {d['b']:,})", font_size=30),
            cmath(r"P(p \le \tfrac12 \mid \text{data})", r"\approx", r"1.15 \times 10^{-42}", font_size=32),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"baptisms recorded in the city"), why(r"a uniform prior on $p$, \ the chance of a boy"),
                why(r"``as certain as any moral truth''")]
        with self.voiceover(
            "<bookmark mark='a'/> Eleven years later, Pierre-Simon Laplace found the same idea independently, and turned it into "
            "a working method for science. His most famous application was to births. <bookmark mark='b'/> In Paris from 1745 to "
            "1770 there were two hundred and fifty-one thousand, five hundred and twenty-seven boys baptized, and two hundred "
            "and forty-one thousand, nine hundred and forty-five girls. <bookmark mark='c'/> With a uniform prior on the chance "
            "of a boy, the posterior is a beta distribution with these enormous parameters. <bookmark mark='d'/> The posterior "
            "probability that boys are no more likely than girls is about one in ten to the forty-two. Laplace concluded that "
            "the excess of boys was as certain as any truth of the moral sciences. Part 10's Arbuthnot reached a similar "
            "conclusion with a significance test; Laplace stated it as a probability about the hypothesis itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=3, top=0.9, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sunrise(self):
        d = load("laplace")
        rows = [
            cmath(r"P(\text{success next} \mid s \text{ of } n)", r"=", r"\int_0^1 p\,\pi(p \mid s, n)\,dp = \frac{s + 1}{n + 2}", font_size=32),
            cmath(r"\text{the sun, \ 5{,}000 years}", r":", rf"n = s = {d['days']:,}\ \text{{days}}", font_size=30),
            cmath(r"P(\text{it rises tomorrow})", r"=", r"\frac{1{,}826{,}214}{1{,}826{,}215}", font_size=32),
            cmath(r"\text{Laplace}", r":", r"\text{far greater, \ for one who knows the mechanism}", font_size=30),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"Laplace's rule of succession"), why(r"his example, \ in the \emph{Essai philosophique} (1814)"),
                why(r"odds of 1,826,214 to 1"), why(r"the prior matters when it encodes real knowledge")]
        with self.voiceover(
            "<bookmark mark='a'/> Laplace also asked how likely the next trial is to succeed, after s successes in n. Average "
            "the chance p over the posterior, and the answer is s plus one over n plus two: the rule of succession, under a uniform prior and conditionally independent Bernoulli trials with a common probability. "
            "<bookmark mark='b'/> His notorious example is the sunrise. Suppose the sun has risen every day for five thousand "
            "years, one million, eight hundred and twenty-six thousand, two hundred and thirteen days. <bookmark mark='c'/> "
            "The rule gives odds of one million, eight hundred and twenty-six thousand, two hundred and fourteen to one that it "
            "rises tomorrow. <bookmark mark='d'/> Laplace added at once that the probability is far greater for anyone who "
            "understands what makes the sun rise. A uniform prior is a specific assumption on this scale. The rule also assumes conditionally independent trials with one stable probability; physical knowledge belongs in "
            "the prior. That tension runs through this whole part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 15", font_size=34, color=GREY_B), label(r"First Bayes", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"prior $\times$ likelihood $\propto$ posterior; \ updating one observation at a time",
            r"conjugate families: \ beta--binomial, \ gamma--Poisson, \ normal--normal",
            r"summaries, \ credible and HPD intervals, \ predictive distributions",
            r"choosing priors, \ and checking how much they matter; \ the normal model and Student's $t$",
            r"grids and a Metropolis walk; \ credible intervals on the Coverage Board; \ Bayes factors",
        ], color=POST, font_size=26)
        prereq = note(r"prerequisites: \ Parts 9 and 11").to_corner(DL, buff=0.3)
        built = note(r"built: \ the billiard table; \ \texttt{statkit.bayes}").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifteen: first Bayes. <bookmark mark='b'/> We'll build the machinery, prior times "
            "likelihood proportional to posterior; meet the conjugate families that make it algebra; summarize posteriors "
            "with credible intervals, and predict new data; face the choice of prior honestly; recover Student's t as a "
            "posterior; compute posteriors on grids, and with a Metropolis walk when grids fail; test credible intervals on "
            "the Coverage Board; and take a first look at Bayesian hypothesis testing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
