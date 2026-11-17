# Philosophy, Built — Part 19: Life

Part 19 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of biology.
Paley's watch and Hume's objection; Darwin's one long argument as a consilience; the eye's clock (Nilsson and Pelger:
1829 one-percent steps, about 364,000 generations); design against selection as likelihoods (Sober), and why design
predicts nothing until the designer is specified. Lewontin's recipe; the breeder's equation with and without heredity
(simulated: response 0, 0.48 and 0.83 per generation against h²S); Sober's selection *of* and selection *for*;
random drift (24 neutral populations; a single mutant's fixation against Kimura's formula, 40,000 runs per case) and
the statisticalist–causalist debate. Fitness as a propensity; the Price equation derived and checked on 500 birds
(selection +0.449, transmission −0.102, to 10⁻¹⁵); Fisher's fundamental theorem as its special case, with the variance
selection uses up. Hawks and doves under replicator dynamics (p* = V/C = 2/3), evolutionarily stable strategies,
rock–paper–scissors on the simplex and Sinervo's lizards; Lewis–Skyrms signalling games learned by urn reinforcement
(94% of runs reach a signalling system, split evenly between the two conventions). Kin selection: Hamilton's rule
from the Price equation, simulated for siblings, half-siblings and cousins; relatedness computed exactly by
enumerating Mendel's lotteries (haplodiploid sisters r = 3/4, sister to brother 1/4; Trivers and Hare). Levels of
selection: a Simpson reversal between two groups, the multilevel Price decomposition (+0.03 between, −0.013 within),
the sixty-year debate, and the Wall's nineteenth brick. Dawkins and Hull; the spandrels; Godfrey-Smith's three
adaptationisms; developmental systems and niche construction. Function: Aristotle to Kant to Mayr; Wright, Millikan
and Cummins; Swampman's heart as a Price List. Species: twenty-two concepts, the greenish warbler's ring, cladistic
parsimony on eight animals and eight characters (birds sit with lizards), and kinds after all (Boyd, Okasha,
pluralism). Information: the genetic code counted (entropy 4.22 bits, 24% of point mutations silent), Maynard Smith
against Godfrey-Smith, and the parity thesis in bits. Cooperation: the prisoner's dilemma, a round-robin tournament,
the shadow of the future (TFT resists ALLD iff w > 1/2; tipping point 1/5 at w = 3/4), and Nowak's five rules. What is
life: Schrödinger, entropy budgets for a body and a planet, five definitions against seven cases, and the problem of
one example. Artificial life: von Neumann's constructor, Conway's glider, Lenia's equation, and a creature the
Reasoner found itself and films on screen (mass 430 → 47.3, steady to 0.7%, gliding at 0.47 cells per step).

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/evo.py`, tested in
`tests/philosophy/test_evo.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy19.compute       # every computed item (under a minute; .cache/philosophy19)
python tools/build.py philosophy19 -q l                # 480p preview
python tools/build.py philosophy19                     # 1080p30 -> renders/philosophy19.mp4
python tools/qa_scene.py philosophy19 Alife            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Dobzhansky (1973); Paley and Darwin; the questions; the plan. | — |
| 1 | `Design` | Paley (1802); Hume (1779); Darwin (1859); Whewell; Nilsson and Pelger (1994); Sober (likelihoods). | the eye's generations; likelihood ratios |
| 2 | `Recipe` | Lewontin (1970); the breeder's equation; Sober's sieve (1984); Kimura (1968); Beatty (1984); Walsh, Lewens and Ariew; Matthen and Ariew; Millstein; Reisman and Forber. | truncation selection at three heritabilities; neutral drift; fixation against Kimura |
| 3 | `Fitness` | the tautology objection; Popper; Mills and Beatty (1979); Price (1970); Fisher (1930); Price (1972); Ewens (1989). | the Price terms on 500 birds; mean and variance of fitness under selection |
| 4 | `Games` | Maynard Smith and Price (1973); Taylor and Jonker (1978); Sinervo and Lively (1996); Lewis (1969); Skyrms (2010). | hawk–dove trajectories; ESS margins; three RPS flows; signalling learning curves |
| 5 | `Kin` | Darwin's difficulty; Haldane; Hamilton (1964); Trivers and Hare (1976). | the Price covariance; four kin simulations; exact relatedness |
| 6 | `Levels` | Simpson's reversal; the multilevel Price equation; Wynne-Edwards (1962); Williams (1966); Sober and Wilson (1998); Nowak, Tarnita and Wilson (2010); Abbot et al. (2011); Okasha (2006); **the Wall's nineteenth brick**. | between- and within-group terms |
| 7 | `Genes` | Dawkins (1976, 1982); Hull (1980); Gould and Lewontin (1979); Gould and Vrba (1982); Godfrey-Smith (2001); Parker; Oyama (1985); Griffiths and Gray (1994). | — |
| 8 | `Function` | Aristotle; Bacon; Kant (1790); Mayr (1974); Wright (1973); Millikan (1984); Cummins (1975); Swampman as a **Price List**; Bigelow and Pargetter (1987). | the Swampman conflict and its exits |
| 9 | `Species` | Mayr (1942); Mayden (1997); Ghiselin (1974); Hull; Irwin et al. (2001); Hennig; Fitch; Boyd (1991); Okasha (2002); Kitcher (1984); Ereshefsky. | Fitch parsimony on three trees; where each character arises |
| 10 | `Information` | the genetic code; Freeland and Hurst (1998); Shannon; Maynard Smith (2000); Millikan; Shea; Godfrey-Smith; Griffiths and Gray. | degeneracy, entropy, silent mutations; mutual information under three backgrounds |
| 11 | `Cooperation` | the prisoner's dilemma; Axelrod (1980, 1984); Axelrod and Hamilton (1981); Trivers (1971); Wilkinson (1984); Nowak (2006). | a six-strategy round robin; TFT against ALLD over a long game |
| 12 | `Life` | Schrödinger (1944); Prigogine; Penrose; Maturana and Varela; Joyce (1994); Cleland (2012); Machery (2012); Bedau (1996). | entropy budgets; five definitions against seven cases |
| 13 | `Alife` | von Neumann (1966); Conway (1970); Berlekamp, Conway and Guy (1982); Beer (2004); Chan (2019); Langton (1987); Ray (1991); Lenski et al. (2003); Pattee (1989); Sober (1991). | Conway's glider; a Lenia creature, filmed; its mass over 1500 steps |
| 14 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. Derive the Price equation $\bar w \, \Delta \bar z = \mathrm{Cov}(w, z) + \mathrm{E}(w \, \Delta z)$ for two types with no mutation.

   *Solution.* Let type $i$ have frequency $q_i$, trait value $z_i$ and fitness $w_i$ (offspring per individual), with $\bar w = \sum_i q_i w_i$. Next generation, type $i$ has frequency $q_i' = q_i w_i/\bar w$, and its offspring's trait is $z_i' = z_i + \Delta z_i$. So $\bar z' = \sum_i q_i w_i (z_i + \Delta z_i)/\bar w$, and $\bar w\,\bar z' = \sum_i q_i w_i z_i + \sum_i q_i w_i \Delta z_i$. Subtract $\bar w \bar z$ and note $\sum_i q_i w_i z_i - \bar w \bar z = \mathrm{Cov}(w, z)$: $\bar w\,\Delta\bar z = \mathrm{Cov}(w, z) + \mathrm{E}(w\,\Delta z)$. With faithful transmission and no mutation, $\Delta z_i = 0$ and only the covariance, selection, is left.

