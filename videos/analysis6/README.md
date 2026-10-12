# Analysis, Built — Part 6: L^p, Hilbert Space and the Geometry of Functions

Part 6 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 3, 4, 6 and 7 of *Real and Complex Analysis*, in a hook, 15 chapters and an outro.

Convexity and Jensen, Young, Hölder and Minkowski as pictures, the L^p spaces and their completeness (Riesz-Fischer, run on the hook's ramps), inner products and the parallelogram law, nearest points and projections, the Riesz representation of functionals, orthonormal bases and Parseval, Fourier series in L^2 and Fejér, complex measures, Radon-Nikodym, the dual of L^p, differentiation of measures, absolute continuity and the change-of-variables formula.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis6.compute                # once: every computed item (cached in .cache/analysis6)
python tools/build.py analysis6 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis6_2160p.mp4
python tools/build.py analysis6                   # 1080p30 -> renders/analysis6.mp4
python tools/build.py analysis6 -q l              # fast 480p preview
python tools/export_script.py analysis6           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis6         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Which distance between functions? |
| 1 | [`Convexity`](s02_convexity.py) | 1. Convex functions and Jensen's inequality |
| 2 | [`Holder`](s03_holder.py) | 2. Young, Hoelder and Minkowski |
| 3 | [`Lp`](s04_lp.py) | 3. The spaces L^p |
| 4 | [`RieszFischer`](s05_rieszfischer.py) | 4. L^p is complete |
| 5 | [`Hilbert`](s06_hilbert.py) | 5. Inner products and the parallelogram law |
| 6 | [`Projection`](s07_projection.py) | 6. The nearest point |
| 7 | [`RieszHilbert`](s08_rieszhilbert.py) | 7. Every functional is an inner product |
| 8 | [`Orthonormal`](s09_orthonormal.py) | 8. Orthonormal bases, Bessel and Parseval |
| 9 | [`FourierL2`](s10_fourierl2.py) | 9. Fourier series in L^2, and Fejer |
| 10 | [`ComplexMeasures`](s11_complex.py) | 10. Complex measures |
| 11 | [`RadonNikodym`](s12_radon.py) | 11. The Radon-Nikodym theorem |
| 12 | [`DualLp`](s13_dual.py) | 12. The dual of L^p |
| 13 | [`Differentiation`](s14_differentiation.py) | 13. Differentiating measures |
| 14 | [`AbsolutelyContinuous`](s15_absolute.py) | 14. The fundamental theorem, for Lebesgue |
| 15 | [`ChangeOfVariables`](s16_change.py) | 15. Change of variables |
| 16 | [`Outro`](s17_outro.py) | The sixth row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `ramps` | continuous ramps converging in L^1 to a step (||ramp_n - step||_1 = 1/(4n)); no continuous limit |
| `jensen` | Jensen's inequality for exp on 10^4 random weightings |
| `young` | Young's inequality as two areas; Hoelder and Minkowski on random vectors |
| `parallel` | the parallelogram law in L^p[0, 1] for p = 1, 2, 3: equality only at p = 2 |
| `stacking` | Riesz-Fischer's proof run on the ramps: a subsequence with summable increments |
| `projection` | e^x projected onto span{1, x, x^2} in L^2[0, 1]: normal equations vs orthonormal basis |
| `rieszh` | the representer of f -> int f w found from an orthonormal basis |
| `legendre` | Gram-Schmidt on 1, x, ..., x^6 in L^2[-1, 1] gives the normalized Legendre polynomials |
| `fejer` | the Fejer kernel; s_N and sigma_N for the sawtooth (no overshoot) and for a continuous f |
| `variation` | total variation of sin(5x) dx on [0, 2 pi]; the Cantor measure on a null set |
| `radon` | the density d lambda / dm recovered as a limit of ratios, and von Neumann's g = h / (1 + h) |
| `dual` | the dual norm of l^p is the l^q norm, with the extremal vector |
| `lebdiff` | averages over shrinking intervals at 1000 random points; the Vitali covering lemma |
| `cantorac` | the Cantor function: derivative 0 off the Cantor set, total rise 1; its covers of length (2/3)^n |
| `holder` | Hoelder's proof run on two normalized functions: |FG| under |F|^p/p + |G|^q/q (area exactly 1) |
| `lpnorms` | ||2x||_p on [0, 1] rising to the essential sup; x^(-1/2) and 1/x near 0 and at infinity |
| `bessel` | the sign function's Legendre coefficients: Bessel's partial sums filling up ||sign||^2 = 2 |
| `trigdense` | Rudin's kernel c_k ((1 + cos t)/2)^k: trigonometric polynomials converging uniformly (4.24) |
| `unbounded` | |x|^(-1/4) on (-pi, pi): unbounded, not Riemann integrable, its Fourier series converges in L^2 |
| `cpath` | a complex measure as a closed path in C: mu(X) = 0, |mu|(X) = 2 pi (inscribed polygons) |
| `probe` | a functional on C[0, 1] probed with narrowing bumps reveals its measure (density plus an atom) |
| `maximal` | the maximal function of an indicator, and the weak-type estimate |
| `ftc` | x^2 sin(1/x^2): differentiable everywhere, f' not integrable; sqrt(x): absolutely continuous |
| `polar` | the Gaussian integral by polar coordinates: the Jacobian r, and int e^(-x^2) = sqrt(pi) |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
