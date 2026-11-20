from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#F25F5C")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ the chair in 1979", r"The data of the day say the economy has room to grow. \ "
             r"Does it?", "Chapter two. Play it: the chair in 1979.",
             lit={1979: r"the chair"}, scale=("nation",), horizon=("a quarter", "a year"))
        self.desk()
        self.choose()
        self.reveal()

    def desk(self):
        P = load("playit")
        board = VGroup(
            label(r"early 1979: \ what is on your desk", font_size=28, color=E.ACCENT),
            label(rf"consumer prices over 1978: \ up {P['pi']:.1f}\%", font_size=25, color=INFL),
            label(rf"output growth since 1947: \ {P['trend_growth']:.1f}\% a year on average", font_size=25,
                  color=GREY_A),
            label(rf"output at the end of 1978: \ {abs(P['gap_rt']):.1f}\% below that trend", font_size=25,
                  color=OUTPUT),
            label(rf"the federal funds rate: \ {P['ff']:.1f}\%", font_size=25, color=RATE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.4)
        note_ = label(r"the data as published in February 1979, \ from the Philadelphia Fed's real-time archive",
                      font_size=19, color=GREY_B).to_edge(DOWN, buff=0.7)
        tag = data_tag(r"Philadelphia Fed, \ Real-Time Data Set (vintage 1979Q1); \ BLS CPI and the funds rate via "
                       r"FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn in the chair. It is early 1979, and this is what is on your desk. <bookmark mark='a'/> "
            f"Consumer prices rose {P['pi']:.1f} percent over 1978. <bookmark mark='b'/> Since 1947, American output "
            f"has grown about {P['trend_growth']:.1f} percent a year on average. <bookmark mark='c'/> And by the "
            f"figures published that winter, output at the end of 1978 was {abs(P['gap_rt']):.1f} percent below that "
            "trend: room to grow, it seems, without pushing prices up. <bookmark mark='d'/> The federal funds rate "
            f"is {P['ff']:.0f} percent. <bookmark mark='e'/> These are the numbers as they were published at the "
            "time, from an archive the Federal Reserve Bank of Philadelphia keeps of every release."
        ) as vo:
            self.play(FadeIn(board[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", board[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.clear_scene()

    def _chips(self, P):
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.9, height=0.95, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=22, color=c))
                         for c, t in zip(CHIP, (r"A: \ about 4\% below potential", r"B: \ about at potential",
                                                r"C: \ about 2\% above"))]).arrange(RIGHT, buff=0.35)
        for ch in chips:
            ch[1].move_to(ch[0])
        return chips

    def choose(self):
        P = load("playit")
        rows = VGroup(
            label(r"today's best estimate of the same quarter, \ the end of 1978:", font_size=26, color=E.ACCENT),
            label(r"how far was output from what the economy could produce \ without speeding up inflation?",
                  font_size=24, color=OUTPUT),
            label(r"(the Congressional Budget Office's estimate of potential output, \ with today's data)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 1.6)
        chips = self._chips(P).move_to(DOWN * 1.0)
        ring = countdown().scale(0.7).next_to(chips, DOWN, buff=0.4)
        with self.voiceover(
            "Now the question. With everything learned and revised since, the Congressional Budget Office estimates "
            "what the economy could have produced in each quarter without speeding up inflation: its potential. "
            "<bookmark mark='a'/> Where does today's estimate put output at the end of 1978? <bookmark mark='b'/> "
            "About four percent below potential, so even more room than you thought; about at potential; or about "
            "two percent above it? Pause, and choose."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        chips = self._chips(P).move_to(UP * 2.4)
        rows = VGroup(
            label(rf"C: \ today's estimate is {P['gap_today']:+.1f}\%, \ not {P['gap_rt']:+.1f}\%", font_size=26,
                  color=CHIP[2]),
            label(r"the trend of the 1950s and 1960s had ended: \ productivity growth slowed after 1973", font_size=22,
                  color=GREY_A),
            label(rf"Taylor's rule with the data of the day: \ {P['rule_rt']:.1f}\%; \ with today's: "
                  rf"{P['rule_today']:.1f}\%", font_size=23, color=RATE),
            label(rf"the actual rate: \ {P['ff']:.1f}\%, \ below both", font_size=23, color=RATE),
            label(r"Orphanides: \ overoptimistic estimates of potential, \ not only a lack of resolve, \ fed the Great "
                  r"Inflation",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).next_to(chips, DOWN, buff=0.55)
        tag = published_tag(r"Orphanides, \ \emph{AER} 91(4) (2001) and \emph{JME} 50(3) (2003); \ CBO via FRED",
                            corner=DR, font_size=12)
        with self.voiceover(
            f"<bookmark mark='a'/> Today's estimate: output was {say_num(P['gap_today'], 1)} percent from its "
            "potential, above it, not below. If you chose C, you knew something nobody knew in 1979. "
            "<bookmark mark='b'/> The trend of the fifties and sixties had ended: productivity growth slowed after "
            "1973, and estimates made by extending the old trend saw slack that was not there. "
            "<bookmark mark='c'/> Put the two gaps into Taylor's rule from Part 30. With the data of the day it says "
            f"{P['rule_rt']:.1f} percent; with today's, {P['rule_today']:.1f}. <bookmark mark='d'/> The actual rate "
            f"was {P['ff']:.0f}, below both. <bookmark mark='e'/> Athanasios Orphanides showed that the Federal "
            "Reserve's own real-time estimates of the gap in the 1970s were far too optimistic about potential "
            "output, and argued that this misreading, rather than a lack of resolve alone, explains much of the Great "
            "Inflation. A rule is only as good as "
            "the data put into it."
        ) as vo:
            self.play(FadeIn(chips), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(chips[2], color=WHITE))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