2. In hawk–dove with $V = 4$, $C = 6$, find the mixed ESS, and show that it resists invasion by pure hawks.

   *Solution.* With hawk share $p$, a hawk earns $p(V - C)/2 + (1 - p)V$ and a dove $(1 - p)V/2$. They are equal when $p = V/C = 2/3$. Against a population at $p = 2/3$ a pure hawk earns exactly what the residents earn, so the second ESS condition decides: the residents must do better against the invader than the invader does against itself. Residents against a hawk earn $\tfrac23 \cdot \tfrac{V - C}{2} + \tfrac13 \cdot 0 = -\tfrac23$; a hawk against a hawk earns $(V - C)/2 = -1$. Since $-\tfrac23 > -1$, the hawks cannot spread.

3. Show that with $r = 1/8$ and $c = 1$, altruism spreads only if $b > 8$. Which relative has $r = 1/8$?

   *Solution.* Hamilton's rule says an altruistic act spreads when $rb > c$. With $r = 1/8$ and $c = 1$ that is $b/8 > 1$, so $b > 8$. First cousins are related by $r = 1/8$: they share a pair of grandparents, and a gene passes from you to a grandparent and back down to a cousin with probability $(1/2)^3$ through each grandparent, $2 \times 1/16$. Hence Haldane's quip about laying down his life for eight cousins.

