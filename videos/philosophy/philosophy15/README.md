# Philosophy, Built — Part 15: The Problem of Induction

Part 15 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): can the past tell us anything
about the future, and if no argument shows that it can, what can be said for learning from experience? Russell's
chicken; Hume's argument and the circle, Hume's custom, Black's rule-circularity and Salmon's counterinductive
mirror, Strawson and Goodman; Laplace's rule of succession and the sunrise, de Finetti's representation theorem, and
Carnap's λ-continuum; the Nyāya five-membered inference, Dignāga's wheel of reasons (checked on nine small
universes) and the Cārvāka challenge; Hempel's ravens as a Price List, with Good, Scheffler and Goodman, and the
Bayesian accounting (a raven is worth about nine thousand shoes); firmness versus increase, six confirmation measures
that rank two pieces of evidence oppositely (Fitelson), and Glymour's old evidence; Goodman's grue, its symmetry, one
learner under two encodings, and grue reproduced in eight small neural networks that fit the data identically and
disagree after T; Popper's falsification, Duhem and Quine (Neptune and Vulcan), verisimilitude and the Miller–Tichý
theorem (checked over all 32,258 pairs on three atoms), Tichý's likeness and Miller's translation that reverses it,
and Salmon's bridge; inference to the best explanation (Peirce, Semmelweis, Harman, Lipton), van Fraassen's bad lot
and Dutch book, and Douven's race between an explanationist and a Bayesian; merging of opinions (Blackwell–Dubins),
Cromwell's rule, Doob and Belot; learning in the limit, Gold's theorem by adversary, Putnam's diagonal against
Laplace, and Kelly's hierarchy of empirical questions; Ockham's razor, Kelly's retraction game and efficiency theorem,
and the Bayesian Occam factor; Solomonoff's universal prior, a toy mixture over 510 programs, and its catches; code
lengths, two-part MDL (Rissanen) and compression in modern learning; Wolpert's no free lunch, proved on all 256
worlds over three bits (the Wall's fifteenth brick), its positive side in VC dimension and PAC learning, and what each
learner bets on; and Reichenbach's pragmatic vindication, its objections, and Schurz's meta-induction with its
worst-case regret bound.

Every verdict on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/induction.py`:
Laplace's rule and the sunrise, the wheel of reasons, the ravens' Bayes factors, the confirmation measures, grue under
two encodings, the Miller–Tichý search and Miller's translation, Douven's explanationist, merging, Gold's adversary,
Putnam's diagonal, Kelly's retraction game, the toy universal prior, MDL, no free lunch (all worlds and the proof
slice), VC shattering, the straight rule and the meta-inductor. The networks of the grue chapter are trained in
[`compute.py`](compute.py). Tested in `tests/philosophy/test_induction.py`.

## Build it

```bash
python -m videos.philosophy.philosophy15.compute       # every computed item (about ten seconds; .cache/philosophy15)
python tools/build.py philosophy15 -q l                # 480p preview
python tools/build.py philosophy15                     # 1080p30 -> renders/philosophy15.mp4
python tools/qa_scene.py philosophy15 Lunch            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Russell's chicken (1912); the plan. | — |
| 1 | `Hume` | Hume (1748): the argument and the circle; custom; Black (1958), Salmon's counterinductivist, Strawson (1952), Goodman; six kinds of answer. | — |
| 2 | `Laplace` | the rule of succession (Bayes 1763, Laplace 1814); the sunrise; de Finetti (1937); Carnap's continuum (1952). | odds of 1,826,214 to 1; exchangeable orderings at 1/30; four λ-curves |
| 3 | `Wheel` | the Nyāya inference; vyāpti; Dignāga's hetucakra (c. 480); the Cārvāka challenge, Dharmakīrti, Gaṅgeśa. | nine universes: 2 good, 2 contradictory, 5 inconclusive |
| 4 | `Ravens` | Hempel (1945); **Price List**: Nicod, equivalence, the white shoe; Good (1967); the Bayesian accounting. | Bayes factors 1.0101 and 1.0000011 |
| 5 | `Measures` | firmness vs increase (Carnap); six measures; Fitelson's measure sensitivity; old evidence (Glymour 1980). | six measures on two pieces of evidence: three each way |
| 6 | `Grue` | Goodman (1955); the symmetry of grue and green; grue in neural networks; entrenchment, natural kinds, inductive bias. | one learner, two encodings; eight networks that agree before T and not after |
| 7 | `Popper` | falsification (1934); Duhem and Quine; Neptune and Vulcan; Lakatos; verisimilitude (1963), Miller and Tichý (1974); Salmon (1981). | no false theory closer than another in 32,258 pairs; Tichý's likeness and Miller's flip |
| 8 | `Explain` | abduction (Peirce 1903); Semmelweis; Harman (1965), Lipton (2004); van Fraassen (1989); Douven (2013); Greaves and Wallace (2006). | a thousand races: speed, false confidence, Brier inaccuracy |
| 9 | `Merging` | washing out of priors; Blackwell and Dubins (1962); Cromwell's rule; Diaconis and Freedman (1986); Doob; Belot (2013). | Ann and Bo merge (gap 0.8 → 0.02); Cy never learns |
| 10 | `Gold` | identification in the limit (Putnam, Gold 1965); Gold (1967); Putnam's diagonal (1963); Kelly's hierarchy (1996). | the adversary: 29 mind changes in 30 steps; Laplace wrong 24 times of 24 |
| 11 | `Ockham` | Ockham's razor; Kelly's retraction game and Ockham efficiency theorem (2007); the Bayesian Occam factor (Jefferys and Berger 1992, MacKay). | three retractions against none |
| 12 | `Solomonoff` | the universal prior (1964); Solomonoff's error bound; incomputability; machine-relativity; approximations. | a mixture over 510 programs learning 011011… |
| 13 | `MDL` | Shannon's code lengths; two-part MDL (Rissanen 1978); AIC and BIC; double descent; PAC-Bayes; language models as compressors. | polynomial fits of degree 0–8; code lengths minimal at the true degree |
| 14 | `Lunch` | **no free lunch** (Wolpert 1996), proved; smooth worlds; VC dimension and PAC learning; **the Wall's fifteenth brick**; inductive biases. | 16 consistent worlds; four learners on 256 worlds; shattering by thresholds and intervals |
| 15 | `Reichenbach` | the pragmatic vindication (1938); the straight rule; three objections; meta-induction (Schurz 2008) and its regret bound. | the straight rule converging; exponential weights over five methods, regret within the bound |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Hume, *An Enquiry concerning Human Understanding* (1748), §4; Skyrms, *Choice and Chance* (4th ed. 2000);
Howson and Urbach, *Scientific Reasoning: The Bayesian Approach* (3rd ed. 2006); Goodman, *Fact, Fiction, and
Forecast* (1955); Popper, *The Logic of Scientific Discovery* (1959); Lipton, *Inference to the Best Explanation*
(2nd ed. 2004); Kelly, *The Logic of Reliable Inquiry* (1996); Li and Vitányi, *An Introduction to Kolmogorov
Complexity and Its Applications* (4th ed. 2019); Grünwald, *The Minimum Description Length Principle* (2007);
Shalev-Shwartz and Ben-David, *Understanding Machine Learning* (2014); Schurz, *Hume's Problem Solved* (2019);
Matilal, *The Character of Logic in India* (1998); Henderson, "The Problem of Induction" (SEP).

Papers: Hempel (1945); Carnap (1950, 1952); Black (1958); Blackwell and Dubins (1962); Putnam (1963); Solomonoff
(1964); Gold (1967); Good (1967); Miller (1974); Tichý (1974); Rissanen (1978); Glymour (1980); Salmon (1981);
Littlestone and Warmuth (1994); Wolpert (1996); Fitelson (1999); Greaves and Wallace (2006); Kelly (2007); Schurz
(2008); Douven (2013); Belot (2013); Delétang et al. (2024).
