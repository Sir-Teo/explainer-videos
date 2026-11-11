from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, ask, comma, illustration, load


class Reality(VoiceoverScene):
    def construct(self):
        r = load("rc")
        self.card()
        self.null()
        self.bootstrap()
        self.rc_formula()
        self.dists(r)
        self.spa_rw()
        self.table(r)
        self.question()

    def card(self):
        c = chapter_card(11, r"Reality checks", r"Is the best rule better than the best of many useless ones?",
                         lit=(2000,), part=PART)
        with self.voiceover("Chapter eleven. Halbert White's reality check for data snooping, and the two tests that "
                            "improved on it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def null(self):
        rows = [cmath(r"d_{k,t}", r"=", r"r^{(k)}_t - r^{\text{bench}}_t", font_size=40, colors={r"d_{k,t}": RULE}),
                cmath(r"H_0", r":", r"\ \max_{k \le N}\ \mathbb{E}\,d_{k,t} \le 0", font_size=40, colors={r"H_0": BAD}),
                cmath(r"V", r"=", r"\sqrt{T}\,\max_k \bar d_k", font_size=40, colors={r"V": HURDLE})]
        whys = [why(r"each rule's daily return over the benchmark; here the benchmark is cash, so $d$ is the rule's "
                    r"excess return"),
                why(r"the null that matters after a search: not that one rule has no edge, but that none of the $N$ does. "
                    r"The test is of the whole universe at once"),
                why(r"the statistic is the best rule's mean, scaled. Its null distribution depends on how the $N$ rules "
                    r"are correlated, which no formula knows, so it is bootstrapped")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.45, edge=6.9)
        with self.voiceover(
            "White's idea, in 2000, was to test the right null hypothesis. <bookmark mark='a'/> For each of N rules, take "
            "its return over a benchmark, day by day. <bookmark mark='b'/> After a search, the question is not whether "
            "one rule has an edge, but whether any of the N does; the null is that the best of them has none. "
            "<bookmark mark='c'/> The natural statistic is the best rule's average, scaled by the square root of T. Its "
            "distribution under the null depends on how all N rules move together, which no formula knows, so White "
            "bootstrapped it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def bootstrap(self):
        rng = np.random.default_rng(5)
        T = 40
        W = 12.0 / T
        orig = VGroup(*[Rectangle(width=W * 0.92, height=0.5, stroke_width=0,
                                  fill_color=interpolate_color(ManimColor(IS_C), ManimColor(OOS_C), i / T),
                                  fill_opacity=0.85) for i in range(T)]).arrange(RIGHT, buff=W * 0.08).move_to(UP * 1.8)
        lab1 = label(r"the $T$ days, in order", font_size=18, color=GREY_A).next_to(orig, UP, buff=0.15)
        idx, t = [], 0
        while len(idx) < T:
            start = int(rng.integers(T))
            L = int(rng.geometric(0.15))
            idx += [(start + j) % T for j in range(L)]
        idx = idx[:T]
        res = VGroup(*[orig[i].copy() for i in idx]).arrange(RIGHT, buff=W * 0.08).move_to(DOWN * 0.4)
        lab2 = label(r"one resample: blocks of random length (mean 10 days), from random starting days, wrapping round",
                     font_size=18, color=GREY_A).next_to(res, DOWN, buff=0.2)
        foot = wrapped_label(r"Politis and Romano's stationary bootstrap keeps each block's days together, and so keeps the "
                             r"autocorrelation that a day-by-day resample would destroy. Every rule is resampled on the "
                             r"same days, so their correlation survives too", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The bootstrap has to respect two kinds of dependence. <bookmark mark='a'/> Through time: returns cluster, "
            "and some of these rules depend on autocorrelation, so resampling single days would destroy what is being "
            "tested. Dimitris Politis and Joseph Romano's stationary bootstrap resamples blocks of random length, here "
            "ten days on average, from random starting points. <bookmark mark='b'/> And across rules: every rule is "
            "resampled on the same days, so their correlation is kept. Each resample gives every rule a new average, "
            "and the best of them, recentred, is one draw of the statistic under the null."
        ) as vo:
            self.play(FadeIn(orig), FadeIn(lab1))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(orig[i], res[k]) for k, i in enumerate(idx)], lag_ratio=0.03),
                      run_time=3)
            self.play(FadeIn(lab2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def rc_formula(self):
        rows = [cmath(r"\bar d^{\,*}_{k,b}", r"=", r"\tfrac1T \textstyle\sum_t d_{k,\tau_b(t)}", font_size=38,
                      colors={r"\bar d^{\,*}_{k,b}": OOS_C}),
                cmath(r"V^*_b", r"=", r"\sqrt{T}\,\max_k \big(\bar d^{\,*}_{k,b} - \bar d_k\big)", font_size=38,
                      colors={r"V^*_b": HURDLE}),
                cmath(r"p", r"=", r"\tfrac1B \textstyle\sum_b \mathbb{1}\{V^*_b \ge V\}", font_size=40, colors={r"p": BAD})]
        whys = [why(r"rule $k$'s average on bootstrap resample $b$; $\tau_b$ are the resampled days. Computed for all "
                    r"10{,}000 rules at once: a matrix of day counts times the matrix of returns"),
                why(r"recentred at each rule's own sample mean, which imposes the null: every rule's edge is set to zero, "
                    r"and only the luck of the draw remains"),
                why(r"White's (2000) reality-check $p$-value: how often the best of $N$ rules with no edge looks as good "
                    r"as the best of the real ones. $B = 500$ resamples, as in Sullivan, Timmermann and White")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.45, edge=6.9)
        with self.voiceover(
            "In symbols. <bookmark mark='a'/> On each resample b, every rule gets a new average. For ten thousand rules "
            "this is one matrix product, the resample's day counts times the returns. <bookmark mark='b'/> Subtract each "
            "rule's own sample mean, which imposes the null by setting every edge to zero, and take the best. "
            "<bookmark mark='c'/> The p-value is how often that best-of-N luck matches the real best. Five hundred "
            "resamples, as Sullivan, Timmermann and White used."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def dists(self, r):
        panels = VGroup()
        for era, title, col in (("in", r"1926--1986", IS_C), ("out", r"1987--2020", OOS_C)):
            a = r[era]
            e = np.asarray(a["Vb_edges"])
            h = np.asarray(a["Vb_hist"], float)
            c = (e[:-1] + e[1:]) / 2
            xmax = max(e[-1], a["V"]) * 1.1
            top = h.max() * 1.15
            g = axes([0, xmax], [0, top], x_length=5.4, y_length=3.2, xlabel=r"$V^*$: the best of 10{,}000, by luck",
                     ylabel=r"resamples", xticks=[], yticks=[], font_size=12)
            ax = g.ax
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=NOISE, fill_opacity=0.7).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
            lv = Line(ax.c2p(a["V"], 0), ax.c2p(a["V"], top), color=col, stroke_width=3)
            cap = VGroup(label(title, font_size=20, color=col),
                         MathTex(rf"p = {a['rc_p']:.3f}", font_size=26, color=GOOD if a["rc_p"] < 0.05 else BAD)).arrange(
                RIGHT, buff=0.4)
            panels.add(VGroup(cap, VGroup(g, bars, lv)).arrange(DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.1)
        foot = wrapped_label(r"grey: the bootstrap distribution of the best recentred rule; the line: the real best. "
                             r"500 stationary-bootstrap draws, mean block length 10. Zero means 0/500 exceedances, not zero true probability. Original sample-SD studentisers are not estimated serial long-run standard errors; validity needs bootstrap assumptions.", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"The original reality check uses five hundred stationary-bootstrap draws. <bookmark mark='a'/> The earlier bootstrap exceedance fraction is {r['in']['rc_p']:.3f}; zero means zero out of five hundred, not zero true probability. This random rule universe and market series are not an exact replication of the cited Dow study. <bookmark mark='b'/> The later fraction is {r['out']['rc_p']:.3f}. Nonrejection does not prove all rules useless or establish equivalence. Stationarity, moment and resampling assumptions, the original studentisation choices and Monte Carlo uncertainty all limit interpretation."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.add(illustration(r"the House's \texttt{backtest.reality\_check}, $B = 500$"))
        self.wait(0.4)
        self.clear_scene()

    def spa_rw(self):
        cards = VGroup(
            desk_question(r"Hansen's SPA (2005)", r"studentise each rule by its own volatility, so a quiet rule's average "
                          r"counts for more; and stop rules that are clearly worse than the benchmark from widening the "
                          r"null. More power, and less sensitive to adding bad rules", width=12.2, font_size=19),
            desk_question(r"Romano and Wolf's step-down (2005)", r"step-down joint hypothesis testing: "
                          r"reject every rule above the bootstrap's critical value, remove them, recompute the critical "
                          r"value for those left, repeat. asymptotic familywise control needs valid studentisation and bootstrap assumptions", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Two refinements motivate the next diagnostics. <bookmark mark='a'/> Hansen's superior predictive ability approach studentises and reduces the influence of clearly inferior rules on the bootstrap null. Proper time-series inference needs suitable long-run variance and bootstrap regularity conditions. <bookmark mark='b'/> Romano and Wolf's step-down method repeatedly compares remaining statistics with bootstrap critical values. Familywise error control is an asymptotic result under appropriate assumptions, not an unconditional finite-sample promise. The unchanged House implementation uses sample standard deviations and five hundred resamples; its reported results are simplified approximations to those methods."
        ) as vo:
            for k, mk in enumerate(("a", "b")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def table(self, r):
        a, b = r["in"], r["out"]
        head = VGroup(*[label(h, font_size=18, color=GREY_A) for h in (r"", r"1926--1986", r"1987--2020")])
        data = [
            (r"the best rule's $t$, nominal", f"{a['best_t']:.1f}", f"{b['best_t']:.1f}", None),
            (r"rules with $t > 1.96$", comma(a["n_t2"]), comma(b["n_t2"]), None),
            (r"White's reality check, $p$", f"{a['rc_p']:.3f}", f"{b['rc_p']:.3f}", True),
            (r"Hansen's SPA, $p$", f"{a['spa_p']:.3f}", f"{b['spa_p']:.3f}", True),
            (r"Romano--Wolf: step-down rejections", str(a["rw_n"]), str(b["rw_n"]), False),
        ]
        rows = [head]
        for t, x, y, isp in data:
            def col(v):
                if isp is None:
                    return WHITE
                if isp:
                    return GOOD if float(v) < 0.05 else BAD
                return GOOD if int(v) > 0 else BAD
            rows.append(VGroup(label(t, font_size=19, color=RULE), MathTex(x, font_size=26, color=col(x)),
                               MathTex(y, font_size=26, color=col(y))))
        xs = [-4.0, 1.0, 4.4]
        for j, row in enumerate(rows):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.4 - 0.72 * j, 0])
            if j:
                row[0].align_to(np.array([xs[0] - 2.4, 0, 0]), LEFT)
        foot = wrapped_label(rf"after 1986, {b['n_t2']} rules clear the textbook hurdle on their own, about what ten "
                             r"thousand rules with no edge would produce, and none survives the step-down. Before 1987, "
                             rf"{a['rw_n']} do, {a['rw_families']['cb']} of them channel breakouts",
                             12.0, 18, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"The original procedures yield different research-era diagnostics. <bookmark mark='a'/> Earlier RC and SPA exceedance fractions are {a['rc_p']:.3f} and {a['spa_p']:.3f}, while the saved step-down algorithm rejects {a['rw_n']} rules. Model-based rejection does not identify individually true effects with certainty. <bookmark mark='b'/> Later RC and SPA fractions are {b['rc_p']:.3f} and {b['spa_p']:.3f}, with {b['rw_n']} step-down rejections. These are gross returns relative to cash, not market-active performance. Sample-standard-deviation studentisers do not estimate serial long-run variance; finite-bootstrap results remain approximate, with no exact paper-replication or future-profit guarantee."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows[1:]], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"you add 5,000 deliberately terrible rules (each the negative of a good one) to the universe. What "
                r"happens to White's $p$-value, and to Hansen's?".replace("5,000", "5{,}000"))
        with self.voiceover(
            "Pause and predict. You add five thousand deliberately terrible rules to the universe, each the mirror "
            "image of a good one. What happens to White's p-value, and to Hansen's?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
