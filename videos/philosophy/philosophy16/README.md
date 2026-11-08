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
