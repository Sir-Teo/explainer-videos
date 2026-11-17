# Psychology, Built: Part 7, The Brain

On 13 September 1848 an explosion drove an iron rod through the head of a railway foreman, Phineas Gage. He was
talking within minutes and lived for about twelve more years. What happened to his character afterwards is one of
the most retold stories in psychology, and most of the retelling is not in the record. Behind the story is an old
question: is the mind in one place, or everywhere? For most of history the only way to ask was to wait for an
accident, a stroke or a surgeon's knife, and then see what the person could no longer do.

This part is about that method: what damage has shown, how to read it, and how it misleads. The route: a tour of
the parts, with one line on each; Gall's good idea and bad method, Flourens's pigeons and Lashley's rats, whose
"mass action" is reproduced in a model brain where every job has a place; Broca and Wernicke, two aphasias, and a
diagram that predicted a third; the logic of dissociation, and how one damaged resource with noisy tests fakes a
double dissociation; Penfield's map and the magnification of the visual cortex; the viewer's own blind spot, and
what fills it; the man who could not make new memories and still learned a skill; the brain cut in two, the
interpreter, and the failure of "left-brained" and "right-brained" people; a catalogue of things that break
alone; a brain that rewires; and today's answer, a network of specialized parts, with the ten-percent myth
settled by an energy bill. The practice chapter is a clinical neuropsychologist's question about one patient; the
frontier is lesion mapping in thousands of patients and the error an artery puts in the map.

## Where the numbers come from

| What | Source |
|---|---|
| Gage's accident, his recovery, "no longer Gage", the stagecoach in Chile | Harlow (1868), from secondary accounts; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md), with what was read and what was not |
| 86 billion neurons, 19% of them in the cerebral cortex | Azevedo et al. (2009), from the abstract |
| The brain is about 2% of body weight and uses about 20% of its energy | Raichle and Gusnard (2002), opening lines |
| Mass action in the rat's cortex | Lashley (1929), from later accounts; no figure is quoted |
| Leborgne ("Tan") and the left frontal lesion | Broca (1861), from secondary accounts |
| The scans of Broca's two preserved brains | Dronkers et al. (2007), from the abstract |
| The second aphasia, the diagram and the predicted third syndrome | Wernicke (1874) and Lichtheim (1885), from secondary accounts |
| 126 patients stimulated while awake, 1928 to 1936 | Penfield and Boldrey (1937), from a later review |
| Magnification of human visual cortex, M = 17.3 / (E + 0.75) mm per degree | Horton and Hoyt (1991), from a citing source |
| H.M.'s operation (1953), what was lost and what was spared | Scoville and Milner (1957) and Milner's later reports, from secondary accounts |
| The split-brain experiments and the interpreter | Gazzaniga and LeDoux (1978) and Sperry's laboratory, from secondary accounts |
| 1,011 people, 7,266 regions: lateralization is local | Nielsen et al. (2013), from the abstract |
| Blindsight in patient D.B. | Weiskrantz et al. (1974), from the abstract |
| One eye closed in kittens, and in adult cats | Wiesel and Hubel (1963), from the abstract |
| The hand's map redrawn after a finger is lost | Merzenich et al. (1984), from the abstract |
| 16 taxi drivers; 79 trainees, 39 qualified, 20 not, 31 controls | Maguire et al. (2000) and Woollett and Maguire (2011), from the abstracts |
| 581 stroke patients: voxelwise lesion maps are displaced along the arteries | Mah et al. (2014), from the abstract |
| The single-case t test | Crawford and Howell (1998) |
| Every score, curve, share, chance and map "computed by Psyche" | `explainer.psychology.psyche.brain` |

The numbers that depend on choices made for the film. Lashley's model cortex has 12 regions; a rat loses one to
seven adjacent regions; the "one place" task needs region 5 and the "six ways" task can be done by any of six
regions, each alone. In the dissociation model a task's score is a logistic function of the resource a lesion
leaves (half-points 0.55 for task A and 0.35 for task B, slope 0.12); a score is "impaired" when it lies more
than two control standard deviations (0.05) below a healthy score; "noisy" tests add an error with the same
standard deviation as the controls' spread. The blind spot is taken to be centred 15 degrees from fixation and
5.5 degrees wide, and the film says that people differ. The patient of chapter 13 is invented: eight controls
scoring 34, 31, 38, 29, 35, 33, 36, 30 on a 40-point test, and a patient scoring 24. The base rate of low scores
assumes independent tests and a cutoff at the 5th percentile. The lesion-mapping sheet is 40 by 40 voxels, fed by
a trunk along the middle row with six branches; 400 simulated patients; the deficit is the share of a disc of
radius 3 destroyed, plus noise of standard deviation 0.5; the displacement is averaged over 30 simulated studies.
The 1,011 simulated people of chapter 8 show what a whole-brain type and what local lateralization would each
predict; they are not Nielsen's data. Resting power is taken as 80 W, so the brain's fifth is 16 W. Every brain
on screen is a schematic, and each is tagged so.

