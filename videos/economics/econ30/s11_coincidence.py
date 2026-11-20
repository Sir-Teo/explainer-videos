from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Coincidence(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The natural rate and the divine coincidence", r"When does stabilizing inflation also "
             r"stabilize output?", "Chapter nine. The natural rate and the divine coincidence.",
             lit={1898: r"Wicksell", 2007: r"Blanchard and Gal\'i"}, scale=("nation",), horizon=("a quarter", "a year"))
        self.wicksell()
        self.divine()

    def wicksell(self):
        rows = VGroup(
            label(r"Knut Wicksell, \ 1898: \ the natural rate of interest", font_size=26, color=E.ACCENT),
            label(r"the real rate at which output equals what flexible prices would give", font_size=22,
                  color=CB),
            label(r"a demand shock moves the natural rate: \ optimism raises it, \ fear lowers it", font_size=22,
                  color=OUTPUT),
            label(r"the central bank's job: \ move its rate with the natural rate", font_size=22, color=RATE),
            label(r"set the real rate below it, \ and demand runs ahead; \ above it, \ demand falls short",
                  font_size=22, color=GREY_A),
            label(r"the natural rate cannot be seen: \ only estimated \ (Part 31)", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Wicksell, \ \emph{Interest and Prices} (1898); \ Woodford, \ \emph{Interest and Prices} "
                            r"(2003)", corner=DR, font_size=12)
        with self.voiceover(
            "The IS curve's benchmark has an old name. <bookmark mark='a'/> In 1898 the Swedish economist Knut "
            "Wicksell called it the natural rate of interest: <bookmark mark='b'/> the real rate at which output "
            "equals what it would be with flexible prices. <bookmark mark='c'/> Demand shocks move it: optimism "
            "raises it, fear lowers it. <bookmark mark='d'/> So the central bank's job, in this model, is to move "
            "its rate with the natural rate. <bookmark mark='e'/> Hold the real rate below the natural rate and "
            "demand runs ahead of supply; above it, demand falls short. <bookmark mark='f'/> The trouble is that "
            "nobody can see the natural rate. It can only be estimated, as Part thirty-one does."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def _panel(self, R, center, title, col, lo, hi):
        q = np.array(R["q"])
        ax = plane([0, 11], [lo, hi], center=center, x_length=4.6, y_length=3.4, xticks=[0, 4, 8],
                   yticks=[lo, 0, hi], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0",
                   font_size=13)
        zero = seg(ax, 0, 0, 11, 0, GREY_D, 1.2)
        lines = VGroup(DashedVMobject(path(ax, q, np.clip(R["pi"], lo, hi), INFL, 3, smooth=False), num_dashes=24),
                       path(ax, q, np.clip(R["x"], lo, hi), OUTPUT, 4, smooth=False))
        t = label(title, font_size=19, color=col).next_to(ax, UP, buff=0.15)
        return VGroup(ax, zero, t), lines

    def divine(self):
        R = load("coincidence")
        d, c = R["demand"], R["cost"]
        pd_ = self._panel(d, LEFT * 3.4 + DOWN * 0.4, r"a demand shock, \ inflation held at target", OUTPUT,
                          -0.5, 0.5)
        pc_ = self._panel(c, RIGHT * 3.4 + DOWN * 0.4, r"a cost-push shock, \ inflation held at target", COST,
                          -2.5, 0.5)
        key = VGroup(label(r"green: \ output gap", font_size=18, color=OUTPUT),
                     label(r"red, \ dashed: \ inflation", font_size=18, color=INFL)).arrange(RIGHT, buff=0.6).to_edge(
            UP, buff=0.35)
        notes = VGroup(
            label(rf"output gap \ {d['x'][0]:+.3f}\%: \ zero as well", font_size=18, color=OUTPUT).next_to(
                pd_[0], DOWN, buff=0.3),
            label(rf"output gap \ {c['x'][0]:+.2f}\%: \ a trade-off", font_size=18, color=COST).next_to(
                pc_[0], DOWN, buff=0.3),
        )
        foot = label(r"Blanchard and Gal\'i, \ 2007: \ the coincidence holds only when nothing pushes costs on "
                     r"its own", font_size=19, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Blanchard and Gal\'i, \ \emph{JMCB} 39(s1) (2007); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now a remarkable property of the model. Suppose the central bank holds inflation at exactly its "
            "target, whatever it takes. <bookmark mark='a'/> After a demand shock, the output gap stays at zero "
            "too: moving the policy rate with the natural rate kills both at once. Olivier Blanchard and Jordi Galí "
            "called this the divine coincidence. <bookmark mark='b'/> But after a cost-push shock, holding "
            f"inflation at target means an output gap of {say_num(c['x'][0])} percent. "
            "<bookmark mark='c'/> The coincidence holds only when nothing pushes costs up on its own: no oil "
            "shocks, no wage push, no supply chains breaking. When those happen, the central bank must choose, "
            "and the next chapter asks how."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag), FadeIn(pd_[0]), FadeIn(pc_[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in pd_[1]], lag_ratio=0.3), FadeIn(notes[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in pc_[1]], lag_ratio=0.3), FadeIn(notes[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
