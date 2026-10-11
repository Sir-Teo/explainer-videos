# General Relativity, Part 2: Inside Black Holes, Spinning Spacetime, and the Expanding Universe

The sequel to [Part 1](../relativity/README.md), which derived Einstein's equation and the
Schwarzschild solution. Part 2 is a math-heavy explainer in 18 chapters and five parts. It takes the
equation where Part 1 stopped: through the horizon, around a spinning black hole, into the energy
carried by gravitational waves, and out to the whole universe. Units are G = c = 1 throughout, as
the video explains in its first minutes.

* **Part I, inside black holes.** The radial plunge (a cycloid in proper time, frozen in Schwarzschild
  time), the tortoise coordinate and Eddington–Finkelstein coordinates (light cones that tip over), and
  Kruskal–Szekeres coordinates (the full four-region spacetime, r becoming time, and the Einstein–Rosen
  bridge pinching off). Then Penrose's conformal compactification, Schwarzschild's Penrose diagram and
  stellar collapse. Finally, Raychaudhuri's equation derived from the commutator of covariant derivatives,
  focusing, trapped surfaces and Penrose's 1965 singularity theorem.
* **Part II, spinning spacetime.**
  - Gravitomagnetism from the linearized equations, with Lense–Thirring dragging.
  - Geodetic precession derived exactly; the space part is shown as the missing wedge of a cone cut from
    Flamm's paraboloid.
  - Gravity Probe B.
  - The Kerr metric, its anatomy (two horizons, the ergosphere, the ring singularity) and the band of
    allowed angular velocities.
  - Negative energy and the Penrose process; δA ≥ 0 and Christodoulou's irreducible mass.
  - The ISCO and accretion efficiency.
  - Bardeen's shadow, with two ray-traced Kerr images.
* **Part III, gravitational waves, derived.**
  - The retarded solution, then the tensor virial theorem: h_ij = (2/r) Q̈_ij.
  - Isaacson's energy, the 8π/5 angular integral and the quadrupole formula.
  - The binary's luminosity and the chirp, with every factor of 5/256.
  - Hulse–Taylor.
  - Ringdown as a Regge–Wheeler simulation checked against Leaver's quasinormal frequency.
  - GW150914's real ringdown, Hawking's area theorem and GW250114.
* **Part IV, black-hole thermodynamics.**
  - Bekenstein's question.
  - Surface gravity and the first law, derived by differentiating the Kerr horizon area.
  - The four laws.
  - Hawking radiation two ways: the exponential redshift of peeling light rays, Fourier-transformed
    numerically into a Boltzmann factor, and the smooth tip of the Euclidean cigar.
* **Part V, the universe.** The three homogeneous geometries, the FLRW metric, the Friedmann equations
  from the Ricci tensor, ΛCDM's ingredients and histories, the cosmological redshift, the
  Davis–Lineweaver diagram (proper, comoving, conformal), the horizon problem, and the open questions
  (the Hubble tension, DESI).

**As in Part 1, nothing is a cartoon unless it says so.**
- Every metric and curvature statement on screen is checked with sympy (`geometry.py`). That includes
  the Kerr metric's Ricci-flatness, which is verified exactly, component by component.
- Worldlines are integrated geodesics.
- The black-hole images are backward ray traces of Kerr null geodesics. Their shadow agrees pixel for
  pixel with Bardeen's analytic edge.
- The ringdown is a numerical solution of the Regge–Wheeler equation.
- The Hawking spectrum is a numerical Fourier transform.
- The gravitational-wave chapter shows LIGO's public strain data.

Schematics are labeled `schematic`, and the few illustrative choices are listed below.

**Watch:** [`published/relativity2.mp4`](../../published/relativity2.mp4) (1080p, subtitles and chapters embedded).

```bash
python -m videos.relativity2.compute          # once: every computed item (~6 min on 4 cores, cached in .cache/relativity2)
python -m videos.relativity2.geometry         # the symbolic checks on their own (~11 s)
python tools/build.py relativity2 -q l        # preview
python tools/build.py relativity2             # final 1080p30 + subtitles + chapters
python tools/export_script.py relativity2     # regenerate SCRIPT.md from the code
python tools/check_narration.py relativity2   # Whisper listen test of every narration line
python tools/publish.py relativity2 --audio-kbps 64   # GitHub-sized copy -> published/relativity2.mp4
```

