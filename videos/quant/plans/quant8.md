# Part 8 · Decisions and Control: the expansion plan

Plan of record for taking `videos/quant/quant8/` from 28 to about 60 minutes under the November 2026 standard
(SYLLABUS.md §1, with the "Hands-on, as in *AI, Built*" addendum: 16–20 chapters, replays, labs, live simulations,
about 2 CPU-hours). Research and planning only: nothing in the repo was edited. The prototype scripts used to get
the expected outputs below are in the scratchpad (`proto/dn.py`, `dn1.py`, `bt.py`, `eik.py`).

**Conflict in the standard, resolved here.** §1 says "a chapter is 4–6 minutes" and also "16–20 chapters, 50–60
minutes". Both can't hold. This plan follows the newer hands-on rule, as AI Part 26 does: 20 manifest entries of
2.6–3.6 minutes each, about 60 minutes in total. Each syllabus item gets one or two chapters. The SYLLABUS
§1 sentence should be changed to "3–6 minutes" (flagged for the owner).

---

## 1. Current state (lecture_length.py quant8: 28.2 min)

| # | Chapter (module) | Min | What it covers, and how deep |
|---|---|---|---|
| H | How much to bet (`s01_hook`) | 2.8 | Haghani–Dewey 60% coin; Kelly growth curve g(f); 20,000 simulated players per fraction (finished bars); plan; House card. No era/timeline block. |
| 1 | Utility (`s02_utility`) | 2.1 | Bernoulli, vNM named; log curve with chord and CE = 86.6 (static); CRRA; Arrow–Pratt **stated, not derived**; CE table over γ. No axioms. |
| 2 | Bellman & HJB (`s03_bellman`) | 2.9 | Three-line ladder (Bellman → HJB → FOC), **no derivation steps**; viscosity in one caption; 3D policy surface π*(t,w) with a floor (grid solver, Gauss–Hermite), slices vs portfolio-insurance closed form (gap ≤ 0.005). Best visual in the part. No verification theorem. |
| 3 | Merton (`s04_merton`) | 1.4 | π* = (μ−r)/(γσ²) on French 1926–2020 (8.2% premium, σ 18.5%): 238%/79%/24% at γ = 1/3/10, ±2 SE bars. **No consumption**, no martingale method, no mutual-fund theorem, no derivation of its own. |
| 4 | Kelly (`s05_kelly`) | 3.6 | Kelly/Breiman/Thorp cards; realized growth vs fraction on US history (peak 218%, 12.6%); bootstrap of best fraction; registered split-sample test; fractional parabola (2c − c²) and a drawdown table. Breiman **stated, not proved**; paths are never drawn. |
| 5 | Samuelson (`s06_samuelson`) | 2.7 | P(Kelly richer) vs horizon; CE growth −3.6% vs +3.9% for γ = 3; Peters' coin (82% lose, top 1% hold 86%); Doctor–Wakker–Wang reply. Solid. |
| 6 | LTCM (`s07_ltcm`) | 2.3 | Crisis card (PWG 1999: 28:1, $1.3tn notional, $3.6bn rescue); illustrative Kelly leverage 100 → 11 when vol triples. |
| 7 | Stopping (`s08_stopping`) | 1.8 | Secretary 1/e (exact + simulated); Snell recursion **one line**; American put boundary from a 500-step tree (9.87 vs 9.35). No smooth fit, no proof, no free boundary. |
| 8 | Behaviour (`s09_behaviour`) | 1.7 | PT value/weighting curves (TK 1992 parameters), disposition, lottery stocks; Ellsberg, Gilboa–Schmeidler, Hansen–Sargent, Maenhout formula **quoted**. No experiment. |
| 9 | Frontiers (`s10_frontier`) | 2.9 | BSDE two-rate call spread (LSMC → PDE 1.230, real experiment); MFG **two equations only, no experiment**; PPO on log-Merton 48% → 184% (one seed, finished curve plus final heat map; no replay). |
| 10 | House (`s11_house`) | 0.9 | Rule 9 (≤ Kelly, default half, resize on vol forecast); trial counter 72. |
| O | Outro (`s12_outro`) | 3.2 | Recap, 3 desk questions, 5 problems, forward links, next part. |

Overall: the numbers are real and honestly labelled, but the part is a survey. Derivations are stated rather than
proved, items 6–9 get under 3 minutes between them, and nothing is shown learning or being computed live. There
are no labs and no industry or frontier chapter in the new sense, and Davis–Norman, consumption, smooth fit and
viscosity are absent or one caption long.

## 2. Audit

### (a) Syllabus items (SYLLABUS §6, Part 8)

| Item | Now | Verdict |
|---|---|---|
| 1 Expected utility, risk aversion, CE | ch 1 | thin (Arrow–Pratt not derived; no axioms) |
| 2 DP; HJB derived | ch 2 | thin (no derivation steps, no verification) |
| 3 Merton by HJB and simulation | ch 2–3 | thin (HJB solved only in README problem; no consumption; simulation only via grid) |
| 4 Kelly, fractional, Thorp; Samuelson; ergodicity | ch 4–5 | covered; Breiman unproved; no live paths |
| 5 Optimal stopping; Snell; American preview | ch 7 | thin |
| 6 Prospect theory; ambiguity | ch 8 | thin (no derivation, no data) |
| 7 Viscosity solutions | one caption | missing in practice |
| 8 BSDEs | ch 9 | covered (one experiment), thin on theory |
| 9 Mean-field games | ch 9 | thin (no picture, no computation) |
| 10 RL: PPO on Merton vs closed form | ch 9 | covered, one seed, no replay, no baseline |
| (not in syllabus) transaction costs, consumption, martingale method | – | **missing**; core in every control text (added as items below) |

### (b) Textbook sections → chapter of the new plan

Chapter numbers are the new plan's (§3). TOCs are from memory; ones marked *(TOC unverified)* need checking
against the book in the Phase-0 pass.

| Book · section | New chapter |
|---|---|
| Pham (2009) ch 1 stochastic analysis | Part 5 |
| Pham ch 2 control problems, financial examples | 3, 4 |
| Pham ch 3 classical approach: DPP, HJB, verification theorem, Merton, investment–consumption | 3, 4, 6, 7 |
| Pham ch 4 viscosity approach (definition, comparison, superreplication under constraints) | 5 (constraints: Part 9 note) |
| Pham ch 5 optimal switching/stopping, free boundary, smooth fit | 12, 13 (switching: README only) |
| Pham ch 6 BSDEs and control (incl. reflected BSDE ↔ American) | 15 (reflected: mentioned in 13, 15) |
| Pham ch 7 martingale and convex-duality methods | 7 (duality for incomplete markets: README pointer to Kramkov–Schachermayer, absent) |
| Touzi (2013) ch 2 control and DP; ch 3 optimal stopping; ch 4 verification examples *(TOC unverified)* | 3, 4, 12 |
| Touzi ch 5–6 viscosity solutions and the DPE in the viscosity sense | 5 |
| Touzi ch 7–8 stochastic target problems | absent → README: superhedging is Part 9; noted as dropped |
| Touzi ch 9–11 BSDEs, quadratic BSDEs, probabilistic numerics | 15 (quadratic: README pointer) |
| Touzi ch 12 finite differences (Tourin) | 5 (monotone schemes), Part 16 |
| Karatzas–Shreve *Methods* ch 1 Brownian market | Part 9 |
| K–S *Methods* ch 3 single-agent consumption/investment (martingale method) | 6, 7 |
| K–S *Methods* ch 4 equilibrium | Part 23 |
| K–S *Methods* ch 6 constrained consumption/investment | 4 (floor), 7 (pointer) |
| K–S *Brownian Motion* §2.6, ch 2 optional sampling (stopping) | 12 |
| Björk (4th ed.) "Stochastic optimal control" chapter: HJB, verification, linear regulator, optimal consumption–investment, mutual-fund theorems; "martingale approach to optimal investment"; "optimal stopping" *(chapter numbers unverified)* | 4, 6, 7, 12 (LQ regulator: used in 16) |
| Merton *Continuous-Time Finance* (1990) ch 4 (1969 paper), ch 5 (1971 paper) *(other chapter numbers unverified)* | 6, 7 |
| Øksendal ch 10 optimal stopping; ch 11 stochastic control | 12, 13; 3, 4 |
| Bertsekas *DP and Optimal Control* I: DP algorithm; perfect-state-information problems (LQ, dynamic portfolio analysis, optimal stopping); infinite horizon; approximate DP *(numbering unverified)* | 3, 12, 17 |
| Sutton–Barto (2nd ed.) ch 3 MDPs, 4 DP, 6 TD, 13 policy gradient | 3, 17 (AI Part 26 teaches 2–13 in full) |
| Back *Asset Pricing and Portfolio Choice* ch 1 utility; ch 2 portfolio choice and SDFs; dynamic-programming chapter; ch 14 continuous-time portfolio choice | 2, 6, 3, 6–7 |
| Carmona–Delarue vol I ch 1 MFG by examples (finance); ch 3–4 MFG and FBSDEs; ch 6 McKean–Vlasov control *(TOC partly unverified)* | 16 (ch 6: README) |
| Shreve I ch 4, Shreve II ch 8 American securities | 12, 13 (pricing in Parts 10, 16) |
| Topics checked for completeness: utility theory **2**; Bellman/HJB **3, 4**; verification **4**; viscosity **5**; Merton **6**; consumption **7**; Davis–Norman **8**; Kelly **9, 10**; stopping **12, 13**; MFG **16**; RL **17** | |

