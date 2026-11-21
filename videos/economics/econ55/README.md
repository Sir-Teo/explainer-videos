# Economics, Built: Part 55, Identifying Macro

Part 55 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act X, *The Graduate Core*. It asks how anyone can say what a policy did,
with one history and no control group. Its answer: only by adding an assumption the data cannot supply, about timing,
the long run, signs, an outside instrument or a change in variance, and then by testing it where the truth is known,
against instruments built from the bank's own records and from markets, and against regions that saw different
policies. What survives every credible method is the sign and the timing of policy's effects; their size still
depends on the assumption.

It opens on Sims's price puzzle, recomputed from the Data Room: a monthly vector autoregression of industrial
production, consumer prices and the federal funds rate, 1965-1995, with twelve lags, says the price level is higher
for 36 months after a one-point rise in the funds rate, by up to 0.24%; add the producer price index for all
commodities, a piece of what the Federal Reserve saw coming, and prices are lower from month 22 and 1.1% lower after
four years. From there it covers:

- what a VAR identifies (Sims 1980): with three variables the surprises' covariance has six numbers and the mixing
  matrix nine; three rotations of one Island history fit it exactly and tell three stories (a tightening that does
  nothing, one that raises output, one that crashes it and raises inflation);
- Play it: three unlabelled sets of impulse responses; the monetary tightening is the one with the rate up and output
  and inflation down, and recognizing it by its signs is itself an identifying assumption;
- five schemes: timing (recursive ordering), the long run (Blanchard and Quah 1989), signs (Uhlig 2005), an outside
  instrument (Stock and Watson 2012; Mertens and Ravn 2013), a change in variance (Rigobon 2003);
- all five on the Island's structural VAR, whose truth is known: on one history and on 300, timing is wrong on
  average (inflation's first-quarter fall of 0.34 points per point of the rate comes out as zero by assumption), the
  instrument and the change in variance are right on average (-0.34), the long run recovers the supply shock (output
  +1.26% for good, against 1.26), and the sign set, 2,638 of 24,000 candidates, contains the truth for inflation's
  first year and a half but sits below it for output, as Baumeister and Hamilton warned;
- local projections (Jorda 2005) against VARs (Plagborg-Moller and Wolf 2021) in 300 histories: a VAR with one lag
  when the truth has two is off by 0.07 at four years; projections are nearly unbiased but their spread is twice a
  short VAR's;
- narrative (Romer and Romer 2004) and high-frequency (Kuttner 2001; Gurkaynak, Sack and Swanson 2005) shocks as
  instruments (Gertler and Karadi 2015), on Part 31's Island: a recursive VAR shows the price puzzle (inflation up
  0.43), a noisy signal of the bank's news shrinks it (0.13), narrative shocks and clean surprises recover the truth,
  surprises with an information effect (Nakamura and Steinsson 2018) understate it;
- an intermission film of the yield curve's slope, the 10-year Treasury yield minus the 3-month bill, 1953-2026, with
  the NBER's recessions, as a line and a tune;
- Part 30's three-equation New Keynesian model estimated by the Kalman filter and random-walk Metropolis-Hastings (An
  and Schorfheide 2007; Smets and Wouters 2007) on 200 simulated quarters: with all three series observed, every
  posterior is 10 to 35% as wide as its prior (the Phillips slope 0.106 against 0.1);
- weak identification (Canova and Sala 2009): leave the rate out, and the posteriors of four of the five parameters
  are 64 to 92% as wide as their priors; the likelihood of sigma, the others re-estimated, falls 36 log points by
  sigma = 3 with the rate observed, and 1.5 across the whole range without it;
- cross-sectional macro: Part 32's currency union, where comparing regions recovers the relative multiplier (1.53,
  planted 1.5) and the nation's is 0.56 (planted 0.6): the missing intercept (Nakamura and Steinsson 2014; Wolf
  2023); shift-share designs identified by shares or by shocks (Goldsmith-Pinkham, Sorkin and Swift 2020; Borusyak,
  Hull and Jaravel 2022);
- impulse-response matching (Christiano, Eichenbaum and Evans 2005) on 400 Island quarters: sigma 1.48 (truth 1.5),
  the Phillips slope 0.072 (truth 0.1) and between 0.04 and 0.13 across 60 histories;
- forecasts at the turns (the forecasters in 2008, the Federal Reserve in 2021) and what macroeconomics knows (Ramey
  2016; Nakamura and Steinsson 2018);
- the Dials: the effect of a one-point tightening on industrial production, with two rows added from the hook (-0.80
  without commodity prices, -1.12 with them), and the spending multiplier from Part 32;
