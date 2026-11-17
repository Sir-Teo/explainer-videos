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

## Problems and solutions

1. Add a term $0.5\,t^3$ to the falling-body law. How many data points before the best system finds it?

   *Solution.* Use the film's mosaic: $t$ from 0 to 2, noise of standard deviation 0.6, code length $\tfrac{n}{2}\log_2(2\pi e\,\hat\sigma^2) + \tfrac{d+1}{2}\log_2 n$. On $[0, 2]$ the cubic term is mostly absorbed by the quadratic: the best parabola misses $0.5\,t^3$ by only about 0.076 in standard deviation, an eighth of the noise. So the extra parameter pays for itself only with many points. Over 300 noise draws each, the cubic is chosen about 20% of the time with 40 points, half the time at about 400, 84% at 800 and 92% at 1,000. The best system finds a small, nearly collinear term only when the mosaic is large; until then the quadratic really is the better system.

2. Past: 50 heads in 100 tosses. What chance do the next 100 tosses give to undermining futures?

   *Solution.* On the Humean view the chance of heads is the frequency over the whole history of 200 tosses, so "the chance is one half" requires exactly 50 heads in the next 100. Every other future undermines it. The theory gives that future probability $\binom{100}{50}/2^{100} = 0.080$, so it gives undermining futures probability $0.920$, more than the film's 75% with ten tosses: the longer the future, the more of its probability the theory spends on its own falsity.

3. For a dome of height $\propto r^{a}$, for which exponents $a$ can the ball start to slide on its own?

   *Solution.* Along the surface the pull of gravity is proportional to the slope, so the equation of motion is $\ddot r = c\,r^{a-1}$. Try $r = A\,t^k$, which starts at rest at the top: $k(k-1)\,A\,t^{k-2} = c\,A^{a-1}\,t^{k(a-1)}$, so $k - 2 = k(a - 1)$, $k = 2/(2 - a)$. This is a genuine start from rest ($k > 1$, so $\dot r(0) = 0$) exactly when $0 < a < 2$. The top must also be an equilibrium, a point where the force vanishes, which needs $a > 1$ (at $a = 1$ the dome is a cone and the ball cannot rest at the apex). So the ball can start to slide on its own for $1 < a < 2$; Norton's dome, $a = 3/2$, gives $r \propto t^4$. At $a = 2$ the force is linear, Lipschitz, and the solution is unique.

4. With $\lambda = 0.9$, what initial precision forecasts the Lorenz system to time 50?

   *Solution.* A forecast fails when the error, growing like $\varepsilon\,e^{\lambda t}$, reaches the size of the attractor, about 1 in the film's units, so the horizon is $t \approx \ln(1/\varepsilon)/\lambda$. For $t = 50$ with $\lambda = 0.9$, $\ln(1/\varepsilon) = 45$ and $\varepsilon = e^{-45} \approx 3 \times 10^{-20}$: about twenty correct decimal digits in the initial state, where one in a thousand bought about seven time units.

5. Show that a Kac ring with an even number of marks returns to its start after $N$ ticks.

   *Solution.* After $N$ ticks every ball has moved once around the ring of $N$ sites, so it is back at its starting site, and it has crossed every edge exactly once, so it has changed colour once for each mark. With an even number of marks every ball has changed colour an even number of times and has its original colour. So the whole configuration recurs after $N$ ticks. (With an odd number of marks every ball has the opposite colour at $N$, and the start recurs at $2N$, as in the film.)

6. Szilard's engine with the partition at $\tfrac13$: the expected work, and the cost of erasing the record.

   *Solution.* With the partition at $x = 1/3$, the molecule is on the small side with probability $1/3$ and expands it to the whole box, gaining $kT\ln 3$; on the large side, probability $2/3$, it gains $kT\ln(3/2)$. Expected work: $kT\big(\tfrac13\ln 3 + \tfrac23\ln\tfrac32\big) = kT \times 0.637$, the Shannon entropy of the measurement in nats (0.918 bits), less than the $kT\ln 2$ of a central partition. Erasing the record costs at least $kT$ times its entropy, $0.637\,kT$, if the eraser exploits the known odds, and $kT\ln 2$ for a memory treated as a full bit. Either way the cycle gains nothing.

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
