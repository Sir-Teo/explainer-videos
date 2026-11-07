# Computer Science, Built — Part 56: Spectral Graphs and Expanders

Part 56 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act XI, *The Research Frontier*. A graph's matrices have eigenvalues,
and they know what its drawing hides: how hard the graph is to cut, how fast a random walk on it forgets where it
started, and how current flows through it. Graphs that are sparse yet impossible to cut, expanders, save random bits,
correct errors and prove theorems, and the same linear algebra, through electrical flows and fast Laplacian solvers,
led in 2022 to maximum flow in almost-linear time. Every bound is checked on small graphs and on the series' own:
Part 18's city grid, Part 36's internet and a word graph from *Pride and Prejudice*.

The instruments are in `explainer/cs/spectral/` (tested in `tests/test_cs56_spectral.py`):
* `spectra.py`: the Laplacian L = D − A and the normalized Laplacian N = I − D^{−1/2} A D^{−1/2}; a stochastic block
  model with planted communities; conductance, and the sweep cut over the Fiedler order of N's second eigenvector
  (scaled by D^{−1/2}); Cheeger's inequality checked against conductance found by brute force over every cut of
  12-vertex random graphs; the lazy walk (I + D^{−1}A)/2, its total-variation distance from stationarity step by step
  against the spectral-gap bound, on a cycle, a grid, a random 4-regular graph and a barbell; random simple d-regular
  graphs by stub pairing that avoids loops and repeated edges (after Steger and Wormald); the spectra of Part 18's
  city grid, Part 36's tiered internet and a word co-occurrence graph of one novel; random regular graphs against the
  Ramanujan bound 2√(d − 1), with the expander mixing lemma checked on random pairs of sets; rotation maps and the
  zig-zag product, with its second eigenvalue against the Reingold–Vadhan–Wigderson bound; effective resistance from
  the pseudo-inverse, and commute time 2m R_eff against simulated walks; a Spielman–Srivastava sparsifier (edges
  sampled by weight times resistance and reweighted); and conjugate gradients on an ill-conditioned Laplacian, plain
  and preconditioned by its sparsifier. (The scenes' small illustrative graphs, such as the Petersen graph, the
  circuits, the toy Tanner graph and the flow network, are computed inline with NumPy.)

## Chapters

* **Hook.** Two 16-vertex rings, every vertex with 3 neighbours, one with local chords and one with random chords:
  alike in a drawing, but λ₂ of the normalized Laplacian is 0.097 against 0.279. The same number for the series' own
  graphs: Part 18's city grid (256 vertices, 437 edges, λ₂ = 0.009, best sweep cut 0.038), Part 36's internet (125,
  213, 0.191, 0.198) and the words of a novel (252, 1,346, 0.241, 0.333). The plan, ending at almost-linear max-flow.
* **1. The Laplacian.** L = D − A on a 5-vertex graph (the third vertex's row: 3, and −1 for each neighbour; L𝟏 = 0);
  xᵀLx = Σ (x_i − x_j)² derived as the energy in springs (a smooth labelling stores 7, the same values rearranged
  39); zero energy means constant on components (two hexagons: eigenvalue 0 twice; one bridge: λ₂ = 0.20); λ₂ as
  Fiedler's algebraic connectivity (path 0.15, cycle 0.59, cube Q₃ 2.00, K₈ 8); two planted communities of 60
  (120 vertices, 821 edges: λ₂ = 3.02 stands apart, the bulk starts at λ₃ = 4.60); the normalized Laplacian and the
  series' graphs again.
* **2. Rayleigh quotients and the Fiedler vector.** The Rayleigh quotient as a weighted average of eigenvalues;
  Courant–Fischer (Fischer 1905, Courant 1920), so adding an edge never lowers any λ_k; a cut as a ±1 vector (energy
  4 per cut edge), the NP-hard minimum bisection and its relaxation, bisection ≥ nλ₂/4 (here 12/4 × 0.20 = 0.61 ≤ 1);
  the Fiedler vector drawn as colours, a slow wave on an 8 × 4 grid, Fiedler's 1975 connectivity theorem; on the
  120-vertex graph its signs agree with the planted communities on 100% of the vertices; spectral clustering of three
  pentagon clusters by (v₂, v₃) (eigenvalues 0, 0.40, 0.40, then 2.08); Shi–Malik, Ng–Jordan–Weiss and METIS.
* **3. Cheeger's inequality.** Volume and conductance on a two-bridge graph (cutting off three vertices: 2 edges,
  volume 8, φ = 0.25; between the clusters: 2 edges, volume 18, φ = 0.11); λ₂/2 ≤ φ(G) ≤ √(2λ₂) (Cheeger 1970;
  Dodziuk 1984, Alon and Milman 1985); the easy side proved with one test vector; the hard side proved: shift by the
  weighted median, keep one half, cut at a random threshold on z², Cauchy–Schwarz; the sweep cut (best prefix of the
  toy: the first six; on the 120-vertex graph the curve dips to φ = 0.137 at k = 60, exactly the planted split); 53
  connected random graphs on 12 vertices against brute force over 2,047 cuts: all inside the bounds, the sweep exact in
  32 of 53; tightness (the hypercube, a long cycle).
