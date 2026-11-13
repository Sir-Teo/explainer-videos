from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (BAD, FORCE, FREQ, GOOD, HIST, LEVEL, PART, RATIO, STR, TIME, TUNE, clip, load,
                                        ring, say, window)


class RealStrings(SoundScene):
    def construct(self):
        self.card()
        self.never_stops()
        self.decay()
        self.stiffness()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Real strings", r"What does a real string do that the ideal one cannot?",
                            lit=(1877,), part=PART)
        with self.voiceover("Chapter eleven. Real strings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def never_stops(self):
        ideal, real = clip("real.ideal"), clip("real.damped")
        a = Spectrogram(ideal, width=5.6, height=3.4, fmax=4000.0, marks=[(1000, "1 kHz"), (3000, "3 kHz")])
        b = Spectrogram(real, width=5.6, height=3.4, fmax=4000.0, marks=[(1000, "1 kHz"), (3000, "3 kHz")])
        a.move_to(LEFT * 3.3 + DOWN * 0.3)
        b.move_to(RIGHT * 3.6 + DOWN * 0.3)
        a.playhead.set_opacity(0), b.playhead.set_opacity(0)
        ta = label(r"the ideal string", font_size=30, color=STR).next_to(a.frame, UP, buff=0.25)
        tb = label(r"the same string, \ with losses", font_size=30, color=TUNE).next_to(b.frame, UP, buff=0.25)
        with self.voiceover(
            "Everything so far was about an ideal string, and the ideal string has a flaw you can hear at once. "
            "Here it is, plucked: the wave equation and nothing else."
        ):
            self.play(FadeIn(a), FadeIn(ta))
        with self.listen(ideal) as snd:
            window(snd, r"the ideal string", detail=r"no losses")
            a.playhead.set_opacity(1)
            snd.drive(a.playhead, a.follow())
        a.playhead.set_opacity(0)
        with self.voiceover(
            "It never dies away. Every partial rings for ever at full strength, and it sounds like a buzzer, not an "
            "instrument. Now the string we have actually been using."
        ):
            self.play(FadeIn(b), FadeIn(tb))
        with self.listen(real) as snd:
            window(snd, r"with losses")
            b.playhead.set_opacity(1)
            snd.drive(b.playhead, b.follow())
        b.playhead.set_opacity(0)
        where = VGroup(label(r"where the energy goes", font_size=26, color=GREY_B),
                       label(r"into the air it pushes aside", font_size=26),
                       label(r"into heat, inside the wire", font_size=26),
                       label(r"through the bridge, into the box: \ that part is the sound", font_size=26, color=TUNE)
                       ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A real string loses energy three ways: to the air it pushes, to friction inside the wire, "
            "<bookmark mark='a'/> and through the bridge into the body of the instrument. That last loss is not a "
            "defect. It is the sound. A string that kept all its energy would be silent."
        ) as vo:
            self.play(Group(a, ta, b, tb).animate.shift(UP * 0.5), FadeIn(where[:3]))
            vo.wait_until("a")
            self.play(FadeIn(where[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        d = load("real")
        rows = d["rows"]
        eq = MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"c^2 \frac{\partial^2 u}{\partial x^2}",
                     r"\;-\; 2\sigma_0 \frac{\partial u}{\partial t}",
                     r"\;+\; 2\sigma_1 \frac{\partial^3 u}{\partial t\, \partial x^2}", font_size=40).to_edge(UP, buff=0.45)
        eq[3].set_color(LEVEL), eq[4].set_color(FORCE)
        notes = VGroup(label(r"a brake on all motion alike", font_size=24, color=LEVEL).next_to(eq[3], DOWN, buff=0.2),
                       label(r"a brake on sharp bends", font_size=24, color=FORCE).next_to(eq[4], DOWN, buff=0.2))
        notes[0].shift(LEFT * 1.3)
        notes[1].shift(RIGHT * 1.0)
        ymax = max(r["decay_model"] for r in rows) * 1.12
        g = axes([0.5, 12.5], [0, ymax], x_length=6.6, y_length=3.4, xlabel=r"partial", ylabel=r"decay rate (per second)",
                 xticks=[1, 4, 8, 12], yticks=[0, 2, 4], font_size=20)
        g.move_to(LEFT * 3.0 + DOWN * 1.2)
        line = curve(g.ax, [r["n"] for r in rows], [r["decay_model"] for r in rows], FORCE, stroke_width=2.5)
        # the first term alone: the same rate for every mode (sigma_0, read off the model's first two values)
        sigma0 = rows[0]["decay_model"] - (rows[1]["decay_model"] - rows[0]["decay_model"]) / 3
        flat = DashedLine(g.ax.c2p(1, sigma0), g.ax.c2p(12, sigma0), color=LEVEL, stroke_width=2.5, dash_length=0.12)
        pts = VGroup(*[Dot(g.ax.c2p(r["n"], r["decay_measured"]), radius=0.07, color=TUNE) for r in rows])
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=FORCE, stroke_width=3),
                            label(r"the model: \ $\sigma_0 + \sigma_1 (n\pi/L)^2$", font_size=24, color=FORCE)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.07, color=TUNE),
                            label(r"measured on the simulated string", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.15)
                     ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.7 + UP * 0.2)
        t60 = VGroup(label(r"time to fall by 60 decibels", font_size=24, color=GREY_B),
                     label(rf"partial 1: \ {rows[0]['t60']:.1f} seconds", font_size=28, color=harmonic_color(1)),
                     label(rf"partial 12: \ {rows[11]['t60']:.1f} seconds", font_size=28, color=harmonic_color(12))
                     ).arrange(DOWN, buff=0.15).move_to(RIGHT * 3.7 + DOWN * 1.7)
        with self.voiceover(
            "In the equation, loss is two extra terms. <bookmark mark='a'/> One brakes all motion alike. "
            "<bookmark mark='b'/> The other brakes sharp bends harder than gentle ones, so it takes more from the "
            "high modes, which are all bends. Each mode then dies away at its own steady rate."
        ) as vo:
            self.play(FadeIn(eq[:3]), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(eq[3]), FadeIn(notes[0]), Create(flat))
            vo.wait_until("b")
            self.play(FadeIn(eq[4]), FadeIn(notes[1]))
            self.play(ReplacementTransform(flat.copy().set_opacity(0.0), line), run_time=1.6)
        with self.voiceover(
            "Here is that rate for the first twelve partials: the curve from the equation, "
            "<bookmark mark='a'/> and the points measured on the bead simulation. They agree to within "
            f"{say(100 * d['decay_worst_rel'], 1)} percent. <bookmark mark='b'/> The fundamental needs "
            f"{say(rows[0]['t60'], 1)} seconds to fall by sixty decibels; the twelfth partial, "
            f"{say(rows[11]['t60'], 1)}. That is what you saw in the spectrogram: a note that starts bright and "
            "ends as almost a pure tone."
        ) as vo:
            self.play(FadeIn(leg[0]), Indicate(line, color=FORCE, scale_factor=1.03))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.08), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(t60))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stiffness(self):
        d = load("real")
        rows = d["rows"]
        c = clip("real.stiff")
        eq = MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"c^2 \frac{\partial^2 u}{\partial x^2}",
                     r"\;-\; \kappa^2 \frac{\partial^4 u}{\partial x^4}", font_size=40).move_to(LEFT * 3.6 + UP * 2.8)
        eq[3].set_color(BAD)
        res = MathTex(r"f_n", r"=", r"n f_1", r"\sqrt{1 + B n^2}", font_size=44).move_to(RIGHT * 3.4 + UP * 2.8)
        res[3].set_color(BAD)
        ymax = rows[11]["sharp_cents_stiff"] * 1.1
        g = axes([0.5, 12.5], [0, ymax], x_length=6.6, y_length=3.3, xlabel=r"partial", font_size=20,
                 ylabel=r"how sharp it is of a true harmonic (cents)", xticks=[1, 4, 8, 12], yticks=[0, 100, 200])
        g.move_to(LEFT * 2.9 + DOWN * 1.2)
        thin = curve(g.ax, [r["n"] for r in rows], [r["sharp_cents"] for r in rows], TUNE, stroke_width=3)
        thick = curve(g.ax, [r["n"] for r in rows], [r["sharp_cents_stiff"] for r in rows], BAD, stroke_width=3)
        leg = VGroup(
            label(rf"our wire, {d['wire_mm']} mm: \ partial 12 is {rows[11]['sharp_cents']:.0f} cents sharp", font_size=24, color=TUNE),
            label(rf"a wire six times as stiff: \ {rows[11]['sharp_cents_stiff']:.0f} cents", font_size=24, color=BAD),
            label(r"(100 cents is a semitone)", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.9 + DOWN * 0.6)
        with self.voiceover(
            "The second thing a real string has is stiffness. A wire is not perfectly limp. It resists being bent, "
            "like a very thin ruler. <bookmark mark='a'/> That adds a restoring force of its own, a term with four "
            "derivatives, which hardly matters for a gentle curve and matters a great deal for a tight one. "
            "<bookmark mark='b'/> The effect is that the upper modes come out sharp. The partials are no longer "
            "exactly one, two, three times the fundamental. They are stretched."
        ) as vo:
            from explainer.music.monochord.physics import pluck_shape
            xs = np.linspace(0, 1, 161)
            limp = pluck_shape(xs, 1.0, 0.3, 1.0)
            kern = np.exp(-0.5 * (np.linspace(-1, 1, 41) / 0.45) ** 2)
            stiff_shape = np.convolve(np.pad(limp, 20, mode="edge"), kern / kern.sum(), mode="valid")
            va = StringView(width=5.4, scale=1.3).move_to(LEFT * 3.4 + DOWN * 1.1)
            vb = StringView(width=5.4, scale=1.3, color=BAD).move_to(RIGHT * 3.4 + DOWN * 1.1)
            va.set_shape(limp)
            vb.set_shape(stiff_shape * np.sin(np.pi * xs) ** 0.05)
            la = label(r"a perfectly limp string: \ a sharp corner costs nothing", font_size=24, color=GREY_A).next_to(va, DOWN, buff=0.3)
            lb = label(r"a stiff wire: \ it will not take the corner", font_size=24, color=BAD).next_to(vb, DOWN, buff=0.3)
            self.play(FadeIn(eq[:3]), FadeIn(va), FadeIn(la), FadeIn(vb), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(eq[3]))
            vo.wait_until("b")
            self.play(Write(res))
        self.play(FadeOut(va), FadeOut(vb), FadeOut(la), FadeOut(lb), run_time=0.4)
        with self.voiceover(
            f"On our half-millimetre wire the stretch is small: by the twelfth partial, {say(rows[11]['sharp_cents'])} "
            "cents. <bookmark mark='a'/> Make the wire six times stiffer, as if it were a thin rod, and the twelfth "
            f"partial is {say(rows[11]['sharp_cents_stiff'])} cents sharp: more than two semitones. Listen to what "
            "that does to a pluck."
        ) as vo:
            self.play(FadeIn(g), Create(thin), FadeIn(leg[0]), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(thick), FadeIn(leg[1]))
        with self.listen(c) as snd:
            window(snd, r"a wire six times as stiff")
            head = Line(g.ax.c2p(0.5, 0), g.ax.c2p(0.5, ymax), color=WHITE, stroke_width=1.5)
            snd.show(head)
            snd.drive(head, lambda m, t: m.set_x(g.ax.c2p(0.5 + 12 * min(t / c.duration, 1.0), 0)[0]))
        payoff = VGroup(label(r"where this comes back", font_size=22, color=GREY_B),
                        label(r"Part 6: \ why a piano's octaves are tuned wide", font_size=24, color=TUNE),
                        label(r"Part 7: \ the piano's string", font_size=24, color=TUNE),
                        label(r"Part 9: \ no tension at all: \ a bar", font_size=24, color=TUNE)
                        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 2.4)
        with self.voiceover(
            "It no longer sounds quite like a string. It is on the way to a bell, or a struck bar. A piano's bass "
            "strings are short and thick, so they are stiff, and this stretched ladder of partials is a large part "
            "of what makes a piano sound like a piano. <bookmark mark='a'/> Losses and stiffness change the modes, "
            "but they leave one thing alone: the modes still do not talk to each other. In the last chapter of this "
            "part's physics, that fails too."
        ) as vo:
            self.play(FadeIn(payoff))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
