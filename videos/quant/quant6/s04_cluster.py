from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card, tbar

NF, NT = 4, 6  # firms, months in the toy panel; rows ordered (month, firm)


def omega(kind: str, size=0.16):
    n = NF * NT
    g = VGroup()
    for a in range(n):
        for b in range(n):
            ta, fa, tb, fb = a // NF, a % NF, b // NF, b % NF
            v = 0.9 if a == b else (0.5 if (kind == "firm" and fa == fb) or (kind == "time" and ta == tb) else 0.0)
            sq = Square(side_length=size, stroke_width=0.3, stroke_color=GREY_D, fill_color=EST, fill_opacity=v)
            sq.move_to([(b - n / 2 + 0.5) * size, -(a - n / 2 + 0.5) * size, 0])
            sq.ij = (ta, fa, tb, fb)
            g.add(sq)
    return g


class Cluster(VoiceoverScene):
    def construct(self):
        p = load("petersen")
        pn = load("panel")
        self.card()
        self.masks()
        self.derive()
        self.petersen(p)
        self.finance(pn)

    def card(self):
        c = chapter_card(3, r"Clustering: the shocks that are shared", r"Whose errors move together?", part=PART)
        with self.voiceover("Chapter three. Clustering: the shocks that are shared."):
            show_card(self, c)
        self.play(FadeOut(c))

    def masks(self):
        om = omega("firm").to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        title = label(r"$\Omega$ for 4 firms $\times$ 6 months, rows ordered (month, firm)", font_size=22,
                      color=GREY_A).next_to(om, UP, buff=0.25)
        kind_l = label(r"a firm effect: each firm's errors persist", font_size=24, color=EST).next_to(om, DOWN, buff=0.3)

        def mask(rule, color):
            return VGroup(*[SurroundingRectangle(sq, buff=0, stroke_width=0, fill_color=color, fill_opacity=0.45)
                            for sq in om if rule(*sq.ij)])

        m_ols = mask(lambda ta, fa, tb, fb: ta == tb and fa == fb, GOOD)
        m_firm = mask(lambda ta, fa, tb, fb: fa == fb, GOOD)
        m_time = mask(lambda ta, fa, tb, fb: ta == tb, GOOD)
        side = VGroup(
            label(r"each estimator covers part of the matrix:", font_size=23, color=GREY_A),
            label(r"OLS / White: the diagonal only", font_size=23, color=GREY_A),
            label(r"clustered by firm: same-firm cells", font_size=23, color=GREY_A),
            label(r"clustered by month: same-month blocks", font_size=23, color=GREY_A),
            wrapped_label(r"lit cells left uncovered (red) are variance the standard error never sees", 5.4, 22, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)

        def missing(rule):
            return VGroup(*[SurroundingRectangle(sq, buff=0, stroke_width=0, fill_color=BAD, fill_opacity=0.75)
                            for sq in om if sq.get_fill_opacity() > 0.3 and not rule(*sq.ij)])

        with self.voiceover(
            "In a panel, many firms over many months, errors can be linked two more ways. Here is the error covariance "
            "matrix for four firms over six months, rows ordered month by month. <bookmark mark='a'/> A firm effect, a "
            "persistent component per firm, links every pair of observations of the same firm: stripes. "
            "<bookmark mark='b'/> Least squares, even with White's correction, covers only the diagonal; what it misses "
            "lights up red. <bookmark mark='c'/> Clustering by firm covers the stripes. <bookmark mark='d'/> A time "
            "effect, a shock every firm shares in a month, makes diagonal blocks instead. Firm clusters miss them; "
            "month clusters cover them."
        ) as vo:
            self.play(FadeIn(om), FadeIn(title), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(kind_l))
            vo.wait_until("b")
            miss = missing(lambda ta, fa, tb, fb: ta == tb and fa == fb)
            self.play(FadeIn(m_ols), FadeIn(side[1]))
            self.play(FadeIn(miss), FadeIn(side[4]))
            vo.wait_until("c")
            self.play(FadeOut(miss), FadeOut(m_ols), FadeIn(m_firm), FadeIn(side[2]))
            vo.wait_until("d")
            new = omega("time").move_to(om)
            for sq, nq in zip(om, new):
                sq.ij = nq.ij
            self.play(FadeOut(m_firm), Transform(om, new),
                      Transform(kind_l, label(r"a time effect: every firm shares the month's shock", font_size=24,
                                              color=EST).move_to(kind_l)))
            for sq, nq in zip(om, new):
                sq.set_fill(opacity=nq.get_fill_opacity())
            miss2 = missing(lambda ta, fa, tb, fb: fa == fb)
            self.play(FadeIn(m_firm), FadeIn(miss2))
            self.play(FadeOut(m_firm), FadeOut(miss2), FadeIn(m_time), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\hat V_{cl}": GOOD, r"\rho_x \rho_u": BAD}
        rows = [cmath(r"\hat V_{cl}", r"=", r"(X^\top X)^{-1}\Big(\textstyle\sum_g X_g^\top \hat u_g \hat u_g^\top X_g\Big)"
                      r"(X^\top X)^{-1}", font_size=36, colors=C_),
                cmath(r"\mathrm{Var}(\hat\beta)", r"\approx", r"\frac{\sigma_u^2}{\sum x^2}\Big[1 + (n_g - 1)\,"
                      r"\rho_x \rho_u\Big]", font_size=36, colors=C_),
                cmath(r"\hat V_{2way}", r"=", r"\hat V_{firm} + \hat V_{time} - \hat V_{firm \cap time}", font_size=36,
                      colors=C_)]
        whys = [why(r"the meat sums each cluster's total score, squared: any correlation inside a cluster is kept"),
                why(r"Moulton's factor: equal clusters of size $n_g$; the damage needs both $x$ and $u$ to be "
                    r"correlated within clusters"),
                why(r"inclusion--exclusion: the same-firm cells plus the same-month cells, minus the diagonal counted "
                    r"twice (Cameron, Gelbach and Miller 2011)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=1.0, edge=6.8)
        with self.voiceover(
            "The clustered estimator sums the scores within each cluster, squares the total, and adds over clusters: "
            "every correlation inside a cluster is kept, every correlation across clusters is assumed away. It needs "
            "many clusters, because each cluster is one observation of the meat. <bookmark mark='a'/> Moulton's factor "
            "says what ignoring it costs: the naive variance times one plus the cluster size minus one, times the "
            "within-cluster correlations of both the regressor and the error. With forty-nine industries in a month, "
            "even small correlations multiply into a large factor. <bookmark mark='b'/> With both kinds of effect, "
            "Cameron, Gelbach and Miller's two-way estimator adds the firm and month clusters and subtracts the "
            "diagonal they both counted."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def petersen(self, p):
        des = ["firm 50%", "time 50%", "firm 25% + time 25%"]
        dlab = [r"firm effect", r"time effect", r"both"]
        est = ["OLS", "firm", "time", "two-way", "FM"]
        elab = [r"OLS", r"by firm", r"by month", r"two-way", r"Fama--MacBeth"]
        cols = [BAD, DATA_C, ALT, GOOD, EST]
        ck = np.asarray(p["checkpoints"], float)
        g = axes([0, 3], [0, 1.25], x_length=8.0, y_length=4.0, ylabel=r"average standard error / true spread",
                 xticks=[], yticks=[0, 0.5, 1.0], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(3, 1), color=GREY_B, stroke_width=2)
        n = ValueTracker(0.0)

        def bars():
            out = VGroup()
            k = n.get_value()
            for i, d in enumerate(des):
                for j, e in enumerate(est):
                    path = np.asarray(p["designs"][d]["path"][e])
                    v = float(np.interp(k, np.arange(len(path)), path))
                    out.add(tbar(ax, i + 0.12 + 0.17 * j, min(v, 1.25), cols[j], width=0.15))
            return out
        bm = always_redraw(bars)
        cnt = always_redraw(lambda: MathTex(rf"\text{{replications: }} {int(np.interp(n.get_value(), np.arange(len(ck)), ck)):,}"
                                            .replace(",", "{,}"), font_size=26, color=GREY_A).next_to(g, UP, buff=0.1)
                            .align_to(g, RIGHT))
        dl = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                      for i, t in enumerate(dlab)])
        leg = legend(list(zip(cols, elab)), font_size=19).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        r = {d: p["designs"][d]["ratio"] for d in des}
        txt = wrapped_label(rf"{p['firms']} firms $\times$ {p['years']} years, {p['reps']:,} simulated panels per "
                            r"design; Petersen (2009), Table~1's design".replace(",", "{,}"), 4.4, 19, GREY_B)
        txt.next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        with self.voiceover(
            "Mitchell Petersen ran the experiment in 2009, and we repeat it: five hundred firms over ten years, with "
            "firm effects, time effects or both. Each bar is a method's average standard error over the true spread; "
            "one is honest. <bookmark mark='a'/> Watch them settle as replications pile up. With a firm effect, least "
            f"squares reports {r['firm 50%']['OLS']:.2f} of the truth, Fama-MacBeth {r['firm 50%']['FM']:.2f}, "
            f"clustering by firm {r['firm 50%']['firm']:.2f}. <bookmark mark='b'/> With a time effect, least squares "
            f"reports {r['time 50%']['OLS']:.2f}; clustering by month, with only ten clusters, {r['time 50%']['time']:.2f}; "
            f"Fama-MacBeth {r['time 50%']['FM']:.2f}. <bookmark mark='c'/> With both, the two-way estimator, "
            f"{r['firm 25% + time 25%']['two-way']:.2f}. And in Petersen's survey, forty-two percent of panel papers had "
            "not adjusted at all."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(dl), FadeIn(leg), FadeIn(txt))
            self.add(bm, cnt)
            vo.wait_until("a")
            self.play(n.animate.set_value(len(ck) - 1), run_time=vo.until("b"), rate_func=linear)
            vo.wait_until("c")
            self.play(Indicate(leg[3], color=GOOD))
        bm.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def finance(self, pn):
        res = pn["results"]
        rows = VGroup(
            label(r"The finance rule", font_size=32, color=WHITE),
            wrapped_label(r"returns share time shocks (the market, the month's news): cluster by month, or use "
                          r"Fama--MacBeth; corporate panels (leverage, investment) share firm effects: cluster by firm; "
                          r"when in doubt, two-way, with enough clusters in each dimension", 11.4, 25, GREY_A),
            MathTex(rf"\text{{industry momentum: by industry }} t = {res['clustered by industry']['t']:.2f},\quad "
                    rf"\text{{by month }} t = {res['clustered by month']['t']:.2f}", font_size=32, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(UP, buff=0.8)
        q = predict(r"Industry momentum, 49 industries, 1{,}116 months: cluster by industry or by month?").next_to(
            rows, DOWN, buff=0.5)
        with self.voiceover(
            "Which dimension? Whatever the regressor and the error both share. Returns share the month; a firm's "
            "leverage shares the firm. When in doubt, cluster both ways, with enough clusters in each. "
            "<bookmark mark='a'/> Pause and predict: the opening regression, cluster by industry or by month? "
            f"<bookmark mark='b'/> By month. By industry, the t-statistic moves from {res['pooled OLS']['t']:.2f} to "
            f"{res['clustered by industry']['t']:.2f}; by month, to {res['clustered by month']['t']:.2f}. The shared "
            "shock is the market."
            " Clustering by month fixes the standard error. Fama and MacBeth fix the whole regression, and resolve the five verdicts. Next."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
