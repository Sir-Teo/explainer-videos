from __future__ import annotations

from math import comb

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403

NAMES = {"mom": r"$2\bar x - 1$", "max": r"$m$ \ (MLE)", "umvue": r"$m(1 + \tfrac1k) - 1$", "range": r"$(m - m_1)\tfrac{k+1}{k-1} - 1$"}
COLS = {"mom": MOM, "max": MAX, "umvue": UMVUE, "range": S.PRIOR}
MODELS = [("uniform", (r"the textbook:", r"uniform capture")), ("newer", (r"newer tanks captured", r"relative capture weights \ from 1 to 3")),
          ("offset", (r"serials start", r"at 1{,}001"))]


class Compare(VoiceoverScene):
    def construct(self):
        self.card()
        self.board()
        self.multiplier()
        self.game()
        self.lessons()

    def card(self):
        card = chapter_card(11, r"Comparing estimators", r"Which recipe would you send to war?", part=PART)
        with self.voiceover("Chapter eleven. Comparing estimators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def board(self):
        d = load("board")
        rows_ = d["rows"]
        xs = [-1.2, 2.2, 5.3]
        ys = {e: 1.0 - 0.95 * i for i, e in enumerate(("mom", "max", "umvue", "range"))}
        heads = VGroup(*[VGroup(*[label(x, font_size=22, color=GREY_A) for x in t]).arrange(DOWN, buff=0.08).move_to([xs[j], 2.35, 0])
                         for j, (_, t) in enumerate(MODELS)])
        names = VGroup(*[label(NAMES[e], font_size=24, color=COLS[e]).move_to([-4.9, ys[e], 0]) for e in ys])
        for nm in names:
            if nm.width > 3.0:
                nm.width = 3.0
        line = Line([-6.4, 1.75, 0], [6.6, 1.75, 0], color=GREY_D)
        cols = VGroup()
        for j, (mname, _) in enumerate(MODELS):
            col = VGroup()
            best = min(rows_[mname], key=lambda e: rows_[mname][e]["rmse"])
            for e in ys:
                r = rows_[mname][e]
                rm = MathTex(rf"{r['rmse']:,.0f}".replace(",", "{,}"), font_size=34, color=S.ACCENT if e == best else WHITE)
                sub = MathTex(rf"\text{{bias}}\ {r['bias']:+,.0f}".replace(",", "{,}") + rf",\ \text{{SD}}\ {r['sd']:.0f}", font_size=20,
                              color=GREY_B)
                cell = VGroup(rm, sub).arrange(DOWN, buff=0.08).move_to([xs[j], ys[e], 0])
                if e == best:
                    cell.add(SurroundingRectangle(cell, color=S.ACCENT, buff=0.08, corner_radius=0.08))
                col.add(cell)
            cols.add(col)
        head = label(r"RMSE, \ $N = 300$, \ $k = 5$ tanks", font_size=24, color=GREY_B).move_to([-4.9, 2.4, 0])
        tag = simulated_tag(r"simulated: \ 10,000 factories per model", corner=DR)
        with self.voiceover(
            "Time to compare the recipes, and to test them on more than the textbook model. Here's an MSE board: four "
            "estimators, each graded on ten thousand factories with three hundred tanks, five captured, under three "
            "different worlds. The big number is the root mean squared error; underneath are the bias and the "
            "standard deviation. We've added a fourth recipe, built from the range between the smallest and largest "
            "serial, for a reason that will become clear. <bookmark mark='a'/> In the textbook world, where every tank "
            "is equally likely to be captured, the best unbiased estimator wins, at fifty. The maximum is biased low, "
            "the moment estimator is noisy, and the range estimator is noisier still, since it uses two order "
            "statistics and an assumption less. <bookmark mark='b'/> Now suppose newer tanks, the ones with higher "
            "serials, are more likely to be at the front and so more likely to be captured, with sequential sampling weights up to three times as large. These are sampling weights, not an exact ratio of marginal inclusion probabilities. Every estimator is pushed upward. The moment estimator is now biased by nearly fifty. The best "
            "unbiased estimator is biased too, by sixteen, but it still wins on error. "
            "<bookmark mark='c'/> Finally, suppose the numbering doesn't start at one, but at a thousand and one, and "
            "nobody told us. Every estimator that assumed a start at one is off by hundreds or thousands. Only the "
            "range estimator, which never assumed where the numbers start, is still right on average, with the same "
            "error of about eighty it had everywhere else."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(names), Create(line), FadeIn(head), FadeIn(tag))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cols[k]], lag_ratio=0.2))
        self.clear_scene()

    def multiplier(self):
        N, k = 300, 5
        js = np.arange(k, N + 1)
        pm = np.array([comb(int(j) - 1, k - 1) for j in js], float) / comb(N, k)
        Em, Em2 = (pm * js).sum(), (pm * js ** 2).sum()
        a_s = np.linspace(1.0, 1.4, 200)
        rmse = np.sqrt(np.array([(pm * (a * js - 1 - N) ** 2).sum() for a in a_s]))
        a_opt = (N + 1) * Em / Em2
        r_opt = np.sqrt((pm * (a_opt * js - 1 - N) ** 2).sum())
        a_u = 1 + 1 / k
        r_u = np.sqrt((pm * (a_u * js - 1 - N) ** 2).sum())
        A = axes([1.0, 1.4], [40, 80], x_length=7.2, y_length=4.4, xlabel=r"multiplier $a$ in $a\,m - 1$, \ $k = 5$",
                 ylabel=r"RMSE, \ exact, \ $N = 300$", xticks=[1.0, 1.1, 1.2, 1.3, 1.4], yticks=[40, 50, 60, 70, 80],
                 center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = clip_curve(ax, a_s, rmse, LIK, 3.5, ymin=40, ymax=80)
        pu = VGroup(Dot(ax.c2p(a_u, r_u), radius=0.09, color=UMVUE),
                    MathTex(rf"\text{{UMVUE}}:\ {r_u:.1f}", font_size=24, color=UMVUE).next_to(ax.c2p(a_u, r_u), DR, buff=0.12))
        po = VGroup(Dot(ax.c2p(a_opt, r_opt), radius=0.09, color=S.ACCENT),
                    MathTex(rf"a^* = {a_opt:.3f}:\ {r_opt:.1f}", font_size=24, color=S.ACCENT).next_to(ax.c2p(a_opt, r_opt), DL, buff=0.12))
        rows = fit_rows(VGroup(
            MathTex(r"\mathrm{MSE}(a) = \sum_j P_N(m = j)\,(a j - 1 - N)^2", font_size=26),
            MathTex(r"a^* = \frac{(N + 1)\,E_N m}{E_N m^2}", font_size=28),
            MathTex(r"a^* \approx \frac{k + 2}{k + 1} = 1.167", font_size=28, color=S.ACCENT),
            label(r"shrink the UMVUE a little:", font_size=24, color=GREY_A),
            label(r"biased, \ and slightly better \ (here by 1.5\%)", font_size=24, color=GREY_A),
        ), 5.0, 0.34, [4.4, -0.3, 0])
        with self.voiceover(
            "Is the best unbiased estimator the best, full stop? <bookmark mark='a'/> Consider every recipe of the "
            "form a times the maximum, minus one. The maximum's distribution is known exactly, so each recipe's mean "
            "squared error can be computed exactly, with no simulation. <bookmark mark='b'/> The unbiased choice, a "
            "equals one plus one over k, gives fifty point four. <bookmark mark='c'/> But the minimum is a "
            "little to the left, at a multiplier close to k plus two over k plus one. That recipe is biased low, "
            "slightly, and its error is slightly smaller, forty-nine point seven. And a star barely depends on N, so the shrunken recipe can be approximated without knowing N by the fixed multiplier k plus two over k plus one. The exact optimum shown still uses the simulated truth. <bookmark mark='d'/> Part 8's lesson again: accepting a little bias can buy a little "
            "variance. Here the gain is small, about one and a half percent. The big differences on the board came from the model, "
            "not from bias."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(cv))
            vo.wait_until("b")
            self.play(FadeIn(pu))
            vo.wait_until("c")
            self.play(FadeIn(po), FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def game(self):
        lines = [
            "from explainer.stats.kit.estimation import tank_game",
            "",
            "def mine(s):       # one row of serials per factory",
            "    m = s.max(1)",
            "    return m + m / s.shape[1]     # your recipe",
            "",
            "tank_game(mine, N=300, k=6, reps=10_000)",
            "# {'bias': 1.5, 'sd': 42.3, 'rmse': 42.3, ...}",
            "tank_game(mine, model=\"newer\")  # a world it did not assume",
        ]
        code = code_block(lines, font_size=22).move_to([0, 0.6, 0])
        frame = SurroundingRectangle(code, color=GREY_D, buff=0.3, corner_radius=0.12)
        head = label(r"Built: \ the tank factory game", font_size=34, color=S.ACCENT).to_edge(UP, buff=0.4)
        foot = fit_rows(VGroup(
            label(r"any recipe, \ any $N$ and $k$, \ three worlds: \ bias, \ SD, \ RMSE, \ bias and RMSE with Monte Carlo errors; SD as a point estimate", font_size=24),
            label(r"\texttt{explainer/stats/kit/estimation.py}: \ also Newton's method and the observed information", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And here is the game, built into statkit, so you can play it yourself. "
            "<bookmark mark='b'/> Write any recipe as a function of the captured serials, one row per factory. This "
            "one is the maximum plus the maximum over k, a near-miss of the best unbiased estimator. "
            "<bookmark mark='c'/> The game simulates ten thousand factories and grades the recipe, reporting its bias, "
            "its standard deviation and its root mean squared error, with Monte Carlo standard errors for bias and RMSE, as Part 7 insisted; SD is reported as a point estimate. <bookmark mark='d'/> And you can grade it on worlds it didn't assume. Try to beat forty-two "
            "under the textbook model. The theory of this part says you can't with an unbiased recipe, while within the multiplier family shown, a modest shrinkage buys a small gain here. A biased estimator can do much better at a particular N and worse elsewhere."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(frame), FadeIn(code[:6], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(code[6:8], lag_ratio=0.2), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(code[8:]), FadeIn(foot[1]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"efficiency is bought with assumptions", font_size=32, color=S.ACCENT),
            VGroup(label(r"the UMVUE is best when serials start at 1 and capture is uniform;", font_size=26),
                   label(r"the range estimator gives up 60\% more RMSE to survive an unknown start", font_size=26)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            VGroup(label(r"Ruggles \& Brodie's real work was learning the numbering:", font_size=26, color=GREY_A),
                   label(r"blocks by maker, \ codes on gearboxes and wheel moulds, \ serials never used", font_size=26, color=GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            label(r"misspecified models: \ the MLE still estimates something, \ the KL-closest member (Part 22)", font_size=26,
                  color=GREY_A),
            label(r"robust statistics: \ estimators that degrade gracefully (Part 30)", font_size=26, color=GREY_A),
        ), 12.6, 0.45, [0, 0.0, 0])
        intro = label('Accuracy depends on the model assumptions', font_size=36)
        with self.voiceover(
            "What does the board teach? <bookmark mark='a'/> Efficiency is bought with assumptions. "
            "<bookmark mark='b'/> The best unbiased estimator is the best only in the world it was derived for, where "
            "serials start at one and every tank is equally likely to be caught. The range estimator gives up sixty "
            "percent more error to survive not knowing where the numbers start. Which to use is a judgement about which "
            "world you're in. <bookmark mark='c'/> The wartime statisticians knew this. Much of their real work was "
            "learning how the Germans numbered things: blocks of serials allotted to each manufacturer, codes stamped on "
            "gearboxes, and wheel moulds that could be counted directly. <bookmark mark='d'/> When the model is wrong, "
            "maximum likelihood still estimates something: the member of the model closest to the truth in "
            "Kullback–Leibler divergence, which Part 22 makes precise. <bookmark mark='e'/> And estimators designed to "
            "degrade gracefully when the model is a little wrong are the subject of robust statistics, in Part 30."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
