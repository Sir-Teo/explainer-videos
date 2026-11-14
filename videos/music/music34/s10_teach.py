from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Teach(SoundScene):
    def construct(self):
        chapter(self, 9, r"Two traditions, \ and how they are taught", r"How is a raga learned?")
        self.two()
        self.guru()
        self.bols()
        self.now()
        self.instruments()

    # ------------------------------------------------------------------
    def two(self):
        items = [
            (r"Hindustani: \ north India, \ Pakistan, \ Bangladesh; \ shaped by Persian and court traditions", WHITE),
            (r"Carnatic: \ south India; \ largely devotional texts, \ a large composed repertory", WHITE),
            (r"shared: \ raga, \ tala, \ the drone, \ improvisation within rules", TUNE),
            (r"different: \ instruments \ (sitar, \ sarod, \ tabla; \ veena, \ mridangam), \ the systems of scales and talas", WHITE),
            (r"both are classical in the full sense: \ theory, \ treatises, \ lineages", GREY_A),
        ]
        rows_scene(self, r"north and south", items,
                   "There are two classical traditions. <bookmark mark='b'/> Hindustani music, of north India, Pakistan and "
                   "Bangladesh, shaped in part by Persian and courtly traditions. <bookmark mark='c'/> Carnatic music, of the "
                   "south, largely devotional in its texts, with a large composed repertory. <bookmark mark='d'/> They share raga, "
                   "tala, the drone and improvisation within rules. <bookmark mark='e'/> They differ in instruments, sitar, sarod "
                   "and tabla in the north, veena and mridangam in the south, and in their systems of scales and talas. "
                   "<bookmark mark='f'/> Both are classical in the full sense, with theory, treatises and lineages.", marks="cdef")

    # ------------------------------------------------------------------
    def guru(self):
        items = [
            (r"\textit{guru--\'si\d{s}ya parampar\=a}: \ learning by living and practising with a teacher, \ for years", WHITE),
            (r"Hindustani lineages are \textit{ghar\=an\=a}s: \ schools with their own styles", WHITE),
            (r"teaching is by imitation: \ the teacher sings, \ the student repeats", WHITE),
            (r"what is passed on is not only notes but the gamakas, \ the timing, \ the taste", TUNE),
            (r"today: \ also universities, \ recordings and lessons online", GREY_A),
        ]
        rows_scene(self, r"teacher and student", items,
                   "How is this learned? <bookmark mark='b'/> Traditionally through the guru-shishya parampara: years of "
                   "living and practising with a teacher. <bookmark mark='c'/> In the north the lineages are gharanas, schools "
                   "each with their own style. <bookmark mark='d'/> Teaching is by imitation: the teacher sings, the student "
                   "repeats. <bookmark mark='e'/> What passes on is not only notes but the gamakas, the timing, the taste. "
                   "<bookmark mark='f'/> Today universities, recordings and online lessons have joined the old ways.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def bols(self):
        items = [
            (r"drummers learn by speaking: \ every stroke has a syllable, \ \textit{bol}", WHITE),
            (r"a composition is first recited, \ then played", WHITE),
            (r"Carnatic \textit{solka\d{t}\d{t}u}: \ rhythmic syllables recited as an art in themselves", WHITE),
            (r"a notation that is spoken: \ the voice holds rhythm the way sargam holds melody", TUNE),
            (r"the same idea as Part 10's neumes: \ a memory aid for what is learned by ear", GREY_A),
        ]
        rows_scene(self, r"rhythm you can say", items,
                   "Rhythm is learned by speaking. <bookmark mark='b'/> Every tabla stroke has a syllable, a bol, and "
                   "<bookmark mark='c'/> a composition is recited before it is played. <bookmark mark='d'/> In the south, "
                   "solkattu, rhythmic syllables, is recited as an art in itself. <bookmark mark='e'/> It is a notation that is "
                   "spoken: the voice holds rhythm as sargam holds melody, <bookmark mark='f'/> a memory aid for what is learned "
                   "by ear, like Part 10's neumes.", marks="cdef")

    # ------------------------------------------------------------------
    def now(self):
        items = [
            (r"Ravi Shankar and Ali Akbar Khan brought Hindustani music to world audiences from the 1950s", WHITE),
            (r"film songs, \ fusion and jazz have borrowed ragas and talas", WHITE),
            (r"the classical traditions continue: \ festivals, \ the December season in Chennai", WHITE),
            (r"borrowing is easy; \ understanding takes the years of study the tradition asks for", TUNE),
            (r"Part 47 asks what all the world's musics share", GREY_A),
        ]
        rows_scene(self, r"today", items,
                   "The music lives today. <bookmark mark='b'/> Ravi Shankar and Ali Akbar Khan brought Hindustani music to world "
                   "audiences from the 1950s. <bookmark mark='c'/> Film songs, fusion and jazz have borrowed ragas and talas. "
                   "<bookmark mark='d'/> And the classical traditions themselves continue, in festivals and in the December music "
                   "season of Chennai. <bookmark mark='e'/> Borrowing is easy; understanding takes the years the tradition asks "
                   "for. <bookmark mark='f'/> Part 47 asks what all the world's musics share.", marks="cdef")

    # ------------------------------------------------------------------
    def instruments(self):
        items = [
            (r"north: \ sitar and sarod \ (plucked), \ sarangi \ (bowed), \ bansuri \ (flute), \ shehnai \ (reed)", WHITE),
            (r"tabla \ (two drums) \ and the older pakhawaj", WHITE),
            (r"south: \ veena \ (plucked), \ violin \ (adopted in the 19th century, \ played seated), \ flute", WHITE),
            (r"mridangam \ (double-headed drum), \ ghatam \ (clay pot), \ kanjira \ (frame drum)", TUNE),
            (r"the voice is the model every instrument imitates", GREY_A),
        ]
        rows_scene(self, r"the instruments", items,
                   "The instruments differ between north and south. <bookmark mark='b'/> In the north, the plucked sitar and sarod, the bowed sarangi, the bansuri flute and the shehnai, a double reed; <bookmark mark='c'/> and for rhythm, the tabla and the older pakhawaj. <bookmark mark='d'/> In the south, the veena, the violin, adopted in the nineteenth century and played seated, and the flute; <bookmark mark='e'/> and for rhythm, the mridangam, the clay pot ghatam and the frame drum kanjira. <bookmark mark='f'/> In both, the voice is the model every instrument tries to imitate.", marks="cdef")
