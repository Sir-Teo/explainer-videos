from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.three()
        self.maker()
        self.history()
        self.mitsui()
        self.title()

    def three(self):
        H = R["hook"]
        B = H["big3"]
        sheds = VGroup(*[draw.warehouse(2.6, docks=5, trucks=1) for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to([0, 1.6, 0])
        c = stat_cards([(f"${B['MCK']['rev']:.0f}bn", "McKesson, year to March 2026", DRUG),
                        (f"${B['COR']['rev']:.0f}bn", "Cencora, year to September 2026", DRUG),
                        (f"${B['CAH']['rev']:.0f}bn", "Cardinal Health, year to June 2026", DRUG)], y=-0.5, size=36, span=12.4)
        tot = tx(f"together ${H['big3_rev']:.0f}bn of revenue; ${H['big3_ni']:.1f}bn of profit: {100 * H['big3_ni'] / H['big3_rev']:.1f} cents a dollar",
                 20, GOOD, bold=True).move_to([0, -2.1, 0])
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Three American companies you may never have heard of. <bookmark mark='a'/> McKesson took in "
             f"{B['MCK']['rev']:.0f} billion dollars in its last year. <bookmark mark='b'/> Cencora, "
             f"{B['COR']['rev']:.0f} billion. <bookmark mark='c'/> Cardinal Health, {B['CAH']['rev']:.0f} billion. They "
             "make nothing. They buy medicines from the companies that make them and deliver them to pharmacies and "
             f"hospitals. <bookmark mark='d'/> Together, almost a trillion dollars of revenue, and about "
             f"{H['big3_ni']:.0f} billion of profit: one cent on the dollar.",
             base=[sheds, src], steps=[c[0], c[1], c[2], tot])

    def maker(self):
        H = R["hook"]
        items = [("McKesson (wholesaler)", H["big3"]["MCK"]["rev"], DRUG, f"${H['big3']['MCK']['rev']:.0f}bn"),
                 ("Johnson & Johnson (the largest drug maker)", H["maker_rev"], GOODS, f"${H['maker_rev']:.0f}bn")]
        rows = hbars(items, max_value=420, x0=-1.2, top=1.0, row=1.4, length=7.0, size=18, bar_h=0.7)
        hd = tx("Revenue, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("the same medicines are counted twice: once when the maker sells them, again when the wholesaler does", 16, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("McKesson and Johnson & Johnson, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Put that beside the companies that invent and make the medicines. <bookmark mark='a'/> McKesson's revenue "
             f"was {H['big3']['MCK']['rev']:.0f} billion dollars. <bookmark mark='b'/> Johnson and Johnson, the largest "
             f"drug and device maker in this series' extract, took in {H['maker_rev']:.0f} billion. The middleman's revenue "
             "is four times the maker's, because it counts the whole price of every box it passes on, from every maker at "
             "once. Its profit is another matter.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1]])

    def history(self):
        Hh = R["hook"]["mck_hist"]
        rev = {y + 1: v[0] for y, v in Hh.items()}
        ni = {y + 1: v[1] for y, v in Hh.items()}
        ch = line_chart({"revenue": (rev, DRUG)}, x=(2011, 2026), y=(0, 450), xticks=[2011, 2014, 2017, 2020, 2023, 2026],
                        yticks=[0, 100, 200, 300, 400], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="McKesson's revenue, $bn, fiscal years to March", width=8.8, height=4.4, center=(-1.0, -0.45))
        nb = VGroup(*[Dot(ch.ax.c2p(y, 20 * max(v, 0)), radius=0.05, color=GOOD) for y, v in ni.items()])
        nl = tx("net profit x 20, to be visible", 14, GOOD).next_to(nb[-1], DOWN, buff=0.25, aligned_edge=RIGHT)
        src = source("McKesson, Forms 10-K via SEC company facts", size=12)
        f, l = min(rev), max(rev)
        beat(self,
             f"<bookmark mark='a'/> McKesson's revenue has grown from {rev[f]:.0f} billion dollars in its year to March "
             f"{f} to {rev[l]:.0f} billion. <bookmark mark='b'/> Its profit, magnified twenty times so it shows at all, has "
             f"never been more than {max(ni.values()):.1f} billion in a year. That is the first puzzle of this film: a "
             "business that keeps about a penny of each dollar, and is one of the largest in the world.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["revenue"], ch.labels["revenue"]), VGroup(nb, nl)])

    def mitsui(self):
        H = R["hook"]
        T = R["trading"]
        ship = draw.ship(3.2)
        ship.move_to([-4.2, 1.4, 0])
        c = stat_cards([(f"¥{T['rev'] / 1e3:.1f}trn", f"Mitsui & Co.'s revenue, year to March 2026 (${H['mitsui_rev']:.0f}bn)", TRADE),
                        (f"¥{T['profit']:.0f}bn", f"its profit (${H['mitsui_ni']:.1f}bn)", GOOD),
                        (f"{100 * T['equity'] / T['profit']:.0f}%", "of that profit came from companies it partly owns", TRADE)],
                       y=-0.7, size=34, span=12.4)
        src = source("Mitsui & Co., consolidated financial results for the year ended 31 March 2026", size=12)
        beat(self,
             "And the second puzzle comes from Japan. <bookmark mark='a'/> Mitsui and Company began as a trading house: a "
             f"company that bought and sold goods for others. Its revenue was {T['rev'] / 1e3:.1f} trillion yen in its last "
             f"year, about {H['mitsui_rev']:.0f} billion dollars. <bookmark mark='b'/> Its profit was {T['profit']:.0f} "
             f"billion yen, six cents on the dollar, far more than a penny. <bookmark mark='c'/> But more than half of it "
             "came not from trading at all, but from mines, gas fields and other companies it partly owns. The middleman "
             "became an owner.",
             base=[ship, src], steps=[c[0], c[1], c[2]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-three: the middlemen. If the internet removes the middleman, why "
                            "are the middlemen among the largest companies in every country?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
