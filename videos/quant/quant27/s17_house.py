from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import ml as ML
from videos.quant.quant27.common import BAD, COMPLEX, GOOD, HURDLE, LINEAR, NET, PART, TREE, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("zoo"), load("theory"), load("autoenc"), load("sdf"), load("images"), load("pretrained"),
                   load("conformal"), load("envelope"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(16, r"Rule 27: the model desk", r"What must a machine-learned forecast survive before the "
                         r"House trades it?", part=PART)
        with self.voiceover("Chapter sixteen. The House's twenty-seventh rule: what a learned model must survive."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, z, t, a, s, im, p, c, e):
        rows_z = z["rows"]
        r2s = [rows_z[m]["r2"] for m in z["models"]]
        k5 = max(r["total"] for r in a["rows"] if r["model"] == "linear betas")
        rows = [(r"the zoo on 2019--20: every $R^2$ below zero; Sharpe ratios $\pm 0.7$ (s.e.)",
                 rf"{100 * min(r2s):.1f}\%\ \text{{to}}\ {100 * max(r2s):.1f}\%", BAD),
                (r"ridgeless at $\gamma = 0.9$ against theory; the misspecified model at $\gamma = 10$",
                 rf"9.0;\ \ R^2\ {100 * (1 - t['mis']['ridgeless'][-1] / t['mis']['null']):.1f}\%", COMPLEX),
                (r"one factor explains coins (total $R^2$); five linear", rf"45\%;\ {100 * k5:.1f}\%", LINEAR),
                (r"the adversarial SDF: Sharpe ratio, correlation with the market", rf"{s['sr_adv']:.2f},\ "
                 rf"{s['corr_mkt_adv']:.3f}", NET),
                (r"chart CNN against momentum, 2020", rf"{im['sr_cnn']:.2f}\ \text{{vs}}\ {im['sr_mom']:.2f}", TREE),
                (r"conformal coverage: split 90\%, adaptive on Bitcoin", rf"{100 * c['0.1']['cover']:.1f}\%,\ "
                 rf"{100 * c['btc']['cover_aci']:.1f}\%", GOOD),
                (r"NN3 on coins: research, then 2021--25", rf"{e['nn3']['row']['research']['sharpe']:.2f}\ \to\ "
                 rf"{e['nn3']['row']['holdout']['sharpe']:.2f}", NET),
                (r"the complexity timer: research, then 2021--25", rf"{e['kmz']['row']['research']['sharpe']:.2f}\ \to\ "
                 rf"{e['kmz']['row']['holdout']['sharpe']:.2f}", COMPLEX),
                (r"the trial counter", comma(e["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.2]
        tab = VGroup()
        for j, (txt, v, col) in enumerate(rows):
            y = 2.5 - 0.56 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(v, font_size=22).move_to([hx[1], y, 0])))
        title = label(r"The model desk's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"every number computed in this part from public data or simulation; none is a forecast, and "
                             r"none is advice", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> On two years of coins, every model in the zoo forecast worse than "
            "zero, and the test could not rank them. The theory of overparameterised regression matched simulation "
            "to the decimal, and explained when complexity pays. One factor explained nearly half of every week's "
            "coin returns, but its premium had the wrong sign. The adversarial discount factor learned to short the "
            "market. The chart network lost to momentum. Conformal intervals kept their promise on average, and the "
            "adaptive one kept it through the storms. And on the sealed years, the network that came last in "
            "research earned a Sharpe ratio of one point three, while the complexity timer lost a little."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The ridge risk theorem, in the House", ML.ridge_risk_theory, "atom = max", 9, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter 6's theorem is nine lines in the House. The atom of zero eigenvalues counts in the bias; below "
            "the threshold the ridgeless risk is sigma squared gamma over one minus gamma; above it, the lost signal "
            "plus the falling variance; and in general two integrals against the Marchenko-Pastur law. It is the "
            "yardstick every simulation in that chapter was checked against."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{ols}, \texttt{enet}, \texttt{pcr}, \texttt{pls}, \texttt{GBMRegressor}, \texttt{MLPEnsemble}",
             r"the zoo"),
            (r"\texttt{rff}, \texttt{ridge\_dual}, \texttt{kmz\_timing}, \texttt{kernel\_weights}", r"complexity"),
            (r"\texttt{mp\_density}, \texttt{ridge\_risk\_theory}, \texttt{ridge\_risk\_misspecified}",
             r"the theory, exact"),
            (r"\texttt{CondAutoencoder}, \texttt{AdversarialSDF}, \texttt{CrossAttention}, \texttt{ChartCNN}",
             r"modern architectures"),
            (r"\texttt{dollar\_bars}, \texttt{triple\_barrier}, \texttt{fracdiff}, \texttt{uniqueness\_weights}",
             r"the practitioner's tools"),
            (r"\texttt{split\_conformal}, \texttt{adaptive\_conformal}, \texttt{r2\_oos}, \texttt{decile\_spread}",
             r"intervals and scoring"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 8.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 27: no model is believed for its fit. A learned forecast enters the House only against a "
                             r"simple baseline at equal budget, validated walk-forward with every trial counted and the "
                             r"test's power stated; judged after economic restrictions (liquid assets, costs, value "
                             r"weights); averaged over seeds; with a conformal interval; and its complexity must pay for "
                             r"itself out of sample.", 12.4, 18, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds to the House. <bookmark mark='a'/> The zoo; complexity; the theory, exact; four "
            "modern architectures; the practitioner's tools; and intervals and scoring. <bookmark mark='b'/> And the "
            "twenty-seventh rule. No model is believed for its fit. A learned forecast enters the House only against "
            "a simple baseline given the same budget, validated walk-forward with every trial counted and the power of "
            "the test stated; judged after economic restrictions, on liquid assets, net of costs and with value "
            "weights; averaged over seeds; with a conformal interval around it; and its complexity must pay for itself "
            "out of sample."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the network that fits training perfectly", r"interpolation is not failure (Chapter 6); "
                          r"ask for the ridge path and the out-of-sample risk, and the baseline at the same budget",
                          width=12.0, font_size=19),
            desk_question(r"the zoo that cannot be ranked", r"state the test's power before the result: two years of "
                          r"forty coins cannot separate a Sharpe ratio of one from zero", width=12.0, font_size=19),
            desk_question(r"the edge in illiquid coins", r"rerun on the liquid half, value-weighted, at a realistic cost; "
                          r"what is left is the edge", width=12.0, font_size=19),
            desk_question(r"the research loser that won the hold-out", r"it was registered before the results, so it "
                          r"counts; fund it by a ramp, gated by a monitor, as Rule 26 says", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> A network that fits its training data "
            "perfectly is not thereby useless; ask for the ridge path, the out-of-sample risk and the baseline. "
            "<bookmark mark='b'/> A zoo that cannot be ranked is a statement about the test, so state its power first. "
            "<bookmark mark='c'/> An edge in illiquid coins is rerun on the liquid ones, net of costs. <bookmark "
            "mark='d'/> And the network that lost in research and won on the sealed years counts, because it was "
            "registered first; it is funded by a ramp, with a monitor, and not by its best five years."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
