from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Agreements(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Trade agreements: \ escaping a dilemma", r"Why would a country promise not to use a tariff "
             r"that helps it?", "Chapter eleven. Trade agreements: escaping a dilemma.",
             lit={1947: r"the GATT", 1995: r"the WTO", 1999: r"Bagwell and Staiger"}, scale=("nation", "world"),
             horizon=("a decade",))
        self.game()
        self.responses()
        self.rules()

    def game(self):
        W = load("war")
        pay = W["pay"]
        k = 100
        cells = VGroup()
        names = (("free", r"free trade"), ("tariff", r"a tariff"))
        for i, (ri, rn) in enumerate(names):
            for j, (cj, cn) in enumerate(names):
                a, b = pay[f"{ri}|{cj}"]
                box = Rectangle(width=3.4, height=1.3, stroke_color=GREY_C, stroke_width=2)
                box.move_to(np.array([-0.4 + 3.4 * j, 0.6 - 1.3 * i, 0]))
                txt = VGroup(label(f"{k * a:+.0f}", font_size=30, color=ISLAND if a >= 0 else TARIFF),
                             label(r",", font_size=30, color=GREY_B),
                             label(f"{k * b:+.0f}", font_size=30, color=ARCH if b >= 0 else TARIFF)).arrange(
                    RIGHT, buff=0.15).move_to(box)
                cells.add(VGroup(box, txt))
        rows = VGroup(*[label(n, font_size=22, color=ISLAND).next_to(cells[2 * i], LEFT, buff=0.3)
                        for i, (_, n) in enumerate(names)])
        cols = VGroup(*[label(n, font_size=22, color=ARCH).next_to(cells[j], UP, buff=0.2)
                        for j, (_, n) in enumerate(names)])
        who = VGroup(label(r"the Island", font_size=22, color=ISLAND).next_to(rows, LEFT, buff=0.3).rotate(PI / 2),
                     label(r"the Archipelago", font_size=22, color=ARCH).next_to(cols, UP, buff=0.2))
        note_ = label(rf"gains against free trade, \ in hundredths; \ each country's best tariff: "
                      rf"{W['nash']:.2f}", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The large-country tariff makes trade policy a game. <bookmark mark='a'/> Two large economies, the "
            "Island and the Archipelago, each choose free trade or the tariff that is best for itself. The numbers "
            "are each country's gain over free trade, computed from Agora's model. <bookmark mark='b'/> If the "
            f"Island taxes and the Archipelago does not, the Island gains {k * pay['tariff|free'][0]:.0f} and the "
            f"Archipelago loses {abs(k * pay['tariff|free'][1]):.0f}. <bookmark mark='c'/> The reverse, in the other "
            "corner. <bookmark mark='d'/> So whatever the other does, each does better with a tariff, and both "
            f"end up taxing, each {abs(k * pay['tariff|tariff'][0]):.0f} worse off than under free trade. "
            "<bookmark mark='e'/> It is the prisoner's dilemma of Part eleven, and the 1930s played it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cells[0]), FadeIn(rows), FadeIn(cols), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(cells[2]))
            vo.wait_until("c")
            self.play(FadeIn(cells[1]))
            vo.wait_until("d")
            self.play(FadeIn(cells[3]), Indicate(cells[3], color=TARIFF, scale_factor=1.05))
            vo.wait_until("e")
            self.play(Indicate(cells[0], color=GAIN, scale_factor=1.05))
        self.clear_scene()

    def responses(self):
        W = load("war")
        top = W["prohibitive"] * 0.45
        ax = plane([0, top], [0, top], center=LEFT * 2.2 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[0, 0.5, 1.0, 1.5], yticks=[0, 0.5, 1.0, 1.5], xlabel=r"the Archipelago's tariff",
                   ylabel=r"the Island's tariff", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        g, br = W["grid"], W["br"]
        bI = path(ax, g, br, ISLAND, 3.2, xr=(0, top), yr=(0, top))
        bA = path(ax, br, g, ARCH, 3.2, xr=(0, top), yr=(0, top))
        nash = dot(ax, W["nash"], W["nash"], TARIFF, 0.1)
        free = dot(ax, 0, 0, GAIN, 0.1)
        side = VGroup(
            label(r"teal: \ the Island's best tariff \\ for each Archipelago tariff", font_size=18, color=ISLAND),
            label(r"gold: \ the Archipelago's", font_size=18, color=ARCH),
            label(rf"they cross at {W['nash']:.2f} each: \\ the trade war's equilibrium", font_size=18,
                  color=TARIFF),
            label(r"free trade, \ at the corner, \\ is better for both, \\ but neither will go there \\ alone",
                  font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The same game as a picture. <bookmark mark='a'/> The teal line is the Island's best tariff for each "
            "tariff the Archipelago might set; <bookmark mark='b'/> the gold line, the Archipelago's. "
            f"<bookmark mark='c'/> They cross at {W['nash']:.2f} each, the equilibrium of a trade war, where neither "
            "wants to change. <bookmark mark='d'/> Both would be better off at the corner, with no tariffs, but "
            "neither will move there alone, because each tariff's gain comes out of the other's pocket."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(bI), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(bA), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(nash, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(free, scale=1.5), FadeIn(side[3]))
        self.clear_scene()

    def rules(self):
        F = load("film")
        cards = point_cards([
            (r"the GATT, \ 1947", r"23 countries agree \\ to bind tariffs \\ and cut them \\ in rounds", GAIN),
            (r"reciprocity", r"I cut if you cut: \\ each gives up \\ its terms-of-trade gain \\ together", ISLAND),
            (r"most favoured nation", r"one tariff for all \\ members: \\ no deals that \\ shift the burden", ARCH),
            (r"the WTO, \ 1995", r"a court for disputes, \\ and permission \\ to retaliate \\ if it is ignored",
             FISH),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"agreements that neutralize the externality", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.6)
        foot = label(rf"America's average tariff on goods: \ {F['v2024']:.1f}\% in 2024, \ {F['v2025']:.1f}\% in "
                     r"2025 \ (Part 66)", font_size=21, color=TARIFF).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Bagwell and Staiger, \ \emph{AER} 89(1) (1999); \ BEA, \ via FRED", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Kyle Bagwell and Robert Staiger argued in 1999 that this is what trade agreements are for. "
            "<bookmark mark='a'/> In 1947 twenty-three countries signed the General Agreement on Tariffs and Trade, "
            "binding their tariffs and cutting them, round after round. <bookmark mark='b'/> Its rule of reciprocity "
            "means each country gives up its terms-of-trade gain at the same time as the others give up theirs. "
            "<bookmark mark='c'/> Its rule of the most favoured nation, one tariff for every member, stops two "
            "countries from striking deals that push the cost onto a third. <bookmark mark='d'/> In 1995 the World "
            "Trade Organization added a court for disputes, and permission to retaliate when a ruling is ignored. "
            f"<bookmark mark='e'/> The game has not gone away. America's average tariff on goods was "
            f"{F['v2024']:.1f} percent in 2024 and {F['v2025']:.1f} percent in 2025, the largest rise in a single "
            "year since this series begins, in 1929. Part sixty-six returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
