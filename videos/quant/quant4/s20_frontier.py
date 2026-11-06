from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, Q_C, load

PAPERS = [
    (2022, r"Wang and Ramdas, \textit{JRSS B} 84(3)", r"e-BH: false discovery control with e-values, under any "
           r"dependence"),
    (2023, r"Ramdas, Gr\"unwald, Vovk and Shafer, \textit{Statistical Science} 38(4)",
           r"the survey: game-theoretic statistics and safe anytime-valid inference"),
    (2023, r"Ruf, Larsson, Koolen and Ramdas, \textit{Electronic Journal of Probability} 28",
           r"Ville's theorem for composite nulls: an event is null exactly when some e-process blows up on it"),
    (2024, r"Waudby-Smith and Ramdas, \textit{JRSS B} 86(1)", r"estimating means by betting: the confidence sequences "
           r"of chapter 16"),
    (2024, r"Shekhar and Ramdas, \textit{IEEE Trans.\ Information Theory} 70(2)",
           r"nonparametric two-sample testing by betting: has the distribution changed?"),
    (2024, r"Gr\"unwald, de Heide and Koolen, \textit{JRSS B} 86(5)", r"safe testing: e-values with optional "
           r"continuation, read before the Royal Statistical Society"),
    (2024, r"Gr\"unwald, \textit{PNAS} 121(39)", r"post-hoc decisions with e-values: guarantees must match the decision rule"),
    (2024, r"Larsson, Ramdas and Ruf, arXiv:2402.18810", r"the numeraire e-variable: the log-optimal test is "
           r"finance's numeraire portfolio"),
    (2025, r"Fischer and Ramdas, \textit{JRSS B}", r"sequential Monte Carlo testing by betting: anytime-valid "
           r"permutation tests (for backtests, Part 26)"),
    (2025, r"Ramdas and Wang, \textit{Hypothesis Testing with E-values}", r"the 390-page monograph, Foundations and "
           r"Trends in Statistics"),
]


