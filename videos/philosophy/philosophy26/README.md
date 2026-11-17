# Philosophy, Built — Part 26: The Quantum Puzzle

Part 26 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of quantum
mechanics, with the no-go theorems computed on a small Hilbert-space simulator. The formalism in one chapter (states,
superposition, the Born rule sampled two thousand times at each of five angles; a Mach–Zehnder interferometer whose
fringe visibility equals the overlap of the which-path records; uncertainty on a qubit, with Robertson's bound and
ΔX² + ΔZ² ≥ 1 checked on five thousand random states; entanglement). The measurement problem: a linear pointer,
Schrödinger's cat, improper mixtures (half a singlet is ½I, like a coin flip, but the pair is pure), and Maudlin's
three claims as a **Price List** (Bohm, GRW and Everett each give up one). EPR's criterion of reality and Bohm's spin version. Bell's theorem: the CHSH inequality derived
line by line, all 16 local deterministic strategies enumerated (|S| = 2 always), the singlet's 2√2 at the standard
angles and Tsirelson's bound found by a search over angles; the correlation curve; Mermin's device (every instruction
set agrees on at least 5 of 9 setting pairs, the quantum device on half of 9 000 runs). The CHSH game: every classical
strategy played (eight win 3/4, eight win 1/4) and the quantum strategy simulated over 20 000 games (0.856 against
cos²(π/8) ≈ 0.854); the PR box (no-signalling, S = 4) and the ladder 2, 2√2, 4: **the Wall's twenty-sixth brick**
(Bell; Kochen–Specker). Fifty years of experiments, from
Freedman and Clauser to the 2015 loophole-free tests and the 2022 Nobel prize. GHZ: four certain predictions,
0 of 64 local assignments, and the GHZ game (64 classical strategies, none above 3/4; the GHZ strategy always wins).
Kochen–Specker and the Peres–Mermin square: operator products computed, 0 of 512 assignments, the best meeting 5 of 6
constraints; Cabello's eighteen-vector parity proof (0 of 2¹⁸ = 262 144 assignments); contextuality. Spekkens' toy
theory (six states of knowledge over four real states) and PBR: the entangled measurement whose outcomes are each
forbidden for one of four product preparations. Everett: branching, decoherence computed (|ρ₀₁| = ½ cosⁿθ), branches
counted against weighed (fifty measurements with Born weights 0.9 and 0.1), and the probability problem (Deutsch,
Wallace, Sebens and Carroll, and their critics). Bohmian mechanics: sixty trajectories integrated through two slits,
never crossing, reproducing the fringes; which slit, and the 'surreal trajectories' dispute. GRW: rates for one particle and a
pointer, a simulated hit, and the experiments that bound it (Donadi et al. 2021). QBism, relational quantum mechanics,
Wigner's friend with the measurement that tells unitary evolution from collapse (1 against ½), and Frauchiger–Renner
as a second **Price List**. The free will theorem, device-independent
cryptography, certified randomness, and the interpretation-neutrality of quantum computing.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/quantum.py` (with
`prop` for the Price Lists), tested in `tests/philosophy/test_quantum.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy26.compute       # every computed item (seconds; .cache/philosophy26)
python tools/build.py philosophy26 -q l                # 480p preview
python tools/build.py philosophy26                     # 1080p30 -> renders/philosophy26.mp4
python tools/qa_scene.py philosophy26 Game             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Feynman (1965); the puzzle; the plan. | — |
| 1 | `Formalism` | Born (1926); von Neumann (1932); Robertson (1929); Schrödinger (1935). | the Born rule, sampled; an interferometer with which-path markers; 5 000 random states |
| 2 | `Measurement` | Schrödinger's cat (1935); d'Espagnat; Bell (1990); Maudlin (1995); the measurement problem as a **Price List**. | the reduced state of half a singlet; purities |
| 3 | `EPR` | Einstein, Podolsky and Rosen (1935); Bohm; Bohr; Einstein (1947). | — |
| 4 | `Bell` | Bell (1964); Clauser, Horne, Shimony and Holt (1969); Tsirelson (1980); Mermin (1981). | 16 local strategies; 2√2; the correlation curve; 8 instruction sets, 9 000 runs |
| 5 | `Game` | the CHSH game; Popescu and Rohrlich (1994); van Dam (2005); Pawłowski et al. (2009); **the Wall's twenty-sixth brick**. | every classical strategy; 20 000 quantum games; the PR box's marginals |
| 6 | `Experiments` | Freedman and Clauser (1972); Aspect (1982); Weihs et al. (1998); Hensen, Giustina, Shalm et al. (2015); the Big Bell Test (2018); Nobel (2022). | — |
| 7 | `GHZ` | Greenberger, Horne and Zeilinger (1989); Pan et al. (2000); Mermin (1990). | eigenvalues; 64 assignments; the GHZ game's 64 strategies |
| 8 | `Kochen` | Kochen and Specker (1967); Peres and Mermin (1990); Cabello, Estebaranz and García-Alcaine (1996); Howard et al. (2014). | the magic square; 512 assignments; 18 vectors, 2¹⁸ assignments |
| 9 | `PBR` | Spekkens (2007); Pusey, Barrett and Rudolph (2012). | the toy theory's table; the PBR probability table |
| 10 | `Everett` | Everett (1957); Deutsch (1999); Wallace (2012); Vaidman; Sebens and Carroll; Albert, Kent, Price. | decoherence; branches counted and weighed |
| 11 | `Bohm` | de Broglie (1927); Bohm (1952); Englert et al. (1992); Dürr et al. (1993); Kocsis et al. (2011); Bell (1982). | two-slit trajectories; which slit |
| 12 | `GRW` | Ghirardi, Rimini and Weber (1986); Diósi and Penrose; Donadi et al. (2021). | rates; a hit |
| 13 | `Friend` | QBism (Fuchs, Schack, Caves); Rovelli (1996); Bohr; Wigner (1961); Proietti et al. (2019); Frauchiger and Renner (2018) as a **Price List**. | Wigner's test, 2 000 runs each way |
| 14 | `FreeWill` | Conway and Kochen (2006); Ekert (1991); Pironio et al. (2010); Shor; Deutsch. | — |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. Show that $\langle \Psi^- | \sigma_a \otimes \sigma_b | \Psi^- \rangle = -\cos(a - b)$.

   *Solution.* Measure in the x–z plane: $\sigma_a = \cos a\,Z + \sin a\,X$. Expanding, $\langle\sigma_a \otimes \sigma_b\rangle = \cos a\cos b\,\langle ZZ\rangle + \sin a\sin b\,\langle XX\rangle + \cos a\sin b\,\langle ZX\rangle + \sin a\cos b\,\langle XZ\rangle$. For $|\Psi^-\rangle = (|01\rangle - |10\rangle)/\sqrt2$: $ZZ$ gives $-1$ on both terms; $XX$ swaps $|01\rangle$ and $|10\rangle$, sending $|\Psi^-\rangle$ to $-|\Psi^-\rangle$; and $ZX$, $XZ$ map it to a state orthogonal to it, so their expectations vanish. Hence $-\cos a\cos b - \sin a\sin b = -\cos(a - b)$: perfect anticorrelation along any common axis.

