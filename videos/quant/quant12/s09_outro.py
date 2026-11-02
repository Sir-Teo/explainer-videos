from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load

DESK = [
    (r"Why is the VIX above realized volatility on average?",
     r"because variance is insurance: it spikes when wealth falls, so buyers pay a premium (Carr and Wu 2009); on two "
     r"years of bitcoin surfaces, implied variance exceeded realized in three weeks out of four"),
    (r"Replicate a variance swap with options.",
     r"hold $\frac{2}{T}\frac{dK}{K^2}$ of every out-of-the-money option (puts below the forward, calls above) and "
     r"delta-hedge with the future; the strip is a log contract, and It\^o turns it into realized variance"),
    (r"A dealer's book is short gamma near a big open-interest strike as expiry approaches. What do its hedges do?",
     r"they chase the market: buying rallies and selling dips, which amplifies moves (Baltussen et al.\ 2021); long "
     r"gamma would damp them and pin the price near the strike"),
]

PROBLEMS = [
    r"From $C(K, T)$ and the forward equation, derive Dupire's formula $\sigma^2_{loc} = \partial_T C / (\frac12 K^2 "
    r"\partial_{KK} C)$ at zero rates.",
    r"Show that $-\log(S_T/F)$ equals a forward position plus a strip of options weighted $1/K^2$, and hence derive "
    r"the variance-swap strike.",
    r"For SSVI, check Gatheral and Jacquier's calendar condition: $\theta_T$ non-decreasing and $0 \le "
    r"\partial_\theta(\theta\varphi(\theta)) \le \frac{1 + \sqrt{1 - \rho^2}}{\rho^2}\varphi(\theta)$, for the power-law "
    r"$\varphi$.",
    r"Show that near the money, local-volatility skew is about twice the implied skew: $\partial_k\sigma_{loc} "
    r"\approx 2\,\partial_k\sigma_{imp}$.",
    r"Derive Martin's bound: if $\text{cov}(m_T R_T, R_T) \le 0$, then $\mathbb{E}[R_T] - R_f \ge \text{var}^Q(R_T)/R_f$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("surface"), load("varswap"), load("history"), load("localvol"), load("vae"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, w, h, lv, v):
        items = [
            (r"the surface is the market's map of fear: smile, skew, term structure", IV),
            (rf"next-day quotes followed the spot: sticky moneyness {s['sticky_rmse']['sticky moneyness']:.1f} vs sticky "
             rf"strike {s['sticky_rmse']['sticky strike']:.1f} vol points", SPOT),
            (rf"SSVI fits the Surface to {s['rmse_ssvi']:.2f} vol points with no arbitrage", LV),
            (rf"local volatility reprices today but flattens tomorrow: forward skew {100 * lv['fwd_skew']:.1f} vs "
             rf"{100 * lv['spot_skew']:.1f} points", BAD),
            (rf"a variance swap is a strip of options: {100 * w['kvar']:.0f}\% vs {100 * w['atm']:.0f}\% at the money", OPT),
            (rf"bitcoin's variance premium: positive {100 * h['share_positive']:.0f}\% of weeks, $t = {h['vrp_t']:.1f}$", RV),
            (r"Volmageddon: when everyone is short volatility, the hedging is the shock", BAD),
            (rf"two learned numbers rebuild a surface to {v['recon_rmse_volpts']:.1f} vol points", LV),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 12 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part twelve in eight lines. The surface is the market's map of fear. On our day, the smile moved with "
            "the spot. SSVI fits it without arbitrage to a fraction of a volatility point. Local volatility reprices "
            "today's options and gets tomorrow's smile wrong. A variance swap is a strip of options, priced above "
            "at-the-money volatility. Bitcoin's variance premium was positive three weeks in four. When everyone is "
            "short volatility, their hedging becomes the shock. And two learned numbers rebuild a whole surface."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. The VIX sits above realized volatility because variance is insurance. "
            "<bookmark mark='a'/> A variance swap is replicated by every out-of-the-money option, weighted by one "
            "over the strike squared, and a delta hedge. <bookmark mark='b'/> And a dealer short gamma into expiry "
            "chases the market; long gamma, it pins it. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: Dupire's formula, the log contract's strip, SSVI's calendar condition, the local "
            "skew's factor of two, and Martin's bound. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"stochastic volatility and jumps, which fix the forward smile", [13]),
            (r"rough volatility and path-dependent models", [14]),
            (r"exotics priced off the surface", [15]),
            (r"computing prices: PDEs, Monte Carlo, Fourier", [16]),
            (r"the variance premium as a factor", [24, 32]),
        ])
        with self.voiceover(
            "Where this comes back. Stochastic volatility and jumps, in Part thirteen, fix the forward smile. Rough "
            "volatility follows. Exotics in Part fifteen are priced off this surface, with the methods of Part "
            "sixteen. And the variance premium returns as a factor and a strategy."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gatheral, \textit{The Volatility Surface}; Bergomi, \textit{Stochastic Volatility Modeling}, ch.\ 1--2",
             r"Rebonato, \textit{Volatility and Correlation}; Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 20, 27"],
            [r"Dupire (1994); Derman and Kani (1994); Gy\"ongy (1986); Carr and Madan (1998)",
             r"Demeterfi, Derman, Kamal and Zou (1999); Lee (2004); Gatheral (2004); Gatheral and Jacquier (2014)",
             r"Carr and Wu (2009); Bollerslev, Tauchen and Zhou (2009); Martin (2017)",
             r"Baltussen, Da, Lammers and Martens (2021); Bergeron, Fung, Hull and Poulos (2022); Kingma and Welling (2014)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. The data are the Surface and a hundred "
            "weekly surfaces rebuilt from Deribit's trades, Binance's Bitcoin prices, and the VIX from the St. Louis Fed."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 13, Stochastic Volatility and Jumps", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now read, fit and trade the surface. <bookmark mark='a'/> Next, Part thirteen: "
            "stochastic volatility and jumps. Heston, SABR and Bates, calibrated to the Surface, and why their smiles "
            "move the way real ones do."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
