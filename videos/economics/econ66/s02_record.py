from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Record(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What the tariffs did", r"Who paid for the tariffs of 2018 and 2025, \ and what did they "
             r"cost?", "Chapter one. What the tariffs did.", lit={2019: "Amiti, Redding and Weinstein",
                                                                     2020: "Fajgelbaum et al."},
             scale=("nation",), horizon=("a year",))
        self.first_war()
        self.effective()
        self.prices()

    def first_war(self):
        cards = point_cards([
            (r"who paid", r"import prices before the tariff did not fall: \ the whole tariff reached American "
             r"buyers \ (Amiti, \ Redding and Weinstein; \ Fajgelbaum et al.)", PRICE),
            (r"what it cost", r"by the end of 2018, \ \$3.2 billion a month in tariffs paid and \$1.4 billion a "
             r"month of real income lost", TARIFF),
            (r"the net bill", r"\$51 billion a year to buyers of imports; \ after tariff revenue and producers' "
             r"gains, \ \$7.2 billion, \ 0.04\% of GDP \ (Fajgelbaum et al.)", US),
            (r"the factories", r"industries more exposed to the tariffs lost jobs: \ dearer inputs and "
             r"retaliation outweighed the protection \ (Flaaen and Pierce)", ROW),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the first round: \ 2018--19", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Amiti, \ Redding and Weinstein, \ JEP 33(4) (2019); \ Fajgelbaum, \ Goldberg, \ "
                            r"Kennedy and Khandelwal, \ QJE 135(1) (2020); \ Flaaen and Pierce, \ FEDS 2019-086",
                            corner=DL, font_size=12)
        with self.voiceover(
            "In 2018 and 2019 the United States raised tariffs on washing machines, solar panels, steel, aluminium "
            "and then most imports from China, and its partners retaliated. <bookmark mark='a'/> Mary Amiti, "
            "Stephen Redding and David Weinstein, and separately Pablo Fajgelbaum and coauthors, looked at the "
            "prices foreign sellers charged before the tariff. They did not fall. The whole tariff reached American "
            "buyers. <bookmark mark='b'/> By the end of 2018, Amiti and her coauthors estimated, Americans were "
            "paying three point two billion dollars a month in tariffs, and losing another one point four billion "
            "a month of real income to the trade that no longer happened. <bookmark mark='c'/> Fajgelbaum and "
            "coauthors put the loss to buyers of imports at fifty-one billion dollars a year; after counting the "
            "tariff revenue and the gains to protected producers, the net loss was seven point two billion, four "
            "hundredths of one percent of GDP. Small, because most of it was a transfer. <bookmark mark='d'/> And "
            "Aaron Flaaen and Justin Pierce found that manufacturing industries more exposed to the tariffs lost "
            "jobs relative to others: the dearer inputs and the retaliation outweighed the protection."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def effective(self):
        E_ = load("effective")
        t = np.array(E_["t"])
        r = 100 * np.array(E_["rate"])
        ax = plane([2015, 2027], [0, 12.5], center=LEFT * 1.9 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[2015, 2017, 2019, 2021, 2023, 2025, 2027], yticks=[0, 2, 4, 6, 8, 10, 12],
                   ylabel=r"customs duties over imports of goods, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, t, r, TARIFF, 3.2, smooth=False)
        dots_ = VGroup(*[dot(ax, x, y, TARIFF, 0.05) for x, y in zip(t, r)])
        court = vline(ax, 2026 + 1.6 / 12, 0, 12.5, GREY_B)
        clab = label(r"February 2026: \\ the Supreme Court \\ strikes down the \\ emergency tariffs", font_size=13,
                     color=GREY_B).next_to(ax.ax.c2p(2026.15, 12), RIGHT, buff=0.08)
        side = VGroup(
            label(rf"2017: \ {100 * E_['q2017']:.1f}\%", font_size=18, color=GREY_A),
            label(rf"end of 2019: \ {100 * E_['q2019']:.1f}\%", font_size=18, color=GREY_A),
            label(rf"early 2025: \ {100 * E_['q2025_1']:.1f}\%", font_size=18, color=GREY_A),
            label(rf"peak, \ end of 2025: \ {100 * E_['peak']:.1f}\%", font_size=18, color=TARIFF),
            label(rf"third quarter of 2026: \ {100 * E_['last']:.1f}\%", font_size=18, color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax.ax, RIGHT, buff=0.35).shift(DOWN * 0.6)
        if side.get_right()[0] > 6.95:
            side.scale_to_fit_width(6.95 - side.get_left()[0])
        tag = data_tag(rf"BEA via FRED: \ B235RC1Q027SBEA over A255RC1Q027SBEA \ (retrieved {E_['retrieved']})",
                       corner=DL, font_size=12)
        with self.voiceover(
            "The second round was larger. <bookmark mark='a'/> Here is the effective tariff rate: the customs "
            "duties the United States collected each quarter, over its imports of goods. <bookmark mark='b'/> "
            f"About {100 * E_['q2017']:.1f} percent in 2017; {100 * E_['q2019']:.1f} percent at the end of the "
            f"first round. <bookmark mark='c'/> In 2025 it rose from {100 * E_['q2025_1']:.1f} percent to "
            f"{100 * E_['peak']:.1f} percent by the end of the year, the highest since the Second World War. "
            "<bookmark mark='d'/> In February 2026 the Supreme Court ruled, six to three, that the emergency-powers "
            "law used for most of the new tariffs did not allow tariffs at all. Tariffs under other laws remained, "
            f"and by the third quarter of 2026 the rate was {100 * E_['last']:.1f} percent."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(dots_), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(court), FadeIn(clab), FadeIn(side[4]))
        self.clear_scene()

    def prices(self):
        P = load("prices")
        t = np.array(P["t"])
        keep = t < 2026.0
        t = t[keep]
        P = {**P, "goods": list(np.array(P["goods"])[keep]), "imports": list(np.array(P["imports"])[keep])}
        ax = plane([2023, 2026], [97, 103], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[2023, 2024, 2025, 2026], yticks=[97, 99, 101, 103],
                   ylabel=r"index, \ January 2025 = 100", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        g = path(ax, t, P["goods"], TEXT, 3.0, smooth=False)
        im = path(ax, t, P["imports"], ROW, 3.0, smooth=False)
        start = vline(ax, 2025 + 3.5 / 12, 97, 103, GREY_C)
        key = legend_rows([(TEXT, "consumer prices of goods (less food and energy)"),
                           (ROW, "import prices, before the tariff (less food and fuel)")], font_size=15)
        key.next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.5)
        if key.width > 4.2:
            key.scale_to_fit_width(4.2).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.5)
        side = VGroup(
            label(rf"goods prices, \ 2024: \ {100 * P['goods_2024']:+.1f}\%".replace("-", "{-}"), font_size=17,
                  color=TEXT),
            label(rf"goods prices, \ 2025: \ {100 * P['goods_2025']:+.1f}\%", font_size=17, color=TEXT),
            label(rf"import prices, \ 2025: \ {100 * P['imports_2025']:+.1f}\%", font_size=17, color=ROW),
            label(r"retail pass-through by September 2025: \\ about a fifth \ (Cavallo et al.)", font_size=17,
                  color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        tag = published_tag(r"BLS via FRED: \ CUSR0000SACL1E, \ IREXFDFLS; \ Cavallo, \ Llamas and Vazquez, \ NBER "
                            r"WP 34496 (2025)", corner=DL, font_size=12)
        with self.voiceover(
            "Who paid this time? <bookmark mark='a'/> In orange, the prices foreign sellers charged at the border, "
            "before the tariff, excluding food and fuel. They did not fall in 2025: they rose about "
            f"{100 * P['imports_2025']:.0f} percent. Foreign sellers did not absorb the tariff; as in 2018, it was "
            "paid at the American border. <bookmark mark='b'/> In green, the consumer prices of goods other than "
            f"food and energy: down {100 * -P['goods_2024']:.1f} percent in 2024, up {100 * P['goods_2025']:.1f} "
            "percent in 2025. <bookmark mark='c'/> The rise reached shoppers slowly. Alberto Cavallo, Paola Llamas "
            "and Franco Vazquez tracked daily prices in large American retailers: by September 2025 about a fifth "
            "of the tariff had reached the prices of imported goods on the shelves, adding about seven tenths of a "
            "point to the consumer price index. The rest was, for the moment, absorbed by importers and retailers "
            "in their margins."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(start), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(im), FadeIn(key[1]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(g), FadeIn(key[0]), FadeIn(side[:2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
