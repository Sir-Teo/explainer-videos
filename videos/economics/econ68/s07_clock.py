from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


def rd_panel(R: dict, lo: float, hi: float, ymax: float, title: str, color) -> VGroup:
    at = R["at"]
    ax = plane([lo, hi], [0, ymax], x_length=5.6, y_length=3.8,
               xticks=[lo, at, hi], yticks=[0, ymax / 2, ymax],
               xfmt=lambda v: f"{int(v) % 24}:00", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=13)
    t, y = np.array(R["t"]), np.array(R["y"])
    m = (t >= lo) & (t <= hi)
    pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.045, color=GREY_A) for a, b in zip(t[m], y[m])])
    lx = np.linspace(at - 2, at - 1e-3, 30)
    rx = np.linspace(at, at + 2, 30)
    fl = path(ax, lx, np.exp(np.polyval(R["left"], lx - at)), color, 3.0, smooth=False)
    fr = path(ax, rx, np.exp(np.polyval(R["right"], rx - at)), color, 3.0, smooth=False)
    cut = vline(ax, at, 0, ymax, TOLL, 2.0)
    head = label(title, font_size=17, color=color).next_to(ax.ax, UP, buff=0.12)
    g = VGroup(ax, pts, fl, fr, cut, head)
    g.ax, g.pts, g.fits, g.cut, g.head = ax, pts, VGroup(fl, fr), cut, head
    return g


class Clock(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The clock: \ a discontinuity in time", r"What happens in the minutes around the moment the "
             r"price changes?", "Chapter six. The clock: a discontinuity in time.", scale=("city",),
             horizon=("a day",))
        self.panels()
        self.meaning()

    def panels(self):
        C = load("clock")
        n, f = C["nine"], C["five"]
        p9 = rd_panel(n, 19, 23, 3200, r"9 pm: \ the toll falls from \$9 to \$2.25", BUS)
        p5 = rd_panel(f, 3, 7, 3200, r"5 am: \ the toll rises from \$2.25 to \$9", TOLL)
        VGroup(p9, p5).arrange(RIGHT, buff=0.9).move_to(UP * 0.15)
        yl = label(r"cars entering per ten minutes, \ average weekday", font_size=15, color=GREY_A).to_edge(
            UP, buff=0.35)
        j9 = 100 * (np.exp(n["jump"]) - 1)
        j5 = 100 * (np.exp(f["jump"]) - 1)
        notes = VGroup(
            label(rf"jump: \ +{j9:.0f}\%; \ {n['extra_first_hour']:,.0f} extra cars in the first hour".replace(
                ",", "{,}"), font_size=16, color=BUS).next_to(p9, DOWN, buff=0.25),
            label(rf"jump: \ {j5:.0f}\%; \ {-f['extra_first_hour']:,.0f} fewer cars in the first hour".replace(
                ",", "{,}").replace("-", "{-}"), font_size=16, color=TOLL).next_to(p5, DOWN, buff=0.25),
        )
        tag = data_tag(rf"MTA zone entries by ten-minute block, \ {C['weekdays']} weekdays of 2025--2026; \ "
                       r"agora.congestion.time\_rd", corner=DL, font_size=12)
        with self.voiceover(
            "Now the clock. <bookmark mark='a'/> On the left, cars entering the zone every ten minutes on an "
            f"average weekday, from seven to eleven at night, over {C['weekdays']} weekdays. The toll falls from "
            "nine dollars to two twenty-five at nine o'clock. <bookmark mark='b'/> A line through the blocks on "
            f"each side, and the gap where they meet: entries jump by {j9:.0f} percent the moment the toll falls. "
            f"In the first hour after nine, about {n['extra_first_hour']:,.0f} more cars enter than the evening's "
            "trend predicts. <bookmark mark='c'/> On the right, the morning, when the toll rises at five. Drivers "
            f"crowd in before it, and entries fall by {-j5:.0f} percent at the stroke of five: about "
            f"{-f['extra_first_hour']:,.0f} fewer cars in the next hour than the early-morning trend."
        ) as vo:
            self.play(FadeIn(yl), FadeIn(tag), FadeIn(p9.ax), FadeIn(p9.head), FadeIn(p9.cut))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in p9.pts], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(p9.fits), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(p5.ax), FadeIn(p5.head), FadeIn(p5.cut),
                      LaggedStart(*[FadeIn(d) for d in p5.pts], lag_ratio=0.02), run_time=1.6)
            self.play(Create(p5.fits), FadeIn(notes[1]), run_time=1.5)
        self.clear_scene()

    def meaning(self):
        rows = VGroup(
            label(r"the cleanest result in the study: \ prices move people in time", font_size=22, color=DATA),
            label(r"but a jump at the cutoff measures retiming: \ the car that waits until 9:05 still comes",
                  font_size=22, color=TOLL),
            label(r"it cannot tell how many trips were given up altogether", font_size=22, color=GREY_A),
            label(r"Vickrey's point, \ measured: \ a price by time of day spreads the peak", font_size=22,
                  color=BUS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "What does the clock show? <bookmark mark='a'/> It is the cleanest result in the study: nothing else "
            "changes at nine o'clock, so the jump is the price. <bookmark mark='b'/> But read it carefully. A "
            "discontinuity at a cutoff measures retiming: the driver who waits until five past nine still comes. "
            "<bookmark mark='c'/> It cannot tell how many trips were given up altogether. <bookmark mark='d'/> What "
            "it does measure is Vickrey's point: a price that varies by time of day spreads the peak."
        ) as vo:
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
