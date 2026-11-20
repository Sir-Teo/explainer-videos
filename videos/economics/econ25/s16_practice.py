from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ reserves and payments", r"Who manages the money, \ and how does it move?",
             "Chapter fourteen. In practice: reserves and payments.", lit={2008: r"interest on reserves",
                                                                         2023: r"FedNow"},
             scale=("firm", "nation"), horizon=("a day",))
        self.reserves()
        self.payments()
        self.who()

    def reserves(self):
        ba = load("base")
        t = np.array(ba["t"])
        ax = plane([1990, 2027], [0, 4500], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 1000, 2000, 3000, 4000],
                   ylabel=r"US banks' reserves, \ billions of dollars", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=16)
        line_ = path(ax, t, ba["reserves"], color=CB, width=3, smooth=False, xr=(1990, 2027))
        side = VGroup(
            label(rf"2007: \ {ba['reserves_2007']:.0f} billion", font_size=21, color=CB),
            label(rf"2014: \ {commas(ba['reserves_2014'])} billion", font_size=21, color=CB),
            label(r"since 2008 the Fed pays \\ interest on reserves, \\ and sets that rate", font_size=20,
                  color=RATE),
            label(r"an ample-reserves system: \\ the desk steers rates, \\ not the quantity", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Federal Reserve Board: \ total reserves of depository institutions, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Chapter ten said the central bank sets the price of reserves. Here is how that works now. "
            f"<bookmark mark='a'/> Before the crisis of 2008, American banks held about {ba['reserves_2007']:.0f} "
            "billion dollars of reserves, kept scarce so that small changes moved the overnight rate. "
            f"<bookmark mark='b'/> By 2014, after the Fed's bond purchases, about {ba['reserves_2014']:,.0f} billion. "
            "<bookmark mark='c'/> Since October 2008 the Fed has paid interest on reserves, and by setting that rate "
            "it sets a floor under what banks will lend for. <bookmark mark='d'/> In 2019 it said it would keep "
            "reserves ample for good. The New York Fed's trading desk now steers rates with administered rates and "
            "repurchase agreements, not by rationing the quantity of money."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=2)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def payments(self):
        rows = VGroup(
            label(r"payments: \ moving deposits between banks, \ settled in reserves", font_size=25, color=E.ACCENT),
            label(r"wholesale: \ Fedwire and its peers settle each payment at once, \ in central bank money",
                  font_size=22, color=CB),
            label(r"retail: \ cards, \ transfers and cheques, \ settled in batches between banks", font_size=22,
                  color=BANK),
            label(r"instant payments for everyone: \ India's UPI \ (2016), \ Brazil's Pix \ (2020), \ the Fed's "
                  r"FedNow \ (2023)", font_size=22, color=MONEY),
            label(r"in Kenya, \ M-Pesa \ (2007) \ made the mobile phone a bank account", font_size=22, color=COCO),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Money's first job is paying. <bookmark mark='a'/> A payment between customers of different banks "
            "moves a deposit from one bank to the other, and the banks settle between themselves in reserves. "
            "<bookmark mark='b'/> Large payments go through systems like Fedwire, which settle each one at once in "
            "central bank money. <bookmark mark='c'/> Everyday payments, cards and transfers, are netted and "
            "settled in batches. <bookmark mark='d'/> In the last decade, instant payment systems have spread: "
            "India's UPI in 2016, Brazil's Pix in 2020, the Federal Reserve's FedNow in 2023. "
            "<bookmark mark='e'/> And in Kenya, M-Pesa, launched in 2007, turned the mobile phone into an account "
            "for millions who had none: Kocherlakota's memory, held by a phone company."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def who(self):
        cards = point_cards([
            (r"central bank desks", r"administered rates, \\ repo, \ the balance sheet", CB),
            (r"bank treasurers", r"liquidity, \ reserves, \\ the cost of deposits", BANK),
            (r"payment systems", r"settlement, \ fraud, \\ instant payments", MONEY),
            (r"finance ministries", r"seigniorage, \ debt, \\ and the temptation to print", PRICE),
        ], width=12.0, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "So: central bank desks steer rates and manage the balance sheet; bank treasurers manage liquidity and "
            "the cost of deposits; payment systems settle, guard against fraud and race to be instant; and finance "
            "ministries collect seigniorage and must resist the temptation of chapter six."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.5),
                      run_time=4)
        self.wait(1.0)
        self.clear_scene()
