from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Decision(VoiceoverScene):
    def construct(self):
        self.card()
        self.wald()
        self.language()
        self.binomial()
        self.criteria()
        self.region()
        self.uniform()

    def card(self):
        card = chapter_card(1, r"Decision theory", r"Estimation as a game against nature", lit=(1950,), part=PART)
        with self.voiceover("Chapter one. Decision theory: estimation as a game against nature."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def wald(self):
        rows = fit_rows(VGroup(
            label(r"1928, \ 1944: \ von Neumann (and Morgenstern): \ the theory of games", font_size=26, color=GREY_A),
            label(r"1939: \ Abraham Wald: \ estimation and testing as one problem, \ a choice under uncertainty", font_size=26),
            label(r"1950: \ \emph{Statistical Decision Functions}", font_size=26, color=S.ACCENT),
            label(r"nature picks $\theta$; \ the statistician picks a rule $\delta$; \ the loss is scored on average", font_size=26, color=MMC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> John von Neumann's theory of games, from 1928 and his 1944 book with Oskar Morgenstern, "
            "studied two players choosing strategies against each other. <bookmark mark='b'/> In 1939 Abraham Wald saw that "
            "estimation and testing are one problem of this kind: choosing an action when the state of the world is "
            "unknown. <bookmark mark='c'/> His book Statistical Decision Functions appeared in 1950, the year he died in a "
            "plane crash in India. <bookmark mark='d'/> In Wald's game, nature picks the parameter, the statistician picks a "
            "rule for turning data into an action, and the loss is scored on average over the data."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def language(self):
        rows = [
            cmath(r"L(\theta, a)", r":", r"\text{the loss of action } a \text{ when the truth is } \theta", font_size=34),
            cmath(r"\delta", r":", r"\mathcal X \to \mathcal A, \ \text{a decision rule}", font_size=34),
            cmath(r"R(\theta, \delta)", r"=", r"E_\theta\, L(\theta, \delta(X)): \ \text{the risk function}", font_size=34),
            cmath(r"\delta \text{ inadmissible}", r":", r"\exists\, \delta': \ R(\theta, \delta') \le R(\theta, \delta)\ \forall \theta, \ < \text{ for some}", font_size=30),
        ]
        rows[2][-1].set_color(MMC)
        rows[3][-1].set_color(INADC)
        whys = [why(r"e.g.\ $(a - \theta)^2$"), why(r"an estimator, \ or a test"), why(r"one curve per rule"), why(r"dominated")]
        with self.voiceover(
            "<bookmark mark='a'/> The ingredients. A loss function scores each action against each possible truth; "
            "for estimation, usually the squared error. <bookmark mark='b'/> A decision rule maps every possible data"
            " set to an action: an estimator, or a test. <bookmark mark='c'/> Its risk function is the expected loss "
            "when the truth is theta: a whole curve, one value for each theta, not a single number. <bookmark "
            "mark='d'/> A rule is inadmissible if another rule's risk is never larger and somewhere smaller. Under "
            "the specified model, loss and permitted actions, a dominating rule has no larger risk; Stein's theorem "
            "says that the sample means are one."
        ) as vo:
            heading=label('Risk scores a rule under a specified model and loss',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def binomial(self):
        d = load("binomial")
        p = np.asarray(d["p"])
        A = axes([0, 1], [0, 0.018], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"risk $E(\hat p - p)^2$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.005, 0.01, 0.015], center=[-2.5, 0.2, 0])
        ax = A.ax
        mle = polyline(ax, p, d["mle"], MLEC, 4)
        bay = polyline(ax, p, d["bayes11"], BAYESC, 4)
        mm = polyline(ax, p, d["minimax"], MMC, 4)
        side = fit_rows(VGroup(
            label(rf"$X \sim \mathrm{{Bin}}({d['n']}, p)$, \ squared error", font_size=22),
            label(r"blue: \ $X/n$, \ risk $p(1 - p)/n$", font_size=22, color=MLEC),
            label(r"orange: \ $(X + 1)/(n + 2)$, \ Laplace's rule", font_size=22, color=BAYESC),
            label(r"gold: \ $(X + \sqrt n/2)/(n + \sqrt n)$: \ flat", font_size=22, color=MMC),
            label(r"the curves cross: \ no rule is best at every $p$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A first example: estimate a proportion p from sixteen trials, with squared error loss. "
            f"<bookmark mark='b'/> The sample proportion, X over n, has risk p times one minus p over n: zero at the ends, "
            f"largest in the middle. <bookmark mark='c'/> Laplace's rule of succession, X plus one over n plus two, pulls "
            f"toward a half: better in the middle, worse near the ends. <bookmark mark='d'/> And a stranger rule, X plus "
            f"root n over two, over n plus root n, has exactly the same risk at every p: a flat line at "
            f"{say(d['max_minimax'], 2)}. <bookmark mark='e'/> The curves cross. No rule is best at every p, so we need a "
            f"way to summarize a risk curve by a single number."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact risk functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mle), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(bay), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def criteria(self):
        d = load("binomial")
        rows = [
            cmath(r"\text{minimax}", r":", r"\min_\delta \max_\theta R(\theta, \delta): \ \text{guard against the worst } \theta", font_size=32),
            cmath(r"\text{Bayes}", r":", r"\min_\delta \textstyle\int R(\theta, \delta)\, \pi(d\theta): \ \text{average over a prior}", font_size=32),
            cmath(r"\text{max risk}", r":", rf"X/n \ {d['max_mle']:.4f}; \ \ \text{{flat rule}} \ {d['max_minimax']:.4f}", font_size=32),
            cmath(r"\text{Bayes risk, uniform}", r":", rf"X/n \ {d['bayes_mle']:.4f}; \ \text{{Laplace}} \ {d['bayes_11']:.4f}; \ \text{{flat}} \ {d['bayes_minimax']:.4f}", font_size=30),
        ]
        rows[0][-1].set_color(MMC)
        rows[1][-1].set_color(BAYESC)
        whys = [why(r"the pessimist"), why(r"the posterior mean, \ for squared error"), why(r"the flat rule is minimax"), why(r"Laplace's is Bayes")]
        with self.voiceover(
            f"<bookmark mark='a'/> Two summaries dominate the theory. The minimax criterion judges a rule by its worst risk "
            f"and picks the rule whose worst case is best. <bookmark mark='b'/> The Bayes criterion averages the risk over "
            f"a prior distribution for theta; for squared error the minimizer is the posterior mean. <bookmark mark='c'/> "
            f"The sample proportion's worst risk is one over four n, {say(d['max_mle'], 4)}; the flat rule's is "
            f"{say(d['max_minimax'], 2)}, and it is the minimax rule. <bookmark mark='d'/> Averaged over a uniform prior, "
            f"Laplace's rule does best, as it must: it is the posterior mean under that prior. The flat rule is itself "
            f"Bayes, for a Beta prior with both parameters equal to root n over two."
        ) as vo:
            heading=label('Minimax and Bayes summarize risk differently',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def region(self):
        d = load("binomial")
        r = d["region"]
        tab = table_rows([[r"$n$", r"the flat rule beats $X/n$ when", r"its constant risk", r"max risk of $X/n$"]] +
                         [[f"{int(n):,}", rf"${r[n][0]:.3f} < p < {r[n][1]:.3f}$", f"{1 / (4 * (1 + int(n) ** 0.5) ** 2):.5f}", f"{1 / (4 * int(n)):.5f}"]
                          for n in ("16", "100", "1000")], font_size=28, col_buff=0.8, row_buff=0.3,
                         colors=[GREY_A, None, None, None]).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"as $n$ grows, \ the minimax rule wins on a shrinking interval around $\tfrac12$", font_size=26, color=MMC),
            label(r"and loses, \ by a ratio tending to $\infty$, \ near $p = 0$ and $p = 1$", font_size=26, color=INADC),
            label(r"minimax protects against a worst case \ that may be implausible", font_size=26, color=S.ACCENT),
        ), 12.4, 0.4, [0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> But look at where the minimax rule wins. With sixteen trials, it beats the sample proportion between {say(r['16'][0], 1)} and {say(r['16'][1], 1)}. With a hundred, only between {say(r['100'][0], 2)} and {say(r['100'][1], 2)}; with a thousand, between {say(r['1000'][0], 2)} and {say(r['1000'][1], 2)}. <bookmark mark='b'/> For each fixed sample size, its risk ratio diverges as p tends to zero or one, because its risk never falls below its constant. <bookmark mark='c'/> Minimax buys protection against the worst value of p, which may be a value nobody believes. That tension, between guarding the worst case and doing well on average, runs through the whole subject."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tab[1:]], lag_ratio=0.4), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def uniform(self):
        rows = [
            cmath(r"\delta^* \text{ uniformly best}", r":", r"R(\theta, \delta^*) \le R(\theta, \delta)\ \forall \theta, \delta", font_size=32),
            cmath(r"\delta_{\theta_0}(X) \equiv \theta_0", r":", r"R(\theta_0, \delta_{\theta_0}) = 0", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"R(\theta, \delta^*) = 0 \ \text{for every } \theta: \ \text{impossible}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{restrict the rules } (\text{unbiased, equivariant}) \text{ or summarize the risk}", font_size=30),
        ]
        rows[2][-1].set_color(INADC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"the hope"), why(r"the stopped clock"), why(r"unless the data are perfect"), why(r"the two escapes")]
        with self.voiceover(
            "<bookmark mark='a'/> Why not simply ask for the rule that is best at every theta? <bookmark mark='b'/> Because "
            "of the stopped clock: the rule that ignores the data and always answers theta nought has zero risk at theta "
            "nought. <bookmark mark='c'/> A uniformly best rule would have to match it, so it would need zero risk at every "
            "theta, which is impossible unless the data reveal theta exactly. <bookmark mark='d'/> There are two ways out, "
            "and this part takes both: restrict the competition to a natural class, such as unbiased or equivariant rules, "
            "and find the best there; or summarize each risk curve by its maximum or its average."
        ) as vo:
            heading=label('A uniformly best rule would need perfect identification',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
