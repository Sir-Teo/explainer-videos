# The Riemann Hypothesis, Visualized: Primes, Zeros, and the 2026 Quasi-Riemann Proof

A 16-chapter explainer in four parts. It builds the Riemann hypothesis from
prime counting, Euler's product and analytic continuation. It shows how the
zeros of zeta control the primes, through the explicit formula, the error
term, Möbius cancellation and Dirichlet L-functions. Then it explains OpenAI's
October 2026 claimed proof of the **quasi-Riemann hypothesis**, that no zero of
ζ or of any Dirichlet L-function has real part greater than 7/8. It walks
through how the proof works, following the 49-page 11/12 paper's own outline,
and ends on what has been verified and what the result does *not* prove.

Every number, curve and point on screen that comes from mathematics is computed,
not drawn. That covers the zeros, prime counts, the Mertens walk, the domain
coloring, Gauss sums, Kummer's angles, the explicit-formula waves and the
"spectrum of the primes". Schematics are labeled `schematic`.

**Watch:** [`published/riemann.mp4`](../../published/riemann.mp4) (1080p, subtitles and chapters embedded).

<!-- CHAPTERS -->

```bash
python -m videos.riemann.compute          # once: real-math footage (~4 min on 4 cores, cached in .cache/riemann)
python tools/build.py riemann -q l        # preview
python tools/build.py riemann             # final 1080p30 + subtitles + chapters
python tools/export_script.py riemann     # regenerate SCRIPT.md from the code
python tools/check_narration.py riemann   # Whisper listen test of every narration line
python tools/publish.py riemann           # GitHub-sized copy -> published/riemann.mp4
```

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 1 | `Hook` | Primes look random but count smoothly. Riemann's formula rebuilds the staircase from waves, one per zero. RH, then the October 2026 claim. Roadmap. | Primes ≤ 100; π(x) to 10⁵ vs li(x); Riemann's explicit formula for π(x) with 0–200 zero pairs (mpmath `ei`, `riemannr`). |
| 2 | `CountingPrimes` | π(x). The average gap grows by ln 10 per decade, so the density is 1/ln x (Gauss). li(x), the PNT, and an error with about half as many digits as π(x). | π(10ᵏ) sieved here to 10⁹ and asserted against OEIS A006880; li(10ᵏ) − π(10ᵏ) to 10²⁴; density measured just below 10⁶. |
| 3 | `EulerProduct` | ζ(s), ζ(2) = π²/6, the divergent harmonic series. The sieve derivation of Euler's product. Unique factorization. Infinitely many primes. | — |
| 4 | `ComplexZeta` | n⁻ˢ as length × rotation. Partial sums as a spiral of arrows. Divergence for σ < 1. The spiral's center *is* the continuation, ζ(s) = lim(Σ n⁻ˢ − N¹⁻ˢ/(1−s)). The first zero. | Live partial sums; center checked against `mpmath.zeta`. |
| 5 | `ZeroLandscape` | Domain coloring of ζ. The pole, the trivial zeros, the critical strip, zeros on Re s = ½. The functional equation and the four-fold symmetry. RH. Hardy's Z, and what is known about zeros on the line. | ζ on a 1170×900 grid (mpmath); Z(t) for t ≤ 52, asserted to have exactly 10 sign changes. |
| 6 | `ExplicitFormula` | Chebyshev's ψ. von Mangoldt's explicit formula. ρ = β + iγ: γ is the frequency, β the growth rate. ψ rebuilt from 1…1000 zeros. In reverse, a cosine sum over prime powers peaks at the zeros. | First 1000 zeros (`mpmath.zetazero`); the 78,734 prime powers < 10⁶; spectrum peaks asserted within 0.15 of the true ordinates. |
| 7 | `ErrorTerm` | Wave size x^β. Θ = sup Re ρ sets the error. RH ⟺ Θ = ½ (von Koch). Zero on Re s = 1 excluded (1896). Zero-free regions pinch toward 1 (shown to scale). The quasi-RH. | The 1 − 1/(5.56 ln t) region drawn to scale on a log-height axis. |
| 8 | `MobiusRandomness` | μ(n); 1/ζ = Σ μ(n)n⁻ˢ. Mertens' M(x) next to a coin-flip walk. RH ⟺ M(x) = O(x^{½+ε}) (Littlewood). Cancellation ⇒ zero-free half-plane. | μ and M to 10⁷ (max \|M\|/√x = 0.566 beyond x = 200); a seeded random walk. |
| 9 | `DirichletL` | The mod-4 prime race (first lead change at 26,861). χ₄ and L(s, χ). GRH. The Landau–Siegel "ghost" and Siegel's ineffectivity. Uniformity. Consequences of the claim. | Race to 10⁵ (first flip asserted = 26,861, Leech 1957); class totals to 10⁷. |
| 10 | `Announcement` | The release (722 manuscripts, 372 families, ~4,000 problems; zeta work an exception to the fixed procedure). Family 003's three manuscripts. The theorem. The ⅛–⅞ band. The Lean statement. | Lean statement copied from `lean/ComparatorChallenges/QuasiRiemannHypothesis.lean`. |
| 11 | `EisensteinWorld` | ℤ[ω], six units, norm, Eisenstein primes. ζ_K = ζ·L(s, χ₋₃), and L_K(s, χ∘N) = L(s, χ)L(s, χχ₋₃). The sextic residue symbol: periodic and multiplicative, and trivial on sixth powers. | Eisenstein primes in a disk; the 12 integers of norm 7; (u/π)₆ for π = 4 + ω, computed by modular arithmetic. |
| 12 | `Amplification` | The goal: a power saving for one Möbius sum A₁(D). Embed it in the family A_u(D). The crucial mean-square estimate. Copies at u = p⁶. H^{1/6}\|A₁\|² ≲ DH ⇒ \|A₁\| ≲ D^{11/12}. | A *toy* family with quadratic symbols over ℤ (D = 4000, u ≤ 3000): copies at u = p² cluster at A₁ (asserted). |
| 13 | `ThetaReflection` | The large sieve as Bessel's inequality. Poisson summation (Jacobi's identity, both sides computed). Gauss sums. μ is absorbed (the Hasse / Heath-Brown identity). Kummer's 1846 angles. The cubic theta function. χ⁻¹χ⁻² = χ⁻³ = ±1. Heath-Brown's quadratic large sieve. | A sextic Gauss sum mod 37 (\|G\| = √37 asserted); Kummer sums for all 3,014 primes p ≡ 1 mod 3 below 60,000 (24 : 14 : 7 for p < 500, asserted). |
| 14 | `Descent` | Cube layers in the theta coefficients; Möbius inversion. The recursion that shrinks both scales (schematic). How the 199-page paper gets from 11/12 to 7/8. The lineage of ingredients. | — |
| 15 | `Status` | Not peer reviewed. The Lean formalization and what it does and doesn't buy. Early reactions. What follows if it holds. What it does not do: RH remains open. | — |
| 16 | `Outro` | Recap and credits. | |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| primes, π(x), ψ(x), Eisenstein primes | blue |
| the smooth prediction (li, x, R) | green |
| nontrivial zeros, the critical line, the waves they make | yellow |
| proven (or claimed) zero-free regions, the 7/8 line | teal |
| hypothetical off-line zeros, Landau–Siegel zeros | red |
| μ(n), M(x), Möbius sums A_u(D) | lilac |
| Dirichlet characters, residue symbols | orange |
| Gauss sums | pink |
| theta functions, the reflection | gold |
| the large sieve | pale green |

