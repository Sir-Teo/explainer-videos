# General Relativity, Derived: From a Falling Elevator to Einstein's Field Equations

A math-heavy explainer, in 19 chapters and four parts, that derives general relativity from
scratch.

* **Part 1, gravity is geometry.** Spacetime and proper time, the equivalence principle,
  gravitational redshift (Pound–Rebka, GPS). Then the central idea: a thrown ball's worldline is
  the one of *maximal proper time*, and expanding the proper time gives Newton's action.
* **Part 2, the mathematics of curvature.** Metrics, Gauss's intrinsic curvature, tensors, the
  geodesic equation and Christoffel symbols, the covariant derivative and parallel transport, the
  Riemann tensor (derived as a commutator), and geodesic deviation. It shows that Newton's tidal
  tensor *is* the curvature of spacetime.
* **Part 3, Einstein's equation.** The stress–energy tensor and its conservation, the Bianchi
  identity, the failure of R_μν = κT_μν, the Einstein tensor and κ = 8πG/c⁴ from the Newtonian
  limit. Then Baez and Bunn's "ball of coffee grounds" reading (and Friedmann's acceleration
  equation), and a second derivation from the Einstein–Hilbert action, closing with Lovelock's theorem.
* **Part 4, solutions and tests.** The Schwarzschild solution derived from the static spherical
  ansatz, then four applications:
  - Mercury's 42.98″ per century from the orbit equation.
  - Light bending of 1.75″ (half from warped time, half from warped space) and the 1919 eclipse.
  - Photon spheres, a ray-traced black hole, and the EHT image.
  - Gravitational waves, from the linearized equations to LIGO's GW150914 data.

**Nothing is a cartoon unless it says so.** Every curvature formula on screen is computed with
sympy from its metric and asserted against the slide (`geometry.py`). Orbits, light rays and the
black-hole images are integrations of Schwarzschild geodesics. Tides and the ball of test particles
are integrations of Newtonian gravity, and parallel transport is an ODE solve on the sphere. The
gravitational-wave chapter shows LIGO's public strain data. Exaggerations are labeled on screen with
their factor, and schematics are labeled `schematic`.

**Watch:** [`published/relativity.mp4`](../../published/relativity.mp4) (1080p, subtitles and chapters embedded).

