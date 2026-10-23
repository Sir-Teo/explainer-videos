# AI, Built — Part 25: Symmetry and Science

Part 25 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the last part of Act IV, *Generation and Perception*. What a network gains by
knowing the symmetries of its problem, and what that did for science: groups, invariance and equivariance; functions of
sets; graph networks, the Weisfeiler–Leman limit of message passing, over-smoothing and attention; networks that turn
with the molecule; the protein-folding problem from Anfinsen and CASP to AlphaFold 2 and 3 and protein design; weather
on a mesh (GraphCast, GenCast, ECMWF's AIFS); neural operators; materials by the million (GNoME); and mathematics, from
AlphaGeometry and proofs in Lean to discovery by search (FunSearch, AlphaEvolve) and the 2025–26 frontier. Every
experiment runs on the computer that renders the video (`compute.py`), on synthetic data; numbers about the large
systems are the published ones, cited on screen.

* **Hook: turn the molecule.** The 2024 Nobel Prize in Chemistry (Baker; Hassabis and Jumper) and in Physics
  (Hopfield, Hinton); five charged particles turned through a full circle while three trained networks predict their
  energy: a plain MLP's answer swings, the MLP trained on turned copies swings less, a network built on distances does
  not move; the question; four domains; the plan.
* **1. How we got here.** The long prelude: ENIAC's forecast (1950), Kendrew's myoglobin (1958), Anfinsen (1961),
  Weisfeiler–Leman (1968), the Protein Data Bank (1971, seven structures), ECMWF's first forecast (1979), convolutions
  (1989, Part 10), CASP (1994), the graph neural network (Gori, Monfardini & Scarselli 2005); the decade: message
  passing, Deep Sets and SchNet (2017), AlphaFold at CASP13 (2018) and CASP14 (2020), EGNN and neural operators (2021),
  200 million predicted structures (2022), GraphCast, GNoME, RFdiffusion and FunSearch (2023), the Nobel, AlphaFold 3,
  AlphaGeometry and AlphaProof (2024), operational AI forecasts, AlphaEvolve and olympiad gold (2025), Erdős problems
  resolved by AI (2026); the recipe (find what doesn't matter, build it in) as a table from images to fields, and
  geometric deep learning (Bronstein, Bruna, Cohen & Veličković 2021); three ways to get a symmetry.
* **2. Invariance and equivariance.** Groups (the square's four turns, 16! orderings, SO(3), shifts); invariance
  f(g·x) = f(x) and equivariance f(g·x) = g·f(x) as a commutative diagram on our five particles; group averaging
  (the Reynolds operator) derived step by step, and its price; augmentation as its cheap version; the check, computed:
  four trained networks (EGNN, a message-passing network on raw coordinates, an MLP, the MLP on turned copies) given
  turned, shifted and reordered inputs, with the error of each against its own test error.
* **3. Functions of sets.** Sixteen points from four shapes; what an MLP sees, and how a renumbering changes it; the
  Deep Sets theorem (Zaheer et al. 2017) with the base-4 proof, power sums and Newton's identities, Wagstaff et al.
  (2019); φ shared across elements, a sum, ρ; PointNet (Qi et al. 2017); attention without positions as an equivariant
  set function; Deep Sets against an MLP and an MLP shown reordered copies, 32 to 8,192 training sets, three seeds,
  the same steps: accuracy and how often a reordering changes the answer.
* **4. Message passing.** Graphs and adjacency matrices; permutation equivariance f(PX, PAPᵀ) = P f(X, A); the MPNN
  framework (Gilmer et al. 2017: QM9, 134,000 molecules, chemical accuracy on 11 of 13 properties) and the GCN (Kipf &
  Welling 2017); the history (Sperduti & Starita 1997; Gori et al. 2005; Scarselli et al. 2009; Bruna et al. 2014;
  Defferrard et al. 2016; Duvenaud et al. 2015; Battaglia et al. 2018); a two-layer GCN on a three-community graph with
  60 labelled nodes, replayed (its guesses for every node at eight checkpoints), against an MLP on the nodes' own hints,
  three seeds.
* **5. What message passing can't see.** Colour refinement (1-WL; Weisfeiler & Leman 1968) run on decalin and
  bicyclopentyl, which it cannot tell apart; the theorem MPNN ≤ 1-WL (Xu, Hu, Leskovec & Jegelka 2019; Morris et al.
  2019) proved by induction, and GIN; sum against mean and max aggregation (node degrees from identical features,
  three seeds); unions of cycles and "is there a triangle?": GIN's outputs identical for every graph (the base rate),
  GIN with random node features (Sato et al. 2021; Abboud et al. 2021), a network on pairs of nodes (Maron et al. 2019);
  1-WL on random graphs and on random 3-regular graphs; k-WL, subgraph counts, positional encodings, graph
  transformers; Babai (2016).
* **6. Deep graph networks.** Over-smoothing (Li, Han & Wu 2018; Oono & Suzuki 2020) derived from the spectrum of
  D^{-1/2}(A + I)D^{-1/2}; the Dirichlet energy under repeated averaging against λ₂^{2k}, and the nodes' features
  collapsing (computed); plain and residual GCNs from 2 to 64 layers, three seeds; over-squashing (Alon & Yahav 2021;
  Topping et al. 2022); graph attention (Veličković et al. 2018) and GATv2 (Brody, Alon & Yahav 2022); a transformer
  as attention on the complete graph; graph transformers; the Evoformer as attention on pairs.
* **7. Networks that turn with the molecule.** E(3); the gradient of an invariant energy is an equivariant force,
  derived; SchNet (Schütt et al. 2017); EGNN (Satorras, Hoogeboom & Welling 2021) with its equivariance proved line by
  line; spherical harmonics and the block-diagonal action of a rotation on degrees 0, 1, 2 (computed), Clebsch–Gordan
  products, tensor field networks (Thomas et al. 2018), NequIP (Batzner et al. 2022), MACE (Batatia et al. 2022);
  the charged five-body system (after Kipf et al. 2018 and Satorras et al. 2021): EGNN, a plain GNN, an MLP and the MLP
  on turned copies, 100 to 3,000 training systems, three seeds, 3,000 steps each; the training of EGNN and the MLP
  replayed on one test system.
* **8. The protein-folding problem.** Amino acids and folds; Kendrew and Perutz; the PDB (seven structures in 1971,
  more than 250,000 in 2026); Anfinsen's ribonuclease (1961); Levinthal's argument (1969) as arithmetic; CASP (Moult &
  Fidelis, 1994) and GDT_TS; co-evolution (Marks et al. 2011; Morcos et al. 2011); AlphaFold at CASP13 (Senior et al.
  2020: 24 of 43 hard domains at TM ≥ 0.7, against 14); classical MDS (Torgerson 1952) recovering a three-helix bundle
  from its distances, up to a mirror image; gradient descent on noisy partial distances from twelve random starts,
  replayed: some land on the fold, the rest on its mirror image.
* **9. AlphaFold 2: the Evoformer.** The architecture (Jumper et al. 2021): MSA and templates, 48 Evoformer blocks, the
  structure module, recycling; row attention with pair bias, column attention, the outer-product mean; the triangle
  inequality and the triangle multiplicative updates (outgoing, incoming) and triangle attention; the link to chapter
  5's pair network; completing a distance matrix from a quarter of the pairs, per-pair updates against triangle updates
  of the same size and training, three seeds (with a separation-only baseline and the rate of triangle-inequality
  violations); CASP14 (median GDT 92.4 overall, 87.0 on the hardest; 0.96 Å backbone r.m.s.d.₉₅ against 2.8 Å; Moult's
  words).
* **10. AlphaFold 2: frames, FAPE and recycling.** Residues as rigid frames, the residue gas, invariant point attention
  and why it is invariant; FAPE derived (clamp and length scale 10 Å), invariant to rigid motions but not to
  reflections; FAPE against distance RMSD on our bundle's mirror image, on a structure with every atom moved 1 Å, and on
  chapter 8's twelve folds; recycling (a random number of passes in training, gradients through the last) added to
  chapter 9's model; July 2021 (code; RoseTTAFold, Baek et al.), the AlphaFold Protein Structure Database (214,684,311
  entries in 2022), pLDDT, the limits.
* **11. AlphaFold 3: diffusion over atoms.** Abramson et al. (2024): proteins, nucleic acids, ligands, ions; a 4-block
  MSA module and the 48-block Pairformer; a diffusion module on raw atom coordinates with "no invariance or
  equivariance … required", random rotations and translations instead, and cross-distillation against hallucination;
  the question tested on a toy: an E(2)-equivariant denoiser against a plain MLP on randomly turned chains, the same
  steps, two seeds (bond lengths, clashes, novelty against the training set); PoseBusters ("50% more accurate than the
  best traditional methods"), the AlphaFold Server, code for academics (November 2024), Chai-1, Boltz-1, Protenix,
  Boltz-2, OpenFold3, Isomorphic Labs' IsoDDE (February 2026).
* **12. Designing proteins.** The inverse problem; Top7 (Kuhlman et al. 2003) and Rosetta; ProteinMPNN (Dauparas et al.
  2022: 52.4% native sequence recovery against 32.9% for Rosetta); RFdiffusion (Watson et al. 2023: RoseTTAFold
  fine-tuned to denoise frames, 200 steps; binders 19% experimental success, about two orders of magnitude over the
  Rosetta-based rate; a haemagglutinin binder 0.63 Å from its design) and the pipeline (eight ProteinMPNN sequences,
  the AlphaFold 2 filter, pAE < 5, RMSD < 2 Å); our toy denoiser's training replayed (samples from fixed noise at six
  checkpoints); AlphaProteo, BindCraft, ESM3 (2024), RFdiffusion3, BoltzGen (2025); the Responsible AI x Biodesign
  commitments (2024).
* **13. Weather on a mesh.** Bjerknes (1904), Richardson (1922), Charney, Fjørtoft & von Neumann (1950), ECMWF (1979),
  a day of skill per decade (Bauer, Thorpe & Brunet 2015); GraphCast (Lam et al. 2023): 0.25° grid, 227 variables, the
  multimesh (40,962 nodes, 327,660 edges), 16 processor layers, 36.7 million parameters, 39 years of ERA5, four weeks on
  32 TPU v4, 90% of 1,380 targets against HRES, rollouts of up to 12 steps in training; our toy atmosphere (forced,
  damped vorticity on a 32 × 32 periodic square) and an encode–process–decode mesh network with a three-level
  multimesh, against the same network on the finest edges only, persistence and climatology, over 40 steps; GenCast
  (Price et al. 2024: 97.2% of 1,320 targets against ENS, 99.8% beyond 36 hours); AIFS Single operational on 25 February
  2025 and AIFS ENS on 1 July 2025, both upgraded on 12 May 2026; WeatherNext 2 (November 2025); NOAA's AI global models
  (17 December 2025).
* **14. Neural operators.** Burgers' equation; operators against fixed grids; Chen & Chen (1995), DeepONet (Lu et al.
  2021), the Fourier neural operator (Li et al. 2021) derived from a kernel integral and the convolution theorem;
  weights on frequencies, shift equivariance, O(n log n); an FNO trained here at 64 points, replayed, and tested from 32
  to 1,024 points against a CNN of the same layout, three seeds; FourCastNet (Pathak et al. 2022).
* **15. Materials by the million.** Crystals, the 230 space groups, DFT (Kohn & Sham 1965), stability as the lower
  convex hull; GNoME (Merchant et al. 2023): about 48,000 stable crystals known computationally before, 2.2 million
  stable against previous work, 381,000 on the updated hull, hit rates above 80% (structure) and 33% (composition)
  against about 1%, 736 independently realized; the active-learning flywheel run on a made-up chemistry of 6,840
  candidates, against random picks, three seeds; Cheetham & Seshadri (2024); the A-Lab (Szymanski et al. 2023), its
  critique (Leeman et al. 2024) and its 2026 correction (36 compounds of 57 targets); MACE-MP-0, MatterGen.
* **16. Geometry and proofs.** Lean and Mathlib (291,099 theorems, 139,563 definitions, 772 contributors, October
  2026); Appel & Haken (1976), Gonthier (2005), Flyspeck (2014), the Liquid Tensor Experiment (2022); AlphaGeometry
  (Trinh et al. 2024: 100 million synthetic theorems, 9% with auxiliary constructions, a 151-million-parameter language
  model; IMO-AG-30: 25 against Wu's method 10, DD+AR 14, GPT-4 0; average gold medallist 25.9) and AlphaGeometry 2
  (Chervonyi et al. 2025: 84% of IMO geometry 2000–2024); IMO 2024 (AlphaProof and AlphaGeometry 2, 28 of 42), IMO 2025
  (Gemini Deep Think and OpenAI's model, 35), IMO 2026 (Huawei's Celia and Xiaohongshu's dots-note-3.0 reported 42 of
  42, solutions submitted to the organizers for grading; AFP, 23 July 2026), the details in Part 28; Gauss (Math Inc.,
  September 2025: the strong prime number theorem in Lean); Erdős problem #728 (January 2026: GPT-5.2 Pro and
  Aristotle, a Lean proof); Feng et al. (2026: 700 open Erdős problems, 13 addressed, 5 by seemingly new arguments).
* **17. Discovery by search.** Propose, evaluate exactly, keep the best; AlphaTensor (Part 26); FunSearch
  (Romera-Paredes et al. 2024: a cap set of 512 in dimension 8, up from 496); online bin packing with an evolutionary
  search over priority functions (random mutations standing in for the language model), against first fit and best
  fit, two seeds, on held-out sequences; Sim, Renau & Hart (2025); matrix multiplication as a tensor and its rank;
  Strassen (1969) and Winograd (1971); our alternating-least-squares search for 2 × 2 decompositions at ranks 6, 7 and 8
  from 30 random starts each; AlphaEvolve (Novikov et al. 2025): 4 × 4 complex matrices in 48 multiplications, the
  kissing number in 11 dimensions (593), more than 50 problems (75% matched, 20% improved), 0.7% of Google's compute, a
  23% kernel speed-up and 1% of Gemini's training time; Dumas, Pernet & Sedoglavic (2025): 48 over the rationals;
  Georgiev, Gómez-Serrano, Tao & Wagner (2025): 67 problems.
* **Recap** in twelve pictures from the part's own results, where it comes back (Parts 26, 28, 29, 30, 31), six
  problems, Part 26's teaser, references.

## Running it

From the repo root:

```
python tools/make.py ai25                       # everything: the computations, then English and Chinese
python -m videos.ai.ai25.compute                # only the numbers (every experiment; resumable)
python -m videos.ai.ai25.compute nbody --force  # one item again
python tools/build.py ai25                      # English
python tools/build.py ai25 --lang zh            # Chinese
```

Everything is seeded (numpy `default_rng` and `torch.manual_seed`, one generator per run, including the initial
weights) and runs on one torch thread (`AI25_THREADS` to change it); there is no multiprocessing. Every item made of
several runs saves each run as it finishes (`CACHE.partial`), so an interrupted computation resumes; trained weights
go to `.cache/ai25/models/`, and an item that needs them (`equivariance`, the examples in `deepsets` and `pair`) trains
them again if they are missing. Nothing is downloaded: every dataset is synthetic. No other part's results are used.
On a busy 4-core machine the whole part computes in about two and a half hours of wall time; the longest items are
`nbody` (48 runs, EGNN about 1.5 minutes each), `pair`, `weather`, `fno` and `diffusion`.

## Results on this machine

RESULTS

## References

Books: M. M. Bronstein, J. Bruna, T. Cohen & P. Veličković, *Geometric Deep Learning: Grids, Groups, Graphs,
Geodesics, and Gauges* (2021); W. L. Hamilton, *Graph Representation Learning* (2020); S. J. D. Prince, *Understanding
Deep Learning* (2023), ch. 13; P. Lynch, *The Emergence of Numerical Weather Prediction: Richardson's Dream* (2006).

Symmetry, sets and graphs: B. Weisfeiler & A. Leman, *A reduction of a graph to a canonical form and an algebra arising
during this reduction* (1968); L. Babai, *Graph isomorphism in quasipolynomial time* (2016); M. Zaheer et al., *Deep
Sets* (NeurIPS 2017); C. R. Qi et al., *PointNet* (CVPR 2017); E. Wagstaff et al., *On the limitations of representing
functions on sets* (ICML 2019); A. Sperduti & A. Starita, *Supervised neural networks for the classification of
structures* (1997); M. Gori, G. Monfardini & F. Scarselli, *A new model for learning in graph domains* (2005); F.
Scarselli et al., *The graph neural network model* (2009); J. Bruna et al., *Spectral networks and locally connected
networks on graphs* (2014); M. Defferrard et al. (2016); D. Duvenaud et al., *Convolutional networks on graphs for
learning molecular fingerprints* (2015); T. Kipf & M. Welling, *Semi-supervised classification with graph convolutional
networks* (ICLR 2017); J. Gilmer et al., *Neural message passing for quantum chemistry* (ICML 2017); P. Battaglia et
al., *Relational inductive biases, deep learning, and graph networks* (2018); K. Xu, W. Hu, J. Leskovec & S. Jegelka,
*How powerful are graph neural networks?* (ICLR 2019); C. Morris et al., *Weisfeiler and Leman go neural* (AAAI 2019);
H. Maron et al., *Provably powerful graph networks* (NeurIPS 2019); R. Sato, M. Yamada & H. Kashima, *Random features
strengthen graph neural networks* (2021); R. Abboud et al. (IJCAI 2021); Q. Li, Z. Han & X.-M. Wu (AAAI 2018); K. Oono
& T. Suzuki, *Graph neural networks exponentially lose expressive power for node classification* (ICLR 2020); U. Alon &
E. Yahav, *On the bottleneck of graph neural networks* (ICLR 2021); J. Topping et al., *Understanding over-squashing
and bottlenecks on graphs via curvature* (ICLR 2022); P. Veličković et al., *Graph attention networks* (ICLR 2018); S.
Brody, U. Alon & E. Yahav, *How attentive are graph attention networks?* (ICLR 2022).

Geometry: K. T. Schütt et al., *SchNet* (2017); N. Thomas et al., *Tensor field networks* (2018); V. G. Satorras, E.
Hoogeboom & M. Welling, *E(n) equivariant graph neural networks* (ICML 2021); S. Batzner et al., *E(3)-equivariant
graph neural networks for data-efficient and accurate interatomic potentials* (Nat. Commun. 2022); I. Batatia et al.,
*MACE* (NeurIPS 2022); T. Kipf et al., *Neural relational inference* (ICML 2018).

Proteins: J. C. Kendrew et al. (Nature 1958); C. B. Anfinsen et al. (PNAS 1961), C. B. Anfinsen, *Principles that
govern the folding of protein chains* (Science 1973); C. Levinthal, *How to fold graciously* (1969); W. S. Torgerson
(1952); J. Moult et al., *A large-scale experiment to assess protein structure prediction methods* (1995); D. S. Marks
et al. (PLoS One 2011); F. Morcos et al. (PNAS 2011); A. W. Senior et al., *Improved protein structure prediction
using potentials from deep learning* (Nature 2020); J. Jumper et al., *Highly accurate protein structure prediction
with AlphaFold* (Nature 2021) and its supplementary information; M. Baek et al., *RoseTTAFold* (Science 2021); M.
Varadi et al., *AlphaFold Protein Structure Database* (2022); J. Abramson et al., *Accurate structure prediction of
biomolecular interactions with AlphaFold 3* (Nature 2024); Google DeepMind & Isomorphic Labs, AlphaFold 3 announcement
(8 May 2024); Isomorphic Labs, *IsoDDE* technical report (10 February 2026); B. Kuhlman et al., *Design of a novel
globular protein fold with atomic-level accuracy* (Science 2003); J. Dauparas et al., *Robust deep learning–based
protein sequence design using ProteinMPNN* (Science 2022); J. L. Watson et al., *De novo design of protein structure
and function with RFdiffusion* (Nature 2023); R. Krishna et al., RFdiffusion3 (bioRxiv 2025); The Royal Swedish
Academy of Sciences, the Nobel Prize in Chemistry 2024.

Weather and operators: L. F. Richardson, *Weather Prediction by Numerical Process* (1922); J. G. Charney, R. Fjørtoft &
J. von Neumann, *Numerical integration of the barotropic vorticity equation* (1950); P. Bauer, A. Thorpe & G. Brunet,
*The quiet revolution of numerical weather prediction* (Nature 2015); R. Lam et al., *Learning skillful medium-range
global weather forecasting* (Science 2023); I. Price et al., *Probabilistic weather forecasting with machine learning*
(Nature 2024/25); S. Lang et al., *AIFS — ECMWF's data-driven forecasting system* (2024); ECMWF, AIFS operational
notes (2025, 2026); NOAA, AI-driven global models (17 December 2025); T. Chen & H. Chen (1995); L. Lu et al.,
*DeepONet* (Nat. Mach. Intell. 2021); Z. Li et al., *Fourier neural operator for parametric partial differential
equations* (ICLR 2021); J. Pathak et al., *FourCastNet* (2022).

Materials: W. Kohn & L. J. Sham (1965); A. Jain et al., *The Materials Project* (2013); A. Merchant et al., *Scaling
deep learning for materials discovery* (Nature 2023); A. K. Cheetham & R. Seshadri, *Artificial intelligence driving
materials discovery? Perspective on the article: Scaling deep learning for materials discovery* (Chem. Mater. 2024);
N. J. Szymanski et al., *An autonomous laboratory for the accelerated synthesis of novel materials* (Nature 2023;
corrected 2026); J. Leeman et al., *Challenges in high-throughput inorganic material prediction and autonomous
synthesis* (PRX Energy 2024); I. Batatia et al., *A foundation model for atomistic materials chemistry* (2023); C. Zeni
et al., *MatterGen* (Nature 2025).

Mathematics: K. Appel & W. Haken (1976); G. Gonthier (2005/2008); T. Hales et al., *A formal proof of the Kepler
conjecture* (2017); the Liquid Tensor Experiment (2022); Mathlib statistics (leanprover-community.github.io, October
2026); T. H. Trinh et al., *Solving olympiad geometry without human demonstrations* (Nature 2024); Y. Chervonyi et al.,
*Gold-medalist performance in solving olympiad geometry with AlphaGeometry2* (2025); T. Hubert et al., AlphaProof
(Nature 2025); AFP, *AI catches up with humans to score 100% at top maths contest* (23 July 2026); Math Inc., Gauss
(2025); N. Sothanaphan, *Resolution of Erdős problem #728* (2026); T. Feng et al., *Semi-autonomous mathematics
discovery with Gemini: a case study on the Erdős problems* (2026); B. Romera-Paredes et al., *Mathematical discoveries
from program search with large language models* (Nature 2024); K. Sim, Q. Renau & E. Hart, *Beyond the hype:
benchmarking LLM-evolved heuristics for bin packing* (2025); V. Strassen (1969); S. Winograd (1971); A. Fawzi et al.,
AlphaTensor (Nature 2022); A. Novikov et al., *AlphaEvolve* (2025); J.-G. Dumas, C. Pernet & A. Sedoglavic, *A
non-commutative algorithm for multiplying 4 × 4 matrices using 48 non-complex multiplications* (2025); B. Georgiev, J.
Gómez-Serrano, T. Tao & A. Z. Wagner, *Mathematical exploration and discovery at scale* (2025).

## Problems, with solutions

**1. Compositions.** Show that a composition of G-equivariant maps is G-equivariant, and that an invariant map applied
after equivariant layers makes the whole network invariant.

*Solution.* If f(g·x) = g·f(x) and h(g·y) = g·h(y), then h(f(g·x)) = h(g·f(x)) = g·h(f(x)): the composition is
equivariant (the actions on the intermediate spaces may differ; only consistency between consecutive layers matters).
If the last map r is invariant, r(g·y) = r(y), then r(h(f(g·x))) = r(g·h(f(x))) = r(h(f(x))). This is why equivariant
networks keep their layers equivariant and only make the read-out invariant (a sum over particles, a norm): an
invariant layer in the middle would throw away the information about orientation that later layers might need.

**2. Deep Sets.** Number a countable universe by c(x) ∈ {1, 2, …}. Show that X ↦ Σ_{x∈X} 4^{−c(x)} is one-to-one on
finite sets. What goes wrong for multisets, and how does a larger base fix it?

*Solution.* Write S(X) = Σ 4^{−c(x)} in base 4: its k-th digit after the point is 1 if the element numbered k is in X
and 0 otherwise. A finite sum of distinct powers of 4^{−1} with coefficients 0 or 1 never carries (each digit is at most
1 < 3), and a terminating base-4 expansion is unique, so S(X) = S(Y) forces the same digits, X = Y. For a multiset,
the coefficient of 4^{−k} is the multiplicity m_k; as long as every m_k ≤ 3 the digits are still read off uniquely,
but a multiplicity of 4 carries into the next place (4·4^{−k} = 4^{−(k−1)}), and then {x_k, x_k, x_k, x_k} and {x_{k−1}}
collide. In base b, multiplicities below b are safe; for bounded multisets choose b larger than the largest multiplicity
(GIN's injectivity lemma uses the same idea).

**3. Regular graphs.** Show that colour refinement gives every node of a d-regular graph the same colour at every
round, and conclude that no message-passing network can tell a 6-cycle from two triangles.

*Solution.* By induction: at round 0 all colours are equal. If all nodes share one colour c at round t, every node's
signature at round t + 1 is (c, the multiset {c, …, c} of size d), the same for every node, so all nodes again share a
colour. Two d-regular graphs with the same number of nodes therefore have identical colour histograms at every round.
C₆ and 2C₃ are both 2-regular on 6 nodes, so 1-WL cannot separate them; by the theorem of chapter 5 (an MPNN's states
are functions of the WL colours) every message-passing network gives every node of both graphs the same state, hence
the same sum read-out. Yet one has triangles and the other doesn't.

**4. Over-smoothing.** For a connected graph, show that Â = D^{−1/2}(A + I)D^{−1/2} has top eigenvalue 1 with eigenvector
∝ D^{1/2}𝟏, and that Â^k X converges to the projection of X onto it.

*Solution.* Here D is the degree matrix of A + I. Â·D^{1/2}𝟏 = D^{−1/2}(A + I)𝟏 = D^{−1/2}D𝟏 = D^{1/2}𝟏, so D^{1/2}𝟏 is an
eigenvector with eigenvalue 1. Â is similar to the random-walk matrix P = D^{−1}(A + I) (Â = D^{1/2} P D^{−1/2}), which
is stochastic, so every eigenvalue has |λ| ≤ 1. For a connected graph, P is irreducible, and the self-loops make it
aperiodic, so by Perron–Frobenius λ = 1 is simple and every other eigenvalue has |λ| < 1. With Â = Σ λ_i u_i u_iᵀ
(orthonormal, Â symmetric), Â^k X = u₁u₁ᵀX + Σ_{i≥2} λ_i^k u_i u_iᵀ X, and the second term is at most |λ₂|^k ‖X‖. Each
column of the limit is a multiple of D^{1/2}𝟏: every node's feature is fixed by its degree, and the information that
told the nodes apart is gone.

**5. EGNN.** Show that x_i′ = x_i + C Σ_j (x_i − x_j) φ(‖x_i − x_j‖²) satisfies x′(Rx + t) = R x′(x) + t for every
orthogonal R. Is it then blind to reflections?

*Solution.* Put y_i = Rx_i + t. Then y_i − y_j = R(x_i − x_j) and ‖y_i − y_j‖ = ‖x_i − x_j‖ because R is orthogonal, so
every φ is unchanged and y_i′ = Rx_i + t + C Σ_j R(x_i − x_j) φ(·) = R x_i′ + t. Nothing used det R = +1, so the layer
is equivariant to reflections too (E(n), not just SE(n)), and any invariant read-out gives a molecule and its mirror
image the same value: such a network can't tell enantiomers apart from positions alone. When chirality matters, as in
proteins, one adds a pseudoscalar (a triple product (x_j − x_i)·((x_k − x_i) × (x_l − x_i)), which changes sign under
reflection) or, as AlphaFold 2 does, works with right-handed frames and a loss such as FAPE.

**6. The Fourier layer.** Show that v ↦ F^{−1}[R_k v̂_k] commutes with shifts of the periodic grid, and that the same R_k
define the layer on any grid with more than 2k_max points.

*Solution.* Shift by s grid points: (τ_s v)_n = v_{n−s}. Its discrete Fourier coefficients are (τ_s v)^_k = e^{−2πiks/N}
v̂_k. Multiplying by R_k and inverting gives F^{−1}[R_k e^{−2πiks/N} v̂_k] = τ_s F^{−1}[R_k v̂_k]: the phase factor is
exactly a shift. (A shift of the continuous variable by any amount acts the same way on the Fourier series, so the
operator commutes with all shifts of the circle.) The weights R_k are indexed by frequency k = 0, …, k_max − 1, not by
grid point. A grid of N points represents the frequencies |k| < N/2, so for N > 2k_max every learned frequency exists
on it and the layer is defined by the same numbers: sample the input on the new grid, transform, multiply the same
modes, transform back. What does change with N is aliasing in the pointwise nonlinearities between Fourier layers,
which is why the error is not exactly constant across resolutions.

## 习题与解答

**1. 复合。** 证明G-等变映射的复合仍是G-等变的；并证明在等变层之后接一个不变映射，整个网络就是不变的。

*解答。* 若f(g·x) = g·f(x)且h(g·y) = g·h(y)，则h(f(g·x)) = h(g·f(x)) = g·h(f(x))：复合是等变的（中间空间上的作用可以不同，只要相邻
两层一致）。若最后一个映射r不变，r(g·y) = r(y)，则r(h(f(g·x))) = r(g·h(f(x))) = r(h(f(x)))。所以等变网络让各层保持等变，只在读出时
变成不变的（对粒子求和、取范数）：在中间插一个不变层，会扔掉后面的层可能需要的朝向信息。

**2. Deep Sets。** 给可数全集编号c(x) ∈ {1, 2, …}。证明X ↦ Σ_{x∈X} 4^{−c(x)}在有限集合上是一一对应的。对多重集会出什么问题？更大的
底数怎样修正它？

*解答。* 把S(X) = Σ 4^{−c(x)}写成四进制：小数点后第k位，若编号为k的元素在X中就是1，否则是0。系数为0或1的有限个不同的4^{−k}之和
不会进位（每位至多1 < 3），而有限的四进制展开是唯一的，所以S(X) = S(Y)意味着各位相同，X = Y。对多重集，4^{−k}的系数是重数m_k；
只要每个m_k ≤ 3，各位仍能唯一读出；但重数为4就会进到前一位（4·4^{−k} = 4^{−(k−1)}），于是{x_k, x_k, x_k, x_k}和{x_{k−1}}撞在一起。
以b为底时，小于b的重数是安全的；对有界的多重集，取比最大重数更大的底数即可（GIN的单射引理用的是同一个想法）。

**3. 正则图。** 证明颜色细化在每一轮都给d-正则图的每个节点同一种颜色，并由此说明没有消息传递网络能分辨6元环和两个三角形。

*解答。* 归纳：第0轮所有颜色相同。若第t轮所有节点都是颜色c，则第t + 1轮每个节点的签名都是（c，大小为d的多重集{c, …, c}），对每个
节点都一样，所以所有节点再次同色。因此节点数相同的两个d-正则图在每一轮的颜色直方图都相同。C₆和2C₃都是6个节点的2-正则图，所以
1-WL分不开它们；由第5章的定理（MPNN的状态是WL颜色的函数），任何消息传递网络都给两个图的每个节点同样的状态，于是求和读出也相同。
可一个有三角形，另一个没有。

**4. 过平滑。** 对连通图，证明Â = D^{−1/2}(A + I)D^{−1/2}的最大特征值是1，特征向量 ∝ D^{1/2}𝟏，并且Â^k X收敛到X在它上面的投影。

*解答。* 这里D是A + I的度矩阵。Â·D^{1/2}𝟏 = D^{−1/2}(A + I)𝟏 = D^{−1/2}D𝟏 = D^{1/2}𝟏，所以D^{1/2}𝟏是特征值为1的特征向量。Â与随机
游走矩阵P = D^{−1}(A + I)相似（Â = D^{1/2} P D^{−1/2}），P是随机矩阵，所以所有特征值|λ| ≤ 1。图连通时P不可约，自环使它非周期，
由佩龙–弗罗贝尼乌斯定理，λ = 1是单根，其余特征值|λ| < 1。写Â = Σ λ_i u_i u_iᵀ（正交归一，Â对称），则Â^k X = u₁u₁ᵀX +
Σ_{i≥2} λ_i^k u_i u_iᵀ X，第二项至多|λ₂|^k ‖X‖。极限的每一列都是D^{1/2}𝟏的倍数：每个节点的特征只由它的度决定，区分节点的信息消失了。

**5. EGNN。** 证明x_i′ = x_i + C Σ_j (x_i − x_j) φ(‖x_i − x_j‖²)对每个正交矩阵R满足x′(Rx + t) = R x′(x) + t。它因此看不见反射吗？

*解答。* 令y_i = Rx_i + t。则y_i − y_j = R(x_i − x_j)，而且因为R正交，‖y_i − y_j‖ = ‖x_i − x_j‖，所以每个φ都不变，
y_i′ = Rx_i + t + C Σ_j R(x_i − x_j) φ(·) = R x_i′ + t。证明里没用到det R = +1，所以这一层对反射也等变（是E(n)，而不仅是SE(n)），
任何不变读出都给一个分子和它的镜像同样的值：这样的网络单凭位置分不清对映体。当手性要紧时，比如蛋白质，就加上一个赝标量（三重积
(x_j − x_i)·((x_k − x_i) × (x_l − x_i))，在反射下变号），或者像AlphaFold 2那样，用右手坐标系和FAPE这样的损失。

**6. 傅里叶层。** 证明v ↦ F^{−1}[R_k v̂_k]与周期网格的平移交换，并且同样的R_k在任何多于2k_max个点的网格上定义了这一层。

*解答。* 平移s个格点：(τ_s v)_n = v_{n−s}。它的离散傅里叶系数是(τ_s v)^_k = e^{−2πiks/N} v̂_k。乘以R_k再反变换，得到
F^{−1}[R_k e^{−2πiks/N} v̂_k] = τ_s F^{−1}[R_k v̂_k]：相位因子恰好是一次平移。（连续变量平移任意量，对傅里叶级数的作用也是这样，所以这个
算子与圆周上的所有平移交换。）权重R_k按频率k = 0, …, k_max − 1编号，而不是按格点编号。N个点的网格能表示|k| < N/2的频率，所以只要
N > 2k_max，每个学到的频率在新网格上都存在，这一层由同样的数定义：在新网格上采样输入，变换，乘上同样的模式，再变换回来。随N变化的是
傅里叶层之间逐点非线性带来的混叠，这就是为什么误差在不同分辨率上并不完全不变。

## Glossary (new terms in this part)

| English | 中文 |
|---|---|
| symmetry, transformation | 对称，变换 |
| group, group action, identity, inverse | 群，群作用，单位元，逆元 |
| permutation, permutation group | 置换（排列），置换群 |
| rotation group SO(3), E(3), E(n), SE(3) | 转动群SO(3)，E(3)，E(n)，SE(3) |
| rigid motion, reflection, translation | 刚体运动，反射，平移 |
| invariant, invariance | 不变的，不变性 |
| equivariant, equivariance | 等变的，等变性 |
| group averaging (Reynolds operator) | 群平均（雷诺算子） |
| data augmentation | 数据增强 |
| canonicalization (standard pose) | 规范化（标准姿态） |
| geometric deep learning | 几何深度学习 |
| set function, multiset | 集合函数，多重集 |
| Deep Sets, PointNet | Deep Sets，PointNet |
| power sums, Newton's identities | 幂和，牛顿恒等式 |
| graph, node, edge, adjacency matrix | 图，节点，边，邻接矩阵 |
| graph neural network (GNN) | 图神经网络（GNN） |
| message passing (MPNN), message, readout | 消息传递（MPNN），消息，读出 |
| graph convolutional network (GCN) | 图卷积网络（GCN） |
| hop, receptive field | 跳，感受野 |
| stochastic block model, community | 随机块模型，社群 |
| Weisfeiler–Leman test (1-WL), colour refinement | 魏斯费勒–莱曼检验（1-WL），颜色细化 |
| graph isomorphism | 图同构 |
| graph isomorphism network (GIN) | 图同构网络（GIN） |
| sum / mean / max aggregation | 求和 / 平均 / 最大值聚合 |
| regular graph, union of cycles | 正则图，若干环的并 |
| random node features (RNI) | 随机节点特征（RNI） |
| pair network (provably powerful graph network) | 节点对网络（可证明强大的图网络） |
| k-WL, subgraph counts, positional encoding | k-WL，子图计数，位置编码 |
| over-smoothing, Dirichlet energy | 过平滑，狄利克雷能量 |
| over-squashing, bottleneck, curvature | 过挤压，瓶颈，曲率 |
| residual (skip) connection | 残差（跳跃）连接 |
| graph attention (GAT, GATv2), graph transformer | 图注意力（GAT，GATv2），图Transformer |
| decalin, bicyclopentyl | 十氢萘，联环戊烷 |
| E(n)-equivariant graph network (EGNN) | E(n)等变图网络（EGNN） |
| SchNet, radial basis functions | SchNet，径向基函数 |
| spherical harmonics, degree ℓ | 球谐函数，阶ℓ |
| Wigner D-matrix (rotation block) | 维格纳D矩阵（转动块） |
| Clebsch–Gordan coefficients, tensor product | 克莱布什–戈尔丹系数，张量积 |
| tensor field network, NequIP, MACE, e3nn | 张量场网络，NequIP，MACE，e3nn |
| interatomic potential, force field | 原子间势，力场 |
| n-body system, charged particles | 多体系统，带电粒子 |
| protein, amino acid, residue | 蛋白质，氨基酸，残基 |
| fold, backbone, C-alpha (Cα) | 折叠（构象），主链，Cα原子 |
| helix, strand, loop, three-helix bundle | 螺旋，链，环，三螺旋束 |
| X-ray crystallography, cryo-EM | X射线晶体学，冷冻电镜 |
| Protein Data Bank (PDB) | 蛋白质数据库（PDB） |
| Levinthal's paradox | 列文索尔悖论 |
| CASP, GDT_TS, free modelling | CASP，GDT_TS，自由建模（无模板） |
| multiple sequence alignment (MSA), co-evolution, contact | 多序列比对（MSA），共进化，接触 |
| distogram | 距离直方图 |
| classical multidimensional scaling (MDS), Gram matrix | 经典多维尺度分析（MDS），格拉姆矩阵 |
| mirror image, chirality, right-handed | 镜像，手性，右手的 |
| RMSD, distance RMSD (dRMSD), Kabsch alignment | 均方根偏差（RMSD），距离均方根偏差（dRMSD），Kabsch对齐 |
| Evoformer, pair representation, MSA representation | Evoformer，残基对表示，MSA表示 |
| row / column attention, outer product mean | 行 / 列注意力，外积均值 |
| triangle inequality, triangle multiplicative update, triangle attention | 三角不等式，三角乘法更新，三角注意力 |
| structure module, rigid frame, residue gas | 结构模块，刚性坐标系，残基气体 |
| invariant point attention (IPA) | 不变点注意力（IPA） |
| frame-aligned point error (FAPE), clamp | 坐标系对齐点误差（FAPE），截断 |
| recycling | 循环（回收） |
| pLDDT (confidence) | pLDDT（置信度） |
| AlphaFold Protein Structure Database | AlphaFold蛋白质结构数据库 |
| Pairformer, diffusion module | Pairformer，扩散模块 |
| cross-distillation, hallucination | 交叉蒸馏，幻觉 |
| ligand, docking, PoseBusters | 配体，分子对接，PoseBusters |
| protein design, inverse folding, binder | 蛋白质设计，逆折叠，结合子 |
| sequence recovery | 序列还原率 |
| motif scaffolding | 基序支架 |
| denoiser, denoising diffusion | 去噪器，去噪扩散 |
| numerical weather prediction (NWP) | 数值天气预报（NWP） |
| reanalysis (ERA5) | 再分析（ERA5） |
| icosahedral mesh, multimesh | 二十面体网格，多尺度网格（multimesh） |
| encoder–processor–decoder | 编码器–处理器–解码器 |
| rollout, lead time | 推演（展开），预报时效 |
| persistence, climatology | 持续性预报，气候平均 |
| ensemble forecast | 集合预报 |
| vorticity | 涡度 |
| neural operator, Fourier neural operator (FNO), DeepONet | 神经算子，傅里叶神经算子（FNO），DeepONet |
| Burgers' equation, pseudo-spectral solver | 伯格斯方程，伪谱求解器 |
| convolution theorem, Fourier mode | 卷积定理，傅里叶模式 |
| resolution invariance, zero-shot super-resolution | 分辨率不变性，零样本超分辨率 |
| crystal, space group, formation energy | 晶体，空间群，形成能 |
| density functional theory (DFT) | 密度泛函理论（DFT） |
| convex hull, energy above hull, stable | 凸包，凸包上方能量，稳定 |
| active learning, surrogate model, hit rate | 主动学习，代理模型，命中率 |
| autonomous laboratory | 自主实验室 |
| proof assistant, kernel, Lean, Mathlib | 证明助手，内核，Lean，Mathlib |
| formal proof, formalization, autoformalization | 形式化证明，形式化，自动形式化 |
| four-colour theorem, Kepler conjecture | 四色定理，开普勒猜想 |
| symbolic deduction engine, auxiliary construction | 符号演绎引擎，辅助构造 |
| synthetic theorems, traceback | 合成定理，回溯 |
| Erdős problems | 埃尔德什问题 |
| cap set | 帽集 |
| online bin packing, first fit, best fit, priority function | 在线装箱，首次适配，最佳适配，优先级函数 |
| genetic programming, mutation, crossover | 遗传规划，变异，交叉 |
| tensor rank, tensor decomposition | 张量秩，张量分解 |
| alternating least squares | 交替最小二乘 |
| Strassen's algorithm | 施特拉森算法 |
| kissing number | 接吻数 |
| evolutionary coding agent | 进化编程智能体 |

Names stay in Latin script: AlphaFold, AlphaFold-Multimer, AlphaFold Server, RoseTTAFold, ESMFold, ESM3, ProteinMPNN,
RFdiffusion, RFdiffusion3, BindCraft, AlphaProteo, BoltzGen, Boltz-1, Boltz-2, Chai-1, Protenix, OpenFold3, IsoDDE,
Rosetta, Top7, GraphCast, GenCast, AIFS, FourCastNet, Pangu-Weather, WeatherNext, GNoME, MatterGen, MACE-MP-0, A-Lab,
EGNN, SchNet, NequIP, MACE, e3nn, GIN, GCN, GAT, PointNet, Deep Sets, FNO, DeepONet, Lean, Mathlib, AlphaGeometry,
AlphaProof, Gemini Deep Think, Aristotle, Gauss, FunSearch, AlphaEvolve, AlphaTensor.
