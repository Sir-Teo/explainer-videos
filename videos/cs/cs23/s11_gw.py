from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class MaxCut(VoiceoverScene):
    def construct(self):
        self.card()
        self.sphere()
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
            label(rf"here 12 vertices: \ SDP value {g['sdp']:.2f}, \ true maximum {g['exact']}", font_size=21,
                  color=HEAD),
            label(r"round: \ a \textbf{random hyperplane} through the centre; \\ each side of it is a side of the cut",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is one of the most elegant algorithms in this course. <bookmark mark='a'/> MAX-CUT asks for a split "
            "of a graph's vertices into two sides that cuts as many edges as possible. It is NP-hard. <bookmark "
            "mark='b'/> Write each vertex's side as plus or minus one; an edge is cut when the product of its ends is "
            "minus one. <bookmark mark='c'/> Michel Goemans and David Williamson relaxed the signs to unit vectors, and "
            "rewarded each edge for how far apart its two vectors point. <bookmark mark='d'/> That is a semidefinite "
            "program, a cousin of linear programming that can be solved efficiently. The vectors of adjacent vertices "
            "spread apart over the sphere. <bookmark mark='e'/> For this graph of twelve vertices the relaxation is "
            "worth eighteen point three, a little above the true maximum of eighteen. <bookmark mark='f'/> Now cut the "
            "sphere with a random plane through its centre, and put the vertices on each side of the plane on each "
            "side of the cut."
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
            label(r"edge by edge, \ the expected cut is at least $\alpha$ times the SDP, \\ which is at least OPT: \ "
                  r"a $0.878$-approximation", font_size=21, color=YES),
            label(r"random assignment gives $\tfrac12$; \ nothing beat it for 20 years before 1995", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Why is that good? <bookmark mark='a'/> Two vectors at angle theta are separated by a random plane with "
            "probability theta over pi: the plane's direction has to fall in the wedge between them. <bookmark "
            "mark='b'/> Compare that with what the relaxation credited the edge, one minus cos theta over two. Their "
            "ratio is never less than about zero point eight seven eight. <bookmark mark='c'/> The worst case is an "
            "angle of about a hundred and thirty-four degrees. <bookmark mark='d'/> So edge by edge, the expected "
            "cut is at least zero point eight seven eight times the relaxation, which is at least the optimum. "
            "<bookmark mark='e'/> Before 1995 the best known guarantee was one half, from putting every vertex on a "
            "random side."
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
                [r"Goemans--Williamson, \ one hyperplane", rf"${g['alpha']:.3f}$",
                 f"{np.mean([x['gw_mean'] / x['exact'] for x in r]):.3f} \\ (worst {min(x['gw_mean'] / x['exact'] for x in r):.3f})"],
                [r"best of 200 hyperplanes", r"---", f"{np.mean([x['gw_best'] / x['exact'] for x in r]):.3f}"],
                [r"the SDP itself \ (an upper bound)", r"---", f"{np.mean([x['sdp'] / x['exact'] for x in r]):.3f}"]]
        tab = grid_table([r"", r"guarantee", r"mean ratio to the true maximum"], rows, widths=[5.0, 1.9, 5.0],
                         row_h=0.5, font_size=22, mono_cols=(), colors=[[NO] * 3, [YES] * 3, [LAM] * 3, [GREY_A] * 3])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"our SDP: \ unit vectors in $\mathbb{R}^k$, \ $k \approx \sqrt{2n}$, \ by projected gradient \ "
                  r"(Burer and Monteiro)", font_size=21, color=GREY_A),
            label(r"Khot, \ Kindler, \ Mossel and O'Donnell (2004): \ under the Unique Games Conjecture, \ "
                  r"$0.878$ is \textbf{optimal}", font_size=22, color=HEAD),
            label(r"H\aa stad (2001): \ beating $\tfrac{16}{17} \approx 0.941$ is NP-hard, \ unconditionally",
                  font_size=22, color=NO),
            label(r"the template \ (relax to geometry, \ round at random) \ now runs through approximation algorithms",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.26).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "We tried it on thirty random graphs, against the true maximum found by checking every split. <bookmark "
            "mark='a'/> Random sides cut about two thirds of the maximum. One random hyperplane averaged ninety-six "
            "percent, and its worst graph ninety-four, comfortably above the guarantee; the best of two hundred "
            "hyperplanes found the optimum on every graph. We solved the semidefinite program the simple way, by "
            "gradient steps on unit vectors. <bookmark mark='b'/> And the constant is no accident. Subhash Khot and "
            "colleagues showed in 2004 that if the Unique Games Conjecture holds, nobody can beat zero point eight "
            "seven eight in polynomial time. <bookmark mark='c'/> Without the conjecture, Johan Håstad proved that "
            "beating sixteen seventeenths is NP-hard. <bookmark mark='d'/> Relax to geometry, then round at random: "
            "the template now runs through the whole field."
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
