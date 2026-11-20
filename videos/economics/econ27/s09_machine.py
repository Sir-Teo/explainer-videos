from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


def tank(width: float, height: float, color) -> VGroup:
    """An open-topped tank: three sides of a rectangle."""
    w, h = width / 2, height / 2
    return VGroup(Line([-w, h, 0], [-w, -h, 0]), Line([-w, -h, 0], [w, -h, 0]), Line([w, -h, 0], [w, h, 0])).set_stroke(
        color, 3)


class Machine(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Phillips's machine", r"Can you build the economy out of water?", "Chapter eight. Phillips's "
             "machine.", lit={1949: r"the Phillips machine"}, scale=("nation",), horizon=("a year",))
        self.history()
        self.flows()
        self.lessons()

    def history(self):
        rows = VGroup(
            label(r"Bill Phillips, \ a New Zealand engineer studying at the LSE, \ 1949", font_size=24,
                  color=E.ACCENT),
            label(r"the first machine built in a garage in Croydon", font_size=23, color=GREY_A),
            label(r"income is water; \ spending, \ saving, \ taxes and imports are flows through valves",
                  font_size=23, color=WATER),
            label(r"about fourteen were built, \ for universities and central banks", font_size=23, color=GREY_A),
            label(r"the same Phillips drew the Phillips curve, \ in 1958 \ (Part 28)", font_size=23, color=RATE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"the Science Museum Group and Engineering New Zealand's histories of the machine",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1949, a New Zealand engineer studying economics at the London School of Economics, Bill Phillips, "
            "built the Keynesian economy out of water. <bookmark mark='a'/> The first machine was built in a garage "
            "in Croydon. <bookmark mark='b'/> In it, income is water pumped to the top of the machine. It flows down "
            "through pipes and valves: some to consumption, some leaking away into saving, taxes and imports, while "
            "investment and government spending are pumped back in. <bookmark mark='c'/> About fourteen were "
            "built, for universities and central banks. <bookmark mark='d'/> Nine years later, the same Phillips "
            "drew the curve that bears his name, the subject of Part twenty-eight."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def flows(self):
        M = load("moniac")
        Y = np.array(M["Y"])
        steps = len(Y)
        lo, hi = 500.0, 850.0
        main = tank(2.6, 3.6, WATER).move_to(LEFT * 3.9 + DOWN * 0.4)
        fill = ValueTracker(0.0)

        def level(v):
            return float(np.clip((v - lo) / (hi - lo), 0.02, 1.0))

        water = always_redraw(lambda: Rectangle(width=2.5, height=3.55 * level(fill.get_value()), stroke_width=0,
                                                fill_color=WATER, fill_opacity=0.7).align_to(main, DOWN).shift(
            UP * 0.03).set_x(main.get_x()))
        name = label(r"income", font_size=22, color=WATER).next_to(main, UP, buff=0.15)
        num = always_redraw(lambda: DecimalNumber(fill.get_value(), num_decimal_places=0, font_size=30,
                                                  color=WHITE).move_to(main.get_center()))
        out = VGroup(
            label(rf"spending: \ {M['b']} of disposable income", font_size=19, color=SPEND),
            label(rf"leaks: \ saving, \ and taxes at {100 * M['tax']:.0f}\%", font_size=19, color=SAVE),
            label(rf"pumped back in: \ investment {M['I']:.0f}, \ government {M['G'][0]:.0f}", font_size=19,
                  color=GOV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 3.6 + DOWN * 3.1)
        arrows = VGroup(
            Arrow(main.get_right() + DOWN * 1.2, main.get_right() + RIGHT * 1.3 + DOWN * 1.2, color=SAVE,
                  stroke_width=4, buff=0),
            Arrow(main.get_left() + LEFT * 1.0 + UP * 1.6, main.get_left() + UP * 1.6, color=GOV, stroke_width=4,
                  buff=0),
        )
        ax = plane([0, steps], [lo, hi], center=RIGHT * 2.6 + DOWN * 0.2, x_length=6.0, y_length=4.4,
                   xticks=[0, 20, 40, 60], yticks=[500, 600, 700, 800], xlabel=r"time", ylabel=r"income",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        full = path(ax, np.arange(steps), Y, color=WATER, width=3, smooth=False)
        trace = full.copy()
        tr = ValueTracker(0.0)
        trace.add_updater(lambda m: m.pointwise_become_partial(full, 0, max(tr.get_value(), 1e-3)))
        endline = seg(ax, 0, M["end"], steps, M["end"], color=OUTPUT, width=2, dashed=True)
        side = VGroup(
            label(rf"government spending rises by {M['dG']:.0f}", font_size=20, color=GOV),
            label(rf"the level climbs from {M['start']:.0f} to {M['end']:.0f}: \ a multiplier of "
                  rf"{M['multiplier']:.2f}", font_size=20, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, UP, buff=0.2).shift(RIGHT * 0.3)
        tag = island_tag(corner=DR, font_size=14)
        fill.set_value(Y[0])
        with self.voiceover(
            "Agora can run a small version. <bookmark mark='a'/> The level of water in the tank is income. Each "
            f"period, households spend {M['b']} of what is left after taxes, which flows round again as someone "
            f"else's income. Saving and taxes at {100 * M['tax']:.0f} percent leak out. Investment and the "
            "government's purchases are pumped back in. <bookmark mark='b'/> The tank settles where the leaks "
            f"exactly match what is pumped in: at {M['start']:.0f}. <bookmark mark='c'/> Now open the government's "
            f"valve, {M['dG']:.0f} more each period. Watch the level climb, quickly at first, then more slowly, "
            f"<bookmark mark='d'/> until it settles at {M['end']:.0f}. The multiplier is "
            f"{M['multiplier']:.2f}, smaller than the cross's two and a half, because taxes now leak too. And it "
            "takes time: the water has to go round."
        ) as vo:
            self.add(water, num)
            self.play(FadeIn(main), FadeIn(name), FadeIn(ax), FadeIn(tag), run_time=1)
            vo.wait_until("a")
            self.play(FadeIn(out), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
            vo.wait_until("b")
            self.add(trace)
            self.play(tr.animate.set_value(M["shock_at"] / (steps - 1)), run_time=1.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), Create(endline))
            self.play(tr.animate.set_value(1.0), fill.animate.set_value(Y[-1]), run_time=6, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        trace.clear_updaters()
        self.clear_scene()

    def lessons(self):
        rows = VGroup(
            label(r"what a hydraulic model gets right", font_size=28, color=E.ACCENT),
            label(r"stocks and flows must add up: \ every dollar spent is someone's income", font_size=23,
                  color=WATER),
            label(r"adjustment takes time, \ and leaks set the multiplier", font_size=23, color=SAVE),
            label(r"what it leaves out", font_size=26, color=HOLD),
            label(r"expectations: \ water does not anticipate the valve being opened", font_size=23, color=GREY_A),
            label(r"prices: \ in the machine, \ nothing gets cheaper when demand is short", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "What does a model made of water get right? <bookmark mark='a'/> That stocks and flows must add up: "
            "every dollar spent is someone's income, and nothing disappears. <bookmark mark='b'/> That adjustment "
            "takes time, and that the leaks set the size of the multiplier. <bookmark mark='c'/> And what does it "
            "leave out? <bookmark mark='d'/> Expectations: water does not anticipate that the valve will be opened "
            "next year, but people do, and Parts twenty-eight and twenty-nine show why that matters. "
            "<bookmark mark='e'/> And "
            "prices. In the machine, nothing gets cheaper when demand is short. In a real economy it does, slowly. "
            "That is the next question."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
