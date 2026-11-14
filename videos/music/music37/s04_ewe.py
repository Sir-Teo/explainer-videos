from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403

ROLE = {"bell": (r"bell \ (gankogui)", TUNE), "rattle": (r"rattle \ (axatse)", GREY_A), "kagan": (r"kagan", BLUE),
        "kidi": (r"kidi", "#A3E635"), "sogo": (r"sogo", EAR), "lead": (r"lead \ (atsimevu)", WHITE)}


def cells_for(name, d):
    if name == "lead":
        return sorted({o for cyc in d["lead"] for o, _ in cyc})
    return sorted({o for ons in d["parts"][name].values() for o in ons})


class Ewe(SoundScene):
    def construct(self):
        chapter(self, 3, r"An Ewe ensemble", r"How do six parts fit around one bell?")
        self.people()
        self.parts()
        self.hear()
        self.relation()
        self.lead()
        self.learning()

    # ------------------------------------------------------------------
    def people(self):
        items = [
            (r"the Ewe live in southeastern Ghana, \ southern Togo and Benin; \ Ewe is a tonal language", WHITE),
            (r"dance-drumming: \ music, \ dance and song as one event, \ at funerals, \ festivals and gatherings", WHITE),
            (r"\textit{agbadza}, \ once a war dance, \ is now among the most widely played; \ \textit{gahu} came west from Nigeria and Benin", WHITE),
            (r"an ensemble: \ bell, \ rattle, \ supporting drums, \ a lead drum, \ singers and dancers", TUNE),
            (r"we play parts of our own in that manner, \ not a transcription of any one piece", GREY_A),
        ]
        rows_scene(self, r"the Ewe", items,
                   "The standard pattern is the backbone of much Ewe music. <bookmark mark='b'/> The Ewe live in southeastern "
                   "Ghana, southern Togo and Benin, and speak a tonal language, which matters for drums. <bookmark mark='c'/> Their "
                   "dance-drumming is music, dance and song as a single event, at funerals, festivals and gatherings. "
                   "<bookmark mark='d'/> Agbadza, once a war dance, is among the most widely played today; gahu came west "
                   "from Nigeria and Benin in the twentieth century. <bookmark mark='e'/> An ensemble has a bell, a rattle, supporting drums, a "
                   "lead drum, singers and dancers. <bookmark mark='f'/> What follows are parts of our own in that manner, not a "
                   "transcription of any one piece.", marks="cdef")

    # ------------------------------------------------------------------
    def grid(self, d, cell=0.38):
        rows_ = VGroup()
        for name in d["order"]:
            ons = cells_for(name, d) if name != "lead" else []          # the lead's phrase changes: lit as it plays
            pat = ["x" if i in ons else "." for i in range(12)]
            nm, col = ROLE[name]
            rows_.add(pat_row(pat, cell=cell, color=col, name=nm, size=18))
        rows_.arrange(DOWN, buff=0.18, aligned_edge=RIGHT)
        return rows_

    def parts(self):
        d = load("ewe")
        rows_ = self.grid(d).move_to(DOWN * 0.1 + LEFT * 1.6)
        notes = VGroup(label(r"the timeline: \ everyone's reference", font_size=17, color=TUNE),
                       label(r"down on the four beats, \ up with the bell", font_size=17, color=GREY_A),
                       label(r"a high drum: \ pairs between the beats", font_size=17, color=BLUE),
                       label(r"open and muted strokes, \ in conversation", font_size=17, color="#A3E635"),
                       label(r"a lower drum, \ answering", font_size=17, color=EAR),
                       label(r"the lead: \ a different phrase each cycle", font_size=17, color=WHITE))
        for n, r in zip(notes, rows_):
            n.next_to(r, RIGHT, buff=0.4)
        head = label(r"six parts in twelve pulses \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the six parts, each drawn on the twelve-pulse cycle. <bookmark mark='a'/> The iron double bell, "
            "gankogui, plays the timeline, the reference for everyone. <bookmark mark='b'/> The axatse, a gourd rattle in a "
            "net of beads, strikes down on the thigh on the four beats and up against the hand with the bell. "
            "<bookmark mark='c'/> Kagan, the smallest drum, plays muted pairs between the beats. <bookmark mark='d'/> Kidi "
            "mixes open tones and muted presses, and sogo, a bigger drum, answers it. <bookmark mark='e'/> Over them the lead "
            "drum, atsimevu, the tallest, plays phrases that change, call to the other drums, and cue the dancers. Its row is "
            "left empty here, because its phrase is different each time round; it will light as it plays."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            for mark, idx in zip("abcde", ((0,), (1,), (2,), (3, 4), (5,))):
                vo.wait_until(mark)
                self.play(*[FadeIn(rows_[i]) for i in idx], *[FadeIn(notes[i]) for i in idx])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("ewe")
        c = clip("ewe.layers")
        rows_ = self.grid(d, cell=0.44).move_to(UP * 0.1)
        head = label(r"the parts enter one by one", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now hear them enter one by one: the bell for two cycles, then the rattle, kagan, kidi and sogo, and finally the "
            "lead drum for four cycles. Watch each row light where its part strikes, and try to keep hold of the bell as the "
            "texture thickens."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        total = d["cycles"]
        cyc = 12 * d["pulse"]
        with self.listen(c) as snd:
            window(snd, r"six parts, \ entering", detail=r"bell, \ noise and membrane models", corner=DL, tag_corner=DR)
            for i, name in enumerate(d["order"]):
                t0 = d["entries"][name]
                ncyc = int(round(total - t0 / cyc))
                if name == "lead":
                    for k in range(ncyc):
                        ons = [o for o, _ in d["lead"][k % 4]]
                        flash_cells(snd, rows_[i].cells, ons, t0 + k * cyc, d["pulse"], 1, 12, color=ROLE[name][1])
                else:
                    flash_cells(snd, rows_[i].cells, cells_for(name, d), t0, d["pulse"], ncyc, 12, color=ROLE[name][1])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relation(self):
        items = [
            (r"each player knows a part by where it falls against the bell, \ not by counting", WHITE),
            (r"the parts are short and repeat; \ the music lies in how they interlock", WHITE),
            (r"a part played alone can sound like a different rhythm: \ its meaning is relational", WHITE),
            (r"the bell is the one fixed point: \ lose it and you lose your place", TUNE),
            (r"Part 11's meter, \ distributed across an ensemble", GREY_A),
        ]
        rows_scene(self, r"a part is a relation", items,
                   "How do the players stay together? <bookmark mark='b'/> Each knows a part by where it falls against the bell, "
                   "not by counting pulses. <bookmark mark='c'/> The parts are short and repeat; the music lies in how they "
                   "interlock. <bookmark mark='d'/> A part played alone can sound like a different rhythm altogether: its "
                   "meaning is its relation to the others. <bookmark mark='e'/> The bell is the one fixed point; teachers stress "
                   "that to lose the bell is to lose your place. <bookmark mark='f'/> Part 11's meter, here distributed across a "
                   "whole ensemble.", marks="cdef")

    # ------------------------------------------------------------------
    def lead(self):
        items = [
            (r"the lead drum plays phrases that change, \ and the ensemble's drums respond", WHITE),
            (r"drum strokes can carry the tones of spoken Ewe: \ phrases are often learned with words", WHITE),
            (r"the lead drummer signals changes of section and the dancers' movements", WHITE),
            (r"improvisation within a repertoire of known phrases, \ as in Part 34's tabla", TUNE),
            (r"call and response returns in chapter 9", GREY_A),
        ]
        rows_scene(self, r"the lead drum", items,
                   "The lead drum is different. <bookmark mark='b'/> It plays phrases that change, and the supporting drums "
                   "respond. <bookmark mark='c'/> Because Ewe is a tonal language, drum strokes of high and low pitch can follow "
                   "the tones of speech, and phrases are often learned with words. <bookmark mark='d'/> The lead drummer signals "
                   "changes of section and cues the dancers. <bookmark mark='e'/> It is improvisation within a repertoire of "
                   "known phrases, much like the tabla player of Part 34. <bookmark mark='f'/> Call and response returns in "
                   "chapter nine.", marks="cdef")

    # ------------------------------------------------------------------
    def learning(self):
        items = [
            (r"taught by ear and by syllables: \ each part has a spoken mnemonic", WHITE),
            (r"Ewe master drummers have taught at universities in Ghana, \ the USA and Europe since the 1960s", WHITE),
            (r"David Locke's studies of gahu and agbadza write the parts down against the bell", WHITE),
            (r"transcription is an argument: \ chapter 4 shows why", TUNE),
            (r"the lab lets you mute and solo each of our parts", GREY_A),
        ]
        rows_scene(self, r"learning the parts", items,
                   "How is this learned? <bookmark mark='b'/> By ear and by syllables: each part has a spoken mnemonic. "
                   "<bookmark mark='c'/> Ewe master drummers have taught at universities in Ghana, the United States and Europe "
                   "since the nineteen-sixties, <bookmark mark='d'/> and David Locke's studies of gahu and agbadza write the "
                   "parts down against the bell. <bookmark mark='e'/> But transcription is itself an argument, as chapter four "
                   "shows. <bookmark mark='f'/> The lab lets you mute and solo each of our parts.", marks="cdef")
