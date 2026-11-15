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
]
