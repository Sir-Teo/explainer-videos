# Philosophy, Built — Part 30: Mind and Machine

Part 30 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the fourth part of Act VI,
*Mind and Meaning*: the philosophy of mind, from Descartes's two substances to representation in neural networks, with
a functional role realized twice and a Chinese rulebook written. Avicenna's floating man; Descartes's dualism, the
pineal gland and the conceivability argument in modal logic; Elisabeth of Bohemia's question (1643). Ryle's category
mistake; logical behaviourism and its failures (circularity, Putnam's super-spartans, perfect actors); the identity
theory of Place and Smart; Kripke's objection and multiple realizability. Functionalism: a probabilistic machine table
for a pain role, realized in a network of threshold units and in a water tank, run in lockstep for 1000 steps (outputs
agree 1000 times; 'carry on' 468, 'say ouch' 282, 'wince' 180, 'sigh' 70 in both), machine and analytic
functionalism, and the Ramsey–Lewis definition carried out: a seven-microstate 'brain' has exactly one realization of
the theory among 1806 assignments (pain = h1 ∨ h2 ∨ h3), a tank one of 6, a thermostat none, and with only the bump
platitudes the brain has two (calm and soothed swap). Turing's imitation game, his nine objections answered one by one, and the test
since (ELIZA, the Loebner Prize, Jones and Bergen 2025). Searle's Chinese room, a rulebook of 8 rules that is perfect
on a narrow test about Schank's restaurant story (8 of 8) and helpless outside it, the systems, robot, brain-simulator
and other-minds replies, and the dilemma for functionalism. Block's Blockhead, its table measured (an hour's test needs
about 10^25 764 entries against 10^80 atoms), Leibniz's mill, the China brain, absent and inverted qualia.
Supervenience, weak, strong and global, defined and checked on three sets of worlds (A: weak only; B: global only;
C: all three). Kim's exclusion argument, step by step, **the Wall's thirtieth brick**, and the mind–body tetrad as a
**Price List** (reductive physicalism, epiphenomenalism, interactionist dualism, harmless overdetermination), and the
autonomy reply: Yablo's pigeon under interventions ('red' carries 0.714 bits about pecking with one bit of cause, as
much as the exact shade with 2.58; 'scarlet' 0.369), proportionality and realization-insensitivity (List and Menzies
2009), and Kim's answer.
Emergence: Mill and Broad, Conway's Game of Life with Gosper's glider gun simulated for 150 generations (a glider every
30; four in flight), a law about gliders found by running the rules for 600 generations (36 + 5k live cells at
generation 30k, at all 21 checks), Bedau's weak emergence and Chalmers's strong emergence. Eliminativism, its replies, and Dennett's
real patterns, measured on his bar code: pattern plus exceptions costs 3% of the bit map with no noise, 48% at 10%,
85% at 25%, and more than the bit map at 50% (a compressor agrees). Content naturalized: Dretske's information on a fuel gauge (2 bits with a perfect needle, 1.48 at 10%
error, and no reading certain once there is any error), the misrepresentation problem, Millikan's teleosemantics and the
frog, Fodor's asymmetric dependence. The language of thought, systematicity (Fodor and Pylyshyn 1988) and a SCAN-like
test built (a lookup table gets 0 of 65 held-out commands with 'jump', a compositional interpreter all 65), with Lake
and Baroni's networks. And representation in networks: the extended mind revisited, Shea's varitel semantics, and a
network whose hidden layer carries x perfectly while the output ignores it (a probe reads x at 100%; after the probe's
direction is removed a new probe is at 49.3%, and the task is still at 100%).

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/mind.py` (with `prop` for
the Price List), tested in `tests/philosophy/test_mind.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy30.compute       # every computed item (seconds; .cache/philosophy30)
python tools/build.py philosophy30 -q l                # 480p preview
python tools/build.py philosophy30                     # 1080p30 -> renders/philosophy30.mp4
python tools/qa_scene.py philosophy30 Function         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Turing (1950); four questions; the plan. | — |
| 1 | `Dualism` | Avicenna (c. 1020); Descartes (1641); Elisabeth of Bohemia (1643). | — |
| 2 | `Identity` | Ryle (1949); Putnam (1963); Place (1956); Smart (1959); Kripke (1970). | — |
| 3 | `Function` | Putnam (1967); Armstrong (1968); Lewis (1970, 1972). | one role in two substrates, 1000 steps; a Ramsey sentence's occupants |
| 4 | `Turing` | Turing (1950); Weizenbaum (1966); Jones and Bergen (2025). | — |
| 5 | `Room` | Searle (1980); Schank and Abelson; Dennett and Hofstadter (1981). | a rulebook, inside and outside its script |
| 6 | `Block` | Block (1978, 1981); Leibniz (1714). | Blockhead's table against the universe |
| 7 | `Supervenience` | Davidson (1970); Kim (1984); Jackson (1998); Horgan (1993). | three relations on three sets of worlds |
| 8 | `Exclusion` | Kim (1998); Huxley; Jackson (1982); Popper and Eccles (1977); Bennett (2003); **the Wall's thirtieth brick**; **the Price List**; Yablo (1992); Woodward (2003); List and Menzies (2009). | the tetrad's minimal conflicts; proportional causes |
| 9 | `Emergence` | Mill (1843); Broad (1925); Conway (1970); Gosper (1970); Bedau (1997); Chalmers (2006). | Gosper's gun, 150 generations; its law, to 600 |
| 10 | `Eliminate` | Churchland (1981); Baker (1987); Dennett (1987, 1991). | a bar code's description length at six noise levels |
| 11 | `Content` | Dretske (1981); Millikan (1984); Fodor (1987, 1990). | a gauge's bits at four error rates |
| 12 | `LOT` | Fodor (1975); Fodor and Pylyshyn (1988); Lake and Baroni (2018, 2023). | a table and a compositional interpreter on 65 commands |
| 13 | `Represent` | Clark and Chalmers (1998); Shea (2018); Elazar et al. (2021). | a probe, and its direction removed |
| 14 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. Realize the pain table of chapter 3 in a third substrate; prove the outputs agree step by step.

   *Solution.* Third substrate: a register holding an integer, 0 for calm, 1 for soothed, 2 for hurt, updated by a lookup from (register, input, random draw) to (new register, output) that copies the table entry for entry. Claim: fed the same inputs and the same draws, the units, the tank and the register give the same outputs at every step. Proof by induction, with the encodings units-on $\leftrightarrow$ litres $\leftrightarrow$ register value. At step 0 all three encode calm. If at step $t$ they encode the same table state, then each applies the same table entry to the same input and draw, so each emits that entry's output and moves to the encoding of that entry's next state. So they agree at step $t + 1$, and for all steps. Physically the three share nothing but the table.

