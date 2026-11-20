from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Tariffs(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The tariffs of 2018 and 2025", r"Who paid?", "Chapter ten. The tariffs of 2018 and 2025.",
             lit={2019: r"Amiti, \ Redding and Weinstein", 2020: r"Fajgelbaum et al."}, scale=("market", "nation"),
             horizon=("a year",))
        self.paid()

    def paid(self):
        T = load("tariffs")
        cards = point_cards([
            (r"2018--19", rf"duties on \$300bn+ of imports; \\ America's average tariff \\ {T['rate2017']:.1f}\% $\to$ "
                          rf"{T['rate2019']:.1f}\%", TARIFF),
            (r"who paid", r"foreign prices \\ did not fall: \\ the tariff passed \\ fully to US buyers", WHITE),
            (r"the bill", rf"buyers lost \${T['buyers_loss'] / 1e9:.0f}bn \\ ({T['buyers_share']:.2f}\% of GDP); \\ "
                          rf"net of revenue and \\ producer gains, \ \${T['net_loss'] / 1e9:.1f}bn", ARCH),
            (r"2025", rf"the average tariff: \\ {T['rate2024']:.1f}\% $\to$ {T['rate2025']:.1f}\%; \\ imports from "
                      rf"China \\ \${T['imp2024']:.0f}bn $\to$ \${T['imp2025']:.0f}bn", CHINA),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a natural experiment in tariffs", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FAJGELBAUM_2020.tag + r"; \ BEA and Census, \ via FRED", corner=DR, font_size=11)
        with self.voiceover(
            "In 2018 and 2019 America raised tariffs on washing machines, solar panels, steel, aluminium and, in "
            "several rounds, on most imports from China, and its partners retaliated. <bookmark mark='a'/> "
            f"America's average duty on goods rose from {T['rate2017']:.1f} percent to {T['rate2019']:.1f}. "
            "<bookmark mark='b'/> Who paid? Part thirty-five's large-country argument says foreign sellers should "
            "cut their prices and bear part of the tariff. They did not: Mary Amiti, Stephen Redding and David "
            "Weinstein, and Pablo Fajgelbaum and coauthors, found that the prices foreigners charged did not fall, "
            "so the tariff passed in full to American buyers. <bookmark mark='c'/> The buyers of imports lost "
            f"about {T['buyers_loss'] / 1e9:.0f} billion dollars a year; after counting the tariff revenue and "
            f"the gains to protected producers, the net loss was about {T['net_loss'] / 1e9:.1f} billion, "
            f"{T['net_share']:.2f} percent of GDP. <bookmark mark='d'/> In 2025 the average tariff jumped from "
            f"{T['rate2024']:.1f} percent to {T['rate2025']:.1f}, and imports from China fell from "
            f"{T['imp2024']:.0f} billion dollars to {T['imp2025']:.0f} billion. Part sixty-six measures what "
            "followed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