```bash
python -m videos.relativity.fetch             # optional: re-download GW150914 strain + the EHT image (committed in data/)
python -m videos.relativity.compute           # once: every computed item (~4 min on 4 cores, cached in .cache/relativity)
python -m videos.relativity.geometry          # the symbolic checks on their own (~5 s)
python tools/build.py relativity -q l         # preview
python tools/build.py relativity              # final 1080p30 + subtitles + chapters
python tools/export_script.py relativity      # regenerate SCRIPT.md from the code
python tools/check_narration.py relativity    # Whisper listen test of every narration line
python tools/publish.py relativity            # GitHub-sized copy -> published/relativity.mp4
```

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 1 | `Hook` | Mercury's unexplained 43″/century; G = 8πG T/c⁴ and Wheeler's summary; "the apple falls because time runs slower near the ground"; light bending, GPS clocks, black holes, waves; the plan. | The exact GR orbit equation integrated for a rosette (exaggerated, labeled); a ray fan, a ray-traced black hole, LIGO's strain. |
| 2 | `Newton` | F = GMm/r², g = −∇Φ; Gauss's law (flux independent of the surface) → divergence theorem → ∇²Φ = 4πGρ. Two problems: no time in Poisson's equation (the Sun-vanishes thought experiment on a spacetime diagram) and the unexplained equality m_G = m_I (Apollo 15, Eötvös, MICROSCOPE). | |
| 3 | `Spacetime` | Spacetime diagrams; the invariant interval under a live Lorentz boost (an event sliding on its hyperbola); proper time; the twin paradox at 0.8c (10 vs 6 years) and a family of trips; straight worldlines *maximize* τ; η_μν and the summation convention. | The boost and the event's coordinates, live. |
| 4 | `Equivalence` | Einstein's 1907 "happiest thought"; box on Earth ≡ accelerating rocket, falling box ≡ floating box. Light falls (the beam across the accelerating cabin; 5.5 fm across a 10 m room). Redshift from the Rindler diagram: pulses arrive stretched by 1 + gh/c². Pound–Rebka (2.46 × 10⁻¹⁵); GPS (+45.7 − 7.2 ≈ +38 µs/day, ~11 km/day); g₀₀ = −(1 + 2Φ/c²). | Rindler worldlines and light pulses (ratio asserted = 1 + ah exactly); clock rate vs orbit radius (zero at 1.5 R⊕). |
| 5 | `MaximalAging` | The ball thrown up and caught 2 s later. Of all worldlines between the two events, the most proper time goes to the parabola with peak 4.905 m = gT²/8, Newton's (τ − T = 3.57 × 10⁻¹⁶ s). Gain from height (linear) vs cost of speed (quadratic). Hover/lopsided/too-high paths age less. Expanding τ: −mc²τ = ∫(½mv² − mΦ)dt − mc²T, so δτ = 0 ⇔ mẍ = −m∇Φ. Why the rubber-sheet picture misleads. Tides as the unremovable part of gravity. | τ − T for 121 parabolas, checked against the closed form and a 40-digit mpmath quadrature of the exact square root; three other shapes; a ring of 24 particles falling toward the Earth (exact Newtonian integration, shown until 1.6× stretch). |
| 6 | `IntrinsicCurvature` | Gauss's Theorema Egregium; ds² = g_ij dx^i dx^j (Cartesian, polar, sphere); the metric as a field of Tissot ellipses; a varying metric isn't curvature (polar plane). The 90-90-90 triangle (270°, excess = area/R², Gauss–Bonnet); parallel transport around it returns rotated 90°. | Parallel transport integrated around the octant triangle (turn asserted 90.000°). |
| 7 | `Tensors` | A fixed arrow, three coordinate systems, three sets of components; V′ = (∂x′/∂x)V; vectors as derivatives; covectors as stacks of level lines and ω_μV^μ as a crossing count; one Jacobian per index; zero in one frame ⇒ zero in all; g_μν as dot product, index lowering (arrow → stack). | Components computed per basis. |
| 8 | `Geodesics` | Great circle vs parallel (0.723R vs 0.785R). The geodesic equation from Euler–Lagrange, line by line, and Γ = ½g^{λσ}(∂g + ∂g − ∂g). Sphere: Γ^θ_φφ, Γ^φ_θφ; 12 integrated geodesics meet at the antipode. Γ ≠ 0 in flat polar coordinates: not a tensor; locally inertial coordinates. Newtonian limit Γ^i_00 = ∂_iΦ/c² ⇒ ẍ = −∇Φ. | 12 geodesics integrated with their Christoffel symbols (great circles asserted); all Γs sympy-checked. |
| 9 | `ParallelTransport` | A constant field whose polar components vary; ∇_μV^λ = ∂_μV^λ + Γ^λ_μν V^ν from the product rule; the check ∇_φV^r = 0. Covectors (−Γ); ∇g = 0 + torsion-free ⇒ Levi-Civita = Christoffel. The transport equation; geodesics transport their own tangent. Latitude circles: 2π(1 − cos θ₀) = cap area/R² (180°, 48°, 0°). Foucault's pendulum: 271°/day in Paris. | Transport integrated around latitude circles (holonomy asserted). |
| 10 | `Riemann` | Rotation ∝ area (12 loops, slope 1/R²); δV^ρ = −R^ρ_σμν V^σ δa^μ δb^ν; [∇_μ, ∇_ν]V^ρ = R^ρ_σμν V^σ derived with the cancellations shown; flat ⇔ R = 0; symmetries; 1, 6, 20 components; Ricci, scalar (2/R² for a sphere). Geodesic deviation; c²R^i_0j0 = ∂_i∂_jΦ: tides are curvature; the trace c²R₀₀ = ∇²Φ. | Loop holonomies; the loop-transport sign checked numerically against R (to 0.03%); R^i_0j0 and R₀₀ in the weak field by sympy. |
| 11 | `StressEnergy` | Energy density picks up γ² under a boost (1.5625 at 0.6c), so the source is a rank-2 tensor; T^μν block by block; perfect fluid; ∂_μT^μν = 0 is continuity + Euler; ∇_μT^μν = 0. | |
| 12 | `FieldEquations` | Four requirements; the guess R_μν = κT_μν from c²R₀₀ = ∇²Φ; the Bianchi identity (proof in locally inertial coordinates) and its double contraction; why the guess fails (T would be constant); G_μν, Λ; κ = 8πG/c⁴ via the trace-reversed form; 2.08 × 10⁻⁴³ s²/(kg·m); pressure gravitates. | |
| 13 | `Meaning` | Baez–Bunn: V̈/V = −4πG(ρ + (p_x+p_y+p_z)/c²); a 3D ball of test particles in vacuum (egg, same volume) and in dust (shrinks); Riemann = Weyl + Ricci; 10 − 4 = 6; Friedmann's acceleration equation and the ΛCDM expansion (acceleration from 7.7 Gyr). | 320 particles integrated (vacuum volume constant to O(t³), asserted); ΛCDM a(t) (age 13.8 Gyr, z_acc = 0.63, asserted). |
| 14 | `Action` | S = (c⁴/16πG)∫(R − 2Λ)√−g d⁴x; √−g as true volume; Jacobi's formula; the variation line by line, the Palatini identity's boundary term, T_μν from δS_M; Lovelock's theorem; Hilbert vs Einstein, 20 and 25 November 1915. | |
| 15 | `Schwarzschild` | Static spherical ansatz; the 9 Christoffel symbols and 4 Ricci components; α = −β; (re^{2α})′ = 1; r_s = 2GM/c² from the Newtonian limit; Birkhoff; r_s of the Sun (2.95 km) and Earth (8.87 mm); 60 µs/day at Earth's surface; clock rate √(1 − r_s/r); Flamm's paraboloid; light cones closing; Kretschmann 12r_s²/r⁶; the horizon. | Every component sympy-checked; Ricci-flatness and the Kretschmann scalar asserted. |
| 16 | `Mercury` | Conserved E and ℓ; V_eff with the new −GMℓ²/(c²r³) term vs Newton's; ISCO; the orbit equation u″ + u = GM/ℓ² + 3GMu²/c²; resonance ⇒ Δφ = 6πGM/(c²a(1−e²)); 0.1035″ × 415.2 = 42.98″/century; Venus 8.6″, Earth 3.8″; 43″ ≈ 1/43 of the Moon. | Precession from the exact apsidal integral (to 10⁻¹⁴); the exaggerated rosette integrated from the same equation. |
| 17 | `Light` | Null geodesics; u = sinφ/b + (GM/c²b²)(1 + cos²φ) ⇒ δ = 4GM/(c²b) = 1.75″; half from time, half from space (Einstein 1911: 0.83″); the 1919 eclipse; the photon sphere and b_c = 2.6 r_s; a ray-traced thin disk; the EHT's M87*. | The exact deflection integral at the solar limb (1.7512″); 18 exact null geodesics; two 1280×720 ray traces (shadow size asserted against b_c). |
| 18 | `Waves` | g = η + h; Lorenz gauge; G_μν = −½□h̄_μν ⇒ □h̄ = −16πG T/c⁴: waves at c; TT gauge, + and × on rings of free particles; quadrupole formula and h ~ (r_s/r)(v²/c²); the chirp; GW150914's real strain, its time-frequency map and the GR chirp for 𝓜 = 31 M⊙; 4 × 10⁻¹⁸ m. | LIGO strain whitened and band-passed; Morlet time-frequency map; the leading-order chirp placed by its coalescence time. |
| 19 | `Outro` | Recap over the turning disk; the equation; credits. | |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| the metric g_μν, lengths, spatial curvature (g_rr) | blue |
| proper time τ, clocks, the time part of the metric (g_tt) | teal |
| Newton: the potential Φ, the field g, Newtonian predictions | gold |
| Christoffel symbols, the covariant-derivative correction | green |
| curvature: Riemann, Ricci, the Einstein tensor, tides; GR's predictions | lilac |
| matter: T_μν, ρ, p, masses | deep orange |
| light, photons, light cones | yellow |
| vectors being transported | pink |
| covectors (level-line stacks) | brown |
| gravitational waves h_μν | rose |
| the cosmological constant Λ | indigo |

