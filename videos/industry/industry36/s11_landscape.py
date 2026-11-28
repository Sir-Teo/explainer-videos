from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403

OFFSET = {"Microsoft": UP, "Oracle": UP, "SAP": LEFT, "Salesforce": DOWN, "Adobe": UP, "Intuit": DOWN, "ServiceNow": RIGHT,
          "Palo Alto": UP, "Workday": DOWN, "Autodesk": LEFT, "Synopsys": UP, "Atlassian": DOWN, "Cadence": UP, "Twilio": DOWN,
          "Zoom": UP, "CrowdStrike": DOWN, "Snowflake": RIGHT, "Palantir": RIGHT, "Datadog": UP, "Zscaler": RIGHT, "Veeva": UP,
          "DocuSign": RIGHT, "HubSpot": LEFT, "Okta": LEFT, "MongoDB": LEFT, "Tyler": UP, "Cloudflare": DOWN, "Dynatrace": RIGHT,
          "Box": LEFT, "GitLab": LEFT, "Freshworks": RIGHT}
FLOOR = -0.42
UNLABELLED = {"Box", "Tyler", "Dynatrace", "DocuSign", "HubSpot", "Zscaler", "Freshworks", "Zoom", "Autodesk"}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who sells the software, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: platforms, applications, design tools, developer tools, data "
             "and security, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.profits()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([-0.15, 2.6], [FLOOR - 0.02, 0.5], x_length=10.0, y_length=4.9,
                           xticks=[lx(1), lx(3), lx(10), lx(30), lx(100), lx(300)], yticks=[-0.4, -0.2, 0, 0.2, 0.4],
                           xfmt=lambda v: f"${10 ** v:g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="operating income per dollar of revenue, median of the last five years", size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 3)
            y = max(c["margin"], FLOOR)
            d = Dot(pa.ax.c2p(lx(c["rev"]), y), radius=min(r, 0.3), color=col, fill_opacity=0.85)
            lab = tx(c["name"], 11, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.05)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d) if c["name"] in UNLABELLED else VGroup(d, lab))
        order = ["platform", "apps", "design", "dev", "data", "security"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Software: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        zero = DashedLine(pa.ax.c2p(-0.15, 0), pa.ax.c2p(2.6, 0), color=GREY_B, stroke_width=1.5)
        src = source("Forms 10-K and 20-F via SEC company facts (SAP in euros at the Federal Reserve's annual average rate)", size=12)
        g = {c["name"]: c for c in C}
        pc = lambda n: 100 * g[n]["margin"]  # noqa: E731
        beat(self,
             "The whole industry in one picture. <bookmark mark='a'/> The platforms on top: Microsoft kept a median "
             f"{pc('Microsoft'):.0f} cents of each dollar as operating income over five years, Oracle {pc('Oracle'):.0f}. "
             f"<bookmark mark='b'/> The big application companies, from Adobe at {pc('Adobe'):.0f} and Intuit at "
             f"{pc('Intuit'):.0f} to Salesforce at {pc('Salesforce'):.0f} and Workday near zero. <bookmark mark='c'/> The "
             f"design-tool makers, Cadence {pc('Cadence'):.0f} and Synopsys {pc('Synopsys'):.0f}, whose software chips are "
             "designed with. <bookmark mark='d'/> The developer tools. <bookmark mark='e'/> The data companies, many still losing "
             "money on this measure, partly because of the stock they pay. <bookmark mark='f'/> And security, growing fast at "
             "the break-even line.",
             base=[pa, xl, hd, key, zero, src],
             steps=[groups["platform"], groups["apps"], groups["design"], groups["dev"], groups["data"], groups["security"]])

    def profits(self):
        C = {c["name"]: c for c in R["landscape"]["companies"]}
        names = ["Microsoft", "Oracle", "Adobe", "SAP", "Salesforce", "Intuit", "Cadence", "ServiceNow", "Snowflake"]
        items = []
        for n in names:
            c = C[n]
            v = c["rev"] * c["margin"]
            items.append((n, v, GROUP_COL[c["group"]], f"{'-' if v < 0 else ''}${abs(v):.1f}bn"))
        rows = hbars(items, max_value=150, x0=-0.2, top=2.4, row=0.56, length=6.0, size=15, bar_h=0.33)
        hd = tx("Revenue times its five-year median margin, $bn: a typical year's operating income", 19, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("Forms 10-K and 20-F via SEC company facts; this series' calculation", size=12)
        beat(self,
             "Count it in dollars. <bookmark mark='a'/> On a typical year's margin, Microsoft earns about "
             f"{items[0][1]:.0f} billion dollars of operating income. <bookmark mark='b'/> Oracle, Adobe, SAP and Salesforce "
             f"between them about {sum(i[1] for i in items[1:5]):.0f} billion. <bookmark mark='c'/> Everyone else is far behind. "
             "In this series' reading, software rewards scale more than any other industry: the same code, sold to one more customer, costs "
             "almost nothing.",
             base=[rows.axis, hd, src], steps=[rows[0], VGroup(*rows[1:5]), VGroup(*rows[5:])])

    def map(self):
        cols = [("Platforms", GROUP_COL["platform"], ["Microsoft", "Oracle", "Apple", "Google", "IBM"]),
                ("Applications", GROUP_COL["apps"], ["Salesforce", "SAP", "Adobe", "ServiceNow", "Workday", "Intuit", "Zoho", "Kingdee"]),
                ("Design and engineering", GROUP_COL["design"], ["Autodesk", "Cadence", "Synopsys", "Dassault Systemes"]),
                ("Developers and data", GROUP_COL["data"], ["Snowflake", "Databricks", "Datadog", "MongoDB", "Atlassian", "GitLab"]),
                ("Security", GROUP_COL["security"], ["Palo Alto", "CrowdStrike", "Zscaler", "Cloudflare", "Okta"]),
                ("Owners of many", GA, ["Constellation Software", "private equity's portfolios"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.3, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Apple, Google, IBM, Zoho, Kingdee, Dassault Systemes, Databricks and "
                  "Constellation Software", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The platforms. <bookmark mark='b'/> The applications, from Salesforce and "
             "Germany's SAP to India's Zoho and China's Kingdee. <bookmark mark='c'/> "
             "The design and engineering tools, with France's Dassault. <bookmark mark='d'/> The developer and data tools, "
             "including Databricks, still private. <bookmark mark='e'/> Security. <bookmark mark='f'/> And the buyers of many "
             "small software companies, like Canada's Constellation Software and private equity, which Part 47 takes up.",
             base=[head("The map of the business"), note], steps=list(gr))
