# Analysis, Built — Part 7: Complex Analysis

Part 7 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 10-14 and 17 of *Real and Complex Analysis*, in a hook, 12 chapters and an outro.

Holomorphic functions as conformal maps, integration and winding numbers, Goursat and Cauchy's formula, power series, the open mapping and maximum modulus theorems, residues and the argument principle, the Schwarz lemma, Runge's theorem, normal families and Montel, the Riemann mapping theorem (with a computed Schwarz-Christoffel map), harmonic functions and the Poisson integral, Weierstrass and Blaschke products, and the Hardy space H^p.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis7.compute                # once: every computed item (cached in .cache/analysis7)
python tools/build.py analysis7 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis7_2160p.mp4
python tools/build.py analysis7                   # 1080p30 -> renders/analysis7.mp4
python tools/build.py analysis7 -q l              # fast 480p preview
python tools/export_script.py analysis7           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis7         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Why is C so much better behaved than R? |
| 1 | [`Holomorphic`](s02_holomorphic.py) | 1. Complex derivatives are rotations |
| 2 | [`Integration`](s03_integration.py) | 2. Path integrals and winding numbers |
| 3 | [`CauchyFormula`](s04_cauchy.py) | 3. Cauchy's formula and its miracles |
| 4 | [`OpenMapping`](s05_openmap.py) | 4. Zeros, open maps, the maximum modulus |
| 5 | [`Residues`](s06_residues.py) | 5. The global Cauchy theorem and residues |
| 6 | [`Schwarz`](s07_schwarz.py) | 6. The Schwarz lemma and three lines |
| 7 | [`Runge`](s08_runge.py) | 7. Runge's theorem |
| 8 | [`NormalFamilies`](s09_montel.py) | 8. Normal families |
| 9 | [`RiemannMapping`](s10_riemann.py) | 9. The Riemann mapping theorem |
| 10 | [`Harmonic`](s11_harmonic.py) | 10. A tour: harmonic functions |
| 11 | [`ZerosProducts`](s12_products.py) | 11. A tour: products and continuation |
| 12 | [`Hp`](s13_hp.py) | 12. A tour: H^p and the shift |
| 13 | [`Outro`](s14_outro.py) | The seventh row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `exp` | e^z from its series: e^(2 pi i) = 1, pi/2 as the first zero of the cosine series, periodicity |
| `conformal` | grids under z^2 and e^z: angles preserved, Jacobians are rotation-scalings; z + 0.4i conj(z) is not |
| `winding` | a random closed curve and the winding numbers of 24 points, from the integral, asserted integers |
| `goursat` | nested triangles: the remainder bound for e^z shrinks like 8^-n; for conj(z) the ratio is stuck |
| `cauchy` | Cauchy's formula at random points; the Fibonacci numbers as contour integrals; roots by the argument principle |
| `maxmod` | |z^2 + e^z| on the closed unit disk: the maximum is on the boundary |
| `residues` | three real integrals by residues, against quadrature; Rouche for z^5 + 3z + 1 |
| `schwarz` | a self-map of the disk with f(0) = 0 obeys |f(z)| <= |z|; the three-lines theorem's log-convexity |
| `runge` | polynomial approximation of 1/z: on a horseshoe the error goes to 0, on an annulus it never drops below 1 |
| `montel` | sin(nz) blows up on a disk; z^n -> 0 locally uniformly; a subsequence of a bounded family |
| `riemann` | the Schwarz-Christoffel map of the disk onto an L-shaped hexagon: vertices to 1e-12, angles kept |
| `poisson` | the Poisson integral of boundary data on the disk, asserted harmonic |
| `products` | sin(pi z) against its Euler product; a Blaschke product's zeros |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
