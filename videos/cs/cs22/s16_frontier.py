from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.exact()
        self.threesum()
        self.neighbours()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ exactness, \ 3SUM \ and nearest neighbours",
                            r"What can geometry still not do fast, \ or right?", lit=(1995, 2015),
                            extra=((1995, r"Gajentaan--Overmars"), (2015, r"Andoni--Razenshteyn")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: exactness, three-sum, and nearest neighbours."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def exact(self):
        d = load("frontier")
        head = label(r"Exact geometric computation", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('exact predicates + correct invariants, constructions and tie rules: \\ robust combinatorics', font_size=22, color=WHITE),
            label(rf"the price, \ on nearly collinear points: \ {d['float_ns']:.0f} ns in floating point, \ "
                  rf"{d['exact_ns'] / 1000:.0f} $\mu$s in rationals, \ {d['exact_ns'] / d['float_ns']:.0f}$\times$",
                  font_size=22, color=NO),
            label(r"adaptive filters \ (chapter 1) \ pay it only where needed: \ CGAL, \ LEDA, \ Shewchuk's "
                  r"\texttt{Triangle}", font_size=22, color=YES),
            label(r"degenerate inputs: \ simulate a symbolic perturbation \ (Edelsbrunner and M\"ucke, 1990)",
                  font_size=22, color=LAM),
            label(r"still hard: \ \textbf{constructions}. \ An intersection point needs more bits than its inputs, \\ "
                  r"and chained constructions explode; \ snap rounding \ (Hobby, 1999) \ trades exactness for size",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Robustness requires more than one exact determinant. <bookmark mark='a'/> Exact predicates support correct combinatorial decisions when the algorithm's invariants, constructions and degeneracy conventions are also correct. Our underflow witness showed why a filter must certify its arithmetic conditions. <bookmark mark='b'/> The displayed rational-to-float timing ratio comes from this Python implementation on these near-collinear inputs. It is not a universal price of exactness. Raw repetitions and matching outputs are retained. <bookmark mark='c'/> Adaptive filters use a cheap certified case and fall back when necessary. Our fallback uses Python rationals; Shewchuk's expansion arithmetic is a different implementation. <bookmark mark='d'/> Symbolic perturbation consistently selects a combinatorial convention for degenerate inputs. It does not repair already-rounded constructed coordinates. <bookmark mark='e'/> Intersections can increase coordinate complexity, especially through repeated constructions. Exact constructions, interval methods and snap-rounding techniques make different precision and topology tradeoffs. We do not infer a general three-dimensional impossibility or open problem from this example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                if ln is not lines[0]:
                    self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def threesum(self):
        d = load("frontier")
        head = label(r"3SUM: \ the quadratic wall of the plane", font_size=34).to_edge(UP, buff=0.35)
        nums = d["nums"]
        O = np.array([-3.6, -0.5, 0])
        sx, sy = 0.052, 1.05e-5

        def P(x, y):
            return O + np.array([x * sx, y * sy, 0])
        cub = ParametricFunction(lambda t: P(t, t ** 3), t_range=[-64, 64], color=GREY_D, stroke_width=1.5)
        axes = VGroup(Line(P(-66, 0), P(66, 0), color=GREY_D, stroke_width=1),
                      Line(P(0, -2.6e5), P(0, 2.6e5), color=GREY_D, stroke_width=1))
        pts = VGroup(*[Dot(P(a_, a_ ** 3), radius=0.06, color=HEAD) for a_ in nums])
        tl = VGroup()
        for (a_, b_, c_), col in zip(d["triples"], (YES, LAM)):
            xs = sorted((a_, b_, c_))
            m = (xs[2] ** 3 - xs[0] ** 3) / (xs[2] - xs[0])
            k = xs[0] ** 3 - m * xs[0]
            lo, hi = xs[0] - 6, xs[2] + 6
            tl.add(VGroup(Line(P(lo, m * lo + k), P(hi, m * hi + k), color=col, stroke_width=2.5),
                          *[Dot(P(x, x ** 3), radius=0.09, color=col) for x in xs]))
        cap = label(r"the 14 numbers, \ lifted to $(a, a^3)$; \\ the axes are scaled differently, \ which keeps lines "
                    r"straight", font_size=18, color=GREY_A).next_to(axes, DOWN, buff=0.15)
        trip = r"; \ ".join(rf"${a_} + {b_} + {c_} = 0$".replace("+ -", "- ") for a_, b_, c_ in d["triples"])
        lines = VGroup(
            label(r"3SUM: \ do three of $n$ numbers sum to zero? \\ $O(n^2)$ is easy", font_size=22, color=WHITE),
            MathTex('\\begin{gathered}(a-b)(b-c)(c-a)\\ne0:\\\\a+b+c=0\\iff(a,a^3),(b,b^3),(c,c^3)\\text{ collinear}\\end{gathered}', font_size=28, color=LAM),
            label(rf"our 14 numbers: \ {trip}; \\ and exactly {len(d['collinear'])} collinear triples", font_size=21,
                  color=YES),
            label(r"Gajentaan and Overmars (1995): \ collinearity, \\ covering by strips, \ motion planning among "
                  r"segments, \\ \dots\ are all \textbf{3SUM-hard}", font_size=21, color=HEAD),
            label('selected real-RAM results: Gr\\o nlund--Pettie (2014), Chan (2018); \\\\ truly subquadratic 3SUM is a model-dependent conjecture', font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        if lines.width > 6.6:
            lines.width = 6.6
            lines.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Three-sum asks whether three distinct input positions sum to zero. We use distinct numerical values for this geometric reduction. <bookmark mark='a'/> Sorting and two pointers give a quadratic algorithm in the arithmetic model. <bookmark mark='b'/> Map each value a to a, a cubed. For distinct a, b and c, the collinearity determinant factors into pairwise differences times a plus b plus c. <bookmark mark='c'/> Our fourteen values are distinct, so the factorization applies. <bookmark mark='d'/> Exhaustively checking all triples finds the same two zero sums and two collinear triples. <bookmark mark='e'/> Gajentaan and Overmars developed reductions connecting three-sum to families of geometric decision problems. Those are conditional hardness relationships. <bookmark mark='f'/> The cited 2014 and 2018 real-RAM results improve logarithmic factors. A conjecture excluding n to the two minus epsilon algorithms requires a specified model and number domain; it is not a proved lower bound or a statement about every restricted integer instance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), Create(cub))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in pts], lag_ratio=0.1), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]), LaggedStart(*[Create(t) for t in tl], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
            vo.wait_until("f")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def neighbours(self):
        head = label(r"Nearest neighbours: \ what is possible", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('exact high-dimensional search: \\ lower bounds depend on metric, dimension and cell-probe parameters', font_size=22, color=NO),
            label('Euclidean $c>1$ near-neighbour hashing: \\ data-independent exponent approaches $1/c^2$', font_size=22,
                  color=LAM),
            label('Andoni--Razenshteyn (2015): $\\rho=1/(2c^2-1)$; \\\\ query $O(dn^{\\rho+o(1)})$, space $O(n^{1+\\rho+o(1)}+dn)$', font_size=22, color=YES),
            label('Indyk--Xu (2023): \\ hard instances for HNSW, NSG and fast-preprocessing DiskANN', font_size=22, color=HEAD),
            label('the same paper: \\ low intrinsic dimension guarantees for slow-preprocessing DiskANN',
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Approximate near-neighbour theory needs a precise problem. <bookmark mark='a'/> Exact-search lower bounds depend on dimension, metric, storage and the cell-probe model; they do not prohibit every small fast index on structured data. <bookmark mark='b'/> For the randomized Euclidean near-neighbour task at a chosen radius, with constant success probability and approximation c greater than one, data-independent hashing has an exponent approaching one over c squared under its standard asymptotic assumptions. <bookmark mark='c'/> Andoni and Razenshteyn's 2015 data-dependent scheme attains rho equal to one over two c squared minus one, with dimension and space factors shown here. Its optimality comparison concerns a hashing model, not every possible index. <bookmark mark='d'/> Indyk and Xu's 2023 paper already gives hard instances for HNSW, NSG and fast-preprocessing DiskANN. Our teaching experiment does not establish that graphs beat all hashing methods. <bookmark mark='e'/> The paper also proves low-intrinsic-dimension guarantees for slow-preprocessing DiskANN, a distinct construction. An algorithm name alone does not transfer a theorem between those variants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                if ln is not lines[0]:
                    self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label('Selected research results and model questions', font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label('3SUM: \\ what follows from a stated real-RAM conjecture?', font_size=24,
                  color=NO),
            label('Chan--Zheng (2022): \\ $O(n^{4/3})$ planar incidence counting; \\\\ older bounds included a $2^{O(\\log^*n)}$ factor', font_size=24, color=LAM),
            label('reproduce a published graph hard instance; \\ specify rules before proving a routing bound', font_size=24,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem takes the third", font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here are three research exercises with a dated starting point. <bookmark mark='a'/> For three-sum, write down the computational model before claiming a conditional barrier. <bookmark mark='b'/> For planar point-line incidences, Chan and Zheng in 2022 obtained an n to the four thirds counting algorithm, removing an extra iterated-logarithm factor from earlier bounds. Model-specific lower bounds do not prove unrestricted optimality. <bookmark mark='c'/> For graph search, published hard instances already exist. Reproduce one, specify the construction and query rules, then test what a proposed change actually guarantees. <bookmark mark='d'/> The starred exercise follows that last route. It is a reproducible research extension, not a claim that nobody has constructed a bad input."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs[0]))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                if q is not qs[0]:
                    self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
