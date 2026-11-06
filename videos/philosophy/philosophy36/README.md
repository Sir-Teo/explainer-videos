# Philosophy, Built — Part 36: Weighing Lives

Part 36 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*: population
ethics and the far future. Parfit's question (1984) and his blocks; the total (Sidgwick 1874), average, critical-level
(Blackorby, Bossert and Donaldson) and variable-value (Hurka 1983; Ng 1989) views, each a formula, scored on Parfit's
sequence A, B, …, Z (twice the people, 55% of the welfare, 10% more in total at each step): four views, four best worlds
(Z, A, D, E). The repugnant conclusion, drawn and stated; scope insensitivity (Desvousges et al. 1993: $80, $78, $88
for 2,000, 20,000 and 200,000 birds) and the debunking reply (Tännsjö 2002; Huemer 2008; the joint statement of 2021);
Arrhenius's very repugnant conclusion at 601 times A's population. The mere addition paradox, A → A+ → B → B+ → C, each
view's verdict at each step; the benign addition, which only the average view refuses; and a **Price List** for the
repugnant conclusion (accept Z; deny mere addition; Parfit's perfectionism; deny transitivity, with Temkin and Rachels).
Arrhenius's impossibility theorems (2000), with the experiment behind them: six conditions, five views, a search over
small populations that puts a cross in every row, the sadistic conclusion worked through, the counterexamples shown,
and **the Wall's thirty-sixth brick**. Narveson's neutrality (1973) and McMahan's asymmetry (1981); Broome's argument
that neutrality cannot be a range (2004: six contradictions from four levels); Benatar's asymmetry and antinatalism
(2006); Parfit's non-identity problem, with depletion (no one harmed; 41,000 against 60,000) and the fourteen-year-old
girl; wide views and principle Q; Meacham's harm-minimizing view (2012), which conserves and chooses A. Discounting:
the Ramsey rule (1928) derived; Stern against Nordhaus (1.4% against 5.5%; a million dollars in a century worth
$249,003 against $4,729); one climate policy, two verdicts; Stern's δ read as a 0.1% annual chance of extinction;
Weitzman's declining rate (1998) and the Green Book's schedule. The long future: strong longtermism (Greaves and
MacAskill 2021), existential risk (Bostrom 2002; Ord's estimate, labelled as an estimate), Parfit's three outcomes
counted two ways, and Thorstad's point (2023): a point of risk is worth 0.06 of a century if risk stays at 1 in 6, and
100 centuries in a time of perils; cluelessness and washing out. Fanaticism: Pascal's mugging (Bostrom 2009); a chain of
long shots (Beckstead and Thomas) under expected value, bounded utility and probability discounting; recklessness,
timidity or intransitivity; Wilkinson (2022) and Monton (2019). Infinite ethics: catching up (1965) against an infinite
permutation; **Basu and Mitra's theorem (2003), proved** on enumerated rationals; Svensson, Zame, Bostrom's
infinitarian paralysis, Askell. Doing the most good: QALYs and DALYs; a heavy-tailed portfolio (the best intervention
44 times the median; Ord's 15,000 to one); who counts, with a toy of expected moral weights; effective altruism and its
critics (Srinivasan; Gabriel; Crary). Pricing lives: Schelling's statistical lives (1968) and a $12 million VSL from a
wage-risk trade-off; NICE's threshold and the rule of rescue (Jonsen 1986); QALYs against fair innings and priority
(Harris 1987; Williams 1997); VSL transferred across incomes, and the equity weights that undo it; Anderson (1993).

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/population.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_population.py` and cached by [`compute.py`](compute.py);
cited figures (the birds, Stern's and the EPA's social costs of carbon, Ord's estimate, NICE's threshold, the range
of US agencies' VSLs) are labelled as such.

## Build it

```bash
python -m videos.philosophy.philosophy36.compute       # every computed item (seconds; .cache/philosophy36)
python tools/build.py philosophy36 -q l                # 480p preview
python tools/build.py philosophy36                     # 1080p30 -> renders/philosophy36.mp4
python tools/qa_scene.py philosophy36 Arrhenius        # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Parfit (1984); four questions; the plan. | — |
| 1 | `Views` | Parfit; Sidgwick (1874); Blackorby, Bossert and Donaldson; Hurka (1983); Ng (1989). | Parfit's sequence under four views |
| 2 | `Repugnant` | Parfit (1984, 2016); Desvousges et al. (1993); Tännsjö (2002); Huemer (2008); Arrhenius. | the blocks; the very repugnant conclusion |
| 3 | `Addition` | Parfit (1984, 1986); Huemer (2008); Temkin (2012); Rachels (1998); **the Price List**. | the staircase; each view's verdicts; the benign addition |
| 4 | `Arrhenius` | Arrhenius (2000); **the Wall's thirty-sixth brick**. | six conditions, five views, searched; the sadistic conclusion |
| 5 | `NonIdentity` | Narveson (1973); McMahan (1981); Broome (2004); Benatar (2006); Parfit; Meacham (2012). | neutrality's contradictions; depletion; harm minimization |
| 6 | `Discount` | Ramsey (1928); Stern (2006); Nordhaus (2008); EPA (2023); Weitzman (1998, 2001). | the Ramsey rule; present values; one policy; δ as hazard; declining rates |
| 7 | `Longterm` | Greaves and MacAskill (2021); Bostrom (2002); Ord (2020); Thorstad (2023); Greaves (2016); Tarsney (2023). | Parfit's three outcomes; the value of a point of risk |
| 8 | `Fanaticism` | Bostrom (2009); Beckstead and Thomas; Wilkinson (2022); Monton (2019). | a chain of long shots under three rules |
| 9 | `Infinite` | Diamond (1965); Basu and Mitra (2003); Svensson (1980); Zame (2007); Bostrom (2011); Askell (2018). | catching up; the Basu–Mitra construction |
| 10 | `Effective` | Singer (1972, 1975, 2015); MacAskill (2015); Ord (2013); Srinivasan (2015); Gabriel (2017); Crary (2023). | a heavy-tailed portfolio; expected moral weights |
| 11 | `Prices` | Schelling (1968); Jonsen (1986); Harris (1987); Williams (1997); Anderson (1993). | a VSL; two regulations; three weightings; VSL transfer |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

Welfare levels are on a scale with 0 a life just worth living. The variable-value view multiplies the average by
50 (1 − e^(−N/50)); the prioritarian view sums 10 (1 − e^(−w/10)). The Arrhenius search runs over populations of one or
two groups, of 1 to 20 people, at levels −4 to 10, with the repugnant conclusion tested by powers of ten up to two
million lives. Meacham's view is simplified to a one-to-one matching by place. The cost-effectiveness portfolio, the
moral weights and the three patients are toys; the existential-risk model values each century survived at one.

## Problems (solutions in the notes)

1. Show that the average view calls a mere addition worse exactly when the added lives are below the average.
2. Show that every critical-level view with c > 0 implies the sadistic conclusion.
3. Derive the Ramsey rule for u(c) = log c, and say what η is. (η = 1.)
4. With constant risk r after this century, show that halving this century's risk r is worth half a century, whatever r.
5. Find two streams that the catching-up criterion leaves unranked.
6. A rule costs $90 million and prevents 7 expected deaths: find its break-even VSL. ($12.86 million.)
