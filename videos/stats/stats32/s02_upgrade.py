from __future__ import annotations

from videos.stats.stats32.common import *  # noqa: F403


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.problem()
        self.counting()
        self.plan()

    def card(self):
        card = chapter_card(1, r"Upgrade: \ what Part 19 shrank", r"From a first look to the whole theory", lit=(1996,), part=PART)
        with self.voiceover("Chapter one. An upgrade of Part 19."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        u = upgrade_card(19, r"ridge shrinks every coefficient; \ the lasso sets some to zero by soft thresholding; \ CV picks $\lambda$",
                         r"more observations than variables, \ and that the fitted coefficients were the end of the story",
                         r"$p \gg n$: \ when the lasso finds the truth, \ how to compute and tune it, \ and honest inference after it",
                         width=11.0, font_size=24).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 19 met ridge regression and the lasso. Ridge shrinks every coefficient towards zero; "
            "the lasso shrinks and sets some exactly to zero, by soft thresholding; and cross-validation chooses how much. "
            "<bookmark mark='b'/> It quietly assumed more observations than variables, and it treated the fitted "
            "coefficients as the end of the story. <bookmark mark='c'/> This part drops both assumptions. With far more "
            "variables than observations, when does the lasso find the true variables? How is its whole path computed, and "
            "its penalty chosen? And how can we attach honest confidence intervals to coefficients that were selected by "
            "looking at the data?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(u[0]), FadeIn(u[1][0]), FadeIn(u[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(u[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(u[1][1][2]))
        self.wait(1.0)
        self.clear_scene()

    def problem(self):
        rows = [
            cmath(r"y", r"=", r"X\beta + \varepsilon, \ \ X \in \mathbb R^{n \times p}, \ p > n", font_size=32),
            cmath(r"X^\top X", r":", r"\text{rank} \le n < p: \ \text{singular}", font_size=30),
            cmath(r"X(\hat\beta + v)", r"=", r"X\hat\beta \ \text{for every } v \in \mathrm{null}(X)", font_size=30),
            cmath(r"\|\beta\|_0", r"=", r"s \ll n: \ \text{only } s \text{ coefficients are nonzero}", font_size=30),
        ]
        rows[3][-1].set_color(SPIKE)
        whys = [why(r"more unknowns than equations"), why(r"no unique least-squares fit"),
                why(r"null-space dimension $p-\mathrm{rank}(X)$"), why(r"the assumption that rescues us")]
        with self.voiceover(
            "<bookmark mark='a'/> The problem, precisely. A linear model with more coefficients than observations. "
            "<bookmark mark='b'/> X transpose X has rank at most n, so it is singular and the normal equations have "
            "no unique solution. <bookmark mark='c'/> Add any vector from the null space of X to a solution and the "
            "fit is unchanged: a family with dimension p minus the rank of X; exact interpolation requires the "
            "outcome to lie in its column space, and nothing in the data prefers one to another. <bookmark mark='d'/>"
            " The rescue is an assumption: that only s of the coefficients are nonzero, with s much smaller than n. "
            "Identifying which coefficients matter also needs a suitable design and sufficiently strong signals; "
            "identical columns can prevent unique support identification."
        ) as vo:
            intro=label('An underdetermined regression needs structure for identifiability',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def counting(self):
        rows = [
            cmath(r"\text{unknown support}", r":", r"\binom{p}{s} \ \text{possibilities}", font_size=32),
            cmath(r"\log_2 \binom{p}{s}", r"\approx", r"s \log_2(p/s): \ \text{bits needed to name it}", font_size=30),
            cmath(r"n", r"\gtrsim", r"s \log(p/s): \ \text{enough, \ with the right method}", font_size=30),
            cmath(r"p = 20{,}000, \ s = 10", r":", r"s \log(p/s) \approx 76", font_size=30),
        ]
        rows[2][-1].set_color(SPIKE)
        whys = [why(r"which $s$ of the $p$?"), why(r"an information count"), why(r"chapter nine; \ Part 50's lower bound"),
                why(r"design, noise, signal strength and constants matter")]
        with self.voiceover(
            "<bookmark mark='a'/> A counting argument says how much data that needs. If s of p coefficients are "
            "nonzero, there are p choose s possible supports. <bookmark mark='b'/> Naming one takes about s log of p "
            "over s bits. <bookmark mark='c'/> And the theory of this part shows that, with the right method, the "
            "number of observations needed grows like s log of p over s: linearly in the number of true effects, only"
            " logarithmically in the number of candidates. <bookmark mark='d'/> With twenty thousand genes and ten "
            "that matter, that is about seventy-six: seventy-six is an order-of-magnitude count, not a clinical "
            "sample-size guarantee. Constants, noise, signal strength and design conditions also matter."
        ) as vo:
            intro=label('Sparse recovery sample counts depend on design, signal strength and noise',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def plan(self):
        rows = fit_rows(VGroup(
            label(r"penalize: \ $\min_\beta \ \tfrac1{2n}\|y - X\beta\|^2 + \lambda\, \mathrm{pen}(\beta)$", font_size=26),
            label(r"$\mathrm{pen} = \|\beta\|_2^2$: \ ridge, \ generically dense, without a selection threshold", font_size=26, color=RIDGE),
            label(r"$\mathrm{pen} = \|\beta\|_0$: \ best subset, \ sparse but intractable", font_size=26, color=RES),
            label(r"$\mathrm{pen} = \|\beta\|_1$: \ the lasso, \ sparse and convex", font_size=26, color=LASSO),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Every method in this part adds a penalty to the least-squares loss. <bookmark "
            "mark='b'/> Penalize the squared length of beta and you get ridge regression: stable and generically "
            "dense; individual coordinates can cross zero, but it does not create a selection threshold. <bookmark "
            "mark='c'/> Penalize the number of nonzero coefficients and you get best subset selection: sparse, but "
            "computationally intractable. <bookmark mark='d'/> Penalize the sum of absolute values and you get the "
            "lasso: sparse, and convex. The next three chapters take them in turn."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
