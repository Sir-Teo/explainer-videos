from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import BAD, FUND_C, HURDLE, LEV_C, PART, SPIRAL_C, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.claims(load("spiral"), load("research"), load("dd"), load("dash"))
        self.stakes()
        self.not_this()
        self.act()
        self.history()
        self.objectives()
        self.house()
        self.question()

    def title_card(self):
        card = part_title(PART, r"Leverage, Liquidity and Crises")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-one. Leverage, liquidity and crises: how borrowed money and short funding turn small losses into "
            "forced sales, forced sales into spirals, and one firm's trouble into everyone's. From LTCM to Silicon Valley "
            "Bank, with the mathematics of each."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def claims(self, sp, rs, dd, ds):
        k2 = [x for x in sp["rows"] if x["kappa"] == 2.0][0]
        cards = VGroup(
            desk_question(r"spirals amplify", rf"when lenders raise margins as prices fall, a 3\% shock to a levered "
                          rf"holder's asset ends as a {100 * k2['fall']:.0f}\% fall: {k2['amp']:.1f} times", width=12.4,
                          font_size=19),
            desk_question(r"links share, then spread", rf"in a complete network of ten banks, a shock to one up to "
                          rf"{rs['thr']:.0f} fells only that bank; beyond it all ten fail: a threshold in closed form", width=12.4,
                          font_size=19),
            desk_question(r"solvent banks can fail", rf"with assets worth 85\% if sold early, depositors run on any bank "
                          rf"whose assets return less than {dd['thr85']:.2f}: the run, not the losses, decides",
                          width=12.4, font_size=19),
            desk_question(r"even the safest asset", rf"in March 2020 the ten-year Treasury yield rose from "
                          rf"{ds['y10']['m9']:.2f}\% to {ds['y10']['m18']:.2f}\% in nine days as stocks fell", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> Spirals amplify: when lenders raise margins as prices fall, a "
            f"three percent shock ends as a {100 * k2['fall']:.0f} percent fall, {k2['amp']:.1f} times larger. "
            "<bookmark mark='b'/> Links between banks first share losses, then spread them: a complete network of ten "
            f"loses only the bank that was hit, for shocks up to {rs['thr']:.0f}; beyond, all ten fail. <bookmark mark='c'/> Solvent banks can "
            "fail: with assets that fetch eighty-five percent if sold early, a run hits any bank whose assets return less "
            f"than {dd['thr85']:.2f}. <bookmark mark='d'/> And even the safest asset can be sold in a panic: in March "
            f"twenty twenty, the Treasury yield rose from {ds['y10']['m9']:.2f} to {ds['y10']['m18']:.2f} percent as "
            "stocks fell."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"crises end firms", r"LTCM, Bear Stearns, Lehman, AIG, Archegos, SVB and Credit Suisse were "
                          r"large, admired, and gone within weeks", width=12.4, font_size=19),
            desk_question(r"and set the rules", r"Basel III, central clearing, stress tests, resolution plans and margin "
                          r"rules were each written after one", width=12.4, font_size=19),
            desk_question(r"why the House cares", r"every strategy it runs is financed by someone; Part 40 measured what it "
                          r"might lose, this part asks whether it can survive losing it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Crises end firms: LTCM, Bear Stearns, Lehman, AIG, Archegos, Silicon "
            "Valley Bank and Credit Suisse were large, admired, and gone within weeks. <bookmark mark='b'/> They set the "
            "rules: capital and liquidity ratios, central clearing, stress tests and margin rules were each written after "
            "one. <bookmark mark='c'/> And every strategy the House runs is financed by someone. Part forty measured what "
            "it might lose; this part asks whether it can survive losing it."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_this(self):
        cards = VGroup(
            desk_question(r"not prediction", r"no model here says when the next crisis comes; they say how a shock "
                          r"grows, and what makes a system fragile", width=12.4, font_size=19),
            desk_question(r"not blame", r"firms appear only as the public record describes them; allegations are "
                          r"labelled as reported", width=12.4, font_size=19),
            desk_question(r"not advice", r"the House's rule is a teaching example, not a recommendation to anyone",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And what this part is not. <bookmark mark='a'/> It is not prediction: no model here says when the next crisis "
            "comes, only how a shock grows and what makes a system fragile. <bookmark mark='b'/> It is not blame: firms "
            "appear as the public record describes them. <bookmark mark='c'/> And it is not advice."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Act seven, the system. Part forty measured risk one firm at a time. This part follows "
            "leverage and liquidity across firms, into crises. Then Part forty-two lets machines into the market, and "
            "Part forty-three asks whether any of it beats the market."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        R = BAD
        entries = [(1983, r"Diamond--Dybvig", I), (1987, r"the crash", R), (1992, r"Shleifer--Vishny", I),
                   (1998, r"LTCM", R), (2001, r"Eisenberg--Noe", I), (2008, r"Lehman, AIG", R),
                   (2009, r"Brunnermeier--Pedersen", I), (2010, r"Geanakoplos", I), (2015, r"Shanghai; contagion", R),
                   (2017, r"SRISK", I), (2020, r"the dash for cash", R), (2023, r"SVB, Credit Suisse", R)]
        strip = era_strip(entries, y0=1980, y1=2026, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Forty years of crises, and of their theory", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "Forty years of crises, and of the theory that followed them. Diamond and Dybvig's bank runs; the crash of "
            "nineteen eighty-seven; Shleifer and Vishny's limits to selling; LTCM. <bookmark mark='a'/> Eisenberg and "
            "Noe's clearing, Lehman and AIG, Brunnermeier and Pedersen's spirals, Geanakoplos's leverage cycle. "
            "<bookmark mark='b'/> Then Shanghai and the contagion threshold, SRISK, the dash for cash, and the runs of "
            "twenty twenty-three."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Leverage and haircuts; Minsky, Kindleberger and the leverage cycle",
            r"Loss and margin spirals; fire sales through common holdings",
            r"Networks: Eisenberg--Noe clearing and the contagion threshold",
            r"Systemic risk measured: CoVaR, MES and SRISK",
            r"Five crises: 1998, 2008, 2015, 2020 and 2022--23, from public data",
            r"Runs: Diamond--Dybvig and global games; the House's liquidity stress",
            r"For the researcher: the clearing theorem, proved and checked",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: leverage and its cycle; spirals and fire sales; networks of obligations; systemic risk measured; "
            "five crises from public data; bank runs and the House's own liquidity stress; and the theorem behind "
            "network clearing, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("treasury", "portfolio"))
        with self.voiceover(
            "In the House, the treasury and funding desk joins the risk function, and asks a question no risk number "
            "answers on its own: if every lender wanted more at once, what would the House have to sell?"
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()

    def question(self):
        rows = VGroup(label(r"a fund at 5$\times$ leverage loses 10\%", font_size=26),
                      label(r"its lender raises haircuts from 20\% to 30\%", font_size=26, color=GREY_A),
                      label(r"what must it sell?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        q = pause_card(r"a fund at 5$\times$ loses 10\%, and its haircut rises from 20\% to 30\%. What must it sell?")
        with self.voiceover(
            "A desk question to start. <bookmark mark='a'/> A fund at five times leverage loses ten percent. "
            "<bookmark mark='b'/> Its lender raises the haircut on its collateral from twenty to thirty percent. "
            "<bookmark mark='c'/> Pause and predict: how much must it sell?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
