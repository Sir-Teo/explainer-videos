from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.headset()
        self.camouflage()
        self.machines()

    def card(self):
        card = chapter_card(13, r"In practice: \ headsets, \ camouflage and machine vision",
                            r"Where does the theory of the bet earn its keep?", lit={2008: r"Hoffman \& Banks"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: headsets, camouflage and machine vision."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def headset(self):
        head = heading(r"A headset tells two stories about depth")
        eyeL, eyeR = np.array([-5.6, -0.25, 0]), np.array([-5.6, 0.25, 0])
        eyes = VGroup(*[Circle(radius=0.16, color=GREY_B, stroke_width=3).move_to(p) for p in (eyeL, eyeR)])
        screen = Line([-4.4, -1.4, 0], [-4.4, 1.4, 0], color=GREY_A, stroke_width=6)
        sl = label(r"the screen, \ optically about 1.5 m away", font_size=20, color=GREY_A).next_to(screen, DOWN, buff=0.15)
        virt = Dot([-2.0, 0, 0], color=VISION, radius=0.1)
        vl = label(r"a virtual object, \ 0.4 m away", font_size=20, color=VISION).next_to(virt, UP, buff=0.15)
        verg = VGroup(Line(eyeL, virt.get_center(), color=VISION, stroke_width=2),
                      Line(eyeR, virt.get_center(), color=VISION, stroke_width=2))
        focus = DashedLine([-5.4, 0, 0], [-4.4, 0, 0], color=LIKE, stroke_width=3)
        fig = VGroup(eyes, screen, sl, virt, vl, verg, focus)
        rows = rows_of([
            (r"vergence: \ the eyes turn in for the object's depth", VISION),
            (r"accommodation: \ the lens must focus at the screen, \ wherever the object is", LIKE),
            (r"in the world the two always agree, \ and the brain expects them to", PRIOR),
            (r"Hoffman, \ Girshick, \ Akeley and Banks, \ 2008: \ the conflict slows fusion and causes fatigue", WHITE),
            (r"the fix being built: \ displays whose focus follows the eyes", POST),
        ], 6.4, 26, 0.32).move_to([3.3, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"drawn to no scale").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Chapter six said cues are combined. A virtual-reality headset is a machine for making cues disagree. "
            "<bookmark mark='a'/> When you look at a virtual object, your eyes turn inward for its depth: here, forty "
            "centimetres. That part works, because the headset gives each eye its own picture, as Wheatstone's did. "
            "<bookmark mark='b'/> But the light comes from a screen whose optical distance is fixed, about a metre "
            "and a half in many headsets, and your lens has to focus there to keep the picture sharp. "
            "<bookmark mark='c'/> In the real world, where the eyes point and where they focus always agree, and the "
            "two are coupled in the brain. <bookmark mark='d'/> In 2008, David Hoffman, Ahna Girshick, Kurt Akeley and "
            "Martin Banks showed that this vergence-accommodation conflict slows the fusing of stereo images, makes "
            "depth harder to judge, and causes fatigue and discomfort. <bookmark mark='e'/> Engineers are now building "
            "displays whose focal distance changes with where you look. The theory says what the display must get "
            "right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eyes), FadeIn(screen), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(virt), FadeIn(vl), Create(verg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(focus), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def camouflage(self):
        head = heading(r"Camouflage: \ attacking the bet")
        rng = np.random.default_rng(1414)
        bark = VGroup(*[Ellipse(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x, y, 0])
                        for x, y, w, h, c in zip(rng.uniform(-1.8, 1.8, 160), rng.uniform(-1.3, 1.3, 160),
                                                 rng.uniform(0.15, 0.4, 160), rng.uniform(0.1, 0.28, 160),
                                                 rng.choice([GREY_D, GREY_C, GREY_B, "#2E2E2E"], 160))])
        bg = Rectangle(width=4.2, height=3.0, fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        moth = Triangle(fill_color=GREY_C, fill_opacity=1, stroke_width=0).scale(0.7).rotate(PI)
        patches = VGroup(*[Ellipse(width=0.35, height=0.2, stroke_width=0, fill_color=c, fill_opacity=1).move_to(p)
                           for p, c in (([-0.45, 0.3, 0], "#2E2E2E"), ([0.42, 0.25, 0], GREY_A), ([0.0, -0.4, 0], "#2E2E2E"))])
        target = VGroup(moth, patches)
        scene_ = VGroup(bg, bark, target).move_to([-3.6, -0.2, 0])
        ring = DashedVMobject(Circle(radius=0.75, color=WORLD, stroke_width=3), num_dashes=24).move_to(target)
        rl = label(r"a target, \ with patches at its edge", font_size=22, color=WORLD).next_to(scene_, DOWN, buff=0.25)
        rows = rows_of([
            (r"disruptive colouring: \ high-contrast patches at the edge break the outline, \ defeating grouping", WHITE),
            (r"Cuthill and colleagues, \ 2005: \ paper moths with edge patches were eaten less by birds", POST),
            (r"countershading: \ dark above, \ light below, \ cancels the shading that would reveal a body's shape", PRIOR),
            (r"camouflage is designed against the priors: \ it makes the wrong explanation the best one", LIKE),
        ], 6.0, 26, 0.34).move_to([3.4, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Animals have been attacking the visual system's bets for far longer than engineers have been helping "
            "them. <bookmark mark='a'/> Disruptive colouring puts patches of strong contrast at the edge of the "
            "body, which break its outline into pieces that group with the background instead of with each other. "
            "<bookmark mark='b'/> In 2005, Innes Cuthill and colleagues pinned paper moths, with dead mealworms as "
            "bait, to trees in a wood, and counted how many birds took. Targets with patches touching their edges "
            "survived better than targets with the same patches inside. <bookmark mark='c'/> Countershading, dark on "
            "the back and light on the belly, cancels the shading that light from above would put on a rounded "
            "body, which chapter seven showed the visual system reads as shape. <bookmark mark='d'/> Camouflage is "
            "designed against the priors. It doesn't hide information so much as make the wrong explanation the "
            "best one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(scene_), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "a":
                    self.play(Create(ring), FadeIn(rl))
        self.clear_scene()

    def machines(self):
        head = heading(r"When machines see for us")
        rows = rows_of([
            (r"machine vision now reads scans, \ checks parts and drives cars", WHITE),
            (r"its errors are not ours: \ texture where we use shape; \ stickers on a stop sign that we would ignore", BAD),
            (r"2018: \ Eykholt and colleagues: \ a few stickers made a network read a stop sign as a speed limit", BAD),
            (r"so a human and a machine together can beat either, \ if their errors differ and each knows when to defer", POST),
            (r"the psychology of the human in the loop: \ Parts 51 and 60", GREY_A),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "Last, machines that see for us. <bookmark mark='a'/> Machine vision now reads medical scans, inspects "
            "parts on production lines and helps drive cars. <bookmark mark='b'/> Chapter eleven showed that its "
            "errors aren't ours. It can rely on texture where we rely on shape, and can be thrown by changes we'd "
            "ignore. <bookmark mark='c'/> In 2018, Kevin Eykholt and colleagues put a few black and white stickers on "
            "a real stop sign, and a network read it as a speed-limit sign from most of the angles and distances "
            "they tested. A person sees a stop sign with graffiti. <bookmark mark='d'/> That difference is also an "
            "opportunity. If a person's errors and a machine's are different, the two together can beat either, but "
            "only if each knows when to defer to the other, which is a question about people as much as machines. "
            "<bookmark mark='e'/> That's human factors, Part 51, and minds and machines, Part 60."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
