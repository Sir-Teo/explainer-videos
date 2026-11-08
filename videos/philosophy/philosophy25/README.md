# Philosophy, Built — Part 25: Space and Time

Part 25 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of space and
time, with every geometry and spacetime built. Newton's absolute space and his bucket, its paraboloid computed (a
15 cm bucket at about one turn a second climbs some 4 cm), and Mach's reply. The Leibniz–Clarke correspondence: the
static and kinematic shifts, checked on a universe of six moving bodies (every inter-body distance unchanged by a
shift, a rotation, a boost and a rotation in time, though only the last would curve the water). Kant's incongruent
counterparts: orientation as signed area, two hundred rigid motions that never change its sign, and a frame carried
round a Möbius strip that comes back reversed. Non-Euclidean geometry built in the Poincaré disk: geodesics, many
parallels, hyperbolic triangles whose angle sums fall from 177° to 23.5° while their areas (the defect) approach π;
Gauss's survey triangle and its 15 arcseconds of spherical excess. Poincaré's disk world, whose shrinking rulers
measure a hyperbolic plane, and conventionalism (Poincaré, Reichenbach, Einstein, Putnam). Spacetime structures from
Aristotle to Leibniz, and Earman's symmetry principles: Galilean spacetime has just enough. Special relativity:
the Minkowski diagram with tilting slices of simultaneity, Einstein's lightning strikes in four frames, the invariant
interval. Reichenbach's ε and Malament's theorem. McTaggart's A- and B-series and his regress; presentism, the growing
block, the moving spotlight and eternalism; the Rietdijk–Putnam argument with its boost computed, and the
presentist's replies. General relativity and the hole argument (Einstein 1913; Earman and Norton 1987), the hole
diffeomorphism animated, as a **Price List** and **the Wall's twenty-fifth brick**. Barbour and Bertotti's best
matching, built with the Kabsch algorithm. Gödel's rotating universe, Lewis's grandfather paradox, and Deutsch's
closed timelike curves, whose fixed points are computed for the grandfather and knowledge paradoxes. And, labelled
as speculative, spacetime from entanglement (Maldacena; Ryu and Takayanagi; Van Raamsdonk; ER = EPR), and causal sets
(Bombelli, Lee, Meyer and Sorkin): four hundred events sprinkled into flat spacetime, the coordinates forgotten, and
the dimension (2, 3, 4) recovered from the causal order alone by the Myrheim–Meyer estimator.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/spacetime.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_spacetime.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy25.compute       # every computed item (seconds; .cache/philosophy25)
python tools/build.py philosophy25 -q l                # 480p preview
python tools/build.py philosophy25                     # 1080p30 -> renders/philosophy25.mp4
python tools/qa_scene.py philosophy25 Hole             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Augustine; four questions; the plan. | — |
| 1 | `Bucket` | Newton (1687); Mach (1883); Maudlin. | the bucket's paraboloid |
| 2 | `Leibniz` | Leibniz and Clarke (1715–16); Galileo's ship. | shifted universes, every distance checked |
| 3 | `Hands` | Kant (1768, 1783); Möbius; Wu (1957). | signed areas; Möbius transport |
| 4 | `Geometry` | Euclid; Lobachevsky (1829); Bolyai (1832); Gauss; Poincaré; Riemann (1854). | hyperbolic triangles; Gauss's excess |
| 5 | `Convention` | Poincaré (1902); Reichenbach (1928); Einstein; Putnam; Duhem and Quine. | the disk world's measurements |
| 6 | `Structures` | Aristotle; Newton; Galileo; Leibniz; Earman (1989); Maudlin (2012). | — |
| 7 | `Relativity` | Einstein (1905); Minkowski (1908). | simultaneity in four frames; the interval |
| 8 | `Simultaneity` | Reichenbach (1928); Malament (1977); Sarkar and Stachel (1999). | Reichenbach's ε |
| 9 | `McTaggart` | McTaggart (1908); Prior; Russell, Mellor, Smart. | — |
| 10 | `Theories` | Rietdijk (1966); Putnam (1967); Stein (1968). | the Rietdijk–Putnam boost |
| 11 | `Hole` | Einstein (1913, 1915); Earman and Norton (1987); **the Wall's twenty-fifth brick**; the hole as a **Price List**. | the hole diffeomorphism |
| 12 | `Relational` | Barbour and Bertotti (1982); Barbour (1999); Kabsch (1976). | best matching |
| 13 | `TimeTravel` | Gödel (1949); Lewis (1976); Deutsch (1991); Novikov; Hawking (1992). | Deutsch's fixed points |
| 14 | `Emergence` | Maldacena (1997); Ryu and Takayanagi (2006); Van Raamsdonk (2010); Maldacena and Susskind (2013); Hawking, King and McCarthy (1976); Malament (1977); Bombelli, Lee, Meyer and Sorkin (1987); Huggett and Wüthrich. | a causal set's links; the dimension from order |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Earman, *World Enough and Space-Time* (1989); Huggett (ed.), *Space from Zeno to Einstein* (1999); Barbour,
*The End of Time* (1999); Dainton, *Time and Space* (2nd ed., 2010); Maudlin, *Philosophy of Physics: Space and Time*
(2012); Arntzenius, *Space, Time, and Stuff* (2012); Norton, "The Hole Argument" (*Stanford Encyclopedia of
Philosophy*).

Papers and primary texts: Newton (1687); Leibniz and Clarke (1715–16); Kant (1768); Lobachevsky (1829); Bolyai
(1832); Riemann (1854); Mach (1883); Poincaré (1902); Einstein (1905, 1915); Minkowski (1908); McTaggart (1908);
Reichenbach (1928); Gödel (1949); Rietdijk (1966); Putnam (1967); Stein (1968); Hawking, King and McCarthy (1976);
Lewis (1976); Malament (1977); Barbour and Bertotti (1982); Bombelli, Lee, Meyer and Sorkin (1987); Earman and Norton
(1987); Meyer (1988); Deutsch (1991); Hawking (1992); Maldacena (1997); Sarkar and Stachel
(1999); Ryu and Takayanagi (2006); Van Raamsdonk (2010); Maldacena and Susskind (2013); Huggett and Wüthrich (2013).