* **4. Random walks and mixing.** p_{t+1} = p_t D^{−1}A spreading over the two-bridge graph; π = d/2m stationary; the
  8-cycle oscillates, the lazy walk settles; D^{1/2}WD^{−1/2} = I − N/2, so μ₂ = 1 − γ/2 (0.936 on the toy, the
  slowest mode); TV ≤ ½√(1/π_min)(1 − γ/2)^t, so (2/γ − 1) ln 2 ≤ t_mix ≤ (1/γ) ln(4/π_min). Four 64-vertex graphs,
  measured: random 4-regular (gap 0.1654; bounds 8 and 33, t_mix 15), 8 × 8 grid (0.0463; 30 and 131; 51), cycle
  (0.0048; 288 and 1,151; > 300), barbell (993 edges, gap 0.0019; 730 and 2,920; > 300). PageRank revisited: the jump
  bounds |μ₂| by 0.85 (Haveliwala and Kamvar 2003); Part 18's 20,000 pages and 79,990 links converged to 10⁻¹² in 52
  steps, about 0.58 a step.
* **5. Expanders.** Edge, vertex and spectral expansion on the Petersen graph (5 edges leave the outer 5; h = 1 over
  all 637 sets; eigenvalues 3, 1, −2, so λ = 2; Cheeger for degree d: 1 ≤ 1 ≤ 3.46); the expander mixing lemma
  (e(S, T) = 9 against d|S||T|/n = 7.2 on a random 3-regular graph) and its proof; Alon–Boppana by closed walks in the
  tree, and Ramanujan graphs (Lubotzky, Phillips and Sarnak 1988); one random d-regular graph on 400 vertices per
  degree: λ = 2.820, 3.434, 4.424, 5.244, 6.416 against 2√(d − 1) = 2.828, 3.464, 4.472, 5.292, 6.633 for d = 3, 4,
  6, 8, 12, worst mixing-lemma error 0.20 to 0.34; existence by counting and a union bound (Pinsker 1973).
* **6. Explicit expanders: the zig-zag product.** Explicit means a neighbour function in time polynomial in log N;
  Margulis (1973) shear maps on a torus, Gabber–Galil (1981), Lubotzky–Phillips–Sarnak; the product drawn as a step,
  a cloud move and a step (G = K₅, H a 4-cycle: 20 vertices of degree 4); why the gap survives,
  1 − λ_Z ≥ (1 − λ_H)²(1 − λ_G) (after Vadhan); our product (G random 8-regular on 60, H random 3-regular on 8: 480
  vertices of degree 9) measures λ_Z = 0.811 against λ_G = 0.665, λ_H = 0.745, the RVW bound 0.908, the proved bound
  0.978 and λ_G + λ_H + λ_H² = 1.966; the recursion G_{t+1} = G_t² ⓩ H keeping λ ≤ 2/5; Reingold's SL = L (2005).
* **7. Expanders at work.** A walk instead of fresh coins: r + t log₂ D bits; the hitting bound μ(μ + λ)^t (and
  Gillman's Chernoff bound); illustrative savings with r = 256, μ = ½, λ = ¼, degree 2¹⁰: error 2⁻²⁰ for 716 bits (46
  steps) against 5,120; expander codes (Tanner 1981; Sipser and Spielman 1996): unique neighbours on a toy code of 12
  bits and 9 checks (2 bits, 6 edges, 4 unique checks, 1 shared); flip decoding of 2 errors (4 unsatisfied checks, then
  3, then 0); Dinur's gap amplification (Part 27); Jellyfish (2012) and Xpander (2016).
* **8. Graphs as electrical networks.** Ohm and Kirchhoff give Lx = b; one amp through nine one-ohm resistors
  (voltages 1.36 down to 0, 0.45 in = 0.09 + 0.36 out at one vertex); R_eff = bᵀL⁺b (series 2, parallel 0.5, our
  circuit 1.36); Thomson's principle (electrical 1.36, two paths 1.50, one path 3.00) and Rayleigh monotonicity;
  commute time = 2m R_eff derived (Chandra et al. 1989); a 5 × 5 grid corner to corner: m = 40, R_eff = 2.136,
  predicted 170.9, measured 174.0 over 2,000 round trips (1.8% apart); Pólya's walks by shorting shells (8k + 4 edges).
* **9. Laplacian solvers and sparsifiers.** CG sees one hop further per iteration (a 20-vertex path: κ = 161, exact in
  10 steps); preconditioning by a spectral sparsifier: 300 vertices, 13,657 edges, κ = 40.2, a sparsifier of 1,591
  edges with xᵀL_Hx/xᵀL_Gx in [0.965, 1.033] on 200 random x, CG 67 iterations against 14; Foster's theorem (two K₈
  and a bridge: bridge 1.00, clique edges 0.25, 57 edges summing to 15 = n − 1); Spielman–Srivastava sampling (40
  draws keep 27 of 57 edges, the bridge among them; missing it: 6% by resistance, 49% uniformly), Batson–Spielman–
  Srivastava; all resistances by Johnson–Lindenstrauss; low-stretch trees on a 6 × 6 grid (snake: total stretch 210,
  κ = 46.8; spine: 150, κ = 23.2); Spielman–Teng (2004).
* **10. From electrical flows to max-flow.** An 8-vertex network with capacities 1 to 4 and maximum flow 4; the
  electrical flow with r_e = 1/u_e² puts 2.82 on an edge of capacity 2 (congestion 1.41); Thomson's lemma bounds the
  weighted mean of squared congestion by 1 (0.43 here); multiplicative weights over electrical flows (ε = 0.5, 30
  rounds): the averaged flow's worst congestion falls from 1.412 to 1.035, so scaling gives 3.86, 96.6% of the
  maximum (Christiano, Kelner, Mądry, Spielman and Teng 2011); interior points, where every Newton step is an
  electrical flow; min-ratio cycles on low-stretch trees (Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva 2022);
  the exponent of m from 3 (1972) to 1.5 (1998), 4/3 (2011) and 1 + o(1) (2022).
