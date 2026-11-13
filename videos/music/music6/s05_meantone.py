from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Meantone(SoundScene):
    def construct(self):
        chapter(self, 4, r"Pure thirds, \ and a wolf", r"What if the thirds come first?", lit=(1584,), extra=((1523, r"Aron's meantone"),),
                spoken="Pure thirds, and a wolf")
        self.idea()
        self.chords()
        self.circle()
        self.keys()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("meantone")
        title = label(r"A worked example: \ how much must a fifth give up?", font_size=36).to_edge(UP, buff=0.4)
        card = history_card(1523, r"Pietro Aron, \ Venice",
                            r"describes how to tune a keyboard so that the major thirds are pure, by making every fifth a little flat.", width=5.2, font_size=20).to_corner(UL, buff=0.4).shift(DOWN * 0.8)
        ask = pause_card(r"Four pure fifths overshoot a pure third by one comma, \ 21.5 cents. \\ If all four fifths are to share the correction equally, \ how much narrower must each one be?",
                         width=7.6, font_size=26).move_to(RIGHT * 2.7 + UP * 0.9)
        steps = VGroup(MathTex(r"\tfrac{21.5}{4} = 5.4\ \text{cents each}", font_size=36),
                       MathTex(rf"\text{{a fifth of }} 702.0 - 5.4 = {d['fifth_cents']:.1f}\ \text{{cents}}", font_size=34),
                       MathTex(r"\text{exactly: } f^4 = 5 \;\Rightarrow\; f = \sqrt[4]{5} = 1.4953", font_size=34, color=GOOD)).arrange(DOWN, buff=0.28).move_to(RIGHT * 2.9 + UP * 0.6)
        name = label(r"each fifth gives up a quarter of the comma: \ \textbf{quarter-comma meantone}", font_size=30, color=TUNE).move_to(DOWN * 2.0)
        beat = label(rf"on middle C, \ such a fifth beats {d['fifth_beat']:.1f} times a second: \ a slow, \ tolerable waver", font_size=26, color=GREY_A).move_to(DOWN * 2.8)
        with self.voiceover(
            "The first answer starts from what Renaissance musicians cared about most: the third. In 1523 "
            "Pietro Aron, in Venice, described how to tune a keyboard so that its major thirds are pure. The "
            "idea is one line of arithmetic. <bookmark mark='a'/> Four pure fifths overshoot a pure third by a "
            "comma. So make the fifths smaller. If all four share the correction equally, how much narrower "
            "must each fifth be? Pause and work it out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A quarter of twenty-one and a half cents: five point four cents each. <bookmark mark='a'/> So each "
            f"fifth becomes {say(d['fifth_cents'], 1)} cents instead of seven hundred and two. "
            "<bookmark mark='b'/> In exact terms, four of these fifths must multiply to five, so the fifth is "
            "the fourth root of five. <bookmark mark='c'/> Because every fifth gives up a quarter of the comma, "
            "this is called quarter-comma meantone. The name meantone comes from its whole tone, which is "
            f"exactly half of the pure third. <bookmark mark='d'/> A fifth this narrow "
            f"beats about {say(d['fifth_beat'], 1)} times a second on middle C. It is a slow waver, and "
            "listeners accepted it gladly, because in return every third was perfectly still."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(name))
            vo.wait_until("d")
            self.play(FadeIn(beat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chords(self):
        d = load("meantone")
        c = clip("meantone.three")
        e = d["three_errors"]
        note = listen_note(r"The chord of C major, \ three times: \ in Pythagorean tuning, \ in equal temperament, \ and in meantone. \\ Listen to the third settle.", width=10.0, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes((r"Pythagorean", r"equal", r"meantone"), buff=0.5, width=3.3, height=1.3, font_size=30).move_to(DOWN * 0.3)
        vals = VGroup(*[label(rf"third: \ {e[k]:.0f} cents wide" if e[k] > 0.5 else r"third: \ pure", font_size=26, color=error_color(e[k])).next_to(b, DOWN, buff=0.2)
                        for k, b in zip(("pythagorean", "equal", "meantone"), bx)])
        with self.voiceover(
            "This is what they were buying. The chord of C major, three times: in Pythagorean tuning, in the "
            "equal temperament of a modern piano, and in meantone."
        ):
            self.play(FadeIn(note, shift=DOWN * 0.2), FadeIn(bx), FadeIn(vals))
        with self.listen(c) as snd:
            window(snd, r"C major: \ Pythagorean, \ equal, \ meantone", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("pythagorean", "equal", "meantone"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        with self.voiceover(
            "The first is bright and restless. The second, the one you know, shimmers. The third stands still. "
            "To ears that had grown up with Pythagorean thirds, a meantone chord was a revelation, and the music "
            "of the next two centuries, full of slow, glowing triads, was written for it."
        ):
            self.play(Indicate(bx[2][0], color=GOOD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circle(self):
        d = load("meantone")
        w = load("well")["table"]["meantone"]
        circ = FifthsCircle(radius=2.0).move_to(LEFT * 3.7 + DOWN * 0.2)
        edges = VGroup(*[circ.edge(k, color=error_color(err, 8.0) if n != "G#" else BAD, stroke_width=6 if n != "G#" else 10) for k, (n, err) in enumerate(w["fifths"])])
        bars = key_bars([v for _, v in w["thirds"]], [n for n, _ in w["thirds"]], width=6.4, height=2.0, top=45.0).move_to(RIGHT * 3.2 + DOWN * 1.2)
        bl = label(r"the major third on each note: \ cents wider than pure", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.35)
        head = label(r"quarter-comma meantone, \ all the way round", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        facts = VGroup(label(rf"eleven fifths, \ each {d['narrow_by']:.1f} cents narrow", font_size=26, color=NARROW),
                       label(rf"the twelfth: \ {d['wolf_wide_by']:.0f} cents \emph{{wide}}", font_size=26, color=BAD),
                       label(rf"eight pure thirds; \ four that are {d['bad_third_wide_by']:.0f} cents wide", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 1.8)
        with self.voiceover(
            "Now carry it round the circle. <bookmark mark='a'/> Eleven fifths, each five cents narrow. But "
            "narrowing eleven fifths has taken away far more than the Pythagorean comma, so the twelfth fifth "
            f"comes out much too wide: by {say(d['wolf_wide_by'])} cents. <bookmark mark='b'/> This wolf is worse "
            "than the Pythagorean one. <bookmark mark='c'/> And look at the thirds. Eight of them are pure: the "
            "ones on C, G, D, A, E, and on F, B flat and E flat. The other four, the ones that have to cross the "
            f"wolf, are {say(d['bad_third_wide_by'])} cents too wide. They are not thirds at all, and no ear will "
            "take them for thirds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e, (n, _) in zip(edges, w["fifths"]) if n != "G#"], lag_ratio=0.12), FadeIn(facts[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(edges[circ.index("G#")]), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars.base), FadeIn(bars.labels), FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars.bars], lag_ratio=0.1), FadeIn(facts[2]), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keys(self):
        d = load("meantone")
        c = clip("meantone.keys")
        q = listen_card(r"One chord shape, \ a major triad, \ in two keys of a meantone keyboard. \\ A is on C. \ B is on A flat. \ What has happened to B?", width=9.8, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes((r"A: \ C, \ E, \ G", r"B: \ A$\flat$, \ C, \ E$\flat$"), buff=1.2, width=3.8, height=1.5, font_size=32).move_to(DOWN * 0.4)
        with self.voiceover(
            "Hear what that means for a player. The same chord shape, a major triad, in two keys of a meantone "
            "keyboard. First on C. Then on A flat, which on this keyboard is the key called G sharp."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"a major chord on C, \ then on A flat", kind="synthesized", detail=r"quarter-comma meantone", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        ans = VGroup(VGroup(label(r"third: \ pure", font_size=26, color=GOOD), label(rf"fifth: \ {d['narrow_by']:.0f} cents narrow", font_size=26, color=NARROW)).arrange(DOWN, buff=0.1).next_to(bx[0], DOWN, buff=0.25),
                     VGroup(label(rf"third: \ {d['bad_third_wide_by']:.0f} cents wide", font_size=26, color=BAD), label(rf"fifth: \ the wolf, \ {d['wolf_wide_by']:.0f} cents wide", font_size=26, color=BAD)).arrange(DOWN, buff=0.1).next_to(bx[1], DOWN, buff=0.25))
        hist = VGroup(label(r"the standard keyboard tuning of Europe for some two hundred years", font_size=26, color=GREY_A),
                      label(r"composers stayed in the good keys; \ some organs had split black keys, \ with a separate G$\sharp$ and A$\flat$", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first is the sweetest major chord a keyboard has ever made. The second is unusable. "
            "<bookmark mark='a'/> Its third is forty-one cents wide and its fifth is the wolf. The trouble is "
            "that a meantone keyboard has a G sharp but no A flat: the two are different notes, forty-one cents "
            "apart, and there is only one key for both. <bookmark mark='b'/> For some two hundred years this was "
            "the normal keyboard tuning of Europe. Composers simply stayed in the good keys, which is one reason "
            "so much early music is written with few sharps or flats. Some organ builders went further, and "
            "split the black keys in two: the front half for G sharp, the back half for A flat."
        ) as vo:
            self.play(FadeOut(q), FadeIn(ans[0]))
            vo.wait_until("a")
            self.play(FadeIn(ans[1]))
            vo.wait_until("b")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()
