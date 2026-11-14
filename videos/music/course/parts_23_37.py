"""Acts IV to VI: Parts 23 to 37 as they are built (see ``videos/music/course/__init__.py``)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=23, level="U", widget="isorhythm", prereq=(10, 11, 12, 16, 17, 20),
        question="How did Western music go from one line of chant to many voices, and how did it learn to write rhythm "
                 "down?",
        story="Paris, about 1200: under the half-built vault of Notre Dame, Pérotin stretches one syllable of chant "
              "under a minute of music in three dancing voices, and four singers need what no one has had, a way to "
              "write rhythm. The part goes back to the chant: eight modes fixed by a final, a range and a reciting "
              "tone, and the theorists' rule for finding a mode, which is already an algorithm. Guido's hexachords "
              "name the notes by ut re mi fa sol la, and choosing the syllables is a shortest path through the "
              "hexachords. Organum begins in parallel fifths and fourths, walks into tritones (9 in one psalm verse), "
              "and escapes by a boundary rule that makes the voices move differently for the first time; then it "
              "turns free and florid. Rhythm is first a menu of six patterns read from ligatures, then Franco's note "
              "shapes, then the Ars nova's two levels of measure, whose rules of imperfection and alteration need "
              "lookahead to read. Isorhythm lays a color of pitches through a talea of rhythm until they realign at "
              "their least common multiple; a scan of the rhythm alone finds the taleae of de Vitry's motets (33 bars "
              "in Lugentium siccentur, repeated 98 bars in 100 against 72 by chance). Eighty-nine fourteenth-century "
              "pieces, counted, keep perfect intervals on the beat (59 in 100, against 34 elsewhere), write parallel "
              "fifths and octaves about sixty times as often as Bach, end 88 times in 89 on a bare fifth and octave, "
              "and use the Landini cadence most in Landini's and Ciconia's generation. The Ars subtilior pushes "
              "written rhythm to proportions; and much of what we count, the sharps of musica ficta above all, was "
              "added by editors. The Tune is sung as chant, organum and an isorhythmic motet.",
        handoff="The Renaissance in Part 24; modes becoming keys in Part 25; cycles of different lengths again in "
                "minimalism (Part 30); modes in other traditions in Parts 34 and 35; modal jazz in Part 39; finding "
                "music in archives by machine in Part 63.",
        outside="Part 10 for neumes, Guido's staff and Franco's shapes; Part 11 for metre and polyrhythm; Part 12 for "
                "modes; Part 16 for the rules of counterpoint; Part 17 for the chorales and the choir; Part 20 for "
                "the crab canon. Least common multiples, shortest paths, dynamic programming.",
        objectives={
            "U": ["Name the eight modes by final and range, and hear the difference between an authentic and a plagal mode.",
                  "Sing a line in hexachord syllables, and say where a mutation is needed.",
                  "Recognize parallel, free and florid organum, a motet, and an isorhythmic tenor by ear and on the page."],
            "M": ["Implement the theorists' mode rule, solmization by fewest mutations, and Franco's imperfection and alteration.",
                  "Build an isorhythmic tenor and compute when color and talea realign; find a talea in a real tenor by a scan against shuffled bars.",
                  "Count intervals on and off the beat, parallels, cadences and final sonorities in a corpus, and compare them with Bach's."],
            "D": ["Explain what an edition adds to a medieval source (musica ficta, rhythm, text underlay) and how that biases corpus counts.",
                  "Design a model that learns the rules of musica ficta from editions and measures where editors disagree."],
            "I": ["Read a modern edition of medieval music knowing which accidentals are editorial.",
                  "Use two cycles of different lengths, as color and talea, to make long music that never quite repeats."],
        },
        results=[
            ("Color against talea", r"\text{they realign after } \operatorname{lcm}(c, t) \text{ notes: } 7 \text{ and } 5 \to 35"),
            ("De Vitry's taleae", r"12, 18, 33 \text{ bars}; \ \textit{Lugentium}: \ 0.98 \text{ of bars repeated at } 33 \ (\text{chance } 0.72)"),
            ("On the beat", r"59\% \text{ perfect}, \ 8\% \text{ dissonant}; \ \text{elsewhere } 34\% \text{ and } 23\%"),
            ("Parallel fifths and octaves", r"2.9 \text{ per 100 moves}; \ \text{Bach } 0.05"),
            ("Musica ficta", r"2{,}149 \text{ of } 65{,}681 \text{ notes outside the gamut}; \ 64\% \text{ rise a semitone}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 10),
        D=(13,),
        I=(9,),
        also=(("Monochord's medieval toolkit: modes, hexachords, organum, rhythmic modes, mensuration, isorhythm, census", "explainer/music/monochord/medieval.py"),
              ("The fourteenth-century corpus: 89 pieces from the edition's encodings", "explainer/music/monochord/trecento.py")),
    ),
]
