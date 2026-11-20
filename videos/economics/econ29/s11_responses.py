from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Responses(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The model beside the data", r"What does a technology shock do, \ and does the model's cycle "
             r"look like America's?", "Chapter nine. The model beside the data.", lit={1986: r"Prescott"},
             scale=("nation",), horizon=("a quarter", "a decade"))
        self.irf()
        self.why()
        self.scorecard()

    def irf(self):
        R = load("rbc")["irf"]
        q = np.arange(len(R["y"]))
        left = plane([0, 40], [-0.3, 2.2], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                     xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel=r"quarters after the shock",
                     ylabel=r"\% from steady state", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                     font_size=14)
        right = plane([0, 40], [-1, 7], center=RIGHT * 3.2 + DOWN * 0.4, x_length=5.0, y_length=4.4,
                      xticks=[0, 10, 20, 30, 40], yticks=[0, 2, 4, 6], xlabel=r"quarters after the shock",
                      ylabel=r"\% from steady state", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                      font_size=14)
        z0 = seg(left, 0, 0, 40, 0, GREY_D, 1.2)
        z1 = seg(right, 0, 0, 40, 0, GREY_D, 1.2)
        spec = (("z", TECH, r"technology"), ("y", OUTPUT, r"output"), ("n", HOURS, r"hours"),
                ("c", CONS, r"consumption \ (= the wage)"))
        curves = {k: path(left, q, R[k], c, 3, yr=(-0.3, 2.2)) for k, c, _ in spec}
        names = {k: label(n_, font_size=17, color=c) for k, c, n_ in spec}
        names["y"].next_to(left.ax.c2p(1, R["y"][1]), UR, buff=0.05)
        names["z"].next_to(left.ax.c2p(16, R["z"][16]), UP, buff=0.08)
        names["n"].next_to(left.ax.c2p(4, R["n"][4]), DL, buff=0.05).shift(RIGHT * 0.6)
        names["c"].next_to(left.ax.c2p(22, R["c"][22]), UP, buff=0.1)
        inv = path(right, q, R["i"], INVEST, 3, yr=(-1, 7))
        inv_n = label(r"investment", font_size=17, color=INVEST).next_to(right.ax.c2p(4, R["i"][4]), UR, buff=0.1)
        head = label(r"a 1\% improvement in technology, \ then fading at 5\% a quarter", font_size=22,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the model's answer. <bookmark mark='a'/> Technology on the Island improves by one percent, and the "
            "improvement fades by five percent a quarter. <bookmark mark='b'/> Output jumps by "
            f"{R['y'][0]:.1f} percent, almost twice the shock, because people also work more: <bookmark mark='c'/> "
            f"hours rise {R['n'][0]:.1f} percent. <bookmark mark='d'/> Consumption rises only "
            f"{R['c'][0]:.2f} percent at first, and keeps rising for three years, while the wage moves with it "
            f"exactly. <bookmark mark='e'/> Investment takes the windfall: up {R['i'][0]:.1f} percent on impact. "
            "Every series moves together, and in the right order of size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(right), FadeIn(z0), FadeIn(z1), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(curves["z"]), FadeIn(names["z"]))
            vo.wait_until("b")
            self.play(Create(curves["y"]), FadeIn(names["y"]))
            vo.wait_until("c")
            self.play(Create(curves["n"]), FadeIn(names["n"]))
            vo.wait_until("d")
            self.play(Create(curves["c"]), FadeIn(names["c"]))
            vo.wait_until("e")
            self.play(Create(inv), FadeIn(inv_n))
        self.clear_scene()

    def why(self):
        R = load("rbc")["irf"]
        rows = VGroup(
            label(r"why each line looks as it does", font_size=27, color=E.ACCENT),
            label(r"consumption smoothing: \ the good times will fade, \ so spread the gain over years", font_size=22,
                  color=CONS),
            label(r"so the windfall goes into capital: \ investment swings hardest", font_size=22, color=INVEST),
            label(r"intertemporal substitution: \ a temporarily high wage makes now the time to work",
                  font_size=22, color=HOURS),
            label(r"with Hansen's labour, \ the wage equals $A c$: \ it can only move as consumption does",
                  font_size=22, color=CONS),
            label(rf"capital carries the shock forward: \ it peaks after {int(np.argmax(R['k']))} quarters, "
                  r"\ when most of the shock has faded", font_size=22, color=INVEST),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Each line has a reason. <bookmark mark='a'/> The household knows the good times will fade, so it does "
            "not spend the gain at once; it spreads it over years. That is consumption smoothing, from Part "
            "twenty-two. <bookmark mark='b'/> So the windfall goes into capital, and investment swings hardest. "
            "<bookmark mark='c'/> The wage is temporarily high, so now is the time to work: intertemporal "
            "substitution. <bookmark mark='d'/> With Hansen's indivisible labour, the labour condition says the "
            "wage equals A times consumption, so it can only move as slowly as consumption does. "
            "<bookmark mark='e'/> And the extra capital keeps output up after the shock has faded: capital peaks "
            f"after {int(np.argmax(R['k']))} quarters."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def scorecard(self):
        F = load("facts")
        d, m = F["data"], F["model"]
        items = [
            (r"output's s.d., \ \%", d["y"]["sd"], m["y"]["sd"], True, OUTPUT),
            (r"consumption, \ relative", d["c"]["rel"], m["c"]["rel"], False, CONS),
            (r"investment, \ relative", d["i"]["rel"], m["i"]["rel"], True, INVEST),
            (r"hours, \ relative", d["n"]["rel"], m["n"]["rel"], True, HOURS),
            (r"output per hour, \ relative", d["w"]["rel"], m["w"]["rel"], False, PROD),
            (r"hours with output per hour, \ correlation", d["corr_nw"], m["corr_nw"], False, HOLD),
            (r"output's persistence \ (one quarter)", d["ac_y"], m["ac_y"], True, OUTPUT),
        ]
        xs = [-3.6, 1.0, 3.3, 5.4]
        hrow = VGroup(*[label(h, font_size=20, color=GREY_B).move_to(RIGHT * x + UP * 2.45) for h, x in
                        zip((r"statistic", rf"US, \ {F['first'][:4]}--{F['last'][:4]}", r"the Island", r"verdict"),
                            xs)])
        rows = VGroup()
        for n, (name, a, b, ok, col) in enumerate(items):
            y = 1.75 - 0.62 * n
            mark = label(r"close" if ok else r"miss", font_size=20, color=E.GAIN if ok else E.MISS)
            rows.add(VGroup(label(name, font_size=20, color=col).move_to(RIGHT * xs[0] + UP * y),
                            label(f"{a:.2f}", font_size=21).move_to(RIGHT * xs[1] + UP * y),
                            label(f"{b:.2f}", font_size=21).move_to(RIGHT * xs[2] + UP * y),
                            mark.move_to(RIGHT * xs[3] + UP * y)))
        rule = Line(LEFT * 6.6, RIGHT * 6.6, stroke_color=GREY_D, stroke_width=1.5).move_to(UP * 2.12)
        foot = label(r"HP-filtered quarterly data; \ the Island: \ 20{,}000 simulated quarters, \ filtered the same "
                     r"way", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.55)
        tag = data_tag(r"BEA and BLS via FRED; \ the Island: \ simulated", corner=DR, font_size=12)
        with self.voiceover(
            "Now the test Prescott proposed: simulate the Island for twenty thousand quarters, filter the result "
            "exactly as the data were filtered, and put its numbers beside America's. <bookmark mark='a'/> The "
            f"size of the cycle: {m['y']['sd']:.1f} percent against {d['y']['sd']:.1f}. Close, from shocks sized "
            "only by the Solow residual. <bookmark mark='b'/> Consumption: the model's is far too smooth, though "
            "the data here include cars and other durables. <bookmark mark='c'/> Investment: about three times "
            "as volatile as output, against four and a half. The right order. <bookmark mark='d'/> Hours: "
            f"{m['n']['rel']:.2f} against {d['n']['rel']:.2f}, thanks to Hansen. <bookmark mark='e'/> Output per "
            "hour: too smooth. <bookmark mark='f'/> And the worst miss: in the model, hours and output per hour "
            f"move together, with a correlation of {m['corr_nw']:.2f}. In the data, there is no correlation at all. "
            "<bookmark mark='g'/> Persistence: close. A model with one shock and no frictions gets the broad shape "
            "of the cycle. That is what impressed people. The misses are where the next chapters dig."
        ) as vo:
            self.play(FadeIn(hrow), FadeIn(rule), FadeIn(foot), FadeIn(tag))
            for mk, r in zip("abcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
