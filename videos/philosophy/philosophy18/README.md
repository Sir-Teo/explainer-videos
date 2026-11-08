# Philosophy, Built — Part 18: Theories and Reality

Part 18 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): explanation, theory change and
scientific realism. Is the electron real? (Thomson's beam; Putnam's no-miracles sentence.) The Vienna Circle and the
verification principle, falsifiability's mirror-image trouble, Ayer's 1946 criterion and Church's one-paragraph
trivialization (each entailment checked by truth table), Neurath's boat, and what survived; Hempel and Oppenheim's
deductive-nomological model, Bromberger's flagpole (computed both ways), the birth-control pills and hexed salt
against Salmon's statistical relevance, Scriven's paresis, and what makes a law (gold and uranium spheres; best
systems; Armstrong); Newton's moon test (one law, apple and Moon, agreeing within 1%), Friedman and Kitcher's
unification, Strevens, mechanisms (Machamer, Darden and Craver), and Salmon's causal processes against the faster-than-
light spot; Kuhn's cycle, the Copernican revolution computed (Ptolemy's epicycle and Copernicus's orbits give Mars the
same sky, retrograde loops and all), a toy of revolution as a threshold cascade (an analogy: 42% convert in one year),
incommensurability and the Necker cube, and Kuhn's five values; Lakatos's research programmes with Neptune and Vulcan,
Feyerabend and Laudan; underdetermination with two Newtonian worlds (at rest and moving: every relative quantity the
same), the Duhem problem at OPERA (faster-than-light neutrinos and a loose cable, as a Price List), and Quine's web;
the no-miracles argument, its base-rate fallacy (Magnus and Callender, computed), and retail arguments (the Arago
spot, Perrin's thirteen methods, Hacking's spray); Laudan's list as a timeline, the realism trilemma (Price List) and
the Wall's eighteenth brick; structural realism with Fresnel's equations (Brewster's angle, 56.3°) surviving into
Maxwell's theory, Newman's objection, and ontic structural realism; constructive empiricism, Maxwell's continuum,
Hacking's entity realism, and the best of a bad lot; Nagel's reduction with temperature recovered from 100,000
simulated molecules, multiple realizability, and Putnam's peg; emergence and universality with the 2D Ising model
sampled by Swendsen–Wang, Onsager's exact magnetization, Kadanoff block spins flowing to order, disorder or the fixed
point, and Batterman's argument; idealization (how false the small-angle pendulum is), Weisberg's three kinds, and
simulation; demarcation (Popper, Kuhn, Lakatos, Laudan's obituary, the cluster view) and string theory's non-empirical
confirmation; inductive risk (Rudner) as a decision whose threshold moves with the costs of error, Jeffrey and
Douglas, and Longino's social objectivity; and AI scientists (a miniature BACON rediscovers Kepler's third law;
AlphaFold, FunSearch, AlphaEvolve) and explanation from black boxes.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/science.py`, tested in
`tests/philosophy/test_science.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy18.compute       # every computed item (under a minute; .cache/philosophy18)
python tools/build.py philosophy18 -q l                # 480p preview
python tools/build.py philosophy18                     # 1080p30 -> renders/philosophy18.mp4
python tools/qa_scene.py philosophy18 Emergence        # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Thomson (1897); Putnam (1975); realism against anti-realism; the plan. | — |
| 1 | `Vienna` | the Vienna Circle (1929); Ayer (1936, 1946); Church (1949); Neurath (1932); Carnap, Quine, Hempel. | Church's four entailments |
| 2 | `Laws` | Hempel and Oppenheim (1948); Bromberger's flagpole; Salmon (1971); Scriven (1959); laws (Lewis; Armstrong). | the shadow from the height, and the height from the shadow |
| 3 | `Unify` | Newton's moon test; Friedman (1974); Kitcher (1981); Strevens (2008); Machamer, Darden and Craver (2000); Salmon (1984). | g/60² against the Moon's acceleration |
| 4 | `Kuhn` | Kuhn (1957, 1962, 1977); Granovetter (1978); Hanson (1958); Okasha (2011). | Mars seen from Earth in both systems; the threshold cascade |
| 5 | `Programmes` | Lakatos (1970); Le Verrier, Neptune and Vulcan; Feyerabend (1975); Laudan (1977). | — |
| 6 | `Under` | van Fraassen's Newtonian worlds; Duhem (1906); OPERA (2011–12) as a **Price List**; Quine (1951); Laudan and Leplin (1991); Stanford (2006). | two orbits, at rest and moving; the Duhem conflict and its exits |
| 7 | `Miracles` | Putnam (1975); Magnus and Callender (2004); Arago; Perrin (1913); Hacking (1983). | P(true \| successful) against the base rate |
| 8 | `Meta` | Laudan (1981); Poincaré (1902); the realism trilemma (**Price List**); Kitcher, Psillos, Fahrbach; **the Wall's eighteenth brick**. | Laudan's list as a timeline |
| 9 | `Structure` | Fresnel (1823) and Maxwell; Worrall (1989); Poincaré; Newman (1928); Ladyman (1998); Ladyman and Ross (2007). | reflectances and Brewster's angle |
| 10 | `Empiricism` | van Fraassen (1980, 1989); Maxwell (1962); Churchland (1985); Hacking (1983); Lipton (2004). | — |
| 11 | `Reduction` | Nagel (1961); Schaffner (1967); Putnam (1967, 1975); Fodor (1974). | temperature from 100,000 molecules |
| 12 | `Emergence` | the Ising model; Onsager (1944); Yang (1952); Kadanoff (1966); Wilson; universality; Batterman (2002); Butterfield (2011). | three lattices; |m| against Onsager; block-spin flows; exponents |
| 13 | `Models` | idealization; Weisberg (2013); Batterman and Rice (2014); Cartwright (1983); Box (1976); Parker, Morrison, Winsberg. | the exact pendulum period against the idealized one |
| 14 | `Demarcation` | Popper (1934); Kuhn; Lakatos; Laudan (1983); Pigliucci and Boudry (2013); Dawid (2013); Ellis and Silk (2014). | — |
| 15 | `Values` | Rudner (1953); Jeffrey (1956); Douglas (2009); Merton (1942); McMullin (1982); Longino (1990). | the best threshold under three costs of error |
| 16 | `Machines` | BACON (Langley 1978); AlphaFold; FunSearch; AlphaEvolve; Reichenbach (1938); Humphreys; de Regt; Sullivan. | 48 power products of the planets' data |
| 17 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Godfrey-Smith, *Theory and Reality* (2003; 2nd ed. 2021); Salmon, *Four Decades of Scientific Explanation*
(1989); Kuhn, *The Structure of Scientific Revolutions* (1962) and *The Copernican Revolution* (1957); van Fraassen,
*The Scientific Image* (1980) and *Laws and Symmetry* (1989); Psillos, *Scientific Realism: How Science Tracks Truth*
(1999); Batterman, *The Devil in the Details* (2002); Douglas, *Science, Policy, and the Value-Free Ideal* (2009);
Weisberg, *Simulation and Similarity* (2013); Hacking, *Representing and Intervening* (1983); Ladyman and Ross,
*Every Thing Must Go* (2007); Longino, *Science as Social Knowledge* (1990); Dawid, *String Theory and the Scientific
Method* (2013).

Papers: Duhem (1906); Neurath (1932); Hempel and Oppenheim (1948); Church (1949); Hempel (1950); Quine (1951); Rudner
(1953); Jeffrey (1956); Scriven (1959); Nagel (1961); Maxwell (1962); Putnam (1967, 1975); Schaffner (1967); Lakatos
(1970); Salmon (1971, 1984); Friedman (1974); Fodor (1974); Laudan (1977, 1981, 1983); Granovetter (1978); Langley
(1978); Kitcher (1981); McMullin (1982); Armstrong (1983); Churchland (1985); Worrall (1989); Laudan and Leplin (1991);
Ladyman (1998); Machamer, Darden and Craver (2000); Magnus and Callender (2004); Stanford (2006); Strevens (2008);
Humphreys (2009); Fahrbach (2011); Okasha (2011); Butterfield (2011); Pigliucci and Boudry (2013); Batterman and Rice
(2014); Ellis and Silk (2014); de Regt (2017); Sullivan (2022).
