from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403

LETTERS = "ABCDE"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F", "#C9A0FF")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: \ how much should the island save?", r"Which saving rate leaves the islanders the "
             r"most to consume, \ a century from now?", "Chapter four. Play it: how much should the island save?",
             lit={1961: r"Phelps's fable"}, scale=("household", "nation"), horizon=("a century",))
        self.guess()
        self.reveal()
        self.golden()
        self.jump()

    def guess(self):
        p = load("playit")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        head = label(r"the island saves 15\%. \ Choose a new saving rate for the next hundred years.", font_size=23,
                     color=GREY_A).move_to(stage.box.get_top() + DOWN * 0.55)
        q = label(r"which leaves the most consumption per worker in year 100?", font_size=26,
                  color=E.ACCENT).next_to(head, DOWN, buff=0.4)
        chips = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {100 * s:.0f}\%", font_size=28, color=c))
                         for i, (s, c) in enumerate(zip(p["options"], CHIP))]).arrange(RIGHT, buff=0.35)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(q, DOWN, buff=0.7)
        hint = label(r"more saving means more boats and nets, \ but less to eat now", font_size=21,
                     color=GREY_B).next_to(chips, DOWN, buff=0.6)
        ring = countdown().next_to(hint, DOWN, buff=0.35)
        with self.voiceover(
            "Your turn. The island saves fifteen percent of its output and has settled at that rate's steady state. "
            "<bookmark mark='a'/> You may choose a new saving rate, to hold for the next hundred years. Which leaves "
            "the islanders the most to consume, per worker, in year one hundred? <bookmark mark='b'/> A, ten "
            "percent; B, twenty; C, thirty-three; D, fifty; or E, seventy. <bookmark mark='c'/> Remember that every "
            "fish saved to build a boat is a fish not eaten. Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(hint), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        base = np.array(p["base"])
        t = np.arange(len(base))
        ax = plane([0, 100], [0.3, 1.3], center=DOWN * 0.45 + LEFT * 1.2, x_length=9.4, y_length=5.2,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[0.4, 0.6, 0.8, 1.0, 1.2],
                   ylabel=r"consumption per worker, \ relative to staying at 15\%", xlabel=r"years",
                   yfmt=lambda v: f"{v:.1f}", font_size=16)
        one = DashedLine(ax.ax.c2p(0, 1), ax.ax.c2p(100, 1), color=GREY_B, stroke_width=2)
        lines, ends = VGroup(), VGroup()
        for i, (s, c) in enumerate(zip(p["options"], CHIP)):
            r = p["runs"][f"{s:.2f}"]
            rel = np.array(r["c"]) / base
            lines.add(path(ax, t, rel, color=c, width=4 if f"{s:.2f}" == p["best"] else 3, smooth=False))
            ends.add(label(rf"{LETTERS[i]}: \ {100 * s:.0f}\% \ \ {100 * r['vs_base_end']:+.0f}\%".replace("-", "{-}"),
                           font_size=18, color=c).next_to(ax.ax.c2p(100, rel[-1]), RIGHT, buff=0.12))
        ends.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(ax.ax.c2p(100, 0.8), RIGHT, buff=0.25)
        best = p["runs"][p["best"]]
        r50 = p["runs"]["0.50"]
        with self.voiceover(
            "Here are the hundred years, computed. Each line is consumption per worker under a new saving rate, "
            "relative to staying at fifteen percent. <bookmark mark='a'/> Every higher rate starts with a cut: the "
            "islanders eat less to build more. Save seventy percent and consumption falls by more than half at once. "
            "<bookmark mark='b'/> Then the boats and nets pay off. Thirty-three percent overtakes the old rate after "
            f"{best['cross']} years, and ends about {100 * best['vs_base_end']:.0f} percent above it. "
            "<bookmark mark='c'/> Fifty percent takes "
            f"{r50['cross']} years to catch up and ends only {100 * r50['vs_base_end']:.0f} percent above, and seventy "
            "percent never catches up at all: the "
            "island is building more capital than is worth having. <bookmark mark='d'/> If you chose C, thirty-three "
            "percent, you found the best rate in the long run. It has a name."
        ) as vo:
            self.play(FadeIn(ax), Create(one))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(ends[2]), Indicate(lines[2], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(ends[3]), FadeIn(ends[4]), FadeIn(ends[0]), FadeIn(ends[1]))
            vo.wait_until("d")
            self.play(Indicate(ends[2], color=WHITE))
        self.clear_scene()

    def golden(self):
        p = load("playit")
        g = p["golden"]
        ax = plane([0, 1], [0, 1.6], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.5, 1.0, 1.5],
                   xlabel=r"saving rate $s$", ylabel=r"steady-state consumption $c^\ast$",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=16)
        curve = path(ax, g["s"], g["c"], color=CONS, width=4)
        top = Dot(ax.ax.c2p(g["s_gold"], g["c_gold"]), radius=0.1, color=WHITE)
        drop = DashedLine(ax.ax.c2p(g["s_gold"], 0), ax.ax.c2p(g["s_gold"], g["c_gold"]), color=GREY_B)
        side = VGroup(
            MathTex(r"c^\ast = (1-s)\,y^\ast = f(k^\ast) - (n+g+\delta)\,k^\ast", font_size=32),
            MathTex(r"\frac{dc^\ast}{dk^\ast} = 0 \;\Rightarrow\; f'(k_{\text{gold}}) = n + g + \delta", font_size=32,
                    color=E.ACCENT),
            MathTex(r"\text{Cobb-Douglas:}\quad s_{\text{gold}} = \alpha", font_size=34),
            label(r"Edmund Phelps, \ 1961: \ \emph{A Fable for Growthmen}", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        tag = published_tag(r"Phelps, AER 51(4) (1961): \ 638--643", corner=DR, font_size=13)
        warn = label(r"above it: \ dynamically inefficient \ (everyone could eat more, \ now and later)",
                     font_size=20, color=HOLD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "It is the golden rule of accumulation, so named by Edmund Phelps in 1961, in a paper subtitled a fable "
            "for growthmen. <bookmark mark='a'/> In the steady state, consumption is output less what must be "
            "invested to stay there. <bookmark mark='b'/> Plot it against the saving rate: zero saving leaves no "
            "capital and little output; saving everything leaves nothing to eat. <bookmark mark='c'/> In between is "
            "a peak, where an extra unit of capital produces exactly what it costs to maintain: the marginal product "
            "of capital equals n plus g plus delta. <bookmark mark='d'/> With Cobb-Douglas production that happens "
            "when the saving rate equals capital's share, a third. <bookmark mark='e'/> Saving more than that is "
            "worse than wasteful. An economy above the golden rule could consume more now and in every future year, "
            "just by saving less. Economists call it dynamically inefficient."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(top), Create(drop), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(warn))
        self.clear_scene()

    def jump(self):
        p = load("playit")
        j = p["jump"]
        yrs = np.arange(len(j["y"]))
        top = plane([0, 80], [0, 1.6], center=UP * 1.6 + LEFT * 1.4, x_length=8.8, y_length=2.4,
                    xticks=[0, 20, 40, 60, 80], yticks=[0, 0.5, 1.0, 1.5],
                    ylabel=r"log income per worker", font_size=14, yfmt=lambda v: f"{v:.1f}")
        y0 = np.log(j["y"][0])
        up = path(top, yrs, np.log(j["y"]) - y0, color=OUTPUT, width=4, smooth=False)
        stay = path(top, yrs, np.log(j["base"]) - y0, color=GREY_B, width=2.5, smooth=False)
        bot = plane([0, 80], [0, 0.05], center=DOWN * 2.05 + LEFT * 1.4, x_length=8.8, y_length=2.1,
                    xticks=[0, 20, 40, 60, 80], yticks=[0, 0.02, 0.04], xlabel=r"years",
                    ylabel=r"growth a year", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        gl = path(bot, yrs[1:], j["growth"], color=E.ACCENT, width=4, smooth=False)
        side = VGroup(
            label(rf"year {j['t0']}: \ saving {100 * j['lo']:.0f}\% $\to$ {100 * j['hi']:.0f}\%", font_size=21,
                  color=SAVE),
            label(rf"growth peaks at {pc(j['peak_growth'])}", font_size=21, color=E.ACCENT),
            label(rf"half the gain within {j['half']} years", font_size=21, color=GREY_A),
            label(rf"then back to {pc(j['long_growth'], 0)}", font_size=21, color=E.ACCENT),
            label(rf"income for good: \ {100 * j['level_gain']:+.0f}\%", font_size=23, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "One more experiment shows what saving can and cannot do. <bookmark mark='a'/> In year "
            f"{j['t0']} the island doubles its saving rate, from {100 * j['lo']:.0f} to {100 * j['hi']:.0f} percent, "
            "and keeps it there. <bookmark mark='b'/> Growth jumps: income per worker grows by about "
            f"{100 * j['peak_growth']:.1f} percent in the first year, more than twice its usual rate. "
            f"<bookmark mark='c'/> Half of the eventual gain arrives within {j['half']} years. "
            "<bookmark mark='d'/> Then growth slides back to two percent, technology's rate, where it stays. "
            f"<bookmark mark='e'/> What is left is a level: income about {100 * j['level_gain']:.0f} percent higher "
            "than it would have been, for ever. A country can save its way to being richer. It cannot save its way "
            "to growing faster for ever."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), Create(stay))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(up), Create(gl), run_time=3, rate_func=linear)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(up, color=WHITE))
        self.clear_scene()
