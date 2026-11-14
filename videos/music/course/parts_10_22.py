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
]
