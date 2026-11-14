# Psychology, Built: Part 15, The Other Senses

A sound made of six harmonics of 200 Hz is heard as one note at 200 Hz. Take the 200 and the 400 away, so that there
is no energy at all at 200 Hz, and most people still hear 200 Hz: the missing fundamental, the reason a telephone
voice keeps its pitch. The film plays it, and then explains it.

This part covers everything after the eye. Sound in physics' units, and the decibel as Fechner's logarithm made into a
unit; the threshold of hearing by frequency. The cochlea: the eardrum's pressure gain, von Békésy's travelling wave in
cadaver cochleas, Greenwood's place map, Kemp's echoes and the outer hair cells' amplifier, and Psyche's bank of
gammatone filters. Masking: Fletcher's band-widening experiment and the critical band. Pitch: Seebeck, Ohm and
Schouten's residue, phase locking, and Licklider's summary autocorrelation, which finds the missing fundamental. Where
a sound is: the duplex theory, Woodworth's interaural delays, Jeffress's coincidence circuit run in Psyche, and the
owl-versus-gerbil story. Auditory scene analysis, with a streaming demonstration to hear. Speech: no acoustic
invariant, categorical perception and its correction, the McGurk effect as cue combination and its wide individual
differences. Music: roughness from the cochlea, consonance at simple ratios, and the Tsimane'. Touch's four channels,
two-point thresholds, proprioception and the rubber hand; pain from Descartes's bell rope to Melzack and Wall's gate,
run as a circuit, phantom limbs and placebo; smell's combinatorial code, the tongue map and the trillion smells; the
vestibular sense and motion sickness. The practice chapter is hearing aids, cochlear implants, codecs and haptics; the
frontier is hidden hearing loss, chronic pain as learning, and the mismatch negativity. Act III ends here.

## Where the numbers come from

