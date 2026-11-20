from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403

LETTERS = "ABCDE"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F", "#C9A0FF")
SAY = ("one hour", "six minutes", "thirty-six seconds", "three and a half seconds", "a third of a second")
SHOW = (r"1 hour", r"6 minutes", r"36 seconds", r"3.6 seconds", r"0.36 seconds")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ how much work buys an hour of light?", r"In 1800 a tallow candle's light cost 5.4 "
             r"hours of work. \ What did the same light cost in 1992?", "Chapter one. Play it: how much work buys an "
             "hour of light?", lit={1800: r"the tallow candle", 1992: r"?"}, scale=("household",),
             horizon=("a century",))
        self.guess()
        self.reveal()
        self.fact()

    def guess(self):
        p = load("playit")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        head = label(r"1{,}000 lumen-hours: \ 5.4 hours of work in 1800, \ with a tallow candle", font_size=23,
                     color=GREY_A).move_to(stage.box.get_top() + DOWN * 0.55)
        q = label(r"how much work bought the same light in 1992?", font_size=27, color=E.ACCENT).next_to(
            head, DOWN, buff=0.4)
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {SHOW[i]}", font_size=22, color=c))
                         for i, c in enumerate(CHIP)]).arrange(RIGHT, buff=0.25)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(q, DOWN, buff=0.7)
        ring = countdown().next_to(chips, DOWN, buff=0.6)
        with self.voiceover(
            "Your turn. In 1800, a thousand lumen-hours of light from tallow candles cost an American labourer about "
            f"{p['start']:.1f} hours of work. <bookmark mark='a'/> What did the same light cost in 1992? "
            f"<bookmark mark='b'/> A, {SAY[0]}; B, {SAY[1]}; C, {SAY[2]}; D, {SAY[3]}; or E, {SAY[4]}. "
            "<bookmark mark='c'/> Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        l_ = load("light")
        p = load("playit")
        ax = plane([1790, 2000], [np.log10(0.00005), np.log10(30)], center=DOWN * 0.45 + LEFT * 1.4, x_length=8.8,
                   y_length=5.2, xticks=[1800, 1850, 1900, 1950, 2000],
                   yticks=[np.log10(v) for v in (0.0001, 0.001, 0.01, 0.1, 1, 10)],
                   ylabel=r"hours of work per 1{,}000 lumen-hours \ (log)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=15)
        colors = {"candle": LIGHT, "lamp": "#E8A0B4", "town gas": "#9FB8F2", "kerosene lamp": "#F29E8E",
                  "electric lamp": "#7BD88F"}
        dots = VGroup()
        for r in l_["rows"]:
            if r["year"] is None or r["year"] < 1800:
                continue
            dots.add(Dot(ax.ax.c2p(r["year"], np.log10(r["hours"])), radius=0.06, color=colors[r["device"]]))
        front = path(ax, l_["frontier_years"], [np.log10(v) for v in l_["frontier"]], color=WHITE, width=2.5,
                     smooth=False)
        leg = VGroup(*[VGroup(Dot(radius=0.06, color=c), label(k, font_size=15, color=c)).arrange(RIGHT, buff=0.08)
                       for k, c in colors.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(
            ax.ax.c2p(1965, np.log10(5)))
        side = VGroup(
            label(rf"1800, \ tallow candle: \ {l_['tallow_1800']:.2f} hours", font_size=20, color=LIGHT),
            label(rf"1883, \ Edison's lamp: \ {l_['edison_1883']:.2f}", font_size=20, color="#7BD88F"),
            label(rf"1992, \ compact fluorescent: \\ {l_['cfl_1992']:.6f} hours, \ {l_['seconds_1992']:.2f} seconds",
                  font_size=20, color="#7BD88F"),
            label(rf"about {commas(round(l_['ratio_1800_1992'], -3))} times cheaper; \\ "
                  rf"{-100 * l_['rate_1800_1992']:.1f}\% a year for 192 years", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(tables.NORDHAUS_LIGHT.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Here is Nordhaus's answer, every lamp he priced from 1800 on, on a log scale. "
            f"<bookmark mark='a'/> The tallow candle, {l_['tallow_1800']:.2f} hours. Whale oil, town gas and kerosene "
            "brought it down. <bookmark mark='b'/> Edison's carbon lamp of 1883 cost about three quarters of an "
            "hour. <bookmark mark='c'/> And in 1992, with a compact fluorescent bulb, the same light cost about "
            f"{l_['seconds_1992']:.2f} seconds of work. If you chose E, you were right. <bookmark mark='d'/> That is a "
            f"fall of about {round(l_['ratio_1800_1992'], -3):,.0f} times, {-100 * l_['rate_1800_1992']:.1f} percent a "
            "year for nearly two centuries, while the real wage rose only a fraction as much. Almost all of it came "
            "from ideas."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=3)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(front), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        del p
        self.clear_scene()

    def fact(self):
        l_ = load("light")
        f = next(x for x in facts.FACTS if x.key == "price_of_light")
        guess_m = label(r"your choice: \\ A to E", font_size=19, color=E.ACCENT)
        data_m = label(rf"5.37 hours in 1800; \\ 0.43 seconds in 1992: \\ about {commas(round(l_['ratio_1800_1992'], -3))}"
                       r" times cheaper", font_size=19, color=WHITE)
        agora_m = label(r"ideas, \ used by all at once, \\ accumulate: \ the cost \\ keeps falling \ (chapter 4)",
                        font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"your guess", guess_m), (r"the data", data_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22).move_to(UP * 0.1)
        with self.voiceover(
            "That goes on the series' list of facts. <bookmark mark='a'/> The labour cost of light fell by a factor "
            "of hundreds of thousands since antiquity, and by tens of thousands since 1800. Agora's column is filled "
            "by the model this part builds: ideas, which everyone can use at once, accumulate, and the cost of "
            "everything made with them keeps falling."
        ) as vo:
            self.play(FadeIn(fc))
            vo.wait_until("a")
            self.play(Indicate(agora_m, color=WHITE))
        self.clear_scene()
