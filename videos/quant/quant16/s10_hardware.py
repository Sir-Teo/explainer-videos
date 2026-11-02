from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load, predict

VALIDATION = [
    (r"\texttt{mc\_call}, \texttt{asian\_control}, \texttt{stratified\_call}", r"Black--Scholes; Kemna--Vorst", r"3 s.e."),
    (r"\texttt{normals}, \texttt{brownian\_bridge}, \texttt{path\_matrix}", r"$LL^\top = \min(t_i, t_j)$", r"$10^{-12}$"),
    (r"\texttt{mlmc}, \texttt{mlmc\_run}", r"Black--Scholes; Milstein's $\beta \ge 1.7$", r"3 s.e."),
    (r"\texttt{lsm\_put}, \texttt{andersen\_broadie\_put}, \texttt{bermudan\_tree}", r"European $<$ Bermudan $<$ American",
     r"bracket"),
    (r"\texttt{greeks\_three\_ways}, \texttt{aad\_greeks}, \texttt{aad\_basket}", r"closed-form Greeks; bumps", r"$10^{-3}$"),
    (r"\texttt{fd\_european}, \texttt{fd\_american\_put}, \texttt{fd\_american\_penalty}", r"Black--Scholes; the tree",
     r"0.02"),
    (r"\texttt{heston\_adi}, \texttt{carr\_madan}, \texttt{cos\_price}, \texttt{lewis\_call}", r"each other", r"$10^{-8}$"),
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
            history_card(r"margin", r"ISDA SIMM", r"Initial margin on uncleared derivatives is computed from delta, vega and "
                         r"curvature sensitivities, risk class by risk class: thousands of Greeks per counterparty, every "
                         r"day.", color=QC.FIRM, width=6.2, font_size=18),
            history_card(r"capital", r"Basel's FRTB (2019)", r"The standardised approach to market-risk capital is a "
                         r"sensitivities-based method: the same Greeks again, for the regulator.", color=QC.FIRM, width=6.2,
                         font_size=18),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Where does all this run? Every night a bank reprices its whole book under thousands of scenarios: for "
            "risk limits, for capital, and for the valuation adjustments of Part twenty-one, which simulate every "
            "counterparty's exposure years ahead. Trades down, scenarios across; each cell is a pricing. "
            "<bookmark mark='a'/> And it is not only prices. Initial margin on uncleared derivatives, under ISDA's "
            "standard model, is computed from delta, vega and curvature sensitivities. The Basel Committee's 2019 "
            "market-risk rules compute standardised capital from sensitivities too. A large bank needs millions of "
            "Greeks a day, which is exactly the market for adjoint differentiation."
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
                         r"vendor-run.", color=QC.IDEA, width=6.3, font_size=18)
        d = history_card(r"open and cleared", r"QuantLib, ORE, the OCC", r"QuantLib (open source since 2000) ships Sobol "
                         r"paths with a Brownian bridge (chapter 6); ORE (2016, built on QuantLib) adds XVA, with adjoint "
                         r"sensitivities and GPU runs in recent releases. The Options Clearing Corporation sets margin with a "
                         r"Monte Carlo model, STANS.", color=QC.IDEA, width=6.3, font_size=18)
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
        items = [(r"Python loop", par["t_loop"], BAD), (r"numpy, float64", par["t_numpy"], OPT),
                 (r"numpy, float32", par["t_float32"], QC.THETA)] + \
                [(rf"{w} process{'es' if w != '1' else ''} (draw + price)", t, GOOD) for w, t in par["procs"].items()]
        base = par["t_gen_numpy"]
        g = axes([-3.5, 2.5], [0, len(items) + 1], x_length=7.2, y_length=4.4, xlabel=r"seconds for $10^6$ payoffs (log)",
                 xticks=[-3, -2, -1, 0, 1, 2], xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=2.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (nm, t, col) in enumerate(items):
            y = len(items) - i
            x1 = np.clip(np.log10(t), -3.5, 2.5)
            bars.add(VGroup(Rectangle(width=max(ax.c2p(x1, 0)[0] - ax.c2p(-3.5, 0)[0], 0.02), height=0.42, stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(-3.5, y), aligned_edge=LEFT),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(-3.5, y), LEFT, buff=0.15),
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
            MathTex(rf"\text{{COS vs Monte Carlo's best:}}\ {speed:,.0f}\times".replace(",", "{,}"), font_size=26,
                    color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(UP * 1.4)
        loadtxt = wrapped_label(rf"this machine, {par['date']}: {par['cores']} cores shared with other jobs (load "
                                rf"{par['load'][0]:.0f} at the time); best of three", 3.6, 16, GREY_B)
        loadtxt.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        q = predict(r"Monte Carlo is embarrassingly parallel. Is a Longstaff--Schwartz pricing?", width=4.0,
                    font_size=18).to_corner(DR, buff=0.25)
        verdict = ("barely helps here, because the machine is shared and already busy" if sp4 < 1.5 else
                   "helps, though less than the four cores promise")
        with self.voiceover(
            "What does hardware buy on this machine? One million payoffs, priced six ways. A Python loop over the "
            f"paths takes {par['t_loop']:.1f} seconds. <bookmark mark='a'/> The same arithmetic as one vectorised "
            f"numpy line takes {par['t_numpy'] * 1e3:.0f} milliseconds, about {par['t_loop'] / par['t_numpy']:,.0f} "
            "times faster: the first speed-up of every quant is to stop looping. Single precision changes little "
            "here. <bookmark mark='b'/> Splitting the paths over four processes, each with its own random stream, "
            f"{verdict}. <bookmark mark='c'/> And the race said the rest: on one core, the cosine method beat Monte "
            f"Carlo's best accuracy about {speed:,.0f} times faster. Algorithms first. Pause and predict: is "
            "Longstaff–Schwartz embarrassingly parallel? Not fully: every date's regression gathers all the paths."
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
        head = label(r"The House's nightly validation report: every engine function against an independent result",
                     font_size=24, color=QC.HOUSE).to_edge(UP, buff=0.5)
        rows = VGroup(VGroup(label(r"functions", font_size=18, color=GREY_B), label(r"checked against", font_size=18,
                                                                                    color=GREY_B),
                             label(r"tolerance", font_size=18, color=GREY_B)))
        for a_, b_, c_ in VALIDATION:
            rows.add(VGroup(label(a_, font_size=17, color=QC.HOUSE), label(b_, font_size=17, color=GREY_A),
                            label(c_, font_size=17, color=GOOD)))
        for r in rows:
            r[0].move_to([-3.2, 0, 0])
            r[1].move_to([3.0, 0, 0])
            r[2].move_to([5.9, 0, 0])
        rows.arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        for r in rows:
            r[0].set_x(-3.2)
            r[1].set_x(3.0)
            r[2].set_x(5.9)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        foot = wrapped_label(r"\texttt{tests/test\_quant\_house.py}: run on every change; a failing line stops the "
                             r"night's prices", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Finally, the part of the engine no one sees. Every function this part built is checked against an "
            "independent answer, every night: Monte Carlo against closed forms within three standard errors, path "
            "constructions against the covariance to round-off, the American bounds against a tree, the adjoints "
            "against bumps, the grids against Fourier and each other. <bookmark mark='a'/> A failing line stops the "
            "night's prices. Model risk is mostly computation risk, and this report is how the House sleeps."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3, run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
