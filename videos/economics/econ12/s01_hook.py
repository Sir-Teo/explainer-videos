from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

PRICE = "#F2C14E"


def lysine_plot(center=LEFT * 2.4 + DOWN * 0.35, x_length=7.6, y_length=4.6):
    """The lysine prices Connor's text states, the months between left blank; ADM's cost as a band."""
    L = load("lysine")
    ax = plane([1990, 1995.6], [0, 1.4], center=center, x_length=x_length, y_length=y_length,
               xticks=[1990, 1991, 1992, 1993, 1994, 1995], yticks=[0, 0.4, 0.8, 1.2], ylabel=r"\$ a pound",
               font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}")
    a = ax.ax
    lo, hi = L["cost"]
    cost = Polygon(a.c2p(1990, lo), a.c2p(1995.6, lo), a.c2p(1995.6, hi), a.c2p(1990, hi), stroke_width=0,
                   fill_color=HOLD, fill_opacity=0.35)
    cl = label(r"ADM's cost: \ 65 to 70 cents", font_size=15, color=HOLD).next_to(a.c2p(1990.15, lo), DOWN,
                                                                             buff=0.1, aligned_edge=LEFT)
    pts = VGroup(*[Dot(a.c2p(x, y), radius=0.08, color=PRICE) for x, y in L["points"]])
    spans = VGroup()
    for x0, x1, y0, y1 in [*L["spans"], L["after"]]:
        if abs(y1 - y0) < 1e-9:
            spans.add(Line(a.c2p(x0, y0), a.c2p(x1, y0), color=PRICE, stroke_width=6))
        else:
            spans.add(Polygon(a.c2p(x0, y0), a.c2p(x1, y0), a.c2p(x1, y1), a.c2p(x0, y1), stroke_width=0,
                              fill_color=PRICE, fill_opacity=0.9))
    marks = VGroup()
    for x, t, h in ((L["production"], r"ADM's plant opens", 1.36), (L["meeting"], r"Mexico City", 1.22),
                    (L["mole"][0], r"the informant", 1.36), (L["raid"], r"the raid", 1.36)):
        marks.add(VGroup(DashedLine(a.c2p(x, 0), a.c2p(x, h - 0.06), color=GREY_B, stroke_width=1.5),
                         label(t, font_size=14, color=GREY_A).move_to(a.c2p(x, h))))
    return ax, cost, cl, pts, spans, marks


