from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAUSS, LOSS, PART, REAL, TAIL, VOL, load, real_data

# the facts, each as one number: (key, label, how a model passes)
FACTS = [
    ("kurt", r"fat tails: excess kurtosis", "rel"),
    ("alpha", r"tail exponent $\alpha$ (Hill)", "rel"),
    ("acf1_r", r"no linear memory: $\rho_1(r)$", "small"),
    ("acf1_abs", r"clustering: $\rho_1(|r|)$", "rel"),
    ("acf100_abs", r"long memory: $\rho_{100}(|r|)$", "rel"),
    ("lev", r"leverage: $\operatorname{corr}(r_t, |r_{t+1..5}|)$", "rel"),
    ("kurt_month", r"monthly returns closer to Gaussian", "rel"),
]
MODELS = [("iid normal", r"independent\\Gaussian days", GAUSS), ("iid t", r"independent\\Student-$t$ days", VOL),
          ("GARCH", r"GARCH,\\Gaussian shocks", QC.IDEA), ("GJR-t", r"GJR-GARCH,\\$t$ shocks", LOSS)]


def passes(kind: str, real: float, sim: float) -> bool:
    """A model passes a row when it lands within half of the real number either way (or, for the absence of linear
    memory, when its lag-1 autocorrelation is small, as the market's is)."""
    if kind == "small":
        return abs(sim) < 0.1
    return np.sign(sim) == np.sign(real) and 0.5 * abs(real) <= abs(sim) <= 1.5 * abs(real)


def fmt(key: str, v: float) -> str:
    if key == "kurt" and v > 100:
        return r">100"
    if key in ("kurt", "kurt_month"):
        return f"{v:.1f}"
    if key == "alpha":
        return f"{v:.1f}"
    return f"{v:+.3f}".replace("+0.000", "0.000").replace("-0.000", "0.000")


PAPERS = [
    (r"Cont (2001), \textit{Quantitative Finance}", r"``Empirical properties of asset returns: stylized facts and "
     r"statistical issues'': the list, measured across markets; the yardstick ever since", REAL),
    (r"Takahashi and Mizuno (2024), arXiv", r"diffusion models generate return series through wavelet images, and are "
     r"checked against the stylized facts", VOL),
    (r"Kim, Choi and Kim (2025), arXiv", r"a diffusion model whose noise follows geometric Brownian motion reproduces "
     r"heavy tails, volatility clustering and the leverage effect more realistically than conventional diffusion models",
     LOSS),
    (r"Yang et al.\ (2025), \textit{TwinMarket}, arXiv", r"a market of language-model agents: individual actions add up "
     r"to group behaviour, with emergent bubbles and recessions", QC.IDEA),
]


