# Analysis, Built — Part 8: Banach Spaces

Part 8 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapter 5 of *Real and Complex Analysis* and chapters 1-5 of *Functional Analysis*, in a hook, 12 chapters and an outro.

Banach and Fréchet spaces, topological vector spaces, Baire's theorem, the uniform boundedness principle (and the divergent Fourier series it produces), the open mapping and closed graph theorems, Hahn-Banach as separation, duals, weak and weak-star convergence, Banach-Alaoglu, Krein-Milman, compact operators and the Fredholm alternative, and a sampler of applications.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis8.compute                # once: every computed item (cached in .cache/analysis8)
python tools/build.py analysis8 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis8_2160p.mp4
python tools/build.py analysis8                   # 1080p30 -> renders/analysis8.mp4
python tools/build.py analysis8 -q l              # fast 480p preview
python tools/export_script.py analysis8           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis8         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Chapters (22:45)

```
0:00 A continuous function whose Fourier series diverges
1:54 1. Banach spaces and bounded operators
3:29 2. Spaces without norms
5:12 3. Baire's theorem
6:39 4. Uniform boundedness
8:37 5. Open mappings and closed graphs
10:02 6. Hahn-Banach
11:41 7. Dual spaces
12:52 8. Weak convergence
14:22 9. Banach-Alaoglu
15:51 10. Extreme points
17:05 11. Compact operators
18:36 12. Four applications
21:00 The eighth row of the ledger
```

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | A continuous function whose Fourier series diverges |
| 1 | [`Banach`](s02_banach.py) | 1. Banach spaces and bounded operators |
| 2 | [`TVS`](s03_tvs.py) | 2. Spaces without norms |
| 3 | [`Baire`](s04_baire.py) | 3. Baire's theorem |
| 4 | [`UniformBoundedness`](s05_ubp.py) | 4. Uniform boundedness |
| 5 | [`OpenMapping`](s06_openmap.py) | 5. Open mappings and closed graphs |
| 6 | [`HahnBanach`](s07_hahnbanach.py) | 6. Hahn-Banach |
| 7 | [`Dual`](s08_dual.py) | 7. Dual spaces |
| 8 | [`Weak`](s09_weak.py) | 8. Weak convergence |
| 9 | [`Alaoglu`](s10_alaoglu.py) | 9. Banach-Alaoglu |
| 10 | [`KreinMilman`](s11_kreinmilman.py) | 10. Extreme points |
| 11 | [`Compact`](s12_compact.py) | 11. Compact operators |
| 12 | [`Samples`](s13_samples.py) | 12. Four applications |
| 13 | [`Outro`](s14_outro.py) | The eighth row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `lebesgue` | the Lebesgue constants ||D_n||_1 to n = 10^6 (Fejer's sum), against (4/pi^2) log n + 1.27; the continuous near-extremal f_n with s_n(f_n)(0) close to ||D_n||_1 |
| `volterra` | the Volterra operator on L^2[0, 1]: norm 2/pi; singular values 2/((2k - 1) pi) |
| `baire` | nested intervals dodging the rationals; a dense G_delta of measure zero |
| `openmap` | a bounded bijection of R^2 and of l^2 (finite section): T(B) contains the ball of radius 1/||T^-1|| |
| `separation` | two convex polygons separated by a hyperplane through the midpoint of their closest points; gauges |
| `weak` | <e_n, y> -> 0 for 50 random y in l^2; sin(nx) -> 0 weakly; Mazur's averages of sin(nx) |
| `alaoglu` | probability measures on [0, 1] with no limit, and a subsequence whose moments converge |
| `extreme` | extreme points of the l^p balls in R^3 by the splitting test; the L^1 ball has none |
| `compact` | the Green's operator of -u'' on [0, 1]: eigenvalues 1/(n pi)^2, eigenvectors sines |
| `haar` | Haar measure on SO(3) from random unit quaternions: invariance of averages |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
