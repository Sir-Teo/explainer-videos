# Psychology, Built: Part 22, Concepts and Categories

Is a penguin a bird? Everyone says yes, and everyone takes a little longer to say it than for a robin. This part
asks what you know when you know what a bird is. Definitions fail; two equations replace them, a prototype and a
memory of every member; six small problems show that attention has to learn; a table of confusions becomes a map in
which Roger Shepard finds a law of generalization he argued should hold for any mind; and then similarity itself is
questioned, by Amos Tversky's asymmetries, by networks of knowledge, by theories that override resemblance, by a
learner that needs only three examples, and by a machine that reads meaning from the company words keep.

Typicality on you and in Rosch's ratings; the classical view and Wittgenstein's games; family resemblance computed on
Psyche's bird table; fuzzy boundaries; Posner and Keele's dot patterns and Homa and Vosburgh's open data; the context
model and the generalized context model derived, with the 5-4 structure where they part from prototypes; Shepard,
Hovland and Jenkins's six problems on Nosofsky et al.'s 1994 open data, a delta-rule network that cannot learn them,
and ALCOVE fitted with and without attention learning; classical and non-metric scaling derived, with Ekman's colours
closing into Newton's circle and Rothkopf's Morse code mapped by length and rhythm; Shepard's law tested on that map
and derived from consequential regions; the metric axioms and their failures, the contrast model, and Tversky's count
of asymmetries rerun on the open table; the hierarchical network, its failures, spreading activation and the Semantic
Priming Project; the basic level and category utility; Rips's pizza, Barsalou's goals, Keil's raccoon and Gelman and
Markman's blackbird; the number game and the size principle; and word vectors from Jane Austen's novels, with their
neighbours, a map, an opposite in the wrong place, analogies, and the biases of larger corpora. The practice chapter
is diagnosis as a polythetic category, card sorting for navigation design, and categories in recommendation, search
and dataset labels; the frontier is representational similarity analysis, language models' judgements of colour and
pitch, one-shot learning, and the open questions.

## Where the numbers come from

