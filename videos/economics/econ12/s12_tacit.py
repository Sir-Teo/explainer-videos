from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

UP_C = "#F2788F"
DN_C = "#7EC8F5"


class Tacit(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Tacit collusion \ and the law", r"If firms keep prices high without ever agreeing to, \ is "
             r"that a crime?", "Chapter ten. Tacit collusion and the law.", lit={1890: r"the Sherman Act"},
             scale=("firm", "market", "nation"), horizon=("a year", "a decade"))
        self.law()
        self.matching()
        self.airlines()
        self.rockets()

    def law(self):
        rows = VGroup(
            label(r"chapter 8's high price needed no agreement: \ each firm simply expects the others to punish a cut",
                  font_size=23),
            label(r"the Sherman Act (1890) and the EU's Article 101 \ forbid agreements and concerted practices",
                  font_size=23, color=LEADER),
            label(r"parallel prices alone are not enough: \ rivals facing the same costs \ move together anyway",
                  font_size=23, color=GREY_A),
            label(r"Bell Atlantic v.\ Twombly (2007): \ a complaint needs facts suggesting an agreement, \ not "
                  r"just parallel conduct", font_size=23),
            label(r"Wood Pulp (1993): \ parallel pricing proves concertation \ only if nothing else explains it",
                  font_size=23),
            label(r"so the law reaches what firms say to each other, \ not what they expect of each other",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Sherman Act, 15 U.S.C. \S 1; \ TFEU art.\ 101; \ 550 U.S. 544 (2007); \ Ahlstr\"om v.\ "
                            r"Commission (1993)", corner=DR, font_size=12)
        with self.voiceover(
            "The cartel of chapter eight held its price high without anyone agreeing to anything. "
            "<bookmark mark='a'/> Each firm simply expected the others to punish a cut. Economists call this tacit "
            "collusion. <bookmark mark='b'/> The law forbids something narrower. America's Sherman Act of 1890 and "
            "the European Union's Article one hundred and one forbid agreements, and practices concerted between "
            "firms, that restrain competition. <bookmark mark='c'/> Parallel prices alone are not enough, because "
            "rivals facing the same costs move together anyway. <bookmark mark='d'/> In Bell Atlantic against "
            "Twombly, in 2007, the American Supreme Court held that a complaint must allege facts suggesting an "
            "agreement, not just parallel behaviour. <bookmark mark='e'/> And in the Wood Pulp case of 1993, the "
            "European Court of Justice held that parallel pricing proves concertation only if nothing else can "
            "explain it. <bookmark mark='f'/> So the law reaches what firms say to each other, but not what they "
            "merely expect of each other."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def matching(self):
        b = load("boats")
        c = b["c"]
        pm = b["mono_P"]

        def each(p):
            return (p - c) * (100 - p) / 2

        rows = VGroup(
            label(r"some practices make tacit collusion easier, \ with nothing said", font_size=25),
            label(r"``we match any lower price'': \ a promise to customers \ that is also a message to rivals",
                  font_size=24, color=LEADER),
            label(rf"both yards post \${pm:.0f} with a matching promise: \ \${each(pm):,.1f} each".replace(",", "{,}"),
                  font_size=24, color=CARTEL),
            label(rf"cut to \${pm - 1:.0f}? \ the rival matches at once: \ \${each(pm - 1):,.0f} each, \ less"
                  .replace(",", "{,}"), font_size=24, color=GREY_A),
            label(r"undercutting no longer wins anyone: \ Bertrand's war never starts", font_size=25, color=EQ),
            label(r"so do advance announcements of price rises, \ and shared databases of rivals' prices",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Some business practices make tacit collusion easier without a word being said. "
            "<bookmark mark='a'/> Take a promise to match any lower price. It sounds like a gift to customers, but "
            "it is also a message to rivals. <bookmark mark='b'/> Suppose both yards post the monopoly's fifty-five "
            "dollars, each promising to match any lower price. Each earns a thousand and twelve dollars fifty. "
            "<bookmark mark='c'/> If Crusoe cuts to fifty-four, Dara matches at once, the yards split the island "
            "at the lower price, and Crusoe earns a little less. <bookmark mark='d'/> Undercutting no longer wins a "
            "single customer, so Bertrand's war never starts. <bookmark mark='e'/> Announcing price rises in advance, "
            "and sharing databases of each other's prices, can work the same way."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def airlines(self):
        hc = history_card(1992, r"United States v.\ Airline Tariff Publishing Company", r"eight airlines and the fare "
                          r"database they owned: \ fares posted to start weeks ahead, \\ withdrawn or matched before "
                          r"anyone could buy them", color=LEADER, width=11.6, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"the Justice Department: \ the airlines used first and last ticket dates and fare footnotes \\ "
                  r"to negotiate the end of each other's discounts", font_size=23),
            label(r"a conversation held in fares: \ an offer, \ a reply, \ an agreement", font_size=24, color=CARTEL),
            label(r"settled by consent decrees in 1993 and 1994: \ fares may carry no other message", font_size=23,
                  color=GREY_A),
            label(r"what if the conversation is between pricing algorithms? \ chapter 16", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"U.S. v.\ ATPCO, Civ.\ No.\ 92-2854 (D.D.C.); \ Competitive Impact Statement (1994)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Where does signalling end and agreement begin? In December 1992 the Justice Department sued eight "
            "airlines and the Airline Tariff Publishing Company, the fare database they owned. "
            "<bookmark mark='a'/> It alleged that the airlines used the database's first and last ticket dates and "
            "its fare footnotes to negotiate the end of each other's discounts: posting fares that would start only "
            "weeks later, and withdrawing or matching them before anyone could buy one. <bookmark mark='b'/> It was a "
            "conversation held in fares, with offers, replies and agreements. <bookmark mark='c'/> The cases were "
            "settled by consent decrees in 1993 and 1994, which forbade fare codes that carry any other message. "
            "<bookmark mark='d'/> What happens when the conversation is between pricing algorithms is chapter "
            "sixteen's question."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def rockets(self):
        r = load("rockets")
        months = np.arange(len(r["up"]))
        ax = plane([-0.3, 5.3], [0, 1.6], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1, 1.5], xlabel=r"months after a change in crude",
                   ylabel=r"pump price moved, \ per \$1 of crude", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        lu = path(ax, months, r["up"], color=UP_C, width=3.5, smooth=False)
        ld = path(ax, months, r["down"], color=DN_C, width=3.5, smooth=False)
        du = VGroup(*[Dot(a.c2p(m, v), radius=0.06, color=UP_C) for m, v in zip(months, r["up"])])
        dd = VGroup(*[Dot(a.c2p(m, v), radius=0.06, color=DN_C) for m, v in zip(months, r["down"])])
        leg = VGroup(label(r"after a rise", font_size=16, color=UP_C), label(r"after a fall", font_size=16,
                                                                           color=DN_C)).arrange(DOWN, buff=0.08)
        leg.move_to(a.c2p(3.6, 0.45))
        side = VGroup(
            label(r"``rockets and feathers'': \ pump prices said to rise \\ like rockets, \ and fall like feathers",
                  font_size=21),
            label(r"Borenstein, \ Cameron and Gilbert (1997): \\ retail prices respond faster to crude's rises \\ "
                  r"than to its falls", font_size=21, color=LEADER),
            label(rf"the Data Room's monthly prices, \ {r['first'][:4]}--{r['last'][:4]}: \\ first month, \ "
                  rf"{r['up0']:.2f} after a rise, \ {r['down0']:.2f} after a fall \\ (difference "
                  rf"{r['diff0']:.2f}, \ standard error {r['se0']:.2f})", font_size=20, color=PUMP),
            label(r"monthly averages blur what happens within weeks: \\ this data can't settle it either way",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Borenstein, Cameron and Gilbert, QJE 112(1) (1997); \ BLS and EIA via FRED; \ the fit: "
                            r"\ Agora", corner=DR, font_size=12)
        with self.voiceover(
            "One suspected sign of tacit coordination is found at the petrol pump. <bookmark mark='a'/> Drivers say "
            "that prices rise like rockets and fall like feathers. <bookmark mark='b'/> In 1997 Severin Borenstein, "
            "Colin Cameron and Richard Gilbert found that American retail prices did respond faster to rises in "
            "crude oil than to falls, and suggested inventory lags and the market power of some sellers as reasons. "
            "<bookmark mark='c'/> Agora tried the same question on the Data Room's monthly prices since 1986, "
            "measuring the pump price's response to each dollar of crude per gallon. In the first month, the pump "
            f"moves {100 * r['up0']:.0f} cents after a rise, and {100 * r['down0']:.0f} cents after a fall: a "
            f"difference of about {100 * r['diff0']:.0f} cent, with a standard error of {100 * r['se0']:.0f}. "
            "<bookmark mark='d'/> Monthly averages blur what happens within "
            "a few weeks, so this data cannot settle the question either way, which is a lesson about data as much "
            "as about petrol."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lu), FadeIn(du), Create(ld), FadeIn(dd), FadeIn(leg), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
