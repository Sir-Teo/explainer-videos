from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, COMB, comma, load


class Counter(VoiceoverScene):
    def construct(self):
        c = load("counter")
        self.card()
        self.history(c)
        self.sources(c)
        self.hurdle(c)
        self.correlated(c)
        self.shuffled(load("permnull"), c)
        self.question()

    def card(self):
        c = chapter_card(8, r"The counter explodes", r"What does a search over thousands of formulas do to the bar a "
                         r"result must clear?", part=PART)
        with self.voiceover("Chapter eight. Since Part twenty-six the series has kept a trial counter: every "
                            "configuration tried on the way to a registered strategy. Machines that search thousands of "
                            "formulas make it run. What does that do to the bar a result must clear?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self, c):
        parts = np.array(c["parts"])
        cnt = np.array(c["count"], float)
        top = float(np.ceil(cnt[-1] / 5000) * 5000)
        g = axes([0.5, parts[-1] + 0.5], [0, top], x_length=9.6, y_length=4.4, xlabel=r"part", ylabel=r"the trial counter",
                 xticks=[1, 10, 20, 26, 29], yticks=[0, top / 2, top], font_size=15,
                 yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}")).move_to(LEFT * 0.4 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.22, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=(HURDLE if p == PART else QC.HOUSE), fill_opacity=0.85).move_to(
            ax.c2p(p, 0), aligned_edge=DOWN) for p, v in zip(parts, cnt)])
        i26 = int(np.flatnonzero(parts == 26)[0])
        t26 = label(rf"Part 26: {comma(cnt[i26] - cnt[i26 - 1])} trading rules", font_size=17, color=QC.HOUSE).next_to(
            bars[i26], UP, buff=0.15).shift(LEFT * 1.4)
        t29 = MathTex(comma(cnt[-1]), font_size=26, color=HURDLE).next_to(bars[-1], UP, buff=0.12)
        n25, n_add, n_now = int(cnt[i26 - 1]), int(cnt[-1] - cnt[-2]), int(cnt[-1])
        with self.voiceover(
            f"""This is existing registration metadata, read without changing the ledger. <bookmark mark='a'/> The counter reaches {n25:,} by Part twenty-five; Part twenty-six's recorded data-snooping study adds ten thousand rules. <bookmark mark='b'/> The historical increment for Part twenty-nine is {n_add:,}, and the count through this part is {n_now:,}. These registrations already exist. Restoring the unchanged original calculations creates no new registration or market trial, and no sealed payoff is read. The recorded count documents a search history, not independent tests."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:-1]], lag_ratio=0.05), FadeIn(t26))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(t29))
        self.wait(0.4)
        self.clear_scene()

    def sources(self, c):
        s = c["by_source"]
        tot = sum(s.values())
        recorded_increment = int(c["count"][-1] - c["count"][-2])
        difference = recorded_increment - tot
        items = [(r"random formulas, Chapter 3", s["random"], RAND_C),
                 (r"genetic programming, three runs", s["gp"], GP_C),
                 (r"distinct formulas written by the RL generator, Chapter 5", s["rl"], RL_C),
                 (r"combinations of the top alphas, Chapter 7", s["combinations"], COMB)]
        rows = VGroup()
        for t, v, col in items:
            rows.add(VGroup(label(t, font_size=20, color=col), MathTex(comma(v), font_size=28, color=col)))
        for j, r_ in enumerate(rows):
            r_[0].move_to([-1.6, 1.6 - 0.8 * j, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
            r_[1].move_to([4.8, 1.6 - 0.8 * j, 0])
        line = Line([-6.0, -1.7, 0], [5.6, -1.7, 0], color=GREY_C, stroke_width=1.5)
        total = VGroup(label(r"current restored evaluations", font_size=22), MathTex(comma(tot), font_size=32, color=HURDLE))
        total[0].move_to([-1.6, -2.2, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
        total[1].move_to([4.8, -2.2, 0])
        foot = wrapped_label(rf"current restored count: {tot:,}; existing registered increment: {recorded_increment:,}. "
                             rf"Difference: {difference:,}; no registry change or retry to match a historical count", 12.0, 16,
                             GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"""The original computational accounting uses four sources. <bookmark mark='a'/> Ten thousand random draws, per-seed unique GP strings, distinct valid RL strings, and compared combination sizes include repeats, related expressions and adaptive rewards. <bookmark mark='b'/> The current restored originals total {tot:,}, while the existing registered increment is {recorded_increment:,}, a difference of {difference:,}. The restored RL original evaluated {s['rl']:,} strings; the earlier checked-in notes reported808. That difference is preserved without another run to seek a match or a registry rewrite. Current computational counts and historical registration metadata answer different questions. Neither is an independent-test count, and no external agent system is run here."""
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(line), FadeIn(total), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hurdle(self, c):
        N = sum(c["by_source"].values())
        T = 3.0
        h = math.sqrt(2 * math.log(N)) / math.sqrt(T)
        rows = [cmath(r"\widehat{SR}_i", r"\approx", r"SR_i+\varepsilon_i/\sqrt T,\quad\varepsilon_i\sim N(0,1)", font_size=30),
                cmath(r"\max_{i\le N}\widehat{SR}_i", r"\sim", r"\sqrt{2\ln N}/\sqrt T\quad\text{(leading independent null scale)}", font_size=28),
                cmath(rf"N={comma(N)},\quad T=3", r"\to", rf"{h:.2f}\quad\text{{annualised SR units}}", font_size=30),
                cmath(r"\text{scope}", r":", r"\text{model reference only; no strategy pass/fail}", font_size=28)]
        whys = [why(r"IID returns, approximately Gaussian Sharpe noise near zero; $T$ is years under consistent annualisation"),
                why(r"independent, comparable, pre-specified null strategies; not an exact expected maximum or rejection threshold"),
                why(r"fixed arithmetic applied to the original search count, not an estimated independent count"),
                why(r"the sealed strategy result is excluded; this calculation supplies no performance verdict")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(f"Consider a reference model. <bookmark mark='a'/> Near a zero Sharpe, independent returns with consistent annualisation give approximate annual Sharpe noise of one over square root T years. Dependence, tails and selection can change that uncertainty. <bookmark mark='b'/> For independent comparable Gaussian null strategies the leading maximum scale is square root two log N divided by square root T. It is not an exact expectation, p-value or universal hurdle. <bookmark mark='c'/> Using the original count {N:,} and three years gives {h:.2f} annualised Sharpe units. <bookmark mark='d'/> The actual strategies are related and adaptive, so this is fixed model arithmetic only. The sealed strategy result remains excluded, and no pass or fail conclusion is supplied.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def correlated(self, c):
        cards = VGroup(
            desk_question(r"dependence needs a model", r"formula strings and adaptive rewards are not independent Gaussian tests; a covariance estimate alone does not calibrate every tail", width=12.4, font_size=19),
            desk_question(r"bookkeeping is not a damage bound", r"a complete familywise bound needs valid marginal tail probabilities and all tested configurations; the raw count alone is insufficient", width=12.4, font_size=19),
            desk_question(r"freeze the full evaluation protocol", r"data vintage, signal timing, selection, costs, outcome coverage and all later decisions; the sealed experiment remains excluded", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Three qualifications. <bookmark mark='a'/> Dependence often reduces a maximum relative to an independent reference, but one effective count need not fit every tail or adaptive search. <bookmark mark='b'/> The raw counter is bookkeeping, not a general upper bound on damage. A union bound would also need valid marginal probabilities and a complete tested family; neither follows from counting formulas. <bookmark mark='c'/> A clean future evaluation freezes the data, timing, selection rule, costs and reporting protocol before outcomes are seen. Its power and validity still need analysis. No sealed experiment is opened in this review.") as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def shuffled(self, p, c):
        rows = [cmath(r"\tilde r_{t+1}", r"=", r"\pi_t(r_{t+1})\quad\text{(shared daily cross-sectional shuffle)}", font_size=29),
                cmath(r"M", r"=", rf"\max_{{i\le {p['n_forms']}}}|\overline{{IC}}_i(\tilde r)|", font_size=30),
                cmath(r"\sigma_e\sqrt{2\ln 2N}", r"=", rf"{p['indep_bar']:.4f}\quad\text{{(leading Gaussian reference)}}", font_size=28),
                cmath(r"\overline M", r"=", rf"{p['mean_null_max']:.4f},\quad N_{{\rm scale}}=\tfrac12 e^{{(\overline M/\sigma_e)^2/2}}\approx {p['n_eff']:.0f}", font_size=28)]
        whys = [why(r"hold the formula vectors fixed; the same shuffle is shared across their scores, conditional on the supplied grid"),
                why(rf"first {p['n_forms']} pre-drawn formulas, {p['n_perm']} shared shuffles; not a replay of GP, RL or combination selection"),
                why(r"two-sided independent Gaussian maximum scale, using a separate noise design's spread"),
                why(r"inverting a leading scale is a calibration index, not an identified number of independent tests")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        note_ = wrapped_label(r"No extrapolation to the full adaptive search; no strategy performance verdict", 11.6, 19, HURDLE).to_edge(DOWN, buff=0.35)
        with self.voiceover(f"Now inspect one specific shuffle design. <bookmark mark='a'/> Tomorrow's finite returns are permuted among eligible coins within each day, with a shared permutation for all fixed formulas. Exchangeability of those coin labels under a relevant null is an assumption; heterogeneous risks and serial structure complicate it. <bookmark mark='b'/> The unchanged original scores {p['n_forms']} pre-drawn formulas on {p['n_perm']} such shuffles. It does not repeat the adaptive GP, RL or combination search. <bookmark mark='c'/> The leading independent Gaussian reference is {p['indep_bar']:.4f}. <bookmark mark='d'/> The observed mean shuffled maximum is {p['mean_null_max']:.4f}. Inverting that leading scale gives about {p['n_eff']:.0f}, a calibration index using this noise spread. Twenty maxima and a mismatched reference do not identify an independent-trial count. We do not scale this fraction to the full search or claim that a strategy clears a corrected hurdle.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"use the leading independent Gaussian reference for a million noise formulas and two years "
                       r"of IID daily data. What annual Sharpe scale does it give?")
        with self.voiceover(
            'Pause and predict. Use the leading independent Gaussian reference for a million pure-noise formulas and two years of independent daily data. What annual Sharpe scale does it give?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
