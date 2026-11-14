from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Oddity(SoundScene):
    def construct(self):
        chapter(self, 4, r"Oddity and homometry", r"Can a rhythm refuse to be cut in half?", extra=((1991, r"Arom, \textit{African Polyphony}"),))
        self.arom()
        self.count()
        self.quiz()
        self.meaning()
        self.both()

    # ------------------------------------------------------------------
    def arom(self):
        d = load("oddity")
        g1 = necklace("x.x.x..x.x..", radius=1.3, color=TUNE).move_to(LEFT * 3.2 + UP * 0.1)
        g2 = necklace("x.x.xx.x.x.x", radius=1.3, color=EAR).move_to(RIGHT * 3.2 + UP * 0.1)
        cut = DashedLine(g2[0].get_top() + UP * 0.2, g2[0].get_bottom() + DOWN * 0.2, color=WHITE, stroke_width=2).rotate(-2 * TAU / 12, about_point=g2[0].get_center())
        caps = VGroup(label(r"E(5, 12): \ no stroke has a partner opposite: \ odd", font_size=20, color=TUNE).next_to(g1, DOWN, buff=0.4),
                      label(r"E(7, 12): \ strokes facing each other: \ not odd", font_size=20, color=EAR).next_to(g2, DOWN, buff=0.4))
        head = label(r"Arom's rhythmic oddity", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The ethnomusicologist Simha Arom noticed something about the rhythms of the Aka people of Central Africa: no "
            "two strokes are ever exactly half a cycle apart. The necklace cannot be cut into two equal halves that start on "
            "strokes. He called it rhythmic oddity. <bookmark mark='a'/> The five-stroke Euclidean rhythm in twelve has it. "
            "<bookmark mark='b'/> The seven-stroke bell pattern cannot: seven strokes in twelve pulses must include two "
            "opposite each other, because there are only six opposite pairs of places, a pigeonhole argument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(caps[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("oddity")
        cells = VGroup()
        for n in ("8", "12", "16"):
            row = d["counts"][n]
            ks = sorted(row, key=int)
            b = columns([row[k] for k in ks], ks, width=3.4, height=2.0, color=TUNE, fmt="{:.0f}", font_size=14)
            cells.add(VGroup(label(rf"{n} pulses", font_size=20, color=WHITE), b, label(r"strokes", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.8).move_to(DOWN * 0.2)
        head = label(r"odd rhythms, \ counted \ (up to rotation)", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"never more than half the pulses: \ above that, \ some pair must face each other", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A program can count the odd rhythms, treating rotations as the same rhythm. For twelve pulses there are twenty "
            "with four strokes, sixteen with five, six with six, and none with seven or more. For sixteen pulses the count "
            "peaks at five and six strokes. Above half the pulses there are none at all, by the same pigeonhole. Chemillier "
            "and Truchet later enumerated the Aka patterns' relatives this way, as words with the oddity property."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("oddity")
        c = clip("oddity.quiz")
        card = listen_card(r"Two rhythms of four strokes in eight pulses. \ Neither is a rotation or a mirror image of the other. \ "
                           r"Do they contain the same intervals between their strokes? \ Listen, \ then decide.", width=10.4)
        with self.voiceover(
            "A question for your ears. Two rhythms, four strokes in eight pulses each. Neither is a rotation or a mirror image "
            "of the other. Do they contain the same intervals between their strokes, or different ones?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = necklace(d["patterns"][0], radius=1.3, color=GREY_A).move_to(LEFT * 3.2 + UP * 0.2)
        gb = necklace(d["patterns"][1], radius=1.3, color=GREY_A).move_to(RIGHT * 3.2 + UP * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 11's clave", corner=DL, tag_corner=DR)
            for key, g, pt in (("A", ga, d["patterns"][0]), ("B", gb, d["patterns"][1])):
                ons = [i for i, ch in enumerate(pt) if ch == "x"]
                for cc in range(3):
                    for j, o in enumerate(ons):
                        t0 = d["starts"][key] + (cc * 8 + o) * 0.17
                        pulse(snd, g.dots[j], t0, t0 + 0.15, buff=0.04)
        iv = d["content"]
        ans = label(rf"both: \ {iv[0]} pairs a pulse apart, \ {iv[1]} two apart, \ {iv[2]} three apart, \ {iv[3]} four apart", font_size=21, color=TUNE).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "They do. Both have two pairs of strokes one pulse apart, one pair two apart, two pairs three apart and one pair "
            "four apart. Rhythms like these are called homometric, the word Part 29 borrowed from crystallography for chords. "
            "They sound different, yet every interval between strokes is shared. Among rhythms of four strokes in eight "
            "pulses this is the only such pair; among six strokes in twelve there are fifteen."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"oddity: \ a timeline that never divides into equal halves keeps the listener oriented", WHITE),
            (r"Arom's reading: \ the asymmetry tells players where they are in a long cycle", WHITE),
            (r"homometry: \ interval content does not determine a rhythm", WHITE),
            (r"the patterns are the music of particular people; \ the mathematics only describes them", TUNE),
            (r"Part 37 returns to timelines in their own musical worlds", GREY_A),
        ]
        rows_scene(self, r"what the properties mean", items,
                   "What do these properties mean in music? <bookmark mark='b'/> A timeline that never splits into equal halves "
                   "never sounds the same at two points of its cycle. <bookmark mark='c'/> Arom read this as a way for players to "
                   "keep their place in a long cycle. <bookmark mark='d'/> Homometry says that the intervals alone do not fix a "
                   "rhythm. <bookmark mark='e'/> And the patterns belong to particular people and traditions; the mathematics "
                   "describes them, it does not explain why they were chosen. <bookmark mark='f'/> Part 37 returns to timelines "
                   "in their own musical worlds.", marks="cdef")

    # ------------------------------------------------------------------
    def both(self):
        items = [
            (r"E(5, 12) is both maximally even and odd", WHITE),
            (r"E(7, 12) is maximally even but cannot be odd", WHITE),
            (r"Arom's Aka timelines live in longer cycles, \ where both can hold", WHITE),
            (r"Toussaint measured many timelines on both properties at once", TUNE),
            (r"two simple properties, \ and a large share of the world's timelines satisfy them", GREY_A),
        ]
        rows_scene(self, r"evenness and oddity together", items,
                   "The two properties can be combined. <bookmark mark='b'/> E of five, twelve is both maximally even and odd. <bookmark mark='c'/> E of seven, twelve is maximally even but cannot be odd. <bookmark mark='d'/> Arom's Aka timelines live in longer cycles, where both properties can hold at once. <bookmark mark='e'/> Toussaint measured many of the world's timelines on both. <bookmark mark='f'/> Two simple properties, and a large share of traditional timelines satisfy them.", marks="cdef")