2. Show that strong supervenience implies weak and global supervenience.

   *Solution.* Weak: within each world, physical twins are mental twins. Strong: for any $x$ and $y$, in the same world or different ones, physical twins are mental twins. Strong implies weak by taking $x$ and $y$ in the same world. Strong implies global: suppose worlds $w_1, w_2$ have the same physical distribution, matched by a bijection $f$ between their individuals that preserves physical properties. By strong supervenience each $x$ in $w_1$ is a mental twin of $f(x)$ in $w_2$, so $f$ also preserves mental properties, and the mental distributions are the same.

3. Find two sets of worlds: weak but not global, and global but not weak.

   *Solution.* Weak but not global (the film's set A): worlds $w_1, w_2$, individuals $a, b$, all four physically alike; in $w_1$ both are mentally M, in $w_2$ both are mentally N. Within each world physical twins are mental twins, so weak supervenience holds; but the two worlds are physically identical and mentally different, so global fails. Global but not weak (set B): in $w_1$, $a$ and $b$ are physically alike but $a$ is M and $b$ is N, so weak fails; let $w_2$ differ physically in any way. Since no two worlds share a physical distribution, global supervenience holds vacuously.

4. State Kim's argument as five propositions and find every minimal inconsistent subset.

   *Solution.* (1) Distinctness: $M \ne P$. (2) Mental causation: $M$ causes $P^*$. (3) Closure: $P^*$ has a sufficient physical cause, $P$. (4) Exclusion: no event has two sufficient causes unless it is overdetermined. (5) No systematic overdetermination. From (1)–(3), $P^*$ has two distinct causes, $M$ and $P$; by (4) it is overdetermined, which (5) forbids. Every proper subset is consistent, as the positions on the Price List show: drop (1) and you are a reductive physicalist, (2) an epiphenomenalist, (3) an interactionist dualist, (4) with Yablo or List and Menzies, (5) with Bennett. So the only minimal inconsistent subset is all five.

5. Estimate Blockhead's table for a 5-minute test with a 10\,000-word vocabulary.

   *Solution.* At the film's rate of 300 characters a minute, about 60 words a minute, a five-minute test is about 300 words of the interrogator's. With a 10,000-word vocabulary there are $10{,}000^{300} = 10^{1200}$ possible inputs, and Blockhead needs an entry for each (and for every prefix, which adds less than one part in ten thousand). Against $10^{80}$ atoms in the observable universe that is more than $10^{1100}$ entries per atom.

6. Build a network that uses $x$, and show that removing the probe's direction now hurts the output.

   *Solution.* Use the film's network (two binary inputs, 32 hidden units) but make the output depend on $x$: output $x \oplus y$. A linear probe reads $x$ from the hidden layer perfectly, and a linear readout computes $x \oplus y$ perfectly. Remove the probe's direction: the trained readout falls to chance (51% in one run), because it was using that direction. Repeat, removing each new probe direction until $x$ can no longer be read (three directions here): a freshly trained readout of the output is then at chance too. Now the information about $x$ is not just carried but used, by Shea's standard represented, and amnesic probing shows the difference that the film's network, which ignored $x$, did not.

## Sources

Texts: Kim, *Philosophy of Mind* (3rd ed., 2011) and *Mind in a Physical World* (1998); Turing (1950); Searle (1980,
with the BBS commentaries); Block (1981); Bedau (1997); Shea, *Representation in Cognitive Science* (2018); Ravenscroft,
*Philosophy of Mind: A Beginner's Guide*.

Primary texts and papers: Avicenna (c. 1020); Descartes (1641); Elisabeth of Bohemia (1643); Leibniz (1714); Mill
(1843); Huxley (1874); Broad (1925); Ryle (1949); Turing (1950); Place (1956); Smart (1959); Putnam (1963, 1967);
Weizenbaum (1966); Armstrong (1968); Davidson (1970); Kripke (1970); Conway (1970); Lewis (1970, 1972); Fodor (1975, 1987,
1990); Popper and Eccles (1977); Block (1978, 1981); Searle (1980); Churchland (1981); Dretske (1981); Dennett and
Hofstadter (1981); Jackson (1982, 1998); Kim (1984, 1998); Millikan (1984); Baker (1987); Dennett (1987, 1991); Fodor
and Pylyshyn (1988); Yablo (1992); Horgan (1993); Bedau (1997); Clark and Chalmers (1998); Bennett (2003); Woodward
(2003); Chalmers (2006); List and Menzies (2009); Lake and Baroni (2018, 2023); Elazar et al. (2021); Jones and Bergen
(2025).
