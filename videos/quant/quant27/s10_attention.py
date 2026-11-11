from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, fit_right, load


class Attention(VoiceoverScene):
    def construct(self):
        a = load("attention")
        self.card()
        self.why_cross()
        self.mechanism()
        self.equivariance()
        self.heat(a)
        self.result(a)
        self.question()

    def card(self):
        c = chapter_card(9, r"Attention across assets", r"Should one coin's forecast depend on every other coin?",
                         lit=(2025,), part=PART)
        with self.voiceover('Chapter nine. The pointwise models already use cross-sectional ranks. Attention adds learned set interactions beyond that relative preprocessing.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_cross(self):
        cards = VGroup(
            desk_question(r"relative, not absolute", 'Inputs already contain cross-sectional ranks. Set interactions can add relationships beyond that relative preprocessing.', width=12.2, font_size=29),
            desk_question(r"leaders and laggards", 'Lead-lag dependence is a hypothesis to test with matched information and timing; this comparison does not identify it.', width=12.2, font_size=29),
            desk_question(r"the frontier", 'Kelly, Kuznetsov, Malamud and Xu (2025) report pricing improvements in their own stock study. This crypto illustration is not a replication or causal ablation.', width=12.2, font_size=29),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Why model a set of assets jointly? <bookmark mark='a'/> Cross-sectional context may change the interpretation of a characteristic, although our inputs already encode ranks among peers. <bookmark mark='b'/> Interactions may represent shared states or lead-lag structure, but the saved model comparison does not establish either mechanism. <bookmark mark='c'/> Published asset-pricing transformers motivate exploring these interactions. Their reported improvements concern their own data and evaluation designs; our smaller crypto example is not a replication."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def mechanism(self):
        rows = [cmath(r"h_i", r"=", r"E\, z_i", font_size=32, colors={r"h_i": COIN}),
                cmath(r"q_i,\ k_i,\ v_i", r"=", r"W_Q h_i,\ \ W_K h_i,\ \ W_V h_i", font_size=32,
                      colors={r"q_i,\ k_i,\ v_i": NET}),
                cmath(r"a_{ij}", r"=", r"\frac{\exp(q_i^{\top}k_j/\sqrt{d})}{\sum_{l} \exp(q_i^{\top}k_l/\sqrt{d})}",
                      font_size=32, colors={r"a_{ij}": HURDLE}),
                cmath(r"\hat r_i", r"=", r"w^{\top}\,\mathrm{FFN}\Big(h_i + \textstyle\sum_j a_{ij}\, v_j\Big)", font_size=32,
                      colors={r"\hat r_i": GOOD})]
        whys = [why(r"embed each coin's fifteen characteristics in $d = 32$ dimensions"),
                why(r"each coin asks a question (query), advertises what it has (key) and offers content (value)"),
                why(r"how much coin $i$ listens to coin $j$: a softmax of query--key similarity across this week's coins, "
                    r"summing to one (AI, Built, Part 13)"),
                why(r"coin $i$'s forecast reads its own embedding plus a weighted average of every coin's values; four "
                    r"heads, one layer, trained on mean squared error")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The mechanism is AI, Built's thirteenth part, applied to a cross-section. <bookmark mark='a'/> Embed each "
            "coin's characteristics. <bookmark mark='b'/> From the embedding, each coin forms a query, what it is "
            "looking for; a key, what it offers to be found by; and a value, what it contributes. <bookmark mark='c'/> "
            "Coin i's attention to coin j is a softmax of how well its query matches j's key, across all the coins "
            "of that week. <bookmark mark='d'/> And its forecast reads its own embedding plus the attention-weighted "
            "average of everyone's values. One layer, four heads, trained like every other model here."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def equivariance(self):
        thm = theorem_card(r"Permutation equivariance", VGroup(
            MathTex(r"f(\Pi Z) = \Pi f(Z)\ \ \text{for every permutation}\ \Pi", font_size=30),
            MathTex(r"f_i(Z) = \rho\Big(\phi(z_i),\ \tfrac1N\textstyle\sum_j \psi(z_j)\Big)\ \ \text{(fixed size; representation conditions)}",
                    font_size=30),
            MathTex(r"a_{ij} \equiv \tfrac1N\ \Rightarrow\ \hat r_i = g\big(z_i,\ \bar v\big)", font_size=30, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3), who=r"Zaheer et al.\ (2017); Lee et al.\ (2019)", width=10.6,
            font_size=24).move_to(UP * 0.6)
        whys = VGroup(
            why(r"relabel the coins and the forecasts are relabelled the same way: attention sums over all $j$, so the "
                r"order cannot matter, and a week may hold any number of coins"),
            why('Uniform attention averages learned values. It does not automatically demean returns, identify the market, or preserve variable set cardinality.'),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        for w in whys:
            if w.width > 12.6:
                w.scale_to_fit_width(12.6)
        with self.voiceover(
            "One useful property is permutation equivariance. <bookmark mark='a'/> Shared rowwise maps and attention without fixed slot embeddings relabel forecasts when the inputs are relabelled. This symmetry does not guarantee accuracy. <bookmark mark='b'/> Deep Sets representations need regularity, cardinality and latent-dimension conditions. A plain mean loses set size unless size is supplied or fixed. <bookmark mark='c'/> Uniform attention averages learned value vectors. That operation is not automatically demeaning, identifying a market factor or demonstrating that no leaders exist."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(whys[0]))
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.play(FadeIn(whys[1]))
        self.wait(0.4)
        self.clear_scene()

    def heat(self, a):
        A = np.asarray(a["attention"], float)
        n = A.shape[0]
        k = min(n, 40)
        sub = A[:k, :k]
        sub = sub.copy()
        vmax = float(sub.max())
        cell = 5.2 / k
        grid = VGroup()
        for i in range(k):
            for j in range(k):
                v = min(sub[i, j] / max(vmax, 1e-12), 1.0)
                grid.add(Square(side_length=cell, stroke_width=0, fill_color=interpolate_color(ManimColor(BLACK), ManimColor(HURDLE), v),
                                fill_opacity=1).move_to(np.array([(j - k / 2) * cell, (k / 2 - i) * cell, 0])))
        grid.move_to(LEFT * 2.6 + DOWN * 0.2)
        frame = SurroundingRectangle(grid, color=GREY_C, buff=0.02, stroke_width=1.5)
        xl = label(r"coin $j$ (listened to)", font_size=16, color=GREY_A).next_to(frame, DOWN, buff=0.15)
        yl = label(r"coin $i$", font_size=16, color=GREY_A).next_to(frame, LEFT, buff=0.15)
        wk = str(a["example"]["week"])
        uni = 5 / a["n_assets"]
        side = VGroup(
            MathTex(rf"\text{{week of}}\ {wk[:4]}\text{{-}}{wk[4:6]}\text{{-}}{wk[6:]},\ {a['n_assets']}\ \text{{coins}}",
                    font_size=22),
            MathTex(rf"\text{{weight on its top 5}}:\ {100 * a['top5_share']:.1f}\%", font_size=24, color=HURDLE),
            MathTex(rf"\text{{uniform would give}}:\ {100 * uni:.1f}\%", font_size=24, color=GREY_B),
            wrapped_label('First 40 rows and columns of one selected seed/week; original head-averaged values, without renormalisation. Colour spans zero to the displayed maximum; omitted columns retain the remaining row mass.', 3.8, 23, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        side.add(MathTex(rf"\text{{colour scale: }}0\text{{--}}{vmax:.4f}",font_size=24,color=HURDLE).next_to(side,DOWN,buff=.2).align_to(side,LEFT))
        fit_right(side)
        with self.voiceover(
            f"Inspect one selected seed and week, with attention heads averaged. <bookmark mark='a'/> The matrix shows the first {k} rows and columns with original weights and a zero-to-maximum colour scale. Omitted columns retain the remaining mass. <bookmark mark='b'/> The saved full-matrix top-five share is {100*a['top5_share']:.2f} percent, compared with uniform {100*uni:.2f} percent over {a['n_assets']} assets. This descriptive heatmap does not establish attention behaviour in all weeks, causal feature importance or the absence of leaders."
        ) as vo:
            self.add(grid,frame,xl,yl)
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def result(self, a):
        r = a["rows"]
        hx = [-3.0, 1.6, 4.6]
        head = VGroup(label(r"coins, test year 2020", font_size=18, color=GREY_B),
                      label(r"attention", font_size=20, color=NET), label(r"one coin at a time", font_size=20, color=TREE))
        data = [(r"$R^2_{\text{oos}}$", rf"{100 * r['attention']['r2']:.1f}\%", rf"{100 * r['pointwise']['r2']:.1f}\%"),
                (r"quintile long-short Sharpe", rf"{r['attention']['sr_ew']:.2f}", rf"{r['pointwise']['sr_ew']:.2f}")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(x, font_size=18, color=GREY_A), MathTex(b, font_size=26),
                                                 MathTex(c, font_size=26)) for x, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.7 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.8, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label('Original selected architectures and training schedules differ. Both receive cross-sectional ranks. Gross performance and one selected heatmap do not isolate a causal attention effect.', 11.6, 23, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"The original research comparison reports zero-benchmark R squared of {100*r['attention']['r2']:.2f} percent for attention and {100*r['pointwise']['r2']:.2f} for the pointwise network. <bookmark mark='a'/> Their gross long-short Sharpes are {r['attention']['sr_ew']:.3f} and {r['pointwise']['sr_ew']:.3f}. <bookmark mark='b'/> Both use ranked relative inputs. Their parameter counts, training effort and architectures differ, so the comparison is not a pure attention ablation. The outputs do not isolate sample size, overfitting or a learned market factor as the cause."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q=ask(r"Prove attention's row-permutation equivariance. Which breaks it: a fixed row-slot embedding, or an asset identity that moves with the asset when rows are permuted? State the distinction.")
        with self.voiceover("Pause and predict. Prove attention's row-permutation equivariance. Distinguish a fixed row-slot embedding from an asset identity or alphabetical rank that moves with the asset. The latter need not break reindexing equivariance."):
            self.play(FadeIn(q))
        self.clear_scene()
