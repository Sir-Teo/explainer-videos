# Music, Built: Part 4, The Ear

Part 4 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Parts 1 to 3 built a string, the air that carries its sound and the spectrum that
takes the sound apart, and ended with a tone that keeps its pitch although it has no energy at its fundamental. A
spectrum describes the air; this part opens the instrument that listens to it. Every model in it is Monochord's own
(`explainer/music/monochord/ear.py`: about four hundred lines), checked against published measurements of real
ears; every sound is computed in `compute.py`. Dates and attributions are the published ones, listed under Sources.

* **The ear that sings.** Two pure tones, 1000 and 1200 Hz, and the third tone at 800 Hz that many listeners hear
  beneath them, which is not in the recording (183 dB down); Kemp's microphone in an ear canal (1978); Gold's
  amplifier (1948) against Békésy's passive wave (Nobel Prize, 1961; his cochleas came from cadavers); the plan.
* **1. From air to water.** The path of a sound; the mismatch between air and the cochlea's fluid (1.1% of the
  power would get in); a worked example, the middle ear as a transformer (area ratio 17, lever 1.3: pressure × 22,
  27 dB; 1% → 27%); the ear canal as Part 2's stopped pipe (2.5 cm: about 3,500 Hz), and the threshold of hearing,
  lowest where the canal resonates.
* **2. A wave that sorts.** The cochlea unrolled; Helmholtz's harp and what Békésy saw (from 1928); the travelling
  wave in Monochord's cochlea, and why it stops; seven tones an octave apart, each peak 4.6 mm from the last;
  a worked example (where does 3000 Hz peak?); the model's map against Greenwood's; inner and outer hair cells.
* **3. How fine is the ruler?** Two tones on one stretch of membrane; Fletcher's band-widening experiment (1940)
  run on the model (a band of 133 Hz at 1 kHz); the ERB formula; a worked example (133 Hz at 1 kHz is 2.3
  semitones; 3.6 at 250 Hz); an ear question (beats, roughness, two tones); the Tune's opening as a cochleagram;
  resolved and unresolved partials (the first eight).
* **4. How loud is loud?** A tone sliding from 100 Hz to 10 kHz at constant pressure; the threshold of hearing;
  an ear question (three tones of one pressure); phons (Fletcher and Munson, 1933) and the A weighting; sones
  (Stevens, 1936): ten times the power is twice as loud, so ten violins are twice as loud as one; a worked
  example (sixteen first violins: 12 dB, 2.3 times as loud); 120 dB heard as twelve doublings.
* **5. What a loud sound hides.** The power-spectrum model of masking; what a 1 kHz tone at 70 dB hides (a worked
  example, read off the graph); an ear question (a pulsing tone alone, beside the loud tone, far above it); why
  masking spreads upwards; codecs, mixing, orchestration, hearing loss.
* **6. A second clock.** Hair cells pass on half of each cycle; ten fibres mark every crest between them (the
  volley idea; Wever and Bray, 1930); where in the cycle the spikes fall at 250, 1000 and 4000 Hz; the clock fades
  above about 1 kHz and stops by about 5 kHz; an ear question (up or down: 17 cents, then 5); the ear resolves 2 Hz
  through a filter 133 Hz wide.
* **7. The pitch that is not there.** An ear question: one note with all its partials, without the lowest three,
  the same over low noise, and its fundamental alone; Helmholtz's distortion explanation and Licklider's masking
  test of it; Schouten's residue (1940); Licklider's autocorrelation model (1951) on the three sounds (130.9,
  130.8, 130.8 Hz); a worked example (600, 800, 1000 Hz: 200 Hz); Schouten's shifted partials (the spacing stays
  200 Hz, the pitch rises to 205); telephones, small loudspeakers, organ pipes, roots of chords.
* **8. Where pitch stops.** The Tune's opening in pure tones, then above 5 kHz; Attneave and Olson (1971); the
  model's pitch strength against frequency, and the piano's range laid beneath it.
* **9. Two kinds of high.** Shepard's tones (1964): twenty-four steps up that end where they began (the waveforms
  are identical); how they are made; chroma and height; why the octave.
* **10. The only pair you get.** No sound. Hair cells do not grow back; the notch at 4 kHz; the NIOSH rule (85 dBA
  for 8 hours, halved for every 3 dB); a worked example (100 dBA: 15 minutes; 20 dB earplugs: a hundred times as
  long); four habits.
