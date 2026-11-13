from __future__ import annotations

import math

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Schelleng(SoundScene):
    def construct(self):
        chapter(self, 8, r"How hard to press", r"Why is a violin so much harder to play than a piano?", lit=(1863,), extra=((1973, r"Schelleng's diagram"),))
        self.quiz()
        self.diagram()
        self.example()
        self.start()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("schelleng")
        c = clip("schelleng.three")
        a, b = LEFT * 4.6 + UP * 1.6, RIGHT * 4.6 + UP * 1.6
        string = Line(a, b, color=STR, stroke_width=4)
        bridge = Triangle(color=WOOD, fill_opacity=1, stroke_width=0).scale(0.22).next_to(a, DOWN, buff=0)
        bow = Line(DOWN * 0.7, UP * 0.7, color=BOWED, stroke_width=8).move_to(a + (b - a) * 0.1)
        knobs = VGroup(label(r"how fast: \ the bow's speed", font_size=28, color=GREY_A), label(r"how hard: \ the force pressing hair to string", font_size=28, color=BOWED),
                       label(r"where: \ how far from the bridge", font_size=28, color=WOOD)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.6)
        arrows = VGroup(Arrow(bow.get_top() + LEFT * 0.0, bow.get_top() + UP * 0.8, color=GREY_A, buff=0.05, stroke_width=3),
                        Arrow(bow.get_center() + RIGHT * 1.1, bow.get_center() + RIGHT * 0.1, color=BOWED, buff=0.0, stroke_width=3),
                        DoubleArrow(a + DOWN * 0.95, bow.get_bottom() + DOWN * 0.25, color=WOOD, buff=0.0, stroke_width=3, tip_length=0.15))
        with self.voiceover(
            "A pianist chooses one number for each note: the hammer's speed. A violinist's bow arm chooses "
            "three, and goes on choosing them for as long as the note lasts. <bookmark mark='a'/> How fast to "
            "draw the bow. <bookmark mark='b'/> How hard to press it into the string. <bookmark mark='c'/> And "
            "where on the string to put it: how far from the bridge. The Helmholtz motion of the last chapter "
            "exists only for some combinations of the three."
        ) as vo:
            self.play(FadeIn(string), FadeIn(bridge), FadeIn(bow))
            for mark, k, ar in zip("abc", knobs, arrows):
                vo.wait_until(mark)
                self.play(FadeIn(k), GrowArrow(ar) if not isinstance(ar, DoubleArrow) else FadeIn(ar), run_time=0.7)
        self.wait(0.3)
        self.clear_scene()
        q = listen_card(r"One note, \ bowed three times: \ the same speed, \ the same place on the string. \\ Only the force changes: \ too much, \ about right, \ too little, \ in some order. \ Which is which?",
                        width=10.4, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(("A", "B", "C"), buff=1.3, width=2.6, height=1.3).move_to(DOWN * 0.5)
        with self.voiceover(
            "Hear what happens outside them. One note, bowed three times, at the same speed and the same place. "
            "Only the force changes. One has too much, one about the right amount, one too little. Which is "
            "which?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ three bow forces", detail=r"a model violin", corner=DL, tag_corner=DR)
            for ev, bq in zip("ABC", bx):
                t0 = snd.time_of(ev)
                pulse(snd, bq, t0, t0 + 1.5)
        f, r = d["forces"], d["regimes"]
        ans = VGroup(*[VGroup(label(t1, font_size=26, color=col), label(t2, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(bq, DOWN, buff=0.25)
                       for bq, t1, t2, col in zip(bx, (rf"too much: \ {f['heavy']:.1f} N", rf"right: \ {f['right']:.1f} N", rf"too little: \ {f['light']:.2f} N"),
                                                  (r"a crushed growl, \\ and the pitch falls", r"the Helmholtz motion", rf"the string slips {r['light']['slips_per_period']:.0f} times \\ a period: \ thin and glassy"), (BAD, GOOD, AIR))])
        with self.voiceover(
            "A had too much. The string could not break free on time, so each cycle took too long: the sound is "
            "a growl, and the pitch has fallen. B was right. C had too little. The bow could not hold on, and "
            f"the string slipped {say(r['light']['slips_per_period'])} times in every period instead of once: a "
            "thin, glassy whistle that players call surface sound. Every beginner's violin makes both of those "
            "noises, often in the same bar."
        ):
            self.play(FadeOut(q), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chart(self):
        d = load("schelleng")
        rows = d["rows"]
        lg = math.log10
        g = axes([lg(0.035), lg(0.32)], [-2.2, 1.2], x_length=6.2, y_length=4.6, xlabel=r"where the bow is: \ fraction of the string from the bridge", ylabel=r"bow force (N)",
                 xticks=[lg(0.04), lg(0.07), lg(0.1), lg(0.2), lg(0.3)], yticks=[-2, -1, 0, 1], xfmt=lambda v: f"{10 ** v:.2g}", yfmt=lambda v: {-2: "0.01", -1: "0.1", 0: "1", 1: "10"}[int(round(v))], font_size=20)
        pt = lambda beta, force: g.ax.c2p(lg(beta), lg(force))  # noqa: E731
        hi = VGroup(*[Dot(pt(r["beta"], r["max"]), radius=0.07, color=BAD) for r in rows])
        lo = VGroup(*[Dot(pt(r["beta"], r["min"]), radius=0.07, color=AIR) for r in rows])
        b0, b1 = rows[0]["beta"], rows[-1]["beta"]
        hi_line = DashedLine(pt(b0, rows[0]["schelleng_max"]), pt(b1, rows[-1]["schelleng_max"]), color=BAD, stroke_width=2)
        lo_line = DashedLine(pt(b0, rows[0]["schelleng_min"]), pt(b1, rows[-1]["schelleng_min"]), color=AIR, stroke_width=2)
        wedge = Polygon(*[pt(r["beta"], r["max"]) for r in rows], *[pt(r["beta"], r["min"]) for r in rows[::-1]], stroke_width=0, fill_color=GOOD, fill_opacity=0.16)
        return d, g, pt, hi, lo, hi_line, lo_line, wedge

    def diagram(self):
        d, g, pt, hi, lo, hi_line, lo_line, wedge = self.chart()
        rows = d["rows"]
        VGroup(g, hi, lo, hi_line, lo_line, wedge).move_to(RIGHT * 3.1 + DOWN * 0.3)
        card = history_card(1973, r"John Schelleng, \ ``The bowed string and the player''", r"a retired radio engineer and amateur cellist maps the forces a bowed string will accept.", width=5.6, font_size=20).to_corner(UL, buff=0.35)
        t_hi = VGroup(label(r"too hard: \ the string cannot let go", font_size=24, color=BAD), MathTex(r"F_{\max} \propto \frac{\text{bow speed}}{\text{distance}}", font_size=28, color=BAD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t_lo = VGroup(label(r"too lightly: \ the bow cannot hold on", font_size=24, color=AIR), MathTex(r"F_{\min} \propto \frac{\text{bow speed}}{\text{distance}^2}", font_size=28, color=AIR)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t_ok = label(r"between them: \ the Helmholtz motion", font_size=26, color=GOOD)
        key = label(r"dots: \ Monochord's string. \ Dashes: \ Schelleng's formulas.", font_size=20, color=GREY_B)
        notes = VGroup(t_hi, t_lo, t_ok, key).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(LEFT * 3.9 + DOWN * 1.0)
        wide, narrow = rows[6], rows[0]
        with self.voiceover(
            "In 1973 John Schelleng, a retired radio engineer and an amateur cellist, drew the map. Across: "
            "where the bow is, as a fraction of the string's length from the bridge. Up: the force on the bow. "
            "Both scales are logarithmic. <bookmark mark='a'/> There is a largest force. When Helmholtz's corner "
            "comes by, it gives the string a jolt, and that jolt has to be enough to break the rosin's grip. "
            "Press harder than the jolt can overcome and the string stays stuck too long: the growl. The limit "
            "is proportional to the bow's speed, divided by its distance from the bridge. The red dots are "
            "where Monochord's simulated string actually gave up; the dashed line is Schelleng's formula. "
            "<bookmark mark='b'/> There is a smallest force. All through the sticking part of the cycle, the "
            "string's energy is leaking away into the bridge, which is the point of the instrument, and the "
            "bow has to hold on against the wobble that leaves behind. Press too lightly and the string breaks "
            "away early. That limit rises faster towards the bridge: as one over the distance squared, in "
            f"Schelleng's formula. Monochord's string needs about {say(d['min_ratio'][3])} times his minimum, and "
            f"its slope is steeper, {say(abs(d['slope_min']), 1)} rather than two. The formula was only ever "
            "meant as a guide. <bookmark mark='c'/> Between the two limits is a wedge, and the Helmholtz "
            f"motion lives inside it. With the bow a fifth of the way along the string, the wedge is wide: the "
            f"largest force is {say(wide['max'] / wide['min'])} times the smallest. At four percent, close to the "
            f"bridge, it has all but closed: a factor of {say(narrow['max'] / narrow['min'], 1)}."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in hi], lag_ratio=0.1), Create(hi_line), FadeIn(t_hi), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in lo], lag_ratio=0.1), Create(lo_line), FadeIn(t_lo), FadeIn(key), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(wedge), FadeIn(t_ok))
        f = d["forces"]
        marks = VGroup(*[VGroup(Dot(pt(0.1, f[k]), radius=0.09, color=WHITE), label(nm, font_size=24).next_to(pt(0.1, f[k]), RIGHT, buff=0.12)) for k, nm in zip(d["order"], "ABC")])
        with self.voiceover(
            "And here are the three notes you just heard. A, far above the wedge. C, far below it. B, in the "
            "middle. A violinist's right arm spends its life steering inside this wedge without looking at it."
        ):
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def example(self):
        title = label(r"A worked example: \ moving towards the bridge", font_size=36).to_edge(UP, buff=0.4)
        ask = pause_card(r"A violinist moves the bow from one tenth of the string's length to one twentieth, \ at the same speed. \\ By Schelleng's two rules, \ what happens to the largest force? \ To the smallest? \ To the room between them?",
                         width=10.4, font_size=26).move_to(UP * 1.0)
        tab = VGroup(
            VGroup(label(r"largest force", font_size=28, color=BAD), MathTex(r"\propto \tfrac{1}{\text{distance}}", font_size=30), label(r"doubles", font_size=28, color=BAD)),
            VGroup(label(r"smallest force", font_size=28, color=AIR), MathTex(r"\propto \tfrac{1}{\text{distance}^2}", font_size=30), label(r"four times as large", font_size=28, color=AIR)),
            VGroup(label(r"the room between", font_size=28, color=GOOD), MathTex(r"F_{\max} / F_{\min}", font_size=30), label(r"halves", font_size=28, color=GOOD)),
            VGroup(label(r"the force on the bridge", font_size=28, color=TUNE), MathTex(r"\propto \tfrac{\text{speed}}{\text{distance}}", font_size=30), label(r"doubles: \ 6 dB louder, \ and brighter", font_size=28, color=TUNE)),
        )
        for r in tab:
            r[0].move_to(LEFT * 5.9, aligned_edge=LEFT)
            r[1].move_to(LEFT * 1.2)
            r[2].move_to(RIGHT * 1.0, aligned_edge=LEFT)
        for k, r in enumerate(tab):
            r.shift(UP * (0.9 - 0.95 * k))
        with self.voiceover(
            "A worked example. A violinist moves the bow from a tenth of the string's length to a twentieth, "
            "twice as close to the bridge, keeping the same speed. By Schelleng's two rules, what happens to "
            "the largest force, to the smallest, and to the room between them? Pause, and work it out."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "The largest force goes as one over the distance: it doubles. <bookmark mark='a'/> The smallest goes "
            "as one over the distance squared: four times as large. <bookmark mark='b'/> So the whole window "
            "moves up, and the room inside it halves. The player must press harder, and more exactly. "
            "<bookmark mark='c'/> What is the reward? The sawtooth on the bridge is proportional to bow speed "
            "over distance, so it doubles too: six decibels louder, with a sharper corner and so more high "
            "partials. That is how string players make a loud, brilliant sound: near the bridge, with weight. "
            "And a soft, veiled one: out over the fingerboard, with almost none. Composers write both into "
            "the score, in Italian: sul ponticello, on the bridge, and sul tasto, on the fingerboard."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def start(self):
        head = label(r"And the note has to be started", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"the map is for a note \\ already sounding", r"started from rest with a small steady force, \ Monochord's string never finds \\ the Helmholtz motion. \ It slips several times a period, \ and stays that way."),
            (r"so players bite", r"pressed firmly at first and then eased, \ the same string settles into one slip a period, \\ and keeps it at forces where it could never have begun."),
            (r"the attack has \\ its own map", r"Knut Guettler, \ 2002: \ for the first slips to come on time, \ the bow's force and \\ its acceleration must sit inside a narrow triangle."),
            (r"a piano key cannot \\ be pressed wrongly", r"a bow can, \ in three ways at once, \ on every note. \\ That is the price of a sound that can swell, \ fade and change colour while it lasts."),
        ], left=-6.5, text_left=-2.7, top=1.9, step=1.4, name_size=26, text_size=23, color=BOWED)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "One more difficulty, and Monochord ran into it before I did. <bookmark mark='a'/> Schelleng's map "
            "is for a note that is already sounding. Started from rest, with a small steady force inside the "
            "wedge, Monochord's string never found the Helmholtz motion at all. It slipped several times a "
            "period, and stayed that way. <bookmark mark='b'/> What worked was what players do: press firmly "
            "for the first instant, then ease off. The string settles into one slip a period, and then keeps "
            "it, even at forces where it could never have started. Violinists call it the bite at the start "
            "of the stroke. <bookmark mark='c'/> The attack has a map of its own, drawn by Knut Guettler in "
            "2002: bow force against bow acceleration, with a narrow triangle inside which the first few slips "
            "arrive on time. <bookmark mark='d'/> So this is why a violin is hard and a piano is not. A piano "
            "key cannot be pressed wrongly. A bow can, in three ways at once, on every note. That is the "
            "price of a sound that can swell, fade and change its colour for as long as it lasts."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
