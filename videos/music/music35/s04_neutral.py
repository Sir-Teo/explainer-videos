from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Neutral(SoundScene):
    def construct(self):
        chapter(self, 3, r"Neutral intervals, \ old and new", r"Where did the half-flat come from?", extra=((940, r"al-F\=ar\=ab\=\i"),))
        self.farabi()
        self.safi()
        self.greek()
        self.table()
        self.three()
        self.why()
        self.west()

    # ------------------------------------------------------------------
    def farabi(self):
        d = load("neutral")
        rows_ = {r["name"]: r for r in d["rows"]}
        ruler = cents_ruler([[rows_["Pythagorean minor third 32/27"]["cents"]], [rows_["just minor third 6/5"]["cents"]], [rows_["Zalzal's neutral third 27/22"]["cents"]],
                             [rows_["just major third 5/4"]["cents"]], [rows_["Pythagorean major third 81/64"]["cents"]]], width=9.0, top=450,
                            labels=[r"32/27", r"6/5", r"27/22", r"5/4", r"81/64"], colors=[BLUE, BLUE, EAR, TUNE, TUNE], row_gap=0.55, show_et=False).move_to(RIGHT * 0.6 + DOWN * 0.4)
        vals = VGroup(*[label(rf"{rows_[k]['cents']:.0f}", font_size=16, color=GREY_A).next_to(ruler.rows[i][1], RIGHT, buff=0.2)
                        for i, k in enumerate(["Pythagorean minor third 32/27", "just minor third 6/5", "Zalzal's neutral third 27/22", "just major third 5/4", "Pythagorean major third 81/64"])])
        side = label(r"Zalzal's fret, \ recorded by al-F\=ar\=ab\=\i: \ 27/22, \ 355 cents, \ between every minor and major third", font_size=21, color=EAR).to_edge(UP, buff=1.0)
        head = label(r"a fret in the middle", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The half-flat is old. In the tenth century the philosopher al-Farabi, in his Great Book of Music, the most "
            "advanced treatise on tuning of its time, described the frets of the oud. <bookmark mark='a'/> Among them was the "
            "fret of the eighth-century lutenist Zalzal, at a ratio of twenty-seven to twenty-two above the open string: "
            "three hundred and fifty-five cents, a neutral third. On the ruler it sits between every kind of minor third and "
            "every kind of major third. Al-Farabi also gives a neutral second, twelve elevenths, about one hundred and fifty "
            "cents."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(vals))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def safi(self):
        d = load("safi")
        ruler = cents_ruler([d["notes"]], width=11.0, top=1200, labels=None, colors=[TUNE], show_et=True).move_to(UP * 0.6)
        sizes = VGroup(*[label(rf"{s:.0f}", font_size=13, color=GREY_A) for s in d["steps"]])
        for i, s in enumerate(sizes):
            x0 = -5.5 + 11.0 * d["notes"][i] / 1200
            x1 = -5.5 + 11.0 * (d["notes"][i + 1] if i + 1 < len(d["notes"]) else 1200) / 1200
            s.move_to([(x0 + x1) / 2, 0.1, 0])
        rows_ = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (r"\d{S}af\=\i\ al-D\=\i n al-Urmaw\=\i \ (13th century): \ 17 notes to the octave", WHITE),
            (r"made by a chain of pure fourths: \ every whole tone split into limma, \ limma, \ comma \ (90, \ 90, \ 24 cents)", TUNE),
            (r"some notes land near just intervals: \ 180 and 384 cents, \ close to 10/9 and 5/4; \ Zalzal's 355 falls between its notes", WHITE))]).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        head = label(r"seventeen notes from a chain of fourths", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three centuries later Safi al-Din al-Urmawi organised the scale differently. <bookmark mark='a'/> His gamut has "
            "seventeen notes to the octave, <bookmark mark='b'/> made by a chain of pure fourths, so that every whole tone is "
            "split into two limmas and a comma: ninety, ninety and twenty-four cents. The program builds it and lists the "
            "steps. <bookmark mark='c'/> Some notes land near just intervals, one hundred and eighty and three hundred and "
            "eighty-four cents, close to ten ninths and five fourths, while Zalzal's neutral third falls between its notes. It "
            "became "
            "the basis for theory in the Persian and Ottoman worlds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(sizes))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("neutral")
        hdr = VGroup(*[label(s, font_size=19, color=GREY_A) for s in (r"interval", r"cents", r"24 steps: \ error", r"53 steps: \ error")])
        rows_ = [hdr]
        short = {"Zalzal's neutral third 27/22": r"Zalzal's third 27/22", "neutral second 12/11": r"neutral second 12/11", "Pythagorean minor third 32/27": r"Pyth. minor third 32/27",
                 "just minor third 6/5": r"just minor third 6/5", "just major third 5/4": r"just major third 5/4", "Pythagorean major third 81/64": r"Pyth. major third 81/64"}
        for r in d["rows"]:
            rows_.append(VGroup(label(short[r["name"]], font_size=19, color=EAR if "neutral" in r["name"] or "Zalzal" in r["name"] else WHITE),
                                label(f"{r['cents']:.1f}", font_size=19, color=WHITE),
                                label(f"{r['e24']:+.1f}", font_size=19, color=TUNE if abs(r["e24"]) < abs(r["e53"]) else GREY_A),
                                label(f"{r['e53']:+.1f}", font_size=19, color=TUNE if abs(r["e53"]) < abs(r["e24"]) else GREY_A)))
        xs = [-3.6, 0.2, 2.4, 4.6]
        tbl = VGroup()
        for i, r in enumerate(rows_):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 2.0 - 0.6 * i, 0])
            tbl.add(r)
        head = label(r"two grids, \ measured against the old ratios", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"24 equal steps fits the neutral intervals; \ 53 fits the Pythagorean and just ones", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two modern grids try to capture all this. Arabic theory in the twentieth century adopted twenty-four equal steps "
            "to the octave, quarter tones; Turkish theory, fifty-three, as the next chapters show. Measure each against the old "
            "ratios. Twenty-four steps fits the neutral intervals well, within five cents, but misses the just thirds by up "
            "to sixteen. Fifty-three fits the Pythagorean and just thirds within a cent or two, but misses the neutral "
            "intervals by about eight. Neither grid is the music; each is a choice of what to approximate."
        ):
            self.play(FadeIn(head), FadeIn(tbl), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"neutral intervals are found well beyond the Arab world: \ Persian, \ Turkish, \ Central Asian, \ some African musics", WHITE),
            (r"Part 5: \ a neutral third is rougher than a pure third on harmonic tones", WHITE),
            (r"in melody, \ against a drone or a tonic, \ it is a colour of its own", WHITE),
            (r"listeners raised with this music hear it as stable and expressive", TUNE),
            (r"consonance depends on harmonic timbre; \ melodic intervals depend on culture as well", GREY_A),
        ]
        rows_scene(self, r"why neutral intervals?", items,
                   "Why would a music choose neutral intervals? <bookmark mark='b'/> They are found far beyond the Arab world, in "
                   "Persian, Turkish and Central Asian music and some African musics. <bookmark mark='c'/> On harmonic tones a "
                   "neutral third is rougher than a pure one, as Part 5 would predict, <bookmark mark='d'/> but in melody, heard "
                   "against a tonic, it is a colour of its own. <bookmark mark='e'/> Listeners raised with this music hear it as "
                   "stable and expressive. <bookmark mark='f'/> Consonance depends on timbre; melodic intervals depend on "
                   "culture as well.", marks="cdef")

    # ------------------------------------------------------------------
    def three(self):
        d = load("thirds3")
        c = clip("thirds3.three")
        names = [r"24 steps: \ 350", r"Zalzal: \ 355", r"53 steps: \ 362"]
        cells = VGroup(*[label(n, font_size=26, color=col) for n, col in zip(names, (TUNE, EAR, BLUE))]).arrange(RIGHT, buff=1.5).move_to(UP * 0.4)
        head = label(r"three neutral thirds", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"twelve cents apart at most: \ can you hear the difference?", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "How much do these differences matter to the ear? Here are three neutral thirds over C: the twenty-four-step "
            "three hundred and fifty, Zalzal's three hundred and fifty-five, and fifty-three steps' three hundred and "
            "sixty-two. They span twelve cents, about the difference a careful listener can just detect in a chord. Listen "
            "for whether the colour changes."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"350, \ 355, \ 362", detail=r"an oud model", corner=DL, tag_corner=DR)
            ks = ["24", "zalzal", "53"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def greek(self):
        items = [
            (r"al-Kind\=\i \ (9th century): \ the first Arabic treatises on music, \ from Greek sources", WHITE),
            (r"Greek theory had three genera of tetrachord: \ diatonic, \ chromatic, \ enharmonic", WHITE),
            (r"Ptolemy's lists included `even' tetrachords with neutral-sized steps", WHITE),
            (r"Arabic theorists measured and classified ajnas in that tradition, \ and went beyond it", TUNE),
            (r"the same Greek sources fed medieval European theory \ (Part 23)", GREY_A),
        ]
        rows_scene(self, r"the Greek inheritance", items,
                   "This theory has Greek roots. <bookmark mark='b'/> Al-Kindi, in the ninth century, wrote the first Arabic treatises on music, drawing on Greek sources. <bookmark mark='c'/> Greek theory had three kinds of tetrachord, diatonic, chromatic and enharmonic, <bookmark mark='d'/> and Ptolemy's lists included an even tetrachord with steps of about neutral size. <bookmark mark='e'/> Arabic theorists measured and classified ajnas in that tradition and went far beyond it. <bookmark mark='f'/> The same Greek sources fed medieval European theory, as Part 23 showed.", marks="cdef")

    # ------------------------------------------------------------------
    def west(self):
        items = [
            (r"20th-century European composers tried quarter tones too: \ Alois H\'aba, \ Ivan Wyschnegradsky", WHITE),
            (r"they built quarter-tone pianos and clarinets", WHITE),
            (r"for them the quarter tone was a new colour; \ in maqam it is a native step", WHITE),
            (r"spectral composers \ (Part 30) \ later used them to follow the harmonic series", TUNE),
            (r"the same interval, \ two musical worlds", GREY_A),
        ]
        rows_scene(self, r"quarter tones in the West", items,
                   "Europe discovered quarter tones too. <bookmark mark='b'/> Twentieth-century composers such as Alois Hába and Ivan Wyschnegradsky wrote quarter-tone music <bookmark mark='c'/> and had quarter-tone pianos and clarinets built. <bookmark mark='d'/> For them the quarter tone was a new colour; in maqam it is a native step. <bookmark mark='e'/> The spectral composers of Part 30 later used such intervals to follow the harmonic series. <bookmark mark='f'/> The same interval, in two musical worlds.", marks="cdef")
