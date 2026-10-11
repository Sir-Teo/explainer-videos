# Quantum Mechanics, Part 2: Where the Rules Come From (Symmetry, Sums over Paths, and the Structure of Matter)

A 20-chapter, math-heavy sequel to [Part 1](../quantum). Part 1 ended with the whole theory on one screen: the
Schrödinger equation, the Born rule and [x̂, p̂] = iħ. It also admitted how we got them: the equation was guessed
from plane waves, the Born rule was postulated, and the commutator was computed from a guessed p̂ = −iħ∂ₓ. Part 2
**derives** them, by three independent roads, and then uses the theory on real matter.

- **Symmetry.** A symmetry preserves every |⟨φ|ψ⟩|², so (Wigner) it is unitary. Time translation is a one-parameter
  unitary group, so (Stone) U(t) = e^{−iĤt/ħ} with Ĥ Hermitian, and iħ∂ₜψ = Ĥψ follows with no waves at all. The
  i is a rotation generator (J² = −1). Translations define momentum. "Translation moves position" gives
  [X̂, P̂] = iħ, and P̂ = −iħ∂ₓ follows. The trace argument shows the Hilbert space must be infinite-dimensional,
  and Stone–von Neumann says every solution is x and −iħ∂ₓ in disguise. Galilean boosts give Ĥ = P̂²/2m + V(X̂).
  Rotations don't commute; [Ĵₓ, Ĵ_y] = iħĴ_z alone gives j(j + 1)ħ² and allows half-integer spin. Local phase
  invariance forces p → p − qA (electromagnetism). The Aharonov–Bohm effect is simulated.
- **Sums over paths.** The propagator. Feynman's screens. Time slicing gives K = ∫𝒟x e^{iS/ħ}. Imaginary time
  turns paths into Brownian motion: kernel products and path-integral Monte Carlo give the oscillator's ground
  state. The Schrödinger equation is derived from the short-time kernel (⟨η²⟩ = iħε/m, the "dW² = dt" of path
  integrals). Time slicing doubles as an algorithm, with error ~ ε². Stationary phase, the Cornu spiral and
  Euler–Lagrange give Newton's laws. WKB gives Hamilton–Jacobi at order ħ⁰ and the 1/√p amplitude at order ħ¹;
  Airy turning points give ∮p dx = (n + ½)h. Gamow's tunneling integral is set against 29 measured alpha-decay
  half-lives spanning 24 decades.
- **Approximations.** Rayleigh–Schrödinger perturbation theory, derived. The Stark-shifted box in closed form.
  Level repulsion; a stretched drum shows crossings (separable) vs. avoided crossings (dented), per von
  Neumann–Wigner. The anharmonic oscillator's exact rational series (Bender–Wu) diverges, with optimal truncation
  and Dyson's argument. Time-dependent perturbation theory: sinc² → 2πtδ(ω), Fermi's golden rule, tested exactly on
  a level decaying into 601 levels (rate, Lorentzian line, recurrence). The hydrogen 2p lifetime comes out at
  1.596 ns.
- **Many particles.** Exchange symmetry (P̂² = 1 ⇒ ±1). Bosons and fermions on the (x₁, x₂) plane, the Pauli
  principle, Slater determinants, the exchange hole, Hong–Ou–Mandel. Helium by perturbation theory, the
  variational principle (ζ = 27/16) and a two-electron (s-wave) numerical solve, which also gives 1s2s singlet vs.
  triplet (0.82 eV computed, 0.80 measured). Ionization energies Z = 1–86 (NIST). Bloch's theorem; wells added
  one by one become bands; Kronig–Penney; metals vs. insulators.
- **Open systems.** Density matrices, the Bloch ball, the partial trace of a singlet. Gleason's theorem: the Born
  rule is the only consistent probability rule. Decoherence: the environment as a recorder, N-spin dephasing, fringe
  visibility, a cat state's Wigner fringes fading as e^{−4Λt x₀²}, Joos–Zeh/Schlosshauer time scales. What
  decoherence does not solve.
- **Relativity.** Klein–Gordon's problems; Dirac's linearization forces four anticommuting 4×4 matrices: four
  components, spin ½ and negative energies (positrons). Zitterbewegung as interference between the ± branches,
  simulated in 1 + 1 D. The Pauli equation gives g = 2, and QED gives g − 2. Hydrogen's n = 2: Bohr → Dirac fine
  structure (10.95 GHz) → Lamb shift (1057.8 MHz).

Like Part 1, **nothing is a cartoon**. Every wave is a numerical solution (split-operator FFTs, gauge-twisted FFT
steps with Peierls phases, exact eigen-expansions, finite-difference and Fourier-grid eigenproblems). Every random
sample is seeded. Every symbolic step the slides rely on is checked with sympy or numerically, and every number
the narration states is computed in [`compute.py`](compute.py) and asserted against theory or data. Schematics are
labeled `schematic`.

