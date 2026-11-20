from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403

CHIP = ("#F2C14E", "#F25F5C")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ stay or withdraw?", r"You have a deposit, \ and a rumour. \ What do you do?",
             "Chapter two. Play it: stay, or withdraw?", lit={1983: r"Diamond and Dybvig"}, scale=("person",),
             horizon=("a day",))
        self.choose()
        self.reveal()

    def choose(self):
        d = load("dd")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        rows = VGroup(
            label(r"you have one coconut deposited at the Island's bank", font_size=23, color=GREY_A),
            label(rf"withdraw tomorrow: \ {d['c1']:.2f} \ \ wait until the loans are repaid: \ {d['c2']:.2f}",
                  font_size=24, color=DEPOSIT),
            label(r"you do not need the money tomorrow", font_size=23, color=GREY_A),
            label(r"a rumour: \ half of the other depositors will withdraw tomorrow", font_size=25, color=RUN),
            label(r"the bank pays withdrawers in full, \ selling loans early if it must", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.28).move_to(stage.box.get_top() + DOWN * 1.8)
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=28, color=c))
                         for c, t in zip(CHIP, (r"A: \ stay", r"B: \ withdraw"))]).arrange(RIGHT, buff=0.6)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(rows, DOWN, buff=0.5)
        ring = countdown().next_to(chips, DOWN, buff=0.35)
        with self.voiceover(
            "Your turn. You have deposited one coconut at the Island's bank. <bookmark mark='a'/> If you withdraw "
            f"tomorrow, the bank pays you {d['c1']:.2f}. If you wait until its loans are repaid, it promises "
            f"{d['c2']:.2f}. <bookmark mark='b'/> You do not need the money tomorrow. <bookmark mark='c'/> But you "
            "hear a rumour: half of the other depositors will withdraw tomorrow. <bookmark mark='d'/> The bank will "
            "pay them in full, selling loans early if it has to. Do you stay, or withdraw? Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        d = load("dd")
        ax = plane([0, 0.85], [0, 1.6], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75], yticks=[0, 0.5, 1.0, 1.5], xlabel=r"share of depositors withdrawing "
                   r"tomorrow", ylabel=r"what you get", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:g}",
                   font_size=16)
        stay = path(ax, d["f"], d["stay"], color=STAY, width=4)
        wd = seg(ax, 0, d["c1"], 0.85, d["c1"], color=RUN, width=3)
        thr = seg(ax, d["threshold"], 0, d["threshold"], d["c1"], color=WHITE, width=2, dashed=True)
        half = dot(ax, 0.5, d["at_half"], color=STAY, r=0.09)
        side = VGroup(
            label(rf"withdraw: \ {d['c1']:.2f}, \ while the bank lasts", font_size=20, color=RUN),
            label(r"stay: \ what is left, \\ shared among the stayers", font_size=20, color=STAY),
            label(rf"if half withdraw: \ stay and get {d['at_half']:.2f}", font_size=21, color=STAY),
            label(rf"beyond {100 * d['threshold']:.0f}\%, \ staying pays less: \\ everyone should run", font_size=21,
                  color=RUN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the arithmetic. <bookmark mark='a'/> A withdrawer gets "
            f"{d['c1']:.2f}, as long as the bank has anything left. <bookmark mark='b'/> A depositor who stays gets "
            "whatever is left when the loans are repaid, shared among the stayers. The more people withdraw, the "
            "more loans the bank sells early, and the less is left. <bookmark mark='c'/> If half withdraw, staying "
            f"still gets you {d['at_half']:.2f}: if you chose A, you were right. <bookmark mark='d'/> But if more "
            f"than about {100 * d['threshold']:.0f} percent withdraw, staying pays less than running. And if "
            "everyone believes everyone else will run, each is right to run. Nothing about the bank's loans has "
            "changed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(wd), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(stay), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromCenter(half), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(thr), FadeIn(side[3]))
        self.clear_scene()
