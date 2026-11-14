from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Cairo(SoundScene):
    def construct(self):
        chapter(self, 4, r"Cairo, \ 1932", r"Can a living tradition be standardized?", extra=((1932, r"the Congress of Arab Music"),))
        self.mishaqa()
        self.congress()
        self.practice()
        self.bartok()
        self.ehalf()
        self.after()
        self.orchestras()

    # ------------------------------------------------------------------
    def mishaqa(self):
        items = [
            (r"Mikh\=a'\=\i l Mush\=aqa \ (Damascus, \ 19th century): \ the octave as 24 equal quarter tones", WHITE),
            (r"a theorist's simplification: \ easy to write, \ easy to teach", WHITE),
            (r"by the 20th century, \ the standard way to notate Arabic music", WHITE),
            (r"a half-flat sign for notes a quarter tone low: \ E half-flat, \ B half-flat", TUNE),
            (r"the grid names the notes; \ it does not say exactly where musicians put them", GREY_A),
        ]
        rows_scene(self, r"the quarter-tone grid", items,
                   "The twenty-four-step grid is a nineteenth-century idea. <bookmark mark='b'/> The Damascus scholar Mikhail "
                   "Mushaqa described the octave as twenty-four equal quarter tones. <bookmark mark='c'/> It was a theorist's "
                   "simplification, easy to write and to teach, <bookmark mark='d'/> and by the twentieth century it was the "
                   "standard way to notate Arabic music, <bookmark mark='e'/> with a half-flat sign for notes a quarter tone low. "
                   "<bookmark mark='f'/> But the grid names the notes; it does not say exactly where musicians put them.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def congress(self):
        items = [
            (r"1932: \ King Fu'\=ad's government invites musicians and scholars to Cairo", WHITE),
            (r"committees on scales, \ instruments, \ recording, \ education, \ history", WHITE),
            (r"European guests: \ Bart\'ok, \ Hindemith, \ Hornbostel, \ Lachmann, \ Farmer, \ Sachs", WHITE),
            (r"the scale committee heard and discussed many tunings, \ and recommended no single equal grid", TUNE),
            (r"the congress also made recordings: \ an early archive of the music of the time", GREY_A),
        ]
        rows_scene(self, r"the congress", items,
                   "The question came to a head in Cairo. <bookmark mark='b'/> In 1932 King Fuad's government invited musicians "
                   "and scholars to a Congress of Arab Music, <bookmark mark='c'/> with committees on scales, instruments, "
                   "recording, education and history. <bookmark mark='d'/> Among the European guests were Bartók, Hindemith, "
                   "Erich von Hornbostel, Robert Lachmann, Henry George Farmer and Curt Sachs. <bookmark mark='e'/> The scale "
                   "committee heard and discussed many tunings and did not settle on a single equal grid. <bookmark mark='f'/> The "
                   "congress also recorded ensembles from across the region, an early archive of the music of its time.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"musicians report that the same half-flat note differs from maqam to maqam", WHITE),
            (r"E half-flat in Rast is often described as higher than in Bayati", WHITE),
            (r"and it can shift within a phrase: \ higher rising, \ lower falling", WHITE),
            (r"intonation is part of the maqam, \ as gamaka is part of the raga \ (Part 34)", TUNE),
            (r"the grid is a map; \ the music is the territory", GREY_A),
        ]
        rows_scene(self, r"what musicians do", items,
                   "What do musicians actually do? <bookmark mark='b'/> They report, and measurements agree, that the same "
                   "half-flat note is not fixed from maqam to maqam: <bookmark mark='c'/> the E half-flat of Rast is often "
                   "described as higher than that of Bayati, <bookmark mark='d'/> and it may shift within a phrase, higher when "
                   "rising, lower when falling. <bookmark mark='e'/> Intonation belongs to the maqam, as gamaka belongs to the "
                   "raga in Part 34. <bookmark mark='f'/> The grid is a map; the music is the territory.", marks="cdef")

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (r"after 1932: \ conservatories, \ radio orchestras, \ notated arrangements", WHITE),
            (r"the qanun gained levers to play the grid's quarter tones \ (chapter 9)", WHITE),
            (r"keyboards and electronic instruments now offer `Arabic scale' presets", WHITE),
            (r"some teachers worry that fixed tunings flatten the music's nuance", TUNE),
            (r"standardization helps teaching and ensembles; \ it can also erase what makes a tradition", GREY_A),
        ]
        rows_scene(self, r"after the congress", items,
                   "The twentieth century standardized anyway. <bookmark mark='b'/> Conservatories, radio orchestras and notated "
                   "arrangements spread. <bookmark mark='c'/> The qanun gained small levers to play the grid's notes. "
                   "<bookmark mark='d'/> Keyboards and electronic instruments now offer Arabic scale presets. "
                   "<bookmark mark='e'/> Some teachers worry that fixed tunings flatten the music's nuance. "
                   "<bookmark mark='f'/> Standardization helps teaching and ensembles; it can also erase part of what makes a "
                   "tradition what it is.", marks="cdef")

    # ------------------------------------------------------------------
    def ehalf(self):
        d = load("ehalf")
        c = clip("ehalf.two")
        ruler = cents_ruler([sorted(set(d["rast"])), sorted(set(d["bayati"]))], width=8.0, top=600, labels=[r"Rast on C", r"Bayati on D"], colors=[TUNE, BLUE]).move_to(UP * 0.4)
        cap = label(r"an illustration with values of ours: \ E half-flat at 360 in Rast, \ 340 in Bayati", font_size=21, color=EAR).to_edge(DOWN, buff=1.1)
        head = label(r"one notated pitch, \ two placements", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is what such a difference sounds like, as an illustration with values of our own, not a measurement: a Rast "
            "phrase on C with its E half-flat at three hundred and sixty cents, then a Bayati phrase on D with the same "
            "notated E half-flat at three hundred and forty. Twenty cents, a comma: one sign on the page, two pitches in the "
            "music."
        ):
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Rast, \ then Bayati", detail=r"an oud model", corner=DL, tag_corner=DR)
            pulse(snd, ruler.rows[0][3], d["starts"]["rast"], d["starts"]["bayati"] - 0.5, buff=0.06)
            pulse(snd, ruler.rows[1][3], d["starts"]["bayati"], c.duration, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bartok(self):
        items = [
            (r"Bart\'ok collected Arab folk music in Algeria in 1913, \ before Cairo", WHITE),
            (r"at the congress he urged recording village musicians, \ not only city ensembles", WHITE),
            (r"Hindemith and others debated whether Western instruments should be admitted", WHITE),
            (r"the European scholars were guests; \ the decisions were Egyptian and Arab", TUNE),
            (r"the recordings made then are now studied for how the music has changed", GREY_A),
        ]
        rows_scene(self, r"European ears", items,
                   "European ears were part of the story. <bookmark mark='b'/> Bartók had collected Arab folk music in Algeria in 1913. <bookmark mark='c'/> At the congress he urged recording village musicians, not only city ensembles. <bookmark mark='d'/> Hindemith and others debated whether Western instruments such as the piano should be admitted. <bookmark mark='e'/> The Europeans were guests; the decisions were Egyptian and Arab. <bookmark mark='f'/> The recordings made then are now studied for how the music has changed since.", marks="cdef")

    # ------------------------------------------------------------------
    def orchestras(self):
        items = [
            (r"Cairo's radio and film made a new ensemble: \ the \textit{firqa}, \ a large orchestra", WHITE),
            (r"violins in sections, \ qanun, \ oud, \ ney, \ percussion, \ and later electric instruments", WHITE),
            (r"singers such as Umm Kulth\=um and Muhammad `Abd al-Wahh\=ab reached the whole Arab world", WHITE),
            (r"unison playing by many violins blurs fine intonation, \ and favoured a shared grid", TUNE),
            (r"media change tuning: \ Part 60's theme, \ heard here", GREY_A),
        ]
        rows_scene(self, r"the twentieth-century sound", items,
                   "The twentieth century made a new sound. <bookmark mark='b'/> Cairo's radio and film industry built the firqa, a large orchestra <bookmark mark='c'/> with violin sections, qanun, oud, ney and percussion, and later electric instruments. <bookmark mark='d'/> Singers such as Umm Kulthum and Muhammad Abd al-Wahhab reached the whole Arab world through it. <bookmark mark='e'/> Many violins playing in unison blur fine distinctions of intonation, which favoured a shared grid. <bookmark mark='f'/> Media change tuning, a theme Part 60 returns to.", marks="cdef")
