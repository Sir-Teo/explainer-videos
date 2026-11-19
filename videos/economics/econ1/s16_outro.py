from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403

PROBLEMS = [
    r"Crusoe catches $F = 3\sqrt{h}$ fish and gathers $C = 4\sqrt{10-h}$ coconuts. \ Show that a fish costs "
    r"$\tfrac{4}{3}\sqrt{h/(10-h)}$ coconuts; \ evaluate it at $h = 5$, and say why it rises with $h$.",
    r"Ana needs 2 hours per fish and 3 per coconut; \ Bo needs 4 and 4. \ Who has an absolute advantage in what, \ "
    r"who a comparative advantage, \ and at what prices (coconuts per fish) do both gain from trade?",
    r"Buyers' cards: \$5, \$4, \$3, \$2, \$1. \ Sellers' cards: \$1.50, \$2.50, \$3.50, \$4.50, \$5.50. \ Find the "
    r"competitive quantity, the price band and the largest total gain. \ A sixth seller arrives with a \$1.00 card: "
    r"what changes?",
    r"In Haifa the fined centres averaged 8.0, 16.4 and 18.7 late pick-ups a week before, during and after the "
    r"fine; \ the others 10.0, 9.2 and 8.25. \ Compute the difference in differences for each period, \ and state "
    r"the assumption it rests on.",
    r"Derive the rule of 70. \ How long does income take to double at 0.164\% a year, \ and at 1.334\%? \ By what "
    r"factor does it rise in a century at 2\%?",
    r"A city fines littering, \ and complaints about litter rise. \ Give two explanations other than ``the fine "
    r"caused more littering'', \ and a design that would tell them apart.",
    r"$\star$ \ Simon's Martian, measured: \ for one country, \ estimate how much economic activity is coordinated "
    r"inside firms rather than between them through markets. \ What data would you need, \ and what would mislead you?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = label(ASK, font_size=56, color=E.ACCENT).move_to(UP * 1.6)
        a = wrapped_label(r"Nobody, \ and millions of people: \ each knowing one small thing, \ coordinated by "
                          r"prices that carry what nobody knows in full. \ And the same order can fail, \ in ways "
                          r"that very clever people did not see coming.", 11.5, 34, WHITE).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "So: who feeds Paris? <bookmark mark='a'/> Nobody, and millions of people. Each of them knows one small "
            "thing, and they are coordinated by prices that carry what nobody knows in full. And the same order "
            "can fail, in ways that very clever people did not see coming."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
        self.clear_scene()

    def recap(self):
        pit, ric, pins, tin, fine, lr, c = (load(k) for k in ("pit", "ricardo", "pins", "tin", "fine", "longrun",
                                                              "collapses"))
        items = [
            (rf"the pit: \ strangers with private cards found the band {dollars(pit['p_lo'])} to "
             rf"{dollars(pit['p_hi'])} \ in three periods", E.DEMAND),
            (r"cost is what you give up: \ the slope of the frontier, \ rising with diminishing returns", CRUSOE),
            (rf"comparative, not absolute, advantage: \ both gain at {ric['price']:.1f} coconut a fish", FRIDAY),
            (rf"the pin factory: \ {pins['per_person']:,} pins a man, \ against at most {pins['alone_at_most']}; "
             r"\ limited by the extent of the market".replace(",", "{,}", 1), E.FIRMS),
            (rf"Hayek's tin: \ one price told sixty users what nobody knew; \ rationing wasted "
             rf"{100 * tin['extra_share']:.1f}\% more", TIN),
            (rf"a fine is a price: \ late pick-ups rose by about {fine['did']:.0f} a week, \ and stayed up", FINE),
            (rf"the long view: \ {100 * lr['g_uk_pre']:.2f}\% a year, then {100 * lr['g_world']:.2f}\%: \ "
             rf"{lr['world_ratio']:.0f} times richer since 1820", WHITE),
            (r"a model is a map, \ wrong on purpose; \ is and ought are kept apart", E.OUGHT),
            (rf"1929: \ output down {100 - c['gdp29_min']:.0f}\%; \ 2008: \ forecast up, \ and it fell", E.MISS),
            (r"the Tableau, \ Agora, \ the Island, \ the Facts, \ the Dials", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=col) for i, (t, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 1, \ in ten lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part one in ten lines. <bookmark mark='a'/> Strangers holding private cards found the competitive "
            "price in three periods. Cost is what you give up, and it rises as you do more of one thing. Two "
            "people gain from trade whenever their costs differ, even if one is better at everything. A pin factory "
            "multiplies what each worker makes, if there's a market for the pins. One price told sixty users of tin "
            "what none of them knew. A fine became a price, and late pick-ups rose. Income was nearly flat for "
            "centuries, and has risen fifteenfold since 1820. A model is a map, wrong on purpose, and what is must "
            "be kept apart from what ought to be. The order can fail: in 1929 badly, and in 2008 unforeseen. And "
            "the series has its tools: the Tableau, Agora, the Island, the Facts and the Dials."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=36.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22, width=13.0)
        with self.voiceover(
            "The problems. A derivation of Crusoe's opportunity cost; a comparative advantage puzzle; a pit market "
            "to solve by hand; the Haifa data, as a difference in differences; the arithmetic of compound growth; "
            "a design critique; and a research problem, marked with a star, on Simon's Martian. Full solutions are "
            "in the part's notes."
        ):
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Adam Smith, \emph{The Wealth of Nations} (1776), Book I, chs 1--3",
             r"David Ricardo, \emph{Principles of Political Economy and Taxation} (1817), ch. 7",
             r"Fr\'ed\'eric Bastiat, \emph{Economic Sophisms} (1845)",
             r"The CORE Team, \emph{The Economy}, units 1--2; \ N. Gregory Mankiw, \emph{Principles of Economics}, chs "
             r"1--3",
             r"Robert Heilbroner, \emph{The Worldly Philosophers}; \ Dani Rodrik, \emph{Economics Rules} (2015)"],
            [r"Hayek (1945), ``The Use of Knowledge in Society'', \emph{AER} 35",
             r"Coase (1937), ``The Nature of the Firm'', \emph{Economica} 4; \ Simon (1991), \emph{JEP} 5(2)",
             r"Chamberlin (1948), \emph{JPE} 56; \ Smith (1962), \emph{JPE} 70; \ Gode and Sunder (1993), \emph{JPE} "
             r"101; \ Cliff (1997)",
             r"Gneezy and Rustichini (2000), ``A Fine Is a Price'', \emph{Journal of Legal Studies} 29",
             r"Friedman (1953), ``The Methodology of Positive Economics''; \ Read (1958), ``I, Pencil''",
             r"Bolt and van Zanden (2024), the Maddison Project Database 2023; \ Besley and Hennessy (2009)"])
        with self.voiceover(
            "The reading for this part: Smith, Ricardo and Bastiat in the original; the first chapters of any "
            "principles textbook, such as the CORE team's free one, or Mankiw's; and the papers by Hayek, Coase, "
            "Simon, Smith, and Gneezy and Rustichini. Each is short, and each is still worth reading."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        isl = island_shape(8.0, 3.8).move_to(DOWN * 0.4)
        old = VGroup(islander("crusoe", 0.7, name=True, font_size=16), islander("friday", 0.7, name=True,
                                                                                font_size=16))
        old.arrange(RIGHT, buff=0.4).move_to(isl.get_center() + LEFT * 2.0)
        new = VGroup(*[islander(k, 0.7, name=True, font_size=16) for k in ("ana", "bo", "chidi", "dara")])
        new.arrange(RIGHT, buff=0.35).move_to(isl.get_center() + RIGHT * 1.6)
        boat = VGroup(Polygon([-0.8, 0, 0], [0.8, 0, 0], [0.55, -0.32, 0], [-0.55, -0.32, 0], stroke_width=0,
                              fill_color="#8A6A3B", fill_opacity=1),
                      Line([0, 0, 0], [0, 0.9, 0], color=GREY_A, stroke_width=3),
                      Polygon([0.05, 0.85, 0], [0.05, 0.15, 0], [0.6, 0.2, 0], stroke_width=0, fill_color=GREY_A,
                              fill_opacity=0.9)).move_to([6.2, -2.6, 0])
        stall = VGroup(fish_glyph(0.5), label(r"fish: \ \$?", font_size=24, color=E.ACCENT)).arrange(RIGHT, buff=0.15)
        stall.next_to(new, UP, buff=0.4)
        nxt = VGroup(label(r"Next: \ Part 2", font_size=30, color=GREY_B),
                     label(r"The Scissors", font_size=56, color=WHITE),
                     label(r"what sets a price? \ demand and supply, \ built from the cards", font_size=26,
                           color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        logo = scissors_logo(0.9).next_to(nxt[1], LEFT, buff=0.4)
        with self.voiceover(
            "And here's the problem the next part opens with. <bookmark mark='a'/> A boat comes ashore, and four "
            "more people step off it: Ana, Bo, Chidi and Dara. <bookmark mark='b'/> Ana fishes. Bo would like to buy. "
            "Soon there is a fish market on the Island, with buyers and sellers on both sides, and a question: what "
            "will a fish cost? "
            "<bookmark mark='c'/> Part two: the scissors. Why water is cheap and diamonds are dear, how demand and "
            "supply are built from the cards in the pit, and who really pays a tax."
        ) as vo:
            self.play(FadeIn(isl), FadeIn(old))
            vo.wait_until("a")
            self.play(boat.animate.move_to([3.8, -2.2, 0]), run_time=2)
            self.play(LaggedStart(*[FadeIn(n, shift=LEFT * 0.3) for n in new], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(stall, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(nxt), FadeIn(logo))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
