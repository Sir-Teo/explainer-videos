from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Mergers(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Mergers that destroy value", r"Why do so many acquisitions disappoint the acquirer?",
             "Chapter thirteen. Mergers that destroy value.",
             lit={1995: r"Berger and Ofek", 1998: r"DaimlerChrysler", 2005: r"Moeller, Schlingemann and Stulz"},
             scale=("firm",), horizon=("a decade",))
        self.discount()
        self.acquirers()

    def discount(self):
        G = load("conglomerates")
        total, before = 100 * G["discount"], 100 * G["before"]
        after = total - before
        ax = plane([-0.6, 1.6], [-15, 2], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.4, y_length=4.4, xticks=[],
                   yticks=[-15, -10, -5, 0], ylabel=r"value against stand-alone units, \ \%",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        b0 = bars(ax, [0], [total], [COST], width=0.55)
        p0, p1 = ax.ax.c2p(0.75, 0), ax.ax.c2p(1.25, before)
        bb = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=GREY_B,
                       fill_opacity=0.85).move_to((p0 + p1) / 2)
        q0, q1 = ax.ax.c2p(0.75, before), ax.ax.c2p(1.25, total)
        ba = Rectangle(width=q1[0] - q0[0], height=abs(q1[1] - q0[1]), stroke_width=0, fill_color=COST,
                       fill_opacity=0.85).move_to((q0 + q1) / 2)
        labs = VGroup(label(r"the discount \\ measured", font_size=14, color=COST).next_to(ax.ax.c2p(0, 0), UP,
                                                                                          buff=0.1),
                      label(r"before \ + \ after \\ diversifying", font_size=14, color=GREY_A).next_to(
                          ax.ax.c2p(1, 0), UP, buff=0.1))
        side = VGroup(
            label(r"a diversified firm's value against the sum of its parts, \\ each valued like a firm that does "
                  r"only that", font_size=19, color=WHITE),
            label(rf"the Island: \ {total:.1f}\%", font_size=21, color=COST),
            label(rf"grey: \ {before:.1f} points were there before the firms diversified; \\ red: \ "
                  rf"{after:.1f} came after".replace("-", "{-}"), font_size=19, color=GREY_A),
            label(r"America, \ 1986--91: \ diversified firms worth 13--15\% less \ (Berger and Ofek)",
                  font_size=19, color=E.ACCENT),
            label(r"later work: \ much of it was selection, \ firms that diversify were worth less already",
                  font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Berger and Ofek, \ Journal of Financial Economics 37(1) (1995); \ the Island: \ "
                            r"agora.org.conglomerates", corner=DL, font_size=12)
        with self.voiceover(
            "Firms also grow by buying other firms, and the record is sobering. <bookmark mark='a'/> Compare a "
            "diversified firm's value with the sum of its parts, each valued like a firm that does only that "
            f"business. <bookmark mark='b'/> On the Island, diversified firms are worth {abs(total):.1f} percent less. "
            "<bookmark mark='c'/> But the Island knows something an analyst would not: "
            f"{abs(before):.1f} points of that were there before the firms diversified, and only "
            f"{abs(after):.1f} came after. <bookmark mark='d'/> Philip Berger and Eli Ofek measured the discount in "
            "American firms from 1986 to 1991: thirteen to fifteen percent. <bookmark mark='e'/> Later work argued "
            "that much of it was selection: firms that chose to diversify were already worth less. The habit of "
            "chapter nine again: ask what the comparison would have shown before the event."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b0[0], UP), FadeIn(labs[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bb, UP), FadeIn(labs[1]))
            self.play(GrowFromEdge(ba, UP), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def acquirers(self):
        rows = VGroup(
            history_card(r"\$240 bn", r"lost by acquirers' shareholders, \ 1998--2001", r"12 cents per dollar spent, "
                         r"\ around the announcements; \ against \$7 billion in all of the 1980s \ (Moeller, \ "
                         r"Schlingemann and Stulz)", color=COST, width=11.4, font_size=20),
            history_card(1998, r"Daimler-Benz and Chrysler", r"billed as a merger of equals, \ about \$36 billion; \ "
                         r"in 2007, \ 80.1\% of Chrysler is sold to Cerberus for \$7.4 billion", color=CEO,
                         width=11.4, font_size=20),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.7)
        why = label(r"why: \ overconfident bidders, \ empire building, \ the winner's curse of Part 16, \\ and "
                    r"cultures, \ chapter twelve's relational contracts, \ that do not merge", font_size=20,
                    color=GREY_A).next_to(rows, DOWN, buff=0.45)
        tag = published_tag(r"Moeller, \ Schlingemann and Stulz, \ Journal of Finance 60(2) (2005); \ news reports, "
                            r"\ 1998 and 2007", corner=DL, font_size=12)
        with self.voiceover(
            "And the acquirers? <bookmark mark='a'/> Sara Moeller, Frederik Schlingemann and René Stulz added up "
            "what acquiring firms' shareholders lost around merger announcements from 1998 to 2001: two hundred "
            "and forty billion dollars, twelve cents for every dollar spent, against seven billion in the whole of "
            "the 1980s, most of it in a few deals by highly valued firms. <bookmark mark='b'/> The most famous of "
            "that wave was billed as a merger of equals: Daimler-Benz and Chrysler, in 1998, a deal of about "
            "thirty-six billion dollars. In 2007 Daimler sold eighty point one percent of Chrysler to the private "
            "equity firm Cerberus for seven point four billion. <bookmark mark='c'/> Why do acquirers overpay? "
            "Overconfident bidders, chief executives building empires, Part sixteen's winner's curse, and cultures, "
            "chapter twelve's relational contracts, that do not merge as easily as balance sheets."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.clear_scene()
