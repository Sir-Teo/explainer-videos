# Philosophy, Built — Part 23: God and the Philosophers

Part 23 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of religion,
with every argument's logic checked. What a proof of God would need (valid, sound, not too strong, reaching the right
God), and four families of argument. Anselm's *Proslogion* II as a reductio, checked for validity; Gaunilo's island
and Plantinga's reply; Kant's thalers and Frege's second-level existence. Plantinga's modal ontological argument in four
lines, checked on every reflexive frame with up to three worlds (valid on all 8 S5 frames, on only 8 of 34 S4 frames;
the conclusion needs only B), and its mirror image, equally valid. Gödel's ontological proof formalized in a finite
higher-order modal logic (properties as sets of world-individual cells, positiveness as a set of properties): across
every model with up to four cells, Gödel's own axioms have no model (Benzmüller and Woltzenlogel Paleo, 2016), and
every model of Scott's axioms has one God and a single world, the modal collapse Sobel proved in 1987: **the Wall's
twenty-third brick**. Aquinas's five ways, with a relay of overlapping lifetimes as a countermodel to the third way's
quantifier shift; causal series *per se* and *per accidens*; Leibniz's argument from contingency, Cleanthes and
Edwards's Inuit. The principle of sufficient reason and van Inwagen's collapse argument, checked on finite spaces of
worlds (no proposition can explain the big conjunctive contingent fact once there are two worlds), with Pruss's,
Spinoza's and Della Rocca's responses. The kalām: al-Ghazālī's planets counted over growing pasts, Hilbert's hotel and
Craig's subtraction argument, Tristram Shandy, and what cosmology (Borde, Guth and Vilenkin; Hartle and Hawking) does
and does not show. Design: Paley, Hume, Darwin and Sober's likelihoods; fine-tuning with a window of width 0.001
(likelihood ratio 500), a multiverse of 10 000 universes on the evidence that *some* universe permits life and on the
evidence that *this* one does (Hacking's and White's inverse gambler's fallacy), and the measure and prediction
problems. Pascal's wager with infinite utilities, Hájek's mixed strategies (four of five strategies tie at infinity),
Bernoulli's St. Petersburg game simulated, many gods, James and Clifford. The logical problem of evil (Part 2's six
claims, Mackie) and Plantinga's free-will defence given a model; transworld depravity pictured; Molina and Adams;
natural evil. Rowe's fawn as a Bayesian update and the evidential problem as a **Price List** (Rowe, van Inwagen,
theodicy, skeptical theism), CORNEA and Draper. Hume on miracles by the numbers: one witness leaves a one-in-a-million
miracle at about one in ten thousand; four independent witnesses make it more probable than not (Price, Babbage,
Earman), and why independence matters. Foreknowledge and freedom: Boethius, Ockham, Molina, open theism, and Prior's
branching time built (the Peircean and Ockhamist verdicts on the sea battle). Reformed epistemology, Alston's
perception of God, Schellenberg's hiddenness argument, and religious disagreement. Udayana's Nyāya proofs,
Dharmakīrti's dilemma for a permanent creator (checked for consistency), Avicenna's Necessary Existent, and the Dao.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/theism.py` (with
`prop` for the consistency checks), tested in `tests/philosophy/test_theism.py` and cached by
[`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy23.compute       # every computed item (seconds; .cache/philosophy23)
python tools/build.py philosophy23 -q l                # 480p preview
python tools/build.py philosophy23                     # 1080p30 -> renders/philosophy23.mp4
python tools/qa_scene.py philosophy23 Godel            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Leibniz (1714); what a proof would need; four families; the plan. | — |
| 1 | `Anselm` | Anselm (1078); Gaunilo; Plantinga (1974); Kant (1781); Frege. | Proslogion II checked for validity |
| 2 | `Plantinga` | Plantinga (1974); Malcolm (1960); Hartshorne (1962). | the argument and its mirror on every small frame |
| 3 | `Godel` | Gödel (1970, published 1987); Scott; Sobel (1987); Benzmüller and Woltzenlogel Paleo (2016); Anderson; Fitting; **the Wall's twenty-third brick**. | every finite model of Gödel's and Scott's axioms |
| 4 | `Cosmos` | Aquinas (1270); Leibniz (1714); Hume (1779); Edwards (1959). | a countermodel to the third way |
| 5 | `PSR` | Leibniz; Spinoza (1677); van Inwagen (1983); Pruss (2006); Della Rocca (2010). | explainers of the big conjunctive contingent fact |
| 6 | `Kalam` | al-Ghazālī (1095); Craig (1979); Russell; Borde, Guth and Vilenkin (2003); Hartle and Hawking (1983). | planetary revolutions over growing pasts |
| 7 | `Design` | Paley (1802); Hume; Darwin; Sober (2003); Hacking (1987); White (2000); McGrew, McGrew and Vestrup (2001); Carter (1974). | fine-tuning likelihoods and posteriors with a multiverse |
| 8 | `Wager` | Pascal (1670); Hájek (2003); Bernoulli (1738); James (1896); Clifford (1877). | five strategies' expected utilities; the St. Petersburg game |
| 9 | `Evil` | Mackie (1955); Plantinga (1974); Molina (1588); Adams (1977); Swinburne; Hick (1966). | Mackie's set and the free-will defence's model |
| 10 | `Evidence` | Rowe (1979); van Inwagen (2006); Wykstra (1984); Bergmann (2001); Draper (1989); the evidential problem as a **Price List**. | Rowe's posterior as a function of P(E given God) |
| 11 | `Miracles` | Hume (1748); Price (1767); Babbage (1837); Earman (2000). | the posterior against the number of witnesses |
| 12 | `Foreknow` | Boethius (524); Ockham; Molina; open theism; Prior (1967); Frankfurt (1969). | the sea battle in Peircean and Ockhamist time |
| 13 | `Experience` | Plantinga (2000); Alston (1991); Swinburne; Schellenberg (1993); Hick (1989). | — |
| 14 | `Traditions` | Udayana (984); Dharmakīrti (c. 640); Avicenna (1037); the *Daodejing*. | Dharmakīrti's four claims checked |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Oppy, *Arguing about Gods* (2006); Mackie, *The Miracle of Theism* (1982); Swinburne, *The Existence of God*
(2nd ed., 2004); Plantinga, *God, Freedom, and Evil* (1974) and *Warranted Christian Belief* (2000); Craig and
Moreland (eds.), *The Blackwell Companion to Natural Theology* (2009); Sobel, *Logic and Theism* (2004); Pruss, *The
Principle of Sufficient Reason* (2006); Earman, *Hume's Abject Failure* (2000); van Inwagen, *The Problem of Evil*
(2006); Hájek, "Pascal's Wager" (*Stanford Encyclopedia of Philosophy*).

Papers and primary texts: Anselm (1078); Aquinas, *Summa Theologiae* I q. 2 a. 3; al-Ghazālī (1095); Avicenna;
Udayana; Dharmakīrti; Boethius (524); Molina (1588); Pascal (1670); Leibniz (1714); Hume (1748, 1779); Kant (1781);
Paley (1802); Clifford (1877); James (1896); Mackie (1955); Malcolm (1960); Hick (1966); Prior (1967); Rowe (1979);
Craig (1979); van Inwagen (1983); Wykstra (1984); Sobel (1987); Hacking (1987); Draper (1989); Schellenberg (1993);
White (2000); Hájek (2003); Borde, Guth and Vilenkin (2003); Benzmüller and Woltzenlogel Paleo (2016).
