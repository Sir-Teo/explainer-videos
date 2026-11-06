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

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/quantum.py` (with
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
