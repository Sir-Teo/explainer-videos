"""Act II, Notes: Parts 10 to 22 as they are built (see ``videos/music/course/__init__.py``)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=10, level="U", widget="notation",
        question="What does each way of writing music down keep, what does it throw away, and how much of a piece "
                 "of music is on its page?",
        story="A clay tablet from Ugarit, about 1400 BCE, holds the oldest nearly complete piece of written music: "
              "the names of pairs of lyre strings, each followed by a number. Nobody knows how it goes, because "
              "the scribe left out what every musician of the city knew. That is the problem of notation, and the "
              "part follows a thousand years of answers. Neumes record only whether a melody rises or falls: 85 "
              "melodies on six notes fit the signs over the Tune's first phrase. Guido of Arezzo's lines, about "
              "1025, turn pitch into height on a page, a graph three centuries before Oresme, though one that "
              "counts the steps of a scale and hides which of them are small. Franco of Cologne's shapes give "
              "notes their lengths; dots and ties write any length that halvings reach; bar lines and scores let "
              "many read together. Tablature and figured bass write what to do instead of what will sound, and "
              "each stands for millions of choices that the staff, or the player, must make. Gongche and jianpu "
              "write a note's place in its scale, and guqin tablature a gesture with no rhythm at all. A piano "
              "roll and a MIDI file keep one performance to the millisecond and forget how its notes are spelled, "
              "which in meantone is a difference of 41 cents; MusicXML and MEI keep the page. Then the count: the "
              "Tune's page is 168 bits and its sound 127,000 times as many, and a performance by four measured "
              "rules shows where some of the difference lies. The frontier is the way back, from a page of "
              "pixels to notes. The Tune is read from ten notations, and its last phrase is played as none of "
              "them says.",
        handoff="Part 11 takes the note values and bars of this part and asks where rhythm and metre come from. Key "
                "signatures and the spelling of notes return with scales and keys (Parts 12 and 15); figured bass "
                "grows into harmony (Parts 17 and 18); neumes and mensural notes return in their own centuries "
                "(Parts 23 and 24); what a performer adds is Part 43; MIDI returns with the sequencer (Part 53) "
                "and when machines transcribe sound (Part 61).",
        outside="Part 1 for ratios and the Tune; Part 6 for meantone and why G sharp is not A flat; Part 7 for why "
                "one note sounds different on different strings. Logarithms to base two for counting bits; "
                "nothing else.",
        objectives={
            "U": ["Read a melody from a staff, from numbered notation and from tablature, and say what each tells you.",
                  "Explain how note shapes, dots and ties write duration, and what a bar line is for.",
                  "Say what neumes, tablature, figured bass and a MIDI file each leave out."],
            "M": ["Count the melodies that fit a contour, and the tablatures of a melody, by dynamic programming.",
                  "Write any length k/2^n with dots and ties, and prove the rule for dots.",
                  "Compute the bits in a score and in its sound, and what a round trip through a format loses."],
            "D": ["Describe the pipeline of optical music recognition and why a tilted or speckled page breaks it.",
                  "Say what is solved and open in reading music by machine, and where the encoding standards stand."],
            "I": ["Choose a notation or a file format for a task by what it must keep.",
                  "Keep spelled pitches and exact durations in software, and convert at the edges.",
                  "Read and realize a figured bass or a chord chart, knowing what is left to you."],
        },
        results=[
            ("Melodies that fit a contour", r"W_k(s) = \sum_{s' \text{ allowed by sign } k} W_{k+1}(s'),\qquad W_n(s) = 1"),
            ("A dotted note", r"1 + \tfrac12 + \tfrac14 + \cdots + \tfrac{1}{2^n} = 2 - \tfrac{1}{2^n}"),
            ("Perfect time", r"\text{breve, semibreve, semibreve, breve} \;=\; 3,\ 1,\ 2,\ 3"),
            ("A sharp and its flat, in meantone", r"\frac{8/5}{25/16} = \frac{128}{125} \approx 41 \text{ cents}"),
            ("The Tune's page", r"42 \times (\log_2 6 \to 3 \;+\; \log_2 2 = 1) = 168 \text{ bits}"),
            ("Sound against page", r"\frac{27.7\ \text{s} \times 48000 \times 16}{168} \approx 1.3 \times 10^{5}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 9),
        D=(10,),
        I=(5, 8),
        also=(("Monochord's score: spelled pitches, exact durations, readers and writers, and what notations keep, counted", "explainer/music/monochord/score/__init__.py"),
              ("The engraver and the other notations, drawn", "explainer/music/staff.py")),
    ),
    Part(
        n=11, level="U", widget="rhythm",
        question="Where do beat and metre come from, how are rhythms counted and measured, and what is a rhythm "
                 "when it is played too fast to count?",
        story="Play sixteen identical strokes and listeners hear them in pairs, tick and tock: Bolton found it in "
              "1894, and a century later the brain's response was seen to differ on the ticks. Metre is something "
              "a listener adds. The part starts from a pulse and finds the window in which a beat can be felt, "
              "from about a quarter of a second to two seconds, steadiest near two beats a second. A metre is "
              "pulses nested in pulses, drawn as Lerdahl and Jackendoff's grid of dots; a toy pulse finder taps "
              "the Tune at the tempo it was played. Accents tell the listener which beats are strong: louder "
              "sounds begin groups and longer ones end them. The beat is cut in twos and threes. Syncopation is "
              "a note on a weak pulse before a silent strong one, and Longuet-Higgins and Lee's index measures "
              "it: 0 for a rhythm on the beats, 4 for the son clave, 7 for the off-beats; listeners want most to "
              "move in between. Six eighth notes are two threes or three twos, and music that changes between "
              "them, or plays both at once, is hemiola and polyrhythm. Seven pulses make three unequal beats, "
              "three ways, and the count of such metres obeys a(n) = a(n-2) + a(n-3). Swing is not a ratio: on "
              "records the short note stays near 100 ms, so the ratio is two to one at one tempo only. Then "
              "three against two is sped up until, near twenty clicks a second, it stops being a rhythm and "
              "becomes two notes a perfect fifth apart: an interval is a polyrhythm too fast to count. The "
              "frontier is the telephone game on rhythms, which reads a listener's expectations, and what it "
              "found in fifteen countries. The Tune is played in four, as a waltz, in five, in seven, swung, "
              "and with a hemiola.",
        handoff="Part 12 turns from when to which: the notes a piece chooses from. Rhythm returns inside melody "
                "(Part 14) and harmonic rhythm (Part 18); its mathematics, necklaces and evenness, in Part 33; "
                "tala and the timelines of West Africa in Parts 34 and 37; swing in Part 38; the listener's "
                "expectations in Part 46; and machines that find the beat in Part 62.",
        outside="Part 1 for the ratio 3:2; Part 4 for the lowest pitch the ear hears; Part 9 for the drums; "
                "Part 10 for note values, dots and bar lines. Fractions and logarithms; nothing else.",
        objectives={
            "U": ["Turn a tempo into the time between beats, and read a time signature as a nesting of pulses.",
                  "Say what makes a beat strong, and how loudness and length group sounds.",
                  "Clap three against two, and count a bar of seven three ways."],
            "M": ["Compute a metre's weights and a rhythm's syncopation index.",
                  "Count the metres made of twos and threes, and prove the recurrence.",
                  "Derive the swing ratio from a short note of fixed length, and the interval that a polyrhythm becomes."],
            "D": ["Describe the telephone game on rhythms and what it has and has not shown.",
                  "Say what is known and disputed about syncopation, microtiming and the urge to move."],
            "I": ["Choose a tempo and a level of the metre to beat or to click.",
                  "Programme a swung or an uneven metre knowing its values in milliseconds.",
                  "Make a new rhythm by sliding an old one against the grid."],
        },
        results=[
            ("Tempo", r"T = \frac{60}{\text{beats per minute}}\ \text{s};\qquad 0.25\ \text{s} \lesssim T \lesssim 2\ \text{s}"),
            ("A metre's weights", r"\tfrac44 \text{ in sixteenths}: \; 5\,1\,2\,1\,3\,1\,2\,1\,4\,1\,2\,1\,3\,1\,2\,1"),
            ("Syncopation", r"S = \sum_{\text{notes } n} \max\big(0,\ \max_{\text{rests before the next note}} w_r - w_n\big)"),
            ("Twos and threes", r"a(n) = a(n-2) + a(n-3):\quad a(7) = 3,\ a(12) = 12"),
            ("Swing", r"\text{ratio} = \frac{T - 0.1\ \text{s}}{0.1\ \text{s}} \;\Rightarrow\; 2:1 \text{ at } 200 \text{ to the minute}"),
            ("Rhythm into pitch", r"3 : 2 \ \text{at } 100 \text{ cycles a second} \;=\; 300\ \text{Hz} : 200\ \text{Hz} \;=\; 702 \text{ cents}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 9),
        D=(10,),
        I=(7, 8),
        also=(("Monochord's rhythm engine: metres, syncopation, the pulse, polyrhythm, swing, the telephone game", "explainer/music/monochord/rhythm.py"),
              ("A kit of struck things for marking time", "explainer/music/monochord/instruments/drumkit.py")),
    ),
    Part(
        n=12, level="U", widget="scale",
        question="Why do keyboards have seven white keys and five black, what makes that choice of notes special, "
                 "and how many scales could there be?",
        story="Every octave of every keyboard has seven white keys and five black, and the part derives that "
              "layout from the fifth of Part 1. Stack fifths and fold them into an octave: at five, seven and "
              "twelve notes the steps between neighbours come in just two sizes, and those stacks are the "
              "pentatonic, diatonic and chromatic scales. The three-gap theorem says a stack never has more than "
              "three sizes of step, and the sizes at which it has two (2, 3, 5, 7, 12, 17, 29, 41, 53) are the "
              "denominators of Part 6's continued fraction. Seven notes give seven modes, which fall in order of "
              "brightness along the chain of fifths, each the one before with a single note lowered. The white "
              "keys are also the most even way to choose seven notes of twelve; every kind of interval in them "
              "comes in two sizes, with the tritone as a single landmark; and each interval occurs a different "
              "number of times (2, 5, 4, 3, 6, 1), so that a move of a fifth changes one note, which is the "
              "system of keys. Minor borrows a leading note and so has three forms. Whole-tone and octatonic "
              "scales map onto themselves and have no home. A fourth can be filled six ways, and south Indian "
              "theory makes 2 x 6 x 6 = 72 parent scales that way; maqam and slendro divide the octave where no "
              "piano key lies. Burnside's lemma counts 352 shapes of scale on twelve notes, 66 of them with seven "
              "notes, and among those the white keys are the most even, have the most fifths and are the "
              "smoothest. The frontier is why the world's scales have five to seven unequal steps. The Tune is "
              "played in the seven modes and in scales of five, six and eight notes.",
        handoff="Part 13 sounds the notes of a scale together: intervals and chords. Melody moves through the "
                "scale in Part 14; the deep-scale property becomes the system of keys in Part 15; evenness and "
                "necklaces return in Part 33; raga, maqam and the gamelan's tunings get Parts 34 to 36; the "
                "blues scale and its bent notes, Part 38.",
        outside="Part 1 for the fifth; Part 5 for roughness; Part 6 for commas, meantone and continued fractions; "
                "Part 10 for the hexachord and spelling; Part 11 for necklaces. Counting and modular arithmetic.",
        objectives={
            "U": ["Build the pentatonic, diatonic and chromatic scales by stacking fifths.",
                  "Name the seven modes, put them in order of brightness, and write each on any note.",
                  "Write the three forms of the minor scale and say what each is for."],
            "M": ["Find the sizes of step in a stack of any generator, and where there are two.",
                  "Compute a scale's interval vector, its common tones under transposition, and its evenness.",
                  "Count scale shapes with Burnside's lemma, and the melakartas by their rule."],
            "D": ["State the three-gap theorem and its link to continued fractions.",
                  "Set out the competing explanations for scales of five to seven unequal steps."],
            "I": ["Choose a mode or a symmetric scale for the colour it gives.",
                  "Move between keys by the notes they share.",
                  "Lay out the notes of an instrument that plays one scale."],
        },
        results=[
            ("Stacks of fifths", r"\text{two sizes of step at } n = 2, 3, 5, 7, 12, 17, 29, 41, 53"),
            ("The three-gap theorem", r"\{k\alpha \bmod 1\}_{k<n} \text{ cut the circle into gaps of at most three lengths}"),
            ("The most even seven of twelve", r"\left\lfloor \tfrac{12k + 5}{7} \right\rfloor = 0, 2, 4, 5, 7, 9, 11"),
            ("The diatonic interval vector", r"\langle 2, 5, 4, 3, 6, 1 \rangle"),
            ("Scale shapes on twelve notes", r"\tfrac{1}{12}\sum_{d \mid 12} \varphi(d)\, 2^{12/d} = 352"),
            ("Parent scales", r"2 \times \tbinom{4}{2} \times \tbinom{4}{2} = 72"),
        ],
        U=(0, 1, 3, 4, 5, 6),
        D=(2, 10),
        I=(7, 8, 9),
        also=(("Monochord's scales: stacks, modes, evenness, interval vectors, necklaces, parent scales", "explainer/music/monochord/scales.py"),
              ("Pictures of scales: a keyboard, the octave as a circle, steps as a bar", "explainer/music/scaleviz.py")),
    ),
    Part(
        n=13, level="U", widget="chord",
        question="Why are C-E-G and E-G-C the same chord, why are chords built in thirds, and why is the same chord "
                 "clear in the middle of the piano and muddy at the bottom?",
        story="In 1722 Rameau claimed that a chord is the same chord whichever of its notes is lowest, and the part "
              "works up to that claim and tests it. An interval has a number, counted in letters, and a quality, "
              "and the quality turns out to be a direction on the line of fifths: sharpward is major, flatward "
              "minor. Inversion sends each interval to its partner (the numbers add to nine), leaving six interval "
              "classes. Three notes with no two of them a tone or less apart are exactly the four triads, so a "
              "stack of thirds is what is left when neighbours are forbidden; a major scale holds three major "
              "triads, three minor and one diminished, and the three major ones hold every note. A chord has a "
              "root in any inversion, and the reason is the missing fundamental of Part 4: a major triad is "
              "harmonics 4, 5 and 6 of a note two octaves below its root. Parncutt's model counts each note's "
              "votes for the roots it could be a harmonic of; the major triad is clear, the minor a little less, "
              "the diminished triad ties with a note that is not in it, and A-C-E-G splits between A and C. A "
              "fourth note gives the seventh chords; the dominant seventh carries the scale's one tritone, which "
              "resolves by two semitones in contrary motion, and in harmonics 4:5:6:7 it fuses. Thirds stacked to "
              "the thirteenth are the whole scale. Voicing matters as much as naming: a major third is one and a "
              "half critical bands wide high up and a third of one at the bottom of the piano, so chords are "
              "spaced wide below and close above, as the harmonic series is; the root is the note to double, the "
              "fifth can be left out, the third cannot, and a distorting amplifier leaves only root and fifth. "
              "Chords are written as figured bass, Roman numerals, lead-sheet symbols and Nashville numbers, and "
              "laid out on Euler's lattice of fifths and thirds, where neighbouring triads share two notes. The "
              "frontier is what makes a chord sound as it does, and why naming chords from sound is hard. The "
              "Tune is played over one set of chords in six voicings.",
        handoff="Part 14 asks which notes of a melody are chord notes; Part 15 gives the chords their jobs in a "
                "key; Parts 16 and 17 are voice leading; Part 18, progressions. Euler's lattice returns as "
                "geometry in Part 32, shells and chord scales in Part 39, distortion in Part 50, and machines "
                "that name chords in Part 62.",
        outside="Part 1 for the harmonic series; Part 4 for critical bands and the missing fundamental; Part 5 for "
                "roughness; Part 6 for pure intervals and commas; Part 10 for figured bass and spelling; Part 12 "
                "for the scale, the line of fifths and the nineteen shapes of three notes.",
        objectives={
            "U": ["Name any written interval and its inversion, and place it on the line of fifths.",
                  "Build the four triads and the five common seventh chords on any note, and find them in a major scale.",
                  "Find a chord's root and inversion, and write it as figures, a Roman numeral and a lead-sheet symbol."],
            "M": ["Show that three notes with no two adjacent form one of the four triads.",
                  "Run Parncutt's root model on a chord and report its root and its ambiguity.",
                  "Compute a voicing's roughness, and the lowest register at which an interval stays clear."],
            "D": ["Explain the root as a missing fundamental, and say where that explanation strains (the minor triad).",
                  "Set out why roughness and harmonicity together still misplace the augmented triad."],
            "I": ["Space a chord for a given register, and choose what to double and what to leave out.",
                  "Read and write a chart in lead-sheet symbols and in numbers, and transpose it.",
                  "Move between chords by the smallest motion, using inversions."],
        },
        results=[
            ("Quality from the line of fifths", r"|d| \le 1 \text{ perfect};\quad 2 \le |d| \le 5 \text{ major } (d>0) \text{ or minor } (d<0);\quad |d| \ge 6 \text{ augmented or diminished}"),
            ("Inversion", r"n + n' = 9,\qquad s + s' = 12"),
            ("Triads", r"a + b + c = 12,\ a, b, c \ge 3 \ \Rightarrow\ \{3,3,6\},\ \{3,4,5\},\ \{3,5,4\},\ \{4,4,4\}"),
            ("The major triad", r"4 : 5 : 6 \quad \text{(the minor: } 10 : 12 : 15)"),
            ("Root salience (Parncutt)", r"S(r) = \sum_{p \in \text{chord}} w\big((p - r) \bmod 12\big),\quad w(0, 7, 4, 10, 2) = 10, 5, 3, 2, 1"),
            ("The harmonic seventh", r"1200 \log_2 \tfrac{7}{4} = 968.8 \text{ cents}"),
        ],
        U=(0, 1, 2, 3, 4, 6),
        D=(5, 11),
        I=(7, 8, 9),
        also=(("Monochord's chords: intervals, spelling, inversion, roots, voicings, the Tonnetz, a chord listener", "explainer/music/monochord/chords.py"),
              ("Pictures of chords: Euler's lattice, bars for the twelve notes, rows of partials", "explainer/music/chordviz.py"),
              ("The engraver, now with chords and a grand staff", "explainer/music/staff.py")),
    ),
    Part(
        n=14, level="U", widget="melody",
        question="What do melodies do, which of those things would any string of notes in a small range do anyway, "
                 "and can a machine learn to expect the next note?",
        story="Textbooks have said for four hundred years that a leap should be followed by a step back. The part "
              "tests that on fifty-four tunes that half the world can sing, and then on the same tunes with their "
              "notes shuffled: the shuffled ones obey the rule more often. A melody is first a contour, which "
              "listeners keep before the intervals; it is the same tune in any key, and eight moves of up, down "
              "and repeat tell all fifty-four apart. Half of all moves are steps, a quarter repeats and a quarter "
              "leaps; steps mostly fall and fourths mostly rise; the ear splits a line that leaps too far into "
              "two streams. A tune fits in an octave and lives near its middle. Phrases are arches about a breath "
              "long that end lower than they began. Then the leap rule is explained: a leap away from the middle "
              "of a small range lands near its edge, and the next note is probably back toward the middle, as it "
              "is for a die; real tunes and shuffled ones both turn back after leaps away from the middle and "
              "carry on after leaps toward it (von Hippel and Huron, 2000). What chance does not explain is the "
              "rest: gap-fill in part, momentum after a step, leaps that land on the notes of the home chord, "
              "tendency tones (7 to 1, 4 to 3, 6 to 5), repetition and sequence, and phrases that end as "
              "questions until the last one answers on the first degree. A note carries 4.3 bits if nothing is "
              "known, 3.2 given which notes are common and 2.6 given the note before; patterns of moves follow "
              "Zipf's law. A model that only counts what followed what is surprised by the Tune exactly once, at "
              "its leap of a fifth, and finds a minor-key tune from another tradition hardest of all. Speech has "
              "its own melody, which a song must respect. The frontier is predicting what a listener expects, "
              "and what makes a tune stick. The Tune's first phrase is played eight ways.",
        handoff="Part 15 turns tendency tones and the note that phrases end on into a key. Two melodies at once are "
                "Parts 16 and 20; motive and sequence grow into form in Part 21; melody is the whole art in Parts "
                "34 and 35; expectation becomes a theory of emotion in Part 46; and the counting model is the "
                "ancestor of the composing machines of Part 65.",
        outside="Part 4 for streaming and pitch; Part 10 for contour codes; Part 11 for rhythm and stress; Part 12 "
                "for scale degrees; Part 13 for the home chord and the tritone. Probability: conditional "
                "probability, regression to the mean, entropy in bits.",
        objectives={
            "U": ["Describe a melody by its contour, moves, range and phrase shapes.",
                  "Name the tendency tones of a major scale and say where each goes.",
                  "Mark a tune's phrases, its repeats and its sequences, and write its plan in letters."],
            "M": ["Test a claimed regularity of melody against shuffled notes and against a random walk in the same range.",
                  "Compute the chance that a die turns back after a rise, and explain the leap rule by regression to the mean.",
                  "Train a variable-order Markov model on a corpus and read a tune's information content in bits."],
            "D": ["Separate what follows from range and step size from what needs a composer.",
                  "Say why a model's surprise depends on the music it was trained on."],
            "I": ["Write a singable tune: within an octave, mostly steps, with a peak and a repeated motive.",
                  "Set words so that stress, or tone, agrees with the melody.",
                  "Use a contour code to find a tune from a hummed fragment."],
        },
        results=[
            ("Moves in 54 tunes", r"\text{steps } 50\%,\ \text{repeats } 25\%,\ \text{leaps } 25\%;\quad \overline{|\Delta|} = 2.0 \text{ semitones}"),
            ("After a leap, turning back", r"\text{tunes } 63\%,\quad \text{shuffled } 79\%;\qquad \text{away from the middle } 75\%,\ \text{toward it } 20\%"),
            ("A die", r"P(X_3 < X_2 \mid X_2 - X_1 \ge 2,\ X_3 \ne X_2) = \tfrac{4}{5}"),
            ("Information in a note", r"\log_2 20 = 4.3 \ \to\ H_0 = 3.2 \ \to\ H_1 = 2.6 \text{ bits}"),
            ("Surprise", r"h(x_t) = -\log_2 p(x_t \mid x_{t-n}, \dots, x_{t-1})"),
            ("Zipf's law for pairs of moves", r"f(r) \propto r^{-1.3}"),
        ],
        U=(0, 1, 2, 3, 4, 7, 8),
        D=(5, 12),
        I=(11,),
        also=(("Monochord's melodies: counts, chance baselines, a variable-order model of the next note", "explainer/music/monochord/melody.py"),
              ("The corpus: fifty-four traditional tunes in scale degrees", "explainer/music/monochord/tunes.py"),
              ("Pictures of melodies: a tune as bars in time and pitch, bar charts, a tune against itself", "explainer/music/melodyviz.py")),
    ),
    Part(
        n=15, level="U", widget="key",
        question="What is a key, where does a listener's sense of home come from, and how can a machine find it?",
        story="Play four chords and then a single tone, and every listener can say how well the tone fits. Krumhansl "
              "and Kessler did that in 1982 for all twelve notes: the ratings form a hierarchy, the tonic on top, "
              "then its triad, then the scale, then the five notes outside it. The same ranking is found by "
              "counting how much of the time each note sounds in fifty-four tunes (r = 0.92), newcomers to "
              "Indian music pick up a raga's ranking from short passages, and children acquire a key over "
              "years: a key is learned statistics. In a key the seven chords have three jobs (tonic, "
              "predominant, dominant), because the chords on four and five hold every leaning note of Part 14, "
              "and four cadences punctuate phrases. A key finder correlates the notes of a piece with the "
              "profile of each of the 24 keys. With the listeners' ratings it is right 81 times in a hundred on "
              "the tunes in all twelve keys, usually missing by a fifth; with profiles counted from music, 98; "
              "\"the last note\" alone is right 91 times; five notes are usually enough. The best clue is the "
              "rarest interval: two notes a tritone apart lie in only two major scales, and one more note "
              "decides. The Tune uses six notes that belong to C major and F major alike, which is why the "
              "key finder wavers and why a key is a matter of weights, not of membership. Keys a fifth apart "
              "share six notes; the 24 profiles' similarities lay the keys on a torus, with relative and "
              "parallel minors beside each major key; signatures are addresses on the circle of fifths. Music "
              "leaves home by a new leading note and a pivot chord: keys a fifth apart share four triads, two "
              "fifths apart two, further none; a tonicization visits and a modulation stays. A minor key "
              "borrows a major dominant. A Dorian sea shanty is in neither mode, and the key finder says so "
              "by being wrong. In equal temperament every key is the same key, moved; the characters of keys "
              "came from unequal tunings. The frontier is whether keys are everywhere, when major and minor "
              "condensed out of the modes, and what exactly a listener stores. The Tune travels through all "
              "twelve keys and ends on a deceptive cadence.",
        handoff="Act III begins: two voices in Part 16, four in Part 17, progressions in Part 18, distant keys "
                "quickly in Part 19. Form as a journey between keys is Part 21. The torus returns as geometry "
                "in Part 32, and finding the key of a recording in Part 62.",
        outside="Part 6 for temperaments; Part 12 for the scale, the line of fifths and the interval vector; "
                "Part 13 for triads, the dominant seventh and Roman numerals; Part 14 for tendency tones, phrase "
                "endings and the corpus. Correlation; Bayes's rule; a little linear algebra for the map.",
        objectives={
            "U": ["Name a key from its signature, and give its relative and parallel keys.",
                  "Say what job each chord of a major key does, and name the four cadences by ear.",
                  "Tell a tonicization from a modulation, and find a pivot chord between neighbouring keys."],
            "M": ["Find the key of a passage by correlating its notes with 24 profiles, and by Bayes's rule.",
                  "Count the major scales that contain a set of notes, from the interval vector.",
                  "Compute the similarity of two keys' profiles, and place the keys by multidimensional scaling."],
            "D": ["Set out the evidence that key profiles are learned from the statistics of music.",
                  "Say what a profile leaves out (order), and what would decide between profiles and grammars."],
            "I": ["Transpose a song to suit a voice, and plan the keys of a programme.",
                  "Harmonize a tune with tonic, predominant and dominant chords.",
                  "Move between keys smoothly, by pivot chords and by neighbours on the circle of fifths."],
        },
        results=[
            ("The probe-tone hierarchy (C major)", r"6.35 \ (\text{tonic}) > 4.8 \ (\text{triad}) > 3.5 \ (\text{scale}) > 2.4 \ (\text{outside})"),
            ("Ratings and counts", r"r(\text{ratings}, \text{time on each note in 54 tunes}) = 0.92"),
            ("The key finder", r"\hat{k} = \arg\max_k \ \operatorname{corr}(d, P_k), \qquad k \in \{24 \text{ keys}\}"),
            ("Scales containing a pair of notes", r"v = \langle 2, 5, 4, 3, 6, 1 \rangle: \ \text{a fifth is in 6 major scales, a tritone in 2}"),
            ("Notes two keys share", r"7 - d \quad (d \le 5 \text{ fifths apart}); \qquad \text{triads shared: } 4, 2, 0"),
            ("Nearest keys to C major", r"r: \ \text{A minor } 0.65, \ \text{G, F } 0.59, \ \text{E minor } 0.54, \ \text{C minor } 0.51"),
        ],
        U=(0, 1, 3, 4, 8, 9, 10),
        D=(2, 12),
        I=(11,),
        also=(("Monochord's keys: profiles, key finders, the map of keys", "explainer/music/monochord/key.py"),
              ("Pictures of keys: the circle of fifths, the torus laid flat, a meter of keys", "explainer/music/keyviz.py")),
    ),
]