4. Give two groups in which altruists lose within each group yet rise overall. Which Price term is positive?

   *Solution.* Let fitness be $1 + 5f$ for selfish individuals and $5f$ for altruists, where $f$ is the share of altruists in their group (benefit $b = 5$, cost $c = 1$). Group A has 80 altruists and 20 selfish, group B 20 and 80. Within A the altruists fall from 80% to 76%, within B from 20% to 11%: they lose in each group. But group A, full of altruists, has far more offspring, and overall the altruists rise from 50% to 57%. In the multilevel Price equation the covariance between group fitness and group altruism is positive; the within-group term is negative and smaller.

5. A codon mutates at one letter. Why are third-position changes most often silent?

   *Solution.* The genetic code is redundant mostly in the third position. Many amino acids are coded by all four codons that share the first two letters (alanine is GCU, GCC, GCA and GCG), and many others by pairs that differ only between U and C, or A and G, in the third. Crick's wobble hypothesis explains this: the third base pairs loosely with the transfer RNA's anticodon. So a change at the third letter usually leaves the amino acid, and the protein, unchanged, while a change at the first or second almost always alters it.

6. Check by hand that the glider returns to its shape after four steps, shifted by $(1, 1)$.

   *Solution.* Write the glider's live cells as (row, column): $(0,1), (1,2), (2,0), (2,1), (2,2)$. The rules: a live cell with two or three live neighbours survives, a dead cell with exactly three is born, every other cell is dead next step. Counting neighbours by hand: generation 1 is $(1,0), (1,2), (2,1), (2,2), (3,1)$; generation 2 is $(1,2), (2,0), (2,2), (3,1), (3,2)$; generation 3 is $(1,1), (2,2), (2,3), (3,1), (3,2)$; generation 4 is $(1,2), (2,3), (3,1), (3,2), (3,3)$, which is the starting shape with one added to every row and every column. Every phase has five cells, and the shape recurs every four steps, one cell further along the diagonal.

## Sources

Texts: Sober, *The Nature of Selection* (1984) and *Philosophy of Biology* (1993; 2nd ed. 2000); Okasha, *Evolution
and the Levels of Selection* (2006); Godfrey-Smith, *Darwinian Populations and Natural Selection* (2009) and
*Philosophy of Biology* (2014); Sterelny and Griffiths, *Sex and Death* (1999); Maynard Smith, *Evolution and the
Theory of Games* (1982); Dawkins, *The Selfish Gene* (1976) and *The Extended Phenotype* (1982); Sober and Wilson,
*Unto Others* (1998); Skyrms, *Signals* (2010); Axelrod, *The Evolution of Cooperation* (1984); Nowak, *Evolutionary
Dynamics* (2006); Schrödinger, *What Is Life?* (1944); Bedau and Cleland (eds.), *The Nature of Life* (2010); von
Neumann, *Theory of Self-Reproducing Automata* (ed. Burks, 1966).

Papers: Hamilton (1964); Lewontin (1970); Price (1970, 1972); Trivers (1971); Maynard Smith and Price (1973); Wright
(1973); Ghiselin (1974); Cummins (1975); Trivers and Hare (1976); Taylor and Jonker (1978); Mills and Beatty (1979);
Gould and Lewontin (1979); Hull (1980); Axelrod and Hamilton (1981); Beatty (1984); Millikan (1984); Bigelow and
Pargetter (1987); Ewens (1989); Pattee (1989); Boyd (1991); Ray (1991); Sober (1991); Nilsson and Pelger (1994);
Griffiths and Gray (1994); Joyce (1994); Sinervo and Lively (1996); Freeland and Hurst (1998); Maynard Smith (2000);
Godfrey-Smith (2001); Irwin et al. (2001); Walsh, Lewens and Ariew (2002); Matthen and Ariew (2002); Millstein (2002);
Okasha (2002); Lenski et al. (2003); Beer (2004); Reisman and Forber (2005); Nowak (2006); Nowak, Tarnita and Wilson
(2010); Abbot et al. (2011); Cleland (2012); Machery (2012); Chan (2019).
