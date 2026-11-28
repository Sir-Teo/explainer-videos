from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Could America carry a fourth network, and where is home internet going?",
             "Chapter ten. Called it? A promise to build a fourth network, made in 2019, and our own call on cable's "
             "losses.", lit=("change",))
        self.dish()
        self.ours()
        self.watch()

    def dish(self):
        q1 = quote(["'we committed to offer 5G broadband service to at least 70% of the U.S. population and to have",
                    "deployed a core network no later than June 14, 2023'"], "DISH Network, Form 10-K for 2019", size=18).move_to([0, 2.0, 0])
        q2 = quote(["'In August 2025, following these transactions, we terminated our deployment of our 5G Network,",
                    "after meeting certain interim and final build-out requirements established by the FCC'"],
                   "EchoStar (formerly DISH), Form 10-K for 2025", size=18).move_to([0, -0.2, 0])
        verdict = tx("right about building it; wrong that a fourth network would last", 20, TOWER, bold=True).move_to([0, -2.2, 0])
        src = source("DISH Network, Form 10-K for 2019; EchoStar, Form 10-K for 2025", size=12)
        beat(self,
             "First, the fourth network. <bookmark mark='a'/> In 2019, as T-Mobile and Sprint merged, the satellite "
             "television company DISH set out to become the new fourth national network, and committed to offer 5G service to at least seventy per cent of Americans by June 2023. "
             "<bookmark mark='b'/> It met its build-out requirements. Then, in August 2025, it stopped building, sold its "
             "best airwaves to AT&T and SpaceX, and began taking the network apart. <bookmark mark='c'/> The promise was "
             "kept on paper; the market did not leave room for a fourth.",
             base=[src], steps=[q1, q2, verdict])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, TOWER, bold=True),
                       tx("Comcast will report fewer domestic broadband customers", 22, WHITE, bold=True),
                       tx("at 31 December 2027 than at 31 December 2026.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, TOWER, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: it lost {C['cm24']} thousand in 2024 and {C['cm25']} thousand in 2025",
                       "for: its 2026 filings report fewer customers and lower average rates",
                       "for: fixed wireless and fibre keep adding homes",
                       "against: new plans and bundles with mobile could slow the loss to nothing"], size=17).move_to([0, -0.7, 0])
        rule = tx("scored on Comcast's Form 10-K for 2027: total domestic broadband customers; unscored if no longer reported", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. <bookmark mark='a'/> We say Comcast, the largest cable company, will end 2027 with fewer home "
             f"broadband customers than it ends 2026 with, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> "
             f"For: it lost {C['cm24']} thousand in 2024 and {C['cm25']} thousand in 2025, its 2026 reports blame fewer "
             "customers and lower rates, and fixed wireless and fibre keep growing. Against: price cuts and bundles with "
             "its mobile service could stop the loss. <bookmark mark='c'/> Comcast's annual report for 2027 will settle it.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch, whichever way the call goes", 22, WHITE, bold=True),
                   tx("churn: whether the three carriers' customers start moving faster", 18, WIRELESS),
                   tx("fixed wireless: whether the mobile networks have room for millions more homes", 18, TOWER),
                   tx("space: whether satellites that talk to ordinary phones become a real network", 18, SAT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things will tell you where this industry is going. <bookmark mark='a'/> Churn: if customers start "
             "moving faster between three look-alike networks, prices fall. <bookmark mark='b'/> Fixed wireless: whether "
             "the mobile networks have the capacity for millions more homes, or fill up. <bookmark mark='c'/> And space: "
             "whether satellites that talk to ordinary phones become a network of their own, or a backup for the ones on "
             "the ground.",
             base=[tag], steps=[g[:2], g[2], g[3]])
