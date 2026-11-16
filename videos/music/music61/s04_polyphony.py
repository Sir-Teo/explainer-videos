from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403

NAMES = {0: "C", 1: r"C$\sharp$", 2: "D", 3: r"E$\flat$", 4: "E", 5: "F", 6: r"F$\sharp$", 7: "G", 8: r"A$\flat$", 9: "A", 10: r"B$\flat$", 11: "B"}


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Polyphony(SoundScene):
    def construct(self):
        chapter(self, 3, r"Many notes at once", r"Why is a chord so much harder than a melody?")
        self.why()
        self.quiz()
        self.salience()
        self.cancel()
        self.hidden()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"one note: \ one period, \ one comb of partials at $f_0, \ 2f_0, \ 3f_0, \dots$", WHITE),
            (r"a chord: \ several combs added, \ and the wave no longer repeats at any of their periods", WHITE),
            (r"the combs share teeth: \ C and G share every third partial of C; \ an octave shares every partial of the upper note", WHITE),
            (r"so the question becomes: \ which set of combs explains this spectrum?", TUNE),
        ]
        rows_scene(self, r"why polyphony is hard", items,
                   "A melody has one note at a time; music mostly does not. <bookmark mark='b'/> One note has one period and one comb of partials. <bookmark mark='c'/> A chord adds several combs, and the wave no longer repeats at any of their periods, so a single-period tracker can return a shared period or subharmonic rather than identify each note. <bookmark mark='d'/> Worse, the combs share teeth. In exact three-to-two tuning, C and G share every third C partial; equal temperament and inharmonic instruments give near-overlaps instead; an octave shares every partial of its upper note. <bookmark mark='e'/> So the question becomes: which set of combs explains this spectrum?", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("chords")
        c = clip("chords.two")
        card = listen_card(r"Two piano chords. \ Are they the same chord, \ or does one have a note the other lacks?", width=9.0)
        with self.voiceover("Your turn. Two piano chords. Are they the same chord, or does one have a note the other lacks?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two chords", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"different: \ the second adds C5, \ an octave above the C. \ It brightens the chord, \ but is easy to miss", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("Different. The second adds a C an octave above the lowest note. It makes the chord a little brighter, and it is easy to miss, for the reason we just saw: ideal harmonic spectra overlap this way; real piano inharmonicity, attacks and independent decay can supply extra cues."):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def salience(self):
        d = load("chords")
        cands = d["cands"]
        sal = np.array(d["triad"]["salience"])
        W, H = 10.5, 2.6
        x0 = -W / 2
        bw = W / len(cands)
        bars = VGroup(*[Rectangle(width=bw * 0.75, height=max(0.01, H * v), stroke_width=0, fill_color=TUNE if m in d["triad"]["truth"] else GREY_B,
                                  fill_opacity=0.9).move_to([x0 + bw * (i + 0.5), -1.3, 0], aligned_edge=DOWN) for i, (m, v) in enumerate(zip(cands, sal))])
        ticks = VGroup(*[label(nm(m), font_size=12, color=GREY_A).move_to([x0 + bw * (i + 0.5), -1.55, 0]) for i, m in enumerate(cands) if m % 12 in (0, 4, 7)])
        eq = MathTex(r"s(m) = \sum_{h=1}^{8} \alpha^{h-1}\, S\!\left(m + 12\log_2 h\right), \qquad \alpha = 0.8", font_size=32, color=WHITE).to_edge(UP, buff=1.0)
        top = sorted(range(len(cands)), key=lambda i: -sal[i])[:5]
        note = label(r"gold: \ the notes played \ (C4, \ E4, \ G4); \ the tallest grey bars are their octaves below, \ and notes whose partials they share", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"salience: \ harmonic summation", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "One answer is salience, after Anssi Klapuri. <bookmark mark='a'/> For every candidate note, add up the spectrum at "
            "its first eight partials, each weighted a little less than the one before. <bookmark mark='b'/> For C-E-G the notes "
            "played stand out, but not alone: each note's octave below collects the same partials, plus a few, and so do notes "
            "whose partials happen to land on the chord's. Salience ranks candidates; it does not decide which are there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(ticks), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note), *[Indicate(bars[i], color=EAR, scale_factor=1.05) for i in top])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cancel(self):
        items = [
            (r"1. \ find the most salient candidate", WHITE),
            (r"2. \ subtract its partials from the spectrum, \ but not all of a shared partial: \ real spectra are smooth, \ so take only the share a smooth envelope predicts", WHITE),
            (r"3. \ repeat until what is left has no salient pitch", WHITE),
            (r"Klapuri \ (2003, \ 2006): \ iterative estimation and cancellation; \ later, \ joint estimation of whole sets of notes", WHITE),
            (r"and the octave? \ only the smoothness of the lower note's spectrum betrays its upper neighbour", TUNE),
        ]
        rows_scene(self, r"estimate, \ then cancel", items,
                   "Salience ranks; a second step decides. Klapuri's method estimates and cancels. <bookmark mark='b'/> Find the "
                   "most salient candidate. <bookmark mark='c'/> Subtract its partials from the spectrum, but not all of a shared "
                   "partial: real spectra are smooth, so take only the share that a smooth envelope through the note's other "
                   "partials predicts. <bookmark mark='d'/> Repeat until what is left has no salient pitch. <bookmark mark='e'/> "
                   "Anssi Klapuri published this in 2003 and refined it in 2006; later methods estimate whole sets of notes "
                   "jointly. <bookmark mark='f'/> And the octave? Only an unusually bright, uneven run of even partials betrays an "
                   "upper octave sitting on a lower note.", marks="bcdef")

    # ------------------------------------------------------------------
    def hidden(self):
        d = load("chords")
        rows_ = []
        for name, t, key in ((r"C-E-G", d["triad"], "triad"), (r"C-E-G-C", d["octave"], "octave")):
            rows_.append(VGroup(label(name, font_size=22, color=WHITE),
                                label(", ".join(nm(m) for m in t["truth"]), font_size=18, color=GREY_A),
                                label(", ".join(nm(m) for m in t["nmf"]) or "nothing", font_size=18, color=TUNE if sorted(t["nmf"]) == sorted(t["truth"]) else EAR),
                                label(", ".join(nm(m) for m in t["net"]) or "nothing", font_size=18, color=TUNE if sorted(t["net"]) == sorted(t["truth"]) else EAR)))
        g = VGroup(*rows_).arrange(DOWN, buff=0.6)
        for r in g:
            r[0].set_x(-5.0)
            r[1].set_x(-2.2)
            r[2].set_x(1.0)
            r[3].set_x(4.3)
        top = VGroup(*[label(t, font_size=16, color=GREY_A).move_to([x, g.get_top()[1] + 0.5, 0]) for t, x in
                       ((r"played", -2.2), (r"NMF \ (Chapter 5)", 1.0), (r"the network \ (Chapter 6)", 4.3))])
        o = d["octave"]
        found_nmf, found_net = 72 in o["nmf"], 72 in o["net"]
        head = label(r"the hidden octave", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is what the two transcribers of the coming chapters report for the two chords. <bookmark mark='a'/> The "
            f"plain triad: {'both find it exactly' if sorted(d['triad']['nmf']) == [60, 64, 67] and sorted(d['triad']['net']) == [60, 64, 67] else 'not quite exactly, as the colours show'}. "
            "<bookmark mark='b'/> With the octave added, "
            + ("both hear the upper C." if found_nmf and found_net else
               "the factorization misses the upper C, explaining its partials with the lower one." if not found_nmf and found_net else
               "the network misses the upper C." if found_nmf and not found_net else
               "neither hears the upper C: its partials are all claimed by the lower one.")
            + " Octaves are the classic failure of transcription, by machines and by people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()
