from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.cars()
        self.tonnage()
        self.jobs()
        self.ecom()

    def cars(self):
        T = R["traffic"]
        ch = line_chart({"carloads": (T["carloads"], RAIL), "containers and trailers": (T["intermodal"], SKY)},
                        x=(2000, 2027), y=(400, 1600), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[400, 800, 1200, 1600], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}k",
                        ylabel="American rail traffic, thousands a month (seasonally adjusted)", width=9.0, height=4.4,
                        center=(-1.0, -0.45))
        a, b = T["car_a"], T["int_a"]
        hd = tx("Intermission: freight in four pictures", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Bureau of Transportation Statistics, rail freight carloads and intermodal traffic, via FRED", size=12)
        beat(self,
             "An intermission, and four pictures of American freight. <bookmark mark='a'/> First, the railways' traffic. "
             f"Carloads, the coal, grain, chemicals and cars that fill a wagon each, fell from about {a[2006] / 1e3:,.0f} "
             f"thousand a month in 2006 to {a[2025] / 1e3:,.0f} thousand in 2025. <bookmark mark='b'/> Containers and "
             f"trailers on trains grew from {b[2000] / 1e3:,.0f} thousand a month in 2000 to {b[2025] / 1e3:,.0f} thousand. "
             "The railway is turning from a carrier of coal into a carrier of boxes.",
             base=[hd, ch.frame, src], steps=[VGroup(ch.lines["carloads"], ch.labels["carloads"]),
                                              VGroup(ch.lines["containers and trailers"], ch.labels["containers and trailers"])])

    def tonnage(self):
        T = R["traffic"]
        ch = line_chart({"truck tonnage": (T["tonnage"], TRUCK)}, x=(2000, 2027), y=(60, 130),
                        xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[60, 80, 100, 120], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="truck tonnage index, 2015 = 100 (seasonally adjusted)",
                        width=9.2, height=4.4, center=(-0.6, -0.45), label_end=False)
        last = max(T["tonnage"])
        m = marker(ch.ax, last, T["tonnage"][last], f"2026: {T['tonnage'][last]:.0f}", TRUCK, side=DOWN)
        src = source("American Trucking Associations' truck tonnage index, via the BTS and FRED", size=12)
        beat(self,
             "Second, the trucks. <bookmark mark='a'/> The tonnage carried by American trucks rose by more than half from "
             "2000 to 2019, fell in the recession of 2009 and the pandemic, <bookmark mark='b'/> and has moved "
             "sideways since: lots of trucks, and not much more freight for them.",
             base=[ch.frame, src], steps=[ch.lines["truck tonnage"], m])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"truck transportation": (J["truck"], TRUCK), "couriers and messengers": (J["couriers"], PARCEL),
                         "rail transportation": (J["rail"], RAIL)}, x=(2000, 2027), y=(0, 1700),
                        xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 500, 1000, 1500], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:,.0f}k", ylabel="Americans employed, thousands (seasonally adjusted)",
                        width=8.8, height=4.4, center=(-1.2, -0.45))
        last = {k: v[max(v)] for k, v in J.items()}
        first = {k: v[min(v)] for k, v in J.items()}
        src = source("BLS, all employees by industry, via FRED", size=12)
        beat(self,
             "Third, the people. <bookmark mark='a'/> Trucking firms employ about "
             f"{last['truck'] / 1e3:.1f} million Americans. <bookmark mark='b'/> Couriers and messengers, the parcel "
             f"companies and their contractors, went from {first['couriers']:,.0f} thousand in 2000 to {last['couriers']:,.0f} "
             f"thousand. <bookmark mark='c'/> The railways employ {last['rail']:,.0f} thousand, against "
             f"{first['rail']:,.0f} thousand in 2000. More boxes and fewer coal trains, carried by fewer people: the "
             "railway's version of productivity.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["truck transportation"], ch.labels["truck transportation"]),
                                          VGroup(ch.lines["couriers and messengers"], ch.labels["couriers and messengers"]),
                                          VGroup(ch.lines["rail transportation"], ch.labels["rail transportation"])])

    def ecom(self):
        E = R["traffic"]["ecom"]
        ch = line_chart({"online retail sales": (E, PARCEL)}, x=(2000, 2027), y=(0, 350), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0, 100, 200, 300], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="American e-commerce retail sales, $bn a quarter (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        last = max(E)
        m1 = marker(ch.ax, 2000.0, E[min(E)], f"1999: ${E[min(E)]:.0f}bn", ALL, side=UP)
        m2 = marker(ch.ax, last, E[last], f"2026: ${E[last]:.0f}bn", PARCEL, side=LEFT)
        src = source("Census Bureau, quarterly e-commerce retail sales, via FRED", size=12)
        beat(self,
             "And fourth, why the parcels multiplied. <bookmark mark='a'/> Americans bought about "
             f"{E[min(E)]:.0f} billion dollars of goods online in the last quarter of 1999. <bookmark mark='b'/> By 2026 it "
             f"was about {E[last]:.0f} billion a quarter, and almost every order ends in a parcel at a door.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["online retail sales"], m1), m2])
