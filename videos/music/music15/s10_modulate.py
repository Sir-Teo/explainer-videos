from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Modulate(SoundScene):
    def construct(self):
        chapter(self, 9, r"Leaving home", r"How does music change key?")
        self.how()
        self.pivots()
        self.quiz()
        self.reading()

    # ------------------------------------------------------------------
    def how(self):
        scales = VGroup(label(r"C major: \quad C \ D \ E \ F \ G \ A \ B", font_size=32, color=WHITE), label(r"G major: \quad G \ A \ B \ C \ D \ E \ F$\sharp$", font_size=32, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(UP, buff=0.5)
        row = VGroup(label(r"in C major:", font_size=28, color=GREY_A), label(r"D, \ F$\sharp$, \ A, \ C", font_size=40, color=EAR), label(r"$\rightarrow$", font_size=40, color=WHITE), label(r"G, \ B, \ D", font_size=40, color=TUNE)).arrange(RIGHT, buff=0.4).move_to(UP * 0.7)
        l1 = label(r"the dominant seventh of G: \ it holds F$\sharp$, \ which is not in C major", font_size=26, color=EAR).next_to(row, DOWN, buff=0.35)
        piv = VGroup(label(r"A, \ C, \ E", font_size=40, color=BLUE), label(r"vi in C major \ = \ ii in G major", font_size=30, color=WHITE)).arrange(RIGHT, buff=0.7).move_to(DOWN * 1.5)
        l2 = label(r"a pivot chord: \ one chord, \ a job in each key", font_size=26, color=BLUE).next_to(piv, DOWN, buff=0.3)
        with self.voiceover(
            "A piece of music does not have to stay in one key. Getting to another takes one new note. "
            "G major differs from C major by a single note, F sharp. <bookmark mark='a'/> Play the "
            "dominant seventh of G, which contains that F sharp and the tritone that goes with it, and "
            "the ear is pulled toward G as it was pulled toward C: this is a dominant of the dominant. "
            "<bookmark mark='b'/> To make the move smooth, composers approach it through a chord that "
            "belongs to both keys. A, C, E is the chord on six in C major, and the chord on two in G "
            "major: a predominant there. It is called a pivot. The listener hears it in the old key; "
            "the next chord reinterprets it in the new one."
        ) as vo:
            self.play(FadeIn(scales[0]))
            self.wait(3.0)
            self.play(FadeIn(scales[1]), FadeIn(row[0]))
            vo.wait_until("a")
            self.play(FadeIn(row[1]), FadeIn(row[2]), FadeIn(row[3]), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(piv), FadeIn(l2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("modulate")
        c = clip("modulate.two")
        card = listen_card(r"Two phrases that begin in C major. \ Both use the dominant of G. \ In which does the music move house, \ and stay: \ A or B?", width=9.6)
        with self.voiceover(
            "An ear question. Two phrases that begin in C major. Both use the dominant of G. In one, the "
            "music comes back; in the other it moves house, and stays. Which is the one that moves: A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        kb = keys(41, 77, width=10.0, height=1.3).to_edge(DOWN, buff=1.25)
        ra = chips(d["visit"]["names"], font_size=30, buff=0.5)
        rb = chips([n if k < 4 else n for k, n in enumerate(d["move"]["names"])], font_size=30, buff=0.5)
        la, lb = label(r"A", font_size=40, color=GREY_A), label(r"B", font_size=40, color=GREY_A)
        rows = VGroup(VGroup(la, ra).arrange(RIGHT, buff=0.6), VGroup(lb, rb).arrange(RIGHT, buff=0.6)).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(UP * 1.2)
        for x in list(ra) + list(rb):
            x.set_opacity(0.0)
        self.play(FadeOut(card), FadeIn(la), FadeIn(lb), FadeIn(kb))
        self.add(ra, rb)
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["visit"]["chords"] + d["move"]["chords"], d["times"]["A"] + d["times"]["B"], end=c.duration)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.12)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.12)
        kb.clear()
        for x in list(ra) + list(rb):
            x.set_opacity(1.0)
        for x in rb[4:]:
            x.set_color(TUNE)
        gl = label(r"these four are in G major", font_size=22, color=TUNE).next_to(VGroup(*rb[4:]), DOWN, buff=0.2)
        with self.voiceover(
            "B. In A, the dominant of G led to a G chord, and then G turned back into the dominant of "
            "C and went home: the new key was visited, for one chord. Musicians call that a "
            "tonicization. <bookmark mark='a'/> In B, after the same visit came a full cadence in G: "
            "four, five, one, with the new key's own chords. That is a modulation. The difference is "
            "not in the chord that leaves. It is in whether the new key is confirmed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(gl))
        self.wait(0.3)
        self.kb, self.rows, self.gl = kb, rows, gl

    # ------------------------------------------------------------------
    def reading(self):
        d = load("modulate")["reading"]
        read = VGroup(label(r"the key finder, \ on the last three chords at each moment:", font_size=24, color=GREY_B),
                      label(r"A: \ " + r" $\cdot$ ".join(tex(x.replace(" major", "")) for x in d["A"]["path"]), font_size=30, color=WHITE),
                      label(r"B: \ " + r" $\cdot$ ".join(tex(x.replace(" major", "")) for x in d["B"]["path"]), font_size=30, color=WHITE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Give the key finder a short memory, three chords, and let it follow both phrases. "
            "<bookmark mark='a'/> In A it says C, then G for a moment, then C again. In B it says C, "
            "then G, and stays there. A key, to the machine and to you, is not a fact about a piece. It "
            "is a running estimate, held over the last few seconds, and music is written to move it."
        ) as vo:
            self.play(FadeOut(self.kb))
            vo.wait_until("a")
            self.play(FadeIn(read))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pivots(self):
        d = load("more")["pivots"]
        ch = columns([p["shared"] for p in d[:5]], [tex(p["key"].replace(" major", "")) for p in d[:5]], width=7.0, height=2.6, color=WEAK, hot=(1, 2), hot_color=BLUE, fmt="{:.0f}", font_size=26, top=7).move_to(LEFT * 2.6 + DOWN * 0.9)
        xl = label(r"triads that C major shares with each key, \ one fifth further each time", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        lists = VGroup(label(r"with G: \ " + r", \ ".join(tex(x) for x in d[1]["chords"]), font_size=28, color=WHITE), label(r"with D: \ " + r", \ ".join(tex(x) for x in d[2]["chords"]), font_size=28, color=WHITE),
                       label(r"with A and beyond: \ none", font_size=28, color=EAR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.9 + UP * 0.2)
        head = label(r"how many pivot chords are there?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How many pivots are there? Count the triads two keys have in common. <bookmark mark='a'/> "
            f"C major and G major, one fifth apart, share {say(d[1]['shared'])} of their seven chords. "
            f"<bookmark mark='b'/> C and D, two fifths apart, share {say(d[2]['shared'])}. "
            "<bookmark mark='c'/> Three fifths apart, and beyond: none at all. So moving to a "
            "neighbouring key is easy, and there are several doors. Moving to a distant key through "
            "ordinary triads is impossible in one step. Composers who wanted distant keys had to go "
            "by way of the keys between, or invent new chords to serve as doors, and Part 19, on "
            "chromatic harmony, is the story of those inventions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(VGroup(ch.bars[0], ch.labels[0], ch.values[0])), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[1], ch.labels[1], ch.values[1])), FadeIn(lists[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(ch.bars[2], ch.labels[2], ch.values[2])), FadeIn(lists[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(ch.bars[3], ch.labels[3], ch.values[3])), FadeIn(VGroup(ch.bars[4], ch.labels[4], ch.values[4])), FadeIn(lists[2]))
        self.wait(0.4)
        self.clear_scene()
