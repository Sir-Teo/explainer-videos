# Plan: Part 9, *No Arbitrage*, expanded from 21 to about 57 minutes

Scope: research and planning only; nothing in the repo was edited. Sources read: `videos/quant/SYLLABUS.md` §1
(including the Revision of November 2026 and the "Hands-on, as in *AI, Built*" bullet), §6 Part 9; `READING.md` §1–2
and §4 Part 9; every file in `videos/quant/quant9/`; `explainer/quant/house/{arbitrage,surface,smile,trees}.py`;
`explainer/quant/{__init__,viz,data}.py`; `explainer/ai/viz.py`; `videos/ai/LECTURE_GUIDE.md`;
`videos/ai/ai21/s12_reflow.py` (`replay`, `measure`); `videos/quant/quant10/s06_greeks.py` (the 3D bar in this series).
Numbers marked **probe** were computed during planning with the House's own code (scratch scripts, not committed).
Length rule used: `tools/lecture_length.py` counts narration at 140 words/min, so 3.0 min ≈ 420 words.

---

## 1. Current state (`lecture_length.py quant9`: 20.8 min, 10 scenes)

| # | Scene (min, words) | What it covers | Depth |
|---|---|---|---|
| — | Hook "One price" (2.9, 406) | desk question C=10, P=7, K=100, S=103; Deribit inverse parity C−P = 1−K/F; 339 call–put pairs, median 3.4 bp (trades), 1.5 bp (marks), p90 9.9 bp; implied basis 2.8%→4.8%/yr; objectives; House chart | real computed experiment (`parity`); dots plot, static |
| 1 | Parity (2.8, 388) | definition of arbitrage; parity with borrow fee h; ORW 2004 (one sentence); GameStop crisis card (SEC staff report); box spread, Robinhood 2019 | ladders only; no derivation of parity itself, no visual of payoffs |
| 2 | FTAP (2.3, 322) | 2-D cone of payoff arrows (bond, stock 80/100/125); price 130 outside cone; LP returns θ = (+1.79, −0.0143); state prices, SDF m=ψ/π, Q=(1+r)ψ | the signature picture exists but is 2-D, static, and the theorem is asserted, not proved |
| 3 | Tree (1.7, 241) | CRR 4-step call 9.35, nodes fade in back to front; incompleteness: interval [0, 0.197] constant for 3–33 states, BS 0.080 inside | fold-back is node fade, no hedge, no derivation of q; LP stated, not solved on screen |
| 4 | Continuous (1.9, 268) | four history cards (HK 79, HP 81, DMW 90, DS 94); numeraire ladder (GEKR 95, T-forward, Bitcoin numeraire) | cards only; no Girsanov, no NFLVR content, no numeraire derivation |
| 5 | Density (1.9, 273) | BL formula; SVI fits of 26 Dec (16 d) and 27 Mar (107 d); Q(down 20%) 2.9% / 19.1%, Q(up 20%) 1.8% / 18.4%; checks pass | real computed result; one derivative step; no butterflies, no fit shown |
| 6 | Ross (1.7, 242) | P = πm, m = δφ(j)/φ(i), Perron–Frobenius; 9-state economy recovered to 1e−15; with "permanent" tilt error 0.051, long-run −2.5% vs +2.0% | synthetic experiment; heatmaps static |
| 7 | MOT (1.9, 260) | the LP stated; forward-start straddle in [0.137, 0.218] vs log-normal 0.180 (fwd vol 45%); two optimal couplings | real computed; the LP is a black box; no dual, no hedge |
| 8 | House (0.8, 112) | checker function table; Rule 10; trial counter 72 | — |
| — | Outro (2.8, 398) | recap, three desk questions, five problems, references | — |

Verdict: every syllabus item is touched, but eight of ten are thin (one ladder or one static plot each); there is no
industry chapter, no frontier chapter, no lab (`code_block`) moment, no replay of anything solved, and no 3D.

## 2. Audit

### (a) Syllabus items

| Item | Status now | Where it goes |
|---|---|---|
| 1 Arbitrage, LOOP, parity, practical failures | thin (no parity proof, no payoff visual; GameStop card good) | ch 1–2, plus industry ch 17 |
| 2 One-period FTAP by Farkas, proved | thin (picture yes, proof only in README problem 2) | ch 3–4 |
| 3 State prices, SDF, Q | thin (one ladder) | ch 5 |
| 4 CRR | thin (fold-back without hedge or derivation) | ch 6 |
| 5 Completeness; super-replication LP | thin (interval plot; LP not solved on screen) | ch 7–8 |
| 6 HK, HP, DS | thin (history cards only) | ch 9–10 |
| 7 Numeraire; forward and annuity measures | thin (ladder) | ch 11 |
| 8 Breeden–Litzenberger | covered once, thinly | ch 12–13 |
| 9 Ross recovery and BHS critique | covered, synthetic only | ch 14 |
| 10 MOT bounds by LP | covered thinly (no dual/hedge) | ch 15–16 |

### (b) Textbook core sections → chapter