class Frontier(VoiceoverScene):
    def construct(self):
        s = load("scorecard")
        self.card()
        self.scorecard(s)
        self.papers(s)

    def card(self):
        c = chapter_card(15, r"Frontier: the facts as a test", r"Can a machine invent a market that passes them?",
                         lit=(2001, 2024, 2025), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: the stylized facts as a test."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def scorecard(self, s):
        real = s["real"]
        med = {m: {k: float(np.median(v)) for k, v in s["sims"][m].items()} for m, _, _ in MODELS}
        xs = [-1.7, 0.35, 2.15, 3.95, 5.75]
        y0, dy = 2.45, 0.66
        head = VGroup(label(r"US market\\1926--2020", font_size=18, color=REAL).move_to([xs[0], y0 + 0.62, 0]))
        for (m, txt, col), x in zip(MODELS, xs[1:]):
            head.add(label(txt, font_size=17, color=col).move_to([x, y0 + 0.62, 0]))
        rows, cells = VGroup(), []
        for i, (k, txt, kind) in enumerate(FACTS):
            y = y0 - i * dy
            name = label(txt, font_size=21, color=GREY_A)
            name.move_to([-6.9 + name.width / 2, y, 0])
            rv = MathTex(fmt(k, real[k]), font_size=26, color=REAL).move_to([xs[0], y, 0])
            rows.add(VGroup(name, rv))
            rc = VGroup()
            for (m, _, col), x in zip(MODELS, xs[1:]):
                ok = passes(kind, real[k], med[m][k])
                box = RoundedRectangle(width=1.6, height=0.5, corner_radius=0.08, stroke_width=0,
                                       fill_color=QC.GAIN if ok else LOSS, fill_opacity=0.28).move_to([x, y, 0])
                rc.add(VGroup(box, MathTex(fmt(k, med[m][k]), font_size=24).move_to([x, y, 0])))
            cells.append(rc)
        names = VGroup(*[r_[0] for r_ in rows])
        if names.get_right()[0] > xs[0] - 0.8:
            for nm in names:
                if nm.get_right()[0] > xs[0] - 0.8:
                    nm.scale_to_fit_width(xs[0] - 0.8 + 6.9).align_to([-6.9, 0, 0], LEFT)
        score = {m: sum(passes(kind, real[k], med[m][k]) for k, _, kind in FACTS) for m, _, _ in MODELS}
        best = max(score, key=score.get)
        tot = VGroup(label(r"rows passed", font_size=19, color=GREY_A).move_to([-6.9 + 0.9, y0 - len(FACTS) * dy, 0]))
        for (m, _, col), x in zip(MODELS, xs[1:]):
            tot.add(MathTex(rf"{score[m]}/{len(FACTS)}", font_size=28, color=col).move_to([x, y0 - len(FACTS) * dy, 0]))
        src = note(rf"each model fitted to the US market and simulated for {s['n']:,} days, 8 seeds, medians shown; "
                   r"green: within half of the real number either way".replace(",", "{,}"),
                   font_size=15).to_edge(DOWN, buff=0.12)
        closest = max(med, key=lambda m: med[m]["acf100_abs"])
        lm = med[closest]["acf100_abs"]
        best_name = {"iid normal": "independent Gaussian days", "iid t": "independent Student t days",
                     "GARCH": "GARCH with Gaussian shocks", "GJR-t": "the asymmetric GARCH with fat-tailed shocks"}[closest]
        with self.voiceover(
            "Cont's list of stylized facts did not stay a description. It became a test: anyone who claims to "
            "simulate a market is asked whether the fake passes it. Run the test. Each row is one fact, the first "
            "column its value in ninety-four years of the American market. <bookmark mark='a'/> Against it, four "
            "simulated markets, each fitted to the same data. Independent Gaussian days fail almost everything, as "
            "they must. <bookmark mark='b'/> Independent Student t days get fat tails, too fat in fact, and nothing "
            "else: no clustering, no leverage. <bookmark mark='c'/> GARCH, Part seven's model, adds clustering, but "
            "with Gaussian shocks its tails are thin and it is blind to direction. <bookmark mark='d'/> The "
            f"asymmetric GARCH with fat-tailed shocks does best of the four, {score['GJR-t']} rows of {len(FACTS)}. "
            f"<bookmark mark='e'/> And the row every model fails is long memory: a hundred days on, the real "
            f"market's size of move still correlates at {real['acf100_abs']:.2f}; the closest of these, "
            f"{best_name}, manages {lm:.3f}. Long memory is why Part seven builds HAR and Part fourteen asks whether "
            "volatility is rough."
        ) as vo:
            self.play(FadeIn(head[0]), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.15, run_time=2.5),
                      FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), LaggedStart(*[FadeIn(c[0]) for c in cells], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(head[2]), LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(head[3]), LaggedStart(*[FadeIn(c[2]) for c in cells], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(head[4]), LaggedStart(*[FadeIn(c[3]) for c in cells], lag_ratio=0.1), FadeIn(tot))
            vo.wait_until("e")
            self.play(Indicate(VGroup(*[c[j] for c in cells[4:5] for j in range(4)]), color=YELLOW, scale_factor=1.1))
        self.wait(0.5)
        self.clear_scene()

    def papers(self, s):
        cards = VGroup()
        for who, what, col in PAPERS:
            body = VGroup(label(who, font_size=25, color=col), wrapped_label(what, 5.8, 22, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12)
            frame = RoundedRectangle(width=6.3, height=body.height + 0.4, corner_radius=0.1, stroke_color=col,
                                     stroke_width=1.5, fill_color="#0E141C", fill_opacity=1).move_to(body)
            cards.add(VGroup(frame, body))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.4)).to_edge(UP, buff=0.6)
        if cards.width > 13.0:
            cards.scale_to_fit_width(13.0)
        btc = s["btc"]
        tail = wrapped_label(rf"Bitcoin, 2017--2020, on the same card: excess kurtosis {btc['kurt']:.0f}, clustering "
                             rf"{btc['acf1_abs']:.2f} at one day but {btc['acf100_abs']:.2f} at a hundred, leverage "
                             rf"{btc['lev']:+.3f}: the same facts, a shorter memory", 12.0, 24, BTC)
        tail.next_to(cards, DOWN, buff=0.45)
        with self.voiceover(
            "The frontier runs exactly this test with far larger machines. Rama Cont's 2001 survey wrote down the list, "
            "measured across markets, and it has been the yardstick since. <bookmark mark='a'/> In 2024 Tomonori "
            "Takahashi and Takayuki Mizuno generated return series with diffusion models, the method behind image "
            "generators, by turning the series into wavelet images, and checked them against the facts. In 2025 Gihun "
            "Kim, Sun-Yong Choi and Yeoneung Kim made the model's noise follow geometric Brownian motion, and report "
            "heavy tails, clustering and the leverage effect closer to the real thing than standard diffusion models "
            "give. <bookmark mark='b'/> Others build markets out of language-model agents; the TwinMarket project "
            "reports bubbles and recessions emerging from individual decisions. Whether such markets pass every row "
            "is exactly what this card checks. <bookmark mark='c'/> And Bitcoin, our second market, passes the same "
            f"card its own way: excess kurtosis {btc['kurt']:.0f}, clustering, a leverage effect, and a memory that "
            "fades much sooner. Part seventeen trains generators of its own, and scores them on this card. Next, the "
            "House opens its doors."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.wait(0.5)
        self.clear_scene()
