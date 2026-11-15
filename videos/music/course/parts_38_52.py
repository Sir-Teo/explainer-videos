"""Act VI's last parts and Act VII: Parts 38 onwards as they are built (see ``videos/music/course/__init__.py``)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=38, level="U", widget="swing", prereq=(11, 13, 17, 18, 32, 37),
        question="What is swing, and how did the blues, ragtime and the swing band build the language of jazz?",
        story="Asked what swing is, jazz musicians say that if you have to ask you will never know; but it can be "
              "measured. The part builds the twelve-bar blues, three lines of four with every chord a dominant seventh, "
              "and its variants up to the jazz blues; blue notes as regions between minor and major rather than "
              "pitches, heard in a phrase with its third bent from 300 to about 385 cents; and the AAB verse, each line "
              "answered in the bars it leaves open. Joplin's Maple Leaf Rag (1899), played from its encoding, puts 46 "
              "of its first strain's 85 right-hand attacks between the eighths against 3 of 45 in the left hand. A "
              "simple swing model, 3:1 at 120 beats a minute falling to 1:1 at 300, the trend Friberg and Sundström "
              "measured, keeps the short note near a tenth of a second at fast tempos; late downbeats are a second "
              "ingredient, and random deviations are not. The swing band trades riffs between sections. A walking bass "
              "is a shortest path under four rules, meeting every chord on its root after a semitone; guide tones, the "
              "third and seventh, move two semitones in all through ii-V-I; and a dominant shares its tritone with "
              "exactly one other, its substitute, so the bass can slide by semitones. The Tune becomes a twelve-bar "
              "blues sung with blue thirds, a rag and a riff chart.",
        handoff="Standards and reharmonisation in Part 39; the riff, backbeat and song in Part 40; arranging in Part 41; "
                "performing and improvising in Part 43; beat tracking and chord recognition in Part 62.",
        outside="Part 11 for meter; Part 13 for seventh chords; Part 17 and Part 18 for voice leading and progressions; "
                "Part 32 for voice leading as distance; Part 37 for timelines and call and response. Dynamic "
                "programming, swing ratios, syncopation measures.",
        objectives={
            "U": ["Hear the twelve-bar form, blue notes and an AAB verse, and name what each does.",
                  "Hear a rag's syncopated right hand against its march-like left hand.",
                  "Hear swing change with tempo, and a tritone substitution in the bass."],
            "M": ["Model swung eighths at any tempo and compute the short note's length.",
                  "Generate a walking bass and guide-tone lines as shortest paths through a progression.",
                  "Prove that exactly two dominant sevenths share a tritone, and count a rag's syncopations."],
            "D": ["Design an experiment to separate what makes a performance swing, and for whom."],
            "I": ["Walk a bass, voice guide tones and set a drum machine's swing as players and producers do."],
        },
        results=[
            ("The twelve-bar blues", r"I^7\,I^7\,I^7\,I^7 \,|\, IV^7\,IV^7\,I^7\,I^7 \,|\, V^7\,IV^7\,I^7\,V^7"),
            ("The swing model", r"r = 3 \text{ at } 120 \text{ bpm} \to 1 \text{ at } 300; \ \text{short note} \approx 100 \text{ ms}"),
            ("Maple Leaf Rag", r"46/85 \text{ right-hand attacks between the eighths; left hand } 3/45"),
            ("Guide tones", r"Dm^7 \to G^7 \to C^{maj7}: \ F/C,\ F/B,\ E/B \ (2 \text{ semitones})"),
            ("Tritone substitution", r"G^7 \cap D\flat^7 = \{F, B\}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 9),
        D=(10,),
        I=(7, 8),
        also=(("Monochord's blues and swing: forms, the swing model, walking bass, guide tones, tritone substitutes, syncopation", "explainer/music/monochord/blues.py"),),
    ),
    Part(
        n=39, level="U", widget="bebop", prereq=(12, 18, 31, 32, 37, 38),
        question="How do jazz players improvise through changes, and why were Coltrane's Giant Steps so hard?",
        story="On 5 May 1959 John Coltrane recorded Giant Steps: twenty-six chords in sixteen bars, coming home to three "
              "keys a major third apart, at nearly 290 beats a minute. The part starts from bebop, whose players wrote "
              "contrafacts, new melodies on the shared changes of standards. The bebop scale adds one chromatic passing "
              "tone to a chord's mode so that its four chord tones alternate with four others: a run from any chord "
              "tone keeps chord tones on every beat, proved and checked for every dominant and sixth chord, where the "
              "plain mode manages about two beats in three. Lines aim at targets, usually guide tones, and enclose them; "
              "players learn formulas in every key; chord-scale theory names safe notes and avoid notes, from George "
              "Russell's 1953 Lydian Chromatic Concept to the Berklee school. Kind of Blue slowed the changes to two chords "
              "in thirty-two bars and voiced them in fourths. Coltrane's third cycles put three tonic triads in a line up "
              "the Tonnetz's major-third axis, joining keys that share only three notes. Reharmonisation adds secondary "
              "dominants and tritone substitutes under a fixed melody. A page-long improviser, a phrase grammar of runs, "
              "arpeggios and enclosures aimed at guide tones, beats random scale notes by the series' measures (chord "
              "tones on 90 per cent of beats against 57) and cannot listen; free jazz, Pressing's model and the brain "
              "scanner frame what it lacks. The Tune becomes a bebop head with an improvised chorus, then travels "
              "through C, A flat and E.",
        handoff="The song and its riffs in Part 40; composing as search in Part 42; performing together in Part 43; pattern "
                "search in Part 63; machines that compose and improvise in Part 65.",
        outside="Part 12 for modes; Part 18 for progressions; Part 31 for the Tonnetz; Part 32 for voice leading; Part 37 for "
                "call and response; Part 38 for swing, guide tones and tritone substitution. Generative grammars, "
                "baselines and evaluation.",
        objectives={
            "U": ["Hear bebop lines land on chord tones, and hear an enclosure arrive.",
                  "Hear modal jazz's static harmony and quartal voicings, and Coltrane's third cycle.",
                  "Tell an improviser's line from a random one by ear."],
            "M": ["Prove that the bebop scale keeps chord tones on every beat, and check it by program.",
                  "Compute chord scales, avoid notes, key centres and the notes two keys share.",
                  "Build and evaluate a phrase-grammar improviser against baselines."],
            "D": ["Design a study separating recalled patterns from local choices in improvised solos."],
            "I": ["Practise formulas through the keys and reharmonise a standard, as players and arrangers do."],
        },
        results=[
            ("The bebop scale", r"C\,B\,B\flat\,A\,G\,F\,E\,D: \ \text{chord tones at positions } 0, 2, 4, 6"),
            ("Giant Steps", r"26 \text{ chords in } 16 \text{ bars; tonics } B, G, E\flat \ (4 \text{ semitones apart})"),
            ("Shared notes", r"\text{keys a fifth apart share } 6 \text{ of } 7; \text{ a major third apart, } 3"),
            ("Avoid notes", r"\text{a scale tone a semitone above a chord tone: } F \text{ over } C^{maj7}"),
            ("The improviser", r"\text{chord tones on } 90\% \text{ of beats vs } 57\% \text{ (random in scale)}"),
        ],
        U=(0, 1, 2, 3, 5, 6, 7, 8),
        D=(10,),
        I=(4, 9),
        also=(("Monochord's changes: bebop scales, chord scales, third cycles, reharmonisation, a phrase-grammar improviser and its judge", "explainer/music/monochord/changes.py"),),
    ),
    Part(
        n=40, level="U", widget="steps", prereq=(11, 14, 21, 37, 38, 39),
        question="How has the popular song's form been shaped by the technologies that sold it, from sheet music to streaming?",
        story="The hit single's introduction shrank from over twenty seconds in the mid-1980s to about five by the mid-2010s "
              "(Léveillé Gauvin, 2018), and on streaming services a play pays only after about thirty seconds. The part "
              "follows the song from Tin Pan Alley's thirty-two-bar AABA to verse and chorus and the song factories; from "
              "progressions to loops (I-V-vi-IV, bVII-IV-I, the aeolian loop), where melody and harmony part company (4 of "
              "the 12 on-beat notes of our hook lie outside the chord); riffs, and why distortion forces power chords; the "
              "backbeat, funk's one, disco's four on the floor, house and half-time trap, with drum-machine swing on the "
              "sixteenths; hooks, titles and prosody, measured as the share of syllables whose stress matches the beat; "
              "the 808 from first principles, a struck resonator sagging from 81 to 52 Hz and six square waves for the "
              "hats, tuned into a bass line; the break, the sampler and the law; flow, a verse of ours placed on the beat and "
              "in threes, measured after Ohriner; and the build, the drop and the sidechain. Corpus studies (Mauch and "
              "colleagues; Serrà and colleagues) frame what sixty years of charts show, and what they leave out. The Tune "
              "becomes a pop single and then a beat that samples Variation 7.",
        handoff="Composing as search in Part 42; dynamics and the compressor in Part 50; synthesis in Parts 51 and 52; the "
                "workstation in Part 53; mastering and loudness in Part 57; the business of music in Part 60.",
        outside="Part 11 for meter; Part 14 for melody; Part 21 for form; Part 37 for timelines and interlocking; Part 38 for "
                "swing and the blues; Part 39 for standards. Oscillators and resonators, compressors, corpus statistics.",
        objectives={
            "U": ["Hear AABA and verse-chorus forms, loops and riffs, and name them.",
                  "Hear the backbeat, four on the floor and a half-time beat, and drum-machine swing.",
                  "Hear a sidechain pump and a power chord stay clear through distortion."],
            "M": ["Build drum-machine voices from their circuits' principles: a struck resonator and six square waves.",
                  "Measure prosody and flow on a sixteenth-note grid.",
                  "Compute a sidechain's ducking and recovery, and chop and re-sequence a recording."],
            "D": ["Design a study of whether new platforms change how songs are written or only which win."],
            "I": ["Program a beat, tune an 808 and sidechain a pad, as producers do; clear samples or replay them."],
        },
        results=[
            ("Intros", r"20 \text{ s (mid-1980s)} \to 5 \text{ s (mid-2010s)}"),
            ("The 808 kick", r"y = \sin\!\big(\textstyle\int 2\pi f(t)\,dt\big) e^{-t/\tau}, \ f: 81 \to 52 \text{ Hz}"),
            ("The 808 hats", r"205.3,\ 304.4,\ 369.6,\ 522.7,\ 540,\ 800 \text{ Hz squares}"),
            ("Sidechain", r"\text{back within 1 dB after } \tau \ln D"),
            ("Flow", r"\text{accents every } 3 \text{ sixteenths against the beat}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 9),
        D=(10,),
        I=(6, 7, 8),
        also=(("Monochord's song studio: drum-machine voices, patterns, sidechain, chopping, prosody and flow", "explainer/music/monochord/song.py"),),
    ),
    Part(
        n=41, level="U", widget="orchestra", prereq=(3, 5, 7, 8, 9, 17, 20),
        question="What does an orchestrator control, and can a computer orchestrate a sound?",
        story="Ravel called Boléro (1928) a piece for orchestra without music: one tune in two halves, stated eighteen "
              "times over one snare-drum rhythm, with only the instruments changing. In one statement a horn, a celesta "
              "and two piccolos sit on the tune's harmonics and fuse into a colour no single player owns: additive "
              "synthesis with players. The part builds an orchestra from the series' own physical models, measuring "
              "sixteen harmonics on each and resynthesising them, and asks what an orchestrator controls: ranges, "
              "registers and transposition; loudness and brightness (a trumpet blown hard is brighter, not just louder, "
              "its centroid nearly doubling); sections, where eight violins are 10.6 dB above one, between the "
              "incoherent 9 and coherent 18; doubling, blend and balance; spacing, where the same C major chord is three "
              "times rougher close and low than open; textures and the melody of timbres. Then it turns Ravel around: a "
              "solver fits non-negative loudnesses to 42 candidates and keeps the best four, spelling a sung vowel within "
              "7.1 dB a band but a bell only within 31.5, because a bell's partials are not harmonics. The Tune is heard "
              "in eight orchestrations, the last matched to a vowel.",
        handoff="Composing as search in Part 42; performing together in Part 43; music for picture in Part 44; the auditory "
                "scene and timbre space in Part 45; synthesis from physical models in Part 52; the hall in Part 55.",
        outside="Part 3 for spectra and additive synthesis; Part 5 for roughness; Parts 7-9 for the instrument models; "
                "Part 17 for voicing and the voice; Part 20 for counterpoint. Least squares, decibels.",
        objectives={
            "U": ["Hear instrument families and registers, and tell a clarinet from a flute on one note.",
                  "Hear brightness rise with effort, and a section's chorus against one player.",
                  "Hear a doubling fuse, and a chord muddy in a low close voicing."],
            "M": ["Measure an instrument's harmonics on a physical model and resynthesise it additively.",
                  "Compute the level of n coherent and incoherent players, and a combination's fusion on a harmonic series.",
                  "Orchestrate a target spectrum by non-negative least squares and subset search."],
            "D": ["Design a study that predicts blend and layering from the score and the instruments' spectra."],
            "I": ["Voice and double for balance and clarity, and mock up an orchestration before rehearsal."],
        },
        results=[
            ("Players", r"n \text{ incoherent: } 10\log_{10} n \text{ dB}; \ \text{coherent: } 20\log_{10} n"),
            ("Eight violins", r"+10.6 \text{ dB measured}"),
            ("Ravel's harmonics", r"0,\ -2.0,\ +13.7 \text{ cents from the series}"),
            ("Spacing", r"\text{roughness } 1.33,\ 0.96,\ 0.19"),
            ("The solver", r"\min_{w \ge 0} \lVert A w - b \rVert: \ 18.3 \to 7.1 \text{ dB a band}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8),
        D=(10,),
        I=(9,),
        also=(("Monochord's orchestra: measured spectra, sections, fusion, spacing roughness and the matching solver", "explainer/music/monochord/orchestra.py"),),
    ),
    Part(
        n=42, level="U", widget="motive", prereq=(14, 16, 17, 18, 20, 21, 22),
        question="Is composing search under constraints, and what would a program need in order to judge its own drafts?",
        story="Beethoven's sketchbooks of 1822 to 1824 show the Ode to Joy approached in draft after draft; what the search "
              "found has 30 notes in its first two phrases and not one leap. The part treats composing as search under "
              "constraints. It starts with the motive and the classical operations on it (inversion, retrograde, "
              "augmentation, diminution, fragmentation, interval change, new rhythm, embellishment), all diatonic and all "
              "functions from melodies to melodies; grows Schoenberg's sentence from four notes; varies the Tune four "
              "ways; plans tension bar by bar and measures it against the plan. It counts what rules do, exactly: of "
              "2,562,890,625 eight-note melodies on fifteen white keys, five rules leave 9,252. It builds a dice game of "
              "its own in the format of Kirnberger's (1757), 176 bars with about 1.6 x 10^13 distinct minuets and 41 bits "
              "of entropy; reruns Hiller and Isaacson's generate-and-test (277 draws for a twelve-note line, most rejected "
              "at the cadence); shows a Markov chain copying more as it remembers more; evolves melodies; and builds a "
              "searcher whose critics are the series' own rules, which keeps draft 1,205 of 2,000 and shows what it threw "
              "away. The Tune's first four notes become Variation 42.",
        handoff="Performing in Part 43; expectation and emotion in Part 46; sequencers in Part 53; machines that compose in "
                "Part 65; generative audio in Part 66.",
        outside="Part 14 for melody and its statistics; Part 16 for counterpoint's rules and counting; Part 18 for "
                "progressions; Part 20 for canon; Part 21 for form; Part 22 for grammars. Dynamic programming, Markov "
                "chains, entropy, search.",
        objectives={
            "U": ["Hear a motive's inversion, retrograde, augmentation and fragments, and the motive inside a phrase.",
                  "Hear ornamental, rhythmic, harmonic and character variations of one theme.",
                  "Hear a late climax and an early one, and a chain that copies against one that wanders."],
            "M": ["Implement diatonic operations on a motive and find the shortest chain of operations between two figures.",
                  "Count melodies under rules exactly by dynamic programming, and a dice game's distinct pieces and entropy.",
                  "Build a generate-and-test searcher with hard and soft critics, and a genetic algorithm with the same critics."],
            "D": ["Design a study that measures novelty and value separately for human and machine composers."],
            "I": ["Sketch many drafts and judge them later; write fragments and rules that a game engine recombines."],
        },
        results=[
            ("The funnel", r"15^8 = 2{,}562{,}890{,}625 \to 9{,}252 \text{ under five rules}"),
            ("Two dice", r"H = -\textstyle\sum_s p_s \log_2 p_s \approx 3.27 \text{ bits}"),
            ("Our dice game", r"\approx 1.6 \times 10^{13} \text{ minuets}, \ 41 \text{ bits}"),
            ("Generate and test", r"277 \text{ draws for 12 notes}"),
            ("The searcher", r"2{,}000 \text{ drafts}: \ 164 \text{ scored}, \ \text{draft } 1{,}205 \text{ kept}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7),
        D=(10,),
        I=(8, 9),
        also=(("Monochord's composer: motive operations, the funnel, the dice game, generate and test, chains, critics and the searcher", "explainer/music/monochord/composer.py"),),
    ),
    Part(
        n=43, level="U", widget="duo", prereq=(4, 6, 7, 10, 11, 37),
        question="What does a performer add to the notes, and how do players stay together?",
        story="In 2007 a critic's CD of Joyce Hatto went into a computer and the track database named another pianist: over a "
              "hundred recordings under her name were other people's, and timing analysis showed it, because no two pianists "
              "shape time alike. The part measures what a performer adds to a score. It plays the Tune exactly as written and "
              "as performed by five rules after the KTH system (phrase arch, duration contrast, high loud, punctuation, final "
              "ritardando), each heard alone and together at three strengths; derives the final ritardando from a runner "
              "braking (tempo squared falling linearly, q = 2); hears legato and staccato as held time; hears a 60-cent "
              "vibrato at its mean pitch; models ensembles by linear phase correction, where a duo's asynchrony shrinks by "
              "1 - (alpha1 + alpha2) a beat, holds only for totals between 0 and 2 (best near 0.85 for our noise levels), "
              "drifts 264 ms in 24 beats with nobody listening and shakes apart above 2; compares democratic and autocratic "
              "quartets after Wing and colleagues; and fingerprints ten model pianists by their tempo curves: a time-stretched "
              "copy matches its source at 0.9999, a pianist's own second take at 0.988, other pianists at most 0.90. Practice "
              "(about a fifth of the differences in music, by meta-analysis), anxiety and the body close the part.",
        handoff="Music for picture in Part 44; expectation and emotion in Part 46; MIDI and the workstation in Part 53; beat "
                "tracking and transcription in Parts 61 and 62; generative audio in Part 66.",
        outside="Part 4 for loudness; Part 6 for tuning; Part 7 for the piano; Part 10 for notation; Part 11 for meter; Part "
                "37 for ensemble timelines. Autoregressive processes, correlation.",
        objectives={
            "U": ["Hear a deadpan and an expressive performance of the same notes, and name what changed.",
                  "Hear legato and staccato, a vibrato's pitch, and three shapes of final ritardando.",
                  "Hear a duo that holds, one that drifts and one that shakes apart."],
            "M": ["Implement performance rules and the kinematic ritardando, and measure a performance's deviations.",
                  "Derive a duo's asynchrony variance under linear phase correction, and its stability bound.",
                  "Identify a performer, or a copy, by correlating normalised tempo curves."],
            "D": ["Design a study that separates an interpretation from the common part of expression and from noise."],
            "I": ["Humanise sequenced parts; decide who leads in chamber music; practise with spacing and interleaving."],
        },
        results=[
            ("Ritardando", r"v(x) = \left[1 + (w^q - 1)\,x\right]^{1/q}"),
            ("Phase correction", r"A_{k+1} = (1 - \alpha_1 - \alpha_2) A_k + \varepsilon_k"),
            ("Stability", r"0 < \alpha_1 + \alpha_2 < 2"),
            ("Variance", r"\tfrac{2\sigma_T^2}{1 - b^2} + \tfrac{4\sigma_M^2}{1 + b}, \ b = 1 - \alpha_1 - \alpha_2"),
            ("A copy", r"r = 0.9999 \text{ against } 0.988 \text{ for a second take}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7),
        D=(10,),
        I=(8, 9),
        also=(("Monochord's performer: rules of expression, the kinematic ritardando, vibrato, phase correction and the identity test", "explainer/music/monochord/perform.py"),),
    ),
    Part(
        n=44, level="U", widget="hits", prereq=(4, 11, 19, 27, 31, 40, 42, 43),
        question="What does music do to a picture, and how is music written for a scene of unknown length?",
        story="One animated scene of ours, three scores, three different films; then the same comic score cut to the picture "
              "and 0.6 s late, where every hit misses. The part covers what film music does (Boltz's experiment, Cohen's "
              "model), leitmotifs (a motive in three moods), spotting and hit points, and the tolerance of sync (sound may lag "
              "a picture by about 125 ms but lead it by only 45). It works the click track's arithmetic (frames per beat = "
              "1440 / tempo) and finds, by scanning every tempo, the only two between 70 and 160 that put three hits within a "
              "frame of a beat: 88.28 (beats 4, 11 and 16) and 153.69; the nearest written click, 16-2, drifts 1.6 frames by "
              "the landing, and a variable click lands every hit exactly. It hears Hollywood harmony (chromatic mediants, the "
              "Lydian sound, the minor iv), ducks music under a model voice (6 dB more room in the speech band), and builds "
              "an adaptive score as a state machine driven by a simulated game, whose transitions wait half a boundary on "
              "average (0.25 s for a beat, 1 s for a bar, 2 s for a phrase). A sound chip of ours shows duty cycles, LFSR "
              "noise and the one-channel arpeggio chord. The Tune becomes a cue on a hit point, a leitmotif and an adaptive "
              "loop.",
        handoff="The auditory scene in Part 45; expectation and emotion in Part 46; oscillators in Part 51; FM in Part 52; the "
                "workstation in Part 53; loudness in Part 57; machines that compose in Part 65.",
        outside="Part 4 for masking; Part 11 for meter; Part 19 for mixture; Part 27 for Wagner; Part 31 for transformations; "
                "Part 40 for the sidechain; Part 42 for motives and dice games; Part 43 for timing. Frame rates, state machines.",
        objectives={
            "U": ["Hear one scene read three ways by three scores, and music that misses its picture.",
                  "Hear a leitmotif change mood, and sound early, in sync and late against a picture.",
                  "Hear film harmony's chromatic mediants and minor iv, and music ducked under a voice."],
            "M": ["Convert between tempo, frames per beat and click notation, and find tempos that hit a set of hit points.",
                  "Build an adaptive score as a state machine and compute its transition delays.",
                  "Compute a pulse wave's harmonics from its duty cycle, and build a chip's channels."],
            "D": ["Design a player study comparing transition rules for responsiveness and musical coherence."],
            "I": ["Spot a scene and set its tempos; write segments, layers and stingers for middleware; mix under dialogue."],
        },
        results=[
            ("Frames per beat", r"f = 24 \times 60 / \text{tempo}"),
            ("A hit", r"\text{beat} = (t - t_0) \times \text{tempo} / 60"),
            ("The scene", r"88.28 \text{ bpm: beats } 4, 11, 16"),
            ("Waiting for a boundary", r"E[\text{delay}] = u / 2"),
            ("A pulse of duty d", r"a_k \propto |\sin(\pi k d)| / k"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6),
        D=(10,),
        I=(7, 8, 9),
        also=(("Monochord's music for picture and play: click arithmetic, the tempo finder, the chip, the adaptive score and ducking", "explainer/music/monochord/screen.py"),),
    ),
    Part(
        n=45, level="U", widget="stream", prereq=(4, 5, 14, 16, 17, 41),
        question="How does one pressure wave become a scene of separate voices, and why do counterpoint's rules follow?",
        story="Send an ascending and a descending scale to the two ears, note by note alternately, and listeners hear two "
              "smooth melodies that neither ear was given (Deutsch's scale illusion, in stereo). The part builds the rules "
              "of auditory scene analysis and their consequences: ABA- streaming heard at four settings, and a competition "
              "model of ours (a tone captures the next with a strength falling exponentially in time and on the ERB scale) "
              "whose one constant fits van Noorden's coherence boundary, read from his figure, within 0.28 semitone, with "
              "the fission boundary and the ambiguous region between; interleaved melodies (Frère Jacques hidden, crossing "
              "its distractor 15 times, then released by register) and implied polyphony; simultaneous grouping by "
              "harmonicity (a mistuned harmonic popping out), common onset, common fate and place; the continuity illusion; "
              "Huron's derivation of voice-leading rules from these principles, with parallel fifths fusing and crossing "
              "lines heard as bouncing; a timbre space of the series' own 13 instruments by MDS on five measurements; "
              "Shepard tones and Risset's glide, the octave-scrambled Tune, the tritone paradox; absolute pitch and "
              "everyday pitch memory. The Tune is hidden in another line and released by timbre.",
        handoff="Expectation and emotion in Part 46; origins and universals in Part 47; rooms and space in Part 55; "
                "transcription in Part 61; source separation in Part 64.",
        outside="Part 4 for the ear and its ERB scale; Part 5 for roughness and fusion; Part 14 for melody and contour; "
                "Part 16 for counterpoint; Part 17 for chorales; Part 41 for timbre. Gestalt principles, MDS.",
        objectives={
            "U": ["Hear the scale illusion, ABA- streaming and its build-up, and a tune vanish in another and return.",
                  "Hear a mistuned harmonic, an early harmonic and a vibrating group of harmonics come apart from a tone.",
                  "Hear the continuity illusion, Shepard tones and the octave-scrambled Tune."],
            "M": ["Derive the competition model's straight-line boundary and fit it to published points.",
                  "Measure attack, brightness, odd/even balance, jaggedness and decay, and build a timbre space by MDS.",
                  "Construct grouping stimuli: interleaved melodies, mistuned complexes, Shepard tones."],
            "D": ["Design a test of whether networks trained on natural sound reproduce human streaming boundaries."],
            "I": ["Separate parts by register and timbre; voice-lead for independence or fusion as the texture requires."],
        },
        results=[
            ("Capture", r"e^{-\Delta t / \tau}\, e^{-|\Delta z| / w}"),
            ("Two streams when", r"\Delta z > (w / \tau)\, T"),
            ("Fit", r"w / \tau = 32.4 \text{ ERB-numbers/s}, \ \text{rms } 0.28 \text{ st}"),
            ("ERB-number", r"z = 21.4 \log_{10}(1 + 0.00437 f)"),
            ("Shepard tone", r"\textstyle\sum_o a(o + c)\, \sin(2\pi f_0 2^{o + c} t)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 8, 9),
        D=(10,),
        I=(6, 7),
        also=(("Monochord's auditory scene: the scale illusion, the streaming model, grouping stimuli, Shepard tones and the timbre space", "explainer/music/monochord/scene.py"),),
    ),
    Part(
        n=46, level="U", widget="ending", prereq=(14, 15, 18, 21, 38, 42, 45),
        question="Why does music move us, and how much of that can expectation, measured in bits, explain?",
        story="In 2011 Salimpoor and colleagues caught dopamine released twice, at a musical chill and in the seconds of "
              "anticipation before it; Meyer had argued in 1956 that musical emotion is expectation delayed and fulfilled. "
              "The part builds a listener: a variable-order Markov model blended by prediction by partial matching, in the "
              "manner of Pearce's IDyOM, trained on the series' 51 major-key tunes and listening to each with a short-term "
              "model that learns the piece. It measures surprise (information content) and uncertainty (entropy) note by "
              "note: the Tune costs 1.98 bits a note, random scale notes 3.93; Part 42's kept draft 3.1 against a rejected "
              "draft's 3.8; probe tones rank C, D, F sharp as listeners do. Expectation is learned (a Saffran-style stream "
              "of tone words, heard and tested); repetition teaches it (a leap costs 4.8 bits, then 2.1); delay makes an "
              "ending more certain (the deceptive turn costs 6.3 bits and the final C only 0.9, against 1.2 undelayed); "
              "denial leaves the cost unpaid (F sharp, 10.9 bits, falling to 2.2 when repeated). It covers the ERAN and "
              "reward, Cheung's interaction of surprise and uncertainty, groove's inverted U and syncopation, the cues of "
              "expressed emotion (a quiz in four settings), chills, sad music, memory, and what does not replicate.",
        handoff="Origins and universals in Part 47; mastering and loudness in Part 57; recommendation in Part 63; machines "
                "that compose in Part 65; replication in Part 67.",
        outside="Part 14 for melody and the corpus; Part 15 for key and probe tones; Part 18 for cadences; Part 21 for form; "
                "Part 38 for syncopation; Part 42 for tension and the searcher; Part 45 for grouping. Entropy, Markov models.",
        objectives={
            "U": ["Hear expected, delayed and denied endings, a suspension and a Neapolitan, and say what each does.",
                  "Learn tone 'words' from a stream, and rank probe tones by fit.",
                  "Hear the cues of four expressed emotions, and four grooves of rising syncopation."],
            "M": ["Build a PPM listener with long- and short-term models, and compute surprise and uncertainty per note.",
                  "Compute transitional probabilities in a stream and a syncopation index for a pattern.",
                  "Compare melodies by mean surprise, and engineer endings by their cost in bits."],
            "D": ["Design a study measuring how much of moment-to-moment pleasure surprise and uncertainty predict."],
            "I": ["Build and delay expectations in songs and scores; choose music for its cues with measured effects."],
        },
        results=[
            ("Surprise", r"h(x) = -\log_2 p(x \mid \text{context})"),
            ("Uncertainty", r"H = -\textstyle\sum_x p(x)\log_2 p(x) \le \log_2 n"),
            ("The Tune", r"1.98 \text{ bits a note; random notes } 3.93"),
            ("Delay", r"\text{turn } 6.3 \text{ bits, arrival } 0.9 \ (\text{plain } 1.2)"),
            ("Statistical learning", r"P(\text{next} \mid \text{inside a word}) = 1, \ \text{across} \approx 1/3"),
        ],
        U=(0, 1, 2, 5, 6, 8, 9),
        D=(10,),
        I=(3, 4, 7),
        also=(("Monochord's listener: PPM, surprise and uncertainty, syncopation and statistical learning", "explainer/music/monochord/listener.py"),),
    ),
    Part(
        n=47, level="U", widget="prior", prereq=(1, 8, 11, 12, 14, 43, 46),
        question="What is shared by all the world's music, what is learned, and how much can transmission alone explain?",
        story="A vulture's wing bone with five holes lay in Hohle Fels cave for at least 35,000 years; a pipe its size, by "
              "Part 8's flute model, sounds about 766 Hz, and evenly spaced holes give uneven steps. Every society studied "
              "sings (Mehr's 315 ethnographies); lullabies and dance songs are recognized across cultures (an ear question "
              "in one melody sung both ways). Savage's statistical universals are checked on the series' 54 tunes, and the "
              "check's limits stated; the Tsimane' are indifferent to dissonance, so that taste is learned. Iterated "
              "reproduction reveals priors: 400 random three-interval rhythms tapped back by a simulated Bayesian listener "
              "go from 28 to 68 per cent near small-integer ratios, in its prior's proportions, and a 7/8 listener's chains "
              "end on 2:2:3. Twenty random melodies passed through forty simulated singers lose half their pitch levels, "
              "halve their steps and settle on simple lengths, and copying error falls from 0.31 to 0.08 a note; samplers "
              "forget the Tune, likeliest-value singers keep it. Tune families are drawn by Needleman-Wunsch alignment and "
              "UPGMA (the Tune, the Alphabet Song and Baa, Baa cluster apart; a simulated family's branching recovered 4.8 "
              "of 6 times on average). It covers birds, whales and Snowball with Rayleigh's test, infants, nPVI by language "
              "(French folk tunes 24.7, English 35.8, permutation p = 0.16), amusia, the Mozart effect and publication bias, "
              "transfer and therapy, the theories of origin, and the genetics of rhythm.",
        handoff="Digital audio in Part 48; melodic similarity at scale in Part 63; machines that compose in Part 65; research "
                "practice in Part 67; the Tune's whole family in Part 68.",
        outside="Part 1 and Part 8 for pipes; Part 5 for roughness; Part 11 for meter; Part 12 for scales; Part 14 for the "
                "corpus; Part 43 for phase correction; Part 46 for statistical learning. Bayesian inference, Markov chains, "
                "sequence alignment, hierarchical clustering, circular statistics, meta-analysis.",
        objectives={
            "U": ["Tell a lullaby from a dance song, and a consonant chord from a dissonant one, and say which preference is learned.",
                  "Hear a random rhythm become a simple one under iterated reproduction, and a random melody become singable.",
                  "Judge which of two dancers is on the beat, and hear a one-note change in the style of the Montreal battery."],
            "M": ["Simulate iterated reproduction with a Bayesian listener and show the chains converge to its prior.",
                  "Build a transmission chain of singers and measure pitch levels, step size, simple lengths and copying error.",
                  "Align and cluster melodies into a family tree; compute nPVI by group with a permutation test; apply Rayleigh's test."],
            "D": ["Design chains with each bias switched off, to find which universals need which biases."],
            "I": ["Read claims about music and the mind by sample, control, effect size and replication."],
        },
        results=[
            ("Iterated learning", r"x_{t+1} \sim p(\theta \mid d(x_t)) \ \Rightarrow\ x_\infty \sim p(\theta)"),
            ("Rhythm chains", r"28\% \to 68\% \text{ near small-integer ratios in 5 rounds}"),
            ("Transmission", r"\text{levels } 11.7 \to 5.6,\ \text{step } 5.6 \to 2.7 \text{ semitones}"),
            ("nPVI", r"\tfrac{100}{m-1}\textstyle\sum_k \left|\frac{d_k - d_{k+1}}{(d_k+d_{k+1})/2}\right|"),
            ("Rayleigh", r"R = \big|\tfrac1n\textstyle\sum_k e^{i\theta_k}\big|,\ p \approx e^{-nR^2}"),
        ],
        U=(0, 1, 2, 3, 4, 8, 11),
        D=(12,),
        I=(5, 6, 7, 9, 10),
        also=(("Monochord's origins: transmission, rhythm priors, alignment and trees, nPVI, Rayleigh's test", "explainer/music/monochord/origins.py"),),
    ),
    Part(
        n=48, level="U", widget="dither", prereq=(2, 3, 4, 30, 47),
        question="How can a list of numbers hold a sound exactly, and how many numbers, how precise, are enough?",
        story="44,100 samples a second came from video: three samples a line, 245 lines, 60 fields (or 294 and 50). Behind "
              "the accident is the sampling theorem, built here as a sum of sincs through a signal's samples (the error "
              "falls from 0.25 with 4 samples per point to 4 in 100,000 with 128) and proved by spectral copies. Aliasing "
              "folds 5 and 7 kHz to 3 and 1 kHz at 8 kHz sampling, and an ear question turns a sweep round; the stair-step "
              "is a picture of a hold whose images (33 dB down near 44 kHz) a filter removes, and the steps are heard "
              "before it does. Quantization measures 6.02 N + 1.76 dB within 0.1 dB from 5 bits up; an ear question hears "
              "4 bits with and without dither. Dither's moments are measured: none (error tied to the input), RPDF (mean "
              "freed), TPDF (mean and variance freed, a quarter of a step squared); a sine 0.4 of a step high vanishes "
              "without dither and survives with it. Noise shaping cuts the error below 4 kHz from -26 to -44 dB while the "
              "total rises; a one-bit delta-sigma modulator gains 9 and 15 dB per octave of oversampling for first and "
              "second order (75 dB at 64 times). Jitter costs -20 log10(2 pi f sigma), measured to 0.1 dB, and periodic "
              "jitter makes sidebands at -70 dB. Resampling, an ear question at 16 kHz, and the high-resolution debate "
              "(Meyer and Moran; Reiss) close it.",
        handoff="Filters, delay and reverb in Part 49; aliasing from distortion in Part 50; alias-free oscillators in Part 51; "
                "dither and true peaks in Part 57; perceptual coding in Part 58.",
        outside="Part 2 for waves; Part 3 for spectra and the Fourier transform; Part 4 for hearing's range and threshold; "
                "Part 30 for sound as numbers; Part 47 for blind testing. Fourier series, convolution, probability.",
        objectives={
            "U": ["Hear aliasing turn a sweep round, and hear the stair-step's images before a reconstruction filter.",
                  "Tell a 4-bit Tune with dither from one without, and a 16 kHz rate from 48 kHz.",
                  "Hear one bit at three speeds, and flat and shaped noise as residues."],
            "M": ["Reconstruct a band-limited signal from its samples by sinc interpolation and measure the truncation error.",
                  "Measure SNR against 6.02 N + 1.76 dB, and the error's mean and variance under no, RPDF and TPDF dither.",
                  "Build error-feedback noise shaping and a delta-sigma modulator, and measure their in-band SNR."],
            "D": ["Find how far below Nyquist music can be sampled, by sparsity and l1 recovery, before listeners notice."],
            "I": ["Choose word lengths, dither and shaping for recording, mastering and delivery; test formats blind and level-matched."],
        },
        results=[
            ("Sampling theorem", r"x(t) = \textstyle\sum_n x[n]\,\mathrm{sinc}(f_s t - n), \quad f_s > 2B"),
            ("Aliasing", r"f \mapsto |f - f_s \,\mathrm{round}(f/f_s)|"),
            ("Quantization", r"\mathrm{SNR} = 6.02\,N + 1.76 \text{ dB}"),
            ("TPDF dither", r"\mathrm{E}[e \mid x] = 0,\ \mathrm{Var}[e \mid x] = \Delta^2/4"),
            ("Jitter", r"\mathrm{SNR} = -20\log_{10}(2\pi f \sigma_t)"),
        ],
        U=(0, 1, 2, 3, 4, 10),
        D=(11,),
        I=(5, 6, 7, 8, 9),
        also=(("Monochord's converters: sampling, reconstruction, quantization, dither, shaping, delta-sigma, jitter", "explainer/music/monochord/digital.py"),),
    ),
    Part(
        n=49, level="U", widget="biquad", prereq=(3, 7, 30, 45, 48),
        question="How do delay and addition make every filter, echo and reverberation in a studio?",
        story="In 1947 Bill Putnam sold his studio bathroom's echo as art; in 1962 Schroeder built a room out of four combs "
              "and two all-passes, and an ear question sets it beside a simulated tiled room. The part builds convolution "
              "sample by sample and hears an echo; feedback places poles (a one-pole low-pass, the z-plane, a band-pass at "
              "Q 50 ringing a quarter of a second); the cookbook biquads draw five equalizers, matched by ear in an ear "
              "question, and a Butterworth built by the bilinear transform matches SciPy to rounding. Sixty all-passes "
              "leave every level unchanged and turn a snare into a chirp (an ear question). Combs make notches, peaks and "
              "a 220 Hz pitch from noise; a flanger, a chorus and a phaser move them. A tiled room by Allen and Berkley's "
              "image sources rings 1.22 s by Schroeder's backward integration, within 2 per cent of Eyring's 1.24; Farina's "
              "sweep recovers its response (error 19 dB down) and parts a distorting loudspeaker's harmonics. Schroeder's "
              "reverberator stays sparse (echo density 0.2) where an eight-line feedback delay network fills in; octave "
              "bands separate stone from steel; a steel plate by finite differences (246 by 123 points) starts bright and "
              "rings 2.6 s in the bass, 1.0 s at 4 kHz; a spring is a loop of 80 all-passes.",
        handoff="Nonlinear effects in Part 50; resonant filters in Part 51; delay-line physical models in Part 52; real halls "
                "in Part 55; equalizers and reverbs in a mix in Part 56.",
        outside="Part 3 for spectra; Part 7 for Karplus-Strong; Part 30 for sound as numbers; Part 45 for the auditory scene; "
                "Part 48 for sampling. Convolution, the z-transform, linear algebra (orthogonal matrices), finite differences.",
        objectives={
            "U": ["Match a groove to a low-pass, a high-pass and a peak by ear, and hear a ringing pole.",
                  "Hear an all-pass smear a snare, combs make a pitch, and a flanger, chorus and phaser move.",
                  "Tell Schroeder's reverberator from a simulated room, and hear a plate, a spring and a cathedral."],
            "M": ["Convolve by hand and by FFT; design biquads from the cookbook and read them from poles and zeros.",
                  "Simulate a room by image sources and measure RT60 by Schroeder integration against Sabine and Eyring.",
                  "Measure an impulse response with an exponential sweep; build a feedback delay network and a plate."],
            "D": ["Find the smallest feedback delay network that passes, blind, for a measured room."],
            "I": ["Equalize, delay and reverberate in a mix; measure a room by sweep and predict it by Sabine."],
        },
        results=[
            ("Convolution", r"y[n] = \textstyle\sum_k h[k]\,x[n-k]"),
            ("Stability", r"|p_i| < 1 \text{ for every pole}"),
            ("Sabine", r"T_{60} = 0.161\,V / (S\alpha)"),
            ("Schroeder integration", r"E(t) = \int_t^\infty h^2(\tau)\,d\tau"),
            ("Comb decay", r"g = 10^{-3D/(f_s T_{60})}"),
        ],
        U=(0, 1, 2, 3, 4, 5),
        D=(11,),
        I=(6, 7, 8, 9, 10),
        also=(("Monochord's effects rack: biquads, combs, image-source rooms, sweeps, Schroeder, FDN, plate, spring", "explainer/music/monochord/effects.py"),),
    ),
    Part(
        n=50, level="U", widget="compressor", prereq=(4, 8, 40, 48, 49),
        question="What do effects that are not linear, or that change with the signal, do to sound, and how are they built?",
        story="Two accidents made two genres: a damaged amplifier on Rocket 88 (1951), and Auto-Tune set to act instantly on "
              "Believe (1998); an ear question hears Part 8's voice sung 28 cents off and hard-tuned to 0.6. Shapers make "
              "harmonics (odd only, for odd shapers: a hard clip's third at -11 dB, fifth at -18.5), Chebyshev polynomials "
              "deliver any harmonics exactly at full size (third -6.02 dB, fifth -12.04) and differently when quiet; two "
              "tones intermodulate (a fifth's products fall on multiples of 110 Hz, a third's on 55: the power chord); a "
              "clipped sweep aliases (an ear question), and the alias energy falls from -26.8 dB to -32.5 by antiderivative "
              "antialiasing and -47.3 by 8x oversampling. A compressor after Giannoulis, Massberg and Reiss draws its static "
              "curves, attacks in 12 ms, halves a groove's loudness spread (an ear question) while its attack keeps the punch "
              "(crest factor up); limiters, gates and a kick-keyed sidechain follow. Resampling ties pitch to time; PSOLA "
              "and the phase vocoder untie them; YIN and a corrector at three speeds tune a voice; a 16-band vocoder and ring "
              "modulation close it.",
        handoff="Waveshaping and alias-free oscillators in Part 51; nonlinear physical models in Part 52; compressors in a mix in "
                "Part 56; limiters in Part 57; pitch tracking in Part 61.",
        outside="Part 4 for difference tones; Part 8 for the voice's source and filter; Part 40 for the guitar; Part 48 for "
                "aliasing; Part 49 for filters. Polynomials, Fourier series, autocorrelation, the short-time Fourier transform.",
        objectives={
            "U": ["Hear hard-tuned from natural, three shapers on one note, and a power chord against a major chord distorted.",
                  "Hear aliasing in a clipped sweep, a compressed groove at matched loudness, pumping, and a sidechain duck.",
                  "Hear pitch shifted by resampling and by PSOLA, a stretch by overlap-add and by the phase vocoder, and a vocoder."],
            "M": ["Design a Chebyshev shaper by its harmonics; measure intermodulation and aliasing, with ADAA and oversampling.",
                  "Build a feedforward compressor with a soft knee, attack and release; measure its curves and a groove's spread.",
                  "Track pitch by YIN, correct it with PSOLA at a chosen speed, stretch by the phase vocoder, and vocode."],
            "D": ["Find the smallest neural amplifier model indistinguishable at every knob setting and free of aliasing."],
            "I": ["Choose fifths under distortion, compressor timing for punch, sidechains for space, and correction speed for style."],
        },
        results=[
            ("Chebyshev", r"T_n(\cos\theta) = \cos n\theta"),
            ("Intermodulation", r"m f_1 \pm n f_2"),
            ("Static curve", r"y = T + (x - T)/R \quad (x > T + W/2)"),
            ("Ring modulation", r"\sin a \sin b = \tfrac12[\cos(a-b) - \cos(a+b)]"),
            ("Phase vocoder", r"\omega_k + \Delta\phi_k / H_a \Rightarrow \phi \mathrel{+}= \hat\omega_k H_s"),
        ],
        U=(0, 1, 2, 3, 4, 7, 8),
        D=(11,),
        I=(5, 6, 9, 10),
        also=(("Monochord's dynamics: shapers, Chebyshev, ADAA, compressor, gate, OLA, phase vocoder, YIN, PSOLA, vocoder", "explainer/music/monochord/dynamics.py"),),
    ),
    Part(
        n=51, level="U", widget="ladder", prereq=(3, 8, 48, 49, 50),
        question="How does a synthesizer make a sound from nothing, and how is its analogue circuit run inside a computer?",
        story="The first synthesizer weighed nearly two hundred tons: Cahill's Telharmonium (1906) summed dynamos' near-sines and sent them down telephone lines; Moog's modules (1964) and Switched-On Bach (1968) did the job by subtraction. An ear question hears forty hand-set sines against a two-oscillator patch a search fitted to them (3.0 dB away, missing a bump a low-pass cannot make). A sawtooth is built from sines; the Hammond's nine drawbars borrow tempered wheels (fifths 2.0 cents flat, the third 13.7 sharp); four sources and a filter sweep follow. A naive digital sawtooth aliases (25.6 dB at 110 Hz to 10.3 at 3.5 kHz, 3 dB worse an octave); PolyBLEP cuts it by 14 to 16 dB (an ear question), BLIT sits near 64. The ladder is four poles and a loop, 1/((1+s)^4+k), ringing at k = 4 and losing bass as 1/(1+k); run against its circuit equations, forward steps converge at 6 dB per doubling and the trapezoid with Newton at 12 (37.2 dB at 48 kHz); an ear question hears the saturating circuit against its linear equations, and past k = 4 the filter sings the Tune. Envelopes, LFOs, pulse width, hard sync and unison move one note; wavetables scan eight cycles (aliasing 18 dB naive, 56 band-limited); struck resonators make an 808-style kit (decay 0.454 s against 0.453 predicted); a grid search fits patches, recovers a hidden one, and fails on an organ (27 dB).",
        handoff="FM, granular and physical-model synthesis in Part 52; MIDI and the sequencer in Part 53; synthesizers in a mix in "
                "Part 56; transcription, the inverse problem for recordings, in Part 61; differentiable synthesizers in Part 66.",
        outside="Part 3 for Fourier series; Part 6 for equal temperament; Part 8 for source and filter; Part 40 for the 808; "
                "Part 48 for aliasing; Part 49 for poles and filters. Laplace transforms, ordinary differential equations, "
                "Newton's method, Runge-Kutta.",
        objectives={
            "U": ["Hear a fitted patch against its target, three Hammond registrations, and a filter sweep with and without resonance.",
                  "Hear a naive sawtooth alias against PolyBLEP, the ladder at three resonances, and its circuit against its equations.",
                  "Hear three envelopes on one patch, vibrato, tremolo and a wobble, pulse-width modulation, hard sync and unison."],
            "M": ["Build naive, PolyBLEP, BLIT and additive sawtooths, and measure each one's aliasing against pitch.",
                  "Derive the ladder's response and its k = 4 edge; step its circuit forward and by the trapezoid with Newton.",
                  "Build envelopes, wavetables, struck-resonator drums, and a grid search that fits a patch to harmonic levels."],
            "D": ["Decide whether gradient descent through a differentiable ladder fits real notes as reliably as a search."],
            "I": ["Choose an oscillator algorithm, a filter solver and a sample rate for a plug-in, and a patch for a sound."],
        },
        results=[
            ("Sawtooth", r"\tfrac{2}{\pi}\sum_k (-1)^{k+1} \sin(2\pi k f t)/k"),
            ("Ladder", r"H(s) = 1/\big((1 + s/\omega_c)^4 + k\big)"),
            ("Edge", r"(1 + j)^4 = -4 \Rightarrow k = 4"),
            ("Pulse", r"|a_k| \propto |\sin(\pi k w)|/k"),
            ("Resonator", r"\tau = 2Q/(2\pi f)"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7),
        D=(11,),
        I=(5, 8, 9, 10),
        also=(("Monochord's synthesizer: oscillators, the ladder and its solvers, envelopes, wavetables, drums, patch fitting", "explainer/music/monochord/synth.py"),),
    ),
]
