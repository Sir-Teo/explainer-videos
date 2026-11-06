from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.family()
        self.history()
        self.chart()
        self.worked_bs()
        self.board()
        self.turn()
        self.testing()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1956,)).to_edge(UP, buff=0.35)
        hc = history_card(1956, r"R. R. Bahadur \& L. J. Savage, \ \emph{The nonexistence of certain statistical procedures}",
                          r"in the \emph{Annals}: \ over the family of all distributions with a finite mean, \ no confidence interval "
                          r"of bounded length covers the mean with probability bounded away from zero, \ and no test of a mean has "
                          r"power above its size", color=MISSC, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a finite mean is not enough: \ a tiny chance of a huge value can move it anywhere", font_size=26, color=GREY_A),
            label(r"and a sample of any fixed size will usually not see that value", font_size=26, color=MISSC),
            label(r"so ``distribution-free'' cannot mean ``about the mean, \ with no assumptions''", font_size=28, color=TESTPT),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1956 Raghu Raj Bahadur and Leonard Savage published a short paper with a forbidding title: "
            "the nonexistence of certain statistical procedures. Over the family of all distributions with a finite mean, no "
            "confidence interval for the mean, of any bounded length, has coverage bounded away from zero; and no test about "
            "the mean has power greater than its size. <bookmark mark='b'/> The reason is simple. A finite mean is a weak "
            "condition: a tiny probability of a huge value can move the mean anywhere. <bookmark mark='c'/> And a sample of any "
            "fixed size will usually not contain that value. <bookmark mark='d'/> So distribution-free inference cannot mean "
            "inference about the mean with no assumptions at all."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def family(self):
        rows = [
            cmath(r"P_\varepsilon", r"=", r"(1 - \varepsilon)\,N(0, 1) + \varepsilon\,\delta_{3/\varepsilon}", font_size=38),
            cmath(r"E_{P_\varepsilon} X", r"=", r"3 \ \text{ for every } \varepsilon", font_size=38),
            cmath(r"P(\text{no atom in } n)", r"=", r"(1 - \varepsilon)^n \to 1 \text{ as } \varepsilon \to 0", font_size=36),
            cmath(r"\text{then}", r":", r"t\text{-interval near } 0, \ \text{far from } 3", font_size=38),
        ]
        rows[1][-1].set_color(TESTPT)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"a normal plus a far-away atom"), why(r"the mean never changes"), why(r"the atom is rarely seen"), why(r"the sample looks like $N(0, 1)$")]
        with self.voiceover(
            "<bookmark mark='a'/> A concrete family makes the argument visible. Mix a standard normal with a small probability "
            "epsilon of a single value, three over epsilon. <bookmark mark='b'/> Every member of the family has mean exactly "
            "three. <bookmark mark='c'/> But the chance that a sample of n contains the far-away value is small when epsilon is "
            "small: the sample misses it with probability one minus epsilon to the n. <bookmark mark='d'/> When it does, the "
            "sample looks exactly like standard normal data, and the t-interval sits near zero, nowhere near the true mean of "
            "three."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def history(self):
        rows = [
            cmath(r"\text{Wilks (1941)}", r":", r"\text{tolerance intervals from order statistics: \ distribution-free}", font_size=32),
            cmath(r"[X_{(r)}, X_{(n+1-r)}]", r":", r"\text{covers a fraction } \ge \beta \text{ of } P \text{ with known probability}", font_size=32),
            cmath(r"\text{why}", r":", r"F(X_{(k)}) \sim \mathrm{Beta}(k, n + 1 - k) \text{ for any continuous } F", font_size=34),
            cmath(r"\text{the same fact}", r":", r"\text{returns in chapter 1 as the law of conformal coverage}", font_size=32),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"a statistician's oldest tool"), why(r"order statistics"), why(r"the probability integral transform"), why(r"seventy years later")]
        with self.voiceover(
            "<bookmark mark='a'/> Distribution-free inference for prediction is older than it looks. In 1941 Samuel "
            "Wilks built tolerance intervals from order statistics: no assumption about the distribution except "
            "continuity. <bookmark mark='b'/> The interval between two order statistics covers at least a fraction "
            "beta of the population, with a probability that can be computed exactly. <bookmark mark='c'/> The reason "
            "is that the distribution function evaluated at the k-th order statistic has a Beta distribution, whatever "
            "the distribution is: the probability integral transform makes every continuous law uniform. <bookmark "
            "mark='d'/> The same fact returns in chapter one, seventy years later, as the exact law of conformal "
            "coverage."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("bs")
        rows = d["rows"]
        le = np.log10([r["eps"] for r in rows])
        A = axes([-3.1, -0.4], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=rf"$\varepsilon$ \ (log scale), \ $n = {d['n']}$", ylabel=r"coverage of the 95\% $t$-interval",
                 xticks=[-3, -2, -1], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 0.5, 0.95], center=[-2.5, 0.2, 0])
        ax = A.ax
        ub = polyline(ax, le, [r["upper"] for r in rows], GREY_B, 3)
        sim = VGroup(polyline(ax, le, [r["sim"] for r in rows], MISSC, 4), *[Dot(ax.c2p(a, r["sim"]), radius=0.07, color=MISSC) for a, r in zip(le, rows)])
        nom = DashedLine(ax.c2p(-3.1, 0.95), ax.c2p(-0.4, 0.95), color=COVC, stroke_width=2)
        r3 = [r for r in rows if r["eps"] == 0.003][0]
        side = fit_rows(VGroup(
            label(r"every distribution here has mean 3", font_size=22),
            label(rf"red: \ simulated coverage, \ {r3['sim']:.2f} at $\varepsilon = 0.003$", font_size=22, color=MISSC),
            label(r"grey: \ the bound $1 - (1 - \varepsilon)^n(1 - \text{tiny})$", font_size=22, color=GREY_B),
            label(rf"at $\varepsilon = 0.001$: \ {rows[-1]['sim']:.3f}; \ and $\to 0$", font_size=22, color=MISSC),
            label(r"no $n$ is large enough for every $P$", font_size=22, color=TESTPT),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The t-interval's coverage across the family, with fifty observations. Every distribution has "
            f"mean three. <bookmark mark='b'/> As epsilon shrinks, the simulated coverage falls: {say(r3['sim'], 2)} at epsilon "
            f"three in a thousand. <bookmark mark='c'/> It follows the bound set by the chance of seeing no atom at all. "
            f"<bookmark mark='d'/> At epsilon one in a thousand it is {say(rows[-1]['sim'], 3)}, and it goes to zero. <bookmark "
            f"mark='e'/> Whatever n you fix, some member of the family defeats it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(simulated_tag(r"simulated; \ bound exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sim), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ub), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def worked_bs(self):
        rows = [
            cmath(r"n = 50, \ \varepsilon = 0.003", r":", r"P(\text{no atom}) = 0.997^{50} = 0.861", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"\text{coverage} \le 1 - 0.861 + \text{tiny} \approx 14\%", font_size=36),
            cmath(r"\varepsilon = 0.0003", r":", r"P(\text{some atom}) = 1 - 0.9997^{50} = 1.5\%", font_size=36),
            cmath(r"\text{and the mean}", r":", r"\text{still exactly } 3 \text{, \ whatever } \varepsilon", font_size=36),
        ]
        rows[1][-1].set_color(MISSC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"almost every sample is normal"), why(r"the simulated 14\%"), why(r"smaller still"), why(r"a far atom carries it")]
        with self.voiceover(
            "<bookmark mark='a'/> The numbers behind the chart. With fifty observations and epsilon three in a "
            "thousand, the chance that the sample contains no atom is point nine nine seven to the fiftieth, about "
            "eighty-six percent. <bookmark mark='b'/> In that case the data are plain normal and the interval sits "
            "near zero, nowhere near the mean, so the coverage is at most about fourteen percent, as the simulation "
            "showed. <bookmark mark='c'/> Shrink epsilon tenfold, and only one and a half percent of samples ever see "
            "an atom. <bookmark mark='d'/> Yet the mean is exactly three throughout, carried by a value so rare and so "
            "far away that no sample of fifty can be expected to find it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("Bahadur"),
                   f"<bookmark mark='a'/> On the Board: the t-interval for the mean, over the mixture with epsilon three in a "
                   f"thousand, covers {100 * br[0]['achieved']:.1f} percent of the time: broken. <bookmark mark='b'/> But on the "
                   f"same family, a split conformal prediction interval for the next observation covers "
                   f"{100 * br[1]['achieved']:.1f} percent: kept, with no assumption at all.",
                   [("a", [0]), ("b", [1])])

    def turn(self):
        rows = fit_rows(VGroup(
            label(r"what changed?", font_size=28, color=GREY_A),
            label(r"the mean: \ a functional of $P$ that a rare event can move without limit", font_size=26, color=MISSC),
            label(r"the next observation: \ exchangeable with the ones we have", font_size=26, color=COVC),
            label(r"its rank among them is uniform, \ whatever $P$ is", font_size=26, color=COVC),
            label(r"this part: \ what that one fact guarantees, \ and the theorems that say what it cannot", font_size=26, color=TESTPT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What changed between the two rows? <bookmark mark='b'/> The mean is a functional of the "
            "distribution that a rare event can move without limit. <bookmark mark='c'/> The next observation is different: it "
            "is exchangeable with the ones we already have. <bookmark mark='d'/> So its rank among them is uniformly "
            "distributed, whatever the distribution is. <bookmark mark='e'/> This part is about what that one fact guarantees, "
            "and about the theorems that say what it cannot."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def testing(self):
        rows = [
            cmath(r"\text{tests of the mean}", r":", r"\text{every test of } H_0: \mu = \mu_0 \text{ has power} \le \text{size}", font_size=34),
            cmath(r"\text{over the family}", r":", r"\text{all laws with a finite mean}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{tests of the median are fine: \ the sign test}", font_size=34),
            cmath(r"\text{the lesson}", r":", r"\text{the functional decides, \ not the method}", font_size=34),
        ]
        rows[0][-1].set_color(MISSC)
        rows[2][-1].set_color(COVC)
        whys = [why(r"Bahadur \& Savage's second theorem"), why(r"too rich a family"), why(r"Part 16"), why(r"medians are robust")]
        with self.voiceover(
            "<bookmark mark='a'/> Bahadur and Savage's paper has a second theorem, about tests. Over the family of all "
            "distributions with a finite mean, every test of a hypothesis about the mean has power no larger than its "
            "size against every alternative: it cannot do better than a coin. <bookmark mark='b'/> The family is "
            "simply too rich. <bookmark mark='c'/> But tests of the median are fine: the sign test of Part sixteen is "
            "exact and powerful over every continuous distribution. <bookmark mark='d'/> The lesson is that the "
            "functional decides what is possible, not the cleverness of the method: the median cannot be moved by a "
            "rare value, and the mean can."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def upgrade(self):
        cards = [
            upgrade_card(34, r"split conformal covers at least $1 - \alpha$, \ by experiment", r"exchangeability; \ coverage on average",
                         r"chapters 1--3: \ the proofs, \ and what cannot be had"),
            upgrade_card(56, r"conformal selection needs only exchangeability", r"exchangeable data",
                         r"chapters 4--9: \ beyond exchangeability, \ and conditional guarantees"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part thirty-four showed by experiment that split conformal covers at "
            "least one minus alpha, assuming exchangeability, on average. Chapters one to three prove it, and prove what "
            "cannot be had. <bookmark mark='b'/> Part fifty-six's conformal selection needed only exchangeability. Chapters four "
            "to nine go beyond it, and ask for conditional guarantees."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 57", font_size=34, color=GREY_B), label(r"Distribution-Free Inference", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the quantile lemma, \ proved; \ full, \ split and jackknife$+$ conformal",
            r"impossibility: \ conditional coverage, \ distribution-free functionals",
            r"conditional guarantees over function classes; \ group coverage on NHANES",
            r"beyond exchangeability; \ online coverage; \ outliers; \ risk control; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 34, \ 46, \ 47").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.dfree}, \ the rank strip").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-seven: distribution-free inference. <bookmark mark='b'/> The quantile lemma, "
            "proved, with full, split and jackknife plus conformal; the impossibility theorems for conditional coverage and for "
            "distribution-free functionals; conditional guarantees over function classes, with group coverage on NHANES blood "
            "pressures; going beyond exchangeability; coverage online; outlier detection; risk control; and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
