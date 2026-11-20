from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Tariffs(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The tariffs of 2018 and 2025", r"Who paid?", "Chapter ten. The tariffs of 2018 and 2025.",
             lit={2019: r"Amiti, \ Redding and Weinstein", 2020: r"Fajgelbaum et al."}, scale=("market", "nation"),
             horizon=("a year",))
        self.history()
        self.paid()

    def history(self):
        T = load("tariffs")
        ax = plane([1929, 2026], [0, 20], center=LEFT * 1.5 + DOWN * 0.35, x_length=9.0, y_length=4.8,
                   xticks=[1930, 1950, 1970, 1990, 2010, 2025], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"America's average tariff, \ duties as \% of goods imports", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        y, r = np.array(T["years"]), np.array(T["rate"])
        old_, new_ = y <= 2017, y >= 2017
        ln = path(ax, y[old_], r[old_], GREY_A, 3.0, smooth=False)
        ln2 = path(ax, y[new_], r[new_], TARIFF, 3.4, smooth=False)
        rate = dict(zip(T["years"], T["rate"]))
        pk = dot(ax, T["peak_y"], T["peak"], WHITE, 0.07)
        d25 = dot(ax, 2025, rate[2025], TARIFF, 0.09)
        side = VGroup(
            label(rf"{T['peak_y']}: \ {T['peak']:.1f}\% \\ after Smoot-Hawley \\ (1930)", font_size=18,
                  color=GREY_A),
            label(r"1947 on: \ the GATT's \\ rounds of cuts", font_size=18, color=GAIN),
            label(rf"2017: \ {T['rate2017']:.1f}\%; \\ 2019: \ {T['rate2019']:.1f}\%", font_size=18, color=TARIFF),
            label(rf"2025: \ {T['rate2025']:.1f}\%, \\ the highest \\ since {T['since']}", font_size=18,
                  color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BEA, \ NIPA customs duties and goods imports, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Here is America's average tariff since 1929: customs duties as a share of the goods it imported. "
            f"<bookmark mark='a'/> After the Smoot-Hawley tariff of 1930 it peaked at {T['peak']:.0f} percent in "
            f"{T['peak_y']}. <bookmark mark='b'/> From 1947, round after round of agreements brought it down, to "
            f"{T['rate2017']:.1f} percent by 2017. <bookmark mark='c'/> In 2018 and 2019 America raised tariffs on "
            "washing machines, solar panels, steel, aluminium and, in several rounds, on most imports from China, "
            f"and its partners retaliated. The average nearly doubled, to {T['rate2019']:.1f} percent. "
            f"<bookmark mark='d'/> In 2025 it jumped to {T['rate2025']:.1f}, the highest since {T['since']}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(pk, scale=1.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ln2), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(d25, scale=1.8), FadeIn(side[3]), Indicate(ln2, color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def paid(self):
        T = load("tariffs")
        cards = point_cards([
            (r"the theory", r"a large country's tariff: \\ foreign sellers cut \\ their prices and \\ bear part of it",
             TARIFF),
            (r"who paid", r"foreign prices \\ did not fall: \\ the tariff passed \\ fully to US buyers", WHITE),
            (r"the bill", rf"buyers lost \${T['buyers_loss'] / 1e9:.0f}bn \\ ({T['buyers_share']:.2f}\% of GDP); \\ "
                          rf"net of revenue and \\ producer gains, \ \${T['net_loss'] / 1e9:.1f}bn", ARCH),
            (r"2025", rf"the average tariff: \\ {T['rate2024']:.1f}\% $\to$ {T['rate2025']:.1f}\%; \\ imports from "
                      rf"China \\ \${T['imp2024']:.0f}bn $\to$ \${T['imp2025']:.0f}bn", CHINA),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a natural experiment in tariffs", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FAJGELBAUM_2020.tag + r"; \ BEA and Census, \ via FRED", corner=DR, font_size=11)
        with self.voiceover(
            "The tariffs of 2018 and 2019 covered more than three hundred billion dollars of imports. Who paid? "
            "Part thirty-five's large-country argument says foreign sellers should cut their prices and bear part "
            "of the tariff. <bookmark mark='b'/> They did not: Mary Amiti, Stephen Redding and David "
            "Weinstein, and Pablo Fajgelbaum and coauthors, found that the prices foreigners charged did not fall, "
            "so the tariff passed in full to American buyers. <bookmark mark='c'/> The buyers of imports lost "
            f"about {T['buyers_loss'] / 1e9:.0f} billion dollars a year; after counting the tariff revenue and "
            f"the gains to protected producers, the net loss was about {T['net_loss'] / 1e9:.1f} billion, "
            f"{T['net_share']:.2f} percent of GDP. <bookmark mark='d'/> In 2025, with the average tariff at "
            f"{T['rate2025']:.1f} percent, America's imports from China fell from {T['imp2024']:.0f} billion dollars "
            f"to {T['imp2025']:.0f} billion. Part sixty-six measures what followed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
