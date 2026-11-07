from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


def tex_sci(v: float) -> str:
    m, e = f"{v:.1e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


_NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def say_sci(v: float) -> str:
    m, e = f"{v:.1e}".split("e")
    a, b = m.split(".")
    return f"{_NUM[int(a)]} point {_NUM[int(b)]} times ten to the minus {_NUM[-int(e)] if -int(e) < 10 else -int(e)}"


class SubGaussian(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.norms()
        self.hoeffding()
        self.chart()
        self.rare()

    def card(self):
        card = chapter_card(1, r"Sub-Gaussian and sub-exponential variables", r"Tails you can count on, \ at every $n$", part=PART)
        with self.voiceover("Chapter one. Sub-Gaussian and sub-exponential variables: tails you can count on, at every n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"\|X\|_{\psi_2}", r"=", r"\inf\{t > 0 : E\, e^{X^2/t^2} \le 2\}: \ \text{sub-Gaussian}", font_size=34),
            cmath(r"EX=0,\ \|X\|_{\psi_2} \lesssim K", r"\Longleftrightarrow_{\text{up to constants}}", r"P(|X| > t) \le 2 e^{-t^2/K^2} \ \Longleftrightarrow_{\text{up to constants}} \ E e^{\lambda X} \le e^{\lambda^2 K^2}", font_size=30),
            cmath(r"\|X\|_{\psi_1}", r"=", r"\inf\{t : E\, e^{|X|/t} \le 2\}: \ \text{sub-exponential, \ tails } e^{-t/K}", font_size=32),
            cmath(r"\|XY\|_{\psi_1}", r"\le", r"\|X\|_{\psi_2}\|Y\|_{\psi_2}: \ \text{squares of sub-Gaussians are sub-exponential}", font_size=30),
        ]
        rows[0][-1].set_color(GAUSSC)
        rows[2][-1].set_color(MATC)
        whys = [why(r"an Orlicz norm"), why(r"three equivalent views, \ up to constants"), why(r"heavier, \ but still light"), why(r"why $\chi^2$ is sub-exponential")]
        heading = label('Tail, norm and centered MGF conditions agree up to constants', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The workhorse of the subject is a norm that measures how heavy a tail is. The psi-two norm of a random variable is the smallest t such that the expectation of e to the X squared over t squared is at most two. Variables with a finite psi-two norm are called sub-Gaussian. <bookmark mark='b'/> Up to universal constants, three statements are equivalent: the norm is at most K, the tails fall like e to the minus t squared over K squared, and, after centering, the moment generating function is bounded by that of a normal with variance a universal constant times K squared. <bookmark mark='c'/> With the absolute value in place of the square we get the psi-one norm and sub-exponential variables, whose tails fall like e to the minus t over K. <bookmark mark='d'/> And the product of two sub-Gaussians is sub-exponential, which is why a chi-square variable, a sum of squared normals, has sub-exponential rather than Gaussian tails."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def norms(self):
        d = load("orlicz")
        nm = {"normal": r"$N(0,1)$", "rademacher": r"$\pm 1$ signs", "uniform": r"uniform, \ variance 1", "laplace": r"Laplace, \ variance 1", "exponential": r"Exp(1) $- 1$"}
        rows = [[r"law", r"$\|X\|_{\psi_2}$", r"$\|X\|_{\psi_1}$", r"type"]]
        for r in d["rows"]:
            rows.append([nm[r["law"]], f"{r['psi2']:.3f}" if r["psi2"] else r"$\infty$", f"{r['psi1']:.3f}",
                         r"sub-Gaussian" if r["psi2"] else r"sub-exponential"])
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.36, colors=[GREY_B, GAUSSC, GAUSSC, GAUSSC, MATC, MATC])
        tab.move_to([0, 0.8, 0])
        foot = label(rf"exact: \ $\|N(0,1)\|_{{\psi_2}} = \sqrt{{8/3}} = {d['normal_psi2']:.3f}$; \ signs: \ $1/\sqrt{{\log 2}} = {d['rad_psi2']:.3f}$", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"empirical norms from 200,000 draws; \ the Laplace and exponential have no $\psi_2$ norm", font_size=24, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Some values, estimated from two hundred thousand draws and checked against exact formulas. "
            f"The standard normal has psi-two norm root eight thirds, about {say(d['normal_psi2'], 2)}; a random sign has one "
            f"over root log two, about {say(d['rad_psi2'], 2)}; the uniform with variance one lies between. <bookmark "
            f"mark='b'/> The Laplace and the centred exponential have exponential tails: their psi-two norm is infinite, but "
            f"their psi-one norm is finite. Bounded variables are always sub-Gaussian; heavy-tailed ones, like the t, are "
            f"neither."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated; \ two exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def hoeffding(self):
        rows = [
            cmath(r"X_i \text{ independent},\ EX_i=0,\ \|X_i\|_{\psi_2} \le K", r":", r"P\big(|\textstyle\sum a_i X_i| \ge t\big) \le 2\exp\Big(-\frac{c\, t^2}{K^2 \|a\|_2^2}\Big)", font_size=30),
            cmath(r"X_i \text{ independent},\ EX_i=0,\ \|X_i\|_{\psi_1} \le K", r":", r"P\big(|\textstyle\sum a_i X_i| \ge t\big) \le 2\exp\Big(-c \min\Big(\frac{t^2}{K^2\|a\|_2^2}, \frac{t}{K \|a\|_\infty}\Big)\Big)", font_size=28),
            cmath(r"\text{read}", r":", r"\text{Gaussian for small deviations, \ exponential for large ones}", font_size=32),
            cmath(r"\text{Bernstein: } EX_i=\mu,\ |X_i-\mu|\le1,\ \mathrm{Var}(X_i)=\sigma^2", r":", r"e^{-n t^2 / (2(\sigma^2 + t/3))}: \ \text{sees the variance}", font_size=30),
        ]
        rows[0][-1].set_color(GAUSSC)
        rows[1][-1].set_color(MATC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"general Hoeffding"), why(r"Bernstein's inequality, \ general form"), why(r"two regimes"), why(r"rare events: \ $\sigma^2 \ll 1$")]
        heading = label('Independent centered sums have Gaussian and exponential tail regimes', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The two basic inequalities. For a weighted sum of independent, mean-zero sub-Gaussians, the general Hoeffding inequality: Gaussian tails, with the variance replaced by K squared times the squared length of the weights. <bookmark mark='b'/> For independent, mean-zero sub-exponentials, Bernstein's inequality has a Gaussian regime for small deviations and an exponential regime for large ones. <bookmark mark='c'/> Small deviations look Gaussian; large ones only exponential, because a single big summand can dominate. <bookmark mark='d'/> For bounded variables with small variance, Bernstein's classical form uses the variance itself rather than the range, which is everything for rare events."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("tails")
        r = d["0.02"]
        t = np.asarray(r["t"])
        A = axes([0, 0.08], [-8, 0.2], x_length=7.4, y_length=4.4, xlabel=r"$t$: \ excess of the sample mean over $p$", ylabel=r"$\log_{10} P(\bar X - p \ge t)$",
                 xticks=[0, 0.02, 0.04, 0.06, 0.08], yticks=[-8, -6, -4, -2, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), 1e-9))  # noqa: E731
        ce = clip_curve(ax, t, lg(r["exact"]), EXACTC, 4, ymin=-8, ymax=0.2)
        ch = clip_curve(ax, t, lg(r["hoeffding"]), BADC, 3.5, ymin=-8, ymax=0.2)
        cb = clip_curve(ax, t, lg(r["bernstein"]), BNDC, 3.5, ymin=-8, ymax=0.2)
        cc = clip_curve(ax, t, lg(r["chernoff"]), GOODC, 3.5, ymin=-8, ymax=0.2)
        side = fit_rows(VGroup(
            label(rf"Bernoulli$(0.02)$, \ $n = {d['n']}$: \ a rare event", font_size=22),
            label(r"white: \ the exact binomial tail", font_size=22, color=EXACTC),
            label(r"red: \ Hoeffding, \ blind to the variance", font_size=22, color=BADC),
            label(r"purple: \ Bernstein, \ uses $\sigma^2 = 0.0196$", font_size=22, color=BNDC),
            label(r"green: \ Chernoff's exact exponent", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The difference matters most for rare events. Two hundred trials of an event with "
            "probability two percent, and the chance that the observed rate exceeds two percent by t. <bookmark mark='b'/> "
            "In white, the exact binomial tail. <bookmark mark='c'/> In red, Hoeffding's bound, which only knows that each "
            "trial lies between zero and one, and is hopelessly loose: it treats a two percent event as if it were a coin "
            "toss. <bookmark mark='d'/> In purple, Bernstein's bound, which uses the variance, and is orders of magnitude "
            "tighter. <bookmark mark='e'/> In green, Chernoff's bound with the exact Kullback–Leibler exponent, tighter still. "
            "The more a bound knows about the variables, the closer it comes to the truth."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cc), FadeIn(side[4]))
        self.clear_scene()

    def rare(self):
        d = load("tails")
        r = d["0.5"]
        t = np.asarray(r["t"])
        i = int(np.argmin(np.abs(t - 0.1)))
        j = int(np.argmin(np.abs(np.asarray(d["0.02"]["t"]) - 0.04)))
        q = d["0.02"]
        rows = [
            cmath(r"p = 0.5, \ t = 0.1", r":", rf"\text{{exact }} {tex_sci(r['exact'][i])}, \ \text{{Hoeffding }} {tex_sci(r['hoeffding'][i])}, \ \text{{Bernstein }} {tex_sci(r['bernstein'][i])}", font_size=30),
            cmath(r"p = 0.02, \ t = 0.04", r":", rf"\text{{exact }} {tex_sci(q['exact'][j])}, \ \text{{Hoeffding }} {tex_sci(q['hoeffding'][j])}, \ \text{{Bernstein }} {tex_sci(q['bernstein'][j])}", font_size=30),
            cmath(r"\text{a coin}", r":", r"\text{Hoeffding is nearly sharp: \ the variance is as large as it can be}", font_size=32),
            cmath(r"\text{a rare event}", r":", r"\text{only a variance-aware bound is useful}", font_size=32),
        ]
        rows[2][-1].set_color(GAUSSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"$n = 200$"), why(r"$n = 200$"), why(r"$\sigma^2 = 1/4$"), why(r"Part 48's Bousquet, \ again")]
        heading = label('Exact tail probabilities and upper bounds answer different questions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> For a fair coin, at a tenth above a half, the exact tail is {say_sci(r['exact'][i])}, Hoeffding gives {say_sci(r['hoeffding'][i])} and Bernstein {say_sci(r['bernstein'][i])}: the bounds are upper guarantees, not approximations to the exact probability. <bookmark mark='b'/> For the rare event, at four points above two percent, the exact tail is {say_sci(q['exact'][j])}, while Hoeffding gives {say_sci(q['hoeffding'][j])}. <bookmark mark='c'/> For a coin the variance is already as large as a bounded variable allows, so Hoeffding loses little. <bookmark mark='d'/> For rare events only a bound that sees the variance is any use, the same lesson as Bousquet's inequality in Part forty-eight."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