**Watch:** [`published/quantum2.mp4`](../../published/quantum2.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

CHAPTERS

</details>

```bash
python -m videos.quantum2.compute          # once: every simulation (~25 min on 4 cores, cached in .cache/quantum2)
python tools/build.py quantum2 -q l        # preview
python tools/build.py quantum2             # final 1080p30 + subtitles + chapters
python tools/export_script.py quantum2     # regenerate SCRIPT.md from the code
python tools/check_narration.py quantum2   # Whisper listen test of every narration line
python tools/publish.py quantum2           # GitHub-sized copy -> published/quantum2.mp4
```

## The visual language

Part 2 keeps Part 1's conventions without change. A complex amplitude has its **phase as the hue** (constant
lightness in OKLCH: 0 red, π/2 yellow-green, π cyan, 3π/2 violet) and its **size as height or brightness**. A
phase wheel sits in a corner whenever phase colors are on screen. Real two-particle wavefunctions use the same
map, so their sign reads as red (+) or cyan (−).

Choices made for this video, several following the physics-education literature:

* **One worked derivation per idea, line by line.** Each new line grows out of the previous one, and a grey note
  says *why* it follows (Renkl & Atkinson's worked examples, Mayer's signaling principle). Only the line that
  changes is colored. Narration is never duplicated as on-screen text (Mayer's redundancy principle).
* **Concrete before abstract.** The sum over paths starts from the double slit with real arrows: 14 paths per slit,
  chained tip to tail at every screen point, building the fringes live. Only then come time slicing and ∫𝒟x.
* **Misconceptions stated and refuted aloud** (Muller et al.): "the electron feels B" (the computed |ψ|² at the
  flux tube stays below 10⁻⁴ of the incoming peak); "the Pauli exclusion is a force" (the same Hamiltonian for
  distinguishable particles, bosons and fermions; Mullin & Blaylock 2003); "decoherence solves the measurement
  problem" (it doesn't; Schlosshauer 2004); "Zitterbewegung is a trembling point" (it is interference between the
  ± energy parts; Thaller); "spin and g = 2 are relativistic" (Lévy-Leblond 1967 gets both from a non-relativistic
  equation; the narration says relativity adds antimatter and fine structure).
* **The Aharonov–Bohm effect, honestly.** The simulation slides the fringes continuously, one per flux quantum
  h/e, as for an idealized unshielded solenoid. Tonomura's shielded toroid could only show shifts of 0 or half a
  fringe, because the superconductor quantizes the trapped flux in units of h/2e, and the video says so.
* **Stationary phase as cancellation you can see.** A Cornu spiral is built from the actual actions of a family
  of paths, with a moving pointer linking each path on the left to its arrow on the right, and it tightens as ħ
  shrinks. In the 2D picture, brightness is how well neighboring arrows agree (a locally averaged e^{iS/ħ}), so the
  stationary point is literally the bright spot.
* **"Phase = area / ħ"** is a motif that recurs and is recapped at the end: the Weyl relation (a phase-space
  rectangle), the Aharonov–Bohm flux and the Bohr–Sommerfeld orbit area.
* **Log-scale plots** draw an L-shaped frame at the bottom-left instead of axes through the origin (which on a log
  scale would cut through the middle of the data).

