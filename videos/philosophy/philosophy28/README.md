# Philosophy, Built — Part 28: Meaning in Use

Part 28 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the second part of Act VI,
*Mind and Meaning*: meaning as use, from Wittgenstein to computed pragmatics, with a Rational Speech Acts model and a
signalling game built. The *Tractatus*: pictures and logical space, truth tables, and all 16 truth functions of two
propositions generated from Wittgenstein's single operation N (by depth: 2, 3, 5 and 6 new functions), and the ladder
thrown away. The *Investigations*: the builders of §2, the multiplicity of language games (§23), family resemblance
computed on six games (no feature shared by all six, yet 10 of the 15 pairs share something and the network is
connected), and meaning as use (§43). Kripke's plus and quus: a record of 1000 sums that both rules fit, the 143
rival 'quus_b' rules for bounds 57–199, the sceptic's four candidate facts, the sceptical solution, Kripkenstein, and
**the Wall's twenty-eighth brick**. The private language argument: the diary of §258 and the beetle in the box of §293.
Quine's gavagai (rabbit, undetached rabbit part and rabbit stage assented to in the same 20 of 40 scenes), the
indeterminacy of translation, and proxy functions computed: a permutation of the domain that keeps the truth value of
all 300 random first-order sentences while every name and predicate now applies to something else; Chomsky's and
Lewis's replies. Davidson's radical interpretation and charity computed: three alien sentences heard 60 times by
speakers who err one time in ten, all six translation schemes tried, and charity picking the true one (50 of 60 right,
not 60), and charity against the speakers' error rate (200 trials at each rate: the truth every time up to 3 errors in 10, 182 of 200 at a half, chance, 34 of 200, at two thirds); the very idea of a conceptual scheme, triangulation and Grandy's humanity. Austin's performatives, felicity
conditions and the three acts; Searle's taxonomy and directions of fit; indirect speech acts. Grice's cooperative
principle and maxims, implicature (the garage, the reference letter), the tests for it, flouting (tautology, irony,
metaphor, 'Home Sweet Home'), and Horn's, Levinson's and Sperber and Wilson's successors. Horn scales and the
Gricean derivation of 'some, not all'; Noveck's children and Bott and Noveck's reaction times. The Rational Speech Acts
model (Frank and Goodman) built: the literal listener, the speaker and the pragmatic listener on a three-object
reference game (hearing 'blue', 0.6 for the blue square against 0.4), 'some' over four states of three cookies (the
pragmatic listener gives 'all' about 6 in 1000), how the effect grows with α, and the listener at recursion depths
0 to 6 (0.5, 0.6, 0.64, ... 0.66; Franke and Degen on how deep people go); hyperbole, politeness, and where the
model reaches. Lewis signalling games learned by Roth–Erev reinforcement (Skyrms): of 200 runs of 6000 rounds, 196 end
above 90% success and 172 above 99%; with three states 169 succeed and 26 stick near two thirds in partial pooling;
the information the learned signals carry (0.98 of 1 bit; 1.52 of 1.58; the pooled runs 0.90); Lewis's conventions
and Skyrms's informational content. Distributional semantics built: Saussure, Harris and Firth, a
small corpus turned into positive-PMI word vectors and a truncated SVD, nearest neighbours (cat → dog; king → queen)
the space of words, and analogies as directions (king − prince + princess → queen; the city–country analogies fail on so small a corpus). The octopus (Bender and Koller), Harnad's grounding problem, conceptual role and the replies,
Brandom's deontic scorekeeping built (commitments and entitlements over a six-move conversation), a **Price List** of four inconsistent
claims; probing the Reasoner's own vectors (kinds: 15 of 17 held-out words;
fiction against fact: 0 of 6, because the corpus does not mark it), and Othello-GPT. Pragmatics in machines:
implicature benchmarks, a pragmatic captioner (the green square called 'green' two to one), and Grice's maxims as
requirements for assistants.

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/pragmatics.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_pragmatics.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy28.compute       # every computed item (about a minute; .cache/philosophy28)
python tools/build.py philosophy28 -q l                # 480p preview
python tools/build.py philosophy28                     # 1080p30 -> renders/philosophy28.mp4
python tools/qa_scene.py philosophy28 RSA              # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | four questions about use; the plan. | — |
| 1 | `Tractatus` | Wittgenstein (1921); Post (1921). | logical space; all 16 truth functions from N |
| 2 | `Games` | Wittgenstein (1953), §§2, 23, 43, 66. | family resemblance on six games |
| 3 | `Rules` | Kripke (1982); **the Wall's twenty-eighth brick**. | plus and quus on 1000 sums; 143 rivals |
| 4 | `Private` | Wittgenstein (1953), §§258, 293; Ayer (1954). | — |
| 5 | `Quine` | Quine (1960, 1968); Chomsky (1969); Lewis (1983). | gavagai in 40 scenes; a proxy function on 300 sentences |
| 6 | `Charity` | Davidson (1973, 1974); Grandy (1973). | six translation schemes on 60 observations; the error-rate sweep |
| 7 | `Acts` | Austin (1955/1962); Searle (1969, 1975). | — |
| 8 | `Grice` | Grice (1957, 1967/1975); Horn (1984); Levinson (2000); Sperber and Wilson (1986). | — |
| 9 | `Scalar` | Horn (1972); Noveck (2001); Bott and Noveck (2004). | — |
| 10 | `RSA` | Frank and Goodman (2012); Goodman and Frank (2016); Kao et al. (2014); Franke and Degen (2016). | a reference game; 'some' over four states; the effect of α; recursion depth |
| 11 | `Signals` | Lewis (1969); Skyrms (2010); Roth and Erev (1995). | 200 runs with two states and with three; bits carried |
| 12 | `Vectors` | Saussure (1916); Harris (1954); Firth (1957); Mikolov et al. (2013). | PPMI vectors and SVD on a small corpus; three analogies |
| 13 | `Octopus` | Harnad (1990); Bender and Koller (2020); Piantadosi and Hill (2022); Mollo and Millière (2023); Brandom (1994); **the Price List**. | a scorekeeper's six moves; the four claims' minimal conflicts |
| 14 | `Probe` | Li et al. (2023). | two probes: kinds and fiction |
| 15 | `Machines` | Ruis et al. (2023); Hu et al. (2023); Andreas and Klein (2016); Cohn-Gordon et al. (2018). | a literal and a pragmatic captioner |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Wittgenstein, *Tractatus Logico-Philosophicus* (1921) and *Philosophical Investigations* (1953); Kripke,
*Wittgenstein on Rules and Private Language* (1982); Quine, *Word and Object* (1960); Davidson, *Inquiries into Truth
and Interpretation* (1984); Grice, *Studies in the Way of Words* (1989); Lewis, *Convention* (1969); Skyrms, *Signals*
(2010); Levinson, *Pragmatics* (1983); Lycan, *Philosophy of Language* (3rd ed., 2019).

Papers and primary texts: Saussure (1916); Post (1921); Ayer (1954); Harris (1954); Austin (1955/1962); Firth (1957);
Grice (1957, 1975); Quine (1968); Horn (1984); Levinson (2000); Chomsky (1969); Searle (1969, 1975); Horn (1972); Davidson (1973, 1974); Grandy
(1973); Lewis (1983); Harnad (1990); Brandom (1994); Roth and Erev (1995); Noveck (2001); Bott and Noveck (2004); Frank
and Goodman (2012); Mikolov et al. (2013); Kao et al. (2014); Sperber and Wilson (1986); Andreas and Klein (2016); Franke and Degen (2016); Goodman and Frank (2016);
Cohn-Gordon et al. (2018); Bender and Koller (2020); Piantadosi and Hill (2022); Mollo and Millière (2023); Li et al.
(2023); Ruis et al. (2023); Hu et al. (2023).
