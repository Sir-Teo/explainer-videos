# Philosophy, Built — Part 37: Is and Ought

Part 37 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*:
metaethics, what moral claims are. Mackie's opening sentence (1977) and four questions (logic, metaphysics, meaning,
knowledge). Hume's paragraph (1739); Prior's tea (1960) and its dilemma; Searle's derivation from promising (1964) and
Hare's reply; ought implies can as a bridge, with Chituc et al. (2016); a deontic logic KD built on serial Kripke
models and checked on every model of up to three worlds (175,616 models), and Schurz's pattern (1997) confirmed on
eight inferences: every valid inference from is-only premises to an ought is a logical truth or has an idle ought —
**the Wall's thirty-seventh brick**. Moore's open question (1903), the naturalistic fallacy, Frankena (1939), Moore's
ideal and organic unities, the paradox of analysis (Langford 1942) and water as H₂O. Realism: non-naturalism
(Shafer-Landau, Enoch, Parfit) and Cornell realism (Boyd, Brink, Sturgeon), Harman's challenge (1977) and moral
explanations; Railton's reforming definition (1986); Blackburn's supervenience challenge (1971); moral knowledge
(intuitionism, seemings, perception, the puzzle of moral testimony); moral twin earth (Horgan and Timmons 1991). Error
theory: Mackie's relativity and queerness, the companions in guilt (Cuneo 2007), fictionalism, abolitionism and
conservationism (Joyce, Garner, Olson), and a **Price List** for Mackie's triad with the PhilPapers 2020 shares (62%
realism, 26% anti-realism). Expressivism: Ayer (1936), Stevenson's disagreement in attitude (1944), Smith's moral
problem (1994) as a computed triad, Blackburn's quasi-realism and creeping minimalism (Dreier 2004), hybrid views
(Copp; Ridge). The Frege–Geach problem (Geach 1965), Blackburn's higher-order attitudes and Hale's reply, **Gibbard's
norm-world pairs built** (eight pairs, two left by the premises, all in the conclusion), Dorr's wishful thinking (2002),
and the negation problem (Unwin 1999; Schroeder 2008). Relativism (Herodotus; Harman 1975; Wong 2006), the
disagreement problem and MacFarlane's assessment-sensitivity, disagreement as evidence (Part 12), constructivism (Rawls
1980; Korsgaard 1996; Street 2010), and Dworkin's challenge (1996). Street's Darwinian dilemma (2006), run as an analogy
(evolved approval correlates 0.83 with fitness, −0.02 with an independent truth, 0.68 with a truth tied to fitness),
third-factor replies, Joyce (2006), and selective debunking (Singer; de Lazari-Radek and Singer; Kahane). Moral
psychology: Haidt's dumbfounding and social intuitionism (2001), folk objectivism (Goodwin and Darley 2008), moral
foundations (Graham, Haidt and Nosek 2009), Greene's dual process and the reanalysis debate (McGuire et al. 2009;
Berker 2009), Mikhail's moral grammar. Mencius (性善) against Gaozi, Xunzi (性恶), Mozi's inclusive care, and two
theories of moral learning. Reflective equilibrium (Goodman 1955; Rawls 1971; Daniels 1979) built as weighted MaxSAT
on six trolley commitments: double effect and the three judgments survive (16 of 22); after Greene's reweighting, welfare
and the switch (10); Singer's critique (1974); moral progress on each view.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/metaethics.py` (with
`prop` for the Price Lists and the satisfiability checks), tested in `tests/philosophy/test_metaethics.py` and cached
by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy37.compute       # every computed item (seconds; .cache/philosophy37)
python tools/build.py philosophy37 -q l                # 480p preview
python tools/build.py philosophy37                     # 1080p30 -> renders/philosophy37.mp4
python tools/qa_scene.py philosophy37 Geach            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Mackie (1977); four questions; the plan. | — |
| 1 | `Hume` | Hume (1739); Prior (1960); Searle (1964); Hare; Kant; Chituc et al. (2016); Schurz (1997); **the Wall's thirty-seventh brick**. | KD on every model of up to three worlds; eight inferences |
| 2 | `Moore` | Moore (1903); Frankena (1939); Langford (1942); Putnam; Kripke. | — |
| 3 | `Realism` | Shafer-Landau; Enoch; Parfit; Boyd; Brink; Sturgeon; Harman (1977); Railton (1986); Blackburn (1971); Huemer; Hills; Horgan and Timmons (1991). | the PhilPapers share |
| 4 | `Error` | Mackie (1977); Cuneo (2007); Streumer; Joyce (2001); Garner; Olson (2014); **the Price List**. | Mackie's triad's minimal conflict |
| 5 | `Express` | Ayer (1936); Stevenson (1944); Smith (1994); Brink; Nagel; McDowell; Blackburn; Dreier (2004); Copp; Ridge. | Smith's triad |
| 6 | `Geach` | Geach (1965); Blackburn (1984); Hale (1986); Gibbard (1990, 2003); Dorr (2002); Unwin (1999); Schroeder (2008). | norm-world pairs eliminated |
| 7 | `Construct` | Herodotus; Harman (1975); Wong (2006); MacFarlane (2014); Rawls (1980); Korsgaard (1996); Street (2010); Dworkin (1996). | — |
| 8 | `Debunk` | Street (2006); Enoch; Wielenberg; Copp; Joyce (2006); Singer (2005); de Lazari-Radek and Singer (2012); Kahane (2011). | the dilemma as an analogy |
| 9 | `Psych` | Haidt (2001); Goodwin and Darley (2008); Graham, Haidt and Nosek (2009); Greene (2001, 2013); McGuire et al. (2009); Berker (2009); Mikhail (2011). | — |
| 10 | `Mencius` | Mencius; Gaozi; Xunzi; Mozi; Ivanhoe; Van Norden. | — |
| 11 | `Equilibrium` | Goodman (1955); Rawls (1971); Daniels (1979); Kelly and McGrath (2010); Singer (1974). | weighted MaxSAT on six commitments, twice |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The deontic models are serial (KD); "idle" means that replacing the conclusion's outermost O- or P-subformula by a
fresh atom leaves the inference valid, which by uniform substitution suffices for replacement by any formula. The
debunking toy is labelled an analogy: two hundred kinds of act, replicator dynamics on approval for 400 generations;
it models the structure of Street's argument, not human history. The equilibrium's links are hard constraints and
its weights are invented.

