from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Counterfactual(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The counterfactual: \ the \$15 plan", r"What would the toll first planned have done, \ and "
             r"how sure can the answer be?", "Chapter eight. The counterfactual: the fifteen-dollar plan.",
             lit={2024: "the pause"}, scale=("city",), horizon=("a year",))
        self.history()
        self.uncertainty()

    def history(self):
        O = load("official")
        hc = history_card(r"June 2024", r"a toll paused", r"a \$15 charge due on 30 June is paused weeks before it "
                          r"starts; \ in November a \$9 charge is approved, \ rising to \$12 in 2028 and \$15 in "
                          r"2031", color=TOLL, width=11.6, font_size=22).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"the counterfactual has a date: \ the plan that was nearly adopted, \ and the one scheduled",
                  font_size=21, color=GREY_A),
            label(rf"the question: \ what would \${O['plan_2024']:.0f} have done, \ and what will "
                  rf"\${O['toll_2028']:.0f} do?", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hc, DOWN, buff=0.7)
        tag = published_tag(r"Office of the Governor (14 November 2024); \ NY1 (17 November 2026)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Good counterfactuals are ones someone needs. <bookmark mark='a'/> This one has a date. In June 2024 a "
            "fifteen-dollar charge, due to begin on the thirtieth, was paused weeks before it started. In November "
            "a nine-dollar charge was approved instead, rising to twelve dollars in 2028 and fifteen in 2031. "
            "<bookmark mark='b'/> So the question writes itself: what would fifteen dollars have done, and what "
            "will the next steps do?"
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows, shift=UP * 0.1))
        self.clear_scene()

    def uncertainty(self):
        R = load("cf")
        ax = plane([-10, 8], [0, 4], center=RIGHT * 0.9 + DOWN * 0.2, x_length=8.6, y_length=4.4,
                   xticks=[-10, -5, 0, 5], yticks=[], xlabel=r"percent \ (or dollars, \ last row)",
                   xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        zero = vline(ax, 0, 0, 4, GREY_C, 1.4)
        lv = [100 * (np.exp(x) - 1) for x in R["lnV"]]
        dT = [100 * x for x in R["dT"]]
        items = [(3.3, lv, TOLL, r"traffic at \$15 \ (vs no toll)"),
                 (2.3, dT, BUS, r"time per trip at \$15"),
                 (1.3, R["mec"], MODEL, r"cost of a car's delay, \ \$")]
        rows = VGroup()
        names = VGroup()
        for y, (lo, mid, hi), col, nm in [(y, v, c, n) for y, v, c, n in items]:
            bar = Line(ax.ax.c2p(lo, y), ax.ax.c2p(hi, y), stroke_color=col, stroke_width=10, stroke_opacity=0.55)
            d = Dot(ax.ax.c2p(mid, y), radius=0.09, color=WHITE)
            txt = label(rf"{mid:.1f} \ [{lo:.1f}, \ {hi:.1f}]".replace("-", "{-}"), font_size=16, color=col).next_to(
                bar, UP, buff=0.08)
            rows.add(VGroup(bar, d, txt))
            names.add(label(nm, font_size=17, color=col).next_to(ax.ax.c2p(-10, y), LEFT, buff=0.25))
        foot = VGroup(
            label(r"each draw: \ both estimates from their standard errors; \ value of time \$14--24, \ 2--5 miles, "
                  r"\ other costs \$15--40", font_size=16, color=GREY_A),
            label(r"the median, \ and the range that holds 90\% of 2,000 draws", font_size=16, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        tag = island_tag(r"computed: \ agora.congestion.counterfactual", corner=UL, font_size=12)
        with self.voiceover(
            "And the answer must carry its uncertainty. <bookmark mark='a'/> Two kinds: the estimates themselves, "
            "each with a standard error, and the assumptions, each with a range. Draw both two thousand times, "
            "recalibrate the model each time, and report the median with the range that holds ninety percent of "
            f"the draws. <bookmark mark='b'/> At fifteen dollars, traffic in the zone would be about "
            f"{say_pct(-(np.exp(R['lnV'][1]) - 1), 1)} below its uncharged level, somewhere between "
            f"{-lv[2]:.1f} and {-lv[0]:.1f} percent. <bookmark mark='c'/> Trips in the zone would be about "
            f"{say_pct(-R['dT'][1], 1)} faster. <bookmark mark='d'/> And the delay a car imposes on other drivers "
            f"is worth between {R['mec'][0]:.1f} and {R['mec'][2]:.1f} dollars, a range wide enough to say what "
            "matters: the narrow case for fifteen dollars is weaker than the case for nine, and both rest on "
            "costs the model leaves out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(GrowFromCenter(r_[0]), FadeIn(r_[1]), FadeIn(r_[2]))
        self.clear_scene()
