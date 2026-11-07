# Quant, Built — Part 17: Deep Pricing and Hedging

The scientific and bilingual visual polish is in progress. Historical build notes below do not certify current-source renders. Final artifact-bound checks will be recorded in the [sequential QA log](../../../docs/qa/quantitative-finance-polish.md); full continuous production-voice listening remains a separate pending pass.

Part 17 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the frontier of Act III, Derivatives. It covers:

* learning a pricing formula from prices (Hutchinson, Lo and Poggio 1994), hedging with it, and a network's Greeks;
* the neural calibrator for rough Bergomi (Horvath, Muguruza and Tomas 2021): learning the map, label noise,
  calibrating through the network, and two years of weekly surfaces;
* differential machine learning (Huge and Savine 2020) and its classical twin, a Gaussian process with gradients;
* high dimensions: the deep BSDE solver (E, Han and Jentzen 2017; Han, Jentzen and E 2018) and deep optimal stopping
  (Becker, Cheridito and Jentzen 2019);
* the deep hedger (Buehler, Gonon, Teichmann and Wood 2019): the indifference price, entropic risk and CVaR, the drift
  trap, and where it learns not to trade (Leland 1985; Whalley and Wilmott 1997; Imaki et al. 2021);
* neural SDEs and robust bounds for exotics (Gierjatowicz et al. 2022);
* market generators, judged by the stylized facts of Part 1, and hedgers tested across them;
* production and model risk (SR 26-2, 17 April 2026, replacing SR 11-7; PRA SS1/23), what has reached desks, and the
  frontier of 2023–2026.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`deep`](../../../explainer/quant/house/deep.py) module), and every network was trained on one shared CPU, most of
them several times (seeds), with checkpoints so the training can be replayed on screen. The production version
retrains them at full size. Data: Part 13's Deribit BTC option surfaces, and Binance daily BTC closes.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 64 minutes)

* **A machine that hedges** (2.7 min). A network learns a corridor around delta at 0.5% costs; it needs 3.01 where
  daily delta hedging needs 3.55, and on one simulated month it trades on 11 of 30 days; J.P. Morgan's data-driven
  hedging of index option books since 2018 (as reported by Risk.net); the history strip (1985–2026); the plan.
* **1. Learning a pricing formula** (3.2). Hutchinson, Lo and Poggio (1994) redone: Merton's homogeneity, universal
  approximation, a 3 × 64 network trained on 66,150 simulated prices (worst error 0.05% of the strike), its delta
  hedging 200 fresh options as well as the true delta (tracking error 0.214–0.217 against 0.209); **lab**:
  `train_mlp_regressor`.
* **2. A network's Greeks** (2.8). The second derivative of a ReLU network vanishes almost everywhere: its gamma error
  is 12 times SiLU's; butterflies priced by the network are negative 13% of the time with ReLU, 4% with SiLU, never
  with softplus (Breeden–Litzenberger).
* **3. The neural calibrator: learning the map** (3.0). 12,000 rough Bergomi parameter sets, 894,903 Monte Carlo
  labels, a 4 × 96 network over 40 epochs; label noise bounds the held-out error, and the gap to a fresh simulation
  overstates it by √1.5.
* **4. Calibrating through the network** (3.1). A tanh map into the training box and its vanishing gradient at the
  walls; 12 starts of Adam and L-BFGS fit the Surface to 0.97 vol points in 2.8 s (H = 0.074, η = 1.89, ρ = −0.40),
  against hours by simulation; **lab**: `calibrate_neural`.
* **5. Rough volatility, week by week** (2.3). 100 weekly surfaces: 77 calibrations end on the box's floor H = 0.02,
  every Monte Carlo re-check agrees within half a vol point; argmin in the box is not the market's H.
* **6. Differential machine learning** (2.7). Pathwise derivatives as labels (Huge and Savine 2020), unbiased by
  dominated convergence: with 256 samples the price error falls from 3.69–5.28 to 0.43–0.81 and deltas are 22 times
  more accurate; **lab**: the twin loss.
* **7. Differential labels in three dimensions** (2.5). Tangent planes on 64 payoffs; the Gaussian process with
  gradients (Dixon, Halperin and Bilokon, ch. 3) as the exact twin: grid errors 45.4 / 6.6 / 3.5 (payoffs only,
  with slopes, GP), and its cubic cost.
* **8. A hundred dimensions: the deep BSDE** (3.0). Itô and the non-linear Feynman–Kac formula (Pardoux–Peng 1990);
  Han, Jentzen and E's default-risk claim on 100 assets; shooting from a guessed u₀ with 39 small networks; the
  curse of dimensionality against polynomial work; Deep Galerkin and multilevel Picard.
* **9. Watching the deep BSDE converge** (2.6). 256 test paths landing on their payoffs; 57.35 ± 0.05 against the
  reference 57.300 (+0.08%); the linear check without default lands 4.04 below plain Monte Carlo; **lab**: the
  forward sweep.
