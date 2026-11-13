# Psychology, Built: Part 2, The Experiment

**In progress.** The compute, the Archive entries, the laboratory and the first chapters are written; the film is
not yet complete.

Berlin, 1904. A horse named Hans answers arithmetic with his hoof, and a commission of thirteen finds no trick.
One student, Oskar Pfungst, changes one thing at a time and counts: Hans is right 98 times in 100 when the
questioner knows the answer and 8 in 100 when he does not. Nobody cheated. The questioners were telling the horse
the answer with a movement of the head too small for them to feel. Every rule of experimental design in psychology
is a way of asking a mind a question without telling it the answer, and most of them are in that story: the
comparison, the control group, the blind, and the shuffled deck, which psychologists used first.

## Where the numbers come from

| What | Source |
|---|---|
| Hans, the commission of 12 September 1904, Pfungst's counts | Pfungst (1907; transl. 1911), read from the translation ([`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md)) |
| The shuffled deck of 1884 | Peirce and Jastrow, "On small differences in sensation" |
| The "bright" and "dull" rats | Rosenthal and Fode (1963), Table 1 |
| Teacher expectancy by weeks of contact | Raudenbush (1984) |
| Detection dogs | Lit, Schweitzer and Oberbauer (2011) |
| Demand effects, measured | de Quidt, Haushofer and Roth (2018) |
| Unblinding in a drug trial | Mitchell et al. (2021) |
| The model of Hans | `explainer.psychology.psyche.cueing`, four parameters fitted to Pfungst's eight conditions |
| Every study of "the game" | `explainer.psychology.lab` on the Pool (simulated; the truth is planted) |

## Built in this part

* `explainer/psychology/lab.py`: the laboratory. Assignment by shuffle, balance, Welch and paired comparisons, the
  randomization test, Latin and Williams squares, power, and a `Lab` that runs the randomized experiment, the
  cross-over and Campbell and Stanley's six unsound designs on the Pool with the truth known.
* `explainer/psychology/psyche/cueing.py`: Clever Hans as a mechanism, a reader of an involuntary cue whose
  detection falls with distance as a psychometric function.
* The Pool gains repeat sessions (practice, day-to-day variation) and an eagerness to sign up for things.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| An animal reads its handler | Pfungst 1907 | replicated |
| "Bright" rats learn faster | Rosenthal and Fode 1963 | not directly tested |
| Teachers' expectations raise IQ | Rosenthal and Jacobson 1968 | replicated, smaller |
| Subjects do what they think is wanted | Orne 1962 | replicated |
| People cannot be random | Wagenaar 1972 | replicated |

## Build it

```bash
python -m videos.psychology.psych2.compute            # every number (a few seconds), into .cache/psych2/
python tools/qa_scene.py psych2 Pfungst               # one chapter, silent, at 480p, with a contact sheet
python -m pytest tests/psychology                     # the laboratory, the Pool, the Ledger and the Archive
```

## Open checks

Stated from standard references and not yet read against a primary source: Milgram (1963), 26 of 40 participants
continuing to 450 volts; the Tuskegee study, 1932 to 1972; the three principles of the Belmont Report (1979);
Chevreul's pendulum (1833) and Carpenter's "ideo-motor" (1852); Arnett's figures on samples (2008), known here from
secondary sources; Wagenaar (1972) and Falk and Konold (1997) on produced randomness, known here from search
summaries of the reviews.
