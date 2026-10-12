# Analysis, Built — Part 9: Distributions and the Fourier Transform

Part 9 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 6-9 of *Functional Analysis* and chapter 9 of *Real and Complex Analysis*, in a hook, 12 chapters and an outro.

Test functions and distributions, derivatives of anything (and the sawtooth's series differentiated term by term), supports and the local structure theorem, convolution and mollifiers, the Fourier transform on L^1 and L^2 (inversion with Gibbs, Plancherel), the Schwartz space as a quarter turn, tempered distributions and Poisson summation, Paley-Wiener with a domain-colored transform and contour-shifted inversion, Denjoy-Carleman, Sobolev spaces, fundamental solutions built by shifting contours (Malgrange-Ehrenpreis), and Wiener's Tauberian theorem with the prime number theorem.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis9.compute                # once: every computed item (cached in .cache/analysis9)
python tools/build.py analysis9 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis9_2160p.mp4
python tools/build.py analysis9                   # 1080p30 -> renders/analysis9.mp4
python tools/build.py analysis9 -q l              # fast 480p preview
python tools/export_script.py analysis9           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis9         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Differentiating anything |
| 1 | [`TestFunctions`](s02_test.py) | 1. Test functions |
| 2 | [`Distributions`](s03_distributions.py) | 2. Distributions |
| 3 | [`Calculus`](s04_calculus.py) | 3. Calculus with distributions |
| 4 | [`Structure`](s05_structure.py) | 4. Supports and local structure |
| 5 | [`Convolution`](s06_convolution.py) | 5. Convolution and mollifiers |
| 6 | [`FourierL1`](s07_fourier.py) | 6. The Fourier transform |
| 7 | [`Plancherel`](s08_plancherel.py) | 7. Inversion and Plancherel |
| 8 | [`Schwartz`](s09_schwartz.py) | 8. Tempered distributions |
| 9 | [`PaleyWiener`](s10_paleywiener.py) | 9. Paley-Wiener |
| 10 | [`Sobolev`](s11_sobolev.py) | 10. Sobolev spaces |
| 11 | [`Fundamental`](s12_fundamental.py) | 11. Fundamental solutions |
| 12 | [`Wiener`](s13_wiener.py) | 12. Wiener and the primes |
| 13 | [`Outro`](s14_outro.py) | The ninth row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `delta` | narrowing bumps tested against 10 functions -> phi(0); smoothed steps' derivatives have integral 1 |
| `mollifier` | the C-infinity bump exp(-1/(1 - x^2)): derivatives to order 10 vanish at the edge (sympy) |
| `pv` | <p.v. 1/x, phi> by symmetric truncation at eps = 10^-k, against the odd-part integral |
| `sawcomb` | the sawtooth's series differentiated term by term, tested against a bump -> -1/2 int phi + pi phi(0) |
| `structure` | delta''' + delta' as the 5th derivative of a continuous function, tested against phi |
| `mollify` | mollified delta' blows up like eps^-2; the mollified Cantor measure like eps^(log2/log3 - 1) |
| `pairs` | box <-> sinc, Gaussian <-> Gaussian, triangle <-> sinc^2: FFT against closed forms |
| `plancherel` | Plancherel for random functions; inversion of the box: L^2 convergence with Gibbs' overshoot |
| `poisson` | Poisson summation: sum e^(-pi n^2 t) = t^(-1/2) sum e^(-pi n^2 / t) paleywiener the transform of a bump on a complex grid: growth like e^(|Im z|) |
| `sobolev` | the sawtooth's H^s norms: finite exactly for s < 1/2 fundamental the heat kernel; the Newtonian potential tested against phi; u'' + u = delta with E = sin|x| / 2 |
| `wiener` | translates of a Gaussian approximate a function; translates of sinc^2 stop at the band-limit bound |
| `contour` | u'' + u = delta by shifting the inversion contour past the zeros of 1 - t^2; u = E * f checked |
| `decay` | the transforms of a box, a triangle and a bump: 1/t, 1/t^2, faster than every power |
| `pwshift` | the bump's transform inverted along Im z = y: the same b(x) inside the support, 0 outside |
| `gevrey` | sup |b^(n)| to n = 20: too fast for analyticity, inside the non-quasi-analytic class (n!)^2 |
| `zeta` | the 3-4-1 inequality for zeta, and |zeta(1 + it)| bounded away from 0 |
| `primes` | pi(x) against x / log x and li(x), and Chebyshev's psi(x) / x, up to 10^8, four points per decade |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
