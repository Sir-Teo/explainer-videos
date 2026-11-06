# Philosophy, Built — Part 40: Beauty

Part 40 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*:
aesthetics. Hume's beauty "in the mind which contemplates" (1757), a preview of the dissonance curve and the wallpaper
groups, and four questions. Plato's ladder (*Symposium*), *Republic* X and the *Hippias Major*; Aristotle's mimesis,
catharsis and order; Plotinus, Aquinas, Hutcheson (1725), Burke's sublime (1757); rasa in the *Natyashastra* and
Abhinavagupta. **The Pythagorean comma computed** (3¹²/2¹⁹ = 531441/524288, 23.46 cents) on the spiral of fifths that
does not close; **equal temperament measured** (fifths 1.96 cents off, thirds 13.69 to 15.64); **Pythagorean,
quarter-comma meantone and equal temperament compared** (thirds and wolf fifths); Zhu Zaiyu (1584); other scales.
Beats drawn; **the dissonance curve built** (Plomp and Levelt 1965, in Sethares's form): minima exactly at 6:5, 5:4,
4:3, 3:2, 5:3 and 2:1, and **moving with stretched timbres** (an "octave" of 2.1); Helmholtz (1863), von Békésy, the
critical band, Rameau, McDermott et al. (2010; the Tsimane', 2016), Krumhansl, Meyer, Huron. **All seventeen wallpaper
groups generated from their operations and classified by flowchart** (17 built, 17 distinct names), drawn as a
gallery and with **p4m's mirrors, glides and rotation centres computed**; Fedorov (1891), Pólya, the Alhambra
(Grünbaum 2006), Escher, Weyl, Conway's orbifolds; space groups, Penrose, Shechtman, girih; Gombrich's broken
symmetry. Birkhoff's *Aesthetic Measure* (1933) and Eysenck; Bense, Moles and Berlyne's inverted U; **compression**
(zlib shrinks rule 90 to 42% but cannot touch rule 30) and **compression progress as a toy of Schmidhuber's
interestingness**; Kolmogorov, logical depth, effective complexity; Pollock's fractals and their critics. The golden
ratio and Fibonacci; **a look-elsewhere test** (70% of random eight-length "buildings" contain φ within 3%); Fechner
(1876), McManus, Green, Markowsky; **Vogel's sunflower at the golden angle and near it**; faces (Langlois and
Roggman), Dutton, Komar and Melamid. Hume's standard of taste (Sancho's kinsmen; the true judge), **a panel of critics
simulated as an analogy** (true judges converge to 0.998; a shared prejudice stalls at about 0.62), a **Price List**
for the paradox of taste — **the Wall's fortieth brick**; Levinson's circle, mere exposure (Zajonc; Cutting), blind
tasting (Brochet; Hodgson). Kant's four moments, free play, free and dependent beauty, the antinomy of taste, the
sublime and genius; Schiller, Hegel, Schopenhauer, Nietzsche; Bourdieu and Korsmeyer. What is art? Tolstoy, Bell,
Collingwood, Weitz (1956), Duchamp, Warhol's Brillo boxes, Danto (1964, 1981), Dickie (1974), Levinson (1979), Gaut
(2000), environmental and everyday aesthetics, Sibley (1959), theories of art's value. Forgery (Goodman 1968; van
Meegeren), Dutton, Newman and Bloom, Walton, restoration (Brandi); AI art (the 2022 Colorado prize; the US Copyright
Office, 2023; *Thaler v. Perlmutter*, 2023 and 2025) and aesthetic predictors. Mathematical beauty (Hardy 1940;
Erdős's Book; Zeki et al. 2014) with **Euclid's and the √2 proofs shown**; Xie He's six principles, *yijing*, Wang
Guowei (1908), Cook Ding, Confucius and Xunzi on music, Ji Kang, wabi-sabi, and modern Chinese aesthetics (Cai
Yuanpei, Zhu Guangqian, Zong Baihua, Li Zehou).

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/aesthetics.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_aesthetics.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy40.compute       # every computed item (seconds; .cache/philosophy40)
python tools/build.py philosophy40 -q l                # 480p preview
python tools/build.py philosophy40                     # 1080p30 -> renders/philosophy40.mp4
python tools/qa_scene.py philosophy40 Symmetry         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Hume (1757); a preview; four questions; the plan. | the curve and a wallpaper pattern, previewed |
| 1 | `Greeks` | Plato; Aristotle; Plotinus; Aquinas; Hutcheson; Burke; Bharata; Abhinavagupta. | — |
| 2 | `Harmony` | the Pythagoreans; Kepler; Zhu Zaiyu; Stevin; meantone; scales. | the comma; the spiral of fifths; equal and meantone temperaments |
| 3 | `Roughness` | Helmholtz; Plomp and Levelt; Sethares; von Békésy; Fletcher; Rameau; McDermott et al.; Krumhansl; Meyer; Huron. | beats; the dissonance curve; stretched partials |
| 4 | `Symmetry` | Fedorov; Pólya; Conway; Penrose; Shechtman; Lu and Steinhardt; Grünbaum; Escher; Weyl; Gombrich. | 17 groups generated and classified; p4m's elements |
| 5 | `Order` | Birkhoff; Eysenck; Bense; Moles; Berlyne; Schmidhuber; Kolmogorov; Bennett; Gell-Mann and Lloyd; Taylor; Jones-Smith and Mathur. | compression of five images; compression progress |
| 6 | `Golden` | Fechner; McManus; Green; Markowsky; Vogel; Langlois and Roggman; Rhodes; Dutton; Komar and Melamid. | Fibonacci ratios; the look-elsewhere test; the sunflower |
| 7 | `Hume` | Hume (1757); Levinson; Zajonc; Cutting; Brochet; Hodgson; Sibley; Zangwill; **the Wall's fortieth brick**. | the critics panel (analogy); **the Price List** |
| 8 | `Kant` | Kant (1790); Schiller; Hegel; Schopenhauer; Nietzsche; Bourdieu; Korsmeyer. | — |
| 9 | `Art` | Tolstoy; Bell; Collingwood; Weitz; Duchamp; Warhol; Danto; Dickie; Levinson; Gaut; Hepburn; Carlson; Saito; Sibley; Nussbaum; Lopes. | — |
| 10 | `Authentic` | Goodman; van Meegeren; Dutton; Newman and Bloom; Walton; Brandi; the US Copyright Office; *Thaler v. Perlmutter*; LAION. | — |
| 11 | `East` | Hardy; Erdős; Aigner and Ziegler; Zeki et al.; Xie He; Wang Guowei; Zhuangzi; Confucius; Xunzi; Ji Kang; Cai Yuanpei; Zhu Guangqian; Zong Baihua; Li Zehou. | — |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The dissonance model is Sethares's parametrization of Plomp and Levelt's curve, with six partials of amplitude 0.88^k
at middle C; "stretched" partials sit at k^log2(2.1). The wallpaper groups are built from standard coset
representatives on oblique, rectangular, centred, square and hexagonal lattices; p3m1 and p31m are built the same way
with mirrors in two orientations and named by the classifier. The compression-progress observer predicts each cell
from the three above it with Laplace-smoothed counts. The golden-ratio test draws eight lengths uniformly from 1 to
10, 20,000 times (seed 1876). The critics panel is labelled an analogy: thirty works, novices (noise 1.5,
idiosyncrasy 1.0), true judges (0.4, 0.3), prejudiced judges with a shared bias of weight 1.2, 400 trials per panel
size.

## Problems (solutions in the notes)

1. Show that no power of 3/2 equals a power of 2.
2. How many cents is the syntonic comma 81/80?
3. Explain why two harmonic tones at ratio 3:2 share every second partial of the lower tone.
4. Which wallpaper groups have no mirrors and no glides?
5. Why does averaging remove a critic's noise but not a shared prejudice?
6. State the paradox of taste as an inconsistent triad, and say which claim Kant denies.