| What | Source |
|---|---|
| Harmonic complexes of 200 Hz, with and without the first two harmonics; a 200 Hz tone; the streaming sequences (500 and 560 Hz, then 500 and 1000 Hz); a fifth (220 and 330 Hz) and a tritone (220 and 311 Hz), each with six harmonics | Psyche (`compute.py`, item `sounds`), played in the film |
| A classic telephone line passes roughly 300 to 3400 Hz | the usual account |
| 0 dB SPL = 20 µPa; 130 dB is about 3.2 million times the pressure; typical levels of everyday sounds | definitions; the levels are approximate, as usually tabulated |
| Loudness doubles about every 10 dB | Stevens, as in Part 11 |
| Threshold in quiet: most sensitive near 3.3 kHz (−5 dB SPL), about 40 dB at 50 Hz, 3.4 dB at 1 kHz | Terhardt's (1979) formula, as used in perceptual coders |
| A pressure gain of about twenty from eardrum to oval window; a basilar membrane about 35 mm long; about 3,500 inner and 12,000 outer hair cells | textbook values |
| Cadaver cochleas, strobe light, silver flakes; a wave peaking at a place set by frequency; Nobel Prize 1961 | von Békésy (1960) and reviews |
| Greenwood's map f = 165.4(10^2.1x − 0.88): 250, 1000 and 4000 Hz at 0.18, 0.40 and 0.67 of the length from the apex | Greenwood (1990); computed |
| Emissions from the ear | Kemp (1978) |
| Outer hair cells change length with voltage; prestin; 40 to 60 dB of sensitivity lost without it | Brownell et al. (1985); Zheng et al. (2000); Liberman et al. (2002), from reviews |
| Newborn hearing screening by otoacoustic emissions | the usual account |
| ERB(f) = 24.7(4.37f/1000 + 1): 133 Hz at 1 kHz, 456 Hz at 4 kHz; 48 gammatone filters from 80 Hz to 7 kHz | Glasberg and Moore (1990); Psyche (`hearing.filterbank`) |
| Band-widening at 2 kHz; the knee at one ERB, 241 Hz | Fletcher (1940), the power-spectrum model computed |
| Seebeck's sirens (1841); Ohm's law of hearing; Schouten's residue (1940) | the usual history |
| Phase locking up to about 4 to 5 kHz; melodies hard above about 5 kHz | textbook values |
| Summary autocorrelation finds 200 Hz for harmonics 1–6, 3–6 and 5–8 | Licklider (1951); Meddis and Hewitt (1991); Psyche (`hearing.pitch`) |
| Interaural delay up to 656 µs; 261 µs at 30°; thresholds near 10 µs | Woodworth's formula, r = 8.75 cm; the threshold as usually quoted |
| The duplex theory | Rayleigh (1907) |
| A Jeffress array: a 500 Hz tone from 30°, 3 s of phase-locked spikes; the busiest detector at 275 µs, 32° | Jeffress (1948); Psyche (`hearing.jeffress`) |
| Owls fit Jeffress; in gerbils precisely timed glycinergic inhibition shifts best delays | Carr and Konishi (1990), from memory; Brand et al. (2002) |
| Recordings through someone else's ears increase front-back confusions | the usual account |
| The cocktail party; auditory scene analysis; the streaming boundary | Cherry (1953); Bregman (1990); van Noorden (1975) |
| The /d/ of "di" and "du"; the pattern playback | Liberman and colleagues at Haskins, schematic |
| A /b/–/d/ continuum: identification by a logistic, ABX predicted from labels, peak 0.69 | Liberman et al. (1957); Psyche (`hearing.identification`, `hearing.abx_from_labels`) |
| Gradient sensitivity within categories, by eye tracking | McMurray, Tanenhaus and Aslin (2002) |
| Voice ba on lips ga: 98% of adults report da or a blend | McGurk and MacDonald (1976), as widely reported |
| Psyche with equal reliabilities: 6% b, 88% d, 6% g | Psyche (`hearing.mcgurk`) |
| Individuals from 0% to 100%, stable over a year | Mallick, Magnotti and Beauchamp (2015) |
| 300 simulated listeners: median 27% fused; 26% almost never and 6% almost always; the model says ga on 35% of trials | Psyche (`compute.py`, item `speech`) |
| Roughness of two tones; dips at 6:5, 5:4, 4:3, 3:2, 5:3 and 2:1 for six-harmonic tones | Plomp and Levelt (1965), in Sethares's form, computed |
| The Tsimane' rate consonant and dissonant chords equally pleasant; roughness still disliked | McDermott et al. (2016) |
| Four mechanoreceptor types; about 17,000 fibres from each hand | textbook; Johansson and Vallbo (1979), from memory |
| Two-point thresholds: fingertip 2 to 3 mm, back about 39 mm, calf about 45 mm | as usually tabulated from Weinstein (1968) |
| Tendon vibration makes the arm feel straighter | Goodwin, McCloskey and Matthews (1972) |
| The rubber hand; 353 people and suggestibility | Botvinick and Cohen (1998); Lush et al. (2020) |
| The bell rope | Descartes, *L'Homme* (1664) |
| Wounded soldiers asked for less relief | Beecher (1946), from later accounts |
| The 2020 definition of pain | the International Association for the Study of Pain |
| The gate, as a circuit: T for an injury of 1 is 1.00 alone and 0.44 while rubbing | Melzack and Wall (1965); Psyche (`hearing.gate`), parameters chosen |
| The mirror box | Ramachandran and Rogers-Ramachandran (1996) |
| Naloxone undoes placebo relief after wisdom-tooth removal | Levine, Gordon and Fields (1978) |
| Odorant receptor genes, about a thousand in rodents and about 400 working in people; Nobel Prize 2004 | Buck and Axel (1991) and later counts |
| The tongue map from Hänig's small differences; every region tastes every taste | Hänig (1901); Boring (1942); Collings (1974) |
| Mixtures of 10, 20 or 30 from 128 odorants; 26 people; at least 1.72 trillion; the reanalyses | Bushdid et al. (2014); Gerkin and Castro (2015); Meister (2015) |
| A count of mixtures of 30 from 128, each with a private neighbourhood: 62, 2.0 million and 2.4 × 10^14 at overlap thresholds of 40%, 60% and 80% | Psyche (`hearing.bushdid_estimate`); one natural way to count, not the paper's exact formula |
| The vestibulo-ocular reflex, about 10 ms | textbook value |
| Sensory conflict | Reason and Brand (1975) |
| About 736,900 cochlear implants registered worldwide by December 2019 | the US National Institute on Deafness and Other Communication Disorders, as quoted |
| CD at 1,411 kbit/s; MP3 at 128 to 256 kbit/s | standard rates |
| Mice, two hours of noise: thresholds recover, synapses do not | Kujawa and Liberman (2009); later reviews |
| The mismatch negativity | Näätänen, Gaillard and Mäntysalo (1978), from memory |

