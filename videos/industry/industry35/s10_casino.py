from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Casino(VoiceoverScene):
    def construct(self):
        card(self, 8, "The house and the kingdom", "How do casinos and theme parks turn a visit into a margin?",
             "Chapter eight. The house and the kingdom. Two more businesses that sell a stay: the casino resort, which "
             "earns on the odds, and the theme park, which earns on everything around the ride.", lit=("unit", "moat"))
        self.strip()
        self.roulette()
        self.hold()
        self.macau()
        self.sands()
        self.disney()

    def strip(self):
        Cs = R["casino"]
        items = [("slot machines", Cs["slots"], CASINO, f"{bn(Cs['slots'], 2)}: {Cs['slotpct']:.1f}% of play"),
                 ("table games", Cs["tables"], BRAND, f"{bn(Cs['tables'], 2)}: {Cs['tablepct']:.1f}% of chips"),
                 ("of which baccarat", Cs["bacc"], OWNER, bn(Cs["bacc"], 2))]
        rows = hbars(items, max_value=5.5, x0=-0.4, top=1.3, row=1.0, length=4.4, size=17, bar_h=0.55)
        chips = VGroup(*[draw.chip_stack(0.7, n=k, color=c) for k, c in ((6, CASINO), (4, BRAND), (8, BAD), (3, OWNER))]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([0, -2.2, 0])
        hd = tx(f"what the Las Vegas Strip's casinos won from gamblers in 2025: {bn(Cs['strip'], 2)}", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Nevada Gaming Control Board, gaming revenue report, December 2025 (twelve months)", size=12)
        beat(self,
             f"In 2025 the casinos of the Las Vegas Strip won {Cs['strip']:.1f} billion dollars from gamblers. "
             f"<bookmark mark='a'/> {Cs['slots']:.1f} billion came from slot machines, which kept about {Cs['slotpct']:.0f} "
             f"cents of every dollar put through them. <bookmark mark='b'/> {Cs['tables']:.1f} billion came from the tables, "
             f"which kept {Cs['tablepct']:.0f} per cent of the chips players bought. <bookmark mark='c'/> Baccarat alone, the "
             f"game of the biggest gamblers, brought {Cs['bacc']:.1f} billion.",
             base=[rows.axis, hd, chips, src], steps=list(rows))

    def roulette(self):
        Rl = R["casino"]["roulette"]
        hist, edges = Rl["hist"], Rl["edges"]
        mids = [(edges[i] + edges[i + 1]) / 2 for i in range(len(hist))]
        items = [(f"{mids[i]:+.0f}" if i % 3 == 0 else "", hist[i], GOOD if mids[i] > 0 else (BAD if mids[i] < 0 else GREY_B), "") for i in range(len(hist))]
        cols = vbars(items, base_y=-2.2, height=3.4, width=0.42, gap=0.12, size=11, max_value=max(hist) * 1.1)
        hd = tx(f"{Rl['players']:,} players, ${Rl['buy_in']:.0f} of chips each, ${Rl['bet']:.0f} on red, up to {Rl['spins']} spins", 20, WHITE, bold=True).to_edge(UP, buff=0.5)
        lab = tx("each player's result, $ (single-zero roulette: 18 of 37 pockets win)", 16, GREY_A).to_edge(UP, buff=1.1)
        win = VGroup(*[c for c, x in zip(cols, mids) if x > 0])
        lose = VGroup(*[c for c, x in zip(cols, mids) if x <= 0])
        tag = estimate_tag("the Works: a simulated evening; the odds are exact, the players are invented", size=12)
        beat(self,
             f"Why does the house always win? Watch {Rl['players']:,} invented gamblers. Each buys {Rl['buy_in']:.0f} dollars "
             f"of chips and bets {Rl['bet']:.0f} on red, spin after spin. Eighteen of the wheel's thirty-seven pockets are red, "
             f"so each bet loses, on average, one thirty-seventh: {100 * Rl['edge']:.1f} per cent. <bookmark mark='a'/> After "
             f"the evening, {100 * Rl['win_share']:.0f} per cent of them walk away ahead, some well ahead. <bookmark mark='b'/> "
             "The rest are behind, and some have lost everything they bought. No single player is predictable. The casino, "
             "facing all of them, is.",
             base=[hd, lab, tag], steps=[win, lose])

    def hold(self):
        Rl = R["casino"]["roulette"]
        Cs = R["casino"]
        c = stat_cards([(f"{100 * Rl['edge']:.1f}%", "the house's edge on each bet", BRAND),
                        (f"${Rl['wagered'] / Rl['players']:,.0f}", "bet per player in the evening, from $500 of chips", OWNER),
                        (f"{100 * Rl['hold']:.1f}%", "of the chips bought, kept by the house", CASINO)], y=1.4, size=36, span=12)
        stacks = VGroup(*[draw.chip_stack(0.6, n=n_, color=CASINO if i < 6 else GREY_B) for i, n_ in enumerate((5, 7, 4, 6, 8, 5, 3, 2, 4))]).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([0, -2.4, 0])
        note = tx(f"the Strip's tables in 2025 kept {Cs['tablepct']:.1f}% of the chips bought", 18, GREY_B).move_to([0, -0.4, 0])
        tag = estimate_tag("the Works: the simulated evening", size=12)
        beat(self,
             "Now the trick of the numbers. <bookmark mark='a'/> The edge on each bet is only 2.7 per cent. "
             "<bookmark mark='b'/> But chips go round: a player who buys 500 dollars of them bets, on average, about "
             f"{Rl['wagered'] / Rl['players']:,.0f} dollars in the evening, winning some back and betting it again. "
             f"<bookmark mark='c'/> So the house keeps {100 * Rl['hold']:.0f} per cent of the chips sold. <bookmark mark='d'/> "
             f"That is close to the {Cs['tablepct']:.0f} per cent the Strip's tables actually kept in 2025. A casino does not "
             "need a large edge, only a lot of bets.",
             base=[tag, stacks], steps=list(c) + [note])

    def macau(self):
        M = R["casino"]["macau"]
        items = [(str(y), v, CASINO if y != 2020 else BAD, f"{v:.0f}bn") for y, v in M.items()]
        cols = vbars(items, base_y=-2.2, height=3.6, width=1.6, gap=1.0, size=18, max_value=310)
        hd = tx("Macao's gross gaming revenue, billions of patacas", 21, WHITE, bold=True).to_edge(UP, buff=0.7)
        note = tx(f"special gaming tax: {R['casino']['tax']}% of gross gaming revenue, plus {R['casino']['contrib']}% in contributions", 17, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Macao's Gaming Inspection and Coordination Bureau, as reported in Las Vegas Sands' Forms 10-K for 2019, 2020 and 2025", size=12)
        beat(self,
             "The biggest casino market is not Las Vegas. <bookmark mark='a'/> Macao's casinos won 293 billion patacas in "
             f"2019, about {get('lv35.ggr19.usd'):.1f} billion dollars, four times what the Strip won in 2025. "
             f"<bookmark mark='b'/> In 2020, with travel into Macao all but stopped, {M[2020]:.0f} billion. <bookmark mark='c'/> In 2025, {M[2025]:.0f} billion, "
             f"still {100 * (1 - M[2025] / M[2019]):.0f} per cent below. <bookmark mark='d'/> The government takes 35 per cent "
             "of the casinos' winnings as tax, and another five in contributions: in Macao the house shares its edge.",
             base=[hd, src], steps=[cols[0], cols[1], cols[2], note])

    def sands(self):
        Cs = R["casino"]
        items = [("Marina Bay Sands, Singapore: one resort", Cs["mbs"], BRAND, bn(Cs["mbs"], 2)),
                 ("its six resorts in Macao, with ferries", Cs["macau_ebitda"], CASINO, bn(Cs["macau_ebitda"], 2))]
        rows = hbars(items, max_value=3.3, x0=1.2, top=1.0, row=1.3, length=5.0, size=17, bar_h=0.65)
        hd = tx("Las Vegas Sands: adjusted property EBITDA, 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"Las Vegas Sands sold its Las Vegas resort and expo centre in 2022, for about {bn(Cs['lvsale'], 2)}", 17, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Las Vegas Sands, Form 10-K for 2025", size=12)
        beat(self,
             "Location is everything. <bookmark mark='a'/> Las Vegas Sands' single resort in Singapore, Marina Bay Sands, "
             f"earned {Cs['mbs']:.1f} billion dollars before interest, tax and depreciation in 2025, <bookmark mark='b'/> more "
             f"than all its resorts in Macao together, {Cs['macau_ebitda']:.1f} billion. Singapore awarded only two "
             "concessions for casino resorts, in 2006. <bookmark mark='c'/> And the company named after Las Vegas no longer has a casino there: it sold its "
             f"Las Vegas resort and convention centre in 2022 for about {Cs['lvsale']:.2f} billion dollars.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], note])

    def disney(self):
        Dn = R["casino"]["disney"]
        items = [("theme park admissions", Dn["adm"], PARK, bn(Dn["adm"])), ("hotels, cruises, vacation club", Dn["resorts"], CRUISE, bn(Dn["resorts"])),
                 ("food, drink and merchandise in the parks", Dn["merch"], BRAND, bn(Dn["merch"])),
                 ("licensing, shops, publishing", Dn["lic"], OWNER, bn(Dn["lic"])), ("parks licensing and other", Dn["plic"], FIXC, bn(Dn["plic"]))]
        rows = hbars(items, max_value=14, x0=1.0, top=1.9, row=0.78, length=4.8, size=16, bar_h=0.46)
        hd = tx(f"Disney's Experiences, year to October 2026: revenue {bn(Dn['rev'])}", 20, WHITE, bold=True).to_edge(UP, buff=0.55)
        seg = Dn["op"] + Dn["ent"] + Dn["sports"]
        note = tx(f"operating income {bn(Dn['op'])}: {100 * Dn['op'] / seg:.0f}% of all Disney's segment operating income", 17, GOOD, bold=True).to_edge(DOWN, buff=0.75)
        wheel = draw.ferris_wheel(2.0).move_to([5.3, -1.3, 0])
        src = source("The Walt Disney Company, Form 10-K for the year to 3 October 2026", size=12)
        beat(self,
             "And the kingdom. <bookmark mark='a'/> Disney's parks business sold "
             f"{Dn['adm']:.1f} billion dollars of tickets in its latest year, <bookmark mark='b'/> {Dn['resorts']:.1f} billion "
             "of hotel nights, cruises and holiday-club stays, <bookmark mark='c'/> and "
             f"{Dn['merch']:.1f} billion of food, drink and souvenirs inside the gates: the ticket is about a third of the "
             f"total. <bookmark mark='d'/> Licensing its characters, and its own shops and books, added {Dn['lic']:.1f} billion, "
             f"<bookmark mark='e'/> and other licensing {Dn['plic']:.1f} billion, including royalties from Tokyo Disney Resort, "
             "which a Japanese company, Oriental Land, owns and runs. <bookmark mark='f'/> The segment earned "
             f"{Dn['op']:.1f} billion dollars of operating income, {100 * Dn['op'] / seg:.0f} per cent of all Disney's, and the "
             f"company spent {Dn['capex']:.1f} billion that year on parks, resorts and other property. Like the cruise lines, "
             "and unlike the hotel brands, Disney still builds and owns most of what it runs; in Tokyo it is paid like a "
             "franchisor.",
             base=[rows.axis, hd, wheel, src], steps=list(rows) + [note])
