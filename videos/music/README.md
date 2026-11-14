# Music, Built (音乐，从零搭建)

A sixty-eight-part course on music, planned to the standard of *Computer Science, Built* and *Statistics, Built*.
It covers a music degree, a music-technology degree, the first years of a doctorate, and the working knowledge of
the industry:
- **sound**: the physics of strings, pipes and drums, the ear, and why some sounds go together;
- **notes**: notation, rhythm, scales, chords, melody and key;
- **voices**: counterpoint, harmony, fugue, form and analysis;
- **history**: a thousand years of Western art music, each era taken as a technical problem and its solution;
- **after tonality**: the twentieth century, and the mathematics of music (sets, groups, geometry, tilings);
- **many musics**: raga, maqam, the musics of East and Southeast Asia, African timelines, blues, jazz and song;
- **the craft**: orchestration, composition, performance, and music for film and games;
- **the mind**: auditory scenes, expectation and emotion, the origins and universals of music;
- **electric sound**: digital audio, effects, synthesis, MIDI and the workstation;
- **the studio and the stage**: transducers, rooms, recording, mixing, mastering, codecs, live sound, the business;
- **listening machines**: transcription, beat and chord tracking, fingerprinting and recommendation, source
  separation, and models that write and render music;
- **the research frontier**: a *Frontier* chapter in every part, and a closing part on how music research is done.

Each part is a 30–60 minute lecture with a story. It derives its mathematics on screen, tells its history, builds
something that runs, and plays what it builds. Two rules hold for every minute:

1. **Everything you hear, you see, and everything you see, you can hear.** A sound never plays without a picture
   locked to it (a waveform, a spectrogram, a score with a playhead, a string in motion), and the picture is drawn
   from the same samples that go to the soundtrack.
2. **Every sound is a computed result.** The series plays no third-party recordings as music. Its sounds come from
   its own engine, rendered from public-domain scores or from material written for the series, by the part's
   `compute.py`. Numbers follow the rule of the other series: a computation, a measurement or a cited source.

The videos are `music1` … `music68`. The standard, the devices, the sound pipeline and the part-by-part plan
are in [`SYLLABUS.md`](SYLLABUS.md).

**Status (2026-11-13):** production runs on the plan's proposed defaults (the Tune is *Ah! vous dirai-je, maman*;
the rights rule as written; sixty-eight parts; English first; see [`SYLLABUS.md`](SYLLABUS.md) §9). Phase 0, the sound pipeline, is built and proven on
a test film (`videos/music/soundcheck/`). **Part 1, *One String*, is built**: fifteen chapters, 47 minutes narrated, with its
lab, its interactive and its problem set ([`music1/README.md`](music1/README.md)). How a part is made, with the
lessons of this pilot, is [`LECTURE_GUIDE.md`](LECTURE_GUIDE.md). **Parts 2 to 9 are built** too, which completes Act I: *Waves in Air* (34 minutes; [`music2/README.md`](music2/README.md)), *The Spectrum* (33 minutes;
[`music3/README.md`](music3/README.md)), *The Ear* (48 minutes; [`music4/README.md`](music4/README.md)), *Consonance* (39 minutes;
[`music5/README.md`](music5/README.md)), *Tuning* (37 minutes; [`music6/README.md`](music6/README.md)), *Strings, Hammers and Bows* (39 minutes;
[`music7/README.md`](music7/README.md)), *Pipes, Reeds and Voices* (41 minutes; [`music8/README.md`](music8/README.md)) and *Drums, Bars and Bells* (34 minutes;
[`music9/README.md`](music9/README.md)). **Act II has begun** with Part 10, *Writing It Down* (38 minutes;
[`music10/README.md`](music10/README.md)) Part 11, *Rhythm and Meter* (32 minutes; [`music11/README.md`](music11/README.md)), Part 12, *Scales and Modes* (32 minutes;
[`music12/README.md`](music12/README.md)) and Part 13, *Intervals and Chords* (40 minutes; [`music13/README.md`](music13/README.md)); the running record is [`SYLLABUS.md`](SYLLABUS.md) §8.

