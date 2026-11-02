# Part 4 · Martingales and Measure: expansion plan (24 → ~58 min)

Research-only plan; no repository file was edited. The chapters are planned under the lead's addendum (16–20 chapters, about 3 min each, as in *AI, Built*), which overrides the "4–6 min each" line in SYLLABUS §1. Each syllabus item still gets at least one full chapter, and the larger items get two. Target: **20 scenes = hook + 18 numbered chapters + outro, ≈ 58 min** (lecture_length floor 50). Narration runs at about 165 words/min in this series (Hook: 315 words = 1.9 min), so a 3.2-min chapter is about 530 words.

Labels used below: **[V]** checked this session against the URL given; **[K]** a standard citation known with confidence (classic paper or textbook); **(unverified)** not confirmed, and it must not go on screen as a fact until it is checked.

---

## 1. Current state (`python tools/lecture_length.py quant4`: 23.5 min)

| Scene | Min | What it covers | Depth |
|---|---|---|---|
| Hook | 1.9 | Sign-continuation e-process on the US market since 1926 (passes 20 in Feb 1929, reaches 10^101); started in 2000 it peaks at 6.7. Objectives, House | Real data. Finished plot, drawn with `Create` |
| 1 Information & cond. exp. | 1.8 | 3 tosses, partitions refining, E[#H\|F_n] bars; projection picture (2D plane); tower | Good visual. No definition of σ-algebra or measurability, no proof of the projection property |
| 2 Martingales & optional stopping | 2.5 | Definition, Ville/Doob card, examples, best-of-21 Doob martingale, OST statement, doubling with ∞ bankroll vs 1023 | OST is stated, not proved. No stopping-time chapter, no martingale transform |
| 3 Ruin & bold play | 2.3 | a/b by OST, de Moivre's (q/p)^X, roulette curves, Dubins–Savage, casino firm card | Derivation ladder. Computed |
| 4 Barings | 1.5 | Crisis card, Nikkei from FRED, Kobe | Facts only; the doubling is narrated, not shown |
| 5 Doob decomposition | 2.0 | Biased coin; US log wealth 9.06 = 7.28 + 1.78; M² compensator 2.893 vs QV 2.894 | Strong real-data result. Uniqueness is not derived |
| 6 Change of measure | 2.4 | P/Q/L table; equivalence; L paths: median 0.002 under P, 67% above 100 under Q | Good. No Radon–Nikodym theorem, density process, Bayes formula or Girsanov-on-a-coin |
| 7 Stable laws | 2.7 | Lévy family; McCulloch α = 1.40 (US), 1.27 (BTC); Mantegna–Stanley return-probability slope | Computed. No characteristic-function derivation, no fit shown learning |
| 8 Testing by betting | 2.4 | Ville's inequality card; peeking (t-test 50% vs e 3.2%); real-data verdicts | Ville is not proved on screen (the proof is in the README problem). Simulation shown as finished plots |
| 9 e-value monitor | 1.1 | `EProcess` code card, House rule 5 | Code shown but never run on screen |
| Outro | 2.9 | Recap, three desk questions, five problems, payoffs, references | — |

Missing altogether: σ-algebras and measurability, the martingale transform ("you can't beat the system"), stopping times as an object, a proof of optional stopping, the first-passage paradox, martingale convergence (upcrossings, Pólya, UI, Lévy upward), the Radon–Nikodym theorem, the density process and Bayes formula, Kakutani, Wald's identities, Azuma, the era/history segment, an industry chapter, a frontier chapter, and any fitted or trained object.

## 2. Audit

### (a) Syllabus items (SYLLABUS §6, Part 4)

| # | Item | Now | Verdict | Planned chapters |
|---|---|---|---|---|
| 1 | Probability spaces, filtrations as information | ch1, first half | thin (no σ-algebra, no measurability, no Kolmogorov) | 1 |
| 2 | Conditional expectation as projection; tower | ch1, second half | thin (picture only, no definition or properties) | 2 |
| 3 | Martingales: Ville, Doob | ch2, first half | thin | 3, 4 |
| 4 | Optional stopping and its hypotheses | ch2, second half | thin (statement only) | 5, 6 |
| 5 | Doubling, admissibility, Barings | ch2 end + ch4 | thin (doubling never simulated) | 7, 8 |
| 6 | Doob decomposition | ch5 | covered (uniqueness and ⟨M⟩ missing) | 11 |
| 7 | Change of measure, Radon–Nikodym, equivalence | ch6 | change of measure covered; RN theorem missing | 12, 13 |
| 8 | Stable laws | ch7 | covered, without a fit shown learning | 14 |
| 9 | Martingale convergence; gambler's ruin | ch3 (ruin only) | convergence **missing** | 9, 10 |
| 10 | Game-theoretic probability, e-values, anytime-valid | ch8–9 | covered; no learned bettor, no confidence sequence | 15, 16, 18 |
| — | Industry chapter | firm card only | **missing** | 17 |
| — | Frontier chapter | one card | **missing** | 18 |

### (b) Textbook core sections → chapter

Section numbers are from memory of the editions named and are marked (≈) where a number is uncertain. Check them against the books' tables of contents before the README audit table is published.

**Williams, *Probability with Martingales* (1991)**

| Section | Where |
|---|---|
| Ch 0 Branching-process example (Z_n/μ^n is a martingale) | Ch10, as one example of a convergent martingale (20 s) |
| Ch 1–3 Measure spaces, events, random variables; Borel–Cantelli | Ch1 (σ-algebra = answerable questions; coin space ≅ [0,1]); Borel–Cantelli → README only |
| Ch 4 Independence (monkey typing Shakespeare, ≈4.9) | Ch1 (independence); monkey → Ch6 ABRACADABRA |
| Ch 5–6 Integration, expectation; MON, DOM, Fatou | Ch6 (definition card: DCT used in the OST proof) |
| Ch 7–8 Strong law (easy version), product measure | Ch13 (the SLLN drives L_n → 0; product measure for Kakutani) |
| Ch 9 Conditional expectation: Kolmogorov's definition, least-squares predictor (≈9.4), properties (≈9.7) | Ch2 |
| Ch 10 Filtrations, martingales, previsible processes, "you can't beat the system" (≈10.6–10.7), stopping times, stopped supermartingales, OST (≈10.9–10.10), "awaiting the almost inevitable" (≈10.11), hitting times of SRW (≈10.12), exercise ABRACADABRA | Ch3, 4, 5, 6 |
| Ch 11 Upcrossing lemma, Doob's forward convergence theorem | Ch10 |
| Ch 12 L²-bounded martingales, orthogonal increments, Doob decomposition, ⟨M⟩ (≈12.11–12.12), Lévy's Borel–Cantelli | Ch11 (Doob, ⟨M⟩); three-series theorem → README (not core here) |
| Ch 13 Uniform integrability | Ch6 (why OST fails), Ch10 |
| Ch 14 UI martingales, Lévy upward/downward, Doob's submartingale and L^p inequalities, Kakutani's product theorem (≈14.12), Radon–Nikodym by martingales (≈14.13), likelihood ratios and equivalent measures (≈14.15–14.17) | Ch10 (Lévy upward), Ch15 (maximal inequality = Ville), Ch13 (RN, Kakutani), Ch12 (likelihood ratio) |
| Ch 15 Applications: martingale representation, discrete Black–Scholes, Mabinogion sheep, filtering | Part 9 (pricing), Part 5 (representation), Part 7 (filtering); README pointer |
| Ch 16–18 Characteristic functions, weak convergence, CLT | Ch14 (characteristic functions and the generalized CLT); Donsker → Part 5 |

**Shreve I, *The Binomial Asset Pricing Model* (2004)**

| Section | Where |
|---|---|
| 2.1–2.2 Finite probability spaces, random variables, distributions | Ch1 |
| 2.3 Conditional expectations | Ch2 |
| 2.4 Martingales | Ch3 |
| 2.5 Markov processes | Ch3 (card: Markov ≠ martingale); full treatment in Part 5 |
| 3.1 Change of measure | Ch12 |
| 3.2 Radon–Nikodým derivative process (density process, conditional Bayes) | Ch12 |
| 3.3 Capital asset pricing (utility maximization with state prices) | Parts 8, 9, 23 |
| 4 American derivative securities | Parts 8, 10 |
| 5.2 First passage times (generating function E[α^τ] from the exponential martingale) | Ch5 |
| 5.3 Reflection principle | Ch5 |
| 5.4 Perpetual American put | Parts 8, 10 |

**Shreve II, ch 1–2** (READING §2 maps them to Part 4): 1.1–1.3 infinite probability spaces and Lebesgue measure on [0,1] via coin tosses → Ch1; 1.4 convergence of integrals (MCT, DCT) → Ch6 card; 1.6 change of measure (Z, E_Q[X] = E_P[XZ]) → Ch12; 2.2 information and σ-algebras → Ch1; 2.3 independence → Ch1; 2.4 general conditional expectations → Ch2.

**Föllmer–Schied, 4th ed. (2016)** (≈ for section titles): 1.1–1.2 arbitrage and martingale measures (the one-period FTAP) → previewed in Ch12–13, proved in Part 9; 1.3–1.6 derivatives, completeness, geometry → Part 9; ch 4 monetary risk measures → Part 40; ch 5 dynamic arbitrage theory, the multi-period FTAP (Dalang–Morton–Willinger) → Part 9; ch 6 American claims, Snell envelope (with the Doob decomposition of the Snell envelope) → Part 8, and Ch11 points to it; App. A.2 absolutely continuous measures, densities, equivalence → Ch13. **Recommendation:** change the Part 4 textbook line from "Föllmer–Schied ch. 1" to "Föllmer–Schied §1.2 (preview) and App. A.2"; ch 1 belongs to Part 9.

### (c) READING.md paper list for Part 4

| Paper | Now | Plan |
|---|---|---|
| Kolmogorov (1933) *Grundbegriffe* | absent | on screen, Ch1 history card (axioms; the definition of conditional expectation) |
| Ville (1939) | on screen (ch2, ch8) | Ch3, Ch15 |
| Doob (1953) *Stochastic Processes* | on screen | Ch3, Ch11 |
| Fama (1965) | on screen | Ch14 |
| Mantegna–Stanley (1995) *Nature* | on screen | Ch14 |
| Shafer–Vovk (2001; 2019) | on screen (card) | Ch15 (the game: Skeptic, Forecaster, Reality) |
| Ramdas–Grünwald–Vovk–Shafer (2023) *Stat. Sci.* 38(4):576–601 [V] | on screen (card) | Ch15, Ch18 |
| Board of Banking Supervision (1995) Barings report | references only | on screen, Ch8 crisis card source line |

Papers to add to READING.md (all [V] unless marked [K]): Li (1980) *Ann. Probab.* 8(6):1171–1176; Dubins–Savage (1965) [K]; Wald (1945) "Sequential tests of statistical hypotheses," *Ann. Math. Stat.* [K]; Kakutani (1948) "On equivalence of infinite product measures," *Ann. Math.* [K]; Nikodym (1930) *Fund. Math.* 15 [K]; Esscher (1932) [K]; Gerber–Shiu (1994) *TSA* 46:99–191; Harrison–Pliska (1981) [K]; Dybvig–Huang (1988) *RFS* 1(4):377–401; Koutrouvelis (1980) *JASA* [K]; McCulloch (1986) [K]; Azuma (1967) *Tohoku Math. J.* [K]; Augenblick–Rabin (2021) *QJE* 136(2):933–985; the Part 4 frontier list (Ch18); the industry sources (Ch17).

---

## 3. The proposed chapter list (manifest order)

| Scene module | Chapter title | Items | Min | Status |
|---|---|---|---|---|
| s01_hook | Can you beat a fair game? | era | 3.0 | deepened |
| s02_information | 1. Information: σ-algebras and filtrations | 1 | 2.8 | deepened |
| s03_projection | 2. Conditional expectation is a projection | 2 | 3.2 | new (split out of old ch1) |
| s04_martingales | 3. Martingales: Ville's fair games | 3 | 2.8 | deepened |
| s05_system | 4. You can't beat the system | 3 | 2.8 | new |
| s06_stopping | 5. Stopping times, and the walk that always wins | 4 | 3.0 | new |
| s07_optional | 6. Optional stopping, proved | 4 | 3.2 | new |
| s08_doubling | 7. Doubling and admissible strategies | 5 | 2.6 | new |
| s09_barings | 8. Doubling down: Barings, 1995 | 5 | 2.4 | deepened |
| s10_ruin | 9. Gambler's ruin and bold play | 9 | 2.6 | kept, plus duration |
| s11_convergence | 10. Martingales converge | 9 | 3.2 | new |
| s12_doob | 11. Doob's decomposition | 6 | 3.2 | deepened |
| s13_measure | 12. Change of measure | 7 | 3.2 | deepened |
| s14_radon | 13. Radon–Nikodym, and the singular infinite | 7 | 3.2 | new |
| s15_stable | 14. Heavy tails as stable laws | 8 | 3.0 | deepened |
| s16_betting | 15. Ville's inequality and testing by betting | 10 | 3.0 | deepened |
| s17_learner | 16. Learning to bet | 10 | 3.2 | new (absorbs old ch9 House) |
| s18_industry | 17. The house, the book and the market | industry | 4.0 | new |
| s19_frontier | 18. Frontier: anytime-valid inference, 2023–2026 | 10 | 3.0 | new |
| s20_outro | Recap, desk questions, problems, the House | — | 2.8 | deepened |
| | **Total** | | **≈ 58.2** | |

Caches are keyed by module name (CLAUDE.md), so renumbering re-renders everything. That is acceptable here because every kept chapter's narration changes anyway. The `compute.py` items keep their names (`doob`, `measure`, `ruin`, `stable`, `nikkei`, `peeking`, `eprocess`, `envelope`), so the cached numbers survive.

**Hands-on summary.** Every chapter has an on-screen simulation (c). The fitted or trained objects (a) are the stable-law MLE replay (Ch14), the online bettor replay (Ch16) and the Bayesian drift learner (Ch10). The six labs (b) are `cond_exp` (Ch2), `martingale_transform` (Ch4), `pattern_wait` (Ch6), `esscher_tilt` (Ch12), `ONSBettor` (Ch16) and `e_bh` (Ch18). The compute budget (d) is in §6.

---

## 4. Chapter specifications

Each chapter follows the order in SYLLABUS §1: question → card → derivation (`ladder` + `why`) → experiment → predict → takeaway. "Live" means that a `ValueTracker` drives the simulation on screen, with paths growing step by step (`tracing`/`always_redraw`) rather than `Create` on a finished curve.

### Hook · Can you beat a fair game? (3.0, deepened)
- **Goal:** pose the question, show the era, and give the plan.
- **Beats:** (1) The current betting cold open, now live: a date counter ticks from 1926 and the wealth line grows with it; the "20" line lights up when it is crossed in Feb 1929; the run started in 2000 is drawn in parallel and never crosses. (2) *How we got here* (≈70 s), with the timeline strip lit in turn: 1654 Pascal–Fermat; 1713/1718 de Moivre's ruin; 1900 Bachelier; 1933 Kolmogorov; 1939 Ville; 1945 Wald; 1953 Doob; 1965 Samuelson and Dubins–Savage; 1979–81 Harrison–Kreps–Pliska; 1995 Barings; 2001 Shafer–Vovk; 2023 the anytime-valid survey. (3) Objectives card (18 lines in 6 groups). (4) House chart.
- **Signature visual: the problem of points.** Use `binomial_tree` for a first-to-3 game with the score at A 2, B 1 and 64 pistoles staked. The leaves light up 64/0, values flow back, and the root shows 48/16. A second tree from 2–0 gives 56/8. Pascal's letter of 29 July 1654 [V: https://www.york.ac.uk/depts/maths/histstat/pascal.htm]. The caption: "the value of an interrupted fair game = its conditional expectation; the sequence of values is a martingale (Ch3)".
- **Predict:** "Score 2–0 in a first-to-3 game. What share is fair?" (56 of 64).

### 1 · Information: σ-algebras and filtrations (2.8)
- **Goal:** a σ-algebra is the set of yes/no questions you can answer; a filtration is that set growing; a variable is measurable when it is constant on the blocks you cannot tell apart.
- **Beats:** the eight-world strip (kept); a "question deck" beside it: F_n holds 2, 4, 16, 256 events (2^(2^n)), each one a union of blocks. Test two variables for F_1-measurability: X = first toss passes (its bars are constant on the blocks); #heads fails (red cross). Adapted process. Independence: learning the first toss leaves the block averages of the second toss unchanged. Infinite tosses: Kolmogorov's 1933 axioms card (Ω, F, P; countable additivity), and the coin space is the unit interval.
- **Derivation:** $\mathcal F_n=\sigma(\text{first }n\text{ tosses})=\{\text{unions of the }2^n\text{ blocks}\}$ (generated by a partition); $|\mathcal F_n|=2^{2^n}$ (each block in or out); $X\ \mathcal G\text{-measurable}\iff X$ constant on each atom (finite case); $\omega=(\omega_1,\omega_2,\dots)\mapsto\sum_k\omega_k2^{-k}$ carries the fair-coin measure to Lebesgue measure (Shreve II §1.2).
- **Signature visual (the coin-space zoom):** the unit interval [0,1] as a long bar. Each toss halves the block that contains the hidden "true world" (a gold dot), and the dyadic grid lines appear as information arrives. The camera zooms in (`frame_to`) on the shrinking block for six tosses, then pulls back to show 64 slivers. The picture *is* F_n: what you know is which sliver you are in. Ch13 reuses this grid for Radon–Nikodym.
- **Experiment:** none needed; the chapter is short and conceptual. The question deck counts are exact.
- **Predict:** "Is 'the number of heads in the first two tosses is even' an F_1 event?" (No: it depends on toss 2.)

### 2 · Conditional expectation is a projection (3.2, new)
- **Goal:** Kolmogorov's definition by partial averages, the L² projection, and the properties, each with a one-line proof.
- **Beats:** the motivating question ("the best forecast of tomorrow's return, given today's?"); definition card; 3D projection; tower; properties; data; lab.
- **Derivation:**
  1. $Y=\mathbb E[X\mid\mathcal G]$ iff $Y$ is $\mathcal G$-measurable and $\mathbb E[X\mathbf 1_A]=\mathbb E[Y\mathbf 1_A]\ \forall A\in\mathcal G$ (Kolmogorov's definition).
  2. On a partition: $Y=\sum_j \frac{\mathbb E[X\mathbf 1_{B_j}]}{P(B_j)}\mathbf 1_{B_j}$ (take $A=B_j$).
  3. $\mathbb E[(X-Y)Z]=0$ for every $\mathcal G$-measurable $Z\in L^2$ (approximate $Z$ by indicator sums; linearity).
  4. $\mathbb E[(X-Z)^2]=\mathbb E[(X-Y)^2]+\mathbb E[(Y-Z)^2]$ (expand; the cross term vanishes by 3), so $Y$ minimizes the mean squared error (Pythagoras).
  5. Taking out what is known: $\mathbb E[ZX\mid\mathcal G]=Z\,\mathbb E[X\mid\mathcal G]$ (check the definition with $Z\mathbf 1_A$).
  6. Tower: $\mathcal H\subset\mathcal G\Rightarrow\mathbb E[\mathbb E[X\mid\mathcal G]\mid\mathcal H]=\mathbb E[X\mid\mathcal H]$ (both satisfy the definition on $A\in\mathcal H\subset\mathcal G$).
  7. Independence: $\sigma(X)\perp\mathcal G\Rightarrow\mathbb E[X\mid\mathcal G]=\mathbb E X$; Jensen: $\varphi(\mathbb E[X\mid\mathcal G])\le\mathbb E[\varphi(X)\mid\mathcal G]$ (supporting lines).
- **Signature visual (`ThreeDScene`, replacing the 2D sketch):** Ω = {a, b, c} with P = (0.5, 0.3, 0.2). A random variable is an arrow in ℝ³, drawn in the coordinates √p_i·x_i so that the picture's Euclidean geometry is the L²(P) geometry. G = σ({a,b},{c}) is a translucent plane, the span of (√.5, √.3, 0) and (0, 0, √.2). X drops a perpendicular onto the plane, and a right-angle marker appears. The camera orbits 120° so the viewer sees the right angle from the side. Then H = trivial σ-algebra, a line along (√.5, √.3, √.2): the projected point slides down onto it, and so does X's direct projection, landing on the same point (tower). Numbers on screen: X = (3, 0, 1) → E[X\|G] = (1.875, 1.875, 1) → E X = 1.7 (both projections average to 1.7: tower).
- **Experiment (real data):** `condexp`. Ken French daily market 1926–2020 (`data.ken_french_daily`). E[r_{t+1} \| sign r_t] by era, with 200 block-bootstrap seeds drawn as bands. Expected (probe this session): 1926–74 ρ₁ = 0.104, E[r\|up] = +13.5 bp, E[r\|down] = −9.4 bp; 1975–99 ρ₁ = 0.126 (+16.0 / −5.0 bp); 2000–20 ρ₁ = −0.096 (−0.3 / +7.9 bp). The projection has turned around in sign, which ties back to the Hook.
- **Lab 1:** the House's `cond_exp(x, labels, p)`:
  ```python
  def cond_exp(x, labels, p=None):
      """E[X | G], G generated by the partition `labels`: the average on each block."""
      x = np.asarray(x, float); p = np.ones_like(x) if p is None else np.asarray(p, float)
      out = np.empty_like(x)
      for b in np.unique(labels):
          m = labels == b
          out[m] = (p[m] * x[m]).sum() / p[m].sum()
      return out
  ```
  Run it first on the 3-point space (output 1.875, 1.875, 1 appears), then on the market with labels = sign of yesterday (the bars from the experiment).
- **Predict:** "In 2000–2020, after a down day, what is the best forecast of today's return: up, down or zero?" (Up, +7.9 bp.)

### 3 · Martingales: Ville's fair games (2.8)
- **Goal:** the definition; sub- and supermartingales; the main examples, proved; convex functions of martingales.
- **Beats:** definition card + Ville history card (kept); examples proved on a ladder; best-of-21 Doob martingale, now live; Jensen → a call on a martingale is worth more the longer it runs; Markov ≠ martingale card.
- **Derivation:** $S_n^2-n$: $\mathbb E[S_{n+1}^2\mid\mathcal F_n]=S_n^2+2S_n\mathbb E\xi+\mathbb E\xi^2=S_n^2+1$ (expand, independence). Exponential martingale: $Z_n=e^{\theta S_n}/(\cosh\theta)^n$, since $\mathbb E e^{\theta\xi}=\cosh\theta$ (mgf of ±1). Doob: $M_n=\mathbb E[X\mid\mathcal F_n]$, $\mathbb E[M_{n+1}\mid\mathcal F_n]=M_n$ (tower). Jensen: $\varphi$ convex ⇒ $\varphi(M)$ is a submartingale; with $\varphi(x)=(x-K)^+$, $\mathbb E(M_T-K)^+$ is non-decreasing in $T$ (the forward is a martingale under Q → calendar spreads ≥ 0, Part 12).
- **Signature visual (the fan of tomorrows):** live best-of-21 paths. At the current point of the highlighted path, a small vertical "next-step fan" shows the two possible next values with their probabilities as dot sizes, and a balance tick marks their mean exactly at the current value. As the ValueTracker advances, the fan moves along with the path. The fan is the definition (tomorrow's mean = today), shown at every point.
- **Experiment:** `martingales`, a small simulation: the call value E(S_n − 2)^+ on the walk for n = 1…50 rises monotonically; drawn live.
- **Predict:** "Is \|S_n\| a martingale?" (No: a submartingale; its mean grows like √(2n/π).)

### 4 · You can't beat the system (2.8, new)
- **Goal:** any predictable stake on a fair game is a fair game: the martingale transform.
- **Derivation:** $(H\cdot M)_n=\sum_{k\le n}H_k\Delta M_k$, $H_k\in\mathcal F_{k-1}$, bounded (stake decided before the toss); $\mathbb E[(H\cdot M)_{n+1}-(H\cdot M)_n\mid\mathcal F_n]=H_{n+1}\mathbb E[\Delta M_{n+1}\mid\mathcal F_n]=0$ (taking out what is known; martingale). On roulette, red at even money: $\mathbb E[\Delta\mid\mathcal F]=-\tfrac1{37}$ per unit, so $\mathbb E[\text{gain}]=-\tfrac1{37}\mathbb E[\sum H_k]$: **every system pays the same tax per unit staked.** A cheater with $H_k\in\mathcal F_k$ (stake after peeking) can set $H_k=\operatorname{sign}\Delta M_k$ and win surely; that is why predictability is the whole hypothesis (Williams ≈10.6–10.7).
- **Signature visual (the curtain desk):** a row of 12 face-down tosses behind a grey curtain. The stake bar for toss k is drawn first, then the curtain lifts one card and the wealth line steps. Then six small multiples run live side by side: flat, martingale (doubling), d'Alembert, Labouchère, Fibonacci, Oscar's grind. Each has its wealth path, a "total staked" counter and a "loss ÷ staked" readout that settles to −0.0270 on all six.
- **Experiment:** `systems`. 20,000 sessions × 6 systems × {fair coin, European roulette}, each session to 200 spins or a stop rule. Expected: on the fair coin the mean P&L is within 2 s.e. of 0 for all six; on roulette, mean P&L ÷ mean total staked = −0.0270 ± sampling error for all six. The distributions differ: doubling is very left-skewed, Paroli right-skewed. Shown as `side_density` histograms with the mean marked.
- **Lab 2:** `martingale_transform` plus one stake rule, run on the curtain desk:
  ```python
  def martingale_transform(H, dM):
      """(H . M)_n: stake H_k, fixed before step k, times the fair increment dM_k."""
      return np.concatenate([[0.0], np.cumsum(np.asarray(H) * np.asarray(dM))])

  def doubling_stakes(dM, base=1.0):
      H, h = [], base
      for d in dM:                # h is decided before d is seen
          H.append(h); h = base if d > 0 else 2 * h
      return np.array(H)
  ```
- **Predict:** "Labouchère or flat betting: which loses more per unit staked on roulette?" (Neither: 2.70% each.)

### 5 · Stopping times, and the walk that always wins (3.0, new)
- **Goal:** a stopping time decides using only the past. The first passage of a fair walk to +1 happens with probability 1, yet its expected time is infinite.
- **Beats:** definition; allowed and forbidden rules; stopped process; the paradox; first-passage law and its generating function (Shreve I §5.2–5.3); Wald's identities.
- **Derivation:**
  1. $\tau$ is a stopping time iff $\{\tau\le n\}\in\mathcal F_n\ \forall n$ (decide with what you know).
  2. $M^\tau_n=M_{\tau\wedge n}=M_0+\sum_{k\le n}\mathbf 1_{\{k\le\tau\}}\Delta M_k$ and $\{k\le\tau\}=\{\tau\le k-1\}^c\in\mathcal F_{k-1}$, so $M^\tau$ is a martingale transform, hence a martingale (Ch4).
  3. Reflection: $P(\tau_1>n)=P(\max_{k\le n}S_k\le0)=P(S_n\in\{0,1\})\sim\sqrt{2/(\pi n)}$ (reflect paths after their first visit to +1; Stirling).
  4. $\mathbb E\tau_1=\sum_n P(\tau_1>n)=\infty$ (harmonic-type divergence).
  5. Wald: if $\mathbb E\tau<\infty$, $\mathbb E S_\tau=\mu\,\mathbb E\tau$. Here $S_{\tau_1}=1$ and $\mu=0$ would give $1=0$, so $\mathbb E\tau_1=\infty$ (a one-line proof by contradiction).
  6. Generating function: $Z_n=e^{\sigma S_n}(\cosh\sigma)^{-n}$ stopped at $\tau_1$ is bounded for $\sigma>0$ (OST) ⇒ $\mathbb E[\alpha^{\tau_1}]=\frac{1-\sqrt{1-\alpha^2}}{\alpha}$ with $\alpha=1/\cosh\sigma$ (Shreve I Thm 5.2.3); its derivative at α = 1 is +∞, which agrees with step 4.
- **Signature visual (the bell and the curtain):** one walk runs toward a curtain on the right. Rule A, "ring when you first reach +1", rings the moment it happens. Rule B, "ring at the walk's highest point in 100 steps", tries to ring, and the curtain is pulled back to show that the decision needed the future (ghost path in grey); a red stamp reads "not a stopping time". Then 400 walks run live on shared axes, each freezing with a gold dot at τ₁; a counter "hit +1: 92.0% … 97.5% … 99.2%" rises. A log-log panel of P(τ > n) traces out slope −½ against the exact curve, and a running average of the τ's drawn so far keeps jumping upward and never settles.
- **Experiment:** `firstpassage`. 10,000 walks to n = 10⁵ (chunked int8; ≈5 min). Expected: P(τ>100) = 0.0796 (exact C(100,50)/2¹⁰⁰); P(τ>10⁴) ≈ 0.0080; sample mean of τ ∧ 10⁵ grows like √n; the max drawdown before hitting +1 has median ≈ 1 and a 99th percentile in the hundreds (to be computed).
- **Predict:** "After 100 fair steps, what fraction of walks has not yet been up 1?" (≈8%.)

### 6 · Optional stopping, proved (3.2, new)
- **Goal:** the theorem with its proof; why each hypothesis matters; pattern waiting times as an application.
- **Derivation:**
  1. $\mathbb E M_{\tau\wedge n}=M_0$ for every $n$ (Ch5: stopped martingale).
  2. $M_{\tau\wedge n}\to M_\tau$ a.s. when $\tau<\infty$ a.s.
  3. (a) $\tau\le N$: take $n=N$. (b) $|M_{\tau\wedge n}|\le K$: dominated convergence. (c) $\mathbb E\tau<\infty$, $|\Delta M|\le c$: $|M_{\tau\wedge n}|\le|M_0|+c\tau\in L^1$, dominated convergence. The general condition is uniform integrability of $\{M_{\tau\wedge n}\}$ (Williams ch 13–14).
  4. Counterexample, from Ch5: $\mathbb E S_{\tau_1\wedge n}=0$ for all $n$, but $S_{\tau_1}=1$: the mass escapes (not UI).
  5. Pattern waiting time (Li 1980): before each toss a new gambler stakes $1 on the pattern at fair odds. The casino's net is a martingale with bounded increments and $\mathbb E\tau<\infty$, so $\mathbb E\tau=\sum_{k:\,\text{prefix}_k=\text{suffix}_k}m^k$: HH = 2+4 = 6, HT = 4, HTH = 2+8 = 10, HHH = 14; ABRACADABRA: $26^{11}+26^4+26\approx3.67\times10^{15}$.
- **Signature visual (the leaking balance):** the histogram of $S_{\tau_1\wedge n}$ for n = 10, 100, 1,000, 10,000 (live, morphing). Almost all the mass piles into a gold spike at +1, while a thin red tail slides off to the left edge of the frame. A fulcrum under the histogram stays balanced at 0 throughout (mean 0). At n = ∞ the tail has left the frame and the scale tips: the mean jumps to 1. The jump is uniform integrability failing. Second visual: the gamblers' queue for HH, coloured chips for each gambler, the payouts of 4 and 2 lighting when HH lands.
- **Experiment:** `patterns`. 200,000 simulated sequences each for HH, HT, HTH, HHH and Penney pairs. Expected: sample means 6.00, 4.00, 10.0, 14.0 (±0.02–0.05); Penney: P(THH before HHT) = 0.75 (exact 3/4, by Conway's leading-number odds, computed with the same function).
- **Lab 3:** the House's `pattern_wait` (Conway's leading number, Li 1980):
  ```python
  def pattern_wait(pat, m=2):
      """Expected i.i.d. draws (m equally likely symbols) until `pat` first appears."""
      return sum(m ** k for k in range(1, len(pat) + 1) if pat[:k] == pat[-k:])
  ```
  Run it live: `pattern_wait("HH") → 6`, `"HT" → 4`, `"ABRACADABRA", 26 → 3670344487444778`.
- **Predict:** "HH or HT: which takes longer to appear?" (HH: 6 against 4, though each has probability ¼ per pair.)

### 7 · Doubling and admissible strategies (2.6, new)
- **Goal:** doubling escapes optional stopping only through unbounded credit; finance outlaws it with admissibility.
- **Derivation:** with bankroll $2^k-1$: $\mathbb E=(1-2^{-k})\cdot1-2^{-k}(2^k-1)=0$ (bounded steps, OST holds). Sessions until first ruin ~ Geometric($2^{-k}$), mean $2^k$. Admissible: wealth $V_t\ge -c$ for all $t$; then $V$ is a supermartingale under Q (a local martingale bounded below), so $\mathbb E_Q V_T\le V_0$: no free lunch (Harrison–Pliska 1981; Dybvig–Huang 1988, *RFS* 1(4):377–401 [V: https://ideas.repec.org/a/oup/rfinst/v1y1988i4p377-401.html]). Proof in Part 9; here, the discrete intuition. Short options are the same shape of payoff: many small premiums and a rare large loss (Part 11).
- **Signature visual (the staircase and the cliff):** 1,000 doublers with bankroll 1,023 run live on one axis. Gold staircases climb by +1 a session; at random moments one turns into a red vertical cliff to −1,023 (a sound tick on each). Readouts: "mean wealth: 0.0 ± s.e." stays flat, while "median wealth" climbs steadily. A final histogram shows a big spike on the right and a tiny far-left mass with equal moments.
- **Experiment:** `doubling` (House `martingale.doubling`). 1,000 doublers × 3,000 sessions, seeded. Expected: about 95% ruined at least once by session 3,000 (1 − (1023/1024)^3000 ≈ 0.946); mean P&L within s.e. of 0.
- **Predict:** "With bankroll 1,023, how many sessions on average until the first ruin?" (1,024.)

### 8 · Doubling down: Barings, 1995 (2.4, deepened)
- **Goal:** the crisis file. The hidden account supplied the unbounded credit that Ch7 showed doubling needs.
- **Beats:** crisis card (kept: about £830m, account 88888, ING for £1, founded 1762). Board of Banking Supervision, report of 18 July 1995 (date per secondary sources; FIA retrospective [V: https://www.fia.org/marketvoice/articles/25-years-ago-barings-offers-hard-lesson-risk-controls] gives $1.3bn and the collapse on 26 Feb 1995). FRED Nikkei with Kobe (kept). **New:** a schematic replay of a "double the long position after every down day" rule on the real Nikkei daily closes, Jul 1994 – Feb 1995, with position size and cumulative P&L drawn live under the index, and a "capital" line that is crossed in February. It is labelled `schematic: a doubling rule on the real index, not Leeson's book`. Last beat: segregation of front and back office as the control that enforces the bounded-bankroll hypothesis.
- **Unverified (keep off screen until checked against the BoBS report):** the size of Leeson's futures position, the strike range of the short straddles, the "£827m" exact figure.
- **Experiment:** `nikkei` (kept) + `nikkei_doubling` (seconds). Expected: the schematic rule's position grows through January; P&L crosses a stated capital line in late Feb. Report the date it is crossed, computed.
- **Predict:** "If the doubling rule had been capped at 4 doublings, would the loss have been bounded?" (Yes, at 15 units per cycle; computed.)

### 9 · Gambler's ruin and bold play (2.6, kept + duration)
- Keep the ladder (a/b, de Moivre), the roulette curves and Dubins–Savage. Move the casino card to Ch17.
- **Add:** expected duration from the $S_n^2-n$ martingale: shift the start to 0 with barriers $-a$ and $b-a$; $\mathbb E S_\tau^2=\mathbb E\tau$ (OST, bounded steps, $\mathbb E\tau<\infty$), so $\mathbb E\tau=(b-a)^2\tfrac ab+a^2\tfrac{b-a}b=a(b-a)$. Worked: a = 50, b = 100 → 2,500 bets.
- **Live:** 200 ruin games from 50 run on screen, each freezing at 0 (red) or 100 (gold); counters converge to 50%, then the same with p = 18/37 → 6.3% (existing `ruin` numbers).
- **Experiment:** `ruin` (kept) + durations (4,000 games). Expected: mean duration 2,500 ± ~30 on the fair coin.
- **Predict:** "Starting at 50 of 100 on a fair coin, how many bets on average?" (2,500.)

### 10 · Martingales converge (3.2, new; syllabus item 9)
- **Goal:** Doob's forward convergence theorem through upcrossings (a trading strategy), Pólya's urn, Lévy's upward theorem as learning, and uniform integrability.
- **Derivation:**
  1. Upcrossing strategy: buy 1 unit when M < a, sell when M > b, repeat; $H$ is predictable.
  2. $(H\cdot M)_n\ge(b-a)U_n[a,b]-(M_n-a)^-$ (each completed upcrossing earns at least $b-a$; the last open trade loses at most $(M_n-a)^-$).
  3. Supermartingale ⇒ $\mathbb E(H\cdot M)_n\le0$ (Ch4) ⇒ $(b-a)\mathbb E U_n\le\mathbb E(M_n-a)^-$ (Doob's upcrossing lemma).
  4. $\sup_n\mathbb E|M_n|<\infty$ ⇒ $U_\infty[a,b]<\infty$ a.s. for all rational $a<b$ ⇒ $M_n$ converges a.s. (no oscillation).
  5. Pólya: $R_n/(n+2)$ is a martingale ($\mathbb E[R_{n+1}\mid\mathcal F_n]=R_n+\frac{R_n}{n+2}$; divide); bounded ⇒ converges; limit Uniform(0,1) for one red and one blue ball.
  6. Lévy upward: $\mathbb E[X\mid\mathcal F_n]\to\mathbb E[X\mid\mathcal F_\infty]$ a.s. and in $L^1$ (UI by the tower and Jensen).
  7. Not every limit keeps the mean: $L_n\to0$ while $\mathbb E L_n=1$ (Ch12). UI ⇔ $L^1$ convergence ⇔ $M_n=\mathbb E[M_\infty\mid\mathcal F_n]$.
- **Signature visual (the upcrossing trader):** one path with a horizontal band [a, b]. Every upcrossing is highlighted in gold with a "bought at a / sold at b" marker pair, and an "upcrossings: 3" counter ticks. The trader's P&L line runs underneath. Then 100 Pólya urns run live (fraction of red against draws): early jitter, then flattening, each settling to its own level; on the right axis the limits drop into a histogram that fills out flat (uniform).
- **Hands-on (a), a learner shown learning:** `drift_posterior`. A Bayesian estimate of the market's daily mean (normal prior, known σ from EWMA), updated day by day on Ken French 1926–2020. Its posterior mean is a Doob martingale under the model, and its 95% band narrows like 1/√t, scrubbed with a ValueTracker against the date. Expected: after 94 years the arithmetic annualized mean ≈ 10.6% (0.042%/day × 252), 95% band ≈ ±3.7% (2 × 18%/√94). The drift is learnable only over decades (Merton 1980, *JFE* 8 [K]), and this links to Ch11.
- **Experiment:** `polya` (10,000 urns × 2,000 draws, seconds) + `upcrossings` (fair walk stopped in [−30, 30], checking Doob's bound). Expected: K–S distance of the urn limits from Uniform(0,1) < 0.02; mean upcrossings below the bound.
- **Predict:** "Pólya urn from one red and one blue: chance the red fraction ends above 90%?" (10%.)

### 11 · Doob's decomposition (3.2, deepened)
- **Goal:** uniqueness of drift + martingale; the predictable part depends on the filtration (Ivey); ⟨M⟩.
- **Derivation:**
  1. $A_n=\sum_{k\le n}\mathbb E[\Delta X_k\mid\mathcal F_{k-1}]$, $M=X-X_0-A$; $\mathbb E[\Delta M_k\mid\mathcal F_{k-1}]=0$ (by construction).
  2. Uniqueness: if $A-A'=M'-M$ is predictable and a martingale, then $\Delta=\mathbb E[\Delta\mid\mathcal F_{k-1}]=0$ (a predictable martingale is constant).
  3. $M^2=\langle M\rangle+N$, with $\langle M\rangle_n=\sum\mathbb E[(\Delta M_k)^2\mid\mathcal F_{k-1}]$ (apply 1 to $M^2$; $\mathbb E[\Delta(M^2)\mid\mathcal F]=\mathbb E[(\Delta M)^2\mid\mathcal F]$).
  4. Change the filtration and $A$ changes: $\mathcal G_n\supset\mathcal F_n$ ⇒ $A^{\mathcal G}\neq A^{\mathcal F}$ in general (the same path, a different forecast).
- **Signature visual (one P&L, two drifts):** a single simulated punto-banco P&L path. Under the casino's filtration its predictable part is a line sloping down at −1.24% per unit staked; under an edge-sorter's filtration the same path's predictable part is a line sloping up at +6.5%. The two martingale remainders are drawn underneath in different colours. Numbers are from the court record: the house edge was 1.24% (player) / 1.06% (banker); perfect edge sorting gave the player a long-term edge of about 6.5%. *Ivey v Genting Casinos* [2017] UKSC 67, which held it was cheating; £7.7m won at Crockfords, Aug 2012 [V: press summary https://www.supremecourt.uk/cases/docs/uksc-2016-0213-press-summary.pdf; High Court [2014] EWHC 3394 (QB) https://caselaw.nationalarchives.gov.uk/ewhc/qb/2014/3394]. The path is labelled `simulated, with the court's edge figures`. Then the kept market split (9.06 = 7.28 + 1.78) and the compensator (2.893 vs 2.894), both now drawn with a date tracker.
- **Experiment:** `doob` (kept) + `ivey_sim` (seconds: 10,000 hands, per-hand ±1 with a signal-dependent mean calibrated to give the two drifts).
- **Lab (repeat of an existing House function, not counted among the six):** `doob_decomposition` shown (7 lines) and run on the 55% coin.
- **Predict:** "Is the drift a property of the price, or of what you know?" (Of what you know.)

### 12 · Change of measure (3.2, deepened)
- **Goal:** Q reweights worlds without moving them; the density process; Bayes' rule; the drift changes (discrete Girsanov); the Esscher transform on real returns.
- **Derivation:**
  1. $L=\frac{dQ}{dP}(\omega)=\frac{Q(\omega)}{P(\omega)}$; $\mathbb E_Q X=\mathbb E_P[LX]$, $\mathbb E_P L=1$ (sum over ω).
  2. Density process $Z_n=\mathbb E_P[L\mid\mathcal F_n]=\prod_{k\le n}\frac{q_{\omega_k}}{p_{\omega_k}}$ is a P-martingale (Doob martingale).
  3. Bayes: $\mathbb E_Q[X\mid\mathcal F_n]=\frac{\mathbb E_P[XL\mid\mathcal F_n]}{Z_n}$ (check the definition: for $A\in\mathcal F_n$, $\mathbb E_Q[X\mathbf 1_A]=\mathbb E_P[XL\mathbf 1_A]=\mathbb E_P[Z_n\,\tfrac{\mathbb E_P[XL\mid\mathcal F_n]}{Z_n}\mathbf 1_A]$).
  4. Discrete Girsanov: under P the step ξ is ±1 with mean 0; under Q it has mean $2q-1$. So $S_n$ is a P-martingale and $S_n-(2q-1)n$ is a Q-martingale.
  5. Esscher: $\frac{dQ}{dP}=\frac{e^{\theta R}}{\mathbb E_P e^{\theta R}}$; choose θ so that $\mathbb E_Q[e^{R}]=e^{r_f}$ (every asset earns the riskless rate under Q; Gerber–Shiu 1994, *TSA* 46:99–191 [V: https://pages.stern.nyu.edu/~dbackus/Disasters/Gerber_Shiu_94.pdf]).
- **Signature visual (recolour, don't move):** 200 coin-walk paths drawn under P as a grey `path_fan`. Then each path's stroke opacity and width animate to be proportional to its L under Q = 0.6. No path moves, yet the fan's visible centre of mass swings upward, and a side density (`side_density`) of S₅₀ morphs from P's to Q's. Caption: "a change of measure moves weight, not paths." Then the kept P/Q/L table and the L-collapse paths.
- **Experiment:** `measure` (kept) + `esscher`. Ken French daily log returns 1926–2020 with the Ken French rf. Expected (probe this session): θ ≈ −2.60. The mean daily log return goes from 3.64 bp under P to 0.60 bp under Q; the mass of the worst 1% of days rises from 1.00% to 1.13%. Q fattens the crash tail, which is what the risk premium pays for. Histograms P vs Q overlaid.
- **Lab 4:** `esscher_tilt`:
  ```python
  def esscher_tilt(x, target):
      """Weights w (dQ/dP up to a constant, e^{θx}) with E_Q[e^x] = e^target (Esscher 1932)."""
      x = np.asarray(x, float)
      def w(th):
          v = np.exp(th * (x - x.mean())); return v / v.sum()
      th = brentq(lambda th: np.log(w(th) @ np.exp(x)) - target, -100, 100)
      return th, w(th)
  ```
  Run it live: θ and the two histograms appear.
- **Predict:** "Under Q, are crash days more or less likely than under P?" (More.)

### 13 · Radon–Nikodym, and the singular infinite (3.2, new)
- **Goal:** the RN theorem through martingale convergence on dyadic partitions; equivalence and null sets; Kakutani's dichotomy.
- **Derivation:**
  1. $Q\ll P$ ($P(A)=0\Rightarrow Q(A)=0$) ⇒ $\exists L\ge0$: $Q(A)=\mathbb E_P[L\mathbf 1_A]$ (Radon 1913, Nikodym 1930).
  2. On the dyadic filtration: $Z_n(\omega)=Q(I_n(\omega))/P(I_n(\omega))$, with $I_n(\omega)$ the level-n cell. $\mathbb E_P[Z_{n+1}\mid\mathcal F_n]=Z_n$ (the two children's Q-masses add up to the parent's).
  3. $Z\ge0$ ⇒ converges (Ch10); $Q\ll P$ ⇒ UI ⇒ $Z_\infty=dQ/dP$ (Williams ≈14.13).
  4. Equivalent ($P\sim Q$): the same null sets. An arbitrage ($V_0=0$, $P(V_T\ge0)=1$, $P(V_T>0)>0$) is defined through null sets only, so it is invariant under $\sim$ (FTAP preview, Part 9).
  5. Kakutani: product measures $P=\otimes\mathrm{Ber}(p_k)$, $Q=\otimes\mathrm{Ber}(q_k)$, Hellinger affinity $\rho_k=\sqrt{p_kq_k}+\sqrt{(1-p_k)(1-q_k)}$. Then $\prod\rho_k>0\Rightarrow P\sim Q$ and $\prod\rho_k=0\Rightarrow P\perp Q$. With $q_k\equiv0.6$: $\rho=0.9949$, $\rho^n\to0$, so the measures are mutually singular (the strong law separates them). With $q_k=\frac12+\frac{c}{k}$: $\sum(q_k-\tfrac12)^2<\infty$ ⇒ equivalent.
- **Signature visual (`ThreeDScene`, density emerging):** P = uniform on the unit square and Q with density $f(x,y)=\frac{(1+2xy)}{1.5}$ (any smooth positive choice, stated on screen). 3D bars of height Q(cell)/P(cell) on a 2×2 grid, then 4×4, 8×8, 16×16, 32×32: each bar splits into four children whose average is the parent (a martingale), and the city of bars smooths into the surface dQ/dP while the camera orbits. A second, singular Q (mass on the diagonal) is then tried: its bars grow without bound along a ridge and fall to 0 elsewhere, and no surface emerges (Q ⊥ P). Then the kept L-collapse paths, recaptioned as Kakutani: under P, L → 0; under Q, L → ∞. P and Q are equivalent at every finite n and singular in the limit.
- **Experiment:** `radon` (dyadic ratios, exact) + `kakutani` (2,000 paths × 10,000 tosses for q = 0.6 and for q_k = ½ + 0.2/k, so Σ(q_k − ½)² < ∞). Expected: constant tilt gives median log₁₀L₁₀₀₀₀ ≈ −88 (= −10,000 × 0.0204/ln 10); decaying tilt gives L converging to a positive random limit with mean 1 (UI).
- **Predict:** "A fair coin and a 50.1% coin: equivalent on infinite sequences?" (No: any fixed tilt is singular; only a fading tilt keeps them equivalent.) Forward link: Cameron–Martin and Girsanov (Part 5), and why volatility cannot be changed by a change of measure (quadratic variation is measure-invariant).

### 14 · Heavy tails as stable laws (3.0, deepened)
- Keep: the Lévy family, Mandelbrot/Fama, McCulloch α by decade, the Mantegna–Stanley return probability, the truncated-Lévy verdict.
- **Add, derivation:** stability $X_1+\dots+X_n\overset d=n^{1/\alpha}X$ (symmetric, centred). Characteristic function $\varphi(t)=e^{-|ct|^\alpha}$, so $\varphi(t)^n=e^{-n|ct|^\alpha}=\varphi(n^{1/\alpha}t)$ (one line), and $-\log|\varphi(t)|=|c|^\alpha|t|^\alpha$, so $\log(-\log|\varphi(t)|^2)=\log(2c^\alpha)+\alpha\log|t|$ (Koutrouvelis 1980 regression). Generalized CLT: a tail ~ x^{−α}, α<2, gives a stable limit; α>2 gives the Gaussian.
- **Signature visual (the slope is α):** the empirical characteristic function $\hat\varphi(t)=\frac1n\sum e^{itr_j}$ computed live: a point spinning on the unit circle for one t, its average drawn as a vector whose length is
  |φ̂(t)|. Sweeping t moves a dot onto the log(−log|φ̂|²) vs log t plot; the dots line up, and a fitted line shows
  slope 1.4–1.6 (US) against 2.0 (Gaussian control).
- **Hands-on (a), a fit shown learning:** `stable_mle`. A maximum-likelihood fit of (α, β, γ, δ) with scipy's `levy_stable` on a 4,000-return subsample, Nelder–Mead with a callback logging each iterate. Replay: α's path and the NLL curve scrubbed together; 3 seeds (subsamples) as a spread band; the McCulloch estimate as a dashed baseline (same data). Narration branches on whether MLE and McCulloch agree within the seed band.
- **Experiment:** `stable` (kept) + `ecf` + `aggregation` (kurtosis of h-day sums, h = 1…60: a stable law predicts it constant, finite variance predicts it decays). Expected: US kurtosis decays from ≈ 20 at h=1 toward single digits by h = 20 (to be computed), confirming finite variance.
- **Predict:** "If returns were stable with α = 1.5, how would 4-day returns' width scale vs 1-day?" (4^{1/1.5} ≈ 2.52×, not 2×.)

### 15 · Ville's inequality and testing by betting (3.0, deepened)
- **Goal:** Ville's inequality proved; e-values; why peeking breaks p-values; Shafer–Vovk's game.
- **Derivation:**
  1. $W\ge0$ a (super)martingale, $W_0=1$; $\tau=\inf\{n:W_n\ge c\}$.
  2. $1\ge\mathbb E W_{\tau\wedge n}\ge c\,P(\tau\le n)$ (OST at the bounded time $\tau\wedge n$; $W\ge0$).
  3. $n\to\infty$: $P(\sup_nW_n\ge c)\le1/c$ (Ville 1939); with $c=1/\alpha$ this is an anytime-valid level-α test.
  4. e-value: $E\ge0$, $\mathbb E_{H_0}E\le1$ ⇒ $P(E\ge1/\alpha)\le\alpha$ (Markov). Calibration: $p\mapsto$ e-value via $\kappa p^{\kappa-1}$ (Vovk–Wang 2021 [K]).
  5. Peeking: $|S_n|/\sqrt n$ exceeds 1.96 infinitely often (LIL), so the daily t-test's false-alarm rate → 1.
- **Signature visual (two counters):** 2,000 fair games running live, two panels. Left: z-statistics with the ±1.96 band; each time a path touches the band it turns red and a "t-test false alarms" counter ticks (it climbs toward 50% by day 2,500). Right: e-process wealth paths on log axes with the 20 line; a "false alarms" counter that stops near 3.2% (kept numbers). The visual point is the counter on the left running away while the one on the right stops.
- Shafer–Vovk game card: Skeptic bets, Forecaster announces, Reality moves; probability = what Skeptic can't make money against.
- **Experiment:** `peeking` (kept; now saved per-day for the live replay).
- **Predict:** "Check a valid 5% t-test daily for 10 years on a fair game: false-alarm rate?" (About half.)

### 16 · Learning to bet (3.2, new; absorbs old ch9)
- **Goal:** the bettor is a learner. Its stake λ_t is learned online, its log-wealth is its score, and how fast it rejects depends on the edge and on how well it learns. The House's monitor is upgraded.
- **Derivation:**
  1. Wealth $W_t=\prod(1+\lambda_tx_t)$, $\lambda_t\in\mathcal F_{t-1}$, $|\lambda_t|\le\frac12$ ⇒ a nonnegative martingale under $H_0:\mathbb E[x_t\mid\mathcal F_{t-1}]=0$ (Ch4).
  2. Growth per step $g(\lambda)=\mathbb E\log(1+\lambda x)\approx\lambda\mu-\tfrac12\lambda^2(\sigma^2+\mu^2)$ (Taylor) ⇒ $\lambda^*\approx\mu/(\sigma^2+\mu^2)$, $g^*\approx\mu^2/2\sigma^2$ (Kelly, Part 8).
  3. Time to reject at 1/α: $\approx\log(1/\alpha)/g^*=2\log20/\mathrm{SR}_d^2$. A daily Sharpe of 0.05 (≈ 0.8 a year) needs ≈ 2,400 days ≈ 9.5 years; an annual Sharpe of 2 (daily 0.126) needs ≈ 380 days.
  4. ONS update (Cutkosky–Orabona 2018 [K]; used by Waudby-Smith–Ramdas 2024): $z_t=\frac{x_t}{1+\lambda_tx_t}$, $A_t=1+\sum z^2$, $\lambda_{t+1}=\mathrm{clip}(\lambda_t+\frac{2}{2-\log3}\frac{z_t}{A_t},\pm\frac12)$. aGRAPA: $\lambda_t=\mathrm{clip}(\hat\mu_{t-1}/(\hat\sigma^2_{t-1}+\hat\mu^2_{t-1}))$.
  5. Confidence sequence: $C_t=\{m:\ W_t(m)<1/\alpha\}$ (test every mean m at once and keep the ones not rejected) is valid at all times simultaneously.
- **Signature visual (TrainingReplay, as in ai21 `replay`):** left, the bettor's λ_t as a needle on a dial from −½ to ½, swinging and then settling near the Kelly fraction (a gold tick). Right, the log-wealth curve with the 20 line. Both are scrubbed by one ValueTracker through 10,000 steps of a simulated strategy with a daily Sharpe of 0.05. Then `measure`-style: rejection-time distributions for four bettors at equal budgets (the fixed-λ mixture, i.e. the current House `EProcess`; ONS; aGRAPA; the oracle Kelly) × edges {0, 0.02, 0.05, 0.1} × 8 seeds, drawn as bands. Narration branches on whether ONS beats the mixture at small edges. Finally a confidence sequence for Bitcoin's mean daily return (2018–2020), shrinking live and covering 0.
- **Experiment:** `learner`. Simulation grid (vectorized over 500 reps): 4 bettors × 4 edges × 10,000 steps, ≈10 min. Real: ONS on the Hook's sign test, US from 1926/1975/2000 and BTC from 2018; compare the date it crosses 20 with the mixture's (from `eprocess`). `confseq`: betting CS for the BTC mean, ≈2 min. Expected: at edge 0, rejection rate ≤ 5% for all four; median rejection time at SR_d = 0.05 ≈ 2,400 steps for the oracle, and somewhat more for learners.
- **Lab 5:** `ONSBettor` (new in `explainer/quant/house/martingale.py`):
  ```python
  class ONSBettor:
      """Testing by betting with an online-Newton-step stake (anytime-valid under mean-zero x)."""
      def __init__(self): self.lam, self.A, self.logw = 0.0, 1.0, 0.0
      def update(self, x):                     # |x| < 1
          self.logw += np.log1p(self.lam * x)
          z = x / (1 + self.lam * x)
          self.A += z * z
          self.lam = float(np.clip(self.lam + 2 / (2 - np.log(3)) * z / self.A, -0.5, 0.5))
          return np.exp(self.logw)
  ```
  Run it on 2,000 simulated days; the readouts "λ = 0.13, W = 4.2 …" update live. House rule 5 is restated.
- **Predict:** "A strategy with an annual Sharpe of 0.8: how many years before a perfect bettor can flag it at 1/20?" (≈ 9.5.)

### 17 · The house, the book and the market: industry (4.0, new)
Three firm cards (`firm_card`), one computed experiment each where possible. Public record only.

**(i) Casinos: a portfolio of martingales with drift.**
- Nevada statewide roulette hold (win ÷ drop): 17.34% in 2024; average 18.84% for monthly 2004–Feb 2026, monthly s.d. 3.15 pts, range 9.17–25.70%; blackjack 14.30% (2024) [V: UNLV Center for Gaming Research, *Nevada Table Games: Historical Hold Percentage Variations*, March 2026, https://www.library.unlv.edu/sites/default/files/2026-06/nv_table_hold.pdf]. The point: the edge is 5.26% per spin on a double-zero wheel, but chips are re-bet, so hold ≈ edge × turnover per dollar of drop (17.34/5.26 ≈ 3.3 spins per dollar bought in). This is Ch4's "the same tax per unit staked" at industrial scale.
- Table limits enforce bounded steps, which is when optional stopping holds (kept from the old ruin chapter).
- Computed `casino`: P(the house loses on N even-money unit bets). Azuma: $P(\text{loss})\le e^{-(N/37)^2/(2N)}=e^{-N/2738}$; normal approx z = (N/37)/√N; simulated. Expected: N = 10⁴ → Azuma 0.026, normal ≈ 3.5×10⁻³; N = 10⁵ → 10⁻¹⁶ (bound) vs z = 8.5. Then a simulated distribution of monthly hold with turnover 3.3 against the observed 3.15-pt s.d.: the narration branches on whether the spread of spins alone explains it (it should be smaller; mix of bet sizes and high rollers widens it).
- Advantage players: Thorp, *Beat the Dealer* (1962) [K]; *Uston v. Resorts International*, 445 A.2d 370 (N.J. 1982) [citation V via search; the holding, that Atlantic City casinos could not exclude counters on their own because the Casino Control Commission regulates the rules, is **(unverified wording)**]; Ivey (Ch11 numbers): the court held that changing the filtration by edge sorting was cheating.

**(ii) Bookmakers and the closing line.**
- Kaunitz, Zhong, Kreiner (2017), arXiv:1710.02824 [V: https://arxiv.org/abs/1710.02824]. They used the consensus of public odds as the probability (the market as the martingale), and bet where a book's odds exceeded it. Backtest 2005–15: 56,435 bets, 3.5% return; live: 265 bets of $50 over 5 months, 47.2% hit rate, $957.50 profit; then bookmakers "severely limit[ed]" their accounts [V: MIT Technology Review, 19 Oct 2017, https://www.technologyreview.com/2017/10/19/67760/the-secret-betting-strategy-that-beats-online-bookmakers/]. A bookmaker manages risk the way a casino does, and also by refusing the counterparties whose drift points the other way.
- Bill Benter: Hong Kong racing syndicate; "Computer based horse race handicapping and wagering systems: a report" (1994), in Hausch, Lo, Ziemba (eds.), *Efficiency of Racetrack Betting Markets* [V: https://econpapers.repec.org/bookchap/wsiwschap/9789812819192_5f0019.htm]. He combined a fundamental model with the public's odds. Bloomberg Businessweek (2018): "close to a billion dollars" [V: https://www.bloomberg.com/news/features/2018-05-03/the-gambler-who-cracked-the-horse-racing-code].
- Flutter (FanDuel) FY2024 10-K: sportsbook net revenue margin (revenue ÷ stakes) 7.9% vs 7.5% in 2023 **(definition V in the 10-K text; the 7.9% figure was seen only in a search summary: confirm the segment and number in MD&A before it goes on screen)** https://www.sec.gov/Archives/edgar/data/1635327/000162828025009852/flut-20241231.htm.

**(iii) Prediction markets and sequential testing.**
- Kalshi: *KalshiEX v. CFTC*, D.D.C., Judge Jia Cobb, Sept 2024: the CFTC exceeded its authority in barring congressional-control contracts; D.C. Cir. denied a stay; the CFTC later moved to drop its appeal [V: https://www.theblock.co/post/319206/federal-court-clears-kalshi-to-list-election-betting-contracts-denies-cftcs-motion].
- Polymarket 2024 US presidential market: ≈ $3.6bn cumulative volume; one French trader ("Théo") reported net profit ≈ $78.7m (Chainalysis) to ≈ $85m (WSJ) **(reported by secondary outlets; label "reported")** [V: https://www.theblock.co/post/324996/polymarket-whale-us-election-profit-france-ban].
- Is a betting price a martingale? Augenblick–Rabin (2021), *QJE* 136(2):933–985 [V: https://ideas.repec.org/a/oup/qjecon/v136y2021i2p933-985..html]: for a Bayesian, expected squared movement equals expected uncertainty reduction, $\mathbb E\sum(\pi_{t+1}-\pi_t)^2=\mathbb E[\pi_0(1-\pi_0)-\pi_T(1-\pi_T)]$ (the martingale's ⟨M⟩, Ch11). On 11 million Betfair transactions in 150,000 markets they find consistent excess movement, coming from high-frequency changes [V: abstract, https://rabin.scholars.harvard.edu/abstract-belief-movement-uncertainty-reduction-rational-updating]. Bürgi, Deng, Whelan (2025), "Makers and Takers: The Economics of the Kalshi Prediction Market," CESifo WP 12122: over 300,000 contracts, prices get more accurate near the close, there is a favourite–longshot bias, and it is stronger for takers [V: https://www.ifo.de/en/cesifo/publications/2025/working-paper/makers-and-takers-economics-kalshi-prediction-market; the "−22% average return after fees" figure is **(unverified)**].
- Computed `beliefs`: the movement/uncertainty-reduction ratio on (a) simulated Bayesian forecasts (best-of-21, Ch3) → 1.00 ± s.e.; (b) a simulated forecaster who overreacts by 30% → ratio > 1. The Doob martingale from Ch3 is checked here as a test.
- Sequential testing in industry: Optimizely's always-valid p-values (Johari, Koomen, Pekelis, Walsh, *Operations Research*, DOI 10.1287/opre.2021.2135) [V: https://arxiv.org/abs/1512.04922]; Netflix canary releases (Lindon, Sanden, Shirikian, KDD 2022, arXiv:2205.14762) [V: https://arxiv.org/abs/2205.14762]; Wald's SPRT (1945) as the origin. Trading desks monitoring strategy decay with CUSUM or sequential tests is common practice, but no firm-specific public source was found: say "standard practice" without naming a firm.
- **Predict:** "Roulette's edge is 5.26%; why do casinos report ≈ 17% hold?" (Chips are re-bet ≈ 3× per dollar bought.)

### 18 · Frontier: anytime-valid inference, 2023–2026 (3.0, new)
On screen as `history_card`s on a 2023–2026 strip, each with one line on what it found. All [V]:
- Ramdas, Grünwald, Vovk, Shafer (2023), "Game-theoretic statistics and safe anytime-valid inference," *Stat. Sci.* 38(4):576–601, arXiv:2210.01948, https://projecteuclid.org/journals/statistical-science/volume-38/issue-4/Game-Theoretic-Statistics-and-Safe-Anytime-Valid-Inference/10.1214/23-STS894.full
- Ruf, Larsson, Koolen, Ramdas (2023), "A composite generalization of Ville's martingale theorem using e-processes," *EJP* 28, art. 127, arXiv:2203.04485. An event is null exactly when some nonnegative martingale (e-process) blows up on it. https://arxiv.org/abs/2203.04485
- Waudby-Smith, Ramdas (2024), "Estimating means of bounded random variables by betting," *JRSS B* (DOI 10.1093/jrsssb/qkad009; vol. 86(1):1–27 **(volume/pages unverified)**), arXiv:2010.09686. Betting confidence sequences, which Ch16 uses.
- Shekhar, Ramdas (2024), "Nonparametric two-sample testing by betting," *IEEE Trans. Inf. Theory* 70(2):1178–1203, arXiv:2112.09162. Relevant to regime-change detection.
- Grünwald, de Heide, Koolen (2024), "Safe testing," *JRSS B* 86(5) (read before the RSS 24 Jan 2024), arXiv:1906.07801. https://imstat.org/meetings-calendar/rss-discussion-paper-meeting-safe-testing-by-grunwald-et-al/
- Grünwald (2024), "Beyond Neyman–Pearson: e-values enable hypothesis testing with a data-driven alpha," *PNAS* 121(39), arXiv:2205.00901.
- Larsson, Ramdas, Ruf (2025), "The numeraire e-variable and reverse information projection," *Ann. Statist.* **(venue per a talk listing; verify)**, arXiv:2402.18810. The log-optimal e-variable is finance's numéraire (Kelly) portfolio. https://arxiv.org/abs/2402.18810
- Fischer, Ramdas (2025), "Sequential Monte-Carlo testing by betting," *JRSS B* (DOI 10.1093/jrsssb/qkaf014), arXiv:2401.07365. Anytime-valid permutation tests, which apply to backtests (Part 26).
- Ramdas, Wang (2025), *Hypothesis Testing with E-values*, Foundations and Trends in Statistics 1(1–2):1–390, arXiv:2410.23614, https://nowpublishers.com/article/Details/STA-002
- Background (pre-2023, on screen as the base): Wang, Ramdas (2022), "False discovery rate control with e-values," *JRSS B* 84(3):822–852 (e-BH).
- **Signature visual (the numéraire bridge):** split screen. Left, the Kelly portfolio's wealth from Part 8's preview; right, the log-optimal e-variable's wealth on the same simulated returns. They are the same curve, and the label morphs from "numéraire portfolio" to "numeraire e-variable". This links Part 4 to Parts 8 and 9.
- **Experiment:** `ebh`. 200 simulated strategies (20 with a true daily Sharpe of 0.08, 180 null) monitored by ONS e-processes for 2,520 days; e-BH at 10% applied each day; 20 seeds. Expected: realized FDR ≤ 10% on every day for every seed (bands), with discoveries rising over time. Compare BH on daily t-test p-values, whose FDR inflates under peeking.
- **Lab 6:** `e_bh`:
  ```python
  def e_bh(e, alpha=0.1):
      """Wang & Ramdas (2022): reject the k* largest e-values, k* = max{k : e_(k) >= K / (alpha k)}."""
      e = np.asarray(e, float); K = len(e); order = np.argsort(e)[::-1]
      ok = np.flatnonzero(e[order] >= K / (alpha * np.arange(1, K + 1)))
      return order[: ok.max() + 1] if len(ok) else order[:0]
  ```
- **Predict:** "Monitor 200 strategies daily; does e-BH's guarantee survive peeking?" (Yes: e-processes stopped at any time remain e-values.)

### Outro (2.8, deepened)
Recap (18 lines in 6 cards); desk questions (below); problem set (`problem_set`, 6 problems, ~90 s); payoffs (Parts 5, 8, 9, 12, 23, 26, 40); references card; House chart: the monitor at the data desk, flowing to research (Part 26). Next: Part 5.

---

## 5. Revised SYLLABUS.md §6 entry (ready to paste)

```markdown
### Part 4 · Martingales and Measure (~58)
1. Probability spaces and filtrations as information: σ-algebras as the questions you can answer, measurability,
   Kolmogorov (1933); coin space as the unit interval.
2. Conditional expectation as orthogonal projection: Kolmogorov's definition, the properties, the tower; regression
   is the same projection with data.
3. Martingales: Ville (1939) named them after a betting system; Doob; sub- and supermartingales; Jensen.
4. You can't beat the system: the martingale transform, and the same tax per unit staked for every roulette system.
5. Stopping times and optional stopping, proved: the walk that always wins, with E[τ] = ∞; Wald; uniform
   integrability; pattern waiting times (Li 1980).
6. The doubling strategy, admissibility (Harrison–Pliska 1981; Dybvig–Huang 1988), and Barings (1995): doubling
   down in Leeson's "88888" account.
7. Gambler's ruin and bold play (de Moivre; Dubins–Savage 1965); expected duration.
8. Martingale convergence: upcrossings, Pólya's urn, Lévy's upward theorem as learning.
9. Doob decomposition: drift plus martingale, ⟨M⟩; the drift depends on the filtration (Ivey v Genting, 2017).
10. Change of measure on a coin: density process, Bayes, discrete Girsanov, the Esscher transform on real returns.
11. Radon–Nikodym by martingales; equivalent measures agree on what is impossible; Kakutani's dichotomy.
12. Heavy tails: stable laws (Lévy; Fama 1965; Mantegna–Stanley 1995), the characteristic function and the
    generalized CLT.
13. Game-theoretic probability (Shafer–Vovk): Ville's inequality, testing by betting, e-values, anytime-valid
    inference (Ramdas et al. 2023); learning the bet (ONS, aGRAPA); confidence sequences.

*Textbooks:* Williams *Probability with Martingales* ch. 9–14; Shreve I ch. 2, 3, 5; Shreve II ch. 1–2;
Föllmer–Schied §1.2 (preview) and App. A.2.
*Computed:* conditional means of the market by era; six betting systems; first passage and Wald; pattern waits;
doubling and a schematic doubling rule on the 1995 Nikkei; Pólya's urn and upcrossings; a Bayesian drift learner;
Doob's decomposition of the market; the Esscher measure of US returns; dyadic Radon–Nikodym and Kakutani; stable
fits (McCulloch, ECF, MLE replayed); peeking; online bettors trained and compared; e-BH on 200 strategies;
casino hold and Azuma.
*Visuals:* the coin-space zoom; projection in 3D; the curtain desk; the bell and the curtain; the leaking balance;
the staircase and the cliff; the upcrossing trader; one P&L with two drifts; paths recoloured, not moved; the 3D
density emerging from dyadic bars; the bettor's needle learning Kelly.
*Crisis:* Barings 1995. *Firms:* casinos (Nevada hold vs edge), advantage players (Thorp, Uston, Ivey), bookmakers
(Kaunitz et al. 2017, Benter), prediction markets (Kalshi, Polymarket, Betfair), sequential testing (Optimizely,
Netflix).
*Desk:* "A martingale starts at 1 and stops at 0 or 3. Probability it hits 3?"; "Expected flips to HH?";
"Penney's game: you pick HHT, I pick THH. Who wins?"; "A fair walk is stopped the first time it is up 1. E[τ]?"
*House:* the e-value monitor with learned bets (`ONSBettor`), confidence sequences and e-BH (used again in Part 26).
```

New desk solutions for the README: Penney: THH beats HHT with probability 3/4 (HHT can only be preceded by T…HH once a T has appeared, unless the first two tosses are HH, probability ¼). E[τ₁] = ∞ by Wald (Ch5). New problems: (6) Pólya's limit is Uniform(0,1) (induction: P(R_n = k) = 1/(n+1)); (7) Wald's identity, proved via the martingale S_n − nμ and OST under E τ < ∞. Keep problems 1–5.

---

## 6. Minutes, compute budget, House additions

### Minutes per chapter (estimate; ≈165 words/min)
Hook 3.0 · 1: 2.8 · 2: 3.2 · 3: 2.8 · 4: 2.8 · 5: 3.0 · 6: 3.2 · 7: 2.6 · 8: 2.4 · 9: 2.6 · 10: 3.2 · 11: 3.2 · 12: 3.2 · 13: 3.2 · 14: 3.0 · 15: 3.0 · 16: 3.2 · 17: 4.0 · 18: 3.0 · Outro 2.8 → **≈ 58.2 min** (floor 50 cleared by 8 min; if the first render runs long, trim 9 and 8 first).

### Compute items (`python -m videos.quant.quant4.compute`, seeded `default_rng(seed)`, cached in `.cache/quant4/`)

| Item | Status | What | Est. CPU min |
|---|---|---|---|
| doob, measure, ruin, stable, nikkei, peeking, eprocess, envelope | kept (peeking: save per-day series; ruin: + durations) | — | 4 |
| condexp | new | era conditional means, 200 block-bootstrap seeds | 1 |
| martingales | new | call value vs maturity on the walk; next-step fans | <1 |
| systems | new | 6 systems × 2 games × 20,000 sessions | 4 |
| firstpassage | new | 10,000 walks to 10⁵ steps, chunked | 5 |
| patterns | new | 200,000 sequences × 6 patterns; Penney | 2 |
| doubling | new | 1,000 doublers × 3,000 sessions | 2 |
| nikkei_doubling | new | schematic rule on FRED NIKKEI225 1994-07 → 1995-03 | <1 |
| polya, upcrossings | new | 10,000 urns × 2,000; Doob's bound | 1 |
| drift_posterior | new | Bayesian daily-mean learner on KF 1926–2020, checkpoints | 1 |
| ivey_sim | new | 10,000 hands, two filtrations | <1 |
| esscher | new | θ, P/Q histograms (KF mkt + rf) | <1 |
| radon, kakutani | new | dyadic bars to 32×32; 2,000 × 10,000 tosses × 2 tilts | 3 |
| ecf, aggregation | new | ECF regression with bootstrap; kurtosis vs h | 3 |
| stable_mle | new, resumable per seed | levy_stable MLE, 3 seeds × 4,000 obs, iterates logged | 30–45 (fallback: 2,000 obs) |
| learner | new | 4 bettors × 4 edges × 500 reps × 10,000 steps; real-data ONS | 12 |
| confseq | new | betting CS for BTC mean (Binance 1d, 2018–2020) | 2 |
| casino | new | Azuma vs normal vs simulation; monthly-hold simulation | 3 |
| beliefs | new | Augenblick–Rabin ratio on simulated Bayesian/overreacting forecasts | 2 |
| ebh | new | 200 strategies × 2,520 days × 20 seeds, ONS + e-BH vs BH | 8 |
| **Total** | | | **≈ 85–100 min** on 4 cores (inside the 2 h budget) |

Data: `data.ken_french_daily` (mkt, rf), `data.binance_klines("BTCUSDT","1d")`, `data.fred("NIKKEI225")`, and simulations. The research window stays at 2020 (sealed envelope). New registrations in `envelope`: the ONS sign tests (4 trials), the BTC confidence sequence (1); the trial counter shows 10.

### House library additions (`explainer/quant/house/martingale.py`, tests in `tests/test_quant_house.py`)
`cond_exp`, `martingale_transform`, `stake rules` (doubling, d'Alembert, Labouchère, Fibonacci, Paroli, Oscar), `first_passage_survival` (exact P(S_n ∈ {0,1})), `pattern_wait`, `polya_urn`, `upcrossings`, `esscher_tilt`, `hellinger_affinity`, `ecf_alpha` (Koutrouvelis regression), `ONSBettor`, `AGrapaBettor`, `betting_cs`, `e_bh`. Tests: `pattern_wait("HH") == 6`, `cond_exp` agrees with brute force, `e_bh` reduces to BH on calibrated p-values, the `ONSBettor` false-alarm rate is ≤ α on 2,000 null runs, `esscher_tilt` hits its target to 1e-10.

### Open checks before writing narration
1. Barings: the BoBS report's own figures (loss, dates, position sizes) before anything beyond the current card goes on screen.
2. The Flutter 7.9% margin and its segment, from the 10-K MD&A.
3. The *Uston v. Resorts* holding wording.
4. The Bürgi–Deng–Whelan return figures (only the qualitative findings are cleared).
5. Waudby-Smith–Ramdas volume and pages; the Larsson–Ramdas–Ruf venue; the Augenblick–Lazarus–Thaler venue (QJE 2025? unverified, so it is not used on screen).
6. Williams section numbers marked ≈.

