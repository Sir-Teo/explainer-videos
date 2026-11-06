from __future__ import annotations

from datetime import datetime, timedelta, timezone

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, load, mono, trace)


def clock_face(color, r=0.95):
    """An analogue clock: rim, twelve ticks and one hand (``face.hand``)."""
    rim = Circle(radius=r, color=color, stroke_width=3)
    ticks = VGroup(*[Line(rim.get_center() + r * 0.85 * np.array([np.cos(a), np.sin(a), 0]),
                          rim.get_center() + r * np.array([np.cos(a), np.sin(a), 0]), color=GREY_B,
                          stroke_width=2) for a in np.linspace(0, 2 * PI, 12, endpoint=False)])
    hand = Line(ORIGIN, UP * r * 0.75, color=WHITE, stroke_width=4)
    hub = Dot(radius=0.06, color=WHITE)
    g = VGroup(rim, ticks, hand, hub)
    g.hand = hand
    return g


class Time(VoiceoverScene):
    def construct(self):
        self.card()
        self.clocks()
        self.dst()
        self.leap()
        self.y2038()
        self.rules()
        self.skew()

    def card(self):
        card = chapter_card(12, r"Time in APIs", r"What time is it, \ and how long did that take?",
                            lit=(1972, 2022), extra=((1972, r"the first leap second"),
                                                     (2022, r"CGPM: \ leap seconds to end by 2035")), part=PART)
        with self.voiceover("Chapter twelve. Time in APIs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def clocks(self):
        head = label(r"Two clocks", font_size=36).to_edge(UP, buff=0.3)
        face = clock_face(DATA).move_to([-3.6, 1.15, 0])
        wt = label(r"wall clock \ (\texttt{CLOCK\_REALTIME})", font_size=20, color=DATA).next_to(face, UP, buff=0.15)
        mt = label(r"monotonic clock \ (\texttt{CLOCK\_MONOTONIC})", font_size=20, color=YES).move_to(
            [3.6, wt.get_y(), 0])
        counter = mono("5031.2", size=40, color=YES)
        cbox = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.12, stroke_color=YES, stroke_width=2).move_to(
            [3.6, 1.15, 0])
        counter.move_to(cbox)
        cunit = label(r"seconds since boot", font_size=16, color=GREY_B).next_to(cbox, DOWN, buff=0.1)

        wr = [mono("start      12:00:00.0", size=17, color=WHITE), mono("end        11:59:59.3", size=17, color=WHITE),
              mono("end - start = -0.7 s", size=17, color=NO)]
        mr = [mono("start      5031.2", size=17, color=WHITE), mono("end        5032.5", size=17, color=WHITE),
              mono("end - start = 1.3 s", size=17, color=YES)]
        wg = VGroup(*wr).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.6, -0.75, 0])
        mg = VGroup(*mr).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -0.75, 0])
        step = label(r"NTP steps it back 2\,s", font_size=19, color=NO).next_to(face, RIGHT, buff=0.25)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(wg, DOWN, buff=0.15).align_to(wg, LEFT)
        notes = VGroup(
            wrapped_label(r"the wall clock is a date: \ set by NTP, \ by people, \ by a virtual machine resuming; \ "
                          r"it can jump either way \ (Part 38)", 6.0, font_size=19, color=DATA),
            wrapped_label(r"the monotonic clock only moves forwards; \ it means nothing as a date or on another "
                          r"machine, \ but it is the one to time requests with", 6.0, font_size=19, color=YES),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A computer has more than one clock, and Part 38 showed that no two machines' clocks agree. "
            "<bookmark mark='a'/> The wall clock tells the date and time of day. It is set by NTP, by people, and it "
            "can jump, backwards as well as forwards. <bookmark mark='b'/> Time a request with it, and if the clock "
            "is stepped back while the request runs, the duration comes out negative. <bookmark mark='c'/> The "
            "monotonic clock only ever moves forwards. It means nothing as a date and nothing on another machine, but"
            " it is the right clock for timeouts, retries and latency."
        ) as vo:
            self.play(FadeIn(head), FadeIn(face), FadeIn(wt), Create(cbox), FadeIn(counter), FadeIn(mt),
                      FadeIn(cunit))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(wr[0]), FadeIn(mr[0]), FadeIn(ill))
            c = face[0].get_center()
            self.play(Rotate(face.hand, -PI / 3, about_point=c),
                      Transform(counter, mono("5031.9", size=40, color=YES).move_to(cbox)), run_time=1.0)
            self.play(Rotate(face.hand, 2 * PI / 3, about_point=c), face[0].animate.set_color(NO), FadeIn(step),
                      run_time=0.5)
            self.play(Rotate(face.hand, -PI / 4, about_point=c), face[0].animate.set_color(DATA),
                      Transform(counter, mono("5032.5", size=40, color=YES).move_to(cbox)), run_time=1.0)
            self.play(FadeIn(wr[1]), FadeIn(mr[1]))
            self.play(FadeIn(wr[2]), FadeIn(mr[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Circumscribe(mg, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def dst(self):
        T = load("time")
        g = T["dst_gap"]
        start = datetime.fromisoformat(g["start"])
        wall = datetime.fromisoformat(g["plus_1h_wall"])
        norm = datetime.fromisoformat(g["normalized"])
        head = label(r"The hour that does not exist", font_size=36).to_edge(UP, buff=0.3)
        sub = label(r"New York, \ 8 March 2026", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.15)
        t0 = start.astimezone(timezone.utc).replace(hour=4, minute=0)
        # the clocks change at 02:00 standard time: before it the start's offset (EST), after it the normalized
        # time's (EDT), both read from the computed data
        names = {start.utcoffset(): "EST", norm.utcoffset(): "EDT"}
        change = start.replace(hour=2, minute=0).astimezone(timezone.utc)
        y = 0.75

        def X(dt):
            return -5.3 + 1.8 * (dt.astimezone(timezone.utc) - t0).total_seconds() / 3600

        def local(t):
            return t.astimezone(start.tzinfo if t < change else norm.tzinfo)
        axis = Line([X(t0) - 0.25, y, 0], [X(t0 + timedelta(hours=6)) + 0.25, y, 0], color=GREY_C, stroke_width=2)
        ticks, utc_l, loc_l = VGroup(), VGroup(), VGroup()
        for h in range(7):
            t = t0 + timedelta(hours=h)
            loc = local(t)
            nm = names[loc.utcoffset()]
            x = X(t)
            ticks.add(Line([x, y - 0.08, 0], [x, y + 0.08, 0], color=GREY_C, stroke_width=2))
            utc_l.add(label(t.strftime("%H:%M") + r"\,Z", font_size=16, color=GREY_B).next_to([x, y, 0], DOWN,
                                                                                               buff=0.15))
            loc_l.add(label(loc.strftime("%H:%M ") + nm, font_size=17,
                            color=DATA if nm == "EST" else LAM).next_to([x, y, 0], UP, buff=0.15))
        jump = X(change)
        ul = label(r"UTC", font_size=16, color=GREY_B).next_to(utc_l, LEFT, buff=0.2)
        ll = label(r"local", font_size=16, color=GREY_A).next_to(loc_l, LEFT, buff=0.2)
        gap = RoundedRectangle(width=3.0, height=0.85, corner_radius=0.1, stroke_color=NO, stroke_width=2,
                               fill_color=NO, fill_opacity=0.12).move_to([jump, 2.15, 0])
        gl = label(r"02:00--02:59: \ never shown", font_size=17, color=NO).move_to(gap).shift(DOWN * 0.18)
        jl = DashedLine(gap.get_bottom(), [jump, y + 0.55, 0], color=NO, stroke_width=2, dash_length=0.07)
        s_dot = Dot([X(start), y, 0], radius=0.1, color=HEAD)
        s_l = label(start.strftime("%H:%M ") + names[start.utcoffset()], font_size=17, color=HEAD).next_to(s_dot, DOWN,
                                                                                                 buff=0.55)
        ghost = label(wall.strftime("%H:%M") + r"\ ?", font_size=19, color=NO).move_to(gap).shift(UP * 0.18)
        n_dot = Dot([X(norm), y, 0], radius=0.1, color=YES)
        n_l = label(norm.strftime("%H:%M ") + names[norm.utcoffset()], font_size=17, color=YES).next_to(
            n_dot, DOWN, buff=0.55)
        br = BraceBetweenPoints([X(start), y - 0.95, 0], [X(norm), y - 0.95, 0], direction=DOWN, color=GREY_A)
        bl = label(rf"{g['elapsed_hours']:g} real hour", font_size=17, color=GREY_A).next_to(br, DOWN, buff=0.08)
        code = code_block([
            "start = datetime(2026, 3, 8, 1, 30, tzinfo=ZoneInfo('America/New_York'))",
            f"start + timedelta(hours=1)   # {g['plus_1h_wall']}: no such wall time",
            f"normalized through UTC       # {g['normalized']}",
        ], size=15).move_to([0, -1.85, 0])
        code[1].set_color(NO)
        code[2].set_color(YES)
        lh = T["lord_howe_offset"][:5]
        note = wrapped_label(rf"offsets are not even whole hours: \ Lord Howe Island is UTC$+${lh}, \ and its "
                             r"daylight saving shift is half an hour \ (computed with Python's \texttt{zoneinfo})",
                             12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Time zones make the wall clock stranger still. <bookmark mark='a'/> In New York on the eighth of March "
            "2026, clocks jump from two in the morning straight to three. The hour between never happens there. "
            "<bookmark mark='b'/> Start at half past one and add one hour of wall-clock time, and Python's zoneinfo "
            "hands back half past two, a time that does not exist that day. <bookmark mark='c'/> Normalized through "
            "UTC, it is half past three, daylight time: exactly one real hour later. <bookmark mark='d'/> Nor are "
            "offsets whole hours. Lord Howe Island is ten and a half hours ahead of UTC, and its clocks change by "
            "half an hour."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(axis), FadeIn(ticks), FadeIn(utc_l), FadeIn(ul))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in loc_l], lag_ratio=0.25), FadeIn(ll), run_time=1.6)
            self.play(Create(jl), FadeIn(gap), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_l), FadeIn(code[0]))
            self.play(FadeIn(ghost, shift=UP * 0.2), FadeIn(code[1]))
            vo.wait_until("c")
            self.play(FadeIn(n_dot, scale=0.5), FadeIn(n_l), GrowFromCenter(br), FadeIn(bl), FadeIn(code[2]))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def leap(self):
        T = load("time")
        head = label(r"Leap seconds", font_size=36).to_edge(UP, buff=0.3)
        frame = RoundedRectangle(width=4.6, height=1.2, corner_radius=0.12, stroke_color=GREY_B,
                                 stroke_width=2).move_to([-3.6, 1.6, 0])
        shown = mono("23:59:58", size=44, color=WHITE).move_to(frame)
        dl = label(r"31 December 2016, \ UTC", font_size=17, color=GREY_A).next_to(frame, UP, buff=0.12)
        A = axes([0, 24, 6], [0, 1.2, 0.5], x_length=5.4, y_length=2.4, xticks=[0, 12, 24], yticks=[1],
                 fx=lambda v: {0: r"noon", 12: r"midnight", 24: r"noon"}[v], fy=lambda v: f"{v:g}\\,s")
        A.move_to([3.4, 1.15, 0])
        ax = A.ax
        al = label(r"how far the clock has fallen behind", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.12)
        stepc = trace(ax, [(0, 0), (12, 0), (12, 1), (24, 1)], NO, width=3)
        smear = trace(ax, [(0, 0), (24, 1)], YES, width=3)
        sl = label(r"one step", font_size=16, color=NO).next_to(ax.c2p(12, 0.75), LEFT, buff=0.12)
        ml = label(r"a smear", font_size=16, color=YES).next_to(ax.c2p(18, 0.75), DR, buff=0.05)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(ax, UP, buff=0.45).align_to(ax, RIGHT)
        cnt = label(rf"{T['leap_seconds_since_1972']} leap seconds inserted since 1972", font_size=24,
                    color=HEAD).next_to(frame, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"code that assumes a minute has sixty seconds meets one with sixty-one; \ the leap second "
                          r"of 2012 hung servers at several large sites", 12.4, font_size=20, color=NO),
            wrapped_label(r"Google, \ from 2008: \ \textbf{smear} the extra second over many hours, \ so no clock "
                          r"ever reads \texttt{:60}", 12.4, font_size=20, color=YES),
            wrapped_label(r"2022: \ the General Conference on Weights and Measures decided to stop adding leap "
                          r"seconds by 2035", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "UTC also has extra seconds. <bookmark mark='a'/> The Earth's rotation wanders, and to keep clocks in "
            "step with it a leap second is occasionally inserted: the clock reads twenty-three fifty-nine and sixty "
            "seconds. <bookmark mark='b'/> Twenty-seven have been added since 1972. Code that assumes every minute "
            "has sixty seconds meets one with sixty-one, and the leap second of 2012 hung servers at several large "
            "sites. <bookmark mark='c'/> Since 2008 Google has smeared the extra second instead, running its clocks "
            "slightly slow for hours, so that no clock ever shows sixty. <bookmark mark='d'/> And in 2022 the General"
            " Conference on Weights and Measures decided to stop adding leap seconds by 2035."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(shown), FadeIn(dl))
            vo.wait_until("a")
            for s, c in (("23:59:59", WHITE), ("23:59:60", HEAD), ("00:00:00", WHITE)):
                self.play(Transform(shown, mono(s, size=44, color=c).move_to(frame)), run_time=0.5)
                self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(cnt), FadeIn(notes[0]))
            self.play(FadeIn(A), FadeIn(al), Create(stepc), FadeIn(sl), FadeIn(ill))
            vo.wait_until("c")
            self.play(Create(smear), FadeIn(ml), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def y2038(self):
        T = load("time")
        last = datetime.fromisoformat(T["unix_2038"])
        wrapped = last - timedelta(seconds=2 ** 32 - 1)      # one second later, read as a signed 32-bit number
        head = label(r"19 January 2038", font_size=36).to_edge(UP, buff=0.3)
        w = 0.36
        cells = VGroup(*[Square(w - 0.04, stroke_color=GREY_B, stroke_width=1.2) for _ in range(32)]).arrange(
            RIGHT, buff=0.04).move_to([0, 1.5, 0])
        cells[0].set_stroke(LAM, 2)
        bits = VGroup(*[mono("0" if i == 0 else "1", size=18, color=LAM if i == 0 else DATA).move_to(c)
                        for i, c in enumerate(cells)])
        sign = label(r"sign", font_size=16, color=LAM).next_to(cells[0], UP, buff=0.1)
        tl = label(r"Unix time: \ seconds since 1970, \ in a signed 32-bit integer", font_size=19,
                   color=GREY_A).next_to(cells, UP, buff=0.45)
        before = VGroup(label(rf"$2^{{31}} - 1 = {2 ** 31 - 1:,}$".replace(",", "{,}"), font_size=24, color=DATA),
                        mono(last.strftime("%Y-%m-%dT%H:%M:%SZ"), size=22, color=DATA)).arrange(RIGHT, buff=0.5)
        before.next_to(cells, DOWN, buff=0.4)
        plus = label(r"$+1$\,s", font_size=26, color=HEAD).next_to(cells[-1], UP, buff=0.12)
        after = VGroup(label(rf"$-2^{{31}} = {-2 ** 31:,}$".replace(",", "{,}"), font_size=24, color=NO),
                       mono(wrapped.strftime("%Y-%m-%dT%H:%M:%SZ"), size=22, color=NO)).arrange(RIGHT, buff=0.5)
        after.next_to(before, DOWN, buff=0.35)
        notes = VGroup(
            wrapped_label(r"the carry ripples through all 31 value bits into the sign: \ the largest positive "
                          r"number becomes the most negative \ (Part 4's two's complement)", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"operating systems have moved to a 64-bit \texttt{time\_t}; \ the bug survives in file "
                          r"formats, \ database columns and protocol fields that kept 32 bits", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Then there are the bits a time is stored in. <bookmark mark='a'/> Unix time counts seconds since 1970. "
            "In a signed 32-bit integer, the largest value, two to the thirty-one minus one, is seven seconds past "
            "three fourteen in the morning of the nineteenth of January 2038. <bookmark mark='b'/> One second later, "
            "the carry ripples all the way into the sign bit, and the clock reads December 1901. <bookmark mark='c'/>"
            " Operating systems have moved to 64 bits, but the bug lives on wherever a file format, a database column"
            " or a protocol field kept only 32."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(cells), FadeIn(sign))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=0.03), run_time=1.2)
            self.play(FadeIn(before))
            vo.wait_until("b")
            self.play(FadeIn(plus))
            flips = [Transform(bits[i], mono("0", size=18, color=GREY_B).move_to(cells[i])) for i in range(31, 0, -1)]
            self.play(LaggedStart(*flips, lag_ratio=0.12), run_time=2.2)
            self.play(Transform(bits[0], mono("1", size=18, color=NO).move_to(cells[0])),
                      cells[0].animate.set_stroke(NO, 3), FadeIn(after), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        T = load("time")
        start = datetime.fromisoformat(T["dst_gap"]["start"])
        utc = start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        head = label(r"Rules for time in an API", font_size=36).to_edge(UP, buff=0.3)
        spec = [(r"store instants in UTC", utc, YES),
                (r"keep the zone \textit{name} for local times, \ not an offset", "America/New_York, not -05:00",
                 DATA),
                (r"on the wire, \ ISO 8601 \ (RFC 3339), \ with the offset", start.isoformat(), LAM),
                (r"measure durations with a monotonic clock", "time.monotonic()", HEAD),
                (r"never do calendar arithmetic by adding seconds", "8 March 2026 in New York: 23 hours", NO)]
        rows = VGroup()
        for i, (r, ex, c) in enumerate(spec):
            n = label(f"{i + 1}", font_size=24, color=c)
            t = wrapped_label(r, 5.4, font_size=21, color=WHITE)
            e = mono(ex, size=16, color=c)
            rows.add(VGroup(n, t, e))
        for k, row in enumerate(rows):
            yy = 2.2 - k * 0.95
            row[0].move_to([-6.3, yy, 0])
            row[1].move_to([-5.9, yy, 0], aligned_edge=LEFT)
            row[2].move_to([0.6, yy, 0], aligned_edge=LEFT)
        rules_ = VGroup(*[Line([-6.6, 2.2 - k * 0.95 - 0.47, 0], [6.6, 2.2 - k * 0.95 - 0.47, 0], color=GREY_E,
                               stroke_width=1) for k in range(4)])
        note = wrapped_label(r"an offset says where a time was, \ once; \ a zone name says how that place's clocks "
                             r"will change, \ which a meeting next July needs", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So an API that handles time keeps a few rules. <bookmark mark='a'/> Store instants in UTC. "
            "<bookmark mark='b'/> For a local time, such as a meeting, keep the zone's name, America slash New York, "
            "rather than an offset: the offset changes twice a year, and the zone's rules change by law. "
            "<bookmark mark='c'/> On the wire, write ISO 8601, in the RFC 3339 profile, with the offset included. "
            "<bookmark mark='d'/> Measure durations with the monotonic clock. <bookmark mark='e'/> And never do "
            "calendar arithmetic by adding seconds: in New York, the eighth of March 2026 had only twenty-three "
            "hours."
        ) as vo:
            self.play(FadeIn(head), Create(rules_))
            for mk, row in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(row[0]), FadeIn(row[1]), FadeIn(row[2], shift=LEFT * 0.2))
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def skew(self):
        head = label(r"Expiry, \ and clocks that disagree", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, tmax = -4.4, 6.2, 12.0

        def X(m):
            return x0 + (x1 - x0) * m / tmax
        ya, yb = 1.7, 0.4
        axis = Line([X(0), -0.5, 0], [X(tmax), -0.5, 0], color=GREY_C, stroke_width=1.5)
        tk = VGroup(*[VGroup(Line([X(m), -0.56, 0], [X(m), -0.44, 0], color=GREY_C),
                             label(f"{m}", font_size=16, color=GREY_B).next_to([X(m), -0.5, 0], DOWN, buff=0.1))
                      for m in range(0, 13, 2)])
        unit = label(r"real minutes", font_size=16, color=GREY_B).next_to(tk, DOWN, buff=0.12)
        na = label(r"A stores the key", font_size=18, color=DATA).move_to([x0 - 0.15, ya, 0], aligned_edge=RIGHT)
        nb = label(r"B checks it, \ 2\,min fast", font_size=18, color=LAM).move_to([x0 - 0.15, yb, 0],
                                                                                   aligned_edge=RIGHT)
        va = Rectangle(width=X(10) - X(0), height=0.42, stroke_width=0, fill_color=YES, fill_opacity=0.55).move_to(
            [(X(0) + X(10)) / 2, ya, 0])
        val = label(r"valid for 10 minutes", font_size=17, color=BLACK).move_to(va)
        vb = Rectangle(width=X(8) - X(0), height=0.42, stroke_width=0, fill_color=YES, fill_opacity=0.55).move_to(
            [(X(0) + X(8)) / 2, yb, 0])
        eb = Rectangle(width=X(tmax) - X(8), height=0.42, stroke_width=0, fill_color=NO, fill_opacity=0.45).move_to(
            [(X(8) + X(tmax)) / 2, yb, 0])
        ebl = label(r"expired", font_size=17, color=WHITE).move_to(eb)
        rt = DashedLine([X(9), ya + 0.55, 0], [X(9), -0.5, 0], color=HEAD, stroke_width=2.5, dash_length=0.08)
        rl = label(r"a retry at 9 minutes", font_size=17, color=HEAD).next_to(rt, UP, buff=0.08)
        twice = label(r"treated as new: \ charged twice", font_size=18, color=NO).next_to(eb, DOWN, buff=0.12)
        twice.align_to(eb, RIGHT)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(tk, DOWN, buff=0.12).align_to(tk, RIGHT)
        notes = VGroup(
            wrapped_label(r"let one clock decide expiry, \ the one that stored the key; \ keep keys far longer than "
                          r"clients retry, \ plus any skew", 12.4, font_size=20, color=YES),
            wrapped_label(r"where order across machines matters, \ use Part 38's hybrid logical clocks, \ not wall "
                          r"clocks that are assumed to agree", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Clocks also meet chapter five's idempotency keys. <bookmark mark='a'/> A key is kept for a limited time,"
            " here ten minutes, and a request that arrives after it expires is treated as new. <bookmark mark='b'/> "
            "If the service that checks the key runs two minutes fast, the key expires early, and a retry at nine "
            "minutes is charged a second time. <bookmark mark='c'/> So let one clock decide expiry, keep keys far "
            "longer than any client retries, and where order across machines matters, use Part 38's hybrid logical "
            "clocks rather than trusting wall clocks to agree."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tk), FadeIn(unit), FadeIn(ill), FadeIn(na), FadeIn(nb))
            vo.wait_until("a")
            self.play(GrowFromEdge(va, LEFT), FadeIn(val))
            vo.wait_until("b")
            self.play(GrowFromEdge(vb, LEFT))
            self.play(FadeIn(eb), FadeIn(ebl))
            self.play(Create(rt), FadeIn(rl))
            self.play(FadeIn(twice))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
