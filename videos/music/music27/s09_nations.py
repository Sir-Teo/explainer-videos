from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Nations(SoundScene):
    def construct(self):
        chapter(self, 8, r"Nations and their songs", r"Whose music was it?", extra=((1893, r"Dvořák's \textit{New World}"),))
        self.national()
        self.listen_two()
        self.americas()
        self.whose()

    # ------------------------------------------------------------------
    def national(self):
        items = [
            (r"Glinka's \textit{A Life for the Tsar} \ (1836): \ a Russian opera on a Russian story", WHITE),
            (r"`the Five' in St Petersburg: \ Balakirev, \ Borodin, \ Cui, \ Mussorgsky, \ Rimsky-Korsakov", WHITE),
            (r"Smetana's \textit{Má vlast} \ (1874--79), \ Grieg's Norway, \ Chopin's Poland", WHITE),
            (r"folk modes, \ drones and dance rhythms as signs of a people", TUNE),
            (r"often a composer's idea of the folk, \ made in a city for a concert hall", GREY_A),
        ]
        rows_scene(self, r"national styles", items,
                   "The century of nations wanted national music. <bookmark mark='b'/> Mikhail Glinka's A Life for the Tsar, "
                   "of 1836, is usually counted the first Russian opera on a Russian story, <bookmark mark='c'/> and in St "
                   "Petersburg a group of five, Balakirev, Borodin, Cui, Mussorgsky and Rimsky-Korsakov, set out to write "
                   "music that did not sound German. <bookmark mark='d'/> Smetana wrote a cycle of tone poems on Bohemia, "
                   "Grieg drew on Norwegian dances, and Chopin, as chapter three heard, on Poland's. <bookmark mark='e'/> The "
                   "signs were folk modes, drones and dance rhythms. <bookmark mark='f'/> Often they were a city composer's "
                   "idea of the folk, made for a concert hall.", marks="cdef")

    # ------------------------------------------------------------------
    def listen_two(self):
        d = load("nations")
        c = clip("nations.two")
        gL = voices_roll(d["lift"], width=5.4, height=2.6, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.08).move_to(LEFT * 3.3 + DOWN * 0.3)
        gR = voices_roll(d["rag"], width=5.4, height=2.6, colors=[TUNE, GREY_A], bar_h=0.06).move_to(RIGHT * 3.3 + DOWN * 0.3)
        lL = label(r"J. Rosamond Johnson, \ 1900: \ \textit{Lift Every Voice and Sing}", font_size=19, color=GREY_A).next_to(gL, UP, buff=0.3)
        lR = label(r"Scott Joplin, \ 1899: \ \textit{Maple Leaf Rag}", font_size=19, color=GREY_A).next_to(gR, UP, buff=0.3)
        cap = label(rf"in the rag, \ {100 * d['rh_onbeat'] / d['rh_notes']:.0f} in 100 of the right hand's notes fall on a beat; \ "
                    rf"{100 * d['lh_onbeat'] / d['lh_notes']:.0f} of the left hand's", font_size=19, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Two pieces from the Library, both from Black America at the century's turn. First the hymn written in 1900 by "
            "the brothers James Weldon and J. Rosamond Johnson for schoolchildren in Jacksonville, Florida, later adopted as "
            "an anthem; here Part 17's choir sings its first eight bars, without the words. Then sixteen bars of Scott "
            "Joplin's Maple Leaf Rag, of 1899: a march's steady left hand under a right hand that keeps landing between "
            "the beats."
        ):
            self.play(FadeIn(gL), FadeIn(gR), FadeIn(lL), FadeIn(lR), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a hymn, \ then a rag", kind="synthesized", detail=r"choir; \ then piano", corner=DL, tag_corner=DR)
            flash_voices(snd, gL, d["lift"], d["starts"]["lift"], d["units"]["lift"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash_voices(snd, gR, d["rag"], d["starts"]["rag"], d["units"]["rag"], colors=[TUNE, GREY_A])
            pulse(snd, lL, d["starts"]["lift"], d["starts"]["rag"] - 0.5, buff=0.08)
            pulse(snd, lR, d["starts"]["rag"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def americas(self):
        items = [
            (r"Antonín Dvořák in New York, \ 1892--95: \ American music should grow from Black and Native American song", WHITE),
            (r"his \textit{New World} symphony \ (1893): \ pentatonic tunes, \ heard as American", WHITE),
            (r"the Fisk Jubilee Singers \ (from 1871) \ carried spirituals to concert halls in America and Europe", WHITE),
            (r"Joplin's rags: \ a published, \ notated art; \ he also wrote an opera, \ \textit{Treemonisha}", TUNE),
            (r"Lili`uokalani, \ the last monarch of Hawai`i: \ \textit{Aloha `Oe} \ (1878), \ in the Library", GREY_A),
        ]
        rows_scene(self, r"new worlds", items,
                   "The argument crossed the Atlantic. <bookmark mark='b'/> Antonín Dvořák, directing a conservatory in New "
                   "York from 1892, said that American music should grow from Black and Native American song, "
                   "<bookmark mark='c'/> and his New World symphony of 1893 has pentatonic tunes that audiences heard as "
                   "American. <bookmark mark='d'/> The Fisk Jubilee Singers, from 1871, had already carried spirituals to "
                   "concert halls in America and Europe. <bookmark mark='e'/> Joplin's rags were a published, notated art, "
                   "and he wrote an opera, Treemonisha. <bookmark mark='f'/> And Liliuokalani, the last monarch of the "
                   "Hawaiian Kingdom, wrote Aloha Oe in 1878; in the Library it is the piece with the clearest key of all.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def whose(self):
        items = [
            (r"`national' music was often made from other people's music", WHITE),
            (r"collecting folk songs: \ an act of love, \ and of selection and editing", WHITE),
            (r"Black American music became the foundation of the next century's popular music", TUNE),
            (r"its creators were rarely the ones paid for it", EAR),
            (r"Act VI hears other musics on their own terms; \ Part 60, \ who gets paid", GREY_A),
        ]
        rows_scene(self, r"whose music?", items,
                   "Whose music was it? <bookmark mark='b'/> National music was often made from other people's music, "
                   "<bookmark mark='c'/> and collecting folk songs was an act of love and also of selection and editing. "
                   "<bookmark mark='d'/> Black American music, the spiritual, the rag and soon the blues and jazz, became the "
                   "foundation of the next century's popular music, <bookmark mark='e'/> and its creators were rarely the ones "
                   "paid for it. <bookmark mark='f'/> Act VI listens to other musics on their own terms, and Part 60 asks who "
                   "gets paid.", marks="cdef")
