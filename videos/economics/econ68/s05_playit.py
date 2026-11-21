from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


def options(title: str, opts, color) -> VGroup:
    head = label(title, font_size=23, color=color)
    boxes = VGroup()
    for k, o in enumerate(opts):
        b = RoundedRectangle(width=2.7, height=0.8, corner_radius=0.1, stroke_color=color, stroke_width=2)
        t = label(rf"{'ABCD'[k]}: \ {o}", font_size=19, color=WHITE).move_to(b)
        boxes.add(VGroup(b, t))
    boxes.arrange(RIGHT, buff=0.25)
    return VGroup(head, boxes).arrange(DOWN, buff=0.25)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: \ predict the result", r"Before seeing the estimates, \ what do you expect?",
             "Chapter four. Play it: predict the result.", scale=("city",), horizon=("a year",))
        self.ask()
        self.reveal()

    def questions(self):
        q1 = options(r"1. \ Traffic through the two tunnels in 2025, \ relative to the other crossings:",
                     (r"no change", r"down 1--5\%", r"down 5--15\%", r"down 15\%+"), TOLL)
        q2 = options(r"2. \ Bus speeds inside the business district, \ relative to outside:",
                     (r"no change", r"up 1--3\%", r"up 3--10\%", r"up 10\%+"), BUS)
        q3 = options(r"3. \ Car entries in the ten minutes after 9 pm, \ against the ten before:",
                     (r"the same", r"up 5--15\%", r"up 15--40\%", r"up 40\%+"), DATA)
        return VGroup(q1, q2, q3).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)

    def ask(self):
        g = self.questions()
        head = label(r"three predictions, \ written down before the estimates", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Your turn, as the dissertation's first reader. Write down your predictions before the estimates "
            "arrive; a forecast written first cannot be revised afterwards. <bookmark mark='a'/> One: in 2025, how "
            "did traffic through the two tunnels change, relative to the other crossings? <bookmark mark='b'/> Two: "
            "how did bus speeds inside the business district change, relative to routes outside? <bookmark "
            "mark='c'/> Three: on weekdays, how do car entries in the ten minutes after nine at night compare with "
            "the ten minutes before, when the toll falls from nine dollars to two twenty-five? Pause, and choose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(g[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(g[2], shift=UP * 0.1))
        self.wait(4.0)
        self.clear_scene()

    def reveal(self):
        D, Bu, C = load("did"), load("buses"), load("clock")
        g = self.questions()
        j9 = 100 * (np.exp(C["nine"]["jump"]) - 1)
        picks = (1, 1, 2)
        notes = VGroup(
            label(rf"{100 * D['effect']:.1f}\% \ (and {100 * D['adjusted']:.1f}\% after the trend)".replace("-", "{-}"),
                  font_size=18, color=TOLL),
            label(rf"+{100 * Bu['effect']:.1f}\%", font_size=18, color=BUS),
            label(rf"+{j9:.0f}\% \ (the fitted lines' jump)", font_size=18, color=DATA),
        )
        for q, n_ in zip(g, notes):
            n_.next_to(q[1], RIGHT, buff=0.2)
        grp = VGroup(g, notes)
        if grp.width > 13.2:
            grp.scale_to_fit_width(13.2)
        grp.move_to(DOWN * 0.1)
        with self.voiceover(
            "The answers, in the order the next chapters will earn them. <bookmark mark='a'/> One: B. Relative to "
            f"the other crossings, tunnel traffic fell by {say_pct(-D['effect'], 1)}, and by about "
            f"{say_pct(-D['adjusted'], 1)} once the tunnels' earlier drift is taken out. <bookmark mark='b'/> Two: "
            f"B. Buses inside the district got {say_pct(Bu['effect'], 1)} faster than buses outside. <bookmark "
            f"mark='c'/> Three: C. Car entries jump by about {j9:.0f} percent the moment the toll drops. The "
            "largest effect is not on whether people drive, but when."
        ) as vo:
            self.play(FadeIn(g))
            for mk, q, n_, k in zip("abc", g, notes, picks):
                vo.wait_until(mk)
                self.play(q[1][k][0].animate.set_stroke(WHITE, 4).set_fill(WHITE, 0.12), FadeIn(n_))
        self.clear_scene()
