from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Hazard(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The price: \ moral hazard", r"If depositors never run, \ who watches the bank?",
             "Chapter seven. The price: moral hazard.", lit={1977: r"Merton", 1989: r"the S\&L clean-up"},
             scale=("firm", "nation"), horizon=("years",))
        self.put()
        self.history()

    def put(self):
        m = load("merton")
        ax = plane([0, 0.3], [0, 18], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 5, 10, 15],
                   xlabel=r"volatility of the bank's assets, \ a year",
                   ylabel=r"value today", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}",
                   font_size=16)
        own = DashedLine(ax.ax.c2p(0, m["V"] - m["D"]), ax.ax.c2p(0.3, m["V"] - m["D"]), color=GREY_B,
                         stroke_width=2)
        put = path(ax, m["sigma"], m["put"], color=CB, width=4)
        eq = path(ax, m["sigma"], m["equity"], color=EQUITY, width=4)
        hi = m["points"][-1]
        gap = Line(ax.ax.c2p(0.25, m["V"] - m["D"]), ax.ax.c2p(0.25, hi["equity"]), color=CB, stroke_width=5)
        side = VGroup(
            label(rf"assets {m['V']:.0f}, \ insured deposits {m['D']:.0f}: \\ the owners' own money is "
                  rf"{m['V'] - m['D']:.0f}", font_size=20, color=GREY_A),
            label(r"deposit insurance is a put: \\ the insurer pays any shortfall", font_size=20, color=CB),
            label(rf"at 25\% volatility: \ the put is worth {hi['put']:.1f}, \\ and the owners' stake "
                  rf"{hi['equity']:.1f}", font_size=20, color=EQUITY),
            label(r"with a flat premium, \\ the insurer's loss is the owners' gain: \\ insurance rewards "
                  r"risk-taking", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Merton, \ J.\ Banking \& Finance 1(1) (1977): \ 3--11", corner=DR, font_size=12)
        with self.voiceover(
            "Every cure has a price. Robert Merton showed in 1977 how to value deposit insurance. "
            f"<bookmark mark='a'/> Take a bank with assets of {m['V']:.0f} and insured deposits of {m['D']:.0f}, so "
            f"the owners' own money, the dashed line, is {m['V'] - m['D']:.0f}. <bookmark mark='b'/> The insurer pays "
            "depositors whatever the assets fall short of a year from now. That is a put option on the bank's "
            "assets, and its value, in blue, rises steeply with how risky those assets are. "
            "<bookmark mark='c'/> In green, the value of the owners' stake. With assets as volatile as a quarter of "
            f"their value in a year, the put is worth {hi['put']:.1f}, and the owners' stake is worth "
            f"{hi['equity']:.1f}, not {m['V'] - m['D']:.0f}. <bookmark mark='d'/> If the premium is flat, every "
            "dollar of the insurer's expected loss is a dollar for the owners. So insurance rewards the bank for "
            "taking risks, unless it is priced to the risk, capped, or matched by rules. Depositors who never run "
            "also never watch."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(own), FadeIn(side[0]), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(put), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(eq), FadeIn(side[2]), Create(gap), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def history(self):
        rows = VGroup(
            label(r"the savings and loans, \ 1980s", font_size=27, color=E.ACCENT),
            label(r"thrifts held long fixed-rate mortgages, \ funded by insured deposits", font_size=22,
                  color=GREY_A),
            label(r"when rates jumped, \ many were insolvent; \ allowed to keep going, \ some gambled for "
                  r"resurrection", font_size=22, color=RUN),
            label(r"the clean-up: \ up to about \$124 billion to taxpayers", font_size=24, color=RUN),
            label(r"too big to fail: \ when creditors expect a rescue, \ the biggest banks borrow more cheaply \ "
                  r"(Part 33)", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Federal Reserve History, \ ``Savings and Loan Crisis''; \ Curry and Shibut, FDIC "
                            r"Banking Review 13(2) (2000)", corner=DR, font_size=12)
        with self.voiceover(
            "America learned this the expensive way. <bookmark mark='a'/> In the 1980s, the savings and loan "
            "associations held long, fixed-rate mortgages, funded by insured deposits. <bookmark mark='b'/> When "
            "interest rates jumped, many became insolvent. Allowed to keep operating, some gambled on risky loans: "
            "if the bets paid off, the owners recovered; if not, the insurer paid. <bookmark mark='c'/> The "
            "clean-up cost taxpayers as much as a hundred and twenty-four billion dollars. "
            "<bookmark mark='d'/> The same logic applies to banks so large that creditors expect a rescue: they can "
            "borrow more cheaply, and grow larger. Part thirty-three returns to too big to fail."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
