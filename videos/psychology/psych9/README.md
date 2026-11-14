# Psychology, Built: Part 9, Genes and Evolution

In February 1979 two men met in Ohio for the first time since they were a few weeks old. They were identical
twins, adopted by different families, and they were thirty-nine. As the newspapers told it, both were called Jim,
both had married a Linda and then a Betty, and each had owned a dog called Toy. As evidence the story is worth
almost nothing: nobody wrote down beforehand what would be compared, and two strangers compared on two hundred
things will share about ten of them. The design behind the story is another matter. Identical twins raised in
different homes share their genes and not their home, and a psychologist in Minnesota spent the next twenty years
measuring pairs like them on measures fixed in advance.

This part asks how much of who a person is was inherited, and, harder, what that question means. The route: why a
family tree cannot separate genes from a home; how many small genes add up to a bell curve, and the bookkeeping
of variance that Fisher introduced; the twin design, its four-line formula and its path diagram; the same design
on the Pool, where the truth is planted, first working and then failing as each of its four assumptions is
switched off; six traits whose heritability the viewer guesses; what heritability is not (not fixedness, not
about groups, not about a person, not a constant); the three laws of behaviour genetics and the puzzle of the
shared home; the decade of candidate genes and why its findings were not there; genome-wide association, a
million tests at once; what a polygenic score can say about groups and about one person, and why it is smaller
inside families; evolution as a source of hypotheses and of stories. The practice chapter does the arithmetic of
consumer scores and embryo selection; the frontier is the family itself, and whose genomes have been studied.

## Where the numbers come from

| What | Source |
|---|---|
| The "Jim twins" (reunited 1979 at 39; the listed coincidences); about 70% of IQ variance going with genes in twins reared apart | Bouchard et al. (1990), from summaries and press accounts; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| *Hereditary Genius* (1869), the twin questionnaire (1875), "eugenics" coined (1883) | Galton, from histories of the twin method |
| Many factors of small effect give continuous variation (1918) | Fisher (1918), from histories |
| 111 studies of intelligence-test scores: identical twins .86, fraternal twins .60 | Bouchard and McGue (1981), from the abstract; the .60 is an open check |
| 17,804 traits, 14,558,903 twin pairs, mean heritability 49%, 69% of traits fitting an additive model | Polderman et al. (2015), from the abstract |
| The three laws, and the fourth | Turkheimer (2000); Chabris et al. (2015) |
| Among poor families the shared home took 60% of the differences in children's IQ and genes almost none | Turkheimer et al. (2003), from the abstract |
| Heritability of general cognitive ability: 41%, 55%, 66% at 9, 12 and 17 | Haworth et al. (2010), from the abstract |
| Height gained in a century: 20.2 cm (South Korean women), 16.5 cm (Iranian men) | NCD-RisC (2016), from the abstract |
| Six twin heritabilities (schooling .40, personality .47, cognitive ability at 17 .66, ADHD .74, schizophrenia .81) | Branigan et al. (2013); Vukasović and Bratko (2015); Haworth et al. (2010); Faraone and Larsson (2019); Sullivan et al. (2003) |
| The serotonin-transporter interaction (2003) and its pooled test (2009: 14 studies, more than 14,000 people) | Caspi et al. (2003); Risch et al. (2009) |
| 12 variants for intelligence: 1 of 32 tests significant, 10 to 15 expected | Chabris et al. (2012), from the abstract |
| 18 candidate genes for depression, samples of 62,138 to 443,264, none supported | Border et al. (2019), from the abstract |
| Schooling: 126,559 people and 3 positions (0.02% each, about a month a copy); 1.1 million and 1,271; 3 million and 3,952; scores predicting 11–13% and 12–16%; effects about 40% smaller within families; 7–10% for cognitive performance | Rietveld et al. (2013); Lee et al. (2018); Okbay et al. (2022), from the abstracts |
| Non-transmitted alleles have 29.9% of the transmitted alleles' effect on schooling | Kong et al. (2018), from the abstract |
| 178,086 siblings; smaller within-family estimates for schooling, cognition, height, depressive symptoms, smoking | Howe et al. (2022), from the abstract |
| Height: all common variants reach about 45% (40% for the 12,111 found); twins about 80% | Yengo et al. (2022), from the abstract; the twin figure is the textbook one |
| Scores about 4.5 times less accurate in African and about 2 times in East Asian ancestry; about 79% of participants European | Martin et al. (2019), from summaries and the preprint |
| Choosing the best of ten embryos: about 2.5 IQ points | Karavani et al. (2019), from summaries |
| 10,047 people, 37 cultures; 36 of 37 and 37 of 37 | Buss (1989), from summaries |
| Fewer methyl tags on IGF2 six decades after the Dutch famine (60 people); maternal care and methylation in rats | Heijmans et al. (2008); Weaver et al. (2004), from the abstracts |
| Betty the crow (2002), and wild crows' routine tool bending (2016) | Weir et al. (2002), from accounts of both studies |