## Computations (`compute.py`, `geometry.py`)

`geometry.py` computes Christoffel symbols, Riemann, Ricci, the Einstein tensor and the
Kretschmann scalar for any metric with sympy, in Carroll's conventions. It asserts every formula the
video shows:
- the sphere's Γs, R^θ_φθφ = sin²θ and R = 2/R²;
- the flat polar plane's nonzero Γs and zero curvature;
- the four Ricci components of the static spherical ansatz, and the combinations used to solve it;
- Schwarzschild's Ricci-flatness and its Kretschmann scalar 12r_s²/r⁶;
- the weak-field limits Γ^i_00 = ∂_iΦ, R₀₀ = ∇²Φ and R^i_0j0 = ∂_i∂_jΦ.

`compute.py` caches each item in `.cache/relativity/<item>.npz`. The checks run every time an
item is computed, and scenes assert the numbers their narration quotes.

| Item | What | Checks |
|---|---|---|
| `consts` | r_s of the Sun and Earth, 8πG/c⁴, Earth-surface time dilation, solar-limb deflection, Pound–Rebka shift, Sun–Earth light time, LIGO arm change | r_s = 2953 m and 8.87 mm; 2.077 × 10⁻⁴³; 1.751″; 2.46 × 10⁻¹⁵; 499 s; 4 × 10⁻¹⁸ m ≈ 1/420 proton |
| `aging` | τ − T for parabolas of peak 0–12 m (T = 2 s) and three other shapes | numerical = closed form; maximum at gT²/8 = 4.905 m; 3.57 × 10⁻¹⁶ s; the expansion vs the exact √ at 40 digits (mpmath) |
| `rocket` | light pulses from floor to ceiling of a Rindler rocket (gh/c² = 0.5) | received spacing / emitted = 1 + ah exactly |
| `gps` | clock rate in circular orbit vs radius (gravity, speed, net) | GPS +45.7, −7.2, +38.5 µs/day; 11.5 km/day; zero at 1.5 R⊕ |
| `tidal` | 24 particles (ring of 800 km) released at 4 R⊕, integrated until 1.6 R⊕ | relative accelerations = the linear tidal law (on a 1 km ring, 10⁻³) |
| `ball` | 320 test particles: near a point mass (tidal regime) and inside uniform matter | V̈(0) = 0 in vacuum; V̈/V = −4πGρ in matter |
| `transport` | parallel transport on the unit sphere: the octant triangle, four latitude circles, 12 caps | triangle turn 90.000°; holonomy 2π(1 − cos θ₀); angle = area for every cap (10⁻⁶); Foucault 271°/day, 31.8 h |
| `sgeo` | 12 geodesics from one point via the geodesic equation | all meet at the antipode; each lies in a plane through the center; 0.7854 vs 0.7227 |
| `mercury` | apsidal angle from the exact cubic integral for Mercury, Venus, Earth; an exaggerated rosette | 42.98″, 8.62″, 3.84″ per century; agrees with 6πGM/(c²a(1−e²)) to 10⁻⁶; 415.2 orbits/century |
| `light` | exact deflection (cancellation-free integral) at the solar limb and at 3–50 r_s; 18 null rays (Binet form x″ = −1.5h²x/r⁵) | 1.7512″ vs weak-field 1.7512″; second-order term matches; capture ⇔ b < 3√3/2 r_s |
| `bh80`, `bh20` | 1280×720 backward ray traces of a thin disk (3–13 r_s) at inclinations 80° and 20°: crossing radii and angles, photon angular momentum (Doppler), escape directions | shadow half-width = the critical impact parameter as seen from 50 r_s (to 3 pixels); the approaching side is blueshifted |
| `cosmo` | flat ΛCDM a(t) (Planck 2018) | age 13.8 Gyr; acceleration from a = 0.613 (z = 0.632), t = 7.7 Gyr |
| `gw` | GW150914 from `data/gw150914.json`: 35–350 Hz band-pass, the 7 ms shifted and inverted L1 overlay, a Morlet time-frequency map, the leading-order chirp for 𝓜 = 28.6 × 1.09 M⊙ | H1/L1 correlation > 0.5 (0.59); 35 Hz → merger in 0.16 s |