### (c) READING.md papers (Part 8)

| Paper | Now | New plan |
|---|---|---|
| von Neumann–Morgenstern 1944 | on screen | ch 2: axioms card |
| Kelly 1956 | on screen | ch 9 |
| Bellman 1957 | on screen | ch 3 |
| Breiman 1961 | mentioned | ch 9: proof sketch on screen |
| Ellsberg 1961 | on screen | ch 14 |
| Pratt 1964; Arrow 1965 | on screen | ch 2: derived |
| Merton 1969; 1971 | 1969 on screen; 1971 cited only | ch 6; ch 7 (consumption rule derived) |
| Samuelson 1979 | on screen | ch 11 |
| Kahneman–Tversky 1979; TK 1992 | on screen | ch 14 |
| Crandall–Lions 1983 | one caption | ch 5 |
| Gilboa–Schmeidler 1989 | on screen | ch 14 |
| Davis–Norman 1990 | **absent** | ch 8 |
| Pardoux–Peng 1990 | on screen | ch 15 |
| El Karoui–Peng–Quenez 1997 | on screen | ch 15 |
| Hansen–Sargent 2001 | mentioned | ch 14 (+ Maenhout derived) |
| Huang–Malhamé–Caines 2006 | mentioned | ch 16 |
| Thorp 2006 | **absent** (the book is cited instead) | ch 18: primary source for the facts |
| Lasry–Lions 2007 | mentioned (as 2006) | ch 16 (CRAS notes 2006, JJM 2007) |
| Schulman et al. 2017 | on screen | ch 17 |
| Peters 2019 | on screen | ch 11 |

**Add to READING.md** (all used on screen below): Snell 1952 (Trans. AMS); Allais 1953 (*Econometrica*); Dynkin
1963; McKean 1965 (perpetual American put); Magill–Constantinides 1976 (*JET*); Karatzas–Lehoczky–Shreve 1987
(*SIAM J. Control Optim.*); Cox–Huang 1989 (*JET*); Barles–Souganidis 1991 (*Asymptotic Analysis*); Grossman–Zhou
1993 (*Math. Finance*); Shreve–Soner 1994 (*Ann. Appl. Probab.*); Benartzi–Thaler 1995 (*QJE*); Bergman 1995 (*RFS*);
Rabin 2000 (*Econometrica*); Almgren–Chriss 2001 (*J. Risk*); Anderson–Hansen–Sargent 2003 (*JEEA*); Janeček–Shreve
2004 (*Finance Stoch.*); Rogers 2004 (transaction-cost asymptotics, *(title unverified)*); Maenhout 2004 (*RFS*);
Benter 1994 (in Hausch–Lo–Ziemba, *Efficiency of Racetrack Betting Markets*); Gobet–Lemor–Warin 2005 (*AAP*);
Almgren–Thum–Hauptmann–Li 2005 (*Risk* 18); Carlin–Lobo–Viswanathan 2007 (*JF*); MacLean–Thorp–Ziemba 2011
(book); Haghani–Dewey 2016 (arXiv 1701.01427); Peters–Gell-Mann 2016 (*Chaos*); Moreira–Muir 2017 (*JF*);
Cardaliaguet–Lehalle 2018 (*Math. Financ. Econ.*; arXiv 1610.09904); Han–Jentzen–E 2018 (*PNAS*);
Lacker–Zariphopoulou 2019 (*Math. Finance*; arXiv 1703.07685); Wang–Zariphopoulou–Zhou 2020 (*JMLR*);
Doctor–Wakker–Wang 2020 (*Nature Physics*); Meder et al. 2021 (*PLoS Comput. Biol.*; arXiv 1906.04652); and the
frontier papers of ch 19. Journals not opened in this pass are given from memory: *(verify venue)*.

---

## 3. The new chapter list (20 manifest entries, ≈ 60 min)

Word targets are ≈ 140 words a minute. The **Lab** chapters (3, 8, 12, 16, plus PPO in 17) show a House function
as a `code_block` (`explainer/ai/viz.py`, at most 12 lines) and then run it, with the output drawn live from the
cached trace. **Replay** chapters use the AI 21 `replay`/`measure` pattern: a `ValueTracker` scrubs the
checkpoints with the curve, and seeds are drawn as `band`s. Colours follow `common.py` (KELLY, OVER, UNDER, VALUE).
New House functions go in `explainer/quant/house/control.py`, each tested in `tests/test_quant_house.py` against a
closed form.

### H · How much to bet, and how we got here (`s01_hook`, 3.5 min; deepened)
- **Goal:** the question (sizing), the stakes (30% of trained players went bust), and the era.
- **Beats:** (1) Haghani–Dewey game. (2) **Live:** 5 × 40 players per fraction (10%, 20%, 40%, 100%) as
  dots on a log-wealth axis, flipping together, 300 flips in 12 s; the 100% column collapses to the floor and the
  20% column climbs to the $250 cap. The finished table follows, as now. (3) Kelly's curve g(f), as now.
  (4) **New, how we got here (75 s):** the `timeline` strip lit in order: Bernoulli 1738, vNM 1944, Kelly 1956,
  Bellman 1957, Merton 1969/71, Samuelson 1979, Kahneman–Tversky 1979, Crandall–Lions 1983, Davis–Norman 1990,
  Pardoux–Peng 1990, Lasry–Lions/HMC 2006, PPO 2017. One sentence each; the gold ideas stack into a tree with
  "maximize expected utility" at the root. (5) Objectives card.
- **Pause-and-predict:** "Before the simulation: which column goes bust most, 40% or 100%? And does 40% grow at all?"
- **Compute:** `coin_live` (paths for 160 players × 4 fractions, seeded; seconds).

### 1 · Utility and risk aversion (`s02_utility`, 3.0 min; deepened)
- **Goal:** why a consistent chooser maximizes E u(W); what the curvature measures; the Arrow–Pratt premium derived.
- **Beats:** Bernoulli's St Petersburg in one line → the vNM axioms card (completeness, transitivity, continuity,
  independence) → **signature visual:** the gamble as two weights hung on the utility curve, joined by a chord. The
  chord's midpoint drops a horizontal line to the curve, and that point is the CE. A γ slider (ValueTracker 0.5 → 30)
  bends the CRRA curve live, and the CE slides left toward 50, its readout updating (the existing table becomes the
  trace of the slider). → Arrow–Pratt derivation → Rabin's calibration as the warning that expected utility of
  wealth can't explain small-stakes aversion (one sentence; prospect theory in ch 14).
