# The Archive: sources and checks

Every dataset in `explainer/psychology/archive/` is listed here with where it comes from, its licence, and the
check that was made before it was used on screen. A dataset whose licence does not allow redistribution is cited
and summarized, not stored. Dates are the day the check was made.

| Key | What | Source | Licence | Check |
|---|---|---|---|---|
| `kant_1786` | The three objections of the Preface to the *Metaphysical Foundations of Natural Science* | Kant (1786), Akademie 4:471; English by E. B. Bax (1883), p. 141 | public domain | 2026-11-13: quotations read against the 1883 translation ([Wikisource, p. 141](https://en.wikisource.org/wiki/Page:Kant%27s_Prolegomena_etc_(1883).djvu/263)) |
| `helmholtz_1850` | Nerve lengths, delays and speeds of Helmholtz's first report; his human values; the later measurements | Helmholtz (1850), as reported by Schmidgen, "Of frogs and men", *Endeavour* 26 (2002) 142–148 ([repository copy](https://epub.uni-regensburg.de/27126/1/schmidgen.pdf)) | facts only | 2026-11-13: 50–60 mm, 0.0014–0.0020 s, 25–43 m/s, about 60 m/s in humans, 0.1 s of "perceiving and willing", Hirsch 34, Donders and de Jaager 26.00–26.09, Helmholtz and Baxt 33.9 and then 64.6 m/s, all read in Schmidgen |
| `donders_1868` | Mean reaction times by the a-, b- and c-methods: 201, 284, 237 ms | Donders (1868; transl. Koster 1969); Roelofs, *Acta Psychologica* 191 (2018) 228–233 | facts only | 2026-11-13: the three means, the differences 36 and 47 ms, the ordering a < c < b and the students' notebook result confirmed from Roelofs's abstract ([Europe PMC](https://europepmc.org/article/MED/30343095)) and a search summary of the paper. **Open:** the paper's full text and Koster's translation were not retrievable from this environment; read both before the narrated master. Note that the English Wikipedia article on Donders (as of this date) swaps the labels of the two differences |
| `ebbinghaus_1885` | Savings after 20 min, 1 h, 8.8 h, 1, 2, 6 and 31 days; probable errors; his formula and fitted column | Ebbinghaus (1885), ch. VII, in the Ruger and Bussenius translation (1913) | public domain | 2026-11-13: transcribed from the chapter's table images at [psychclassics.yorku.ca](https://psychclassics.yorku.ca/Ebbinghaus/memory7.htm) |
| `woods_2015` | Simple visual reaction time of 1,469 adults: 231 ms raw, 213 ms after hardware correction; 0.55 ms per year of age; detection time 131 ms | Woods et al., *Frontiers in Human Neuroscience* 9 (2015) 131 | CC BY (summary statistics) | 2026-11-13: read from the abstract ([PMC4374455](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4374455/)) |

## Looked for and not used

- **Merkel's 1885 table of choice reaction times** (one to ten alternatives), the data Hick refitted in 1952. The
  table as usually reproduced from Woodworth (1938) could not be checked against a source from this environment,
  so Part 1 does not show it. Part 25 (Deciding in Time) should transcribe it from Woodworth or from Merkel's
  paper (*Philosophische Studien* 2, 73–127) and Hick's own data from Hick (1952).
- **Hedge, Powell and Sumner (2018)**, trial-level reaction times for seven tasks ([OSF](https://osf.io/cwzds/)).
  Public, but the OSF project states no licence. To be fetched at compute time (not stored here) when Parts 3,
  18 and 59 need it, after confirming the terms with the paper's data statement.
