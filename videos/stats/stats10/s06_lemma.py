from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class Lemma(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.dice()
        self.knapsack()
        self.frontier()
        self.proof()
        self.consequences()

    def card(self):
        card = chapter_card(5, r"The Neyman--Pearson lemma", r"The most powerful test is a knapsack", lit=(1933,), part=PART)
        with self.voiceover("Chapter five. The Neyman–Pearson lemma."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        tc = theorem_card(r"Neyman--Pearson lemma", r"To test $H_0: X \sim p_0$ against $H_1: X \sim p_1$ (both simple), \ the test that "
                          r"rejects when \ $\displaystyle \frac{p_1(x)}{p_0(x)} > k$ \ (randomizing when it equals $k$) \ is the most "
                          r"powerful test of its size.", who=r"J. Neyman \& E. S. Pearson (1933)", color=ALTC, width=10.4,
                          font_size=26).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"rank the possible outcomes by how much more likely they are under $H_1$ than under $H_0$", font_size=26),
            label(r"reject for the top of the ranking, \ until the size budget $\alpha$ is spent", font_size=26, color=OBS),
        ), 12.6, 0.34, [0, -1.9, 0])
        intro = label('Spend a size budget to maximize power', font_size=36)
        with self.voiceover(
            "Which test is the most powerful? For the simplest case, one null distribution against one alternative, "
            "Neyman and Pearson answered completely. <bookmark mark='a'/> Reject when the likelihood ratio, the "
            "probability of the data under the alternative divided by its probability under the null, exceeds a "
            "constant. No test of the same size has more power. <bookmark mark='b'/> In words: rank every possible "
            "outcome by how much more likely it is under the alternative than under the null. <bookmark mark='c'/> "
            "Then reject for outcomes from the top of the ranking down, until you've spent your budget of false-alarm "
            "probability. It's a fractional knapsack problem when boundary randomization is allowed, and the likelihood ratio is value per unit weight. A greedy rule need not solve an arbitrary non-randomized knapsack."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def dice(self):
        d = load("knapsack")
        sums, p0, p1 = np.asarray(d["sums"]), np.asarray(d["p0"]), np.asarray(d["p1"])
        A = axes([1.5, 12.5], [0, 0.2], x_length=7.4, y_length=3.6, xlabel=r"the sum of two dice", ylabel=r"probability",
                 xticks=list(range(2, 13)), yticks=[0, 0.1, 0.2], center=[-2.2, 0.0, 0])
        ax = A.ax
        b0 = bars_at(ax, sums - 0.18, p0, 0.34, NULLC, opacity=0.8)
        b1 = bars_at(ax, sums + 0.18, p1, 0.34, ALTC, opacity=0.8)
        leg = legend([(NULLC, r"$H_0$: \ two fair dice"), (ALTC, r"$H_1$: \ the second die rolls a six $\tfrac13$ of the time")],
                     font_size=22).to_edge(UP, buff=0.3)
        lr = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=OBS).next_to(ax.c2p(s_, 0), DOWN, buff=1.05) for s_, v in zip(sums, d["lr"])])
        lrl = label(r"$p_1/p_0$", font_size=22, color=OBS).next_to(lr[0], LEFT, buff=0.3)
        rows = fit_rows(VGroup(
            label(r"you see only the sum; \ is the second die loaded?", font_size=24),
            label(r"each sum: \ a weight $p_0$, \ which costs size,", font_size=24, color=GREY_A),
            label(r"and a value $p_1$, \ which buys power", font_size=24, color=GREY_A),
            label(r"sums 2 to 6: \ \emph{less} likely under $H_1$;", font_size=24, color=OBS),
            label(r"12: \ twice as likely", font_size=24, color=OBS),
        ), 5.0, 0.34, [4.4, -0.4, 0])
        intro = label('Fair dice or one loaded die?', font_size=36)
        with self.voiceover(
            "A concrete example. <bookmark mark='a'/> Someone rolls two dice and tells you only the sum. Under the "
            "null, both dice are fair. Under the alternative, the second die is loaded, coming up six a third of the "
            "time. <bookmark mark='b'/> Here are the two distributions of the sum: grey for the null, green for the "
            "alternative. <bookmark mark='c'/> Under each sum, the likelihood ratio. Sums from two to six are a little "
            "less likely under the alternative; twelve is twice as likely. <bookmark mark='d'/> Think of each possible "
            "sum as an item you might put in your rejection region. Its weight is its null probability, which spends "
            "your size budget, and its value is its alternative probability, which buys power."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), FadeIn(leg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b0, lag_ratio=0.05), FadeIn(b1, lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(lr), FadeIn(lrl), FadeIn(rows[3:]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1:3]))
        self.clear_scene()

    def knapsack(self):
        d = load("knapsack")
        sums, p0, p1, order = np.asarray(d["sums"]), np.asarray(d["p0"]), np.asarray(d["p1"]), list(d["order"])
        # the budget bar: alpha = 1/6, drawn as a bar 6 units wide for probability 1
        X0, W, Y = -5.6, 11.2, 1.2
        frame = Rectangle(width=W / 6, height=0.6, stroke_color=REJ, stroke_width=3).move_to([X0 + W / 12, Y, 0])
        budget_l = label(r"size budget \ $\alpha = \tfrac16$", font_size=22, color=REJ).next_to(frame, UP, buff=0.15)
        pow_frame = Rectangle(width=W, height=0.6, stroke_color=GREY_D, stroke_width=1.5).move_to([X0 + W / 2, -0.6, 0])
        pow_l = label(r"power: \ the $p_1$ collected", font_size=22, color=ALTC).next_to(pow_frame, UP, buff=0.15).align_to(pow_frame, LEFT)
        items, vals = VGroup(), VGroup()
        x_cost, x_val = X0, X0
        for i in order[:3]:
            w = p0[i] * W
            v = p1[i] * W
            items.add(VGroup(Rectangle(width=w, height=0.6, stroke_width=1, stroke_color=BLACK, fill_color=NULLC, fill_opacity=0.85)
                             .move_to([x_cost + w / 2, Y, 0]),
                             MathTex(str(sums[i]), font_size=22, color=BLACK).move_to([x_cost + w / 2, Y, 0])))
            vals.add(Rectangle(width=v, height=0.6, stroke_width=1, stroke_color=BLACK, fill_color=ALTC, fill_opacity=0.85)
                     .move_to([x_val + v / 2, -0.6, 0]))
            x_cost += w
            x_val += v
        rows = fit_rows(VGroup(
            label(r"greedy by $p_1/p_0$: \ 12 (2.0), \ then 11 (1.4), \ then 10 (1.2)", font_size=26),
            MathTex(rf"\text{{size}} = \tfrac{{1}}{{36}} + \tfrac{{2}}{{36}} + \tfrac{{3}}{{36}} = \tfrac16,\qquad \text{{power}} = {d['best_power']:.3f}",
                    font_size=30, color=OBS),
            label(r"brute force over all $2^{11} = 2{,}048$ possible rejection regions: \ none of size $\le \tfrac16$ does better",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.32, [0, -2.4, 0])
        intro = label('Choose outcomes by their likelihood ratio', font_size=36)
        with self.voiceover(
            "Now fill the knapsack. <bookmark mark='a'/> The budget is a size of one sixth. <bookmark mark='b'/> The best "
            "value for weight is a sum of twelve, with likelihood ratio two: it costs one thirty-sixth of size and buys "
            "two thirty-sixths of power. <bookmark mark='c'/> Next, eleven, with ratio one point four. "
            "<bookmark mark='d'/> Then ten, at one point two. That exactly spends the budget: size one sixth, and power "
            "point two three three. <bookmark mark='e'/> Is this really the best? There are only two thousand and "
            "forty-eight possible rejection regions, every subset of the eleven sums, so we can check them all. None with "
            "size at most one sixth has more power. Notice how weak even the best test is: with a single roll, the "
            "evidence is thin."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Create(frame), FadeIn(budget_l), Create(pow_frame), FadeIn(pow_l))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(items[k], shift=DOWN * 0.2), GrowFromEdge(vals[k], LEFT))
            self.play(FadeIn(rows[:2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def frontier(self):
        d = load("knapsack")
        size, power = np.asarray(d["size"]), np.asarray(d["power"])
        A = axes([0, 1], [0, 1], x_length=5.4, y_length=5.4, xlabel=r"size $\alpha$", ylabel=r"power", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 0.5, 1], center=[-2.6, -0.2, 0])
        ax = A.ax
        cloud = VGroup(*[Dot(ax.c2p(a, b), radius=0.018, color=NULLC, fill_opacity=0.6) for a, b in zip(size, power)])
        fr = np.asarray(d["front"])
        front = polyline(ax, fr[:, 0], fr[:, 1], OBS, 3.5)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        best = Dot(ax.c2p(d["best_size"], d["best_power"]), radius=0.08, color=REJ)
        rows = fit_rows(VGroup(
            label(r"each dot: \ one of the 2,048 rejection regions", font_size=24, color=GREY_A),
            label(r"the likelihood-ratio regions trace the upper edge", font_size=26, color=OBS),
            label(r"the diagonal: \ tests no better than a coin with bias $\alpha$", font_size=24, color=GREY_A),
            label(r"randomizing between corners fills in the edge \ (the lemma's tie-breaking)", font_size=22, color=GREY_A),
        ), 5.6, 0.36, [3.9, -0.2, 0])
        with self.voiceover(
            "Here are all two thousand and forty-eight regions at once. <bookmark mark='a'/> Each dot is a possible "
            "test, placed by its size and its power. <bookmark mark='b'/> The orange line joins the regions the "
            "likelihood ratio builds, adding sums in order of their ratio. Every dot lies on or below it. Whatever size "
            "you're willing to accept, the likelihood ratio test sits on the frontier. <bookmark mark='c'/> The dashed "
            "diagonal is what you'd get by ignoring the data and rejecting at random with probability alpha. "
            "<bookmark mark='d'/> Between the corners of the frontier, a test can reach the edge by randomizing, which is "
            "what the lemma's clause about ties is for."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(cloud, lag_ratio=0.0005), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(front), FadeIn(best), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\phi(x)", r"=", r"\mathbf 1\{p_1 > k p_0\} + \gamma\mathbf 1\{p_1 = k p_0\},\quad \phi' \text{ any test with } E_0\phi' \le E_0\phi", font_size=30),
            cmath(r"\big(\phi(x) - \phi'(x)\big)\big(p_1(x) - k\,p_0(x)\big)", r"\ge", r"0 \quad \text{for every } x", font_size=30),
            cmath(r"\sum_x \big(\phi - \phi'\big)\big(p_1 - k\,p_0\big)", r"\ge", r"0", font_size=30),
            cmath(r"E_1\phi - E_1\phi'", r"\ge", r"k\,\big(E_0\phi - E_0\phi'\big) \ge 0", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the likelihood-ratio test, \ and any rival of no larger size"),
                why(r"where $\phi = 1$, \ both factors $\ge 0$; \ where $\phi = 0$, \ both $\le 0$"), why(r"add up over outcomes"),
                why(r"rearrange: \ more power than any rival")]
        intro = label('Why a likelihood-ratio rule wins', font_size=36)
        with self.voiceover(
            "The proof is three lines. <bookmark mark='a'/> Let phi be the likelihood ratio test, and phi prime any rival "
            "whose size is no larger. <bookmark mark='b'/> At every outcome, the product of phi minus phi prime and p1 "
            "minus k p0 is at least zero. Where phi rejects, p1 exceeds k p0 and phi minus phi prime can't be negative. "
            "Where phi accepts, both factors are at most zero. <bookmark mark='c'/> Sum over all outcomes. "
            "<bookmark mark='d'/> The power difference is at least k times the size difference, which is at least zero. "
            "The likelihood ratio test wins."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def consequences(self):
        rows = [
            cmath(r"\frac{p_\delta(x)}{p_0(x)}", r"=", r"\exp\Big(\frac{n\delta\bar x}{\sigma^2} - \frac{n\delta^2}{2\sigma^2}\Big)", font_size=34),
            cmath(r"\text{reject when}", r"\ ", r"\bar x > c \quad \text{whatever } \delta > 0", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"normal mean, \ $\sigma$ known: \ increasing in $\bar x$"), why(r"the same test for every $\delta > 0$: \ \emph{uniformly} most powerful")]
        foot = fit_rows(VGroup(
            label(r"monotone likelihood ratio gives a UMP one-sided test (Karlin \& Rubin, 1956)", font_size=24),
            label(r"two-sided normal mean: \ no UMP test exists; \ we settle for unbiased tests, \ or the likelihood ratio of ch.~6", font_size=24,
                  color=GREY_A),
            label(r"composite hypotheses in general: \ Part 46", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.0, 0])
        intro = label('A most powerful one-sided normal-mean test', font_size=36)
        with self.voiceover(
            "What does the lemma say about everyday tests? <bookmark mark='a'/> For a normal mean with known sigma, the "
            "likelihood ratio between a positive delta and zero is an increasing function of x-bar. <bookmark mark='b'/> "
            "So the most powerful test rejects for large x-bar, and it's the same test whatever positive delta we had "
            "in mind. It's uniformly most powerful against all one-sided alternatives: the z-test is optimal. "
            "<bookmark mark='c'/> Samuel Karlin and Herman Rubin showed in 1956 that this happens whenever the "
            "likelihood ratio is monotone in a statistic. <bookmark mark='d'/> For this normal-mean model with two-sided alternatives no uniformly "
            "most powerful test exists, since the best test against positive deltas is the worst against negative ones. "
            "<bookmark mark='e'/> Part 46 develops the general theory."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k], shift=RIGHT * 0.2))
        self.clear_scene()
