from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Unison(SoundScene):
    def construct(self):
        chapter(self, 6, r"Three strings for one note", r"Why does a piano note die away in two stages?", lit=(1877,), extra=((1977, r"Weinreich's coupled strings"),))
        self.puzzle()
        self.three()
        self.why()

    def graph(self):
        d = load("unison")
        g = axes([0, 6], [-62, 3], x_length=7.0, y_length=3.3, xlabel=r"seconds", ylabel=r"level at the bridge (dB)", xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[-60, -40, -20, 0], font_size=20)
        cols = {"one": GREY_A, "unison": AIR, "apart": TUNE}
        curves = {k: curve_from(g, d["t"], np.maximum(d[f"db_{k}"], -62), cols[k]) for k in cols}
        return d, g, curves, cols

    # ------------------------------------------------------------------
    def puzzle(self):
        strings = VGroup(*[Line(LEFT * 3.0, RIGHT * 3.0, color=STR, stroke_width=4) for _ in range(3)]).arrange(DOWN, buff=0.16).move_to(LEFT * 3.0 + UP * 1.5)
        ham = RoundedRectangle(width=0.4, height=1.0, corner_radius=0.15, stroke_width=0, fill_color=FELT, fill_opacity=1).move_to(strings.get_left() + RIGHT * 0.8 + DOWN * 1.0)
        bridge = Rectangle(width=0.16, height=1.0, stroke_width=0, fill_color=WOOD, fill_opacity=1).move_to(strings.get_right())
        names = VGroup(label(r"three strings, \ one hammer, \ one bridge", font_size=26, color=GREY_A).next_to(strings, UP, buff=0.3))
        facts = VGroup(label(r"most notes of a piano have three strings, \ tuned alike", font_size=28),
                       label(r"three strings are louder than one. \ That is not the whole reason.", font_size=28, color=GREY_A),
                       label(r"a piano note falls fast for a second, \ then lingers for ten", font_size=28, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 0.4 + DOWN * 1.9)
        with self.voiceover(
            "Open the lid of a piano and you find a third oddity. For most notes the hammer strikes not one "
            "string but three, tuned to the same pitch and passing over the same bridge. <bookmark mark='a'/> "
            "The obvious reason is loudness, and it is true as far as it goes. <bookmark mark='b'/> But it "
            "hides a puzzle. A piano has to do two things that pull against each other. A note must be loud, "
            "so the strings must give their energy to the soundboard quickly. And a note must sing, so the "
            "strings must keep their energy for a long time. Somehow a piano does both: every note falls "
            "away quickly for the first second or so, and then lingers. The answer was found in 1977, by "
            "Gabriel Weinreich."
        ) as vo:
            self.play(FadeIn(strings), FadeIn(bridge), FadeIn(ham), FadeIn(names), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(ham.animate(rate_func=there_and_back, run_time=0.5).shift(UP * 0.5), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d, g, curves, cols = self.graph()
        c = clip("unison.three")
        g.move_to(RIGHT * 2.9 + DOWN * 1.2)
        for cu in curves.values():
            cu.shift(RIGHT * 2.9 + DOWN * 1.2)
        q = listen_card(r"One note, \ three ways: \ one string; \ two strings in perfect unison; \ two strings one cent apart. \\ Which starts loudest? \ Which lasts longest?",
                        width=10.6, font_size=26).to_edge(UP, buff=0.35)
        tags = VGroup(label(r"1: \ one string", font_size=26, color=cols["one"]), label(r"2: \ two, \ in perfect unison", font_size=26, color=cols["unison"]),
                      label(r"3: \ two, \ a cent apart", font_size=26, color=cols["apart"])).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(LEFT * 4.3 + DOWN * 1.0)
        with self.voiceover(
            "Listen first. The same note three ways. One string alone. Then two strings in perfect unison. "
            "Then two strings tuned one cent apart, a hundredth of a semitone. Which starts loudest? And which "
            "lasts longest?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(tags))
        heads = {}
        for k, cu in curves.items():
            cu.set_stroke(opacity=0.0)
            self.add(cu)
            heads[k] = Dot(g.ax.c2p(0, 0), radius=0.09, color=cols[k]).set_opacity(0)
            self.add(heads[k])
        with self.listen(c) as snd:
            window(snd, r"one string; \ two in unison; \ two a cent apart", detail=r"model strings on a soundboard", corner=DL, tag_corner=DR)
            for k in ("one", "unison", "apart"):
                t0 = snd.time_of(k)
                db = d[f"db_{k}"]
                snd.drive(heads[k], lambda m, t, t0=t0, db=db: m.set_opacity(1.0 if t0 <= t < t0 + 4.2 else 0.0).move_to(
                    g.ax.c2p(float(np.clip(t - t0, 0, 4.2)), max(float(np.interp(np.clip(t - t0, 0, 4.2), d["t"], db)), -62))))
                snd.drive(curves[k], lambda m, t, t0=t0: m.set_stroke(opacity=1.0 if t >= t0 else 0.0))
        for k in curves:
            curves[k].set_stroke(opacity=1)
            heads[k].set_opacity(0)
        rows = {r["name"]: r for r in d["rows"]}
        with self.voiceover(
            "Two strings start louder than one, as you would expect. But in perfect unison the pair is gone "
            f"almost at once: after one second it is {say(abs(rows['unison']['at_1s']))} decibels down, where "
            f"the single string has fallen only {say(abs(rows['one']['at_1s']))}. <bookmark mark='a'/> The pair "
            "tuned a cent apart does something neither of the others does. It drops just as fast at first, dips, "
            f"and then comes back and settles into a slow decay: about {say(abs(d['late_db_s']))} decibels a "
            f"second instead of {say(abs(d['early_db_s']))}. After five seconds it is by far the loudest of the "
            "three. That is the piano's two-stage decay, from nothing but a hundredth of a semitone."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(Indicate(curves["apart"], color=WHITE, scale_factor=1.0), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        card = history_card(1977, r"Gabriel Weinreich, \ ``Coupled piano strings''", r"the strings of one note are not independent: they talk to each other through the bridge.", width=5.4, font_size=20).to_corner(UL, buff=0.4)

        def pair(up2, col, at):
            s1 = VMobject(stroke_color=STR, stroke_width=4).set_points_smoothly([at + LEFT * 1.8, at + UP * 0.35, at + RIGHT * 1.8])
            s2 = VMobject(stroke_color=STR, stroke_width=4).set_points_smoothly([at + LEFT * 1.8 + DOWN * 0.9, at + DOWN * 0.9 + UP * 0.35 * up2, at + RIGHT * 1.8 + DOWN * 0.9])
            br = Rectangle(width=0.14, height=1.3, stroke_width=0, fill_color=WOOD, fill_opacity=1).move_to(at + RIGHT * 1.8 + DOWN * 0.45)
            return VGroup(s1, s2, br)

        a = pair(1, GOOD, LEFT * 1.6 + UP * 1.0)
        b = pair(-1, BAD, LEFT * 1.6 + DOWN * 1.3)
        la = VGroup(label(r"moving together:", font_size=26, color=TUNE), label(r"both push the bridge at once.", font_size=24, color=GREY_A),
                    label(r"Loud, \ and over twice as fast.", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(a, RIGHT, buff=0.4)
        lb = VGroup(label(r"moving oppositely:", font_size=26, color=AIR), label(r"their pushes cancel; \ the bridge stays still.", font_size=24, color=GREY_A),
                    label(r"Quiet, \ and it rings on.", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(b, RIGHT, buff=0.4)
        end = VGroup(label(r"the hammer starts them together; \ a cent of mistuning lets them drift apart", font_size=26, color=GOOD),
                     label(r"a tuner's unison is never quite perfect, \ on purpose", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Weinreich's explanation is one idea. The strings of a note are not independent. They share a "
            "bridge, and the bridge moves a little. <bookmark mark='a'/> If two strings move together, up and "
            "down in step, both push on the bridge at once. The bridge moves twice as far, the soundboard gets "
            "a loud sound, and the strings lose their energy twice as fast. <bookmark mark='b'/> If the two "
            "strings move oppositely, one up while the other is down, their pushes cancel. The bridge hardly "
            "moves. Almost nothing reaches the soundboard, and so the strings keep their energy and ring on. "
            "<bookmark mark='c'/> The hammer starts the strings moving together: that is the loud, fast "
            "beginning. If they are perfectly in tune they stay together, and the note simply dies. But tune "
            "them a hair apart, and they slowly slide out of step into the opposite motion, the one that "
            "lasts. That is the singing tail. A piano tuner leaves a unison very slightly imperfect, and "
            "chooses how imperfect by listening to how the note dies. And the soft pedal on a grand shifts the "
            "hammers sideways to strike two strings instead of three: the third string, left unstruck, is "
            "pulled into the opposite motion at once, and the note is not just quieter. It sings longer."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(end[0]))
            self.wait(max(vo.remaining() - 16.0, 0.1))
            self.play(FadeIn(end[1]))
        self.wait(0.3)
        self.clear_scene()
