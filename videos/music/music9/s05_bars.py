from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Bars(SoundScene):
    def construct(self):
        chapter(self, 4, r"Bars", r"How do you tune a piece of wood with a knife?", lit=(1877,), extra=((1750, r"Euler and Bernoulli's bending bar"),))
        self.stiff()
        self.modes()
        self.knife()
        self.quiz()
        self.mallets()

    # ------------------------------------------------------------------
    def stiff(self):
        title = label(r"A worked example: \ a bar is not a string", font_size=36).to_edge(UP, buff=0.4)
        bar = Rectangle(width=7.0, height=0.5, stroke_color=WOODC, stroke_width=3, fill_color=WOODC, fill_opacity=0.35).move_to(UP * 1.9)
        half = Rectangle(width=3.5, height=0.5, stroke_color=WOODC, stroke_width=3, fill_color=WOODC, fill_opacity=0.35).move_to(UP * 1.0 + LEFT * 1.75)
        ask = pause_card(r"A string under tension, \ cut to half its length, \ sounds an octave higher. \\ A wooden bar is held straight by its own stiffness, \ and its frequency goes as \\ its thickness divided by the \emph{square} of its length. \ Cut it in half: \ how much higher?", width=10.4, font_size=26).move_to(DOWN * 1.0)
        rows = VGroup(MathTex(r"f \propto \frac{\text{thickness}}{\text{length}^2}", font_size=40),
                      label(r"half the length: \ four times the frequency, \ two octaves", font_size=30, color=TUNE),
                      label(r"half the thickness: \ half the frequency, \ an octave down", font_size=28, color=GREY_A),
                      label(r"the width does not matter at all", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.1)
        with self.voiceover(
            "Now take away the tension altogether. A wooden bar, lying on two supports, is held straight by "
            "nothing but its own stiffness: bend it, and it springs back. Part 1 met stiffness as a small "
            "nuisance in piano strings. In a bar it is everything. A worked example. A string cut to half "
            "its length sounds an octave higher. A bar's frequency goes as its thickness, divided by the "
            "square of its length. Cut a bar in half: how much higher does it sound? Pause, and say."
        ):
            self.play(FadeIn(title), FadeIn(bar), FadeIn(half), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Half the length, squared, is a quarter: four times the frequency. Two octaves. "
            "<bookmark mark='a'/> So the bars of a marimba do not halve in length for each octave, as a "
            "harp's strings nearly do. They shrink much more slowly. <bookmark mark='b'/> And there are two "
            "more handles a string does not have. Make the bar thinner and it gets lower, because it is "
            "less stiff. Make it wider, and nothing happens to its pitch at all."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(Indicate(half, color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        d = load("bars")
        x = np.asarray(d["x"])
        rows = VGroup()
        cols = (AIR, TUNE, EAR)
        for k in range(3):
            sh = np.asarray(d[f"shape{k}"])
            xs = np.linspace(0, 1, len(sh))
            c = VMobject(stroke_color=cols[k], stroke_width=4).set_points_smoothly([np.array([6.0 * (u - 0.5), 0.42 * v, 0]) for u, v in zip(xs[::6], sh[::6])])
            base = DashedLine(LEFT * 3.0, RIGHT * 3.0, color=GREY_D, stroke_width=1.5)
            rows.add(VGroup(base, c, label(rf"{d['uniform'][k]:.2f}", font_size=34, color=cols[k]).next_to(base, RIGHT, buff=0.4)))
        rows.arrange(DOWN, buff=0.75).move_to(LEFT * 1.6 + UP * 0.4)
        iv = d["uniform_intervals"]
        notes = VGroup(label(r"free at both ends: \ it rests on cords at the still points of its lowest mode", font_size=24, color=GREY_A),
                       label(rf"overtones at 2.76 and 5.40: \ {iv[1]:.0f} and {iv[2]:.0f} cents up", font_size=26, color=BAD),
                       label(r"an octave and a sharp fourth; \ two octaves and a sharp fourth", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A bar on a marimba or a xylophone is free at both ends: it rests on two cords, placed where its "
            "lowest mode stands still. <bookmark mark='a'/> That lowest mode is one gentle bend. "
            "<bookmark mark='b'/> The next has three still points, and the one after, four. Their frequencies "
            f"are {say(d['uniform'][1], 2)} and {say(d['uniform'][2], 2)} times the lowest. <bookmark mark='c'/> "
            "In musical terms the first overtone is an octave and a sharp fourth above the note, and the "
            "second is two octaves and a sharp fourth. Strike a plain bar and you hear its note with a sour "
            "clink on top. A length of steel pipe dropped on a floor is a free bar, and that is its sound."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def knife(self):
        d = load("bars")
        m, xy = d["marimba"], d["xylophone"]

        def profile(th, col, y):
            th = np.asarray(th)
            xs = np.linspace(-3.2, 3.2, len(th))
            top = [np.array([u, y + 0.35, 0]) for u in xs]
            bot = [np.array([u, y + 0.35 - 0.7 * t, 0]) for u, t in zip(xs, th)]
            return Polygon(*top, *bot[::-1], stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.3)

        plain = profile(np.ones(60), GREY_B, 2.0)
        pm = profile(d["profile_marimba"][::4], WOODC, 0.5)
        px = profile(d["profile_xylophone"][::4], TUNE, -1.0)
        VGroup(plain, pm, px).shift(LEFT * 3.0)
        t0 = VGroup(label(r"a plain bar", font_size=26, color=GREY_B), MathTex(r"1 : 2.76 : 5.40", font_size=34, color=GREY_B)).arrange(DOWN, buff=0.1).next_to(plain, RIGHT, buff=0.6)
        t1 = VGroup(label(rf"an arch {100 * m['depth']:.0f}\% deep: \ a marimba", font_size=26, color=WOODC), MathTex(rf"1 : {m['ratios'][1]:.2f} : {m['ratios'][2]:.1f}", font_size=34, color=WOODC)).arrange(DOWN, buff=0.1).next_to(pm, RIGHT, buff=0.6)
        t2 = VGroup(label(rf"an arch {100 * xy['depth']:.0f}\% deep: \ a xylophone", font_size=26, color=TUNE), MathTex(rf"1 : {xy['ratios'][1]:.2f} : {xy['ratios'][2]:.1f}", font_size=34, color=TUNE)).arrange(DOWN, buff=0.1).next_to(px, RIGHT, buff=0.6)
        end = VGroup(label(r"the middle is where the lowest mode bends most: \ thin it, \ and that mode falls furthest", font_size=24, color=GREY_A),
                     label(rf"the marimba's cut lowers the bar's own note by {m['octaves_down']:.1f} octaves", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is what a maker does about it. Turn the bar over, and carve an arch out of its underside. "
            "<bookmark mark='a'/> The lowest mode does most of its bending in the middle of the bar. Thin the "
            "middle, and you weaken the bar exactly where that mode needs its stiffness: its frequency "
            "drops a long way. The overtones bend elsewhere as well, and drop less. So the ratios between "
            "them open out. <bookmark mark='b'/> Monochord carves until the first overtone is exactly four "
            f"times the note. That takes an arch {say(100 * m['depth'])} percent of the way through the wood, "
            f"and the second overtone lands at {say(m['ratios'][2], 1)}. One, four, ten: two octaves above "
            "the note, and three octaves and a major third. Those are the tunings stamped on every concert "
            "marimba. <bookmark mark='c'/> A shallower cut puts the first overtone at three times the note, "
            "a twelfth above, and the second near six. That is a xylophone, and the reason it sounds "
            "brighter and drier than a marimba. <bookmark mark='d'/> The same knife does a second job. The "
            f"marimba's arch lowers the bar's own note by {say(m['octaves_down'], 1)} octaves. Without it, "
            "the bass bars of a marimba would be as long as the instrument is wide."
        ) as vo:
            self.play(FadeIn(plain), FadeIn(t0))
            vo.wait_until("a")
            self.play(FadeIn(end[0]))
            vo.wait_until("b")
            self.play(FadeIn(pm), FadeIn(t1))
            vo.wait_until("c")
            self.play(FadeIn(px), FadeIn(t2))
            vo.wait_until("d")
            self.play(FadeIn(end[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        c = clip("bars.pair")
        q = listen_card(r"One note on two wooden bars. \ One is a plain bar; \ one has been carved. \\ Which has been carved?", width=8.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.3).move_to(DOWN * 0.2)
        with self.voiceover(
            "Can you hear the knife? One note, on two wooden bars. One is plain. One has been carved until "
            "its overtones are in tune. Which has been carved?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ two bars", detail=r"computed modes of a free bar", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.8)
        ans = VGroup(label(r"plain: \ a note with a clink on it", font_size=26, color=GREY_B).next_to(bx[0], DOWN, buff=0.25), label(r"carved: \ one clear note", font_size=26, color=WOODC).next_to(bx[1], DOWN, buff=0.25))
        tube = VGroup(label(r"under each bar, \ a tube closed at the bottom, \ tuned to the bar's note:", font_size=24, color=GREY_A),
                      label(r"Part 8's stopped pipe answers at 1, \ 3, \ 5 \ldots \ and so not at the bar's 4 or 10", font_size=24, color=AIR)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "B. The plain bar clinks; the carved one sings. <bookmark mark='a'/> One more piece of tuning "
            "hangs under every marimba bar: a tube, closed at the bottom, as long as a quarter of the "
            "note's wavelength. You met it in Part 8. A stopped pipe answers at one, three and five times "
            "its lowest note, and the bar's overtones are at four and ten. So the tube strengthens the "
            "note, and only the note."
        ) as vo:
            self.play(FadeOut(q), FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(tube))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mallets(self):
        d = load("bars")
        m = d["mallets"]
        c = clip("bars.mallets")
        head = label(r"And the mallet", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)

        def col(db, color, name, sub):
            hb = partial_bars(db, width=3.0, height=2.0, db=True, floor_db=-50.0, colors=[color] * 4, font_size=18)
            return VGroup(hb, label(name, font_size=28, color=color).next_to(hb, UP, buff=0.2), label(sub, font_size=22, color=GREY_A).next_to(hb, DOWN, buff=0.2))

        a = col(m["soft_db"], WOODC, r"a soft yarn mallet", rf"on the bar for {m['soft_ms']:.1f} ms").move_to(LEFT * 3.2 + UP * 0.5)
        b = col(m["hard_db"], STEEL, r"a hard rubber one", rf"on the bar for {m['hard_ms']:.2f} ms").move_to(RIGHT * 3.2 + UP * 0.5)
        note = listen_note(r"One carved bar, \ two mallets.", width=5.0, font_size=26).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The maker fixes where a bar's overtones are. The player decides how much of each to have, with "
            "the choice of mallet. <bookmark mark='a'/> It is Part 7's piano hammer again. A soft mallet, "
            "wound with yarn, stays on the bar for a millisecond or two, and a blow that slow cannot start "
            "an overtone that vibrates a thousand times a second: you get the note and little else. "
            "<bookmark mark='b'/> A hard mallet bounces off in a quarter of a millisecond, and every "
            "overtone the maker tuned is there. Listen: the same bar, the two mallets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"one bar, \ two mallets", detail=r"computed modes, \ two contact times", corner=UL, tag_corner=UR)
            pulse(snd, a[1], snd.time_of("soft"), snd.time_of("soft") + 1.6, buff=0.12)
            pulse(snd, b[1], snd.time_of("hard"), snd.time_of("hard") + 1.6, buff=0.12)
        with self.voiceover(
            "Warm, and then bright. A marimba player carries a dozen pairs of mallets, and choosing among "
            "them is choosing a filter."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
