# Analysis, Built — Part 10: Banach Algebras and the Spectral Theorem

Part 10 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 4 and 10-13 of *Functional Analysis* and chapter 18 of *Real and Complex Analysis*, in a hook, 12 chapters and an outro.

The shift's disc of spectrum without eigenvalues, Banach algebras and the Neumann series, the spectrum (nonempty by Liouville, measured by Gelfand's formula, and the Volterra operator), functions of operators by Cauchy's formula, Gelfand theory and Wiener's 1/f theorem, C*-algebras, operators on Hilbert space, compact self-adjoint operators and the string's modes, multiplication by x and the Born rule, projection-valued measures and the spectral theorem (proved with the whole series), unbounded operators and a circle of self-adjoint extensions, the Cayley transform, Stone's theorem, and what all of it proves about quantum mechanics.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the [top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis.analysis10.compute                # once: every computed item (cached in .cache/analysis10)
python tools/build.py analysis10 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis10_2160p.mp4
python tools/build.py analysis10                   # 1080p30 -> renders/analysis10.mp4
python tools/build.py analysis10 -q l              # fast 480p preview
python tools/export_script.py analysis10           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis10         # Whisper listen test of every narration line
```

The scenes share the series' instruments in [`explainer/analysis`](../../explainer/analysis) and helpers from earlier parts (see [`common.py`](common.py)). The full narration is in [`SCRIPT.md`](SCRIPT.md).

## Scenes

| # | Scene | Chapter |
|---|---|---|
| 0 | [`Hook`](s01_hook.py) | Two meanings of spectrum |
| 1 | [`BanachAlgebras`](s02_algebras.py) | 1. Banach algebras |
| 2 | [`Spectrum`](s03_spectrum.py) | 2. The spectrum |
| 3 | [`SymbolicCalculus`](s04_calculus.py) | 3. Functions of an operator |
| 4 | [`Gelfand`](s05_gelfand.py) | 4. Gelfand theory |
| 5 | [`HilbertOperators`](s06_hilbert.py) | 5. Operators on Hilbert space |
| 6 | [`CompactSelfAdjoint`](s07_compact.py) | 6. Compact self-adjoint operators |
| 7 | [`NoEigenvectors`](s08_noeigen.py) | 7. A spectrum with no eigenvectors |
| 8 | [`SpectralTheorem`](s09_spectral.py) | 8. The spectral theorem |
| 9 | [`Unbounded`](s10_unbounded.py) | 9. Unbounded operators |
| 10 | [`Cayley`](s11_cayley.py) | 10. The Cayley transform |
| 11 | [`Stone`](s12_stone.py) | 11. Stone's theorem |
| 12 | [`QuantumClosure`](s13_quantum.py) | 12. What this proves about quantum mechanics |
| 13 | [`Outro`](s14_outro.py) | The last row of the ledger |

## Computations (`compute.py`)

| Item | What is computed and asserted |
|---|---|
| `shift` | the backward shift's eigenvectors (1, l, l^2, ...) for 200 l in the disc; the forward shift has none; the pseudospectra of N x N sections (a Jordan block: only eigenvalue 0) filling the disc |
| `neumann` | (I - A)^-1 = sum A^n for a random A with ||A|| = 0.8, error <= 0.8^(n+1) / 0.2 |
| `radius` | ||A^n||^(1/n) -> max |eigenvalue| for random matrices; n! ||V^n|| -> 1/2 for the Volterra operator |
| `calculus` | e^A and sqrt(A) by the Cauchy integral around the spectrum, against scipy; spectral mapping |
| `wiener` | 1/f for f = 1.2 + Li_2(e^(i theta)): its Fourier coefficients are absolutely summable (Wiener's 1/f) |
| `normal` | for a normal matrix A* is a polynomial in A; f(A) by eigenvectors = f(A) by interpolation |
| `numrange` | the numerical range of a non-normal 4 x 4 matrix: a convex set containing the eigenvalues |
| `green` | the Green's operator of -d^2/dx^2 on [0, 1]: eigenvalues 1/(n pi)^2, eigenfunctions sin(n pi x); power iteration and deflation; the heat equation by the eigen-expansion against Crank-Nicolson |
| `multop` | multiplication by x on L^2[0, 1]: narrowing bumps are approximate eigenvectors, none is exact |
| `pvm` | a 50 x 50 self-adjoint H: the spectral measure E_(x,x) as weights on the eigenvalues; the ergodic averages of a unitary converge to the projection onto its fixed vectors |
| `twisted` | i d/dx on [0, 1] with f(1) = e^(i theta) f(0): spectrum {2 pi n - theta} |
| `momentum` | -i d/dx, diagonalized by the FFT: F P F^-1 = multiplication by xi |
| `stone` | e^(-itH) for a discretized oscillator by the spectral decomposition and by split-operator steps |
| `hydrogen` | the radial hydrogen problem (l = 0) by finite differences: bound states at -1/(2 n^2), a continuum |
| `commutator` | [x, p] for N x N matrices has trace 0: it cannot be i I |

## Sources

W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976); *Real and Complex Analysis*, 3rd ed. (1987); *Functional Analysis*, 2nd ed. (1991). Theorem numbers on screen are those editions'. Each part's credits scene lists the original authors and the companion texts.