## The real-math footage (`compute.py`)

| Item | What | Check |
|---|---|---|
| `zeros` | ordinates of the first 1000 nontrivial zeros (`mpmath.zetazero`) | γ₁ = 14.134725141734693 |
| `primes` | odd-only sieve to 10⁹; π(x), ψ(x) staircases; li(10ᵏ) − π(10ᵏ) at 40 digits | π(10ᵏ) = OEIS A006880 for k ≤ 9 |
| `mobius` | μ and M(x) to 10⁷ | — |
| `race` | π(x; 4, 3) − π(x; 4, 1) to 10⁷ | first lead change at 26,861 |
| `landscape` | ζ(s) on σ ∈ [−9, 4], t ∈ [−3, 33] | — |
| `hardy` | Z(t), 0 ≤ t ≤ 52 | 10 sign changes = 10 zeros |
| `riemann_pi` | R(x) − Σ 2Re R(x^ρ) (first three Möbius terms of R(x^ρ)), 200 zero pairs | median error 0.09 at K = 200 |
| `kummer` | Σₓ e(x³/p) for all 3,014 primes p ≡ 1 (mod 3) below 60,000 | \|cos θ_p\| ≤ 1 |
| `toy_family` | A_u = Σ_{D<n≤2D, n odd squarefree} μ(n)(u/n) W(n/D) | — |
| `spectrum` | −Σ_{n≤10⁶} Λ(n) w(n) n^{−½} cos(t ln n), cos² taper | every peak in 8 < t < 60 within 0.15 of a zero |

