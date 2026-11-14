from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Priors(VoiceoverScene):
    def construct(self):
        self.card()
        self.discs()
        self.retrain()
        self.speed()
        self.fog()
        self.aperture()
        self.plane()

    def card(self):
        card = chapter_card(7, r"Priors made visible", r"Can you see the assumptions your eyes make?",
                            lit={1982: r"Thompson", 2002: r"Weiss", 2004: r"Adams"}, part=PART, scale=("mind",),
                            marr=("what",))
        with self.voiceover("Chapter seven. Priors made visible."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def discs(self):
        d = load("light")
        head = heading(r"On you: \ bumps or dents?")
        grid = Group()
        pattern = (1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1)
        for k, up in enumerate(pattern):
            img = picture(d["top"] if up else d["bottom"], 1.35, smooth=True)
            img.move_to([-5.0 + (k % 6) * 1.5, 1.2 - (k // 6) * 1.6, 0])
            grid.add(img)
        rows = rows_of([
            (r"discs lighter at the top look like bumps; \ lighter at the bottom, \ like dents", WHITE),
            (r"the shading fits either: \ a bump lit from above, \ or a dent lit from below", LIKE),
            (r"the visual system assumes light from above, \ and a little to the left", PRIOR),
            (r"turn your head upside down and they swap: \ the prior is tied to the head, \ not to the sky", YOU),
        ], 12.4, 27, 0.3).to_edge(DOWN, buff=0.85)
        tag = psyche_tag(r"computed: \ each disc shaded from top to bottom, \ or bottom to top")
        with self.voiceover(
            "Here are twelve discs, shaded from light to dark. <bookmark mark='a'/> To most people, the discs that "
            "are lighter at the top look like bumps, standing out of the page, and the ones lighter at the bottom "
            "like dents. <bookmark mark='b'/> The shading itself is ambiguous. A bump lit from above and a dent lit "
            "from below produce exactly the same image. <bookmark mark='c'/> So the visual system uses a prior: light "
            "comes from above. Vilayanur Ramachandran made this demonstration famous in 1988, and later measurements "
            "found the assumed light is above and a little to the left. <bookmark mark='d'/> If you can, tilt your "
            "head all the way over, or turn your screen upside down. The bumps and dents swap. The assumption is "
            "tied to your head, not to the real sky, which is a cheap approximation that works because we usually "
            "hold our heads upright."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def retrain(self):
        head = heading(r"A prior can be retrained")
        rows = rows_of([
            (r"2004: \ Adams, \ Graf and Ernst: \ judge shaded shapes, \ bump or dent", WHITE),
            (r"training: \ touch the shapes, \ through a force-feedback device, \ with the light really from the side", TOUCH),
            (r"after an hour or two, \ the light the observers assumed had moved toward the trained direction", PRIOR),
            (r"and the shift carried over to a different task, \ judging which of two patches was lighter", POST),
            (r"a prior is a learned summary of the world, \ and it keeps learning", GREY_A),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.ADAMS_2004.cite)
        with self.voiceover(
            "Is that prior built in, or learned? <bookmark mark='a'/> In 2004, Wendy Adams, Erich Graf and Marc Ernst "
            "showed observers shaded shapes and asked whether each was a bump or a dent. <bookmark mark='b'/> Then "
            "they trained them. The observers touched the shapes through a force-feedback device, and what they "
            "felt was consistent with light falling from a direction off to the side, not from above. "
            "<bookmark mark='c'/> After the training, the direction of light they assumed when looking had moved "
            "toward the trained direction. <bookmark mark='d'/> And the change wasn't confined to the task they "
            "trained on. It carried over to a different judgment, of which of two patches looked lighter. "
            "<bookmark mark='e'/> So a prior isn't a fixed setting. It's a learned summary of the world, and it keeps "
            "being updated. Where priors come from in the first place is the frontier's question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def speed(self):
        d = load("motion")
        head = heading(r"Low contrast looks slower")
        A = axes([np.log10(0.02), 0], [0, 1.1], x_length=6.8, y_length=4.2, xticks=[np.log10(v) for v in (0.02, 0.1, 0.3, 1.0)],
                 xfmt=lambda v: f"{10 ** v:.2g}", yticks=[0, 0.5, 1.0], xlabel=r"contrast",
                 ylabel=r"perceived speed / true speed", center=[-2.6, -0.3, 0])
        ax = A.ax
        line = curve(ax, np.log10(d["c"]), d["speed"], POST, stroke_width=5)
        true = DashedLine(ax.c2p(np.log10(0.02), 1.0), ax.c2p(0, 1.0), color=WORLD, stroke_width=2)
        tl = label(r"true speed", font_size=22, color=WORLD).next_to(true, UP, buff=0.08).align_to(true, RIGHT)
        sp = np.interp([1.0, 0.3, 0.1], d["c"], d["speed"])
        rows = rows_of([
            (r"1982: \ Thompson: \ a faint grating looks slower than a strong one moving at the same speed", WHITE),
            (r"the model: \ a prior that most things are still or slow, \ and a measurement noisier at low contrast", PRIOR),
            (rf"in this model, \ at contrasts 1, \ 0.3 and 0.1: \ {sp[0]:.2f}, \ {sp[1]:.2f}, \ {sp[2]:.2f} of the true speed", POST),
        ], 5.0, 26, 0.34).move_to([4.3, 0.0, 0])
        keep_in_frame(rows)
        tag = VGroup(psyche_tag(r"computed: \ the posterior mean with a slow prior"),
                     published_tag(rf"{archive.THOMPSON_1982.cite}; \ {archive.WEISS_2002.cite}", corner=DL))
        with self.voiceover(
            "The second prior you can see concerns speed. <bookmark mark='a'/> In 1982, Peter Thompson showed that a "
            "moving grating of low contrast looks slower than the same grating at high contrast, moving at exactly "
            "the same speed. <bookmark mark='b'/> In 2002, Yair Weiss, Eero Simoncelli and Edward Adelson explained "
            "it with two assumptions: that most things in the world are still or move slowly, and that a measurement "
            "of motion is noisier at low contrast. That's chapter five's shrinkage. A noisier measurement means more "
            "weight on the prior, and the prior says slow. <bookmark mark='c'/> In this version of their model, a "
            "grating at full contrast is seen at about nine tenths of its true speed; at contrast point three, half; "
            "at point one, a tenth. Those exact numbers are the model's, not people's, but the direction is right, at "
            "least for slow and moderate speeds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(true), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fog(self):
        head = heading(r"Driving in fog")
        rows = rows_of([
            (r"1998: \ Snowden, \ Stimpson and Ruddle: \ in a driving simulator, \ uniform fog made speeds look slower, \ and people drove faster", WHITE),
            (r"a frightening prediction, \ if fog lowers contrast everywhere", BAD),
            (r"2012: \ Pretto and colleagues: \ fog that thickens with distance, \ like real fog, \ made speeds look faster", LIKE),
            (r"real fog removes far contrast more than near: \ the near field carries the speed signal", PRIOR),
            (r"the Ledger's note: \ the slowing is robust for slow and moderate speeds; \ above that, \ mixed", GREY_A),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        tag = note(r"the Ledger has the row").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A prior that slows faint motion has an obvious practical worry. <bookmark mark='a'/> In 1998, Robert "
            "Snowden, Nicola Stimpson and Roy Ruddle put drivers in a simulator and lowered the contrast of the whole "
            "scene, as a uniform fog would. Speeds looked slower, and people drove faster to compensate. "
            "<bookmark mark='b'/> If that held on real roads, fog would be even more dangerous than it seems. "
            "<bookmark mark='c'/> But in 2012, Paolo Pretto and colleagues simulated fog the way real fog behaves, "
            "thicker with distance, so that far contrast is lost much more than near. Then speeds looked faster, "
            "not slower. <bookmark mark='d'/> The difference is informative. Real fog leaves the near road, sweeping "
            "past, at reasonable contrast, and the far field, which is now washed out, normally moves slowly in the "
            "image anyway. <bookmark mark='e'/> The laboratory effect is robust. What it means on a road depends on "
            "the details, which is what the Ledger's note says."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def aperture(self):
        head = heading(r"The aperture problem")
        hole = Circle(radius=1.6, color=GREY_B, stroke_width=3).move_to([-3.4, -0.2, 0])
        ang = np.radians(20)  # the stripes' orientation
        u, nrm = np.array([np.cos(ang), np.sin(ang), 0]), np.array([-np.sin(ang), np.cos(ang), 0])
        bars = VGroup()
        for k in range(-5, 6):
            t = 0.4 * k
            half = np.sqrt(max(1.9 ** 2 - t ** 2, 0.01))
            bars.add(Line(t * nrm - half * u, t * nrm + half * u, color=LIKE, stroke_width=4))
        bars.move_to(hole.get_center())
        mask = Difference(Square(6.4).move_to(hole), Circle(radius=1.6).move_to(hole), fill_color=BLACK,
                          fill_opacity=1, stroke_width=0)
        true_arrow = Arrow(hole.get_center() + LEFT * 0.7, hole.get_center() + RIGHT * 0.9, buff=0, color=WORLD,
                           stroke_width=5)
        n = np.array([np.cos(np.radians(-70)), np.sin(np.radians(-70)), 0])
        norm_arrow = Arrow(hole.get_center(), hole.get_center() + 1.2 * 0.342 * 2.2 * n, buff=0, color=LIKE,
                           stroke_width=5)
        rows = rows_of([
            (r"an edge seen through a small window: \ only motion across the edge can be measured", WHITE),
            (r"the true motion, \ to the right, \ and any motion along the edge give the same image", LIKE),
            (r"every neuron in V1 looks through such a window: \ its receptive field", GREY_A),
            (r"one edge gives a line of possible velocities; \ two edges, \ two lines", PRIOR),
        ], 5.6, 26, 0.34).move_to([3.6, -0.1, 0])
        keep_in_frame(rows)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Weiss's model explains more than the speed of gratings. It explains a puzzle about direction. "
            "<bookmark mark='a'/> Look at a moving edge through a small window. Only the motion across the edge, "
            "perpendicular to it, changes the image. <bookmark mark='b'/> Here the stripes really move to the right. "
            "But motion to the right and a slower motion straight across the stripes look identical through the "
            "window, as does any combination of either one with sliding along the stripes. "
            "<bookmark mark='c'/> This isn't a curiosity: every neuron in primary visual cortex looks at the world "
            "through such a window, its receptive field. <bookmark mark='d'/> So one edge gives not a velocity but a "
            "line of possible velocities. An object with two edges at different angles gives two lines, and they "
            "cross at the true velocity."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(mask), Create(hole), FadeIn(tag))
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), bars.animate.shift(RIGHT * 0.25), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowArrow(true_arrow), GrowArrow(norm_arrow), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def plane(self):
        d = load("motion")
        head = heading(r"Two edges: \ where do the lines cross?")
        A = axes([-0.4, 1.4], [-1.0, 0.6], x_length=6.0, y_length=5.3, xticks=[0, 0.5, 1.0], yticks=[-1, -0.5, 0, 0.5],
                 xlabel=r"$v_x$", ylabel=r"$v_y$", center=[-3.0, -0.3, 0])
        ax = A.ax
        lines = VGroup()
        for nrm, s in zip(d["normals"], d["nspeeds"]):
            nrm = np.array(nrm)
            perp = np.array([-nrm[1], nrm[0]])
            p0, p1 = s * nrm - 1.6 * perp, s * nrm + 1.6 * perp
            ts = np.linspace(0, 1, 60)
            pts = [p0 + t * (p1 - p0) for t in ts]
            pts = [p for p in pts if -0.4 <= p[0] <= 1.4 and -1.0 <= p[1] <= 0.6]
            lines.add(VMobject(color=LIKE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in pts]))
        origin = Dot(ax.c2p(0, 0), color=PRIOR, radius=0.07)
        ol = label(r"the prior: \ still", font_size=20, color=PRIOR).next_to(origin, UL, buff=0.05)
        ioc = Dot(ax.c2p(1, 0), color=WORLD, radius=0.08)
        il = label(r"truth", font_size=20, color=WORLD).next_to(ioc, UR, buff=0.05)
        va = Dot(ax.c2p(*d["va"]), color=GREY_B, radius=0.07)
        vl = label(r"vector average", font_size=20, color=GREY_B).next_to(va, DOWN, buff=0.1)
        maps = VGroup(*[Dot(ax.c2p(*v), color=POST, radius=0.08) for v in d["v"]])
        path = VMobject(color=POST, stroke_width=2).set_points_smoothly([ax.c2p(*v) for v in d["v"]])
        a = d["angles"]
        s = d["speeds"]
        rows = rows_of([
            (r"high contrast: \ the percept sits where the lines cross", WORLD),
            (rf"lower contrast: \ {abs(a[1]):.0f}$^\circ$ off, \ at {s[1]:.2f} of the speed", POST),
            (rf"lowest: \ {abs(a[2]):.0f}$^\circ$ off, \ at {s[2]:.2f}, \ heading for the vector average", POST),
            (r"people see a faint rhombus drift in a direction it is not moving: \ the model predicts by how much", PRIOR),
        ], 5.6, 26, 0.34).move_to([3.7, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the MAP velocity for edges at 20$^\circ$ and 60$^\circ$")
        with self.voiceover(
            "Here are those two lines of possible velocities, for an object with edges at twenty and sixty degrees, "
            "really moving to the right at speed one. <bookmark mark='a'/> They cross at the truth. When the edges "
            "are high in contrast and the measurements are sharp, the most probable velocity is just there. "
            "<bookmark mark='b'/> Lower the contrast, and the lines become blurry bands, and the slow prior, centred "
            "on zero, pulls the answer toward stillness. It doesn't pull straight toward zero. It slides along the "
            "bands, toward the point where they're both nearly satisfied at low speed: eight degrees off course, at "
            "eight tenths of the speed. <bookmark mark='c'/> At the lowest contrast, thirty degrees off, at less than "
            "half the speed, heading toward the simple average of the two edges' motions. <bookmark mark='d'/> And "
            "that's what people see. A thin rhombus moving to the right, at low contrast, appears to drift off at an "
            "angle. Researchers had explained the high-contrast and low-contrast cases with two different rules. "
            "One prior, and one noise level, explains both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(lines), FadeIn(origin), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(ioc), FadeIn(il), FadeIn(maps[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(lines.animate.set_stroke(width=9, opacity=0.4), FadeIn(maps[1]), Create(path), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(maps[2]), FadeIn(va), FadeIn(vl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
