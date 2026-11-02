from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data

MODELS = ["LV", "Heston", "Bates", "VG"]
COLS = {"LV": QC.SPOT, "Heston": QC.OPTION, "Bates": QC.GAIN, "VG": QC.IMPLIED}
NAMES = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma"}


class ModelRisk(VoiceoverScene):
    def construct(self):
        m = load("modelrisk")
        self.card()
        self.fans(m)
        self.table(m)
        self.derive()
        self.tilt(load("robust"), load("outcomes"))

    def card(self):
        c = chapter_card(14, r"Same vanillas, different exotics", r"How much does the choice of model move an exotic's "
                         r"price?", lit=(2006,), part=PART)
        with self.voiceover("Chapter fourteen. Same vanillas, different exotics: measuring model risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fans(self, m):
        M = m["models"]
        g = axes([0, 120], [0.55, 1.6], x_length=6.4, y_length=4.4, xlabel=r"days", ylabel=r"bitcoin / today",
                 xticks=[0, 30, 60, 90, 120], yticks=[0.6, 0.8, 1.0, 1.25, 1.5], font_size=15).to_edge(LEFT, buff=0.5)
        ax = g.ax
        t = np.arange(121)
        fans = VGroup()
        for k in MODELS:
            P = np.clip(np.asarray(M[k]["paths"])[:25], 0.55, 1.6)
            fans.add(path_fan(ax, t, P, color=COLS[k], stroke_width=1.2, opacity=0.35))
        bars = [DashedLine(ax.c2p(0, y), ax.c2p(120, y), stroke_color=GREY_C, stroke_width=1.5) for y in (0.8, 1.25)]
        h = axes([-0.25, 0.25], [0.3, 0.8], x_length=5.0, y_length=3.6, xlabel=r"log strike, 79 days",
                 ylabel=r"implied vol", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.6, 0.8], font_size=14).to_edge(RIGHT, buff=0.5)
        mk = m["market"]
        mdots = VGroup(*[Dot(h.ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(mk["k"], mk["iv"])
                         if -0.25 <= a <= 0.25])
        sm = VGroup()
        for k in MODELS:
            kk, iv = np.asarray(M[k]["smile_k"]), np.asarray(M[k]["smile"], float)
            ok = np.isfinite(iv)
            sm.add(curve(h.ax, kk[ok], np.clip(iv[ok], 0.3, 0.8), COLS[k], stroke_width=2.5))
        leg = legend([(COLS[k], NAMES[k]) for k in MODELS] + [(WHITE, r"market quotes")], font_size=16)
        leg.arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        src = real_data(r"Deribit bitcoin options, 10 December 2025; models calibrated in Part 13", corner=UR)
        with self.voiceover(
            "Here is model risk made visible. Four models, local volatility, Heston, Bates with jumps, and variance "
            "gamma, each calibrated in Part thirteen to the same bitcoin Surface of the tenth of December 2025. "
            "<bookmark mark='a'/> Simulate each one, twenty thousand daily paths for a hundred and twenty days. The "
            "fans look alike. <bookmark mark='b'/> And on the right, their smiles at seventy-nine days, read off "
            "their own simulated call prices, sit on the same market quotes. By the standard of the vanillas they "
            "were fitted to, these are the same model. Now ask them about paths."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[LaggedStart(*[Create(p) for p in f], lag_ratio=0.05) for f in fans], lag_ratio=0.3,
                                  run_time=5), *[Create(b) for b in bars])
            vo.wait_until("b")
            self.play(FadeIn(h), FadeIn(mdots), LaggedStart(*[Create(s) for s in sm], lag_ratio=0.3), FadeIn(leg))
        self.wait(0.4)
        self.clear_scene()

    def table(self, m):
        M = m["models"]
        items = [("vanilla90", r"90-day at-the-money call", 4), ("doc", r"down-and-out call, barrier 0.8", 4),
                 ("onetouch", r"one-touch at 0.8", 3), ("dnt", r"double-no-touch (0.8, 1.25)", 3),
                 ("coupon", r"4-month autocall: fair coupon", 3)]
        head = VGroup(label(r"per unit of spot", font_size=19, color=GREY_A),
                      *[label(NAMES[k], font_size=19, color=COLS[k]) for k in MODELS], label(r"spread", font_size=19,
                                                                                             color=BAD))
        tab = VGroup(head)
        spreads = {}
        for key, nm, dg in items:
            vals = np.array([M[k][key] for k in MODELS])
            spreads[key] = (vals.max() - vals.min()) / vals.mean()
            row = VGroup(label(nm, font_size=20))
            for k, v in zip(MODELS, vals):
                txt = f"{100 * v:.1f}\\%" if key == "coupon" else f"{v:.{dg}f}"
                row.add(MathTex(txt, font_size=26, color=COLS[k]))
            row.add(MathTex(f"{100 * spreads[key]:.0f}\\%", font_size=26, color=BAD))
            tab.add(row)
        xs = [-3.9, -0.9, 1.0, 2.8, 4.6, 6.2]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.5 - 0.62 * i, 0])
        tab.scale_to_fit_width(min(tab.width, 13.2)).move_to(UP * 0.8)
        cp = {k: M[k]["coupon"] for k in MODELS}
        hi_k, lo_k = max(cp, key=cp.get), min(cp, key=cp.get)
        dn = {k: M[k]["dnt"] for k in MODELS}
        dhi, dlo = max(dn, key=dn.get), min(dn, key=dn.get)
        van = [M[k]["vanilla90"] for k in MODELS]
        van3 = np.array([M[k]["vanilla90"] for k in ("LV", "Heston", "Bates")])
        v3 = (van3.max() - van3.min()) / van3.mean()
        foot = wrapped_label(rf"the vanillas: local vol, Heston and Bates agree to {100 * v3:.1f}\%; variance gamma, the "
                             rf"worst fit of the four, is {100 * (M['VG']['vanilla90'] / np.mean(van3) - 1):+.0f}\% off. "
                             r"The path-dependent products spread far more", 12.0, 20, GREY_A).to_edge(DOWN, buff=0.5)
        pp = pause_card(r"Which is most model-dependent: the one-touch, the double-no-touch or the autocall?", width=6.0)
        pp.to_corner(DR, buff=0.3)
        with self.voiceover(
            "Pause and predict: which of these depends most on the model, the one-touch, the double-no-touch, or "
            "the autocall? <bookmark mark='a'/> The table. The ninety-day at-the-money call: local volatility, "
            f"Heston and Bates agree to {100 * v3:.1f} percent, and variance gamma, the worst fit of the four, is "
            f"{100 * (M['VG']['vanilla90'] / np.mean(van3) - 1):.0f} percent off. <bookmark mark='b'/> The one-touch "
            f"spreads {100 * spreads['onetouch']:.0f} percent: it is pinned by the skew, which all of them fit. The "
            f"double-no-touch spreads {100 * spreads['dnt']:.0f} percent, from {dn[dlo]:.3f} under {NAMES[dlo]} to "
            f"{dn[dhi]:.3f} under {NAMES[dhi]}: it depends on how volatility moves along the path, which the "
            f"vanillas do not pin. And the autocall's fair coupon runs from {100 * cp[lo_k]:.1f} percent under "
            f"{NAMES[lo_k]} to {100 * cp[hi_k]:.1f} percent under {NAMES[hi_k]}. Same vanillas, different exotics."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\mu(X)", r"=", r"\sup_{Q \in \mathcal Q}\mathbb E^{Q}[X] - \inf_{Q \in \mathcal Q}\mathbb E^{Q}[X]",
                  font_size=36, colors={r"\mu(X)": BAD}),
            cmath(r"\sup_Q \big\{\mathbb E^{Q}[V] : D(Q\,\|\,P) \le \eta\big\}", r":", r"\frac{dQ_\theta}{dP} = "
                  r"\frac{e^{\theta V}}{\mathbb E\,e^{\theta V}}", font_size=32,
                  colors={r"\sup_Q \big\{\mathbb E^{Q}[V] : D(Q\,\|\,P) \le \eta\big\}": QC.Q}),
            cmath(r"\eta(\theta)", r"=", r"\theta\,\mathbb E_{Q_\theta}[V] - \log \mathbb E\,e^{\theta V}", font_size=34,
                  colors={r"\eta(\theta)": IV}),
            cmath(r"\text{reserve}", r"=", r"\text{model price} - \text{worst plausible price}", font_size=36,
                  colors={r"\text{reserve}": OPT}),
        ]
        whys = [why(r"Cont (2006): the range of prices over every model consistent with the calibration instruments; "
                    r"zero for the vanillas themselves, a coherent measure of model uncertainty"),
                why(r"Glasserman and Xu (2014): the worst case over all models within relative entropy $\eta$ of the "
                    r"model; by entropy duality (Donsker--Varadhan) the optimum is an exponential tilt"),
                why(r"plug the tilt into the relative entropy; solve for $\theta$, then the worst price is "
                    r"$\mathbb E_{Q_\theta}[V]$, all from the model's own paths"),
                why(r"what the desk holds back (chapter 17); both are computed, neither needs a new model")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Two ways to put a number on it. Rama Cont, in 2006: take every model consistent with the instruments "
            "you calibrate to, and measure the range of prices they give. It is zero for the vanillas themselves, "
            "and it behaves like a proper risk measure. Our four models give a crude lower bound on that range. "
            "<bookmark mark='a'/> Paul Glasserman and Xingbo Xu, in 2014, ask a different question: what is the "
            "worst price over every model within a given relative entropy of yours? The answer is beautiful: the "
            "worst model is an exponential tilt of your own, re-weighting each path by e to the theta times its "
            "payoff. <bookmark mark='b'/> Plug the tilt into the entropy and solve for theta, and the worst price "
            "comes from paths you already have. <bookmark mark='c'/> The gap between the model price and the worst "
            "plausible price is what a desk holds back as a reserve."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def tilt(self, r, o):
        rows = r["rows"]
        eta = np.array([x["eta"] for x in rows])
        val = np.array([x["value"] for x in rows])
        pl = np.array([x["p_lost"] for x in rows])
        sh = o["show"]
        P = np.asarray(sh["paths"])[:80]
        t = np.arange(P.shape[1]) * 3 / 21
        g = axes([0, 24], [0.45, 1.5], x_length=6.2, y_length=4.0, xlabel=r"months", ylabel=r"index / start",
                 xticks=[0, 6, 12, 18, 24], yticks=[0.5, 0.75, 1.0, 1.25], font_size=14).to_edge(LEFT, buff=0.4)
        ax = g.ax
        W = {k: np.asarray(v)[:80] for k, v in r["shown"].items()}
        e = ValueTracker(0.0)
        keys = sorted(W, key=float)

        def wts():
            x = e.get_value()
            if x <= 0:
                return np.ones(80)
            k = min(keys, key=lambda kk: abs(float(kk) - x))
            return W[k]

        def fan():
            w = wts()
            w = w / max(w.max(), 1e-9)
            return VGroup(*[curve(ax, t, np.clip(P[j], 0.45, 1.5), BAD if o["show"]["ki_day"][j] >= 0 else SPOT,
                                  stroke_width=1.3).set_stroke(opacity=float(0.08 + 0.8 * w[j])) for j in range(80)])
        lines = always_redraw(fan)
        h = axes([0, 0.5], [float(val.min()) - 0.02, 1.01], x_length=5.0, y_length=3.6,
                 xlabel=r"relative entropy budget $\eta$", ylabel=r"worst value of the note", xticks=[0, 0.25, 0.5],
                 yticks=[round(float(val.min()), 2), 1.0], font_size=14).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        tr = always_redraw(lambda: Dot(h.ax.c2p(e.get_value(), float(np.interp(e.get_value(), eta, val))), radius=0.08,
                                       color=BAD))
        cv = curve(h.ax, eta, val, BAD, stroke_width=3)
        i1 = int(np.argmin(np.abs(eta - 0.1)))
        foot = wrapped_label(rf"at $\eta = 0.1$ the worst model values the note at {val[i1]:.3f} instead of 1, and gives a "
                             rf"loss of more than 3\% a probability of {100 * pl[i1]:.0f}\% instead of {100 * pl[0]:.0f}\%", 5.4, 19,
                             GREY_A).next_to(h, DOWN, buff=0.3)
        src = illustration(r"the CSI 500 snowball at its fair coupon: 40{,}000 paths, 80 drawn; opacity = the tilt's weight",
                           corner=DL)
        with self.voiceover(
            "Watch the tilt on chapter seven's snowball. Eighty of its paths, in the model. As the entropy budget "
            "eta grows, the worst-case model re-weights them: paths that end in a loss grow brighter, paths that "
            "knock out early fade. <bookmark mark='a'/> On the right, the worst value of the note as the budget "
            f"grows. At eta of 0.1 it is {val[i1]:.3f} instead of one, and the worst model gives a loss of more than three percent "
            f"a probability of {100 * pl[i1]:.0f} percent instead of {100 * pl[0]:.0f}. A small, believable change "
            "of model costs the buyer several points. The curve is a menu for the desk: pick how much model doubt to "
            "price, and read off the reserve."
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), FadeIn(src))
            self.add(lines, tr)
            vo.wait_until("a")
            self.play(Create(cv), e.animate.set_value(0.5), run_time=max(vo.remaining(1.0) - 1.0, 3.0), rate_func=linear)
            self.play(FadeIn(foot))
        lines.clear_updaters()
        tr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
