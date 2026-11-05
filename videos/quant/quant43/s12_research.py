from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         comma, fit_right, load)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        self.card()
        self.setup_storey()
        self.theorem()
        self.proof()
        self.tradeoff()
        self.check(r)
        self.bsw_cons()
        self.dependence(r)
        self.fdr_demo(load("fdr"))
        self.qtable(load("fdr"))
        self.record(r)
        self.bg_theorem()
        self.bg_proof()
        self.bg_check(load("bg_theory"))
        self.qvalues()
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How many have no skill, and where does skill go?", r"Why does Storey's estimate err on the "
                          r"safe side, and why do investors in skilled funds earn no alpha?", part=PART)
        with self.voiceover("For the researcher. Two theorems. Chapter two counted skilled funds using an estimate of how "
                            "many have no skill; Part twenty-five stated that it errs high, and this chapter proves why, "
                            "and what dependence does to it. Chapter three said skilled managers' investors earn no "
                            "alpha; this chapter proves that too, and checks both by simulation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_storey(self):
        rows = [cmath(r"m", r"=", r"m_0 + m_1", font_size=42),
                cmath(r"p_i \sim U(0, 1)", r":", r"i \text{ a true null}", font_size=40, colors={r"p_i \sim U(0, 1)": LUCK_C}),
                cmath(r"W(\lambda)", r"=", r"\#\{i : p_i > \lambda\}", font_size=42),
                cmath(r"\hat\pi_0(\lambda)", r"=", r"\frac{W(\lambda)}{m(1 - \lambda)}", font_size=44, colors={r"\hat\pi_0(\lambda)": HURDLE})]
        whys = [why(r"$m$ tests, $m_0$ of them true nulls (no skill), $m_1$ alternatives; $\pi_0 = m_0/m$ is unknown"),
                why(r"a continuous test's $p$-value is uniform under its null: the only assumption about nulls"),
                why(r"the number of $p$-values above a threshold $\lambda$"),
                why(r"Storey (2002): if every large $p$-value were a null, $W$ would be $m_0(1 - \lambda)$ on average")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The setting. <bookmark mark='a'/> m tests, of which m nought are true nulls: funds, or strategies, with no "
            "skill. <bookmark mark='b'/> Each null's p-value is uniform. That is the only assumption. "
            "<bookmark mark='c'/> Count the p-values above a threshold lambda. <bookmark mark='d'/> And scale: if every "
            "large p-value came from a null, the count would average m nought times one minus lambda."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\mathbb E\,\hat\pi_0(\lambda) = \pi_0 + (1 - \pi_0)\,\frac{\bar P_1(\lambda)}{1 - \lambda}\ "
                            r"\ge\ \pi_0,\qquad \bar P_1(\lambda) = \frac{1}{m_1}\sum_{i \in H_1} P(p_i > \lambda)", font_size=28),
                    wrapped_label(r"before truncation at one, the estimator is biased upward by the alternatives whose "
                                  r"$p$-values happen to be large; it never underestimates the share of nulls on average, "
                                  r"whatever the dependence between tests", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Storey's estimator is conservative (Storey 2002)", st, r"this part's proof", width=11.8,
                            font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The estimator's expectation is the true share, plus a term from the "
            "alternatives whose p-values land above lambda. <bookmark mark='b'/> So, on average, it never "
            "underestimates the share of funds with no skill; it is biased upward by exactly the weak alternatives. "
            "And, a point the proof makes plain, this needs no independence between the tests."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\mathbb E\,W(\lambda)", r"=", r"\textstyle\sum_i P(p_i > \lambda)", font_size=40, colors={r"=": HURDLE}),
                cmath(r"", r"=", r"m_0(1 - \lambda) + m_1\,\bar P_1(\lambda)", font_size=40),
                cmath(r"\div\ m(1 - \lambda)", r"\Rightarrow", r"\pi_0 + (1 - \pi_0)\frac{\bar P_1(\lambda)}{1 - \lambda}", font_size=38),
                cmath(r"\bar P_1 \ge 0", r"\Rightarrow", r"\mathbb E\,\hat\pi_0 \ge \pi_0", font_size=40, colors={r"\Rightarrow": GOOD})]
        whys = [why(r"a count is a sum of indicators; its expectation is the sum of their probabilities, by linearity alone"),
                why(r"each null contributes $1 - \lambda$, being uniform; each alternative its own probability"),
                why(r"divide by $m(1 - \lambda)$"),
                why(r"the extra term is a probability over a positive number: the bias is upward, and vanishes only if no "
                    r"alternative's $p$-value exceeds $\lambda$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof is linearity. <bookmark mark='a'/> A count is a sum of indicators, and its expectation is the sum "
            "of their probabilities. Nothing about independence is used. <bookmark mark='b'/> Each null contributes one "
            "minus lambda, being uniform; each alternative, its own probability. <bookmark mark='c'/> Divide. "
            "<bookmark mark='d'/> The extra term is a probability over a positive number, so the bias is upward, and "
            "vanishes only if no alternative's p-value ever exceeds lambda."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def tradeoff(self):
        rows = [cmath(r"\text{bias}", r"=", r"(1 - \pi_0)\frac{\bar P_1(\lambda)}{1 - \lambda}", font_size=40, colors={r"\text{bias}": COST_C}),
                cmath(r"\text{Var}\,\hat\pi_0", r"\approx", r"\frac{\pi_0\,\lambda}{m(1 - \lambda)}\ \ (\text{independent tests})",
                      font_size=36, colors={r"\text{Var}\,\hat\pi_0": LUCK_C}),
                cmath(r"\lambda \uparrow", r"\Rightarrow", r"\text{less bias, more variance}", font_size=40)]
        whys = [why(r"strong alternatives have small $p$-values, so for large $\lambda$ few of them are counted"),
                why(r"a binomial count over a shrinking range: the estimate gets noisier as $\lambda$ rises"),
                why(r"Storey chose $\lambda$ by bootstrapping the mean squared error; Barras, Scaillet and Wermers use the same "
                    r"idea")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Which threshold? <bookmark mark='a'/> The bias falls as lambda rises, since strong alternatives rarely have "
            "large p-values. <bookmark mark='b'/> But the variance rises, because fewer p-values are counted. "
            "<bookmark mark='c'/> A bias-variance trade-off, which Storey settled by bootstrapping the error."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check(self, r):
        rows = r["rows"]
        g = axes([0, 1], [0.75, 1.0], x_length=7.4, y_length=4.2, xlabel=r"threshold $\lambda$",
                 ylabel=r"mean of $\hat\pi_0$ over 400 samples", xticks=[0, 0.5, 1], yticks=[0.8, 0.9, 1.0], font_size=15
                 ).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        truth = DashedLine(ax.c2p(0, r["pi0"]), ax.c2p(1, r["pi0"]), color=GOOD, stroke_width=2)
        cols = {1.0: COST_C, 2.0: HURDLE, 3.0: SKILL_C}
        objs = VGroup()
        for mu, col in cols.items():
            sub = [x for x in rows if x["mu"] == mu]
            xs = np.array([x["lam"] for x in sub])
            th = curve(ax, xs, np.array([x["theory"] for x in sub]), col, stroke_width=2.5)
            dots = VGroup(*[Dot(ax.c2p(x["lam"], x["mean"]), radius=0.06, color=col) for x in sub])
            objs.add(VGroup(th, dots))
        leg = legend([(COST_C, r"weak alternatives, $\mu = 1$"), (HURDLE, r"$\mu = 2$"), (SKILL_C, r"strong, $\mu = 3$"),
                      (GOOD, r"true $\pi_0 = 0.8$")], font_size=16)
        side = VGroup(leg, label(r"lines: the theorem; dots: simulation", font_size=15, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        w1 = [x for x in rows if x["mu"] == 1.0 and x["lam"] == 0.5][0]
        s3 = [x for x in rows if x["mu"] == 3.0 and x["lam"] == 0.5][0]
        wm, sm = w1["mean"], s3["mean"]
        with self.voiceover(
            "The check. A thousand tests, eighty percent nulls, four hundred samples per setting. "
            "<bookmark mark='a'/> With weak alternatives, the estimator sits well above the truth: at lambda of a half, "
            f"{wm:.3f} against nought point eight. <bookmark mark='b'/> With strong ones, {sm:.3f}, almost unbiased. "
            "<bookmark mark='c'/> And every simulated mean sits on the theorem's line, at every threshold."
        ) as vo:
            self.play(FadeIn(g), FadeIn(truth), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(objs[0][0]), FadeIn(objs[0][1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(objs[2][0]), FadeIn(objs[2][1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(objs[1][0]), FadeIn(objs[1][1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def bsw_cons(self):
        rows = [cmath(r"\hat\pi^+_\gamma", r"=", r"\hat S^+_\gamma - \hat\pi_0\,\gamma/2", font_size=42, colors={r"\hat\pi^+_\gamma": SKILL_C}),
                cmath(r"\mathbb E\,\hat\pi_0 \ge \pi_0", r"\Rightarrow", r"\text{the lucky share is over-subtracted}", font_size=36),
                cmath(r"\Rightarrow", r"", r"\hat\pi^+ \text{ errs low: a lower bound on skill, in expectation}", font_size=36,
                      colors={r"\Rightarrow": GOOD})]
        whys = [why(r"Chapter 2's skilled share"),
                why(r"by the theorem, the estimated number of lucky nulls is too large on average"),
                why(r"so the estimated skilled share is conservative, apart from skilled funds that are not significant at "
                    r"$\gamma$, which also push it down")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A corollary for Chapter two. <bookmark mark='a'/> The skilled share subtracts the expected lucky nulls. "
            "<bookmark mark='b'/> By the theorem, that number is overestimated on average. <bookmark mark='c'/> So the "
            "estimated skilled share errs low: in expectation, a lower bound on skill. When Barras, Scaillet and Wermers "
            "found almost none, the bias was on skill's side."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def dependence(self, r):
        d = r["dep"]
        lines = VGroup(*[label(rf"correlation {x['rho']:.1f}: mean {x['mean']:.3f}, spread {x['sd']:.3f}", font_size=24,
                               color=[GOOD, HURDLE, BAD][i]) for i, x in enumerate(d)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.4).move_to(UP * 0.4)
        note_ = wrapped_label(r"1,000 tests, 80\% nulls, alternatives at $\mu = 2$, $\lambda = 0.5$; equicorrelated "
                              r"$z$-statistics", 10.4, 17, GREY_B).next_to(lines, DOWN, buff=0.5)
        s0, s6 = d[0]["sd"], d[-1]["sd"]
        with self.voiceover(
            "What dependence does. The theorem's mean needs no independence, but the variance does. "
            "<bookmark mark='a'/> With independent tests, the estimate's spread across samples is "
            f"{s0:.3f}. <bookmark mark='b'/> Give every pair of tests a correlation of nought point six, as funds in the "
            f"same market have, and the mean barely moves while the spread rises to {s6:.3f}. Correlated tests leave the "
            "estimator honest on average and unreliable in any one sample."
        ) as vo:
            self.play(FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def fdr_demo(self, f):
        q = f["q"]["0.1"]
        rows = [cmath(r"p_{(1)} \le \cdots \le p_{(m)}", r":", r"\text{sort the funds' one-sided } p\text{-values}", font_size=36),
                cmath(r"k^*", r"=", r"\max\{k : p_{(k)} \le q\,k/m\}", font_size=42, colors={r"k^*": HURDLE}),
                cmath(r"\text{naive } p < 0.05", r":", rf"{f['naive_n']}\ \text{{funds, }} {100 * f['naive_fdr']:.0f}\%\ \text{{false}}",
                      font_size=36, colors={r"\text{naive } p < 0.05": BAD}),
                cmath(r"\text{BH at } q = 10\%", r":", rf"{q['bh']}\ \text{{funds, }} {100 * q['bh_fdr']:.0f}\%\ \text{{false}}",
                      font_size=36, colors={r"\text{BH at } q = 10\%": GOOD})]
        whys = [why(r"in Chapter 2's population, with 22 truly skilled funds among 2,000"),
                why(r"Benjamini and Hochberg (1995): declare the $k^*$ smallest; the expected share of false ones is at "
                    r"most $q$; dividing by $\hat\pi_0$ (Storey) admits a few more"),
                why(r"testing each fund at 5\%: most of the funds declared skilled are lucky"),
                why(rf"controlling the false discovery rate: fewer, and none false here; Storey's version declares "
                    rf"{q['storey']}")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        nn, nf, nb, fb = f["naive_n"], 100 * f["naive_fdr"], q["bh"], 100 * q["bh_fdr"]
        with self.voiceover(
            "And how the estimate is used: controlling false discoveries, on Chapter two's population. "
            "<bookmark mark='a'/> Sort the funds' p-values. <bookmark mark='b'/> Benjamini and Hochberg's rule declares "
            "the smallest k, with k the largest index whose p-value is below q times k over m; the expected share of "
            f"false discoveries is then at most q. <bookmark mark='c'/> Testing each fund at five percent declares {nn} "
            f"funds skilled, {nf:.0f} percent of them falsely. <bookmark mark='d'/> The rule at ten percent declares "
            f"{nb}, and {fb:.0f} percent are false: fewer claims, and true ones."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def qtable(self, f):
        top = f["top"][:12]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=QC.IDEA) for h_ in (r"rank", r"$t$", r"$q$-value", r"truth")]))
        for x in top:
            tab.add(VGroup(label(rf"{x['rank']}", font_size=18), label(rf"{x['t']:.2f}", font_size=18, color=ACT_C),
                           label(rf"{x['q']:.3f}", font_size=18, color=HURDLE),
                           label(r"skilled" if x["skilled"] else r"lucky", font_size=18, color=SKILL_C if x["skilled"] else LUCK_C)))
        xs = [-3.6, -1.2, 1.2, 3.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 3.1 - 0.47 * j, 0])
        q1, q12 = top[0]["q"], top[-1]["q"]
        with self.voiceover(
            "Storey's q-values, on the same population: for each fund, the smallest false discovery rate at which it "
            f"would be declared skilled. <bookmark mark='a'/> The best funds have q-values near {q1:.3f}. "
            f"<bookmark mark='b'/> By the twelfth, {q12:.3f}. Here all twelve are truly skilled, because the population "
            "had twenty-two skilled funds with large alphas; with weaker skill, lucky funds would mix in further down, "
            "and the q-value says how far down to stop."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:7]], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[7:]], lag_ratio=0.15), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def record(self, r):
        q = r["record_boot_q"]
        rows = VGroup(
            label(rf"the House's 25 rows, one-sided hold-out $p$-values: $\hat\pi_0 = {r['record_pi0']:.2f}$", font_size=24,
                  color=REC_C),
            label(rf"bootstrap 90\% range: {q[0]:.2f} to {q[1]:.2f}", font_size=24, color=HURDLE),
            label(r"and the rows are correlated: the range is too narrow", font_size=22, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        p0, lo, hi = r["record_pi0"], q[0], q[1]
        with self.voiceover(
            "And on the House's own record. <bookmark mark='a'/> Twenty-five rows, one-sided p-values for a positive "
            f"hold-out Sharpe: an estimated share with no edge of {p0:.2f}. <bookmark mark='b'/> A bootstrap gives a "
            f"ninety percent range from {lo:.2f} to {hi:.2f}. <bookmark mark='c'/> And because many rows are related "
            "factor portfolios, the true uncertainty is wider still. The theorem says the estimate is not too low on "
            "average; twenty-five correlated rows say little more than that."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def bg_theorem(self):
        st = VGroup(MathTex(r"\mathbb E\bigl[\alpha^{\text{net}}_{t+1} \mid \mathcal F_t\bigr] = 0\ \ \Rightarrow\ \ "
                            r"\text{Cov}\bigl(\alpha^{\text{net}}_{t+1},\ X_t\bigr) = 0\ \ \text{for every } X_t \in \mathcal F_t",
                            font_size=30),
                    wrapped_label(r"in Berk and Green's market, investors' net alpha is a martingale difference: nothing "
                                  r"public, past returns included, predicts it; skill shows up as size, not as persistence",
                                  9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"No persistence for investors (after Berk and Green 2004)", st, r"this part's proof",
                            width=11.8, font_size=22)
        with self.voiceover(
            "The second theorem, for Chapter three. <bookmark mark='a'/> In Berk and Green's market, investors' net "
            "alpha next year has expectation zero given everything public today, so it is uncorrelated with anything "
            "public, including past returns. <bookmark mark='b'/> Skill is real and shows up as size, not as "
            "persistence in what investors earn."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def bg_proof(self):
        rows = [cmath(r"A_t", r"=", r"\frac{\mathbb E_t[a] - f}{b}\quad (A_t > 0)", font_size=40, colors={r"A_t": ACT_C}),
                cmath(r"\alpha^{\text{net}}_{t+1}", r"=", r"a - bA_t - f + \varepsilon_{t+1} = \bigl(a - \mathbb E_t[a]\bigr) + \varepsilon_{t+1}",
                      font_size=34),
                cmath(r"\mathbb E_t\bigl[a - \mathbb E_t[a]\bigr]", r"=", r"0,\quad \mathbb E_t[\varepsilon_{t+1}] = 0", font_size=38),
                cmath(r"\Rightarrow", r"", r"\mathbb E[\alpha^{\text{net}}_{t+1} X_t] = \mathbb E\bigl[X_t\,\mathbb E_t[\alpha^{\text{net}}_{t+1}]\bigr] = 0",
                      font_size=34, colors={r"\Rightarrow": GOOD})]
        whys = [why(r"competitive flows: the fund grows until the expected net alpha after fees is zero"),
                why(r"substitute the size: the scale cost and the fee cancel the expected skill"),
                why(r"the investors' posterior mean is their best guess, so its error has mean zero given their "
                    r"information; the return noise is independent of it"),
                why(r"by the tower property, for any public $X_t$; with $X_t$ last year's return, no persistence")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof, in four lines. <bookmark mark='a'/> Competitive flows set the fund's size so that the expected "
            "net alpha is zero. <bookmark mark='b'/> Substitute it: what is left of next year's net alpha is the error "
            "in investors' estimate of skill, plus noise. <bookmark mark='c'/> The posterior mean is investors' best "
            "guess, so its error has mean zero given what they know. <bookmark mark='d'/> And by the tower property, "
            "anything they know, last year's return included, is uncorrelated with it. The fair game of Part one, "
            "reappearing as an equilibrium."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def bg_check(self, b):
        rows = VGroup(
            label(rf"with flows: next year's net alpha on this year's, slope {b['slope']:+.3f} $\pm$ {b['se']:.3f}", font_size=23,
                  color=ACT_C),
            label(rf"without flows, sizes fixed: slope {b['slope_fixed']:.3f} $\pm$ {b['se_fixed']:.3f}", font_size=23,
                  color=SKILL_C),
            label(rf"theory without flows: $\sigma_a^2/(\sigma_a^2 + \sigma_\varepsilon^2)$ = {b['theory_fixed']:.3f}", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        note_ = label(rf"400 simulated managers, {comma(b['n'])} fund-years with assets in both years", font_size=16,
                      color=GREY_B).to_edge(DOWN, buff=0.6)
        s1, e1, s2, th = b["slope"], b["se"], b["slope_fixed"], b["theory_fixed"]
        with self.voiceover(
            "The check, in Chapter three's simulation. <bookmark mark='a'/> Regress each fund's net alpha next year on "
            f"this year's: a slope of {s1:+.3f}, with a standard error of {e1:.3f}. No persistence, as the theorem says. "
            "<bookmark mark='b'/> Now remove the flows: every fund keeps the same size. The slope becomes "
            f"{s2:.3f}. <bookmark mark='c'/> And the theory for that world, the share of a fund's return variance that "
            f"is skill, gives {th:.3f}. The same managers, the same skill: persistence appears or vanishes with the "
            "flows."
        ) as vo:
            self.play(FadeIn(note_))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def qvalues(self):
        cards = VGroup(
            desk_question(r"Part 25 stated it; this chapter proved it", r"Storey's conservativeness, its exact bias, "
                          r"its behaviour under dependence, and its consequence for counting skill", width=12.4,
                          font_size=19),
            desk_question(r"$q$-values", r"Storey's $q$-value for a fund is the smallest false discovery rate at which "
                          r"it would be declared skilled: a ranking with an error rate attached", width=12.4, font_size=19),
            desk_question(r"two theorems, one message", r"skill can be counted but rarely identified, and where it "
                          r"exists, competition moves its reward from investors to managers", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How the two theorems fit together. <bookmark mark='a'/> Part twenty-five stated Storey's estimate; this "
            "chapter proved its bias, its behaviour under dependence, and what it implies for counting skill. "
            "<bookmark mark='b'/> In practice it gives each fund a q-value, the smallest false discovery rate at which "
            "it would be called skilled. <bookmark mark='c'/> And with Berk and Green: skill can be counted but rarely "
            "identified, and where it exists, competition moves its reward from investors to managers."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"false discovery rates", r"Benjamini and Hochberg (1995) control the expected share of false "
                          r"discoveries; Storey's $q$-values sharpen it with $\hat\pi_0$", width=12.4, font_size=19),
            desk_question(r"in finance", r"Harvey, Liu and Zhu (2016): a $t$ of 3, not 2, for new factors; Barras, "
                          r"Scaillet and Wermers for funds; Chen and Zimmermann on how many anomalies replicate",
                          width=12.4, font_size=19),
            desk_question(r"empirical Bayes", r"Efron's local false discovery rate: the probability that this fund, "
                          r"with this $t$, is a null; Part 25's shrinkage is its cousin", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where this connects. <bookmark mark='a'/> Yoav Benjamini and Yosef Hochberg's false discovery rate, which "
            "Storey's estimate sharpens. <bookmark mark='b'/> In finance: Campbell Harvey, Yan Liu and Heqing Zhu's "
            "higher bar for new factors, Barras, Scaillet and Wermers for funds, and work on how many published "
            "anomalies replicate. <bookmark mark='c'/> And Bradley Efron's local false discovery rate: the probability "
            "that this particular fund is a null, a cousin of Part twenty-five's shrinkage."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"dependence", r"estimators of $\pi_0$ and the false discovery rate whose variance is "
                          r"controlled when every test shares the same market", width=12.4, font_size=19),
            desk_question(r"time-varying skill", r"skill that appears and decays, as Chapter 4's markets adapt: a share "
                          r"of skilled funds that is not a constant", width=12.4, font_size=19),
            desk_question(r"the researcher's own garden", r"applying the same counting to a research programme: how many "
                          r"of a field's published results are nulls", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open problems. <bookmark mark='a'/> Estimators whose variance stays controlled when every test shares "
            "one market. <bookmark mark='b'/> Skill that comes and goes, as adaptive markets would predict. "
            "<bookmark mark='c'/> And turning the counting on research itself: how many of a field's published results "
            "are nulls."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House's 25 rows are correlated. Does that bias Storey's estimate of their null share up, "
                       r"down, or neither?")
        with self.voiceover(
            "Pause and predict. The House's twenty-five rows are correlated. Does that bias Storey's estimate of their "
            "null share up, down, or neither?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
