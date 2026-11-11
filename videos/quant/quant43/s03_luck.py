from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, SKILL_C, fit_right,
                                         load)


class Luck(VoiceoverScene):
    def construct(self):
        x = load("luck")
        self.card(x)
        self.streaks()
        self.population(x)
        self.hist(x)
        self.percentiles(x)
        self.ff2010()
        self.bsw_method()
        self.bsw_result(x)
        self.sig(x)
        self.persistence_chart(x)
        self.persistence()
        self.question()

    def card(self, x):
        bn, ns = (x['best_null'], x['n_sig_null'])
        c = chapter_card(2, 'Luck or skill?', 'How do you tell a skilled manager from a lucky one?', part=PART)
        with self.voiceover(f"Chapter two, and the answer to the pause: about {bn:.1f}. In the House's simulation, the luckiest of two thousand skill-less funds has a t-statistic of {bn:.2f}, and {ns} of them pass the usual two-standard-error test. A selected maximum can look impressive even under this null. A selected winner requires inference that accounts for the selection procedure; aggregate tail counts are one possible approach."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def streaks(self):
        rows=[cmath(r"P(\text{five wins})",r"=",r"(1/2)^5=1/32",font_size=42),
              cmath(r"\mathbb E[\text{number among }2000]",r"=",r"2000/32=62.5",font_size=38),
              cmath(r"P(\text{at least one})",r"=",r"1-(31/32)^{2000}\approx1",font_size=38)]
        whys=[why(r"toy null: independent symmetric annual wins with probability one half, ignoring costs"),
              why(r"linearity needs the marginal streak probabilities, not independence between funds"),
              why(r"this last formula additionally assumes independent funds; approximately one is not certainty")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "A toy streak calculation. <bookmark mark='a'/> Assume independent symmetric annual wins with "
            "probability one half, ignoring costs. A five-year winning streak then has probability one in thirty-two. "
            "<bookmark mark='b'/> Among two thousand funds the expected count is sixty-two point five, by linearity. "
            "<bookmark mark='c'/> If funds are also independent, the chance of at least one streak is extremely close "
            "to one. A selected winner therefore raises a selection problem. This is one null calculation, not a "
            "claim that every zero-mean return has a one-half win probability or that aggregate streak counting is "
            "the only possible test of skill."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def population(self, x):
        t = x["truth"]
        rows = [cmath(r"\text{zero alpha}", r":", rf"{100 * t['pi0']:.1f}\%\ \text{{of funds}}", font_size=40,
                      colors={r"\text{zero alpha}": LUCK_C}),
                cmath(r"\text{unskilled}", r":", rf"{100 * t['minus']:.1f}\%,\ \alpha = -3.2\%\ \text{{a year}}", font_size=40,
                      colors={r"\text{unskilled}": COST_C}),
                cmath(r"\text{skilled}", r":", rf"{100 * t['plus']:.1f}\%,\ \alpha = +3.8\%\ \text{{a year}}", font_size=40,
                      colors={r"\text{skilled}": SKILL_C}),
                cmath(r"\text{each}", r":", r"240\ \text{months, tracking error } 5\%", font_size=40)]
        whys = [why(r"chosen three-group probabilities loosely motivate the teaching example; these are not fitted empirical shares"),
                why(r"funds with negative alpha relative to the chosen benchmark"),
                why(r"a small minority with real skill"),
                why(r"2,000 funds in the House's simulation; the truth is known, so every method can be checked")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A world where the truth is known. <bookmark mark='a'/> Most funds have no alpha at all. "
            "<bookmark mark='b'/> About a quarter have negative alpha relative to the chosen benchmark; the generator does not separately model their fees. "
            "<bookmark mark='c'/> About one in a hundred has real skill. These are chosen teaching probabilities, motivated by the questions studied by Laurent Barras, Olivier "
            "Scaillet and Russ Wermers, rather than an empirical fit in this lecture. <bookmark mark='d'/> Each fund is measured "
            "for twenty years, with five percent tracking error."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def hist(self, x):
        e = np.asarray(x["edges"], float)
        h = np.asarray(x["hist"], float)
        hn = np.asarray(x["hist_null"], float)
        top = float(max(h.max(), hn.max()) * 1.1)
        g = axes([-8, 6], [0, top], x_length=9.4, y_length=4.2, xlabel=r"$t$-statistic of alpha",
                 ylabel=r"number of funds", xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[], font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        w = (e[1] - e[0])
        bars = VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(1e-3, ax.c2p(0, h[i])[1] - ax.c2p(0, 0)[1]),
                                  stroke_width=0, fill_color=ACT_C, fill_opacity=0.6).move_to(ax.c2p(e[i] + w / 2, h[i] / 2))
                        for i in range(len(h))])
        xs = np.repeat(e, 2)[1:-1]
        ys = np.repeat(hn, 2)
        nl = curve(ax, xs, ys, LUCK_C, stroke_width=2.5)
        cut = DashedLine(ax.c2p(1.96, 0), ax.c2p(1.96, top), color=HURDLE, stroke_width=1.5)
        leg = legend([(ACT_C, r"the population"), (LUCK_C, r"if no fund had skill")], font_size=16).to_corner(UR, buff=0.4)
        with self.voiceover(
            "The t-statistics of all two thousand. <bookmark mark='a'/> The outline shows what they would look like if "
            "no fund had skill: a bell centred at zero. <bookmark mark='b'/> The simulated mixture is shifted left, by "
            "the unskilled quarter, with a thin extra tail on the right. <bookmark mark='c'/> Beyond the usual cut-off "
            "at two, the right tail holds a mix of a few skilled funds and many lucky ones. An individual statistic does not reveal true skill with certainty; population inference also needs assumptions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(nl), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.02), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(cut))
        self.wait(0.4)
        self.clear_scene()

    def percentiles(self, x):
        pct, ap, npc = x["pct"], x["act_pct"], x["null_pct"]
        tab = VGroup(VGroup(label(r"percentile", font_size=19, color=QC.IDEA), label(r"the funds", font_size=19, color=QC.IDEA),
                            label(r"luck alone", font_size=19, color=QC.IDEA)))
        for p_, a_, b_ in zip(pct, ap, npc):
            tab.add(VGroup(label(rf"{p_}", font_size=19), label(rf"{a_:+.2f}", font_size=19, color=ACT_C),
                           label(rf"{b_:+.2f}", font_size=19, color=LUCK_C)))
        xs = [-3.0, 0.6, 3.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.6 - 0.6 * j, 0])
        fd = x["exp_fd"]
        note_ = label(rf"standard-normal approximation: about {fd['t2']:.0f} funds above $t = 1.96$ and {fd['t3']:.1f} above 3, of 2,000",
                      font_size=17, color=GREY_B).to_edge(DOWN, buff=0.5)
        a99, n99, a1, n1 = ap[-1], npc[-1], ap[0], npc[0]
        t2, t3 = fd["t2"], fd["t3"]
        with self.voiceover(
            "A fresh simulated zero-alpha population provides a reference for the mixture population's t-statistics, percentile by percentile, "
            "with the same sample length and residual-volatility assumptions. This is not a bootstrap of real fund returns. <bookmark mark='a'/> In the left tail the funds are far "
            f"worse than luck: {a1:.2f} against {n1:.2f} at the first percentile. <bookmark mark='b'/> In the right "
            f"tail they are only a little better: {a99:.2f} against {n99:.2f} at the ninety-ninth. "
            f"<bookmark mark='c'/> The standard-normal tail approximation puts about {t2:.0f} funds above the usual cut-off, and {t3:.1f} above "
            "a statistic of three; the simulated statistics have a finite-degree Student distribution, so these are approximate reference counts."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:]], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def ff2010(self):
        cards=VGroup(
            desk_question('Fama and French (2010)','compare empirical fund-alpha statistics with a resampled null distribution, retaining economically relevant dependence in their design',width=12.4,font_size=19),
            desk_question('published inference','few funds cover costs under their benchmark and bootstrap assumptions; other studies use different designs and reach different tail conclusions',width=12.4,font_size=19),
            desk_question('this lecture','the displayed null is a separately generated zero-alpha population, not an empirical fund-return bootstrap',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("The empirical literature uses a different experiment. <bookmark mark='a'/> Fama and French compare fund-alpha statistics with a bootstrapped null, with dependence handled in their resampling design. <bookmark mark='b'/> Their inference that few funds cover costs is conditional on their data, benchmarks and bootstrap assumptions. Other studies use different designs and obtain different tail conclusions. <bookmark mark='c'/> The lecture's displayed reference population is separately simulated at zero alpha; it does not reproduce that empirical bootstrap.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def bsw_method(self):
        rows=[cmath(r"\widetilde\pi_0",r"=",r"\#\{p_i>\lambda\}/[m(1-\lambda)]",font_size=40),
              cmath(r"\widehat\pi_0",r"=",r"\min(1,\widetilde\pi_0)",font_size=42),
              cmath(r"\widehat\pi^+",r"=",r"\max(0,\widehat S^+_\gamma-\widehat\pi_0\gamma/2)",font_size=38)]
        whys=[why(r"two-sided p-values for zero alpha; large p-values also occur under weak alternatives"),
              why(r"the implementation caps at one; the raw expectation proof does not automatically transfer"),
              why(r"a descriptive tail-component estimate; power and alternative leakage affect interpretation")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "The simplified tail decomposition. <bookmark mark='a'/> Scale the number of large two-sided p-values "
            "to estimate the zero-alpha share, recognising contamination from weak alternatives. "
            "<bookmark mark='b'/> The unchanged helper caps that estimate at one. <bookmark mark='c'/> It subtracts "
            "an estimated lucky-null tail share and takes the positive part. The result is a descriptive component "
            "estimate, not automatic identification of positive skill. Power, leakage from negative-alpha alternatives "
            "and both nonlinear guards matter. The research chapter proves the raw identity and its limits."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def bsw_result(self, x):
        t, e = x["truth"], x["est"]
        heads = [r"", r"true share", r"estimated"]
        body = [(r"zero alpha", t["pi0"], e["pi0"], LUCK_C), (r"unskilled", t["minus"], e["minus"], COST_C),
                (r"skilled", t["plus"], e["plus"], SKILL_C)]
        tab = VGroup(VGroup(*[label(h_, font_size=21, color=QC.IDEA) for h_ in heads]))
        for nm, a_, b_, col in body:
            tab.add(VGroup(label(nm, font_size=22, color=col), label(rf"{100 * a_:.1f}\%", font_size=22),
                           label(rf"{100 * b_:.1f}\%", font_size=22, color=col)))
        xs = [-3.0, 0.8, 3.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 1.6 - 0.9 * j, 0])
        note_ = label(r"significance level $\gamma = 0.2$, $\lambda = 0.5$; one population of 2,000", font_size=16,
                      color=GREY_B).to_edge(DOWN, buff=0.6)
        pi0t, pi0e, mt, me, pt, pe = 100 * t["pi0"], 100 * e["pi0"], 100 * t["minus"], 100 * e["minus"], 100 * t["plus"], 100 * e["plus"]
        with self.voiceover(
            "The result in this one simulated population. <bookmark mark='a'/> The share with no alpha: "
            f"{pi0t:.1f} percent in truth, {pi0e:.1f} estimated. <bookmark mark='b'/> Unskilled: {mt:.1f} against "
            f"{me:.1f}. <bookmark mark='c'/> Skilled: {pt:.1f} against {pe:.1f}. These estimates happen to be close in this selected run; they are not known empirical truth or a universal bound on the "
            "population shares."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            self.play(FadeIn(tab[1], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sig(self, x):
        ns, sh = x["n_sig"], 100 * x["share_true_skilled_among_sig"]
        rows = VGroup(
            label(rf"funds with $t > 1.96$: {ns} of 2,000", font_size=26, color=ACT_C),
            label(rf"truly skilled among them: {sh:.0f}\%", font_size=26, color=SKILL_C),
            label(r"the rest: selected nonpositive-alpha funds", font_size=24, color=LUCK_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        with self.voiceover(
            f"So what does a significant fund mean? <bookmark mark='a'/> {ns} of the two thousand clear the usual "
            f"bar. <bookmark mark='b'/> Of those, only {sh:.0f} percent are truly skilled. <bookmark mark='c'/> The "
            "rest have nonpositive true alpha. This is a realised false discovery proportion in one run, not expected FDR. A star "
            "manager's record, alone, says less than it seems."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def persistence_chart(self, x):
        ps = x["persist"]
        mx = max(abs(p["next_alpha"]) for p in ps) * 1.2
        g = axes([0.3, 10.7], [-mx, mx * 0.5], x_length=8.4, y_length=4.2, xlabel=r"decile of the first ten years' $t$-statistic",
                 ylabel=r"mean alpha in the next ten years", xticks=list(range(1, 11)), yticks=[-0.02, 0],
                 yfmt=lambda u: rf"{100 * u:+.0f}\%", font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for p in ps:
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, p["next_alpha"])[1]
            col = COST_C if p["next_alpha"] < 0 else SKILL_C
            b = Rectangle(width=0.55, height=max(abs(y1 - y0), 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([ax.c2p(p["decile"], 0)[0], (y0 + y1) / 2, 0])
            bars.add(b)
        top, bot = ps[-1], ps[0]
        lab = label(rf"top decile: {100 * top['share_skilled']:.0f}\% truly skilled", font_size=17, color=SKILL_C).to_corner(UR, buff=0.5)
        tn, bn, ts = 100 * top["next_alpha"], 100 * bot["next_alpha"], 100 * top["share_skilled"]
        with self.voiceover(
            "Persistence, in the simulated population. Rank funds by their first ten years, then watch the next ten. "
            f"<bookmark mark='a'/> The bottom decile keeps losing: {bn:+.1f} percent a year, because its funds are "
            "mostly funds with negative true alpha. <bookmark mark='b'/> The top decile barely persists: "
            f"{tn:+.1f} percent. Only {ts:.0f} percent of its funds are truly skilled; the rest were lucky, and luck "
            "does not systematically repeat. This is a teaching mechanism, not a replication of Carhart's empirical study."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[:5]], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[5:]], lag_ratio=0.15), FadeIn(lab), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def persistence(self):
        cards = VGroup(
            desk_question(r"Carhart (1997)", r"winners' persistence is mostly momentum in their holdings and differences "
                          r"in costs; only the worst funds persist reliably, as he reports", width=12.4, font_size=19),
            desk_question(r"why the losers persist", r"cost differences can persist; a lucky streak does not systematically persist", width=12.4,
                          font_size=19),
            desk_question(r"the puzzle", r"if some skill exists, why does it not show up as lasting outperformance? "
                          r"The next chapter's answer: money", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And over time. <bookmark mark='a'/> Mark Carhart found that winners' persistence is mostly momentum in what "
            "they hold, and differences in costs; only the worst funds reliably stay bad. <bookmark mark='b'/> High "
            "cost differences can persist; a lucky streak does not systematically persist. <bookmark mark='c'/> Which leaves a puzzle: if a little skill "
            "exists, why does it not show up as lasting outperformance?"
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a manager is truly skilled, and investors can see it. Will the fund's investors earn more than "
                       r"the market? Will the manager?")
        with self.voiceover(
            "Pause and predict. A manager is truly skilled, and investors can see it. Will the fund's investors earn "
            "more than the market? Will the manager?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
