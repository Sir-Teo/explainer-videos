from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART, VALUE, load


class Frontier(VoiceoverScene):
    def construct(self):
        f = load("forecaster")
        self.card()
        self.forecasts()
        self.llms()
        self.replication()
        self.replay(f)

    def card(self):
        c = chapter_card(18, r"Frontier: machines reading the statements", r"Can a model forecast earnings better "
                         r"than an analyst?", lit=(2025,), part=PART)
        with self.voiceover("Chapter eighteen. The frontier: machines reading the statements."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def forecasts(self):
        a = firm_card(r"Man versus machine learning",
                      r"An unbiased machine-learning forecast of earnings as the benchmark: analysts' forecasts are "
                      r"biased upward, more so at long horizons, and the bias predicts low returns; common linear "
                      r"models did worse than the analysts out of sample.",
                      source=r"van Binsbergen, Han and Lopez-Lira, RFS 36(6), 2023", width=4.3, font_size=18)
        b = firm_card(r"... revisited",
                      r"A reply attributes the machine's edge to look-ahead in its inputs: without it, linear models "
                      r"forecast as accurately. The original authors dispute this. Unsettled.",
                      source=r"Zhang, Zhu and Linnainmaa, RFS 38(12), 2025", width=4.3, font_size=18)
        c = firm_card(r"Man plus machine",
                      r"An AI model trained on disclosures beat most analysts' stock forecasts; analysts did better "
                      r"where institutional knowledge mattered (intangibles, distress, small illiquid firms), and the "
                      r"combination beat both.", source=r"Cao, Jiang, Wang and Yang, JFE 160, 2024", width=4.3,
                      font_size=18)
        VGroup(a, b, c).arrange(RIGHT, buff=0.25, aligned_edge=UP).scale_to_fit_width(13.4).move_to(UP * 0.2)
        with self.voiceover(
            "The frontier is machines that read statements. In 2023 Jules van Binsbergen, Xiao Han and Alejandro "
            "Lopez-Lira built a machine-learning forecast of earnings as an unbiased benchmark and found analysts' "
            "forecasts biased upward, more so at long horizons, with the bias predicting low returns; the usual "
            "linear models did worse than the analysts. <bookmark mark='a'/> In 2025 a reply in the same journal "
            "argued that the machine's edge came from information it could not have had in real time, and that "
            "without it linear models forecast as well; the original authors dispute that. It is unsettled, and it is "
            "the point-in-time problem of chapter five again. <bookmark mark='b'/> Sean Cao and coauthors trained "
            "a model on disclosures and found it beat most analysts' stock forecasts, while analysts kept the edge "
            "where institutional knowledge mattered, and the two together beat either."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def llms(self):
        w = crisis_card(r"2024 -- 2025", r"Two papers withdrawn",
                        r"Kim, Muhn and Nikolaev's ``Financial statement analysis with large language models'' (arXiv "
                        r"2407.17866) reported GPT-4 beating analysts at predicting earnings changes. Its authors "
                        r"withdrew it in 2025 while they review the findings. Their ``Bloated disclosures'' (arXiv "
                        r"2306.10224) was withdrawn after a co-author's replication did not support it.",
                        width=6.4, font_size=20)
        fb = firm_card(r"FinanceBench",
                       r"150 questions about public filings, with answers checked by hand. GPT-4-Turbo with a "
                       r"retrieval system answered 81\% of them wrongly or not at all.",
                       numbers=[(r"81\%", r"wrong or refused")], source=r"Islam et al., arXiv 2311.11944 (2023)",
                       width=6.0, font_size=20)
        VGroup(w, fb).arrange(RIGHT, buff=0.35, aligned_edge=UP).scale_to_fit_width(13.3).move_to(UP * 0.2)
        with self.voiceover(
            "Large language models arrived in this literature fast, and so did a cautionary tale. A widely read 2024 "
            "working paper reported that GPT-4, given anonymised statements, predicted the direction of earnings "
            "changes better than analysts. Its authors withdrew it in 2025 while they review the findings, and an "
            "earlier paper of theirs was withdrawn after a co-author's own replication did not support it. Neither is "
            "a finding; both are reminders to replicate. <bookmark mark='a'/> On plain questions about filings the "
            "record is sobering: in the FinanceBench test of 2023, GPT-4-Turbo with document retrieval answered "
            "eighty-one percent of a hundred and fifty questions wrongly or not at all. Part twenty-eight measures "
            "newer models."
        ) as vo:
            self.play(FadeIn(w, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(fb, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def replication(self):
        cards = VGroup(
            firm_card(r"Is there a replication crisis?",
                      r"153 factors in 93 countries: most replicate, cluster into 13 themes, and hold up out of sample, "
                      r"in a Bayesian framework that shrinks each towards its theme.",
                      source=r"Jensen, Kelly and Pedersen, JF 78(5), 2023", width=4.3, font_size=18),
            firm_card(r"Duration-driven returns",
                      r"Firms whose cash flows arrive sooner have earned higher returns: a duration factor, chapter 2's "
                      r"object priced in the cross-section.", source=r"Gormsen and Lazarus, JF 78(3), 2023", width=4.3,
                      font_size=18),
            firm_card(r"Intangible value",
                      r"Count capitalised intangibles in book value, and value works again: chapter 8's book is not "
                      r"the economist's capital.", source=r"Eisfeldt, Kim and Papanikolaou, CFR 11(2), 2022", width=4.3,
                      font_size=18),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).scale_to_fit_width(13.4).move_to(UP * 0.2)
        with self.voiceover(
            "Three more threads. Theis Jensen, Bryan Kelly and Lasse Pedersen asked in 2023 whether finance has a "
            "replication crisis, and on a hundred and fifty-three factors in ninety-three countries answered mostly "
            "no: the counterweight to chapter fourteen's decay. <bookmark mark='a'/> Niels Gormsen and Eben Lazarus "
            "found that firms whose cash flows come sooner earn higher returns, pricing chapter two's duration. "
            "<bookmark mark='b'/> And Andrea Eisfeldt, Edward Kim and Dimitris Papanikolaou showed that counting "
            "intangible capital in book value changes what value investing finds: the book in chapter eight's formula "
            "is an accounting choice."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, f):
        ep = np.asarray(f["epochs"], float)
        V = np.asarray(f["val_curves"]) * 1e4
        snaps = np.asarray(f["snaps"])
        y = np.asarray(f["y_test"])
        res = f["res"]
        best = int(f["best_seed"])
        L = np.vstack([V[best:best + 1], np.delete(V, best, axis=0)])
        ck_idx = [0, 2, 5, 9, 13, 17, len(ep) - 1]

        def frame(k):
            i = ck_idx[k]
            a = axes([-0.1, 0.2], [-0.1, 0.2], x_length=3.6, y_length=3.6, xlabel=r"realised", ylabel=r"predicted",
                     xticks=[0, 0.1, 0.2], yticks=[0, 0.1, 0.2], font_size=14)
            pts = VGroup(*[Dot(a.ax.c2p(np.clip(u, -0.1, 0.2), np.clip(v, -0.1, 0.2)), radius=0.025, color=QC.Q,
                               fill_opacity=0.6) for u, v in zip(y[:250], snaps[i][:250])])
            diag = DashedLine(a.ax.c2p(-0.1, -0.1), a.ax.c2p(0.2, 0.2), color=GREY_C, stroke_width=1.5)
            return VGroup(a, diag, pts)

        rp = TrainingReplay(ep, L, frame, [ep[i] for i in ck_idx], ylabel=r"validation error ($\times 10^{-4}$)",
                            xlabel=r"epoch", left=LEFT * 3.6 + DOWN * 0.3, right=RIGHT * 3.0 + DOWN * 0.3,
                            x_length=5.0, y_length=3.4)
        ax = rp.ax
        base = VGroup()
        for key, col, name in (("ols", CASH, r"OLS"), ("ridge", VALUE, r"ridge on splines")):
            v = res[key] * 1e4
            yv = float(np.clip(v, rp.lo, rp.hi))
            ln = DashedLine(ax.c2p(ep[0], yv), ax.c2p(ep[-1], yv), color=col, stroke_width=2)
            base.add(VGroup(ln, label(name, font_size=15, color=col).next_to(ln, RIGHT, buff=0.08)))
        mlp, ols, ridge, rw = res["mlp"], res["ols"], res["ridge"], res["rw"]
        spread = float(np.ptp(f["mlp_test"]))
        beats = (ols - mlp) > spread
        tab = VGroup(
            label(r"test error, years 11--12 ($\times 10^{-4}$):", font_size=19, color=GREY_A),
            MathTex(rf"\text{{random walk}}\ {rw * 1e4:.2f}\quad \text{{OLS}}\ {ols * 1e4:.2f}\quad "
                    rf"\text{{ridge}}\ {ridge * 1e4:.2f}\quad \text{{MLP}}\ {mlp * 1e4:.2f}", font_size=24),
            MathTex(rf"\text{{MLP across 5 seeds: }}{f['mlp_test'].min() * 1e4:.3f}\text{{--}}"
                    rf"{f['mlp_test'].max() * 1e4:.3f};\ \ \text{{noise floor}}\ {f['floor'] * 1e4:.2f}", font_size=22,
                    color=QC.Q),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.25)
        head = label(rf"simulated panel, truth known: 14 items, {f['n_train']:,} training firm-years; MLP {f['config']}; "
                     r"replayed: the best seed on validation".replace(",", "{,}"), font_size=17,
                     color=GREY_B).to_edge(UP, buff=0.3)
        gain = 100 * (ols - mlp) / ols
        verdict = (f"The network beats least squares by {gain:.1f} percent, more than its seed spread, because it can "
                   "learn that losses fade faster than profits; ridge on splines, which can bend too, ties it. "
                   if beats else "The network does not beat least squares by more than its own seed spread. ")
        with self.voiceover(
            "The House trains its own small forecaster, on a simulated panel whose truth we know: profits persist "
            "with point eight, losses only with point four, accruals carry a reversing error, and three of the "
            "fourteen items are pure noise. Next year's earnings over assets is the target. The models get equal "
            "data: a random walk, ordinary least squares, ridge regression on splines, and a two-layer neural network, "
            "five seeds. <bookmark mark='a'/> Here the network learns. On the right its validation error, with the "
            "spread of five seeds as a band and the linear baselines as dashed lines; on the left, its predictions "
            "for the test years against what happened, tightening around the diagonal. <bookmark mark='b'/> The "
            f"verdict. The random walk, {rw * 1e4:.2f}; least squares, {ols * 1e4:.2f}; the network, {mlp * 1e4:.2f}. "
            + verdict + f"All of them sit just above the noise floor of {f['floor'] * 1e4:.2f}. With clean, low-dimensional "
            "inputs, a flexible model has little to find; the frontier's fights are about the inputs, not the network."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), FadeIn(base))
            vo.wait_until("a")
            rp.play(self, run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()
