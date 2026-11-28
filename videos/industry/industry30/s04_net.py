from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Net(VoiceoverScene):
    def construct(self):
        card(self, 3, "The network", "What does it take to carry a phone call, and what does it cost?",
             "Chapter three. The network. A phone reaches a tower over the air, the tower reaches the network over a cable, "
             "and the network reaches everything else. Every part of it costs money before it carries a byte.", lit=("make",))
        self.diagram()
        self.dollar()
        self.capex()
        self.people()
        self.giants()

    def diagram(self):
        ph = draw.phone(0.9, screen=WIRELESS).move_to([-5.6, -0.6, 0])
        tw = draw.cell_tower(2.4).move_to([-3.0, 0.0, 0])
        waves = VGroup(*[Arc(radius=r, start_angle=-0.5, angle=1.0, stroke_color=WIRELESS, stroke_width=3).move_arc_center_to(
            tw.get_top() + DOWN * 0.3) for r in (0.4, 0.7, 1.0)]).rotate(PI, about_point=tw.get_top() + DOWN * 0.3)
        fiber = Line([-2.5, -1.2, 0], [0.6, -1.2, 0], stroke_color=TOWER, stroke_width=6)
        fl = tx("backhaul: fibre to the network", 14, TOWER).next_to(fiber, DOWN, buff=0.12)
        core = draw.server_rack(1.6).move_to([1.6, -0.4, 0])
        cl = tx("the core: switching, billing", 14, GREY_A).next_to(core, UP, buff=0.12)
        net = VGroup(draw.server_rack(1.0), draw.server_rack(1.0), draw.server_rack(1.0)).arrange(RIGHT, buff=0.15).move_to([5.0, -0.4, 0])
        inet = tx("the internet: everyone else's servers", 14, OVER).next_to(net, DOWN, buff=0.12)
        link = Line([2.3, -0.4, 0], [4.0, -0.4, 0], stroke_color=OVER, stroke_width=5)
        tags = VGroup(tx("radio: spectrum", 14, WIRELESS).next_to(waves, LEFT, buff=0.15), tx("the tower: a rented site", 14, GREY_A).next_to(tw, RIGHT, buff=0.2).shift(UP * 0.8))
        tag = estimate_tag("a simplified picture of a mobile network", size=12)
        beat(self,
             "Here is the path of a phone call or a video. <bookmark mark='a'/> The phone talks to an antenna on a tower "
             "over a band of radio spectrum. <bookmark mark='b'/> The tower is joined to the network by fibre, the "
             "backhaul. <bookmark mark='c'/> The core of the network switches the traffic, bills it and passes it on "
             "<bookmark mark='d'/> to the internet, where the services you actually want live. The phone company owns or "
             "rents everything up to that last step, and earns nothing from what happens after it.",
             base=[tag], steps=[VGroup(ph, tw, waves, tags), VGroup(fiber, fl), VGroup(core, cl), VGroup(link, net, inet)])

    def dollar(self):
        rev = R["net"]["vz_rev"]
        parts = [("services and network", get("vz30.costsvc") / rev, WIRELESS), ("phones", get("vz30.equipcost") / rev, CABLE),
                 ("selling and overheads", get("vz30.sga") / rev, ALL), ("wear on the network", get("vz30.da") / rev, BAD),
                 ("operating profit", 1 - (get("vz30.costsvc") + get("vz30.equipcost") + get("vz30.sga") + get("vz30.da")) / rev, GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}c", 21, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"Verizon, 2025: where a dollar of its ${rev:.0f}bn of revenue went", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Verizon Communications, Form 10-K for 2025: consolidated operating expenses", size=12)
        beat(self,
             f"Follow a dollar of Verizon's {rev:.0f} billion. <bookmark mark='a'/> About {100 * parts[0][1]:.0f} cents ran "
             "the services and the network: power, sites, backhaul, the rent on towers. <bookmark mark='b'/> "
             f"{100 * parts[1][1]:.0f} cents bought the phones it sold. <bookmark mark='c'/> {100 * parts[2][1]:.0f} went "
             f"on selling, shops and overheads, <bookmark mark='d'/> {100 * parts[3][1]:.0f} on the wear of the network, "
             f"<bookmark mark='e'/> and {100 * parts[4][1]:.0f} cents was left as operating profit, before interest on the "
             "debt that paid for the airwaves.",
             base=[hd, src], steps=[VGroup(bar[i], labs[i]) for i in range(5)])

    def capex(self):
        C = R["net"]["capex"]
        items = [(k, 100 * C[k][0] / C[k][1], WIRELESS if k in ("Verizon", "AT&T", "T-Mobile") else CABLE,
                  f"{100 * C[k][0] / C[k][1]:.0f}% (${C[k][0]:.1f}bn)") for k in ("Verizon", "AT&T", "T-Mobile", "Charter", "Comcast")]
        rows = hbars(items, max_value=25, x0=0.0, top=1.8, row=0.8, length=5.6, size=17, bar_h=0.42)
        lab = tx("capital spending per dollar of revenue, 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 and SEC company facts (Verizon's capital expenditures include capitalized software)", size=12)
        v = C["Verizon"]
        beat(self,
             "Building and renewing all that costs a fixed slice of every dollar. <bookmark mark='a'/> Verizon spent "
             f"{v[0]:.1f} billion dollars on its networks in 2025, about {100 * v[0] / v[1]:.0f} cents of each dollar of "
             f"revenue; AT&T {100 * C['AT&T'][0] / C['AT&T'][1]:.0f}; T-Mobile {100 * C['T-Mobile'][0] / C['T-Mobile'][1]:.0f}. "
             f"<bookmark mark='b'/> Charter, rebuilding its cable network, {100 * C['Charter'][0] / C['Charter'][1]:.0f}. A new "
             "generation of mobile technology has arrived roughly every decade, and the spending never really stops.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:])])

    def people(self):
        c = stat_cards([(f"{get('vz30.emp'):,.0f}", "Verizon's full-time equivalent staff, end of 2025", WIRELESS),
                        (f"{get('vz30.union'):.0f}%", "of them represented by two unions", ALL),
                        (f"{R['traffic']['jobs'][max(R['traffic']['jobs'])]:,.0f}k", "Americans in telecoms jobs, 2026", CABLE)],
                       y=0.6, size=38, span=12.4)
        vans = VGroup(*[draw.van(1.1, color="#E8EAED") for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([0, -1.7, 0])
        src = source("Verizon Communications, Form 10-K for 2025; BLS via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> Verizon employed about {get('vz30.emp'):,.0f} people at the end of 2025, "
             f"<bookmark mark='b'/> about {get('vz30.union'):.0f} per cent of them represented by two unions. "
             "<bookmark mark='c'/> The whole industry employs about "
             f"{R['traffic']['jobs'][max(R['traffic']['jobs'])]:,.0f} thousand Americans, as the intermission shows, far "
             "fewer than a generation ago.",
             base=[vans, src], steps=[c[0], c[1], c[2]])

    def giants(self):
        N = R["net"]
        C = N["capex"]
        items = [("Verizon, AT&T and T-Mobile together", N["three"], WIRELESS, f"${N['three']:.1f}bn"),
                 ("Alphabet", C["Alphabet"][0], OVER, f"${C['Alphabet'][0]:.1f}bn"),
                 ("Meta", C["Meta"][0], OVER, f"${C['Meta'][0]:.1f}bn")]
        rows = hbars(items, max_value=100, x0=0.4, top=1.4, row=1.0, length=5.6, size=17, bar_h=0.5)
        lab = tx("capital spending, 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 and SEC company facts", size=12)
        beat(self,
             "And here is a sign of where the money went. <bookmark mark='a'/> The three wireless carriers together spent "
             f"about {N['three']:.0f} billion dollars on their networks in 2025. <bookmark mark='b'/> Alphabet alone spent "
             f"{C['Alphabet'][0]:.0f} billion, <bookmark mark='c'/> and Meta {C['Meta'][0]:.0f}. The "
             "companies that run over the pipes now out-build the companies that own them.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2]])
