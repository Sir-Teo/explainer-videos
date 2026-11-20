from __future__ import annotations

from videos.economics.econ25.s12_banks import tacct
from videos.economics.econ26.common import *  # noqa: F403


class Shadow(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Runs without depositors", r"Where did the run of 2007--08 happen?", "Chapter nine. Runs "
             "without depositors.", lit={2008: r"the Reserve Primary Fund", 2012: r"Gorton and Metrick"},
             scale=("firm", "nation"), horizon=("a day", "a year"))
        self.repo()
        self.haircuts()
        self.funds()
        self.lesson()

    def repo(self):
        R = load("repo")
        dealer = tacct(r"a dealer bank", BOND, [(rf"securities \ {R['assets']:.0f}", BOND)],
                       [(rf"repo \ {R['repo_from']:.0f}", RUN), (rf"equity \ {R['equity']:.0f}", EQUITY)],
                       width=5.0).move_to(UP * 1.2)
        rows = VGroup(
            label(r"repo: \ sell a bond today, \ promise to buy it back tomorrow at a slightly higher price",
                  font_size=22,
                  color=GREY_A),
            label(r"in effect, \ an overnight loan secured by the bond, \ rolled over every day", font_size=22,
                  color=GREY_A),
            label(rf"the haircut: \ lend only {100 * (1 - R['haircut_from']):.0f} against a bond worth 100",
                  font_size=22,
                  color=RUN),
            label(r"the lenders are money funds, \ companies' treasurers, \ other banks: \ no insurance", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Gorton and Metrick, \ J.\ Financial Economics 104(3) (2012): \ 425--451", corner=DR,
                            font_size=12)
        with self.voiceover(
            "By 2007, much of America's lending no longer ran through deposits at all. <bookmark mark='a'/> Here is a "
            f"dealer bank holding {R['assets']:.0f} of securities, funded by {R['equity']:.0f} of its own money and "
            f"{R['repo_from']:.0f} of repo. A repo is a sale of a bond today with a promise to buy it back tomorrow at "
            "a slightly higher price. <bookmark mark='b'/> In effect it is an overnight loan, secured by the bond, "
            "rolled over every day. <bookmark mark='c'/> The lender keeps a margin, called the haircut: it lends only "
            f"{100 * (1 - R['haircut_from']):.0f} against a bond worth a hundred. <bookmark mark='d'/> And the lenders "
            "are money market funds, companies' treasurers and other banks, with no deposit insurance behind them. "
            "Gary Gorton and Andrew Metrick argued that this is where the run of 2007 and 2008 happened."
        ) as vo:
            self.play(FadeIn(dealer), FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def haircuts(self):
        R = load("repo")
        ax = plane([0, 0.5], [0, 52], center=LEFT * 2.3 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 10, 20, 30, 40, 50],
                   xlabel=r"the haircut", ylabel=r"largest possible assets per unit of equity",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}", font_size=16)
        curve = path(ax, R["h"], R["lev"], color=BOND, width=4, yr=(0, 52))
        d0 = dot(ax, R["haircut_from"], R["max_leverage_from"], color=STAY, r=0.09)
        d1 = dot(ax, R["haircut_to"], R["max_leverage_to"], color=RUN, r=0.09)
        side = VGroup(
            label(r"with haircut $h$, \\ assets $\le$ equity $/\, h$", font_size=21, color=BOND),
            label(rf"at {100 * R['haircut_from']:.0f}\%: \ up to {R['max_leverage_from']:.0f} times equity",
                  font_size=20, color=STAY),
            label(rf"at {100 * R['haircut_to']:.0f}\%: \ up to {R['max_leverage_to']:.0f} times", font_size=20,
                  color=RUN),
            label(rf"the dealer can now carry {R['can_hold_after']:.0f}: \\ it must sell {R['must_sell']:.0f}, \\ "
                  r"into a market where everyone is selling", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A run on repo does not look like a queue. It looks like a number. <bookmark mark='a'/> If lenders keep "
            "a haircut h, a dealer can hold at most its equity divided by h. <bookmark mark='b'/> At a haircut of "
            f"{100 * R['haircut_from']:.0f} percent, that is {R['max_leverage_from']:.0f} times its equity. "
            f"<bookmark mark='c'/> In 2007 and 2008, lenders worried about what the bonds were worth and raised "
            f"haircuts. At {100 * R['haircut_to']:.0f} percent, the most it can hold is {R['max_leverage_to']:.0f} "
            f"times its equity. <bookmark mark='d'/> So with the same {R['equity']:.0f} of equity, the dealer can "
            f"now carry only {R['can_hold_after']:.0f} of securities, and must sell {R['must_sell']:.0f}, into a "
            "market where everyone else is selling too. Raising the haircut is withdrawing the deposit. Gorton and "
            "Metrick's data covered only some kinds of collateral, and critics argue the run was smaller in the "
            "wider repo market; that it happened in securitized bonds is not in doubt."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(d0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(d1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def funds(self):
        m = load("mmf")
        ax = plane([1980, 2027], [0, 9], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6, 8],
                   ylabel=r"money market funds' assets, \ trillions of dollars", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        line_ = path(ax, m["t"], m["v"], color=DEPOSIT, width=3, smooth=False)
        k08 = int(np.argmin(np.abs(np.array(m["t"]) - 2008.75)))
        mark = dot(ax, m["t"][k08], m["v"][k08], color=RUN, r=0.09)
        side = VGroup(
            label(r"16 September 2008: \\ the Reserve Primary Fund \\ ``breaks the buck''", font_size=20, color=RUN),
            label(r"\$785 million of Lehman's paper, \\ about 1\% of the fund: \\ its shares fall to 97 cents",
                  font_size=19, color=GREY_A),
            label(r"19 September: \\ the Treasury guarantees \\ money funds' shares", font_size=19, color=CB),
            label(rf"the total rose: \ {m['q2_2008']:.2f} to {m['q4_2008']:.2f} trillion; \\ money fled prime "
                  r"funds \\ for government funds", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve, \ Financial Accounts: \ money market funds' total financial assets, \ via "
                       r"FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Money market funds took deposits in all but name: shares meant to be worth exactly one dollar, which "
            "you could withdraw at any time. <bookmark mark='a'/> On the sixteenth of September 2008, the day after "
            "Lehman Brothers failed, the oldest of them, the Reserve Primary Fund, broke the buck. "
            "<bookmark mark='b'/> It held seven hundred and eighty-five million dollars of Lehman's short-term "
            "paper, about one percent of the fund, and its shares were marked down to ninety-seven cents. "
            "By that afternoon, investors had asked for about a quarter of the fund's money. "
            "<bookmark mark='c'/> On the "
            "nineteenth, the Treasury guaranteed money funds' shares. <bookmark mark='d'/> Here is the strange "
            f"part: money funds' total assets rose that autumn, from {m['q2_2008']:.1f} to {m['q4_2008']:.1f} trillion "
            "dollars. The money did not leave the funds. It left the prime funds, which lend to companies, for "
            "funds that hold only government debt. The run was on companies' short-term borrowing. In March 2020, "
            "prime funds ran again, and the Federal Reserve set up a facility to lend against their assets."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(mark), FadeIn(side[0]))
            for mk, r_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def lesson(self):
        rows = VGroup(
            label(r"shadow banking: \ maturity transformation outside the banks", font_size=27, color=E.ACCENT),
            label(r"short, \ runnable funding: \ repo, \ commercial paper, \ money-fund shares", font_size=23,
                  color=RUN),
            label(r"long or illiquid assets: \ mortgage bonds, \ loans to companies", font_size=23, color=LOAN),
            label(r"no insurance, \ and in 2007 no lender of last resort", font_size=23, color=HOLD),
            label(r"in 2008 the Fed lent to dealers and funds, \ and in effect became one", font_size=23, color=CB),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The lesson. <bookmark mark='a'/> Shadow banking is maturity transformation outside the banks. "
            "<bookmark mark='b'/> It is funded short, by repo, commercial paper and money-fund shares, all of which "
            "can run. <bookmark mark='c'/> It holds long or illiquid assets: mortgage bonds and loans to companies. "
            "<bookmark mark='d'/> It had no deposit insurance, and in 2007 no lender of last resort. "
            "<bookmark mark='e'/> In 2008, the Federal Reserve lent to dealers and money funds directly, and in "
            "effect became one. Diamond and Dybvig's model fits wherever there is short funding and long assets."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(Indicate(rows[4], color=WHITE))
        self.clear_scene()
