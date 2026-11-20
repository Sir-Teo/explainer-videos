from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


def hist_panel(C, nm, col, center, title):
    bins = np.array(C["bins"])
    ax = plane([4.2, 5.8], [0, 0.7], center=center, x_length=5.4, y_length=3.6,
               xticks=[4.25, 4.5, 4.75, 5.05, 5.5], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"starting wage, \ \$",
               ylabel=r"share of restaurants", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: rf"{100 * v:.0f}\%",
               font_size=12)
    bars = {}
    for wv, fc, op in (("before", GREY_B, 0.55), ("after", col, 0.85)):
        g = VGroup()
        for k, h in enumerate(C["hist"][f"{nm}_{wv}"]):
            x0, x1 = bins[k], bins[k + 1]
            p0, p1 = ax.ax.c2p(x0 + 0.005, 0), ax.ax.c2p(x1 - 0.005, min(h, 0.7))
            g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0, fill_color=fc,
                            fill_opacity=op if h > 0 else 0).move_to((p0 + p1) / 2))
        bars[wv] = g
    head = label(title, font_size=20, color=col).next_to(ax, UP, buff=0.15)
    return ax, bars, head


class Border(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The border design", r"Did the law bind, \ and what did the critics find?",
             "Chapter five. The border design.", lit={1994: r"Card and Krueger", 2000: r"Neumark and Wascher"},
             scale=("firm", "market"), horizon=("a year",))
        self.wages()
        self.debate()

    def wages(self):
        C = load("ck")
        a1, b1, h1 = hist_panel(C, "nj", NJ, LEFT * 3.4 + DOWN * 0.3, r"New Jersey")
        a2, b2, h2 = hist_panel(C, "pa", PA, RIGHT * 3.4 + DOWN * 0.3, r"Pennsylvania")
        keys = label(r"grey: \ February; \ coloured: \ November", font_size=18, color=GREY_A).to_edge(UP, buff=0.4)
        foot = label(rf"New Jersey: \ {100 * C['nj']['below_new_before']:.0f}\% paid under \$5.05 before; \ "
                     rf"{100 * C['nj']['at_new_after']:.0f}\% paid exactly \$5.05 after", font_size=19,
                     color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = data_tag(r"Card and Krueger (1994), \ public data", corner=DR, font_size=12)
        with self.voiceover(
            "First, did the law bite? Here are the starting wages restaurants reported. <bookmark mark='a'/> In "
            "February, in both states, many paid exactly the old minimum, four twenty-five, and most paid less than "
            f"five oh five: {100 * C['nj']['below_new_before']:.0f} percent in New Jersey. <bookmark mark='b'/> By "
            "November New Jersey's distribution had jumped: almost nobody paid below the new minimum, and "
            f"{100 * C['nj']['at_new_after']:.0f} percent paid exactly five dollars and five cents. "
            "<bookmark mark='c'/> Pennsylvania's barely moved. The law bound hard, on almost every New Jersey "
            "restaurant, and yet employment did not fall."
        ) as vo:
            self.play(FadeIn(keys), FadeIn(tag), FadeIn(a1), FadeIn(a2), FadeIn(h1), FadeIn(h2))
            vo.wait_until("a")
            self.play(FadeIn(b1["before"]), FadeIn(b2["before"]))
            vo.wait_until("b")
            self.play(FadeIn(b1["after"]), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(b2["after"]))
        self.clear_scene()

    def debate(self):
        C = load("ck")
        N = tables.NW_2000.data
        cards = point_cards([
            (r"prices", rf"entr\'ees: \ New Jersey \\ {100 * C['price_nj']:+.1f}\%, \ Pennsylvania \\ "
                        rf"{100 * C['price_pa']:+.1f}\%", NJ),
            (r"2000: \ payroll records", rf"Neumark and Wascher, \\ {N['stores']} restaurants: \\ employment "
                                        rf"{N['effect']:+.1f}\% \\ in New Jersey", LOSS),
            (r"2000: \ the reply", r"Card and Krueger, \\ government payroll-tax \\ records: \ no loss", WAGE),
            (r"since", r"border counties, \\ panels of states, \\ synthetic controls, \\ bunching", E.ACCENT),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"the costs went somewhere, \ and the debate began", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        tag = published_tag(tables.NW_2000.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Where did the cost go? <bookmark mark='a'/> Partly into prices: the price of an entrée rose about "
            f"{100 * C['price_nj']:.0f} percent in New Jersey relative to Pennsylvania. <bookmark mark='b'/> The "
            "result provoked a fierce reply. David Neumark and William Wascher argued that telephone answers about "
            f"employment were noisy, collected payroll records from {N['stores']} restaurants, and found employment "
            f"about {abs(N['effect']):.1f} percent lower in New Jersey. <bookmark mark='c'/> Card and Krueger answered "
            "with the government's own payroll-tax records, which showed no relative loss, and traced the difference "
            "to a handful of restaurants owned by a single franchisee. <bookmark mark='d'/> Twenty-five years of "
            "designs followed: neighbouring counties across state lines, panels of states, synthetic controls. The "
            "next chapter shows the one that changed the conversation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
