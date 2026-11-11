from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, FullRangeReplay, answer_under, load, pause_at,
                                        real_data)


class Frontier(VoiceoverScene):
    def construct(self):
        nm, m = load("neural_mot"), load("mot")
        self.card()
        self.transport()
        self.trained(nm, m)
        self.more()
        self.predict()

    def card(self):
        c = chapter_card(18, r"The frontier, 2023 to 2026", r"Where is the theory of no arbitrage moving?",
                         lit=(2025,), part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def transport(self):
        cards = VGroup(
            history_card(2023, r"Neufeld and Sester, \textit{IEEE Trans.\ Inf.\ Theory}", r"learn model-free bounds from quotes; also fixed-marginal MOT. Earlier neural penalty methods: Eckstein and Kupper", width=4.3, font_size=18),
            history_card(2023, r"Hasenbichler, Joseph, Loeper, Ob\l\'oj and Pammer", r"the martingale Sinkhorn "
                         r"algorithm: the martingale closest to Brownian motion between two marginals, in any "
                         r"dimension (arXiv 2310.13797, revised 2026)", width=4.3, font_size=18),
            history_card(2024, r"Engstr\"om, K\"allblad and Karlsson", r"many marginals at once: a sequential structure "
                         r"plus entropic regularization makes lookback and Asian bounds computable (arXiv 2406.09959)",
                         width=4.3, font_size=18),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        with self.voiceover(
            """Three directions in recent transport work. Neufeld and Sester's 2023 paper learns model-free bounds from market inputs, with offline training for fast online pricing, and also studies fixed-marginal MOT. Neural penalty methods build on earlier work, including Eckstein and Kupper. <bookmark mark='a'/> Hasenbichler, Joseph, Loeper, Obloj and Pammer develop martingale Sinkhorn for a martingale closest to Brownian motion between marginals, under the paper's moment and feasibility assumptions. <bookmark mark='b'/> Engstrom, Kallblad and Karlsson exploit sequential structure and entropy regularization for many marginals, including lookback and Asian examples. Our next computation illustrates a neural dual penalty solver; it is not a reproduction of a paper's full empirical study."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def trained(self, nm, m):
        runs = nm["runs"]
        tr = [np.asarray(r["trace"]) for r in runs]
        steps = tr[0][:, 0]
        L = np.array([t[:, 1] for t in tr])
        lp = nm["lp"]
        gx, gy = np.asarray(nm["gx"]), np.asarray(nm["gy"])
        snaps = nm["snap_steps"]
        pay = np.abs(gy[None, :] / gx[:, None] - 1)

        def frame(i):
            H = np.asarray(runs[0]["snaps"][str(snaps[i])])
            slack = H - pay
            a = axes([gx[0], gx[-1]], [gy[0], gy[-1]], x_length=4.0, y_length=3.8, xlabel=r"$S_1 / F_1$",
                     ylabel=r"$S_2 / F_2$", xticks=[0.6, 1.0, 1.4], yticks=[0.5, 1.0, 1.5, 2.0], font_size=13)
            dx = a.ax.c2p(gx[1], 0)[0] - a.ax.c2p(gx[0], 0)[0]
            dy = a.ax.c2p(0, gy[1])[1] - a.ax.c2p(0, gy[0])[1]
            cells = VGroup()
            for p in range(len(gx)):
                for q in range(len(gy)):
                    s = slack[p, q]
                    if s < 0:
                        col, op = ARB, min(0.9, 0.3 + 3 * abs(s))
                    else:
                        col, op = HEDGE, max(0.08, 0.9 - 2.5 * s)
                    cells.add(Rectangle(width=dx, height=dy, stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                        a.ax.c2p(gx[p], gy[q])))
            t = label(rf"step {snaps[i]:,}".replace(",", "{,}"), font_size=20, color=Q_C).next_to(a, UP, buff=0.05)
            return VGroup(a, cells, t)

        rp = FullRangeReplay(steps, L, frame, snaps, ylabel=r"raw dual cost (not a certified bound)", xlabel=r"training step",
                            color=Q_C, left=LEFT * 3.6 + DOWN * 0.3, right=RIGHT * 3.2 + DOWN * 0.3)
        lpl = DashedLine(rp.ax.c2p(steps[0], lp), rp.ax.c2p(steps[-1], lp), color=CALL, stroke_width=2)
        lpt = MathTex(rf"\text{{LP}}\ {lp:.4f}", font_size=22, color=CALL).next_to(lpl, DOWN, buff=0.08).align_to(lpl, RIGHT)
        key = label(r"display window only; gold: above claim; red: constraint violation (penalized)", font_size=17,
                    color=GREY_A).to_edge(DOWN, buff=0.25)
        gaps = nm["gap_pct"]
        # one row, between the chart and the colour key at the bottom
        res = VGroup(*[MathTex(rf"\text{{seed }} {i}:\ {b:.4f}\ ({g:+.2f}\%)", font_size=21, color=Q_C)
                       for i, (b, g) in enumerate(zip(nm["bounds"], gaps))]).arrange(RIGHT, buff=0.4)
        res.next_to(key, UP, buff=0.25)
        head = label(rf"three networks ($u$, $v$, $h$), {nm['steps']:,} steps, three seeds".replace(",", "{,}"),
                     font_size=24).to_edge(UP, buff=0.3)
        deficits = [r["violation"] for r in runs]
        verdict = (f"Raw dual costs differ from the LP by {min(gaps):.2f} to {max(gaps):.2f} percent. "
                   f"Weighted mean positive shortfalls range from {min(deficits):.5f} to {max(deficits):.5f}. "
                   "These are not maximum violations and do not certify a superhedge. "
                   "The run does not isolate approximation, optimization and penalty errors. ")
        with self.voiceover(
            f"""The House restores the existing neural dual illustration. Three networks represent u and v for static payoffs and h for the position between dates. The loss is raw hedge cost plus a weighted squared-shortfall penalty. <bookmark mark='a'/> On the left, a central-window sample of hedge minus claim: red is a violation, gold is above. On the right, raw costs for all three fixed seeds, on their full stored range. <bookmark mark='b'/> The initial costs are below the LP value. Penalty optimization then overshoots to much higher costs before returning toward the LP. {verdict}<bookmark mark='c'/> For this small finite problem, the linear program is exact and faster. Neural approximations may help in larger problems, with separate feasibility and optimization checks. Neither a small weighted average shortfall nor a dense sampled window certifies the full continuum."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), Create(lpl), FadeIn(lpt), FadeIn(key))
            vo.wait_until("a")
            vo.wait_until("b")
            rp.play(self, run_time=max(vo.until("c") - 1.5, 6.0))
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def more(self):
        cards = VGroup(
            history_card(2024, r"Guyon, \textit{Finance and Stochastics}", r"joint S\&P 500 and VIX smiles: no joint "
                         r"arbitrage exactly when a calibrating martingale measure exists; the closest one found by a "
                         r"Sinkhorn-type algorithm", width=4.3, font_size=17),
            history_card(2023, r"Neufeld, Papapantoleon and Xiang, \textit{Management Science}", r"a fundamental theorem "
                         r"and super-hedging duality for multi-asset bounds, solved as semi-infinite linear programs, "
                         r"up to 60 assets", width=4.3, font_size=17),
            history_card(2026, r"Bartl, Beiglb\"ock and Pammer, \textit{JEMS}", r"the adapted Wasserstein distance on "
                         r"processes: martingales form a closed, geodesically convex subspace", width=4.3, font_size=17),
            history_card(2023, r"Heston, Jacobs and Kim (Federal Reserve)", r"kernels with different economic properties can fit options similarly; economic restrictions improve identification in their empirical model",
                         width=4.3, font_size=17),
            history_card(2025, r"Horvath, \textit{JFE}", r"arbitrage-based recovery: one maturity's state prices, "
                         r"26 years of S\&P 500 options (chapter 14)", width=4.3, font_size=17),
            history_card(2026, r"Shikhman et al., ICAIF 2026 (forthcoming)", r"inverse learning of risk-neutral "
                         r"densities: accurate prices need not pin the density (chapter 13)", width=4.3, font_size=17),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(ORIGIN)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            """Beyond transport: Guyon's 2024 framework studies joint SPX and VIX calibration and the associated no-arbitrage feasibility problem under its stated constraints. <bookmark mark='a'/> Neufeld, Papapantoleon and Xiang derive multi-asset superhedging bounds and give semi-infinite programming computations, including examples with sixty assets. <bookmark mark='b'/> Bartl, Beiglbock and Pammer develop adapted Wasserstein geometry, including closedness and geodesic convexity of martingales in their process space. <bookmark mark='c'/> Heston, Jacobs and Kim find low statistical power to distinguish economically different kernels from option fits. Monotonicity and path-independence restrictions resolve anomalies within their empirical models. Horvath's recovery study and Shikhman and coauthors' inverse-density analysis are further examples; each conclusion depends on its model, data and assumptions."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards[3:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"When does a neural dual cost become a certified upper bound?")
        with self.voiceover(
            """Pause and predict. When is a neural dual cost a certified upper bound? <bookmark mark='a'/> Only after establishing hedge dominance on the claim's full support. A penalty does not enforce the constraint. Checking every pair in a finite support can certify that discrete problem; a dense sample alone does not certify a continuum."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"penalty alone gives no bound; certify all finite-support pairs, or prove interpolation and tail control for a continuum")))
        self.wait(0.4)
        self.clear_scene()
