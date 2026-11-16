from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403
from explainer.music.monochord import timelines as TT

LAYER_C = {"clave": TUNE, "bass": BLUE, "conga": EAR, "guitar": "#A3E635"}


class Clave(SoundScene):
    def construct(self):
        chapter(self, 8, r"The clave", r"How can two sticks organise a whole band?")
        self.family()
        self.travels()
        self.sides()
        self.anticipate()
        self.son()
        self.history()

    # ------------------------------------------------------------------
    def family(self):
        d = load("clave")
        c = clip("clave.family")
        tre = pat_row(TT.TIMELINES["tresillo (8)"], cell=0.55, name=r"tresillo: \ 3 + 3 + 2", size=20)
        cin = pat_row(TT.TIMELINES["cinquillo (8)"], cell=0.55, color=BLUE, name=r"cinquillo: \ 2 + 1 + 2 + 1 + 2", size=20)
        hab = pat_row(["x" if i in d["habanera"] else "." for i in range(8)], cell=0.55, color=EAR, name=r"habanera: \ 3 + 1 + 2 + 2", size=20)
        rows_ = VGroup(tre, cin, hab).arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(UP * 0.3)
        cap = label(r"eight pulses: \ the tresillo is Euclidean, \ E(3,8)", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "The clave belongs to a family that begins with a simpler figure: three strokes in eight pulses, grouped three, "
            "three, two. In Cuba it is called the tresillo, and it is Bjorklund's three in eight. <bookmark mark='a'/> Fill "
            "it in and you get the cinquillo, five strokes in eight. <bookmark mark='b'/> Add one stroke to the tresillo, on the "
            "middle beat, and you get the habanera, the rhythm of a nineteenth-century Cuban dance. Hear the tresillo and the cinquillo on "
            "claves, four bars each, and then the habanera on a bass, over the tresillo."
        ) as vo:
            self.play(FadeIn(tre), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(cin))
            vo.wait_until("b")
            self.play(FadeIn(hab))
        st = d["starts"]
        p8 = d["pulse8"]
        with self.listen(c) as snd:
            window(snd, r"tresillo, \ cinquillo, \ habanera", detail=r"bar and plucked-string models", corner=DL, tag_corner=DR)
            flash_cells(snd, tre.cells, TT.onsets(TT.TIMELINES["tresillo (8)"]), st["tresillo (8)"], p8, 4, 8)
            flash_cells(snd, cin.cells, TT.onsets(TT.TIMELINES["cinquillo (8)"]), st["cinquillo (8)"], p8, 4, 8, color=BLUE)
            flash_cells(snd, hab.cells, d["habanera"], st["habanera"], p8, 4, 8, color=EAR)
            flash_cells(snd, tre.cells, TT.onsets(TT.TIMELINES["tresillo (8)"]), st["habanera"], p8, 4, 8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def travels(self):
        items = [
            (r"the habanera crossed to Spain, \ and back to the Americas: \ Argentina's tango grew from it", WHITE),
            (r"in New Orleans, \ Jelly Roll Morton called it the `Spanish tinge', \ needed for real jazz", WHITE),
            (r"the 3 + 3 + 2 grouping runs under rhythm and blues, \ rock and roll and much later dance music", WHITE),
            (r"one of the most widespread rhythmic cells in the music of the Americas", TUNE),
            (r"Part 38 meets it in the blues", GREY_A),
        ]
        rows_scene(self, r"the tresillo travels", items,
                   "The tresillo travelled further than almost any rhythm. <bookmark mark='b'/> The habanera crossed to Spain and "
                   "back to the Americas, and Argentina's tango grew from it. <bookmark mark='c'/> In New Orleans, Jelly Roll "
                   "Morton called it the Spanish tinge, and said you could not play real jazz without it. "
                   "<bookmark mark='d'/> The three-three-two grouping runs under rhythm and blues, rock and roll, and much later "
                   "dance music. <bookmark mark='e'/> It is one of the most widespread rhythmic cells in the music of the "
                   "Americas. <bookmark mark='f'/> Part 38 meets it in the blues.", marks="cdef")

    # ------------------------------------------------------------------
    def sides(self):
        d = load("clave")
        c = clip("clave.sides")
        three2 = pat_row(["x" if i in d["three_two"] else "." for i in range(16)], cell=0.42, name=r"three-two", size=20)
        two3 = pat_row(["x" if i in d["two_three"] else "." for i in range(16)], cell=0.42, color=BLUE, name=r"two-three", size=20)
        rows_ = VGroup(three2, two3).arrange(DOWN, buff=0.5, aligned_edge=RIGHT).move_to(UP * 0.4)
        halves = VGroup()
        for r in rows_:
            mid = (r.cells[7].get_right() + r.cells[8].get_left()) / 2
            halves.add(DashedLine(mid + UP * 0.35, mid + DOWN * 0.35, color=GREY_A, stroke_width=2))
        cap = label(r"the same five strokes, \ starting in the other half", font_size=20, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Son clave has two halves: one with three strokes, which is a tresillo, and one with two. <bookmark mark='a'/> "
            "Played starting with the three, it is three-two clave; starting with the two, two-three. The strokes are the "
            "same; what differs is which half lines up with the start of the melody's phrase. A band's arrangement is said "
            "to be in clave when its phrases fit one side consistently, and crossed when they do not. Hear three-two, then "
            "two-three, three cycles each."
        ) as vo:
            self.play(FadeIn(three2), FadeIn(halves[0]))
            vo.wait_until("a")
            self.play(FadeIn(two3), FadeIn(halves[1]), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"three-two, \ then two-three", detail=r"bar and membrane models", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(three2, two3), 0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
            sweep(snd, rows_, [d["sides"]["three-two"], d["sides"]["two-three"]], 16 * d["pulse"])
            flash_cells(snd, three2.cells, d["three_two"], d["sides"]["three-two"], d["pulse"], 3, 16)
            flash_cells(snd, two3.cells, d["two_three"], d["sides"]["two-three"], d["pulse"], 3, 16, color=BLUE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def anticipate(self):
        d = load("son")
        bars = VGroup()
        for k, ch in enumerate(d["chords"]):
            box = Rectangle(width=2.8, height=1.0, stroke_color=GREY_B, stroke_width=1.5)
            bars.add(VGroup(box, label(ch, font_size=26, color=WHITE).move_to(box.get_top() + DOWN * 0.3)))
        bars.arrange(RIGHT, buff=0.0).move_to(UP * 0.6)
        marks = VGroup()
        for k, b in enumerate(bars):
            box = b[0]
            x6 = box.get_left()[0] + box.width * 6 / 16
            x12 = box.get_left()[0] + box.width * 12 / 16
            marks.add(Dot([x6, box.get_bottom()[1] + 0.25, 0], radius=0.09, color=BLUE))
            nxt = d["chords"][(k + 1) % 4]
            dd = Dot([x12, box.get_bottom()[1] + 0.25, 0], radius=0.09, color=EAR)
            marks.add(dd)
            marks.add(label(nxt, font_size=16, color=EAR).next_to(box, DOWN, buff=0.12).set_x(x12))
        cl = pat_row(["x" if i % d["clave_period"] in d["clave"] else "." for i in range(64)], cell=0.175, name=r"clave", size=16)
        cl[1].stretch_to_fit_width(bars.width)
        cl.arrange(RIGHT, buff=0.35).next_to(bars, DOWN, buff=0.9)
        cl.shift(RIGHT * (bars.get_center()[0] - cl[1].get_center()[0]))
        side = VGroup(label(r"blue: \ the bass on the `and' of beat 2", font_size=19, color=BLUE),
                      label(r"pink: \ on beat 4, \ already the \textit{next} chord's root, \ held over the bar line", font_size=19, color=EAR),
                      label(r"no bass note on beat 1: \ the \textit{bajo anticipado}", font_size=19, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        head = label(r"the anticipated bass \ (tumbao)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In Cuban son the bass does something unusual. <bookmark mark='a'/> It plays on the and of beat two, and then on "
            "beat four, where it already plays the root of the next chord and holds it over the bar line. "
            "<bookmark mark='b'/> On beat one, where most basses land, it is silent. This anticipated bass, the bajo "
            "anticipado, makes every chord seem to arrive early, and gives son its forward lean."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(cl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.1), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def son(self):
        d = load("son")
        c = clip("son.layers")
        n = d["clave_period"]
        twice = lambda onsets: [bar * 16 + o for bar in range(2) for o in onsets]
        pats = {"clave": d["clave"], "bass": twice([6, 12]), "conga": twice([4, 8, 14, 15]), "guitar": twice([o for o, _ in d["guitar"]])}
        names = {"clave": r"clave", "bass": r"bass", "conga": r"conga", "guitar": r"guitar"}
        rows_ = VGroup(*[pat_row(["x" if i in pats[k] else "." for i in range(n)], cell=0.28, color=LAYER_C[k], name=names[k], size=20) for k in ("clave", "bass", "conga", "guitar")]).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to(UP * 0.3)
        chords = label(r"chords: \ C, \ F, \ G, \ F, \ one a bar", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"a son texture of ours, \ two bars per clave cycle", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now a son texture of our own, built over three-two clave: the clave alone, then the anticipated bass, a conga "
            "with a slap on beat two and two open tones at the end of the bar, and a guitar figure between the beats, each "
            "entering in turn. Every part fits the clave, and none of them doubles it."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(chords))
        cyc = n * d["pulse"]
        with self.listen(c) as snd:
            window(snd, r"clave, \ bass, \ conga, \ guitar", detail=r"bar, \ string and membrane models", corner=DL, tag_corner=DR)
            for i, k in enumerate(("clave", "bass", "conga", "guitar")):
                t0 = d["entries"][k] if k != "clave" else 0.0
                ncyc = int(round(d["cycles"] * 16 / n - t0 / cyc))
                flash_cells(snd, rows_[i].cells, pats[k], t0, d["pulse"], ncyc, n, color=LAYER_C[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"son grew in eastern Cuba and reached Havana around 1910, \ mixing Spanish song and African rhythm", WHITE),
            (r"the clave itself: \ two hardwood sticks, \ the higher struck against the lower in the hand", WHITE),
            (r"in New York in the 1960s and 70s, \ son and its relatives became salsa", WHITE),
            (r"clave as a rule even when nobody plays it: \ arrangers, \ singers and dancers stay `in clave'", TUNE),
            (r"a timeline as a law of composition", GREY_A),
        ]
        rows_scene(self, r"son and salsa", items,
                   "Son grew in eastern Cuba and reached Havana around 1910, mixing Spanish song and African rhythm. "
                   "<bookmark mark='b'/> The clave itself is two hardwood sticks, the higher struck against the lower, which "
                   "rests on the fingers of a cupped hand. <bookmark mark='c'/> In New York in the nineteen-sixties and seventies "
                   "son and its relatives became salsa. <bookmark mark='d'/> And clave acts as a rule even when nobody plays it: "
                   "arrangers, singers and dancers stay in clave. <bookmark mark='e'/> A timeline as a law of composition.",
                   marks="bcde")