Shading the black hole: Page–Thorne thin-disk flux (with the corrected constant √3/2) times
g⁴ (bolometric Doppler and gravitational shift, g = 1/(u^t(1 − Ωλ))). The disk texture and
colors are illustrative, as the scene says.

## Data

* `data/gw150914.json`, made by `fetch.py`, holds 0.65 s of whitened LIGO strain (H1 and L1)
  around GW150914. It comes from the 32 s, 4096 Hz files of the
  [Gravitational Wave Open Science Center](https://gwosc.org/eventapi/json/GWTC-1-confident/GW150914/v3/),
  and also holds the GWTC-1 parameters (35.6 + 30.6 → 63.1 M⊙, 3.1 M⊙c² radiated, 440 Mpc, z = 0.09).
  Whitening follows the GWOSC tutorial (Welch PSD, 4 s Hann segments).
* `data/eht_m87.jpg` is the Event Horizon Telescope's image of M87*. Credit: EHT Collaboration
  ([ESO eso1907a](https://www.eso.org/public/images/eso1907a/)), licensed CC BY 4.0.

## Fact-check notes and sources

The derivations follow standard texts: S. Carroll, *Spacetime and Geometry* and his lecture notes
([gr-qc/9712019](https://arxiv.org/abs/gr-qc/9712019)); Misner, Thorne & Wheeler, *Gravitation*;
Hartle, *Gravity*; Schutz, *A First Course in General Relativity*. Specific sources:

* **Baez & Bunn**, *The Meaning of Einstein's Equation*, [gr-qc/0103044](https://arxiv.org/abs/gr-qc/0103044)
  (Am. J. Phys. 73, 644, 2005): the ball statement, V̈/V = −½(ρ + P_x + P_y + P_z) with
  8πG = c = 1, and the Friedmann derivation.
* **Luminet**, *Image of a spherical black hole with thin accretion disk*, A&A 75, 228 (1979). The
  redshift 1 + z = (1 − 3M/r)^(−½)(1 + (M/r³)^½ b sin θ₀ sin α) is used in its equivalent
  four-velocity form. The scanned paper's Page–Thorne constant reads √3/3; the correct value is √3/2.
* **Will**, *The Confrontation between General Relativity and Experiment*, Living Rev. Relativ. 17, 4
  (2014), [arXiv:1403.7377](https://arxiv.org/abs/1403.7377): light deflection ½(1 + γ)·4GM/(c²b),
  the split between g₀₀ and g_ij, VLBI tests of γ to ~10⁻⁴, and Mercury.
* **Ashby**, *Relativity in the Global Positioning System*, Living Rev. Relativ. 6, 1 (2003). The
  video's rates (+45.7, −7.2 µs/day) use a ground clock at rest on a spherical Earth of radius
  6,371 km. Ashby, referencing the geoid and Earth's rotation, gives a net 38.6 µs/day; the
  narration says "about 38".
* **History.**
  - Einstein's "happiest thought" is from the unpublished 1920 manuscript *Grundgedanken und
    Methoden der Relativitätstheorie* (Collected Papers vol. 7); the idea dates from 1907
    (*Jahrbuch der Radioaktivität und Elektronik* 4).
  - Einstein's 1911 deflection was 0.83″ (*Ann. Phys.* 35, 898).
  - The November 1915 papers are dated 4, 11, 18 (Mercury: 43″/century) and 25 November (the
    field equations, in trace-reversed form). Hilbert submitted his variational paper on
    20 November 1915; priority is debated, so the video states only the dates.
  - Schwarzschild's letter from the Russian front is dated 22 December 1915; he died 11 May 1916.
  - Le Verrier (1859): ~38″/century; Newcomb (1882): ~43″.
  - Pound & Rebka, PRL 4, 337 (1960): a 22.5 m path, measured shift 1.05 ± 0.10 of prediction;
    Pound & Snider (1965): 1%.
  - Eötvös–Pekár–Fekete (measurements 1906–1908): a few × 10⁻⁹; MICROSCOPE (2022): ~10⁻¹⁵.
  - Apollo 15's hammer and feather: David Scott, 2 August 1971.
* **The 1919 eclipse** (Dyson, Eddington & Davidson, Phil. Trans. A 220, 291, 1920). Sobral was
  observed by Crommelin and Davidson, 1.98″; Príncipe by Eddington and Cottingham, 1.61″. The ±0.12″
  and ±0.30″ are the paper's *probable* errors. Dyson organized the expeditions from Greenwich. The
  result was read on 6 November 1919.
* **GW150914** (Abbott et al., PRL 116, 061102, 2016): detected 14 September 2015, 09:50:45 UTC;
  Livingston first, Hanford 6.9 ms later; peak strain 1.0 × 10⁻²¹. The masses quoted are GWTC-1's
  (Phys. Rev. X 9, 031040, 2019).
* **Lovelock**, J. Math. Phys. 12, 498 (1971); 13, 874 (1972).
* **Cosmology**: Planck 2018 (H₀ = 67.4, Ω_m = 0.315); Riess et al. (1998) and Perlmutter et al.
  (1999).
* **The EHT images**: M87* released 10 April 2019 (6.5 × 10⁹ M⊙); Sgr A* on 12 May 2022.

On-screen simplifications, stated here for the record:

* The weak-field metric in chapter 4 has only g₀₀. The spatial part, −2Φ/c², enters later, in the
  discussion of light bending.
* The rocket's redshift diagram uses gh/c² = 0.5, and the light beam across the cabin uses an
  acceleration ~10¹⁶ g. Both are labeled.
* The "too high", "hover" and "lopsided" worldlines in chapter 5 are three arbitrary non-parabolic
  paths through the same two events; any such path ages less.
* The ball of test particles is integrated with Newtonian tidal forces (the weak-field limit of
  geodesic deviation). The vacuum ball's volume is constant only to order t³ (V = 1 − t⁴/2 + …), so
  the animation stops early.
* The Schwarzschild light cones are drawn in Schwarzschild coordinates. The statement that every
  future-directed path inside r_s leads inward uses better coordinates (Eddington–Finkelstein),
  which the video mentions but doesn't draw.
* The eclipse star field is schematic, with displacements ∝ 1/b exaggerated ~290×.
* The binary and its waveform in chapter 18 are schematic. The LIGO data and the chirp line
  (leading-order quadrupole, detector-frame chirp mass) are not.
