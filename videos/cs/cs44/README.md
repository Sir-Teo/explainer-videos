# Computer Science, Built — Part 44: People and Products

Part 44 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth and last part of Act VIII, *Building Software*. Software is used by people,
and both the people and the product can be measured. Fitts's law falls out of Shannon's channel capacity, Hick's law
is the entropy of a choice, perception has thresholds and colour has formulas, which we turn on this series' own
palette. Where intuition runs out, industry runs controlled experiments: we derive the A/B test and its power, show
why checking it every morning breaks it, and repair it with a sequential test and with CUPED.

The instruments are in `explainer/cs/people/` (tested in `tests/test_cs44_people.py`):
* `hci.py`: an aimed movement as a sequence of corrected submovements, each landing with an error proportional to the
  distance it covers, and a Fitts experiment on twenty conditions with a least-squares fit; the same target at the
  screen edge; a chooser who halves the candidates (Hick's n + 1 possibilities) and the Huffman mean number of yes/no
  questions for a skewed menu (Hyman); the keystroke-level model with operator times from Card, Moran and Newell
  (1980), except B (a mouse-button press), which comes from Kieras's later KLM guide, and four methods for two tasks;
  the Nielsen–Landauer curve 1 − (1 − L)ⁿ, and the same with problem visibilities drawn from a Beta distribution.
* `colour.py`: sRGB's transfer curve both ways, CIE XYZ and CIELAB, Ottosson's OKLab, relative luminance and the WCAG
  contrast ratio, colour-vision deficiency simulated with the matrices of Machado, Oliveira and Fernandes (2009) in
  linear light; a report on this series' palette (each colour under three deficiencies, the closest pairs in OKLab,
  contrast on the background); a grey ramp in code values against light; checks against published values.
* `experiments.py`: the two-proportion z-test; sample size and simulated power; daily peeking at A/A tests; the
  mixture sequential probability ratio test; CUPED on synthetic users; twenty null metrics, uncorrected and with
  Benjamini–Hochberg; a sample-ratio-mismatch check by χ²; Simpson's paradox; Thompson sampling against a 50/50
  split; a marketplace with limited supply; Warner's randomized response.

## Chapters

* **Hook.** San Francisco, 9 December 1968: Engelbart's NLS demo from SRI, with a mouse and pointer (Engelbart and
  English, 1964), hypertext, two people editing one document live, and video of a colleague thirty miles away. The
  ideas reach ordinary desks: the Xerox Alto (1973), Jobs's visit to PARC (1979), the Macintosh (1984), Windows 1.0
  (1985), the web (1991), multi-touch phones (2007). Two kinds of measurement previewed: simulated pointing falls on
  Fitts's line (R² = 0.99), and an A/A test checked daily for a month declares a winner 28% of the time against the
  promised 5%.
* **1. Pointing is a channel.** Fitts's reciprocal tapping (1954): only the ratio D/W matters, logarithmically.
  Shannon's C = B log₂(1 + S/N) (Part 28) becomes the index of difficulty ID = log₂(D/W + 1) bits (MacKenzie's form,
  1992, never negative) and MT = a + b·ID, with 1/b a throughput. Why a logarithm: Meyer et al.'s submovements (1988),
  each shrinking the remaining distance by a roughly constant factor. Our simulated hand on twenty targets (D from 64
  to 1024 px, W from 8 to 64 px): a = 0.333 s, b = 0.086 s per bit, R² = 0.994, a throughput of 11.6 bits per second
  (people with a mouse manage a few bits per second, Soukoreff and MacKenzie 2004). Infinitely deep targets: the same
  target takes 0.77 s in the middle of the screen and 0.40 s at the edge, hence the Macintosh's single menu bar and
  the corners. The steering law (Accot and Zhai, 1997), T = a + b·A/W, linear rather than logarithmic: a cascading
  menu is a tunnel.
