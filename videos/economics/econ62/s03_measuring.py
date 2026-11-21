from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403

SHORT = {"dispersed shareholders": r"dispersed shareholders", "private equity": r"private equity",
         "family-owned, outside chief executive": r"family, \ outside CEO", "multinational subsidiary":
         r"multinational subsidiary", "family-owned, family chief executive": r"family, \ family CEO",
         "founder": r"founder", "government": r"government"}


class Measuring(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Measuring management", r"Can you score how well a firm is run, \ and does the score mean "
             r"anything?", "Chapter two. Measuring management.", lit={2007: r"Bloom and Van Reenen"},
             scale=("firm", "nation"), horizon=("a year",))
        self.survey()
        self.scores()

    def survey(self):
        cols = VGroup(
            VGroup(label(r"operations", font_size=22, color=PLANT),
                   label(r"is the process lean? \\ are defects tracked?", font_size=17, color=GREY_A)),
            VGroup(label(r"monitoring", font_size=22, color=MGR),
                   label(r"are results measured, \\ reviewed, \ acted on?", font_size=17, color=GREY_A)),
            VGroup(label(r"targets", font_size=22, color=OWN),
                   label(r"are goals stretching, \\ linked and understood?", font_size=17, color=GREY_A)),
            VGroup(label(r"people", font_size=22, color=WORK),
                   label(r"are the good rewarded \\ and the poor moved on?", font_size=17, color=GREY_A)),
        )
        for c in cols:
            c.arrange(DOWN, buff=0.2)
        cols.arrange(RIGHT, buff=0.7).move_to(UP * 0.8)
        scale_ = VGroup(*[VGroup(Square(side_length=0.55, stroke_color=MGR, stroke_width=2,
                                        fill_color=MGR, fill_opacity=0.12 + 0.17 * k),
                                 label(str(k + 1), font_size=20, color=WHITE)) for k in range(5)])
        for s_ in scale_:
            s_[1].move_to(s_[0])
        scale_.arrange(RIGHT, buff=0.15)
        ends = VGroup(label(r"no practice", font_size=16, color=GREY_B).next_to(scale_, LEFT, buff=0.25),
                      label(r"best practice", font_size=16, color=GREY_B).next_to(scale_, RIGHT, buff=0.25))
        sc = VGroup(scale_, ends).next_to(cols, DOWN, buff=0.7)
        how = label(r"18 practices, \ each scored 1 to 5 from a long telephone interview with a plant manager, \\ "
                    r"who is not told it is being scored; \ the interviewer does not see the firm's accounts",
                    font_size=19, color=WHITE).next_to(sc, DOWN, buff=0.5)
        tag = published_tag(r"Bloom and Van Reenen, \ Quarterly Journal of Economics 122(4) (2007); \ the World "
                            r"Management Survey", corner=DL, font_size=12)
        with self.voiceover(
            "If management matters, it has to be measured, and for a long time economists thought it could not be. "
            "Nicholas Bloom and John Van Reenen built a way. <bookmark mark='a'/> They score eighteen basic "
            "practices in four groups: operations, whether the process is lean and defects are tracked; "
            "monitoring, whether results are measured, reviewed and acted on; targets, whether goals are "
            "stretching and understood; and people, whether good performers are rewarded and poor ones moved on. "
            "<bookmark mark='b'/> Each practice gets a score from one, no practice, to five, best practice. "
            "<bookmark mark='c'/> The scores come from a long telephone interview with a plant manager, with open "
            "questions, so the manager does not know what a good answer is, and the interviewer never sees the "
            "firm's accounts. The survey has since covered thousands of firms in dozens of countries."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sc))
            vo.wait_until("c")
            self.play(FadeIn(how))
        self.clear_scene()

    def scores(self):
        M = load("management")
        sc, lp = np.array(M["score"]), np.array(M["log_tfp"])
        by = M["by_owner"]
        order = sorted(by, key=lambda k: by[k])
        ax = plane([1.5, 4.5], [-1.2, 1.2], center=LEFT * 3.6 + DOWN * 0.4, x_length=5.0, y_length=4.4,
                   xticks=[2, 3, 4], yticks=[-1, 0, 1], xlabel=r"management score", ylabel=r"log productivity",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=14)
        pts = VGroup(*[dot(ax, x, y, GREY_B, 0.03) for x, y in zip(sc[:400], lp[:400])])
        xs = np.linspace(1.6, 4.4, 2)
        b = M["slope"]
        a0 = lp.mean() - b * sc.mean()
        fit = path(ax, xs, a0 + b * xs, MGR, 3.0, smooth=False)
        bars_ = VGroup()
        for k, name in enumerate(order):
            v, y = by[name], -k * 0.42
            nm = label(SHORT[name], font_size=15, color=GREY_A).move_to([0, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=(v - 2.0) * 2.6, height=0.26, stroke_width=0, fill_color=OWN,
                            fill_opacity=0.85).move_to([0.15, y, 0], aligned_edge=LEFT)
            bars_.add(VGroup(nm, bar, label(f"{v:.2f}", font_size=14, color=WHITE).next_to(bar, RIGHT, buff=0.1)))
        bars_.to_edge(RIGHT, buff=0.5).shift(UP * 0.9)
        bh = label(r"mean score by owner", font_size=18, color=OWN).next_to(bars_, UP, buff=0.2)
        foot = label(rf"slope: \ {b:.2f} log points of productivity per point of score \\ (planted "
                     rf"{M['planted_slope']:.2f})", font_size=18, color=MGR).next_to(bars_, DOWN, buff=0.4)
        real = label(r"in the survey's data: \ the United States scores highest on average; \\ family firms run by "
                     r"the eldest son score low; \\ competition goes with better management", font_size=17,
                     color=E.ACCENT).next_to(foot, DOWN, buff=0.3)
        for m in (foot, real):
            if m.width > 5.8:
                m.width = 5.8
            m.align_to(bars_, RIGHT)
        tag = island_tag(r"the Island: \ 1,500 firms; \ ownership means and slope planted; \ agora.org.management"
                         .replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            "Here is the survey run on the Island's fifteen hundred firms. <bookmark mark='a'/> Each dot is a firm: "
            "its management score against its productivity. <bookmark mark='b'/> Better-managed firms are more "
            f"productive: {b:.2f} log points per point of score. On the Island that slope was planted, and it is "
            "causal by construction. In real survey data the same pattern appears, but a correlation alone cannot "
            "say which way it runs: profitable firms may simply afford consultants. <bookmark mark='c'/> By owner, "
            "multinationals and firms with dispersed shareholders score highest; family firms run by a family "
            "chief executive, and government firms, lowest. <bookmark mark='d'/> Those patterns were planted to "
            "echo the survey's real findings: across countries the United States scores highest on average, "
            "family firms that hand the top job to the eldest son score low, and firms facing more competition "
            "are better managed. Whether the scores cause productivity needs an experiment: chapter four."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.002), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(r_) for r_ in bars_], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(real))
        self.clear_scene()
