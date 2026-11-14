from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


def blocks(plan, colors, unit=0.32, h=0.8):
    g = VGroup()
    for name, bars in plan:
        r = Rectangle(width=unit * bars, height=h, stroke_color=colors[name], stroke_width=2, fill_color=colors[name], fill_opacity=0.25)
        g.add(VGroup(r, label(name, font_size=20, color=WHITE).move_to(r)))
    return g.arrange(RIGHT, buff=0.06)


class Forms(SoundScene):
    def construct(self):
        chapter(self, 1, r"From AABA to verse and chorus", r"How did the shape of a song change?")
        self.tinpan()
        self.aaba()
        self.vc()
        self.why()
        self.factories()

    # ------------------------------------------------------------------
    def tinpan(self):
        items = [
            (r"Tin Pan Alley, \ New York, \ 1890s--1950s: \ songs written to sell as sheet music, \ then records", WHITE),
            (r"the standard form: \ a verse, \ often dropped, \ then a 32-bar refrain in four eight-bar sections, \ AABA", WHITE),
            (r"A states the tune twice; \ B, \ the bridge or `middle eight', \ goes elsewhere; \ A returns", WHITE),
            (r"Gershwin, \ Berlin, \ Porter, \ Rodgers: \ the songs jazz took as standards \ (Part 39)", TUNE),
            (r"the title usually sits at the start or end of each A", GREY_A),
        ]
        rows_scene(self, r"the thirty-two-bar song", items,
                   "For the first half of the twentieth century, American popular songs came from Tin Pan Alley, songwriters "
                   "in New York writing to sell sheet music, and then records. <bookmark mark='b'/> The standard form was a verse, "
                   "often dropped, then a thirty-two bar refrain in four eight-bar sections: A A B A. <bookmark mark='c'/> A "
                   "states the tune twice; B, the bridge or middle eight, goes somewhere else; A returns. <bookmark mark='d'/> "
                   "Gershwin, Berlin, Porter and Rodgers wrote in it, and jazz took their songs as standards, as Part 39 heard. "
                   "<bookmark mark='e'/> The title usually sits at the start or end of each A.", marks="bcde")

    # ------------------------------------------------------------------
    def aaba(self):
        d = load("forms")
        c = clip("forms.aaba")
        colors = {"A": TUNE, "B": EAR}
        g = blocks([("A", 8), ("A", 8), ("B", 8), ("A", 8)], colors, unit=0.36).move_to(UP * 0.6)
        cap = label(r"a song of ours in AABA, \ each section shortened to four bars for listening", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"AABA: \ thirty-two bars", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the shape in a song of our own, each section shortened to four bars: the A tune, the A tune again, the "
            "bridge, which moves to the subdominant and leans on the dominant, and the A tune to close."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"AABA", kind="synthesized", detail=r"a model voice, \ Part 7's piano, \ bass", corner=DL, tag_corner=DR)
            for i, (name, t0) in enumerate(d["aaba"]):
                pulse(snd, g[i], t0, t0 + 16 * beat - 0.05, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vc(self):
        d = load("forms")
        c = clip("forms.vc")
        colors = {"verse": BLUE, "pre": GREY_A, "chorus": TUNE}
        g = blocks([("verse", 4), ("pre", 2), ("chorus", 4)], colors, unit=1.0).move_to(UP * 0.6)
        notes = VGroup(label(r"verse: \ new words each time, \ sparser", font_size=18, color=BLUE),
                       label(r"pre-chorus: \ lift", font_size=18, color=GREY_A),
                       label(r"chorus: \ same words each time, \ the title, \ fullest", font_size=18, color=TUNE)).arrange(RIGHT, buff=0.6).next_to(g, DOWN, buff=0.5)
        head = label(r"verse, \ pre-chorus, \ chorus", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "From the 1960s the verse and chorus took over. The verse tells the story, with new words each time; a "
            "pre-chorus lifts; the chorus repeats the same words, carries the title, and is the fullest moment, here with a "
            "second voice and a pad."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes))
        with self.listen(c) as snd:
            window(snd, r"verse, \ pre-chorus, \ chorus", kind="synthesized", detail=r"a model voice and band", corner=DL, tag_corner=DR)
            ks = ["verse", "pre", "chorus"]
            for i, k in enumerate(ks):
                end = d["vc"][ks[i + 1]] - 0.05 if i < 2 else c.duration
                pulse(snd, g[i], d["vc"][k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"rock and roll and the 45 rpm single favoured shorter, \ repeated, \ danceable forms", WHITE),
            (r"the Beatles and their contemporaries mixed both: \ verse--chorus songs with a middle eight", WHITE),
            (r"radio play rewarded a chorus heard early and often", WHITE),
            (r"the chorus became the song's hook and its title: \ the part you remember", TUNE),
            (r"chapter 2 turns to the harmony under those choruses", GREY_A),
        ]
        rows_scene(self, r"why the change?", items,
                   "Why the change? <bookmark mark='b'/> Rock and roll and the seven-inch single favoured shorter, repeated, "
                   "danceable forms. <bookmark mark='c'/> The Beatles and their contemporaries mixed both, writing verse and "
                   "chorus songs with a middle eight. <bookmark mark='d'/> Radio rewarded a chorus heard early and often. "
                   "<bookmark mark='e'/> The chorus became the song's hook and its title: the part you remember. "
                   "<bookmark mark='f'/> Chapter two turns to the harmony under those choruses.", marks="cdef")

    # ------------------------------------------------------------------
    def factories(self):
        items = [
            (r"New York's Brill Building, \ early 1960s: \ teams of writers in small rooms, \ writing to order", WHITE),
            (r"Motown, \ Detroit, \ from 1959: \ writers, \ a house band and quality-control meetings, \ like a car plant", WHITE),
            (r"from the 1990s, \ Swedish writer-producers such as Max Martin wrote hits for others worldwide", WHITE),
            (r"the song as a designed product, \ tested against an audience", TUNE),
            (r"Part 42 treats composing as search; \ the market is one of the judges", GREY_A),
        ]
        rows_scene(self, r"song factories", items,
                   "Songs have often been made in factories. <bookmark mark='b'/> In New York's Brill Building in the early "
                   "1960s, teams of writers in small rooms wrote to order. <bookmark mark='c'/> Motown, in Detroit from 1959, had "
                   "writers, a house band and weekly quality-control meetings, modelled on the city's car plants. "
                   "<bookmark mark='d'/> From the 1990s Swedish writer-producers such as Max Martin wrote hits for singers around "
                   "the world. <bookmark mark='e'/> The song became a designed product, tested against an audience. "
                   "<bookmark mark='f'/> Part 42 treats composing as search, and the market is one of the judges.", marks="cdef")