## Problems and solutions

1. Show that p ⊢ p ∨ Oq is valid in KD, and that Oq can be replaced by any formula.

   *Solution.* In KD, as in any normal modal logic, the propositional tautology $p \to (p \lor X)$ holds for every formula $X$, and modus ponens gives $p \vdash p \lor X$. With $X = Oq$, $p \vdash p \lor Oq$: from a purely descriptive premise, a conclusion containing "ought". That is Prior's first counterexample to Hume's law. Since nothing about $Oq$ was used, any formula, normative or not, can take its place, which is why Schurz's theorem counts such conclusions as only vacuously normative: the "ought" part can be replaced salva validitate.

2. Find a countermodel to Op ⊢ p with two worlds.

   *Solution.* Two worlds: $w_0$, the actual one, where $p$ is false, and $w_1$, where $p$ is true. Let $w_1$ be the only world ideal relative to $w_0$ ($w_0 R w_1$), and let $w_1$ see itself, so the frame is serial. At $w_0$, $Op$ holds (every ideal world makes $p$ true) and $p$ fails. So $Op \nvdash p$: what ought to be need not be, which is the point of deontic logic dropping the T axiom.

3. Show that Op → Pp is valid in KD but not in K, where a world may have no ideal world.

   *Solution.* $Pp$ is $\lnot O\lnot p$: some ideal world makes $p$ true. In KD every world has at least one ideal world (seriality). If $Op$ holds at $w$, $p$ is true at all of $w$'s ideal worlds, and there is at least one, so $Pp$ holds. In K a world may have no ideal worlds. There $Op$ is vacuously true (every ideal world, of which there are none, makes $p$ true) and $Pp$ is false. So $Op \to Pp$, the D axiom, is valid in KD and not in K: in K, a dead-end world makes everything obligatory and nothing permitted.

4. In the norm-world semantics, show that "lying is wrong" and "lying is not wrong" leave no pair in common.

   *Solution.* In Gibbard's semantics a judgment is the set of norm-world pairs it leaves open. "Lying is wrong" leaves open exactly the pairs whose norms forbid lying. "Lying is not wrong" (the negation of the whole judgment) leaves open exactly the pairs whose norms permit lying. Each pair's norm either forbids or permits lying, so every pair is in exactly one of the two sets: they are disjoint, and accepting both leaves no pair, no plan that can be carried out. That is the inconsistency the simple attitude theory could not express, and it falls out of the semantics as ordinary set complementation.

5. Give weights for which reflective equilibrium keeps D, F and H.

   *Solution.* In the film's problem the links make $D$ (never kill an innocent) conflict with switching ($S$) and with double effect ($DDE$), while agreeing with the footbridge ($F$) and the surgeon ($H$) judgments. Keeping $\{D, F, H\}$ beats the default equilibrium $\{DDE, S, F, H\}$ when $w_D + w_F + w_H > w_{DDE} + w_S + w_F + w_H$, that is $w_D > w_{DDE} + w_S = 6$. With $D$ raised from 3 to 7 and everything else as in the film, the Reasoner's equilibrium is $\{D, F, H\}$, weight 17 against 16; at $w_D = 6$ the two tie. Confidence in the absolute principle has to outweigh the switch judgment and double effect together.

6. State Mackie's argument from queerness as a valid argument, and say which premise you would deny.

   *Solution.* (1) If there are objective values, they are intrinsically action-guiding: knowing one would give anyone a reason to act, whatever they want. (2) Nothing else in the world is intrinsically action-guiding in that way. (3) If there were such entities, knowing them would require a special faculty of moral intuition, unlike any other way of knowing. (4) We have no such faculty, and no entity is metaphysically that strange. (5) So there are no objective values. As stated the argument is valid. The premise most worth denying is the implicit one that what is unlike anything else is therefore not real: the companions-in-guilt reply says epistemic norms ("believe what your evidence supports") are categorical and action-guiding in the same way, so premise (2) is false and queerness proves too much.