The GW150914 ringdown reuses Part 1's strain snapshot (`videos/relativity/data/gw150914.json`), and
the black-hole shading reuses Part 1's disk texture. The narration script is in [`SCRIPT.md`](SCRIPT.md).

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 1 | `Hook` | A spinning black hole, ray-traced; recap of Part 1 (where Schwarzschild's metric misbehaves at r = 2M); the five-part plan; G = c = 1 (M☉ = 1.48 km = 4.93 µs). | The a = 0.99 Kerr image, turning. |
| 2 | `Infall` | E = (1 − 2M/r) dt/dτ conserved; (dr/dτ)² = E² − (1 − 2M/r); the cycloid r = (r₀/2)(1 + cos η). Two clocks: the astronaut's watch (finite, ~35M from 10M) vs the station's (t → ∞). Signals arrive ever later; late-time redshift ∝ e^{t/4M} (197 µs for 10 M☉). τ_max = πM inside; tides 2M h/r³ (2 × 10⁷ g at a 10 M☉ horizon, 10⁻⁴ g at Sgr A*'s, and over a day to live inside M87*). | The fall integrated in η and in t, with the station clock running to ∞; the received signals and their redshift slope 1/4M (asserted). |
| 3 | `Finkelstein` | dt/dr = ±1/(1 − 2M/r) ⇒ the tortoise coordinate r*; v = t + r*; the dr² terms cancel and the Eddington–Finkelstein metric is regular at 2M (Eddington 1924, Finkelstein 1958). The Schwarzschild chart morphs into (t̃, r): cones stop closing and tip over. Outgoing rays linger near, hover on, or fall from the horizon; the astronaut's cone. | Every light cone and ray computed from the metric; the morph is a coordinate transformation, point by point. |
| 4 | `Kruskal` | u = t − r*; U = −e^{−u/4M}, V = e^{v/4M}; UV = (1 − r/2M)e^{r/2M}; ds² = −(32M³/r)e^{−r/2M}dUdV. The Schwarzschild grid morphs into Kruskal's wedge (hyperbolas and spokes). Regions I–IV; r = 0 as a hyperbola; inside, r is time. The Einstein–Rosen bridge embedded at T = const, pinching off (Fuller & Wheeler). | The grid morph; the boosted infaller; the bridge profiles embedded exactly (the T = 0 slice equals Flamm's paraboloid; throat radius asserted against UV). |
| 5 | `Penrose` | arctan compactification; conformal factors preserve light cones. Minkowski's grid folds into a triangle (i±, i⁰, ℐ±). Kruskal → the Penrose diagram, with r = 0 at arctan U + arctan V = π/2. The black hole as the region that can't reach ℐ⁺. A star at 5M collapsing: the exterior is exact (Birkhoff); the event horizon forms at the center before the surface reaches 2M (teleology). | Both morphs; the star's surface in compactified Kruskal coordinates, drawn over the eternal diagram it covers (crosses r = 2M, ends at UV = 1, asserted). |
| 6 | `Focusing` | Lifshitz–Khalatnikov (1963) vs Penrose (1965). B_ab = ∇_b u_a = θ/3 h + σ + ω; dB/dτ from the commutator [∇,∇] = Riemann; the trace gives Raychaudhuri's equation. R_μν u^μ u^ν = 4π(ρ + 3p) is Baez–Bunn's ball. dθ/dλ ≤ −θ²/2 ⇒ caustic within 2/\|θ₀\|. Trapped surfaces (both fronts shrink inside 2M). Penrose's theorem and the idea of its proof; Nobel 2020; Hawking's cosmological version. | The focusing bound and a matter-filled example (ODE, asserted); a parallel beam focused by a mass (exact null geodesics); flash fronts outside and inside the horizon in EF coordinates (asserted to grow / shrink). |
| 7 | `Gyroscopes` | Linearized field equation with mass currents ⇒ g_0i ~ the magnetic vector potential; far field −2J sin²θ/r. ZAMOs circle at ω = 2J/r³; Lense–Thirring precession (a dipole field). Geodetic precession 2π(1 − √(1 − 3M/r)) per orbit (58.8° at 10M, de Sitter 1916). The space part: Flamm's cone unrolled, wedge 2π(1 − √(1 − 2M/r)) = 38° here, 2/3 of the effect in weak fields. Gravity Probe B. | Gyroscope spin parallel-transported around the orbit (asserted vs the closed form); transport on the cone (wedge asserted); GP-B's 6606 and 39.2 mas/yr computed from its orbit. |
| 8 | `Kerr` | The Kerr metric in Boyer–Lindquist form, Ricci-flat; a → 0 Schwarzschild, M → 0 flat; the g_tφ far field matches Part II's. No-hair. Δ = 0 ⇒ r± = M ± √(M² − a²); the ergosurface r = M + √(M² − a² cos²θ); the ring singularity; cosmic censorship. The band of allowed Ω (closing to Ω_H at the horizon; no static observers inside the ergosphere). Light circles swept around by the dragging. | Horizon, ergosurface and ring drawn from the metric as a sweeps 0 → 0.99; the Ω band from g_tt + 2g_tφΩ + g_φφΩ² = 0 (asserted); null directions from the metric. |
| 9 | `Extraction` | E = −p·ξ_t = local energy + ω L; negative-energy orbits inside the ergosphere. The Penrose process (Penrose 1969): +9.5% energy out. E − Ω_H L ≥ 0 ⇒ δM ≥ Ω_H δJ ⇔ δA ≥ 0. Christodoulou's irreducible mass, M² = M_irr² + J²/4M_irr²; up to 29% of an extremal hole's mass extractable (fusion: 0.7%). | A decay at r = 1.4M (a = 0.99) with exact conservation of E and L at the split; both fragments' geodesics; the area change asserted positive; constant-area curves in the J–M plane. |
| 10 | `Shadow` | ISCO vs spin (6M → M prograde, 9M retrograde, Bardeen–Press–Teukolsky); efficiency 1 − E_ISCO: 5.7%, 32% at Thorne's a = 0.998, 42% at extremality. Carter's constant; spherical photon orbits ⇒ Bardeen's (ξ, η) and the shadow edge; circle (√27 M) → letter D. Side-by-side ray traces at a = 0 and a = 0.99, edge-on and nearly face-on (size within 7%). M87*: ~40 µas predicted, 42 µas measured; Sgr A*. | ISCOs by minimizing E (asserted vs BPT); shadow edges from Bardeen's formulas; four 1280×720 Kerr ray traces, their captured pixels equal to Bardeen's interior. |
| 11 | `Quadrupole` | h̄ = 4∫T/\|x − y\| retarded ⇒ h̄_ij = (4/r)∫T_ij; ∂_t²T⁰⁰ = ∂_i∂_jT^ij and two integrations by parts ⇒ h_ij = (2/r)Q̈_ij. Isaacson's ⟨∂h∂h⟩/32π; the TT angular integral 8π/5 ⇒ L = ⅕⟨Q⃛_ij Q⃛_ij⟩ (× G/c⁵). A steel beam: 2 × 10⁻²⁹ W. The binary: Q⃛² = 32μ²a⁴ω⁶, L = (32/5)μ²M³/a⁵; the radiation pattern (8× stronger along the axis). | The angular integral (numerical vs 8π/5 for random Q, asserted); the spiral h₊ field of a binary in its plane; L sympy-checked; the radiation pattern. |
| 12 | `Inspiral` | E = −μM/2a ⇒ ȧ = −(64/5)μM²/a³; t_merge = (5/256)a₀⁴/(μM²). f = ω/π, ḟ ∝ 𝓜^{5/3}f^{11/3}, the chirp mass, f(τ). A GW150914-like inspiral: 30 → 180 Hz, 980 → 310 km. Hulse–Taylor: Peters–Mathews f(e) = 11.86; Ṗ = −2.40 × 10⁻¹²; the periastron-shift parabola; agreement 0.998; ω̇ = 4.23°/yr; the Double Pulsar; merger in ~300 Myr. | The inspiral integrated (vs Peters, asserted); Ṗ from the measured masses and orbit (asserted vs Weisberg & Huang); the cumulative shift curve. |
| 13 | `Ringdown` | Regge–Wheeler: ∂_t²ψ − ∂_{r*}²ψ + V ψ = 0, V = (1 − 2M/r)(ℓ(ℓ+1)/r² − 6M/r³), peak at 3.28M. A pulse hits the barrier: a damped ringing, then a power-law tail. Fit vs Leaver: Mω = 0.3737 − 0.0890i. The photon-sphere picture. GW150914's last cycles with the predicted 251 Hz, 4.0 ms tone. Hawking's area theorem (1971): ≤ 29% radiated for equal masses; GW150914 radiated ~5%. GW250114: areas 2.37 × 10⁵ → 3.73 × 10⁵ km², 4.4σ. | The wave equation solved on a grid; the fitted ringdown vs Leaver's continued fraction (to <1.5% across fit windows, asserted); the Kerr QNM from the `qnm` package; LIGO strain with the predicted damped sinusoid. |
| 14 | `Thermodynamics` | Bekenstein's box of gas (1972). Surface gravity: a hovering rocket's redshifted acceleration → 1/4M; κ = (r₊ − r₋)/2(r₊² + a²). Differentiating A(M, J) gives dM = (κ/8π)dA + Ω_H dJ. The four laws (Bardeen, Carter & Hawking 1973), and why classically T = 0. | The first law and κ sympy-checked; the redshifted acceleration curve. |
| 15 | `Hawking` | Peeling: each factor of 10 closer delays escape by 4M ln 10. A wave stretched exponentially (rate κ); its Fourier transform has negative-frequency content with \|β/α\|² = e^{−2πω/κ}: a Planck spectrum at T = κ/2π = 1/8πM. The Euclidean route: near the horizon ds² = ρ²dτ²/16M² + dρ², smooth only if τ ~ τ + 8πM (Gibbons & Hawking 1977). The cigar vs the cone. Numbers: 6.2 × 10⁻⁸ K per M☉; T = T_CMB at 0.61 Moon masses; S = A/4 = 10⁷⁷ k; ~10⁶⁷ yr. | Outgoing null rays near the horizon (gaps asserted = 4M ln 10); the stretched wave's transform, checked against the exact Gamma-function result and the Boltzmann factor (within 3%); the cigar embedded exactly. |
| 16 | `Friedmann` | Homogeneity and isotropy ⇒ three geometries (sphere, flat, Poincaré disk with measured angle sums). FLRW: ds² = −dt² + a²(dr²/(1 − kr²) + r²dΩ²); Hubble's law. Christoffels, Ricci, G_tt ⇒ the Friedmann equation; the acceleration equation (Part 1's ball); ρ ∝ a⁻³, a⁻⁴, a⁰. Densities vs a (equality at z ≈ 3400, Λ takes over at z ≈ 0.3); ρ_c ≈ 5 protons/m³. A family of a(t): closed, flat, open, de Sitter, ΛCDM. | Triangle angle sums on each geometry; every FLRW curvature component sympy-checked; ΛCDM with radiation integrated (age 13.79 Gyr, asserted); the closed universe recollapses. |
| 17 | `Horizons` | dχ = dt/a ⇒ λ ∝ a. The Davis–Lineweaver diagram: the past light cone (a teardrop), the Hubble sphere, superluminal recession; morph to comoving and to conformal coordinates. Particle horizon 46 Gly; event horizon 16.7 Gly. The CMB (z ≈ 1090, ~370 kyr): sphere at 45 Gly, horizon patches ~1° across, ~10⁴ causally disconnected patches; inflation. The Hubble tension (67 vs 73.5) and DESI's evolving-dark-energy hint. | Light cones, Hubble sphere and horizons computed for Planck ΛCDM (46.1, 16.7, 14.5 Gly; recession = c at z = 1.48, asserted); the CMB patches to scale. |
| 18 | `Outro` | Recap over the Kerr image; G_μν + Λg_μν = 8πG T_μν/c⁴; credits. | |

