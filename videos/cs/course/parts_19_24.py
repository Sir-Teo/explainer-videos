"""Act IV, Algorithms: paradigms, randomness, strings, geometry, optimization and practice (Parts 19-24)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=19, level="U", widget="rootsquaring", prereq=(2, 16, 18),
        question="Which few ideas produce most good algorithms, and how far can a better decomposition go?",
        story="The part opens with a million digits of pi, certified between two bounds, and two million-digit "
              "numbers multiplied several ways. Greedy comes first: interval scheduling by earliest finish, proved "
              "by an exchange argument, then coins and matchings where a plausible rule fails, and Whitney's "
              "matroids, the structures on which greedy is right for every nonnegative weighting. Divide and "
              "conquer follows: Karatsuba's three half-size products instead of four, Strassen's seven instead of "
              "eight, and the fast Fourier transform, which evaluates a polynomial at the roots of unity because "
              "squaring them halves their number at every level. The FFT multiplies integers, and the part is "
              "careful about what that needs: a small rounding distance is a diagnostic, and the certificate is an "
              "exact check modulo two primes. Dynamic programming fills tables for edit distance, knapsack, matrix "
              "chains and trees, and backtracking with Dancing Links searches where no structure is known. The "
              "part ends with the maximum subarray solved four ways, cubic to linear, and with the open questions "
              "about the exponent of matrix multiplication, edit distance under SETH and circuits for the DFT.",
        handoff="Insert and delete scripts return as paths in an edit graph in Part 21; branch and bound and linear "
                "programming in Part 23; knapsack, subset sum and generalized Sudoku as NP-complete problems in "
                "Part 26; the conditional lower bound for edit distance in Part 27; big-integer arithmetic and "
                "modular transforms in Part 30; the quantum Fourier transform in Part 53.",
        outside="Complex numbers on the unit circle, and matrix multiplication.",
        objectives={
            "U": ["Prove a greedy rule correct by an exchange argument, and give a counterexample to a rule that "
                  "only looks plausible.",
                  "Fill and trace back the tables for edit distance and knapsack, and explain why O(nW) is "
                  "pseudo-polynomial.",
                  "Solve the maximum-subarray problem by Kadane's recurrence and say what each of the four "
                  "methods reuses."],
            "M": ["Derive Karatsuba's and Strassen's recurrences and solve them, counting the additions as well "
                  "as the products.",
                  "Derive the FFT from the even and odd split at the roots of unity, and prove the inverse by "
                  "orthogonality.",
                  "Prove that greedy is optimal for every nonnegative weighting of a hereditary system exactly "
                  "when the system is a matroid."],
            "D": ["State what a barrier for the laser method restricts and what it leaves open about the matrix "
                  "multiplication exponent.",
                  "Explain how a truly subquadratic exact edit-distance algorithm would contradict SETH, and why "
                  "Morgenstern's bound does not cover circuits with unrestricted coefficients."],
            "I": ["Certify a floating-point FFT product with an independent exact check instead of trusting "
                  "the distance to the nearest integer.",
                  "Choose a multiplication method and a cutoff from measurements, stating the timing boundary: "
                  "what was converted, carried and checked outside the timer."],
        },
        results=[
            ("Greedy and matroids", r"\text{greedy is optimal for every } w\ge 0\iff(E,\mathcal I)\text{ is a matroid}"),
            ("Karatsuba's identity", r"x_1y_0+x_0y_1=(x_1+x_0)(y_1+y_0)-x_1y_1-x_0y_0"),
            ("Two recurrences", r"3\,T(\tfrac n2)+O(n)=\Theta(n^{\log_2 3}),\qquad 7\,T(\tfrac n2)+O(n^2)=\Theta(n^{\log_2 7})"),
            ("The FFT step", r"A(\pm\omega^k)=A_e(\omega^{2k})\pm\omega^k A_o(\omega^{2k}),\qquad \omega=e^{2\pi i/n}"),
            ("Orthogonality", r"\sum_{k=0}^{n-1}\omega^{jk}=0\ \ (n\nmid j),\qquad F^{-1}=\tfrac1n\,\overline F"),
            ("Edit distance", r"D_{i,j}=\min\bigl\{D_{i-1,j}+1,\ D_{i,j-1}+1,\ D_{i-1,j-1}+[a_i\ne b_j]\bigr\}"),
        ],
        U=(0, 1, 3, 5, 9, 10, 11, 14, 15), D=(16,), I=(7,),
        also=(("The paradigms' instruments", "explainer/cs/algo/paradigms.py"),),
    ),
    Part(
        n=20, level="U", widget="bloombits", prereq=(2, 16, 17, 19),
        question="What can an algorithm do with coin flips that it cannot easily do without them?",
        story="The part opens with the top twenty words of the thirty novels counted twice: by Part 17's exact hash "
              "table, and by a sketch that keeps thirty-two candidate words in about eighteen kilobytes of program "
              "data. It separates Las Vegas algorithms, always right with a random running time, from Monte Carlo "
              "ones, and shows how independent repetition shrinks a one-sided error to 2^-k. Freivalds checks a "
              "matrix product with three matrix-vector products, Schwartz and Zippel test a polynomial identity at "
              "random points, Karger finds a minimum cut by contracting random edges, and Miller and Rabin repair "
              "Fermat's test after 561 fools it. Random walks solve 2-SAT, two choices flatten the fullest bin, and "
              "Bloom filters, reservoirs, Count-Min, HyperLogLog, the AMS sketch and MinHash answer questions about "
              "streams in little memory. The Job is rebuilt on a Count-Min sketch for ledger row 9, and a sweep of "
              "twenty hash seeds shows that its exact answer was not guaranteed. The part then turns to where the "
              "coins come from: the probabilistic method, conditional expectations, RANDU's fifteen planes, and the "
              "open question whether P equals BPP.",
        handoff="Fingerprints become Rabin and Karp's string search in Part 21, and locality-sensitive hashing "
                "finds nearest neighbours in Part 22; Part 23 rounds linear programs at random; Part 27 develops "
                "BPP, hardness against randomness and streaming lower bounds; Part 29 builds cryptographic "
                "generators and Part 30 needs the large primes; Bloom filters return in Part 34's storage engines, "
                "sketches in Parts 46 and 47, two choices in Part 48 and expanders in Part 56.",
        outside="Discrete probability: independence, expectation, Markov's inequality, and arithmetic modulo a prime.",
        objectives={
            "U": ["Tell a Las Vegas algorithm from a Monte Carlo one, and compute how many independent rounds "
                  "bring a one-sided error below a target.",
                  "Run Freivalds' check and the Miller-Rabin test by hand on small inputs, and say what a pass "
                  "does and does not certify.",
                  "Size a Bloom filter for a target false-positive rate, and explain why it never gives a false "
                  "negative."],
            "M": ["Prove Freivalds' bound by deferred decisions and the Schwartz-Zippel lemma by induction on the "
                  "number of variables.",
                  "Derive Karger's 2/(n(n-1)) bound and the corollary that a graph has at most n-choose-2 minimum "
                  "cuts.",
                  "Derive the Count-Min guarantee for one fixed item and the variance of the AMS estimator from "
                  "four-wise independent signs."],
            "D": ["State the hardness premise under which P equals BPP, and explain why a deterministic identity "
                  "test would imply circuit lower bounds.",
                  "Use the expectation argument and the local lemma to prove that an object exists, and say what "
                  "Moser and Tardos add."],
            "I": ["Choose between an exact table, Misra-Gries, Count-Min and HyperLogLog for a stream, stating "
                  "the guarantee each one actually has for the implementation's hashes.",
                  "Explain why a simulation generator such as the Mersenne Twister must not be used for secrets, "
                  "and what RANDU did to three-dimensional samples."],
        },
        results=[
            ("Amplification", r"\Pr[\text{a wrong answer passes one round}]\le\tfrac12\ \Rightarrow\ \Pr[\text{passes }k]\le 2^{-k}"),
            ("Schwartz-Zippel", r"p\not\equiv 0,\ \deg p=d:\qquad \Pr_{r\in S^n}\bigl[p(r)=0\bigr]\le\frac{d}{|S|}"),
            ("Karger's contraction", r"\Pr[C\text{ survives}]\ \ge\ \prod_{i=3}^{n}\Bigl(1-\frac2i\Bigr)=\frac{2}{n(n-1)}"),
            ("Two choices", r"\max\text{ load}:\quad \frac{\ln n}{\ln\ln n}\,(1+o(1))\ \ \text{against}\ \ \frac{\ln\ln n}{\ln 2}+O(1)"),
            ("Bloom filter", r"f\approx\bigl(1-e^{-kn/m}\bigr)^k,\qquad k^*=\tfrac mn\ln 2,\quad f^*\approx 0.6185^{\,m/n}"),
            ("Count-Min", r"w\ge\tfrac e\varepsilon,\ d\ge\ln\tfrac1\delta:\quad f_x\le\hat f_x\le f_x+\varepsilon N\ \text{ w.p. }\ge 1-\delta"),
        ],
        U=(0, 1, 2, 4, 5, 7, 8), D=(16,), I=(10, 13),
        also=(("The randomized instruments", "explainer/cs/algo/randomized.py"),
              ("The Job on a sketch", "explainer/cs/algo/job3.py")),
    ),
    Part(
        n=21, level="U", widget="skipahead", prereq=(12, 17, 19, 20),
        question="How do you find, compress and compare text without reading all of it again each time?",
        story="The part opens with Queequeg found four ways in the 25 megabytes of thirty novels: by a naive scan, "
              "by Knuth, Morris and Pratt, by Boyer and Moore, and by sixteen rank requests on an index. The naive "
              "scan costs about one comparison per character on English and (n - m + 1) m on a run of one letter; "
              "rolling hashes, the border table of KMP and the skips of Boyer and Moore each remove part of that "
              "cost, and Aho and Corasick search for many patterns in one pass. The part then indexes the text "
              "itself: a suffix tree, the suffix array of the whole corpus, and the Burrows-Wheeler transform, "
              "whose last-to-first mapping both inverts it and searches it backwards as the FM-index. Compression "
              "follows from the same structure: Lempel and Ziv's back-references, Huffman and ANS coding, and the "
              "rule that a better model of context costs fewer bits. Alignment, Myers' diff on the history of the "
              "course's own syllabus, rsync and content-defined chunks compare and synchronize texts. The part "
              "ends with periods, palindromes and Lyndon words, and with indexes whose size follows the number of "
              "runs of the transform.",
        handoff="Part 27 proves the conditional lower bound behind edit distance's quadratic wall; Part 28 adds "
                "noise to the information theory; Parts 34 and 35 compress storage engines and column stores; "
                "Part 41 builds git's merges on Myers' diff and its packfiles on delta compression; Part 47 uses "
                "inverted indexes and near-duplicate detection, and Part 57 connects learning to compression.",
        outside="Logarithms and the idea of entropy as bits per symbol; modular arithmetic for the rolling hash.",
        objectives={
            "U": ["Compute the border table of a pattern and trace Knuth-Morris-Pratt on a text without moving "
                  "backwards in it.",
                  "Build the suffix array and the Burrows-Wheeler transform of a short string by hand, and "
                  "invert the transform with the last-to-first mapping.",
                  "Parse a text into Lempel-Ziv back-references, and read an edit script off Myers' edit graph."],
            "M": ["Prove the 2n comparison bound of KMP by the amortized argument, and the (m - 1)/p collision "
                  "bound of a rolling hash with a random base.",
                  "Run backward search on an FM-index, counting the rank requests, and explain what locating "
                  "adds to counting.",
                  "Derive the O(N(D + 1)) bound of Myers' algorithm from furthest-reaching paths on diagonals."],
            "D": ["State what an index of size proportional to the number of runs r of the transform supports, "
                  "and how r relates to the Lempel-Ziv phrase count z.",
                  "State exactly what the SETH lower bound for edit distance covers, and which variants "
                  "(approximation, banded, compressed inputs) escape it."],
            "I": ["Choose between fixed blocks, a rolling checksum and content-defined chunks for "
                  "synchronizing or deduplicating files, and predict what an insertion does to each.",
                  "Report a compressor or an index honestly: emitted bytes against a cost model, and count "
                  "queries against locate queries."],
        },
        results=[
            ("Rolling hash", r"h_{i+1}=\bigl(h_i-t_i\,b^{m-1}\bigr)\,b+t_{i+m}\pmod p,\qquad \Pr[\text{collision}]\le\frac{m-1}{p}"),
            ("Knuth-Morris-Pratt", r"\text{comparisons}\le 2n,\qquad \text{periods of } w=\{\,|w|-|u| : u\text{ a border of }w\,\}"),
            ("Last-to-first mapping", r"L[i]=T[\mathrm{SA}[i]-1],\qquad \mathrm{LF}(i)=C[L[i]]+\operatorname{rank}_{L[i]}(L,i)"),
            ("Backward search", r"lo\leftarrow C[c]+\operatorname{rank}_c(L,lo),\quad hi\leftarrow C[c]+\operatorname{rank}_c(L,hi)"),
            ("Myers' diff", r"D=n+m-2\,\mathrm{LCS}(a,b),\qquad \text{time } O\bigl(N(D+1)\bigr),\ N=n+m"),
            ("Fine and Wilf", r"\text{periods }p,q,\ |w|\ge p+q-\gcd(p,q)\ \Rightarrow\ \gcd(p,q)\text{ is a period}"),
        ],
        U=(0, 1, 2, 3, 10, 13), D=(16,), I=(14,),
        also=(("The string instruments", "explainer/cs/algo/strings.py"),),
    ),
    Part(
        n=22, level="U", widget="orientgrid", prereq=(4, 16, 18, 20),
        question="How can a program that only computes signs of determinants get geometry right?",
        story="The part opens with one orientation test asked three ways in double precision and answered three "
              "ways: left, on the line, right. Kettner's grid of neighbouring doubles shows a speckled band of "
              "wrong signs, and the part repairs the predicate with a certified floating filter and an exact "
              "fallback before it builds anything. On that one primitive it builds convex hulls, with the lower "
              "bound that a hull of points on a parabola sorts, the sweep line for segment intersections, and "
              "Fisk's three-colour proof that a gallery of n walls needs at most n/3 guards. Fortune's beach line "
              "of parabolas draws the Voronoi diagram, Lawson's flips reach its dual, the Delaunay triangulation, "
              "and the lifting map shows that triangulation to be the shadow of a convex hull on a paraboloid. "
              "Backwards analysis prices random insertion, Seidel's planar linear programming and Welzl's "
              "enclosing circle. The part ends with range search, point location, the failure of kd-trees in high "
              "dimensions and graph indexes that replace them, duality, a robot among Minkowski sums, and the "
              "3SUM barrier.",
        handoff="Part 23 takes linear programming to many dimensions with the simplex method; Part 27 builds "
                "fine-grained complexity on 3SUM; Part 47's search engine and Part 48's maps use the neighbour "
                "graphs of chapter 12; Part 51 draws triangles with the orientation test and traces rays through "
                "bounding-volume hierarchies; Part 52 returns to floating point.",
        outside="Coordinates, determinants of small matrices, and the equations of a line, a circle and a parabola.",
        objectives={
            "U": ["Compute an orientation test as a signed area and use it to run Graham's scan by hand.",
                  "Explain with an example why a floating-point orientation sign can be wrong, and what a "
                  "filtered predicate does about it.",
                  "Prove the art gallery bound from a triangulation and a three-colouring."],
            "M": ["Prove the n log n lower bound for convex hulls by lifting numbers to a parabola, and state "
                  "what Chan's algorithm gains when the hull is small.",
                  "Derive the in-circle test from the lifting map, and explain why Lawson's flips terminate.",
                  "Use backwards analysis to bound the expected work of random insertion and of Seidel's "
                  "linear programming."],
            "D": ["State the 3SUM conjecture with its computational model, and reduce 3SUM to finding three "
                  "collinear points.",
                  "Describe what is proved and what is only measured about graph indexes for nearest "
                  "neighbours, and reproduce a published hard instance."],
            "I": ["Choose between a kd-tree, an exact scan and an approximate graph index from the dimension "
                  "and the data, and report recall with the number of distance evaluations.",
                  "Check a planned motion against obstacles over the whole segment, not at sampled points, and "
                  "state the contact convention."],
        },
        results=[
            ("Orientation", r"\operatorname{orient}(p,q,r)=\operatorname{sign}\bigl[(q_x-p_x)(r_y-p_y)-(q_y-p_y)(r_x-p_x)\bigr]"),
            ("Hulls sort", r"x\mapsto(x,x^2):\ \text{the hull lists the } x_i \text{ in order}\ \Rightarrow\ \Omega(n\log n)"),
            ("Art gallery", r"\lfloor n/3\rfloor\ \text{guards always suffice, and are sometimes necessary}"),
            ("The lifting map", r"(x,y)\mapsto(x,y,x^2+y^2):\quad \text{Delaunay}=\text{shadow of the lower convex hull}"),
            ("Backwards analysis", r"\Pr[\text{step } i \text{ moves the optimum}]\le\frac2i\ \Rightarrow\ \mathbb E[\text{moves}]\le 2H_n"),
            ("3SUM as collinearity", r"\det\begin{pmatrix}1&a&a^3\\1&b&b^3\\1&c&c^3\end{pmatrix}=(b-a)(c-a)(c-b)(a+b+c)"),
        ],
        U=(0, 1, 2, 3, 4, 10), D=(15,), I=(12, 14),
        also=(("The geometry instruments", "explainer/cs/algo/geometry.py"),),
    ),
    Part(
        n=23, level="U", widget="dualbound", prereq=(18, 19, 20, 22),
        question="How do you find the best choice, and how do you prove that nothing better exists?",
        story="In 1945 Stigler found a diet for 39.93 dollars a year by insight; two years later Laderman's team "
              "worked Dantzig's simplex method by hand and found 39.69, with a proof that no diet is cheaper. The "
              "part builds that method on Chvatal's three-product linear program: a polytope with six vertices, a "
              "walk of two pivots to a profit of 13, and dual prices (1, 0, 1) that certify it. It then asks how "
              "long the walk can be: Dantzig's rule takes 2^n - 1 pivots on Klee and Minty's cubes, while "
              "ellipsoids and the central path give polynomial bounds. Total unimodularity explains when the "
              "vertices are integers; when they are not, branch and bound uses the relaxation as a guide. For "
              "NP-hard problems the part proves how close a fast algorithm can get: factor 2 for vertex cover, "
              "H_n for set cover, 3/2 for metric tours, 0.878 for MAX-CUT by a random hyperplane. It ends with "
              "decisions made without the future (ski rental, paging), multiplicative weights, convex "
              "optimization in a page, and three open questions: strongly polynomial LP, the polynomial Hirsch "
              "conjecture and the Unique Games Conjecture.",
        handoff="Part 27 builds the PCP theorem behind the hardness results and states the Unique Games "
                "Conjecture; Part 32's kernel replaces pages with CLOCK; Part 45 packs virtual machines, an "
                "integer program solved by heuristics, and Part 48 balances load online; Part 52 explains why LP "
                "solvers fight floating point; Part 57 turns multiplicative weights into a theory of learning.",
        outside="Linear algebra: Gaussian elimination, matrix-vector products and determinants; the gradient of "
                "a function of several variables for chapter 13.",
        objectives={
            "U": ["Model a small planning problem as a linear program and solve it by pivoting a simplex "
                  "tableau.",
                  "Write the dual of a linear program and use a dual solution to prove that a primal solution "
                  "is optimal.",
                  "Prove the factor-2 guarantee for vertex cover and the competitive ratio of the break-even "
                  "rule for ski rental."],
            "M": ["Prove weak duality, state strong duality and Farkas' lemma, and read shadow prices and "
                  "complementary slackness off an optimal tableau.",
                  "Explain why a totally unimodular constraint matrix with integer right-hand sides gives "
                  "integer vertices, and why the triangle's matching polytope does not.",
                  "Derive the Goemans-Williamson constant from the probability that a random hyperplane "
                  "separates two unit vectors, and the regret bound of multiplicative weights from its "
                  "potential."],
            "D": ["State what smoothed analysis proves about a simplex method and what it does not say about "
                  "Dantzig's rule on a perturbed cube.",
                  "State the Hirsch conjecture, Santos's counterexample and the open polynomial version, and "
                  "the approximation thresholds that follow from the Unique Games Conjecture."],
            "I": ["Solve an integer program by branch and bound with exact bounds, and explain why a nearly "
                  "integral relaxation is not a feasible answer.",
                  "Report a solver or heuristic result with its certificate: a dual bound, an optimality gap, "
                  "or a guarantee and the model it assumes."],
        },
        results=[
            ("Strong duality", r"\max\{c^\top x: Ax\le b,\ x\ge 0\}=\min\{b^\top y: A^\top y\ge c,\ y\ge 0\}"),
            ("Complementary slackness", r"y_i\,(b-Ax)_i=0,\qquad x_j\,(A^\top y-c)_j=0"),
            ("Klee-Minty", r"\text{Dantzig's rule on the } n\text{-cube}:\ 2^n-1\ \text{pivots}"),
            ("Total unimodularity", r"\text{all minors of } A\in\{0,\pm1\},\ b\in\mathbb Z^m\ \Rightarrow\ \text{vertices of }\{Ax\le b,\ x\ge 0\}\in\mathbb Z^n"),
            ("Goemans-Williamson", r"\frac{\theta}{\pi}\ \ge\ \alpha\,\frac{1-\cos\theta}{2},\qquad \alpha=\min_\theta\frac{2\theta}{\pi(1-\cos\theta)}\approx 0.878"),
            ("Multiplicative weights", r"\text{regret}\le\frac{\ln n}{\eta}+\frac{\eta T}{8}=\sqrt{\tfrac12\,T\ln n}\quad\text{at }\eta=\sqrt{8\ln n/T}"),
        ],
        U=(0, 1, 2, 3, 8, 11), D=(14,), I=(7,),
        also=(("The optimization instruments", "explainer/cs/algo/optim.py"),),
    ),
    Part(
        n=24, level="U", widget="lowbitladder", prereq=(9, 10, 16, 17),
        question="When two algorithms have the same big-O, what decides which one is fast?",
        story="The part opens with two loops that add up n numbers, one over an array and one along a shuffled "
              "linked list: the same linear bound, and very different measured times. Its first half builds the "
              "everyday tools: prefix sums and difference arrays, Fenwick trees from the lowest set bit, segment "
              "trees over any associative operation, sparse tables and lowest common ancestors, two pointers and "
              "monotonic stacks, binary search on a monotone predicate, word-level bit tricks, meet in the middle "
              "and square-root blocks. Its second half is algorithm engineering on the rendering machine: search "
              "layouts from a sorted array to Eytzinger order and a 16-key node compared by vector instructions, "
              "a vectorized tokenizer, a Swiss-style hash table, radix sort against comparison sort, and the top "
              "twenty by a heap. A chapter on benchmarking says what such timings can and cannot show, and the "
              "part keeps to it: no cache-miss counter was collected, so no cause is claimed. The Job is "
              "engineered natively for the ledger's tenth row, the first measured on real hardware rather than "
              "modelled. The part ends with learned indexes and algorithms that use predictions.",
        handoff="B+ trees and vectorized query execution return in Part 35; ancestor queries on a history that is "
                "a DAG, not a tree, in Part 41; columnar files and SIMD scans in Part 46; galloping intersection "
                "of posting lists in Part 47; tail latency against load in Part 48; the roofline model in Part 60. "
                "Act V begins with Part 25, Undecidable.",
        outside="Two's complement and bitwise operators; enough C to read a short loop.",
        objectives={
            "U": ["Answer range-sum queries with prefix sums and apply range updates with a difference array.",
                  "Trace a Fenwick tree's query and update loops with the lowest-set-bit step, and say which "
                  "cells each one touches.",
                  "Solve a problem with two pointers or a monotonic stack and prove it linear by counting pushes "
                  "and pops."],
            "M": ["Build a segment tree for an associative operation with a small record per node, such as the "
                  "four numbers of the maximum subarray, and add lazy range updates.",
                  "Explain why a sparse table answers range minima in constant time but not range sums, and "
                  "reduce range minimum to lowest common ancestor and back.",
                  "Count the 3^n iterations of submask enumeration, and use meet in the middle to halve an "
                  "exponent."],
            "D": ["State what a learned index certifies about a lookup and what its model can cost in the worst "
                  "case.",
                  "State the consistency and robustness bounds of ski rental with a prediction, and propose a "
                  "cost model that could be tested on held-out workloads."],
            "I": ["Choose a search layout, a hash table or a sort for a hot path from measurements, and say "
                  "which mechanism the measurement does not isolate.",
                  "Design a benchmark with a fixed sample plan, interleaved variants, an observable result and "
                  "an output check, and report its spread.",
                  "Use Amdahl's law with a measured phase fraction to predict what speeding up one phase can "
                  "give."],
        },
        results=[
            ("Prefix sums", r"S_i=\sum_{j<i}a_j,\qquad \sum_{j=l}^{r}a_j=S_{r+1}-S_l"),
            ("Fenwick tree", r"\text{cell } i \text{ holds } a\bigl(i-\operatorname{lowbit}(i),\,i\bigr],\qquad \operatorname{lowbit}(i)=i\ \&\ (-i)"),
            ("Fenwick query cost", r"\text{prefix query}:\ \operatorname{popcount}(i)\le\lfloor\log_2 n\rfloor+1\ \text{cells}"),
            ("Sparse table", r"\min a[l..r]=\min\bigl(M_k[l],\,M_k[r-2^k+1]\bigr),\qquad k=\lfloor\log_2(r-l+1)\rfloor"),
            ("Submasks", r"\sum_{m\subseteq[n]}2^{|m|}=3^n"),
            ("Amdahl's law", r"\text{speedup}=\frac{1}{(1-p)+p/s}\ \le\ \frac{1}{1-p}"),
        ],
        U=(0, 1, 2, 5, 6, 13), D=(15,), I=(9, 10, 11, 12, 14),
        also=(("The practice instruments", "explainer/cs/algo/practice.py"),),
    ),
]
