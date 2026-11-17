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

## Problems and solutions

1. Show that Church's $D$ is not entailed by $O_1, O_2, O_3$ alone, so it is not itself an observation.

   *Solution.* Church's sentence is $D = (\lnot O_1 \land O_2) \lor (O_3 \land \lnot S)$. Make all three observations true: the first disjunct is false, and $D$ reduces to $\lnot S$. So whether $D$ holds is not settled by $O_1, O_2, O_3$; it depends on the arbitrary $S$. $D$ is not entailed by the observations (nor is its negation), so it is not itself an observation report. It is a theoretical sentence that Ayer's criterion counts as directly verifiable, which is how every $S$ slips in.

2. State the flagpole as a Woodward intervention. Which variable can be set, and which follows?

   *Solution.* The variables are the pole's height $H$, the sun's elevation $\theta$ and the shadow's length $L$, with $L = H/\tan\theta$. On Woodward's account an explanation cites a relation that stays true under interventions. Set the height (cut the pole, or lengthen it) with $\theta$ fixed, and the shadow changes as the equation says: $H$ can be set and $L$ follows. Set the shadow by some other means (cover the ground, cast another shadow over it) and the pole's height does not change. The relation is invariant under interventions on $H$ but not on $L$, so the height explains the shadow and not the reverse.

3. With $P(S \mid T) = 0.9$ and $P(S \mid \lnot T) = 0.1$, what base rate makes $P(T \mid S) = 1/2$?

   *Solution.* Let $\pi$ be the base rate of true theories. $P(T \mid S) = 0.9\pi / (0.9\pi + 0.1(1 - \pi))$. Setting this to $1/2$ gives $0.9\pi = 0.1(1 - \pi)$, so $\pi = 0.1$. If one candidate theory in ten is true, success makes a theory exactly as likely true as false; below that, a successful theory is more likely false. The no-miracles argument is only as strong as the unknown base rate.

4. Show that a Galilean boost leaves Newton's equations for two bodies unchanged.

   *Solution.* A boost is $x' = x - vt$, $t' = t$. Differentiating twice, $\ddot x' = \ddot x$: accelerations are the same in both frames. Newtonian forces between two bodies depend on their separation, and $x_1' - x_2' = x_1 - x_2$, so the forces are unchanged, and masses are unchanged. So $m_1 \ddot x_1 = F(x_1 - x_2)$ and $m_2 \ddot x_2 = -F(x_1 - x_2)$ hold in the boosted frame in the same form. Velocities change by $v$, so no experiment on the pair reveals absolute velocity: Galileo's ship.

5. Coarse-grain a $9 \times 9$ checkerboard by $3 \times 3$ majority. What do you get, and why?

   *Solution.* Every $3 \times 3$ block of a checkerboard has five squares of one colour and four of the other, and the majority colour is the colour of its corners. The corner of block $(i, j)$ sits at $(3i, 3j)$, whose colour has the parity of $3i + 3j$, that is, of $i + j$. So the coarse-grained picture is a $3 \times 3$ checkerboard: the pattern is a fixed point of the coarse-graining, as perfect alternation looks the same at every scale. (With an even block size the blocks would tie.) Coarse-graining once more leaves a single square.

6. In the inductive-risk model, find the threshold when the two costs are equal and $P(\text{toxic}) = 1/2$.

   *Solution.* In the Reasoner's model the statistic is $N(0, 1)$ for a safe chemical and $N(1.5, 1)$ for a toxic one. With equal costs and equal priors, expected loss is smallest where the two densities cross, halfway: threshold 0.75. Both error rates are then 22.7%. The film's threshold of about 1.3, with equal costs, came from its prior of 0.3 on toxicity; with the prior at one half the threshold falls, and the same data are called toxic more often.

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
