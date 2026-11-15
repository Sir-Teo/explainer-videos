from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Oldest(SoundScene):
    def construct(self):
        chapter(self, 1, r"The oldest instruments", r"How old is music, \ and how could we know?")
        self.timeline()
        self.pipes()
        self.bones()
        self.older()

    # ------------------------------------------------------------------
    def timeline(self):
        ev = [
            (55000, r"Divje Babe: \ a bear bone with holes \ (disputed)", GREY_B),
            (42500, r"Gei{\ss}enkl\"osterle: \ swan bone and mammoth ivory", TUNE),
            (37000, r"Hohle Fels: \ the vulture flute", TUNE),
            (8500, r"Jiahu, \ China: \ crane-bone flutes", BLUE),
            (4500, r"Ur: \ lyres in royal graves", EAR),
            (3400, r"Ugarit: \ a hymn written in notation", GOLD),
        ]
        tl = log_timeline(ev, width=11.0, lo=2000, hi=100000, y=-0.2, size=17)
        head = label(r"instruments that survive, \ on a logarithmic scale of years", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"each step along the axis multiplies the age by about three", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Put the oldest surviving instruments on a line, with time on a logarithmic scale. <bookmark mark='a'/> At Divje "
            "Babe in Slovenia, a cave bear's thigh bone with holes, perhaps fifty to sixty thousand years old and linked to "
            "Neanderthals; many think the holes are a carnivore's bites. <bookmark mark='b'/> At Geissenklösterle, flutes of "
            "swan bone and of mammoth ivory, dated in 2012 to about forty-two or forty-three thousand years. "
            "<bookmark mark='c'/> The vulture flute of Hohle Fels, a few kilometres away. <bookmark mark='d'/> At Jiahu in "
            "China, flutes of red-crowned crane bone, some nine thousand years old, with five to eight holes; one could "
            "still be played. <bookmark mark='e'/> Lyres buried in the royal graves of Ur, about forty-five hundred years "
            "ago. <bookmark mark='f'/> And at Ugarit, about thirty-four hundred years ago, a hymn written on clay in a "
            "notation scholars still argue over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl[:-1]), FadeIn(cap), FadeIn(tl.marks.copy().set_opacity(0.15)))
            for mark, m in zip("abcdef", tl.marks):
                vo.wait_until(mark)
                self.play(FadeIn(m))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipes(self):
        d = load("hook")
        f = d["fundamental"]
        W1, W2 = 11.0 * 0.218 / 0.34, 11.0
        p1 = RoundedRectangle(width=W1, height=0.45, corner_radius=0.18, stroke_color=GREY_A, fill_color="#E7DCC8", fill_opacity=0.25)
        p2 = RoundedRectangle(width=W2, height=0.45, corner_radius=0.18, stroke_color=GREY_A, fill_color="#E7DCC8", fill_opacity=0.12)
        g = VGroup(VGroup(p1, label(rf"21.8 cm, \ the fragment: \ about {f['0.218']:.0f} Hz \ ({note_of(f['0.218'])})", font_size=18, color=WHITE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT),
                   VGroup(p2, label(rf"34 cm, \ one estimate of the whole: \ about {f['0.34']:.0f} Hz \ ({note_of(f['0.34'])})", font_size=18, color=WHITE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(DOWN * 0.3)
        eq = MathTex(r"f \approx \frac{c}{2\,(L + 0.61\,a + 0.85\,a)}", font_size=40).to_edge(UP, buff=1.1)
        head = label(r"what a pipe's length says", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A pipe open at both ends sounds when a pressure wave fits twice its length, as Part 8 showed, plus a little at "
            "each end, where the air keeps moving past the opening. <bookmark mark='a'/> The surviving fragment is "
            f"{say(21.8, 1)} centimetres long: as a pipe it would sound about {say(f['0.218'])} hertz with its holes closed. "
            f"<bookmark mark='b'/> If the whole flute was nearer thirty-four centimetres, as one estimate has it, about "
            f"{say(f['0.34'])} hertz, the top of a soprano's range. The physics fixes the region; the lost end and the "
            "player's breath decide the rest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(g.copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bones(self):
        items = [
            (r"Nicholas Conard and colleagues \ (2009): \ the Hohle Fels flute, \ in twelve pieces, \ five holes, \ a notched end", WHITE),
            (r"fine marks near the holes look like measurements: \ the maker planned where the holes would go", WHITE),
            (r"ivory flutes in nearby caves are harder to make: \ split a tusk, \ hollow both halves, \ glue them airtight", WHITE),
            (r"several flutes in neighbouring caves suggest a tradition, \ not one inventor", TUNE),
            (r"the same caves hold the oldest figurative carvings: \ music arrives with art", GREY_A),
        ]
        rows_scene(self, r"what the bones say", items,
                   "What do these bones tell us? <bookmark mark='b'/> Nicholas Conard and colleagues published the Hohle Fels "
                   "flute in 2009: twelve pieces, five holes and a notched end. <bookmark mark='c'/> Fine marks near the holes "
                   "look like measurements, as if the maker planned where each hole would go. <bookmark mark='d'/> Ivory flutes "
                   "from nearby caves are harder still to make: split a tusk, hollow both halves, and fit them back together "
                   "airtight. <bookmark mark='e'/> Several flutes from neighbouring caves suggest a tradition, not a single "
                   "inventor. <bookmark mark='f'/> And the same caves hold some of the oldest figurative carvings: music arrives "
                   "in the record with art.", marks="cdef")

    # ------------------------------------------------------------------
    def older(self):
        items = [
            (r"a voice, \ a clap, \ a drum of wood and skin leave nothing behind", WHITE),
            (r"a flute that took planning implies music already worth the trouble", WHITE),
            (r"so music is older than the oldest instrument, \ by an unknown margin", WHITE),
            (r"to look further back we need other evidence: \ what all living peoples share, \ and what other animals do", TUNE),
            (r"chapter 2: \ every society sings", GREY_A),
        ]
        rows_scene(self, r"older than any flute", items,
                   "Bones are not the beginning. <bookmark mark='b'/> A voice, a clap, a drum of wood and skin leave nothing "
                   "behind. <bookmark mark='c'/> A flute that took planning implies music already worth the trouble. "
                   "<bookmark mark='d'/> So music is older than the oldest instrument, by a margin nobody knows. "
                   "<bookmark mark='e'/> To look further back we need other evidence: what all living peoples share, and what "
                   "other animals do. <bookmark mark='f'/> Chapter two: every society sings.", marks="bcdef")
