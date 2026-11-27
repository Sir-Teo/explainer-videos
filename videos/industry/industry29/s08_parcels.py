from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Parcels(VoiceoverScene):
    def construct(self):
        card(self, 6, "The parcel networks", "How do you deliver twenty million parcels a day?",
             "Chapter six. The parcel networks. UPS and FedEx move tens of millions of packages a day through hubs, and in "
             "2025 and 2026 both reshaped themselves.", lit=("make", "change"))
        self.hub()
        self.scale()
        self.margins()
        self.people()
        self.amazon()

    def hub(self):
        n = 10
        ang = [TAU * k / n + 0.3 for k in range(n)]
        left = np.array([-3.6, -0.2, 0])
        right = np.array([3.6, -0.2, 0])
        pl = [left + 2.2 * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
        pr = [right + 2.2 * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
        direct = VGroup(*[Line(pl[i], pl[j], stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.7)
                          for i in range(n) for j in range(i + 1, n)])
        hub = VGroup(*[Line(p, right, stroke_color=PARCEL, stroke_width=2.5) for p in pr])
        dots = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in pl + pr], Dot(right, radius=0.2, color=PARCEL))
        L = R["parcels"]["lanes"]
        l1 = tx(f"every city to every city: {L[10]['direct']} lanes", 17, GREY_A).next_to(direct, DOWN, buff=0.4)
        l2 = tx(f"through one hub: {L[10]['hub']} lanes", 17, PARCEL, bold=True).next_to(hub, DOWN, buff=0.4)
        tag = estimate_tag("counting lanes in each direction", size=12)
        beat(self,
             "First, the idea behind every parcel network. <bookmark mark='a'/> Ten cities that each send parcels to all "
             f"the others need {L[10]['direct']} lanes, most of them carrying a few boxes in a half-empty truck. "
             f"<bookmark mark='b'/> Send everything through one hub, and you need {L[10]['hub']}, every one of them full. "
             f"With forty cities, it is {L[40]['direct']:,} against {L[40]['hub']}. The parcel's journey is longer, but every "
             "truck and plane in the network is full, which is Run it's lesson again: fill the trip.",
             base=[dots, tag], steps=[VGroup(direct, l1), VGroup(hub, l2)])

    def scale(self):
        P = R["parcels"]
        c = stat_cards([(f"{P['ups_adv'] / 1e3:.1f}m", "UPS parcels a day, 2025", PARCEL), (f"${P['ups_rpp']:.2f}", "UPS revenue a parcel", PARCEL),
                        (f"{P['fdx_adv'] / 1e3:.1f}m", "FedEx parcels a day, fiscal 2026", FUEL), (f"${P['fdx_yield']:.2f}", "FedEx revenue a parcel", FUEL)],
                       y=1.0, size=36, span=12.8)
        boxes = VGroup(*[draw.parcel(0.36) for _ in range(14)]).arrange(RIGHT, buff=0.12).move_to([0, -1.4, 0])
        tag = estimate_tag(f"UPS's US domestic parcels alone: about ${P['ups_day_rev'] / 1e6:.0f}m of revenue a working day (this series' arithmetic)", size=12)
        src = source("Forms 10-K of UPS (2025) and FedEx (fiscal 2026)", size=12)
        beat(self,
             f"<bookmark mark='a'/> UPS delivered about {P['ups_adv'] / 1e6:.1f} million parcels a working day in 2025, "
             f"<bookmark mark='b'/> at {P['ups_rpp']:.2f} dollars each. <bookmark mark='c'/> FedEx, {P['fdx_adv'] / 1e6:.1f} "
             f"million a day in its year to May 2026, <bookmark mark='d'/> at {P['fdx_yield']:.2f}. In America alone, UPS's "
             f"domestic parcels brought in about {P['ups_day_rev'] / 1e6:.0f} million dollars every working day.",
             base=[boxes, tag, src], steps=[c[0], c[1], c[2], c[3]])

    def margins(self):
        P = R["parcels"]["margins"]
        ch = line_chart({"UPS": (P["UPS"], PARCEL), "FedEx": (P["FedEx"], FUEL)}, x=(2015, 2026), y=(0, 16),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 4, 8, 12, 16], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="operating profit per dollar of revenue (FedEx's years end in May)", width=9.0, height=4.4,
                        center=(-1.2, -0.45))
        src = source("Forms 10-K via SEC company facts", size=12)
        u, f = P["UPS"], P["FedEx"]
        fb = max(f, key=f.get)
        beat(self,
             f"<bookmark mark='a'/> UPS kept {u[2021]:.0f} cents of operating profit per dollar in the parcel boom of 2021, "
             f"and {u[2025]:.0f} in 2025. <bookmark mark='b'/> FedEx kept at most {f[fb]:.0f} cents, in {fb}, and "
             f"{f[2026]:.0f} in its latest year. Between a railway's forty cents and a trucker's three: networks with hubs and buildings, "
             "but with a driver at every door.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["UPS"], ch.labels["UPS"]), VGroup(ch.lines["FedEx"], ch.labels["FedEx"])])

    def people(self):
        P = R["parcels"]
        c = stat_cards([(f"{P['hourly']:,.0f}", "hourly employees at UPS", PARCEL), ("75,000", "managers", ALL),
                        (f"{get('ups29.union'):.0f}%", "of its US employees in unions", SKY)], y=0.6, size=40, span=12)
        vans = VGroup(*[draw.van(1.1, color=PARCEL) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, -1.8, 0])
        src = source("United Parcel Service, Form 10-K for 2025", size=12)
        beat(self,
             "Why the margin is thinner than a railway's: people. <bookmark mark='a'/> UPS employs about "
             f"{P['hourly']:,.0f} hourly workers, <bookmark mark='b'/> and about seventy-five thousand managers. "
             f"<bookmark mark='c'/> Nearly {get('ups29.union'):.0f} per cent of its American employees are in unions, mostly "
             "those who handle and carry the parcels. One crew moves a whole train; a parcel network needs a driver for "
             "every route, every day, and a sorter for every shift in every hub.",
             base=[vans, src], steps=[c[0], c[1], c[2]])

    def amazon(self):
        P = R["parcels"]
        g = VGroup(tx("UPS, 2025", 22, PARCEL, bold=True),
                   tx(f"Amazon: {P['amazon']:.1f}% of revenue, to be cut by half by June 2026 from 2024's volume", 18, WHITE),
                   tx(f"{P['buildings']:.0f} buildings closed; {P['positions']:,.0f} operational positions cut", 18, BAD),
                   tx("revenue per parcel up 6.6%, volume down 7%", 18, GOOD),
                   tx("FedEx, 1 June 2026: FedEx Freight spun off to shareholders", 22, FUEL, bold=True)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        src = source("United Parcel Service, Form 10-K for 2025; FedEx, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Then both changed shape. <bookmark mark='a'/> Amazon was UPS's largest customer, "
             f"{P['amazon']:.1f} per cent of its revenue in 2025, and UPS chose to carry less of it: a planned cut of half by "
             f"June 2026. <bookmark mark='b'/> It closed {P['buildings']:.0f} buildings in 2025 and cut about "
             f"{P['positions']:,.0f} operational positions. <bookmark mark='c'/> Volume fell seven per cent and revenue per "
             "parcel rose six and a half: fewer, better-paying parcels. <bookmark mark='d'/> And on 1 June 2026 FedEx gave "
             "its shareholders its part-load trucking business, FedEx Freight, as a separate company.",
             base=[src], steps=[g[:2], g[2], g[3], g[4]])
