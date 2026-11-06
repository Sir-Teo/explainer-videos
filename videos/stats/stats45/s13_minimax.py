from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class NormalMeans(VoiceoverScene):
    def construct(self):
        self.card()
        self.baranchik()
        self.factors()
        self.strawderman()
        self.risks()
        self.table()
        self.lesson()

    def card(self):
        card = chapter_card(12, r"Minimaxity and admissibility for normal means", r"Better than $X$, \ and beyond improvement", lit=(1971,), part=PART)
        with self.voiceover("Chapter twelve. Minimaxity and admissibility in the normal-means problem: better than X, and beyond improvement."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def baranchik(self):
        rows = [
            cmath(r"\delta_r(x)", r"=", r"\Big(1 - r(s)\tfrac{p - 2}{s}\Big) x, \ \ s = \|x\|^2", font_size=34),
            cmath(r"\mathrm{SURE}", r"=", r"p - (p - 2)^2 \tfrac{r(s)(2 - r(s))}{s} - 4(p - 2)\, r'(s)", font_size=32),
            cmath(r"0 \le r \le 2, \ r \uparrow", r"\Rightarrow", r"\mathrm{SURE} \le p: \ \delta_r \text{ is minimax}", font_size=32),
            cmath(r"r \equiv 1", r":", r"\text{James--Stein; } \ \ r(s) = \min(1, \tfrac{s}{p - 2}): \ \text{the positive part}", font_size=30),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(ADMC)
        whys = [why(r"a family of shrinkers"), why(r"chapter 10's identity"), why(r"Baranchik (1970)"), why(r"two members")]
        with self.voiceover(
            "<bookmark mark='a'/> X is minimax, with constant risk p, so any estimator whose risk never exceeds p is "
            "minimax too. Alexander Baranchik's family shrinks by r of s times p minus two over s, where s is the squared "
            "length of x. <bookmark mark='b'/> Chapter ten's SURE, worked out for this correction, is p minus two terms: one "
            "proportional to r times two minus r, and one to the derivative of r. <bookmark mark='c'/> So if r stays "
            "between zero and two and never decreases, SURE is at most p for every data set, and every such rule is "
            "minimax. <bookmark mark='d'/> r equal to one is James–Stein; capping the shrinkage at x itself gives the "
            "positive part. A whole family of estimators beats X, and they compete among themselves."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def factors(self):
        d = load("minimax")
        s = np.asarray(d["s"])
        A = axes([0, 30], [-1.5, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$s = \|x\|^2$", ylabel=r"shrinkage factor",
                 xticks=[0, 10, 20, 30], yticks=[-1, 0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        raw = clip_curve(ax, s, d["shrink_js_raw"], INADC, 4, ymin=-1.5)
        plus = polyline(ax, s, d["shrink_js"], MMC, 4)
        st = polyline(ax, s, d["shrink_straw"], JSC, 4)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"$p = {d['p']}$: \ the factor multiplying $x$", font_size=22),
            label(r"red: \ James--Stein, \ negative when $s < p - 2$", font_size=22, color=INADC),
            label(r"gold: \ the positive part, \ a kink at $s = p - 2$", font_size=22, color=MMC),
            label(r"green: \ Strawderman: \ smooth, \ in $(0, 1)$", font_size=22, color=JSC),
            label(r"Brown: \ admissible rules are smooth", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Compare the factors by which three of them multiply x, in {d['p']} dimensions. <bookmark "
            f"mark='b'/> James–Stein's factor goes negative when the squared length of x is below p minus two, flipping the "
            f"estimate through the origin, which is absurd. <bookmark mark='c'/> The positive part clips it at zero, leaving "
            f"a kink. <bookmark mark='d'/> In green, the posterior mean under a proper prior due to William Strawderman: "
            f"smooth, and always strictly between zero and one. <bookmark mark='e'/> Brown showed that admissible "
            f"estimators in this problem are smooth, generalized Bayes rules, so the positive part's kink is a sign of its "
            f"inadmissibility."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(exact_tag(r"exact: \ incomplete gamma functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(raw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(plus), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(st), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def strawderman(self):
        d = load("minimax")
        rows = [
            cmath(r"\theta \mid \lambda", r"\sim", r"N\big(0, (\lambda^{-1} - 1) I\big), \ \ \lambda \sim (1 - a)\lambda^{-a} \text{ on } (0, 1]", font_size=30),
            cmath(r"X \mid \lambda", r"\sim", r"N(0, \lambda^{-1} I): \ \ E[\theta \mid x] = (1 - E[\lambda \mid x])\, x", font_size=30),
            cmath(r"E[\lambda \mid x]", r"=", r"\frac{\int_0^1 \lambda^{p/2 - a + 1} e^{-\lambda s/2} d\lambda}{\int_0^1 \lambda^{p/2 - a} e^{-\lambda s/2} d\lambda}", font_size=32),
            cmath(r"p \ge 5, \ 3 - p/2 \le a < 1", r"\Rightarrow", r"\text{proper Bayes, \ so admissible; \ and minimax}", font_size=30),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"a scale mixture of normals"), why(r"conjugate given $\lambda$"), why(r"incomplete gamma functions"), why(rf"Strawderman (1971); \ here $p = {d['p']}$, $a = {d['a']}$")]
        with self.voiceover(
            f"<bookmark mark='a'/> Strawderman's prior is a scale mixture of normals: given lambda, theta is normal with "
            f"variance one over lambda minus one, and lambda has a density proportional to lambda to the minus a on zero "
            f"to one. <bookmark mark='b'/> Given lambda, X is normal with variance one over lambda, and the posterior mean "
            f"shrinks x by the posterior mean of lambda. <bookmark mark='c'/> That is a ratio of two incomplete gamma "
            f"integrals. <bookmark mark='d'/> For a below one the prior is proper, so the rule is admissible; and in 1971 "
            f"Strawderman proved it minimax whenever p is at least five and a is at least three minus p over two. Here p is "
            f"five and a is one half: an estimator that beats X everywhere and cannot itself be beaten everywhere. His "
            f"construction needs at least five dimensions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def risks(self):
        d = load("minimax")
        nrm = np.asarray(d["nrm"])
        r = d["risks"]
        A = axes([0, 40], [0, 5.4], x_length=7.4, y_length=4.4, xlabel=r"$\|\theta\|^2$", ylabel=r"risk, \ $p = 5$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 1, 2, 3, 4, 5], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"mle": MLEC, "js": INADC, "jsplus": MMC, "bar": S.PRIOR, "straw": JSC}
        cs = {k: polyline(ax, nrm, r[k], c, 4) for k, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"blue: \ $X$, \ 5", font_size=22, color=MLEC),
            label(r"red: \ James--Stein; \ gold: \ positive part", font_size=22, color=INADC),
            label(r"purple: \ Baranchik, \ $r(s) = \min(1, s/(p + 1))$", font_size=22, color=S.PRIOR),
            label(rf"green: \ Strawderman: \ {r['straw'][0]:.2f} at $\theta = 0$", font_size=22, color=JSC),
            label(r"all minimax; \ none best everywhere", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Their risks in five dimensions, simulated with common random numbers. X has risk five. "
            f"<bookmark mark='b'/> James–Stein and its positive part are below it everywhere, the positive part most at the "
            f"origin. <bookmark mark='c'/> A Baranchik rule with a smooth, increasing r sits close to the positive part. "
            f"<bookmark mark='d'/> Strawderman's proper Bayes rule has risk {say(r['straw'][0], 1)} at the origin, far "
            f"below the others, and gives some of that back far away, though it stays under five. <bookmark mark='e'/> All "
            f"are minimax; none is below all the others everywhere. Among minimax rules, the choice is a choice of where to "
            f"spend the improvement, which is a prior belief in disguise."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 40,000 draws per point")))
            vo.wait_until("a")
            self.play(Create(cs["mle"]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["js"]), Create(cs["jsplus"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["bar"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["straw"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("minimax")
        r = d["risks"]
        nrm = np.asarray(d["nrm"])
        idx = [0, 2, 5, 10, 20]
        names = [("mle", r"$X$"), ("js", r"James--Stein"), ("jsplus", r"positive part"), ("bar", r"Baranchik"), ("straw", r"Strawderman")]
        rows = [[r"$\|\theta\|^2 =$"] + [f"{nrm[i]:.0f}" for i in idx]]
        for k, nm in names:
            rows.append([nm] + [f"{r[k][i]:.2f}" for i in idx])
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.28, colors=[GREY_A, MLEC, INADC, MMC, S.PRIOR, JSC]).move_to([0, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> In numbers, at five distances from the origin. <bookmark mark='b'/> At the origin the "
            f"proper Bayes rule's risk is {say(r['straw'][0], 1)}, against {say(r['jsplus'][0], 1)} for the positive part "
            f"and {say(r['js'][0], 1)} for James–Stein. <bookmark mark='c'/> At a squared distance of forty, every shrinker "
            f"is back near five, Strawderman's closest of all: it spent its improvement near the origin. The gains are large only where the prior, explicit or "
            f"implicit, puts its weight."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tab[2:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[t[-1] for t in tab[1:]]), color=S.ACCENT))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"shrink toward any point, \ or any subspace: \ the same theorem \ (Lindley 1962)", font_size=26),
            label(r"unequal variances, \ unknown $\sigma^2$: \ Berger (1976) and others", font_size=26, color=GREY_A),
            label(r"the guarantee is for the total loss: \ one coordinate can suffer", font_size=26, color=INADC),
            label(r"Efron \& Morris (1972): \ limited translation, \ cap each coordinate's shift", font_size=26, color=MMC),
            label(r"the Coverage Board, \ next: \ what shrinkage does to intervals", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theory extends in every direction. One can shrink toward any fixed point, or toward "
            "the grand mean or a regression fit, as Dennis Lindley suggested in 1962, at the cost of one dimension per "
            "parameter estimated. <bookmark mark='b'/> Unequal variances and unknown noise levels were handled by James "
            "Berger and others. <bookmark mark='c'/> But the guarantee is always for the total loss, and a coordinate far "
            "from the rest can be badly over-shrunk. <bookmark mark='d'/> Efron and Morris's limited-translation rules of "
            "1972 cap how far any one coordinate may be moved. <bookmark mark='e'/> And what shrinkage does to an interval, "
            "the Board shows next."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
        rows = board_rows("James")
        show_board(self, rows,
                   "<bookmark mark='a'/> Ten means, nine of them zero and one equal to five, with James–Stein-centred intervals "
                   "of plus or minus one point six four five. For the large mean, shrinkage drags the centre about a unit "
                   "toward zero, and coverage falls to about two thirds: broken. <bookmark mark='b'/> For a zero mean, the "
                   "same intervals cover ninety-seven percent of the time: conservative. Good total risk does not make "
                   "honest intervals for each coordinate; Part forty-six takes this up.",
                   [("a", [0]), ("b", [1])])
