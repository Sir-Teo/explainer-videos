from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.lipitor()
        self.today()
        self.title()

    def lipitor(self):
        H = R["hook"]
        lip = H["lipitor"]
        items = [(str(y), v / 1e3, BRAND if y < 2012 else GENERIC, f"${v / 1e3:.1f}bn") for y, v in sorted(lip.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.4, gap=1.0, x0=-1.2)
        pills = VGroup(*[draw.tablet(0.22).move_to([-5.8 + 0.5 * (i % 5), 1.8 - 0.5 * (i // 5), 0]) for i in range(20)])
        note = tx("November 2011: Lipitor loses its US exclusivity", 18, PRICE, bold=True).move_to([1.6, 2.6, 0])
        fall = tx(f"{100 * H['lip_fall']:.0f}% in one year", 22, BAD, bold=True).next_to(bars_[2], RIGHT, buff=0.4)
        src = source("Pfizer Inc., Form 10-K 2012 (Exhibit 13, Financial Review): Lipitor revenues", size=12)
        beat(self,
             "In 2010 Pfizer sold ten point seven billion dollars of one cholesterol pill, Lipitor. <bookmark mark='a'/> "
             f"In 2011 it sold {lip[2011] / 1e3:.1f} billion. <bookmark mark='b'/> That November, Lipitor's exclusivity in "
             "America ran out, and from May 2012 several generic makers sold the same molecule. <bookmark mark='c'/> In "
             f"2012 Pfizer's Lipitor sales were {lip[2012] / 1e3:.1f} billion: {-100 * H['lip_fall']:.0f} per cent gone in "
             "a year. Nothing about the pill had changed: the same molecule, made the same way, treating the same "
             "patients. Only the law had changed, and with it the price.",
             base=[pills, src], steps=[VGroup(bars_[0], bars_[1]), note, [bars_[2], fall]])

    def today(self):
        H = R["hook"]
        t = H["tirz"]
        c = stat_cards([(f"${t[2025]:.1f}bn", f"Lilly's tirzepatide (Mounjaro and Zepbound), 2025: {H['lly_share']}% of its revenue", LAB),
                        (f"{H['key_share']}%", f"of Merck's 2025 sales from one drug, Keytruda, whose US patent ends in {H['key_us']}", BRAND)],
                       y=0.6, size=44, span=12)
        caps = VGroup(*[draw.capsule(0.7, LAB if i % 2 else BRAND).move_to([-4.0 + 1.0 * i, -1.9, 0]) for i in range(9)])
        src = source("Eli Lilly and Company and Merck & Co., Forms 10-K 2025", size=12)
        beat(self,
             "The same pattern runs the industry today. <bookmark mark='a'/> Eli Lilly's tirzepatide, sold as Mounjaro "
             f"for diabetes and Zepbound for obesity, brought in {t[2025]:.1f} billion dollars in 2025, more than twice "
             f"the year before, and {H['lly_share']} per cent of all Lilly's revenue. <bookmark mark='b'/> Merck took "
             f"{H['key_share']} per cent of its sales from one cancer drug, Keytruda, whose main American patent runs out "
             f"in {H['key_us']}. <bookmark mark='c'/> A drug company is a handful of protected products, each with an "
             "end date, and a search for the next ones.",
             base=[src], steps=[c[0], c[1], caps])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty: pharmaceuticals. Why does a pill that costs cents to make sell "
                            "for dollars, and then one day for cents?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
