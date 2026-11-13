from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Pfungst(VoiceoverScene):
    def construct(self):
        self.card()
        self.knowledge()
        self.sight()
        self.cue()
        self.distance()
        self.laboratory()

    def card(self):
        card = chapter_card(1, r"Who knows the answer?", r"What did one student try that thirteen experts had not?",
                            lit={1904: r"the Hans Commission", 1907: r"Pfungst's \emph{Clever Hans}"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter one. Who knows the answer?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def knowledge(self):
        d = load("hans")
        rows = {r["name"]: r for r in d["rows"]}
        a, b = rows["numerals, questioner knows"], rows["numerals, questioner does not know"]
        hc = history_card(1904, r"Oskar Pfungst, Berlin", r"Stumpf's student: \ change one thing at a time, and "
                          r"count", color=P.ARCHIVE, width=6.6, font_size=30).to_corner(UL, buff=0.4)
        # the test: a card only the horse can see
        hans = horse(2.0).move_to([-4.6, -1.6, 0])
        asker = questioner(1.7).move_to([-1.9, -1.75, 0])
        cardm = RoundedRectangle(width=0.9, height=1.15, corner_radius=0.08, stroke_color=WHITE, stroke_width=2,
                                 fill_color="#1B2230", fill_opacity=1).move_to([-3.25, -0.2, 0])
        num = MathTex(r"8", font_size=54).move_to(cardm)
        back = label(r"?", font_size=44, color=BLIND).move_to(asker.head).shift(UP * 0.75)
        bars = share_bars([(r"questioner knows the number", a["share"], a["lo"], a["hi"], a["n"], KNOWS),
                           (r"questioner does not", b["share"], b["lo"], b["hi"], b["n"], BLIND)],
                          width=1.5, height=3.3, gap=1.5, font_size=26)
        bars.move_to([3.4, -0.55, 0])
        ylab = label(r"answers right", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.25)
        src = historical_tag(archive.PFUNGST_1907.cite + r", ch.~II")
        with self.voiceover(
            "The investigation fell to a student of Stumpf's, Oskar Pfungst. And Pfungst did what the commission "
            "had not. He stopped watching for the trick, and started changing one thing at a time, and counting. "
            "<bookmark mark='a'/> His first question: does it matter whether the person asking knows the answer? "
            "He held up a card with a number on it, so that only the horse could see it. Sometimes the questioner "
            "had looked at the card first. Sometimes nobody in the yard knew what was on it. "
            f"<bookmark mark='b'/> When the questioner knew the number, Hans tapped it correctly {100 * a['share']:.0f} "
            f"times in a hundred. <bookmark mark='c'/> When the questioner didn't know, {100 * b['share']:.0f} in a "
            "hundred. <bookmark mark='d'/> So Hans can't read numbers. Whatever he's doing, he needs someone "
            "nearby who knows the answer. Pfungst called the second condition procedure without knowledge. We "
            "call it a blind, and this is the experiment that invented it."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(hans), FadeIn(asker), FadeIn(cardm), FadeIn(num))
            self.play(FadeIn(back, shift=DOWN * 0.15))
            self.play(FadeIn(bars.base), FadeIn(ylab))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars.bars[0], DOWN), FadeIn(bars.labels[0]))
            self.play(FadeIn(bars.values[0]), FadeIn(bars.whiskers[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars.bars[1], DOWN), FadeIn(bars.labels[1]))
            self.play(FadeIn(bars.values[1]), FadeIn(bars.whiskers[1]))
            vo.wait_until("d")
            self.play(Indicate(bars.labels[1], color=BLIND, scale_factor=1.08))
        self.clear_scene()

    def sight(self):
        d = load("hans")
        rows = {r["name"]: r for r in d["rows"]}
        a, b = rows["blinders, questioner seen"], rows["blinders, questioner not seen"]
        head = heading(r"Blinders: \ can Hans see the questioner?")
        hans = horse(2.3).move_to([-4.3, -0.9, 0])
        flap = Rectangle(width=0.5, height=0.62, stroke_color=WHITE, stroke_width=2, fill_color="#1B2230",
                         fill_opacity=1).move_to(hans.eye.get_center() + RIGHT * 0.12 + UP * 0.02)
        asker = questioner(1.9).move_to([-1.2, -1.1, 0])
        gaze = DashedLine(hans.eye.get_center(), asker.head.get_left(), color=GREY_B, stroke_width=2)
        bars = share_bars([(r"questioner in sight", a["share"], a["lo"], a["hi"], a["n"], KNOWS),
                           (r"questioner out of sight", b["share"], b["lo"], b["hi"], b["n"], BLIND)],
                          width=1.5, height=3.3, gap=1.5, font_size=26)
        bars.move_to([3.4, -0.75, 0])
        src = historical_tag(archive.PFUNGST_1907.cite + r", ch.~II")
        with self.voiceover(
            "Second question: through which sense does the answer reach him? Hearing was ruled out quickly. Hans "
            "answered questions that were only thought, and never spoken. <bookmark mark='a'/> So Pfungst put "
            "blinders on the horse, and had the questioner stand where Hans couldn't see him. Hans fought it. He "
            "strained to get the questioner back in view, which he had never done before. <bookmark mark='b'/> "
            f"With the questioner in sight, {100 * a['share']:.0f} per cent right. <bookmark mark='c'/> Out of "
            f"sight, {100 * b['share']:.0f}: two answers out of {b['n']}. <bookmark mark='d'/> The answer is "
            "coming in through the horse's eyes, from the person asking, and it only exists if that person knows "
            "it. So now Pfungst knew where to look. He stopped watching the horse, and watched the questioner."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(hans), FadeIn(asker), Create(gaze))
            vo.wait_until("a")
            self.play(FadeIn(flap, shift=DOWN * 0.2), FadeOut(gaze))
            self.play(Wiggle(hans, scale_value=1.03, rotation_angle=0.02 * TAU), FadeIn(bars.base))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars.bars[0], DOWN), FadeIn(bars.labels[0]), FadeIn(bars.values[0]),
                      FadeIn(bars.whiskers[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars.bars[1], DOWN), FadeIn(bars.labels[1]), FadeIn(bars.values[1]),
                      FadeIn(bars.whiskers[1]))
            vo.wait_until("d")
            self.play(Circumscribe(asker, color=P.ACCENT, buff=0.15), run_time=2.0)
        self.clear_scene()

    def cue(self):
        head = heading(r"What the horse was reading")
        hans = horse(2.4).move_to([-4.4, -1.0, 0])
        asker = questioner(2.4).move_to([1.2, -0.95, 0])
        target = VGroup(label(r"the answer is", font_size=26, color=GREY_A), MathTex(r"5", font_size=60, color=KNOWS))
        target.arrange(RIGHT, buff=0.25).next_to(asker, UP, buff=0.5)
        counter = label(r"0", font_size=72, color=HORSE).move_to([-1.6, 1.3, 0])
        steps = VGroup(
            label(r"the tapping starts: \ the questioner leans forward a little, to count", font_size=28),
            label(r"the right count is reached: \ the tension lets go, and the head comes up", font_size=28,
                  color=KNOWS),
            label(r"a fifth of a millimetre is enough", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.85)
        # a magnifier on the head
        lens = Circle(radius=1.15, stroke_color=P.ACCENT, stroke_width=3, fill_color="#101726", fill_opacity=1)
        lens.move_to([4.8, 0.9, 0])
        big = Circle(radius=0.55, stroke_width=0, fill_color=P.HUMAN, fill_opacity=0.9).move_to(lens).shift(DOWN * 0.25)
        ghost = big.copy().set_fill(opacity=0.25)
        up = Arrow(big.get_top() + UP * 0.02, big.get_top() + UP * 0.5, buff=0, color=KNOWS, stroke_width=5,
                   max_tip_length_to_length_ratio=0.4)
        link = DashedLine(asker.head.get_right(), lens.get_left(), color=P.ACCENT, stroke_width=2)
        sch = schematic_tag(UR)
        src = historical_tag(archive.PFUNGST_1907.cite + r", ch.~II")
        pivot = hans.pivot.get_center()

        def tap(k):
            self.play(Rotate(hans.leg, -0.38, about_point=pivot), run_time=0.24, rate_func=rush_into)
            new = label(rf"{k}", font_size=72, color=HORSE).move_to(counter)
            counter.become(new)
            self.play(Rotate(hans.leg, 0.38, about_point=pivot), run_time=0.24, rate_func=rush_from)

        with self.voiceover(
            "And here is what he saw. <bookmark mark='a'/> When the horse begins to tap, the questioner bends "
            "forward a little, to watch the foot and keep count. Nobody notices doing it. <bookmark mark='b'/> "
            "And as the taps approach the number the questioner has in mind, the tension builds. One, two, three, "
            "four. <bookmark mark='c'/> At the right count it lets go, and the head comes up. A tiny upward jerk. "
            "<bookmark mark='d'/> Hans stops tapping when he sees it. He was never counting. He was tapping until "
            "the human relaxed. <bookmark mark='e'/> The movement is small. Pfungst measured it later in the "
            "laboratory at about a millimetre, often less, and the horse could respond to a fifth of that. Which "
            "is why thirteen people watching for a signal didn't see one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hans), FadeIn(asker), FadeIn(target), FadeIn(counter), FadeIn(sch),
                      FadeIn(src))
            vo.wait_until("a")
            self.play(Rotate(asker, -0.14, about_point=asker.body.get_bottom()), FadeIn(steps[0]))
            vo.wait_until("b")
            for k in range(1, 5):
                tap(k)
            vo.wait_until("c")
            tap(5)
            self.play(Rotate(asker, 0.14, about_point=asker.body.get_bottom()), asker.head.animate.shift(UP * 0.08),
                      FadeIn(steps[1]), run_time=0.6)
            self.play(Create(link), FadeIn(lens), FadeIn(ghost), FadeIn(big))
            self.play(big.animate.shift(UP * 0.28), GrowArrow(up))
            vo.wait_until("d")
            self.play(Circumscribe(counter, color=HORSE, buff=0.12))
            vo.wait_until("e")
            self.play(FadeIn(steps[2]))
        self.clear_scene()

    def distance(self):
        d = load("hans")
        rd = d["reader"]
        pts = [r for r in d["rows"] if r["name"].startswith("distance")]
        near = [r for r in d["rows"] if r["name"] in ("numerals, questioner knows", "blinders, questioner seen")]
        head = heading(r"How good were his eyes? \ Pfungst moves the questioner away")
        A = axes([0, 6], [0, 1.05], x_length=7.2, y_length=4.3, xlabel=r"distance of the questioner (metres)",
                 ylabel=r"answers right", xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.6, -0.5, 0])
        ax = A.ax
        model = curve(ax, d["grid"], d["p_correct_grid"], P.PSYCHE, 4)
        dots = VGroup()
        for r in near + pts:
            p_ = ax.c2p(r["distance"], r["share"])
            dots.add(VGroup(Line(ax.c2p(r["distance"], r["lo"]), ax.c2p(r["distance"], r["hi"]), color=P.HUMAN,
                                 stroke_width=3), Dot(p_, radius=0.09, color=P.HUMAN)))
        half = DashedLine(ax.c2p(rd["d0"], 0), ax.c2p(rd["d0"], 0.55), color=P.PSYCHE, stroke_width=2)
        leg = legend([(P.HUMAN, r"Pfungst's tests, 95\% intervals"),
                      (P.PSYCHE, r"Psyche: \ a cue harder to see from afar")], font_size=24)
        leg.move_to([4.2, 1.6, 0], aligned_edge=LEFT).set_x(4.35)
        note_ = wrapped_label(r"the distance series is given in words in the book: \ ``accurate up to $3\tfrac12$ "
                              r"metres'', ``one-third correct'', ``no correct responses''", 4.6, 22, GREY_B)
        note_.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        half_lab = VGroup(label(r"half the cues are seen at", font_size=26, color=P.PSYCHE),
                          label(rf"{rd['d0']:.1f} metres", font_size=44, color=P.PSYCHE))
        half_lab.arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(note_, DOWN, buff=0.5).align_to(leg, LEFT)
        src = historical_tag(archive.PFUNGST_1907.cite + r", ch.~II")
        tag = psyche_tag(r"curve: Psyche (a model with four numbers, fitted)")
        with self.voiceover(
            "Now Pfungst could do something the commission never could. He could predict. If Hans is reading a "
            "small movement, then moving the questioner away should make the movement harder to see. "
            "<bookmark mark='a'/> So he did. Close up, Hans is nearly perfect. <bookmark mark='b'/> Out to three "
            "and a half metres, still accurate. Then it collapses. Between four and four and a half metres, a "
            "third right. Beyond that, nothing. <bookmark mark='c'/> Von Osten, by the way, was the questioner in "
            "most of these tests, and believed they were testing the horse's hearing. <bookmark mark='d'/> We can "
            "write the idea down as a model: a cue that's detected less often as its image on the eye gets "
            "smaller. Four numbers, fitted to Pfungst's counts. <bookmark mark='e'/> It says half the cues are "
            f"seen at about {rd['d0']:.1f} metres. This is a measurement of a horse's eyesight, made with "
            "arithmetic problems, and it's the same kind of curve you'll measure on yourself in Part 11."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.3) for x in dots[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=1.3) for x in dots[2:]], lag_ratio=0.7), FadeIn(leg[0]),
                      run_time=5.0)
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(Create(model), FadeIn(leg[1]), FadeIn(tag), run_time=2.5)
            vo.wait_until("e")
            self.play(Create(half), FadeIn(half_lab))
        self.clear_scene()

    def laboratory(self):
        d = load("hans")
        lab_ = d["laboratory"]
        head = heading(r"Pfungst takes the horse's place")
        n, made = lab_["people"], lab_["made_the_movement"]
        cols = [KNOWS] * made + [GREY_C] * (n - made)
        crowd = people_row(n, cols, height=0.75, buff=0.2, per_row=13).move_to([0, 1.0, 0])
        cap = label(rf"{n} people each think of a number; \ Pfungst taps, and watches them", font_size=30)
        cap.next_to(crowd, UP, buff=0.4)
        res = VGroup(label(rf"{made} of {n}", font_size=60, color=KNOWS),
                     label(r"gave him the signal, and did not know it", font_size=32))
        res.arrange(RIGHT, buff=0.4).next_to(crowd, DOWN, buff=0.45)
        moral = VGroup(
            label(r"Nobody cheated. \ The questioner knew the answer, and the answer leaked.", font_size=34,
                  color=P.ACCENT),
            label(r"The remedy: \ a questioner who does not know it.", font_size=34, color=BLIND),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        src = historical_tag(archive.PFUNGST_1907.cite + r", ch.~IV")
        with self.voiceover(
            "One more experiment, and it's the one that makes this a discovery about people and not about a "
            "horse. Pfungst went back to the laboratory and played the part of Hans himself. "
            f"<bookmark mark='a'/> He asked {n} people, one at a time, to think hard of a number, while he tapped "
            "with his hand and watched them. None of them knew what he was looking for. "
            f"<bookmark mark='b'/> {made} of the {n} gave him the same involuntary jerk of the head at the right "
            "count, and from it he could tell their number. They were sure they had given nothing away. "
            "<bookmark mark='c'/> So the commission was right that nobody cheated. Von Osten had spent four "
            "years, with no intention of doing so, teaching a horse to read his face. And everyone who asked a "
            "question and knew the answer was telling it. <bookmark mark='d'/> The remedy follows at once: put "
            "the question through someone who doesn't know the answer. Keep that in mind. It comes back in "
            "chapter seven with rats, and children, and police dogs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            people_white = crowd.copy()
            for p_ in people_white:
                p_.set_color(P.HUMAN)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in people_white], lag_ratio=0.06), run_time=3.0)
            vo.wait_until("b")
            self.play(ReplacementTransform(people_white, crowd), run_time=1.5)
            self.play(FadeIn(res, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(moral[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(moral[1], shift=UP * 0.15))
        self.clear_scene()
