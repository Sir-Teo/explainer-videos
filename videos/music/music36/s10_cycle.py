from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403

COL = {"gong": EAR, "kenong": TUNE, "kempul": BLUE, "ketuk": GREY_A}


class Cycle(SoundScene):
    def construct(self):
        chapter(self, 9, r"The gong cycle and interlocking parts", r"How does a gamelan keep time?")
        self.colotomy()
        self.hear()
        self.kotekan()
        self.irama()
        self.layers()
        self.worldwide()
        self.kebyar()

    # ------------------------------------------------------------------
    def colotomy(self):
        items = [
            (r"gamelan music is built on cycles, \ marked by the gongs: \ \textit{colotomic} structure", WHITE),
            (r"the big gong \ (\textit{gong ageng}) \ ends each cycle", WHITE),
            (r"smaller gongs \ (kenong, \ kempul, \ ketuk) \ divide it into halves, \ quarters, \ eighths", WHITE),
            (r"the \textit{balungan}, \ the skeleton melody, \ is played one note per beat on the sarons", TUNE),
            (r"Part 34's tala marked by claps; \ here marked by gongs", GREY_A),
        ]
        rows_scene(self, r"the gong cycle", items,
                   "Gamelan music is built on cycles marked by gongs, a structure called colotomic. <bookmark mark='b'/> The great "
                   "gong ends each cycle; <bookmark mark='c'/> smaller gongs, kenong, kempul and ketuk, divide it into halves, "
                   "quarters and eighths. <bookmark mark='d'/> Over them the balungan, the skeleton melody, is played one note per "
                   "beat on the sarons. <bookmark mark='e'/> Part 34's tala was marked by claps; this one by gongs.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("cycle")
        c = clip("cycle.lancaran")
        grid = VGroup()
        for i in range(16):
            col = VGroup(Square(0.6, stroke_color=GREY_B, stroke_width=1.2), label(str(d["balungan"][i]), font_size=20, color=WHITE))
            col[1].move_to(col[0])
            marks = VGroup(*[label(inst[:3], font_size=12, color=COL[inst]) for inst in d["colotomic"][i]]).arrange(DOWN, buff=0.05)
            col.add(marks)
            grid.add(col)
        grid.arrange(RIGHT, buff=0.05).move_to(UP * 0.4)
        for col in grid:
            col[2].next_to(col[0], DOWN, buff=0.12)
        head = label(r"a lancaran cycle of ours: \ 16 beats", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"balungan in slendro degrees 1--5; \ ket = ketuk, \ ken = kenong, \ kem = kempul, \ gon = gong", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Here is a lancaran, a sixteen-beat form, with a balungan of our own in an illustrative slendro. The ketuk ticks "
            "on the odd beats, the kenong strikes every four beats, the kempul in between, and the great gong on the "
            "sixteenth beat ends the cycle, together with the last kenong. Listen to two cycles, and feel where the gong falls."
        ):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"lancaran", detail=r"Part 9's bars and gongs", corner=DL, tag_corner=DR)
            pulse(snd, grid, 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.3)
            b = d["beat"]
            for i in range(32):
                pulse(snd, grid[i % 16][0], i * b, (i + 1) * b - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kotekan(self):
        d = load("kotekan")
        c = clip("kotekan.three")
        card = listen_card(r"A fast figure, \ three times: \ first one part, \ then another part, \ then both together. \ "
                           r"When both play, \ does it sound like one player or two?", width=10.4)
        with self.voiceover(
            "A question for your ears. A fast figure, played first by one player alone, then by a second alone, then by both "
            "together. When both play, does it sound like one player or two?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)

        def row(part, col):
            g = VGroup(*[VGroup(Square(0.5, stroke_color=GREY_B, stroke_width=1), label(str(x) if x else "", font_size=16, color=col)) for x in part]).arrange(RIGHT, buff=0.04)
            for cc in g:
                cc[1].move_to(cc[0])
            return g
        rows_ = VGroup(VGroup(label(r"polos", font_size=20, color=TUNE), row(d["polos"], TUNE)).arrange(RIGHT, buff=0.4),
                       VGroup(label(r"sangsih", font_size=20, color=BLUE), row(d["sangsih"], BLUE)).arrange(RIGHT, buff=0.4),
                       VGroup(label(r"both", font_size=20, color=WHITE), row(d["figure"], WHITE)).arrange(RIGHT, buff=0.4)).arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"one part, \ the other, \ both", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            p = d["pulse"]
            for ri, k in enumerate(("polos", "sangsih", "both")):
                for i in range(48):
                    t0 = d["starts"][k] + i * p
                    pulse(snd, rows_[ri][1][i % 16][0], t0, t0 + p - 0.01, buff=0.02)
        ans = label(r"one line: \ two players, \ each playing every other note, \ make a figure too fast for either alone", font_size=21, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "It sounds like one player, playing very fast. In fact each player has a gap on every other pulse, and together "
            "they fill every pulse exactly once, like Part 33's tiling canon. Balinese musicians call this kotekan: "
            "interlocking parts that let two players make a figure too fast for either alone."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        items = [
            (r"a gamelan is layered by speed: \ gongs slowest, \ balungan, \ then faster and faster elaborations", WHITE),
            (r"each layer doubles or quadruples the density of the one below", WHITE),
            (r"the elaborating instruments \ (bonang, \ gender, \ gambang) \ paraphrase the balungan", WHITE),
            (r"heterophony again \ (chapter 6), \ organised by speed", TUNE),
            (r"Balinese kebyar \ (from 1915): \ sudden changes of tempo and dynamics, \ virtuoso interlocking", GREY_A),
        ]
        rows_scene(self, r"layers of speed", items,
                   "A gamelan is layered by speed. <bookmark mark='b'/> The gongs are slowest, then the balungan, then faster "
                   "and faster elaborations, <bookmark mark='c'/> each layer two or four times as dense as the one below. "
                   "<bookmark mark='d'/> The elaborating instruments, bonang, gender and gambang, paraphrase the balungan: "
                   "<bookmark mark='e'/> heterophony again, organised by speed. <bookmark mark='f'/> And Balinese gong kebyar, "
                   "from around 1915, added sudden changes of tempo and dynamics and virtuoso interlocking.", marks="cdef")

    # ------------------------------------------------------------------
    def irama(self):
        d = load("irama")
        c = clip("irama.two")
        cells = VGroup(label(r"two notes per beat", font_size=24, color=TUNE), label(r"four notes per beat", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"one balungan, \ two densities of elaboration", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'Javanese musicians call the relation between the balungan and its elaboration irama. Here is one balungan line of ours with an elaborating part playing two notes for every balungan note, then four. As the elaboration fills in, the balungan slows, and the music seems to open up.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"two, \ then four per beat", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            ks = ['two', 'four']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kebyar(self):
        d = load("kebyar")
        c = clip("kebyar.burst")
        cells = VGroup(label(r"fast, \ interlocking, \ paired and beating", font_size=24, color=EAR), label(r"then the gong", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"in the manner of gong kebyar \ (ours)", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'Gong kebyar, the Balinese style that arose around 1915, is famous for explosions of sound. Here is a burst of our own in that manner: a fast interlocking figure on paired metallophones, beating seven times a second, cut off dead by a gong. Kebyar means to flare up.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"a kebyar burst", detail=r"Part 9's bars and gong", corner=DL, tag_corner=DR)
            ts = [0.0, d["pulse"] * d["n"]]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worldwide(self):
        items = [
            (r"university gamelans in North America, \ Europe, \ Australia and Japan", WHITE),
            (r"students learn by imitation and memory, \ often without notation", WHITE),
            (r"cipher notation \ (\textit{kepatihan}): \ the balungan written as numbers 1 to 7", WHITE),
            (r"a gamelan is played by a group: \ no soloist, \ no conductor; \ the drummer leads", TUNE),
            (r"Part 43 turns to performing together", GREY_A),
        ]
        rows_scene(self, r"gamelan worldwide", items,
                   "Gamelan is now played worldwide. <bookmark mark='b'/> Universities in North America, Europe, Australia and Japan own gamelans, <bookmark mark='c'/> and students learn by imitation and memory, often without notation, <bookmark mark='d'/> though a cipher notation, kepatihan, writes the balungan as the numbers one to seven. <bookmark mark='e'/> A gamelan has no soloist and no conductor; the drummer leads the tempo and the changes. <bookmark mark='f'/> Part 43 turns to performing together.", marks="cdef")