- in practice (central banks' research departments) and a frontier of heterogeneous-agent models estimated on micro
  and macro data (Bayer, Born and Luetticke 2024), micro moments and expectations data (Coibion, Gorodnichenko and
  Kamdar 2018), and new instruments.

There is no *Called it?* in this part; Chapter 11 recalls Parts 1 and 28's.

## Build it

```bash
python -m videos.economics.econ55.compute              # every number (about five minutes), into .cache/econ55/
python tools/qa_scene.py econ55 Island                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ55 -q l   # the whole part, silent preview
python tools/build.py econ55                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 55                     # the lab
```

The data are FRED's industrial production, CPI, federal funds rate and producer price index for all commodities (the
hook), and its 10-year and 3-month Treasury yields with the NBER's recession months (the intermission), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); every other number is computed.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The price puzzle | Sims's VAR on American data, with and without commodity prices; the question; objectives |
| 1 | What a VAR knows, and what it does not | Six numbers for nine; three rotations, three stories |
| 2 | Play it: which shock was it? | Three unlabelled responses; signs as an assumption |
| 3 | Five ways to identify a shock | Timing, the long run, signs, an instrument, a change in variance |
| 4 | The five, on the Island's history | One history; 300 histories; which recover the truth |
| 5 | Local projections | One regression per horizon; bias against variance in 300 histories |
| 6 | Narrative and high-frequency shocks | The two sources; the information effect; the price puzzle cured |
| — | Intermission | The yield curve's slope, 1953-2026, with recessions, as a line and a tune; the story so far |
| 7 | Estimating a DSGE model | State space, the Kalman likelihood, Metropolis-Hastings; posteriors |
| 8 | What the data cannot tell apart | The rate left out; posteriors against priors; a flat profile |
| 9 | Macro from the cross-section | Regions and the missing intercept; shift-share designs |
| 10 | Matching impulse responses | The estimator; the model fitted to an Island's responses |
| 11 | Forecasts, and what macroeconomics knows | The record at the turns; what survives every method |
| 12 | The Dials | A one-point tightening (two rows added); the spending multiplier |
| 13 | In practice: research departments | Models, surprises, projections, briefings |
| 14 | Frontier: micro data and expectations | Estimated HANK; micro moments; expectations as data; new instruments |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 56, *The Core Exam* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's macro-econometrics (`explainer.economics.agora.macrometrics`),
Part 31's monetary history (`agora.cb`), Part 32's regions (`agora.fiscal`) and the Island's Part 55 truths; the
narration states the cached numbers.

- **The price puzzle.** 100 x log industrial production, 100 x log CPI, (100 x log PPI, all commodities,) and the
  funds rate, monthly 1965-1995; a VAR(12) with a constant; the Cholesky shock to the funds rate, last, scaled to one
  point; 300 residual-bootstrap replications for the 16-84% bands.
- **The Island's structural VAR.** Output growth, inflation and the rate follow a VAR(2) driven by supply, demand and
  monetary shocks; the impact matrix has the monetary shock lowering output and inflation within the quarter; the
  demand and monetary columns are set so that only supply moves output's level in the long run; in a random half of
  quarters the monetary shock's s.d. doubles; a proxy is the monetary shock plus noise of s.d. 0.8. Histories of 240
  quarters (200 for the projections); VAR(4) unless stated; responses per point of the rate on impact.
- **Sign restrictions.** 4,000 random orthonormal rotations, each column tried with both signs; kept if the rate rises
  and output growth and inflation fall for three quarters.
- **The DSGE model.** x = E x' - (1/sigma)(i - E pi') + d, pi = beta E pi' + kappa x + u, i = phi_pi pi + phi_x x + v,
  with AR(1) shocks (persistence 0.8, 0.6, 0.4; s.d. 0.5, 0.2, 0.25), beta 0.99, kappa 0.1, sigma 1.5, phi_pi 1.5,
  phi_x 0.25; measurement error s.d. 0.05; gamma priors for kappa, sigma, phi_pi and phi_x (means 0.15, 1.5, 1.5,
  0.25), a beta prior for rho_v (mean 0.5); 6,000 draws after 1,500, with the proposal scaled from the inverse Hessian
  at the mode.
- **Matching.** The same model with the monetary shock's s.d. 1; 400 quarters; local projections with four lags on a
  proxy (the innovation plus noise of half its s.d.); weights from 60 more histories.

## Problems and solutions

**1.** *Counting: with n variables, how many restrictions does a structural VAR need beyond Sigma = BB'? How many does
the recursive ordering supply?*

*Solution.* B has n^2 entries and Sigma, being symmetric, gives n(n+1)/2 equations, so n(n-1)/2 more are needed:
three for n = 3. A lower-triangular B has exactly n(n-1)/2 zeros above its diagonal, so the recursive ordering
supplies exactly enough, which is why it identifies every shock, rightly or wrongly.

**2.** *Timing: in a VAR of output, prices and the rate, which zeros does ordering the rate last impose, and what must
the bank not know for them to hold?*

