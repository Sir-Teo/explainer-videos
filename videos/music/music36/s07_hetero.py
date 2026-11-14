from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Hetero(SoundScene):
    def construct(self):
        chapter(self, 6, r"Heterophony and gagaku", r"Can everyone play the same tune differently?")
        self.idea()
        self.hear()
        self.gagaku()
        self.sho()
        self.korea()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"heterophony: \ one melody, \ played by several voices at once, \ each in its own version", WHITE),
            (r"one plays it plainly; \ one ornaments it; \ one holds its main notes", WHITE),
            (r"not counterpoint \ (independent lines) \ and not harmony \ (chords): \ a third texture", TUNE),
            (r"common in East and Southeast Asian ensembles, \ in Arabic music, \ in folk hymn singing", WHITE),
            (r"the melody exists in the players' minds; \ each realizes it on their instrument", GREY_A),
        ]
        rows_scene(self, r"heterophony", items,
                   "East Asian ensembles often use a texture that Western theory long overlooked. <bookmark mark='b'/> In "
                   "heterophony several voices play one melody at once, each in its own version: <bookmark mark='c'/> one plainly, "
                   "one ornamented, one holding its main notes. <bookmark mark='d'/> It is neither counterpoint, independent lines, "
                   "nor harmony, chords, but a third texture, <bookmark mark='e'/> common in East and Southeast Asia, in Arabic "
                   "music, and in some folk hymn singing. <bookmark mark='f'/> The melody exists in the players' minds; each "
                   "realizes it on their own instrument.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("hetero")
        c = clip("hetero.three")
        total = max(a + du for _, a, du in d["plain"])
        g = VGroup(mroll([[p + 72, a, du] for p, a, du in d["ornamented"]], width=10.0, height=1.0, lo=70, hi=86, color=EAR, total=total, bar_h=0.1),
                   mroll([[p + 60, a, du] for p, a, du in d["plain"]], width=10.0, height=1.0, lo=58, hi=74, color=TUNE, total=total, bar_h=0.12),
                   mroll([[p + 48, a, du] for p, a, du in d["sustained"]], width=10.0, height=0.6, lo=46, hi=60, color=BLUE, total=total, bar_h=0.12)).arrange(DOWN, buff=0.5).move_to(DOWN * 0.2)
        labs = VGroup(label(r"ornamented", font_size=17, color=EAR).next_to(g[0], LEFT, buff=0.2), label(r"plain", font_size=17, color=TUNE).next_to(g[1], LEFT, buff=0.2),
                      label(r"held", font_size=17, color=BLUE).next_to(g[2], LEFT, buff=0.2))
        head = label(r"the Tune's first phrase, \ three ways at once", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the idea with the Tune's first phrase: a plucked string plays it plainly, a metallophone an octave up "
            "ornaments it with neighbour notes, and a low tone holds its main notes. Three versions, one melody, sounding "
            "together."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(labs))
        with self.listen(c) as snd:
            window(snd, r"heterophony", detail=r"string, \ bar and tone", corner=DL, tag_corner=DR)
            u = d["unit"]
            flash(snd, g[0].notes, [a * u for _, a, _ in d["ornamented"]], hot=WHITE, base=EAR)
            flash(snd, g[1].notes, [a * u for _, a, _ in d["plain"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gagaku(self):
        items = [
            (r"\textit{gagaku}: \ Japan's imperial court music, \ performed for over a thousand years", WHITE),
            (r"brought from Tang China and Korea in the 7th to 9th centuries, \ and preserved", WHITE),
            (r"the \textit{sh\=o}, \ a mouth organ of 17 pipes, \ plays sustained clusters, \ \textit{aitake}", WHITE),
            (r"slow, \ heterophonic, \ with a cycle marked by drums", TUNE),
            (r"a living museum of music that changed elsewhere", GREY_A),
        ]
        rows_scene(self, r"gagaku", items,
                   "Japan preserved one of the oldest orchestral traditions. <bookmark mark='b'/> Gagaku, the imperial court "
                   "music, has been performed for over a thousand years, <bookmark mark='c'/> brought from Tang China and Korea "
                   "between the seventh and ninth centuries and kept ever since. <bookmark mark='d'/> The sho, a mouth organ of "
                   "seventeen pipes, sustains clusters of five or six notes called aitake. <bookmark mark='e'/> The music is slow "
                   "and heterophonic, its cycles marked by drums. <bookmark mark='f'/> It is a living museum of music that "
                   "changed elsewhere.", marks="cdef")

    # ------------------------------------------------------------------
    def sho(self):
        d = load("sho")
        c = clip("sho.three")
        cells = VGroup(label(r"cluster 1", font_size=24, color=TUNE), label(r"cluster 2", font_size=24, color=TUNE), label(r"cluster 3", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"clusters in the manner of the sh\=o \ (ours)", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The sho's sound is unlike any Western harmony: six notes at once, many of them a tone or a fourth apart, swelling slowly and moving to the next cluster as the melody changes. These three are our own voicings in that manner, on additive tones, not the traditional aitake."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"three clusters", kind="synthesized", detail=r"additive tones", corner=DL, tag_corner=DR)
            ts = [0.0, 2.6, 5.2]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def korea(self):
        items = [
            (r"Korea's court and ritual music: \ \textit{jongmyo jeryeak}, \ the royal ancestral rite, \ still performed", WHITE),
            (r"bronze bells and stone chimes in sets, \ descendants of China's \textit{bianzhong} and \textit{bianqing}", WHITE),
            (r"slow tempos, \ long notes, \ heterophony", WHITE),
            (r"a ritual music preserved as East Asia's courts changed", TUNE),
            (r"the same instruments, \ kept alive in three countries in different ways", GREY_A),
        ]
        rows_scene(self, r"court music in Korea", items,
                   "Korea kept its own court music. <bookmark mark='b'/> Jongmyo jeryeak, the music of the royal ancestral rite, is still performed. <bookmark mark='c'/> It uses sets of bronze bells and stone chimes descended from China's bianzhong and bianqing, <bookmark mark='d'/> with slow tempos, long notes and heterophony. <bookmark mark='e'/> It is ritual music preserved while East Asia's courts changed around it. <bookmark mark='f'/> The same family of instruments lives on in China, Korea and Japan, each in its own way.", marks="cdef")
