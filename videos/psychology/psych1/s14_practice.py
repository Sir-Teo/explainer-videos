from __future__ import annotations

from videos.psychology.psych1.common import *  # noqa: F403

ROAD, SCREEN, CLINIC, TRACK = "#F2C14E", "#7EC8F5", "#7BD88F", "#FF7F6E"


def tile(big: str, title: str, text: str, color, source: str, width=6.75, height=3.0) -> VGroup:
    num = label(big, font_size=76, color=color)
    t = label(title, font_size=36, color=WHITE)
    body = wrapped_label(text, width - 0.8, 27, GREY_A)
    src = label(source, font_size=19, color=GREY_C)
    if src.width > width - 0.8:
        src.width = width - 0.8
    inner = VGroup(VGroup(num, t).arrange(RIGHT, buff=0.4, aligned_edge=DOWN), body, src)
    inner.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(width=width, height=max(height, inner.height + 0.55), corner_radius=0.14, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.95)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    return VGroup(box, inner)


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.uses()
        self.in_practice()

    def card(self):
        card = chapter_card(13, r"In practice: \ reaction time at work", r"Where does a reaction time earn its "
                            r"living?", lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: reaction time at work."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def uses(self):
        tiles = VGroup(
            tile(r"2.5 s", r"on the road", r"the reaction time highway design allows a driver: \ at 100 km/h, "
                 rf"{100 / 3.6 * 2.5:.0f} metres before the brakes go on", ROAD,
                 r"AASHTO, \emph{A Policy on Geometric Design of Highways and Streets}"),
            tile(r"0.1 s", r"on a screen", r"a response within about a tenth of a second feels instantaneous; "
                 r"latency is budgeted against it", SCREEN, r"Miller (1968); \ Card, Robertson \& Mackinlay (1991)"),
            tile(r"$\pm$", r"in the clinic", r"slower and more variable reactions: \ part of concussion "
                 r"assessment and of cognitive screening in old age", CLINIC,
                 r"reaction time and its trial-to-trial variability"),
            tile(r"0.100 s", r"on the track", r"a start sooner than this after the gun is a false start: \ no one "
                 r"is held to react that fast", TRACK, r"World Athletics, Technical Rules"),
        ).arrange_in_grid(2, 2, buff=(0.3, 0.25))
        head = heading(r"Where a reaction time earns its living", font_size=34).to_edge(UP, buff=0.25)
        tiles.next_to(head, DOWN, buff=0.25)
        if tiles.get_bottom()[1] < -3.85:
            tiles.scale_to_fit_height(tiles.height - (-3.85 - tiles.get_bottom()[1]))
            tiles.next_to(head, DOWN, buff=0.25)
        # the road, drawn while the first tile is alone on screen
        metres = 100 / 3.6 * 2.5
        xa, xb, yr = -5.9, 1.3, -2.0
        road = VGroup(Line([-6.6, yr, 0], [6.6, yr, 0], color=GREY_B, stroke_width=5),
                      DashedLine([-6.6, yr - 0.45, 0], [6.6, yr - 0.45, 0], color=GREY_D, stroke_width=3))
        car = RoundedRectangle(width=0.95, height=0.42, corner_radius=0.12, stroke_width=0, fill_color=ROAD,
                               fill_opacity=1).move_to([xa, yr + 0.26, 0])
        hazard = VGroup(Triangle(stroke_width=0, fill_color=P.ERR, fill_opacity=1).scale(0.32),
                        label(r"a hazard", font_size=26, color=P.ERR)).arrange(DOWN, buff=0.1)
        hazard.move_to([5.7, yr + 0.62, 0])
        ran = Line([xa, yr - 0.95, 0], [xb, yr - 0.95, 0], color=ROAD, stroke_width=6)
        ran_lab = label(rf"2.5 s at 100 km/h: \ {metres:.0f} m, \ and the brakes are not on yet", font_size=28,
                        color=ROAD).next_to(ran, DOWN, buff=0.12).align_to(ran, LEFT)
        you = Line([xa, yr - 0.95, 0], [xa + (xb - xa) / 10, yr - 0.95, 0], color=WHITE, stroke_width=10)
        you_lab = label(r"your reaction in this video", font_size=24, color=WHITE).next_to(you, UP, buff=0.1)
        you_lab.align_to(you, LEFT)
        steps = VGroup(*[label(t, font_size=28, color=GREY_A) for t in (r"see", r"recognise", r"decide",
                                                                        r"move a foot")])
        for k, t in enumerate(steps):
            t.move_to([xa + (xb - xa) * (k + 0.5) / 4, yr + 1.15, 0])
        seps = VGroup(*[Line([xa + (xb - xa) * k / 4, yr + 0.85, 0], [xa + (xb - xa) * k / 4, yr + 1.45, 0],
                             color=GREY_D, stroke_width=2) for k in range(5)])
        scene = VGroup(road, car, hazard, ran, ran_lab, you, you_lab, steps, seps)
        with self.voiceover(
            "Where does a reaction time earn its living? <bookmark mark='a'/> On the road. An engineer deciding "
            "how far ahead a hazard must be visible needs the driver's reaction time, and the American design "
            f"standard allows two and a half seconds. <bookmark mark='r'/> At a hundred kilometres an hour, "
            f"that's {100 / 3.6 * 2.5:.0f} metres of road. <bookmark mark='s'/> It's about ten times your "
            "reaction in this video, because a real driver isn't waiting with a finger on a key. "
            "<bookmark mark='t'/> There's seeing, recognising, deciding, and moving a foot. Stages, again. <bookmark mark='b'/> On a screen. When a system answers within about "
            "a tenth of a second, it feels instantaneous. Much slower, and the user notices the wait. Interface "
            "engineers budget their latency against that figure. <bookmark mark='c'/> In the clinic. Reaction "
            "time, and especially how much it varies from one trial to the next, is part of concussion "
            "assessment, and of cognitive screening in old age. <bookmark mark='d'/> And on the track. A "
            "sprinter who leaves the blocks less than a tenth of a second after the gun is ruled to have jumped "
            "it, on the grounds that nobody can react that fast. A fact about the nervous system, written into a "
            "rulebook."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tiles[0], shift=UP * 0.2))
            self.play(FadeIn(road), FadeIn(car), FadeIn(hazard))
            vo.wait_until("r")
            self.play(car.animate(rate_func=linear).set_x(xb), Create(ran, rate_func=linear), run_time=2.5)
            self.play(FadeIn(ran_lab))
            vo.wait_until("s")
            self.play(FadeIn(you), FadeIn(you_lab))
            vo.wait_until("t")
            self.play(FadeIn(seps), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in steps], lag_ratio=0.5),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeOut(scene), FadeIn(tiles[1], shift=UP * 0.2))
            for mark, t in zip("cd", tiles[2:]):
                vo.wait_until(mark)
                self.play(FadeIn(t, shift=UP * 0.2))
        self.clear_scene()

    def in_practice(self):
        head = label(r"In practice", font_size=52, color=P.ACCENT)
        rows = VGroup()
        for a, b in (
            (r"Who uses it", r"UX and human-factors engineers, road and vehicle designers, clinical "
                             r"neuropsychologists, sports officials"),
            (r"What to ask of any timing claim", r"What does the number include? \ Which device measured it? \ "
                                                 r"Is it one person's average, or a group's?"),
            (r"What carries over", r"a difference between two conditions is safer than an absolute time; \ a "
                                   r"distribution says more than a mean"),
        ):
            rows.add(VGroup(label(a, font_size=32, color=P.ACCENT), wrapped_label(b, 12.4, 34, WHITE))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.14))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        g = VGroup(head, rows).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(ORIGIN)
        with self.voiceover(
            "So here is this part's practice card. <bookmark mark='a'/> Who uses this: interface and "
            "human-factors engineers, road and vehicle designers, clinical neuropsychologists. "
            "<bookmark mark='b'/> What to ask of any timing claim: what does the number include, which device "
            "measured it, and is it one person's average or a group's? <bookmark mark='c'/> And what carries "
            "over from today: a difference between two conditions is safer than an absolute time, and a "
            "distribution tells you more than a mean."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=LEFT * 0.2))
        self.clear_scene()
