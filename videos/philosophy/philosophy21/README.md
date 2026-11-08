# Philosophy, Built — Part 21: Identity and Persistence

Part 21 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): what it is to be the same
thing, at a time and over time, and what it is to be the same person. Three puzzles (the ship, the teleporter, the
girl and the old woman) and why they matter (responsibility, prudence, advance directives, copies). Identity: numerical
and qualitative, two axioms (reflexivity and Leibniz's law) with symmetry and transitivity derived, the converse
principle (the identity of indiscernibles), the necessity of identity (Barcan, Kripke), and identity in programs and
records (`is` against `==`, run; primary keys; record linkage). Black's spheres and Quine's grades of discernibility,
computed by brute force over automorphisms (Black's spheres and the singlet state are weakly discernible), the
Leibniz–Clarke shift argument, and identical particles (French and Redhead, Saunders, Muller and Seevinck). The statue
and the lump: Gibbard's Lumpl and Goliath, pluralists and monists, modal profiles tabulated across five scenarios, and
the grounding problem. The ship of Theseus, repaired and rebuilt plank by plank over forty days, the closest
continuer, how many ships there were on five views (Chisholm's mereological essentialism among them), and real ships
of Theseus (Ise Jingū, USS Constitution, a code base). Relative identity (Geach, Perry), sortals (Wiggins), criteria of
identity (sets, directions, numbers, events), and apparent failures of Leibniz's law in opaque contexts (Superman).
Evans's one-page proof that identity cannot be vague, model-checked over precisifications (with rigid names, 0 of 9
pairs make identity indeterminate; with shifting names, 486 of 729 do, and the abstraction step fails), Lewis's
diagnosis, and the replies. Endurance, perdurance and stage theory as spacetime worms, the arguments for worms,
Kripke's spinning disc, and persistence and the theory of time. Temporary intrinsics: Lewis's problem, four answers,
and a **Price List**. Locke's memory criterion, Reid's brave officer computed (memory is not transitive; its ancestral
is), Butler's circularity and Shoemaker's quasi-memory, and Williams's two tellings of one case. Parfit: connectedness
fading and continuity holding over a simulated lifetime (half the ten-year-old's memories gone by twenty-four;
year-to-year overlap never below 94%), the teletransporter and the branch-line case, the combined spectrum, what
matters, and experimental philosophy on the moral self. Fission: Wiggins's case, split-brain patients, branching
worms (Lewis), the fission **Price List**, **the Wall's twenty-first brick**, and the only-x-and-y principle.
Animalism (Olson), the thinking-animal problem, the brain, remnant, constitution and narrative views, and Shoemaker's
Brownson. No self: the chariot of the *Milindapañha*, Hume's bundle, Buddhist reductionism, the Indian debate
(Nyāya, Nāgārjuna, Śāntideva), and the self as a model (Dennett, Metzinger, Strawson, Zahavi). Copies: whole brain
emulation, one set of weights run as many instances, a table of what transfers and what is only analogy, the ethics
of copyable minds, software forks, and model versions as ships of Theseus (a weight vector drifting through forty
random updates: similarity to the original falls below one half by the twenty-fourth, while each version stays within
0.97 of the last).

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/persist.py`, tested
in `tests/philosophy/test_persist.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy21.compute       # every computed item (seconds; .cache/philosophy21)
python tools/build.py philosophy21 -q l                # 480p preview
python tools/build.py philosophy21                     # 1080p30 -> renders/philosophy21.mp4
python tools/qa_scene.py philosophy21 Fission          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Butler (1726); three puzzles; the stakes; the plan. | — |
| 1 | `Identity` | Leibniz (1686); Frege (1892); Barcan (1947); Kripke (1971); Fellegi and Sunter (1969). | `is` and `==`, run |
| 2 | `Discern` | Black (1952); Hacking (1975); Quine (1976); Leibniz–Clarke (1716); French and Redhead (1988); Saunders (2006); Muller and Seevinck (2009). | grades of discernibility on five structures |
| 3 | `Coincidence` | Gibbard (1975); Wiggins (1968); Baker (2000); Lewis (1971); Bennett (2004). | modal profiles in five scenarios |
| 4 | `Theseus` | Plutarch; Hobbes (1655); Nozick (1981); Chisholm (1973, 1976). | forty days of planks, two ships |
| 5 | `Relative` | Geach (1967); Perry (1970); Wiggins (1980); Davidson (1969); Quine (1956, 1985). | — |
| 6 | `Evans` | Evans (1978); Lewis (1988); Williamson (1994); Barnes and Williams (2011); van Inwagen (1988). | indeterminate identity over precisifications |
| 7 | `Persistence` | Lewis (1986); Sider (2001); Hawley (2001); Kripke's disc; Broad (1923). | — |
| 8 | `Intrinsics` | Lewis (1986); Johnston (1987); Haslanger (1989); temporary intrinsics as a **Price List**. | the conflict and its exits |
| 9 | `Locke` | Locke (1694); Reid (1785); Butler (1736); Shoemaker (1970); Williams (1970). | memory and its ancestral |
| 10 | `Parfit` | Parfit (1971, 1984); Johnston (1992); Nichols and Bruno (2010); Strohminger and Nichols (2014); Tobia (2015). | connectedness and continuity over a lifetime |
| 11 | `Fission` | Wiggins (1967); Sperry and Gazzaniga; Nagel (1971); Lewis (1976); the fission **Price List**; **the Wall's twenty-first brick**; Noonan. | the branching continuity graph |
| 12 | `Animal` | Olson (1997); Snowdon; McMahan (2002); Johnston (2007); Baker; Schechtman (1996); Shoemaker (1963). | — |
| 13 | `Anatta` | the *Milindapañha*; Hume (1739); Vasubandhu; Nāgārjuna; Śāntideva; Parfit; Siderits (2007); Dennett (1992); Metzinger (2003). | — |
| 14 | `Copies` | Sandberg and Bostrom (2008); model instances; Shulman and Bostrom (2021); forks; model versions as ships of Theseus. | a weight vector drifting through forty updates |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Noonan and Curtis, "Identity" (*Stanford Encyclopedia of Philosophy*, 2022); Wiggins, *Sameness and Substance
Renewed* (2001); Sider, *Four-Dimensionalism* (2001); Hawley, *How Things Persist* (2001); Parfit, *Reasons and
Persons*, Part III (1984); Olson, *The Human Animal* (1997); Baker, *Persons and Bodies* (2000); Perry (ed.),
*Personal Identity* (1975; 2nd ed. 2008); Siderits, *Buddhism as Philosophy* (2007); Metzinger, *Being No One* (2003).

Papers: Locke (1694); Butler (1736); Reid (1785); Barcan (1947); Black (1952); Shoemaker (1963, 1970); Geach (1967);
Wiggins (1967, 1968); Perry (1970); Williams (1970); Kripke (1971); Lewis (1971, 1976, 1988); Nagel (1971); Parfit
(1971); Gibbard (1975); Hacking (1975); Quine (1976); Evans (1978); Johnston (1987, 1992); van Inwagen (1988); French
and Redhead (1988); Dennett (1992); Bennett (2004); Saunders (2006); Muller and Saunders (2008); Muller and Seevinck
(2009); Sandberg and Bostrom (2008); Nichols and Bruno (2010); Barnes and Williams (2011); Strohminger and Nichols
(2014); Tobia (2015); Shulman and Bostrom (2021).