| What | Source |
|---|---|
| Family resemblance and similarity to the prototype for eleven birds and a bat | Psyche's bird table (features by common knowledge, an illustration), item `birds` |
| Classification of prototypes, distortions, old items and random patterns for categories of 3, 6 and 9 | Homa and Vosburgh (1976), as packaged in catlearn 1.1, fetched by `explainer.psychology.opendata` and checked by SHA-256, item `homa` |
| The context model's and the prototype model's P(A) for the 16 items of the 5-4 structure | Psyche (`concepts.gcm_prob`, `prototype_prob`), item `gcm54` |
| Mean error in 16 blocks of 16 trials for the six problems, 40 learners each | Nosofsky, Gluck, Palmeri, McKinley and Glauthier (1994), as packaged in catlearn 1.1, item `shj` |
| ALCOVE fitted with attention learning (c 7.77, φ 1.82, λw 0.178, λα 0.466; SSE 0.209) and without (SSE 0.335); a delta-rule network | Psyche (`concepts.fit_alcove_shj`, `delta_rule_network`), 20 random orders per problem, item `shj` |
| Ekman's 14 colours from 434 to 674 nm, 31 raters; the non-metric map (stress 0.029) | Ekman (1954), as packaged in smacof 2.1-7; Psyche (`concepts.nonmetric_mds`), item `ekman` |
| Rothkopf's 36 Morse signals and 598 listeners; the map (stress 0.19); the exponential law (R² 0.71 in log g; a Gaussian −0.12) | Rothkopf (1957), smacof's asymmetric `morse2`; Psyche (`concepts.shepard_generalization`, `fit_exponential_law`), item `morse` |
| Consequential regions under four priors on size | Psyche (`concepts.consequential_region_gradient`), item `regions` |
| 69 students, 66 against 3; 21 pairs of countries; 555 Morse pairs of unequal length, 336, 181 and 38 | Tversky (1977), pp. 334 and 336 |
| The same count on the open table: 555, 336, 182 and 37, mean difference 3.2 points, sign test p ≈ 10⁻¹¹ | Psyche (`concepts.prominence_asymmetry`), item `morse` |
| Spreading activation from *robin* in an illustrative network | Psyche (`concepts.spreading_activation`), item `network` |
| 1,661 targets, 768 people, four universities; priming of about 19 ms in lexical decision and 6 in naming; first associates 26 and 20 ms against 42 and 60 in 2008 | Hutchison et al. (2013), the paper's method and discussion |
| Category utility at three levels of an illustrative taxonomy | Psyche (`concepts.category_utility`, `nested_world`), item `levels` |
| The number game after one, and two sets of four, examples | Psyche (`concepts.number_game`; 34 mathematical hypotheses and every range), item `numbers` |
| 729,322 words of six novels; 4,000 words; PPMI and a 100-dimensional SVD; neighbours, two analogies and a map | Jane Austen via janeaustenr 1.0.0 (Project Gutenberg texts); Psyche (`concepts.cooccurrence`, `ppmi_svd`, `neighbours`, `analogy`), item `austen` |
| LSA 64.4% on 80 TOEFL items; applicants 64.5% | Landauer and Dumais (1997) |
| 227 symptom sets meeting DSM-5's rule for a major depressive episode | Psyche (`concepts.polythetic_count`), item `cardsort` |
| 3,703 patients, 1,030 profiles of 12 symptoms, the commonest 1.8% | Fried and Nesse (2015), the paper's abstract and results |
| A card sort by 40 simulated people of 12 groceries | Psyche (`concepts.card_sort`, illustrative features), item `cardsort` |
| Ekman's colours against wavelength (ρ 0.77), cone excitations (0.65) and hue angle in the opponent plane (0.83; 0.91 with one fitted weight) | Psyche (`concepts.rsa`, `hue_angle_distances`; Part 13's cones and opponent channels), item `ekman` |
| Language models' similarity ratings against people's: pitch 0.92, colour 0.89, loudness 0.89, consonants 0.57, taste 0.54, timbre 0.42 | Marjieh, Sucholutsky, van Rijn, Jacoby and Griffiths (2024), the paper (arXiv 2302.01308v2) |
| One-shot classification errors of 3.3% (the model) and 4.5% (people) | Lake, Salakhutdinov and Tenenbaum (2015) |

## Built in this part

* `explainer/psychology/psyche/concepts.py`: the generalized context model and the prototype model; the six problems,
  ALCOVE with its fit and attention, and a delta-rule network; classical and non-metric scaling (SMACOF with monotone
  regression); Shepard's generalization measure, the exponential law and consequential regions; Tversky's contrast
  model and his asymmetry count; category utility in a nested world; spreading activation with a fan; the number
  game; co-occurrence, PPMI and the SVD, neighbours and analogies; RSA and hue angles; the polythetic count and a
  card sort. Tested in `tests/psychology/test_concepts.py`.
* `explainer/psychology/rdata.py`: a reader for R's XDR data files that reads data and never evaluates anything, so
  the classic datasets packaged in CRAN source packages can be used without R.
* `explainer/psychology/opendata.py` gains CRAN source tarballs with mirrors, one member read from a tarball without
  extracting it, and readers for Nosofsky et al. (1994), Homa and Vosburgh (1976), Ekman (1954), Rothkopf (1957) and
  Jane Austen's novels.
