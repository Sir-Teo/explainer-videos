# Analysis, Built — Part 5: Measure and the Lebesgue Integral

Part 5 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapter 11 of *Principles* and chapters 1, 2 and 8 of *Real and Complex Analysis*, in a hook, 12 chapters and an outro.

Why Riemann's integral is not enough (three ways mass escapes), outer measure and null sets (the Cantor set, the rationals, a fat Cantor set), the Vitali set, sigma-algebras and measurable functions, simple functions, the monotone and dominated convergence theorems, Fatou, Egorov and Lusin, the Riesz representation theorem that builds Lebesgue measure from the Riemann integral, and Fubini with its counterexample.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis5.compute                # once: every computed item (cached in .cache/analysis5)
python tools/build.py analysis5 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis5_2160p.mp4
python tools/build.py analysis5                   # 1080p30 -> renders/analysis5.mp4
python tools/build.py analysis5 -q l              # fast 480p preview
python tools/export_script.py analysis5           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis5         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Chapters (26:19)

```
0:00 Limits under the integral, without uniformity
2:37 1. A length for every set
5:08 2. A set with no length
6:54 3. Sigma-algebras and measurable functions
8:52 4. Measures
10:12 5. The integral, and monotone convergence
12:23 6. Fatou's lemma
13:44 7. Dominated convergence
16:04 8. Every positive functional is an integral
17:59 9. Lebesgue measure, and Riemann revisited
19:39 10. Measurable is nearly continuous
20:59 11. Product measures and Fubini
22:37 12. Convolution and the layer cake
24:29 The fifth row of the ledger
```

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Limits under the integral, without uniformity |
| 1 | [`Length`](s02_length.py) | 1. A length for every set |
| 2 | [`Vitali`](s03_vitali.py) | 2. A set with no length |
| 3 | [`SigmaAlgebras`](s04_sigma.py) | 3. Sigma-algebras and measurable functions |
| 4 | [`Measures`](s05_measures.py) | 4. Measures |
| 5 | [`Integral`](s06_integral.py) | 5. The integral, and monotone convergence |
| 6 | [`Fatou`](s07_fatou.py) | 6. Fatou's lemma |
| 7 | [`Dominated`](s08_dominated.py) | 7. Dominated convergence |
| 8 | [`RieszRepresentation`](s09_riesz.py) | 8. Every positive functional is an integral |
| 9 | [`Lebesgue`](s10_lebesgue.py) | 9. Lebesgue measure, and Riemann revisited |
| 10 | [`NearlyContinuous`](s11_lusin.py) | 10. Measurable is nearly continuous |
| 11 | [`Products`](s12_products.py) | 11. Product measures and Fubini |
| 12 | [`Convolution`](s13_convolution.py) | 12. Convolution and the layer cake |
| 13 | [`Outro`](s14_outro.py) | The fifth row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `escapes` | the spike n 1_(0, 1/n], the runaway 1_[n, n+1], the spreading (1/n) 1_[0, n]: integral 1, limit 0 |
| `cantor` | covers of the Cantor set (total (2/3)^n) and of the rationals (total eps); the fat Cantor set (removed lengths 4^-n, measure 1/2, no interval) |
| `vitali` | the orbit of rotation by 1 radian on the circle: dense (its largest gap) |
| `simple` | Rudin 1.17's dyadic simple functions for f = x^2 + sin 5x + 1: sup |s_n - f| <= 2^-n |
| `mct` | min(1/sqrt x, n) on (0, 1]: integrals 2 - 1/n increasing to 2 |
| `dct` | n sin(x/n)/x -> 1 under the lid 1 (integrals n Si(1/n)); the typewriter; Egorov for x^n |
| `riesz` | the Riesz construction for the Riemann integral: mu(V) = sup Lambda f over f < V, for random open V |
| `lusin` | a 100-step function repaired to a continuous one off a set of measure < eps |
| `fubini` | (x^2 - y^2)/(x^2 + y^2)^2 on the unit square: iterated integrals +pi/4 and -pi/4 convolution ||f * g||_1 <= ||f||_1 ||g||_1 for random functions; the layer-cake formula |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
