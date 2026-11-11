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
            label('fixed power variant: \\\\ $0\\le x_j,\\quad x_j+\\sum_{i<j}2^{j-i+1}x_i\\le5^{j+1}$ \\\\ $\\max\\sum_j2^{n-1-j}x_j$; zero-based indices', font_size=22, color=LAM),
            label(r"Dantzig's rule visits \textbf{every} vertex: \\ $2^n$ of them, \ always uphill", font_size=22,
                  color=NO),
            label(rf"here $n = 3$: \ {len(path) - 1} pivots, \ all 8 corners", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            (
            "How many pivots can simplex need? <bookmark mark='a'/> Klee and Minty constructed deformed cubes "
            "showing exponential behavior for Dantzig's rule. <bookmark mark='b'/> We execute a fixed "
            'power-coefficient variant: each upper row depends on all earlier coordinates, with powers of two in '
            'the matrix and powers of five on the right. The objective also uses powers of two. This is the '
            "model drawn here after rescaling the axes. <bookmark mark='c'/> Exact arithmetic checks feasibility "
            'and strict objective increase at every visited vertex. Dantzig visits all two to the n vertices on '
            "these instances. <bookmark mark='d'/> In three dimensions that is seven pivots through eight "
            'corners, not a theorem about every pivot rule or every cube.'
        )
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
            label("Bland's observed counts on this variant; \\\\ separate variants give exponential lower bounds", font_size=22, color=LAM),
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
        head = label('Finite experiments and a separate smoothed theorem', font_size=34).to_edge(UP, buff=0.35)
        r1 = [[rf"{p['sigma']:g}", f"{p['mean']:.0f}", str(p["max"]), str(p["unbounded_trials"])] for p in k["perturbed"]]
        t1 = grid_table([r"noise $\sigma$", r"optimal mean", r"worst", r"unbounded"], r1, widths=[1.4, 1.7, 1.2, 1.5], row_h=0.4,
                        font_size=20, mono_cols=(), colors=[[WHITE, NO, GREY_A, GREY_A]] * len(r1))
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
            label('100 seeded positive dense LPs: \\ finite pivot observations',
                  font_size=22, color=YES),
            label('Spielman--Teng: \\ two-phase shadow vertex; \\\\ additive Gaussian normals and RHS; \\ expected polynomial in dimensions and $1/\\sigma$', font_size=22, color=LAM),
            label('our Dantzig experiment: \\ multiplicative matrix noise; \\\\ zeros stay zero; \\ not the theorem model', font_size=22,
                  color=HEAD),
            label(r"G\"odel Prize 2008; \ the idea now explains $k$-means, \ local search and more", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Finite experiments and smoothed analysis answer different questions. <bookmark mark='a'/> Our dense "
            'positive random LPs take relatively few Dantzig pivots on these one hundred seeded instances; their '
            "optimal values are checked independently. <bookmark mark='b'/> Spielman and Teng analyze a "
            'particular two-phase shadow-vertex method under additive Gaussian perturbations of constraint '
            'normals and right-hand sides. Their expected polynomial bound depends on dimensions and inverse '
            "perturbation scale. It is not a theorem for our Dantzig implementation. <bookmark mark='c'/> Our "
            'separate cube experiment multiplies nonzero matrix entries by one plus sigma times a Gaussian. '
            'Zeros stay zero. The table summarizes only optimal runs and separately counts unbounded ones; every '
            "status is checked against another solver. <bookmark mark='d'/> These observations illustrate "
            'sensitivity under this chosen model. They do not establish the shadow-vertex theorem, nor show that '
            'all bad instances disappear under arbitrary noise.'
        )
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
