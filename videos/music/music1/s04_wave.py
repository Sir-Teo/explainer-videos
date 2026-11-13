from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (FORCE, FREQ, GOOD, LEFT_C, MASS, PART, RATIO, RIGHT_C, STR, TIME, TUNE, clip,
                                        film, load, say, window)


def wall(height=1.6) -> VGroup:
    """A wall, hatched."""
    r = Rectangle(width=0.22, height=height, stroke_width=0, fill_color=GREY_C, fill_opacity=0.9)
    hatch = VGroup(*[Line(r.get_corner(DL) + UP * y + RIGHT * 0.22, r.get_corner(DL) + UP * (y + 0.2) + RIGHT * 0.5,
                          color=GREY_D, stroke_width=1.5) for y in np.arange(0.0, height - 0.1, 0.22)])
    return VGroup(r, hatch)


class Wave(SoundScene):
    def construct(self):
        self.card()
        self.flick()
        self.superposition()
        self.speed()
        self.round_trip()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"A wave on a string", r"What does a string do when you let it go?", lit=(1713,),
                            part=PART)
        with self.voiceover("Chapter three. A wave on a string."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def flick(self):
        d = load("pulse")
        frames = d["right"]
        per = (len(frames) - 1) / 2.0          # frames per unit of time (the pulse crosses the rope in one unit)
        rope = StringView(width=6.4, scale=1.5, supports=False).move_to(LEFT * 3.2 + UP * 0.3)
        w = wall().move_to(rope.p(1.0) + RIGHT * 0.11)
        hand = label(r"your hand", font_size=24, color=GREY_B).next_to(rope.p(0.0), DOWN, buff=0.5)
        wl = label(r"a wall", font_size=24, color=GREY_B).next_to(w, DOWN, buff=0.25)
        tr = film(rope, frames)
        with self.voiceover(
            "Forget music for a minute. Take a long rope, tie the far end to a wall, and flick the near end. "
            "<bookmark mark='a'/> A bump runs down the rope. It keeps its shape, and it travels at a steady speed. "
            "<bookmark mark='b'/> When it reaches the wall it comes back, upside down."
        ) as vo:
            self.play(FadeIn(rope), FadeIn(w), FadeIn(hand), FadeIn(wl))
            vo.wait_until("a")
            self.play(tr.animate.set_value(0.42 * per), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(1.15 * per), run_time=max(vo.remaining(), 3.0), rate_func=linear)
        # the trick: let the rope carry on past the wall, with a mirror-image bump coming the other way
        ghost = StringView(width=6.4, scale=1.5, supports=False, color=LEFT_C, stroke_width=3).move_to(RIGHT * 3.2 + UP * 0.3)
        ghost.curve.set_stroke(opacity=0.75)
        gtr = film(ghost, -frames[:, ::-1])
        glabel = label(r"an imaginary rope, \ and an upside-down bump", font_size=26, color=LEFT_C)
        glabel.next_to(ghost, UP, buff=1.1)
        still = Dot(rope.p(1.0), radius=0.09, color=GOOD)
        stag = label(r"this point never moves", font_size=24, color=GOOD).next_to(still, DOWN, buff=1.0)
        with self.voiceover(
            "Why upside down? Here is a way to see it. Imagine the rope does not stop at the wall but carries on, "
            "<bookmark mark='a'/> and that on the imaginary half an upside-down copy of the bump is coming the other "
            "way. <bookmark mark='b'/> The two bumps arrive at the wall together, and there they cancel exactly, "
            "always. <bookmark mark='c'/> That point never moves. So this endless rope behaves, on our side, exactly "
            "like a rope tied to a wall. The reflection is the imaginary bump walking out into the real world."
        ) as vo:
            tr.set_value(0)
            gtr.set_value(0)
            vo.wait_until("a")
            self.play(w.animate.set_opacity(0.25), FadeIn(ghost), FadeIn(glabel), FadeOut(wl))
            vo.wait_until("b")
            self.play(tr.animate.set_value(0.5 * per), gtr.animate.set_value(0.5 * per), run_time=3.0,
                      rate_func=linear)
            self.play(FadeIn(still), FadeIn(stag), run_time=0.4)
            self.play(tr.animate.set_value(1.15 * per), gtr.animate.set_value(1.15 * per),
                      run_time=max(vo.remaining() - 0.5, 4.0), rate_func=linear)
        self.wait(0.3)
        rope.clear_updaters()
        ghost.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def superposition(self):
        d = load("pulse")
        frames = d["cross"]
        per = (len(frames) - 1) / 2.0
        rope = StringView(width=11.0, scale=1.5).shift(UP * 0.9)
        tr = film(rope, frames)
        defn = definition_card(r"Superposition", r"when two waves meet on a string, \ the displacement is the sum of "
                               r"the two. \ Each then carries on as if the other had not been there.",
                               color=TUNE, width=9.4, font_size=28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One more experiment. Send two bumps towards each other. <bookmark mark='a'/> They do not bounce. They "
            "do not merge. They pass straight through, and while they overlap the rope's height is simply the two "
            "heights added. <bookmark mark='b'/> This is called superposition, and everything in this part depends "
            "on it. Waves on a string add."
        ) as vo:
            self.play(FadeIn(rope))
            vo.wait_until("a")
            self.play(tr.animate.set_value(0.25 * per), run_time=3.0, rate_func=linear)
            self.play(tr.animate.set_value(0.45 * per), run_time=max(vo.until("b"), 2.0), rate_func=linear)
            self.play(FadeIn(defn, shift=UP * 0.2), run_time=0.6)
            self.play(tr.animate.set_value(0.25 * per), run_time=max(vo.remaining() - 0.3, 2.0), rate_func=linear)
        rope.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def speed(self):
        d = load("pulse")
        g = load("mersenne")
        rows = [(r"sound in air", d["sound_in_air"], GREY_B), (r"our monochord's string", d["speed_measured"], TUNE),
                (r"a guitar's top string", g["guitar"]["c"], FREQ)]
        bars = VGroup()
        for name, v, col in rows:
            bar = Rectangle(width=v / 60.0, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.9)
            t = label(name, font_size=28, color=WHITE)
            val = label(rf"{v:.0f} m/s", font_size=28, color=col)
            bars.add(VGroup(t, bar, val))
        for b in bars:
            b[1].next_to(ORIGIN, RIGHT, buff=0).shift(LEFT * 2.2)
            b[0].next_to(b[1], LEFT, buff=0.3)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        bars.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        for b in bars:
            shift = bars[0][1].get_left()[0] - b[1].get_left()[0]
            b.shift(RIGHT * shift)
        bars.move_to(DOWN * 1.5 + RIGHT * 0.6)
        law = MathTex(r"c", r"=", r"\sqrt{\frac{T}{\mu}}", font_size=64).move_to(UP * 2.2 + LEFT * 3.2)
        law[0].set_color(TIME), law[2].set_color(FORCE)
        units = MathTex(r"\sqrt{\frac{\text{N}}{\text{kg/m}}} = \sqrt{\frac{\text{kg}\,\text{m/s}^2}{\text{kg/m}}}"
                        r" = \frac{\text{m}}{\text{s}}", font_size=34, color=GREY_A).next_to(law, RIGHT, buff=0.9)
        meas = label(rf"timed in the simulation: \ {d['speed_measured']:.1f} m/s \qquad "
                     rf"from the formula: \ {d['speed_formula']:.1f} m/s", font_size=28, color=GOOD)
        meas.next_to(VGroup(law, units), DOWN, buff=0.5).set_x(0)
        rope = StringView(width=9.0, scale=1.0).move_to(UP * 2.7)
        tr = film(rope, d["right"])
        per = (len(d["right"]) - 1) / 2.0
        gates = VGroup(*[DashedLine(rope.p(f) + UP * 0.75, rope.p(f) + DOWN * 0.35, color=TIME, stroke_width=2,
                                    dash_length=0.08) for f in (0.35, 0.7)])
        gl = label(r"timed between two points", font_size=22, color=TIME).next_to(gates, DOWN, buff=0.12)
        VGroup(law, units).shift(DOWN * 1.5)
        meas.shift(DOWN * 1.35)
        bars.shift(DOWN * 0.75)
        with self.voiceover(
            "How fast does the bump go? Tighten the rope and it goes faster. Use a heavier rope and it goes slower. "
            "<bookmark mark='a'/> The speed turns out to be the square root of the tension over the mass per metre, "
            "<bookmark mark='b'/> which at least has the right units. We will derive it in the next chapter. "
            f"<bookmark mark='c'/> On our monochord's string we timed a bump between two points: "
            f"{say(d['speed_measured'], 1)} metres a second, against {say(d['speed_formula'], 1)} from the formula."
        ) as vo:
            self.play(FadeIn(rope), FadeIn(gates), FadeIn(gl), run_time=0.5)
            self.play(tr.animate.set_value(0.6 * per), run_time=vo.until("a"), rate_func=linear)
            self.play(Write(law))
            vo.wait_until("b")
            self.play(FadeIn(units))
            vo.wait_until("c")
            tr.set_value(0)
            self.play(tr.animate.set_value(0.6 * per), FadeIn(meas), run_time=3.0, rate_func=linear)
        rope.clear_updaters()
        with self.voiceover(
            f"That is slower than sound in air. On a guitar's top string a wave runs at {say(g['guitar']['c'])} "
            "metres a second: faster than sound, on a wire a quarter of a millimetre thick."
        ):
            self.play(FadeOut(rope), FadeOut(gates), FadeOut(gl),
                      LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def round_trip(self):
        d = load("pulse")
        frames = d["split"]
        n = len(frames) - 1                      # one period
        s = StringView(width=10.4, scale=1.6).shift(UP * 1.4)
        tr = film(s, frames, loop=True)
        ends = VGroup(label(r"fixed", font_size=22, color=GREY_B).next_to(s.p(0.0), DOWN, buff=0.35),
                      label(r"fixed", font_size=22, color=GREY_B).next_to(s.p(1.0), DOWN, buff=0.35))
        span = VGroup(DoubleArrow(s.p(0.0) + DOWN * 1.5, s.p(1.0) + DOWN * 1.5, buff=0, color=RATIO, stroke_width=3,
                                  tip_length=0.18),
                      MathTex(r"L", font_size=40, color=RATIO).move_to(s.p(0.5) + DOWN * 1.85))
        with self.voiceover(
            "Now the string of an instrument: short, tight, and fixed at both ends. Pull a bump into it and let go. "
            "<bookmark mark='a'/> The bump splits into two halves that run opposite ways. Each one reaches its end, "
            "flips, and comes back. <bookmark mark='b'/> They cross in the middle, flip again at the far ends, "
            "<bookmark mark='c'/> and arrive home at the same moment, the right way up. The string is exactly as it "
            "started, and it all happens again."
        ) as vo:
            self.play(FadeIn(s), FadeIn(ends))
            vo.wait_until("a")
            self.play(tr.animate.set_value(0.4 * n), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(0.8 * n), run_time=vo.until("c"), rate_func=linear)
            self.play(tr.animate.set_value(1.0 * n), run_time=max(vo.remaining() - 0.3, 2.0), rate_func=linear)
        eq = MathTex(r"\text{time for one round trip}", r"=", r"\frac{2L}{c}", font_size=44).move_to(DOWN * 1.2)
        eq[2].set_color(TIME)
        eq2 = MathTex(r"f", r"=", r"\frac{c}{2L}", r"=", r"\frac{1}{2L}\sqrt{\frac{T}{\mu}}", font_size=52)
        eq2.move_to(DOWN * 2.6)
        eq2[0].set_color(FREQ), eq2[4].set_color(GOOD)
        box = SurroundingRectangle(eq2[4], color=GOOD, buff=0.15, corner_radius=0.1, stroke_width=2)
        with self.voiceover(
            "How long did that take? Each half travelled the length of the string twice, <bookmark mark='a'/> so one "
            "cycle takes two L over c. <bookmark mark='b'/> The frequency is one over that: c over two L. Put in the "
            "speed, <bookmark mark='c'/> and there is Mersenne's law, with its one half. The half is the round trip."
        ) as vo:
            tr.set_value(0)
            self.play(FadeIn(span))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(eq2[:3]))
            vo.wait_until("c")
            self.play(FadeIn(eq2[3:]), Create(box))
        c = clip("pulse.bump")
        slow = 1.6 / (d["period_ms"] / 1000)      # one round trip every 1.6 seconds of film
        count = VGroup(label(rf"one round trip takes {d['round_trip_ms']:.2f} ms: \ "
                             rf"{1000 / d['round_trip_ms']:.1f} of them every second", font_size=28, color=TIME),
                       label(rf"the string is shown slowed {slow:.0f} times; \ the sound is at full speed", font_size=24,
                             color=GREY_A)).arrange(DOWN, buff=0.15).move_to(DOWN * 1.0)
        with self.voiceover(
            "So this is what the pitch of a string is. It is the number of round trips a wave makes along it each "
            f"second. On the monochord's open string a round trip takes {say(d['round_trip_ms'], 2)} thousandths of "
            f"a second, so there are {say(1000 / d['round_trip_ms'], 1)} of them a second. Here is that string, let "
            "go from this bump: the motion slowed down, the sound not."
        ) as vo:
            self.play(FadeOut(eq), FadeOut(span), FadeOut(eq2), FadeOut(box), FadeIn(count))
            turns = max(1, round(vo.remaining() / 2.4))
            self.play(tr.animate.set_value(turns * n), run_time=max(vo.remaining() - 0.1, 2.0), rate_func=linear)
        s.clear_updaters()
        with self.listen(c) as snd:
            window(snd, r"the string let go from a bump")
            snd.drive(s, s.film(frames, (d["period_ms"] / 1000) / n, slow=slow, loop=True))
        tr2 = film(s, frames, loop=True)
        with self.voiceover(
            "A string has a pitch because a wave on it keeps coming back. That is the idea. To make it exact, and to "
            "find where that speed comes from, we need the string's equation of motion."
        ) as vo:
            self.play(tr2.animate.set_value(3 * n), run_time=max(vo.remaining(), 2.0), rate_func=linear)
        s.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
