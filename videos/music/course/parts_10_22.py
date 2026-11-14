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
]
