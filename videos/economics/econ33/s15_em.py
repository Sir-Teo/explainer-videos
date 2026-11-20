from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403

CUR = {"baht": ("#F2C14E", r"Thailand's baht"), "won": ("#7EC8F5", r"Korea's won"),
       "peso": ("#E8A0B4", r"Mexico's peso")}


class EM(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Sudden stops", r"Why are crises in emerging markets so violent?",
             "Chapter thirteen. Sudden stops.", lit={1994: r"Mexico", 1997: r"Thailand and Korea",
                                                     1998: r"Calvo"},
             scale=("nation", "world"), horizon=("a month", "a year"))
        self.currencies()
        self.sin()

    def currencies(self):
        E_ = load("em")
        ax = plane([-6, 24], [80, 260], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[-6, 0, 6, 12, 18, 24], yticks=[100, 150, 200, 250],
                   xlabel=r"months from the month before the crisis", ylabel=r"dollars' price in local currency, \ "
                   r"that month = 100", xfmt=lambda v: f"{v:+.0f}" if v else "0", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        lines, side = {}, VGroup()
        for k, (col, name) in CUR.items():
            d = E_[k]
            t0 = int(d["before_date"][:4]) + (int(d["before_date"][5:7]) - 1) / 12
            xs = [12 * (t - t0) for t in d["t"]]
            ys = [100 * v / d["before"] for v in d["v"]]
            lines[k] = path(ax, xs, ys, col, 3.2, xr=(-6, 24), yr=(80, 260), smooth=False)
            side.add(label(rf"{name}: \ lost {d['fall']:.0f}\% \\ of its dollar value by "
                           rf"{d['peak_date'][:7].replace('-', '/')}", font_size=19, color=col))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Board of Governors (H.10), \ via FRED: \ EXTHUS, \ EXKOUS, \ EXMXUS", corner=DR,
                       font_size=12)
        with self.voiceover(
            "In emerging economies, crises have a signature of their own. <bookmark mark='a'/> In December 1994 "
            "Mexico could no longer defend its peso, and within a year it had lost "
            f"{E_['peso']['fall']:.0f} percent of its value against the dollar. <bookmark mark='b'/> On the second "
            "of July 1997 Thailand, out of reserves, let the baht float; by January it had lost "
            f"{E_['baht']['fall']:.0f} percent. <bookmark mark='c'/> The panic spread to Indonesia, Malaysia and "
            f"Korea, whose won lost {E_['won']['fall']:.0f} percent by January 1998. <bookmark mark='d'/> Guillermo "
            "Calvo called these sudden stops: foreign capital that had been flowing in for years stops, or "
            "reverses, within months, and a country that was borrowing abroad to invest must suddenly cut spending "
            "by the whole of the flow."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for mk, k in zip("abc", ("peso", "baht", "won")):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(side[list(CUR).index(k)]), run_time=1.6)
            vo.wait_until("d")
            self.play(*[Indicate(lines[k], color=WHITE, scale_factor=1.0) for k in lines])
        self.clear_scene()

    def sin(self):
        E_ = load("em")
        b = E_["baht"]
        before, after = b["before"], b["peak"]
        rows = VGroup(
            label(r"original sin: \ an emerging economy cannot borrow abroad in its own currency", font_size=25,
                  color=E.ACCENT),
            label(rf"a Thai firm owes \$1 million: \ {before:.1f} million baht in June 1997", font_size=23,
                  color=WHITE),
            label(rf"in January 1998, \ the same debt is {after:.1f} million baht: \ {after / before:.1f} times as "
                  r"heavy", font_size=23, color=CRISIS),
            label(r"Fisher's debt deflation, \ through the exchange rate: \ the fall that should help exporters "
                  r"bankrupts borrowers", font_size=22, color=CREDIT),
            label(r"and the IMF lends, \ on conditions: \ its record is Part 34's", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"Calvo, \ \emph{Journal of Applied Economics} 1(1) (1998); \ Eichengreen and Hausmann "
                            r"(1999)", corner=DR, font_size=12)
        with self.voiceover(
            "Why so violent? <bookmark mark='a'/> Barry Eichengreen and Ricardo Hausmann named the reason original "
            "sin: most emerging economies cannot borrow abroad in their own currency, so their debts are in "
            f"dollars. <bookmark mark='b'/> A Thai company owing a million dollars owed {before:.1f} million baht "
            f"in June 1997. <bookmark mark='c'/> By January 1998 it owed {after:.1f} million baht, "
            f"{after / before:.1f} times as much, with revenues still in baht. <bookmark mark='d'/> It is Fisher's "
            "debt deflation again, through the exchange rate: the depreciation that ought to help the economy by "
            "making exports cheaper bankrupts everyone who borrowed in dollars, and with them the banks that lent. "
            "<bookmark mark='e'/> Then the International Monetary Fund lends, with conditions attached. Whether its "
            "conditions helped is a long argument, which Part thirty-four takes up with the open economy."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
