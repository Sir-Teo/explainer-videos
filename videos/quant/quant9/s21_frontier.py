from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, answer_under, load, pause_at,
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
            history_card(2023, r"Neufeld and Sester, \textit{IEEE Trans.\ Inf.\ Theory}", r"neural networks for "
                         r"model-free pricing and martingale optimal transport: the dual's functions as networks, the "
                         r"constraint as a penalty", width=4.3, font_size=18),
            history_card(2023, r"Hasenbichler, Joseph, Loeper, Ob\l\'oj and Pammer", r"the martingale Sinkhorn "
                         r"algorithm: the martingale closest to Brownian motion between two marginals, in any "
                         r"dimension (arXiv 2310.13797, revised 2026)", width=4.3, font_size=18),
            history_card(2024, r"Engstr\"om, K\"allblad and Karlsson", r"many marginals at once: a sequential structure "
                         r"plus entropic regularization makes lookback and Asian bounds computable (arXiv 2406.09959)",
                         width=4.3, font_size=18),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        with self.voiceover(
            "Most of the recent work is in martingale optimal transport. In 2023 Ariel Neufeld and "
            "Julian Sester replaced the dual's functions with neural networks and the hedging "
            "constraint with a penalty, so the bounds scale to many assets and dates. <bookmark "
            "mark='a'/> Manuel Hasenbichler, Benjamin Joseph, Grégoire Loeper, Jan Obłój and Gudmund "
            "Pammer built a martingale version of Sinkhorn's algorithm, for the martingale closest to "
            "Brownian motion between two marginals, in any dimension. <bookmark mark='b'/> And Linn "
            "Engström, Sigrid Källblad and Johan Karlsson handle many marginals at once, enough to "
            "bound lookback and Asian options. Here is the first of these ideas, trained."
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

        rp = TrainingReplay(steps, L, frame, snaps, ylabel=r"the learned upper bound", xlabel=r"training step",
                            color=Q_C, left=LEFT * 3.6 + DOWN * 0.3, right=RIGHT * 3.2 + DOWN * 0.3)
        lpl = DashedLine(rp.ax.c2p(steps[0], lp), rp.ax.c2p(steps[-1], lp), color=CALL, stroke_width=2)
        lpt = MathTex(rf"\text{{LP}}\ {lp:.4f}", font_size=22, color=CALL).next_to(lpl, DOWN, buff=0.08).align_to(lpl, RIGHT)
        key = label(r"gold: hedge just above the claim; bright gold: touching; red: below it (penalized)", font_size=17,
                    color=GREY_A).to_edge(DOWN, buff=0.25)
        gaps = nm["gap_pct"]
        res = VGroup(*[MathTex(rf"\text{{seed }} {i}:\ {b:.4f}\ \ (+{g:.2f}\%)", font_size=22, color=Q_C)
                       for i, (b, g) in enumerate(zip(nm["bounds"], gaps))]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        res.next_to(rp.g, DOWN, buff=0.3).align_to(rp.g, LEFT)
        head = label(rf"three networks ($u$, $v$, $h$), {nm['steps']:,} steps, three seeds".replace(",", "{,}"),
                     font_size=24).to_edge(UP, buff=0.3)
        above = all(g > 0 for g in gaps)
        verdict = (f"All three land just above the program's bound, by {min(gaps):.2f} to {max(gaps):.2f} percent: "
                   "smooth networks cannot draw the hedge's kinks exactly. " if above else
                   f"They land within {max(abs(g) for g in gaps):.2f} percent of the program's bound, on both sides: "
                   "a penalized constraint is not a guarantee. ")
        with self.voiceover(
            "The House trains a neural dual on chapter fifteen's problem. Three small networks: u and "
            "v for the options at each date, h for the delta held in between. The loss is the hedge's "
            "cost plus a penalty wherever the hedge falls below the claim. <bookmark mark='a'/> On "
            "the left, the hedge minus the claim over the grid of price pairs: red where it is below, "
            "gold above, brightest where it just touches. On the right, the bound it implies, three "
            "seeds, against the linear program's line. <bookmark mark='b'/> At first the hedge is far "
            "too expensive, then too cheap and red, then it settles onto the claim. "
            f"{verdict}"
            "<bookmark mark='c'/> In one dimension the linear program wins: exact, and faster. The "
            "networks matter where the program cannot go, dozens of assets and dates."
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
            history_card(2023, r"Heston, Jacobs and Kim (Federal Reserve)", r"options alone cannot tell pricing kernels "
                         r"apart; monotonicity and path-independence, from recovery theory, remove the anomalies",
                         width=4.3, font_size=17),
            history_card(2025, r"Horvath, \textit{JFE}", r"arbitrage-based recovery: one maturity's state prices, "
                         r"26 years of S\&P 500 options (chapter 14)", width=4.3, font_size=17),
            history_card(2026, r"Shikhman, Galarnyk, Dash and Welsh, ICAIF", r"inverse learning of risk-neutral "
                         r"densities: accurate prices need not pin the density (chapter 13)", width=4.3, font_size=17),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(ORIGIN)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Beyond transport. Julien Guyon, in 2024, solved a famous puzzle, fitting the S&P 500 and "
            "VIX smiles jointly: there is no joint arbitrage exactly when a calibrating martingale "
            "measure exists, and he finds the closest one with a Sinkhorn-type algorithm. <bookmark "
            "mark='a'/> Ariel Neufeld, Antonis Papapantoleon and Qikun Xiang proved a fundamental "
            "theorem for multi-asset bounds and solved them as semi-infinite linear programs, up to "
            "sixty assets. <bookmark mark='b'/> Daniel Bartl, Mathias Beiglböck and Gudmund Pammer "
            "built a geometry on stochastic processes in which the martingales form a closed, convex "
            "set. <bookmark mark='c'/> And on the pricing kernel, Steven Heston, Kris Jacobs and "
            "Hyung Joo Kim showed that options alone cannot tell kernels apart, while recovery-style "
            "constraints remove the anomalies. The theorem is nearly fifty years old, and still a "
            "live field."
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
        card = pause_at(r"Why is a neural network's dual only approximately an upper bound?")
        with self.voiceover(
            "Pause and predict. Why is the neural dual only approximately an upper bound? <bookmark "
            "mark='a'/> The constraint is penalized, not enforced; certify the hedge on a fine grid."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"the constraint is penalized, not enforced: the hedge may dip below the "
                                                r"claim; certify by checking it on a fine grid")))
        self.wait(0.4)
        self.clear_scene()
