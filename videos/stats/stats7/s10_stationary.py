from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403

GRAPH_POS = [(-5.4, 1.2), (-5.4, -1.4), (-3.4, -0.1), (-1.0, -0.1), (1.0, 1.2), (1.0, -1.4)]
PAGE_POS = [(-1.6, 1.6), (-3.4, 0.0), (-1.2, -0.6), (-3.6, -2.2), (0.8, -2.0), (2.8, -0.4), (2.4, 1.8)]


class Stationary(VoiceoverScene):
    def construct(self):
        self.card()
        self.eigen()
        self.balance()
        self.walk()
        self.pagerank()
        self.periodic()

    def card(self):
        card = chapter_card(9, r"Stationary distributions", r"Where the probability comes to rest", part=PART)
        with self.voiceover("Chapter nine. Stationary distributions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def eigen(self):
        d = load("chain")
        st_ = np.asarray(d["stationary"])
        rows = [
            cmath(r"\pi P", r"=", r"\pi", r",\qquad", r"\textstyle\sum_i \pi_i = 1", font_size=36),
            cmath(r"\pi_1", r"=", r"0.7\pi_1 + 0.3\pi_2 + 0.2\pi_3", r",\ \dots", font_size=32),
            cmath(r"\pi", r"=", rf"({st_[0]:.4f},\ {st_[1]:.4f},\ {st_[2]:.4f})", r"=", r"\big(\tfrac{19}{41},\ \tfrac{13}{41},\ "
                  r"\tfrac{9}{41}\big)", font_size=32),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"a left eigenvector of $P$ with eigenvalue 1"), why(r"mass in = mass out, \ state by state"),
                why(r"the weather chain's long-run shares, \ exactly")]
        thm = theorem_card(r"Convergence", r"a finite chain that can reach every state from every other (irreducible) and is not "
                           r"periodic has exactly one stationary $\pi$, \ and $\pi_0 P^t \to \pi$ from every start",
                           who=r"Perron (1907), \ Frobenius (1912); \ Markov (1906)", color=CHAIN, width=10.4,
                           font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The settled distribution is the one that doesn't change in a step. <bookmark mark='a'/> A row vector pi "
            "with pi times P equal to pi: a left eigenvector of the transition matrix, with eigenvalue one, scaled to "
            "add up to one. <bookmark mark='b'/> Each equation says that the mass flowing into a state equals the mass "
            "already there. <bookmark mark='c'/> For the weather chain, solving them gives nineteen forty-firsts "
            "sunny, thirteen forty-firsts cloudy, nine forty-firsts rainy. <bookmark mark='d'/> And a theorem of Oskar "
            "Perron and Georg Frobenius guarantees, for a finite chain that can get from anywhere to anywhere and "
            "doesn't cycle, that this distribution exists, is unique, and is reached from every start."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.95, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.clear_scene()

    def balance(self):
        rows = [
            cmath(r"\pi_i P_{ij}", r"=", r"\pi_j P_{ji}", r"\quad \text{for all } i, j", font_size=36),
            cmath(r"\sum_i \pi_i P_{ij}", r"=", r"\sum_i \pi_j P_{ji}", r"=", r"\pi_j", font_size=34),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"detailed balance: \ the flow from $i$ to $j$ equals the flow back"), why(r"sum over $i$: \ $\pi$ is stationary")]
        rem = fit_rows(VGroup(
            label(r"stationary: \ the total flow into each state balances; \ detailed: \ each pair of states balances", font_size=24,
                  color=GREY_A),
            label(r"a chain with detailed balance is \emph{reversible}: \ run backwards, it looks the same", font_size=24, color=CHAIN),
            label(r"the easy way to build a chain with a chosen $\pi$: \ chapter 11", font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "There's an easier condition to check. <bookmark mark='a'/> Detailed balance: for every pair of states, the "
            "flow of probability from i to j equals the flow back from j to i. <bookmark mark='b'/> Sum it over i, and "
            "the right side becomes pi j, since each row of P sums to one. So detailed balance implies stationarity. "
            "<bookmark mark='c'/> Stationarity balances the total flow into each state; detailed balance balances "
            "every pair. A chain that satisfies it is reversible: filmed and played backwards, it looks statistically "
            "the same. And it's the easy way to design a chain with any stationary distribution we want, which is "
            "exactly what chapter eleven will do."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.1, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rem], lag_ratio=0.4))
        self.clear_scene()

    def walk(self):
        d = load("chain")
        edges, deg, sq = d["edges"], np.asarray(d["deg"]), np.asarray(d["walk_stat"])
        pos = [np.array([x, y, 0]) for x, y in GRAPH_POS]
        lines = VGroup(*[Line(pos[a], pos[b], color=GREY_C, stroke_width=2.5) for a, b in edges])
        nodes = VGroup(*[VGroup(Circle(radius=0.22 + 1.4 * sq[i], color=CHAIN, stroke_width=3, fill_color=CHAIN, fill_opacity=0.25),
                                MathTex(str(int(deg[i])), font_size=24)).move_to(pos[i]) for i in range(6)])
        rows = fit_rows(VGroup(
            label(r"walk on a graph: \ step to a random neighbour", font_size=26),
            MathTex(r"P_{ij} = \frac{1}{\deg i} \ \ (j \sim i)", font_size=30),
            MathTex(r"\pi_i = \frac{\deg i}{2|E|}", font_size=34, color=EXACT),
            label(r"check: \ $\pi_i P_{ij} = \frac{1}{2|E|} = \pi_j P_{ji}$", font_size=24, color=GREY_A),
            MathTex(rf"\pi = (" + ",\\ ".join(f"{v:.3f}" for v in sq) + ")", font_size=24, color=CHAIN),
        ), 5.6, 0.3, [3.9, 0.2, 0])
        with self.voiceover(
            "Detailed balance makes some stationary distributions obvious. <bookmark mark='a'/> A random walk on a "
            "graph steps to a neighbour chosen at random; the number on each node is its degree, how many neighbours "
            "it has. <bookmark mark='b'/> Guess that the stationary chance of a node is its degree, over twice the "
            "number of edges. <bookmark mark='c'/> Check detailed balance: pi i times one over degree i is one over "
            "twice the edges, the same in both directions. So the guess is right: a random walker spends time in "
            "proportion to how connected a node is. The circles are drawn to that size."
        ) as vo:
            self.play(Create(lines), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def pagerank(self):
        d = load("chain")
        links = {int(k): v for k, v in d["links"].items()}
        pr = np.asarray(d["pagerank"])
        pos = [np.array([x, y, 0]) for x, y in PAGE_POS]
        arrows = VGroup()
        for i, outs in links.items():
            for j in outs:
                v = pos[j] - pos[i]
                u = v / np.linalg.norm(v)
                arrows.add(Arrow(pos[i] + u * 0.45, pos[j] - u * 0.45, buff=0, color=GREY_C, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.1))
        nodes = VGroup(*[Circle(radius=0.35, color=S.EST, stroke_width=3, fill_color=S.EST, fill_opacity=0.2).move_to(p) for p in pos])
        big = VGroup(*[Circle(radius=0.25 + 1.6 * pr[i], color=S.EST, stroke_width=3, fill_color=S.EST, fill_opacity=0.35).move_to(pos[i])
                       for i in range(7)])
        labs = VGroup(*[MathTex(f"{pr[i]:.2f}", font_size=22).move_to(pos[i]) for i in range(7)])
        grp = VGroup(arrows, nodes, big, labs).shift(LEFT * 1.6)
        rows = fit_rows(VGroup(
            label(r"the random surfer: \ follow a random link with chance 0.85, \ else jump to any page", font_size=22),
            MathTex(r"G = 0.85\, L + 0.15\, \tfrac{1}{n}\mathbf 1\mathbf 1^\top", font_size=28),
            MathTex(r"\text{PageRank} = \text{the stationary } \pi \text{ of } G", font_size=28, color=S.EST),
            label(r"power iteration: \ $\pi \leftarrow \pi G$, \ 40 steps", font_size=22, color=GREY_A),
            label(r"the jump makes the chain irreducible and aperiodic: \ Perron--Frobenius applies", font_size=22, color=GREY_A),
        ), 4.8, 0.28, [4.4, 0.3, 0])
        hc = note(r"S. Brin \& L. Page, \ ``The anatomy of a large-scale hypertextual web search engine'' (1998)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The most valuable stationary distribution ever computed belonged to a chain on the web. "
            "<bookmark mark='a'/> Pages link to pages. Imagine a surfer who, at each step, follows a random link from "
            "the current page with chance point eight five, and otherwise jumps to a page chosen at random. "
            "<bookmark mark='b'/> That's a Markov chain on the pages, and its stationary distribution is PageRank: the "
            "long-run share of time the surfer spends on each page. Sergey Brin and Larry Page built a search engine "
            "on it in 1998. The random jump guarantees the conditions of the convergence theorem. "
            "<bookmark mark='c'/> On this little web of seven pages, power iteration converges in a few dozen steps, "
            "and the page that many others link to, with a third of the surfer's time, comes out on top."
        ) as vo:
            self.play(FadeIn(nodes), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(Transform(nodes, big), FadeIn(labs), FadeIn(rows[3:]))
        self.clear_scene()

    def periodic(self):
        A = axes([0, 10], [0, 1.05], x_length=6.0, y_length=3.2, xlabel=r"step $t$", ylabel=r"$P(X_t = \text{left})$",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1], center=[-2.8, -0.8, 0])
        ax = A.ax
        vals = [1 if t % 2 == 0 else 0 for t in range(11)]
        pts = VGroup(*[Dot(ax.c2p(t, v), radius=0.08, color=BAD) for t, v in enumerate(vals)])
        ln = polyline(ax, np.arange(11), vals, BAD, 2)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(10, 0.5), color=EXACT, stroke_width=2)
        mat = MathTex(r"P = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}", font_size=34).move_to([3.6, 1.6, 0])
        rows = fit_rows(VGroup(label(r"$\pi = (\tfrac12, \tfrac12)$ is stationary", font_size=24, color=EXACT),
                               label(r"but from a fixed start the chain alternates for ever", font_size=24, color=BAD),
                               label(r"periodic: \ returns only at even times", font_size=22, color=GREY_A),
                               label(r"the cure: \ a little laziness, \ $P' = \tfrac12(I + P)$", font_size=22, color=S.ACCENT)),
                        5.2, 0.25, [3.8, -0.6, 0])
        with self.voiceover(
            "One condition in that theorem is easy to overlook. <bookmark mark='a'/> A chain on two states that always "
            "switches. Half and half is stationary. <bookmark mark='b'/> But start on the left, and the chance of "
            "being on the left goes one, zero, one, zero, for ever. It never converges, because the chain is "
            "periodic: it can only return at even times. <bookmark mark='c'/> The cure is a little laziness: stay put "
            "with chance a half. Every chain used in practice is built to be aperiodic."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(half), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
