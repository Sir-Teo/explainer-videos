from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Vertical(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Vertical mergers: \ the bargaining model on trial", r"When a supplier buys a customer, \ "
             r"who pays?", "Chapter eight. Vertical mergers: the bargaining model on trial.",
             lit={2016: r"AT\&T and Time Warner", 2018: r"Judge Leon"}, scale=("firm", "market"),
             horizon=("a year",))
        self.case()
        self.model()
        self.curve()

    def case(self):
        rows = VGroup(
            history_card(2016, r"AT\&T agrees to buy Time Warner", r"\$85.4 billion: \ the owner of DirecTV buys "
                         r"CNN, \ TNT, \ HBO and Warner Bros.", color=DEF, width=11.0, font_size=21),
            history_card(2017, r"the Justice Department sues", r"Time Warner's channels would cost AT\&T's rival "
                         r"distributors more, \ and their customers would pay", color=GOV, width=11.0, font_size=21),
            history_card(2018, r"Judge Richard Leon, \ 12 June", r"the government's bargaining model `lacks both "
                         r"reliability and factual credibility': \ the merger may proceed", color=E.ACCENT,
                         width=11.0, font_size=21),
            history_card(2019, r"the Court of Appeals affirms", r"the theory accepted as economics; \ its "
                         r"prediction rejected on the evidence", color=GREY_A, width=11.0, font_size=21),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.1)
        tag = published_tag(r"United States v. AT\&T, 310 F. Supp. 3d 161 (D.D.C. 2018); \ 916 F.3d 1029 (D.C. "
                            r"Cir. 2019)", corner=DL, font_size=12)
        with self.voiceover(
            "So far the merging firms sold the same thing. A vertical merger joins a supplier and its customer. "
            "<bookmark mark='a'/> In October 2016 AT&T, which owned the satellite distributor DirecTV, agreed to buy "
            "Time Warner, which owned CNN, TNT, HBO and Warner Brothers, for eighty-five billion dollars. <bookmark "
            "mark='b'/> The Justice Department sued in 2017. Its theory: once AT&T owned the channels, it could "
            "charge rival distributors more for them, and their customers would pay. Its expert, Carl Shapiro, "
            "built a bargaining model that predicted bills higher by roughly half a billion dollars a year. "
            "<bookmark mark='c'/> In June 2018 Judge Richard Leon let the merger proceed. The model, he wrote, "
            "lacked both reliability and factual credibility. <bookmark mark='d'/> The appeals court affirmed in "
            "2019, with a careful distinction: the judge had accepted the bargaining theory as economics, and "
            "rejected its prediction on the evidence. The fight was over the inputs."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.clear_scene()

    def model(self):
        V = load("vertical")
        boxes = flow_chain([(r"the sports \\ channel", BIRCH), (r"Harbour Cable \\ (rival, 60\%)", ALDER)],
                           box_w=2.6, box_h=1.1, buff=1.2, font_size=20).move_to(UP * 2.0 + LEFT * 2.6)
        own = RoundedRectangle(width=2.6, height=1.1, corner_radius=0.15, stroke_color=CEDAR, fill_color=CEDAR,
                               fill_opacity=0.15).move_to(DOWN * 0.1 + LEFT * 2.6)
        ownt = label(r"Northern Dish \\ (40\%)", font_size=20, color=CEDAR).move_to(own)
        link = Line(boxes.boxes[0].get_bottom(), own.get_top() + LEFT * 0.0, color=CEDAR, stroke_width=3)
        lk = label(r"one owner \\ after the merger", font_size=15, color=CEDAR).next_to(link, LEFT, buff=0.1)
        rows = VGroup(
            label(r"if talks fail, \ the channel goes dark on Harbour Cable:", font_size=19, color=GREY_A),
            label(rf"{100 * 0.10:.0f}\% of Harbour's subscribers leave, \ {100 * 0.45:.0f}\% of them to Northern "
                  r"Dish \ (margin \$40 a month)", font_size=19, color=WHITE),
            MathTex(r"\Delta\text{fee} = \underbrace{\tfrac12}_{\text{bargaining weight}} \times 0.10 \times 0.45 "
                    rf"\times \$40 = \${V['fee_rise']:.2f}", font_size=30, color=CARTEL),
            label(rf"on a fee of \$2.00: \ +{V['rise_pct']:.0f}\% for the rival", font_size=21, color=CARTEL),
            label(r"but Northern Dish no longer pays a marked-up fee: \ saves \$2.00 a subscriber", font_size=19,
                  color=SAVE),
            label(rf"per subscriber in the market: \ rivals' costs +\${V['rival_cost']:.2f}, \ the saving "
                  rf"\${V['edm']:.2f}", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        if rows.width > 7.6:
            rows.width = 7.6
            rows.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.merger.vertical; \ Nash bargaining over the fee", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is the model on the Island. <bookmark mark='a'/> A sports channel sells to two distributors: "
            "Harbour Cable, with sixty percent of subscribers, and Northern Dish, with forty. The channel and "
            "Northern Dish merge. <bookmark mark='b'/> The fee Harbour pays is bargained. Each side's strength is "
            "what it would get if talks failed and the channel went dark on Harbour's subscribers. Before the "
            "merger, the channel just loses Harbour's fees. After it, some of Harbour's angry subscribers switch "
            "to Northern Dish, and their forty dollars a month now belong to the channel's owner. <bookmark "
            "mark='c'/> Suppose ten percent would leave and forty-five percent of those would go to Northern Dish. "
            "With equal bargaining power, the fee rises by half of that gain: "
            f"{V['fee_rise']:.2f} dollars a subscriber a month, <bookmark mark='d'/> {V['rise_pct']:.0f} percent on "
            "a two-dollar fee. Rivals' costs rise, and some of that reaches their customers' bills. <bookmark "
            "mark='e'/> But there is a saving too. Northern Dish no longer pays a marked-up price for the channel: "
            "the elimination of double marginalization of Part forty-four. <bookmark mark='f'/> Spread over all "
            f"subscribers, rivals' costs rise by {V['rival_cost']:.2f} and the integrated distributor saves "
            f"{V['edm']:.2f}. On these inputs the merger lowers costs on balance."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(boxes.boxes[0]), FadeIn(boxes.boxes[1]), GrowArrow(boxes.arrows[0]), FadeIn(own),
                      FadeIn(ownt))
            self.play(Create(link), FadeIn(lk))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def curve(self):
        V = load("vertical")
        C = V["curve"]
        d, net = 100 * np.array(C["depart"]), np.array(C["net"])
        ax = plane([0, 30], [-1.0, 1.0], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.6, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[-1.0, -0.5, 0, 0.5, 1.0],
                   xlabel=r"subscribers who would leave in a blackout, \ \%",
                   ylabel=r"net cost per subscriber, \ \$ a month", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(30, 0), color=GREY_C, stroke_width=1.2)
        cv = path(ax, d, net, CARTEL, 3.2, smooth=False)
        th = vline(ax, 100 * C["threshold"], -1.0, 1.0, E.ACCENT, 1.8)
        thl = label(rf"{100 * C['threshold']:.1f}\%", font_size=17, color=E.ACCENT).next_to(
            ax.ax.c2p(100 * C["threshold"], 1.0), UP, buff=0.05)
        side = VGroup(
            label(r"above the line, \ the merger raises costs on balance", font_size=20, color=CARTEL),
            label(r"below it, \ the saving wins", font_size=20, color=SAVE),
            label(r"the departure rate in a blackout: \\ the input the trial turned on", font_size=20,
                  color=E.ACCENT),
            label(r"the government estimated it from surveys and models; \\ the defence said going dark would cost "
                  r"too much \\ in fees and advertising, \\ and offered to arbitrate instead", font_size=17,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the same model, \ the departure rate varied", corner=DL, font_size=12)
        with self.voiceover(
            "Now vary the one input nobody can observe directly: how many subscribers would really leave if the "
            "channel went dark. <bookmark mark='a'/> The net effect rises with it. <bookmark mark='b'/> Below "
            f"{say_num(100 * C['threshold'], 1)} percent, the saving wins; above it, the merger raises costs on "
            "balance. <bookmark mark='c'/> In the real trial that number decided a great deal. The government drew "
            "it from surveys and industry models. The defence said a long blackout would cost the channels too "
            "much in lost fees and advertising to be a credible threat, and Turner offered rival distributors "
            "arbitration of fee disputes with no blackout while it ran, which takes the threat off the table. "
            "The judge found the government's inputs unconvincing. "
            "The lesson for an expert: a model is only as persuasive as the evidence behind its most sensitive "
            "input, so find that input first and spend the effort there."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(th), FadeIn(thl), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()
