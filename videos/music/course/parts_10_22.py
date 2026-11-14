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
]