## Built in this part

* `explainer/psychology/psyche/brain.py`, the brain as parts that can be damaged: a box-and-arrow `Architecture`
  with lesions (`LICHTHEIM`, the language diagram, and `MEMORY`), `maze_lesions` (Lashley's result from a brain
  in which every job has a place), `dissociations` and `chance_of_double` (one resource against two, with noisy
  tests), `crawford_howell` (one patient against a small control sample), the cortical magnification functions
  (`magnification`, `cortical_distance`, `area_share`), `blind_spot`, and `lesion_study` (lesion-symptom mapping
  on a sheet fed by one artery). Tested in `tests/psychology/test_brain.py`.
* The Ledger gains four rows and the Archive seventeen datasets.
* On the Homunculus map nothing lights yet: this part says where to look, not how a faculty works.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Damage to the frontal lobes changed a careful, capable man into an impulsive and unreliable one (Phineas Gage) | Harlow 1868 | story and record |
| Damage to the lower rear part of the left frontal lobe takes away fluent speech and spares understanding | Broca 1861 | replicated |
| Years of navigating London enlarge the back of the hippocampus | Maguire and colleagues 2000 | replicated |
| People differ in which hemisphere dominates, and that makes them logical or creative | Pines, in a magazine article, 1973 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Wernicke's aphasia and the
diagram (history, and the logic of the chapter; language has its own rows in Part 23), Lashley's mass action (a
result that stands and a conclusion that did not; memory's rows are in Part 20), Penfield's map and the
magnification formula (measurements, entered with the senses in Part 15 and Part 13), H.M. (a case; the kinds of
memory get their rows in Part 20), the split-brain experiments and blindsight (cases; consciousness is Part 27),
the neuron count and the energy share (measurements, not claims about the mind), the critical period (Part 30),
the remapped hand (a measurement in monkeys, told as history), and Mah et al.'s demonstration of bias in lesion
maps (a methods result at the frontier).

## Build it

