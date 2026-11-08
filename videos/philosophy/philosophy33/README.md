# Philosophy, Built — Part 33: Rational Choice

Part 33 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the first part of Act VII,
*Value*: what it is to choose well, from preferences to Newcomb's problem. Bernoulli (1738) and the theory
of rational choice. Preferences: completeness and transitivity; the small-improvement argument against completeness
(de Sousa 1974; Chang 2002; Aumann 1962); a money pump, built (15 trades, 15 cents, back where it started); ordinal
utility; revealed preference tested on data (Samuelson 1938; Afriat 1967): a shopper whose two weeks violate GARP, with
Afriat's efficiency index 0.917. The St Petersburg game (1713, 1738) played a million times (averages 6.4 after ten,
12.51 after a thousand, 24.64 after a million), Bernoulli's log utility (expected utility 2, worth 4 ducats), Menger
(1934). The von Neumann–Morgenstern theorem (1944): axioms, the construction of u, and parallel indifference lines in
the Marschak–Machina triangle (slope 1.5 for a middle utility of 0.6). Allais (1953): for every one of 201 utilities of
a million, expected utility picks the risky option in both pairs or the safe one in both, never the common 1A and 2B;
the pairs drawn as parallel segments of slope 10, and the fanning-out the common choices need (Machina 1982). Savage
(1954): states, acts, consequences, the sure-thing principle, and Savage's own tickets. Ellsberg (1961): no single
probability for any of the 61 possible urns fits the common choices; maxmin expected utility (Gilboa and Schmeidler
1989) does. Risk-weighted expected utility (Buchak 2013) with r(p) = p²: 1A 0.8 over 1B 0.7861, 2B 0.01 over 2A 0.0097.
Prospect theory (1979, 1992): the value and weighting functions, the fourfold pattern (certainty equivalents 9.98,
76.85, −8.26, −83.12) and the Asian disease problem (1981), whose flip prospect theory predicts (105.9 against 93.55;
−353.15 against −438.53); rank-dependent utility (Quiggin 1982). The Kelly criterion (1956): f* = 2p − 1, the growth
curve, a thousand simulated fortunes at four fractions (median 10^6.4 at f = 0.1, 10^8.6 at the Kelly 0.2, 457 ruined at
0.4, all 1000 ruined at 0.6, where expected wealth is 10^49), Samuelson's objection, Thorp, fractional Kelly and
Shannon. The Pasadena game (Nover and Hájek 2004): the natural order sums to ln 2 = 0.69314, two-to-one to (3/2) ln 2 =
1.03972 (Riemann's rearrangement theorem); weak and relative expectations (Easwaran 2008; Colyvan 2006). Newcomb's
problem (Nozick 1969) at every accuracy (the tie at 0.5005), ten thousand simulated players (one-boxers average
$906,219, two-boxers $102,620; Lewis 1981), and its **Price List** with the PhilPapers 2020 shares (two boxes 39%, one
box 31%). Evidential against causal decision theory (Jeffrey 1965; Gibbard and Harper 1978; Lewis 1981; Joyce 1999):
the smoking lesion (EDT abstains, CDT smokes), Egan's psychopath button (2007; CDT presses, EDT refrains), death in
Damascus and ratifiability, and **the Wall's thirty-third brick**. Policies: Parfit's hitchhiker (1984), the
prisoner's dilemma against a twin (Lewis 1979; cooperation wins evidentially above r = 5/7), functional decision theory
(Yudkowsky and Soares 2017) and its critics (Schwarz 2018; MacAskill 2019). Dynamic choice: Ulysses and the sirens;
naive, sophisticated and resolute choosers (McClennen 1990); hyperbolic against exponential discounting, with a
reversal at nine days (Strotz 1956; Ainslie 1975); Hammond (1988) and Machina (1989). Good's theorem (1967), drawn as a
convex envelope (0.722 against 0.6 for an 80% forecast) and checked on 2000 random problems (569 helped, none hurt);
Buchak's risk-weighted counterexample and the off-switch game (Hadfield-Menell et al. 2017). The two envelopes
(Kraitchik 1953): a proper prior makes switching gain exactly 0 on average; Broome's prior (1995) makes it gain at every
amount, because the expected amount is infinite.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/decision.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_decision.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy33.compute       # every computed item (seconds; .cache/philosophy33)
python tools/build.py philosophy33 -q l                # 480p preview
python tools/build.py philosophy33                     # 1080p30 -> renders/philosophy33.mp4
python tools/qa_scene.py philosophy33 Newcomb          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Bernoulli (1738); four questions; the plan. | — |
| 1 | `Preferences` | completeness, transitivity; de Sousa (1974), Chang (2002), Aumann (1962); Samuelson (1938), Afriat (1967). | a money pump; GARP and the efficiency index |
| 2 | `StPetersburg` | N. and D. Bernoulli (1713, 1738); Menger (1934). | a million games; log utility |
| 3 | `VNM` | von Neumann and Morgenstern (1944); Marschak; Machina. | parallel lines in the triangle |
| 4 | `Allais` | Allais (1953); Kahneman and Tversky (1979); Machina (1982). | 201 utilities; the fanning-out, zoomed |
| 5 | `Savage` | Savage (1954): the sure-thing principle; the tickets. | — |
| 6 | `Ellsberg` | Ellsberg (1961); Gilboa and Schmeidler (1989). | 61 urns; maxmin expected utility |
| 7 | `Risk` | Buchak (2013); Kahneman and Tversky (1979, 1992); Quiggin (1982); Tversky and Kahneman (1981). | risk-weighted utility; the fourfold pattern; the Asian disease |
| 8 | `Kelly` | Kelly (1956); Samuelson; Thorp (1962); Shannon. | the growth curve; 1000 fortunes at four fractions |
| 9 | `Pasadena` | Nover and Hájek (2004); Riemann; Easwaran (2008); Colyvan (2006). | two orders of the same series |
| 10 | `Newcomb` | Nozick (1969); Lewis (1981); **the Price List**. | any accuracy; 10 000 players |
| 11 | `EDTCDT` | Jeffrey (1965); Gibbard and Harper (1978); Lewis (1981); Joyce (1999); Eells (1982); Egan (2007); **the Wall's thirty-third brick**. | the lesion; the button; Damascus |
| 12 | `FDT` | Parfit (1984); Lewis (1979); Yudkowsky and Soares (2017); Schwarz (2018); MacAskill (2019). | acts against policies; the twin's dilemma |
| 13 | `Dynamic` | McClennen (1990); Strotz (1956); Ainslie (1975); Hammond (1988); Machina (1989). | three choosers; a preference reversal |
| 14 | `Good` | Good (1967); Buchak (2010); Hadfield-Menell et al. (2017). | the envelope; 2000 problems; a counterexample |
| 15 | `Envelopes` | Kraitchik (1953); Nalebuff (1989); Broome (1995). | a proper prior; Broome's prior |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The Allais fanning-out is drawn in two zoomed panels at one scale, because the segments 1A–1B and 2A–2B have slope 10
in the triangle: the common choices need indifference lines steeper than that near 1A and flatter near 2A. The
Newcomb survey shares are PhilPapers 2020 target faculty, accept or lean towards (Bourget and Chalmers 2023). The
Asian disease percentages (72% of 152; 78% of 155) are those Tversky and Kahneman report; the prospect values are
computed with their 1992 parameters.

## Problems (solutions in the notes)

1. Show that the money pump needs only strict cyclic preference, not completeness.
2. Prove that g(f) = p log(1+f) + (1−p) log(1−f) is concave, and find where it crosses zero.
3. For which u($1M) does REU with r(p) = p² give the Allais pattern? (About 0.33 to 0.83.)
4. At what accuracy does a two-boxer's average equal a one-boxer's, in the simulation?
5. Draw Good's envelope for two acts, and find a test with value exactly zero.
6. Show that no proper prior makes every amount equally likely to be the smaller envelope.