## Color legend

Part 2 keeps every color from Part 1, and adds five.

| Concept | Color |
|---|---|
| the metric g_μν, lengths, spatial geometry | blue |
| proper time τ, clocks, the time part of the metric | teal |
| curvature, horizons (r = 2M, r±), GR's predictions | lilac |
| matter, stars, masses | deep orange |
| light, light rays and light cones | yellow |
| gravitational waves | rose |
| the cosmological constant Λ | indigo |
| the singularity r = 0 (drawn as a zigzag) | red |
| spin: J, a, Ω, frame dragging, the ergosphere; the rotation ω_ab | lime |
| the expansion θ of a bundle of rays | pale yellow |
| temperature, Hawking radiation | salmon |
| negative-energy orbits (the Penrose process) | periwinkle |
| entropy | light pink |

## Computations (`compute.py`, `geometry.py`, `raytrace.py`)

`geometry.py` reuses the sympy machinery (Christoffel symbols, Riemann, Ricci) and checks:
- Eddington–Finkelstein: the substitution t = v − r*, the cancellation of dr², a nonzero determinant at
  r = 2M, Ricci-flatness, and the outgoing null directions in (t̃, r);
- Kruskal: UV = (1 − r/2M)e^{r/2M} and the conformal factor −(32M³/r)e^{−r/2M}, finite at r = 2M;
- Penrose: the arctan conformal factor 1/(cos²ũ cos²ṽ), and the singularity UV = 1 as the straight line
  arctan U + arctan V = π/2;
