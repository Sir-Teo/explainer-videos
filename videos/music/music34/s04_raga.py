from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Raga(SoundScene):
    def construct(self):
        chapter(self, 3, r"More than a scale", r"What makes a raga a raga?")
        self.what()
        self.quiz()
        self.bhupali()
        self.grammar()
        self.time()
        self.vadi()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"a raga has a scale, \ but two ragas can share one and still be different", WHITE),
            (r"\textit{\=aroha} and \textit{avaroha}: \ how it climbs and how it descends, \ often by different notes", WHITE),
            (r"\textit{pakad} or \textit{calan}: \ characteristic phrases that identify it", WHITE),
            (r"\textit{v\=ad\=i} and \textit{samv\=ad\=i}: \ the notes it dwells on", TUNE),
            (r"gamaka: \ how each note is approached, \ shaken, \ left", GREY_A),
        ]
        rows_scene(self, r"what a raga is", items,
                   "A raga is not just a scale. <bookmark mark='b'/> It has one, but two ragas can share the same notes and still be different ragas. <bookmark mark='c'/> A raga has a way of climbing, the aroha, and a way of descending, the avaroha, often by different notes. <bookmark mark='d'/> It has characteristic phrases, pakad or calan, by which a listener recognises it within seconds. <bookmark mark='e'/> Hindustani accounts often identify prominent vadi and samvadi notes; their status and assignments vary by raga and school. <bookmark mark='f'/> And it has its own ways of approaching, shaking and leaving each note, the gamakas of the next chapter.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("raga")
        c = clip("raga.quiz")
        card = listen_card(r"Two ragas, \ each as an ascent, \ a descent and a characteristic phrase, \ over the drone. \ "
                           r"One is Bilawal, \ with the notes of the major scale; \ the other is Yaman, \ with a raised Ma. \ "
                           r"Which is Yaman, \ A or B?", width=10.6)
        with self.voiceover(
            "A question for your ears. Two ragas, each played as an ascent, a descent and a characteristic phrase of our own, "
            "over the drone. One is Bilawal, with the notes of the major scale. The other is Yaman, an evening raga, with a "
            "raised Ma. Which is Yaman, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        rows_ = VGroup()
        for key, name in zip("AB", d["order"]):
            r = d["ragas"][name]
            rows_.add(VGroup(label(key, font_size=40, color=GREY_A),
                             VGroup(VGroup(label(r"up:", font_size=16, color=GREY_A), sargam(r["aroha"], size=20)).arrange(RIGHT, buff=0.25),
                                    VGroup(label(r"down:", font_size=16, color=GREY_A), sargam(r["avaroha"], size=20)).arrange(RIGHT, buff=0.25),
                                    VGroup(label(r"phrase:", font_size=16, color=GREY_A), sargam(r["pakad"], size=20)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.2)
        for g in rows_:
            g[1].set_opacity(0.0)
        self.play(FadeOut(card), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            pulse(snd, rows_[0][0], d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.1)
            pulse(snd, rows_[1][0], d["starts"]["B"], c.duration, buff=0.1)
        with self.voiceover(
            "B is Yaman. Its Ma is raised, tivra, written M with a mark, and it typically begins its climb from Ni below "
            "Sa and skips Sa and Pa on the way up. A is our simplified Bilawal-based teaching sketch, using the major-scale notes. Same Sa, the same five "
            "other notes, and a different raga: these sketches contrast a pitch alteration and a habit of movement; a complete raga identity needs more context."
        ):
            self.play(*[g[1].animate.set_opacity(1.0) for g in rows_])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grammar(self):
        items = [
            (r"Yaman climbs N. \ R G M' D N S' \ ---\ it avoids Sa and Pa going up", WHITE),
            (r"it descends S' N D P M' G R S, \ with every note", WHITE),
            (r"such rules are tendencies taught by example, \ not laws: \ masters bend them", WHITE),
            (r"Part 14's melody model could learn them: \ which note follows which, \ in each raga", TUNE),
            (r"computational studies do exactly this to recognise ragas \ (chapter 10)", GREY_A),
        ]
        rows_scene(self, r"a raga's grammar", items,
                   "A raga's movement has a grammar. <bookmark mark='b'/> Yaman climbs Ni, Re, Ga, raised Ma, Dha, Ni, Sa, "
                   "avoiding Sa and Pa on the way up, <bookmark mark='c'/> and comes down through every note. "
                   "<bookmark mark='d'/> Such rules are tendencies, taught by example rather than stated as laws, and great "
                   "musicians bend them. <bookmark mark='e'/> Part 14's melody model could learn them, which note follows which "
                   "in each raga, <bookmark mark='f'/> and computational studies do exactly that to recognise ragas, as the "
                   "frontier chapter shows.", marks="cdef")

    # ------------------------------------------------------------------
    def time(self):
        items = [
            (r"Hindustani tradition assigns ragas to times of day: \ Bhairav at dawn, \ Yaman in the evening", WHITE),
            (r"and to seasons: \ Malhar for the monsoon", WHITE),
            (r"each raga carries a mood, \ \textit{rasa}: \ devotion, \ longing, \ heroism, \ peace", WHITE),
            (r"these associations are learned, \ like film's chromatic mediants \ (Part 31)", TUNE),
            (r"Part 46 asks how music carries emotion at all", GREY_A),
        ]
        rows_scene(self, r"time, \ season, \ mood", items,
                   "Ragas carry more than notes. <bookmark mark='b'/> The Hindustani tradition assigns them to times of day: "
                   "Bhairav at dawn, Yaman in the early evening, <bookmark mark='c'/> and some to seasons, the Malhar ragas to the "
                   "monsoon. <bookmark mark='d'/> Each carries a mood, a rasa: devotion, longing, heroism, peace. "
                   "<bookmark mark='e'/> These associations are learned within the tradition, like film's chromatic mediants in "
                   "Part 31. <bookmark mark='f'/> Part 46 asks how music carries emotion at all.", marks="cdef")

    # ------------------------------------------------------------------
    def bhupali(self):
        d = load("bhupali")
        c = clip("bhupali.phrase")
        rows_ = VGroup(VGroup(label(r"up:", font_size=18, color=GREY_A), sargam(d["aroha"], size=24, color=TUNE)).arrange(RIGHT, buff=0.3),
                       VGroup(label(r"down:", font_size=18, color=GREY_A), sargam(d["avaroha"], size=24, color=TUNE)).arrange(RIGHT, buff=0.3),
                       VGroup(label(r"phrase:", font_size=18, color=GREY_A), sargam(d["pakad"], size=24, color=TUNE)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.4)
        cap = label(r"five notes: \ S R G P D \ ---\ no Ma, \ no Ni; \ Ga is its vadi, \ the note it dwells on", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"raga Bhupali \ (phrases ours)", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A third raga, Bhupali, uses only five notes, Sa, Re, Ga, Pa and Dha, the pentatonic scale of Part 12: no Ma and "
            "no Ni at all. Its vadi, the note it dwells on, is Ga. Listen for how the phrases lean on Ga and come home through "
            "Re and the Dha below Sa."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Bhupali", kind="synthesized", detail=r"a bowed tone over the tanpura", corner=DL, tag_corner=DR)
            u = d["unit"]
            t = 0.3
            for i in range(len(d["aroha"])):
                pulse(snd, rows_[0][1][i], t, t + u - 0.03, buff=0.04)
                t += u if i < len(d["aroha"]) - 1 else 1.2
            for i in range(len(d["avaroha"])):
                pulse(snd, rows_[1][1][i], t, t + u - 0.03, buff=0.04)
                t += u if i < len(d["avaroha"]) - 1 else 1.2
            for i in range(len(d["pakad"])):
                pulse(snd, rows_[2][1][i], t, t + 0.47, buff=0.04)
                t += 0.5
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vadi(self):
        items = [
            (r"\textit{v\=ad\=\i}: \ the most important note; \ \textit{samv\=ad\=\i}: \ its partner, \ usually a fourth or fifth away", WHITE),
            (r"Yaman: \ v\=ad\=\i Ga, \ samv\=ad\=\i Ni \ (as commonly taught)", WHITE),
            (r"Bhupali: \ v\=ad\=\i Ga, \ samv\=ad\=\i Dha", WHITE),
            (r"a raga's centre of gravity: \ phrases return to these notes and rest on them", TUNE),
            (r"Part 15's key profiles measured the same idea for Western keys", GREY_A),
        ]
        rows_scene(self, r"the notes a raga leans on", items,
                   "Ragas lean on particular notes. <bookmark mark='b'/> The vadi is the most important note, and the samvadi its partner, usually a fourth or fifth away. <bookmark mark='c'/> In Yaman, as commonly taught, the vadi is Ga and the samvadi Ni. <bookmark mark='d'/> In Bhupali, Ga and Dha. <bookmark mark='e'/> They are the raga's centre of gravity: phrases return to them and rest there. <bookmark mark='f'/> Part 15’s Western key profiles offer an analogy, not an equivalence with vadi theory.", marks="cdef")
