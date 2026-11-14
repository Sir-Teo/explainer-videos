from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Taqsim(SoundScene):
    def construct(self):
        chapter(self, 8, r"Taqsim and modulation", r"How does an improviser travel?")
        self.what()
        self.hear()
        self.hijaz()
        self.tarab()
        self.learn()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"\textit{taqs\=\i m}: \ an improvised solo, \ usually without a fixed beat", WHITE),
            (r"it reveals the maqam: \ its lower jins first, \ then the ghammaz, \ then the upper register", WHITE),
            (r"and it travels: \ modulating to related maqamat through a shared note, \ then returning", WHITE),
            (r"a good taqsim prepares the listener for the song that follows", TUNE),
            (r"Part 34's alap does the same work, \ in another tradition", GREY_A),
        ]
        rows_scene(self, r"the taqsim", items,
                   "The taqsim is where a player shows the maqam. <bookmark mark='b'/> It is an improvised solo, usually without "
                   "a fixed beat, <bookmark mark='c'/> revealing the maqam step by step: its lower jins, then the ghammaz, then "
                   "the upper register. <bookmark mark='d'/> And it travels, modulating to related maqamat through a shared note, "
                   "and coming home. <bookmark mark='e'/> A good taqsim prepares the listener for the song that follows. "
                   "<bookmark mark='f'/> Part 34's alap does the same work in another tradition.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("taqsim")
        c = clip("taqsim.bayati")
        cs = [p[0] for p in d["phrase"]]
        tot = sum(p[1] for p in d["phrase"])
        ax = Axes(x_range=[0, tot, 2], y_range=[-50, 800, 100], x_length=10.6, y_length=3.2, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": False}).move_to(DOWN * 0.3)
        segs = VGroup()
        t = 0.0
        for i, (cc, dd) in enumerate(d["phrase"]):
            col = EAR if d["saba_from"] <= i < d["saba_to"] and cc in (400,) else (BLUE if d["saba_from"] <= i < d["saba_to"] else TUNE)
            segs.add(Line(ax.c2p(t, cc), ax.c2p(t + dd * 0.92, cc), color=col, stroke_width=6))
            t += dd
        lines = VGroup(*[DashedLine(ax.c2p(0, c_), ax.c2p(tot, c_), color=DIM, stroke_width=1) for c_ in (0, 150, 300, 400, 500, 700)])
        labs = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(ax.c2p(0, c_), LEFT, buff=0.15) for n, c_ in (("D", 0), ("E half-flat", 150), ("F", 300), (r"G$\flat$", 400), ("G", 500), ("A", 700))])
        head = label(r"a taqsim of ours: \ Bayati on D, \ a visit to Saba, \ home", font_size=25, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"gold: \ Bayati; \ blue: \ the Saba passage, \ its lowered fourth G$\flat$ in pink", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a short taqsim of our own on the oud, in Bayati on D, drawn as pitch against time. It dwells on the "
            "tonic, rises to the fourth, G, and falls back. Then it changes one note: G becomes G flat, and the music is "
            "suddenly in Saba, darker and more anxious, a common move from Bayati. It climbs to A through the new note, and "
            "finally returns to Bayati's G and comes home to D."
        ):
            self.play(FadeIn(head), FadeIn(lines), FadeIn(labs), FadeIn(segs), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"taqs\=\i m", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, t0 in enumerate(d["times"]):
                pulse(snd, segs[i], t0, t0 + d["phrase"][i][1] * 0.9, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tarab(self):
        items = [
            (r"\textit{\d{t}arab}: \ the ecstatic state that music can produce in performers and listeners", WHITE),
            (r"A. J. Racy's \textit{Making Music in the Arab World} \ (2003): \ tarab as a shared experience", WHITE),
            (r"audiences respond: \ \textit{All\=ah!}, \ \textit{y\=a sal\=am!} \ after a fine phrase", WHITE),
            (r"the singer repeats and varies a line until the room is moved", TUNE),
            (r"Umm Kulth\=um's concerts could last for hours, \ shaped by the audience's response", GREY_A),
        ]
        rows_scene(self, r"tarab", items,
                   "Why does it matter so much? <bookmark mark='b'/> Arabic has a word, tarab, for the ecstatic state music can "
                   "produce. <bookmark mark='c'/> The ethnomusicologist A. J. Racy described it as an experience shared by "
                   "performers and listeners. <bookmark mark='d'/> Audiences respond aloud after a fine phrase, <bookmark mark='e'/> "
                   "and the singer repeats and varies a line until the room is moved. <bookmark mark='f'/> Umm Kulthum's "
                   "concerts could last for hours, shaped by the audience's response.", marks="cdef")

    # ------------------------------------------------------------------
    def learn(self):
        items = [
            (r"students learn songs and pieces in a maqam before they improvise in it", WHITE),
            (r"they absorb the sayr from the repertory: \ typical openings, \ cadences, \ modulations", WHITE),
            (r"a taqsim recombines these learned gestures in new orders", WHITE),
            (r"the Persian radif and the raga's phrases work the same way", TUNE),
            (r"improvisation within a tradition is fluency, \ not invention from nothing", GREY_A),
        ]
        rows_scene(self, r"learning to improvise", items,
                   "How does one learn to improvise like this? <bookmark mark='b'/> Students learn songs and pieces in a maqam before they improvise in it, <bookmark mark='c'/> absorbing its path from the repertory: typical openings, cadences and modulations. <bookmark mark='d'/> A taqsim recombines these learned gestures in new orders. <bookmark mark='e'/> The Persian radif and the raga's phrases work the same way. <bookmark mark='f'/> Improvisation within a tradition is fluency, not invention from nothing.", marks="cdef")

    # ------------------------------------------------------------------
    def hijaz(self):
        d = load("hijaz")
        c = clip("hijaz.taqsim")
        tot = sum(p[1] for p in d["phrase"])
        ax = Axes(x_range=[0, tot, 2], y_range=[-50, 900, 100], x_length=10.6, y_length=3.0, tips=False, axis_config={"color": GREY_B, "include_numbers": False}).move_to(DOWN * 0.3)
        segs = VGroup()
        t = 0.0
        for cc, dd in d["phrase"]:
            segs.add(Line(ax.c2p(t, cc), ax.c2p(t + dd * 0.92, cc), color=EAR if cc in (100, 400) else TUNE, stroke_width=6))
            t += dd
        labs = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(ax.c2p(0, c_), LEFT, buff=0.15) for n, c_ in (("D", 0), (r"E$\flat$", 100), (r"F$\sharp$", 400), ("G", 500), ("A", 700), (r"B$\flat$", 800))])
        lines = VGroup(*[DashedLine(ax.c2p(0, c_), ax.c2p(tot, c_), color=DIM, stroke_width=1) for c_ in (0, 100, 400, 500, 700, 800)])
        head = label(r"a second taqsim of ours: \ Hijaz on D", font_size=25, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"pink: \ the two notes around Hijaz's wide step, \ E$\flat$ and F$\sharp$", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And a second taqsim of ours, in Hijaz on D. Listen to the wide step between E flat and F sharp, the jins Hijaz's "
            "signature, which many listeners outside the tradition hear as the sound of the whole region. The taqsim dwells "
            "on it, climbs to A and B flat, and comes back down through it to D."
        ):
            self.play(FadeIn(head), FadeIn(lines), FadeIn(labs), FadeIn(segs), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Hijaz", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, t0 in enumerate(d["times"]):
                pulse(snd, segs[i], t0, t0 + d["phrase"][i][1] * 0.9, buff=0.05)
        self.wait(0.3)
        self.clear_scene()
