# Philosophy, Built — Part 31: Consciousness

Part 31 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the fifth part of Act VI,
*Mind and Meaning*: what it is like, why it seems to resist physical explanation, and the scientific theories that try
anyway, with a workspace that ignites, an observer that loses its confidence, a simplified Φ computed by cutting, and
an agent that minimizes expected free energy. Nagel's bat (1974) and the view from nowhere; Block's access and
phenomenal consciousness (1995). Chalmers's easy problems and the hard problem (1995), **the Wall's thirty-first
brick**, and his map of responses, types A to F (2003). Jackson's Mary (1982) as an epistemic model (three
possibilities agree on every physical truth; the tomato leaves one), and the ability, acquaintance and
phenomenal-concept replies. Zombies (Kirk 1974; Chalmers 1996): two-dimensional matrices computed for 'water is H2O'
(necessary, not a priori: the diagonal and the actual row differ) and 'pain is C-fibre firing' (the two coincide, so the
zombie scenario's falsity carries over), the argument in modal logic (□(P → Q) ∧ ◇(P ∧ ¬Q) has no model; the weaker
P → Q has a two-world one), and the zombie argument as a **Price List** (type-A and type-B physicalism, Russellian
monism, property dualism). Levine's explanatory gap (1983), the phenomenal concept strategy (Loar, Papineau) and
Chalmers's master argument (2007). Illusionism (Dennett 1988, 1991; Frankish 2016), the meta-problem (Chalmers 2018) and
a self-model built (4096 shades told apart, 12 bits; eleven basic colour words, 3.46 bits; 933 278 of 8 386 560
discriminable pairs share a word: an analogy), and Graziano's attention schema theory (2013). Russellian monism, panpsychism and the combination problem (James 1890).
The global workspace (Baars 1988; Dehaene, Kerszberg and Changeux 1998): one recurrent equation that ignites, a masking
curve over 200 trials per delay (0 seen up to 30 ms, 24 at 40, 81 at 50, 141 at 60, 200 by 100), and all-or-none
activity at the threshold delay (136 low, 64 high, none between). Higher-order theories (Rosenthal; Armstrong; Lau),
blindsight, and an observer simulated over 20 000 trials (77% correct; type-2 AUROC 0.705 with a good monitor, 0.498 in
'blindsight'), with the three type-2 ROC curves drawn. Integrated information (Tononi 2004; IIT 4.0, 2023): a simplified Φ in the style of IIT 2.0, labelled as
such, computed by cutting the OR–AND–XOR loop (cuts lose 1, 2.585 and 2 bits; Φ = 1), in each of its eight states
(two have no past; one has Φ = 1.585), and on four systems (separate pairs and a feedforward chain 0; loops 1).
Aaronson's objection (2014): a 2-bit adder scores 0, a ring of ten XORs 2, a 2×5 torus 6, random XOR expanders 4.17 on
average; the unfolding argument (Doerig et al. 2019): the loop unrolled for three steps matches it from all 8 starts,
with Φ = 0; the 2023 open letter. Predictive processing and the free-energy principle (Helmholtz; Friston 2010; Clark;
Hohwy; Seth 2021): F for three beliefs (0.693, 1.966, 3.891 nats) and a T-maze agent scored by expected free energy
(looking at the cue, then following it: G = −3.43, chosen 86% of the time). The Koch–Chalmers bet and the Cogitate
adversarial collaboration (Nature, 2025). Animal consciousness: the Cambridge (2012) and New York (2024) declarations,
Birch's eight criteria (2021) and the UK Sentience Act (2022). Machines: Butlin, Long et al.'s fourteen indicator
properties (2023), applied to the Reasoner's own toys (two each, six in all), the gaming problem for self-reports, and
Long, Sebo et al. (2024) on AI welfare.

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/consciousness.py`
(with `prop` for the Price List and `modal` for the modal check), tested in `tests/philosophy/test_consciousness.py`
and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy31.compute       # every computed item (a minute; .cache/philosophy31)
python tools/build.py philosophy31 -q l                # 480p preview
python tools/build.py philosophy31                     # 1080p30 -> renders/philosophy31.mp4
python tools/qa_scene.py philosophy31 Workspace        # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Nagel (1974); four questions; the plan. | — |
| 1 | `Bat` | Nagel (1974); Block (1995). | — |
| 2 | `Hard` | Chalmers (1995, 2003); **the Wall's thirty-first brick**. | — |
| 3 | `Mary` | Jackson (1982, 1998); Lewis (1988); Nemirow (1990); Conee (1994); Loar (1990). | what Mary can rule out |
| 4 | `Zombies` | Kirk (1974); Chalmers (1996); Kripke; **the Price List**. | two 2D matrices; a modal check; the argument's minimal conflicts |
| 5 | `Gap` | Levine (1983); Loar (1990); Papineau (2002); Chalmers (2007). | — |
| 6 | `Illusion` | Dennett (1988, 1991); Frankish (2016); Chalmers (2018); Berlin and Kay (1969); Graziano (2013). | a self-model's capacity |
| 7 | `Panpsychism` | Russell (1927); Eddington (1928); Strawson (2006); Goff (2017); James (1890). | — |
| 8 | `Workspace` | Baars (1988); Dehaene, Kerszberg and Changeux (1998); Del Cul et al. (2007). | ignition; a masking curve; bimodality |
| 9 | `Higher` | Rosenthal (1986); Weiskrantz (1986); Lau and Rosenthal (2011). | performance and confidence, 20 000 trials; type-2 ROC curves |
| 10 | `IIT` | Tononi (2004); Balduzzi and Tononi (2008); Albantakis et al. (2023). | cuts; Φ in eight states; four systems |
| 11 | `Aaronson` | Aaronson (2014); Tononi (2014); Doerig et al. (2019); the 2023 letter. | an adder against XOR structures; unfolding |
| 12 | `Predict` | Helmholtz (1867); Friston (2010); Friston et al. (2015); Clark; Hohwy (2013); Seth (2021). | free energy of three beliefs; a T-maze agent |
| 13 | `Cogitate` | Koch and Chalmers (1998); Melloni et al. (2021, 2023); Cogitate (2025). | — |
| 14 | `Animals` | Cambridge (2012); New York (2024); Birch et al. (2021); Birch (2024). | — |
| 15 | `Machines` | Butlin, Long et al. (2023); Chalmers (2023); Long, Sebo et al. (2024). | fourteen indicators, applied to three toys |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Chalmers, *The Conscious Mind* (1996) and *The Character of Consciousness* (2010); Dennett, *Consciousness
Explained* (1991); Seth, *Being You* (2021); Dehaene, *Consciousness and the Brain* (2014); Albantakis et al., 'Integrated
information theory (IIT) 4.0' (2023); Butlin, Long et al., 'Consciousness in Artificial Intelligence' (2023); Frankish,
'Illusionism as a Theory of Consciousness' (2016); Birch, *The Edge of Sentience* (2024).

Primary texts and papers: Helmholtz (1867); James (1890); Russell (1927); Eddington (1928); Berlin and Kay (1969); Nagel
(1974); Kirk (1974); Jackson (1982, 1998); Levine (1983); Rosenthal (1986); Weiskrantz (1986); Baars (1988); Dennett
(1988, 1991); Lewis (1988); Loar (1990); Nemirow (1990); Conee (1994); Block (1995, 2011); Chalmers (1995, 2003, 2007,
2018, 2023); Dehaene, Kerszberg and Changeux (1998); Papineau (2002); Tononi (2004, 2014); Strawson (2006); Del Cul,
Baillet and Dehaene (2007); Balduzzi and Tononi (2008); Friston (2010); Lau and Rosenthal (2011); the Cambridge
Declaration (2012); Clark (2013); Graziano (2013); Hohwy (2013); Aaronson (2014); Friston et al. (2015); Goff (2017); Doerig, Schurger,
Hess and Herzog (2019); Birch et al. (2021); Melloni et al. (2021, 2023); Fleming et al. (2023); the New York
Declaration (2024); Long, Sebo et al. (2024); Cogitate Consortium (2025).