* **11. Frontier: high-dimensional expanders.** Complexes, links and Garland's local-to-global principle; Ramanujan
  complexes; what they have done (matroid bases sampled by Anari, Liu, Oveis Gharan and Vinzant 2019, spectral
  independence, the 2022 locally testable codes and good quantum LDPC codes, Dinur's PCP proof); the random regular
  graphs under 2√(d − 1), Friedman's theorem and Marcus–Spielman–Srivastava's bipartite Ramanujan graphs of every
  degree. Four open problems and the ★ research problem, the small-set expansion hypothesis.
* **Outro.** Recap, payoffs (Parts 57, 58, 59, 60, 61), practice, problems, next part.

## Build

```bash
python -m videos.cs.cs56.compute
python -m unittest tests.test_cs56_spectral
python tools/build.py cs56
```

## Problems, with solutions

1. **The energy.** Show that xᵀLx = Σ_{(i,j)∈E} (x_i − x_j)², and that the multiplicity of the eigenvalue 0 equals
   the number of components.

   *Solution.* With L = D − A, xᵀDx = Σ_i d_i x_i² = Σ_{(i,j)∈E} (x_i² + x_j²), because each edge adds one to the
   degree of each of its ends, and xᵀAx = Σ_{i,j} A_ij x_i x_j = 2 Σ_{(i,j)∈E} x_i x_j, because each edge appears in A
   as (i, j) and as (j, i). Subtracting, xᵀLx = Σ_E (x_i² + x_j² − 2x_i x_j) = Σ_E (x_i − x_j)² ≥ 0. So L is symmetric
   and positive semidefinite, and then xᵀLx = ‖L^{1/2}x‖² vanishes exactly when Lx = 0. The null space of L is
   therefore {x : x_i = x_j across every edge}, the vectors constant on each connected component (a path inside a
   component forces equal values along it). If the components are C₁, …, C_k, their indicator vectors have disjoint
   supports, so they are independent, and they span that space: its dimension is k. Since L is symmetric, the
   algebraic multiplicity of 0 equals the dimension of its eigenspace, k. Chapter 1's two hexagons have the eigenvalue
   0 twice; one bridge leaves it once and lifts the other to λ₂ = 0.20.

2. **Two spectra.** Compute the Laplacian spectrum of the cycle C_n and of the hypercube Q_d.

   *Solution.* Cycle: number the vertices modulo n, so L = 2I − S − S⁻¹ with S the cyclic shift. The vectors
   χ_k(j) = ω^{jk}, ω = e^{2πi/n}, k = 0, …, n − 1, satisfy Sχ_k = ω^k χ_k, so
   Lχ_k = (2 − ω^k − ω^{−k})χ_k = (2 − 2cos(2πk/n))χ_k. The n of them are orthogonal, so this is the whole spectrum:
   2 − 2cos(2πk/n) for k = 0, …, n − 1, with real eigenvectors cos(2πjk/n) and sin(2πjk/n); every eigenvalue other
   than 0 (and 4 when n is even) occurs twice. In particular λ₂ = 2 − 2cos(2π/n) ≈ 4π²/n²; for n = 8 it is
   2 − √2 ≈ 0.586, chapter 1's cycle (the tests check n = 12). Hypercube: the vertices are x ∈ {0, 1}^d, joined when
   they differ in one bit. For S ⊆ {1, …, d} let χ_S(x) = (−1)^{Σ_{i∈S} x_i}. Flipping bit i multiplies χ_S by −1 if
   i ∈ S and by 1 otherwise, so (Aχ_S)(x) = Σ_i χ_S(x ⊕ e_i) = (d − 2|S|)χ_S(x) and Lχ_S = 2|S| χ_S. The 2^d
   characters are orthogonal, so the spectrum is 2k with multiplicity C(d, k), k = 0, …, d: for Q₃, 0, 2, 2, 2, 4, 4,
   4, 6, and λ₂ = 2 as in chapter 1. Both graphs illustrate chapter 3's tightness remarks. Q_d is d-regular, so λ₂ of
   N is 2/d; the half-cube {x₁ = 0} cuts 2^{d−1} edges and has volume d · 2^{d−1}, so φ ≤ 1/d = λ₂/2, and with
   Cheeger's lower bound φ(Q_d) = λ₂/2 exactly. For C_n with n even, λ₂(N) = 1 − cos(2π/n) ≈ 2π²/n², while φ = 2/n
   (every cut crosses at least two edges, and the smaller side has volume at most n): of order √λ₂. For n = 64,
   λ₂(N) = 0.0048 (chapter 4's gap), φ = 0.031 and √(2λ₂) = 0.098.

3. **Cheeger, the easy side.** Prove λ₂/2 ≤ φ(G).

   *Solution.* N = D^{−1/2}LD^{−1/2} has the eigenvalue 0 with eigenvector D^{1/2}𝟏, so by Courant–Fischer λ₂(N) is the
   minimum of xᵀNx/xᵀx over x ≠ 0 orthogonal to D^{1/2}𝟏. Substitute x = D^{1/2}y: the constraint becomes
   Σ_i d_i y_i = 0, the numerator yᵀLy = Σ_E (y_i − y_j)² and the denominator Σ_i d_i y_i². So any such y gives an
   upper bound on λ₂. For a set S, take y = a on S and y = −b off it, with a = 1/vol S and b = 1/vol S̄; then
   Σ_i d_i y_i = 1 − 1 = 0. Only the cut edges have a difference across them, a + b each, so the numerator is
   |E(S, S̄)|(a + b)², and the denominator is vol S · a² + vol S̄ · b² = a + b. Hence
   λ₂ ≤ |E(S, S̄)|(a + b) ≤ 2|E(S, S̄)|/min(vol S, vol S̄) = 2φ(S), since each of a and b is at most one over the
   smaller volume. This holds for every S, so for the best one: λ₂/2 ≤ φ(G). On chapter 3's two-bridge graph,
   λ₂ = 0.129 and φ(G) = 1/9 ≈ 0.111 by brute force over all 2,047 cuts: 0.064 ≤ 0.111 ≤ √(2 × 0.129) = 0.508.

4. **The expander mixing lemma.** Prove |e(S, T) − d|S||T|/n| ≤ λ√(|S||T|).

   *Solution.* Let A be the adjacency matrix of a d-regular graph on n vertices, with eigenvalues d = μ₁ ≥ μ₂ ≥ … ≥ μ_n,
   orthonormal eigenvectors v₁ = 𝟏/√n, v₂, …, v_n, and λ = max_{i≥2} |μ_i|. The count e(S, T) = 𝟏_Sᵀ A 𝟏_T is the number
   of joined pairs (s, t) with s ∈ S and t ∈ T. Write 𝟏_S = (|S|/n)𝟏 + x and 𝟏_T = (|T|/n)𝟏 + y with x, y ⊥ 𝟏 and
   expand. The main term is (|S||T|/n²) 𝟏ᵀA𝟏 = d|S||T|/n, since 𝟏ᵀA𝟏 = dn. The cross terms vanish: A𝟏 = d𝟏, so
   (|S|/n) 𝟏ᵀAy = (|S|/n) d 𝟏ᵀy = 0, and likewise xᵀA𝟏 = 0. So e(S, T) − d|S||T|/n = xᵀAy. Writing
   y = Σ_{i≥2} c_i v_i gives Ay = Σ_{i≥2} μ_i c_i v_i and ‖Ay‖ ≤ λ‖y‖, so by Cauchy–Schwarz |xᵀAy| ≤ λ‖x‖‖y‖. Finally
   ‖x‖² = ‖𝟏_S‖² − |S|²/n = |S|(1 − |S|/n) ≤ |S|, and the same for y, which gives the lemma (and, keeping the factors,
   the sharper λ√(|S|(1 − |S|/n)|T|(1 − |T|/n))). In chapter 5's 20-vertex example e(S, T) = 9 against 7.2; on the
   400-vertex random regular graphs the worst normalized error over 200 random pairs of sets was 0.20 to 0.34, against
   λ from 2.82 to 6.42.

5. **Build.** Build the zig-zag product of two graphs of your choice, and compare its second eigenvalue with the RVW
   bound.

   *Solution notes.* `explainer/cs/spectral/spectra.py` has the pieces. H must have exactly as many vertices as G's
   degree D: take G = `random_regular(N, D, seed)` and H = `random_regular(D, d, seed)`, `cycle(D)` or the complete
   graph on D vertices. `rotation_map_regular` numbers each vertex's neighbours and records, for the edge from v to its
   i-th neighbour w, which neighbour of w the vertex v is; `zigzag(G, H)` adds, for each vertex (v, a) and each pair
   (i, j), the edge made of a zig (a to its i-th neighbour a′ in H), the big step (port a′ of v to port b′ of w) and a
   zag (b′ to its j-th neighbour b in H). Check that Z is symmetric and d²-regular (as `test_zigzag_regular` does),
   then compute each λ as the second largest |eigenvalue| (`np.linalg.eigvalsh`) divided by the degree, and compare
   λ_Z with the RVW bound f(λ_G, λ_H) = ½(1 − λ_H²)λ_G + ½√((1 − λ_H²)²λ_G² + 4λ_H²), with the bound proved in chapter
   6, 1 − (1 − λ_H)²(1 − λ_G), and with λ_G + λ_H + λ_H². `zigzag_experiment` (G random 8-regular on 60, H random
   3-regular on 8) gives 480 vertices of degree 9 and λ_Z = 0.811 against 0.908, 0.978 and 1.966. With the same G and
   H = K₈ (λ_H = 1/7) the product has degree 49 and λ_Z = 0.681, which equals the RVW bound to the digits we printed;
   with G random 5-regular on 60 and H = C₅, λ_Z = 0.932 against 0.957. Two traps: a bipartite H, such as the 4-cycle
   in the test, has λ_H = 1, so every bound is 1, and indeed λ_Z = 1; and Z can have repeated edges and loops, which
   must be kept as multiplicities (the code adds one for each (i, j)). A complete answer also iterates
   G_{t+1} = G_t² ⓩ H and watches the degree stay at d² while λ stays bounded.

6. **★ Research.** The small-set expansion hypothesis.

   *Discussion.* Open. Raghavendra and Steurer (2010) conjectured that for every η > 0 there is a δ > 0 such that it
   is NP-hard to tell a regular graph in which some set of a δ fraction of the volume has conductance at most η from
   one in which every such set has conductance at least 1 − η, and showed that this hypothesis implies the unique
   games conjecture. Spectral methods cannot settle it directly: Cheeger's inequality certifies that some cut is
   cheap, but says nothing about how large its sides are, and a graph can have many eigenvalues near zero while all
   its small sets expand, so the bottom of the spectrum does not reveal small non-expanding sets. The evidence pulls
   both ways. Arora, Barak and Steurer (2010) solve small-set expansion and unique games in subexponential time, exp
   of a power of n that shrinks with η, by exploiting graphs with few small eigenvalues; so, if 3-SAT needs
   exponential time, any reduction that proves the hypothesis must blow instances up by a power that grows as η
   shrinks. On the other side, the 2-to-2 theorem (Khot, Minzer and Safra 2018, with
   Dinur and Kindler) came from proving that the non-expanding small sets of the Grassmann graph have a rigid
   structure. A good partial answer would solve small-set expansion in polynomial time on a natural class of graphs
   beyond those with few small eigenvalues, prove that a fixed level of a hierarchy such as sum-of-squares fails on
   some family of small-set expansion instances, or give a reduction from small-set expansion to a problem not yet
   known to be equivalent to it.

## 习题与解答

1. **能量。** 证明 xᵀLx = Σ_{(i,j)∈E} (x_i − x_j)²，并证明特征值 0 的重数等于连通分量的个数。

   *解答。* 由 L = D − A，xᵀDx = Σ_i d_i x_i² = Σ_{(i,j)∈E} (x_i² + x_j²)，因为每条边给它的两个端点的度各加一；
   xᵀAx = Σ_{i,j} A_ij x_i x_j = 2 Σ_{(i,j)∈E} x_i x_j，因为每条边在 A 中以 (i, j) 和 (j, i) 各出现一次。相减得
   xᵀLx = Σ_E (x_i² + x_j² − 2x_i x_j) = Σ_E (x_i − x_j)² ≥ 0。所以 L 对称半正定，于是 xᵀLx = ‖L^{1/2}x‖² 恰在
   Lx = 0 时为零。因此 L 的零空间是 {x：每条边两端取值相等}，即在每个连通分量上取常数的向量（分量内的一条路径迫使沿途取值
   相等）。若连通分量为 C₁, …, C_k，它们的指示向量支撑集互不相交，因而线性无关，并张成这个空间：维数为 k。L 对称，所以 0
   的代数重数等于其特征空间的维数 k。第 1 章的两个六边形有两个特征值 0；加一座桥后只剩一个，另一个升到 λ₂ = 0.20。

2. **两个谱。** 计算圈 C_n 与超立方体 Q_d 的拉普拉斯谱。

   *解答。* 圈：把顶点按模 n 编号，则 L = 2I − S − S⁻¹，S 为循环移位。向量 χ_k(j) = ω^{jk}（ω = e^{2πi/n}，
   k = 0, …, n − 1）满足 Sχ_k = ω^k χ_k，所以 Lχ_k = (2 − ω^k − ω^{−k})χ_k = (2 − 2cos(2πk/n))χ_k。这 n 个向量两两正交，
   所以这就是全部的谱：2 − 2cos(2πk/n)，k = 0, …, n − 1，实特征向量为 cos(2πjk/n) 与 sin(2πjk/n)；除 0（n 为偶数时还有
   4）以外每个特征值出现两次。特别地 λ₂ = 2 − 2cos(2π/n) ≈ 4π²/n²；n = 8 时为 2 − √2 ≈ 0.586，即第 1 章的圈（测试检查了
   n = 12）。超立方体：顶点为 x ∈ {0, 1}^d，恰差一位的两点相连。对 S ⊆ {1, …, d} 令 χ_S(x) = (−1)^{Σ_{i∈S} x_i}。翻转第 i 位
   时，若 i ∈ S 则 χ_S 乘以 −1，否则不变，所以 (Aχ_S)(x) = Σ_i χ_S(x ⊕ e_i) = (d − 2|S|)χ_S(x)，Lχ_S = 2|S| χ_S。这 2^d
   个向量两两正交，所以谱为 2k，重数 C(d, k)，k = 0, …, d：Q₃ 为 0, 2, 2, 2, 4, 4, 4, 6，λ₂ = 2，与第 1 章一致。这两个图
   也说明了第 3 章关于紧性的话。Q_d 是 d-正则的，所以 N 的 λ₂ 为 2/d；半立方体 {x₁ = 0} 割断 2^{d−1} 条边，体积为
   d · 2^{d−1}，所以 φ ≤ 1/d = λ₂/2，再由 Cheeger 下界得 φ(Q_d) = λ₂/2，恰好取等。n 为偶数时，C_n 的 λ₂(N) =
   1 − cos(2π/n) ≈ 2π²/n²，而 φ = 2/n（每个割至少割断两条边，较小一侧的体积至多为 n）：与 √λ₂ 同阶。n = 64 时
   λ₂(N) = 0.0048（第 4 章的谱间隙），φ = 0.031，√(2λ₂) = 0.098。

3. **Cheeger 不等式的容易一侧。** 证明 λ₂/2 ≤ φ(G)。

   *解答。* N = D^{−1/2}LD^{−1/2} 有特征值 0，特征向量为 D^{1/2}𝟏，所以由 Courant–Fischer 定理，λ₂(N) 是 xᵀNx/xᵀx 在所有
   与 D^{1/2}𝟏 正交的非零 x 上的最小值。代入 x = D^{1/2}y：约束变为 Σ_i d_i y_i = 0，分子为 yᵀLy = Σ_E (y_i − y_j)²，分母为
   Σ_i d_i y_i²。所以任何这样的 y 都给出 λ₂ 的一个上界。对集合 S，令 y 在 S 上为 a、在 S 外为 −b，其中 a = 1/vol S，
   b = 1/vol S̄；则 Σ_i d_i y_i = 1 − 1 = 0。只有被割断的边两端有差，每条差 a + b，所以分子为 |E(S, S̄)|(a + b)²，分母为
   vol S · a² + vol S̄ · b² = a + b。于是 λ₂ ≤ |E(S, S̄)|(a + b) ≤ 2|E(S, S̄)|/min(vol S, vol S̄) = 2φ(S)，因为 a 与 b
   都不超过较小体积的倒数。这对每个 S 都成立，对最好的那个也成立：λ₂/2 ≤ φ(G)。在第 3 章的双桥图上，λ₂ = 0.129，穷举全部
   2,047 个割得 φ(G) = 1/9 ≈ 0.111：0.064 ≤ 0.111 ≤ √(2 × 0.129) = 0.508。

4. **扩展图混合引理。** 证明 |e(S, T) − d|S||T|/n| ≤ λ√(|S||T|)。

   *解答。* 设 A 为 n 个顶点的 d-正则图的邻接矩阵，特征值 d = μ₁ ≥ μ₂ ≥ … ≥ μ_n，标准正交特征向量 v₁ = 𝟏/√n, v₂, …, v_n，
   λ = max_{i≥2} |μ_i|。计数 e(S, T) = 𝟏_Sᵀ A 𝟏_T 是满足 s ∈ S、t ∈ T 且相连的有序对 (s, t) 的个数。写
   𝟏_S = (|S|/n)𝟏 + x，𝟏_T = (|T|/n)𝟏 + y，其中 x, y ⊥ 𝟏，然后展开。主项为 (|S||T|/n²) 𝟏ᵀA𝟏 = d|S||T|/n，因为
   𝟏ᵀA𝟏 = dn。交叉项为零：A𝟏 = d𝟏，所以 (|S|/n) 𝟏ᵀAy = (|S|/n) d 𝟏ᵀy = 0，同理 xᵀA𝟏 = 0。于是
   e(S, T) − d|S||T|/n = xᵀAy。写 y = Σ_{i≥2} c_i v_i，则 Ay = Σ_{i≥2} μ_i c_i v_i，‖Ay‖ ≤ λ‖y‖，由 Cauchy–Schwarz 得
   |xᵀAy| ≤ λ‖x‖‖y‖。最后 ‖x‖² = ‖𝟏_S‖² − |S|²/n = |S|(1 − |S|/n) ≤ |S|，y 同理，引理得证（保留这些因子，还得到更强的
   λ√(|S|(1 − |S|/n)|T|(1 − |T|/n))）。第 5 章 20 个顶点的例子中 e(S, T) = 9，对比 7.2；在 400 个顶点的随机正则图上，200
   对随机集合中归一化误差的最大值在 0.20 到 0.34 之间，而 λ 在 2.82 到 6.42 之间。

5. **动手。** 用你选的两个图构造 zig-zag 积（之字形积），并把它的第二特征值与 RVW 界比较。

   *解答要点。* `explainer/cs/spectral/spectra.py` 里已有所需的部件。H 的顶点数必须等于 G 的度 D：取
   G = `random_regular(N, D, seed)`，H = `random_regular(D, d, seed)`、`cycle(D)` 或 D 个顶点的完全图。
   `rotation_map_regular` 给每个顶点的邻居编号，并对从 v 到它第 i 个邻居 w 的边记下 v 是 w 的第几个邻居；`zigzag(G, H)` 对
   每个顶点 (v, a) 和每一对 (i, j) 加一条边，它由三步组成：zig（在 H 中从 a 走到它的第 i 个邻居 a′）、大步（从 v 的端口 a′
   走到 w 的端口 b′）、zag（在 H 中从 b′ 走到它的第 j 个邻居 b）。检查 Z 对称且是 d²-正则的（如 `test_zigzag_regular`
   所做），然后把每个 λ 算作绝对值第二大的特征值（`np.linalg.eigvalsh`）除以度，把 λ_Z 与 RVW 界
   f(λ_G, λ_H) = ½(1 − λ_H²)λ_G + ½√((1 − λ_H²)²λ_G² + 4λ_H²)、第 6 章证明的界 1 − (1 − λ_H)²(1 − λ_G) 以及
   λ_G + λ_H + λ_H² 比较。`zigzag_experiment`（G 为 60 个顶点的随机 8-正则图，H 为 8 个顶点的随机 3-正则图）给出 480 个
   度为 9 的顶点，λ_Z = 0.811，对比 0.908、0.978 和 1.966。用同一个 G 和 H = K₈（λ_H = 1/7），积的度为 49，λ_Z = 0.681，
   在打印的位数内等于 RVW 界；用 60 个顶点的随机 5-正则图 G 和 H = C₅，λ_Z = 0.932，对比 0.957。两个陷阱：二部图 H（例如测试
   中的 4-圈）的 λ_H = 1，所有界都是 1，而 λ_Z 也确实是 1；Z 可能有重边和自环，必须按重数保留（代码对每个 (i, j) 加一）。
   完整的答案还应迭代 G_{t+1} = G_t² ⓩ H，看度保持为 d²，同时 λ 保持有界。

6. **★ 研究。** 小集合扩张假设。

   *讨论。* 尚未解决。Raghavendra 和 Steurer（2010）猜想：对每个 η > 0 都存在 δ > 0，使得区分下面两种正则图是 NP 难的：
   一种有某个占体积 δ 比例的集合，其导率至多为 η；另一种中每个这样的集合导率都至少为 1 − η。他们还证明了这个假设蕴含唯一
   博弈猜想。谱方法无法直接解决它：Cheeger 不等式保证某个割很便宜，却不说它的两侧有多大；一个图可以有许多接近零的特征值，
   而它所有的小集合都扩张，所以谱的底部看不出不扩张的小集合。证据指向两边。Arora、Barak 和 Steurer（2010）用利用小特征值
   很少的图的方法，在亚指数时间（exp 的指数是 n 的一个随 η 缩小的幂）内求解小集合扩张和唯一博弈；因此，如果 3-SAT 需要指数
   时间，任何证明这个假设的归约都必须把实例规模放大到一个随 η 缩小而增长的幂。另一方面，2-to-2 定理（Khot、Minzer 和 Safra 2018，与 Dinur 和 Kindler 合作）来自证明 Grassmann 图中不
   扩张的小集合具有刚性的结构。好的部分结果可以是：在小特征值很少的图之外的一类自然的图上，用多项式时间求解小集合扩张；证明
   平方和（sum-of-squares）这类层级的某个固定层在某一族小集合扩张实例上失效；或者给出从小集合扩张到某个尚不知与之等价的问题
   的归约。

## Glossary additions

* **Laplacian L = D − A, normalized Laplacian N, quadratic form (energy)** — the matrix whose form is the sum of
  squared differences across the edges; its degree-weighted version, with eigenvalues in [0, 2].
* **algebraic connectivity, Fiedler vector, Fiedler order** — λ₂ of L; its eigenvector; the vertices sorted by it.
* **Rayleigh quotient, Courant–Fischer theorem** — energy over length; eigenvalues as min-max of the quotient.
* **minimum bisection, relaxation, spectral clustering, multilevel partitioning (METIS)** — the best balanced cut;
  allowing real values; clustering points embedded by bottom eigenvectors; coarsen, cut, refine.
* **volume, conductance φ, sweep cut, Cheeger's inequality** — the sum of degrees; cut edges over the smaller volume;
  the best prefix of the Fiedler order; λ₂/2 ≤ φ ≤ √(2λ₂).
* **random walk, stationary distribution, lazy walk, spectral gap γ, total variation, mixing time** — a step to a
  random neighbour; π = d/2m; staying put half the time; λ₂ of N; half the L¹ distance; the first t with TV ≤ ¼.
* **expander (edge, vertex, spectral expansion), expander mixing lemma** — a sparse graph in which every set has many
  edges leaving it; edges between any two sets as in a random graph, up to λ√(|S||T|).
* **Alon–Boppana bound, Ramanujan graph** — λ ≥ 2√(d − 1) − o(1); a graph that meets it.
* **explicit construction, rotation map, zig-zag product, SL = L** — a neighbour function computable in poly(log N);
  edge labels at both ends; a step in a cloud, a step between clouds, a step in a cloud; undirected reachability in
  logarithmic space.
* **expander walk sampling, hitting bound, Tanner graph, unique neighbour, expander code, flip decoding** — reusing
  random bits along a walk; μ(μ + λ)^t; bits joined to the checks they take part in; a check hit once; the code of an
  expanding Tanner graph; flipping bits with mostly unsatisfied checks.
* **gap amplification** — Dinur's rounds that double the fraction of violated constraints.
* **effective resistance, pseudo-inverse L⁺, Thomson's principle, Rayleigh monotonicity** — bᵀL⁺b; the inverse on
  vectors summing to zero; current minimizes energy; lowering a resistance never raises R_eff.
* **hitting time, commute time, Foster's theorem** — expected steps to reach a vertex; there and back, 2m R_eff; the
  edges' resistances sum to n − 1.
* **condition number, preconditioning, spectral sparsifier, stretch, low-stretch spanning tree** — λ_n/λ₂; solving
  with a nearby easier matrix; a sparse H with L_H within 1 ± ε of L_G; an edge's tree-path resistance.
* **congestion, multiplicative weights, electrical flow, log barrier, interior-point method, min-ratio cycle** —
  flow over capacity; raising the cost of overused edges; the flow current takes; −Σ log of the slack; Newton steps
  inside the polytope; the circulation with the best gain per length.
* **high-dimensional expander, link, local-to-global, spectral independence** — a complex whose links all expand; the
  neighbourhood of a vertex as a graph; Garland's principle; a spectral condition for fast-mixing samplers.
* **small-set expansion hypothesis, unique games conjecture, sparsest cut** — that small sets' expansion is hard to
  approximate; Khot's conjecture (Part 27); the cut of least edges per vertex on the smaller side.

## Sources

* D. Spielman, *Spectral and Algebraic Graph Theory* (book draft); F. Chung, *Spectral Graph Theory* (AMS, 1997);
  S. Hoory, N. Linial and A. Wigderson, "Expander graphs and their applications", Bull. AMS 2006; S. Vadhan,
  *Pseudorandomness* (2012); D. Levin, Y. Peres and E. Wilmer, *Markov Chains and Mixing Times* (2009); P. Doyle and
  J. L. Snell, *Random Walks and Electric Networks* (1984).
* M. Fiedler, "Algebraic connectivity of graphs", Czech. Math. J. 1973, and "A property of eigenvectors of
  nonnegative symmetric matrices and its application to graph theory", Czech. Math. J. 1975; E. Fischer (1905) and
  R. Courant (1920) on the min-max principle.
* J. Cheeger, "A lower bound for the smallest eigenvalue of the Laplacian" (1970); J. Dodziuk, "Difference equations,
  isoperimetric inequality and transience of certain random walks", Trans. AMS 1984; N. Alon and V. Milman,
  "λ₁, isoperimetric inequalities for graphs, and superconcentrators", J. Combin. Theory B 1985; N. Alon,
  "Eigenvalues and expanders", Combinatorica 1986; A. Sinclair and M. Jerrum, "Approximate counting, uniform
  generation and rapidly mixing Markov chains", Inform. and Comput. 1989.
* J. Shi and J. Malik, "Normalized cuts and image segmentation", IEEE TPAMI 2000; A. Ng, M. Jordan and Y. Weiss, "On
  spectral clustering: analysis and an algorithm", NIPS 2001; G. Karypis and V. Kumar, "A fast and high quality
  multilevel scheme for partitioning irregular graphs", SIAM J. Sci. Comput. 1998.
* S. Brin and L. Page, "The anatomy of a large-scale hypertextual web search engine", WWW 1998; T. Haveliwala and
  S. Kamvar, "The second eigenvalue of the Google matrix" (2003).
* M. Pinsker, "On the complexity of a concentrator" (1973); G. Margulis, "Explicit constructions of concentrators"
  (1973); O. Gabber and Z. Galil, "Explicit constructions of linear-sized superconcentrators", JCSS 1981;
  A. Lubotzky, R. Phillips and P. Sarnak, "Ramanujan graphs", Combinatorica 1988; J. Friedman, "A proof of Alon's
  second eigenvalue conjecture and related problems", Mem. AMS 2008; A. Marcus, D. Spielman and N. Srivastava,
  "Interlacing families I: bipartite Ramanujan graphs of all degrees" and "Interlacing families II: mixed
  characteristic polynomials and the Kadison–Singer problem", Ann. of Math. 2015.
* O. Reingold, S. Vadhan and A. Wigderson, "Entropy waves, the zig-zag graph product, and new constant-degree
  expanders and extractors", FOCS 2000 (Ann. of Math. 2002); O. Reingold, "Undirected ST-connectivity in log-space",
  STOC 2005; R. Aleliunas, R. Karp, R. Lipton, L. Lovász and C. Rackoff, "Random walks, universal traversal sequences,
  and the complexity of maze problems", FOCS 1979.
* R. M. Tanner, "A recursive approach to low complexity codes", IEEE Trans. Inf. Theory 1981; M. Sipser and
  D. Spielman, "Expander codes", IEEE Trans. Inf. Theory 1996; D. Gillman, "A Chernoff bound for random walks on
  expander graphs", SIAM J. Comput. 1998; I. Dinur, "The PCP theorem by gap amplification", STOC 2006 (JACM 2007).
* A. Singla, C.-Y. Hong, L. Popa and P. B. Godfrey, "Jellyfish: networking data centers randomly", NSDI 2012;
  A. Valadarsky, G. Shahaf, M. Dinitz and M. Schapira, "Xpander: towards optimal-performance datacenters", CoNEXT
  2016.
* A. Chandra, P. Raghavan, W. Ruzzo, R. Smolensky and P. Tiwari, "The electrical resistance of a graph captures its
  commute and cover times", STOC 1989; R. Foster, on the average impedance of an electrical network (1949);
  G. Pólya, on random walks in a street network, Math. Ann. 1921.
* D. Spielman and S.-H. Teng, "Nearly-linear time algorithms for graph partitioning, graph sparsification, and
  solving linear systems", STOC 2004; D. Spielman and N. Srivastava, "Graph sparsification by effective
  resistances", STOC 2008; J. Batson, D. Spielman and N. Srivastava, "Twice-Ramanujan sparsifiers", STOC 2009.
* J. Edmonds and R. Karp, "Theoretical improvements in algorithmic efficiency for network flow problems", JACM 1972;
  A. Goldberg and S. Rao, "Beyond the flow decomposition barrier", JACM 1998; P. Christiano, J. Kelner, A. Mądry,
  D. Spielman and S.-H. Teng, "Electrical flows, Laplacian systems, and faster approximation of maximum flow in
  undirected graphs", STOC 2011; L. Chen, R. Kyng, Y. Liu, R. Peng, M. Probst Gutenberg and S. Sachdeva, "Maximum
  flow and minimum-cost flow in almost-linear time", FOCS 2022.
* H. Garland, "p-adic curvature and the cohomology of discrete subgroups of p-adic groups", Ann. of Math. 1973;
  A. Lubotzky, B. Samuels and U. Vishne on Ramanujan complexes (2005); N. Anari, K. Liu, S. Oveis Gharan and
  C. Vinzant, "Log-concave polynomials II: high-dimensional walks and an FPRAS for counting bases of a matroid", STOC
  2019; N. Anari, K. Liu and S. Oveis Gharan, "Spectral independence in high-dimensional expanders and applications
  to the hardcore model", FOCS 2020; I. Dinur, S. Evra, R. Livne, A. Lubotzky and S. Mozes, "Locally testable codes
  with constant rate, distance, and locality", STOC 2022; P. Panteleev and G. Kalachev, "Asymptotically good quantum
  and locally testable classical LDPC codes", STOC 2022.
* S. Arora, S. Rao and U. Vazirani, "Expander flows, geometric embeddings and graph partitioning", STOC 2004;
  P. Raghavendra and D. Steurer, "Graph expansion and the unique games conjecture", STOC 2010; S. Arora, B. Barak and
  D. Steurer, "Subexponential algorithms for unique games and related problems", FOCS 2010; S. Khot, D. Minzer and
  M. Safra, "Pseudorandom sets in Grassmann graph have near-perfect expansion", FOCS 2018.
