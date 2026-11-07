from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Carving(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.likelihood()
        self.chart()
        self.table()
        self.multivariate()
        self.carving()

    def card(self):
        card = chapter_card(4, r"Randomization and carving", r"Trading a little noise for a lot of power", lit=(2018,), part=PART)
        with self.voiceover("Chapter four. Randomization and carving: trading a little noise for a lot of power."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\text{hard selection}", r":", r"\text{report } Y \text{ if } Y > c: \ \text{a sharp cut at } c", font_size=30),
            cmath(r"\text{near } c", r":", r"\text{the lower endpoint tends to }-\infty\text{ as }y\downarrow c", font_size=32),
            cmath(r"\text{randomized}", r":", r"\text{report } Y \text{ if } Y + W > c, \ \ W \sim N(0, \gamma^2) \text{ independent}", font_size=32),
            cmath(r"\text{now}", r":", r"\text{a soft cut: \ information survives}", font_size=30),
        ]
        rows[1][-1].set_color(NAIVEC)
        rows[3][-1].set_color(SPLITC)
        whys = [why(r"chapter 3's truncation"), why(r"Kivaranovic \& Leeb"), why(r"Tian \& Taylor (2018)"), why(r"the point of randomizing")]
        head = label('Idea', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Why are conditional intervals so long near the edge? With hard selection, report Y only if it exceeds c, the law given selection is cut off sharply at c. <bookmark mark='b'/> If Y lands just above c, almost any mean below it could have produced it, and its finite lower endpoint tends to minus infinity as the observation approaches the threshold. An interior observation does not itself have an infinite endpoint. <bookmark mark='c'/> Xiaoying Tian and Jonathan Taylor's remedy is to select on a noisy copy instead: report Y if Y plus an independent normal W exceeds c. <bookmark mark='d'/> Now the cut is soft. A value near c is only somewhat less likely to have been selected, so some of the information that hard selection destroys survives."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def likelihood(self):
        rows = [
            cmath(r"p_\mu(y \mid \text{selected})", r"=", r"\frac{\phi((y-\mu)/\sigma)\,\Phi((y-c)/\gamma)}{\sigma\,\Phi((\mu-c)/\sqrt{\sigma^2+\gamma^2})}", font_size=30),
            cmath(r"\gamma \to 0", r":", r"\Phi(\cdot) \to 1\{y > c\}: \ \text{hard truncation}", font_size=34),
            cmath(r"\gamma \to \infty", r":", r"\Phi(\cdot) \to \text{const}: \ \text{no selection effect, \ random selection}", font_size=32),
            cmath(r"\text{inference}", r":", r"\text{invert its pivot, \ numerically}", font_size=32),
        ]
        rows[0][-1].set_color(SPLITC)
        whys = [why(r"the selective likelihood"), why(r"chapter 3"), why(r"selection by coin toss"), why(r"or by MCMC in many dimensions")]
        head = label('Likelihood', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The selected density is the normal density times the probability of selection given y, divided by the marginal probability of selection. That denominator depends on mu and must stay in the likelihood. <bookmark mark='b'/> As the randomization vanishes it becomes the hard truncation of chapter three. <bookmark mark='c'/> As it grows, the selection no longer depends on y at all, so there is no selection effect, but the selection itself becomes a coin toss. <bookmark mark='d'/> In between, invert the pivot of this selective likelihood; in one dimension by quadrature, in many by Monte Carlo."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("carving")
        ys = np.asarray(d["curve"]["y"])
        hard = np.asarray(d["curve"]["hard"], float)
        soft = np.asarray(d["curve"]["soft"], float)
        A = axes([2.0, 4.0], [-8.2, 3.2], x_length=7.4, y_length=4.4, xlabel=r"observed $y$ \ (selected when above $c = 2$)", ylabel=r"lower 95\% limit for $\mu$",
                 xticks=[2, 2.5, 3, 3.5, 4], yticks=[-8, -4, 0, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        ch = polyline(ax, ys, hard, NAIVEC, 4)
        cs = polyline(ax, ys, soft, SPLITC, 4)
        diag = DashedLine(ax.c2p(2.0, 2.0 - 1.96), ax.c2p(4.0, 4.0 - 1.96), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the lower end of the selective interval", font_size=22),
            label(rf"red: \ hard selection: \ {hard[0]:.1f} (below viewport) at $y$ just above 2", font_size=22, color=NAIVEC),
            label(rf"teal: \ randomized, \ $\gamma = 1$: \ {soft[0]:.2f}", font_size=22, color=SPLITC),
            label(r"grey: \ the naive $y - 1.96$", font_size=22, color=GREY_B),
            label(r"far from the edge, \ all three agree", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The lower end of the interval, as a function of the observed value. <bookmark mark='b'/> With hard selection, a value just above the threshold gives a lower limit far below zero; the curve leaves the displayed range below minus eight, without a false horizontal plateau. <bookmark mark='c'/> With randomization of standard deviation one, the same observation gives {say(soft[0], 2)}. <bookmark mark='d'/> The naive limit, y minus one point nine six, ignores selection altogether. <bookmark mark='e'/> Far from the threshold all three agree, because there selection carries little information."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact, \ by quadrature")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(diag), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("carving")
        hdr = [r"randomization $\gamma$", r"selected", r"coverage", r"median length"]
        body = [[f"{r['gamma']:g}", f"{100 * r['selected']:.0f}\\%", f"{100 * r['coverage']:.1f}\\%", f"{r['len']:.2f}"] for r in d["rows"]]
        tab = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.28, colors=[GREY_B] + [WHITE] * len(body)).move_to([0, 0.5, 0])
        foot = fit_rows(VGroup(
            label(r"$\mu = 1$, \ threshold $c = 2$, \ 1,500 draws per row; \ uncapped interval lengths", font_size=22, color=GREY_A),
            label(r"coverage is exact at every $\gamma$; \ the interval shortens sharply as soon as $\gamma > 0$", font_size=24, color=SPLITC),
            label(r"the price: \ selection becomes noisier", font_size=24, color=NAIVEC),
        ), 12.4, 0.25, [0, -2.4, 0])
        r0, r1 = d["rows"][0], d["rows"][3]
        with self.voiceover(
            f"<bookmark mark='a'/> By simulation, with a true mean of one and the threshold at two. <bookmark mark='b'/> "
            f"Every row covers about ninety-five percent: the method is exact whatever the randomization. <bookmark "
            f"mark='c'/> But the median length falls from {say(r0['len'], 2)} with hard selection to {say(r1['len'], 2)} with "
            f"randomization of standard deviation one. <bookmark mark='d'/> The price is that selection itself becomes "
            f"noisier, which in a real problem means occasionally selecting the wrong variable."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r[2] for r in tab[1:]]), color=SPLITC))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r[3] for r in tab[1:]]), color=SPLITC), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def multivariate(self):
        rows = [
            cmath(r"\text{randomized lasso}", r":", r"\arg\min \tfrac12\|y - X\beta\|^2 + \lambda\|\beta\|_1 + \tfrac\epsilon2\|\beta\|^2 - \omega'\beta, \ \ \omega \sim N(0, \gamma^2 I),\ \epsilon>0", font_size=32),
            cmath(r"\text{selective law}", r":", r"\text{the density of } y \text{ times } P(\text{same } E, s \mid y)", font_size=34),
            cmath(r"\text{computation}", r":", r"\text{change variables; \ sample by MCMC}", font_size=32),
            cmath(r"\text{result}", r":", r"\text{valid, \ and nearly naive length}", font_size=32),
        ]
        rows[0][-1].set_color(SPLITC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"Tian \& Taylor (2018)"), why(r"randomization smooths it"), why(r"Panigrahi \& Taylor"), why(r"power regained")]
        head = label('Multivariate', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> In many dimensions the same idea applies to the lasso itself: perturb its objective by a random linear term omega transpose beta, with a positive ridge term to ensure a finite optimizer even when p exceeds n. <bookmark mark='b'/> The selective law of y is its density times the probability, over omega, of selecting the same active set and signs. <bookmark mark='c'/> A change of variables, from omega to the lasso's solution and subgradient, makes that probability tractable, and Snigdha Panigrahi and Taylor sample from it by Markov chain Monte Carlo or approximate it. <bookmark mark='d'/> The result is valid selective intervals which can recover much of the lost power. Exact likelihood calculations and computational approximations have different validity requirements; near-naive length is not a uniform theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def carving(self):
        rows = fit_rows(VGroup(
            label(r"carving \ (Fithian, \ Sun \& Taylor 2014):", font_size=28, color=GREY_A),
            label(r"select on a fraction of the data, \ as in splitting", font_size=26, color=SPLITC),
            label(r"but infer with all of it, \ conditioning on the selection", font_size=26, color=CONDC),
            label(r"optimal carving tests weakly improve on splitting: \ the held-out part is used, \ and so is what is left in the first part", font_size=26, color=HYBC),
            label(r"splitting is randomization too: \ the random split is the noise", font_size=26, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A close relative is data carving, from Fithian, Sun and Taylor. <bookmark mark='b'/> Select on a fraction of the data, as in sample splitting, <bookmark mark='c'/> but then infer with all of it, conditioning on the selection. <bookmark mark='d'/> Their optimal carving tests can weakly improve on splitting within the specified testing class because they also use information left in the selection sample. This does not order every pair of interval procedures. <bookmark mark='e'/> Splitting is itself a kind of randomization, with the random split as the noise, which leads to the next chapter."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
