from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
        bn, ns = x["best_null"], x["n_sig_null"]
        c = chapter_card(2, r"Luck or skill?", r"How do you tell a skilled manager from a lucky one?", part=PART)
        with self.voiceover(
            f"Chapter two, and the answer to the pause: about {bn:.1f}. In the House's simulation, the luckiest of two "
            f"thousand skill-less funds has a t-statistic of {bn:.2f}, and {ns} of them pass the usual two-standard-error "
            "test. With enough funds, someone always looks brilliant. The question is never whether the best fund is "
            "significant, but whether there are more good funds than luck would make."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def streaks(self):
        rows = [cmath(r"P(\text{5 wins} \mid \text{no skill})", r"=", r"(1/2)^5 = 1/32", font_size=40, colors={r"=": HURDLE}),
                cmath(r"\mathbb E[\#\text{ streaks among } 2{,}000]", r"=", r"2{,}000/32 \approx 62", font_size=38),
                cmath(r"P(\text{at least one})", r"=", r"1 - (31/32)^{2000} \approx 1", font_size=40, colors={r"=": COST_C})]
        whys = [why(r"ignoring costs, a zero-skill fund beats the market in any one year about half the time"),
                why(r"so about sixty funds will beat it five years running by chance alone"),
                why(r"a five-year streak somewhere is certain; the desk question's fund is one of the sixty, unless more "
                    r"than sixty have such streaks")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Back to the desk question. <bookmark mark='a'/> Ignoring costs, a fund with no skill beats the market in "
            "any one year about half the time, so five years running with probability one in thirty-two. "
            "<bookmark mark='b'/> Among two thousand funds, about sixty will do it by chance. <bookmark mark='c'/> And "
            "the chance that at least one does is essentially one. So a five-year streak is evidence only if many more "
            "than sixty funds have one: which is exactly the counting of Barras, Scaillet and Wermers."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
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
        whys = [why(r"the shares follow Barras, Scaillet and Wermers' estimates for US equity funds, as they report"),
                why(r"funds whose alpha does not cover their costs"),
                why(r"a small minority with real skill"),
                why(r"2,000 funds in the House's simulation; the truth is known, so every method can be checked")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A world where the truth is known. <bookmark mark='a'/> Most funds have no alpha at all. "
            "<bookmark mark='b'/> About a quarter have negative alpha: they do not cover their costs. "
            "<bookmark mark='c'/> About one in a hundred has real skill. These shares follow Laurent Barras, Olivier "
            "Scaillet and Russ Wermers' estimates for American equity funds. <bookmark mark='d'/> Each fund is measured "
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
            "no fund had skill: a bell centred at zero. <bookmark mark='b'/> The real population is shifted left, by "
            "the unskilled quarter, with a thin extra tail on the right. <bookmark mark='c'/> Beyond the usual cut-off "
            "at two, the right tail holds a mix of a few skilled funds and many lucky ones. Telling them apart one by "
            "one is impossible; counting them is not."
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
        note_ = label(rf"luck alone: about {fd['t2']:.0f} funds above $t = 1.96$ and {fd['t3']:.1f} above 3, of 2,000",
                      font_size=17, color=GREY_B).to_edge(DOWN, buff=0.5)
        a99, n99, a1, n1 = ap[-1], npc[-1], ap[0], npc[0]
        t2, t3 = fd["t2"], fd["t3"]
        with self.voiceover(
            "Fama and French's comparison, done the same way: the funds' t-statistics, percentile by percentile, "
            "against a population with every alpha set to zero. <bookmark mark='a'/> In the left tail the funds are far "
            f"worse than luck: {a1:.2f} against {n1:.2f} at the first percentile. <bookmark mark='b'/> In the right "
            f"tail they are only a little better: {a99:.2f} against {n99:.2f} at the ninety-ninth. "
            f"<bookmark mark='c'/> And luck alone puts about {t2:.0f} funds above the usual cut-off, and {t3:.1f} above "
            "a t of three."
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
        cards = VGroup(
            desk_question(r"Fama and French (2010)", r"bootstrap the funds' returns with their alphas set to zero, to "
                          r"build the distribution of $t$-statistics that luck alone would give", width=12.4, font_size=19),
            desk_question(r"what they found", r"net of costs, the actual distribution lies to the left of luck's; few "
                          r"funds have enough skill to cover their costs, as they report", width=12.4, font_size=19),
            desk_question(r"Kosowski et al. (2006)", r"by the same kind of bootstrap, the very best funds' alphas are "
                          r"larger than luck would give, before costs", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How the literature does it on real funds. <bookmark mark='a'/> Eugene Fama and Kenneth French bootstrap "
            "each fund's returns with its alpha set to zero, to see what luck alone would produce. "
            "<bookmark mark='b'/> Net of costs, the real distribution lies to the left of luck's: few funds earn their "
            "fees, as they report. <bookmark mark='c'/> Robert Kosowski and coauthors, with a similar bootstrap, found "
            "that the very best funds' alphas before costs are larger than luck would give."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def bsw_method(self):
        rows = [cmath(r"\hat\pi_0", r"=", r"\frac{\#\{p_i > \lambda\}}{m(1 - \lambda)}", font_size=42, colors={r"\hat\pi_0": LUCK_C}),
                cmath(r"\text{lucky in a tail}", r"\approx", r"\hat\pi_0\,\gamma/2", font_size=40),
                cmath(r"\hat\pi^+", r"=", r"\hat S^+_\gamma - \hat\pi_0\,\gamma/2", font_size=42, colors={r"\hat\pi^+": SKILL_C})]
        whys = [why(r"Storey (2002): $p$-values above $\lambda$ come mostly from true nulls, which are uniform; so their "
                    r"count, scaled, estimates the share of nulls"),
                why(r"of the nulls, a share $\gamma/2$ land in each significant tail by chance"),
                why(r"Barras, Scaillet and Wermers (2010): the significant share in the right tail, less the lucky part, "
                    r"estimates the skilled share; the left tail, the unskilled")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Barras, Scaillet and Wermers count, rather than pick. <bookmark mark='a'/> First, John Storey's estimate "
            "of how many funds have no alpha: large p-values come mostly from them, and are spread evenly, so their "
            "count, scaled up, estimates the share. <bookmark mark='b'/> Of those, a known fraction lands in each "
            "significant tail by luck. <bookmark mark='c'/> So the share significant in the right tail, minus the lucky "
            "part, estimates the skilled share; the left tail, the unskilled. The research chapter proves why the "
            "first step works."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
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
            "And it works. <bookmark mark='a'/> The share with no alpha: "
            f"{pi0t:.1f} percent in truth, {pi0e:.1f} estimated. <bookmark mark='b'/> Unskilled: {mt:.1f} against "
            f"{me:.1f}. <bookmark mark='c'/> Skilled: {pt:.1f} against {pe:.1f}. Not one fund was identified; the "
            "shares were."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sig(self, x):
        ns, sh = x["n_sig"], 100 * x["share_true_skilled_among_sig"]
        rows = VGroup(
            label(rf"funds with $t > 1.96$: {ns} of 2,000", font_size=26, color=ACT_C),
            label(rf"truly skilled among them: {sh:.0f}\%", font_size=26, color=SKILL_C),
            label(r"the rest: zero-alpha funds that were lucky", font_size=24, color=LUCK_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        with self.voiceover(
            f"So what does a significant fund mean? <bookmark mark='a'/> {ns} of the two thousand clear the usual "
            f"bar. <bookmark mark='b'/> Of those, only {sh:.0f} percent are truly skilled. <bookmark mark='c'/> The "
            "rest are zero-alpha funds that were lucky. That is the false discovery rate, and it is why a star "
            "manager's record, alone, says less than it seems."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            "mostly the unskilled, whose costs are permanent. <bookmark mark='b'/> The top decile barely persists: "
            f"{tn:+.1f} percent. Only {ts:.0f} percent of its funds are truly skilled; the rest were lucky, and luck "
            "does not repeat. Carhart's finding, reproduced with the truth known."
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
            desk_question(r"why the losers persist", r"high costs are permanent; a lucky streak is not", width=12.4,
                          font_size=19),
            desk_question(r"the puzzle", r"if some skill exists, why does it not show up as lasting outperformance? "
                          r"The next chapter's answer: money", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And over time. <bookmark mark='a'/> Mark Carhart found that winners' persistence is mostly momentum in what "
            "they hold, and differences in costs; only the worst funds reliably stay bad. <bookmark mark='b'/> High "
            "costs are permanent; a lucky streak is not. <bookmark mark='c'/> Which leaves a puzzle: if a little skill "
            "exists, why does it not show up as lasting outperformance?"
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
