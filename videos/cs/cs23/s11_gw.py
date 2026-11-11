from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import optim as O
from fractions import Fraction
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class MaxCut(VoiceoverScene):
    def construct(self):
        self.card()
        self.sphere()
        self.local_bound()
        self.alpha()
        self.measured()

    def card(self):
        card = chapter_card(10, r"A random hyperplane: \ MAX-CUT", r"How do you split a graph to cut the most edges?",
                            lit=(1995,), extra=((1995, r"Goemans--Williamson"),), part=PART)
        with self.voiceover("Chapter ten. A random hyperplane: MAX-CUT."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sphere(self):
        g = load("gw")
        V = np.array(g["V3"])
        E = [tuple(e) for e in g["E"]]
        head = label(r"Relax the two sides to unit vectors", font_size=32).to_edge(UP, buff=0.3)
        view = View3(origin=LEFT * 2.8 + DOWN * 0.3, scale=2.4, th=-0.4, ph=0.35)
        rnd = np.random.default_rng(7).standard_normal(3)
        rnd /= np.linalg.norm(rnd)
        show_cut = ValueTracker(0.0)

        def world():
            gg = VGroup()
            for t in np.linspace(0, math.pi, 7)[1:-1]:
                pts = [view.p(math.sin(t) * math.cos(u), math.sin(t) * math.sin(u), math.cos(t))
                       for u in np.linspace(0, TAU, 49)]
                gg.add(VMobject(color=GREY_E, stroke_width=1).set_points_as_corners(pts))
            for u in np.linspace(0, math.pi, 7)[:-1]:
                pts = [view.p(math.sin(t) * math.cos(u), math.sin(t) * math.sin(u), math.cos(t))
                       for t in np.linspace(0, TAU, 49)]
                gg.add(VMobject(color=GREY_E, stroke_width=1).set_points_as_corners(pts))
            side = V @ rnd >= 0
            c = show_cut.get_value()
            for u, v in E:
                cut = side[u] != side[v]
                col = interpolate_color(ManimColor(GREY_B), ManimColor(YES if cut else GREY_D), c)
                gg.add(Line(view.p(V[u]), view.p(V[v]), color=col, stroke_width=1.5 + 1.5 * c * cut))
            for i in range(len(V)):
                col = interpolate_color(ManimColor(WHITE), ManimColor(DATA if side[i] else HEAD), c)
                gg.add(Dot(view.p(V[i]), radius=0.07, color=col))
            if c > 0.01:
                a = np.cross(rnd, [0, 0, 1.0])
                a /= np.linalg.norm(a)
                b = np.cross(rnd, a)
                ring = [view.p(math.cos(t) * a + math.sin(t) * b) for t in np.linspace(0, TAU, 73)]
                gg.add(VMobject(color=NO, stroke_width=3, stroke_opacity=c).set_points_as_corners(ring))
            return gg
        w = always_redraw(world)
        side = VGroup(
            label(r"MAX-CUT: \ split the vertices into two sides, \\ cutting as many edges as possible: \ NP-hard",
                  font_size=21, color=WHITE),
            label(r"sides as signs: \ $x_i = \pm 1$; \ an edge is cut when $x_i x_j = -1$", font_size=21, color=GREY_A),
            MathTex(r"\max \sum_{ij \in E} \frac{1 - v_i \cdot v_j}{2}, \quad \|v_i\| = 1", font_size=32, color=LAM),
            label(r"relax: \ unit \textbf{vectors} instead of signs; \\ a semidefinite program, \ solvable", font_size=21,
                  color=LAM),
            label(rf"exact cut {g['exact']}; \ rank-3 local {g['sdp3_local']:.2f}; \\ separate certified dual upper {g['sdp']:.2f}", font_size=21,
                  color=HEAD),
            label(r"round: \ a \textbf{random hyperplane} through the centre; \\ each side of it is a side of the cut",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "A geometric relaxation gives a useful route to MAX-CUT. <bookmark mark='a'/> Split vertices into "
            "two sides and maximize crossing edges, an NP-hard problem. <bookmark mark='b'/> Encode each side by "
            "a sign, so an edge contributes one minus the sign product over two. <bookmark mark='c'/> Replace "
            "signs by unit vectors; their Gram matrix gives a semidefinite relaxation. <bookmark mark='d'/> We "
            'optimize vectors locally by projected gradient. That produces a feasible primal objective, not a '
            'certified global SDP optimum. The three-dimensional sphere is a separate rank-three visualization. '
            "<bookmark mark='e'/> For this graph the exact cut is eighteen. A separate rational dual matrix "
            'certificate bounds it above; local vector values and certified upper bounds are stored separately. '
            "<bookmark mark='f'/> A random plane through the origin rounds the pictured vectors to an actual "
            'feasible cut.'
        )
        ) as vo:
            self.play(FadeIn(head))
            self.add(w)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), view.th.animate.set_value(0.4), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), view.th.animate.set_value(1.0), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), show_cut.animate.set_value(1.0), run_time=1.5)
            self.play(view.th.animate.set_value(1.8), run_time=3.0)
        w.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def alpha(self):
        g = load("gw")
        head = label(r"Where 0.878 comes from", font_size=34).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, math.pi, math.pi / 4], y_range=[0, 1.6, 0.25], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        cut = ax.plot(lambda t: t / math.pi, x_range=[0, math.pi], color=YES)
        sdp = ax.plot(lambda t: (1 - math.cos(t)) / 2, x_range=[0, math.pi], color=LAM)
        def rf(t):
            return (t / math.pi) / ((1 - math.cos(t)) / 2)
        t0 = next(t for t in np.linspace(0.05, 1.5, 2000) if rf(t) <= 1.58)
        ratio = ax.plot(rf, x_range=[t0, math.pi], color=HEAD)
        lab = VGroup(label(r"$\theta/\pi$: \ chance the edge is cut", font_size=19, color=YES),
                     label(r"$(1 - \cos\theta)/2$: \ its SDP reward", font_size=19, color=LAM),
                     label(r"their ratio", font_size=19, color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lab.next_to(ax, UP, buff=0.15).align_to(ax, LEFT).shift(RIGHT * 0.6)
        mp = Dot(ax.c2p(g["theta"], g["alpha"]), color=NO, radius=0.08)
        xl = label(r"angle $\theta$ between the two vectors", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        side = VGroup(
            label(r"two vectors at angle $\theta$ are separated \\ by a random hyperplane with probability $\theta/\pi$",
                  font_size=21, color=WHITE),
            MathTex(r"\alpha = \min_{0 < \theta \le \pi} \frac{\theta/\pi}{(1 - \cos\theta)/2} \approx " +
                    f"{g['alpha']:.4f}", font_size=30, color=HEAD),
            label(rf"attained at $\theta \approx {g['theta']:.2f}$ \ ({math.degrees(g['theta']):.0f}$^\circ$)",
                  font_size=21, color=NO),
            label('for fixed vectors: \\ $\\mathbb E[\\mathrm{cut}]\\ge\\alpha F(V)$; \\\\ globally optimal SDP vectors give $\\alpha\\,\\mathrm{OPT}$ \\\\ (or explicitly subtract optimization error)', font_size=21, color=YES),
            label(r"random assignment gives $\tfrac12$; \ nothing beat it for 20 years before 1995", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "Why does hyperplane rounding help? <bookmark mark='a'/> Vectors at angle theta are separated with "
            "probability theta over pi. <bookmark mark='b'/> Compare this probability with the edge's vector "
            'reward, one minus cosine theta over two. The ratio is at least alpha, about zero point eight seven '
            "eight. <bookmark mark='c'/> Its minimum is near one hundred thirty-four degrees, checked here by an "
            "independent scalar root solve. <bookmark mark='d'/> For any fixed vectors, expected cut is at least "
            'alpha times their own objective. To conclude alpha times the integer optimum, the theorem uses a '
            'globally optimal SDP solution, or explicitly accounts for its optimization error. Our local solver '
            "alone supplies neither premise. <bookmark mark='e'/> Independent random vertex labels give the "
            'elementary one-half guarantee. A finite average of sampled cuts estimates an expectation; it does '
            'not prove a universal bound.'
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(cut), FadeIn(lab[0]))
            vo.wait_until("b")
            self.play(Create(sdp), FadeIn(lab[1]))
            self.play(Create(ratio), FadeIn(lab[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(mp, scale=1.6), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        g = load("gw")
        r = g["rows"]
        head = label(r"Thirty random graphs of 16 vertices", font_size=32).to_edge(UP, buff=0.35)
        rows = [[r"random sides", r"$\tfrac12$", f"{np.mean([x['random_mean'] / x['exact'] for x in r]):.3f}"],
                ['local vectors, \\ 200-plane sample mean', r"local only",
                 f"{np.mean([x['gw_mean'] / x['exact'] for x in r]):.3f} \\ (worst {min(x['gw_mean'] / x['exact'] for x in r):.3f})"],
                [r"best of 200 hyperplanes", r"---", f"{np.mean([x['gw_best'] / x['exact'] for x in r]):.3f}"],
                ['certified dual upper bound', r"---", f"{np.mean([x['sdp'] / x['exact'] for x in r]):.3f}"]]
        tab = grid_table([r"", r"guarantee", r"mean ratio to the true maximum"], rows, widths=[5.0, 1.9, 5.0],
                         row_h=0.5, font_size=22, mono_cols=(), colors=[[NO] * 3, [YES] * 3, [LAM] * 3, [GREY_A] * 3])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label('projected-gradient vectors: \\ local primal objective; \\\\ separate rational dual PSD certificates give upper bounds', font_size=21, color=GREY_A),
            label(r"Khot, \ Kindler, \ Mossel and O'Donnell (2004): \ under the Unique Games Conjecture, \ "
                  r"$0.878$ is \textbf{optimal}", font_size=22, color=HEAD),
            label('H\\aa stad (2001): \\ factor $16/17+\\varepsilon$ is NP-hard for fixed $\\varepsilon>0$; \\ unless $P=NP$',
                  font_size=22, color=NO),
            label(r"the template \ (relax to geometry, \ round at random) \ now runs through approximation algorithms",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.26).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            (
            "These thirty seeded graphs have separately enumerated exact maximum cuts. <bookmark mark='a'/> The "
            'table compares two hundred valid random vertex assignments and two hundred hyperplanes per graph. '
            'It reports finite means and best observed cuts. Exact rational positive-definiteness certificates '
            'give separate dual upper bounds; the projected-gradient objectives remain local primal '
            "observations. <bookmark mark='b'/> The dated Khot-Kindler-Mossel-O'Donnell result says, under the "
            'Unique Games Conjecture, no polynomial algorithm uniformly improves alpha by a fixed positive '
            "amount. <bookmark mark='c'/> Without that conjecture, Håstad's hardness excludes a factor sixteen "
            "seventeenths plus any fixed epsilon unless P equals NP. <bookmark mark='d'/> Geometry and random "
            'rounding are the template; the certificate, optimization error and expectation model determine '
            'which guarantee actually follows.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*x)) for x in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()


    def local_bound(self):
        vectors, local = O.gw_vectors(2,[(0,1)],iters=0,seed=0)
        optimum, _ = O.maxcut_exact(2,[(0,1)])
        assert 0 < local < optimum == 1
        # lambda=(1/2,1/2); diag(lambda)-L/4=[[1/4,1/4],[1/4,1/4]].
        dual = [[Fraction(1,4)]*2 for _ in range(2)]
        assert sum([Fraction(1,2),Fraction(1,2)]) == 1
        assert dual[0][0]*dual[1][1]-dual[0][1]*dual[1][0] == 0
        head=label('A local vector objective is not an upper bound',font_size=32).to_edge(UP,buff=.35)
        left,right=LEFT*4.8,LEFT*2.3
        edge=Line(left,right,color=HEAD,stroke_width=5)
        nodes=VGroup(Dot(left,radius=.16,color=DATA),Dot(right,radius=.16,color=NO))
        graph_note=label('one edge; exact maximum cut = 1',font_size=24,color=YES).next_to(nodes,DOWN,buff=.6)
        rows=VGroup(
            label('zero gradient iterations; seed 0',font_size=24,color=GREY_A),
            MathTex(rf'F(V)={local:.6f}<1=\mathrm{{OPT}}',font_size=38,color=NO),
            label('the feasible local primal value cannot certify an upper bound',font_size=22,color=NO),
            MathTex(r'\lambda=(1/2,1/2),\quad \sum_i\lambda_i=1',font_size=32,color=YES),
            MathTex(r'z^T(\operatorname{Diag}\lambda-L/4)z=(z_1+z_2)^2/4\ge0',font_size=29,color=YES),
            label('separate dual certificate: every cut is at most 1',font_size=24,color=YES),
        ).arrange(DOWN,buff=.35).move_to(RIGHT*2.25)
        if rows.width>7.8:rows.width=7.8;rows.set_x(2.25)
        with self.voiceover("A two-vertex graph makes the certificate issue visible. Its one edge can certainly be cut. <bookmark mark='a'/> Start our seeded vector solver but allow zero gradient steps. Its feasible local objective is about zero point one three eight, below the exact cut value one. It therefore cannot be an upper bound. <bookmark mark='b'/> Independently choose both dual multipliers equal to one half. The displayed quadratic form is a square divided by four, so the dual matrix is positive semidefinite and the multipliers sum to one. <bookmark mark='c'/> That separate certificate proves every cut is at most one. A feasible cut attaining one and a valid dual upper bound of one close the gap; a local primal value alone would not.") as vo:
            self.play(FadeIn(head),Create(edge),FadeIn(nodes),FadeIn(graph_note),FadeIn(rows[0]))
            vo.wait_until('a');self.play(FadeIn(rows[1]),FadeIn(rows[2]))
            vo.wait_until('b');self.play(FadeIn(rows[3]),FadeIn(rows[4]))
            vo.wait_until('c');self.play(FadeIn(rows[5]),Indicate(edge,color=YES))
        self.wait(.3);self.clear_scene()