class Hook(VoiceoverScene):
    def construct(self):
        self.plant()
        self.tapes()
        self.slogan()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def plant(self):
        L = load("lysine")
        ax, cost, cl, pts, spans, marks = lysine_plot()
        side = VGroup(
            label(r"lysine: \ an amino acid \\ added to animal feed", font_size=21),
            label(r"1989: \ ADM commits \$150 million \\ to the world's largest lysine plant, \\ in Decatur, "
                  r"Illinois", font_size=21, color=CRUSOE),
            label(r"1991: \ the plant opens, \ and a price war: \\ \$1.30 a pound in 1990, \\ 64 cents by July 1992",
                  font_size=21, color=PRICE),
            label(r"below ADM's own cost: \\ everyone is losing money", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Connor, Choices 13(3) (1998): \ prices as stated in the text", corner=DR, font_size=13)
        with self.voiceover(
            "Lysine is an amino acid. Farmers add it to the feed of pigs and chickens to help them grow. "
            "<bookmark mark='a'/> In 1989 the American agribusiness Archer Daniels Midland, A D M, "
            "committed a hundred and fifty million dollars to build the world's largest lysine plant, in Decatur, "
            "Illinois. <bookmark mark='b'/> When it opened, in 1991, a price war broke out with the Japanese and "
            "Korean firms that had supplied the market. A pound of lysine had sold for a dollar thirty in 1990. By "
            "July 1992 it sold for sixty-four cents. <bookmark mark='c'/> That was below what it cost A D M to make "
            "it, about sixty-five to seventy cents a pound, and the older Asian plants were losing even more."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1:]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(cost), FadeIn(cl), FadeIn(side[3]))
        del L
        self.wait(0.5)
        self.clear_scene()

    def tapes(self):
        L = load("lysine")
        ax, cost, cl, pts, spans, marks = lysine_plot()
        side = VGroup(
            label(r"June 1992, \ Mexico City: \\ the first meeting of a \\ ``lysine association''", font_size=21,
                  color=CARTEL),
            label(r"November 1992: \ Mark Whitacre, \\ head of ADM's lysine division, \\ becomes an FBI informant",
                  font_size=21, color=LEADER),
            label(r"prices climb: \ 98 cents, \ then \\ \$1.08 to \$1.13, \ then about \$1.20", font_size=21,
                  color=PRICE),
            label(r"June 1995: \ more than seventy FBI agents \\ raid ADM's headquarters", font_size=21,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Connor, Choices 13(3) (1998)", corner=DR, font_size=13)
        with self.voiceover(
            "In April 1992 two A D M executives flew to Japan and proposed to their rivals an amino acids trade "
            "association. <bookmark mark='a'/> In June, in Mexico City, the lysine association met for the first "
            "time: to raise prices, and to divide the world's output among its members. <bookmark mark='b'/> In "
            "November, the head of A D M's lysine division, Mark Whitacre, began working for the F B I. For nearly "
            "three years he recorded hundreds of tapes, and the F B I secretly filmed the association's meetings. "
            "<bookmark mark='c'/> Prices climbed: ninety-eight cents a pound by the end of 1992, a steady dollar "
            "eight to a dollar thirteen through most of 1994, then about a dollar twenty. "
            "<bookmark mark='d'/> At the end of June 1995 more than seventy F B I agents raided A D M's "
            "headquarters, and interviewed its officers in their homes that night."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(cost), FadeIn(cl), FadeIn(pts), FadeIn(marks[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in spans], lag_ratio=0.4), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(marks[3]), FadeIn(side[3]))
        del L
        self.clear_scene()

    def slogan(self):
        L = load("lysine")
        q = quote_card(r"Our competitors are our friends. \ Our customers are the enemy.", r"a corporate slogan, \ as "
                       r"ADM's president described it to a rival on a tape played at the trial", width=11.0,
                       font_size=32, color=CARTEL).to_edge(UP, buff=0.6)
        lo, hi = L["overcharge_pct"]
        rows = VGroup(
            label(rf"1996: \ ADM pleads guilty, \ fined \$100 million, \ \${L['fine']} million of it for lysine: "
                  r"\ then a record", font_size=23),
            label(rf"Connor's estimate: \ the cartel raised American lysine prices \\ {lo} to {hi} percent above "
                  r"the competitive price", font_size=23, color=PRICE),
            label(r"three ADM executives went to prison, \ the informant among them: \ he had also embezzled "
                  r"\$9 million", font_size=23, color=GREY_A),
            label(r"why did the price war happen? \ why did the cartel work? \ and why do most of them not?",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(q, DOWN, buff=0.55)
        tag = published_tag(r"Connor, Choices 13(3) (1998); \ U.S. Department of Justice (1996, 2005)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "On one tape played at the trial, A D M's president told an executive of its largest rival about a "
            "company slogan: our competitors are our friends; our customers are the enemy. "
            "<bookmark mark='a'/> In 1996 A D M pleaded guilty and was fined a hundred million dollars, seventy "
            "million of it for lysine and the rest for a second cartel, in citric acid: then the largest criminal "
            "antitrust fine ever. <bookmark mark='b'/> The economist John "
            "Connor estimated that the cartel had raised American lysine prices by twelve to twenty-eight percent "
            "above what competition would have set. <bookmark mark='c'/> Three A D M executives went to prison, "
            "Whitacre among them: while informing, he had also embezzled about nine million dollars from the "
            "company. "
            "<bookmark mark='d'/> Why did the price war happen? Why did the cartel work? And why do so many cartels "
            "fail?"
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"airlines", r"a route flown \\ by two or three", LEADER),
            (r"phones", r"three networks \\ in most countries", CRUSOE),
            (r"chips", r"a handful of foundries \\ and designers", DARA),
            (r"cloud", r"three providers \\ hold most of it", ENTRANT),
            (r"groceries", r"a few chains \\ in each town", COMPETE),
            (r"fuel", r"stations that can see \\ each other's signs", PUMP),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"most markets have a few sellers, \ not one or many", font_size=32, color=E.ACCENT
                     ).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Lysine is unusual only in being caught on film. Most markets are neither a monopoly nor a crowd of "
            "price takers. <bookmark mark='a'/> An airline route is flown by two or three carriers. Most countries "
            "have three mobile networks. A handful of firms make the most advanced chips, and three providers hold "
            "most of the cloud. A town has a few supermarket chains, and its petrol stations can read each other's "
            "price signs from across the road. <bookmark mark='b'/> In all of them, each firm's best price depends "
            "on what the few others do: the games of Part eleven, played for markets."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"do a few firms behave like a monopoly, \ like competitors, \ or in between?", font_size=29,
                  color=CRUSOE),
            label(r"how do firms keep rivals out, \ and when do they agree not to compete?", font_size=29,
                  color=CARTEL),
            label(r"and what can the law see, \ and what should it do?", font_size=29, color=LEADER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part ten had one seller; Part nine, so many that none mattered. This part asks the question in between: "
            "how do a handful of firms compete, and when do they stop? <bookmark mark='a'/> Do a few firms behave "
            "like a monopoly, like perfect competitors, or somewhere between? <bookmark mark='b'/> How do they keep "
            "rivals out, and when do they agree not to compete at all? <bookmark mark='c'/> And what can the law "
            "see, and what should it do?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = yards(1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 12 \ $\cdot$ \ Competition among the Few", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twelve: competition among the few."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act III \ $\cdot$ \ Markets", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"play a price war; \ Cournot's quantities, \ Bertrand's prices, \ and the paradox between them",
            r"capacity, \ difference and location: \ Hotelling's line, \ Salop's circle, \ Dixit and Stiglitz",
            r"commitment: \ Stackelberg's leader, \ and the capacity that keeps a rival out",
            r"collusion: \ when a cartel holds, \ price wars nobody started, \ lysine, \ and leniency",
            r"concentration, \ mergers, \ contestable markets; \ the overcharge dial; \ common owners and algorithms",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part closes Act Three, on markets. <bookmark mark='a'/> You'll fight a price war, and we'll use it "
            "to meet Cournot's competition in quantities, Bertrand's in prices, and the paradox between them. "
            "<bookmark mark='b'/> How capacity, product differences and location resolve it: Hotelling's line, "
            "Salop's circle, and the model of monopolistic competition that trade and macroeconomics borrow. "
            "<bookmark mark='c'/> Commitment: the leader who moves first, and the capacity that keeps a rival out. "
            "<bookmark mark='d'/> Collusion: when a cartel can hold, price wars that nobody started, the lysine "
            "cartel's prices, and the leniency programmes that break cartels. <bookmark mark='e'/> Then "
            "concentration, mergers and contestable markets; a dial for how much cartels overcharge; and the new "
            "worries, common owners and pricing algorithms."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
