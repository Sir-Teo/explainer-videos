# Philosophy, Built — Part 32: Free Will

Part 32 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the last part of Act VI,
*Mind and Meaning*: whether anything we do is up to us, with the consequence argument's rules checked on a model,
Frankfurt's case modelled, an undetermined moment replayed a thousand times, a readiness potential rebuilt from noise,
and a diagonal that keeps a mind from predicting itself. Schopenhauer (1839); determinism defined (Laplace 1814; Part
24) and the dilemma of luck. Aristotle's sea battle and logical fatalism; Chrysippus's cylinder (Cicero, *On Fate*) and
the lazy argument with co-fated events. List's levels (2019): 900 microstates, each with one successor, grouped
into three agent-level states, from which 'deliberating' leads to tea 0.45, coffee 0.40, still deliberating 0.15. Van Inwagen's consequence argument (1983) with the operator N and rules α and β,
derived step by step. A model of options (each action the set of worlds it might lead to; N p when p is true and no
action guarantees not-p): on McKay and Johnson's coin (1996) N(no heads) and N(no tails) hold but N(not tossed) does
not, so agglomeration fails, and with it rule β; checked on all 64 pairs of the model's 8 propositions (α fails 0 times,
β twice, β□ never), the repaired argument of Finch and Warfield (1998), and **the Wall's thirty-second brick**.
Frankfurt cases (1969) on the same model (no choice about whether Jones shoots, a choice about whether he shoots on his
own: a flicker of freedom), Fischer's flickers, Widerker's dilemma and buffered cases. Compatibilism: Hobbes and Hume
and the conditional analysis; Frankfurt's hierarchy (1971); Fischer and Ravizza's reasons-responsiveness (1998);
Lewis's local miracles (1981); the free will tetrad as a **Price List** with the PhilPapers 2020 shares (compatibilism
59%, libertarianism 19%, no free will 11%). Libertarianism: agent causation (Chisholm; O'Connor) and Kane's
self-forming actions (1996); van Inwagen's rollback simulated (708 truths in 1000 replays at a chance of 0.7).
Where indeterminism could act: a torn decision as a damped double well, where an offset of 10⁻³⁰ still decides, each
factor of ten adding 2.95 time units (Balaguer 2010; Tegmark 2000). Pereboom's four cases and Galen Strawson's basic
argument (1994); life without basic desert. P. F. Strawson's
'Freedom and Resentment' (1962), the participant and objective stances, the faces of responsibility (Watson 1996;
Shoemaker 2015), Wallace, Watson and experimental philosophy.
Libet (1983) and Schurger, Sitt and Dehaene's leaky stochastic accumulator (2012), built: 964 of 1000 runs cross
within 20 s, mean 6.3 s; averaged backward from the crossings, the noise alone rises from 0.118 to 0.300, half of it in
the last 0.35 s; Soon et al. (2008) and Maoz et al. (2019). Dennett's evitability: in a deterministic world of falling rocks a blind agent is hit 34 times in 400 steps, a sighted
one dodges 32 times and is never hit, and a rerun repeats every step. Self-prediction: a contrarian agent defeats both public
predictions (MacKay 1960), a diagonal agent differs from every one of six predictors (Part 7), and Newcomb's problem
(Nozick 1969). The free will theorem (Conway and Kochen 2006) and what it does and does not show. Moral luck (Williams;
Nagel 1976): six of ten thousand equally careless drivers kill a child; four kinds of luck; two ledgers, by outcome
(6 units on 6 drivers) and by risk (0.0005 on each, 5 in all), with a victim 99.33% certain (Zimmerman 2002). Responsibility gaps for
learning machines (Matthias 2004; Sparrow 2007) and ways to close them.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/freewill.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_freewill.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy32.compute       # every computed item (seconds; .cache/philosophy32)
python tools/build.py philosophy32 -q l                # 480p preview
python tools/build.py philosophy32                     # 1080p30 -> renders/philosophy32.mp4
python tools/qa_scene.py philosophy32 Beta             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Schopenhauer (1839); four questions; the plan. | — |
| 1 | `Dilemma` | Laplace (1814); determinism defined (Part 24); List (2019); the dilemma. | a world deterministic below, open at the agent's level |
| 2 | `Fate` | Aristotle; Chrysippus (Cicero, *On Fate*); the lazy argument. | — |
| 3 | `Consequence` | van Inwagen (1983): N, α, β, the derivation. | — |
| 4 | `Beta` | McKay and Johnson (1996); Finch and Warfield (1998); **the Wall's thirty-second brick**. | every instance of α, β and β□ on the coin |
| 5 | `Frankfurt` | Frankfurt (1969); Fischer (1994); Widerker (1995); Hunt; Pereboom. | the case on the options model |
| 6 | `Compatibilism` | Hobbes (1651); Hume (1748); Frankfurt (1971); Fischer and Ravizza (1998); Lewis (1981); **the Price List**. | the tetrad's minimal conflicts |
| 7 | `Libertarian` | Reid; Chisholm (1964); O'Connor (2000); Kane (1996); Balaguer (2010); Tegmark (2000); van Inwagen (2000). | a torn decision in a double well; 1000 replays of one moment |
| 8 | `Hard` | Pereboom (2001, 2014); G. Strawson (1994); Caruso. | — |
| 9 | `Reactive` | P. F. Strawson (1962); Watson (1996); Scanlon; Shoemaker (2015); Wallace (1994); Watson (1987); Nahmias. | — |
| 10 | `Libet` | Libet et al. (1983); Schurger, Sitt and Dehaene (2012); Soon et al. (2008); Maoz et al. (2019). | a leaky accumulator; its backward average |
| 11 | `Predict` | Dennett (1984, 2003); MacKay (1960); the diagonal (Part 7); Nozick (1969). | a deterministic avoider; a contrarian; a diagonal over six predictors |
| 12 | `Theorem` | Conway and Kochen (2006); Kochen–Specker; Bell (Part 26). | — |
| 13 | `Luck` | Williams and Nagel (1976, 1979); Zimmerman (2002); Enoch and Marmor (2007). | 10 000 careless drivers; two ledgers of blame |
| 14 | `Machines` | Matthias (2004); Sparrow (2007). | — |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Kane (ed.), *The Oxford Handbook of Free Will* (2nd ed., 2011); van Inwagen, *An Essay on Free Will* (1983);
Fischer, Kane, Pereboom and Vargas, *Four Views on Free Will* (2007); McKenna and Pereboom, *Free Will: A Contemporary
Introduction* (2016).

Primary texts and papers: Aristotle, *On Interpretation* 9; Cicero, *On Fate*; Hobbes (1651); Hume (1748); Laplace
(1814); Schopenhauer (1839); MacKay (1960); P. F. Strawson (1962); Chisholm (1964); Frankfurt (1969, 1971); Nozick
(1969); Williams (1976); Nagel (1979); Lewis (1981); Libet et al. (1983); Watson (1987); G. Strawson (1994); Fischer
(1994); Wallace (1994); Widerker (1995); Kane (1996); McKay and Johnson (1996); Finch and Warfield (1998); Fischer and
Ravizza (1998); O'Connor (2000); van Inwagen (2000); Pereboom (2001, 2014); Matthias (2004); Conway and Kochen (2006);
Sparrow (2007); Soon et al. (2008); Schurger, Sitt and Dehaene (2012); Maoz et al. (2019); Bourget and Chalmers (2023).
