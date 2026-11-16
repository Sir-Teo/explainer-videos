from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Ombak(SoundScene):
    def construct(self):
        chapter(self, 8, r"Tuned apart on purpose", r"Why would an orchestra tune out of unison?")
        self.idea()
        self.quiz()
        self.rates()
        self.design()
        self.west()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"Balinese gamelan instruments come in pairs: \ \textit{pengumbang} \ and \textit{pengisep}", WHITE),
            (r"the pair is tuned slightly apart, \ so every note beats: \ \textit{ombak}, \ `wave'", WHITE),
            (r"the beating gives the ensemble its shimmer", WHITE),
            (r"Part 5: \ two tones close in pitch beat at their difference frequency", TUNE),
            (r"regulated beating is prominent here; \ intentional detuning also exists elsewhere", GREY_A),
        ]
        rows_scene(self, r"ombak", items,
                   "In many Balinese gamelan types, particular instruments are built in detuned pairs. <bookmark mark='b'/> The two members, pengumbang and pengisep, are tuned slightly apart, so every note they play together beats: ombak, the wave. <bookmark mark='c'/> The beating gives the whole ensemble its shimmer. <bookmark mark='d'/> It is Part 5's physics: two tones close in pitch beat at their difference frequency. <bookmark mark='e'/> European ensembles also use vibrato and intentional detuning; these Balinese pairs make a deliberately regulated beating texture especially prominent.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("ombak")
        c = clip("ombak.quiz")
        card = listen_card(r"Three notes in three octaves, \ each on two metallophones together. \ "
                           r"In one version the pair is tuned exactly together; \ in the other, \ apart. \ Which shimmers, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three notes, in three octaves, each played on two metallophones at once. In one version "
            "the two are tuned exactly together; in the other, apart. Which shimmers, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup(label(r"A", font_size=44, color=GREY_A), label(r"B", font_size=44, color=GREY_A)).arrange(RIGHT, buff=4.0).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.12)
            pulse(snd, cells[1], d["starts"]["B"], c.duration, buff=0.12)
        offs = r", \ ".join(f"{x:.0f}" for x in d["cents_off"])
        ans = VGroup(label(r"B: \ the second instrument 6 Hz higher at every pitch", font_size=21, color=TUNE),
                     label(rf"in cents: \ {offs} \ ---\ the same beat needs less detuning as pitch rises", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            f"B shimmers. Its second instrument is tuned six hertz higher at every pitch, so every note beats six times a second. In cents, that is {say(round(d['cents_off'][0]))} at the low note, {say(round(d['cents_off'][1]))} in the middle and {say(round(d['cents_off'][2]))} at the top: this demonstration keeps a constant beat rate rather than constant cents; real tuning practices and rate profiles vary."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        items = [
            (r"measured gamelans show beat rates of a few hertz to about eight, \ fairly even across the range", WHITE),
            (r"different villages and styles prefer faster or slower shimmer", WHITE),
            (r"a designed property: \ the tuner sets a rate, \ and derives every pair's detuning from it", WHITE),
            (r"Part 6's tuning by beats, \ used to make beats", TUNE),
            (r"the gamelan sound is in the space between two instruments", GREY_A),
        ]
        rows_scene(self, r"a beat by design", items,
                   "The shimmer is designed. <bookmark mark='b'/> Measured Balinese gamelans show beat rates from a few hertz to "
                   "about eight, fairly even across the range, <bookmark mark='c'/> and different villages and styles prefer "
                   "faster or slower shimmer. <bookmark mark='d'/> The tuner chooses a rate and derives every pair's detuning from "
                   "it: <bookmark mark='e'/> Part 6's tuning by beats, used to make beats instead of removing them. "
                   "<bookmark mark='f'/> The gamelan's sound lives in the space between two instruments.", marks="cdef")

    # ------------------------------------------------------------------
    def rates(self):
        d = load("rates")
        c = clip("rates.two")
        cells = VGroup(label(r"3 beats a second", font_size=24, color=TUNE), label(r"8 beats a second", font_size=24, color=EAR)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"slow shimmer, \ fast shimmer", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'The beat rate is a choice. Here are two notes on paired metallophones, first tuned to beat three times a second, a slow, wide wave, then eight times a second, a fast shimmer close to roughness. Different Balinese styles prefer different rates.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"3 Hz, \ then 8 Hz", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            ks = ['slow', 'fast']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def west(self):
        items = [
            (r"Paris, \ 1889: \ Debussy heard a Javanese gamelan at the World Exhibition", WHITE),
            (r"Colin McPhee lived in Bali in the 1930s and transcribed its music", WHITE),
            (r"Britten, \ Messiaen, \ Steve Reich and Lou Harrison drew on gamelan in different ways", WHITE),
            (r"Harrison built American gamelans, \ tuned by his own ratios", TUNE),
            (r"influence ran both ways: \ Balinese composers write new music for gamelan today", GREY_A),
        ]
        rows_scene(self, r"gamelan and the West", items,
                   "Gamelan has fascinated Western musicians. <bookmark mark='b'/> In Paris in 1889 Debussy heard a Javanese gamelan at the World Exhibition. <bookmark mark='c'/> Colin McPhee lived in Bali in the 1930s and transcribed its music. <bookmark mark='d'/> Britten, Messiaen, Steve Reich and Lou Harrison drew on gamelan in different ways, <bookmark mark='e'/> and Harrison built American gamelans tuned to ratios of his own choosing. <bookmark mark='f'/> Influence runs both ways: Balinese and Javanese composers write new music for gamelan today.", marks="cdef")
