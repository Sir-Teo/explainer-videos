# The Navier–Stokes Equations, Derived and Visualized

A 28-minute, 14-chapter explainer that builds the incompressible Navier–Stokes
equations from Newton's second law, deriving every term on screen. It then
shows what the equations do, using real simulations, and covers the open
mathematics: the Millennium Prize problem and the 2026 claimed forced blow-up.

**Watch:** [`published/navier_stokes.mp4`](../../published/navier_stokes.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

- `0:00` Every swirl obeys one equation
- `1:21` Describing a fluid: fields
- `2:46` F = ma for a fluid parcel
- `4:04` Acceleration: the material derivative
- `7:07` The pressure force
- `8:59` The viscous force
- `11:57` Conservation of mass
- `13:41` What decides the pressure?
- `15:30` Putting it together
- `17:00` The Reynolds number
- `19:34` Instability and turbulence
- `21:14` Vortex stretching and the $1M question
- `23:39` 2026: OpenAI's forced blow-up claim
- `27:10` Recap

</details>

```bash
python -m videos.navier_stokes.simulate        # once: precompute footage (~40 min, cached in .cache/sims)
python tools/build.py navier_stokes -q l       # preview
python tools/build.py navier_stokes            # final 1080p30 + subtitles + chapters
python tools/export_script.py navier_stokes    # regenerate SCRIPT.md from the code
```

## Outline

| # | Scene | What it establishes | Derivation on screen |
|---|---|---|---|
| 1 | `Hook` | Kármán vortex street (LBM, Re = 150). The equation is F = ma for fluid parcels. | — |
| 2 | `VelocityField` | Continuum view: velocity field **u**(**x**,t), pressure p. 4 unknowns. | — |
| 3 | `NewtonForParcels` | m = ρ dV, so ρ**a** = force per volume. Three kinds of force. | F = ma → ρa = F/dV |
| 4 | `MaterialDerivative` | Steady nozzle: ∂**u**/∂t = 0 yet parcels accelerate. Advection = centripetal acceleration. Nonlinearity. | chain rule → D**u**/Dt = ∂**u**/∂t + (**u**·∇)**u** |
| 5 | `PressureForce` | Only pressure *differences* push. Why vortex cores have low pressure. | box faces + Taylor → −∇p; ρ\|u\|²/r = ∂p/∂r |
| 6 | `ViscousForce` | Shear stress, net force ∝ curvature. Laplacian = "neighbors' average minus me". Smoothing. Water vs honey (spectral sim). | τ = μ ∂u/∂y → μ ∂²u/∂y² → μ∇²**u**; Taylor stencil for f″ |
| 7 | `Incompressibility` | 3 equations, 4 unknowns. Divergence: source, sink, swirl. Nozzle U₁A₁ = U₂A₂. | box flux → ∇·**u** = 0 |
| 8 | `PressureEnforcer` | Pressure has no evolution equation. It is a Lagrange multiplier. Stagnation flow. Instant action (sound speed). | div of momentum eq. → ∇²p = −ρ∇·[(**u**·∇)**u**] |
| 9 | `FullEquation` | Assembly, ν = μ/ρ, reading it as a sentence, initial and no-slip conditions. | template → full system |
| 10 | `ReynoldsNumber` | Inertia vs viscosity. Dynamic similarity. Cylinder at Re = 1, 40, 150, 1000. Re of bacteria up to airliners. | scaling → Re = UL/ν; nondimensionalization → 1/Re |
| 11 | `Turbulence` | Kelvin–Helmholtz roll-up (spectral). Richardson cascade. 2D inverse cascade (spectral). | — |
| 12 | `MillenniumProblem` | Blow-up question, the $1M prize, vortex stretching, why 2D is solved, Leray and CKN. | curl → vorticity equation with (**ω**·∇)**u** |
| 13 | `ForcedBlowup` | Sept 2026: OpenAI's claimed forced blow-up. Fefferman's options A–D. Cascade idea. Status and caveats. | — (theorem statement only) |
| 14 | `Outro` | Recap over the vortex street. | — |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| velocity **u**, streamlines | blue |
| pressure p, −∇p | red (pressure maps: dark = low, bright red = high) |
| ∂**u**/∂t (local change) | teal |
| (**u**·∇)**u** (advection, the nonlinear term) | yellow |
| viscosity μ, ν, ∇²**u** | green |
| external force **f** | purple |
| divergence ∇·**u**, vorticity **ω** | orange |
| vorticity maps in simulations | blue = clockwise, orange = counter-clockwise |

## Simulations (`simulate.py`)

| Name | Solver | Used in |
|---|---|---|
| `cyl_re150`, `cyl_re1`, `cyl_re40`, `cyl_re1000` | D2Q9 lattice-Boltzmann, 714×240 lattice, D = 36. Re = 1000 uses a Smagorinsky sub-grid model. | 1, 10, 14 |
| `kh` | pseudo-spectral vorticity, 384², double shear layer + passive dye | 11 |
| `turb` | pseudo-spectral, 384², decaying 2D turbulence | 11 |
| `viscous_pair` | pseudo-spectral, 256², same initial field at ν = 4·10⁻⁴ and 2·10⁻² | 6 |

All runs are 2D. The narration says so, and points out where real 3D flows differ.

## Fact-check notes and sources

* **History.** Navier presented his equations in 1822, derived from a molecular model. Stokes gave the continuum derivation in 1845. Leray proved global weak solutions in 1934 (*Acta Math.* 63). Caffarelli–Kohn–Nirenberg proved partial regularity in 1982 (*CPAM* 35): the singular set has zero 1D parabolic Hausdorff measure. Global regularity in 2D is classical (Leray, Ladyzhenskaya).
* **Clay problem.** C. Fefferman, [official problem description](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf). Statements (A) and (B) are global smoothness with f = 0 on ℝ³ and on the torus. Statements (C) and (D) are breakdown, where a smooth force satisfying decay bounds is allowed.
* **Reynolds numbers** are order-of-magnitude values. A swimming bacterium is ~10⁻⁴ (Purcell, *Life at low Reynolds number*, 1977, where coasting distance is ≪ 1 Å). Aortic blood flow is ~10³. A human swimmer is ~10⁶. Flow over an airliner wing is ~10⁷. The cylinder wake first sheds vortices at Re ≈ 47.
* **Richardson's rhyme** is from *Weather Prediction by Numerical Process* (1922).

### Sources for Part 13 (the 2026 claim)

The OpenAI post itself returned HTTP 403 to automated fetching. The wording
used in the video is therefore taken from the coverage and statements below,
and is deliberately limited to points they agree on.

* OpenAI, *On the Navier–Stokes Millennium Prize Problem*, 8 Sep 2026: <https://openai.com/index/navier-stokes-solution/>
* K. Kakaes, *AI Has Solved One of Math's $1 Million Millennium Prize Problems*, Quanta Magazine, 8 Sep 2026: <https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/>
  * Fefferman quote: "I was thrilled that the problem was solved."
  * Córdoba–Martínez-Zoroa "infinite cascade" of layers; earlier constructions had non-smooth forcing.
  * ~10,000 agents, 88 h, Lean formalization by AI in a further 17 h.
* T. Buckmaster, public statement, 7–8 Sep 2026: <https://cims.nyu.edu/~tristanb/statement.pdf>
  * Buckmaster and Alpöge's Lean-verified forced blow-up results for IPM, Boussinesq and 3D Euler.
  * The precise statement relayed by OpenAI: "Existence of forced blowup in R³ and T³ … option c and d in Fefferman".
  * The priority dispute, from Buckmaster's side.
* The Tufts Daily, *Mathematicians still checking the Navier-Stokes proof that OpenAI claims to have solved*, 24 Sep 2026: <https://www.tuftsdaily.com/article/2026/09/mathematicians-still-checking-the-navier-stokes-proof-that-openai-claims-to-have-solved>
  * The forced case is the one addressed; the unforced case remains open.
  * Clay recognizes solutions only after publication and vetting.
* The Next Web, 8 Sep 2026: <https://thenextweb.com/news/openai-navier-stokes-claim-verification-credit>
  * The verification and credit disputes. OpenAI's denials (Mark Chen, Sébastien Bubeck).
  * OpenAI will not claim the prize.
* S. Willison, *Some thoughts on the Navier–Stokes Millennium Prize Problem*, 8 Sep 2026: <https://simonwillison.net/2026/Sep/8/on-navier-stokes/>
  * Quotes from the OpenAI post: timeline, token counts, Lean via GPT-6 Astra.
* Theorem as summarized by later preprints: for every ν > 0 there is a force and a smooth solution on ℝ³×[0,1) with compact spatial support and bounded L² norm whose velocity norm blows up as t → 1. See e.g. arXiv:2609.23868.

The scene describes the status **as of October 2026**: the claim was announced, independent checking was in progress, Clay recognition was pending, and the unforced question was still open. Update `s13_forced_blowup.py` if that changes.
