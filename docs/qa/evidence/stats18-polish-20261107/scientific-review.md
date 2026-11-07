# Part 18 scientific source review

Reviewed all 12 chapters, the README/solutions, all ten compute items, local helpers and the survey toolkit. All ten compute items were refreshed and all 12 scene classes import. Six reference regressions and eight existing survey toolkit checks pass.

- Horvitz–Thompson's constant-contribution, zero-variance ideal now states fixed sample size and feasible positive inclusion probabilities. Exhaustive Poisson-sample enumeration demonstrates the remaining random-size variance; pairwise inclusion conditions for variance estimation are explicit.
- Meng's identity is independently checked. Its displayed effective size compares realized squared error with an approximate small-fraction SRS variance; it is not labeled the MSE of an unspecified sampling mechanism. The cited 2.3-million example is hypothetical, inferred from the CCES defect correlation, rather than an actual CCES sample of that size.
- The island lottery now draws 1,000 actual adults without replacement and highlights their towns. The old animation selected only 25 distinct towns with different inclusion probabilities. Design-based expectation/variance is distinguished from the regularity needed for approximate normal intervals, and association is distinguished from causal effect.
- Largest-remainder integer allocations preserve n = 1,000. Formula and simulation now use the same allocations, and the SRS comparator includes its finite-population correction. An independent small-population enumeration checks the stratified variance. Post-stratification needs populated cells and appropriate response assumptions.
- The cluster illustration intentionally retains unequal person inclusion from uniform town draws and explicitly identifies its small-town bias. Kish's equal-cluster approximation is qualified. The PPS comparison describes a 174-fold SD reduction, rather than an ambiguous precision ratio; known town totals do not imply equal enumeration costs.
- The ratio scatter uses the exact cached observations behind the shown estimate. Off-viewport incomes are omitted rather than moved to the edge; fitted lines and Meng error curves are geometrically clipped without false plateaus. Ratio/GREG claims state denominator and asymptotic conditions rather than exact finite-sample unbiasedness.
- The raking animation now performs four full two-margin rounds and reports those same margins' discrepancy. It no longer displays the unrelated three-margin fit's history. The weighted Board SE is identified as a plug-in approximation, not a complete design variance. Coarse marginal raking can leave bias even when response is MAR in continuous predictors. Kish's weight-dispersion diagnostic is not a measure of selection bias or calibration gains.
- The phone draw and respondent inclusion probabilities are distinguished; the simulated response rates are not called identical. The Xbox case separates interviews and unique respondents. Historical election bars use a consistent two-candidate denominator, with all-vote Roosevelt share labeled separately.
- Twenty explanatory introductions now carry context headings; headings remain during the first derivation row. Visual verification follows.

Historical checks:

- Wang, Rothschild, Goel & Gelman (2015), [author-hosted paper](https://5harad.com/papers/forecasting-with-nonrepresentative-polls.pdf): 750,148 interviews, 345,858 unique respondents.
- Meng (2018), [CCES project summary](https://cces.gov.harvard.edu/publications/statistical-paradises-and-paradoxes-big-data-i-law-large-populations-big-data): hypothetical one-percent sample implied by the estimated defect correlation.
- Pew (2019), [response-rate report](https://www.pewresearch.org/short-reads/2019/02/27/response-rates-in-telephone-surveys-have-resumed-their-decline/): 6% in 2018; low response alone does not determine bias.
- [National Archives](https://www.archives.gov/electoral-college/1936) verifies the electoral result; the two-candidate bar uses rounded all-vote shares 36.54% and 60.80%, normalized before plotting.

This source receipt is not visual, continuous-listening or bilingual production approval.
