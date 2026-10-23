from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (DDIM_C, DPMPP_C, HEUN_C, PART, SCHED, bars_chart, legend, load, log_axes, logcurve,
                                   take_away)

NAMES = {"cos": r"ours: \ cosine", "linb": r"linear $\beta$ \ (VP SDE)", "fm": r"straight line", "logn": r"EDM: \ log-normal"}
SHORT = {"cos": r"cosine", "linb": r"linear $\beta$", "fm": r"straight line", "logn": r"log-normal"}
SPOKEN = {"cos": "our cosine schedule", "linb": "the linear-beta schedule", "fm": "the straight-line schedule",
          "logn": "EDM's log-normal"}
SP_NAME = {"time": r"uniform in $t$", "ddpm": r"DDPM's steps", "logsnr": r"uniform in log-SNR", "edm": r"EDM, $\rho = 7$"}
SP_SPOKEN = {"time": "uniform in time", "ddpm": "DDPM's own steps", "logsnr": "uniform in log signal-to-noise",
             "edm": "EDM's spacing"}


class Schedules(VoiceoverScene):
    def construct(self):
        self.card()
        self.snr()
        self.invariance()
        self.trained()
        self.spacing()

    def card(self):
        card = chapter_card(7, r"Noise schedules", r"Which noise levels, how often, and in what order?", part=PART)
        with self.voiceover("Chapter seven. Noise schedules."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def snr(self):
        s = load("schedules")
        t = np.asarray(s["t"])
        g = axes([0, 1], [-14, 14], x_length=6.4, y_length=4.2, xlabel=r"time $t$ \ ($0$: data, \ $1$: noise)",
                 ylabel=r"log-SNR \ $\lambda = \log(\alpha^2 / \sigma^2)$", xticks=[0, 0.5, 1], yticks=[-10, 0, 10],
                 center=[-2.8, -0.3, 0])
        items = [("ddpm", r"DDPM: \ linear $\beta$, \ $1{,}000$ steps"), ("cosine", r"Nichol \& Dhariwal: \ cosine"),
                 ("trig", r"ours: \ $\alpha = \cos(\pi t/2)$"), ("fm", r"flow matching's straight line")]
        cols = {"ddpm": SCHED["ddpm"], "cosine": SCHED["cosine"], "trig": SCHED["trig"], "fm": SCHED["fm"]}
        curves = VGroup(*[curve(g.ax, t, np.clip(np.asarray(s[f"logsnr_{k}"]), -14, 14), cols[k], 3) for k, _ in items])
        lg = legend([(cols[k], n) for k, n in items], font_size=20).move_to([3.6, 1.6, 0])
        d = definition_card(r"signal-to-noise ratio", MathTex(r"\mathrm{SNR}(t) = \alpha_t^2 / \sigma_t^2", font_size=30),
                            width=4.2).move_to([3.6, -0.3, 0])
        lt = float(s["logsnr_T"])
        tdot = Dot(g.ax.c2p(1, lt), radius=0.08, color=SCHED["ddpm"])
        tl = label(rf"DDPM's last step: \ $\lambda = {lt:.1f}$, \ not $-\infty$", font_size=20, color=SCHED["ddpm"]).next_to(tdot, LEFT, buff=0.15)
        lin = VGroup(label(r"Lin et al.\ (2024): \ never trained at pure noise,", font_size=20, color=GREY_A),
                     label(r"so the model can't make a very dark or very bright picture;", font_size=20, color=GREY_A),
                     label(r"the fix: \ rescale to zero SNR at the end", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, -2.3, 0])
        with self.voiceover(
            "A noise schedule says how much signal survives at each time. Its one number is the signal-to-noise "
            "ratio, alpha squared over sigma squared, best seen on a log scale. <bookmark mark='a'/> DDPM's linear "
            "betas, the cosine schedule of Alex Nichol and Prafulla Dhariwal, ours, and flow matching's straight "
            "line all run from plenty of signal to almost none, at different speeds. <bookmark mark='b'/> One "
            f"detail matters: DDPM's last step still has a log signal-to-noise ratio of {lt:.1f}, not minus infinity. "
            "<bookmark mark='c'/> In 2024 Shanchuan Lin and colleagues showed that a model never trained at pure "
            "noise can't make a very dark or very bright image, and rescaled the schedule to end at zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(d))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.3), FadeIn(lg), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tdot, scale=1.5), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeIn(lin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def invariance(self):
        s = load("schedules")
        rows = [
            cmath(r"\mathcal L_\infty", r"=", r"\tfrac12\, \mathbb E \int_0^1 \big(-\tfrac{d}{dt}\mathrm{SNR}(t)\big)\, "
                  r"\big\| x_0 - \hat x_0(x_t, t) \big\|^2\, dt", font_size=32),
            cmath(r"\mathcal L_\infty", r"=", r"\tfrac12\, \mathbb E \int_{\mathrm{SNR}_{\min}}^{\mathrm{SNR}_{\max}} "
                  r"\big\| x_0 - \hat x_0(x_v, v) \big\|^2\, dv", font_size=32),
        ]
        whys = [why(r"the bound, \ steps to zero \ (Kingma et al., 2021)"), why(r"change variable to $v = \mathrm{SNR}$")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-2.6, buff=0.5, edge=6.85)
        bins = np.asarray(s["bins"])
        mid = (bins[:-1] + bins[1:]) / 2
        keys = [("ddpm", SCHED["ddpm"], r"DDPM"), ("trig", SCHED["trig"], r"ours"), ("fm", SCHED["fm"], r"straight line"),
                ("edm", SCHED["edm"], r"EDM's log-normal")]
        top = max(float(np.asarray(s[f"dens_{k}"]).max()) for k, _, _ in keys) * 1.1
        g = axes([-14, 14], [0, top], x_length=7.0, y_length=2.6, xlabel=r"log-SNR $\lambda$",
                 ylabel=r"how often training visits each noise level", xticks=[-10, 0, 10], center=[-2.0, -1.75, 0])
        cs = VGroup(*[curve(g.ax, mid, np.asarray(s[f"dens_{k}"]), c, 3) for k, c, _ in keys])
        lg = legend([(c, n) for _, c, n in keys], font_size=20).move_to([4.6, -1.5, 0])
        with self.voiceover(
            "Does the schedule change what is being learned? In 2021 Diederik Kingma, Tim Salimans, Ben Poole and "
            "Jonathan Ho took the bound to continuous time: an integral over time of the clean-point error, weighted "
            "by how fast the signal-to-noise ratio falls. <bookmark mark='a'/> Change the variable to the ratio "
            "itself, and the schedule disappears: only its two ends remain. Every schedule with the same ends has the "
            "same bound. <bookmark mark='b'/> What the schedule does change is practice: with time drawn uniformly, "
            "each schedule visits the noise levels with a different frequency, and the network learns best where it "
            "practises most. <bookmark mark='c'/> EDM, in the next chapter, skips the schedule and draws noise levels "
            "from a log-normal directly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(g), LaggedStart(*[Create(c_) for c_ in cs[:3]], lag_ratio=0.3), FadeIn(lg[:3]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cs[3]), FadeIn(lg[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trained(self):
        a = load("ablate")
        sig = [float(v) for v in a["sig"]]
        kinds = ["cos", "linb", "fm", "logn"]
        D = {k: np.asarray(a[f"{k}_eps_derr"]) for k in kinds}  # seed, noise level
        vals = np.concatenate([np.maximum(D[k], 1e-6).ravel() for k in kinds])
        lo, hi = math.floor(math.log10(vals.min())), math.ceil(math.log10(vals.max()))
        g = log_axes([math.log10(sig[0]) - 0.1, math.log10(sig[-1]) + 0.1], [lo, hi], x_length=6.0, y_length=3.8,
                     xlabel=r"noise level $\sigma$ \ (in $x = x_0 + \sigma n$)",
                     ylabel=r"error against the exact denoiser", xticks=sig, yticks=[10.0 ** e for e in range(lo, hi + 1)],
                     yfmt=lambda v: f"10^{{{int(round(math.log10(v)))}}}", center=[-3.0, -0.2, 0])
        lines = VGroup()
        for k in kinds:
            m = D[k].mean(0)
            band_ = band(g.ax, np.log10(sig), np.log10(np.maximum(D[k].min(0), 1e-6)), np.log10(np.maximum(D[k].max(0), 1e-6)),
                         SCHED[k], 0.18)
            lines.add(VGroup(band_, logcurve(g.ax, sig, np.maximum(m, 1e-6), SCHED[k])))
        heun = {k: np.asarray(a[f"{k}_eps_heun"]) for k in kinds}
        ch = bars_chart([heun[k].mean() for k in kinds], [SCHED[k] for k in kinds], [SHORT[k] for k in kinds],
                        height=2.2, bar_w=0.7, gap=0.45, spread=[(heun[k].min(), heun[k].max()) for k in kinds], digits=3,
                        font_size=18).move_to([4.2, -1.3, 0])
        fl = float(a["floor"])
        chl = label(rf"distance from the data, \ Heun, $35$ evaluations \\ (floor ${fl:.3f}$; \ bars: mean, \ whiskers: "
                    rf"${len(heun['cos'])}$ seeds)", font_size=18, color=GREY_A).next_to(ch, UP, buff=0.3)
        lg = legend([(SCHED[k], NAMES[k]) for k in kinds], font_size=18).move_to([4.2, 2.3, 0])
        best = min(kinds, key=lambda k: heun[k].mean())
        worst = max(kinds, key=lambda k: heun[k].mean())
        hi_err = max(kinds, key=lambda k: D[k][:, -1].mean())
        lo_hi = min(kinds, key=lambda k: D[k][:, -1].mean())
        spread_overlap = heun[best].max() > heun[worst].min()
        verdict = (f"After sampling, the spreads overlap: {SPOKEN[best]} is best on average, {SPOKEN[worst]} worst, but "
                   "seeds differ as much as schedules do." if spread_overlap else
                   f"After sampling, {SPOKEN[best]} is best and {SPOKEN[worst]} worst, every seed of one beating every "
                   "seed of the other.")
        with self.voiceover(
            f"We trained the same noise-guessing network four ways, changing only which noise levels it practises: "
            f"the same budget, {len(heun['cos'])} seeds each. <bookmark mark='a'/> Because our letters' exact denoiser is "
            "known, we can see where each one is wrong. At low noise they all agree. <bookmark mark='b'/> At the "
            f"highest noise, {SPOKEN[hi_err]} is the furthest off and {SPOKEN[lo_hi]} the closest: the one that "
            "practises there most. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(lines[kinds.index(k)][1], color=SCHED[k]) for k in (hi_err, lo_hi)])
            vo.wait_until("c")
            self.play(FadeIn(ch), FadeIn(chl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spacing(self):
        s = load("schedules")
        sps = list(s["spacings"])
        kinds = list(s["spacing_solvers"])
        budgets = [int(b) for b in s["budgets"]]
        j = budgets.index(16) if 16 in budgets else 1
        names = {"ddim": r"DDIM", "heun": r"Heun", "dpmpp2m": r"DPM-Solver++(2M)"}
        cols = {"ddim": DDIM_C, "heun": HEUN_C, "dpmpp2m": DPMPP_C}
        head = VGroup(label(r"at about $16$ evaluations:", font_size=22, color=GREY_A),
                      *[label(SP_NAME[sp], font_size=22, color=GREY_A) for sp in sps])
        xs = [-4.9, -1.9, 0.6, 3.1, 5.6]
        for i, h in enumerate(head):
            h.move_to([xs[i], 1.9, 0])
        rows = VGroup()
        best = {}
        for r, k in enumerate(kinds):
            errs = [float(s[f"err_{k}_{sp}"][j]) for sp in sps]
            best[k] = sps[int(np.argmin(errs))]
            row = VGroup(label(names[k], font_size=24, color=cols[k]).move_to([xs[0], 1.1 - 0.75 * r, 0]))
            for c, (sp, e) in enumerate(zip(sps, errs)):
                m = MathTex(f"{e:.3f}", font_size=30, color=WHITE if sp == best[k] else GREY_B).move_to([xs[c + 1], 1.1 - 0.75 * r, 0])
                row.add(m)
                if sp == best[k]:
                    row.add(SurroundingRectangle(m, color=cols[k], buff=0.1, corner_radius=0.06))
            rows.add(row)
        note_ = label(r"the error at the end, \ against the exact solution of the ODE, \ same starting noise", font_size=20,
                      color=GREY_A).next_to(rows, DOWN, buff=0.4)
        same = len(set(best.values())) == 1
        verdict = (f"One spacing wins for all three: {SP_SPOKEN[best[kinds[0]]]}." if same else
                   "No spacing wins for every solver: for DDIM the best is " + SP_SPOKEN[best["ddim"]] + ", for Heun "
                   + SP_SPOKEN[best["heun"]] + ", for DPM-Solver plus plus " + SP_SPOKEN[best["dpmpp2m"]] + ".")
        edm_note = ("On image models EDM's spacing has become a standard; on our letters it is not always the best. "
                    "The spacing is a setting of the sampler, tuned like any other." if any(b != "edm" for b in best.values())
                    else "On image models EDM's spacing has become a standard, and on our letters it is the best too.")
        ta = take_away(r"A schedule chooses which noise levels the network practises, \ and where the sampler steps; \ "
                       r"the bound itself doesn't care.")
        with self.voiceover(
            "The schedule also decides where a sampler puts its steps. Here are three samplers, with the exact "
            "denoiser, at the same budget of about sixteen network evaluations, on four spacings of the noise "
            "levels. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + edm_note
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[r_[0] for r_ in rows])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[1:])) for r_ in rows], lag_ratio=0.3), FadeIn(note_))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
