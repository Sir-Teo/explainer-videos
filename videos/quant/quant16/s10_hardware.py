from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load, predict, axes, data_range, pause_card, flat_camera

VALIDATION = [
    (r"Monte Carlo and variance reduction", r"selected Black--Scholes checks: $4$ s.e.; geometric Asian: $3$ s.e.; finite-seed dispersion tests"),
    (r"Path factors and discrepancy", r"$\max|LL^\top-C|<10^{-12}$ on the test grid; one-dimensional discrepancy reference"),
    (r"Multilevel estimator", r"fixed-run price check: $3$ s.e. plus $0.01$; fitted Milstein variance exponent $\ge1.7$"),
    (r"Stopping policies and bounds", r"selected tree/order comparisons with explicit Monte Carlo and finite-grid allowances"),
    (r"Greeks and adjoints", r"selected delta disagreement $<0.02$; AAD/bump relative allowance $1\%$; basket delta $<10^{-3}$"),
    (r"ADI, FFT and Lewis/COS", r"selected ADI difference $<0.03$, FFT $<0.01$, Lewis/COS agreement $<10^{-8}$"),
    (r"American penalty solver", r"selected grid differs from the 2,000-step tree by less than $0.02$; finite boundary check"),
    (r"Toy amplitude and interpolation", r"20-run toy amplitude RMSE comparison; polynomial interpolation tolerance $10^{-10}$"),
]


