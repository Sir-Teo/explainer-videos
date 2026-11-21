from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Data(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Data, \ attention and free goods", r"What is a service worth if nobody pays for it?",
             "Chapter twelve. Data, attention and free goods.",
             lit={2017: r"the privacy paradox", 2019: r"Brynjolfsson, Collis and Eggers"}, scale=("person", "nation"),
             horizon=("a year",))
        self.survey()
        self.values()
        self.privacy()

    def survey(self):
        W = load("wta")
        lo, hi = np.log10(100.0), np.log10(1e6)
        ax = plane([lo, hi], [0, 1.05], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.4, y_length=4.4,
                   xticks=[2, 3, 4, 5, 6], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"offer to give up search for a "
                   r"year, \ \$ (log scale)", ylabel=r"share who accept",
                   xfmt=lambda v: {2: "100", 3: "1,000", 4: "10,000", 5: "100,000", 6: "1,000,000"}[int(round(v))]
                   .replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}", font_size=14)
        pts = VGroup(*[dot(ax, np.log10(x), s, RIDER, 0.08) for x, s in zip(W["bin_mid"], W["bin_share"])])
        fit = path(ax, np.log10(W["grid"]), W["fit"], WHITE, 2.6)
        med = np.log10(W["median_hat"])
        ml = VGroup(seg(ax, lo, 0.5, med, 0.5, GAIN, 1.6, dashed=True), seg(ax, med, 0, med, 0.5, GAIN, 1.6,
                                                                             dashed=True))
        side = VGroup(
            label(r"4,000 Island users, \ each offered a random sum".replace(",", "{,}"), font_size=19, color=WHITE),
            label(r"dots: \ the share who take the money and give up search", font_size=19, color=RIDER),
            label(r"a logit in the log of the offer", font_size=19, color=WHITE),
            label(rf"half accept at \${W['median_hat']:,.0f}: \ the median value of free search".replace(",", "{,}"),
                  font_size=20, color=GAIN),
            label(rf"planted: \ \${W['median']:,.0f}".replace(",", "{,}"), font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.platform.wta\_survey; \ valuations planted", corner=DL, font_size=12)
        with self.voiceover(
            "A search engine charges its users nothing, so it adds nothing to their measured spending, and "
            "almost nothing to GDP. What is it worth? Ask what it would take to give it up. <bookmark mark='a'/> "
            "Four thousand Island users are each offered a random sum to go without search for a year, and the "
            "offer is real: accept it and the search is switched off. <bookmark mark='b'/> The share who accept "
            "rises with the offer. <bookmark mark='c'/> Fit a logit in the log of the offer, <bookmark mark='d'/> "
            f"and half accept at {W['median_hat']:,.0f} dollars: the median user values free search at about "
            f"that much a year. <bookmark mark='e'/> The value the Island planted was {W['median']:,.0f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ml), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def values(self):
        items = [("search engines", 17530), ("email", 8414), ("digital maps", 3648)]
        ax = plane([0, 20000], [-0.6, 2.6], center=LEFT * 1.0 + UP * 0.6, x_length=8.0, y_length=3.0,
                   xticks=[0, 5000, 10000, 15000, 20000], yticks=[], xlabel=r"median annual value, \ \$",
                   xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        bs, ls = VGroup(), VGroup()
        for k, (n, v) in enumerate(items):
            y = 2 - k
            p0, p1 = ax.ax.c2p(0, y - 0.3), ax.ax.c2p(v, y + 0.3)
            bs.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=RIDER,
                             fill_opacity=0.85).move_to((p0 + p1) / 2))
            ls.add(label(rf"{n}: \ \${v:,}".replace(",", "{,}"), font_size=18, color=WHITE).next_to(
                bs[-1], RIGHT, buff=0.15))
        foot = VGroup(
            label(r"Facebook: \ a median of about \$48 a month to give it up for a month", font_size=20,
                  color=SELL),
            label(r"none of it in GDP: \ Brynjolfsson and colleagues propose counting it alongside \ (`GDP-B')",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(ax, DOWN, buff=0.7)
        tag = published_tag(r"Brynjolfsson, \ Collis and Eggers, \ PNAS 116(15) (2019)", corner=DL, font_size=12)
        with self.voiceover(
            "Erik Brynjolfsson, Avinash Collis and Felix Eggers asked Americans this question at scale. "
            "<bookmark mark='a'/> The median user would give up search engines for a year only for about "
            "seventeen and a half thousand dollars, email for about eight thousand four hundred, and digital maps "
            "for about three thousand six hundred. <bookmark mark='b'/> To give up Facebook for a month, the "
            "median was about forty-eight dollars. None of this value appears in GDP, which measures what is "
            "paid, so Brynjolfsson and his colleagues propose measuring the welfare from free goods alongside it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bs], lag_ratio=0.3), FadeIn(ls), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def privacy(self):
        cards = point_cards([
            (r"the price is attention and data", r"free to the user, \ paid for by advertisers: \ Part 44's "
             r"two-sided market, \ with the user's data as the input", PLAT),
            (r"the privacy paradox", r"Athey, \ Catalini and Tucker: \ students who said they valued privacy "
             r"still gave away friends' email addresses for a free pizza", SURGE),
            (r"what data is worth", r"to the platform, \ how much better it targets; \ to the user, \ the risk "
             r"of what it reveals; \ the two are rarely measured together", DRIVER),
            (r"rules", r"consent, \ limits on tracking, \ the right to take your data elsewhere: \ each changes "
             r"what the market can price", GREY_A),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"paying with data", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Athey, \ Catalini and Tucker, \ NBER Working Paper 23488 (2017); \ Part 44",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Free is not quite free. <bookmark mark='a'/> The user pays with attention and data, which the "
            "platform sells to advertisers: Part forty-four's two-sided market, with the user's information as an "
            "input. <bookmark mark='b'/> How much do people mind? Susan Athey, Christian Catalini and Catherine "
            "Tucker found that students who said they cared about privacy still handed over their friends' email "
            "addresses for a free pizza: stated preferences and choices part company, as they did in Part sixty's "
            "surveys. <bookmark mark='c'/> What data is worth to the platform is how much better it targets; to "
            "the user, the risk of what it reveals; the two are rarely measured together. <bookmark mark='d'/> "
            "And the rules, consent, limits on tracking, the right to take your data elsewhere, each change what "
            "this market can price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
