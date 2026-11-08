# Philosophy, Built — Part 17: Cause

Part 17 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the metaphysics and the
mathematics of causation. Does smoking cause cancer? (Doll and Hill, Fisher's gene, Cornfield's inequality.) Hume's two
definitions and al-Ghazālī's cotton eight centuries earlier; why regularity is not enough; Mill's methods run on a
table of fires, Mackie's INUS conditions computed from a Boolean model, and the selection of "the" cause (Hart and
Honoré); Lewis's counterfactual analysis, Suzy and Billy (late preemption), trumping, overdetermination, influence, and
the boulder against transitivity; Suppes's probability-raising and screening off, Hesslow's pills (two paths that
cancel), and Cartwright's effective strategies; Russell's "On the Notion of Cause", Woodward's interventions and
invariance; structural causal models, chains, forks and colliders, Berkson's paradox (0.00 → −0.66), and
d-separation on the sprinkler graph; the do-operator as graph surgery, the back-door criterion (naive 0.12, adjusted
0.20 = truth, and from 200,000 samples), the front door for smoking, tar and a hidden gene (0.342 = truth), and two
models with one distribution and two effects; Pearl's do-calculus, its three rules checked by d-separation along the
front-door derivation, completeness (Tian, Shpitser, Huang and Valtorta), and M-bias; the ladder of causation, the
firing squad on three rungs, twin networks, and the probabilities of necessity and sufficiency; Halpern and Pearl's
actual causation on six classic cases, the late-preemption Price List, normality, and degrees of responsibility; the
causal Markov condition, Reichenbach's common cause, Yule's nonsense correlations (40% of independent random-walk
pairs have |r| > 0.5), Bell's bound (2 against 2√2), and faithfulness; the PC algorithm from 20,000 samples, Meek's
rules, the Markov equivalence class (the Wall's seventeenth brick), and LiNGAM's escape from it; potential outcomes,
Rubin's perfect doctor and all 70 randomizations, the bridge to structural models, instruments (OLS 1.07, IV 0.49)
and difference in differences (Card and Krueger, +2.7); causal inference at work (CUPED, uplift, double machine
learning, invariant causal prediction, and language models); and Kim's exclusion argument as a Price List, with
Yablo's pigeon.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/causal.py` (structural
models, d-separation, the do-calculus's side conditions, Halpern–Pearl, PC), tested in
`tests/philosophy/test_causal.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy17.compute       # every computed item (a few seconds; .cache/philosophy17)
python tools/build.py philosophy17 -q l                # 480p preview
python tools/build.py philosophy17                     # 1080p30 -> renders/philosophy17.mp4
python tools/qa_scene.py philosophy17 Discovery        # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Doll and Hill (1950, 1954); Fisher's gene (1958); Cornfield (1959); the plan. | — |
| 1 | `Hume` | Hume (1739, 1748): two definitions; al-Ghazālī (1095); regularity is not enough; Kant. | — |
| 2 | `Mill` | Mill's methods (1843); Mackie's INUS conditions (1965); Hart and Honoré (1959). | agreement and difference on a table of fires; prime implicants and INUS |
| 3 | `Lewis` | Lewis (1973, 2000); Suzy and Billy (Hall 2004); trumping (Schaffer 2000); overdetermination; transitivity. | the but-for test on Suzy and Billy |
| 4 | `Prob` | Suppes (1970); screening off; Hesslow (1976); Cartwright (1979). | Hesslow's pills: P(T) 0.30 either way, direct effect 0.2 |
| 5 | `Intervene` | Russell (1913); Woodward (2003); invariance; manipulability and anthropocentrism. | — |
| 6 | `Graphs` | structural causal models (Wright 1921; Pearl 2000); chains, forks, colliders; Berkson; d-separation. | Berkson's paradox; seven d-separation queries |
| 7 | `Do` | the do-operator; the back-door criterion; the front-door formula; non-identifiability. | naive, adjusted and true effects, exact and sampled; the front door; two models, one distribution |
| 8 | `Calculus` | Pearl's three rules (1995); completeness (Tian and Pearl 2002; Shpitser and Pearl, Huang and Valtorta 2006); transportability; M-bias. | each rule's side condition along the front-door derivation; the bow arc; M-bias (0.30 → 0.22) |
| 9 | `Ladder` | association, intervention, counterfactuals; twin networks (Balke and Pearl 1994); PN and PS (Tian and Pearl 2000); the causal hierarchy theorem. | the firing squad on three rungs; PN 0.6, PS 0.375, PNS 0.3 |
| 10 | `Actual` | Halpern and Pearl (2005), modified (Halpern 2015); **Price List** for late preemption; normality (Halpern and Hitchcock 2015); responsibility (Chockler and Halpern 2004). | the definition on six classic cases; responsibility in four elections |
| 11 | `Markov` | the causal Markov condition (Spirtes, Glymour and Scheines 1993); Reichenbach (1956); Yule (1926); Sober (2001); Bell and CHSH; faithfulness (Meek 1995; Robins et al. 2003). | 11 parameters for 31; 2,000 random-walk pairs; all 16 local strategies |
| 12 | `Discovery` | PC (Spirtes and Glymour 1991); Meek's rules; **Verma and Pearl (1990), the Wall's seventeenth brick**; LiNGAM (Shimizu et al. 2006); FCI, GES, NOTEARS. | PC from 20,000 samples; the 3-graph equivalence class; residual dependence both ways |
| 13 | `Outcomes` | Neyman (1923), Rubin (1974), Holland (1986); SUTVA; Galles and Pearl (1998); Dawid (2000); Wright (1928); Card and Krueger (1994); Snow (1855). | the perfect doctor; all 70 randomizations; IV against OLS; difference in differences |
| 14 | `Industry` | CUPED (Deng et al. 2013); uplift; doubly robust and double ML; causal forests; invariant causal prediction (Peters et al. 2016); language models and causal benchmarks. | 400 simulated A/B tests; uplift against response targeting; coefficients across environments |
| 15 | `Mind` | Kim's exclusion argument (1998) as a **Price List**; Huxley, Sider, Bennett, List and Menzies; Yablo's pigeon (1992). | the Price List's five exits; proportionality on five shades |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Pearl, *Causality* (2000; 2nd ed. 2009); Pearl and Mackenzie, *The Book of Why* (2018); Spirtes, Glymour and
Scheines, *Causation, Prediction, and Search* (1993; 2nd ed. 2000); Woodward, *Making Things Happen* (2003); Halpern,
*Actual Causality* (2016); Paul and Hall, *Causation: A User's Guide* (2013); Imbens and Rubin, *Causal Inference for
Statistics, Social, and Biomedical Sciences* (2015); Hernán and Robins, *Causal Inference: What If* (2020); Peters,
Janzing and Schölkopf, *Elements of Causal Inference* (2017); Beebee, Hitchcock and Menzies (eds.), *The Oxford
Handbook of Causation* (2009); Kim, *Mind in a Physical World* (1998).

Papers: Hume (1739, 1748); Mill (1843); Russell (1913); Wright (1921, 1928); Neyman (1923); Yule (1926); Reichenbach
(1956); Hart and Honoré (1959); Mackie (1965); Suppes (1970); Lewis (1973, 2000); Rubin (1974); Hesslow (1976);
Cartwright (1979); Holland (1986); Verma and Pearl (1990); Spirtes and Glymour (1991); Yablo (1992); Balke and Pearl
(1994); Card and Krueger (1994); Pearl (1995); Meek (1995); Galles and Pearl (1998); Dawid (2000); Tian and Pearl
(2000, 2002); Sober (2001); Robins et al. (2003); Sider (2003); Bennett (2003); Chockler and Halpern (2004); Hall
(2004); Halpern and Pearl (2005); Shimizu et al. (2006); Shpitser and Pearl (2006); Huang and Valtorta (2006); Knobe
and Fraser (2008); List and Menzies (2009); Hitchcock and Knobe (2009); Deng et al. (2013); Andersen (2013); Halpern
(2015); Halpern and Hitchcock (2015); Peters, Bühlmann and Meinshausen (2016); Chernozhukov et al. (2018); Wager and
Athey (2018); Zheng et al. (2018); Imbens (2020); Bareinboim, Correa, Ibeling and Icard (2022); Cinelli, Forney and
Pearl (2022); Kıcıman et al. (2023); Jin et al. (2023, 2024); Zečević et al. (2023).
