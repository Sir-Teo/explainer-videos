from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Persian(SoundScene):
    def construct(self):
        chapter(self, 6, r"The Persian dastgah", r"Is a mode a scale, \ or a repertory?")
        self.system()
        self.radif()
        self.intervals()
        self.koron()
        self.avaz()

    # ------------------------------------------------------------------
    def system(self):
        items = [
            (r"Persian classical music: \ seven \textit{dastg\=ahs} \ and five \textit{\=av\=azes}", WHITE),
            (r"Shur, \ Homayun, \ Segah, \ Chahargah, \ Mahur, \ Rast-Panjgah, \ Nava", WHITE),
            (r"a dastgah is a family of melodies, \ \textit{gushehs}, \ each with its own range and centre", WHITE),
            (r"a performance travels through gushehs, \ rising in register, \ then returns to the opening mode", TUNE),
            (r"more like a raga's path or a maqam's sayr than a single scale", GREY_A),
        ]
        rows_scene(self, r"dastgah", items,
                   "Persia has a related system with a different organisation. <bookmark mark='b'/> Its classical music has seven "
                   "dastgahs and five avazes: <bookmark mark='c'/> Shur, Homayun, Segah, Chahargah, Mahur, Rast-Panjgah and "
                   "Nava. <bookmark mark='d'/> A dastgah is not a scale but a family of melodies, gushehs, each with its own range "
                   "and centre. <bookmark mark='e'/> A performance travels through the gushehs, rising in register, and returns "
                   "to the opening mode: <bookmark mark='f'/> more like a raga's path or a maqam's sayr than a single scale.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def radif(self):
        items = [
            (r"the \textit{radif}: \ the canonical collection of gushehs, \ learned by heart", WHITE),
            (r"Mirza Abdollah's radif \ (late 19th century) \ is the best known for instruments", WHITE),
            (r"a student memorises it, \ then improvises from it for life", WHITE),
            (r"improvisation by recombining and varying learned models", TUNE),
            (r"Part 42 asks how improvisers draw on memorised material", GREY_A),
        ]
        rows_scene(self, r"the radif", items,
                   "The repertory has a name. <bookmark mark='b'/> The radif is the canonical collection of gushehs, learned by "
                   "heart; <bookmark mark='c'/> Mirza Abdollah's radif, of the late nineteenth century, is the best known for "
                   "instruments. <bookmark mark='d'/> A student memorises it and then improvises from it for life, "
                   "<bookmark mark='e'/> by recombining and varying the learned models. <bookmark mark='f'/> Part 42 asks how "
                   "improvisers in every tradition draw on memorised material.", marks="cdef")

    # ------------------------------------------------------------------
    def intervals(self):
        items = [
            (r"Ali-Naqi Vaziri \ (early 20th century): \ 24 quarter tones, \ and two signs: \ \textit{koron} \ (lower) \ and \textit{sori} \ (raise)", WHITE),
            (r"a koron lowers a note by roughly a quarter tone \ ---\ but by how much exactly varies", WHITE),
            (r"Hormoz Farhat \ (1990): \ the measured intervals are flexible, \ not fixed quarter tones", WHITE),
            (r"the same pattern as Cairo and Istanbul: \ a grid for notation, \ flexibility in performance", TUNE),
            (r"three traditions, \ one lesson about tuning theories", GREY_A),
        ]
        rows_scene(self, r"koron and sori", items,
                   "The tuning question appears here too. <bookmark mark='b'/> In the early twentieth century Ali-Naqi Vaziri "
                   "proposed twenty-four quarter tones and two signs, koron to lower a note and sori to raise it. "
                   "<bookmark mark='c'/> A koron lowers a note by roughly a quarter tone, but by how much exactly varies. "
                   "<bookmark mark='d'/> Hormoz Farhat's study of 1990 found the intervals flexible rather than fixed quarter "
                   "tones. <bookmark mark='e'/> It is the same pattern as Cairo and Istanbul: a grid for notation, flexibility in "
                   "performance. <bookmark mark='f'/> Three traditions, one lesson about tuning theories.", marks="cdef")

    # ------------------------------------------------------------------
    def avaz(self):
        items = [
            (r"\=av\=az: \ unmetred singing of classical poetry \ (Hafez, \ Rumi, \ Saadi)", WHITE),
            (r"\textit{ta\d{h}r\=\i r}: \ a rapid, \ yodel-like ornament, \ a signature of Persian singing", WHITE),
            (r"an instrument answers the singer phrase by phrase", WHITE),
            (r"the poem's metre and meaning shape the melody", TUNE),
            (r"Part 40 turns to song across traditions", GREY_A),
        ]
        rows_scene(self, r"song and poetry", items,
                   "Persian classical music is bound to poetry. <bookmark mark='b'/> The avaz is unmetred singing of classical poems, by Hafez, Rumi or Saadi. <bookmark mark='c'/> Its signature ornament is tahrir, a rapid, yodel-like break in the voice. <bookmark mark='d'/> An instrument answers the singer phrase by phrase, <bookmark mark='e'/> and the poem's metre and meaning shape the melody. <bookmark mark='f'/> Part 40 turns to song across traditions.", marks="cdef")

    # ------------------------------------------------------------------
    def koron(self):
        d = load("koron")
        c = clip("koron.phrase")
        cells = VGroup(*[label(n, font_size=26, color=EAR if cc == 150 else WHITE) for n, cc in zip(["D", r"E\,koron", "F", "G", "F", r"E\,koron", "D", "C", "D"], [p[0] for p in d["phrase"]])]).arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        head = label(r"a phrase of ours with a koron", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"E koron: \ written here 150 cents above D; \ in practice it varies", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Here is a phrase of our own on D in the Persian manner, using one koron note: E lowered by about a quarter tone, "
            "placed here at one hundred and fifty cents above D. It is the same interval as the Arabic Bayati's second step, "
            "and in practice it is placed differently from player to player and phrase to phrase."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a koron phrase", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, t0 in enumerate(d["times"]):
                pulse(snd, cells[i], t0, t0 + d["phrase"][i][1] * 0.9, buff=0.06)
        self.wait(0.3)
        self.clear_scene()