## Fact-check notes and sources

### The October 2026 claim (Parts 3–4)

Everything said about the claim is taken from the primary materials in
[`github.com/openai/math`](https://github.com/openai/math), at commit `adc7f12`
(Oct 6, 2026, 14:58 PDT). Statements about reception come from the press
coverage listed below. The status described is **as of October 7, 2026**.
Update `s15_status.py` and this file if the status changes.

* **Release facts.** From the README: 722 manuscripts in 372 families, about 4,000 problems posed, an unreleased internal model, and on average three hours of ChatGPT Pro thinking per result. "Exceptions to this fixed procedure include work on a zero-free region for the Riemann zeta function and proof of the Hodge Conjecture for CM abelian varieties. Additionally, the writeup for the Re(s) > 11/12 zero-free region for the Riemann zeta function was human edited for readability." The README also says: "Some of the unformalized results could have issues."
* **Family 003** (`CONTENTS.md`, `overview.tex`):
  * *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8*, Sept 30, 2026, 199 pages. Theorem 1.1: every finite-order Hecke L-function over ℚ(√−3) has no zero in Re s > 7/8, and the same holds for every Dirichlet L-function, including ζ. The paper states: "The Riemann hypothesis remains open."
  * *The Quasi-Riemann Hypothesis* (alternate 11/12 proof), Oct 5, 2026, 49 pages. Chapters 11–14 follow its §2 outline: Möbius power saving ⇒ zero-free half-plane; the sextic family A_u(D); the mean square (2.3) ≪ D^{1+ε}H with H = D^{1+ϑ}; A_{p⁶}(D) = A₁(D) + O(D/Y); |A₁|² ≪ D^{1+ε}H^{5/6} + D²H^{−1/3}; Poisson summation and the identity μ(n)γ₋₁(n) = χ_n(−1)G(n)⁻¹ᾱ(n)γ₂(n) (after Hasse and Heath-Brown); Patterson's formula for the cubic theta coefficients; the quadratic twist χ_p⁻¹χ_p⁻² = χ_p³; the Goldmakher–Louvel quadratic large sieve; cube removal by Möbius inversion; and the transfer/recursion. The corollaries quoted in chapter 9 are from its introduction and from Corollary 1.2 of the 7/8 paper: Vinogradov's least-nonresidue conjecture, deterministic square roots, Miller's test, class numbers, and Euler's 65 idoneal numbers.
  * *Uniform exclusion of Landau–Siegel zeros*, Oct 1, 2026, 9 pages: (1 − β) log q ≥ c for an absolute c > 0.
* **Lean** (`lean/docs/003.md`, `lean/formalization.yaml`, `lean/ComparatorChallenges/`). Comparator challenges cover ζ, Dirichlet, and Hecke at 7/8, and the uniform real-zero gap. `QuasiRiemannHypothesis.json` permits only the axioms `propext`, `Quot.sound` and `Classical.choice`. The catalogue lists 162 manuscripts with formalized main results. `lean/OAI/NumberTheory/DirichletL` is 137,158 lines and contains no `sorry`. **This video did not compile the library.** "If it compiles as claimed" is said deliberately.
* **The 7/8 paper's structure** (its §1 "Proof overview"). Part I proves 11/12 by a "balanced first stage" with a zero detector. Part II "starts from that conclusion and introduces prime compensation, asymmetric scales, and two additional moment estimates." The paper names its contribution as "the construction of these compatible reflected and Poisson comparisons … with positive exponent margins chosen independently of the target character."
* **Coverage and reactions:**
  * J. Howlett, *OpenAI unleashes hundreds more math results upon a field already in shock*, Scientific American, Oct 6, 2026. Source for Andrew Sutherland's "We should ask for receipts" and for Tao's criticism of the pace: <https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/>
  * J. Kahn, *OpenAI publishes solutions to more than 370 outstanding math challenges*, Fortune, Oct 7, 2026. Source for Daniel Litt: "My view is that this is great for mathematics." <https://fortune.com/2026/10/07/openai-math-controversy-solutions-370-outstanding-challenges-published-criticisms-celebration/>
  * Latent Space / AINews, Oct 7, 2026. Quotes Levent Alpöge on X (Oct 6, 11:39 PM): "Big, big, big, big props for quasiriemann and no Siegel zeroes." <https://www.latent.space/p/ainews-quasi-riemann-hypothesis-openai>
  * XenoSpectrum, *OpenAI Publishes 722 AI-Generated Math Manuscripts…*, Oct 7, 2026: <https://xenospectrum.com/en/openai-math-manuscripts-verification/>
  * The release time ("about 6 p.m. Eastern") is from Scientific American and matches the repository's first commit.

### Classical mathematics

* Riemann, *Über die Anzahl der Primzahlen unter einer gegebenen Grösse* (1859). The quote "Es ist sehr wahrscheinlich, dass alle Wurzeln reell sind" refers to the roots of his ξ(t), which are real exactly when the zeros of ζ are on the critical line.
* PNT: Hadamard; de la Vallée Poussin (1896). Explicit formula: von Mangoldt (1895). Von Koch (1901): RH ⟺ π(x) = li(x) + O(√x ln x). Littlewood (1912): RH ⟺ M(x) = O(x^{½+ε}). Mertens conjecture disproved: Odlyzko & te Riele (1985). Hardy (1914): infinitely many zeros on the line. Conrey (1989): more than 2/5.
* Platt & Trudgian, *The Riemann hypothesis is true up to 3·10¹²*, Bull. LMS (2021). It covers 12,363,153,437,138 zeros up to height 3,000,175,332,800, all simple and on the line.
* 2026 "more than two thirds": arXiv:2608.13637 (argument credited to Anthropic's Claude, checked by L. Alpöge and R. Furman; Lean companion `anthropics/zeta-23-lean`), and an independent proof, arXiv:2609.02882. Both are unrefereed preprints.
* Zero-free region constant 1/5.558691 (|t| ≥ 2): Mossinghoff, Trudgian & Yang, arXiv:2212.06867. The video draws the region with this constant and does not claim it is the best known. A 2026 preprint by Bellotti, Trudgian & Yang reports 4.896 for t ≥ 3.
* Siegel (1935), ineffective lower bound for L(1, χ). Chebyshev's bias (1853 letter). The first x with π(x;4,1) > π(x;4,3) is 26,861 (Leech, 1957), recomputed here.
* Kummer (1846), cubic Gauss sums for p < 500: the 3 : 2 : 1 pattern, recomputed here as 24 : 14 : 7. Heath-Brown & Patterson (1979), equidistribution. Patterson (1978), the X^{5/6} conjecture. Dunn & Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture*, Annals of Math. 200 (2024), proved assuming GRH.
* Kubota (1969), Patterson (1977): the cubic theta function. Heath-Brown (1995): quadratic large sieve. Goldmakher & Louvel: its number-field version. Blomer, Goldmakher & Louvel: higher-order large sieve.
