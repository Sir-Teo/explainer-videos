# Philosophy, Built — Part 35: The Right and the Good

Part 35 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*: normative
ethics, the three great theories made precise enough to compute. Three questions (what is good, what is right, how
should I be) and the PhilPapers 2020 split (virtue 37%, deontology 32%, consequentialism 31%). Bentham (1789) and his
felicific calculus kept as a ledger (keep the promise, +26.5 against −21.9); Mill's higher pleasures (1863); Sidgwick
(1874) and the dualism of practical reason; rules against calculation, simulated on 200,000 promise cases: a perfect
act utilitarian gains 0.083 a case, an unbiased one falls below the rule at noise 0.9 and a self-serving one at 0.5,
while Hare's two-level thinker (1981) stays above it to noise 1.5; Hooker's rule consequentialism (2000) and Smart's
rule worship. Theories of welfare (Parfit 1984), the experience machine (Nozick 1974; 77% would not enter; De Brigard
2010), and sour grapes (Elster 1983): desire satisfaction climbs back to 0.98 while the capability index stays at 0.2
(Sen; Nussbaum 2000). Harsanyi's aggregation theorem (1955), with the ex-ante and ex-post egalitarian rules each broken
as it predicts (Diamond 1967), and the utility possibility frontier with its utilitarian (1/2, 3/4), egalitarian and
Nash points. Distribution: sums, priority (Parfit 1991), maximin, Gini and Atkinson; levelling down; Nozick's utility
monster, given 90.9 of 100 units by the sum (k²/(k² + n)), 31.7 by priority and 0.1 by maximin; Singer's pond (1972)
with logarithmic welfare: equalize at a gift of 24,750, give 89% under full compliance and 98% alone, Murphy's
cooperative principle (2000) still 89%, Scheffler's prerogative (1982) 4,091 at M = 10; demandingness and Williams's
integrity (1973). Kant's formulas (1785) and a toy world of promises in which universal lying collapses trust to
0.008; the humanity formula as O'Neill's consent test (1985), with Parfit's gangster and Korsgaard's *Fellow
Creatures* (2018). Universalizability tested on five maxims: two hits, two false positives, one false negative;
Constant, Kant and the murderer at the door (1797), with Korsgaard's two-level reading (1986); Korsgaard, Herman and
Parfit's convergence. Ross's prima facie duties (1930); doing and allowing (Rachels 1975; Quinn 1989; Kagan's additive
fallacy, 1988); the paradox of deontology (Nozick 1974; Scheffler 1982) and consequentializing it (k > 5), and **the
Wall's thirty-fifth brick**. The trolley problem (Foot 1967; Thomson 1985, 2008), double effect, the loop and the
trapdoor (Greene et al. 2009), a **Price List** with the PhilPapers shares (switch 63%, push 22%), and the Moral Machine
(Awad et al. 2018). Contractualism (Scanlon 1998); Taurek's numbers (1977), with each person's chance under saving the
many, a coin and a weighted lottery (5, 3 and 4.33 saved), and the tie-breaking reply (Kamm; Scanlon); the Transmitter
Room and partial aggregation (Voorhoeve 2014). Virtue: Aristotle's mean, eudaimonia and practical wisdom; particularism
(Dancy 2004), where the best fixed weighting of three reasons, out of 343, judges 17 of 27 cases by ignoring pleasure
and promises, and weights for the defeaters too (McKeever and Ridge 2006) fit all 27; Confucius and Mencius;
situationism (Darley and Batson 1973; Milgram 1963; Harman; Doris). Care (Gilligan 1982; Noddings 1984; Held; Kittay;
Tronto) and one thought too many (Williams 1976; Railton 1984; Wolf 1982). Moral uncertainty (MacAskill, Bykvist and
Ord 2020): expected choiceworthiness on the footbridge flips with normalization, a compromise option wins every method
while a voting parliament pushes (Newberry and Ord 2021), and the value of moral information is 0.8, four times the
best choice now.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/ethics.py` (with `prop`
for the Price List), tested in `tests/philosophy/test_ethics.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy35.compute       # every computed item (seconds; .cache/philosophy35)
python tools/build.py philosophy35 -q l                # 480p preview
python tools/build.py philosophy35                     # 1080p30 -> renders/philosophy35.mp4
python tools/qa_scene.py philosophy35 Maxims           # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Kant's starry heavens; three questions; the plan. | the PhilPapers split |
| 1 | `Utility` | Bentham (1789); Mill (1863); Sidgwick (1874); Hare (1981); Hooker (2000); Smart. | the felicific ledger; act against rule under noise and bias |
| 2 | `Welfare` | Parfit (1984); Nozick (1974); De Brigard (2010); Elster (1983); Sen; Nussbaum (2000). | the experience machine survey; sour grapes |
| 3 | `Harsanyi` | Harsanyi (1955); Diamond (1967); Sen (1973). | two egalitarian rules broken; the frontier |
| 4 | `Distribution` | Parfit (1991); Atkinson (1970); Nozick (1974); Singer (1972); Murphy (2000); Scheffler (1982); Williams (1973). | five views of three societies; levelling down; the utility monster; the pond |
| 5 | `Kant` | Kant (1785); O'Neill (1985); Parfit; Korsgaard (2018). | the promise world; the consent test on seven acts |
| 6 | `Maxims` | Kant; Constant (1797); Korsgaard (1985, 1986); Herman (1993); Parfit (2011). | five maxims universalized |
| 7 | `Deontology` | Ross (1930); Rachels (1975); Quinn (1989); Kagan (1988); Nozick; Scheffler; Dreier; Portmore; **the Wall's thirty-fifth brick**. | the paradox, and the agent-relative weight that consequentializes it |
| 8 | `Trolley` | Foot (1967); Thomson (1985, 2008); Aquinas; Greene et al. (2009); Kamm; Awad et al. (2018); **the Price List**. | the trolley tetrad's minimal conflicts |
| 9 | `Contract` | Scanlon (1998); Taurek (1977); Timmermann (2004); Kamm; Voorhoeve (2014). | three lotteries on the rocks; the Transmitter Room |
| 10 | `Virtue` | Aristotle; Anscombe (1958); Hursthouse (1999); Dancy (2004); McKeever and Ridge (2006); Confucius; Mencius; Darley and Batson (1973); Milgram (1963); Harman; Doris. | every weighting of reasons, searched |
| 11 | `Care` | Kohlberg; Gilligan (1982); Noddings (1984); Held (2006); Kittay; Tronto; Williams (1976); Railton (1984); Wolf (1982). | — |
| 12 | `Uncertainty` | MacAskill, Bykvist and Ord (2020); Bostrom (2009); Newberry and Ord (2021). | expected choiceworthiness under three normalizations; a parliament; the value of moral information |
| 13 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The ledger's numbers and the promise cases' distribution are invented: what is computed is the structure. The
two-level thinker breaks a promise only when its estimate of the gain exceeds 2. The utility monster's resources are
split equally among the ten ordinary people, which is optimal for every view by symmetry and concavity. The pond's
welfare is the logarithm of income; Scheffler's prerogative multiplies your own welfare by M. The particularist judge
scores pleasure +1 (−1 if cruel), a promise +1 (0 if coerced) and a lie −2 (0 inside a game), and calls an act
permissible when the sum is at least 0; a defeater appears only with the reason it defeats, which leaves 27 cases.
The consent test counts deception and force as making consent impossible, as O'Neill does.

## Problems (solutions in the notes)

1. Show that W = min(E u₁, E u₂) violates the vNM independence axiom.
2. Find a distribution that maximin ranks above another although both totals and priority sums are lower.
3. In the promise world, find the largest share of liars for which lending never stops.
4. Write a maxim that the universal law test forbids though it is harmless, and explain why.
5. For what agent-relative weight k does the constraint against killing one to save n hold? (k > n.)
6. Show that range normalization can reverse a verdict of variance normalization.
