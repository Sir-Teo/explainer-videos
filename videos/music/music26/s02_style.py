from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Style(SoundScene):
    def construct(self):
        chapter(self, 1, r"A style of shared expectations", r"Why could a piece be funny?", extra=((1781, r"Haydn's Op. 33"),))
        self.galant()
        self.empfindsam()
        self.schemata()
        self.k265()
        self.joke()
        self.concerts()

    # ------------------------------------------------------------------
    def galant(self):
        items = [
            (r"after 1730: \ the galant style, \ from Italian opera: \ a tune over a simple bass", WHITE),
            (r"short phrases, \ clear cadences, \ slow harmony under quick melody", WHITE),
            (r"the public grows: \ concerts, \ printed music for amateurs, \ the keyboard in every parlour", WHITE),
            (r"a shared vocabulary of stock patterns: \ the schemata of Part 18", TUNE),
            (r"Rosen's \textit{The Classical Style} \ (1971): \ Haydn, \ Mozart, \ Beethoven made it dramatic", GREY_A),
        ]
        rows_scene(self, r"from galant to Classical", items,
                   "The Classical style grew out of a lighter one. <bookmark mark='b'/> From about 1730 composers trained "
                   "in Italian opera wrote in a galant manner, a tune over a simple bass, <bookmark mark='c'/> with short "
                   "phrases, clear cadences, and harmony that moves slowly under a quick melody. "
                   "<bookmark mark='d'/> Its audience was growing: public concerts, printed music for amateurs, a keyboard "
                   "in every comfortable parlour. <bookmark mark='e'/> It rested on a shared vocabulary of stock patterns, "
                   "the schemata of Part 18, which every trained musician knew. <bookmark mark='f'/> Charles Rosen's book "
                   "The Classical Style argued that Haydn, Mozart and Beethoven turned this polite language into drama.", marks="cdef")

    # ------------------------------------------------------------------
    def schemata(self):
        items = [
            (r"the Romanesca, \ the Prinner, \ the Fonte, \ the Monte, \ the Ponte: \ named by Robert Gjerdingen \ (2007)", WHITE),
            (r"each a bass and a melody that move together in a known way", WHITE),
            (r"taught to apprentices in Naples through partimenti \ (Part 25)", WHITE),
            (r"a listener who knows them hears what is coming, \ and notices when it does not come", TUNE),
            (r"Part 18 found few in Bach's chorales: \ they belong to this style", GREY_A),
        ]
        rows_scene(self, r"the stock patterns", items,
                   "Those patterns now have names. <bookmark mark='b'/> The musicologist Robert Gjerdingen, in 2007, "
                   "systematized historical schemata, retaining some older names and introducing others: the Romanesca, the Prinner, the Fonte, the Monte, the Ponte, and a dozen more. "
                   "<bookmark mark='c'/> Each is a bass line and a melody moving together in a known way. "
                   "<bookmark mark='d'/> Apprentices learned them in Naples, through the partimenti of Part 25. "
                   "<bookmark mark='e'/> A listener who knows them hears what is coming, and notices when it does not "
                   "come. <bookmark mark='f'/> Part 18's detector found few of them in Bach's chorales, which was the wrong "
                   "repertory: they belong to the galant and Classical style.", marks="cdef")

    # ------------------------------------------------------------------
    def joke(self):
        items = [
            (r"Haydn, \ String Quartet Op. 33 No. 2 \ (1781), \ finale: \ a cheerful rondo", WHITE),
            (r"near the end: \ an Adagio, \ then the tune in fragments, \ separated by silences", WHITE),
            (r"each fragment could be the end; \ none is \ (until the last, \ after a long rest)", WHITE),
            (r"the joke works only if everyone knows how a piece ends", TUNE),
            (r"Classical style: \ conventions so shared that they can be played with", GREY_A),
        ]
        rows_scene(self, r"a joke about endings", items,
                   "Haydn's joke shows how strong the expectations were. <bookmark mark='b'/> The finale of his String Quartet Opus 33 Number 2, of 1781, is a cheerful rondo, <bookmark mark='c'/> but near the end it slows to an Adagio, then breaks its tune into fragments separated by silences, <bookmark mark='d'/> each of which could be the end and is not, until after a long rest the opening phrase returns, and stops in mid-air. <bookmark mark='e'/> The joke only works because familiar conventions can support an ending joke, without assuming uniform knowledge across an audience. <bookmark mark='f'/> That is the Classical style: conventions so firmly shared that a composer could play with them, and the audience would get it.", marks="cdef")

    # ------------------------------------------------------------------
    def k265(self):
        items = [
            (r"K. 265: \ a theme and twelve variations, \ each keeping the theme's harmony and phrase plan", WHITE),
            (r"variations 1 to 7: \ running figures in one hand or the other, \ triplets, \ syncopations", WHITE),
            (r"variation 8: \ the minore, \ in C minor, \ with imitation", WHITE),
            (r"variation 11: \ Adagio, \ ornamented; \ variation 12: \ a fast finale in triple time", TUNE),
            (r"the plan of a Classical variation set, \ which Variation 26 imitates", GREY_A),
        ]
        rows_scene(self, r"Mozart's twelve variations", items,
                   "Mozart's set shows the vocabulary in order. <bookmark mark='b'/> Twelve variations, each keeping the theme's harmony and its plan of four-bar phrases. <bookmark mark='c'/> The first seven decorate it with running figures in one hand or the other, triplets and syncopations. <bookmark mark='d'/> The eighth turns to C minor, the minore, with the hands imitating each other. <bookmark mark='e'/> The eleventh is a slow, ornamented Adagio, and the twelfth a fast finale in triple time. <bookmark mark='f'/> That is the plan of a Classical variation set, and this part's own variation at the end follows it.", marks="cdef")

    # ------------------------------------------------------------------
    def concerts(self):
        items = [
            (r"Vienna: \ concerts in theatres, \ halls and private houses; \ Mozart's own subscription concerts \ (1784)", WHITE),
            (r"London: \ Salomon's concerts bring Haydn in 1791 and 1794", WHITE),
            (r"publishers in Vienna, \ Paris and London sell parts and keyboard arrangements", WHITE),
            (r"a public that pays expects to understand at once", TUNE),
            (r"the style is clear because its audience is wide", GREY_A),
        ]
        rows_scene(self, r"a public for music", items,
                   "Who listened? <bookmark mark='b'/> In Vienna, audiences in theatres, halls and private houses; in 1784 Mozart sold subscriptions to his own concerts. <bookmark mark='c'/> In London, the violinist and impresario Johann Peter Salomon brought Haydn over twice in the 1790s for concert seasons that made him a celebrity. <bookmark mark='d'/> Publishers in Vienna, Paris and London sold the parts, and keyboard arrangements for the home. <bookmark mark='e'/> Public concerts and domestic publishing helped circulate recognizable conventions, <bookmark mark='f'/> and the clarity of the style is partly a consequence of the width of its audience.", marks="cdef")

    # ------------------------------------------------------------------
    def empfindsam(self):
        items = [
            (r"Carl Philipp Emanuel Bach, \ Bach's second son, \ in Berlin and Hamburg", WHITE),
            (r"\textit{Empfindsamkeit}: \ sudden changes of mood, \ sighs, \ silences, \ surprising harmonies", WHITE),
            (r"his \textit{Essay on the True Art of Playing Keyboard Instruments} \ (1753, \ 1762)", WHITE),
            (r"Haydn is said to have owed a great deal to it", TUNE),
            (r"galant ease and sensitive expression: \ the two sides the Classical style joined", GREY_A),
        ]
        rows_scene(self, r"the sensitive style", items,
                   "The galant was not the only new manner. <bookmark mark='b'/> Carl Philipp Emanuel Bach, Johann Sebastian's second son, worked for the Prussian king in Berlin and then in Hamburg, <bookmark mark='c'/> and his keyboard music cultivated the sensitive style: sudden changes of mood, sighing figures, silences, harmonies that turn where they are not expected. <bookmark mark='d'/> His Essay on the True Art of Playing Keyboard Instruments, published in two parts in 1753 and 1762, taught a generation how to play and how to improvise. <bookmark mark='e'/> Haydn is reported to have said that he owed a great deal to it. <bookmark mark='f'/> The galant's ease and the sensitive style's expression are the two sides that the Classical style joined.", marks="cdef")