- **Derivation (ladder):**
  - $\mathbb E\,u(W+\tilde\varepsilon)=u(W-\pi)$ — definition of the risk premium for a fair gamble $\tilde\varepsilon$
  - $\mathbb E\,u(W+\tilde\varepsilon)\approx u(W)+\tfrac12\sigma^2u''(W)$ — Taylor to second order, $\mathbb E\tilde\varepsilon=0$
  - $u(W-\pi)\approx u(W)-\pi u'(W)$ — Taylor to first order, π small
  - $\pi\approx\tfrac12\sigma^2\big(-u''(W)/u'(W)\big)=\tfrac12\sigma^2A(W)$ — equate
  - $\pi/W\approx\tfrac12\gamma\,(\sigma/W)^2,\ \gamma=-Wu''/u'$ — relative risk aversion; CRRA ⇒ γ constant
- **Experiment:** CE table (existing) plus a check of the approximation: for ±10 and ±50 gambles, exact premium against
  ½γσ²/W. Expected: within 1% at ±10, 13.4 vs 12.5 at ±50 for γ = 1.
- **Pause-and-predict:** "Γ = 3, the 50-or-150 flip: will you pay more or less than 20 to avoid it?" (more: CE 67.1).

### 2 · Bellman's principle: solving backwards (`s03_bellman`, 3.0 min; **Lab 1**, replay)
- **Goal:** the principle of optimality and backward induction; CRRA's homogeneity makes the policy myopic.
- **Beats:** a 3-period tree (a binomial stock) with values flowing back node by node, the best fraction picked at
  each node from a little parabola → the general recursion → homogeneity: guess $V_n(w)=v_n w^{1-\gamma}/(1-\gamma)$,
  and the max no longer depends on w → **Lab 1:** `control.bellman_merton` as code (sketch below) → run.
  **Replay (signature visual):** the 3D value surface V(t, w) builds backward from year 10, one slab a month,
  driven by a ValueTracker. At the moving slab, a small inset shows E[V_{n+1}] as a function of π at w = 1, its peak
  dot tracing the policy line on the floor. Then the floor case (existing surface) is rebuilt the same way, so the
  policy surface "grows" toward the deadline. The existing slice plot and the 0.005 gap close the chapter.
- **Lab 1 code (≤12 lines):**
  ```python
  def bellman_merton(mu, r, sig, gam, T, steps, w, pis, z, q):   # z, q: Gauss–Hermite nodes, weights
      dt = T / steps;  V = crra(w, gam)                           # terminal utility
      R = np.exp((mu - sig**2/2)*dt + sig*np.sqrt(dt)*z) - 1      # stock return at each node
      for n in reversed(range(steps)):
          W1 = w[:, None, None] * (1 + r*dt + pis[None, :, None]*(R - r*dt))
          EV = (interp(w, V, W1) * q).sum(-1)                      # E[V_{n+1}] for every (w, pi)
          k = EV.argmax(1); V = EV[np.arange(len(w)), k]           # best fraction at every wealth
          policy[n] = pis[k]
      return V, policy
  ```
- **Derivation:** $V_n(w)=\max_\pi\mathbb E[V_{n+1}(w(1+r\Delta+\pi(R-r\Delta)))]$ (principle of optimality);
  substitute the CRRA guess ⇒ $v_n=v_{n+1}\max_\pi\mathbb E[(1+r\Delta+\pi(R-r\Delta))^{1-\gamma}]/(1-\gamma)$ (w factors out)
  ⇒ π* is the same at every w and n (myopia).
- **Compute:** `bellman_sweep`: value and policy at every 6th step, with and without the floor (existing solver; ~1 min).
- **Expected:** 61.7% at every step (as now); floor gap ≤ 0.005.
- **Pause-and-predict:** "As the deadline nears with wealth just above the floor, does the stock fraction rise or fall?"

### 3 · The HJB equation and the verification theorem (`s04_hjb`, 3.2 min; new)
- **Goal:** derive the HJB from the DPP and Itô, solve Merton's by the ansatz, and know why the guess is right.
- **Signature visual:** **the sup as a moving parabola.** Under the 3D V(t, w), a 2D panel shows the Hamiltonian
  $H(\pi)=(r+\pi(\mu-r))wV_w+\tfrac12\pi^2\sigma^2w^2V_{ww}$ as a downward parabola in π. A dot runs along w. With no
  floor the parabola rescales but its peak stays at 61.7%, a vertical line that never moves. Switch the floor on and
  the peak slides toward 0 as w falls to the floor. "The policy is the argmax of a parabola at every point."
- **Derivation:**
  - $V(t,x)=\sup_\pi\mathbb E[V(t+h,X_{t+h})]$ — DPP over [t, t+h]
  - $V(t+h,X_{t+h})=V+\int_t^{t+h}(V_s+\mathcal L^{\pi}V)\,ds+\int_t^{t+h}V_x\pi\sigma X\,dW$ — Itô
  - $0=\sup_\pi\mathbb E\big[\tfrac1h\int_t^{t+h}(V_s+\mathcal L^\pi V)ds\big]$ — the dW integral has mean 0; divide by h
  - $0=V_t+\sup_\pi\{(r+\pi(\mu-r))xV_x+\tfrac12\pi^2\sigma^2x^2V_{xx}\}$ — h → 0; $V(T,x)=u(x)$
  - $\pi^*=-\frac{(\mu-r)V_x}{\sigma^2xV_{xx}}$ — FOC (the parabola's vertex; needs $V_{xx}<0$)
  - $V=f(t)\frac{x^{1-\gamma}}{1-\gamma}\Rightarrow f'+(1-\gamma)\big(r+\tfrac{\theta^2}{2\gamma}\big)f=0,\ \theta=\tfrac{\mu-r}\sigma$ — ansatz; $xV_x=(1-\gamma)V,\ x^2V_{xx}=-\gamma(1-\gamma)V$
  - **Verification theorem card:** if a $C^{1,2}$ function w solves the HJB with $w(T,\cdot)=u$, then for any admissible π:
    $u(X_T^\pi)=w(t,x)+\int(w_s+\mathcal L^\pi w)ds+M_T\le w(t,x)+M_T$ — Itô, and the HJB says the drift is ≤ 0
    ⇒ $\mathbb E u(X^\pi_T)\le w(t,x)$ — M is a martingale (the localisation and integrability condition is stated on the card)
    ⇒ equality for π*, so $w=V$ and π* is optimal.
- **Experiment:** `hjb_fd`: an implicit finite-difference policy-iteration solve of the HJB on (t, log x) (200 × 400),
  against the closed form f(t). Expected: policy 61.7% ± 0.1 pp, relative value error below 1e-3 (target, asserted in
  compute). The run shows each policy-iteration pass converging (2–4 passes per step).
- **Pause-and-predict:** "Double σ. What happens to the Merton fraction?" (falls 4×).

### 4 · When the value function has kinks: viscosity solutions (`s05_viscosity`, 2.6 min; new)
- **Goal:** why HJB solutions need not be smooth, what a viscosity solution is, and why monotone schemes converge.
- **Beats:** kinks arise from constraints, stopping and max(·,·), as in the floor's value at the deadline →
  toy: $|u'|=1$ on (−1, 1), $u(\pm1)=0$: infinitely many zig-zags satisfy it almost everywhere → **signature
  visual:** smooth test functions φ (parabolas) slide in to touch each candidate from above and below. At a ∧ kink
  (local max) nothing smooth touches from below, and the touches from above give $|\varphi'|\le1$, so the
  subsolution test holds. At a ∨ kink, $\varphi$ from below has slope 0, which violates the supersolution test, and
  the kink turns red. Every ∨ kink fails, and only 1 − |x| survives. Definition card (sub/super via touching) →
  comparison principle ⇒ uniqueness (Crandall–Lions 1983; Fleming–Soner as the reference) → Barles–Souganidis:
  monotone + stable + consistent ⇒ convergence.
- **Derivation:** definition only: u is a subsolution if $u-\varphi$ has a local max at $x_0$ ⇒ $F(x_0,u,\varphi',\varphi'')\le0$, and a supersolution if a local min ⇒ $\ge0$. Here $F=|p|-1$ (with the sign convention stated on the card).
- **Experiment:** `viscosity`: march $u_t+|u_x|=1$ to steady state on 21/81/321 nodes. **Live:** the upwind (Godunov)
  profile rises into the tent while the central-difference profile develops odd–even teeth that grow. Prototype:
  upwind error 0.0 on every grid (exact 1 − |x|); central max error 2.5e6 (21 nodes) to 1.5e131 (321 nodes) by t = 6.
  Second panel: the floor-Merton grid solver from ch 2 is monotone, and that is why it converged.
- **Pause-and-predict:** "Which zig-zag will the computer find?"

### 5 · Merton's problem (`s06_merton`, 3.0 min; deepened, **live simulation**)
- **Goal:** the answer, what it means in practice (rebalancing, two-fund separation), and its fragile input.
- **Beats:** π* recap from ch 3 → **signature visual:** a two-colour glass (stock above, bond below) beside a
  live GBM path. When the stock rises the stock layer swells, and a rebalance arrow pours it back to 61.7% (sell
  winners, buy losers). A second glass, buy-and-hold, drifts. → multi-asset: $\pi^*=\frac1\gamma\Sigma^{-1}(\mu-r\mathbf 1)$,
  so every investor holds the same risky mix in different amounts (mutual-fund theorem; Part 30) → the US data and
  the ±2 SE bars (existing) → Merton's 1980 point that drift is hard to estimate.
- **Experiment:** existing `merton_us`; plus `rebalance_sim`: 2,000 30-year paths (μ 8%, r 2%, σ 18%), constant mix vs buy-and-hold
  from 61.7%: the CE growth for γ = 3 (expected: constant mix ahead by a few tenths of a percent a year (to be
  computed); branch narration on the sign).
- **Pause-and-predict:** "Stocks just fell 20%. Does Merton buy or sell?"

### 6 · Consumption, and the martingale method (`s07_consumption`, 2.8 min; new)
- **Goal:** Merton 1971's consumption rule, and the static (Cox–Huang/KLS) view: the investor buys a payoff.
- **Derivation (consumption):**
  - $\rho V=\sup_{c,\pi}\{u(c)+(rx+\pi x(\mu-r)-c)V_x+\tfrac12\pi^2\sigma^2x^2V_{xx}\}$ — stationary HJB, infinite horizon
  - $u'(c^*)=V_x$ — FOC in c (eat until the marginal utility of eating equals that of saving)
  - $V=A\frac{x^{1-\gamma}}{1-\gamma}\Rightarrow c^*=A^{-1/\gamma}x$ — ansatz
  - $\frac{c^*}{x}=\nu=\frac{\rho-(1-\gamma)(r+\theta^2/(2\gamma))}{\gamma}$ — substitute, match the coefficients of $x^{1-\gamma}$ (need ν > 0)
  - finite horizon: $c^*/x=\nu/(1-e^{-\nu(T-t)})$ — same steps, with $f(t)$
  - Worked: ρ 3%, γ = 3 ⇒ ν = 3.57% a year; γ = 1 ⇒ ν = ρ = 3.0%.
- **Derivation (martingale method):**
  - $\xi_T=e^{-(r+\theta^2/2)T-\theta W_T}$ — state-price density (Part 9 preview)
  - $\max\mathbb E\,u(X_T)$ s.t. $\mathbb E[\xi_TX_T]=x$ — any payoff is attainable (complete market)
  - $u'(X_T)=y\xi_T\Rightarrow X_T=(y\xi_T)^{-1/\gamma}$ — pointwise Lagrangian
  - $X_T\propto e^{(\theta/\gamma)W_T}=e^{\pi^*\sigma W_T}\propto S_T^{\pi^*}$ — the Merton investor owns a power claim on the stock
- **Signature visual:** a scatter of terminal states, with state price ξ on the x-axis and terminal wealth on y.
  Points from 2,000 simulated constant-mix paths land exactly on the curve $(y\xi)^{-1/\gamma}$ as they are simulated.
  The γ slider steepens or flattens the curve ("buy wealth where it is cheap"). Then a life-cycle strip shows the
  consumption rate climbing to 1/(T − t) near the end.
- **Experiment:** `martingale_check`: daily-rebalanced paths vs the power-claim formula; expected agreement to within
  discretization error (target max relative error < 0.5%; to be computed).
- **Pause-and-predict:** "A more patient investor (lower ρ) with γ = 3: does she consume more or less of her wealth?"

### 7 · Transaction costs: the no-trade wedge (`s08_costs`, 3.2 min; new, **Lab 2**)
- **Goal:** with proportional costs, never trade inside a band; trade only at its edges; the band ∝ ε^{1/3}.
- **Signature visual:** the (bond x, stock y) wealth plane. Merton is a ray from the origin. With costs it opens into
  a **wedge**. A wealth dot diffuses live, untouched inside the wedge and pushed back at the edges by tiny trades
  (a flash and a cost tick), a reflected diffusion. A turnover counter runs for the wedge and for the always-on-the-ray
  investor side by side. Then a cost slider widens the wedge as ε^{1/3}.
- **Derivation:**
  - buy: $dx=-(1+\varepsilon)dL,\ dy=dL$; sell: $dx=(1-\varepsilon)dU,\ dy=-dU$ — controls are cumulative trades (singular control)
  - $\max\{\mathcal L V,\ V_y-(1+\varepsilon)V_x,\ (1-\varepsilon)V_x-V_y\}=0$ — HJB variational inequality: in each region one term binds
  - $V(x,y)=(x+y)^{1-\gamma}v(\pi),\ \pi=\frac y{x+y}$ — homogeneity reduces to one state
  - $\pi_\pm\approx\pi^*\pm\big(\tfrac{3}{2\gamma}\pi^{*2}(1-\pi^*)^2\varepsilon\big)^{1/3}$, welfare loss $O(\varepsilon^{2/3})$ — small-cost asymptotics (Janeček–Shreve 2004; Rogers 2004; check the constant against the paper)
  - Davis–Norman 1990 constructed the solution; Shreve–Soner 1994 proved it with viscosity solutions (link to ch 4).
- **Lab 2 code:**
  ```python
  def no_trade_band(mu, r, sig, gam, eps, dt, steps, grid, z, q):
      R = np.exp((mu - sig**2/2)*dt + sig*np.sqrt(dt)*z);  h = np.ones_like(grid)
      for n in range(steps):                                     # h(pi) = E[(W_T/W)^(1-gam)]
          G = grid[:, None]*R + (1 - grid[:, None])*np.exp(r*dt)  # gross return from post-trade pi'
          C = (G**(1-gam) * np.interp(grid[:, None]*R/G, grid, h) * q).sum(1)
          J = (1 - eps*abs(grid[None] - grid[:, None]))**(1-gam) * C[None]
          k = J.argmin(1); h = J[np.arange(len(grid)), k]       # gam > 1: minimize h
      stay = grid[k] == grid
      return grid[stay].min(), grid[stay].max()
  ```
- **Experiment (prototype run, γ = 3, μ 8%, r 2%, σ 18%, monthly, 30 years, 601-point grid, 1.4 s per ε):**

  | ε | DP band | half-width | asymptotic half-width |
  |---|---|---|---|
  | 0.1% | 59.4–64.0% | 2.3 pp | 3.0 pp |
  | 0.5% | 57.2–66.2% | 4.5 pp | 5.2 pp |
  | 1% | 55.8–67.8% | 6.0 pp | 6.5 pp |
  | 2% | 54.0–69.6% | 7.8 pp | 8.2 pp |

  Monthly monitoring narrows the band at small ε, and the narration says so. `costs_sim` (γ = 1, quarterly, ε = 1%):
  band 158–202%. The band grows 0.26% a year faster net of costs than rebalancing to Merton every quarter, and
  turns over 10% a year against 44%.
- **Pause-and-predict:** "Costs double. Does the band double?" (no: × 2^{1/3} ≈ 1.26; the table shows 4.5 → 6.0 pp).

### 8 · Kelly and Breiman (`s09_kelly`, 3.0 min; deepened, **live paths**)
- **Goal:** derive the Kelly fraction, prove that it eventually beats everything, and measure it on history.
- **Beats:** Kelly 1956 card (Shannon showed Thorp the paper at MIT in 1960, per Thorp 2006) → derivations →
  **signature visual:** three wealth fans (½, 1, 2 × Kelly; 60 paths each) growing live on a log axis for 40 years,
  with each fan's median line in bold and a side density filling. The 2× fan's median drifts flat while its top
  paths explode. At the end the fans freeze, and the "time average" lines (slopes = g(f)) are laid over them. Then
  the US realized-growth parabola (existing), and Breiman's race.
- **Derivation:**
  - $g(f)=p\log(1+f)+q\log(1-f)$; $g'(f)=\frac p{1+f}-\frac q{1-f}=0\Rightarrow f^*=p-q$ — coin
  - $d\log W=(r+f(\mu-r)-\tfrac12f^2\sigma^2)dt+f\sigma dW$ — Itô on log W
  - $f^*=\frac{\mu-r}{\sigma^2}$, $g^*-r=\tfrac12\theta^2$ — vertex of the parabola (= Merton at γ = 1)
  - $\tfrac1n\log W_n(f)\to g(f)$ a.s. — strong law of large numbers on i.i.d. log-returns
  - $g(f^*)>g(f)\Rightarrow W_n(f^*)/W_n(f)=e^{n(g(f^*)-g(f))+o(n)}\to\infty$ a.s. — Breiman 1961 (fixed-fraction rivals; the general case is stated)
- **Experiment:** `breiman_race`: 10,000 paths of Kelly against ½ and 2× Kelly; P(Kelly ahead) against years
  (existing `samuelson` gives 64/73/87% at 10/30/100 years against the γ = 3 fraction); plus existing `kelly_us`.
- **Pause-and-predict:** "At 2× Kelly, what is the median growth rate?" (r: zero excess growth).

### 9 · Fractional Kelly, estimation risk, and LTCM (`s10_fractional`, 3.2 min; deepened; crisis file)
- **Goal:** why practitioners bet a fraction; what an overestimated edge does; leverage beyond Kelly as a crisis.
- **Derivation:** $g(cf^*)-r=(2c-c^2)(g^*-r)$ — substitute $f=cf^*$ into the parabola; if the true edge is the
  estimate divided by k, betting full Kelly on the estimate is k × Kelly on the truth, and k = 2 earns nothing:
  Benter's warning, quoted (below).
- **Signature visual:** the growth parabola with a **fuzzy vertex**: the bootstrap cloud of best fractions
  (existing `kelly_us` bootstrap, 116–302%) as a horizontal blur under the peak. A "bet" marker at full Kelly on the
  estimate slides into the falling side for the low draws, coloured OVER. Half Kelly stays on the flat top for nearly
  every draw. Then the existing drawdown table (10/80/100% chance of halving), then LTCM: crisis card, and the Kelly
  leverage line falling from 100 to 11 as a vol slider triples σ, with 28:1 crossing from safe to ruinous.
- **Experiment:** existing `fractional`, `kelly_us`, `ltcm`; new `edge_error`: growth of full and half Kelly when the
  edge is mis-estimated by factors 0.5–3 (closed form plus 2,000 paths). Expected: full Kelly's excess growth hits 0 at
  k = 2 (Benter), half Kelly's at k = 4.
- **Pause-and-predict:** "You estimate Sharpe 1; the truth is 0.5. Which grows faster: full or half Kelly on your estimate?"

### 10 · Samuelson's objection, and ergodicity (`s11_samuelson`, 2.6 min; light deepening)
- Keep the existing content. Add the CE derivation:
  $\log W_T\sim N(mT,s^2T)\Rightarrow \mathrm{CE}=\big(\mathbb E W_T^{1-\gamma}\big)^{\frac1{1-\gamma}}=W_0e^{(m+\frac12(1-\gamma)s^2)T}$
  (normal mgf), so the CE rate is $r+f(\mu-r)-\tfrac12\gamma f^2\sigma^2$, maximized at Merton, not at Kelly.
- **Live:** Peters' coin, 100,000 players as a histogram on a log axis, flipping for 60 rounds, with the ensemble
  mean (rising) and the median (falling) traced together. Add Toda (2023) to the "controversy" panel, and Meder et
  al. (2021): subjects' risk aversion moved toward the time-optimal value under multiplicative dynamics.
- **Pause-and-predict:** "What fraction of your wealth should you stake on Peters' coin?" (25%; problem 5).

### 11 · Optimal stopping: the Snell envelope (`s12_snell`, 3.0 min; new; **Lab 3**)
- **Goal:** the value of the right to stop is the smallest supermartingale above the payoff, and you stop where they meet.
- **Signature visual:** **a rope over pegs.** For a symmetric random walk on {0, …, 20}, absorbed at the ends,
  the payoff g is a jagged skyline of pegs. Value iteration is replayed with a ValueTracker: from U = g, each sweep
  replaces U by max(g, average of neighbours), and the curve lifts and smooths until it is the **least concave
  majorant**, a rope pulled taut over the highest pegs. "Stop" lights where rope touches peg; "continue" where it
  hangs above. The secretary problem (existing) follows as a 30-second example.
- **Derivation:**
  - $U_N=g_N,\ U_n=\max(g_n,\mathbb E[U_{n+1}\mid\mathcal F_n])$ — backward induction
  - U is a supermartingale with $U\ge g$, and any supermartingale $\tilde U\ge g$ has $\tilde U\ge U$ — induction from N
  - $\tau^*=\min\{n:U_n=g_n\}$ and $U_{n\wedge\tau^*}$ is a martingale ⇒ $U_0=\mathbb E\,g_{\tau^*}$ — on $\{n<\tau^*\}$ the max picks the continuation term
  - random walk: $\mathbb E[U_{n+1}\mid S_n=x]=\tfrac12(U(x-1)+U(x+1))$ ⇒ the stationary U is the smallest function ≥ g with $U(x)\ge$ the average of its neighbours, i.e. concave (Dynkin–Yushkevich)
- **Lab 3 code:** `control.snell_envelope(g, steps)`: 6 lines (loop `U = np.maximum(g, 0.5*(U[:-2] + U[2:]))` with
  absorbing ends), then `concave_majorant(g)` as a 4-line check (`scipy.spatial.ConvexHull` upper hull). Run live:
  the sweeps play, and an `assert` line turns green when the two agree to 1e-10.
- **Compute:** `snell_rw` (sweeps saved every 5; seconds).
- **Pause-and-predict:** "Which pegs will the rope touch?"

### 12 · Free boundaries: smooth fit and the American put (`s13_smoothfit`, 2.6 min; new)
- **Goal:** in continuous time the stop/continue boundary is unknown and found by smooth fit.
- **Derivation (perpetual put, McKean 1965):**
  - $\tfrac12\sigma^2S^2V''+rSV'-rV=0$ in the continuation region — Itô and no-arbitrage for the held option
  - $V=AS^{-\beta},\ \beta=2r/\sigma^2$ — power ansatz, the bounded root
  - $V_b(S)=(K-b)(S/b)^{-\beta}$ for an exercise level b — value matching at b
  - $\frac{d}{db}(K-b)b^{\beta}=0\Rightarrow b^*=\frac{\beta K}{1+\beta}$ — choose b to maximize ⇔ $V'(b^*)=-1$ (smooth fit)
  - r 5%, σ 30%, K 100 ⇒ β = 1.11, b* = 52.6, V(100) = 23.2.
- **Signature visual:** a b slider sweeps the family $V_b$. Each candidate meets the payoff (K − S)⁺ at b with
  a visible kink angle (a protractor readout). The value at S = 100 rises then falls, and the maximum is exactly
  where the angle closes to 0, the curve kissing the payoff. Then the finite-maturity boundary (existing tree) and
  the variational inequality $\min(-V_t-\mathcal LV,\ V-g)=0$, as a link to ch 4 and to the reflected BSDE in ch 14.
- **Experiment:** `perpetual_put`: closed form vs a 40-year CRR tree. Expected: tree boundary → 52.6, value → 23.2
  (within 0.1); the existing `american` 9.87 / 9.35.
- **Pause-and-predict:** "Rates rise. Does the exercise boundary move up or down?" (up: β grows, b* → K).

### 13 · How people decide: prospect theory and ambiguity (`s14_behaviour`, 3.6 min; deepened)
- **Goal:** where expected utility fails empirically (Allais, Rabin, Ellsberg), the replacements, and one data test.
- **Beats:** Allais's paradox (independence fails) → CPT: value $v(x)=x^\alpha$, $-\lambda(-x)^\alpha$; weighting
  $w(p)=p^\delta/(p^\delta+(1-p)^\delta)^{1/\delta}$ (TK 1992: α 0.88, λ 2.25, δ 0.61 gains / 0.69 losses), applied
  rank-dependently → **signature visual:** the kinked S-curve with a **movable reference point**. A stock's
  return histogram slides under it. Then a horizon slider (1 → 36 months) widens the return distribution, and the
  CPT value of stocks climbs past that of T-bills. → Ambiguity: Ellsberg urn, maxmin (Gilboa–Schmeidler), Hansen–Sargent
  → Maenhout derivation (below) → **visual:** a fan of plausible drifts, and nature's worst-case drift sliding down
  as the investor's π rises; the robust π is where the two lines cross.
- **Derivation (robust Merton, Maenhout 2004):**
  - $0=V_t+\sup_\pi\inf_h\{(r+\pi(\mu-r)+\pi\sigma h)xV_x+\tfrac12\pi^2\sigma^2x^2V_{xx}+\frac{h^2}{2\Psi}\}$ — nature distorts the drift by $\pi\sigma h$ at an entropy cost
  - $h^*=-\Psi\pi\sigma xV_x$ — inner minimization (a parabola in h)
  - $\Psi=\theta/((1-\gamma)V)$ — Maenhout's scaling (keeps the problem homothetic)
  - $\Rightarrow\ \pi^*=\frac{\mu-r}{(\gamma+\theta)\sigma^2}$ — the outer FOC; doubt acts as extra risk aversion
- **Experiments:** `myopic_loss` (Benartzi–Thaler 1995 redone on French 1926–2020, CPT with TK 1992 parameters,
  overlapping windows). Prototype: stocks' CPT value is below bills' up to 15 months and above it from 18
  (15 mo: 0.055 vs 0.059; 18 mo: 0.075 vs 0.070), a crossover at about 16–17 months (Benartzi–Thaler: about 1
  year, against bonds). Register with the trial counter. `robust_fraction`: θ chosen by detection-error probability
  $p=\Phi(-\tfrac{\Delta\mu\sqrt T}{2\sigma})$ over 94 years. My hand calculation (to be computed): p = 20% ⇒ θ ≈ 1.9,
  π ≈ 49%; p = 10% ⇒ θ ≈ 4.4, π ≈ 32%, against 79% for γ = 3 with no doubt.
- **Pause-and-predict:** "If you checked your portfolio every five years instead of every month, how much more in stocks would a loss-averse investor hold?"

### 14 · Backward SDEs (`s15_bsde`, 2.8 min; deepened, replay)
- **Goal:** the pricing equation solved backwards from the payoff for value and hedge; nonlinear pricing.
- **Derivation:**
  - $-dY=f(t,Y,Z)dt-Z\,dW,\ Y_T=\xi$ — definition; (Y, Z) adapted (Pardoux–Peng: unique if f is Lipschitz)
  - $f=-rY-\theta Z\Rightarrow Y_t=\mathbb E^{\mathbb Q}[e^{-r(T-t)}\xi\mid\mathcal F_t]$ — linear generator = Black–Scholes; $Z=\sigma S\Delta$
  - $f=-rY-\theta Z-(R-r)(Y-Z/\sigma)^-$ — borrow at R, lend at r (Bergman); comparison theorem ⇒ price lies between the BS prices at r and at R
  - scheme: $Z_n\approx\mathbb E[Y_{n+1}\Delta W_n\mid S_n]/\Delta t$, $Y_n\approx\mathbb E[Y_{n+1}\mid S_n]+f(Y_n,Z_n)\Delta t$ — regression on basis functions (Gobet–Lemor–Warin)
- **Signature visual (replay):** forward paths fan out. Then, step by step backwards (ValueTracker over n), the
  scatter of $(S_n, Y_{n+1})$ is drawn and the regression curve snaps through it. It becomes $Y_n$, and the next
  scatter forms. At the end $Y_0$ lands between the two BS lines, beside the existing convergence plot.
- **Compute:** existing `bsde` plus `bsde_replay` (regression curves at every 5th step, 20k paths; ~1 min).
- **Pause-and-predict:** "Will the two-rate price be closer to BS at 1% or at 6%?"

### 15 · Mean-field games: the crowd that sells together (`s16_mfg`, 3.0 min; new; **Lab 4**)
- **Goal:** the MFG fixed point (HJB backward, crowd forward), shown on a liquidation game with a closed form.
- **Model:** each of N traders sells q₀ over [0, T]; price drift $-\kappa\bar v(t)$ (permanent impact of the
  average selling rate); temporary cost $\eta v^2$; risk penalty $\phi Q^2$.
- **Derivation:**
  - $d(X+QS)=-\eta v^2dt-\kappa\bar vQ\,dt+Q\sigma dW$ — mark-to-market wealth; own impact integrates to a constant
  - minimize $\int_0^T(\eta Q'^2+\kappa m(t)Q+\phi Q^2)dt$, $m=\frac1N\sum_{j\ne i}v_j$ — expected cost
  - $2\eta Q''=\kappa m+2\phi Q$ — Euler–Lagrange
  - symmetric equilibrium $m=-\frac{N-1}NQ'$ ⇒ $2\eta Q''+\kappa\frac{N-1}NQ'-2\phi Q=0$ — consistency (the fixed point)
  - φ = 0: $Q'(t)\propto e^{-at}$, $a=\frac{\kappa(N-1)}{2N\eta}$ — N = 1 is TWAP (Almgren–Chriss with no risk aversion); N → ∞ is the MFG: front-loaded
- **Signature visual:** two arrows of time. Each player's value/strategy curve runs right to left, and the crowd's
  inventory distribution (a histogram of 500 dots) runs left to right. **Fictitious play** is replayed: the crowd
  curve m_k(t) and the best response alternate until they lock. Then an **N slider** (1 → 2 → 10 → ∞) bends the
  liquidation curve from a straight line into an exponential race.
- **Lab 4 code:** `control.mfg_liquidation(N, kappa, eta, phi, T, iters)`: discretize the EL ODE as a tridiagonal
  solve given m, update `m = (1 - a)*m + a*best_response`, ≤ 12 lines. Run: residual printed per iteration,
  falling geometrically.
- **Expected:** share sold in the first fifth of the horizon at κT/(2η) = 2: TWAP 20%, N = 2: 28.7%, MFG: 38.0%
  (closed form). Fictitious play matches the closed form to < 1e-6 (to be computed; damping 0.5).
- **Also on screen:** HMC 2006 / Lasry–Lions 2006–07; the systems view (HJB + Fokker–Planck pair, existing ladder);
  Cardaliaguet–Lehalle 2018 (trade crowding); Carlin–Lobo–Viswanathan 2007 (predatory trading, the N-player version);
  Lacker–Zariphopoulou 2019: competition on relative performance makes agents hold more risk (CARA case).
- **Pause-and-predict:** "You know 9 other funds are selling the same stock this week. Sell faster or slower than alone?"

### 16 · Reinforcement learning on Merton's problem (`s17_rl`, 3.4 min; deepened; **training replay, Lab 5**)
- **Goal:** a learner that never sees the formula finds it; the noise problem; and costs, where no formula exists.
- **Beats:** MDP framing (state (t, w) or (t, π_pre); action π; reward = log growth net of cost) → policy gradient
  and the PPO clip (one ladder, AI 26 ch 8–9 referenced) → **Lab 5:** the 10-line core of `control.ppo_merton`
  (rollout, TD advantage, clipped loss) → **replay:** the learned policy heat map over (t, log w) and the
  mean-fraction curve scrubbed together through checkpoints (0, 10, 25, 50, 100, 200, 299), 5 seeds as a band, the
  discrete-time optimum 184% dashed. Baselines at equal evaluation: the DP policy and the closed form. →
  **costs:** PPO on the ε = 1% problem (state (t, π_pre), action = target fraction). Its policy is drawn as a
  target-vs-current map with the DP band (158–202%) outlined, the "do nothing" diagonal forming or not.
- **Derivation:** $\nabla J=\mathbb E[\nabla\log\pi_\theta(a\mid s)\,\hat A]$; $\hat A=r+V(s')-V(s)$ (one-step TD;
  keeps one step's noise); $L^{\rm clip}=\mathbb E\min(\rho\hat A,\mathrm{clip}(\rho,1\pm\epsilon)\hat A)$.
- **Experiments:** `ppo` × 5 seeds (existing settings; ~2.5 min each, single thread). `ppo_costs` × 5 seeds,
  300 iters × 1,024 ten-year quarterly episodes (~4 min each). **Narration branches**: if the learned band's edges
  are within ±15 pp of the DP's and its net growth beats quarterly-Merton rebalancing, say so; otherwise say the
  0.26%-a-year signal sits under ~0.3%-a-year episode noise at this budget, and show where it stalls. Prototype signal
  size: the band beats quarterly rebalancing by 0.26% a year, with Monte Carlo SE 0.02% at 200k paths.
- **Pause-and-predict:** "Will the agent learn to do nothing?"

### 17 · Industry: who sizes bets for a living (`s18_industry`, 3.0 min; new)
- **Goal:** the same mathematics as practised, from the public record; every fact below was checked.
- **Beats and facts (narration in this order):**
  1. **Thorp.** Shannon gave him Kelly's paper at MIT in 1960. On 3 November 1969 his partnership "decided to … use
     the Kelly criterion to allocate its assets". Through May 1998 the partnership and its continuations
     "compounded at approximately 20% annually with a standard deviation of about 6%", with about zero market
     correlation: about $80 billion of trades, some 1.25 million "bets" averaging $65,000. In 1994 a Kelly-sized sports-betting test turned
     $50,000 into a $123,000 profit in 101 days, with the edge estimates "deliberately chosen to be conservative".
     Source: Thorp (2006), *Handbook of Asset and Liability Management* ch 9, pp. 385–428,
     https://www.gwern.net/doc/statistics/decision/2006-thorp.pdf. (The existing card's "≈ 15% a year after fees,
     1969–1988" comes from *A Man for All Markets*: verify against the book, or replace it with the 2006 figures.)
  2. **Benter (Hong Kong racing).** "If one overestimates the advantage by more than a factor of two, Kelly betting
     will cause a negative rate of capital growth"; under full Kelly "downswings during which more than 50% of
     total wealth is lost are a common occurrence"; so bet "1/2 or 1/3" Kelly; "a conservative fractional Kelly
     betting strategy was employed throughout": about 470 races a year against a ~19% track take, four of five
     seasons profitable. Source: Benter (1994), in Hausch, Lo, Ziemba (eds.), *Efficiency of Racetrack Betting
     Markets*, https://www.gwern.net/doc/statistics/decision/1994-benter.pdf.
  3. **Berlekamp.** Kelly's research assistant at Bell Labs (1960, 1962); around 1989 he bought most of James Ax's
     stake in Axcom and with Simons, Straus and Laufer overhauled Medallion's trading
     (https://en.wikipedia.org/wiki/Elwyn_Berlekamp; UC Senate memorial,
     https://senate.universityofcalifornia.edu/in-memoriam/files/elwyn-berlekamp.html). That Medallion used
     Kelly sizing: *(unverified; omit from screen)*.
  4. **Risk budgets as control constraints.** Norway's GPFG: the mandate caps expected relative volatility (tracking
     error) at 1.25 percentage points, and it was 0.37 pp at the end of 2025
     (https://www.nbim.no/en/investments/risk-management/). Bridgewater's All Weather (1996): equal risk in each of four
     economic environments, with "leverage … an implementation tool"
     (https://www.bridgewater.com/research-and-insights/the-all-weather-story). Multi-manager pods: press reports
     (WSJ via Business Insider, 2024) say a Millennium manager who loses 5% has capital halved and at 7.5% is
     likely fired (https://www.aol.com/strategy-69-billion-hedge-fund-193733084.html), *reported, not disclosed by
     the firm*. **Math link (on screen):** Grossman–Zhou (1993): with a drawdown limit α, the optimal policy is
     Merton's fraction of the cushion $W_t-\alpha M_t$, the floor picture of ch 2 with a floor that ratchets up.
     Volatility targeting is Merton with a moving σ: π_t ∝ 1/σ̂_t² (Moreira–Muir 2017 *(verify venue)*).
  5. **Execution desks.** Almgren–Chriss (2001) is a control problem solved daily. Almgren, Thum, Hauptmann and Li
     (2005, *Risk* 18) fitted impact on Citigroup's US equity desks' data (a 3/5 power in size). Part 37 in full.
  6. **Haghani** (of the coin experiment) runs Elm Wealth, which sizes positions by Merton's rule; *The Missing
     Billionaires* (2023, with James White, Wiley *(co-author and publisher unverified)*).
- **Experiment:** `drawdown_policy`: 2,000 paths, Kelly against Grossman–Zhou at α = 0.8. Expected: no path below
  80% of its running maximum (by construction), at the cost of lower median growth (to be computed). Also
  `vol_target` on Ken French daily data (1926–2020): a constant-mix market portfolio vs one scaled by 1/σ̂² (21-day
  realized), same average exposure. Registered with the trial counter; narration branches on the result.
- **Pause-and-predict:** "A pod is down 4.9%. What does the Grossman–Zhou investor do with her stock fraction?"

### 18 · Frontier, 2023–2026 (`s19_frontier`, 2.6 min; new)
All checked on arXiv/JMLR this pass (2 Nov 2026):
- **Jia, Zhou (2023),** "q-Learning in Continuous Time," *JMLR* 24(161):1–61, https://jmlr.org/papers/v24/22-0755.html
  (and Jia's erratum on a sampling assumption). The continuous-time analogue of Q-learning: what to learn when Δt → 0.
- **Dai, Dong, Jia, Zhou (2023),** "Learning Merton's Strategies in an Incomplete Market: Recursive Entropy
  Regularization and Biased Gaussian Exploration," arXiv 2312.11797. RL learns Merton without estimating μ;
  the optimal exploration is Gaussian but biased.
- **Dai, Dong, Jia, Zhou (2026),** "Merton's Problem with Recursive Perturbed Utility," arXiv 2602.13544:
  a closed-form, wealth-independent Gaussian policy.
- **Huh, Jeon, Koo, Lim (2025),** "Pontryagin-Guided Deep Learning for Large-Scale Constrained Dynamic Portfolio
  Choice" (later retitled "Breaking the Dimensional Barrier for Constrained Dynamic Portfolio Choice"), arXiv 2501.12600: up to 1,000 assets, against roughly seven
  for dynamic programming; recovers the closed form unconstrained.
- **Huh, Koo (2026),** "Breaking the Dimensional Barrier: Dynamic Portfolio Choice with Parameter Uncertainty via
  Pontryagin Projection," arXiv 2601.03175: reports beating a model-free PPO baseline on analytic benchmarks.
  Tie this to ch 16, where our PPO needed hand-tuning.
- **Laurière, Perrin, Pérolat, Girgin, Muller, Élie, Geist, Pietquin,** "Learning in Mean Field Games: A Survey,"
  arXiv 2205.12944 (v4, July 2024). Model-free learning of MFG equilibria (background: Carmona–Laurière, arXiv 2107.04568).
- **Chee, Frikha, Li (2026),** "A Monotone Limit Approach to Entropy-Regularized American Options," arXiv
  2602.18062: reflected BSDEs plus entropy regularization for stopping, uniting ch 11–12, 14 and 16.
- **Toda (2023),** "'Ergodicity Economics' is Pseudoscience," arXiv 2306.03275: the sharpest critique, to sit
  against Peters (2019) and Meder et al.
- **Visual:** the chapter's chapters as nodes of a graph (DP, HJB, BSDE, MFG, RL). Each paper lights the edge it
  builds (e.g. RL ↔ HJB for Jia–Zhou, BSDE ↔ stopping for Chee–Frikha–Li).

### 19 · The sizing module, recap, desk and problems (`s20_outro`, 3.2 min; merged House + outro)
- House card: new functions (bellman_merton, hjb_fd, no_trade_band, snell_envelope, perpetual_put, mfg_liquidation,
  cpt_value, robust_fraction, grossman_zhou, ppo_merton with costs). Rule 9 is extended: "rebalance only outside
  the no-trade band", and "drawdown budget as a Grossman–Zhou floor". The trial counter reads its new value
  (+3: myopic loss, vol target, split-sample Kelly).
- Recap in 10 lines; the existing 3 desk questions plus one new one: "With 1% costs and γ = 3, your stock weight
  drifted from 62% to 66%. Trade?" (no: inside the 56–68% band). Existing problems 1–5 plus **problem 6**
  (perpetual put smooth fit) and **problem 7** (the N-player liquidation ODE). Solutions go in the README (EN + ZH).
- Where this comes back, and next: Part 9.

### Minutes

| # | Chapter | Min | Status |
|---|---|---|---|
| H | How much to bet, and how we got here | 3.5 | deepened |
| 1 | Utility and risk aversion | 3.0 | deepened |
| 2 | Bellman's principle (Lab 1) | 3.0 | deepened |
| 3 | HJB and verification | 3.2 | new |
| 4 | Viscosity solutions | 2.6 | new |
| 5 | Merton's problem | 3.0 | deepened |
| 6 | Consumption and the martingale method | 2.8 | new |
| 7 | Transaction costs (Lab 2) | 3.2 | new |
| 8 | Kelly and Breiman | 3.0 | deepened |
| 9 | Fractional Kelly, estimation risk, LTCM | 3.2 | merged/deepened |
| 10 | Samuelson and ergodicity | 2.6 | light |
| 11 | Snell envelope (Lab 3) | 3.0 | new |
| 12 | Smooth fit and the American put | 2.6 | new |
| 13 | Prospect theory and ambiguity | 3.6 | deepened |
| 14 | BSDEs | 2.8 | deepened |
| 15 | Mean-field games (Lab 4) | 3.0 | new |
| 16 | Reinforcement learning (Lab 5) | 3.4 | deepened |
| 17 | Industry | 3.0 | new |
| 18 | Frontier | 2.6 | new |
| 19 | Sizing module, recap, desk, problems | 3.2 | merged |
| | **Total** | **≈ 60.3** | gate: `lecture_length.py quant8 --floor 50` |

If narration runs long, cut first: the secretary example (−0.4), the rebalance_sim panel (−0.3), the Bridgewater
line (−0.2).

## 4. Compute budget (≈ 2 CPU-hours, seeded, resumable)

| Item | What | Est. CPU-min |
|---|---|---|
| existing: coin, merton_us, kelly_us, fractional, samuelson, ergodic, ltcm, secretary, american, envelope | as now | 6 |
| existing: bellman → **bellman_sweep** | + value/policy every 6th step, both cases | 2 |
| existing: bsde (+ **bsde_replay**) | regression snapshots | 6 |
| **coin_live** | 160 players × 4 fractions paths | <1 |
| **utility_check** | exact vs Arrow–Pratt premia | <1 |
| **hjb_fd** | FD policy iteration 200 × 400 + convergence table | 3 |
| **viscosity** | eikonal 3 grids, two schemes, snapshots | <1 |
| **rebalance_sim** | 2,000 × 30 y, monthly | 1 |
| **martingale_check**, **consumption** | 2,000 daily paths; closed forms | 2 |
| **davis_norman** | 4 ε × γ ∈ {1, 3}, 30 y monthly (1.4 s each) + 2,000-path wedge simulation + turnover | 3 |
| **kelly_live**, **breiman_race**, **edge_error** | fans, 10,000-path race, edge sweep | 3 |
| **snell_rw**, **perpetual_put** | sweeps; 40-year tree | 1 |
| **myopic_loss** (registered) | CPT on French 1926–2020, h = 1..36 | <1 |
| **robust_fraction** | detection errors, θ grid | <1 |
| **mfg_crowd** | fictitious play, N ∈ {1, 2, 10, ∞}, 500-agent visual sample | <1 |
| **ppo** × 5 seeds | existing settings, 1 thread each, 4 in parallel | 13 |
| **ppo_costs** × 5 seeds + DP baseline | ε = 1%, γ = 1, quarterly | 22 |
| **drawdown_policy** | Kelly vs Grossman–Zhou, 2,000 paths | 1 |
| **vol_target** (registered) | French daily | <1 |
| **Total** | | **≈ 65 CPU-min** (≈ 25 min wall on 4 cores) |

PPO items use `CACHE.partial` per seed (resumable). All others are seconds to minutes and recompute in full.
`python -m videos.quant.quant8.compute` rebuilds everything (README "Build it").

## 5. Revised SYLLABUS.md §6 entry (ready to paste)

```markdown
### Part 8 · Decisions and Control (~60)
1. Expected utility: the vNM axioms, Arrow–Pratt derived, certainty equivalents; Allais and Rabin as warnings.
2. Dynamic programming (Bellman 1957), backward induction on a grid; the HJB equation derived from the DPP and
   Itô; the verification theorem.
3. Viscosity solutions in outline (Crandall–Lions 1983): kinks, touching test functions, comparison; monotone
   schemes converge (Barles–Souganidis 1991).
4. Merton's problem (1969/71) by HJB: the fraction (μ − r)/(γσ²), rebalancing, two-fund separation; on 94 years of
   US data with its error bars.
5. Consumption (Merton 1971) and the martingale method (Cox–Huang 1989; Karatzas–Lehoczky–Shreve 1987): the
   investor buys a power claim.
6. Transaction costs: the Davis–Norman (1990) no-trade wedge, Shreve–Soner (1994), the ε^{1/3} band, by
   dynamic programming here.
7. Kelly (1956) and Breiman (1961), proved; fractional Kelly and estimation risk (Thorp, Benter); Samuelson's
   objection (1979); ergodicity and the controversy (Peters 2019; Doctor–Wakker–Wang 2020; Toda 2023).
8. Optimal stopping: the Snell envelope as the least concave majorant; smooth fit (McKean 1965); the American
   put preview.
9. Prospect theory (KT 1979/1992; Benartzi–Thaler 1995 redone on data); ambiguity (Ellsberg; Gilboa–Schmeidler;
   Hansen–Sargent; Maenhout's robust Merton derived).
10. BSDEs (Pardoux–Peng 1990; El Karoui–Peng–Quenez 1997): two-rate pricing by regression.
11. Mean-field games (Lasry–Lions; Huang–Malhamé–Caines 2006): a liquidating crowd, closed form and fictitious play.
12. Reinforcement learning on the same problems: PPO on Merton (5 seeds) and on the transaction-cost problem,
    against the DP band.

*Textbooks:* Pham ch 1–7; Touzi ch 2–6, 9; Karatzas–Shreve *Methods* ch 3, 6; Björk (stochastic control, the
martingale approach, optimal stopping); Merton *Continuous-Time Finance* ch 4–5; Øksendal ch 10–11; Back ch 1–2,
14; Bertsekas vol. I; Sutton–Barto ch 3–6, 13; Carmona–Delarue vol. I.
*Trained:* PPO on Merton (5 seeds, AI 26's code) converging to the Merton line; PPO on the transaction-cost
problem against the DP band; replayed with checkpoints.
*Labs:* the Bellman grid solver; the no-trade band; the Snell envelope; MFG fictitious play; PPO's core.
*Visuals:* the value surface built backward slab by slab; the HJB sup as a moving parabola; test functions
touching a kink; the Davis–Norman wedge with a reflected wealth dot; Kelly fans growing live; the Snell envelope as
a rope over pegs; the smooth-fit slider; the crowd's two arrows of time.
*Crisis:* leverage beyond Kelly, using LTCM's published leverage (full story in 41).
*Firms:* Thorp's partnership and Kelly sizing (Thorp 2006); Benter's syndicate; risk budgets (NBIM's 1.25 pp
limit; multi-manager drawdown rules, as reported); execution desks.
*Desk:* "You have a 60% coin at even odds. What fraction do you bet?" "With 1% costs your weight drifted from 62%
to 66%. Trade?"
*House:* the sizing module (Merton, Kelly, no-trade band, drawdown floor).
```

## 6. Estimated minutes

≈ 60 minutes over 20 manifest entries (table in §3), against 28.2 now. 13 chapters are new or substantially
rebuilt, and 5 labs (3 required). Trained or fitted models are replayed in ch 2, 11, 14, 15 and 16. Live simulations
run in H, 5, 6, 7, 8, 10 and 17. Compute is about 65 CPU-minutes.

**Implementation notes.** Rename modules to `s01`–`s20` as listed; caches are keyed by scene module name, so
renaming invalidates the rendered caches, which is expected. Compute items keep their names. `zh_lines.py` and
`narration_zh.json` must be regenerated for every changed line; new on-screen strings go in `quant_text_zh.json`
(glossary additions for QUANT_ZH_GUIDE.md: 验证定理, 黏性解, 无交易区间, 斯内尔包络, 光滑粘合, 平均场博弈, 虚拟博弈,
短视损失厌恶, 稳健控制). The README audit table is §2(b) above, and the reading guide gets one line per added paper.
