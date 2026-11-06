from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class KleeMinty(VoiceoverScene):
    def construct(self):
        self.card()
        self.cube()
        self.counts()
        self.smoothed()

    def card(self):
        card = chapter_card(4, r"Exponential in theory, \ fast in practice", r"Can the walk take forever?",
                            lit=(1972, 2001), extra=((1972, r"Klee--Minty"), (2001, r"smoothed analysis")), part=PART)
        with self.voiceover("Chapter four. Exponential in theory, fast in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cube(self):
        k = load("kleeminty")
        V = [tuple(v) for v in k["cube_vertices"]]
        F = k["cube_faces"]
        path = k["cube_path"]
        mx = np.max(np.array(V), axis=0)
        Vn = [tuple(np.array(v) / mx * np.array([2.4, 2.4, 2.4])) for v in V]
        pn = [tuple(np.array(p) / mx * np.array([2.4, 2.4, 2.4])) for p in path]
        head = label(r"The Klee--Minty cube", font_size=34).to_edge(UP, buff=0.3)
        view = View3(origin=LEFT * 2.6 + DOWN * 1.0, scale=1.3, th=-0.7, ph=0.35, center=(1.2, 1.2, 1.2))
        poly = always_redraw(lambda: view.polytope(Vn, F, color=DATA, opacity=0.16))
        here = ValueTracker(0.0)

        def trail():
            t = here.get_value()
            g = VGroup()
            for i in range(min(int(t), len(pn) - 1)):
                g.add(Line(view.p(pn[i]), view.p(pn[i + 1]), color=HEAD, stroke_width=4))
            k_ = min(int(t), len(pn) - 2)
            f = t - k_
            a, b = np.array(pn[k_]), np.array(pn[k_ + 1])
            g.add(Dot(view.p(*(a + (b - a) * min(f, 1.0))), radius=0.1, color=HEAD))
            return g
        tr = always_redraw(trail)
        side = VGroup(
            label(r"Klee and Minty (1972): \ a cube, \ squashed", font_size=22, color=WHITE),
            label(r"each coordinate's bounds depend on the one before: \\ $\varepsilon x_{j-1} \le x_j \le 1 - "
                  r"\varepsilon x_{j-1}$", font_size=22, color=LAM),
            label(r"Dantzig's rule visits \textbf{every} vertex: \\ $2^n$ of them, \ always uphill", font_size=22,
                  color=NO),
            label(rf"here $n = 3$: \ {len(path) - 1} pivots, \ all 8 corners", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "How many pivots can the simplex method need? <bookmark mark='a'/> In 1972 Victor Klee and George Minty "
            "built a bad example: a cube, squashed so that it is no longer square. <bookmark mark='b'/> Each "
            "coordinate's bounds depend a little on the coordinate before it, which tilts every face slightly. "
            "<bookmark mark='c'/> On this cube, Dantzig's rule visits every vertex before reaching the top, "
            "climbing at every step. In n dimensions that is two to the n vertices. <bookmark mark='d'/> Here in "
            "three dimensions: seven pivots, through all eight corners."
        ) as vo:
            self.play(FadeIn(head))
            self.add(poly, tr)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), view.th.animate.set_value(-0.35), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            for i in range(1, len(pn)):
                self.play(here.animate.set_value(i - 0.001 if i == len(pn) - 1 else i), run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), view.th.animate.set_value(-0.9), run_time=2.0)
        poly.clear_updaters()
        tr.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        k = load("kleeminty")
        head = label(r"Pivots on Klee--Minty cubes", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["n"]), words(r["dantzig"]), words(2 ** r["n"] - 1), words(r["bland"]), words(r["steepest"])]
                for r in k["rows"]]
        tab = grid_table([r"$n$", r"Dantzig", r"$2^n - 1$", r"Bland", r"greatest improvement"], rows,
                         widths=[0.9, 1.7, 1.7, 1.5, 3.2], row_h=0.37, font_size=20, mono_cols=(),
                         colors=[[WHITE, NO, GREY_A, LAM, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        side = VGroup(
            label(r"Dantzig: \ exactly $2^n - 1$, \ every time", font_size=22, color=NO),
            label(r"Bland's rule is exponential here too \\ (Avis and Chv\'atal, 1978)", font_size=22, color=LAM),
            label(r"greatest improvement solves this cube in one pivot, \\ but Jeroslow (1973) built cubes that defeat it",
                  font_size=22, color=YES),
            label(r"almost every rule proposed has its own bad cube; \\ Zadeh's rule fell in 2011 \ (Friedmann)",
                  font_size=22, color=HEAD),
            label(r"no pivot rule is known to be polynomial", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "We ran our simplex on Klee–Minty cubes up to twelve dimensions. <bookmark mark='a'/> Dantzig's rule "
            "takes exactly two to the n minus one pivots, every time: four thousand and ninety-five at twelve. "
            "<bookmark mark='b'/> Bland's rule does better on this cube but is exponential on its own variants, as "
            "David Avis and Chvátal showed. <bookmark mark='c'/> The greatest-improvement rule, which tries every "
            "edge and takes the one that gains most, solves this cube in one pivot; Robert Jeroslow built cubes in "
            "1973 that defeat it too. <bookmark mark='d'/> The pattern repeated for decades: almost every pivot rule "
            "proposed has acquired its own bad example, the last famous one, Zadeh's rule, in 2011. <bookmark "
            "mark='e'/> No pivot rule is known to run in polynomial time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.1))
            for mk, s_ in zip("abcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.wait(0.3)
        self.clear_scene()

    def smoothed(self):
        k = load("kleeminty")
        head = label(r"Why it works anyway: \ smoothed analysis", font_size=34).to_edge(UP, buff=0.35)
        r1 = [[rf"{p['sigma']:g}", f"{p['mean']:.0f}", str(p["max"])] for p in k["perturbed"]]
        t1 = grid_table([r"noise $\sigma$", r"mean pivots", r"worst"], r1, widths=[1.8, 2.0, 1.4], row_h=0.4,
                        font_size=20, mono_cols=(), colors=[[WHITE, NO, GREY_A]] * len(r1))
        c1 = label(rf"Klee--Minty, \ $n = {k['perturbed_n']}$, \ every entry of $A$ \\ multiplied by $1 + \sigma g$, \ "
                   r"$g$ Gaussian", font_size=18, color=GREY_A)
        g1 = VGroup(c1, t1).arrange(DOWN, buff=0.2)
        r2 = [[f"{p['n']} $\\times$ {p['m']}", f"{p['mean']:.1f}", str(p["max"])] for p in k["random"]]
        t2 = grid_table([r"random LP", r"mean pivots", r"worst"], r2, widths=[2.2, 2.0, 1.4], row_h=0.4,
                        font_size=20, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(r2))
        c2 = label(r"random dense LPs, \ 20 of each size", font_size=18, color=GREY_A)
        g2 = VGroup(c2, t2).arrange(DOWN, buff=0.2)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        notes = VGroup(
            label(r"in practice: \ a small multiple of the number of constraints \ (here under half of $m$)",
                  font_size=22, color=YES),
            label(r"Spielman and Teng (2001): \ perturb any LP by Gaussian noise of size $\sigma$; \ the expected pivots "
                  r"are polynomial in $n$, $m$ and $1/\sigma$", font_size=22, color=LAM),
            label(r"bad instances are knife-edge constructions: \ shake them and they fall over", font_size=22,
                  color=HEAD),
            label(r"G\"odel Prize 2008; \ the idea now explains $k$-means, \ local search and more", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Yet the simplex method is fast on real problems, usually a small multiple of the number of "
            "constraints. Why? <bookmark mark='a'/> On random dense programs our simplex took under half as many "
            "pivots as there are constraints: thirty-four on average for a hundred and sixty. <bookmark mark='b'/> "
            "Daniel Spielman and Shang-Hua Teng explained it in 2001 with smoothed analysis: take any linear "
            "program, even the worst, and add a little Gaussian noise to its data. The expected number of pivots is "
            "then polynomial in the size and in one over the size of the noise. <bookmark mark='c'/> The bad "
            "instances are knife-edge constructions. Shake them and they fall over. On our ten-dimensional cube, "
            "tiny noise changes nothing, but noise of ten percent cuts the thousand and twenty-three pivots to about "
            "four hundred, and thirty percent to about seventy-five. <bookmark mark='d'/> They won the Gödel Prize "
            "for it, and smoothed analysis now explains why other algorithms that are bad in the worst case work in "
            "practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(g1), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
