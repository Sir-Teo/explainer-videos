# Analysis, Built — Part 4: Calculus in Many Dimensions

Part 4 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapter 9 of *Principles of Mathematical Analysis* (and a tour of chapter 10), in a hook, 9 chapters and an outro.

The derivative becomes a linear map: operator norms and the Neumann series, the derivative as the best linear approximation (a contour map zoomed until its level lines are straight), partial derivatives and their museum of failures, the contraction principle and Picard's existence theorem, the inverse and implicit function theorems built from one contraction, higher derivatives and the equality of mixed partials, and a labeled tour of differential forms and Stokes' theorem.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis4.compute                # once: every computed item (cached in .cache/analysis4)
python tools/build.py analysis4 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis4_2160p.mp4
python tools/build.py analysis4                   # 1080p30 -> renders/analysis4.mp4
python tools/build.py analysis4 -q l              # fast 480p preview
python tools/export_script.py analysis4           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis4         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Newton's method, and the contraction behind it |
| 1 | [`LinearMaps`](s02_linear.py) | 1. Linear maps and their norms |
| 2 | [`Derivative`](s03_derivative.py) | 2. The derivative is a linear map |
| 3 | [`Partials`](s04_partials.py) | 3. Partial derivatives are not enough |
| 4 | [`Contraction`](s05_contraction.py) | 4. The contraction principle |
| 5 | [`Picard`](s06_picard.py) | 5. Picard: differential equations in C[a, b] |
| 6 | [`InverseFunction`](s07_inverse.py) | 6. The inverse function theorem |
| 7 | [`ImplicitFunction`](s08_implicit.py) | 7. The implicit function theorem |
| 8 | [`HigherOrder`](s09_higher.py) | 8. Mixed partials, and differentiating under the integral |
| 9 | [`FormsTour`](s10_forms.py) | 9. A tour of integration in many variables |
| 10 | [`Outro`](s11_outro.py) | The fourth row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `newton` | Newton's method on F(x, y) = (x^2 + y^2 - 4, xy - 1): iterates, residuals squaring each step |
| `linmaps` | the operator norm as the largest singular value (the unit circle's image is an ellipse); the Neumann series for an inverse, summed (Rudin 9.8) |
| `derivative` | the derivative as a linear map: tangent-plane residuals |f(p + h) - f(p) - Ah| / |h| -> 0; the contour map zoomed until its level lines are parallel and evenly spaced |
| `museum` | xy / (x^2 + y^2) (partials at 0, not continuous) and x^2 y / (x^2 + y^2) (directional derivatives in every direction, not linear in the direction: not differentiable) contraction cos x = x by iteration, errors under c^n / (1 - c) |x1 - x0|; Newton near a simple root |
| `picard` | Picard iterates for y' = y and y' = x + sin y, sup distances shrinking geometrically |
| `inverse` | the inverse function theorem's contraction phi(x) = x + A^-1 (y - f(x)) for f = (e^x cos y, e^x sin y) |
| `implicit` | the folium x^3 + y^3 = 3xy traced by continuation; its fold where f_y = 0 |
| `mixed` | f = xy(x^2 - y^2)/(x^2 + y^2): f_xy(0, 0) = -1, f_yx(0, 0) = 1; differentiation under the integral |
| `forms` | area factors of a map on a grid against |det J| |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
