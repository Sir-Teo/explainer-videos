from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403

KEYS = ["g5", "g7", "g8", "g9"]


class Bartok(SoundScene):
    def construct(self):
        chapter(self, 6, r"Bartók: \ fieldwork, \ symmetry, \ proportion", r"Did Bartók compose with the golden section?", extra=((1906, r"Bartók and Kodály's first collecting"),))
        self.fieldwork()
        self.additive()
        self.counts()
        self.axes()
        self.golden()
        self.null()

    # ------------------------------------------------------------------
    def fieldwork(self):
        items = [
            (r"Béla Bartók and Zoltán Kodály, \ from 1906: \ peasant songs recorded on phonograph cylinders", WHITE),
            (r"Hungarian, \ Slovak, \ Romanian, \ later Turkish and Arab music: \ thousands of melodies transcribed", WHITE),
            (r"the old modes, \ pentatonic tunes, \ and rhythms in groups of 2 and 3", WHITE),
            (r"not quotation but a language, \ learned like a mother tongue", TUNE),
            (r"Bartók died in 1945; \ much of his music is still in copyright in some countries", GREY_A),
        ]
        rows_scene(self, r"music from the villages", items,
                   "In Hungary the new materials came from fieldwork. <bookmark mark='b'/> From 1906 Béla Bartók and Zoltán Kodály travelled through villages recording peasant songs on phonograph cylinders, <bookmark mark='c'/> Hungarian, Slovak and Romanian at first, later Turkish and Arab, and Bartók transcribed thousands of melodies. <bookmark mark='d'/> He found old modes, pentatonic tunes, and dances whose beats come in uneven groups of two and three pulses. <bookmark mark='e'/> His aim, he wrote, was not to quote these tunes but to absorb them until they became a composer's mother tongue. <bookmark mark='f'/> The examples here are original sketches of the stated procedures.", marks="cdef")

    # ------------------------------------------------------------------
    def additive(self):
        d = load("bartok")
        c = clip("bartok.four")
        rows_ = VGroup()
        for g in d["groupings"]:
            cells = VGroup()
            for n in g:
                grp = VGroup(*[Square(side_length=0.36, stroke_width=1.5, stroke_color=GREY_B, fill_color=TUNE if j == 0 else GREY_B, fill_opacity=0.85 if j == 0 else 0.25) for j in range(n)]).arrange(RIGHT, buff=0.05)
                cells.add(grp)
            cells.arrange(RIGHT, buff=0.22)
            name = label(r" + ".join(str(n) for n in g) + rf" \ = \ {sum(g)}", font_size=22, color=GREY_A)
            rows_.add(VGroup(name, cells).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"additive rhythm: \ quick pulses grouped in 2s and 3s \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here are such rhythms, on Part 9's drums. The quick pulse never changes; what changes is how the pulses are "
            "grouped, a low drum on the first pulse of each group. Two plus three, five. Two plus two plus three, seven. "
            "Three plus three plus two, eight pulses that do not fall into fours. And two plus two plus two plus three, "
            "nine. Bartók called these Bulgarian rhythms, after the dances where he heard them."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"5, \ 7, \ 8, \ 9", detail=r"Part 9's drums", corner=DL, tag_corner=DR)
            for i, k in enumerate(KEYS):
                st = d["starts"][k]
                end = d["starts"][KEYS[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("bartok")
        ks = list(range(4, 15))
        bars = columns([d["counts"][str(k)] for k in ks], [str(k) for k in ks], width=7.4, height=2.8, color=TUNE, fmt="{:.0f}", font_size=17)
        bars.move_to(LEFT * 2.0 + DOWN * 0.4)
        t = label(r"ways to group n pulses into 2s and 3s", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"7 pulses: \ 3 ways", WHITE), (r"12 pulses: \ 12 ways", WHITE),
            (r"each count: \ the counts 2 and 3 places back, \ added", TUNE), (r"a Padovan sequence", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.move_to(RIGHT * 4.4 + DOWN * 0.2)
        with self.voiceover(
            "How many such rhythms are there? Count the ways to fill n pulses with groups of two and three. "
            f"<bookmark mark='a'/> Seven pulses can be grouped {say(d['counts']['7'])} ways: two two three, two three two, "
            f"three two two. <bookmark mark='b'/> Twelve pulses, {say(d['counts']['12'])} ways. <bookmark mark='c'/> Each "
            "count is the sum of the counts two and three places back, because a grouping of n pulses ends with a group "
            "of two or a group of three. <bookmark mark='d'/> Mathematicians call these the Padovan numbers; a dancer just "
            "calls them the dances."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def golden(self):
        items = [
            (r"Ernő Lendvai \ (from the 1950s): \ Bartók built his forms on the golden section and the Fibonacci numbers", WHITE),
            (r"his showpiece: \ \textit{Music for Strings, \ Percussion and Celesta} \ (1936), \ first movement", WHITE),
            (r"89 bars, \ a Fibonacci number, \ the climax at 55, \ another", WHITE),
            (r"Roy Howat \ (1983) \ and others: \ the score has 88 bars, \ and the counting of events is flexible", TUNE),
            (r"Bartók left no word that he used the golden section", GREY_A),
        ]
        rows_scene(self, r"the golden section, \ claimed", items,
                   "Bartók's music also became the centre of a numerical claim. <bookmark mark='b'/> The Hungarian analyst Ernő "
                   "Lendvai argued, from the 1950s on, that Bartók built his forms on the golden section and the Fibonacci "
                   "numbers. <bookmark mark='c'/> His showpiece was the first movement of the Music for Strings, Percussion and "
                   "Celesta, of 1936: <bookmark mark='d'/> eighty-nine bars, a Fibonacci number, with the climax at bar "
                   "fifty-five, another. <bookmark mark='e'/> Critics, Roy Howat among them, pointed out that the score has "
                   "eighty-eight bars, and that which events count as landmarks is flexible. <bookmark mark='f'/> Bartók himself "
                   "left no word that he used the golden section at all. Part 21 asked the same question of other music; here "
                   "is the null model.", marks="cdef")

    # ------------------------------------------------------------------
    def null(self):
        d = load("bartok")["golden"]
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 1, 0.25], x_length=7.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to(LEFT * 2.0 + DOWN * 0.3)
        c1 = ax.plot_line_graph([m for m, _ in d["curve"]], [p for _, p in d["curve"]], line_color=TUNE, add_vertex_dots=False, stroke_width=4)
        c2 = ax.plot_line_graph([m for m, _ in d["curve2"]], [p for _, p in d["curve2"]], line_color=EAR, add_vertex_dots=False, stroke_width=4)
        xl = label(r"landmarks an analyst might pick \ (climaxes, \ entries, \ changes of texture)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"chance at least one lands near a golden point", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.2).shift(RIGHT * 1.6)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"88 bars, \ within 1 bar: \ one landmark {100 * d['p1']:.1f} in 100", TUNE),
            (rf"five landmarks: \ {100 * d['p5']:.0f} in 100", TUNE),
            (rf"within 2 bars, \ ten landmarks: \ {100 * d['p10_2']:.0f} in 100", EAR),
            (r"a claim needs its landmarks fixed in advance", WHITE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6))
        side.move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "Suppose events fall at random bars in an eighty-eight-bar movement. How often does one of them land within a "
            "bar of a golden point, at 0.382 or 0.618 of the way through? <bookmark mark='a'/> For a single, pre-chosen "
            f"landmark, about {say(100 * d['p1'], 1)} times in a hundred: rare. <bookmark mark='b'/> But an analyst "
            "can choose among many landmarks, climaxes, entries, changes of texture. With five to choose from, the chance is "
            f"{say(round(100 * d['p5']))} in a hundred. <bookmark mark='c'/> Allow two bars either way and ten landmarks, and "
            f"it is {say(round(100 * d['p10_2']))} in a hundred: more likely than not. <bookmark mark='d'/> A golden-section "
            "claim is stronger evidence when landmarks and tolerances are specified independently, or when selection and multiple testing are modeled explicitly."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(c1))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def axes(self):
        items = [
            (r"Lendvai's `axis system': \ keys a minor third apart treated as one function", WHITE),
            (r"tonic axis: \ C, \ E$\flat$, \ F$\sharp$, \ A \ (a diminished seventh, \ the octatonic's triads)", WHITE),
            (r"dominant axis: \ G, \ B$\flat$, \ C$\sharp$, \ E; \ subdominant axis: \ F, \ A$\flat$, \ B, \ D", WHITE),
            (r"a key's opposite pole, \ a tritone away, \ substitutes for it", TUNE),
            (r"a symmetric map of keys: \ disputed, \ but it names something real in the music", GREY_A),
        ]
        rows_scene(self, r"Bartók's axes", items,
                   "Lendvai also proposed a symmetric map of keys. <bookmark mark='b'/> In his axis system, keys a minor third apart do the same job. <bookmark mark='c'/> The tonic axis is C, E flat, F sharp and A, the four triads chapter four found inside one octatonic scale; <bookmark mark='d'/> the dominant axis is G, B flat, C sharp and E, and the subdominant F, A flat, B and D. <bookmark mark='e'/> A key's opposite pole, a tritone away, can stand in for it. <bookmark mark='f'/> Like the golden section, the system is disputed, but it names something real: Bartók's keys do move by minor thirds and tritones.", marks="cdef")
