from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


def pipe_outline(x0, x1, y, fn, half=0.5, color=GREY_B) -> VGroup:
    """The walls of a pipe whose half-height at the fraction s of its length is ``half * fn(s)``."""
    s = np.linspace(0, 1, 200)
    top = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners([[x0 + (x1 - x0) * v, y + half * fn(v), 0] for v in s])
    bot = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners([[x0 + (x1 - x0) * v, y - half * fn(v), 0] for v in s])
    return VGroup(top, bot)


class Impedance(SoundScene):
    def construct(self):
        chapter(self, 10, r"Why a string needs a box", r"What happens when sound meets a change?", lit=(1877,))
        self.step()
        self.water()
        self.horn()

    # ------------------------------------------------------------------
    def step(self):
        d = load("impedance")
        x0, x1, y = -5.8, 5.8, 0.9
        walls = pipe_outline(x0, x1, y, lambda s: 0.5 if s < 0.5 else 1.0, half=0.8)
        tr_ = Trace([x0, y, 0], [x1, y, 0], scale=0.55 / float(np.abs(d["step_frames"]).max()), color=FORCE)
        tr = film(tr_, d["step_frames"])
        zdef = definition_card(r"Impedance",
                               r"how hard the air must be pushed to make it move: \ pressure divided by flow. \ "
                               r"In open air it is $\rho c \approx %.0f$ in SI units; \ in a pipe, \ $\rho c$ divided by "
                               r"the pipe's area." % d["z_air"], width=11.0, font_size=26).to_edge(DOWN, buff=0.35)
        res = VGroup(label(r"comes back: \ $\dfrac{S_1 - S_2}{S_1 + S_2} = %.2f$" % d["r_formula"], font_size=28, color=GREY_A),
                     label(r"in the simulation: \ $%.2f$" % d["r_sim"], font_size=28, color=TUNE)).arrange(RIGHT, buff=0.9)
        res.move_to(DOWN * 0.75)
        with self.voiceover(
            "Part 1 ended on a puzzle: a string on its own is almost silent. The reason is the same reason a pulse "
            "came back from the open end of a pipe. <bookmark mark='a'/> Watch a pulse of pressure travel down a "
            "narrow pipe that suddenly becomes four times as wide. <bookmark mark='b'/> Part goes on. Part comes "
            "back, upside down. Nothing was in the way. The pulse met a change in how hard the air is to push, and "
            f"that is enough. <bookmark mark='c'/> The quantity that changed is called impedance: the pressure it "
            "takes to produce a given flow. Wherever the impedance changes, some of the wave is turned back, "
            "<bookmark mark='d'/> and how much is a simple formula, which the simulation confirms."
        ) as vo:
            head = label(r"a pulse of pressure in a pipe that suddenly becomes four times as wide", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
            bare = StringView(width=3.0, scale=0.4, stroke_width=3).move_to(DOWN * 1.6)
            lens = Lens(bare.p(0), bare.p(1), amp=0.16, color=TUNE)
            btag = label(r"Part 1's puzzle: \ a string on its own is almost silent", font_size=26, color=GREY_B).next_to(bare, DOWN, buff=0.4)
            self.play(FadeIn(walls), FadeIn(tr_), FadeIn(bare), FadeIn(lens), FadeIn(btag))
            vo.wait_until("a")
            self.play(FadeOut(bare), FadeOut(lens), FadeOut(btag), FadeIn(head), run_time=0.4)
            self.play(tr.animate.set_value(len(d["step_frames"]) - 1), run_time=max(vo.until("c") - 0.2, 5.0), rate_func=linear)
            self.play(FadeIn(zdef))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def water(self):
        d = load("impedance")
        sea = Rectangle(width=13.0, height=2.6, stroke_width=0, fill_color="#1D4E89", fill_opacity=0.55).move_to(DOWN * 2.4)
        surf = Line(LEFT * 6.5 + DOWN * 1.1, RIGHT * 6.5 + DOWN * 1.1, color=AIR, stroke_width=2)
        za = VGroup(label(r"air", font_size=34, color=AIR), MathTex(r"\rho c = %.0f" % d["z_air"], font_size=38)).arrange(RIGHT, buff=0.4).move_to(LEFT * 4.0 + UP * 0.2)
        zw = VGroup(label(r"water", font_size=34, color="#7FB3FF"), MathTex(r"\rho c = %s" % f"{d['z_water']:,.0f}".replace(",", "{,}"), font_size=38)
                    ).arrange(RIGHT, buff=0.4).move_to(LEFT * 3.6 + DOWN * 2.2)
        a_in = Arrow(RIGHT * 1.0 + UP * 2.4, RIGHT * 2.4 + DOWN * 1.0, color=FORCE, stroke_width=6, buff=0)
        a_back = Arrow(RIGHT * 2.6 + DOWN * 1.0, RIGHT * 4.0 + UP * 2.4, color=FORCE, stroke_width=6, buff=0)
        a_thru = Arrow(RIGHT * 2.5 + DOWN * 1.2, RIGHT * 3.0 + DOWN * 2.6, color=FORCE, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.12)
        t_back = label(rf"{100 * (1 - d['through_water']):.1f}\% comes back", font_size=28, color=GREY_A).next_to(a_back, RIGHT, buff=0.1)
        t_thru = label(rf"{100 * d['through_water']:.2f}\% goes in: \ ${d['through_water_db']:.0f}$ dB", font_size=28, color=TUNE).next_to(a_thru, RIGHT, buff=0.3)
        head = label(r"sound in air, \ meeting water", font_size=32, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Now the extreme case. Sound in air arrives at the surface of water. Water is eight hundred times as "
            "dense and far stiffer: its impedance is three and a half thousand times that of air. "
            f"<bookmark mark='a'/> Only about a thousandth of the energy gets in. The rest bounces off. That is why "
            "you cannot hear the poolside from under water, and it is a problem your own ear has to solve, because "
            "the inner ear is full of fluid. <bookmark mark='b'/> A string has the same problem the other way round. "
            "It is thin, dense and stiff; the air is light and soft. The string swings, and the air just slips "
            "round it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sea), FadeIn(surf), FadeIn(za), FadeIn(zw), GrowArrow(a_in))
            vo.wait_until("a")
            self.play(GrowArrow(a_back), GrowArrow(a_thru), FadeIn(t_back), FadeIn(t_thru))
            vo.wait_until("b")
            s = StringView(width=3.4, scale=0.5, stroke_width=3).move_to(LEFT * 3.6 + UP * 2.2)
            tag = label(r"a bare string: \ little air moved", font_size=24, color=GREY_B).next_to(s, DOWN, buff=0.45)
            lens = Lens(s.p(0), s.p(1), amp=0.18, color=TUNE)
            self.play(FadeIn(s), FadeIn(lens), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def horn(self):
        d = load("impedance")
        x0, x1 = -5.8, 5.8
        y1, y2 = 1.9, -1.1

        def sudden(s):
            return 0.25 if s < 2.0 / 6.0 else 1.0

        def flare(s):
            x = 6.0 * s
            return 0.25 if x < 1.5 else (1.0 if x > 2.5 else 0.25 * 4.0 ** (x - 1.5))

        w1, w2 = pipe_outline(x0, x1, y1, sudden, half=0.8), pipe_outline(x0, x1, y2, flare, half=0.8)
        top = float(max(np.abs(d["frames_sudden"]).max(), np.abs(d["frames_horn"]).max()))
        t1 = Trace([x0, y1, 0], [x1, y1, 0], scale=0.6 / top, color=FORCE)
        t2 = Trace([x0, y2, 0], [x1, y2, 0], scale=0.6 / top, color=FORCE)
        tr = ValueTracker(0.0)
        n = len(d["frames_sudden"])

        def upd(tv, frames):
            def f(m):
                v = min(max(tr.get_value(), 0.0), n - 1.000001)
                i = int(v)
                a = v - i
                tv.set_shape((1 - a) * frames[i] + a * frames[i + 1])
            return f

        t1.add_updater(upd(t1, d["frames_sudden"]))
        t2.add_updater(upd(t2, d["frames_horn"]))
        tags = VGroup(label(r"a sudden opening", font_size=26, color=GREY_A).next_to(w1, UP, buff=0.1).align_to(w1, LEFT),
                      label(r"the same opening, \ through a flare one metre long", font_size=26, color=GREY_A).next_to(w2, UP, buff=0.1).align_to(w2, LEFT))
        res = VGroup(label(rf"{100 * d['sudden']:.0f}\% of the energy gets out \ (formula: {100 * d['sudden_formula']:.0f}\%)", font_size=26, color=BAD
                           ).next_to(w1, DOWN, buff=0.12).align_to(w1, RIGHT),
                     label(rf"{100 * d['horn']:.0f}\% gets out: \ ${d['gain_db']:+.1f}$ dB", font_size=26, color=GOOD).next_to(w2, DOWN, buff=0.12).align_to(w2, RIGHT))
        with self.voiceover(
            "The cure is to make the change gradual. Here is a narrow pipe opening into one sixteen times its "
            "area: on top suddenly, below through a flare a metre long. The same pulse goes down both. "
            f"<bookmark mark='a'/> From the sudden opening, {say(100 * d['sudden'])} percent of the energy gets out. "
            f"Through the flare, {say(100 * d['horn'])} percent. <bookmark mark='b'/> That is what the bell of a "
            "trumpet is for, and a megaphone, and the horn of an old gramophone. And it is what the box of the "
            "monochord does for the string: a wide wooden plate, driven through the bridge, is a far better match to "
            "the air than a wire is. A musical instrument is two things. Something that vibrates, and something "
            "that hands the vibration to the air."
        ) as vo:
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(tags), FadeIn(t1), FadeIn(t2))
            self.play(tr.animate.set_value(n - 1), run_time=max(vo.until("a") + 3.0, 6.0), rate_func=linear)
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
        t1.clear_updaters(), t2.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