- the Kerr metric: Ricci-flat, exactly, in rational coordinates (x = cos θ); flat as M → 0; Schwarzschild
  as a → 0; the far field g_tφ → −2J sin²θ/r; horizons and ergosurface;
- Kerr thermodynamics: κ, Ω_H, A, the first law ∂M/∂A = κ/8π and ∂M/∂J = Ω_H, Christodoulou's formula,
  and κ = 1/4M as the limit of a hovering observer's redshifted acceleration;
- the near-horizon (Rindler) limit used in the Euclidean argument;
- the binary's L = (32/5)μ²a⁴ω⁶, ȧ, ḟ, f(τ) and the merger time;
- the FLRW Christoffels, Ricci tensor, G_tt and G_rr, and the acceleration equation.

`raytrace.py` traces Kerr null geodesics backward from a ZAMO camera at r = 100M, in Mino time, with
numba. Velocities are projected back onto √R and √Θ away from turning points, which keeps the
conserved quantities exact over long paths. A 1280×720 frame takes ~30 s.

`compute.py` caches each item in `.cache/relativity2/<item>.npz`. The checks run every time an item
is computed, and scenes assert the numbers their narration quotes.

| Item | What | Checks |
|---|---|---|
| `consts` | Sun as length/time; infall τ_max and tides for 10 M☉, Sgr A*, M87*; Gravity Probe B; T_H, S, lifetime, T = T_CMB mass; ρ_c; c⁵/G and the steel beam | 1476.6 m, 4.9255 µs; πM = 155 µs (10 M☉), 66.5 s, 27.9 h; 2.1 × 10⁷ g; GP-B 6606 and 39.2 mas/yr; 6.17 × 10⁻⁸ K, 1.049 × 10⁷⁷ k, 2.10 × 10⁶⁷ yr, 0.61 M_Moon; 5.1 protons/m³ |
| `infall` | drop from rest at 10M: τ, t, v, Kruskal coordinates, emitted and received signals | the cycloid's closed form; t(r) numerical = closed form (10⁻⁶); v = t + r*; late-time ln(redshift) slope = 1/4M (to 1%) |
| `bridge` | Kruskal T = const slices embedded as surfaces of revolution | T = 0 is Flamm's paraboloid; throat radius from UV = T²; pinches off at the singularity |
| `collapse` | a star's surface (static at 5M, then free fall) in Kruskal coordinates | crosses r = 2M; ends at UV = 1 (r = 0) |
| `raych` | flash fronts outside and inside 2M; the focusing bound; a parallel beam past a mass | outgoing front grows outside, both shrink inside; θ = −2/λ solves the bound with equality; focusing with matter is faster |
| `gpb` | gyroscope spin transported around circular orbits; transport on Flamm's cone | precession = 2π(1 − √(1 − 3M/r)) (10⁻⁷); wedge = 2π(1 − √(1 − 2M/r)) (10⁻⁶); 2/3 ratio in the weak field |
| `kerr_orbits` | ISCO and efficiency vs spin; photon orbits; the Ω band; a ZAMO infall; the Penrose process | ISCO by minimization = BPT (10⁻⁴); 5.72%, 42.3%, 32.1% (a = 0.998); Ω band closes to Ω_H; the decay conserves E and L exactly, fragment 1 has E < 0 and falls in, fragment 2 escapes; δA > 0 |
| `kerr80`, `kerr20` | 1280×720 Kerr ray traces (a = 0.99) of a thin disk (ISCO–26M) at inclinations 80° and 20° | captured pixels = Bardeen's interior (no mismatch beyond 0.02M of the edge); approaching side blueshifted |
| `kerr80_0`, `kerr20_0` | the same traces at a = 10⁻⁴, shaded identically | as above |
| `shadows` | Bardeen's edge for a = 0 … 0.998, edge-on and face-on | a = 0 is the √27 circle; edge-on extent at a = 0.99 |
| `qnm` | Leaver's continued fraction (ℓ = 2, n = 0, 1); the Regge–Wheeler time-domain ringdown; Kerr QNMs; GW150914's ringdown | Mω = 0.37367 − 0.08896i (Leaver 1985), n = 1 too; `qnm` package agrees (10⁻⁵); fit vs Leaver within 1.5% (ω_R) and 3% (ω_I) across four windows; GW150914 251 Hz, 4.0 ms; GW250114 252 Hz, 4.1 ms |
| `inspiral` | the leading-order inspiral; Hulse–Taylor's decay and periastron shift | a(t) = Peters (10⁻⁹); chirp mass 28.6 M☉ (source); f(e) = 11.857; Ṗ = −2.4021 × 10⁻¹² (Weisberg & Huang: −2.40263, from unrounded masses); ω̇ = 4.2262°/yr (measured 4.2266); ~301 Myr to merge |
| `quad` | the TT angular integral for random Q_ij | = 8π/5 · Q_ij Q_ij (10⁻⁴) |
| `hawking` | an exponentially redshifted wave and its numerical Fourier transform; peeling rays; the cigar | transform = exact Gamma-function result (10⁻⁴); ratio = e^{−2πω/κ} (3%); escape-time gaps = 4M ln 10; cigar tip smooth only at period 8πM |
| `cosmo2` | flat ΛCDM with radiation (Planck 2018): a(t), horizons, light cones, densities; a family of universes | age 13.79 Gyr; particle horizon 46.1 Gly; event horizon 16.7 Gly; Hubble radius 14.5 Gly; v = c at z = 1.48; D(CMB) = 45 Gly; horizon patch ~1.2°; z_eq ≈ 3400, z_mΛ = 0.30; Einstein–de Sitter age 2/3H₀; the closed model recollapses |

