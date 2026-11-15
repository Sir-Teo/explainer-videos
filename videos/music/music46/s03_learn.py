from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Learn(SoundScene):
    def construct(self):
        chapter(self, 2, r"Statistical learning", r"How do expectations get into a listener?")
        self.saffran()
        self.quiz()
        self.probe()
        self.harmony()
        self.children()

    # ------------------------------------------------------------------
    def saffran(self):
        items = [
            (r"Jenny Saffran and colleagues \ (1996): \ 8-month-old infants heard two minutes of a continuous stream of syllables", WHITE),
            (r"made of nonsense `words', \ with no pauses: \ only the transitional probabilities marked the boundaries", WHITE),
            (r"the infants told words from part-words afterwards", WHITE),
            (r"in 1999 the same was shown with tones: \ for infants and adults", TUNE),
            (r"expectation is learned by counting, \ without trying", GREY_A),
        ]
        rows_scene(self, r"learning by counting", items,
                   "Expectations are learned, and the learning is statistical. <bookmark mark='b'/> In 1996 Jenny Saffran and "
                   "colleagues played eight-month-old infants two minutes of a continuous stream of syllables, "
                   "<bookmark mark='c'/> made of nonsense words with no pauses, so only the transitional probabilities from one "
                   "syllable to the next marked where words began. <bookmark mark='d'/> Afterwards the infants told words from "
                   "part-words. <bookmark mark='e'/> In 1999 the same was shown with tones, for infants and adults. "
                   "<bookmark mark='f'/> Expectation is learned by counting, without trying.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("learn")
        c = clip("learn.stream")
        card = listen_card(r"A stream of tones with no pauses, \ about 20 seconds. \ Then two groups of three. \ "
                           r"One was a `word' that kept recurring in the stream; \ the other was not. \ Which was the word?", width=10.4)
        with self.voiceover(
            "Try it. A stream of tones with no pauses, about twenty seconds of it. Then two groups of three tones. One of them "
            "was a word that kept recurring in the stream; the other was not. Which was the word?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        seq = d["sequence"]
        r = keyroll(seq, width=12.0, height=1.6, lo=58, hi=73, colors=[GREY_B] * len(seq)).move_to(UP * 0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first triplet", r"second triplet")]).arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=1.3)
        self.play(FadeOut(card), FadeIn(r), FadeIn(boxes))
        st = d["starts"]
        ioi = d["ioi"]
        with self.listen(c) as snd:
            window(snd, r"a stream, \ then a test", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [st["stream"] + i * ioi for i in range(len(seq))], hot=WHITE, base=GREY_B)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.2, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        cols = [TUNE, BLUE, EAR, "#A3E635"]
        k = 0
        for w in range(len(seq) // 3):
            wi = [tuple(x) for x in d["words"]].index(tuple(seq[3 * w: 3 * w + 3]))
            for j in range(3):
                r.notes[3 * w + j].set_fill(cols[wi], 1.0)
        ans = VGroup(label(r"the second: \ a word; \ the first was the end of one word and the start of another", font_size=19, color=TUNE),
                     label(rf"inside a word, \ the next tone was certain \ (probability {d['tp_inside']:.1f}); \ across a boundary, \ {d['tp_across']:.2f} on average", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2).next_to(r, DOWN, buff=0.3)
        with self.voiceover(
            "The second. The stream was made of four three-tone words, coloured now, in random order. Inside a word the "
            "next tone was certain; across a boundary it was one of three. The first triplet straddled a boundary, and "
            "most listeners find it less familiar, without being able to say why."
        ):
            self.play(FadeOut(boxes), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmony(self):
        items = [
            (r"the same learning builds a sense of key: \ Krumhansl's probe-tone profiles track how often notes occur \ (Part 15)", WHITE),
            (r"listeners without training expect a tonic after a dominant, \ and respond to a wrong chord", WHITE),
            (r"Bigand and Poulin-Charronnat \ (2006): \ non-musicians' implicit knowledge of harmony nearly matches musicians'", WHITE),
            (r"a style is a statistical environment; \ expectations are its fingerprints in the listener", TUNE),
            (r"chapter 3: \ a listener built the same way", GREY_A),
        ]
        rows_scene(self, r"a lifetime of counting", items,
                   "A lifetime of such counting builds a listener. <bookmark mark='b'/> It builds a sense of key: Carol "
                   "Krumhansl's probe-tone profiles track how often notes occur, as Part 15 showed. <bookmark mark='c'/> Listeners "
                   "without training expect a tonic after a dominant, and respond to a wrong chord; <bookmark mark='d'/> "
                   "Emmanuel Bigand and Bénédicte Poulin-Charronnat argued in 2006 that non-musicians' implicit knowledge of "
                   "harmony nearly matches musicians'. <bookmark mark='e'/> A style is a statistical environment, and "
                   "expectations are its fingerprints in the listener. <bookmark mark='f'/> Chapter three builds a listener the "
                   "same way.", marks="bcdef")

    # ------------------------------------------------------------------
    def probe(self):
        d = load("probe")
        c = clip("probe.three")
        nm = {"C": r"then C", "D": r"then D", "F sharp": r"then F$\sharp$"}
        cells = VGroup(*[VGroup(label(nm[k], font_size=22, color=WHITE),
                                label(rf"{d['ic'][k]:.1f} bits", font_size=18, color=EAR)) .arrange(DOWN, buff=0.2) for k in d["order"]]).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        for cc in cells:
            cc[1].set_opacity(0)
        head = label(r"probe tones", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"Krumhansl and Shepard's method \ (1979): \ a context, \ then one note; \ how well does it fit?", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Krumhansl and Shepard measured such learning with probe tones: play a context, then one note, and ask how well "
            "it fits. Here, the Tune's first phrase three times, followed by D, by C, and by F sharp."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three probes", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(d["order"]):
                end = st[d["order"][i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.1)
        with self.voiceover(
            f"Listeners rate C as fitting best, then D, and F sharp worst; our listener's surprise ranks them the same way: "
            f"{say(d['ic']['C'], 1)}, {say(d['ic']['D'], 1)} and {say(d['ic']['F sharp'], 1)} bits. Fit and predictability "
            "are close to one thing."
        ):
            self.play(*[cc[1].animate.set_opacity(1) for cc in cells])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def children(self):
        items = [
            (r"infants hear contour and rhythm from the start; \ key and harmony take years of exposure", WHITE),
            (r"Trainor and Trehub \ (1994): \ by about age seven, \ children notice a changed note that leaves the key more than one that stays in it", WHITE),
            (r"preference for consonance, \ and for endings on the tonic, \ grows through childhood", WHITE),
            (r"the schemas of chapter 1 are built slowly, \ from the music a child hears", TUNE),
            (r"Part 47 asks which parts need no learning at all", GREY_A),
        ]
        rows_scene(self, r"growing up a listener", items,
                   "Children show the learning happening. <bookmark mark='b'/> Infants hear contour and rhythm from the start, but "
                   "key and harmony take years of exposure. <bookmark mark='c'/> Laurel Trainor and Sandra Trehub found in 1994 "
                   "that by about the age of seven, children notice a changed note that leaves the key more readily than one that "
                   "stays in it. <bookmark mark='d'/> Preference for consonance, and for endings on the tonic, grows through "
                   "childhood. <bookmark mark='e'/> The schemas of chapter one are built slowly, from the music a child hears. "
                   "<bookmark mark='f'/> Part 47 asks which parts need no learning at all.", marks="bcdef")