*Solution.* The third column of B, the monetary shock, has zeros in the output and price rows: policy cannot move
output or prices within the period. Ordering output first also means output does not respond within the period to the
price shock. For the monetary column to be the policy shock, the bank's rate must respond only to this period's
output and prices and to the past: if it also responds to news about future inflation that the VAR does not contain,
that news enters the 'policy shock' and produces the price puzzle.

**3.** *The long run: with C(1) = (I - A_1 - ... - A_p)^-1, show that only the first shock moves the first variable's
level for ever if C(1)B is lower triangular.*

*Solution.* The response of the first variable (a growth rate) at horizon h to shock j is the (1, j) entry of Psi_h B;
the level's long-run response is the sum over h, which is the (1, j) entry of (sum Psi_h) B = C(1)B. If C(1)B is lower
triangular, its first row is (c, 0, ..., 0): only the first shock has a permanent effect on the level.

**4.** *An instrument: if z_t = lambda e^m_t + eta_t with eta independent of every shock, show that Cov(u_t, z_t) is
proportional to b_m.*

*Solution.* u_t = B e_t = sum_j b_j e^j_t with the shocks uncorrelated and of unit variance. Then Cov(u_t, z_t) = sum_j
b_j Cov(e^j_t, lambda e^m_t + eta_t) = lambda b_m, since only the monetary shock is correlated with z. The scale is
unknown, so normalize: per point of the rate on impact.

**5.** *Heteroskedasticity: if only e^m's variance changes, show that Sigma_1 - Sigma_0 has rank one, and find b_m from
it.*

*Solution.* Sigma_r = B D_r B' with D_r diagonal; only the monetary entry differs, so Sigma_1 - Sigma_0 =
(s_1^2 - s_0^2) b_m b_m', a matrix of rank one. Its only non-zero eigenvalue's eigenvector is b_m up to scale (and
sign, fixed by letting the rate rise).

**6.** *Local projections: in a VAR(1), show that the population projection coefficient at horizon h equals A^h b.*

*Solution.* Iterating, x_{t+h} = A^{h+1} x_{t-1} + sum_{k=0..h} A^k B e_{t+h-k}. Project x_{t+h} on the shock e^j_t
controlling for x_{t-1}: the shocks at other dates are uncorrelated with e^j_t and x_{t-1}, so the coefficient is the
term with k = h, A^h b_j: the VAR's impulse response.

**7.** *Weak identification: a posterior is 90% as wide as its prior. What should a referee ask for?*

*Solution.* That the posterior be shown against the prior; that the estimate be repeated with a different prior (if
the posterior moves with it, the data are silent); a likelihood profile or a check that the parameter moves the
model's predictions for the observed series; and, if possible, data that would identify it, as the rate did in the
film.

**8.** *The missing intercept: in y_rt = m_l (g_rt - gbar_t) + m_a gbar_t + u_t + e_rt, show that year effects remove
m_a and leave m_l.*

*Solution.* Averaging over regions in year t gives ybar_t = m_a gbar_t + u_t + ebar_t, since the deviations average to
zero. Subtracting, y_rt - ybar_t = m_l (g_rt - gbar_t) + (e_rt - ebar_t): the national terms, including m_a gbar_t and
the common shock u_t, are gone. A regression with year effects estimates m_l; m_a has been absorbed into the year
effects, the missing intercept.

## Lab and interactive

- `python -m videos.economics.labs 55`: the Island's identification schemes on one history against the truth; the
  sign set's size; local projections against VARs; the New Keynesian model's Kalman likelihood at the truth and away
  from it; a short Metropolis-Hastings run; regions.
- The interactive (course site): identify. The reader rotates the mixing matrix of a fitted VAR and watches the
  'monetary' responses change, with the true ones beside them, then turns on the sign restrictions and sees which
  rotations survive.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[55]`; the monetary-shock and multiplier
dials are in `explainer/economics/dials.py` (two rows added: this part's VARs, 1965-1995); the FRED series are in the
Data Room. The forecast record of Chapter 11 is Parts 1 and 28's *Called it?* entries. The models are stated from the
papers cited in the chapters (Sims 1980 and 1992, Blanchard and Quah 1989, Kuttner 2001, Rigobon 2003, Romer and Romer
2004, Gurkaynak, Sack and Swanson 2005, Jorda 2005, Uhlig 2005, Christiano, Eichenbaum and Evans 2005, An and
Schorfheide 2007, Smets and Wouters 2007, Canova and Sala 2009, Stock and Watson 2012 and 2018, Mertens and Ravn 2013,
Nakamura and Steinsson 2014 and 2018, Baumeister and Hamilton 2015, Gertler and Karadi 2015, Ramey 2016,
Coibion, Gorodnichenko and Kamdar 2018, Goldsmith-Pinkham, Sorkin and Swift 2020, Plagborg-Moller and Wolf 2021,
Borusyak, Hull and Jaravel 2022, Wolf 2023, Bayer, Born and Luetticke 2024, Li, Plagborg-Moller and Wolf 2024) and
computed here.
