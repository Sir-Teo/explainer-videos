from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


def _window(d, lo, hi, prefix=""):
    t = d[prefix + "t"]
    k = (t >= lo) & (t <= hi)
    return t[k], d[prefix + "S"][k], d[prefix + "upper"][k], d[prefix + "lower"][k], d[prefix + "asleep"][k]


class TwoProcess(VoiceoverScene):
    def construct(self):
        self.card()
        self.pressure()
        self.gate()
        self.recovery()
        self.second_wind()

    def card(self):
        card = chapter_card(4, r"Two processes", r"What decides when you sleep, and for how long?",
                            lit={1982: r"the two-process model"}, part=PART, scale=("brain", "person"), marr=("what", "how"))
        with self.voiceover(
            "Chapter four. Two processes."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def pressure(self):
        d = load("sleep")
        b = archive.BORBELY_1982.data
        t, S, _, _, asleep = _window(d, 48, 96)
        head = heading(r"Process S: \ the pressure to sleep")
        A = axes([48, 96], [0, 0.8], x_length=7.6, y_length=3.6, xticks=[], yticks=[],
                 xlabel=r"two days; \ shaded: asleep", ylabel=r"sleep pressure", center=[-3.0, -0.2, 0])
        ax = A.ax
        A.add(hour_labels(ax, [48, 60, 72, 84, 96], 0))
        bands = sleep_bands(ax, t, asleep, 0, 0.8)
        line = curve(ax, t, S, SLEEPC, stroke_width=4.5)
        up = label(r"awake: \ $\dfrac{dS}{dt} = \dfrac{1 - S}{18.2}$", font_size=31, color=WHITE)
        down = label(r"asleep: \ $\dfrac{dS}{dt} = -\dfrac{S}{4.2}$", font_size=31, color=SLEEPC)
        eqs = VGroup(up, down).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows = rows_of([
            (rf"awake, it rises toward a ceiling: \ time constant ${b['tau_rise_h']:.1f}$ hours", WHITE),
            (rf"asleep, it falls, four times as fast: \ ${b['tau_fall_h']:.1f}$ hours", SLEEPC),
            (r"measured from the slow waves of deep sleep: \ the longer awake, the larger they start, \ and they die away "
             r"along this curve", GREY_A),
            (r"one ingredient: \ adenosine, which builds up in the waking brain", THRESH),
        ], 5.1, 28, 0.24)
        side = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.3, -0.25, 0])
        keep_in_frame(side)
        src = published_tag(archive.BORBELY_1982.cite)
        tag = psyche_tag(r"computed: Psyche, with the published time constants")
        with self.voiceover(
            "In 1982 the Swiss sleep scientist Alexander Borbély proposed that the timing of sleep comes "
            "from two processes, and only two. <bookmark mark='a'/> The first he called process S, for "
            "sleep. It's a pressure. While you're awake it rises, quickly at first and then more slowly, "
            "toward a ceiling. <bookmark mark='b'/> While you're asleep it falls, about four times as "
            "fast. <bookmark mark='c'/> And it isn't a figure of speech. It was measured, from the slow "
            "waves of deep sleep. The longer someone has been awake, the larger the slow waves at the "
            "start of their sleep, and through the night they die away along this falling curve. The time "
            f"constants are the published ones: about {b['tau_rise_h']:.0f} hours on the way up, and "
            f"about {b['tau_fall_h']:.0f} on the way down. <bookmark mark='d'/> What the pressure is made "
            "of is still argued over. One ingredient is a molecule called adenosine, which builds up in "
            "the brain during waking. Keep that name in mind. We'll need it in chapter nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(bands))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(up), FadeIn(rows[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(down), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def gate(self):
        d = load("sleep")
        hb, mb = spoken_time(d["bed"])
        hr, mr = spoken_time(d["rise"])
        assert (hb, hr) == (22, 7) and mb > 50 and mr < 10, (hb, mb, hr, mr)
        t, S, hi, lo, asleep = _window(d, 48, 144)
        head = heading(r"Process C: \ the clock opens and closes the gate")
        A = axes([48, 144], [-0.12, 0.9], x_length=8.0, y_length=4.2, xticks=[], yticks=[],
                 xlabel=r"four days; \ shaded: asleep", ylabel=r"", center=[-2.85, -0.3, 0])
        ax = A.ax
        A.add(hour_labels(ax, [48, 60, 72, 84, 96, 108, 120, 132, 144], -0.12))
        bands = sleep_bands(ax, t, asleep, -0.12, 0.9)
        upper = curve(ax, t, hi, CLOCKC, stroke_width=3)
        lower = curve(ax, t, lo, CLOCKC, stroke_width=3)
        line = curve(ax, t, S, SLEEPC, stroke_width=4.5)
        tb, tr = 48 + d["bed"], 72 + d["rise"]
        db = Dot(ax.c2p(tb, float(np.interp(tb, t, S))), radius=0.1, color=WHITE)
        dr = Dot(ax.c2p(tr, float(np.interp(tr, t, S))), radius=0.1, color=WHITE)
        ulab = VGroup(db, label(r"sleep begins", font_size=26, color=WHITE).next_to(db, UP, buff=0.12))
        llab = VGroup(dr, label(r"sleep ends", font_size=26, color=WHITE).next_to(dr, DOWN, buff=0.12))
        rows = rows_of([
            (r"the clock moves two thresholds through the day: \ lowest in the small hours, \ highest around midday", CLOCKC),
            (r"the pressure reaches the upper one: \ sleep", SLEEPC),
            (r"it falls to the lower one: \ waking", SLEEPC),
            (rf"the model sleeps from {clock_time(d['bed'])} to {clock_time(d['rise'])}: \ ${d['usual']:.1f}$ hours", WHITE),
            (r"but the thresholds were set to make an ordinary night come out right. \ The test is the nights they were "
             r"not set on", THRESH),
        ], 4.5, 28, 0.24).move_to([4.65, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.BORBELY_1982.cite)
        tag = psyche_tag(r"computed: Psyche, the two-process model")
        with self.voiceover(
            "The second is process C, for circadian: the clock of chapter one. <bookmark mark='a'/> In the "
            "model, the clock moves two thresholds up and down through the day. They're lowest in the "
            "small hours, and highest around the middle of the day. <bookmark mark='b'/> When the "
            "pressure climbs to the upper threshold, sleep begins. <bookmark mark='c'/> When it has "
            "fallen to the lower one, sleep ends. So a pressure that would put you to sleep at four in "
            "the morning isn't enough to do it at noon. <bookmark mark='d'/> Run it, and the model sleeps "
            f"from about eleven at night to seven in the morning: {d['usual']:.1f} hours a night. "
            "<bookmark mark='e'/> That by itself proves little, because the thresholds were set so that "
            "an ordinary night comes out right. The test of a model is what it says about the nights it "
            "wasn't set on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(upper), Create(lower), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(bands), FadeIn(ulab), FadeIn(rows[1]), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(llab), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def recovery(self):
        d = load("sleep")
        t, S, hi, lo, asleep = _window(d, 24, 120, "lost_")
        peak = float(S.max())
        extra = 60 * (d["recovery"] - d["usual"])
        head = heading(r"A night without sleep, \ and the night after")
        A = axes([24, 120], [0, 1.08], x_length=8.0, y_length=4.2, xticks=[], yticks=[],
                 xlabel=r"four days; \ shaded: asleep", ylabel=r"", center=[-2.85, -0.3, 0])
        ax = A.ax
        A.add(hour_labels(ax, [24, 36, 48, 60, 72, 84, 96, 108, 120], 0))
        bands = sleep_bands(ax, t, asleep, 0, 1.08)
        upper = curve(ax, t, hi, CLOCKC, stroke_width=2.5)
        lower = curve(ax, t, lo, CLOCKC, stroke_width=2.5)
        line = curve(ax, t, S, SLEEPC, stroke_width=4.5)
        awake = VGroup(Line(ax.c2p(31, 0.95), ax.c2p(71, 0.95), color=THRESH, stroke_width=4),
                       *[Line(ax.c2p(v, 0.92), ax.c2p(v, 0.98), color=THRESH, stroke_width=4) for v in (31, 71)])
        alab = label(rf"awake for {d['awake_before']:.0f} hours", font_size=27, color=THRESH).next_to(awake, UP, buff=0.08)
        rlab = label(rf"${d['recovery']:.1f}$ h asleep", font_size=27, color=SLEEPC).next_to(ax.c2p(71.5, 0.95), RIGHT, buff=0.1)
        rows = rows_of([
            (rf"the pressure climbs to ${peak:.2f}$, \ far past where sleep would begin", SLEEPC),
            (rf"the sleep that follows: \ ${d['recovery']:.1f}$ hours. \ Not sixteen: \ {extra:.0f} minutes more than "
             r"usual", WHITE),
            (r"why: \ the pressure falls fastest when it is highest, \ so a debt is paid in depth, not length; \ and the "
             r"clock ends the sleep in the morning", GREY_A),
            (r"sleepers do this: \ after a lost night, \ a little longer and much deeper", THRESH),
        ], 4.5, 28, 0.26).move_to([4.65, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche, the two-process model")
        with self.voiceover(
            "So keep the model awake. It wakes at seven, skips a night, and goes to bed at eleven the next "
            f"evening, after {d['awake_before']:.0f} hours. <bookmark mark='a'/> The pressure keeps "
            "climbing, far past the level where sleep would normally begin. <bookmark mark='b'/> And the "
            f"sleep that follows lasts {d['recovery']:.1f} hours. Not sixteen. It lost a whole night, and "
            f"it sleeps about {extra:.0f} minutes longer than usual. <bookmark mark='c'/> There are two "
            "reasons, and both are in the curves. The pressure falls fastest when it's highest. So a "
            "large debt is paid off mostly in depth, in more and larger slow waves, and only a little in "
            "length. And the clock ends the sleep in the morning, whatever is still owed. "
            "<bookmark mark='d'/> That's what sleepers do. After a lost night people sleep somewhat "
            "longer, and much more deeply. The model was built to predict the slow waves of that recovery "
            "night, and it does it with two time constants. For a model with almost nothing in it, "
            "that's a success."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(upper), Create(lower), FadeIn(awake), FadeIn(alab))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(bands), FadeIn(rows[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rlab, scale=1.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def second_wind(self):
        a = load("alert")
        hh, mm = spoken_time(a["lowest_clock"])
        assert (hh, mm) == (5, 22), (hh, mm)
        low_t = 48 + a["lowest_clock"]
        head = heading(r"Awake all night: \ the second wind")
        A = axes([31, 71], [-1.15, 0.0], x_length=8.0, y_length=4.2, xticks=[], yticks=[],
                 xlabel=r"forty hours awake; \ shaded: the night", ylabel=r"alertness", center=[-2.85, -0.3, 0])
        ax = A.ax
        A.add(hour_labels(ax, [36, 42, 48, 54, 60, 66], -1.15))
        night = night_bands(ax, 31, 71, y0=-1.15, y1=0.0)
        line = curve(ax, a["night_t"], a["night_a"], MODEL, stroke_width=4.5)
        dl = Dot(ax.c2p(low_t, a["at_dawn"]), radius=0.1, color=BAD)
        dn = Dot(ax.c2p(63.0, a["next_afternoon"]), radius=0.1, color=MODEL)
        ll = label(rf"lowest at {clock_time(a['lowest_clock'])}", font_size=27, color=BAD).next_to(dl, DOWN, buff=0.12)
        ln = label(r"15:00, \ still no sleep", font_size=27, color=MODEL).next_to(dn, UP, buff=0.35).shift(LEFT * 1.0)
        rows = rows_of([
            (r"alertness: \ the clock's push to stay awake, \ minus the pressure to sleep", WHITE),
            (rf"lowest at about {clock_time(a['lowest_clock'])}: \ the pressure is high and the clock's push is at its "
             r"weakest", BAD),
            (r"then it comes back up, with no sleep at all: \ the second wind", MODEL),
            (r"if sleepiness were only time awake, \ it could only get worse", GREY_A),
            (r"the hours before dawn: \ both processes at their worst together", THRESH),
        ], 4.5, 28, 0.26).move_to([4.65, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche; \ alertness in arbitrary units")
        with self.voiceover(
            "One more prediction, and you may have tested it yourself. Put the two processes together as "
            "alertness: the clock's push to stay awake, minus the pressure to sleep. Now follow it "
            "through that night without sleep. <bookmark mark='a'/> Through the evening and the night it "
            "falls, and it's lowest at about twenty past five in the morning, when the pressure is high "
            "and the clock's push is at its weakest. <bookmark mark='b'/> And then it comes back up. With "
            "no sleep at all, the model is more alert the next afternoon than it was at dawn. Anyone who "
            "has stayed up all night knows this as the second wind. <bookmark mark='c'/> And one process "
            "couldn't produce it. If sleepiness were only a matter of time awake, it could only get "
            "worse. <bookmark mark='d'/> It also says where the danger is. In the hours before dawn the "
            "two processes are at their worst together, and that's the stretch that people who study "
            "accidents on the night shift worry about most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(night), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=5.0, rate_func=linear)
            self.play(FadeIn(dl, scale=1.5), FadeIn(ll), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(dn, scale=1.5), FadeIn(ln), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()
