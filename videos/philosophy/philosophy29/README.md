# Philosophy, Built — Part 29: Being and Time-Consciousness

Part 29 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the third part of Act VI,
*Mind and Meaning*: phenomenology, existentialism, hermeneutics and their heirs, with the frame problem built.
Brentano's thesis that intentionality is the mark of the mental, acts directed at what does not exist, Twardowski's
act, content and object, Meinong's objects, Chisholm's marks and the pains-and-moods objection. Husserl's epoché and
the natural attitude, noesis and noema (Gurwitsch's and Føllesdal's readings), a cube seen from 4000 viewpoints (1193
show one face, 2232 two, 575 three, none more, yet all six are seen from somewhere), and eidetic variation on 5000
random triangles as an analogy (five invariants; obtuse 73%, acute 27%). The living present: James's specious present,
Husserl's 1905 diagram of sinking retentions animated, and a retentional present tested on all 120 orderings of five
notes (a knife-edge present tells 5 apart, a two-note window 20, a fading trace all 120, and the order can be read
back), with Dainton's cinematic, retentional and extensional models, Grush and Varela. Heidegger's question of being,
Dasein and being-in-the-world against the Cartesian picture, the hammer (ready-to-hand, present-at-hand, breakdown and
the referential whole), care, das Man, being-towards-death, and the political shadow. Dreyfus: the four assumptions of
symbolic AI, the five stages of skill, and what learning answered and did not. The frame problem: McCarthy and Hayes's
situation calculus, frame axioms against Reiter's successor-state axioms (200 000 against 1000 for 100 actions and 1000
fluents), Dennett's robots acted out by a planner (R1 carries the bomb out; with successor-state axioms the plan is
open, remove the bomb, pull; the work grows from 8 states and 105 deduced facts to 76 states and 11 805 facts as
irrelevant fluents are added), the logical and the philosophical problem (Fodor's isotropy, Hamlet's problem), **the
Wall's twenty-ninth brick**, and a **Price List** of three claims (Dreyfus, the logicists, bounded rationality).
Merleau-Ponty's body schema, motor intentionality, Schneider, the cane and the phantom limb; Braitenberg's vehicles 2a,
2b, 3a and 3b simulated; and 4E cognition with its critics. Sartre's existence before essence, bad faith and the look;
Fanon; Beauvoir's situated freedom. Kierkegaard's stages and Nietzsche's death of God, genealogy and eternal return:
a reversible cellular automaton on 11 cells returns after 93 steps (return times from 9 to 513 on rings of 5 to 20
cells), and Simmel's wheels (rates 1, 2, 1/π) come within 0.0000096 of a turn by time 355 and never return. The
hermeneutic circle from Schleiermacher to Gadamer, with an iteration of part and whole as an analogy (a text that can
answer back corrects any prejudice; a wholly ambiguous one leaves it as it was), and its critics. Saussure's signs and
differences, made exact on Part 28's word vectors (a random rotation changes every coordinate, correlation −0.14, and
no cosine or neighbour; Procrustes recovers it from 8 anchors to 10⁻¹⁵; five groups of words share a point), Derrida's
différance stated carefully, a closed dictionary in which every chain of definitions ends in a circle and 3 of 18
words must be grounded from outside, and the critics. Foucault's discipline, the Panopticon, power/knowledge and
biopower, a threshold gamed by 3049 of 20 000 people (acceptances 6179 → 9228, only 67% of them qualified), Goodhart,
Deleuze and Zuboff. The Frankfurt school, Habermas's validity claims, the ideal speech situation and principle (D),
its critics, and the 'Habermas Machine'. Nishida's pure experience and logic of place, the Kyoto school, Dōgen's
being-time and Nāgārjuna. And the analytic–continental divide: Davos, Carnap against 'the nothing itself nothings',
and the bridges (Dreyfus–McDowell, naturalized phenomenology, neurophenomenology, heterophenomenology, Winograd and
Flores, predictive processing).

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/phenomenology.py`
(with `pragmatics` for the word vectors and `prop` for the Price List), tested in
`tests/philosophy/test_phenomenology.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy29.compute       # every computed item (seconds; .cache/philosophy29)
python tools/build.py philosophy29 -q l                # 480p preview
python tools/build.py philosophy29                     # 1080p30 -> renders/philosophy29.mp4
python tools/qa_scene.py philosophy29 Frame            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Husserl (1900); four questions; the plan. | — |
| 1 | `Brentano` | Brentano (1874); Twardowski (1894); Meinong (1904); Chisholm (1957); Tye; Crane. | — |
| 2 | `Husserl` | Husserl (1900, 1913); Gurwitsch; Føllesdal (1969). | a cube from 4000 viewpoints; 5000 triangles varied |
| 3 | `Time` | James (1890); Husserl (1905/1928); Dainton (2000); Grush (2006); Varela (1999). | Husserl's diagram; three presents on 120 melodies |
| 4 | `Heidegger` | Heidegger (1927); the Black Notebooks (2014). | — |
| 5 | `Dreyfus` | Dreyfus (1965, 1972, 2007); Dreyfus and Dreyfus (1980); Haugeland. | — |
| 6 | `Frame` | McCarthy and Hayes (1969); McCarthy (1980); Fodor (1983, 1987); Dennett (1984); Reiter (1991); Shanahan; **the Wall's twenty-ninth brick**; **the Price List**. | axioms counted; Dennett's robots planned |
| 7 | `Body` | Merleau-Ponty (1945); Braitenberg (1984); Varela, Thompson and Rosch (1991); Kirsh and Maglio (1994); O'Regan and Noë (2001); Clark and Chalmers (1998); Adams and Aizawa (2008). | four vehicles simulated |
| 8 | `Sartre` | Sartre (1943, 1944, 1946); Fanon (1952); Beauvoir (1947, 1949). | — |
| 9 | `Recurrence` | Kierkegaard (1843, 1844); Nietzsche (1882, 1887); Poincaré (1890); Simmel (1907). | a reversible automaton's return; Simmel's wheels |
| 10 | `Hermeneutic` | Schleiermacher; Dilthey (1883); Gadamer (1960); Habermas; Ricoeur (1965); Hirsch (1967). | the circle as an iteration (an analogy) |
| 11 | `Signs` | Saussure (1916); Derrida (1967, 1968, 1988); Searle (1977); Cambridge (1992). | rotation and Procrustes; a closed dictionary |
| 12 | `Foucault` | Bentham (1791); Foucault (1966, 1975, 1976); Goodhart (1975); Deleuze (1990); Zuboff (2019). | a threshold gamed |
| 13 | `Habermas` | Horkheimer (1937); Horkheimer and Adorno (1947); Marcuse (1964); Habermas (1981); Alexy; Lyotard (1979); Tessler et al. (2024). | — |
| 14 | `Kyoto` | Nishida (1911, 1926); Watsuji (1935); Nishitani (1961); Heidegger (1959); Dōgen (1240); Nāgārjuna. | — |
| 15 | `Bridges` | Davos (1929); Heidegger (1929); Carnap (1932); Winograd and Flores (1986); Dennett (1991); Varela (1996); Petitot et al. (1999); Dreyfus–McDowell (2005–07). | — |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Moran, *Introduction to Phenomenology* (2000); Zahavi, *Husserl's Phenomenology* (2003); Dreyfus,
*Being-in-the-World* (1991) and *What Computers Still Can't Do* (1992); Gallagher and Zahavi, *The Phenomenological
Mind* (2008); Varela, Thompson and Rosch, *The Embodied Mind* (1991); Shanahan, "The Frame Problem" (*Stanford
Encyclopedia of Philosophy*); Heisig, *Philosophers of Nothingness* (2001).

