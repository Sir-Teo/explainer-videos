from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.earth()
        self.kantorovich()
        self.why_stats()
        self.taxonomy()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1781,)).to_edge(UP, buff=0.35)
        hc = history_card(1781, r"G. Monge, \ \emph{M\'emoire sur la th\'eorie des d\'eblais et des remblais}",
                          r"to the Paris Academy of Sciences: \ earth dug from one place (the \emph{d\'eblais}) must fill "
                          r"holes elsewhere (the \emph{remblais}); \ which shovelful should go where, \ so that the total "
                          r"distance carried is least?", color=TGT, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a question about moving mass at least cost", font_size=26, color=GREY_A),
            label(r"on a line: \ monotone pairing is optimal for convex difference costs", font_size=26, color=PLANC),
            label(r"two centuries later: \ a way to compare probability distributions", font_size=26, color=SRC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1781 Gaspard Monge presented a memoir to the Paris Academy of Sciences on cuttings and "
            "fillings. Earth dug from one place must fill holes in another: which shovelful should go where, so that the "
            "total distance carried is as small as possible? <bookmark mark='b'/> It is a question about moving mass at "
            "least cost. <bookmark mark='c'/> Uncrossing motivates transport geometry. On a line, monotone pairing is optimal for a convex cost of displacement, but the optimum need not be unique for plain distance. "
            "<bookmark mark='d'/> Two centuries later, the same question became one of statistics' most useful ways of "
            "comparing probability distributions."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def earth(self):
        d = load("hook")
        xs, f, g = np.asarray(d["xs"]), np.asarray(d["f"]), np.asarray(d["g"])
        src, tgt = np.asarray(d["src"]), np.asarray(d["tgt"])
        A = axes([0, 10], [-0.45, 0.45], x_length=11.0, y_length=4.6, xlabel=r"position", ylabel=r"",
                 xticks=[0, 2, 4, 6, 8, 10], center=[0, -0.1, 0])
        ax = A.ax
        def from_zero(ys, c, op):
            pts = [ax.c2p(xs[0], 0)] + [ax.c2p(a, b) for a, b in zip(xs, ys)] + [ax.c2p(xs[-1], 0)]
            return VGroup(Polygon(*pts, stroke_width=0, fill_color=c, fill_opacity=op), curve(ax, xs, ys, c, 3))
        pile = from_zero(f, SRC, 0.35)
        holes = from_zero(-g, TGT, 0.3)
        zero = Line(ax.c2p(0, 0), ax.c2p(10, 0), color=GREY_C, stroke_width=1.5)
        lab1 = label(r"the earth: \ $\mu$", font_size=24, color=SRC).move_to(ax.c2p(3, 0.47))
        lab2 = label(r"the holes: \ $\nu$", font_size=24, color=TGT).move_to(ax.c2p(7, -0.5))
        dots = VGroup(*[Dot(ax.c2p(x, 0.02), radius=0.06, color=SRC) for x in src])
        mono = VGroup(*[Dot(ax.c2p(y, -0.02), radius=0.06, color=PLANC) for y in tgt])
        arcs = VGroup(*[ArcBetweenPoints(ax.c2p(x, 0.02), ax.c2p(y, -0.02), angle=-PI / 3, stroke_width=1.5, color=PLANC, stroke_opacity=0.6)
                        for x, y in zip(src[::2], tgt[::2])])
        cross = VGroup(*[ArcBetweenPoints(ax.c2p(x, 0.02), ax.c2p(y, -0.02), angle=-PI / 3, stroke_width=1.5, color=NAIVEC2, stroke_opacity=0.6)
                         for x, y in zip(src[::2], tgt[::-1][::2])])
        side = side_groups([
            [(rf"monotone plan: \ $W_2 = {d['w2']:.2f}$", PLANC)],
            [(rf"crossing plan: \ {d['w2_cross']:.2f}", NAIVEC2)],
            [(rf"with distance as the cost: \ {d['w1']:.2f} \ vs \ {d['w1_cross']:.2f}", GREY_A)],
        ], width=5.2, pos=(3.4, 2.55, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> Monge's problem on a line. The blue pile of earth, mu, must fill the gold holes, nu, "
            f"drawn below the axis. <bookmark mark='b'/> Cut the earth into forty equal shovelfuls. <bookmark mark='c'/> "
            f"The monotone plan sends the leftmost shovelful to the leftmost hole, and so on in order: the ordering is preserved. "
            f"With the squared distance as the cost, its root mean cost is {say(d['w2'], 2)}. <bookmark mark='d'/> A crossing "
            f"plan, which sends the leftmost earth to the rightmost hole, costs {say(d['w2_cross'], 2)}. <bookmark mark='e'/> "
            f"With the plain distance as the cost, Monge's own choice, the two cost almost the same, {say(d['w1'], 2)} and "
            f"{say(d['w1_cross'], 2)}: when every shovelful moves right, any plan carries the same total distance. The cost "
            f"function matters."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), Create(pile), Create(holes), FadeIn(lab1), FadeIn(lab2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(arcs), TransformFromCopy(dots, mono), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeOut(arcs), Create(cross), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def kantorovich(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Monge's problem asks for a map: each shovelful goes to one place. That can be impossible, "
            "if a single point of earth must fill two holes. <bookmark mark='b'/> In 1942 Leonid Kantorovich relaxed it: let "
            "mass split, and look for a coupling, a joint distribution whose marginals are mu and nu. <bookmark mark='c'/> "
            "The cost is then linear in the coupling, and the problem is a linear program, Part twenty-one's subject. "
            "<bookmark mark='d'/> Kantorovich shared the 1975 economics Nobel prize with Tjalling Koopmans for the theory of "
            "optimal allocation that grew from it.",
            [(r"\text{Monge}", r":", r"\min_{T: \ T_\#\mu = \nu} \int c(x, T(x))\,d\mu", 40),
             (r"\text{Kantorovich}", r":", r"\min_{\pi \in \Pi(\mu, \nu)} \int c(x, y)\,d\pi(x, y)", 40),
             (r"\text{so}", r":", r"\text{a linear program in } \pi", 40),
             (r"1975", r":", r"\text{Nobel prize, \ with Koopmans}", 40)],
            [r"a map", r"a coupling", r"Part 21", r"optimal allocation"],
            colors=[(1, PLANC)])

    def why_stats(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why statistics cares. <bookmark mark='b'/> The optimal cost, with the cost a power of a "
            "distance, defines the Wasserstein distance between distributions: a metric that sees geometry, so two point "
            "masses a little apart are a little apart, where total variation calls them maximally different. <bookmark "
            "mark='c'/> Its optimal maps define multivariate ranks and quantiles, which the line had and the plane lacked. "
            "<bookmark mark='d'/> And its geometry makes sampling a form of optimization, and generative models a form of "
            "transport.",
            [(r"W_p(\mu, \nu)", r"=", r"\big(\min_\pi \int \|x - y\|^p\,d\pi\big)^{1/p}", 40),
             (r"\text{geometry}", r":", r"W(\delta_0, \delta_h) = |h|; \ \ \mathrm{TV} = 1", 40),
             (r"\text{maps}", r":", r"\text{ranks and quantiles in } \mathbb R^d", 40),
             (r"\text{flows}", r":", r"\text{sampling} = \text{optimization}", 40)],
            [r"a metric on laws", r"Part 43's distances", r"chapter 7", r"chapters 8--9"],
            colors=[(0, PLANC)])

    def taxonomy(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one and two: duality, the line's quantile "
            "solution, and the Wasserstein distances with their geodesics. <bookmark mark='c'/> Chapters three to five: the "
            "statistics of estimating them, the curse of dimensionality, entropic smoothing, and transport maps. "
            "<bookmark mark='d'/> Chapters six and seven: barycenters, and multivariate ranks with a distribution-free test. "
            "<bookmark mark='e'/> Chapters eight and nine: gradient flows, Langevin sampling and generative models.",
            [(r"the plan:", GREY_A),
             (r"1--2: \ duality, \ Wasserstein distances, \ geodesics", PLANC),
             (r"3--5: \ empirical rates, \ Sinkhorn, \ transport maps", ENTC),
             (r"6--7: \ barycenters, \ multivariate ranks", TGT),
             (r"8--9: \ gradient flows, \ generative models", FLOWC)])

    def upgrade(self):
        cards = [
            upgrade_card(21, r"linear programming, \ duality, \ the simplex", r"a finite, \ given problem",
                         r"chapter 1: \ the transport LP and its dual, \ as a statistic"),
            upgrade_card(60, r"Wasserstein balls as uncertainty sets", r"the distance used, \ never studied",
                         r"chapters 2--5: \ what it is, \ and how well it can be estimated"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part twenty-one solved linear programs and their duals; chapter one "
            "turns the transport program into a statistic. <bookmark mark='b'/> Part sixty used Wasserstein balls as "
            "uncertainty sets without studying the distance; chapters two to five study it, and ask how well it can be "
            "estimated from data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 61", font_size=34, color=GREY_B), label(r"Optimal Transport in Statistics", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Kantorovich duality; \ Wasserstein distances on NHANES; \ geodesics on Old Faithful",
            r"the curse of dimensionality; \ Sinkhorn; \ estimating transport maps",
            r"barycenters of blood pressure by age; \ center-outward ranks; \ a distribution-free test",
            r"Langevin as a gradient flow; \ flow matching; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 21, \ 43, \ 48, \ 51").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ot}, \ the transport flow").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-one: optimal transport in statistics. <bookmark mark='b'/> Kantorovich duality, "
            "Wasserstein distances on NHANES and geodesics on Old Faithful; the curse of dimensionality, Sinkhorn's "
            "algorithm, and estimating transport maps; barycenters of blood pressure by age, center-outward ranks and a "
            "distribution-free test; Langevin dynamics as a gradient flow, flow matching, and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
