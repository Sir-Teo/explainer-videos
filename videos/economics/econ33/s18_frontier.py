from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ crises in models and in new places", r"Where will the next one come from?",
             "Chapter sixteen. Frontier: crises in models and in new places.",
             lit={2014: r"Brunnermeier and Sannikov", 2020: r"the dash for cash"}, scale=("market", "world"),
             horizon=("a year", "a decade"))
        self.paradox()
        self.nonbanks()
        self.questions()

    def paradox(self):
        rows = VGroup(
            label(r"linearized models: \ crises are just big shocks", font_size=25, color=GREY_A),
            label(r"Brunnermeier and Sannikov (2014): \ solve the model whole, \ and it has two regimes", font_size=25,
                  color=E.ACCENT),
            label(r"near normal times: \ stable; \ after losses: \ prices, \ leverage and volatility feed on each "
                  r"other", font_size=22, color=CRISIS),
            label(r"the volatility paradox: \ quieter times invite more leverage, \ so risk builds when it looks "
                  r"lowest", font_size=22, color=HOUSE),
        ).arrange(DOWN, buff=0.48).move_to(UP * 0.2)
        tag = published_tag(r"Brunnermeier and Sannikov, \ \emph{AER} 104(2) (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "Where is the research now? <bookmark mark='a'/> The models of Parts twenty-nine and thirty are usually "
            "solved near their steady state, where a crisis can only be a large shock. <bookmark mark='b'/> Markus "
            "Brunnermeier and Yuliy Sannikov solved a model with a financial sector globally, and found two "
            "regimes. <bookmark mark='c'/> Near normal times the economy is stable. After losses push experts' net "
            "worth down, prices, leverage and volatility feed on each other, the loops of chapters four to six, "
            "and the economy can stay in the bad region for a long time. <bookmark mark='d'/> And a volatility "
            "paradox: when measured risk is low, the experts borrow more, so the system is most fragile when it "
            "looks safest. Minsky's idea, as an equation."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def nonbanks(self):
        F = load("frontier")
        ax = plane([2000, 2027], [0, 9], center=LEFT * 1.8 + DOWN * 0.4, x_length=9.0, y_length=4.4,
                   xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 3, 6, 9],
                   ylabel=r"money market funds' assets, \ \$ trillion", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, F["t"], F["mmf"], CB, 3.2, xr=(2000, 2027), smooth=False)
        side = VGroup(
            label(rf"2008: \ \${F['peak08']:.1f} trillion", font_size=20, color=CB),
            label(rf"{F['last_date'][:4]}: \ \${F['last']:.1f} trillion", font_size=20, color=CB),
            label(r"runnable money \\ outside the banks: \\ rescued in 2008, \\ and again in March 2020", font_size=19,
                  color=CRISIS),
            label(r"the new questions: \\ funds, \ insurers, \ private credit, \\ stablecoins; \ climate and \\ "
                  r"cyber risk", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Board of Governors, \ Financial Accounts (Z.1), \ via FRED: \ MMMFFAQ027S", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Second, the next crisis may not start in a bank. <bookmark mark='a'/> Money market funds, whose shares "
            "behave like deposits without being insured, held "
            f"{F['peak08']:.1f} trillion dollars in 2008, when one broke the buck. <bookmark mark='b'/> They now "
            f"hold {F['last']:.1f} trillion. <bookmark mark='c'/> In March 2020, in the dash for cash at the start "
            "of the pandemic, they had to be rescued again, and even the market for Treasury bonds came under severe "
            "strain. <bookmark mark='d'/> Regulators are now asking the questions of this part about investment "
            "funds, insurers, private credit and stablecoins, and about risks that are new: a changing climate that "
            "reprices whole classes of assets, and a cyber attack that stops payments."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"when to lean against a boom, \ and with which tool", font_size=22, color=BANK),
            label(r"how much of a crisis's cost is the crisis, \ and how much the boom before it", font_size=22,
                  color=CRISIS),
            label(r"whether known rescues make the next boom bigger", font_size=22, color=HOLD),
            label(r"where the leverage has gone: \ out of banks, \ into funds and private credit", font_size=22,
                  color=CREDIT),
            label(r"why nobody notices, \ again: \ the Queen's question has not gone away", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.2)
        tag = published_tag(r"Brunnermeier and Sannikov (2014); \ Jord\`a, \ Schularick and Taylor (2013); \ "
                            r"Greenwood et al. (2022)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> When to lean against a boom, and with which tool, given how "
            "often booms end quietly. <bookmark mark='b'/> How much of a crisis's cost is the crisis itself, and "
            "how much the boom and misallocation that came before it. <bookmark mark='c'/> Whether rescues that "
            "everyone now expects make the next boom bigger. <bookmark mark='d'/> Where the leverage has gone, now "
            "that so much lending happens outside banks. <bookmark mark='e'/> And the Queen's question, which has "
            "not gone away: why the many bright people inside a system find it so hard to see the risk of the "
            "whole."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
