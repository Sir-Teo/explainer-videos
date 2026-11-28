from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.who()
        self.sales()
        self.revenue()
        self.history()
        self.title()

    def who(self):
        H = R["hook"]
        rest = VGroup(*[draw.restaurant(1.8) for _ in range(3)]).arrange(RIGHT, buff=0.5).move_to([0, 1.4, 0])
        c = stat_cards([(f"{H['rest']:,}", "McDonald's restaurants, end of 2025", FR),
                        (f"{H['fr']}%", "run by franchisees, not by McDonald's", OP)], y=-1.1, size=40, span=10)
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "There were "
             f"{H['rest']:,} McDonald's restaurants in the world at the end of 2025. <bookmark mark='a'/> You might think "
             f"McDonald's runs them. <bookmark mark='b'/> It runs about one in twenty. The other {H['fr']} per cent are run by "
             "franchisees: local business owners who bought the right to sell the burgers, hired the crew, and pay "
             "McDonald's every month. So who owns a fast-food restaurant, and who makes the money?",
             base=[rest, src], steps=[c[0], c[1]])

    def sales(self):
        H = R["hook"]
        items = [("sold at franchisees' restaurants", H["frsales"], OP, f"${H['frsales']:.0f}bn"),
                 ("McDonald's own revenue", H["rev"], FR, f"${H['rev']:.1f}bn")]
        rows = hbars(items, max_value=140, x0=-0.4, top=1.0, row=1.4, length=7.0, size=18, bar_h=0.7)
        hd = tx("McDonald's in 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("franchisees' sales are not McDonald's revenue; only what they pay McDonald's is", 16, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Customers spent {H['frsales']:.0f} billion dollars at franchised McDonald's in 2025. "
             f"<bookmark mark='b'/> McDonald's own revenue was {H['rev']:.0f} billion. The franchisees' sales are not "
             "McDonald's revenue at all; what counts is what the franchisees pay it, plus the sales of the few restaurants it "
             "runs itself.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1]])

    def revenue(self):
        H = R["hook"]
        items = [("rent from franchisees", H["rents"], FR, f"${H['rents']:.1f}bn"),
                 ("royalties from franchisees", H["royal"], FR, f"${H['royal']:.1f}bn"),
                 ("sales at its own restaurants", H["cosales"], OP, f"${H['cosales']:.1f}bn")]
        rows = hbars(items, max_value=12, x0=0.0, top=1.4, row=1.0, length=6.2, size=18, bar_h=0.55)
        hd = tx("McDonald's revenue in 2025, by where it came from", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        q = tx(f"operating income: ${H['op']:.1f}bn, {100 * H['op'] / H['rev']:.0f} cents of each dollar of revenue", 19, GOOD, bold=True).move_to([0, -1.9, 0])
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> The largest part of McDonald's revenue is rent: {H['rents']:.1f} billion dollars from "
             f"franchisees in 2025. <bookmark mark='b'/> Royalties, a share of each restaurant's sales, were "
             f"{H['royal']:.1f} billion. <bookmark mark='c'/> Its own restaurants sold {H['cosales']:.1f} billion. "
             f"<bookmark mark='d'/> And its operating income was {H['op']:.1f} billion: {100 * H['op'] / H['rev']:.0f} cents of "
             "every dollar of revenue, a margin you would expect of a software company, not a burger chain. The company "
             "collects more in rent than in royalties.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2], q])

    def history(self):
        Hh = R["hook"]["hist"]
        rev = {y: v[0] for y, v in Hh.items()}
        op = {y: v[1] for y, v in Hh.items()}
        ch = line_chart({"revenue": (rev, FR), "operating income": (op, GOOD)}, x=(2010, 2025), y=(0, 30),
                        xticks=[2010, 2013, 2016, 2019, 2022, 2025], yticks=[0, 10, 20, 30], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="McDonald's, $bn a year", width=8.6, height=4.3, center=(-1.2, -0.45))
        src = source("McDonald's, Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Strangely, McDonald's revenue was larger in 2013, {max(rev.values()):.1f} billion dollars, "
             f"than in 2025, {rev[2025]:.1f} billion. <bookmark mark='b'/> But its operating income rose from about "
             f"{op[2013]:.0f} billion to {op[2025]:.0f} billion. In 2013 it ran {get('md34.co13'):,} of its own restaurants; by "
             f"2025, about {round(get('md34.rest') * (100 - get('md34.fr')) / 100, -2):,.0f}. It handed thousands to franchisees: "
             "it gave up their sales, and kept their rent and royalties.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["revenue"], ch.labels["revenue"]), VGroup(ch.lines["operating income"], ch.labels["operating income"])])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-four: restaurants and franchising. Who actually owns a fast-food "
                            "restaurant, and who is making the money?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
