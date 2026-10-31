from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import NEURON, PART, load, log_axes

DCOL = {1: "#9BE37B", 2: "#F7D154", 4: "#58A6FF", 8: "#FF9F45", 16: "#D4A5FF", 64: "#FF6B8B"}


class Barron(VoiceoverScene):
    def construct(self):
        self.card()
        self.curse()
        self.maurey()
        self.experiment()
        self.theorem()

    def card(self):
        card = chapter_card(6, r"Escaping the curse", r"How many units does it take in a thousand dimensions?",
                            part=PART)
        with self.voiceover("Chapter six. Escaping the curse of dimensionality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def curse(self):
        m = 6
        s = 0.34
        line = VGroup(*[Dot([-5.8 + i * s, 2.9, 0], radius=0.055, color=DCOL[1]) for i in range(m)])
        sq = VGroup(*[Dot([-5.8 + i * s, 2.05 - j * s, 0], radius=0.05, color=DCOL[2]) for i in range(m) for j in range(m)])
        cube = VGroup(*[Dot([-5.8 + i * s + 0.2 * k, -1.15 - j * s + 0.15 * k, 0], radius=0.04, color=DCOL[4],
                            fill_opacity=0.45 + 0.1 * k) for k in range(m) for i in range(m) for j in range(m)])
        cl = VGroup(MathTex(rf"{m}", font_size=30, color=DCOL[1]).next_to(line, RIGHT, buff=0.4),
                    MathTex(rf"{m}^2 = {m ** 2}", font_size=30, color=DCOL[2]).next_to(sq, RIGHT, buff=0.4),
                    MathTex(rf"{m}^3 = {m ** 3}", font_size=30, color=DCOL[4]).next_to(cube, RIGHT, buff=0.3))
        rows = [cmath(r"n", r"=", r"m^d", font_size=42),
                cmath(r"h", r"=", r"\tfrac{2}{m-1} \ \asymp\ n^{-1/d}", font_size=42),
                cmath(r"\text{miss}", r"\propto", r"h^2 \ \propto\ n^{-2/d}", font_size=42)]
        whys = [why(r"$m$ points along each of $d$ axes"), why(r"the spacing of the grid"),
                why(r"the chord bound of chapter 5, \\ in every direction")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=1.2, buff=0.7, edge=6.9)
        ex = label(r"to halve the miss in $d = 100$: \\ $2^{50}$ times as many points", font_size=34, color=C.SURPRISE)
        ex.move_to([3.0, -1.9, 0])
        with self.voiceover(
            "One layer can draw anything; how many units does it take? A table does the same job with one entry per "
            "point of a grid, and joining the dots in one dimension is exactly a layer of hinges. "
            "<bookmark mark='a'/> But a grid with m points along each axis has m to the d points in d dimensions. "
            "<bookmark mark='b'/> Turn it around: with n points to spend, the spacing scales as n to the minus one over d for large grids, "
            "<bookmark mark='c'/> and the miss shrinks like n to the minus two over d. <bookmark mark='d'/> In a "
            "hundred dimensions, halving the miss takes two to the fiftieth times as many points. That's the curse "
            "of dimensionality, Richard Bellman's phrase."
        ) as vo:
            self.play(FadeIn(line), FadeIn(cl[0]), FadeIn(sq), FadeIn(cl[1]))
            self.play(FadeIn(cube), FadeIn(cl[2]))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maurey(self):
        colors = {r"\omega": NEURON, r"\omega_k": NEURON}
        rows = [cmath(r"f(x)", r"=", r"\mathbb{E}_{\omega}\big[\cos(", r"\omega", r"\cdot x)\big]", font_size=36,
                      colors=colors),
                cmath(r"f_n(x)", r"=", r"\tfrac{1}{n} \textstyle\sum_{k=1}^{n} \cos(", r"\omega_k", r"\cdot x)",
                      font_size=36, colors=colors),
                cmath(r"\mathbb{E}\,|f_n(x) - f(x)|^2", r"=", r"\tfrac{1}{n}\, \operatorname{Var}\cos(", r"\omega",
                      r"\cdot x)", font_size=36, colors=colors),
                cmath(r"\mathbb{E}_{\omega}\!\int |f_n(x) - f(x)|^2\,d\mu(x)", r"\le", r"\tfrac{1}{n}", font_size=34, colors=colors)]
        whys = [why(r"$f$ is an average of cosine units: \\ a Gaussian bump, \ its Fourier transform"),
                why(r"$n$ units, \ directions $\omega_k$ drawn at random"),
                why(r"an average of $n$ independent draws"),
                why(r"$|\cos| \le 1$: \ average over a fixed input distribution $\mu$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.0, buff=0.45, edge=6.9)
        some = label(r"the average over random choices \\ is $\le 1/n$, \ so \textit{some} choice \\ of $n$ units is "
                     r"within $1/\sqrt{n}$ in $L^2(\mu)$, \\ in any dimension", font_size=28, color=C.BITS).move_to([3.9, -2.2, 0])
        # in one dimension: the Gaussian bump, and the average of n cosines with random frequencies (illustrative draw)
        ax = Axes(x_range=[-4, 4, 1], y_range=[-1.0, 1.1, 0.5], x_length=6.6, y_length=2.1, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-2.9, -2.4, 0])
        xg = np.linspace(-4, 4, 321)
        gs = np.random.default_rng(1993)  # an illustrative draw of random frequencies
        om = gs.standard_normal(100)
        bump = DashedVMobject(curve(ax, xg, np.exp(-xg ** 2 / 2), WHITE, 3), num_dashes=50)
        waves = VGroup(*[curve(ax, xg, np.cos(w_ * xg), NEURON, 1.5).set_stroke(opacity=0.35) for w_ in om[:5]])

        def avg(n_):
            return curve(ax, xg, np.cos(np.outer(om[:n_], xg)).mean(0), C.BITS, 4)

        nl = VGroup(MathTex(r"n = ", font_size=30, color=C.BITS), Integer(5, font_size=30, color=C.BITS))
        nl.arrange(RIGHT, buff=0.1).move_to(ax.c2p(3.0, 0.8))
        dl = label(r"$d = 1$: \ the bump \ (dashed), \ random cosines, \ their average", font_size=22, color=GREY_A)
        dl.next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        itag = note(r"illustrative: \ one random draw").next_to(ax, DOWN, buff=0.1).align_to(ax, LEFT)
        f5, f100 = avg(5), avg(100)
        cite_ = cite(r"B.~Maurey, \ via G.~Pisier (1981); \ L.~K.~Jones (1992); \ A.~R.~Barron (1993)", corner=DR)
        with self.voiceover(
            "In 1993 Andrew Barron showed that networks escape this, for a large class of functions, and the reason "
            "fits on one screen. Take a smooth bump, a Gaussian, in d dimensions. <bookmark mark='a'/> It is exactly "
            "an average of cosine waves, one for each direction omega, weighted by its Fourier transform. "
            "<bookmark mark='b'/> Draw n directions at random and average just those n waves: a network with n units, "
            "each a wave in one direction. <bookmark mark='c'/> At any point, that's an average of n independent "
            "draws, so its squared error is the variance of one draw, divided by n. <bookmark mark='d'/> And a "
            "cosine lies between minus one and one, so the expected squared error is at most one over n. Average over inputs under any fixed probability distribution, and the same bound holds, with no d anywhere. "
            "<bookmark mark='e'/> If random units do that well on average, some particular choice of n units does at "
            "least as well in mean squared error under that input distribution, in any dimension. The argument is Bernard Maurey's, from probability."
        ) as vo:
            step(0)
            self.play(Create(ax), Create(bump), FadeIn(dl), FadeIn(itag))
            vo.wait_until("a")
            self.play(Indicate(rows[0][3], color=NEURON), FadeIn(cite_), LaggedStart(*[Create(w_) for w_ in waves],
                                                                                      lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            step(1)
            self.play(Create(f5), FadeIn(nl))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeOut(waves), Transform(f5, f100), ChangeDecimalToValue(nl[1], 100), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(some))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        b = load("barron")
        ns = np.asarray(b["mc_n"], float)
        g = log_axes([0, 5], [-4, 0], 7.4, 4.6, center=[-1.6, -0.5, 0], xlabel=r"units \ (network) \ or points \ (grid)",
                     ylabel=r"typical miss \ (log scale)", xticks=range(0, 6), yticks=range(-4, 1))
        ax = g.ax

        def path(n, e, col, dashed=False):
            m = curve(ax, np.log10(n), np.log10(np.maximum(e, 1e-4)), col, 4)
            return DashedVMobject(m, num_dashes=24) if dashed else m

        grids = {d: path(np.asarray(b[f"grid_n{d}"], float), np.asarray(b[f"grid{d}"]), DCOL[d], True)
                 for d in (1, 2, 4, 8)}
        mcs = {d: path(ns, np.asarray(b[f"mc{d}"]), DCOL[d]) for d in (1, 4, 16, 64)}
        gl = legend([(DCOL[d], rf"grid, \ $d = {d}$") for d in (1, 2, 4, 8)], font_size=20)
        ml = legend([(DCOL[d], rf"random units, \ $d = {d}$") for d in (1, 4, 16, 64)], font_size=20)
        VGroup(gl, ml).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([5.2, 0.2, 0])
        for row in gl:
            row[0].become(DashedLine(row[0].get_start(), row[0].get_end(), color=row[0].get_color(), stroke_width=5,
                                     dash_length=0.08))
        tag = note(r"computed: \ the Gaussian bump on $[-1, 1]^d$; \ grid: \ joining the dots").to_corner(DR, buff=0.2)
        sl = {int(k): float(v) for k, v in b["mc_slope"].items()}
        gs = {int(k): float(v) for k, v in b["grid_slope"].items()}
        g8, g8n = float(np.asarray(b["grid8"])[-1]), int(np.asarray(b["grid_n8"])[-1])
        mc64 = float(np.asarray(b["mc64"])[-1])
        with self.voiceover(
            "Here it is, computed. <bookmark mark='a'/> First the grid, in one, two, four and eight dimensions: the "
            f"lines flatten, with slopes of {gs[1]:.1f}, {gs[2]:.1f}, {gs[4]:.2f} and {gs[8]:.2f}, close to minus two "
            f"over d. In eight dimensions, {g8n:,} points still miss by {g8:.3f}. <bookmark mark='b'/> Now n random "
            "cosine units, in one, four, sixteen and sixty-four dimensions. The four lines lie on top of each other, "
            f"with slopes between {min(sl.values()):.2f} and {max(sl.values()):.2f}: the miss falls like one over the "
            f"square root of n, whatever the dimension. In sixty-four dimensions, {int(ns[-1]):,} units miss by "
            f"{mc64:.4f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(grids[d]) for d in (1, 2, 4, 8)], lag_ratio=0.4), FadeIn(gl), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(mcs[d]) for d in (1, 4, 16, 64)], lag_ratio=0.4), FadeIn(ml), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        th = theorem_card(r"Barron's bound",
                          r"if $C_f = \int |\omega|\, |\hat f(\omega)|\, d\omega$ is finite, \ a network with one hidden "
                          r"layer of $n$ sigmoid units has \ $\int (f - f_n)^2\, d\mu \ \le\ (2 r C_f)^2 / n$ \ on a ball "
                          r"of radius $r$: \ a rate that does not depend on the dimension", who=r"A.~R.~Barron (1993)",
                          width=11.0, font_size=27, color=NEURON).move_to(UP * 1.6)
        notes_ = VGroup(
            label(r"any $n$ functions fixed in advance do no better than $n^{-1/d}$ \ on this class: \\ the network "
                  r"wins by choosing its units' directions to fit $f$", font_size=26, color=GREY_A),
            label(r"the catch: \ $C_f$ can be enormous for rough functions; \\ and it says nothing about whether "
                  r"training finds the units", font_size=26, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 1.7)
        with self.voiceover(
            "Barron's theorem says this for ordinary S-shaped units, for every function whose Fourier transform, "
            "weighted by frequency, has a finite total, C f: the squared miss is at most two r C f, squared, over n. "
            "<bookmark mark='a'/> He also showed what a fixed basis can't do: any n functions chosen before you see "
            "f, such as a grid's, can do no better than n to the minus one over d on this class. The network escapes "
            "because it chooses the directions of its units to suit f. <bookmark mark='b'/> The catch: for rough, "
            "wiggly functions C f can be astronomically large, and the theorem says nothing about whether gradient "
            "descent will find the units. Still, it was the first hint of why networks work in high dimensions."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(notes_[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(notes_[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
