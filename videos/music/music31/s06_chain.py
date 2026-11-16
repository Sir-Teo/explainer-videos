from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Chain(SoundScene):
    def construct(self):
        chapter(self, 5, r"The long chain", r"Can one pattern of moves visit every triad?", extra=((1824, r"Beethoven's Ninth"),))
        self.ninth()
        self.hear()
        self.quiz()
        self.all24()
        self.tours()
        self.proof()

    # ------------------------------------------------------------------
    def ninth(self):
        items = [
            (r"Beethoven, \ Symphony No. 9 \ (1824), \ second movement, \ the development", WHITE),
            (r"a passage of nineteen triads: \ C, \ a, \ F, \ d, \ B$\flat$, \ g, \ E$\flat$ ...", WHITE),
            (r"each a fifth or a third from the last: \ R, \ L, \ R, \ L ... \ (Cohn)", WHITE),
            (r"no key holds it: \ nineteen successive triads in Cohn’s reading", TUNE),
            (r"the full chain would visit all 24 before returning home", GREY_A),
        ]
        rows_scene(self, r"Beethoven's chain", items,
                   "A celebrated long chain comes from Beethoven. <bookmark mark='b'/> In the development of "
                   "the second movement of his Ninth Symphony, of 1824, <bookmark mark='c'/> Richard Cohn traces a passage of "
                   "nineteen triads, C major, A minor, F major, D minor, B flat, G minor, E flat and on, <bookmark mark='d'/> "
                   "each reached from the last by R or by L, alternately. <bookmark mark='e'/> No key holds it: it slides "
                   "through most of the triads there are. <bookmark mark='f'/> Continued, the chain would visit all twenty-four "
                   "before coming home.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("chain")
        c = clip("chain.nineteen")
        names = d["first"]
        row1 = VGroup(*[label(tex_triad(n), font_size=24, color=TUNE if not n.endswith("m") else BLUE) for n in names[:10]]).arrange(RIGHT, buff=0.35)
        row2 = VGroup(*[label(tex_triad(n), font_size=24, color=TUNE if not n.endswith("m") else BLUE) for n in names[10:]]).arrange(RIGHT, buff=0.35)
        cells = VGroup(row1, row2).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        flat = list(row1) + list(row2)
        head = label(r"the chain R, \ L, \ R, \ L ... \ from C: \ nineteen triads \ (our voicing)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"gold: \ major; \ blue: \ minor; \ every step keeps two notes", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Here are the nineteen chords as the chain gives them, in our own voicing on Part 7's piano, at a brisk pace. "
            "Listen to how smooth each step is, and how far the whole passage travels: it starts in C major and ends in A "
            "major, by way of keys with five and six flats and sharps."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"nineteen triads", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, m in enumerate(flat):
                pulse(snd, m, i * d["unit"], (i + 1) * d["unit"] - 0.03, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("keys")
        c = clip("keys.quiz")
        card = listen_card(r"Two chains of six chords from C major. \ One stays inside the key of C; \ "
                           r"one, \ by R and L alone, \ leaves it. \ Which stays home, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two chains of six chords, both starting from C major and moving smoothly. One stays "
            "inside the key of C; the other, made only of R and L moves, wanders out of it. Which one stays home, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = VGroup(*[label(tex_triad(n), font_size=30, color=GREY_A) for n in d["A"]]).arrange(RIGHT, buff=0.45).move_to(UP * 0.8)
        gb = VGroup(*[label(tex_triad(n), font_size=30, color=GREY_A) for n in d["B"]]).arrange(RIGHT, buff=0.45).move_to(DOWN * 1.0)
        la = label(r"A", font_size=34, color=GREY_A).next_to(ga, LEFT, buff=0.6)
        lb = label(r"B", font_size=34, color=GREY_A).next_to(gb, LEFT, buff=0.6)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(6):
                pulse(snd, ga[i], d["starts"]["A"] + i * d["unit"], d["starts"]["A"] + (i + 1) * d["unit"] - 0.05, buff=0.06)
                pulse(snd, gb[i], d["starts"]["B"] + i * d["unit"], d["starts"]["B"] + (i + 1) * d["unit"] - 0.05, buff=0.06)
        ans = VGroup(label(r"A: \ all in C major: \ I, \ vi, \ IV, \ ii, \ V, \ I", font_size=21, color=TUNE).next_to(ga, DOWN, buff=0.3),
                     label(r"B: \ B$\flat$ and G minor bring in B$\flat$: \ the key has moved", font_size=21, color=EAR).next_to(gb, DOWN, buff=0.3))
        with self.voiceover(
            'A stays home: C, A minor, F, D minor, G, C, every chord in C major. B starts the same way, but its fifth chord is B flat major, and B flat is not in C major; the chain is already on its way to the flat keys. Both can sound smooth; only A remains diatonic to C major. A chromatic chain can still have a tonal context.'
        ):
            self.play(FadeIn(ans), *[x.animate.set_color(TUNE) for x in ga])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def all24(self):
        d = load("chain")
        names = d["full"]
        n = len(names)
        R = 2.6
        dots = VGroup()
        for i, nm in enumerate(names):
            ang = np.pi / 2 - 2 * np.pi * i / n
            p = np.array([R * np.cos(ang), R * np.sin(ang) - 0.2, 0])
            dots.add(label(tex_triad(nm), font_size=17, color=TUNE if not nm.endswith("m") else BLUE).move_to(p))
        ring = Circle(radius=R, color=GREY_B, stroke_width=1).move_to(DOWN * 0.2)
        head = label(r"R, \ L, \ R, \ L ...: \ all 24 triads, \ then C again", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Continued, the chain visits every one of the twenty-four triads exactly once before returning to C major: a "
            "single loop through the whole space, alternating major and minor. On the Tonnetz it runs in a straight band "
            "across the torus. Beethoven's passage walks most of the way round."
        ):
            self.play(FadeIn(head), FadeIn(ring), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.08), run_time=4.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tours(self):
        d = load("hamilton")
        c = clip("hamilton.tour")
        names = d["chain"]
        row1 = VGroup(*[label(tex_triad(n), font_size=22, color=TUNE if not n.endswith("m") else BLUE) for n in names[:13]]).arrange(RIGHT, buff=0.3)
        row2 = VGroup(*[label(tex_triad(n), font_size=22, color=TUNE if not n.endswith("m") else BLUE) for n in names[13:]]).arrange(RIGHT, buff=0.3)
        cells = VGroup(row1, row2).arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        flat = [*row1, *row2]
        head = label(rf"tours of all 24 triads, \ each once: \ {d['count']} of them", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        mv = d["moves"]
        cap = label(rf"this one: \ {mv['P']} P, \ {mv['L']} L, \ {mv['R']} R; \ the R--L chain is the only tour with no P at all", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "The R L chain is one way to visit every triad once and come home. Are there others? A program can try every "
            f"route on the graph of moves: there are exactly {say(d['count'])} such tours, counting each once whatever its "
            "starting point or direction. Only one of them, the R L chain, uses no P at all. Here is another, which leans on "
            "P: major to minor and back, on and on, with L and R to change family. Twenty-four chords, each once."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a tour of all 24", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(len(flat)):
                pulse(snd, flat[i], i * d["unit"], (i + 1) * d["unit"] - 0.05, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        items = [
            (r"R then L from C major: \ C to a minor to F major", WHITE),
            (r"so each R--L pair moves a major triad down a fifth: \ the pair acts like the transposition $T_5$", WHITE),
            (r"twelve pairs pass through all twelve major triads before C returns", WHITE),
            (r"and the R in each pair stops on a minor triad: \ twelve more, \ all different", TUNE),
            (r"24 chords, \ each once: \ the order of LR is 12, \ as chapter two's group predicts", GREY_A),
        ]
        rows_scene(self, r"why the chain visits all 24", items,
                   "Why must the chain visit every triad? <bookmark mark='b'/> Take R then L from C major: C, A minor, F major. <bookmark mark='c'/> Each R L pair moves a major triad down a fifth; the pair acts like a transposition. <bookmark mark='d'/> Down a fifth twelve times passes through all twelve major triads before C comes back, <bookmark mark='e'/> and the R inside each pair stops on a minor triad, the relative minor, twelve more, all different. <bookmark mark='f'/> Twenty-four chords, each once: the order of L R is twelve, as the group in chapter two predicts.", marks="cdef")
