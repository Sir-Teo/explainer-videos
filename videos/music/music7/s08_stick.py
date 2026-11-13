from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Stick(SoundScene):
    def construct(self):
        chapter(self, 7, r"Stick and slip", r"How does a bow keep a string going?", lit=(1863,), extra=((1863, r"Helmholtz watches a bowed string"),))
        self.rosin()
        self.under_bow()
        self.corner()
        self.sawtooth()

    # ------------------------------------------------------------------
    def rosin(self):
        d = load("bow")
        g = axes([0, 1.0], [0, 0.9], x_length=5.4, y_length=3.0, xlabel=r"how fast the string slides past the hair (m/s)", ylabel=r"friction, \ as a fraction of the bow's force", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.3, 0.8], font_size=18)
        g.move_to(RIGHT * 3.5 + DOWN * 0.9)
        v = np.linspace(0, 1, 200)
        mu = d["mu_d"] + (d["mu_s"] - d["mu_d"]) * 0.05 / (0.05 + v)
        cu = curve_from(g, v, mu, BOWED)
        stick = Line(g.ax.c2p(0, 0), g.ax.c2p(0, d["mu_s"]), color=GOOD, stroke_width=6)
        tags = VGroup(label(r"gripping: \ anything up to 0.8", font_size=22, color=GOOD).next_to(g.ax.c2p(0, 0.82), RIGHT, buff=0.15),
                      label(r"sliding: \ about 0.3", font_size=22, color=BOWED).next_to(g.ax.c2p(0.7, 0.32), UP, buff=0.1))
        notes = VGroup(label(r"a plucked string dies away; \ a bowed one can last as long as the bow does", font_size=30, color=GREY_A).to_edge(UP, buff=0.45),
                       label(r"the bow is horsehair, \\ rubbed with rosin: \\ the dried resin of pine trees", font_size=26).move_to(LEFT * 3.9 + UP * 0.6),
                       label(r"rosin grips hard while nothing slides, \\ and lets go once sliding starts", font_size=28, color=BOWED).move_to(LEFT * 3.9 + DOWN * 1.4))
        with self.voiceover(
            "A plucked string and a struck string have one thing in common. They are given their energy at the "
            "start, and after that they can only die away. A violin can hold a note for as long as the bow "
            "lasts. Something is feeding the string, continuously, and yet the bow only ever moves one way. "
            "How does a steady pull make a vibration? <bookmark mark='a'/> The secret is in the rosin. A bow is "
            "a ribbon of horsehair rubbed with dried pine resin, and rosin has a peculiar kind of friction. "
            "<bookmark mark='b'/> As long as the string is not sliding against the hair, rosin grips it hard: "
            "the friction can be anything up to about eight tenths of the force pressing them together. But "
            "once the string starts to slide, the grip collapses, to about three tenths. It is sticky when "
            "still and slippery when moving. Every squeaking door hinge and squealing brake works the same way."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]), FadeIn(g), Create(stick), FadeIn(tags[0]))
            self.play(Create(cu), FadeIn(tags[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def under_bow(self):
        d = load("bow")
        g = axes([0, 2], [-2.1, 0.6], x_length=9.6, y_length=3.4, xlabel=r"time, \ in periods of the note", ylabel=r"speed of the string under the bow (m/s)", xticks=[0, 0.5, 1, 1.5, 2], yticks=[-2, -1, 0, 0.2], font_size=20)
        g.move_to(DOWN * 0.3)
        cu = curve_from(g, d["t"], d["v"], BOWED)
        bowline = DashedLine(g.ax.c2p(0, d["speed"]), g.ax.c2p(2, d["speed"]), color=GOOD, stroke_width=2)
        bl = label(r"the bow's speed: \ 0.2 m/s", font_size=22, color=GOOD).next_to(g.ax.c2p(1.35, d["speed"]), UP, buff=0.08)
        t1 = label(r"sticking: \ carried along by the hair", font_size=24, color=GOOD).move_to(g.ax.c2p(0.55, -0.5))
        t2 = label(rf"slipping: \ flying back at {abs(d['flyback']):.1f} m/s", font_size=24, color=BOWED).move_to(g.ax.c2p(1.62, -1.55))
        res = label(rf"it slips for {100 * d['regime']['slip_fraction']:.0f}\% of each period: \ the bow is {100 * d['beta']:.0f}\% of the way along the string", font_size=28, color=TUNE).to_edge(DOWN, buff=0.35)
        head = label(r"Monochord's string under a bow", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Put that friction on Monochord's string, a tenth of the way from the bridge, and draw the bow at "
            "twenty centimetres a second. This is the speed of the string at the point under the hair, through "
            "two periods of the note. <bookmark mark='a'/> For most of each period the string is stuck to the "
            "hair, and simply rides along with it, at the bow's own speed. All that time the bow is dragging "
            "the string sideways, and the string is pulling back harder and harder. <bookmark mark='b'/> Then "
            "the grip fails. The string breaks free and flies back the other way, "
            f"{say(abs(d['flyback']) / d['speed'])} times as fast as the bow was carrying it. Sliding fast, it "
            "feels little friction. <bookmark mark='c'/> And then it is caught again, and the cycle repeats: "
            "stick, slip, stick, slip, a hundred and ninety-six times a second. Notice the proportions. The "
            f"string slips for {say(100 * d['regime']['slip_fraction'])} percent of each period, and the bow is "
            f"{say(100 * d['beta'])} percent of the way along the string. That is not a coincidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(bowline), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(cu), run_time=3.0)
            self.play(FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corner(self):
        d = load("bow")
        card = history_card(1863, r"Hermann von Helmholtz", r"watches a grain of starch on a bowed string through a microscope whose lens vibrates: it traces a zigzag, not a sine.", width=5.4, font_size=20).to_corner(UL, buff=0.35)
        a, b = LEFT * 5.2 + DOWN * 0.5, RIGHT * 5.2 + DOWN * 0.5
        tau = ValueTracker(0.08)
        string = always_redraw(lambda: VMobject(stroke_color=STR, stroke_width=4).set_points_as_corners(helmholtz_points(a, b, tau.get_value(), 1.2)))
        env = VGroup(*[VMobject(stroke_color=GREY_D, stroke_width=1.5).set_points_smoothly([a + (b - a) * x + UP * s * 4.8 * x * (1 - x) for x in np.linspace(0, 1, 30)]) for s in (1, -1)])
        beta = d["beta"]
        bow = always_redraw(lambda: Line(DOWN * 0.45, UP * 0.45, color=BOWED, stroke_width=7).move_to(a + (b - a) * beta + UP * helmholtz_y(beta, tau.get_value(), 1.2)))
        ends = VGroup(label(r"bridge", font_size=22, color=GREY_B).next_to(a, DOWN, buff=0.2), label(r"nut", font_size=22, color=GREY_B).next_to(b, DOWN, buff=0.2),
                      label(r"bow", font_size=22, color=BOWED).next_to(a + (b - a) * beta, DOWN, buff=0.75))
        notes = VGroup(label(r"two straight lines, \ and a corner that runs round the string once a period", font_size=26, color=STR),
                       label(r"corner beyond the bow: \ the string sticks. \quad Corner between bow and bridge: \ it slips.", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        tau.add_updater(lambda m, dt: m.increment_value(dt * 0.16))
        self.add(tau)
        with self.voiceover(
            "What is the whole string doing meanwhile? Helmholtz found out in the eighteen sixties, by "
            "sticking a grain of starch to a bowed string and watching it through a microscope whose lens "
            "vibrated in time with the note. He expected something like the smooth curves of Part 1. "
            "<bookmark mark='a'/> What he saw was this. The string is never curved at all. At every moment it "
            "is two straight lines, meeting at a corner, and the corner races round the string, out along one "
            "side and back along the other, once in every period. <bookmark mark='b'/> Watch the point under "
            "the bow. While the corner makes its long journey to the far end and back, that point moves "
            "steadily one way: it is stuck to the hair. When the corner passes it, heading for the bridge, "
            "the string snaps free; and when the corner comes back from the bridge it is caught again. The "
            "slip lasts exactly as long as the corner takes to visit the bridge and return. Hence the tenth "
            "of the period. This is called the Helmholtz motion, and it is what every violinist, violist and "
            "cellist is trying to produce, on every note."
        ) as vo:
            self.play(FadeIn(card), FadeIn(env), FadeIn(string), FadeIn(ends), FadeIn(bow))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        tau.clear_updaters()
        string.clear_updaters()
        bow.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def sawtooth(self):
        d = load("bow")
        c = clip("bow.pair")
        g = axes([0, 2], [-1.15, 1.15], x_length=5.6, y_length=2.2, xlabel=r"time, \ in periods", ylabel=r"force on the bridge", xticks=[0, 1, 2], yticks=[], font_size=18)
        g.move_to(LEFT * 3.6 + UP * 1.4)
        saw = curve_from(g, d["t"], d["bridge"], BOWED)
        hb = partial_bars(d["harmonics_db"], width=5.8, height=2.4, db=True, floor_db=-30.0, colors=[BOWED] * 12, font_size=16).move_to(RIGHT * 3.3 + UP * 1.3)
        ideal = VGroup(*[Dot(hb.base.get_left() + RIGHT * (5.8 / 12) * (k + 0.5) + UP * 2.4 * (1 + v / 30.0), radius=0.05, color=WHITE) for k, v in enumerate(d["sawtooth_db"])])
        hl = VGroup(label(r"bars: \ the bowed string", font_size=22, color=BOWED), label(r"dots: \ $1/n$, \ a perfect sawtooth", font_size=22)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(hb, UP, buff=0.15)
        bx = boxes((r"the bare force", r"through a violin's body"), buff=0.6, width=4.0, height=1.0, font_size=28).move_to(DOWN * 2.0)
        with self.voiceover(
            "And the force on the bridge? As the corner travels, the slope of the string at the bridge changes "
            "steadily; when the corner arrives and bounces, the slope flips. <bookmark mark='a'/> A steady climb "
            "and a sudden drop: a sawtooth. Here the climb is a staircase, and in a moment you will see why. "
            "<bookmark mark='b'/> Fourier, in Part 3, gave us a sawtooth's recipe: every partial present, the "
            "n-th at one n-th of the first. Monochord's bowed string agrees with that to a fraction of a "
            "decibel, with one exception. The tenth partial is missing. The bow is at a tenth of the length, "
            "a node of that partial, just as with the pluck and the hammer. A sawtooth with its tenth, "
            "twentieth and thirtieth partials taken out is a staircase of ten steps. <bookmark mark='c'/> "
            "Compare the three ways of playing. A plucked string's partials fall as one over n squared. A "
            "struck string's depend on the felt. A bowed string's fall only as one over n, and they never die "
            "away. It is the richest signal of the three, and by itself it is harsh. Listen to the bare force, "
            "and then to the same force through a violin's body."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(saw), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hb), FadeIn(ideal), FadeIn(hl))
            self.wait(max(vo.until("c") - 6.0, 0.1))
            self.play(Indicate(hb.bars[9], color=WHITE, scale_factor=1.6), Indicate(hb.numbers[9], color=BAD, scale_factor=1.6))
            vo.wait_until("c")
            self.play(FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"a bowed G: \ bare, \ then through the body", detail=r"a model violin", corner=DL, tag_corner=DR)
            for ev, b in zip(("bare", "body"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.6)
        with self.voiceover(
            "The first is a buzz, like a cheap synthesizer. The second is recognisably a violin. Once again "
            "the string supplies the raw material and the box decides the voice. We will open that box in "
            "chapter nine. First, the player."
        ):
            self.play(Indicate(bx[1][0], color=GOOD))
        self.wait(0.3)
        self.clear_scene()
