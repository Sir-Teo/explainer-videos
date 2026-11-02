from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load, loglog, polyline, predict


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
        th = q["theta"]
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
        top = MathTex(rf"a = \sin^2\theta = {q['a']}\ \ (\text{{the price, scaled to }}[0, 1])", font_size=30,
                      color=OPT).to_edge(UP, buff=0.4)
        refl = wrapped_label(r"Grover's operator $Q$: reflect about $|\text{bad}\rangle$, then about the prepared "
                             r"state. Two reflections are a rotation by twice the angle between their mirrors: $2\theta$",
                             5.0, 18, GREY_A).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.2)
        with self.voiceover(
            "Chapter one's error fell like one over root n. A quantum computer can do better; here is how. Load the "
            "distribution of paths into a quantum state, and rotate an extra qubit by each path's payoff. The state is now a vector in a plane: the part "
            "where that qubit reads one, good, and the rest. <bookmark mark='a'/> Its angle theta encodes the "
            "price: the price is sine squared of theta. Measuring once is a coin flip with that probability, which "
            "is just Monte Carlo. <bookmark mark='b'/> Grover's operator is two reflections, and two reflections make "
            "a rotation, by twice theta. Apply it m times and the state sits at angle two m plus one times theta. "
            "<bookmark mark='c'/> The probability of good now oscillates with m, and fast oscillations pin theta "
            "down far more sharply than coin flips ever could."
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
                    r"samples. Suzuki et al.\ (2020) do it without phase estimation, by maximum likelihood")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "In symbols. An operator A prepares the state with amplitude root a on the good part; Rebentrost, Gupt "
            "and Bromley in 2018, and Stamatopoulos and colleagues in 2020, built such circuits for options. <bookmark mark='a'/> Grover's operator, two reflections, rotates by twice theta. "
            "<bookmark mark='b'/> After m applications the good probability is sine squared of two m plus one, times "
            "theta. <bookmark mark='c'/> Combine measurements at several m, and the error falls like one over the "
            "number of oracle calls, against one over its square root for Monte Carlo. Montanaro proved this for "
            "Monte Carlo in general in 2015, and Suzuki and colleagues showed in 2020 that simple maximum likelihood "
            "over a few powers is enough, without the costly phase estimation."
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
                 ylabel=r"likelihood after each power", xticks=[0, np.pi / 4, np.pi / 2],
                 xfmt=lambda v: {0: "0", 1: r"\pi/4"}.get(int(round(4 * v / np.pi)), r"\pi/2"), yticks=[], font_size=14)
        g.to_corner(UL, buff=0.5)
        ax = g.ax
        truth = DashedLine(ax.c2p(q["one"]["theta"], 0), ax.c2p(q["one"]["theta"], 1.1), stroke_color=WHITE, stroke_width=1.5)
        cur = curve(ax, th, curves[0], QC.Q, stroke_width=2.5)
        tag = MathTex(rf"m = {pw[0]}", font_size=28, color=QC.Q).next_to(g, RIGHT, buff=0.2)
        rows = q["rows"]
        calls = np.log10([r["calls"] for r in rows])
        errs = np.array([np.abs(r["errs"]) for r in rows]).T
        h = loglog(1.5, 6, -6, -0.5, r"oracle calls (samples)", r"error in $a$", x_length=5.6, y_length=3.6,
                   xt=[2, 3, 4, 5, 6], yt=[-6, -4, -2], font_size=13).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        hx = h.ax
        band_ = band(hx, calls, np.clip(np.log10(np.percentile(errs, 10, axis=0) + 1e-9), -6, -0.5),
                     np.clip(np.log10(np.percentile(errs, 90, axis=0) + 1e-9), -6, -0.5), QC.Q, 0.18)
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
            "Here it is learning, simulated exactly. Fifty measurements with no Grover steps give a broad likelihood "
            "for theta: Monte Carlo. <bookmark mark='a'/> Add fifty at one step, at two, four, eight, sixteen: each "
            "power multiplies in a faster-oscillating likelihood, and the peaks that agree survive. The curve "
            "sharpens to a needle at the true angle. <bookmark mark='b'/> Repeat forty times and plot the error "
            "against the number of oracle calls. Monte Carlo falls with slope minus a half. Amplitude estimation falls "
            f"with slope {q['slope']:.2f}, near minus one. With {last['calls']:,} calls its error is "
            f"{last['mc'] / last['rmse']:.0f} times smaller than Monte Carlo's at the same count."
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
                         r"Goldman Sachs and IBM: advantage on autocallables and TARFs needs about 8{,}000 logical qubits "
                         r"and a T-depth of 54 million, run in about a second: T-gates at 10 MHz, where the logical "
                         r"clock rates then estimated were around 10 kHz.", color=QC.IDEA, width=6.3, font_size=18)
        b = history_card(2024, r"Stamatopoulos and Zeng (\textit{Quantum})", r"quantum signal processing replaces the "
                         r"arithmetic: about 16 times fewer T-gates and 4 times fewer logical qubits; advantage needs "
                         r"about 4{,}700 logical qubits and $10^9$ T-gates at 45 MHz.", color=QC.IDEA, width=6.3,
                         font_size=18)
        grid = VGroup(a, b).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.6)
        q = predict(r"A quadratic speedup in samples, each sample $10^4$ times slower than a CPU's. When does it win?",
                    width=6.4, font_size=21).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So why do banks still use classical computers? Because the speedup is in samples, not in seconds. In "
            "2021 a team from Goldman Sachs and IBM costed it end to end for real products, autocallables and target "
            "redemption forwards. Beating a classical machine would take about eight thousand error-corrected "
            "logical qubits running a circuit fifty-four million T-gates deep, in about a second: a ten megahertz "
            "rate, where the logical clocks then in prospect ran near ten kilohertz. <bookmark mark='a'/> In 2024 two "
            "of the authors cut that with quantum signal processing: about four thousand seven hundred logical "
            "qubits and a billion T-gates, at forty-five megahertz. Still far beyond any machine built so far. "
            "<bookmark mark='b'/> Pause and predict: a quadratic speedup in samples, but each sample ten thousand times "
            "slower. It wins only once the classical run needs more than about ten thousand squared samples, so only "
            "for the most demanding accuracies."
            " Last, the frontier."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
