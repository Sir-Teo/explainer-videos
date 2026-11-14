from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


def cross(center, size=0.22, color=WHITE):
    c = np.asarray(center, float)
    return VGroup(Line(c + LEFT * size, c + RIGHT * size, color=color, stroke_width=6),
                  Line(c + UP * size, c + DOWN * size, color=color, stroke_width=6))


class Blind(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.find()
        self.filling()
        self.measure()

    def card(self):
        card = chapter_card(6, r"On you: \ find your blind spot", r"Where is the hole in your field of view?",
                            lit=(), part=PART, scale=("brain", "mind"), marr=("what", "tissue"))
        with self.voiceover(
            "Chapter six. On you: find your blind spot."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def why(self):
        b = load("blindspot")
        head = heading(r"Each eye has a patch with no receptors")
        c0 = np.array([-3.6, -0.3, 0])
        eye = Circle(radius=2.1, color=VOLT, stroke_width=4).move_to(c0)
        lens = Ellipse(width=0.5, height=1.3, color=PARIETAL, stroke_width=3, fill_color=PARIETAL,
                       fill_opacity=0.35).move_to(c0 + LEFT * 1.85)
        retina = Arc(radius=2.0, start_angle=-PI * 0.42, angle=PI * 0.84, color=FRONTAL, stroke_width=8).move_arc_center_to(c0)
        fovea = Dot(c0 + RIGHT * 2.0, radius=0.1, color=THRESH)
        a = np.radians(-17)
        disc = c0 + 2.0 * np.array([np.cos(a), np.sin(a), 0])
        hole = Dot(disc, radius=0.17, color=BACKGROUND)
        nerve = Line(disc, disc + np.array([1.7, -0.75, 0]), color=DATA, stroke_width=10)
        labels = VGroup(
            label(r"the receptors line the back", font_size=22, color=FRONTAL).next_to(retina, UP, buff=0.2).shift(
                RIGHT * 0.6),
            label(r"centre of gaze", font_size=22, color=THRESH).next_to(fovea, RIGHT, buff=0.15),
            label(r"the nerve leaves here: \ no receptors", font_size=22, color=DATA).next_to(nerve.get_end(), DOWN,
                                                                                         buff=0.1),
        )
        keep_in_frame(labels)
        rows = VGroup(
            wrapped_label(rf"about {b['centre_deg']:.0f} degrees to the side of where you look, \ toward your "
                          r"temple", 5.0, 28, WHITE),
            wrapped_label(rf"about {b['width_deg']:.1f} degrees across: \ room for eleven full moons side by side",
                          5.0, 28, THRESH),
            wrapped_label(r"one in each eye, \ and you have never noticed either", 5.0, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([4.0, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"schematic: the right eye, seen from above").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now an experiment on you, and it starts with a design flaw. The light-sensitive cells line the "
            "back of your eye. Their fibres have to get out of the eye to reach the brain. "
            "<bookmark mark='a'/> They gather at one spot and leave together as the optic nerve. At that "
            "spot there's no room for receptors. So each of your eyes has a patch that sees nothing at all. "
            f"<bookmark mark='b'/> It sits about {b['centre_deg']:.0f} degrees to the side of where you're "
            "looking, toward your temple. <bookmark mark='c'/> And it isn't small. It's about five and a "
            "half degrees across. The full moon is half a degree. You could line up eleven full moons inside "
            "your blind spot. <bookmark mark='d'/> You have one in each eye, you've had them all your life, "
            "and you've never noticed either. Let's find one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(eye, lens, retina, fovea)), FadeIn(labels[0]),
                      FadeIn(labels[1]))
            vo.wait_until("a")
            self.play(FadeIn(hole), Create(nerve), FadeIn(labels[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def find(self):
        b = load("blindspot")
        stage = demo_stage(13.6, 6.6, tag=r"On you: \ the blind spot of your right eye", center=[0, -0.25, 0])
        c = stage.box.get_center()
        fix = cross(c + np.array([-4.0, 0.6, 0]))
        dot = Dot(c + np.array([4.0, 0.6, 0]), radius=0.2, color=THRESH)
        screens = 8.0 / config.frame_width * b["distance_per_separation"]
        steps = VGroup(
            label(r"1. \ Close your left eye.", font_size=28, color=WHITE),
            label(r"2. \ Look at the cross. \ Keep looking at it.", font_size=28, color=WHITE),
            label(rf"3. \ Move closer or further: \ about {screens:.0f} screen-widths away, the dot vanishes.",
                  font_size=28, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(c + np.array([0, -1.9, 0]))
        ring = countdown_ring(0.45).move_to(c + np.array([6.0, 2.55, 0]))
        with self.voiceover(
            "Close your left eye. <bookmark mark='a'/> With your right eye, look at the cross on the left, "
            "and keep looking at it. Don't look at the dot. You can see the dot anyway, out of the corner "
            "of your eye. <bookmark mark='b'/> Now slowly move your head toward the screen, or away from "
            f"it. Somewhere around {screens:.0f} screen-widths away, the dot will disappear. Not dim. Not "
            "blurred. Gone. Take a few seconds to find the distance. <bookmark mark='c'/> When you've found "
            "it, move a little closer or a little further, and the dot comes back. Its image has just "
            "crossed the patch of your retina where the nerve leaves."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(fix), FadeIn(dot), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), FadeIn(ring))
            self.play(ring.t.animate.set_value(0.0), run_time=9.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeOut(ring))
        self.wait(2.0)
        self.clear_scene()

    def filling(self):
        stage = demo_stage(13.6, 6.6, tag=r"On you: \ what is in the hole?", center=[0, -0.25, 0])
        c = stage.box.get_center()
        fix = cross(c + np.array([-4.0, 0.6, 0]))
        y = c[1] + 0.6
        left = Line([c[0] + 1.6, y, 0], [c[0] + 3.55, y, 0], color=THRESH, stroke_width=10)
        right = Line([c[0] + 4.45, y, 0], [c[0] + 6.3, y, 0], color=THRESH, stroke_width=10)
        gap_l = label(r"a gap in the line", font_size=22, color=GREY_B).next_to([c[0] + 4.0, y, 0], UP, buff=0.35)
        rows = VGroup(
            label(r"Same eye, same cross, same distance.", font_size=28, color=WHITE),
            label(r"The gap falls in your blind spot. \ Is the line broken?", font_size=28, color=WHITE),
            wrapped_label(r"Most people see an unbroken line. \ You do not see a hole: \ you see what surrounds "
                          r"it, carried across.", 12.0, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(c + np.array([0, -1.85, 0]))
        with self.voiceover(
            "Here's the part that should bother you. Same eye, same cross, same distance. "
            "<bookmark mark='a'/> Where the dot was, there's now a line with a gap in it, and the gap is "
            "sitting in your blind spot. Look at the cross, and ask yourself whether the line is broken. "
            "<bookmark mark='b'/> Most people see an unbroken line. The gap is on the screen, and it isn't "
            "in what you see. <bookmark mark='c'/> So the hole in your field of view doesn't look like a "
            "hole. It doesn't look black, and it doesn't look like anything. Your visual system carries "
            "across whatever surrounds it, a line, a colour, a pattern, and hands you a finished picture. "
            "You can't see what you're missing. That will matter in a few minutes, when we meet people who "
            "have lost half the world and don't know it. And it's the first hint of Part 14: what you see is "
            "something your brain concludes."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(fix), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(left), Create(right), FadeIn(gap_l), FadeIn(rows[1]))
            self.wait(4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
            vo.wait_until("c")
        self.clear_scene()

    def measure(self):
        b = load("blindspot")
        head = heading(r"The geometry, \ and a way to measure yours")
        eye = Dot([-6.2, -2.0, 0], radius=0.14, color=VOLT)
        d = 6.6
        sx = -6.2 + d
        screen = Line([sx, -2.7, 0], [sx, 1.6, 0], color=GREY_B, stroke_width=5)
        fix_pt = np.array([sx, -2.0, 0])
        near, far = fix_pt + UP * d * b["near"], fix_pt + UP * d * b["far"]
        rays = VGroup(Line(eye.get_center(), fix_pt, color=GREY_C, stroke_width=2),
                      Line(eye.get_center(), near, color=THRESH, stroke_width=2),
                      Line(eye.get_center(), far, color=THRESH, stroke_width=2))
        spot = Line(near, far, color=LESION, stroke_width=12)
        marks = VGroup(label(r"your eye", font_size=26, color=VOLT).next_to(eye, DOWN, buff=0.12),
                       label(r"the cross", font_size=26, color=GREY_A).next_to(fix_pt, RIGHT, buff=0.15),
                       label(r"the blind spot", font_size=26, color=LESION).next_to(spot, RIGHT, buff=0.15),
                       label(r"distance $d$", font_size=26, color=GREY_A).move_to([-6.2 + d / 2, -2.4, 0]),
                       label(r"the screen, from the side", font_size=24, color=GREY_B).next_to(screen, UP, buff=0.1))
        side = VGroup(
            label(r"offset $= d \tan(\mathrm{angle})$", font_size=38, color=MODEL),
            wrapped_label(rf"centre: \ ${b['centre']:.2f}\,d$ from the cross", 4.6, 30, WHITE),
            wrapped_label(rf"width: \ about ${b['width']:.2f}\,d$", 4.6, 30, WHITE),
            wrapped_label(rf"at 57 cm, where a degree is a centimetre: \ {b['at_57_centre']:.0f} cm out, "
                          rf"{b['at_57']:.0f} cm wide", 4.6, 30, THRESH),
            wrapped_label(r"This part's interactive measures your own, \ with a moving dot and two key presses.",
                          4.6, 29, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.55, -0.3, 0])
        keep_in_frame(side)
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "You can turn that into a measurement with one line of trigonometry. <bookmark mark='a'/> Your "
            "eye, the cross, and the screen seen from the side. A point at a given angle from where you're "
            "looking lands on the screen at your distance times the tangent of the angle. "
            f"<bookmark mark='b'/> So the blind spot is centred about {b['centre']:.2f} of your viewing "
            f"distance from the cross, and it's about {b['width']:.2f} of that distance wide. At "
            "fifty-seven centimetres, the distance at which one degree is one centimetre, it's "
            f"{b['at_57_centre']:.0f} centimetres out and {b['at_57']:.0f} centimetres wide. A hole the "
            "size of an orange, at arm's length. <bookmark mark='c'/> The interactive for this part measures "
            "your own. A dot moves slowly outward, you press a key when it vanishes and again when it comes "
            "back, and the page works out where your blind spot starts and ends. People differ, so yours "
            "won't be exactly fifteen degrees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eye), Create(screen), FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(marks[3]),
                      FadeIn(marks[4]), Create(rays[0]), Write(side[0]))
            vo.wait_until("b")
            self.play(Create(rays[1]), Create(rays[2]), Create(spot), FadeIn(marks[2]), FadeIn(side[1]),
                      FadeIn(side[2]))
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()