Everything else is computed by `compute.py` with Psyche's `genes` module. The twin registry is simulated under
the infinitesimal model with planted shares of 0.5 (additive genes), 0.2 (shared home) and 0.3 (the rest); "the
Pool's twin registry" in the film means these simulated families. The example study in chapter 4 is chosen by
rule (of 101 studies of 1,000 + 1,000 pairs, the one with the median estimate) and its intervals are bootstrap
percentiles. The chances in the hook's coincidence count (200 comparisons, 1 in 20 each) are an illustration and
are said to be. The miniature genome has 2,500 unlinked positions, 500 of them causal, and a trait with a
heritability of 0.5; its significance line is 0.05 / 2,500. The embryo calculation uses the top of the published
range for cognitive performance (10%) and the published within-family shrinkage (40%).

## Built in this part

* `explainer/psychology/psyche/genes.py`: the sum of L loci; families under the infinitesimal model with switches
  for unequal environments, assortative mating, dominance and gene-environment correlation; Falconer's estimates
  and their standard error; a maximum-likelihood ACE fit; adoption and parent-offspring designs; Lewontin's two
  fields; power for one variant; a flexibly analysed null candidate gene; genotypes, a polygenic trait, a
  genome-wide scan and polygenic scores; the sibling design with genetic nurture and stratification; the
  expected gain from choosing among embryos; coincidences among strangers. Tested in
  `tests/psychology/test_genes.py` against closed forms and the module's own planted answers.
* The Ledger gains three rows and the Archive twenty-three datasets.
* The series' first path diagram (the ACE model); the notation returns in Part 44.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| On almost every psychological trait, identical twins are more alike than fraternal twins | Bouchard and McGue 1981 | replicated |
| Common variants in a few named genes explain who becomes depressed after stress, or who scores higher on tests | Caspi and colleagues 2003 | failed |
| A score added up from many common gene variants predicts how far a person goes in school | Rietveld and colleagues 2013 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the Jim twins and the Minnesota
study (an anecdote and the study it began), Galton and Fisher (history and theory), Turkheimer's laws and the
table of heritabilities (summaries whose evidence is the first row), the heritability that depends on wealth and
on age (entered with intelligence in Part 32), the century of height, genetic nurture, the within-sibship scan,
height's variants and the portability of scores (methods results at the frontier), the embryo simulation, mate
preferences in 37 cultures (entered in Part 37), the famine and methylation, and Betty the crow.

## Build it

