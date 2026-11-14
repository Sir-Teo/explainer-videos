from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Masters(SoundScene):
    def construct(self):
        chapter(self, 9, r"Bach, \ Handel, \ Rameau", r"Three careers born in two years: \ what did each make of the inheritance?", extra=((1685, r"Bach and Handel born"),))
        self.bach()
        self.handel()
        self.lascia()
        self.rameau()
        self.others()

    # ------------------------------------------------------------------
    def bach(self):
        items = [
            (r"Johann Sebastian Bach, \ 1685--1750: \ organist, \ court musician, \ then cantor in Leipzig", WHITE),
            (r"a cantata almost every Sunday for years; \ the Passions, \ the Mass in B minor", WHITE),
            (r"the summa of counterpoint: \ Part 20's fugues, \ Part 17's chorales", TUNE),
            (r"French, \ Italian and German styles combined in one hand", WHITE),
            (r"old-fashioned at his death; \ revived from 1829, \ with Mendelssohn's \textit{St Matthew Passion}", GREY_A),
        ]
        rows_scene(self, r"Bach", items,
                   "Three composers born within two years of each other gathered the century up. <bookmark mark='b'/> "
                   "Johann Sebastian Bach, born in 1685, was an organist and court musician before he became cantor of "
                   "Saint Thomas's in Leipzig, <bookmark mark='c'/> where for years he produced a cantata almost every "
                   "Sunday, as well as the Passions and, later, the Mass in B minor. <bookmark mark='d'/> His music is the "
                   "summit of the counterpoint of Parts 17 and 20, <bookmark mark='e'/> combining the French, Italian and "
                   "German styles of his time. <bookmark mark='f'/> At his death he was old-fashioned, and his revival "
                   "dates from 1829, when Felix Mendelssohn conducted the St Matthew Passion in Berlin.", marks="cdef")

    # ------------------------------------------------------------------
    def handel(self):
        items = [
            (r"George Frideric Handel, \ 1685--1759: \ trained in Germany, \ formed in Italy, \ settled in London", WHITE),
            (r"Italian operas for London, \ from \textit{Rinaldo} \ (1711): \ the da capo aria", WHITE),
            (r"when opera failed, \ the English oratorio: \ \textit{Messiah} \ (1742)", WHITE),
            (r"a businessman-composer: \ his own companies, \ his own theatres", TUNE),
            (r"never out of the repertory since", GREY_A),
        ]
        rows_scene(self, r"Handel", items,
                   "George Frideric Handel was born a few weeks earlier, in the same part of Germany, but his career ran "
                   "the other way. <bookmark mark='b'/> Trained in Germany and formed in Italy, he settled in London, "
                   "<bookmark mark='c'/> where from Rinaldo in 1711 he wrote Italian operas for London audiences, made of "
                   "da capo arias. <bookmark mark='d'/> When the fashion for Italian opera collapsed he invented the English "
                   "oratorio, Messiah among them, first performed in Dublin in 1742. <bookmark mark='e'/> He was a "
                   "businessman as well as a composer, running his own companies and his own seasons. "
                   "<bookmark mark='f'/> Unlike Bach, he has never left the repertory.", marks="cdef")

    # ------------------------------------------------------------------
    def lascia(self):
        d = load("handel")
        c = clip("handel.lascia")
        vs = [d["voice"], d["rh"], d["lh"]]
        g = voices_roll(vs, width=11.4, height=3.4, colors=[EAR, TUNE, GREY_A], bar_h=0.12).move_to(DOWN * 0.35)
        head = label(r"Handel, \ \textit{Lascia ch'io pianga} \ (\textit{Rinaldo}, \ 1711): \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(r"a sarabande rhythm, \ the weight on the second beat: \ chapter 5's dance as a lament", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "This is the opening of one of Rinaldo's arias, Lascia ch'io pianga, let me weep, sung from the encoding by "
            "the synthetic choir's soprano, with the accompaniment on harpsichord. Listen for the slow triple time with "
            "its weight on the second beat: it is chapter five's sarabande, used for a lament."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Handel, \ \textit{Lascia ch'io pianga}", detail=r"from the encoding, \ synthetic voice and harpsichord", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[EAR, TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rameau(self):
        items = [
            (r"Jean-Philippe Rameau, \ 1683--1764: \ the theorist of chapter 8", WHITE),
            (r"his first opera at fifty: \ \textit{Hippolyte et Aricie} \ (1733)", WHITE),
            (r"French tragedy in music: \ dances, \ choruses, \ orchestral storms", WHITE),
            (r"accused of too much harmony and noise, \ as Monteverdi had been of too much dissonance", TUNE),
            (r"by 1750 a younger, \ simpler style was arriving: \ Part 26", GREY_A),
        ]
        rows_scene(self, r"Rameau", items,
                   "The third, Jean-Philippe Rameau, born in 1683, was the theorist of the last chapter. "
                   "<bookmark mark='b'/> He wrote his first opera at the age of fifty, Hippolyte et Aricie, in 1733, "
                   "<bookmark mark='c'/> French tragedy in music, full of dances, choruses and orchestral storms. "
                   "<bookmark mark='d'/> Critics accused him of too much harmony and too much noise, as Monteverdi had "
                   "been accused of too much dissonance. <bookmark mark='e'/> By 1750 a younger, simpler style was "
                   "arriving from Italy, built on tunes over plain accompaniments, and Part 26 follows it.")

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"Georg Philipp Telemann: \ the most prolific, \ thousands of works, \ the most famous German of his day", WHITE),
            (r"Domenico Scarlatti, \ in Lisbon and Madrid: \ 555 keyboard sonatas, \ each in two halves", WHITE),
            (r"Henry Purcell, \ London: \ \textit{Dido and Aeneas}, \ songs, \ grounds", WHITE),
            (r"Elisabeth Jacquet de La Guerre, \ Paris: \ harpsichord suites, \ an opera \ (1694)", TUNE),
            (r"fame then and fame now are different lists", GREY_A),
        ]
        rows_scene(self, r"and many more", items,
                   "Three names leave out most of the century. <bookmark mark='b'/> Georg Philipp Telemann wrote thousands of works and was the most famous German composer of his day, far more famous than Bach. <bookmark mark='c'/> Domenico Scarlatti, at the courts of Lisbon and Madrid, wrote five hundred and fifty-five keyboard sonatas, each a binary dance turned into an experiment. <bookmark mark='d'/> Henry Purcell in London wrote Dido and Aeneas, and songs and grounds. <bookmark mark='e'/> Elisabeth Jacquet de La Guerre, in Paris, published harpsichord suites and, in 1694, an opera. <bookmark mark='f'/> Fame then and fame now are different lists, and a history that counts only the canon counts badly.", marks="cdef")
