from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


def clock(pcs, radius=1.3, color=TUNE, label_size=18, labels=True):
    """Twelve pitch classes round a circle, the set's members filled."""
    g = VGroup()
    ring = Circle(radius=radius, color=GREY_B, stroke_width=2)
    g.add(ring)
    dots = VGroup()
    for k in range(12):
        ang = np.pi / 2 - 2 * np.pi * k / 12
        pos = np.array([radius * np.cos(ang), radius * np.sin(ang), 0])
        on = k in pcs
        dots.add(Dot(pos, radius=0.12 if on else 0.06, color=color if on else GREY_B))
        if labels:
            g.add(label(LETTER[k], font_size=label_size, color=GREY_A if on else GREY_B).move_to(pos * 1.28))
    poly = Polygon(*[dots[k].get_center() for k in sorted(pcs)], color=color, stroke_width=2, fill_opacity=0.12) if len(pcs) >= 3 else VGroup()
    g.add(poly, dots)
    g.dots = dots
    return g


class Wholetone(SoundScene):
    def construct(self):
        chapter(self, 1, r"A scale without a home", r"What happens when every step is the same size?", extra=((1910, r"Debussy's \textit{Voiles} published"),))
        self.symmetry()
        self.quiz()
        self.debussy()
        self.scriabin()
        self.pentatonic()
        self.micro()
        self.slendro()

    # ------------------------------------------------------------------
    def symmetry(self):
        d = load("wholetone")
        maj = clock([0, 2, 4, 5, 7, 9, 11], color=BLUE).move_to(LEFT * 3.4 + DOWN * 0.2)
        wt = clock([0, 2, 4, 6, 8, 10], color=TUNE).move_to(RIGHT * 3.4 + DOWN * 0.2)
        lm = label(r"C major: \ two sizes of step, \ 12 different transpositions", font_size=21, color=BLUE).next_to(maj, DOWN, buff=0.5)
        lw = label(rf"whole-tone: \ one size of step, \ only {d['periods']['whole']} different transpositions", font_size=21, color=TUNE).next_to(wt, DOWN, buff=0.5)
        head = label(r"the twelve pitch classes round a clock \ (Part 12)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Put the twelve pitch classes round a clock, as Part 12 did. The major scale uses two sizes of step, whole and half, and that unevenness distinguishes its scale positions, though it does not alone choose a tonic among modes: each of its twelve transpositions is a different set of notes, and context helps listeners interpret the half steps and establish a tonic. <bookmark mark='a'/> The whole-tone scale uses one size of step only. Turn it by a whole step and it lands on itself; there are only two different whole-tone scales in all. <bookmark mark='b'/> Every note is in the same position as every other: no half steps, no diatonic leading tone or built-in unique tonic; a bass pedal and other context can still establish a center."
        ) as vo:
            self.play(FadeIn(head), FadeIn(maj), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(wt), FadeIn(lw))
            vo.wait_until("b")
            self.play(Rotate(wt[-2:], angle=-2 * np.pi / 6, about_point=wt[0].get_center()), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("wholetone")
        c = clip("wholetone.two")
        card = listen_card(r"The Tune's first phrase twice: \ once in C major, \ once with every degree moved onto the whole-tone scale. \ "
                           r"Which has no half steps at all, \ A or B?", width=10.4)
        with self.voiceover(
            "Hear the difference. The Tune's first phrase twice: once in C major, and once with each degree of the scale "
            "moved onto the same degree of the whole-tone scale. Which version has no half steps at all, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = mroll(d["major"], width=5.0, height=2.0, lo=70, hi=88, color=GREY_A).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = mroll(d["whole"], width=5.0, height=2.0, lo=70, hi=88, color=GREY_A).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, gA.notes, [d["starts"]["major"] + n[1] * d["unit"] for n in d["major"]], hot=WHITE, base=GREY_A)
            flash(snd, gB.notes, [d["starts"]["whole"] + n[1] * d["unit"] for n in d["whole"]], hot=WHITE, base=GREY_A)
            pulse(snd, la, d["starts"]["major"], d["starts"]["whole"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["whole"], c.duration, buff=0.1)
        ans = VGroup(label(r"A: \ C major, \ ends at home", font_size=22, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ whole-tone, \ G$\sharp$ and A$\sharp$ in place of G and A", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is whole-tone. The leap that was a perfect fifth, C up to G, becomes C up to G sharp, an augmented fifth, and "
            "the phrase no longer sounds as if it is going anywhere. It floats."
        ):
            self.play(FadeIn(ans), gA.animate.set_color(BLUE), gB.animate.set_color(TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debussy(self):
        items = [
            (r"Debussy, \ \textit{Voiles} \ (`Veils' or `Sails'), \ Preludes Book I \ (1910)", WHITE),
            (r"almost all of it on one whole-tone scale, \ over a held B$\flat$ in the bass", WHITE),
            (r"a short middle section on the pentatonic black keys", WHITE),
            (r"the pedal note gives the ear somewhere to stand when the scale gives it nowhere", TUNE),
            (r"the scale had been heard before \ (Glinka, \ Liszt); \ Debussy made a whole piece of it", GREY_A),
        ]
        rows_scene(self, r"a piece without a home", items,
                   "Debussy built a whole piece on the idea. <bookmark mark='b'/> Voiles, which can mean veils or sails, is "
                   "from his first book of Preludes, published in 1910. <bookmark mark='c'/> Almost all of it uses a single "
                   "whole-tone scale, over a B flat held in the bass, <bookmark mark='d'/> with a short middle section on the "
                   "five black keys, a pentatonic scale. <bookmark mark='e'/> The held bass note gives the ear somewhere to "
                   "stand when the scale gives it nowhere. <bookmark mark='f'/> The scale was not new, Glinka and Liszt had "
                   "used it for magic and menace, but Debussy made a whole piece of it.", marks="cdef")

    # ------------------------------------------------------------------
    def pentatonic(self):
        items = [
            (r"the pentatonic \ (Part 12): \ five notes, \ no half steps, \ in music on every continent", WHITE),
            (r"Debussy and Ravel use it for the exotic and the pastoral", WHITE),
            (r"slendro, \ the gamelan's five-note tuning, \ is close to equal steps, \ not to the piano's pentatonic", WHITE),
            (r"the piano could only approximate it: \ the gamelan was heard through the black keys", TUNE),
            (r"Act VI hears these musics on their own terms", GREY_A),
        ]
        rows_scene(self, r"five notes, \ heard through a piano", items,
                   "The black keys hold the other scale Paris heard. <bookmark mark='b'/> The pentatonic, five notes with no "
                   "half steps, which Part 12 found in music on every continent, <bookmark mark='c'/> became in Debussy and "
                   "Ravel a colour for the exotic and the pastoral. <bookmark mark='d'/> But slendro, the gamelan's five-note "
                   "tuning, is closer to five equal steps than to the piano's pentatonic, <bookmark mark='e'/> so the piano "
                   "could only approximate what Debussy heard: this black-key approximation is one compositional response, not an equivalence with gamelan tuning. "
                   "<bookmark mark='f'/> Act VI hears these musics on their own terms.", marks="cdef")

    # ------------------------------------------------------------------
    def slendro(self):
        d = load("slendro")
        c = clip("slendro.two")
        gA = mroll(d["slendro"], width=5.2, height=2.0, lo=58, hi=76, color=TUNE, bar_h=0.12).move_to(LEFT * 3.3 + DOWN * 0.1)
        gB = mroll(d["piano"], width=5.2, height=2.0, lo=58, hi=76, color=BLUE, bar_h=0.12).move_to(RIGHT * 3.3 + DOWN * 0.1)
        lA = label(r"five equal steps: \ 0, \ 240, \ 480, \ 720, \ 960 cents", font_size=20, color=TUNE).next_to(gA, UP, buff=0.3)
        lB = label(r"the black keys: \ 0, \ 200, \ 400, \ 700, \ 900 cents", font_size=20, color=BLUE).next_to(gB, UP, buff=0.3)
        cap = label(r"the differences: \ 0, \ 40, \ 80, \ 20, \ 60 cents: \ up to most of a semitone", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Hear how far the approximation is. The hook's core melody twice: first on bars tuned to five equal steps of two "
            "hundred and forty cents, then moved degree for degree onto the piano's black keys, whose steps are two hundred "
            "and three hundred cents. The two scales differ by up to eighty cents, most of a semitone, on the third degree. "
            "The tune is recognizably the same; its colour is not."
        ):
            self.play(FadeIn(gA), FadeIn(gB), FadeIn(lA), FadeIn(lB), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"equal steps, \ then the black keys", detail=r"Part 9's bars; \ Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, gA.notes, [d["starts"]["slendro"] + n[1] * d["beat"] for n in d["slendro"]], hot=WHITE, base=TUNE)
            flash(snd, gB.notes, [d["starts"]["piano"] + n[1] * d["beat"] for n in d["piano"]], hot=WHITE, base=BLUE)
            pulse(snd, lA, d["starts"]["slendro"], d["starts"]["piano"] - 0.5, buff=0.08)
            pulse(snd, lB, d["starts"]["piano"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scriabin(self):
        items = [
            (r"Alexander Scriabin, \ \textit{Prometheus} \ (1910): \ one six-note chord as the source of everything", WHITE),
            (r"C, \ F$\sharp$, \ B$\flat$, \ E, \ A, \ D: \ fourths of different sizes, \ stacked", WHITE),
            (r"five of its six notes lie in one whole-tone scale", WHITE),
            (r"a part for a `colour organ' that bathes the hall in light", TUNE),
            (r"like Debussy, \ a harmony that floats, \ reached by a different road", GREY_A),
        ]
        rows_scene(self, r"Scriabin's mystic chord", items,
                   "In Moscow, Alexander Scriabin took the same idea further. <bookmark mark='b'/> His Prometheus, of 1910, grows from a single six-note chord, <bookmark mark='c'/> C, F sharp, B flat, E, A and D, a stack of fourths of different sizes. <bookmark mark='d'/> Five of its six notes lie in one whole-tone scale; only the A does not. <bookmark mark='e'/> The score even has a part for a colour organ, meant to bathe the hall in light. <bookmark mark='f'/> Like Debussy's, it is a harmony that floats, reached by a different road.", marks="cdef")

    # ------------------------------------------------------------------
    def micro(self):
        items = [
            (r"Ferruccio Busoni \ (1907): \ why only twelve? \ a call for thirds and sixths of a tone", WHITE),
            (r"Alois Hába in Prague: \ quarter-tone pianos and an opera \ (1931)", WHITE),
            (r"Julián Carrillo in Mexico: \ `Sonido 13', \ pianos tuned in sixteenths of a tone", WHITE),
            (r"the twelve-note equal octave of Part 6 was a choice, \ not a law", TUNE),
            (r"Part 33 asks which divisions of the octave are good, \ and why", GREY_A),
        ]
        rows_scene(self, r"smaller steps", items,
                   "Some composers went beyond the piano's twelve notes. <bookmark mark='b'/> In 1907 Ferruccio Busoni asked why the octave should have only twelve, and imagined thirds and sixths of a tone. <bookmark mark='c'/> In Prague, Alois Hába built quarter-tone pianos and wrote a quarter-tone opera. <bookmark mark='d'/> In Mexico, Julián Carrillo's Sonido Trece divided the whole step into as many as sixteen parts. <bookmark mark='e'/> The twelve-note equal octave of Part 6 was a choice, not a law. <bookmark mark='f'/> Part 33 asks which divisions of the octave are good, and why.", marks="cdef")