```bash
python -m videos.psychology.psych9.compute            # every number (about half a minute), into .cache/psych9/
python tools/qa_scene.py psych9 PoolTest              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych9 -q l   # the whole part, silent preview
python tools/build.py psych9                          # 1080p30 with narration
python tools/qa_scene.py psych9 PoolTest --lang zh    # the Chinese edition of one chapter
python tools/make.py psych9                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 9                    # the lab: twins, a broken assumption, a genome-wide scan
python tools/check_ledger.py psych9                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # Psyche's genes module, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two men called Jim | The reunion; coincidences among strangers; the design behind the anecdote; objectives |
| 1 | Nature and nurture | Galton's families; two worlds with the same parent-child correlation, and what adoption shows; eugenics named |
| 2 | From peas to bell curves | Mendel against the bell curve; 1, 2, 5 and 50 genes; a score in three parts; regression to the mean and its slope |
| 3 | The logic of twins | Two kinds of twins; two clouds of points; Falconer's four lines; the path diagram; the classic data |
| 4 | On the Pool: when the design is right, and when it is wrong | 2,000 studies at each size; one study fitted by maximum likelihood; four assumptions switched off; adoption and twins apart as checks |
| 5 | On you: guess the heritability | Six traits, guessed and then revealed |
| 6 | What heritability is not | Height in a century; seed in two fields; the rectangle; heritability against the spread of environments, wealth and age |
| 7 | Three laws and a puzzle | Turkheimer's laws and fifty years of twin studies; the shared home that counts for little; what is in the remainder |
| 8 | The candidate-gene decade | The serotonin transporter; what a thousand people can detect; a null gene analysed 18 ways; the tests of 2009, 2012 and 2019 |
| 9 | A million tests | One regression a position and the line at 5 × 10⁻⁸; a miniature genome at three sample sizes; the real history |
| 10 | What a polygenic score can say | Building and testing a score; groups against one person; smaller within families; missing heritability; epigenetics |
| 11 | Evolution as a source of hypotheses | The second "why"; 37 cultures; just-so stories and what a testable claim needs; a crow and a wire |
| 12 | The Ledger | Twin heritability, candidate genes, and the score for schooling |
| 13 | In practice: what a genetic test can deliver | Counselling for single genes; a consumer score; choosing among embryos; six questions |
| 14 | Frontier: inside the family | Stratification; Mendel's lottery between siblings; whose genomes; four open questions |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 10 |

## Sources

**Books.** V. S. Knopik, J. M. Neiderhiser, J. C. DeFries and R. Plomin, *Behavioral Genetics* (7th ed., 2017).
K. P. Harden, *The Genetic Lottery* (2021). D. S. Falconer and T. F. C. Mackay, *Introduction to Quantitative
Genetics* (4th ed., 1996). D. J. Kevles, *In the Name of Eugenics* (1985).

**Papers.**
- T. J. Bouchard, D. T. Lykken, M. McGue, N. L. Segal and A. Tellegen, "Sources of human psychological
  differences: the Minnesota Study of Twins Reared Apart", *Science* 250 (1990) 223–228.
- F. Galton, "The history of twins, as a criterion of the relative powers of nature and nurture", *Fraser's
  Magazine* 12 (1875) 566–576; *Hereditary Genius* (1869).
- R. A. Fisher, "The correlation between relatives on the supposition of Mendelian inheritance", *Transactions
  of the Royal Society of Edinburgh* 52 (1918) 399–433.
- T. J. Bouchard and M. McGue, "Familial studies of intelligence: a review", *Science* 212 (1981) 1055–1059.
- T. J. C. Polderman et al., "Meta-analysis of the heritability of human traits based on fifty years of twin
  studies", *Nature Genetics* 47 (2015) 702–709.
- E. Turkheimer, "Three laws of behavior genetics and what they mean", *Current Directions in Psychological
  Science* 9 (2000) 160–164. C. F. Chabris, J. J. Lee, D. Cesarini, D. J. Benjamin and D. I. Laibson, "The fourth
  law of behavior genetics", *Current Directions in Psychological Science* 24 (2015) 304–312.
- E. Turkheimer, A. Haley, M. Waldron, B. D'Onofrio and I. I. Gottesman, "Socioeconomic status modifies
  heritability of IQ in young children", *Psychological Science* 14 (2003) 623–628.
- C. M. A. Haworth et al., "The heritability of general cognitive ability increases linearly from childhood to
  young adulthood", *Molecular Psychiatry* 15 (2010) 1112–1120.
- NCD Risk Factor Collaboration, "A century of trends in adult human height", *eLife* 5 (2016) e13410.
- P. F. Sullivan, K. S. Kendler and M. C. Neale, "Schizophrenia as a complex trait", *Archives of General
  Psychiatry* 60 (2003) 1187–1192. S. V. Faraone and H. Larsson, "Genetics of attention deficit hyperactivity
  disorder", *Molecular Psychiatry* 24 (2019) 562–575. A. R. Branigan, K. J. McCallum and J. Freese, "Variation
  in the heritability of educational attainment", *Social Forces* 92 (2013) 109–140. T. Vukasović and D. Bratko,
  "Heritability of personality", *Psychological Bulletin* 141 (2015) 769–785.
- A. Caspi et al., "Influence of life stress on depression: moderation by a polymorphism in the 5-HTT gene",
  *Science* 301 (2003) 386–389. N. Risch et al., "Interaction between the serotonin transporter gene (5-HTTLPR),
  stressful life events, and risk of depression", *JAMA* 301 (2009) 2462–2471.
- C. F. Chabris et al., "Most reported genetic associations with general intelligence are probably false
  positives", *Psychological Science* 23 (2012) 1314–1323.
- R. Border et al., "No support for historical candidate gene or candidate gene-by-interaction hypotheses for
  major depression across multiple large samples", *American Journal of Psychiatry* 176 (2019) 376–387.
- C. A. Rietveld et al., "GWAS of 126,559 individuals identifies genetic variants associated with educational
  attainment", *Science* 340 (2013) 1467–1471. J. J. Lee et al., "Gene discovery and polygenic prediction from a
  genome-wide association study of educational attainment in 1.1 million individuals", *Nature Genetics* 50
  (2018) 1112–1121. A. Okbay et al., "Polygenic prediction of educational attainment within and between families
  from genome-wide association analyses in 3 million individuals", *Nature Genetics* 54 (2022) 437–449.
- A. Kong et al., "The nature of nurture: effects of parental genotypes", *Science* 359 (2018) 424–428.
- L. J. Howe et al., "Within-sibship genome-wide association analyses decrease bias in estimates of direct
  genetic effects", *Nature Genetics* 54 (2022) 581–592.
- L. Yengo et al., "A saturated map of common genetic variants associated with human height", *Nature* 610
  (2022) 704–712.
- A. R. Martin et al., "Clinical use of current polygenic risk scores may exacerbate health disparities",
  *Nature Genetics* 51 (2019) 584–591.
- E. Karavani et al., "Screening human embryos for polygenic traits has limited utility", *Cell* 179 (2019)
  1424–1435.
- D. M. Buss, "Sex differences in human mate preferences: evolutionary hypotheses tested in 37 cultures",
  *Behavioral and Brain Sciences* 12 (1989) 1–49. S. J. Gould and R. C. Lewontin, "The spandrels of San Marco and
  the Panglossian paradigm", *Proceedings of the Royal Society B* 205 (1979) 581–598.
- B. T. Heijmans et al., "Persistent epigenetic differences associated with prenatal exposure to famine in
  humans", *PNAS* 105 (2008) 17046–17049. I. C. G. Weaver et al., "Epigenetic programming by maternal behavior",
  *Nature Neuroscience* 7 (2004) 847–854.
- A. A. S. Weir, J. Chappell and A. Kacelnik, "Shaping of hooks in New Caledonian crows", *Science* 297 (2002)
  981.

## Problems and solutions

**1.** *In a study of 250 identical and 250 fraternal pairs the correlations are .62 and .40. Give Falconer's
three shares. The standard error of each correlation is about (1 − r²)/√n: can this study tell the shared home's
share from zero?*

h² = 2(.62 − .40) = .44; c² = 2(.40) − .62 = .18; e² = 1 − .62 = .38. The standard errors of the two
correlations are (1 − .3844)/√250 = .039 and (1 − .16)/√250 = .053. The shared home's share is 2 r_F − r_I, so
its standard error is √(4 × .053² + .039²) = .113, and .18 is 1.6 standard errors from zero: no. The
heritability's standard error is 2√(.039² + .053²) = .13, so the study says "somewhere between about .2 and .7".
A twin study of this size settles that the trait is heritable and very little else.

**2.** *A trait has a² = 0.6 and no shared home, but spouses resemble each other, so fraternal twins share 0.6 of
A, not 0.5. What do the two twin correlations become, and what does Falconer's formula report?*

Identical twins: r_I = a² = .60. Fraternal twins: r_F = .6 × .6 = .36. The formula reports h² = 2(.60 − .36) =
.48 and c² = 2(.36) − .60 = .12. Twelve points of genetic variance have been filed under "shared home", because
the formula's one half was too small. Assortative mating makes twin studies understate genes and invent a home
effect; the equal-environments failure does the opposite; a real study has both.

**3.** *In each of two fields the heritability of plant height is 0.9 and the variance is 1; the fields' means
differ by 3. What is the heritability in the two fields pooled, half from each? What does that say about pooling
populations?*

The pooled variance is the variance within fields plus the variance between them: 1 + (3/2)² = 3.25. The genetic
variance is still 0.9, so the pooled heritability is 0.9/3.25 = .28. No gene changed. Heritability fell from .9
to .28 because an environmental difference was added to the population being described. A heritability belongs
to a population in its range of environments, and the gap between the fields, which is entirely environmental,
sits inside a population whose "heritability" could be quoted to argue the opposite.

**4.** *A variant explains 0.02% of the variance of a trait. How many people give an 80% chance of detecting it
at p < .05? At p < 5 × 10⁻⁸? What is the chance with 300 people?*

For a correlation of √r², n ≈ (z_{α/2} + z_power)² (1 − r²)/r². With r² = .0002: at .05, (1.960 + 0.842)² ×
.9998/.0002 = 39,237. At 5 × 10⁻⁸ the critical z is 5.451, so (5.451 + 0.842)²/.0002 = 197,966. With 300 people
the test statistic has mean √(300 × .0002) = 0.245, and the chance of passing ±1.96 is Φ(0.245 − 1.96) +
Φ(−0.245 − 1.96) = .043 + .014 = 5.7%: barely more than the 5% a variant with no effect at all would give.
`genes.n_for_r2` and `genes.power_for_r2` do this arithmetic.

**5.** *A genome-wide study makes 10⁶ independent tests of variants that do nothing. How many pass at p < .05? At
p < 5 × 10⁻⁸? A score predicts 14% of a trait: what is the chance that someone in its top tenth is above the
median?*

At .05: 50,000 false hits. At 5 × 10⁻⁸: 0.05, so one such study in twenty has a single false hit. For the score,
the correlation is √.14 = .374. For a person whose score is z standard deviations up, the trait is normal with
mean .374 z and standard deviation √.86 = .927, so the chance of being above the median is Φ(.374 z/.927). In the
top tenth z averages 1.75, giving about Φ(.71) = .76; the film's simulation gives 76%. One in four of the people
the score ranks highest is below average.

**6.** *With `explainer.psychology.psyche.genes`: run `twin_study` with `mz_extra` from 0 to 0.6 and plot
Falconer's h². Then use `sibling_design` to find the `nurture` that makes the within-family effect 40% smaller
than the population effect.*

```python
import numpy as np
from explainer.psychology.psyche import genes as G
for m in (0.0, 0.2, 0.4, 0.6):
    d = G.twin_study(100_000, 100_000, 0.5, 0.2, 0.3, mz_extra=m, rng=np.random.default_rng(1))
    print(m, round(G.falconer(d.r_mz, d.r_dz)["h2"], 2))        # 0.5, 0.62, 0.74, 0.86