* **10. Deep optimal stopping** (3.4). Becker, Cheridito and Jentzen (2019): bang-bang decisions, one network per
  date; the five-asset Bermudan max-call at 26.107 ± 0.040 against Longstaff–Schwartz's 26.103 ± 0.028 and the
  published [26.156, 26.162]; two assets 13.886 against a tree's 13.902; the exercise tunnel in 3D.
* **11. The deep hedger** (3.1). Buehler, Gonon, Teichmann and Wood (2019): entropic risk, cash invariance, the
  indifference price; with no costs the network converges onto delta (price 2.360 against 2.355, holdings within
  0.095 shares); **lab**: `hedge_pnl`.
* **12. Risk measures and the drift trap** (3.6). CVaR by Rockafellar–Uryasev (the learned w = 2.819, the empirical
  VaR 2.818); under a 30% drift the hedger adds Merton's μ/γσ²S, a bet on the drift (the drift-trained hedger prices
  2.292 against 2.385); QLBS, RL hedging and deep Bellman hedging.
* **13. Where not to trade** (3.0). The band opening in the trade map; Leland (1985: σ̂ = 26.5% at 0.5% costs) and
  Whalley–Wilmott's cube-root band (1997) derived; at 0.5% costs: daily delta 3.55, Leland 3.37, Whalley–Wilmott
  3.08, the band network 3.01.
* **14. The band as a surface** (3.1). The learned band's two sheets over time and price against Whalley–Wilmott's
  (width at the money 0.22 at 30 days, 0.28 at 5; theirs 0.31 and 0.58); Imaki et al.'s architecture and Davis,
  Panas and Zariphopoulou (1993); doubling the cost widens it 1.17 times against 2^{1/3} = 1.26; **lab**:
  `Hedger.band`.
* **15. Neural SDEs and robust bounds** (3.5). Gierjatowicz et al. (2022): 36 vanillas repriced within 0.19 vol
  points while a down-and-out call ranges from 0.0671 to 0.0703 (Heston 0.0685); the two extreme smiles never more
  than 0.72 vol points apart; the bounds nest inside Part 9's MOT bounds.
* **16. Market generators** (3.7). GJR-GARCH, a signature-trained network and a diffusion model invent 32-day bitcoin
  windows, scored on the stylized facts and on expected-signature distances; four real and four invented windows.
* **17. Production and model risk** (3.1). SR 26-2 (17 April 2026) replacing SR 11-7, PRA SS1/23; the checklist
  applied to this part's networks; the known-answer scoreboard; firm files (J.P. Morgan, Danske Bank).
* **18. The frontier, 2023 to 2026** (1.8). Generative option markets (SANOS, DYSANOS, GROMM), whether deep hedgers
  hedge, second-order training, stopping and duals, signature-kernel generators; one claim re-run.
* **19. Rule 17, tested** (1.7). Four hedgers priced on Black–Scholes paths, on GJR-GARCH paths and on 1,010 real
  30-day stretches of bitcoin; Rule 17 (no network without a slower independent engine; inputs outside the box go to
  it; hedgers tested on two generators and on history).
* **For the researcher: the deep BSDE's loss as an error certificate** (4.7). In the linear case (no default),
  Y_T − g = e^{RT}(y₀ − u₀) + ∫e^{R(T−t)}(Z − Z*)·dW, so by Itô's isometry the loss is e^{2RT}(y₀ − u₀)² plus the
  hedge's error and |y₀ − u₀| ≤ e^{−RT}√loss; Han and Long (2020) prove sup E|Y − Ŷ|² + E∫|Z − Ẑ|² ≤ C(h + loss) for
  Lipschitz drivers. Ten-dimensional basket minimum (reference 72.548 ± 0.006 from 2 million paths), trained 3,000
  iterations at N = 5/10/20/40 steps: the error never crosses the bound; final loss 17.4/12.2/9.3/9.6, bound
  4.09/3.42/2.98/3.03, actual error 0.004/0.016/0.044/0.138 (loose by 20–1,000×: the loss is mostly the hedge's
  variance); the floor falls with h, then the networks' own error takes over. The 100-dimensional default-risk run of
  chapter 9: y₀ → 57.3 inside y₀ ± √loss (indicative, the constant unknown). Three open problems; pause: loss 9 at
  R = 2%, T = 1 bounds the price error by e^{−0.02} × 3 = 2.94; with the true hedge the loss would shrink to
  e^{2RT}(y₀ − u₀)² plus the time-step floor.
* **Recap, desk questions, ten problems (two at qualifying-exam level)** (2.7). Eleven lines; four desk questions;
  solutions below.

## Hands-on