Shading the Kerr images: the Page–Thorne flux of a thin Kerr disk (Page & Thorne 1974, in closed form,
zero at the ISCO) times g⁴, where g is the redshift of the disk's circular-orbit gas as seen by the
camera. Brightness is compressed
with a gamma of 0.5 so the inner edge and the lensed far side are both visible, and color is a
monotonic map of the local flux, normalized to the disk's peak. In each side-by-side pair, both images use
the spinning disk's scale: Page–Thorne fluxes at the same accretion rate compare directly, so equal radii get
equal colors and only the spinning disk's inner region runs hotter. The colors are illustrative; the geometry
is exact.

## Fact-check notes and sources

The derivations follow S. Carroll, *Spacetime and Geometry*; Misner, Thorne & Wheeler, *Gravitation*;
E. Poisson, *A Relativist's Toolkit* (Raychaudhuri, congruences, Kerr); R. Wald, *General
Relativity*; Hartle, *Gravity*; Maggiore, *Gravitational Waves* vol. 1 (the quadrupole formula and
the Isaacson tensor); and Baumann, *Cosmology*. Specific sources:

* **Coordinates and diagrams.**
  - Eddington, Nature 113, 192 (1924), wrote the form but did not note that it is regular at the
    horizon. Lemaître (1933) called the singularity "fictive".
  - Finkelstein, Phys. Rev. 110, 965 (1958) ("a perfect unidirectional membrane").
  - Kruskal, Phys. Rev. 119, 1743 (1960), written up by Wheeler; Szekeres, Publ. Math. Debrecen 7,
    285 (1960).
  - Einstein & Rosen, Phys. Rev. 48, 73 (1935); Fuller & Wheeler, Phys. Rev. 128, 919 (1962): the
    throat pinches off.
  - Penrose, PRL 10, 66 (1963); Carter, Phys. Rev. 141, 1242 (1966).
  - Oppenheimer & Snyder, Phys. Rev. 56, 455 (1 September 1939).
  - Infall: τ_max = πM (Lewis & Kwan, PASA 24, 46, 2007).
