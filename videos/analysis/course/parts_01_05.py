"""Principles of Mathematical Analysis, and the Lebesgue integral (Parts 1-5)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="covergame",
        question="What is a real number, and what must a set be like for every infinite process inside it to land somewhere?",
        story="In 1807 Fourier claims that a sawtooth is a sum of sines, and Lagrange objects: the part opens with the "
              "questions that claim raised about limits, functions and numbers. The rational line is dense and still "
              "full of holes; Rudin's map p to (2p + 2)/(p + 2) shows that the rationals below the square root of 2 "
              "have no largest element. Dedekind's cuts fill the holes, and the least-upper-bound property gives the "
              "Archimedean property, decimals, nested intervals and the bisection engine. Cantor's zigzag and "
              "diagonal separate the countable rationals from the uncountable reals. Then the part turns from "
              "numbers to space: metric spaces, open and closed sets, and compactness as a game of open covers, "
              "which Heine-Borel wins on closed bounded sets by bisection and loses on (0, 1]. The Cantor set and "
              "the connected subsets of the line follow, and the part ends with a warning: in C[0, 1] the closed "
              "unit ball is closed and bounded but not compact.",
        handoff="Completeness becomes the convergence of Cauchy sequences in Part 2, and the rational ruler returns "
                "there as Thomae's function. The Cantor set returns as an integrator in Part 3 and as a null set in "
                "Part 5; what replaces Heine-Borel in a function space is Arzelà-Ascoli in Part 3 and Riesz's "
                "theorem in Part 8.",
        outside="Calculus, and some practice in reading and writing proofs (sets, functions, induction, proof by contradiction).",
        objectives={
            "U": ["Prove that no rational has square 2 and that the rationals with square below 2 have no largest "
                  "element, using the map p to (2p + 2)/(p + 2).",
                  "Decide whether a given subset of the line or the plane is open, closed, bounded, compact or "
                  "connected, and justify the answer from the definitions.",
                  "Run Cantor's diagonal argument and explain why it shows the reals are uncountable."],
            "M": ["Construct the real numbers by Dedekind cuts and prove that the supremum of a bounded set of cuts "
                  "is their union.",
                  "Prove Heine-Borel by bisection and point to the step that fails on (0, 1]."],
            "D": ["Prove that a nonempty perfect set in Euclidean space is uncountable, and apply it to the Cantor set.",
                  "Show that the closed unit ball of C[0, 1] is not compact by exhibiting functions pairwise at sup "
                  "distance 1."],
            "I": ["Implement bisection in exact arithmetic and state the error after k steps.",
                  "Compute a sup distance between two functions numerically and say which metric a given "
                  "approximation problem is using."],
        },
        results=[
            ("Rudin's hop (1.1)", r"q=\frac{2p+2}{p+2}\ \Longrightarrow\ q^2-2=\frac{2(p^2-2)}{(p+2)^2},\qquad q-p=\frac{2-p^2}{p+2}"),
            ("The least-upper-bound property", r"\emptyset\ne E\subset\mathbb{R}\ \text{bounded above}\ \Longrightarrow\ \sup E\ \text{exists in}\ \mathbb{R}"),
            ("Counting", r"\mathbb{Q}\ \text{is countable},\qquad \mathbb{R}\ \text{is uncountable}"),
            ("Cauchy-Schwarz and the plane's metrics", r"|x\cdot y|\le |x|\,|y|,\qquad d_\infty\le d_2\le d_1\le 2\,d_\infty"),
            ("Heine-Borel", r"E\subset\mathbb{R}^k\ \text{is compact}\iff E\ \text{is closed and bounded}"),
            ("The tents in C[0, 1]", r"\|f_m-f_n\|_\infty=1\ \ (m\ne n)\ \Longrightarrow\ \{f:\|f\|_\infty\le 1\}\ \text{is not compact}"),
        ],
        U=(0, 1, 3, 4, 5, 6, 7, 8), D=(11,),
    ),
    Part(
        n=2, level="U", widget="greedyrearrange", prereq=(1,),
        question="When does an infinite process settle on a value, and can the order of the terms change that value?",
        story="The part opens with one series, 1 - 1/2 + 1/3 - ..., which sums to ln 2 in its natural order and, "
              "reordered by a greedy rule, to pi, to -1 or to infinity. To explain that, limits are built as a game: "
              "epsilon moves first, then N. Cauchy sequences let convergence be checked without knowing the limit, "
              "and upper and lower limits record the high- and low-water marks of a tail. Series get the comparison, "
              "condensation, root and ratio tests, the number e with its irrationality, power series, summation by "
              "parts, and Riemann's rearrangement theorem, proved by the opening's algorithm. The same game with "
              "delta defines continuity; compactness then gives extreme values and uniform continuity, and "
              "connectedness gives intermediate values. The derivative is the limit seen by zooming in, and the mean "
              "value theorem, L'Hôpital's rule and Taylor's theorem follow. The part ends with exp(-1/x²), smooth "
              "but not the sum of its Taylor series, and with the mean value inequality for vector-valued functions.",
        handoff="Rudin's grid m/(m + n) becomes Part 3's main problem, the swap of two limits, and the sawtooth "
                "series returns there as a Fourier series. The nowhere-differentiable function is proved in Part 3, "
                "completeness drives the contraction principle in Part 4, and the fact that no function is "
                "continuous exactly at the rationals waits for Baire's theorem in Part 8.",
        outside="Calculus: derivatives, the logarithm and the geometric series as computations.",
        objectives={
            "U": ["Play the epsilon-N and epsilon-delta games: given epsilon, produce an N or a delta and prove it works.",
                  "Decide the convergence of a series by comparison, condensation, the root test or the ratio test.",
                  "State and use the extreme value, intermediate value and mean value theorems, and give an example "
                  "showing each hypothesis is needed."],
            "M": ["Prove that Cauchy sequences converge in Euclidean space, and that a continuous function on a "
                  "compact set is uniformly continuous.",
                  "Compute a radius of convergence from the upper limit of the n-th roots, and prove Taylor's "
                  "theorem with Lagrange's remainder."],
            "D": ["Prove Riemann's rearrangement theorem for prescribed upper and lower limits of the partial sums.",
                  "Prove Dirichlet's test by summation by parts, and Mertens's theorem, with the example showing "
                  "that the Cauchy product can diverge without absolute convergence."],
            "I": ["Bound the error of a truncated series before computing it, as for e with the tail bound 1/(n! n).",
                  "Explain why the order of summation matters in a conditionally convergent sum and not in an "
                  "absolutely convergent one."],
        },
        results=[
            ("The Cauchy criterion", r"(p_n)\subset\mathbb{R}^k\ \text{converges}\iff \forall\varepsilon>0\ \exists N:\ |p_n-p_m|<\varepsilon\ \ (n,m\ge N)"),
            ("The number e", r"e=\sum_{n=0}^{\infty}\frac{1}{n!}=\lim_{n\to\infty}\Bigl(1+\frac1n\Bigr)^{n},\qquad 0<e-s_n<\frac{1}{n!\,n}"),
            ("Radius of convergence", r"\sum c_n z^n\ \text{converges for}\ |z|<R,\ \text{diverges for}\ |z|>R,\qquad \frac1R=\limsup_{n\to\infty}|c_n|^{1/n}"),
            ("Riemann's rearrangement theorem", r"\sum a_n\ \text{conditionally convergent},\ \alpha\le\beta\ \Longrightarrow\ \exists\ \text{a rearrangement with}\ \liminf s_n'=\alpha,\ \limsup s_n'=\beta"),
            ("Pringsheim's ratio for the alternating harmonic series", r"\frac{\#\text{positive terms}}{\#\text{negative terms}}\to e^{2(T-\ln 2)}\ \text{when the greedy rearrangement sums to}\ T"),
            ("Taylor's theorem", r"f(\beta)=\sum_{k=0}^{n-1}\frac{f^{(k)}(\alpha)}{k!}(\beta-\alpha)^k+\frac{f^{(n)}(\xi)}{n!}(\beta-\alpha)^n\ \text{for some}\ \xi\ \text{between}\ \alpha\ \text{and}\ \beta"),
        ],
        U=(0, 1, 2, 4, 5, 9, 10, 11, 12, 13, 14), D=(7, 8),
    ),
    Part(
        n=3, level="U", widget="gibbsfejer", prereq=(1, 2),
        question="When may two limits be swapped: the limit of a sequence of functions with an integral, a derivative, or continuity itself?",
        story="The part opens on Rudin's main problem with three failed swaps: x to the n loses continuity, a bump "
              "keeps its limit but not its integral, and sin(nx)/sqrt(n) converges while its slopes blow up. "
              "Riemann's integral is built from upper and lower sums, tested on continuous, monotone, Dirichlet's "
              "and Thomae's functions, and stretched into the Stieltjes integral, where the Cantor function "
              "integrates x to 1/2. Uniform convergence is the first answer to the main problem: uniform limits keep "
              "continuity and integrals, and make C(X) a complete metric space. In that space the part finds a "
              "continuous function with no derivative anywhere, replaces Heine-Borel by Arzelà-Ascoli, and proves "
              "that polynomials are dense, by Weierstrass's kernel and then by Stone-Weierstrass. Power series give "
              "exp, cos, sin and pi. The part ends where the series began, with Fourier series: the partial sum is "
              "the best mean-square approximation, Parseval accounts for all the energy, the sum of 1/n² is pi²/6, "
              "and the sawtooth's overshoot never drops below 8.95% of the jump.",
        handoff="C[a, b] with the sup distance is the complete space in which Picard solves differential equations "
                "in Part 4. Dirichlet's function and term-by-term integration of the sawtooth are settled by "
                "Lebesgue's integral in Part 5, and Bessel, Parseval and best approximation become the geometry of "
                "Hilbert space in Part 6.",
        outside="Calculus, including integration by parts and the trigonometric identities.",
        objectives={
            "U": ["Compute upper and lower sums and use the criterion U - L < epsilon to prove a function integrable.",
                  "Tell pointwise from uniform convergence by computing the sup of |f_n - f|, and apply the M-test.",
                  "Give the three examples in which a limit fails to pass through continuity, an integral and a derivative."],
            "M": ["Prove that a uniform limit of continuous functions is continuous and that integrals pass "
                  "through uniform limits.",
                  "Compute Fourier coefficients, and prove Bessel's inequality and the best-approximation property "
                  "of the partial sums."],
            "D": ["Prove Arzelà-Ascoli by the diagonal process, and Stone-Weierstrass in its four steps, with the "
                  "example of the conjugate function on the circle for complex algebras.",
                  "Prove that Rudin's function of Theorem 7.18 is continuous and nowhere differentiable."],
            "I": ["Approximate a continuous function by Bernstein polynomials or Fejér means and measure the sup error.",
                  "Predict the Gibbs overshoot at a jump, and say which sense of convergence (sup, mean-square) a "
                  "truncated Fourier series can be trusted in."],
        },
        results=[
            ("Riemann's criterion", r"f\in\mathscr{R}(\alpha)\iff \forall\varepsilon>0\ \exists P:\ U(P,f,\alpha)-L(P,f,\alpha)<\varepsilon"),
            ("Integrals pass through uniform limits", r"f_n\in\mathscr{R}\ \text{on}\ [a,b],\ \sup_{[a,b]}|f_n-f|\to 0\ \Longrightarrow\ \int_a^b f\,dx=\lim_{n\to\infty}\int_a^b f_n\,dx"),
            ("Arzelà-Ascoli", r"K\ \text{compact},\ (f_n)\subset C(K)\ \text{pointwise bounded and equicontinuous}\ \Longrightarrow\ \text{a subsequence converges uniformly}"),
            ("Stone-Weierstrass", r"\mathscr{A}\subset C(K;\mathbb{R})\ \text{an algebra that separates points and vanishes nowhere}\ \Longrightarrow\ \overline{\mathscr{A}}=C(K;\mathbb{R})"),
            ("Parseval", r"f(x)\sim\sum_{n=-\infty}^{\infty}c_n e^{inx}\ \Longrightarrow\ \frac{1}{2\pi}\int_{-\pi}^{\pi}|f(x)|^2\,dx=\sum_{n=-\infty}^{\infty}|c_n|^2"),
            ("Gibbs's overshoot, as a share of the jump", r"\frac{\operatorname{Si}(\pi)}{\pi}-\frac12=0.0895\ldots,\qquad \operatorname{Si}(\pi)=\int_0^{\pi}\frac{\sin t}{t}\,dt"),
        ],
        U=(0, 1, 2, 4, 5, 6, 7), D=(8, 10, 12), I=(11, 14, 15),
    ),
    Part(
        n=4, level="U", widget="cobwebcontract", prereq=(1, 2, 3),
        question="What is the derivative of a map of several variables, and how does one idea, a map that shrinks distances, solve equation after equation?",
        story="The part opens with Newton's method on a circle and a hyperbola, and with the picture behind it: a map "
              "of the plane that shrinks every distance collapses the plane onto its one fixed point. Linear maps "
              "get a norm, the largest stretch, and the invertible ones form an open set, by a geometric series of "
              "matrices. The derivative becomes the linear map seen when a contour map is zoomed until its level "
              "lines are straight and evenly spaced. Two museum functions show that partial derivatives, and even "
              "directional derivatives in every direction, do not make a derivative; continuous partials do. Then "
              "the contraction principle is proved and used: for cos x = x, for Picard's solution of differential "
              "equations in C[0, h], and for the inverse and implicit function theorems, each built from one "
              "contraction. The part turns to two more swaps, mixed partials that disagree and differentiation "
              "under the integral sign, and ends with a tour, stated and checked but not proved, of the change of "
              "variables formula and Stokes' theorem.",
        handoff="The geometric series for an inverse returns in Part 10, where it runs the theory of the spectrum. "
                "The angle form whose integral detects a hole previews the winding numbers of Part 7, and the "
                "ledger's unanswered question about Fourier series waits for the integral of Part 5.",
        outside="Linear algebra: matrices as linear maps, determinants and inverses.",
        objectives={
            "U": ["Compute a Jacobian matrix and use it as the best linear approximation of a map near a point.",
                  "Show by example that the existence of partial derivatives does not imply differentiability, "
                  "or even continuity.",
                  "Iterate a contraction and bound the distance to its fixed point before computing it."],
            "M": ["Prove the contraction principle, and prove that continuous partial derivatives make a function "
                  "continuously differentiable.",
                  "Derive the inverse function theorem from the contraction x + A^{-1}(y - f(x)), and the implicit "
                  "function theorem from the inverse function theorem."],
            "D": ["Prove that mixed partials agree when one of them is continuous, and analyse the function whose "
                  "mixed partials at the origin are -1 and 1.",
                  "State exactly where completeness and the Lipschitz condition enter Picard's theorem, with the "
                  "equation y' = 2 sqrt(y) as the example of lost uniqueness."],
            "I": ["Solve an initial value problem by Picard iteration and compare with a numerical integrator.",
                  "Explain why Newton's method doubles the number of correct digits near a simple root, and check "
                  "an area by a line integral around its boundary."],
        },
        results=[
            ("Invertible maps form an open set (9.8)", r"\|B-A\|\,\|A^{-1}\|<1\ \Longrightarrow\ B\ \text{is invertible},\qquad \|BA\|\le\|B\|\,\|A\|"),
            ("The derivative is a linear map", r"\lim_{h\to 0}\frac{|f(x+h)-f(x)-Ah|}{|h|}=0,\qquad A=f'(x)"),
            ("The contraction principle (9.23)", r"d(\varphi(x),\varphi(y))\le c\,d(x,y),\ c<1,\ X\ \text{complete}\ \Longrightarrow\ \text{exactly one}\ x^*=\varphi(x^*),\quad d(x_n,x^*)\le\frac{c^n}{1-c}\,d(x_1,x_0)"),
            ("The inverse function theorem (9.24)", r"f\in\mathscr{C}^1,\ f'(a)\ \text{invertible}\ \Longrightarrow\ f\ \text{has a local}\ \mathscr{C}^1\ \text{inverse}\ g,\qquad g'(f(x))=f'(x)^{-1}"),
            ("The implicit function theorem, one variable each", r"f(a,b)=0,\ \frac{\partial f}{\partial y}(a,b)\ne 0\ \Longrightarrow\ y=g(x)\ \text{near}\ a,\qquad g'(x)=-\frac{\partial f/\partial x}{\partial f/\partial y}"),
            ("Differentiating under the integral (9.42)", r"\varphi,\ \frac{\partial\varphi}{\partial t}\ \text{continuous on}\ [a,b]\times[c,d]\ \Longrightarrow\ \frac{d}{dt}\int_a^b\varphi(x,t)\,dx=\int_a^b\frac{\partial\varphi}{\partial t}(x,t)\,dx"),
        ],
        U=(0, 1, 2, 3, 4), D=(8,), I=(5, 9),
    ),
    Part(
        n=5, level="M", widget="masslid", prereq=(1, 2, 3),
        question="When may a limit pass through an integral if the convergence is not uniform?",
        story="The part opens with powers of cos(m! pi x), continuous functions whose double limit is Dirichlet's "
              "function, which has no Riemann integral, and with three sequences of integral 1 that go to zero at "
              "every point: mass escapes by growing tall, sliding away or spreading thin. Lebesgue's answer starts "
              "with length: cover a set by countably many intervals as cheaply as possible. The rationals and the "
              "Cantor set get measure zero, a fat Cantor set gets measure 1/2 without containing an interval, and "
              "Vitali's set gets no length at all, so the theory keeps to a sigma-algebra of measurable sets. The "
              "integral is a supremum over simple functions, and three limit theorems govern it: monotone "
              "convergence, Fatou's lemma, and dominated convergence, which needs only a lid, one integrable "
              "function above the whole sequence. Riesz's representation theorem then builds Lebesgue measure from "
              "the Riemann integral, Lusin shows measurable functions are nearly continuous, and Fubini allows "
              "either order of integration when the absolute value is integrable. The part ends by integrating the "
              "sawtooth series term by term, with the constant 2 as the lid.",
        handoff="With Lebesgue's integral the spaces of p-th power integrable functions are complete: that theorem "
                "and the geometry of the case p = 2 are Part 6, which also shows that a sequence converging in area "
                "has a subsequence converging at almost every point and uses the density of continuous functions "
                "with compact support.",
        outside="Parts 1 to 3, or a first course in real analysis: compactness, uniform convergence, the Riemann integral.",
        objectives={
            "U": ["Show that a countable set and the Cantor set have outer measure zero by exhibiting the covers.",
                  "Give three sequences of integral 1 that converge to zero at every point, and say how the mass "
                  "escapes in each."],
            "M": ["Prove the monotone convergence theorem, deduce Fatou's lemma, and deduce dominated convergence "
                  "from Fatou applied to 2g - |f_n - f|.",
                  "Justify a swap of limit and integral, or of two integrals, by naming the lid or checking that "
                  "the absolute value is integrable.",
                  "State Lebesgue's criterion for Riemann integrability and apply it to Thomae's and Dirichlet's functions."],
            "D": ["Construct Vitali's set and prove it cannot be given a length that is countably additive and "
                  "rotation invariant.",
                  "Outline the proof of the Riesz representation theorem, and prove Egorov's and Lusin's theorems."],
            "I": ["Recognise a conditionally convergent integral such as that of sin x / x, which is an improper "
                  "Riemann integral but not a Lebesgue integral.",
                  "Bound a convolution by the product of the two L1 norms, and compute an integral from its level "
                  "sets by the layer cake formula."],
        },
        results=[
            ("Outer measure", r"m^*(E)=\inf\Bigl\{\sum_{k=1}^{\infty}\ell(I_k):\ E\subset\bigcup_{k=1}^{\infty}I_k,\ I_k\ \text{intervals}\Bigr\}"),
            ("Monotone convergence", r"0\le f_1\le f_2\le\cdots,\ f_n\to f\ \Longrightarrow\ \int f_n\,d\mu\to\int f\,d\mu"),
            ("Fatou's lemma", r"f_n\ge 0\ \Longrightarrow\ \int\liminf_{n\to\infty}f_n\,d\mu\le\liminf_{n\to\infty}\int f_n\,d\mu"),
            ("Dominated convergence", r"f_n\to f,\ |f_n|\le g,\ \int g\,d\mu<\infty\ \Longrightarrow\ \int|f_n-f|\,d\mu\to 0"),
            ("Riesz representation", r"\Lambda\ \text{positive and linear on}\ C_c(X)\ \Longrightarrow\ \Lambda f=\int_X f\,d\mu\ \text{for exactly one regular measure}\ \mu"),
            ("Fubini, and the norm of a convolution", r"\iint|f|<\infty\ \Longrightarrow\ \int\!\!\int f\,dx\,dy=\int\!\!\int f\,dy\,dx,\qquad \|f*g\|_1\le\|f\|_1\,\|g\|_1"),
        ],
        U=(0, 1), D=(2, 8, 10), I=(12,),
    ),
]
