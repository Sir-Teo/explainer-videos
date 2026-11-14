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
    Part(
        n=24, level="U", widget="treatment", prereq=(6, 14, 16, 20, 23),
        question="What made sixteenth-century polyphony sound as it does, and can its style be measured well enough to "
                 "say who wrote a piece?",
        story="In 1540 a Nuremberg publisher remembered a remark: now that Josquin is dead, he is putting out more works "
              "than when he was alive. Printing had made Josquin a brand and his works a puzzle, and the part learns the "
              "century's style well enough to ask a statistical question: who wrote this? Thirds and sixths become the "
              "sound of the music, in 84 sonorities in 100 of Palestrina's 1,318 Mass movements against 51 in Part 23's "
              "fourteenth century, and a place to end, in 90 of his final chords against 1 in 89. Equal voices build "
              "pieces from points of imitation: 70 in 100 of his movements open with one, at the octave, fourth or fifth. "
              "Of his 102,279 dissonances against the bass, a program finds 55 in 100 passing, 31 suspensions, 10 "
              "neighbours and 2.6 free: the rules Jeppesen wrote down are habits followed ninety-seven times in a "
              "hundred. A nearest-centroid test on twelve features recognizes Palestrina from Monteverdi 95 times in "
              "100, which is the wrong question (genre, date and encoding differ), and Monteverdi's 1592 madrigals from "
              "his 1603 and 1605 ones 73 times in 100. The second practice that Artusi attacked in Cruda Amarilli is "
              "there in the numbers: free dissonance rises from 23 in 100 in Book 3 to 45 and 49. Zarlino's 4:5:6 "
              "triad, meantone and Vicentino's thirty-one tones answer what tuning a world of triads wants; Gesualdo "
              "pushes the modes to breaking. The Tune becomes a four-voice point of imitation.",
        handoff="The Baroque, figured bass and the second practice as the norm in Part 25; meantone and well temperament in "
                "Parts 6 and 25; nineteenth-century chromaticism in Part 27; the song in Part 40; style by statistics in "
                "Parts 62 and 67.",
        outside="Part 6 for tuning; Part 14 for gap fill; Part 16 for species counterpoint; Part 17 for the choir; Part "
                "20 for imitation and the counterpoint search; Part 23 for the fourteenth-century corpus and musica "
                "ficta. Standardization, nearest-centroid classification, leave-one-out validation.",
        objectives={
            "U": ["Hear the difference between a fourteenth-century and a sixteenth-century ending, and a point of imitation.",
                  "Recognize passing notes, neighbours, suspensions and cambiatas, and a prepared from a struck dissonance.",
                  "Explain the three kinds of Mass and what a madrigal sets to music."],
            "M": ["Classify every dissonance in a piece by its treatment, and measure sonorities, imitation and melodic leaps in a corpus.",
                  "Build a stylometric test with standardized features and leave-one-out, and say what it confounds.",
                  "Compute the third and fifth of just, Pythagorean, meantone and equal tunings in cents."],
            "D": ["Design an attribution test held out by source, and interpret its failure modes.",
                  "Model editorial accidentals as uncertain data and propose how to measure editors' disagreement."],
            "I": ["Tune thirds pure in a choir and explain why they differ from the piano's.",
                  "Write a point of imitation and complete it in free counterpoint."],
        },
        results=[
            ("Sonorities with a third", r"51\% \text{ (14th century)} \to 84\% \text{ (Palestrina)}; \ \text{final chords } 1/89 \to 90\%"),
            ("Palestrina's dissonances", r"102{,}279: \ \text{passing } 55\%, \ \text{suspension } 31\%, \ \text{neighbour } 10\%, \ \text{free } 2.6\%"),
            ("The second practice", r"\text{free dissonance: Book 3 } 23\%, \ \text{Book 4 } 45\%, \ \text{Book 5 } 49\%"),
            ("Attribution", r"\text{Palestrina vs Monteverdi } 95\% \ (\text{confounded}); \ \text{Book 3 vs Books 4--5 } 73\%"),
            ("Thirty-one tones", r"10 \text{ steps} = 387.1 \text{ cents}, \ 0.8 \text{ above } 5{:}4"),
        ],
        U=(0, 1, 2, 3, 4, 6, 8, 9),
        D=(12,),
        I=(10,),
        also=(("Monochord's sixteenth-century toolkit: dissonance treatment, melody, sonority, imitation, stylometry, tuning", "explainer/music/monochord/palestrina.py"),
              ("The sixteenth-century corpus: Palestrina's Masses and Monteverdi's madrigals", "explainer/music/monochord/renaissance.py")),
    ),
    Part(
        n=25, level="U", widget="figuredbass", prereq=(6, 10, 15, 17, 18, 24),
        question="How did the music of 1600 to 1750 come to rest on a bass line, a figured bass and two keys?",
        story="In 1589 Vincenzo Galilei hung weights on strings to test a legend two thousand years old and found that "
              "an octave needs four times the weight, not twice: the numbers belong to the strings, and music need not "
              "obey them. His circle in Florence wanted song that served the words, and monody, recitative and aria, and "
              "opera followed. The figured bass made every piece a top and a bottom: figuring the bass of Corelli's "
              "Grave from his violins and realizing it again recovers 80 in 100 of his notes and his first violin only "
              "28 times in 100. Ornament and affect were the player's; the dances of the suite became characters; the "
              "concerto was built from a ritornello's returns, which a program matching intervals finds in any key but "
              "misses when the mode changes. Werckmeister's temperament gave keys colours, C's third 3.9 cents wide and "
              "F sharp's 21.5, and eight modes became two keys: Ionian and Aeolian label 35 in 100 of Palestrina's "
              "movements and all of Bach's chorales, 185 major and 178 minor. Bach, Handel and Rameau gathered the "
              "century up, and what the scores do not say, pitch and tempo, is still argued. The Tune becomes a French "
              "overture and a chaconne with an ornamented reprise.",
        handoff="The Classical style in Part 26; equal temperament's victory in Part 27; the song and opera in Part 40; "
                "orchestration in Part 41; performance practice in Part 43.",
        outside="Part 6 for temperaments; Part 10 for figures and the realizer; Part 15 for keys; Part 17 for the chorales; "
                "Part 18 for the rule of the octave; Part 21 for binary form; Part 24 for the second practice. "
                "Mersenne's law; dynamic programming; interval matching.",
        objectives={
            "U": ["Hear recitative and aria, a ground bass, and the four dances of the suite.",
                  "Read a figured bass and name the chord each figure asks for.",
                  "Hear the difference between a smooth and a rough key in a well temperament."],
            "M": ["Figure a bass from upper parts and realize it by dynamic programming; measure what the realization keeps.",
                  "Find a theme's returns at any transposition by matching intervals, and explain what that misses.",
                  "Compute every key's third and fifth in meantone, Werckmeister III and equal temperament."],
            "D": ["Weigh the evidence for historical pitch and tempo, and state an estimate with its uncertainty.",
                  "Explain how the leading tone and musica ficta made the modes converge on major and minor."],
            "I": ["Realize a figured bass at the keyboard, choosing a top line.",
                  "Choose a pitch standard and a temperament for a Baroque performance, and justify them."],
        },
        results=[
            ("Galilei's weights", r"f \propto \sqrt{T}: \ \text{octave} = 4{:}1, \ \text{the legend's } 2{:}1 \text{ gives } 600 \text{ cents}"),
            ("Corelli realized", r"80\% \text{ of his notes kept}; \ \text{top voice} = \text{first violin } 28\%"),
            ("Werckmeister III", r"\text{third: C } +3.9, \ \text{F}\sharp \ +21.5 \text{ cents}"),
            ("Modes to keys", r"\text{Palestrina: Ionian + Aeolian } 35\%; \ \text{Bach: } 185 \text{ major}, \ 178 \text{ minor}"),
            ("The meantone wolf", r"737.6 \text{ cents} \ (\text{good fifths } 696.6)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 9),
        D=(10,),
        I=(6,),
        also=(("Monochord's Baroque toolkit: Galilei's strings, figures from upper parts, ritornello finder, key colours, ornaments", "explainer/music/monochord/baroque.py"),),
    ),
    Part(
        n=26, level="U", widget="galantphrase", prereq=(7, 15, 21, 22, 24, 25),
        question="What made the Classical style a shared language, and can a program hear who is speaking it?",
        story="In the early 1780s Mozart wrote twelve variations on a French song whose tune is the series' Tune. The "
              "style he wrote in ran on shared expectations, strong enough that Haydn could make a joke of an ending. "
              "Its phrases lean on four and eight bars, a question and its answer, though in the thirty-three quartet "
              "movements of the corpus most of 146 authentic cadences fall elsewhere. A key tracker that knows no "
              "themes reads sonata form in Haydn's Op. 74 No. 1, home, the dominant, a development through distant "
              "keys, home again, and 14 of 18 major-key movements whose readings it trusts go first to the dominant. "
              "The quartet is a conversation the first violin leads in 55 to 62 bars in 100, kept moving by "
              "accompaniment figures in a quarter of all bars. Beethoven made the language longer and wider and made a "
              "home key something to be won. A fair attribution test, one genre, one city, one generation, scores 55 "
              "in 100: better than shuffled names (33), worse than always saying Mozart (45). The fortepiano and the "
              "metronome changed what a score could ask for. The Tune becomes a Classical set: theme with Alberti "
              "bass, minore, adagio, finale.",
        handoff="The Romantic century in Part 27; the song and its accompaniment in Part 40; orchestration in Part 41; "
                "performance and tempo in Part 43; style by statistics in Parts 62 and 65.",
        outside="Part 7 for the bowed string and the piano; Part 15 for keys; Part 18 for n-grams; Part 21 for the period, "
                "the sentence and sonata theory; Part 22 for topics; Part 24 for the attribution test; Part 25 for binary "
                "form and the ritornello. Leave-one-out classification; permutation tests.",
        objectives={
            "U": ["Hear a half cadence and an authentic cadence, and a period built from them.",
                  "Follow a sonata-form movement's keys: exposition, development, recapitulation.",
                  "Hear block chords, an Alberti bass and repeated chords under one melody."],
            "M": ["Detect authentic cadences and measure phrase lengths in a corpus of quartets.",
                  "Trace a movement's tonal plan with a windowed key tracker and find its second key.",
                  "Run a leave-one-out attribution test with a permutation null, and say what it can and cannot show."],
            "D": ["Design a style model that locates where two composers' styles differ within a movement.",
                  "Weigh the evidence on Beethoven's metronome marks."],
            "I": ["Build a fair comparison for a classifier: hold genre, place and time fixed, and report the null."],
        },
        results=[
            ("Cadence gaps", r"146 \text{ cadences}; \ \text{exactly 4 or 8 bars: Mozart } 30\%, \ \text{Haydn } 11\%"),
            ("The second key", r"14 \text{ of } 18 \text{ major-key movements} \to \text{V}; \ 2 \text{ of } 2 \text{ minor} \to \text{III}"),
            ("Who leads", r"\text{first violin: Haydn } 62\%, \ \text{Mozart } 59\%, \ \text{Beethoven } 55\%"),
            ("Attribution", r"55\% \ \text{vs shuffled names } 33\% \ (p \approx 0.03), \ \text{always Mozart } 45\%"),
            ("Beethoven's range", r"\text{span } 35.2 \text{ semitones vs } 26.6 \text{ (Haydn)}, \ 25.8 \text{ (Mozart)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8),
        D=(9,),
        I=(7,),
        also=(("Monochord's Classical toolkit: cadences, phrase gaps, who leads, accompaniment figures, tonal plans, second keys", "explainer/music/monochord/classical.py"),),
    ),
]
