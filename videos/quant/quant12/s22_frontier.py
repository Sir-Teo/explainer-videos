from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


class Frontier(VoiceoverScene):
    def construct(self):
        o = load("operator_net")
        self.card()
        self.papers()
        self.replication(o)
        self.more()

    def card(self):
        c = chapter_card(19, r"Frontier, 2023--2026", r"What is new in surfaces?", lit=(2025,), part=PART)
        with self.voiceover("Chapter nineteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def papers(self):
        cards = VGroup(
            firm_card(r"Operator deep smoothing (ICLR 2025)",
                      r"Wiedemann, Jacquier and Gonon: a graph neural operator maps a day's raw quotes straight to a smooth "
                      r"surface, one network for every day, trained on a decade of intraday S\&P 500 options and respecting "
                      r"no-arbitrage constraints. Chapter 17 trained one network per surface; this trains one for all.",
                      width=6.3, font_size=19),
            firm_card(r"VolGAN (Applied Mathematical Finance, 2024)",
                      r"Vuleti\'c and Cont: a generative adversarial network that simulates tomorrow's whole surface "
                      r"together with the index, re-weighting its scenarios to remove arbitrage; used to test hedging "
                      r"strategies. Chapter 17's autoencoder walk, made dynamic.", width=6.3, font_size=19),
            firm_card(r"Surfaces as images for returns (2023)",
                      r"Kelly, Kuznetsov, Malamud and Xu: implied-volatility surfaces of individual stocks, read like "
                      r"images by an ensemble of machine-learning models, predict the cross-section of stock returns out "
                      r"of sample (Part 27).", width=6.3, font_size=19),
            firm_card(r"No-arbitrage SVI and eSSVI (2022)",
                      r"Martini and Mingone: the exact region of raw SVI parameters free of butterfly arbitrage, and a "
                      r"global parametrization of eSSVI (maturity-dependent $\rho$) free of all static arbitrage.", width=6.3,
                      font_size=19),
        )
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "Four lines of current research, each checked against the paper. Ruben Wiedemann, Antoine Jacquier and "
            "Lukas Gonon, at ICLR in 2025: operator deep smoothing. Instead of fitting one network per surface, as in "
            "Chapter seventeen, they train one neural operator that maps any day's raw quotes straight to a smooth "
            "surface, on ten years of intraday S&P 500 options, with the no-arbitrage conditions built into training. "
            "<bookmark mark='a'/> Milena Vuletić and Rama Cont's VolGAN generates tomorrow's whole surface together "
            "with the index, re-weighting its scenarios so that they are free of arbitrage, and uses them to test "
            "hedges: the autoencoder's walk, made dynamic. <bookmark mark='b'/> Bryan Kelly and co-authors read the "
            "surfaces of individual stocks as images and find that they forecast which stocks will outperform, out of "
            "sample: Part twenty-seven's subject. <bookmark mark='c'/> And Claude Martini and Arianna Mingone settled two "
            "of this part's open questions: the exact set of SVI parameters with no butterfly arbitrage, and a global "
            "arbitrage-free version of SSVI whose tilt can change with maturity."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
            vo.wait_until("c")
            self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def replication(self, o):
        R = o["runs"]
        H = [np.asarray(r["hist"]) for r in R]
        steps = H[0][:, 0]
        te = np.array([h[:, 2] for h in H])
        tr = np.array([h[:, 1] for h in H])
        hi = float(max(te.max(), tr.max(), o["dec_rmse"], o["ssvi_rmse"]) * 1.05)
        g = axes([0, steps[-1]], [0, hi], x_length=6.4, y_length=4.0, xlabel=r"training step",
                 ylabel=r"RMSE (vol points)", xticks=[0, steps[-1]], xfmt=lambda u: f"{u:,.0f}".replace(",", "{,}"),
                 yticks=[0, round(hi / 2), round(hi)], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        bt = seed_band(g.ax, steps, np.clip(tr, 0, hi), LV)
        bte = seed_band(g.ax, steps, np.clip(te, 0, hi), IV)
        dec = DashedLine(g.ax.c2p(0, o["dec_rmse"]), g.ax.c2p(steps[-1], o["dec_rmse"]), color=GREY_B)
        ss = DashedLine(g.ax.c2p(0, o["ssvi_rmse"]), g.ax.c2p(steps[-1], o["ssvi_rmse"]), color=OPT)
        leg = legend([(LV, r"training weeks"), (IV, r"held-out weeks (the last 20\%)"),
                      (GREY_B, 'two-component PCA, fitted on all weeks'),
                      (OPT, r"SSVI fitted to each held-out week itself")], font_size=16).next_to(g, UP, buff=0.1
                                                                                                ).align_to(g, LEFT)
        mt = float(np.mean([r["test"] for r in R]))
        beats_dec = mt < o["dec_rmse"]
        beats_ssvi = mt < o["ssvi_rmse"]
        side = VGroup(
            wrapped_label("latent-conditioned IV regression; the full-sample VAE and each test week's entire grid supply its two codes", 4.6, 19, GREY_A),
            MathTex(rf"\text{{held out: }} {mt:.2f}\ \text{{vs PCA}}\ {o['dec_rmse']:.2f}\ \text{{vs SSVI}}\ "
                    rf"{o['ssvi_rmse']:.2f}", font_size=26, color=IV),
            wrapped_label('PCA and VAE use all weeks; SSVI fits test quotes. Conditional reconstruction, not a predictive race.', 4.6, 18,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"{o['n_quotes']:,} quotes from {o['n_weeks']} weekly Deribit surfaces; three seeds".replace(",", "{,}"))
        d, s_ = o["dec_rmse"], o["ssvi_rmse"]
        first = o["first_test_day"]
        b1 = ("The network beats the decoder: reading the quotes directly helps. " if beats_dec else
              "The network does not beat the decoder: the two numbers, not the network, set the limit. ")
        b2 = ("the network even beats it, " if beats_ssvi else "fitted to each week it does better, ")
        with self.voiceover(
            f"""Here is a latent-conditioned regression illustration, rather than a replication of the graph neural operator. It takes log-moneyness, square-root maturity, and two codes from the week's entire fitted grid. The final regressor trains on the first eighty percent of weeks and holds out weeks from {first}. But the autoencoder was fitted on all weeks, including those later dates; their full current grids also supply their codes. These are conditional reconstruction checks, not fully unseen-date forecasts. <bookmark mark='a'/> Across three seeds the regressor's error is {mt:.2f} volatility points. The {d:.2f} baseline is a two-component PCA fitted to all weeks, with its reconstructed grid clamped to the supported coordinates. It is not the autoencoder decoder. SSVI's {s_:.2f} error uses fits to each test week's own quotes. These methods condition on different information and are not a fair predictive race."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(leg), FadeIn(bt), FadeIn(bte), Create(dec), Create(ss))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def more(self):
        rows = VGroup(
            wrapped_label(r"0DTE surfaces: Bandi, Fusari and Ren\`o (2023), Chapter 16", 11.6, 22, GREY_A),
            wrapped_label(r"joint S\&P 500 and VIX smiles, rough and path-dependent volatility (Guyon and Lekeufack 2023; "
                          r"signature models): Part 14", 11.6, 22, GREY_A),
            wrapped_label(r"neural calibrators and market generators: Part 17", 11.6, 22, GREY_A),
            wrapped_label(r"pause and predict: a generator of surfaces passes the arbitrage checker every day. Is it a good "
                          r"risk model?", 11.6, 22, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN)
        with self.voiceover(
            "Elsewhere on the frontier: same-day option surfaces, which Chapter sixteen met; the joint fitting of S&P "
            "500 and VIX smiles with path-dependent and rough volatility, which is Part fourteen; and neural "
            "calibrators and market generators, which are Part seventeen. <bookmark mark='a'/> Pause and predict: a "
            "generator of surfaces passes the arbitrage checker every single day. Is it a good risk model? Not "
            "necessarily. Static no-arbitrage says nothing about how surfaces move or how large the tails are; "
            "Part forty tests risk models on exactly that."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:3]], lag_ratio=0.4, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
