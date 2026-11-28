from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Selling(VoiceoverScene):
    def construct(self):
        card(self, 6, "Selling it", "If a copy costs nothing, why is selling it so expensive?",
             "Chapter six. Selling it. The largest cost in software is not writing it or running it, but persuading "
             "businesses to buy it.", lit=("dollar", "moat"))
        self.salesforce()
        self.rule40()
        self.arr()
        self.flywheel()

    def salesforce(self):
        S = R["selling"]["crm"]
        sm = {y: 100 * v[0] for y, v in S.items()}
        om = {y: 100 * v[1] for y, v in S.items()}
        ch = line_chart({"sales and marketing, % of revenue": (sm, SALES), "operating margin, %": (om, PROFIT)}, x=(2008, 2025), y=(-10, 60),
                        xticks=[2008, 2012, 2016, 2020, 2025], yticks=[-10, 0, 20, 40, 60], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}%", ylabel="Salesforce, fiscal years to January (named for the year before)",
                        width=8.6, height=4.3, center=(-1.0, -0.45))
        src = source("Salesforce, Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> For fifteen years Salesforce spent between {min(v for y, v in sm.items() if y <= 2022):.0f} and "
             f"{max(sm.values()):.0f} cents of every dollar of revenue on sales and marketing, while its revenue grew from one "
             f"billion dollars to over thirty. <bookmark mark='b'/> Its operating margin hovered near zero, between "
             f"{min(om.values()):.0f} and {max(v for y, v in om.items() if y <= 2022):.0f} per cent. Then, from 2023, it cut "
             f"selling to {sm[2025]:.0f} cents and the margin jumped to {om[2025]:.0f} per cent. In this series' reading, the "
             "profit had been there all along, spent on winning the next customer.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["sales and marketing, % of revenue"], ch.labels["sales and marketing, % of revenue"]),
                                          VGroup(ch.lines["operating margin, %"], ch.labels["operating margin, %"])])

    def rule40(self):
        P = R["selling"]["r40"]
        pa = viz.plot_axes([-5, 60], [-40, 50], x_length=9.6, y_length=5.0, xticks=[0, 20, 40, 60], yticks=[-40, -20, 0, 20, 40],
                           xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"{v:.0f}%", ylabel="free cash flow, % of revenue", size=13).move_to([-0.4, -0.45, 0])
        xl = tx("revenue growth, latest year", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.4)
        line = Line(pa.ax.c2p(-5, 45), pa.ax.c2p(60, -20), color=STOCK, stroke_width=2).set_opacity(0.8)
        ll = tx("growth + margin = 40%", 14, STOCK).move_to(pa.ax.c2p(52, -6))
        dots = VGroup()
        show = {"Oracle", "Salesforce", "Adobe", "Palantir", "Snowflake", "Datadog", "Zoom", "Cloudflare", "CrowdStrike"}
        for n_, v in P.items():
            col = GROUP_COL[v["group"]]
            d = Dot(pa.ax.c2p(100 * v["growth"], 100 * v["fcf"]), radius=0.07, color=col)
            g = VGroup(d)
            if n_ in show:
                g.add(tx(n_, 11, col, bold=True).next_to(d, UP if n_ not in ("Oracle", "Snowflake", "Workday", "HubSpot") else DOWN, buff=0.05))
            dots.add(g)
        hd = tx("growth against free cash flow, latest fiscal year", 21, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Forms 10-K and 20-F via SEC company facts; free cash flow is operating cash flow less capital spending", size=12)
        beat(self,
             "Investors judge the trade between growing and earning with a rule of thumb: growth plus margin should be at "
             "least forty per cent. <bookmark mark='a'/> Here is the industry, growth across, free cash flow up. "
             "<bookmark mark='b'/> Most companies sit near or above the line: slow growers like Zoom and Adobe make up for it in "
             f"cash; fast growers like Snowflake and Cloudflare clear it mostly by growing. Palantir, growing {100 * P['Palantir']['growth']:.0f} per cent "
             f"with {100 * P['Palantir']['fcf']:.0f} per cent cash margins, is far above it; Oracle, spending heavily on data "
             "centres, far below.",
             base=[pa, xl, hd, src], steps=[dots, VGroup(line, ll)])

    def arr(self):
        Sl = R["selling"]
        c = stat_cards([(f"${Sl['cw_arr']:.1f}bn", "CrowdStrike's annual recurring revenue, January 2026, up 24%", SALES),
                        ("$1.0bn", "of it added during the year: net new ARR", PROFIT)], y=1.8, size=40, span=11)
        bars_ = vbars([("January 2025", get("cw36.arr25"), GA, f"${get('cw36.arr25'):.1f}bn"),
                       ("January 2026", Sl["cw_arr"], SALES, f"${Sl['cw_arr']:.1f}bn")], base_y=-2.5, height=2.4, width=1.4, gap=1.2, size=15, max_value=6)
        note = tx("the number the sales force is judged by, every quarter", 18, GREY_B).move_to([0, 0.6, 0])
        src = source("CrowdStrike, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Sales forces are judged by one number above all. <bookmark mark='a'/> CrowdStrike, which sells security "
             f"software, ended its last year with {Sl['cw_arr']:.1f} billion dollars of annual recurring revenue, up 24 per "
             "cent. <bookmark mark='b'/> One billion of it was net new: added during the year, after customers who left. "
             "<bookmark mark='c'/> That net new figure, quarter by quarter, is how investors decide whether the selling is "
             "working, and why the companies report it so prominently.",
             base=[src, bars_], steps=[c[0], c[1], note])

    def flywheel(self):
        Pl = R["platform"]
        q = quote(["'we've engineered a frictionless flywheel with an emphasis on self-service, making it easy for",
                   "customers to try and get value first and foremost and then virally expand within an organization'"],
                  "Atlassian, Form 10-K for fiscal 2026", size=17).move_to([0, 1.8, 0])
        items = [("Atlassian: sales and marketing", 100 * Pl["team"]["sm"] / Pl["team"]["rev"], SALES, f"{100 * Pl['team']['sm'] / Pl['team']['rev']:.0f}%"),
                 ("Atlassian: engineering", 100 * Pl["team"]["rnd"] / Pl["team"]["rev"], ENG, f"{100 * Pl['team']['rnd'] / Pl['team']['rev']:.0f}%"),
                 ("Salesforce: sales and marketing", 100 * Pl["crm"]["sm"] / Pl["crm"]["rev"], SALES, f"{100 * Pl['crm']['sm'] / Pl['crm']['rev']:.0f}%"),
                 ("Salesforce: engineering", 100 * Pl["crm"]["rnd"] / Pl["crm"]["rev"], ENG, f"{100 * Pl['crm']['rnd'] / Pl['crm']['rev']:.0f}%")]
        rows = hbars(items, max_value=55, x0=0.8, top=0.4, row=0.7, length=4.8, size=16, bar_h=0.42)
        src = source("Atlassian, Form 10-K for fiscal 2026; Salesforce, Form 10-K for fiscal 2026; SEC company facts", size=12)
        beat(self,
             "There is another way to sell. <bookmark mark='a'/> Atlassian, the maker of Jira and Confluence, lets teams try "
             "its products and buy them online, and relies on them to spread inside a company. <bookmark mark='b'/> It spends "
             f"{100 * Pl['team']['sm'] / Pl['team']['rev']:.0f} per cent of its revenue on selling and "
             f"{100 * Pl['team']['rnd'] / Pl['team']['rev']:.0f} on engineering. <bookmark mark='c'/> Salesforce, which sells "
             f"mainly through its own sales teams, spends {100 * Pl['crm']['sm'] / Pl['crm']['rev']:.0f} and "
             f"{100 * Pl['crm']['rnd'] / Pl['crm']['rev']:.0f}. The cheaper the product is to try, the less it costs to sell.",
             base=[src], steps=[q, VGroup(rows[0], rows[1]), VGroup(rows[2], rows[3])])
