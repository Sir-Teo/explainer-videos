from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Retro(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Retrospectives", r"Years later: \ were the predictions right?",
             "Chapter twelve. Retrospectives.", lit={2010: r"Ashenfelter and Hosken", 2019: r"Cooper et al.",
                                                     2024: r"Brot-Goldberg et al."},
             scale=("market", "nation"), horizon=("a year", "a decade"))
        self.island()
        self.real()

    def island(self):
        R = load("retro")
        months = np.array(R["months"])
        tr, co = np.array(R["treated"]), np.array(R["control"])
        tr = 100 * tr / tr[months < 0].mean()
        co = 100 * co / co[months < 0].mean()
        ax = plane([-12, 12], [96, 120], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.8,
                   xticks=[-12, -6, 0, 6, 12], yticks=[100, 105, 110, 115, 120], xlabel=r"months from the merger",
                   ylabel=r"Alder's price, \ before = 100", xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v
                   else "0", yfmt=lambda v: f"{v:.0f}", font_size=14)
        zero = vline(ax, -0.5, 96, 120, E.ACCENT, 1.6)
        pt = path(ax, months, tr, BIRCH, 3.0, smooth=False)
        pc = path(ax, months, co, ALDER, 3.0, smooth=False)
        key = VGroup(label(rf"gold: \ {R['n_treated']} towns where Alder and Birch met", font_size=15, color=BIRCH),
                     label(rf"blue: \ {R['n_control']} towns where they did not", font_size=15, color=ALDER)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.ax.c2p(-12, 120), RIGHT, buff=0.1).shift(DOWN * 0.15)
        rows = VGroup(
            label(r"difference in differences:", font_size=20, color=GREY_A),
            label(rf"the merger raised Alder's price {R['estimate']:.1f}\%", font_size=23, color=WHITE),
            label(rf"the truth: \ {R['predicted']:.1f}\%", font_size=20, color=GREY_A),
            label(rf"the GUPPI screen said {R['guppi']:.1f}\%", font_size=21, color=GOV),
            label(rf"the agency's plain logit said {R['agency']:.1f}\%", font_size=21, color=SIM),
            label(r"a retrospective scores the tools, \\ not just the merger", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ the merger consummated, \ prices with common shocks and noise", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Suppose the Island's court let the merger through. A year later, an economist at the agency runs a "
            "retrospective. <bookmark mark='a'/> In the towns where Alder and Birch met, prices after the merger "
            "are compared with prices before; <bookmark mark='b'/> in the towns where they did not meet, the same, "
            "to remove whatever else changed. <bookmark mark='c'/> The difference in differences: the merger raised "
            f"Alder's price by {R['estimate']:.1f} percent, close to the truth of {R['predicted']:.1f}. <bookmark "
            f"mark='d'/> Now set the predictions against it. The GUPPI screen said {R['guppi']:.1f}. The agency's "
            f"plain-logit simulation said {R['agency']:.1f}, too low, for the reason of chapter six. <bookmark "
            "mark='e'/> That is the real value of a retrospective: it scores the tools, so that the next "
            "prediction is made with a better one."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(pt), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(pc), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def real(self):
        cards = VGroup(
            history_card(2010, r"Orley Ashenfelter and Daniel Hosken", r"five consumer-product mergers the agencies "
                         r"had let through: \ four raised prices, \ typically by 3 to 7\%", color=ALDER, width=11.8,
                         font_size=19),
            history_card(2019, r"Zack Cooper, \ Stuart Craig, \ Martin Gaynor and John Van Reenen",
                         r"hospital mergers within five miles of each other: \ prices about 6\% higher afterwards",
                         color=WORK, width=11.8, font_size=19),
            history_card(2024, r"Brot-Goldberg, \ Cooper, \ Craig and Klarnet", r"the FTC challenged 13 hospital "
                         r"mergers in 2000--2020, \ about 1\%; \ standard screens would have flagged about 20\%",
                         color=CARTEL, width=11.8, font_size=19),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.35)
        note_ = label(r"the samples are selected: \ mergers studied are those someone thought worth studying",
                      font_size=19, color=HOLD).next_to(cards, DOWN, buff=0.4)
        tag = published_tag(r"Ashenfelter and Hosken, JLE (2010); \ Cooper et al., QJE (2019), \ as summarized in "
                            r"Gaynor's testimony; \ Brot-Goldberg et al., AER: Insights (2024)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Real retrospectives have become a literature of their own. <bookmark mark='a'/> Orley Ashenfelter and "
            "Daniel Hosken studied five consumer-product mergers that the agencies had let through, near the line "
            "where they might have been challenged. Four raised prices, typically by three to seven percent. "
            "<bookmark mark='b'/> Zack Cooper and his coauthors found that mergers between hospitals within five "
            "miles of each other were followed by prices about six percent higher. <bookmark mark='c'/> And a 2024 "
            "study counted only thirteen hospital mergers challenged by the Federal Trade Commission between 2000 "
            "and 2020, about one percent of them, when the agency's own standard screens would have flagged about "
            "a fifth. <bookmark mark='d'/> These samples are selected, by data and by interest, and averaging across "
            "them is risky; Part forty-four's Dial records the disagreement. Read together, they suggest that "
            "American review has let through more harmful mergers than it has blocked harmless ones, though that "
            "conclusion is itself disputed."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()
