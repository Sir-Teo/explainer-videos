from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Concentration(VoiceoverScene):
    def construct(self):
        self.card()
        self.azuma()
        self.mcdiarmid()
        self.idea()
        self.bins()
        self.freedman()

    def card(self):
        card = chapter_card(6, r"Martingale concentration", r"Hoeffding, \ without independence", part=PART)
        with self.voiceover("Chapter six. Concentration for martingales: Hoeffding's inequality without independence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def azuma(self):
        rows = [
            cmath(r"|M_k - M_{k-1}|", r"\le", r"c_k \ \ \text{for a martingale } M", font_size=34),
            cmath(r"E\big[e^{\lambda D_k} \mid \mathcal F_{k-1}\big]", r"\le", r"e^{\lambda^2 c_k^2 / 2} \ \ \text{(Hoeffding's lemma, conditionally)}", font_size=30),
            cmath(r"E e^{\lambda (M_n - M_0)}", r"\le", r"e^{\lambda^2 \sum c_k^2 / 2} \ \ \text{(peel off one step at a time)}", font_size=30),
            cmath(r"P(|M_n - M_0| \ge t)", r"\le", r"2 \exp\!\big(-t^2 / 2\textstyle\sum c_k^2\big)", font_size=34),
        ]
        rows[3][-1].set_color(MARTC)
        whys = [why(r"bounded differences"), why(r"a bounded, \ mean-zero step"), why(r"the tower property"), why(r"Azuma--Hoeffding (1967, 1963)")]
        with self.voiceover(
            "<bookmark mark='a'/> Part six's Hoeffding inequality needed independence. Martingales do without it. "
            "Suppose each step has absolute value bounded by a deterministic c k. <bookmark mark='b'/> Hoeffding's "
            "lemma, applied conditionally, bounds the conditional moment generating function of each step. <bookmark "
            "mark='c'/> The tower property peels the steps off one at a time, from the last to the first. <bookmark "
            "mark='d'/> Chernoff's method then gives the Azuma–Hoeffding inequality: a Gaussian tail with variance "
            "proxy the sum of the squared bounds, for any martingale at all."
        ) as vo:
            heading=label('Conditional increment bounds replace independence',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mcdiarmid(self):
        rows = [
            cmath(r"f(x_1, \ldots, x_n)", r":", r"\text{changing one } x_i \text{ moves } f \text{ by at most } c_i", font_size=32),
            cmath(r"M_k", r"=", r"E[f(X) \mid X_1, \ldots, X_k]: \ \text{a Doob martingale with steps} \le c_k", font_size=30),
            cmath(r"P(|f - E f| \ge t)", r"\le", r"2 \exp\!\big(-2t^2 / \textstyle\sum c_i^2\big)", font_size=34),
            cmath(r"\text{e.g.}", r":", r"\text{empty bins, \ increasing subsequences, \ graph colourings}", font_size=32),
        ]
        rows[2][-1].set_color(MARTC)
        whys = [why(r"bounded differences"), why(r"reveal one coordinate at a time"), why(r"McDiarmid (1989)"), why(r"functions of many independent inputs")]
        with self.voiceover(
            "<bookmark mark='a'/> The most useful consequence is Colin McDiarmid's. Take any function of independent inputs "
            "that changes by at most c i when the i-th input changes. <bookmark mark='b'/> Reveal the inputs one at a time: "
            "the successive predictions of f form a Doob martingale whose steps are bounded by the c's. <bookmark mark='c'/> "
            "So f concentrates around its mean with a Gaussian tail, <bookmark mark='d'/> for functions far too complicated to "
            "analyse directly: the number of empty bins, the longest increasing subsequence of a random permutation, the "
            "chromatic number of a random graph, or the risk of a learned predictor in Part fifty-four."
        ) as vo:
            heading=label('Independent inputs give bounded-difference concentration',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bins(self):
        d = load("azuma")
        ts = np.asarray(d["ts"], float)
        A = axes([0, 62], [-5, 0], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$\log_{10} P(|Z - EZ| \ge t)$",
                 xticks=[0, 20, 40, 60], yticks=[-5, -4, -3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), np.finfo(float).tiny))  # noqa: E731
        emp_ok = np.asarray(d["emp"]) > 0
        emp = VGroup(polyline(ax, ts[emp_ok], lg(np.asarray(d["emp"])[emp_ok]), CHAINC, 3),
                     *[Dot(ax.c2p(a, b), radius=0.06, color=CHAINC) for a, b in zip(ts[emp_ok], lg(np.asarray(d["emp"])[emp_ok]))])
        bnd = polyline(ax, ts, lg(d["bound"]), MARTC, 3)
        side = fit_rows(VGroup(
            label(rf"{d['n']:,} balls into {d['n']:,} bins: \ $Z$ = the empty bins", font_size=22),
            label(rf"$E Z = n(1 - 1/n)^n = {d['mean_theory']:.1f}$; \ simulated {d['mean']:.1f}, \ SD {d['sd']:.1f}", font_size=22, color=GREY_A),
            label(r"moving one ball changes $Z$ by at most 1: \ $c_i = 1$", font_size=22),
            label(r"blue: \ 20,000 simulations; \ gold: \ McDiarmid's bound", font_size=22, color=MARTC),
            label(r"valid, \ the right shape, \ loose: \ it cannot know the variance", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test. Throw a thousand balls into a thousand bins at random and count the empty bins. <bookmark mark='b'/> Its mean is n times one minus one over n to the n, about {d['mean_theory']:.0f}, and simulation gives a standard deviation of about ten. <bookmark mark='c'/> Moving one ball changes the count by at most one, so McDiarmid applies with every c equal to one. <bookmark mark='d'/> In blue, the simulated tail probabilities on a log scale; in gold, the bound. <bookmark mark='e'/> The bound always holds and has the right Gaussian shape, but it is loose: it uses only the worst-case change of one ball, Its sub-Gaussian variance proxy corresponds to a scale near sixteen, rather than the actual standard deviation near ten. A finite Monte Carlo curve also has sampling error. Inequalities that use the variance do better."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 throws of 1,000 balls")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(emp), Create(bnd), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def freedman(self):
        rows = fit_rows(VGroup(
            label(r"Freedman (1975): \ steps $\le c$, \ predictable variation $\langle M \rangle_n \le v$", font_size=26),
            label(r"$P(M_n - M_0 \ge t, \ \langle M \rangle_n \le v) \le \exp\!\Big(-\dfrac{t^2}{2(v + ct/3)}\Big)$", font_size=28, color=MARTC),
            label(r"Bernstein for martingales: \ the variance, \ not the range, \ sets the scale", font_size=26, color=S.ACCENT),
            label(r"the workhorse of bandit and sequential-testing proofs \ (Part 58)", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> David Freedman's inequality of 1975 uses the variance. If the steps are bounded by "
            "c and the predictable variation is at most v, <bookmark mark='b'/> the tail is bounded by the "
            "exponential of minus t squared divided by two times the quantity v plus c t over three. <bookmark "
            "mark='c'/> It is Bernstein's inequality for martingales: when the steps are usually small, the variance "
            "rather than the range sets the scale. <bookmark mark='d'/> It is the workhorse of the proofs for bandits"
            " and sequential tests in Part fifty-eight."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"D_k", r"=", r"E[f \mid X_{1:k}] - E[f \mid X_{1:k-1}]", font_size=34),
            cmath(r"\phantom{D}", r"\in", r"[L_k, \ L_k + c_k], \ \ L_k \text{ known given } X_{1:k-1}", font_size=32),
            cmath(r"E[e^{\lambda D_k} \mid X_{1:k-1}]", r"\le", r"e^{\lambda^2 c_k^2 / 8} \ \ \text{(Hoeffding's lemma, range } c_k)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"P(f - E f \ge t) \le e^{-2t^2 / \sum c_k^2}", font_size=34),
        ]
        rows[3][-1].set_color(MARTC)
        whys = [why(r"one coordinate revealed"), why(r"independence keeps the range $c_k$"), why(r"a range, \ not a bound: \ $1/8$"), why(r"Chernoff")]
        with self.voiceover(
            "<bookmark mark='a'/> Why the constant two in McDiarmid's bound, not the one half of Azuma's? Look at one "
            "martingale step: what is learned by revealing the k-th input. <bookmark mark='b'/> Because the inputs are "
            "independent, the step lies in an interval of length c k whose position is already known from the earlier "
            "inputs. <bookmark mark='c'/> Hoeffding's lemma for a variable confined to a range of length c gives the "
            "sharper exponent, lambda squared c squared over eight. <bookmark mark='d'/> Multiplying through the steps and "
            "optimizing lambda yields e to the minus two t squared over the sum of the c k squared."
        ) as vo:
            heading=label('A known interval length sharpens the exponential bound',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
