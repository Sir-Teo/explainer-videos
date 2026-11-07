# Part 13: Experiments by Design — scientific source review

Reviewed all 15 scenes, the README and problem solutions, all 15 compute items, the local drawing helpers and the design toolkit. All scene modules import. The full compute refresh completed, followed by a refresh of the field item after adding its analytic effective plot variance.

The review removes p-value selection from the blocking example: the first seeded replicate now appears regardless of significance (RCBD p = 0.189, versus 0.968 when blocks are ignored). The all-replicate power comparison remains separate. It seeds Dunnett integration, aligns unadjusted contrast p-values with the pooled ANOVA error, omits constant defining columns from fractional contrasts, and distinguishes every displayed subset from full-run summaries.

Scientific corrections cover normal-theory assumptions versus sharp-null randomization, independent symmetric signs for Darwin’s nonrandomized pairs, the denominator correction in the mean of F, mixed nutrient changes in the planned contrasts, Latin-square permutation classes, high-minus-low interaction coding, complementary fractions, admissible Plackett–Burman run counts, five-level central composite designs, approximate versus integer optimal designs, and approximate power/MDE calculations. CUPED now allows finite-sample fitted-adjustment bias and labels asymptotic inference; sample-ratio mismatch is a diagnostic flag. Curves are geometrically clipped without flattening their off-scale values.

Seven new independent checks plus the existing design toolkit checks pass **15 tests**. References include statsmodels linear-model contrasts and block tests, paired whole-plot t tests, explicit alias contrasts, rotatable prediction variance, the optimal-design equivalence bound and exhaustive randomization probabilities.

English visual verification is in progress. No bilingual production approval: Chinese tables, continuous listening/playback and final narrated masters remain open.
