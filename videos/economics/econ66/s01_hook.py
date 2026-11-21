from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.board()
        self.vietnam()
        self.best_case()
        self.question()
        self.title()
        self.objectives()

    def board(self):
        hc = history_card(r"2 April 2025", r"a tariff on almost every country", r"the United States announces a "
                          r"tariff of at least ten percent on imports from almost every country, \ higher for those "
                          r"it runs a deficit with, \ each set by one formula", color=TARIFF, width=11.6,
                          font_size=22).to_edge(UP, buff=0.5)
        eq = MathTex(r"\Delta\tau_i", r"=", r"\frac{m_i - x_i}{\varepsilon\,\varphi\, m_i}", font_size=52)
        eq.next_to(hc, DOWN, buff=0.7)
        notes = VGroup(
            label(r"$m_i$, \ $x_i$: \ US imports from and exports to country $i$", font_size=21, color=GREY_A),
            label(r"$\varepsilon = 4$: \ how much imports fall when their price rises", font_size=21, color=US),
            label(r"$\varphi = 0.25$: \ the share of a tariff that reaches import prices", font_size=21,
                  color=PRICE),
            label(r"then halved, \ with a floor of ten percent", font_size=21, color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(eq, DOWN, buff=0.5)
        tag = published_tag(r"Office of the United States Trade Representative, \ \emph{Reciprocal Tariff "
                            r"Calculations} (April 2025)", corner=DL, font_size=12)
        with self.voiceover(
            "On the second of April 2025, the President of the United States stood in the Rose Garden with a board "
            "of countries and numbers. <bookmark mark='a'/> Imports from almost every country would pay a tariff of "
            "at least ten percent, and more from countries the United States bought more from than it sold to. "
            "<bookmark mark='b'/> The numbers came from one formula, published that evening by the Trade "
            "Representative. <bookmark mark='c'/> The tariff on a country is the bilateral deficit, imports minus "
            "exports, divided by imports, and by two parameters: epsilon, how strongly imports fall when their "
            "price rises, set at four; and phi, the share of a tariff that reaches import prices, set at a quarter. "
            "Four times a quarter is one, so they cancel. <bookmark mark='d'/> The result was then halved, with a "
            "floor of ten percent."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(hc, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in notes[:3]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[3], shift=RIGHT * 0.1))
        self.clear_scene()

    def vietnam(self):
        F = load("formula")
        rows = VGroup(
            label(rf"Vietnam, \ 2024: \ imports \${F['imports']:.1f} billion, \ exports \${F['exports']:.1f} billion",
                  font_size=24, color=WHITE),
            MathTex(rf"\frac{{{F['imports']:.1f} - {F['exports']:.1f}}}{{{F['imports']:.1f}}} = "
                    rf"{100 * F['raw']:.0f}\%", font_size=44, color=GREY_A),
            label(rf"halved: \ {100 * F['rate']:.0f}\% \quad published: \ {100 * F['published']:.0f}\%",
                  font_size=26, color=TARIFF),
            label(rf"with $\varphi = 0.945$, \ near the evidence: \ {100 * F['rate_945']:.0f}\%", font_size=26,
                  color=PRICE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"USTR (2024 trade); \ Corinth and Veuger, \ American Enterprise Institute (April 2025)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Take Vietnam. <bookmark mark='a'/> In 2024 the United States imported about a hundred and thirty-seven "
            "billion dollars of goods from Vietnam and sold it about thirteen. <bookmark mark='b'/> The deficit "
            f"over imports is {100 * F['raw']:.0f} percent. <bookmark mark='c'/> Halved, "
            f"{100 * F['rate']:.0f}; the published rate was {100 * F['published']:.0f}. <bookmark mark='d'/> "
            "Within days economists were arguing about phi. The evidence from the 2018 tariffs, which this part "
            "will show, is that tariffs reached import prices almost one for one. Kevin Corinth and Stan Veuger "
            f"pointed out that with phi near 0.95, the same formula gives about {100 * F['rate_945']:.0f} percent. "
            "One parameter, a factor of four. And a deeper question: does a bilateral deficit measure anything a "
            "tariff should fix?"
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def best_case(self):
        cards = point_cards([
            (r"the best case for", r"security: \ supplies a rival can cut off; \ leverage in bargaining; \ revenue; "
             r"\ and places Part 36's China shock left behind", STATE),
            (r"the best case against", r"buyers at home pay the tariff; \ partners retaliate; \ resources move to "
             r"what the country does worse; \ and the deficit is a matter of saving, \ not of tariffs", FREE),
        ], width=12.6, cols=2, font_size=21).move_to(DOWN * 0.1)
        head = label(r"each side's best case", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Before the evidence, each side's best case, as its most careful defenders would make it. <bookmark "
            "mark='a'/> For: some supplies, chips, medicines, rare minerals, should not depend on a rival that can "
            "cut them off; a tariff is leverage in negotiations; it raises revenue; and the places the China shock "
            "of Part thirty-six left behind deserve protection. <bookmark mark='b'/> Against: the tariff is paid "
            "mostly by buyers at home; partners retaliate; labour and capital move into what the country does "
            "relatively badly; and an overall trade deficit is set by how much a country saves and invests, which "
            "a tariff barely touches. This part puts each claim to the data and the models."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"who paid for the tariffs of 2018 and 2025?", font_size=26, color=PRICE),
            label(r"when do tariff wars start, \ and why does anyone sign a trade agreement?", font_size=26,
                  color=TARIFF),
            label(r"what does a bilateral deficit measure?", font_size=26, color=US),
            label(r"how does dependence become power, \ and what is resilience worth?", font_size=26, color=STATE),
            label(r"when does industrial policy work?", font_size=26, color=FREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: what happens to the gains from trade when trade becomes a weapon? <bookmark mark='a'/> "
            "Who paid for the tariffs of 2018 and 2025? <bookmark mark='b'/> When do tariff wars start, and why "
            "does anyone sign a trade agreement? <bookmark mark='c'/> What does a bilateral deficit measure? "
            "<bookmark mark='d'/> How does dependence on a supplier become power over you, and what is resilience "
            "worth? <bookmark mark='e'/> And when does industrial policy work?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        flags = VGroup(*[RoundedRectangle(width=0.7, height=0.45, corner_radius=0.06, stroke_color=c,
                                          stroke_width=2, fill_color=c, fill_opacity=0.35)
                         for c in (US, ROW, TARIFF, STATE, FREE, PRICE, US, ROW)]).arrange(RIGHT, buff=0.18)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 66 \ $\cdot$ \ Geoeconomics and Industrial Policy", font_size=34, color=E.ACCENT)
        VGroup(flags, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-six: geoeconomics and industrial policy."):
            self.play(LaggedStart(*[FadeIn(f, scale=0.6) for f in flags], lag_ratio=0.1), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what the tariffs of 2018 and 2025 did to prices, \ trade and welfare",
            r"tariff wars as games: \ optimal tariffs, \ Nash tariffs, \ and why trade agreements exist",
            r"tariffs in the quantitative trade model, \ and what bilateral deficits do and do not mean",
            r"weaponized interdependence, \ geoeconomic power, \ and resilience against efficiency",
            r"industrial policy: \ infant industries, \ the new evidence, \ and subsidy races",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-five asked what machines will do to the economy. This part asks what states do with it. "
            "By the end you will know <bookmark mark='a'/> what the tariffs of 2018 and 2025 did to prices, trade "
            "and welfare; <bookmark mark='b'/> why countries are tempted into tariff wars, and why trade agreements "
            "exist; <bookmark mark='c'/> how to run tariffs through the quantitative trade model of Part thirty-six, "
            "and what a bilateral deficit does and does not mean; <bookmark mark='d'/> how interdependence becomes "
            "a weapon, and what resilience is worth; <bookmark mark='e'/> and when industrial policy has worked, "
            "from Napoleon's blockade to South Korea's heavy industry, and when subsidies become a race."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
