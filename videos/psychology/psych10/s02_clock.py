from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


def _low_points(t, x):
    """The time of each cycle's lowest point (one per cycle, between a fall through zero and the next rise)."""
    out, start = [], None
    for i in range(1, len(x)):
        if x[i - 1] >= 0 > x[i]:
            start = i
        elif x[i - 1] < 0 <= x[i] and start is not None:
            j = start + int(np.argmin(x[start:i]))
            a, b, c = x[j - 1], x[j], x[j + 1]          # a parabola through the three lowest samples
            shift = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) else 0.0
            out.append(float(t[j] + shift * (t[j + 1] - t[j])))
            start = None
    return np.array(out)


class ClockInside(VoiceoverScene):
    def construct(self):
        self.card()
        self.free()
        self.where()
        self.entrain()

    def card(self):
        card = chapter_card(1, r"A clock inside", r"Does the body keep time by itself, and how well?",
                            lit={1938: r"Kleitman's cave"}, part=PART, scale=("molecule", "brain", "person"),
                            marr=("how", "tissue"))
        with self.voiceover(
            "Chapter one. A clock inside."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def free(self):
        c = load("clock")
        cz = archive.CZEISLER_1999.data
        head = heading(r"Left alone, \ the clock runs slow")
        A = axes([0, 288], [-1.3, 1.3], x_length=12.2, y_length=1.7, xticks=[], yticks=[], xlabel=r"", ylabel=r"",
                 center=[0, 1.75, 0])
        ax = A.ax
        grid = VGroup(*[Line(ax.c2p(d * 24, -1.3), ax.c2p(d * 24, 1.3), color=GREY_D, stroke_width=1.5) for d in range(13)])
        wave = curve(ax, c["t"], c["x"], CLOCKC, stroke_width=3.5)
        lows = _low_points(c["t"], c["x"])
        ldots = VGroup(*[Dot(ax.c2p(v, float(c["x"].min())), radius=0.07, color=WHITE) for v in lows])
        cap = label(r"Psyche's clock in the dark, \ twelve days; \ the grey lines are midnights", font_size=26,
                    color=GREY_A).next_to(A, DOWN, buff=0.12)
        drift = (lows - lows[0]) - 24.0 * np.arange(len(lows))
        B = axes([0, 12], [0, 2.4], x_length=5.4, y_length=2.3, xticks=[0, 4, 8, 12], yticks=[0, 1, 2],
                 xlabel=r"day", ylabel=r"how late the low point comes, in hours", center=[-3.6, -1.45, 0])
        bx = B.ax
        ddots = VGroup(*[Dot(bx.c2p(k, float(v)), radius=0.07, color=CLOCKC) for k, v in enumerate(drift) if k <= 12])
        pub = DashedLine(bx.c2p(0, 0), bx.c2p(12, 12 * (cz["period_h"] - 24.0)), color=DATA, stroke_width=3)
        lg = legend([(CLOCKC, rf"the model: \ ${c['free_period']:.2f}$ hours"),
                     (DATA, rf"published: \ ${cz['period_h']:.2f}$ hours")], font_size=26)
        rows = rows_of([
            (rf"{cz['people']} people on a {cz['day_hours']}-hour day for about a month: \ the clock cannot follow, \ so it "
             r"shows its own pace", WHITE),
            (rf"${cz['period_h']:.2f}$ hours: \ 24 hours and 11 minutes, \ nearly the same in everyone", DATA),
            (r"earlier estimates of 25 hours: \ people switched their own lamps, \ and the lamps pushed the clock", GREY_A),
        ], 6.0, 28, 0.24).move_to([3.75, -1.35, 0])
        keep_in_frame(rows)
        lg.move_to(bx.c2p(0.6, 2.05), aligned_edge=LEFT)
        src = published_tag(archive.CZEISLER_1999.cite)
        tag = psyche_tag(r"computed: Psyche's clock (a model)")
        with self.voiceover(
            "Sixty years after the cave, a team at Harvard led by Charles Czeisler settled the question, "
            "and they did it with Kleitman's own trick. <bookmark mark='a'/> Put people on a "
            f"{cz['day_hours']}-hour day, in dim light, for about a month. The body's clock can't follow "
            "a day that long. So it runs at its own pace, and the pace can be read off the body's "
            f"temperature and its hormones. <bookmark mark='b'/> In {cz['people']} people, young and old, "
            f"the clock's own period averaged {cz['period_h']:.2f} hours: twenty-four hours and eleven "
            "minutes, and nearly the same in everyone. <bookmark mark='c'/> Earlier experiments had said "
            "twenty-five. In those, people switched their own lamps on and off, and the lamps were pushing "
            "the clock. <bookmark mark='d'/> At the top is Psyche's clock. It's two equations: an "
            "oscillator of a kind engineers have used for a century, with its period set near the "
            "published one. Left in the dark, its low point comes a little later each day. "
            f"<bookmark mark='e'/> Its period is {c['free_period']:.2f} hours. So the clock is real, it's "
            "built in, and it's wrong. It loses about ten minutes a day, and something has to set it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(grid), FadeIn(cap), FadeIn(B), Create(wave),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(pub), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(ldots, lag_ratio=0.2), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(ddots, lag_ratio=0.2), FadeIn(lg[0]), run_time=1.5)
        self.clear_scene()

    def where(self):
        head = heading(r"Where it is, \ and what it is made of")
        cx = -4.3
        eyes = VGroup(*[VGroup(Circle(radius=0.42, color=VOLT, stroke_width=3),
                               Dot(radius=0.15, color=VOLT)).move_to([cx + s * 1.5, -1.9, 0]) for s in (-1, 1)])
        cross = np.array([cx, -0.2, 0])
        nerves = VGroup()
        for s in (-1, 1):
            nerves.add(Line(eyes[(s + 1) // 2].get_top(), cross, color=LIGHTC, stroke_width=5))
            nerves.add(Line(cross, cross + np.array([-s * 1.3, 1.5, 0]), color=LIGHTC, stroke_width=5, stroke_opacity=0.5))
        scn = VGroup(*[Dot(cross + np.array([s * 0.22, 0.42, 0]), radius=0.14, color=CLOCKC) for s in (-1, 1)])
        ring = Circle(radius=0.55, color=CLOCKC, stroke_width=2).move_to(cross + UP * 0.42)
        scn_lab = wrapped_label(r"the suprachiasmatic nucleus: \ ``above the crossing''", 3.6, 27, CLOCKC)
        scn_lab.next_to(ring, UP, buff=0.9)
        eye_lab = label(r"the eyes, from above", font_size=25, color=GREY_A).next_to(eyes, DOWN, buff=0.15)
        cross_lab = wrapped_label(r"the optic nerves cross", 1.7, 26, LIGHTC).move_to([cx - 1.75, -0.45, 0])
        rows = rows_of([
            (r"about 20{,}000 neurons, \ in a pair of clusters", WHITE),
            (r"destroy it in a rat (1972): \ sleep and waking at all hours; \ the daily rhythm is gone", WHITE),
            (r"transplant one from a hamster with a short day (1990): \ the host takes the donor's period", WHITE),
            (r"and every cell in it keeps time by itself", CLOCKC),
        ], 7.2, 28, 0.2).move_to([3.1, 1.75, 0])
        keep_in_frame(rows)
        loop = loop_diagram([r"clock genes switch on", r"their proteins build up", r"the proteins switch the genes off"],
                            [CLOCKC, CLOCKC, BAD], width=7.6, font_size=25,
                            feedback=r"the proteins decay, \ the genes come back on: \ about a day a turn")
        loop.move_to([3.1, -1.7, 0])
        keep_in_frame(loop)
        tag = note(r"a diagram; \ the animal experiments are described from the textbooks").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Where is it? <bookmark mark='a'/> Follow the optic nerves back from the eyes, to the point "
            "where they cross. Just above that crossing sits a pair of tiny clusters of cells, about "
            "twenty thousand neurons in all. It's called the suprachiasmatic nucleus, which means the "
            "nucleus above the crossing. <bookmark mark='b'/> Destroy it in a rat, and the animal still "
            "sleeps and wakes, but at all hours. The daily rhythm is gone. <bookmark mark='c'/> Transplant "
            "one from a hamster bred to have a short day, and the host animal takes on the donor's period. "
            "The clock went with the tissue. <bookmark mark='d'/> And it isn't the wiring that keeps time. "
            "Each cell does. <bookmark mark='e'/> Inside each one, a set of genes makes proteins that "
            "build up over the hours, and then switch their own genes off. The proteins decay, the genes "
            "come back on, and the loop goes round again: about once a day. Remember the shape of that. A "
            "signal that shuts off its own source, after a delay. A brake that arrives late makes a loop "
            "swing. We'll meet it again before the end of this part, in a different tissue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eyes), FadeIn(eye_lab))
            vo.wait_until("a")
            self.play(Create(nerves), FadeIn(cross_lab), run_time=1.5)
            self.play(FadeIn(scn, scale=1.5), Create(ring), FadeIn(scn_lab), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(loop.boxes, lag_ratio=0.3), FadeIn(loop.arrows), run_time=2.0)
            self.play(Create(loop.back[0]), FadeIn(loop.back[1]), FadeIn(loop.back[2]), run_time=1.5)
        self.clear_scene()

    def entrain(self):
        c = load("clock")
        k = archive.KLEITMAN_1938.data
        hh, mm = spoken_time(c["home_minimum"])
        assert (hh, mm) == (4, 20), (hh, mm)
        head = heading(r"Give it a day, \ and it locks on. \ Up to a point")
        A = axes([0, 96], [-1.4, 1.4], x_length=7.6, y_length=2.2, xticks=[0, 24, 48, 72, 96], yticks=[],
                 xfmt=lambda v: f"{int(v) // 24}", xlabel=r"days; \ shaded: lights off, 23:00 to 7:00", ylabel=r"",
                 center=[-3.0, 1.25, 0])
        ax = A.ax
        nights = night_bands(ax, 0, 96, y0=-1.4, y1=1.4)
        wave = curve(ax, c["home_t"], c["home_x"], CLOCKC, stroke_width=4)
        lows = _low_points(c["home_t"], c["home_x"])
        ldots = VGroup(*[Dot(ax.c2p(v, float(c["home_x"].min())), radius=0.08, color=WHITE) for v in lows])
        face = clock_icon(0.8, CLOCKC, c["home_minimum"]).move_to([2.4, 1.45, 0])
        per_lab = label(rf"period: \ ${c['home_period']:.1f}$ hours", font_size=32, color=CLOCKC)
        low_lab = label(rf"low point at {clock_time(c['home_minimum'])}", font_size=32, color=WHITE)
        why = wrapped_label(r"nobody set that time: \ it is where the pushes from the light balance", 3.4, 27, GREY_A)
        side = VGroup(per_lab, low_lab, why).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(face, RIGHT, buff=0.4)
        keep_in_frame(side)
        boxes = VGroup()
        for d, ok in zip(c["days"], c["locked"]):
            col = MODEL if ok else BAD
            box = RoundedRectangle(width=0.9, height=1.0, corner_radius=0.1, color=col, stroke_width=3, fill_color=col,
                                   fill_opacity=0.15)
            boxes.add(VGroup(box, label(rf"{int(d)} h", font_size=29, color=col).move_to(box.get_center() + UP * 0.18),
                             label(r"locks" if ok else r"drifts", font_size=24, color=col).move_to(box.get_center() + DOWN * 0.24)))
        boxes.arrange(RIGHT, buff=0.1).move_to([-3.25, -1.85, 0])
        bcap = label(r"the length of day the clock is given", font_size=26, color=GREY_A).next_to(boxes, UP, buff=0.15)
        rows = rows_of([
            (rf"on the cave's {k['day_hours']}-hour day the model does what Kleitman did: \ it runs at "
             rf"${c['cave_period_dim']:.1f}$ to ${c['cave_period_room']:.1f}$ hours", CLOCKC),
            (r"and Richardson? \ People's clocks differ. \ From two people, nobody can say why he adapted", GREY_A),
        ], 5.3, 28, 0.3).move_to([4.1, -1.85, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's clock; \ 16 hours of room light, 8 of darkness")
        with self.voiceover(
            "Now give the clock a day: sixteen hours of ordinary room light, and eight of darkness. "
            "<bookmark mark='a'/> It locks on. Its period becomes twenty-four hours exactly, and its low "
            "point settles at twenty past four in the morning. That's close to where the low point of "
            "body temperature sits in someone who sleeps from eleven to seven. Nobody set that time. It's "
            "where the pushes from the light balance out. <bookmark mark='b'/> But light can only pull "
            "the clock so far. Shorten the day, or lengthen it, and ask whether the clock follows. "
            "Twenty-three hours: yes. Twenty-five: yes. Twenty-two, or twenty-six and beyond: no. "
            f"<bookmark mark='c'/> So on the cave's {k['day_hours']}-hour day, the model does what "
            f"Kleitman did. It ignores the schedule, and runs at about {c['cave_period_dim']:.1f} hours. "
            "<bookmark mark='d'/> And Richardson? The model has one clock, and people's clocks differ: in "
            "their period, and in how hard light pushes them. Whether that's why the younger man adapted, "
            "nobody can say from two people. What we can say is that Kleitman's result is the one that a "
            "clock like this predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(nights), Create(wave), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(ldots, lag_ratio=0.3), FadeIn(face), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(bcap), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.5), run_time=9.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), Indicate(boxes[-1], color=BAD, scale_factor=1.08))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