* **11. Frontier: the ear is alive.** Friction cut to a quarter makes the model's peak 13 dB taller and twice as
  sharp; Rhode (1971), Brownell (1985), prestin (2000); an oscillator at the edge of oscillation responds as the
  cube root of the force (100 dB in, 33 dB out); the third tone again, with a guide (2f₁ − f₂; Tartini, 1754; the
  newborn hearing test); emissions; what is not known: hidden hearing loss, the amplifier in vivo, music through
  cochlear implants, regeneration. ★ research problem.
* **Variation 4, recap and problems.** The Tune with partials 3 to 6 only, then as Shepard tones; the ledger; what
  we found; five problems; where it comes back; in practice; references; two pairs of strings, and Part 5.

## What is computed, and what is heard

`python -m videos.music.music4.compute` (about ten seconds) fills `.cache/music4/`.

| Item | What it computes | Checked against |
|---|---|---|
| `two` | two pure tones; the spectrum of an oscillator at a Hopf bifurcation driven by them | a line at 2f₁ − f₂, 18 dB below the tones; none in the clip |
| `outer` | the canal's quarter-wave resonance; the middle ear's gain and power transmission | area ratio and lever from the anatomy (Pickles); 27 dB |
| `wave` | the long-wave cochlea at seven frequencies; a film at 1 kHz; the place map; damping at a quarter | the peak just basal of the local resonance; Greenwood (1990) |
| `bands` | gammatone filters and their widths; Fletcher's experiment; resolved partials; a 64-band cochleagram | the ERB formula of Glasberg and Moore (1990), to 1% |
| `loud` | the threshold in quiet (Terhardt's formula), the A weighting, sones | ISO 226 and IEC 61672 values at 100 Hz, 1 kHz, 3.5 kHz |
| `mask` | the masked threshold beside a 1 kHz tone at 70 dB | the probe at 1150 Hz hidden by 11 dB, at 3000 Hz clear by 37 dB |
| `locking` | a hair cell and nerve model: synchrony and pitch strength from 250 Hz to 8 kHz; spike rasters | the shape of Johnson's (1980) cat data: strong below 1 kHz, gone by 5 kHz |
| `pitch` | the summary autocorrelation of a pure tone, a full tone and one without partials 1 to 3; Schouten's shift | the same pitch within a cent; 205.3 Hz for the shifted complex (first pitch shift: 205) |
| `limit` | the Tune's opening in pure tones near 500 Hz and above 5 kHz | (heard) |
| `shepard` | twenty-five Shepard tones | step 12 equals step 0 exactly |
| `dose` | permitted hours against level | NIOSH (1998): 85 dBA, 8 h, 3 dB exchange |
| `active` | the response of a Hopf oscillator against force | slope 1/3 on a log-log plot |
| `tune` | Variation 4; the pitch model on each of its notes | every missing fundamental within 0.2 cents |
| `nextpart` | two strings at 2:3 and at 32:45 | (heard) |

Monochord's ear is held against its references in `tests/music/test_ear.py`; this part's claims and clips in
`tests/music/test_music4.py`.

**Sounds.** Sixteen clips, labelled on screen. `synthesized`: pure tones and sums of them (the two tones, the seven
octaves, the three pairs, the sweep, the equal-pressure tones, the masking test, the pitch pairs, the note with and
without its bottom, the shifted partials, the Tune in pure tones, Shepard's scale, the Variation). `physical
model`: Part 1's plucked string (the Tune's opening for the cochleagram, the note 10 dB apart, the two pairs of
strings at the end). There are no recordings. Three clips say that they need bass (they begin at 100 or 125 Hz).

**What the models are, and are not.** The cochlea is a one-dimensional long-wave model with a logarithmic map; its
place map is a straight line where Greenwood's bends below about 500 Hz, and the film shows both. The masking
pattern is the power-spectrum model with symmetric gammatone filters; measured masking spreads further upwards, and
the film says so. The "nerve" is a half-wave rectifier and a low-pass filter, which gives the right shape for the
loss of phase locking but is not a model of any particular species; the film says that the limit in humans has not
been measured directly. The Hopf oscillator is the normal form, not a cochlea. Whether a given viewer hears the
third tone depends on the playback level and on their loudspeakers, which also distort; the film gives a guide tone
and does not claim that everyone will.

**The ear thread.** Six pause-and-listen questions (chapters 3, 4, 5, 6, 7 and 9) and four demonstrations with
something to listen for (chapters 4, 7, 8 and 11): in this part the listener is the apparatus.

## Build

```bash
python -m videos.music.music4.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music4 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music4 --sync                         # the sound gates
python tools/dead_air.py renders/music4_480p.mp4 --sound music4   # no empty screen; no sound over a still one
python tools/lecture_length.py music4                          # 30 to 60 minutes, listening included
python tools/build.py music4                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 4                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A concert.** A concert measures 103 dBA where you stand. For how long is it safe? You put in earplugs that
   take off 15 dB: how long now, and by what factor did the time grow?

   *Solution.* 103 is 18 dB above 85, which is six steps of 3 dB, so the eight hours are halved six times:
   8 h / 64 = 7.5 minutes. With the plugs the level at the ear is 88 dBA, one step above 85: 4 hours. The factor
   is 2^(15/3) = 32. (The lab computes both.)

2. **The edge.** An amplifier's response is proportional to the cube root of the force. Show that 100 dB of input
   becomes 33 dB of output, and that its gain rises by 20 dB for every 30 dB that the sound falls.

   *Solution.* If x = k F^(1/3) then 20 log x = 20 log k + (1/3) · 20 log F: every decibel of input gives a third
   of a decibel of output, so 100 dB becomes 33.3 dB. The gain is x/F = k F^(−2/3), or in decibels
   20 log k − (2/3) · 20 log F: lower the input by 30 dB and the gain rises by 20 dB. A sound 90 dB weaker than
   another is amplified 60 dB more, which is the order of the cochlear amplifier's gain for the faintest sounds.

3. **Ear.** The lab (`python -m videos.music.labs 4`) plays a sound with partials at 900, 1200 and 1500 Hz, then
   pure tones at 300 and at 600 Hz in an order it prints afterwards. Which pure tone has its pitch? Then the three
   partials are moved up 50 Hz: does the pitch rise or fall?

   *Solution.* The partials are the third, fourth and fifth of 300 Hz, the largest frequency that divides all
   three, and the pure tone at 300 Hz matches. (Some listeners match the octave above, 600 Hz; the pitch of a
   residue is less definite than that of a full tone, and octave errors are the commonest.) Moved up 50 Hz the
   partials are 950, 1250 and 1550 Hz: no longer harmonics of anything near 300, but closest to the third, fourth
   and fifth partials of 1250/4 = 312.5 Hz. The pitch rises, by about 70 cents; Monochord's model says 313.1 Hz.

4. **Build.** Run `ear.pitch` on every note of Variation 4 and plot its errors. Then lower the model's limit on
   nerve timing (`corner`) from 1200 Hz to 600 Hz, and to 300 Hz. Which notes does it lose first?

   *Solution sketch.* The notes and their frequencies are in `load("tune")["checks"]`; each is partials 3 to 6 of
   its fundamental, and `ear.pitch(y, sr, lo=100, hi=700, corner=...)` takes the cutoff. With the standard 1200 Hz
   every note comes out within a fraction of a cent, with a salience between 0.28 and 0.56. At 600 Hz the model
   still finds the two lowest notes, C and D (partials from 785 Hz), with a salience below 0.2, and loses E, F, G
   and A, whose partials start above 980 Hz: the summary's peak at the period has sunk beneath a neighbouring
   ripple and the answer is about 660 cents off. At 300 Hz it loses all six, and no peak stands more than 0.04
   above the floor. That is the experiment of chapter 8 run on the model: the higher the partials, the more the
   pitch depends on the clock, and without the clock there is no pitch to find.

5. **★ Research.** Build a cochlear-implant simulator: a bank of N bands, each replaced by noise with the band's
   envelope. How many bands does Monochord's pitch model need to follow the Tune? What does that predict for
   implant users?

   *Pointers.* This is the noise vocoder of Shannon et al. (1995), who showed that speech survives with four
   bands. Pitch does not: with the fine timing replaced by noise, the autocorrelation model has only the envelope's
   periodicity, which is weak above about 300 Hz, and place cues as coarse as the bands. Compare your curve with
   melody recognition in implant users (McDermott, 2004; Limb and Roy, 2014). Open questions: whether coding the
   timing of low partials on a few electrodes (fine-structure strategies), or current steering between electrodes,
   restores a usable pitch, and how to measure it without relying on rhythm.

## Sources

Books: B. C. J. Moore, *An Introduction to the Psychology of Hearing* (6th ed., 2012); C. J. Plack, *The Sense of
Hearing* (3rd ed., 2018); J. O. Pickles, *An Introduction to the Physiology of Hearing* (4th ed., 2012), for the
anatomy (eardrum about 55 mm² effective, stapes footplate 3.2 mm², lever 1.3; about 3,500 inner and 12,000 outer
hair cells; about 30,000 nerve fibres); W. M. Hartmann, *Signals, Sound, and Sensation* (1997); G. von Békésy,
*Experiments in Hearing* (1960).

Papers: H. von Helmholtz, *On the Sensations of Tone* (1863); G. Tartini, *Trattato di musica* (1754), for the
third sound; A. Seebeck, *Annalen der Physik* 53 (1841); E. G. Wever and C. W. Bray, "Action currents in the
auditory nerve in response to acoustical stimulation", *PNAS* 16 (1930); H. Fletcher and W. A. Munson, "Loudness,
its definition, measurement and calculation", *JASA* 5 (1933); S. S. Stevens, "A scale for the measurement of a
psychological magnitude: loudness", *Psychological Review* 43 (1936); H. Fletcher, "Auditory patterns", *Reviews of
Modern Physics* 12 (1940); J. F. Schouten, "The residue, a new component in subjective sound analysis", *Proc. KNAW*
43 (1940); T. Gold, "Hearing. II. The physical basis of the action of the cochlea", *Proc. R. Soc. B* 135 (1948);
J. C. R. Licklider, "A duplex theory of pitch perception", *Experientia* 7 (1951), and "'Periodicity' pitch and
'place' pitch", *JASA* 26 (1954); R. N. Shepard, "Circularity in judgments of relative pitch", *JASA* 36 (1964);
J. E. Rose et al., "Phase-locked response to low-frequency tones in single auditory nerve fibers of the squirrel
monkey", *J. Neurophysiol.* 30 (1967); F. Attneave and R. K. Olson, "Pitch as a medium", *American Journal of
Psychology* 84 (1971); W. S. Rhode, "Observations of the vibration of the basilar membrane in squirrel monkeys
using the Mössbauer technique", *JASA* 49 (1971); D. T. Kemp, "Stimulated acoustic emissions from within the human
auditory system", *JASA* 64 (1978); D. H. Johnson, "The relationship between spike rate and synchrony in responses
of auditory-nerve fibers to single tones", *JASA* 68 (1980); W. E. Brownell et al., "Evoked mechanical responses of
isolated cochlear outer hair cells", *Science* 227 (1985); D. D. Greenwood, "A cochlear frequency-position function
for several species: 29 years later", *JASA* 87 (1990); B. R. Glasberg and B. C. J. Moore, "Derivation of auditory
filter shapes from notched-noise data", *Hearing Research* 47 (1990); E. Terhardt, "Calculating virtual pitch",
*Hearing Research* 1 (1979), for the threshold formula; J. Zheng et al., "Prestin is the motor protein of cochlear
outer hair cells", *Nature* 405 (2000); S. Camalet, T. Duke, F. Jülicher and J. Prost, "Auditory sensitivity
provided by self-tuned critical oscillations of hair cells", *PNAS* 97 (2000); V. M. Eguíluz et al., "Essential
nonlinearities in hearing", *PRL* 84 (2000); S. G. Kujawa and M. C. Liberman, "Adding insult to injury: cochlear
nerve degeneration after 'temporary' noise-induced hearing loss", *J. Neurosci.* 29 (2009); F.-G. Zeng,
"Celebrating the one millionth cochlear implant", *JASA Express Letters* 2 (2022); J. Lv et al., "AAV1-hOTOF gene
therapy for autosomal recessive deafness 9", *The Lancet* 403 (2024).

Standards and reports: NIOSH, *Criteria for a Recommended Standard: Occupational Noise Exposure* (1998); ISO 226
(equal-loudness contours); IEC 61672 (the A weighting); World Health Organization, *World Report on Hearing* (2021)
and its "Make Listening Safe" initiative, for the estimate of over a billion young people at risk.