* **Labs** (the House's own code on screen, then run): `train_mlp_regressor` (ch. 1), `calibrate_neural` (ch. 4),
  `train_differential` (ch. 6), `deep_bsde`'s forward sweep (ch. 9), `deep_stopping` (ch. 10), `hedge_pnl` (ch. 11),
  `Hedger.band` with `quoting.ww_band` (ch. 14).
* **Training replays** (seeds as bands): HLP's network (3 seeds), the calibrator (2 seeds), the calibration itself
  (12 starts), differential ML (3 seeds), the deep BSDE (2 seeds and the linear run), deep stopping date by date, the
  no-cost hedger converging onto delta (3 seeds), the drift-trained hedger onto Merton's line (3 seeds), the band
  opening in the trade map (3 seeds), a Whalley–Wilmott start against the default (2 seeds each), the neural SDE's
  calibration and push, the diffusion model (3 seeds).
* **3D:** the learned price surface and its error; the network's implied-volatility surface converging onto the
  Surface's quotes; tangent planes and the Gaussian-process shell; the exercise tunnel; the band's two sheets over
  (time, price) with a path riding between them; the low and high neural-SDE surfaces over Heston's.

## Textbook audit

| Book · chapter | Where |
|---|---|
| Dixon–Halperin–Bilokon 1 (statistical learning, ML in finance) | ch. 1 |
| DHB 2 (probabilistic modelling) | Parts 6, 27 |
| DHB 3 (Bayesian regression, Gaussian processes) | ch. 7: a GP with gradient observations as the twin of differential ML |
| DHB 4 (feedforward networks, universal approximation, back-propagation) | ch. 1 (UAT, the training replay), ch. 2 |
| DHB 5 (interpretability: sensitivities, Jacobians) | ch. 2: a pricing network's Greeks are its Jacobian and Hessian |
| DHB 6–7 (sequence models, HMMs, filters) | Part 7; ch. 16 uses GJR-GARCH as a baseline |
| DHB 8 (RNNs, LSTMs, CNNs) | ch. 16 (the LSTM generator; Quant GANs' convolutions) |
| DHB 9 (introduction to RL) | Part 8 |
| DHB 10 (RL in finance: QLBS) | ch. 12 (QLBS and RL hedging as the RL view of the same objective) |
| DHB 11 (inverse RL) | Part 29 |
| DHB 12 (frontiers) | ch. 18 |
| Kelly–Xiu, *Financial Machine Learning* (the virtue of complexity) | ch. 1 (an over-parameterized network fits 66,150 prices without overfitting); returns → Parts 25–30. Derivatives are not a core topic of the survey |
| Jentzen–Kuckuck–von Wurstemberger, *Mathematical Introduction to Deep Learning* | ch. 9 (why the cost is polynomial in the dimension) |
| Glasserman ch. 7 (pathwise and likelihood-ratio Greeks) | Part 16; ch. 6 proves the pathwise label unbiased, ch. 7 sends the digital back to the LR method |
| Glasserman ch. 8; Savine (AAD) | Part 16 (LSM, duality, the tape); ch. 10 uses Part 16's LSM number, ch. 6 its adjoint labels |
| Shreve II 6.4/6.6; Øksendal 8 (Feynman–Kac) | Part 5; ch. 8 derives the non-linear version (Pardoux–Peng) |
| Gatheral 2–3 | Parts 12–13; ch. 15 calibrates a neural SV model to Heston prices |

## Papers, chapter by chapter

* ch. 1 Hutchinson, Lo and Poggio (1994); Cybenko (1989); Hornik (1991); Ruf and Wang (2020, a review of "far over a
  hundred" papers). ch. 2 Breeden–Litzenberger (Part 12); Dugas et al. (2009); Ackerer, Tagasovska and Vatter (2020).
* ch. 3–5 Hernandez (2016); Bayer and Stemper (2018); Liu, Oosterlee and Bohte (2019); Horvath, Muguruza and Tomas
  (2021).
* ch. 6–7 Huge and Savine (2020); DHB ch. 3.
* ch. 8–9 E, Han and Jentzen (2017); Han, Jentzen and E (2018); Pardoux and Peng (1990); Sirignano and Spiliopoulos
  (2018); Hutzenthaler, Jentzen, Kruse and Nguyen (2020).
* ch. 10 Becker, Cheridito and Jentzen (2019, Table 1: [26.156, 26.162] for five assets); Broadie and Detemple (1997);
  Longstaff and Schwartz (2001, Part 16).
* ch. 11–12 Hodges and Neuberger (1989); Buehler, Gonon, Teichmann and Wood (2019); Rockafellar and Uryasev (2000);
  Merton (1969); François, Gauthier, Godin and Pérez Mendoza (2024); Buehler, Murray, Pakkanen and Wood (2021);
  Halperin (QLBS); Kolm and Ritter (2019); Cao, Chen, Hull and Poulos (2021); Buehler, Murray and Wood (2022).
* ch. 13–14 Leland (1985); Whalley and Wilmott (1997); Davis, Panas and Zariphopoulou (1993); Imaki, Imajo, Ito,
  Minami and Nakagawa (2021); Arzel and Lehdili (2026).
* ch. 15 Gierjatowicz, Sabate-Vidales, Šiška, Szpruch and Žurič (2022); Cuchiero, Khosrawi and Teichmann (2020);
  Guyon and Mustapha (SSRN 4309576).
* ch. 16 Ho, Jain and Abbeel (2020); Wiese, Knobloch, Korn and Kretschmer (2020); Buehler, Horvath, Lyons, Perez
  Arribas and Wood (2020); Liao, Ni, Szpruch, Wiese, Sabate-Vidales and Xiao (2020); Ni, Szpruch, Sabate-Vidales, Xiao,
  Wiese and Liao (2021); Kidger, Foster, Li, Oberhauser and Lyons (2021); Chevyrev and Oberhauser (2022).
* ch. 17 SR 11-7 (2011); SR 26-2 (2026); PRA SS1/23; Risk.net on J.P. Morgan and Danske; Cherrat et al. (2023,
  *Quantum* 7, 1191); Ferguson and Green (2018).
* ch. 18 SANOS (2026), DYSANOS (2026), GROMM (2026); Zernikov (2026); Godin (2026); Mueller, Akkari, Gonon and Wood
  (2024); François et al. (2025); Reppen, Soner and Tissot-Daguette (2022); Bayer, Pelizzari and Schoenmakers (2023);
  Ye and Wong (2025); Issa, Horvath, Lemercier and Salvi (2023).

## Build it

```bash
python -m videos.quant.quant17.compute calib_data          # 60 resumable chunks, ~1 h (two processes share them)
python -m videos.quant.quant17.compute                     # everything else; every training item checkpoints and resumes
EXPLAINER_TTS=silent python tools/qa_scene.py quant17 Band # one chapter, silent, with a contact sheet
python tools/make.py quant17 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Your hedger has costs. Why does the optimal hedge have a band?**
   * Holding δ instead of the frictionless Δ adds hedging variance of order (δ − Δ)²σ²S² per unit time, so the risk
     grows with the square of the gap.
   * Trading back costs c|δ − Δ|S, linear in the gap.
   * Near Δ the quadratic risk is smaller than the linear cost, so it pays to wait until the gap is large enough.
     Balancing the two gives a band of half-width (3cSΓ²/2γ)^{1/3} (Whalley–Wilmott), widest where gamma is large.
   * The deep hedger learns the same principle without the asymptotics (chapters 13–14).
2. **A neural calibrator fits the surface beautifully. How do you know it is right?**
   * Re-price the calibrated parameters with the slow engine (fresh Monte Carlo) and compare errors.
   * Check every input lies inside the training ranges: in chapter 5, H pressed against the floor of the box, where
     the tanh map's gradient vanishes (chapter 4).
   * Know the network's error against fresh simulation, separated from the noise of its own labels (chapter 3).
   * A network extrapolates silently, so these checks are part of the model, not an extra.
3. **You have a thousand simulated payoffs. Why also record their derivatives?**
   * With adjoint differentiation each sample's pathwise derivatives cost about one extra pricing, and give d labels
     more per sample; for a Lipschitz payoff they are unbiased estimates of the delta.
   * They pin down the function's shape between samples: prices, and above all Greeks, need far fewer samples.
   * Not for a digital: its pathwise derivative is zero almost surely (use likelihood-ratio labels or smoothing).
4. **Your deep hedger makes money on average with no costs. Is it hedging?**
   * Partly it is speculating. Under a drift μ the exponential-utility hedge is Δ + μ/(γσ²S): Merton's portfolio on
     top of the replicating hedge (chapter 12).
   * Compare its holdings with delta and price it on driftless paths; it needs more there than a driftless hedger.
   * Train under a (near-)martingale measure (Buehler et al. 2021), or use a risk measure that weighs bad outcomes
     enough (François et al. 2024), unless the drift is a view you mean to hold.

## Problems, with solutions

1. **Indifference price.**
   * ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c, so the entropic risk is cash invariant.
   * Without the claim and with a martingale stock, not trading is optimal and the minimal risk is 0. With it, the
     seller is indifferent when ρ(−Z + hedge − costs + p) = 0, i.e. at p = min_δ ρ(−Z + (δ·S)_T − C_T).
2. **The band's scaling.**
   * Over dt, a gap ε costs (γ/2) ε² σ²S² dt of certainty equivalent.
   * Keeping the gap within ±h means trading about (σ²S²Γ²/h) dt shares at cost cS per share; inside, E ε² = h²/3.
   * Minimizing γh²σ²S²/6 + cSσ²S²Γ²/h over h gives h³ = 3cSΓ²/2γ.
3. **The BSDE behind the solver.**
   * By Itô, dY = (u_t + 𝓛u) dt + ∇uᵀσ(X) dW.
   * The PDE says u_t + 𝓛u = (1 − δ)Q(u)u + Ru = f(Y), so dY = f(Y) dt + Z·dW with Z = σ(X)ᵀ∇u and Y_T = min_i X_T^i.
4. **Differential regression.** With features Φ (n × p) and their input gradients ∇Φ, minimize
   ‖Φw − y‖² + λ‖∇Φ w − ∂y‖². The normal equations are (ΦᵀΦ + λ ∇Φᵀ∇Φ) w = Φᵀy + λ ∇Φᵀ∂y.
5. **Deep stopping's bound.**
   * Given X_n, the objective g_n F + E[G_{n+1}|X_n](1 − F) is linear in F, maximized by F = 1{g_n ≥ E[G_{n+1}|X_n]}.
   * Any {0,1} rule defines a stopping time τ, and E[g_τ] ≤ sup_τ E[g_τ], the Bermudan price.
6. **Leland's volatility.** Between rebalances ΔΔ ≈ ΓΔS, so E|ΔΔ|S = ΓS²σ√Δt √(2/π). The cost per unit time is
   (k/2)ΓS²σ√(2/π)/√Δt with round-trip cost k = 2c. Adding it to ½σ²S²Γ in the pricing equation of a short option gives
   ½σ̂²S²Γ with σ̂² = σ²(1 + √(2/π) k/(σ√Δt)).
7. **Merton's term.** In a complete market with zero rates, the terminal wealth with the claim is −Z + (δ·S)_T. Write
   δ = Δ + η: the Δ part replicates Z exactly, leaving max E[−e^{−γ(x − p + (η·S)_T)}], the no-claim CARA problem, whose
   solution holds μ/(γσ²) in money, i.e. η = μ/(γσ²S).
8. **Label noise.** If y = F + ε with ε independent of the network's prediction F̂, E(F̂ − y)² = E(F̂ − F)² + E ε² ≥ E ε².
   Doubling the label variance raises this floor, but a smooth fit to many labels near each θ averages their noise, so
   the network's own error E(F̂ − F)² grows much less than the labels' variance.
9. **(qual) The loss decomposition.** Solve the linear SDE: Y_T = e^{RT}y₀ + ∫₀^T e^{R(T−t)}Z_t·dW_t, and by the
   martingale representation of e^{−RT}g, g = e^{RT}u₀ + ∫e^{R(T−t)}Z*_t·dW_t. Then Y_T − g = e^{RT}(y₀ − u₀) +
   ∫e^{R(T−t)}(Z − Z*)·dW. For adapted, square-integrable Z the integral has mean zero, so the cross term vanishes, and
   Itô's isometry gives E|Y_T − g|² = e^{2RT}(y₀ − u₀)² + E∫e^{2R(T−t)}|Z − Z*|²dt.
10. **(qual) The floor.** By problem 9 the loss is at least E∫e^{2R(T−t)}|Z − Z*|² ≥ min over step processes of
   E∫|Z − Z*|²; on each step the best constant is the conditional mean Z̄_i = E[(1/h)∫_{t_i}^{t_{i+1}}Z*dt | F_{t_i}], and
   Σ_iE∫_{t_i}^{t_{i+1}}|Z*_t − Z̄_i|²dt ≤ Σ_i∫E|Z*_t − Z*_{t_i}|²dt ≤ Σ_i C h² = C T h if E|Z*_t − Z*_s|² ≤ C|t − s|
   (Zhang 2004 shows this L²-regularity for Lipschitz data): the floor is O(1/N).

## For the researcher

* **The theorems.** Han, Jentzen and E (2018), *PNAS* 115; Han and Long (2020), "Convergence of the deep BSDE method for
  coupled FBSDEs," *Probab. Uncertain. Quant. Risk* 5:5 (Theorem 1, the a posteriori estimate); Zhang (2004), "A
  numerical scheme for BSDEs," *Ann. Appl. Probab.* 14, for the L²-regularity of Z.
* **Simplifications.** The linear case for the exact identity; batch losses averaged over 500 iterations; one seed per
  step count, started from different initial y₀; the nonlinear band uses C = 1, which is not a theorem.
* **Open problems.** Sharper certificates that separate price and hedge; why training reaches small losses; computable
  constants for validation.

## Data and reproducibility

* Deribit BTC option surfaces of Part 13 (Wednesdays 2024–2025); Binance BTCUSDT daily closes (Aug 2017 – Dec 2025).
* The rough Bergomi training set: 12,000 parameter sets × 80 points, 10,000 paths each, one step a day; parameter box
  H ∈ [0.02, 0.5], η ∈ [0.3, 4], ρ ∈ [−0.9, 0.6], vol ∈ [25%, 120%].
* References checked against the sources: HJE (2018) 57.300 by multilevel Picard; BCJ (2019) Table 1; HLP (1994);
  Part 16's Longstaff–Schwartz on the same max-call, read from its cache; the Risk.net reports (J.P. Morgan's
  data-driven hedging of vanilla index books since 2018, a large share of its Euro Stoxx vanilla book priced with deep
  hedging, the extension to cliquets); SR 26-2 (Federal Reserve, 17 April 2026); PRA SS1/23; the arXiv abstracts of
  the 2023–2026 papers.
* No strategy was tested; the trial counter is unchanged at 310.

---

# 量化金融，从零搭建 — 第17部分：深度定价与对冲

本部分讲：

* 从价格中学习定价公式（Hutchinson、Lo与Poggio，1994），用它对冲，以及网络的希腊字母；
* 粗糙Bergomi的神经网络校准器（Horvath、Muguruza与Tomas，2021）：学习映射、标签噪声、通过网络校准，以及两年的周度曲面；
* 差分机器学习（Huge与Savine，2020），以及它的经典孪生方法：带梯度观测的高斯过程；
* 高维：深度BSDE求解器（E、Han与Jentzen，2017；Han、Jentzen与E，2018）和深度最优停时（Becker、Cheridito与Jentzen，2019）；
* 深度对冲器（Buehler、Gonon、Teichmann与Wood，2019）：无差异价格、熵风险与条件风险价值、漂移陷阱，以及它学会在哪里不交易
  （Leland 1985；Whalley与Wilmott 1997；Imaki等 2021）；
* 神经SDE与奇异期权的稳健界（Gierjatowicz等，2022）；
* 用第1部分的典型事实评判的市场生成器，以及跨生成器检验的对冲器；
* 投产与模型风险（2026年4月17日的SR 26-2取代SR 11-7；英国PRA SS1/23）、已经进入交易台的应用，以及2023–2026年的前沿。

所有网络都在一台共享CPU上训练，多数训练了不止一次（多个种子），并保存检查点，以便在屏幕上回放训练过程；投产版本会以完整规模重新训练。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约64分钟）

* **一台会对冲的机器。** 在0.5%成本下，网络在Delta周围学出一条走廊：它需要3.01，而每日Delta对冲需要3.55；在一个模拟月份里它只在30天中的11天交易；据Risk.net报道，摩根大通自2018年起用数据驱动的引擎对冲指数期权账本；历史条（1985–2026）；本部分安排。
* **1. 学习一个定价公式。** 重做Hutchinson、Lo与Poggio（1994）：默顿齐次性、万能逼近定理；一个3 × 64的网络在66,150个模拟价格上训练（最大误差为行权价的0.05%），它的Delta对冲200个新期权，与真实Delta一样好（跟踪误差0.214–0.217，对0.209）；**实验**：`train_mlp_regressor`。
* **2. 网络的希腊字母。** ReLU网络的二阶导数几乎处处为零：它的gamma误差是SiLU的12倍；网络给出的蝶式价差，ReLU有13%为负，SiLU为4%，softplus从不为负（Breeden–Litzenberger）。
* **3. 神经网络校准器：学习映射。** 12,000组粗糙Bergomi参数、894,903个蒙特卡洛标签、4 × 96网络训练40轮；标签噪声为留出集误差设了下限，与新模拟之差把它夸大了√1.5倍。
* **4. 通过网络来校准。** 用tanh映射进训练框，以及它在边界处消失的梯度；12个起点的Adam与L-BFGS在2.8秒内把曲面拟合到0.97个波动率点（H = 0.074，η = 1.89，ρ = −0.40），而用模拟要几个小时；**实验**：`calibrate_neural`。
* **5. 逐周的粗糙波动率。** 100个周度曲面：77次校准停在训练框的下限H = 0.02，每次蒙特卡洛复核都在半个波动率点之内；框内的最优点不是市场的H。
* **6. 差分机器学习。** 用路径导数作标签（Huge与Savine，2020），由控制收敛定理保证无偏：256个样本时价格误差从3.69–5.28降到0.43–0.81，Delta平均精确22倍；**实验**：孪生损失。
* **7. 三维中的导数标签。** 64个收益上的切平面；带梯度的高斯过程（Dixon、Halperin与Bilokon，第3章）是精确的孪生方法：网格误差45.4 / 6.6 / 3.5（只用收益、加斜率、高斯过程），以及它的三次方成本。
* **8. 一百维：深度BSDE。** 伊藤公式与非线性费曼-卡茨公式（Pardoux–Peng，1990）；Han、Jentzen与E挂钩100个资产、带违约风险的衍生品；从猜测的u₀出发用39个小网络打靶；维数灾难对多项式工作量；深度Galerkin与多层Picard。
* **9. 看深度BSDE收敛。** 256条测试路径落在各自的收益上；57.35 ± 0.05，对参考值57.300（+0.08%）；无违约的线性检验比普通蒙特卡洛低4.04；**实验**：前向扫描。
* **10. 深度最优停时。** Becker、Cheridito与Jentzen（2019）：bang-bang决策，每个日期一个网络；五资产百慕大最大值看涨期权26.107 ± 0.040，对Longstaff–Schwartz的26.103 ± 0.028和已发表的[26.156, 26.162]；两资产13.886，对二叉树13.902；三维中的行权隧道。
* **11. 深度对冲器。** Buehler、Gonon、Teichmann与Wood（2019）：熵风险、现金不变性、无差异价格；无成本时网络收敛到Delta（价格2.360对2.355，持仓相差不超过0.095股）；**实验**：`hedge_pnl`。
* **12. 风险度量与漂移陷阱。** 用Rockafellar–Uryasev公式求CVaR（学到的w = 2.819，经验VaR为2.818）；在30%的漂移下，对冲者加上默顿项μ/γσ²S，即对漂移的押注（带漂移训练的对冲者定价2.292，对2.385）；QLBS、强化学习对冲与深度Bellman对冲。
* **13. 何时不交易。** 交易图中打开的无交易区间；推导Leland（1985：0.5%成本下σ̂ = 26.5%）与Whalley–Wilmott的立方根区间（1997）；0.5%成本下：每日Delta 3.55，Leland 3.37，Whalley–Wilmott 3.08，区间网络3.01。
* **14. 作为曲面的无交易区间。** 学到的区间在时间与价格上的两张曲面，对Whalley–Wilmott的（平值处宽度30天0.22、5天0.28；他们的0.31与0.58）；Imaki等的架构与Davis、Panas与Zariphopoulou（1993）；成本加倍时区间变宽1.17倍，而2^{1/3} = 1.26；**实验**：`Hedger.band`。
* **15. 神经SDE与稳健界。** Gierjatowicz等（2022）：36个普通期权都重新定价到0.19个波动率点之内，而一个向下敲出看涨期权的价格可在0.0671到0.0703之间（赫斯顿为0.0685）；两个极端模型的微笑相差从未超过0.72个波动率点；这些界嵌在第9部分的鞅最优传输界之内。
* **16. 市场生成器。** GJR-GARCH、用签名训练的网络和扩散模型生成32天的比特币窗口，按典型事实和期望签名距离评分；四个真实窗口与四个生成窗口。
* **17. 投产与模型风险。** 2026年4月17日的SR 26-2取代SR 11-7，英国PRA SS1/23；把清单用于本部分的网络；已知答案记分板；公司档案（摩根大通、丹斯克银行）。
* **18. 前沿：2023至2026年。** 生成式期权市场（SANOS、DYSANOS、GROMM）、深度对冲者是否在对冲、二阶训练、停时与对偶、签名核生成器；重跑一个论断。
* **19. 检验第17条规则。** 四个对冲者分别在Black–Scholes路径、GJR-GARCH路径和1,010段真实的30天比特币区间上定价；第17条规则（没有更慢的独立引擎就不用网络；训练框外的输入交给它；对冲者要在两个生成器和历史上检验）。
* **写给研究者：深度BSDE的损失作为误差证书。** 线性情形（无违约）下Y_T − g = e^{RT}(y₀ − u₀) + ∫e^{R(T−t)}(Z − Z*)·dW，由伊藤等距，损失等于e^{2RT}(y₀ − u₀)²加上对冲的误差，所以|y₀ − u₀| ≤ e^{−RT}√损失；Han与Long（2020）对利普希茨驱动项证明sup E|Y − Ŷ|² + E∫|Z − Ẑ|² ≤ C(h + 损失)。十维篮子最小值（200万条路径得参考值72.548 ± 0.006），N = 5/10/20/40步各训练3,000次：误差从不越过界；最终损失17.4/12.2/9.3/9.6，界4.09/3.42/2.98/3.03，实际误差0.004/0.016/0.044/0.138（宽松20–1,000倍：损失主要是对冲的方差）；下限随h下降，然后网络自身的误差接管。第9章的一百维违约风险运行：y₀ → 57.3，位于y₀ ± √损失之内（示意，常数未知）。三个开放问题；暂停题：R = 2%、T = 1时损失9给出价格误差上界e^{−0.02} × 3 = 2.94；用真实对冲时损失会缩小到e^{2RT}(y₀ − u₀)²加上时间步长下限。
* **回顾、交易台问题、十道习题（两道为资格考试水平）。** 十一行回顾；四个交易台问题；解答见下文。

## 交易台问题与解答

1. **你的对冲器有成本。为什么最优对冲有一个区间？**
   * 持有δ而不是无摩擦的Δ，单位时间的对冲方差约为(δ − Δ)²σ²S²：风险随偏差的平方增长。
   * 交易回去的成本是c|δ − Δ|S，与偏差成线性关系。
   * 在Δ附近，平方的风险小于线性的成本，所以值得等到偏差足够大。两者平衡给出半宽度(3cSΓ²/2γ)^{1/3}的区间（Whalley–Wilmott），在Gamma大的地方最宽。
   * 深度对冲器不借助渐近分析就学到了同样的原理（第13–14章）。
2. **神经网络校准器把曲面拟合得很漂亮。怎么知道它是对的？**
   * 用慢速引擎（新的蒙特卡洛）在校准参数下重新定价并比较误差。
   * 检查每个输入都在训练范围内：第5章里，H顶在了训练框的下限，那里双曲正切映射的梯度消失（第4章）。
   * 知道网络相对新模拟的误差，并把它与自身标签的噪声区分开（第3章）。
   * 网络外推时不会发出警告，所以这些检查是模型的一部分，而不是附加项。
3. **你有一千个模拟收益。为什么还要记录它们的导数？**
   * 用伴随微分，每个样本的路径导数只需约一次额外定价，每个样本多出d个标签；对利普希茨收益，它们是Delta的无偏估计。
   * 它们确定了样本之间函数的形状：价格，尤其是希腊字母，所需样本少得多。
   * 数字期权例外：它的路径导数几乎处处为零（改用似然比标签或光滑化）。
4. **你的深度对冲器在没有成本时平均能赚钱。它是在对冲吗？**
   * 部分是在投机。在漂移μ下，指数效用的对冲是Δ + μ/(γσ²S)：复制对冲之上叠加了默顿的投资组合（第12章）。
   * 在无漂移路径上把它的持仓与Delta比较并定价；在那里它比无漂移训练的对冲器需要更多。
   * 在（近似）鞅测度下训练（Buehler等，2021），或使用对不利结果赋予足够权重的风险度量（François等，2024），除非漂移是你有意持有的观点。

## 习题与解答

1. **无差异价格。** ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c，所以熵风险具有现金不变性。没有权益且股票为鞅时，不交易是最优的，最小风险为0；有权益时，卖方在ρ(−Z + 对冲 − 成本 + p) = 0时无差异，即p = min_δ ρ(−Z + (δ·S)_T − C_T)。
2. **区间的标度。** 在dt时间内，偏差ε的确定性等价成本为(γ/2)ε²σ²S²dt；把偏差保持在±h内，约需交易(σ²S²Γ²/h)dt股，每股成本cS；区间内E ε² = h²/3。对h最小化γh²σ²S²/6 + cSσ²S²Γ²/h，得h³ = 3cSΓ²/2γ。
3. **求解器背后的BSDE。** 由伊藤公式，dY = (u_t + 𝓛u)dt + ∇uᵀσ(X)dW；偏微分方程给出u_t + 𝓛u = (1 − δ)Q(u)u + Ru = f(Y)，所以dY = f(Y)dt + Z·dW，Z = σ(X)ᵀ∇u，Y_T = min_i X_T^i。
4. **差分回归。** 设特征Φ（n × p）及其对输入的梯度∇Φ，最小化‖Φw − y‖² + λ‖∇Φw − ∂y‖²；正规方程为(ΦᵀΦ + λ∇Φᵀ∇Φ)w = Φᵀy + λ∇Φᵀ∂y。
5. **深度停时的下界。** 给定X_n，目标g_nF + E[G_{n+1}|X_n](1 − F)对F是线性的，在F = 1{g_n ≥ E[G_{n+1}|X_n]}处取最大；任何{0,1}规则都定义一个停时τ，而E[g_τ] ≤ sup_τ E[g_τ]，即百慕大期权的价格。
6. **利兰的波动率。** 两次再平衡之间ΔΔ ≈ ΓΔS，所以E|ΔΔ|S = ΓS²σ√Δt √(2/π)；单位时间成本为(k/2)ΓS²σ√(2/π)/√Δt，往返成本k = 2c。把它加到卖出期权定价方程中的½σ²S²Γ项上，得½σ̂²S²Γ，σ̂² = σ²(1 + √(2/π) k/(σ√Δt))。
7. **默顿项。** 在零利率的完备市场中，带权益的终值财富为−Z + (δ·S)_T。令δ = Δ + η：Δ部分精确复制Z，剩下max E[−e^{−γ(x − p + (η·S)_T)}]，即没有权益的CARA问题，其解持有金额μ/(γσ²)，即η = μ/(γσ²S)。
8. **标签噪声。** 若y = F + ε且ε独立于网络的预测F̂，则E(F̂ − y)² = E(F̂ − F)² + Eε² ≥ Eε²。标签方差加倍会抬高这个下限，但对每个θ附近许多标签的光滑拟合会平均掉它们的噪声，所以网络自身的误差E(F̂ − F)²增长远小于标签的方差。
9. **（资格考试）损失的分解。** 解线性SDE：Y_T = e^{RT}y₀ + ∫₀^T e^{R(T−t)}Z_t·dW_t；由e^{−RT}g的鞅表示，g = e^{RT}u₀ + ∫e^{R(T−t)}Z*_t·dW_t。于是Y_T − g = e^{RT}(y₀ − u₀) + ∫e^{R(T−t)}(Z − Z*)·dW。对适应、平方可积的Z，积分均值为零，交叉项消失，伊藤等距给出E|Y_T − g|² = e^{2RT}(y₀ − u₀)² + E∫e^{2R(T−t)}|Z − Z*|²dt。
10. **（资格考试）下限。** 由第9题，损失至少为在阶梯过程上取最小的E∫|Z − Z*|²；每步上最好的常数是条件均值Z̄_i，且若E|Z*_t − Z*_s|² ≤ C|t − s|（Zhang 2004对利普希茨数据证明了这种L²正则性），Σ_iE∫|Z*_t − Z̄_i|²dt ≤ C T h：下限为O(1/N)。

## 写给研究者

* **定理。** Han、Jentzen与E（2018），*PNAS* 115；Han与Long（2020），*Probab. Uncertain. Quant. Risk* 5:5（定理1，后验估计）；Zhang（2004），*Ann. Appl. Probab.* 14，论Z的L²正则性。
* **简化。** 精确恒等式只对线性情形；批损失在500次迭代上平均；每种步数一个种子，从不同的初始y₀出发；非线性的带取C = 1，这不是定理。
* **开放问题。** 把价格与对冲分开的更紧证书；训练为何能达到小损失；可用于验证的可计算常数。
