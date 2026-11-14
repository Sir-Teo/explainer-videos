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
]