## Built in this part

* `explainer/psychology/psyche/hearing.py`: decibels and Terhardt's threshold in quiet; harmonic complexes and spectra;
  the ERB scale, Greenwood's map, gammatone filters, a filter bank, hair cells, excitation patterns and a schematic
  travelling wave; summary autocorrelation and its pitch; the power-spectrum model of masking; Woodworth's interaural
  delay, phase-locked spikes and a Jeffress array; categorical identification and the label model of ABX; the McGurk
  effect as cue combination; Melzack and Wall's gate as a circuit; a model nose and a combinatorial count of
  discriminable mixtures. Tested in `tests/psychology/test_hearing.py`.
* `explainer/voiceover.py`: `VoiceoverScene.sound`, so a scene can play a demonstration the viewer hears.
* The Ledger gains six rows and the Archive fourteen datasets.
* The course's interactive plays pairs of tones whose missing fundamental moves one way and whose harmonics move the
  other, and reports which the reader follows.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A voice saying one syllable on lips saying another is often heard as a third | McGurk and MacDonald 1976 | replicated |
| Discrimination of speech sounds peaks at the phoneme boundary | Liberman, Harris, Hoffman and Griffith 1957 | story and record |
| The body is mapped in order on the cortex, the hands and face magnified | Penfield and Boldrey 1937 | replicated |
| Synchronous stroking makes a rubber hand feel like one's own | Botvinick and Cohen 1998 | contested |
| Different parts of the tongue taste different tastes | Hänig 1901 | story and record |
| People can discriminate more than a trillion smells | Bushdid, Magnasco, Vosshall and Keller 2014 | contested |

The first row's note records the wide differences between people; the third is the row Part 7 deferred to this part
(Roux, Djidjeli and Durand 2018; Gordon et al. 2023). Shown without a row, with the reason recorded in
`explainer/psychology/ledger.py`: von Békésy (the history of a measurement), Kemp (a discovery told as history), Melzack
and Wall (a theory, modelled), Levine, Gordon and Fields (placebo analgesia is entered in Part 57), McDermott et al. (one
cross-cultural study, with its limits) and Kujawa and Liberman (an animal result at the frontier).

## Build it

