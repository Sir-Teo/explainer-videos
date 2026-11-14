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
    Part(
        n=27, level="U", widget="rubato", prereq=(7, 15, 17, 21, 25, 26),
        question="How did the nineteenth century stretch music, and can the stretching be measured?",
        story="Between 1800 and 1870 the piano gained an iron frame, felt hammers and two more octaves, and the scores "
              "climbed with it: Clara Wieck's polonaises of 1831 reach E7, high above Mozart's F6. Schubert's Lieder made "
              "the piano a character; a key-finder hears Der Lindenbaum turn its stanza from E major to E minor, one "
              "semitone in the tune, while the piano plays seven notes for every one sung. The mazurka's uneven beat and "
              "the two kinds of rubato, a phrase arch and Mozart's stolen time, are modelled and heard. Berlioz made a "
              "theme a character and asked for 27 wind, brass and timpani players; Wagner made a chord a question that "
              "five keys can hold. Measured across a Library of 827 pieces from 1370 to 1924, instrumental music grew "
              "more chromatic by about 5.6 notes in a hundred per century from 1680 to 1900 (95% interval 2.4 to 8.2), "
              "while songs stayed plain; then Schoenberg and Webern jump to 25 to 30. The century also built national "
              "styles, the solo recital, the conductor, the canon and the first recordings. The Tune becomes a nocturne, "
              "a Lied and a transformed leitmotif.",
        handoff="What is left when the key goes in Parts 28 and 29; the song in Part 40; orchestration in Part 41; "
                "performing and the evidence of recordings in Part 43; music that tells a story in Part 44; style and "
                "history as data in Parts 62 and 67.",
        outside="Part 7 for the piano and the bowed string; Part 15 for key profiles; Part 17 for the synthetic voice; Part 21 "
                "for chroma and form; Parts 23 to 26 for the earlier collections. Linear regression and the bootstrap; "
                "time warping.",
        objectives={
            "U": ["Hear a Lied's piano as part of the meaning, and a stanza turned from major to minor.",
                  "Hear a mazurka's uneven beat, a phrase arch and stolen time.",
                  "Hear a theme transformed in character, and the Tristan chord's unresolved question."],
            "M": ["Read MusicXML and Humdrum scores whole, with chords, ties, transposing instruments and split spines.",
                  "Measure chromaticism and tonal clarity window by window with key profiles.",
                  "Fit a trend across a corpus with a bootstrap interval, and separate genre from date."],
            "D": ["Design a corpus study of nineteenth-century harmony with composers as random effects.",
                  "Use early recordings as evidence for performance style, and say what they cannot show."],
            "I": ["Turn a familiar historical claim into a measured trend with an interval, and report what the data cannot support."],
        },
        results=[
            ("The keyboard", r"54 \to 88 \text{ keys}, \ 1720\text{--}1880; \ \text{Clara Wieck's polonaises reach E7}"),
            ("Der Lindenbaum", r"\text{E major} \to \text{E minor}: \ \text{G}\sharp \to \text{G}; \ 1443 \text{ piano notes to } 205 \text{ sung}"),
            ("The orchestra", r"5, \ 9, \ 18, \ 27, \ 19 \text{ wind, brass, timpani} \ (1759\text{--}1876)"),
            ("Instrumental chromaticism", r"+5.6 \text{ per century, } 1680\text{--}1900 \ [2.4, \ 8.2]; \ \text{all pieces } [-0.8, \ 4.9]"),
            ("After 1900", r"\text{Schoenberg, Webern: } 25\text{--}30\% \text{ outside the key, clarity } < 0.56"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 9),
        D=(10,),
        I=(7,),
        also=(("Monochord's Romantic toolkit: whole-score readers, chromaticism and clarity, transformations, the phrase arch, the mazurka's beats", "explainer/music/monochord/romantic.py"),),
    ),
    Part(
        n=28, level="U", widget="symmetric", prereq=(6, 11, 12, 15, 21, 27),
        question="What did composers build when they left the major and minor scales, and how can a claim about a scale be tested?",
        story="At the 1889 Paris Exposition Debussy heard a Javanese gamelan, and within twenty-five years composers had "
              "rebuilt their scales and rhythms. The whole-tone scale has one step size and only two transpositions, so "
              "it has no home; of the 352 shapes a set of pitch classes can take, just 15 map onto themselves under some "
              "transposition, every one a pattern repeated every 1, 2, 3, 4 or 6 semitones, and Messiaen's seven modes "
              "are the large ones. Planing slides one chord shape under a melody; the octatonic scale holds C major and "
              "F sharp major together, and a key-finder shows two clear keys making one unclear one. Displaced accents "
              "keep the pulse and lose the metre; Bartók's additive rhythms are counted by the Padovan numbers, and a "
              "golden-section claim with ten loose landmarks succeeds by chance 61 times in 100. A four-note passage "
              "fits some octatonic scale by chance 42 times in 100 and some diatonic one 49 times, which is why the "
              "octatonic debate needs long passages and null models. The Tune is planed in whole-tone chords, then set "
              "over an octatonic ostinato with accents placed by chance.",
        handoff="Twelve tones in Part 29; transformations and the geometry of chords in Parts 31 and 32; rhythm and scale as "
                "mathematics in Part 33; the gamelan in Part 36; loops and sequencers in Part 53.",
        outside="Part 6 for equal temperament; Part 9 for bars and gongs; Part 11 for syncopation and polyrhythm; Part 12 for "
                "scales and Burnside's count; Part 15 for key profiles; Part 21 for the golden section. Group actions on "
                "Z12, cosets, recurrences, exact null models.",
        objectives={
            "U": ["Hear the whole-tone scale, planing, the octatonic, displaced accents and additive rhythm.",
                  "Explain why the whole-tone and octatonic scales have no home key.",
                  "Recognize bitonality and say what makes two layers sound like two keys."],
            "M": ["Enumerate the pitch-class sets with limited transposition and prove they are unions of cosets.",
                  "Compute the exact chance that a k-note set fits a scale, and count additive and palindromic rhythms.",
                  "Test a golden-section claim against a null model with landmarks and tolerance."],
            "D": ["Design a corpus test of the octatonic in Stravinsky with rival explanations and a chance baseline.",
                  "Evaluate the historical evidence for the 1913 'riot'."],
            "I": ["Turn a pattern-finding claim into a test with a stated null model, fixed before looking."],
        },
        results=[
            ("Symmetric scales", r"352 \text{ shapes}; \ 15 \text{ symmetric}; \ \text{Messiaen's 7 are the large ones}"),
            ("Fits by chance", r"4 \text{ notes: octatonic } 42\%, \ \text{diatonic } 49\%; \ 7 \text{ notes: } 3\%, \ 1.5\%"),
            ("Two keys at once", r"\text{tune } r = 0.96 \ (\text{C}), \ \text{chords } 0.83 \ (\text{F}\sharp), \ \text{together } 0.74"),
            ("The golden section", r"88 \text{ bars, } \pm 2, \ 10 \text{ landmarks: } 61\% \text{ by chance}"),
            ("Rhythms", r"\text{groupings of 12 pulses: } 12; \ \text{palindromes of 16: } 193 \text{ of } 20{,}569"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 8, 9),
        D=(10,),
        I=(6,),
        also=(("Monochord's modern toolkit: symmetry census, chance fits, additive and palindromic rhythms, the golden-section null", "explainer/music/monochord/modern.py"),),
    ),
    Part(
        n=29, level="U", widget="setclass", prereq=(12, 15, 27, 28),
        question="What replaced the key when Schoenberg gave it up, and what mathematics lies under the twelve-tone method?",
        story="In 1908 a soprano in Schoenberg's Second String Quartet sang of the air of another planet, and the key "
              "dissolved. His Piano Pieces Op. 19 (1911), played here from the encoding, keep a centre made of an "
              "interval, G and B, while all twelve notes are used. Set theory names such music: transposition and "
              "inversion make 224 set classes, counted by brute force and by Burnside's lemma, as in Forte's table; 23 "
              "pairs share an interval vector without being the same chord; and every hexachord has its complement's "
              "interval vector, checked on all 924 and proved by counting pairs. The twelve-tone row has 48 forms; "
              "Webern's canon Dormi Jesu inverts every one of its 45 intervals exactly. Of all rows starting on C, "
              "3,856 use every interval once, and in each the first and last notes are a tritone apart, because "
              "1 + 2 + ... + 11 = 66. Six hexachords are all-combinatorial. Total serialism followed, and the critics said "
              "it sounded like a cloud of points; listening experiments find that people follow contour and texture far "
              "better than rows. The Tune becomes a row grown from its own intervals, then a pointillist variation.",
        handoff="Sound itself in Part 30; transformations in Part 31; the geometry of chords in Part 32; Fourier views of "
                "sets and rhythms in Part 33; expectation in Part 46; machines that compose in Part 65.",
        outside="Part 3 for the Fourier transform; Part 12 for Burnside's lemma; Part 15 for keys; Part 22 for hierarchy; "
                "Part 27 for chromaticism; Part 28 for symmetric sets. The dihedral group, Burnside's lemma, "
                "permutations, depth-first search, double counting.",
        objectives={
            "U": ["Hear free atonal music and say what holds it together.",
                  "Find a chord's prime form and interval vector, and the forms of a row.",
                  "Hear an inversion and a retrograde, and judge whether a line is a form of a row."],
            "M": ["Count set classes by brute force and by Burnside's lemma, and enumerate Z-relations.",
                  "Prove the hexachord theorem by double counting, and the tritone property of all-interval rows.",
                  "Enumerate all-interval rows by search and test hexachords for combinatoriality."],
            "D": ["Relate homometric sets in crystallography to Z-related sets via the discrete Fourier transform.",
                  "Design a perception study separating interval content from surface features."],
            "I": ["Verify an exhaustive claim by enumeration, then prove it, and say what each establishes."],
        },
        results=[
            ("Set classes", r"224 = (4096 + \cdots)/24; \ \text{sizes } 12, 29, 38, 50, 38, 29, 12 \ (\text{Forte})"),
            ("Z-relations", r"23 \text{ pairs}; \ 15 \text{ among hexachords}; \ \text{hexachord theorem: } 924 / 924"),
            ("Webern's canon", r"45 \text{ of } 45 \text{ intervals inverted}, \ 46 \text{ of } 46 \text{ durations equal}"),
            ("All-interval rows", r"3{,}856; \ \text{ends a tritone apart: } 1 + \cdots + 11 = 66 \equiv 6"),
            ("A shared hexachord", r"\text{by chance } 1/924 \text{ of random rows}"),
        ],
        U=(0, 1, 2, 4, 5, 6, 7, 8, 9),
        D=(10,),
        I=(3,),
        also=(("Monochord's atonal toolkit: prime forms, interval vectors, set classes, Z-pairs, rows, all-interval and combinatorial searches", "explainer/music/monochord/atonal.py"),),
    ),
    Part(
        n=30, level="U", widget="poissoncloud", prereq=(1, 2, 3, 5, 7, 28, 29),
        question="What happened when composers stopped arranging notes and started arranging sound, chance and process?",
        story="In 1948 Pierre Schaeffer closed the groove of a disc of train noises and heard music. Tape let sounds be "
              "re-speeded, reversed and cut: without its first quarter-second a bell hardly sounds like a bell. Cage gave "
              "his choices to chance and, in 4'33'', to the room. Cologne built sounds from sine waves; Stockhausen's "
              "Studie II used 81 frequencies, each the 25th root of 5 above the last. Xenakis composed the statistics of "
              "clouds: their onsets form a Poisson process, whose per-second counts match Poisson's law and clump in a "
              "way the ear hears at once, and his sieves build scales from residue classes, one repeating only every 35 "
              "semitones. Clusters beat about eight times a second, which is why sound masses are rough. Two loops of one "
              "figure pass through twelve alignments, symmetric about the middle; a brass note's sixteen harmonics, "
              "given to an ensemble, rebuild it between the piano's keys. The Tune is phased against itself, turned "
              "into a cloud of glissandi, and played on a string's harmonics, where its A is 59 cents flat.",
        handoff="Transformations in Part 31; the mathematics of loops and rhythm in Part 33; the auditory scene in Part 45; "
                "filters in Part 49; synthesis in Parts 51 and 52; the studio in Part 53; generative audio in Part 66.",
        outside="Part 1 for the string's harmonics; Part 2 for tape speed; Part 3 for Fourier; Part 5 for beats and "
                "roughness; Part 7 for the instruments; Part 8 for the lips and the voice; Part 9 for bells. The Poisson "
                "process, residue classes, the Chinese remainder theorem, harmonic analysis.",
        objectives={
            "U": ["Hear what tape speed, reversal and a cut attack do to a sound.",
                  "Hear a random cloud against an even one, a cluster against an open chord, and two loops drifting apart.",
                  "Explain spectral orchestration and why it needs pitches between the piano's keys."],
            "M": ["Simulate a Poisson process and check its counts against Poisson's law.",
                  "Build scales from sieves, and count a phased figure's alignments.",
                  "Measure a tone's harmonics and orchestrate them by register."],
            "D": ["Design an experiment on when sonification beats a plot.",
                  "Analyse a process piece as a walk through a finite set of states."],
            "I": ["Build a unit-generator patch, and use random processes with controlled statistics in sound design."],
        },
        results=[
            ("Tape", r"\times 2 \text{ speed: up an octave, half as long; the bell without its attack}"),
            ("Studie II", r"81 \text{ frequencies}, \ \sqrt[25]{5} = 111.45 \text{ cents apart}"),
            ("A Poisson cloud", r"\text{mean} = \text{variance} = \lambda; \ \text{gaps' spread} = \text{mean}"),
            ("A cluster", r"\tfrac12 \text{ semitone apart near C4: } 8 \text{ beats/s}"),
            ("Harmonics against keys", r"5: -14, \ 7: -31, \ 11: \pm 49, \ 13: +41 \text{ cents}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7),
        D=(9,),
        I=(8,),
        also=(("Monochord's sound-mass toolkit: tape operations, phasing, Poisson clouds, sieves, clusters, spectra orchestrated", "explainer/music/monochord/soundmass.py"),),
    ),
    Part(
        n=31, level="U", widget="tonnetz", prereq=(5, 13, 15, 19, 27, 28, 29),
        question="When late-Romantic and film harmony leaves the key behind, what logic connects its chords?",
        story="Two chords that share no key can still sound inevitable. Hugo Riemann's moves name the logic: P, L and R "
              "each keep two notes of a triad and move the third by a semitone or a whole tone. Built by brute force, the "
              "PLR group and the transpositions and inversions are both of order 24, commute, and each acts on the 24 "
              "triads in exactly one way: two dual groups, and L and R alone generate the first, a dihedral group in which "
              "LR has order 12. Euler's lattice, closed by equal temperament into a torus, draws every triad as a "
              "triangle; from C major there are 1, 3, 6, 8, 5 and 1 triads at 0 to 5 steps, B flat minor alone the "
              "farthest. Repeating P and L walks the hexatonic scale, P and R the octatonic; the families split the "
              "triads four and three ways, and an augmented triad sits one semitone from six of them. The chain R, L, R, "
              "L... visits all 24 triads, as Beethoven's Ninth begins to, and is one of exactly 62 tours. Film composers use "
              "chromatic mediants for wonder and the hexatonic pole for the uncanny; jazz moves through three keys a major "
              "third apart, and the tritone substitution is the same idea for seventh chords. The Tune is harmonized by a "
              "walk on the Tonnetz that rediscovers tonic, subdominant and dominant.",
        handoff="The geometry of chords in Part 32; the mathematics of scales in Part 33; jazz harmony in Part 39; music for "
                "picture in Part 44; chord recognition in Part 62.",
        outside="Part 6 for Euler's lattice and the comma; Part 13 for triads; Part 19 for the hexatonic cycle; Part 27 for "
                "Tristan; Part 28 for the symmetric scales; Part 29 for inversion. Group actions, dihedral groups, "
                "breadth-first search, Hamiltonian cycles.",
        objectives={
            "U": ["Hear and name P, L and R, and the chromatic mediants and hexatonic pole built from them.",
                  "Find a triad's place on the Tonnetz and walk between triads by flips.",
                  "Explain why the R-L chain visits every triad."],
            "M": ["Build the PLR and T/I groups by brute force and show they commute and act simply transitively.",
                  "Count distances, cycles, systems and Hamiltonian tours on the PLR graph.",
                  "Compare PLR distance with voice-leading distance."],
            "D": ["Design a listening experiment that separates the circle of keys, the Tonnetz and voice leading."],
            "I": ["Score a cue with mediants and poles, and harmonize a melody by a walk on the Tonnetz."],
        },
        results=[
            ("The moves", r"P, L, R: \text{ two notes kept, one moved } 1 \text{ or } 2 \text{ semitones}"),
            ("Two groups", r"|\langle P,L,R \rangle| = |\langle T,I \rangle| = 24, \ \text{commuting}"),
            ("The dihedral relations", r"P^2 = L^2 = R^2 = 1, \ (LR)^{12} = 1, \ P = R(LR)^3"),
            ("Distances from C", r"1, 3, 6, 8, 5, 1 \text{ triads at } 0 \ldots 5 \text{ steps}"),
            ("Tours", r"62 \text{ Hamiltonian cycles; one without } P"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7),
        D=(8,),
        I=(6,),
        also=(("Monochord's neo-Riemannian toolkit: P, L, R, the two groups, the Tonnetz, cycles, tours, seventh chords", "explainer/music/monochord/neoriemann.py"),),
    ),
]