class Hardware(VoiceoverScene):
    def construct(self):
        race = load("race")
        par = load("parallel")
        self.card()
        self.overnight()
        self.firms()
        self.machine(par, race)
        self.validation(load("envelope"))

    def card(self):
        c = chapter_card(17, r"Industry: the overnight run, GPUs and adjoints", r"How do banks actually compute all this?",
                         lit=(2011,), part=PART)
        with self.voiceover("Chapter seventeen. Industry: the overnight run, graphics chips, and adjoints at banks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def overnight(self):
        nT, nS = 10, 28
        cells = VGroup(*[Square(side_length=0.36, stroke_color=GREY_D, stroke_width=1, fill_color=QC.SPOT, fill_opacity=0.0)
                         for _ in range(nT * nS)]).arrange_in_grid(rows=nT, cols=nS, buff=0.04)
        cells.to_edge(UP, buff=0.9)
        rl = label(r"trades (a book has hundreds of thousands)", font_size=18, color=GREY_A).rotate(PI / 2)
        rl.next_to(cells, LEFT, buff=0.15)
        cl = label(r"scenarios: market paths for XVA (Part 21), stresses, VaR (Part 40)", font_size=18,
                   color=GREY_A).next_to(cells, UP, buff=0.12)
        order = np.random.default_rng(1).permutation(len(cells))
        reg = VGroup(
            history_card(r"margin", r"ISDA SIMM", r"A sensitivity-based model for initial margin on covered non-cleared derivatives. Version 2.9+2606 "
                         r"was published in 2026; publication does not establish every firm's implementation date.", color=QC.FIRM, width=6.2, font_size=18),
            history_card(r"capital", r"Basel's FRTB (2019)", r"The market-risk standardised approach includes a sensitivities-based method, plus default-risk "
                         r"and residual-risk components. Applicability and implementation dates depend on jurisdiction.", color=QC.FIRM, width=6.2,
                         font_size=18),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Banks use large pricing workloads for exposure, limits, margin and capital, with schedules and approximations varying by firm and purpose. The grid is an illustration of trades crossed with scenarios, not a measured bank production run. <bookmark mark='a'/> ISDA SIMM uses sensitivities for covered non-cleared initial margin. Its published methodology version does not imply every firm's current implementation. Basel's market-risk standardized approach includes a sensitivities-based component as well as default and residual-risk charges. These workloads help explain demand for efficient gradients, while operational and regulatory scope must be checked for the actual institution."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(rl), FadeIn(cl))
            self.play(LaggedStart(*[cells[i].animate.set_fill(opacity=0.85) for i in order], lag_ratio=0.004, run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(reg[0], shift=UP * 0.2))
            self.play(FadeIn(reg[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        a = firm_card(r"Danske Bank", r"Risk.net's In-House System of the Year for 2015, for adjoint differentiation "
                      r"across its pricing and risk: counterparty valuation adjustments with their sensitivities in "
                      r"seconds on ordinary hardware (as reported by Risk.net). Antoine Savine, then at Danske, wrote the "
                      r"2018 textbook on the method.", width=6.3, font_size=18)
        b = firm_card(r"JPMorgan and Maxeler", r"The bank and the vendor reported moving its credit-derivatives risk "
                      r"computation onto FPGA chips: a run of about eight hours fell to under four minutes (Weston, "
                      r"Spooner, Racani\`ere and Mencer 2012; as reported, 2011). JPMorgan took a stake in Maxeler.",
                      width=6.3, font_size=18)
        c = history_card(r"benchmark", r"STAC-A2", r"Designed by bank quants with STAC: Monte Carlo Greeks of a multi-asset, "
                         r"path-dependent Heston option with early exercise. Chapters 2--11 in one test; results are "
                         r"reported for specific implementations, including STAC-audited results.", color=QC.IDEA, width=6.3, font_size=18)
        d = history_card(r"open and cleared", r"QuantLib, ORE, the OCC", r"QuantLib (open source since 2000) ships Sobol "
                         r"paths with a Brownian bridge; ORE builds valuation and risk analytics on QuantLib. The OCC's official "
                         r"methodology describes STANS as a full-portfolio Monte Carlo margin system, introduced in 2006.", color=QC.IDEA, width=6.3, font_size=18)
        grid = VGroup(VGroup(a, b).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(c, d).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.3:
            grid.scale_to_fit_height(7.3)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "Two firm files, from the public record. Danske Bank won Risk.net's in-house system award for 2015 for "
            "building adjoint differentiation through its pricing and risk systems: as reported, counterparty "
            "adjustments and their sensitivities in seconds on ordinary hardware. Antoine Savine, who worked there, "
            "wrote the textbook on it. <bookmark mark='a'/> JPMorgan went the hardware way. With the firm Maxeler it "
            "moved the core of its credit-derivatives risk run onto programmable chips; the bank's and vendor's own "
            "account says a run of about eight hours fell to under four minutes, and the bank took a stake in the "
            "company. <bookmark mark='b'/> Graphics chips are measured by STAC-A2, a benchmark designed by bank "
            "quants: Monte Carlo Greeks of a multi-asset Heston option with early exercise, which is chapters two to "
            "eleven in a single test. <bookmark mark='c'/> In the open, QuantLib ships Sobol paths with a Brownian "
            "bridge and ORE builds valuation adjustments on it; the Options Clearing Corporation sets margins by "
            "Monte Carlo."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(d, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def machine(self, par, race):
        n = par["n"]
        items = [(r"loop ($10^5\times10$)", par["t_loop"], BAD), (r"numpy, float64", par["t_numpy"], OPT),
                 (r"numpy, float32", par["t_float32"], QC.THETA)] + \
                [(rf"{w} process{'es' if w != '1' else ''} (draw + price)", t, GOOD) for w, t in par["procs"].items()]
        base = par["procs"]["1"]
        xr = data_range([np.log10(t) for _, t, _ in items])
        baseline = xr[0]
        g = axes(xr, [0, len(items) + 1], x_length=5.2, y_length=4.4, xlabel=r"recorded seconds (log); row workloads differ",
                 xticks=[-3, -2, -1, 0, 1, 2], xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=2.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (nm, t, col) in enumerate(items):
            y = len(items) - i
            x1 = np.log10(t)
            bars.add(VGroup(Rectangle(width=max(ax.c2p(x1, 0)[0] - ax.c2p(baseline, 0)[0], 0.02), height=0.42, stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(baseline, y), aligned_edge=LEFT),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(baseline, y), LEFT, buff=0.15),
                            MathTex(rf"{t:.3g}\,\text{{s}}", font_size=20, color=GREY_A).next_to(ax.c2p(x1, y), RIGHT, buff=0.1)))
        p = par["procs"]
        sp4 = base / p["4"] if "4" in p else float("nan")
        pts = race["points"]
        mc = min((q for q in pts if q["method"].startswith("Monte Carlo")), key=lambda q: q["err"])
        cos = min((q for q in pts if q["method"] == "COS" and q["err"] < mc["err"]), key=lambda q: q["time"])
        speed = mc["time"] / cos["time"]
        side = VGroup(
            MathTex(rf"\text{{loop}} \div \text{{numpy}}:\ {par['t_loop'] / par['t_numpy']:,.0f}\times".replace(",", "{,}"),
                    font_size=26, color=OPT),
            MathTex(rf"4\ \text{{processes}}:\ {sp4:.1f}\times\ \text{{one}}", font_size=26, color=GOOD),
            wrapped_label(rf"COS example: {cos['time'] * 1000:.3g} ms; absolute numerical-reference difference {cos['err']:.2g}; "
                          r"not matched to MC total error", 4.0, 21, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(UP * 1.4)
        loadtxt = wrapped_label(rf"recorded {par['date']}: host reports {par['cores']} logical CPUs; container quota is 4 CPU equivalents. "
                                r"Best of 2 loop runs, 5 NumPy runs, 3 draw/process runs. Vector rows reuse normals; pool rows draw and price.", 4.0, 19, GREY_B)
        loadtxt.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        q = predict(r"Monte Carlo is embarrassingly parallel. Is a Longstaff--Schwartz pricing?", width=4.0,
                    font_size=18).to_corner(DR, buff=0.25)
        r32 = par["t_numpy"] / par["t_float32"]
        f32 = (f"Single precision, half the bytes to move, is another {r32:.0f} times faster here." if r32 >= 1.5 else
               "Single precision changes little here.")
        verdict = ("barely helps here, because the machine is shared and already busy" if sp4 < 1.5 else
                   "helps, though less than the four cores promise")
        with self.voiceover(
            f"These timings use distinct workloads and repetition counts. The Python loop times one hundred thousand pre-generated payoffs, then extrapolates tenfold to {par['t_loop']:.3f} seconds. <bookmark mark='a'/> NumPy directly prices one million pre-generated values in {par['t_numpy'] * 1000:.2f} milliseconds. The ratio {par['t_loop'] / par['t_numpy']:.0f} illustrates these implementations, with extrapolation and shared-machine effects. Float32 throughput does not certify price or Greek accuracy. <bookmark mark='b'/> Pool workers both draw normals and price them, so compare four workers with the one-worker pool: ratio {sp4:.2f}. Startup, communication, workload and CPU quota all matter; host load alone cannot explain the result. The recorded host reports {par['cores']} logical CPUs, while the container quota is four CPU equivalents. <bookmark mark='c'/> The separate COS timing and numerical-reference difference are shown without claiming matched total accuracy to Monte Carlo. LSM path simulation can be parallelized, but each exercise date requires regression reductions and synchronization."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[3:]], lag_ratio=0.3), FadeIn(side[1]), FadeIn(loadtxt))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def validation(self, env):
        head = wrapped_label(r"Selected repository numerical tests: ten tests passed in this review", 12.0, 28, QC.HOUSE).to_edge(UP, buff=0.3)
        rows = VGroup(*[VGroup(wrapped_label(title, 6.0, 23, QC.HOUSE),
                              wrapped_label(detail, 6.0, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
                       for title, detail in VALIDATION])
        rows.arrange_in_grid(rows=4, cols=2, cell_alignment=UL, buff=(0.45, 0.28)).next_to(head, DOWN, buff=0.35)
        if rows.height > 5.8:
            rows.scale_to_fit_height(5.8)
        foot = wrapped_label(r"Source: tests/test\_quant\_house.py; fixed examples and tolerances. Numerical verification does not certify model adequacy or every production price.", 12.4, 20, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Ten selected engine tests passed in this review. They check fixed examples at their actual tolerances: stochastic comparisons with sampling allowances, covariance identities, multilevel diagnostics, stopping examples, adjoint-bump agreement, grid and transform comparisons, and toy interpolation and amplitude cases. These are the repository's tests, not evidence of an automated nightly bank process or independent validation of every engine function. <bookmark mark='a'/> A passing suite supports these numerical cases. It does not certify every price, all discretization biases, out-of-sample calibration behaviour or the financial model itself. Model misspecification and computational error are distinct concerns. Next, quantum resource estimates."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3, run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
