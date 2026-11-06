from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, tag_box


def _button(text, color=DATA, w=1.5):
    return tag_box(text, color=color, size=20, w=w, h=0.6)


class Access(VoiceoverScene):
    def construct(self):
        self.card()
        self.who()
        self.assistive()
        self.motor()
        self.cognitive()
        self.universal()

    def card(self):
        card = chapter_card(6, r"Accessibility", r"Who is the interface for?", lit=(1999, 2023),
                            extra=((1999, r"WCAG 1.0"), (2023, r"WCAG 2.2")), part=PART)
        with self.voiceover("Chapter six. Accessibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def who(self):
        head = label(r"Who it is for", font_size=36).to_edge(UP, buff=0.3)
        people = VGroup(*[Dot(radius=0.11, color=GREY_D) for _ in range(100)]).arrange_in_grid(rows=10, cols=10,
                                                                                            buff=0.17)
        people.move_to([-4.3, 0.35, 0])
        lit = [people[k] for k in range(100) if k % 6 == 0][:16]       # 16 of 100, spread through the grid
        who = wrapped_label(r"about 1.3 billion people, \ 16\% of the world, \ live with significant disability "
                            r"\ (WHO, \ 2022 report; \ 2023 fact sheet)", 4.2, font_size=19,
                            color=HEAD).next_to(people, DOWN, buff=0.3)
        rows = [[r"touch", r"one arm", r"arm injury", r"new parent"],
                [r"see", r"blind", r"cataract", r"distracted driver"],
                [r"hear", r"deaf", r"ear infection", r"bartender"]]
        tab = grid_table([r"", r"permanent", r"temporary", r"situational"], rows, widths=[1.1, 1.6, 1.9, 2.5],
                         row_h=0.62, font_size=20, mono_cols=())
        tab.move_to([2.8, 1.3, 0])
        for r in range(1, 4):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(KERN)
            tab.cells[r][3].set_color(YES)
        src = note(r"after Microsoft's Inclusive Design toolkit", font_size=16).next_to(tab, DOWN, buff=0.15)
        line = wrapped_label(r"disability is a mismatch between a person and a design, \ and everyone meets one: "
                             r"\ age alone brings most of them", 6.6, font_size=20, color=WHITE).next_to(
            src, DOWN, buff=0.4)
        with self.voiceover(
            "Accessibility is design for people whose bodies or minds differ from the designer's. "
            "<bookmark mark='a'/> The World Health Organization estimates that about one point three billion "
            "people, sixteen per cent of the world, live with a significant disability. <bookmark mark='b'/> And "
            "the line is blurry. Microsoft's inclusive design toolkit draws a spectrum: a person with one arm, a "
            "person with a broken arm and a parent holding a baby all need a phone that works one-handed. The same "
            "goes for blindness, a cataract and a driver's eyes on the road, and for deafness, an ear infection and a "
            "noisy bar. <bookmark mark='c'/> Disability is a mismatch between a person and a design, and with age "
            "almost everyone meets one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(people))
            vo.wait_until("a")
            self.play(*[d.animate.set_color(HEAD) for d in lit], FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(src))
            for r in range(1, 4):
                self.play(FadeIn(VGroup(*tab.cells[r])), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(line))
        self.wait(0.4)
        self.clear_scene()

    def assistive(self):
        head = label(r"Assistive technology", font_size=36).to_edge(UP, buff=0.3)
        frame = RoundedRectangle(width=5.4, height=3.6, corner_radius=0.15, stroke_color=GREY_C, fill_color=BG,
                                 fill_opacity=1).move_to([-3.7, 0.0, 0])
        btns = VGroup(_button("Home"), _button("Search"), _button("Buy", color=YES)).arrange(RIGHT, buff=0.2)
        btns.move_to(frame).shift(UP * 0.7)
        body = VGroup(*[Line([0, 0, 0], [w, 0, 0], color=GREY_D, stroke_width=5) for w in (4.2, 3.6, 4.0)]
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(btns, DOWN, buff=0.45).align_to(btns,
                                                                                                         LEFT)
        speech = label(r"``Buy, \ button''", font_size=20, color=DATA).next_to(frame, DOWN, buff=0.25).set_x(-5.2)
        ring = SurroundingRectangle(btns[0], color=HEAD, buff=0.08, stroke_width=4)
        lens = Circle(radius=0.75, color=LAM, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(
            btns[2].get_center() + DOWN * 1.35)
        big = _button("Buy", color=YES).scale(1.6).move_to(lens)
        voice = label(r"``click Buy''", font_size=20, color=KERN).next_to(frame, DOWN, buff=0.25).set_x(-2.2)
        notes = VGroup(
            wrapped_label(r"\textbf{screen readers} speak the accessibility tree \ (Part 42): \ a role, \ a name "
                          r"and a state for everything a person can use", 5.6, font_size=19, color=DATA),
            wrapped_label(r"\textbf{switch access}: \ one switch moves a highlight, \ another selects; \ every "
                          r"action must be reachable in that order", 5.6, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{magnification}: \ WCAG asks that text resize to 200\%, \ and that pages reflow "
                          r"at 320 CSS pixels wide without scrolling sideways", 5.6, font_size=19, color=LAM),
            wrapped_label(r"\textbf{voice control} acts on what it hears: \ the visible label must be part of the "
                          r"accessible name \ (WCAG 2.5.3)", 5.6, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.0, 0])
        with self.voiceover(
            "Each kind of assistive technology asks something different of software. <bookmark mark='a'/> A screen "
            "reader speaks the accessibility tree that Part 42 built from the page: this is a button, named Buy. "
            "<bookmark mark='b'/> Someone who can press only one or two switches, with a hand, a foot or a breath, "
            "steps a highlight through the controls, so every action must be reachable in that order. "
            "<bookmark mark='c'/> Magnifiers enlarge the screen; the guidelines ask that text resize to twice its "
            "size, and that a page still work at three hundred and twenty pixels wide. <bookmark mark='d'/> Voice "
            "control acts on names: say click Buy, and it must find a control whose accessible name contains the "
            "visible word."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(btns), Create(body))
            vo.wait_until("a")
            self.play(Indicate(btns[2], color=DATA), FadeIn(speech), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(notes[1]))
            for b in btns[1:]:
                self.play(ring.animate.move_to(b), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeOut(ring), FadeIn(lens), FadeIn(big), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeOut(lens), FadeOut(big), FadeIn(voice), FadeIn(notes[3]))
            self.play(Indicate(btns[2], color=KERN, scale_factor=1.15))
        self.wait(0.4)
        self.clear_scene()

    def motor(self):
        f = load("fitts")
        a, b = f["a"], f["b"]
        head = label(r"Motor accessibility: \ bigger targets", font_size=36).to_edge(UP, buff=0.3)
        D, px = 480, 0.0105                            # an illustrative reach of 480 CSS pixels, drawn to scale
        start = Dot([-6.2, -0.2, 0], radius=0.07, color=WHITE)
        sizes = [(16, NO), (24, HEAD), (44, YES)]
        targets = VGroup()
        for k, (w, c) in enumerate(sizes):
            sq = Square(w * px * 2.2, stroke_color=c, fill_color=c, fill_opacity=0.35).move_to(
                [-6.2 + D * px, 1.1 - 1.3 * k, 0])
            targets.add(sq)
        reach = VGroup(*[DashedLine(start.get_center(), t.get_left(), color=GREY_C, stroke_width=1.5) for t in targets])
        names = VGroup(*[label(rf"{w} px", font_size=18, color=c).next_to(t, RIGHT, buff=0.15)
                         for (w, c), t in zip(sizes, targets)])
        dl = label(rf"reach {D} px", font_size=17, color=GREY_B).next_to(start, DOWN, buff=0.15)
        ill = note(r"illustrative reach; \ targets drawn 2.2 times larger than the reach's scale", font_size=16
                   ).next_to(targets, DOWN, buff=0.35).align_to(start, LEFT)
        rows = []
        for w, _ in sizes:
            ID = math.log2(D / w + 1)
            rows.append([f"{w}", f"{ID:.2f}", f"{1000 * (a + b * ID):.0f}"])
        tab = grid_table([r"width \ (px)", r"$\log_2(D/W + 1)$", r"predicted ms"], rows, widths=[1.6, 2.4, 1.9],
                         row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([3.5, 1.4, 0])
        for r, (_, c) in enumerate(sizes, 1):
            for cc in tab.cells[r]:
                cc.set_color(c)
        fit = note(rf"with chapter 1's fit, \ $MT = {a:.2f} + {b:.3f}\,\log_2(D/W+1)$ seconds", font_size=17
                   ).next_to(tab, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"WCAG 2.2 \ (2.5.8, \ AA): \ targets at least \textbf{24 by 24 CSS pixels}, \ or spaced "
                          r"so that a 24-pixel circle on each touches no other; \ 44 by 44 at AAA \ (2.5.5)", 5.8,
                          font_size=19, color=HEAD),
            wrapped_label(r"a tremor widens the scatter of the hand, \ so the same target is effectively smaller; "
                          r"\ every drag needs a single-tap alternative \ (2.5.7), \ and every action a keyboard "
                          r"route", 5.8, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(fit, DOWN, buff=0.4)
        with self.voiceover(
            "Chapter one's law has an accessibility reading. <bookmark mark='a'/> For a given reach, a wider target "
            "is quicker to hit. With chapter one's fit, a sixteen-pixel target four hundred and eighty pixels away "
            f"takes about {rows[0][2]} milliseconds, a forty-four-pixel one {rows[2][2]}. <bookmark mark='b'/> For "
            "someone with a tremor, whose hand scatters widely, the difference decides whether the target can be "
            "hit at all. WCAG 2.2 sets a minimum of twenty-four by twenty-four CSS pixels, or enough space around a "
            "smaller target. <bookmark mark='c'/> And anything done by dragging must also work with a single tap, "
            "and everything with a keyboard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(start), FadeIn(dl))
            vo.wait_until("a")
            self.play(Create(reach), FadeIn(targets), FadeIn(names), FadeIn(ill))
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      *[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 4)], FadeIn(fit))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), Indicate(targets[1], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def cognitive(self):
        head = label(r"Cognitive accessibility, \ and captions", font_size=36).to_edge(UP, buff=0.3)

        def page(title, x):
            fr = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.1, stroke_color=GREY_C).move_to([x, 0.9, 0])
            nav = VGroup(*[Rectangle(width=0.62, height=0.22, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
                           for _ in range(3)]).arrange(RIGHT, buff=0.12).next_to(fr.get_top(), DOWN, buff=0.2)
            t = label(title, font_size=17, color=GREY_A).next_to(nav, DOWN, buff=0.3)
            lines = VGroup(*[Line([0, 0, 0], [2.2, 0, 0], color=GREY_D, stroke_width=4) for _ in range(3)]).arrange(
                DOWN, buff=0.2).next_to(t, DOWN, buff=0.2)
            return VGroup(fr, nav, t, lines)
        p1, p2 = page(r"page one", -5.2), page(r"page two", -2.0)
        same = label(r"same menu, \ same place \ (3.2.3)", font_size=18, color=DATA).next_to(VGroup(p1, p2), DOWN,
                                                                                         buff=0.15)
        tbox = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.1, stroke_color=GREY_C).move_to([1.3, 0.9, 0])
        bar = Rectangle(width=2.4, height=0.2, stroke_color=HEAD, fill_color=HEAD, fill_opacity=0.8).move_to(
            tbox).shift(UP * 0.45)
        bar.align_to(tbox, LEFT).shift(RIGHT * 0.3)
        tq = label(r"Need more time?", font_size=19, color=WHITE).next_to(bar, DOWN, buff=0.25)
        ext = _button("Extend", color=YES, w=1.5).next_to(tq, DOWN, buff=0.2)
        tl = label(r"warn, \ and let people extend \ (2.2.1)", font_size=18, color=HEAD).next_to(tbox, DOWN,
                                                                                               buff=0.15)
        video = Rectangle(width=3.0, height=2.3, stroke_color=GREY_C, fill_color=GREY_E, fill_opacity=0.6).move_to(
            [4.9, 0.9, 0])
        play_ = Triangle(color=GREY_B, fill_opacity=0.8).rotate(-PI / 2).scale(0.3).move_to(video).shift(UP * 0.3)
        cap = label(r"[door slams] \ Who's there?", font_size=17, color=WHITE)
        cap.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.06)
        cap.move_to(video.get_bottom() + UP * 0.35)
        vl = label(r"captions, \ with sounds \ (1.2.2)", font_size=18, color=YES).next_to(video, DOWN, buff=0.15)
        ill = note(r"illustrative", font_size=16).to_corner(UR, buff=0.3).shift(DOWN * 0.6)
        lines = VGroup(
            wrapped_label(r"plain words and short sentences; \ the same thing in the same place on every page; \ no "
                          r"time limit a person cannot turn off or extend", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"WCAG 2.2's 3.3.8: \ signing in must not require a memory or puzzle test, \ so let "
                          r"password managers fill the field and let people paste", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Some disabilities affect memory, attention or reading. <bookmark mark='a'/> For them, and for everyone "
            "who is tired or in a hurry, the rules are mostly restraint: plain words, short sentences, and "
            "navigation that stays the same from page to page, so nothing has to be relearned. "
            "<bookmark mark='b'/> A time limit should come with a warning and a way to extend it, or not exist. "
            "<bookmark mark='c'/> WCAG 2.2 added that signing in must not depend on remembering or solving a puzzle: "
            "let a password manager fill the field, and let people paste. <bookmark mark='d'/> And video needs "
            "captions, including the sounds that matter, for deaf viewers, and for everyone watching on a train "
            "with the sound off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(same), FadeIn(lines[0]))
            self.play(Indicate(p1[1], color=DATA), Indicate(p2[1], color=DATA))
            vo.wait_until("b")
            self.play(FadeIn(tbox), FadeIn(bar), FadeIn(tq), FadeIn(ext), FadeIn(tl))
            self.play(bar.animate.stretch_to_fit_width(0.6, about_edge=LEFT), run_time=1.5)
            self.play(Indicate(ext, color=YES), bar.animate.stretch_to_fit_width(2.4, about_edge=LEFT))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(video), FadeIn(play_), FadeIn(cap), FadeIn(vl))
        self.wait(0.4)
        self.clear_scene()

    def universal(self):
        head = label(r"Universal design", font_size=36).to_edge(UP, buff=0.3)
        y0, y1 = 0.6, 1.3                                  # the road and the pavement
        road = Line([-4.6, y0, 0], [-2.8, y0, 0], color=GREY_B, stroke_width=4)
        kerb = VGroup(Line([-6.6, y1, 0], [-5.4, y1, 0], color=GREY_B, stroke_width=4),
                      Line([-5.4, y1, 0], [-4.6, y0, 0], color=YES, stroke_width=6))
        step = VGroup(DashedLine([-5.4, y1, 0], [-4.6, y1, 0], color=GREY_C, stroke_width=2),
                      DashedLine([-4.6, y1, 0], [-4.6, y0, 0], color=GREY_C, stroke_width=2))
        kinds = ((r"wheelchair", HEAD), (r"pram", DATA), (r"suitcase", LAM), (r"bicycle", KERN))
        names = VGroup(*[label(t, font_size=18, color=c) for t, c in kinds]).arrange(RIGHT, buff=0.3).next_to(
            VGroup(road, kerb), UP, buff=0.9).align_to(kerb, LEFT)
        riders = VGroup(*[Dot([-6.3, y1 + 0.1, 0], radius=0.1, color=c) for _, c in kinds])
        cap = wrapped_label(r"a kerb cut, \ made for wheelchairs, \ used by everyone pushing anything", 3.6,
                            font_size=18, color=YES).next_to(road, DOWN, buff=0.3).align_to(kerb, LEFT)
        pillars = VGroup()
        for name, ex, c in ((r"Perceivable", r"text alternatives, \\ captions, \ contrast", DATA),
                            (r"Operable", r"keyboard, \ time, \\ target size", HEAD),
                            (r"Understandable", r"plain, \ predictable, \\ helps with errors", YES),
                            (r"Robust", r"a correct tree \\ for assistive tech", LAM)):
            box = RoundedRectangle(width=2.15, height=1.7, corner_radius=0.1, stroke_color=c, fill_color=c,
                                   fill_opacity=0.1)
            t = label(name, font_size=20, color=c)
            e = label(ex, font_size=17, color=GREY_A)
            VGroup(t, e).arrange(DOWN, buff=0.2).move_to(box)
            if t.width > 2.0:
                t.width = 2.0
            pillars.add(VGroup(box, t, e))
        pillars.arrange(RIGHT, buff=0.15).move_to([2.25, 0.9, 0])
        pt = label(r"WCAG's four principles", font_size=20, color=WHITE).next_to(pillars, UP, buff=0.15)
        lines = VGroup(
            wrapped_label(r"\textbf{universal design} \ (the architect Ronald Mace's term): \ design once for the "
                          r"widest range of people, \ instead of adding a special version later", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"contrast was derived in Part 42, \ and chapter 4 checked this series' own palette "
                          r"against it", 12.4, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Designing for the edges usually helps the middle. <bookmark mark='a'/> Cuts in the kerb were fought for "
            "by wheelchair users; now everyone with a pram, a suitcase or a bicycle uses them, and the pattern is "
            "called the curb-cut effect. Captions, made for deaf viewers, are read in every noisy room. "
            "<bookmark mark='b'/> The architect Ronald Mace called this universal design: one design for the widest "
            "range of people, rather than a special version added later. <bookmark mark='c'/> The web's guidelines "
            "rest on four principles. Content must be perceivable, operable, understandable, and robust enough to "
            "work with assistive technology. <bookmark mark='d'/> Contrast belongs to the first; Part 42 derived it, "
            "and chapter four checked this series' palette."
        ) as vo:
            self.play(FadeIn(head), Create(road), Create(step), Create(kerb[0]))
            vo.wait_until("a")
            self.play(FadeOut(step), Create(kerb[1]), FadeIn(cap))
            for k, (dot, nm) in enumerate(zip(riders, names)):
                self.play(FadeIn(dot), FadeIn(nm), run_time=0.3)
                path = VMobject().set_points_as_corners([dot.get_center(), [-5.4, y1 + 0.1, 0],
                                                         [-4.6, y0 + 0.1, 0], [-3.4 - 0.25 * k, y0 + 0.1, 0]])
                self.play(MoveAlongPath(dot, path), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(pt), LaggedStart(*[FadeIn(p) for p in pillars], lag_ratio=0.3), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), Indicate(pillars[0], color=DATA))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