```bash
python -m videos.psychology.psych7.compute            # every number (under a minute), into .cache/psych7/
python tools/qa_scene.py psych7 Logic                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych7 -q l   # the whole part, silent preview
python tools/build.py psych7                          # 1080p30 with narration
python tools/qa_scene.py psych7 Logic --lang zh       # the Chinese edition of one chapter
python tools/make.py psych7                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 7                    # the lab: lesions, dissociations and one patient's score
python tools/check_ledger.py psych7                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # Psyche's brain, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | An iron rod, and a question | Gage's accident; the story against the record; one place or everywhere; objectives |
| 1 | A tour of the parts | Four numbers; four lobes, the cerebellum and the brainstem; six structures under the cortex; the crossing |
| 2 | Bumps, pigeons and rats | Gall's idea and his method; Flourens's removals; Lashley's mass action from two model brains |
| 3 | Two aphasias and a diagram | Broca's patient; Wernicke's opposite patient; the diagram and the syndrome it predicted; Broca's brains scanned |
| 4 | The logic of dissociation | One resource gives a single dissociation; what a double one rules out; noisy tests and a large screen; the rules |
| 5 | Maps | Penfield's strip; the magnification of the visual cortex; the share of the map given to the centre of gaze |
| 6 | On you: find your blind spot | Why each eye has one; finding it; what fills the hole; the geometry, and a measurement |
| 7 | The man who could not make new memories | H.M.'s operation; what was lost and what was spared; a skill learned without the memory of learning; what one patient can carry |
| 8 | Two hemispheres | The cable cut; one word, two answers; the interpreter; "left-brained" people against the data |
| 9 | Things that break alone | Neglect, agnosia, prosopagnosia, blindsight; the catalogue read with chapter 4's rules |
| 10 | A brain that rewires | The critical period; a map redrawn in an adult; the taxi drivers, before and after |
| 11 | One place, or everywhere? | Specialized, connected, redundant: the unit is a network; the ten-percent myth and the energy bill |
| 12 | The Ledger | Gage, Broca's area, the taxi drivers, and brain types |
| 13 | In practice: one patient, one question | A z-score; the same case as a sample of eight; how many low scores a battery gives a healthy person; the report |
| 14 | Frontier: mapping damage in thousands | Lesion-symptom mapping; the map pulled toward the artery; four open questions and a research problem |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 8 |

## Sources

**Books.** B. Kolb and I. Q. Whishaw, *Fundamentals of Human Neuropsychology* (8th ed., 2021). T. Shallice, *From
Neuropsychology to Mental Structure* (1988), for the logic of dissociation. M. Macmillan, *An Odd Kind of Fame:
Stories of Phineas Gage* (2000). S. Corkin, *Permanent Present Tense* (2013), on H.M. M. S. Gazzaniga, *Tales from
Both Sides of the Brain* (2015).

**Papers.**
- J. M. Harlow, "Recovery from the passage of an iron bar through the head", *Publications of the Massachusetts
  Medical Society* 2 (1868) 327–347.
- P. Broca, "Perte de la parole, ramollissement chronique et destruction partielle du lobe antérieur gauche du
  cerveau", *Bulletin de la Société d'Anthropologie* 2 (1861) 235–238. N. F. Dronkers, O. Plaisant, M. T.
  Iba-Zizen and E. A. Cabanis, "Paul Broca's historic cases: high resolution MR imaging of the brains of Leborgne
  and Lelong", *Brain* 130 (2007) 1432–1441.
- C. Wernicke, *Der aphasische Symptomencomplex* (1874). L. Lichtheim, "On aphasia", *Brain* 7 (1885) 433–484.
- K. S. Lashley, *Brain Mechanisms and Intelligence* (1929); "In search of the engram", *Symposia of the Society
  for Experimental Biology* 4 (1950) 454–482.
- W. Penfield and E. Boldrey, "Somatic motor and sensory representation in the cerebral cortex of man as studied
  by electrical stimulation", *Brain* 60 (1937) 389–443.
- J. C. Horton and W. F. Hoyt, "The representation of the visual field in human striate cortex", *Archives of
  Ophthalmology* 109 (1991) 816–824.
- W. B. Scoville and B. Milner, "Loss of recent memory after bilateral hippocampal lesions", *Journal of
  Neurology, Neurosurgery and Psychiatry* 20 (1957) 11–21.
- M. S. Gazzaniga and J. E. LeDoux, *The Integrated Mind* (1978).
- J. A. Nielsen et al., "An evaluation of the left-brain vs. right-brain hypothesis with resting state functional
  connectivity magnetic resonance imaging", *PLoS ONE* 8 (2013) e71275.
- L. Weiskrantz, E. K. Warrington, M. D. Sanders and J. Marshall, "Visual capacity in the hemianopic field
  following a restricted occipital ablation", *Brain* 97 (1974) 709–728.
- T. N. Wiesel and D. H. Hubel, "Single-cell responses in striate cortex of kittens deprived of vision in one
  eye", *Journal of Neurophysiology* 26 (1963) 1003–1017.
- M. M. Merzenich et al., "Somatosensory cortical map changes following digit amputation in adult monkeys",
  *Journal of Comparative Neurology* 224 (1984) 591–605.
- E. A. Maguire et al., "Navigation-related structural change in the hippocampi of taxi drivers", *PNAS* 97
  (2000) 4398–4403. K. Woollett and E. A. Maguire, "Acquiring 'the Knowledge' of London's layout drives
  structural brain changes", *Current Biology* 21 (2011) 2109–2114.
- F. A. C. Azevedo et al., "Equal numbers of neuronal and nonneuronal cells make the human brain an
  isometrically scaled-up primate brain", *Journal of Comparative Neurology* 513 (2009) 532–541. M. E. Raichle
  and D. A. Gusnard, "Appraising the brain's energy budget", *PNAS* 99 (2002) 10237–10239.
- J. R. Crawford and D. C. Howell, "Comparing an individual's test score against norms derived from small
  samples", *The Clinical Neuropsychologist* 12 (1998) 482–486.
- Y.-H. Mah, M. Husain, G. Rees and P. Nachev, "Human brain lesion-deficit inference remapped", *Brain* 137
  (2014) 2522–2531.

## Problems and solutions

**1.** *In the diagram of chapter 3, a lesion cuts the link between word sounds and concepts and leaves
everything else. Which of understanding, speaking and repeating survive? Name the lesion that gives the opposite
pattern for repeating.*

Follow each task's route. Understanding runs hearing, word sounds, concepts: it uses the cut link, so it fails.
Speaking runs concepts, word movements, mouth: untouched. Repeating runs hearing, word sounds, the pathway, word
movements, mouth: it never passes through concepts, so it survives. The patient repeats sentences they do not
understand. That syndrome exists (it is called transcortical sensory aphasia), and Lichtheim's version of the
diagram predicted it in the same way as the third row of the film's table. The opposite pattern for repeating is
the film's third row: cut the pathway between word sounds and word movements, and the patient understands and
speaks and cannot repeat (conduction aphasia).

**2.** *Under one resource, a share p_A = 0.20 of patients fail only task A and, with noisy tests, p_B = 0.007
fail only task B. Show that the chance a screen of N patients contains both kinds is
1 − (1 − p_A)^N − (1 − p_B)^N + (1 − p_A − p_B)^N, and evaluate it for N = 100.*

Each patient is of kind A-only, B-only or neither, independently. Let E_A be "no A-only patient among the N" and
E_B the same for B. Then P(E_A) = (1 − p_A)^N, P(E_B) = (1 − p_B)^N, and both happen when every patient is of
neither kind, P(E_A and E_B) = (1 − p_A − p_B)^N. The screen contains both kinds unless E_A or E_B happens, so the
chance is 1 − P(E_A) − P(E_B) + P(E_A and E_B). For N = 100: 0.8^100 is about 2 × 10^-10, 0.993^100 = 0.495 and
0.793^100 is about 10^-10, so the chance is 0.505. Half of all clinics that screen a hundred patients from a
world with one resource will hold a "double dissociation". The cure is not a stricter cutoff alone; it is a
prediction made before the search, tests of known reliability, and a second patient of the rare kind.

**3.** *With M(E) = 17.3 / (E + 0.75) mm per degree, show that the cortical distance from the centre of gaze to
eccentricity E is 17.3 ln(1 + E/0.75) mm. How much larger must a letter be at 8 degrees than at 1 degree to cover
the same length of cortex?*

Distance is the integral of M: the integral from 0 to E of 17.3 / (e + 0.75) de = 17.3 [ln(E + 0.75) − ln 0.75] =
17.3 ln(1 + E/0.75). To 1 degree that is 14.7 mm, to 8 degrees 42.5 mm: the first degree takes a third of the
distance to the eighth. A small letter of size s at eccentricity E covers about s M(E) of cortex, so equal cortex
needs s proportional to 1/M, that is to E + 0.75. The ratio is 8.75 / 1.75 = 5. (At 16 degrees it is
16.75 / 1.75 = 9.6, the last letter of the film's chart.)

**4.** *Your blind spot is centred 15 degrees from fixation and is 5.5 degrees wide. Two marks are 10 cm apart.
How far from them must your eye be for one to vanish while you fix the other? How many full moons (0.5 degrees)
fit across the hole?*

A point at angle a from fixation lands d tan(a) from the fixation mark on a screen at distance d. So
10 cm = d tan 15°, d = 10 / 0.268 = 37 cm. The hole runs from 12.25 to 17.75 degrees, that is from
37.3 tan 12.25° = 8.1 cm to 37.3 tan 17.75° = 11.9 cm: 3.8 cm wide on the screen at that distance. Across it fit
5.5 / 0.5 = 11 full moons. The interactive for this part measures the two edges on your own eye.

**5.** *Eight controls score a mean of 33.25 with standard deviation 3.11; a patient scores 24. Compute z and the
single-case t. Repeat for thirty controls with the same mean and standard deviation, and explain the change.*

z = (24 − 33.25) / 3.11 = −2.98, which the normal curve gives to 1 healthy person in about 690. The single-case
test is t = (x − mean) / (s √((n + 1)/n)) on n − 1 degrees of freedom. With n = 8: t = −2.98 / √(9/8) = −2.81 on
7 degrees of freedom, a one-tailed probability of 0.013, 1 in 76. With n = 30: t = −2.98 / √(31/30) = −2.93 on 29
degrees of freedom, a probability of 0.0033, 1 in about 300. Two things changed. The factor √((n + 1)/n) shrinks
toward 1, because the control mean is better known; and, much more important, the t distribution's tails thin
toward the normal's, because the control standard deviation is better known. As n grows the answer approaches
the z-score's 1 in 690. With eight controls the z-score overstates the rarity ninefold.

**6.** *With `explainer.psychology.psyche.brain`: build an `Architecture` in which two tasks share one module and
each has a module of its own. Which lesions dissociate them? Then run `lesion_study` with and without `vascular`
and compare where the maps point.*

```python
import numpy as np
from explainer.psychology.psyche import brain as B

