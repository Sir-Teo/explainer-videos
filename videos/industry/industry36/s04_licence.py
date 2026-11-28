from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Licence(VoiceoverScene):
    def construct(self):
        card(self, 3, "From licence to subscription", "Why would a company choose to make its revenue fall?",
             "Chapter three. From licence to subscription. Software used to be sold like a book: pay once, own it for ever. "
             "Most of it is now rented. The switch is painful, and the pain has a shape.", lit=("dollar", "change"))
        self.works()
        self.adobe()
        self.year2013()
        self.now()

    def works(self):
        J = R["licence"]["works"]
        xs = list(range(1, len(J["licence"]) + 1))
        lic = {x: v for x, v in zip(xs, J["licence"])}
        sw_ = {x: v for x, v in zip(xs, J["switched"])}
        ch = line_chart({"keeps selling licences": (lic, LIC), "switches to subscriptions in year 4": (sw_, SUB)}, x=(1, 10), y=(0, 1400),
                        xticks=[1, 4, 7, 10], yticks=[0, 400, 800, 1200], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:.0f}",
                        ylabel="revenue, in units of one year's subscription per customer", width=8.4, height=4.3, center=(-1.0, -0.45),
                        nudge={"keeps selling licences": -0.15})
        sw = J["switch"] + 1
        mk = marker(ch.ax, sw, sw_[sw], f"year {sw}: revenue falls {100 * (1 - sw_[sw] / lic[sw]):.0f}%", LOSS, side=DOWN)
        tag = estimate_tag("the Works: a licence costs three years' subscription plus 20% a year for upkeep; a third of owners convert each year", size=12)
        beat(self,
             "First the Works' version. <bookmark mark='a'/> A company sells licences: the customer pays three years' worth "
             "up front, then a fifth of that each year for updates and support. Revenue grows with the number of new "
             "customers. <bookmark mark='b'/> In year four it stops selling licences and rents the software instead, at one "
             f"year's worth a year. <bookmark mark='c'/> Revenue falls by {100 * (1 - sw_[sw] / lic[sw]):.0f} per cent, because "
             "new customers now pay a third as much in their first year. Then it climbs past the old path and keeps going, as "
             "subscribers pile up, year after year. This is the J-curve.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["keeps selling licences"], ch.labels["keeps selling licences"]),
                                          VGroup(ch.lines["switches to subscriptions in year 4"], ch.labels["switches to subscriptions in year 4"]), mk])

    def adobe(self):
        A = R["licence"]["adobe"]
        rev = {y: v[0] for y, v in A.items()}
        op = {y: v[1] for y, v in A.items()}
        ch = line_chart({"revenue": (rev, SUB), "operating income": (op, PROFIT)}, x=(2009, 2025), y=(0, 25),
                        xticks=[2009, 2013, 2017, 2021, 2025], yticks=[0, 5, 10, 15, 20, 25], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Adobe, fiscal years to about December, $bn", width=8.6, height=4.3, center=(-1.0, -0.45))
        mk = marker(ch.ax, 2013, rev[2013], "2013: Creative Cloud", LOSS, side=UP)
        src = source("Adobe, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Now the real one. <bookmark mark='a'/> Adobe, the maker of Photoshop, sold its programs as licences for "
             "decades. Its revenue grew to "
             f"{rev[2012]:.1f} billion dollars in 2012. <bookmark mark='b'/> Then it moved them to a subscription, Creative "
             f"Cloud. In 2013 revenue fell to {rev[2013]:.1f} billion and operating income from {op[2012]:.1f} billion to "
             f"{op[2013]:.1f}. Then the curve turned: revenue {rev[2019]:.0f} billion in 2019 and {rev[2025]:.0f} billion in "
             f"2025, with operating income of {op[2025]:.1f} billion.",
             base=[ch.frame, src], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), mk])

    def year2013(self):
        L = R["licence"]
        c = stat_cards([(f"{L['prod13']}%", "of revenue from licences in 2013, against 81% in 2011", LIC),
                        (f"{L['cc13']:.1f}m", "paid Creative Cloud subscriptions, end of 2013 (0.3m a year before)", SUB),
                        (f"${L['arr13']:.0f}m", "Creative annual recurring revenue (from $155m)", PROFIT)], y=0.6, size=36, span=12)
        q = quote(["'We anticipate that our shift to a subscription model will increase the amount of our recurring",
                   "revenue that is ratably reported'"], "Adobe Systems, Form 10-K for fiscal 2013", size=17).move_to([0, -1.7, 0])
        src = source("Adobe Systems, Form 10-K for fiscal 2013", size=12)
        beat(self,
             "Inside the dip, the numbers that mattered were moving the other way. <bookmark mark='a'/> In 2011, "
             f"81 per cent of Adobe's revenue came from selling licences; by 2013, {L['prod13']} per cent. "
             f"<bookmark mark='b'/> Paid Creative Cloud subscriptions went from 0.3 million to {L['cc13']:.1f} million in a "
             f"year, <bookmark mark='c'/> and the recurring revenue they brought from 155 million dollars to {L['arr13']:.0f} "
             "million. <bookmark mark='d'/> Adobe told its shareholders what it was doing: trading a sale today for revenue "
             "recognized over the life of the subscription.",
             base=[src], steps=list(c) + [q])

    def now(self):
        L = R["licence"]
        parts = [("subscriptions", L["sub25"] / L["rev25"], SUB), ("licences and services", 1 - L["sub25"] / L["rev25"], LIC)]
        bar = viz.bar_split(parts, 1.0, width=11.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n_, 14, GREY_A)).arrange(DOWN, buff=0.05).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n_, v, c) in enumerate(parts)])
        hd = tx(f"Adobe's revenue in fiscal 2025: {bn(L['rev25'])}", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("the customer pays less up front, but pays every year, and the seller sees every year coming", 17, GREY_B).move_to([0, -1.9, 0])
        src = source("Adobe, Form 10-K for fiscal 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Today {100 * parts[0][1]:.0f} per cent of Adobe's revenue is subscriptions. "
             "<bookmark mark='b'/> Why do it? The customer pays less to start, so more of them start. The seller swaps a lumpy "
             "sale that must be made again with each new version for a stream that arrives every year without a new sale, "
             "and can raise the price at renewal. In this series' reading, that stream is worth far more than the boxes it "
             "replaced, which is why almost the whole industry made the same switch.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0], bar[1], labs[1]), note])
