from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

FUND = "#7EC8F5"
ALGO = "#C9A0FF"


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ common owners \ and pricing algorithms", r"What if the rivals share their owners, "
             r"\ or let software set their prices?", "Chapter sixteen. Frontier: common owners and pricing "
             "algorithms.", lit={2018: r"Azar, Schmalz and Tecu", 2020: r"Calvano et al."},
             scale=("firm", "market", "world"), horizon=("a year", "a decade"))
        self.owners()
        self.mhhi()
        self.algorithms()
        self.open()

    def owners(self):
        rows = VGroup(
            label(r"index funds own a few percent of almost every listed firm: \ rivals included", font_size=24),
            label(r"a fund that owns both airlines on a route \ gains little when one wins passengers from the other",
                  font_size=24, color=FUND),
            label(r"Azar, \ Schmalz and Tecu (2018): \ on American air routes, \ fares were higher where common "
                  r"ownership was higher", font_size=23, color=CARTEL),
            label(r"Dennis, \ Gerardi and Schenone (2022): \ the link comes from market shares in the measure, \\ "
                  r"not from ownership", font_size=23, color=GREY_A),
            label(r"the original authors dispute the reply: \ the question is open", font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Azar, Schmalz and Tecu, JF 73(4) (2018); \ Dennis, Gerardi and Schenone, JF 77(5) "
                            r"(2022)", corner=DR, font_size=13)
        with self.voiceover(
            "Two new worries sit at the frontier. The first is about who owns firms. <bookmark mark='a'/> Index "
            "funds now own a few percent of almost every listed company, which means they own rivals too. "
            "<bookmark mark='b'/> A fund that owns both airlines on a route gains little when one wins passengers "
            "from the other, so if owners steer firms at all, they might steer them away from competing. "
            "<bookmark mark='c'/> In 2018 Jose Azar, Martin Schmalz and Isabel Tecu reported that on American air "
            "routes, fares were higher where common ownership was higher. <bookmark mark='d'/> In 2022 Patrick "
            "Dennis, Kristopher Gerardi and Carola Schenone argued that the link came from the market shares built "
            "into the measure, not from ownership. <bookmark mark='e'/> The original authors dispute that reply, "
            "and the question remains open."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def mhhi(self):
        c = load("common")
        xs = np.array(c["xs"])
        ax = plane([0, 0.5], [4800, 10200], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 0.1, 0.28, 0.5], yticks=[5000, 7500, 10000], xlabel=r"share of each airline held by "
                   r"the common funds", ylabel=r"modified HHI", font_size=16, xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"))
        a = ax.ax
        one = path(ax, xs, c["curve_one"], color=FUND, width=3.5)
        many = path(ax, xs, c["curve_many"], color=CARTEL, width=3.5)
        ol_ = label(r"the rest held by one owner", font_size=15, color=FUND).next_to(a.c2p(0.3, 5600), DOWN,
                                                                                    buff=0.1)
        ml_ = label(r"the rest held by a thousand small ones", font_size=15, color=CARTEL).next_to(
            a.c2p(0.12, 9700), DOWN, buff=0.1)
        cs = c["common_share"]
        d1 = Dot(a.c2p(cs, c["mhhi_one"]), radius=0.08, color=FUND)
        d2 = Dot(a.c2p(cs, c["mhhi_many"]), radius=0.08, color=CARTEL)
        side = VGroup(
            label(r"O'Brien and Salop (2000): \\ the modified HHI adds what each firm's \\ owners gain from its rivals' "
                  r"profits", font_size=21),
            label(rf"two airlines, \ half the market each: \\ HHI {c['hhi']:,.0f}".replace(",", "{,}"), font_size=21,
                  color=GREY_A),
            label(rf"{c['funds']} funds own {100 * c['stake']:.0f}\% of each: \ {100 * cs:.0f}\% in common",
                  font_size=21, color=FUND),
            label(rf"rest with one owner: \ MHHI {c['mhhi_one']:,.0f}; \\ rest dispersed: \ {c['mhhi_many']:,.0f}, \ "
                  r"nearly a merger".replace(",", "{,}"), font_size=21, color=CARTEL),
            label(r"the same holdings, \ two answers: \\ it depends on who actually controls the firm", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"O'Brien and Salop, Antitrust Law Journal 67 (2000); \ the numbers: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "How would one measure the effect? <bookmark mark='a'/> Daniel O'Brien and Steven Salop's modified "
            "Herfindahl index adds to the usual index what each firm's controlling owners gain from its rivals' "
            "profits. <bookmark mark='b'/> Take two airlines with half the market each, an ordinary index of five "
            "thousand. <bookmark mark='c'/> Four funds each own seven percent of both, so twenty-eight percent of "
            "each airline is held in common. <bookmark mark='d'/> If the rest of each airline belongs to one large "
            "owner, the modified index rises only to about five thousand one hundred and eighty. If the rest is "
            "spread over a thousand small shareholders, the funds control both firms, and the index reaches nearly "
            "ten thousand, almost a merger. <bookmark mark='e'/> The same holdings give two answers. It depends on "
            "who actually controls the firm, which is exactly what the two sides dispute."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(one), Create(many), FadeIn(ol_), FadeIn(ml_), FadeIn(d1), FadeIn(d2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def algorithms(self):
        rows = VGroup(
            label(r"Calvano, \ Calzolari, \ Denicol\`o and Pastorello (2020): \ two learning algorithms set prices "
                  r"against each other", font_size=23),
            label(r"with no instruction to collude, \ and no way to talk, \ they learned to price above "
                  r"competition", font_size=23, color=ALGO),
            label(r"and to answer a price cut with a short price war: \ chapter 8's punishment, \ discovered",
                  font_size=23, color=CARTEL),
            label(r"Assad, \ Clark, \ Ershov and Xu (2024): \ German petrol stations that adopted pricing software",
                  font_size=23),
            label(r"margins rose where a station had rivals, \ and in two- and three-station markets \ only when "
                  r"all of them adopted", font_size=23, color=PUMP),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        tag = published_tag(r"Calvano et al., AER 110(10) (2020); \ Assad et al., JPE 132(3) (2024)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The second worry is software. <bookmark mark='a'/> In 2020 Emilio Calvano, Giacomo Calzolari, Vincenzo "
            "Denicolo and Sergio Pastorello let two simple learning algorithms set prices against each other, over "
            "and over. <bookmark mark='b'/> They had no instruction to collude and no way to communicate, yet they "
            "learned to price above the competitive level. <bookmark mark='c'/> And they learned to answer a price "
            "cut with a short price war before returning to the high price: chapter eight's punishment, discovered "
            "by trial and error. <bookmark mark='d'/> Is it happening? In 2024 Stephanie Assad, Robert Clark, Daniel "
            "Ershov and Lei Xu studied German petrol stations that adopted pricing software. "
            "<bookmark mark='e'/> Adoption raised margins only for stations that had rivals, and in markets of two "
            "or three stations, only when all of them adopted."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"is it an agreement when two firms use the same pricing software? \ (the RealPage case, \ "
                  r"2024--25)", font_size=23),
            label(r"should funds that own rivals be limited, \ or their votes?", font_size=23, color=FUND),
            label(r"can regulators audit an algorithm's prices \ the way they read a cartel's tapes?", font_size=23,
                  color=ALGO),
            label(r"how do digital platforms compete: \ Part 44; \ how is market power measured: \ Part 43",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        tag = published_tag(r"U.S. v.\ RealPage (M.D.N.C., filed 2024; proposed settlement, November 2025)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Open questions follow. <bookmark mark='a'/> Is it an agreement when rivals hand their prices to the "
            "same software? In 2024 the Justice Department sued RealPage, alleging that its software recommended "
            "rents to competing landlords using their private data; in November 2025 the company agreed to a proposed "
            "settlement that stops it using rivals' current private data. <bookmark mark='b'/> Should funds that "
            "own rivals be limited, or their votes? <bookmark mark='c'/> Can regulators audit an algorithm's prices "
            "the way the F B I once listened to a cartel's tapes? <bookmark mark='d'/> Platforms, and how to measure "
            "market power directly, are Parts forty-four and forty-three."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
