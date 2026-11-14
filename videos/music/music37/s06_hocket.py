from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class Hocket(SoundScene):
    def construct(self):
        chapter(self, 5, r"Interlocking and hocket", r"Can one melody belong to several players?")
        self.what()
        self.siku()
        self.pipes()
        self.arom()
        self.why()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"\textit{hocket} \ (Latin \textit{hoquetus}, \ a hiccup): \ a melody split so each player sounds only some notes", WHITE),
            (r"in thirteenth- and fourteenth-century Europe, \ two voices traded notes and rests \ (Part 23)", WHITE),
            (r"in the Andes, \ the \textit{siku} panpipe is split in two rows, \ played by two people", WHITE),
            (r"in Central Africa, \ ensembles of horns that each sound one or two pitches", TUNE),
            (r"in Bali, \ kotekan \ (Part 36); \ in handbell choirs, \ one bell per player", GREY_A),
        ]
        rows_scene(self, r"hocket", items,
                   "The Ewe parts interlock in time. A stronger kind of interlocking shares out a melody itself. "
                   "<bookmark mark='b'/> This is hocket, from the Latin for a hiccup: a melody split so that each player sounds "
                   "only some of its notes. <bookmark mark='c'/> In thirteenth- and fourteenth-century Europe, two voices traded "
                   "notes and rests, as Part 23 heard. <bookmark mark='d'/> In the Andes, the siku panpipe is split into two rows "
                   "held by two people. <bookmark mark='e'/> In Central Africa there are ensembles of horns that each sound one "
                   "or two pitches. <bookmark mark='f'/> And in Bali there is kotekan, from Part 36; in a handbell choir, one bell "
                   "per player.", marks="cdef")

    # ------------------------------------------------------------------
    def siku(self):
        d = load("hocket")
        c = clip("hocket.siku")
        mel = d["melody"]
        ira = [[p, a, du] for (p, a, du), x in zip(mel, d["ira"]) if x is not None]
        arka = [[p, a, du] for (p, a, du), x in zip(mel, d["arka"]) if x is not None]
        roll = voices_roll([ira, arka], width=10.5, height=2.4, colors=[TUNE, BLUE], lo=70, hi=83, bar_h=0.16).move_to(DOWN * 0.3)
        def pipes_row(pitches, col):
            g = VGroup(*[Rectangle(width=0.32, height=1.6 - 0.12 * k, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.25) for k in range(len(pitches))]).arrange(RIGHT, buff=0.06, aligned_edge=UP)
            return g
        ira_p = VGroup(pipes_row([72, 76, 79, 83], TUNE), label(r"ira: \ C E G B", font_size=18, color=TUNE)).arrange(DOWN, buff=0.15)
        arka_p = VGroup(pipes_row([74, 77, 81, 84], BLUE), label(r"arka: \ D F A C", font_size=18, color=BLUE)).arrange(DOWN, buff=0.15)
        top = VGroup(ira_p, arka_p).arrange(RIGHT, buff=1.4).to_edge(UP, buff=0.35)
        stage = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (r"ira alone", r"arka alone", r"both")]).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "A siku is a panpipe in two halves. One row, called ira, has every other note of the scale, here C, E, G and B; "
            "the other, arka, has the notes between, D, F, A and C. Each row is held by a different player, so no melody that "
            "moves by step can be played by one person. <bookmark mark='a'/> Here is the Tune's opening on two model "
            "panpipes: the ira player alone, the arka player alone, and then both."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(roll), FadeIn(stage))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"ira, \ arka, \ both", detail=r"Part 8's flute model", corner=DL, tag_corner=DR)
            for k, which in (("ira", (0,)), ("arka", (1,)), ("both", (0, 1))):
                for j in which:
                    v = [ira, arka][j]
                    flash(snd, roll.parts[j].notes, [st[k] + n[1] * d["beat"] for n in v], hot=WHITE, base=[TUNE, BLUE][j])
            ks = ["ira", "arka", "both"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        ans = label(r"alone, \ each part is a stutter; \ together, \ one melody", font_size=22, color=TUNE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Alone, each part is a stutter of notes and silences. Together, they are one melody, and the join is "
            "inaudible. Andean siku bands are large, and every pair of players shares its melodies this way."
        ):
            self.play(FadeOut(stage), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipes(self):
        d = load("hocket")
        c = clip("hocket.pipes")
        names = {72: "C", 74: "D", 76: "E", 79: "G", 81: "A"}
        rows_ = VGroup()
        for i, m in enumerate(d["order"]):
            ons = d["pipes"][str(m)]
            pat = ["x" if k in ons else "." for k in range(12)]
            rows_.add(pat_row(pat, cell=0.42, color=VOICE_C[i % 5], name=rf"pipe {names[m]}", size=18))
        rows_.arrange(DOWN, buff=0.16, aligned_edge=RIGHT)
        mel = VGroup(*[label(names[m] if m else "", font_size=20, color=WHITE) for m in d["combined"]])
        for k, n in enumerate(mel):
            n.next_to(rows_[-1].cells[k], DOWN, buff=0.35)
        ml = label(r"heard", font_size=18, color=WHITE).next_to(mel, LEFT, buff=0.4).match_x(rows_[-1][0])
        g = VGroup(rows_, mel, ml).move_to(DOWN * 0.1)
        head = label(r"five pipes, \ one pitch each \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Push the idea further: five pipes, each with one pitch only. Each player has a short rhythm of their own on a "
            "single note, and the melody exists only between them. The pipes enter one at a time: first A, alone for two "
            "cycles, then G, E, D and C, and then all five for three more cycles."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"five pipes, \ entering", detail=r"Part 8's flute model", corner=DL, tag_corner=DR)
            total = 0.0
            end = c.duration - 0.8
            for i, m in enumerate(d["order"]):
                t0 = d["entries"][str(m)]
                ncyc = int(round((end - t0) / (12 * d["pulse"])))
                flash_cells(snd, rows_[i].cells, d["pipes"][str(m)], t0, d["pulse"], ncyc, 12, color=VOICE_C[i % 5])
            last = d["entries"][str(d["order"][-1])]
            flash_cells(snd, mel, [k for k, m in enumerate(d["combined"]) if m], last, d["pulse"], int(round((end - last) / (12 * d["pulse"]))), 12, color=WHITE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arom(self):
        items = [
            (r"the Banda-Linda of the Central African Republic play in horn ensembles of up to eighteen", WHITE),
            (r"each horn sounds one or two pitches; \ the polyphony exists only in the whole", WHITE),
            (r"Simha Arom recorded each player separately, \ hearing the others on headphones \ (from the 1970s)", WHITE),
            (r"so each part could be written down exactly, \ and the whole rebuilt from its parts", TUNE),
            (r"\textit{African Polyphony and Polyrhythm} \ (1985; \ English 1991)", GREY_A),
        ]
        rows_scene(self, r"how to transcribe a hocket", items,
                   "How can anyone write such music down? <bookmark mark='b'/> The Banda-Linda of the Central African Republic "
                   "play in ensembles of up to eighteen horns, <bookmark mark='c'/> each sounding one or two pitches, so that the "
                   "polyphony exists only in the whole. <bookmark mark='d'/> Simha Arom's solution, from the nineteen-seventies, "
                   "was to record each player separately while they heard the others on headphones, <bookmark mark='e'/> so "
                   "that every part could be written down exactly and the whole rebuilt from its parts. <bookmark mark='f'/> The "
                   "results are in his African Polyphony and Polyrhythm.", marks="cdef")

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"breath: \ a pipe or horn player can rest between their notes", WHITE),
            (r"speed: \ two players together can play faster than either alone", WHITE),
            (r"sound: \ similar pipes, \ close in pitch, \ fuse into one line in the ear \ (Part 16)", WHITE),
            (r"society: \ no one owns the melody; \ it exists only if everyone plays", TUNE),
            (r"the next chapters hear an instrument that does this inside one player's hands", GREY_A),
        ]
        rows_scene(self, r"why hocket?", items,
                   "Why make music this way? <bookmark mark='b'/> For breath: a pipe player can rest between notes. "
                   "<bookmark mark='c'/> For speed: two players together can play faster than either alone. "
                   "<bookmark mark='d'/> For sound: similar pipes close in pitch fuse into one line in the ear, as Part 16 "
                   "explained. <bookmark mark='e'/> And for society: no one owns the melody, which exists only if everyone plays. "
                   "<bookmark mark='f'/> The next chapters hear an instrument on which one player's two hands do this, and the "
                   "ear does the rest.", marks="cdef")
