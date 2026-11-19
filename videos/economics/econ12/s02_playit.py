from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

YOU = "#7BD88F"


def price_chip(p: float, color, w=1.35, font_size=30) -> VGroup:
    box = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(rf"\${p:.0f}", font_size=font_size, color=color).move_to(box)
    return VGroup(box, t)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ name your price", r"Crusoe charges \$40 for a repair that costs either yard \$10. "
             r"What do you charge?", "Chapter one. Play it: name your price.", lit={1883: r"Bertrand's review"},
             scale=("firm", "market"), horizon=("a season",))
        self.rules()
        self.reveal()
        self.twenty()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.0, 5.8, center=DOWN * 0.2)
        rules = VGroup(
            label(r"you open a second boatyard on the Island, \ beside Crusoe's", font_size=26),
            label(rf"a repair costs either yard \${p['cost']:.0f}; \ at a price of \$$p$, \ islanders want $100 - p$ "
                  r"repairs a season", font_size=25),
            label(r"every customer goes to the cheaper yard; \ at equal prices they split evenly", font_size=25),
            label(rf"Crusoe's sign says \${p['rival']:.0f}. \ Which do you post?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(stage.box.get_center() + UP * 1.25)
        chips = VGroup(*[price_chip(r["p"], YOU) for r in p["rows"]]).arrange(RIGHT, buff=0.45).next_to(
            rules, DOWN, buff=0.5)
        crusoe = VGroup(islander("crusoe", 0.8), price_chip(p["rival"], CRUSOE, w=1.2, font_size=26)).arrange(
            RIGHT, buff=0.2).move_to(stage.box.get_corner(DR) + LEFT * 1.7 + UP * 0.75)
        ring = countdown().next_to(chips, DOWN, buff=0.45)
        with self.voiceover(
            "Before any theory, a price war to fight. You open a second boatyard on the Island, beside Crusoe's. "
            "A repair costs either yard ten dollars in timber and time. At a price of p dollars, the islanders want "
            "a hundred minus p repairs a season, and every one of them takes their boat to the cheaper yard; if "
            "the prices are equal, they split evenly. Crusoe's sign says forty dollars. You can post forty-five, "
            "forty, thirty-nine, twenty-five or ten. Which do you choose? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(rules[0]), FadeIn(crusoe))
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), run_time=1.5)
            self.play(FadeIn(rules[3]), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.2),
                      run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        heads = [r"your price", r"your customers", r"repairs", r"your profit"]
        best = p["best"]["p"]
        table = VGroup()
        cols_x = [-4.2, -1.4, 1.3, 4.0]
        for j, h in enumerate(heads):
            table.add(label(h, font_size=22, color=GREY_B).move_to(RIGHT * cols_x[j] + UP * 2.3))
        rows = VGroup()
        for i, r in enumerate(p["rows"]):
            y = 1.5 - 0.72 * i
            share = {0.0: r"none", 0.5: r"half", 1.0: r"all"}[r["share"]]
            col = E.ACCENT if r["p"] == best else (HOLD if r["profit"] == 0 else WHITE)
            rows.add(VGroup(
                label(rf"\${r['p']:.0f}", font_size=26, color=YOU).move_to(RIGHT * cols_x[0] + UP * y),
                label(share, font_size=24).move_to(RIGHT * cols_x[1] + UP * y),
                label(f"{r['q']:.0f}", font_size=24).move_to(RIGHT * cols_x[2] + UP * y),
                label(rf"\${r['profit']:,.0f}".replace(",", "{,}"), font_size=26, color=col).move_to(
                    RIGHT * cols_x[3] + UP * y),
            ))
        rule = Line(LEFT * 5.4 + UP * 1.95, RIGHT * 5.2 + UP * 1.95, color=GREY_C, stroke_width=1.5)
        frame = SurroundingRectangle(rows[2], color=E.ACCENT, stroke_width=3, buff=0.12)
        foot = VGroup(
            label(r"one dollar under Crusoe takes the whole island: \ nearly twice the profit of matching him",
                  font_size=24, color=E.ACCENT),
            label(r"but Crusoe can do the same sum", font_size=24, color=CRUSOE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is what each choice earns this season, if Crusoe stays at forty. <bookmark mark='a'/> At "
            "forty-five you serve nobody. At forty you split the island with him: thirty repairs each, at a margin of "
            "thirty dollars, nine hundred dollars of profit. <bookmark mark='b'/> At thirty-nine every islander comes "
            "to you: sixty-one repairs at twenty-nine dollars each, seventeen hundred and sixty-nine dollars. At "
            "twenty-five you still take everyone, but earn less, and at ten, your cost, you earn nothing. "
            "<bookmark mark='c'/> So one dollar under Crusoe nearly doubles what you would earn by matching him. "
            "<bookmark mark='d'/> But Crusoe can do the same sum."
        ) as vo:
            self.play(FadeIn(table), Create(rule), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(Create(frame), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def twenty(self):
        p = load("playit")
        b = load("boats")
        line = NumberLine(x_range=[0, 60, 10], length=11.0, include_numbers=True, font_size=22, color=GREY_B
                          ).move_to(UP * 0.4)
        lab = label(r"price of a repair, \ dollars", font_size=18, color=GREY_B).next_to(line, DOWN, buff=0.45)

        def pin(v, text, col, h):
            d = Dot(line.n2p(v), radius=0.09, color=col)
            t = label(text, font_size=19, color=col).move_to(line.n2p(v) + UP * h)
            end = t.get_bottom() if h > 0 else t.get_top()
            return VGroup(d, Line(d.get_center(), [d.get_center()[0], end[1], 0], color=col, stroke_width=1.5), t)

        pins = VGroup(
            pin(b["mono_P"], rf"one yard alone: \ \${b['mono_P']:.0f}", CARTEL, 1.3),
            pin(p["rival"], rf"Crusoe's sign: \ \${p['rival']:.0f}", CRUSOE, 2.1),
            pin(p["cost"], rf"the cost: \ \${p['cost']:.0f}", COMPETE, 1.3),
        )
        rows = VGroup(
            label(rf"against twenty yards all at \${p['rival']:.0f}, \ matching earns a 21st share: \ "
                  rf"\${p['split21']:.0f}", font_size=23),
            label(rf"undercutting by a dollar still takes everyone: \ \${p['undercut']:,.0f}".replace(",", "{,}"),
                  font_size=23, color=E.ACCENT),
            label(r"with one rival or twenty, \ the pull is the same: \ down", font_size=24, color=YOU),
            label(r"where does it stop? \ two answers, \ 45 years apart", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now imagine twenty yards, every one posting forty dollars. <bookmark mark='a'/> Matching them earns you "
            "a twenty-first share of the island, about eighty-six dollars a season. <bookmark mark='b'/> Undercutting "
            "by a dollar still takes every customer, and the same seventeen hundred and sixty-nine dollars. "
            "<bookmark mark='c'/> With one rival or twenty, the pull on the price is the same: down. "
            "<bookmark mark='d'/> Where does it stop? Economics gave two answers, forty-five years apart, and they "
            "contradict each other."
        ) as vo:
            self.play(Create(line), FadeIn(lab), FadeIn(pins), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
