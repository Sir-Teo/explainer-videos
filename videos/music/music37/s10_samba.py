from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403

ROWS = [("surdo2", r"surdo \ (higher)", BLUE), ("surdo1", r"surdo \ (deeper)", "#60A5FA"), ("caixa", r"caixa", GREY_A),
        ("shaker", r"chocalho", GREY_B), ("tamborim", r"tamborim", EAR), ("agogo_hi", r"agog\^o \ high", TUNE), ("agogo_lo", r"agog\^o \ low", "#A3E635")]
ENTRY = {"surdo2": "surdos", "surdo1": "surdos", "caixa": "caixa", "shaker": "shaker", "tamborim": "tamborim", "agogo_hi": "agogo", "agogo_lo": "agogo"}


class Samba(SoundScene):
    def construct(self):
        chapter(self, 9, r"Samba, \ and call and response", r"How does a parade of hundreds play as one?")
        self.history()
        self.parts()
        self.hear()
        self.surdos()
        self.callresp()
        self.song()
        self.overlap()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"samba took shape in Rio de Janeiro around 1900, \ among Afro-Brazilian families from Bahia", WHITE),
            (r"1917: \ \textit{Pelo Telefone}, \ registered by Donga, \ the first recorded samba", WHITE),
            (r"from 1928 the \textit{escolas de samba}, \ samba schools, \ were founded to parade at Carnival", WHITE),
            (r"a \textit{bateria}, \ the percussion section, \ can number two or three hundred players", TUNE),
            (r"many layers, \ each simple, \ locked to one beat", GREY_A),
        ]
        rows_scene(self, r"samba", items,
                   "Across the Atlantic in Brazil, a different ensemble music grew. <bookmark mark='b'/> Samba took shape in Rio "
                   "de Janeiro around 1900, among Afro-Brazilian families who had come from Bahia. <bookmark mark='c'/> In 1917 "
                   "Pelo Telefone, registered by the composer Donga, became the first recorded samba. <bookmark mark='d'/> From "
                   "1928 samba schools were founded to parade at Carnival, <bookmark mark='e'/> and today a school's bateria, its "
                   "percussion section, can number two or three hundred players. <bookmark mark='f'/> Many layers, each simple, "
                   "all locked to one beat.", marks="cdef")

    # ------------------------------------------------------------------
    def grid(self, d, cell=0.36):
        rows_ = VGroup()
        for k, name, col in ROWS:
            ons = d["parts"][k]
            rows_.add(pat_row(["x" if i in ons else "." for i in range(16)], cell=cell, color=col, name=name, size=17))
        return rows_.arrange(DOWN, buff=0.13, aligned_edge=RIGHT)

    def parts(self):
        d = load("samba")
        rows_ = self.grid(d).move_to(LEFT * 1.6 + DOWN * 0.1)
        notes = VGroup(label(r"bass drums: \ the beat, \ in two voices", font_size=17, color=BLUE), label(r"", font_size=17),
                       label(r"a snare: \ every pulse, \ accents between", font_size=17, color=GREY_A),
                       label(r"a shaker: \ every pulse", font_size=17, color=GREY_B),
                       label(r"a small frame drum: \ syncopated", font_size=17, color=EAR),
                       label(r"a double bell: \ a two-tone pattern", font_size=17, color=TUNE), label(r"", font_size=17))
        for n_, r in zip(notes, rows_):
            n_.next_to(r, RIGHT, buff=0.4)
        head = label(r"a batucada of ours: \ sixteen pulses, \ two bars", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a batucada of our own, in sixteen pulses, two bars of two beats. <bookmark mark='a'/> Two surdos, the "
            "big bass drums, play the beat between them. <bookmark mark='b'/> The caixa, a snare drum, plays every pulse with "
            "accents between the beats, and the chocalho, a shaker, plays every pulse too. <bookmark mark='c'/> The tamborim, "
            "a small frame drum struck with a stick, plays a syncopated figure, and <bookmark mark='d'/> the agogô, a double "
            "bell, plays a two-tone pattern. Real baterias have more, the repinique that leads and the cuíca that sings, but "
            "these will do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            for mark, idx in zip("abcd", ((0, 1), (2, 3), (4,), (5, 6))):
                vo.wait_until(mark)
                self.play(*[FadeIn(rows_[i]) for i in idx], *[FadeIn(notes[i]) for i in idx])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("samba")
        c = clip("samba.layers")
        rows_ = self.grid(d, cell=0.4).move_to(UP * 0.1)
        head = label(r"the parts enter one by one", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it build: the surdos, then the caixa, the shaker, the tamborim and the agogô, and then everything for "
            "three more cycles."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        cyc = 16 * d["pulse"]
        with self.listen(c) as snd:
            window(snd, r"a batucada, \ building", detail=r"membrane, \ noise and bell models", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(*rows_), 0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
            for i, (k, _, col) in enumerate(ROWS):
                t0 = d["entries"][ENTRY[k]]
                ncyc = int(round(d["cycles"] - t0 / cyc))
                flash_cells(snd, rows_[i].cells, d["parts"][k], t0, d["pulse"], ncyc, 16, color=col)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surdos(self):
        items = [
            (r"the deeper surdo \ (\textit{primeira}) \ marks the second beat; \ the higher \ (\textit{segunda}) \ the first", WHITE),
            (r"so samba's weight falls on beat two, \ the opposite of a march", WHITE),
            (r"a third surdo often plays between them, \ varying", WHITE),
            (r"the bass line is a conversation: \ question on one, \ answer on two", TUNE),
            (r"the same shape as the music this chapter turns to now", GREY_A),
        ]
        rows_scene(self, r"two drums in conversation", items,
                   "Listen again to the surdos. <bookmark mark='b'/> The deeper one, the primeira, marks the second beat; the "
                   "higher, the segunda, marks the first. <bookmark mark='c'/> So samba's weight falls on beat two, the opposite "
                   "of a march. <bookmark mark='d'/> A third surdo often plays between them, varying its part. "
                   "<bookmark mark='e'/> The bass line is a conversation, a question on one and an answer on two. "
                   "<bookmark mark='f'/> Which is the shape of the music this chapter turns to now.", marks="cdef")

    # ------------------------------------------------------------------
    def callresp(self):
        items = [
            (r"\textit{call and response}: \ a leader sings a line, \ a group answers", WHITE),
            (r"found across sub-Saharan Africa: \ Ewe songs, \ Shona songs at a bira, \ work songs", WHITE),
            (r"in the Americas: \ spirituals, \ gospel, \ samba's \textit{partido alto}, \ the son's \textit{montuno}", WHITE),
            (r"the leader may improvise; \ the response stays the same and holds the group together", TUNE),
            (r"Part 38's blues is built from it", GREY_A),
        ]
        rows_scene(self, r"call and response", items,
                   "Call and response: a leader sings a line and a group answers. <bookmark mark='b'/> It is found across "
                   "sub-Saharan Africa, in Ewe songs, in Shona songs at a bira, in work songs. <bookmark mark='c'/> In the "
                   "Americas it shapes spirituals and gospel, samba's partido alto, and the montuno section of a son, where the "
                   "singer improvises over a repeated chorus. <bookmark mark='d'/> The leader may improvise; the response stays "
                   "the same and holds the group together. <bookmark mark='e'/> Part 38's blues is built from it.", marks="bcde")

    # ------------------------------------------------------------------
    def song(self):
        d = load("callresp")
        c = clip("callresp.song")
        cyc = d["cycle"]
        p = d["pulse"]
        lead, resp = [], []
        for r in range(d["rounds"]):
            base = r * 2 * 12
            for m, a, du in d["call"]:
                lead.append([m + (2 if (r == 2 and m == 72) else 0), base + a, du])
            for m, a, du in d["response"]:
                resp.append([m, base + 12 + a - (2 if (r == 2 and a == 0) else 0), du + (2 if (r == 2 and a == 0) else 0)])
        roll = voices_roll([lead, resp], width=11.2, height=2.6, colors=[EAR, TUNE], total=d["rounds"] * 24, lo=58, hi=76, bar_h=0.16).move_to(UP * 0.1)
        leg = VGroup(label(r"leader", font_size=20, color=EAR), label(r"chorus", font_size=20, color=TUNE)).arrange(RIGHT, buff=1.0).next_to(roll, UP, buff=0.35)
        cap = label(r"over the bell and a drum on the four beats; \ model voices", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "A call and response of our own, over the standard pattern on the bell and a drum on the four beats. A leader's "
            "phrase fills one cycle, the chorus answers in the next, three times. The third time, the leader varies the call, "
            "and the chorus comes in early."
        ):
            self.play(FadeIn(leg), FadeIn(roll), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"call and response", kind="synthesized", detail=r"model voices, \ bell and drum", corner=DL, tag_corner=DR)
            flash(snd, roll.parts[0].notes, [n[1] * p for n in lead], hot=WHITE, base=EAR)
            flash(snd, roll.parts[1].notes, [n[1] * p for n in resp], hot=WHITE, base=TUNE)
            cursor(snd, roll, 0.0, p)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overlap(self):
        items = [
            (r"in much African practice the parts overlap: \ the chorus enters before the leader has finished", WHITE),
            (r"so there is never silence at the join: \ the cycle has no seam", WHITE),
            (r"the leader's freedom and the chorus's constancy are another kind of interlocking", WHITE),
            (r"the bell, \ the parts, \ the call and the response: \ all cycles inside cycles", TUNE),
            (r"chapter 10 asks how such music is measured, \ and by whom", GREY_A),
        ]
        rows_scene(self, r"no seam", items,
                   "That early entry is typical. <bookmark mark='b'/> In much African practice the parts overlap: the chorus "
                   "enters before the leader has finished. <bookmark mark='c'/> So there is never silence at the join, and the "
                   "cycle has no seam. <bookmark mark='d'/> The leader's freedom and the chorus's constancy are another kind of "
                   "interlocking. <bookmark mark='e'/> The bell, the parts, the call and the response: cycles inside cycles. "
                   "<bookmark mark='f'/> Chapter ten asks how such music is measured, and by whom.", marks="cdef")
