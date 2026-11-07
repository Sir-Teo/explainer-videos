from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load, loglog, polyline, predict, axes, data_range, pause_card, flat_camera


class Quantum(VoiceoverScene):
    def construct(self):
        q = load("qae")
        self.card()
        self.rotation(q)
        self.proof()
        self.replay(q)
        self.cost()

    def card(self):
        c = chapter_card(18, r"Quantum amplitude estimation", r"What would a quantum computer actually speed up?",
                         lit=(2021,), part=PART)
        with self.voiceover("Chapter eighteen. Quantum amplitude estimation: the real speedup, and its price."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rotation(self, q):
        th = float(np.arcsin(np.sqrt(q["a"])))  # a = sin^2(theta)
        o = LEFT * 2.6 + DOWN * 0.6
        R = 2.8
        good = Arrow(o, o + UP * R, buff=0, stroke_width=2, color=GOOD, tip_length=0.15)
        bad = Arrow(o, o + RIGHT * R, buff=0, stroke_width=2, color=BAD, tip_length=0.15)
        lg = label(r"$|\text{good}\rangle$: the payoff's ancilla reads 1", font_size=18, color=GOOD).next_to(good, UP, buff=0.1)
        lb = label(r"$|\text{bad}\rangle$", font_size=20, color=BAD).next_to(bad, RIGHT, buff=0.1)
        arc = Arc(radius=R, start_angle=0, angle=PI / 2, arc_center=o, stroke_color=GREY_D, stroke_width=1.5)
        ang = ValueTracker(th)
        vec = always_redraw(lambda: Arrow(o, o + R * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]), buff=0,
                                          stroke_width=5, color=OPT, tip_length=0.2))
        proj = always_redraw(lambda: DashedLine(o + R * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                                o + R * np.array([0, np.sin(ang.get_value()), 0]), stroke_color=GREY_B,
                                                stroke_width=1.5))
        m = ValueTracker(0)
        rd = VGroup(readout(r"m =", lambda: round(m.get_value()), digits=0, font_size=28, color=OPT),
                    readout(r"P(\text{good}) = \sin^2\big((2m + 1)\theta\big) =",
                            lambda: np.sin((2 * round(m.get_value()) + 1) * th) ** 2, digits=3, font_size=28, color=GOOD),
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        top = MathTex(rf"a = \sin^2\theta = {q['a']}\ \ (\text{{toy bounded mean in }}[0, 1])", font_size=30,
                      color=OPT).to_edge(UP, buff=0.4)
        refl = wrapped_label(r"Grover's operator $Q$: reflect about $|\text{bad}\rangle$, then about the prepared "
                             r"state. Two reflections are a rotation by twice the angle between their mirrors: $2\theta$",
                             5.0, 18, GREY_A).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.2)
        with self.voiceover(
            "Amplitude estimation concerns oracle queries, before charging for building the oracle. Imagine a coherently prepared path distribution and a bounded payoff scaled into zero to one. An unbounded call requires truncation or another justified encoding, with its own error. <bookmark mark='a'/> The good-state probability a equals sine squared theta; one measurement is a Bernoulli observation. Our numerical demonstration uses a toy mean, not an encoded financial path distribution. <bookmark mark='b'/> The ideal Grover operator combines two reflections, rotating this two-dimensional subspace by twice theta. Its construction requires coherent state preparation and its inverse. <bookmark mark='c'/> Measurements at several powers can sharpen an angle estimate, while aliases, failure probability and oracle cost remain essential. The geometry describes an ideal operation rather than a circuit we have run."
        ) as vo:
            self.play(FadeIn(top), Create(good), Create(bad), FadeIn(lg), FadeIn(lb), Create(arc))
            vo.wait_until("a")
            self.play(FadeIn(vec), FadeIn(proj), FadeIn(rd))
            vo.wait_until("b")
            self.play(FadeIn(refl))
            for k in (1, 2, 3):
                self.play(m.animate.set_value(k), ang.animate.set_value((2 * k + 1) * th), run_time=1.4)
                self.wait(0.4)
            vo.wait_until("c")
            self.play(m.animate.set_value(0), ang.animate.set_value(th), run_time=1.2)
        for x in (vec, proj, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\mathcal{A}|0\rangle", r"=", r"\sqrt{1 - a}\,|\psi_0\rangle|0\rangle + \sqrt a\,|\psi_1\rangle|1\rangle,"
                  r"\quad a = \mathbb{E}[\tilde f(X)]", font_size=32, colors={r"\mathcal{A}|0\rangle": OPT}),
            cmath(r"Q", r"=", r"-\mathcal{A}S_0\mathcal{A}^{-1}S_\chi\ \ \text{rotates by } 2\theta,\ \ a = \sin^2\theta",
                  font_size=32),
            cmath(r"P(\text{good after } Q^m)", r"=", r"\sin^2\big((2m + 1)\theta\big)", font_size=34, colors={r"=": GOOD}),
            cmath(r"\text{error}", r"=", r"O(1/N)\ \text{oracle calls, against } O(1/\sqrt N)", font_size=34,
                  colors={r"\text{error}": GOOD}),
        ]
        whys = [why(r"load the distribution, then rotate an ancilla by the (normalised) payoff (Rebentrost, Gupt and "
                    r"Bromley 2018; Stamatopoulos et al.\ 2020)"),
                why(r"the product of two reflections is a rotation by twice the angle between them"),
                why(r"apply the rotation $m$ times"),
                why(r"Brassard, H{\o}yer, Mosca and Tapp (2002); Montanaro (2015) for Monte Carlo: quadratically fewer "
                    r"oracle queries for bounded normalized means at fixed success probability; confidence amplification and implementation costs are additional")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "For a normalized payoff between zero and one, the preparation operator puts square root a on the good subspace. <bookmark mark='a'/> The ideal Grover iterate uses that preparation, its inverse and reflections. <bookmark mark='b'/> After m iterates the good probability is sine squared of two m plus one times theta. <bookmark mark='c'/> Standard amplitude-estimation guarantees can achieve additive error of order one over query count at fixed success probability, compared with Monte Carlo's inverse-square-root sampling scale. Confidence amplification adds factors. Specific maximum-likelihood schedules also need alias and failure analysis. Neither this oracle statement nor Montanaro's broader algorithms establish an end-to-end speedup for an arbitrary derivative-pricing program."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, q):
        th = np.asarray(q["theta_grid"])
        curves = [np.asarray(c) for c in q["curves"]]
        pw = q["powers6"]
        g = axes([0, np.pi / 2], [0, 1.1], x_length=5.4, y_length=3.0, xlabel=r"$\theta$",
                 ylabel=r"likelihood divided by its maximum after each power", xticks=[0, np.pi / 4, np.pi / 2],
                 xfmt=lambda v: {0: "0", 1: r"\pi/4"}.get(int(round(4 * v / np.pi)), r"\pi/2"), yticks=[], font_size=14)
        g.to_corner(UL, buff=0.5)
        ax = g.ax
        truth = DashedLine(ax.c2p(q["one"]["theta"], 0), ax.c2p(q["one"]["theta"], 1.1), stroke_color=WHITE, stroke_width=1.5)
        cur = curve(ax, th, curves[0], QC.Q, stroke_width=2.5)
        tag = MathTex(rf"m = {pw[0]}", font_size=28, color=QC.Q).next_to(g, RIGHT, buff=0.2)
        rows = q["rows"]
        calls = np.log10([r["calls"] for r in rows])
        errs = np.array([np.abs(r["errs"]) for r in rows]).T
        p10 = np.percentile(errs, 10, axis=0)
        p90 = np.percentile(errs, 90, axis=0)
        yr = data_range(np.log10(p10), np.log10(p90), np.log10([r["rmse"] for r in rows]), np.log10([r["mc"] for r in rows]))
        h = loglog(*data_range(calls), *yr, r"oracle queries $\sum_m 50(2m+1)$", r"error in $a$", x_length=5.6, y_length=3.6,
                   xt=[2, 3, 4, 5, 6], yt=[-6, -4, -2], font_size=13).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        hx = h.ax
        band_ = band(hx, calls, np.log10(p10),
                     np.log10(p90), QC.Q, 0.18)
        qline = polyline(hx, calls, np.log10([r["rmse"] for r in rows]), QC.Q, radius=0.04)
        mline = polyline(hx, calls, np.log10([r["mc"] for r in rows]), GREY_B, radius=0.04)
        leg = legend([(QC.Q, rf"amplitude estimation (40 runs; slope {q['slope']:.2f})"),
                      (GREY_B, r"Monte Carlo, same calls (slope $-0.5$)")], font_size=15).next_to(h, UP, buff=0.1)
        leg.align_to(h, LEFT)
        last = rows[-1]
        side = MathTex(rf"{last['calls']:,}".replace(",", "{,}") + rf"\ \text{{calls: }}{last['rmse']:.1e}\ \text{{vs}}\ "
                       rf"{last['mc']:.1e}\ (\times {last['mc'] / last['rmse']:.0f})", font_size=26, color=GOOD)
        side.to_corner(DL, buff=0.5)
        src = illustration(r"an exact simulation of the measurement statistics (not a circuit); 50 shots per power",
                           corner=DR)
        with self.voiceover(
            f"The toy amplitude is {q['a']:.1f}. We simulate only ideal binomial measurement counts, not quantum circuits, state preparation or financial paths. Each likelihood curve is divided by its maximum, so it is neither a normalized probability density nor a posterior. <bookmark mark='a'/> Fifty shots at each scheduled Grover power multiply oscillating likelihood factors. Resolving aliases depends on the schedule and finite-grid maximum-likelihood procedure. <bookmark mark='b'/> Forty independent repetitions give empirical RMSE, fitted slope {q['slope']:.2f}. The band is the tenth-to-ninetieth percentile of absolute errors, not a confidence interval. The comparator is the analytical Bernoulli Monte Carlo RMSE at the same summed oracle-query budget. At {last['calls']:,} queries the ratio is {last['mc'] / last['rmse']:.0f}. This is an ideal statistical experiment, with no wall-clock or gate-level advantage measured."
        ) as vo:
            self.play(FadeIn(g), FadeIn(truth), Create(cur), FadeIn(tag))
            vo.wait_until("a")
            for k in range(1, len(curves)):
                self.play(Transform(cur, curve(ax, th, curves[k], QC.Q, stroke_width=2.5)),
                          Transform(tag, MathTex(rf"m = {pw[k]}", font_size=28, color=QC.Q).move_to(tag)), run_time=1.0)
                self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(h), FadeIn(band_), Create(mline), Create(qline), FadeIn(leg), FadeIn(src))
            self.play(FadeIn(side))
        self.wait(0.5)
        self.clear_scene()

    def cost(self):
        a = history_card(2021, r"Chakrabarti, Krishnakumar, Mazzola, Stamatopoulos, Woerner, Zeng (\textit{Quantum})",
                         r"Autocallable resource case: 3 assets, 20 steps, target error $2\times10^{-3}$; 8{,}000 logical qubits, "
                         r"T-count $1.2\times10^{10}$, T-depth $5.4\times10^7$. TARF is a different resource case. "
                         r"These are dated fault-tolerant estimates, not measured runtime.", color=QC.IDEA, width=6.3, font_size=22)
        b = history_card(2024, r"Stamatopoulos and Zeng (\textit{Quantum})", r"QSP autocallable case: 4{,}700 logical qubits, total T-count $2.4\times10^9$, T-depth $4.5\times10^7$. "
                         r"Matching an assumed classical second needs a 45 MHz sequential T-layer rate. The quoted 16-fold T-count "
                         r"and 4-fold qubit gains compare this paper's 19{,}200-qubit arithmetic reference.", color=QC.IDEA, width=6.3,
                         font_size=22)
        grid = VGroup(a, b).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.6)
        q = predict(r"A quadratic speedup in samples, each sample $10^4$ times slower than a CPU's. When does it win?",
                    width=6.4, font_size=21).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two primary papers estimate resources under different stated constructions. In the twenty-twenty-one autocallable case, three assets and twenty time steps at target error two thousandths require roughly eight thousand logical qubits. The T-count is twelve billion and sequential T-depth fifty-four million. Counts and depths are different. This is not a demonstrated runtime, and the paper's TARF case has different resources. <bookmark mark='a'/> In twenty-twenty-four, the quantum-signal-processing construction reports about four thousand seven hundred logical qubits, total T-count two point four billion and T-depth forty-five million. Its amplitude-estimation tolerance is one thousandth at stated confidence point six eight. Matching an assumed classical second requires forty-five million sequential T-layers per second, not that many total gates per second. The sixteen-fold count and four-fold qubit improvements compare that paper's arithmetic reference, not the earlier eight-thousand-qubit headline. Error correction, physical qubits and state-preparation costs remain part of implementation. <bookmark mark='b'/> In a toy cost model, classical work proportional to one over error squared competes with quantum query work proportional to R over error. With equal normalized constants, crossover is near classical sample count R squared. If R is ten thousand, that is about one hundred million. Actual constants, payoff scale, confidence and an accuracy-dependent oracle cost can change the result."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
