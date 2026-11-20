from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class RentControl(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Rent control", r"Who gains when rents are capped?",
             "Chapter nine. Rent control.", lit={1994: r"San Francisco's Proposition I",
                                                 2019: r"Diamond, \ McQuade and Qian"},
             scale=("household", "city"), horizon=("a decade",))
        self.design()
        self.results()

    def design(self):
        D = load("housing")["dmq"]
        ax = NumberLine(x_range=[1900, 2000, 10], length=11.0, include_numbers=True, font_size=20, color=GREY_B,
                        decimal_number_config={"group_with_commas": False, "num_decimal_places": 0}).move_to(
            DOWN * 0.6)
        treated = Rectangle(width=ax.n2p(1980)[0] - ax.n2p(1900)[0], height=0.8, stroke_width=0, fill_color=RENT,
                            fill_opacity=0.5).move_to((ax.n2p(1900) + ax.n2p(1980)) / 2 + UP * 0.7)
        control = Rectangle(width=ax.n2p(2000)[0] - ax.n2p(1980)[0], height=0.8, stroke_width=0, fill_color=CITY,
                            fill_opacity=0.5).move_to((ax.n2p(1980) + ax.n2p(2000)) / 2 + UP * 0.7)
        cut = DashedLine(ax.n2p(1980) + DOWN * 0.3, ax.n2p(1980) + UP * 1.5, color=E.ACCENT, stroke_width=3)
        lt = label(r"small rental buildings built before 1980: \\ rent-controlled from 1994", font_size=19,
                   color=RENT).next_to(treated, UP, buff=0.25)
        lc = label(r"built from 1980: \\ not controlled", font_size=19, color=CITY).next_to(control, UP, buff=0.25)
        head = label(r"year a building was built", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        foot = label(r"compare the tenants and landlords on either side of the line, \ before and after 1994",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.DMQ_2019.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Expensive cities are under pressure to cap rents. San Francisco gave economists a clean test. "
            f"<bookmark mark='a'/> In {D['year']} its voters extended rent control to small multi-family "
            f"buildings built before {D['built_before']}, <bookmark mark='b'/> while those built later stayed "
            "uncontrolled. <bookmark mark='c'/> Rebecca Diamond, Tim McQuade and Franklin Qian compared tenants and "
            "landlords in buildings on either side of that line, before and after the law, tracking where tenants "
            "moved for years afterwards."
        ) as vo:
            self.play(Create(ax), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(treated), FadeIn(lt), Create(cut))
            vo.wait_until("b")
            self.play(FadeIn(control), FadeIn(lc))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def results(self):
        D = load("housing")["dmq"]
        rows = [(r"tenants moving away", D["mobility"], CITY), (r"rental housing supplied", D["supply"], RENT)]
        bars = VGroup()
        x0 = 0.6
        for k, (nm, v, col) in enumerate(rows):
            y = 1.5 - 1.6 * k
            r = Rectangle(width=abs(v) * 20, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to(np.array([x0 + v * 10, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=col).next_to(r, UP, buff=0.12, aligned_edge=RIGHT), r,
                            label(f"{100 * v:.0f}\\%", font_size=26, color=WHITE).next_to(r, LEFT, buff=0.15)))
        zero = Line(np.array([x0, 2.4, 0]), np.array([x0, -0.6, 0]), color=GREY_B, stroke_width=2)
        notes = VGroup(
            label(r"incumbent tenants stay: \\ a transfer to them, \\ worth thousands a year", font_size=18,
                  color=CITY),
            label(r"landlords sell to owners \\ and redevelop", font_size=18, color=RENT),
        )
        notes[0].move_to(np.array([x0 + 0.4, bars[0][1].get_y(), 0]), aligned_edge=LEFT)
        notes[1].move_to(np.array([x0 + 0.4, bars[1][1].get_y(), 0]), aligned_edge=LEFT)
        foot = wrapped_label(r"fewer rental homes likely pushed market rents up, \ a cost borne by the next "
                             r"renters: \ the law protected the tenants it covered and \ undermined its own goals "
                             r"for the city", 12.0, 21, E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.DMQ_2019.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Two findings. <bookmark mark='a'/> Tenants in controlled buildings were about "
            f"{abs(100 * D['mobility']):.0f} percent less likely to move, and less likely to be displaced from the "
            "city: rent control did what it promised for the people it covered, a transfer worth thousands of "
            "dollars a year each. <bookmark mark='b'/> But landlords of controlled buildings cut the rental "
            f"housing they offered by {abs(100 * D['supply']):.0f} percent, selling to owner-occupiers and "
            "redeveloping their buildings. <bookmark mark='c'/> Fewer rental homes push up the rents "
            "that everyone else pays, so the law's cost fell on future renters. Rent control is a transfer from "
            "landlords and future tenants to current ones, paid for partly in lost housing."
        ) as vo:
            self.play(FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
