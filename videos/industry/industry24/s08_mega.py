from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403

OVER_NAME = {"suez": "Suez Canal", "scot": "Scottish Parliament", "sydney": "Sydney Opera House",
             "nhs": "NHS IT system (UK)", "bigdig": "Boston's Big Dig", "denver": "Denver airport", "brooklyn": "Brooklyn Bridge",
             "channel": "Channel Tunnel", "jubilee": "Jubilee Line extension", "greatbelt": "Great Belt bridge"}


class Mega(VoiceoverScene):
    def construct(self):
        card(self, 6, "Megaprojects", "Why do the biggest projects run late and over budget?",
             "Chapter six. Megaprojects. Everything in this film so far gets worse with size: the estimate is more "
             "uncertain, the contract longer, the winner's curse larger.", lit=("change",))
        self.iron()
        self.table_()
        self.rail()
        self.hsr()
        self.why()

    def iron(self):
        M = R["mega"]
        dots = VGroup(*[Circle(radius=0.32, stroke_width=0, fill_color=BAD if i < 9 else GOOD, fill_opacity=0.9) for i in range(10)]
                      ).arrange(RIGHT, buff=0.25).move_to([0, 1.0, 0])
        lab = tx(f"{M['share'] / 10:.0f} out of 10 large projects run over budget", 24, BAD, bold=True).move_to([0, -0.2, 0])
        q = tx("'Over budget, over time, over and over again'", 22, PRICE, bold=True).move_to([0, -1.4, 0])
        src = source("Flyvbjerg, 'What You Should Know about Megaprojects and Why', Project Management Journal, 2014", size=12)
        beat(self,
             "Bent Flyvbjerg, at Oxford, keeps a database of big projects' costs and schedules. <bookmark mark='a'/> His "
             "summary: nine out of ten of them cost more than planned. <bookmark mark='b'/> He calls it the iron law of "
             "megaprojects: over budget, over time, over and over again. And he finds no sign of it getting better in the "
             "seventy years for which comparable data exist.",
             base=[src], steps=[[dots, lab], q])

    def table_(self):
        O = R["mega"]["overruns"]
        items = [(OVER_NAME[k], v, BAD if v >= 200 else PRICE, f"+{v:,.0f}%") for k, v in sorted(O.items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=2000, x0=-0.6, top=2.4, row=0.5, length=6.4, size=15, bar_h=0.3)
        lab = tx("cost overruns, in real terms", 15, GREY_A).to_edge(UP, buff=0.3)
        src = source("Flyvbjerg (2014), Table 2", size=12)
        beat(self,
             "Some famous ones. <bookmark mark='a'/> The Sydney Opera House cost fourteen hundred per cent more than "
             "planned; the Scottish Parliament building sixteen hundred. <bookmark mark='b'/> Boston's Big Dig, the "
             f"tunnel under the city centre, {O['bigdig']:.0f} per cent; Denver's airport {O['denver']:.0f}; the Channel "
             f"Tunnel {O['channel']:.0f}. Even the Brooklyn Bridge, {O['brooklyn']:.0f} per cent. The overruns are not "
             "a modern disease, and they are not only public projects.",
             base=[rows.axis, lab, src], steps=[rows[:4], rows[4:]])

    def rail(self):
        M = R["mega"]
        items = [("rail: cost overrun", M["rail"], BAD, f"+{M['rail']}%"), ("rail: passengers below forecast", M["rail_demand"], BAD, f"-{M['rail_demand']}%"),
                 ("roads: cost overrun", M["road"], PRICE, f"+{M['road']}%")]
        rows = hbars(items, max_value=60, x0=0.4, top=1.2, row=1.0, length=5.6, size=18, bar_h=0.5)
        lab = tx("the average transport project", 16, GREY_A).move_to([0, 2.2, 0])
        src = source("Flyvbjerg (2014), citing Flyvbjerg et al. (2002, 2005)", size=12)
        beat(self,
             f"For transport, the averages. <bookmark mark='a'/> Rail projects cost {M['rail']} per cent more than "
             f"planned on average, <bookmark mark='b'/> and carried {M['rail_demand']} per cent fewer passengers than "
             "forecast. Costs too low and benefits too high: the two errors point the same way. "
             f"<bookmark mark='c'/> Roads, {M['road']} per cent over, with even odds that traffic is wrong by more than a "
             "fifth.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2]])

    def hsr(self):
        M = R["mega"]
        items = [("2008 plan: LA and Anaheim to San Francisco (2008 dollars)", M["hsr08"], GOOD, f"${M['hsr08']:.0f}bn"),
                 ("spent 2006 to 2025", M["spent"], GREY_B, f"${M['spent']:.1f}bn"),
                 (f"2026 plan: Merced to Bakersfield, done {M['mb_done']}", M["mb"], PRICE, f"${M['mb']:.1f}bn"),
                 (f"2026 plan: Phase 1, cheaper route, done {M['p1_done']}", M["phase1"], BAD, f"${M['phase1']:.1f}bn"),
                 ("2026 plan: Phase 1 as first designed", M["full"], BAD, f"${M['full']:.1f}bn")]
        rows = hbars(items, max_value=240, x0=0.2, top=1.9, row=0.75, length=5.2, size=14, bar_h=0.42)
        lab = tx("California's high-speed railway", 17, GREY_A).to_edge(UP, buff=0.5)
        src = source("California High-Speed Rail Authority, Business Plans of November 2008 and 2026", size=12)
        beat(self,
             f"California's high-speed railway is the reference class in action. <bookmark mark='a'/> In 2008, the year "
             f"voters approved {M['bond']:.0f} billion dollars of bonds for it, its plan put the line from Los Angeles and "
             f"Anaheim to San Francisco at about {M['hsr08']} billion dollars. <bookmark mark='b'/> By the end of 2025 the "
             f"authority had spent {M['spent']} billion. <bookmark mark='c'/> Its 2026 plan puts the first stretch, "
             f"Merced to Bakersfield in the Central Valley, at {M['mb']} billion, done in {M['mb_done']}. "
             f"<bookmark mark='d'/> The first phase, by a cheaper route using existing tracks, at {M['phase1']} billion, "
             f"done in {M['p1_done']}, <bookmark mark='e'/> and, as first designed, {M['full']} billion.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3], rows[4]])

    def why(self):
        g = VGroup(tx("Why are the first estimates low?", 22, WHITE, bold=True),
                   tx("optimism bias: planners imagine the project going right", 18, PRICE),
                   tx("strategic misrepresentation: low estimates win approval, as low bids win tenders", 18, BAD),
                   tx("lock-in: 'easy to begin and difficult and expensive to stop'", 18, BAD),
                   quote(["'In the world of civic projects, the first budget is really just a down payment. If people",
                          "knew the real cost from the start, nothing would ever be approved.'"],
                         "Willie Brown, former mayor of San Francisco, 2013, quoted by Flyvbjerg", size=16)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        src = source("Flyvbjerg (2014)", size=12)
        beat(self,
             "Why are the first numbers so low? Flyvbjerg names several reasons. <bookmark mark='a'/> One is optimism "
             "bias: planners picture the project going right. <bookmark mark='b'/> Another is strategic "
             "misrepresentation: a low estimate wins approval, just as a low bid wins a tender. It is the winner's curse "
             "again, with a government as the bidder. <bookmark mark='c'/> And once begun, projects lock in: 'easy to "
             "begin and difficult and expensive to stop'. <bookmark mark='d'/> San Francisco's former mayor, Willie "
             "Brown, put it plainly in 2013: the first budget is really just a down payment, and if people knew the real "
             "cost from the start, nothing would ever be approved. Flyvbjerg's answer is to get projects right before "
             "they start, in what he calls proper front-end management.",
             base=[src], steps=[g[:2], g[2], g[3], g[4]])
