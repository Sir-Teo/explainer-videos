from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ new auctions, \ new bidders", r"What happens "
             r"when the seller can cheat, \ the bidders are machines, \ and the goods must be bought back first?",
             "Chapter fifteen. Frontier: new auctions, new bidders.",
             lit={2017: r"the incentive auction", 2019: r"display ads go first-price", 2020: r"Akbarpour and Li"},
             scale=("market", "nation"), horizon=("a decade",))
        self.incentive()
        self.credible()
        self.machines()
        self.open_q()

    def incentive(self):
        f = load("spectrum")["fcc"]
        hc = history_card(2017, r"the FCC's broadcast incentive auction", r"buy the airwaves back from television "
                          r"stations, \ and sell them to phone companies, \ at once", color=SECOND, width=11.6,
                          font_size=24).to_edge(UP, buff=0.4)
        left = VGroup(
            label(r"the reverse auction", font_size=28, color=FIRST),
            label(r"a falling clock: \ each station \\ stays, \ or sells its channel", font_size=23, color=GREY_A),
            label(r"a computer checks, \ at every step, \\ that the stations left can be \\ repacked into fewer "
                  r"channels", font_size=23, color=GREY_A),
            label(rf"\${f['reverse_bn']:.2f} billion \\ to {f['stations']} stations", font_size=28, color=FIRST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        right = VGroup(
            label(r"the forward auction", font_size=28, color=SECOND),
            label(r"a rising clock: \\ phone companies bid \\ for the freed spectrum", font_size=23, color=GREY_A),
            label(r"if the sale didn't cover the purchase, \\ try again, \ clearing less",
                  font_size=23, color=GREY_A),
            label(rf"\${f['forward_bn']:.1f} billion; \\ {f['mhz']} MHz cleared", font_size=28, color=SECOND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(left, right).arrange(RIGHT, buff=1.4, aligned_edge=UP).next_to(hc, DOWN, buff=0.45)
        foot = label(r"Milgrom and Segal: \ a falling clock is ``obviously strategy-proof'': \ stay while the price "
                     r"beats your value", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"FCC, Auction 1000 (2017); \ Milgrom and Segal, JPE 128(1) (2020)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The largest design problem yet was the FCC's incentive auction, which closed in April 2017. The "
            "spectrum phone companies wanted was being used by television stations, so the auction had to buy it "
            "back and sell it on, at the same time. <bookmark mark='a'/> In the reverse auction, a clock offered each "
            "station a falling price for its channel, and each decided whether to stay on the air or sell. At every "
            "step a computer checked that the stations still broadcasting could be repacked into fewer channels, "
            "a hard puzzle, solved again and again. It paid ten billion dollars to a hundred and seventy-five "
            "stations. <bookmark mark='b'/> In the forward auction, phone companies bid on a rising clock for the "
            "spectrum freed. If their bids did not cover what the stations were paid, the auction tried again, "
            "aiming to clear less spectrum, stage by stage, until they did: nineteen point eight billion dollars, "
            "for eighty-four megahertz. <bookmark mark='c'/> Paul Milgrom and Ilya Segal "
            "designed the clocks so that a station's best plan was plain even to someone who does not trust game "
            "theory: stay in while the price beats your value. Such an auction is called obviously "
            "strategy-proof."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def credible(self):
        rows = VGroup(
            label(r"Goethe's problem, \ formalized: \ a seller can cheat in ways bidders can't see", font_size=24),
            label(r"in a sealed second-price auction, \ a fake second bid just below the winner's is undetectable",
                  font_size=23, color=HOLD),
            label(r"Akbarpour and Li (2020): \ among optimal auctions, \ the first-price is the only credible sealed "
                  r"one", font_size=23, color=FIRST),
            label(r"and the ascending clock the only credible one in which honesty is dominant", font_size=23,
                  color=SECOND),
            label(r"2019: \ the exchanges selling display ads moved from second price to first", font_size=24,
                  color=E.ACCENT),
            label(r"buyers could not check the second price they were charged", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Akbarpour and Li, Econometrica 88(2) (2020)", corner=DR, font_size=13)
        with self.voiceover(
            "Chapter three's poet comes back. <bookmark mark='a'/> In 2020 Mohammad Akbarpour and Shengwu Li asked "
            "which auctions a seller cannot cheat in without being caught. <bookmark mark='b'/> In a sealed "
            "second-price auction, a seller can slip in a fake bid just below the winner's, and nobody can tell. "
            "<bookmark mark='c'/> They proved that among the auctions that raise the most, the first-price auction "
            "is the only sealed one that is credible, since the winner pays what it bid, whatever else was "
            "written. <bookmark mark='d'/> And the ascending clock is the only credible one in which honest bidding "
            "is dominant, since everyone sees the price rise. <bookmark mark='e'/> The market had found the same "
            "thing. In 2019 the big exchanges that sell display advertisements on websites moved from second price "
            "to first. <bookmark mark='f'/> Among the reasons: advertisers, bidding through many layers of software, "
            "could not check the second price they were charged."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def machines(self):
        rows = VGroup(
            label(r"most advertisers no longer bid: \ they set a budget and a target, \ and software bids for them",
                  font_size=23),
            label(r"the software maximizes value bought, \ subject to a return on each dollar: \ not profit",
                  font_size=23, color=ALLPAY),
            label(r"then even Vickrey's auction loses its dominant strategy", font_size=23, color=HOLD),
            label(r"the guarantee: \ at least half the best possible value \ (Aggarwal, \ Badanidiyuru and Mehta, "
                  r"\ 2019)", font_size=22, color=E.ACCENT),
            label(r"and a seller who learns reserves from past bids \ teaches bidders to shade, \ to lower the next "
                  r"reserve", font_size=22, color=RESERVE),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Aggarwal, Badanidiyuru and Mehta, WINE (2019); \ Amin, Rostamizadeh and Syed, NeurIPS "
                            r"(2013)", corner=DR, font_size=12)
        with self.voiceover(
            "The bidders are changing too. <bookmark mark='a'/> Most advertisers no longer choose bids. They set a "
            "budget and a target, so many dollars of sales per dollar spent, and the platform's software bids for "
            "them in every auction. <bookmark mark='b'/> That software buys as much value as it can, subject to the "
            "target. It does not maximize profit, which is what every theorem in this part assumed. "
            "<bookmark mark='c'/> And with such bidders, even Vickrey's auction loses its dominant strategy. "
            "<bookmark mark='d'/> What survives is a guarantee: Gagan Aggarwal, Ashwinkumar Badanidiyuru and Aranyak "
            "Mehta showed in 2019 that with these bidders, Vickrey's rule still delivers at least half the best "
            "possible value. <bookmark mark='e'/> Sellers are learning too, and that has its own trap: a seller "
            "who sets tomorrow's reserve from today's bids gives bidders a reason to bid low today, to lower "
            "tomorrow's reserve."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open_q(self):
        head = label(r"open questions", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        qs = VGroup(
            label(r"when machines bid against machines, \ what equilibrium, \ if any, \ do they reach?", font_size=24),
            label(r"can a seller learn reserves without being gamed, \ and how fast?", font_size=24, color=RESERVE),
            label(r"how should auctions sell things that come in packages, \ such as compute, \ spectrum and "
                  r"electricity at once?", font_size=24, color=SECOND),
            label(r"when an auction design is copied, \ how do we know it fits the new bidders?", font_size=24,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So the frontier has open questions. <bookmark mark='a'/> When software bids against software, what "
            "equilibrium do they reach, if any? <bookmark mark='b'/> Can a seller learn the right reserve without "
            "being gamed, and how quickly? <bookmark mark='c'/> How should auctions sell things that come in "
            "packages, such as computing power, spectrum, or electricity across hours? <bookmark mark='d'/> And "
            "when a design is copied from one country or one market to another, how do we know it fits the new "
            "bidders? The Dutch learned that one the expensive way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcd", qs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
