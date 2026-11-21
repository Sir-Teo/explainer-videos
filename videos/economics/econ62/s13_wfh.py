from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class WFH(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Working from home, \ randomized", r"Does a worker at home work more or less, \ and do they "
             r"stay?", "Chapter eleven. Working from home, randomized.",
             lit={2015: r"Bloom, Liang, Roberts and Ying", 2024: r"hybrid, in Nature"}, scale=("person", "firm"),
             horizon=("a year",))
        self.trial()
        self.evidence()

    def trial(self):
        W = load("wfh")
        vals = [100 * W["minutes"], 100 * W["rate"], 100 * W["performance"]]
        ses = [200 * W["minutes_se"], 200 * W["rate_se"], 200 * W["performance_se"]]
        ax = plane([-0.6, 2.6], [-2, 20], center=LEFT * 3.4 + UP * 0.2, x_length=5.2, y_length=3.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"home against office, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cols = (WORK, OWN, GAIN)
        b = bars(ax, range(3), vals, cols, width=0.5)
        err = VGroup(*[Line(ax.ax.c2p(k, v - s), ax.ax.c2p(k, v + s), color=WHITE, stroke_width=2)
                       for k, (v, s) in enumerate(zip(vals, ses))])
        names = (r"minutes \\ worked", r"calls \\ a minute", r"calls \\ in all")
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, -2), DOWN, buff=0.1)
                        for k, (n, c) in enumerate(zip(names, cols))])
        q = VGroup(
            label(r"quit during the trial", font_size=17, color=GREY_A),
            VGroup(Rectangle(width=4.0 * W["quit_office"], height=0.32, stroke_width=0, fill_color=GREY_B,
                             fill_opacity=0.85), label(rf"office {100 * W['quit_office']:.0f}\%", font_size=15,
                                                       color=GREY_B)).arrange(RIGHT, buff=0.12),
            VGroup(Rectangle(width=4.0 * W["quit_home"], height=0.32, stroke_width=0, fill_color=GAIN,
                             fill_opacity=0.85), label(rf"home {100 * W['quit_home']:.0f}\%", font_size=15,
                                                       color=GAIN)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.75).align_to(ax, LEFT)
        side = VGroup(
            label(rf"{W['n']} call-centre volunteers, \ half sent home at random", font_size=19, color=WHITE),
            label(r"more minutes: \ fewer breaks and sick days", font_size=19, color=WORK),
            label(r"more calls a minute: \ a quieter room", font_size=19, color=OWN),
            label(rf"performance +{vals[2]:.0f}\% \ ($\pm${ses[2]:.0f})", font_size=21, color=GAIN),
            label(r"and quits fall by more than half", font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.org.wfh; \ effects planted", corner=DL, font_size=12)
        with self.voiceover(
            "Working from home is a question about organization that became a question for everyone in 2020. The "
            f"Island runs the trial properly. <bookmark mark='a'/> {W['n']} call-centre workers who volunteer to "
            "work from home; half, chosen at random, are sent home for forty weeks. <bookmark mark='b'/> At home "
            "they work more minutes a shift, with fewer breaks and sick days, <bookmark mark='c'/> and take more "
            f"calls a minute, in a quieter room. <bookmark mark='d'/> In all, {vals[2]:.0f} percent more calls. "
            "<bookmark mark='e'/> And they quit far less often. These numbers were planted to echo a real trial."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), Create(err[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), Create(err[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[2], DOWN), Create(err[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(q), FadeIn(side[4]))
        self.clear_scene()

    def evidence(self):
        rows = VGroup(
            history_card(2010, r"Ctrip's call centre, \ Shanghai", r"volunteers randomized to home for nine months: "
                         r"\ performance +13\%, \ 9 points from more minutes and 4 from more calls a minute; \ "
                         r"promotions, \ for the same performance, \ fewer", color=GAIN, width=11.4, font_size=20),
            history_card(2021, r"Trip.com, \ hybrid", r"1,600 graduates in engineering, \ marketing and finance, "
                         r"\ two days a week at home: \ quits down by a third; \ no change in performance reviews or "
                         r"promotions".replace("1,600", "1{,}600"), color=OWN, width=11.4, font_size=20),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
        foot = VGroup(
            label(r"both studies had the firm's co-founder, \ James Liang, \ as an author", font_size=19,
                  color=HOLD),
            label(r"what home work does depends on the job: \ measurable, \ independent tasks gain; \\ the young, "
                  r"\ who learn by watching, \ may lose", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(rows, DOWN, buff=0.45)
        tag = published_tag(r"Bloom, \ Liang, \ Roberts and Ying, \ QJE 130(1) (2015); \ Bloom, \ Han and Liang, \ "
                            r"Nature 630 (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "The real trial came first. <bookmark mark='a'/> Nicholas Bloom, James Liang, John Roberts and Zhichun "
            "Jenny Ying randomized volunteers at Ctrip's call centre in Shanghai to work from home for nine months. "
            "Performance rose thirteen percent: nine points from working more minutes, four from more calls a "
            "minute. Quits fell sharply. But for the same performance, home workers were promoted less often. "
            "<bookmark mark='b'/> A decade later, a second trial at the same firm, now Trip.com, sent sixteen "
            "hundred graduate employees in engineering, marketing and finance home two days a week. Quits fell by "
            "a third, and performance reviews and promotions did not change. <bookmark mark='c'/> One caution: "
            "both studies had the firm's co-founder, James Liang, as an author, though the randomization is what "
            "makes them credible. <bookmark mark='d'/> And the effects depend on the job: measurable, independent "
            "tasks gain from quiet; the young, who learn by watching others, may lose."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
