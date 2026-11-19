from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

YOU = "#7BD88F"


def price_chip(p: float, color, w=1.35, font_size=30) -> VGroup:
    box = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(rf"\${p:.0f}", font_size=font_size, color=color).move_to(box)
    return VGroup(box, t)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ buy a boat you cannot inspect", r"Bo knows what his old boat is worth. \ You "
             r"don't. \ What do you offer?", "Chapter one. Play it: buy a boat you cannot inspect.",
             lit={1970: r"Akerlof's lemons"}, scale=("person", "market"), horizon=("a day",))
        self.rules()
        self.reveal()
        self.lesson()

    def rules(self):
        o = load("offers")
        stage = game_stage(12.0, 5.8, center=DOWN * 0.2)
        rules = VGroup(
            label(r"Bo is selling one of his old boats; \ he knows how sound it is, \ you can only look at the paint",
                  font_size=24),
            label(r"to Bo, \ the boat is worth anything from \$0 to \$100, \ every value equally likely", font_size=24),
            label(r"to you, \ whatever it is worth to Bo, \ plus \$30: \ you need a boat, \ he doesn't", font_size=24),
            label(r"you make one offer; \ Bo sells if it beats what the boat is worth to him", font_size=24),
            label(r"which offer do you make?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to(stage.box.get_center() + UP * 1.05)
        chips = VGroup(*[price_chip(r["p"], YOU) for r in o["rows"]]).arrange(RIGHT, buff=0.45).next_to(
            rules, DOWN, buff=0.4)
        bo = islander("bo", 0.8).move_to(stage.box.get_corner(DR) + LEFT * 0.9 + UP * 0.8)
        ring = countdown().next_to(chips, DOWN, buff=0.35)
        with self.voiceover(
            "Before the theory, a purchase. Bo is selling one of his old boats. He has sailed it for years and knows "
            "exactly how sound it is; you can only look at the paint. To Bo, the boat could be worth anything from "
            "nothing to a hundred dollars, every value equally likely as far as you can tell. To you it is worth "
            "whatever it is worth to Bo, plus thirty dollars, because you need a boat and he doesn't. You make one "
            "offer, and Bo sells if your offer beats what the boat is worth to him. You can offer eighty, sixty, "
            "forty, thirty or twenty dollars. Which do you choose? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(rules[0]), FadeIn(bo))
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), run_time=1.5)
            self.play(FadeIn(rules[3]), FadeIn(rules[4]),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.2), run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        o = load("offers")
        heads = [r"your offer", r"Bo sells", r"the boats you get, \\ on average, \ to you", r"you gain \\ per boat",
                 r"you gain, \\ on average"]
        xs = [-5.0, -2.6, 0.2, 3.0, 5.4]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.45) for h, x in zip(heads, xs)])
        rows = VGroup()
        best = max(o["rows"], key=lambda r: r["expected_gain"])["p"]
        for i, r in enumerate(o["rows"]):
            y = 1.45 - 0.7 * i
            g = r["gain_if_sold"]
            col = E.ACCENT if r["p"] == best else (HOLD if g < 0 else WHITE)
            rows.add(VGroup(
                label(rf"\${r['p']:.0f}", font_size=26, color=YOU).move_to(RIGHT * xs[0] + UP * y),
                label(rf"{100 * r['accept']:.0f}\% of the time", font_size=21).move_to(RIGHT * xs[1] + UP * y),
                label(rf"\${r['value']:.0f}", font_size=24).move_to(RIGHT * xs[2] + UP * y),
                label((r"$-$" if g < 0 else "") + rf"\${abs(g):.0f}", font_size=24,
                      color=HOLD if g < 0 else WHITE).move_to(RIGHT * xs[3] + UP * y),
                label((r"$-$" if r["expected_gain"] < 0 else "") + rf"\${abs(r['expected_gain']):.2f}", font_size=24,
                      color=col).move_to(RIGHT * xs[4] + UP * y),
            ))
        rule = Line(LEFT * 6.0 + UP * 1.95, RIGHT * 6.3 + UP * 1.95, color=GREY_C, stroke_width=1.5)
        frame = SurroundingRectangle(rows[[r["p"] for r in o["rows"]].index(best)], color=E.ACCENT, stroke_width=3,
                                     buff=0.1)
        foot = label(r"Bo only accepts offers above what his boat is worth: \ the higher you go, \ the worse the boats "
                     r"that join", font_size=22, color=LEMON).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is what each offer brings you. <bookmark mark='a'/> Offer eighty, and Bo sells whenever his boat is "
            "worth less than eighty to him: eight times in ten. But then the boat you get is worth forty to him on "
            "average, so seventy to you, and you lose ten dollars a boat. <bookmark mark='b'/> At sixty you break "
            "even: the boats that sell are worth thirty to Bo, sixty to you. <bookmark mark='c'/> At forty, thirty or "
            "twenty you gain on every boat you buy, but you buy less often. The best you can do is thirty dollars, "
            "which gains four dollars fifty on average. <bookmark mark='d'/> Every dollar you add to your offer "
            "brings in boats Bo values more, but also tells you nothing about which boat you are getting."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
            self.play(Create(frame))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        o = load("offers")
        ps = np.array(o["ps"])
        ax = plane([0, 100], [-22, 8], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 20, 30, 40, 60, 80, 100], yticks=[-20, -10, 0, 5], xlabel=r"your offer, \ \$",
                   ylabel=r"your average gain, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        curve = path(ax, ps, o["curve"], color=YOU, width=3.5)
        zero = DashedLine(a.c2p(0, 0), a.c2p(100, 0), color=GREY_B, stroke_width=1.5)
        best = Dot(a.c2p(o["best"], o["best_gain"]), radius=0.09, color=E.ACCENT)
        side = VGroup(
            label(r"if you could inspect the boat, \\ you would buy every one, \\ and gain \$30 each time", font_size=21,
                  color=GOOD),
            label(rf"because you can't, \\ your best offer is \${o['best']:.0f}, \\ and most boats stay with Bo",
                  font_size=21, color=E.ACCENT),
            label(r"every boat is worth more to you than to Bo: \\ each that stays unsold is a trade lost", font_size=21,
                  color=LOSS),
            label(r"and with many buyers bidding, \\ where does the price settle? \\ the next chapter", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Draw your average gain against your offer. <bookmark mark='a'/> If you could inspect the boat, you "
            "would buy every one at what it is worth to Bo, and gain thirty dollars each time. "
            "<bookmark mark='b'/> Because you can't, your best offer is thirty dollars, and seven boats in ten stay "
            "with Bo. <bookmark mark='c'/> Yet every boat is worth more to you than to him, so each one that stays "
            "unsold is a trade that should have happened and didn't. <bookmark mark='d'/> And when many buyers bid "
            "against each other, where does the price settle? That is Akerlof's question."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), Create(curve), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(best, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
