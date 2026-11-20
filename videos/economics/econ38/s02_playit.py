from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ a minimum wage a fifth higher", r"What happens to employment?",
             "Chapter one. Play it: a minimum wage a fifth higher.", lit={1994: r"Card and Krueger"},
             scale=("firm", "market"), horizon=("a year",))
        self.choose()
        self.reveal()

    def choose(self):
        cards = point_cards([
            (r"A: \ falls 10\%", r"New Jersey's restaurants \\ cut a tenth of jobs \\ relative to Pennsylvania",
             CHIP[0]),
            (r"B: \ falls 3\%", r"a small loss, \\ as the textbook's \\ modest elasticities say", CHIP[1]),
            (r"C: \ no change", r"employers absorb it \\ in prices or profits", CHIP[2]),
            (r"D: \ rises", r"New Jersey gains \\ jobs relative \\ to Pennsylvania", CHIP[3]),
        ], width=12.6, cols=4, font_size=20).move_to(UP * 0.1)
        q = wrapped_label(r"New Jersey's minimum rises 19\%, \ Pennsylvania's does not: \ by November, \ how does "
                          r"employment in New Jersey's restaurants compare?", 12.0, 26, E.ACCENT).to_edge(UP, buff=0.6)
        ring = countdown().scale(0.7).next_to(cards, DOWN, buff=0.5)
        tag = data_tag(r"Card and Krueger (1994), \ public data", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn. New Jersey's minimum wage rises nineteen percent; Pennsylvania's stays put. By November, "
            "how did employment in New Jersey's restaurants compare with Pennsylvania's? <bookmark mark='a'/> It "
            "fell by a tenth; it fell by a few percent, as modest textbook elasticities suggest; it did not change; "
            "or it rose. Pause, and choose."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        C = load("ck")
        ax = plane([-0.3, 1.3], [19, 24.5], center=LEFT * 2.0 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[0, 1], yticks=[19, 20, 21, 22, 23, 24], xlabel="", ylabel=r"full-time-equivalent "
                   r"employees per restaurant", xfmt=lambda v: "February" if v < 0.5 else "November",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines = VGroup()
        for nm, col in (("nj", NJ), ("pa", PA)):
            d = C[nm]
            lines.add(VGroup(seg(ax, 0, d["before"], 1, d["after"], col, 4), dot(ax, 0, d["before"], col, 0.09),
                             dot(ax, 1, d["after"], col, 0.09),
                             label(f"{d['before']:.2f}", font_size=17, color=col).next_to(ax.ax.c2p(0, d["before"]),
                                                                                      LEFT, buff=0.15),
                             label(f"{d['after']:.2f}", font_size=17, color=col).next_to(
                                 ax.ax.c2p(1, d["after"]), RIGHT, buff=0.15).shift(
                                 (DOWN if nm == "nj" else UP) * 0.17)))
        keys = VGroup(label(r"New Jersey", font_size=19, color=NJ), label(r"Pennsylvania", font_size=19, color=PA)
                      ).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.2)
        side = VGroup(
            label(r"D: \ it rose, \ relatively", font_size=24, color=CHIP[3]),
            label(rf"New Jersey \ +{C['nj']['after'] - C['nj']['before']:.2f}; \\ Pennsylvania \ "
                  rf"{C['pa']['after'] - C['pa']['before']:+.2f}", font_size=19, color=WHITE),
            label(rf"difference in differences: \\ +{C['did']:.2f} employees \ (s.e. {C['se_balanced']:.2f})",
                  font_size=19, color=E.ACCENT),
            label(rf"about +{100 * C['emp_rel']:.0f}\% relative, \\ as the starting wage \\ rose "
                  rf"{100 * C['wage_rel']:.0f}\% "
                  r"relative", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Card and Krueger (1994), \ public data, \ recomputed", corner=DR, font_size=12)
        with self.voiceover(
            "The answer is D. <bookmark mark='a'/> In February, New Jersey's restaurants employed "
            f"{C['nj']['before']:.2f} full-time equivalents each, Pennsylvania's {C['pa']['before']:.2f}. "
            f"By November, New Jersey's had {C['nj']['after']:.2f} and Pennsylvania's had fallen to "
            f"{C['pa']['after']:.2f}. <bookmark mark='b'/> Pennsylvania is the counterfactual: what would have "
            "happened "
            "to New Jersey without the rise. Comparing the changes, the difference in differences, New Jersey gained "
            f"{C['did']:.2f} employees per restaurant relative, with a standard error of {C['se_balanced']:.2f}. "
            f"<bookmark mark='c'/> About {100 * C['emp_rel']:.0f} percent more jobs, as the starting wage rose about "
            f"{100 * C['wage_rel']:.0f} percent. These are Card and Krueger's numbers, recomputed here from their "
            "published data, to the second decimal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(keys), FadeIn(tag), LaggedStart(*[FadeIn(g_) for g_ in lines],
                                                                          lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
