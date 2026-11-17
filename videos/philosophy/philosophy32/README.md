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

## Problems and solutions

1. Show that rule $\beta$ is valid on every model in which each action leads to a single world.

   *Solution.* $N p$ holds when $p$ is true at the actual world and no available action leads only to $\lnot p$-worlds. If every action leads to a single world, "no action guarantees $\lnot p$" means every action's world is a $p$-world. Suppose $N p$ and $N(p \to q)$. Then every action's world is in $p$ and in $p \to q$, hence in $q$; and the actual world, in $p$ and $p \to q$, is in $q$. So $N q$: rule $\beta$ holds. It fails only when an action can lead to more than one world, as with McKay and Johnson's coin.

2. Find a model on which $\beta$ fails but agglomeration holds, or prove there is none.

   *Solution.* There is none. In this semantics $N$ is closed under entailment: if $X \subseteq Y$ and $N X$, then the actual world is in $Y$, and an action leading only to $\lnot Y$ would lead only to $\lnot X$, which $N X$ excludes. Now suppose agglomeration holds and $N p$, $N(p \to q)$. Agglomeration gives $N(p \land (p \to q))$, that is $N(p \land q)$, and closure gives $N q$. So agglomeration implies $\beta$, and a model where $\beta$ fails must be one where agglomeration fails too. (A brute-force search over every model with up to four worlds and three actions finds no counterexample, as it should.)

3. Give a buffered Frankfurt case on the options model, with no flicker at all.

   *Solution.* Make Black's trigger something Jones does not do: an involuntary sign, a blush that would appear only if Jones were going to decide not to shoot, and that does not appear. Then Jones's only available action is to deliberate and decide, and it leads to one world, "shoots on his own". In the options model there is a single action, so Jones has no choice about anything: $N$(shoots) and $N$(shoots on his own) both hold, and there is no flicker of freedom at all. Yet he shoots on his own, for his own reasons, and seems responsible. Pereboom's buffered version gets the same result with a voluntary but non-robust precondition for deciding otherwise. The cost, as Widerker argued, is that the sign must be a reliable indicator of a future free decision, which an indeterminist can deny exists.

4. For the rollback, how many replays make the share within 0.01 of 0.7, 95% of the time?

   *Solution.* The share in $n$ replays has standard deviation $\sqrt{0.7 \times 0.3/n}$. For it to lie within 0.01 of 0.7 with probability 95% we need $1.96\sqrt{0.21/n} \le 0.01$, so $n \ge 1.96^2 \times 0.21/0.0001 \approx 8{,}070$. The exact binomial calculation first reaches 95% at about $n = 8{,}000$ (the lattice of possible shares makes it oscillate slightly). A thousand replays, as in the film, pin the share down only to within about 0.03.

5. Show that with no noise, the accumulator never crosses a threshold above $I/k$.

   *Solution.* Without noise the accumulator is $dx/dt = I - kx$ from $x(0) = 0$, whose solution is $x(t) = (I/k)(1 - e^{-kt})$. This increases toward $I/k$ but is below it at every finite time. So a threshold above $I/k$ is never crossed, and one at $I/k$ only in the limit. In the film's units, $I = 0.1$ and $k = 0.5$, so the ceiling is 0.2: crossing a higher threshold is the work of noise alone, which is Schurger's point about the readiness potential.

6. Write the diagonal agent for infinitely many predictors, and say what it needs to compute.

   *Solution.* Let $P_1, P_2, \ldots$ be the predictors, each a function from situations to acts (left or right), with situations numbered $1, 2, \ldots$. The diagonal agent, in situation $k$, does the opposite of $P_k(k)$. It differs from every predictor $P_k$ at situation $k$, so no predictor on the list predicts it correctly everywhere. To act, it must compute $P_k(k)$ for each $k$: it needs an effective enumeration of the predictors and the ability to run each on its own index. If the list is given by a program (an effective listing of total computable predictors), the agent is computable, and so no effective list of predictors can include every computable agent. If the list is all total computable predictors, there is no such enumeration (deciding which programs are total is undecidable), and the agent would need an oracle: Cantor's diagonal, and Turing's, again.

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
