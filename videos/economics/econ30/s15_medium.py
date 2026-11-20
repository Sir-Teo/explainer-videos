from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Medium(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Medium-scale models: \ what each friction buys", r"Why do central banks' models have so many "
             r"moving parts?", "Chapter thirteen. Medium-scale models: what each friction buys.",
             lit={2005: r"Christiano, \ Eichenbaum and Evans", 2007: r"Smets and Wouters"}, scale=("nation",),
             horizon=("a quarter", "three years"))
        self.hump()
        self.frictions()

    def hump(self):
        H = load("hybrid")
        q = np.array(H["base"]["q"])
        ax = plane([0, 15], [-0.35, 0.1], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[0, 4, 8, 12], yticks=[-0.3, -0.2, -0.1, 0, 0.1], xlabel=r"quarters after a tightening",
                   ylabel=r"output gap, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0",
                   font_size=15)
        zero = seg(ax, 0, 0, 15, 0, GREY_D, 1.5)
        base = path(ax, q, H["base"]["x"], GREY_B, 3, smooth=False)
        rich = path(ax, q, H["rich"]["x"], OUTPUT, 3.5, smooth=False)
        T = island.truths(30)["hybrid"]
        side = VGroup(
            label(r"grey: \ the three equations: \\ the biggest effect at once", font_size=19, color=GREY_B),
            label(r"in the data, \ output's response \\ builds for a year or more \\ (the hump)", font_size=19,
                  color=E.ACCENT),
            label(rf"green: \ add habits ({T['habit']}), \\ indexation of prices ({T['index']}) \\ and a smoothed "
                  rf"rule ({T['smooth']})", font_size=19, color=OUTPUT),
            label(rf"the trough moves to {H['rich']['peak_x']} quarters \\ after the shock", font_size=19,
                  color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The three-equation model has a problem with timing. <bookmark mark='a'/> After a monetary "
            "tightening, its output falls most in the very first quarter, then recovers. <bookmark mark='b'/> In "
            "the data, as Part thirty-one will measure, output's response builds for a year or more before it "
            "turns: a hump. <bookmark mark='c'/> Add three frictions to the Island: households whose consumption "
            "habits make them slow to change spending, firms that index unchanged prices to past inflation, and "
            "a central bank that moves its rate gradually. <bookmark mark='d'/> The response now builds, with the "
            f"trough {H['rich']['peak_x']} quarters after the shock. Each friction is there to buy a feature of the "
            "data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(base), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rich), FadeIn(side[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def frictions(self):
        cards = point_cards([
            (r"habits", r"consumption adjusts slowly: \\ the hump in spending", OUTPUT),
            (r"sticky wages", r"labour costs adjust slowly: \\ inflation stays persistent", INFL),
            (r"indexation", r"unchanged prices rise with \\ past inflation: \ persistence", PRICE),
            (r"investment costs", r"capital adjusts slowly: \\ the hump in investment", CB),
            (r"variable utilization", r"output can rise before \\ capital does", COST),
            (r"many shocks", r"Smets and Wouters: \ seven, \\ estimated on US data", E.ACCENT),
        ], width=12.8, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"Christiano, \ Eichenbaum and Evans, \ 2005; \ Smets and Wouters, \ 2007", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = published_tag(r"Christiano, \ Eichenbaum and Evans, \ \emph{JPE} 113(1) (2005); \ Smets and Wouters, \ "
                            r"\emph{AER} 97(3) (2007)", corner=DR, font_size=12)
        with self.voiceover(
            "This is how the models central banks use were built. Lawrence Christiano, Martin Eichenbaum and "
            "Charles Evans in 2005, and Frank Smets and Raf Wouters in 2007, each added frictions to buy features of "
            "the data. <bookmark mark='a'/> Habits give the hump in spending. <bookmark mark='b'/> Sticky wages, "
            "with Calvo's fairy visiting workers too, keep inflation persistent. <bookmark mark='c'/> Indexation "
            "makes prices carry past inflation forward. <bookmark mark='d'/> Costs of adjusting investment give the "
            "hump in investment. <bookmark mark='e'/> Variable utilization lets output rise before capital does. "
            "<bookmark mark='f'/> And Smets and Wouters let seven shocks drive the economy, and estimated the whole "
            "model on American data. The critics ask whether each friction describes how people behave, or only "
            "repairs a fit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
