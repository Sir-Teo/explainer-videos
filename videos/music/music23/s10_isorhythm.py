from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Isorhythm(SoundScene):
    def construct(self):
        chapter(self, 9, r"Isorhythm", r"What happens when a rhythm and a melody have different lengths?", extra=((1320, r"de Vitry's motets"),))
        self.engine()
        self.listen_engine()
        self.found()
        self.vitry()

    # ------------------------------------------------------------------
    def engine(self):
        d = load("isorhythm")
        color, talea = d["color"], d["talea"]
        per = d["periods"]
        cc = VGroup(*[label(LETTER[p % 12], font_size=24, color=TUNE) for p in color]).arrange(RIGHT, buff=0.35)
        tt = VGroup()
        for x in talea:
            w = 0.32 * abs(x)
            tt.add(Rectangle(width=w, height=0.28, stroke_width=1.5 if x < 0 else 0, stroke_color=GREY_B, fill_color=BLUE if x > 0 else BLACK, fill_opacity=0.9 if x > 0 else 0.0))
        tt.arrange(RIGHT, buff=0.06)
        lc = label(rf"color: \ {len(color)} pitches", font_size=22, color=TUNE).next_to(cc, LEFT, buff=0.5)
        lt = label(rf"talea: \ {sum(1 for x in talea if x > 0)} notes and {sum(1 for x in talea if x < 0)} rests", font_size=22, color=BLUE).next_to(tt, LEFT, buff=0.5)
        top = VGroup(VGroup(lc, cc), VGroup(lt, tt)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 1.4)
        rows_ = VGroup(*[label(t, font_size=23, color=c_) for t, c_ in (
            (r"the tenor's pitches \ (the color) \ are laid through a repeating rhythm \ (the talea)", WHITE),
            (rf"{len(color)} pitches and {sum(1 for x in talea if x > 0)} notes: \ they start together again after {per['lcm']} notes", WHITE),
            (rf"that is {per['colors']} statements of the color \ and {per['taleae']} of the talea: \ the least common multiple", TUNE),
            (r"the word `isorhythm' is modern: \ Friedrich Ludwig, \ 1904", GREY_A))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 1.3)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        with self.voiceover(
            "Many fourteenth-century motet tenors use this cyclic procedure. <bookmark mark='a'/> Take a fragment of "
            "chant, its pitches only: the color. Take a rhythm, a sequence of lengths and rests: the talea. Lay the "
            "pitches through the rhythm, one pitch to each note, repeating each as often as needed. "
            f"<bookmark mark='b'/> Here the color has {say(len(color))} pitches and the talea {say(sum(1 for x in talea if x > 0))} "
            f"notes, so they drift against each other and only start together again after {say(per['lcm'])} notes, "
            f"<bookmark mark='c'/> which is {say(per['colors'])} statements of the color and {say(per['taleae'])} of the "
            "talea: the least common multiple, the same arithmetic as Part 11's polyrhythms. <bookmark mark='d'/> The "
            "composers had no name for the whole procedure; the musicologist Friedrich Ludwig coined the word isorhythm, "
            "equal rhythm, in 1904."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_engine(self):
        d = load("isorhythm")
        c = clip("isorhythm.engine")
        notes, upper = d["notes"], d["upper"]
        g = voices_roll([upper, notes], width=11.6, height=3.0, colors=[GREY_A, TUNE], bar_h=0.12).move_to(DOWN * 0.2)
        n_col, n_tal = len(d["color"]), sum(1 for x in d["talea"] if x > 0)
        for k, b in enumerate(g.parts[1].notes):
            b.set_fill(TUNE if (k // n_col) % 2 == 0 else BLUE)
        ticks = VGroup()
        span = sum(abs(x) for x in d["talea"])
        for k in range(d["periods"]["taleae"] + 1):
            x = g.frame.get_left()[0] + g.frame.width * span * k / g.total
            ticks.add(Line([x, g.frame.get_bottom()[1] - 0.15, 0], [x, g.frame.get_bottom()[1] - 0.35, 0], color=BLUE, stroke_width=2))
        tl = label(r"talea boundaries", font_size=18, color=BLUE).next_to(ticks, DOWN, buff=0.1)
        cl = label(r"the tenor, \ coloured by statement of the color", font_size=18, color=TUNE).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        with self.voiceover(
            "Here is that tenor, sung, with a free voice above it. The tenor's notes are coloured by which statement of "
            "the color they belong to, and the ticks below mark where each talea begins. Listen for the rhythm repeating "
            "while the melody slides across it."
        ):
            self.play(FadeIn(g), FadeIn(ticks), FadeIn(tl), FadeIn(cl))
        with self.listen(c) as snd:
            window(snd, r"color against talea", detail=r"two synthetic voices", kind="synthesized", corner=UR, tag_corner=UL)
            flash(snd, g.parts[1].notes, [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def found(self):
        d = load("isorhythm")
        v = d["vitry"]
        lug = v[0]
        sc = {int(k): x for k, x in lug["scan"].items()}
        lags = sorted(sc)
        ax = Axes(x_range=[0, max(lags) + 5, 33], y_range=[0, 1.05, 0.5], x_length=6.0, y_length=2.6, tips=False,
                  axis_config={"color": GREY_B, "stroke_width": 1.5, "include_numbers": False}).move_to(LEFT * 3.2 + UP * 0.3)
        curve = VMobject(color=TUNE, stroke_width=2).set_points_as_corners([ax.c2p(k, sc[k]) for k in lags])
        chance = DashedLine(ax.c2p(0, lug["chance"]), ax.c2p(max(lags) + 5, lug["chance"]), color=GREY_B, stroke_width=1.5)
        peaks = VGroup(*[label(rf"{k}", font_size=16, color=TUNE).next_to(ax.c2p(k, sc[k]), UP, buff=0.08) for k in (33, 66, 99) if k in sc])
        t = label(r"\textit{Lugentium siccentur}: \ the tenor's rhythm, \ repeated at each lag \ (bars)", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.3)
        cl = label(r"shuffled bars: \ chance", font_size=15, color=GREY_B).next_to(chance, RIGHT, buff=0.1).shift(UP * 0.15 + LEFT * 1.5)
        tab = VGroup()
        tab.add(VGroup(label(r"motet", font_size=18, color=GREY_B), label(r"talea", font_size=18, color=GREY_B), label(r"tenor", font_size=18, color=GREY_B), label(r"top voice", font_size=18, color=GREY_B), label(r"chance", font_size=18, color=GREY_B)))
        for r in v:
            short = " ".join(r["title"].split(".")[-1].split()[:2]).title()
            tab.add(VGroup(label(rf"\textit{{{short}}}", font_size=18, color=WHITE), label(rf"{r['lag']} bars", font_size=17, color=TUNE),
                           label(rf"{r['shares'][2]:.2f}", font_size=17, color=TUNE), label(rf"{r['shares'][0]:.2f}", font_size=17, color=WHITE), label(rf"{r['chance']:.2f}", font_size=17, color=GREY_B)))
        xs = [1.1, 3.3, 4.25, 5.2, 6.15]
        for i, row in enumerate(tab):
            y = 1.6 - 0.45 * i
            for k, cell in enumerate(row):
                cell.move_to([xs[k], y, 0])
                if k == 0:
                    cell.align_to([xs[0] - 0.55, 0, 0], LEFT)
        cap = VGroup(label(r"the scan finds each talea, \ and its multiples, \ in de Vitry's four motets", font_size=21, color=TUNE),
                     label(r"but plain tenors of long notes repeat by chance too: \ in two of the four the margin is small", font_size=21, color=EAR)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "If a tenor was built this way, a program should be able to find the talea without being told. Cut the voice "
            "into bars, describe each bar by its rhythm alone, and for every lag ask what share of bars is repeated "
            "exactly that many bars later. <bookmark mark='a'/> In the tenor of Philippe de Vitry's motet Lugentium "
            f"siccentur, the share jumps to {lug['shares'][2]:.2f} at a lag of {say(lug['lag'])} bars, and again at "
            "sixty-six and ninety-nine: the talea and its multiples. The dashed line is chance, the best the same bars "
            "reach when their order is shuffled. <bookmark mark='b'/> The scan finds a talea in all four of de Vitry's "
            "motets in the corpus: twelve bars, eighteen and thirty-three, and in Vos qui admiramini lags of fifteen, thirty and "
            "forty-five bars all score almost the same. The upper voices repeat too, less "
            "strictly, a step towards the later practice of making every voice isorhythmic. <bookmark mark='c'/> But "
            "look at the chance column. A tenor of plain long notes repeats its rhythm by accident, so in two of the "
            "four the margin over chance is small. A better detector would also check that the pitches change while the "
            "rhythm repeats, which would help distinguish independent pitch and rhythm cycles from trivial sustained-note repetition."
        ) as vo:
            self.play(Create(ax), FadeIn(t))
            self.play(Create(curve), Create(chance), FadeIn(cl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(peaks))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(cap[0]))
            vo.wait_until("c")
            self.play(FadeIn(cap[1]), Indicate(VGroup(*[row[4] for row in tab[1:]]), color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vitry(self):
        d = load("vitry")
        c = clip("vitry.excerpt")
        vs = d["voices"]
        g = voices_roll(vs, width=11.6, height=3.6, colors=[EAR, TUNE, BLUE, GREY_A], bar_h=0.1).move_to(DOWN * 0.3)
        head = label(r"Philippe de Vitry, \ \textit{Vos qui admiramini}: \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(r"two texts above, \ a slow tenor and contratenor below: \ pitches and lengths from \textit{Polyphonic Music of the Fourteenth Century}, \ voices synthetic", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.35)
        cap.scale_to_fit_width(min(cap.width, 12.6))
        with self.voiceover(
            "And here is the real thing: the opening of de Vitry's Vos qui admiramini, sung by the film's synthetic "
            "voices from the pitches and lengths of a modern edition. Two quick upper voices, each with its own Latin "
            "poem; below them the slow isorhythmic tenor and a contratenor. Listen to how the upper voices chatter in "
            "short notes over the long, regular steps beneath."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"de Vitry, \ \textit{Vos qui admiramini}", detail=r"from the edition, \ synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[EAR, TUNE, BLUE, GREY_A])
            cursor(snd, g, 0.0, d["quarter"])
        self.wait(0.3)
        self.clear_scene()
