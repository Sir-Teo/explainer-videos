from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Measure(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Corruption measured four ways", r"How do you measure what people hide?",
             "Chapter eight. Corruption measured four ways.",
             lit={2001: r"Fisman", 2004: r"Reinikka and Svensson", 2007: r"Fisman and Miguel"},
             scale=("firm", "nation", "world"), horizon=("a year",))
        self.four()
        self.uganda()
        self.surveys()

    def four(self):
        cards = point_cards([
            (r"physical audits", r"core samples: \\ what was built \\ against what was \\ paid for", AUDIT),
            (r"prices", r"share prices that \\ move with a \\ patron's health", LOBBY),
            (r"behaviour", r"diplomats' unpaid \\ parking tickets, \\ when nothing \\ forces payment", POL),
            (r"surveys", r"what firms and \\ experts say they \\ see or pay", VOTER),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.3)
        head = label(r"four ways to see what is hidden", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CORRUPTION_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Corruption is hidden on purpose, so economists measure it indirectly. <bookmark mark='a'/> First, "
            "physical audits: compare what was built with what was paid for, as Olken's engineers did. <bookmark "
            "mark='b'/> Second, prices: Fisman's share prices, which priced the value of a connection. <bookmark "
            "mark='c'/> Third, behaviour where nothing forces honesty. Until 2002, diplomats at the United Nations "
            "in New York could ignore parking tickets, because of diplomatic immunity. Raymond Fisman and Edward "
            "Miguel found that diplomats from countries with more corruption at home ran up many more unpaid "
            "tickets: norms travel with people. <bookmark mark='d'/> Fourth, surveys of what firms, citizens and "
            "experts say they see or pay. Each has its blind spots; together they agree on more than any one alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def uganda(self):
        T = tables.CORRUPTION_47.data
        chain = flow_chain([(r"the central \\ government", ELITE), (r"district \\ officials", CORRUPT),
                            (r"the schools", POOR), (r"published in \\ the newspapers", AUDIT)],
                           notes=[r"grants for \\ each pupil", r"where most \\ of it stopped",
                                  r"about one-fifth \\ arrived, \ mid-1990s", r"the monthly \\ transfers to \\ "
                                                                               r"each district"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 1.9)
        foot = label(r"a public expenditure tracking survey: \ follow the money, \ school by school", font_size=21,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        grid = VGroup(*[Square(side_length=0.21, stroke_width=0, fill_color=FEW, fill_opacity=0.9)
                        for _ in range(100)]).arrange_in_grid(rows=5, cols=20, buff=0.06).move_to(DOWN * 0.9)
        keep = T["uganda_9195"]
        glab = label(r"each square: \ 1\% of the grant sent", font_size=16, color=GREY_A).next_to(grid, UP, buff=0.15)
        gres = label(rf"{keep} of every 100 arrived, \ on average, \ 1991--95; \ the rest stopped on the way",
                     font_size=18, color=WHITE).next_to(grid, DOWN, buff=0.2)
        tag = published_tag(tables.CORRUPTION_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "A fifth way is to follow the money. <bookmark mark='a'/> In the early 1990s Uganda's central "
            "government sent grants for every primary-school pupil, through district officials. <bookmark "
            "mark='b'/> Ritva Reinikka and Jakob Svensson surveyed schools to see what actually arrived. <bookmark "
            f"mark='c'/> In the mid-1990s, about one-fifth: on average, schools received only {T['uganda_9195']} "
            "percent of the grants between 1991 and 1995. <bookmark mark='d'/> Then the government began "
            "publishing the monthly transfers to each district in the newspapers, so that head teachers and "
            "parents knew what to expect, and the share reaching schools rose sharply. Information worked here "
            "where meetings had not in Indonesia: it told people exactly what to look for."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), LaggedStart(*[FadeIn(q) for q in grid], lag_ratio=0.01), FadeIn(glab),
                      run_time=1.5)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
                if mk == "c":
                    self.play(LaggedStart(*[q.animate.set_fill(LOSS, opacity=0.35) for q in grid[keep:]],
                                          lag_ratio=0.01), FadeIn(gres), run_time=2.0)
        self.clear_scene()

    def surveys(self):
        W = load("wgi")
        ax = plane([2.8, 5.3], [-2.0, 2.5], center=LEFT * 1.9 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[3, 4, 5], yticks=[-2, -1, 0, 1, 2],
                   xlabel=r"GDP per head, \ 2021 dollars at PPP \ (log scale)",
                   ylabel=r"control of corruption \ (World Bank estimate)",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}")
                   if v else "0", font_size=13)
        pts = VGroup(*[dot(ax, x, y, VOTER, 0.045) for x, y in zip(W["x"], W["y"]) if 2.8 <= x <= 5.3])
        fit = seg(ax, 2.9, W["intercept"] + W["slope"] * 2.9, 5.2, W["intercept"] + W["slope"] * 5.2, E.ACCENT, 2.6)
        names = VGroup()
        for c in ("DNK", "SGP", "USA", "CHN", "RUS", "VEN", "NGA", "IND", "RWA", "BWA"):
            if c in W["pick"]:
                p = W["pick"][c]
                names.add(label(p["name"], font_size=12, color=WHITE).next_to(ax.ax.c2p(p["x"], p["y"]), UR,
                                                                             buff=0.03))
        side = VGroup(
            label(rf"{W['n']} countries, \\ latest estimate", font_size=18, color=WHITE),
            label(rf"correlation with \\ log income: \ {W['corr']:.2f}", font_size=18, color=E.ACCENT),
            label(r"which causes which? \\ both, \ and \\ perceptions follow \\ income too", font_size=18, color=HOLD),
            label(r"far above the line: \\ Rwanda, \ Botswana, \\ Denmark", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ Worldwide Governance Indicators \ (GOV\_WGI\_CC.EST) \ and WDI", corner=DL,
                       font_size=12)
        with self.voiceover(
            "The most widely used measure is built from surveys. <bookmark mark='a'/> The World Bank's Worldwide "
            "Governance Indicators combine dozens of surveys of firms, households and experts into one estimate of "
            f"how well each country controls corruption. Here it is for {W['n']} countries, against income. "
            f"<bookmark mark='b'/> The correlation is {W['corr']:.2f}: rich countries are seen as cleaner. "
            "<bookmark mark='c'/> But which causes which? Corruption may keep countries poor, growth may pay for "
            "honest institutions, and, as Olken found, perceptions may simply follow appearances. <bookmark "
            "mark='d'/> The countries far above the line, cleaner than their incomes predict, such as Rwanda and "
            "Botswana, are where economists look for what institutions and reforms can do."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.005), FadeIn(names), FadeIn(side[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
