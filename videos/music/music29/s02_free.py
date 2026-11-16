from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Free(SoundScene):
    def construct(self):
        chapter(self, 1, r"Atonality, \ free", r"What holds music together without a key?", extra=((1912, r"\textit{Pierrot lunaire}"),))
        self.emancipation()
        self.op19()
        self.counted()
        self.bells()
        self.pierrot()

    # ------------------------------------------------------------------
    def emancipation(self):
        items = [
            (r"Schoenberg: \ `the emancipation of the dissonance' \ ---\ no need to resolve", WHITE),
            (r"Part 27's measure: \ Op. 19 has a quarter of its notes outside any key; \ clarity 0.55", WHITE),
            (r"what replaces the key: \ small cells of intervals, \ repeated, \ transposed, \ turned upside down", TUNE),
            (r"and short pieces: \ without keys, \ long forms were hard to hold together", WHITE),
            (r"Schoenberg disliked the word `atonal'; \ he preferred `pantonal'", GREY_A),
        ]
        rows_scene(self, r"the emancipation of the dissonance", items,
                   "What did leaving the key mean? <bookmark mark='b'/> Schoenberg called it the emancipation of the "
                   "dissonance: a dissonant chord no longer needs to resolve to a consonant one. <bookmark mark='c'/> Part 27 "
                   "measured the result: in his Opus 19 a quarter of the sounding time is outside any key, and the key-finder's "
                   "best fit drops to about 0.55. <bookmark mark='d'/> What holds such music together is small cells of "
                   "intervals, repeated, transposed and turned upside down, <bookmark mark='e'/> and brevity: without a key to "
                   "return to, long forms were hard to hold together, and many pieces of these years last a minute or two. "
                   "<bookmark mark='f'/> Schoenberg disliked the word atonal; he preferred pantonal, a term expressing his objection to the negative implication of atonal; it does not mean every passage literally sounds all keys simultaneously.", marks="cdef")

    # ------------------------------------------------------------------
    def op19(self):
        d = load("op19")
        c = clip("op19.no2")
        lo = min(n[0] for n in d["notes"]) - 1
        hi = max(n[0] for n in d["notes"]) + 1
        g = mroll(d["notes"], width=11.4, height=3.4, lo=lo, hi=hi, color=TUNE, bar_h=0.1).move_to(DOWN * 0.2)
        head = label(r"Schoenberg, \ Op. 19 No. 2, \ whole", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"a repeated major third, \ G and B, \ pulses through; \ chords gather round it", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Hear the second piece of the set, whole, nine bars. A single interval, a major third from G to B, pulses in "
            "even eighth notes almost all the way through, and chords gather around it and dissolve again. The third is "
            "what the ear holds on to; there is no key for it to belong to."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Op. 19 No. 2", detail=r"from the encoding, \ Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=TUNE)
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("op19")
        pt = d["pc_time"]
        bars = columns([x for x in pt], [PC[k] for k in range(12)], width=8.4, height=2.6, color=TUNE, hot=(7, 11), hot_color=EAR, fmt="{:.0f}", font_size=17)
        bars.move_to(LEFT * 1.6 + DOWN * 0.4)
        t = label(r"Op. 19 No. 2: \ beats of sounding time on each pitch class", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"G and B tower over the rest", EAR),
            (r"but all twelve pitch classes are used", WHITE),
            (r"a centre without a key: \ an interval, \ not a tonic", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.4))
        side.move_to(RIGHT * 4.6 + DOWN * 0.2)
        with self.voiceover(
            "Count the sounding time on each pitch class. <bookmark mark='a'/> G and B, the pulsing third, tower over the "
            "rest. <bookmark mark='b'/> But every one of the twelve pitch classes is used. <bookmark mark='c'/> The piece has a "
            "centre, but the centre is an interval, not a tonic with a scale around it: one of the ways free atonality "
            "holds together."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pierrot(self):
        items = [
            (r"\textit{Erwartung} \ (1909): \ a half-hour monodrama with almost no repetition", WHITE),
            (r"\textit{Pierrot lunaire} \ (1912): \ 21 poems, \ a speaking-singing voice \ (\textit{Sprechstimme}) \ and five players", WHITE),
            (r"Berg and Webern, \ his pupils: \ Berg's \textit{Wozzeck} \ (1925), \ Webern's tiny pieces", WHITE),
            (r"Expressionism: \ inner states, \ anxiety, \ dreams, \ in painting and music alike", TUNE),
            (r"by 1920 Schoenberg wanted a method that would let him write long forms again", EAR),
        ]
        rows_scene(self, r"Vienna's expressionism", items,
                   "Around these pieces grew a whole repertory. <bookmark mark='b'/> Erwartung, of 1909, is a half-hour "
                   "monodrama for soprano and orchestra with almost no repeated material. <bookmark mark='c'/> Pierrot "
                   "lunaire, of 1912, sets twenty-one poems for a voice that half speaks and half sings, with five players. "
                   "<bookmark mark='d'/> His pupils Alban Berg and Anton Webern went their own ways: Berg toward the opera "
                   "Wozzeck, Webern toward pieces a few seconds long. <bookmark mark='e'/> The movement around them, in painting "
                   "as well as music, is called Expressionism: inner states, anxiety, dreams. <bookmark mark='f'/> By about "
                   "1920 Schoenberg wanted a method that would let him write long forms again.", marks="cdef")

    # ------------------------------------------------------------------
    def bells(self):
        a = pc_clock([9, 6, 11], radius=1.15, color=TUNE).move_to(LEFT * 4.3 + DOWN * 0.2)
        b = pc_clock([7, 0, 5], radius=1.15, color=BLUE).move_to(DOWN * 0.2)
        c_ = pc_clock([9, 6, 11, 7, 0, 5], radius=1.15, color=EAR).move_to(RIGHT * 4.3 + DOWN * 0.2)
        la = label(r"A, \ F$\sharp$, \ B: \ (0 2 5)", font_size=20, color=TUNE).next_to(a, DOWN, buff=0.45)
        lb = label(r"G, \ C, \ F: \ fourths, \ (0 2 7)", font_size=20, color=BLUE).next_to(b, DOWN, buff=0.45)
        lc = label(r"together: \ (0 1 2 4 6 7)", font_size=20, color=EAR).next_to(c_, DOWN, buff=0.45)
        head = label(r"Op. 19 No. 6: \ the two `bell' chords", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Go back to the piece the part began with. <bookmark mark='a'/> Its first chord, high in the piano, is A, F sharp and B, with prime form zero two five. <bookmark mark='b'/> The second, lower, is G, C and F, stacked fourths with prime form zero two seven, a different set class. <bookmark mark='c'/> Sounding together they make a six-note set, spread widely in register; its heard grouping depends on spacing and context. The piece is built from these two bell-like chords, a small cell repeated and varied, one example of motivic and textural organization in free atonality."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(c_), FadeIn(lc))
        self.wait(0.4)
        self.clear_scene()
