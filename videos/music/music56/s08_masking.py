from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403

TCOL = {"vox": TUNE, "piano": BLUE, "guitar": "#A3E635", "bass": EAR, "kick": GREY_A, "snare": GREY_A, "hat": GREY_A}


def heat(map_, tracks, centres, cell_w=0.36, cell_h=0.42, origin=(-4.2, 1.4)):
    g = VGroup()
    for i, k in enumerate(tracks):
        for j, v in enumerate(map_[k]):
            col = interpolate_color(ManimColor("#14202C"), ManimColor(RED), float(np.clip(v, 0, 1)))
            g.add(Rectangle(width=cell_w, height=cell_h, stroke_width=0.5, stroke_color="#0B0F14", fill_color=col, fill_opacity=1.0)
                  .move_to([origin[0] + cell_w * j, origin[1] - cell_h * i, 0]))
    return g


class Masking(SoundScene):
    def construct(self):
        chapter(self, 7, r"Masking between tracks", r"Why does a part that sounds fine alone vanish in the mix?")
        self.idea()
        self.rule()
        self.maps()
        self.carving()
        self.heard()
        self.lessons()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"Part 4: \ a louder sound hides a quieter one in the same critical band, \ and a little way above it", WHITE),
            (r"in a mix every track sits in every other track's way: \ the guitar alone is bright and clear; \ in the band it is a blur", WHITE),
            (r"so a mix is not a balance of levels alone, \ but of spectra, \ band by band, \ moment by moment", WHITE),
            (r"to see it, \ map it: \ for each track and each band, \ how much of the track is covered by the rest", TUNE),
        ]
        rows_scene(self, r"one track hides another", items,
                   "Every engineer has met this. <bookmark mark='b'/> In Part 4 a louder sound hid a quieter one in the same "
                   "critical band, and a little way above it. <bookmark mark='c'/> In a mix every track sits in every other's way: "
                   "the guitar alone is bright and clear; in the band it becomes a blur. <bookmark mark='d'/> So a mix is not only "
                   "a balance of levels but of spectra, band by band and moment by moment. <bookmark mark='e'/> To see it, map it: "
                   "for each track and each band, how much of the track is covered by the rest of the mix.", marks="bcde")

    # ------------------------------------------------------------------
    def rule(self):
        eq = MathTex(r"\text{masked fraction}_{k,b} = \frac{\sum_t E_k(b,t)\,\bigl[E_{\text{rest}}(b,t) > E_k(b,t)\bigr]}{\sum_t E_k(b,t)}", font_size=34, color=TUNE).move_to(UP * 1.2)
        items = [
            (r"$E_k(b, t)$: \ track $k$'s energy in band $b$ \ (24 bands, \ equally spaced in ERBs, \ 50 Hz to 12 kHz) \ and frame $t$ \ (43 ms windows, \ 21 ms steps)", WHITE),
            (r"$E_{\text{rest}}$: \ everything else in the mix, \ in the same channel; \ left and right are judged apart, \ so panning counts", WHITE),
            (r"a cell is given away when the rest is stronger: \ the ideal binary mask of Part 64's source separation", WHITE),
            (r"a stand-in for the ear's partial loudness, \ simple and explicit", GREY_A),
        ]
        rows = text_rows(items, font_size=20).move_to(DOWN * 1.0)
        head = label(r"a masking map", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is Monochord's map. <bookmark mark='a'/> Split each track into twenty-four bands, equally spaced on the "
            "ear's ERB scale from fifty hertz to twelve kilohertz, and into forty-three-millisecond analysis windows at twenty-one-millisecond steps. "
            "<bookmark mark='b'/> In each cell compare the track with everything else in the mix, left and right channels "
            "separately, so that panning counts. <bookmark mark='c'/> Where the rest is stronger, the cell is given away; it is "
            "the ideal binary mask that Part 64 will use to pull sources apart. The masked fraction is the share of the track's "
            "energy in cells it gives away. <bookmark mark='d'/> It is a stand-in for the ear's partial loudness, simple and "
            "explicit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maps(self):
        d = load("masking")
        tracks = d["tracks"]
        cen = d["centres"]
        hr = heat(d["rough"], tracks, cen, origin=(-4.6, 1.6))
        hc = heat(d["carved"], tracks, cen, origin=(-4.6, 1.6))
        names = VGroup(*[label(k, font_size=16, color=TCOL[k]).move_to([-5.5, 1.6 - 0.42 * i, 0]) for i, k in enumerate(tracks)])
        fx = VGroup(*[label(f"{int(round(cen[j], -1 if cen[j] < 1000 else -2))}", font_size=11, color=GREY_A).move_to([-4.6 + 0.36 * j, 1.6 - 0.42 * len(tracks) + 0.05, 0]) for j in range(0, len(cen), 4)])
        fl = label(r"band centre, \ Hz", font_size=13, color=GREY_A).next_to(fx, DOWN, buff=0.1)
        ov = VGroup()
        for i, k in enumerate(tracks):
            a, b = d["overall"]["rough"][k], d["overall"]["carved"][k]
            ov.add(label(rf"{100 * a:.0f}\% $\to$ {100 * b:.0f}\%", font_size=15, color=TCOL[k]).move_to([5.5, 1.6 - 0.42 * i, 0]))
        ovh = label(r"masked, \ rough $\to$ carved", font_size=14, color=GREY_A).move_to([5.5, 2.15, 0])
        scale = VGroup(label(r"none masked", font_size=13, color=GREY_A), VGroup(*[Rectangle(width=0.2, height=0.18, stroke_width=0, fill_opacity=1, fill_color=interpolate_color(ManimColor("#14202C"), ManimColor(RED), i / 9)) for i in range(10)]).arrange(RIGHT, buff=0),
                       label(r"all", font_size=13, color=GREY_A)).arrange(RIGHT, buff=0.15).to_edge(DOWN, buff=0.35)
        tag = label(r"the rough mix: \ every fader at 0, \ every pan centre, \ no EQ", font_size=17, color=WHITE).to_edge(UP, buff=0.95)
        tag2 = label(r"carved: \ panned, \ high-passed, \ cut where the tracks collide", font_size=17, color=TUNE).to_edge(UP, buff=0.95)
        head = label(r"binary energy-overlap proxy: \ our session", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is our session's map, a row for each track, low bands on the left, red where the track is buried. <bookmark mark='a'/> In the rough mix, every fader at nought, every pan in the centre, no equalization: the voice is mostly clear, but the binary energy-overlap proxy marks {say(100 * d['overall']['rough']['guitar'])} per cent of its energy as overlapped, not removed or proven inaudible, the bass {say(100 * d['overall']['rough']['bass'])}, the piano {say(100 * d['overall']['rough']['piano'])}. <bookmark mark='b'/> Carved, panned and high-passed and cut where the tracks collide, the reds thin out: the guitar down to {say(100 * d['overall']['carved']['guitar'])} per cent, the voice to {say(100 * d['overall']['carved']['vox'])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(fx), FadeIn(fl), FadeIn(scale), FadeIn(ovh))
            vo.wait_until("a")
            self.play(FadeIn(hr), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeOut(hr), FadeIn(hc), FadeOut(tag), FadeIn(tag2), FadeIn(ov))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def carving(self):
        rows = VGroup(VGroup(label(r"track", font_size=17, color=GREY_A), label(r"what was done", font_size=17, color=GREY_A), label(r"why", font_size=17, color=GREY_A)))
        data = [("vox", r"high-pass 110 Hz; \ +2 dB at 3 kHz", r"presence above the band"),
                ("piano", r"left; \ high-pass 180 Hz; \ $-4$ dB at 900 Hz", r"leave the bass its bottom, \ the guitar its middle"),
                ("guitar", r"right; \ high-pass 300 Hz; \ +2 dB at 2 kHz", r"live above the piano"),
                ("bass", r"$-4$ dB at 60 Hz and at 800 Hz", r"leave 60 Hz to the kick"),
                ("kick", r"$-6$ dB at 130 Hz, \ $-5$ at 300", r"leave the bass its notes"),
                ("snare", r"high-pass 150 Hz; \ $-3$ dB at 400 Hz", r"less box"), ("hat", r"high-pass 600 Hz; \ a little right", r"only its sizzle")]
        for k, a, b in data:
            rows.add(VGroup(label(k, font_size=18, color=TCOL[k]), label(a, font_size=16, color=WHITE), label(b, font_size=16, color=GREY_A)))
        rows.arrange(DOWN, buff=0.22)
        for r in rows:
            r[0].set_x(-5.2)
            r[1].next_to([-4.2, r[0].get_y(), 0], RIGHT, buff=0)
            r[2].next_to([1.6, r[0].get_y(), 0], RIGHT, buff=0)
        rows.move_to(DOWN * 0.1)
        head = label(r"the carving", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the carving. <bookmark mark='a'/> The voice high-passed and given a little presence near three kilohertz. The piano panned left, high-passed at a hundred and eighty hertz, and cut at nine hundred, where the guitar's arpeggios live; the guitar panned right, high-passed, and lifted at two kilohertz. <bookmark mark='b'/> The kick and the bass divide the bottom between them: this example cuts the bass around sixty hertz to favor its kick, the kick gives up a hundred and thirty and three hundred to the bass's notes. The snare loses some box, and the hi-hat keeps only its sizzle. Every cut gives a band to someone else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:4]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.3), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("masking")
        c = clip("masking.two")
        boxes = choice_boxes([r"rough", r"carved"], width=3.0, height=0.9, buff=1.4, size=22).move_to(UP * 0.4)
        note = label(r"listen for the guitar's arpeggios and the bass's notes", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"rough and carved, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear both, with headphones: the rough mix, then the carved one. Listen for the guitar's arpeggios and the bass's notes."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"rough, \ then carved", kind="physical model", detail=r"our session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["rough"], st["carved"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["carved"], c.duration, buff=0.08)
        with self.voiceover(
            "In the rough mix everything is there and nothing is clear; carved, each part has a place, in the spectrum and "
            "between the loudspeakers, and the arpeggios and bass notes can be followed."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lessons(self):
        items = [
            (r"carving is a trade: \ every band given to one track is taken from another; \ the map shows both sides", WHITE),
            (r"cut before boosting: \ a cut makes room, \ a boost makes everything louder and fights the others", WHITE),
            (r"pan to unmask: \ two parts in the same band, \ on opposite sides, \ hide each other less", WHITE),
            (r"the first equalizer is the arrangement: \ parts written in different registers do not need carving \ (Part 41)", TUNE),
        ]
        rows_scene(self, r"what the map teaches", items,
                   "What does the map teach? <bookmark mark='b'/> Carving is a trade: every band given to one track is taken from another, and the map shows both sides of the bargain. <bookmark mark='c'/> Cutting and boosting are both useful; choose them for the target sound and available headroom. <bookmark mark='d'/> Pan to unmask: two parts in the same band, on opposite sides, hide each other less. <bookmark mark='e'/> And the first equalizer is the arrangement: parts written in different registers, as Part 41's orchestrators knew, may need less spectral adjustment.", marks="bcde")
