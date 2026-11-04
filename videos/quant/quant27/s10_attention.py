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
        with self.voiceover("Chapter nine. Every model so far forecast each coin from its own characteristics alone. "
                            "The transformer lets every coin look at every other."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_cross(self):
        cards = VGroup(
            desk_question(r"relative, not absolute", r"a coin with high momentum means something different when every coin "
                          r"has high momentum: the cross-section is context", width=12.2, font_size=20),
            desk_question(r"leaders and laggards", r"news reaches some assets first; a forecast for the laggard should "
                          r"read the leader (Lo and MacKinlay's lead-lag, Part 7)", width=12.2, font_size=20),
            desk_question(r"the frontier", r"Kelly, Kuznetsov, Malamud and Xu (2025) put a transformer inside the "
                          r"stochastic discount factor and report large falls in pricing errors relative to earlier "
                          r"machine-learning models, from information shared across assets", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Why should one asset's forecast depend on the others? <bookmark mark='a'/> Because characteristics are "
            "relative. High momentum means one thing when it is rare and another when every coin has it. <bookmark "
            "mark='b'/> Because news reaches some assets first, and a forecast for the laggard should read the "
            "leader. <bookmark mark='c'/> And because the frontier says so: in 2025 Bryan Kelly, Boris Kuznetsov, "
            "Semyon Malamud and Teng Andrea Xu put a transformer inside the stochastic discount factor and reported "
            "large reductions in pricing errors relative to earlier machine-learning models, from information shared "
            "across assets."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
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
            MathTex(r"f_i(Z) = \rho\Big(\phi(z_i),\ \tfrac1N\textstyle\sum_j \psi(z_j)\Big)\ \ \text{(Deep Sets)}",
                    font_size=30),
            MathTex(r"a_{ij} \equiv \tfrac1N\ \Rightarrow\ \hat r_i = g\big(z_i,\ \bar v\big)", font_size=30, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3), who=r"Zaheer et al.\ (2017); Lee et al.\ (2019)", width=10.6,
            font_size=24).move_to(UP * 0.6)
        whys = VGroup(
            why(r"relabel the coins and the forecasts are relabelled the same way: attention sums over all $j$, so the "
                r"order cannot matter, and a week may hold any number of coins"),
            why(r"uniform attention collapses to the cross-sectional mean: the transformer then only conditions each "
                r"coin on this week's average coin, a learned version of demeaning"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        for w in whys:
            if w.width > 12.6:
                w.scale_to_fit_width(12.6)
        with self.voiceover(
            "One property makes this the right architecture for a cross-section, and it is a theorem. <bookmark "
            "mark='a'/> Relabel the coins, and the forecasts are relabelled the same way: attention sums over all "
            "the others, so their order cannot matter, and a week may hold any number of coins. <bookmark mark='b'/> "
            "Zaheer and coauthors showed that functions with this property are, essentially, functions of each "
            "element and of an average over the set. <bookmark mark='c'/> And at one extreme, attention that is "
            "uniform collapses to exactly that average: each coin's forecast is conditioned on this week's average "
            "coin, a learned version of the cross-sectional demeaning that every quant does by hand."
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
        sub = sub / sub.sum(1, keepdims=True)
        vmax = float(np.quantile(sub, 0.99))
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
            wrapped_label(r"the first 40 coins shown, rows renormalised; the first layer's attention, heads averaged. The "
                          r"trained model listens to nearly everyone equally: it has learned the average coin, not a "
                          r"leader", 3.8, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "What did the House's transformer learn to look at? <bookmark mark='a'/> Here is its attention in one "
            "week of 2020: each row a coin, each column the coins it listens to. <bookmark mark='b'/> It is nearly "
            "flat. Each coin puts about seven percent of its attention on its five favourite others, where uniform "
            "attention would put six and a half. The model has learned the average coin, the market, and no leaders."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(grid), Create(frame), FadeIn(xl), FadeIn(yl), run_time=1.5)
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
        foot = wrapped_label(r"both trained on mid-2018 to mid-2019, early-stopped on the second half of 2019, three seeds "
                             r"averaged; the comparison network has the same width and sees only the coin's own "
                             r"characteristics", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And the forecasts. <bookmark mark='a'/> Against a network of the same width that sees one coin at a "
            "time, the transformer does worse on both counts: an R squared of minus ten percent against minus one, "
            "and a losing long-short portfolio where the simpler network's earned point six. <bookmark mark='b'/> "
            "The extra freedom to look across coins was freedom to fit the training weeks' particular cross "
            "sections. The idea needs, again, far more weeks than coins offer; the published gains came from decades "
            "of thousands of stocks."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"prove that a one-layer attention model without positional encoding is permutation equivariant. Why "
                r"would adding a coin's alphabetical index as an input break it, and should it?")
        with self.voiceover(
            "Pause and predict. Show that one layer of attention without positional encoding is permutation "
            "equivariant. Why would adding each coin's alphabetical position as an input break the property, and "
            "should anyone want that?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
