from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Spectrum(VoiceoverScene):
    def construct(self):
        card(self, 4, "Invisible land", "What is a licence to the airwaves worth?",
             "Chapter four. Invisible land. A spectrum licence is the right to use a band of radio frequencies across a "
             "territory, and it is bought like land.", lit=("moat", "dollar"))
        self.bands()
        self.cband()
        self.echo()
        self.loss()

    def bands(self):
        items = [("low band (600-850 MHz)", "travels far and through walls; carries little", WIRELESS, 0.4),
                 ("mid band (C-Band, 3.7 GHz)", "covers a town from a tower; carries much more", TOWER, 1.0),
                 ("millimetre wave (28-39 GHz)", "a city block at most; carries the most", CABLE, 1.6)]
        g = VGroup()
        for i, (n, d, c, f) in enumerate(items):
            y = 1.8 - 1.5 * i
            wave = FunctionGraph(lambda x, f=f: 0.25 * np.sin(2 * np.pi * f * 2 * x), x_range=[-6.2, -2.6], color=c, stroke_width=3).move_to([-4.4, y, 0])
            g.add(VGroup(wave, tx(n, 19, c, bold=True).move_to([0.6, y + 0.2, 0], aligned_edge=LEFT),
                         tx(d, 16, GREY_A).move_to([0.6, y - 0.25, 0], aligned_edge=LEFT)))
        tag = estimate_tag("this series' reading; the bands are those named in Verizon's Form 10-K for 2025", size=12)
        beat(self,
             "Not all airwaves are alike. In this series' reading, <bookmark mark='a'/> the low frequencies travel far and "
             "through walls, so one tower covers a lot of countryside, but they carry little traffic. "
             "<bookmark mark='b'/> The middle frequencies, like the band called C-Band, cover a town and carry much more: "
             "these were the prize of the 2020s. <bookmark mark='c'/> The highest, millimetre waves, carry the most but "
             "barely cross a street. A carrier needs a layer of each.",
             base=[tag], steps=[g[0], g[1], g[2]])

    def cband(self):
        S = R["spectrum"]
        q = quote(["'the FCC announced that Cellco was the winning bidder with respect to approximately $45.5 billion of licenses'"],
                  "Verizon Communications, Form 10-K for 2020, on FCC Auction 107 (C-Band)", size=18).move_to([0, 2.0, 0])
        items = [("Verizon: C-Band licences won", S["vz"], WIRELESS, f"${S['vz']:.1f}bn"),
                 ("AT&T: 2021 acquisitions, mostly C-Band", S["att"], WIRELESS, f"${S['att']:.1f}bn")]
        rows = hbars(items, max_value=50, x0=0.6, top=0.4, row=1.1, length=5.2, size=17, bar_h=0.55)
        src = source("Verizon, Form 10-K for 2020; AT&T, Form 10-K for 2021", size=12)
        beat(self,
             "The biggest American auction of recent years sold a band known as C-Band, and ended in February 2021. "
             f"<bookmark mark='a'/> Verizon alone won about {S['vz']:.1f} billion dollars of licences. "
             f"<bookmark mark='b'/> AT&T spent {S['att']:.1f} billion on acquisitions in 2021, mostly C-Band licences "
             "and the cost of clearing the band. For a year's worth of their capital spending, they bought the right to "
             "use some frequencies, and still had to build the antennas to use them. The licences sit on the balance "
             "sheet as assets, and earn nothing until the network is built.",
             base=[src], steps=[q, VGroup(rows.axis, rows[0]), rows[1]])

    def echo(self):
        S = R["spectrum"]
        e = VGroup(RoundedRectangle(corner_radius=0.1, width=3.0, height=1.2, stroke_color=SAT, stroke_width=3), tx("EchoStar", 24, SAT, bold=True))
        e[1].move_to(e[0])
        e.move_to([-4.0, 0.2, 0])
        a = VGroup(RoundedRectangle(corner_radius=0.1, width=3.0, height=1.0, stroke_color=WIRELESS, stroke_width=3), tx("AT&T", 22, WIRELESS, bold=True))
        a[1].move_to(a[0])
        a.move_to([3.6, 1.6, 0])
        x = VGroup(RoundedRectangle(corner_radius=0.1, width=3.0, height=1.0, stroke_color=OVER, stroke_width=3), tx("SpaceX", 22, OVER, bold=True))
        x[1].move_to(x[0])
        x.move_to([3.6, -1.2, 0])
        a1 = Arrow(e.get_right(), a.get_left(), buff=0.15, color=WIRELESS, stroke_width=5)
        l1 = tx(f"${S['att_echo']:.2f}bn, closed 28 July 2026", 15, WIRELESS).next_to(a1, UP, buff=0.05)
        a2 = Arrow(e.get_right(), x.get_left(), buff=0.15, color=OVER, stroke_width=5)
        l2 = tx(f"about ${S['spacex']:.0f}bn, up to $11bn in SpaceX shares", 15, OVER).next_to(a2, DOWN, buff=0.05)
        src = source("EchoStar, Form 10-K for 2025; AT&T, Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "Licences can also be sold, and in 2025 the largest owner of unused American spectrum sold most of its "
             "own. <bookmark mark='a'/> EchoStar, which as DISH had set out to build a fourth national network, "
             f"<bookmark mark='b'/> agreed to sell licences to AT&T for {S['att_echo']:.2f} billion dollars in cash, a "
             "sale completed in July 2026, <bookmark mark='c'/> and others to SpaceX for about "
             f"{S['spacex']:.0f} billion, much of it in SpaceX shares.",
             base=[src], steps=[e, VGroup(a1, l1, a), VGroup(a2, l2, x)])

    def loss(self):
        S = R["spectrum"]
        q = quote(["'In August 2025, following these transactions, we terminated our deployment of our 5G Network, after",
                   "meeting certain interim and final build-out requirements established by the FCC, and we began the",
                   "abandonment and decommission process'"], "EchoStar, Form 10-K for 2025", size=17).move_to([0, 1.5, 0])
        c = stat_cards([(f"${S['sats_rev']:.1f}bn", "EchoStar's revenue, 2025", ALL), (f"-${abs(S['sats_op']):.1f}bn", "its operating result, 2025", BAD)],
                       y=-1.3, size=40, span=8)
        src = source("EchoStar, Form 10-K for 2025; SEC company facts", size=12)
        beat(self,
             "And the network it had built? <bookmark mark='a'/> In its own words, it 'terminated' the deployment and "
             "began taking it apart, moving its customers onto AT&T's network. <bookmark mark='b'/> In 2025 it took in "
             f"{S['sats_rev']:.0f} billion dollars <bookmark mark='c'/> and reported an operating loss of "
             f"{abs(S['sats_op']):.0f} billion, after writing down spectrum and a network it would no longer use. The "
             "airwaves were worth more to the networks that already had customers.",
             base=[src], steps=[q, c[0], c[1]])