## The story

**A string.** The oldest experiment in science is a musical one. Stop a stretched string at half its length and it
sounds an octave higher; at two thirds, a fifth. The Pythagoreans built a cosmos on that, and the question they
left has been open for 2,500 years: *why do simple ratios sound good?* Mersenne measured the string, Sauveur found
its overtones, Fourier gave them a mathematics, Helmholtz put the answer in the ear, and in 2016 an experiment in
the Bolivian Amazon suggested that part of the answer is not in the ear at all. This series follows the string
from a single wire to an orchestra, a studio, a streaming service and a model that writes songs. Each act puts a
new question to it:

* **Act I, Sound (1–9).** *What is a musical sound, and why do some sounds go together?* The string, the air, the
  spectrum, the ear, consonance and tuning; then the instruments, family by family, as physics.
* **Act II, Notes (10–15).** *How did sound become something you can write down?* Notation, rhythm and meter,
  scales, chords, melody, and key as a thing in the listener.
* **Act III, Voices (16–22).** *How do many notes move together?* Counterpoint derived from how hearing groups
  sounds, four-part harmony, chromatic harmony, canon and fugue, form, and analysis as parsing.
* **Act IV, A Thousand Years (23–27).** *How did Europe get from one line of chant to a Mahler symphony?* Five eras,
  each a technical problem: writing rhythm, printing counterpoint, inventing the bass, staging a key, stretching it.
* **Act V, After Tonality (28–33).** *What is left when the key goes, and what does mathematics see in music?* New
  scales and rhythms, twelve tones, sound itself as material; then transformations, the geometry of chords, and
  the combinatorics of rhythm and scale.
* **Act VI, Many Musics (34–40).** *What do the world's other answers look like?* Raga and tala, maqam, the bells
  and gongs of Asia, African timelines, the blues and swing, jazz changes, and the song from Tin Pan Alley to the
  drop.
* **Act VII, The Craft (41–44).** *How is a piece actually made and played?* Orchestration, composing, performing,
  and writing for picture and for play.
* **Act VIII, The Mind (45–47).** *What does a listener do?* The auditory scene, expectation and emotion, and where
  music comes from.
* **Act IX, Electric Sound (48–53).** *How do numbers become sound?* Sampling, filters and reverb, dynamics and
  pitch processing, two parts of synthesis, MIDI and the workstation.
* **Act X, The Studio and the Stage (54–60).** *How does music reach a million ears, and who gets paid?*
  Microphones and loudspeakers, rooms and space, recording and mixing, mastering, codecs, live sound, the business.
* **Act XI, Listening Machines (61–66).** *Can a machine hear, and can it write?* Transcription, beat and chords,
  finding music, source separation, symbolic generation, generative audio.
* **Act XII, Coda (67–68).** *How does the field know what it knows, and what did we build?* Research methods and
  the open problems; then the Variations, performed.

Every part ends on the question the next part answers. Every act ends on the limit the next act gets past.

Four devices hold the series together.

