from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403

NM = {53: "F", 59: "B", 63: r"D$\sharp$", 68: r"G$\sharp$", 69: "A", 70: r"A$\sharp$", 71: "B", 52: "E", 56: r"G$\sharp$", 62: "D",
      57: "A", 60: "C", 64: "E", 50: "D", 65: "F", 45: "A"}


class Wagner(SoundScene):
    def construct(self):
        chapter(self, 6, r"Wagner: \ the endless melody", r"What happens when a chord never resolves?", extra=((1865, r"\textit{Tristan und Isolde}"),))
        self.verdi()
        self.drama()
        self.tristan()
        self.chord()
        self.motives()
        self.mahler()
        self.reaction()

    # ------------------------------------------------------------------
    def drama(self):
        items = [
            (r"Richard Wagner, \ 1813--1883: \ the music drama, \ words and music his own", WHITE),
            (r"\textit{Der Ring des Nibelungen}: \ four evenings, \ about fifteen hours, \ finished 1874", WHITE),
            (r"Bayreuth, \ 1876: \ a theatre built for it, \ the orchestra hidden in a covered pit", WHITE),
            (r"no separate numbers: \ continuous music, \ an `endless melody'", TUNE),
            (r"a modern legend, \ and a toxic one: \ Wagner's antisemitic writings are part of the record", EAR),
        ]
        rows_scene(self, r"the music drama", items,
                   "If Schubert's songs are the century's smallest form, Wagner's dramas are its largest. "
                   "<bookmark mark='b'/> Richard Wagner wrote his own words and called his works music dramas. "
                   "<bookmark mark='c'/> The Ring of the Nibelung takes four evenings, about fifteen hours, and was finished in "
                   "1874. <bookmark mark='d'/> For it he built a theatre at Bayreuth, opened in 1876, with the orchestra hidden "
                   "in a covered pit. <bookmark mark='e'/> Traditional aria-recitative divisions are often weakened in his mature dramas, though there are still recognizable numbers and formal articulations, "
                   "what he called endless melody. <bookmark mark='f'/> He is also a toxic figure: his antisemitic writings are "
                   "part of the record, and part of how his music was later used.", marks="cdef")

    # ------------------------------------------------------------------
    def tristan(self):
        d = load("tristan")
        c = clip("tristan.two")
        def stack(chords, x, col):
            g = VGroup()
            for i, ch in enumerate(chords):
                col_ = VGroup(*[label(NM.get(m, str(m)), font_size=22, color=col).move_to([x + 1.25 * i, -1.6 + 0.12 * (m - 45), 0]) for m in ch])
                g.add(col_)
            return g
        gp = stack(d["plain"], -5.6, GREY_A)
        gt = stack(d["tristan"], 1.0, TUNE)
        lp = label(r"A minor: \ i, \ iv, \ V7, \ i", font_size=22, color=GREY_A).move_to([-3.7, 2.4, 0])
        lt = label(r"the Tristan chord, \ the line rising, \ E7", font_size=22, color=TUNE).move_to([2.9, 2.4, 0])
        with self.voiceover(
            "The most famous chord of the century opens Tristan und Isolde, first staged in Munich in 1865. Hear a plain "
            "cadence in A minor first, for comparison. Then the chord as textbooks give it, F, B, D sharp and G sharp, with "
            "the line above rising G sharp, A, A sharp, B, and the music landing on E seven, the dominant of A minor. And "
            "then nothing: the A minor chord it points to does not come."
        ):
            self.play(FadeIn(gp), FadeIn(gt), FadeIn(lp), FadeIn(lt))
        with self.listen(c) as snd:
            window(snd, r"a cadence, \ then Tristan", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            flash(snd, list(gp), [d["starts"]["plain"] + 2 * d["unit"] * i for i in range(4)], hot=WHITE, base=GREY_A)
            flash(snd, list(gt), [d["starts"]["tristan"] + 2 * d["unit"] * i for i in range(4)], hot=WHITE, base=TUNE)
            pulse(snd, VGroup(*gp), d["starts"]["plain"], d["starts"]["tristan"] - 0.2, buff=0.15, color=GREY_A)
            pulse(snd, VGroup(*gt), d["starts"]["tristan"], c.duration, buff=0.15, color=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chord(self):
        d = load("tristan")
        rows_ = text_rows([
            (r"F, \ B, \ D$\sharp$, \ G$\sharp$: \ the same sounds as F, \ A$\flat$, \ C$\flat$, \ E$\flat$, \ a half-diminished seventh", WHITE),
            (r"its spelling supports several functional readings in A minor \ (Part 19)", WHITE),
            (rf"keys whose scale holds all four notes: \ {d['fits_tristan'][0]} \ (a plain triad: \ {d['fits_plain'][0]})", WHITE),
            (r"the resolution goes to a dominant seventh \ ---\ itself unresolved", TUNE),
            (r"delayed closure is a dramatic motif; \ the last chord, \ at Isolde's death, \ is B major", EAR),
        ], font_size=24)
        head = label(r"a chord that asks a question", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Why is the chord so unsettling? <bookmark mark='a'/> Its four sounds are the same as F, A flat, C flat and E flat, an ordinary half-diminished seventh, but spelled as Wagner spells it, their spelling invites several functional interpretations in A minor, as Part 19 showed. <bookmark mark='b'/> Count the keys whose scales contain all four notes: {say(d['fits_tristan'][0])}, against {say(d['fits_plain'][0])} for a plain A minor triad, counting the minor scale's raised notes as inside. <bookmark mark='c'/> And where it resolves, it resolves only to a dominant seventh, itself a question. <bookmark mark='d'/> Delayed closure is a dramatic motif, not the literal absence of local tonics throughout the opera. Its final B-major chord supplies a large-scale ending, rather than simply resolving the opening A-minor dominant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def motives(self):
        items = [
            (r"the leitmotif: \ a short idea tied to a person, \ an object, \ a feeling", WHITE),
            (r"named by Hans von Wolzogen's guide to the \textit{Ring} \ (1876), \ not by Wagner", WHITE),
            (r"motives transform as their meanings change: \ the ring, \ the curse, \ the sword", WHITE),
            (r"the orchestra comments on what the characters do not say", TUNE),
            (r"a network of motives: \ by one count over a hundred in the \textit{Ring}", GREY_A),
        ]
        rows_scene(self, r"the leitmotif", items,
                   "Wagner built his dramas from motives. <bookmark mark='b'/> A leitmotif is a short musical idea tied to a "
                   "person, an object or a feeling. <bookmark mark='c'/> The name comes from guides like Hans von Wolzogen's "
                   "to the Ring, published for the first Bayreuth festival, not from Wagner himself. <bookmark mark='d'/> The "
                   "motives transform as their meanings change, as Berlioz's obsession did, <bookmark mark='e'/> and the "
                   "orchestra can tell the audience what a character does not say. <bookmark mark='f'/> Counts of the Ring's "
                   "motives vary with the counter, from a few dozen to well over a hundred: a network, rather than a list.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def reaction(self):
        items = [
            (r"Wagnerism: \ a cult across Europe, \ in poetry and painting as well as music", WHITE),
            (r"the `War of the Romantics': \ Leipzig and Brahms against Weimar, \ Liszt and Wagner", WHITE),
            (r"after \textit{Tristan}: \ Bruckner, \ Mahler, \ Strauss, \ the young Schoenberg", WHITE),
            (r"chromaticism as a language of longing: \ the key is felt most when it is withheld", TUNE),
            (r"chapter seven asks whether the Library shows the stretching", GREY_A),
        ]
        rows_scene(self, r"after \textit{Tristan}", items,
                   "The effect was enormous. <bookmark mark='b'/> Wagnerism became a movement across Europe, in poetry and "
                   "painting as well as music. <bookmark mark='c'/> Critics took sides in what is now called the War of the "
                   "Romantics, Leipzig and Brahms against Weimar, Liszt and Wagner. <bookmark mark='d'/> After Tristan came "
                   "Bruckner, Mahler, Richard Strauss and the young Schoenberg, <bookmark mark='e'/> for whom chromatic "
                   "harmony was a language of longing: the key felt most strongly where it is withheld. "
                   "<bookmark mark='f'/> Is the stretching visible in the notes themselves? Chapter seven measures it.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def mahler(self):
        items = [
            (r"Anton Bruckner's symphonies: \ cathedrals of brass, \ over an hour long", WHITE),
            (r"Gustav Mahler: \ `a symphony must be like the world: \ it must embrace everything' \ (as reported)", WHITE),
            (r"Mahler's Eighth \ (Munich, \ 1910): \ advertised as the `Symphony of a Thousand'", WHITE),
            (r"Richard Strauss's tone poems and operas: \ \textit{Salome} \ (1905) \ pushes the key to its edge", TUNE),
            (r"size and chromaticism grew together; \ both reached a limit", GREY_A),
        ]
        rows_scene(self, r"the century ends large", items,
                   "The century ended large. <bookmark mark='b'/> Anton Bruckner's symphonies are cathedrals of brass, often over an hour long. <bookmark mark='c'/> Gustav Mahler is reported to have said that a symphony must be like the world, and embrace everything. <bookmark mark='d'/> His Eighth Symphony, first performed in Munich in 1910, was advertised as the Symphony of a Thousand, for the number of performers. <bookmark mark='e'/> Richard Strauss's Salome, of 1905, pushed the key nearly to its edge. <bookmark mark='f'/> Some works expanded both scale and chromatic resources; neither had one universal historical limit.", marks="cdef")

    # ------------------------------------------------------------------
    def verdi(self):
        items = [
            (r"Italian opera: \ Rossini, \ Bellini, \ Donizetti, \ then Giuseppe Verdi \ (1813--1901)", WHITE),
            (r"\textit{bel canto}: \ the singer's line first, \ the orchestra a guitar beneath it", WHITE),
            (r"Verdi's \textit{Rigoletto} \ (1851): \ `La donna è mobile', \ a tune the audience left the theatre singing", WHITE),
            (r"in the Library: \ 2 notes in 100 outside its key, \ among the plainest pieces of the century", TUNE),
            (r"two opposite answers to one question: \ how should music serve drama?", GREY_A),
        ]
        rows_scene(self, r"the other opera", items,
                   "Wagner was not the only answer. <bookmark mark='b'/> Italian opera ran from Rossini, Bellini and Donizetti to Giuseppe Verdi, born the same year as Wagner. <bookmark mark='c'/> Its ideal was bel canto, beautiful singing: the singer's line first, the orchestra often a large guitar beneath it. <bookmark mark='d'/> In Verdi's Rigoletto, of 1851, the Duke's song La donna è mobile is a tune the audience was meant to leave the theatre singing, <bookmark mark='e'/> and in the Library it is one of the plainest pieces of the century, two notes in a hundred outside its key. <bookmark mark='f'/> Verdi and Wagner developed distinct, internally varied approaches to one question: how music should serve drama.", marks="cdef")
