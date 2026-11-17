# Philosophy, Built — Part 16: Evidence by Numbers

Part 16 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of
statistics. The replication crisis (Open Science Collaboration 2015; Bem 2011; Amgen 2012); Fisher's lady tasting tea
and the p-value, Neyman and Pearson's errors and lemma, Jeffreys's Bayes factors, Fisher's fiducial argument, and
three verdicts from one coin (60 heads in 100: p = 0.057, no rejection at power 0.46, B₀₁ = 1.10); the feud and the
"null ritual"; the distribution of p under the null and an alternative, six misreadings each refuted by simulation,
confidence intervals and their fallacy, and the ASA statement (2016); base rates on a 1,000-person grid (PPV 9%), the
prosecutor's fallacy in R v. Sally Clark, People v. Collins (one in twelve million, yet a 42% chance of a second
matching couple), and Ioannidis's positive predictive value, recomputed; the garden of
forking paths on one noise data set (4 of 48 paths significant), a p-hacking simulator (5% → 37%), the winner's curse
(type M and type S errors), the replication record and its remedies; optional stopping (35% false rejections after
100 looks) against a likelihood-ratio stopper (5%), and the debate over intentions; the likelihood principle, the
binomial and negative-binomial coins (identical likelihoods, p = 0.073 and 0.033), Birnbaum's theorem proved on the
mixture experiment, and its Price List (the Wall's sixteenth brick); Lindley's paradox (z = 2 at n from 10 to a
million: B₀₁ from 0.54 to 135), why it happens, prior sensitivity and the Edwards–Lindman–Savage bound, the
Sellke–Bayarri–Berger bound and p < 0.005, and Bem re-analysed; Mayo's severity curves and the fallacies of rejection
and acceptance; Simpson's paradox at Berkeley (women ahead in 4 of 6 departments, behind overall), in COVID-19 case
fatality, and its causal reading; the reference class problem (Venn, Reichenbach, Hájek) and in machines; A/B testing,
peeking (31% false wins) against an e-process (4%), and group-sequential boundaries (Wald, Pocock, O'Brien–Fleming);
testing by betting, Kelly's growth rate, Ville's inequality proved and checked, and why e-values compose; and AIC
against BIC (Forster and Sober), with AIC's estimate tracking predictive accuracy.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/stats.py` (no SciPy:
its own normal and Student-t distributions), tested in `tests/philosophy/test_stats.py` and cached by
[`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy16.compute       # every computed item (under a minute; .cache/philosophy16)
python tools/build.py philosophy16 -q l                # 480p preview
python tools/build.py philosophy16                     # 1080p30 -> renders/philosophy16.mp4
python tools/qa_scene.py philosophy16 Betting          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Fisher (1935); the replication crisis; the plan. | — |
| 1 | `Schools` | Fisher (1925, 1935), Neyman and Pearson (1933), Jeffreys (1939); fiducial probability; the feud; the null ritual. | the lady tasting tea (1/70); α and β; three verdicts on 60 heads in 100 |
| 2 | `PValue` | the definition; six misreadings; confidence intervals (Neyman 1937; Morey et al. 2016); the ASA statement (2016). | p under null and alternative; each misreading simulated; 95 of 100 intervals |
| 3 | `BaseRate` | natural frequencies (Gigerenzer and Hoffrage 1995); Sally Clark; People v. Collins (1968); Ioannidis (2005). | a 1,000-person grid: PPV 9%; a second matching couple (42%); Ioannidis's table and PPV curves |
| 4 | `Garden` | forking paths (Gelman and Loken); Simmons, Nelson and Simonsohn (2011); Gelman and Carlin (2014); the replication record; remedies. | 48 analyses of one noise data set; the p-hacking simulator; type M and S errors |
| 5 | `Stopping` | optional stopping (Armitage et al. 1969); the stopping rule principle (Edwards, Lindman and Savage 1963); the debate. | a p-value path; rejection rate by number of looks; a likelihood-ratio stopper |
| 6 | `Likelihood` | Royall's three questions; the law of likelihood (Hacking 1965); **Birnbaum's theorem** (1962); **Price List**; **the Wall's sixteenth brick**. | binomial and negative binomial likelihoods and p-values |
| 7 | `Lindley` | Lindley's paradox (1957); prior sensitivity; Edwards–Lindman–Savage; Sellke–Bayarri–Berger (2001); Benjamin et al. (2018); Bem re-analysed. | B₀₁ against n at fixed z; B₀₁ against prior width; the bound table |
| 8 | `Severity` | Mayo's severity requirement; fallacies of rejection and acceptance; severity and the flat-prior posterior. | severity curves for a significant and a non-significant result |
| 9 | `Simpson` | Berkeley 1973 (Bickel et al. 1975); COVID-19 case fatality (von Kügelgen et al. 2021); the causal reading. | the six departments, aggregate and by department |
| 10 | `Reference` | Venn (1866); Reichenbach; Hájek (2007); reference classes in insurance, medicine, risk scores. | — |
| 11 | `AB` | A/B testing (Kohavi et al. 2020); peeking; Wald (1945), Pocock (1977), O'Brien–Fleming (1979), always-valid p (Johari et al. 2017). | 2,000 A/A tests with and without peeking; an e-process |
| 12 | `Betting` | Shafer and Vovk; e-values; Kelly (1956) and GROW; Ville's inequality (1939), proved; optional continuation. | wealth under the null and the alternative; growth curves; Ville checked |
| 13 | `Models` | AIC (1973) and BIC (1978); Forster and Sober (1994); consistency and efficiency. | training fit, AIC's estimate and predictive fit; which degree each picks |
| 14 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. Prevalence 0.1%, sensitivity 99%, false positives 1%: what share of positives are sick?

   *Solution.* In 100,000 people, 100 are sick and 99 of them test positive; 99,900 are well and 999 of them test positive. So $99/(99 + 999) = 9.0\%$ of positives are sick. The test is good; the base rate is low, so most positives are false.

2. For Ann's and Bo's coins, show that the Bayes factor under a uniform prior is the same.

   *Solution.* Ann's likelihood is $\binom{12}{9}\theta^9(1-\theta)^3$ and Bo's, for the third tail on the twelfth toss, is $\binom{11}{9}\theta^9(1-\theta)^3$: the same function of $\theta$ up to a constant. The Bayes factor for "the chance is uniform on $[0, 1]$" against "the coin is fair" is $\int_0^1 c\,\theta^9(1-\theta)^3\,d\theta \,\big/\, c\,(1/2)^{12}$, and the constant $c$ cancels. With the Beta integral $9!\,3!/13! = 1/2860$, both get $4096/2860 = 1.43$: weak evidence of bias, the same for both, where their $p$-values (0.073 and 0.033) disagreed.

3. Prove that under $H_0$ the $p$-value of a continuous test statistic is uniform on $[0, 1]$.

   *Solution.* Let the statistic $T$ have continuous distribution function $F_0$ under $H_0$, and $p = 1 - F_0(T)$. Then $F_0(T)$ is uniform on $[0, 1]$ (the probability integral transform: $P(F_0(T) \le u) = P(T \le F_0^{-1}(u)) = u$), so $P(p \le u) = P(F_0(T) \ge 1 - u) = u$ for every $u$: $p$ is uniform. That is why, under the null, a test at level $\alpha$ rejects with probability exactly $\alpha$, and why a pile of $p$-values from true nulls is flat.

4. If $E_1, E_2$ are independent e-values, is $E_1 E_2$ one? Is $(E_1 + E_2)/2$?

   *Solution.* Both are. For the product, independence gives $E[E_1E_2] = E[E_1]\,E[E_2] \le 1$ under the null, and the product is nonnegative. (It is also valid when $E_2$ is an e-value conditionally on the first study's data, which is how betting continues a study.) For the average, linearity alone gives $E[(E_1 + E_2)/2] \le 1$, with no independence needed. The product grows fast when both studies point the same way; the average is the safe choice when the studies may be dependent.

5. Compute Lindley's $B_{01}$ for $z = 3$, $n = 10^4$, $\tau = 1$. Which way does it point?

   *Solution.* With known unit variance and $\theta \sim N(0, \tau^2)$ under $H_1$, $B_{01} = \sqrt{1 + n\tau^2}\,\exp\!\big(-\tfrac{z^2}{2}\cdot\tfrac{n\tau^2}{1 + n\tau^2}\big)$. For $z = 3$, $n = 10^4$, $\tau = 1$: $\sqrt{10001} \times e^{-4.4996} = 100.0 \times 0.0111 = 1.11$. A three-sigma result ($p = 0.0027$) leaves the Bayes factor slightly in favour of the null: with ten thousand observations a real effect of the size the prior expects would give a far larger $z$, so $z = 3$ is about as likely under the null.

6. Reweight Berkeley's six departments by total applicants: who is admitted more?

   *Solution.* Weight each department by its total applicants (men and women together, 4,526 in all) and apply each sex's own admission rate there. Men: $\sum_d w_d\,r^{\text{men}}_d = 38.7\%$. Women: 43.0%. Women are admitted more, reversing the raw 44.5% against 30.4%: the gap in the raw table came from women applying to the departments that admitted few applicants of either sex.

## Sources

Texts: Royall, *Statistical Evidence: A Likelihood Paradigm* (1997); Hacking, *Logic of Statistical Inference*
(1965); Mayo, *Statistical Inference as Severe Testing* (2018); Sober, *Evidence and Evolution* (2008), ch. 1; Berger
and Wolpert, *The Likelihood Principle* (2nd ed. 1988); Shafer and Vovk, *Game-Theoretic Foundations for Probability
and Finance* (2019); Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (2020); Gigerenzer,
*Calculated Risks* (2002).

Papers: Fisher (1925, 1930); Neyman and Pearson (1933); Neyman (1937); Jeffreys (1939); Ville (1939); Wald (1945);
Lindley (1957); Birnbaum (1962); Edwards, Lindman and Savage (1963); Armitage, McPherson and Rowe (1969); Akaike
(1973); Bickel, Hammel and O'Connell (1975); Schwarz (1978); Forster and Sober (1994); Sellke, Bayarri and Berger
(2001); Ioannidis (2005); Hájek (2007); Simmons, Nelson and Simonsohn (2011); Gelman and Carlin (2014); Mayo (2014);
Open Science Collaboration (2015); Wasserstein and Lazar (2016); Johari et al. (2017); Benjamin et al. (2018);
Shafer (2021); Ramdas et al. (2023); Grünwald, de Heide and Koolen (2024).