Primary texts and papers: Dōgen, *Uji* (1240); Bentham (1791); Kierkegaard (1843, 1844); Brentano (1874); Nietzsche
(1882, 1887); James (1890); Twardowski (1894); Husserl (1900–01, 1905/1928, 1913); Meinong (1904); Simmel (1907);
Nishida (1911, 1926); Saussure (1916); Heidegger (1927, 1929); Carnap (1932); Watsuji (1935); Sartre (1943, 1946);
Merleau-Ponty (1945); Beauvoir (1947, 1949); Horkheimer and Adorno (1947); Fanon (1952); Chisholm (1957); Gadamer
(1960); Nishitani (1961); Marcuse (1964); Ricoeur (1965); Foucault (1966, 1975, 1976); Derrida (1967, 1988); Hirsch
(1967); McCarthy and Hayes (1969); Føllesdal (1969); Dreyfus (1965, 1972, 2007); Goodhart (1975); Searle (1977);
Lyotard (1979); McCarthy (1980); Dreyfus and Dreyfus (1980); Habermas (1981); Fodor (1983, 1987); Dennett (1984,
1991); Braitenberg (1984); Winograd and Flores (1986); Deleuze (1990); Reiter (1991); Kirsh and Maglio (1994); Varela
(1996, 1999); Clark and Chalmers (1998); Petitot et al. (1999); Dainton (2000); O'Regan and Noë (2001); Grush (2006);
Adams and Aizawa (2008); Zuboff (2019); Tessler et al. (2024).
