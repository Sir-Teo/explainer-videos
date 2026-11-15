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
]