arch = B.Architecture(modules=("shared", "only A", "only B"),
                      tasks={"A": ("shared", "only A"), "B": ("shared", "only B")})
for lesion in ({"shared": 1.0}, {"only A": 1.0}, {"only B": 1.0}):
    print(lesion, arch.performance(lesion))
print(arch.dissociates("A", "B"))

for vascular in (True, False):
    study = B.lesion_study(rng=np.random.default_rng(1), vascular=vascular)
    print(vascular, study["centre"], study["shift"], round(study["displacement"], 2))
```

A lesion of the shared module fails both tasks; a lesion of "only A" fails A and spares B; a lesion of "only B"
does the reverse. `dissociates` reports a double dissociation, with the two private modules as the lesions that
give it. Remove the private modules (both tasks on one module) and it reports none. So a double dissociation
shows that each task has something the other does not; it does not show that they share nothing. In the lesion
study the critical region is centred at (22, 26). With an artery, this seed puts the map's centre at (22.4, 22.3),
3.7 voxels away and nearly all of it toward the trunk (row 20); with lesions anywhere it is at (20.9, 26.9), 1.4
voxels away in no particular direction. Over thirty studies the averages are 2.4 and 1.1 voxels, and with an
artery the map moved toward the trunk in 23 of the 30.

**7.** ★ *Design the lesion study that would tell "this region is needed" from "a connection passing under this
region is needed", and say what each outcome would look like.*

There is no single right answer; a good one has four parts. (i) Describe each patient's damage twice: the share
of the region's grey matter destroyed, and the share of the tract destroyed (from the scan, laid on an atlas of
the white matter, or better from that patient's own diffusion imaging). In strokes the two go together, because
one artery feeds both; that correlation is the problem, so report it. (ii) Find the patients who separate them.
Small cortical lesions that spare the white matter (some tumours, some surgical removals), and deep lesions that
cut the tract and spare the cortex (small subcortical strokes, demyelination). These patients are rare, which is
why the question is open; a multi-centre register is the realistic route. (iii) State the predictions before
looking. If the region is needed, the deficit follows grey-matter damage among patients matched on tract damage,
and deep lesions that spare the cortex leave the task alone. If the connection is needed, the deficit follows
tract damage, appears after deep lesions wherever along the tract they fall, and cortical lesions that spare
the tract leave the task alone. If both matter, both effects appear and the model needs both terms. (iv) Add a
method with different weaknesses. Brief magnetic stimulation over the region in healthy people disturbs the
cortex and not the fibres passing beneath; stimulation of the exposed white matter during surgery does the
reverse. A conclusion that holds across lesions and stimulation is worth more than a larger lesion sample, since
no number of strokes removes the artery from the design.

## Where it comes back

Watching an intact brain at work, and what a scan's coloured map is: Part 8. The map of the visual field from the
retina in, and receptive fields: Part 13. Filling in, and seeing as a conclusion: Part 14. The body's map and
touch: Part 15. Neglect, with attention: Part 18. H.M. and the kinds of memory: Part 20. Aphasia, with language:
Part 23. Blindsight and the interpreter: Part 27. Critical periods: Part 30. Maps of brain data as statistics:
Part 49. Psyche's `brain` module is the lesionable architecture later parts test their box-and-arrow models in.

## Open checks

Before the narrated master:

* Harlow (1848, 1868) and Macmillan (2000) were not read. The rod is described as "more than a metre long, as
  thick as a broom handle, about six kilograms" because sources differ on the exact figures; the date of death
  differs between sources (1860 or 1861), so the film says "about twelve more years". "Business enough" for the
  doctor, the cart, and "the most capable man they had" are from the usual accounts. That he drove a stagecoach
  in Chile "for years" follows Harlow as reported by Macmillan; check the length.
* The count of neurons and the cortex's share are from the abstract of Azevedo et al. (2009); "most of the rest
  are in the cerebellum" is from the same paper as usually cited (about 69 billion) and was not checked. The
  corpus callosum's "some two hundred million fibres" is a textbook figure. Resting power of 80 W, and so 16 W
  for the brain, is a round figure for an adult at rest.
* Gall: "around 1800", "more than two dozen faculties" (the usual figure is 27) and the examples are from
  histories of phrenology. Flourens: "the 1820s", pigeons, the three results as stated are the standard summary
  of his 1824 book, not read. Lashley (1929, 1950) was not read; no quotation is used; "thirty years" is from the
  1950 paper's title and usual accounts.
* Broca (1861): "in hospital for twenty years" (Leborgne is usually said to have been at Bicêtre for 21 years)
  and "he understood what was said to him" follow secondary accounts. Wernicke was 26 in 1874 (born 1848).
  "Conduction aphasia was then found" is the standard history; check who first described a clear case.
* Penfield and Boldrey (1937): 126 patients, 1928 to 1936, is from a later review. The order along the strip is
  simplified, and the lengths of the film's segments are not measurements. Two-point thresholds ("a few
  millimetres" on a fingertip, "centimetres" on the back) are textbook values.
* Horton and Hoyt's formula is from a citing source. "First charted from soldiers with small wounds" refers to
  Inouye and to Holmes; neither was read and neither is named. The blind spot's position and size (15 degrees
  out, 5.5 degrees wide) are typical textbook values; the film says people differ. "About two screen-widths" for
  the demonstration depends on the layout in `s07_blind.py` and should be re-checked on the final render.
* H.M.: the operation's exact date differs between sources, so only the year is given. "A patient of sound mind"
  paraphrases the usual account of how radical the operation was; check Scoville and Milner's own description of
  their case series. Milner's mirror-tracing report (1962) was not read: "three days" and "no memory of having
  done it" are from secondary accounts, and the film's curve is the shape of the result, tagged as computed.
  That the removal included the amygdala and the surrounding cortex is from later imaging reports (Corkin and
  colleagues, 1997), not read.
* Split brain: the operations "in the nineteen-sixties", the key and ring, and the chicken claw, snow scene and
  shovel are from Gazzaniga's own later accounts; the patient's reply in the quotation card is the wording
  Gazzaniga gives there, to be checked against *The Integrated Mind*. The 1973 article is M. Pines, *New York Times Magazine*, 9 September 1973: confirm the headline.
  Nielsen et al.'s group was at the University of Utah.
* The catalogue (neglect, visual agnosia, prosopagnosia, blindsight) is described from textbooks; only blindsight
  cites a paper, from its abstract. That the reverse of prosopagnosia has been described (objects lost, faces
  kept) refers to the patient C.K. of Moscovitch and colleagues (1997), not read.
* Wiesel and Hubel (1963): "the first months of life" and "even for a year" in adults follow the abstracts of the
  1963 papers. The film's coloured columns are a schematic. Merzenich et al. (1984): owl monkeys, mapped two to
  eight months after the loss, from the abstract; "a touch on the face felt in the missing hand" is Ramachandran
  and colleagues (1992), not read.
* Maguire et al. (2000): "some twenty-five thousand streets" and "takes years" are the usual description of the
  Knowledge; the counts for 2011 are from the abstract.
* William James and the ten-percent myth: the attribution to a misreading of "The Energies of Men" (1907) is the
  usual account and is given as probable.
* Chapter 13: "the standard deviation could easily be off by a quarter" is the standard error of a standard
  deviation from eight observations, 1/√14 = 0.27. That real batteries are correlated and still give most healthy
  adults at least one low score is stated without a figure; a norms study should be cited before the master.
* Chapter 14: "since the early two-thousands" for voxel-based lesion-symptom mapping refers to Bates et al.
  (2003), not read. Mah et al. (2014) is described from its abstract; "a London group" is University College
  London. The line that methods weighing all voxels together "do better" should be tied to a reference.
* The teaser for Part 8 (the salmon of 2009) is checked with Part 8's own sources.
