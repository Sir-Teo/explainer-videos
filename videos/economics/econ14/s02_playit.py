from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403

YOU = "#7BD88F"


def chip(text, color, w=1.6, font_size=26) -> VGroup:
    box = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(text, font_size=font_size, color=color).move_to(box)
    return VGroup(box, t)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ write Friday's contract", r"You can see the harvest, \ not the work. \ What share "
             r"of the harvest do you give Friday?", "Chapter one. Play it: write Friday's contract.",
             lit={1987: r"Holmström and Milgrom"}, scale=("person", "firm"), horizon=("a season",))
        self.rules()
        self.reveal()
        self.curve()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.0, 5.8, center=DOWN * 0.2)
        rules = VGroup(
            label(r"you are Crusoe, \ and you hire Friday to work your coconut grove", font_size=24),
            label(rf"a day's harvest is Friday's effort, \ in baskets, \ plus luck: \ rain or wind, \ give or take "
                  rf"{p['sigma']:.0f} baskets", font_size=23),
            label(r"effort is tiring: \ the 10th basket of effort costs Friday a basket's worth, \ the 20th two",
                  font_size=23),
            label(r"Friday dislikes risk, \ and has other work worth nothing extra: \ you must make the job worth taking",
                  font_size=23),
            label(r"you pay a fixed amount, \ plus a share of the harvest: \ which share?", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to(stage.box.get_center() + UP * 1.0)
        chips = VGroup(*[chip(t_, YOU) for t_ in (r"none", r"a third", r"two-thirds", r"all of it")]).arrange(
            RIGHT, buff=0.45).next_to(rules, DOWN, buff=0.4)
        who = pair(height=0.7).move_to(stage.box.get_corner(DR) + LEFT * 1.3 + UP * 0.75)
        ring = countdown().next_to(chips, DOWN, buff=0.35)
        with self.voiceover(
            "This time you are the employer. You are Crusoe, and you hire Friday to work your coconut grove. A day's "
            "harvest is Friday's effort, measured in baskets, plus luck: rain or wind can add or take away five "
            "baskets or so. Effort is tiring, more so the more there is of it. Friday dislikes risk, and could do "
            "other work, so you must make the job worth taking. You can't see how hard Friday works, only the "
            "harvest. You pay a fixed amount, plus a share of the harvest. Which share do you offer: none of it, a "
            "third, two-thirds, or all of it? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(rules[0]), FadeIn(who))
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), run_time=1.5)
            self.play(FadeIn(rules[3]), FadeIn(rules[4]),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.2), run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        heads = [r"Friday's share", r"fixed pay", r"Friday's effort, \\ baskets a day", r"what the risk \\ costs Friday",
                 r"your profit, \\ baskets a day"]
        xs = [-5.0, -2.5, 0.2, 3.0, 5.4]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.4) for h, x in zip(heads, xs)])
        names = [r"none", r"a third", r"two-thirds", r"all of it"]
        best = max(range(len(p["rows"])), key=lambda k: p["rows"][k]["profit"])
        rows = VGroup()
        for i, r in enumerate(p["rows"]):
            y = 1.35 - 0.8 * i
            fixed = r["fixed"]
            ft = (r"$-$" if fixed < -1e-9 else "") + rf"{abs(fixed):.2f}"
            rows.add(VGroup(
                label(names[i], font_size=24, color=YOU).move_to(RIGHT * xs[0] + UP * y),
                label(ft, font_size=23, color=PAY).move_to(RIGHT * xs[1] + UP * y),
                label(rf"{r['effort']:.2f}", font_size=23, color=EFFORT).move_to(RIGHT * xs[2] + UP * y),
                label(rf"{r['risk']:.2f}", font_size=23, color=RISK).move_to(RIGHT * xs[3] + UP * y),
                label(rf"{r['profit']:.2f}", font_size=25, color=E.ACCENT if i == best else WHITE).move_to(
                    RIGHT * xs[4] + UP * y),
            ))
        rule = Line(LEFT * 6.0 + UP * 1.9, RIGHT * 6.3 + UP * 1.9, color=GREY_C, stroke_width=1.5)
        frame = SurroundingRectangle(rows[best], color=E.ACCENT, stroke_width=3, buff=0.18)
        foot = VGroup(
            label(r"a negative fixed pay is a rent: \ Friday pays for the right to keep a share", font_size=21,
                  color=PAY),
            label(rf"if you could see effort, \ you'd ask for {p['fb_effort']:.0f} baskets and earn {p['fb_profit']:.2f}: "
                  r"\ not seeing costs you the difference", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is what each share does, with the fixed pay set so that Friday just accepts. "
            "<bookmark mark='a'/> Give Friday none of the harvest, and Friday has no reason to make an effort: you "
            "get nothing. <bookmark mark='b'/> Give Friday all of it, and Friday works as hard as if the grove were "
            "theirs, ten baskets a day. But all the luck now falls on Friday, who dislikes it, so you must lower the "
            "rent to two and a half baskets to keep Friday on, and you earn two and a half. "
            "<bookmark mark='c'/> A third brings three and a third baskets of effort, and also earns you two and a "
            "half. <bookmark mark='d'/> Two-thirds is best: six and two-thirds baskets of effort, and three and a third "
            "baskets of profit a day. <bookmark mark='e'/> A negative fixed pay is a rent: Friday pays you for the "
            "right to a share. And if you could see effort, you would simply ask for ten baskets and earn five; not "
            "seeing costs you the difference."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), Create(frame))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def curve(self):
        p = load("playit")
        bs = np.array(p["betas"])
        ax = plane([0, 1], [0, 5.5], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 1 / 3, 2 / 3, 1], yticks=[0, 2.5, p["best_profit"], 5], xlabel=r"Friday's share of the "
                   r"harvest", ylabel=r"your profit, \ baskets a day", font_size=16,
                   xfmt=lambda v: {0: "0", 1: "1"}.get(round(v, 3), f"{v:.2f}"), yfmt=lambda v: f"{v:.2f}")
        a = ax.ax
        c = path(ax, bs, p["profit_curve"], color=YOU, width=3.5)
        fb = DashedLine(a.c2p(0, p["fb_profit"]), a.c2p(1, p["fb_profit"]), color=GREY_B, stroke_width=1.5)
        fbl = label(r"if effort could be seen", font_size=15, color=GREY_B).next_to(a.c2p(0.05, p["fb_profit"]), UP,
                                                                                   buff=0.08, aligned_edge=LEFT)
        best = Dot(a.c2p(p["beta_star"], p["best_profit"]), radius=0.09, color=E.ACCENT)
        side = VGroup(
            label(r"too small a share: \ Friday barely tries", font_size=21, color=EFFORT),
            label(r"too large: \ Friday carries all the luck, \\ and must be paid to bear it", font_size=21,
                  color=RISK),
            label(rf"the best share, \ {p['beta_star']:.2f}, \ balances the two", font_size=22, color=E.ACCENT),
            label(r"the gap to the dashed line \\ is the price of not seeing effort", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Draw your profit against Friday's share. <bookmark mark='a'/> With too small a share, Friday barely tries. "
            "<bookmark mark='b'/> With too large a one, Friday carries all the luck, and must be paid to bear it. "
            "<bookmark mark='c'/> The best share, two-thirds, balances the two. <bookmark mark='d'/> And the gap "
            "between the top of the curve and the dashed line is what it costs not to see effort. The rest of this "
            "part is about that gap: what makes it larger, and what can close it."
        ) as vo:
            self.play(FadeIn(ax), Create(c), Create(fb), FadeIn(fbl), FadeIn(tag))
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "c":
                    self.play(FadeIn(best, scale=1.5), run_time=0.5)
        self.clear_scene()
