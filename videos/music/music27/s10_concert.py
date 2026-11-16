from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Concert(SoundScene):
    def construct(self):
        chapter(self, 9, r"The concert becomes a museum", r"When did old music become the repertoire?", extra=((1829, r"the \textit{St Matthew Passion} revived"),))
        self.virtuoso()
        self.conductor()
        self.museum()
        self.women()
        self.recordings()

    # ------------------------------------------------------------------
    def virtuoso(self):
        items = [
            (r"Niccolò Paganini in Vienna, \ 1828: \ a violinist as a sensation, \ rumoured to be in league with the devil", WHITE),
            (r"Franz Liszt: \ the pianist as a star; \ in London, \ 1840, \ his concerts were billed as `recitals'", WHITE),
            (r"the solo recital: \ one performer, \ a whole evening, \ from memory", WHITE),
            (r"the iron-framed piano made it possible: \ a hall filled by one instrument", TUNE),
            (r"virtuosity as spectacle: \ adored, \ and distrusted", GREY_A),
        ]
        rows_scene(self, r"the virtuoso", items,
                   "The century made performers into stars. <bookmark mark='b'/> When Niccolò Paganini played in Vienna in "
                   "1828, he was a sensation, and rumours said he had sold his soul to the devil for his technique. "
                   "<bookmark mark='c'/> Franz Liszt did the same for the piano; in London in 1840 his concerts were billed as "
                   "recitals, <bookmark mark='d'/> one performer for a whole evening, eventually from memory. "
                   "<bookmark mark='e'/> Chapter one's iron-framed piano made that possible: one instrument could fill a hall. "
                   "<bookmark mark='f'/> Virtuosity was adored, and distrusted as mere spectacle.", marks="cdef")

    # ------------------------------------------------------------------
    def conductor(self):
        items = [
            (r"the Classical orchestra was led from the keyboard or the first violin's desk", WHITE),
            (r"by the 1830s a conductor with a baton, \ facing the players \ (Spohr, \ Weber, \ Mendelssohn)", WHITE),
            (r"Mendelssohn at Leipzig's Gewandhaus from 1835: \ a regular orchestra, \ a planned season", WHITE),
            (r"Wagner, \ \textit{On Conducting} \ (1869): \ tempo should bend with the music", TUNE),
            (r"the conductor as interpreter: \ the score read, \ not only beaten", GREY_A),
        ]
        rows_scene(self, r"the conductor", items,
                   "The orchestra gained a leader who does not play. <bookmark mark='b'/> A Classical orchestra was led from "
                   "the keyboard or the first violin's desk. <bookmark mark='c'/> By the 1830s conductors such as Louis Spohr, "
                   "Carl Maria von Weber and Felix Mendelssohn stood in front with a baton. <bookmark mark='d'/> Mendelssohn "
                   "made Leipzig's Gewandhaus orchestra, from 1835, a model of regular rehearsal and a planned season. "
                   "<bookmark mark='e'/> Wagner's essay On Conducting, of 1869, argued that tempo should bend with the music, "
                   "chapter four's rubato for a whole orchestra. <bookmark mark='f'/> The conductor became an interpreter.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def museum(self):
        items = [
            (r"1829: \ Mendelssohn, \ twenty, \ revives Bach's \textit{St Matthew Passion} in Berlin", WHITE),
            (r"1850: \ the Bach-Gesellschaft begins a complete edition; \ others follow for Handel, \ Mozart, \ Beethoven", WHITE),
            (r"concert programmes fill with music by the dead: \ `classics', \ a canon", WHITE),
            (r"William Weber \ (2008): \ a `great transformation of musical taste'", TUNE),
            (r"new music must now compete with the museum: \ the problem of the next century", EAR),
        ]
        rows_scene(self, r"the canon", items,
                   "And the concert became a museum. <bookmark mark='b'/> In 1829 Felix Mendelssohn, aged twenty, "
                   "conducted Bach's St Matthew Passion in Berlin, a landmark public revival after a long period outside the regular concert repertory, and in "
                   "a shortened form. <bookmark mark='c'/> In 1850 the Bach Society began a complete edition of his works, and "
                   "editions of Handel, Mozart and Beethoven followed. <bookmark mark='d'/> Concert programmes, which in 1780 "
                   "had been mostly new music, filled with the music of the dead: the classics, the canon. "
                   "<bookmark mark='e'/> The historian William Weber calls this a great transformation of musical taste. "
                   "<bookmark mark='f'/> From then on, a new piece had to compete with the museum, which is the problem the "
                   "next act begins with.", marks="cdef")

    # ------------------------------------------------------------------
    def women(self):
        items = [
            (r"Clara Wieck Schumann, \ 1819--1896: \ a concert career of over sixty years", WHITE),
            (r"she shaped the canon as a performer: \ Beethoven, \ Schumann, \ Brahms, \ from memory", WHITE),
            (r"her own works: \ the polonaises in this part's Library, \ a piano concerto, \ a trio \ (1846)", WHITE),
            (r"Fanny Hensel \ (née Mendelssohn): \ over 450 works, \ most unpublished in her life", TUNE),
            (r"the Library's gaps are the century's: \ who was published, \ who was kept", GREY_A),
        ]
        rows_scene(self, r"who was heard", items,
                   "Who made the canon? <bookmark mark='b'/> Clara Wieck Schumann gave concerts for more than sixty years, "
                   "<bookmark mark='c'/> and as a performer she shaped what was played: Beethoven, Robert Schumann, Brahms. "
                   "<bookmark mark='d'/> Her own works include the polonaises measured in chapters one and seven, a piano "
                   "concerto and a piano trio of 1846. <bookmark mark='e'/> Fanny Hensel, Felix Mendelssohn's sister, wrote "
                   "more than four hundred and fifty works, most of them unpublished in her lifetime. <bookmark mark='f'/> The "
                   "Library's gaps are the century's: who was published, and who was kept.", marks="cdef")

    # ------------------------------------------------------------------
    def recordings(self):
        items = [
            (r"1877: \ Thomas Edison's phonograph records sound on tinfoil", WHITE),
            (r"1889: \ Brahms records part of his first Hungarian Dance on a wax cylinder, \ in Vienna", WHITE),
            (r"the first time a composer's own playing could outlive him", WHITE),
            (r"early recordings show a different style: \ more rubato, \ more sliding between notes", TUNE),
            (r"the century ends with music that can be kept as sound, \ not only as a score", GREY_A),
        ]
        rows_scene(self, r"the first recordings", items,
                   "The century ended with a machine. <bookmark mark='b'/> In 1877 Thomas Edison's phonograph recorded sound on tinfoil. <bookmark mark='c'/> In 1889 Brahms played part of his first Hungarian Dance into a wax cylinder in Vienna; the recording is barely audible through the noise. <bookmark mark='d'/> Sound recording allowed an audible trace of playing to survive, alongside older mechanical and notated records. <bookmark mark='e'/> And the earliest recordings show a style unlike today's: different patterns of rubato, tempo flexibility and sliding, varying by performer and repertory. <bookmark mark='f'/> The century that began with scores ended with music that could be kept as sound.", marks="cdef")
