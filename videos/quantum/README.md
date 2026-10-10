# Quantum Mechanics, Visualized: The Wavefunction, the Schrödinger Equation, and Why [x, p] = iħ

A __LENGTH__-minute, 18-chapter explainer in five parts. It builds quantum mechanics from one experiment,
electrons landing one at a time behind two slits, and is released in the centenary year of the
Schrödinger equation (1926–2026).

- **Amplitudes.** Why probabilities don't add but complex arrows do. The wavefunction as a complex number at every
  point, drawn three ways: a helix, a phasor and a phase color. Born's rule.
- **The Schrödinger equation.** Derived from plane waves. Why ψ must be complex. Heat equation vs. Schrödinger.
  The continuity equation. Wave packets: dispersion, phase vs. group velocity, spreading. The particle in a box,
  quantization by "shooting", stationary states, Bohr frequencies. Quantum carpets and exact revivals. Tunneling,
  and the barrier as an energy filter.
- **The mathematical framework.** Hilbert space and the Hamiltonian as a matrix. Hermitian operators and the
  spectral theorem. Unitary evolution as a bank of clocks. The postulates, the Born rule as Pythagoras, and
  collapse. ⟨x|p⟩, the Fourier transform and [x̂, p̂] = iħ. Momentum as the generator of translations. The
  Heisenberg equation and conservation laws. The Robertson and Schrödinger–Robertson uncertainty relations, derived.
- **Two exactly solvable worlds.** The harmonic oscillator by ladder operators. Coherent and squeezed states.
  Ehrenfest's theorem and Wigner functions. Hydrogen: separation, a short route to the ground state, quantization,
  degeneracy, the orbitals, real orbitals as interference, and the Bohr frequencies as the light atoms emit.
- **Spin and entanglement.** Stern–Gerlach, the Bloch sphere, Pauli matrices, sequential measurements, Larmor
  precession and the 4π spinor. Configuration space, the singlet, CHSH and Bell's theorem, with a quantum and a
  local-hidden-variable simulation side by side.

