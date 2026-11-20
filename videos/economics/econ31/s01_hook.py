from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.sentence()
        self.yields()
        self.question()
        self.title()
        self.objectives()

    def sentence(self):
        S = load("spreads")
        head = VGroup(label(r"London, \ 26 July 2012", font_size=30, color=E.ACCENT),
                      label(r"Spain's 10-year yield this month: \ " + rf"{S['jul12']['ES']:.1f}\%; \ Italy's "
                            rf"{S['jul12']['IT']:.1f}\%; \ Germany's {S['jul12']['DE']:.1f}\%", font_size=23,
                            color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.7)
        q = quote_card(r"Within our mandate, \ the ECB is ready to do whatever it takes to preserve the euro. \ "
                       r"And believe me, \ it will be enough.", r"Mario Draghi, \ President of the European Central "
                       r"Bank", width=10.4, font_size=30, color=CB).next_to(head, DOWN, buff=0.6)
        foot = label(r"the programme he announced in September was never used", font_size=24, color=PRICE).next_to(
            q, DOWN, buff=0.55)
        tag = published_tag(r"Draghi, \ speech at the Global Investment Conference, \ London, \ 26 July 2012; \ OECD "
                            r"bond yields via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "On the twenty-sixth of July 2012, the euro looked as if it might break apart. Spain was paying "
            f"{S['jul12']['ES']:.1f} percent to borrow for ten years, Italy {S['jul12']['IT']:.1f}, while Germany paid "
            f"{S['jul12']['DE']:.1f}. Investors were pricing the chance that a country would leave the currency, "
            "or default. <bookmark mark='a'/> That day the president of the European Central Bank, Mario Draghi, "
            "told an investment conference in London: within our mandate, the ECB is ready to do whatever it takes "
            "to preserve the euro. And believe me, it will be enough. <bookmark mark='b'/> In September the bank "
            "announced the programme behind the sentence: it would buy a country's short-term bonds without limit, "
            "on conditions. It never bought a single one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def yields(self):
        S = load("spreads")
        t = np.array(S["t"])
        ax = plane([2007, 2017], [0, 8], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2008, 2010, 2012, 2014, 2016], yticks=[0, 2, 4, 6, 8],
                   ylabel=r"10-year government bond yield, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        lines = {c: path(ax, t, S[c], COUNTRY[c], 3 if c in ("IT", "ES") else 2.4, smooth=False)
                 for c in ("DE", "GB", "IT", "ES")}
        jul = vline(ax, 2012.54, 0, 8, E.ACCENT, 2.5)
        jtag = label(r"26 July 2012", font_size=16, color=E.ACCENT).next_to(ax.ax.c2p(2012.54, 8), UP, buff=0.08)
        side = VGroup(
            label(r"grey: \ Germany", font_size=18, color=COUNTRY["DE"]),
            label(r"blue: \ Britain, \ outside the euro", font_size=18, color=COUNTRY["GB"]),
            label(r"green: \ Italy; \ gold: \ Spain", font_size=18, color=COUNTRY["IT"]),
            label(rf"two years later: \ Spain {S['jul14']['ES']:.1f}\%, \\ Italy {S['jul14']['IT']:.1f}\%",
                  font_size=19,
                  color=E.ACCENT),
            label(r"a sentence, \ and a promise \\ that was never tested", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OECD, \ long-term government bond yields, \ monthly, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Here are the yields, month by month. <bookmark mark='a'/> Germany's in grey, and Britain's in blue: "
            "Britain is outside the euro and borrows in a currency its own central bank issues. "
            "<bookmark mark='b'/> Italy in green and Spain in gold climb away from them from 2010. "
            "<bookmark mark='c'/> Then the sentence. <bookmark mark='d'/> Two years later Spain paid "
            f"{S['jul14']['ES']:.1f} percent and Italy {S['jul14']['IT']:.1f}, about what Britain paid. "
            "<bookmark mark='e'/> Their debts had not shrunk in those two years; they had grown. What "
            "changed was a promise by a central bank, which never had to be kept. This part asks how a central bank "
            "can do that, and how anyone can tell what it achieves."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(lines["DE"]), Create(lines["GB"]), FadeIn(side[0]), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(lines["IT"]), Create(lines["ES"]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(jul), FadeIn(jtag))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what does a central bank do, \ day to day, \ to set an interest rate?", font_size=26, color=CB),
            label(r"how can anyone measure what its decisions do, \ when it acts on what it sees?", font_size=26,
                  color=OUTPUT),
            label(r"what can it do when its rate is at zero, \ or a country's debt is under attack?", font_size=26,
                  color=BOND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: what does a central bank actually do, and how do we know what it achieves? "
            "<bookmark mark='a'/> What it does, day to day, to set an interest rate. <bookmark mark='b'/> How anyone "
            "can measure the effects of its decisions, when it makes them because of what it sees coming. "
            "<bookmark mark='c'/> And what it can do when its rate is already at zero, or when a country's debt is "
            "under attack."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1954, 2027], [0, 20], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["ff"], RATE, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 31 \ $\cdot$ \ The Central Bank", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-one: the central bank."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the balance sheet: \ reserves, \ a corridor and a floor; \ a seat in the chair in 1979",
            r"how a rate reaches the economy; \ why its effects are hard to measure",
            r"four ways to identify a policy shock, \ scored on the Island against the truth",
            r"rules with the data of the day; \ the zero bound, \ QE, \ guidance, \ negative rates",
            r"the neutral rate; \ the euro and the lender of last resort; \ communication; \ dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The central bank's balance sheet, the market for reserves, and "
            "how a rate is set there; then you take the chair in 1979. <bookmark mark='b'/> How the rate reaches "
            "spending and prices, and why its effects are so hard to measure. <bookmark mark='c'/> Four answers to "
            "that problem, each run on the Island, where the true effect is known. <bookmark mark='d'/> Policy rules "
            "with the data of the day, and the tools for when the rate is at zero: asset purchases, promises, "
            "negative rates. <bookmark mark='e'/> The neutral rate of interest, the euro crisis, the central bank's "
            "words as a tool, and three dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
