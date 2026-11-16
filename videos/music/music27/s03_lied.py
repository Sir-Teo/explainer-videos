from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Lied(SoundScene):
    def construct(self):
        chapter(self, 2, r"The song and its piano", r"What can a piano say that the words do not?", extra=((1815, r"Schubert's \textit{Erlkönig}"),))
        self.schubert()
        self.keys()
        self.share()
        self.quiz()
        self.cycles()

    # ------------------------------------------------------------------
    def schubert(self):
        items = [
            (r"the Lied: \ a German poem set for voice and piano, \ for a room of friends", WHITE),
            (r"Schubert wrote more than 600; \ \textit{Erlkönig} \ (1815) \ at eighteen", WHITE),
            (r"in \textit{Erlkönig} the piano's hammering octaves are the galloping horse", WHITE),
            (r"strophic songs repeat one tune for every stanza; \ through-composed songs follow the poem", TUNE),
            (r"Schubert's favourite move between: \ the same tune, \ changed from major to minor", EAR),
        ]
        rows_scene(self, r"the Lied", items,
                   "The Romantic song began in rooms. <bookmark mark='b'/> A Lied is a German poem set for voice and piano, "
                   "sung among friends; Schubert's circle called these evenings Schubertiads. <bookmark mark='c'/> Schubert "
                   "wrote more than six hundred of them, and set Goethe's Erlkönig at eighteen, in 1815, <bookmark mark='d'/> "
                   "where the piano's hammering octaves are the horse galloping through the night. <bookmark mark='e'/> A "
                   "strophic song repeats one tune for every stanza; a through-composed song follows the poem wherever it "
                   "goes. <bookmark mark='f'/> Schubert's favourite move lies between the two: the same tune again, but changed "
                   "from major to minor, so that the music remembers and grieves at once.", marks="cdef")

    # ------------------------------------------------------------------
    def keys(self):
        d = load("lied")
        T = d["bars"]
        x0, W = -5.6, 11.2
        cells = VGroup()
        rowy = {(4, "major"): 0.9, (4, "minor"): 0.3, (11, "major"): 1.5, (0, "major"): -0.3}
        for k in d["keys"]:
            key = tuple(k["key"])
            y = rowy.get(key, -0.9)
            col = TUNE if key == (4, "major") else EAR if key == (4, "minor") else BLUE if key == (11, "major") else GREY_B
            cells.add(Rectangle(width=W * 2 / T - 0.03, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + W * (k["bar"] + 1) / T, y, 0]))
        names = VGroup(*[label(n, font_size=18, color=c_).move_to([x0 - 0.95, y, 0]) for n, y, c_ in (
            (r"B major", 1.5, BLUE), (r"E major", 0.9, TUNE), (r"E minor", 0.3, EAR), (r"C major", -0.3, GREY_B), (r"other", -0.9, GREY_B))])
        ticks = VGroup(*[label(str(b), font_size=15, color=GREY_B).move_to([x0 + W * b / T, -1.5, 0]) for b in range(0, int(T) + 1, 10)])
        stz = VGroup(*[label(t, font_size=18, color=GREY_A).move_to([x0 + W * b / T, -2.1, 0]) for t, b in (
            (r"stanza 1", 15), (r"stanza 2: \ minor", 31), (r"the cold wind", 47), (r"the last stanza", 66))])
        head = label(r"\textit{Der Lindenbaum}: \ the key of every two bars", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Part 15's key-finder can hear that move. Here it reads Der Lindenbaum two bars at a time. "
            "<bookmark mark='a'/> The first stanza, the happy memory of the tree, sits in E major, with B major, its "
            "dominant, at the ends of phrases. <bookmark mark='b'/> Then the same tune returns, now in E minor: the "
            "traveller has to pass the tree in the dark. <bookmark mark='c'/> A cold wind blows, the piano storms, and the "
            "key wanders; <bookmark mark='d'/> and the last stanza brings back E major, as a memory heard from far away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(ticks))
            for mark, (a, b) in zip("abcd", ((0, 26), (26, 36), (36, 56), (56, 80))):
                vo.wait_until(mark)
                sel = [c_ for c_, k in zip(cells, d["keys"]) if a <= k["bar"] < b]
                self.play(LaggedStart(*[FadeIn(c_) for c_ in sel], lag_ratio=0.05), FadeIn(stz["abcd".index(mark)]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def share(self):
        d = load("lied")
        sh = d["share"]
        bars_v = columns(sh["voice"], None, width=10.4, height=1.4, color=TUNE, font_size=14).move_to(UP * 0.9)
        bars_p = columns(sh["piano"], None, width=10.4, height=1.4, color=GREY_A, font_size=14).move_to(DOWN * 1.3)
        lv = label(r"voice: \ notes per two bars", font_size=19, color=TUNE).next_to(bars_v, UP, buff=0.15).align_to(bars_v, LEFT)
        lp = label(r"piano: \ notes per two bars", font_size=19, color=GREY_A).next_to(bars_p, UP, buff=0.15).align_to(bars_p, LEFT)
        cap = label(rf"in all: \ {sh['n_voice']} sung notes, \ {sh['n_piano']} played: \ about {sh['n_piano'] / sh['n_voice']:.0f} to 1", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Count the notes, and the piano's part in the song is plain to see. Above, the voice's notes in every two bars; "
            f"below, the piano's. The voice sings {say(sh['n_voice'])} notes in the whole song. The piano plays "
            f"{say(sh['n_piano'])}, about {say(round(sh['n_piano'] / sh['n_voice']))} for every one sung, and it plays alone "
            "where the voice is silent, in the prelude, between the stanzas, and in the storm. The tree, the wind and the "
            "memory are in the accompaniment."
        ):
            self.play(FadeIn(lv), FadeIn(bars_v), FadeIn(lp), FadeIn(bars_p), FadeIn(cap))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("lied")
        c = clip("lied.quiz")
        card = listen_card(r"The same four bars of \textit{Der Lindenbaum}, \ twice: \ once in E major, \ once in E minor. \ "
                           r"Which is the minor, \ A or B? \ Listen to the third note of the tune.", width=10.6)
        with self.voiceover(
            "Hear it for yourself. The same four bars of the song, twice: once from the first stanza, in E major, and once "
            "from the second, in E minor, in some order. Which is the minor, A or B? Listen to the third note of the tune."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll([d["A"]["voice"], d["A"]["piano"]], width=5.4, height=2.8, colors=[EAR, GREY_A], lo=40, hi=80, bar_h=0.08).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll([d["B"]["voice"], d["B"]["piano"]], width=5.4, height=2.8, colors=[TUNE, GREY_A], lo=40, hi=80, bar_h=0.08).move_to(RIGHT * 3.3 + DOWN * 0.2)
        for g in (gA, gB):
            for b in g.parts[0].notes:
                b.set_color(GREY_A)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"piano and a synthetic tenor", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, [d["A"]["voice"], d["A"]["piano"]], d["starts"]["A"], d["unit"], colors=[GREY_A, GREY_A])
            flash_voices(snd, gB, [d["B"]["voice"], d["B"]["piano"]], d["starts"]["B"], d["unit"], colors=[GREY_A, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"A: \ G natural, \ E minor \ (bar 27)", font_size=22, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ G sharp, \ E major \ (bar 7)", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "A is the minor. The tune is the same, but where B sings G sharp, A sings G natural, and the piano's chords "
            "change with it. One semitone, and a memory becomes a loss."
        ):
            self.play(FadeIn(ans), gA.parts[0].animate.set_color(EAR), gB.parts[0].animate.set_color(TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycles(self):
        items = [
            (r"the song cycle: \ a story told in songs \ (Beethoven, \ \textit{An die ferne Geliebte}, \ 1816)", WHITE),
            (r"Schubert: \ \textit{Die schöne Müllerin} \ (1823), \ \textit{Winterreise} \ (1827)", WHITE),
            (r"Robert Schumann's year of song, \ 1840: \ \textit{Dichterliebe}, \ the piano gets the last word", WHITE),
            (r"Clara Schumann, \ Fanny Hensel, \ Brahms, \ Wolf: \ the Lied as a serious art", TUNE),
            (r"Part 40 returns to song: \ words, \ breath and accompaniment, \ in every tradition", GREY_A),
        ]
        rows_scene(self, r"songs that tell a story", items,
                   "Songs gathered into stories. <bookmark mark='b'/> Beethoven's An die ferne Geliebte, of 1816, is an influential early integrated song cycle, with earlier collections and related practices complicating a first-ever claim, songs that follow one another without a break. <bookmark mark='c'/> Schubert's two cycles on Müller's poems followed. <bookmark mark='d'/> In 1840, the year he married Clara Wieck, Robert Schumann wrote well over a hundred songs, among them Dichterliebe, whose last song ends with a long piano postlude: the piano has the last word. <bookmark mark='e'/> Clara Schumann, Fanny Hensel, Brahms and Hugo Wolf further developed an already substantial song tradition. <bookmark mark='f'/> Part 40 comes back to song in every tradition: words, breath and accompaniment.", marks="cdef")