The emphasis is on the mathematics: every result is derived on screen, one line at a time, with a note saying why
each line follows from the last. **Nothing is a cartoon.** Every wave on screen is a numerical solution of the
Schrödinger equation, by a split-operator FFT, an exact eigen-expansion or a finite-difference eigenproblem. Every
histogram is counted from seeded Born-rule samples. Every number the narration quotes is computed in
[`compute.py`](compute.py) and asserted against theory, either there or in the scene that uses it (see
[Simulations](#simulations-computepy)). Schematics are labeled `schematic`.

**Watch:** [`published/quantum.mp4`](../../published/quantum.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

__CHAPTERS__

</details>

```bash
python -m videos.quantum.compute          # once: every simulation (~15 min on 4 cores, cached in .cache/quantum)
python tools/build.py quantum -q l        # preview
python tools/build.py quantum             # final 1080p30 + subtitles + chapters
python tools/export_script.py quantum     # regenerate SCRIPT.md from the code
python tools/check_narration.py quantum   # Whisper listen test of every narration line
python tools/publish.py quantum           # GitHub-sized copy -> published/quantum.mp4
```

## The visual language

A complex amplitude ψ is never shown as a single colored curve. Its **phase is the hue** and its **size is the
height** (in 1D) or **brightness** (in 2D and 3D). The hue order is the same as the Riemann video's domain coloring:
phase 0 is red, π/2 yellow-green, π cyan and 3π/2 violet. Unlike a plain HSV wheel, the hues here are taken at
constant lightness and chroma in OKLCH, a perceptually uniform space, so no phase looks brighter than another
(`colormap.py`).

The convention is taught before it is relied on (chapter 3). First come arrows along x, then the same arrows
stood up into a 3D helix (x, Re ψ, Im ψ). The camera turns to show that the textbook "wiggle" is only the real part's
shadow, with the imaginary part a quarter cycle behind. Last, each arrow's direction becomes a color. A phase wheel
stays in a corner whenever phase colors are on screen. This follows the physics-education literature: PhET found
phase color confusing when it was shown without explanation (McKagan et al. 2008).

Other choices made to avoid documented misconceptions:

* **Energy and wavefunction are never drawn on the same axis** in the tunneling chapter. The barrier appears as a
  band on the wave plot, and the energy diagram is a separate panel. Drawing ψ on the energy line encourages the
  "tunneling costs energy" error (Wittmann et al. 2005; McKagan et al. 2008), and the chapter shows the opposite:
  the transmitted part has *higher* mean energy.
* **Global vs. relative phase.** Multiplying ψ by e^{iα} changes nothing measurable. But three packets with
  *identical* |ψ|² and different phase winding fly apart (Styer 1996).
* **"Stationary" is not "at rest."** A box eigenstate has zero current but a two-peaked momentum distribution.
* **Uncertainty is a property of the state.** σx σp is computed from states alone, and no apparatus appears in
  the proof.
* **Detection dots are resampled every frame** and labeled as possible outcomes, never drawn as trajectories.
* **Stern–Gerlach:** the lab picture and the Bloch sphere are separate panels, and the sphere shows
  orthogonal states as antipodal.
* **Entanglement** is shown in configuration space (x₁, x₂), not as a string between particles (after Schroeder).

| Concept | Color |
|---|---|
| position x, σx, ⟨x⟩ | blue |
| momentum p, k, φ(p), σp | orange |
| energy E, the Hamiltonian, levels | green |
| time t, clocks e^{−iEt/ħ}, revival times | teal |
| potentials V(x), walls, barriers | grey |
| \|ψ\|², probabilities, detections | warm yellow |
| probability current j | pink |
| iħ, commutators, the uncertainty bound | lilac |
| classical particles, trajectories, bounds | sepia |
| raising / lowering operators a†, a | light green / salmon |
| spin up / spin down, the Bloch vector | amber / periwinkle, pale teal |
| Alice / Bob | teal / magenta |
| Wigner function > 0 / < 0 | amber / blue |

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 1 | `Hook` | Electrons arrive one at a time, yet build interference stripes. What passes through the slits is a complex wave, and detection is random with probability \|ψ\|². The equation is a century old (1926). Roadmap. | 70,000 detections sampled from the simulated arrival density, shown at Tonomura's counts (10, 100, 3,000, 20,000, 70,000); a 1024 × 1024 split-operator solution of a packet through two slits. |
| 2 | `Amplitudes` | P₁₂ ≠ P₁ + P₂. Amplitudes add: \|z₁+z₂\|² = \|z₁\|² + \|z₂\|² + 2\|z₁\|\|z₂\|cos Δφ, derived. Feynman's clock picture. Fringe spacing λL/d, de Broglie λ = h/p (5.36 pm at 50 kV). | Single-slit and double-slit runs. The fringe spacing measured on the simulation (71.0) vs. λL/d = 71.5; dark fringes at path differences of 0.50, 1.49, 2.45 λ. |
| 3 | `Wavefunction` | ψ: ℝ → ℂ; arrows, then a helix, then phase color. Born's rule with P = 0.556 on an interval. Global phase is invisible; momentum is written in the phase (p = ħk). Plane waves. | Exact free evolution of three packets with the same density and k = +1.5, 0, −1.5. |
| 4 | `SchrodingerEquation` | Requirements. The plane-wave derivation (E = ħω, p = ħk). Why ψ is complex: real standing waves vanish everywhere at once. Heat equation vs. Schrödinger. ∂ψ/∂t = −(i/ħ)Hψ as a rotation. The continuity equation and current j, derived. | Heat vs. Schrödinger from the same bump: ∫u² falls to 50%, ∫\|ψ\|² stays at 100%. ∫\|ψ\|² = 1.000000 for a moving packet. |
| 5 | `FreeParticle` | Fourier synthesis of a packet. Dispersion ω = ħk²/2m. Phase velocity ħk/2m vs. group velocity ħk/m. Spreading law σ(t) = σ₀√(1 + (ħt/2mσ₀²)²). Real numbers. | Partial sums of 1–25 plane waves. Exact packet evolution: σ(t) matches the law to 1 part in 10⁴. One tracked crest moves at 1.001 (theory 1). An electron at 1 Å spreads to 5.9 Å in 1 fs; a 1 µg grain at 1 µm takes ~10⁶ years. |
| 6 | `Box` | Separation of variables, the energy eigenproblem. Quantization by shooting. φₙ and Eₙ ∝ n². Stationary states (colors turn, density frozen), with j = 0 but momentum near ±nπħ/L. Superposition: ⟨x⟩ = L/2 − (16L/9π²)cos ω₂₁t. | E₁ = 0.376 eV for an electron in 1 nm. Sloshing period 3.67 fs. The ⟨x⟩ formula asserted numerically. |
| 7 | `Carpet` | A packet in the box as clocks turning at rates ∝ n². Break-up, the quantum carpet, and revivals at T = 4mL²/πħ, with a mirror image at T/2 and two copies at T/4, derived. | Exact 300-term eigen-expansion. Revival overlap > 0.999; half-probability copies at T/4. T = 11.0 fs for an electron in 1 nm. |
| 8 | `Tunneling` | Evanescent waves; the stationary scattering state; T = [1 + V₀² sinh²κa / 4E(V₀−E)]⁻¹ and T ≈ 16(E/V₀)(1−E/V₀)e^{−2κa}. Resonances above the barrier. The barrier as an energy filter. STM, alpha decay, the 2025 Nobel Prize. | Split-operator packet: transmitted 0.1416 vs. ∫T(k)\|φ(k)\|²dk = 0.1418 (vs. 0.131 at the mean energy). Transmitted ⟨k⟩ = 1.033 (incoming 1.000), mean energy +6.7%. κ = 5.12 nm⁻¹ at 1 eV; e^{−2κa} = 0.006 (0.5 nm), 3.5 × 10⁻⁵ (1 nm); STM ×8.8 per Å. |
| 9 | `HilbertSpace` | Sampled ψ as a vector, the inner product, orthonormal sine basis, expansion and Parseval. The 8 × 8 finite-difference Hamiltonian; its eigenvectors are exactly sampled sines. Hermitian ⇒ real eigenvalues, orthogonal eigenvectors. The spectral theorem; U(t) as clocks. | Eigenvalue ratios at N = 8, 64, 1,024 → 1, 4, 9, 16, 25. Partial sums of the carpet packet's series. |
| 10 | `Measurement` | The five postulates. The Born rule as squared shadows (Pythagoras), collapse. Energy measurements on the packet. ⟨A⟩ = ⟨ψ\|A\|ψ⟩, derived. Position and momentum as other bases. | 2,000 Born-rule samples vs. \|cₙ\|² (χ² checked). The first outcomes, E₇ and E₄, with collapse. ΣEₙ\|cₙ\|² = ⟨ψ\|H\|ψ⟩ = 484.73; sample mean 487.1. |
| 11 | `Commutator` | p̂ eigenstates; ⟨x\|p⟩; the momentum wavefunction as a Fourier transform. Gaussians: σx σp = ħ/2. [x̂, p̂] = iħ derived on a test function (on Born's gravestone). e^{−iap̂/ħ}ψ(x) = ψ(x−a) by Taylor series. d⟨A⟩/dt = (i/ħ)⟨[H, A]⟩; symmetry ⇒ conservation. | Partial Taylor sums (up to 30 terms) marching a Gaussian over by a = 2.5. |
| 12 | `Uncertainty` | Cauchy–Schwarz. Robertson's σA σB ≥ ½\|⟨[A, B]⟩\| derived line by line. Equality only for Gaussians. The σx–σp plane. The Schrödinger–Robertson bound with the covariance term. | σx σp for Gaussians (0.500), box states (0.568, 1.670, 2.627, …) and oscillator states (n + ½). A spreading packet keeps σx²σp² − cov² = 1/4 exactly. |
| 13 | `Oscillator` | Why parabolas are universal. a, a† and H = ħω(a†a + ½), with the ½ coming from [x, p]. The ladder, the bottom rung, the Gaussian ground state, Eₙ = ħω(n + ½), Hermite functions. Tunneling into the forbidden region. Correspondence at n = 30. | A 4,001 × 4,001 matrix gives eigenvalues 0.5000, 1.5000, …; P(outside) = erfc(1) = 0.157. |
| 14 | `ClassicalLimit` | Ehrenfest's theorem from the commutator. Coherent states (a\|α⟩ = α\|α⟩) vs. squeezed states. The Wigner function: marginals as shadows, a coherent blob orbiting the classical circle, W < 0 for \|1⟩, cat-state fringes. | Split-operator coherent state: ⟨x⟩ = 4 cos t and σx = 1/√2 throughout. A squeezed state breathes 4×. 81 Wigner functions from the evolved ψ; W₁(0, 0) = −1/π; marginals checked. |
| 15 | `Hydrogen` | The Bohr radius by dimensional analysis. Separation, Yₗᵐ ∝ e^{imφ}, V_eff. The ground state from an ansatz. Quantization by shooting, Eₙ = −13.6 eV/n², degeneracy n². Orbitals; p_x as interference of m = ±1. 1s + 2p sloshing at 2.47 × 10¹⁵ Hz → 121.6 nm. The Balmer lines. | A radial finite-difference matrix (8,000 points) for ℓ = 0, 1, 2 gives −1/2n² for every ℓ. Numerov shooting. P(r) peaks at a₀. Volume renders of 11 orbitals and 48 frames of the superposition. Balmer lines in air: 656.28, 486.14, 434.05, 410.18 nm; Lyman-α 121.568 nm. |
| 16 | `Spin` | Stern–Gerlach (Frankfurt, 1922): a smear vs. two spots. Deriving cos(θ/2)\|↑⟩ + e^{iφ}sin(θ/2)\|↓⟩; the Bloch sphere. Pauli matrices, [Sx, Sy] = iħSz. Sequential measurements, cos²(θ/2), z → x → z. Larmor precession; 360° gives −\|ψ⟩. | 6,000 simulated atoms, classical vs. quantum. 1,000 atoms × 13 angles on cos²(θ/2); z → x → z gives 487 / 513. Electron \|γ\|/2π = 28.0 GHz/T. |
| 17 | `Bell` | Two particles share one ψ(x₁, x₂): product vs. entangled. The singlet; E(a, b) = −cos θ. EPR; CHSH \|S\| ≤ 2 proved in one line. Quantum 2√2 (Tsirelson). No signaling. Experiments: 1972, 1982, 2015 (S = 2.42 ± 0.20), Nobel 2022. | σ(x₂) = 1.14 vs. σ(x₂ \| x₁ = 1.5) = 0.28. 10⁵ pairs per setting: \|S\| = 2.828 (quantum) vs. 1.996 (hidden instructions, A = sign(a·λ)). Correlation curves −cos θ vs. the straight line. |
| 18 | `Outro` | The theory on one screen, a gallery of the computed pictures, and where to go next. | |

## Simulations (`compute.py`)

Every item is computed with ħ = m = 1 (atomic units for hydrogen) and cached in `.cache/quantum/<item>.npz`. The
double-slit movie is stored as `slits_frames.npy`, a memory-mapped float16 file of about 700 MB. Seeded items use
PCG64. Checks run every time an item is computed. Numbers quoted by the narration are also asserted in the
scenes, where they are used.

| Item | What | Checks |
|---|---|---|
| `slits` | 2D split-operator (Strang) solution on 1024², with complex absorbing boundaries. A Gaussian packet (k₀ = 0.75, λ = 8.38) hits a plate with two 20-wide slits 60 apart; the time-integrated current j_x on a screen 512 away gives the arrival density; single-slit runs too. 70,000 detections sampled from P₁₂ (seed 1989). | About 11% passes the slits, split evenly between single slits. Dark fringes at path differences within 0.05 of (m + ½)λ; near-zeros with both slits open, none for P₁ + P₂. |
| `packet` | Free Gaussian (σ₀ = 2, k₀ = 2), exact in Fourier space, plus a tracked phase crest. | σ(t) matches the law to 10⁻⁴; ⟨x⟩ = k₀t; σ_k constant. Crest velocity 1.001 (k₀/2). |
| `carpet` | Infinite well (L = 1), packet x₀ = 0.3, σ = 0.06, k₀ = 30, in 300 eigenstates. A 1,200 × 900 space-time carpet, plus movies. | Σ\|cₙ\|² = 1 − 2 × 10⁻⁸. Overlap with the initial state at T and with its mirror at T/2 > 0.999. Two copies of probability ½ (±0.01) at T/4. |
| `fd` | −½d²/dx² as tridiagonal matrices, N = 8, 64, 1,024. | Eigenvalues equal (1 − cos(nπ/(N+1)))/h² exactly; eigenvectors equal sampled sines; ratios → n² (10⁻⁴ at N = 1,024). E₁ = 0.376 eV for 1 nm. |
| `measure` | 2,000 energy outcomes from \|cₙ\|² (seed 1926). | χ² within 4σ; ΣEₙ\|cₙ\|² = ½∫\|ψ′\|² to 2 × 10⁻³ (484.73). |
| `uncert` | σx σp for Gaussians, box states and oscillator states, plus a spreading Gaussian (with its covariance). | Gaussians 0.5 (10⁻⁶); box ½√(n²π²/3 − 2) (10⁻⁴); oscillator n + ½ (10⁻⁶); σx²σp² − cov² = ¼ (10⁻⁵). |
| `tunnel` | 1D split-operator, 8,000 points, dt = 0.01, through a rectangular barrier (V₀ = 0.7, a = 2.5, exactly 25 cells). | Transmitted within 0.003 of ∫T(k)\|φ(k)\|²dk (0.1416 vs. 0.1418); R + T = 1. Transmitted ⟨k⟩ above the incoming one, mean energy ratio 1.067. dt = 0.01 resolves the kinetic phase up to the grid's highest k (at 0.05, a 0.15% splitting artifact appears at \|k\| ≈ 20). |
| `oscillator` | A 4,001-point finite-difference spectrum; split-operator coherent and squeezed states over two periods; Wigner functions by direct quadrature. | Eₙ = n + ½ to 2 × 10⁻⁴; erfc(1) to 10⁻⁷; ⟨x⟩ = 4 cos t to 2 × 10⁻³; coherent width constant; W₁(0, 0) = −1/π; cat marginal = \|ψ\|². |
| `hydrogen` | Radial finite differences (ℓ = 0, 1, 2); Numerov shooting; radial densities. Rydberg with the reduced mass and Edlén air index. Emission + absorption volume renders (hue = phase) of 11 orbitals, of m = ±1 and p_x, and 48 frames of (1s + 2p)/√2. | Eₙ = −1/2n² for every ℓ (0.6%); P(r) normalized, peak at a₀. H-α (air) 656.28 nm, H-β 486.13, Lyman-α 121.567 (vacuum). |
| `spin` | Stern–Gerlach deflections (classical cos θ uniform vs. ±1); 1,000 atoms × 13 angles; z → x → z (seed 1922). | Every angle within 4 standard errors of cos²(θ/2). |
| `bell` | 10⁵ singlet pairs per CHSH setting from the Born rule; a local model A = sign(cos(α − λ)), B = −sign(cos(β − λ)) (seed 1964). | \|S\| within 0.03 of 2√2 and of 2; E(θ) on −cos θ and on −1 + 2θ/π (0.015); Alice's marginal 50/50. |
| `pair` | A product and an entangled two-particle Gaussian on (x₁, x₂). | Product: conditional width equals marginal width; entangled: conditional < 0.3 × marginal. |
| `extras` | Same-density trio; heat vs. Schrödinger; Taylor translation; the barrier's stationary scattering state (4 × 4 solve); box-state momentum densities. | ⟨x⟩ = kt; ∫u² halves while ∫\|ψ\|² is constant to 10⁻¹⁰; the 30-term Taylor sum equals ψ(x − a) to 10⁻⁶; \|r\|² + \|t\|² = 1 and \|t\|² = T(E) to 10⁻¹². |
| `numbers` | Constants the narration quotes (CODATA 2022 via `scipy.constants`). | 50 kV electron λ = 5.36 pm (relativistic); 1 eV λ = 1.226 nm; 1 nm box: E₁ = 0.376 eV, 3.67 fs, 11.0 fs; \|γₑ\|/2π = 28.02 GHz/T. |

## Fact-check notes and sources

The mathematics is standard. The derivations follow Griffiths & Schroeter, *Introduction to Quantum Mechanics*
(3rd ed.); Zwiebach's MIT 8.04 / 8.05 lecture notes (OCW); Sakurai & Napolitano, *Modern Quantum Mechanics*;
Preskill's Ph219 notes (CHSH and Tsirelson); and Styer, "Quantum revivals versus classical periodicity in the
infinite square well" (Am. J. Phys. 69, 56, 2001). Historical claims were checked against the primary sources:

* **Planck**, talk to the German Physical Society, 14 December 1900 (Verh. DPG 2, 237): ε = hν for the resonators.
* **Einstein**, Ann. Phys. 17, 132 (received 18 March 1905). **Bohr**, Phil. Mag. 26 (1913). **de Broglie**, thesis, Paris, 1924.
* **Heisenberg**, Z. Phys. 33, 879 (received 29 July 1925). **Born & Jordan**, Z. Phys. 34, 858 (received 27
  September 1925), where pq − qp = h/2πi first appears. The relation is engraved on the gravestone of Max and
  Hedwig Born in Göttingen's Stadtfriedhof ([photo, COMSOL](https://www.comsol.com/blogs/a-tour-of-the-famous-scientists-laid-to-rest-in-gottingen-city-cemetery/)).
* **Schrödinger**, "Quantisierung als Eigenwertproblem", Ann. Phys. 79, 361 (Part I, received 27 January 1926)
  through 81, 109 (Part IV, received 21 June 1926), which contains the time-dependent equation. The centenary was
  marked, for example, by the ESI symposium *The World in One Line: Schrödinger's Equation Turns 100* (Vienna,
  January 2026).
* **Born**, Z. Phys. 37, 863 (received 25 June 1926): "the probability is proportional to the square" is a footnote
  added in proof. Nobel Prize 1954.
* **Kennard**, Z. Phys. 44, 326 (1927), proves σx σp ≥ h/4π; **Heisenberg**'s 1927 paper (Z. Phys. 43, 172) does
  not contain ħ/2. **Robertson**, Phys. Rev. 34, 163 (1929). **Schrödinger**, Sitzungsber. Preuss. Akad. Wiss. (1930).
* **Stern & Gerlach**, Frankfurt, February 1922 (Z. Phys. 9, 349, received 1 March 1922), interpreted as space
  quantization at the time; spin came later (**Uhlenbeck & Goudsmit**, 1925). **Pauli** matrices, Z. Phys. 43, 601 (1927).
* **Tonomura et al.**, "Demonstration of single-electron buildup of an interference pattern", Am. J. Phys. 57, 117
  (1989). The figure frames show 10, 100, 3,000, 20,000 and 70,000 electrons. The experiment used an electron
  biprism, the electron analog of two slits; the video says "two openings" and simulates slits. Earlier
  single-electron buildups exist (Merli, Missiroli & Pozzi, 1976).
* **Ehrenfest** (1927). **Talbot** (1836), whose optical self-imaging is the same mathematics as quantum carpets.
  **Gamow** (1928), alpha decay as tunneling.
* **Bell**, Physics Physique Fizika 1, 195 (1964). **CHSH**, PRL 23, 880 (1969). **Cirel'son (Tsirelson)**, Lett. Math.
  Phys. 4, 93 (1980). **Freedman & Clauser**, PRL 28, 938 (1972). **Aspect et al.**, PRL 49, 91 and 1804 (1982).
  **Hensen et al.**, Nature 526, 682 (2015): 245 trials, S = 2.42 ± 0.20, 1.3 km. **Giustina et al.** and **Shalm et
  al.**, PRL 115, 250401 and 250402 (2015), reported p-values rather than S.
* **Nobel Prize in Physics 2022** (Aspect, Clauser, Zeilinger): "for experiments with entangled photons, establishing
  the violation of Bell inequalities and pioneering quantum information science". **2025** (Clarke, Devoret,
  Martinis): "for the discovery of macroscopic quantum mechanical tunnelling and energy quantisation in an electric
  circuit".
* **Constants**: CODATA 2022 via `scipy.constants`. The hydrogen ground state is quoted as −13.6 eV (the Rydberg
  energy, 13.6057 eV, assumes an infinitely heavy nucleus); with the proton's recoil it is −13.598 eV, as the video
  notes. The Balmer lines are standard air wavelengths: 656.28 nm in air vs. 656.46 nm in vacuum for H-α.

Visualization practice: B. Thaller, *Visual Quantum Mechanics* (2000) and *Advanced Visual Quantum Mechanics* (2005),
for phase as hue; P. Kovesi, "Good colour maps" (arXiv:1509.03700), for constant-lightness cyclic maps; S. McKagan et
al., "Developing and researching PhET simulations for teaching quantum mechanics", Am. J. Phys. 76, 406 (2008); D.
Styer, "Common misconceptions regarding quantum mechanics", Am. J. Phys. 64, 31 (1996); D. Schroeder's quantum web
apps (configuration-space pictures of two particles); M. Wittmann, J. Morgan & L. Bao, "Addressing student models of
energy loss in quantum tunnelling", Eur. J. Phys. 26, 939 (2005); A. Kohnle et al., QuVis (St Andrews).

On-screen simplifications, stated here for the record:

* The 2D double-slit simulation has slits as long gaps in a 2D plane (a cross-section of real slits). The
  detector-plate view spreads the dots uniformly along the slit direction. Brightness right of the slit plate is
  boosted ×2, and the video says so on screen.
* Orbital renders integrate \|ψ\|² along each line of sight with a little self-absorption. Each image is scaled to
  its own brightness and size (~n²a₀), as the caption notes.
* The p_x orbital is shown as (ψ₂,₁,₋₁ − ψ₂,₁,₁)/√2 (Condon–Shortley phases), which is proportional to x.
* The Stern–Gerlach screens are Monte Carlo pictures with an assumed beam width; the apparatus drawing is a
  schematic.
* "Hidden instructions" is one specific local model (A = sign(a·λ)). The CHSH bound of 2 holds for every local model,
  as derived on screen.