2. Find CHSH settings giving $|S| = 2.5$. What is the classical model nearest to them?

   *Solution.* Space the four settings evenly, $a = 0$, $b = \varphi$, $a' = 2\varphi$, $b' = 3\varphi$. With $E = -\cos(\text{angle})$, $|S| = 3\cos\varphi - \cos 3\varphi$, which is $2\sqrt2$ at $\varphi = 45^\circ$. It equals 2.5 at $\varphi \approx 26.4^\circ$ (and again at $60^\circ$). Equivalently, keep the optimal settings and add noise: a singlet of visibility $V = 2.5/2\sqrt2 = 0.884$ gives 2.5. The nearest a local model can come is $|S| = 2$, reached by a deterministic strategy (say every answer $+1$, which satisfies three of the four terms) or, for the noisy singlet, at visibility $1/\sqrt2$, below which a local model reproduces the statistics.

3. Prove that shared randomness cannot raise the CHSH game above $\tfrac34$.

   *Solution.* With shared randomness $\lambda$, a strategy is a mixture of deterministic ones: $P(\text{win}) = \sum_\lambda p(\lambda)\,P(\text{win} \mid \lambda)$, an average, so it is at most the best deterministic value. A deterministic strategy is four bits $a_0, a_1, b_0, b_1$, and winning all four questions would need $a_0 \oplus b_0 = 0$, $a_0 \oplus b_1 = 0$, $a_1 \oplus b_0 = 0$ and $a_1 \oplus b_1 = 1$. Adding the four equations modulo 2, the left side is 0 (each bit appears twice) and the right side 1. So at most three of the four questions are won: $P(\text{win}) \le 3/4$.

