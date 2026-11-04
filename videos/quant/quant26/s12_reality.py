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
                             r"Before 1987 the real best is three times beyond anything luck produced; after, it sits at "
                             r"the edge of luck", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The reality check on the ten thousand rules. <bookmark mark='a'/> In the first era, the real best rule "
            "lies far beyond anything the bootstrap's luck produced: the p-value is zero, as Sullivan, Timmermann and "
            "White found for the Dow before 1987. <bookmark mark='b'/> In the second era the real best sits at the edge "
            "of the luck distribution, with a p-value of point zero five six. Ten thousand rules, thirty-four years, "
            "and the best of them is not distinguishable from the best of ten thousand useless ones."
        ) as vo:
            vo.wait_until("a")
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
            desk_question(r"Romano and Wolf's step-down (2005)", r"not only `is the best real?' but `which ones are?': "
                          r"reject every rule above the bootstrap's critical value, remove them, recompute the critical "
                          r"value for those left, repeat. The familywise error rate stays at 5\%", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Two refinements followed in 2005. <bookmark mark='a'/> Peter Hansen's test for superior predictive ability "
            "divides each rule by its own volatility, so that a quiet rule's average counts for more, and it stops "
            "rules that are clearly worse than the benchmark from padding the null distribution, which White's test "
            "allows. <bookmark mark='b'/> And Joseph Romano and Michael Wolf asked a better question: not whether the "
            "best rule is real, but which rules are. Their step-down procedure rejects every rule above the "
            "bootstrap's critical value, removes them, recomputes the critical value for those that remain, and "
            "repeats, keeping the chance of any false rejection at five percent."
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
            (r"Romano--Wolf: rules found real", str(a["rw_n"]), str(b["rw_n"]), False),
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
            row[0].align_to(np.array([xs[0] - 2.4, 0, 0]), LEFT)
        foot = wrapped_label(rf"after 1986, {b['n_t2']} rules clear the textbook hurdle on their own, about what ten "
                             r"thousand rules with no edge would produce, and none survives the step-down. Before 1987, "
                             rf"{a['rw_n']} do, {a['rw_families']['cb']} of them channel breakouts",
                             12.0, 18, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "All three, in both eras. <bookmark mark='a'/> Before 1987 every test agrees: the best rule's t-statistic "
            "is thirteen and a half, both p-values are zero, and Romano and Wolf find a hundred and fifty-three rules "
            "that are individually real. <bookmark mark='b'/> After 1986, two hundred and fourteen rules clear the "
            "textbook hurdle of two on their own, about what ten thousand rules with no edge would produce. The best has "
            "a t of three point three. White's p-value is point zero five six, Hansen's point four seven, and Romano and "
            "Wolf find none. Sullivan, Timmermann and White reached the same verdict with the Dow in 1999: the rules "
            "had worked, and they had stopped."
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