* The Ledger gains eight rows; the Archive eight datasets.
* The course's interactive is the number game: three rounds of examples, your judgements against the model's.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Members of a category differ reliably in how typical they are, and typical members are classified faster | Rips, Shoben and Smith 1973 | replicated |
| Objects are named, verified and first learned at a middle level of abstraction, the basic level | Rosch, Mervis, Gray, Johnson and Boyes-Braem 1976 | replicated |
| After learning distortions of a prototype, people classify the never-seen prototype as well as or better than the items they studied | Posner and Keele 1968 | replicated |
| Of the six ways to split eight three-feature objects four and four, Type I is learned fastest, then II, then III, IV and V, and VI slowest | Shepard, Hovland and Jenkins 1961 | replicated |
| Generalization falls off exponentially with distance in psychological space | Shepard 1957 | replicated |
| Similarity judgements are asymmetric: a less prominent thing is judged more similar to a prominent one than the reverse | Tversky 1977 | replicated, smaller |
| Knowledge is stored in a hierarchy of concepts with each property stored once, so checking a fact takes longer the more links it crosses | Collins and Quillian 1969 | failed |
| A word is recognized faster after a related word than after an unrelated one | Meyer and Schvaneveldt 1971 | replicated, smaller |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Kruschke (a model, fitted here),
Rips, Barsalou and Murphy and Medin (single studies and a theoretical paper, told as the case for theories), Keil,
Gelman and Markman and Medin and Ortony (development, Part 30), Xu and Tenenbaum with Tenenbaum and Griffiths (a model
and its test, described), Harris, Firth, Nida and Lin (the history of an idea), Landauer and Dumais, Caliskan et al.
and Harnad (a model's benchmark, a measurement of text and an argument), Fried and Nesse, Kotov et al. and DSM-5
(Part 39), Yang et al. (a dataset's audit), Marjieh et al. (Part 60), Lake et al., Peterson et al. and Lake and
Baroni (frontier models), Huth et al. (Part 49).

## Build it

```bash
python -m videos.psychology.psych22.compute            # every number (a few minutes; fetches three CRAN packages once)
python tools/qa_scene.py psych22 Attention             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych22 -q l   # the whole part, silent preview
python tools/build.py psych22                          # 1080p30 with narration
python tools/qa_scene.py psych22 Law --lang zh         # the Chinese edition of one chapter
python tools/make.py psych22                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 22                    # the lab: the 5-4 structure to Jane Austen's word vectors
python tools/check_ledger.py psych22                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's concepts module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Is a penguin a bird? | Typicality on you; Rosch's ratings; the questions; objectives |
| 1 | No definition | The classical view; Wittgenstein's games; family resemblance computed; fuzzy boundaries |
| 2 | The average member | Posner and Keele's dot patterns; Homa and Vosburgh's open data; the prototype model |
| 3 | Every member remembered | The context model; the GCM derived; the 5-4 structure; the debate |
| 4 | Six problems, and attention that learns | The six problems; the 1994 data; a delta-rule network's failure; ALCOVE derived and fitted |
| 5 | A map of similarity | Classical and non-metric scaling derived; Ekman's colour circle; Rothkopf's Morse map |
| 6 | A universal law of generalization | Shepard's claim; his bias-free measure; the law tested on Morse code; consequential regions derived |
| 7 | Similarity is not distance | The metric axioms; three failures; the contrast model derived; Tversky's count rerun; spaces or features |
| 8 | Knowledge as a network | Collins and Quillian's hierarchy; its failures; spreading activation; semantic priming at scale |
| 9 | Concepts as theories | The basic level; category utility derived; similarity is not enough; psychological essentialism |
| 10 | Learning a concept from a few examples | The number game; the size principle derived; the model's generalization; suspicious coincidences |
| 11 | Meaning from company | Harris and Firth; PPMI and the SVD derived; Austen's neighbours and map; LSA, analogies, bias, grounding |
| 12 | The Ledger | Typicality; the basic level; the prototype effect; the six problems; Shepard's law; asymmetry; the hierarchy; priming |
| 13 | In practice: taxonomies, diagnosis, recommendation | 227 ways to be depressed; a card sort; recommendation, search and labels |
| 14 | Frontier: concepts in minds and machines | RSA on Ekman's colours; language models' judgements; one-shot learning; open questions |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 23 |

## Sources

* E. Rosch, Cognitive representations of semantic categories, Journal of Experimental Psychology: General 104 (1975)
  192-233; E. Rosch and C. B. Mervis, Family resemblances, Cognitive Psychology 7 (1975) 573-605; L. J. Rips, E. J.
  Shoben and E. E. Smith, Journal of Verbal Learning and Verbal Behavior 12 (1973) 1-20.
* L. Wittgenstein, Philosophical Investigations (1953), §§ 66-67; M. E. McCloskey and S. Glucksberg, Natural
  categories: well defined or fuzzy sets?, Memory & Cognition 6 (1978) 462-472; J. A. Hampton, Cognition 65 (1998)
  137-165.
* M. I. Posner and S. W. Keele, Journal of Experimental Psychology 77 (1968) 353-363 and 83 (1970) 304-308; D. Homa
  and R. Vosburgh, JEP: Human Learning and Memory 2 (1976) 322-330.
* D. L. Medin and M. M. Schaffer, Context theory of classification learning, Psychological Review 85 (1978) 207-238;
  R. M. Nosofsky, JEP: General 115 (1986) 39-57; D. L. Medin and P. J. Schwanenflugel, JEP: HLM 7 (1981) 355-368; J.
  D. Smith and J. P. Minda, JEP: LMC 26 (2000) 3-27.
* R. N. Shepard, C. I. Hovland and H. M. Jenkins, Psychological Monographs 75 (1961) no. 13; R. M. Nosofsky, M. A.
  Gluck, T. J. Palmeri, S. C. McKinley and P. Glauthier, Memory & Cognition 22 (1994) 352-369; J. K. Kruschke,
  ALCOVE, Psychological Review 99 (1992) 22-44; K. J. Kurtz et al., JEP: LMC 39 (2013).
* W. S. Torgerson, Psychometrika 17 (1952) 401-419; R. N. Shepard, Psychometrika 27 (1962) 125-140 and 219-246; J.
  B. Kruskal, Psychometrika 29 (1964) 1-27; G. Ekman, Dimensions of color vision, Journal of Psychology 38 (1954)
  467-474; E. Z. Rothkopf, JEP 53 (1957) 94-101; J. de Leeuw and P. Mair, Multidimensional scaling using
  majorization: SMACOF in R, Journal of Statistical Software 31 (2009) 1-30.
* R. N. Shepard, Psychometrika 22 (1957) 325-345; R. N. Shepard, Toward a universal law of generalization for
  psychological science, Science 237 (1987) 1317-1323; C. R. Sims, Science 360 (2018) 652-656.
* A. Tversky, Features of similarity, Psychological Review 84 (1977) 327-352; A. Tversky and I. Gati, Studies of
  similarity, in Cognition and Categorization (1978) 79-98; C. M. Aguilar and D. L. Medin, Psychonomic Bulletin &
  Review 6 (1999) 328-337.
* A. M. Collins and M. R. Quillian, JVLVB 8 (1969) 240-247; C. Conrad, JEP 92 (1972) 149-154; A. M. Collins and E. F.
  Loftus, Psychological Review 82 (1975) 407-428; J. R. Anderson, Cognitive Psychology 6 (1974) 451-474; D. E. Meyer
  and R. W. Schvaneveldt, JEP 90 (1971) 227-234; M. Lucas, Psychonomic Bulletin & Review 7 (2000) 618-630; K. A.
  Hutchison et al., The semantic priming project, Behavior Research Methods 45 (2013) 1099-1114.
* E. Rosch, C. B. Mervis, W. D. Gray, D. M. Johnson and P. Boyes-Braem, Cognitive Psychology 8 (1976) 382-439; J. W.
  Tanaka and M. Taylor, Cognitive Psychology 23 (1991) 457-482; J. E. Corter and M. A. Gluck, Psychological Bulletin
  111 (1992) 291-303.
* G. L. Murphy and D. L. Medin, Psychological Review 92 (1985) 289-316; L. J. Rips, Similarity, typicality, and
  categorization, in Similarity and Analogical Reasoning (1989) 21-59; L. W. Barsalou, Memory & Cognition 11 (1983)
  211-227; F. C. Keil, Concepts, Kinds, and Cognitive Development (1989); S. A. Gelman and E. M. Markman, Cognition 23
  (1986) 183-209; D. L. Medin and A. Ortony, Psychological essentialism, in Similarity and Analogical Reasoning (1989).
* J. B. Tenenbaum, Rules and similarity in concept learning, NIPS 12 (2000); J. B. Tenenbaum and T. L. Griffiths,
  Behavioral and Brain Sciences 24 (2001) 629-640; F. Xu and J. B. Tenenbaum, Word learning as Bayesian inference,
  Psychological Review 114 (2007) 245-272.
* Z. S. Harris, Distributional structure, Word 10 (1954) 146-162; J. R. Firth, A synopsis of linguistic theory
  1930-1955 (1957); T. K. Landauer and S. T. Dumais, Psychological Review 104 (1997) 211-240; A. Caliskan, J. J.
  Bryson and A. Narayanan, Science 356 (2017) 183-186; S. Harnad, The symbol grounding problem, Physica D 42 (1990)
  335-346.
* E. I. Fried and R. M. Nesse, Journal of Affective Disorders 172 (2015) 96-102; R. Kotov et al., The Hierarchical
  Taxonomy of Psychopathology (HiTOP), Journal of Abnormal Psychology 126 (2017) 454-477; K. Yang, K. Qinami, L.
  Fei-Fei, J. Deng and O. Russakovsky, Towards fairer datasets, FAT* (2020) 547-558.
* N. Kriegeskorte, M. Mur and P. Bandettini, Representational similarity analysis, Frontiers in Systems Neuroscience 2
  (2008) 4; R. Marjieh, I. Sucholutsky, P. van Rijn, N. Jacoby and T. L. Griffiths, Large language models predict
  human sensory judgments across six modalities, Scientific Reports 14 (2024); B. M. Lake, R. Salakhutdinov and J.
  B. Tenenbaum, Science 350 (2015) 1332-1338; J. C. Peterson, J. T. Abbott and T. L. Griffiths, Cognitive Science 42
  (2018) 2648-2669; B. M. Lake and M. Baroni, Nature 623 (2023) 115-121; A. G. Huth, W. A. de Heer, T. L. Griffiths,
  F. E. Theunissen and J. L. Gallant, Nature 532 (2016) 453-458.
* Open data: A. J. Wills et al., catlearn 1.1; J. de Leeuw, P. Mair and P. Groenen, smacof 2.1-7; J. Silge,
  janeaustenr 1.0.0 (all from CRAN; the files are fetched on first use and never committed).

## Problems and solutions

**1. A prototype is a one-exemplar GCM.** The GCM gives P(A | x) = β_A Σ_{a∈A} η(x, a) / Σ_K β_K Σ_{k∈K} η(x, k),
with η(x, y) = exp(−c d(x, y)). If category A stores a single exemplar at its mean μ_A (and B one at μ_B), the sums
have one term each and P(A | x) = β_A η(x, μ_A) / Σ_K β_K η(x, μ_K): the prototype model. In the 5-4 structure the
prototype of A is (1, 1, 1, 1). Item A1 = 1110 differs from it in one feature and A2 = 1010 in two, so the prototype
model must rank A1 above A2. But A2 is one feature from two other A items (A1 and A3) and two or more from every B
item, while A1 is one feature from two B items (B1 = 1100 and B2 = 0110), so the summed similarity favours A2. People
made fewer errors on A2 (Medin and Schaffer 1978, Experiment 2): the exemplar model's ordering.

**2. Double centring.** Let X be n × k with centred columns (1ᵀX = 0) and B = XXᵀ, so b_ij = x_i · x_j. Then
d_ij² = b_ii + b_jj − 2 b_ij, i.e. D⁽²⁾ = diag(B) 1ᵀ + 1 diag(B)ᵀ − 2B. With J = I − 11ᵀ/n, J1 = 0, so the first two
terms vanish under J · J and −½ J D⁽²⁾ J = J B J = B, since JX = X. B = XXᵀ is positive semi-definite; a negative
eigenvalue of −½ J D⁽²⁾ J therefore shows that no Euclidean configuration, in any number of dimensions, has exactly
these distances. Classical MDS then keeps the positive part; non-metric MDS gives up the distances and keeps their
order.

**3. Shepard's integral.** For s > d the region of size s holds the second stimulus with probability 1 − d/s, so
g(d) = ∫_d^∞ s e^{−s} (1 − d/s) ds = ∫_d^∞ (s − d) e^{−s} ds = e^{−d} ∫_0^∞ u e^{−u} du = e^{−d}. With sizes uniform on
[0, L], g(d) = (1/L) ∫_d^L (1 − d/s) ds = (1/L)[L − d − d ln(L/d)] for d < L and 0 beyond. Its slope, −ln(L/d)/L, is
unbounded at 0, so it falls steeply at first and reaches zero at d = L. Uncertainty spread over regions of every size
is what gives the exponential's steady upward curve; a bounded prior gives a curve that ends.

**4. The contrast model's asymmetry.** S(a, b) − S(b, a) = θ f(A∩B) − α f(A−B) − β f(B−A) − θ f(A∩B) + α f(B−A) +
β f(A−B) = (β − α)[f(A−B) − f(B−A)]. It vanishes when α = β (no focusing on the subject) or when the two objects have
equally many distinctive features. With α > β, S(a, b) > S(b, a) exactly when f(A−B) < f(B−A): the subject with fewer
distinctive features, the less prominent one, is more similar to the referent than the reverse.

**5. Indistinguishable concepts.** Among 1 to 100, the multiples of 10 are 10, 20, …, 100 and the numbers ending in 0
are the same ten numbers. Every example is in both or neither, and the two have the same size, so their likelihoods
are equal for every set of examples: the posterior ratio is the prior ratio forever. Only the prior, or examples from
outside 1 to 100, or a different kind of evidence (being told the rule), can decide. Any learner faces such sets of
hypotheses that its data cannot separate; it is the number game's version of model mimicry (Part 48).

**6. Prominence by dashes.** In `concepts.prominence_asymmetry`, pass the number of dashes of each signal as the
prominence; pairs with equal counts drop out. On Rothkopf's table this leaves 493 pairs: in 266 the signal with fewer
dashes heard first is called "same" more often, in 192 the reverse, 35 ties (sign test p ≈ 0.0006), a mean difference
of 1.8 points. With temporal length it is 336, 182 and 37 (p ≈ 10⁻¹¹, 3.2 points), and with the share of dashes there
is no asymmetry at all (266 against 276). What makes a signal prominent here is how much of it there is to hear, which
length measures best.

**7. ⋆ A study on which the models must disagree.** One answer: use a structure like 5-4, where an item closer to
the prototype is surrounded by the other category's exemplars, and test it before and after adding exemplars of the
other category near it. The exemplar model predicts that accuracy on that item falls as the new exemplars are added;
the prototype model, if the prototypes are unchanged, predicts no change. Another: transfer to new items at equal
distance from the prototype but different distances from the stored exemplars. A good design states, before the
data, which pattern each model predicts with its parameters fitted to the training phase alone, so that one cannot
mimic the other after the fact.

## Open checks

Before the narrated master:

* Rosch's typicality ladder and McCloskey and Glucksberg's borderline items are drawn from summaries of the papers;
  the ladder's order, not its values, is shown.
* Hutchison et al.'s priming effects (about 19 and 6 ms; 26 and 20 against 42 and 60) are from the paper's
  discussion; check them against its tables.
* Fried and Nesse's 1,030 profiles and 1.8% are from the abstract and results; Marjieh et al.'s correlations are
  from the arXiv version (2302.01308v2).
* The English preflight flags the bird table's rotated column labels (*builds nests*, *eats insects*, *swims*):
  their bounding boxes touch, the drawn text does not. Reviewed on the frame and accepted.
