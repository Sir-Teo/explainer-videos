from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Over(VoiceoverScene):
    def construct(self):
        card(self, 8, "What runs over the pipe", "Who earns from the traffic, and who makes the equipment?",
             "Chapter eight. What runs over the pipe. The carriers sell access; the money in what is accessed goes "
             "elsewhere, and so does some of the money in the equipment.", lit=("dollar", "change"))
        self.ratio()
        self.six()
        self.light()
        self.equipment()
        self.space()
        self.reading()

    def ratio(self):
        H = R["hook"]
        a, b = H["carriers3"], H["over"]
        items = [("2015", a[2015], WIRELESS, f"${a[2015]:.0f}bn"), ("2015 ", b[2015], OVER, f"${b[2015]:.0f}bn"),
                 ("2025", a[2025], WIRELESS, f"${a[2025]:.0f}bn"), ("2025 ", b[2025], OVER, f"${b[2025]:.0f}bn")]
        cols = vbars(items, base_y=-2.0, height=3.8, width=1.3, gap=0.5, size=16, max_value=680)
        key = VGroup(VGroup(Dot(color=WIRELESS), tx("Verizon, AT&T and T-Mobile", 15, WIRELESS)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=OVER), tx("Alphabet, Meta and Netflix", 15, OVER)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.8)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Back to the opening picture, as bars. <bookmark mark='a'/> In 2015 the three carriers took in about three "
             f"times as much as Alphabet, Meta and Netflix together: {a[2015]:.0f} billion against {b[2015]:.0f}. "
             f"<bookmark mark='b'/> In 2025, {a[2025]:.0f} against {b[2025]:.0f}. The services that need the network now "
             "earn almost twice what the networks do.",
             base=[key, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:])])

    def six(self):
        Rv = R["over"]["rev25"]
        items = [(k, v, OVER if k in ("Alphabet", "Meta", "Netflix") else WIRELESS, f"${v:.0f}bn") for k, v in Rv.items()]
        rows = hbars(items, max_value=420, x0=0.2, top=1.9, row=0.72, length=5.8, size=17, bar_h=0.4)
        lab = tx("revenue, 2025", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Company by company. <bookmark mark='a'/> Alphabet alone took in "
             f"{Rv['Alphabet']:.0f} billion dollars in 2025, nearly three times Verizon's {Rv['Verizon']:.0f}. Meta, "
             f"{Rv['Meta']:.0f}. <bookmark mark='b'/> The carriers, between {Rv['T-Mobile']:.0f} and {Rv['Verizon']:.0f} "
             "billion each. Their money comes from what people do over the networks, not from carrying it, and it scales "
             "across every network in the world at once.",
             base=[rows.axis, lab, src], steps=[VGroup(*[r for r, (k, *_ ) in zip(rows, items) if k in ("Alphabet", "Meta", "Netflix")]),
                                                VGroup(*[r for r, (k, *_ ) in zip(rows, items) if k not in ("Alphabet", "Meta", "Netflix")])])

    def light(self):
        N = R["net"]
        v = N["capex"]["Verizon"]
        nc, nr = N["nflx"]
        items = [("Verizon: network spending per dollar of revenue", 100 * v[0] / v[1], WIRELESS, f"{100 * v[0] / v[1]:.1f}c"),
                 ("Netflix: capital spending per dollar of revenue", 100 * nc / nr, OVER, f"{100 * nc / nr:.1f}c")]
        rows = hbars(items, max_value=14, x0=1.2, top=1.0, row=1.2, length=5.0, size=17, bar_h=0.6)
        lab = tx("2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 and SEC company facts", size=12)
        beat(self,
             "Here is the asymmetry in one comparison. <bookmark mark='a'/> Verizon spent about "
             f"{100 * v[0] / v[1]:.0f} cents of every dollar it took in on its network. <bookmark mark='b'/> Netflix, whose "
             f"films travel over those networks, spent about {100 * nc / nr:.1f} cents of each of its "
             f"{nr:.0f} billion dollars on property and equipment. It rents servers and relies on everyone else's pipes; "
             "the pipe owners carry the films and must keep building to do so.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1]])

    def equipment(self):
        E = R["over"]["equip"]
        items = [("Ericsson, SEK bn, 2015", E["ERIC"][2015], EQUIP, f"{E['ERIC'][2015]:.0f}"), ("Ericsson, SEK bn, 2025", E["ERIC"][2025], EQUIP, f"{E['ERIC'][2025]:.0f}"),
                 ("Nokia, EUR bn, 2019", E["NOK"][2019], FOREIGN, f"{E['NOK'][2019]:.1f}"), ("Nokia, EUR bn, 2025", E["NOK"][2025], FOREIGN, f"{E['NOK'][2025]:.1f}")]
        top = max(E["ERIC"][2015], E["ERIC"][2025])
        rows = hbars([(n, v / (top if "SEK" in n else max(E["NOK"][2019], E["NOK"][2025])), c, t) for n, v, c, t in items],
                     max_value=1.1, x0=0.6, top=1.6, row=0.85, length=5.0, size=16, bar_h=0.42)
        lab = tx("revenue of the two Western radio-network makers that file with the SEC, each in its own currency", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Ericsson and Nokia, Forms 20-F via SEC company facts", size=12)
        beat(self,
             "The makers of the radio equipment have not done much better. <bookmark mark='a'/> Ericsson's revenue was "
             f"about {E['ERIC'][2015]:.0f} billion Swedish kronor in 2015 <bookmark mark='b'/> and {E['ERIC'][2025]:.0f} "
             f"billion in 2025. <bookmark mark='c'/> Nokia's, {E['NOK'][2019]:.1f} billion euros in 2019 "
             f"<bookmark mark='d'/> and {E['NOK'][2025]:.1f} in 2025. In this series' reading, carriers buy a new "
             "generation of radios about once a decade, and as little as they can in between.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def space(self):
        N = R["net"]
        ac, ar = N["asts"]
        c = stat_cards([(f"${1e3 * ar:.0f}m", "AST SpaceMobile's revenue, 2025", SAT), (f"${ac:.2f}bn", "its capital spending, 2025", BAD),
                        (f"${N['irdm']:.2f}bn", "Iridium's revenue, 2025", ALL), ("about $20bn", "SpaceX's price for EchoStar's spectrum", OVER)],
                       y=0.4, size=32, span=12.6)
        src = source("AST SpaceMobile, Form 10-K for 2025; AST SpaceMobile and Iridium via SEC company facts; EchoStar, Form 10-K for 2025", size=12)
        beat(self,
             "And a new kind of network is being built over everyone's heads. <bookmark mark='a'/> AST SpaceMobile, which "
             f"is putting up satellites to connect, in its own words, 'standard, unmodified, off-the-shelf mobile phones', took in {1e3 * ar:.0f} million dollars in "
             f"2025 <bookmark mark='b'/> and spent {ac:.2f} billion building. <bookmark mark='c'/> Iridium, the oldest "
             f"satellite-phone network, took in {N['irdm']:.2f} billion. <bookmark mark='d'/> And SpaceX agreed to pay about "
             "twenty billion dollars for spectrum on the ground. Whether space becomes a fourth network, or a fifth, is "
             "the open question of the decade.",
             base=[src], steps=[c[0], c[1], c[2], c[3]])

    def reading(self):
        g = VGroup(tx("Why the pipe captures so little, in this series' reading", 21, WHITE, bold=True),
                   tx("the network is costly and must be rebuilt every generation", 18, BAD),
                   tx("three networks offer nearly the same thing, so they compete on price", 18, WIRELESS),
                   tx("the services that use the network sell to the whole world over everyone's pipes", 18, OVER),
                   tx("and the scarce inputs, spectrum and towers, are owned by governments and landlords", 18, TOWER)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Why? In this series' reading, <bookmark mark='a'/> a network is costly and must be rebuilt every generation. "
             "<bookmark mark='b'/> Three networks sell nearly the same thing, so they compete on price. "
             "<bookmark mark='c'/> The services that use the network sell to the whole world over every carrier's pipes "
             "at once, so no carrier can charge them for being essential. <bookmark mark='d'/> And the scarce inputs, the "
             "airwaves and the tower sites, belong to governments, which auction them, and to landlords, who rent them.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