| Concept | Color |
|---|---|
| everything from Part 1 (x blue, p orange, E green, t teal, V grey, \|ψ\|² warm yellow, iħ lilac, classical sepia, …) | unchanged |
| the action S, a path's phase S/ħ | rose |
| gauge fields A, χ, magnetic flux Φ | lime |
| angular momentum J, L (J₊ / J₋ reuse a† / a's light green / salmon) | light orange |
| perturbations λV and their matrix elements | pink |
| approximations: WKB, partial sums, variational estimates | magenta |
| bosons / fermions | sky blue / soft red |
| environments / coherences (off-diagonal ρ) | slate / violet |
| Dirac's positive / negative energies | amber / blue |
| nuclei, alpha particles | deep orange |

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 1 | `Hook` | Part 1's three lines, and how each was guessed. Feynman's view of the double slit: one arrow per path, chained tip to tail; sweeping the screen point draws the fringes. Every path, weighted by e^{iS/ħ}. Three roads (symmetry, paths, classical limit) and the plan. | A Huygens–Feynman sum (2D Green's function phase and 1/√r) through two finite slits: 28 arrows per screen point at 241 points; fringes at whole-wavelength path differences, central spacing λL/d. |
| 2 | `TimeSymmetry` | Wigner: symmetries are unitary (or antiunitary). U(t + s) = U(t)U(s) and Stone's theorem. The derivation U(ε) = 1 − iεĤ/ħ, unitarity ⇒ Ĥ† = Ĥ, iħ∂ₜψ = Ĥψ. Why i: J² = −1; the power series of e^{−iθ} spirals onto the circle. Energy is the generator of time translations; the Bloch sphere rotates rigidly. | The series of e^{−2.3i}, term by term; a precessing spin. |
| 3 | `Translations` | T(a) = e^{−iaP̂/ħ} defines momentum. [X̂, T(a)] = aT(a) ⇒ [X̂, P̂] = iħ. ⟨x\|P̂ψ⟩ = −iħψ′, derived. tr[X, P] = 0 ⇒ infinite dimensions; Stone–von Neumann. A boost multiplies ψ by e^{imvx/ħ}; velocity P/m in every frame ⇒ Ĥ = P̂²/2m + V(X̂). TB = e^{−imva/ħ}BT: phase = area/ħ. | A random 5 × 5 commutator whose diagonal sums to 0; a boosted packet whose momentum distribution slides by exactly mv. |
| 4 | `Rotations` | Rotations don't commute (two books). R_x R_y R_x⁻¹ R_y⁻¹ = R_z(ε²) ⇒ [Ĵₓ, Ĵ_y] = iħĴ_z. Ladder operators, the top and bottom rungs, j(j + 1)ħ², 2j ∈ ℕ. Integer j orbital, half-integer spin, (−1)^{2j}. Y₂ᵐ on spheres; \|J\| > max J_z. | The leftover angle/ε² → 0.99993 with axis → z; spherical harmonics rendered with phase as hue; L₊Y = ħ√(ℓ(ℓ+1) − m(m+1))Y checked on a grid (error 7.5 × 10⁻⁵). |
| 5 | `Gauge` | Local phase changes leave \|ψ\|² alone but not the momentum operator; A → A + ∇χ, p → p − qA, φ → φ − ∂ₜχ give H = (p − qA)²/2m + qφ (Fock, London, Weyl). Path phase (q/ħ)∫A·dℓ; loop phase qΦ/ħ by Stokes. The AB effect, simulated. Tonomura (1986) and h/2e. | A packet through two slits around a flux tube inside the wall, for 13 fluxes: the center turns dark at Φ = h/2e, the fringe phase moves 2π per h/e (slope 1.02), and Φ = h/e reproduces Φ = 0 to 10⁻⁶. |
| 6 | `PathIntegral` | The propagator; the free kernel as a chirp. Feynman & Hibbs' screens. Time slicing: K = ∫𝒟x e^{iS/ħ} (Dirac 1933, Feynman 1948). Imaginary time: positive weights, Brownian paths (Feynman–Kac). | The oscillator's short-time kernel as a matrix; repeated application relaxes any shape to the ground state; E₀ = 0.4407 (ε = 2) … 0.49995 (ε = 0.05), error ~ ε². Path-integral Monte Carlo: 100-slice loops, ⟨x²⟩ = 0.511 vs. 0.499 exact for that discretization. |
| 7 | `PathToSchrodinger` | Feynman's derivation: Taylor-expand ψ(x + η), Gaussian moments {1, 0, iħε/m}, the Schrödinger equation. ⟨η²⟩ ∝ ε ↔ (dW)² = dt; typical paths are nowhere smooth. Strang splitting = Feynman's slice: the algorithm behind Part 1's simulations. | A 2¹⁸-step Brownian path at four zooms (×8 each); a packet in an anharmonic well evolved with 6/ε slices vs. an exact eigen-expansion: slope 2.01. |
| 8 | `StationaryPhase` | A thrown ball's family of paths; S(a) = S_cl + π²a²/4T. The arrows form a Cornu spiral; as ħ shrinks only paths with \|S − S_cl\| ≲ ħ survive. A 2D family; δS = 0 ⇒ Euler–Lagrange ⇒ mẍ = −V′. 1 g ball: S/ħ ≈ 4.7 × 10³⁰. Fermat's principle. | Actions of 321 paths by quadrature (matching the closed form to 10⁻⁵); Cornu sums matching the stationary-phase value; the bending that turns the arrow 4 × 10¹⁰ times. |
| 9 | `WKB` | ψ = Ae^{iS/ħ}: Hamilton–Jacobi at ħ⁰, A ∝ 1/√p at ħ¹. Exact vs. WKB in a quartic well. Airy functions at turning points, π/4 each ⇒ ∮p dx = (n + ½)h (Kramers 1926). Phase-space orbits of area (n + ½)h; a Wigner function on its orbit. | H = p²/2 + x⁴: Fourier-grid spectrum (E₀ = 0.667986) vs. WKB: −18% at n = 0, −0.03% at n = 10, −0.008% at n = 20; the old rule (no ½) far off; orbit areas/h = 2.51, 3.51, 4.51, 5.50. |
| 10 | `Gamow` | U-238 vs. Po-212: ×2 in energy, ×10²⁴ in lifetime (Geiger–Nuttall). The Coulomb barrier (28 MeV at R ≈ 9.3 fm, turning point 61 fm). 2G in closed form: 88 for U-238, 32 for Po-212; ν ≈ 7.8 × 10²⁰ s⁻¹. | 29 measured half-lives vs. Gamow's formula with R = 1.2(A_d^{1/3} + 4^{1/3}) fm and no fitting: correlation 0.998, median miss a factor of 1.8; U-238 predicted 4.6 Gyr; worst at N = 126. |
| 11 | `Perturbation` | Rayleigh–Schrödinger theory, derived to second order. The Stark-shifted box: E⁽¹⁾ = 0, E⁽²⁾ = −(15 − π²)F²/24π⁴. Level repulsion. A stretched drum: crossings when separable, gaps with a dent (von Neumann–Wigner). The anharmonic series diverges (Bender–Wu, Dyson); optimal truncation. | The second-order sum (59 states) matches the closed form to 10⁻⁶; drum spectra (2116-point finite differences, 226 stretches) with and without a dent; 40 exact rational Bender–Wu coefficients (1/2, 3/4, −21/8, 333/16, …) checked against the large-order law; best truncation at g = 0.02: order 16, error 3 × 10⁻⁸. |
| 12 | `GoldenRule` | Interaction-picture coefficients; first order; sin²(ωt/2)/(ω/2)² → 2πtδ(ω); Γ = (2π/ħ)\|V\|²ρ (Dirac 1927; Fermi). An exact test. The Lorentzian of width ħΓ. Hydrogen 2p: golden rule with the photon density of states. | One level + 601 levels (602 × 602 exact): rate 0.3163 vs. 2πV²/δ = 0.3142, quadratic start, revival at 2πħ/δ, Lorentzian populations; τ(2p) = 1.596 ns, 3.9 million Lyman-α cycles. |
| 13 | `Identical` | P̂ψ(x₁, x₂) = ψ(x₂, x₁), P̂² = 1 ⇒ ±1; spin–statistics; anyons in 2D. Distinguishable / bosons / fermions in a box. Pauli; Slater determinants; the exchange hole. Hong–Ou–Mandel: tt + rr = ½ − ½ = 0. | P(\|x₁ − x₂\| < 0.1L) = 20% / 38% / 1.6%; the 3-fermion pair density; a seeded HOM dip (2,000 pairs per delay). |
| 14 | `Helium` | −108.8 eV without repulsion; ⟨1/r₁₂⟩ = 5Z/8 by the shell theorem ⇒ −74.8 eV; the variational principle; ζ = 27/16 ⇒ −77.5 eV; an s-wave two-electron solve −78.3 eV; measured −79.0 eV. 1s2s singlet vs. triplet: the triplet's node at r₁ = r₂. Ionization energies and shells. | sympy: ⟨1/r₁₂⟩, first order, ζ*, E(ζ*); a 2D finite-difference (Temkin–Poet) solve, Richardson-extrapolated: ground −2.8787 Ha (s-limit −2.8790), 1s2s splitting 0.818 eV vs. 0.796 measured (NIST); NIST ionization energies Z = 1–86. |
| 15 | `Bands` | Wells added one by one: levels split by tunneling into bands. Bloch's theorem from [Ĥ, T̂(a)] = 0. Kronig–Penney: cos ka = ½ tr M(E); gaps where \|f\| > 1. E(k). Band filling: metals vs. insulators (Wilson 1931). | Finite-difference spectra of 1–32 wells (N levels per band, every 32-well level inside a KP band); bonding/antibonding states of 2 wells; Bloch states on a ring of 8 cells (k = 2πn/8a, landing on the KP curves). |
| 16 | `Density` | Superposition vs. coin flip; ρ = Σpᵢ\|ψᵢ⟩⟨ψᵢ\|, P(a) = tr(ρPₐ); coherences; purity. The Bloch ball; different ensembles, same ρ. The singlet's partial trace: ρ_A = I/2, S = ln 2. Gleason's theorem: the Born rule is the only consistent rule. | A rotating orthonormal frame with outcome probabilities ⟨eᵢ\|ρ\|eᵢ⟩ always summing to 1.000. |
| 17 | `Decoherence` | The environment as a recorder: coherences × ⟨E₁\|E₀⟩. N-spin dephasing; the Bloch arrow shrinks to the axis. Which-path visibility. A cat's Wigner fringes decay as e^{−4Λt x₀²} while the blobs survive. Time scales. What decoherence does and doesn't explain. | \|⟨E₁\|E₀⟩\| for N = 1, 5, 20, 200 random spins; 31 Wigner functions of the decohering cat (fringe height matches e^{−4sx₀²/(1+4s)}/√(1+4s) to 0.01). |
| 18 | `Dirac` | Klein–Gordon's problems. H = cα·p + βmc²; squaring forces anticommuting α, β ⇒ 4 × 4 matrices, four components, spin ½, negative energies. Hole theory, Anderson's positron. Zitterbewegung as interference between branches. | All ten anticommutators and H² = (p² + m²)I checked numerically; a 1 + 1 D Dirac packet, half positive and half negative energy, solved exactly in k-space: its center trembles at ω = 2.09 (≈ 2mc²/ħ) around its positive-energy part, which stays put. |
| 19 | `FineStructure` | (σ·π)² = π² − qħσ·B ⇒ g = 2. g/2 = 1.00115965218059(13); α/2π (Schwinger 1948). Dirac's hydrogen formula; n = 2: 10.95 GHz fine structure (10.969 measured); the Lamb shift 1057.8 MHz → QED. | The Dirac level formula with CODATA α and the reduced mass. |
| 20 | `Outro` | The derivations on one screen; phase = area/ħ three times; a gallery of computed pictures; where to go next. | |

## Simulations (`compute.py`)

Every item uses ħ = m = 1 (atomic units for helium) and is cached in `.cache/quantum2/<item>.npz`. The
Aharonov–Bohm movies are stored as memory-mapped `ab_movie_000.npy` and `ab_movie_050.npy` (float16, about 55 MB
each). Seeded items use PCG64. Checks run every time an item is computed.

| Item | What | Checks |
|---|---|---|
| `hook` | Huygens–Feynman sum through two slits (λ = 1, d = 4, w = 1.2, L₁ = 20, L₂ = 40). | 28 arrows/point converge to the 800-point sum; bright fringes at whole-λ path differences (central to 0.05 λ); central spacing λL/d within 4%. |
| `symmetry` | Rotation commutators; a random 5 × 5 commutator; spherical-harmonic sphere renders; L₊ on a (θ, φ) grid; a boost. | angle/ε² → 1, axis → z; tr[X, P] = 0; L₊ error < 10⁻⁴; ⟨p⟩ shifts by mv exactly. |
| `ab` | 1280 × 1152 grid (h = 0.25), k₀ = 1.2; a smooth slit plate (V₀ = 10, tanh edges); a flux tube inside the wall; a Peierls phase on the links crossing a cut through the top slit, applied exactly by a gauge-twisted FFT per row (checked against expm on a small ring to 10⁻¹²); Strang splitting, dt = 0.2; an absorbing detector slab. 13 fluxes. | \|ψ\|² at the tube < 3 × 10⁻⁸ at all times (its largest value is the initial packet's far tail); α = 1 equals α = 0; the center is dark at α = ½; the fringe phase moves 2π per flux quantum (±8%). Sharp plate edges were measured to scatter 0.8% of the wave into high-energy states that leak through the wall; the smooth plate brings that to 2 × 10⁻⁶. |
| `pathint` | Euclidean short-time kernels of the oscillator on 561 points; their top eigenvalue; relaxation; Metropolis PIMC (β = 10, 100 slices, 30,000 sweeps, seed 1948); the free kernel's composition law (sympy). | E₀ → ½ with slope 2 in ε; ⟨x²⟩ within 3% of the exact 100-slice value (0.4994), which is within 0.2% of the continuum. |
| `slicing` | Strang slicing vs. an exact Fourier-grid eigen-expansion; a 2¹⁸-step Brownian path (seed 1923). | Global error ~ ε^{2.01}; Σ(dW)² = 1. |
| `stationary` | 321 paths of a thrown ball; arrows for ħ = 0.25, 0.08, 0.025; a 401² map of S(a, b). | S_cl = −g²T³/24; S(a) and S(a, b) vs. closed forms (10⁻⁵); Cornu sums vs. stationary phase (12%). |
| `wkb` | p²/2 + x⁴ on a 400-point Fourier grid; WKB/Bohr–Sommerfeld; n = 6 WKB wave; the n = 8 Wigner function. | E₀ = 0.667986259; WKB error < 0.5% for n ≥ 3 and shrinking; the WKB wave matches inside to 6%; Wigner normalization 1 (10⁻³); orbit areas (n + ½)h. |
| `gamow` | Gamow's formula for 29 alpha emitters from the committed snapshot. | Data span > 23.5 decades; model–data correlation > 0.99, scatter < 0.8 decades; ν ~ 10²¹ s⁻¹. |
| `perturb` | Drum spectra (sparse shift-invert), the Stark box (2,000 points), Bender–Wu to order 40 (exact fractions), exact anharmonic E₀(g). | FD drum = separable FD levels (10⁻⁶); gaps close without the dent and stay open with it; E⁽²⁾ = −(15 − π²)/24π⁴ (10⁻⁴); first six coefficients and the large-order law (1%); best order ≈ 1/3g. |
| `golden` | 1 + 601 levels (δ = V = 0.05), exact. | Rate within 2% of 2πV²/δ; quadratic start (10⁻⁵); revival > 0.2 near 2π/δ; Lorentzian populations (6%). |
| `identical` | Two particles in a box; three fermions; a seeded HOM dip (seed 1987). | Normalization; bunching > distinguishable > antibunching; ψ_A = 0 on the diagonal; exchange hole; dip < 25 counts. |
| `helium` | sympy: ⟨1/r₁₂⟩ = 5Z/8, first order −11/4, ζ* = Z − 5/16, E = −729/256; Temkin–Poet 2D finite differences (h = 0.1, 0.07, Richardson). | −74.83, −77.49, −79.005 eV; ground −2.8790 (3 × 10⁻³); singlet–triplet within 6% of 0.796 eV; noble gases are peaks. |
| `bands` | Kronig–Penney chains of 1–32 wells (140 points/cell); KP band edges; Bloch states on an 8-cell ring. | Every 32-well level lies in a KP band; N levels per band; ring momenta = 2πn/(8a). |
| `decoherence` | Wigner functions of ρ(x, x′)e^{−Λt(x−x′)²} for a cat (x₀ = ±3); N-spin dephasing (seed 1982); Joos–Zeh rates. | Fringe decay = the exact Gaussian formula (0.01); blobs survive; 200 spins never recohere; 2 spins do. |
| `dirac` | Dirac/Pauli algebra; a 1 + 1 D packet, spinor (1, i)/√2, exact in k-space, with and without its negative-energy part. | Anticommutators; H² = p² + m²; half positive energy; the positive part's center fixed (10⁻⁶); trembling at ω ∈ (1.9, 2.6). |
| `numbers` | h/e, h/2e; the ball's S/ħ; the hydrogen 2p rate (golden rule + photon density of states, reduced mass); Dirac's n = 2 fine structure; α/2π; ħ/2mc. | h/2e (CODATA); 1.596 ns; 10.95 GHz; 1.931 × 10⁻¹³ m. |

## Data snapshots (`data/`)

* `alpha_decay.json`: 29 even-even alpha emitters (Po-208 … Cf-252). Half-lives and alpha branchings are from the
  NNDC NuDat 3 data file (https://www.nndc.bnl.gov/nudat3/data/output.json), cross-checked against NUBASE2020
  (Kondev et al., Chin. Phys. C 45, 030001, 2021). Q_α is from AME2020 (Huang et al. and Wang et al., Chin. Phys. C
  45, 030002/030003, 2021), identical to NuDat's to 0.1 eV. Retrieved 2026-10-11; per-row URLs are in the file. The
  video uses partial alpha half-lives (T / branch). For the actinides only 67–81% of decays go ground state to
  ground state; the simple model ignores this.
* `ionization.json`: first ionization energies, Z = 1–86, from the NIST Atomic Spectra Database (ver. 5.12),
  retrieved 2026-10-11 (the query URL is in the file; PubChem only as a cross-check).

## Fact-check notes and sources

The mathematics is standard: Sakurai & Napolitano (symmetry, angular momentum, perturbation theory), Ballentine
(*Quantum Mechanics: A Modern Development*, ch. 3, for the Galilean derivation of [X, P] and Ĥ), Feynman & Hibbs
(*Quantum Mechanics and Path Integrals*, 1965), Griffiths & Schroeter (WKB, helium, the variational principle),
Ashcroft & Mermin (Bloch, bands), Schlosshauer (decoherence), Thaller (*Advanced Visual Quantum Mechanics*, the
Dirac equation and Zitterbewegung). Historical claims were checked against primary sources (DOIs via Crossref):

* **Wigner**, *Gruppentheorie* (Vieweg, 1931), pp. 251–254; the standard complete proof is **Bargmann**, J. Math.
  Phys. 5, 862 (1964). **Stone**, PNAS 16, 172 (1930) and Ann. Math. 33, 643 (1932). **von Neumann**, Math. Ann.
  104, 570 (1931). **Weyl**, Z. Phys. 46, 1 (1927). The finite-dimensional trace argument is folklore. **Wintner**,
  Phys. Rev. 71, 738 (1947) and **Wielandt**, Math. Ann. 121, 21 (1949) prove the stronger result that X and P
  cannot both be bounded. **Bargmann**, Ann. Math. 59, 1 (1954): mass as a central charge of the Galilei group.
* **Born, Heisenberg & Jordan**, Z. Phys. 35, 557 (1926): the angular-momentum spectrum from the algebra,
  half-integers allowed. **Rauch et al.**, Phys. Lett. A 54, 425 (1975) and **Werner et al.**, PRL 35, 1053 (1975):
  the 4π spinor rotation.
* **Fock**, Z. Phys. 39, 226 (1926); **London**, Z. Phys. 42, 375 (1927); **Weyl**, Z. Phys. 56, 330 (1929).
  **Ehrenberg & Siday**, Proc. Phys. Soc. B 62, 8 (1949); **Aharonov & Bohm**, Phys. Rev. 115, 485 (1959);
  **Chambers**, PRL 5, 3 (1960); **Tonomura et al.**, PRL 56, 792 (1986) and **Osakabe et al.**, PRA 34, 815
  (1986), with phase shifts of 0 or π because the superconducting shield traps flux in units of h/2e. Flux quanta
  (CODATA 2022, exact): h/e = 4.135 667 696… × 10⁻¹⁵ Wb, h/2e = 2.067 833 848… × 10⁻¹⁵ Wb.
* **Dirac**, Phys. Z. Sowjetunion 3, 64 (1933); **Feynman**, Rev. Mod. Phys. 20, 367 (1948), §6, which derives
  the Schrödinger equation from the short-time kernel (the ψ(x + η) notation follows Feynman & Hibbs §4-1). The
  "more screens, more holes" argument is in Feynman & Hibbs, ch. 1. **Kac**, Trans. AMS 65, 1 (1949).
  **Mehler**, J. reine angew. Math. 66, 161 (1866).
* **Wentzel**, Z. Phys. 38, 518 (1926); **Kramers**, Z. Phys. 39, 828 (1926), titled *Wellenmechanik und
  halbzahlige Quantisierung*; **Brillouin**, C. R. Acad. Sci. 183, 24 (1926); **Jeffreys**, Proc. London Math.
  Soc. (2) 23, 428 (1925). **Einstein**, Verh. DPG 19, 82 (1917); **Keller**, Ann. Phys. 4, 180 (1958); Maslov
  (1965).
* **Gamow**, Z. Phys. 51, 204 (1928, received 2 August 1928); **Gurney & Condon**, Nature 122, 439 (1928);
  **Geiger & Nuttall**, Phil. Mag. 22, 613 (1911).
* **Schrödinger**, Ann. Phys. 80, 437 (1926), Part III: perturbation theory and the Stark effect. **Bender &
  Wu**, Phys. Rev. 184, 1231 (1969) (E₀ = ½ + ¾g − 21/8 g² + 333/16 g³ − 30885/128 g⁴ + 916731/256 g⁵ − …,
  confirmed against Janke & Kleinert); the large-order law is from Bender & Wu, PRL 27, 461 (1971) and PRD 7,
  1620 (1973). **Dyson**, Phys. Rev. 85, 631 (1952), a heuristic argument. **von Neumann & Wigner**, Phys. Z. 30,
  467 (1929), the non-crossing rule.
* **Dirac**, Proc. R. Soc. A 114, 243 (1927); "Golden Rule No. 2" in Fermi's *Nuclear Physics* (Chicago, 1950).
  **Weisskopf & Wigner**, Z. Phys. 63, 54 (1930). Hydrogen 2p: A = 6.2648 × 10⁸ s⁻¹, τ = 1.596 ns (NIST ASD);
  ⟨1s\|z\|2p₀⟩ = 128√2/243 a₀.
* **Pauli**, Z. Phys. 31, 765 (1925); Nobel Prize 1945. **Heisenberg**, Z. Phys. 38, 411 (1926); **Dirac**, Proc.
  R. Soc. A 112, 661 (1926); **Fermi**, Z. Phys. 36, 902 (1926). **Fierz**, Helv. Phys. Acta 12, 3 (1939);
  **Pauli**, Phys. Rev. 58, 716 (1940). **Leinaas & Myrheim**, Nuovo Cimento B 37, 1 (1977); **Wilczek**, PRL 49,
  957 (1982). **Hong, Ou & Mandel**, PRL 59, 2044 (1987).
* Helium: the measured total −79.005 eV is the sum of the two NIST ionization energies (24.587 + 54.418 eV). It
  equals −2.90339 Ha; the nonrelativistic, infinite-mass value −2.903724 Ha differs by recoil, relativity and QED.
  **Hylleraas**, Z. Phys. 54, 347 (1929). The 1s2s levels are ³S₁ at 19.8196 eV and ¹S₀ at 20.6158 eV (NIST ASD).
  The s-wave ("Temkin–Poet") model's ground state is −2.8790 Ha.
* **Bloch**, Z. Phys. 52, 555 (1929, received 10 August 1928); **Floquet**, Ann. ÉNS 12, 47 (1883); **Kronig &
  Penney**, Proc. R. Soc. A 130, 499 (1931); **Wilson**, Proc. R. Soc. A 133, 458 (1931).
* **von Neumann**, Göttinger Nachr. 1927, 245; **Landau**, Z. Phys. 45, 430 (1927). **Gleason**, J. Math. Mech.
  6, 885 (1957).
* **Zeh**, Found. Phys. 1, 69 (1970); **Zurek**, PRD 24, 1516 (1981) and 26, 1862 (1982), Physics Today 44(10),
  36 (1991); **Joos & Zeh**, Z. Phys. B 59, 223 (1985); the decoherence-time table is from **Schlosshauer**, Phys.
  Rep. 831, 1 (2019), Table 1 (Δx = the object's size); **Schlosshauer**, RMP 76, 1267 (2004). **Brune et al.**,
  PRL 77, 4887 (1996); Nobel Prize 2012 (Haroche, Wineland). **Lindblad**, CMP 48, 119 (1976); **Gorini,
  Kossakowski & Sudarshan**, J. Math. Phys. 17, 821 (1976); **Caldeira & Leggett**, Physica A 121, 587 (1983).
* **Klein**, Z. Phys. 37, 895 (1926); **Gordon**, Z. Phys. 40, 117 (1926); **Dirac**, Proc. R. Soc. A 117, 610
  (1928, received 2 January 1928). Hole theory: Proc. R. Soc. A 126, 360 (1930) identified holes with protons; the
  anti-electron is in Proc. R. Soc. A 133, 60 (1931). **Anderson**, Science 76, 238 (1932) and Phys. Rev. 43, 491
  (1933). **Lévy-Leblond**, CMP 6, 286 (1967). **Schrödinger**, Sitzungsber. Preuss. Akad. 24, 418 (1930);
  **Gerritsma et al.**, Nature 463, 68 (2010). **Darwin**, Proc. R. Soc. A 118, 654 (1928); **Gordon**, Z. Phys.
  48, 11 (1928).
* **Fan, Myers, Sukra & Gabrielse**, PRL 130, 071801 (2023): g/2 = 1.00115965218059(13). **Schwinger**, Phys.
  Rev. 73, 416 (1948). **Lamb & Retherford**, Phys. Rev. 72, 241 (1947), "about 1000 Mc/sec"; modern
  2S₁/₂–2P₁/₂ = 1057.847 MHz and 2P₃/₂–2P₁/₂ = 10,969.05 MHz (NIST ASD levels).

Visualization and pedagogy: Ogborn & Taylor, Phys. Educ. 40, 26 (2005); Taylor et al., Comput. Phys. 12, 190
(1998); Hanc, Tuleja & Hančová, AJP 71, 386 (2003); Mullin & Blaylock, AJP 71, 1223 (2003); Galvez et al., AJP 73,
127 (2005); Passante et al., PRST-PER 11, 020135 (2015); Wittmann et al., AJP 70, 218 (2002) and EJP 26, 939
(2005); Caprez et al., PRL 99, 210401 (2007); Batelaan & Tonomura, Physics Today 62(9), 38 (2009); Mayer, Am.
Psychol. 63, 760 (2008); Renkl & Atkinson (2003); Muller et al. (2008); Crouch et al., AJP 72, 835 (2004); the
3Blue1Brown FAQ and SoME guidance; QuVis (St Andrews), PhET (Band Structure, Alpha Decay), Schroeder's two-particle
apps.

On-screen simplifications, stated here for the record:

* The hook's path sum is Huygens' construction (the 2D Green's function's phase and 1/√r fall-off, no obliquity
  factor). The paths' geometry is drawn to scale, except that y is magnified relative to x.
* The Aharonov–Bohm flux tube is infinitely thin and sits inside the slit plate. Its continuous sweep is the
  idealized (unshielded) case; Tonomura's experiment is described separately.
* Gamow's model uses one radius parameter, the assault frequency v/2R, and no preformation factor. The video says
  where it fails worst (N = 126).
* The helium "numerical" value keeps only the monopole (s-wave) part of 1/r₁₂ (the Temkin–Poet model). The
  1s2s pictures are that model's states.
* The which-path fringe picture and the Gleason frame are schematic illustrations of formulas; the HOM counts are
  seeded samples on the ideal curve, not measured data.
* The Dirac simulation is in 1 + 1 dimensions (two-component), where the same Zitterbewegung appears.