4. Write the four-particle GHZ argument. How many local assignments must fail?

   *Solution.* Take $(|0000\rangle + |1111\rangle)/\sqrt2$. Products with an even number of Y's are certain: $XXXX = +1$, and every product with two X's and two Y's is $-1$ (and $YYYY = +1$). Now suppose predetermined values $x_i, y_i = \pm1$. Multiply $XXYY$, $XYXY$ and $XYYX$: $(x_1x_2y_3y_4)(x_1y_2x_3y_4)(x_1y_2y_3x_4) = x_1x_2x_3x_4$, since $x_1^3 = x_1$ and each $y$ appears twice. Quantum mechanics says the left side is $(-1)^3 = -1$ and the right side $+1$. Every one of the $2^8 = 256$ assignments fails at least one of the eight certain predictions; the best satisfy six.

5. In the Peres–Mermin square, which single constraint can always be met last? Why five, not six?

   *Solution.* For any assignment of $\pm1$ to the nine cells, the product of the three row products and the product of the three column products are both the product of all nine numbers, so they are equal. The constraints demand $+1$ for all rows (product $+1$) and $+1, +1, -1$ for the columns (product $-1$): impossible together, so at least one constraint fails, for every assignment. But any five can be met: fill the cells to satisfy the constraints you choose, and the sixth is then forced to the wrong sign by the parity count. Which one is left over is entirely up to you; that is why the best assignments meet five, and none meets six.

6. GRW: how many particles must a superposition involve to collapse within a microsecond?

   *Solution.* A GRW hit comes to each particle at a rate of about $10^{-16}$ per second, and a hit on any one particle of an entangled pointer collapses the whole superposition, so $N$ particles collapse at rate $N \times 10^{-16}$ per second, with mean waiting time $10^{16}/N$ seconds. For a mean time of one microsecond, $N = 10^{16}/10^{-6} = 10^{22}$ particles: about a tenth of a gram of matter, small next to the $10^{23}$ particles of a pointer.

## Sources

Texts: Albert, *Quantum Mechanics and Experience* (1992); Bell, *Speakable and Unspeakable in Quantum Mechanics*
(1987); Wallace, *The Emergent Multiverse* (2012); Dürr, Goldstein and Zanghì, *Quantum Physics without Quantum
Philosophy* (2013); Maudlin, *Philosophy of Physics: Quantum Theory* (2019); Myrvold, "Philosophical Issues in Quantum
Theory" (*Stanford Encyclopedia of Philosophy*).

Papers: Born (1926); Robertson (1929); von Neumann (1932); Einstein, Podolsky and Rosen (1935); Schrödinger (1935); Bohm (1952); Everett
(1957); Wigner (1961); Bell (1964, 1982); Kochen and Specker (1967); Clauser, Horne, Shimony and Holt (1969); Freedman
and Clauser (1972); Tsirelson (1980); Aspect, Dalibard and Roger (1982); Ghirardi, Rimini and Weber (1986);
Greenberger, Horne and Zeilinger (1989); Peres (1990); Mermin (1981, 1990); Ekert (1991); Englert, Scully, Süssmann and
Walther (1992); Dürr, Fusseder, Goldstein and Zanghì (1993); Popescu and Rohrlich (1994); Maudlin (1995); Rovelli
(1996); Cabello, Estebaranz and García-Alcaine (1996); Weihs et al. (1998); Deutsch (1999); Pan et al. (2000); Caves,
Fuchs and Schack (2002); van Dam (2005); Conway and Kochen (2006); Spekkens (2007); Pawłowski et al. (2009); Pironio
et al. (2010); Kocsis et al. (2011); Pusey, Barrett and Rudolph (2012); Howard et al. (2014); Hensen et al., Giustina
et al., Shalm et al. (2015); Frauchiger and Renner (2018); Sebens and Carroll (2018); Proietti et al. (2019); Donadi et
al. (2021).