class Frontier(VoiceoverScene):
    def construct(self):
        eb = load("ebh")
        nu = load("numeraire")
        self.card()
        self.papers()
        self.bridge(nu)
        self.ebh(eb)

    def card(self):
        c = chapter_card(18, r"Frontier: anytime-valid inference, 2023--2026", r"What is being built on Ville's idea now?",
                         part=PART)
        with self.voiceover("Chapter eighteen. The frontier: anytime-valid inference, from 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.4)

    def papers(self):
        rows = VGroup()
        for yr, who, what in PAPERS:
            y = MathTex(str(yr), font_size=26, color=QC.IDEA)
            t = VGroup(label(who, font_size=20, color=WHITE), label(what, font_size=18, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)
            rows.add(VGroup(y, t).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.6)
        if rows.height > 7.4:
            rows.scale_to_fit_height(7.4)
        for r_ in rows:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        with self.voiceover(
            "Ville's idea is now a fast-moving field. Its foundations: Ruodu Wang and Aaditya Ramdas showed in 2022 "
            "that e-values control false discoveries under any dependence, and a 2023 survey by Ramdas, Grünwald, "
            "Vovk and Shafer mapped the subject. <bookmark mark='a'/> Ruf, Larsson, Koolen and Ramdas extended "
            "Ville's theorem to composite hypotheses: an event is impossible exactly when some e-process blows up on "
            "it. Waudby-Smith and Ramdas estimated means by betting, the confidence sequences of chapter sixteen, "
            "and Shekhar and Ramdas tested whether two distributions differ. <bookmark mark='b'/> Grünwald, de Heide "
            "and Koolen's safe testing was read before the Royal Statistical Society in 2024, and Grünwald showed "
            "post-hoc decision guarantees with e-values. A data-chosen level must not be read as an ordinary "
            "pre-fixed type-I error bound. <bookmark mark='c'/> "
            "Larsson, Ramdas and Ruf linked log-optimal e-variables for specified hypothesis classes to numéraire portfolios; Fischer and "
            "Ramdas made permutation tests anytime-valid, which matters for backtests; and in 2025 Ramdas and Wang "
            "collected it all in a monograph."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:2]], lag_ratio=0.5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[2:5]], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[5:7]], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[7:]], lag_ratio=0.5))
        self.wait(0.6)
        self.clear_scene()

    def bridge(self, nu):
        d, w = np.asarray(nu["days"], float), np.asarray(nu["log10w"], float)
        g = axes([0, 2520], [float(min(w.min(), -0.5)), float(w.max()) + 0.5], x_length=6.6, y_length=4.0,
                 xlabel=r"days of a strategy with a daily Sharpe of 0.08 (simulated)", ylabel=r"$\log_{10}$ wealth",
                 xticks=[0, 1260, 2520], yticks=[0, 2, 4], font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        ln = tracing(ax, d, w, tk, QC.IDEA, stroke_width=3.5)
        l1 = label(r"Part 8: a restricted Kelly bet", font_size=28, color=DRIFT)
        l2 = label(r"Part 4: the same wealth as a test", font_size=28, color=MART)
        l1.to_corner(UR, buff=0.5)
        l2.move_to(l1).align_to(l1, RIGHT)
        side = VGroup(
            MathTex(rf"\widehat\lambda = \arg\max_{{\lambda\in[0,0.5]}} \widehat{{\mathbb E}}_{{alt}}"
                    rf"\log(1 + \lambda x) = {nu['lam']:.3f}", font_size=27),
            wrapped_label(r"Grid optimization over fixed linear stakes under a simulated alternative. "
                          r"This illustrates log growth; it does not establish optimality over all e-values "
                          r"or uniformly greatest finite-sample power.", 4.8, 19, GREY_A),
            wrapped_label(r"one object, two names: Parts 4, 8 and 9 meet here", 4.8, 21, QC.IDEA),
        )
        if side[0].width > 4.8:
            side[0].scale_to_fit_width(4.8)
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(l1, DOWN, buff=0.5).align_to(l1, RIGHT)
        with self.voiceover(
            "That bridge deserves a picture. On simulated bounded outcomes, choose a fixed linear stake from a "
            "grid between zero and one half, maximizing estimated expected log growth under the alternative. "
            "<bookmark mark='a'/> This is a restricted Kelly illustration. <bookmark mark='b'/> Under a conditional "
            "mean-zero null the same wealth is a valid test. General numéraire theory studies log-optimal e-values "
            "for specified null and alternative classes; it does not promise uniformly greatest finite-sample power."
        ) as vo:
            self.play(FadeIn(g))
            self.add(ln)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(len(d) - 1)), FadeIn(l1), run_time=4, rate_func=linear)
            ln.clear_updaters()
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(l1, l2), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def ebh(self, eb):
        days = np.asarray(eb["days"], float)
        fe, fb = np.asarray(eb["fdp_e"]), np.asarray(eb["fdp_b"])
        de, dbb = np.asarray(eb["disc_e"], float), np.asarray(eb["disc_b"], float)
        g1 = axes([0, 2520], [0, 1], x_length=5.4, y_length=3.0, xlabel=r"days; reviews every 21 days",
                  ylabel=r"mean FDP and min--max over 20 seeds", xticks=[0, 1260, 2520], yticks=[0, 0.1, 0.5, 1],
                  font_size=14)
        g2 = axes([0, 2520], [0, 30], x_length=5.4, y_length=3.0, xlabel=r"days watched", ylabel=r"discoveries",
                  xticks=[0, 1260, 2520], yticks=[0, 10, 20, 30], font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.7)
        tenp = DashedLine(g1.ax.c2p(0, 0.1), g1.ax.c2p(2520, 0.1), color=GREY_B, stroke_width=1.5)
        sb_e = seed_band(g1.ax, days, fe, MART)
        sb_b = seed_band(g1.ax, days, fb, LOSS)
        de_l = curve(g2.ax, days, de.mean(0), MART, stroke_width=3)
        db_l = curve(g2.ax, days, dbb.mean(0), LOSS, stroke_width=3)
        leg = legend([(MART, r"e-BH on ONS e-processes"), (LOSS, r"BH on one-sided known-variance $z$ p-values")], font_size=18)
        leg.arrange(RIGHT, buff=0.65).to_edge(UP, buff=0.15)
        card = lab_card(r"e-BH", [
            "def e_bh(e, alpha=0.1):",
            "    e = np.asarray(e, float); K = len(e)",
            "    order = np.argsort(e)[::-1]",
            "    ok = np.flatnonzero(e[order] >= K / (alpha * np.arange(1, K + 1)))",
            "    return order[: ok.max() + 1] if len(ok) else order[:0]",
        ], source="explainer/quant/house/martingale.py", width=6.6, font_size=17).to_corner(DL, buff=0.3)
        res = VGroup(
            MathTex(rf"\text{{first 21-day review with}} \ge 10 \text{{ discoveries:}}", font_size=24),
            MathTex(rf"\text{{FDR: e-BH }} {100 * eb['stop_e']:.1f}\%,\ \text{{BH }} {100 * eb['stop_b']:.1f}\%",
                    font_size=26, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.4)
        pred = desk_question(r"Does e-BH survive a common stopping rule based on all 200 strategies?",
                             r"Yes, if each process is valid in the joint filtration. Reported FDRs use 20 seeds; "
                             r"no action by the horizon contributes FDP zero.",
                             width=5.6, font_size=19).next_to(res, UP, buff=0.25).align_to(res, RIGHT)
        e_ok = eb["stop_e"] <= 0.1
        b_bad = eb["stop_b"] > 0.1
        verdict = ("e-BH's false discovery rate stays under ten percent; BH's rises well above it." if e_ok and b_bad
                   else "here both happen to stay near their target." if e_ok else
                   "here even e-BH overshoots, a warning about small samples of seeds.")
        with self.voiceover(
            "Finally the frontier at work on a desk problem. Two hundred strategies are watched every day for ten "
            "years; twenty have a true daily Sharpe of point zero eight, the rest none. Each is monitored by a "
            "learning e-process; the desk reviews e-BH every twenty-one trading days at ten percent. "
            "<bookmark mark='a'/> The rule is five lines: sort the e-values, and reject the largest k whose values "
            "clear the number of strategies over alpha times k. <bookmark mark='b'/> On the left, the false "
            "discovery proportion over twenty seeds; on the right, discoveries. The ordinary approach, Benjamini and "
            "Hochberg on one-sided known-variance z p-values, finds more and faster. <bookmark mark='c'/> Suppose "
            f"each method acts at its first review with ten discoveries. In these twenty seeds, {verdict} "
            "No action by the horizon counts as zero false discovery proportion. <bookmark mark='d'/> "
            "The guarantee at a common stopping time requires each e-process to be valid in the joint filtration. "
            "That condition holds in this independent-strategy simulation; the numerical average is not a proof."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(tenp), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sb_e), Create(de_l))
            self.play(FadeIn(sb_b), Create(db_l))
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
