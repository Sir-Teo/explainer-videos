"""Rudin's graduate books: L^p and Hilbert space, complex analysis, Banach spaces, distributions, spectra (Parts 6-10)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=6, level="M", widget="pnormball", prereq=(3, 5),
        question="Which distance between functions is the right one, and why is the square-integral distance special?",
        story="The part opens with three ways to measure a vector, the diamond, the circle and the square, and with "
              "continuous ramps that form a Cauchy sequence in the area distance and close in on a step that is not "
              "continuous: the hole that L^1 fills. Jensen's inequality and Young's two areas give Hoelder and "
              "Minkowski, so the p-norms are distances, and Riesz and Fischer's summable steps, run on the same "
              "ramps, show that L^p is complete. The turn is the parallelogram law: of all the L^p spaces only L^2 "
              "has angles, and with them come the nearest point of a closed convex set, functionals as inner "
              "products, and orthonormal bases with Bessel and Parseval. That answers the Fourier question in L^2, "
              "while Fejer's positive kernel gives uniform convergence for continuous functions. The second half "
              "applies the Hilbert space to measures: von Neumann's proof of Radon-Nikodym, the dual of L^p and of "
              "C(X), Lebesgue's differentiation theorem by the maximal function, and absolute continuity as the "
              "exact condition for the fundamental theorem of calculus, with the Cantor function as the failure. "
              "It ends with the change of variables formula and the Gaussian integral.",
        handoff="The dual of L^infinity and the Fourier series that diverges are left for Hahn-Banach and uniform "
                "boundedness in Part 8; Plancherel on the line and Sobolev spaces build on L^2 in Part 9; orthogonal "
                "projections are the bricks of the spectral theorem in Part 10, which Parseval's identity foreshadows.",
        outside="Linear algebra: inner products and orthogonal projection in R^n.",
        objectives={
            "U": ["Compute p-norms of vectors and of simple functions, and use the parallelogram law to test "
                  "whether a norm comes from an inner product.",
                  "Project a function onto a finite-dimensional subspace of L^2 by the normal equations or by "
                  "Gram-Schmidt, and check that the error is perpendicular to the subspace."],
            "M": ["Prove Hoelder and Minkowski from Young's inequality, and Riesz-Fischer from the limit theorems "
                  "of Part 5.",
                  "Prove the projection theorem from the parallelogram law, and derive the Riesz representation "
                  "and the equivalent forms of completeness of an orthonormal set (Parseval)."],
            "D": ["Prove Radon-Nikodym by von Neumann's Hilbert space argument and deduce that the dual of L^p is "
                  "L^q for finite p.",
                  "Prove the Hardy-Littlewood maximal inequality from the covering lemma, deduce Lebesgue's "
                  "differentiation theorem, and characterize absolutely continuous functions as integrals of "
                  "their derivatives."],
            "I": ["Compute a least-squares approximation in an orthonormal basis, and say why it beats a Taylor "
                  "polynomial over an interval.",
                  "Choose between partial sums and Fejer means of a Fourier series, knowing which converges in "
                  "which norm and which one overshoots at a jump."],
        },
        results=[
            ("Hoelder and Minkowski", r"\int |fg|\,d\mu \le \|f\|_p\,\|g\|_q,\quad \|f+g\|_p \le \|f\|_p+\|g\|_p"
                                      r"\quad \bigl(\tfrac1p+\tfrac1q=1\bigr)"),
            ("Riesz-Fischer", r"L^p(\mu)\ \text{is complete for } 1\le p\le\infty"),
            ("Parallelogram law and projection",
             r"\|x+y\|^2+\|x-y\|^2 = 2\|x\|^2+2\|y\|^2;\quad x = Px + Qx,\ \ Qx\perp M"),
            ("Riesz representation; Parseval for a maximal orthonormal set",
             r"\Lambda x=\langle x,y\rangle,\ \ \|\Lambda\|=\|y\|;\quad \sum_\alpha |\langle x,u_\alpha\rangle|^2=\|x\|^2"),
            ("Lebesgue-Radon-Nikodym", r"\lambda=\lambda_a+\lambda_s,\quad \lambda_a(E)=\int_E h\,d\mu,\quad "
                                       r"h\in L^1(\mu),\quad \lambda_s\perp\mu"),
            ("Fundamental theorem of calculus",
             r"f \text{ absolutely continuous}\iff f(x)-f(a)=\int_a^x f'(t)\,dt,\ \ f'\in L^1"),
        ],
        U=(0, 1, 2, 5, 6, 8), D=(11, 12, 13), I=(9, 15),
    ),
    Part(
        n=7, level="M", widget="rouchewinding", prereq=(2, 3, 4, 6),
        question="Why is a function with one complex derivative so much better behaved than a differentiable function on the real line?",
        story="The part opens with e^(-1/x^2) from Part 2, smooth on the real line with a Taylor series that says "
              "nothing, and shows it exploding along the imaginary axis. A complex derivative is a rotation and a "
              "scaling, so holomorphic maps keep angles; integrals around closed paths count turns, and Goursat's "
              "bisection proves Cauchy's theorem. Cauchy's formula then delivers the three miracles: one "
              "derivative gives a power series (the Fibonacci numbers come out as contour integrals), Liouville's "
              "theorem gives the fundamental theorem of algebra, and the values on a short arc decide the function "
              "everywhere. The global half computes real integrals by residues, counts roots with Rouche's dog on a "
              "leash, and uses the maximum principle as a tool in the Schwarz lemma and the three lines theorem. "
              "Runge's theorem says when polynomials approximate, Montel's theorem gives compactness, and the "
              "Riemann mapping theorem is proved as an extremal problem and computed for an L-shaped hexagon by "
              "Schwarz-Christoffel. A tour without proofs ends the part: harmonic functions and Poisson's integral, "
              "Weierstrass and Blaschke products, continuation, and the Hardy space H^2 with the shift.",
        handoff="Cauchy's formula, Liouville's theorem and Runge's theorem run the spectral theory and the "
                "functional calculus of Part 10, where the shift's spectrum is the closed disk; the three lines "
                "theorem and Paley-Wiener return with the Fourier transform in Part 9.",
        outside="Complex numbers and power series; for H^2, Fourier series in L^2 from Part 6.",
        objectives={
            "U": ["Check the Cauchy-Riemann equations and explain why a holomorphic map with nonzero derivative "
                  "preserves angles.",
                  "Compute path integrals of powers of z and the winding number of a closed curve around a point."],
            "M": ["Prove Cauchy's theorem for a triangle by Goursat's bisection and derive Cauchy's formula, power "
                  "series, Liouville's theorem and the fundamental theorem of algebra from it.",
                  "Prove the open mapping theorem, the maximum modulus principle and the Schwarz lemma, and use "
                  "Rouche's theorem to count zeros."],
            "D": ["Prove the Riemann mapping theorem from Montel's theorem as an extremal problem, saying where "
                  "simple connectivity enters.",
                  "Prove Runge's theorem by pushing poles, and explain why polynomials cannot approximate 1/z on "
                  "an annulus."],
            "I": ["Evaluate real integrals by residues, choosing the contour and bounding the part that fades.",
                  "Solve the Dirichlet problem on the disk with Poisson's integral, and count the roots of a "
                  "polynomial in a disk numerically with the argument principle."],
        },
        results=[
            ("Cauchy-Riemann equations",
             r"f=u+iv \text{ real-differentiable}:\quad f'(z_0) \text{ exists}\iff u_x=v_y,\ \ u_y=-v_x"),
            ("Cauchy's formula", r"f(a)\,\operatorname{Ind}_\gamma(a)=\frac{1}{2\pi i}\int_\gamma\frac{f(z)}{z-a}\,dz,"
                                 r"\quad \operatorname{Ind}_\gamma(a)=\frac{1}{2\pi i}\int_\gamma\frac{dz}{z-a}\in\mathbb{Z}"),
            ("Cauchy's estimates, hence Liouville", r"|f^{(n)}(a)|\le \frac{n!\,M}{R^n}\ \text{ if } |f|\le M "
                                                    r"\text{ on } D(a;R)"),
            ("Residue theorem",
             r"\frac{1}{2\pi i}\int_\gamma f\,dz=\sum_k \operatorname{Res}(f;a_k)\operatorname{Ind}_\gamma(a_k)"),
            ("Argument principle",
             r"\frac{1}{2\pi i}\int_{|z|=r}\frac{f'(z)}{f(z)}\,dz=\#\{\text{zeros of } f \text{ in } |z|<r\}"),
            ("Riemann mapping theorem", r"\Omega\ne\mathbb{C} \text{ simply connected}\implies "
                                        r"\Omega \text{ is conformally equivalent to the disk}"),
        ],
        U=(0, 1, 2, 3), D=(7, 9, 12), I=(5, 10),
    ),
    Part(
        n=8, level="M", widget="lebesgueconstant", prereq=(1, 3, 6),
        question="Does a continuous function always have a convergent Fourier series, and what can be proved about every complete normed space at once?",
        story="The part opens with Dirichlet's kernel: a function bounded by one can line up its sign with the "
              "kernel's, so the norm of the functional f -> s_n(f)(0) is the integral of |D_n|, which grows like "
              "(4/pi^2) log n. Du Bois-Reymond built a divergent example by hand in 1873; Banach and Steinhaus get "
              "one in three lines. After Banach and Frechet spaces and the Volterra operator's norm 2/pi, Baire's "
              "theorem is proved with nested intervals dodging the rationals, and its three children follow: "
              "uniform boundedness (most continuous functions have Fourier series that diverge at 0), the open "
              "mapping theorem and the closed graph theorem, with Hellinger-Toeplitz as a corollary. Hahn-Banach, "
              "the pillar not built on Baire, supplies enough functionals and separates convex sets. The turn is "
              "compactness: the unit vectors of l^2 stay root two apart, but they converge weakly, and "
              "Banach-Alaoglu makes the dual unit ball weak-star compact. Krein-Milman finds extreme points and "
              "shows L^1 is not a dual space; compact operators keep linear algebra alive, with the string's "
              "Green's operator as the model. Four applications close the part: a Banach limit, Grothendieck's "
              "closed-graph argument, Haar measure, and c_0 uncomplemented in l^infinity.",
        handoff="Frechet spaces and weak-star limits carry the test functions and distributions of Part 9; "
                "Hellinger-Toeplitz is why Part 10 needs unbounded operators, Alaoglu makes its maximal ideal space "
                "compact, and the Volterra and Green's operators return there with their spectra.",
        outside="Metric spaces and compactness (Part 1), the sup norm on C(X) and Arzela-Ascoli (Part 3), and the "
                "L^p spaces with their duals (Part 6).",
        objectives={
            "U": ["Compute the operator norm of a matrix or of a simple integral operator, and explain why a linear "
                  "map is continuous exactly when it is bounded.",
                  "Run the nested-interval argument that proves Baire's theorem on the real line, and say what "
                  "meager and residual mean."],
            "M": ["Prove Banach-Steinhaus, the open mapping theorem and the closed graph theorem from Baire's "
                  "theorem, and use the Lebesgue constants to show that Fourier series of continuous functions "
                  "can diverge.",
                  "State Hahn-Banach in its extension and separation forms, prove the one-dimensional extension "
                  "step, and prove Banach-Alaoglu from Tychonoff's theorem."],
            "D": ["Prove with Alaoglu and Krein-Milman that L^1[0, 1] is not the dual of any Banach space, and "
                  "explain why L^p for p below 1 has no nonzero continuous functionals.",
                  "Prove that a locally compact topological vector space is finite-dimensional, and state the "
                  "Fredholm alternative for compact operators."],
            "I": ["Compute Lebesgue constants and decide when an interpolation or summation method is stable by "
                  "checking whether its operator norms stay bounded.",
                  "Discretize a compact integral operator and read its eigenvalues or singular values, knowing "
                  "they can accumulate only at zero."],
        },
        results=[
            ("Baire's theorem", r"X \text{ complete metric},\ V_n \text{ open and dense}\implies \bigcap_n V_n "
                                r"\text{ is dense in } X"),
            ("Banach-Steinhaus, X a Banach space", r"\sup_\alpha\|\Lambda_\alpha x\|<\infty \ \text{for every } x"
                                                   r"\implies \sup_\alpha\|\Lambda_\alpha\|<\infty"),
            ("Lebesgue constants", r"\|f\mapsto s_n(f;0)\|=\frac{1}{2\pi}\int_{-\pi}^{\pi}|D_n(t)|\,dt"
                                   r"=\frac{4}{\pi^2}\log n+O(1)"),
            ("Open mapping, X and Y Banach spaces", r"\Lambda:X\to Y \text{ bounded, onto}\implies "
                                                    r"\Lambda(U_X)\supset \delta\,U_Y,\ \ \delta>0"),
            ("Hahn-Banach", r"\|x\|=\max\{|\Lambda x| : \Lambda\in X^*,\ \|\Lambda\|\le 1\}"),
            ("Banach-Alaoglu; Krein-Milman for K compact convex",
             r"\{\|\Lambda\|\le1\}\subset X^* \text{ is weak}^*\text{ compact};\quad "
             r"K=\overline{\operatorname{co}}\,(\operatorname{ext}K)"),
        ],
        U=(0, 1, 3), D=(2, 10), I=(11, 12),
    ),
    Part(
        n=9, level="M", widget="deltabump", prereq=(6, 7, 8),
        question="How can every function be differentiated, even one with jumps, and what does the Fourier transform do to the result?",
        story="The part opens with Dirac's delta, which no function can be, and with narrowing bumps that return "
              "phi(0) when integrated against a smooth phi: ask what delta does, not what it is. Test functions "
              "are built from the flat function of Part 2, distributions are the continuous functionals on them, "
              "and the derivative is defined by moving it onto the test function, so the sign function's "
              "derivative is two delta and the sawtooth's series may be differentiated term by term. Locally "
              "every distribution is a derivative of a continuous function, and convolution with a bump turns it "
              "back into a smooth one. The second half is the Fourier transform in Rudin's convention: box to "
              "sinc, inversion with Gibbs' overshoot, Plancherel, the Schwartz space on which the transform is a "
              "quarter turn, tempered distributions and Poisson summation. Then what it buys: Paley-Wiener reads "
              "support as growth in the complex plane, Sobolev norms read smoothness as decay, and fundamental "
              "solutions are found by shifting the inversion contour past the zeros of the symbol "
              "(Malgrange-Ehrenpreis). It ends with Wiener's Tauberian theorem and the prime number theorem.",
        handoff="The convolution algebra L^1 and its maximal ideals are the first case of Gelfand's theory in Part "
                "10, where Wiener's 1/f theorem gets a three-line proof and Plancherel's theorem becomes the "
                "spectral theorem for the momentum operator.",
        outside="Integration by parts and Fourier series; for chapters 9 and 11, Cauchy's theorem (Part 7); for the "
                "topology of the test functions, Frechet spaces (Part 8).",
        objectives={
            "U": ["Differentiate functions with corners and jumps as distributions, and check the answer by "
                  "pairing with a test function.",
                  "Compute the Fourier transforms of a box, a triangle and a Gaussian, and use the rules for "
                  "shifts and derivatives."],
            "M": ["Define distributions, their order, support and derivatives, and prove that a convergent "
                  "sequence of distributions may be differentiated term by term.",
                  "Prove the inversion theorem and Plancherel's theorem, extend the transform to tempered "
                  "distributions, and derive Poisson summation."],
            "D": ["State and prove one direction of the Paley-Wiener theorem by shifting the contour, and prove "
                  "Sobolev's lemma for s greater than n/2.",
                  "Outline the proof of Malgrange-Ehrenpreis, and explain how Wiener's Tauberian theorem with the "
                  "non-vanishing of zeta on the line Re s = 1 gives the prime number theorem."],
            "I": ["Find a fundamental solution of a constant-coefficient operator and use convolution with it to "
                  "solve the equation for any right-hand side.",
                  "Predict the decay of a transform from the smoothness of the function, and say when a truncated "
                  "inversion will show Gibbs' overshoot."],
        },
        results=[
            ("Derivative of a distribution", r"\langle D^\alpha T,\phi\rangle=(-1)^{|\alpha|}\langle T,D^\alpha\phi\rangle;"
                                             r"\qquad H'=\delta,\quad (\operatorname{sgn})'=2\delta"),
            ("Fourier transform and Plancherel",
             r"\hat f(t)=\frac{1}{\sqrt{2\pi}}\int f(x)e^{-ixt}\,dx,\qquad \|\hat f\|_2=\|f\|_2"),
            ("Tempered distributions and Poisson summation",
             r"\langle\hat u,\phi\rangle=\langle u,\hat\phi\rangle,\quad \hat\delta=\tfrac{1}{\sqrt{2\pi}},\quad "
             r"\sum_{n}\phi\bigl(n\sqrt{2\pi}\bigr)=\sum_{n}\hat\phi\bigl(n\sqrt{2\pi}\bigr)"),
            ("Paley-Wiener, for smooth functions and every N",
             r"\operatorname{supp}\phi\subset[-A,A]\iff \hat\phi \text{ entire},\ "
             r"|\hat\phi(z)|\le \gamma_N(1+|z|)^{-N}e^{A|\operatorname{Im}z|}"),
            ("Sobolev's lemma", r"\int(1+|t|^2)^s|\hat f(t)|^2\,dt<\infty,\ \ s>\tfrac n2"
                                r"\implies f \text{ is continuous}"),
            ("Fundamental solutions", r"P(D)E=\delta\implies P(D)(E*f)=f;\quad E \text{ exists for every } P\ne 0"),
        ],
        U=(0, 3, 6), D=(9, 12), I=(7, 11),
    ),
    Part(
        n=10, level="M", widget="approxeigen", prereq=(6, 7, 8, 9),
        question="What does it mean to diagonalize an operator that has no eigenvectors?",
        story="The part opens with two meanings of spectrum: hydrogen's lines, and the set of lambda where T - "
              "lambda has no inverse. The shift on l^2 has no eigenvalue, yet its spectrum is the closed disc, and a "
              "finite section's eigenvalues lie while its resolvent tells the truth. Banach algebras give "
              "operators an arithmetic: the Neumann series, a spectrum that is compact and nonempty by "
              "Liouville, Gelfand's formula for its radius, and the Volterra operator with spectrum {0} and no "
              "eigenvector. Cauchy's formula with the resolvent as kernel defines f(A), and Gelfand's transform "
              "turns a commutative algebra into functions, which proves Wiener's 1/f theorem in three lines. In "
              "Hilbert space the compact self-adjoint case is the vibrating string; multiplication by x has an "
              "interval of spectrum, approximate eigenvectors and the Born rule; and the spectral theorem for "
              "normal operators is proved with tools from Parts 3, 5, 6, 7 and 8. Unbounded operators come with "
              "domains: i d/dx on [0, 1] has a circle of self-adjoint extensions, the Cayley transform reduces "
              "the unbounded theorem to the unitary one, and Stone's theorem forces time evolution to be "
              "e^(-itH). The part ends with hydrogen's spectrum and the reason position and momentum must be "
              "unbounded.",
        handoff="This is the last part: it closes the ledger from the least upper bound property to the spectral "
                "theorem and proves what the quantum films assumed. The film names where the road divides: "
                "operator algebras, index theory, nonlinear analysis, partial differential equations and "
                "harmonic analysis.",
        outside="Eigenvalues and diagonalization of matrices; for the last three chapters, the vocabulary of "
                "quantum mechanics (states, observables, the Schroedinger equation) helps but is not needed.",
        objectives={
            "U": ["Sum a Neumann series to invert I - A when the norm of A is below one, and bound the error "
                  "after n terms.",
                  "Compute adjoints, projections and the numerical range of small matrices, and say what "
                  "self-adjoint, unitary and normal mean."],
            "M": ["Prove that the spectrum of an element of a Banach algebra is compact and nonempty, and prove "
                  "Gelfand's spectral radius formula.",
                  "Prove the spectral theorem for compact self-adjoint operators, and show that multiplication "
                  "by x on L^2[0, 1] has spectrum [0, 1] and no eigenvalue."],
            "D": ["Prove the spectral theorem for bounded normal operators from Gelfand-Naimark and the Riesz "
                  "representation theorem, and extend it to unbounded self-adjoint operators by the Cayley "
                  "transform.",
                  "Compute deficiency indices and classify the self-adjoint extensions of i d/dx on an interval; "
                  "state Stone's theorem."],
            "I": ["Diagonalize a discretized operator to solve the heat or the Schroedinger equation, and read a "
                  "state's spectral measure as the Born rule.",
                  "Use the size of the resolvent, not the eigenvalues, to judge a non-normal matrix, and explain "
                  "why no finite matrices satisfy the canonical commutation relation."],
        },
        results=[
            ("Neumann series", r"\|x\|<1\implies (e-x)^{-1}=\sum_{n\ge0}x^n,\quad "
                               r"\Bigl\|(e-x)^{-1}-\sum_{k\le n}x^k\Bigr\|\le\frac{\|x\|^{n+1}}{1-\|x\|}"),
            ("Gelfand's spectral radius formula", r"\sigma(x)\ne\emptyset \text{ is compact},\qquad "
                                                  r"\max_{\lambda\in\sigma(x)}|\lambda|=\lim_{n\to\infty}\|x^n\|^{1/n}"),
            ("Functional calculus and spectral mapping",
             r"f(x)=\frac{1}{2\pi i}\int_\Gamma f(\lambda)(\lambda e-x)^{-1}\,d\lambda,\qquad \sigma(f(x))=f(\sigma(x))"),
            ("Gelfand-Naimark, A commutative", r"\|x^*x\|=\|x\|^2 \text{ for all } x\implies "
                                               r"x\mapsto\hat x:\ A\cong C(\Delta)"),
            ("Spectral theorem, T normal, E a projection-valued measure",
             r"T=\int_{\sigma(T)}\lambda\,dE(\lambda),\qquad f(T)=\int_{\sigma(T)} f\,dE"),
            ("Stone's theorem", r"U(t) \text{ continuous unitary group}\iff U(t)=e^{itA},\ \ A=A^*"),
        ],
        U=(0, 1, 5), D=(4, 8, 10), I=(6, 11, 12),
        also=(("Quantum mechanics, the first film", "videos/physics/quantum"),
              ("Quantum mechanics, the second film", "videos/physics/quantum2")),
    ),
]