```bash
python -m videos.psychology.psych15.compute            # every number and every sound (seconds), into .cache/psych15/
python tools/qa_scene.py psych15 Pitch                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych15 -q l   # the whole part, silent preview (the demonstrations still play)
python tools/build.py psych15                          # 1080p30 with narration
python tools/qa_scene.py psych15 Pitch --lang zh       # the Chinese edition of one chapter
python tools/make.py psych15                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 15                    # the lab: filters, pitch, delays, gates
python tools/check_ledger.py psych15                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's hearing module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A pitch that is not there | Six harmonics, heard; the fundamental removed, the pitch kept; a 200 Hz tone; objectives |
| 1 | Sound, and the decibel | A pressure wave; the decibel ladder as Fechner's law; the threshold in quiet and the audiogram |
| 2 | The cochlea | From air to fluid; von Békésy's travelling wave; Greenwood's map; the amplifier; Psyche's filter bank |
| 3 | Filters and masking | Fletcher's band-widening and the critical band; upward spread; what masking is for |
| 4 | Pitch | Seebeck, Ohm and the residue; phase locking; summary autocorrelation; place and time together |
| 5 | Where is it? | Time and level cues; Jeffress's circuit; Psyche's array; owls and gerbils; the outer ear |
| 6 | Auditory scene analysis | One wave from many sources; streaming, heard; Bregman's grouping cues |
| 7 | Speech | No invariant; categorical perception; the story corrected; the McGurk effect as cue combination; individual differences |
| 8 | Music | Roughness and the simple ratios; a fifth and a tritone, heard; the Tsimane' |
| 9 | Touch and the body | Four channels; two-point thresholds; proprioception; the rubber hand |
| 10 | Pain | The bell rope; the gate as a circuit; why rubbing helps; phantom limbs and placebo |
| 11 | Smell and taste | A combinatorial code; flavour and the tongue map; a trillion smells; how fragile the count is |
| 12 | Balance, and the senses together | The vestibular sense; sensory conflict and motion sickness |
| 13 | The Ledger | McGurk; categorical perception; the homunculus; the rubber hand; the tongue map; a trillion smells |
| 14 | In practice: hearing aids, codecs and haptics | Compression; cochlear implants; perceptual coding; touch engineered |
| 15 | Frontier: hidden losses and learned pain | What is solid and argued; hidden hearing loss; chronic pain; the mismatch negativity |
| | Recap, problems, and the road ahead | Ten lines; the first and third objections; payoffs; problems; references; Part 16 |

## Sources

**Books.** B. C. J. Moore, *An Introduction to the Psychology of Hearing*, 6th ed. (Brill, 2012). A. S. Bregman,
*Auditory Scene Analysis* (MIT Press, 1990). J. M. Wolfe et al., *Sensation & Perception* (Sinauer/Oxford). G. von
Békésy, *Experiments in Hearing* (McGraw-Hill, 1960). J. T. Reason and J. J. Brand, *Motion Sickness* (Academic Press,
1975). E. G. Boring, *Sensation and Perception in the History of Experimental Psychology* (1942).

**Papers.** H. Fletcher, Auditory patterns, *Rev. Mod. Phys.* 12 (1940) 47–65. E. Terhardt, Calculating virtual pitch,
*Hear. Res.* 1 (1979) 155–182. D. D. Greenwood, A cochlear frequency-position function for several species—29 years
later, *J. Acoust. Soc. Am.* 87 (1990) 2592–2605. D. T. Kemp, Stimulated acoustic emissions from within the human
auditory system, *J. Acoust. Soc. Am.* 64 (1978) 1386–1391. W. E. Brownell, C. R. Bader, D. Bertrand and Y. de
Ribaupierre, Evoked mechanical responses of isolated cochlear outer hair cells, *Science* 227 (1985) 194–196. B. R.
Glasberg and B. C. J. Moore, Derivation of auditory filter shapes from notched-noise data, *Hear. Res.* 47 (1990)
103–138. J. F. Schouten, The residue and the mechanism of hearing, *Proc. K. Ned. Akad. Wet.* 43 (1940) 991–999. J. C.
R. Licklider, A duplex theory of pitch perception, *Experientia* 7 (1951) 128–134. R. Meddis and M. J. Hewitt,
Virtual pitch and phase sensitivity of a computer model of the auditory periphery, *J. Acoust. Soc. Am.* 89 (1991)
2866–2882. Lord Rayleigh, On our perception of sound direction, *Phil. Mag.* 13 (1907) 214–232. L. A. Jeffress, A place
theory of sound localization, *J. Comp. Physiol. Psychol.* 41 (1948) 35–39. C. E. Carr and M. Konishi, A circuit for
detection of interaural time differences in the brain stem of the barn owl, *J. Neurosci.* 10 (1990) 3227–3246. A.
Brand, O. Behrend, T. Marquardt, D. McAlpine and B. Grothe, Precise inhibition is essential for microsecond interaural
time difference coding, *Nature* 417 (2002) 543–547. E. C. Cherry, Some experiments on the recognition of speech, with
one and with two ears, *J. Acoust. Soc. Am.* 25 (1953) 975–979. L. P. A. S. van Noorden, *Temporal coherence in the
perception of tone sequences* (thesis, Eindhoven, 1975). A. M. Liberman, K. S. Harris, H. S. Hoffman and B. C.
Griffith, The discrimination of speech sounds within and across phoneme boundaries, *J. Exp. Psychol.* 54 (1957)
358–368. B. McMurray, M. K. Tanenhaus and R. N. Aslin, Gradient effects of within-category phonetic variation on
lexical access, *Cognition* 86 (2002) B33–B42. H. McGurk and J. MacDonald, Hearing lips and seeing voices, *Nature* 264
(1976) 746–748. D. B. Mallick, J. F. Magnotti and M. S. Beauchamp, Variability and stability in the McGurk effect,
*Psychon. Bull. Rev.* 22 (2015) 1299–1307. R. Plomp and W. J. M. Levelt, Tonal consonance and critical bandwidth, *J.
Acoust. Soc. Am.* 38 (1965) 548–560. W. A. Sethares, Local consonance and the relationship between timbre and scale,
*J. Acoust. Soc. Am.* 94 (1993) 1218–1228. J. H. McDermott, A. F. Schultz, E. A. Undurraga and R. A. Godoy,
Indifference to dissonance in native Amazonians reveals cultural variation in music perception, *Nature* 535 (2016)
547–550. R. S. Johansson and Å. B. Vallbo, Tactile sensibility in the human hand, *J. Physiol.* 286 (1979) 283–300. S.
Weinstein, Intensive and extensive aspects of tactile sensitivity, in D. R. Kenshalo (ed.), *The Skin Senses* (1968).
G. M. Goodwin, D. I. McCloskey and P. B. C. Matthews, The contribution of muscle afferents to kinaesthesia shown by
vibration induced illusions of movement, *Brain* 95 (1972) 705–748. M. Botvinick and J. Cohen, Rubber hands 'feel'
touch that eyes see, *Nature* 391 (1998) 756. W. Penfield and E. Boldrey, Somatic motor and sensory representation in
the cerebral cortex of man as studied by electrical stimulation, *Brain* 60 (1937) 389–443. F.-E. Roux, I. Djidjeli and
J.-B. Durand, Functional architecture of the somatosensory homunculus detected by electrostimulation, *J. Physiol.* 596
(2018) 941–956. E. M. Gordon et al., A somato-cognitive action network alternates with effector regions in motor
cortex, *Nature* 617 (2023) 351–359. P. Lush et al., Trait phenomenological control predicts experience of
mirror synaesthesia and the rubber hand illusion, *Nat. Commun.* 11 (2020) 4853. H. K. Beecher, Pain in men wounded in
battle, *Ann. Surg.* 123 (1946) 96–105. R. Melzack and P. D. Wall, Pain mechanisms: a new theory, *Science* 150 (1965)
971–979. V. S. Ramachandran and D. Rogers-Ramachandran, Synaesthesia in phantom limbs induced with mirrors, *Proc. R.
Soc. B* 263 (1996) 377–386. J. D. Levine, N. C. Gordon and H. L. Fields, The mechanism of placebo analgesia, *Lancet* 2
(1978) 654–657. L. Buck and R. Axel, A novel multigene family may encode odorant receptors, *Cell* 65 (1991) 175–187.
D. P. Hänig, Zur Psychophysik des Geschmackssinnes, *Philos. Stud.* 17 (1901) 576–623. V. B. Collings, Human taste
response as a function of locus of stimulation on the tongue and soft palate, *Percept. Psychophys.* 16 (1974)
169–174. C. Bushdid, M. O. Magnasco, L. B. Vosshall and A. Keller, Humans can discriminate more than 1 trillion
olfactory stimuli, *Science* 343 (2014) 1370–1372. R. C. Gerkin and J. B. Castro, The number of olfactory stimuli that
humans can discriminate is still unknown, *eLife* 4 (2015) e08127. M. Meister, On the dimensionality of odor space,
*eLife* 4 (2015) e07865. S. G. Kujawa and M. C. Liberman, Adding insult to injury, *J. Neurosci.* 29 (2009)
14077–14085. R. Näätänen, A. W. K. Gaillard and S. Mäntysalo, Early selective-attention effect on evoked potential
reinterpreted, *Acta Psychol.* 42 (1978) 313–329.

## Problems and solutions

**1. Decibels.** 20 log₁₀ 10 = 20 dB for ten times the pressure; intensity goes as pressure squared, so ten times the
intensity is 10 log₁₀ 10 = 10 dB. Two unrelated sources add in intensity: two equal 60 dB sources give 60 + 10 log₁₀ 2
= 63 dB, not 120.

**2. The ear's filters.** ERB(500) = 24.7 × (2.185 + 1) = 78.7 Hz; ERB(4000) = 24.7 × (17.48 + 1) = 456 Hz. The
ERB-rate is 21.4 log₁₀(4.37f/1000 + 1): 3.37 at 100 Hz and 33.3 at 8 kHz, so about 30 ERBs, about thirty
independent-ish channels, span the range of speech.

**3. Two ears.** At 90°, (0.0875/343)(π/2 + 1) = 2.55 × 10⁻⁴ × 2.571 = 656 µs. For small angles θ + sin θ ≈ 2θ, so
10 µs gives θ ≈ 10⁻⁵/(2 × 2.55 × 10⁻⁴) = 0.0196 rad ≈ 1.1°: about a degree, which is roughly the best directional
acuity measured straight ahead.

**4. The missing fundamental.** Each component sin(2πnf₀t + φₙ) has period 1/(nf₀), which divides 1/f₀, so the sum
repeats every 1/f₀ whichever harmonics are present. The autocorrelation of any signal with period T is maximal (equal
to its value at zero lag) at every multiple of T, and in each filter's output the same holds, so the summary peaks at
1/f₀ even when no filter is tuned to f₀.

**5. The label model.** Let X be A (the case X = B is symmetric). Each presentation receives a covert label, category
2 with probability p_A, p_B or p_A. If A and B get different labels, the listener chooses the one whose label matches
X's; if the same, a coin is tossed. P(correct) = p_A²(1 − p_B) + (1 − p_A)²p_B + ½[p_Ap_B + (1 − p_A)(1 − p_B)], which
simplifies to ½[1 + (p_A − p_B)²]: a half when the labels are equally likely, one when they are certain and different.

**6. The gate.** With w_L = 0.3, w_S = 1, k = 0.5, g = 3 and S = 1, T = (0.3L + 1)/(1 + 3(L − 0.5)) for L > 0.5. Setting
T = 0.5 gives 0.3L + 1 = 1.5L − 0.25, so L ≈ 1.04. With g = 6, 0.3L + 1 = 3L − 1, so L ≈ 0.74: a stronger gate needs
less rubbing.

**7. ★ Hearing or reporting.** If the McGurk effect only changed responses, a visual ga would shift the criterion for
saying da without changing sensitivity. Use detection theory (Part 12): present audio da and audio ba, each with a
face saying ga or a still face, and ask "da or not?" with confidence ratings. A perceptual effect lowers d′ between
audio ba and audio da when the ga face is present (the two sounds become alike), while a pure response bias moves c
and leaves d′ unchanged. Add trials where the face is shown after the sound, too late to change hearing: any effect
there is a reporting effect.

## Where it comes back

Conditioning: Part 16. Prediction errors: Part 17. Attention and the cocktail party: Part 18. Speech and language:
Part 23. Hearing aids, alarms and the human in the loop: Part 51. Pain and placebo in the clinic: Part 57. The
predictive brain: Part 58. Psyche's `hearing` module supplies the filter bank, the pitch model and the gate those
parts use.

## Open checks

Before the narrated master:

* The levels of everyday sounds, the pressure gain of the middle ear, the membrane's length and the hair-cell counts
  are textbook values, approximate.
* Von Békésy's methods (silver flakes, strobe light, cadaver temporal bones) are from reviews.
* Brownell (1985), prestin (2000) and the 40 to 60 dB loss are from reviews.
* Schouten's residue at Philips (1940) and Seebeck's sirens (1841) are the usual history.
* The 10 µs ITD threshold and the 4 to 5 kHz limit of phase locking are standard values.
* Carr and Konishi (1990) is cited from memory; Brand et al. (2002) from the abstract.
* McGurk and MacDonald's 98% is as widely reported; the children's rates are not stated on screen.
* Two-point thresholds are as tabulated in teaching sources from Weinstein (1968).
* Johansson and Vallbo's 17,000 fibres is from memory.
* Beecher's comparison of soldiers and civilians is described without numbers.
* Human olfactory receptor counts vary between about 350 and 400 by source; "about 400" is used.
* Bushdid et al.: 26 participants as usually reported.
* The cochlear-implant count (736,900 by December 2019) is the NIDCD figure as quoted by secondary sources.
* The mismatch negativity citation (Näätänen et al. 1978) is from memory.
