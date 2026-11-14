# Music, Built: Part 37, Timelines

Part 37 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act VI. One bell pattern, seven strokes in twelve pulses, is heard
from Ghana to Cuba to Brazil; written as steps it reads 2-2-1-2-2-2-1, the major scale turned into time. This part
studies musics organized around such timelines: how to measure them, how an Ewe ensemble builds its parts against a
bell, three against two and the argument over how to write it, hocket, the mbira and the melodies that form in the
listener's ear though nobody plays them, the clave, samba, and call and response. The tools are Monochord's
(`explainer/music/monochord/timelines.py`); the instruments are its models: an iron bell by modal synthesis, Part 9's
membranes for drums and its bar for claves and mbira tines (held at one end), Part 8's flute for pipes, Part 35's
retuned plucked string for guitar and bass, and Part 17's model choir. Every part, pattern and melody played is ours;
the timelines are the well-known ones, as they are commonly transcribed. Published findings are the ones listed under
Sources.

* **Seven strokes in twelve pulses.** An ear question (how many beats a cycle?); the bell with four beats and with six,
  heard; where the pattern is heard; the plan.
* **1. The standard pattern.** Its steps and the major scale's (2 2 1 2 2 2 1); bell, scale and both, heard; the seven
  rotations as the seven modes; Dorian and Aeolian, heard; maximal evenness and Bjorklund's E(7,12); a deep set (each
  distance between strokes occurs 2, 5, 4, 3, 6 and 1 times, as the diatonic scale's intervals do); a caution.
* **2. Measuring timelines.** Five measures; ten timelines measured (bossa nova the most even of the sixteen-pulse
  ones, soukous the least; son clave, rumba clave and bossa nova odd; the standard pattern on three of the four
  off-beat pulses); the off-beat pulses drawn; four claves, heard; centrality by swap distance (son clave 6, bossa
  nova 8, the rest 10 or 12); what the measures cannot say.
* **3. An Ewe ensemble.** The Ewe; six parts of ours (bell, rattle, kagan, kidi, sogo, lead drum); the parts entering,
  heard; a part is a relation; the lead drum; learning the parts.
* **4. Three against two.** Four, six and three beats in twelve pulses (the bell on 2 of 4, 3 of 6, 2 of 3); four,
  six, both and the bell, heard; hemiola; Jones, Nketia, Kubik, Arom, Agawu and Locke on notation; two notations drawn;
  where is one?
* **5. Interlocking and hocket.** Hocket from medieval Europe to the Andes and Central Africa; the Tune's opening on two
  model panpipes, each alone and together, heard; five single-pitch pipes entering, heard; Arom's playback method; why
  hocket.
* **6. The mbira.** The mbira dzavadzimba; a clamped tine's partials (1 : 6.27 : 17.55), heard plain and buzzing; how it
  is played; kushaura and kutsinhira of ours, heard; the bira; the mbira travels.
* **7. Inherent patterns.** Kubik and the amadinda; an ear question (two parts at ten notes a second: which of three
  melodies do the high notes make?); the streaming model, which recovers the melody note for note; the same notes at
  about three a second, heard; what the model leaves out; Reich and Ligeti.
* **8. The clave.** Tresillo, cinquillo and habanera, heard; the tresillo travels; son clave three-two and two-three,
  heard; the anticipated bass; a son texture of ours, layer by layer, heard; son and salsa.
* **9. Samba, and call and response.** Samba; a batucada of ours drawn and heard; two surdos in conversation; call and
  response; a call and response of ours, heard; no seam.
* **10. Frontier: timing measured.** Non-isochronous subdivision (Polak; Polak and London); an ear question (which beat
  is divided unequally?); meter across cultures (Hannon and Trehub; Jacoby and McDermott; Jacoby and colleagues);
  ★ research problem: how are rhythm categories learned, and how fast can they change?; archives and ethics.
* **Variation 37, recap and problems.** The Tune's first two phrases as an inherent pattern: its fourteen notes on a
  grid of 48 pulses, three to a beat, shared between two mbira parts on even and odd pulses with a low filler (8 of
  its notes in one part, 6 in the other, neither playing the Tune); each part alone, both together, then over the
  standard pattern on claves; the ledger; what we found; five problems; where it comes back; in practice; references;
  Part 38.

## What is computed, and what is heard

