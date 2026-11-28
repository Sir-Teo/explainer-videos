from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Cloud(VoiceoverScene):
    def construct(self):
        card(self, 6, "The subscription and the cloud", "What pays for free delivery, and what paid for the bad years?",
             "Chapter six. The subscription and the cloud: two businesses that are not shops, and that changed what the shop "
             "could afford.", lit=("dollar", "moat"))
        self.subs()
        self.autoship()
        self.cloud()
        self.reading()

    def subs(self):
        S = R["cloud"]["subs"]
        ch = line_chart({"subscription services": (S, SUBS)}, x=(2015, 2025), y=(0, 60), xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                        yticks=[0, 20, 40, 60], yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon's subscription revenue (Prime and digital), $bn a year",
                        width=8.4, height=4.3, center=(-1.4, -0.45), label_end=False)
        m = marker(ch.ax, 2025, S[2025], f"2025: ${S[2025]:.1f}bn", SUBS, side=LEFT)
        van = draw.van(1.3, color=SHOP).move_to([5.0, 1.8, 0])
        src = source("Amazon.com, Forms 10-K for 2017-2025", size=12)
        beat(self,
             "First, the subscription. <bookmark mark='a'/> Prime is a membership that includes fast, free delivery on "
             "tens of millions of items, films and series, live sports and more. Amazon's subscription revenue was "
             f"{S[2015]:.1f} billion dollars in 2015. <bookmark mark='b'/> By 2025, {S[2025]:.1f} billion. In this series' "
             "reading the fee does two jobs: it pays toward the vans, and it changes the shopper. Once the delivery is "
             "already paid for, every extra order feels free, and the member checks Amazon first.",
             base=[ch.frame, van, src], steps=[ch.lines["subscription services"], m])

    def autoship(self):
        C = R["cloud"]
        c = stat_cards([(f"{C['autoship']:.1f}%", "of Chewy's sales came from Autoship customers, fiscal 2025", SUBS),
                        (f"{R['direct']['wayfair_repeat']:.1f}%", "of Wayfair's 2025 orders came from repeat customers", SHOP)], y=0.5, size=40, span=11)
        src = source("Chewy, Form 10-K for fiscal 2025; Wayfair, Form 10-K for 2025", size=12)
        beat(self,
             "Others found their own ways to make buyers come back without being bought again. <bookmark mark='a'/> Chewy, "
             f"which sells pet food online, gets {C['autoship']:.0f} per cent of its sales from customers on Autoship, "
             "deliveries that repeat on a schedule, because the dog eats the same food every month. <bookmark mark='b'/> "
             f"Wayfair, selling furniture, gets {R['direct']['wayfair_repeat']:.0f} per cent of its orders from people who "
             "have bought before. Chapter eight shows why that matters so much.",
             base=[src], steps=[c[0], c[1]])

    def cloud(self):
        C = R["cloud"]
        ch = line_chart({"AWS": (C["aws_op"], CLOUD), "the shops": (C["store_op"], SHOP)}, x=(2015, 2025), y=(-15, 50),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[-10, 0, 10, 20, 30, 40, 50],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon's operating income, $bn a year (the shops: North America and International)",
                        width=8.4, height=4.3, center=(-1.4, -0.45))
        S = C["store_op"]
        m = marker(ch.ax, 2022, S[2022], f"2022: -${abs(S[2022]):.1f}bn", BAD, side=RIGHT)
        m2 = marker(ch.ax, 2022, C["aws_op"][2022], f"AWS: ${C['aws_op'][2022]:.1f}bn", CLOUD, side=UP)
        rack = draw.server_rack(1.6, lit=0.8).move_to([5.4, 1.6, 0])
        src = source("Amazon.com, Forms 10-K for 2017-2025: segment operating income", size=12)
        beat(self,
             "Second, the cloud. <bookmark mark='a'/> AWS rents out computing power, storage and software to other "
             "companies, and its operating income rose from "
             f"{C['aws_op'][2015]:.1f} billion dollars in 2015 to {C['aws_op'][2025]:.1f} billion in 2025. "
             "<bookmark mark='b'/> The shops' earnings were far smaller and far less steady. <bookmark mark='c'/> In 2022 "
             f"the shops lost {abs(S[2022]):.1f} billion dollars, while the cloud "
             f"earned {C['aws_op'][2022]:.1f} billion. Without it, Amazon as a whole would have reported a large operating "
             "loss that year.",
             base=[ch.frame, rack, src], steps=[VGroup(ch.lines["AWS"], ch.labels["AWS"]), VGroup(ch.lines["the shops"], ch.labels["the shops"]),
                                                VGroup(m, m2)])

    def reading(self):
        g = VGroup(tx("Why the shop could take the long view", 22, WHITE, bold=True),
                   tx("the cloud earned steady profits on rented computers", 18, CLOUD),
                   tx("Prime turned delivery into a fee paid in advance", 18, SUBS),
                   tx("ads turned the shop's traffic into nearly pure margin", 18, ADS),
                   tx("so the shop could price low and build the network ahead of demand", 18, SHOP)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading; Part 37 covers the cloud", size=12)
        beat(self,
             "In this series' reading, that is the answer to the letter of 1997. <bookmark mark='a'/> A cloud with steady "
             "profits, <bookmark mark='b'/> a subscription paid in advance, <bookmark mark='c'/> and advertising on the "
             "shop's own pages <bookmark mark='d'/> let the shop price low and build its network before the orders came. "
             "A rival that has only the shop has to make the shop pay on its own. Part 37 looks at the cloud itself.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
