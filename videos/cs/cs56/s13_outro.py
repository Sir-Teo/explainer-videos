from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Spectral Graphs and Expanders", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"x^{\mathsf T} L x = \sum_{ij} (x_i - x_j)^2", font_size=40, color=HEAD), r"energy", HEAD),
            tile(MathTex(r"\tfrac{\lambda_2}{2} \le \phi \le \sqrt{2\lambda_2}", font_size=46, color=YES),
                 r"Cheeger", YES),
            tile(MathTex(r"(1 - \tfrac{\gamma}{2})^t", font_size=54, color=DATA), r"mixing", DATA),
            tile(MathTex(r"2\sqrt{d - 1}", font_size=56, color=KERN), r"Ramanujan", KERN),
            tile(label(r"step, \ cloud, \ step", font_size=38, color=LAM), r"the zig-zag product", LAM),
            tile(MathTex(r"C = 2m\,R_{\mathrm{eff}}", font_size=50, color=NO), r"graphs as circuits", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The Laplacian, whose quadratic form is the energy of a labelling, and whose "
            "second eigenvalue says how connected a graph is. The Fiedler vector and the sweep cut, with Cheeger's "
            "inequality to guarantee them. Random walks whose mixing time is set by the spectral gap. Expanders, "
            "random and Ramanujan, and the zig-zag product that builds them explicitly. Graphs as electrical "
            "networks, where commute times are resistances, and the sparsifiers and solvers that led to maximum flow "
            "in almost linear time. One idea runs through it: a graph's eigenvalues summarize its global shape in a "
            "handful of numbers."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"semantics and fixed points", [58]),
            (r"algorithms on graphs whose nodes see only their neighbours", [59]),
            (r"the unique games conjecture on the open-problems map", [61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 58 meets fixed points again, in the meaning of programs. Part 59 runs "
            "algorithms on graphs where each node sees only its neighbourhood, and proves how far that sight must "
            "reach. And Part 61 puts this part's open problem, the unique games conjecture, on the map of what is "
            "still unknown."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"cluster", r"spectral clustering: \ embed by the bottom eigenvectors, \ then k-means"),
            (r"partition", r"METIS-style multilevel partitioning for sharding and parallel work"),
            (r"rank", r"PageRank and its relatives are random walks with a restart"),
            (r"wire", r"expander-like topologies for data-centre networks"),
            (r"solve", r"Laplacian systems with preconditioned CG or multigrid"),
        ])
        with self.voiceover(
            "In practice. Spectral clustering embeds a graph by its bottom eigenvectors and then clusters the points. "
            "Multilevel partitioners split graphs for sharding and for parallel computation. PageRank is a random "
            "walk with a restart. Data-centre networks have been built on expander-like topologies. And Laplacian "
            "systems are solved every day with preconditioned conjugate gradients and multigrid."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $x^{\mathsf T} L x = \sum_{(i,j) \in E} (x_i - x_j)^2$, \ and that the multiplicity of the "
            r"eigenvalue 0 equals the number of components.",
            r"Compute the Laplacian spectrum of the cycle $C_n$ and of the hypercube $Q_d$.",
            r"Prove the easy direction of Cheeger's inequality, \ $\lambda_2 / 2 \le \phi(G)$.",
            r"Prove the expander mixing lemma: \ $|e(S, T) - d|S||T|/n| \le \lambda \sqrt{|S||T|}$.",
            r"\textit{Build.} \ Build the zig-zag product of two graphs of your choice, \ and compare its second "
            r"eigenvalue with the RVW bound.",
            r"$\bigstar$ \textit{Research.} \ The small-set expansion hypothesis.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: construct a zig-zag product yourself and check its second eigenvalue against the bound of "
            "Reingold, Vadhan and Wigderson. The last, marked with a star, is a research problem: whether telling if "
            "small sets expand is hard."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 57, \ Learning Theory", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"PAC learning, \ and why it needs a bound", HEAD),
            (r"VC dimension and Rademacher complexity", YES),
            (r"boosting, \ margins and kernels", DATA),
            (r"why overparameterized networks generalize", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 57: learning theory. When can a machine learn from examples, how many examples does it "
            "need, and why do enormous neural networks generalize at all, when the classical theory says they should "
            "not?"
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Spielman, \ \textit{Spectral and Algebraic Graph Theory}; \ Chung, \ \textit{Spectral Graph Theory}",
             r"Hoory, \ Linial and Wigderson \ (2006); \ Vadhan, \ \textit{Pseudorandomness}"],
            [r"Fiedler \ (1973); \ Alon \ (1986); \ Sinclair and Jerrum \ (1989)",
             r"Reingold, \ Vadhan and Wigderson \ (2000); \ Reingold \ (2005); \ Spielman and Teng \ (2004)",
             r"Spielman and Srivastava \ (2008); \ Marcus, \ Spielman and Srivastava \ (2015)",
             r"Chen, \ Kyng, \ Liu, \ Peng, \ Probst Gutenberg and Sachdeva \ (2022)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