1. **Monochord** (`explainer/music/monochord/`): the instrument the series builds, in code. It starts in Part 1 as
   one simulated string and each part adds the layer it teaches:
   - the physics: strings, tubes, membranes, bars and bells by finite differences and modes; a cochlea model;
   - the theory: pitch, tuning, score, rhythm, scale, chord and key modules; counterpoint and voice-leading
     checkers; a harmonizer; a canon solver; a grammar parser; the transformational and geometric tools;
   - the instruments: bowed, plucked and struck strings, reeds, brass, a singing voice, tuned percussion;
   - the electronics: oscillators, filters, envelopes, FM, grains, waveguides, effects, a sequencer and audio graph;
   - the studio: virtual microphones and loudspeakers, rooms, a mixer, a mastering chain with a loudness meter, a
     lossless and a perceptual codec, a PA and feedback simulator;
   - the listeners: pitch and onset detection, transcription, beat and chord tracking, a fingerprinter, a
     recommender, a separator, and small generative models.

   Each layer is checked against something that does not share its code: closed-form solutions, `scipy.signal`,
   published measurements and standards (ISO 226, ITU-R BS.1770 against ffmpeg's meter), public instrument samples
   and head-related transfer functions, and scores whose analysis is known.
2. **The Tune and the Variations** (`explainer.music.variations`): one melody carried through every part. The Tune
   is *Ah! vous dirai-je, maman* (France, published 1761), which the world sings as *Twinkle, Twinkle, Little
   Star* and on which Mozart wrote twelve variations. It opens on a rising fifth, the 3:2 of Part 1. Every part
   writes one variation with what it has just taught: on one string, in eight temperaments, as a species
   counterpoint, a chorale, a fugue, an isorhythmic motet, a twelve-tone row, a raga elaboration, a bebop head, a
   pop single, a film cue, an FM patch, a mix, a master at 32 kbit/s, a transcription, a model's continuation.
   Each variation adds a row to the ledger: the score, the rendered audio, and what was measured. The finale
   performs them.
3. **The Chain** (`explainer.music.chain`): the path a piece of music travels, drawn on every chapter card with the
   part's links lit: *mind → score → hands → instrument → air → ear → mind*, and the industrial detour through
   *microphone → mix → master → codec → stream*. Beside it runs the timeline strip (from the Hohle Fels flute to
   2030, on a compressed scale). Payoff cards link ideas forward; each part closes with an *In practice* card.
4. **The Library** (`explainer/music/library/`): the series' sources, with their provenance and rights recorded per
   item. Public-domain scores as data (Bach's chorales and *Well-Tempered Clavier*, Mozart's K. 265, folk-tune
   collections, Joplin's rags), and measured references (instrument samples, HRTFs, equal-loudness contours,
   published tunings of gamelans and maqam performances).

## How it looks and sounds

The series draws in the manner of 3Blue1Brown with the lecture set pieces of `explainer.ai.lecture`, plus its own
instruments in `explainer/music/`:

* **The playhead is always visible.** When sound plays, something on screen moves with it: a cursor on the staff, a
  bead on the string, a column on the spectrogram.
* **One sound, many pictures.** The same four bars are shown as a score, a piano roll, a spectrogram, a path on the
  Tonnetz and a path in chord space, and the camera moves between them without the sound stopping.
* **Continuity.** A waveform unrolls into its spectrum. A polyrhythm speeds up until it is an interval. The circle
  of fifths lifts into a spiral, then into the tuning lattice. A reverb tail resolves into individual reflections
  in a drawn room.
* **Listening windows.** The narration stops, the example plays, and the screen says what to listen for. Every part
  has *pause-and-listen* questions: the ear-training thread of a music degree, run inside the lecture.
* **Color is meaning.** The twelve pitch classes keep one hue each, arranged by fifths so that near keys look
  alike. The Tune is always gold. Time, frequency and level keep their colors across every plot.
* **Honest playback.** A demonstration that needs headphones, or low bass, or a difference smaller than a
  streaming codec preserves, says so on screen, and the argument is also made visually (a difference signal, a
  measured curve), so the film works on a phone speaker and with the sound off.

## The parts

| # | Part | Ideas, mathematics and history | What we build, compute and hear |
|---|---|---|---|
| **I** | **Sound** | | |
| 1 | One String | Pythagoras and the false legend of the hammers, the monochord, Mersenne's laws, the wave equation, d'Alembert against Bernoulli, modes and harmonics, pluck position | a simulated string checked against the analytic solution; the Tune on one string |
| 2 | Waves in Air | pressure waves, the speed of sound (Newton's error, Laplace's fix), decibels, the inverse-square law, diffraction, standing waves, Helmholtz resonators, Doppler | a 2-D acoustic simulator; the Tune blown on tuned bottles |
| 3 | The Spectrum | Fourier series and transform, timbre, the spectrogram, windows and the Gabor limit, phase, noise colors, why the attack matters | our STFT and constant-Q transform; the Tune built one partial at a time |
| 4 | The Ear | the cochlea as a frequency analyzer, critical bands, loudness and equal-loudness contours, masking, pitch by place and by timing, the missing fundamental, hearing loss | a gammatone cochlea; the Tune with its fundamentals removed, and as Shepard tones |
| 5 | Consonance | Pythagoras, Galileo, Euler, Rameau, Helmholtz's beats, Plomp and Levelt, Sethares's curves, harmonicity, the Tsimane' experiment | dissonance curves that find the just ratios; a timbre whose "octave" is 2.1 |
| 6 | Tuning | the Pythagorean and syntonic commas, just intonation, meantone and wolves, well temperament, Zhu Zaiyu and Stevin, continued fractions and why 12, stretched pianos | the tuning lattice; the Tune in eight temperaments; a comma pump that drifts flat |
| 7 | Strings, Hammers and Bows | guitar bodies, the piano's hammer and inharmonicity, Helmholtz motion of the bowed string, the Schelleng diagram, the blind tests of Stradivari | plucked, struck and bowed physical models; Schelleng's wedge found by simulation |
| 8 | Pipes, Reeds and Voices | bores and impedance, why a clarinet lacks even harmonics, the reed as a valve, brass bells and mouthpieces, the source-filter voice, formants, overtone singing | a clarinet model, a brass model and a voice that sings vowels |
| 9 | Drums, Bars and Bells | Bessel modes of a membrane, how timpani and tabla become harmonic, tuned bars, the bell's minor third, Chladni figures, "can one hear the shape of a drum?" | modal percussion; two different drums with the same spectrum, computed |
| **II** | **Notes** | | |
| 10 | Writing It Down | the Hurrian hymn, neumes, Guido's staff, mensural notation, tablature, jianpu and gongche, piano roll, MIDI, MusicXML; what notation leaves out | the series' score format and engraver; the Tune in ten notations |
| 11 | Rhythm and Meter | pulse and tempo, meter as nested periods, syncopation, hemiola, polyrhythm, additive meters, swing, the rhythm–pitch continuum | the rhythm engine; a 3:2 polyrhythm accelerated into a fifth |
| 12 | Scales and Modes | stacking fifths to 5, 7 and 12, the three-gap theorem, maximal evenness, the modes by brightness, scales of the world, counting scales with Burnside | all 352 necklaces of twelve; the Tune in every mode |
| 13 | Intervals and Chords | spelling and the line of fifths, triads and sevenths, inversion and Rameau's fundamental bass, figured bass, voicing and critical bands, the Tonnetz | a chord module with root finding; the low-interval limit computed |
| 14 | Melody | contour, steps and leaps, the arch, gap-fill and regression to the mean, motif and sequence, entropy and expectation | an n-gram model of folk melody; the Tune's surprise, note by note |
| 15 | Key | scale-degree qualia, the probe-tone experiment, cadences, key finding, the torus of keys, modulation | a key finder scored on the *Well-Tempered Clavier*; a modulation's path on the torus |
| **III** | **Voices** | | |
| 16 | Two Voices | organum, Fux's species, why parallel fifths are forbidden (Huron's derivation from auditory streaming), dissonance treatment | a species checker and generator; every first-species answer to the Tune, counted |
| 17 | Four Voices | the chorale, ranges and spacing, voice-leading rules and how often Bach breaks them, non-chord tones, harmonization as search | a harmonizer scored against Bach's own; the Tune as a chorale |
| 18 | Progressions | tonic, predominant, dominant; root motion; sequences; the rule of the octave; partimento and the galant schemata; ground basses | a harmonic transition model from the chorales; the Tune over the Folia |
| 19 | Chromatic Harmony | secondary dominants, mixture, the Neapolitan and augmented sixths, the diminished seventh as a four-way door, enharmonic modulation, the Tristan chord | a modulation pathfinder between any two keys; a tension curve |
| 20 | Canon and Fugue | rounds, invertible counterpoint, the symmetries of a subject, tonal answers, stretto, the *Musical Offering* and its endlessly rising canon | a canon solver; a three-voice fugue exposition on the Tune |
| 21 | Form | phrase, period and sentence; binary, ternary, rondo, variation, sonata; song forms; repetition; self-similarity matrices | form found from audio; the Tune as a miniature sonata |
| 22 | Analysis | Schenker's reductions and their critics, Lerdahl and Jackendoff's generative theory, harmony as a grammar, parsing | a probabilistic grammar of chord sequences; the Tune reduced and regrown |
| **IV** | **A Thousand Years** | | |
| 23 | Chant to Polyphony | the modes, Guido's hexachord, organum at Notre Dame, the rhythmic modes, the Ars Nova, isorhythm, Machaut | an isorhythm engine; the Tune as chant, organum and motet |
| 24 | The Renaissance | thirds become consonant, imitation, Josquin and the attribution problem, Palestrina's rules, Petrucci's press, Zarlino, Vicentino's 31 tones | a stylometric attribution test; the Tune as a point of imitation |
| 25 | The Baroque | Monteverdi against Artusi, Vincenzo Galilei's strings, basso continuo, opera, the ritornello, the suite, temperament and key character | a figured-bass realizer; the Tune as a French overture and a chaconne |
| 26 | The Classical Style | schemata at work, periodic phrasing, sonata form as drama, Haydn's wit, Mozart's K. 265 on our Tune, Beethoven's motives and his metronome | Mozart's twelve variations measured; our own Classical set beside them |
| 27 | The Romantic Century | the iron piano, the Lied, programme music, the leitmotif, the growing orchestra, rubato, harmony stretched to its limit | a chromaticism index across two centuries; the Tune as a nocturne |
| **V** | **After Tonality** | | |
| 28 | New Scales, New Rhythms | Debussy and the gamelan, whole-tone and octatonic collections, Stravinsky's accents, Bartók's fieldwork and symmetry, Messiaen's modes | every scale of limited transposition, enumerated; the golden-section claim tested |
| 29 | Twelve Tones | free atonality, pitch-class sets, the interval vector and the Z-relation, the hexachord theorem, rows and combinatoriality, can rows be heard | the set classes derived by Burnside; all all-interval rows enumerated |
| 30 | Sound Itself | musique concrète, chance, the electronic studio, Xenakis's stochastic music, Ligeti's clouds, Reich's phasing, spectral music | a phasing engine; the Tune as a glissando cloud and as a spectrum |
| 31 | Transformations | Lewin's intervals as group actions, the T/I and PLR groups and their duality, the Tonnetz as a torus, hexatonic cycles, film music's wonder chords | the group checked by brute force; the Tune harmonized by a walk on the Tonnetz |
| 32 | The Geometry of Chords | Tymoczko's orbifolds, dyads on a Möbius strip, voice leading as distance, why triads work, the Fourier transform of a chord | chord space as an instrument; minimal voice leading solved; Bach's efficiency measured |
| 33 | The Mathematics of Rhythm and Scale | Euclidean rhythms, well-formed scales and continued fractions, tiling canons and Vuza, de Bruijn sequences in Sanskrit, change ringing, regular temperaments | a Vuza canon found at period 72; a temperament finder that rediscovers 12, 19, 31 and 53 |
| **VI** | **Many Musics** | | |
| 34 | Raga and Tala | the drone, swara and shruti, raga as a path, gamaka, the 72 melakartas, tala cycles, the arithmetic of the tihai | a tihai solver; a tanpura with its buzzing bridge; the Tune as an alap and gat |
| 35 | Maqam | al-Fārābī and Ṣafī al-Dīn, ajnas, neutral intervals, sayr and modulation, Turkish commas, Persian dastgah, rhythmic cycles, the 1932 Cairo congress | maqam in cents against measured practice; the Tune in Rast, Bayati and Hijaz |
| 36 | Bronze and Silk | the two-tone bells of Marquis Yi, the twelve lü and Jing Fang's 53, the guqin's harmonics, gagaku, the gamelan's tunings, beats by design, interlocking | a two-tone bell and a bronze ensemble; the Tune as balungan with kotekan |
| 37 | Timelines | the standard pattern and the diatonic scale, Ewe ensembles, 3:2, the mbira's inherent patterns, interlocking, clave, samba | timeline geometry measured; the Tune emerging from parts nobody plays |
| 38 | Blues and Swing | the twelve-bar form, blue notes, ragtime, swing ratios measured against tempo, guide tones, ii–V–I, the tritone substitution | a swing model; Joplin rendered; the Tune as a blues and a big-band riff |
| 39 | Changes | bebop and the contrafact, the bebop scale's theorem, chord-scale theory, modal jazz, Coltrane's thirds on the Tonnetz, improvisation | an improviser over changes; the Tune as a bebop head with Coltrane changes |
| 40 | The Song | AABA to verse-chorus to the loop, rock harmony, groove, the hook, hip-hop's breakbeat and flow, the drop, pop measured over sixty years | corpus statistics of charts; the Tune as a pop single and a sampled beat |
| **VII** | **The Craft** | | |
| 41 | Orchestration | ranges and registers, blend and balance, why sixteen violins are not one loud violin, *Boléro*'s synthetic organ, orchestration as optimization | a solver that orchestrates a target spectrum; the Tune eight ways |
| 42 | Composing | motive and development, variation technique, planning tension, working under constraint, dice games, the *Illiac Suite*, generate and test | a generate-and-test composer with its rejected drafts shown |
| 43 | Performing | expressive timing and dynamics, vibrato, intonation in practice, ensemble synchronization, practice science, the Hatto hoax | an expressive performer; an ensemble that stays together, and one that does not |
| 44 | Music for Picture and Play | what film music does, leitmotifs, hit points and click-track arithmetic, adaptive game music, chiptune under hardware limits | one scene scored three ways; an adaptive score driven by a game |
| **VIII** | **The Mind** | | |
| 45 | The Scene | auditory scene analysis, streaming, timbre space, absolute pitch, the great illusions | a streaming model; the Tune hidden in another melody, then heard |
| 46 | Expectation and Emotion | Meyer, statistical learning, surprise and uncertainty, chills, tension, groove's inverted U | a listener model; three endings: expected, delayed, denied |
| 47 | Origins and Universals | the oldest flutes, what is and is not universal, theories of origin, birds and whales, infants, music and language, the Mozart effect | cultural transmission simulated; the Tune's family tree |
| **IX** | **Electric Sound** | | |
| 48 | Digital Audio | the sampling theorem, aliasing, quantization noise, dither, noise shaping, delta-sigma, why 44,100 | converters simulated; the Tune at one bit, sounding fine |
| 49 | Filters, Delay and Reverb | impulse responses, poles and zeros, equalizers, combs, flangers and phasers, Schroeder's reverberator, feedback delay networks, plates and springs | a pole-zero instrument; the Tune in a bathroom, a plate and a cathedral |
| 50 | Dynamics, Distortion and Pitch | waveshaping and Chebyshev polynomials, intermodulation and the power chord, compressors, the phase vocoder, PSOLA, Auto-Tune, the vocoder | our compressor, fuzz and pitch corrector; the voice of Part 8, tuned |
| 51 | Synthesis I: Oscillators and Filters | the Telharmonium, additive and subtractive synthesis, alias-free oscillators, the Moog ladder, envelopes and modulation, wavetables | an analog-modelled voice; the Tune switched on |
| 52 | Synthesis II: FM, Grains and Physical Models | Chowning's discovery and Bessel functions, granular synthesis, sampling, Karplus–Strong, digital waveguides, modal synthesis | an FM engine checked against the Bessel sidebands; a grain cloud |
| 53 | MIDI, Sequencers and the DAW | player pianos and Nancarrow, MUSIC N, the 1983 handshake, the protocol byte by byte, real-time audio, the audio graph, plug-ins, live coding | a sequencer and audio graph with a measured real-time budget; a tempo canon |
| **X** | **The Studio and the Stage** | | |
| 54 | Microphones and Loudspeakers | transduction both ways, polar patterns, proximity effect, noise, Thiele–Small parameters, boxes and ports, crossovers, amplifiers, headphones | virtual microphones and loudspeakers; the Tune through a phone speaker and a ported box |
| 55 | Rooms and Space | Sabine and Symphony Hall, modes, absorption and diffusion, concert-hall design, localization, stereo, Ambisonics, binaural audio | an image-source room; the Tune walked through four halls and around your head |
| 56 | Recording and Mixing | from the horn to the workstation, stereo microphone arrays, phase, gain staging, balance, panning laws, masking, depth, automatic mixing | the session: our instruments recorded and mixed three ways |
| 57 | Mastering and Loudness | the chain, true peaks, BS.1770 and LUFS, the loudness war measured, normalization, vinyl's RIAA curve and geometry | a loudness meter that agrees with ffmpeg; the same master, loud and dynamic |
| 58 | Compression for the Ear | lossless coding, masking thresholds, the MDCT and its cancelling aliases, MP3 to Opus, listening tests, neural codecs | a lossless coder and a perceptual codec; the sound the codec throws away |
| 59 | Live Sound | Shea Stadium, gain before feedback, line arrays and interference, subwoofer arrays, delay towers, system tuning, hearing health | array and feedback simulators; the Tune from the front row and the car park |
| 60 | The Business of Music | two copyrights, where a stream's money goes, deals and recoupment, superstars and power laws, cost disease, similarity lawsuits, AI and rights | a royalty waterfall; pro-rata against user-centric payout; the odds two melodies collide |
| **XI** | **Listening Machines** | | |
| 61 | Pitch, Onsets and Transcription | YIN, salience, onset detection, non-negative matrix factorization, neural transcription, from notes to a score | a transcriber scored against known scores; the Tune after five round trips |
| 62 | Beat, Chords and Structure | tempograms, beat tracking by dynamic programming, time warping and score following, chord recognition, structure from self-similarity | a beat tracker, an aligner and a chord recognizer; an accompanist that follows rubato |
| 63 | Finding Music | Shazam's constellations, tagging and embeddings, the faults of GTZAN, collaborative filtering, cold start, popularity feedback | a fingerprinter over the whole series; a recommender on listeners whose tastes we know |
| 64 | Source Separation | the cocktail party, panning and ICA, harmonic–percussive separation, masks and oracles, the phase problem, U-Nets and Demucs | separators scored against our own multitracks; a mashup from separated stems |
| 65 | Machines that Compose | Markov chains and plagiarism, constraints, Cope, recurrent networks, the Music Transformer, tokenizations, evaluation | Markov models and a small transformer; the Tune continued, with the copying measured |
| 66 | Generative Audio | WaveNet, vocoders, VQ-VAE and neural codecs, language models over audio tokens, diffusion, differentiable DSP, voices, rights | a DDSP instrument and a token model trained on our own sounds |
| **XII** | **Coda** | | |
| 67 | Doing Research in Music | the methods of musicology, theory, ethnomusicology, cognition, acoustics and MIR; listening tests; corpus bias; the open-problems map | the series audited: every verdict re-run with intervals |
| 68 | The Variations | the whole chain run once, end to end; what survives it; what was built; the suite performed | the round trip from score to sound to score; the concert |

## Shared code and the Chinese edition

`explainer/music/` will hold Monochord, the sound layer for scenes (`sound.py`: a `SoundScene` on top of
`VoiceoverScene`), the visual instruments listed in the syllabus, and the chapter cards with the Chain and the
timeline. The lecture set pieces are reused from `explainer.ai.lecture`. The course material follows
[`videos/coursekit/AUTHORING.md`](../coursekit/AUTHORING.md): `videos/music/course/`, a lab per part
(`python -m videos.music.labs N`), and an interactive per part that makes sound in the browser.

The series is planned in English and Chinese like *Computer Science, Built* (narration tables in each part's
`zh_lines.py`, on-screen text in `videos/music/music_text_zh.json`, terms in `videos/music/MUSIC_ZH_GUIDE.md`),
subject to the decision in the syllabus §9.