out = G.sibling_design(400_000, np.random.default_rng(2), direct=0.3, nurture=0.4)
print(out["population"], out["within"], out["ratio"])            # 0.50, 0.30, 0.60
```

The estimate is a² + 2 m e²: each tenth of the unshared variance that identical twins secretly share adds 0.06
to the "heritability". In the sibling design the population slope is direct + nurture/2 and the within-family
slope is direct, so a ratio of 0.6 needs nurture = (4/3) × direct.

**7.** ★ *Design the study that would tell a direct effect of a child's genes from an effect of the home their
parents' genes made, and say what result would count against genetic nurture.*

Three designs attack it from different sides, and the answer is their agreement. (a) Trios: genotype both parents
and the child, and split each parent's alleles into those passed on and those not. The alleles not passed on can
act only through the parents; a score built from them should predict the child's outcome if genetic nurture is
real, after controls for ancestry. (b) Adoption: the adoptive parents' scores cannot reach the child through
inheritance at all; if they predict the adoptee's schooling, that is nurture; if only the birth parents' scores
do, it is transmission. (c) Siblings: the difference between two siblings' scores is Mendel's lottery, so the
within-family slope is the direct effect; the gap between it and the population slope bounds everything else
(nurture, stratification, assortative mating together). Against genetic nurture would count: a non-transmitted
score with no association in large samples; adoptive parents' scores that predict nothing; within- and
between-family slopes that agree. Fix the outcome, the score and the analysis in advance, power the study for a
within-family effect a third smaller than the published one, and say beforehand how small an effect you would
call zero.

## Where it comes back

Reasoning about cheats as a test of an evolutionary claim: Part 24. How people understand a risk, the
counsellor's problem: Part 26. Temperament and what parents do: Part 30. Intelligence, its heritability across
wealth and age, and the history of eugenics: Part 32. Personality, where twin and family studies disagree: Part
33. Mate preferences across cultures and the rival accounts: Part 37. The genetics of depression, psychosis and
addiction: Parts 40 and 41. Path diagrams fitted in earnest: Part 44. Psyche's `genes` module supplies the twin
and family simulators those parts use.

## Open checks

Before the narrated master:

* Bouchard et al. (1990) was not read. The number of reared-apart pairs differs between secondary sources and is
  not given in the film; "about seventy percent" is the study's headline as summarized. The Jim twins' details
  (the date, Linda and Betty, the sons' names, the dog) are from popular accounts and are told as "the newspapers
  told it"; sources differ on whether they were separated at three or four weeks, so the film says "a few weeks".
* Galton: that *Hereditary Genius* (1869) surveyed judges, statesmen, scientists and poets is from memory of the
  book's chapters; the twin questionnaire's date (1875) and the coining of "eugenics" (1883) are from histories.
  "Within fifty years it was law in many countries" summarizes sterilization and immigration laws of 1907 to the
  1930s and is told in Part 32.
* The comparison of identical with fraternal twins "first made in the nineteen-twenties" (Merriman, Siemens) is
  from histories found by search; the names are not used in the film.
* Bouchard and McGue (1981): the .86 for identical twins reared together is confirmed by a paper that cites it;
  the .60 for fraternal twins is from memory of the paper's figure. If it is wrong, the shares shown (.52, .34,
  .14) change with it.
* Lewontin's two-fields picture is attributed from memory (1970); the film calls it "a picture due to the
  geneticist Richard Lewontin".
* Height's twin heritability of "about 0.8" in well-fed countries is the textbook figure. Phenylketonuria as a
  single-gene condition prevented by diet is textbook medicine.
* Turkheimer et al. (2003): the film uses the abstract's wording (60% shared environment and genes close to zero
  among impoverished families; the reverse among affluent ones). "Later samples disagree" summarizes mixed
  replications; the meta-analysis usually cited (Tucker-Drob and Bates 2016) was not checked.
* "Adoptive brothers and sisters are by adulthood hardly more alike in personality than strangers" summarizes
  adoption studies from memory (Plomin and Daniels 1987; Loehlin's Texas project); no number is shown.
* Caspi et al. (2003): the cohort's size is not given; "one of the most celebrated findings of its decade" is a
  characterization. Risch et al. (2009): 14 studies and "more than 14,000" people are from a university summary
  (14,250 in the paper, from memory).
* The "chopsticks gene" is the standard teaching example of stratification (Hamer and Sirota 2000, from memory).
* Kong et al. (2018): "in Iceland" follows the authors' affiliation (deCODE); the abstract as retrieved does not
  name the population.
* Martin et al. (2019): the 4.5-fold figure is from a news summary of the paper, the 2-fold figure for East
  Asian ancestry from the preprint's "2- to 5-fold", and 79% European from a truncated excerpt.
* "About as good as published scores get" for a score predicting 10% of cognitive performance refers to Lee et
  al. (2018); later scores should be checked. Karavani et al.'s 2.5 points is for ten embryos, from summaries.
* Buss (1989): counts from secondary summaries; page range from the journal listing.
* Gould and Lewontin (1979) and the phrase "just-so stories" are from memory of the paper.
* Betty the crow: the 2016 field study's reference (Rutz and colleagues, *Royal Society Open Science*) is from
  memory. Octopuses are mentioned without numbers.
* The outro's Mammoth Cave story (Kleitman and a student, 1938, a 28-hour day) is from the syllabus and will be
  verified with Part 10.