`python -m videos.music.music37.compute` (about ten seconds) fills `.cache/music37/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `scale` | the standard pattern in four and six; its steps, rotations, modes and interval content | the major scale (tests) |
| `metrics` | evenness, Euclidean test, oddity, off-beatness for ten timelines; swap distances and centrality | breadth-first swaps (tests) |
| `ewe`, `threetwo` | six parts of ours against the bell; four beats against six | — |
| `hocket` | the Tune split between two panpipe rows by pitch; five single-pitch pipes | every note in one part only |
| `mbira` | a clamped tine with and without buzz; two interlocking parts | the beam's eigenvalues |
| `inherent` | two designed parts; the streaming model's high stream; fast and slow | the target melody, note for note |
| `clave`, `son` | tresillo, cinquillo, habanera; son clave both ways; a son texture | — |
| `samba`, `callresp` | a batucada; call and response with model voices | — |
| `uneven` | a beat divided equally and unequally (illustrative proportions) | — |
| `tune`, `variation` | Variation 37 | the Tune, note for note |

Monochord's tools are held in `tests/music/test_timelines.py`; this part's claims and clips in
`tests/music/test_music37.py`.

**Sounds.** The iron bell and agogô are modal models with designed ratios; the drums are Part 9's membrane (open,
muted and slapped strokes); the claves and mbira tines are Part 9's bars; rattles, shakers, snare and claps are
filtered noise; the pipes are Part 8's flute; the guitar and bass are Part 35's retuned plucked string through Part 7's
body; the voices are Part 17's choir (labelled `synthesized`). There are no recordings.

**What the models are, and are not.** *The ensembles* (Ewe, son, samba) are parts of our own in the manner of those
musics, not transcriptions of any piece; real performances vary their parts, and the lead drum's language is far
richer than four phrases. *The timelines* are given as they are usually transcribed; musicians may start them
elsewhere and play them with uneven timing. *The streaming model* is a single split point: real streaming depends on
rate, separation, timbre, loudness and attention. *The uneven subdivision* uses illustrative proportions of our own,
not measurements.

## Build

```bash
python -m videos.music.music37.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music37 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music37 --sync                         # the sound gates
python tools/dead_air.py renders/music37_480p.mp4 --sound music37  # no empty screen; no sound over a still one
python tools/lecture_length.py music37                          # 30 to 60 minutes, listening included
python tools/build.py music37                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 37                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Compute the swap distances among the six five-stroke claves, and each one's total.

   *Solution.* Writing each as its onsets (son 0 3 6 10 12, rumba 0 3 7 10 12, bossa 0 3 6 10 13, gahu 0 3 6 10 14,
   soukous 0 3 6 10 11, shiko 0 4 6 10 12), the swap distance is the sum of the differences between corresponding
   onsets. Son is 1 from rumba, bossa, soukous and shiko and 2 from gahu: total 6, the least. Bossa nova totals 8;
   rumba, soukous and shiko 10; gahu 12. The lab prints the totals.

2. **Prove.** Prove that pulse k of an n-pulse cycle lies on a regular polygon through pulse 0 (a diameter counts)
   exactly when gcd(k, n) > 1.

   *Solution.* A regular polygon through pulse 0 with its vertices on pulses has vertices at the multiples of some step
   s that divides n, with s < n so that it has at least two vertices. If k is a vertex then s divides both k and n, so
   gcd(k, n) ≥ s > 1. Conversely, if g = gcd(k, n) > 1, the polygon with step g has n/g ≥ 2 vertices (n/g = 1 would mean
   g = n, so k = 0, which is on every polygon) and k is a multiple of g. So the off-beat pulses are exactly those with
   gcd(k, n) = 1: in twelve, pulses 1, 5, 7 and 11 after the start.

3. **Ear.** The lab plays interlocking parts at several speeds; say when the inherent melody appears.

   *Solution.* The lab prints the speeds in the order played. At three notes a second most listeners hear one leaping
   line; by eight or twelve the high notes separate into the melody. Where the change happens for you depends on the
   size of the leaps, and on whether you are listening for it.

4. **Build.** Design two interlocking parts whose high notes spell a melody of your own; check them with the streaming
   model.

   *Where to look.* Use `timelines.design_inherent` (or `interlock_melody` for a melody with its own rhythm), keep the
   melody above the split and the filler at least an octave below, and check that `timelines.inherent` returns your
   melody while neither part's high notes alone do. Then render both parts at several speeds with `timelines.mbira`.

5. ★ **How are rhythm categories learned, and how fast can they change?**

   *Where the frontier is.* Record players and listeners from several traditions, with motion capture of the dance;
   measure the timing of every stroke and where each body places the beat; run iterated-reproduction experiments that
   start from uneven grids as well as even ones; and follow learners over months, to see how their categories move.

## Sources

* K. Agawu, *Representing African Music* (2003); "Structural analysis or cultural analysis? Competing perspectives on
  the 'standard pattern' of West African rhythm", *Journal of the American Musicological Society* (2006).
* A. M. Jones, *Studies in African Music* (1959); J. H. K. Nketia, *African Music in Ghana* (1962) and *Drumming in Akan
  Communities of Ghana* (1963).
* D. Locke, *Drum Gahu* (1987).
* S. Arom, *African Polyphony and Polyrhythm* (1985; English 1991).
* G. Kubik, "The phenomenon of inherent rhythms in East and Central African instrumental music", *African Music*
  (1962); P. Berliner, *The Soul of Mbira* (1978).
* G. T. Toussaint, *The Geometry of Musical Rhythm* (2013; 2nd ed. 2020); "The rhythm that conquered the world: what
  makes a 'good' rhythm good?", *Percussive Notes* (2011); J. Pressing, "Cognitive isomorphisms between pitch and
  rhythm in world musics", *Studies in Music* (1983); J. Rahn, "Turning the analysis around: Africa-derived rhythms and
  Europe-derived music theory", *Black Music Research Journal* (1996).
* L. P. A. S. van Noorden, *Temporal Coherence in the Perception of Tone Sequences* (1975); A. S. Bregman, *Auditory
  Scene Analysis* (1990).
* R. Polak, "Rhythmic feel as meter: non-isochronous beat subdivision in jembe music from Mali", *Music Theory Online*
  (2010); R. Polak and J. London, "Timing and meter in Mande drumming from Mali", *Music Theory Online* (2014).
* E. E. Hannon and S. E. Trehub, "Metrical categories in infancy and adulthood", *Psychological Science* (2005); N.
  Jacoby and J. H. McDermott, "Integer ratio priors on musical rhythm revealed cross-culturally by iterated
  reproduction", *Current Biology* (2017); N. Jacoby and others, "Commonality and variation in mental representations
  of music revealed by a cross-cultural comparison of rhythm priors in 15 countries", *Nature Human Behaviour* (2024).
* Part 9 for bars and membranes; Part 11 for meter; Part 16 for streams; Part 33 for Euclidean rhythms; Part 36 for
  interlocking parts.
