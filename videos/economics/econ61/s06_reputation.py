from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Reputation(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Reputation", r"Why is almost every rating five stars, \ and what can a platform do about it?",
             "Chapter five. Reputation.", lit={2014: r"Airbnb's simultaneous reviews", 2015: r"Nosko and Tadelis"},
             scale=("person", "market"), horizon=("a year",))
        self.ratings()
        self.redesign()

    def ratings(self):
        R = load("reputation")
        h1, h2 = np.array(R["pp_hist"], float), np.array(R["epp_hist"], float)
        e1, e2 = np.linspace(0.9, 1.0, 21), np.linspace(0.4, 0.65, 21)
        top = max(h1.max(), h2.max()) * 1.15
        ax1 = plane([0.9, 1.0], [0, top], center=LEFT * 4.1 + UP * 0.2, x_length=4.2, y_length=3.6,
                    xticks=[0.9, 0.95, 1.0], yticks=[], xlabel=r"percent positive", ylabel=r"sellers",
                    xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ax2 = plane([0.4, 0.65], [0, top], center=LEFT * 0.0 + UP * 0.2, x_length=4.2, y_length=3.6,
                    xticks=[0.4, 0.5, 0.6], yticks=[], xlabel=r"effective percent positive", ylabel=r"sellers",
                    xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        b1 = bars(ax1, (e1[:-1] + e1[1:]) / 2, h1, [SELL] * 20, width=0.0045)
        b2 = bars(ax2, (e2[:-1] + e2[1:]) / 2, h2, [DRIVER] * 20, width=0.011)
        side = VGroup(
            label(r"2,000 Island sellers, \\ each good 80 to 99\% of the time".replace(",", "{,}"), font_size=18,
                  color=WHITE),
            label(r"happy buyers rate 60\% of the time; \\ unhappy ones complain 5\% of the time", font_size=18,
                  color=GREY_A),
            label(rf"percent positive: \\ median {100 * R['pp_median']:.1f}\%; \ {100 * R['share_above_98']:.0f}\% "
                  r"of sellers at 98\% or more", font_size=18, color=SELL),
            label(r"positives over all sales, \\ silence counted", font_size=18, color=DRIVER),
            label(rf"correlation with true quality: \\ {R['corr_pp']:.2f} \ against \ {R['corr_epp']:.2f}",
                  font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 4.3:
            side.width = 4.3
            side.to_edge(RIGHT, buff=0.35)
        foot = label(r"eBay's sellers (Nosko and Tadelis): \ percent positive, \ median 100\%, \ mean 99.3\%; \ "
                     r"effective percent positive, \ median 67\%, \ mean 64\%", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Nosko and Tadelis, \ NBER Working Paper 20830 (2015); \ the Island: \ "
                            r"agora.platform.reputation", corner=DL, font_size=12)
        with self.voiceover(
            "Ratings let strangers trust each other, and they have a famous problem: almost everyone is "
            "excellent. <bookmark mark='a'/> The Island's marketplace has two thousand sellers, each delivering a "
            "good transaction between eighty and ninety-nine percent of the time. <bookmark mark='b'/> Happy "
            "buyers leave a positive rating sixty percent of the time; unhappy ones mostly say nothing, and "
            "complain only five percent of the time. <bookmark mark='c'/> So the score the platform displays, "
            f"positive ratings over all ratings, piles up at the top: a median of {100 * R['pp_median']:.1f} "
            f"percent, with {100 * R['share_above_98']:.0f} percent of sellers at ninety-eight or more. <bookmark "
            "mark='d'/> Chris Nosko and Steven Tadelis proposed counting the silence: positive ratings over all "
            "transactions, the effective percent positive. It spreads the sellers out. <bookmark mark='e'/> And it "
            f"tracks their true quality better, a correlation of {R['corr_epp']:.2f} against {R['corr_pp']:.2f}. "
            "<bookmark mark='f'/> On eBay they found the displayed score had a median of one hundred percent and "
            "a mean of 99.3, while the effective score had a median of 67 percent. Their argument: a bad "
            "transaction hurts not only the seller but the platform, because a buyer who had one is less likely "
            "to come back at all."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(ax1), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.05),
                      FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(ax2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.05),
                      FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def redesign(self):
        cards = point_cards([
            (r"why ratings inflate", r"silence instead of complaints; \ fear of a retaliating review; \ raters "
             r"who feel sorry for the seller", SURGE),
            (r"Airbnb, \ 2014", r"an experiment hides each review until both sides have written theirs; \ fewer "
             r"retaliating and reciprocating reviews, \ slightly lower ratings, \ more reviews; \ then adopted "
             r"for everyone", RIDER),
            (r"count what is unsaid", r"effective percent positive; \ returns, \ complaints and repeat purchases "
             r"as signals", DRIVER),
            (r"the platform's stake", r"a rating system is a public good the platform must supply: \ each rater "
             r"helps strangers, \ not themselves", PLAT),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"redesigning a reputation system", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Fradkin, \ Grewal and Holtz, \ Marketing Science 40(6) (2021); \ Tadelis, \ Annual "
                            r"Review of Economics 8 (2016)", corner=DL, font_size=12)
        with self.voiceover(
            "What can a platform do? <bookmark mark='a'/> First see why ratings inflate: unhappy buyers stay "
            "silent, a bad review invites a bad one back, and raters feel sorry for the person they are rating. "
            "<bookmark mark='b'/> In 2014 Airbnb ran an experiment that hid each review until both guest and host "
            "had written theirs, so neither could retaliate. Andrey Fradkin, Elena Grewal and David Holtz found "
            "fewer retaliating and reciprocating reviews, slightly lower ratings, and more reviews written; the "
            "design was then given to everyone. <bookmark mark='c'/> Second, count what is unsaid: silence, "
            "returns, complaints and whether a buyer ever comes back. <bookmark mark='d'/> Underneath is "
            "Part fifteen's logic: a rating is a public good. Each rater helps strangers, not themselves, so "
            "ratings are undersupplied and shaded, and the platform, which gains from trust, has to supply the "
            "system that produces it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
