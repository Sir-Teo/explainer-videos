from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403

TEMPS = ["quarter-comma meantone", "Werckmeister III", "equal"]
TCOL = {"quarter-comma meantone": BLUE, "Werckmeister III": TUNE, "equal": GREY_A}
ORDER = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "Eb", "Bb", "F"]


class Temperament(SoundScene):
    def construct(self):
        chapter(self, 7, r"Temperament and the colour of keys", r"Did keys really have characters?", extra=((1722, r"\textit{The Well-Tempered Clavier}"),))
        self.chart()
        self.wolf()
        self.quiz()
        self.characters()
        self.equal()

    # ------------------------------------------------------------------
    def chart(self):
        d = load("keys")
        ax = Axes(x_range=[-0.5, 11.5, 1], y_range=[-5, 45, 10], x_length=10.0, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "stroke_width": 1.5}, y_axis_config={"include_numbers": True, "font_size": 18}).move_to(DOWN * 0.4)
        xl = VGroup(*[label(k.replace("#", r"$\sharp$").replace("b", r"$\flat$") if len(k) > 1 else k, font_size=18, color=GREY_A).next_to(ax.c2p(i, -5), DOWN, buff=0.15) for i, k in enumerate(ORDER)])
        yl = label(r"major third, \ cents wider than pure", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        curves = VGroup()
        keys_ = VGroup()
        for name in TEMPS:
            tab = {r["key"]: r["third_error"] for r in d["table"][name]}
            pts = [ax.c2p(i, tab[k]) for i, k in enumerate(ORDER)]
            curves.add(VGroup(VMobject(color=TCOL[name], stroke_width=3).set_points_as_corners(pts), *[Dot(p, radius=0.05, color=TCOL[name]) for p in pts]))
            keys_.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=TCOL[name], stroke_width=4), label(name, font_size=19, color=TCOL[name])).arrange(RIGHT, buff=0.15))
        keys_.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.5)
        wc, wf = d["werck_C"], d["werck_Fs"]
        with self.voiceover(
            "Part 6 showed that no tuning makes every interval pure in every key. The Baroque lived with the choice. "
            "The chart shows the major third of each major key, going round the circle of fifths, in cents wider than "
            "pure. <bookmark mark='a'/> In quarter-comma meantone, the eight common keys have pure thirds, and four keys "
            "far from home have thirds forty-one cents wide, strongly compromised in this layout. <bookmark mark='b'/> In Andreas Werckmeister's "
            f"third temperament, of 1691, every key is usable, with several different interval profiles; some keys share the same third sizes: C's third is {wc['third_error']:.0f} "
            f"cents wide, F sharp's {wf['third_error']:.0f}, as wide as Pythagorean. <bookmark mark='c'/> In equal "
            "temperament every third is fourteen cents wide, and transposed interval ratios are the same, while register and instruments still matter."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            for mark, cv, kk in zip("abc", curves, keys_):
                vo.wait_until(mark)
                self.play(Create(cv), FadeIn(kk), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wolf(self):
        d = load("wolf")
        c = clip("temperament.wolf")
        bx = boxes((r"C--G", r"G$\sharp$--E$\flat$"), buff=2.6)
        vals = VGroup(label(rf"{d['good']:.1f} cents", font_size=24, color=TUNE).next_to(bx[0], DOWN, buff=0.3),
                      label(rf"{d['wolf']:.1f} cents", font_size=24, color=RED).next_to(bx[1], DOWN, buff=0.3))
        head = label(r"quarter-comma meantone: \ a good fifth, \ and the wolf", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        cap = label(r"eleven fifths a little narrow; \ the twelfth absorbs the rest, \ 35.7 cents too wide", font_size=22, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why were meantone's remote keys strongly compromised in this layout? Because the circle does not close. Eleven of its fifths are each "
            "narrowed by a quarter of a comma, and the twelfth, between G sharp and E flat, has to absorb the "
            "difference: it is more than a third of a semitone too wide. Players called it the wolf, for its howl. Here "
            "is a good meantone fifth, then the wolf."
        ):
            self.play(FadeIn(head), FadeIn(bx), FadeIn(vals), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a fifth, \ then the wolf", detail=r"organ tones, \ meantone", kind="synthesized", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], d["starts"]["good"], d["starts"]["wolf"] - 0.5)
            pulse(snd, bx[1], d["starts"]["wolf"], c.duration)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("keys")
        c = clip("keys.cadences")
        card = listen_card(r"A cadence, \ I IV V I, \ in Werckmeister III, \ played first in C, \ then in F$\sharp$. \ "
                           r"Which key's major chords sound rougher? \ (Listen to the thirds, \ not the pitch.)", width=10.4)
        with self.voiceover(
            "Listen. A plain cadence, tonic, subdominant, dominant, tonic, played on organ tones tuned exactly to "
            "Werckmeister's temperament, first in C, then in F sharp. Which key's chords sound rougher?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes((r"C", r"F$\sharp$"), buff=2.4)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"C, \ then F$\sharp$", detail=r"organ tones, \ Werckmeister III", kind="synthesized", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], d["starts"]["C"], d["starts"]["F#"] - 0.5)
            pulse(snd, bx[1], d["starts"]["F#"], c.duration)
        wc, wf = d["werck_C"], d["werck_Fs"]
        ans = VGroup(label(rf"third {wc['third_error']:+.1f} cents".replace("+", "$+$"), font_size=24, color=TUNE).next_to(bx[0], DOWN, buff=0.3),
                     label(rf"third {wf['third_error']:+.1f} cents".replace("+", "$+$"), font_size=24, color=RED).next_to(bx[1], DOWN, buff=0.3))
        with self.voiceover(
            "F sharp is rougher: its thirds beat fast, while C's are nearly smooth. In Werckmeister's tuning the keys with "
            "few sharps and flats are sweet, and the remote ones are sharp-edged, and a composer could use the difference."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def characters(self):
        items = [
            (r"1713: \ Mattheson describes the character of each key: \ D major `sharp and stubborn', \ F minor `deep and heavy'", WHITE),
            (r"some of it is tuning: \ in a well temperament, \ remote keys really are rougher", WHITE),
            (r"some is instruments: \ open strings, \ natural trumpets in D and C", WHITE),
            (r"some is convention, \ passed from piece to piece", WHITE),
            (r"1722: \ Bach's \textit{Well-Tempered Clavier}: \ a prelude and fugue in every key, \ playable in one tuning", TUNE),
        ]
        rows_scene(self, r"the character of keys", items,
                   "Theorists wrote about the character of each key. <bookmark mark='b'/> Mattheson, in 1713, called D "
                   "major sharp and stubborn, and F minor deep and heavy, and others gave different lists. "
                   "<bookmark mark='c'/> Part of it is tuning: in a well temperament the remote keys really are rougher, "
                   "as you just heard. <bookmark mark='d'/> Part is instruments: string players' open strings favour some "
                   "keys, and natural trumpets were often built or crooked for favored keys such as D and C. <bookmark mark='e'/> And part is convention, "
                   "learned from the pieces in each key. <bookmark mark='f'/> In 1722 Bach compiled The Well-Tempered "
                   "Clavier, a prelude and fugue in each of the twenty-four keys, playable on one instrument in one "
                   "tuning: well-tempered, not necessarily equal, a question chapter ten returns to.", marks="cdef")

    # ------------------------------------------------------------------
    def equal(self):
        items = [
            (r"1584: \ Zhu Zaiyu, \ a Ming prince, \ computes twelve equal semitones to many digits", WHITE),
            (r"about 1605: \ Simon Stevin in the Netherlands, \ independently", WHITE),
            (r"lutes and viols, \ with frets across all strings, \ were close to equal already", WHITE),
            (r"keyboards resisted: \ the thirds of equal temperament are 14 cents wide", TUNE),
            (r"it became standard only in the nineteenth century \ (Part 27)", GREY_A),
        ]
        rows_scene(self, r"equal, early", items,
                   "Equal temperament itself was not new. <bookmark mark='b'/> In 1584 Zhu Zaiyu, a prince of the Ming dynasty in China, computed the twelfth root of two to many digits and built pipes to it. <bookmark mark='c'/> Around 1605 the Flemish engineer Simon Stevin did the same, independently. <bookmark mark='d'/> Fretted instruments like the lute and viol, with each fret running under every string, were already close to equal. <bookmark mark='e'/> Keyboard players resisted it because its thirds are fourteen cents wide, <bookmark mark='f'/> and it became the standard only in the nineteenth century, as Part 27 will show.", marks="cdef")
