from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.screens()
        self.brakes()
        self.clinic()

    def card(self):
        card = chapter_card(13, r"In practice: \ menus, \ brakes and clinics", r"Where does decision time matter?",
                            lit={1954: r"Fitts", 2000: r"Green", 2001: r"Ratcliff, \ Thapar \& McKoon"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: menus, brakes and clinics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def screens(self):
        head = heading(r"Designing for the clock")
        scr = RoundedRectangle(corner_radius=0.12, width=6.2, height=4.0, stroke_color=GREY_B, fill_color="#12161D",
                               fill_opacity=1).move_to([-3.3, -0.1, 0])
        cursor = Dot([-5.4, -1.3, 0], radius=0.07, color=WHITE)
        small = Rectangle(width=0.3, height=0.3, stroke_color=LOST, fill_color=LOST, fill_opacity=0.5
                          ).move_to([-2.0, 0.55, 0])
        big = Rectangle(width=1.2, height=0.3, stroke_color=MODEL, fill_color=MODEL, fill_opacity=0.5
                        ).move_to([-1.6, -0.3, 0])
        corner = Polygon(scr.get_corner(UR), scr.get_corner(UR) + LEFT * 0.6, scr.get_corner(UR) + DOWN * 0.6,
                         stroke_width=0, fill_color=BOUND, fill_opacity=0.7)
        a1 = DashedLine(cursor.get_center(), small.get_center(), color=GREY_B, stroke_width=1.5)
        a2 = DashedLine(cursor.get_center(), big.get_center(), color=GREY_B, stroke_width=1.5)
        dist_s = float(np.linalg.norm(small.get_center() - cursor.get_center()))
        id_small = np.log2(2 * dist_s / 0.3)
        id_big = np.log2(2 * float(np.linalg.norm(big.get_center() - cursor.get_center())) / 1.2)
        b = 0.15
        lt = VGroup(label(rf"{id_small:.1f} bits", font_size=18, color=LOST).next_to(small, RIGHT, buff=0.1),
                    label(rf"{id_big:.1f} bits", font_size=18, color=MODEL).next_to(big, RIGHT, buff=0.1),
                    label(r"a corner: \ infinitely deep", font_size=17, color=BOUND).next_to(corner, DOWN, buff=0.08)
                    .align_to(scr, RIGHT).shift(LEFT * 0.1))
        assert id_small - id_big > 1.5
        rows = rows_of([
            (rf"Fitts: \ a target four times wider saves about {id_small - id_big:.0f} bits, \ about "
             rf"{1000 * b * (id_small - id_big):.0f} ms at an illustrative {1000 * b:.0f} ms a bit", MODEL),
            (r"an edge or a corner of the screen cannot be overshot: \ its width is effectively infinite; \ "
             r"so menus live there", BOUND),
            (r"Hick and Hyman: \ one broad menu often beats a deep tree of small ones; \ and frequent choices "
             r"should cost fewer bits", EVIDENCE),
            (r"ISO 9241-9 tests pointing devices by Fitts's law; \ designing for minds is Part 52", GREY_A),
        ], 5.6, 22, 0.36).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"Fitts's index computed on the drawing; \ the slope is illustrative")
        with self.voiceover(
            "These laws earn their living in design. <bookmark mark='a'/> On a screen, Fitts's law prices every "
            "target. Make a button four times wider and you save about two bits, a few hundred milliseconds at a "
            "typical slope, on every press. <bookmark mark='b'/> An edge or corner of the screen can't be "
            "overshot, so its effective width is infinite, which is why menus and close buttons live there. "
            "<bookmark mark='c'/> Hick and Hyman price the choice itself: one broad menu often beats a deep tree of "
            "small ones, and frequent choices should cost the fewest bits. <bookmark mark='d'/> An international "
            "standard tests mice, trackpads and touchscreens by Fitts's law. Designing for minds is Part 52."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(scr), FadeIn(cursor))
            vo.wait_until("a")
            self.play(FadeIn(small), FadeIn(big), Create(a1), Create(a2), FadeIn(lt[0]), FadeIn(lt[1]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(corner), FadeIn(lt[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def brakes(self):
        head = heading(r"Brakes")
        v = 100 / 3.6
        cases = [(r"expected", 0.75, MODEL), (r"unexpected", 1.25, BOUND), (r"surprise", 1.5, LOST),
                 (r"design value", 2.5, GREY_B)]
        A = axes([0, 75], [0, 4], x_length=6.4, y_length=3.2, xticks=[0, 25, 50, 75], yticks=[],
                 xfmt=lambda v_: f"{v_:.0f}", xlabel=r"metres travelled before the brakes act, \ at 100 km/h",
                 center=[-3.0, -0.2, 0], font_size=16)
        bars_ = VGroup()
        for k, (name, t, c) in enumerate(cases):
            dist = v * t
            r = Rectangle(width=abs(A.ax.c2p(dist, 0)[0] - A.ax.c2p(0, 0)[0]), height=0.42, stroke_width=0,
                          fill_color=c, fill_opacity=0.85)
            r.move_to(A.ax.c2p(0, 3.4 - k), aligned_edge=LEFT)
            bars_.add(VGroup(r, label(rf"{name}: \ {t:.2f} s, \ {dist:.0f} m", font_size=18, color=c).next_to(
                r, UP, buff=0.05).align_to(r, LEFT).shift(RIGHT * 0.12)))
        rows = rows_of([
            (r"Green, \ 2000: \ drivers' perception--brake times run from about 0.7 s when they expect the "
             r"event, \ to about 1.5 s for a true surprise", WHITE),
            (r"at 100 km/h each second is almost 28 metres, \ travelled before the brakes do anything", BOUND),
            (r"road design assumes 2.5 s, \ long enough for nearly every driver: \ a design for the tail of the "
             r"distribution, \ not its mean \ (chapter three)", MODEL),
        ], 5.6, 22, 0.36).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Green (2000); \ AASHTO stopping sight distance")
        with self.voiceover(
            "On the road, decision time is distance. <bookmark mark='a'/> Marc Green reviewed studies of how long "
            "drivers take to start braking. About three quarters of a second when they expect the event, about one "
            "and a quarter when it's unexpected, and about one and a half for a true surprise. "
            "<bookmark mark='b'/> At a hundred kilometres an hour, each second is almost twenty-eight metres, "
            "travelled before the brakes do anything at all. <bookmark mark='c'/> Road engineers assume two and a "
            "half seconds when they set how far ahead a driver must be able to see. That's a design for the slow "
            "tail of the distribution, not its mean, which is exactly the lesson of chapter three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars_[:3]], lag_ratio=0.4),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars_[3], shift=RIGHT * 0.2), FadeIn(rows[2]))
        self.clear_scene()

    def clinic(self):
        head = heading(r"Slower, \ or more careful?")
        items = [
            (r"older adults", BOUND, r"Ratcliff, \ Thapar \& McKoon, \ 2001 onward: \ slower mainly through wider "
             r"bounds and longer $t_0$; \ drift often about the same as the young"),
            (r"clinical groups", DRIFT, r"in ADHD, \ anxiety, \ depression and others, \ the model asks which "
                                        r"number differs: \ evidence, \ caution, \ or the motor stage"),
            (r"treatments", MODEL, r"a drug that speeds people by lowering their caution is not one that sharpens "
                                   r"their evidence; \ drift is a better outcome than mean time"),
        ]
        cols = VGroup()
        for k, (t, c, body) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.15, width=4.1, height=3.4, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.35 + 4.35 * k, 0.5, 0])
            b = VGroup(label(t, font_size=30, color=c), wrapped_label(body, 3.6, 25, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.25)
            b.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.25)
            cols.add(VGroup(box, b))
        note = label(r"the diffusion model turns ``slower'' into a question with three answers", font_size=26,
                     color=MODEL).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Ratcliff, \ Thapar \& McKoon (2001)")
        with self.voiceover(
            "And in the clinic, the diffusion model turns slower into a question with three answers. "
            "<bookmark mark='a'/> Older adults respond more slowly, and from 2001 onward Roger Ratcliff, Anjali "
            "Thapar and Gail McKoon found that in many tasks it's mainly because they set wider bounds and take "
            "longer to see and move. The quality of their evidence is often about the same as the young. They're "
            "more careful, not worse. <bookmark mark='b'/> The same question is asked of groups with attention "
            "deficit disorder, anxiety or depression: is the difference in the evidence, the caution, or the motor "
            "stage? <bookmark mark='c'/> And of treatments. A drug that makes people faster by lowering their "
            "caution isn't one that sharpens their evidence, so the drift is a better outcome measure than the mean "
            "time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            self.play(FadeIn(note))
        self.clear_scene()