* **Singularities.**
  - Raychaudhuri, Phys. Rev. 98, 1123 (1955).
  - Lifshitz & Khalatnikov, Adv. Phys. 12, 185 (1963).
  - Penrose, PRL 14, 57 (1965): a non-compact Cauchy surface, a closed trapped surface and the null
    convergence condition imply future-incomplete null geodesics.
  - Hawking & Penrose, Proc. R. Soc. A 314, 529 (1970).
  - Nobel Prize 2020: "for the discovery that black hole formation is a robust prediction of the
    general theory of relativity".
  - Baez & Bunn, [gr-qc/0103044](https://arxiv.org/abs/gr-qc/0103044).
* **Frame dragging.**
  - Lense & Thirring, Phys. Z. 19, 156 (1918); de Sitter, MNRAS 77, 155 (1916).
  - Gravity Probe B: Everitt et al., PRL 106, 221101 (2011). Geodetic −6601.8 ± 18.3 vs −6606.1
    mas/yr; frame dragging −37.2 ± 7.2 vs −39.2 mas/yr; 642 km polar orbit; launched 20 April 2004;
    guide star IM Pegasi. The video's predictions (6604 and 39.05) use the simple formulas with
    a = 7027.4 km and are rounded on screen to 6600 and 39.
  - LAGEOS and LARES: Ciufolini & Pavlis, Nature 431, 958 (2004); Ciufolini et al. (2016). Stated as
    "within a few percent".
* **Kerr.**
  - Kerr, PRL 11, 237 (1963); Boyer & Lindquist, J. Math. Phys. 8, 265 (1967); Carter, Phys. Rev.
    174, 1559 (1968).
  - Penrose, Riv. Nuovo Cim. 1, 252 (1969).
  - Christodoulou, PRL 25, 1596 (1970); Christodoulou & Ruffini, PRD 4, 3552 (1971).
  - Bardeen, Press & Teukolsky, ApJ 178, 347 (1972).
  - Bardeen, in *Black Holes* (Les Houches 1973): the shadow.
  - Page & Thorne, ApJ 191, 499 (1974); Thorne, ApJ 191, 507 (1974): a* = 0.998.
  - Efficiencies 5.72%, 32.1% (a = 0.998), 42.3% (extremal). Extractable fraction 1 − 1/√2 = 29%.
* **EHT.**
  - M87*, 10 April 2019: 6.5 ± 0.7 × 10⁹ M☉, ring 42 ± 3 µas.
  - Sgr A*, 12 May 2022.
  - Non-spinning models are disfavored by GRMHD modeling, but neither spin is robustly measured.
    The video's "about 40 µas" is the a = 0 shadow (2√27 M/D) for 6.5 × 10⁹ M☉ at 16.8 Mpc.
* **Gravitational waves.**
  - Isaacson, Phys. Rev. 166, 1272 (1968).
  - Peters & Mathews, Phys. Rev. 131, 435 (1963); Peters, Phys. Rev. 136, B1224 (1964).
  - Hulse & Taylor, ApJ 195, L51 (1975); Weisberg & Huang, ApJ 829, 55 (2016). Intrinsic
    Ṗ = −2.398(4) × 10⁻¹² vs GR −2.40263(5) × 10⁻¹², a ratio of 0.9983 ± 0.0016; ω̇ = 4.226585°/yr.
  - Double Pulsar: Kramer et al., PRX 11, 041050 (2021), 0.999963(63).
* **Ringdown and the area theorem.**
  - Regge & Wheeler, Phys. Rev. 108, 1063 (1957); Leaver, Proc. R. Soc. A 402, 285 (1985).
  - Stein, J. Open Source Softw. 4, 1683 (2019): the `qnm` package.
  - Hawking, PRL 26, 1344 (1971): the area theorem and the (2 − √2)m bound.
  - GW150914: 3.1 ± 0.4 M☉ radiated; predicted ringdown 251 ± 8 Hz, 4.0 ± 0.3 ms.
  - Isi et al., PRL 127, 011103 (2021).
  - GW250114: LVK, PRL 135, 111403 (2025), [arXiv:2509.08054](https://arxiv.org/abs/2509.08054). Masses
    33.6 + 32.2 → 62.7 M☉, χ_f = 0.68; area increase at 4.4σ. The video's areas (2.37 × 10⁵ →
    3.73 × 10⁵ km²) are computed from the median masses and spins; the press release rounds to
    240,000 and 400,000.
  - Overtone: LVK, PRL 136, 041403 (2026), [arXiv:2509.08099](https://arxiv.org/abs/2509.08099).
* **Thermodynamics.**
  - Bekenstein, Lett. Nuovo Cim. 4, 737 (1972) and PRD 7, 2333 (1973).
  - Bardeen, Carter & Hawking, Commun. Math. Phys. 31, 161 (1973).
  - Hawking, Nature 248, 30 (1974) and Commun. Math. Phys. 43, 199 (1975).
  - Gibbons & Hawking, PRD 15, 2752 (1977).
  - The formula T = ħc³/8πGMk is on Hawking's memorial stone in Westminster Abbey (15 June 2018).
  - The Sun's entropy (~10⁵⁸ k) is from Egan & Lineweaver, ApJ 710, 1825 (2010).
  - The lifetime is the photon-only estimate 5120πG²M³/ħc⁴ ≈ 2.1 × 10⁶⁷ yr; Page's 2013 estimate with
    gravitons is 1.2 × 10⁶⁷ yr. The narration says "around 10⁶⁷".
  - The information problem: the island and replica-wormhole computations (Penington 2019;
    Almheiri et al. 2019) reproduce the Page curve, but the mechanism is not settled. The video
    calls it open.
* **Cosmology.**
  - Friedmann, Z. Phys. 10, 377 (1922); Lemaître (1927); Robertson (1935–36); Walker (1937);
    Hubble, PNAS 15, 168 (1929).
  - Planck 2018 (A&A 641, A6): the video uses H₀ = 67.4 and Ω_m = 0.315, as in Part 1, with
    Ω_r h² = 4.18 × 10⁻⁵.
  - Davis & Lineweaver, PASA 21, 97 (2004): the three-panel diagram, the 46 Gly particle horizon and
    superluminal recession.
  - The horizon problem's ~1° (Baumann's lectures give 1.16°).
  - Inflation: Guth, PRD 23, 347 (1981).
* **Open questions (as of October 2026).**
  - Hubble tension: SH0ES (2025) 73.5 ± 0.9; the Local Distance Network (2026) 73.50 ± 0.81, at
    ~7σ vs Planck+SPT+ACT 67.2 ± 0.4. CCHP's TRGB value (~70.4) sits between. The video says
    "five to seven sigma".
  - DESI DR2 (2025) prefers evolving dark energy at 2.8–4.2σ depending on the supernova sample, with
    no 5σ claim. Full-survey results are expected in 2027.

On-screen simplifications, stated here for the record:

* In chapter 5 the star's surface and everything outside it are exact, drawn in compactified Kruskal
  coordinates. The collapse is slid in Schwarzschild time (a boost of U and V, an exact symmetry) so the
  surface crosses the horizon mid-diagram. The star's interior is a shaded region, and the standard
  collapse diagram beside it is schematic, labeled so.
* The proof sketch of Penrose's theorem is a schematic, labeled so.
* The stretched wave in the redshift derivation (chapter 17) is schematic. The diagram after it is
  computed.
* The Kerr images use illustrative colors and a gamma-compressed brightness (above). The comparison
  pairs (a = 0 vs a = 0.99) are traced identically and shaded on one temperature scale.
* Gravity Probe B's predictions use the leading-order formulas for a circular polar orbit. The
  official analysis includes Earth's oblateness and the orbit's actual shape (6606.1 and 39.2).
* "A few hundred thousand years" for the CMB (narration): this model gives ~370,000 years.
* The Kerr Penrose-process example uses a decay at r = 1.4M with fragments of 5% rest mass, chosen so
  the escaping fragment is clearly visible. Penrose's maximum gain for a single decay is
  (√2 − 1)/2 ≈ 21%.
* The inspiral animation's orbit is drawn with the leading-order (Newtonian + quadrupole) dynamics.
  Its last few hundred kilometers, where that breaks down, are not shown.
