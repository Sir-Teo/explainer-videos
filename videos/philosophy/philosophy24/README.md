# Philosophy, Built — Part 24: Laws, Chance and the Arrow

Part 24 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the metaphysics of physics,
with every toy universe built. What laws are: the regularity view and van Fraassen's two spheres (gold, and
uranium-235 above its 52 kg critical mass); Lewis's best-system account built as a contest of polynomial laws on 40
noisy measurements of a falling ball, scored by two-part description length (the quadratic wins, at about 60 bits);
Armstrong, Dretske and Tooley's necessitation and Lewis's "mighty biceps" objection; Bird's powers and Maudlin's
primitivism; Albert and Loewer's Mentaculus. Chance: the Principal Principle; Humean chance in a world of twenty coin
tosses, where undermining futures carry 75% of the chance; the big bad bug derived; Hall's and Lewis's New Principle,
checked against the old as the world grows (one in twelve against one eighth, agreeing to four decimals at 10 000
tosses). Determinism defined by models (Earman, Montague) and checked theory by theory; Norton's dome, its solutions
r(t) = (t − T)⁴/144 verified numerically and animated as four histories that agree and then part, and the
Lipschitz condition they violate. Chaos: the Lorenz system, two runs 10⁻⁹ apart, a Lyapunov exponent of about 0.90,
forecast horizons; Poincaré's roulette wheel, where four very different spreads of speeds all give red with chance
one half. Statistical mechanics: Boltzmann's counting for a hundred molecules; a toy kinetic gas in which H falls to
Maxwell's distribution; Loschmidt's reversal of the hook's gas; Poincaré recurrence with rotors; the Kac ring of
1959, built: decay like (1 − 2μ)ᵗ, all black at t = N (27 marks), all white at 2N, reversal, and a typical
low-entropy present that is a dip, with entropy rising toward the past as well as the future: **the Wall's
twenty-fourth brick** (Loschmidt). The Past Hypothesis, Penrose's 1 in 10^(10^123), Boltzmann's fluctuation and
Boltzmann brains, and the arrow of time as a **Price List**. Maxwell's demon, Szilard's engine simulated (expected work
kT times the entropy of the measurement), Landauer's bound (2.87 × 10⁻²¹ J per bit at 300 K) and Bérut's
measurement, Bennett's exorcism; the AND gate's 1.19 lost bits, the Toffoli gate, compute–copy–uncompute, and how far
today's chips sit above the floor. The other arrows (radiative, causal, counterfactual, epistemic) and Lewis's
asymmetry of traces.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/physlaws.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_physlaws.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy24.compute       # every computed item (seconds; .cache/philosophy24)
python tools/build.py philosophy24 -q l                # 480p preview
python tools/build.py philosophy24                     # 1080p30 -> renders/philosophy24.mp4
python tools/qa_scene.py philosophy24 Kac              # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Laplace (1814); a film that runs both ways; three questions and a fourth; the plan. | the hook's gas |
| 1 | `Regularity` | Hume; van Fraassen (1989); Tooley (1977); Lewis's mosaic (1986). | — |
| 2 | `BestSystem` | Ramsey (1928); Lewis (1973, 1983, 1994); Rissanen; Albert and Loewer's Mentaculus. | polynomial laws scored in bits |
| 3 | `Universals` | Dretske, Tooley (1977); Armstrong (1983); Lewis (1983); van Fraassen; Bird (2007); Maudlin (2007). | — |
| 4 | `Chance` | Lewis (1980, 1986, 1994); Thau (1994); Hall (1994). | undermining futures; the New Principle |
| 5 | `Determinism` | Laplace; Montague; Earman (1986); Xia (1992); Loewer (2001); Diaconis, Holmes and Montgomery (2007); Bartoš et al. (2023). | — |
| 6 | `Dome` | Norton (2003, 2008); Picard and Lindelöf; Malament (2008); Korolev (2007). | the dome's solutions, checked |
| 7 | `Chaos` | Lorenz (1963, 1972); Benettin; Poincaré (1896); Strevens (2003). | the Lyapunov exponent; horizons; the roulette wheel |
| 8 | `Entropy` | Clausius (1865); Boltzmann (1877); Planck. | microstates of a hundred molecules |
| 9 | `Reversal` | Boltzmann (1872); Loschmidt (1876); Poincaré (1890); Zermelo (1896). | H falling; Loschmidt's reversal; recurrence |
| 10 | `Kac` | Kac (1959); **the Wall's twenty-fourth brick**. | the Kac ring, every way |
| 11 | `Past` | Albert (2000); Penrose (1979, 1989); Callender; Price; Carroll and Chen; Boltzmann (1895); Albrecht and Sorbo (2004); the arrow as a **Price List**. | fluctuation probabilities |
| 12 | `Demon` | Maxwell (1867); Szilard (1929); Landauer (1961, 1991); Bérut et al. (2012); Bennett (1982). | Szilard's engine, simulated |
| 13 | `Reversible` | Bennett (1973); Toffoli (1980); Fredkin and Toffoli (1982). | the AND gate's lost bits; the Toffoli gate |
| 14 | `Arrows` | Ritz and Einstein (1909); Popper (1956); Reichenbach; Lewis (1979); Albert; Maudlin; Price (1996). | — |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Armstrong, *What Is a Law of Nature?* (1983); Earman, *A Primer on Determinism* (1986); Sklar, *Physics and
Chance* (1993); Price, *Time's Arrow and Archimedes' Point* (1996); Albert, *Time and Chance* (2000); Strevens,
*Bigger than Chaos* (2003); Leff and Rex (eds.), *Maxwell's Demon 2* (2003); Bird, *Nature's Metaphysics* (2007);
Maudlin, *The Metaphysics Within Physics* (2007); Kac, *Probability and Related Topics in Physical Sciences* (1959).

Papers and primary texts: Laplace (1814); Clausius (1865); Maxwell (1867); Boltzmann (1872, 1877, 1895); Loschmidt
(1876); Poincaré (1890, 1896); Zermelo (1896); Ritz and Einstein (1909); Ramsey (1928); Szilard (1929); Popper
(1956); Landauer (1961, 1991); Lorenz (1963); Bennett (1973, 1982); Lewis (1973, 1979, 1980, 1983, 1986, 1994);
Dretske (1977); Tooley (1977); Penrose (1979, 1989); Toffoli (1980); Fredkin and Toffoli (1982); van Fraassen (1989);
Xia (1992); Hall (1994); Thau (1994); Loewer (2001); Norton (2003, 2008); Albrecht and Sorbo (2004); Callender (2004);
Carroll and Chen (2004); Diaconis, Holmes and Montgomery (2007); Korolev (2007); Malament (2008); Bérut et al.
(2012); Bartoš et al. (2023).