**Correction found:** `READING.md`/`SYLLABUS.md` cite "Björk ch. 1–3, 10, 26". In the **4th edition (2020)**, which
READING.md names, ch. 10 is *Parity Relations and Delta Hedging*, ch. 11 *The Martingale Approach to Arbitrage
Theory*, ch. 15 *Change of Numeraire*, and ch. 26 *Optimal Consumption and Investment* (OUP table of contents,
https://academic.oup.com/book/43511). The old numbers fit an earlier edition. The revised entry below uses 4th-edition
numbers.

| Book, section | Chapter here |
|---|---|
| Shreve I ch. 1 (one-period and multiperiod binomial no-arbitrage model, computational considerations) | 6 |
| Shreve I ch. 3 (state prices: change of measure, Radon–Nikodým process, the utility-maximization link) | 5, 9 |
| Shreve I ch. 4 (American derivatives) | 6 (one beat), full in Parts 8/10 |
| Shreve I ch. 6 (interest-rate assets, forward measure in the binomial model) | 11 (one beat), full in Part 19 |
| Shreve II ch. 5 (risk-neutral pricing, Girsanov, martingale representation, two FTAPs) | 9 |
| Shreve II ch. 9 (change of numéraire) | 11 |
| Björk ch. 2 Binomial model; ch. 3 A more general one-period model (no arbitrage, martingale measures, completeness, SDF) | 3–8 |
| Björk ch. 9 A primer on incomplete markets | 7–8 |
| Björk ch. 10 Parity relations and delta hedging | 1 |
| Björk ch. 11–12 The martingale approach; its mathematics | 9–10 |
| Björk ch. 15 Change of numeraire | 11 |
| Björk ch. 29, 34 Incomplete markets; good-deal bounds | 8 (named, one beat); good-deal bounds left to Part 13 |
| Duffie DAPT ch. 1 A Arbitrage and state prices, B Risk-neutral probabilities (verified); C–F optimality, complete markets, representative agent, state-price beta (titles from memory) | 3–5; equilibrium sections → Part 23 |
| Duffie ch. 2 Multiperiod model: arbitrage, state prices and martingales; redundant securities; American exercise (from memory) | 6, 9 |
| Duffie ch. 6 State prices and equivalent martingale measures: arbitrage, numeraire invariance, doubling strategies, Girsanov and market prices of risk, complete markets (section list from memory) | 9–11 |
| Delbaen–Schachermayer ch. 1 The story in a nutshell; ch. 2 finite Ω (FTAP, change of numéraire, Kramkov's optional decomposition) | 3–4, 8, 11 |
| D–S ch. 5 Kreps–Yan; ch. 6 Dalang–Morton–Willinger; ch. 8 continuous-time overview (NFLVR, admissibility, σ-martingales) (from memory) | 10 |
| Föllmer–Schied ch. 1.1–1.6 (arbitrage, martingale measures, derivative securities, completeness, geometric characterization) (from memory) | 3–5, 7 |
| Föllmer–Schied ch. 5 dynamic arbitrage, binomial model, convergence to BS; ch. 7 superhedging (uniform Doob decomposition, superhedging with liquid options) (from memory) | 6, 8, 15 |
| Henry-Labordère *Model-free Hedging* (Routledge lists: *Pricing and hedging without tears*; *Martingale optimal transport*; *Model-independent options*; *Continuous-time MOT and Skorokhod embedding*) | 15–16, 18 |
| Hull OFOD *Binomial trees*; *Martingales and measures* (coverage map → 9) | 6, 11 |
| Cochrane *Asset Pricing* Part I (contingent claims, SDF) | 5 (full in Part 23) |

### (c) READING.md papers for Part 9

| Paper | Now | Plan |
|---|---|---|
| Arrow 1964; Debreu 1959 | mentioned (ladder) | on screen ch 5 (history card + Arrow security bars) |
| Stoll 1969 | on screen (hook) | ch 1 |
| Ross 1978 | mentioned | on screen ch 5 (linear pricing ⇒ state prices) |
| Breeden–Litzenberger 1978 | on screen | ch 12 |
| Cox–Ross–Rubinstein 1979 | on screen | ch 6 |
| Harrison–Kreps 1979 | on screen (card) | ch 4 theorem card, ch 9 |
| Harrison–Pliska 1981 | on screen (card) | ch 9 (both FTAPs) |
| Dalang–Morton–Willinger 1990 | card | ch 10 |
| Delbaen–Schachermayer 1994 | card | ch 10, definition card NFLVR |
| Geman–El Karoui–Rochet 1995 | ladder | ch 11 theorem card |
| Hobson 1998 | mentioned | ch 15 (lookback/Azéma–Yor picture, one beat) |
| Ofek–Richardson–Whitelaw 2004 | mentioned | ch 2 on screen, ch 17 |
| Beiglböck–Henry-Labordère–Penkner 2013 | mentioned | ch 15 duality theorem card |
| **Galichon–Henry-Labordère–Touzi 2014** | **absent** | ch 15: the dual as stochastic control (continuous-time MOT) |
| Ross 2015 | on screen | ch 14 |
| Borovička–Hansen–Scheinkman 2016 | on screen | ch 14 |

## 3. The final chapter list (20 scenes, ≈57 min)

Conventions for every chapter: chapter card; definition/theorem cards from `explainer/ai/lecture.py`; derivations by
`ladder` with `why`; Q-objects in `C.Q`/`Q_C`, P-objects in `C.P`; every number from `compute.py`; narration branches on
computed verdicts. "Lab" = `code_block` (≤12 lines of the House's real function) then run, output appearing live.
"Replay" = `ValueTracker` scrub of iterations with the objective drawn alongside (the `TrainingReplay` class in
`explainer/quant/viz.py`, or the `replay` pattern of ai21 s12). Words are narration targets.

### 00 · Hook: One price, and how we got here (2.5 min, 350 w) — `s01_hook.py`, keep and extend
Keep the desk question and Deribit parity dots. Add the era strip (timeline 1900–2030, ideas gold): 1902 Farkas, 1964
Arrow, 1969 Stoll, 1973 BSM, 1976–79 Ross/CRR/Harrison–Kreps, 1981 Harrison–Pliska, 1994 Delbaen–Schachermayer, 1998
Hobson/LTCM (red), 2013 BHP, 2015 Ross recovery, 2021 GameStop (red). Objectives card rewritten to the ten items.
Pause: "Before the answer: is C − P = S − K enough, or do you need the put's price too?"

### 01 · Parity, assembled on screen (3.0 min, 420 w) — item 1 — new `s02_parity.py` (split)
- **Goal:** prove parity by replication and see the arbitrage lock in.
- **Beats:** definition card (arbitrage: cost ≤ 0, payoff ≥ 0, P(payoff>0)>0; LOOP as its corollary) → build long
  call and short put payoff diagrams; they add, kink cancels, to the straight forward line → parity → the mispriced
  put (6): assemble the four legs one by one; a fan of 200 simulated S_T values each lands on P&L = +1 → Björk ch. 10
  bounds (C ≥ S − Ke^{−rT}, C ≤ S) as the band the call curve must live in → Deribit lab.
- **Derivation:** $(S_T-K)^+-(K-S_T)^+=S_T-K$ (case split at $K$); price of RHS $=S-Ke^{-rT}$ (buy stock, borrow PV(K));
  LOOP ⇒ $C-P=S-Ke^{-rT}$; inverse options: $\tilde C=C/F$, divide by $F$: $\tilde C-\tilde P=1-K/F$ (BTC numeraire,
  forward link to ch 11); $F=K/(1-(\tilde C-\tilde P))$.
- **Signature visual:** two hockey sticks sliding together and fusing into one straight line; then the arbitrage
  ledger: each leg's payoff line stacks, the stack flattens to a horizontal line at +1, and the dots of 200 simulated
  outcomes drop onto it. The flattening *is* the idea: no state of the world remains in the payoff.
- **Lab 1:** `arbitrage.implied_forward(trades, window=600)` (move the pairing loop now in `compute_parity` into the
  House, ≤12 lines: group by (expiry, K), nearest put within 600 s, F = K/(1 − (C−P))), run on 10 Dec 2025: counter
  ticks to 339 pairs, dots appear per expiry.
- **Experiment (new, `futures_basis`, ~3 min fetch+compute):** Deribit **futures** trades, same hours
  (`deribit_trades(DAY, hours, kind="future")`; verified the history API serves them, e.g. BTC-30JAN26 traded 93,355.0
  with index 92,789.33 at 00:00:11 UTC). Compare each dated future's F/index with the options-implied F per expiry.
  Expected: agreement within a few bp of price (probe spot check: futures 4.3%/yr vs options 4.5%/yr at 51 days,
  ≈2.8 bp of price); narration branches on the measured median gap.
- **Pause:** "If the put were 8, which legs flip?" (all four.)

### 02 · Where parity breaks: borrow, carve-outs, GameStop (3.0 min, 420 w) — item 1
- **Goal:** parity's assumptions (shorting, European exercise, funding) and what violations price.
- **Beats:** borrow fee h as a dividend → ORW 2004 (violations concentrate where shorting is costly) → Palm/3Com
  (2 March 2000): Palm closed $95.06; 3Com, holding 1.5 Palm per share, closed $81.81 ⇒ stub −$60.78 per 3Com share,
  about −$22 bn in aggregate; Palm short interest peaked at 147.6% of float; Palm puts were roughly twice the price
  parity implied; on 16 March 2000 the synthetic short (via options) was about $39.12 against $55.25 for the stock
  (Lamont–Thaler; Chicago Booth Review) → GameStop crisis card (kept) → American box, Robinhood 2019 (kept, short).
- **Derivation:** lending a share earns h: $1$ share at 0 → $e^{hT}$ at T; portfolio A = call + $Ke^{-rT}$, B = put +
  $e^{-hT}$ shares lent ⇒ both pay $\max(S_T,K)$ ⇒ $C-P=Se^{-hT}-Ke^{-rT}$; invert:
  $h=-\tfrac1T\ln\frac{C-P+Ke^{-rT}}{S}$ (reason: "read parity backwards").
- **Signature visual:** a slider for h; the forward line drops, the put's price bar grows, the synthetic-short price
  marker moves off the stock price; for Palm the gap opens to $55.25 → $39.12 and is labelled "the price of
  borrowing". Then the 3Com bar split into "1.5 Palm" (taller than 3Com itself) and a negative stub bar below zero.
- **Experiment:** no new data. On screen: the published Palm gap ($55.25 stock vs $39.12 synthetic, 16 March 2000)
  and the 3Com stub arithmetic 81.81 − 1.5 × 95.06 = −60.78. An implied annual borrow fee needs the options' maturity
  from Lamont–Thaler's table; compute it only once that is checked against the paper, otherwise show the gap alone.
  Computed companion: the cached Deribit parity residuals (`parity`) as the "liquid, easy-to-borrow" contrast:
  median 3.4 bp.
- **Pause:** "The stub is negative. Why didn't everyone buy 3Com and short Palm?" (borrow scarce/recalled; 30% of
  negative-stub cases end with the link severed, Mitchell–Pulvino–Stafford 2002.)

### 03 · The geometry of arbitrage, in 3D (3.0 min, 420 w) — item 2 — new `s04_geometry.py` (`ThreeDScene`)
- **Goal:** see "no arbitrage" as a subspace missing an orthant.
- **Beats:** three states ⇒ payoffs live in ℝ³; the positive orthant = "never lose, sometimes win" → the market's
  zero-cost payoffs (bond + stock, θ·p = 0) form a line through the origin → no arbitrage ⇔ that line meets the
  orthant only at 0 → raise the stock's price from 100 to 130: the line rotates and pierces the orthant; the piercing
  point is the arbitrage payoff (0.64, 0.36, 0) → the separating plane through the line with normal ψ.
- **Derivation (setting):** $D\in\mathbb R^{2\times3}$, $p\in\mathbb R^2$; zero-cost set $Z=\{D^\top\theta:\theta\cdot
  p=0\}$; arbitrage ⇔ $Z\cap(\mathbb R^3_+\setminus\{0\})\neq\emptyset$ (definition); plane $\psi^\perp\supset Z$ with
  $\psi>0$ ⇔ $\psi\cdot D^\top\theta=0$ whenever $\theta\cdot p=0$ ⇔ $D\psi\parallel p$ (orthogonal complements) ⇒
  normalize: $D\psi=p$.
- **Signature visual:** camera orbiting ℝ³ (axes "pays in state 1/2/3"), translucent orthant, the zero-cost line in red;
  a ValueTracker on the stock price rotates the line; a translucent plane pivots about the line keeping the orthant on
  one side, its normal arrow ψ drawn and labelled with live components; as the price nears 125 one component of ψ
  shrinks to 0 (the plane lies on a face); past it no plane exists and the line enters the orthant (glow). The plane's
  normal is literally the state-price vector: the viewer sees why positivity of ψ and separation are the same thing.
- **Experiment:** ψ(p) for stock prices 81…124 (max-min ψ from `ftap`), min ψ → 0 at both ends (probe at 100:
  ψ = (0.385, 0.308, 0.308)).
- **Pause:** "At a stock price of exactly 125, is there an arbitrage?" (Yes: short one share, buy 125 bonds; cost 0,
  payoff 125 − S = (45, 25, 0): never negative, sometimes positive. The line touches the orthant's face; ψ₃ = 0.)

### 04 · The fundamental theorem, proved and solved (3.0 min, 420 w) — item 2 — `s03_ftap.py` rewritten
- **Goal:** prove FTAP-1 (finite Ω) and watch an LP decide it.
- **Beats:** theorem card (Harrison–Kreps 1979; Farkas 1902; Stiemke 1915) → proof (easy direction, then Stiemke via
  separation of a subspace and a compact convex set) → the LP formulation → Lab 2: the House's teaching simplex runs.
- **Derivation:** (⇐) $p=D\psi$, $\psi>0$, $D^\top\theta\ge0$, $\neq0$ ⇒ $\theta\cdot p=\psi\cdot D^\top\theta>0$ (inner
  product of positive vectors) — no arbitrage. (⇒) $L=\{(-\theta\cdot p,\,D^\top\theta)\}\subset\mathbb R^{1+m}$ linear;
  NA ⇔ $L\cap\mathbb R^{1+m}_+=\{0\}$; $K=\{x\ge0,\ \sum x=1\}$ compact convex, disjoint from $L$ ⇒ strict separation:
  $\exists\lambda$: $\lambda\cdot x>0\ \forall x\in K$ and $\lambda\cdot\ell=0\ \forall\ell\in L$ (hyperplane
  separation; a linear functional bounded on a subspace vanishes on it) ⇒ $\lambda\gg0$ (take $x=e_j$) ⇒
  $-\lambda_0\theta\cdot p+\sum_j\lambda_j(D^\top\theta)_j=0\ \forall\theta$ ⇒ $p=D\psi$, $\psi=\lambda_{1:m}/\lambda_0$.
  LP: $\max t$ s.t. $D\psi=p$, $\psi\ge t\mathbf 1$; NA ⇔ optimum $t^*>0$.
- **Signature visual:** the 2-D cone picture (kept from now) becomes the *dual* view of ch 3's 3-D picture: the same
  stock-price slider moves the price dot across the cone boundary while the 3-D inset rotates the line — two pictures
  of one fact, linked by colour.
- **Lab 2 + replay:** new `arbitrage.simplex(c, A_eq, b_eq, trace=True)` (dense tableau, Bland's rule, ≤12 lines on
  screen: pick entering column, ratio test, pivot, record vertex and objective), tested against HiGHS. Run on the FTAP
  LP at p = 100 and p = 130: the tableau pivots one by one (rows flash), objective t climbs to 0.308 at 100; at 130
  phase 1 ends infeasible and the dual ray (the arbitrage θ = (+1.79, −0.0143)) is read off.
- **Pause:** "How many states must you add before the LP can't find state prices for any price inside (80, 125)?"
  (Never: more states only widen the cone.)

### 05 · State prices, the SDF, and Q: one object in three units (3.0 min, 420 w) — item 3
- **Goal:** ψ, m and Q are one vector; Q is P reweighted.
- **Beats:** Arrow security card (Arrow 1964; Debreu 1959) → linear pricing ⇒ state prices (Ross 1978) → divide by π:
  the SDF → normalize: Q → the risk-neutral simplex: the triangle of all (q₁,q₂,q₃), the line of q pricing the stock,
  the segment inside = every EMM (endpoints (5/9, 0, 4/9) and (0, 1, 0) for the 80/100/125 stock at r = 0) → real data:
  the BTC pricing kernel.
- **Derivation:** $p=\sum_j\psi_jd_j$; $\pi_j>0$ ⇒ $p=\sum_j\pi_j(\psi_j/\pi_j)d_j=\mathbb E^P[md]$ (multiply and divide);
  bond: $\sum\psi_j=1/(1+r)$ (price of 1 in every state); $q_j=(1+r)\psi_j$ ⇒ $\sum q_j=1$, $p=\frac{1}{1+r}\mathbb E^Q[d]$;
  $\frac{dQ}{dP}=\frac{q_j}{\pi_j}=(1+r)m_j$ (the Radon–Nikodým derivative is the normalized SDF); $\mathbb
  E^P[m]=1/(1+r)$.
- **Signature visual:** three bar charts over the same states: P bars (blue) → each bar multiplied by its m (m bars
  grow tall in crash states) → bars renormalized to Q (gold); the morph P→Q is one animation, the bars in bad states
  growing. Then the simplex triangle with the EMM segment glowing; dragging the stock price slides the segment out of
  the triangle exactly when ch 3's line pierced the orthant.
- **Experiment (new `kernel`, ~3 min):** BTC empirical pricing kernel at the 16-day expiry: q from the Surface's SVI
  density; p from 16-day BTC log returns, Binance daily closes 2021-04 … 2025-11 (cached), Gaussian KDE, rescaled to
  the Surface's spot; m(s) = q(s)/p(s) with a 1000-draw stationary-bootstrap band (`econ.stationary_bootstrap`).
  Expected: m above 1 in the left tail; whether m is monotone or U-shaped (the "pricing kernel puzzle", Jackwerth 2000)
  is unknown until computed — narration branches; the band will be wide (≈110 non-overlapping windows), and the video
  says so. Label `P estimated from history`.
- **Pause:** "If Q-probabilities of a crash are higher than P's, which way does m tilt?"

### 06 · The tree: replication in one step, then folding back (3.5 min, 490 w) — item 4 — `s04_tree.py` rewritten
- **Goal:** derive q from replication; run a multi-step hedge that replicates exactly.
- **Beats:** one step: S = 100 → 120 or 80, call K = 100, r = 0 → find Δ, B → q falls out, no π used (CRR 1979) →
  N steps: the fold-back, node by node, with Δ at each node → run the hedge along a simulated path: the ledger ends
  exactly at the payoff → convergence to BS with N; the odd/even sawtooth → American put: one node where exercising
  wins (Shreve I.4; full in Part 10).
- **Derivation:** $\Delta Su+B e^{r\Delta t}=V_u$, $\Delta Sd+Be^{r\Delta t}=V_d$ (replicate both states) ⇒
  $\Delta=\frac{V_u-V_d}{S(u-d)}$ (subtract), $B=e^{-r\Delta t}\frac{uV_d-dV_u}{u-d}$ (substitute) ⇒ $V=\Delta S+B=
  e^{-r\Delta t}[qV_u+(1-q)V_d]$, $q=\frac{e^{r\Delta t}-d}{u-d}$ (collect terms); $0<q<1\iff d<e^{r\Delta t}<u$ (NA,
  ch 4). Example: Δ = 0.5, B = −40, V = 10, q = 0.5 (probe).
- **Signature visual:** one step as geometry: payoff points (80, 0) and (120, 20) in the (S, V) plane; the replicating
  portfolio is the straight line through them (slope Δ, intercept B), and its height at S = 100 is the price. Then
  the `BinomialTree` folding back: values flow leftward along edges with the Δ printed at each node; a path lights up
  and a `HedgeLedger`-style bar (cash, shares) rebalances at each node, landing on the payoff to the cent.
- **Lab 3:** `trees.crr` (the backward-induction loop, ≤10 lines) on screen, then run N = 1…500 live: price vs N
  drawn as it computes; probe values: N = 1: 12.44, 2: 8.82, 3: 10.79, 4: 9.35, 50: 9.898, 51: 9.996, 200: 9.935,
  201: 9.960 → BS 9.948 (K = 100, σ = 25%, T = 1, r = 0).
- **Experiment:** replication along 1,000 paths of the 4-step tree: max |hedge − payoff| = 0 to 1e−12 (exact).
- **Pause:** "Why does the price zigzag between odd and even N?" (the strike falls on a node for even N, between
  nodes for odd.)

### 07 · Incomplete markets: the interval, solved as a linear program (3.0 min, 420 w) — item 5
- **Goal:** super- and sub-replication as dual LPs; the second fundamental theorem.
- **Beats:** add a third state (80/100/125): no line through three points → super-replication = cheapest line *above*
  the three payoff points; sub-replication = richest line below → the LP in the (B, Δ) plane solved graphically →
  duality: the same numbers as max/min of E^Q over the EMM segment of ch 5 → theorem card: complete ⇔ Q unique
  (Harrison–Pliska 1981, second FTAP) → the interval is (0, 100/9) and open.
- **Derivation:** $\bar p=\min_{B,\Delta}\{B+100\Delta: B+\Delta s_j\ge X_j\ \forall j\}$; LP duality ⇒
  $\bar p=\max_{q\ge0}\{\sum q_jX_j:\sum q_j=1,\ \sum q_js_j=100\}$ (Lagrange multipliers of the constraints are a
  probability; the stock constraint makes it a martingale); call $X=(0,0,25)$: vertex $q=(5/9,0,4/9)$ ⇒ $\bar p=
  25\cdot4/9=100/9\approx11.11$; primal vertex $\Delta=5/9$, $B=-44.44$ (tight at states 1 and 3); $\underline p$: $q\to
  (0,1,0)$ ⇒ 0; strictly positive Q excludes endpoints ⇒ open interval.
- **Signature visual:** split screen. Left, (S, payoff): the three payoff points and a line lowered onto them from
  above until it rests on two (a lid), its height at 100 = 11.11; a second line pushed up from below. Right, (B, Δ)
  plane: three half-planes shade in, the objective's level line sweeps down and stops at the vertex; the simplex dot
  hops vertex → vertex (Lab 2's `simplex` again, now on this LP: replay of pivots with the objective value). Bottom:
  the ch 5 simplex triangle with the call's expectation coloured along the EMM segment; its max and min sit at the
  segment's ends. Primal and dual light up together.
- **Experiment:** existing `incomplete` (interval for an ATM call constant at [0, 0.197] as states go 3 → 33) kept as
  the closing plot.
- **Pause:** "Add a fourth state at 100. Does the interval change?" (No: the lid still rests on 80 and 125.)

### 08 · Completing the market, and super-replication through time (2.5 min, 350 w) — item 5
- **Goal:** traded options complete the market; dynamic super-replication = BS at the highest volatility.
- **Beats:** 33-state market; add traded calls one strike at a time → the interval for a digital (pays 1 above 1.1)
  closes around its true price (Ross 1976, *Options and efficiency*) → many periods: a trinomial tree with only stock
  and bond; super-replication by dynamic programming (Föllmer–Schied ch. 7; Kramkov 1996 optional decomposition,
  named) → its price converges to Black–Scholes at the *largest* volatility the tree allows: the uncertain-volatility
  model (Avellaneda–Levy–Parás 1995; Lyons 1995).
- **Derivation:** one trinomial step, convex $V$: $\max_{q:\ \mathbb E^q[S_1]=S_0}\mathbb E^q[V(S_1)]$ puts all mass on
  the extremes (a convex function's max over a segment of measures is at an endpoint, by linearity in q and Jensen) ⇒
  each step is a CRR step with $u=e^{\sigma\sqrt{\Delta t}}$ ⇒ super-price = CRR price ⇒ $\to BS(\sigma_{\max})$;
  sub-price: all mass on the middle ⇒ intrinsic value.
- **Signature visual:** the interval bar for the digital shrinking strike by strike (ValueTracker over strikes), each
  new strike's payoff hinge flashing on the state axis; then a trinomial tree whose super-price fold-back chooses, at
  each node, the outer branches (they glow), the middle branches greying out.
- **Experiment (`completing`, seconds; `super_tree`, seconds):** probe: digital true 0.290; interval [0, 0.779] with no
  options → [0.032, 0.713] (1 strike) → [0.139, 0.488] (4) → [0.223, 0.379] (5) → [0.253, 0.338] (10). Trinomial super
  price N = 1, 4, 16, 64, 256: 12.44, 9.35, 9.79, 9.91, 9.94 → BS(25%) 9.95.
- **Pause:** "Which single extra strike narrows the digital's interval most?" (the ones bracketing 1.1.)

### 09 · Continuous time: Harrison–Kreps–Pliska, and Girsanov as reweighting (3.0 min, 420 w) — item 6
- **Goal:** the continuous-time FTAPs; Q as reweighted paths.
- **Beats:** self-financing = gains are stochastic integrals (Part 5) → discounted prices must be Q-martingales; Q
  from P by Girsanov with the market price of risk λ = (μ − r)/σ → both theorems (HK 1979, HP 1981): NA ⇔ EMM exists
  (with admissibility; ch 10), complete ⇔ unique (martingale representation gives the hedge) → MC: pricing with
  P-paths and weights.
- **Derivation:** $dS=\mu Sdt+\sigma SdW$; $\tilde S=S/B$: $d\tilde S=(\mu-r)\tilde Sdt+\sigma\tilde SdW$ (Itô, product
  rule); $W^Q_t=W_t+\lambda t$ ⇒ $d\tilde S=\sigma\tilde SdW^Q$ (substitute); $Z_T=\frac{dQ}{dP}=e^{-\lambda W_T-\frac12
  \lambda^2T}$ (Girsanov); $V_0=\mathbb E^P[Z_TB_T^{-1}X]=\mathbb E^Q[B_T^{-1}X]$; $\mathbb E^P[Z_T^2]=e^{\lambda^2T}$ ⇒
  effective sample size $N e^{-\lambda^2T}$ (square the exponential, Gaussian MGF).
- **Signature visual:** a `PathFan` of 200 P-paths (blue) with drift; each path's thickness and colour morph to its
  weight $Z_T$ (high-return paths thin out, low ones thicken, recoloured gold); the terminal density on the side shifts
  left from the P-density to the Q-density as weights apply; the discounted mean line flattens to S₀. The measure
  change is seen as the same paths counted differently.
- **Experiment (`girsanov`, ~1 min):** μ = 10%, r = 0, σ = 25%, 200k seeded paths: weighted P-price of the ATM call vs BS
  9.95 (expected within ~2 MC s.e.); ESS fraction e^{−0.16} = 0.852 predicted and measured.
- **Pause:** "If μ were 60%, what happens to the weights?" (ESS e^{−5.76} ≈ 0.3%: a few paths carry the price.)

### 10 · Free lunches, doubling, and bubbles: Delbaen–Schachermayer (3.0 min, 420 w) — item 6
- **Goal:** why continuous time needs admissibility and NFLVR; strict local martingales.
- **Beats:** the continuous-time doubling strategy wins 1 for sure in finite time → its cost: unbounded interim losses
  → admissibility (wealth ≥ −a) → still not enough in general: Kreps 1981 "free lunch", DS 1994 "no free lunch with
  vanishing risk" (definition card) ⇔ equivalent (σ-, Delbaen–Schachermayer 1998, named) martingale measure;
  Dalang–Morton–Willinger 1990 for discrete time on any Ω → bubbles: a strict local martingale price satisfies NFLVR
  yet E^Q[S_T] < S₀, and parity fails (Cox–Hobson 2005).
- **Derivation:** strategy $\theta_t=(T-t)^{-1/2}$ on $W$: $X_t=\int_0^t(T-s)^{-1/2}dW_s$ has quadratic variation
  $\ln\frac{T}{T-t}\to\infty$ (Itô isometry) ⇒ a time-changed BM with infinite clock (Dambis–Dubins–Schwarz) ⇒ hits 1
  before $T$ a.s.; stop there. $P(\min X<-k\text{ before }+1)=\frac1{1+k}$ (gambler's ruin for BM, Part 4). Bubble:
  $S_t=1/|B_t|$, $B$ 3-D BM from $(1,0,0)$: local martingale (Itô; $1/|x|$ harmonic in ℝ³), $\mathbb E[S_T]=2\Phi(1/\sqrt
  T)-1<1$ ⇒ strict; $C-P=\mathbb E[S_T]-K\neq S_0-K$ (parity with a bubble).
- **Signature visual:** 200 doubling-strategy wealth paths all crawling up to the line +1 and stopping, while a
  histogram of their worst losses grows on the left with a tail that keeps going (counter: 50% below −1, 9% below −10);
  a floor at −a slides in (admissibility) and most paths are cut off before winning. Then a fan of 1/|B| paths: each
  path "fair", yet the mean line sinks from 1 toward 0.683 at T = 1 — the bubble seen as mass escaping to a few huge
  paths that the average never gets back.
- **Experiment (`free_lunch`, ~3 min):** doubling via time change, 20k paths: fractions below −1, −10 vs 1/2, 1/11;
  inverse Bessel E[S_T] for T ∈ {0.25, 1, 4}: MC (exact Gaussian sampling of B_T) vs 2Φ(1/√T) − 1 = 0.9545, 0.6827,
  0.3829.
- **Pause:** "The doubler never loses at the end. Why is it not an arbitrage in the theorem's sense?" (unbounded
  credit; not admissible.)

### 11 · Change of numeraire (3.5 min, 490 w) — item 7 — `s05_continuous.py` → `s11_numeraire.py`
- **Goal:** any positive asset can be the unit; derive the density; use it four times.
- **Beats:** theorem card (Geman–El Karoui–Rochet 1995; Jamshidian 1989) → derivation → (i) N(d1) and N(d2) are the
  same event's probability under the stock and the bond numeraire → (ii) Margrabe's exchange option in two lines
  (Margrabe 1978) → (iii) T-forward and annuity measures (one line each; Parts 18–19) → (iv) Deribit: BTC is the
  numeraire, so parity read 1 − K/F → the Ross link previewed (ch 14: the long bond as numeraire).
- **Derivation:** $V_0/N_0=\mathbb E^{Q^N}[V_T/N_T]$ and $V_0/B_0=\mathbb E^Q[V_T/B_T]$ ⇒ $\frac{dQ^N}{dQ}=\frac{N_T/N_0}
  {B_T/B_0}$ (equate; LOOP); BS: $C=\mathbb E^Q[e^{-rT}S_T1_{S_T>K}]-Ke^{-rT}Q(S_T>K)=S_0Q^S(S_T>K)-Ke^{-rT}Q(S_T>K)$
  (first term: change to the stock numeraire); under $Q^S$, $\ln S_T$ has drift $r+\frac12\sigma^2$ (Girsanov with
  $\sigma$) ⇒ $N(d_1)$; ATM σ = 25%, T = 1: N(d1) = 0.5497, N(d2) = 0.4503, C = 9.95. Margrabe: $\frac{(S^1_T-S^2_T)^+}
  {S^2_T}=(R_T-1)^+$, $R=S^1/S^2$ a $Q^{S^2}$-martingale with vol $\sigma^2=\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2$
  ⇒ price $=S^2_0\,BS(R_0,1,\sigma,T)$. Inverse option: $\tilde C=\mathbb E^{Q^{BTC}}[(S_T-K)^+/S_T]$ (USD price ÷
  BTC price).
- **Signature visual:** a path fan in dollars; a second numeraire's path is drawn; every path is divided by it point
  by point and the fan visibly re-shapes (rescaling every path), while path weights recolour by $N_T/N_0$; the two
  terminal densities q(s) and q(s)·s/F (the share measure) are drawn on one axis and the areas right of K shade:
  0.4503 under Q, 0.5497 under Q^S. One payoff, two units, two probabilities, one price.
- **Experiment (`numeraire`, ~1 min):** Margrabe (S₁ = S₂ = 100, σ = 30%, ρ = 0.5 ⇒ σ_R = 30%): formula 11.92 vs 1M-path MC
  under Q and under Q^{S²} (both agree within s.e.); the 107-day Surface call priced in USD and in BTC gives one price.
- **Pause:** "Under the stock numeraire, is the stock's drift higher or lower than r?" (higher by σ².)

### 12 · Butterflies build the density (2.5 min, 350 w) — item 8 — `s06_density.py` split
- **Goal:** state prices are butterfly prices; the density is their limit; static no-arbitrage is convexity.
- **Beats:** the butterfly payoff (triangle of area h) → its price = state price of the bin → a histogram of
  butterflies across strikes → h → 0, histogram becomes the density (BL 1978) → static conditions: C decreasing,
  convex, within bounds — exactly "all butterflies and call spreads cost ≥ 0" → Lab 4: `static_checks` on raw quotes vs
  the SVI fit.
- **Derivation:** $C(K)=e^{-rT}\int_K^\infty(s-K)q(s)ds$; $C'(K)=-e^{-rT}\int_K^\infty q$ (Leibniz; boundary term 0) ⇒
  $-e^{rT}C'(K)=Q(S_T>K)$ (a digital); $C''(K)=e^{-rT}q(K)$; butterfly $\frac{C(K-h)-2C(K)+C(K+h)}{h^2}\to C''(K)$ (Taylor);
  convexity ⇔ $q\ge0$; $-e^{-rT}\le C'\le0$ ⇔ $0\le Q(S_T>K)\le1$.
- **Signature visual:** state prices as a histogram that becomes the density: a row of triangle payoffs tiles the
  strike axis; each lifts into a bar of height (price/h); h halves four times, bars multiply and thin, their outline
  converging onto the smooth BL curve. Then the call curve C(K) with its tangent (digital) and its curvature (density)
  readouts riding along a strike slider.
- **Experiment (`butterflies`, seconds):** butterflies from raw per-instrument Surface quotes (no smoothing) at the
  16-day expiry: count of negative butterflies (expected: some, from noise and bid–ask; branch on count) vs zero for
  SVI; mass and mean of the BL density: 0.99999 and 92,868 vs F = 92,869 (cached).
- **Pause:** "A butterfly costs −0.1. What do you trade?" (buy it: paid to own a non-negative payoff.)

### 13 · The density on the Surface, fitted and stress-tested (3.0 min, 420 w) — item 8
- **Goal:** watch the fit, see the term structure in 3D, and see how much the tails depend on the fit.
- **Beats:** SVI fit replay (Gatheral; Part 12 derives it) → density updates as the fit converges → all 11 expiries
  (1 day to 289 days) as a 3D ridge → calendar condition (total variance rising) → specification band: SVI vs a cubic
  spline in IV vs 2- and 3-component log-normal mixtures — prices nearly equal, tails not (link to Shikhman et al. 2026:
  95 of 126 pricing directions numerically null) → numbers read off (Q(−20%) 2.9% at 16 d, 19.1% at 107 d; cached).
- **Derivation:** $w(k)=\sigma_{BS}^2T$, SVI $w(k)=a+b(\rho(k-m)+\sqrt{(k-m)^2+s^2})$; $C=BS(F,K,\sqrt{w/T})$;
  $q=\partial_{KK}C$ (ch 12); calendar NA: $w(k,T_2)\ge w(k,T_1)$ at fixed $k$ (a calendar spread of forward-moneyness
  calls is a non-negative payoff); Lee's wing bound $b(1+|\rho|)\le2$ (named, Part 12).
- **Signature visual:** `TrainingReplay`: left, the smile (dots = quotes, curve = current fit) and the density beneath
  it reshaping; right, the RMSE curve over iterations (iterates recorded by rerunning `least_squares` with max_nfev =
  1, 2, 4, …). Then a `ThreeDScene`: strike × maturity × density, 11 ridges rising out of the floor, camera walking
  along maturity; the ridges widen with T (variance growing) and the left shoulder fattens (skew).
- **Experiment (`density_fit`, `density_specs`, `density_term`, ~6 min):** fit trace; four specifications at 107 d with
  price RMSE (all small) and Q(down 30%) per spec (spread reported, branch: "the tails disagree by X points");
  densities for all 11 expiries with calendar check (cached 0 violations for the pair; recompute for all).
- **Pause:** "Four fits price every quote within the spread. Should their crash probabilities agree?"

### 14 · Ross recovery, and its critique (3.5 min, 490 w) — item 9 — `s07_ross.py` rewritten
- **Goal:** derive Ross recovery, run it, see where it fails, and know the evidence.
- **Beats:** the claim (Ross 2015) → assumption (transition-independent kernel) → Perron–Frobenius → Lab 5: power
  iteration converging → synthetic truth recovered → BHS 2016: the kernel's permanent martingale component; the
  recovered measure is the long-bond numeraire measure (Martin–Ross 2019; Qin–Linetsky 2016) → sweep: error grows with
  the permanent component → evidence: Jackwerth–Menner 2020 (S&P 500: recovered distributions rejected; simple
  benchmarks not) → defences: Jensen–Lando–Pedersen 2019 generalized recovery; Horvath 2025 arbitrage-based recovery
  (claims to work with a non-trivial permanent component on 26 years of S&P options) — the debate is open.
- **Derivation:** $P_{ij}=\pi_{ij}m_{ij}$ (definition); assume $m_{ij}=\delta\phi_j/\phi_i$ ⇒ $\pi_{ij}=\frac1\delta P_{ij}
  \frac{\phi_i}{\phi_j}$; rows of π sum to 1 ⇒ $\sum_jP_{ij}z_j=\delta z_i$ with $z=1/\phi$ ⇒ $Pz=\delta z$, $z>0$;
  Perron–Frobenius: an irreducible positive matrix has exactly one positive eigenvector (unique) ⇒ π recovered. BHS:
  $M_t=e^{-\rho t}\frac{\hat\phi(X_0)}{\hat\phi(X_t)}\hat M_t$ with $\hat M$ a martingale ⇒ eigen-recovery returns
  $\hat P$ with $d\hat P/dP=\hat M_T$, equal to P iff $\hat M\equiv1$ (untestable from prices).
- **Signature visual:** power iteration as the moving picture: a 9-bar vector multiplied by P again and again,
  wobbling then freezing into the Perron vector (iteration counter; eigenvalue readout 0.879 → 0.905 → 0.945 → 0.970 →
  0.9793 → 0.97999 at k = 1, 2, 5, 10, 20, 40 (probe; δ = 0.98)); then heatmaps truth / recovered / error, and a
  slider for the permanent component's strength that warms the error heatmap.
- **Experiment (`ross` kept; `ross_sweep`, ~1 min):** error vs strength s = 0…1: 0, 0.017, 0.034, 0.051, 0.069, 0.086
  (probe, one economy); add 200 random economies (seeded) as a spread band.
- **Pause:** "Ross's recovered measure looks pessimistic. Is that evidence investors are pessimistic?" (No: it is a
  risk adjustment it cannot separate.)

### 15 · Bounds without a model: martingale optimal transport (3.0 min, 420 w) — item 10 — `s08_mot.py` split
- **Goal:** set up MOT, derive its dual (the model-free hedge), see the hedge touch the payoff.
- **Beats:** marginals fix every vanilla; joining is free except for the martingale property → convex order (Strassen)
  as nested call curves → primal LP → dual = static vanilla portfolio u(S₁) + v(S₂) + dynamic delta h(S₁)(S₂ − S₁)
  (BHP 2013 duality theorem card; GHLT 2014: in continuous time the dual is a stochastic control problem) → Hobson 1998
  for lookbacks (one beat) → the forward-call band is exactly half the straddle's.
- **Derivation:** primal $\sup_\pi\sum\pi_{ij}c_{ij}$ s.t. $\sum_j\pi_{ij}=\mu_i$, $\sum_i\pi_{ij}=\nu_j$, $\sum_j\pi_{ij}
  (y_j-x_i)=0$; Lagrangian with $u_i,v_j,h_i$ ⇒ dual $\inf\sum u_i\mu_i+\sum v_j\nu_j$ s.t. $u_i+v_j+h_i(y_j-x_i)\ge
  c_{ij}$ (weak duality: integrate the inequality against any feasible π; the $h$ term vanishes by the martingale
  constraint); LP strong duality ⇒ equality; feasibility ⇔ $\mu\le_{cx}\nu$ ⇔ $\int(y-k)^+d\nu\ge\int(x-k)^+d\mu\ \forall
  k$ (Strassen 1965). Forward call: $(R-1)^+=\frac12(|R-1|+(R-1))$ and $\mathbb E[R-1\mid S_1]=0$ ⇒ band halves.
- **Signature visual (3D):** `ThreeDScene` over (S₁/F₁, S₂/F₂): the payoff surface |y/x − 1| (a V-shaped trough along
  the diagonal) and the optimal dual hedge surface u(x)+v(y)+h(x)(y−x) lowered onto it from above until it rests on it;
  the contact set lights up and coincides with where the optimal coupling's dots sit (shown on the floor). Camera
  orbits. The idea seen: the price bound is the cheapest hedge that stays above the payoff, and the extreme model lives
  exactly where the hedge touches.
- **Experiment:** dual variables from HiGHS (`res.eqlin.marginals`, extend `mot_bounds(..., dual=True)`); probe bounds
  on the cached marginals: straddle [0.1375, 0.2175], forward call [0.0688, 0.1088] (exactly half), (S₂−S₁)² band
  zero-width at 0.05677, (log S₂/S₁)² [0.0572, 0.0741].
- **Pause:** "Why is the band for (S₂ − S₁)² a single number?" ($\mathbb E[(S_2-S_1)^2]=\mathbb E[S_2^2]-\mathbb E[S_1^2]$
  for any martingale: both marginals fix it.)

### 16 · MOT on the Surface, computed and converging (2.5 min, 350 w) — item 10
- **Goal:** watch the bounds converge (grid, entropic iterations) and read the band against a model.
- **Beats:** Lab 6: `mot_bounds` on screen → run on the Surface (16 d → 107 d) → bounds as the later grid refines →
  entropic MOT (martingale Sinkhorn style) converging to the LP value as ε shrinks → log-normal 0.180 inside the band;
  a dealer outside it is arbitrageable with vanillas plus one delta.
- **Derivation:** entropic dual $\max\ \sum u\mu+\sum v\nu-\varepsilon\sum_{ij}\mu_i\nu_je^{(u_i+v_j+h_i(y_j-x_i)-c_{ij})/
  \varepsilon}$; coordinate ascent: $u$ and $v$ in closed form (log-sum-exp), $h_i$ by a 1-D Newton step (root of
  $\sum_j(y_j-x_i)e^{\cdot}=0$, the martingale condition) — Sinkhorn with a martingale step; gap to LP $=O(\varepsilon\log)$.
- **Signature visual:** the band [lower, upper] drawn as two walls closing in as atoms go 9 → 161 (ValueTracker over
  resolution); then the coupling dot-cloud sharpening from a blur (large ε) to the LP's sparse extreme coupling while
  the objective curve approaches the LP line (`TrainingReplay`, iterations on x).
- **Experiment (`mot_grid` ~10 min, `mot_entropic` ~5 min):** bounds for the straddle at (later) atoms 21, 41, 81, 161,
  321 (earlier 25 → 81) with convex order checked; entropic trace for ε ∈ {0.1, 0.03, 0.01, 0.003}: objective vs
  iteration, converging to 0.2175 / 0.1375 within the stated gap.
- **Pause:** "As the grid gets finer, can the band shrink?" (It can widen or shrink slightly; it converges.)

### 17 · Industry: how arbitrage is traded, and why it is limited (3.5 min, 490 w)
- **Goal:** the businesses that enforce no arbitrage, with numbers, and where they failed.
- **Beats (each a firm/crisis card with sources in §4):**
  1. *ETFs and authorized participants:* creation/redemption in-kind baskets keep price ≈ NAV; Rule 6c-11 (SEC,
     September 2019). March 2020: IG bond ETFs averaged a 3.4% discount mid-March, some over 8%; IOSCO: 6–10% in extreme
     cases; Haddad–Moreira–Muir: liquid bond ETFs at large discounts, more so for safer bonds (the arbitrage band is
     the AP's balance-sheet cost). Full ETF market making: Part 38.
  2. *Box spreads as financing:* box rates sit about 35 bp above Treasuries on average (S&P options, 1996–Apr 2023;
     NY Fed); 2004–2018 convenience yield ≈ 40 bp, 65 bp under 3 months, 100–160 bp in 2008 (van Binsbergen, Diamond,
     Grotteria 2022). A box-spread ETF (BOXX) launched 28 Dec 2022; assets ≈ $7.7 bn by Aug 2025 (aggregator figure).
     Our own Deribit cash-and-carry (ch 1) is the crypto version.
  3. *Parity and hard-to-borrow:* ORW 2004; Palm/3Com (ch 2); Mitchell–Pulvino–Stafford: 82 negative-stub cases
     1985–2000, ~30% severed before convergence.
  4. *Convergence trades:* Royal Dutch/Shell (60:40 claim on one firm): mean absolute deviation 9.53% over 1980–1995
     (RBA, matching Froot–Dabora's sample).
  5. *Limits of arbitrage:* Shleifer–Vishny 1997: arbitrageurs run other people's money; when mispricing widens, capital
     is withdrawn exactly when the trade is best.
  6. *LTCM:* founded Feb 1994; returns 20%, 43%, 41%, 17% (1994–97); about 30:1 leverage end-1997; −44% in August 1998;
     14 firms put up $3.625 bn for 90% on 23 Sept 1998 (NY Fed convened, no Fed money); PWG report 28 April 1999.
     Secondary (label it): ~$4.7 bn equity, ~$125 bn borrowed at the start of 1998. Full story: Part 41.
- **Signature visual:** a "convergence spread" simulator: a mean-reverting spread with a performance-based investor
  flow (Shleifer–Vishny's mechanism, `simulated`): the spread widens, the fund's equity bar shrinks, redemptions cut the
  position at the worst point; three seeds as a band. Then the LTCM card.
- **Experiment (`sv_sim`, ~2 min):** Shleifer–Vishny two-period model with redemption elasticity a ∈ {0, 0.5, 1, 2}:
  probability of forced liquidation before convergence, 1,000 seeded paths each; expected: rises with a.
- **Pause:** "A trade that converges with certainty can still bankrupt you. What one quantity decides it?" (funding
  horizon vs time to convergence.)

### 18 · Frontier, 2023–2026 (2.5 min, 350 w)
- **Goal:** where the theory is moving, with one thing trained on screen.
- **Beats (cards, verified in §5):** neural MOT (Neufeld–Sester 2023) → **trained here**: a small network dual
  (u, v, h as MLPs, penalty method) learning the straddle's upper bound → martingale Sinkhorn (Hasenbichler, Joseph,
  Loeper, Obłój, Pammer) and multi-marginal MOT (Engström–Källblad–Karlsson 2024) → exact joint SPX/VIX: absence of
  joint arbitrage ⇔ a calibrating martingale measure exists (Guyon 2024) → multi-asset FTAP and bounds as linear
  semi-infinite programs, d = 60 (Neufeld–Papapantoleon–Xiang 2023) → adapted Wasserstein geometry: martingales a
  closed geodesically convex set (Bartl–Beiglböck–Pammer 2026) → recovery: Horvath 2025, Heston–Jacobs–Kim 2023 →
  densities: accurate prices need not pin the density (Shikhman et al. 2026).
- **Signature visual:** `TrainingReplay`: left, the learned hedge surface (as in ch 15) forming; right, the dual
  objective falling onto the LP line, three seeds as a band; baseline = LP at equal grid.
- **Experiment (`neural_mot`, ~20 min, torch 2 threads, 3 seeds × 3,000 steps):** expected: learned bound within ~1–2%
  of 0.2175, above it (penalty slack); narration branches on gap and seed spread; says plainly the LP wins in 1-D and
  the network matters in many dimensions.
- **Pause:** "Why does a neural dual give an upper bound only approximately?" (penalized constraints can be violated.)

### 19 · The arbitrage checker, recap, desk, problems (2.5 min, 350 w) — `s09_house.py` + `s10_outro.py` merged
House chart (Rule 10, trial counter 72), new functions listed; recap in ten lines (one per item); desk questions (kept,
plus "Price a digital from two calls" and "The stub is negative: is it an arbitrage?"); problem set (kept five, add:
"show the forward-start call band is half the straddle's"; "derive Margrabe by change of numeraire"); references card.

## 4. Industry sources (public record, checked)

- SEC Rule 6c-11 adopting release (2019) and AP/creation-unit definitions: https://www.govinfo.gov/link/fr/84/57089 ;
  exemptive order https://www.sec.gov/files/rules/exorders/2019/34-87110.pdf
- IG bond ETF discounts, March 2020 (3.4% average, >8% some): https://www.investmentexecutive.com/report-cards/etf-guide-2020/fixed-income-etfs-pass-their-toughest-test/ ;
  IOSCO (6–10% extreme cases): https://www.iosco.org/library/pubdocs/pdf/IOSCOPD682.pdf
- Haddad, Moreira, Muir (2021), "When selling becomes viral", *RFS* 34(11):5309–5351: https://www.nber.org/papers/w27168
- van Binsbergen, Diamond, Grotteria (2022), "Risk-free interest rates", *JFE* 143(1):1–29:
  https://lbsresearch.london.edu/id/eprint/1821 ; NY Fed Liberty Street (box rate +35 bp, 1996–Apr 2023):
  https://libertystreeteconomics.newyorkfed.org/?p=24920
- BOXX (launch 28 Dec 2022; ≥80% box spreads; ≈$7.7 bn AUM 15 Aug 2025, MarketBeat — aggregator, re-check on issuer site):
  https://www.marketbeat.com/stocks/BATS/BOXX/ (unverified against issuer filing)
- Palm/3Com prices and −$22 bn stub: Cochrane, "Stocks as money", NBER w8987: https://www.nber.org/papers/w8987 ;
  147.6% short interest, puts ≈2× parity, synthetic $39.12 vs $55.25 (16 March 2000):
  https://www.chicagobooth.edu/review/can-market-add-and-subtract ; Lamont–Thaler (2003), *JPE* 111(2) (venue from
  memory; verify page range)
- Mitchell, Pulvino, Stafford (2002), *JF* 57(2):551–584: https://www.aqr.com/Insights/Research/Journal-Article/Limited-Arbitrage-in-Equity-Markets
- Froot, Dabora (1999), *JFE* 53(2):189–216: https://www.nber.org/papers/w6572 ; RBA RDP 2003-06 (9.53%):
  https://www.rba.gov.au/publications/rdp/2003/2003-06/examples-of-dual-listed-companies-and-puzzles-in-their-pricing.html
- LTCM: Federal Reserve History, https://www.federalreservehistory.org/essays/ltcm-near-failure ; GAO GGD-00-67R,
  https://www.gao.gov/assets/ggd-00-67r.pdf ; CRS RL30232 (PWG report 28 April 1999),
  https://www.everycrsreport.com/files/19990610_RL30232_fd9283f5230e25d04cbfc2f1a9591b6eb469ffac.html .
  Equity/borrowing figures are from Wikipedia (secondary): label or drop. Notional "$1.25 trillion" (unverified): drop.
- Shleifer, Vishny (1997), "The limits of arbitrage", *JF* 52(1):35–55 (already in READING.md Part 23).

## 5. Frontier sources (verified: authors, year, title, venue/id)

| Item | Status |
|---|---|
| Guyon, J. (2024). "Dispersion-constrained martingale Schrödinger problems and the exact joint S&P 500/VIX smile calibration puzzle." *Finance and Stochastics* 28(1):27–79. https://ideas.repec.org/a/spr/finsto/v28y2024i1d10.1007_s00780-023-00524-y.html | verified |
| Hasenbichler, M., Joseph, B., Loeper, G., Obłój, J., Pammer, G. "The Martingale Sinkhorn Algorithm." arXiv:2310.13797 (v1 2023 as "The Measure Preserving Martingale Sinkhorn Algorithm", Joseph–Loeper–Obłój; v5 March 2026). https://arxiv.org/abs/2310.13797 | verified (preprint) |
| Engström, L., Källblad, S., Karlsson, J. (2024). "Computation of robust option prices via structured multi-marginal martingale optimal transport." arXiv:2406.09959. https://arxiv.org/abs/2406.09959 | verified (preprint) |
| Neufeld, A., Sester, J. (2023). "A deep learning approach to data-driven model-free pricing and to martingale optimal transport." *IEEE Trans. Information Theory* 69(5):3172–3189; arXiv:2103.11435 | verified |
| Neufeld, A., Papapantoleon, A., Xiang, Q. (2023). "Model-free bounds for multi-asset options using option-implied information and their exact computation." *Management Science* 69(4):2051–2068; arXiv:2006.14288 | verified |
| Kupper, M., Nendel, M., Sgarabottolo, A. (2023). "Risk measures based on weak optimal transport." arXiv:2312.05973 | verified (preprint) |
| Bartl, D., Beiglböck, M., Pammer, G. (2026). "The Wasserstein space of stochastic processes." *J. Eur. Math. Soc.* 28(1):393–454. https://ems.press/doi/10.4171/jems/1554 | verified |
| Backhoff-Veraguas, J., Beiglböck, M., Schachermayer, W., Tschiderer, B. "Existence of Bass martingales and the martingale Benamou–Brenier problem in ℝ^d." arXiv:2306.11019 | verified preprint; venue unverified |
| Horvath, F. (2025). "Arbitrage-based recovery." *JFE* 163:103969. https://ideas.repec.org/a/eee/jfinec/v163y2025ics0304405x24001922.html | verified |
| Heston, S., Jacobs, K., Kim, H. J. (2023). "The Pricing Kernel in Options." FEDS 2023-053. https://doi.org/10.17016/FEDS.2023.053 | verified (working paper) |
| Shikhman, L. J., Galarnyk, M., Dash, A., Welsh, N. A. (2026). "Inverse learning of latent risk-neutral densities from irregular option quotes." arXiv:2607.27188, ICAIF 2026 | verified |
| Background, pre-2023: Jackwerth, Menner (2020), "Does the Ross recovery theorem work empirically?" *JFE* 137(3):723–739 | verified |
| Jensen, Lando, Pedersen (2019), "Generalized recovery," *JFE* 133(1) | (unverified venue/pages) |
| Martin, Ross (2019), "Notes on the yield curve," *JFE*; Qin, Linetsky (2016), *Operations Research*; arXiv:1411.3075 | arXiv verified; venues (unverified) |
| Ning, Jaimungal, Zhang, Bergeron, "Arbitrage-free implied volatility surface generation with VAEs," arXiv:2108.04941 | venue unverified; better placed in Part 12 |

Also add to READING.md Part 9 (classics used on screen, from memory, standard citations): Farkas (1902) *J. reine
angew. Math.* 124; Stiemke (1915) *Math. Ann.* 76; Ross (1976) "Options and efficiency" *QJE* 90(1); Margrabe (1978) *JF*
33(1); Kreps (1981) *J. Math. Econ.* 8; Jamshidian (1989) *JF* 44(1); Schachermayer (1992) *Insurance: Math. Econ.* 11;
Avellaneda–Levy–Parás (1995) and Lyons (1995), *Applied Math. Finance* 2(2); Kramkov (1996) *PTRF* 105; Jackwerth
(2000) *RFS* 13(2); Cox–Hobson (2005) *Finance and Stochastics* 9(4); Strassen (1965) *Ann. Math. Stat.* 36. Each to be
checked in the frontier sweep before it goes on screen.

## 6. Hands-on summary

**Replays (ValueTracker, objective drawn alongside):** ch 4 simplex pivots (FTAP LP); ch 7 simplex on the
super-replication LP in the (B, Δ) plane; ch 8 interval closing strike by strike; ch 13 SVI fit with density;
ch 14 power iteration; ch 16 MOT grid refinement and entropic iterations; ch 18 neural dual, 3 seeds as a band.

**Labs (code_block ≤12 lines, then run live):**
1. ch 1 `arbitrage.implied_forward` (new, moved from `compute_parity`): group trades by (expiry, K, cp); nearest put
   within 600 s; skip |ln K/index| > 0.2; `F = K / (1 - (c - p))`; per-expiry median and rate `log(F/index)/T`.
2. ch 4/7 `arbitrage.simplex` (new, teaching): `while True: j = first column with negative reduced cost (Bland);
   if none: return; ratios = b/A[:, j] for A[:, j] > 0; i = argmin; pivot(i, j); trace.append((basis, x, obj))`.
3. ch 6 `trees.crr` (exists): `values = max(cp*(spots-K),0)`; `for n in reversed(range(N)): values = disc*(p*values[1:]
   + (1-p)*values[:-1])`; American: `values = maximum(values, exercise)`.
4. ch 12 `arbitrage.static_checks` (exists): slopes, `diff(slope) < 0` ⇒ butterfly violations, bounds.
5. ch 14 `arbitrage.ross_recovery` + new `power_iteration(P, k)`.
6. ch 16 `arbitrage.mot_bounds` (exists; add `dual=True` returning u, v, h from `res.eqlin.marginals`).

**Things that run on screen:** listed per chapter under *Signature visual* (every chapter has one).

**New House functions (tests in `tests/test_quant_house.py`):** `implied_forward`, `simplex` (agrees with HiGHS on
random small LPs), `superhedge_tree` (trinomial DP; equals CRR for convex payoffs), `power_iteration`,
`mot_bounds(..., dual=True)` (dual objective = primal), `entropic_mot` (→ LP as ε → 0), `mot_neural` in a separate
torch module (`explainer/quant/house/deep.py` already exists; add there).

## 7. Compute budget (≈ 70 CPU-min, under the 2 h default; all seeded; long items resumable via `CACHE.partial`)

| Item | Chapter | Est. min | Notes |
|---|---|---|---|
| `parity` (exists) | 0–1 | 1 | |
| `futures_basis` (new) | 1, 17 | 3 | fetch Deribit futures 00–12 UTC (cached per hour, add to manifest) |
| `ftap_trace`, `simplex_lab` | 3–4, 7 | <1 | |
| `kernel` (BTC SDF, bootstrap 1000) | 5 | 3 | Binance daily cached |
| `crr_convergence`, `crr_replicate` | 6 | 1 | |
| `incomplete` (exists), `completing`, `super_tree` | 7–8 | 1 | |
| `girsanov` (200k paths) | 9 | 1 | |
| `free_lunch` (doubling 20k paths; Bessel) | 10 | 3 | |
| `numeraire` (Margrabe 1M paths; BTC vs USD) | 11 | 1 | |
| `butterflies`, `density` (exists), `density_fit`, `density_specs`, `density_term` | 12–13 | 6 | |
| `ross` (exists), `ross_sweep` (200 economies) | 14 | 1 | |
| `mot` (exists), `mot_dual`, `mot_claims` | 15 | 2 | |
| `mot_grid` (to 81×321), `mot_entropic` | 16 | 15 | partial per grid size |
| `sv_sim` | 17 | 2 | |
| `neural_mot` (3 seeds, torch 2 threads) | 18 | 25 | checkpoints every 250 steps, resumable |
| `envelope` (exists) | 19 | 0 | |
| **Total** | | **≈ 66** | |

## 8. Revised SYLLABUS.md §6 entry (ready to paste)

```markdown
### Part 9 · No Arbitrage (~57)
1. Arbitrage, the law of one price and put–call parity, proved by replication and checked on the Surface against
   Deribit futures; where parity breaks: borrow (Ofek–Richardson–Whitelaw 2004), Palm/3Com, American boxes.
2. One period: the FTAP by separating hyperplanes (Farkas, Stiemke), proved, seen in 3D, and decided by a simplex run
   on screen.
3. State prices and the SDF; Q as the SDF renormalized; the risk-neutral simplex; Bitcoin's empirical pricing kernel.
4. The binomial tree (Cox–Ross–Rubinstein 1979): replication derived, the hedge run along a path, convergence to
   Black–Scholes.
5. Completeness; super-replication as an LP and its dual; options complete the market (Ross 1976); dynamic
   super-replication and uncertain volatility (Avellaneda–Levy–Parás 1995).
6. Continuous time: Harrison–Kreps, Harrison–Pliska, Girsanov as reweighting; doubling, admissibility, NFLVR
   (Delbaen–Schachermayer 1994), strict local martingales and bubbles (Cox–Hobson 2005).
7. Change of numeraire (Geman–El Karoui–Rochet 1995): N(d1) as a probability, Margrabe, forward and annuity
   measures, Bitcoin as numeraire.
8. Breeden–Litzenberger: butterflies become the density; static and calendar no-arbitrage; the density across the
   Surface and its dependence on the fit.
9. Ross recovery (2015), its critique (Borovička–Hansen–Scheinkman 2016) and the evidence (Jackwerth–Menner 2020;
   Horvath 2025).
10. Robust bounds: martingale optimal transport (Hobson 1998; Beiglböck–Henry-Labordère–Penkner 2013;
    Galichon–Henry-Labordère–Touzi 2014), its dual as a model-free hedge, solved by LP and by entropic iteration.
11. Industry: authorized participants and ETF discounts (March 2020), box-spread financing, negative stubs, Royal
    Dutch/Shell, limits of arbitrage (Shleifer–Vishny 1997), LTCM.
12. Frontier: neural and Sinkhorn MOT, joint SPX/VIX no-arbitrage (Guyon 2024), multi-asset bounds, adapted
    Wasserstein, the recovery debate.

*Textbooks:* Shreve I ch. 1, 3; Shreve II ch. 5, 9; Björk (4th ed.) ch. 2–3, 9–12, 15; Duffie DAPT ch. 1–2, 6;
Delbaen–Schachermayer Part I; Föllmer–Schied ch. 1, 5, 7; Henry-Labordère *Model-Free Hedging*.
*Computed:* parity forwards vs futures; the FTAP and super-replication LPs (simplex replay); CRR convergence; dynamic
super-replication; Girsanov reweighting; doubling and bubble simulations; Margrabe; BL densities on all expiries
with specification bands; Ross recovery sweep; MOT bounds, duals, grid and entropic convergence.
*Trained:* a neural MOT dual (3 seeds) against the LP.
*Visuals:* the separating plane in 3D; P→Q bars and the risk-neutral simplex; the tree folding back with its hedge;
paths reweighted and rescaled by a numeraire; butterflies becoming the density; the density ridge in 3D; the dual
hedge surface lowered onto the payoff.
*Crisis:* GameStop 2021: put–call parity and borrow. *Firms:* ETF authorized participants, box-spread lenders,
LTCM (full story in 41).
*Desk:* "Call 10, put 7, strike 100, spot 103, no rates. Arbitrage?"; box spreads, and the 2019 Robinhood
"infinite leverage" box-spread episode; "Price a digital from two calls."
*House:* the arbitrage checker (used on every surface): parity and forwards, FTAP/simplex, super-replication,
static and calendar checks, MOT bounds with duals, Ross recovery.
```

Add the §4–5 papers to `READING.md` §4 Part 9.

## 9. Minutes per chapter

| # | Chapter | Min |
|---|---|---|
| 00 | Hook: one price, and how we got here | 2.5 |
| 01 | Parity, assembled | 3.0 |
| 02 | Where parity breaks | 3.0 |
| 03 | The geometry of arbitrage, in 3D | 3.0 |
| 04 | The FTAP, proved and solved | 3.0 |
| 05 | State prices, SDF, Q | 3.0 |
| 06 | The tree | 3.5 |
| 07 | Incomplete markets: the interval as an LP | 3.0 |
| 08 | Completing the market; super-replication through time | 2.5 |
| 09 | Continuous time; Girsanov as reweighting | 3.0 |
| 10 | Free lunches, doubling, bubbles | 3.0 |
| 11 | Change of numeraire | 3.5 |
| 12 | Butterflies build the density | 2.5 |
| 13 | The density on the Surface | 3.0 |
| 14 | Ross recovery and its critique | 3.5 |
| 15 | Martingale optimal transport | 3.0 |
| 16 | MOT on the Surface, converging | 2.5 |
| 17 | Industry | 3.5 |
| 18 | Frontier | 2.5 |
| 19 | Checker, recap, desk, problems | 2.5 |
| | **Total** | **58.0** (≈ 8,100 narration words) |

Implementation notes: chapter cards renumber 1–18; module names `s01_hook … s20_outro`; Ross and MOT caches keep their
item names (renaming scene modules invalidates narration caches, as CLAUDE.md warns — expected for a rewrite); the
Chinese table `zh_lines.py` needs new entries for every new line; the README chapter list, textbook audit table and
reading guide are rewritten from §2–5 above.