* **2. Choosing, and predicting a task's time.** Hick's lamps (1952) and the n + 1 that counts "no lamp"; a chooser
  who halves the candidates (binary search, Part 16) finds one of 7 lamps or none in log₂ 8 = 3 comparisons; simulated
  for one to ten lamps, a = 0.200 s, b = 0.153 s per bit, R² = 0.999. Hyman (1953): the entropy, not the count. A menu
  chosen with probabilities 0.70, 0.10, 0.10, 0.05, 0.05 carries H = 1.46 bits against log₂ 5 = 2.32 for five equal
  choices, and the best yes/no questioning (a Huffman code, *AI, Built* Part 1) needs 0.7 × 1 + 0.3 × 3 = 1.6
  questions on average. Where the law stops: scanning an unfamiliar list is a linear search, and practice flattens the
  slope. GOMS (Card, Moran and Newell, *The Psychology of Human-Computer Interaction*, 1983): goals, methods of
  operators, selection rules. The keystroke-level model: K 0.28 s, P 1.10, B 0.10, H 0.40, M 1.35 (Card, Moran and
  Newell 1980; B from Kieras's later KLM guide). Deleting a file through a menu, HMPBMPB, 5.5 s; with a shortcut,
  HMPBHMKK (from the same starting position), 5.26 s; renaming through a dialog 9.47 s, inline with F2 8.85 s. The M blocks dominate: a faster design
  asks for fewer decisions, not fewer keys.
* **3. Perception and its thresholds.** 0.1, 1 and 10 seconds (Miller 1968; Card, Robertson and Mackinlay 1991;
  Nielsen, *Usability Engineering*, 1993): instantaneous, flow of thought kept, attention kept, attention lost. Input
  latency: Ng et al. (Microsoft Research, 2012) found people dragging on a touch screen notice delays of a few
  milliseconds; an input crosses sensor, operating system, application, rendering, compositing and display, and each
  stage that waits for the next frame can add 16.7 ms at 60 Hz (Part 42). Weber's fraction ΔI/I = k (1834) and
  Fechner's S = c log(I/I₀) (1860): +0.1 on a bar of 1 is +10%, on a bar of 4 only +2.5%. What pops out: colour and
  orientation are found in parallel, a red *and* tilted line among red upright and blue tilted ones item by item
  (Treisman and Gelade's feature integration theory, 1980). Change blindness (Rensink, O'Regan and Clark, 1997): six
  dashboard numbers behind a flicker, and the errors tile going from 17 to 71 unseen.
* **4. Colour.** Three cones, metamers, CIE XYZ (1931), sRGB (HP and Microsoft, 1996). Code values are not light:
  under the transfer curve (c + 0.055)/1.055 raised to 2.4, code 128 (#808080) emits 21.6% of white's light, and half
  of white's light is #bcbcbc; equal code steps are roughly equal steps of lightness (Weber and Fechner again), so
  blending and lighting must happen in linear light (Part 51). CIELAB (1976) and OKLab (Ottosson, 2020), with this
  series' six colours plotted in OKLab's a–b plane; our conversions give white L = 100.0 in CIELAB and 1.000 in OKLab,
  and sRGB red (0.628, 0.225, 0.126), the published value. The palette under simulated deficiency (Machado, Oliveira
  and Fernandes, 2009), closest pair by OKLab distance: typical vision `data`–`lambda` 0.102; protanopia
  `here`–`true` 0.066; deuteranopia `false`–`kernel` 0.014; tritanopia `data`–`true` 0.066 (below 0.08 counts as easily
  confused). The honest finding: under deuteranopia this series' red for *false* and orange for the kernel are nearly
  the same colour. Contrast on the background: `data` 7.1, `here` 12.1, `true` 9.3, `false` 5.9, `lambda` 6.1,
  `kernel` 6.7, all above WCAG's 4.5 for text and three above 7; a two-series chart separated by red and orange
  becomes one series under deuteranopia, and survives with shapes and direct labels. Never colour alone.
* **5. Text on screens.** A glyph is an outline of Bézier curves (TrueType, Apple, 1991, quadratic; PostScript and
  OpenType CFF, cubic); a pixel is lit when its centre is inside, by counting crossings of a ray (Part 22's
  orientation test; Part 51 rasterizes triangles the same way). "Job" in DejaVu Serif rasterized by FreeType at 8, 12,
  16 and 24 px: at 8 px the whole word is 23 × 11 pixels; one bit per pixel gives 2 levels, antialiasing 41, 66, 80
  and 111 grey levels. Hinting: three equal stems 1.4 px wide land as coverages (0.7, 0.7), (1.0, 0.4) and (0.3, 1.0,
  0.1), and snapped to whole pixels they are equal again; TrueType's hinting programs run on a small stack machine.
  Subpixel rendering: a one-pixel stem starting a third of the way in is two dim greys as whole pixels, and placed to
  a third of a pixel with stripes; ClearType in Windows XP (2001); Apple turned it off in macOS in 2018. Readable text:
  93 characters a line with tight spacing against 60 with spacing 1.5 (Bringhurst: 45 to 75, 66 ideal; WCAG 1.4.8:
  at most 80, spacing at least 1.5); x-height; contrast 4.5 to 1.
* **6. Accessibility.** About 1.3 billion people, 16% of the world, live with significant disability (WHO);
  permanent, temporary and situational versions of each need, after Microsoft's Inclusive Design toolkit. Screen
  readers, switch access, magnification (text to 200%, reflow at 320 CSS pixels) and voice control (the visible label
  in the accessible name, 2.5.3). Motor accessibility with chapter 1's fit, MT = 0.33 + 0.086 log₂(D/W + 1), at a
  reach of 480 px: a 16 px target has ID 4.95 and a predicted 759 ms, 24 px 4.39 and 710 ms, 44 px 3.57 and 640 ms;
  WCAG 2.2's 24 × 24 CSS pixels at AA (2.5.8), 44 × 44 at AAA (2.5.5), and a single-pointer alternative to dragging
  (2.5.7). Cognitive accessibility: consistent navigation (3.2.3), adjustable time limits (2.2.1), sign-in without
  a memory or puzzle test (3.3.8), captions with sounds (1.2.2). Universal design (Ronald Mace) and the curb-cut
  effect; WCAG's four principles, perceivable, operable, understandable, robust.
* **7. Evaluating usability.** Nielsen's ten heuristics (1994) and heuristic evaluation (Nielsen and Molich, 1990);
  thinking aloud (Clayton Lewis at IBM, 1982, from Ericsson and Simon's verbal reports), on an illustrative session.
  Nielsen and Landauer's model (1993), found = 1 − (1 − L)ⁿ with L = 0.31: one user finds 31% of the problems, two
  52%, three 67%, four 77%, five 84% (the chapter's title asks the famous "five users find 85%?"). With visibility
  varying from problem to problem (a Beta distribution with the same mean), five users find 71%, and reaching 84%
  takes 11 users. A problem that hits one user in twenty is found by five users with probability 1 − 0.95⁵ = 23%;
  one round of fifteen would find 99.6% of today's problems, but Nielsen's advice (2000) is three rounds of five,
  fixing in between.
* **8. The A/B test.** A randomized controlled trial (Fisher, 1935): a coin, not a person, assigns users, so the arms
  differ only by chance in every trait, measured or not (Part 20's concentration). The two-proportion z-test derived:
  pooled rate under the null, SE = √(p̂(1 − p̂)(1/n_A + 1/n_B)), p = 2(1 − Φ(|z|)); 500 against 560 conversions out of
  10,000 each (pooled 5.30%, SE 0.317 points) is a 12% lift with z = 1.89 and p = 0.058, not significant. Two errors:
  α = 5%, and β = 20% when δ sits 1.96 + 0.84 standard errors out. Sample size n ≈ 16σ²/δ² per arm, the constant
  (1.96 + 0.84)² × 2 = 15.7; on a 5% conversion rate, relative lifts of 1, 2, 5, 10 and 20% need 2,982,574, 745,643,
  119,303, 29,826 and 7,456 users per arm (the rule of 16 says 3,040,000, 760,000, 121,600, 30,400 and 7,600). Checked
  on 2,000 simulated experiments: at n = 119,302 the power is 0.79 (78.9%), at half that 0.50 (theory
  Φ(2.80/√2 − 1.96) = 0.51); an underpowered test that reaches significance overstates the effect (Gelman and Carlin,
  2014).
* **9. Looking too often.** An A/A test, 1,000 users a day in each arm, 5% converting, z-tested every morning: of six
  p-value paths, one falls below 0.05, on the last morning. Over 4,000 simulated A/A experiments stopped at the first
  p < 0.05: 5% on day 1, 17% after a week, 23% after two weeks, 28% (28.1%) by day 30; the same experiments looked at
  once on day 30 give 4.2%. Why: with no effect z is a scaled random walk, and by the law of the iterated logarithm
  (Khinchin, 1924) its peaks keep reaching √(2 log log n); thirty independent tests would give 79%, overlapping looks
  give 28%. The fix: Wald's sequential test, averaged over plausible effects by Robbins (1970), Λₙ against 1/α = 20; a
  martingale with mean 1 under the null, so by Ville's inequality (1939) P(supₙ Λₙ ≥ 1/α) ≤ α; in z units its
  boundary starts high and comes down; always-valid p-values (Johari, Pekelis and Walsh). On the same traffic: false
  positives 28.1% for daily z-tests, 4.2% for one look, 0.4% for the mixture tuned to 5% lifts and 1.2% tuned to 10%
  lifts; for a real 10% lift within 30 days, power 39% (median stop day 22) and 51% (day 18), against 80% by design
  for a fixed test that needs 29,826 users per arm, the whole 30 days looked at once.
* **10. Less noise, same truth.** CUPED (Deng, Xu, Kohavi and Walker, 2013): Y_cv = Y − θ(X − X̄) with X the user's
  metric in the month before. Derived: θ* = Cov(X, Y)/Var X, the regression slope, and Var(Y − θ*X) = Var Y·(1 − ρ²);
  unbiased because X is measured before randomization. On 20,000 users per arm, 2,000 repeated experiments per
  correlation, the variance ratio is 1.00, 0.90, 0.74, 0.50 and 0.19 at ρ = 0, 0.3, 0.5, 0.7 and 0.9 (theory 1, 0.91,
  0.75, 0.51, 0.19), worth ×1.0, ×1.1, ×1.3, ×2.0 and ×5.3 the users. For a true effect of 0.02 standard deviations
  the 95% interval is ±0.0197 without CUPED, ±0.0171 at ρ = 0.5, ±0.0141 at 0.7 (29% narrower) and ±0.0086 at 0.9 (56%
  narrower). Stratification by the law of total variance; regression adjustment in general, which with
  treatment-by-covariate terms cannot hurt precision in large samples (Lin, 2013).
* **11. Pitfalls at scale.** Twenty metrics in an A/A test: P(at least one p < 0.05) = 1 − 0.95²⁰ = 64.2%, simulated
  64.1%. Bonferroni's α/k, and Benjamini and Hochberg's step-up line αi/k (1995), which controls the false discovery
  rate: with nothing real, 5.0% of experiments make any false discovery (on four illustrative real effects among
  twenty, the line picks them out). Sample-ratio mismatch: 50,000 against 49,000 on a 50/50 split gives χ² = 10.1,
  p = 0.0015, a broken split; 50,100 against 49,900 gives χ² = 0.4, p = 0.53, chance. Simpson's paradox (1951): a
  redesign converting 11.2% against 10.0% on desktop and 5.8% against 3.0% on mobile, but 6.5% against 7.7% overall,
  because 5,200 of its 6,000 visitors were on mobile (illustrative counts). Novelty and primacy effects, read by days
  since first exposure. Twyman's law, with a checklist for an illustrative revenue +38%.
* **12. Bandits and metrics.** Thompson sampling (1933; *AI, Built* Part 26): draw a plausible rate from each beta
  belief and show the higher. Raced over 100,000 visitors with versions converting 5.0% and 5.5% (200 repetitions,
  updates every 500 visitors): a 50/50 split loses about 253 conversions, Thompson sampling 48; but the split measures
  the difference with a standard deviation of 0.0014 (0.14 points) and the bandit 0.0066, about 5 times less
  precise. Bandits for optimizing, A/B tests for learning. A north-star metric, driver metrics and guardrails (load
  time, crashes, unsubscribes, support tickets); ship when the overall evaluation criterion improves and no guardrail
  regresses (Kohavi). Goodhart's law (Goodhart 1975, in Strathern's 1997 wording) and reward hacking (*AI, Built*
  Part 31); dark patterns (Brignull, 2010). Experimenting on people: Kramer, Guillory and Hancock (PNAS 2014), about
  689,000 Facebook users for one week in January 2012, the editorial expression of concern, and the Belmont Report
  (1979).
* **13. Frontier: measuring people, carefully.** Interference: 10,000 buyers and 3,000 items, treatment making buyers
  6 points keener (30% against 36%); the A/B test reports +5.4 points, launching to everyone gives +0.2; with ample
  supply the two agree (+6.0 and +5.9). Fixes: randomize markets, cities or time slots (switchbacks), clusters of
  friends (Ugander et al., 2013). Effects that take years: surrogate indices (Athey, Chetty, Imbens and Kang, 2019)
  and long-running holdouts. Measuring without looking: Warner's randomized response (1965), truthful with
  probability 0.75, otherwise a coin, local differential privacy with ε = ln 7 = 1.95; on a true rate of 20%, the mean
  error of an honest survey against the randomized one is 3.09 against 4.76 points for 100 people, 1.01 against 1.47
  for 1,000, 0.32 against 0.49 for 10,000 and 0.10 against 0.15 for 100,000, about one and a half times; RAPPOR (2014),
  Apple's keyboard statistics (2016), the 2020 US Census (central, not local). Models of the user: computational
  rationality, simulated users and language models as synthetic participants, adaptive interfaces. Four open problems
  and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs44.compute
python -m unittest tests.test_cs44_people
python tools/build.py cs44
```

## Problems, with solutions

1. **Fitts from submovements.** Derive Fitts's law from submovements whose endpoint error is proportional to the
   distance they cover, and say what sets the slope b.

   *Solution.* Let dₖ be the distance left after k submovements, d₀ = D. Each submovement aims at the centre and
   lands with an error proportional to the distance it covered, so dₖ₊₁ = σ|Zₖ|·dₖ with Zₖ independent and σ the
   relative precision of the hand (σ = 0.2, Zₖ standard normal, in our instrument). The movement ends at the first k
   with dₖ ≤ W/2, that is, when Σ log₂(1/(σ|Zᵢ|)) ≥ log₂(2D/W). Each submovement therefore delivers, on average,
   μ = E log₂(1/(σ|Z|)) = log₂(1/σ) − E log₂|Z| bits of the log₂(2D/W) the target asks for, and by the renewal theorem
   the number of submovements is N ≈ log₂(2D/W)/μ plus a constant (the last one overshoots the threshold). With a
   time t per submovement after a reaction time t₀, MT = t₀ + t·N ≈ a + b log₂(2D/W), Fitts's own form, with

   b = t/μ, so 1/b = μ/t bits per second.

   The slope is set by how long a correction takes and how precise it is: a quicker or more accurate hand has a
   smaller b; a is the reaction time plus the constant overshoot. (Crossman and Goodeve's deterministic version, each
   correction leaving a fixed fraction λ, gives b = t/log₂(1/λ).) Numbers: E ln|Z| = −(γ + ln 2)/2, so
   E log₂|Z| = −0.916 and μ = log₂ 5 + 0.916 = 3.24 bits per submovement; with t = 0.25 s, b ≈ 0.25/3.24 = 0.077 s per
   bit. Fitting the twenty simulated conditions against log₂(2D/W) gives 0.076, and simulating ratios D/W from 2⁴ to
   2²⁰ gives 0.077. Against MacKenzie's log₂(D/W + 1), the fit of chapter 1 gives 0.086: the two indices agree at
   D/W = 1 and differ by nearly one bit at large D/W, so MacKenzie's index spans a narrower range and the slope is
   steeper; the extra one is a choice of index, not a different hand.

2. **Questions and entropy.** Show that the best yes/no questioning for a menu with item probabilities pᵢ needs
   between H and H + 1 questions on average.

   *Solution.* A strategy of yes/no questions is a binary tree with the items at its leaves, and the answers to item
   i form a codeword of length lᵢ (its depth); no codeword is a prefix of another, so Kraft's inequality holds:
   Σ 2^(−lᵢ) ≤ 1. Lower bound: with S = Σ 2^(−lᵢ) and qᵢ = 2^(−lᵢ)/S,
   Σ pᵢlᵢ − H = Σ pᵢ log₂(pᵢ/2^(−lᵢ)) = Σ pᵢ log₂(pᵢ/qᵢ) − log₂ S ≥ 0, since the relative entropy is non-negative
   (Gibbs's inequality) and S ≤ 1. Upper bound: the lengths lᵢ = ⌈log₂(1/pᵢ)⌉ satisfy Σ 2^(−lᵢ) ≤ Σ pᵢ = 1, so a
   prefix code, and hence a questioning strategy, with those lengths exists; its mean is
   Σ pᵢ⌈log₂(1/pᵢ)⌉ < Σ pᵢ(log₂(1/pᵢ) + 1) = H + 1. The best strategy (Huffman's) is no worse than this one and no
   better than the bound, so H ≤ L* < H + 1. For chapter 2's menu, p = (0.70, 0.10, 0.10, 0.05, 0.05): H = 1.46 bits,
   the Huffman mean is 1.6 questions, and the lengths ⌈log₂(1/pᵢ)⌉ = (1, 4, 4, 5, 5) give 2.0, all inside
   [1.46, 2.46).

3. **Sample size.** Derive n ≈ 16σ²/δ² per arm for α = 0.05 and power 0.8, and the sample size for a 5% lift on a 5%
   conversion rate.

   *Solution.* With n users per arm and per-user variance σ², each arm's mean has variance σ²/n, and the independent
   arms' variances add, so the estimated difference d̂ is approximately normal with mean δ and
   SE = σ√(2/n). The test rejects when d̂/SE > z₀.₉₇₅ = 1.96 (the opposite tail contributes negligibly under the
   alternative). Power is P(d̂ > 1.96 SE) = Φ(δ/SE − 1.96); setting it to 0.8 = Φ(0.8416) gives
   δ/SE = 1.96 + 0.8416 = 2.8016, so δ² = 2.8016² · 2σ²/n and

   n = (1.96 + 0.8416)² · 2σ²/δ² = 15.70 σ²/δ² ≈ 16σ²/δ².

   For a conversion rate p = 0.05, σ² = p(1 − p) = 0.0475, and a 5% relative lift is δ = 0.05 × 0.05 = 0.0025, so
   n = 15.70 × 0.0475/0.0025² = 119,303 users per arm, about 239,000 in all; the rule of 16 gives 121,600. (Using the
   treated arm's own variance, 0.0525 × 0.9475, instead of the baseline's for both arms gives 122,121.) Our simulation
   at n = 119,302 found the lift in 78.9% of 2,000 experiments.

4. **CUPED.** Prove that CUPED's estimator is unbiased and that its variance is (1 − ρ²) times the plain one, for the
   optimal θ.

   *Solution.* The estimator is Δ̂_cv = (Ȳ_T − Ȳ_C) − θ(X̄_T − X̄_C), where X is measured before randomization.
   Because assignment is independent of X, both arms draw X from the same distribution, so E(X̄_T − X̄_C) = 0 and
   E Δ̂_cv = E(Ȳ_T − Ȳ_C) = Δ for every fixed θ: the adjustment cannot move the expected effect. (If X could be
   changed by the treatment, E(X̄_T − X̄_C) ≠ 0 and the adjustment would subtract part of the effect, hence the rule.)
   For the variance, each arm contributes Var(Y − θX)/n, and
   Var(Y − θX) = Var Y − 2θ Cov(X, Y) + θ² Var X, a parabola in θ with its minimum where the derivative
   −2 Cov(X, Y) + 2θ Var X vanishes: θ* = Cov(X, Y)/Var X, the regression slope. Substituting,
   Var(Y − θ*X) = Var Y − Cov(X, Y)²/Var X = Var Y·(1 − ρ²) with ρ = Cov(X, Y)/√(Var X Var Y), and the arms' variances
   add as before, so Var Δ̂_cv = (1 − ρ²) Var(Ȳ_T − Ȳ_C). In practice θ is estimated from the pooled data; the
   estimator is then unbiased up to a term of order 1/n, and its variance approaches the same limit. Our simulation
   measured ratios of 0.90, 0.74, 0.50 and 0.19 against the theory's 0.91, 0.75, 0.51 and 0.19 at ρ = 0.3, 0.5, 0.7
   and 0.9.

5. **Build.** Simulate daily peeking with a Bonferroni correction over 30 looks, and compare its power with the
   mixture SPRT.

   *Solution notes.* Add `bonferroni(days=30, per_day=1000, p=0.05, lift=0.0, alpha=0.05, trials=4000, seed=2)` to
   `experiments.py`, generating the two arms exactly as `msprt` does (the same calls on `default_rng(seed)`, so the
   same seed gives the same traffic); each day, compute the pooled z of `peeking` on the cumulative counts and stop at
   the first |z| > Φ⁻¹(1 − α/(2 · days)) = 3.14, the two-sided threshold for α/30 = 0.0017 per look. By the union
   bound the chance of any false rejection over the 30 looks is at most 5%, and it is lower because the looks share
   data. A run on the same 4,000 experiments as chapter 9 gives 1.75% false positives with no effect, against 0.4% and
   1.2% for the two mixtures, and for a real 10% lift a power of 44% within 30 days (median stop day 18), between the
   mixture tuned to 5% lifts (39%, day 22) and the one tuned to 10% lifts (51%, day 18); all three are far below the
   80% of a single look on day 30. The comparison is fair only up to day 30: Bonferroni must fix the number of looks
   in advance and cannot continue, while the mixture SPRT stays valid however long it runs. In z units the mixtures'
   boundaries are 9.90, 4.05 and 3.27 on days 1, 10 and 30 (τ for 5% lifts) and 5.47, 3.17 and 3.04 (τ for 10%
   lifts), against Bonferroni's flat 3.14. Group-sequential boundaries (Pocock's, O'Brien and Fleming's) spend α
   across a fixed schedule of looks more efficiently than Bonferroni, and are the natural next comparison; add each as
   a cached item in `compute.py` and a test that the null rejection rate stays below 0.05.

6. **★ Research.** An always-valid sequential test for experiments with interference.

   *Discussion.* Open. The mixture SPRT is valid because, under the null, the likelihood ratio built from independent
   users' outcomes is a non-negative martingale, and Ville's inequality bounds its supremum. Interference breaks each
   step: a user's outcome depends on others' assignments, so outcomes are not independent; "no effect" has several
   meanings (no direct effect, no spillover, no effect of the global launch), and the quantity an A/B difference
   estimates is not the effect of launching to everyone, as chapter 13's marketplace showed (+5.4 points against
   +0.2). One part is easy: under Fisher's sharp null that no assignment changes anyone's outcome, interference
   cannot exist, and a test martingale built from the randomization itself is valid however often it is checked. The
   open part is everything else: confidence sequences for the global effect under a model of interference, valid at
   every look; designs (clusters, switchbacks) that keep power when the clusters themselves arrive sequentially or
   interact weakly; and bounds on the bias when the interference model is wrong. A good partial answer would state an
   interference model (for example, exposure through a known graph or bounded carry-over in time), construct an
   always-valid test or confidence sequence for a stated estimand under it, prove its error rate, and measure its power
   against a fixed-horizon cluster-randomized test on a simulated marketplace such as chapter 13's.

## 习题与解答

1. **由子运动推出菲茨定律。** 设每次子运动的落点误差与它走过的距离成正比，推导菲茨定律，并说明斜率 b 由什么决定。

   *解答。* 设 dₖ 为 k 次子运动之后剩下的距离，d₀ = D。每次子运动瞄准目标中心，落点误差与它走过的距离成正比，所以
   dₖ₊₁ = σ|Zₖ|·dₖ，其中 Zₖ 相互独立，σ 是手的相对精度（在我们的仪器里 σ = 0.2，Zₖ 服从标准正态分布）。当第一次出现
   dₖ ≤ W/2，也就是 Σ log₂(1/(σ|Zᵢ|)) ≥ log₂(2D/W) 时，运动结束。所以每次子运动平均交付
   μ = E log₂(1/(σ|Z|)) = log₂(1/σ) − E log₂|Z| 比特，而目标要求的是 log₂(2D/W) 比特；由更新定理，子运动的次数
   N ≈ log₂(2D/W)/μ 加上一个常数（最后一次会越过阈值）。每次子运动用时 t，反应时间 t₀，则
   MT = t₀ + t·N ≈ a + b log₂(2D/W)，正是菲茨自己的形式，其中

   b = t/μ，即 1/b = μ/t 比特每秒。

   斜率由一次修正用多久、有多准决定：更快或更准的手，b 更小；a 是反应时间加上那个常数的越过量。（Crossman 和 Goodeve 的
   确定性版本中，每次修正剩下固定的比例 λ，得到 b = t/log₂(1/λ)。）数值：E ln|Z| = −(γ + ln 2)/2，所以
   E log₂|Z| = −0.916，μ = log₂ 5 + 0.916 = 3.24 比特每次子运动；t = 0.25 秒时，b ≈ 0.25/3.24 = 0.077 秒每比特。对二十个
   模拟条件按 log₂(2D/W) 拟合得 0.076，对 D/W 从 2⁴ 到 2²⁰ 的模拟得 0.077。按麦肯齐（MacKenzie）的 log₂(D/W + 1) 拟合，
   第一章得到 0.086：两种指数在 D/W = 1 时相同，在 D/W 很大时相差将近一比特，所以麦肯齐的指数跨度更窄、斜率更陡；多出来的
   这部分来自指数的选择，而不是手不同。

2. **提问与熵。** 证明：对于各项概率为 pᵢ 的菜单，最好的是非提问方式平均需要的问题数在 H 和 H + 1 之间。

   *解答。* 一种是非提问策略是一棵二叉树，各项在叶子上，第 i 项得到的回答构成长度为 lᵢ（它的深度）的码字；任何码字都不是
   另一个码字的前缀，所以克拉夫特不等式成立：Σ 2^(−lᵢ) ≤ 1。下界：令 S = Σ 2^(−lᵢ)，qᵢ = 2^(−lᵢ)/S，则
   Σ pᵢlᵢ − H = Σ pᵢ log₂(pᵢ/2^(−lᵢ)) = Σ pᵢ log₂(pᵢ/qᵢ) − log₂ S ≥ 0，因为相对熵非负（吉布斯不等式），且 S ≤ 1。上界：
   长度 lᵢ = ⌈log₂(1/pᵢ)⌉ 满足 Σ 2^(−lᵢ) ≤ Σ pᵢ = 1，所以存在具有这些长度的前缀码，也就存在相应的提问策略；它的平均值为
   Σ pᵢ⌈log₂(1/pᵢ)⌉ < Σ pᵢ(log₂(1/pᵢ) + 1) = H + 1。最好的策略（哈夫曼编码）不比它差，也不可能好过下界，所以
   H ≤ L* < H + 1。对第二章的菜单，p = (0.70, 0.10, 0.10, 0.05, 0.05)：H = 1.46 比特，哈夫曼平均 1.6 个问题，长度
   ⌈log₂(1/pᵢ)⌉ = (1, 4, 4, 5, 5) 给出 2.0，都在 [1.46, 2.46) 之内。

3. **样本量。** 推导在 α = 0.05、功效 0.8 时每组 n ≈ 16σ²/δ²，并求在 5% 的转化率上检测 5% 的提升所需的样本量。

   *解答。* 每组 n 个用户，每个用户的方差为 σ²，每组均值的方差为 σ²/n，两组相互独立，方差相加，所以估计的差 d̂ 近似服从
   均值为 δ、标准误 SE = σ√(2/n) 的正态分布。当 d̂/SE > z₀.₉₇₅ = 1.96 时拒绝（在备择假设下另一侧尾部的贡献可以忽略）。
   功效为 P(d̂ > 1.96 SE) = Φ(δ/SE − 1.96)；令它等于 0.8 = Φ(0.8416)，得 δ/SE = 1.96 + 0.8416 = 2.8016，于是
   δ² = 2.8016² · 2σ²/n，

   n = (1.96 + 0.8416)² · 2σ²/δ² = 15.70 σ²/δ² ≈ 16σ²/δ²。

   转化率 p = 0.05 时，σ² = p(1 − p) = 0.0475；5% 的相对提升是 δ = 0.05 × 0.05 = 0.0025，所以
   n = 15.70 × 0.0475/0.0025² = 119,303 人每组，共约 239,000 人；16 法则给出 121,600。（若实验组用它自己的方差
   0.0525 × 0.9475，而不是两组都用基线的方差，则得 122,121。）我们在 n = 119,302 时的模拟，在 2,000 次实验中有 78.9%
   检测到了这个提升。

4. **CUPED。** 证明 CUPED 的估计量是无偏的，并证明在最优 θ 下它的方差是普通估计量的 (1 − ρ²) 倍。

   *解答。* 估计量为 Δ̂_cv = (Ȳ_T − Ȳ_C) − θ(X̄_T − X̄_C)，其中 X 在随机分组之前测得。由于分组与 X 独立，两组的 X 来自同一
   分布，所以 E(X̄_T − X̄_C) = 0，对任意固定的 θ 都有 E Δ̂_cv = E(Ȳ_T − Ȳ_C) = Δ：调整不会移动效应的期望。（如果 X 会受
   处理影响，E(X̄_T − X̄_C) ≠ 0，调整就会减掉一部分效应，这就是那条规则的由来。）关于方差，每组贡献 Var(Y − θX)/n，而
   Var(Y − θX) = Var Y − 2θ Cov(X, Y) + θ² Var X 是 θ 的抛物线，在导数 −2 Cov(X, Y) + 2θ Var X 为零处取最小值：
   θ* = Cov(X, Y)/Var X，即回归斜率。代回得 Var(Y − θ*X) = Var Y − Cov(X, Y)²/Var X = Var Y·(1 − ρ²)，其中
   ρ = Cov(X, Y)/√(Var X Var Y)；两组方差照旧相加，所以 Var Δ̂_cv = (1 − ρ²) Var(Ȳ_T − Ȳ_C)。实践中 θ 由合并的数据估计；
   这时估计量的偏差是 1/n 阶的，方差趋于同一极限。我们的模拟在 ρ = 0.3、0.5、0.7、0.9 时测得的比值为 0.90、0.74、0.50、
   0.19，理论值为 0.91、0.75、0.51、0.19。

5. **动手。** 模拟对 30 次查看做 Bonferroni 校正的每日偷看，并把它的功效与混合序贯概率比检验（mSPRT）比较。

   *解答要点。* 在 `experiments.py` 里加上 `bonferroni(days=30, per_day=1000, p=0.05, lift=0.0, alpha=0.05, trials=4000,
   seed=2)`，像 `msprt` 那样生成两组数据（对 `default_rng(seed)` 做同样的调用，所以同一个种子给出同样的流量）；每天用
   `peeking` 的合并 z 检验处理累计计数，第一次出现 |z| > Φ⁻¹(1 − α/(2 · days)) = 3.14 时停止，这是每次查看 α/30 = 0.0017
   的双侧阈值。由并集上界，30 次查看中出现任何错误拒绝的概率至多为 5%，又因为各次查看共用数据，实际更低。在与第九章相同的
   4,000 次实验上运行：没有效应时假阳性为 1.75%，两种混合检验为 0.4% 和 1.2%；真实提升 10% 时，30 天内的功效为 44%
   （停止日的中位数为第 18 天），介于针对 5% 提升的混合检验（39%，第 22 天）和针对 10% 提升的混合检验（51%，第 18 天）
   之间；三者都远低于第 30 天只看一次的 80%。这个比较只在第 30 天之前公平：Bonferroni 必须事先定下查看次数，不能继续；而
   mSPRT 不论运行多久都有效。以 z 为单位，混合检验的边界在第 1、10、30 天为 9.90、4.05、3.27（τ 针对 5% 的提升）和 5.47、
   3.17、3.04（τ 针对 10% 的提升），而 Bonferroni 是平直的 3.14。成组序贯边界（Pocock 的、O'Brien 和 Fleming 的）按固定的
   查看计划分配 α，比 Bonferroni 更高效，是下一个自然的比较对象；把每一种都作为 `compute.py` 里的缓存项，并加上一个检验，
   确保零假设下的拒绝率低于 0.05。

6. **★ 研究。** 求一个适用于存在干扰的实验、始终有效的序贯检验。

   *讨论。* 尚未解决。mSPRT 之所以有效，是因为在零假设下，由相互独立的用户结果构造的似然比是一个非负鞅，维尔不等式约束了
   它的上确界。干扰破坏了每一步：一个用户的结果取决于别人的分组，所以结果不再独立；“没有效应”有好几种含义（没有直接效应、
   没有溢出效应、全面上线没有效应），而 A/B 差值估计的量并不是全面上线的效应，第十三章的市场就说明了这一点（+5.4 个百分点
   对 +0.2）。有一部分是容易的：在费希尔的尖锐零假设（任何分组都不改变任何人的结果）下，干扰不可能存在，由随机化本身构造的
   检验鞅不论查看多少次都有效。其余都是开放的：在某个干扰模型下、对全局效应、每次查看都有效的置信序列；当聚类本身按顺序
   到来、或彼此弱相互作用时仍保有功效的设计（聚类、轮换）；以及干扰模型错误时偏差的界。好的部分答案应当给出一个干扰模型
   （例如通过已知图的暴露，或时间上有界的延续效应），在其下为一个明确的估计量构造始终有效的检验或置信序列，证明它的错误率，
   并在第十三章那样的模拟市场上，把它的功效与固定期限的聚类随机化检验比较。

## Glossary additions

* **index of difficulty, Fitts's law, throughput** — log₂(D/W + 1) bits; MT = a + b·ID; 1/b, bits per second.
* **submovement, steering law** — one corrected piece of an aimed movement; T = a + b·A/W for paths through tunnels.
* **Hick–Hyman law, entropy of a choice** — decision time linear in log₂(n + 1), or in H for unequal probabilities.
* **GOMS, keystroke-level model (KLM), operator (K, P, B, H, M)** — goals, operators, methods and selection rules;
  predicting a task's time by adding operator times.
* **response-time thresholds, input latency** — 0.1, 1 and 10 s; the delay from an input to its effect on screen.
* **just-noticeable difference, Weber fraction, Weber–Fechner law** — the smallest detectable change; its ratio to the
  stimulus; sensation as the logarithm of stimulus.
* **preattentive feature, conjunction search, change blindness** — seen in parallel; found item by item; changes
  missed across a blank.
* **cone, metamer, CIE XYZ, sRGB, transfer curve (gamma), linear light** — the eye's three sensors; spectra that look
  alike; the standard observer; the web's colour space; code values to light; values proportional to light.
* **CIELAB, OKLab, perceptual distance** — spaces in which distance approximates visible difference.
* **protanopia, deuteranopia, tritanopia** — missing long, medium or short cones.
* **relative luminance, contrast ratio** — 0.2126R + 0.7152G + 0.0722B in linear light; (L₁ + 0.05)/(L₂ + 0.05).
* **outline, Bézier curve, rasterization, antialiasing, hinting, subpixel rendering, x-height** — how a glyph becomes
  pixels people can read.
* **screen reader, switch access, magnification, voice control, accessible name** — assistive technology and what it
  needs from software.
* **target size, universal design, curb-cut effect, POUR** — WCAG 2.2's 24 and 44 CSS pixels; design for the widest
  range; perceivable, operable, understandable, robust.
* **heuristic evaluation, think-aloud study, Nielsen–Landauer model** — inspection by experts; watching users;
  1 − (1 − L)ⁿ.
* **randomized controlled trial, A/B test, A/A test** — assignment by a coin; two versions; two identical versions.
* **two-proportion z-test, pooled rate, standard error, p-value** — the standard test for conversion rates.
* **false positive (α), false negative (β), power, sample size** — the two errors; 1 − β; n ≈ 16σ²/δ² per arm.
* **peeking, optional stopping, law of the iterated logarithm** — stopping at the first significant look; why a walk
  crosses any fixed line.
* **sequential probability ratio test, mixture SPRT, Ville's inequality, always-valid p-value** — tests safe to read at
  every look.
* **CUPED, covariate, stratification, regression adjustment** — removing variance the past explains.
* **multiple testing, Bonferroni correction, false discovery rate, Benjamini–Hochberg** — many metrics, and two ways to
  correct for them.
* **sample-ratio mismatch (SRM), Simpson's paradox, novelty and primacy effects, Twyman's law** — pitfalls of
  experiments at scale.
* **multi-armed bandit, Thompson sampling, regret** — shifting traffic while learning; conversions lost against the
  best arm.
* **north-star metric, driver metric, guardrail, overall evaluation criterion (OEC)** — what an experiment counts.
* **Goodhart's law, reward hacking, dark pattern** — a measure made a target; designs that trick people.
* **interference, cluster randomization, switchback** — units that affect each other; randomizing groups or time
  slots.
* **surrogate index, holdout** — predicting long-term outcomes; users kept on the old product.
* **randomized response, local differential privacy, ε** — deniable answers; the privacy loss of one answer.
* **computational rationality** — a user modelled as an agent optimizing under perceptual and memory limits.

## Sources

* D. Norman, *The Design of Everyday Things* (revised edn, 2013); S. Card, T. Moran and A. Newell, *The Psychology of
  Human-Computer Interaction* (1983); B. Shneiderman et al., *Designing the User Interface* (6th edn, 2016);
  I. S. MacKenzie, *Human-Computer Interaction: An Empirical Research Perspective* (2013); S. Krug, *Don't Make Me
  Think* (3rd edn, 2014); R. Kohavi, D. Tang and Y. Xu, *Trustworthy Online Controlled Experiments* (2020).
* D. Engelbart and W. English, "A research center for augmenting human intellect", AFIPS Fall Joint Computer
  Conference 1968.
* P. Fitts, "The information capacity of the human motor system in controlling the amplitude of movement", Journal of
  Experimental Psychology 1954; I. S. MacKenzie, "Fitts' law as a research and design tool in human-computer
  interaction", Human-Computer Interaction 1992; D. Meyer, R. Abrams, S. Kornblum, C. Wright and J. Smith, "Optimality
  in human motor performance: ideal control of rapid aimed movements", Psychological Review 1988; J. Accot and S. Zhai,
  "Beyond Fitts' law: models for trajectory-based HCI tasks", CHI 1997; R. W. Soukoreff and I. S. MacKenzie, "Towards
  a standard for pointing device evaluation", International Journal of Human-Computer Studies 2004.
* W. Hick, "On the rate of gain of information", Quarterly Journal of Experimental Psychology 1952; R. Hyman,
  "Stimulus information as a determinant of reaction time", Journal of Experimental Psychology 1953.
* S. Card, T. Moran and A. Newell, "The keystroke-level model for user performance time with interactive systems",
  Communications of the ACM 1980; D. Kieras, *Using the Keystroke-Level Model to Estimate Execution Times* (University
  of Michigan, 2001).
* R. Miller, "Response time in man-computer conversational transactions", AFIPS Fall Joint Computer Conference 1968;
  S. Card, G. Robertson and J. Mackinlay, "The information visualizer, an information workspace", CHI 1991; J. Nielsen,
  *Usability Engineering* (1993); A. Ng, J. Lepinski, D. Wigdor, S. Sanders and P. Dietz, "Designing for low-latency
  direct-touch input", UIST 2012; A. Treisman and G. Gelade, "A feature-integration theory of attention", Cognitive
  Psychology 1980; R. Rensink, J. K. O'Regan and J. Clark, "To see or not to see: the need for attention to perceive
  changes in scenes", Psychological Science 1997.
* B. Ottosson, "A perceptual color space for image processing" (2020); G. Machado, M. Oliveira and L. Fernandes, "A
  physiologically-based model for simulation of color vision deficiency", IEEE Transactions on Visualization and
  Computer Graphics 2009; IEC 61966-2-1 (sRGB); W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* (2023).
* R. Bringhurst, *The Elements of Typographic Style* (1992).
* World Health Organization, *Global Report on Health Equity for Persons with Disabilities* (2022).
* J. Nielsen and R. Molich, "Heuristic evaluation of user interfaces", CHI 1990; J. Nielsen, "Enhancing the
  explanatory power of usability heuristics", CHI 1994; J. Nielsen and T. Landauer, "A mathematical model of the
  finding of usability problems", INTERCHI 1993; C. Lewis, "Using the 'thinking-aloud' method in cognitive interface
  design", IBM Research Report RC 9265, 1982; K. A. Ericsson and H. Simon, *Protocol Analysis: Verbal Reports as Data*
  (1984).
* R. A. Fisher, *The Design of Experiments* (1935); R. Kohavi, R. Longbotham, D. Sommerfield and R. Henne, "Controlled
  experiments on the web: survey and practical guide", Data Mining and Knowledge Discovery 2009; A. Gelman and
  J. Carlin, "Beyond power calculations: assessing type S (sign) and type M (magnitude) errors", Perspectives on
  Psychological Science 2014.
* A. Wald, *Sequential Analysis* (1947); H. Robbins, "Statistical methods related to the law of the iterated
  logarithm", Annals of Mathematical Statistics 1970; J. Ville, *Étude critique de la notion de collectif* (1939);
  R. Johari, P. Koomen, L. Pekelis and D. Walsh, "Peeking at A/B tests: why it matters, and what to do about it",
  KDD 2017.
* A. Deng, Y. Xu, R. Kohavi and T. Walker, "Improving the sensitivity of online controlled experiments by utilizing
  pre-experiment data", WSDM 2013; W. Lin, "Agnostic notes on regression adjustments to experimental data:
  reexamining Freedman's critique", Annals of Applied Statistics 2013.
* Y. Benjamini and Y. Hochberg, "Controlling the false discovery rate: a practical and powerful approach to multiple
  testing", Journal of the Royal Statistical Society B 1995; E. Simpson, "The interpretation of interaction in
  contingency tables", Journal of the Royal Statistical Society B 1951.
* W. Thompson, "On the likelihood that one unknown probability exceeds another in view of the evidence of two
  samples", Biometrika 1933; M. Strathern, "'Improving ratings': audit in the British University system", European
  Review 1997; A. Kramer, J. Guillory and J. Hancock, "Experimental evidence of massive-scale emotional contagion
  through social networks", PNAS 2014; National Commission for the Protection of Human Subjects, *The Belmont Report*
  (1979).
* J. Ugander, B. Karrer, L. Backstrom and J. Kleinberg, "Graph cluster randomization: network exposure to multiple
  universes", KDD 2013; S. Athey, R. Chetty, G. Imbens and H. Kang, "The surrogate index: combining short-term proxies
  to estimate long-term treatment effects more rapidly and precisely", NBER working paper, 2019.
* S. Warner, "Randomized response: a survey technique for eliminating evasive answer bias", Journal of the American
  Statistical Association 1965; Ú. Erlingsson, V. Pihur and A. Korolova, "RAPPOR: randomized aggregatable
  privacy-preserving ordinal response", CCS 2014.
