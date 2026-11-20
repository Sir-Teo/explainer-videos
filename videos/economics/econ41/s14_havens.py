from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Havens(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Corporations and tax havens", r"Where do multinationals' profits go?",
             "Chapter twelve. Corporations and tax havens.", lit={2013: r"Zucman", 2021: r"the global minimum tax",
                                                                 2023: r"T\o{}rsl\o{}v, \ Wier and Zucman"},
             scale=("firm", "world"), horizon=("a year", "a decade"))
        self.shifting()
        self.minimum()

    def shifting(self):
        H = tables.HAVENS.data
        waffle = VGroup(*[Square(side_length=0.36, stroke_width=0, fill_color=CAPITAL if k < H["profits"] else GREY_D,
                                 fill_opacity=0.9) for k in range(100)])
        waffle.arrange_in_grid(rows=10, cols=10, buff=0.06).move_to(LEFT * 3.2 + DOWN * 0.2)
        wl = label(rf"multinational profits, \ 2015: \\ {H['profits']}\% booked in tax havens", font_size=20,
                   color=CAPITAL).next_to(waffle, UP, buff=0.25)
        steps = flow_chain([(r"a patent, \ a brand, \\ a loan", RATE),
                            (r"owned by an affiliate \\ in a haven", CAPITAL),
                            (r"royalties and \\ interest paid to it", TOP)],
                           notes=[r"made where the \\ firm works", r"almost no tax", r"profits taxed \\ where "
                                  r"rates are low"], box_w=2.6, font_size=18, note_size=14).scale(0.85)
        steps.move_to(RIGHT * 3.2 + UP * 0.6)
        side = label(rf"households, \ too: \ about {H['wealth']}\% of \\ their financial wealth \\ is held offshore",
                     font_size=19, color=WORKER).next_to(steps, DOWN, buff=0.5)
        tag = published_tag(tables.HAVENS.tag, corner=DR, font_size=10)
        with self.voiceover(
            "The corporate tax has a second problem besides incidence: profits can be moved on paper. "
            "<bookmark mark='a'/> Thomas Torslov, Ludvig Wier and Gabriel Zucman compared how profitable foreign "
            f"affiliates are in tax havens with firms elsewhere, and estimated that {H['profits']} percent of "
            "multinationals' profits made outside their home countries were booked in havens in 2015. "
            "<bookmark mark='b'/> The method is simple: put a patent, a brand or a loan in an affiliate in a "
            "low-tax country, <bookmark mark='c'/> and have the rest of the group pay it royalties and interest, so "
            "that profits appear where taxes are low. <bookmark mark='d'/> Households do the same with wealth: in "
            f"2013 Zucman estimated that about {H['wealth']} percent of households' financial wealth was held in tax "
            "havens, most of it unrecorded."
        ) as vo:
            self.play(FadeIn(waffle, lag_ratio=0.01), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(wl), *[sq.animate.set_fill(CAPITAL, 0.9) for sq in waffle[:H["profits"]]])
            vo.wait_until("b")
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]), GrowArrow(steps.arrows[0]),
                      FadeIn(steps.boxes[1]),
                      FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def minimum(self):
        H = tables.HAVENS.data
        cards = point_cards([
            (r"October 2021", rf"{H['countries']} of {H['members']} \\ jurisdictions agree a \\ global minimum tax",
             GAIN),
            (rf"{H['minimum']}\%", r"on the profits of \\ multinationals with \\ revenue of 750 \\ million euros "
                                    r"or more",
             TOP),
            (r"how", r"if an affiliate pays \\ less, \ the home \\ country collects \\ the difference", RATE),
            (r"the race to the bottom", r"a floor under it, \\ though the rate is \\ low and the rules \\ have gaps",
             WORKER),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a floor under the race: \ the global minimum tax", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.6)
        tag = published_tag(r"OECD/G20 Inclusive Framework (2021)", corner=DR, font_size=11)
        with self.voiceover(
            "For forty years statutory corporate rates fell around the world, as countries competed for profits on "
            "paper as well as for factories. <bookmark mark='a'/> In October 2021, "
            f"{H['countries']} of the {H['members']} members of the OECD's inclusive framework agreed on a floor: "
            f"<bookmark mark='b'/> a minimum tax of {H['minimum']} percent on the profits of multinationals with "
            "revenue of at least 750 million euros. <bookmark mark='c'/> If an affiliate pays less, its parent's "
            "home country, or others, can collect the difference. <bookmark mark='d'/> It puts a floor under the "
            "race to the bottom; critics note that the floor is low and the rules have exceptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
