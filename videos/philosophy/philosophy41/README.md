# Philosophy, Built — Part 41: Fair Machines

Part 41 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the first of the two
closing parts on the reasoners we build: fairness, discrimination, privacy and explanation in machines that decide.
The COMPAS dispute (ProPublica and Northpointe, 2016) with both sides' numbers; *State v. Loomis*; Dressel and Farid;
lending, hiring, health (Obermeyer et al. 2019) and faces (Buolamwini and Gebru 2018); the history of actuarial
prediction (Burgess 1928; Meehl 1954; Grove et al. 2000; Harcourt's *Against Prediction*) and pretrial reform (New
Jersey 2017; California's Proposition 25, 2020). Independence, separation and sufficiency (Barocas, Hardt and
Narayanan), their incompatibilities and exceptional cases, with **a threshold swept across two calibrated populations built by the Reasoner** (base rates 30% and
50%; false-positive rates about 10% and 30% at 0.5); what the label measures (Lum and Isaac; Ensign et al.; Jacobs and
Wallach). **Chouldechova's identity derived on screen and checked**; **Kleinberg, Mullainathan and Raghavan's
calibration and balance computed**, and **their impossibility proved in four lines and checked on the population**
(base-rate odds 0.42 and 1.02 against y/(1−x) 0.43 and 0.99); a **Price List** for the trilemma — **the Wall's
forty-first brick**. **Group-specific thresholds searched** (equal false positives, equal precision) and **a ledger
of four policies** (one threshold makes the fewest errors; equal precision costs 168 more errors but misses 980 more
reoffenders; demographic parity costs 932 and reverses the gap); Corbett-Davies et al., Hardt, Price and Srebro,
fair training, multicalibration. Hedden's coins, Long, Hellman, Binns, Rawls and Roemer; *SFFA v. Harvard* (2023)
and Ho and Xiang; Friedler, Scheidegger and Venkatasubramanian's two worldviews. Individual fairness (Dwork et al.
2012); **counterfactual fairness on a structural causal model** (Kusner et al. 2017); Kohler-Hausmann and
path-specific effects; intersectionality (Crenshaw 1989) and fairness gerrymandering (Kearns et al. 2018). Disparate
treatment and impact (*Griggs*, 1971), statistical discrimination (Phelps; Arrow), **fairness through unawareness
tested** (a neighbourhood proxy labels 20% of A and 80% of B), Lippert-Rasmussen, Hellman (2008), Eidelson; audits;
insurance (Test-Achats 2011; GINA 2008). Differential privacy (Dwork, McSherry, Nissim and Smith 2006): the failure
of anonymization (Sweeney; Netflix; AOL), **the Laplace mechanism with its e^ε ratio checked**, **randomized response
simulated**, **basic and advanced composition**, **the Dinur–Nissim reconstruction attack run**, central and local
models, DP-SGD and its disparate cost. Contextual integrity (Nissenbaum 2010), the 2020 census, RAPPOR, Warren and
Brandeis, Rachels, Solove, Zuboff; memorization in large models (Carlini et al.), the right to erasure and machine
unlearning; notice and consent (McDonald and Cranor; Balkin's information fiduciaries). The GDPR and the EU AI Act;
**Shapley values and counterfactual explanations computed for a toy credit model**; recourse (Ustun et al.; Karimi
et al.; Venkatasubramanian and Alfano); Rudin, Slack et al., the Rashomon effect, Miller; mechanistic
interpretability (Olah et al.; Elhage et al.; Templeton et al.). Burrell's three opacities, computational
reliabilism, Matthias's responsibility gap, many hands, meaningful human control; model cards, datasheets, audits, the
AI Incident Database; moral crumple zones (Elish), automation bias, Green and Chen; NIST's AI RMF, ISO/IEC 42001 and
Canada's Directive on Automated Decision-Making.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/fairness.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_fairness.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy41.compute       # every computed item (seconds; .cache/philosophy41)
python tools/build.py philosophy41 -q l                # 480p preview
python tools/build.py philosophy41                     # 1080p30 -> renders/philosophy41.mp4
python tools/qa_scene.py philosophy41 Impossible       # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | the COMPAS question; four questions; the plan. | — |
| 1 | `Compas` | ProPublica; Northpointe; *Loomis*; Dressel and Farid; Obermeyer et al.; Buolamwini and Gebru; Burgess; Meehl; Grove et al.; Harcourt; pretrial reform. | — |
| 2 | `Criteria` | Barocas, Hardt and Narayanan; Lum and Isaac; Ensign et al.; Jacobs and Wallach. | a threshold swept across two populations |
| 3 | `Impossible` | Chouldechova; Kleinberg, Mullainathan and Raghavan; **the Wall's forty-first brick**. | the identity checked; calibration and balance; the four-line proof; **the Price List** |
| 4 | `Thresholds` | Corbett-Davies et al.; Hardt, Price and Srebro; Zafar et al.; Agarwal et al.; Hébert-Johnson et al. | group thresholds; the ledger of four policies |
| 5 | `Which` | Hedden; Long; Hellman; Binns; Rawls; Roemer; *SFFA v. Harvard*; Ho and Xiang; Friedler, Scheidegger and Venkatasubramanian. | — |
| 6 | `Individual` | Dwork et al.; Kusner et al.; Kohler-Hausmann; Chiappa; Nabi and Shpitser; Crenshaw; Kearns et al. | counterfactual predictions on a causal model |
| 7 | `Discrimination` | *Griggs*; Phelps; Arrow; Lippert-Rasmussen; Hellman; Eidelson; Gender Shades; Local Law 144; Test-Achats; GINA. | fairness through unawareness, tested |
| 8 | `Privacy` | Sweeney; Narayanan and Shmatikov; Dwork, McSherry, Nissim and Smith; Warner; Dinur and Nissim; Abadi et al.; Bagdasaryan et al. | the Laplace mechanism; randomized response; composition; reconstruction |
| 9 | `Context` | Nissenbaum; the 2020 census; RAPPOR; Warren and Brandeis; Rachels; Solove; Zuboff; Carlini et al.; *Google Spain*; Bourtoule et al.; McDonald and Cranor; Balkin. | — |
| 10 | `Explain` | the GDPR; Wachter, Mittelstadt and Floridi; the EU AI Act; Lundberg and Lee; Wachter, Mittelstadt and Russell; Ustun et al.; Karimi et al.; Venkatasubramanian and Alfano; Rudin; Slack et al.; Miller; Olah et al.; Elhage et al.; Templeton et al. | Shapley values; counterfactual explanations |
| 11 | `Responsibility` | Burrell; Durán and Formanek; Matthias; Thompson; Nissenbaum; Santoni de Sio and Mecacci; Mitchell et al.; Gebru et al.; Raji and Buolamwini; Elish; Skitka et al.; Green and Chen; NIST; ISO/IEC 42001. | — |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The conditional-independence criteria apply to the same prediction variable. A calibrated score can coexist with a separately adjusted binary decision. The Kleinberg trilemma uses equal class-average scores, not error rates of a different thresholded decision; for a binary prediction, those averages are its true-positive and false-positive rates. Perfect predictions and uninformative predictions are explicit exceptional cases in the pairwise comparisons.

The population has 20,000 people per group, each with a true risk drawn from a Beta distribution of concentration 4
and mean 0.3 (group A) or 0.5 (group B), and an outcome drawn from that risk (seed 2016); the score is the true risk,
so it is calibrated by construction. Group thresholds are searched on a grid of 181 points from 0.05 to 0.95. The
unawareness test gives each person a neighbourhood that matches their group with probability 0.8 (seed 1971) and
labels the riskier neighbourhood high risk. The counterfactual model is X = U − A + noise (seed 2017). Randomized
response simulates 2,000 respondents with true share 0.3 (seed 1965); the reconstruction attack hides 64 bits behind
256 noisy subset sums and solves by least squares (seed 2003).

## Problems and solutions

1. Derive Chouldechova's identity from the four cells of the confusion table.

   *Solution.* Write the four cells as TP, FP, FN, TN, with $N$ people in all, prevalence $p = (TP + FN)/N$, $\text{PPV} = TP/(TP + FP)$, $\text{FNR} = FN/(TP + FN)$ and $\text{FPR} = FP/(FP + TN)$. From the PPV, $FP = TP\,(1 - \text{PPV})/\text{PPV}$. From the FNR, $TP = (1 - \text{FNR})(TP + FN) = (1 - \text{FNR})\,pN$. And $FP + TN = (1 - p)N$. Dividing, $\text{FPR} = \dfrac{p}{1 - p}\cdot\dfrac{1 - \text{PPV}}{\text{PPV}}\cdot(1 - \text{FNR})$. So if two groups have equal PPV and equal FNR but different prevalence $p$, their false-positive rates must differ.

2. Show that a perfect predictor satisfies calibration and both balance conditions.

   *Solution.* A perfect predictor gives score $S = Y$. Calibration: among those scored 1, everyone reoffends, and among those scored 0, no one does, in every group, so $P(Y = 1 \mid S = s, A) = s$. Balance for the positive class: $E[S \mid Y = 1, A] = 1$ in every group; for the negative class, $E[S \mid Y = 0, A] = 0$ in every group. All three hold at once, which is one of the two escape routes from Kleinberg, Mullainathan and Raghavan's theorem (the other is equal base rates).

3. Why does a classifier that labels everyone high risk satisfy demographic parity?

   *Solution.* Demographic parity asks that the share labelled high risk be the same in every group. If everyone is labelled high risk, that share is 1 in every group, so parity holds. (So do equal false-positive rates, all 1, and equal false-negative rates, all 0.) The classifier is useless and harsh on everyone: parity is a constraint on how labels are spread across groups, not on whether they track anything, which is why it is usually paired with accuracy.

4. Compute ε for randomized response with a coin that shows heads with probability 3/4.

   *Solution.* Use Warner's protocol with the biased coin for both tosses: heads (probability $3/4$), answer truthfully; tails, toss again and say yes on heads. Then $P(\text{yes} \mid \text{trait}) = \tfrac34 + \tfrac14\cdot\tfrac34 = \tfrac{15}{16}$, $P(\text{yes} \mid \text{no trait}) = \tfrac14\cdot\tfrac34 = \tfrac{3}{16}$, $P(\text{no} \mid \text{no trait}) = \tfrac34 + \tfrac14\cdot\tfrac14 = \tfrac{13}{16}$ and $P(\text{no} \mid \text{trait}) = \tfrac{1}{16}$. The privacy loss is the largest log ratio: $\max(\ln 5, \ln 13) = \ln 13 \approx 2.56$, against $\ln 3$ for the fair coin. (If only the first coin is biased and the second is fair, the ratios are 7 both ways and $\varepsilon = \ln 7 \approx 1.95$.) More truth, less privacy.

5. Two queries with ε = 0.5 each: what is the total by basic composition?

   *Solution.* Basic composition adds the budgets: $0.5 + 0.5 = 1$. Two $0.5$-differentially private releases together are $1$-differentially private, which bounds the ratio of output probabilities with and without any one person by $e^1 \approx 2.72$.

6. Find the Shapley values of f = x₁x₂ at (1, 1) with baseline (0, 0).

   *Solution.* With baseline $(0, 0)$, average each feature's marginal contribution over the two orders of adding them. Adding $x_1$ first: $f(1, 0) - f(0, 0) = 0$; then $x_2$ adds $f(1, 1) - f(1, 0) = 1$. Adding $x_2$ first: it adds 0, then $x_1$ adds 1. So $\varphi_1 = \tfrac12(0 + 1) = \tfrac12$ and $\varphi_2 = \tfrac12$. They sum to $f(1, 1) - f(0, 0) = 1$ (efficiency), and the interaction, which neither feature produces alone, is split equally (symmetry).

